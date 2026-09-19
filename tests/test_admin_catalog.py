from backend import admin_catalog


def setup_function():
    admin_catalog.clear_catalog_cache()


def test_catalog_matches_frozen_release_totals():
    summary = admin_catalog.catalog_summary()
    alignment = summary["release_alignment"]

    assert alignment["units"] == {"actual": 8, "expected": 8, "matches": True}
    assert alignment["journeys"] == {"actual": 58, "expected": 58, "matches": True}
    assert alignment["scenes"] == {"actual": 448, "expected": 448, "matches": True}
    assert alignment["canonical_records"] == {
        "actual": 1561,
        "expected": 1561,
        "matches": True,
    }
    assert alignment["challenge_lab_items"] == {
        "actual": 112,
        "expected": 112,
        "matches": True,
    }
    assert summary["health"]["error_count"] == 0


def test_catalog_normalizes_known_unit1_scene_and_memory_object():
    snapshot = admin_catalog.catalog()
    entities = snapshot["entities"]

    scene_id = "scene:unit-1:Z1:0"
    memory_id = "memory:unit-1:MO-APBIO-U1-P003"
    assert scene_id in entities
    assert memory_id in entities
    assert entities[scene_id]["title"] == "The Light That Should Not Be There"
    assert entities[memory_id]["canonical_term"] == "Hypothesis"

    report = admin_catalog.dependency_report(scene_id, depth=2)
    assert report is not None
    linked_ids = {item["entity"]["id"] for item in report["related"]}
    assert memory_id in linked_ids


def test_unit8_reference_resolves_to_canonical_concept():
    result = admin_catalog.resolve_reference("unit-8", "U8-K-063")
    types = {item["type"] for item in result["matches"]}
    assert "concept" in types


def test_course_map_preserves_all_units_journeys_and_scenes():
    course_map = admin_catalog.course_map()
    assert len(course_map["units"]) == 8
    assert sum(unit["journey_count"] for unit in course_map["units"]) == 58
    assert sum(unit["scene_count"] for unit in course_map["units"]) == 448

    unit8 = next(unit for unit in course_map["units"] if unit["unit_id"] == "unit-8")
    assert unit8["journey_count"] == 8
    assert unit8["scene_count"] == 58
    first_scene = unit8["journeys"][0]["scenes"][0]
    assert first_scene["id"] == "scene:unit-8:U8-J1:0"
    assert first_scene["locus_id"] == "U8-L01"


def test_search_and_dependency_report_expose_linked_content():
    search = admin_catalog.search_entities("Hypothesis", unit_id="unit-1", limit=20)
    assert search["items"]
    assert any(item["type"] == "memory_object" for item in search["items"])

    report = admin_catalog.dependency_report(
        "memory:unit-1:MO-APBIO-U1-P003",
        depth=2,
    )
    assert report is not None
    assert report["direct_inbound"]
    assert report["direct_outbound"]


def test_catalog_is_read_only_data_projection():
    summary = admin_catalog.catalog_summary()
    assert summary["schema"] == admin_catalog.CATALOG_SCHEMA
    assert "draft" not in summary
    assert "publish" not in summary


def test_catalog_course_registry_and_scope_are_explicit():
    courses = admin_catalog.catalog_courses()
    ap_biology = next(item for item in courses["courses"] if item["course_id"] == "ap-biology")
    assert ap_biology["catalog_ready"] is True
    assert ap_biology["editable"] is True

    summary = admin_catalog.catalog_summary("ap-biology")
    assert summary["course_id"] == "ap-biology"
    assert summary["course_title"] == "AP Biology"

    snapshot = admin_catalog.catalog("ap-biology")
    assert snapshot["course_id"] == "ap-biology"
    assert all(entity.get("course_id") == "ap-biology" for entity in snapshot["entities"].values())


def test_development_course_catalog_is_read_only_and_isolated():
    courses = admin_catalog.catalog_courses()
    chemistry = next(item for item in courses["courses"] if item["course_id"] == "ap-chemistry")
    assert chemistry["catalog_ready"] is True
    assert chemistry["editable"] is False
    assert chemistry["catalog_mode"] == "read_only"

    summary = admin_catalog.catalog_summary("ap-chemistry")
    assert summary["course_id"] == "ap-chemistry"
    assert summary["course_title"] == "AP Chemistry"
    assert summary["counts"]["unit"] == 2
    assert summary["counts"]["journey"] == 2
    assert summary["counts"]["scene"] == 4
    assert summary["counts"]["concept"] == 8
    assert summary["counts"]["memory_object"] == 8

    snapshot = admin_catalog.catalog("ap-chemistry")
    assert all(entity.get("course_id") == "ap-chemistry" for entity in snapshot["entities"].values())

    try:
        admin_catalog.require_editable_course("ap-chemistry")
    except ValueError as exc:
        assert "editing is not enabled" in str(exc)
    else:
        raise AssertionError("development course catalog must remain read only")
