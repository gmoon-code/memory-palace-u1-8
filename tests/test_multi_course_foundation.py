from pathlib import Path
from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_course_registry_exposes_ap_biology_without_changing_curriculum():
    payload = client.get("/api/courses")
    assert payload.status_code == 200
    data = payload.json()
    assert data["platform_title"] == "The Story Method"
    assert data["registry_version"] == "1.0"
    assert len(data["courses"]) == 1
    course = data["courses"][0]
    assert course["course_id"] == "ap-biology"
    assert course["status"] == "available"
    assert course["student_visible"] is True
    assert course["unit_count"] == 8


def test_course_aware_routes_wrap_the_existing_ap_biology_runtime():
    course = client.get("/api/courses/ap-biology")
    assert course.status_code == 200
    assert course.json()["course_id"] == "ap-biology"
    assert len(course.json()["units"]) == 8

    units = client.get("/api/courses/ap-biology/units")
    assert units.status_code == 200
    assert units.json()["course_id"] == "ap-biology"
    assert len(units.json()["units"]) == 8

    unit = client.get("/api/courses/ap-biology/units/unit-8")
    assert unit.status_code == 200
    assert unit.json()["title"] == "Ecology"

    journeys = client.get("/api/courses/ap-biology/units/unit-3/journeys")
    assert journeys.status_code == 200
    assert journeys.json()["course_id"] == "ap-biology"
    assert len(journeys.json()["guided_journeys"]) == 7

    journey = client.get("/api/courses/ap-biology/units/unit-3/journeys/U3-J1")
    assert journey.status_code == 200

    obj = client.get("/api/courses/ap-biology/units/unit-3/objects/U3-K-001")
    assert obj.status_code == 200


def test_unknown_course_is_rejected_and_legacy_routes_remain_available():
    assert client.get("/api/courses/not-a-course").status_code == 404
    assert client.get("/api/courses/not-a-course/units").status_code == 404
    assert client.get("/api/course").status_code == 200
    assert client.get("/api/units/unit-8").status_code == 200


def test_student_progress_is_course_scoped_and_migrates_legacy_ap_biology_state():
    state_js = (Path(__file__).resolve().parents[1] / "frontend/js/state.js").read_text(encoding="utf-8")
    assert "story-method-v3:progress:" in state_js
    assert "memory-palace-v2:progress" in state_js
    assert "STATE_VERSION=5" in state_js
    assert "loadState(courseId=DEFAULT_COURSE_ID)" in state_js
    assert "clearCourseProgress(courseId=DEFAULT_COURSE_ID)" in state_js
