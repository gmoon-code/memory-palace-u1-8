from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend import admin_quality


ADMIN_DIR = ROOT / "frontend" / "admin"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"STEP8 QUALITY QA FAIL\n- {message}")


def main() -> None:
    required_files = [
        ROOT / "backend" / "admin_quality.py",
        ROOT / "backend" / "admin_quality_routes.py",
        ADMIN_DIR / "quality.js",
        ADMIN_DIR / "quality.css",
        ROOT / "tests" / "test_admin_quality.py",
        ROOT / "docs" / "admin" / "STEP8_PREVIEW_AND_QUALITY.md",
    ]
    for path in required_files:
        require(path.is_file(), f"missing {path.relative_to(ROOT)}")

    routes = (ROOT / "backend" / "admin_quality_routes.py").read_text(encoding="utf-8")
    quality = (ROOT / "backend" / "admin_quality.py").read_text(encoding="utf-8")
    frontend = (ADMIN_DIR / "quality.js").read_text(encoding="utf-8")
    drafts = (ADMIN_DIR / "drafts.js").read_text(encoding="utf-8")
    builder = (ROOT / "scripts" / "build_github_pages.py").read_text(encoding="utf-8")

    require('prefix="/api/admin/quality"' in routes, "quality API namespace is missing")
    require('@router.get("/preview")' in routes, "draft-aware preview endpoint is missing")
    require('@router.get("/report")' in routes, "quality report endpoint is missing")
    require('@router.get("/entity")' in routes, "entity quality endpoint is missing")
    require("DEVICE_PRESETS" in quality and '"phone"' in quality and '"desktop"' in quality, "responsive device presets are incomplete")
    require("scene-required-reference-reduced" in quality, "draft scientific-reference loss check is missing")
    require("scene-next-locus-review" in quality, "narrative continuity check is missing")
    require("scene-screen-density-high" in quality, "screen-density check is missing")
    require("scene-sentence-density" in quality, "readability check is missing")
    require("media-alt-text-missing" in quality and "media-transcript-missing" in quality, "media accessibility checks are missing")
    require("review-timeline-gap" in quality, "retrieval coverage check is missing")
    require("course_packages.journey(course_id" in quality, "quality preview does not use the selected course package")
    require("admin_catalog.catalog(course_id)" in quality, "quality report catalog reads are not course-scoped")
    require("admin_catalog.content_health(course_id)" in quality, "quality report health checks are not course-scoped")
    require("admin_management._active_draft_rows(course_id)" in quality, "quality draft findings are not course-scoped")
    require("course_id=course_id" in quality, "quality draft/media operations do not preserve course identity")
    require("range(1, 9)" not in quality, "quality still assumes eight AP Biology units")
    require("content.journey_by_id" not in quality, "quality still depends on the AP Biology-only journey loader")
    require('import { learnView } from "/static/js/views/learn.js"' in frontend, "preview does not reuse the student learn renderer")
    require('import { reviewView } from "/static/js/views/review.js"' in frontend, "preview does not reuse the student review renderer")
    require('import { practiceView } from "/static/js/views/practice.js"' in frontend, "preview does not reuse the student practice renderer")
    require('sandbox=""' in frontend, "student preview iframe is not script-sandboxed")
    require("Published baseline" in frontend and "Working copy" in frontend, "published-versus-draft preview controls are missing")
    require("currentAdminCourseCatalogReady()" in frontend, "read-only catalog-ready courses cannot inspect quality workspaces")
    require("qualityModes.has(mode) && currentAdminCourseCatalogReady()" in frontend, "quality workspace access is still tied to editability")
    require("course_id: currentAdminCourseId()" in frontend, "quality frontend does not send selected course identity")
    require("qualityState.units" in frontend and "story-method-course-changed" in frontend, "quality unit choices are not course-driven")
    require("for (let index = 1; index <= 8; index += 1)" not in frontend, "quality unit selector is still hard-coded to eight units")
    require("AP Biology unit" not in frontend, "quality preview still labels every course as AP Biology")
    require("preview-device-button" in frontend, "responsive preview controls are missing")
    require('import "./quality.js";' in drafts, "Step 8 workspace is not loaded by Content Studio")
    require("frontend/admin" not in builder, "public GitHub Pages builder unexpectedly references admin assets")

    preview = admin_quality.build_preview(
        "scene:unit-8:U8-J1:0",
        source="published",
    )
    require(preview["model"]["renderer"] == "learn", "published scene preview did not produce the student learn model")
    require(preview["source_state"] == "published", "published preview source state is incorrect")
    require(bool(preview["model"]["journey"].get("scenes")), "student preview journey contains no scenes")
    require(preview["device_presets"]["phone"]["width"] == 390, "phone reference viewport changed unexpectedly")

    entity_quality = admin_quality.entity_quality(
        "scene:unit-8:U8-J1:0",
        source="published",
    )
    require(entity_quality["schema"] == admin_quality.QUALITY_SCHEMA, "entity quality schema is incorrect")
    require(set(["error_count", "warning_count", "advisory_count"]).issubset(entity_quality), "entity quality counts are incomplete")

    chemistry_preview = admin_quality.build_preview(
        "unit:unit-1",
        source="published",
        course_id="ap-chemistry",
    )
    require(chemistry_preview["course_id"] == "ap-chemistry", "Chemistry preview lost course identity")
    require(chemistry_preview["course_title"] == "AP Chemistry", "Chemistry preview title is not course-scoped")
    require(chemistry_preview["model"]["renderer"] == "unit", "Chemistry F1 unit preview did not use unit renderer")
    require(
        chemistry_preview["model"]["record"].get("title") == "Atomic Structure and Properties",
        "Chemistry F1 unit preview loaded the wrong package unit",
    )

    chemistry_report = admin_quality.quality_report(
        course_id="ap-chemistry",
        unit_id="unit-1",
    )
    require(chemistry_report["scope"]["course_id"] == "ap-chemistry", "Chemistry quality report lost course scope")
    require(
        all(item.get("unit_id") in {None, "unit-1"} for item in chemistry_report["findings"]),
        "Chemistry unit quality report leaked findings from another unit",
    )

    print("STEP8 QUALITY QA PASS")
    print("- draft-aware student preview model")
    print("- real student learn/review/practice renderers")
    print("- responsive reference viewports")
    print("- structural, coverage, retrieval, continuity, readability, density, and accessibility checks")
    print("- preview, health, drafts, media, and package journey reads are explicitly course-scoped")
    print("- read-only catalog-ready courses can be inspected without enabling writes")
    print("- published student runtime remains isolated from Content Studio")


if __name__ == "__main__":
    main()
