from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend import content, course_packages


COURSE_ID = "ap-chemistry"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"AP CHEMISTRY FIXTURE QA FAIL\n- {message}")


def main() -> None:
    registry = content.course_registry()
    record = next((item for item in registry["courses"] if item.get("course_id") == COURSE_ID), None)
    require(record is not None, "AP Chemistry is not registered")
    require(record.get("status") == "development", "fixture course must remain development-only")
    require(record.get("student_visible") is False, "fixture course must remain hidden from students")

    result = course_packages.validate_package(COURSE_ID)
    require(result["valid"], "; ".join(result["errors"]))

    course = course_packages.course(COURSE_ID)
    require(len(course.get("units", [])) == 2, "fixture must expose exactly two units")

    totals = {"journeys": 0, "scenes": 0, "memory_objects": 0, "review_targets": 0, "mixed_sets": 0, "challenge_items": 0}
    for unit in course["units"]:
        unit_id = unit["unit_id"]
        registry_payload = course_packages.journeys(COURSE_ID, unit_id)
        require(len(registry_payload["guided_journeys"]) == 1, f"{unit_id} must contain one fixture journey")
        totals["journeys"] += 1

        meta = registry_payload["guided_journeys"][0]
        journey = course_packages.journey(COURSE_ID, unit_id, meta["palace_id"])
        require(journey is not None, f"{unit_id} fixture journey is missing")
        require(len(journey.get("scenes", [])) == 2, f"{unit_id} must contain two fixture scenes")
        totals["scenes"] += len(journey["scenes"])

        ids: set[str] = set()
        for scene in journey["scenes"]:
            for beat in scene.get("story_beats", []) or []:
                object_id = beat.get("object_id")
                if object_id:
                    ids.add(object_id)
            checkpoint_id = scene.get("checkpoint_object_id")
            if checkpoint_id:
                ids.add(checkpoint_id)

        for object_id in ids:
            obj = course_packages.memory_object(COURSE_ID, unit_id, object_id)
            require(obj is not None, f"{unit_id} cannot resolve {object_id}")
        totals["memory_objects"] += len(ids)

        review = course_packages.review_manifest(COURSE_ID, unit_id)
        mixed = course_packages.mixed_discrimination(COURSE_ID, unit_id)
        lab = course_packages.application_lab(COURSE_ID, unit_id)
        totals["review_targets"] += len(review.get("targets", []))
        totals["mixed_sets"] += len(mixed.get("sets", []))
        totals["challenge_items"] += len(lab.get("items", []))

    require(
        totals == {
            "journeys": 2,
            "scenes": 4,
            "memory_objects": 8,
            "review_targets": 8,
            "mixed_sets": 2,
            "challenge_items": 2,
        },
        f"fixture totals drifted: {totals}",
    )

    print("AP CHEMISTRY FIXTURE QA PASS")
    print(json.dumps({"course_id": COURSE_ID, "hidden": True, "development_only": True, **totals}, indent=2))


if __name__ == "__main__":
    main()
