from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(path: str) -> str:
    target = ROOT / path
    if not target.exists():
        raise AssertionError(f"Missing required capability-audit file: {path}")
    return target.read_text(encoding="utf-8")


def main() -> None:
    capabilities = require("backend/admin_capabilities.py")
    routes = require("backend/admin_capability_routes.py")
    draft_routes = require("backend/admin_draft_routes.py")
    replacement_routes = require("backend/admin_replacement_routes.py")
    frontend = require("frontend/admin/capability-audit.js")
    require("frontend/admin/capability-audit.css")
    tests = require("tests/test_admin_capabilities.py")

    for workspace in (
        "dashboard", "course-map", "units", "journeys", "scenes", "stories",
        "characters", "locations", "replacement", "concepts", "memory-objects",
        "questions", "review", "challenge", "media", "preview", "health",
        "drafts", "versions", "import-export", "publishing", "security", "settings",
    ):
        assert f'"id": "{workspace}"' in capabilities, workspace

    assert 'APIRouter(prefix="/api/admin/capabilities"' in routes
    assert "admin_auth.get_session" in routes
    assert "admin_capability_routes.router" in draft_routes

    for module in (
        "/admin/drafts-core.js",
        "/admin/replacement.js",
        "/admin/publication.js",
        "/admin/health-repair.js",
        "/admin/capability-audit.js",
    ):
        assert module in replacement_routes, module

    assert 'data-view="capability-audit"' in frontend
    assert "Integrated administrator workspace" in frontend
    assert "Characters" in frontend and "Locations" in frontend
    assert "Browse" in capabilities and "Recover" in capabilities
    assert "analytics-deferred" in capabilities
    assert "student_content_write_from_audit" in capabilities

    assert "test_canonical_admin_loader_boots_late_stage_modules" in tests
    assert "test_all_original_administrator_workspaces_have_implementation_evidence" in tests

    print("CONTENT STUDIO ADMIN CAPABILITY AUDIT QA PASS")


if __name__ == "__main__":
    main()
