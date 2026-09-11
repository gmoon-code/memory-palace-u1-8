from functools import lru_cache
import json
from pathlib import Path
from .settings import APBIO_DIR, UNIT1_DIR, UNIT2_DIR, UNIT3_DIR, UNIT4_DIR, UNIT5_DIR, UNIT6_DIR, UNIT7_DIR, UNIT8_DIR

def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

@lru_cache(maxsize=1)
def course(): return _read_json(APBIO_DIR / "course.json")
@lru_cache(maxsize=1)
def canonical(): return _read_json(UNIT1_DIR / "source" / "canonical-unit1.json")
@lru_cache(maxsize=1)
def memory_objects(): return _read_json(UNIT1_DIR / "memory-objects.json")
@lru_cache(maxsize=1)
def content_lock(): return _read_json(UNIT1_DIR / "content-lock.json")
@lru_cache(maxsize=1)
def unit1_registry(): return _read_json(UNIT1_DIR / "journeys.json")
@lru_cache(maxsize=1)
def application_lab(): return _read_json(UNIT1_DIR / "application-lab.json")

@lru_cache(maxsize=1)
def unit2_status():
    for name in ("status-f5.json","status-f4g.json","status-f4f.json","status-f4e.json","status-f4d.json","status-f4c.json","status-f4b.json","status-f4a.json","status-f3.json","status.json"):
        path=UNIT2_DIR / name
        if path.exists(): return _read_json(path)
    return {}
@lru_cache(maxsize=1)
def unit2_source_lock(): return _read_json(UNIT2_DIR / "source" / "canonical-unit2-f1.json")
@lru_cache(maxsize=1)
def unit2_architecture(): return _read_json(UNIT2_DIR / "architecture" / "palace-architecture-f2.json")
@lru_cache(maxsize=1)
def unit2_scene_briefs(): return _read_json(UNIT2_DIR / "briefs" / "scene-briefs-f3.json")
@lru_cache(maxsize=1)
def unit2_journey_briefs(): return _read_json(UNIT2_DIR / "briefs" / "journey-briefs-f3.json")
@lru_cache(maxsize=1)
def unit2_application_lab(): return _read_json(UNIT2_DIR / "application-lab.json")
@lru_cache(maxsize=1)
def unit2_review_manifest(): return _read_json(UNIT2_DIR / "review-manifest-f5.json")
@lru_cache(maxsize=1)
def unit2_mixed_discrimination(): return _read_json(UNIT2_DIR / "mixed-discrimination-f5.json")
@lru_cache(maxsize=1)
def unit2_finalization(): return _read_json(UNIT2_DIR / "finalization-f5.json")

@lru_cache(maxsize=1)
def unit3_status(): return _read_json(UNIT3_DIR / "status.json")
@lru_cache(maxsize=1)
def unit3_source_lock(): return _read_json(UNIT3_DIR / "source" / "canonical-unit3-f1.json")
@lru_cache(maxsize=1)
def unit3_architecture(): return _read_json(UNIT3_DIR / "architecture" / "palace-architecture-f2.json")
@lru_cache(maxsize=1)
def unit3_scene_briefs(): return _read_json(UNIT3_DIR / "briefs" / "scene-briefs-f3.json")
@lru_cache(maxsize=1)
def unit3_journey_briefs(): return _read_json(UNIT3_DIR / "briefs" / "journey-briefs-f3.json")

@lru_cache(maxsize=1)
def unit3_application_lab(): return _read_json(UNIT3_DIR / "application-lab.json")
@lru_cache(maxsize=1)
def unit3_review_manifest(): return _read_json(UNIT3_DIR / "review-manifest-f5.json")
@lru_cache(maxsize=1)
def unit3_mixed_discrimination(): return _read_json(UNIT3_DIR / "mixed-discrimination-f5.json")
@lru_cache(maxsize=1)
def unit3_scope_guards(): return _read_json(UNIT3_DIR / "scope-guards-f5.json")
@lru_cache(maxsize=1)
def unit3_finalization(): return _read_json(UNIT3_DIR / "finalization-f5.json")

