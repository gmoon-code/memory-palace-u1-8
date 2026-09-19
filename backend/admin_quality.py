from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from functools import lru_cache
import re
from typing import Any, Iterable

from . import admin_catalog, admin_drafts, admin_editors, admin_management, course_packages

QUALITY_SCHEMA = "story-method-content-studio-quality-1.0"
PREVIEW_SCHEMA = "story-method-content-studio-preview-1.0"
DEVICE_PRESETS = {
    "phone": {"label": "Phone", "width": 390, "height": 844},
    "tablet": {"label": "Tablet", "width": 768, "height": 1024},
    "laptop": {"label": "Laptop", "width": 1024, "height": 768},
    "desktop": {"label": "Desktop", "width": 1280, "height": 900},
}
EDITOR_TYPES = set(admin_editors.editor_types())
MANAGED_TYPES = set(admin_management.MANAGED_TYPES)
VALID_SOURCES = {"auto", "published", "draft"}


class QualityError(admin_drafts.DraftError):
    pass


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _text(value: Any) -> str:
    return str(value or "").strip()


def _clean_story_text(value: str) -> str:
    return re.sub(r"[*_`#>]", " ", value or "")


def _story_paragraphs(payload: dict[str, Any]) -> list[str]:
    paragraphs = payload.get("story_paragraphs")
    if isinstance(paragraphs, list):
        return [str(item).strip() for item in paragraphs if str(item or "").strip()]
    fallback: list[str] = []
    if _text(payload.get("story_open")):
        fallback.append(_text(payload.get("story_open")))
    for beat in _as_list(payload.get("story_beats")):
        if isinstance(beat, dict) and _text(beat.get("story")):
            fallback.append(_text(beat.get("story")))
    if _text(payload.get("story_close")):
        fallback.append(_text(payload.get("story_close")))
    return fallback


def _text_metrics(paragraphs: Iterable[str]) -> dict[str, Any]:
    clean_paragraphs = [_clean_story_text(str(item)) for item in paragraphs if str(item or "").strip()]
    words_per_paragraph = [len(re.findall(r"\b\w+[\w′'/-]*\b", item, flags=re.UNICODE)) for item in clean_paragraphs]
    joined = " ".join(clean_paragraphs)
    words = re.findall(r"\b\w+[\w′'/-]*\b", joined, flags=re.UNICODE)
    sentences = [item for item in re.split(r"(?<=[.!?])\s+", joined) if item.strip()]
    sentence_word_counts = [len(re.findall(r"\b\w+[\w′'/-]*\b", item, flags=re.UNICODE)) for item in sentences]
    return {
        "paragraph_count": len(clean_paragraphs),
        "word_count": len(words),
        "sentence_count": len(sentences),
        "average_sentence_words": round(sum(sentence_word_counts) / len(sentence_word_counts), 1) if sentence_word_counts else 0.0,
        "max_paragraph_words": max(words_per_paragraph, default=0),
        "paragraphs_over_220_words": sum(1 for value in words_per_paragraph if value > 220),
    }


def _finding(
    severity: str,
    code: str,
    message: str,
    *,
    category: str,
    entity_id: str | None = None,
    unit_id: str | None = None,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "severity": severity,
        "publication_blocking": severity == "error",
        "code": code,
        "category": category,
        "message": message,
        "entity_id": entity_id,
        "unit_id": unit_id,
        "details": details or {},
    }


def _require_course_catalog(course_id: str) -> dict[str, Any]:
    try:
        access = admin_catalog.course_access(course_id)
    except ValueError as exc:
        raise QualityError(str(exc)) from exc
    if not access.get("catalog_ready"):
        raise QualityError(f"Content Studio catalog is not available for course '{course_id}'")
    return access


def _require_course_unit(course_id: str, unit_id: str) -> dict[str, Any]:
    _require_course_catalog(course_id)
    try:
        unit = course_packages.unit(course_id, unit_id)
    except course_packages.CoursePackageError as exc:
        raise QualityError(str(exc)) from exc
    if unit is None:
        raise QualityError(f"Unit '{unit_id}' is not declared for course '{course_id}'")
    return unit


def _course_title(course_id: str) -> str:
    access = _require_course_catalog(course_id)
    return str(access.get("title") or access.get("course_title") or course_id)


def _catalog_entity(entity_id: str, course_id: str = "ap-biology") -> dict[str, Any] | None:
    _require_course_catalog(course_id)
    return admin_catalog.get_entity(entity_id, course_id)


