from __future__ import annotations

from copy import deepcopy
from typing import Any

from . import admin_catalog, admin_drafts, admin_editors

REPLACEMENT_SCHEMA = "story-method-content-studio-replacements-1.1"
SCENE_MODES = ("narrative_only", "narrative_plus_scene_design", "complete_scene")
JOURNEY_MODES = ("complete_journey",)

DEFAULT_PRESERVATION = {
    "title": True,
    "location": True,
    "characters": True,
    "memory_objects": True,
    "quick_recall": True,
    "route": True,
    "external_questions": True,
    "review": True,
    "concept_associations": True,
}

SCENE_LOCKED_FIELDS = {
    "course_id",
    "id",
    "type",
    "unit_id",
    "journey_id",
    "palace_id",
    "scene_index",
    "locus_id",
    "source_path",
}
JOURNEY_LOCKED_FIELDS = {
    "course_id",
    "id",
    "type",
    "unit_id",
    "palace_id",
    "source_path",
}
SCENE_LOCATION_FIELDS = {"locus", "location_description", "scene_layout", "next_locus"}
SCENE_CHARACTER_FIELDS = {"cast", "continuity_object"}
SCENE_MEMORY_FIELDS = {"object_ids"}
SCENE_RECALL_FIELDS = {"checkpoint", "checkpoint_object_id", "checkpoint_prompt"}
SCENE_NARRATIVE_FIELDS = {"story_open", "story_paragraphs", "story_beats", "story_close"}


class ReplacementBlocked(admin_drafts.DraftError):
    pass


def _target_type(entity_id: str, course_id: str = "ap-biology") -> str:
    entity = admin_catalog.get_entity(entity_id, course_id)
    if entity is None:
        raise admin_drafts.DraftNotFound("Catalog entity not found")
    entity_type = str(entity.get("type") or "")
    if entity_type not in {"scene", "journey"}:
        raise admin_drafts.DraftError("Complete Story Replacement supports scene and journey targets")
    return entity_type


def _full_journey(entity_id: str, course_id: str = "ap-biology") -> dict[str, Any]:
    entity = admin_catalog.get_entity(entity_id, course_id)
    if entity is None:
        raise admin_drafts.DraftNotFound("Catalog entity not found")
    source = admin_editors._load_source(
        entity.get("source_path"),
        course_id=course_id,
        unit_id=str(entity.get("unit_id") or ""),
    )
    if not isinstance(source, dict):
        raise admin_drafts.DraftError("The journey source could not be loaded")
    payload = deepcopy(source)
    payload["id"] = entity["id"]
    payload["type"] = "journey"
    payload["unit_id"] = entity.get("unit_id") or payload.get("unit_id")
    payload["palace_id"] = entity.get("palace_id") or payload.get("palace_id")
    payload["source_path"] = entity.get("source_path")
    payload["dependency_counts"] = deepcopy(entity.get("dependency_counts", {}))
    if payload.get("story_title"):
        payload["title"] = payload["story_title"]
    return payload


def replacement_base(entity_id: str, course_id: str = "ap-biology") -> dict[str, Any]:
    entity_type = _target_type(entity_id, course_id)
    if entity_type == "scene":
        return admin_editors.editable_entity(entity_id, course_id)
    return _full_journey(entity_id, course_id)


def _route_signature(payload: dict[str, Any]) -> list[tuple[Any, Any]]:
    if payload.get("type") == "scene":
        return [(payload.get("scene_index"), payload.get("locus_id"))]
    signature: list[tuple[Any, Any]] = []
    for scene in payload.get("scenes", []):
        if isinstance(scene, dict):
            signature.append((scene.get("scene_index"), scene.get("locus_id")))
    return signature


def _story_text(payload: dict[str, Any]) -> str:
    parts: list[str] = []
    if payload.get("type") == "journey":
        for field in ("tagline", "premise", "mission", "finale"):
            value = payload.get(field)
            if isinstance(value, str):
                parts.append(value)
        for scene in payload.get("scenes", []):
            if isinstance(scene, dict):
                parts.append(_scene_story_text(scene))
    else:
        parts.append(_scene_story_text(payload))
    return "\n".join(part for part in parts if part).strip()


