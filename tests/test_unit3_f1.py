import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/"content/ap-biology/unit-3"
def load(rel): return json.loads((U3/rel).read_text())
def test_unit3_f1_counts_and_lock():
 c=load("source/canonical-unit3-f1.json")
 assert c["qa"]["ppt_pages_ingested"]==136
 assert c["qa"]["ced_atoms"]==54
 assert c["qa"]["teacher_test_items_crosswalked"]==24
 assert c["qa"]["canonical_records"]==len(c["canonical_catalog"])
 assert c["qa"]["review_flags_resolved"]==c["qa"]["review_flags"]
def test_unit3_f1_current_topics():
 c=load("source/canonical-unit3-f1.json")
 assert {a["topic"] for a in c["ced_current_atoms"]}=={"3.1","3.2","3.3","3.4","3.5"}
def test_unit3_f1_assessment_revision_flags():
 c=load("source/canonical-unit3-f1.json")
 bad={i["item"] for i in c["assessment_crosswalk"] if i["status"]=="NEEDS_REVISION_BEFORE_REUSE"}
 assert bad=={2,16,23}
def test_unit3_f1_was_not_student_released():
 manifest=load("f1-release-manifest.json")
 assert manifest["student_release"] is False
 assert manifest["journeys"]==0 and manifest["scenes"]==0 and manifest["memory_objects"]==0
def test_unit3_f1_had_no_premature_runtime_content():
 manifest=load("f1-release-manifest.json")
 assert manifest["journeys"]==0 and manifest["scenes"]==0 and manifest["memory_objects"]==0
 assert manifest["student_release"] is False
 assert not (U3/"memory-objects.json").exists()


def test_unit3_every_assessment_item_has_destination():
    c=load("source/canonical-unit3-f1.json")
    assert all(x["mapped_knowledge_ids"] for x in c["assessment_crosswalk"])

def test_unit3_scope_counts_are_locked():
    c=load("source/canonical-unit3-f1.json")
    assert c["qa"]["scope_counts"]=={
        "AP_REQUIRED":54,
        "TEACHER_REQUIRED_ENRICHMENT":117,
        "SCOPE_GUARD":4,
        "PRACTICE_ONLY":11,
    }
