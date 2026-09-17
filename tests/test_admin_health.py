from __future__ import annotations

import os
from pathlib import Path
import sqlite3
import time

import pytest
from fastapi.testclient import TestClient

from backend import admin_auth, admin_health, admin_health_routes
from backend import main as main_module

PASSWORD = "correct-horse-battery-staple"
USERNAME = "teacher-admin"
SESSION_SECRET = "test-session-secret-that-is-longer-than-thirty-two-characters"


def prepare_root(tmp_path: Path) -> None:
    (tmp_path / "server_data").mkdir(parents=True, exist_ok=True)
    (tmp_path / "server_data" / "content-studio-media").mkdir(parents=True, exist_ok=True)
    (tmp_path / "server_data" / "content-studio-publications").mkdir(parents=True, exist_ok=True)
    (tmp_path / "content-studio-backups").mkdir(parents=True, exist_ok=True)
    (tmp_path / ".venv" / "Scripts").mkdir(parents=True, exist_ok=True)
    (tmp_path / "requirements.txt").write_text("fastapi==0.116.1\n", encoding="utf-8")
    digest = __import__("hashlib").sha256((tmp_path / "requirements.txt").read_bytes()).hexdigest()
    (tmp_path / ".venv" / ".content-studio-requirements.sha256").write_text(digest + "\n", encoding="utf-8")
    (tmp_path / ".gitignore").write_text(
        "server_data/\n.env.content-studio-local\ncontent-studio-backups/\n.venv/\n",
        encoding="utf-8",
    )


def configure_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    password_hash = admin_auth.hash_password(PASSWORD, salt=b"0123456789abcdef")
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_USERNAME", USERNAME)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_PASSWORD_HASH", password_hash)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_SESSION_SECRET", SESSION_SECRET)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_DB", str(tmp_path / "server_data" / "admin-security.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_DRAFT_DB", str(tmp_path / "server_data" / "content-studio-drafts.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_MEDIA_DB", str(tmp_path / "server_data" / "content-studio-media.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_MEDIA_DIR", str(tmp_path / "server_data" / "content-studio-media"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_PUBLICATION_DB", str(tmp_path / "server_data" / "content-studio-publication.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_PUBLICATION_DIR", str(tmp_path / "server_data" / "content-studio-publications"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED", "false")
    monkeypatch.setenv("MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED", "false")
    monkeypatch.setenv("MEMORY_PALACE_GITHUB_ALLOW_MERGE", "false")
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_SESSION_TTL_SECONDS", "3600")


def test_health_report_locks_zero_cost_local_mode(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    prepare_root(tmp_path)
    configure_env(monkeypatch, tmp_path)
    monkeypatch.setattr(admin_health, "ROOT", tmp_path)
    monkeypatch.setattr(admin_health, "HOST", "127.0.0.1")

    with sqlite3.connect(tmp_path / "server_data" / "admin-security.sqlite3") as connection:
        connection.execute("CREATE TABLE sample(id INTEGER PRIMARY KEY)")
    report = admin_health.health_report()
    checks = {item["id"]: item for item in report["checks"]}

    assert report["zero_cost_local_mode"] is True
    assert checks["loopback_binding"]["status"] == "ok"
    assert checks["publication_locks"]["status"] == "ok"
    assert checks["zero_cost_boundary"]["status"] == "ok"
    assert checks["private_state_directory"]["status"] == "ok"
    assert checks["private_paths_ignored"]["status"] == "ok"
    assert "repair_all" in report["safe_repair_actions"]


def test_health_report_flags_publication_and_non_loopback(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    prepare_root(tmp_path)
    configure_env(monkeypatch, tmp_path)
    monkeypatch.setattr(admin_health, "ROOT", tmp_path)
    monkeypatch.setattr(admin_health, "HOST", "0.0.0.0")
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED", "true")

    report = admin_health.health_report()
    checks = {item["id"]: item for item in report["checks"]}
    assert report["zero_cost_local_mode"] is False
    assert checks["loopback_binding"]["status"] == "error"
    assert checks["publication_locks"]["status"] == "error"
    assert report["overall"] == "blocked"


def test_safe_repairs_create_directories_and_remove_only_old_temp(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    configure_env(monkeypatch, tmp_path)
    monkeypatch.setattr(admin_health, "ROOT", tmp_path)
    missing_media = tmp_path / "server_data" / "content-studio-media"
    missing_publication = tmp_path / "server_data" / "content-studio-publications"
    assert not missing_media.exists()

    admin_health.run_repair("ensure_private_directories")
    assert missing_media.is_dir()
    assert missing_publication.is_dir()

    stale = tmp_path / "server_data" / "stale.tmp"
    fresh = tmp_path / "server_data" / "fresh.tmp"
    protected = tmp_path / "server_data" / "drafts.sqlite3"
    stale.write_text("old", encoding="utf-8")
    fresh.write_text("new", encoding="utf-8")
    protected.write_text("keep", encoding="utf-8")
    old = time.time() - admin_health.STALE_TEMP_SECONDS - 30
    os.utime(stale, (old, old))

    admin_health.run_repair("cleanup_temp_files")
    assert not stale.exists()
    assert fresh.exists()
    assert protected.exists()


def test_unknown_repair_action_is_rejected():
    with pytest.raises(admin_health.HealthRepairError):
        admin_health.run_repair("delete_everything")


@pytest.fixture
def health_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    prepare_root(tmp_path)
    configure_env(monkeypatch, tmp_path)
    monkeypatch.setattr(main_module, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_health_routes, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_health, "ROOT", tmp_path)
    monkeypatch.setattr(admin_health, "HOST", "127.0.0.1")
    with TestClient(main_module.app) as client:
        login = client.post(
            "/api/admin/login",
            json={"username": USERNAME, "password": PASSWORD},
        )
        assert login.status_code == 200
        yield client, login.json()["csrf_token"]


def test_health_api_requires_session_and_repair_requires_csrf(health_client):
    client, csrf = health_client
    report = client.get("/api/admin/system-health")
    assert report.status_code == 200
    assert "checks" in report.json()

    missing_csrf = client.post(
        "/api/admin/system-health/repair",
        json={"action": "ensure_private_directories"},
    )
    assert missing_csrf.status_code == 403

    repaired = client.post(
        "/api/admin/system-health/repair",
        json={"action": "ensure_private_directories"},
        headers={"X-CSRF-Token": csrf},
    )
    assert repaired.status_code == 200
    assert repaired.json()["ok"] is True
    assert repaired.json()["action"] == "ensure_private_directories"


def test_health_api_rejects_unsafe_action(health_client):
    client, csrf = health_client
    response = client.post(
        "/api/admin/system-health/repair",
        json={"action": "remove_curriculum"},
        headers={"X-CSRF-Token": csrf},
    )
    assert response.status_code == 400