def _scene_story_text(scene: dict[str, Any]) -> str:
    paragraphs = scene.get("story_paragraphs")
    if isinstance(paragraphs, list):
        return "\n".join(str(item) for item in paragraphs if isinstance(item, str)).strip()
    value = scene.get("story_open")
    return value.strip() if isinstance(value, str) else ""


def _scene_refs(scene: dict[str, Any]) -> set[str]:
    refs = {
        str(value)
        for value in scene.get("object_ids", [])
        if value not in (None, "")
    } if isinstance(scene.get("object_ids"), list) else set()
    checkpoint = scene.get("checkpoint_object_id")
    if checkpoint not in (None, ""):
        refs.add(str(checkpoint))
    return refs


def _coverage_refs(payload: dict[str, Any]) -> set[str]:
    if payload.get("type") == "journey":
        refs: set[str] = set()
        for scene in payload.get("scenes", []):
            if isinstance(scene, dict):
                refs.update(_scene_refs(scene))
        return refs
    return _scene_refs(payload)


def _resolve_knowledge(unit_id: str, raw_reference: str, course_id: str = "ap-biology") -> list[dict[str, Any]]:
    resolved = admin_catalog.resolve_reference(unit_id, raw_reference, course_id)
    items: list[dict[str, Any]] = []
    for entity in resolved.get("matches", []):
        if entity.get("type") not in {"concept", "memory_object"}:
            continue
        items.append(entity)
        if entity.get("type") == "memory_object":
            report = admin_catalog.dependency_report(entity["id"], course_id=course_id, depth=1, limit=40) or {}
            for linked in report.get("direct_outbound", []):
                edge = linked.get("edge", {})
                target = linked.get("entity", {})
                if edge.get("kind") == "represents" and target.get("type") == "concept":
                    items.append(target)
    return items


def _scene_catalog_ids_for_journey(journey_id: str, unit_id: str, course_id: str = "ap-biology") -> list[str]:
    items = admin_catalog.list_entities(course_id=course_id, entity_type="scene", unit_id=unit_id, limit=500).get("items", [])
    items = [item for item in items if item.get("journey_id") == journey_id]
    items.sort(key=lambda item: (item.get("scene_index") or 0, item["id"]))
    return [item["id"] for item in items]


def required_knowledge(entity_id: str, course_id: str = "ap-biology") -> list[dict[str, Any]]:
    base = replacement_base(entity_id, course_id)
    unit_id = str(base.get("unit_id") or "")
    raw_refs = set(_coverage_refs(base))
    target_ids = [entity_id]
    if base.get("type") == "journey":
        target_ids.extend(_scene_catalog_ids_for_journey(entity_id, unit_id, course_id))

    direct_entities: list[dict[str, Any]] = []
    for target_id in target_ids:
        report = admin_catalog.dependency_report(target_id, course_id=course_id, depth=1, limit=500) or {}
        for item in report.get("direct_outbound", []):
            edge = item.get("edge", {})
            entity = item.get("entity", {})
            if edge.get("kind") in {"teaches", "teaches_concept"} and entity.get("type") in {"concept", "memory_object"}:
                direct_entities.append(entity)

    records: dict[str, dict[str, Any]] = {}
    for raw in sorted(raw_refs):
        matches = _resolve_knowledge(unit_id, raw, course_id)
        if not matches:
            key = f"raw:{raw}"
            records[key] = {
                "id": key,
                "raw_reference": raw,
                "type": "unresolved",
                "title": raw,
                "canonical_term": raw,
                "canonical_definition": None,
                "source": "scene_reference",
            }
        for entity in matches:
            records[entity["id"]] = {
                "id": entity["id"],
                "raw_reference": raw,
                "type": entity.get("type"),
                "title": entity.get("title"),
                "canonical_term": entity.get("canonical_term") or entity.get("title"),
                "canonical_definition": entity.get("canonical_definition"),
                "knowledge_id": entity.get("knowledge_id"),
                "memory_object_id": entity.get("memory_object_id"),
                "source": "scene_reference",
            }
    for entity in direct_entities:
        records.setdefault(
            entity["id"],
            {
                "id": entity["id"],
                "raw_reference": entity.get("memory_object_id") or entity.get("knowledge_id"),
                "type": entity.get("type"),
                "title": entity.get("title"),
                "canonical_term": entity.get("canonical_term") or entity.get("title"),
                "canonical_definition": entity.get("canonical_definition"),
                "knowledge_id": entity.get("knowledge_id"),
                "memory_object_id": entity.get("memory_object_id"),
                "source": "dependency_graph",
            },
        )
    return sorted(records.values(), key=lambda item: (str(item.get("canonical_term") or "").casefold(), item["id"]))


