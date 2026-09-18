from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


PRODUCT = "The Story Method - Content Studio"
REPOSITORY = "gmoon-code/memory-palace-u1-8"
REPOSITORY_URL = "https://github.com/gmoon-code/memory-palace-u1-8.git"
TARGET_BRANCH = "main"
TARGET_COMMIT = "f5d4fe65d56797803e324f5a66805765a6c07714"
TARGET_VERSION = "1.0.0"
PACKAGE_MANIFEST = "PACKAGE_MANIFEST.json"


class InstallError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_package(package_dir: Path) -> dict:
    manifest_path = package_dir / PACKAGE_MANIFEST
    if not manifest_path.is_file():
        raise InstallError("PACKAGE_MANIFEST.json is missing from the extracted onboarding package.")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InstallError("PACKAGE_MANIFEST.json could not be read.") from exc

    if manifest.get("archive_type") != "story-method-content-studio-teacher-onboarding":
        raise InstallError("This folder is not a recognized Content Studio teacher onboarding package.")
    if manifest.get("content_studio_version") != TARGET_VERSION:
        raise InstallError("The onboarding package version does not match this installer.")
    if manifest.get("validated_runtime_commit") != TARGET_COMMIT:
        raise InstallError("The onboarding package runtime commit does not match this installer.")
    if manifest.get("credentials_included") is not False or manifest.get("private_state_included") is not False:
        raise InstallError("The onboarding package does not confirm exclusion of credentials and private state.")

    records = manifest.get("files")
    if not isinstance(records, list) or not records:
        raise InstallError("The onboarding package file manifest is empty or invalid.")

    expected_paths: set[str] = set()
    for record in records:
        if not isinstance(record, dict):
            raise InstallError("The onboarding package contains an invalid file record.")
        relative = str(record.get("path", ""))
        if not relative or relative == PACKAGE_MANIFEST or "/" in relative or "\\" in relative:
            raise InstallError(f"Unsafe onboarding package file entry: {relative!r}")
        expected_paths.add(relative)
        target = package_dir / relative
        if not target.is_file():
            raise InstallError(f"Onboarding package file is missing: {relative}")
        if target.stat().st_size != int(record.get("size", -1)):
            raise InstallError(f"Onboarding package file size mismatch: {relative}")
        if sha256_file(target) != record.get("sha256"):
            raise InstallError(f"Onboarding package SHA-256 mismatch: {relative}")

    actual_paths = {
        item.name
        for item in package_dir.iterdir()
        if item.is_file() and item.name != PACKAGE_MANIFEST
    }
    if actual_paths != expected_paths:
        raise InstallError("The extracted onboarding package contains unexpected or missing files.")
    return manifest


