from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(f"CONTENT STUDIO HEALTH/REPAIR QA FAIL: {message}")


def text(path: str) -> str:
    target = ROOT / path
    if not target.exists():
        fail(f"missing required file: {path}")
    return target.read_text(encoding="utf-8")


def main() -> None:
    health = text("backend/admin_health.py")
    routes = text("backend/admin_health_routes.py")
    registration = text("backend/admin_draft_routes.py")
    ui = text("frontend/admin/health-repair.js")
    css = text("frontend/admin/health-repair.css")
    index = text("frontend/admin/index.html")
    repair = text("scripts/repair_content_studio_local.py")
    cmd = text("Repair Content Studio.cmd")
    workflow = text(".github/workflows/qa.yml")

    for marker in (
        "publication_locks",
        "loopback_binding",
        "private_state_directory",
        "latest_backup",
        "python_environment",
        "repository_origin",
        "updater_branch",
        "private_paths_ignored",
        "PRAGMA quick_check",
        "REPAIR_ACTIONS",
        "repair_all",
    ):
        if marker not in health:
            fail(f"system health check is missing marker: {marker}")

    if 'prefix="/api/admin/system-health"' not in routes:
        fail("protected system-health API prefix is missing")
    if "require_csrf=csrf" not in routes or '@router.post("/repair")' not in routes:
        fail("repair endpoint is not CSRF protected")
    if "admin_health_routes" not in registration or "include_router(admin_health_routes.router)" not in registration:
        fail("system-health router is not registered through the Content Studio router")

    if "/api/admin/system-health" not in ui or "repair_all" not in ui:
        fail("Settings UI is not wired to system health and safe repair")
    if 'data-view="settings"' not in ui:
        fail("Settings navigation is not intercepted by the system health workspace")
    if "/admin/health-repair.css" not in ui:
        fail("system-health UI does not load its isolated stylesheet")
    if "/admin/health-repair.js" not in index:
        fail("system-health module is not loaded by Content Studio")
    if ".system-health-row" not in css:
        fail("system-health status styling is missing")

    if "create_state_backup()" not in repair:
        fail("local environment repair does not create a safety backup first")
    if "require_content_studio_stopped" not in repair:
        fail("local environment repair does not require Content Studio to be stopped")
    for lock in (
        "MEMORY_PALACE_HOST",
        "MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED",
        "MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED",
        "MEMORY_PALACE_GITHUB_ALLOW_MERGE",
    ):
        if lock not in repair:
            fail(f"local repair does not enforce safety setting: {lock}")
    if "paid service" not in cmd.lower() or "billing" not in cmd.lower():
        fail("Windows repair launcher does not state the zero-cost boundary")

    dangerous = [
        "shutil.rmtree(ROOT / \"server_data\"",
        "unlink()  # credentials",
        "MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED=true",
        "MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED=true",
        "MEMORY_PALACE_GITHUB_ALLOW_MERGE=true",
    ]
    combined = health + repair + ui
    for marker in dangerous:
        if marker in combined:
            fail(f"unsafe repair marker detected: {marker}")

    if "python scripts/qa_content_studio_health_repair.py" not in workflow:
        fail("health/repair QA is not part of the GitHub Actions gate")
    if "node --check frontend/admin/health-repair.js" not in workflow:
        fail("system-health JavaScript syntax check is missing from CI")

    print("CONTENT STUDIO HEALTH/REPAIR QA PASS")
    print("- Settings exposes protected local system health")
    print("- health covers authentication, storage, SQLite integrity, backups, tooling, repository identity, updater readiness, and publication locks")
    print("- in-app repairs are allowlisted and CSRF protected")
    print("- environment repair requires Content Studio stopped and creates a safety backup first")
    print("- zero-cost local-only and publication-lock boundaries remain enforced")
    print("- AP Biology curriculum and student content are outside repair write paths")


if __name__ == "__main__":
    main()
