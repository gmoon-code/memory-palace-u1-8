from pathlib import Path
import hashlib, json, sys
ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/"content/ap-biology/unit-3"
def sha(p):
 h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
def main():
 cat=json.loads((U3/"source/canonical-unit3-f1.json").read_text())
 cov=json.loads((U3/"source/coverage-manifest-f1.json").read_text())
 manifest=json.loads((U3/"f1-release-manifest.json").read_text())
 lock=json.loads((U3/"content-lock-f1.json").read_text())
 assert cat["qa"]["ppt_pages_ingested"]==136
 assert len(cat["ppt_raw_slides"])==136
 assert len(cat["ced_current_atoms"])==54
 assert len(cat["assessment_crosswalk"])==24
 assert cat["qa"]["review_flags"]==cat["qa"]["review_flags_resolved"]
 assert cat["qa"]["review_flags"]>=25
 assert len(cat["canonical_catalog"])==cat["qa"]["canonical_records"]
 assert cov["ppt_coverage"]["unmapped"]==0
 assert cov["assessment_coverage"]["crosswalked_items"]==24
 assert set(cov["assessment_coverage"]["items_needing_revision"])=={2,16,23}
 ids=[r["knowledge_id"] for r in cat["canonical_catalog"]]
 assert ids==[f"U3-K-{i:03d}" for i in range(1,len(ids)+1)]
 assert all(r["canonical_lock"].startswith("LOCKED") for r in cat["canonical_catalog"])
 assert {r["topic"] for r in cat["canonical_catalog"]}=={"3.1","3.2","3.3","3.4","3.5"}
 assert manifest["student_release"] is False and manifest["journeys"]==0 and manifest["scenes"]==0
 for item in lock["protected_files"]:
  p=U3/item["path"]; assert p.exists() and sha(p)==item["sha256"]
 print(f"Unit 3 F1 QA PASS: {len(cat['canonical_catalog'])} canonical records, {len(cat['review_flags'])} resolved flags, 136/136 slides, 24/24 test items")
if __name__=="__main__": main()
