from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

from . import admin_catalog, admin_drafts
from .settings import ROOT

EDITOR_SCHEMA = "story-method-content-studio-editors-1.0"


def _field(path: str, label: str, field_type: str = "text", **extra: Any) -> dict[str, Any]:
    return {"path": path, "label": label, "type": field_type, **extra}


SCHEMAS: dict[str, dict[str, Any]] = {
    "unit": {
        "label": "Unit",
        "groups": [
            {
                "id": "identity",
                "title": "Unit identity",
                "description": "Edit the teacher-facing identity and course framing while stable IDs remain locked.",
                "fields": [
                    _field("title", "Unit title", "text", required=True, max_length=300),
                    _field("status", "Status", "text", max_length=120),
                    _field("subtitle", "Subtitle", "text", max_length=500),
                    _field("description", "Description", "textarea", rows=5, max_length=12000),
                ],
            },
            {
                "id": "teaching",
                "title": "Teaching frame",
                "fields": [
                    _field("introduction", "Unit introduction", "textarea", rows=7, max_length=20000),
                    _field("instructions", "Student instructions", "textarea", rows=6, max_length=20000),
                    _field("prerequisites", "Prerequisites", "list"),
                    _field("ap_mapping", "AP Biology mapping", "list"),
                    _field("conclusion", "Unit conclusion", "textarea", rows=6, max_length=20000),
                ],
            },
        ],
    },
    "journey": {
        "label": "Journey",
        "groups": [
            {
                "id": "identity",
                "title": "Journey identity",
                "fields": [
                    _field("story_title", "Story title", "text", required=True, max_length=500),
                    _field("palace_name", "Palace or route name", "text", max_length=500),
                    _field("tagline", "Tagline", "textarea", rows=3, max_length=3000),
                    _field("estimated_minutes", "Estimated minutes", "number", minimum=0, maximum=600),
                ],
            },
            {
                "id": "narrative",
                "title": "Journey narrative frame",
                "fields": [
                    _field("premise", "Premise", "textarea", rows=6, max_length=20000),
                    _field("mission", "Mission", "textarea", rows=6, max_length=20000),
                    _field("finale", "Finale", "textarea", rows=6, max_length=20000),
                    _field("learner_rule", "Learner rule", "textarea", rows=5, max_length=12000),
                    _field("route_orientation", "Route orientation", "textarea", rows=7, max_length=20000),
                ],
            },
            {
                "id": "guide",
                "title": "Guide character",
                "fields": [
                    _field("guide.name", "Name", "text", max_length=300),
                    _field("guide.role", "Role", "textarea", rows=3, max_length=5000),
                    _field("guide.visual", "Visual description", "textarea", rows=4, max_length=8000),
                    _field("guide.story_job", "Story job", "textarea", rows=4, max_length=8000),
                ],
            },
        ],
    },
    "scene": {
        "label": "Scene",
        "groups": [
            {
                "id": "identity",
                "title": "Scene identity and place",
                "fields": [
                    _field("title", "Scene title", "text", required=True, max_length=500),
                    _field("scene_kicker", "Scene kicker", "textarea", rows=3, max_length=6000),
                    _field("locus", "Locus name", "text", max_length=500),
                    _field("location_description", "Location description", "textarea", rows=4, max_length=10000),
                    _field("scene_layout.orientation", "Spatial orientation", "textarea", rows=5, max_length=12000),
                    _field(
                        "scene_layout.zones",
                        "Scene zones",
                        "object_list",
                        item_fields=[
                            _field("position", "Position", "text", max_length=120),
                            _field("label", "Label", "text", max_length=500),
                            _field("symbol", "Symbol", "text", max_length=120),
                            _field("description", "Description", "textarea", rows=3, max_length=6000),
                        ],
                    ),
                ],
            },
            {
                "id": "story",
                "title": "Narrative story",
                "description": "Each paragraph remains independently movable so a long scene can be revised without losing its structure.",
                "fields": [
                    _field("story_paragraphs", "Story paragraphs", "paragraphs"),
                    _field("continuity_object", "Continuity object", "textarea", rows=3, max_length=6000),
                    _field("next_locus", "Next locus", "text", max_length=500),
                ],
            },
            {
                "id": "cast",
                "title": "Characters and scene objects",
                "fields": [
                    _field(
                        "cast",
                        "Scene cast",
                        "object_list",
                        item_fields=[
                            _field("name", "Name", "text", max_length=300),
                            _field("kind", "Kind", "text", max_length=200),
                            _field("visual", "Visual", "textarea", rows=3, max_length=8000),
                            _field("job", "What it does", "textarea", rows=3, max_length=8000),
                        ],
                    ),
                ],
            },
            {
                "id": "retrieval",
                "title": "Quick Recall and progression",
                "fields": [
                    _field("checkpoint", "Quick Recall enabled", "checkbox"),
                    _field("checkpoint_prompt", "Quick Recall prompt", "textarea", rows=4, max_length=8000),
                    _field("checkpoint_object_id", "Quick Recall knowledge target", "text", max_length=300),
                    _field("object_ids", "Memory Object or concept IDs taught here", "list"),
                ],
            },
        ],
    },
    "character": {
        "label": "Character or scene object",
        "groups": [
            {
                "id": "character",
                "title": "Character or object",
                "fields": [
                    _field("name", "Name", "text", required=True, max_length=300),
                    _field("kind", "Kind", "text", max_length=250),
                    _field("role", "Biological or narrative role", "textarea", rows=4, max_length=8000),
                    _field("visual", "Visual description", "textarea", rows=5, max_length=12000),
                    _field("job", "What it does", "textarea", rows=5, max_length=12000),
                ],
            },
        ],
    },
    "location": {
        "label": "Location",
        "groups": [
            {
                "id": "location",
                "title": "Spatial locus",
                "fields": [
                    _field("title", "Location title", "text", required=True, max_length=500),
                    _field("locus", "Locus name", "text", max_length=500),
                    _field("description", "Location description", "textarea", rows=6, max_length=12000),
                    _field("orientation", "Orientation", "textarea", rows=6, max_length=12000),
                    _field(
                        "zones",
                        "Zones",
                        "object_list",
                        item_fields=[
                            _field("position", "Position", "text", max_length=120),
                            _field("label", "Label", "text", max_length=500),
                            _field("symbol", "Symbol", "text", max_length=120),
                            _field("description", "Description", "textarea", rows=3, max_length=6000),
                        ],
                    ),
                ],
            },
        ],
    },
    "concept": {
        "label": "Canonical concept",
        "groups": [
            {
                "id": "science",
                "title": "Scientific record",
                "fields": [
                    _field("canonical_term", "Canonical term", "text", required=True, max_length=500),
                    _field("canonical_definition", "Canonical definition", "textarea", rows=7, max_length=20000),
                    _field("topic", "Topic", "text", max_length=500),
                    _field("scope_class", "Scope class", "text", max_length=300),
                    _field("source_reference", "Source reference", "textarea", rows=3, max_length=6000),
                    _field("scientific_lock_status", "Scientific lock status", "text", max_length=200),
                ],
            },
            {
                "id": "relationships",
                "title": "Relationships and teaching notes",
                "fields": [
                    _field("prerequisites", "Prerequisites", "list"),
                    _field("related_concepts", "Related concepts", "list"),
                    _field("misconceptions", "Misconceptions to guard against", "list"),
                    _field("teacher_notes", "Teacher notes", "textarea", rows=5, max_length=12000),
                ],
            },
        ],
    },
    "memory_object": {
        "label": "Memory Object",
        "groups": [
            {
                "id": "meaning",
                "title": "Scientific meaning",
                "fields": [
                    _field("canonical_term", "Canonical term", "text", required=True, max_length=500),
                    _field("canonical_definition", "Exact definition", "textarea", rows=6, max_length=20000),
                    _field("pronunciation", "Pronunciation", "text", max_length=1000),
                    _field("word_structure", "Word structure", "textarea", rows=3, max_length=6000),
                    _field("confusable_terms", "Confusable terms", "list"),
                ],
            },
            {
                "id": "mnemonic",
                "title": "Mnemonic construction",
                "fields": [
                    _field("phonological_keyword", "Phonological keyword", "text", max_length=1000),
                    _field("mnemonic_actor", "Mnemonic actor", "text", max_length=2000),
                    _field("mnemonic_object", "Mnemonic object", "text", max_length=2000),
                    _field("function_interaction", "Function or interaction", "textarea", rows=5, max_length=12000),
                    _field("palace_zone", "Palace zone", "text", max_length=1000),
                    _field("primary_palace_locus", "Primary palace locus", "text", max_length=2000),
                ],
            },
            {
                "id": "retrieval",
                "title": "Required retrieval",
                "fields": [
                    _field("productive_retrieval_target", "Productive retrieval target", "textarea", rows=4, max_length=10000),
                    _field("exact_name_required", "Exact name required", "checkbox"),
                    _field("exact_spelling_required", "Exact spelling required", "checkbox"),
                    _field("spelling_retrieval_target", "Spelling retrieval target", "text", max_length=2000),
                    _field("application_question", "Application question", "textarea", rows=5, max_length=12000),
                ],
            },
            {
                "id": "trace",
                "title": "Placement and source trace",
                "fields": [
                    _field("locus_id", "Locus ID", "text", max_length=300),
                    _field("scene_index", "Scene index", "number", minimum=0, maximum=500),
                    _field("source_trace", "Source trace", "textarea", rows=4, max_length=8000),
                    _field("version_status", "Version status", "text", max_length=300),
                ],
            },
        ],
    },
}


