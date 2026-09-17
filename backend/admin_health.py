from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import sqlite3
import subprocess
import sys
import time
from typing import Any
import zipfile

from . import admin_auth
from .settings import HOST, ROOT

EXPECTED_REPOSITORY = "gmoon-code/memory-palace-u1-8"
APPROVED_ORIGINS = {
    "https://github.com/gmoon-code/memory-palace-u1-8.git",
    "git@github.com:gmoon-code/memory-palace-u1-8.git",
}
LOCAL_RELEASE_BRANCHES = {
    "main",
    "admin/content-studio-local-updater",
    "admin/content-studio-health-repair",
}
PUBLICATION_LOCKS = (
    "MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED",
    "MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED",
    "MEMORY_PALACE_GITHUB_ALLOW_MERGE",
)
DATABASE_ENV = {
    "admin security": ("MEMORY_PALACE_ADMIN_DB", "server_data/admin-security.sqlite3"),
    "draft and revision": ("MEMORY_PALACE_ADMIN_DRAFT_DB", "server_data/content-studio-drafts.sqlite3"),
    "media": ("MEMORY_PALACE_ADMIN_MEDIA_DB", "server_data/content-studio-media.sqlite3"),
    "publication history": ("MEMORY_PALACE_ADMIN_PUBLICATION_DB", "server_data/content-studio-publication.sqlite3"),
}
REPAIR_ACTIONS = {
    "ensure_private_directories",
    "checkpoint_databases",
    "cleanup_temp_files",
    "create_backup",
    "repair_all",
}
STALE_TEMP_SECONDS = 24 * 60 * 60
MIN_FREE_BYTES = 500 * 1024 * 1024


class HealthRepairError(RuntimeError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _flag(name: str) -> bool:
    return os.getenv(name, "false").strip().lower() in {"1", "true", "yes", "on"}


def _path_from_env(name: str, fallback: str) -> Path:
    raw = Path(os.getenv(name, fallback)).expanduser()
    if not raw.is_absolute():
        raw = ROOT / raw
    return raw.resolve()


def _check(
    check_id: str,
    category: str,
    status: str,
    title: str,
    message: str,
    *,
    repair_action: str | None = None,
    external_repair: str | None = None,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "id": check_id,
        "category": category,
        "status": status,
        "title": title,
        "message": message,
        "repairable": repair_action is not None,
        "repair_action": repair_action,
        "external_repair": external_repair,
        "details": details or {},
    }


def _run_git(*args: str) -> tuple[int, str]:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=8,
        )
    except (OSError, subprocess.SubprocessError):
        return 127, ""
    return completed.returncode, completed.stdout.strip()


def _sqlite_integrity(path: Path) -> tuple[str, str]:
    if not path.exists():
        return "missing", "Database has not been created yet."
    if not path.is_file():
        return "error", "Configured database path is not a regular file."
    try:
        uri = f"file:{path.as_posix()}?mode=ro"
        with sqlite3.connect(uri, uri=True, timeout=3.0) as connection:
            row = connection.execute("PRAGMA quick_check").fetchone()
        if row and str(row[0]).lower() == "ok":
            return "ok", "SQLite quick_check returned ok."
        return "error", f"SQLite quick_check returned {row[0] if row else 'no result'}."
    except sqlite3.DatabaseError as exc:
        return "error", f"SQLite could not validate this database: {exc}"


def _requirements_digest() -> str | None:
    path = ROOT / "requirements.txt"
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _venv_python() -> Path:
    windows = ROOT / ".venv" / "Scripts" / "python.exe"
    if windows.exists():
        return windows
    return ROOT / ".venv" / "bin" / "python"


