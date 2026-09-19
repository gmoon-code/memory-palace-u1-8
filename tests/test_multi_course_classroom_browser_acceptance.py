from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import (
    admin_auth,
    admin_catalog,
    admin_draft_routes,
    admin_editor_routes,
    admin_management_routes,
    admin_publication_routes,
    admin_quality,
    admin_quality_routes,
    admin_replacement_routes,
)
from backend import main as main_module


PASSWORD = "correct-horse-battery-staple"
USERNAME = "teacher-admin"
SESSION_SECRET = "test-session-secret-that-is-longer-than-thirty-two-characters"


def csrf(token: str) -> dict[str, str]:
    return {"X-CSRF-Token": token}


@pytest.fixture
def classroom_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    password_hash = admin_auth.hash_password(PASSWORD, salt=b"0123456789abcdef")
    for module in (
        main_module,
        admin_draft_routes,
        admin_editor_routes,
        admin_management_routes,
        admin_publication_routes,
        admin_quality_routes,
        admin_replacement_routes,
    ):
        monkeypatch.setattr(module, "ADMIN_ENABLED", True)

    monkeypatch.setenv("MEMORY_PALACE_ADMIN_USERNAME", USERNAME)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_PASSWORD_HASH", password_hash)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_SESSION_SECRET", SESSION_SECRET)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_DB", str(tmp_path / "admin-security.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_DRAFT_DB", str(tmp_path / "content-studio-drafts.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_MEDIA_DB", str(tmp_path / "content-studio-media.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_MEDIA_DIR", str(tmp_path / "content-studio-media"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED", "true")
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_PUBLICATION_DB", str(tmp_path / "content-studio-publication.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_PUBLICATION_DIR", str(tmp_path / "content-studio-publications"))
    monkeypatch.setenv("MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED", "false")
    monkeypatch.setenv("MEMORY_PALACE_GITHUB_ALLOW_MERGE", "false")
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_SESSION_TTL_SECONDS", "3600")
    admin_catalog.clear_catalog_cache()
    admin_quality.clear_quality_cache()

    with TestClient(main_module.app) as client:
        login = client.post("/api/admin/login", json={"username": USERNAME, "password": PASSWORD})
        assert login.status_code == 200
        yield client, login.json()["csrf_token"]

    admin_catalog.clear_catalog_cache()
    admin_quality.clear_quality_cache()


def _first_entity(client: TestClient, course_id: str, entity_type: str, unit_id: str) -> dict:
    response = client.get(
        "/api/admin/catalog/entities",
        params={
            "course_id": course_id,
            "entity_type": entity_type,
            "unit_id": unit_id,
            "limit": 1,
        },
    )
    assert response.status_code == 200
    items = response.json()["items"]
    assert items
    return items[0]


def test_teacher_can_switch_courses_and_inspect_course_local_records(classroom_client):
    client, _ = classroom_client

    page = client.get("/admin")
    assert page.status_code == 200
    assert 'id="admin-course-select"' in page.text

    courses = client.get("/api/admin/courses")
    assert courses.status_code == 200
    records = {item["course_id"]: item for item in courses.json()["courses"]}

    biology = records["ap-biology"]
    chemistry = records["ap-chemistry"]
    assert biology["catalog_ready"] is True
    assert biology["editable"] is True
    assert chemistry["catalog_ready"] is True
    assert chemistry["editable"] is False

    biology_map = client.get(
        "/api/admin/catalog/course-map",
        params={"course_id": "ap-biology"},
    )
    chemistry_map = client.get(
        "/api/admin/catalog/course-map",
        params={"course_id": "ap-chemistry"},
    )
    assert biology_map.status_code == chemistry_map.status_code == 200
    assert len(biology_map.json()["units"]) == 8
    assert len(chemistry_map.json()["units"]) == 9

    biology_unit = client.get(
        "/api/admin/catalog/entity",
        params={"course_id": "ap-biology", "entity_id": "unit:unit-1"},
    )
    chemistry_unit = client.get(
        "/api/admin/catalog/entity",
        params={"course_id": "ap-chemistry", "entity_id": "unit:unit-1"},
    )
    assert biology_unit.status_code == chemistry_unit.status_code == 200
    assert biology_unit.json()["course_id"] == "ap-biology"
    assert chemistry_unit.json()["course_id"] == "ap-chemistry"
    assert biology_unit.json()["title"] == "Chemistry of Life"
    assert chemistry_unit.json()["title"] == "Atomic Structure and Properties"


def test_biology_authoring_path_remains_available_and_non_destructive(classroom_client):
    client, token = classroom_client
    scene = _first_entity(client, "ap-biology", "scene", "unit-1")

    editor = client.get(
        "/api/admin/editors/entity",
        params={"course_id": "ap-biology", "entity_id": scene["id"]},
    )
    assert editor.status_code == 200
    assert editor.json()["entity"]["course_id"] == "ap-biology"

    preview = client.get(
        "/api/admin/quality/preview",
        params={
            "course_id": "ap-biology",
            "entity_id": scene["id"],
            "source": "published",
        },
    )
    assert preview.status_code == 200
    assert preview.json()["course_id"] == "ap-biology"
    assert preview.json()["source_state"] == "published"

    draft = client.post(
        "/api/admin/editors/drafts",
        json={"course_id": "ap-biology", "entity_id": scene["id"]},
        headers=csrf(token),
    )
    assert draft.status_code == 200
    body = draft.json()
    assert body["course_id"] == "ap-biology"
    assert body["entity_id"] == scene["id"]


