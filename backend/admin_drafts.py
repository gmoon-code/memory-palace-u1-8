from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sqlite3
from typing import Any
import uuid

from . import admin_catalog
from .settings import ROOT

DRAFT_SCHEMA = "story-method-content-studio-drafts-1.0"
ALLOWED_STATUSES = {"draft", "archived"}
IMMUTABLE_ENTITY_FIELDS = {"id", "type", "unit_id"}
MAX_DIFF_ITEMS = 500


class DraftError(RuntimeError):
    pass


class DraftConflict(DraftError):
    pass


class DraftNotFound(DraftError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _database_path() -> Path:
    raw = os.getenv(
        "MEMORY_PALACE_ADMIN_DRAFT_DB",
        str(ROOT / "server_data" / "content-studio-drafts.sqlite3"),
    )
    return Path(raw).expanduser()


def _connect() -> sqlite3.Connection:
    path = _database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=5.0)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA foreign_keys=ON")
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS content_drafts (
            draft_id TEXT PRIMARY KEY,
            entity_id TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            unit_id TEXT,
            title TEXT,
            status TEXT NOT NULL CHECK(status IN ('draft', 'archived')),
            base_payload_json TEXT NOT NULL,
            base_fingerprint TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            version INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            archived_at TEXT,
            created_by TEXT NOT NULL,
            updated_by TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_content_drafts_active_entity
        ON content_drafts(entity_id)
        WHERE status = 'draft'
        """
    )
    connection.execute(
        "CREATE INDEX IF NOT EXISTS idx_content_drafts_status_updated ON content_drafts(status, updated_at DESC)"
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS content_draft_revisions (
            revision_id INTEGER PRIMARY KEY AUTOINCREMENT,
            draft_id TEXT NOT NULL REFERENCES content_drafts(draft_id) ON DELETE CASCADE,
            revision_number INTEGER NOT NULL,
            action TEXT NOT NULL,
            note TEXT,
            payload_json TEXT NOT NULL,
            payload_fingerprint TEXT NOT NULL,
            created_at TEXT NOT NULL,
            created_by TEXT NOT NULL,
            source_revision_id INTEGER,
            UNIQUE(draft_id, revision_number)
        )
        """
    )
    connection.execute(
        "CREATE INDEX IF NOT EXISTS idx_content_draft_revisions_lookup ON content_draft_revisions(draft_id, revision_number DESC)"
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS content_draft_snapshots (
            snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            draft_id TEXT NOT NULL REFERENCES content_drafts(draft_id) ON DELETE CASCADE,
            label TEXT NOT NULL,
            payload_json TEXT NOT NULL,
            payload_fingerprint TEXT NOT NULL,
            draft_version INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            created_by TEXT NOT NULL
        )
        """
    )
    connection.execute(
        "CREATE INDEX IF NOT EXISTS idx_content_draft_snapshots_lookup ON content_draft_snapshots(draft_id, snapshot_id DESC)"
    )
    connection.commit()
    return connection


def _canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _fingerprint(payload: Any) -> str:
    return hashlib.sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _dump(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def _load(raw: str) -> Any:
    return json.loads(raw)


def _draft_from_row(row: sqlite3.Row, *, include_payload: bool = True) -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema": DRAFT_SCHEMA,
        "draft_id": row["draft_id"],
        "entity_id": row["entity_id"],
        "entity_type": row["entity_type"],
        "unit_id": row["unit_id"],
        "title": row["title"],
        "status": row["status"],
        "version": int(row["version"]),
        "base_fingerprint": row["base_fingerprint"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "archived_at": row["archived_at"],
        "created_by": row["created_by"],
        "updated_by": row["updated_by"],
    }
    if include_payload:
        result["base_payload"] = _load(row["base_payload_json"])
        result["payload"] = _load(row["payload_json"])
        result["payload_fingerprint"] = _fingerprint(result["payload"])
        result["changed_from_base"] = result["payload_fingerprint"] != result["base_fingerprint"]
    return result


def _revision_from_row(row: sqlite3.Row, *, include_payload: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {
        "revision_id": int(row["revision_id"]),
        "draft_id": row["draft_id"],
        "revision_number": int(row["revision_number"]),
        "action": row["action"],
        "note": row["note"],
        "payload_fingerprint": row["payload_fingerprint"],
        "created_at": row["created_at"],
        "created_by": row["created_by"],
        "source_revision_id": row["source_revision_id"],
    }
    if include_payload:
        result["payload"] = _load(row["payload_json"])
    return result


def _snapshot_from_row(row: sqlite3.Row, *, include_payload: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {
        "snapshot_id": int(row["snapshot_id"]),
        "draft_id": row["draft_id"],
        "label": row["label"],
        "payload_fingerprint": row["payload_fingerprint"],
        "draft_version": int(row["draft_version"]),
        "created_at": row["created_at"],
        "created_by": row["created_by"],
    }
    if include_payload:
        result["payload"] = _load(row["payload_json"])
    return result


def _next_revision_number(connection: sqlite3.Connection, draft_id: str) -> int:
    row = connection.execute(
        "SELECT COALESCE(MAX(revision_number), 0) AS n FROM content_draft_revisions WHERE draft_id = ?",
        (draft_id,),
    ).fetchone()
    return int(row["n"]) + 1


def _insert_revision(
    connection: sqlite3.Connection,
    *,
    draft_id: str,
    action: str,
    payload: dict[str, Any],
    username: str,
    note: str | None = None,
    source_revision_id: int | None = None,
) -> int:
    revision_number = _next_revision_number(connection, draft_id)
    cursor = connection.execute(
        """
        INSERT INTO content_draft_revisions(
            draft_id, revision_number, action, note, payload_json, payload_fingerprint,
            created_at, created_by, source_revision_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            draft_id,
            revision_number,
            action,
            note,
            _dump(payload),
            _fingerprint(payload),
            _now(),
            username,
            source_revision_id,
        ),
    )
    return int(cursor.lastrowid)


