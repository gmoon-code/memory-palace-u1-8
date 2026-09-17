from __future__ import annotations

from contextlib import contextmanager
import hashlib
import io
from pathlib import Path
import socket
import subprocess
import sys
import tarfile
import tempfile
import time
from typing import Iterator

import httpx

from export_content_studio_release_manifest import manifest as expand_manifest

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_IMPLEMENTATION = "cdf4bb2a1ea91415dd1634323ac5ab40ccba863f"
EXPECTED_TREE = "133a3bc9b00c2149662d4e6dba8517f0706b585c"
EXPECTED_BASELINE_MAIN = "6d561f19a19b07b9a386442d327db3ca12299bef"
SCENE_ID = "scene:unit-8:U8-J1:0"
USERNAME = "rc1-rehearsal-owner"
PASSWORD = "RC1-clean-rehearsal-password-2026"
TITLE_A = "RC1 clean rehearsal recovery point"
TITLE_B = "RC1 temporary mutation after backup"
STUDENT_SCOPES = (
    "content",
    "frontend/index.html",
    "frontend/css",
    "frontend/js",
)


class RehearsalError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RehearsalError(message)


def run(command: list[str], *, cwd: Path = ROOT, input_text: str | None = None, check: bool = True, timeout: int = 180) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(command, cwd=cwd, input=input_text, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    if check and completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "command failed"
        raise RehearsalError(f"{' '.join(command)}: {detail}")
    return completed


def git(*args: str) -> str:
    return run(["git", *args]).stdout.strip()


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def extract_frozen_implementation(destination: Path) -> dict:
    expanded = expand_manifest(EXPECTED_IMPLEMENTATION)
    require(expanded["commit"] == EXPECTED_IMPLEMENTATION, "manifest resolved a different implementation commit")
    require(expanded["tree"] == EXPECTED_TREE, "manifest resolved a different implementation tree")
    archive = subprocess.run(["git", "archive", "--format=tar", EXPECTED_IMPLEMENTATION], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with tarfile.open(fileobj=io.BytesIO(archive.stdout), mode="r:") as handle:
        root = destination.resolve()
        for member in handle.getmembers():
            path = (destination / member.name).resolve()
            try:
                path.relative_to(root)
            except ValueError as exc:
                raise RehearsalError(f"unsafe archive path: {member.name}") from exc
            if member.isdev() or member.issym() or member.islnk():
                raise RehearsalError(f"unexpected non-regular archive entry: {member.name}")
        handle.extractall(destination)
    expected_paths = {str(item["path"]) for item in expanded["files"]}
    actual_paths = {path.relative_to(destination).as_posix() for path in destination.rglob("*") if path.is_file()}
    require(actual_paths == expected_paths, "clean extraction does not match the exact tracked-file path manifest")
    for item in expanded["files"]:
        require(item["type"] == "blob", f"unsupported Git object in frozen manifest: {item['path']}")
        path = destination / str(item["path"])
        data = path.read_bytes()
        require(len(data) == int(item["size"]), f"size mismatch in clean extraction: {item['path']}")
        require(git_blob_sha(data) == item["git_object"], f"Git blob mismatch in clean extraction: {item['path']}")
    return expanded


def tree_digest(root: Path, scopes: tuple[str, ...] = STUDENT_SCOPES) -> str:
    digest = hashlib.sha256()
    for scope in scopes:
        target = root / scope
        paths = [target] if target.is_file() else sorted(path for path in target.rglob("*") if path.is_file())
        for path in paths:
            relative = path.relative_to(root).as_posix().encode("utf-8")
            data = path.read_bytes()
            digest.update(len(relative).to_bytes(4, "big"))
            digest.update(relative)
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
    return digest.hexdigest()


def private_state_is_clean(root: Path) -> bool:
    if (root / ".env.content-studio-local").exists():
        return False
    state_dir = root / "server_data"
    if not state_dir.exists():
        return True
    return all((not path.is_file()) or path.name == ".gitkeep" for path in state_dir.rglob("*"))


def run_clean_first_use_setup(root: Path) -> Path:
    env_file = root / ".env.content-studio-local"
    setup = root / "scripts" / "setup_content_studio_local.py"
    require(setup.exists(), "frozen implementation is missing local setup")
    completed = run([sys.executable, str(setup), "--env-file", str(env_file)], cwd=root, input_text=f"{USERNAME}\n{PASSWORD}\n{PASSWORD}\n", timeout=120)
    require(env_file.exists(), "first-use setup did not create the local environment file")
    combined = completed.stdout + completed.stderr
    require("paid plan" in combined.lower(), "first-use setup no longer states the zero-cost boundary")
    text = env_file.read_text(encoding="utf-8")
    require(PASSWORD not in text, "plaintext owner password was written to local configuration")
    require("MEMORY_PALACE_ADMIN_PASSWORD_HASH=scrypt$" in text, "owner password is not stored as a scrypt hash")
    for lock in ("MEMORY_PALACE_HOST=127.0.0.1", "MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED=false", "MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED=false", "MEMORY_PALACE_GITHUB_ALLOW_MERGE=false"):
        require(lock in text, f"first-use setup is missing safety lock: {lock}")
    return env_file


def reserve_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def set_local_port(env_file: Path, port: int) -> None:
    lines = env_file.read_text(encoding="utf-8").splitlines()
    replaced = False
    updated: list[str] = []
    for line in lines:
        if line.startswith("MEMORY_PALACE_PORT="):
            updated.append(f"MEMORY_PALACE_PORT={port}")
            replaced = True
        else:
            updated.append(line)
    if not replaced:
        updated.append(f"MEMORY_PALACE_PORT={port}")
    env_file.write_text("\n".join(updated).rstrip() + "\n", encoding="utf-8")


def wait_until_ready(base_url: str, process: subprocess.Popen[str], timeout: float = 20.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RehearsalError(f"local Content Studio exited before becoming ready with code {process.returncode}")
        try:
            response = httpx.get(f"{base_url}/api/health", timeout=0.5)
            if response.status_code == 200:
                return
        except httpx.HTTPError:
            pass
        time.sleep(0.15)
    raise RehearsalError("local Content Studio did not become ready in time")


def start_server(root: Path, env_file: Path, port: int) -> subprocess.Popen[str]:
    runner = root / "scripts" / "run_content_studio_local.py"
    process = subprocess.Popen([sys.executable, str(runner), "--env-file", str(env_file)], cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, text=True)
    wait_until_ready(f"http://127.0.0.1:{port}", process)
    return process


def stop_server(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=8)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


@contextmanager
def running_server(root: Path, env_file: Path, port: int) -> Iterator[tuple[subprocess.Popen[str], str]]:
    process = start_server(root, env_file, port)
    try:
        yield process, f"http://127.0.0.1:{port}"
    finally:
        stop_server(process)


def csrf(token: str) -> dict[str, str]:
    return {"X-CSRF-Token": token}


def login(base_url: str) -> tuple[httpx.Client, str]:
    client = httpx.Client(base_url=base_url, timeout=20.0)
    response = client.post("/api/admin/login", json={"username": USERNAME, "password": PASSWORD})
    require(response.status_code == 200, f"owner login failed: {response.status_code} {response.text}")
    token = str(response.json().get("csrf_token") or "")
    require(bool(token), "owner login did not return a CSRF token")
    return client, token


def assert_publication_locked(client: httpx.Client, token: str, draft_id: str) -> None:
    status = client.get("/api/admin/publication/status")
    require(status.status_code == 200, "publication status endpoint failed")
    body = status.json()
    require(body.get("publication_enabled") is False, "content publication became enabled")
    require(body.get("github_enabled") is False, "GitHub publication became enabled")
    require(body.get("github_merge_enabled") is False, "GitHub merge became enabled")
    blocked = client.post("/api/admin/publication/candidates", json={"draft_ids": [draft_id], "title": "RC1 rehearsal must remain blocked", "notes": "This request verifies the local publication lock.", "warnings_acknowledged": True}, headers=csrf(token))
    require(blocked.status_code == 503, f"publication candidate was not blocked: {blocked.status_code} {blocked.text}")


def create_rehearsal_draft(client: httpx.Client, token: str) -> dict:
    created = client.post("/api/admin/editors/drafts", json={"entity_id": SCENE_ID}, headers=csrf(token))
    require(created.status_code == 200, f"draft creation failed: {created.status_code} {created.text}")
    draft = created.json()
    payload = dict(draft["payload"])
    payload["title"] = TITLE_A
    saved = client.patch(f"/api/admin/editors/drafts/{draft['draft_id']}", json={"payload": payload, "expected_version": draft["version"], "note": "RC1 clean install and recovery rehearsal", "autosave": False}, headers=csrf(token))
    require(saved.status_code == 200, f"draft save failed: {saved.status_code} {saved.text}")
    return saved.json()


def get_draft(client: httpx.Client, draft_id: str) -> dict:
    response = client.get(f"/api/admin/drafts/{draft_id}")
    require(response.status_code == 200, f"draft could not be reloaded: {response.status_code} {response.text}")
    return response.json()


def mutate_draft(client: httpx.Client, token: str, draft: dict) -> dict:
    payload = dict(draft["payload"])
    payload["title"] = TITLE_B
    response = client.patch(f"/api/admin/editors/drafts/{draft['draft_id']}", json={"payload": payload, "expected_version": draft["version"], "note": "RC1 temporary post-backup mutation", "autosave": False}, headers=csrf(token))
    require(response.status_code == 200, f"post-backup mutation failed: {response.status_code} {response.text}")
    return response.json()


def assert_health_and_repair(client: httpx.Client, token: str) -> None:
    report = client.get("/api/admin/system-health")
    require(report.status_code == 200, f"system health failed: {report.status_code} {report.text}")
    body = report.json()
    require(body.get("zero_cost_local_mode") is True, "system health no longer identifies zero-cost local mode")
    checks = {item["id"]: item for item in body.get("checks", [])}
    require(checks.get("loopback_binding", {}).get("status") == "ok", "health check rejected loopback binding")
    require(checks.get("publication_locks", {}).get("status") == "ok", "health check rejected publication locks")
    repair = client.post("/api/admin/system-health/repair", json={"action": "checkpoint_databases"}, headers=csrf(token))
    require(repair.status_code == 200, f"safe health repair failed: {repair.status_code} {repair.text}")
    repaired = repair.json()
    require(repaired.get("ok") is True, "safe health repair did not report success")
    require(repaired.get("action") == "checkpoint_databases", "unexpected health repair action was performed")
    require(repaired.get("report", {}).get("zero_cost_local_mode") is True, "health repair changed zero-cost local mode")


def create_backup(root: Path) -> Path:
    state = root / "server_data"
    backups = root / "content-studio-backups"
    completed = run([sys.executable, str(root / "scripts" / "backup_content_studio_local.py"), "--state-dir", str(state), "--backup-dir", str(backups)], cwd=root)
    require("backup created" in completed.stdout.lower(), "backup helper did not report success")
    archives = sorted(backups.glob("content-studio-backup-*.zip"))
    require(bool(archives), "backup helper did not create an archive")
    archive = archives[-1]
    checksum = archive.with_suffix(archive.suffix + ".sha256")
    require(checksum.exists(), "backup helper did not create the SHA-256 sidecar")
    expected = checksum.read_text(encoding="utf-8").strip().split()[0]
    actual = hashlib.sha256(archive.read_bytes()).hexdigest()
    require(expected == actual, "backup archive checksum does not match")
    return archive


def restore_backup(root: Path, archive: Path) -> None:
    completed = run([sys.executable, str(root / "scripts" / "restore_content_studio_local.py"), str(archive), "--state-dir", str(root / "server_data"), "--backup-dir", str(root / "content-studio-backups"), "--yes"], cwd=root)
    require("restored successfully" in completed.stdout.lower(), "restore helper did not report success")


def run_embedded_acceptance_helpers(root: Path) -> None:
    for script in ("scripts/qa_zero_cost_windows_launcher.py", "scripts/qa_zero_cost_local_updater.py", "scripts/qa_content_studio_health_repair.py"):
        completed = run([sys.executable, str(root / script)], cwd=root)
        require("PASS" in completed.stdout, f"embedded acceptance helper did not pass: {script}")


def main() -> None:
    require(git("rev-parse", f"{EXPECTED_IMPLEMENTATION}^{{commit}}") == EXPECTED_IMPLEMENTATION, "frozen implementation commit is unavailable")
    require(git("rev-parse", f"{EXPECTED_IMPLEMENTATION}^{{tree}}") == EXPECTED_TREE, "frozen implementation tree changed")
    require(git("rev-parse", f"{EXPECTED_BASELINE_MAIN}^{{commit}}") == EXPECTED_BASELINE_MAIN, "production baseline is unavailable")
    with tempfile.TemporaryDirectory(prefix="content-studio-rc1-clean-rehearsal-") as temp_raw:
        clean = Path(temp_raw) / "content-studio"
        clean.mkdir()
        expanded = extract_frozen_implementation(clean)
        require(private_state_is_clean(clean), "frozen implementation did not begin with clean private state")
        student_before = tree_digest(clean)
        run_embedded_acceptance_helpers(clean)
        env_file = run_clean_first_use_setup(clean)
        port = reserve_port()
        set_local_port(env_file, port)
        with running_server(clean, env_file, port) as (_, base_url):
            client, token = login(base_url)
            try:
                draft = create_rehearsal_draft(client, token)
                draft_id = draft["draft_id"]
                assert_publication_locked(client, token, draft_id)
            finally:
                client.close()
        with running_server(clean, env_file, port) as (_, base_url):
            client, token = login(base_url)
            try:
                persisted = get_draft(client, draft_id)
                require(persisted["payload"]["title"] == TITLE_A, "draft did not persist across local restart")
                assert_health_and_repair(client, token)
                assert_publication_locked(client, token, draft_id)
            finally:
                client.close()
        archive = create_backup(clean)
        with running_server(clean, env_file, port) as (_, base_url):
            client, token = login(base_url)
            try:
                persisted = get_draft(client, draft_id)
                changed = mutate_draft(client, token, persisted)
                require(changed["payload"]["title"] == TITLE_B, "temporary mutation was not saved before restore")
            finally:
                client.close()
        restore_backup(clean, archive)
        with running_server(clean, env_file, port) as (_, base_url):
            client, token = login(base_url)
            try:
                recovered = get_draft(client, draft_id)
                require(recovered["payload"]["title"] == TITLE_A, "restored backup did not recover the saved draft")
                assert_health_and_repair(client, token)
                assert_publication_locked(client, token, draft_id)
            finally:
                client.close()
        student_after = tree_digest(clean)
        require(student_after == student_before, "clean rehearsal modified AP Biology content or student frontend")
        env_text = env_file.read_text(encoding="utf-8")
        require(PASSWORD not in env_text, "plaintext password appeared in local configuration after rehearsal")
        for lock in ("MEMORY_PALACE_HOST=127.0.0.1", "MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED=false", "MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED=false", "MEMORY_PALACE_GITHUB_ALLOW_MERGE=false"):
            require(lock in env_text, f"final local safety lock missing: {lock}")
        print("CONTENT STUDIO RC1 CLEAN INSTALL/RECOVERY REHEARSAL PASS")
        print(f"- exact frozen implementation: {expanded['commit']}")
        print(f"- exact frozen tree: {expanded['tree']}")
        print(f"- exact tracked-file manifest entries verified: {expanded['file_count']}")
        print("- clean first-use owner setup completed without storing the plaintext password")
        print("- owner authentication and CSRF-protected draft editing worked on localhost only")
        print("- harmless Unit 8 draft persisted across process restart")
        print("- Content Health and allowlisted database checkpoint repair passed")
        print("- publication, GitHub delivery, and merge stayed disabled and candidate creation was blocked")
        print("- local backup checksum, post-backup mutation, restore, and recovered draft state passed")
        print("- Windows launcher, updater safety, and health/repair acceptance helpers passed inside the clean copy")
        print("- AP Biology content and the student frontend were byte-identical before and after rehearsal")
        print("- no hosting account, paid service, cloud database, billing account, or payment method was used")


if __name__ == "__main__":
    try:
        main()
    except RehearsalError as exc:
        raise SystemExit(f"CONTENT STUDIO RC1 CLEAN INSTALL/RECOVERY REHEARSAL FAIL\n- {exc}") from exc
