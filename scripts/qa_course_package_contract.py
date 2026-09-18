from __future__ import annotations

import json
from pathlib import Path

from backend import content, course_packages


ROOT = Path(__file__).resolve().parents[1]
COURSE_ID = "ap-biology"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"COURSE PACKAGE CONTRACT QA FAIL\n- {message}")


def main() -> None:
    result = course_packages.validate_package(COURSE_ID)
    require(result["valid"], "; ".join(result["errors"]))

    registry = content.course_registry()
    record = next(item for item in registry["courses"] if item["course_id"] == COURSE_ID)
    require(record["package_schema"] == course_packages.PACKAGE_SCHEMA, "registry package schema does not match loader")
    require(record["package_manifest"] == "platform/course-packages/ap-biology.json", "registry package manifest path changed")

    package = course_packages.package_manifest(COURSE_ID)
    course = course_packages.course(COURSE_ID)
    require(len(package["units"]) == len(course["units"]) == 8, "AP Biology package does not expose 8 units")

    journey_count = 0
    scene_count = 0
    challenge_count = 0
    review_count = 0
    mixed_set_count = 0
    resolved_object_ids: set[str] = set()

    for unit in course["units"]:
        unit_id = unit["unit_id"]
        packaged_registry = course_packages.journeys(COURSE_ID, unit_id)["guided_journeys"]
        legacy_registry = content.journey_registry(unit_id)
        require(
            [item["palace_id"] for item in packaged_registry] == [item["palace_id"] for item in legacy_registry],
            f"{unit_id} package journey order differs from legacy runtime",
        )
        journey_count += len(packaged_registry)

        for meta in packaged_registry:
            palace_id = meta["palace_id"]
            packaged = course_packages.journey(COURSE_ID, unit_id, palace_id)
            legacy = content.journey_by_id(unit_id, palace_id)
            require(packaged == legacy, f"{unit_id}/{palace_id} package journey differs from legacy runtime")
            scene_count += len(packaged.get("scenes", []))
            for scene in packaged.get("scenes", []):
                for object_id in scene.get("object_ids", []) or []:
                    if object_id:
                        resolved_object_ids.add(f"{unit_id}:{object_id}")
                checkpoint_id = scene.get("checkpoint_object_id")
                if checkpoint_id:
                    resolved_object_ids.add(f"{unit_id}:{checkpoint_id}")
                for beat in scene.get("story_beats", []) or []:
                    object_id = beat.get("object_id") if isinstance(beat, dict) else None
                    if object_id:
                        resolved_object_ids.add(f"{unit_id}:{object_id}")

        packaged_lab = course_packages.application_lab(COURSE_ID, unit_id)
        legacy_lab = {
            "unit-1": content.application_lab,
            "unit-2": content.unit2_application_lab,
            "unit-3": content.unit3_application_lab,
            "unit-4": content.unit4_application_lab,
            "unit-5": content.unit5_application_lab,
            "unit-6": content.unit6_application_lab,
            "unit-7": content.unit7_application_lab,
            "unit-8": content.unit8_application_lab,
        }[unit_id]()
        require(packaged_lab == legacy_lab, f"{unit_id} Challenge Lab differs from legacy runtime")
        challenge_count += len(packaged_lab.get("items", []))

        packaged_review = course_packages.review_manifest(COURSE_ID, unit_id)
        packaged_mixed = course_packages.mixed_discrimination(COURSE_ID, unit_id)
        if unit_id == "unit-1":
            require(packaged_review.get("targets") == [], "Unit 1 review adapter is not empty")
            require(packaged_mixed.get("sets") == [], "Unit 1 mixed adapter is not empty")
        else:
            number = unit_id.split("-")[1]
            legacy_review = getattr(content, f"unit{number}_review_manifest")()
            legacy_mixed = getattr(content, f"unit{number}_mixed_discrimination")()
            require(packaged_review == legacy_review, f"{unit_id} review manifest differs from legacy runtime")
            require(packaged_mixed == legacy_mixed, f"{unit_id} mixed discrimination differs from legacy runtime")
        review_count += len(packaged_review.get("targets", []))
        mixed_set_count += len(packaged_mixed.get("sets", []))

    for combined in sorted(resolved_object_ids):
        unit_id, object_id = combined.split(":", 1)
        packaged = course_packages.memory_object(COURSE_ID, unit_id, object_id)
        require(packaged is not None, f"package cannot resolve story Memory Object {combined}")

    require(
        (journey_count, scene_count, challenge_count, review_count, mixed_set_count) == (58, 448, 112, 887, 220),
        "AP Biology package totals drifted",
    )

    print("COURSE PACKAGE CONTRACT QA PASS")
    print(json.dumps({
        "course_id": COURSE_ID,
        "schema": course_packages.PACKAGE_SCHEMA,
        "units": 8,
        "journeys": journey_count,
        "scenes": scene_count,
        "challenge_lab_items": challenge_count,
        "review_targets": review_count,
        "mixed_sets": mixed_set_count,
        "story_object_references_resolved": len(resolved_object_ids),
        "legacy_runtime_equivalence": True,
    }, indent=2))


if __name__ == "__main__":
    main()
