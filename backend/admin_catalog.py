from __future__ import annotations

from collections import defaultdict, deque
from functools import lru_cache
import json
from pathlib import Path
import re
from typing import Any, Iterable

from . import content, course_packages
from .settings import ROOT

CATALOG_SCHEMA = "story-method-content-studio-catalog-1.1"
DEFAULT_COURSE_ID = "ap-biology"


def catalog_courses() -> dict[str, Any]:
    registry = content.course_registry()
    items: list[dict[str, Any]] = []
    for record in registry.get("courses", []):
        if not isinstance(record, dict):
            continue
        course_id = str(record.get("course_id") or "")
        package_result: dict[str, Any] = {"valid": False, "errors": ["Course package not checked"]}
        try:
            package_result = course_packages.validate_package(course_id)
        except Exception as exc:
            package_result = {"valid": False, "errors": [str(exc)], "warnings": []}
        catalog_ready = bool(package_result.get("valid"))
        editable = catalog_ready and record.get("status") == "available"
        items.append(
            {
                **record,
                "catalog_ready": catalog_ready,
                "editable": editable,
                "catalog_mode": "editable" if editable else ("read_only" if catalog_ready else "preparing"),
                "package_validation": {
                    "valid": catalog_ready,
                    "errors": package_result.get("errors", []),
                    "warnings": package_result.get("warnings", []),
                },
            }
        )
    return {
        "platform_id": registry.get("platform_id", "the-story-method"),
        "platform_title": registry.get("platform_title", "The Story Method"),
        "courses": items,
    }


def course_access(course_id: str | None) -> dict[str, Any]:
    resolved = str(course_id or DEFAULT_COURSE_ID).strip()
    record = next(
        (item for item in catalog_courses()["courses"] if item.get("course_id") == resolved),
        None,
    )
    if record is None:
        raise ValueError(f"Course '{resolved}' is not registered")
    return record


def require_editable_course(course_id: str | None) -> dict[str, Any]:
    record = course_access(course_id)
    if not record.get("editable"):
        raise ValueError(
            f"Content Studio editing is not enabled for course '{record.get('course_id')}'. "
            "The course catalog is available in read-only architecture preview mode."
        )
    return record


def _catalog_course_id(course_id: str | None) -> str:
    record = course_access(course_id)
    if not record.get("catalog_ready"):
        raise ValueError(f"Content Studio catalog is not available for course '{record.get('course_id')}'")
    return str(record["course_id"])


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _first(record: dict[str, Any], keys: Iterable[str], default: Any = None) -> Any:
    for key in keys:
        if key in record and record[key] not in (None, ""):
            return record[key]
    return default


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _slug(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip()).strip("-").lower()
    return cleaned or "unnamed"


def _word_count(paragraphs: Any) -> int:
    text = " ".join(str(part) for part in _as_list(paragraphs) if part)
    text = re.sub(r"[*_`#>]", " ", text)
    return len(re.findall(r"\b\w+[\w′'/-]*\b", text, flags=re.UNICODE))


def _repo_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def _records_from_payload(payload: Any, keys: Iterable[str]) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in keys:
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
    return []


def _artifact_records(course_id: str, unit_id: str, artifact_name: str) -> tuple[list[dict[str, Any]], str | None]:
    records = course_packages.artifact_records(course_id, unit_id, artifact_name)
    return records, course_packages.artifact_source_path(course_id, unit_id, artifact_name)


def _canonical_records(course_id: str, unit_id: str) -> tuple[list[dict[str, Any]], str | None]:
    return _artifact_records(course_id, unit_id, "concepts")


def _memory_records(course_id: str, unit_id: str) -> tuple[list[dict[str, Any]], str | None]:
    return (
        course_packages.memory_objects(course_id, unit_id),
        course_packages.artifact_source_path(course_id, unit_id, "memory_objects"),
    )


def _review_records(course_id: str, unit_id: str) -> tuple[list[dict[str, Any]], str | None]:
    return _artifact_records(course_id, unit_id, "review")


def _mixed_sets(course_id: str, unit_id: str) -> tuple[list[dict[str, Any]], str | None]:
    return _artifact_records(course_id, unit_id, "mixed_discrimination")


def _challenge_records(course_id: str, unit_id: str) -> tuple[list[dict[str, Any]], str | None]:
    return _artifact_records(course_id, unit_id, "challenge_lab")


def _release_manifest(course_id: str) -> dict[str, Any]:
    manifest = course_packages.package_manifest(course_id)
    content_root = ROOT / str(manifest.get("content_root") or f"content/{course_id}")
    preferred = content_root / "mainline-release-u1-u8.json"
    candidates = [preferred] if preferred.exists() else sorted(content_root.glob("mainline-release*.json"))
    path = candidates[-1] if candidates else None
    payload = _read_json(path) if path is not None and path.exists() else {}
    return payload if isinstance(payload, dict) else {}