def create_draft(entity_id: str, username: str) -> dict[str, Any]:
    entity = admin_catalog.get_entity(entity_id)
    if entity is None:
        raise DraftNotFound("Catalog entity not found")
    now = _now()
    with _connect() as connection:
        existing = connection.execute(
            "SELECT * FROM content_drafts WHERE entity_id = ? AND status = 'draft'",
            (entity_id,),
        ).fetchone()
        if existing is not None:
            result = _draft_from_row(existing)
            result["existing"] = True
            return result

        draft_id = f"draft-{uuid.uuid4().hex}"
        payload = dict(entity)
        base_fingerprint = _fingerprint(payload)
        connection.execute(
            """
            INSERT INTO content_drafts(
                draft_id, entity_id, entity_type, unit_id, title, status,
                base_payload_json, base_fingerprint, payload_json, version,
                created_at, updated_at, archived_at, created_by, updated_by
            ) VALUES (?, ?, ?, ?, ?, 'draft', ?, ?, ?, 1, ?, ?, NULL, ?, ?)
            """,
            (
                draft_id,
                entity_id,
                entity.get("type"),
                entity.get("unit_id"),
                entity.get("title") or entity.get("canonical_term") or entity_id,
                _dump(payload),
                base_fingerprint,
                _dump(payload),
                now,
                now,
                username,
                username,
            ),
        )
        _insert_revision(
            connection,
            draft_id=draft_id,
            action="created",
            payload=payload,
            username=username,
            note="Working copy created from normalized catalog",
        )
        connection.commit()
        row = connection.execute("SELECT * FROM content_drafts WHERE draft_id = ?", (draft_id,)).fetchone()
    result = _draft_from_row(row)
    result["existing"] = False
    return result


def get_draft(draft_id: str) -> dict[str, Any]:
    with _connect() as connection:
        row = connection.execute("SELECT * FROM content_drafts WHERE draft_id = ?", (draft_id,)).fetchone()
        if row is None:
            raise DraftNotFound("Draft not found")
        revision_count = connection.execute(
            "SELECT COUNT(*) AS n FROM content_draft_revisions WHERE draft_id = ?", (draft_id,)
        ).fetchone()["n"]
        snapshot_count = connection.execute(
            "SELECT COUNT(*) AS n FROM content_draft_snapshots WHERE draft_id = ?", (draft_id,)
        ).fetchone()["n"]
    result = _draft_from_row(row)
    result["revision_count"] = int(revision_count)
    result["snapshot_count"] = int(snapshot_count)
    return result


