import hashlib
import json
from pathlib import Path

from fastapi.testclient import TestClient
from backend.main import app

ROOT=Path(__file__).resolve().parents[1]
U8=ROOT/'content/ap-biology/unit-8'
client=TestClient(app)
def read(rel): return json.loads((U8/rel).read_text(encoding='utf-8'))


def test_unit8_f5_zero_loss_and_memory_objects():
    f=read('finalization-f5.json'); m=read('memory-objects-f5.json')
    assert f['release_status']=='STUDENT_READY_F5'
    assert f['canonical_records']==f['accounted_records']==255 and f['unaccounted_records']==0
    assert f['runtime_memory_objects']==f['story_records']==211
    assert f['challenge_lab_records']==13 and f['scope_guard_records']==31
    assert m['count']==len(m['memory_objects'])==211 and m['exact_name_required_count']==135
    parts=[set(f['destinations']['story']),set(f['destinations']['challenge_lab']),set(f['destinations']['scope_guards'])]
    assert [len(x) for x in parts]==[211,13,31]
    assert not any(parts[i]&parts[j] for i in range(3) for j in range(i+1,3))
    assert len(set().union(*parts))==255


def test_unit8_f5_review_mixed_challenges_and_guards():
    r=read('review-manifest-f5.json'); mix=read('mixed-discrimination-f5.json'); lab=read('application-lab.json'); g=read('scope-guards-f5.json')
    assert r['target_count']==135 and r['non_exact_palace_records']==76 and r['mandatory_spelling_targets']==0 and r['visible_review_limit']==5
    assert mix['set_count']==40 and mix['question_count']==104
    assert all(s['initial_delay_hours']>=48 and len(s['questions'])==len(s['terms']) for s in mix['sets'])
    for s in mix['sets']:
        for q in s['questions']:
            assert q['answer'] in q['choices'] and q['answer'].casefold() not in q['prompt'].casefold()
    assert lab['challenge_count']==lab['practice_only_runtime_count']==13 and len(lab['items'])==13
    assert all(len(x['prompt'])>=150 and len(x['answer_guide'])>=150 and len(x['story_hint'])>=70 for x in lab['items'])
    assert g['guard_count']==len(g['guards'])==31
    assert all(not x['student_runtime'] and not x['permanent_palace'] and not x['challenge_lab'] for x in g['guards'])


def test_unit8_f5_live_api_student_ready():
    assert client.get('/api/health').json()['version'] in {'v2-apbio-0.29.0-u8-f5','v2-apbio-0.30.0-u8-f6'}
    d=client.get('/api/units/unit-8').json()
    assert d['status']=='STUDENT_READY' and d['student_release'] is True and d['preview_release'] is False
    assert d['canonical_records_accounted']==255 and d['runtime_memory_objects']==211 and d['application_challenges']==13
    registry=client.get('/api/units/unit-8/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in registry]==[f'U8-J{i}' for i in range(1,9)]
    assert [x['scene_count'] for x in registry]==[12,9,5,7,5,8,4,8]
    assert sum(x['checkpoint_count'] for x in registry)==18
    for i in range(1,9): assert client.get(f'/api/units/unit-8/journeys/U8-J{i}').status_code==200
    assert client.get('/api/units/unit-8/application-lab').json()['challenge_count']==13
    assert client.get('/api/units/unit-8/review-manifest').json()['target_count']==135
    assert client.get('/api/units/unit-8/mixed-discrimination').json()['set_count']==40
    assert client.get('/api/units/unit-8/scope-guards').json()['guard_count']==31
    assert client.get('/api/units/unit-8/finalization').json()['unaccounted_records']==0
    o=client.get('/api/units/unit-8/objects/U8-K-001').json()
    assert o['scientific_lock_status']=='LOCKED_F1' and o['narrative_lock_status']=='LOCKED_F4A_F4H' and o['student_runtime'] is True


def test_unit8_f5_narratives_frozen_and_lock_hashes():
    lock=read('content-lock-f5.json')
    for rel,digest in lock['files'].items(): assert hashlib.sha256((U8/rel).read_bytes()).hexdigest()==digest
    for rel,digest in lock['protected_narratives'].items(): assert hashlib.sha256((U8/rel).read_bytes()).hexdigest()==digest
    for rel,digest in lock['protected_upstream_locks'].items(): assert hashlib.sha256((U8/rel).read_bytes()).hexdigest()==digest


def test_unit8_f5_mainline_units1_8_totals():
    d=json.loads((ROOT/'content/ap-biology/mainline-release-u1-u8.json').read_text(encoding='utf-8'))
    assert d['units']==['unit-1','unit-2','unit-3','unit-4','unit-5','unit-6','unit-7','unit-8']
    assert d['runtime_version'] in {'v2-apbio-0.29.0-u8-f5','v2-apbio-0.30.0-u8-f6'}
    assert d['totals']=={'canonical_records_units_1_8':1561,'guided_journeys':58,'permanent_scenes':448,'challenge_lab_items':112}
