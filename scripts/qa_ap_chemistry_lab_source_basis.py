from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASIS = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_LAB_SOURCE_BASIS.json"
REPORT = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_LAB_SOURCE_BASIS.md"
F0C = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0C_SCIENCE_COMPONENT_PLAN.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"AP CHEMISTRY LAB SOURCE BASIS FAIL\n- {message}")


def main() -> None:
    for path in (BASIS, REPORT, F0C):
        require(path.is_file(), f"missing lab-source artifact: {path.relative_to(ROOT)}")

    basis = json.loads(BASIS.read_text(encoding="utf-8"))
    plan = json.loads(F0C.read_text(encoding="utf-8"))

    require(basis.get("schema") == "story-method-ap-chemistry-lab-source-basis-1.0", "unexpected lab-source schema")
    require(basis.get("status") == "INVENTORIED_AND_AUTHORIZED_BY_USER_DIRECTIVE", "lab source basis is not authorized")
    require("CED/public College Board" in basis.get("user_directive", ""), "explicit user directive is missing")

    sources = {item["source_id"]: item for item in basis.get("sources") or []}
    require("college-board-ap-chemistry-ced-lab-guidance" in sources, "CED lab guidance source missing")
    require("college-board-ap-chemistry-course-audit" in sources, "Course Audit lab guidance source missing")
    require("college-board-hands-on-lab-faq" in sources, "hands-on lab FAQ source missing")
    require(sources["college-board-ap-chemistry-course-audit"]["url"].startswith("https://apcentral.collegeboard.org/"), "Course Audit source is not College Board")
    require(sources["college-board-hands-on-lab-faq"]["url"].startswith("https://apcentral.collegeboard.org/"), "hands-on FAQ source is not College Board")

    effect = basis.get("clearance_effect") or {}
    require(effect.get("teacher_specific_lab_collection_required") is False, "teacher-specific lab collection should be waived")
    require(effect.get("f0d_teacher_lab_blocker_cleared") is True, "F0D lab blocker is not cleared")
    require(effect.get("exact_16_lab_sequence_selected") is False, "source-basis step must not pretend the final 16-lab slate is selected")

    mapping = basis.get("mapping_policy") or {}
    require("not a College Board official lab assignment" in mapping.get("topic_mapping_method", ""), "topic mapping is not clearly separated from official College Board assignments")
    require("Do not invent or attribute College Board procedures" in mapping.get("procedure_rule", ""), "procedure source guard is missing")
    require("at least 16" in mapping.get("count_rule", "") and "at least 6" in mapping.get("count_rule", ""), "future lab-count rule is incomplete")

    records = plan.get("topics") or []
    require(len(records) == 91, "F0C no longer has 91 topics")
    classes = [record.get("lab_planning", {}).get("candidate_class") for record in records]
    require(classes.count("core_candidate") == 18, "core lab-candidate count changed")
    require(classes.count("supporting_candidate") == 25, "supporting lab-candidate count changed")
    require(classes.count("context_only") == 48, "context-only count changed")
    require(all(record.get("lab_mapping_status") == "college_board_public_guidance_mapped" for record in records), "one or more F0C topics lacks the new lab-source mapping")
    require(all(record.get("lab_planning", {}).get("official_college_board_topic_assignment") is False for record in records), "a project lab mapping is incorrectly labeled as an official College Board assignment")
    require(all(record.get("lab_planning", {}).get("teacher_specific_procedure") is False for record in records), "a teacher-specific lab procedure was invented")

    named = basis.get("named_but_not_ingested_resource") or {}
    require(named.get("status") == "referenced_by_current_course_audit_not_ingested_as_source_document", "Guided Inquiry resource boundary is missing")
    require("Do not reproduce" in named.get("rule", ""), "non-ingested resource reproduction guard is missing")

    report = REPORT.read_text(encoding="utf-8")
    for marker in ("18 core candidates", "25 supporting candidates", "48 context-only", "does not prescribe", "F0D clearance"):
        require(marker in report, f"lab-source report is missing marker: {marker}")

    print("AP CHEMISTRY LAB SOURCE BASIS PASS")
    print("- CED, current AP Chemistry Course Audit guidance, and College Board hands-on-lab guidance are inventoried")
    print("- teacher-specific lab collection is waived by explicit user directive")
    print("- 91 CED topics have project lab-context classifications without claiming official College Board topic assignments")
    print("- no College Board procedure is invented or reproduced from an uningested manual")
    print("- future course still must select at least 16 hands-on labs, at least 6 guided inquiry, and preserve at least 25 percent lab time")
    print("- F0D teacher-lab-source blocker is cleared")


if __name__ == "__main__":
    main()
