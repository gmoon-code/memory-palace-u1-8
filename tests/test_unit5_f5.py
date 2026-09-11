import json,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U5=ROOT/'content/ap-biology/unit-5'; client=TestClient(app)
def read(rel): return json.loads((U5/rel).read_text(encoding='utf-8'))

def test_unit5_f5_zero_loss_and_memory_objects():
    f=read('finalization-f5.json'); m=read('memory-objects-f5.json')
    assert f['release_status']=='STUDENT_READY_F5'
    assert f['canonical_records']==f['accounted_records']==152 and f['unaccounted_records']==0
    assert f['runtime_memory_objects']==f['story_records']==131
    assert f['challenge_lab_records']==16 and f['scope_guard_records']==5
    assert m['count']==len(m['memory_objects'])==131 and m['exact_name_required_count']==130
    parts=[set(f['destinations']['story']),set(f['destinations']['challenge_lab']),set(f['destinations']['scope_guards'])]
    assert [len(x) for x in parts]==[131,16,5]
    assert not any(parts[i]&parts[j] for i in range(3) for j in range(i+1,3))

def test_unit5_f5_review_mixed_challenges_and_guards():
    r=read('review-manifest-f5.json'); mix=read('mixed-discrimination-f5.json'); lab=read('application-lab.json'); g=read('scope-guards-f5.json')
    assert r['target_count']==130 and r['non_exact_palace_records']==1 and r['mandatory_spelling_targets']==0 and r['visible_review_limit']==5
    assert mix['set_count']==32 and mix['question_count']==79
    assert all(s['initial_delay_hours']>=48 and len(s['questions'])==len(s['terms']) for s in mix['sets'])
    for s in mix['sets']:
        for q in s['questions']:
            assert q['answer'] in q['choices'] and q['answer'].casefold() not in q['prompt'].casefold()
    assert lab['challenge_count']==lab['practice_only_runtime_count']==16 and len(lab['items'])==16
    assert g['guard_count']==len(g['guards'])==5

def test_unit5_f5_live_api_student_ready():
    d=client.get('/api/units/unit-5').json()
    assert d['status']=='STUDENT_READY' and d['student_release'] is True and d['preview_release'] is False
    assert d['canonical_records_accounted']==152 and d['runtime_memory_objects']==131 and d['application_challenges']==16
    assert [x['palace_id'] for x in client.get('/api/units/unit-5/journeys').json()['guided_journeys']]==[f'U5-J{i}' for i in range(1,9)]
    assert client.get('/api/units/unit-5/application-lab').json()['challenge_count']==16
    assert client.get('/api/units/unit-5/review-manifest').json()['target_count']==130
    assert client.get('/api/units/unit-5/mixed-discrimination').json()['set_count']==32
    assert client.get('/api/units/unit-5/scope-guards').json()['guard_count']==5
    assert client.get('/api/units/unit-5/finalization').json()['unaccounted_records']==0
    o=client.get('/api/units/unit-5/objects/U5-K-001').json()
    assert o['scientific_lock_status']=='LOCKED_F1' and o['narrative_lock_status']=='LOCKED_F4H'

def test_unit5_f5_nonexact_chi_square_contribution_is_not_forced_into_exact_review():
    r=read('review-manifest-f5.json'); m=read('memory-objects-f5.json')
    assert 'U5-K-115' not in {x['knowledge_id'] for x in r['targets']}
    obj=next(x for x in m['memory_objects'] if x['memory_object_id']=='U5-K-115')
    assert obj['exact_name_required']=='NO' and obj['reverse_prompt_meaning_to_name'] is None

def test_unit5_f5_narratives_frozen_and_lock_hashes():
    lock=read('content-lock-f5.json')
    for rel,digest in lock['protected_narratives'].items(): assert hashlib.sha256((U5/rel).read_bytes()).hexdigest()==digest
    for rel,digest in lock['files'].items(): assert hashlib.sha256((U5/rel).read_bytes()).hexdigest()==digest