def dependency_impact(entity_id: str, course_id: str = "ap-biology") -> dict[str, Any]:
    report = admin_catalog.dependency_report(entity_id, course_id=course_id, depth=3, limit=1000)
    if report is None:
        raise admin_drafts.DraftNotFound("Catalog entity not found")
    downstream: list[dict[str, Any]] = []
    for item in report.get("related", []):
        entity = item.get("entity", {})
        if entity.get("type") in {"question", "question_set", "challenge", "scene", "journey", "concept", "memory_object"}:
            downstream.append(
                {
                    "distance": item.get("distance"),
                    "path": item.get("path", []),
                    "entity": {
                        "id": entity.get("id"),
                        "type": entity.get("type"),
                        "title": entity.get("title"),
                        "unit_id": entity.get("unit_id"),
                    },
                }
            )
    return {
        "related_counts_by_type": report.get("related_counts_by_type", {}),
        "direct_outbound": report.get("direct_outbound", []),
        "direct_inbound": report.get("direct_inbound", []),
        "downstream": downstream[:250],
        "truncated": bool(report.get("truncated")),
    }


def target_plan(entity_id: str, course_id: str = "ap-biology") -> dict[str, Any]:
    base = replacement_base(entity_id, course_id)
    entity_type = base["type"]
    modes = list(SCENE_MODES if entity_type == "scene" else JOURNEY_MODES)
    knowledge = required_knowledge(entity_id, course_id)
    impact = dependency_impact(entity_id, course_id)
    return {
        "schema": REPLACEMENT_SCHEMA,
        "entity_id": entity_id,
        "entity_type": entity_type,
        "course_id": course_id,
        "title": base.get("title") or base.get("story_title") or entity_id,
        "unit_id": base.get("unit_id"),
        "modes": modes,
        "default_preservation": deepcopy(DEFAULT_PRESERVATION),
        "required_knowledge": knowledge,
        "required_knowledge_count": len(knowledge),
        "dependency_impact": impact,
        "published_base": base,
        "published_story_text": _story_text(base),
        "route_signature": _route_signature(base),
    }


def _rebase_pristine_draft(
    draft_id: str,
    payload: dict[str, Any],
    *,
    course_id: str,
) -> dict[str, Any]:
    admin_drafts.get_draft(draft_id, course_id=course_id)
    with admin_drafts._connect() as connection:
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute(
            "SELECT * FROM content_drafts WHERE draft_id = ? AND course_id = ?",
            (draft_id, course_id),
        ).fetchone()
        if row is None:
            raise admin_drafts.DraftNotFound("Draft not found for course")
        if row["status"] != "draft" or int(row["version"]) != 1:
            raise admin_drafts.DraftConflict("An existing changed draft must be archived before this replacement workflow can prepare a full source baseline")
        current = admin_drafts._load(row["payload_json"])
        base = admin_drafts._load(row["base_payload_json"])
        if admin_drafts._fingerprint(current) != admin_drafts._fingerprint(base):
            raise admin_drafts.DraftConflict("An existing changed draft must be archived before this replacement workflow can prepare a full source baseline")
        fingerprint = admin_drafts._fingerprint(payload)
        title = payload.get("title") or payload.get("story_title") or row["title"]
        connection.execute(
            "UPDATE content_drafts SET base_payload_json = ?, base_fingerprint = ?, payload_json = ?, title = ? WHERE draft_id = ? AND course_id = ?",
            (
                admin_drafts._dump(payload),
                fingerprint,
                admin_drafts._dump(payload),
                str(title),
                draft_id,
                course_id,
            ),
        )
        connection.execute(
            "UPDATE content_draft_revisions SET payload_json = ?, payload_fingerprint = ?, note = ? WHERE draft_id = ? AND revision_number = 1",
            (
                admin_drafts._dump(payload),
                fingerprint,
                "Complete Story Replacement working copy created from full published source",
                draft_id,
            ),
        )
        connection.commit()
    return admin_drafts.get_draft(draft_id, course_id=course_id)


