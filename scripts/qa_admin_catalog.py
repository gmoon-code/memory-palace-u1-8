from __future__ import annotations

from pathlib import Path

from backend import admin_catalog

ROOT = Path(__file__).resolve().parents[1]
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

    require(summary["schema"] == "story-method-content-studio-catalog-1.0", "unexpected catalog schema")
    for key, expected in EXPECTED.items():
        record = summary["release_alignment"].get(key)
        require(record is not None, f"release alignment is missing {key}")
        require(record["actual"] == expected, f"{key} normalized total is {record['actual']}, expected {expected}")
        require(record["expected"] == expected, f"{key} frozen total is not {expected}")
        require(record["matches"], f"{key} does not match the frozen release")

    require(summary["health"]["error_count"] == 0, "catalog has blocking release-alignment errors")
    require(len(course_map["units"]) == 8, "course map does not contain all eight units")
    require(
        sum(unit["journey_count"] for unit in course_map["units"]) == 58,
        "course map journey total does not equal 58",
    )
    require(
        sum(unit["scene_count"] for unit in course_map["units"]) == 448,
        "course map scene total does not equal 448",
    )

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
        {item["type"] for item in unit8["matches"]} >= {"concept", "memory_object"},
        "Unit 8 shared concept/Memory Object resolution failed",
    )

    print("ADMIN CATALOG QA PASS")
    print("- frozen Unit 1-8 totals match the normalized catalog")
    print("- protected catalog APIs are read-only")
    print("- Course Map, search, health, and dependency inspector are wired")
    print(f"- unresolved source references are reported: {summary['unresolved_reference_count']}")


if __name__ == "__main__":
    main()
