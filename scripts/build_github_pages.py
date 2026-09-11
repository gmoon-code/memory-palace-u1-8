from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APBIO = ROOT / "content" / "ap-biology"


def copy_file(src: Path, dst: Path) -> None:
    if not src.is_file():
        raise SystemExit(f"GITHUB PAGES BUILD REFUSED: required file missing: {src.relative_to(ROOT)}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_tree(src: Path, dst: Path) -> None:
    if not src.is_dir():
        raise SystemExit(f"GITHUB PAGES BUILD REFUSED: required directory missing: {src.relative_to(ROOT)}")
    shutil.copytree(src, dst)


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
    copy_file(APBIO / "course.json", output / "content" / "ap-biology" / "course.json")

    course = json.loads((APBIO / "course.json").read_text(encoding="utf-8"))
    units = course.get("units", [])
    if len(units) != 8 or any(unit.get("status") != "STUDENT_READY" for unit in units):
        raise SystemExit("GITHUB PAGES BUILD REFUSED: released course registry is not the frozen 8-unit student release")

    journey_count = 0
    journey_files = 0
    for unit in units:
        unit_id = unit["unit_id"]
        src_unit = APBIO / unit_id
        dst_unit = output / "content" / "ap-biology" / unit_id

        registry_name = "journeys.json" if unit_id == "unit-1" else "journeys-f5.json"
        registry_src = src_unit / registry_name
        registry = json.loads(registry_src.read_text(encoding="utf-8"))
        guided = registry.get("guided_journeys", [])
        expected = int(unit.get("journey_count", 0))
        if len(guided) != expected:
            raise SystemExit(f"GITHUB PAGES BUILD REFUSED: {unit_id} journey registry expected {expected}, got {len(guided)}")
        copy_file(registry_src, dst_unit / registry_name)
        journey_count += len(guided)

        for journey in guided:
            palace_id = journey.get("palace_id")
            if not palace_id:
                raise SystemExit(f"GITHUB PAGES BUILD REFUSED: {unit_id} registry has a journey without palace_id")
            copy_file(src_unit / "journeys" / f"{palace_id}.json", dst_unit / "journeys" / f"{palace_id}.json")
            journey_files += 1

        copy_file(src_unit / "application-lab.json", dst_unit / "application-lab.json")

        if unit_id == "unit-1":
            copy_file(src_unit / "memory-objects.json", dst_unit / "memory-objects.json")
        elif unit_id in {"unit-2", "unit-3"}:
            compact = unit_id.replace("unit-", "unit")
            copy_file(src_unit / "source" / f"canonical-{compact}-f1.json", dst_unit / "source" / f"canonical-{compact}-f1.json")
            copy_file(src_unit / "review-manifest-f5.json", dst_unit / "review-manifest-f5.json")
            copy_file(src_unit / "mixed-discrimination-f5.json", dst_unit / "mixed-discrimination-f5.json")
        else:
            copy_file(src_unit / "memory-objects-f5.json", dst_unit / "memory-objects-f5.json")
            copy_file(src_unit / "review-manifest-f5.json", dst_unit / "review-manifest-f5.json")
            copy_file(src_unit / "mixed-discrimination-f5.json", dst_unit / "mixed-discrimination-f5.json")

    if journey_count != 58 or journey_files != 58:
        raise SystemExit(f"GITHUB PAGES BUILD REFUSED: expected 58 journeys, got registry={journey_count}, files={journey_files}")

    prohibited_suffixes = {".pdf", ".xlsx", ".xls", ".docx", ".zip", ".sqlite", ".sqlite3", ".py", ".pyc"}
    prohibited_names = {".git", ".env", "__pycache__", ".pytest_cache"}
    files = [p for p in output.rglob("*") if p.is_file()]
    bad = [p for p in files if p.suffix.lower() in prohibited_suffixes or any(part in prohibited_names for part in p.parts)]
    if bad:
        sample = ", ".join(p.relative_to(output).as_posix() for p in bad[:10])
        raise SystemExit(f"GITHUB PAGES BUILD REFUSED: prohibited deployment files: {sample}")

    print("GITHUB PAGES STATIC BUILD PASS")
    print(json.dumps({"output": str(output), "units": 8, "journeys": 58, "files": len(files)}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    build(Path(args.output))


if __name__ == "__main__":
    main()