def create_replacement_draft(entity_id: str, username: str, course_id: str = "ap-biology") -> dict[str, Any]:
    base = replacement_base(entity_id, course_id)
    draft = admin_drafts.create_draft(entity_id, username, course_id)
    if draft.get("existing"):
        current = draft.get("payload", {})
        complete = bool(current.get("story_paragraphs")) if base.get("type") == "scene" else isinstance(current.get("scenes"), list)
        if complete:
            draft["replacement_plan"] = target_plan(entity_id, course_id)
            return draft
        draft = _rebase_pristine_draft(draft["draft_id"], base, course_id=course_id)
        draft["existing"] = True
    elif draft.get("payload") != base:
        draft = _rebase_pristine_draft(draft["draft_id"], base, course_id=course_id)
        draft["existing"] = False
    draft["replacement_plan"] = target_plan(entity_id, course_id)
    return draft


def _policies(value: dict[str, Any] | None) -> dict[str, bool]:
    result = deepcopy(DEFAULT_PRESERVATION)
    if value:
        for key in result:
            if key in value:
                result[key] = bool(value[key])
    result["route"] = True
    result["external_questions"] = True
    result["review"] = True
    return result


def _copy_present(target: dict[str, Any], source: dict[str, Any], fields: set[str]) -> None:
    for field in fields:
        if field in source:
            target[field] = deepcopy(source[field])


def _scene_candidate(current: dict[str, Any], replacement: dict[str, Any], mode: str, preserve: dict[str, bool]) -> dict[str, Any]:
    if mode not in SCENE_MODES:
        raise admin_drafts.DraftError("Invalid scene replacement mode")
    candidate = deepcopy(current)
    _copy_present(candidate, replacement, SCENE_NARRATIVE_FIELDS)

    if not preserve["title"] and "title" in replacement:
        candidate["title"] = deepcopy(replacement["title"])

    if mode in {"narrative_plus_scene_design", "complete_scene"}:
        if not preserve["location"]:
            _copy_present(candidate, replacement, SCENE_LOCATION_FIELDS)
        if not preserve["characters"]:
            _copy_present(candidate, replacement, SCENE_CHARACTER_FIELDS)

    if mode == "complete_scene":
        for key, value in replacement.items():
            if key in SCENE_LOCKED_FIELDS or key in SCENE_NARRATIVE_FIELDS:
                continue
            if preserve["title"] and key == "title":
                continue
            if preserve["location"] and key in SCENE_LOCATION_FIELDS:
                continue
            if preserve["characters"] and key in SCENE_CHARACTER_FIELDS:
                continue
            if preserve["memory_objects"] and key in SCENE_MEMORY_FIELDS:
                continue
            if preserve["quick_recall"] and key in SCENE_RECALL_FIELDS:
                continue
            candidate[key] = deepcopy(value)

    for key in SCENE_LOCKED_FIELDS:
        if key in current:
            candidate[key] = deepcopy(current[key])
    if preserve["memory_objects"]:
        _copy_present(candidate, current, SCENE_MEMORY_FIELDS)
    if preserve["quick_recall"]:
        _copy_present(candidate, current, SCENE_RECALL_FIELDS)
    if preserve["location"]:
        _copy_present(candidate, current, SCENE_LOCATION_FIELDS)
    if preserve["characters"]:
        _copy_present(candidate, current, SCENE_CHARACTER_FIELDS)
    if preserve["title"] and "title" in current:
        candidate["title"] = current["title"]
    return candidate


