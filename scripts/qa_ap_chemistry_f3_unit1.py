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
RETRIEVAL = ROOT / "content" / "ap-chemistry" / "unit-1" / "source" / "retrieval-architecture.json"
MEMORY = ROOT / "content" / "ap-chemistry" / "unit-1" / "memory-objects.json"
COURSE = ROOT / "content" / "ap-chemistry" / "course.json"
F3 = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F3_UNIT1.json"
REGISTRY = ROOT / "platform" / "courses.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"AP CHEMISTRY F3 UNIT 1 FAIL\n- {message}")


def main() -> None:
    for path in (CATALOG, ARCH, RETRIEVAL, MEMORY, COURSE, F3, REGISTRY):
        require(path.is_file(), f"missing F3 artifact: {path.relative_to(ROOT)}")

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    arch = json.loads(ARCH.read_text(encoding="utf-8"))
    retrieval = json.loads(RETRIEVAL.read_text(encoding="utf-8"))
    memory = json.loads(MEMORY.read_text(encoding="utf-8"))
    course = json.loads(COURSE.read_text(encoding="utf-8"))
    f3 = json.loads(F3.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    scientific = catalog.get("concepts") or []
    objects = memory.get("memory_objects") or []
    require(len(scientific) == 48, "F2 scientific catalog no longer contains 48 records")
    require(memory.get("schema") == "story-method-memory-objects-1.0", "unexpected memory-object schema")
    require(memory.get("phase") == "F3", "memory-object payload is not F3")
    require(memory.get("foundation_status") == "MEMORY_RETRIEVAL_ARCHITECTURE_LOCKED", "memory-object architecture is not locked")
    require(memory.get("count") == len(objects) == 48, "Unit 1 must contain 48 Memory Objects")

    scientific_by_id = {record["knowledge_id"]: record for record in scientific}
    source_ids = [obj.get("source_knowledge_id") for obj in objects]
    memory_ids = [obj.get("memory_object_id") for obj in objects]
    require(len(set(source_ids)) == 48 and set(source_ids) == set(scientific_by_id), "Memory Objects are not one-to-one with scientific records")
    require(len(set(memory_ids)) == 48, "Memory Object IDs are missing or duplicated")

    expected_assignment = {}
    expected_loci = set()
    for journey in arch.get("journeys") or []:
        for locus in journey.get("loci") or []:
            locus_id = f"{journey['journey_plan_id']}-L{locus['order']}"
            expected_loci.add(locus_id)
            for knowledge_id in locus.get("required_record_ids") or []:
                expected_assignment[knowledge_id] = (
                    journey["journey_plan_id"],
                    journey["working_palace_name"],
                    locus_id,
                    locus["name"],
                )
    require(len(expected_assignment) == 48 and len(expected_loci) == 21, "F2 locus assignment changed")

    exact_name_count = 0
    spelling_count = 0
    confusable_count = 0
    for obj in objects:
        source = scientific_by_id[obj["source_knowledge_id"]]
        expected = expected_assignment[obj["source_knowledge_id"]]
        require(obj.get("canonical_term") == source.get("canonical_label"), f"{obj['memory_object_id']} changed canonical term")
        require(obj.get("canonical_definition") == source.get("canonical_verified_statement"), f"{obj['memory_object_id']} changed canonical definition")
        require(obj.get("source_trace") == source.get("source_reference"), f"{obj['memory_object_id']} lost source trace")
        require(obj.get("ap_scope_class") == source.get("scope_class"), f"{obj['memory_object_id']} changed scope class")
        require(obj.get("scientific_lock_status") == "SOURCE_BACKED_LOCK", f"{obj['memory_object_id']} lost scientific lock")
        require(
            (obj.get("journey_plan_id"), obj.get("palace_zone"), obj.get("locus_id"), obj.get("primary_palace_locus")) == expected,
            f"{obj['memory_object_id']} moved away from its F2 palace/locus assignment",
        )
        require(bool(obj.get("micro_locus_anchor")), f"{obj['memory_object_id']} has no micro-locus anchor")
        require(bool(obj.get("mnemonic_actor_or_object")), f"{obj['memory_object_id']} has no mnemonic object")
        require(bool(obj.get("function_or_meaning_interaction")), f"{obj['memory_object_id']} has no scientific mnemonic interaction")
        require(obj.get("pronunciation") is None and obj.get("pronunciation_status") == "deferred_no_source_pronunciation_record", f"{obj['memory_object_id']} invented a source pronunciation")
        require(obj.get("application_question") is None and obj.get("application_answer_key") is None, f"{obj['memory_object_id']} prematurely authored an application question")
        require(obj.get("application_status") == "DEFERRED_TO_QUESTION_AUTHORING_PHASE", f"{obj['memory_object_id']} application status changed")
        require(obj.get("scene_entry") is None and obj.get("guided_scene") is None, f"{obj['memory_object_id']} prematurely authored narrative prose")
        require(obj.get("narrative_status") == "MNEMONIC_OBJECT_LOCKED_SCENE_PROSE_NOT_AUTHORED", f"{obj['memory_object_id']} narrative status changed")

        modes = set(obj.get("retrieval_modes") or [])
        require("name_to_meaning" in modes, f"{obj['memory_object_id']} lacks name-to-meaning retrieval")
        component_types = set(source.get("component_types") or [])
        if component_types & {"equation", "calculation"}:
            require("equation_or_quantitative_reasoning" in modes, f"{obj['memory_object_id']} lacks quantitative retrieval")
        if "graph" in component_types:
            require("graph_interpretation" in modes, f"{obj['memory_object_id']} lacks graph retrieval")
        if "data_table" in component_types:
            require("data_interpretation" in modes, f"{obj['memory_object_id']} lacks data-table retrieval")
        if "diagram" in component_types:
            require("diagram_interpretation" in modes, f"{obj['memory_object_id']} lacks diagram retrieval")
        if "particulate_model" in component_types:
            require("particulate_model_interpretation" in modes, f"{obj['memory_object_id']} lacks particulate-model retrieval")
        if source.get("scope_class") == "AP_SCOPE_GUARD":
            require(obj.get("object_type") == "CORRECTIVE_GUARD", f"{obj['memory_object_id']} scope guard is not corrective")
            require("scope_discrimination" in modes, f"{obj['memory_object_id']} scope guard lacks discrimination retrieval")

        if obj.get("exact_name_required") == "YES":
            exact_name_count += 1
            require("meaning_to_exact_name" in modes, f"{obj['memory_object_id']} exact-name retrieval is missing")
        if obj.get("exact_spelling_required") == "YES":
            spelling_count += 1
            require("spelling" in modes, f"{obj['memory_object_id']} spelling retrieval is missing")
            require(all(obj.get(key) for key in ("spelling_mask_stage_A", "spelling_mask_stage_B", "spelling_mask_stage_C")), f"{obj['memory_object_id']} spelling masks are incomplete")
        if obj.get("confusable_terms"):
            confusable_count += 1
            require("confusable_discrimination" in modes, f"{obj['memory_object_id']} confusable retrieval is missing")

    require(exact_name_count == 18, "exact-name retrieval count changed")
    require(spelling_count == 13, "spelling retrieval count changed")
    require(confusable_count == 26, "confusable-object count changed")

    require(retrieval.get("schema") == "story-method-ap-chemistry-retrieval-architecture-1.0", "unexpected retrieval-architecture schema")
    require(retrieval.get("status") == "RETRIEVAL_ARCHITECTURE_LOCKED_NARRATIVE_NOT_AUTHORED", "retrieval architecture is not locked")
    require(retrieval.get("counts", {}).get("memory_objects") == 48, "retrieval architecture count changed")
    require(len(retrieval.get("confusable_sets") or []) == 8, "F3 must lock eight confusable sets")
    require(retrieval.get("production_boundaries", {}).get("narrative_authored") is False, "F3 incorrectly claims narrative authoring")
    require(retrieval.get("production_boundaries", {}).get("production_journeys") == 0, "F3 created production journeys")
    require(retrieval.get("production_boundaries", {}).get("production_scenes") == 0, "F3 created production scenes")

    u1 = next(unit for unit in course["units"] if unit["unit_id"] == "unit-1")
    require(course.get("status") == "UNIT1_MEMORY_RETRIEVAL_ARCHITECTURE", "course status is not F3")
    require(course.get("production_phase") == "F3_UNIT1_MEMORY_OBJECT_AND_RETRIEVAL_ARCHITECTURE", "course phase is not F3")
    require(u1.get("status") == "MEMORY_RETRIEVAL_LOCKED", "Unit 1 status is not F3 locked")
    require(u1.get("canonical_records") == 48 and u1.get("memory_object_count") == 48, "Unit 1 metadata counts changed")
    require(u1.get("journey_count") == 0 and u1.get("scene_count") == 0, "F3 must not create production journeys or scenes")

    for unit in course["units"][1:]:
        require(unit.get("status") == "SOURCE_BACKED_SCAFFOLD", f"{unit['unit_id']} changed during Unit 1 F3")
        require(unit.get("journey_count") == 0 and unit.get("scene_count") == 0, f"{unit['unit_id']} gained narrative content")
        require(course_packages.memory_objects("ap-chemistry", unit["unit_id"]) == [], f"{unit['unit_id']} gained Memory Objects")

    course_packages.clear_package_cache()
    require(course_packages.validate_package("ap-chemistry")["valid"] is True, "AP Chemistry package no longer validates")
    require(len(course_packages.memory_objects("ap-chemistry", "unit-1")) == 48, "package loader does not expose 48 Unit 1 Memory Objects")
    require(course_packages.journeys("ap-chemistry", "unit-1")["guided_journeys"] == [], "production Unit 1 journeys must remain empty")

    admin_catalog.clear_catalog_cache()
    summary = admin_catalog.catalog_summary("ap-chemistry")
    counts = summary.get("counts", {})
    require(counts.get("unit") == 9, "Content Studio no longer sees nine AP Chemistry units")
    require(counts.get("concept") == 48, "Content Studio no longer exposes 48 Unit 1 concepts")
    require(counts.get("memory_object") == 48, "Content Studio does not expose 48 Unit 1 Memory Objects")
    require(counts.get("journey", 0) == 0 and counts.get("scene", 0) == 0, "Content Studio exposes premature narrative content")
    require(summary.get("unresolved_reference_count") == 0, "Content Studio has unresolved F3 references")

    snapshot = admin_catalog.catalog("ap-chemistry")
    represents = [edge for edge in snapshot["edges"] if edge.get("kind") == "represents" and edge.get("from", "").startswith("memory:unit-1:")]
    require(len(represents) == 48, "Memory Object to scientific-record dependency edges are incomplete")

    chemistry = next(item for item in registry["courses"] if item["course_id"] == "ap-chemistry")
    require(chemistry.get("status") == "development", "AP Chemistry left development state")
    require(chemistry.get("student_visible") is False, "AP Chemistry became student-visible")
    access = next(item for item in admin_catalog.catalog_courses()["courses"] if item["course_id"] == "ap-chemistry")
    require(access.get("editable") is False, "AP Chemistry became editable")

    require(f3.get("status") == "COMPLETE", "F3 documentation does not record completion")
    require(f3.get("counts", {}).get("memory_objects") == 48, "F3 documentation Memory Object count changed")
    require(f3.get("locks", {}).get("narrative_not_authored") is True, "F3 documentation incorrectly claims narrative authoring")

    print("AP CHEMISTRY F3 UNIT 1 PASS")
    print("- 48 Memory Objects map one-to-one to the 48 locked Unit 1 scientific records")
    print("- all F2 journey/locus assignments are preserved with distinct micro-locus anchors")
    print("- exact-name, spelling, quantitative, representation, scope, and confusable retrieval requirements are locked")
    print("- Content Studio exposes 48 linked concepts and 48 linked Memory Objects with zero unresolved references")
    print("- application questions and narrative scene prose remain deferred")
    print("- production journeys and scenes remain zero")
    print("- Units 2-9 remain F1 scaffolds")
    print("- AP Chemistry remains development-only, student-hidden, and read-only")
    print("- F4 Unit 1 narrative briefs and scene-writing architecture is the next authorized phase")


if __name__ == "__main__":
    main()
