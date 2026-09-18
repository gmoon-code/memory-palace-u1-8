from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from export_content_studio_release_manifest import manifest as expand_manifest

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "release" / "content-studio" / "v1.0.0-rc1.json"
VERSION = ROOT / "release" / "content-studio" / "VERSION"
EXPECTED_VERSION = "1.0.0-rc1"
EXPECTED_IMPLEMENTATION = "cdf4bb2a1ea91415dd1634323ac5ab40ccba863f"
EXPECTED_TREE = "133a3bc9b00c2149662d4e6dba8517f0706b585c"
EXPECTED_BASELINE_MAIN = "6d561f19a19b07b9a386442d327db3ca12299bef"

ALLOWED_EVIDENCE = {
    ".github/workflows/qa.yml",
    "docs/admin/CONTENT_STUDIO_RELEASE_CANDIDATE.md",
    "docs/admin/CONTENT_STUDIO_RC1_CLEAN_REHEARSAL.md",
    "docs/admin/CONTENT_STUDIO_V1_RELEASE.md",
    "release/content-studio/VERSION",
    "release/content-studio/v1.0.0-rc1.json",
    "release/content-studio/v1.0.0.json",
    "scripts/export_content_studio_release_manifest.py",
    "scripts/qa_content_studio_release_candidate.py",
    "scripts/qa_content_studio_rc1_clean_rehearsal.py",
    "scripts/qa_content_studio_stable_release.py",
}

# Historical RC1 remains frozen. These files are narrowly scoped post-release
# maintenance discovered during the clean Windows teacher acceptance rehearsal.
ALLOWED_POST_RELEASE_MAINTENANCE = {
    "Backup Content Studio.cmd",
    "Restore Content Studio.cmd",
    "scripts/backup_content_studio_local.py",
    "scripts/qa_zero_cost_backup_restore.py",
    "scripts/qa_zero_cost_runtime.py",
    "distribution/content-studio-teacher/Install Content Studio.cmd",
    "distribution/content-studio-teacher/install_content_studio.py",
    "distribution/content-studio-teacher/START_HERE.txt",
    "distribution/content-studio-teacher/DAILY_USE.txt",
    "distribution/content-studio-teacher/BACKUP_AND_RECOVERY.txt",
    "distribution/content-studio-teacher/FIRST_RUN_CHECKLIST.txt",
    "docs/admin/CONTENT_STUDIO_TEACHER_HANDOFF.md",
    "release/content-studio/teacher-distribution-v1.0.0.json",
    "scripts/build_content_studio_teacher_distribution.py",
    "scripts/qa_content_studio_teacher_distribution.py",
    "server_data/.gitkeep",
}

KEY_OBJECTS = {
    "backend": "e50cc927229aaa04da05e9011242add339537993",
    "frontend/admin": "5ca9e35331d68bd156c4b596911c430ba9ec17c3",
    "frontend/js": "5df314588165696062ed431cba266154d8351ca5",
    ".env.example": "e9d3e685a128d5d827c2e576e947c10149f46c45",
    "Start Content Studio.cmd": "b097e7babef109ed20a6b927b47ded3d58e3731b",
    "Backup Content Studio.cmd": "5bcc9c28a78095057878bc2031cefe88dffd6bea",
    "Restore Content Studio.cmd": "da85a766c0d5abeeeb6ce8a7665bcad076da9233",
    "Repair Content Studio.cmd": "dbf331f485506da7f5fb4b8f43901f116b3fdd87",
    "Update Content Studio.cmd": "6801056db3ba6ff80b0a11efe0bd90965db05974",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"CONTENT STUDIO RELEASE CANDIDATE QA FAIL\n- {message}")


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
    )


def git_text(*args: str) -> str:
    return git(*args).stdout.strip()


