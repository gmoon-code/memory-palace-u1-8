from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = ROOT / "content-studio-backups"
ENV_FILE = ROOT / ".env.content-studio-local"
VENV_DIR = ROOT / ".venv"
REQUIREMENTS = ROOT / "requirements.txt"
REQUIREMENTS_MARKER = VENV_DIR / ".content-studio-requirements.sha256"
EXPECTED_REPOSITORY = "gmoon-code/memory-palace-u1-8"
EXPECTED_WORKFLOW = "Memory Palace QA"
ALLOWED_BRANCHES = {"admin/content-studio-local-updater", "main"}
APPROVED_ORIGINS = {
    "https://github.com/gmoon-code/memory-palace-u1-8",
    "https://github.com/gmoon-code/memory-palace-u1-8.git",
    "git@github.com:gmoon-code/memory-palace-u1-8.git",
    "ssh://git@github.com/gmoon-code/memory-palace-u1-8.git",
}
VALIDATION_COMMANDS = (
    ("scripts/qa_zero_cost_rehearsal.py",),
    ("scripts/qa_zero_cost_runtime.py",),
    ("scripts/qa_zero_cost_windows_launcher.py",),
    ("scripts/qa_zero_cost_backup_restore.py",),
    ("scripts/qa_zero_cost_local_updater.py",),
)


class UpdateError(RuntimeError):
    pass


def run(command: list[str], *, cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "command failed"
        raise UpdateError(f"{' '.join(command)}: {detail}")
    return completed


def git_output(*args: str, cwd: Path = ROOT) -> str:
    return run(["git", *args], cwd=cwd).stdout.strip()


def require_git_checkout() -> None:
    if shutil.which("git") is None:
        raise UpdateError(
            "Git was not found. The safe updater requires the free Git client so it can verify, "
            "fast-forward, and automatically roll code back. The current Content Studio can still be used."
        )
    if git_output("rev-parse", "--is-inside-work-tree") != "true":
        raise UpdateError(
            "This folder is not a Git checkout. The updater made no changes. "
            "Use the current Content Studio until a normal Git clone is available."
        )


def current_branch() -> str:
    branch = git_output("branch", "--show-current")
    if not branch:
        raise UpdateError("The repository is in detached-HEAD mode. The updater made no changes.")
    return branch


def require_approved_branch(branch: str) -> None:
    if branch not in ALLOWED_BRANCHES:
        allowed = ", ".join(sorted(ALLOWED_BRANCHES))
        raise UpdateError(
            f"Updates are disabled on branch {branch!r}. Approved local update branches are: {allowed}."
        )


def require_approved_origin() -> str:
    origin = git_output("remote", "get-url", "origin")
    if origin not in APPROVED_ORIGINS:
        raise UpdateError(
            "The Git origin does not match the official Story Method repository. "
            "The updater refused to download or apply code."
        )
    return origin


def require_clean_worktree() -> None:
    status = git_output("status", "--porcelain", "--untracked-files=all")
    if status:
        raise UpdateError(
            "The repository contains local code-file changes or untracked source files. "
            "The updater will not overwrite them. Content Studio data and credentials in ignored folders do not count."
        )


def local_port(env_file: Path = ENV_FILE) -> int:
    port = 8000
    if not env_file.exists():
        return port
    try:
        for raw in env_file.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key.strip() == "MEMORY_PALACE_PORT":
                candidate = int(value.strip())
                if 1 <= candidate <= 65535:
                    port = candidate
    except (OSError, ValueError):
        pass
    return port


def require_content_studio_stopped(port: int) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.25)
        if sock.connect_ex(("127.0.0.1", port)) == 0:
            raise UpdateError(
                f"Something is listening on the Content Studio port {port}. "
                "Stop Content Studio with Ctrl+C before updating, then run the updater again."
            )


def fetch_target(branch: str) -> str:
    remote_ref = f"refs/remotes/origin/{branch}"
    run(["git", "fetch", "--quiet", "origin", f"refs/heads/{branch}:{remote_ref}"])
    return git_output("rev-parse", remote_ref)


def is_ancestor(base_sha: str, target_sha: str, *, cwd: Path = ROOT) -> bool:
    completed = run(
        ["git", "merge-base", "--is-ancestor", base_sha, target_sha],
        cwd=cwd,
        check=False,
    )
    return completed.returncode == 0


def require_fast_forward(current_sha: str, target_sha: str) -> None:
    if not is_ancestor(current_sha, target_sha):
        raise UpdateError(
            "The remote update is not a fast-forward from the current local version. "
            "The updater refused to rewrite history or discard code."
        )


def github_actions_approved(target_sha: str, *, timeout: float = 10.0) -> bool:
    query = urllib.parse.urlencode(
        {"head_sha": target_sha, "status": "completed", "per_page": "100"}
    )
    url = f"https://api.github.com/repos/{EXPECTED_REPOSITORY}/actions/runs?{query}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "story-method-content-studio-local-updater",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.load(response)
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        raise UpdateError(
            "GitHub could not be reached to verify the exact update commit. "
            "No code was changed. Try again when the connection is available."
        ) from exc

    for item in payload.get("workflow_runs", []):
        if (
            item.get("name") == EXPECTED_WORKFLOW
            and item.get("head_sha") == target_sha
            and item.get("status") == "completed"
            and item.get("conclusion") == "success"
        ):
            return True
    return False