def _published_payload(entity_id: str, course_id: str = "ap-biology") -> dict[str, Any]:
    entity = _catalog_entity(entity_id, course_id)
    if entity is None:
        raise admin_drafts.DraftNotFound("Published catalog entity not found")
    entity_type = str(entity.get("type") or "")
    if entity_type in MANAGED_TYPES:
        return admin_management.managed_entity(entity_id, course_id)
    if entity_type in EDITOR_TYPES:
        return admin_editors.editable_entity(entity_id, course_id)
    return deepcopy(entity)


def _resolve_payload(
    entity_id: str,
    *,
    draft_id: str | None = None,
    source: str = "auto",
    course_id: str = "ap-biology",
) -> dict[str, Any]:
    _require_course_catalog(course_id)
    if source not in VALID_SOURCES:
        raise QualityError("Preview source must be auto, published, or draft")
    entity = _catalog_entity(entity_id, course_id)
    draft: dict[str, Any] | None = None

    if source != "published":
        if draft_id:
            draft = admin_drafts.get_draft(draft_id, course_id=course_id)
            if draft.get("entity_id") != entity_id:
                raise QualityError("Draft does not belong to the requested entity")
        else:
            draft = admin_management._active_draft_for_entity(entity_id, course_id)

    if source == "draft" and draft is None:
        raise admin_drafts.DraftNotFound("No active working copy exists for this entity")

    if draft is not None:
        payload = deepcopy(draft.get("payload") or {})
        return {
            "course_id": course_id,
            "entity_id": entity_id,
            "entity_type": str(draft.get("entity_type") or payload.get("type") or ""),
            "unit_id": draft.get("unit_id") or payload.get("unit_id"),
            "title": payload.get("title") or payload.get("canonical_term") or draft.get("title") or entity_id,
            "source_state": "archived_draft" if draft.get("status") == "archived" else ("new_proposal" if entity_id.startswith("new:") else "draft"),
            "draft_id": draft.get("draft_id"),
            "draft_version": draft.get("version"),
            "payload": payload,
            "published_available": entity is not None,
        }

    if entity is None:
        raise admin_drafts.DraftNotFound("Entity is available only as a working-copy proposal")
    payload = _published_payload(entity_id, course_id)
    return {
        "course_id": course_id,
        "entity_id": entity_id,
        "entity_type": str(entity.get("type") or payload.get("type") or ""),
        "unit_id": entity.get("unit_id") or payload.get("unit_id"),
        "title": payload.get("title") or payload.get("canonical_term") or entity.get("title") or entity_id,
        "source_state": "published",
        "draft_id": None,
        "draft_version": None,
        "payload": payload,
        "published_available": True,
    }


def _merge_source(base: dict[str, Any], overlay: dict[str, Any], *, skip: set[str] | None = None) -> dict[str, Any]:
    result = deepcopy(base)
    blocked = {"id", "type", "course_id", "unit_id", "source_path", "dependency_counts", "coverage"} | (skip or set())
    for key, value in overlay.items():
        if key in blocked:
            continue
        result[key] = deepcopy(value)
    return result


def _scene_journey(
    entity_id: str,
    payload: dict[str, Any],
    course_id: str = "ap-biology",
) -> tuple[dict[str, Any], int]:
    entity = _catalog_entity(entity_id, course_id)
    if entity is None:
        raise QualityError("Scene preview requires a current catalog scene")
    unit_id = str(entity.get("unit_id") or payload.get("unit_id") or "")
    palace_id = str(entity.get("palace_id") or payload.get("palace_id") or "")
    if not unit_id or not palace_id:
        raise QualityError("Scene preview is missing its unit or journey reference")
    journey = course_packages.journey(course_id, unit_id, palace_id)
    if not isinstance(journey, dict):
        raise admin_drafts.DraftNotFound("Student journey source was not found")
    rendered = deepcopy(journey)
    scenes = [deepcopy(item) for item in _as_list(rendered.get("scenes")) if isinstance(item, dict)]
    target_index = int(entity.get("scene_index") if entity.get("scene_index") is not None else payload.get("scene_index") or 0)
    if target_index < 0 or target_index >= len(scenes):
        raise QualityError("Scene index falls outside the student journey")
    scenes[target_index] = _merge_source(scenes[target_index], payload)
    rendered["scenes"] = scenes

    route = [deepcopy(item) for item in _as_list(rendered.get("route")) if isinstance(item, dict)]
    if route and target_index < len(route):
        current = route[target_index]
        current["locus"] = scenes[target_index].get("locus") or current.get("locus")
        current["short"] = scenes[target_index].get("locus") or current.get("short") or current.get("locus")
        route[target_index] = current
        rendered["route"] = route
    return rendered, target_index


