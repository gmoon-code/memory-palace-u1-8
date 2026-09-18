from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def copy_file(src: Path, dst: Path) -> None:
    if not src.is_file():
        raise SystemExit(f"GITHUB PAGES BUILD REFUSED: required file missing: {src.relative_to(ROOT)}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path) -> None:
    if not src.is_dir():
        raise SystemExit(f"GITHUB PAGES BUILD REFUSED: required directory missing: {src.relative_to(ROOT)}")
    shutil.copytree(src, dst)


def repo_path(relative: str) -> Path:
    path = (ROOT / relative).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError as exc:
        raise SystemExit(f"GITHUB PAGES BUILD REFUSED: package path escapes repository: {relative}") from exc
    return path


def copy_relative(relative: str, output: Path) -> None:
    copy_file(repo_path(relative), output / relative)


def load_json(relative: str):
    path = repo_path(relative)
    if not path.is_file():
        raise SystemExit(f"GITHUB PAGES BUILD REFUSED: required JSON missing: {relative}")
    return json.loads(path.read_text(encoding="utf-8"))


def build_course(course_record: dict, output: Path) -> dict:
    course_id = str(course_record.get("course_id") or "")
    package_path = str(course_record.get("package_manifest") or "")
    if not course_id or not package_path:
        raise SystemExit("GITHUB PAGES BUILD REFUSED: available course is missing course_id or package_manifest")

    package = load_json(package_path)
    if package.get("schema") != "story-method-course-package-1.0":
        raise SystemExit(f"GITHUB PAGES BUILD REFUSED: unsupported package schema for {course_id}")
    if package.get("course_id") != course_id:
        raise SystemExit(f"GITHUB PAGES BUILD REFUSED: package id mismatch for {course_id}")

    course_file = str(package.get("course_file") or "")
    copy_relative(course_file, output)
    course = load_json(course_file)
    units = [item for item in course.get("units", []) if isinstance(item, dict)]
    package_units = [item for item in package.get("units", []) if isinstance(item, dict)]

    course_unit_ids = [str(item.get("unit_id") or "") for item in units]
    package_unit_ids = [str(item.get("unit_id") or "") for item in package_units]
    if course_unit_ids != package_unit_ids:
        raise SystemExit(f"GITHUB PAGES BUILD REFUSED: package units do not match course metadata for {course_id}")

    if course_id == "ap-biology":
        if len(units) != 8 or any(unit.get("status") != "STUDENT_READY" for unit in units):
            raise SystemExit("GITHUB PAGES BUILD REFUSED: AP Biology is not the frozen 8-unit student release")

    journey_count = 0
    journey_files = 0
    for unit, unit_package in zip(units, package_units, strict=True):
        unit_id = str(unit["unit_id"])
        journeys = unit_package.get("journeys") or {}
        registry_path = str(journeys.get("registry_path") or "")
        copy_relative(registry_path, output)
        registry = load_json(registry_path)
        collection_key = str(journeys.get("collection_key") or "guided_journeys")
        guided = registry.get(collection_key, []) if isinstance(registry, dict) else []
        if not isinstance(guided, list):
            raise SystemExit(f"GITHUB PAGES BUILD REFUSED: malformed journey registry for {course_id}/{unit_id}")
        expected = int(unit.get("journey_count", 0))
        if len(guided) != expected:
            raise SystemExit(
                f"GITHUB PAGES BUILD REFUSED: {course_id}/{unit_id} journey registry expected {expected}, got {len(guided)}"
            )
        journey_count += len(guided)

        directory = str(journeys.get("directory") or "").rstrip("/")
        template = str(journeys.get("filename_template") or "{journey_id}.json")
        for journey in guided:
            journey_id = str(journey.get("palace_id") or "")
            if not journey_id:
                raise SystemExit(f"GITHUB PAGES BUILD REFUSED: {course_id}/{unit_id} journey lacks palace_id")
            relative = f"{directory}/{template.replace('{journey_id}', journey_id)}"
            copy_relative(relative, output)
            journey_files += 1

        for artifact_name in ("memory_objects", "review", "mixed_discrimination", "challenge_lab"):
            spec = unit_package.get(artifact_name) or {}
            mode = spec.get("mode")
            if mode == "file":
                copy_relative(str(spec.get("path") or ""), output)
            elif mode != "empty":
                raise SystemExit(
                    f"GITHUB PAGES BUILD REFUSED: unsupported {artifact_name} mode for {course_id}/{unit_id}"
                )

    if course_id == "ap-biology" and (journey_count != 58 or journey_files != 58):
        raise SystemExit(
            f"GITHUB PAGES BUILD REFUSED: expected 58 AP Biology journeys, got registry={journey_count}, files={journey_files}"
        )

    return {
        "course_id": course_id,
        "units": len(units),
        "journeys": journey_count,
        "journey_files": journey_files,
    }


def build(output: Path) -> None:
    output = output.resolve()
    if output == ROOT or ROOT in output.parents:
        raise SystemExit("GITHUB PAGES BUILD REFUSED: output must be outside the repository tree")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    copy_file(ROOT / "index.html", output / "index.html")
    copy_file(ROOT / ".nojekyll", output / ".nojekyll")
    copy_tree(ROOT / "frontend" / "css", output / "frontend" / "css")
    copy_tree(ROOT / "frontend" / "js", output / "frontend" / "js")
    copy_tree(ROOT / "platform", output / "platform")

    registry = load_json("platform/courses.json")
    available = [
        item
        for item in registry.get("courses", [])
        if isinstance(item, dict)
        and item.get("student_visible") is not False
        and item.get("status") == "available"
    ]
    if not available:
        raise SystemExit("GITHUB PAGES BUILD REFUSED: no student-visible available courses are registered")

    built = [build_course(course_record, output) for course_record in available]

    prohibited_suffixes = {".pdf", ".xlsx", ".xls", ".docx", ".zip", ".sqlite", ".sqlite3", ".py", ".pyc"}
    prohibited_names = {".git", ".env", "__pycache__", ".pytest_cache"}
    files = [p for p in output.rglob("*") if p.is_file()]
    bad = [p for p in files if p.suffix.lower() in prohibited_suffixes or any(part in prohibited_names for part in p.parts)]
    if bad:
        sample = ", ".join(p.relative_to(output).as_posix() for p in bad[:10])
        raise SystemExit(f"GITHUB PAGES BUILD REFUSED: prohibited deployment files: {sample}")

    print("GITHUB PAGES STATIC BUILD PASS")
    print(
        json.dumps(
            {
                "output": str(output),
                "courses": len(built),
                "units": sum(item["units"] for item in built),
                "journeys": sum(item["journeys"] for item in built),
                "course_packages": built,
                "files": len(files),
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    build(Path(args.output))


if __name__ == "__main__":
    main()
