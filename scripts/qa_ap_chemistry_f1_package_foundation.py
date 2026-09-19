from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend import admin_catalog, course_packages

FOUNDATION = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F1_PACKAGE_FOUNDATION.json"
CROSSWALK = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0B_FRAMEWORK_CROSSWALK.json"
F0D = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0D_READINESS_GATE.json"
COURSE = ROOT / "content" / "ap-chemistry" / "course.json"
REGISTRY = ROOT / "platform" / "courses.json"

EXPECTED_TITLES = ['Atomic Structure and Properties','Compound Structure and Properties','Properties of Substances and Mixtures','Chemical Reactions','Kinetics','Thermochemistry','Equilibrium','Acids and Bases','Thermodynamics and Electrochemistry']
EXPECTED_COUNTS = [8, 7, 13, 9, 11, 9, 12, 11, 11]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"AP CHEMISTRY F1 PACKAGE FOUNDATION FAIL\n- {message}")


def main() -> None:
    for path in (FOUNDATION, CROSSWALK, F0D, COURSE, REGISTRY):
        require(path.is_file(), f"missing F1 dependency: {path.relative_to(ROOT)}")
    foundation = json.loads(FOUNDATION.read_text(encoding="utf-8"))
    crosswalk = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    f0d = json.loads(F0D.read_text(encoding="utf-8"))
    course = json.loads(COURSE.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    require(foundation.get("schema") == "story-method-ap-chemistry-f1-package-foundation-1.0", "unexpected F1 schema")
    require(foundation.get("status") == "COMPLETE", "F1 is not complete")
    require(f0d.get("result") == "COMPLETE", "F1 cannot exist before completed F0D")
    require(course.get("status") == "PACKAGE_FOUNDATION", "course is not in package-foundation state")
    require(course.get("production_phase") == "F1_PACKAGE_FOUNDATION", "course production phase changed")

    units = course.get("units") or []
    require(len(units) == 9, "F1 course must have nine units")
    require([u.get("title") for u in units] == EXPECTED_TITLES, "F1 unit titles/order changed")
    require([u.get("topic_count") for u in units] == EXPECTED_COUNTS, "F1 topic counts changed")

    cross_by_unit = {f"unit-{n}": [] for n in range(1, 10)}
    for record in crosswalk.get("ced_topics") or []:
        cross_by_unit[record["unit_id"]].append((record["topic_id"], record["title"]))
    for unit in units:
        unit_id = unit["unit_id"]
        actual = [(item["topic_id"], item["title"]) for item in unit.get("topics") or []]
        require(actual == cross_by_unit[unit_id], f"{unit_id} topic scaffold diverges from F0B")
        require(unit.get("journey_count") == 0 and unit.get("scene_count") == 0, f"{unit_id} contains narrative content before F2")

    course_packages.clear_package_cache()
    package = course_packages.package_manifest("ap-chemistry")
    require([u["unit_id"] for u in package["units"]] == [f"unit-{n}" for n in range(1, 10)], "package unit IDs are not 1-9")
    require([u["title"] for u in package["units"]] == EXPECTED_TITLES, "package titles diverge from CED lock")
    require(course_packages.validate_package("ap-chemistry")["valid"] is True, "nine-unit package does not validate")

    chemistry = next(item for item in registry["courses"] if item["course_id"] == "ap-chemistry")
    require(chemistry.get("unit_count") == 9, "registry unit_count is not 9")
    require(chemistry.get("status") == "development", "AP Chemistry left development state")
    require(chemistry.get("student_visible") is False, "AP Chemistry became student-visible")

    admin_catalog.clear_catalog_cache()
    access = next(item for item in admin_catalog.catalog_courses()["courses"] if item["course_id"] == "ap-chemistry")
    require(access.get("catalog_ready") is True, "F1 package is not inspectable")
    require(access.get("editable") is False, "F1 package became editable")

    content_text = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "content" / "ap-chemistry").rglob("*.json"))
    for retired in ("APCHEM-U1-J1", "APCHEM-U2-J1", "Atomic Records Hall", "Molecular and Ionic Compound Structure and Properties"):
        require(retired not in content_text, f"retired fixture material leaked into real package foundation: {retired}")

    runtime_totals = foundation.get("foundation_contract") or {}
    for key in ("production_journeys","production_scenes","production_concepts","production_memory_objects","production_review_targets","production_mixed_sets","production_challenge_items"):
        require(runtime_totals.get(key) == 0, f"F1 must not claim produced content: {key}")

    print("AP CHEMISTRY F1 PACKAGE FOUNDATION PASS")
    print("- architecture fixture has graduated into the real nine-unit development package")
    print("- all 91 CED topic IDs and titles exactly match the F0B crosswalk")
    print("- package-declared runtime scaffolds exist for every unit and remain empty")
    print("- retired fixture journeys and old Unit 2 title are absent from the active content tree")
    print("- AP Chemistry remains development-only, student-hidden, catalog-ready, and read-only")
    print("- F2 Unit 1 scientific catalog and journey architecture is the next authorized phase")


if __name__ == "__main__":
    main()
