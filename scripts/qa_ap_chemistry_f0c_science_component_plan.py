from __future__ import annotations

import json
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0C_SCIENCE_COMPONENT_PLAN.json"
AUDIT = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0C_SCIENCE_COMPONENT_PLAN.md"
CROSSWALK = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0B_FRAMEWORK_CROSSWALK.json"
REGISTER = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_SOURCE_REGISTER.json"
FROZEN = "8d6a94fbab3bec63e53daaf80b949825d7eacccd"
F0D_COMPLETION = "afad50022055956df4342d0a963cbe07f8adf329"
PHASE_ORDER = {"F0A_COMPLETE": 1, "F0B_COMPLETE": 2, "F0C_COMPLETE": 3, "F0D_COMPLETE": 4}
VALID_COMPONENT_STATES = {"required", "supporting", "not_primary", "excluded", "not_used"}
EXPECTED_GAPS = ["1.4", "2.2", "7.8", "8.10", "8.11", "9.6", "9.7"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"AP CHEMISTRY F0C SCIENCE COMPONENT PLAN FAIL\n- {message}")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def main() -> None:
    for path in (PLAN, AUDIT, CROSSWALK, REGISTER):
        require(path.is_file(), f"missing F0C dependency: {path.relative_to(ROOT)}")

    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    crosswalk = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    register = json.loads(REGISTER.read_text(encoding="utf-8"))

    require(plan.get("schema") == "story-method-ap-chemistry-f0c-science-component-plan-1.1", "unexpected plan schema")
    require(plan.get("course_id") == "ap-chemistry", "plan is not AP Chemistry")
    require(plan.get("phase") == "F0C", "plan phase is not F0C")
    require(plan.get("status") == "COMPLETE_WITH_COLLEGE_BOARD_LAB_BASIS_AND_F0B_GAPS", "F0C completion status is wrong")
    require(plan.get("topic_count") == 91, "F0C must cover 91 topics")

    records = plan.get("topics") or []
    cross = crosswalk.get("ced_topics") or []
    require(len(records) == len(cross) == 91, "F0B/F0C topic totals diverged")
    require([r["topic_id"] for r in records] == [r["topic_id"] for r in cross], "F0C changed CED topic order")
    require([r["title"] for r in records] == [r["title"] for r in cross], "F0C changed CED topic titles")
    require(plan.get("carried_f0b_source_gaps") == EXPECTED_GAPS, "F0B source gaps were not preserved")

    component_keys = {"concept", "memory_object", "equation", "calculation", "graph", "diagram", "data_table", "particulate_model", "vector", "lab_context"}
    by_topic = {}
    for record in records:
        topic = record["topic_id"]
        by_topic[topic] = record
        components = record.get("science_components") or {}
        require(set(components) == component_keys, f"{topic} component keys are incomplete")
        require(all(value in VALID_COMPONENT_STATES for value in components.values()), f"{topic} has an invalid component state")
        require(components["concept"] == "required", f"{topic} concept is not required")
        require(components["memory_object"] == "required", f"{topic} Memory Object pathway is not required")
        require(components["vector"] == "not_used", f"{topic} unexpectedly uses vector capability")
        require(components["lab_context"] in {"supporting", "not_primary"}, f"{topic} has invalid lab-context state")
        require(record.get("lab_mapping_status") == "college_board_public_guidance_mapped", f"{topic} lab-source mapping is incomplete")
        planning = record.get("lab_planning") or {}
        require(planning.get("candidate_class") in {"core_candidate", "supporting_candidate", "context_only"}, f"{topic} has invalid lab candidate class")
        require(planning.get("official_college_board_topic_assignment") is False, f"{topic} incorrectly claims an official College Board lab assignment")
        require(planning.get("teacher_specific_procedure") is False, f"{topic} incorrectly claims a teacher-specific procedure")
        require(record.get("representation_levels"), f"{topic} has no representation-level plan")
        basis = record.get("source_basis") or {}
        require(basis.get("chemistry_reference_sections"), f"{topic} lost its Zumdahl source mapping")
        require(basis.get("assessment_evidence_source_ids"), f"{topic} lost assessment evidence")

    for topic in EXPECTED_GAPS:
        require(bool(by_topic[topic].get("source_gap_guard")), f"{topic} has no source-gap guard")

    require(by_topic["7.8"]["science_components"]["particulate_model"] == "required", "Topic 7.8 must require a particulate model")
    require(by_topic["8.11"]["science_components"]["calculation"] == "excluded", "Topic 8.11 quantitative pH-solubility calculation exclusion is missing")
    require(by_topic["9.10"]["science_components"]["calculation"] == "not_primary", "Topic 9.10 must not require Nernst calculations")
    require(any("Nernst" in item for item in by_topic["9.10"].get("exclusions", [])), "Topic 9.10 Nernst scope guard is missing")
    require(by_topic["9.7"]["source_basis"]["teacher_depth_sources"] == [], "Topic 9.7 teacher-PPT gap was silently filled")

    lab_guard = plan.get("lab_requirement_guard") or {}
    require("25 percent" in lab_guard.get("ced_requirement", ""), "CED lab-time requirement is missing")
    require("16 hands-on" in lab_guard.get("ced_requirement", ""), "CED hands-on lab count is missing")
    require("6 of the 16 guided inquiry" in lab_guard.get("ced_requirement", ""), "CED guided-inquiry count is missing")
    require(lab_guard.get("f0d_blocker") is False, "lab source blocker should be cleared")
    require(lab_guard.get("source_basis") == "docs/ap-chemistry/AP_CHEMISTRY_LAB_SOURCE_BASIS.json", "F0C does not point to the inventoried lab source basis")
    require(lab_guard.get("mapping_is_official_college_board_assignment") is False, "F0C incorrectly labels project mappings as official College Board assignments")

    summary = plan.get("coverage_summary") or {}
    for component in ("equation", "calculation", "graph", "diagram", "data_table", "particulate_model"):
        counts = Counter(r["science_components"][component] for r in records)
        require(dict(counts) == summary.get(component), f"{component} summary counts do not match topic records")
    require(summary.get("lab_context") == {"supporting": 43, "not_primary": 48}, "lab-context summary changed")
    require(summary.get("lab_planning_candidate_class") == {"core_candidate": 18, "supporting_candidate": 25, "context_only": 48}, "lab candidate summary changed")
    require(summary.get("vector") == {"not_used": 91}, "vector summary changed")

    require(str(register.get("schema") or "").startswith("story-method-ap-chemistry-source-register-1."), "unexpected source-register schema")
    require(PHASE_ORDER.get(register.get("phase_status"), 0) >= PHASE_ORDER["F0C_COMPLETE"], "source register does not record F0C completion")
    require(register.get("f0c_component_plan") == "docs/ap-chemistry/AP_CHEMISTRY_F0C_SCIENCE_COMPONENT_PLAN.json", "source register does not point to F0C plan")

    require(git("rev-parse", f"{F0D_COMPLETION}:content/ap-chemistry") == git("rev-parse", f"{FROZEN}:content/ap-chemistry"), "F0C modified the AP Chemistry architecture fixture")
    require(git("rev-parse", f"{F0D_COMPLETION}:platform/course-packages/ap-chemistry.json") == git("rev-parse", f"{FROZEN}:platform/course-packages/ap-chemistry.json"), "F0C modified the AP Chemistry package manifest")

    registry = json.loads((ROOT / "platform" / "courses.json").read_text(encoding="utf-8"))
    chemistry = next(item for item in registry["courses"] if item["course_id"] == "ap-chemistry")
    require(chemistry.get("status") == "development", "AP Chemistry left development status during F0C")
    require(chemistry.get("student_visible") is False, "AP Chemistry became student-visible during F0C")

    audit = AUDIT.read_text(encoding="utf-8")
    for marker in ("Every one of the 91 CED topics", "Topic 8.11", "Topic 9.10", "Topic 7.8", "Topic 9.7", "F0D Readiness Gate"):
        require(marker in audit, f"F0C audit is missing marker: {marker}")

    print("AP CHEMISTRY F0C SCIENCE COMPONENT PLAN PASS")
    print("- all 91 CED topics retain exact F0B order and source mappings")
    print("- equations, calculations, graphs, diagrams, data tables, and particulate models are classified topic by topic")
    print("- concepts and Memory Object pathways are required for all topics")
    print("- vector capability remains unused for AP Chemistry")
    print("- Topic 7.8 particulate-model requirement and Topics 8.11/9.10 scope guards are locked")
    print("- all seven F0B source gaps remain explicit")
    print("- all 91 topics have College Board-guidance-based project lab-planning classes without claiming official College Board topic assignments")
    print("- F0D completion checkpoint preserves the architecture fixture/package; current course remains development-only and student-hidden")
    print("- updated F0C lab mapping supports the completed F0D readiness gate")


if __name__ == "__main__":
    main()