def schema_for(entity_type: str) -> dict[str, Any]:
    schema = SCHEMAS.get(entity_type)
    if schema is None:
        raise admin_drafts.DraftError(f"No field-specific editor exists for entity type '{entity_type}'")
    return {"schema": EDITOR_SCHEMA, "entity_type": entity_type, **deepcopy(schema)}


def editor_types() -> list[str]:
    return sorted(SCHEMAS)


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


def _records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("memory_objects", "canonical_records", "canonical_catalog", "records", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def _first(record: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in record and record[key] not in (None, ""):
            return record[key]
    return None


def _merge_if_present(target: dict[str, Any], source: dict[str, Any], keys: list[str]) -> None:
    for key in keys:
        if key in source:
            target[key] = deepcopy(source[key])


def _enrich_journey(entity: dict[str, Any], source: dict[str, Any]) -> None:
    _merge_if_present(
        entity,
        source,
        [
            "story_title",
            "palace_name",
            "tagline",
            "premise",
            "mission",
            "finale",
            "estimated_minutes",
            "learner_rule",
            "route_orientation",
            "guide",
            "route",
            "student_release",
            "preview_release",
            "narrative_design",
        ],
    )
    if entity.get("story_title"):
        entity["title"] = entity["story_title"]


def _enrich_scene(entity: dict[str, Any], source: dict[str, Any]) -> None:
    scenes = source.get("scenes") if isinstance(source, dict) else None
    if not isinstance(scenes, list):
        return
    target_index = entity.get("scene_index")
    target_locus = entity.get("locus_id")
    match = None
    for scene in scenes:
        if not isinstance(scene, dict):
            continue
        if target_locus and scene.get("locus_id") == target_locus:
            match = scene
            break
        if scene.get("scene_index") == target_index:
            match = scene
    if match is None:
        return
    _merge_if_present(
        entity,
        match,
        [
            "title",
            "scene_kicker",
            "locus",
            "locus_id",
            "location_description",
            "scene_layout",
            "cast",
            "continuity_object",
            "story_open",
            "story_paragraphs",
            "story_beats",
            "story_close",
            "object_ids",
            "checkpoint",
            "checkpoint_object_id",
            "checkpoint_prompt",
            "next_locus",
        ],
    )


def _enrich_concept(entity: dict[str, Any], source: Any) -> None:
    knowledge_id = str(entity.get("knowledge_id") or "")
    for record in _records(source):
        raw_id = _first(record, "knowledge_id", "Knowledge ID", "source_knowledge_id", "record_id", "id")
        if str(raw_id or "") != knowledge_id:
            continue
        entity["prerequisites"] = deepcopy(_first(record, "prerequisites", "prerequisite_ids") or entity.get("prerequisites") or [])
        entity["related_concepts"] = deepcopy(_first(record, "related_concepts", "relationships", "related_ids") or entity.get("related_concepts") or [])
        entity["misconceptions"] = deepcopy(_first(record, "misconceptions", "common_misconceptions", "confusable_terms") or entity.get("misconceptions") or [])
        entity["teacher_notes"] = deepcopy(_first(record, "teacher_notes", "notes") or entity.get("teacher_notes"))
        return


def _enrich_memory(entity: dict[str, Any], source: Any) -> None:
    memory_id = str(entity.get("memory_object_id") or "")
    for record in _records(source):
        raw_id = _first(record, "memory_object_id", "object_id", "knowledge_id")
        if str(raw_id or "") != memory_id:
            continue
        mapping = {
            "pronunciation": ("pronunciation", "phonetic_pronunciation", "pronunciation_guide"),
            "word_structure": ("word_structure", "morphology", "word_parts"),
            "phonological_keyword": ("phonological_keyword", "phonetic_keyword", "keyword"),
            "mnemonic_actor": ("mnemonic_actor", "mnemonic_character", "actor"),
            "mnemonic_object": ("mnemonic_object", "visual_object", "object"),
            "function_interaction": ("function_interaction", "function_or_interaction", "interaction"),
            "spelling_retrieval_target": ("spelling_retrieval_target", "required_spelling_retrieval"),
        }
        for target_key, aliases in mapping.items():
            value = _first(record, *aliases)
            if value not in (None, ""):
                entity[target_key] = deepcopy(value)
        return


def editable_entity(entity_id: str) -> dict[str, Any]:
    base = admin_catalog.get_entity(entity_id)
    if base is None:
        raise admin_drafts.DraftNotFound("Catalog entity not found")
    entity = deepcopy(base)
    entity_type = str(entity.get("type") or "")
    if entity_type not in SCHEMAS:
        raise admin_drafts.DraftError(f"No field-specific editor exists for entity type '{entity_type}'")

    source = _load_source(entity.get("source_path"))
    if entity_type == "journey" and isinstance(source, dict):
        _enrich_journey(entity, source)
    elif entity_type == "scene" and isinstance(source, dict):
        _enrich_scene(entity, source)
    elif entity_type == "concept":
        _enrich_concept(entity, source)
    elif entity_type == "memory_object":
        _enrich_memory(entity, source)
    return entity


def _get_path(payload: dict[str, Any], path: str) -> Any:
    current: Any = payload
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _iter_fields(schema: dict[str, Any]):
    for group in schema.get("groups", []):
        for field in group.get("fields", []):
            yield field


def _validate_string(value: Any, field: dict[str, Any]) -> None:
    if value is None:
        if field.get("required"):
            raise admin_drafts.DraftError(f"{field['label']} is required")
        return
    if not isinstance(value, str):
        raise admin_drafts.DraftError(f"{field['label']} must be text")
    if field.get("required") and not value.strip():
        raise admin_drafts.DraftError(f"{field['label']} is required")
    max_length = int(field.get("max_length") or 0)
    if max_length and len(value) > max_length:
        raise admin_drafts.DraftError(f"{field['label']} exceeds {max_length} characters")


def validate_payload(entity_type: str, payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise admin_drafts.DraftError("Editor payload must be an object")
    if payload.get("type") != entity_type:
        raise admin_drafts.DraftError("Editor payload type does not match the draft entity type")
    schema = schema_for(entity_type)
    checked = 0
    for field in _iter_fields(schema):
        checked += 1
        value = _get_path(payload, field["path"])
        field_type = field["type"]
        if field_type in {"text", "textarea"}:
            _validate_string(value, field)
        elif field_type == "number":
            if value is not None and not isinstance(value, (int, float)):
                raise admin_drafts.DraftError(f"{field['label']} must be numeric")
            if isinstance(value, (int, float)):
                if field.get("minimum") is not None and value < field["minimum"]:
                    raise admin_drafts.DraftError(f"{field['label']} is below the allowed minimum")
                if field.get("maximum") is not None and value > field["maximum"]:
                    raise admin_drafts.DraftError(f"{field['label']} exceeds the allowed maximum")
        elif field_type == "checkbox":
            if value is not None and not isinstance(value, bool):
                raise admin_drafts.DraftError(f"{field['label']} must be true or false")
        elif field_type == "list":
            if value is not None and not isinstance(value, list):
                raise admin_drafts.DraftError(f"{field['label']} must be a list")
        elif field_type == "paragraphs":
            if value is not None:
                if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                    raise admin_drafts.DraftError(f"{field['label']} must contain text paragraphs")
                if len(value) > 250:
                    raise admin_drafts.DraftError(f"{field['label']} has too many paragraphs")
                if any(len(item) > 30000 for item in value):
                    raise admin_drafts.DraftError(f"{field['label']} contains an oversized paragraph")
        elif field_type == "object_list":
            if value is not None:
                if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
                    raise admin_drafts.DraftError(f"{field['label']} must contain structured items")
                if len(value) > 150:
                    raise admin_drafts.DraftError(f"{field['label']} contains too many items")
                for item in value:
                    for item_field in field.get("item_fields", []):
                        _validate_string(item.get(item_field["path"]), item_field)
    return {"valid": True, "entity_type": entity_type, "fields_checked": checked}


def create_editor_draft(entity_id: str, username: str) -> dict[str, Any]:
    enriched = editable_entity(entity_id)
    draft = admin_drafts.create_draft(entity_id, username)
    if draft.get("existing"):
        draft["editor_schema"] = schema_for(draft["entity_type"])
        return draft

    if draft.get("payload") != enriched:
        fingerprint = admin_drafts._fingerprint(enriched)
        title = enriched.get("title") or enriched.get("canonical_term") or draft.get("title") or entity_id
        with admin_drafts._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                "SELECT version, status FROM content_drafts WHERE draft_id = ?",
                (draft["draft_id"],),
            ).fetchone()
            if row is None:
                raise admin_drafts.DraftNotFound("Draft not found")
            if int(row["version"]) != 1 or row["status"] != "draft":
                raise admin_drafts.DraftConflict("Draft changed while the editor baseline was being prepared")
            connection.execute(
                """
                UPDATE content_drafts
                SET base_payload_json = ?, base_fingerprint = ?, payload_json = ?, title = ?
                WHERE draft_id = ?
                """,
                (
                    admin_drafts._dump(enriched),
                    fingerprint,
                    admin_drafts._dump(enriched),
                    str(title),
                    draft["draft_id"],
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
                    "Field editor working copy created from source-enriched normalized content",
                    draft["draft_id"],
                ),
            )
            connection.commit()
        draft = admin_drafts.get_draft(draft["draft_id"])
        draft["existing"] = False

    draft["editor_schema"] = schema_for(draft["entity_type"])
    return draft


def save_editor_draft(
    draft_id: str,
    *,
    payload: dict[str, Any],
    expected_version: int,
    username: str,
    note: str | None,
    autosave: bool,
) -> dict[str, Any]:
    current = admin_drafts.get_draft(draft_id)
    entity_type = str(current["entity_type"])
    validation = validate_payload(entity_type, payload)
    saved = admin_drafts.update_draft(
        draft_id,
        payload=payload,
        expected_version=expected_version,
        username=username,
        note=note,
        autosave=autosave,
    )
    saved["editor_schema"] = schema_for(entity_type)
    saved["editor_validation"] = validation
    return saved
