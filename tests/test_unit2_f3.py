import json, hashlib
from pathlib import Path
from collections import Counter
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
client=TestClient(app)
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_f3_scene_brief_counts_and_lossless_coverage():
    src=read(U2/'source/canonical-unit2-f1.json')
    d=read(U2/'briefs/scene-briefs-f3.json')
    assert d['counts']['scene_briefs']==49
    assert d['counts']['palace_managed_records']==133
    assert d['counts']['term_introductions']==133
    assigned=[kid for b in d['scene_briefs'] for kid in b['knowledge_ids']]
    palace={r['knowledge_id'] for r in src['canonical_catalog'] if r['retrieval_demand']!='APPLIED_TRANSFER'}
    assert len(assigned)==len(set(assigned))==133
    assert set(assigned)==palace

def test_f3_briefs_have_location_cast_action_visual_and_guardrails():
    d=read(U2/'briefs/scene-briefs-f3.json')
    for b in d['scene_briefs']:
        assert len(b['orientation_sentence'])>=100
        assert set(b['spatial_layout'])=={'left','center','right'}
        assert len(b['stable_cast'])>=2
        assert len(b['science_bearing_action']['during'])>=2
        assert b['visual_spec']['conventional_scientific_visual_required'] is True
        assert b['visual_spec']['must_show']
        assert b['misconception_guards']
        assert b['carry_forward']
        assert b['brief_status']=='LOCKED_F3_SCENE_BRIEF'

def test_f3_keeps_first_exposure_recall_light():
    d=read(U2/'briefs/scene-briefs-f3.json')
    enabled=[b for b in d['scene_briefs'] if b['quick_recall'].get('enabled')]
    assert len(enabled)==17
    counts=Counter(b['journey_id'] for b in enabled)
    assert counts['U2-J1']==4
    assert all(n<=3 for jid,n in counts.items() if jid!='U2-J1')

def test_f3_journey_briefs_use_one_stable_unit_guide_and_continuity():
    d=read(U2/'briefs/journey-briefs-f3.json')
    assert d['journey_count']==7
    assert d['unit_guide']['name']=='Dr. Nia Park'
    for j in d['journeys']:
        assert j['unit_guide']['name']=='Dr. Nia Park'
        assert j['premise'] and j['mission'] and j['stakes'] and j['continuity_object']
        assert j['opening_image'] and j['ending_payoff']
        assert j['status']=='JOURNEY_BRIEF_LOCKED_F3_NO_POLISHED_STORY_PROSE'

def test_f3_content_lock_hashes():
    lock=read(U2/'content-lock-f3.json')
    assert lock['lock_status']=='LOCKED_F3'
    for rel,meta in lock['files'].items():
        p=ROOT/rel
        assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']

def test_f3_api_preserves_briefs_after_final_release():
    d=client.get('/api/units/unit-2').json()
    assert d['student_release'] is True
    assert d['scene_briefs']==49
    s=client.get('/api/units/unit-2/scene-briefs')
    assert s.status_code==200 and s.json()['counts']['scene_briefs']==49
    j=client.get('/api/units/unit-2/journey-briefs')
    assert j.status_code==200 and j.json()['journey_count']==7
    assert client.get('/api/units/unit-2/journeys').status_code==200
