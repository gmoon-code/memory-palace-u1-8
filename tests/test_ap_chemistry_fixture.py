from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_ap_chemistry_foundation_is_registered_but_hidden():
    response = client.get("/api/courses")
    assert response.status_code == 200
    course = next(item for item in response.json()["courses"] if item["course_id"] == "ap-chemistry")
    assert course["status"] == "development"
    assert course["student_visible"] is False
    assert course["unit_count"] == 9


def test_course_aware_student_api_loads_hidden_nine_unit_foundation():
    course = client.get("/api/courses/ap-chemistry")
    assert course.status_code == 200
    body = course.json()
    assert body["course_id"] == "ap-chemistry"
    assert body["status"] == "PACKAGE_FOUNDATION"
    assert len(body["units"]) == 9
    assert sum(unit["topic_count"] for unit in body["units"]) == 91

    units = client.get("/api/courses/ap-chemistry/units")
    assert units.status_code == 200
    assert [item["unit_id"] for item in units.json()["units"]] == [f"unit-{n}" for n in range(1, 10)]
    assert units.json()["units"][1]["title"] == "Compound Structure and Properties"

    journeys = client.get("/api/courses/ap-chemistry/units/unit-1/journeys")
    assert journeys.status_code == 200
    assert journeys.json()["guided_journeys"] == []

    missing_journey = client.get("/api/courses/ap-chemistry/units/unit-1/journeys/APCHEM-U1-J1")
    assert missing_journey.status_code == 404

    missing_object = client.get("/api/courses/ap-chemistry/units/unit-1/objects/APCHEM-U1-K002")
    assert missing_object.status_code == 404

    review = client.get("/api/courses/ap-chemistry/units/unit-1/review-manifest")
    assert review.status_code == 200
    assert review.json()["target_count"] == 0

    mixed = client.get("/api/courses/ap-chemistry/units/unit-2/mixed-discrimination")
    assert mixed.status_code == 200
    assert mixed.json()["set_count"] == 0

    lab = client.get("/api/courses/ap-chemistry/units/unit-9/application-lab")
    assert lab.status_code == 200
    assert lab.json()["challenge_count"] == 0


def test_course_namespace_blocks_cross_course_memory_object_resolution():
    chemistry = client.get("/api/courses/ap-chemistry/units/unit-1/objects/U1-K-001")
    assert chemistry.status_code == 404

    biology = client.get("/api/courses/ap-biology/units/unit-1/objects/APCHEM-U1-K001")
    assert biology.status_code == 404


def test_content_studio_lists_foundation_as_read_only_catalog():
    from backend import admin_catalog

    payload = admin_catalog.catalog_courses()
    chemistry = next(item for item in payload["courses"] if item["course_id"] == "ap-chemistry")
    assert chemistry["catalog_ready"] is True
    assert chemistry["editable"] is False
    assert chemistry["catalog_mode"] == "read_only"