def require_remote_qa(target_sha: str) -> None:
    if not github_actions_approved(target_sha):
        raise UpdateError(
            "The exact remote commit has not completed the required Memory Palace QA workflow successfully. "
            "The updater will wait for a validated commit and made no changes."
        )


def requirements_digest(path: Path = REQUIREMENTS) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def venv_python() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def ensure_virtual_environment() -> Path:
    python_path = venv_python()
    if python_path.exists():
        return python_path
    print("Creating the local Python environment for the updated Content Studio...")
    run([sys.executable, "-m", "venv", str(VENV_DIR)])
    if not python_path.exists():
        raise UpdateError("The local Content Studio Python environment could not be created.")
    return python_path


def install_current_requirements() -> None:
    python_path = ensure_virtual_environment()
    if not REQUIREMENTS.exists():
        raise UpdateError("requirements.txt is missing from the selected Content Studio version.")
    print("Synchronizing the free local Python dependencies...")
    run(
        [
            str(python_path),
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "--no-input",
            "-r",
            str(REQUIREMENTS),
        ]
    )
    REQUIREMENTS_MARKER.parent.mkdir(parents=True, exist_ok=True)
    REQUIREMENTS_MARKER.write_text(requirements_digest() + "\n", encoding="utf-8")


def create_state_backup() -> Path:
    from scripts.backup_content_studio_local import create_backup

    archive = create_backup()
    print(f"Safety backup created: {archive}")
    return archive


def write_recovery_record(*, old_sha: str, target_sha: str, branch: str, backup: Path) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    record = BACKUP_DIR / f"content-studio-code-recovery-{stamp}.json"
    record.write_text(
        json.dumps(
            {
                "record_type": "story-method-content-studio-code-recovery",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "branch": branch,
                "old_commit": old_sha,
                "target_commit": target_sha,
                "state_backup": str(backup),
                "credentials_in_backup": False,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return record


def fast_forward_to(target_sha: str, *, cwd: Path = ROOT) -> None:
    run(["git", "merge", "--ff-only", target_sha], cwd=cwd)


def rollback_code(old_sha: str, *, cwd: Path = ROOT) -> None:
    run(["git", "reset", "--hard", old_sha], cwd=cwd)


def validate_updated_version() -> None:
    python_path = venv_python()
    print("Validating the updated local Content Studio...")
    for relative_parts in VALIDATION_COMMANDS:
        path = ROOT.joinpath(*relative_parts)
        if not path.exists():
            raise UpdateError(f"Required update validation is missing: {path.relative_to(ROOT)}")
        run([str(python_path), str(path)])
    run([str(python_path), "-m", "compileall", "-q", "backend", "scripts", "tests"])
    require_clean_worktree()


def update() -> int:
    require_git_checkout()
    branch = current_branch()
    require_approved_branch(branch)
    require_approved_origin()
    require_clean_worktree()
    require_content_studio_stopped(local_port())

    current_sha = git_output("rev-parse", "HEAD")
    print(f"Current validated code: {current_sha}")
    print("Checking the official GitHub branch for a newer validated version...")
    target_sha = fetch_target(branch)
    print(f"Remote candidate:       {target_sha}")

    if current_sha == target_sha:
        print("Content Studio is already up to date. No files were changed.")
        return 0

    require_fast_forward(current_sha, target_sha)
    require_remote_qa(target_sha)

    backup = create_state_backup()
    record = write_recovery_record(
        old_sha=current_sha,
        target_sha=target_sha,
        branch=branch,
        backup=backup,
    )
    print(f"Code recovery record: {record}")

    try:
        print("Applying the validated fast-forward update...")
        fast_forward_to(target_sha)
        install_current_requirements()
        validate_updated_version()
    except Exception as exc:
        print()
        print(f"Update validation failed: {exc}")
        print("Rolling the code back to the previously working commit...")
        rollback_error: Exception | None = None
        try:
            rollback_code(current_sha)
            install_current_requirements()
        except Exception as inner:
            rollback_error = inner
        if rollback_error is not None:
            raise UpdateError(
                f"The update failed and automatic code rollback also needs attention: {rollback_error}. "
                f"Recovery commit: {current_sha}. State backup: {backup}"
            ) from exc
        raise UpdateError(
            f"The update failed local validation, so the code was automatically restored to {current_sha}. "
            f"The safety backup remains at {backup}."
        ) from exc

    final_sha = git_output("rev-parse", "HEAD")
    if final_sha != target_sha:
        raise UpdateError("The updater finished on an unexpected commit. Stop and inspect the checkout.")

    print()
    print("Content Studio update completed successfully.")
    print(f"Updated code: {final_sha}")
    print(f"Safety backup: {backup}")
    print("Local credentials and Content Studio state were preserved.")
    print("Publication and GitHub merge controls remain governed by the existing local zero-cost safety mode.")
    print("No paid service, billing account, or payment method was used.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Safely fast-forward a local zero-cost Content Studio checkout after exact-commit CI verification."
    )
    parser.parse_args()
    try:
        return update()
    except KeyboardInterrupt:
        print("\nUpdate cancelled. No additional changes will be made.")
        return 130
    except UpdateError as exc:
        print()
        print(f"UPDATE STOPPED: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
