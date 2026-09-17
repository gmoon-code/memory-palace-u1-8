from __future__ import annotations

import os
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.admin_auth import hash_password


RUNNER = ROOT / "scripts" / "run_content_studio_local.py"
SMOKE = ROOT / "scripts" / "smoke_content_studio.py"
USERNAME = "ci-zero-cost-owner"
PASSWORD = "CI-zero-cost-password-2026"


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_for_health(port: int, process: subprocess.Popen[bytes]) -> None:
    url = f"http://127.0.0.1:{port}/api/health"
    for _ in range(60):
        if process.poll() is not None:
            raise SystemExit(f"ZERO-COST RUNTIME QA FAIL: local server exited with {process.returncode}")
        try:
            with urllib.request.urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return
        except (OSError, urllib.error.URLError):
            pass
        time.sleep(0.25)
    raise SystemExit("ZERO-COST RUNTIME QA FAIL: local server did not become ready")


def start(env_file: Path, port: int) -> subprocess.Popen[bytes]:
    process = subprocess.Popen(
        [sys.executable, str(RUNNER), "--env-file", str(env_file)],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    wait_for_health(port, process)
    return process


def stop(process: subprocess.Popen[bytes]) -> None:
    process.terminate()
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def smoke(port: int) -> None:
    env = os.environ.copy()
    env.update(
        {
            "CONTENT_STUDIO_URL": f"http://127.0.0.1:{port}",
            "CONTENT_STUDIO_USERNAME": USERNAME,
            "CONTENT_STUDIO_PASSWORD": PASSWORD,
        }
    )
    subprocess.run(
        [sys.executable, str(SMOKE), "--allow-http-localhost"],
        cwd=ROOT,
        env=env,
        check=True,
    )


def audit_count(database: Path) -> int:
    if not database.exists():
        raise SystemExit("ZERO-COST RUNTIME QA FAIL: security database was not persisted")
    with sqlite3.connect(database) as connection:
        row = connection.execute("SELECT COUNT(*) FROM admin_audit").fetchone()
    return int(row[0])


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="content-studio-zero-cost-") as temp_raw:
        temp = Path(temp_raw)
        database = temp / "admin-security.sqlite3"
        port = free_port()
        env_file = temp / "local.env"
        env_file.write_text(
            "\n".join(
                [
                    "MEMORY_PALACE_ENV=development",
                    "MEMORY_PALACE_HOST=127.0.0.1",
                    f"MEMORY_PALACE_PORT={port}",
                    "MEMORY_PALACE_ADMIN_ENABLED=true",
                    f"MEMORY_PALACE_ADMIN_USERNAME={USERNAME}",
                    f"MEMORY_PALACE_ADMIN_PASSWORD_HASH={hash_password(PASSWORD)}",
                    "MEMORY_PALACE_ADMIN_SESSION_SECRET=ci-zero-cost-session-secret-with-more-than-32-characters",
                    f"MEMORY_PALACE_ADMIN_DB={database}",
                    f"MEMORY_PALACE_ADMIN_DRAFT_DB={temp / 'drafts.sqlite3'}",
                    f"MEMORY_PALACE_ADMIN_MEDIA_DB={temp / 'media.sqlite3'}",
                    f"MEMORY_PALACE_ADMIN_MEDIA_DIR={temp / 'media'}",
                    "MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED=false",
                    f"MEMORY_PALACE_ADMIN_PUBLICATION_DB={temp / 'publication.sqlite3'}",
                    f"MEMORY_PALACE_ADMIN_PUBLICATION_DIR={temp / 'publication'}",
                    "MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED=false",
                    "MEMORY_PALACE_GITHUB_ALLOW_MERGE=false",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        first = start(env_file, port)
        try:
            smoke(port)
        finally:
            stop(first)
        first_audit_count = audit_count(database)
        if first_audit_count < 2:
            raise SystemExit("ZERO-COST RUNTIME QA FAIL: first run did not persist expected audit events")

        second = start(env_file, port)
        try:
            smoke(port)
        finally:
            stop(second)
        second_audit_count = audit_count(database)
        if second_audit_count <= first_audit_count:
            raise SystemExit("ZERO-COST RUNTIME QA FAIL: audit state did not survive process restart")

        print("ZERO-COST CONTENT STUDIO RUNTIME QA PASS")
        print("- authenticated local smoke passed twice")
        print("- service restarted using the same local state directory")
        print(f"- persistent audit events increased from {first_audit_count} to {second_audit_count}")
        print("- publication and GitHub publication remained disabled")


if __name__ == "__main__":
    main()