def _journey_preview(
    entity_id: str,
    payload: dict[str, Any],
    requested_index: int = 0,
    course_id: str = "ap-biology",
) -> tuple[dict[str, Any], int]:
    entity = _catalog_entity(entity_id, course_id)
    if entity is None:
        raise QualityError("Journey preview requires a current catalog journey")
    unit_id = str(entity.get("unit_id") or payload.get("unit_id") or "")
    palace_id = str(entity.get("palace_id") or payload.get("palace_id") or "")
    source = course_packages.journey(course_id, unit_id, palace_id)
    if not isinstance(source, dict):
        raise admin_drafts.DraftNotFound("Student journey source was not found")
    rendered = _merge_source(source, payload)
    scenes = [item for item in _as_list(rendered.get("scenes")) if isinstance(item, dict)]
    if not scenes:
        raise QualityError("Journey preview has no scenes")
    index = max(0, min(int(requested_index), len(scenes) - 1))
    return rendered, index


def _question_preview(resolved: dict[str, Any], course_id: str = "ap-biology") -> dict[str, Any]:
    payload = resolved["payload"]
    question_type = str(payload.get("question_type") or "review")
    scene_id = payload.get("scene_id")
    if question_type == "quick_recall" and scene_id and _catalog_entity(str(scene_id), course_id):
        scene_payload = _published_payload(str(scene_id), course_id)
        scene_payload["checkpoint"] = True
        scene_payload["checkpoint_prompt"] = payload.get("prompt") or scene_payload.get("checkpoint_prompt")
        knowledge_ids = [str(item) for item in _as_list(payload.get("knowledge_ids")) if item not in (None, "")]
        if knowledge_ids:
            scene_payload["checkpoint_object_id"] = knowledge_ids[0]
        journey, index = _scene_journey(str(scene_id), scene_payload, course_id)
        return {
            "renderer": "learn_recall",
            "journey": journey,
            "scene_index": index,
            "scene_count": len(journey.get("scenes", [])),
        }

    choices = [str(item) for item in _as_list(payload.get("choices")) if str(item or "").strip()]
    if choices:
        question = deepcopy(payload)
        question["choices"] = choices
        set_id = "content-studio-preview"
        return {
            "renderer": "review_mixed",
            "review_items": [{"type": "mixed", "setId": set_id, "questionIndex": 0}],
            "mixed_sets": [{"set_id": set_id, "title": payload.get("title") or "Preview question", "questions": [question]}],
        }
    knowledge_ids = [str(item) for item in _as_list(payload.get("knowledge_ids")) if item not in (None, "")]
    return {
        "renderer": "review_exact",
        "review_items": [
            {
                "type": "exact",
                "objectId": knowledge_ids[0] if knowledge_ids else "preview-item",
                "prompt": payload.get("prompt") or "Preview question",
                "hint": payload.get("hint") or "Return to the relevant story memory.",
                "answer": payload.get("answer") or payload.get("target_answer") or "",
            }
        ],
        "mixed_sets": [],
    }


def _challenge_preview(payload: dict[str, Any], course_id: str = "ap-biology") -> dict[str, Any]:
    item = deepcopy(payload)
    item["answer_guide"] = item.get("answer_guide") or item.get("answer") or ""
    item["domain"] = item.get("domain") or _course_title(course_id)
    item["story_hint"] = item.get("story_hint") or "Return to the relevant story scene and reconstruct the mechanism."
    return {
        "renderer": "practice",
        "application_lab": {"title": "Challenge Lab", "items": [item]},
    }


