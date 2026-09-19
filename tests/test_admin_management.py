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
    admin_management,
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
    admin_catalog.clear_catalog_cache()
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
    assert asset["course_id"] == "ap-biology"
    assert asset["sha256"] == hashlib.sha256(png).hexdigest()
    staged_files = list((tmp_path / "content-studio-media").iterdir())
    assert len(staged_files) == 1
    assert not str(staged_files[0]).startswith(str(ROOT / "frontend"))

    preview = client.get(f"/api/admin/management/media/{asset['asset_id']}/file")
    assert preview.status_code == 200
    assert preview.content == png

    wrong_course_preview = client.get(
        f"/api/admin/management/media/{asset['asset_id']}/file",
        params={"course_id": "ap-chemistry"},
    )
    assert wrong_course_preview.status_code == 404

    chemistry_staged = client.get(
        "/api/admin/management/media/staged",
        params={"course_id": "ap-chemistry", "status": "staged", "limit": 100},
    )
    assert chemistry_staged.status_code == 200
    assert chemistry_staged.json()["course_id"] == "ap-chemistry"
    assert chemistry_staged.json()["items"] == []

    chemistry_upload = client.post(
        "/api/admin/management/media/upload?filename=chemistry.png&course_id=ap-chemistry&unit_id=unit-1",
        content=png,
        headers={**csrf(token), "Content-Type": "image/png"},
    )
    assert chemistry_upload.status_code == 400
    assert "editing is not enabled" in chemistry_upload.json()["detail"]

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



def test_chemistry_question_review_and_challenge_reads_are_course_scoped(management_client):
    client, token, _ = management_client

    bank = client.get(
        "/api/admin/management/question-bank",
        params={"course_id": "ap-chemistry", "unit_id": "unit-1", "limit": 1000},
    )
    assert bank.status_code == 200
    bank_payload = bank.json()
    assert bank_payload["course_id"] == "ap-chemistry"
    assert bank_payload["items"]
    assert all(item.get("course_id") == "ap-chemistry" for item in bank_payload["items"])
    assert not any("U1-K-" in str(item) and "APCHEM-U1-K" not in str(item) for item in bank_payload["items"])

    review_question = next(
        item
        for item in bank_payload["items"]
        if item.get("type") == "question"
        and item.get("question_type") == "review"
        and item.get("source_path")
    )
    detail = client.get(
        "/api/admin/management/entity",
        params={"course_id": "ap-chemistry", "entity_id": review_question["id"]},
    )
    assert detail.status_code == 200
    entity = detail.json()["entity"]
    assert entity["course_id"] == "ap-chemistry"
    assert entity["source_path"].startswith("content/ap-chemistry/")
    assert entity["prompt"]

    timeline = client.get(
        "/api/admin/management/review-timeline",
        params={"course_id": "ap-chemistry", "unit_id": "unit-1"},
    )
    assert timeline.status_code == 200
    timeline_payload = timeline.json()
    assert timeline_payload["course_id"] == "ap-chemistry"
    assert timeline_payload["event_count"] > 0
    assert all(event["course_id"] == "ap-chemistry" for event in timeline_payload["events"])

    challenges = client.get(
        "/api/admin/management/challenge-bank",
        params={"course_id": "ap-chemistry", "unit_id": "unit-1", "limit": 1000},
    )
    assert challenges.status_code == 200
    challenge_payload = challenges.json()
    assert challenge_payload["course_id"] == "ap-chemistry"
    assert challenge_payload["items"]
    assert all(item.get("course_id") == "ap-chemistry" for item in challenge_payload["items"])

    blocked_existing = client.post(
        "/api/admin/management/drafts",
        json={"course_id": "ap-chemistry", "entity_id": review_question["id"]},
        headers=csrf(token),
    )
    assert blocked_existing.status_code == 400
    assert "editing is not enabled" in blocked_existing.json()["detail"]

    blocked_proposal = client.post(
        "/api/admin/management/proposals",
        json={
            "course_id": "ap-chemistry",
            "entity_type": "question",
            "unit_id": "unit-1",
            "title": "Read-only chemistry proposal check",
        },
        headers=csrf(token),
    )
    assert blocked_proposal.status_code == 400
    assert "editing is not enabled" in blocked_proposal.json()["detail"]


