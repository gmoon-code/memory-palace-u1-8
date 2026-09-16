from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import admin_auth, admin_draft_routes, admin_editor_routes, admin_publication, admin_publication_routes
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
def publication_client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    password_hash = admin_auth.hash_password(PASSWORD, salt=b"0123456789abcdef")
    monkeypatch.setattr(main_module, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_draft_routes, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_editor_routes, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_publication_routes, "ADMIN_ENABLED", True)
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
    with TestClient(main_module.app) as client:
        login = client.post("/api/admin/login", json={"username": USERNAME, "password": PASSWORD})
        assert login.status_code == 200
        yield client, login.json()["csrf_token"], tmp_path


def changed_scene(client: TestClient, token: str, title: str = "Step 9 candidate-only scene title") -> dict:
    created = client.post("/api/admin/editors/drafts", json={"entity_id": SCENE_ID}, headers=csrf(token))
    assert created.status_code == 200
    draft = created.json()
    payload = dict(draft["payload"])
    payload["title"] = title
    saved = client.patch(
        f"/api/admin/editors/drafts/{draft['draft_id']}",
        json={"payload": payload, "expected_version": draft["version"], "note": "Step 9 publication test", "autosave": False},
        headers=csrf(token),
    )
    assert saved.status_code == 200
    return saved.json()


def create_candidate(client: TestClient, token: str, draft_id: str) -> dict:
    response = client.post(
        "/api/admin/publication/candidates",
        json={
            "draft_ids": [draft_id],
            "title": "Step 9 test release",
            "notes": "Candidate-only publication regression.",
            "warnings_acknowledged": True,
        },
        headers=csrf(token),
    )
    assert response.status_code == 200, response.text
    return response.json()


def test_candidate_creation_is_non_destructive_and_hashes_exact_files(publication_client):
    client, token, tmp_path = publication_client
    before = digest(SCENE_SOURCE)
    draft = changed_scene(client, token)

    candidate = create_candidate(client, token, draft["draft_id"])
    assert candidate["status"] == "created"
    assert digest(SCENE_SOURCE) == before
    manifest = candidate["manifest"]
    assert manifest["publication_model"].startswith("candidate package only")
    assert len(manifest["files"]) == 1
    record = manifest["files"][0]
    assert record["path"].endswith("unit-8/journeys/U8-J1.json")
    assert record["before_sha256"] == before
    assert record["after_sha256"] != record["before_sha256"]

    candidate_root = tmp_path / "content-studio-publications" / "candidates" / candidate["candidate_id"]
    assert (candidate_root / "before" / record["path"]).exists()
    after = candidate_root / "after" / record["path"]
    assert after.exists()
    assert "Step 9 candidate-only scene title" in after.read_text(encoding="utf-8")

    snapshots = client.get(f"/api/admin/drafts/{draft['draft_id']}/snapshots")
    assert snapshots.status_code == 200
    assert any("Pre-publication snapshot" in item["label"] for item in snapshots.json()["items"])
    assert digest(SCENE_SOURCE) == before


def test_candidate_creation_requires_csrf(publication_client):
    client, token, _ = publication_client
    draft = changed_scene(client, token)
    response = client.post(
        "/api/admin/publication/candidates",
        json={"draft_ids": [draft["draft_id"]], "title": "Blocked request", "warnings_acknowledged": True},
    )
    assert response.status_code == 403


def test_stale_candidate_is_rejected_before_validation(publication_client, monkeypatch: pytest.MonkeyPatch):
    client, token, _ = publication_client
    draft = changed_scene(client, token)
    candidate = create_candidate(client, token, draft["draft_id"])

    payload = dict(draft["payload"])
    payload["title"] = "Changed after candidate creation"
    updated = client.patch(
        f"/api/admin/editors/drafts/{draft['draft_id']}",
        json={"payload": payload, "expected_version": draft["version"], "autosave": False},
        headers=csrf(token),
    )
    assert updated.status_code == 200
    monkeypatch.setattr(admin_publication, "_run_candidate_qa", lambda candidate: {"passed": True, "commands": [], "validated_at": "test"})
    result = client.post(
        f"/api/admin/publication/candidates/{candidate['candidate_id']}/validate",
        headers=csrf(token),
    )
    assert result.status_code == 409
    assert "changed after" in result.json()["detail"]


