from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
from typing import Any, Iterable
import uuid

from . import admin_catalog, admin_drafts, admin_editors, course_packages
from .settings import APBIO_DIR, FRONTEND_DIR, ROOT

MANAGEMENT_SCHEMA = "story-method-content-studio-management-1.1"
PORTABLE_SCHEMA = "story-method-content-studio-portable-1.0"
MEDIA_SCHEMA = "story-method-content-studio-media-1.0"
MANAGED_TYPES = {"question", "question_set", "challenge"}
PROPOSAL_TYPES = {"question", "question_set", "challenge"}
EDITABLE_TYPES = set(admin_editors.editor_types()) | MANAGED_TYPES
MAX_IMPORT_RECORDS = 500
MAX_BULK_TARGETS = 75
MAX_BULK_MATCHES = 500
MAX_MEDIA_BYTES = 25 * 1024 * 1024

SAFE_TEXT_KEYS = {
    "title",
    "subtitle",
    "description",
    "introduction",
    "instructions",
    "conclusion",
    "story_title",
    "tagline",
    "premise",
    "mission",
    "finale",
    "learner_rule",
    "route_orientation",
    "scene_kicker",
    "location_description",
    "orientation",
    "story_open",
    "story_paragraphs",
    "story_close",
    "continuity_object",
    "prompt",
    "answer",
    "target_answer",
    "answer_guide",
    "explanation",
    "canonical_science",
    "purpose",
    "domain",
    "canonical_term",
    "canonical_definition",
    "teacher_notes",
    "visual",
    "job",
    "role",
    "application_question",
    "productive_retrieval_target",
    "distractor_notes",
    "caption",
    "alt_text",
    "transcript",
    "notes",
}

MEDIA_TYPES: dict[str, tuple[str, str]] = {
    ".png": ("image", "image/png"),
    ".jpg": ("image", "image/jpeg"),
    ".jpeg": ("image", "image/jpeg"),
    ".webp": ("image", "image/webp"),
    ".gif": ("image", "image/gif"),
    ".mp3": ("audio", "audio/mpeg"),
    ".wav": ("audio", "audio/wav"),
    ".ogg": ("audio", "audio/ogg"),
    ".m4a": ("audio", "audio/mp4"),
    ".mp4": ("video", "video/mp4"),
    ".webm": ("video", "video/webm"),
    ".pdf": ("document", "application/pdf"),
}


