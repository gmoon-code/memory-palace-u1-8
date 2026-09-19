from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import admin_auth, admin_catalog, admin_draft_routes, admin_replacement_routes
from backend import main as main_module


PASSWORD = "correct-horse-battery-staple"
USERNAME = "teacher-admin"
SESSION_SECRET = "test-session-secret-that-is-longer-than-thirty-two-characters"


@pytest.fixture
def admin_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    password_hash = admin_auth.hash_password(PASSWORD, salt=b"0123456789abcdef")
    monkeypatch.setattr(main_module, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_draft_routes, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_replacement_routes, "ADMIN_ENABLED", True)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_USERNAME", USERNAME)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_PASSWORD_HASH", password_hash)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_SESSION_SECRET", SESSION_SECRET)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_DB", str(tmp_path / "admin-security.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_DRAFT_DB", str(tmp_path / "content-studio-drafts.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_SESSION_TTL_SECONDS", "3600")
    admin_catalog.clear_catalog_cache()
    with TestClient(main_module.app) as client:
        login = client.post("/api/admin/login", json={"username": USERNAME, "password": PASSWORD})
        assert login.status_code == 200
        yield client, login.json()["csrf_token"]


def csrf(token: str) -> dict[str, str]:
    return {"X-CSRF-Token": token}


def test_teacher_course_registry_is_explicit_and_safe(admin_client):
    client, _ = admin_client
    response = client.get("/api/admin/courses")
    assert response.status_code == 200
    payload = response.json()
    assert payload["platform_title"] == "The Story Method"

    ap_biology = next(item for item in payload["courses"] if item["course_id"] == "ap-biology")
    assert ap_biology["catalog_ready"] is True
    assert ap_biology["editable"] is True

    ap_chemistry = next(item for item in payload["courses"] if item["course_id"] == "ap-chemistry")
    assert ap_chemistry["catalog_ready"] is True
    assert ap_chemistry["editable"] is False
    assert ap_chemistry["catalog_mode"] == "read_only"


def test_teacher_catalog_requests_are_course_scoped(admin_client):
    client, _ = admin_client
    biology = client.get("/api/admin/catalog/summary?course_id=ap-biology")
    assert biology.status_code == 200
    assert biology.json()["course_id"] == "ap-biology"
    biology_map = client.get("/api/admin/catalog/course-map?course_id=ap-biology")
    assert biology_map.status_code == 200
    assert len(biology_map.json()["units"]) == 8

    chemistry = client.get("/api/admin/catalog/summary?course_id=ap-chemistry")
    assert chemistry.status_code == 200
    assert chemistry.json()["course_id"] == "ap-chemistry"
    assert chemistry.json()["counts"]["unit"] == 2
    assert chemistry.json()["counts"]["journey"] == 2
    assert chemistry.json()["counts"]["scene"] == 4
    assert chemistry.json()["counts"]["concept"] == 8
    assert chemistry.json()["counts"]["memory_object"] == 8
    assert chemistry.json()["unresolved_reference_count"] == 0

    chemistry_map = client.get("/api/admin/catalog/course-map?course_id=ap-chemistry")
    assert chemistry_map.status_code == 200
    assert [unit["title"] for unit in chemistry_map.json()["units"]] == [
        "Atomic Structure and Properties",
        "Molecular and Ionic Compound Structure and Properties",
    ]

    biology_unit = client.get("/api/admin/catalog/entity?course_id=ap-biology&entity_id=unit:unit-1")
    chemistry_unit = client.get("/api/admin/catalog/entity?course_id=ap-chemistry&entity_id=unit:unit-1")
    assert biology_unit.status_code == chemistry_unit.status_code == 200
    assert biology_unit.json()["title"] == "Chemistry of Life"
    assert chemistry_unit.json()["title"] == "Atomic Structure and Properties"


def test_teacher_drafts_and_replacements_carry_course_identity(admin_client):
    client, token = admin_client
    draft = client.post(
        "/api/admin/drafts",
        json={"entity_id": "unit:unit-1", "course_id": "ap-biology"},
        headers=csrf(token),
    )
    assert draft.status_code == 200
    assert draft.json()["course_id"] == "ap-biology"
    assert draft.json()["payload"]["course_id"] == "ap-biology"
    listed = client.get("/api/admin/drafts?course_id=ap-biology&limit=50")
    assert listed.status_code == 200
    assert any(item["draft_id"] == draft.json()["draft_id"] for item in listed.json()["items"])
    plan = client.get(
        "/api/admin/replacements/plan",
        params={"entity_id": "scene:unit-8:U8-J1:0", "course_id": "ap-biology"},
    )
    assert plan.status_code == 200
    assert plan.json()["course_id"] == "ap-biology"


def test_teacher_frontend_exposes_course_selector_and_course_change_contract():
    root = Path(__file__).resolve().parents[1]
    html = (root / "frontend/admin/index.html").read_text(encoding="utf-8")
    js = (root / "frontend/admin/admin.js").read_text(encoding="utf-8")
    assert 'id="admin-course-select"' in html
    assert 'id="admin-course-note"' in html
    assert 'id="student-site-link"' in html
    assert 'selectedCourseId: "ap-biology"' in js
    assert 'apiRequest("/api/admin/courses")' in js
    assert 'courseApiUrl(' in js
    assert 'story-method-course-changed' in js
    assert 'studentLink.href = `/?course=${encodeURIComponent(state.selectedCourseId)}`' in js