def test_managed_duplicate_entity_ids_are_isolated_across_courses(
    management_client,
    monkeypatch: pytest.MonkeyPatch,
):
    client, token, _ = management_client
    shared_id = "question:unit-1:shared-course-record"

    def fake_entity(entity_id: str, course_id: str = "ap-biology"):
        if entity_id != shared_id:
            return None
        label = "Biology" if course_id == "ap-biology" else "Chemistry"
        return {
            "id": shared_id,
            "type": "question",
            "course_id": course_id,
            "unit_id": "unit-1",
            "title": f"{label} shared question",
            "question_type": "review",
            "prompt": f"{label} prompt",
            "answer": f"{label} answer",
            "explanation": f"{label} explanation",
            "knowledge_ids": [],
            "source_path": None,
        }

    monkeypatch.setattr(
        admin_catalog,
        "require_editable_course",
        lambda course_id: {"course_id": course_id, "editable": True, "catalog_ready": True},
    )
    monkeypatch.setattr(admin_catalog, "get_entity", fake_entity)

    biology = client.post(
        "/api/admin/management/drafts",
        json={"course_id": "ap-biology", "entity_id": shared_id},
        headers=csrf(token),
    )
    chemistry = client.post(
        "/api/admin/management/drafts",
        json={"course_id": "ap-chemistry", "entity_id": shared_id},
        headers=csrf(token),
    )
    assert biology.status_code == chemistry.status_code == 200
    biology_draft = biology.json()
    chemistry_draft = chemistry.json()
    assert biology_draft["draft_id"] != chemistry_draft["draft_id"]
    assert biology_draft["course_id"] == "ap-biology"
    assert chemistry_draft["course_id"] == "ap-chemistry"

    biology_payload = dict(biology_draft["payload"])
    biology_payload["prompt"] = "Biology isolated prompt"
    biology_saved = client.patch(
        f"/api/admin/management/drafts/{biology_draft['draft_id']}",
        json={
            "course_id": "ap-biology",
            "payload": biology_payload,
            "expected_version": biology_draft["version"],
            "note": "Biology management isolation",
            "autosave": False,
        },
        headers=csrf(token),
    )
    assert biology_saved.status_code == 200

    wrong_course = client.patch(
        f"/api/admin/management/drafts/{chemistry_draft['draft_id']}",
        json={
            "course_id": "ap-biology",
            "payload": chemistry_draft["payload"],
            "expected_version": chemistry_draft["version"],
            "note": "Wrong course should fail",
            "autosave": False,
        },
        headers=csrf(token),
    )
    assert wrong_course.status_code == 404

    chemistry_payload = dict(chemistry_draft["payload"])
    chemistry_payload["prompt"] = "Chemistry isolated prompt"
    chemistry_saved = client.patch(
        f"/api/admin/management/drafts/{chemistry_draft['draft_id']}",
        json={
            "course_id": "ap-chemistry",
            "payload": chemistry_payload,
            "expected_version": chemistry_draft["version"],
            "note": "Chemistry management isolation",
            "autosave": False,
        },
        headers=csrf(token),
    )
    assert chemistry_saved.status_code == 200

    biology_after = client.get(
        f"/api/admin/drafts/{biology_draft['draft_id']}",
        params={"course_id": "ap-biology"},
    ).json()
    chemistry_after = client.get(
        f"/api/admin/drafts/{chemistry_draft['draft_id']}",
        params={"course_id": "ap-chemistry"},
    ).json()
    assert biology_after["payload"]["prompt"] == "Biology isolated prompt"
    assert chemistry_after["payload"]["prompt"] == "Chemistry isolated prompt"



