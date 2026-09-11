import hashlib,json
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
from scripts.site_release_guard import site_runtime_hash_allowed
ROOT=Path(__file__).resolve().parents[1]; U5=ROOT/'content/ap-biology/unit-5'; client=TestClient(app)
def read(name): return json.loads((U5/name).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def test_unit5_f6_validation_artifact_and_release_state():
    ux=read('ux-validation-f6.json'); status=read('status-f6.json')
    assert ux['release_status']=='STUDENT_READY_F6_VALIDATED'
    assert ux['curriculum_content_changed'] is False
    assert ux['scenes_validated']==50 and ux['recall_scenes_validated']==18
    assert ux['browser_facing_validation']['scene_viewport_contract_checks']==150
    assert ux['browser_facing_validation']['recall_viewport_contract_checks']==54
    assert ux['browser_facing_validation']['result']=='PASS'
    assert ux['browser_facing_validation']['pixel_screenshot_validation']=='NOT_EXECUTED_IN_THIS_CONTAINER'
    assert status['pipeline_stage']=='UNIT5_CLASSROOM_BROWSER_VALIDATED_F6'
    assert status['student_release'] is True and status['preview_release'] is False

def test_unit5_f6_preserves_f5_lock_and_counts():
    ux=read('ux-validation-f6.json'); f5=read('finalization-f5.json')
    assert ux['f5_lock_sha256']==sha(U5/'content-lock-f5.json')
    assert f5['canonical_records']==f5['accounted_records']==152 and f5['unaccounted_records']==0
    assert f5['runtime_memory_objects']==131 and f5['challenge_lab_records']==16 and f5['scope_guard_records']==5
    assert f5['guided_journeys']==8 and f5['permanent_loci']==50
    assert f5['exact_name_review_targets']==130 and f5['mixed_discrimination_sets']==32 and f5['mixed_discrimination_questions']==79

def test_unit5_f6_content_and_runtime_lock():
    lock=read('content-lock-f6.json')
    for rel,digest in lock['files'].items(): assert sha(U5/rel)==digest
    later_f6=ROOT/'content/ap-biology/unit-6/content-lock-f6.json'; later_f5=ROOT/'content/ap-biology/unit-6/content-lock-f5.json'
    later=later_f6 if later_f6.exists() else later_f5
    later_runtime=json.loads(later.read_text(encoding='utf-8')).get('runtime_file_sha256',{}) if later.exists() else {}
    u7f6=ROOT/'content/ap-biology/unit-7/content-lock-f6.json'; u7f5=ROOT/'content/ap-biology/unit-7/content-lock-f5.json'
    u7=u7f6 if u7f6.exists() else u7f5
    u7_runtime=json.loads(u7.read_text(encoding='utf-8')).get('runtime_file_sha256',{}) if u7.exists() else {}
    u8f6=ROOT/'content/ap-biology/unit-8/content-lock-f6.json'; u8f5=ROOT/'content/ap-biology/unit-8/content-lock-f5.json'
    u8=u8f6 if u8f6.exists() else u8f5
    u8_runtime=json.loads(u8.read_text(encoding='utf-8')).get('runtime_file_sha256',{}) if u8.exists() else {}
    for rel,digest in lock['runtime_file_sha256'].items():
        current=sha(ROOT/rel)
        assert current==digest or later_runtime.get(rel)==current or site_runtime_hash_allowed(ROOT,rel,current) or u7_runtime.get(rel)==current or u8_runtime.get(rel)==current

def test_unit5_f6_live_api():
    assert client.get('/api/health').json()['version'].startswith('v2-apbio-')
    u=client.get('/api/units/unit-5').json()
    assert u['status']=='STUDENT_READY' and u['browser_validation']=='PASS_F6'
    assert u['pipeline_stage']=='UNIT5_CLASSROOM_BROWSER_VALIDATED_F6'
    assert len(client.get('/api/units/unit-5/journeys').json()['guided_journeys'])==8
    assert client.get('/api/units/unit-5/application-lab').json()['challenge_count']==16
    assert client.get('/api/units/unit-5/review-manifest').json()['target_count']==130
    mixed=client.get('/api/units/unit-5/mixed-discrimination').json()
    assert mixed['set_count']==32 and mixed['question_count']==79
    assert client.get('/api/units/unit-5/scope-guards').json()['guard_count']==5