class CatalogBuilder:
    def __init__(self, course_id: str = DEFAULT_COURSE_ID) -> None:
        self.course_id = _catalog_course_id(course_id)
        self.course_entity_id = f"course:{self.course_id}"
        self.entities: dict[str, dict[str, Any]] = {}
        self.edges: list[dict[str, str]] = []
        self._edge_keys: set[tuple[str, str, str]] = set()
        self.aliases: dict[tuple[str, str], dict[str, str]] = defaultdict(dict)
        self.unresolved: list[dict[str, Any]] = []
        self.journey_by_raw: dict[tuple[str, str], str] = {}
        self.scene_by_locator: dict[tuple[str, str], str] = {}
        self.scene_by_title: dict[tuple[str, str], list[str]] = defaultdict(list)
        self.character_by_key: dict[tuple[str, str], str] = {}

    def add_entity(
        self,
        entity: dict[str, Any],
        aliases: Iterable[tuple[str, str | None]] = (),
    ) -> str:
        entity.setdefault("course_id", self.course_id)
        entity_id = str(entity["id"])
        current = self.entities.get(entity_id)
        if current is None:
            self.entities[entity_id] = entity
            current = entity
        else:
            for key, value in entity.items():
                if key not in current or current[key] in (None, "", [], {}):
                    current[key] = value
        for unit_id, raw in aliases:
            if raw not in (None, ""):
                self.aliases[(unit_id, str(raw))][current["type"]] = entity_id
        return entity_id

    def edge(self, source: str, target: str, kind: str) -> None:
        if source not in self.entities or target not in self.entities:
            return
        key = (source, target, kind)
        if key in self._edge_keys:
            return
        self._edge_keys.add(key)
        self.edges.append({"from": source, "to": target, "kind": kind})

    def resolve(
        self,
        unit_id: str,
        raw: Any,
        prefer: Iterable[str] = ("memory_object", "concept"),
    ) -> str | None:
        if raw in (None, ""):
            return None
        matches = self.aliases.get((unit_id, str(raw)), {})
        for entity_type in prefer:
            if entity_type in matches:
                return matches[entity_type]
        return next(iter(matches.values()), None)

    def unresolved_ref(self, unit_id: str, source_id: str, raw_ref: Any, relation: str) -> None:
        if raw_ref in (None, ""):
            return
        self.unresolved.append(
            {
                "unit_id": unit_id,
                "source_id": source_id,
                "raw_reference": str(raw_ref),
                "relation": relation,
            }
        )

    def build(self) -> dict[str, Any]:
        course_payload = content.course_by_id(self.course_id)
        if not isinstance(course_payload, dict):
            raise ValueError(f"Course '{self.course_id}' is not available")
        release = _release_manifest()
        self.add_entity(
            {
                "id": self.course_entity_id,
                "type": "course",
                "course_id": self.course_id,
                "title": course_payload.get("course_title") or course_payload.get("title", self.course_id),
                "release_status": release.get("release_status"),
                "runtime_version": release.get("runtime_version"),
            }
        )
        units = [item for item in course_payload.get("units", []) if isinstance(item, dict)]
        for unit in units:
            self._add_unit(unit)
        for unit in units:
            unit_id = str(unit.get("unit_id"))
            self._add_concepts(unit_id)
            self._add_memory_objects(unit_id)
        for unit in units:
            self._add_journeys(str(unit.get("unit_id")))
        for unit in units:
            unit_id = str(unit.get("unit_id"))
            self._add_review_questions(unit_id)
            self._add_mixed_questions(unit_id)
            self._add_challenges(unit_id)
        self._attach_dependency_counts()
        return self._snapshot(release)

    def _add_unit(self, unit: dict[str, Any]) -> None:
        unit_id = str(unit.get("unit_id"))
        summary = content.unit_summary(unit_id) or unit
        entity_id = f"unit:{unit_id}"
        self.add_entity(
            {
                "id": entity_id,
                "type": "unit",
                "unit_id": unit_id,
                "number": summary.get("number"),
                "title": summary.get("title") or summary.get("unit_title") or unit_id,
                "status": summary.get("status") or summary.get("release_status") or summary.get("student_release"),
                "reported_canonical_records": summary.get("canonical_records"),
                "reported_journeys": summary.get("journeys") or summary.get("journey_count") or summary.get("guided_journeys"),
                "reported_scenes": summary.get("permanent_loci") or summary.get("scene_count") or summary.get("scenes"),
                "reported_challenges": summary.get("application_challenges") or summary.get("challenge_count"),
            },
            aliases=[(unit_id, unit_id)],
        )
        self.edge(self.course_entity_id, entity_id, "contains")

    def _add_concepts(self, unit_id: str) -> None:
        records, source_path = _canonical_records(unit_id)
        unit_entity = f"unit:{unit_id}"
        for index, record in enumerate(records):
            knowledge_id = str(
                _first(
                    record,
                    ("knowledge_id", "Knowledge ID", "source_knowledge_id", "record_id", "id"),
                    f"canonical-{index + 1:04d}",
                )
            )
            label = str(
                _first(
                    record,
                    ("canonical_label", "Canonical Label", "canonical_term", "term", "label", "title"),
                    knowledge_id,
                )
            )
            definition = _first(
                record,
                (
                    "canonical_verified_statement",
                    "Canonical Verified Statement",
                    "canonical_definition",
                    "definition",
                    "statement",
                ),
            )
            entity_id = f"concept:{unit_id}:{knowledge_id}"
            self.add_entity(
                {
                    "id": entity_id,
                    "type": "concept",
                    "unit_id": unit_id,
                    "knowledge_id": knowledge_id,
                    "title": label,
                    "canonical_term": label,
                    "canonical_definition": definition,
                    "topic": _first(record, ("topic", "Topic", "ced_topic", "CED Topic")),
                    "scope_class": _first(record, ("scope_class", "Scope Class", "ap_scope_class", "AP Scope Class")),
                    "source_reference": _first(record, ("source_reference", "Source Reference", "source_trace", "Source Trace")),
                    "scientific_lock_status": _first(record, ("canonical_lock", "Canonical Lock", "scientific_lock_status")),
                    "source_path": source_path,
                },
                aliases=[(unit_id, knowledge_id)],
            )
            self.edge(unit_entity, entity_id, "defines")

    def _add_memory_objects(self, unit_id: str) -> None:
        records, source_path = _memory_records(unit_id)
        unit_entity = f"unit:{unit_id}"
        for index, record in enumerate(records):
            memory_id = str(
                _first(record, ("memory_object_id", "object_id", "knowledge_id"), f"memory-{index + 1:04d}")
            )
            source_knowledge_id = _first(record, ("source_knowledge_id", "knowledge_id", "Knowledge ID"))
            title = str(_first(record, ("canonical_term", "canonical_label", "term", "title"), memory_id))
            entity_id = f"memory:{unit_id}:{memory_id}"
            self.add_entity(
                {
                    "id": entity_id,
                    "type": "memory_object",
                    "unit_id": unit_id,
                    "memory_object_id": memory_id,
                    "source_knowledge_id": source_knowledge_id,
                    "title": title,
                    "canonical_term": title,
                    "canonical_definition": _first(
                        record,
                        ("canonical_definition", "canonical_verified_statement", "definition"),
                    ),
                    "object_type": record.get("object_type"),
                    "palace_zone": record.get("palace_zone"),
                    "primary_palace_locus": record.get("primary_palace_locus"),
                    "locus_id": record.get("locus_id"),
                    "scene_index": record.get("scene_index"),
                    "confusable_terms": record.get("confusable_terms") or record.get("confusable_set_ids"),
                    "exact_name_required": record.get("exact_name_required"),
                    "exact_spelling_required": record.get("exact_spelling_required"),
                    "productive_retrieval_target": record.get("productive_retrieval_target"),
                    "application_question": record.get("application_question"),
                    "source_trace": record.get("source_trace") or record.get("source_reference"),
                    "version_status": record.get("version_status"),
                    "source_path": source_path,
                },
                aliases=[(unit_id, memory_id)],
            )
            self.edge(unit_entity, entity_id, "contains")
            if source_knowledge_id:
                concept_id = self.resolve(unit_id, source_knowledge_id, ("concept",))
                if concept_id:
                    self.edge(entity_id, concept_id, "represents")
                else:
                    self.unresolved_ref(unit_id, entity_id, source_knowledge_id, "represents_concept")

    def _add_journeys(self, unit_id: str) -> None:
        unit_entity = f"unit:{unit_id}"
        for journey_index, registry_record in enumerate(content.journey_registry(unit_id)):
            palace_id = str(registry_record.get("palace_id") or f"journey-{journey_index + 1}")
            payload = content.journey_by_id(unit_id, palace_id) or dict(registry_record)
            journey_id = f"journey:{unit_id}:{palace_id}"
            self.journey_by_raw[(unit_id, palace_id)] = journey_id
            self.add_entity(
                {
                    "id": journey_id,
                    "type": "journey",
                    "unit_id": unit_id,
                    "palace_id": palace_id,
                    "order": journey_index,
                    "title": payload.get("story_title") or registry_record.get("story_title") or palace_id,
                    "story_title": payload.get("story_title") or registry_record.get("story_title"),
                    "palace_name": payload.get("palace_name") or registry_record.get("palace_name"),
                    "tagline": payload.get("tagline") or registry_record.get("tagline"),
                    "premise": payload.get("premise"),
                    "mission": payload.get("mission"),
                    "finale": payload.get("finale"),
                    "estimated_minutes": payload.get("estimated_minutes"),
                    "route_orientation": payload.get("route_orientation"),
                    "scene_count": payload.get("scene_count") or registry_record.get("scene_count"),
                    "checkpoint_count": payload.get("checkpoint_count") or registry_record.get("checkpoint_count"),
                    "guide": payload.get("guide"),
                    "source_path": f"content/ap-biology/{unit_id}/journeys/{palace_id}.json",
                },
                aliases=[(unit_id, palace_id)],
            )
            self.edge(unit_entity, journey_id, "contains")
            guide = payload.get("guide")
            if isinstance(guide, dict) and guide.get("name"):
                character_id = self._character(unit_id, guide, journey_id=journey_id)
                self.edge(journey_id, character_id, "guided_by")
            for scene in payload.get("scenes", []):
                if isinstance(scene, dict):
                    self._add_scene(unit_id, journey_id, palace_id, scene)

    def _character(
        self,
        unit_id: str,
        record: dict[str, Any],
        *,
        journey_id: str | None = None,
        scene_id: str | None = None,
    ) -> str:
        name = str(record.get("name") or "Unnamed character")
        key = (unit_id, name.casefold())
        character_id = self.character_by_key.get(key)
        if character_id is None:
            base = f"character:{unit_id}:{_slug(name)}"
            character_id = base
            suffix = 2
            while character_id in self.entities and self.entities[character_id].get("title") != name:
                character_id = f"{base}-{suffix}"
                suffix += 1
            self.character_by_key[key] = character_id
            self.add_entity(
                {
                    "id": character_id,
                    "type": "character",
                    "unit_id": unit_id,
                    "title": name,
                    "name": name,
                    "kind": record.get("kind") or record.get("role"),
                    "role": record.get("role") or record.get("job"),
                    "visual": record.get("visual"),
                    "job": record.get("job") or record.get("story_job"),
                    "journey_ids": [],
                    "scene_ids": [],
                }
            )
        entity = self.entities[character_id]
        if journey_id and journey_id not in entity["journey_ids"]:
            entity["journey_ids"].append(journey_id)
        if scene_id and scene_id not in entity["scene_ids"]:
            entity["scene_ids"].append(scene_id)
        return character_id

    def _add_scene(
        self,
        unit_id: str,
        journey_id: str,
        palace_id: str,
        scene: dict[str, Any],
    ) -> None:
        scene_index = int(scene.get("scene_index", 0))
        scene_id = f"scene:{unit_id}:{palace_id}:{scene_index}"
        locus = str(scene.get("locus") or scene.get("title") or f"Scene {scene_index + 1}")
        locus_id = scene.get("locus_id")
        paragraphs = scene.get("story_paragraphs") or []
        layout = scene.get("scene_layout") if isinstance(scene.get("scene_layout"), dict) else {}
        object_ids = [str(value) for value in _as_list(scene.get("object_ids")) if value not in (None, "")]
        beats = [item for item in _as_list(scene.get("story_beats")) if isinstance(item, dict)]
        if not object_ids:
            object_ids = [str(item.get("object_id")) for item in beats if item.get("object_id")]
        cast = [item for item in _as_list(scene.get("cast")) if isinstance(item, dict)]
        character_names = [str(item.get("name")) for item in cast if item.get("name")]
        self.add_entity(
            {
                "id": scene_id,
                "type": "scene",
                "unit_id": unit_id,
                "journey_id": journey_id,
                "palace_id": palace_id,
                "scene_index": scene_index,
                "locus_id": locus_id,
                "locus": locus,
                "title": scene.get("title") or locus,
                "scene_kicker": scene.get("scene_kicker"),
                "location_description": scene.get("location_description"),
                "orientation": layout.get("orientation"),
                "object_ids": object_ids,
                "character_names": character_names,
                "checkpoint": bool(scene.get("checkpoint")),
                "checkpoint_object_id": scene.get("checkpoint_object_id"),
                "checkpoint_prompt": scene.get("checkpoint_prompt"),
                "next_locus": scene.get("next_locus"),
                "story_word_count": _word_count(paragraphs),
                "story_paragraph_count": len(_as_list(paragraphs)),
                "story_preview": str(paragraphs[0])[:320] if isinstance(paragraphs, list) and paragraphs else str(scene.get("story_open") or "")[:320],
                "source_path": f"content/ap-biology/{unit_id}/journeys/{palace_id}.json",
            },
            aliases=[(unit_id, str(locus_id))] if locus_id else [],
        )
        self.edge(journey_id, scene_id, "contains")
        self.scene_by_locator[(unit_id, f"{palace_id}:{scene_index}")] = scene_id
        if locus_id:
            self.scene_by_locator[(unit_id, str(locus_id))] = scene_id
        scene_title = str(scene.get("title") or "")
        if scene_title:
            self.scene_by_title[(unit_id, scene_title)].append(scene_id)

        location_raw = str(locus_id or f"{palace_id}-{scene_index}")
        location_id = f"location:{unit_id}:{location_raw}"
        self.add_entity(
            {
                "id": location_id,
                "type": "location",
                "unit_id": unit_id,
                "journey_id": journey_id,
                "scene_id": scene_id,
                "title": locus,
                "locus": locus,
                "locus_id": locus_id,
                "description": scene.get("location_description"),
                "orientation": layout.get("orientation"),
                "zones": layout.get("zones", []),
            },
            aliases=[(unit_id, location_raw)],
        )
        self.edge(scene_id, location_id, "located_at")

        for cast_record in cast:
            if cast_record.get("name"):
                character_id = self._character(
                    unit_id,
                    cast_record,
                    journey_id=journey_id,
                    scene_id=scene_id,
                )
                self.edge(scene_id, character_id, "features")

        for raw_object_id in object_ids:
            target = self.resolve(unit_id, raw_object_id, ("memory_object", "concept"))
            if not target:
                self.unresolved_ref(unit_id, scene_id, raw_object_id, "teaches")
                continue
            self.edge(scene_id, target, "teaches")
            if self.entities[target]["type"] == "memory_object":
                for edge in list(self.edges):
                    if edge["from"] == target and edge["kind"] == "represents":
                        self.edge(scene_id, edge["to"], "teaches_concept")

        checkpoint_object_id = scene.get("checkpoint_object_id")
        checkpoint_prompt = scene.get("checkpoint_prompt")
        if scene.get("checkpoint") or checkpoint_prompt:
            question_id = f"question:{unit_id}:QR-{palace_id}-{scene_index}"
            self.add_entity(
                {
                    "id": question_id,
                    "type": "question",
                    "question_type": "quick_recall",
                    "unit_id": unit_id,
                    "journey_id": journey_id,
                    "scene_id": scene_id,
                    "title": f"Quick Recall · {self.entities[scene_id]['title']}",
                    "prompt": checkpoint_prompt or "Quick Recall",
                    "answer": None,
                    "knowledge_ids": [checkpoint_object_id] if checkpoint_object_id else [],
                    "source_path": f"content/ap-biology/{unit_id}/journeys/{palace_id}.json",
                }
            )
            self.edge(scene_id, question_id, "contains_question")
            self.edge(question_id, scene_id, "attached_to")
            if checkpoint_object_id:
                target = self.resolve(unit_id, checkpoint_object_id, ("memory_object", "concept"))
                if target:
                    self.edge(question_id, target, "assesses")
                else:
                    self.unresolved_ref(unit_id, question_id, checkpoint_object_id, "assesses")

    def _add_review_questions(self, unit_id: str) -> None:
        records, source_path = _review_records(unit_id)
        for index, record in enumerate(records):
            knowledge_id = _first(record, ("knowledge_id", "memory_object_id", "object_id"))
            raw_id = str(knowledge_id or f"review-{index + 1:04d}")
            question_id = f"question:{unit_id}:REV-{raw_id}-{index + 1}"
            journey_raw = record.get("journey_id") or record.get("palace_id")
            scene_index = record.get("scene_index")
            journey_id = self.journey_by_raw.get((unit_id, str(journey_raw))) if journey_raw else None
            scene_id = None
            if journey_raw is not None and scene_index is not None:
                scene_id = self.scene_by_locator.get((unit_id, f"{journey_raw}:{scene_index}"))
            if scene_id is None and record.get("scene_title"):
                candidates = self.scene_by_title.get((unit_id, str(record.get("scene_title"))), [])
                if len(candidates) == 1:
                    scene_id = candidates[0]
            self.add_entity(
                {
                    "id": question_id,
                    "type": "question",
                    "question_type": "review",
                    "unit_id": unit_id,
                    "journey_id": journey_id,
                    "scene_id": scene_id,
                    "title": f"Review · {record.get('target_answer') or raw_id}",
                    "prompt": record.get("prompt"),
                    "answer": record.get("target_answer"),
                    "explanation": record.get("canonical_science"),
                    "knowledge_ids": [knowledge_id] if knowledge_id else [],
                    "initial_review_window_hours": record.get("initial_review_window_hours"),
                    "source_path": source_path,
                }
            )
            if journey_id:
                self.edge(question_id, journey_id, "attached_to_journey")
            if scene_id:
                self.edge(question_id, scene_id, "attached_to")
            if knowledge_id:
                target = self.resolve(unit_id, knowledge_id, ("concept", "memory_object"))
                if target:
                    self.edge(question_id, target, "assesses")
                else:
                    self.unresolved_ref(unit_id, question_id, knowledge_id, "assesses")

    def _add_mixed_questions(self, unit_id: str) -> None:
        sets, source_path = _mixed_sets(unit_id)
        unit_entity = f"unit:{unit_id}"
        for set_index, record in enumerate(sets):
            set_raw = str(record.get("set_id") or f"MD-{set_index + 1}")
            set_id = f"question_set:{unit_id}:{set_raw}"
            self.add_entity(
                {
                    "id": set_id,
                    "type": "question_set",
                    "question_type": "mixed_discrimination",
                    "unit_id": unit_id,
                    "set_id": set_raw,
                    "title": record.get("title") or set_raw,
                    "purpose": record.get("purpose"),
                    "knowledge_ids": record.get("knowledge_ids", []),
                    "terms": record.get("terms", []),
                    "initial_delay_hours": record.get("initial_delay_hours"),
                    "source_path": source_path,
                }
            )
            self.edge(unit_entity, set_id, "contains_question_set")
            for knowledge_id in _as_list(record.get("knowledge_ids")):
                target = self.resolve(unit_id, knowledge_id, ("concept", "memory_object"))
                if target:
                    self.edge(set_id, target, "discriminates")
                else:
                    self.unresolved_ref(unit_id, set_id, knowledge_id, "discriminates")
            for q_index, question in enumerate(_as_list(record.get("questions"))):
                if not isinstance(question, dict):
                    continue
                raw_question_id = str(question.get("question_id") or f"{set_raw}-Q{q_index + 1}")
                question_id = f"question:{unit_id}:{raw_question_id}"
                knowledge_id = question.get("knowledge_id")
                self.add_entity(
                    {
                        "id": question_id,
                        "type": "question",
                        "question_type": "mixed_discrimination",
                        "unit_id": unit_id,
                        "question_set_id": set_id,
                        "title": record.get("title") or raw_question_id,
                        "prompt": question.get("prompt"),
                        "choices": question.get("choices", []),
                        "answer": question.get("answer"),
                        "explanation": question.get("explanation"),
                        "knowledge_ids": [knowledge_id] if knowledge_id else [],
                        "source_path": source_path,
                    },
                    aliases=[(unit_id, raw_question_id)],
                )
                self.edge(set_id, question_id, "contains_question")
                if knowledge_id:
                    target = self.resolve(unit_id, knowledge_id, ("concept", "memory_object"))
                    if target:
                        self.edge(question_id, target, "assesses")
                    else:
                        self.unresolved_ref(unit_id, question_id, knowledge_id, "assesses")

    def _add_challenges(self, unit_id: str) -> None:
        records, source_path = _challenge_records(unit_id)
        unit_entity = f"unit:{unit_id}"
        for index, record in enumerate(records):
            raw_id = str(record.get("challenge_id") or f"CL-{index + 1}")
            challenge_id = f"challenge:{unit_id}:{raw_id}"
            knowledge_id = record.get("knowledge_id")
            self.add_entity(
                {
                    "id": challenge_id,
                    "type": "challenge",
                    "question_type": "challenge_lab",
                    "unit_id": unit_id,
                    "challenge_id": raw_id,
                    "title": record.get("title") or raw_id,
                    "domain": record.get("domain"),
                    "challenge_type": record.get("type"),
                    "prompt": record.get("prompt"),
                    "answer": record.get("answer_guide") or record.get("answer"),
                    "knowledge_ids": [knowledge_id] if knowledge_id else [],
                    "prerequisite_loci": record.get("prerequisite_loci", []),
                    "prerequisite_scene_titles": record.get("prerequisite_scene_titles", []),
                    "source_assessment": record.get("source_assessment"),
                    "source_path": source_path,
                },
                aliases=[(unit_id, raw_id)],
            )
            self.edge(unit_entity, challenge_id, "contains_challenge")
            if knowledge_id:
                target = self.resolve(unit_id, knowledge_id, ("concept", "memory_object"))
                if target:
                    self.edge(challenge_id, target, "assesses")
                else:
                    self.unresolved_ref(unit_id, challenge_id, knowledge_id, "assesses")
            matched: set[str] = set()
            for raw_locus in _as_list(record.get("prerequisite_loci")):
                scene_id = self.scene_by_locator.get((unit_id, str(raw_locus)))
                if scene_id:
                    matched.add(scene_id)
                    self.edge(challenge_id, scene_id, "requires_scene")
                else:
                    self.unresolved_ref(unit_id, challenge_id, raw_locus, "requires_scene")
            for title in _as_list(record.get("prerequisite_scene_titles")):
                candidates = self.scene_by_title.get((unit_id, str(title)), [])
                if len(candidates) == 1 and candidates[0] not in matched:
                    self.edge(challenge_id, candidates[0], "requires_scene")

    def _attach_dependency_counts(self) -> None:
        outgoing: dict[str, list[dict[str, str]]] = defaultdict(list)
        incoming: dict[str, list[dict[str, str]]] = defaultdict(list)
        for edge in self.edges:
            outgoing[edge["from"]].append(edge)
            incoming[edge["to"]].append(edge)
        for entity_id, entity in self.entities.items():
            entity["dependency_counts"] = {
                "outbound": len(outgoing.get(entity_id, [])),
                "inbound": len(incoming.get(entity_id, [])),
            }
            if entity["type"] == "concept":
                entity["coverage"] = {
                    "scenes": sum(1 for edge in incoming.get(entity_id, []) if edge["kind"] == "teaches_concept"),
                    "memory_objects": sum(1 for edge in incoming.get(entity_id, []) if edge["kind"] == "represents"),
                    "questions": sum(
                        1
                        for edge in incoming.get(entity_id, [])
                        if edge["kind"] == "assesses"
                        and self.entities.get(edge["from"], {}).get("type") == "question"
                    ),
                    "challenge_items": sum(
                        1
                        for edge in incoming.get(entity_id, [])
                        if edge["kind"] == "assesses"
                        and self.entities.get(edge["from"], {}).get("type") == "challenge"
                    ),
                    "mixed_sets": sum(1 for edge in incoming.get(entity_id, []) if edge["kind"] == "discriminates"),
                }

    def _snapshot(self, release: dict[str, Any]) -> dict[str, Any]:
        counts: dict[str, int] = defaultdict(int)
        question_counts: dict[str, int] = defaultdict(int)
        for entity in self.entities.values():
            counts[entity["type"]] += 1
            if entity["type"] in {"question", "challenge"}:
                question_counts[str(entity.get("question_type") or "unknown")] += 1
        release_totals = release.get("totals", {}) if isinstance(release, dict) else {}
        actual = {
            "units": counts.get("unit", 0),
            "journeys": counts.get("journey", 0),
            "scenes": counts.get("scene", 0),
            "canonical_records": counts.get("concept", 0),
            "challenge_lab_items": counts.get("challenge", 0),
        }
        expected = {
            "units": len(release.get("units", [])) if isinstance(release, dict) else None,
            "journeys": release_totals.get("guided_journeys"),
            "scenes": release_totals.get("permanent_scenes"),
            "canonical_records": release_totals.get("canonical_records_units_1_8"),
            "challenge_lab_items": release_totals.get("challenge_lab_items"),
        }
        alignment = {
            key: {
                "actual": actual[key],
                "expected": expected[key],
                "matches": expected[key] is None or actual[key] == expected[key],
            }
            for key in actual
        }
        course_entity = self.entities.get(self.course_entity_id, {})
        return {
            "schema": CATALOG_SCHEMA,
            "course_id": self.course_id,
            "course_title": course_entity.get("title", self.course_id),
            "release_status": release.get("release_status"),
            "runtime_version": release.get("runtime_version"),
            "counts": dict(sorted(counts.items())),
            "question_counts": dict(sorted(question_counts.items())),
            "release_alignment": alignment,
            "unresolved_reference_count": len(self.unresolved),
            "unresolved_references": sorted(
                self.unresolved,
                key=lambda item: (
                    item["unit_id"],
                    item["source_id"],
                    item["relation"],
                    item["raw_reference"],
                ),
            ),
            "entities": self.entities,
            "edges": self.edges,
            "aliases": {
                f"{unit_id}|{raw}": mapping
                for (unit_id, raw), mapping in sorted(self.aliases.items())
            },
        }


