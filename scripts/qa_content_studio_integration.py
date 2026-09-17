from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    target = ROOT / path
    if not target.is_file():
        raise SystemExit(f"CONTENT STUDIO INTEGRATION QA FAIL: missing {path}")
    return target.read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"CONTENT STUDIO INTEGRATION QA FAIL: {message}")


def main() -> None:
    required_qa = [
        "scripts/qa_admin_foundation.py",
        "scripts/qa_admin_catalog.py",
        "scripts/qa_admin_drafts.py",
        "scripts/qa_admin_editors.py",
        "scripts/qa_admin_replacements.py",
        "scripts/qa_admin_management.py",
        "scripts/qa_admin_quality.py",
        "scripts/qa_admin_publication.py",
    ]
    for path in required_qa:
        require((ROOT / path).is_file(), f"missing prior-stage QA {path}")

    env_example = read(".env.example")
    require("MEMORY_PALACE_ADMIN_ENABLED=false" in env_example, "admin gate must default off")
    require("MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED=false" in env_example, "publication gate must default off")
    require("MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED=false" in env_example, "GitHub publication gate must default off")
    require("MEMORY_PALACE_GITHUB_ALLOW_MERGE=false" in env_example, "server-side merge gate must default off")
    require("MEMORY_PALACE_GITHUB_TOKEN=\n" in env_example, "example GitHub token must remain blank")

    gitignore = read(".gitignore")
    for marker in ("server_data/*", ".env", "*.sqlite3"):
        require(marker in gitignore, f"Git ignore is missing {marker}")

    dockerignore = read(".dockerignore")
    for marker in (".git", ".env", "server_data", "*.sqlite3"):
        require(marker in dockerignore, f"Docker ignore is missing {marker}")

    dockerfile = read("deploy/content-studio/Dockerfile")
    for marker in (
        "FROM python:3.12-slim",
        "MEMORY_PALACE_ENV=production",
        "MEMORY_PALACE_ADMIN_ENABLED=false",
        "MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED=false",
        "MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED=false",
        "MEMORY_PALACE_GITHUB_ALLOW_MERGE=false",
        "USER app",
        "HEALTHCHECK",
        "backend.main:app",
    ):
        require(marker in dockerfile, f"deployment container is missing {marker}")

    pages_builder = read("scripts/build_github_pages.py")
    require('ROOT / "frontend" / "css"' in pages_builder, "GitHub Pages builder must explicitly copy student CSS")
    require('ROOT / "frontend" / "js"' in pages_builder, "GitHub Pages builder must explicitly copy student JavaScript")
    require('frontend" / "admin' not in pages_builder, "GitHub Pages builder must not copy the admin frontend")

    main_py = read("backend/main.py")
    require('docs_url=None' in main_py and 'openapi_url=None' in main_py, "production API documentation endpoints must stay disabled")
    require('@app.get("/api/health")' in main_py, "deployment health endpoint is missing")
    require('@app.post("/api/admin/login")' in main_py, "admin login endpoint is missing")
    require('@app.get("/api/admin/session")' in main_py, "admin session endpoint is missing")
    require('@app.post("/api/admin/logout")' in main_py, "admin logout endpoint is missing")

    deployment = read("deploy/content-studio/README.md")
    for phrase in (
        "persistent",
        "/app/server_data",
        "HTTPS",
        "generate_admin_credentials.py",
        "MEMORY_PALACE_GITHUB_ALLOW_MERGE=false",
        "rollback",
        "GitHub Pages",
    ):
        require(phrase in deployment, f"deployment runbook is missing {phrase}")

    smoke = read("scripts/smoke_content_studio.py")
    require("Refusing non-HTTPS Content Studio URL" in smoke, "smoke test must reject remote HTTP")
    require("X-CSRF-Token" in smoke, "smoke test must verify CSRF-protected logout")
    require("/api/admin/catalog/summary" in smoke, "smoke test must verify authenticated catalog access")
    require("/api/admin/publication/status" in smoke, "smoke test must inspect the publication gate")

    print("CONTENT STUDIO INTEGRATION QA PASS")
    print("- prior Steps 1-9 QA present")
    print("- administrative and publication gates default off")
    print("- private state and secrets excluded from repository/container context")
    print("- production container runs as a non-root user")
    print("- GitHub Pages remains student-only")
    print("- deployment smoke test verifies HTTPS, auth, catalog, publication gate, CSRF, and logout")


if __name__ == "__main__":
    main()
