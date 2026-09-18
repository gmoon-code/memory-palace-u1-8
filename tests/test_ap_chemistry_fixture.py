from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_ap_chemistry_fixture_is_registered_but_hidden():
    response = client.get("/api/courses")
    assert response.status_code == 200
    course = next(item for item in response.json()["courses"] if item["course_id"] == "ap-chemistry")
    assert course["status"] == "development"
    assert course["student_visible"] is False
    assert course["unit_count"] == 2


def test_course_aware_student_api_can_load_hidden_fixture_for_architecture_qa():
    course = client.get("/api/courses/ap-chemistry")
    assert course.status_code == 200
    assert course.json()["course_id"] == "ap-chemistry"
    assert len(course.json()["units"]) == 2

    units = client.get("/api/courses/ap-chemistry/units")
    assert units.status_code == 200
    assert [item["unit_id"] for item in units.json()["units"]] == ["unit-1", "unit-2"]

    journeys = client.get("/api/courses/ap-chemistry/units/unit-1/journeys")
    assert journeys.status_code == 200
    assert [item["palace_id"] for item in journeys.json()["guided_journeys"]] == ["APCHEM-U1-J1"]

    journey = client.get("/api/courses/ap-chemistry/units/unit-1/journeys/APCHEM-U1-J1")
    assert journey.status_code == 200
    assert len(journey.json()["scenes"]) == 2

    obj = client.get("/api/courses/ap-chemistry/units/unit-1/objects/APCHEM-U1-K002")
    assert obj.status_code == 200
    assert obj.json()["canonical_term"] == "Average atomic mass"

    review = client.get("/api/courses/ap-chemistry/units/unit-1/review-manifest")
    assert review.status_code == 200
    assert review.json()["target_count"] == 4

    mixed = client.get("/api/courses/ap-chemistry/units/unit-2/mixed-discrimination")
    assert mixed.status_code == 200
    assert mixed.json()["set_count"] == 1

    lab = client.get("/api/courses/ap-chemistry/units/unit-2/application-lab")
    assert lab.status_code == 200
    assert lab.json()["challenge_count"] == 1


def test_course_namespace_blocks_cross_course_memory_object_resolution():
    chemistry = client.get("/api/courses/ap-chemistry/units/unit-1/objects/U1-K-001")
    assert chemistry.status_code == 404

    biology = client.get("/api/courses/ap-biology/units/unit-1/objects/APCHEM-U1-K001")
    assert biology.status_code == 404


def test_content_studio_lists_fixture_as_preparing_not_editable():
    from backend import admin_catalog

    payload = admin_catalog.catalog_courses()
    chemistry = next(item for item in payload["courses"] if item["course_id"] == "ap-chemistry")
    assert chemistry["catalog_ready"] is False
    assert chemistry["editable"] is False
