from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import (
    admin_auth,
    admin_catalog,
    admin_draft_routes,
    admin_editor_routes,
    admin_management_routes,
    admin_replacement_routes,
)
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
def management_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    password_hash = admin_auth.hash_password(PASSWORD, salt=b"0123456789abcdef")
    monkeypatch.setattr(main_module, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_draft_routes, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_editor_routes, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_replacement_routes, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_management_routes, "ADMIN_ENABLED", True)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_USERNAME", USERNAME)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_PASSWORD_HASH", password_hash)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_SESSION_SECRET", SESSION_SECRET)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_DB", str(tmp_path / "admin-security.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_DRAFT_DB", str(tmp_path / "content-studio-drafts.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_MEDIA_DB", str(tmp_path / "content-studio-media.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_MEDIA_DIR", str(tmp_path / "content-studio-media"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_SESSION_TTL_SECONDS", "3600")
    with TestClient(main_module.app) as client:
        login = client.post(
            "/api/admin/login",
            json={"username": USERNAME, "password": PASSWORD},
        )
        assert login.status_code == 200
        yield client, login.json()["csrf_token"], tmp_path


def csrf(token: str) -> dict[str, str]:
    return {"X-CSRF-Token": token}


def test_question_bank_and_review_timeline_are_protected(management_client):
    client, _, _ = management_client
    bank = client.get("/api/admin/management/question-bank?unit_id=unit-8&limit=1000")
    assert bank.status_code == 200
    body = bank.json()
    assert body["total"] > 0
    assert any(item.get("type") == "question" for item in body["items"])

    timeline = client.get("/api/admin/management/review-timeline?unit_id=unit-8")
    assert timeline.status_code == 200
    review = timeline.json()
    assert review["event_count"] > 0
    assert set(review["phase_counts"]) == {"immediate", "delayed", "discrimination", "application"}
    assert isinstance(review["coverage_gaps"], list)


def test_existing_assessment_edit_stays_in_draft_store(management_client):
    client, token, _ = management_client
    bank = client.get("/api/admin/management/question-bank?unit_id=unit-8&limit=1000").json()
    target = next(
        item
        for item in bank["items"]
        if item.get("type") == "question"
        and item.get("question_type") in {"review", "mixed_discrimination"}
        and item.get("source_path")
    )
    source = ROOT / target["source_path"]
    before = digest(source)

    created = client.post(
        "/api/admin/management/drafts",
        json={"entity_id": target["id"]},
        headers=csrf(token),
    )
    assert created.status_code == 200
    draft = created.json()
    assert draft["changed_from_base"] is False

    payload = draft["payload"]
    payload["prompt"] = str(payload.get("prompt") or "Question") + " Draft-only Step 7 edit."
    saved = client.patch(
        f"/api/admin/management/drafts/{draft['draft_id']}",
        json={
            "payload": payload,
            "expected_version": draft["version"],
            "note": "Step 7 assessment regression edit",
            "autosave": False,
        },
        headers=csrf(token),
    )
    assert saved.status_code == 200
    result = saved.json()
    assert result["version"] == 2
    assert result["changed_from_base"] is True
    assert result["management_validation"]["valid"] is True
    assert digest(source) == before


def test_new_question_proposal_never_enters_published_catalog(management_client):
    client, token, _ = management_client
    response = client.post(
        "/api/admin/management/proposals",
        json={
            "entity_type": "question",
            "unit_id": "unit-8",
            "title": "Draft-only ecosystem transfer question",
            "seed": {
                "prompt": "Explain how a change in energy transfer could affect biomass at a higher trophic level.",
                "answer": "A complete response would connect reduced transfer to less energy available for biomass production.",
                "knowledge_ids": [],
            },
        },
        headers=csrf(token),
    )
    assert response.status_code == 200
    draft = response.json()
    assert draft["entity_id"].startswith("new:question:unit-8:")
    assert draft["proposal"] is True
    assert admin_catalog.get_entity(draft["entity_id"]) is None

    bank = client.get("/api/admin/management/question-bank?unit_id=unit-8&limit=1000")
    assert bank.status_code == 200
    assert any(item["id"] == draft["entity_id"] and item.get("source_state") == "new_proposal" for item in bank.json()["items"])


def test_bulk_replace_previews_then_snapshots_without_source_drift(management_client):
    client, token, _ = management_client
    before = digest(SCENE_SOURCE)
    preview = client.post(
        "/api/admin/management/bulk/preview",
        json={
            "find": "The glass doors",
            "replacement": "The polished glass doors",
            "case_sensitive": True,
            "unit_id": "unit-8",
            "entity_types": ["scene"],
            "limit": 500,
        },
        headers=csrf(token),
    )
    assert preview.status_code == 200
    body = preview.json()
    candidate = next(item for item in body["candidates"] if item["entity_id"] == SCENE_ID)
    assert candidate["expected_version"] == 0
    assert candidate["occurrence_count"] >= 1

    applied = client.post(
        "/api/admin/management/bulk/apply",
        json={
            "find": body["find"],
            "replacement": body["replacement"],
            "case_sensitive": body["case_sensitive"],
            "targets": [
                {
                    "entity_id": candidate["entity_id"],
                    "expected_version": candidate["expected_version"],
                }
            ],
        },
        headers=csrf(token),
    )
    assert applied.status_code == 200
    result = applied.json()
    assert result["updated_count"] == 1
    assert result["occurrence_count"] >= 1
    draft_id = result["results"][0]["draft_id"]
    snapshots = client.get(f"/api/admin/drafts/{draft_id}/snapshots")
    assert snapshots.status_code == 200
    assert snapshots.json()["items"]
    assert snapshots.json()["items"][0]["label"].startswith("Before bulk replace")
    assert digest(SCENE_SOURCE) == before


def test_export_import_preview_respects_active_draft_conflicts(management_client):
    client, token, _ = management_client
    proposal = client.post(
        "/api/admin/management/proposals",
        json={
            "entity_type": "question",
            "unit_id": "unit-8",
            "title": "Portable draft question",
        },
        headers=csrf(token),
    ).json()

    exported = client.get(
        "/api/admin/management/export?unit_id=unit-8&entity_types=question&include_drafts=true&include_catalog=true"
    )
    assert exported.status_code == 200
    bundle = exported.json()
    assert bundle["schema"] == "story-method-content-studio-portable-1.0"
    proposal_record = next(record for record in bundle["records"] if record["entity_id"] == proposal["entity_id"])
    small_bundle = {**bundle, "records": [proposal_record], "record_count": 1}

    preview = client.post(
        "/api/admin/management/import/preview",
        json={"bundle": small_bundle},
        headers=csrf(token),
    )
    assert preview.status_code == 200
    imported_preview = preview.json()
    assert imported_preview["error_count"] == 0
    assert imported_preview["conflict_count"] == 1

    applied = client.post(
        "/api/admin/management/import/apply",
        json={"bundle": small_bundle, "conflict_policy": "skip"},
        headers=csrf(token),
    )
    assert applied.status_code == 200
    assert applied.json()["imported_count"] == 0
    assert applied.json()["skipped_count"] == 1


def test_media_staging_is_private_versioned_and_csrf_protected(management_client):
    client, token, tmp_path = management_client
    png = b"\x89PNG\r\n\x1a\n" + b"step7-private-media"
    endpoint = "/api/admin/management/media/upload?filename=diagram.png&unit_id=unit-8&alt_text=Draft%20diagram"

    denied = client.post(endpoint, content=png, headers={"Content-Type": "image/png"})
    assert denied.status_code == 403

    uploaded = client.post(
        endpoint,
        content=png,
        headers={**csrf(token), "Content-Type": "image/png"},
    )
    assert uploaded.status_code == 200
    asset = uploaded.json()
    assert asset["status"] == "staged"
    assert asset["sha256"] == hashlib.sha256(png).hexdigest()
    staged_files = list((tmp_path / "content-studio-media").iterdir())
    assert len(staged_files) == 1
    assert not str(staged_files[0]).startswith(str(ROOT / "frontend"))

    preview = client.get(f"/api/admin/management/media/{asset['asset_id']}/file")
    assert preview.status_code == 200
    assert preview.content == png

    updated = client.patch(
        f"/api/admin/management/media/{asset['asset_id']}",
        json={
            "expected_version": asset["version"],
            "alt_text": "A draft-only diagram with descriptive alternative text",
            "caption": "Teacher staging caption",
            "transcript": "",
            "unit_id": "unit-8",
            "entity_id": None,
        },
        headers=csrf(token),
    )
    assert updated.status_code == 200
    assert updated.json()["version"] == 2

    archived = client.post(
        f"/api/admin/management/media/{asset['asset_id']}/archive",
        json={"expected_version": 2},
        headers=csrf(token),
    )
    assert archived.status_code == 200
    assert archived.json()["status"] == "archived"
    assert staged_files[0].exists()


def test_management_mutations_require_csrf(management_client):
    client, _, _ = management_client
    proposal = client.post(
        "/api/admin/management/proposals",
        json={"entity_type": "question", "unit_id": "unit-8", "title": "Blocked without CSRF"},
    )
    assert proposal.status_code == 403

    preview = client.post(
        "/api/admin/management/bulk/preview",
        json={"find": "osmosis", "replacement": "osmosis"},
    )
    assert preview.status_code == 403
