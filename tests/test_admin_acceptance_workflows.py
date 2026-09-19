from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import (
    admin_auth,
    admin_draft_routes,
    admin_editor_routes,
    admin_management_routes,
    admin_publication_routes,
    admin_quality,
    admin_quality_routes,
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


def csrf(token: str) -> dict[str, str]:
    return {"X-CSRF-Token": token}


@pytest.fixture
def acceptance_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
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
    admin_quality.clear_quality_cache()

    with TestClient(main_module.app) as client:
        login = client.post("/api/admin/login", json={"username": USERNAME, "password": PASSWORD})
        assert login.status_code == 200
        yield client, login.json()["csrf_token"]

    admin_quality.clear_quality_cache()


def test_teacher_can_preview_representative_scene_from_every_unit(acceptance_client):
    client, _ = acceptance_client
    for number in range(1, 9):
        unit_id = f"unit-{number}"
        records = client.get(
            "/api/admin/catalog/entities",
            params={"entity_type": "scene", "unit_id": unit_id, "limit": 1},
        )
        assert records.status_code == 200
        items = records.json()["items"]
        assert items, f"{unit_id} has no scene available to administrators"
        scene_id = items[0]["id"]
        preview = client.get(
            "/api/admin/quality/preview",
            params={"entity_id": scene_id, "source": "published"},
        )
        assert preview.status_code == 200, f"{unit_id} preview failed for {scene_id}"
        body = preview.json()
        assert body["entity_type"] == "scene"
        assert body["unit_id"] == unit_id
        assert body["source_state"] == "published"
        assert body["model"]["renderer"] in {"learn", "learn_recall"}


def test_scene_edit_preview_validate_candidate_and_recovery_path_is_non_destructive(acceptance_client):
    client, token = acceptance_client
    before = digest(SCENE_SOURCE)

    created = client.post(
        "/api/admin/editors/drafts",
        json={"entity_id": SCENE_ID},
        headers=csrf(token),
    )
    assert created.status_code == 200
    draft = created.json()

    payload = dict(draft["payload"])
    payload["title"] = "Acceptance-test working-copy scene title"
    saved = client.patch(
        f"/api/admin/editors/drafts/{draft['draft_id']}",
        json={
            "payload": payload,
            "expected_version": draft["version"],
            "note": "Administrator acceptance workflow",
            "autosave": False,
        },
        headers=csrf(token),
    )
    assert saved.status_code == 200
    saved_draft = saved.json()
    assert saved_draft["changed_from_base"] is True

    snapshot = client.post(
        f"/api/admin/drafts/{draft['draft_id']}/snapshots",
        json={"label": "Acceptance test recovery point"},
        headers=csrf(token),
    )
    assert snapshot.status_code == 200

    preview = client.get(
        "/api/admin/quality/preview",
        params={"entity_id": SCENE_ID, "source": "auto"},
    )
    assert preview.status_code == 200
    assert preview.json()["source_state"] == "draft"
    assert preview.json()["model"]["journey"]["scenes"][0]["title"] == "Acceptance-test working-copy scene title"

    quality = client.get(
        "/api/admin/quality/entity",
        params={"entity_id": SCENE_ID, "source": "draft"},
    )
    assert quality.status_code == 200
    assert "findings" in quality.json()

    eligible = client.get("/api/admin/publication/eligible", params={"course_id": "ap-biology"})
    assert eligible.status_code == 200
    matching = [item for item in eligible.json()["items"] if item["draft_id"] == draft["draft_id"]]
    assert matching
    assert matching[0]["publication_supported"] is True

    candidate = client.post(
        "/api/admin/publication/candidates",
        json={
            "course_id": "ap-biology",
            "draft_ids": [draft["draft_id"]],
            "title": "Administrator acceptance candidate",
            "notes": "Created only inside the isolated publication workspace.",
            "warnings_acknowledged": True,
        },
        headers=csrf(token),
    )
    assert candidate.status_code == 200, candidate.text
    assert candidate.json()["status"] == "created"
    assert digest(SCENE_SOURCE) == before

    snapshots = client.get(f"/api/admin/drafts/{draft['draft_id']}/snapshots")
    labels = [item["label"] for item in snapshots.json()["items"]]
    assert "Acceptance test recovery point" in labels
    assert any("Pre-publication snapshot" in label for label in labels)
    assert digest(SCENE_SOURCE) == before


def test_story_replacement_question_review_and_challenge_workflows_share_safe_drafts(acceptance_client):
    client, token = acceptance_client
    before = digest(SCENE_SOURCE)

    replacement_draft = client.post(
        "/api/admin/replacements/drafts",
        json={"entity_id": SCENE_ID},
        headers=csrf(token),
    )
    assert replacement_draft.status_code == 200
    replacement_draft = replacement_draft.json()
    replacement = dict(replacement_draft["payload"])
    replacement["story_paragraphs"] = list(replacement["story_paragraphs"]) + [
        "This paragraph exists only inside the administrator acceptance replacement workflow."
    ]
    analysis = client.post(
        "/api/admin/replacements/analyze",
        json={
            "draft_id": replacement_draft["draft_id"],
            "expected_version": replacement_draft["version"],
            "mode": "narrative_only",
            "replacement": replacement,
            "preservation": {},
        },
        headers=csrf(token),
    )
    assert analysis.status_code == 200
    assert analysis.json()["can_apply"] is True
    applied = client.post(
        "/api/admin/replacements/apply",
        json={
            "draft_id": replacement_draft["draft_id"],
            "expected_version": replacement_draft["version"],
            "mode": "narrative_only",
            "replacement": replacement,
            "preservation": {},
        },
        headers=csrf(token),
    )
    assert applied.status_code == 200
    assert applied.json()["applied"] is True
    assert digest(SCENE_SOURCE) == before

    bank = client.get("/api/admin/management/question-bank", params={"unit_id": "unit-8", "limit": 1000})
    assert bank.status_code == 200
    question = next(item for item in bank.json()["items"] if item.get("type") == "question" and item.get("source_path"))
    question_draft = client.post(
        "/api/admin/management/drafts",
        json={"entity_id": question["id"]},
        headers=csrf(token),
    )
    assert question_draft.status_code == 200
    question_draft = question_draft.json()
    qpayload = dict(question_draft["payload"])
    qpayload["prompt"] = str(qpayload.get("prompt") or "Question") + " Acceptance-test working-copy edit."
    question_saved = client.patch(
        f"/api/admin/management/drafts/{question_draft['draft_id']}",
        json={
            "payload": qpayload,
            "expected_version": question_draft["version"],
            "note": "Administrator acceptance question edit",
            "autosave": False,
        },
        headers=csrf(token),
    )
    assert question_saved.status_code == 200

    question_preview = client.get(
        "/api/admin/quality/preview",
        params={"entity_id": question["id"], "source": "auto"},
    )
    assert question_preview.status_code == 200
    assert question_preview.json()["source_state"] == "draft"

    review = client.get("/api/admin/management/review-timeline", params={"unit_id": "unit-8"})
    assert review.status_code == 200
    assert review.json()["event_count"] > 0

    challenges = client.get("/api/admin/management/challenge-bank", params={"unit_id": "unit-8", "limit": 1000})
    assert challenges.status_code == 200
    challenge = challenges.json()["items"][0]
    challenge_entity = client.get("/api/admin/management/entity", params={"entity_id": challenge["id"]})
    assert challenge_entity.status_code == 200
    challenge_preview = client.get(
        "/api/admin/quality/preview",
        params={"entity_id": challenge["id"], "source": "published"},
    )
    assert challenge_preview.status_code == 200
    assert challenge_preview.json()["model"]["renderer"] == "practice"
    assert digest(SCENE_SOURCE) == before
