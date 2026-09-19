from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import admin_auth, admin_catalog, admin_draft_routes, admin_replacement_routes, course_packages
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
    assert chemistry.json()["counts"]["unit"] == 9
    assert chemistry.json()["counts"].get("journey", 0) == 0
    assert chemistry.json()["counts"].get("scene", 0) == 0
    assert chemistry.json()["counts"].get("concept", 0) == 0
    assert chemistry.json()["counts"].get("memory_object", 0) == 0
    assert chemistry.json()["unresolved_reference_count"] == 0

    chemistry_map = client.get("/api/admin/catalog/course-map?course_id=ap-chemistry")
    assert chemistry_map.status_code == 200
    assert [unit["title"] for unit in chemistry_map.json()["units"]] == ['Atomic Structure and Properties','Compound Structure and Properties','Properties of Substances and Mixtures','Chemical Reactions','Kinetics','Thermochemistry','Equilibrium','Acids and Bases','Thermodynamics and Electrochemistry']

    biology_unit = client.get("/api/admin/catalog/entity?course_id=ap-biology&entity_id=unit:unit-1")
    chemistry_unit = client.get("/api/admin/catalog/entity?course_id=ap-chemistry&entity_id=unit:unit-1")
    assert biology_unit.status_code == chemistry_unit.status_code == 200
    assert biology_unit.json()["title"] == "Chemistry of Life"
    assert chemistry_unit.json()["title"] == "Atomic Structure and Properties"

def test_teacher_dependencies_and_source_paths_do_not_cross_courses(admin_client):
    client, _ = admin_client

    chemistry_entities = client.get(
        "/api/admin/catalog/entities?course_id=ap-chemistry&entity_type=unit&limit=50"
    )
    assert chemistry_entities.status_code == 200
    items = chemistry_entities.json()["items"]
    assert len(items) == 9
    assert all(item["course_id"] == "ap-chemistry" for item in items)

    declared = course_packages.declared_unit_source_paths("ap-chemistry", "unit-1")
    assert len(declared) == 6
    assert all(path.startswith("content/ap-chemistry/unit-1/") for path in declared)
    assert not any(path.startswith("content/ap-biology/") for path in declared)

    report = client.get(
        "/api/admin/catalog/dependencies",
        params={"course_id": "ap-chemistry", "entity_id": "unit:unit-1", "depth": 3, "limit": 500},
    )
    assert report.status_code == 200
    payload = report.json()
    assert payload["course_id"] == "ap-chemistry"
    related = [item["entity"] for item in payload["related"]]
    assert all(item["course_id"] == "ap-chemistry" for item in related)

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

    retired_plan = client.get(
        "/api/admin/replacements/plan",
        params={"entity_id": "scene:unit-1:APCHEM-U1-J1:0", "course_id": "ap-chemistry"},
    )
    assert retired_plan.status_code == 404

    blocked = client.post(
        "/api/admin/drafts",
        json={"entity_id": "unit:unit-1", "course_id": "ap-chemistry"},
        headers=csrf(token),
    )
    assert blocked.status_code == 400
    assert "editing is not enabled" in blocked.json()["detail"]

def test_teacher_frontend_exposes_course_selector_and_course_change_contract():
    root = Path(__file__).resolve().parents[1]
    html = (root / "frontend/admin/index.html").read_text(encoding="utf-8")
    js = (root / "frontend/admin/admin.js").read_text(encoding="utf-8")
    editor = (root / "frontend/admin/editor.js").read_text(encoding="utf-8")
    replacement = (root / "frontend/admin/replacement.js").read_text(encoding="utf-8")
    management = (root / "frontend/admin/management.js").read_text(encoding="utf-8")
    quality = (root / "frontend/admin/quality.js").read_text(encoding="utf-8")
    publication = (root / "frontend/admin/publication.js").read_text(encoding="utf-8")
    workflow = (root / "frontend/admin/workflow.js").read_text(encoding="utf-8")
    assert 'id="admin-course-select"' in html
    assert 'id="admin-course-note"' in html
    assert 'id="student-site-link"' in html
    assert 'selectedCourseId: "ap-biology"' in js
    assert 'apiRequest("/api/admin/courses")' in js
    assert 'courseApiUrl(' in js
    assert 'story-method-course-changed' in js
    assert 'data-editable=' in js
    assert 'catalog preview' in js
    assert 'const availableCatalogs = state.courses.filter((item) => item.catalog_ready === true);' in js
    assert 'item.editable !== false' not in js
    assert 'studentLink.href = `/?course=${encodeURIComponent(state.selectedCourseId)}`' in js
    assert 'currentAdminCourseEditable()' in editor
    assert 'Read-only architecture preview' in editor
    assert 'currentAdminCourseEditable()' in replacement
    assert '<option value="unit-8">Unit 8</option>' not in replacement
    assert 'course_id: replacementState.draft.course_id || currentAdminCourseId()' in replacement
    assert 'course_id: replacementState.plan.course_id || currentAdminCourseId()' in replacement
    assert 'managementModes.has(mode) && currentAdminCourseCatalogReady()' in management
    assert 'currentAdminCourseId()' in management
    assert 'currentAdminCourseCatalogReady()' in management
    assert 'currentAdminCourseEditable()' in management
    assert 'course_id: preview.course_id || currentAdminCourseId()' in management
    assert 'course_id: item.course_id || currentAdminCourseId()' in management
    assert '<option value="unit-8">Unit 8</option>' not in management
    assert 'managementState.units' in management
    assert 'course_id: managementState.currentDraft.course_id || currentAdminCourseId()' in management
    assert 'story-method-course-changed' in management
    assert 'qualityModes.has(mode) && currentAdminCourseCatalogReady()' in quality
    assert '<option value="unit-8">Unit 8</option>' not in editor
    assert 'for (let index = 1; index <= 8; index += 1)' not in quality
    assert 'qualityState.units' in quality
    assert 'course_id: currentAdminCourseId()' in quality
    assert 'story-method-course-changed' in quality
    assert 'courseUrl("/api/admin/publication/status")' in publication
    assert 'course_id: currentAdminCourseId()' in publication
    assert 'currentAdminCourseEditable()' in publication
    assert 'story-method-course-changed' in publication
    assert 'course_id: parsed.course_id || "ap-biology"' in workflow
    assert 'new URLSearchParams({ course_id: context.course_id || currentWorkflowCourseId() })' in workflow
    assert 'workflowState.context?.course_id === next.course_id' in workflow
    assert 'story-method-course-changed' in workflow
    assert 'context.course_id || currentWorkflowCourseId()' in workflow
