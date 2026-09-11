import hashlib,json
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
from scripts.site_release_guard import site_runtime_hash_allowed
ROOT=Path(__file__).resolve().parents[1]; U4=ROOT/'content/ap-biology/unit-4'; client=TestClient(app)
def read(name): return json.loads((U4/name).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def test_unit4_f6_validation_artifact_and_release_state():
    ux=read('ux-validation-f6.json'); status=read('status-f6.json')
    assert ux['release_status']=='STUDENT_READY_F6_VALIDATED'
    assert ux['curriculum_content_changed'] is False
    assert ux['scenes_validated']==51 and ux['recall_scenes_validated']==18
    assert ux['browser_facing_validation']['scene_viewport_contract_checks']==153
    assert ux['browser_facing_validation']['recall_viewport_contract_checks']==54
    assert ux['browser_facing_validation']['result']=='PASS'
    assert ux['browser_facing_validation']['pixel_screenshot_validation']=='NOT_EXECUTED_IN_THIS_CONTAINER'
    assert status['pipeline_stage']=='UNIT4_CLASSROOM_BROWSER_VALIDATED_F6'
    assert status['student_release'] is True and status['preview_release'] is False

def test_unit4_f6_preserves_f5_lock_and_counts():
    ux=read('ux-validation-f6.json'); f5=read('finalization-f5.json')
    assert ux['f5_lock_sha256']==sha(U4/'content-lock-f5.json')
    assert f5['canonical_records']==f5['accounted_records']==180 and f5['unaccounted_records']==0
    assert f5['runtime_memory_objects']==162 and f5['challenge_lab_records']==15 and f5['scope_guard_records']==3
    assert f5['guided_journeys']==7 and f5['permanent_loci']==51

def test_unit4_f6_content_and_runtime_lock():
    lock=read('content-lock-f6.json')
    for rel,digest in lock['files'].items(): assert sha(U4/rel)==digest
    candidates=[ROOT/'content/ap-biology/unit-8/content-lock-f6.json',ROOT/'content/ap-biology/unit-8/content-lock-f5.json',ROOT/'content/ap-biology/unit-7/content-lock-f6.json',ROOT/'content/ap-biology/unit-6/content-lock-f6.json',ROOT/'content/ap-biology/unit-5/content-lock-f6.json']
    later=next((x for x in candidates if x.exists()),None)
    later_runtime=json.loads(later.read_text(encoding='utf-8')).get('runtime_file_sha256',{}) if later else {}
    for rel,digest in lock['runtime_file_sha256'].items():
        current=sha(ROOT/rel)
        assert current==digest or later_runtime.get(rel)==current or site_runtime_hash_allowed(ROOT,rel,current)

def test_unit4_f6_live_api():
    assert client.get('/api/health').json()['version'].startswith('v2-apbio-')
    u=client.get('/api/units/unit-4').json()
    assert u['status']=='STUDENT_READY' and u['browser_validation']=='PASS_F6'
    assert u['pipeline_stage']=='UNIT4_CLASSROOM_BROWSER_VALIDATED_F6'
    assert len(client.get('/api/units/unit-4/journeys').json()['guided_journeys'])==7
    assert client.get('/api/units/unit-4/application-lab').json()['challenge_count']==15
    assert client.get('/api/units/unit-4/review-manifest').json()['target_count']==162
    assert client.get('/api/units/unit-4/mixed-discrimination').json()['set_count']==33
    assert client.get('/api/units/unit-4/scope-guards').json()['guard_count']==3
