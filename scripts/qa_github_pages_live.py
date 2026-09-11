from __future__ import annotations

import argparse
import json
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

EXPECTED = {
    "units": 8,
    "journeys": 58,
    "scenes": 448,
    "quick_recalls": 152,
    "challenge_lab_items": 112,
    "review_targets": 887,
    "mixed_sets": 220,
    "mixed_questions": 600,
}


def fetch_bytes(base: str, path: str, version: str, attempts: int = 12) -> bytes:
    url = f"{base.rstrip('/')}/{path.lstrip('/')}"
    separator = "&" if "?" in url else "?"
    url = f"{url}{separator}{urlencode({'v': version})}"
    error: Exception | None = None
    for attempt in range(attempts):
        try:
            request = Request(
                url,
                headers={
                    "Accept": "application/json,text/html,text/css,*/*",
                    "Cache-Control": "no-cache",
                    "Pragma": "no-cache",
                    "User-Agent": "memory-palace-live-qa/1.0",
                },
            )
            with urlopen(request, timeout=20) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status} for {url}")
                return response.read()
        except (HTTPError, URLError, TimeoutError, RuntimeError) as exc:
            error = exc
            if attempt + 1 < attempts:
                time.sleep(min(2 + attempt, 8))
    raise RuntimeError(f"LIVE PAGES QA FAIL · could not fetch {url}: {error}")


def fetch_text(base: str, path: str, version: str) -> str:
    return fetch_bytes(base, path, version).decode("utf-8")


def fetch_json(base: str, path: str, version: str):
    try:
        return json.loads(fetch_text(base, path, version))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"LIVE PAGES QA FAIL · invalid JSON at {path}: {exc}") from exc


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(f"LIVE PAGES QA FAIL · {message}")


def object_ids_for_unit(base: str, unit_id: str, version: str) -> set[str]:
    prefix = f"content/ap-biology/{unit_id}"
    if unit_id == "unit-1":
        data = fetch_json(base, f"{prefix}/memory-objects.json", version)
        return {item["memory_object_id"] for item in data.get("memory_objects", [])}
    if unit_id in {"unit-2", "unit-3"}:
        compact = unit_id.replace("unit-", "unit")
        data = fetch_json(base, f"{prefix}/source/canonical-{compact}-f1.json", version)
        return {item["knowledge_id"] for item in data.get("canonical_catalog", [])}
    data = fetch_json(base, f"{prefix}/memory-objects-f5.json", version)
    return {item["memory_object_id"] for item in data.get("memory_objects", [])}


def run(base: str, version: str) -> None:
    index = fetch_text(base, "", version)
    ensure("Memory Palace" in index, "production root does not contain the Memory Palace shell")
    ensure("./frontend/js/app.js" in index, "production root does not reference the Pages application module")
    ensure("./frontend/css/base.css" in index, "production root does not reference the Pages stylesheet")

    app_js = fetch_text(base, "frontend/js/app.js", version)
    api_js = fetch_text(base, "frontend/js/api.js", version)
    css = fetch_text(base, "frontend/css/app.css", version)
    ensure("from './api.js'" in app_js, "production app.js is not the expected student controller")
    ensure("STATIC_MODE" in api_js and "staticApi" in api_js, "production api.js does not contain the static adapter")
    ensure(".story-shell" in css, "production CSS is missing the story layout")

    course = fetch_json(base, "content/ap-biology/course.json", version)
    units = course.get("units", [])
    ensure(len(units) == EXPECTED["units"], f"expected 8 units, got {len(units)}")
    ensure(all(unit.get("status") == "STUDENT_READY" for unit in units), "a production unit is not STUDENT_READY")

    totals = {
        "units": len(units),
        "journeys": 0,
        "scenes": 0,
        "quick_recalls": 0,
        "challenge_lab_items": 0,
        "review_targets": 0,
        "mixed_sets": 0,
        "mixed_questions": 0,
    }
    resolved_objects = 0

    for unit in units:
        unit_id = unit["unit_id"]
        prefix = f"content/ap-biology/{unit_id}"
        registry_name = "journeys.json" if unit_id == "unit-1" else "journeys-f5.json"
        registry = fetch_json(base, f"{prefix}/{registry_name}", version)
        journeys = registry.get("guided_journeys", [])
        ensure(len(journeys) == int(unit.get("journey_count", 0)), f"{unit_id} journey count mismatch")
        totals["journeys"] += len(journeys)

        available_objects = object_ids_for_unit(base, unit_id, version)
        referenced_objects: set[str] = set()
        for meta in journeys:
            palace_id = meta["palace_id"]
            journey = fetch_json(base, f"{prefix}/journeys/{quote(palace_id)}.json", version)
            ensure(journey.get("palace_id") == palace_id, f"{unit_id}/{palace_id} palace ID mismatch")
            scenes = journey.get("scenes", [])
            ensure(len(scenes) == int(meta.get("scene_count", 0)), f"{unit_id}/{palace_id} scene count mismatch")
            totals["scenes"] += len(scenes)
            for scene in scenes:
                if scene.get("checkpoint"):
                    totals["quick_recalls"] += 1
                    if scene.get("checkpoint_object_id"):
                        referenced_objects.add(scene["checkpoint_object_id"])
                for beat in scene.get("story_beats", []):
                    if beat.get("object_id"):
                        referenced_objects.add(beat["object_id"])

        missing = sorted(referenced_objects - available_objects)
        ensure(not missing, f"{unit_id} has unresolved story Memory Objects: {missing[:8]}")
        resolved_objects += len(referenced_objects)

        lab = fetch_json(base, f"{prefix}/application-lab.json", version)
        totals["challenge_lab_items"] += len(lab.get("items", []))

        if unit_id != "unit-1":
            review = fetch_json(base, f"{prefix}/review-manifest-f5.json", version)
            mixed = fetch_json(base, f"{prefix}/mixed-discrimination-f5.json", version)
            totals["review_targets"] += len(review.get("targets", []))
            sets = mixed.get("sets", [])
            totals["mixed_sets"] += len(sets)
            totals["mixed_questions"] += sum(len(item.get("questions", [])) for item in sets)

    for key, expected in EXPECTED.items():
        ensure(totals[key] == expected, f"expected {expected} {key}, got {totals[key]}")

    print("GITHUB PAGES LIVE PRODUCTION QA PASS")
    print(json.dumps({"base_url": base.rstrip("/") + "/", "deployment_sha": version, **totals, "story_objects_resolved": resolved_objects}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    run(args.base_url, args.version)


if __name__ == "__main__":
    main()
