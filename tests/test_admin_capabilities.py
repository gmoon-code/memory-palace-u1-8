from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend import (
    admin_auth,
    admin_capabilities,
    admin_capability_routes,
    admin_draft_routes,
    admin_replacement_routes,
)
from backend import main as main_module

PASSWORD = "correct-horse-battery-staple"
USERNAME = "teacher-admin"
SESSION_SECRET = "test-session-secret-that-is-longer-than-thirty-two-characters"


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    password_hash = admin_auth.hash_password(PASSWORD, salt=b"0123456789abcdef")
    monkeypatch.setattr(main_module, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_draft_routes, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_capability_routes, "ADMIN_ENABLED", True)
    monkeypatch.setattr(admin_replacement_routes, "ADMIN_ENABLED", True)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_USERNAME", USERNAME)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_PASSWORD_HASH", password_hash)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_SESSION_SECRET", SESSION_SECRET)
    monkeypatch.setenv("MEMORY_PALACE_ADMIN_DB", str(tmp_path / "admin-security.sqlite3"))
    with TestClient(main_module.app) as test_client:
        yield test_client


def login(test_client: TestClient):
    response = test_client.post(
        "/api/admin/login",
        json={"username": USERNAME, "password": PASSWORD},
    )
    assert response.status_code == 200
    return response.json()


def test_capability_audit_requires_owner_authentication(client):
    assert client.get("/api/admin/capabilities").status_code == 401
    login(client)
    response = client.get("/api/admin/capabilities")
    assert response.status_code == 200


def test_all_original_administrator_workspaces_have_implementation_evidence(client):
    login(client)
    report = client.get("/api/admin/capabilities").json()
    assert report["schema"] == admin_capabilities.CAPABILITY_AUDIT_SCHEMA
    assert report["summary"]["workspace_count"] >= 23
    assert report["summary"]["incomplete"] == 0
    assert report["summary"]["implemented"] == report["summary"]["workspace_count"]
    assert report["student_content_write_from_audit"] is False
    assert report["zero_cost_boundary"] is True

    ids = {item["id"] for item in report["workspaces"]}
    required = {
        "dashboard", "course-map", "units", "journeys", "scenes", "stories",
        "characters", "locations", "replacement", "concepts", "memory-objects",
        "questions", "review", "challenge", "media", "preview", "health",
        "drafts", "versions", "import-export", "publishing", "security", "settings",
    }
    assert required.issubset(ids)


def test_integrated_workflow_is_explicit_and_recoverable(client):
    login(client)
    report = client.get("/api/admin/capabilities").json()
    labels = [item["label"] for item in report["workflow"]]
    assert labels == ["Browse", "Edit", "Draft", "Preview", "Validate", "Publish", "Recover"]
    assert report["workflow"][-1]["view"] == "versions"


def test_limits_do_not_claim_unimplemented_features(client):
    login(client)
    report = client.get("/api/admin/capabilities").json()
    limits = {item["id"]: item for item in report["intentional_limits"]}
    assert "analytics-deferred" in limits
    assert limits["analytics-deferred"]["status"] == "deferred"
    assert "media-staging-only" in limits
    assert "publication-off-by-default" in limits


def test_canonical_admin_loader_boots_late_stage_modules(client):
    login(client)
    response = client.get("/admin/drafts.js")
    assert response.status_code == 200
    source = response.text
    modules = (
        "/admin/drafts-core.js",
        "/admin/replacement.js",
        "/admin/publication.js",
        "/admin/health-repair.js",
        "/admin/capability-audit.js",
        "/admin/workflow.js",
    )
    for module in modules:
        assert f'import "{module}"' in source
    assert source.rfind('import "/admin/workflow.js"') > source.rfind('import "/admin/capability-audit.js"')


def test_workflow_asset_preserves_context_without_automatic_mutations(client):
    login(client)
    response = client.get("/admin/workflow.js")
    assert response.status_code == 200
    source = response.text
    assert "story-method-content-studio-workflow-context-v1" in source
    assert "sessionStorage" in source
    assert "workflow-version-history" in source
    for stage in ("browse", "edit", "draft", "preview", "validate", "publish", "recover"):
        assert f'data-workflow-stage="{stage}"' in source
    assert 'method: "POST"' not in source
    assert "content/ap-biology" not in source
