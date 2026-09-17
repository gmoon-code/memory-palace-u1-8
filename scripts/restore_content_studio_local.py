from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import uuid
import zipfile

from backup_content_studio_local import (
    ARCHIVE_TYPE,
    DEFAULT_BACKUP_DIR,
    DEFAULT_STATE_DIR,
    FORMAT_VERSION,
    create_backup,
    sha256_file,
)


class BackupValidationError(RuntimeError):
    pass


def _safe_member(name: str) -> PurePosixPath:
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise BackupValidationError(f"Unsafe archive path: {name}")
    return path


def validate_archive(archive_path: Path, extract_root: Path) -> dict:
    try:
        with zipfile.ZipFile(archive_path, "r") as archive:
            members = archive.namelist()
            for name in members:
                _safe_member(name)
            if "manifest.json" not in members:
                raise BackupValidationError("Backup archive has no manifest.json")
            manifest = json.loads(archive.read("manifest.json").decode("utf-8"))
            if manifest.get("archive_type") != ARCHIVE_TYPE:
                raise BackupValidationError("This is not a Content Studio local backup")
            if manifest.get("format_version") != FORMAT_VERSION:
                raise BackupValidationError("Unsupported Content Studio backup format version")
            if manifest.get("contains_credentials") is not False:
                raise BackupValidationError("Backup manifest does not confirm credential exclusion")

            expected = manifest.get("files")
            if not isinstance(expected, list):
                raise BackupValidationError("Backup manifest file list is invalid")
            expected_paths = set()
            for record in expected:
                if not isinstance(record, dict):
                    raise BackupValidationError("Backup manifest contains an invalid file record")
                relative = _safe_member(str(record.get("path", "")))
                expected_paths.add(relative.as_posix())
                member_name = f"server_data/{relative.as_posix()}"
                if member_name not in members:
                    raise BackupValidationError(f"Backup is missing {member_name}")
                target = extract_root / Path(*relative.parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(member_name) as source, target.open("wb") as dest:
                    shutil.copyfileobj(source, dest)
                if target.stat().st_size != int(record.get("size", -1)):
                    raise BackupValidationError(f"Size mismatch for {relative.as_posix()}")
                if sha256_file(target) != record.get("sha256"):
                    raise BackupValidationError(f"SHA-256 mismatch for {relative.as_posix()}")

            actual_members = {
                PurePosixPath(name).relative_to("server_data").as_posix()
                for name in members
                if name.startswith("server_data/") and not name.endswith("/")
            }
            if actual_members != expected_paths:
                raise BackupValidationError("Backup contains files not represented exactly by the manifest")
            return manifest
    except (zipfile.BadZipFile, json.JSONDecodeError, KeyError, ValueError) as exc:
        raise BackupValidationError(f"Backup validation failed: {exc}") from exc


def restore_backup(
    archive_path: Path,
    *,
    state_dir: Path = DEFAULT_STATE_DIR,
    backup_dir: Path = DEFAULT_BACKUP_DIR,
    create_safety_backup: bool = True,
) -> Path | None:
    archive_path = archive_path.expanduser().resolve()
    state_dir = state_dir.resolve()
    backup_dir = backup_dir.resolve()
    if not archive_path.is_file():
        raise BackupValidationError(f"Backup file not found: {archive_path}")

    with tempfile.TemporaryDirectory(prefix="content-studio-restore-") as tmp_raw:
        extracted = Path(tmp_raw) / "validated-state"
        extracted.mkdir(parents=True, exist_ok=True)
        validate_archive(archive_path, extracted)

        safety_archive = None
        existing_files = state_dir.exists() and any(
            path.is_file() and path.name != ".gitkeep" for path in state_dir.rglob("*")
        )
        if create_safety_backup and existing_files:
            safety_archive = create_backup(state_dir=state_dir, backup_dir=backup_dir)

        staged = state_dir.parent / f"{state_dir.name}.restore-{uuid.uuid4().hex}"
        previous = state_dir.parent / f"{state_dir.name}.previous-{uuid.uuid4().hex}"
        if staged.exists() or previous.exists():
            raise RuntimeError("Restore staging path collision")
        shutil.copytree(extracted, staged)

        moved_previous = False
        try:
            if state_dir.exists():
                state_dir.rename(previous)
                moved_previous = True
            staged.rename(state_dir)
        except Exception:
            if staged.exists():
                shutil.rmtree(staged, ignore_errors=True)
            if moved_previous and previous.exists() and not state_dir.exists():
                previous.rename(state_dir)
            raise
        else:
            if previous.exists():
                shutil.rmtree(previous, ignore_errors=True)
            (state_dir / ".gitkeep").touch(exist_ok=True)
        return safety_archive


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Restore Content Studio local state from a validated zero-cost backup."
    )
    parser.add_argument("backup", nargs="?", help="Path to a Content Studio backup ZIP")
    parser.add_argument("--state-dir", default=str(DEFAULT_STATE_DIR))
    parser.add_argument("--backup-dir", default=str(DEFAULT_BACKUP_DIR))
    parser.add_argument("--yes", action="store_true", help="Skip the interactive RESTORE confirmation")
    args = parser.parse_args()

    raw = args.backup or input("Path to Content Studio backup ZIP: ").strip().strip('"')
    if not raw:
        raise SystemExit("No backup file was selected.")
    archive = Path(raw)

    if not args.yes:
        print("Content Studio should be closed before restoring a backup.")
        print("A safety backup of the current local state will be created first when possible.")
        confirmation = input("Type RESTORE to continue: ").strip()
        if confirmation != "RESTORE":
            raise SystemExit("Restore cancelled. No local state was changed.")

    try:
        safety = restore_backup(
            archive,
            state_dir=Path(args.state_dir),
            backup_dir=Path(args.backup_dir),
        )
    except BackupValidationError as exc:
        raise SystemExit(str(exc)) from exc

    print("Content Studio local state restored successfully.")
    if safety:
        print(f"Pre-restore safety backup: {safety}")
    print("Local owner credentials were left unchanged.")
    print("No paid service, cloud storage, or billing account was used.")


if __name__ == "__main__":
    main()