def test_chemistry_classroom_preview_is_complete_but_all_authoring_stays_locked(classroom_client):
    client, token = classroom_client
    entity_id = "unit:unit-1"

    editor = client.get(
        "/api/admin/editors/entity",
        params={"course_id": "ap-chemistry", "entity_id": entity_id},
    )
    assert editor.status_code == 200
    assert editor.json()["entity"]["course_id"] == "ap-chemistry"

    preview = client.get(
        "/api/admin/quality/preview",
        params={"course_id": "ap-chemistry", "entity_id": entity_id, "source": "published"},
    )
    assert preview.status_code == 200
    preview_body = preview.json()
    assert preview_body["course_id"] == "ap-chemistry"
    assert preview_body["unit_id"] == "unit-1"
    assert preview_body["source_state"] == "published"
    assert preview_body["model"]["renderer"] == "unit"

    journeys = client.get(
        "/api/admin/catalog/entities",
        params={"course_id": "ap-chemistry", "entity_type": "journey", "unit_id": "unit-1", "limit": 50},
    )
    scenes = client.get(
        "/api/admin/catalog/entities",
        params={"course_id": "ap-chemistry", "entity_type": "scene", "unit_id": "unit-1", "limit": 50},
    )
    assert journeys.status_code == scenes.status_code == 200
    assert journeys.json()["items"] == []
    assert scenes.json()["items"] == []

    questions = client.get(
        "/api/admin/management/question-bank",
        params={"course_id": "ap-chemistry", "unit_id": "unit-1", "limit": 1000},
    )
    review = client.get(
        "/api/admin/management/review-timeline",
        params={"course_id": "ap-chemistry", "unit_id": "unit-1"},
    )
    challenge = client.get(
        "/api/admin/management/challenge-bank",
        params={"course_id": "ap-chemistry", "unit_id": "unit-1", "limit": 1000},
    )
    health = client.get(
        "/api/admin/quality/report",
        params={"course_id": "ap-chemistry", "unit_id": "unit-1"},
    )
    publication = client.get(
        "/api/admin/publication/status",
        params={"course_id": "ap-chemistry"},
    )
    for response in (questions, review, challenge, health, publication):
        assert response.status_code == 200
        assert response.json()["course_id"] == "ap-chemistry"

    assert questions.json()["items"] == []
    assert challenge.json()["items"] == []
    assert publication.json()["course_editable"] is False

    blocked = [
        client.post(
            "/api/admin/editors/drafts",
            json={"course_id": "ap-chemistry", "entity_id": entity_id},
            headers=csrf(token),
        ),
        client.post(
            "/api/admin/replacements/drafts",
            json={"course_id": "ap-chemistry", "entity_id": "scene:unit-1:APCHEM-U1-J1:0"},
            headers=csrf(token),
        ),
        client.post(
            "/api/admin/management/proposals",
            json={"course_id": "ap-chemistry", "entity_type": "question", "unit_id": "unit-1", "title": "Acceptance lock check"},
            headers=csrf(token),
        ),
        client.post(
            "/api/admin/publication/candidates",
            json={
                "course_id": "ap-chemistry",
                "draft_ids": ["unreachable-read-only-draft"],
                "title": "Acceptance lock check",
                "notes": "",
                "warnings_acknowledged": True,
            },
            headers=csrf(token),
        ),
    ]
    for response in blocked:
        assert response.status_code == 400
        assert "editing is not enabled" in response.json()["detail"]

def test_switching_course_context_cannot_reuse_a_biology_draft_in_chemistry(classroom_client):
    client, token = classroom_client
    biology_scene = _first_entity(client, "ap-biology", "scene", "unit-1")

    draft = client.post(
        "/api/admin/editors/drafts",
        json={"course_id": "ap-biology", "entity_id": biology_scene["id"]},
        headers=csrf(token),
    )
    assert draft.status_code == 200
    draft_body = draft.json()

    wrong_course = client.get(
        f"/api/admin/drafts/{draft_body['draft_id']}",
        params={"course_id": "ap-chemistry"},
    )
    assert wrong_course.status_code == 404

    chemistry_preview = client.get(
        "/api/admin/quality/preview",
        params={"course_id": "ap-chemistry", "entity_id": "unit:unit-1", "source": "auto"},
    )
    assert chemistry_preview.status_code == 200
    assert chemistry_preview.json()["course_id"] == "ap-chemistry"
    assert chemistry_preview.json()["source_state"] == "published"
    assert chemistry_preview.json()["model"]["renderer"] == "unit"
