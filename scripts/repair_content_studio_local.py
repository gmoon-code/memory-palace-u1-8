from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VENV_DIR = ROOT / ".venv"
ENV_FILE = ROOT / ".env.content-studio-local"
REQUIREMENTS = ROOT / "requirements.txt"
REQUIREMENTS_MARKER = VENV_DIR / ".content-studio-requirements.sha256"
BACKUP_SCRIPT = ROOT / "scripts" / "backup_content_studio_local.py"
HEALTH_QA = ROOT / "scripts" / "qa_content_studio_health_repair.py"
LOCKED_VALUES = {
    "MEMORY_PALACE_HOST": "127.0.0.1",
    "MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED": "false",
    "MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED": "false",
    "MEMORY_PALACE_GITHUB_ALLOW_MERGE": "false",
}


class RepairError(RuntimeError):
    pass


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "command failed"
        raise RepairError(detail)
    return completed


def require_supported_python() -> None:
    if sys.version_info < (3, 10):
        raise RepairError("Content Studio requires Python 3.10 or newer.")


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def enforce_local_locks(path: Path) -> None:
    if not path.exists():
        raise RepairError(
            "Local owner configuration is missing. Start Content Studio once to complete first-time setup."
        )
    original = path.read_text(encoding="utf-8").splitlines()
    seen: set[str] = set()
    updated: list[str] = []
    for line in original:
        if "=" in line and not line.lstrip().startswith("#"):
            key = line.split("=", 1)[0].strip()
            if key in LOCKED_VALUES:
                updated.append(f"{key}={LOCKED_VALUES[key]}")
                seen.add(key)
                continue
        updated.append(line)
    if any(key not in seen for key in LOCKED_VALUES):
        updated.append("")
        updated.append("# Local zero-cost safety locks maintained by Repair Content Studio.")
        for key, value in LOCKED_VALUES.items():
            if key not in seen:
                updated.append(f"{key}={value}")
    path.write_text("\n".join(updated).rstrip() + "\n", encoding="utf-8")


def configured_port(values: dict[str, str]) -> int:
    try:
        value = int(values.get("MEMORY_PALACE_PORT", "8000"))
    except ValueError:
        return 8000
    return value if 1 <= value <= 65535 else 8000


def require_content_studio_stopped(values: dict[str, str]) -> None:
    port = configured_port(values)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        if sock.connect_ex(("127.0.0.1", port)) == 0:
            raise RepairError(
                f"Content Studio is still running on 127.0.0.1:{port}. Stop it before running repair."
            )


def create_state_backup() -> None:
    if not BACKUP_SCRIPT.exists():
        raise RepairError("Backup helper is missing; repair will not continue without a safety backup.")
    completed = run([sys.executable, str(BACKUP_SCRIPT)])
    for line in completed.stdout.splitlines():
        if line.strip():
            print(line)


def ensure_private_directories() -> None:
    for path in (
        ROOT / "server_data",
        ROOT / "server_data" / "content-studio-media",
        ROOT / "server_data" / "content-studio-publications",
        ROOT / "content-studio-backups",
    ):
        path.mkdir(parents=True, exist_ok=True)


def requirements_digest() -> str:
    if not REQUIREMENTS.exists():
        raise RepairError("requirements.txt is missing from this checkout.")
    return hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()


def venv_python(venv: Path = VENV_DIR) -> Path:
    windows = venv / "Scripts" / "python.exe"
    if windows.exists() or os.name == "nt":
        return windows
    return venv / "bin" / "python"


def environment_healthy() -> bool:
    python_path = venv_python()
    if not python_path.exists():
        return False
    check = run(
        [
            str(python_path),
            "-c",
            "import fastapi,httpx,pytest,uvicorn; print('ok')",
        ],
        check=False,
    )
    if check.returncode != 0:
        return False
    if not REQUIREMENTS_MARKER.exists():
        return False
    return REQUIREMENTS_MARKER.read_text(encoding="utf-8").strip() == requirements_digest()


def install_dependencies(python_path: Path) -> None:
    completed = run(
        [
            str(python_path),
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "--no-input",
            "-r",
            str(REQUIREMENTS),
        ],
        check=False,
    )
    if completed.returncode != 0:
        raise RepairError(
            completed.stderr.strip()
            or "Free local Python dependencies could not be installed. Check the internet connection and retry."
        )
    REQUIREMENTS_MARKER.write_text(requirements_digest() + "\n", encoding="utf-8")


def rebuild_environment() -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    old = ROOT / f".venv.repair-old-{stamp}"
    had_old = VENV_DIR.exists()
    if had_old:
        VENV_DIR.rename(old)
    try:
        run([sys.executable, "-m", "venv", str(VENV_DIR)])
        python_path = venv_python()
        if not python_path.exists():
            raise RepairError("The replacement virtual environment did not create a Python executable.")
        install_dependencies(python_path)
    except Exception:
        if VENV_DIR.exists():
            shutil.rmtree(VENV_DIR, ignore_errors=True)
        if had_old and old.exists():
            old.rename(VENV_DIR)
        raise
    else:
        if old.exists():
            shutil.rmtree(old, ignore_errors=True)


def refresh_environment_if_needed(force_rebuild: bool) -> None:
    if force_rebuild or not environment_healthy():
        print("Rebuilding the private Content Studio Python environment...")
        rebuild_environment()
    else:
        print("Private Python environment already matches requirements.txt.")


def validate_repaired_installation() -> None:
    python_path = venv_python()
    run([str(python_path), "-m", "compileall", "-q", "backend", "scripts", "tests"])
    if HEALTH_QA.exists():
        completed = run([str(python_path), str(HEALTH_QA)])
        for line in completed.stdout.splitlines():
            if line.strip():
                print(line)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Repair the local zero-cost Content Studio installation without touching curriculum or private working data."
    )
    parser.add_argument(
        "--rebuild-venv",
        action="store_true",
        help="Force a clean rebuild of the private Python environment",
    )
    args = parser.parse_args()

    try:
        require_supported_python()
        values = parse_env_file(ENV_FILE)
        require_content_studio_stopped(values)
        print("Creating a safety backup before repair...")
        create_state_backup()
        ensure_private_directories()
        enforce_local_locks(ENV_FILE)
        refresh_environment_if_needed(args.rebuild_venv)
        validate_repaired_installation()
    except (RepairError, OSError, subprocess.SubprocessError) as exc:
        print()
        print(f"REPAIR FAILED: {exc}")
        print("Private Content Studio data was not intentionally deleted. A pre-repair backup was required before maintenance.")
        return 1

    print()
    print("CONTENT STUDIO LOCAL REPAIR PASS")
    print("- local-only binding restored")
    print("- publication, GitHub publication, and merge locks forced off")
    print("- private state directories preserved")
    print("- free Python environment validated")
    print("- no paid hosting, paid API, cloud database, or billing account used")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
