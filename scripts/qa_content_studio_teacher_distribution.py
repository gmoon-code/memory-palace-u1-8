from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / "release" / "content-studio" / "teacher-distribution-v1.0.0.json"
BUILDER_PATH = ROOT / "scripts" / "build_content_studio_teacher_distribution.py"
SOURCE_DIR = ROOT / "distribution" / "content-studio-teacher"
EXPECTED_VERSION = "1.0.0"
EXPECTED_REVISION = "2026-09-18.1"
EXPECTED_RUNTIME = "f5d4fe65d56797803e324f5a66805765a6c07714"
EXPECTED_RUNTIME_TREE = "5b2ff607bf5c4077a86bc059a0493b166c76828a"
EXPECTED_REPOSITORY = "gmoon-code/memory-palace-u1-8"
EXPECTED_SOURCE_FILES = {
    "Install Content Studio.cmd",
    "install_content_studio.py",
    "START_HERE.txt",
    "DAILY_USE.txt",
    "BACKUP_AND_RECOVERY.txt",
    "FIRST_RUN_CHECKLIST.txt",
}
EXPECTED_PACKAGE_FILES = EXPECTED_SOURCE_FILES | {"RELEASE_INFO.json", "PACKAGE_MANIFEST.json"}


def fail(message: str) -> None:
    raise SystemExit(f"CONTENT STUDIO TEACHER DISTRIBUTION QA FAIL\n- {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def git_text(*args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        fail(completed.stderr.strip() or f"git {' '.join(args)} failed")
    return completed.stdout.strip()


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def load_builder():
    spec = importlib.util.spec_from_file_location("content_studio_teacher_distribution_builder", BUILDER_PATH)
    if spec is None or spec.loader is None:
        fail("teacher distribution builder could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    require(LOCK_PATH.is_file(), "teacher distribution release lock is missing")
    require(BUILDER_PATH.is_file(), "teacher distribution builder is missing")
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))

    require(lock.get("content_studio_version") == EXPECTED_VERSION, "distribution version mismatch")
    require(lock.get("distribution_revision") == EXPECTED_REVISION, "distribution revision mismatch")
    require(lock.get("repository") == EXPECTED_REPOSITORY, "distribution repository mismatch")
    require(lock.get("runtime_branch") == "main", "distribution runtime branch is not main")
    require(lock.get("validated_runtime_commit") == EXPECTED_RUNTIME, "validated runtime commit mismatch")
    require(lock.get("validated_runtime_tree") == EXPECTED_RUNTIME_TREE, "validated runtime tree mismatch")
    require(lock.get("zero_cost_required") is True, "zero-cost requirement is not locked")
    require(lock.get("credentials_included") is False, "distribution lock permits credentials")
    require(lock.get("private_state_included") is False, "distribution lock permits private state")
    require(lock.get("publication_enabled_by_default") is False, "publication-off default is not locked")
    require(lock.get("github_publication_enabled_by_default") is False, "GitHub publication-off default is not locked")
    require(lock.get("github_merge_enabled_by_default") is False, "GitHub merge-off default is not locked")
    require(lock.get("windows_teacher_acceptance", {}).get("status") == "passed", "Windows teacher acceptance is not locked as passed")

    require(git_text("rev-parse", f"{EXPECTED_RUNTIME}^{{commit}}") == EXPECTED_RUNTIME, "validated runtime commit cannot be resolved")
    require(git_text("rev-parse", f"{EXPECTED_RUNTIME}^{{tree}}") == EXPECTED_RUNTIME_TREE, "validated runtime tree mismatch in Git history")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", EXPECTED_RUNTIME, "HEAD"],
        cwd=ROOT,
    )
    require(ancestor.returncode == 0, "validated teacher runtime is not an ancestor of the distribution head")
    require(git_text("show", f"{EXPECTED_RUNTIME}:release/content-studio/VERSION") == EXPECTED_VERSION, "validated runtime VERSION mismatch")

    actual_sources = {item.name for item in SOURCE_DIR.iterdir() if item.is_file()}
    require(actual_sources == EXPECTED_SOURCE_FILES, f"unexpected teacher distribution source files: {sorted(actual_sources ^ EXPECTED_SOURCE_FILES)}")

    installer = (SOURCE_DIR / "install_content_studio.py").read_text(encoding="utf-8")
    launcher = (SOURCE_DIR / "Install Content Studio.cmd").read_text(encoding="utf-8")
    combined_docs = "\n".join(
        (SOURCE_DIR / name).read_text(encoding="utf-8")
        for name in sorted(EXPECTED_SOURCE_FILES - {"install_content_studio.py", "Install Content Studio.cmd"})
    )

    for marker in (
        f'TARGET_COMMIT = "{EXPECTED_RUNTIME}"',
        'TARGET_BRANCH = "main"',
        'REPOSITORY = "gmoon-code/memory-palace-u1-8"',
        "validate_package",
        "require_fresh_destination",
        "--no-checkout",
        "checkout",
        "--set-upstream-to",
        "server_data",
        ".gitkeep",
    ):
        require(marker in installer, f"installer safety marker is missing: {marker}")

    require('"%~dp0install_content_studio.py"' in launcher, "Windows installer does not quote its Python script path")
    require("paid service" in launcher.lower(), "Windows installer does not state the zero-cost boundary")
    require("127.0.0.1" in combined_docs, "teacher instructions do not state the local-only binding")
    require("publication" in combined_docs.lower(), "teacher instructions do not cover publication safety")
    require("backup" in combined_docs.lower() and "restore" in combined_docs.lower(), "teacher instructions do not cover backup and restore")

    builder = load_builder()
    with tempfile.TemporaryDirectory(prefix="content-studio-teacher-distribution-") as temp_raw:
        temp = Path(temp_raw)
        first = temp / "teacher-a.zip"
        second = temp / "teacher-b.zip"
        builder.build(first)
        builder.build(second)
        require(first.read_bytes() == second.read_bytes(), "teacher distribution ZIP is not deterministic")
        require(first.with_suffix(".zip.sha256").is_file(), "teacher distribution SHA-256 sidecar is missing")

        with zipfile.ZipFile(first, "r") as archive:
            names = set(archive.namelist())
            require(names == EXPECTED_PACKAGE_FILES, f"unexpected archive members: {sorted(names ^ EXPECTED_PACKAGE_FILES)}")
            require(all("/" not in name and "\\" not in name for name in names), "archive contains nested or unsafe paths")
            manifest = json.loads(archive.read("PACKAGE_MANIFEST.json").decode("utf-8"))
            release = json.loads(archive.read("RELEASE_INFO.json").decode("utf-8"))

            require(manifest.get("validated_runtime_commit") == EXPECTED_RUNTIME, "package manifest runtime mismatch")
            require(manifest.get("credentials_included") is False, "package manifest permits credentials")
            require(manifest.get("private_state_included") is False, "package manifest permits private state")
            require(release.get("validated_runtime_commit") == EXPECTED_RUNTIME, "release info runtime mismatch")
            require(release.get("windows_teacher_acceptance") == "passed", "release info does not record Windows acceptance")

            records = manifest.get("files")
            require(isinstance(records, list), "package manifest file records are invalid")
            record_paths = {record.get("path") for record in records}
            require(record_paths == EXPECTED_PACKAGE_FILES - {"PACKAGE_MANIFEST.json"}, "package manifest membership mismatch")
            for record in records:
                payload = archive.read(record["path"])
                require(len(payload) == record["size"], f"package size mismatch for {record['path']}")
                require(sha256(payload) == record["sha256"], f"package hash mismatch for {record['path']}")

            for name in names:
                lowered = name.lower()
                require(".env" not in lowered, f"credential-like file included: {name}")
                require(".sqlite" not in lowered, f"private database included: {name}")
                require(".git" not in lowered, f"Git metadata included: {name}")
                require(".venv" not in lowered, f"virtual environment included: {name}")

        extract = temp / "extracted"
        extract.mkdir()
        with zipfile.ZipFile(first, "r") as archive:
            archive.extractall(extract)
        validation = subprocess.run(
            [sys.executable, str(extract / "install_content_studio.py"), "--validate-package"],
            cwd=extract,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        require(validation.returncode == 0, f"packaged installer self-validation failed: {validation.stderr or validation.stdout}")
        require("VALIDATION PASS" in validation.stdout, "packaged installer did not report validation success")

    curriculum_diff = subprocess.run(
        [
            "git",
            "diff",
            "--quiet",
            EXPECTED_RUNTIME,
            "HEAD",
            "--",
            "content/ap-biology",
        ],
        cwd=ROOT,
    )
    require(curriculum_diff.returncode == 0, "teacher distribution integration changed the locked AP Biology curriculum tree")

    print("CONTENT STUDIO TEACHER DISTRIBUTION QA PASS")
    print(f"- version: {EXPECTED_VERSION}")
    print(f"- distribution revision: {EXPECTED_REVISION}")
    print(f"- validated Windows teacher runtime: {EXPECTED_RUNTIME}")
    print("- deterministic onboarding ZIP and SHA-256 sidecar passed")
    print("- package manifest and installer self-validation passed")
    print("- credentials, private state, Git metadata, and virtual environment excluded")
    print("- existing installs are protected from installer overwrite")
    print("- locked AP Biology curriculum content unchanged")
    print("- local-only zero-cost and publication-off boundaries preserved")


if __name__ == "__main__":
    main()
