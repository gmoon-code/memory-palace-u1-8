from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend import admin_catalog, content, course_packages

COURSE_ID = "ap-chemistry"
EXPECTED_TITLES = ['Atomic Structure and Properties','Compound Structure and Properties','Properties of Substances and Mixtures','Chemical Reactions','Kinetics','Thermochemistry','Equilibrium','Acids and Bases','Thermodynamics and Electrochemistry']
EXPECTED_TOPIC_COUNTS = [8, 7, 13, 9, 11, 9, 12, 11, 11]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"AP CHEMISTRY DEVELOPMENT PACKAGE QA FAIL\n- {message}")


def main() -> None:
    course_packages.clear_package_cache()
    admin_catalog.clear_catalog_cache()
    registry = content.course_registry()
    record = next((item for item in registry["courses"] if item.get("course_id") == COURSE_ID), None)
    require(record is not None, "AP Chemistry is not registered")
    require(record.get("status") == "development", "AP Chemistry must remain development-only")
    require(record.get("student_visible") is False, "AP Chemistry must remain hidden from students")
    require(record.get("unit_count") == 9, "registry must expose nine AP Chemistry units")

    result = course_packages.validate_package(COURSE_ID)
    require(result["valid"], "; ".join(result["errors"]))
    require(result["unit_count"] == 9, "package manifest must expose nine units")

    course = course_packages.course(COURSE_ID)
    require(course.get("status") == "PACKAGE_FOUNDATION", "course status is not PACKAGE_FOUNDATION")
    require(course.get("production_phase") == "F1_PACKAGE_FOUNDATION", "course production phase is not F1")
    units = course.get("units", [])
    require(len(units) == 9, "course metadata must expose nine units")
    require([u.get("title") for u in units] == EXPECTED_TITLES, "CED unit titles or order changed")
    require([u.get("topic_count") for u in units] == EXPECTED_TOPIC_COUNTS, "CED topic counts changed")
    require(sum(u.get("topic_count", 0) for u in units) == 91, "course scaffold must contain 91 topics")

    for unit in units:
        unit_id = unit["unit_id"]
        packaged = course_packages.unit_package(COURSE_ID, unit_id)
        require(packaged.get("title") == unit.get("title"), f"{unit_id} package title differs from course metadata")
        registry_payload = course_packages.journeys(COURSE_ID, unit_id)
        require(registry_payload["guided_journeys"] == [], f"{unit_id} must have no production journeys in F1")
        require(unit.get("journey_count") == 0 and unit.get("scene_count") == 0, f"{unit_id} incorrectly reports produced narrative content")
        require(course_packages.artifact_records(COURSE_ID, unit_id, "concepts") == [], f"{unit_id} concepts must remain empty in F1")
        require(course_packages.memory_objects(COURSE_ID, unit_id) == [], f"{unit_id} Memory Objects must remain empty in F1")
        require(course_packages.review_manifest(COURSE_ID, unit_id).get("targets") == [], f"{unit_id} review must remain empty in F1")
        require(course_packages.mixed_discrimination(COURSE_ID, unit_id).get("sets") == [], f"{unit_id} mixed discrimination must remain empty in F1")
        require(course_packages.application_lab(COURSE_ID, unit_id).get("items") == [], f"{unit_id} Challenge Lab must remain empty in F1")
        declared = course_packages.declared_unit_source_paths(COURSE_ID, unit_id)
        require(len(declared) == 6, f"{unit_id} must declare exactly six foundation runtime source files")
        require(all(path.startswith(f"content/ap-chemistry/{unit_id}/") for path in declared), f"{unit_id} source path escaped its course/unit namespace")

    require(not (ROOT / "content/ap-chemistry/unit-1/journeys/APCHEM-U1-J1.json").exists(), "Unit 1 fixture journey still exists")
    require(not (ROOT / "content/ap-chemistry/unit-2/journeys/APCHEM-U2-J1.json").exists(), "Unit 2 fixture journey still exists")

    access = next(item for item in admin_catalog.catalog_courses()["courses"] if item["course_id"] == COURSE_ID)
    require(access["catalog_ready"] is True, "AP Chemistry package foundation is not catalog-ready")
    require(access["editable"] is False, "AP Chemistry package foundation unexpectedly became editable")
    require(access["catalog_mode"] == "read_only", "AP Chemistry package foundation is not read-only")

    summary = admin_catalog.catalog_summary(COURSE_ID)
    require(summary["counts"].get("unit") == 9, "catalog does not expose nine units")
    for key in ("journey", "scene", "concept", "memory_object", "question", "challenge"):
        require(summary["counts"].get(key, 0) == 0, f"F1 unexpectedly produced {key} entities")
    require(summary["unresolved_reference_count"] == 0, "foundation catalog has unresolved references")

    print("AP CHEMISTRY DEVELOPMENT PACKAGE QA PASS")
    print("- nine CED units and all 91 topic boundaries are loaded")
    print("- all production content collections remain intentionally empty at F1")
    print("- architecture fixture journeys are retired from the live content tree")
    print("- package source paths remain course- and unit-scoped")
    print("- AP Chemistry remains catalog-ready, read-only, development-only, and student-hidden")


if __name__ == "__main__":
    main()
