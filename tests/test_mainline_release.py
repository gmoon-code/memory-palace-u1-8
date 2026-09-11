from fastapi.testclient import TestClient
from backend.main import app
client=TestClient(app)

def test_mainline_has_eight_student_ready_units():
    units=client.get('/api/course').json()['units']
    ready=[u['unit_id'] for u in units if u['status']=='STUDENT_READY']
    assert ready==['unit-1','unit-2','unit-3','unit-4','unit-5','unit-6','unit-7','unit-8']

def test_mainline_runtime_version_is_u8_f6():
    assert client.get('/api/health').json()['version']=='v2-apbio-0.30.0-u8-f6'

def test_all_student_ready_journey_counts():
    assert len(client.get('/api/units/unit-1/journeys').json()['guided_journeys'])==9
    assert len(client.get('/api/units/unit-2/journeys').json()['guided_journeys'])==7
    assert len(client.get('/api/units/unit-3/journeys').json()['guided_journeys'])==7
    assert len(client.get('/api/units/unit-4/journeys').json()['guided_journeys'])==7
    assert len(client.get('/api/units/unit-5/journeys').json()['guided_journeys'])==8
    assert len(client.get('/api/units/unit-6/journeys').json()['guided_journeys'])==6
    assert len(client.get('/api/units/unit-7/journeys').json()['guided_journeys'])==6
    assert len(client.get('/api/units/unit-8/journeys').json()['guided_journeys'])==8
