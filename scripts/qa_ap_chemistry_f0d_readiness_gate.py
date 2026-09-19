from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0D_READINESS_GATE.json"
REPORT = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0D_READINESS_GATE.md"
REGISTER = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_SOURCE_REGISTER.json"
F0A = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0A_SOURCE_INVENTORY.json"
F0B = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0B_FRAMEWORK_CROSSWALK.json"
F0C = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0C_SCIENCE_COMPONENT_PLAN.json"
FROZEN = "8d6a94fbab3bec63e53daaf80b949825d7eacccd"

EXPECTED_UNIT_TITLES = [
    "Atomic Structure and Properties",
    "Compound Structure and Properties",
    "Properties of Substances and Mixtures",
    "Chemical Reactions",
    "Kinetics",
    "Thermochemistry",
    "Equilibrium",
    "Acids and Bases",
    "Thermodynamics and Electrochemistry",
]
EXPECTED_TOPIC_COUNTS = [8, 7, 13, 9, 11, 9, 12, 11, 11]
EXPECTED_GAPS = ["1.4", "2.2", "7.8", "8.10", "8.11", "9.6", "9.7"]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"AP CHEMISTRY F0D READINESS GATE FAIL\n- {message}")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def main() -> None:
    for path in (GATE, REPORT, REGISTER, F0A, F0B, F0C):
        require(path.is_file(), f"missing F0D dependency: {path.relative_to(ROOT)}")

    gate = json.loads(GATE.read_text(encoding="utf-8"))
    register = json.loads(REGISTER.read_text(encoding="utf-8"))
    f0a = json.loads(F0A.read_text(encoding="utf-8"))
    f0b = json.loads(F0B.read_text(encoding="utf-8"))
    f0c = json.loads(F0C.read_text(encoding="utf-8"))

    require(gate.get("schema") == "story-method-ap-chemistry-f0d-readiness-gate-1.0", "unexpected F0D schema")
    require(gate.get("course_id") == "ap-chemistry", "F0D is not AP Chemistry")
    require(gate.get("phase") == "F0D", "readiness artifact is not F0D")
    require(gate.get("result") == "BLOCKED_PENDING_TEACHER_LAB_SOURCE", "F0D must remain blocked until lab source is cleared")
    require(gate.get("phase_status_after_gate") == "F0C_COMPLETE", "blocked F0D must not claim completion")

    artifacts = gate.get("source_artifacts") or {}
    require(artifacts["f0a_inventory"]["git_blob"] == git("rev-parse", "HEAD:docs/ap-chemistry/AP_CHEMISTRY_F0A_SOURCE_INVENTORY.json"), "F0A artifact fingerprint changed")
    require(artifacts["f0b_crosswalk"]["git_blob"] == git("rev-parse", "HEAD:docs/ap-chemistry/AP_CHEMISTRY_F0B_FRAMEWORK_CROSSWALK.json"), "F0B artifact fingerprint changed")
    require(artifacts["f0c_component_plan"]["git_blob"] == git("rev-parse", "HEAD:docs/ap-chemistry/AP_CHEMISTRY_F0C_SCIENCE_COMPONENT_PLAN.json"), "F0C artifact fingerprint changed")

    checks = gate.get("readiness_checks") or {}
    for key in (
        "source_inventory_complete",
        "official_units_locked",
        "all_91_topics_crosswalked",
        "teacher_materials_inventoried",
        "textbook_inventoried",
        "assessment_resources_inventoried",
        "component_plan_complete",
        "source_conflicts_and_gaps_recorded",
        "fixture_excluded_as_academic_evidence",
    ):
        require(checks.get(key) is True, f"readiness check is not complete: {key}")
    require(checks.get("topic_specific_teacher_lab_mapping_complete") is False, "F0D incorrectly claims lab mapping is complete")

    units = gate.get("official_unit_and_topic_lock") or []
    require(len(units) == 9, "F0D must lock nine units")
    require([u.get("title") for u in units] == EXPECTED_UNIT_TITLES, "F0D unit titles changed")
    require([len(u.get("topic_ids") or []) for u in units] == EXPECTED_TOPIC_COUNTS, "F0D topic counts changed")
    locked_topics = [topic for unit in units for topic in unit.get("topic_ids") or []]
    require(len(locked_topics) == 91 and len(set(locked_topics)) == 91, "F0D unit/topic lock must contain 91 unique topics")
    require(locked_topics == [record["topic_id"] for record in f0b["ced_topics"]], "F0D topic lock diverges from F0B CED order")

    resolutions = gate.get("source_gap_resolutions") or []
    require([item.get("topic_id") for item in resolutions] == EXPECTED_GAPS, "F0D did not disposition every F0B source gap")
    require(all(item.get("production_guard") for item in resolutions), "one or more gap dispositions lack production guards")
    topic_97 = next(item for item in resolutions if item["topic_id"] == "9.7")
    require(topic_97.get("disposition") == "ready_at_ced_minimum_with_teacher_depth_gap_retained", "Topic 9.7 teacher-depth gap was hidden")
    require(f0b.get("source_gap_topic_ids") == EXPECTED_GAPS, "F0B source-gap history changed")
    require(f0c.get("carried_f0b_source_gaps") == EXPECTED_GAPS, "F0C source-gap history changed")

    blockers = gate.get("hard_blockers") or []
    require(len(blockers) == 1, "F0D should currently have exactly one hard blocker")
    blocker = blockers[0]
    require(blocker.get("blocker_id") == "teacher-lab-source" and blocker.get("status") == "unresolved", "teacher lab blocker is missing")
    require("25 percent" in blocker.get("ced_course_requirement", ""), "CED lab-time requirement is missing")
    require("16 hands-on" in blocker.get("ced_course_requirement", ""), "CED hands-on lab count is missing")
    require("6 guided-inquiry" in blocker.get("ced_course_requirement", ""), "CED guided-inquiry requirement is missing")
    require(len(blocker.get("clearance_options") or []) == 2, "F0D must document both lab-source clearance paths")

    f0c_guard = f0c.get("lab_requirement_guard") or {}
    require(f0c_guard.get("f0d_blocker") is True, "F0C no longer marks lab source as an F0D blocker")
    require((f0c.get("coverage_summary") or {}).get("lab_context") == {"pending_teacher_lab_source": 91}, "F0C no longer shows 91 pending lab mappings")

    auth = gate.get("authorization") or {}
    require(auth.get("planning_documentation") is True, "blocked F0D should still allow source planning")
    for key in (
        "real_package_construction",
        "real_scientific_record_production",
        "memory_object_production",
        "narrative_story_authoring",
        "question_bank_production",
        "review_system_production",
        "challenge_lab_production",
        "student_visibility",
        "teacher_editability",
    ):
        require(auth.get(key) is False, f"blocked F0D incorrectly authorizes {key}")

    require(register.get("schema") == "story-method-ap-chemistry-source-register-1.4", "source register schema did not advance")
    require(register.get("phase_status") == "F0C_COMPLETE", "blocked F0D must leave phase_status at F0C_COMPLETE")
    require(register.get("f0d_readiness_status") == "BLOCKED_PENDING_TEACHER_LAB_SOURCE", "source register does not record blocked F0D")
    require(register.get("f0d_readiness_gate") == "docs/ap-chemistry/AP_CHEMISTRY_F0D_READINESS_GATE.json", "source register does not point to F0D gate")

    require(f0a.get("status") == "COMPLETE", "F0A is no longer complete")
    require(f0b.get("status") == "COMPLETE_WITH_RECORDED_SOURCE_GAPS", "F0B state changed")
    require(f0c.get("status") == "COMPLETE_WITH_LAB_SOURCE_PENDING_AND_F0B_GAPS", "F0C state changed")

    require(git("rev-parse", "HEAD:content/ap-chemistry") == git("rev-parse", f"{FROZEN}:content/ap-chemistry"), "F0D modified the AP Chemistry architecture fixture")
    require(git("rev-parse", "HEAD:platform/course-packages/ap-chemistry.json") == git("rev-parse", f"{FROZEN}:platform/course-packages/ap-chemistry.json"), "F0D modified the AP Chemistry package manifest")

    registry = json.loads((ROOT / "platform" / "courses.json").read_text(encoding="utf-8"))
    chemistry = next(item for item in registry["courses"] if item["course_id"] == "ap-chemistry")
    require(chemistry.get("status") == "development", "AP Chemistry left development status during blocked F0D")
    require(chemistry.get("student_visible") is False, "AP Chemistry became student-visible during blocked F0D")

    report = REPORT.read_text(encoding="utf-8")
    for marker in (
        "BLOCKED_PENDING_TEACHER_LAB_SOURCE",
        "The teacher laboratory source is still unresolved",
        "Topic 9.7",
        "real nine-unit package",
        "F0D will not invent",
    ):
        require(marker in report, f"F0D report is missing marker: {marker}")

    print("AP CHEMISTRY F0D READINESS GATE PASS")
    print("- readiness gate executed and correctly remains blocked on the unresolved teacher-lab source")
    print("- all nine unit titles and all 91 CED topic boundaries are locked")
    print("- all seven F0B source gaps have explicit bounded production dispositions")
    print("- Topic 9.7 retains its teacher-depth warning")
    print("- F0A, F0B, and F0C artifact fingerprints remain unchanged")
    print("- no real package, scientific records, Memory Objects, narratives, questions, review, or Challenge Lab work is authorized")
    print("- AP Chemistry fixture, package manifest, development status, and student-hidden lock remain unchanged")


if __name__ == "__main__":
    main()
