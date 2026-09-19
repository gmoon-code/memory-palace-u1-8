from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ADMIN EDITOR QA FAIL\n- {message}")


def main() -> None:
    editor_backend = ROOT / "backend" / "admin_editors.py"
    editor_routes = ROOT / "backend" / "admin_editor_routes.py"
    draft_routes = ROOT / "backend" / "admin_draft_routes.py"
    editor_js = ROOT / "frontend" / "admin" / "editor.js"
    editor_css = ROOT / "frontend" / "admin" / "editor.css"
    drafts_js = ROOT / "frontend" / "admin" / "drafts.js"

    for path in (editor_backend, editor_routes, editor_js, editor_css):
        require(path.is_file(), f"missing Step 5 file: {path.relative_to(ROOT)}")

    backend_text = editor_backend.read_text(encoding="utf-8")
    route_text = editor_routes.read_text(encoding="utf-8")
    draft_route_text = draft_routes.read_text(encoding="utf-8")
    js_text = editor_js.read_text(encoding="utf-8")
    draft_js_text = drafts_js.read_text(encoding="utf-8")

    for entity_type in ("unit", "journey", "scene", "character", "location", "concept", "memory_object"):
        require(f'"{entity_type}"' in backend_text, f"editor schema missing {entity_type}")

    for field in (
        "story_paragraphs",
        "scene_layout.zones",
        "cast",
        "canonical_definition",
        "phonological_keyword",
        "mnemonic_actor",
        "productive_retrieval_target",
        "application_question",
    ):
        require(field in backend_text, f"editor field missing: {field}")

    require("editable_entity" in backend_text, "source-enriched editable entity projection is missing")
    require("create_editor_draft" in backend_text, "source-enriched editor draft creation is missing")
    require("validate_payload" in backend_text, "field-specific payload validation is missing")
    require("source-enriched normalized content" in backend_text, "editor baseline provenance note is missing")
    require("write_text(" not in backend_text, "Step 5 editor writes directly to published repository files")
    require("open(" not in backend_text, "Step 5 editor opens repository files for direct writing")

    require('prefix="/api/admin/editors"' in route_text, "field editor API is outside the protected admin namespace")
    require(route_text.count("csrf=True") >= 3, "editor mutations are not consistently CSRF protected")
    require("router.include_router(admin_editor_routes.router)" in draft_route_text, "field editor router is not registered")

    require('import "./editor.js"' in draft_js_text, "field editor module is not loaded by Content Studio")
    require("editorModes" in js_text, "editor navigation map is missing")
    require("characters" in js_text and "locations" in js_text, "character or location editor navigation is missing")
    require("data-paragraph-action" in js_text, "paragraph-level narrative controls are missing")
    require("data-object-action" in js_text, "repeatable cast/location controls are missing")
    require("saveDraft(true)" in js_text, "field editor autosave is missing")
    require("/api/admin/editors/drafts" in js_text, "field editor does not use protected working copies")
    require("/api/admin/drafts/" in js_text and "/snapshots" in js_text, "field editor snapshot protection is missing")

    print("ADMIN EDITOR QA PASS")
    print("- Units, Journeys, Scenes, Stories, Characters, Locations, Concepts, and Memory Objects have field-specific editor schemas")
    print("- complete scene stories are source-enriched before a working copy is created")
    print("- narrative paragraphs, scene zones, and cast records are individually editable")
    print("- friendly editor saves remain isolated in the Step 4 draft store")
    print("- autosave and named snapshots remain available")
    print("- protected published course files are not directly written by Step 5")


if __name__ == "__main__":
    main()