def list_drafts(
    *,
    status: str | None = None,
    unit_id: str | None = None,
    entity_type: str | None = None,
    limit: int = 100,
) -> dict[str, Any]:
    if status is not None and status not in ALLOWED_STATUSES:
        raise DraftError("Invalid draft status")
    clauses: list[str] = []
    params: list[Any] = []
    if status:
        clauses.append("status = ?")
        params.append(status)
    if unit_id:
        clauses.append("unit_id = ?")
        params.append(unit_id)
    if entity_type:
        clauses.append("entity_type = ?")
        params.append(entity_type)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    safe_limit = max(1, min(int(limit), 500))
    with _connect() as connection:
        rows = connection.execute(
            f"SELECT * FROM content_drafts {where} ORDER BY updated_at DESC, draft_id LIMIT ?",
            (*params, safe_limit),
        ).fetchall()
        counts = connection.execute(
            "SELECT status, COUNT(*) AS n FROM content_drafts GROUP BY status"
        ).fetchall()
    return {
        "schema": DRAFT_SCHEMA,
        "items": [_draft_from_row(row, include_payload=False) for row in rows],
        "counts": {row["status"]: int(row["n"]) for row in counts},
    }


def _validate_payload_identity(draft: sqlite3.Row, payload: dict[str, Any]) -> None:
    current = _load(draft["payload_json"])
    for field in IMMUTABLE_ENTITY_FIELDS:
        if field in current and payload.get(field) != current.get(field):
            raise DraftError(f"Draft field '{field}' is immutable")


def update_draft(
    draft_id: str,
    *,
    payload: dict[str, Any],
    expected_version: int,
    username: str,
    note: str | None = None,
    autosave: bool = False,
) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise DraftError("Draft payload must be an object")
    with _connect() as connection:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute("SELECT * FROM content_drafts WHERE draft_id = ?", (draft_id,)).fetchone()
        if row is None:
            raise DraftNotFound("Draft not found")
        if row["status"] != "draft":
            raise DraftError("Archived drafts cannot be edited")
        if int(row["version"]) != int(expected_version):
            raise DraftConflict("Draft changed since this editor loaded it")
        _validate_payload_identity(row, payload)
        current_payload = _load(row["payload_json"])
        current_fingerprint = _fingerprint(current_payload)
        new_fingerprint = _fingerprint(payload)
        if current_fingerprint == new_fingerprint:
            connection.rollback()
            result = _draft_from_row(row)
            result["unchanged"] = True
            return result

        new_version = int(row["version"]) + 1
        now = _now()
        title = payload.get("title") or payload.get("canonical_term") or row["title"]
        action = "autosaved" if autosave else "saved"
        connection.execute(
            """
            UPDATE content_drafts
            SET payload_json = ?, version = ?, title = ?, updated_at = ?, updated_by = ?
            WHERE draft_id = ?
            """,
            (_dump(payload), new_version, str(title), now, username, draft_id),
        )
        revision_id = _insert_revision(
            connection,
            draft_id=draft_id,
            action=action,
            payload=payload,
            username=username,
            note=note,
        )
        connection.commit()
        updated = connection.execute("SELECT * FROM content_drafts WHERE draft_id = ?", (draft_id,)).fetchone()
    result = _draft_from_row(updated)
    result["revision_id"] = revision_id
    result["unchanged"] = False
    return result


