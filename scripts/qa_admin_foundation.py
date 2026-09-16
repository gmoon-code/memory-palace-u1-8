from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ADMIN FOUNDATION QA FAIL\n- {message}")


def main() -> None:
    html = ROOT / "frontend" / "admin" / "index.html"
    css = ROOT / "frontend" / "admin" / "admin.css"
    js = ROOT / "frontend" / "admin" / "admin.js"
    settings = (ROOT / "backend" / "settings.py").read_text(encoding="utf-8")
    main_py = (ROOT / "backend" / "main.py").read_text(encoding="utf-8")
    pages_build = (ROOT / "scripts" / "build_github_pages.py").read_text(encoding="utf-8")
    plan = ROOT / "docs" / "admin" / "CONTENT_STUDIO_IMPLEMENTATION_PLAN.md"

    require(html.is_file(), "frontend/admin/index.html is missing")
    require(css.is_file(), "frontend/admin/admin.css is missing")
    require(js.is_file(), "frontend/admin/admin.js is missing")
    require(plan.is_file(), "Content Studio implementation plan is missing")

    html_text = html.read_text(encoding="utf-8")
    js_text = js.read_text(encoding="utf-8")

    require("Complete Story Replacement" in html_text, "complete story replacement is not represented in admin navigation")
    require("Question Bank" in html_text and "Version History" in html_text and "Publishing" in html_text, "core admin modules are missing")
    require("MEMORY_PALACE_ADMIN_ENABLED" in settings, "admin enable flag is not defined")
    require('os.getenv("MEMORY_PALACE_ADMIN_ENABLED", "false")' in settings, "admin enable flag does not default to false")
    require("if not ADMIN_ENABLED" in main_py, "admin route is not guarded by the disabled-by-default flag")
    require('@app.get("/admin")' in main_py, "admin root route is missing")
    require('@app.get("/admin/{path:path}")' in main_py, "admin asset route is missing")
    require('path == "admin" or path.startswith("admin/")' in main_py, "SPA fallback does not protect the disabled admin route")

    forbidden_write_tokens = [
        'method: "POST"',
        'method: "PUT"',
        'method: "PATCH"',
        'method: "DELETE"',
        "method:'POST'",
        "method:'PUT'",
        "method:'PATCH'",
        "method:'DELETE'",
    ]
    require(not any(token in js_text for token in forbidden_write_tokens), "Step 1 admin JavaScript contains a write request")
    require('readJson("/api/course")' in js_text, "admin dashboard does not read the existing course registry")
    require('/api/units/${encodeURIComponent(unit.unit_id)}' in js_text, "admin dashboard does not read unit summaries for complete inventory totals")

    require('copy_tree(ROOT / "frontend" / "css"' in pages_build, "GitHub Pages build contract unexpectedly changed")
    require('copy_tree(ROOT / "frontend" / "js"' in pages_build, "GitHub Pages build contract unexpectedly changed")
    require('frontend" / "admin' not in pages_build, "GitHub Pages build copies the admin directory")

    print("ADMIN FOUNDATION QA PASS")
    print("- admin shell exists")
    print("- admin is disabled by default")
    print("- Step 1 exposes no write request")
    print("- GitHub Pages excludes admin assets")
    print("- complete story replacement is reserved as a first-class module")
    print("- course registry and unit summaries drive inventory totals")


if __name__ == "__main__":
    main()
