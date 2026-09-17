from __future__ import annotations

from pathlib import Path
import json
import sqlite3
import tempfile
import zipfile

from backup_content_studio_local import create_backup
from restore_content_studio_local import BackupValidationError, restore_backup

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(f"ZERO-COST BACKUP/RESTORE QA FAIL: {message}")


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def main() -> None:
    backup_launcher = (ROOT / "Backup Content Studio.cmd").read_text(encoding="utf-8")
    restore_launcher = (ROOT / "Restore Content Studio.cmd").read_text(encoding="utf-8")
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

    assert_true("backup_content_studio_local.py" in backup_launcher, "backup launcher is not wired to backup tool")
    assert_true("restore_content_studio_local.py" in restore_launcher, "restore launcher is not wired to restore tool")
    assert_true("content-studio-backups/" in gitignore, "local backup directory is not ignored by Git")

    with tempfile.TemporaryDirectory(prefix="content-studio-backup-qa-") as tmp_raw:
        root = Path(tmp_raw)
        state = root / "server_data"
        backups = root / "backups"
        state.mkdir()
        database = state / "content-studio-drafts.sqlite3"
        with sqlite3.connect(database) as connection:
            connection.execute("CREATE TABLE notes (value TEXT NOT NULL)")
            connection.execute("INSERT INTO notes(value) VALUES (?)", ("original",))
            connection.commit()
        media = state / "content-studio-media" / "sample.txt"
        media.parent.mkdir(parents=True)
        media.write_text("original-media", encoding="utf-8")

        archive = create_backup(state_dir=state, backup_dir=backups)
        assert_true(archive.is_file(), "backup ZIP was not created")
        assert_true(archive.with_suffix(".zip.sha256").is_file(), "backup checksum was not created")

        with zipfile.ZipFile(archive, "r") as zipped:
            names = set(zipped.namelist())
            assert_true("manifest.json" in names, "backup manifest is missing")
            assert_true(all(".env" not in name.lower() for name in names), "backup contains a credential environment file")
            manifest = json.loads(zipped.read("manifest.json").decode("utf-8"))
            assert_true(manifest.get("contains_credentials") is False, "manifest does not lock credentials out")
            assert_true(manifest.get("file_count") == 2, "unexpected backup file count")

        with sqlite3.connect(database) as connection:
            connection.execute("UPDATE notes SET value = ?", ("changed",))
            connection.commit()
        media.write_text("changed-media", encoding="utf-8")
        (state / "temporary.txt").write_text("remove-me", encoding="utf-8")

        safety = restore_backup(archive, state_dir=state, backup_dir=backups)
        assert_true(safety is not None and safety.is_file(), "pre-restore safety backup was not created")
        with sqlite3.connect(database) as connection:
            row = connection.execute("SELECT value FROM notes").fetchone()
        assert_true(row == ("original",), "SQLite state did not restore to backup value")
        assert_true(media.read_text(encoding="utf-8") == "original-media", "media state did not restore")
        assert_true(not (state / "temporary.txt").exists(), "restore left files that were not in the backup")

        tampered = root / "tampered.zip"
        with zipfile.ZipFile(archive, "r") as source, zipfile.ZipFile(tampered, "w", compression=zipfile.ZIP_DEFLATED) as dest:
            for name in source.namelist():
                payload = source.read(name)
                if name.endswith("sample.txt"):
                    payload = b"tampered"
                dest.writestr(name, payload)
        before = media.read_bytes()
        try:
            restore_backup(
                tampered,
                state_dir=state,
                backup_dir=backups,
                create_safety_backup=False,
            )
        except BackupValidationError:
            pass
        else:
            fail("tampered backup was accepted")
        assert_true(media.read_bytes() == before, "failed restore modified local state")

    print("ZERO-COST BACKUP/RESTORE QA PASS")
    print("- SQLite backup uses a consistent SQLite snapshot")
    print("- media and staged state are included")
    print("- credentials are excluded")
    print("- restore validates manifest hashes before changing state")
    print("- restore creates a pre-restore safety backup")
    print("- tampered archives are rejected without state drift")
    print("- no paid service or cloud storage is required")


if __name__ == "__main__":
    main()