def run(command: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "command failed"
        raise InstallError(f"{' '.join(command)} failed. {detail}")
    return completed


def git_output(destination: Path, *args: str) -> str:
    return run(["git", "-C", str(destination), *args]).stdout.strip()


def require_prerequisites() -> None:
    if os.name != "nt":
        raise InstallError("This onboarding installer is for Windows.")
    if sys.version_info < (3, 10):
        raise InstallError("Content Studio requires Python 3.10 or newer.")
    if shutil.which("git") is None:
        raise InstallError(
            "Git was not found. Install the free Git for Windows client and run this installer again."
        )


def choose_destination(raw: str | None) -> Path:
    default = Path.home() / "Story Method Content Studio"
    if raw:
        destination = Path(raw).expanduser()
    else:
        entered = input(f"Install folder [{default}]: ").strip().strip('"')
        destination = Path(entered).expanduser() if entered else default
    return destination.resolve()


def require_fresh_destination(destination: Path) -> None:
    if destination.exists():
        try:
            has_items = any(destination.iterdir())
        except OSError as exc:
            raise InstallError(f"Cannot inspect the installation folder: {destination}") from exc
        if has_items:
            raise InstallError(
                f"The installation folder already contains files: {destination}. "
                "This installer will not reset, replace, or overwrite an existing Content Studio checkout."
            )
    destination.parent.mkdir(parents=True, exist_ok=True)


def clone_validated_runtime(destination: Path) -> None:
    print()
    print("Downloading the validated Content Studio repository...")
    run(["git", "clone", "--no-checkout", REPOSITORY_URL, str(destination)])

    print(f"Selecting validated runtime {TARGET_COMMIT}...")
    run(["git", "-C", str(destination), "checkout", "-B", TARGET_BRANCH, TARGET_COMMIT])
    run(
        [
            "git",
            "-C",
            str(destination),
            "branch",
            "--set-upstream-to",
            f"origin/{TARGET_BRANCH}",
            TARGET_BRANCH,
        ]
    )


def verify_checkout(destination: Path) -> None:
    origin = git_output(destination, "remote", "get-url", "origin")
    if origin not in {
        REPOSITORY_URL,
        "https://github.com/gmoon-code/memory-palace-u1-8",
    }:
        raise InstallError("The cloned Git origin does not match the official Story Method repository.")

    head = git_output(destination, "rev-parse", "HEAD")
    if head != TARGET_COMMIT:
        raise InstallError(f"Installed checkout ended on unexpected commit {head}.")

    branch = git_output(destination, "branch", "--show-current")
    if branch != TARGET_BRANCH:
        raise InstallError(f"Installed checkout is not on the supported {TARGET_BRANCH} branch.")

    status = git_output(destination, "status", "--porcelain", "--untracked-files=all")
    if status:
        raise InstallError("The new Content Studio checkout is unexpectedly dirty.")

    version_path = destination / "release" / "content-studio" / "VERSION"
    if not version_path.is_file() or version_path.read_text(encoding="utf-8").strip() != TARGET_VERSION:
        raise InstallError("The installed Content Studio VERSION file does not match v1.0.0.")

    if not (destination / "server_data" / ".gitkeep").is_file():
        raise InstallError("The validated local-state placeholder is missing from the installed checkout.")

    for launcher in (
        "Start Content Studio.cmd",
        "Backup Content Studio.cmd",
        "Restore Content Studio.cmd",
        "Repair Content Studio.cmd",
        "Update Content Studio.cmd",
    ):
        if not (destination / launcher).is_file():
            raise InstallError(f"Required Content Studio launcher is missing: {launcher}")


def start_content_studio(destination: Path) -> int:
    launcher = destination / "Start Content Studio.cmd"
    print()
    print("Validated installation complete.")
    print(f"Installed at: {destination}")
    print(f"Content Studio version: {TARGET_VERSION}")
    print(f"Validated runtime commit: {TARGET_COMMIT}")
    print("No paid service, billing account, payment method, or cloud database was used.")
    print()
    print("Starting Content Studio for first-time owner setup...")
    return subprocess.call(["cmd.exe", "/c", str(launcher)], cwd=destination)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Install the validated zero-cost Story Method Content Studio on Windows."
    )
    parser.add_argument("--install-dir", help="Optional installation folder")
    parser.add_argument(
        "--validate-package",
        action="store_true",
        help="Validate the extracted onboarding package and exit without installing",
    )
    parser.add_argument(
        "--no-start",
        action="store_true",
        help="Install and verify the checkout without starting Content Studio",
    )
    args = parser.parse_args()

    package_dir = Path(__file__).resolve().parent
    try:
        validate_package(package_dir)
        if args.validate_package:
            print("CONTENT STUDIO TEACHER ONBOARDING PACKAGE VALIDATION PASS")
            print(f"- version: {TARGET_VERSION}")
            print(f"- validated runtime: {TARGET_COMMIT}")
            print("- credentials and private Content Studio state are excluded")
            print("- no paid service is required")
            return 0

        require_prerequisites()
        destination = choose_destination(args.install_dir)
        require_fresh_destination(destination)
        clone_validated_runtime(destination)
        verify_checkout(destination)
        if args.no_start:
            print(f"Validated Content Studio installed at {destination}")
            return 0
        return start_content_studio(destination)
    except KeyboardInterrupt:
        print("\nInstallation cancelled. Existing Content Studio data was not overwritten.")
        return 130
    except (InstallError, OSError, subprocess.SubprocessError) as exc:
        print()
        print(f"INSTALLATION STOPPED: {exc}")
        print("No existing Content Studio checkout was reset or overwritten.")
        print("No paid service, billing account, or payment method was used.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
