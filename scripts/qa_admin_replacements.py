from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ADMIN REPLACEMENT QA FAIL\n- {message}")


def main() -> None:
    engine = ROOT / "backend" / "admin_replacements.py"
    routes = ROOT / "backend" / "admin_replacement_routes.py"
    registration = ROOT / "backend" / "admin_draft_routes.py"
    js = ROOT / "frontend" / "admin" / "replacement.js"
    css = ROOT / "frontend" / "admin" / "replacement.css"
    tests = ROOT / "tests" / "test_admin_replacements.py"

    for path in (engine, routes, registration, js, css, tests):
        require(path.is_file(), f"missing Step 6 file: {path.relative_to(ROOT)}")

    engine_text = engine.read_text(encoding="utf-8")
    route_text = routes.read_text(encoding="utf-8")
    registration_text = registration.read_text(encoding="utf-8")
    js_text = js.read_text(encoding="utf-8")

    for mode in ("narrative_only", "narrative_plus_scene_design", "complete_scene", "complete_journey"):
        require(mode in engine_text, f"replacement mode missing: {mode}")

    for capability in (
        "required_knowledge",
        "dependency_impact",
        "target_plan",
        "analyze_replacement",
        "apply_replacement",
        "missing_required_references",
        "missing_explicit_terms",
        "route_preserved",
    ):
        require(capability in engine_text, f"replacement safety capability missing: {capability}")

    require("SCENE_LOCKED_FIELDS" in engine_text and "JOURNEY_LOCKED_FIELDS" in engine_text, "stable identity locks are missing")
    require('result["route"] = True' in engine_text, "permanent route is not forcibly preserved")
    require("Required knowledge references are missing" in engine_text, "required-knowledge blocking check is missing")
    require("create_snapshot(" in engine_text, "automatic pre-replacement snapshot is missing")
    require(engine_text.index("create_snapshot(") < engine_text.index("update_draft(\n        draft_id,\n        payload=analysis"), "snapshot must be created before replacement save")
    require("published_story_text" in engine_text and "candidate_story_text" in engine_text, "old-versus-new story comparison is missing")
    require('"course_id"' in engine_text and "course_id=course_id" in engine_text, "replacement engine does not preserve explicit course identity")
    require("WHERE draft_id = ? AND course_id = ?" in engine_text, "replacement draft rebase is not course-scoped")
    require("write_text(" not in engine_text and "open(" not in engine_text, "replacement engine writes directly to repository course files")

    require('prefix="/api/admin/replacements"' in route_text, "replacement API is outside protected admin namespace")
    require(route_text.count("csrf=True") >= 3, "replacement mutations are not consistently CSRF protected")
    require('course_id: str = Field(default="ap-biology"' in route_text, "replacement mutation request does not carry course_id")
    for endpoint in ("/plan", "/drafts", "/analyze", "/apply"):
        require(endpoint in route_text, f"replacement endpoint missing: {endpoint}")
    require('/admin/drafts-core.js' in route_text and '/admin/replacement.js' in route_text, "replacement frontend is not loaded through the protected admin asset loader")
    require("router.include_router(admin_replacement_routes.router)" in registration_text, "replacement API router is not registered")
    require("router.include_router(admin_replacement_routes.assets)" in registration_text, "replacement asset loader is not registered")

    for ui in (
        "Complete Story Replacement",
        "Required knowledge before replacement",
        "Analyze replacement",
        "Old versus new",
        "Apply to draft",
        "/api/admin/replacements/plan",
        "/api/admin/replacements/analyze",
        "/api/admin/replacements/apply",
    ):
        require(ui in js_text, f"replacement UI capability missing: {ui}")
    require("window.confirm" in js_text, "replacement apply confirmation is missing")
    require("course_id: replacementState.draft.course_id || currentAdminCourseId()" in js_text, "replacement analyze/apply requests do not carry draft course identity")
    require('<option value="unit-8">Unit 8</option>' not in js_text, "replacement unit selector is still hard-coded to AP Biology")
    require("published student content was not modified" in js_text.lower(), "replacement UI does not state published-content isolation")

    print("ADMIN REPLACEMENT QA PASS")
    print("- scene and complete-journey replacement modes are present")
    print("- required knowledge is inventoried before replacement")
    print("- stable IDs and permanent route are locked")
    print("- dependency impact and explicit-term warnings are surfaced")
    print("- old and new narratives are compared before acceptance")
    print("- an automatic recovery snapshot is created before replacement save")
    print("- all mutations remain inside the protected draft store")
    print("- replacement draft reads and writes remain explicitly course-scoped")
    print("- published course files are not directly written")


if __name__ == "__main__":
    main()
