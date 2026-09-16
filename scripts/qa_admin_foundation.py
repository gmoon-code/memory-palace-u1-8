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
    auth = ROOT / "backend" / "admin_auth.py"
    settings = (ROOT / "backend" / "settings.py").read_text(encoding="utf-8")
    main_py = (ROOT / "backend" / "main.py").read_text(encoding="utf-8")
    pages_build = (ROOT / "scripts" / "build_github_pages.py").read_text(encoding="utf-8")
    plan = ROOT / "docs" / "admin" / "CONTENT_STUDIO_IMPLEMENTATION_PLAN.md"

    require(html.is_file(), "frontend/admin/index.html is missing")
    require(css.is_file(), "frontend/admin/admin.css is missing")
    require(js.is_file(), "frontend/admin/admin.js is missing")
    require(auth.is_file(), "backend/admin_auth.py is missing")
    require(plan.is_file(), "Content Studio implementation plan is missing")

    html_text = html.read_text(encoding="utf-8")
    js_text = js.read_text(encoding="utf-8")
    auth_text = auth.read_text(encoding="utf-8")

    require("Complete Story Replacement" in html_text, "complete story replacement is not represented in admin navigation")
    require("Question Bank" in html_text and "Version History" in html_text and "Publishing" in html_text, "core admin modules are missing")
    require("Security and Audit" in html_text, "security and audit workspace is missing")
    require("MEMORY_PALACE_ADMIN_ENABLED" in settings, "admin enable flag is not defined")
    require('os.getenv("MEMORY_PALACE_ADMIN_ENABLED", "false")' in settings, "admin enable flag does not default to false")
    require("if not ADMIN_ENABLED" in main_py, "admin route is not guarded by the disabled-by-default flag")
    require('@app.get("/admin")' in main_py, "admin root route is missing")
    require('@app.get("/admin/{path:path}")' in main_py, "admin asset route is missing")
    require('path == "admin" or path.startswith("admin/")' in main_py, "SPA fallback does not protect the disabled admin route")

    require('@app.post("/api/admin/login")' in main_py, "protected admin login route is missing")
    require('@app.post("/api/admin/logout")' in main_py, "protected admin logout route is missing")
    require('@app.get("/api/admin/session")' in main_py, "admin session route is missing")
    require('@app.get("/api/admin/course")' in main_py, "protected admin course route is missing")
    require('@app.get("/api/admin/audit")' in main_py, "admin audit route is missing")
    require('@app.get("/api/admin/security")' in main_py, "admin security status route is missing")

    require('apiRequest("/api/admin/course")' in js_text, "admin dashboard is not using the protected course route")
    require('/api/admin/units/${encodeURIComponent(unit.unit_id)}' in js_text, "admin dashboard is not using protected unit summaries")
    require('method: "POST"' in js_text, "login and logout POST requests are missing")
    require('method: "PUT"' not in js_text and 'method: "PATCH"' not in js_text and 'method: "DELETE"' not in js_text, "Step 2 frontend exposes a content mutation method")

    require("hashlib.scrypt" in auth_text, "admin passwords are not using scrypt")
    require("httponly=True" in main_py, "admin session cookie is not HttpOnly")
    require('samesite="strict"' in main_py, "admin session cookie is not SameSite strict")
    require("require_csrf=True" in main_py, "protected admin action does not require CSRF")
    require("admin_login_failures" in auth_text, "login failure rate-limit store is missing")
    require("admin_audit" in auth_text, "server-side admin audit store is missing")
    require("session_hash" in auth_text and "csrf_hash" in auth_text, "server-side session token hashing is missing")

    require('copy_tree(ROOT / "frontend" / "css"' in pages_build, "GitHub Pages build contract unexpectedly changed")
    require('copy_tree(ROOT / "frontend" / "js"' in pages_build, "GitHub Pages build contract unexpectedly changed")
    require('frontend" / "admin' not in pages_build, "GitHub Pages build copies the admin directory")

    print("ADMIN FOUNDATION QA PASS")
    print("- admin shell exists and remains disabled by default")
    print("- teacher authentication and server-side sessions are present")
    print("- protected admin read APIs are separated from student APIs")
    print("- login throttling, CSRF protection, and audit storage are present")
    print("- no content mutation API is exposed in Step 2")
    print("- GitHub Pages excludes admin assets")
    print("- complete story replacement remains a first-class module")


if __name__ == "__main__":
    main()
