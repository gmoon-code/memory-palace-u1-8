import json,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U7=ROOT/'content/ap-biology/unit-7'; client=TestClient(app)
def read(rel): return json.loads((U7/rel).read_text(encoding='utf-8'))

def test_unit7_f5_zero_loss_and_memory_objects():
    f=read('finalization-f5.json'); m=read('memory-objects-f5.json')
    assert f['release_status']=='STUDENT_READY_F5'
    assert f['canonical_records']==f['accounted_records']==215 and f['unaccounted_records']==0
    assert f['runtime_memory_objects']==f['story_records']==174
    assert f['challenge_lab_records']==16 and f['scope_guard_records']==25
    assert m['count']==len(m['memory_objects'])==174 and m['exact_name_required_count']==94
    parts=[set(f['destinations']['story']),set(f['destinations']['challenge_lab']),set(f['destinations']['scope_guards'])]
    assert [len(x) for x in parts]==[174,16,25]
    assert not any(parts[i]&parts[j] for i in range(3) for j in range(i+1,3))
    assert len(set().union(*parts))==215

def test_unit7_f5_review_mixed_challenges_and_guards():
    r=read('review-manifest-f5.json'); mix=read('mixed-discrimination-f5.json'); lab=read('application-lab.json'); g=read('scope-guards-f5.json')
    assert r['target_count']==94 and r['non_exact_palace_records']==80 and r['mandatory_spelling_targets']==0 and r['visible_review_limit']==5
    assert mix['set_count']==33 and mix['question_count']==102
    assert all(s['initial_delay_hours']>=48 and len(s['questions'])==len(s['terms']) for s in mix['sets'])
    for s in mix['sets']:
        for q in s['questions']:
            assert q['answer'] in q['choices'] and q['answer'].casefold() not in q['prompt'].casefold()
    assert lab['challenge_count']==lab['practice_only_runtime_count']==16 and len(lab['items'])==16
    assert all(len(x['prompt'])>=150 and len(x['answer_guide'])>=150 and len(x['story_hint'])>=70 for x in lab['items'])
    assert g['guard_count']==len(g['guards'])==25
    assert all(not x['student_runtime'] and not x['permanent_palace'] and not x['challenge_lab'] for x in g['guards'])

def test_unit7_f5_live_api_student_ready():
    d=client.get('/api/units/unit-7').json()
    assert d['status']=='STUDENT_READY' and d['student_release'] is True and d['preview_release'] is False
    assert d['canonical_records_accounted']==215 and d['runtime_memory_objects']==174 and d['application_challenges']==16
    registry=client.get('/api/units/unit-7/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in registry]==[f'U7-J{i}' for i in range(1,7)]
    assert sum(x['scene_count'] for x in registry)==55 and sum(x['checkpoint_count'] for x in registry)==18
    for i in range(1,7): assert client.get(f'/api/units/unit-7/journeys/U7-J{i}').status_code==200
    assert client.get('/api/units/unit-7/application-lab').json()['challenge_count']==16
    assert client.get('/api/units/unit-7/review-manifest').json()['target_count']==94
    assert client.get('/api/units/unit-7/mixed-discrimination').json()['set_count']==33
    assert client.get('/api/units/unit-7/scope-guards').json()['guard_count']==25
    assert client.get('/api/units/unit-7/finalization').json()['unaccounted_records']==0
    o=client.get('/api/units/unit-7/objects/U7-K-001').json()
    assert o['scientific_lock_status']=='LOCKED_F1' and o['narrative_lock_status']=='LOCKED_F4F' and o['student_runtime'] is True

def test_unit7_f5_narratives_frozen_and_lock_hashes():
    lock=read('content-lock-f5.json')
    for rel,digest in lock['files'].items(): assert hashlib.sha256((U7/rel).read_bytes()).hexdigest()==digest
    for rel,digest in lock['protected_narratives'].items(): assert hashlib.sha256((U7/rel).read_bytes()).hexdigest()==digest
    for rel,digest in lock['protected_upstream_locks'].items(): assert hashlib.sha256((U7/rel).read_bytes()).hexdigest()==digest

def test_unit7_f5_mainline_units1_7_totals():
    d=json.loads((ROOT/'content/ap-biology/mainline-release-u1-u7.json').read_text(encoding='utf-8'))
    assert d['units']==['unit-1','unit-2','unit-3','unit-4','unit-5','unit-6','unit-7']
    assert d['runtime_version'] in {'v2-apbio-0.27.0-u7-f5','v2-apbio-0.28.0-u7-f6'}
    assert d['totals']=={'canonical_records_units_1_7':1306,'guided_journeys':50,'permanent_scenes':390,'challenge_lab_items':99}