@lru_cache(maxsize=16)
def catalog(course_id: str = DEFAULT_COURSE_ID) -> dict[str, Any]:
    return CatalogBuilder(_catalog_course_id(course_id)).build()


def clear_catalog_cache() -> None:
    catalog.cache_clear()


def content_health(course_id: str = DEFAULT_COURSE_ID) -> dict[str, Any]:
    snapshot = catalog(_catalog_course_id(course_id))
    problems: list[dict[str, Any]] = []
    for key, record in snapshot["release_alignment"].items():
        if not record["matches"]:
            problems.append(
                {
                    "severity": "error",
                    "code": "release-total-mismatch",
                    "entity_type": key,
                    "message": f"Normalized {key} total {record['actual']} does not match frozen release total {record['expected']}.",
                }
            )
    if snapshot["unresolved_reference_count"]:
        problems.append(
            {
                "severity": "warning",
                "code": "unresolved-references",
                "count": snapshot["unresolved_reference_count"],
                "message": "Some source references could not be linked to a normalized entity.",
            }
        )
    scenes = [entity for entity in snapshot["entities"].values() if entity["type"] == "scene"]
    scenes_without_objects = sum(1 for scene in scenes if not scene.get("object_ids"))
    scenes_without_story = sum(1 for scene in scenes if not scene.get("story_word_count"))
    if scenes_without_objects:
        problems.append(
            {
                "severity": "warning",
                "code": "scenes-without-object-links",
                "count": scenes_without_objects,
                "message": "Some scenes contain no explicit object_ids in the student runtime record.",
            }
        )
    if scenes_without_story:
        problems.append(
            {
                "severity": "warning",
                "code": "scenes-without-story-text",
                "count": scenes_without_story,
                "message": "Some normalized scenes have no story paragraphs available to the catalog.",
            }
        )
    return {
        "error_count": sum(1 for problem in problems if problem["severity"] == "error"),
        "warning_count": sum(1 for problem in problems if problem["severity"] == "warning"),
        "problems": problems,
    }


