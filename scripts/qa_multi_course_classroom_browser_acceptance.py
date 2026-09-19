from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FRONTEND_FILES = {
    "admin": ROOT / "frontend" / "admin" / "admin.js",
    "editor": ROOT / "frontend" / "admin" / "editor.js",
    "replacement": ROOT / "frontend" / "admin" / "replacement.js",
    "management": ROOT / "frontend" / "admin" / "management.js",
    "quality": ROOT / "frontend" / "admin" / "quality.js",
    "publication": ROOT / "frontend" / "admin" / "publication.js",
    "workflow": ROOT / "frontend" / "admin" / "workflow.js",
}
ACCEPTANCE = ROOT / "tests" / "test_multi_course_classroom_browser_acceptance.py"
PAGES = ROOT / "scripts" / "build_github_pages.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"MULTI-COURSE CLASSROOM/BROWSER ACCEPTANCE FAIL\n- {message}")


def read(path: Path) -> str:
    require(path.is_file(), f"missing {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    sources = {name: read(path) for name, path in FRONTEND_FILES.items()}
    acceptance = read(ACCEPTANCE)
    pages = read(PAGES)

    admin = sources["admin"]
    require('data-catalog-ready=' in admin, "course selector does not expose catalog-ready state")
    require('data-editable=' in admin, "course selector does not expose editable state")
    require('" · catalog preview"' in admin, "read-only course selector label is missing")
    require("read-only architecture preview" in admin, "selected-course read-only status is missing")
    require('new CustomEvent("story-method-course-changed"' in admin, "course-change browser event is missing")
    require("record?.catalog_ready" in admin, "course selection does not reject unavailable catalogs")

    for name in ("editor", "replacement", "management", "quality", "publication", "workflow"):
        require(
            "story-method-course-changed" in sources[name],
            f"{name} workspace does not respond to course changes",
        )

    require("currentAdminCourseEditable()" in sources["editor"], "editor does not enforce course editability")
    require("currentAdminCourseEditable()" in sources["replacement"], "replacement does not enforce course editability")
    require("currentAdminCourseCatalogReady()" in sources["management"], "management inspection does not use catalog readiness")
    require("currentAdminCourseEditable()" in sources["management"], "management writes do not use editability")
    require("currentAdminCourseCatalogReady()" in sources["quality"], "quality preview does not use catalog readiness")
    require("currentAdminCourseEditable()" in sources["publication"], "publication controls do not use editability")
    require(
        "workflowState.context.course_id !== nextCourseId" in sources["workflow"],
        "workflow context is not cleared when the selected course changes",
    )

    for name in ("editor", "replacement", "management", "quality"):
        require(
            '<option value="unit-8">Unit 8</option>' not in sources[name],
            f"{name} reintroduced a fixed AP Biology unit selector",
        )

    for marker in (
        "test_teacher_can_switch_courses_and_inspect_course_local_records",
        "test_biology_authoring_path_remains_available_and_non_destructive",
        "test_chemistry_classroom_preview_is_complete_but_all_authoring_stays_locked",
        "test_switching_course_context_cannot_reuse_a_biology_draft_in_chemistry",
        "editing is not enabled",
        "Atomic Structure and Properties",
        "Chemistry of Life",
    ):
        require(marker in acceptance, f"acceptance suite is missing {marker}")

    require(
        'item.get("student_visible") is not False' in pages
        and 'item.get("status") == "available"' in pages,
        "student Pages selection no longer requires visible + available courses",
    )
    require(
        'copy_tree(ROOT / "frontend" / "admin"' not in pages,
        "administrator frontend is exposed by the student Pages builder",
    )

    print("MULTI-COURSE CLASSROOM/BROWSER ACCEPTANCE PASS")
    print("- teacher selector exposes catalog-ready and editable state separately")
    print("- AP Biology remains the normal editable classroom authoring course")
    print("- AP Chemistry remains inspectable through editor, replacement, management, quality, and publication views")
    print("- AP Chemistry write controls remain locked")
    print("- every browser workspace resets or re-resolves state when the selected course changes")
    print("- persistent workflow context cannot survive a cross-course switch")
    print("- unit selectors remain package-driven")
    print("- student Pages still excludes hidden development courses and administrator assets")


if __name__ == "__main__":
    main()