def build_preview(
    entity_id: str,
    *,
    draft_id: str | None = None,
    source: str = "auto",
    scene_index: int = 0,
    course_id: str = "ap-biology",
) -> dict[str, Any]:
    resolved = _resolve_payload(
        entity_id,
        draft_id=draft_id,
        source=source,
        course_id=course_id,
    )
    entity_type = resolved["entity_type"]
    payload = resolved["payload"]
    model: dict[str, Any]

    if entity_type == "scene":
        journey, index = _scene_journey(entity_id, payload, course_id)
        model = {"renderer": "learn", "journey": journey, "scene_index": index, "scene_count": len(journey.get("scenes", []))}
    elif entity_type == "journey":
        journey, index = _journey_preview(entity_id, payload, scene_index, course_id)
        model = {"renderer": "learn", "journey": journey, "scene_index": index, "scene_count": len(journey.get("scenes", []))}
    elif entity_type == "question":
        model = _question_preview(resolved, course_id)
    elif entity_type == "challenge":
        model = _challenge_preview(payload, course_id)
    elif entity_type in {"concept", "memory_object"}:
        model = {"renderer": "knowledge", "record": deepcopy(payload)}
    elif entity_type == "unit":
        model = {"renderer": "unit", "record": deepcopy(payload)}
    else:
        model = {"renderer": "record", "record": deepcopy(payload)}

    quality = entity_quality(
        entity_id,
        draft_id=resolved.get("draft_id"),
        source="draft" if resolved.get("draft_id") else "published",
        course_id=course_id,
    )
    return {
        "schema": PREVIEW_SCHEMA,
        "course_id": course_id,
        "course_title": _course_title(course_id),
        "entity_id": entity_id,
        "entity_type": entity_type,
        "unit_id": resolved.get("unit_id"),
        "title": resolved.get("title"),
        "source_state": resolved.get("source_state"),
        "draft_id": resolved.get("draft_id"),
        "draft_version": resolved.get("draft_version"),
        "published_available": resolved.get("published_available"),
        "device_presets": DEVICE_PRESETS,
        "model": model,
        "quality": quality,
    }


