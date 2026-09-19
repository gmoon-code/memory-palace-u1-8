from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CROSSWALK = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0B_FRAMEWORK_CROSSWALK.json"
AUDIT = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0B_FRAMEWORK_CROSSWALK.md"
REGISTER = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_SOURCE_REGISTER.json"
F0A = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0A_SOURCE_INVENTORY.json"
FROZEN = "8d6a94fbab3bec63e53daaf80b949825d7eacccd"
F0D_COMPLETION = "afad50022055956df4342d0a963cbe07f8adf329"
PHASE_ORDER = {
    "F0A_COMPLETE": 1,
    "F0B_COMPLETE": 2,
    "F0C_COMPLETE": 3,
    "F0D_COMPLETE": 4,
}
REGISTER_SCHEMA_PREFIX = "story-method-ap-chemistry-source-register-1."


EXPECTED_COUNTS = {1: 8, 2: 7, 3: 13, 4: 9, 5: 11, 6: 9, 7: 12, 8: 11, 9: 11}
EXPECTED_GAPS = ["1.4", "2.2", "7.8", "8.10", "8.11", "9.6", "9.7"]
EXPECTED_ASSESSMENT = {
    1: ["assessment-guide-01"],
    2: ["assessment-guide-02"],
    3: ["assessment-guide-03", "assessment-guide-04"],
    4: ["assessment-guide-05"],
    5: ["assessment-guide-06"],
    6: ["assessment-guide-07"],
    7: ["assessment-guide-08"],
    8: ["assessment-guide-09"],
    9: ["assessment-guide-10"],
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"AP CHEMISTRY F0B FRAMEWORK CROSSWALK FAIL\n- {message}")


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def expected_topic_ids() -> list[str]:
    ids: list[str] = []
    for unit, count in EXPECTED_COUNTS.items():
        ids.extend(f"{unit}.{topic}" for topic in range(1, count + 1))
    return ids


