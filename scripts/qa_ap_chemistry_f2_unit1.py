from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend import admin_catalog, course_packages

CATALOG = ROOT / "content" / "ap-chemistry" / "unit-1" / "source" / "scientific-catalog.json"
ARCH = ROOT / "content" / "ap-chemistry" / "unit-1" / "source" / "journey-architecture.json"
CONCEPTS = ROOT / "content" / "ap-chemistry" / "unit-1" / "concepts.json"
COURSE = ROOT / "content" / "ap-chemistry" / "course.json"
F2 = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F2_UNIT1.json"
REGISTRY = ROOT / "platform" / "courses.json"
EXPECTED_TOPICS = [f"1.{n}" for n in range(1, 9)]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"AP CHEMISTRY F2 UNIT 1 FAIL\n- {message}")


def main() -> None:
    for path in (CATALOG, ARCH, CONCEPTS, COURSE, F2, REGISTRY):
        require(path.is_file(), f"missing F2 artifact: {path.relative_to(ROOT)}")

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    arch = json.loads(ARCH.read_text(encoding="utf-8"))
    concepts = json.loads(CONCEPTS.read_text(encoding="utf-8"))
    course = json.loads(COURSE.read_text(encoding="utf-8"))
    f2 = json.loads(F2.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    require(catalog.get("schema") == "story-method-ap-chemistry-scientific-catalog-1.0", "unexpected scientific catalog schema")
    require(catalog.get("status") == "SCIENTIFIC_CATALOG_LOCKED", "scientific catalog is not locked")
    require(catalog.get("record_count") == 48, "Unit 1 must contain 48 locked scientific records")
    records = catalog.get("concepts") or []
    require(len(records) == 48, "scientific record count does not match")
    ids = [r.get("knowledge_id") for r in records]
    require(len(ids) == len(set(ids)) == 48, "scientific record IDs are missing or duplicated")
    require(catalog.get("ced_topic_order") == EXPECTED_TOPICS, "catalog CED topic order changed")
    require(set(r.get("topic") for r in records) == set(EXPECTED_TOPICS), "one or more CED topics has no scientific record")
    require(all(r.get("canonical_lock") == "SOURCE_BACKED_LOCK" for r in records), "one or more scientific records is not source locked")
    require(all(r.get("source_reference") for r in records), "one or more scientific records lacks source trace")
    require(all(r.get("canonical_verified_statement") for r in records), "one or more scientific records lacks canonical science")

    guard_labels = {r["canonical_label"] for r in records if r.get("scope_class") == "AP_SCOPE_GUARD"}
    require({"Mass-spectrum scope guard", "Quantum-number exclusion", "Aufbau-exception scope guard"} <= guard_labels, "required AP scope guards are missing")

    require(concepts.get("concept_count") == 48, "runtime concept count is not 48")
    require(concepts.get("concepts") == records, "runtime concepts diverge from the locked source catalog")

    require(arch.get("schema") == "story-method-ap-chemistry-journey-architecture-1.0", "unexpected journey architecture schema")
    require(arch.get("status") == "ARCHITECTURE_LOCKED_NARRATIVE_NOT_AUTHORED", "journey architecture status changed")
    journeys = arch.get("journeys") or []
    require(len(journeys) == 4, "F2 must plan four Unit 1 journeys")
    require(sum(len(j.get("loci") or []) for j in journeys) == 20, "F2 must plan twenty Unit 1 loci")
    flattened_topics = []
    for journey in journeys:
        flattened_topics.extend(journey.get("ced_topics") or [])
        for locus in journey.get("loci") or []:
            for record_id in locus.get("required_record_ids") or []:
                require(record_id in ids, f"journey architecture references unknown scientific record: {record_id}")
    require(flattened_topics == EXPECTED_TOPICS, "journey plans do not preserve exact CED topic order")
    assigned = [record_id for j in journeys for locus in j.get("loci") or [] for record_id in locus.get("required_record_ids") or []]
    require(len(assigned) == len(set(assigned)) == 48, "scientific records are not assigned exactly once across F2 loci")
    require(set(assigned) == set(ids), "journey architecture does not cover every scientific record")
    require(arch.get("coverage_check", {}).get("narrative_authored") is False, "F2 incorrectly claims narrative authoring")
    require(arch.get("coverage_check", {}).get("memory_objects_authored") is False, "F2 incorrectly claims Memory Object authoring")

    u1 = next(u for u in course["units"] if u["unit_id"] == "unit-1")
    require(course.get("production_phase") == "F2_UNIT1_SCIENTIFIC_CATALOG_AND_JOURNEY_ARCHITECTURE", "course production phase is not F2")
    require(u1.get("status") == "SCIENTIFIC_CATALOG_LOCKED", "Unit 1 status is not F2 locked")
    require(u1.get("canonical_records") == 48, "course metadata does not report 48 Unit 1 records")
    require(u1.get("planned_journey_count") == 4 and u1.get("planned_locus_count") == 20, "course metadata does not report F2 architecture")
    require(u1.get("journey_count") == 0 and u1.get("scene_count") == 0, "F2 must not create production journeys or scenes")

    for unit in course["units"][1:]:
        require(unit.get("status") == "SOURCE_BACKED_SCAFFOLD", f"{unit['unit_id']} changed during Unit 1 F2")
        require(unit.get("journey_count") == 0 and unit.get("scene_count") == 0, f"{unit['unit_id']} gained narrative content")

    course_packages.clear_package_cache()
    require(course_packages.validate_package("ap-chemistry")["valid"] is True, "AP Chemistry package no longer validates")
    require(len(course_packages.artifact_records("ap-chemistry", "unit-1", "concepts")) == 48, "package loader does not expose 48 Unit 1 concepts")
    require(course_packages.journeys("ap-chemistry", "unit-1")["guided_journeys"] == [], "production Unit 1 journey registry must remain empty")

    admin_catalog.clear_catalog_cache()
    snapshot = admin_catalog.catalog_snapshot("ap-chemistry")
    counts = snapshot.get("summary", {}).get("counts", {})
    require(counts.get("unit") == 9, "Content Studio no longer sees nine AP Chemistry units")
    require(counts.get("concept") == 48, "Content Studio does not expose 48 Unit 1 concepts")
    require(counts.get("journey", 0) == 0 and counts.get("scene", 0) == 0, "Content Studio exposes premature Unit 1 narrative content")

    chemistry = next(item for item in registry["courses"] if item["course_id"] == "ap-chemistry")
    require(chemistry.get("status") == "development", "AP Chemistry left development state")
    require(chemistry.get("student_visible") is False, "AP Chemistry became student-visible")
    access = next(item for item in admin_catalog.catalog_courses()["courses"] if item["course_id"] == "ap-chemistry")
    require(access.get("editable") is False, "AP Chemistry became editable")

    require(f2.get("status") == "COMPLETE", "F2 documentation does not record completion")
    require(f2.get("counts", {}).get("scientific_records") == 48, "F2 documentation scientific count changed")
    require(f2.get("counts", {}).get("production_journeys") == 0, "F2 documentation claims production journeys")

    print("AP CHEMISTRY F2 UNIT 1 PASS")
    print("- 48 source-backed scientific records cover CED Topics 1.1-1.8")
    print("- Unit 1 scientific concepts are inspectable in the read-only Content Studio catalog")
    print("- four planned journeys and twenty planned loci preserve exact CED topic order")
    print("- every scientific record is assigned exactly once to a planned locus")
    print("- no narrative scene, Memory Object, review, mixed set, or Challenge Lab item is authored")
    print("- Units 2-9 remain F1 scaffolds")
    print("- AP Chemistry remains development-only, student-hidden, and read-only")
    print("- F3 Unit 1 Memory Object and retrieval architecture is the next authorized phase")


if __name__ == "__main__":
    main()
