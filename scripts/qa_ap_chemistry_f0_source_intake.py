from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_SOURCE_REGISTER.json"
INTAKE = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0_SOURCE_INTAKE.md"
CONTRACT = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0_CURRICULUM_CONTRACT.md"
FROZEN = "8d6a94fbab3bec63e53daaf80b949825d7eacccd"
PHASE_ORDER = {
    "F0A_COMPLETE": 1,
    "F0B_COMPLETE": 2,
    "F0C_COMPLETE": 3,
    "F0D_COMPLETE": 4,
}
REGISTER_SCHEMA_PREFIX = "story-method-ap-chemistry-source-register-1."



def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"AP CHEMISTRY F0 SOURCE INTAKE FAIL\n- {message}")


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> None:
    for path in (REGISTER, INTAKE, CONTRACT):
        require(path.is_file(), f"missing F0 artifact: {path.relative_to(ROOT)}")

    data = json.loads(REGISTER.read_text(encoding="utf-8"))
    require(str(data.get("schema") or "").startswith(REGISTER_SCHEMA_PREFIX), "unexpected source-register schema")
    require(data.get("course_id") == "ap-chemistry", "source register is not AP Chemistry")
    require(data.get("phase") == "F0", "source register is not in F0")
    require(PHASE_ORDER.get(data.get("phase_status"), 0) >= PHASE_ORDER["F0A_COMPLETE"], "F0A source inventory has not completed")

    framework = data.get("framework_authority") or {}
    require(framework.get("publisher") == "College Board", "College Board is not recorded as framework authority")
    require(framework.get("effective") == "Fall 2024", "current framework version is not locked")
    require(framework.get("status_for_2026_27") == "current", "2026-27 framework status is not recorded")

    units = data.get("official_unit_framework") or []
    require(len(units) == 9, "official framework must contain nine units")
    expected_titles = [
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
    require([item.get("title") for item in units] == expected_titles, "official unit titles changed")
    require([item.get("unit_id") for item in units] == [f"unit-{n}" for n in range(1, 10)], "official unit IDs are incomplete")

    requested = {item.get("source_id"): item for item in data.get("required_user_sources") or []}
    require(len(requested) >= 5, "source intake does not track the full teacher-source set")
    require(requested["teacher-ap-chemistry-unit-materials"].get("status") == "received", "teacher PowerPoints are not registered")
    require(requested["primary-ap-chemistry-textbook"].get("status") == "received", "primary textbook is not registered")
    require(requested["teacher-ap-chemistry-assessment-resources"].get("status") == "received", "assessment guides are not registered")
    require(requested["teacher-ap-chemistry-labs"].get("status") in {"pending", "waived_by_user_directive"}, "lab-source state is invalid")
    if PHASE_ORDER.get(data.get("phase_status"), 0) >= PHASE_ORDER["F0D_COMPLETE"]:
        require(requested["teacher-ap-chemistry-labs"].get("status") == "waived_by_user_directive", "completed F0D must record the lab-source directive")
        require(data.get("lab_source_basis") == "docs/ap-chemistry/AP_CHEMISTRY_LAB_SOURCE_BASIS.json", "completed F0D must register the lab-source basis")
    require(requested["teacher-ap-chemistry-pacing"].get("status") == "not_required", "CED-order pacing directive is not registered")

    directives = data.get("user_source_directives") or {}
    require("College Board CED" in directives.get("organization_and_order", ""), "CED organization/order directive is missing")
    require("PPT" in directives.get("ppt_role", ""), "PPT depth directive is missing")
    require("Zumdahl" in directives.get("textbook_role", ""), "Zumdahl chemistry authority is missing")
    require(data.get("f0a_inventory") == "docs/ap-chemistry/AP_CHEMISTRY_F0A_SOURCE_INVENTORY.json", "F0A inventory link is missing")

    differences = {item.get("issue_id"): item for item in data.get("fixture_differences_to_reconcile") or []}
    require("fixture-unit-2-title" in differences, "fixture Unit 2 title discrepancy is not recorded")
    require("fixture-units-3-through-9" in differences, "missing fixture Units 3 through 9 are not recorded")

    current_fixture = git("rev-parse", "HEAD:content/ap-chemistry")
    frozen_fixture = git("rev-parse", f"{FROZEN}:content/ap-chemistry")
    require(current_fixture == frozen_fixture, "F0 modified the AP Chemistry architecture fixture")

    current_package = git("rev-parse", "HEAD:platform/course-packages/ap-chemistry.json")
    frozen_package = git("rev-parse", f"{FROZEN}:platform/course-packages/ap-chemistry.json")
    require(current_package == frozen_package, "F0 modified the AP Chemistry package manifest")

    current_registry = json.loads((ROOT / "platform" / "courses.json").read_text(encoding="utf-8"))
    record = next(item for item in current_registry["courses"] if item["course_id"] == "ap-chemistry")
    require(record.get("status") == "development", "AP Chemistry left development status during F0")
    require(record.get("student_visible") is False, "AP Chemistry became student-visible during F0")

    intake_text = INTAKE.read_text(encoding="utf-8")
    contract_text = CONTRACT.read_text(encoding="utf-8")
    for marker in ("F0A Source Inventory", "F0B Framework Crosswalk", "F0C Science Component Coverage Plan", "F0D Readiness Gate"):
        require(marker in intake_text, f"missing F0 deliverable marker: {marker}")
    phase_rank = PHASE_ORDER.get(data.get("phase_status"), 0)
    if phase_rank < PHASE_ORDER["F0D_COMPLETE"]:
        require("Narrative writing begins" in intake_text and "F0D" in intake_text, "narrative production is not gated behind F0")
    else:
        require("Narrative writing is now authorized" in intake_text and "F0D" in intake_text, "completed F0D narrative authorization is not documented")
        require(data.get("f0d_readiness_status") == "COMPLETE", "completed phase must record completed F0D readiness")
    require("General model knowledge is not used to silently fill source gaps" in contract_text, "source-gap rule is missing")
    require("Particulate models" in contract_text and "quantitative relationships" in contract_text, "chemistry representation contract is incomplete")

    print("AP CHEMISTRY F0 SOURCE INTAKE PASS")
    print("- current College Board framework authority is registered")
    print("- all nine official units and current titles are locked for crosswalking")
    print("- teacher PowerPoints, Zumdahl 11e, and scoring guides are registered as received")
    print("- CED order is locked; separate pacing is not required; lab source state is explicitly tracked")
    print("- fixture discrepancies are recorded without changing fixture content")
    print("- AP Chemistry content and package files remain byte-for-byte at the frozen architecture baseline")
    print("- AP Chemistry remains development-only and hidden from students")
    if PHASE_ORDER.get(data.get("phase_status"), 0) >= PHASE_ORDER["F0D_COMPLETE"]:
        print("- F0D is complete; later package/content production is authorized while publication remains locked")
    else:
        print("- real curriculum and narrative production remain gated behind F0D")


if __name__ == "__main__":
    main()