def main() -> None:
    require(LOCK.exists(), "release lock is missing")
    require(VERSION.exists(), "release VERSION file is missing")
    require((ROOT / "docs/admin/CONTENT_STUDIO_RC1_CLEAN_REHEARSAL.md").exists(), "clean rehearsal evidence document is missing")
    require((ROOT / "scripts/qa_content_studio_rc1_clean_rehearsal.py").exists(), "clean rehearsal gate is missing")
    require(bool(VERSION.read_text(encoding="utf-8").strip()), "release VERSION file is empty")
    lock = json.loads(LOCK.read_text(encoding="utf-8"))

    require(lock.get("version") == EXPECTED_VERSION, "release lock version mismatch")
    require(lock.get("implementation_commit") == EXPECTED_IMPLEMENTATION, "implementation commit changed")
    require(lock.get("implementation_tree") == EXPECTED_TREE, "implementation tree changed")
    require(lock.get("baseline_main_commit") == EXPECTED_BASELINE_MAIN, "baseline main commit changed")
    require(lock.get("zero_cost_required") is True, "$0 requirement is not locked")

    implementation = git_text("rev-parse", f"{EXPECTED_IMPLEMENTATION}^{{commit}}")
    implementation_tree = git_text("rev-parse", f"{implementation}^{{tree}}")
    require(implementation == EXPECTED_IMPLEMENTATION, "implementation commit cannot be resolved exactly")
    require(implementation_tree == EXPECTED_TREE, "implementation tree no longer matches the lock")

    ancestor = git("merge-base", "--is-ancestor", EXPECTED_IMPLEMENTATION, "HEAD", check=False)
    require(ancestor.returncode == 0, "frozen implementation is not an ancestor of the candidate evidence head")

    # The RC1 artifact is historical evidence. Its immutable implementation
    # commit and tree are validated above. Later product work is allowed to
    # evolve HEAD without rewriting or weakening that historical evidence.

    student_diff = git(
        "diff",
        "--quiet",
        EXPECTED_BASELINE_MAIN,
        EXPECTED_IMPLEMENTATION,
        "--",
        "content",
        "frontend/index.html",
        "frontend/css",
        "frontend/js",
        check=False,
    )
    require(student_diff.returncode == 0, "frozen candidate changes published curriculum or student frontend relative to the production baseline")

    for path, expected_object in KEY_OBJECTS.items():
        actual = git_text("rev-parse", f"{EXPECTED_IMPLEMENTATION}:{path}")
        require(actual == expected_object, f"frozen object mismatch for {path}: {actual}")

    env_text = git_text("show", f"{EXPECTED_IMPLEMENTATION}:.env.example")
    for gate in (
        "MEMORY_PALACE_ADMIN_ENABLED=false",
        "MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED=false",
        "MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED=false",
        "MEMORY_PALACE_GITHUB_ALLOW_MERGE=false",
    ):
        require(gate in env_text, f"default safety gate is not locked off: {gate}")

    expanded = expand_manifest(EXPECTED_IMPLEMENTATION)
    require(expanded["commit"] == EXPECTED_IMPLEMENTATION, "expanded manifest commit mismatch")
    require(expanded["tree"] == EXPECTED_TREE, "expanded manifest tree mismatch")
    require(expanded["file_count"] > 100, "expanded exact manifest is unexpectedly small")
    paths = {item["path"] for item in expanded["files"]}
    for required in (
        "backend/admin_auth.py",
        "backend/admin_publication.py",
        "frontend/admin/workflow.js",
        "frontend/admin/usability.js",
        "scripts/bootstrap_content_studio_windows.py",
        "scripts/backup_content_studio_local.py",
        "scripts/restore_content_studio_local.py",
        "scripts/repair_content_studio_local.py",
        "scripts/update_content_studio_local.py",
        "tests/test_admin_acceptance_workflows.py",
        "Start Content Studio.cmd",
        "Backup Content Studio.cmd",
        "Restore Content Studio.cmd",
        "Repair Content Studio.cmd",
        "Update Content Studio.cmd",
    ):
        require(required in paths, f"exact manifest is missing {required}")

    with tempfile.TemporaryDirectory(prefix="content-studio-rc-") as temporary:
        first = Path(temporary) / "manifest-a.json"
        second = Path(temporary) / "manifest-b.json"
        text = json.dumps(expanded, indent=2, ensure_ascii=False) + "\n"
        first.write_text(text, encoding="utf-8")
        second.write_text(json.dumps(expand_manifest(EXPECTED_IMPLEMENTATION), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        require(first.read_bytes() == second.read_bytes(), "exact manifest expansion is not deterministic")

    print("CONTENT STUDIO RELEASE CANDIDATE QA PASS")
    print(f"- historical RC1 version: {EXPECTED_VERSION}")
    print(f"- current release pointer: {VERSION.read_text(encoding='utf-8').strip()}")
    print(f"- frozen implementation commit: {EXPECTED_IMPLEMENTATION}")
    print(f"- frozen implementation tree: {EXPECTED_TREE}")
    print(f"- exact tracked-file manifest entries: {expanded['file_count']}")
    print("- historical RC1 remains frozen at its immutable implementation commit and tree")
    print("- published AP Biology content and student frontend match the production baseline")
    print("- local $0 operation and publication-off defaults remain locked")
    print("- clean install and recovery rehearsal is present as historical RC1 evidence")


if __name__ == "__main__":
    main()
