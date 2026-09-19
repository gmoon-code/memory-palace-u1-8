from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_SOURCE_REGISTER.json"
INTAKE = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0_SOURCE_INTAKE.md"
CONTRACT = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0_CURRICULUM_CONTRACT.md"
FROZEN = "8d6a94fbab3bec63e53daaf80b949825d7eacccd"


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
    require(data.get("schema") == "story-method-ap-chemistry-source-register-1.0", "unexpected source-register schema")
    require(data.get("course_id") == "ap-chemistry", "source register is not AP Chemistry")
    require(data.get("phase") == "F0", "source register is not in F0")
    require(data.get("phase_status") == "SOURCE_INTAKE_OPEN", "F0 source intake is not open")

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

    requested = data.get("required_user_sources") or []
    require(len(requested) >= 5, "source intake does not request the full teacher-source set")
    require(all(item.get("status") == "pending" for item in requested), "F0 claims a user source that has not been ingested")

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
    require("Narrative writing begins after F0D" in intake_text, "narrative production is not gated behind F0")
    require("General model knowledge is not used to silently fill source gaps" in contract_text, "source-gap rule is missing")
    require("Particulate models" in contract_text and "quantitative relationships" in contract_text, "chemistry representation contract is incomplete")

    print("AP CHEMISTRY F0 SOURCE INTAKE PASS")
    print("- current College Board framework authority is registered")
    print("- all nine official units and current titles are locked for crosswalking")
    print("- teacher materials, textbook, labs, assessment resources, and pacing remain explicitly pending")
    print("- fixture discrepancies are recorded without changing fixture content")
    print("- AP Chemistry content and package files remain byte-for-byte at the frozen architecture baseline")
    print("- AP Chemistry remains development-only and hidden from students")
    print("- real curriculum and narrative production remain gated behind F0D")


if __name__ == "__main__":
    main()