def catalog_summary(course_id: str = DEFAULT_COURSE_ID) -> dict[str, Any]:
    snapshot = catalog(_catalog_course_id(course_id))
    return {
        "schema": snapshot["schema"],
        "course_id": snapshot["course_id"],
        "course_title": snapshot["course_title"],
        "release_status": snapshot["release_status"],
        "runtime_version": snapshot["runtime_version"],
        "counts": snapshot["counts"],
        "question_counts": snapshot["question_counts"],
        "release_alignment": snapshot["release_alignment"],
        "unresolved_reference_count": snapshot["unresolved_reference_count"],
        "health": content_health(course_id),
    }


def course_map(course_id: str = DEFAULT_COURSE_ID) -> dict[str, Any]:
    snapshot = catalog(_catalog_course_id(course_id))
    entities = snapshot["entities"]
    units = sorted(
        (entity for entity in entities.values() if entity["type"] == "unit"),
        key=lambda entity: (entity.get("number") or 999, entity["id"]),
    )
    result: list[dict[str, Any]] = []
    for unit in units:
        journeys = sorted(
            (
                entity
                for entity in entities.values()
                if entity["type"] == "journey" and entity.get("unit_id") == unit.get("unit_id")
            ),
            key=lambda entity: (entity.get("order") or 0, entity["id"]),
        )
        normalized_journeys: list[dict[str, Any]] = []
        for journey in journeys:
            scenes = sorted(
                (
                    entity
                    for entity in entities.values()
                    if entity["type"] == "scene" and entity.get("journey_id") == journey["id"]
                ),
                key=lambda entity: (entity.get("scene_index") or 0, entity["id"]),
            )
            normalized_journeys.append(
                {
                    "id": journey["id"],
                    "palace_id": journey.get("palace_id"),
                    "title": journey.get("title"),
                    "palace_name": journey.get("palace_name"),
                    "scene_count": len(scenes),
                    "checkpoint_count": sum(1 for scene in scenes if scene.get("checkpoint")),
                    "scenes": [
                        {
                            "id": scene["id"],
                            "scene_index": scene.get("scene_index"),
                            "title": scene.get("title"),
                            "locus": scene.get("locus"),
                            "locus_id": scene.get("locus_id"),
                            "story_word_count": scene.get("story_word_count"),
                            "object_count": len(scene.get("object_ids", [])),
                            "character_count": len(scene.get("character_names", [])),
                            "checkpoint": bool(scene.get("checkpoint")),
                        }
                        for scene in scenes
                    ],
                }
            )
        result.append(
            {
                "id": unit["id"],
                "unit_id": unit.get("unit_id"),
                "number": unit.get("number"),
                "title": unit.get("title"),
                "journey_count": len(normalized_journeys),
                "scene_count": sum(item["scene_count"] for item in normalized_journeys),
                "journeys": normalized_journeys,
            }
        )
    return {"schema": CATALOG_SCHEMA, "course_id": snapshot["course_id"], "course_title": snapshot["course_title"], "units": result}