def _payload_quality(
    entity_type: str,
    payload: dict[str, Any],
    *,
    entity_id: str,
    unit_id: str | None,
    base_payload: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []

    try:
        if entity_type in EDITOR_TYPES:
            admin_editors.validate_payload(entity_type, payload)
        elif entity_type in MANAGED_TYPES:
            validation = admin_management.validate_managed_payload(entity_type, payload)
            for warning in validation.get("warnings", []):
                findings.append(_finding("warning", "managed-content-warning", str(warning), category="validation", entity_id=entity_id, unit_id=unit_id))
    except admin_drafts.DraftError as exc:
        findings.append(_finding("error", "invalid-editor-payload", str(exc), category="validation", entity_id=entity_id, unit_id=unit_id))

    if entity_type == "scene":
        paragraphs = _story_paragraphs(payload)
        metrics = _text_metrics(paragraphs)
        if not paragraphs:
            findings.append(_finding("error", "scene-story-empty", "Scene has no narrative story text.", category="narrative", entity_id=entity_id, unit_id=unit_id))
        if not _text(payload.get("location_description")):
            findings.append(_finding("warning", "scene-location-description-missing", "Scene has no location description for spatial orientation.", category="spatial", entity_id=entity_id, unit_id=unit_id))
        layout = payload.get("scene_layout") if isinstance(payload.get("scene_layout"), dict) else {}
        if not _text(layout.get("orientation") or payload.get("orientation")):
            findings.append(_finding("warning", "scene-orientation-missing", "Scene has no explicit spatial orientation.", category="spatial", entity_id=entity_id, unit_id=unit_id))
        cast = [item for item in _as_list(payload.get("cast")) if isinstance(item, dict)]
        if not cast:
            findings.append(_finding("warning", "scene-cast-missing", "Scene has no explicit cast or scene objects.", category="narrative", entity_id=entity_id, unit_id=unit_id))
        else:
            unclear = [item.get("name") or "Unnamed" for item in cast if not _text(item.get("visual")) or not _text(item.get("job"))]
            if unclear:
                findings.append(_finding("advisory", "scene-cast-description-incomplete", "Some scene characters or objects lack a visual description or explicit job.", category="narrative", entity_id=entity_id, unit_id=unit_id, details={"count": len(unclear), "examples": unclear[:8]}))
        if metrics["word_count"] > 1300:
            findings.append(_finding("warning", "scene-screen-density-high", "Scene story exceeds 1,300 words and may create a dense student reading screen.", category="readability", entity_id=entity_id, unit_id=unit_id, details=metrics))
        if metrics["paragraphs_over_220_words"]:
            findings.append(_finding("advisory", "scene-long-paragraph", "Scene contains at least one paragraph over 220 words.", category="readability", entity_id=entity_id, unit_id=unit_id, details=metrics))
        if metrics["average_sentence_words"] > 32:
            findings.append(_finding("advisory", "scene-sentence-density", "Average sentence length is above 32 words; review for student readability.", category="readability", entity_id=entity_id, unit_id=unit_id, details=metrics))
        if metrics["paragraph_count"] > 14:
            findings.append(_finding("advisory", "scene-paragraph-density", "Scene contains more than 14 narrative paragraphs on one student screen.", category="readability", entity_id=entity_id, unit_id=unit_id, details=metrics))
        zones = [item for item in _as_list(layout.get("zones")) if isinstance(item, dict)]
        if len(zones) > 8:
            findings.append(_finding("advisory", "scene-zone-density", "Scene uses more than eight spatial zones; review visual load.", category="screen_density", entity_id=entity_id, unit_id=unit_id, details={"zone_count": len(zones)}))
        if len(cast) > 8:
            findings.append(_finding("advisory", "scene-cast-density", "Scene introduces more than eight cast items; review memory load.", category="screen_density", entity_id=entity_id, unit_id=unit_id, details={"cast_count": len(cast)}))
        if base_payload is not None:
            before = {str(item) for item in _as_list(base_payload.get("object_ids")) if item not in (None, "")}
            after = {str(item) for item in _as_list(payload.get("object_ids")) if item not in (None, "")}
            missing = sorted(before - after)
            if missing:
                findings.append(_finding("warning", "scene-required-reference-reduced", "Working copy removes knowledge references present in the published scene. Review the scientific coverage before publication.", category="coverage", entity_id=entity_id, unit_id=unit_id, details={"removed_references": missing[:30], "removed_count": len(missing)}))

    elif entity_type == "journey":
        if not _text(payload.get("mission")):
            findings.append(_finding("warning", "journey-mission-missing", "Journey has no explicit student mission.", category="narrative", entity_id=entity_id, unit_id=unit_id))
        if not _text(payload.get("route_orientation")):
            findings.append(_finding("warning", "journey-route-orientation-missing", "Journey has no route orientation text.", category="spatial", entity_id=entity_id, unit_id=unit_id))
        if isinstance(payload.get("scenes"), list) and not payload.get("scenes"):
            findings.append(_finding("error", "journey-scenes-empty", "Journey working copy contains no scenes.", category="structure", entity_id=entity_id, unit_id=unit_id))

    elif entity_type == "concept":
        if not _text(payload.get("source_reference")):
            findings.append(_finding("advisory", "concept-source-reference-missing", "Canonical concept has no source reference in the normalized editor record.", category="science_trace", entity_id=entity_id, unit_id=unit_id))

    elif entity_type == "memory_object":
        if not _text(payload.get("productive_retrieval_target")):
            findings.append(_finding("warning", "memory-retrieval-target-missing", "Memory Object has no productive retrieval target.", category="retrieval", entity_id=entity_id, unit_id=unit_id))
        if not _text(payload.get("primary_palace_locus") or payload.get("locus_id")):
            findings.append(_finding("warning", "memory-locus-missing", "Memory Object has no explicit palace locus.", category="spatial", entity_id=entity_id, unit_id=unit_id))
        if not _text(payload.get("application_question")):
            findings.append(_finding("advisory", "memory-application-missing", "Memory Object has no application question in the normalized record.", category="retrieval", entity_id=entity_id, unit_id=unit_id))
        if not _text(payload.get("phonological_keyword")) and not _text(payload.get("mnemonic_actor")) and not _text(payload.get("mnemonic_object")):
            findings.append(_finding("advisory", "memory-mnemonic-cue-missing", "Memory Object has no explicit phonological or mnemonic cue in the editor record.", category="memory_design", entity_id=entity_id, unit_id=unit_id))

    elif entity_type == "question":
        knowledge_ids = [item for item in _as_list(payload.get("knowledge_ids")) if item not in (None, "")]
        if not knowledge_ids:
            findings.append(_finding("warning", "question-knowledge-link-missing", "Question has no linked knowledge ID.", category="coverage", entity_id=entity_id, unit_id=unit_id))
        choices = [str(item).strip() for item in _as_list(payload.get("choices")) if str(item or "").strip()]
        if choices and len(choices) < 2:
            findings.append(_finding("warning", "question-choice-count-low", "Question has fewer than two answer choices.", category="assessment", entity_id=entity_id, unit_id=unit_id))
        if choices and len({item.casefold() for item in choices}) != len(choices):
            findings.append(_finding("warning", "question-duplicate-choices", "Question contains duplicate answer choices.", category="assessment", entity_id=entity_id, unit_id=unit_id))
        if not _text(payload.get("explanation") or payload.get("canonical_science")):
            findings.append(_finding("advisory", "question-explanation-missing", "Question has no explanation or canonical-science note.", category="assessment", entity_id=entity_id, unit_id=unit_id))

    elif entity_type == "challenge":
        if not _as_list(payload.get("knowledge_ids")):
            findings.append(_finding("warning", "challenge-knowledge-link-missing", "Challenge Lab item has no linked knowledge ID.", category="coverage", entity_id=entity_id, unit_id=unit_id))
        if not _as_list(payload.get("prerequisite_loci")) and not _as_list(payload.get("prerequisite_scene_titles")):
            findings.append(_finding("advisory", "challenge-prerequisite-missing", "Challenge Lab item has no explicit prerequisite scene or locus.", category="retrieval", entity_id=entity_id, unit_id=unit_id))

    return findings


def entity_quality(
    entity_id: str,
    *,
    draft_id: str | None = None,
    source: str = "auto",
    course_id: str = "ap-biology",
) -> dict[str, Any]:
    resolved = _resolve_payload(
        entity_id,
        draft_id=draft_id,
        source=source,
        course_id=course_id,
    )
    base_payload = None
    if resolved.get("published_available") and resolved.get("source_state") != "published":
        try:
            base_payload = _published_payload(entity_id, course_id)
        except admin_drafts.DraftError:
            base_payload = None
    findings = _payload_quality(
        resolved["entity_type"],
        resolved["payload"],
        entity_id=entity_id,
        unit_id=resolved.get("unit_id"),
        base_payload=base_payload,
    )
    dependency = (
        admin_catalog.dependency_report(entity_id, course_id=course_id, depth=1, limit=200)
        if _catalog_entity(entity_id, course_id)
        else None
    )
    return {
        "schema": QUALITY_SCHEMA,
        "course_id": course_id,
        "course_title": _course_title(course_id),
        "entity_id": entity_id,
        "entity_type": resolved["entity_type"],
        "unit_id": resolved.get("unit_id"),
        "source_state": resolved.get("source_state"),
        "draft_id": resolved.get("draft_id"),
        "draft_version": resolved.get("draft_version"),
        "error_count": sum(1 for item in findings if item["severity"] == "error"),
        "warning_count": sum(1 for item in findings if item["severity"] == "warning"),
        "advisory_count": sum(1 for item in findings if item["severity"] == "advisory"),
        "findings": findings,
        "dependency_counts": dependency.get("related_counts_by_type", {}) if dependency else {},
    }


def _aggregate_findings(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str, str | None], list[dict[str, Any]]] = defaultdict(list)
    passthrough: list[dict[str, Any]] = []
    for item in findings:
        if item.get("details", {}).get("aggregate") is False:
            passthrough.append(item)
            continue
        key = (item["severity"], item["code"], item["category"], item.get("unit_id"))
        grouped[key].append(item)
    result = list(passthrough)
    for (_severity, _code, _category, _unit), items in grouped.items():
        first = deepcopy(items[0])
        if len(items) > 1:
            first["details"] = {
                **first.get("details", {}),
                "count": len(items),
                "sample_entity_ids": [item.get("entity_id") for item in items if item.get("entity_id")][:12],
            }
            first["entity_id"] = None
            first["message"] = f"{first['message']} ({len(items)} records)"
        result.append(first)
    return result


