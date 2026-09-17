from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
VENV_DIR = ROOT / ".venv"
ENV_FILE = ROOT / ".env.content-studio-local"
REQUIREMENTS = ROOT / "requirements.txt"
REQUIREMENTS_MARKER = VENV_DIR / ".content-studio-requirements.sha256"
SETUP_SCRIPT = ROOT / "scripts" / "setup_content_studio_local.py"
RUN_SCRIPT = ROOT / "scripts" / "run_content_studio_local.py"


def fail(message: str, *, code: int = 1) -> int:
    print()
    print(f"ERROR: {message}")
    return code


def require_supported_python() -> None:
    if sys.version_info < (3, 10):
        raise SystemExit(
            "Content Studio requires Python 3.10 or newer. "
            "Install a current free Python 3 release and start again."
        )


def venv_python() -> Path:
    return VENV_DIR / "Scripts" / "python.exe"


def create_virtual_environment() -> None:
    python_path = venv_python()
    if python_path.exists():
        return

    print("Creating the private Content Studio Python environment...")
    subprocess.run(
        [sys.executable, "-m", "venv", str(VENV_DIR)],
        cwd=ROOT,
        check=True,
    )
    if not python_path.exists():
        raise SystemExit("The Content Studio virtual environment could not be created.")


def requirements_digest() -> str:
    return hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()


def dependencies_are_current(expected_digest: str) -> bool:
    if not REQUIREMENTS_MARKER.exists():
        return False
    try:
        return REQUIREMENTS_MARKER.read_text(encoding="utf-8").strip() == expected_digest
    except OSError:
        return False


def install_dependencies_if_needed() -> None:
    expected_digest = requirements_digest()
    if dependencies_are_current(expected_digest):
        print("Content Studio dependencies are already ready.")
        return

    print("Preparing the free local Python dependencies...")
    command = [
        str(venv_python()),
        "-m",
        "pip",
        "install",
        "--disable-pip-version-check",
        "--no-input",
        "-r",
        str(REQUIREMENTS),
    ]
    completed = subprocess.run(command, cwd=ROOT)
    if completed.returncode != 0:
        raise SystemExit(
            "The free Python dependencies could not be installed. "
            "Check the internet connection and try again. No paid service is required."
        )

    REQUIREMENTS_MARKER.write_text(expected_digest + "\n", encoding="utf-8")


def ensure_local_credentials() -> None:
    if ENV_FILE.exists():
        print("Existing local Content Studio credentials found.")
        return

    print()
    print("First-time setup")
    print("Create the local owner sign-in. The password itself is never stored.")
    completed = subprocess.run(
        [str(venv_python()), str(SETUP_SCRIPT), "--env-file", str(ENV_FILE)],
        cwd=ROOT,
    )
    if completed.returncode != 0:
        raise SystemExit("Content Studio owner setup was not completed.")


def run_content_studio() -> int:
    print()
    print("Starting Content Studio on this computer only...")
    print("Your browser will open automatically when the local server is ready.")
    print("Press Ctrl+C in this window whenever you want to stop Content Studio.")
    return subprocess.call(
        [
            str(venv_python()),
            str(RUN_SCRIPT),
            "--env-file",
            str(ENV_FILE),
            "--open-browser",
        ],
        cwd=ROOT,
    )


def main() -> int:
    if os.name != "nt":
        return fail(
            "This helper is the Windows one-click launcher. "
            "Use scripts/run_content_studio_local.py on other operating systems."
        )

    require_supported_python()
    if not REQUIREMENTS.exists():
        return fail(f"Repository requirements file is missing: {REQUIREMENTS}")
    if not SETUP_SCRIPT.exists() or not RUN_SCRIPT.exists():
        return fail("Content Studio setup files are missing from this repository checkout.")

    try:
        create_virtual_environment()
        install_dependencies_if_needed()
        ensure_local_credentials()
        return run_content_studio()
    except KeyboardInterrupt:
        print("\nContent Studio stopped.")
        return 0
    except (OSError, subprocess.SubprocessError) as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