def _journey_candidate(current: dict[str, Any], replacement: dict[str, Any], preserve: dict[str, bool]) -> dict[str, Any]:
    candidate = deepcopy(current)
    for key, value in replacement.items():
        if key in JOURNEY_LOCKED_FIELDS or key == "scenes":
            continue
        if preserve["title"] and key in {"title", "story_title", "palace_name"}:
            continue
        if preserve["route"] and key in {"route", "route_orientation"}:
            continue
        candidate[key] = deepcopy(value)

    current_scenes = [scene for scene in current.get("scenes", []) if isinstance(scene, dict)]
    replacement_scenes = [scene for scene in replacement.get("scenes", []) if isinstance(scene, dict)]
    if replacement_scenes:
        by_index = {scene.get("scene_index"): scene for scene in replacement_scenes}
        merged: list[dict[str, Any]] = []
        for scene in current_scenes:
            supplied = by_index.get(scene.get("scene_index"), {})
            merged.append(_scene_candidate(scene, supplied, "complete_scene", preserve))
        candidate["scenes"] = merged

    for key in JOURNEY_LOCKED_FIELDS:
        if key in current:
            candidate[key] = deepcopy(current[key])
    if preserve["title"]:
        for key in ("title", "story_title", "palace_name"):
            if key in current:
                candidate[key] = deepcopy(current[key])
    if preserve["route"]:
        for key in ("route", "route_orientation"):
            if key in current:
                candidate[key] = deepcopy(current[key])
    return candidate


def build_candidate(current: dict[str, Any], mode: str, replacement: dict[str, Any], preservation: dict[str, Any] | None = None) -> tuple[dict[str, Any], dict[str, bool]]:
    preserve = _policies(preservation)
    entity_type = current.get("type")
    if entity_type == "scene":
        return _scene_candidate(current, replacement, mode, preserve), preserve
    if entity_type == "journey":
        if mode not in JOURNEY_MODES:
            raise admin_drafts.DraftError("Invalid journey replacement mode")
        return _journey_candidate(current, replacement, preserve), preserve
    raise admin_drafts.DraftError("Replacement draft is not a scene or journey")


def _term_present(term: str | None, narrative: str) -> bool:
    if not term:
        return True
    clean = " ".join(term.casefold().split())
    return bool(clean and clean in " ".join(narrative.casefold().split()))