def _validate_latest_backup() -> tuple[str, str, dict[str, Any]]:
    backup_dir = ROOT / "content-studio-backups"
    archives = sorted(backup_dir.glob("content-studio-backup-*.zip"), reverse=True) if backup_dir.exists() else []
    if not archives:
        return "warning", "No local Content Studio backup is available yet.", {}
    archive = archives[0]
    checksum_path = archive.with_suffix(archive.suffix + ".sha256")
    try:
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        if checksum_path.exists():
            expected = checksum_path.read_text(encoding="utf-8").strip().split()[0]
            if expected != digest:
                return "error", "The newest backup archive does not match its SHA-256 checksum.", {"archive": archive.name}
        with zipfile.ZipFile(archive, "r") as handle:
            manifest = json.loads(handle.read("manifest.json").decode("utf-8"))
            if manifest.get("archive_type") != "story-method-content-studio-local-backup":
                return "error", "The newest backup has an unexpected archive type.", {"archive": archive.name}
            expected_files = manifest.get("files") or []
            for record in expected_files:
                relative = str(record.get("path") or "")
                pure = PurePosixPath(relative)
                if not relative or pure.is_absolute() or ".." in pure.parts:
                    return "error", "The newest backup manifest contains an unsafe path.", {"archive": archive.name}
                payload = handle.read(f"server_data/{relative}")
                if len(payload) != int(record.get("size") or -1):
                    return "error", f"Backup size mismatch for {relative}.", {"archive": archive.name}
                if hashlib.sha256(payload).hexdigest() != record.get("sha256"):
                    return "error", f"Backup hash mismatch for {relative}.", {"archive": archive.name}
        return "ok", "The newest backup passed manifest and SHA-256 verification.", {"archive": archive.name}
    except (OSError, ValueError, KeyError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        return "error", f"The newest backup could not be validated: {exc}", {"archive": archive.name}


def health_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    loopback_ok = HOST in {"127.0.0.1", "localhost", "::1"}
    checks.append(
        _check(
            "loopback_binding",
            "security",
            "ok" if loopback_ok else "error",
            "Local-only network binding",
            f"Content Studio is bound to {HOST}." if loopback_ok else f"Content Studio is bound to {HOST}; zero-cost local mode requires a loopback address.",
            external_repair="Repair Content Studio.cmd" if not loopback_ok else None,
        )
    )

    try:
        admin_auth.AdminConfig.from_env().validate()
        auth_status = "ok"
        auth_message = "Owner username, scrypt password hash, and session secret are configured."
    except admin_auth.AdminConfigurationError as exc:
        auth_status = "error"
        auth_message = str(exc)
    checks.append(_check("owner_credentials", "security", auth_status, "Owner authentication configuration", auth_message))

    enabled_locks = [name for name in PUBLICATION_LOCKS if _flag(name)]
    checks.append(
        _check(
            "publication_locks",
            "zero_cost",
            "ok" if not enabled_locks else "error",
            "Publication safety locks",
            "Publication, GitHub delivery, and server-side merge are all disabled." if not enabled_locks else "Local zero-cost mode has an enabled publication gate: " + ", ".join(enabled_locks),
            external_repair="Repair Content Studio.cmd" if enabled_locks else None,
        )
    )

    paid_blueprints = [name for name in ("render.yaml", "railway.toml", "fly.toml") if (ROOT / name).exists()]
    checks.append(
        _check(
            "zero_cost_boundary",
            "zero_cost",
            "ok" if not paid_blueprints else "error",
            "Zero-cost deployment boundary",
            "No paid-hosting blueprint is present in this checkout." if not paid_blueprints else "Paid-hosting configuration is present: " + ", ".join(paid_blueprints),
        )
    )

    state_dir = (ROOT / "server_data").resolve()
    state_ok = state_dir.exists() and state_dir.is_dir() and os.access(state_dir, os.W_OK)
    checks.append(
        _check(
            "private_state_directory",
            "storage",
            "ok" if state_ok else "error",
            "Private state directory",
            f"Private state is writable at {state_dir}." if state_ok else "The private server_data directory is missing or not writable.",
            repair_action="ensure_private_directories" if not state_ok else None,
        )
    )

    media_dir = _path_from_env("MEMORY_PALACE_ADMIN_MEDIA_DIR", "server_data/content-studio-media")
    publication_dir = _path_from_env("MEMORY_PALACE_ADMIN_PUBLICATION_DIR", "server_data/content-studio-publications")
    for check_id, title, path in (
        ("media_directory", "Private media directory", media_dir),
        ("publication_directory", "Private publication workspace", publication_dir),
    ):
        okay = path.exists() and path.is_dir() and os.access(path, os.W_OK)
        checks.append(
            _check(
                check_id,
                "storage",
                "ok" if okay else "warning",
                title,
                f"Writable at {path}." if okay else f"{path} has not been created or is not writable yet.",
                repair_action="ensure_private_directories" if not okay else None,
            )
        )

    try:
        free_bytes = shutil.disk_usage(ROOT).free
        disk_status = "ok" if free_bytes >= MIN_FREE_BYTES else "warning"
        checks.append(
            _check(
                "free_disk_space",
                "storage",
                disk_status,
                "Local free disk space",
                f"{free_bytes / (1024 ** 3):.2f} GiB is currently free.",
                details={"free_bytes": free_bytes},
            )
        )
    except OSError as exc:
        checks.append(_check("free_disk_space", "storage", "warning", "Local free disk space", f"Disk space could not be read: {exc}"))

    for label, (env_name, fallback) in DATABASE_ENV.items():
        path = _path_from_env(env_name, fallback)
        status, message = _sqlite_integrity(path)
        visible_status = "warning" if status == "missing" else status
        checks.append(
            _check(
                f"database_{env_name.lower()}",
                "database",
                visible_status,
                f"{label.title()} database",
                f"{message} Path: {path}",
                repair_action="checkpoint_databases" if status == "ok" else None,
            )
        )

    latest_status, latest_message, latest_details = _validate_latest_backup()
    checks.append(
        _check(
            "latest_backup",
            "backup",
            latest_status,
            "Latest local backup",
            latest_message,
            repair_action="create_backup" if latest_status != "ok" else None,
            details=latest_details,
        )
    )

    requirements_digest = _requirements_digest()
    marker = ROOT / ".venv" / ".content-studio-requirements.sha256"
    python_path = _venv_python()
    if not python_path.exists():
        venv_status = "warning"
        venv_message = "The private .venv Python environment is missing."
    elif requirements_digest is None:
        venv_status = "error"
        venv_message = "requirements.txt is missing."
    elif not marker.exists() or marker.read_text(encoding="utf-8").strip() != requirements_digest:
        venv_status = "warning"
        venv_message = "The local dependency marker does not match requirements.txt."
    else:
        venv_status = "ok"
        venv_message = "The private Python environment matches the current requirements digest."
    checks.append(
        _check(
            "python_environment",
            "tooling",
            venv_status,
            "Private Python environment",
            venv_message,
            external_repair="Repair Content Studio.cmd" if venv_status != "ok" else None,
        )
    )

    git_code, origin = _run_git("remote", "get-url", "origin")
    origin_ok = git_code == 0 and origin in APPROVED_ORIGINS
    checks.append(
        _check(
            "repository_origin",
            "repository",
            "ok" if origin_ok else "warning",
            "Official repository origin",
            f"Origin is {origin}." if origin_ok else "The updater could not confirm the exact approved GitHub origin.",
            details={"origin": origin if git_code == 0 else None, "expected_repository": EXPECTED_REPOSITORY},
        )
    )

    branch_code, branch = _run_git("rev-parse", "--abbrev-ref", "HEAD")
    branch_ok = branch_code == 0 and branch in LOCAL_RELEASE_BRANCHES
    checks.append(
        _check(
            "updater_branch",
            "repository",
            "ok" if branch_ok else "warning",
            "Updater-ready branch",
            f"Current branch {branch} is an approved local release channel." if branch_ok else f"Current branch {branch or 'unknown'} is outside the approved updater release channels.",
            details={"branch": branch if branch_code == 0 else None},
        )
    )

    head_code, head = _run_git("rev-parse", "HEAD")
    checks.append(
        _check(
            "code_version",
            "repository",
            "ok" if head_code == 0 and len(head) == 40 else "warning",
            "Current code version",
            head if head_code == 0 else "Git commit could not be determined.",
            details={"commit": head if head_code == 0 else None},
        )
    )

    gitignore = ROOT / ".gitignore"
    ignore_text = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    required_ignore_tokens = ("server_data", ".env.content-studio-local", "content-studio-backups", ".venv")
    missing_ignore = [token for token in required_ignore_tokens if token not in ignore_text]
    checks.append(
        _check(
            "private_paths_ignored",
            "security",
            "ok" if not missing_ignore else "error",
            "Private local paths excluded from Git",
            "Credentials, local databases, backups, and the private environment are covered by .gitignore." if not missing_ignore else "Missing .gitignore coverage for: " + ", ".join(missing_ignore),
        )
    )

    counts = {status: sum(1 for item in checks if item["status"] == status) for status in ("ok", "warning", "error", "info")}
    overall = "blocked" if counts["error"] else ("attention" if counts["warning"] else "healthy")
    zero_cost = not enabled_locks and not paid_blueprints and loopback_ok
    return {
        "generated_at": _now(),
        "overall": overall,
        "zero_cost_local_mode": zero_cost,
        "summary": {
            **counts,
            "total": len(checks),
            "repairable": sum(1 for item in checks if item["repairable"]),
        },
        "checks": checks,
        "safe_repair_actions": sorted(REPAIR_ACTIONS),
        "external_environment_repair": "Repair Content Studio.cmd",
    }


def _ensure_private_directories() -> dict[str, Any]:
    paths = {
        (ROOT / "server_data").resolve(),
        _path_from_env("MEMORY_PALACE_ADMIN_MEDIA_DIR", "server_data/content-studio-media"),
        _path_from_env("MEMORY_PALACE_ADMIN_PUBLICATION_DIR", "server_data/content-studio-publications"),
        (ROOT / "content-studio-backups").resolve(),
    }
    created: list[str] = []
    for path in paths:
        existed = path.exists()
        path.mkdir(parents=True, exist_ok=True)
        if not path.is_dir():
            raise HealthRepairError(f"Could not create private directory: {path}")
        if not existed:
            created.append(str(path))
    return {"action": "ensure_private_directories", "created": created}


def _checkpoint_databases() -> dict[str, Any]:
    checked: list[str] = []
    for env_name, fallback in DATABASE_ENV.values():
        path = _path_from_env(env_name, fallback)
        if not path.exists() or not path.is_file():
            continue
        try:
            with sqlite3.connect(path, timeout=5.0) as connection:
                connection.execute("PRAGMA wal_checkpoint(PASSIVE)")
                connection.execute("PRAGMA optimize")
            checked.append(str(path))
        except sqlite3.DatabaseError as exc:
            raise HealthRepairError(f"SQLite maintenance failed for {path}: {exc}") from exc
    return {"action": "checkpoint_databases", "databases": checked}


def _cleanup_temp_files() -> dict[str, Any]:
    state_dir = (ROOT / "server_data").resolve()
    if not state_dir.exists():
        return {"action": "cleanup_temp_files", "removed": []}
    cutoff = time.time() - STALE_TEMP_SECONDS
    removed: list[str] = []
    for path in state_dir.rglob("*"):
        if path.is_symlink() or not path.is_file():
            continue
        if path.suffix.lower() not in {".tmp", ".part"} and not path.name.endswith("~"):
            continue
        try:
            if path.stat().st_mtime >= cutoff:
                continue
            path.unlink()
            removed.append(str(path.relative_to(state_dir)))
        except OSError as exc:
            raise HealthRepairError(f"Could not remove stale temporary file {path}: {exc}") from exc
    return {"action": "cleanup_temp_files", "removed": removed}


def _create_backup() -> dict[str, Any]:
    script = ROOT / "scripts" / "backup_content_studio_local.py"
    if not script.exists():
        raise HealthRepairError("Local backup script is missing")
    try:
        completed = subprocess.run(
            [sys.executable, str(script)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise HealthRepairError(f"Backup could not be started: {exc}") from exc
    if completed.returncode != 0:
        raise HealthRepairError(completed.stderr.strip() or "Local backup failed")
    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    return {"action": "create_backup", "output": lines[-4:]}


def run_repair(action: str) -> dict[str, Any]:
    if action not in REPAIR_ACTIONS:
        raise HealthRepairError("Unknown or unsafe repair action")
    if action == "ensure_private_directories":
        result = _ensure_private_directories()
    elif action == "checkpoint_databases":
        result = _checkpoint_databases()
    elif action == "cleanup_temp_files":
        result = _cleanup_temp_files()
    elif action == "create_backup":
        result = _create_backup()
    else:
        results = [_create_backup(), _ensure_private_directories(), _checkpoint_databases(), _cleanup_temp_files()]
        result = {"action": "repair_all", "steps": results}
    return {"ok": True, "performed_at": _now(), **result, "report": health_report()}
