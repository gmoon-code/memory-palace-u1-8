import json,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U3=ROOT/'content/ap-biology/unit-3'; client=TestClient(app)
def read(rel): return json.loads((U3/rel).read_text())

def test_unit3_f5_zero_loss_release_accounting():
    f=read('finalization-f5.json')
    assert f['release_status']=='STUDENT_READY_F5'
    assert f['canonical_records']==f['accounted_records']==186
    assert f['story_records']==171
    assert f['challenge_lab_records']==11
    assert f['scope_guard_records']==4
    assert f['unaccounted_records']==0
    parts=[set(f['destinations']['story']),set(f['destinations']['challenge_lab']),set(f['destinations']['scope_guards'])]
    assert len(parts[0])==171 and len(parts[1])==11 and len(parts[2])==4
    assert not any(parts[i]&parts[j] for i in range(3) for j in range(i+1,3))

def test_unit3_f5_review_and_mixed_discrimination():
    r=read('review-manifest-f5.json'); m=read('mixed-discrimination-f5.json')
    assert r['target_count']==len(r['targets'])==126
    assert r['mandatory_spelling_targets']==0
    assert r['visible_review_limit']==5
    assert m['set_count']==len(m['sets'])==28
    assert m['question_count']==sum(len(x['questions']) for x in m['sets'])==78
    for s in m['sets']:
        assert s['initial_delay_hours']>=48
        assert len(s['questions'])==len(s['terms'])
        for q in s['questions']:
            assert q['answer'] in q['choices']
            assert q['answer'].casefold() not in q['prompt'].casefold()

def test_unit3_f5_challenge_lab_and_scope_guards():
    lab=read('application-lab.json'); guards=read('scope-guards-f5.json')
    assert lab['challenge_count']==lab['practice_only_runtime_count']==11
    assert len(lab['items'])==11
    assert guards['guard_count']==len(guards['guards'])==4
    assert {x['knowledge_id'] for x in guards['guards']}=={'U3-K-069','U3-K-129','U3-K-139','U3-K-166'}
    assert all(not x['student_runtime'] and not x['permanent_palace'] and not x['challenge_lab'] for x in guards['guards'])

def test_unit3_f5_live_api_is_student_ready():
    health=client.get('/api/health').json(); assert health['version'].startswith('v2-apbio-')
    d=client.get('/api/units/unit-3').json()
    assert d['status']=='STUDENT_READY'
    assert d['student_release'] is True and d['preview_release'] is False
    assert d['canonical_records_accounted']==186
    assert d['application_challenges']==11
    reg=client.get('/api/units/unit-3/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in reg]==[f'U3-J{i}' for i in range(1,8)]
    assert client.get('/api/units/unit-3/application-lab').json()['challenge_count']==11
    assert client.get('/api/units/unit-3/review-manifest').json()['target_count']==126
    assert client.get('/api/units/unit-3/mixed-discrimination').json()['set_count']==28
    assert client.get('/api/units/unit-3/scope-guards').json()['guard_count']==4
    assert client.get('/api/units/unit-3/finalization').json()['release_status']=='STUDENT_READY_F5'

def test_unit3_f5_lock_hashes():
    lock=read('content-lock-f5.json')
    for rel,digest in lock['files'].items():
        p=U3/rel; assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
