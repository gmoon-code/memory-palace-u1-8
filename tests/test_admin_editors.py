from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import admin_auth, admin_catalog, admin_draft_routes, admin_editor_routes
from backend import main as main_module
from backend.settings import ROOT

PASSWORD = "correct-horse-battery-staple"
USERNAME = "teacher-admin"
SESSION_SECRET = "test-session-secret-that-is-longer-than-thirty-two-characters"
SCENE_ID = "scene:unit-8:U8-J1:0"
SCENE_SOURCE = ROOT / "content" / "ap-biology" / "unit-8" / "journeys" / "U8-J1.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture
def editor_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    password_hash = admin_auth.hash_password(PASSWORD, salt=b"0123456789abcdef")
    monkeypatch.setattr(main_module, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_draft_routes, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_editor_routes, "ADMIN_ENABLED", True)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_USERNAME", USERNAME)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_PASSWORD_HASH", password_hash)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_SESSION_SECRET", SESSION_SECRET)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_DB", str(tmp_path / "admin-security.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_DRAFT_DB", str(tmp_path / "content-studio-drafts.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_SESSION_TTL_SECONDS", "3600")
    admin_catalog.clear_catalog_cache()
    with TestClient(main_module.app) as client:
        login = client.post(
            "/api/admin/login",
            json={"username": USERNAME, "password": PASSWORD},
        )
        assert login.status_code == 200
        yield client, login.json()["csrf_token"]


def csrf(token: str) -> dict[str, str]:
    return {"X-CSRF-Token": token}


def test_editor_schema_and_types_are_protected(editor_client):
    client, _ = editor_client
    types = client.get("/api/admin/editors/types")
    assert types.status_code == 200
    assert set(types.json()["entity_types"]) == {
        "unit",
        "journey",
        "scene",
        "character",
        "location",
        "concept",
        "memory_object",
    }

    scene_schema = client.get("/api/admin/editors/schema?entity_type=scene")
    assert scene_schema.status_code == 200
    groups = {group["id"]: group for group in scene_schema.json()["groups"]}
    assert {"identity", "story", "cast", "retrieval"}.issubset(groups)
    story_paths = {field["path"] for field in groups["story"]["fields"]}
    assert "story_paragraphs" in story_paths


def test_scene_editor_reads_complete_source_story(editor_client):
    client, _ = editor_client
    response = client.get(f"/api/admin/editors/entity?entity_id={SCENE_ID}")
    assert response.status_code == 200
    entity = response.json()["entity"]
    assert entity["id"] == SCENE_ID
    assert len(entity["story_paragraphs"]) >= 5
    assert isinstance(entity["scene_layout"]["zones"], list)
    assert len(entity["cast"]) >= 1
    assert entity["story_paragraphs"][0].startswith("The glass doors")


def test_field_editor_draft_uses_source_enriched_immutable_base(editor_client):
    client, token = editor_client
    before_source = digest(SCENE_SOURCE)
    response = client.post(
        "/api/admin/editors/drafts",
        json={"entity_id": SCENE_ID},
        headers=csrf(token),
    )
    assert response.status_code == 200
    draft = response.json()
    assert draft["version"] == 1
    assert draft["changed_from_base"] is False
    assert len(draft["payload"]["story_paragraphs"]) >= 5
    assert draft["base_payload"]["story_paragraphs"] == draft["payload"]["story_paragraphs"]
    assert digest(SCENE_SOURCE) == before_source


def test_friendly_scene_save_creates_revision_without_touching_published_story(editor_client):
    client, token = editor_client
    before_source = digest(SCENE_SOURCE)
    draft = client.post(
        "/api/admin/editors/drafts",
        json={"entity_id": SCENE_ID},
        headers=csrf(token),
    ).json()

    payload = draft["payload"]
    payload["story_paragraphs"] = list(payload["story_paragraphs"])
    payload["story_paragraphs"][0] += " Draft-only editor test."
    payload["scene_layout"] = dict(payload["scene_layout"])
    payload["scene_layout"]["orientation"] += " Draft-only orientation test."

    saved = client.patch(
        f"/api/admin/editors/drafts/{draft['draft_id']}",
        json={
            "payload": payload,
            "expected_version": draft["version"],
            "note": "Friendly scene editor test",
            "autosave": True,
        },
        headers=csrf(token),
    )
    assert saved.status_code == 200
    body = saved.json()
    assert body["version"] == 2
    assert body["changed_from_base"] is True
    assert body["editor_validation"]["valid"] is True
    assert digest(SCENE_SOURCE) == before_source

    revisions = client.get(f"/api/admin/drafts/{draft['draft_id']}/revisions")
    assert revisions.status_code == 200
    assert len(revisions.json()["items"]) == 2


def test_field_editor_rejects_malformed_story_structure(editor_client):
    client, token = editor_client
    draft = client.post(
        "/api/admin/editors/drafts",
        json={"entity_id": SCENE_ID},
        headers=csrf(token),
    ).json()
    payload = draft["payload"]
    payload["story_paragraphs"] = "this must stay an ordered list"

    response = client.patch(
        f"/api/admin/editors/drafts/{draft['draft_id']}",
        json={"payload": payload, "expected_version": draft["version"], "autosave": False},
        headers=csrf(token),
    )
    assert response.status_code == 400
    assert "Story paragraphs" in response.json()["detail"]


def test_editor_mutations_require_csrf(editor_client):
    client, _ = editor_client
    no_csrf = client.post("/api/admin/editors/drafts", json={"entity_id": SCENE_ID})
    assert no_csrf.status_code == 403

    validate = client.post(
        "/api/admin/editors/validate",
        json={"entity_type": "scene", "payload": {"id": SCENE_ID, "type": "scene", "unit_id": "unit-8"}},
    )
    assert validate.status_code == 403



def test_generic_editor_reads_all_chemistry_record_types_without_enabling_writes(editor_client):
    client, token = editor_client

    biology_unit = client.get(
        "/api/admin/editors/entity",
        params={"course_id": "ap-biology", "entity_id": "unit:unit-1"},
    )
    chemistry_unit = client.get(
        "/api/admin/editors/entity",
        params={"course_id": "ap-chemistry", "entity_id": "unit:unit-1"},
    )
    assert biology_unit.status_code == chemistry_unit.status_code == 200
    assert biology_unit.json()["entity"]["title"] == "Chemistry of Life"
    assert chemistry_unit.json()["entity"]["title"] == "Atomic Structure and Properties"

    for entity_type in (
        "unit",
        "journey",
        "scene",
        "character",
        "location",
        "concept",
        "memory_object",
    ):
        listing = client.get(
            "/api/admin/catalog/entities",
            params={
                "course_id": "ap-chemistry",
                "entity_type": entity_type,
                "unit_id": "unit-1",
                "limit": 50,
            },
        )
        assert listing.status_code == 200
        items = listing.json()["items"]
        assert items, entity_type
        target = items[0]
        response = client.get(
            "/api/admin/editors/entity",
            params={"course_id": "ap-chemistry", "entity_id": target["id"]},
        )
        assert response.status_code == 200, entity_type
        entity = response.json()["entity"]
        assert entity["course_id"] == "ap-chemistry"
        assert entity["unit_id"] == "unit-1"
        if entity.get("source_path"):
            assert entity["source_path"].startswith("content/ap-chemistry/")

    chemistry_scene = client.get(
        "/api/admin/editors/entity",
        params={
            "course_id": "ap-chemistry",
            "entity_id": "scene:unit-1:APCHEM-U1-J1:0",
        },
    )
    assert chemistry_scene.status_code == 200
    scene = chemistry_scene.json()["entity"]
    assert scene["story_paragraphs"][0].startswith("The **Atomic Records Hall**")
    assert scene["scene_layout"]["zones"][0]["label"] == "Proton badge rail"

    blocked = client.post(
        "/api/admin/editors/drafts",
        json={
            "course_id": "ap-chemistry",
            "entity_id": "unit:unit-1",
        },
        headers=csrf(token),
    )
    assert blocked.status_code == 400
    assert "editing is not enabled" in blocked.json()["detail"]


def test_editor_writes_are_isolated_for_duplicate_entity_ids_when_second_course_is_simulated_editable(
    editor_client,
    monkeypatch: pytest.MonkeyPatch,
):
    client, token = editor_client
    monkeypatch.setattr(
        admin_catalog,
        "require_editable_course",
        lambda course_id: {"course_id": course_id, "editable": True},
    )

    biology = client.post(
        "/api/admin/editors/drafts",
        json={"course_id": "ap-biology", "entity_id": "unit:unit-1"},
        headers=csrf(token),
    )
    chemistry = client.post(
        "/api/admin/editors/drafts",
        json={"course_id": "ap-chemistry", "entity_id": "unit:unit-1"},
        headers=csrf(token),
    )
    assert biology.status_code == chemistry.status_code == 200
    biology_draft = biology.json()
    chemistry_draft = chemistry.json()
    assert biology_draft["draft_id"] != chemistry_draft["draft_id"]
    assert biology_draft["payload"]["title"] == "Chemistry of Life"
    assert chemistry_draft["payload"]["title"] == "Atomic Structure and Properties"

    biology_payload = dict(biology_draft["payload"])
    biology_payload["title"] = "Biology editor isolation check"
    biology_saved = client.patch(
        f"/api/admin/editors/drafts/{biology_draft['draft_id']}",
        json={
            "course_id": "ap-biology",
            "payload": biology_payload,
            "expected_version": biology_draft["version"],
            "note": "Course isolation check",
            "autosave": False,
        },
        headers=csrf(token),
    )
    assert biology_saved.status_code == 200

    wrong_course = client.patch(
        f"/api/admin/editors/drafts/{chemistry_draft['draft_id']}",
        json={
            "course_id": "ap-biology",
            "payload": chemistry_draft["payload"],
            "expected_version": chemistry_draft["version"],
            "autosave": False,
        },
        headers=csrf(token),
    )
    assert wrong_course.status_code == 404

    chemistry_payload = dict(chemistry_draft["payload"])
    chemistry_payload["title"] = "Chemistry editor isolation check"
    chemistry_saved = client.patch(
        f"/api/admin/editors/drafts/{chemistry_draft['draft_id']}",
        json={
            "course_id": "ap-chemistry",
            "payload": chemistry_payload,
            "expected_version": chemistry_draft["version"],
            "note": "Course isolation check",
            "autosave": False,
        },
        headers=csrf(token),
    )
    assert chemistry_saved.status_code == 200

    biology_after = client.get(
        f"/api/admin/drafts/{biology_draft['draft_id']}",
        params={"course_id": "ap-biology"},
    )
    chemistry_after = client.get(
        f"/api/admin/drafts/{chemistry_draft['draft_id']}",
        params={"course_id": "ap-chemistry"},
    )
    assert biology_after.status_code == chemistry_after.status_code == 200
    assert biology_after.json()["payload"]["title"] == "Biology editor isolation check"
    assert chemistry_after.json()["payload"]["title"] == "Chemistry editor isolation check"
