from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import admin_auth, admin_catalog, admin_draft_routes, admin_drafts
from backend import main as main_module

PASSWORD = "correct-horse-battery-staple"
USERNAME = "teacher-admin"
SESSION_SECRET = "test-session-secret-that-is-longer-than-thirty-two-characters"


@pytest.fixture
def draft_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    password_hash = admin_auth.hash_password(PASSWORD, salt=b"0123456789abcdef")
    monkeypatch.setattr(main_module, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_draft_routes, "ADMIN_ENABLED", True)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_USERNAME", USERNAME)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_PASSWORD_HASH", password_hash)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_SESSION_SECRET", SESSION_SECRET)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_DB", str(tmp_path / "admin-security.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_DRAFT_DB", str(tmp_path / "content-studio-drafts.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_SESSION_TTL_SECONDS", "3600")
    with TestClient(main_module.app) as client:
        login = client.post(
            "/api/admin/login",
            json={"username": USERNAME, "password": PASSWORD},
        )
        assert login.status_code == 200
        yield client, login.json()["csrf_token"]


def csrf_headers(token: str) -> dict[str, str]:
    return {"X-CSRF-Token": token}


def create_unit_draft(client: TestClient, csrf: str):
    response = client.post(
        "/api/admin/drafts",
        json={"entity_id": "unit:unit-1"},
        headers=csrf_headers(csrf),
    )
    assert response.status_code == 200
    return response.json()


def test_draft_mutations_require_csrf(draft_client):
    client, _ = draft_client
    assert client.get("/api/admin/drafts/summary").status_code == 200
    missing_csrf = client.post(
        "/api/admin/drafts",
        json={"entity_id": "unit:unit-1"},
    )
    assert missing_csrf.status_code == 403


def test_create_save_compare_and_optimistic_concurrency(draft_client):
    client, csrf = draft_client
    draft = create_unit_draft(client, csrf)
    assert draft["status"] == "draft"
    assert draft["course_id"] == "ap-biology"
    assert draft["payload"]["course_id"] == "ap-biology"
    assert draft["version"] == 1
    assert draft["changed_from_base"] is False

    duplicate = create_unit_draft(client, csrf)
    assert duplicate["draft_id"] == draft["draft_id"]
    assert duplicate["existing"] is True

    payload = dict(draft["payload"])
    payload["title"] = "Unit 1 working title"
    saved = client.patch(
        f"/api/admin/drafts/{draft['draft_id']}",
        json={
            "payload": payload,
            "expected_version": draft["version"],
            "note": "Test title change",
            "autosave": True,
        },
        headers=csrf_headers(csrf),
    )
    assert saved.status_code == 200
    saved_body = saved.json()
    assert saved_body["version"] == 2
    assert saved_body["payload"]["title"] == "Unit 1 working title"
    assert saved_body["changed_from_base"] is True

    stale = client.patch(
        f"/api/admin/drafts/{draft['draft_id']}",
        json={"payload": payload, "expected_version": 1, "autosave": False},
        headers=csrf_headers(csrf),
    )
    assert stale.status_code == 409

    comparison = client.get(f"/api/admin/drafts/{draft['draft_id']}/compare")
    assert comparison.status_code == 200
    assert comparison.json()["changed"] is True
    assert any(item["path"] == "$.title" for item in comparison.json()["changes"])

    published = admin_catalog.get_entity("unit:unit-1")
    assert published["title"] != "Unit 1 working title"


def test_immutable_identity_is_protected(draft_client):
    client, csrf = draft_client
    draft = create_unit_draft(client, csrf)
    payload = dict(draft["payload"])
    payload["id"] = "unit:tampered"
    response = client.patch(
        f"/api/admin/drafts/{draft['draft_id']}",
        json={"payload": payload, "expected_version": draft["version"]},
        headers=csrf_headers(csrf),
    )
    assert response.status_code == 400


def test_revision_snapshot_restore_and_archive_are_non_destructive(draft_client):
    client, csrf = draft_client
    draft = create_unit_draft(client, csrf)
    payload = dict(draft["payload"])
    original_title = payload["title"]
    payload["title"] = "Revision B"

    saved = client.patch(
        f"/api/admin/drafts/{draft['draft_id']}",
        json={"payload": payload, "expected_version": 1, "note": "Revision B"},
        headers=csrf_headers(csrf),
    ).json()

    revisions = client.get(f"/api/admin/drafts/{draft['draft_id']}/revisions").json()["items"]
    assert len(revisions) == 2
    created_revision = next(item for item in revisions if item["action"] == "created")

    snapshot = client.post(
        f"/api/admin/drafts/{draft['draft_id']}/snapshots",
        json={"label": "Before restoration"},
        headers=csrf_headers(csrf),
    )
    assert snapshot.status_code == 200
    snapshot_id = snapshot.json()["snapshot_id"]

    restored = client.post(
        f"/api/admin/drafts/{draft['draft_id']}/revisions/{created_revision['revision_id']}/restore",
        json={"expected_version": saved["version"]},
        headers=csrf_headers(csrf),
    )
    assert restored.status_code == 200
    restored_body = restored.json()
    assert restored_body["payload"]["title"] == original_title
    assert restored_body["version"] == 3

    from_snapshot = client.post(
        f"/api/admin/drafts/{draft['draft_id']}/snapshots/{snapshot_id}/restore",
        json={"expected_version": restored_body["version"]},
        headers=csrf_headers(csrf),
    )
    assert from_snapshot.status_code == 200
    snapshot_restored = from_snapshot.json()
    assert snapshot_restored["payload"]["title"] == "Revision B"

    archived = client.post(
        f"/api/admin/drafts/{draft['draft_id']}/archive",
        json={"expected_version": snapshot_restored["version"]},
        headers=csrf_headers(csrf),
    )
    assert archived.status_code == 200
    archived_body = archived.json()
    assert archived_body["status"] == "archived"

    edit_archived = client.patch(
        f"/api/admin/drafts/{draft['draft_id']}",
        json={
            "payload": snapshot_restored["payload"],
            "expected_version": archived_body["version"],
        },
        headers=csrf_headers(csrf),
    )
    assert edit_archived.status_code == 400

    unarchived = client.post(
        f"/api/admin/drafts/{draft['draft_id']}/restore-archive",
        json={"expected_version": archived_body["version"]},
        headers=csrf_headers(csrf),
    )
    assert unarchived.status_code == 200
    assert unarchived.json()["status"] == "draft"

    history = client.get(f"/api/admin/drafts/{draft['draft_id']}/revisions").json()["items"]
    actions = {item["action"] for item in history}
    assert {"created", "saved", "snapshot_created", "restored_revision", "restored_snapshot", "archived", "restored_from_archive"}.issubset(actions)


def test_summary_and_lists_report_recoverable_state(draft_client):
    client, csrf = draft_client
    draft = create_unit_draft(client, csrf)
    summary = client.get("/api/admin/drafts/summary")
    assert summary.status_code == 200
    body = summary.json()
    assert body["active_drafts"] == 1
    assert body["archived_drafts"] == 0
    assert body["revision_count"] >= 1
    assert body["published_content_write_enabled"] is False

    listing = client.get("/api/admin/drafts?status=draft")
    assert listing.status_code == 200
    assert listing.json()["items"][0]["draft_id"] == draft["draft_id"]


def test_draft_registry_and_filters_are_course_scoped(draft_client):
    client, csrf = draft_client
    registry = client.get("/api/admin/courses")
    assert registry.status_code == 200
    course = next(item for item in registry.json()["courses"] if item["course_id"] == "ap-biology")
    assert course["catalog_ready"] is True

    draft = client.post(
        "/api/admin/drafts",
        json={"entity_id": "unit:unit-1", "course_id": "ap-biology"},
        headers=csrf_headers(csrf),
    )
    assert draft.status_code == 200
    assert draft.json()["course_id"] == "ap-biology"

    scoped = client.get("/api/admin/drafts?course_id=ap-biology&status=draft")
    assert scoped.status_code == 200
    assert len(scoped.json()["items"]) == 1
    assert scoped.json()["items"][0]["course_id"] == "ap-biology"

    summary = client.get("/api/admin/drafts/summary?course_id=ap-biology")
    assert summary.status_code == 200
    assert summary.json()["course_id"] == "ap-biology"
    assert summary.json()["active_drafts"] == 1


def test_identical_entity_ids_remain_isolated_across_courses(draft_client, monkeypatch: pytest.MonkeyPatch):
    client, csrf = draft_client

    monkeypatch.setattr(admin_catalog, "require_editable_course", lambda course_id: {"course_id": course_id})

    def fake_entity(entity_id: str, course_id: str = "ap-biology"):
        if entity_id != "unit:unit-1":
            return None
        return {
            "id": entity_id,
            "type": "unit",
            "course_id": course_id,
            "unit_id": "unit-1",
            "title": "Biology Unit 1" if course_id == "ap-biology" else "Chemistry Unit 1",
        }

    monkeypatch.setattr(admin_catalog, "get_entity", fake_entity)

    biology = client.post(
        "/api/admin/drafts",
        json={"entity_id": "unit:unit-1", "course_id": "ap-biology"},
        headers=csrf_headers(csrf),
    )
    chemistry = client.post(
        "/api/admin/drafts",
        json={"entity_id": "unit:unit-1", "course_id": "ap-chemistry"},
        headers=csrf_headers(csrf),
    )
    assert biology.status_code == chemistry.status_code == 200
    biology_draft = biology.json()
    chemistry_draft = chemistry.json()
    assert biology_draft["draft_id"] != chemistry_draft["draft_id"]
    assert biology_draft["title"] == "Biology Unit 1"
    assert chemistry_draft["title"] == "Chemistry Unit 1"

    wrong_course = client.get(
        f"/api/admin/drafts/{chemistry_draft['draft_id']}?course_id=ap-biology"
    )
    assert wrong_course.status_code == 404

    biology_payload = dict(biology_draft["payload"])
    biology_payload["title"] = "Biology Unit 1 revised"
    wrong_update = client.patch(
        f"/api/admin/drafts/{biology_draft['draft_id']}",
        json={
            "course_id": "ap-chemistry",
            "payload": biology_payload,
            "expected_version": biology_draft["version"],
        },
        headers=csrf_headers(csrf),
    )
    assert wrong_update.status_code == 404

    saved = client.patch(
        f"/api/admin/drafts/{biology_draft['draft_id']}",
        json={
            "course_id": "ap-biology",
            "payload": biology_payload,
            "expected_version": biology_draft["version"],
        },
        headers=csrf_headers(csrf),
    )
    assert saved.status_code == 200
    assert saved.json()["payload"]["title"] == "Biology Unit 1 revised"

    chemistry_after = client.get(
        f"/api/admin/drafts/{chemistry_draft['draft_id']}?course_id=ap-chemistry"
    )
    assert chemistry_after.status_code == 200
    assert chemistry_after.json()["payload"]["title"] == "Chemistry Unit 1"

    archived = client.post(
        f"/api/admin/drafts/{biology_draft['draft_id']}/archive",
        json={"course_id": "ap-biology", "expected_version": saved.json()["version"]},
        headers=csrf_headers(csrf),
    )
    assert archived.status_code == 200
    assert archived.json()["status"] == "archived"
    assert client.get(
        f"/api/admin/drafts/{chemistry_draft['draft_id']}?course_id=ap-chemistry"
    ).json()["status"] == "draft"