def archive_draft(draft_id: str, *, expected_version: int, username: str) -> dict[str, Any]:
    with _connect() as connection:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute("SELECT * FROM content_drafts WHERE draft_id = ?", (draft_id,)).fetchone()
        if row is None:
            raise DraftNotFound("Draft not found")
        if row["status"] == "archived":
            connection.rollback()
            return _draft_from_row(row)
        if int(row["version"]) != int(expected_version):
            raise DraftConflict("Draft changed since this editor loaded it")
        payload = _load(row["payload_json"])
        new_version = int(row["version"]) + 1
        now = _now()
        connection.execute(
            "UPDATE content_drafts SET status = 'archived', version = ?, archived_at = ?, updated_at = ?, updated_by = ? WHERE draft_id = ?",
            (new_version, now, now, username, draft_id),
        )
        _insert_revision(
            connection,
            draft_id=draft_id,
            action="archived",
            payload=payload,
            username=username,
            note="Draft archived without deleting revision history",
        )
        connection.commit()
        updated = connection.execute("SELECT * FROM content_drafts WHERE draft_id = ?", (draft_id,)).fetchone()
    return _draft_from_row(updated)


def unarchive_draft(draft_id: str, *, expected_version: int, username: str) -> dict[str, Any]:
    with _connect() as connection:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute("SELECT * FROM content_drafts WHERE draft_id = ?", (draft_id,)).fetchone()
        if row is None:
            raise DraftNotFound("Draft not found")
        if row["status"] == "draft":
            connection.rollback()
            return _draft_from_row(row)
        if int(row["version"]) != int(expected_version):
            raise DraftConflict("Draft changed since this editor loaded it")
        conflict = connection.execute(
            "SELECT draft_id FROM content_drafts WHERE entity_id = ? AND status = 'draft' AND draft_id <> ?",
            (row["entity_id"], draft_id),
        ).fetchone()
        if conflict is not None:
            raise DraftConflict("Another active draft already exists for this entity")
        payload = _load(row["payload_json"])
        new_version = int(row["version"]) + 1
        now = _now()
        connection.execute(
            "UPDATE content_drafts SET status = 'draft', version = ?, archived_at = NULL, updated_at = ?, updated_by = ? WHERE draft_id = ?",
            (new_version, now, username, draft_id),
        )
        _insert_revision(
            connection,
            draft_id=draft_id,
            action="restored_from_archive",
            payload=payload,
            username=username,
            note="Archived draft restored as active working copy",
        )
        connection.commit()
        updated = connection.execute("SELECT * FROM content_drafts WHERE draft_id = ?", (draft_id,)).fetchone()
    return _draft_from_row(updated)


def list_revisions(draft_id: str, limit: int = 100) -> dict[str, Any]:
    get_draft(draft_id)
    safe_limit = max(1, min(int(limit), 500))
    with _connect() as connection:
        rows = connection.execute(
            "SELECT * FROM content_draft_revisions WHERE draft_id = ? ORDER BY revision_number DESC LIMIT ?",
            (draft_id, safe_limit),
        ).fetchall()
    return {"draft_id": draft_id, "items": [_revision_from_row(row) for row in rows]}


def get_revision(draft_id: str, revision_id: int) -> dict[str, Any]:
    with _connect() as connection:
        row = connection.execute(
            "SELECT * FROM content_draft_revisions WHERE draft_id = ? AND revision_id = ?",
            (draft_id, int(revision_id)),
        ).fetchone()
    if row is None:
        raise DraftNotFound("Revision not found")
    return _revision_from_row(row, include_payload=True)


def restore_revision(
    draft_id: str,
    revision_id: int,
    *,
    expected_version: int,
    username: str,
) -> dict[str, Any]:
    target = get_revision(draft_id, revision_id)
    with _connect() as connection:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute("SELECT * FROM content_drafts WHERE draft_id = ?", (draft_id,)).fetchone()
        if row is None:
            raise DraftNotFound("Draft not found")
        if row["status"] != "draft":
            raise DraftError("Archived drafts must be restored before revising")
        if int(row["version"]) != int(expected_version):
            raise DraftConflict("Draft changed since this editor loaded it")
        payload = target["payload"]
        _validate_payload_identity(row, payload)
        new_version = int(row["version"]) + 1
        now = _now()
        title = payload.get("title") or payload.get("canonical_term") or row["title"]
        connection.execute(
            "UPDATE content_drafts SET payload_json = ?, version = ?, title = ?, updated_at = ?, updated_by = ? WHERE draft_id = ?",
            (_dump(payload), new_version, str(title), now, username, draft_id),
        )
        new_revision_id = _insert_revision(
            connection,
            draft_id=draft_id,
            action="restored_revision",
            payload=payload,
            username=username,
            note=f"Restored from revision {target['revision_number']}",
            source_revision_id=int(revision_id),
        )
        connection.commit()
        updated = connection.execute("SELECT * FROM content_drafts WHERE draft_id = ?", (draft_id,)).fetchone()
    result = _draft_from_row(updated)
    result["revision_id"] = new_revision_id
    result["restored_from_revision_id"] = int(revision_id)
    return result


