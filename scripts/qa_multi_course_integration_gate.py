from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend import admin_catalog, course_packages


REGISTRY = ROOT / "platform" / "courses.json"
MULTI_COURSE_MODULES = (
    "backend/admin_drafts.py",
    "backend/admin_editors.py",
    "backend/admin_replacements.py",
    "backend/admin_management.py",
    "backend/admin_quality.py",
    "backend/admin_publication.py",
    "frontend/admin/editor.js",
    "frontend/admin/replacement.js",
    "frontend/admin/management.js",
    "frontend/admin/quality.js",
    "frontend/admin/publication.js",
    "frontend/admin/workflow.js",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"MULTI-COURSE INTEGRATION GATE FAIL\n- {message}")


def read(relative: str) -> str:
    path = ROOT / relative
    require(path.is_file(), f"missing required file: {relative}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    records = {
        str(item.get("course_id")): item
        for item in registry.get("courses", [])
        if isinstance(item, dict) and item.get("course_id")
    }

    biology = records.get("ap-biology")
    chemistry = records.get("ap-chemistry")
    require(biology is not None, "AP Biology is missing from the course registry")
    require(chemistry is not None, "AP Chemistry development package is missing from the course registry")
    require(biology.get("status") == "available", "AP Biology must remain available")
    require(biology.get("student_visible") is True, "AP Biology must remain student-visible")
    require(chemistry.get("status") == "development", "AP Chemistry development package must remain development-only")
    require(chemistry.get("student_visible") is False, "AP Chemistry development package must remain hidden from students")

    admin_catalog.clear_catalog_cache()
    course_packages.package_manifest.cache_clear()

    access = {item["course_id"]: item for item in admin_catalog.catalog_courses()["courses"]}
    require(access["ap-biology"]["catalog_ready"] is True, "AP Biology catalog must remain ready")
    require(access["ap-biology"]["editable"] is True, "AP Biology editing must remain enabled")
    require(access["ap-chemistry"]["catalog_ready"] is True, "AP Chemistry development catalog must remain inspectable")
    require(access["ap-chemistry"]["editable"] is False, "AP Chemistry development package must remain read-only")

    try:
        admin_catalog.require_editable_course("ap-chemistry")
    except ValueError as exc:
        require("editing is not enabled" in str(exc), "AP Chemistry write block returned an unexpected error")
    else:
        raise SystemExit("MULTI-COURSE INTEGRATION GATE FAIL\n- AP Chemistry unexpectedly allows editing")

    for course_id in ("ap-biology", "ap-chemistry"):
        result = course_packages.validate_package(course_id)
        require(result["valid"], f"{course_id} package invalid: {'; '.join(result['errors'])}")
        manifest = course_packages.package_manifest(course_id)
        root = str(manifest.get("content_root") or "").rstrip("/")
        require(root == f"content/{course_id}", f"{course_id} content root is not course-local")
        for unit in manifest.get("units", []):
            unit_id = str(unit.get("unit_id") or "")
            unit_root = str(unit.get("content_root") or "").rstrip("/")
            require(unit_root.startswith(f"{root}/"), f"{course_id}/{unit_id} escapes the course content root")
            for source in course_packages.declared_unit_source_paths(course_id, unit_id):
                require(
                    source == unit_root or source.startswith(f"{unit_root}/"),
                    f"{course_id}/{unit_id} declares a source outside its unit root: {source}",
                )

    biology_u1 = course_packages.unit("ap-biology", "unit-1")
    chemistry_u1 = course_packages.unit("ap-chemistry", "unit-1")
    require(biology_u1 is not None and chemistry_u1 is not None, "course-local repeated unit-1 IDs are missing")
    require(
        biology_u1.get("title") != chemistry_u1.get("title"),
        "repeated unit IDs are not resolving through separate course packages",
    )

    pages = read("scripts/build_github_pages.py")
    require('item.get("student_visible") is not False' in pages, "Pages builder does not enforce student visibility")
    require('item.get("status") == "available"' in pages, "Pages builder does not enforce available course status")
    require('copy_tree(ROOT / "frontend" / "admin"' not in pages, "Pages builder must not copy administrator frontend")

    catalog = read("backend/admin_catalog.py")
    require("catalog_ready = bool(package_result.get(\"valid\"))" in catalog, "catalog_ready is not package-driven")
    require('editable = catalog_ready and record.get("status") == "available"' in catalog, "editing is not separated from catalog readiness")

    module_text = {path: read(path) for path in MULTI_COURSE_MODULES}
    for path, text in module_text.items():
        require("range(1, 9)" not in text, f"{path} still hard-codes an eight-unit loop")
        require('<option value="unit-8">Unit 8</option>' not in text, f"{path} still hard-codes Unit 8 UI options")

    require("WHERE course_id = ? AND entity_id = ? AND status = 'draft'" in module_text["backend/admin_management.py"], "management active draft lookup is not course-scoped")
    require("idx_media_assets_course_status" in module_text["backend/admin_management.py"], "media database is not course-indexed")
    require("ALTER TABLE media_assets ADD COLUMN course_id" in module_text["backend/admin_management.py"], "legacy media rows do not migrate to course identity")
    require("course_id TEXT NOT NULL DEFAULT 'ap-biology'" in module_text["backend/admin_drafts.py"], "legacy draft migration no longer preserves AP Biology compatibility")
    require("publication_candidates ADD COLUMN course_id" in module_text["backend/admin_publication.py"], "publication candidate migration is not course-scoped")
    require("publication_releases ADD COLUMN course_id" in module_text["backend/admin_publication.py"], "publication release migration is not course-scoped")

    for frontend in (
        "frontend/admin/editor.js",
        "frontend/admin/replacement.js",
        "frontend/admin/management.js",
        "frontend/admin/quality.js",
        "frontend/admin/publication.js",
    ):
        require("currentAdminCourse" in module_text[frontend], f"{frontend} does not derive selected course context")

    management = module_text["frontend/admin/management.js"]
    require("currentAdminCourseCatalogReady()" in management, "management preview access does not use catalog readiness")
    require("currentAdminCourseEditable()" in management, "management write controls do not use editable access")
    quality = module_text["frontend/admin/quality.js"]
    require("currentAdminCourseCatalogReady()" in quality, "quality preview access does not use catalog readiness")
    publication = module_text["frontend/admin/publication.js"]
    require("course_id=" in publication and "currentAdminCourseId()" in publication, "publication inspection requests are not course-scoped")
    require("currentAdminCourseEditable()" in publication, "publication write controls do not use editable access")
    require("status.course_editable" in publication, "publication status does not expose the selected course write gate")

    tests = "\n".join(
        read(path)
        for path in (
            "tests/test_admin_multi_course_foundation.py",
            "tests/test_admin_editors.py",
            "tests/test_admin_replacements.py",
            "tests/test_admin_management.py",
            "tests/test_admin_quality.py",
            "tests/test_admin_publication.py",
        )
    )
    for marker in (
        "ap-chemistry",
        "duplicate",
        "wrong_course",
        "editing is not enabled",
        "course_id",
    ):
        require(marker in tests, f"multi-course regression tests are missing coverage marker: {marker}")

    integration = read("scripts/qa_content_studio_integration.py")
    require("MEMORY_PALACE_ADMIN_ENABLED=false" in integration, "integration gate no longer checks admin-off default")
    require("MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED=false" in integration, "integration gate no longer checks publication-off default")
    require("MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED=false" in integration, "integration gate no longer checks GitHub publication-off default")
    require("MEMORY_PALACE_GITHUB_ALLOW_MERGE=false" in integration, "integration gate no longer checks merge-off default")

    print("MULTI-COURSE INTEGRATION GATE PASS")
    print("- AP Biology remains the editable student-visible production course")
    print("- AP Chemistry remains a hidden catalog-ready read-only development package")
    print("- package roots and declared source files remain course- and unit-scoped")
    print("- drafts, media, quality, management, and publication retain explicit course boundaries")
    print("- catalog-ready inspection remains separate from editable write access")
    print("- public Pages output still selects only available student-visible courses")
    print("- legacy AP Biology rows retain backward-compatible course migration defaults")
    print("- cross-course regression coverage remains present across every protected admin subsystem")


if __name__ == "__main__":
    main()
