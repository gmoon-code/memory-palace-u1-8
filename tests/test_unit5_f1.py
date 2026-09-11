import hashlib,json
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U5=ROOT/'content/ap-biology/unit-5'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit5_f1_accounting_and_scope_partition():
    d=read(U5/'source/canonical-unit5-f1.json')
    assert (len(d['ppt_raw_slides']),len(d['ced_current_atoms']),len(d['canonical_catalog']),len(d['review_flags']),len(d['assessment_semantic_crosswalk']))==(112,34,152,37,10)
    counts={}
    for r in d['canonical_catalog']: counts[r['scope_class']]=counts.get(r['scope_class'],0)+1
    assert counts=={'AP_REQUIRED':34,'TEACHER_REQUIRED_ENRICHMENT':97,'PRACTICE_ONLY':16,'SCOPE_GUARD':5}

def test_unit5_f1_all_slides_and_current_topics_are_accounted():
    d=read(U5/'source/canonical-unit5-f1.json')
    assert [s['slide'] for s in d['ppt_raw_slides']]==list(range(1,113))
    assert {a['topic'] for a in d['ced_current_atoms']}=={'5.1','5.2','5.3','5.4','5.5'}
    assert all(s['coverage_status'] in {'MAPPED','MAPPED_VISUAL','PRESERVED_METADATA','PRESERVED_RAW'} for s in d['ppt_raw_slides'])

def test_unit5_review_flags_and_lock():
    d=read(U5/'source/canonical-unit5-f1.json')
    assert all(f['status']=='RESOLVED' and f['resolution'] for f in d['review_flags'])
    assert all(r['canonical_lock']=='LOCKED_F1' for r in d['canonical_catalog'])
    lock=read(U5/'content-lock-f1.json'); assert lock['lock_status']=='LOCKED_F1'
    for x in lock['protected_files']:
        p=U5/x['path']; assert p.stat().st_size==x['bytes']; assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']

def test_unit5_f1_historical_boundary_is_preserved_after_later_release():
    r=read(U5/'f1-release-manifest.json')
    assert r['student_release'] is False
    assert (r['journeys'],r['scenes'],r['memory_objects'],r['application_challenges'])==(0,0,0,0)
    client=TestClient(app)
    current=client.get('/api/units/unit-5').json()
    assert current['status'] in {'SCIENCE_LOCKED_F1_NOT_STUDENT_RELEASED','LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW','F4G_JOURNEYS1_7_POLISHED_DEVELOPER_PREVIEW','F4H_JOURNEYS1_8_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
    if current['status']=='STUDENT_READY':
        assert current['student_release'] is True
        assert client.get('/api/units/unit-5/application-lab').json()['challenge_count']==16

def test_unit5_pleiotropy_coverage_repair_and_upstream_protection():
    d=read(U5/'source/canonical-unit5-f1.json')
    assert any(r['canonical_label'].casefold()=='pleiotropy' and r['scope_class']=='AP_REQUIRED' for r in d['canonical_catalog'])
    up=read(U5/'upstream-u1-u4-protection-f1.json'); assert up['protected_file_count']==216
    for x in up['protected_files']:
        p=ROOT/x['path']; assert p.stat().st_size==x['bytes']; assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