def get_entity(entity_id: str, course_id: str = DEFAULT_COURSE_ID) -> dict[str, Any] | None:
    return catalog(_catalog_course_id(course_id))["entities"].get(entity_id)


def resolve_reference(unit_id: str, raw_reference: str, course_id: str = DEFAULT_COURSE_ID) -> dict[str, Any]:
    snapshot = catalog(_catalog_course_id(course_id))
    mapping = snapshot["aliases"].get(f"{unit_id}|{raw_reference}", {})
    return {
        "course_id": snapshot["course_id"],
        "unit_id": unit_id,
        "raw_reference": raw_reference,
        "matches": [
            snapshot["entities"][entity_id]
            for entity_id in mapping.values()
            if entity_id in snapshot["entities"]
        ],
    }


def list_entities(
    *,
    course_id: str = DEFAULT_COURSE_ID,
    entity_type: str | None = None,
    unit_id: str | None = None,
    offset: int = 0,
    limit: int = 100,
) -> dict[str, Any]:
    snapshot = catalog(_catalog_course_id(course_id))
    safe_offset = max(0, int(offset))
    safe_limit = max(1, min(int(limit), 500))
    items = [
        entity
        for entity in snapshot["entities"].values()
        if (entity_type is None or entity["type"] == entity_type)
        and (unit_id is None or entity.get("unit_id") == unit_id)
    ]
    items.sort(
        key=lambda entity: (
            entity.get("unit_id") or "",
            entity["type"],
            str(entity.get("title") or "").casefold(),
            entity["id"],
        )
    )
    return {
        "course_id": snapshot["course_id"],
        "total": len(items),
        "offset": safe_offset,
        "limit": safe_limit,
        "items": items[safe_offset : safe_offset + safe_limit],
    }


