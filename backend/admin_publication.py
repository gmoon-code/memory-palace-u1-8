from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime, timezone
import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import tempfile
from typing import Any, Iterable
import uuid

import httpx

from . import admin_catalog, admin_drafts, admin_editors, admin_management, admin_quality, course_packages
from .settings import ROOT

PUBLICATION_SCHEMA = "story-method-content-studio-publication-1.0"
RELEASE_SCHEMA = "story-method-content-studio-release-1.0"
CANDIDATE_STATUSES = {
    "created",
    "validated",
    "submitted",
    "merge_ready",
    "merged_pending_verify",
    "released",
    "failed",
}
MAX_DRAFTS_PER_CANDIDATE = 100
JSON_INDENT = 2


class PublicationError(admin_drafts.DraftError):
    pass


class PublicationConflict(PublicationError):
    pass


class PublicationDisabled(PublicationError):
    pass


@dataclass(frozen=True)
class PublicationConfig:
    enabled: bool
    database_path: Path
    publication_root: Path
    github_enabled: bool
    github_repository: str
    github_token: str
    github_base_branch: str
    github_allow_merge: bool
    github_api_url: str

    @classmethod
    def from_env(cls) -> "PublicationConfig":
        def flag(name: str, default: str = "false") -> bool:
            return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}

        return cls(
            enabled=flag("MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED"),
            database_path=Path(
                os.getenv(
                    "MEMORY_PALACE_ADMIN_PUBLICATION_DB",
                    str(ROOT / "server_data" / "content-studio-publication.sqlite3"),
                )
            ).expanduser(),
            publication_root=Path(
                os.getenv(
                    "MEMORY_PALACE_ADMIN_PUBLICATION_DIR",
                    str(ROOT / "server_data" / "content-studio-publications"),
                )
            ).expanduser(),
            github_enabled=flag("MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED"),
            github_repository=os.getenv(
                "MEMORY_PALACE_GITHUB_REPOSITORY",
                "gmoon-code/memory-palace-u1-8",
            ).strip(),
            github_token=os.getenv("MEMORY_PALACE_GITHUB_TOKEN", "").strip(),
            github_base_branch=os.getenv("MEMORY_PALACE_GITHUB_BASE_BRANCH", "main").strip() or "main",
            github_allow_merge=flag("MEMORY_PALACE_GITHUB_ALLOW_MERGE"),
            github_api_url=os.getenv("MEMORY_PALACE_GITHUB_API_URL", "https://api.github.com").rstrip("/"),
        )

    def require_enabled(self) -> None:
        if not self.enabled:
            raise PublicationDisabled("Controlled publication is disabled on this server")

    def require_github(self) -> None:
        self.require_enabled()
        if not self.github_enabled:
            raise PublicationDisabled("GitHub publication is disabled on this server")
        if not self.github_repository or "/" not in self.github_repository:
            raise PublicationError("MEMORY_PALACE_GITHUB_REPOSITORY is invalid")
        if not self.github_token:
            raise PublicationError("MEMORY_PALACE_GITHUB_TOKEN is not configured")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _json_bytes(payload: Any) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=JSON_INDENT) + "\n").encode("utf-8")



def _course_access(course_id: str, *, editable: bool = False) -> dict[str, Any]:
    try:
        access = (
            admin_catalog.require_editable_course(course_id)
            if editable
            else admin_catalog.course_access(course_id)
        )
    except ValueError as exc:
        raise PublicationError(str(exc)) from exc
    if not access.get("catalog_ready"):
        raise PublicationError(f"Content Studio catalog is not available for course '{course_id}'")
    return access


def _safe_repo_path(source_path: str, course_id: str, unit_id: str | None = None) -> Path:
    _course_access(course_id)
    candidate = (ROOT / source_path).resolve()
    root = ROOT.resolve()
    try:
        relative = candidate.relative_to(root).as_posix()
    except ValueError as exc:
        raise PublicationError("Candidate source path escapes the repository root") from exc

    try:
        manifest = course_packages.package_manifest(course_id)
    except course_packages.CoursePackageError as exc:
        raise PublicationError(str(exc)) from exc
    content_root = str(manifest.get("content_root") or "").rstrip("/")
    if not content_root or (relative != content_root and not relative.startswith(f"{content_root}/")):
        raise PublicationError(f"Candidate source path is outside course '{course_id}': {relative}")

    course_file = str(manifest.get("course_file") or "")
    if relative == course_file:
        if candidate.suffix.lower() != ".json" or not candidate.is_file():
            raise PublicationError(f"Published course source is not a readable JSON file: {relative}")
        return candidate

    if not unit_id:
        raise PublicationError(f"Unit identity is required for publication source: {relative}")
    try:
        declared = course_packages.declared_source_file(course_id, unit_id, relative)
    except course_packages.CoursePackageError as exc:
        raise PublicationError(str(exc)) from exc
    if declared.suffix.lower() != ".json":
        raise PublicationError("Controlled publication currently publishes JSON curriculum records only")
    return declared


