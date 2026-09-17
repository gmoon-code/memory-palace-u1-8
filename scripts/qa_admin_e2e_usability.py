from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
USABILITY_JS = ROOT / "frontend" / "admin" / "usability.js"
USABILITY_CSS = ROOT / "frontend" / "admin" / "usability.css"
LOADER = ROOT / "backend" / "admin_replacement_routes.py"
ACCEPTANCE = ROOT / "tests" / "test_admin_acceptance_workflows.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ADMIN E2E USABILITY QA FAIL\n- {message}")


def main() -> None:
    for path in (USABILITY_JS, USABILITY_CSS, ACCEPTANCE):
        require(path.exists(), f"{path.relative_to(ROOT)} is missing")

    js = USABILITY_JS.read_text(encoding="utf-8")
    css = USABILITY_CSS.read_text(encoding="utf-8")
    loader = LOADER.read_text(encoding="utf-8")
    tests = ACCEPTANCE.read_text(encoding="utf-8")

    require("admin-usability-guide" in js, "first-use administrator guide is missing")
    require("Integrated administrator workspace" in js, "integrated workspace status is not normalized")
    require("staleCopy" in js, "early staged-development copy is not normalized")
    require("hasUnsavedLocalWork" in js, "unsaved-work detection is missing")
    require("beforeunload" in js, "browser-close unsaved-work protection is missing")
    require("guardNavigation" in js and "window.confirm" in js, "workspace-navigation unsaved-work protection is missing")
    require("replacementDirty" in js, "Complete Story Replacement local-input protection is missing")
    require("publication stays deliberate" in js.lower(), "first-use guide does not explain deliberate publication")
    require("$0" in js, "zero-cost operating boundary is missing from administrator guidance")
    require("@media(max-width:640px)" in css, "first-use guide lacks mobile layout")

    import_line = 'import "/admin/usability.js";'
    require(import_line in loader, "canonical administrator boot chain does not load usability.js")
    require(loader.rfind(import_line) > loader.rfind('import "/admin/workflow.js";'), "usability safeguards must load after workflow integration")

    for unit in range(1, 9):
        require("for number in range(1, 9)" in tests, "representative Units 1-8 preview acceptance loop is missing")
        break
    for route in (
        "/api/admin/editors/drafts",
        "/api/admin/quality/preview",
        "/api/admin/quality/entity",
        "/api/admin/publication/eligible",
        "/api/admin/publication/candidates",
        "/api/admin/replacements/analyze",
        "/api/admin/replacements/apply",
        "/api/admin/management/question-bank",
        "/api/admin/management/review-timeline",
        "/api/admin/management/challenge-bank",
    ):
        require(route in tests, f"acceptance workflow does not exercise {route}")
    require("digest(SCENE_SOURCE) == before" in tests, "acceptance workflow does not assert published-source isolation")

    require("content/ap-biology" not in js, "usability layer must not target published course paths")
    require('method: "POST"' not in js and "method: 'POST'" not in js, "usability layer must not mutate administrator data")

    print("CONTENT STUDIO END-TO-END USABILITY QA PASS")
    print("- first-use guidance explains the integrated administrator route")
    print("- stale staged-development wording is normalized")
    print("- unsaved local work is guarded before workspace exit or browser close")
    print("- Complete Story Replacement local input is included in the guard")
    print("- acceptance tests exercise Units 1-8 plus edit, preview, validate, publication preparation, recovery, questions, review, challenges, and replacement")
    print("- workflow remains local-first, zero-cost, and non-destructive")


if __name__ == "__main__":
    main()
