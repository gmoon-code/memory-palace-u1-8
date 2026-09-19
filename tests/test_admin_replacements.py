from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import admin_auth, admin_catalog, admin_draft_routes, admin_replacement_routes, admin_replacements
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


def test_chemistry_replacement_workspace_has_no_fixture_story_and_remains_write_locked(replacement_client):
    client, token = replacement_client
    retired_scene = "scene:unit-1:APCHEM-U1-J1:0"

    plan = client.get(
        "/api/admin/replacements/plan",
        params={"course_id": "ap-chemistry", "entity_id": retired_scene},
    )
    assert plan.status_code == 404

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

    blocked = client.post(
        "/api/admin/replacements/drafts",
        json={"course_id": "ap-chemistry", "entity_id": retired_scene},
        headers=csrf(token),
    )
    assert blocked.status_code == 400
    assert "editing is not enabled" in blocked.json()["detail"]

def test_replacement_analysis_and_apply_reject_wrong_course(replacement_client):
    client, token = replacement_client
    draft = client.post(
        "/api/admin/replacements/drafts",
        json={"course_id": "ap-biology", "entity_id": SCENE_ID},
        headers=csrf(token),
    ).json()
    replacement = dict(draft["payload"])
    replacement["story_paragraphs"] = list(replacement["story_paragraphs"]) + [
        "Course isolation validation paragraph."
    ]
    body = {
        "draft_id": draft["draft_id"],
        "course_id": "ap-chemistry",
        "expected_version": draft["version"],
        "mode": "narrative_only",
        "replacement": replacement,
        "preservation": {},
    }

    analyzed = client.post(
        "/api/admin/replacements/analyze",
        json=body,
        headers=csrf(token),
    )
    assert analyzed.status_code == 404

    applied = client.post(
        "/api/admin/replacements/apply",
        json=body,
        headers=csrf(token),
    )
    assert applied.status_code == 404

    unchanged = client.get(
        f"/api/admin/drafts/{draft['draft_id']}",
        params={"course_id": "ap-biology"},
    )
    assert unchanged.status_code == 200
    assert unchanged.json()["version"] == draft["version"]


def test_identical_replacement_entity_ids_remain_isolated_across_courses(
    replacement_client,
    monkeypatch: pytest.MonkeyPatch,
):
    client, token = replacement_client
    shared_id = "scene:unit-1:shared-route:0"

    def fake_entity(entity_id: str, course_id: str = "ap-biology"):
        if entity_id != shared_id:
            return None
        label = "Biology" if course_id == "ap-biology" else "Chemistry"
        return {
            "id": shared_id,
            "type": "scene",
            "course_id": course_id,
            "unit_id": "unit-1",
            "journey_id": "journey:unit-1:shared-route",
            "palace_id": "shared-route",
            "scene_index": 0,
            "locus_id": f"{course_id}-L01",
            "locus": f"{label} shared locus",
            "title": f"{label} shared scene",
            "story_paragraphs": [f"{label} original narrative."],
            "object_ids": [],
            "cast": [],
            "checkpoint": False,
            "source_path": None,
        }

    monkeypatch.setattr(
        admin_catalog,
        "require_editable_course",
        lambda course_id: {"course_id": course_id, "editable": True},
    )
    monkeypatch.setattr(admin_catalog, "get_entity", fake_entity)
    monkeypatch.setattr(admin_replacements, "required_knowledge", lambda entity_id, course_id="ap-biology": [])
    monkeypatch.setattr(
        admin_replacements,
        "dependency_impact",
        lambda entity_id, course_id="ap-biology": {
            "related_counts_by_type": {},
            "direct_outbound": [],
            "direct_inbound": [],
            "downstream": [],
            "truncated": False,
        },
    )

    biology = client.post(
        "/api/admin/replacements/drafts",
        json={"course_id": "ap-biology", "entity_id": shared_id},
        headers=csrf(token),
    )
    chemistry = client.post(
        "/api/admin/replacements/drafts",
        json={"course_id": "ap-chemistry", "entity_id": shared_id},
        headers=csrf(token),
    )
    assert biology.status_code == chemistry.status_code == 200
    biology_draft = biology.json()
    chemistry_draft = chemistry.json()
    assert biology_draft["draft_id"] != chemistry_draft["draft_id"]
    assert biology_draft["course_id"] == "ap-biology"
    assert chemistry_draft["course_id"] == "ap-chemistry"

    wrong_course = client.post(
        "/api/admin/replacements/analyze",
        json={
            "draft_id": chemistry_draft["draft_id"],
            "course_id": "ap-biology",
            "expected_version": chemistry_draft["version"],
            "mode": "narrative_only",
            "replacement": chemistry_draft["payload"],
            "preservation": {},
        },
        headers=csrf(token),
    )
    assert wrong_course.status_code == 404

    biology_replacement = dict(biology_draft["payload"])
    biology_replacement["story_paragraphs"] = ["Biology replacement narrative."]
    biology_apply = client.post(
        "/api/admin/replacements/apply",
        json={
            "draft_id": biology_draft["draft_id"],
            "course_id": "ap-biology",
            "expected_version": biology_draft["version"],
            "mode": "narrative_only",
            "replacement": biology_replacement,
            "preservation": {},
        },
        headers=csrf(token),
    )
    assert biology_apply.status_code == 200

    chemistry_replacement = dict(chemistry_draft["payload"])
    chemistry_replacement["story_paragraphs"] = ["Chemistry replacement narrative."]
    chemistry_apply = client.post(
        "/api/admin/replacements/apply",
        json={
            "draft_id": chemistry_draft["draft_id"],
            "course_id": "ap-chemistry",
            "expected_version": chemistry_draft["version"],
            "mode": "narrative_only",
            "replacement": chemistry_replacement,
            "preservation": {},
        },
        headers=csrf(token),
    )
    assert chemistry_apply.status_code == 200

    biology_after = client.get(
        f"/api/admin/drafts/{biology_draft['draft_id']}",
        params={"course_id": "ap-biology"},
    ).json()
    chemistry_after = client.get(
        f"/api/admin/drafts/{chemistry_draft['draft_id']}",
        params={"course_id": "ap-chemistry"},
    ).json()

    assert biology_after["payload"]["story_paragraphs"] == ["Biology replacement narrative."]
    assert chemistry_after["payload"]["story_paragraphs"] == ["Chemistry replacement narrative."]
    assert biology_after["payload"]["locus_id"] == "ap-biology-L01"
    assert chemistry_after["payload"]["locus_id"] == "ap-chemistry-L01"
