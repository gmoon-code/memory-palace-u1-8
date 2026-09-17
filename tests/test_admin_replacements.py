from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import admin_auth, admin_draft_routes, admin_replacement_routes, admin_replacements
from backend import main as main_module
from backend.settings import ROOT

PASSWORD = "correct-horse-battery-staple"
USERNAME = "teacher-admin"
SESSION_SECRET = "test-session-secret-that-is-longer-than-thirty-two-characters"
SCENE_ID = "scene:unit-8:U8-J1:0"
JOURNEY_ID = "journey:unit-8:U8-J1"
SCENE_SOURCE = ROOT / "content" / "ap-biology" / "unit-8" / "journeys" / "U8-J1.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture
def replacement_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
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
    with TestClient(main_module.app) as client:
        login = client.post(
            "/api/admin/login",
            json={"username": USERNAME, "password": PASSWORD},
        )
        assert login.status_code == 200
        yield client, login.json()["csrf_token"]


def csrf(token: str) -> dict[str, str]:
    return {"X-CSRF-Token": token}


def test_replacement_plan_inventory_is_source_grounded(replacement_client):
    client, _ = replacement_client
    response = client.get(f"/api/admin/replacements/plan?entity_id={SCENE_ID}")
    assert response.status_code == 200
    plan = response.json()
    assert plan["entity_type"] == "scene"
    assert set(plan["modes"]) == {"narrative_only", "narrative_plus_scene_design", "complete_scene"}
    assert plan["required_knowledge_count"] >= 1
    assert plan["published_story_text"].startswith("The glass doors")
    assert plan["route_signature"] == [[0, "U8-L01"]]


def test_narrative_only_preserves_structure_and_required_refs(replacement_client):
    client, token = replacement_client
    draft = client.post(
        "/api/admin/replacements/drafts",
        json={"entity_id": SCENE_ID},
        headers=csrf(token),
    ).json()
    original = draft["payload"]
    response = client.post(
        "/api/admin/replacements/analyze",
        json={
            "draft_id": draft["draft_id"],
            "expected_version": draft["version"],
            "mode": "narrative_only",
            "replacement": {
                "story_paragraphs": list(original["story_paragraphs"]) + ["A replacement-only closing paragraph for validation."],
                "title": "Should remain preserved",
                "object_ids": [],
                "cast": [],
            },
            "preservation": {},
        },
        headers=csrf(token),
    )
    assert response.status_code == 200
    analysis = response.json()
    assert analysis["can_apply"] is True
    assert analysis["candidate"]["title"] == original["title"]
    assert analysis["candidate"]["object_ids"] == original["object_ids"]
    assert analysis["candidate"]["cast"] == original["cast"]
    assert analysis["route_preserved"] is True


def test_complete_scene_blocks_loss_of_required_knowledge(replacement_client):
    client, token = replacement_client
    draft = client.post(
        "/api/admin/replacements/drafts",
        json={"entity_id": SCENE_ID},
        headers=csrf(token),
    ).json()
    replacement = dict(draft["payload"])
    replacement["story_paragraphs"] = ["A replacement that intentionally drops the linked knowledge references."]
    replacement["object_ids"] = []
    replacement["checkpoint_object_id"] = ""
    response = client.post(
        "/api/admin/replacements/analyze",
        json={
            "draft_id": draft["draft_id"],
            "expected_version": draft["version"],
            "mode": "complete_scene",
            "replacement": replacement,
            "preservation": {"memory_objects": False, "quick_recall": False, "concept_associations": False},
        },
        headers=csrf(token),
    )
    assert response.status_code == 200
    analysis = response.json()
    assert analysis["can_apply"] is False
    assert analysis["missing_required_references"]
    assert any("Required knowledge references" in item for item in analysis["blockers"])


def test_apply_creates_snapshot_and_never_changes_published_story(replacement_client):
    client, token = replacement_client
    before = digest(SCENE_SOURCE)
    draft = client.post(
        "/api/admin/replacements/drafts",
        json={"entity_id": SCENE_ID},
        headers=csrf(token),
    ).json()
    replacement = dict(draft["payload"])
    replacement["story_paragraphs"] = list(replacement["story_paragraphs"]) + ["Draft-only replacement regression paragraph."]
    response = client.post(
        "/api/admin/replacements/apply",
        json={
            "draft_id": draft["draft_id"],
            "expected_version": draft["version"],
            "mode": "narrative_only",
            "replacement": replacement,
            "preservation": {},
        },
        headers=csrf(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["applied"] is True
    assert body["snapshot"]["label"].startswith("Before narrative only replacement")
    assert body["draft"]["version"] == 2
    assert body["draft"]["changed_from_base"] is True
    assert digest(SCENE_SOURCE) == before

    snapshots = client.get(f"/api/admin/drafts/{draft['draft_id']}/snapshots")
    assert snapshots.status_code == 200
    assert len(snapshots.json()["items"]) == 1


def test_complete_journey_preserves_scene_route(replacement_client):
    client, token = replacement_client
    plan = client.get(f"/api/admin/replacements/plan?entity_id={JOURNEY_ID}").json()
    assert plan["modes"] == ["complete_journey"]
    draft = client.post(
        "/api/admin/replacements/drafts",
        json={"entity_id": JOURNEY_ID},
        headers=csrf(token),
    ).json()
    replacement = dict(draft["payload"])
    replacement["scenes"] = [dict(scene) for scene in replacement["scenes"]]
    replacement["scenes"][0]["story_paragraphs"] = list(replacement["scenes"][0]["story_paragraphs"]) + ["Journey replacement draft-only paragraph."]
    response = client.post(
        "/api/admin/replacements/analyze",
        json={
            "draft_id": draft["draft_id"],
            "expected_version": draft["version"],
            "mode": "complete_journey",
            "replacement": replacement,
            "preservation": {},
        },
        headers=csrf(token),
    )
    assert response.status_code == 200
    analysis = response.json()
    assert analysis["route_preserved"] is True
    assert analysis["can_apply"] is True


def test_replacement_mutations_require_csrf(replacement_client):
    client, _ = replacement_client
    assert client.post("/api/admin/replacements/drafts", json={"entity_id": SCENE_ID}).status_code == 403
