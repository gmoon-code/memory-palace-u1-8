from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import admin_auth, admin_draft_routes, admin_editor_routes
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