class ManagementError(admin_drafts.DraftError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _require_course_unit(
    course_id: str,
    unit_id: str,
    *,
    editable: bool = False,
) -> dict[str, Any]:
    try:
        access = (
            admin_catalog.require_editable_course(course_id)
            if editable
            else admin_catalog.course_access(course_id)
        )
    except ValueError as exc:
        raise ManagementError(str(exc)) from exc
    if not access.get("catalog_ready"):
        raise ManagementError(f"Content Studio catalog is not available for course '{course_id}'")
    try:
        unit = course_packages.unit(course_id, unit_id)
    except course_packages.CoursePackageError as exc:
        raise ManagementError(str(exc)) from exc
    if unit is None:
        raise ManagementError(f"Unit '{unit_id}' is not declared for course '{course_id}'")
    return unit


def _repo_file(source_path: str | None) -> Path | None:
    if not source_path:
        return None
    candidate = (ROOT / source_path).resolve()
    try:
        candidate.relative_to(ROOT.resolve())
    except ValueError:
        return None
    return candidate if candidate.exists() and candidate.is_file() else None


def _load_source(source_path: str | None) -> Any:
    path = _repo_file(source_path)
    if path is None:
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _records(payload: Any, keys: Iterable[str]) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in keys:
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def _normalized_overlay(base: dict[str, Any], raw: dict[str, Any] | None) -> dict[str, Any]:
    payload = deepcopy(raw) if isinstance(raw, dict) else {}
    for key, value in base.items():
        if key in {"id", "type", "course_id", "unit_id", "source_path", "question_type", "question_set_id", "scene_id", "journey_id"}:
            payload[key] = deepcopy(value)
        elif key not in payload or payload[key] in (None, "", [], {}):
            payload[key] = deepcopy(value)
    payload.setdefault("title", base.get("title"))
    return payload


def _match_review_question(entity: dict[str, Any], source: Any) -> dict[str, Any] | None:
    knowledge_ids = [str(item) for item in _as_list(entity.get("knowledge_ids")) if item not in (None, "")]
    for record in _records(source, ("targets", "records", "items")):
        raw_knowledge = record.get("knowledge_id") or record.get("memory_object_id") or record.get("object_id")
        if knowledge_ids and str(raw_knowledge or "") not in knowledge_ids:
            continue
        if entity.get("prompt") and record.get("prompt") and entity["prompt"] != record["prompt"]:
            continue
        return record
    for record in _records(source, ("targets", "records", "items")):
        if entity.get("prompt") and record.get("prompt") == entity.get("prompt"):
            return record
    return None


def _match_mixed_question(entity: dict[str, Any], source: Any) -> dict[str, Any] | None:
    raw_id = entity["id"].split(":", 2)[-1]
    for question_set in _records(source, ("sets", "records", "items")):
        for question in _as_list(question_set.get("questions")):
            if not isinstance(question, dict):
                continue
            question_id = str(question.get("question_id") or "")
            if question_id and question_id == raw_id:
                result = deepcopy(question)
                result.setdefault("set_id", question_set.get("set_id"))
                result.setdefault("set_title", question_set.get("title"))
                return result
            if entity.get("prompt") and question.get("prompt") == entity.get("prompt"):
                result = deepcopy(question)
                result.setdefault("set_id", question_set.get("set_id"))
                result.setdefault("set_title", question_set.get("title"))
                return result
    return None


def _match_question_set(entity: dict[str, Any], source: Any) -> dict[str, Any] | None:
    target = str(entity.get("set_id") or "")
    for record in _records(source, ("sets", "records", "items")):
        if str(record.get("set_id") or "") == target:
            return record
    return None


def _match_challenge(entity: dict[str, Any], source: Any) -> dict[str, Any] | None:
    target = str(entity.get("challenge_id") or "")
    for record in _records(source, ("items", "challenges", "records")):
        if str(record.get("challenge_id") or "") == target:
            return record
    return None


def _quick_recall_payload(entity: dict[str, Any], course_id: str = "ap-biology") -> dict[str, Any]:
    result = deepcopy(entity)
    scene_id = entity.get("scene_id")
    if not scene_id:
        return result
    try:
        scene = admin_editors.editable_entity(str(scene_id), course_id)
    except admin_drafts.DraftError:
        return result
    result["prompt"] = scene.get("checkpoint_prompt") or entity.get("prompt")
    result["knowledge_ids"] = [scene.get("checkpoint_object_id")] if scene.get("checkpoint_object_id") else entity.get("knowledge_ids", [])
    result["quick_recall"] = {
        "scene_id": scene_id,
        "checkpoint": bool(scene.get("checkpoint")),
        "checkpoint_object_id": scene.get("checkpoint_object_id"),
    }
    return result


def managed_entity(entity_id: str, course_id: str = "ap-biology") -> dict[str, Any]:
    base = admin_catalog.get_entity(entity_id, course_id)
    if base is None:
        raise admin_drafts.DraftNotFound("Catalog entity not found")
    if str(base.get("course_id") or "") != str(course_id):
        raise ManagementError("Catalog entity course identity does not match requested course")
    entity_type = str(base.get("type") or "")
    if entity_type not in MANAGED_TYPES:
        raise ManagementError(f"Entity type '{entity_type}' is not managed by Step 7")
    if entity_type == "question" and base.get("question_type") == "quick_recall":
        return _quick_recall_payload(base, course_id)

    source_path = base.get("source_path")
    unit_id = str(base.get("unit_id") or "")
    source = (
        admin_editors._load_source(
            source_path,
            course_id=course_id,
            unit_id=unit_id,
        )
        if source_path
        else None
    )
    raw: dict[str, Any] | None = None
    if entity_type == "question":
        if base.get("question_type") == "review":
            raw = _match_review_question(base, source)
        elif base.get("question_type") == "mixed_discrimination":
            raw = _match_mixed_question(base, source)
    elif entity_type == "question_set":
        raw = _match_question_set(base, source)
    elif entity_type == "challenge":
        raw = _match_challenge(base, source)

    payload = _normalized_overlay(base, raw)
    if entity_type == "question" and base.get("question_type") == "review":
        payload["answer"] = payload.get("answer") or payload.get("target_answer")
        payload["explanation"] = payload.get("explanation") or payload.get("canonical_science")
    if entity_type == "challenge":
        payload["answer"] = payload.get("answer") or payload.get("answer_guide")
    return payload


def _replace_baseline(
    draft: dict[str, Any],
    enriched: dict[str, Any],
    username: str,
    note: str,
    *,
    course_id: str,
) -> dict[str, Any]:
    if draft.get("existing"):
        return draft
    if draft.get("payload") == enriched:
        return draft
    fingerprint = admin_drafts._fingerprint(enriched)
    title = enriched.get("title") or enriched.get("prompt") or draft.get("title") or draft["entity_id"]
    with admin_drafts._connect() as connection:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute(
            "SELECT version, status FROM content_drafts WHERE draft_id = ? AND course_id = ?",
            (draft["draft_id"], course_id),
        ).fetchone()
        if row is None:
            raise admin_drafts.DraftNotFound("Draft not found")
        if int(row["version"]) != 1 or row["status"] != "draft":
            raise admin_drafts.DraftConflict("Draft changed while the source-enriched baseline was being prepared")
        connection.execute(
            """
            UPDATE content_drafts
            SET base_payload_json = ?, base_fingerprint = ?, payload_json = ?, title = ?
            WHERE draft_id = ? AND course_id = ?
            """,
            (
                admin_drafts._dump(enriched),
                fingerprint,
                admin_drafts._dump(enriched),
                str(title),
                draft["draft_id"],
                course_id,
            ),
        )
        connection.execute(
            """
            UPDATE content_draft_revisions
            SET payload_json = ?, payload_fingerprint = ?, note = ?
            WHERE draft_id = ? AND revision_number = 1
            """,
            (
                admin_drafts._dump(enriched),
                fingerprint,
                note,
                draft["draft_id"],
            ),
        )
        connection.commit()
    result = admin_drafts.get_draft(draft["draft_id"], course_id=course_id)
    result["existing"] = False
    return result


def create_managed_draft(
    entity_id: str,
    username: str,
    course_id: str = "ap-biology",
) -> dict[str, Any]:
    try:
        admin_catalog.require_editable_course(course_id)
    except ValueError as exc:
        raise ManagementError(str(exc)) from exc
    enriched = managed_entity(entity_id, course_id)
    draft = admin_drafts.create_draft(entity_id, username, course_id)
    return _replace_baseline(
        draft,
        enriched,
        username,
        "Step 7 working copy created from the complete source assessment record",
        course_id=course_id,
    )


def _proposal_defaults(entity_type: str, title: str) -> dict[str, Any]:
    if entity_type == "question":
        return {
            "question_type": "teacher_created",
            "title": title,
            "prompt": "",
            "choices": [],
            "answer": "",
            "explanation": "",
            "knowledge_ids": [],
            "ap_skill": "",
            "difficulty": "",
            "distractor_notes": "",
        }
    if entity_type == "question_set":
        return {
            "question_type": "mixed_discrimination",
            "title": title,
            "purpose": "",
            "knowledge_ids": [],
            "terms": [],
            "initial_delay_hours": None,
            "questions": [],
        }
    return {
        "question_type": "challenge_lab",
        "title": title,
        "domain": "",
        "challenge_type": "",
        "prompt": "",
        "answer": "",
        "knowledge_ids": [],
        "prerequisite_loci": [],
        "prerequisite_scene_titles": [],
        "source_assessment": "teacher_created",
    }


def create_proposed_draft(
    entity_type: str,
    unit_id: str,
    title: str,
    username: str,
    *,
    seed: dict[str, Any] | None = None,
    entity_id: str | None = None,
    course_id: str = "ap-biology",
) -> dict[str, Any]:
    if entity_type not in PROPOSAL_TYPES:
        raise ManagementError("Only questions, question sets, and Challenge Lab items can be created in Step 7")
    _require_course_unit(course_id, unit_id, editable=True)
    clean_title = title.strip()[:500]
    if not clean_title:
        raise ManagementError("A title is required")
    proposed_id = entity_id or f"new:{entity_type}:{unit_id}:{uuid.uuid4().hex}"
    if not proposed_id.startswith("new:"):
        raise ManagementError("New records must use a Step 7 proposal ID")
    if len(proposed_id) > 512:
        raise ManagementError("Proposal ID is too long")

    base = {
        "id": proposed_id,
        "type": entity_type,
        "course_id": course_id,
        "unit_id": unit_id,
        "title": clean_title,
        "proposal": True,
    }
    payload = {**base, **_proposal_defaults(entity_type, clean_title)}
    if isinstance(seed, dict):
        for key, value in seed.items():
            if key not in admin_drafts.IMMUTABLE_ENTITY_FIELDS:
                payload[key] = deepcopy(value)
    payload.update({"id": proposed_id, "type": entity_type, "course_id": course_id, "unit_id": unit_id, "proposal": True})
    payload["title"] = str(payload.get("title") or clean_title)[:500]

    now = admin_drafts._now()
    with admin_drafts._connect() as connection:
        existing = connection.execute(
            "SELECT * FROM content_drafts WHERE course_id = ? AND entity_id = ? AND status = 'draft'",
            (course_id, proposed_id),
        ).fetchone()
        if existing is not None:
            result = admin_drafts._draft_from_row(existing)
            result["existing"] = True
            result["proposal"] = True
            return result
        draft_id = f"draft-{uuid.uuid4().hex}"
        connection.execute(
            """
            INSERT INTO content_drafts(
                draft_id, entity_id, entity_type, course_id, unit_id, title, status,
                base_payload_json, base_fingerprint, payload_json, version,
                created_at, updated_at, archived_at, created_by, updated_by
            ) VALUES (?, ?, ?, ?, ?, ?, 'draft', ?, ?, ?, 1, ?, ?, NULL, ?, ?)
            """,
            (
                draft_id,
                proposed_id,
                entity_type,
                course_id,
                unit_id,
                payload["title"],
                admin_drafts._dump(base),
                admin_drafts._fingerprint(base),
                admin_drafts._dump(payload),
                now,
                now,
                username,
                username,
            ),
        )
        admin_drafts._insert_revision(
            connection,
            draft_id=draft_id,
            action="created_proposal",
            payload=payload,
            username=username,
            note="New Step 7 content proposal created outside the published student runtime",
        )
        connection.commit()
        row = connection.execute("SELECT * FROM content_drafts WHERE draft_id = ?", (draft_id,)).fetchone()
    result = admin_drafts._draft_from_row(row)
    result["existing"] = False
    result["proposal"] = True
    return result


def validate_managed_payload(entity_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    if entity_type not in MANAGED_TYPES:
        raise ManagementError("Unsupported Step 7 content type")
    if not isinstance(payload, dict):
        raise ManagementError("Content payload must be an object")
    if payload.get("type") != entity_type:
        raise ManagementError("Content type does not match the draft")
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(payload.get("title"), str) or not payload.get("title", "").strip():
        warnings.append("A clear teacher-facing title is recommended")
    if entity_type == "question":
        if not isinstance(payload.get("prompt"), str):
            errors.append("Question prompt must be text")
        elif not payload.get("prompt", "").strip():
            warnings.append("Question prompt is empty")
        if payload.get("choices") is not None and not isinstance(payload.get("choices"), list):
            errors.append("Question choices must be a list")
        if payload.get("knowledge_ids") is not None and not isinstance(payload.get("knowledge_ids"), list):
            errors.append("Question knowledge IDs must be a list")
        if payload.get("question_type") != "quick_recall" and not str(payload.get("answer") or "").strip():
            warnings.append("Question answer is empty")
    elif entity_type == "question_set":
        for key in ("knowledge_ids", "terms", "questions"):
            if payload.get(key) is not None and not isinstance(payload.get(key), list):
                errors.append(f"Question set {key.replace('_', ' ')} must be a list")
    elif entity_type == "challenge":
        if payload.get("knowledge_ids") is not None and not isinstance(payload.get("knowledge_ids"), list):
            errors.append("Challenge knowledge IDs must be a list")
        for key in ("prerequisite_loci", "prerequisite_scene_titles"):
            if payload.get(key) is not None and not isinstance(payload.get(key), list):
                errors.append(f"Challenge {key.replace('_', ' ')} must be a list")
        if not str(payload.get("prompt") or "").strip():
            warnings.append("Challenge prompt is empty")
        if not str(payload.get("answer") or payload.get("answer_guide") or "").strip():
            warnings.append("Challenge answer guide is empty")
    if errors:
        raise ManagementError("; ".join(errors))
    return {
        "valid": True,
        "entity_type": entity_type,
        "warnings": warnings,
        "warning_count": len(warnings),
    }


def save_managed_draft(
    draft_id: str,
    *,
    payload: dict[str, Any],
    expected_version: int,
    username: str,
    note: str | None = None,
    autosave: bool = False,
    course_id: str = "ap-biology",
) -> dict[str, Any]:
    try:
        admin_catalog.require_editable_course(course_id)
    except ValueError as exc:
        raise ManagementError(str(exc)) from exc
    current = admin_drafts.get_draft(draft_id, course_id=course_id)
    entity_type = str(current.get("entity_type") or "")
    validation = validate_managed_payload(entity_type, payload)
    saved = admin_drafts.update_draft(
        draft_id,
        payload=payload,
        expected_version=expected_version,
        username=username,
        note=note,
        autosave=autosave,
        course_id=course_id,
    )
    saved["management_validation"] = validation
    saved["proposal"] = str(saved.get("entity_id") or "").startswith("new:")
    return saved


def _active_draft_rows(course_id: str = "ap-biology") -> dict[str, dict[str, Any]]:
    with admin_drafts._connect() as connection:
        rows = connection.execute(
            "SELECT * FROM content_drafts WHERE course_id = ? AND status = 'draft' ORDER BY updated_at DESC",
            (course_id,),
        ).fetchall()
    return {row["entity_id"]: admin_drafts._draft_from_row(row, include_payload=False) for row in rows}


def _proposal_rows(
    *,
    course_id: str = "ap-biology",
    unit_id: str | None = None,
    entity_type: str | None = None,
) -> list[dict[str, Any]]:
    clauses = ["course_id = ?", "status = 'draft'", "entity_id LIKE 'new:%'"]
    params: list[Any] = [course_id]
    if unit_id:
        clauses.append("unit_id = ?")
        params.append(unit_id)
    if entity_type:
        clauses.append("entity_type = ?")
        params.append(entity_type)
    with admin_drafts._connect() as connection:
        rows = connection.execute(
            f"SELECT * FROM content_drafts WHERE {' AND '.join(clauses)} ORDER BY updated_at DESC",
            params,
        ).fetchall()
    return [admin_drafts._draft_from_row(row, include_payload=False) for row in rows]


def question_bank(
    *,
    course_id: str = "ap-biology",
    unit_id: str | None = None,
    question_type: str | None = None,
    query: str | None = None,
    limit: int = 500,
) -> dict[str, Any]:
    if unit_id:
        _require_course_unit(course_id, unit_id)
    snapshot = admin_catalog.catalog(course_id)
    active = _active_draft_rows(course_id)
    q = (query or "").strip().casefold()
    items: list[dict[str, Any]] = []
    for entity in snapshot["entities"].values():
        if entity.get("type") not in {"question", "question_set"}:
            continue
        if unit_id and entity.get("unit_id") != unit_id:
            continue
        if question_type and entity.get("question_type") != question_type:
            continue
        haystack = " ".join(
            str(entity.get(key) or "")
            for key in ("id", "title", "prompt", "answer", "question_type", "set_id")
        ).casefold()
        if q and q not in haystack:
            continue
        item = deepcopy(entity)
        draft = active.get(entity["id"])
        item["draft"] = draft
        item["source_state"] = "draft" if draft else "published"
        items.append(item)
    for proposal in _proposal_rows(course_id=course_id, unit_id=unit_id):
        if proposal.get("entity_type") not in {"question", "question_set"}:
            continue
        if question_type:
            try:
                body = admin_drafts.get_draft(proposal["draft_id"], course_id=course_id)["payload"]
            except admin_drafts.DraftError:
                continue
            if body.get("question_type") != question_type:
                continue
        if q and q not in f"{proposal.get('entity_id')} {proposal.get('title')}".casefold():
            continue
        items.append(
            {
                "id": proposal["entity_id"],
                "type": proposal["entity_type"],
                "course_id": course_id,
                "unit_id": proposal.get("unit_id"),
                "title": proposal.get("title"),
                "source_state": "new_proposal",
                "draft": proposal,
                "proposal": True,
            }
        )
    safe_limit = max(1, min(int(limit), 1000))
    items.sort(key=lambda item: (item.get("unit_id") or "", item.get("question_type") or "", str(item.get("title") or "").casefold(), item["id"]))
    counts: dict[str, int] = {}
    for item in items:
        key = str(item.get("question_type") or item.get("type") or "unknown")
        counts[key] = counts.get(key, 0) + 1
    return {"schema": MANAGEMENT_SCHEMA, "course_id": course_id, "total": len(items), "counts": counts, "items": items[:safe_limit]}


def challenge_bank(
    *,
    course_id: str = "ap-biology",
    unit_id: str | None = None,
    query: str | None = None,
    limit: int = 500,
) -> dict[str, Any]:
    if unit_id:
        _require_course_unit(course_id, unit_id)
    snapshot = admin_catalog.catalog(course_id)
    active = _active_draft_rows(course_id)
    q = (query or "").strip().casefold()
    items: list[dict[str, Any]] = []
    for entity in snapshot["entities"].values():
        if entity.get("type") != "challenge":
            continue
        if unit_id and entity.get("unit_id") != unit_id:
            continue
        haystack = " ".join(str(entity.get(key) or "") for key in ("id", "title", "prompt", "domain", "challenge_type")).casefold()
        if q and q not in haystack:
            continue
        item = deepcopy(entity)
        draft = active.get(entity["id"])
        item["draft"] = draft
        item["source_state"] = "draft" if draft else "published"
        items.append(item)
    for proposal in _proposal_rows(course_id=course_id, unit_id=unit_id, entity_type="challenge"):
        if q and q not in f"{proposal.get('entity_id')} {proposal.get('title')}".casefold():
            continue
        items.append(
            {
                "id": proposal["entity_id"],
                "type": "challenge",
                "course_id": course_id,
                "unit_id": proposal.get("unit_id"),
                "title": proposal.get("title"),
                "source_state": "new_proposal",
                "draft": proposal,
                "proposal": True,
            }
        )
    safe_limit = max(1, min(int(limit), 1000))
    items.sort(key=lambda item: (item.get("unit_id") or "", str(item.get("title") or "").casefold(), item["id"]))
    return {"schema": MANAGEMENT_SCHEMA, "course_id": course_id, "total": len(items), "items": items[:safe_limit]}


def review_timeline(unit_id: str, course_id: str = "ap-biology") -> dict[str, Any]:
    _require_course_unit(course_id, unit_id)
    snapshot = admin_catalog.catalog(course_id)
    entities = snapshot["entities"]
    events: list[dict[str, Any]] = []
    assessed: set[str] = set()

    phase_order = {"immediate": 0, "delayed": 1, "discrimination": 2, "application": 3}
    for entity in entities.values():
        if entity.get("unit_id") != unit_id:
            continue
        entity_type = entity.get("type")
        question_type = entity.get("question_type")
        phase = None
        delay = None
        if entity_type == "question" and question_type == "quick_recall":
            phase = "immediate"
            delay = 0
        elif entity_type == "question" and question_type == "review":
            phase = "delayed"
            delay = entity.get("initial_review_window_hours")
        elif entity_type == "question_set":
            phase = "discrimination"
            delay = entity.get("initial_delay_hours")
        elif entity_type == "challenge":
            phase = "application"
        if phase is None:
            continue
        knowledge_ids = [str(value) for value in _as_list(entity.get("knowledge_ids")) if value not in (None, "")]
        assessed.update(knowledge_ids)
        events.append(
            {
                "phase": phase,
                "delay_hours": delay,
                "course_id": course_id,
                "entity_id": entity["id"],
                "entity_type": entity_type,
                "question_type": question_type,
                "title": entity.get("title"),
                "prompt": entity.get("prompt"),
                "knowledge_ids": knowledge_ids,
                "scene_id": entity.get("scene_id"),
                "journey_id": entity.get("journey_id"),
            }
        )

    taught: dict[str, dict[str, Any]] = {}
    for entity in entities.values():
        if entity.get("type") != "scene" or entity.get("unit_id") != unit_id:
            continue
        for raw_id in _as_list(entity.get("object_ids")):
            raw = str(raw_id)
            taught.setdefault(raw, {"knowledge_id": raw, "scene_ids": [], "scene_titles": []})
            taught[raw]["scene_ids"].append(entity["id"])
            taught[raw]["scene_titles"].append(entity.get("title"))
    gaps = [record for key, record in sorted(taught.items()) if key not in assessed]
    events.sort(
        key=lambda item: (
            phase_order.get(item["phase"], 99),
            item["delay_hours"] if isinstance(item["delay_hours"], (int, float)) else 10**9,
            str(item.get("title") or "").casefold(),
        )
    )
    return {
        "schema": MANAGEMENT_SCHEMA,
        "course_id": course_id,
        "unit_id": unit_id,
        "event_count": len(events),
        "coverage_gap_count": len(gaps),
        "events": events,
        "coverage_gaps": gaps,
        "phase_counts": {
            phase: sum(1 for item in events if item["phase"] == phase)
            for phase in ("immediate", "delayed", "discrimination", "application")
        },
    }


def _active_draft_for_entity(
    entity_id: str,
    course_id: str = "ap-biology",
) -> dict[str, Any] | None:
    with admin_drafts._connect() as connection:
        row = connection.execute(
            "SELECT * FROM content_drafts WHERE course_id = ? AND entity_id = ? AND status = 'draft'",
            (course_id, entity_id),
        ).fetchone()
    return admin_drafts._draft_from_row(row) if row is not None else None


def _editable_base(entity_id: str, course_id: str = "ap-biology") -> dict[str, Any]:
    draft = _active_draft_for_entity(entity_id, course_id)
    if draft is not None:
        return deepcopy(draft["payload"])
    entity = admin_catalog.get_entity(entity_id, course_id)
    if entity is None:
        raise admin_drafts.DraftNotFound("Catalog entity not found")
    entity_type = entity.get("type")
    if entity_type in MANAGED_TYPES:
        return managed_entity(entity_id, course_id)
    if entity_type in set(admin_editors.editor_types()):
        return admin_editors.editable_entity(entity_id, course_id)
    raise ManagementError(f"Entity type '{entity_type}' does not support draft text operations")


def _replace_text(value: str, find: str, replacement: str, case_sensitive: bool) -> tuple[str, int]:
    if not find:
        return value, 0
    if case_sensitive:
        return value.replace(find, replacement), value.count(find)
    pattern = re.compile(re.escape(find), flags=re.IGNORECASE)
    return pattern.subn(replacement, value)


def _safe_text_transform(
    value: Any,
    *,
    find: str,
    replacement: str,
    case_sensitive: bool,
    path: tuple[str, ...] = (),
    allowed: bool = False,
) -> tuple[Any, list[dict[str, Any]]]:
    changes: list[dict[str, Any]] = []
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key, child in value.items():
            child_allowed = key in SAFE_TEXT_KEYS
            transformed, child_changes = _safe_text_transform(
                child,
                find=find,
                replacement=replacement,
                case_sensitive=case_sensitive,
                path=path + (key,),
                allowed=child_allowed,
            )
            result[key] = transformed
            changes.extend(child_changes)
        return result, changes
    if isinstance(value, list):
        result_list: list[Any] = []
        for index, child in enumerate(value):
            transformed, child_changes = _safe_text_transform(
                child,
                find=find,
                replacement=replacement,
                case_sensitive=case_sensitive,
                path=path + (str(index),),
                allowed=allowed,
            )
            result_list.append(transformed)
            changes.extend(child_changes)
        return result_list, changes
    if isinstance(value, str) and allowed:
        updated, count = _replace_text(value, find, replacement, case_sensitive)
        if count:
            changes.append(
                {
                    "path": "$" + "".join(f"[{part}]" if part.isdigit() else f".{part}" for part in path),
                    "occurrences": count,
                    "before": value[:500],
                    "after": updated[:500],
                }
            )
        return updated, changes
    return deepcopy(value), changes


def bulk_replace_preview(
    *,
    find: str,
    replacement: str,
    case_sensitive: bool = False,
    unit_id: str | None = None,
    entity_types: list[str] | None = None,
    limit: int = MAX_BULK_MATCHES,
) -> dict[str, Any]:
    needle = find.strip()
    if len(needle) < 2:
        raise ManagementError("Find text must contain at least two characters")
    allowed_types = set(entity_types or EDITABLE_TYPES)
    invalid = allowed_types - EDITABLE_TYPES
    if invalid:
        raise ManagementError(f"Unsupported bulk entity types: {', '.join(sorted(invalid))}")
    snapshot = admin_catalog.catalog()
    active = _active_draft_rows()
    candidates: list[dict[str, Any]] = []
    safe_limit = max(1, min(int(limit), MAX_BULK_MATCHES))
    for entity in snapshot["entities"].values():
        if entity.get("type") not in allowed_types:
            continue
        if unit_id and entity.get("unit_id") != unit_id:
            continue
        try:
            payload = _editable_base(entity["id"])
        except admin_drafts.DraftError:
            continue
        _new_payload, changes = _safe_text_transform(
            payload,
            find=needle,
            replacement=replacement,
            case_sensitive=case_sensitive,
        )
        if not changes:
            continue
        draft = active.get(entity["id"])
        candidates.append(
            {
                "entity_id": entity["id"],
                "entity_type": entity.get("type"),
                "unit_id": entity.get("unit_id"),
                "title": entity.get("title"),
                "source_state": "draft" if draft else "published",
                "expected_version": int(draft["version"]) if draft else 0,
                "occurrence_count": sum(item["occurrences"] for item in changes),
                "changes": changes[:30],
            }
        )
        if len(candidates) >= safe_limit:
            break
    total_occurrences = sum(item["occurrence_count"] for item in candidates)
    return {
        "schema": MANAGEMENT_SCHEMA,
        "find": needle,
        "replacement": replacement,
        "case_sensitive": case_sensitive,
        "candidate_count": len(candidates),
        "occurrence_count": total_occurrences,
        "candidates": candidates,
        "truncated": len(candidates) >= safe_limit,
    }


def _ensure_editable_draft(entity_id: str, username: str) -> dict[str, Any]:
    active = _active_draft_for_entity(entity_id)
    if active is not None:
        return active
    entity = admin_catalog.get_entity(entity_id)
    if entity is None:
        raise admin_drafts.DraftNotFound("Catalog entity not found")
    if entity.get("type") in MANAGED_TYPES:
        return create_managed_draft(entity_id, username)
    if entity.get("type") in set(admin_editors.editor_types()):
        return admin_editors.create_editor_draft(entity_id, username)
    raise ManagementError("This entity cannot be edited through Step 7 bulk tools")


def bulk_replace_apply(
    *,
    find: str,
    replacement: str,
    case_sensitive: bool,
    targets: list[dict[str, Any]],
    username: str,
) -> dict[str, Any]:
    needle = find.strip()
    if len(needle) < 2:
        raise ManagementError("Find text must contain at least two characters")
    if not targets:
        raise ManagementError("Select at least one bulk replacement target")
    if len(targets) > MAX_BULK_TARGETS:
        raise ManagementError(f"Bulk replacement is limited to {MAX_BULK_TARGETS} records per operation")
    results: list[dict[str, Any]] = []
    for target in targets:
        entity_id = str(target.get("entity_id") or "")
        expected = int(target.get("expected_version") or 0)
        active = _active_draft_for_entity(entity_id)
        if active is not None and expected != int(active["version"]):
            raise admin_drafts.DraftConflict(f"{entity_id} changed after the bulk preview was generated")
        if active is None and expected != 0:
            raise admin_drafts.DraftConflict(f"{entity_id} no longer matches the bulk preview state")
        draft = _ensure_editable_draft(entity_id, username)
        payload, changes = _safe_text_transform(
            draft["payload"],
            find=needle,
            replacement=replacement,
            case_sensitive=case_sensitive,
        )
        if not changes:
            results.append({"entity_id": entity_id, "status": "no_match", "occurrence_count": 0})
            continue
        admin_drafts.create_snapshot(
            draft["draft_id"],
            label=f"Before bulk replace · {needle[:80]}",
            username=username,
        )
        saved = admin_drafts.update_draft(
            draft["draft_id"],
            payload=payload,
            expected_version=int(draft["version"]),
            username=username,
            note=f"Controlled bulk replacement: {needle!r} → {replacement!r}",
            autosave=False,
        )
        results.append(
            {
                "entity_id": entity_id,
                "draft_id": saved["draft_id"],
                "version": saved["version"],
                "status": "updated",
                "occurrence_count": sum(item["occurrences"] for item in changes),
            }
        )
    return {
        "schema": MANAGEMENT_SCHEMA,
        "updated_count": sum(1 for item in results if item["status"] == "updated"),
        "occurrence_count": sum(item["occurrence_count"] for item in results),
        "results": results,
    }


def workspace_search(query: str, *, unit_id: str | None = None, limit: int = 100) -> dict[str, Any]:
    q = query.strip().casefold()
    if len(q) < 2:
        raise ManagementError("Search query must contain at least two characters")
    safe_limit = max(1, min(int(limit), 200))
    results: list[dict[str, Any]] = []
    for entity in admin_catalog.catalog()["entities"].values():
        if unit_id and entity.get("unit_id") != unit_id:
            continue
        haystack = " ".join(
            str(entity.get(key) or "")
            for key in ("id", "title", "canonical_term", "canonical_definition", "prompt", "answer", "locus", "palace_id")
        ).casefold()
        if q in haystack:
            results.append(
                {
                    "source": "catalog",
                    "entity_id": entity["id"],
                    "entity_type": entity.get("type"),
                    "unit_id": entity.get("unit_id"),
                    "title": entity.get("title") or entity.get("canonical_term") or entity["id"],
                }
            )
            if len(results) >= safe_limit:
                break
    if len(results) < safe_limit:
        with admin_drafts._connect() as connection:
            rows = connection.execute("SELECT * FROM content_drafts WHERE status = 'draft' ORDER BY updated_at DESC").fetchall()
        catalog_ids = {item["entity_id"] for item in results}
        for row in rows:
            if unit_id and row["unit_id"] != unit_id:
                continue
            payload = admin_drafts._load(row["payload_json"])
            haystack = admin_drafts._canonical_json(payload).casefold()
            if q not in haystack:
                continue
            if row["entity_id"] in catalog_ids:
                for result in results:
                    if result["entity_id"] == row["entity_id"]:
                        result["source"] = "draft"
                        result["draft_id"] = row["draft_id"]
                        result["version"] = int(row["version"])
                        break
            else:
                results.append(
                    {
                        "source": "new_proposal" if str(row["entity_id"]).startswith("new:") else "draft",
                        "entity_id": row["entity_id"],
                        "entity_type": row["entity_type"],
                        "unit_id": row["unit_id"],
                        "title": row["title"] or row["entity_id"],
                        "draft_id": row["draft_id"],
                        "version": int(row["version"]),
                    }
                )
            if len(results) >= safe_limit:
                break
    for media in list_staged_media(status="staged", limit=safe_limit).get("items", []):
        if len(results) >= safe_limit:
            break
        if unit_id and media.get("unit_id") != unit_id:
            continue
        haystack = " ".join(str(media.get(key) or "") for key in ("original_filename", "alt_text", "caption", "transcript", "entity_id")).casefold()
        if q in haystack:
            results.append(
                {
                    "source": "media",
                    "asset_id": media["asset_id"],
                    "entity_type": "media_asset",
                    "unit_id": media.get("unit_id"),
                    "title": media.get("original_filename"),
                    "kind": media.get("kind"),
                }
            )
    return {"schema": MANAGEMENT_SCHEMA, "query": query, "total": len(results), "items": results[:safe_limit]}


def export_bundle(
    *,
    unit_id: str | None = None,
    entity_types: list[str] | None = None,
    include_drafts: bool = True,
    include_catalog: bool = True,
) -> dict[str, Any]:
    types = set(entity_types or EDITABLE_TYPES)
    active = _active_draft_rows() if include_drafts else {}
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    if include_catalog:
        for entity in admin_catalog.catalog()["entities"].values():
            if entity.get("type") not in types:
                continue
            if unit_id and entity.get("unit_id") != unit_id:
                continue
            entity_id = entity["id"]
            draft_summary = active.get(entity_id)
            if draft_summary and include_drafts:
                payload = admin_drafts.get_draft(draft_summary["draft_id"])["payload"]
                source_state = "draft"
                version = draft_summary["version"]
            else:
                try:
                    payload = _editable_base(entity_id)
                except admin_drafts.DraftError:
                    payload = deepcopy(entity)
                source_state = "published"
                version = 0
            records.append(
                {
                    "entity_id": entity_id,
                    "entity_type": entity.get("type"),
                    "unit_id": entity.get("unit_id"),
                    "source_state": source_state,
                    "version": version,
                    "payload": payload,
                }
            )
            seen.add(entity_id)
    if include_drafts:
        for proposal in _proposal_rows(unit_id=unit_id):
            if proposal.get("entity_type") not in types or proposal["entity_id"] in seen:
                continue
            draft = admin_drafts.get_draft(proposal["draft_id"])
            records.append(
                {
                    "entity_id": proposal["entity_id"],
                    "entity_type": proposal["entity_type"],
                    "unit_id": proposal.get("unit_id"),
                    "source_state": "new_proposal",
                    "version": proposal["version"],
                    "payload": draft["payload"],
                }
            )
    bundle = {
        "schema": PORTABLE_SCHEMA,
        "exported_at": _now(),
        "scope": {"unit_id": unit_id, "entity_types": sorted(types)},
        "record_count": len(records),
        "records": records,
    }
    bundle["fingerprint"] = hashlib.sha256(
        json.dumps(bundle["records"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return bundle


def validate_import_bundle(bundle: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(bundle, dict):
        raise ManagementError("Import payload must be a JSON object")
    if bundle.get("schema") != PORTABLE_SCHEMA:
        raise ManagementError(f"Import bundle must use schema {PORTABLE_SCHEMA}")
    records = bundle.get("records")
    if not isinstance(records, list):
        raise ManagementError("Import bundle records must be a list")
    if len(records) > MAX_IMPORT_RECORDS:
        raise ManagementError(f"Import bundle exceeds the {MAX_IMPORT_RECORDS}-record safety limit")
    active = _active_draft_rows()
    preview: list[dict[str, Any]] = []
    error_count = 0
    for index, record in enumerate(records):
        errors: list[str] = []
        if not isinstance(record, dict):
            preview.append({"index": index, "errors": ["Record must be an object"]})
            error_count += 1
            continue
        entity_id = str(record.get("entity_id") or "")
        entity_type = str(record.get("entity_type") or "")
        unit_id = str(record.get("unit_id") or "")
        payload = record.get("payload")
        if entity_type not in EDITABLE_TYPES:
            errors.append("Unsupported entity type")
        if not isinstance(payload, dict):
            errors.append("Payload must be an object")
        else:
            for key, expected in (("id", entity_id), ("type", entity_type), ("unit_id", unit_id)):
                if payload.get(key) != expected:
                    errors.append(f"Payload {key} does not match the record envelope")
        catalog_entity = admin_catalog.get_entity(entity_id) if entity_id else None
        is_new = entity_id.startswith("new:")
        if catalog_entity is None and not is_new:
            errors.append("Entity ID is neither a current catalog record nor a Step 7 proposal ID")
        if is_new and entity_type not in PROPOSAL_TYPES:
            errors.append("New proposal type is not supported")
        if catalog_entity is not None and catalog_entity.get("type") != entity_type:
            errors.append("Catalog entity type does not match import type")
        if unit_id not in {f"unit-{number}" for number in range(1, 9)}:
            errors.append("Invalid AP Biology unit")
        conflict = active.get(entity_id)
        preview.append(
            {
                "index": index,
                "entity_id": entity_id,
                "entity_type": entity_type,
                "unit_id": unit_id,
                "title": payload.get("title") if isinstance(payload, dict) else None,
                "status": "invalid" if errors else ("conflict" if conflict else ("new" if is_new else "ready")),
                "active_draft": conflict,
                "errors": errors,
            }
        )
        error_count += 1 if errors else 0
    return {
        "schema": MANAGEMENT_SCHEMA,
        "record_count": len(records),
        "error_count": error_count,
        "conflict_count": sum(1 for item in preview if item.get("status") == "conflict"),
        "ready_count": sum(1 for item in preview if item.get("status") in {"ready", "new"}),
        "records": preview,
        "can_apply": error_count == 0,
    }


def apply_import_bundle(bundle: dict[str, Any], *, username: str, conflict_policy: str = "skip") -> dict[str, Any]:
    if conflict_policy not in {"skip", "replace_draft"}:
        raise ManagementError("Import conflict policy must be 'skip' or 'replace_draft'")
    preview = validate_import_bundle(bundle)
    if preview["error_count"]:
        raise ManagementError("Import bundle contains invalid records")
    results: list[dict[str, Any]] = []
    for record in bundle["records"]:
        entity_id = str(record["entity_id"])
        entity_type = str(record["entity_type"])
        unit_id = str(record["unit_id"])
        payload = deepcopy(record["payload"])
        active = _active_draft_for_entity(entity_id)
        if active is not None and conflict_policy == "skip":
            results.append({"entity_id": entity_id, "status": "skipped_conflict", "draft_id": active["draft_id"]})
            continue
        if entity_id.startswith("new:"):
            if active is None:
                created = create_proposed_draft(
                    entity_type,
                    unit_id,
                    str(payload.get("title") or "Imported proposal"),
                    username,
                    seed=payload,
                    entity_id=entity_id,
                )
                active = created
            else:
                admin_drafts.create_snapshot(active["draft_id"], label="Before imported proposal replacement", username=username)
                active = admin_drafts.update_draft(
                    active["draft_id"],
                    payload=payload,
                    expected_version=int(active["version"]),
                    username=username,
                    note="Imported Step 7 proposal replacement",
                )
        else:
            draft = active or _ensure_editable_draft(entity_id, username)
            if active is not None:
                admin_drafts.create_snapshot(draft["draft_id"], label="Before import replacement", username=username)
            active = admin_drafts.update_draft(
                draft["draft_id"],
                payload=payload,
                expected_version=int(draft["version"]),
                username=username,
                note="Imported Content Studio working copy",
            )
        results.append({"entity_id": entity_id, "status": "imported", "draft_id": active["draft_id"], "version": active["version"]})
    return {
        "schema": MANAGEMENT_SCHEMA,
        "imported_count": sum(1 for item in results if item["status"] == "imported"),
        "skipped_count": sum(1 for item in results if item["status"].startswith("skipped")),
        "results": results,
    }


def _media_database_path() -> Path:
    raw = os.getenv(
        "MEMORY_PALACE_ADMIN_MEDIA_DB",
        str(ROOT / "server_data" / "content-studio-media.sqlite3"),
    )
    return Path(raw).expanduser()


def _media_root() -> Path:
    raw = os.getenv(
        "MEMORY_PALACE_ADMIN_MEDIA_DIR",
        str(ROOT / "server_data" / "content-studio-media"),
    )
    root = Path(raw).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    return root


def _media_connect() -> sqlite3.Connection:
    path = _media_database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=5.0)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS media_assets (
            asset_id TEXT PRIMARY KEY,
            original_filename TEXT NOT NULL,
            stored_filename TEXT NOT NULL,
            kind TEXT NOT NULL,
            mime_type TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            sha256 TEXT NOT NULL,
            alt_text TEXT,
            caption TEXT,
            transcript TEXT,
            unit_id TEXT,
            entity_id TEXT,
            status TEXT NOT NULL CHECK(status IN ('staged','archived')),
            version INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            created_by TEXT NOT NULL,
            updated_by TEXT NOT NULL
        )
        """
    )
    connection.execute("CREATE INDEX IF NOT EXISTS idx_media_assets_status ON media_assets(status, updated_at DESC)")
    connection.commit()
    return connection


def _media_row(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "schema": MEDIA_SCHEMA,
        "asset_id": row["asset_id"],
        "original_filename": row["original_filename"],
        "kind": row["kind"],
        "mime_type": row["mime_type"],
        "size_bytes": int(row["size_bytes"]),
        "sha256": row["sha256"],
        "alt_text": row["alt_text"],
        "caption": row["caption"],
        "transcript": row["transcript"],
        "unit_id": row["unit_id"],
        "entity_id": row["entity_id"],
        "status": row["status"],
        "version": int(row["version"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "created_by": row["created_by"],
        "updated_by": row["updated_by"],
    }


def _validate_media_bytes(extension: str, content: bytes) -> None:
    if not content:
        raise ManagementError("Media file is empty")
    checks = {
        ".png": lambda data: data.startswith(b"\x89PNG\r\n\x1a\n"),
        ".jpg": lambda data: data.startswith(b"\xff\xd8\xff"),
        ".jpeg": lambda data: data.startswith(b"\xff\xd8\xff"),
        ".webp": lambda data: len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP",
        ".gif": lambda data: data.startswith((b"GIF87a", b"GIF89a")),
        ".wav": lambda data: len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WAVE",
        ".ogg": lambda data: data.startswith(b"OggS"),
        ".pdf": lambda data: data.startswith(b"%PDF-"),
        ".mp4": lambda data: len(data) >= 12 and data[4:8] == b"ftyp",
        ".m4a": lambda data: len(data) >= 12 and data[4:8] == b"ftyp",
        ".webm": lambda data: data.startswith(b"\x1a\x45\xdf\xa3"),
        ".mp3": lambda data: data.startswith(b"ID3") or (len(data) >= 2 and data[0] == 0xFF and (data[1] & 0xE0) == 0xE0),
    }
    checker = checks.get(extension)
    if checker is not None and not checker(content):
        raise ManagementError("Media file signature does not match its extension")


def stage_media(
    *,
    filename: str,
    content: bytes,
    supplied_mime: str | None,
    kind: str | None,
    unit_id: str | None,
    entity_id: str | None,
    alt_text: str | None,
    caption: str | None,
    transcript: str | None,
    username: str,
) -> dict[str, Any]:
    safe_name = Path(filename).name.strip()
    if not safe_name or safe_name in {".", ".."}:
        raise ManagementError("A valid media filename is required")
    if len(safe_name) > 240:
        raise ManagementError("Media filename is too long")
    extension = Path(safe_name).suffix.lower()
    if extension not in MEDIA_TYPES:
        raise ManagementError("Unsupported media type")
    expected_kind, expected_mime = MEDIA_TYPES[extension]
    if kind and kind != expected_kind:
        raise ManagementError("Media kind does not match the file extension")
    if supplied_mime and supplied_mime not in {expected_mime, "application/octet-stream"}:
        raise ManagementError("Browser media type does not match the file extension")
    if len(content) > MAX_MEDIA_BYTES:
        raise ManagementError("Media file exceeds the 25 MB staging limit")
    _validate_media_bytes(extension, content)
    if unit_id and unit_id not in {f"unit-{number}" for number in range(1, 9)}:
        raise ManagementError("Invalid AP Biology unit")
    if entity_id and not (admin_catalog.get_entity(entity_id) or entity_id.startswith("new:")):
        raise ManagementError("Associated entity ID is not known to Content Studio")

    asset_id = f"asset-{uuid.uuid4().hex}"
    stored_filename = f"{asset_id}{extension}"
    root = _media_root()
    destination = (root / stored_filename).resolve()
    destination.relative_to(root)
    with destination.open("xb") as handle:
        handle.write(content)
    digest = hashlib.sha256(content).hexdigest()
    now = _now()
    try:
        with _media_connect() as connection:
            connection.execute(
                """
                INSERT INTO media_assets(
                    asset_id, original_filename, stored_filename, kind, mime_type,
                    size_bytes, sha256, alt_text, caption, transcript, unit_id, entity_id,
                    status, version, created_at, updated_at, created_by, updated_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'staged', 1, ?, ?, ?, ?)
                """,
                (
                    asset_id,
                    safe_name,
                    stored_filename,
                    expected_kind,
                    expected_mime,
                    len(content),
                    digest,
                    (alt_text or "")[:4000],
                    (caption or "")[:8000],
                    (transcript or "")[:50000],
                    unit_id,
                    entity_id,
                    now,
                    now,
                    username,
                    username,
                ),
            )
            connection.commit()
            row = connection.execute("SELECT * FROM media_assets WHERE asset_id = ?", (asset_id,)).fetchone()
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    return _media_row(row)


def list_staged_media(*, status: str | None = "staged", unit_id: str | None = None, limit: int = 200) -> dict[str, Any]:
    if status not in {None, "", "staged", "archived"}:
        raise ManagementError("Invalid media status")
    clauses: list[str] = []
    params: list[Any] = []
    if status:
        clauses.append("status = ?")
        params.append(status)
    if unit_id:
        clauses.append("unit_id = ?")
        params.append(unit_id)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    safe_limit = max(1, min(int(limit), 500))
    with _media_connect() as connection:
        rows = connection.execute(
            f"SELECT * FROM media_assets {where} ORDER BY updated_at DESC, asset_id LIMIT ?",
            (*params, safe_limit),
        ).fetchall()
    return {"schema": MEDIA_SCHEMA, "items": [_media_row(row) for row in rows]}


def update_media_metadata(
    asset_id: str,
    *,
    expected_version: int,
    alt_text: str | None,
    caption: str | None,
    transcript: str | None,
    unit_id: str | None,
    entity_id: str | None,
    username: str,
) -> dict[str, Any]:
    if unit_id and unit_id not in {f"unit-{number}" for number in range(1, 9)}:
        raise ManagementError("Invalid AP Biology unit")
    if entity_id and not (admin_catalog.get_entity(entity_id) or entity_id.startswith("new:")):
        raise ManagementError("Associated entity ID is not known to Content Studio")
    with _media_connect() as connection:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute("SELECT * FROM media_assets WHERE asset_id = ?", (asset_id,)).fetchone()
        if row is None:
            raise admin_drafts.DraftNotFound("Media asset not found")
        if int(row["version"]) != int(expected_version):
            raise admin_drafts.DraftConflict("Media metadata changed since this editor loaded it")
        new_version = int(row["version"]) + 1
        connection.execute(
            """
            UPDATE media_assets
            SET alt_text = ?, caption = ?, transcript = ?, unit_id = ?, entity_id = ?,
                version = ?, updated_at = ?, updated_by = ?
            WHERE asset_id = ?
            """,
            (
                (alt_text or "")[:4000],
                (caption or "")[:8000],
                (transcript or "")[:50000],
                unit_id,
                entity_id,
                new_version,
                _now(),
                username,
                asset_id,
            ),
        )
        connection.commit()
        updated = connection.execute("SELECT * FROM media_assets WHERE asset_id = ?", (asset_id,)).fetchone()
    return _media_row(updated)


def set_media_status(asset_id: str, *, expected_version: int, status: str, username: str) -> dict[str, Any]:
    if status not in {"staged", "archived"}:
        raise ManagementError("Invalid media status")
    with _media_connect() as connection:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute("SELECT * FROM media_assets WHERE asset_id = ?", (asset_id,)).fetchone()
        if row is None:
            raise admin_drafts.DraftNotFound("Media asset not found")
        if int(row["version"]) != int(expected_version):
            raise admin_drafts.DraftConflict("Media asset changed since this editor loaded it")
        new_version = int(row["version"]) + 1
        connection.execute(
            "UPDATE media_assets SET status = ?, version = ?, updated_at = ?, updated_by = ? WHERE asset_id = ?",
            (status, new_version, _now(), username, asset_id),
        )
        connection.commit()
        updated = connection.execute("SELECT * FROM media_assets WHERE asset_id = ?", (asset_id,)).fetchone()
    return _media_row(updated)


def media_file(asset_id: str) -> tuple[Path, dict[str, Any]]:
    with _media_connect() as connection:
        row = connection.execute("SELECT * FROM media_assets WHERE asset_id = ?", (asset_id,)).fetchone()
    if row is None:
        raise admin_drafts.DraftNotFound("Media asset not found")
    root = _media_root()
    path = (root / row["stored_filename"]).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ManagementError("Invalid staged media path") from exc
    if not path.is_file():
        raise admin_drafts.DraftNotFound("Staged media file is missing")
    return path, _media_row(row)


def existing_media_inventory(limit: int = 1000) -> dict[str, Any]:
    roots = [Path(FRONTEND_DIR).resolve(), APBIO_DIR.resolve()]
    items: list[dict[str, Any]] = []
    safe_limit = max(1, min(int(limit), 2000))
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in MEDIA_TYPES:
                continue
            kind, mime_type = MEDIA_TYPES[path.suffix.lower()]
            try:
                relative = path.relative_to(ROOT.resolve())
            except ValueError:
                continue
            items.append(
                {
                    "path": str(relative).replace(os.sep, "/"),
                    "filename": path.name,
                    "kind": kind,
                    "mime_type": mime_type,
                    "size_bytes": path.stat().st_size,
                    "published": True,
                }
            )
            if len(items) >= safe_limit:
                break
        if len(items) >= safe_limit:
            break
    items.sort(key=lambda item: (item["kind"], item["path"].casefold()))
    return {"schema": MEDIA_SCHEMA, "total": len(items), "items": items, "truncated": len(items) >= safe_limit}