@lru_cache(maxsize=1)
def unit4_status(): return _read_json(UNIT4_DIR / "status.json")
@lru_cache(maxsize=1)
def unit4_source_lock(): return _read_json(UNIT4_DIR / "source" / "canonical-unit4-f1.json")
@lru_cache(maxsize=1)
def unit4_architecture(): return _read_json(UNIT4_DIR / "architecture" / "palace-architecture-f2.json")
@lru_cache(maxsize=1)
def unit4_scene_briefs(): return _read_json(UNIT4_DIR / "briefs" / "scene-briefs-f3.json")
@lru_cache(maxsize=1)
def unit4_journey_briefs(): return _read_json(UNIT4_DIR / "briefs" / "journey-briefs-f3.json")
@lru_cache(maxsize=1)
def unit4_memory_objects(): return _read_json(UNIT4_DIR / "memory-objects-f5.json")
@lru_cache(maxsize=1)
def unit4_application_lab(): return _read_json(UNIT4_DIR / "application-lab.json")
@lru_cache(maxsize=1)
def unit4_review_manifest(): return _read_json(UNIT4_DIR / "review-manifest-f5.json")
@lru_cache(maxsize=1)
def unit4_mixed_discrimination(): return _read_json(UNIT4_DIR / "mixed-discrimination-f5.json")
@lru_cache(maxsize=1)
def unit4_scope_guards(): return _read_json(UNIT4_DIR / "scope-guards-f5.json")
@lru_cache(maxsize=1)
def unit4_finalization(): return _read_json(UNIT4_DIR / "finalization-f5.json")

@lru_cache(maxsize=1)
def unit5_status(): return _read_json(UNIT5_DIR / "status.json")
@lru_cache(maxsize=1)
def unit5_source_lock(): return _read_json(UNIT5_DIR / "source" / "canonical-unit5-f1.json")
@lru_cache(maxsize=1)
def unit5_architecture(): return _read_json(UNIT5_DIR / "architecture" / "palace-architecture-f2.json")
@lru_cache(maxsize=1)
def unit5_scene_briefs(): return _read_json(UNIT5_DIR / "briefs" / "scene-briefs-f3.json")
@lru_cache(maxsize=1)
def unit5_journey_briefs(): return _read_json(UNIT5_DIR / "briefs" / "journey-briefs-f3.json")
@lru_cache(maxsize=1)
def unit5_memory_objects(): return _read_json(UNIT5_DIR / "memory-objects-f5.json")
@lru_cache(maxsize=1)
def unit5_application_lab(): return _read_json(UNIT5_DIR / "application-lab.json")
@lru_cache(maxsize=1)
def unit5_review_manifest(): return _read_json(UNIT5_DIR / "review-manifest-f5.json")
@lru_cache(maxsize=1)
def unit5_mixed_discrimination(): return _read_json(UNIT5_DIR / "mixed-discrimination-f5.json")
@lru_cache(maxsize=1)
def unit5_scope_guards(): return _read_json(UNIT5_DIR / "scope-guards-f5.json")
@lru_cache(maxsize=1)
def unit5_finalization(): return _read_json(UNIT5_DIR / "finalization-f5.json")

@lru_cache(maxsize=1)
def unit6_status(): return _read_json(UNIT6_DIR / "status.json")
@lru_cache(maxsize=1)
def unit6_source_lock(): return _read_json(UNIT6_DIR / "source" / "canonical-unit6-f1.json")
@lru_cache(maxsize=1)
def unit6_architecture(): return _read_json(UNIT6_DIR / "architecture" / "palace-architecture-f2.json")
@lru_cache(maxsize=1)
def unit6_scene_briefs(): return _read_json(UNIT6_DIR / "briefs" / "scene-briefs-f3.json")
@lru_cache(maxsize=1)
def unit6_journey_briefs(): return _read_json(UNIT6_DIR / "briefs" / "journey-briefs-f3.json")
@lru_cache(maxsize=1)
def unit6_memory_objects(): return _read_json(UNIT6_DIR / "memory-objects-f5.json")
@lru_cache(maxsize=1)
def unit6_application_lab(): return _read_json(UNIT6_DIR / "application-lab.json")
@lru_cache(maxsize=1)
def unit6_review_manifest(): return _read_json(UNIT6_DIR / "review-manifest-f5.json")
@lru_cache(maxsize=1)
def unit6_mixed_discrimination(): return _read_json(UNIT6_DIR / "mixed-discrimination-f5.json")
@lru_cache(maxsize=1)
def unit6_scope_guards(): return _read_json(UNIT6_DIR / "scope-guards-f5.json")
@lru_cache(maxsize=1)
def unit6_finalization(): return _read_json(UNIT6_DIR / "finalization-f5.json")

