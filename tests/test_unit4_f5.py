import json,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U4=ROOT/'content/ap-biology/unit-4'; client=TestClient(app)
def read(rel): return json.loads((U4/rel).read_text(encoding='utf-8'))

def test_unit4_f5_zero_loss_and_memory_objects():
    f=read('finalization-f5.json'); m=read('memory-objects-f5.json')
    assert f['release_status']=='STUDENT_READY_F5'
    assert f['canonical_records']==f['accounted_records']==180 and f['unaccounted_records']==0
    assert f['runtime_memory_objects']==f['story_records']==162
    assert f['challenge_lab_records']==15 and f['scope_guard_records']==3
    assert m['count']==len(m['memory_objects'])==162
    parts=[set(f['destinations']['story']),set(f['destinations']['challenge_lab']),set(f['destinations']['scope_guards'])]
    assert [len(x) for x in parts]==[162,15,3]
    assert not any(parts[i]&parts[j] for i in range(3) for j in range(i+1,3))

def test_unit4_f5_review_mixed_challenges_and_guards():
    r=read('review-manifest-f5.json'); mix=read('mixed-discrimination-f5.json'); lab=read('application-lab.json'); g=read('scope-guards-f5.json')
    assert r['target_count']==162 and r['mandatory_spelling_targets']==0 and r['visible_review_limit']==5
    assert mix['set_count']==33 and mix['question_count']==99
    assert all(s['initial_delay_hours']>=48 and len(s['questions'])==len(s['terms']) for s in mix['sets'])
    for s in mix['sets']:
        for q in s['questions']:
            assert q['answer'] in q['choices'] and q['answer'].casefold() not in q['prompt'].casefold()
    assert lab['challenge_count']==lab['practice_only_runtime_count']==15 and len(lab['items'])==15
    assert g['guard_count']==len(g['guards'])==3

def test_unit4_f5_live_api_student_ready():
    d=client.get('/api/units/unit-4').json()
    assert d['status']=='STUDENT_READY' and d['student_release'] is True and d['preview_release'] is False
    assert d['canonical_records_accounted']==180 and d['runtime_memory_objects']==162 and d['application_challenges']==15
    assert [x['palace_id'] for x in client.get('/api/units/unit-4/journeys').json()['guided_journeys']]==[f'U4-J{i}' for i in range(1,8)]
    assert client.get('/api/units/unit-4/application-lab').json()['challenge_count']==15
    assert client.get('/api/units/unit-4/review-manifest').json()['target_count']==162
    assert client.get('/api/units/unit-4/mixed-discrimination').json()['set_count']==33
    assert client.get('/api/units/unit-4/scope-guards').json()['guard_count']==3
    assert client.get('/api/units/unit-4/finalization').json()['unaccounted_records']==0
    o=client.get('/api/units/unit-4/objects/U4-K-046').json()
    assert o['canonical_term']=='Ligand' and o['scientific_lock_status']=='LOCKED_F1'

def test_unit4_f5_narratives_frozen_and_lock_hashes():
    f4=read('content-lock-f4g.json')
    for rel,meta in f4['files'].items():
        if rel.startswith('journeys/U4-J'):
            p=U4/rel; assert p.stat().st_size==meta['bytes']; assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']
    lock=read('content-lock-f5.json')
    for rel,digest in lock['files'].items(): assert hashlib.sha256((U4/rel).read_bytes()).hexdigest()==digest
