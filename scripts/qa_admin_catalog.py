from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend import admin_catalog

EXPECTED = {
    "units": 8,
    "journeys": 58,
    "scenes": 448,
    "canonical_records": 1561,
    "challenge_lab_items": 112,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ADMIN CATALOG QA FAIL\n- {message}")


def main() -> None:
    admin_catalog.clear_catalog_cache()
    summary = admin_catalog.catalog_summary()
    course_map = admin_catalog.course_map()
    main_py = (ROOT / "backend" / "main.py").read_text(encoding="utf-8")
    admin_js = (ROOT / "frontend" / "admin" / "admin.js").read_text(encoding="utf-8")

    require(summary["schema"] == "story-method-content-studio-catalog-1.1", "unexpected catalog schema")
    require(summary["course_id"] == "ap-biology", "catalog summary lost AP Biology course identity")
    require(course_map["course_id"] == "ap-biology", "course map lost AP Biology course identity")
    for key, expected in EXPECTED.items():
        record = summary["release_alignment"].get(key)
        require(record is not None, f"release alignment is missing {key}")
        require(record["actual"] == expected, f"{key} normalized total is {record['actual']}, expected {expected}")
        require(record["expected"] == expected, f"{key} frozen total is not {expected}")
        require(record["matches"], f"{key} does not match the frozen release")

    require(summary["health"]["error_count"] == 0, "catalog has blocking release-alignment errors")
    courses = admin_catalog.catalog_courses()
    chemistry_record = next(item for item in courses["courses"] if item["course_id"] == "ap-chemistry")
    require(chemistry_record["catalog_ready"] is True, "AP Chemistry package did not become catalog ready")
    require(chemistry_record["editable"] is False, "development AP Chemistry fixture unexpectedly became editable")
    require(chemistry_record["catalog_mode"] == "read_only", "AP Chemistry fixture is not marked read only")

    chemistry = admin_catalog.catalog_summary("ap-chemistry")
    require(chemistry["course_id"] == "ap-chemistry", "chemistry catalog lost course identity")
    require(chemistry["counts"].get("unit") == 2, "chemistry catalog does not contain two fixture units")
    require(chemistry["counts"].get("journey") == 2, "chemistry catalog does not contain two fixture journeys")
    require(chemistry["counts"].get("scene") == 4, "chemistry catalog does not contain four fixture scenes")
    require(chemistry["counts"].get("concept") == 8, "chemistry catalog does not contain eight fixture concepts")
    require(chemistry["counts"].get("memory_object") == 8, "chemistry catalog does not contain eight fixture Memory Objects")
    require(chemistry["unresolved_reference_count"] == 0, "chemistry catalog has unresolved fixture references")

    chemistry_snapshot = admin_catalog.catalog("ap-chemistry")
    require(
        all(entity.get("course_id") == "ap-chemistry" for entity in chemistry_snapshot["entities"].values()),
        "chemistry catalog contains an entity from another course",
    )
    chemistry_scenes = [
        entity for entity in chemistry_snapshot["entities"].values() if entity.get("type") == "scene"
    ]
    require(
        chemistry_scenes and all(str(entity.get("source_path") or "").startswith("content/ap-chemistry/") for entity in chemistry_scenes),
        "chemistry scene source paths escaped the chemistry namespace",
    )
    try:
        admin_catalog.require_editable_course("ap-chemistry")
    except ValueError:
        pass
    else:
        require(False, "development chemistry catalog did not enforce its write lock")
    require(len(course_map["units"]) == 8, "course map does not contain all eight units")
    require(
        sum(unit["journey_count"] for unit in course_map["units"]) == 58,
        "course map journey total does not equal 58",
    )
    require(
        sum(unit["scene_count"] for unit in course_map["units"]) == 448,
        "course map scene total does not equal 448",
    )

    require('/api/admin/courses' in main_py, "protected course registry route is missing")
    required_routes = [
        '/api/admin/catalog/summary',
        '/api/admin/catalog/course-map',
        '/api/admin/catalog/entities',
        '/api/admin/catalog/search',
        '/api/admin/catalog/resolve',
        '/api/admin/catalog/entity',
        '/api/admin/catalog/dependencies',
        '/api/admin/catalog/health',
    ]
    for route in required_routes:
        require(route in main_py, f"protected catalog route is missing: {route}")
    require('@app.post("/api/admin/catalog/' not in main_py, "Step 3 unexpectedly exposes a catalog write endpoint")
    require('@app.put("/api/admin/catalog/' not in main_py, "Step 3 unexpectedly exposes a catalog PUT endpoint")
    require('@app.patch("/api/admin/catalog/' not in main_py, "Step 3 unexpectedly exposes a catalog PATCH endpoint")
    require('@app.delete("/api/admin/catalog/' not in main_py, "Step 3 unexpectedly exposes a catalog DELETE endpoint")

    require("/api/admin/catalog/course-map" in admin_js, "admin UI is not connected to the normalized course map")
    require("/api/admin/catalog/dependencies" in admin_js, "admin UI is not connected to dependency inspection")
    require("/api/admin/catalog/search" in admin_js, "admin UI is not connected to catalog search")
    require("/api/admin/catalog/summary" in admin_js, "admin dashboard is not connected to catalog health")

    hypothesis = admin_catalog.resolve_reference("unit-1", "MO-APBIO-U1-P003")
    require(
        any(item["type"] == "memory_object" for item in hypothesis["matches"]),
        "Unit 1 Memory Object alias resolution failed",
    )
    unit8 = admin_catalog.resolve_reference("unit-8", "U8-K-063")
    require(
        any(item["type"] == "concept" for item in unit8["matches"]),
        "Unit 8 canonical concept resolution failed",
    )

    print("ADMIN CATALOG QA PASS")
    print("- frozen Unit 1-8 totals match the normalized catalog")
    print("- protected catalog APIs are read-only and course scoped")
    print("- Course Map, search, health, and dependency inspector are wired")
    print("- AP Chemistry read-only catalog is isolated from AP Biology")
    print(f"- unresolved source references are reported: {summary['unresolved_reference_count']}")


if __name__ == "__main__":
    main()
