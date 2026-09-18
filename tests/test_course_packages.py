from __future__ import annotations

import pytest

from backend import course_packages


def setup_function():
    course_packages.clear_package_cache()


def test_ap_biology_package_validates_and_matches_course_units():
    result = course_packages.validate_package("ap-biology")
    assert result["valid"] is True
    assert result["unit_count"] == 8
    assert result["errors"] == []

    course = course_packages.course("ap-biology")
    package = course_packages.package_manifest("ap-biology")
    assert [u["unit_id"] for u in course["units"]] == [u["unit_id"] for u in package["units"]]


def test_package_runtime_resolves_native_and_legacy_memory_object_formats():
    legacy_adapter = course_packages.memory_object("ap-biology", "unit-2", "U2-K-001")
    native = course_packages.memory_object("ap-biology", "unit-8", "U8-K-001")

    assert legacy_adapter is not None
    assert legacy_adapter["memory_object_id"] == "U2-K-001"
    assert legacy_adapter["canonical_term"]

    assert native is not None
    assert native["memory_object_id"] == "U8-K-001"
    assert native["canonical_term"]


def test_unit1_explicit_empty_review_adapters_are_returned():
    review = course_packages.review_manifest("ap-biology", "unit-1")
    mixed = course_packages.mixed_discrimination("ap-biology", "unit-1")

    assert review == {"unit_id": "unit-1", "target_count": 0, "targets": []}
    assert mixed == {
        "unit_id": "unit-1",
        "set_count": 0,
        "question_count": 0,
        "sets": [],
    }


def test_unknown_course_package_is_rejected():
    with pytest.raises(course_packages.CoursePackageError):
        course_packages.package_manifest("not-a-course")