def create_snapshot(draft_id: str, *, label: str, username: str) -> dict[str, Any]:
    clean_label = label.strip()[:160]
    if not clean_label:
        raise DraftError("Snapshot label is required")
    with _connect() as connection:
        row = connection.execute("SELECT * FROM content_drafts WHERE draft_id = ?", (draft_id,)).fetchone()
        if row is None:
            raise DraftNotFound("Draft not found")
        payload = _load(row["payload_json"])
        cursor = connection.execute(
            """
            INSERT INTO content_draft_snapshots(
                draft_id, label, payload_json, payload_fingerprint, draft_version, created_at, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                draft_id,
                clean_label,
                _dump(payload),
                _fingerprint(payload),
                int(row["version"]),
                _now(),
                username,
            ),
        )
        snapshot_id = int(cursor.lastrowid)
        _insert_revision(
            connection,
            draft_id=draft_id,
            action="snapshot_created",
            payload=payload,
            username=username,
            note=clean_label,
        )
        connection.commit()
        snapshot = connection.execute(
            "SELECT * FROM content_draft_snapshots WHERE snapshot_id = ?", (snapshot_id,)
        ).fetchone()
    return _snapshot_from_row(snapshot, include_payload=True)


def list_snapshots(draft_id: str, limit: int = 100) -> dict[str, Any]:
    get_draft(draft_id)
    safe_limit = max(1, min(int(limit), 500))
    with _connect() as connection:
        rows = connection.execute(
            "SELECT * FROM content_draft_snapshots WHERE draft_id = ? ORDER BY snapshot_id DESC LIMIT ?",
            (draft_id, safe_limit),
        ).fetchall()
    return {"draft_id": draft_id, "items": [_snapshot_from_row(row) for row in rows]}


def restore_snapshot(
    draft_id: str,
    snapshot_id: int,
    *,
    expected_version: int,
    username: str,
) -> dict[str, Any]:
    with _connect() as connection:
        snapshot = connection.execute(
            "SELECT * FROM content_draft_snapshots WHERE draft_id = ? AND snapshot_id = ?",
            (draft_id, int(snapshot_id)),
        ).fetchone()
        if snapshot is None:
            raise DraftNotFound("Snapshot not found")
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute("SELECT * FROM content_drafts WHERE draft_id = ?", (draft_id,)).fetchone()
        if row is None:
            raise DraftNotFound("Draft not found")
        if row["status"] != "draft":
            raise DraftError("Archived drafts must be restored before revising")
        if int(row["version"]) != int(expected_version):
            raise DraftConflict("Draft changed since this editor loaded it")
        payload = _load(snapshot["payload_json"])
        _validate_payload_identity(row, payload)
        new_version = int(row["version"]) + 1
        now = _now()
        title = payload.get("title") or payload.get("canonical_term") or row["title"]
        connection.execute(
            "UPDATE content_drafts SET payload_json = ?, version = ?, title = ?, updated_at = ?, updated_by = ? WHERE draft_id = ?",
            (_dump(payload), new_version, str(title), now, username, draft_id),
        )
        revision_id = _insert_revision(
            connection,
            draft_id=draft_id,
            action="restored_snapshot",
            payload=payload,
            username=username,
            note=f"Restored snapshot: {snapshot['label']}",
        )
        connection.commit()
        updated = connection.execute("SELECT * FROM content_drafts WHERE draft_id = ?", (draft_id,)).fetchone()
    result = _draft_from_row(updated)
    result["revision_id"] = revision_id
    result["restored_from_snapshot_id"] = int(snapshot_id)
    return result


def _diff(before: Any, after: Any, path: str = "$") -> list[dict[str, Any]]:
    changes: list[dict[str, Any]] = []
    if type(before) is not type(after):
        return [{"path": path, "change": "type_changed", "before": before, "after": after}]
    if isinstance(before, dict):
        keys = sorted(set(before) | set(after))
        for key in keys:
            child_path = f"{path}.{key}"
            if key not in before:
                changes.append({"path": child_path, "change": "added", "before": None, "after": after[key]})
            elif key not in after:
                changes.append({"path": child_path, "change": "removed", "before": before[key], "after": None})
            else:
                changes.extend(_diff(before[key], after[key], child_path))
            if len(changes) >= MAX_DIFF_ITEMS:
                break
        return changes[:MAX_DIFF_ITEMS]
    if isinstance(before, list):
        max_len = max(len(before), len(after))
        for index in range(max_len):
            child_path = f"{path}[{index}]"
            if index >= len(before):
                changes.append({"path": child_path, "change": "added", "before": None, "after": after[index]})
            elif index >= len(after):
                changes.append({"path": child_path, "change": "removed", "before": before[index], "after": None})
            else:
                changes.extend(_diff(before[index], after[index], child_path))
            if len(changes) >= MAX_DIFF_ITEMS:
                break
        return changes[:MAX_DIFF_ITEMS]
    if before != after:
        return [{"path": path, "change": "changed", "before": before, "after": after}]
    return []


def compare_draft(
    draft_id: str,
    *,
    revision_id: int | None = None,
    snapshot_id: int | None = None,
) -> dict[str, Any]:
    draft = get_draft(draft_id)
    before_label = "published_catalog_base"
    before = draft["base_payload"]
    if revision_id is not None:
        revision = get_revision(draft_id, revision_id)
        before = revision["payload"]
        before_label = f"revision:{revision_id}"
    elif snapshot_id is not None:
        with _connect() as connection:
            row = connection.execute(
                "SELECT * FROM content_draft_snapshots WHERE draft_id = ? AND snapshot_id = ?",
                (draft_id, int(snapshot_id)),
            ).fetchone()
        if row is None:
            raise DraftNotFound("Snapshot not found")
        before = _load(row["payload_json"])
        before_label = f"snapshot:{snapshot_id}"
    changes = _diff(before, draft["payload"])
    return {
        "draft_id": draft_id,
        "before": before_label,
        "after": f"draft_version:{draft['version']}",
        "changed": bool(changes),
        "change_count": len(changes),
        "truncated": len(changes) >= MAX_DIFF_ITEMS,
        "changes": changes,
    }


def draft_summary() -> dict[str, Any]:
    with _connect() as connection:
        totals = connection.execute(
            "SELECT status, COUNT(*) AS n FROM content_drafts GROUP BY status"
        ).fetchall()
        revision_count = connection.execute("SELECT COUNT(*) AS n FROM content_draft_revisions").fetchone()["n"]
        snapshot_count = connection.execute("SELECT COUNT(*) AS n FROM content_draft_snapshots").fetchone()["n"]
        changed_count = 0
        rows = connection.execute(
            "SELECT base_fingerprint, payload_json FROM content_drafts WHERE status = 'draft'"
        ).fetchall()
        for row in rows:
            if _fingerprint(_load(row["payload_json"])) != row["base_fingerprint"]:
                changed_count += 1
    counts = {"draft": 0, "archived": 0}
    counts.update({row["status"]: int(row["n"]) for row in totals})
    return {
        "schema": DRAFT_SCHEMA,
        "active_drafts": counts["draft"],
        "archived_drafts": counts["archived"],
        "changed_active_drafts": changed_count,
        "revision_count": int(revision_count),
        "snapshot_count": int(snapshot_count),
        "published_content_write_enabled": False,
    }
