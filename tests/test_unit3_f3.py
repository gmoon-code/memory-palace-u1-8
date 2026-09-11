import json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content/ap-biology/unit-3'
def load(rel): return json.loads((U3/rel).read_text())
def test_unit3_f3_counts():
    s=load('briefs/scene-briefs-f3.json'); j=load('briefs/journey-briefs-f3.json')
    assert s['counts']=={'journeys':7,'scene_briefs':54,'palace_managed_records':171,'term_introductions':171,'optional_first_exposure_recalls':18}
    assert len(s['scene_briefs'])==54 and j['journey_count']==7
def test_unit3_f3_zero_loss_and_exact_science():
    src=load('source/canonical-unit3-f1.json'); rec={r['knowledge_id']:r for r in src['canonical_catalog']}
    arch=load('architecture/palace-architecture-f2.json'); s=load('briefs/scene-briefs-f3.json')
    expected={k for l in arch['loci'] for k in l['knowledge_ids']}
    actual=[k for b in s['scene_briefs'] for k in b['knowledge_ids']]
    assert len(actual)==len(set(actual))==171 and set(actual)==expected
    for b in s['scene_briefs']:
        for t in b['term_introductions']:
            assert t['canonical_science']==rec[t['knowledge_id']]['canonical_verified_statement']
def test_unit3_f3_not_student_released():
    s=load('status-f3.json')
    assert s['student_release'] is False and s['journey_count']==0 and s['scene_count']==0
    assert s['status']=='SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED'
def test_unit3_f3_lock_hashes():
    lock=load('content-lock-f3.json')
    for rel,meta in lock['files'].items():
        p=ROOT/rel
        assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']
