import json, re, hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U2=ROOT/'content'/'ap-biology'/'unit-2'; client=TestClient(app)
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_f5_accounts_for_all_142_records():
    final=read(U2/'finalization-f5.json')
    assert final['canonical_records']==142
    assert final['story_records']==133 and final['challenge_lab_records']==9
    assert final['accounted_records']==142 and final['unaccounted_records']==0
    assert len(final['destinations']['story'])==133 and len(final['destinations']['challenge_lab'])==9
    assert set(final['destinations']['story']).isdisjoint(final['destinations']['challenge_lab'])

def test_f5_challenge_lab_covers_all_nine_practice_only_records():
    lab=read(U2/'application-lab.json'); cls=read(U2/'architecture/learning-classification-f2.json')
    expected={r['knowledge_id'] for r in cls['records'] if r['destination']=='CHALLENGE_LAB'}
    assert lab['challenge_count']==9 and lab['practice_only_runtime_count']==9
    assert {x['knowledge_id'] for x in lab['items']}==expected
    assert all(len(x['prompt'])>=100 and len(x['answer_guide'])>=100 for x in lab['items'])

def test_f5_exact_name_review_manifest_is_complete_and_answer_redacted():
    review=read(U2/'review-manifest-f5.json'); cls=read(U2/'architecture/learning-classification-f2.json')
    expected={r['knowledge_id'] for r in cls['records'] if r['exact_name_recall']}
    assert review['target_count']==106 and review['mandatory_spelling_targets']==0
    assert {x['knowledge_id'] for x in review['targets']}==expected
    for x in review['targets']:
        assert x['target_answer'].lower() not in x['prompt'].lower()

def test_f5_all_17_mixed_discrimination_sets_are_operational():
    d=read(U2/'mixed-discrimination-f5.json')
    assert d['set_count']==17 and d['question_count']==44
    assert all(s['initial_delay_hours']>=48 for s in d['sets'])
    for s in d['sets']:
        assert len(s['questions'])>=2
        for q in s['questions']:
            assert q['answer'] in q['choices']
            assert q['answer'].lower() not in q['prompt'].lower()

def test_f5_api_marks_unit2_student_ready_and_exposes_finalization_tools():
    u=client.get('/api/units/unit-2').json()
    assert u['status']=='STUDENT_READY' and u['student_release'] is True and u['preview_release'] is False
    assert u['application_challenges']==9 and u['exact_name_review_targets']==106 and u['mixed_discrimination_sets']==17
    assert len(client.get('/api/units/unit-2/journeys').json()['guided_journeys'])==7
    assert client.get('/api/units/unit-2/application-lab').json()['challenge_count']==9
    assert client.get('/api/units/unit-2/review-manifest').json()['target_count']==106
    assert client.get('/api/units/unit-2/mixed-discrimination').json()['set_count']==17
    assert client.get('/api/units/unit-2/finalization').json()['unaccounted_records']==0

def test_f5_lock_hashes():
    lock=read(U2/'content-lock-f5.json')
    for rel,digest in lock['files'].items():
        p=U2/rel; assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
