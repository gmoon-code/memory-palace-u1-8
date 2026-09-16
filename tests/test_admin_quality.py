from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import admin_auth, admin_draft_routes, admin_editor_routes, admin_quality, admin_quality_routes
from backend import main as main_module
from backend.settings import ROOT

PASSWORD = "correct-horse-battery-staple"
USERNAME = "teacher-admin"
SESSION_SECRET = "test-session-secret-that-is-longer-than-thirty-two-characters"
SCENE_ID = "scene:unit-8:U8-J1:0"
CHALLENGE_ID = "challenge:unit-8:U8-CL-001"
SCENE_SOURCE = ROOT / "content" / "ap-biology" / "unit-8" / "journeys" / "U8-J1.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture
def quality_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    password_hash = admin_auth.hash_password(PASSWORD, salt=b"0123456789abcdef")
    monkeypatch.setattr(main_module, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_draft_routes, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_editor_routes, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_quality_routes, "ADMIN_ENABLED", True)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_USERNAME", USERNAME)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_PASSWORD_HASH", password_hash)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_SESSION_SECRET", SESSION_SECRET)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_DB", str(tmp_path / "admin-security.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_DRAFT_DB", str(tmp_path / "content-studio-drafts.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_MEDIA_DB", str(tmp_path / "content-studio-media.sqlite3"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_MEDIA_DIR", str(tmp_path / "content-studio-media"))
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_SESSION_TTL_SECONDS", "3600")
    admin_quality.clear_quality_cache()
    with TestClient(main_module.app) as client:
        login = client.post(
            "/api/admin/login",
            json={"username": USERNAME, "password": PASSWORD},
        )
        assert login.status_code == 200
        yield client, login.json()["csrf_token"]
    admin_quality.clear_quality_cache()


def csrf(token: str) -> dict[str, str]:
    return {"X-CSRF-Token": token}


def test_published_scene_preview_uses_student_learning_model(quality_client):
    client, _ = quality_client
    response = client.get(
        "/api/admin/quality/preview",
        params={"entity_id": SCENE_ID, "source": "published"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["source_state"] == "published"
    assert body["model"]["renderer"] == "learn"
    assert body["model"]["journey"]["scenes"][0]["story_paragraphs"]
    assert body["model"]["journey"]["scenes"][0]["locus"]
    assert body["device_presets"]["phone"]["width"] == 390
    assert body["device_presets"]["desktop"]["width"] == 1280


def test_scene_working_copy_is_previewed_without_source_drift(quality_client):
    client, token = quality_client
    before = digest(SCENE_SOURCE)
    created = client.post(
        "/api/admin/editors/drafts",
        json={"entity_id": SCENE_ID},
        headers=csrf(token),
    )
    assert created.status_code == 200
    draft = created.json()
    payload = dict(draft["payload"])
    payload["title"] = "Draft-only preview title"
    payload["story_paragraphs"] = list(payload["story_paragraphs"]) + [
        "This sentence exists only inside the protected Step 8 working-copy preview."
    ]
    saved = client.patch(
        f"/api/admin/editors/drafts/{draft['draft_id']}",
        json={
            "payload": payload,
            "expected_version": draft["version"],
            "note": "Step 8 preview regression",
            "autosave": False,
        },
        headers=csrf(token),
    )
    assert saved.status_code == 200

    preview = client.get(
        "/api/admin/quality/preview",
        params={"entity_id": SCENE_ID, "source": "auto"},
    )
    assert preview.status_code == 200
    body = preview.json()
    assert body["source_state"] == "draft"
    scene = body["model"]["journey"]["scenes"][0]
    assert scene["title"] == "Draft-only preview title"
    assert scene["story_paragraphs"][-1].startswith("This sentence exists only")
    assert digest(SCENE_SOURCE) == before

    baseline = client.get(
        "/api/admin/quality/preview",
        params={"entity_id": SCENE_ID, "source": "published"},
    )
    assert baseline.status_code == 200
    assert baseline.json()["model"]["journey"]["scenes"][0]["title"] != "Draft-only preview title"
    assert digest(SCENE_SOURCE) == before


def test_entity_quality_flags_spatial_and_coverage_loss_in_draft(quality_client):
    client, token = quality_client
    draft = client.post(
        "/api/admin/editors/drafts",
        json={"entity_id": SCENE_ID},
        headers=csrf(token),
    ).json()
    payload = dict(draft["payload"])
    payload["location_description"] = ""
    payload["scene_layout"] = dict(payload.get("scene_layout") or {})
    payload["scene_layout"]["orientation"] = ""
    payload["object_ids"] = []
    saved = client.patch(
        f"/api/admin/editors/drafts/{draft['draft_id']}",
        json={"payload": payload, "expected_version": draft["version"], "autosave": False},
        headers=csrf(token),
    )
    assert saved.status_code == 200

    report = client.get(
        "/api/admin/quality/entity",
        params={"entity_id": SCENE_ID, "source": "draft"},
    )
    assert report.status_code == 200
    codes = {item["code"] for item in report.json()["findings"]}
    assert "scene-location-description-missing" in codes
    assert "scene-orientation-missing" in codes
    assert "scene-required-reference-reduced" in codes


def test_challenge_preview_uses_student_practice_model(quality_client):
    client, _ = quality_client
    response = client.get(
        "/api/admin/quality/preview",
        params={"entity_id": CHALLENGE_ID, "source": "published"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["entity_type"] == "challenge"
    assert body["model"]["renderer"] == "practice"
    assert len(body["model"]["application_lab"]["items"]) == 1
    assert "answer_guide" in body["model"]["application_lab"]["items"][0]


def test_quality_report_separates_blockers_warnings_and_advisories(quality_client):
    client, _ = quality_client
    response = client.get("/api/admin/quality/report", params={"unit_id": "unit-8"})
    assert response.status_code == 200
    body = response.json()
    assert body["schema"] == "story-method-content-studio-quality-1.0"
    assert body["scope"]["unit_id"] == "unit-8"
    assert body["publication_blocking_count"] == body["error_count"]
    assert set(body["policy"]) == {"errors", "warnings", "advisories"}
    assert all(item.get("unit_id") in {None, "unit-8"} for item in body["findings"])


def test_quality_endpoints_are_read_only_and_require_authentication(quality_client):
    client, _ = quality_client
    before = digest(SCENE_SOURCE)
    assert client.get("/api/admin/quality/devices").status_code == 200
    assert client.get("/api/admin/quality/entity", params={"entity_id": SCENE_ID}).status_code == 200
    assert digest(SCENE_SOURCE) == before

    client.cookies.clear()
    assert client.get("/api/admin/quality/preview", params={"entity_id": SCENE_ID}).status_code == 401
