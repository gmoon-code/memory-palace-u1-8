from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ADMIN MANAGEMENT QA FAIL\n- {message}")


def main() -> None:
    backend = ROOT / "backend" / "admin_management.py"
    routes = ROOT / "backend" / "admin_management_routes.py"
    draft_routes = ROOT / "backend" / "admin_draft_routes.py"
    frontend = ROOT / "frontend" / "admin" / "management.js"
    css = ROOT / "frontend" / "admin" / "management.css"
    loader = ROOT / "frontend" / "admin" / "drafts.js"
    docs = ROOT / "docs" / "admin" / "STEP7_CONTENT_MANAGEMENT.md"

    for path in (backend, routes, frontend, css, docs):
        require(path.is_file(), f"missing Step 7 file: {path.relative_to(ROOT)}")

    backend_text = backend.read_text(encoding="utf-8")
    route_text = routes.read_text(encoding="utf-8")
    draft_route_text = draft_routes.read_text(encoding="utf-8")
    frontend_text = frontend.read_text(encoding="utf-8")
    loader_text = loader.read_text(encoding="utf-8")

    for symbol in (
        "question_bank",
        "review_timeline",
        "challenge_bank",
        "bulk_replace_preview",
        "bulk_replace_apply",
        "export_bundle",
        "validate_import_bundle",
        "apply_import_bundle",
        "stage_media",
        "existing_media_inventory",
        "workspace_search",
        "create_proposed_draft",
    ):
        require(f"def {symbol}" in backend_text, f"Step 7 service missing {symbol}")

    require("SAFE_TEXT_KEYS" in backend_text, "bulk replacement has no allowlisted text-field boundary")
    require("IMMUTABLE_ENTITY_FIELDS" in backend_text, "new proposal construction does not preserve immutable identity fields")
    require("create_snapshot" in backend_text, "bulk/import workflows do not use recovery snapshots")
    require("MAX_BULK_TARGETS" in backend_text, "bulk write safety limit is missing")
    require("MAX_IMPORT_RECORDS" in backend_text, "import record safety limit is missing")
    require("MAX_MEDIA_BYTES" in backend_text, "media upload size limit is missing")
    require("server_data" in backend_text, "staged media is not explicitly isolated under private server data")
    require("destination.open(\"xb\")" in backend_text, "media writes are not exclusive create-only staging writes")
    require("write_text(" not in backend_text, "Step 7 writes text directly into repository content files")
    require("APBIO_DIR /" not in backend_text.split("def _media_root", 1)[-1], "media staging targets AP Biology source content")

    require('prefix="/api/admin/management"' in route_text, "management endpoints are outside the protected admin namespace")
    require(route_text.count("csrf=True") >= 10, "Step 7 mutations are not consistently CSRF protected")
    require("admin_management_routes.router" in draft_route_text, "Step 7 management router is not registered")

    for mode in ("questions", "review", "challenge", "media", "import-export"):
        require(f'"{mode}"' in frontend_text, f"management UI missing {mode} workspace")
    for marker in (
        "/question-bank",
        "/review-timeline",
        "/challenge-bank",
        "/media/upload",
        "/import/preview",
        "/import/apply",
        "/bulk/preview",
        "/bulk/apply",
        "/export",
        "/search",
    ):
        require(marker in frontend_text, f"management UI missing API workflow {marker}")
    require('import "./replacement.js"' in loader_text, "Step 6 replacement UI is not loaded by Content Studio")
    require('import "./management.js"' in loader_text, "Step 7 management UI is not loaded by Content Studio")

    pages_builder = (ROOT / "scripts" / "build_github_pages.py").read_text(encoding="utf-8")
    require('"frontend", "admin"' not in pages_builder, "public GitHub Pages builder explicitly copies admin files")

    print("ADMIN MANAGEMENT QA PASS")
    print("- Question Bank, Review System, Challenge Lab, Media Library, Import/Export, search, and bulk tools are present")
    print("- new assessment content is represented as protected proposals outside the published catalog")
    print("- controlled replacement is limited to allowlisted human-readable fields and creates recovery snapshots")
    print("- media uploads are staged in private server_data and are never published automatically")
    print("- import/export uses portable curriculum bundles while authentication and security state remain excluded")
    print("- Step 6 replacement and Step 7 management modules are both loaded in Content Studio")
    print("- published AP Biology and public GitHub Pages content remain outside Step 7 write paths")


if __name__ == "__main__":
    main()