def test_validation_and_github_delivery_use_exact_hash_gates(publication_client, monkeypatch: pytest.MonkeyPatch):
    client, token, tmp_path = publication_client
    draft = changed_scene(client, token)
    candidate = create_candidate(client, token, draft["draft_id"])
    candidate_id = candidate["candidate_id"]

    monkeypatch.setattr(
        admin_publication,
        "_run_candidate_qa",
        lambda item: {"passed": True, "commands": [{"command": "test-gate", "returncode": 0}], "validated_at": "test"},
    )
    validated = client.post(f"/api/admin/publication/candidates/{candidate_id}/validate", headers=csrf(token))
    assert validated.status_code == 200
    assert validated.json()["status"] == "validated"

    monkeypatch.setenv("MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED", "true")
    monkeypatch.setenv("MEMORY_PALACE_GITHUB_TOKEN", "test-token")
    monkeypatch.setenv("MEMORY_PALACE_GITHUB_REPOSITORY", "gmoon-code/memory-palace-u1-8")
    monkeypatch.setenv("MEMORY_PALACE_GITHUB_BASE_BRANCH", "main")
    monkeypatch.setenv("MEMORY_PALACE_GITHUB_ALLOW_MERGE", "true")

    candidate_root = tmp_path / "content-studio-publications" / "candidates" / candidate_id
    file_record = validated.json()["manifest"]["files"][0]
    before_bytes = (candidate_root / "before" / file_record["path"]).read_bytes()
    after_bytes = (candidate_root / "after" / file_record["path"]).read_bytes()
    remote_state = {"merged": False}
    monkeypatch.setattr(
        admin_publication,
        "_remote_file_bytes",
        lambda config, path, ref: after_bytes if remote_state["merged"] else before_bytes,
    )

    counter = {"blob": 0}

    def fake_gh(config, method, path, **kwargs):
        if path.endswith("/git/ref/heads/main"):
            return {"object": {"sha": "base-commit"}}
        if path.endswith("/git/commits/base-commit"):
            return {"tree": {"sha": "base-tree"}}
        if path.endswith("/git/blobs") and method == "POST":
            counter["blob"] += 1
            return {"sha": f"blob-{counter['blob']}"}
        if path.endswith("/git/trees") and method == "POST":
            return {"sha": "candidate-tree"}
        if path.endswith("/git/commits") and method == "POST":
            return {"sha": "candidate-commit"}
        if path.endswith("/git/refs") and method == "POST":
            return {"ref": "refs/heads/content-studio/test"}
        if path.endswith("/pulls") and method == "POST":
            return {"number": 42}
        if path.endswith("/commits/candidate-commit/check-runs") and method == "GET":
            return {"check_runs": [{"name": "Memory Palace QA", "status": "completed", "conclusion": "success", "html_url": "https://example.test/check"}]}
        if path.endswith("/pulls/42/merge") and method == "PUT":
            remote_state["merged"] = True
            return {"merged": True, "sha": "merge-sha"}
        raise AssertionError(f"Unexpected fake GitHub call {method} {path}")

    monkeypatch.setattr(admin_publication, "_gh", fake_gh)
    submitted = client.post(f"/api/admin/publication/candidates/{candidate_id}/submit", headers=csrf(token))
    assert submitted.status_code == 200, submitted.text
    assert submitted.json()["status"] == "submitted"
    assert submitted.json()["github"]["pr_number"] == 42

    checks = client.post(f"/api/admin/publication/candidates/{candidate_id}/checks", headers=csrf(token))
    assert checks.status_code == 200
    assert checks.json()["status"] == "merge_ready"

    merged = client.post(f"/api/admin/publication/candidates/{candidate_id}/merge", headers=csrf(token))
    assert merged.status_code == 200
    assert merged.json()["status"] == "merged_pending_verify"

    verified = client.post(f"/api/admin/publication/candidates/{candidate_id}/verify", headers=csrf(token))
    assert verified.status_code == 200, verified.text
    release = verified.json()
    assert release["release_id"].startswith("release-")
    assert release["summary"]["files"][0]["after_sha256"] == hashlib.sha256(after_bytes).hexdigest()
    assert digest(SCENE_SOURCE) == hashlib.sha256(before_bytes).hexdigest()

    archived = client.get(f"/api/admin/drafts/{draft['draft_id']}")
    assert archived.status_code == 200
    assert archived.json()["status"] == "archived"

    rollback = client.post(
        f"/api/admin/publication/releases/{release['release_id']}/rollback",
        json={"title": "Rollback Step 9 test release"},
        headers=csrf(token),
    )
    assert rollback.status_code == 200, rollback.text
    rollback_candidate = rollback.json()
    assert rollback_candidate["kind"] == "rollback"
    rollback_file = rollback_candidate["manifest"]["files"][0]
    assert rollback_file["before_sha256"] == file_record["after_sha256"]
    assert rollback_file["after_sha256"] == file_record["before_sha256"]
    assert digest(SCENE_SOURCE) == hashlib.sha256(before_bytes).hexdigest()


def test_remote_base_change_blocks_submission(publication_client, monkeypatch: pytest.MonkeyPatch):
    client, token, _ = publication_client
    draft = changed_scene(client, token)
    candidate = create_candidate(client, token, draft["draft_id"])
    monkeypatch.setattr(admin_publication, "_run_candidate_qa", lambda item: {"passed": True, "commands": [], "validated_at": "test"})
    assert client.post(f"/api/admin/publication/candidates/{candidate['candidate_id']}/validate", headers=csrf(token)).status_code == 200

    monkeypatch.setenv("MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED", "true")
    monkeypatch.setenv("MEMORY_PALACE_GITHUB_TOKEN", "test-token")
    monkeypatch.setattr(admin_publication, "_remote_file_bytes", lambda config, path, ref: b"remote source changed")
    result = client.post(f"/api/admin/publication/candidates/{candidate['candidate_id']}/submit", headers=csrf(token))
    assert result.status_code == 409
    assert "GitHub base file changed" in result.json()["detail"]
