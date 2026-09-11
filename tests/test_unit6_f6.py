import hashlib,json
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
from scripts.site_release_guard import site_runtime_hash_allowed
ROOT=Path(__file__).resolve().parents[1]; U6=ROOT/'content/ap-biology/unit-6'; client=TestClient(app)
def read(name): return json.loads((U6/name).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def test_unit6_f6_validation_artifact_and_release_state():
    ux=read('ux-validation-f6.json'); status=read('status-f6.json')
    assert ux['release_status']=='STUDENT_READY_F6_VALIDATED'
    assert ux['curriculum_content_changed'] is False
    assert ux['scenes_validated']==53 and ux['recall_scenes_validated']==18
    assert ux['browser_facing_validation']['scene_viewport_contract_checks']==159
    assert ux['browser_facing_validation']['recall_viewport_contract_checks']==54
    assert ux['browser_facing_validation']['route_lengths']==[12,8,8,12,8,5]
    assert ux['browser_facing_validation']['result']=='PASS'
    assert ux['browser_facing_validation']['pixel_screenshot_validation']=='NOT_EXECUTED_IN_THIS_CONTAINER'
    assert status['pipeline_stage']=='UNIT6_CLASSROOM_BROWSER_VALIDATED_F6'
    assert status['student_release'] is True and status['preview_release'] is False

def test_unit6_f6_preserves_f5_curriculum_and_narratives():
    ux=read('ux-validation-f6.json'); f5=read('finalization-f5.json'); f5lock=read('content-lock-f5.json')
    assert ux['f5_lock_sha256']==sha(U6/'content-lock-f5.json')
    assert f5['canonical_records']==f5['accounted_records']==202 and f5['unaccounted_records']==0
    assert f5['runtime_memory_objects']==161 and f5['challenge_lab_records']==16 and f5['scope_guard_records']==25
    assert f5['guided_journeys']==6 and f5['permanent_loci']==53 and f5['optional_first_exposure_recalls']==18
    assert f5['exact_name_review_targets']==134 and f5['mixed_discrimination_sets']==37 and f5['mixed_discrimination_questions']==94
    for rel,digest in f5lock['files'].items(): assert sha(U6/rel)==digest
    for rel,digest in f5lock['protected_narratives'].items(): assert sha(U6/rel)==digest
    for rel,digest in f5lock['protected_upstream_locks'].items(): assert sha(U6/rel)==digest

def test_unit6_f6_content_and_runtime_lock():
    lock=read('content-lock-f6.json'); f5=read('content-lock-f5.json')
    for rel,digest in lock['files'].items(): assert sha(U6/rel)==digest
    historical_changed=[rel for rel,digest in f5['runtime_file_sha256'].items() if lock['runtime_file_sha256'].get(rel)!=digest]
    assert set(historical_changed)=={'backend/main.py','frontend/js/audio.js'}
    u7lock6=ROOT/'content/ap-biology/unit-7/content-lock-f6.json'; u7lock5=ROOT/'content/ap-biology/unit-7/content-lock-f5.json'
    u7lock_path=u7lock6 if u7lock6.exists() else u7lock5
    u7runtime=json.loads(u7lock_path.read_text(encoding='utf-8')).get('runtime_file_sha256',{}) if u7lock_path.exists() else {}
    u8lock6=ROOT/'content/ap-biology/unit-8/content-lock-f6.json'; u8lock5=ROOT/'content/ap-biology/unit-8/content-lock-f5.json'
    u8lock=u8lock6 if u8lock6.exists() else u8lock5
    u8runtime=json.loads(u8lock.read_text(encoding='utf-8')).get('runtime_file_sha256',{}) if u8lock.exists() else {}
    for rel,digest in lock['runtime_file_sha256'].items():
        current=sha(ROOT/rel)
        assert current==digest or u7runtime.get(rel)==current or u8runtime.get(rel)==current or site_runtime_hash_allowed(ROOT,rel,current)

def test_unit6_f6_live_api():
    assert client.get('/api/health').json()['version'] in {'v2-apbio-0.26.0-u6-f6','v2-apbio-0.27.0-u7-f5','v2-apbio-0.28.0-u7-f6','v2-apbio-0.29.0-u8-f5','v2-apbio-0.30.0-u8-f6'}
    u=client.get('/api/units/unit-6').json()
    assert u['status']=='STUDENT_READY' and u['browser_validation']=='PASS_F6'
    assert u['pipeline_stage']=='UNIT6_CLASSROOM_BROWSER_VALIDATED_F6'
    assert len(client.get('/api/units/unit-6/journeys').json()['guided_journeys'])==6
    assert client.get('/api/units/unit-6/application-lab').json()['challenge_count']==16
    assert client.get('/api/units/unit-6/review-manifest').json()['target_count']==134
    mixed=client.get('/api/units/unit-6/mixed-discrimination').json()
    assert mixed['set_count']==37 and mixed['question_count']==94
    assert client.get('/api/units/unit-6/scope-guards').json()['guard_count']==25
    assert client.get('/api/units/unit-6/finalization').json()['unaccounted_records']==0
    for i in range(1,7): assert client.get(f'/api/units/unit-6/journeys/U6-J{i}').status_code==200

def test_unit6_f6_mainline_release_manifest():
    d=json.loads((ROOT/'content/ap-biology/mainline-release-u1-u6.json').read_text(encoding='utf-8'))
    assert d['schema']=='memory-palace-v2-mainline-u1-u6-f6-1.0'
    assert d['release_status']=='STUDENT_READY_UNITS_1_6_UNIT6_F6_VALIDATED'
    assert d['unit6']['stage']=='F6' and d['unit6']['browser_validation']=='PASS_F6'
    assert d['totals']=={'canonical_records_units_1_6':1091,'guided_journeys':44,'permanent_scenes':335,'challenge_lab_items':83}