def analyze_replacement(
    draft_id: str,
    *,
    expected_version: int,
    mode: str,
    replacement: dict[str, Any],
    preservation: dict[str, Any] | None = None,
    course_id: str = "ap-biology",
) -> dict[str, Any]:
    draft = admin_drafts.get_draft(draft_id, course_id=course_id)
    if draft["status"] != "draft":
        raise admin_drafts.DraftError("Archived drafts cannot be replaced")
    if int(draft["version"]) != int(expected_version):
        raise admin_drafts.DraftConflict("Draft changed since this replacement workflow loaded it")
    candidate, preserve = build_candidate(draft["payload"], mode, replacement, preservation)
    if str(draft.get("course_id") or "") != str(course_id):
        raise admin_drafts.DraftNotFound("Draft not found for course")
    base = replacement_base(draft["entity_id"], course_id)
    knowledge = required_knowledge(draft["entity_id"], course_id)
    required_refs = _coverage_refs(base)
    candidate_refs = _coverage_refs(candidate)
    missing_refs = sorted(required_refs - candidate_refs)
    blockers: list[str] = []
    warnings: list[str] = []

    if not _story_text(candidate):
        blockers.append("Replacement narrative is empty")
    if _route_signature(candidate) != _route_signature(base):
        blockers.append("The permanent scene route or stable locus identities changed")
    if missing_refs:
        blockers.append("Required knowledge references are missing from the replacement: " + ", ".join(missing_refs[:30]))

    if candidate.get("type") == "journey":
        base_scenes = [scene for scene in base.get("scenes", []) if isinstance(scene, dict)]
        candidate_scenes = [scene for scene in candidate.get("scenes", []) if isinstance(scene, dict)]
        if len(base_scenes) != len(candidate_scenes):
            blockers.append("Complete journey replacement must preserve the published scene count")
        for scene in candidate_scenes:
            if not _scene_story_text(scene):
                blockers.append(f"Scene {scene.get('scene_index')} has no replacement narrative")

    narrative = _story_text(candidate)
    missing_terms = [
        item.get("canonical_term") or item.get("title")
        for item in knowledge
        if not _term_present(item.get("canonical_term") or item.get("title"), narrative)
    ]
    missing_terms = [str(term) for term in missing_terms if term]
    if missing_terms:
        warnings.append(
            f"{len(missing_terms)} required terms are not explicitly named in the replacement narrative. This is a wording warning, not proof of missing scientific meaning."
        )

    if not preserve["quick_recall"] and any(
        isinstance(scene, dict) and (scene.get("checkpoint") or scene.get("checkpoint_prompt"))
        for scene in (base.get("scenes", []) if base.get("type") == "journey" else [base])
    ):
        warnings.append("Quick Recall preservation was disabled. Confirm that retrieval timing remains intentional.")
    if not preserve["characters"]:
        warnings.append("Character preservation was disabled. Review continuity and biological-role mappings.")
    if not preserve["location"]:
        warnings.append("Location preservation was disabled. Review spatial orientation and palace-locus continuity.")

    impact = dependency_impact(draft["entity_id"], course_id)
    counts = impact.get("related_counts_by_type", {})
    external_count = sum(int(counts.get(key, 0) or 0) for key in ("question", "question_set", "challenge"))
    if external_count:
        warnings.append(f"{external_count} assessment or application records are connected downstream and remain preserved.")

    knowledge_status: list[dict[str, Any]] = []
    for item in knowledge:
        raw = item.get("raw_reference")
        knowledge_status.append(
            {
                **item,
                "reference_present": True if not raw else str(raw) in candidate_refs,
                "term_explicitly_named": _term_present(item.get("canonical_term") or item.get("title"), narrative),
            }
        )

    return {
        "schema": REPLACEMENT_SCHEMA,
        "draft_id": draft_id,
        "course_id": course_id,
        "entity_id": draft["entity_id"],
        "entity_type": draft["entity_type"],
        "mode": mode,
        "preservation": preserve,
        "can_apply": not blockers,
        "blockers": blockers,
        "warnings": warnings,
        "missing_required_references": missing_refs,
        "missing_explicit_terms": missing_terms,
        "required_knowledge": knowledge_status,
        "dependency_impact": impact,
        "published_base": base,
        "current_draft": draft["payload"],
        "candidate": candidate,
        "published_story_text": _story_text(base),
        "current_story_text": _story_text(draft["payload"]),
        "candidate_story_text": narrative,
        "route_preserved": _route_signature(candidate) == _route_signature(base),
    }


def apply_replacement(
    draft_id: str,
    *,
    expected_version: int,
    mode: str,
    replacement: dict[str, Any],
    preservation: dict[str, Any] | None,
    username: str,
    course_id: str = "ap-biology",
) -> dict[str, Any]:
    analysis = analyze_replacement(
        draft_id,
        expected_version=expected_version,
        mode=mode,
        replacement=replacement,
        preservation=preservation,
        course_id=course_id,
    )
    if analysis["blockers"]:
        raise ReplacementBlocked("Replacement blocked: " + " | ".join(analysis["blockers"]))

    snapshot = admin_drafts.create_snapshot(
        draft_id,
        label=f"Before {mode.replace('_', ' ')} replacement · v{expected_version}",
        username=username,
        course_id=course_id,
    )
    saved = admin_drafts.update_draft(
        draft_id,
        payload=analysis["candidate"],
        expected_version=expected_version,
        username=username,
        note=f"Complete Story Replacement applied · {mode}",
        autosave=False,
        course_id=course_id,
    )
    return {
        "schema": REPLACEMENT_SCHEMA,
        "applied": True,
        "snapshot": snapshot,
        "draft": saved,
        "analysis": analysis,
    }