def _connect(config: PublicationConfig | None = None) -> sqlite3.Connection:
    cfg = config or PublicationConfig.from_env()
    cfg.database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(cfg.database_path, timeout=5.0)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA foreign_keys=ON")
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS publication_candidates (
            candidate_id TEXT PRIMARY KEY,
            course_id TEXT NOT NULL DEFAULT 'ap-biology',
            kind TEXT NOT NULL,
            title TEXT NOT NULL,
            notes TEXT,
            status TEXT NOT NULL,
            warnings_acknowledged INTEGER NOT NULL,
            manifest_json TEXT NOT NULL,
            validation_json TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            created_by TEXT NOT NULL,
            github_branch TEXT,
            github_pr_number INTEGER,
            github_commit_sha TEXT,
            github_merge_sha TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS publication_releases (
            release_id TEXT PRIMARY KEY,
            candidate_id TEXT NOT NULL,
            course_id TEXT NOT NULL DEFAULT 'ap-biology',
            title TEXT NOT NULL,
            summary_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            created_by TEXT NOT NULL,
            github_merge_sha TEXT,
            FOREIGN KEY(candidate_id) REFERENCES publication_candidates(candidate_id)
        )
        """
    )
    candidate_columns = {
        str(row["name"])
        for row in connection.execute("PRAGMA table_info(publication_candidates)").fetchall()
    }
    if "course_id" not in candidate_columns:
        connection.execute(
            "ALTER TABLE publication_candidates ADD COLUMN course_id TEXT NOT NULL DEFAULT 'ap-biology'"
        )
    release_columns = {
        str(row["name"])
        for row in connection.execute("PRAGMA table_info(publication_releases)").fetchall()
    }
    if "course_id" not in release_columns:
        connection.execute(
            "ALTER TABLE publication_releases ADD COLUMN course_id TEXT NOT NULL DEFAULT 'ap-biology'"
        )
    connection.execute(
        "CREATE INDEX IF NOT EXISTS idx_publication_candidates_updated ON publication_candidates(updated_at DESC)"
    )
    connection.execute(
        "CREATE INDEX IF NOT EXISTS idx_publication_candidates_course_updated ON publication_candidates(course_id, updated_at DESC)"
    )
    connection.execute(
        "CREATE INDEX IF NOT EXISTS idx_publication_releases_created ON publication_releases(created_at DESC)"
    )
    connection.execute(
        "CREATE INDEX IF NOT EXISTS idx_publication_releases_course_created ON publication_releases(course_id, created_at DESC)"
    )
    connection.commit()
    return connection

def _candidate_dir(candidate_id: str, config: PublicationConfig | None = None) -> Path:
    cfg = config or PublicationConfig.from_env()
    root = cfg.publication_root.expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    candidate = (root / "candidates" / candidate_id).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise PublicationError("Invalid publication candidate path") from exc
    return candidate


def _candidate_row(row: sqlite3.Row) -> dict[str, Any]:
    manifest = json.loads(row["manifest_json"])
    validation = json.loads(row["validation_json"]) if row["validation_json"] else None
    return {
        "schema": PUBLICATION_SCHEMA,
        "course_id": row["course_id"],
        "candidate_id": row["candidate_id"],
        "kind": row["kind"],
        "title": row["title"],
        "notes": row["notes"],
        "status": row["status"],
        "warnings_acknowledged": bool(row["warnings_acknowledged"]),
        "manifest": manifest,
        "validation": validation,
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
        "created_by": row["created_by"],
        "github": {
            "branch": row["github_branch"],
            "pr_number": row["github_pr_number"],
            "commit_sha": row["github_commit_sha"],
            "merge_sha": row["github_merge_sha"],
        },
    }


def _release_row(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "schema": RELEASE_SCHEMA,
        "course_id": row["course_id"],
        "release_id": row["release_id"],
        "candidate_id": row["candidate_id"],
        "title": row["title"],
        "summary": json.loads(row["summary_json"]),
        "created_at": row["created_at"],
        "created_by": row["created_by"],
        "github_merge_sha": row["github_merge_sha"],
    }



def publication_status(course_id: str = "ap-biology") -> dict[str, Any]:
    access = _course_access(course_id)
    cfg = PublicationConfig.from_env()
    candidate_count = 0
    release_count = 0
    if cfg.enabled:
        with _connect(cfg) as connection:
            candidate_count = int(
                connection.execute(
                    "SELECT COUNT(*) AS n FROM publication_candidates WHERE course_id = ?",
                    (course_id,),
                ).fetchone()["n"]
            )
            release_count = int(
                connection.execute(
                    "SELECT COUNT(*) AS n FROM publication_releases WHERE course_id = ?",
                    (course_id,),
                ).fetchone()["n"]
            )
    return {
        "schema": PUBLICATION_SCHEMA,
        "course_id": course_id,
        "course_title": access.get("title") or access.get("course_title") or course_id,
        "course_editable": bool(access.get("editable")),
        "publication_enabled": cfg.enabled,
        "github_enabled": cfg.github_enabled,
        "github_configured": bool(cfg.github_repository and cfg.github_token),
        "github_repository": cfg.github_repository if cfg.github_enabled else None,
        "github_base_branch": cfg.github_base_branch if cfg.github_enabled else None,
        "github_merge_enabled": cfg.github_allow_merge,
        "candidate_count": candidate_count,
        "release_count": release_count,
        "published_content_direct_write": False,
        "candidate_storage": "server-side isolated package",
        "release_gate": "candidate validation plus GitHub Actions before merge",
    }


def _active_changed_drafts(course_id: str = "ap-biology") -> list[dict[str, Any]]:
    _course_access(course_id)
    result: list[dict[str, Any]] = []
    for summary in admin_drafts.list_drafts(
        course_id=course_id,
        status="draft",
        limit=500,
    ).get("items", []):
        draft = admin_drafts.get_draft(summary["draft_id"], course_id=course_id)
        if not draft.get("changed_from_base") and not str(draft.get("entity_id") or "").startswith("new:"):
            continue
        result.append(draft)
    return result


def eligible_drafts(course_id: str = "ap-biology") -> dict[str, Any]:
    access = _course_access(course_id)
    items: list[dict[str, Any]] = []
    for draft in _active_changed_drafts(course_id):
        try:
            quality = admin_quality.entity_quality(
                draft["entity_id"],
                draft_id=draft["draft_id"],
                source="draft",
                course_id=course_id,
            )
            supported, reason = _publication_support(draft, draft.get("payload") or {})
        except admin_drafts.DraftError as exc:
            quality = {"error_count": 1, "warning_count": 0, "advisory_count": 0, "findings": []}
            supported, reason = False, str(exc)
        items.append(
            {
                "course_id": course_id,
                "draft_id": draft["draft_id"],
                "entity_id": draft["entity_id"],
                "entity_type": draft["entity_type"],
                "unit_id": draft.get("unit_id"),
                "title": draft.get("title"),
                "version": draft["version"],
                "payload_fingerprint": draft.get("payload_fingerprint"),
                "quality": {
                    "errors": int(quality.get("error_count") or 0),
                    "warnings": int(quality.get("warning_count") or 0),
                    "advisories": int(quality.get("advisory_count") or 0),
                },
                "publication_supported": bool(access.get("editable")) and supported,
                "publication_note": (
                    reason
                    if access.get("editable")
                    else "Publication writes are disabled for this read-only course"
                ),
            }
        )
    items.sort(key=lambda item: (item.get("unit_id") or "", item["entity_type"], str(item.get("title") or "").casefold()))
    return {
        "schema": PUBLICATION_SCHEMA,
        "course_id": course_id,
        "course_editable": bool(access.get("editable")),
        "items": items,
        "count": len(items),
    }


def _publication_support(draft: dict[str, Any], payload: dict[str, Any]) -> tuple[bool, str]:
    course_id = str(draft.get("course_id") or payload.get("course_id") or "ap-biology")
    entity_type = str(draft.get("entity_type") or "")
    entity_id = str(draft.get("entity_id") or "")
    unit_id = str(draft.get("unit_id") or payload.get("unit_id") or "")
    if entity_type in set(admin_editors.editor_types()):
        if entity_type in {"location", "character"}:
            return True, "Published through the owning journey scene records"
        entity = admin_catalog.get_entity(entity_id, course_id)
        if entity and entity.get("source_path"):
            return True, "Source-backed editor record"
        return False, "The record has no publishable source path"
    if entity_type not in admin_management.MANAGED_TYPES:
        return False, "This entity type is not supported by the current student runtime"
    if not entity_id.startswith("new:"):
        return True, "Existing assessment or application record"

    artifact_name: str | None = None
    if entity_type == "challenge":
        artifact_name = "challenge_lab"
    elif entity_type == "question_set":
        artifact_name = "mixed_discrimination"
    elif entity_type == "question":
        question_type = str(payload.get("question_type") or "")
        if question_type == "review":
            artifact_name = "review"
        elif question_type == "mixed_discrimination" and payload.get("set_id"):
            artifact_name = "mixed_discrimination"
        else:
            return False, "New standalone teacher-created questions have no student-runtime destination yet"

    if artifact_name:
        try:
            path = course_packages.artifact_source_path(course_id, unit_id, artifact_name)
        except course_packages.CoursePackageError as exc:
            return False, str(exc)
        if not path:
            return False, f"The selected course unit has no file-backed {artifact_name} publication destination"
        return True, f"New proposal uses the package-declared {artifact_name} destination"
    return False, "This proposal has no compatible student-runtime publication destination"


def _read_json(
    path: str,
    docs: dict[str, Any],
    before_bytes: dict[str, bytes],
    *,
    course_id: str,
    unit_id: str | None = None,
) -> Any:
    if path not in docs:
        source = _safe_repo_path(path, course_id, unit_id)
        raw = source.read_bytes()
        before_bytes[path] = raw
        try:
            docs[path] = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PublicationError(f"Published source is not valid UTF-8 JSON: {path}") from exc
    return docs[path]

def _records_container(payload: Any, keys: Iterable[str]) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in keys:
            value = payload.get(key)
            if isinstance(value, list):
                return value
    raise PublicationError("Source record collection could not be located")


def _set_alias(record: dict[str, Any], normalized: str, value: Any, aliases: Iterable[str]) -> None:
    for key in aliases:
        if key in record:
            record[key] = deepcopy(value)
            return
    record[normalized] = deepcopy(value)



def _source_path(entity_id: str, course_id: str) -> str:
    entity = admin_catalog.get_entity(entity_id, course_id)
    path = str((entity or {}).get("source_path") or "")
    if not path:
        raise PublicationError(f"No source path is indexed for {entity_id}")
    return path


def _unit_artifact_file(course_id: str, unit_id: str, artifact_name: str) -> str:
    try:
        path = course_packages.artifact_source_path(course_id, unit_id, artifact_name)
    except course_packages.CoursePackageError as exc:
        raise PublicationError(str(exc)) from exc
    if not path:
        raise PublicationError(
            f"Course package has no file-backed '{artifact_name}' destination for {course_id}/{unit_id}"
        )
    _safe_repo_path(path, course_id, unit_id)
    return path

def _scene_record(journey: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    scenes = journey.get("scenes")
    if not isinstance(scenes, list):
        raise PublicationError("Journey source has no scene list")
    locus_id = payload.get("locus_id")
    scene_index = payload.get("scene_index")
    for index, scene in enumerate(scenes):
        if not isinstance(scene, dict):
            continue
        if locus_id and scene.get("locus_id") == locus_id:
            return scene
        if scene_index is not None and int(scene.get("scene_index", index)) == int(scene_index):
            return scene
    raise PublicationError("Scene could not be located in its published journey")


def _apply_scene_fields(scene: dict[str, Any], payload: dict[str, Any]) -> None:
    for key in (
        "title", "scene_kicker", "locus", "location_description", "scene_layout", "cast",
        "continuity_object", "story_open", "story_paragraphs", "story_beats", "story_close",
        "object_ids", "checkpoint", "checkpoint_object_id", "checkpoint_prompt", "next_locus",
    ):
        if key in payload:
            scene[key] = deepcopy(payload[key])



def _apply_unit(
    draft: dict[str, Any],
    payload: dict[str, Any],
    docs: dict[str, Any],
    before: dict[str, bytes],
) -> list[str]:
    course_id = str(draft.get("course_id") or payload.get("course_id") or "ap-biology")
    try:
        manifest = course_packages.package_manifest(course_id)
    except course_packages.CoursePackageError as exc:
        raise PublicationError(str(exc)) from exc
    path = str(manifest.get("course_file") or "")
    course = _read_json(path, docs, before, course_id=course_id)
    units = course.get("units") if isinstance(course, dict) else None
    if not isinstance(units, list):
        raise PublicationError("Course registry has no unit list")
    unit_id = str(draft.get("unit_id") or payload.get("unit_id") or "")
    record = next((item for item in units if isinstance(item, dict) and item.get("unit_id") == unit_id), None)
    if record is None:
        raise PublicationError("Unit record is missing from the selected course metadata")
    for key in ("title", "status", "subtitle", "description", "introduction", "instructions", "prerequisites", "ap_mapping", "conclusion"):
        if key in payload:
            record[key] = deepcopy(payload[key])
    return [path]


def _apply_journey_or_scene(
    draft: dict[str, Any],
    payload: dict[str, Any],
    docs: dict[str, Any],
    before: dict[str, bytes],
) -> list[str]:
    course_id = str(draft.get("course_id") or payload.get("course_id") or "ap-biology")
    unit_id = str(draft.get("unit_id") or payload.get("unit_id") or "")
    entity_id = str(draft["entity_id"])
    path = _source_path(entity_id, course_id)
    journey = _read_json(path, docs, before, course_id=course_id, unit_id=unit_id)
    if draft["entity_type"] == "journey":
        for key in (
            "story_title", "palace_name", "tagline", "premise", "mission", "finale",
            "estimated_minutes", "learner_rule", "route_orientation", "guide", "route",
            "student_release", "preview_release", "narrative_design",
        ):
            if key in payload:
                journey[key] = deepcopy(payload[key])
    else:
        _apply_scene_fields(_scene_record(journey, payload), payload)
    return [path]


def _apply_concept(
    draft: dict[str, Any],
    payload: dict[str, Any],
    docs: dict[str, Any],
    before: dict[str, bytes],
) -> list[str]:
    course_id = str(draft.get("course_id") or payload.get("course_id") or "ap-biology")
    unit_id = str(draft.get("unit_id") or payload.get("unit_id") or "")
    path = _source_path(str(draft["entity_id"]), course_id)
    source = _read_json(path, docs, before, course_id=course_id, unit_id=unit_id)
    records = _records_container(source, ("canonical_records", "canonical_catalog", "records", "items"))
    target = str(payload.get("knowledge_id") or "")
    match = None
    for record in records:
        raw = record.get("knowledge_id") or record.get("Knowledge ID") or record.get("source_knowledge_id") or record.get("record_id") or record.get("id")
        if str(raw or "") == target:
            match = record
            break
    if match is None:
        raise PublicationError("Canonical concept record could not be located")
    mapping = {
        "canonical_term": ("canonical_label", "Canonical Label", "canonical_term", "term", "label", "title"),
        "canonical_definition": ("canonical_verified_statement", "Canonical Verified Statement", "canonical_definition", "definition", "statement"),
        "topic": ("topic", "Topic", "ced_topic", "CED Topic"),
        "scope_class": ("scope_class", "Scope Class", "ap_scope_class", "AP Scope Class"),
        "source_reference": ("source_reference", "Source Reference", "source_trace", "Source Trace"),
        "scientific_lock_status": ("scientific_lock_status", "canonical_lock", "Canonical Lock"),
        "prerequisites": ("prerequisites", "prerequisite_ids"),
        "related_concepts": ("related_concepts", "relationships", "related_ids"),
        "misconceptions": ("misconceptions", "common_misconceptions", "confusable_terms"),
        "teacher_notes": ("teacher_notes", "notes"),
    }
    for key, aliases in mapping.items():
        if key in payload:
            _set_alias(match, key, payload[key], aliases)
    return [path]


def _apply_memory(
    draft: dict[str, Any],
    payload: dict[str, Any],
    docs: dict[str, Any],
    before: dict[str, bytes],
) -> list[str]:
    course_id = str(draft.get("course_id") or payload.get("course_id") or "ap-biology")
    unit_id = str(draft.get("unit_id") or payload.get("unit_id") or "")
    path = _source_path(str(draft["entity_id"]), course_id)
    source = _read_json(path, docs, before, course_id=course_id, unit_id=unit_id)
    records = _records_container(source, ("memory_objects", "records", "items"))
    target = str(payload.get("memory_object_id") or "")
    match = None
    for record in records:
        raw = record.get("memory_object_id") or record.get("object_id") or record.get("knowledge_id")
        if str(raw or "") == target:
            match = record
            break
    if match is None:
        raise PublicationError("Memory Object record could not be located")
    mapping = {
        "canonical_term": ("canonical_term", "canonical_label", "term", "title"),
        "canonical_definition": ("canonical_definition", "canonical_verified_statement", "definition"),
        "pronunciation": ("pronunciation", "phonetic_pronunciation", "pronunciation_guide"),
        "word_structure": ("word_structure", "morphology", "word_parts"),
        "phonological_keyword": ("phonological_keyword", "phonetic_keyword", "keyword"),
        "mnemonic_actor": ("mnemonic_actor", "mnemonic_character", "actor"),
        "mnemonic_object": ("mnemonic_object", "visual_object", "object"),
        "function_interaction": ("function_interaction", "function_or_interaction", "interaction"),
        "palace_zone": ("palace_zone",),
        "primary_palace_locus": ("primary_palace_locus",),
        "confusable_terms": ("confusable_terms", "confusable_set_ids"),
        "productive_retrieval_target": ("productive_retrieval_target",),
        "exact_name_required": ("exact_name_required",),
        "exact_spelling_required": ("exact_spelling_required",),
        "spelling_retrieval_target": ("spelling_retrieval_target", "required_spelling_retrieval"),
        "application_question": ("application_question",),
        "locus_id": ("locus_id",),
        "scene_index": ("scene_index",),
        "source_trace": ("source_trace", "source_reference"),
        "version_status": ("version_status",),
    }
    for key, aliases in mapping.items():
        if key in payload:
            _set_alias(match, key, payload[key], aliases)
    return [path]


def _apply_location(
    draft: dict[str, Any],
    payload: dict[str, Any],
    docs: dict[str, Any],
    before: dict[str, bytes],
) -> list[str]:
    course_id = str(draft.get("course_id") or payload.get("course_id") or "ap-biology")
    unit_id = str(draft.get("unit_id") or payload.get("unit_id") or "")
    entity = admin_catalog.get_entity(str(draft["entity_id"]), course_id) or {}
    scene_id = str(entity.get("scene_id") or "")
    scene_entity = admin_catalog.get_entity(scene_id, course_id) or {}
    path = str(scene_entity.get("source_path") or "")
    if not path:
        raise PublicationError("Location has no owning scene source")
    journey = _read_json(path, docs, before, course_id=course_id, unit_id=unit_id)
    scene_payload = {
        "scene_index": scene_entity.get("scene_index"),
        "locus_id": scene_entity.get("locus_id"),
    }
    scene = _scene_record(journey, scene_payload)
    if "title" in payload:
        scene["title"] = deepcopy(payload["title"])
    if "locus" in payload:
        scene["locus"] = deepcopy(payload["locus"])
    if "description" in payload:
        scene["location_description"] = deepcopy(payload["description"])
    layout = deepcopy(scene.get("scene_layout") or {})
    if "orientation" in payload:
        layout["orientation"] = deepcopy(payload["orientation"])
    if "zones" in payload:
        layout["zones"] = deepcopy(payload["zones"])
    scene["scene_layout"] = layout
    return [path]


def _apply_character(
    draft: dict[str, Any],
    payload: dict[str, Any],
    docs: dict[str, Any],
    before: dict[str, bytes],
) -> list[str]:
    course_id = str(draft.get("course_id") or payload.get("course_id") or "ap-biology")
    unit_id = str(draft.get("unit_id") or payload.get("unit_id") or "")
    entity = admin_catalog.get_entity(str(draft["entity_id"]), course_id) or {}
    original_name = str(entity.get("name") or entity.get("title") or "")
    if not original_name:
        raise PublicationError("Character source identity is missing")
    touched: list[str] = []
    journey_ids = [str(item) for item in entity.get("journey_ids", [])]
    for journey_id in journey_ids:
        journey_entity = admin_catalog.get_entity(journey_id, course_id) or {}
        path = str(journey_entity.get("source_path") or "")
        if not path:
            continue
        journey = _read_json(path, docs, before, course_id=course_id, unit_id=unit_id)
        changed = False
        guide = journey.get("guide") if isinstance(journey, dict) else None
        candidates: list[dict[str, Any]] = []
        if isinstance(guide, dict):
            candidates.append(guide)
        for scene in journey.get("scenes", []) if isinstance(journey, dict) else []:
            if isinstance(scene, dict):
                candidates.extend(item for item in scene.get("cast", []) if isinstance(item, dict))
        for record in candidates:
            if str(record.get("name") or "").casefold() != original_name.casefold():
                continue
            mapping = {"name": "name", "kind": "kind", "role": "role", "visual": "visual", "job": "job"}
            for source_key, target_key in mapping.items():
                if source_key in payload:
                    record[target_key] = deepcopy(payload[source_key])
                    changed = True
        if changed:
            touched.append(path)
    if not touched:
        raise PublicationError("Character could not be located in its owning journey sources")
    return touched

def _find_record(records: list[dict[str, Any]], predicate) -> dict[str, Any] | None:
    return next((item for item in records if isinstance(item, dict) and predicate(item)), None)



def _apply_managed(
    draft: dict[str, Any],
    payload: dict[str, Any],
    docs: dict[str, Any],
    before: dict[str, bytes],
    candidate_id: str,
) -> list[str]:
    course_id = str(draft.get("course_id") or payload.get("course_id") or "ap-biology")
    entity_id = str(draft["entity_id"])
    entity_type = str(draft["entity_type"])
    unit_id = str(draft.get("unit_id") or payload.get("unit_id") or "")
    try:
        unit = course_packages.unit(course_id, unit_id)
    except course_packages.CoursePackageError as exc:
        raise PublicationError(str(exc)) from exc
    if unit is None:
        raise PublicationError(f"Managed content must belong to a declared unit in course '{course_id}'")
    is_new = entity_id.startswith("new:")

    if entity_type == "challenge":
        path = (
            _source_path(entity_id, course_id)
            if not is_new
            else _unit_artifact_file(course_id, unit_id, "challenge_lab")
        )
        source = _read_json(path, docs, before, course_id=course_id, unit_id=unit_id)
        records = _records_container(source, ("items", "challenges", "records"))
        if is_new:
            record = deepcopy(payload)
            for key in ("id", "type", "course_id", "unit_id", "proposal"):
                record.pop(key, None)
            record["challenge_id"] = record.get("challenge_id") or f"CS-{candidate_id[-8:]}-{len(records)+1:03d}"
            records.append(record)
        else:
            target = str(
                payload.get("challenge_id")
                or (admin_catalog.get_entity(entity_id, course_id) or {}).get("challenge_id")
                or ""
            )
            record = _find_record(records, lambda item: str(item.get("challenge_id") or "") == target)
            if record is None:
                raise PublicationError("Challenge Lab record could not be located")
            for key, value in payload.items():
                if key not in {"id", "type", "course_id", "unit_id", "source_path", "dependency_counts", "coverage"}:
                    record[key] = deepcopy(value)
        return [path]

    if entity_type == "question_set":
        path = (
            _source_path(entity_id, course_id)
            if not is_new
            else _unit_artifact_file(course_id, unit_id, "mixed_discrimination")
        )
        source = _read_json(path, docs, before, course_id=course_id, unit_id=unit_id)
        sets = _records_container(source, ("sets", "records", "items"))
        if is_new:
            record = deepcopy(payload)
            for key in ("id", "type", "course_id", "unit_id", "proposal"):
                record.pop(key, None)
            record["set_id"] = record.get("set_id") or f"CS-{candidate_id[-8:]}-{len(sets)+1:03d}"
            sets.append(record)
        else:
            target = str(
                payload.get("set_id")
                or (admin_catalog.get_entity(entity_id, course_id) or {}).get("set_id")
                or ""
            )
            record = _find_record(sets, lambda item: str(item.get("set_id") or "") == target)
            if record is None:
                raise PublicationError("Question set could not be located")
            for key, value in payload.items():
                if key not in {"id", "type", "course_id", "unit_id", "source_path", "dependency_counts", "coverage"}:
                    record[key] = deepcopy(value)
        return [path]

    if entity_type != "question":
        raise PublicationError("Unsupported managed content type")
    question_type = str(payload.get("question_type") or "")

    if question_type == "quick_recall" and not is_new:
        entity = admin_catalog.get_entity(entity_id, course_id) or {}
        scene = admin_catalog.get_entity(str(entity.get("scene_id") or ""), course_id) or {}
        path = str(scene.get("source_path") or "")
        if not path:
            raise PublicationError("Quick Recall has no owning scene source")
        journey = _read_json(path, docs, before, course_id=course_id, unit_id=unit_id)
        target_scene = _scene_record(journey, scene)
        target_scene["checkpoint"] = bool((payload.get("quick_recall") or {}).get("checkpoint", True))
        if "prompt" in payload:
            target_scene["checkpoint_prompt"] = deepcopy(payload["prompt"])
        knowledge = payload.get("knowledge_ids") or []
        if knowledge:
            target_scene["checkpoint_object_id"] = knowledge[0]
        return [path]

    if question_type == "review":
        path = (
            _source_path(entity_id, course_id)
            if not is_new
            else _unit_artifact_file(course_id, unit_id, "review")
        )
        source = _read_json(path, docs, before, course_id=course_id, unit_id=unit_id)
        records = _records_container(source, ("targets", "records", "items"))
        if is_new:
            record = deepcopy(payload)
            for key in ("id", "type", "course_id", "unit_id", "proposal"):
                record.pop(key, None)
            knowledge = record.get("knowledge_ids") or []
            if knowledge and not record.get("knowledge_id"):
                record["knowledge_id"] = knowledge[0]
            if record.get("answer") and not record.get("target_answer"):
                record["target_answer"] = record["answer"]
            if record.get("explanation") and not record.get("canonical_science"):
                record["canonical_science"] = record["explanation"]
            records.append(record)
        else:
            base = admin_catalog.get_entity(entity_id, course_id) or {}
            knowledge = [str(item) for item in payload.get("knowledge_ids", [])]
            record = _find_record(
                records,
                lambda item: (
                    knowledge
                    and str(item.get("knowledge_id") or item.get("memory_object_id") or item.get("object_id") or "") in knowledge
                    and (not base.get("prompt") or item.get("prompt") == base.get("prompt"))
                ),
            )
            if record is None:
                record = _find_record(records, lambda item: base.get("prompt") and item.get("prompt") == base.get("prompt"))
            if record is None:
                raise PublicationError("Review question could not be located")
            if "prompt" in payload:
                record["prompt"] = deepcopy(payload["prompt"])
            if payload.get("answer") is not None:
                record["target_answer"] = deepcopy(payload.get("answer"))
            if payload.get("explanation") is not None:
                record["canonical_science"] = deepcopy(payload.get("explanation"))
            if knowledge:
                record["knowledge_id"] = knowledge[0]
        return [path]

    if question_type == "mixed_discrimination":
        path = (
            _source_path(entity_id, course_id)
            if not is_new
            else _unit_artifact_file(course_id, unit_id, "mixed_discrimination")
        )
        source = _read_json(path, docs, before, course_id=course_id, unit_id=unit_id)
        sets = _records_container(source, ("sets", "records", "items"))
        if is_new:
            set_id = str(payload.get("set_id") or "")
            question_set = _find_record(sets, lambda item: str(item.get("set_id") or "") == set_id)
            if question_set is None:
                raise PublicationError("New mixed-discrimination questions must target an existing set_id")
            questions = question_set.setdefault("questions", [])
            record = deepcopy(payload)
            for key in ("id", "type", "course_id", "unit_id", "proposal", "set_id"):
                record.pop(key, None)
            record["question_id"] = record.get("question_id") or f"CS-{candidate_id[-8:]}-{len(questions)+1:03d}"
            questions.append(record)
        else:
            base = admin_catalog.get_entity(entity_id, course_id) or {}
            raw_id = entity_id.split(":", 2)[-1]
            match = None
            for question_set in sets:
                for question in question_set.get("questions", []) if isinstance(question_set, dict) else []:
                    if not isinstance(question, dict):
                        continue
                    if str(question.get("question_id") or "") == raw_id or (
                        base.get("prompt") and question.get("prompt") == base.get("prompt")
                    ):
                        match = question
                        break
                if match is not None:
                    break
            if match is None:
                raise PublicationError("Mixed-discrimination question could not be located")
            for key, value in payload.items():
                if key not in {"id", "type", "course_id", "unit_id", "source_path", "dependency_counts", "coverage", "set_id"}:
                    match[key] = deepcopy(value)
        return [path]

    raise PublicationError("This question type has no compatible student-runtime publication destination")

def _apply_draft(draft: dict[str, Any], docs: dict[str, Any], before: dict[str, bytes], candidate_id: str) -> list[str]:
    payload = deepcopy(draft.get("payload") or {})
    supported, reason = _publication_support(draft, payload)
    if not supported:
        raise PublicationError(f"{draft['entity_id']}: {reason}")
    entity_type = str(draft["entity_type"])
    if entity_type == "unit":
        return _apply_unit(draft, payload, docs, before)
    if entity_type in {"journey", "scene"}:
        return _apply_journey_or_scene(draft, payload, docs, before)
    if entity_type == "concept":
        return _apply_concept(draft, payload, docs, before)
    if entity_type == "memory_object":
        return _apply_memory(draft, payload, docs, before)
    if entity_type == "location":
        return _apply_location(draft, payload, docs, before)
    if entity_type == "character":
        return _apply_character(draft, payload, docs, before)
    if entity_type in admin_management.MANAGED_TYPES:
        return _apply_managed(draft, payload, docs, before, candidate_id)
    raise PublicationError(f"Unsupported publication entity type: {entity_type}")



def _candidate_manifest_draft(draft: dict[str, Any]) -> dict[str, Any]:
    course_id = str(draft.get("course_id") or "ap-biology")
    quality = admin_quality.entity_quality(
        draft["entity_id"],
        draft_id=draft["draft_id"],
        source="draft",
        course_id=course_id,
    )
    entity = admin_catalog.get_entity(draft["entity_id"], course_id)
    dependency = (
        admin_catalog.dependency_report(
            draft["entity_id"],
            course_id=course_id,
            depth=2,
            limit=500,
        )
        if entity
        else None
    )
    return {
        "course_id": course_id,
        "draft_id": draft["draft_id"],
        "entity_id": draft["entity_id"],
        "entity_type": draft["entity_type"],
        "unit_id": draft.get("unit_id"),
        "title": draft.get("title"),
        "version": int(draft["version"]),
        "payload_fingerprint": draft["payload_fingerprint"],
        "quality": {
            "error_count": int(quality.get("error_count") or 0),
            "warning_count": int(quality.get("warning_count") or 0),
            "advisory_count": int(quality.get("advisory_count") or 0),
            "findings": quality.get("findings", []),
        },
        "dependency_counts": dependency.get("related_counts_by_type", {}) if dependency else {},
    }

def _write_candidate_files(candidate_id: str, docs: dict[str, Any], before: dict[str, bytes], config: PublicationConfig) -> list[dict[str, Any]]:
    root = _candidate_dir(candidate_id, config)
    if root.exists():
        raise PublicationConflict("Candidate package already exists")
    (root / "before").mkdir(parents=True, exist_ok=False)
    (root / "after").mkdir(parents=True, exist_ok=False)
    files: list[dict[str, Any]] = []
    for path in sorted(docs):
        old = before[path]
        new = _json_bytes(docs[path])
        if old == new:
            continue
        before_path = root / "before" / path
        after_path = root / "after" / path
        before_path.parent.mkdir(parents=True, exist_ok=True)
        after_path.parent.mkdir(parents=True, exist_ok=True)
        before_path.write_bytes(old)
        after_path.write_bytes(new)
        files.append(
            {
                "path": path,
                "before_sha256": _sha_bytes(old),
                "after_sha256": _sha_bytes(new),
                "before_bytes": len(old),
                "after_bytes": len(new),
            }
        )
    if not files:
        shutil.rmtree(root, ignore_errors=True)
        raise PublicationError("Selected drafts do not produce a publishable file change")
    return files



def _release_summary_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        f"# {manifest['title']}",
        "",
        f"Course `{manifest.get('course_id') or 'ap-biology'}`",
        "",
        f"Candidate `{manifest['candidate_id']}`",
        "",
        manifest.get("notes") or "No release notes supplied.",
        "",
        "## Working copies",
        "",
    ]
    for draft in manifest.get("drafts", []):
        lines.append(f"- `{draft['entity_id']}` · {draft.get('title') or 'Untitled'} · draft v{draft['version']}")
    if not manifest.get("drafts"):
        lines.append("- Rollback package generated from a prior release.")
    lines.extend(["", "## Files", ""])
    for item in manifest.get("files", []):
        lines.append(f"- `{item['path']}` · `{item['before_sha256'][:12]}` → `{item['after_sha256'][:12]}`")
    lines.extend(
        [
            "",
            "## Safety gates",
            "",
            f"- Publication errors at candidate creation · {manifest.get('error_count', 0)}",
            f"- Teacher-review warnings · {manifest.get('warning_count', 0)}",
            f"- Warnings acknowledged · {bool(manifest.get('warnings_acknowledged'))}",
            "- Local source files modified during candidate creation · false",
            "- GitHub merge requires a separately validated candidate · true",
        ]
    )
    return "\n".join(lines) + "\n"


def create_candidate(
    draft_ids: list[str],
    *,
    title: str,
    notes: str | None,
    warnings_acknowledged: bool,
    username: str,
    course_id: str = "ap-biology",
) -> dict[str, Any]:
    config = PublicationConfig.from_env()
    config.require_enabled()
    access = _course_access(course_id, editable=True)
    clean_ids = list(dict.fromkeys(str(item) for item in draft_ids if str(item).strip()))
    if not clean_ids:
        raise PublicationError("Select at least one changed working copy")
    if len(clean_ids) > MAX_DRAFTS_PER_CANDIDATE:
        raise PublicationError(f"A candidate may contain at most {MAX_DRAFTS_PER_CANDIDATE} working copies")
    clean_title = title.strip()[:300]
    if not clean_title:
        raise PublicationError("A release title is required")

    candidate_id = f"candidate-{uuid.uuid4().hex}"
    drafts: list[dict[str, Any]] = []
    manifest_drafts: list[dict[str, Any]] = []
    for draft_id in clean_ids:
        draft = admin_drafts.get_draft(draft_id, course_id=course_id)
        if str(draft.get("course_id") or "") != course_id:
            raise PublicationConflict("Working copy belongs to a different course")
        if draft["status"] != "draft":
            raise PublicationConflict("Archived working copies cannot enter a publication candidate")
        if not draft.get("changed_from_base") and not str(draft["entity_id"]).startswith("new:"):
            raise PublicationError(f"{draft['entity_id']} has no change to publish")
        manifest_record = _candidate_manifest_draft(draft)
        if manifest_record["quality"]["error_count"]:
            raise PublicationError(f"{draft['entity_id']} has publication-blocking quality errors")
        drafts.append(draft)
        manifest_drafts.append(manifest_record)

    warning_count = sum(item["quality"]["warning_count"] for item in manifest_drafts)
    if warning_count and not warnings_acknowledged:
        raise PublicationError("Teacher-review warnings must be acknowledged before a candidate is created")

    docs: dict[str, Any] = {}
    before: dict[str, bytes] = {}
    touched_by: dict[str, list[str]] = {}
    try:
        for draft in drafts:
            touched = _apply_draft(draft, docs, before, candidate_id)
            for source_path in touched:
                touched_by.setdefault(source_path, []).append(draft["entity_id"])
        files = _write_candidate_files(candidate_id, docs, before, config)
        for draft in drafts:
            admin_drafts.create_snapshot(
                draft["draft_id"],
                label=f"Pre-publication snapshot · {candidate_id[-12:]}",
                username=username,
                course_id=course_id,
            )
        manifest = {
            "schema": PUBLICATION_SCHEMA,
            "course_id": course_id,
            "course_title": access.get("title") or access.get("course_title") or course_id,
            "candidate_id": candidate_id,
            "kind": "content_release",
            "title": clean_title,
            "notes": (notes or "").strip()[:12000],
            "created_at": _now(),
            "created_by": username,
            "warnings_acknowledged": bool(warnings_acknowledged),
            "error_count": 0,
            "warning_count": warning_count,
            "advisory_count": sum(item["quality"]["advisory_count"] for item in manifest_drafts),
            "drafts": manifest_drafts,
            "files": files,
            "file_owners": touched_by,
            "base_branch": config.github_base_branch,
            "publication_model": "candidate package only; no local published source write",
        }
        root = _candidate_dir(candidate_id, config)
        (root / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (root / "release-summary.md").write_text(_release_summary_markdown(manifest), encoding="utf-8")
        now = _now()
        with _connect(config) as connection:
            connection.execute(
                """
                INSERT INTO publication_candidates(
                    candidate_id, course_id, kind, title, notes, status, warnings_acknowledged,
                    manifest_json, validation_json, created_at, updated_at, created_by
                ) VALUES (?, ?, 'content_release', ?, ?, 'created', ?, ?, NULL, ?, ?, ?)
                """,
                (
                    candidate_id,
                    course_id,
                    clean_title,
                    manifest["notes"],
                    1 if warnings_acknowledged else 0,
                    json.dumps(manifest, ensure_ascii=False, sort_keys=True),
                    now,
                    now,
                    username,
                ),
            )
            connection.commit()
        return get_candidate(candidate_id, course_id)
    except Exception:
        if candidate_id:
            shutil.rmtree(_candidate_dir(candidate_id, config), ignore_errors=True)
        raise


def _assert_candidate_fresh(candidate: dict[str, Any]) -> None:
    if candidate.get("kind") == "rollback":
        return
    course_id = str(candidate.get("course_id") or candidate.get("manifest", {}).get("course_id") or "ap-biology")
    for expected in candidate["manifest"].get("drafts", []):
        current = admin_drafts.get_draft(expected["draft_id"], course_id=course_id)
        if current["status"] != "draft":
            raise PublicationConflict(f"{expected['entity_id']} is no longer an active working copy")
        if int(current["version"]) != int(expected["version"]):
            raise PublicationConflict(f"{expected['entity_id']} changed after the candidate was created")
        if current.get("payload_fingerprint") != expected.get("payload_fingerprint"):
            raise PublicationConflict(f"{expected['entity_id']} fingerprint changed after candidate creation")


def get_candidate(candidate_id: str, course_id: str = "ap-biology") -> dict[str, Any]:
    _course_access(course_id)
    config = PublicationConfig.from_env()
    config.require_enabled()
    with _connect(config) as connection:
        row = connection.execute(
            "SELECT * FROM publication_candidates WHERE candidate_id = ? AND course_id = ?",
            (candidate_id, course_id),
        ).fetchone()
    if row is None:
        raise admin_drafts.DraftNotFound("Publication candidate not found for course")
    return _candidate_row(row)


def list_candidates(course_id: str = "ap-biology", limit: int = 100) -> dict[str, Any]:
    _course_access(course_id)
    config = PublicationConfig.from_env()
    config.require_enabled()
    safe_limit = max(1, min(int(limit), 500))
    with _connect(config) as connection:
        rows = connection.execute(
            "SELECT * FROM publication_candidates WHERE course_id = ? ORDER BY created_at DESC LIMIT ?",
            (course_id, safe_limit),
        ).fetchall()
    return {
        "schema": PUBLICATION_SCHEMA,
        "course_id": course_id,
        "items": [_candidate_row(row) for row in rows],
    }


def list_releases(course_id: str = "ap-biology", limit: int = 100) -> dict[str, Any]:
    _course_access(course_id)
    config = PublicationConfig.from_env()
    config.require_enabled()
    safe_limit = max(1, min(int(limit), 500))
    with _connect(config) as connection:
        rows = connection.execute(
            "SELECT * FROM publication_releases WHERE course_id = ? ORDER BY created_at DESC LIMIT ?",
            (course_id, safe_limit),
        ).fetchall()
    return {
        "schema": RELEASE_SCHEMA,
        "course_id": course_id,
        "items": [_release_row(row) for row in rows],
    }


def _update_candidate(
    candidate_id: str,
    *,
    course_id: str = "ap-biology",
    status: str | None = None,
    validation: dict[str, Any] | None = None,
    github: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if status and status not in CANDIDATE_STATUSES:
        raise PublicationError("Invalid candidate status")
    _course_access(course_id)
    config = PublicationConfig.from_env()
    config.require_enabled()
    sets = ["updated_at = ?"]
    values: list[Any] = [_now()]
    if status:
        sets.append("status = ?")
        values.append(status)
    if validation is not None:
        sets.append("validation_json = ?")
        values.append(json.dumps(validation, ensure_ascii=False, sort_keys=True))
    if github:
        mapping = {
            "branch": "github_branch",
            "pr_number": "github_pr_number",
            "commit_sha": "github_commit_sha",
            "merge_sha": "github_merge_sha",
        }
        for key, column in mapping.items():
            if key in github:
                sets.append(f"{column} = ?")
                values.append(github[key])
    values.extend([candidate_id, course_id])
    with _connect(config) as connection:
        cursor = connection.execute(
            f"UPDATE publication_candidates SET {', '.join(sets)} WHERE candidate_id = ? AND course_id = ?",
            values,
        )
        if cursor.rowcount != 1:
            raise admin_drafts.DraftNotFound("Publication candidate not found for course")
        connection.commit()
    return get_candidate(candidate_id, course_id)

def _run_candidate_qa(candidate: dict[str, Any]) -> dict[str, Any]:
    config = PublicationConfig.from_env()
    root = _candidate_dir(candidate["candidate_id"], config)
    with tempfile.TemporaryDirectory(prefix="story-method-release-") as temporary:
        work = Path(temporary) / "repo"
        shutil.copytree(
            ROOT,
            work,
            ignore=shutil.ignore_patterns(".git", "server_data", "__pycache__", ".pytest_cache"),
        )
        for file_record in candidate["manifest"].get("files", []):
            source = root / "after" / file_record["path"]
            destination = work / file_record["path"]
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        commands: list[dict[str, Any]] = []
        passed = True
        for command in LOCAL_QA_COMMANDS:
            try:
                completed = subprocess.run(
                    command,
                    cwd=work,
                    capture_output=True,
                    text=True,
                    timeout=180,
                    env={**os.environ, "MEMORY_PALACE_ADMIN_ENABLED": "false"},
                )
                result = {
                    "command": " ".join(command),
                    "returncode": completed.returncode,
                    "stdout_tail": completed.stdout[-4000:],
                    "stderr_tail": completed.stderr[-4000:],
                }
            except (OSError, subprocess.TimeoutExpired) as exc:
                result = {"command": " ".join(command), "returncode": -1, "error": str(exc)}
            commands.append(result)
            if result["returncode"] != 0:
                passed = False
                break
        return {"passed": passed, "commands": commands, "validated_at": _now()}



def validate_candidate(
    candidate_id: str,
    course_id: str = "ap-biology",
) -> dict[str, Any]:
    _course_access(course_id, editable=True)
    candidate = get_candidate(candidate_id, course_id)
    if candidate["status"] not in {"created", "validated", "failed"}:
        raise PublicationConflict("Only an unsubmitted candidate can be locally revalidated")
    _assert_candidate_fresh(candidate)
    validation = _run_candidate_qa(candidate)
    return _update_candidate(
        candidate_id,
        course_id=course_id,
        status="validated" if validation["passed"] else "failed",
        validation=validation,
    )

def _gh(config: PublicationConfig, method: str, path: str, **kwargs: Any) -> Any:
    config.require_github()
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {config.github_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    response = httpx.request(method, f"{config.github_api_url}{path}", headers=headers, timeout=30.0, **kwargs)
    if response.status_code >= 400:
        detail = response.text[:500]
        raise PublicationError(f"GitHub request failed with {response.status_code}: {detail}")
    if not response.content:
        return {}
    return response.json()


def _remote_file_bytes(config: PublicationConfig, path: str, ref: str) -> bytes:
    payload = _gh(config, "GET", f"/repos/{config.github_repository}/contents/{path}", params={"ref": ref})
    if payload.get("encoding") != "base64" or not payload.get("content"):
        raise PublicationError(f"GitHub did not return file content for {path}")
    return base64.b64decode(str(payload["content"]).replace("\n", ""))


def _assert_remote_base(config: PublicationConfig, candidate: dict[str, Any]) -> None:
    for record in candidate["manifest"].get("files", []):
        remote = _remote_file_bytes(config, record["path"], config.github_base_branch)
        if _sha_bytes(remote) != record["before_sha256"]:
            raise PublicationConflict(f"GitHub base file changed after candidate creation: {record['path']}")



def submit_candidate(
    candidate_id: str,
    course_id: str = "ap-biology",
) -> dict[str, Any]:
    config = PublicationConfig.from_env()
    config.require_github()
    _course_access(course_id, editable=True)
    candidate = get_candidate(candidate_id, course_id)
    if candidate["status"] != "validated" or not (candidate.get("validation") or {}).get("passed"):
        raise PublicationConflict("Candidate must pass local release validation before GitHub submission")
    _assert_candidate_fresh(candidate)
    _assert_remote_base(config, candidate)

    ref = _gh(config, "GET", f"/repos/{config.github_repository}/git/ref/heads/{config.github_base_branch}")
    base_sha = ref["object"]["sha"]
    base_commit = _gh(config, "GET", f"/repos/{config.github_repository}/git/commits/{base_sha}")
    base_tree = base_commit["tree"]["sha"]
    root = _candidate_dir(candidate_id, config)
    tree_items: list[dict[str, Any]] = []
    for record in candidate["manifest"]["files"]:
        raw = (root / "after" / record["path"]).read_bytes()
        blob = _gh(
            config,
            "POST",
            f"/repos/{config.github_repository}/git/blobs",
            json={"content": base64.b64encode(raw).decode("ascii"), "encoding": "base64"},
        )
        tree_items.append({"path": record["path"], "mode": "100644", "type": "blob", "sha": blob["sha"]})
    tree = _gh(
        config,
        "POST",
        f"/repos/{config.github_repository}/git/trees",
        json={"base_tree": base_tree, "tree": tree_items},
    )
    commit = _gh(
        config,
        "POST",
        f"/repos/{config.github_repository}/git/commits",
        json={
            "message": f"Content Studio candidate · {candidate['title']}",
            "tree": tree["sha"],
            "parents": [base_sha],
        },
    )
    branch = f"content-studio/{course_id}/{candidate_id}"
    _gh(
        config,
        "POST",
        f"/repos/{config.github_repository}/git/refs",
        json={"ref": f"refs/heads/{branch}", "sha": commit["sha"]},
    )
    pr = _gh(
        config,
        "POST",
        f"/repos/{config.github_repository}/pulls",
        json={
            "title": f"Content Studio · {candidate['title']}",
            "head": branch,
            "base": config.github_base_branch,
            "body": _release_summary_markdown(candidate["manifest"]),
        },
    )
    return _update_candidate(
        candidate_id,
        course_id=course_id,
        status="submitted",
        github={"branch": branch, "pr_number": int(pr["number"]), "commit_sha": commit["sha"]},
    )


def refresh_github_checks(
    candidate_id: str,
    course_id: str = "ap-biology",
) -> dict[str, Any]:
    config = PublicationConfig.from_env()
    config.require_github()
    _course_access(course_id, editable=True)
    candidate = get_candidate(candidate_id, course_id)
    sha = candidate["github"].get("commit_sha")
    if not sha:
        raise PublicationConflict("Candidate has not been submitted to GitHub")
    checks = _gh(config, "GET", f"/repos/{config.github_repository}/commits/{sha}/check-runs")
    runs = checks.get("check_runs", []) if isinstance(checks, dict) else []
    required = [item for item in runs if isinstance(item, dict)]
    complete = bool(required) and all(item.get("status") == "completed" for item in required)
    successful = complete and all(item.get("conclusion") in {"success", "neutral", "skipped"} for item in required)
    summary = {
        "total": len(required),
        "complete": complete,
        "successful": successful,
        "checks": [
            {
                "name": item.get("name"),
                "status": item.get("status"),
                "conclusion": item.get("conclusion"),
                "html_url": item.get("html_url"),
            }
            for item in required
        ],
    }
    result = _update_candidate(
        candidate_id,
        course_id=course_id,
        status="merge_ready" if successful else "submitted",
    )
    result["github_checks"] = summary
    return result


def merge_candidate(
    candidate_id: str,
    course_id: str = "ap-biology",
) -> dict[str, Any]:
    config = PublicationConfig.from_env()
    config.require_github()
    _course_access(course_id, editable=True)
    if not config.github_allow_merge:
        raise PublicationDisabled("Server-side GitHub merge is disabled; review and merge the pull request manually")
    candidate = refresh_github_checks(candidate_id, course_id)
    if candidate["status"] != "merge_ready":
        raise PublicationConflict("GitHub Actions have not completed successfully")
    pr_number = candidate["github"].get("pr_number")
    sha = candidate["github"].get("commit_sha")
    merged = _gh(
        config,
        "PUT",
        f"/repos/{config.github_repository}/pulls/{pr_number}/merge",
        json={"sha": sha, "merge_method": "squash", "commit_title": f"Publish · {candidate['title']}"},
    )
    if not merged.get("merged"):
        raise PublicationConflict(str(merged.get("message") or "GitHub did not merge the candidate"))
    return _update_candidate(
        candidate_id,
        course_id=course_id,
        status="merged_pending_verify",
        github={"merge_sha": merged.get("sha")},
    )


def verify_release(
    candidate_id: str,
    *,
    username: str,
    course_id: str = "ap-biology",
) -> dict[str, Any]:
    config = PublicationConfig.from_env()
    config.require_github()
    _course_access(course_id, editable=True)
    candidate = get_candidate(candidate_id, course_id)
    if candidate["status"] not in {"submitted", "merge_ready", "merged_pending_verify"}:
        raise PublicationConflict("Only a submitted or merged candidate can be verified as released")
    for record in candidate["manifest"]["files"]:
        remote = _remote_file_bytes(config, record["path"], config.github_base_branch)
        if _sha_bytes(remote) != record["after_sha256"]:
            raise PublicationConflict(
                f"GitHub base branch does not yet contain the candidate version of {record['path']}"
            )

    release_id = f"release-{uuid.uuid4().hex}"
    summary = {
        "course_id": course_id,
        "candidate_id": candidate_id,
        "kind": candidate["kind"],
        "title": candidate["title"],
        "files": candidate["manifest"]["files"],
        "drafts": candidate["manifest"].get("drafts", []),
        "github": candidate["github"],
        "released_at": _now(),
    }
    with _connect(config) as connection:
        existing = connection.execute(
            "SELECT * FROM publication_releases WHERE candidate_id = ? AND course_id = ?",
            (candidate_id, course_id),
        ).fetchone()
        if existing is None:
            connection.execute(
                """
                INSERT INTO publication_releases(
                    release_id, candidate_id, course_id, title, summary_json,
                    created_at, created_by, github_merge_sha
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    release_id,
                    candidate_id,
                    course_id,
                    candidate["title"],
                    json.dumps(summary, ensure_ascii=False, sort_keys=True),
                    _now(),
                    username,
                    candidate["github"].get("merge_sha"),
                ),
            )
        else:
            release_id = existing["release_id"]
        connection.commit()

    if candidate["kind"] == "content_release":
        for expected in candidate["manifest"].get("drafts", []):
            try:
                current = admin_drafts.get_draft(expected["draft_id"], course_id=course_id)
                if (
                    current["status"] == "draft"
                    and int(current["version"]) == int(expected["version"])
                    and current.get("payload_fingerprint") == expected.get("payload_fingerprint")
                ):
                    admin_drafts.archive_draft(
                        current["draft_id"],
                        expected_version=current["version"],
                        username=username,
                        course_id=course_id,
                    )
            except admin_drafts.DraftError:
                pass
    admin_catalog.clear_catalog_cache()
    admin_quality.clear_quality_cache()
    _update_candidate(candidate_id, course_id=course_id, status="released")
    return get_release(release_id, course_id)


