from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "distribution" / "content-studio-teacher"
LOCK_PATH = ROOT / "release" / "content-studio" / "teacher-distribution-v1.0.0.json"
SOURCE_FILES = (
    "Install Content Studio.cmd",
    "install_content_studio.py",
    "START_HERE.txt",
    "DAILY_USE.txt",
    "BACKUP_AND_RECOVERY.txt",
    "FIRST_RUN_CHECKLIST.txt",
)
RELEASE_INFO_NAME = "RELEASE_INFO.json"
MANIFEST_NAME = "PACKAGE_MANIFEST.json"
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_lock() -> dict:
    return json.loads(LOCK_PATH.read_text(encoding="utf-8"))


def release_info(lock: dict) -> dict:
    return {
        "product": "The Story Method - Content Studio",
        "content_studio_version": lock["content_studio_version"],
        "distribution_revision": lock["distribution_revision"],
        "repository": lock["repository"],
        "runtime_branch": lock["runtime_branch"],
        "validated_runtime_commit": lock["validated_runtime_commit"],
        "validated_runtime_tree": lock["validated_runtime_tree"],
        "windows_teacher_acceptance": lock["windows_teacher_acceptance"]["status"],
        "zero_cost_required": lock["zero_cost_required"],
        "credentials_included": False,
        "private_state_included": False,
        "publication_enabled_by_default": False,
    }


def source_payloads(lock: dict) -> dict[str, bytes]:
    payloads: dict[str, bytes] = {}
    for name in SOURCE_FILES:
        path = SOURCE_DIR / name
        if not path.is_file():
            raise SystemExit(f"Teacher distribution source file is missing: {path}")
        payloads[name] = path.read_bytes()
    payloads[RELEASE_INFO_NAME] = (
        json.dumps(release_info(lock), indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    return payloads


def package_manifest(lock: dict, payloads: dict[str, bytes]) -> dict:
    return {
        "archive_type": "story-method-content-studio-teacher-onboarding",
        "format_version": 1,
        "content_studio_version": lock["content_studio_version"],
        "distribution_revision": lock["distribution_revision"],
        "validated_runtime_commit": lock["validated_runtime_commit"],
        "validated_runtime_tree": lock["validated_runtime_tree"],
        "zero_cost_required": True,
        "credentials_included": False,
        "private_state_included": False,
        "files": [
            {
                "path": name,
                "size": len(payloads[name]),
                "sha256": sha256_bytes(payloads[name]),
            }
            for name in sorted(payloads)
        ],
    }


def zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(filename=name, date_time=FIXED_ZIP_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 0
    info.external_attr = 0
    return info


def build(output: Path) -> tuple[Path, Path]:
    lock = load_lock()
    payloads = source_payloads(lock)
    manifest_bytes = (
        json.dumps(package_manifest(lock, payloads), indent=2, sort_keys=True, ensure_ascii=False)
        + "\n"
    ).encode("utf-8")
    payloads[MANIFEST_NAME] = manifest_bytes

    output = output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(payloads):
            archive.writestr(zip_info(name), payloads[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    sidecar = output.with_suffix(output.suffix + ".sha256")
    sidecar.write_text(f"{sha256_file(output)}  {output.name}\n", encoding="utf-8")
    return output, sidecar


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the deterministic Content Studio teacher onboarding ZIP.")
    parser.add_argument("--output", required=True, help="Destination ZIP path")
    args = parser.parse_args()

    archive, sidecar = build(Path(args.output))
    print(f"CONTENT STUDIO TEACHER DISTRIBUTION BUILD PASS")
    print(f"- archive: {archive}")
    print(f"- sha256: {sidecar}")
    print("- credentials and private state excluded")
    print("- no paid service or billing workflow included")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
