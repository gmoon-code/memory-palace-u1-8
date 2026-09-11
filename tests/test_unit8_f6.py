import hashlib
import json
from pathlib import Path

from fastapi.testclient import TestClient
from backend.main import app
from scripts.site_release_guard import site_runtime_hash_allowed

ROOT = Path(__file__).resolve().parents[1]
U8 = ROOT / 'content/ap-biology/unit-8'
client = TestClient(app)


def read(name):
    return json.loads((U8 / name).read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def test_unit8_f6_validation_artifact_and_release_state():
    ux = read('ux-validation-f6.json'); status = read('status-f6.json')
    assert ux['release_status'] == 'STUDENT_READY_F6_VALIDATED'
    assert ux['curriculum_content_changed'] is False
    assert ux['scenes_validated'] == 58 and ux['recall_scenes_validated'] == 18
    assert ux['browser_facing_validation']['scene_viewport_contract_checks'] == 174
    assert ux['browser_facing_validation']['recall_viewport_contract_checks'] == 54
    assert ux['browser_facing_validation']['route_lengths'] == [12,9,5,7,5,8,4,8]
    assert ux['browser_facing_validation']['result'] == 'PASS'
    assert ux['browser_facing_validation']['pixel_screenshot_validation'] == 'NOT_EXECUTED_IN_THIS_CONTAINER'
    assert status['pipeline_stage'] == 'UNIT8_CLASSROOM_BROWSER_VALIDATED_F6'
    assert status['student_release'] is True and status['preview_release'] is False


def test_unit8_f6_preserves_f5_curriculum_and_narratives():
    ux = read('ux-validation-f6.json'); f5 = read('finalization-f5.json'); f5lock = read('content-lock-f5.json')
    assert ux['f5_lock_sha256'] == sha(U8 / 'content-lock-f5.json')
    assert f5['canonical_records'] == f5['accounted_records'] == 255 and f5['unaccounted_records'] == 0
    assert f5['runtime_memory_objects'] == 211 and f5['challenge_lab_records'] == 13 and f5['scope_guard_records'] == 31
    assert f5['guided_journeys'] == 8 and f5['permanent_loci'] == 58 and f5['optional_first_exposure_recalls'] == 18
    assert f5['exact_name_review_targets'] == 135 and f5['mixed_discrimination_sets'] == 40 and f5['mixed_discrimination_questions'] == 104
    for rel, digest in f5lock['files'].items(): assert sha(U8 / rel) == digest
    for rel, digest in f5lock['protected_narratives'].items(): assert sha(U8 / rel) == digest
    for rel, digest in f5lock['protected_upstream_locks'].items(): assert sha(U8 / rel) == digest


def test_unit8_f6_content_and_runtime_lock():
    lock = read('content-lock-f6.json'); f5 = read('content-lock-f5.json')
    for rel, digest in lock['files'].items(): assert sha(U8 / rel) == digest
    changed = [rel for rel, digest in f5['runtime_file_sha256'].items() if lock['runtime_file_sha256'].get(rel) != digest]
    assert set(changed) == {'backend/main.py', 'frontend/js/audio.js'}
    for rel, digest in lock['runtime_file_sha256'].items():
        current=sha(ROOT / rel)
        assert current == digest or site_runtime_hash_allowed(ROOT,rel,current)


def test_unit8_f6_live_api():
    assert client.get('/api/health').json()['version'] == 'v2-apbio-0.30.0-u8-f6'
    u = client.get('/api/units/unit-8').json()
    assert u['status'] == 'STUDENT_READY' and u['browser_validation'] == 'PASS_F6'
    assert u['pipeline_stage'] == 'UNIT8_CLASSROOM_BROWSER_VALIDATED_F6'
    assert len(client.get('/api/units/unit-8/journeys').json()['guided_journeys']) == 8
    assert client.get('/api/units/unit-8/application-lab').json()['challenge_count'] == 13
    assert client.get('/api/units/unit-8/review-manifest').json()['target_count'] == 135
    mixed = client.get('/api/units/unit-8/mixed-discrimination').json()
    assert mixed['set_count'] == 40 and mixed['question_count'] == 104
    assert client.get('/api/units/unit-8/scope-guards').json()['guard_count'] == 31
    assert client.get('/api/units/unit-8/finalization').json()['unaccounted_records'] == 0
    for i in range(1,9): assert client.get(f'/api/units/unit-8/journeys/U8-J{i}').status_code == 200


def test_unit8_f6_mainline_release_manifest():
    d = json.loads((ROOT / 'content/ap-biology/mainline-release-u1-u8.json').read_text(encoding='utf-8'))
    assert d['schema'] == 'memory-palace-v2-mainline-u1-u8-f6-1.0'
    assert d['release_status'] == 'STUDENT_READY_UNITS_1_8_UNIT8_F6_VALIDATED'
    assert d['runtime_version'] == 'v2-apbio-0.30.0-u8-f6'
    assert d['unit8']['stage'] == 'F6' and d['unit8']['browser_validation'] == 'PASS_F6'
    assert d['totals'] == {'canonical_records_units_1_8':1561,'guided_journeys':58,'permanent_scenes':448,'challenge_lab_items':112}