@lru_cache(maxsize=32)
def _published_quality_findings(course_id: str = "ap-biology") -> tuple[dict[str, Any], ...]:
    _require_course_catalog(course_id)
    findings: list[dict[str, Any]] = []
    snapshot = admin_catalog.catalog(course_id)

    for problem in admin_catalog.content_health(course_id).get("problems", []):
        findings.append(
            _finding(
                str(problem.get("severity") or "warning"),
                str(problem.get("code") or "catalog-health"),
                str(problem.get("message") or "Catalog health issue"),
                category="structure",
                details={key: value for key, value in problem.items() if key not in {"severity", "code", "message"}},
            )
        )

    concepts_by_unit: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for entity in snapshot["entities"].values():
        if entity.get("type") == "concept" and entity.get("unit_id"):
            concepts_by_unit[str(entity["unit_id"])].append(entity)
    for unit_id, concepts in concepts_by_unit.items():
        no_scene = [item for item in concepts if int((item.get("coverage") or {}).get("scenes") or 0) == 0]
        if no_scene:
            findings.append(_finding("advisory", "concept-scene-coverage-gap", "Canonical concepts have no explicit scene-level teaches_concept link.", category="coverage", unit_id=unit_id, details={"count": len(no_scene), "sample_entity_ids": [item["id"] for item in no_scene[:12]]}))
        no_retrieval = [
            item
            for item in concepts
            if sum(int((item.get("coverage") or {}).get(key) or 0) for key in ("questions", "challenge_items", "mixed_sets")) == 0
        ]
        if no_retrieval:
            findings.append(_finding("advisory", "concept-retrieval-coverage-gap", "Canonical concepts have no indexed question, mixed-discrimination set, or Challenge Lab link.", category="retrieval", unit_id=unit_id, details={"count": len(no_retrieval), "sample_entity_ids": [item["id"] for item in no_retrieval[:12]]}))

    course_payload = course_packages.course(course_id)
    for unit in course_payload.get("units", []):
        if not isinstance(unit, dict) or not unit.get("unit_id"):
            continue
        unit_id = str(unit["unit_id"])
        try:
            timeline = admin_management.review_timeline(unit_id, course_id)
        except admin_drafts.DraftError:
            continue
        gaps = timeline.get("coverage_gaps", [])
        if gaps:
            findings.append(_finding("warning", "review-timeline-gap", "Scene-linked knowledge IDs have no indexed later retrieval event in the review timeline.", category="retrieval", unit_id=unit_id, details={"count": len(gaps), "sample_knowledge_ids": [item.get("knowledge_id") for item in gaps[:15]]}))

    for unit in course_payload.get("units", []):
        if not isinstance(unit, dict) or not unit.get("unit_id"):
            continue
        unit_id = str(unit["unit_id"])
        registry_payload = course_packages.journeys(course_id, unit_id)
        for registry in registry_payload.get("guided_journeys", []):
            if not isinstance(registry, dict) or not registry.get("palace_id"):
                continue
            palace_id = str(registry["palace_id"])
            journey = course_packages.journey(course_id, unit_id, palace_id)
            if not isinstance(journey, dict):
                continue
            scenes = [item for item in _as_list(journey.get("scenes")) if isinstance(item, dict)]
            expected_indices = list(range(len(scenes)))
            actual_indices = [int(item.get("scene_index", index)) for index, item in enumerate(scenes)]
            if actual_indices != expected_indices:
                findings.append(_finding("error", "journey-scene-index-sequence", "Journey scene indices are not a continuous zero-based route.", category="structure", entity_id=f"journey:{unit_id}:{palace_id}", unit_id=unit_id, details={"actual": actual_indices, "expected": expected_indices}))
            route = [item for item in _as_list(journey.get("route")) if isinstance(item, dict)]
            if route and len(route) != len(scenes):
                findings.append(_finding("warning", "journey-route-count-mismatch", "Journey route node count does not match its scene count.", category="continuity", entity_id=f"journey:{unit_id}:{palace_id}", unit_id=unit_id, details={"route_count": len(route), "scene_count": len(scenes)}))
            for index, scene in enumerate(scenes):
                scene_id = f"scene:{unit_id}:{palace_id}:{int(scene.get('scene_index', index))}"
                normalized = {"id": scene_id, "type": "scene", "unit_id": unit_id, **deepcopy(scene)}
                findings.extend(_payload_quality("scene", normalized, entity_id=scene_id, unit_id=unit_id))
                if index < len(scenes) - 1 and _text(scene.get("next_locus")):
                    expected = {_text(scenes[index + 1].get(key)).casefold() for key in ("locus", "locus_id", "title") if _text(scenes[index + 1].get(key))}
                    next_locus = _text(scene.get("next_locus")).casefold()
                    if expected and next_locus not in expected and len(next_locus) < 180:
                        findings.append(_finding("advisory", "scene-next-locus-review", "Scene next-locus label differs from the following scene's primary labels; review narrative continuity.", category="continuity", entity_id=scene_id, unit_id=unit_id, details={"next_locus": scene.get("next_locus"), "following_scene": scenes[index + 1].get("title")}))

    return tuple(_aggregate_findings(findings))


