from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

from .settings import ROOT


PACKAGE_SCHEMA = "story-method-course-package-1.0"
PACKAGE_DIR = ROOT / "platform" / "course-packages"


class CoursePackageError(ValueError):
    pass


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_repo_path(raw: str) -> Path:
    if not isinstance(raw, str) or not raw.strip():
        raise CoursePackageError("Course package path is missing")
    candidate = (ROOT / raw).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise CoursePackageError(f"Course package path escapes repository root: {raw}") from exc
    return candidate


def _repo_relative_posix(path: Path) -> str:
    """Return a repository-relative path with forward slashes on every OS."""
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError as exc:
        raise CoursePackageError(f"Path escapes repository root: {path}") from exc


@lru_cache(maxsize=32)
def package_manifest(course_id: str) -> dict[str, Any]:
    path = PACKAGE_DIR / f"{course_id}.json"
    if not path.is_file():
        raise CoursePackageError(f"Course package is not available for '{course_id}'")
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise CoursePackageError(f"Course package for '{course_id}' is not an object")
    if payload.get("schema") != PACKAGE_SCHEMA:
        raise CoursePackageError(f"Course package for '{course_id}' uses an unsupported schema")
    if payload.get("course_id") != course_id:
        raise CoursePackageError(f"Course package id mismatch for '{course_id}'")
    return payload


def unit_package(course_id: str, unit_id: str) -> dict[str, Any]:
    manifest = package_manifest(course_id)
    unit = next(
        (item for item in manifest.get("units", []) if isinstance(item, dict) and item.get("unit_id") == unit_id),
        None,
    )
    if unit is None:
        raise CoursePackageError(f"Unit '{unit_id}' is not declared in course package '{course_id}'")
    return unit


def _unit_manifest(course_id: str, unit_id: str) -> dict[str, Any]:
    return unit_package(course_id, unit_id)


def artifact_spec(course_id: str, unit_id: str, artifact_name: str) -> dict[str, Any]:
    unit = unit_package(course_id, unit_id)
    spec = unit.get(artifact_name)
    if not isinstance(spec, dict):
        raise CoursePackageError(
            f"Unit '{unit_id}' in course '{course_id}' has no artifact declaration '{artifact_name}'"
        )
    return spec


def artifact_source_path(course_id: str, unit_id: str, artifact_name: str) -> str | None:
    spec = artifact_spec(course_id, unit_id, artifact_name)
    path = spec.get("path")
    return str(path) if isinstance(path, str) and path else None


def journey_source_path(course_id: str, unit_id: str, journey_id: str) -> str:
    spec = unit_package(course_id, unit_id)["journeys"]
    filename = str(spec["filename_template"]).replace("{journey_id}", journey_id)
    return f"{str(spec['directory']).rstrip('/')}/{filename}"


def _artifact_payload(spec: dict[str, Any]) -> Any:
    mode = spec.get("mode")
    if mode == "empty":
        payload = spec.get("empty_payload")
        if not isinstance(payload, dict):
            raise CoursePackageError("Empty artifact is missing empty_payload")
        return dict(payload)
    if mode != "file":
        raise CoursePackageError(f"Unsupported artifact mode: {mode}")
    path = _safe_repo_path(str(spec.get("path") or ""))
    if not path.is_file():
        raise CoursePackageError(f"Course package artifact is missing: {_repo_relative_posix(path)}")
    payload = _read_json(path)
    if not isinstance(payload, (dict, list)):
        raise CoursePackageError(f"Expected JSON object or list artifact at {_repo_relative_posix(path)}")
    return payload