def get_release(
    release_id: str,
    course_id: str = "ap-biology",
) -> dict[str, Any]:
    _course_access(course_id)
    config = PublicationConfig.from_env()
    config.require_enabled()
    with _connect(config) as connection:
        row = connection.execute(
            "SELECT * FROM publication_releases WHERE release_id = ? AND course_id = ?",
            (release_id, course_id),
        ).fetchone()
    if row is None:
        raise admin_drafts.DraftNotFound("Release not found for course")
    return _release_row(row)


def create_rollback_candidate(
    release_id: str,
    *,
    title: str | None,
    username: str,
    course_id: str = "ap-biology",
) -> dict[str, Any]:
    config = PublicationConfig.from_env()
    config.require_enabled()
    _course_access(course_id, editable=True)
    release = get_release(release_id, course_id)
    original = get_candidate(release["candidate_id"], course_id)
    candidate_id = f"candidate-{uuid.uuid4().hex}"
    source_root = _candidate_dir(original["candidate_id"], config)
    rollback_root = _candidate_dir(candidate_id, config)
    (rollback_root / "before").mkdir(parents=True, exist_ok=False)
    (rollback_root / "after").mkdir(parents=True, exist_ok=False)
    files: list[dict[str, Any]] = []
    try:
        for record in original["manifest"]["files"]:
            current_version = (source_root / "after" / record["path"]).read_bytes()
            restored_version = (source_root / "before" / record["path"]).read_bytes()
            before_dest = rollback_root / "before" / record["path"]
            after_dest = rollback_root / "after" / record["path"]
            before_dest.parent.mkdir(parents=True, exist_ok=True)
            after_dest.parent.mkdir(parents=True, exist_ok=True)
            before_dest.write_bytes(current_version)
            after_dest.write_bytes(restored_version)
            files.append(
                {
                    "path": record["path"],
                    "before_sha256": _sha_bytes(current_version),
                    "after_sha256": _sha_bytes(restored_version),
                    "before_bytes": len(current_version),
                    "after_bytes": len(restored_version),
                }
            )
        manifest = {
            "schema": PUBLICATION_SCHEMA,
            "course_id": course_id,
            "course_title": original["manifest"].get("course_title") or course_id,
            "candidate_id": candidate_id,
            "kind": "rollback",
            "rollback_of_release": release_id,
            "rollback_of_candidate": original["candidate_id"],
            "title": (title or f"Rollback · {release['title']}").strip()[:300],
            "notes": f"Recover the published files to the pre-release state captured by {release_id}.",
            "created_at": _now(),
            "created_by": username,
            "warnings_acknowledged": True,
            "error_count": 0,
            "warning_count": 0,
            "advisory_count": 0,
            "drafts": [],
            "files": files,
            "base_branch": config.github_base_branch,
            "publication_model": "rollback is a new validated candidate; history is never rewritten",
        }
        (rollback_root / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (rollback_root / "release-summary.md").write_text(_release_summary_markdown(manifest), encoding="utf-8")
        now = _now()
        with _connect(config) as connection:
            connection.execute(
                """
                INSERT INTO publication_candidates(
                    candidate_id, course_id, kind, title, notes, status, warnings_acknowledged,
                    manifest_json, validation_json, created_at, updated_at, created_by
                ) VALUES (?, ?, 'rollback', ?, ?, 'created', 1, ?, NULL, ?, ?, ?)
                """,
                (
                    candidate_id,
                    course_id,
                    manifest["title"],
                    manifest["notes"],
                    json.dumps(manifest, ensure_ascii=False, sort_keys=True),
                    now,
                    now,
                    username,
                ),
            )
            connection.commit()
        return get_candidate(candidate_id, course_id)
    except Exception:
        shutil.rmtree(rollback_root, ignore_errors=True)
        raise

def release_summary(
    candidate_id: str,
    course_id: str = "ap-biology",
) -> str:
    candidate = get_candidate(candidate_id, course_id)
    path = _candidate_dir(candidate_id) / "release-summary.md"
    if not path.exists():
        return _release_summary_markdown(candidate["manifest"])
    return path.read_text(encoding="utf-8")