@lru_cache(maxsize=1)
def unit7_status(): return _read_json(UNIT7_DIR / "status.json")
@lru_cache(maxsize=1)
def unit7_source_lock(): return _read_json(UNIT7_DIR / "source" / "canonical-unit7-f1.json")
@lru_cache(maxsize=1)
def unit7_architecture(): return _read_json(UNIT7_DIR / "architecture" / "palace-architecture-f2.json")
@lru_cache(maxsize=1)
def unit7_scene_briefs(): return _read_json(UNIT7_DIR / "briefs" / "scene-briefs-f3.json")
@lru_cache(maxsize=1)
def unit7_journey_briefs(): return _read_json(UNIT7_DIR / "briefs" / "journey-briefs-f3.json")
@lru_cache(maxsize=1)
def unit7_memory_objects(): return _read_json(UNIT7_DIR / "memory-objects-f5.json")
@lru_cache(maxsize=1)
def unit7_application_lab(): return _read_json(UNIT7_DIR / "application-lab.json")
@lru_cache(maxsize=1)
def unit7_review_manifest(): return _read_json(UNIT7_DIR / "review-manifest-f5.json")
@lru_cache(maxsize=1)
def unit7_mixed_discrimination(): return _read_json(UNIT7_DIR / "mixed-discrimination-f5.json")
@lru_cache(maxsize=1)
def unit7_scope_guards(): return _read_json(UNIT7_DIR / "scope-guards-f5.json")
@lru_cache(maxsize=1)
def unit7_finalization(): return _read_json(UNIT7_DIR / "finalization-f5.json")

@lru_cache(maxsize=1)
def unit8_status(): return _read_json(UNIT8_DIR / "status.json")
@lru_cache(maxsize=1)
def unit8_canonical_catalog(): return _read_json(UNIT8_DIR / "canonical-catalog.json")
@lru_cache(maxsize=1)
def unit8_architecture(): return _read_json(UNIT8_DIR / "architecture" / "palace-architecture-f2.json")
@lru_cache(maxsize=1)
def unit8_scene_briefs(): return _read_json(UNIT8_DIR / "briefs" / "scene-briefs-f3.json")
@lru_cache(maxsize=1)
def unit8_journey_briefs(): return _read_json(UNIT8_DIR / "briefs" / "journey-briefs-f3.json")
@lru_cache(maxsize=1)
def unit8_memory_objects(): return _read_json(UNIT8_DIR / "memory-objects-f5.json")
@lru_cache(maxsize=1)
def unit8_application_lab(): return _read_json(UNIT8_DIR / "application-lab.json")
@lru_cache(maxsize=1)
def unit8_review_manifest(): return _read_json(UNIT8_DIR / "review-manifest-f5.json")
@lru_cache(maxsize=1)
def unit8_mixed_discrimination(): return _read_json(UNIT8_DIR / "mixed-discrimination-f5.json")
@lru_cache(maxsize=1)
def unit8_scope_guards(): return _read_json(UNIT8_DIR / "scope-guards-f5.json")
@lru_cache(maxsize=1)
def unit8_finalization(): return _read_json(UNIT8_DIR / "finalization-f5.json")

def unit_by_id(unit_id: str):
    return next((u for u in course()["units"] if u["unit_id"] == unit_id), None)

