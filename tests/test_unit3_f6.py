import hashlib,json
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1];U3=ROOT/'content/ap-biology/unit-3';client=TestClient(app)
def read(name):return json.loads((U3/name).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def test_unit3_f6_validation_artifact_and_release_state():
    ux=read('ux-validation-f6.json');status=read('status-f6.json')
    assert ux['release_status']=='STUDENT_READY_F6_VALIDATED'
    assert ux['curriculum_content_changed'] is False
    assert ux['scenes_validated']==54 and ux['recall_scenes_validated']==18
    assert ux['browser_validation']['scene_viewport_combinations']==162
    assert ux['browser_validation']['recall_viewport_combinations']==54
    assert ux['browser_validation']['result']=='PASS'
    assert status['pipeline_stage']=='UNIT3_CLASSROOM_BROWSER_VALIDATED_F6'
    assert status['student_release'] is True and status['preview_release'] is False

def test_unit3_f6_preserves_f5_lock_and_curriculum_counts():
    ux=read('ux-validation-f6.json');f5=read('finalization-f5.json')
    assert ux['f5_lock_sha256']==sha(U3/'content-lock-f5.json')
    assert f5['canonical_records']==186 and f5['accounted_records']==186
    assert f5['story_records']==171 and f5['challenge_lab_records']==11 and f5['scope_guard_records']==4
    assert f5['guided_journeys']==7 and f5['permanent_loci']==54

def test_unit3_f6_content_lock():
    lock=read('content-lock-f6.json')
    for rel,digest in lock['files'].items():
        assert sha(U3/rel)==digest

def test_unit3_f6_live_api():
    assert client.get('/api/health').json()['version'].startswith('v2-apbio-')
    u=client.get('/api/units/unit-3').json()
    assert u['status']=='STUDENT_READY' and u['browser_validation']=='PASS_F6'
    assert u['pipeline_stage']=='UNIT3_CLASSROOM_BROWSER_VALIDATED_F6'
    assert len(client.get('/api/units/unit-3/journeys').json()['guided_journeys'])==7
    assert client.get('/api/units/unit-3/application-lab').json()['challenge_count']==11
    assert client.get('/api/units/unit-3/review-manifest').json()['target_count']==126
    assert client.get('/api/units/unit-3/mixed-discrimination').json()['set_count']==28
