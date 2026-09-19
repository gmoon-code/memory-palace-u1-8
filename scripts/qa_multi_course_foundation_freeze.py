from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "release" / "architecture" / "multi-course-foundation-v1.0.0.json"

ALLOWED_FREEZE_EVIDENCE = {
    ".github/workflows/qa.yml",
    "docs/architecture/MULTI_COURSE_FOUNDATION_FREEZE.md",
    "docs/architecture/MULTI_COURSE_INTEGRATION_GATE.md",
    "release/architecture/multi-course-foundation-v1.0.0.json",
    "scripts/qa_multi_course_foundation_freeze.py",
}

TREE_PATHS = {
    "repository_tree": None,
    "backend_tree": "backend",
    "content_tree": "content",
    "ap_biology_content_tree": "content/ap-biology",
    "ap_chemistry_fixture_tree": "content/ap-chemistry",
    "frontend_tree": "frontend",
    "frontend_admin_tree": "frontend/admin",
    "frontend_student_js_tree": "frontend/js",
    "platform_tree": "platform",
    "course_packages_tree": "platform/course-packages",
    "package_schemas_tree": "platform/schemas",
    "scripts_tree": "scripts",
    "tests_tree": "tests",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"MULTI-COURSE FOUNDATION FREEZE FAIL\n- {message}")


def git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def object_at(ref: str, path: str | None) -> str:
    spec = f"{ref}^{{tree}}" if path is None else f"{ref}:{path}"
    return git("rev-parse", spec)


def json_at(ref: str, path: str) -> dict:
    raw = git("show", f"{ref}:{path}")
    return json.loads(raw)


def main() -> None:
    require(MANIFEST.is_file(), "freeze manifest is missing")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    require(
        manifest.get("schema") == "story-method-multi-course-foundation-freeze-1.0",
        "unexpected freeze schema",
    )
    baseline = str(manifest.get("implementation_commit") or "")
    require(len(baseline) == 40, "implementation commit is missing")
    require(
        git("rev-parse", f"{baseline}^{{commit}}") == baseline,
        "frozen implementation commit cannot be resolved",
    )
    require(
        object_at(baseline, None) == manifest.get("implementation_tree"),
        "frozen repository tree does not match the manifest",
    )
    require(
        manifest.get("rollback_commit") == baseline,
        "rollback commit is not the frozen implementation commit",
    )
    require(
        manifest.get("rollback_ref") == "freeze/multi-course-foundation-2026-09-19",
        "rollback reference changed",
    )

    fingerprints = manifest.get("git_object_fingerprints") or {}
    for key, path in TREE_PATHS.items():
        require(key in fingerprints, f"missing source fingerprint: {key}")
        require(
            object_at(baseline, path) == fingerprints[key],
            f"source fingerprint changed for {key}",
        )

    file_fingerprints = manifest.get("package_file_fingerprints") or {}
    for path, expected in file_fingerprints.items():
        require(
            git("rev-parse", f"{baseline}:{path}") == expected,
            f"package fingerprint changed for {path}",
        )

    registry = json_at(baseline, "platform/courses.json")
    courses = {
        str(item.get("course_id")): item
        for item in registry.get("courses", [])
        if isinstance(item, dict) and item.get("course_id")
    }
    biology = courses.get("ap-biology") or {}
    chemistry = courses.get("ap-chemistry") or {}
    require(
        biology.get("status") == "available" and biology.get("student_visible") is True,
        "AP Biology frozen registry state changed",
    )
    require(
        chemistry.get("status") == "development" and chemistry.get("student_visible") is False,
        "AP Chemistry frozen registry state changed",
    )

    checkpoint = str(manifest.get("freeze_checkpoint_commit") or "")
    require(len(checkpoint) == 40, "freeze checkpoint commit is missing")
    require(
        git("rev-parse", f"{checkpoint}^{{commit}}") == checkpoint,
        "freeze checkpoint commit cannot be resolved",
    )
    require(
        object_at(checkpoint, None) == manifest.get("freeze_checkpoint_tree"),
        "freeze checkpoint tree does not match the manifest",
    )

    checkpoint_ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", baseline, checkpoint],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    require(checkpoint_ancestor.returncode == 0, "freeze checkpoint does not descend from the implementation")

    changed = {
        line.strip()
        for line in git("diff", "--name-only", f"{baseline}..{checkpoint}").splitlines()
        if line.strip()
    }
    unexpected = sorted(changed - ALLOWED_FREEZE_EVIDENCE)
    require(
        not unexpected,
        "freeze checkpoint changed protected implementation files: " + ", ".join(unexpected),
    )

    for key, path in (
        ("backend_tree", "backend"),
        ("content_tree", "content"),
        ("frontend_tree", "frontend"),
        ("platform_tree", "platform"),
    ):
        require(
            object_at(checkpoint, path) == fingerprints[key],
            f"freeze checkpoint changed protected {path} scope",
        )

    current = git("rev-parse", "HEAD")
    current_ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", checkpoint, current],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    require(current_ancestor.returncode == 0, "current head does not descend from the freeze checkpoint")

    evidence = manifest.get("acceptance_evidence") or []
    for path in evidence:
        require((ROOT / path).is_file(), f"acceptance evidence is missing: {path}")

    actions = manifest.get("validated_actions") or {}
    require(actions.get("run_id") == 35435465751, "validated Actions run changed")
    require(actions.get("conclusion") == "success", "freeze does not record successful validation")
    require(actions.get("validated_commit") == baseline, "validated commit does not match baseline")

    safety = manifest.get("safety_contract") or {}
    for key in (
        "ap_biology_curriculum_changed_by_freeze",
        "ap_chemistry_real_curriculum_started",
        "ap_chemistry_writes_enabled",
        "student_pages_exposes_ap_chemistry",
        "admin_assets_exposed_to_student_pages",
    ):
        require(safety.get(key) is False, f"safety contract unexpectedly enables {key}")
    require(safety.get("main_merged") is False, "freeze incorrectly records a main merge")
    require(safety.get("publication_defaults_remain_closed") is True, "publication safety default is not locked")

    print("MULTI-COURSE FOUNDATION FREEZE PASS")
    print(f"- implementation commit locked at {baseline}")
    print(f"- repository tree locked at {manifest['implementation_tree']}")
    print("- architecture-critical source trees and package blobs match the frozen fingerprints")
    print("- AP Biology remains the production course and AP Chemistry remains a hidden read-only fixture")
    print("- freeze checkpoint changed no protected runtime, curriculum, frontend, or platform scope")
    print(f"- freeze checkpoint locked at {checkpoint}")
    print(f"- rollback reference recorded as {manifest['rollback_ref']}")
    print("- later development may proceed while this historical checkpoint remains verifiable")
    print("- prior classroom/browser acceptance run is preserved as successful evidence")


if __name__ == "__main__":
    main()