def test_chemistry_search_export_bulk_preview_and_import_are_course_scoped(management_client):
    client, token, _ = management_client

    search = client.get(
        "/api/admin/management/search",
        params={
            "course_id": "ap-chemistry",
            "q": "Atomic Structure and Properties",
            "limit": 100,
        },
    )
    assert search.status_code == 200
    search_payload = search.json()
    assert search_payload["course_id"] == "ap-chemistry"
    assert search_payload["items"]
    assert all(item.get("course_id") == "ap-chemistry" for item in search_payload["items"])

    exported = client.get(
        "/api/admin/management/export",
        params={
            "course_id": "ap-chemistry",
            "unit_id": "unit-1",
            "entity_types": "question",
            "include_drafts": "true",
            "include_catalog": "true",
        },
    )
    assert exported.status_code == 200
    bundle = exported.json()
    assert bundle["scope"]["course_id"] == "ap-chemistry"
    assert bundle["records"]
    assert all(record["course_id"] == "ap-chemistry" for record in bundle["records"])
    assert all(record["payload"].get("course_id") == "ap-chemistry" for record in bundle["records"])
    assert "content/ap-biology/" not in str(bundle)

    small_bundle = {
        **bundle,
        "records": [bundle["records"][0]],
        "record_count": 1,
    }
    import_preview = client.post(
        "/api/admin/management/import/preview",
        json={"course_id": "ap-chemistry", "bundle": small_bundle},
        headers=csrf(token),
    )
    assert import_preview.status_code == 200
    assert import_preview.json()["course_id"] == "ap-chemistry"
    assert import_preview.json()["error_count"] == 0

    blocked_import = client.post(
        "/api/admin/management/import/apply",
        json={
            "course_id": "ap-chemistry",
            "bundle": small_bundle,
            "conflict_policy": "skip",
        },
        headers=csrf(token),
    )
    assert blocked_import.status_code == 400
    assert "editing is not enabled" in blocked_import.json()["detail"]

    wrong_course_import = client.post(
        "/api/admin/management/import/preview",
        json={"course_id": "ap-biology", "bundle": small_bundle},
        headers=csrf(token),
    )
    assert wrong_course_import.status_code == 400
    assert "belongs to course 'ap-chemistry'" in wrong_course_import.json()["detail"]

    bulk = client.post(
        "/api/admin/management/bulk/preview",
        json={
            "course_id": "ap-chemistry",
            "find": "The Sorting Gate",
            "replacement": "The Sorting Gate Revised",
            "case_sensitive": True,
            "unit_id": "unit-1",
            "entity_types": ["scene"],
            "limit": 100,
        },
        headers=csrf(token),
    )
    assert bulk.status_code == 200
    bulk_payload = bulk.json()
    assert bulk_payload["course_id"] == "ap-chemistry"
    assert bulk_payload["candidate_count"] > 0
    assert all(item["course_id"] == "ap-chemistry" for item in bulk_payload["candidates"])

    candidate = bulk_payload["candidates"][0]
    blocked_apply = client.post(
        "/api/admin/management/bulk/apply",
        json={
            "course_id": "ap-chemistry",
            "find": bulk_payload["find"],
            "replacement": bulk_payload["replacement"],
            "case_sensitive": bulk_payload["case_sensitive"],
            "targets": [
                {
                    "entity_id": candidate["entity_id"],
                    "expected_version": candidate["expected_version"],
                }
            ],
        },
        headers=csrf(token),
    )
    assert blocked_apply.status_code == 400
    assert "editing is not enabled" in blocked_apply.json()["detail"]


def test_staged_media_rows_are_isolated_by_course_when_second_course_is_editable(
    management_client,
    monkeypatch: pytest.MonkeyPatch,
):
    client, token, _ = management_client
    png = b"\x89PNG\r\n\x1a\n" + b"course-isolated-media"

    monkeypatch.setattr(
        admin_catalog,
        "require_editable_course",
        lambda course_id: {"course_id": course_id, "editable": True, "catalog_ready": True},
    )

    biology = client.post(
        "/api/admin/management/media/upload?filename=biology.png&course_id=ap-biology&unit_id=unit-1",
        content=png,
        headers={**csrf(token), "Content-Type": "image/png"},
    )
    chemistry = client.post(
        "/api/admin/management/media/upload?filename=chemistry.png&course_id=ap-chemistry&unit_id=unit-1",
        content=png,
        headers={**csrf(token), "Content-Type": "image/png"},
    )
    assert biology.status_code == chemistry.status_code == 200
    assert biology.json()["course_id"] == "ap-biology"
    assert chemistry.json()["course_id"] == "ap-chemistry"

    biology_list = client.get(
        "/api/admin/management/media/staged",
        params={"course_id": "ap-biology", "status": "staged", "limit": 100},
    ).json()
    chemistry_list = client.get(
        "/api/admin/management/media/staged",
        params={"course_id": "ap-chemistry", "status": "staged", "limit": 100},
    ).json()

    assert {item["original_filename"] for item in biology_list["items"]} == {"biology.png"}
    assert {item["original_filename"] for item in chemistry_list["items"]} == {"chemistry.png"}

    chemistry_asset = chemistry.json()
    wrong_course = client.patch(
        f"/api/admin/management/media/{chemistry_asset['asset_id']}",
        json={
            "course_id": "ap-biology",
            "expected_version": chemistry_asset["version"],
            "alt_text": "wrong course",
            "caption": "",
            "transcript": "",
            "unit_id": "unit-1",
            "entity_id": None,
        },
        headers=csrf(token),
    )
    assert wrong_course.status_code == 404
