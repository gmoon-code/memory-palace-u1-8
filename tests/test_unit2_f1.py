import hashlib, json
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app

ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
client=TestClient(app)

def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))

def test_unit2_f1_source_lock_counts():
    d=read(U2/'source/canonical-unit2-f1.json')
    assert len(d['ppt_raw_slides'])==109
    assert len(d['packet_current_ced_crosswalk'])==11
    assert len({x['topic'] for x in d['ced_current_atoms']})==10
    assert len(d['ced_current_atoms'])==66
    assert len(d['canonical_catalog'])==142
    assert len(d['review_flags'])==20
    assert d['qa']['blocking_missing_resources']==[]

def test_unit2_f1_locked_files_match_hashes():
    lock=read(U2/'content-lock-f1.json')
    assert lock['lock_status']=='LOCKED_F1'
    assert lock['student_release'] is False
    for rel,meta in lock['files'].items():
        p=ROOT/rel
        assert p.exists()
        assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']

def test_unit2_f1_catalog_ids_and_flags_are_valid():
    d=read(U2/'source/canonical-unit2-f1.json')
    records=d['canonical_catalog']
    ids=[x['knowledge_id'] for x in records]
    assert len(ids)==len(set(ids))==142
    flags={x['flag_id'] for x in d['review_flags']}
    assert all(x['status']=='RESOLVED' for x in d['review_flags'])
    assert all((not r.get('review_flag_id')) or r['review_flag_id'] in flags for r in records)
    assert {r['topic'] for r in records}=={f'2.{i}' for i in range(1,11)}
    assert all(r['canonical_lock'] in {'LOCKED_F1','LOCKED_WITH_CORRECTION_OR_SCOPE_NOTE'} for r in records)
    assert all(r.get('review_flag_id') for r in records if r['canonical_lock']=='LOCKED_WITH_CORRECTION_OR_SCOPE_NOTE')

def test_unit2_api_preserves_f1_lock_after_final_release():
    res=client.get('/api/units/unit-2')
    assert res.status_code==200
    d=res.json()
    assert d['status']=='STUDENT_READY'
    assert d['pipeline_stage']=='UNIT2_FINALIZED_F5'
    assert d['canonical_records']==142
    assert d['review_flags_resolved']==20
    assert d['blocking_missing_resources']==0
    assert d['student_release'] is True
    assert client.get('/api/units/unit-2/journeys').status_code==200
    assert client.get('/api/units/unit-2/application-lab').json()['challenge_count']==9

def test_unit2_final_runtime_uses_locked_catalog_without_duplicate_legacy_files():
    assert not (U2/'memory-objects.json').exists()
    assert not (U2/'journeys.json').exists()
    lab=read(U2/'application-lab.json')
    assert lab['challenge_count']==9
    assert (U2/'finalization-f5.json').exists()
