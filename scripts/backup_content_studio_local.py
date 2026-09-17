from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_STATE_DIR = ROOT / "server_data"
DEFAULT_BACKUP_DIR = ROOT / "content-studio-backups"
FORMAT_VERSION = 1
ARCHIVE_TYPE = "story-method-content-studio-local-backup"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _copy_sqlite_snapshot(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    source_uri = f"file:{source.resolve().as_posix()}?mode=ro"
    src = sqlite3.connect(source_uri, uri=True)
    dst = sqlite3.connect(target)
    try:
        src.backup(dst)
    finally:
        # sqlite3.Connection context managers commit/rollback but do not close
        # the connection object. Explicit close is required on Windows so the
        # temporary snapshot can be removed when the backup workspace exits.
        dst.close()
        src.close()


def _snapshot_state(state_dir: Path, snapshot_dir: Path) -> list[Path]:
    if not state_dir.exists():
        state_dir.mkdir(parents=True, exist_ok=True)

    copied: list[Path] = []
    for source in sorted(state_dir.rglob("*")):
        if source.is_symlink():
            raise RuntimeError(f"Refusing to back up symbolic link: {source}")
        if not source.is_file() or source.name == ".gitkeep":
            continue
        relative = source.relative_to(state_dir)
        target = snapshot_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix.lower() == ".sqlite3":
            _copy_sqlite_snapshot(source, target)
        else:
            shutil.copy2(source, target)
        copied.append(target)
    return copied


def create_backup(*, state_dir: Path = DEFAULT_STATE_DIR, backup_dir: Path = DEFAULT_BACKUP_DIR) -> Path:
    state_dir = state_dir.resolve()
    backup_dir = backup_dir.resolve()
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    archive_path = backup_dir / f"content-studio-backup-{stamp}.zip"

    with tempfile.TemporaryDirectory(prefix="content-studio-backup-") as tmp_raw:
        snapshot_dir = Path(tmp_raw) / "server_data"
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        copied = _snapshot_state(state_dir, snapshot_dir)
        files = []
        for path in copied:
            relative = path.relative_to(snapshot_dir).as_posix()
            files.append(
                {
                    "path": relative,
                    "size": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
            )
        manifest = {
            "archive_type": ARCHIVE_TYPE,
            "format_version": FORMAT_VERSION,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "contains_credentials": False,
            "state_root": "server_data",
            "file_count": len(files),
            "files": files,
        }

        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
            for path in copied:
                relative = path.relative_to(snapshot_dir).as_posix()
                archive.write(path, arcname=f"server_data/{relative}")

    checksum = sha256_file(archive_path)
    archive_path.with_suffix(archive_path.suffix + ".sha256").write_text(
        f"{checksum}  {archive_path.name}\n", encoding="utf-8"
    )
    return archive_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a zero-cost local backup of Content Studio state without credentials."
    )
    parser.add_argument("--state-dir", default=str(DEFAULT_STATE_DIR))
    parser.add_argument("--backup-dir", default=str(DEFAULT_BACKUP_DIR))
    args = parser.parse_args()

    archive = create_backup(
        state_dir=Path(args.state_dir),
        backup_dir=Path(args.backup_dir),
    )
    print(f"Content Studio backup created: {archive}")
    print(f"SHA-256: {archive.with_suffix(archive.suffix + '.sha256')}")
    print("Owner credentials are intentionally excluded from the backup archive.")
    print("No paid service, cloud storage, or billing account was used.")


if __name__ == "__main__":
    main()
