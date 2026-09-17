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
    require('import { learnView } from "/static/js/views/learn.js"' in frontend, "preview does not reuse the student learn renderer")
    require('import { reviewView } from "/static/js/views/review.js"' in frontend, "preview does not reuse the student review renderer")
    require('import { practiceView } from "/static/js/views/practice.js"' in frontend, "preview does not reuse the student practice renderer")
    require('sandbox=""' in frontend, "student preview iframe is not script-sandboxed")
    require("Published baseline" in frontend and "Working copy" in frontend, "published-versus-draft preview controls are missing")
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

    print("STEP8 QUALITY QA PASS")
    print("- draft-aware student preview model")
    print("- real student learn/review/practice renderers")
    print("- responsive reference viewports")
    print("- structural, coverage, retrieval, continuity, readability, density, and accessibility checks")
    print("- published student runtime remains isolated from Content Studio")


if __name__ == "__main__":
    main()