def search_entities(
    query: str,
    *,
    course_id: str = DEFAULT_COURSE_ID,
    unit_id: str | None = None,
    entity_type: str | None = None,
    limit: int = 50,
) -> dict[str, Any]:
    q = query.strip().casefold()
    safe_limit = max(1, min(int(limit), 100))
    if not q:
        return {"query": query, "items": []}
    matches: list[tuple[int, str, dict[str, Any]]] = []
    snapshot = catalog(_catalog_course_id(course_id))
    for entity in snapshot["entities"].values():
        if unit_id and entity.get("unit_id") != unit_id:
            continue
        if entity_type and entity.get("type") != entity_type:
            continue
        haystack_parts = [
            entity.get("title"),
            entity.get("canonical_term"),
            entity.get("canonical_definition"),
            entity.get("palace_id"),
            entity.get("locus"),
            entity.get("locus_id"),
            entity.get("memory_object_id"),
            entity.get("knowledge_id"),
            entity.get("prompt"),
        ]
        haystack = " ".join(
            str(value) for value in haystack_parts if value not in (None, "")
        ).casefold()
        if q not in haystack:
            continue
        title = str(entity.get("title") or "")
        score = 0
        if title.casefold() == q:
            score += 100
        elif title.casefold().startswith(q):
            score += 50
        if str(entity.get("canonical_term") or "").casefold() == q:
            score += 90
        matches.append((score, title.casefold(), entity))
    matches.sort(key=lambda item: (-item[0], item[1], item[2]["id"]))
    return {"course_id": snapshot["course_id"], "query": query, "items": [item[2] for item in matches[:safe_limit]]}


