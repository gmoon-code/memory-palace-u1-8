from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0A_SOURCE_INVENTORY.json"
REGISTER = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_SOURCE_REGISTER.json"
AUDIT = ROOT / "docs" / "ap-chemistry" / "AP_CHEMISTRY_F0A_SOURCE_INVENTORY.md"
FROZEN = "8d6a94fbab3bec63e53daaf80b949825d7eacccd"
PHASE_ORDER = {
    "F0A_COMPLETE": 1,
    "F0B_COMPLETE": 2,
    "F0C_COMPLETE": 3,
    "F0D_COMPLETE": 4,
}
REGISTER_SCHEMA_PREFIX = "story-method-ap-chemistry-source-register-1."

SHA256 = re.compile(r"^[0-9a-f]{64}$")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"AP CHEMISTRY F0A SOURCE INVENTORY FAIL\n- {message}")


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
    for path in (INVENTORY, REGISTER, AUDIT):
        require(path.is_file(), f"missing F0A artifact: {path.relative_to(ROOT)}")

    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    register = json.loads(REGISTER.read_text(encoding="utf-8"))

    require(inventory.get("schema") == "story-method-ap-chemistry-f0a-source-inventory-1.0", "unexpected inventory schema")
    require(inventory.get("course_id") == "ap-chemistry", "inventory is not AP Chemistry")
    require(inventory.get("phase") == "F0A" and inventory.get("status") == "COMPLETE", "F0A is not complete")
    require(inventory.get("source_count") == 27, "source count must be 27")
    require(inventory.get("total_pages") == 3204, "source page total must be 3204")

    ppts = inventory.get("teacher_instructional_materials") or []
    guides = inventory.get("assessment_guides") or []
    require(len(ppts) == 15, "all fifteen teacher PowerPoints are not inventoried")
    require(len(guides) == 10, "all ten scoring-guide PDFs are not inventoried")
    require(sum(item["pages"] for item in ppts) == 1161, "PowerPoint page total changed")
    require(sum(item["pages"] for item in guides) == 587, "scoring-guide page total changed")

    require([item["source_label"] for item in ppts] == [f"PPT U{n}" for n in range(1, 16)], "PPT source-label sequence is incomplete")
    require(all(item.get("organization_authority") is False for item in ppts), "a PPT was incorrectly made an organization authority")

    expected_units = [f"unit-{n}" for n in range(1, 10)]
    ced = inventory.get("ced_order_lock") or []
    require([item.get("unit_id") for item in ced] == expected_units, "CED unit-order lock changed")
    require([item.get("number") for item in ced] == list(range(1, 10)), "CED unit numbers changed")

    guide_units = [item.get("ced_unit_id") for item in guides]
    require(set(guide_units) == set(expected_units), "assessment evidence does not cover all nine CED units")
    require(guide_units.count("unit-3") == 2, "Unit 3 assessment evidence must include 3A and 3B")

    framework = inventory.get("framework_source") or {}
    textbook = inventory.get("chemistry_reference") or {}
    require(framework.get("pages") == 238 and framework.get("effective") == "Fall 2024", "CED source metadata changed")
    require(textbook.get("pages") == 1218 and textbook.get("edition") == "11th", "Zumdahl source metadata changed")
    require("Zumdahl" in textbook.get("title", "") or "Zumdahl" in " ".join(textbook.get("authors") or []), "Zumdahl authority is missing")

    every_source = [framework, textbook, *ppts, *guides]
    require(len(every_source) == 27, "flattened source inventory must contain 27 records")
    filenames = [item.get("filename") for item in every_source]
    require(len(set(filenames)) == 27, "source filenames are not unique")
    require(all(SHA256.fullmatch(str(item.get("sha256") or "")) for item in every_source), "one or more source SHA-256 fingerprints are invalid")
    require(sum(int(item.get("pages", 0)) for item in every_source) == 3204, "flattened page total does not match inventory")

    authority = inventory.get("authority_contract") or {}
    require("Course and Exam Description" in authority.get("organization_and_order", ""), "CED organization authority is missing")
    require("PowerPoint" in authority.get("student_understanding_depth", ""), "PPT depth authority is missing")
    require("Chemistry" in authority.get("chemistry_truth_and_explanatory_reference", ""), "textbook chemistry authority is missing")

    sequence = inventory.get("sequencing_contract") or {}
    require("CED Unit 1 through Unit 9 order" in sequence.get("rule", ""), "CED sequence lock is missing")
    require("source labels only" in sequence.get("ppt_numbering_rule", ""), "PPT numbering is not explicitly non-structural")
    require("F0B" in sequence.get("crosswalk_rule", ""), "crosswalk relocation rule is missing")

    pending = {item.get("source_id"): item for item in inventory.get("still_pending") or []}
    require(pending.get("teacher-ap-chemistry-labs", {}).get("status") == "pending", "teacher lab source state is not pending")
    no_longer_required = {item.get("source_id"): item for item in inventory.get("explicitly_not_required") or []}
    require(no_longer_required.get("teacher-ap-chemistry-pacing", {}).get("status") == "not_required", "pacing source should be waived by CED-order directive")

    require(str(register.get("schema") or "").startswith(REGISTER_SCHEMA_PREFIX), "unexpected source-register schema")
    require(PHASE_ORDER.get(register.get("phase_status"), 0) >= PHASE_ORDER["F0A_COMPLETE"], "source register does not record F0A completion")
    require(register.get("f0a_inventory") == "docs/ap-chemistry/AP_CHEMISTRY_F0A_SOURCE_INVENTORY.json", "source register does not point to inventory")

    current_fixture = git("rev-parse", "HEAD:content/ap-chemistry")
    frozen_fixture = git("rev-parse", f"{FROZEN}:content/ap-chemistry")
    require(current_fixture == frozen_fixture, "F0A modified the AP Chemistry architecture fixture")

    current_package = git("rev-parse", "HEAD:platform/course-packages/ap-chemistry.json")
    frozen_package = git("rev-parse", f"{FROZEN}:platform/course-packages/ap-chemistry.json")
    require(current_package == frozen_package, "F0A modified the AP Chemistry package manifest")

    registry = json.loads((ROOT / "platform" / "courses.json").read_text(encoding="utf-8"))
    chemistry = next(item for item in registry["courses"] if item["course_id"] == "ap-chemistry")
    require(chemistry.get("status") == "development", "AP Chemistry left development status during F0A")
    require(chemistry.get("student_visible") is False, "AP Chemistry became student-visible during F0A")

    audit = AUDIT.read_text(encoding="utf-8")
    for marker in ("Twenty-seven", "3,204", "PPT U15", "Unit 3A", "Unit 3B", "F0B constructs the framework crosswalk"):
        require(marker in audit, f"F0A audit is missing marker: {marker}")

    print("AP CHEMISTRY F0A SOURCE INVENTORY PASS")
    print("- 27 source PDFs fingerprinted across CED, textbook, teacher PPT, and scoring-guide groups")
    print("- 3,204 source pages inventoried")
    print("- CED controls unit/topic order; PPT numbering is explicitly non-structural")
    print("- teacher PPTs control intended student depth; Zumdahl 11e controls chemistry truth within CED scope")
    print("- scoring guides cover CED Units 1-9, with Unit 3 represented by 3A and 3B")
    print("- teacher lab materials remain pending and separate pacing is waived by the CED-order directive")
    print("- AP Chemistry fixture, package manifest, development status, and student-hidden lock remain unchanged")
    print("- F0B Framework Crosswalk is the next authorized phase")


if __name__ == "__main__":
    main()