def _records(payload: Any, keys: list[str] | tuple[str, ...]) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in keys:
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def _first(record: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in record and record[key] not in (None, ""):
            return record[key]
    return default


def _canonical_as_memory_object(record: dict[str, Any]) -> dict[str, Any]:
    knowledge_id = str(_first(record, "knowledge_id", "Knowledge ID", "id", default=""))
    term = _first(record, "canonical_label", "Canonical Label", "canonical_term", "term", default=knowledge_id)
    definition = _first(
        record,
        "canonical_verified_statement",
        "Canonical Verified Statement",
        "canonical_definition",
        "definition",
        default="",
    )
    exact = _first(record, "exact_name_recall", "Exact Name Recall", "exact_name_required", default=False)
    if isinstance(exact, str):
        exact = exact.strip().upper() in {"YES", "TRUE", "REQUIRED"}
    return {
        "memory_object_id": knowledge_id,
        "source_knowledge_id": knowledge_id,
        "canonical_term": term,
        "canonical_definition": definition,
        "exact_name_recall": bool(exact),
        "source_reference": _first(record, "source_reference", "Source Reference", default=""),
        "canonical_lock": _first(record, "canonical_lock", "Canonical Lock", default=""),
    }


def course(course_id: str) -> dict[str, Any]:
    manifest = package_manifest(course_id)
    path = _safe_repo_path(manifest["course_file"])
    if not path.is_file():
        raise CoursePackageError(f"Course metadata is missing for '{course_id}'")
    payload = _read_json(path)
    if not isinstance(payload, dict):
        raise CoursePackageError(f"Course metadata is invalid for '{course_id}'")
    if payload.get("course_id") != course_id:
        raise CoursePackageError(f"Course metadata id mismatch for '{course_id}'")
    return payload


def unit(course_id: str, unit_id: str) -> dict[str, Any] | None:
    return next((item for item in course(course_id).get("units", []) if item.get("unit_id") == unit_id), None)


def journeys(course_id: str, unit_id: str) -> dict[str, Any]:
    spec = _unit_manifest(course_id, unit_id)["journeys"]
    path = _safe_repo_path(spec["registry_path"])
    payload = _read_json(path)
    guided = payload.get(spec.get("collection_key", "guided_journeys"), []) if isinstance(payload, dict) else []
    if not isinstance(guided, list):
        raise CoursePackageError(f"Journey registry is malformed for {course_id}/{unit_id}")
    return {"course_id": course_id, "unit_id": unit_id, "guided_journeys": guided}


def journey(course_id: str, unit_id: str, journey_id: str) -> dict[str, Any] | None:
    spec = _unit_manifest(course_id, unit_id)["journeys"]
    filename = str(spec["filename_template"]).replace("{journey_id}", journey_id)
    path = _safe_repo_path(f"{spec['directory'].rstrip('/')}/{filename}")
    if not path.is_file():
        return None
    payload = _read_json(path)
    return payload if isinstance(payload, dict) else None


def artifact_records(course_id: str, unit_id: str, artifact_name: str) -> list[dict[str, Any]]:
    spec = artifact_spec(course_id, unit_id, artifact_name)
    payload = _artifact_payload(spec)
    keys = spec.get("collection_keys") or ["records", "items"]
    return _records(payload, keys)


def memory_objects(course_id: str, unit_id: str) -> list[dict[str, Any]]:
    spec = artifact_spec(course_id, unit_id, "memory_objects")
    records = artifact_records(course_id, unit_id, "memory_objects")
    if spec.get("format") == "canonical_catalog_as_memory_objects":
        return [_canonical_as_memory_object(record) for record in records]
    return [dict(record) for record in records]


def memory_object(course_id: str, unit_id: str, object_id: str) -> dict[str, Any] | None:
    for record in memory_objects(course_id, unit_id):
        record_id = _first(record, "memory_object_id", "object_id", "knowledge_id", "Knowledge ID")
        if str(record_id or "") == object_id:
            return record
    return None


def review_manifest(course_id: str, unit_id: str) -> dict[str, Any]:
    return _artifact_payload(_unit_manifest(course_id, unit_id)["review"])


def mixed_discrimination(course_id: str, unit_id: str) -> dict[str, Any]:
    return _artifact_payload(_unit_manifest(course_id, unit_id)["mixed_discrimination"])


def application_lab(course_id: str, unit_id: str) -> dict[str, Any]:
    return _artifact_payload(_unit_manifest(course_id, unit_id)["challenge_lab"])


def validate_package(course_id: str) -> dict[str, Any]:
    manifest = package_manifest(course_id)
    errors: list[str] = []
    warnings: list[str] = []
    course_payload: dict[str, Any] = {}

    try:
        course_payload = course(course_id)
    except Exception as exc:
        errors.append(str(exc))
        return {"course_id": course_id, "valid": False, "errors": errors, "warnings": warnings}

    expected_units = [
        str(item.get("unit_id"))
        for item in course_payload.get("units", [])
        if isinstance(item, dict) and item.get("unit_id")
    ]
    package_units = [
        str(item.get("unit_id"))
        for item in manifest.get("units", [])
        if isinstance(item, dict) and item.get("unit_id")
    ]
    if package_units != expected_units:
        errors.append("Course package unit order or membership does not match course.json")

    for unit_spec in manifest.get("units", []):
        if not isinstance(unit_spec, dict):
            errors.append("Course package contains a non-object unit entry")
            continue
        unit_id = str(unit_spec.get("unit_id") or "")
        content_root = str(unit_spec.get("content_root") or "")
        if not content_root.startswith(f"content/{course_id}/"):
            errors.append(f"{unit_id} content_root is outside course namespace")

        try:
            registry = journeys(course_id, unit_id)
            declared = next((u for u in course_payload.get("units", []) if u.get("unit_id") == unit_id), {})
            expected_count = int(declared.get("journey_count") or 0)
            if len(registry["guided_journeys"]) != expected_count:
                errors.append(
                    f"{unit_id} journey count mismatch: package has {len(registry['guided_journeys'])}, course.json declares {expected_count}"
                )
            for meta in registry["guided_journeys"]:
                journey_id = str(meta.get("palace_id") or "")
                if not journey_id:
                    errors.append(f"{unit_id} journey registry contains a record without palace_id")
                    continue
                if journey(course_id, unit_id, journey_id) is None:
                    errors.append(f"{unit_id} journey file missing for {journey_id}")
        except Exception as exc:
            errors.append(f"{unit_id} journeys: {exc}")

        for artifact_name in ("concepts", "memory_objects", "review", "mixed_discrimination", "challenge_lab"):
            spec = unit_spec.get(artifact_name)
            if not isinstance(spec, dict):
                errors.append(f"{unit_id} is missing artifact declaration '{artifact_name}'")
                continue
            if spec.get("mode") == "file":
                try:
                    path = _safe_repo_path(str(spec.get("path") or ""))
                    if not path.is_file():
                        errors.append(f"{unit_id} artifact missing: {artifact_name} -> {spec.get('path')}")
                    elif not _repo_relative_posix(path).startswith(f"content/{course_id}/"):
                        errors.append(f"{unit_id} artifact escapes course namespace: {artifact_name}")
                except Exception as exc:
                    errors.append(f"{unit_id} {artifact_name}: {exc}")
            elif spec.get("mode") == "empty":
                if not isinstance(spec.get("empty_payload"), dict):
                    errors.append(f"{unit_id} empty artifact lacks payload: {artifact_name}")
            else:
                errors.append(f"{unit_id} artifact has unsupported mode: {artifact_name}")

    return {
        "course_id": course_id,
        "schema": manifest.get("schema"),
        "unit_count": len(package_units),
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
    }


def clear_package_cache() -> None:
    package_manifest.cache_clear()