def dependency_report(
    entity_id: str,
    *,
    course_id: str = DEFAULT_COURSE_ID,
    depth: int = 2,
    limit: int = 500,
) -> dict[str, Any] | None:
    snapshot = catalog(_catalog_course_id(course_id))
    entities = snapshot["entities"]
    if entity_id not in entities:
        return None
    max_depth = max(1, min(int(depth), 4))
    safe_limit = max(1, min(int(limit), 1000))
    outgoing: dict[str, list[dict[str, str]]] = defaultdict(list)
    incoming: dict[str, list[dict[str, str]]] = defaultdict(list)
    for edge in snapshot["edges"]:
        outgoing[edge["from"]].append(edge)
        incoming[edge["to"]].append(edge)
    direct_outbound = [
        {"edge": edge, "entity": entities[edge["to"]]}
        for edge in sorted(outgoing.get(entity_id, []), key=lambda item: (item["kind"], item["to"]))
    ]
    direct_inbound = [
        {"edge": edge, "entity": entities[edge["from"]]}
        for edge in sorted(incoming.get(entity_id, []), key=lambda item: (item["kind"], item["from"]))
    ]
    queue: deque[tuple[str, int, list[str]]] = deque([(entity_id, 0, [])])
    visited: dict[str, int] = {entity_id: 0}
    related: list[dict[str, Any]] = []
    while queue and len(related) < safe_limit:
        current, current_depth, path = queue.popleft()
        if current_depth >= max_depth:
            continue
        neighbors = [(edge, edge["to"], "outbound") for edge in outgoing.get(current, [])]
        neighbors.extend((edge, edge["from"], "inbound") for edge in incoming.get(current, []))
        for edge, neighbor, direction in neighbors:
            next_depth = current_depth + 1
            if visited.get(neighbor, 99) <= next_depth:
                continue
            visited[neighbor] = next_depth
            next_path = path + [f"{direction}:{edge['kind']}"]
            related.append(
                {
                    "distance": next_depth,
                    "path": next_path,
                    "entity": entities[neighbor],
                }
            )
            queue.append((neighbor, next_depth, next_path))
            if len(related) >= safe_limit:
                break
    by_type: dict[str, int] = defaultdict(int)
    for item in related:
        by_type[item["entity"]["type"]] += 1
    return {
        "course_id": snapshot["course_id"],
        "entity": entities[entity_id],
        "direct_outbound": direct_outbound,
        "direct_inbound": direct_inbound,
        "related": related,
        "related_counts_by_type": dict(sorted(by_type.items())),
        "depth": max_depth,
        "truncated": len(related) >= safe_limit,
    }