def clear_quality_cache() -> None:
    _published_quality_findings.cache_clear()


def _draft_findings(
    course_id: str = "ap-biology",
    unit_id: str | None = None,
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    active = admin_management._active_draft_rows(course_id)
    for entity_id, summary in active.items():
        if unit_id and summary.get("unit_id") != unit_id:
            continue
        try:
            draft = admin_drafts.get_draft(summary["draft_id"], course_id=course_id)
        except admin_drafts.DraftError:
            continue
        base_payload = None
        if _catalog_entity(entity_id, course_id):
            try:
                base_payload = _published_payload(entity_id, course_id)
            except admin_drafts.DraftError:
                base_payload = None
        findings.extend(
            _payload_quality(
                str(draft.get("entity_type") or ""),
                draft.get("payload") or {},
                entity_id=entity_id,
                unit_id=draft.get("unit_id"),
                base_payload=base_payload,
            )
        )
    return findings


def _media_findings(
    course_id: str = "ap-biology",
    unit_id: str | None = None,
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    try:
        media = admin_management.list_staged_media(
            course_id=course_id,
            status="staged",
            unit_id=unit_id,
            limit=500,
        ).get("items", [])
    except (admin_drafts.DraftError, OSError):
        return findings
    for item in media:
        entity_id = item.get("entity_id") or item.get("asset_id")
        item_unit = item.get("unit_id")
        kind = item.get("kind")
        if kind == "image" and not _text(item.get("alt_text")):
            findings.append(_finding("warning", "media-alt-text-missing", "Staged image has no alternative text.", category="accessibility", entity_id=str(entity_id), unit_id=item_unit, details={"asset_id": item.get("asset_id"), "filename": item.get("original_filename")}))
        if kind in {"audio", "video"} and not _text(item.get("transcript")):
            findings.append(_finding("warning", "media-transcript-missing", "Staged audio or video has no transcript.", category="accessibility", entity_id=str(entity_id), unit_id=item_unit, details={"asset_id": item.get("asset_id"), "filename": item.get("original_filename")}))
        if kind in {"image", "video", "document"} and not _text(item.get("caption")):
            findings.append(_finding("advisory", "media-caption-missing", "Staged visual or document has no caption or contextual description.", category="accessibility", entity_id=str(entity_id), unit_id=item_unit, details={"asset_id": item.get("asset_id"), "filename": item.get("original_filename")}))
    return findings


def quality_report(
    *,
    course_id: str = "ap-biology",
    unit_id: str | None = None,
) -> dict[str, Any]:
    _require_course_catalog(course_id)
    if unit_id:
        _require_course_unit(course_id, unit_id)
    findings = [
        deepcopy(item)
        for item in _published_quality_findings(course_id)
        if not unit_id or item.get("unit_id") in {None, unit_id}
    ]
    findings.extend(_draft_findings(course_id, unit_id))
    findings.extend(_media_findings(course_id, unit_id))
    severity_order = {"error": 0, "warning": 1, "advisory": 2}
    findings.sort(key=lambda item: (severity_order.get(item["severity"], 9), item.get("unit_id") or "", item["category"], item["code"], item.get("entity_id") or ""))
    categories: dict[str, int] = defaultdict(int)
    for item in findings:
        categories[item["category"]] += 1
    return {
        "schema": QUALITY_SCHEMA,
        "course_id": course_id,
        "course_title": _course_title(course_id),
        "scope": {"course_id": course_id, "unit_id": unit_id or "all"},
        "error_count": sum(1 for item in findings if item["severity"] == "error"),
        "warning_count": sum(1 for item in findings if item["severity"] == "warning"),
        "advisory_count": sum(1 for item in findings if item["severity"] == "advisory"),
        "publication_blocking_count": sum(1 for item in findings if item.get("publication_blocking")),
        "category_counts": dict(sorted(categories.items())),
        "finding_count": len(findings),
        "findings": findings,
        "policy": {
            "errors": "Structural or validation failures that must be resolved before Step 9 publication.",
            "warnings": "Content or accessibility risks that require teacher review before publication.",
            "advisories": "Heuristic quality signals for readability, continuity, memory load, and coverage; teacher judgment controls the decision.",
        },
    }