def journey_registry(unit_id: str):
    if unit_id == "unit-1": return unit1_registry()["guided_journeys"]
    if unit_id == "unit-2":
        path=UNIT2_DIR / "journeys-f5.json"
        if not path.exists(): path=UNIT2_DIR / "journeys-f4g.json"
        if not path.exists(): path=UNIT2_DIR / "journeys-f4f.json"
        if not path.exists(): path=UNIT2_DIR / "journeys-f4e.json"
        if not path.exists(): path=UNIT2_DIR / "journeys-f4d.json"
        if not path.exists(): path=UNIT2_DIR / "journeys-f4c.json"
        if not path.exists(): path=UNIT2_DIR / "journeys-f4b.json"
        if not path.exists(): path=UNIT2_DIR / "journeys-f4a.json"
        return _read_json(path)["guided_journeys"] if path.exists() else []
    if unit_id == "unit-3":
        path=UNIT3_DIR / "journeys-f5.json"
        if not path.exists(): path=UNIT3_DIR / "journeys-f4g.json"
        if not path.exists(): path=UNIT3_DIR / "journeys-f4f.json"
        if not path.exists(): path=UNIT3_DIR / "journeys-f4e.json"
        if not path.exists(): path=UNIT3_DIR / "journeys-f4d.json"
        if not path.exists(): path=UNIT3_DIR / "journeys-f4c.json"
        if not path.exists(): path=UNIT3_DIR / "journeys-f4b.json"
        if not path.exists(): path=UNIT3_DIR / "journeys-f4a.json"
        return _read_json(path)["guided_journeys"] if path.exists() else []
    if unit_id == "unit-4":
        path=UNIT4_DIR / "journeys-f5.json"
        if not path.exists(): path=UNIT4_DIR / "journeys-f4g.json"
        if not path.exists(): path=UNIT4_DIR / "journeys-f4f.json"
        if not path.exists(): path=UNIT4_DIR / "journeys-f4e.json"
        if not path.exists(): path=UNIT4_DIR / "journeys-f4d.json"
        if not path.exists(): path=UNIT4_DIR / "journeys-f4c.json"
        if not path.exists(): path=UNIT4_DIR / "journeys-f4b.json"
        if not path.exists(): path=UNIT4_DIR / "journeys-f4a.json"
        return _read_json(path)["guided_journeys"] if path.exists() else []
    if unit_id == "unit-5":
        path=UNIT5_DIR / "journeys-f5.json"
        if not path.exists(): path=UNIT5_DIR / "journeys-f4h.json"
        if not path.exists(): path=UNIT5_DIR / "journeys-f4g.json"
        if not path.exists(): path=UNIT5_DIR / "journeys-f4f.json"
        if not path.exists(): path=UNIT5_DIR / "journeys-f4e.json"
        if not path.exists(): path=UNIT5_DIR / "journeys-f4d.json"
        if not path.exists(): path=UNIT5_DIR / "journeys-f4c.json"
        if not path.exists(): path=UNIT5_DIR / "journeys-f4b.json"
        if not path.exists(): path=UNIT5_DIR / "journeys-f4a.json"
        return _read_json(path)["guided_journeys"] if path.exists() else []
    if unit_id == "unit-6":
        path=UNIT6_DIR / "journeys-f5.json"
        return _read_json(path)["guided_journeys"] if path.exists() and unit6_status().get("student_release") is True else []
    if unit_id == "unit-7":
        path=UNIT7_DIR / "journeys-f5.json"
        return _read_json(path)["guided_journeys"] if path.exists() and unit7_status().get("student_release") is True else []
    if unit_id == "unit-8":
        path=UNIT8_DIR / "journeys-f5.json"
        return _read_json(path)["guided_journeys"] if path.exists() and unit8_status().get("student_release") is True else []
    return []

def journey_by_id(unit_id: str, palace_id: str):
    if unit_id == "unit-1": path=UNIT1_DIR / "journeys" / f"{palace_id}.json"
    elif unit_id == "unit-2": path=UNIT2_DIR / "journeys" / f"{palace_id}.json"
    elif unit_id == "unit-3": path=UNIT3_DIR / "journeys" / f"{palace_id}.json"
    elif unit_id == "unit-4": path=UNIT4_DIR / "journeys" / f"{palace_id}.json"
    elif unit_id == "unit-5": path=UNIT5_DIR / "journeys" / f"{palace_id}.json"
    elif unit_id == "unit-6":
        if unit6_status().get("student_release") is not True: return None
        path=UNIT6_DIR / "journeys" / f"{palace_id}.json"
    elif unit_id == "unit-7":
        if unit7_status().get("student_release") is not True: return None
        path=UNIT7_DIR / "journeys" / f"{palace_id}.json"
    elif unit_id == "unit-8":
        if unit8_status().get("student_release") is not True: return None
        path=UNIT8_DIR / "journeys" / f"{palace_id}.json"
    else: return None
    return _read_json(path) if path.exists() else None

