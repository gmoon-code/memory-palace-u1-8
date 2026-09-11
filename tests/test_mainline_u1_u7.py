import json
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]
client=TestClient(app)

def test_mainline_u1_u7_manifest_and_runtime():
    d=json.loads((ROOT/'content/ap-biology/mainline-release-u1-u7.json').read_text(encoding='utf-8'))
    assert d['units']==[f'unit-{i}' for i in range(1,8)]
    assert d['runtime_version']=='v2-apbio-0.28.0-u7-f6'
    assert d['totals']=={'canonical_records_units_1_7':1306,'guided_journeys':50,'permanent_scenes':390,'challenge_lab_items':99}
    assert client.get('/api/health').json()['version'] in {'v2-apbio-0.28.0-u7-f6','v2-apbio-0.29.0-u8-f5','v2-apbio-0.30.0-u8-f6'}

def test_all_seven_released_units_have_expected_journey_counts():
    expected={'unit-1':9,'unit-2':7,'unit-3':7,'unit-4':7,'unit-5':8,'unit-6':6,'unit-7':6}
    for uid,count in expected.items():
        assert len(client.get(f'/api/units/{uid}/journeys').json()['guided_journeys'])==count

def test_unit7_f5_runtime_surfaces_are_complete():
    assert client.get('/api/units/unit-7/application-lab').json()['challenge_count']==16
    assert client.get('/api/units/unit-7/review-manifest').json()['target_count']==94
    assert client.get('/api/units/unit-7/mixed-discrimination').json()['question_count']==102
    assert client.get('/api/units/unit-7/scope-guards').json()['guard_count']==25
    assert client.get('/api/units/unit-7/finalization').json()['unaccounted_records']==0