def main() -> None:
    for path in (CROSSWALK, AUDIT, REGISTER, F0A):
        require(path.is_file(), f"missing F0B dependency: {path.relative_to(ROOT)}")

    data = json.loads(CROSSWALK.read_text(encoding="utf-8"))
    register = json.loads(REGISTER.read_text(encoding="utf-8"))
    records = data.get("ced_topics") or []

    require(data.get("schema") == "story-method-ap-chemistry-f0b-framework-crosswalk-1.0", "unexpected crosswalk schema")
    require(data.get("course_id") == "ap-chemistry", "crosswalk is not AP Chemistry")
    require(data.get("phase") == "F0B", "crosswalk phase is not F0B")
    require(data.get("status") == "COMPLETE_WITH_RECORDED_SOURCE_GAPS", "F0B completion status is wrong")
    require(data.get("topic_count") == 91 and len(records) == 91, "crosswalk must contain 91 CED topics")

    ids = [record.get("topic_id") for record in records]
    require(ids == expected_topic_ids(), "CED topics are missing, duplicated, or out of order")

    unit_counts = Counter(int(record["unit_id"].split("-")[1]) for record in records)
    require(dict(unit_counts) == EXPECTED_COUNTS, "unit topic counts do not match the CED")

    require(data.get("source_gap_topic_ids") == EXPECTED_GAPS, "recorded source-gap list changed")
    status_counts = Counter(record.get("crosswalk_status") for record in records)
    require(status_counts["complete_source_crosswalk"] == 84, "complete-source topic count changed")
    require(status_counts["partial_teacher_coverage"] == 6, "partial teacher-coverage count changed")
    require(status_counts["teacher_depth_gap"] == 1, "teacher-depth gap count changed")

    valid_ppts = {f"teacher-ppt-{n:02d}" for n in range(1, 16)}
    for record in records:
        topic = record["topic_id"]
        unit = int(topic.split(".")[0])
        skill = record.get("ced_suggested_skill") or {}
        require(re.fullmatch(r"[1-6]\.[A-G]", str(skill.get("code") or "")) is not None, f"{topic} has invalid suggested skill")
        require(bool(skill.get("practice_family")), f"{topic} is missing science-practice family")
        require(record.get("chemistry_reference_sections"), f"{topic} has no Zumdahl mapping")
        require(record.get("assessment_evidence_source_ids") == EXPECTED_ASSESSMENT[unit], f"{topic} has incorrect scoring-guide mapping")
        require(record.get("lab_source_status") == "pending_teacher_lab_collection", f"{topic} incorrectly claims teacher lab mapping")
        for source in record.get("teacher_depth_sources") or []:
            require(source.get("source_id") in valid_ppts, f"{topic} uses an unknown PPT source")
            require(bool(source.get("pages")), f"{topic} has a PPT mapping without pages")
            require(source.get("coverage") in {"direct", "supporting", "partial"}, f"{topic} has invalid PPT coverage state")

    gaps = {record["topic_id"]: record for record in records if record["topic_id"] in EXPECTED_GAPS}
    require(gaps["9.7"].get("teacher_depth_sources") == [], "Topic 9.7 must remain an explicit PPT gap")
    for topic in EXPECTED_GAPS:
        require(bool(gaps[topic].get("source_note")), f"{topic} is missing its source-gap explanation")

    authority = data.get("authority_contract") or {}
    require("Fall 2024" in authority.get("organization_scope_and_order", ""), "CED authority version is missing")
    require("June 2026" in authority.get("official_corrections", ""), "current College Board corrections check is missing")
    require("No topic-level" in authority.get("corrections_effect_on_topic_crosswalk", ""), "corrections impact is not recorded")
    require("PowerPoints" in authority.get("student_depth", ""), "PPT depth authority is missing")
    require("Zumdahl" in authority.get("chemistry_truth", ""), "Zumdahl chemistry authority is missing")

    require(str(register.get("schema") or "").startswith(REGISTER_SCHEMA_PREFIX), "unexpected source-register schema")
    require(PHASE_ORDER.get(register.get("phase_status"), 0) >= PHASE_ORDER["F0B_COMPLETE"], "source register does not record F0B completion")
    require(register.get("f0b_crosswalk") == "docs/ap-chemistry/AP_CHEMISTRY_F0B_FRAMEWORK_CROSSWALK.json", "source register does not point to F0B crosswalk")

    require(git("rev-parse", f"{F0D_COMPLETION}:content/ap-chemistry") == git("rev-parse", f"{FROZEN}:content/ap-chemistry"), "F0B modified the AP Chemistry architecture fixture")
    require(git("rev-parse", f"{F0D_COMPLETION}:platform/course-packages/ap-chemistry.json") == git("rev-parse", f"{FROZEN}:platform/course-packages/ap-chemistry.json"), "F0B modified the AP Chemistry package manifest")

    registry = json.loads((ROOT / "platform" / "courses.json").read_text(encoding="utf-8"))
    chemistry = next(item for item in registry["courses"] if item["course_id"] == "ap-chemistry")
    require(chemistry.get("status") == "development", "AP Chemistry left development status during F0B")
    require(chemistry.get("student_visible") is False, "AP Chemistry became student-visible during F0B")

    audit = AUDIT.read_text(encoding="utf-8")
    for marker in ("all 91 required CED topics", "84", "1.4, 2.2, 7.8, 8.10, 8.11, 9.6, and 9.7", "F0C Science Component Coverage Plan"):
        require(marker in audit, f"F0B audit is missing marker: {marker}")

    print("AP CHEMISTRY F0B FRAMEWORK CROSSWALK PASS")
    print("- all 91 CED topics are present in exact Unit 1-9 order")
    print("- every topic carries a CED suggested skill, PPT depth mapping, Zumdahl reference, and scoring-guide mapping")
    print("- 84 topics have complete teacher-depth/source mappings")
    print("- six topics retain partial PPT coverage and Topic 9.7 remains an explicit PPT gap")
    print("- June 2026 College Board corrections were checked and do not alter the topic crosswalk")
    print("- teacher laboratory mapping remains explicitly pending")
    print("- AP Chemistry fixture, manifest, development status, and student-hidden lock remain unchanged")
    print("- F0C Science Component Coverage Plan is the next authorized phase")


if __name__ == "__main__":
    main()
