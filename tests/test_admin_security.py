from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import admin_auth
from backend import main as main_module

PASSWORD = "correct-horse-battery-staple"
USERNAME = "teacher-admin"
SESSION_SECRET = "test-session-secret-that-is-longer-than-thirty-two-characters"


@pytest.fixture
def admin_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    password_hash = admin_auth.hash_password(PASSWORD, salt=b"0123456789abcdef")
    monkeypatch.setattr(main_module, "ADMIN_ENABLED", True)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_USERNAME", USERNAME)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_PASSWORD_HASH", password_hash)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_SESSION_SECRET", SESSION_SECRET)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_DB", str(tmp_path / "admin-security.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_LOGIN_FAILURE_LIMIT", "3")
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_LOGIN_WINDOW_SECONDS", "600")
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_SESSION_TTL_SECONDS", "3600")
    with TestClient(main_module.app) as client:
        yield client


def login(client: TestClient):
    return client.post(
        "/api/admin/login",
        json={"username": USERNAME, "password": PASSWORD},
    )


def test_password_hash_round_trip():
    encoded = admin_auth.hash_password(PASSWORD, salt=b"fedcba9876543210")
    assert encoded.startswith("scrypt$")
    assert admin_auth.verify_password(PASSWORD, encoded) is True
    assert admin_auth.verify_password("wrong-password", encoded) is False


def test_admin_routes_are_hidden_when_disabled():
    client = TestClient(main_module.app)
    response = client.get("/admin")
    assert response.status_code == 404
    response = client.get("/api/admin/session")
    assert response.status_code == 404


def test_admin_read_api_requires_authentication(admin_client: TestClient):
    response = admin_client.get("/api/admin/course")
    assert response.status_code == 401


def test_login_creates_server_side_session_and_protected_reads(admin_client: TestClient):
    response = login(admin_client)
    assert response.status_code == 200
    body = response.json()
    assert body["authenticated"] is True
    assert body["username"] == USERNAME
    assert body["role"] == "owner"
    assert body["csrf_token"]

    cookie = response.headers["set-cookie"]
    assert "HttpOnly" in cookie
    assert "SameSite=strict" in cookie

    session = admin_client.get("/api/admin/session")
    assert session.status_code == 200
    assert session.json()["csrf_token"] == body["csrf_token"]

    course = admin_client.get("/api/admin/course")
    assert course.status_code == 200
    assert len(course.json()["units"]) == 8

    unit = admin_client.get("/api/admin/units/unit-8")
    assert unit.status_code == 200
    assert unit.json()["unit_id"] == "unit-8"


def test_logout_requires_csrf_and_revokes_session(admin_client: TestClient):
    response = login(admin_client)
    csrf = response.json()["csrf_token"]

    missing = admin_client.post("/api/admin/logout")
    assert missing.status_code == 403

    wrong = admin_client.post("/api/admin/logout", headers={"X-CSRF-Token": "wrong"})
    assert wrong.status_code == 403

    cross_site = admin_client.post(
        "/api/admin/logout",
        headers={"X-CSRF-Token": csrf, "Origin": "https://example.invalid"},
    )
    assert cross_site.status_code == 403

    logout = admin_client.post("/api/admin/logout", headers={"X-CSRF-Token": csrf})
    assert logout.status_code == 200
    assert logout.json()["authenticated"] is False

    expired = admin_client.get("/api/admin/session")
    assert expired.status_code == 401


def test_failed_logins_are_rate_limited_and_audited(admin_client: TestClient):
    for _ in range(3):
        response = admin_client.post(
            "/api/admin/login",
            json={"username": USERNAME, "password": "definitely-wrong"},
        )
        assert response.status_code == 401

    blocked = admin_client.post(
        "/api/admin/login",
        json={"username": USERNAME, "password": "definitely-wrong"},
    )
    assert blocked.status_code == 429

    # A different client/username key does not inherit the blocked identity's failure count.
    other = admin_client.post(
        "/api/admin/login",
        json={"username": "another-user", "password": "definitely-wrong"},
    )
    assert other.status_code == 401


def test_security_and_audit_endpoints_are_owner_only(admin_client: TestClient):
    response = login(admin_client)
    assert response.status_code == 200

    security = admin_client.get("/api/admin/security")
    assert security.status_code == 200
    protections = security.json()["protections"]
    assert protections["csrf_protection"] is True
    assert protections["session_store"] == "server-side sqlite"
    assert protections["content_write_api"] is False

    audit = admin_client.get("/api/admin/audit?limit=20")
    assert audit.status_code == 200
    events = audit.json()["events"]
    assert any(event["event"] == "login" and event["outcome"] == "success" for event in events)
    assert all("client_key" not in event for event in events)


def test_step2_exposes_no_content_write_endpoint():
    admin_routes = {
        route.path: set(route.methods or [])
        for route in main_module.app.routes
        if getattr(route, "path", "").startswith("/api/admin")
    }
    assert admin_routes["/api/admin/login"] == {"POST"}
    assert admin_routes["/api/admin/logout"] == {"POST"}
    assert admin_routes["/api/admin/session"] == {"GET"}
    assert admin_routes["/api/admin/course"] == {"GET"}
    assert admin_routes["/api/admin/units/{unit_id}"] == {"GET"}
    assert admin_routes["/api/admin/security"] == {"GET"}
    assert admin_routes["/api/admin/audit"] == {"GET"}
