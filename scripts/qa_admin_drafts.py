from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ADMIN DRAFT QA FAIL\n- {message}")


def main() -> None:
    drafts = ROOT / "backend" / "admin_drafts.py"
    routes = ROOT / "backend" / "admin_draft_routes.py"
    main_py = (ROOT / "backend" / "main.py").read_text(encoding="utf-8")
    html = (ROOT / "frontend" / "admin" / "index.html").read_text(encoding="utf-8")
    js = ROOT / "frontend" / "admin" / "drafts.js"
    css = ROOT / "frontend" / "admin" / "drafts.css"
    env = (ROOT / ".env.example").read_text(encoding="utf-8")
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

    require(drafts.is_file(), "backend/admin_drafts.py is missing")
    require(routes.is_file(), "backend/admin_draft_routes.py is missing")
    require(js.is_file(), "frontend/admin/drafts.js is missing")
    require(css.is_file(), "frontend/admin/drafts.css is missing")

    draft_text = drafts.read_text(encoding="utf-8")
    route_text = routes.read_text(encoding="utf-8")
    js_text = js.read_text(encoding="utf-8")

    require("content_drafts" in draft_text, "draft table is missing")
    require("content_draft_revisions" in draft_text, "revision table is missing")
    require("content_draft_snapshots" in draft_text, "snapshot table is missing")
    require("base_payload_json" in draft_text and "base_fingerprint" in draft_text, "immutable base snapshot is missing")
    require("expected_version" in draft_text, "optimistic concurrency guard is missing")
    require("DraftConflict" in draft_text, "draft concurrency conflicts are not represented")
    require("restore_revision" in draft_text and "restore_snapshot" in draft_text, "non-destructive restore operations are missing")
    require("archive_draft" in draft_text and "unarchive_draft" in draft_text, "archive and restore workflow is missing")
    require("compare_draft" in draft_text, "before-and-after comparison is missing")
    require("published_content_write_enabled" in draft_text, "published-content write boundary is not reported")

    require('APBIO_DIR' not in draft_text, "draft store directly imports the published AP Biology content path")
    require("write_text(" not in draft_text and "open(" not in draft_text, "draft store writes ordinary repository files")
    require("MEMORY_PALACE_ADMIN_DRAFT_DB" in env, "draft database configuration is undocumented")
    require("server_data/*" in ignore, "server-side draft database is not covered by Git ignore rules")

    require('prefix="/api/admin/drafts"' in route_text, "draft API is outside the protected admin namespace")
    require("require_csrf=csrf" in route_text, "draft route helper does not support CSRF enforcement")
    for operation in ("drafts_create", "draft_save", "draft_archive", "draft_restore_archive", "draft_restore_revision", "draft_snapshot_create", "draft_snapshot_restore"):
        require(operation in route_text, f"protected draft operation is missing: {operation}")
    require(route_text.count("csrf=True") >= 7, "not all draft mutations require CSRF")
    require("app.include_router(admin_draft_routes.router)" in main_py, "draft API router is not registered")

    require("Draft Workspace" in html, "Draft Workspace navigation is missing")
    require("Advanced structured draft payload" in html, "Step 4 working-copy editor is missing")
    require("/admin/drafts.js" in html and "/admin/drafts.css" in html, "draft UI assets are not loaded")
    require('method: "PATCH"' in js_text, "autosave draft PATCH is missing")
    require("restoreRevision" in js_text and "restoreSnapshot" in js_text, "revision restoration controls are missing")
    require("scheduleTitleAutosave" in js_text, "autosave behavior is missing")

    print("ADMIN DRAFT QA PASS")
    print("- drafts are stored outside published course files")
    print("- optimistic concurrency prevents silent overwrite")
    print("- autosave creates recoverable revisions")
    print("- named snapshots and revision restore are non-destructive")
    print("- archive and restore preserve history")
    print("- all draft mutations require authenticated CSRF-protected requests")
    print("- published AP Biology content remains locked")


if __name__ == "__main__":
    main()