def object_index(unit_id="unit-1"):
    if unit_id=="unit-1": return {o["memory_object_id"]:o for o in memory_objects()["memory_objects"]}
    if unit_id=="unit-2":
        records=unit2_source_lock()["canonical_catalog"]
        return {r["knowledge_id"]:{"memory_object_id":r["knowledge_id"],"canonical_term":r["canonical_label"],"canonical_definition":r["canonical_verified_statement"],"exact_name_recall":r.get("exact_name_recall",False),"source_reference":r.get("source_reference",""),"canonical_lock":r.get("canonical_lock","")} for r in records}
    if unit_id=="unit-3":
        records=unit3_source_lock()["canonical_catalog"]
        return {r["knowledge_id"]:{"memory_object_id":r["knowledge_id"],"canonical_term":r["canonical_label"],"canonical_definition":r["canonical_verified_statement"],"exact_name_recall":r.get("exact_name_recall",False),"source_reference":r.get("source_reference",""),"canonical_lock":r.get("canonical_lock","")} for r in records}
    if unit_id=="unit-4":
        path=UNIT4_DIR / "memory-objects-f5.json"
        if path.exists(): return {o["memory_object_id"]:o for o in unit4_memory_objects()["memory_objects"]}
        records=unit4_source_lock()["canonical_catalog"]
        return {r["knowledge_id"]:{"memory_object_id":r["knowledge_id"],"canonical_term":r["canonical_label"],"canonical_definition":r["canonical_verified_statement"],"exact_name_recall":r.get("exact_name_recall",False),"source_reference":r.get("source_reference",""),"canonical_lock":r.get("canonical_lock","")} for r in records}
    if unit_id=="unit-5":
        path=UNIT5_DIR / "memory-objects-f5.json"
        if path.exists(): return {o["memory_object_id"]:o for o in unit5_memory_objects()["memory_objects"]}
        records=unit5_source_lock()["canonical_catalog"]
        return {r["knowledge_id"]:{"memory_object_id":r["knowledge_id"],"canonical_term":r["canonical_label"],"canonical_definition":r["canonical_verified_statement"],"exact_name_recall":r.get("exact_name_recall",False),"source_reference":r.get("source_reference",""),"canonical_lock":r.get("canonical_lock","")} for r in records}
    if unit_id=="unit-6":
        path=UNIT6_DIR / "memory-objects-f5.json"
        if path.exists() and unit6_status().get("student_release") is True: return {o["memory_object_id"]:o for o in unit6_memory_objects()["memory_objects"]}
        records=unit6_source_lock()["canonical_catalog"]
        return {r["knowledge_id"]:{"memory_object_id":r["knowledge_id"],"canonical_term":r["canonical_label"],"canonical_definition":r["canonical_verified_statement"],"source_reference":r.get("source_reference",""),"canonical_lock":r.get("canonical_lock","")} for r in records}
    if unit_id=="unit-7":
        path=UNIT7_DIR / "memory-objects-f5.json"
        if path.exists() and unit7_status().get("student_release") is True: return {o["memory_object_id"]:o for o in unit7_memory_objects()["memory_objects"]}
        records=unit7_source_lock()["canonical_catalog"]
        return {r["knowledge_id"]:{"memory_object_id":r["knowledge_id"],"canonical_term":r["canonical_label"],"canonical_definition":r["canonical_verified_statement"],"source_reference":r.get("source_reference",""),"canonical_lock":r.get("canonical_lock","")} for r in records}
    if unit_id=="unit-8":
        path=UNIT8_DIR / "memory-objects-f5.json"
        if path.exists() and unit8_status().get("student_release") is True: return {o["memory_object_id"]:o for o in unit8_memory_objects()["memory_objects"]}
        records=unit8_canonical_catalog()
        return {r["Knowledge ID"]:{"memory_object_id":r["Knowledge ID"],"canonical_term":r["Canonical Label"],"canonical_definition":r["Canonical Verified Statement"],"source_reference":r.get("Source Reference",""),"canonical_lock":r.get("Canonical Lock","")} for r in records}
    return {}

def unit_summary(unit_id: str):
    unit=unit_by_id(unit_id)
    if not unit:return None
    out=dict(unit)
    if unit_id=="unit-1":
        out.update({"canonical_records":len(canonical()["canonical_records"]),"memory_objects":memory_objects()["count"],"journeys":unit1_registry()["journey_count"],"permanent_loci":unit1_registry()["scene_count"],"checkpoint_count":unit1_registry()["checkpoint_count"],"application_challenges":application_lab()["challenge_count"],"practice_only_runtime_objects":application_lab()["practice_only_runtime_count"]})
    elif unit_id=="unit-2":
        out.update(unit2_status())
    elif unit_id=="unit-3":
        out.update(unit3_status())
    elif unit_id=="unit-4":
        out.update(unit4_status())
    elif unit_id=="unit-5":
        out.update(unit5_status())
    elif unit_id=="unit-6":
        out.update(unit6_status())
    elif unit_id=="unit-7":
        out.update(unit7_status())
    elif unit_id=="unit-8":
        out.update(unit8_status())
    return out
