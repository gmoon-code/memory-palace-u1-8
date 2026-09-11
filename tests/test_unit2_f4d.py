import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U2=ROOT/'content'/'ap-biology'/'unit-2'; client=TestClient(app)
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_f4d_journey4_complete_and_preview_only():
    j=read(U2/'journeys/U2-J4.json')
    assert j['scene_count']==8 and j['checkpoint_count']==3 and j['student_release']=='PILOT_PREVIEW_F4D'
    assert sum(len(s['object_ids']) for s in j['scenes'])==21
    assert len({x for s in j['scenes'] for x in s['object_ids']})==21

def test_f4d_membrane_story_is_substantive_and_spatially_clear():
    j=read(U2/'journeys/U2-J4.json')
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=85 for z in s['scene_layout']['zones'])
        assert len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs'])))>=320
        assert s['cast'][0]['name']=='Dr. Nia Park' and len(s['cast'])>=4

def test_f4d_api_preserves_first_four_polished_journeys():
    d=client.get('/api/units/unit-2').json()
    assert d['preview_release'] is False and d['student_release'] is True
    assert d['polished_journeys']>=4 and d['polished_scenes']>=29
    reg=client.get('/api/units/unit-2/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in reg[:4]]==['U2-J1','U2-J2','U2-J3','U2-J4']
    assert client.get('/api/units/unit-2/journeys/U2-J4').status_code==200

def test_f4d_canonical_adapter_for_integral_membrane_protein():
    r=client.get('/api/units/unit-2/objects/U2-K-101')
    assert r.status_code==200 and 'Integral membrane protein' in r.json()['canonical_term'] and 'some, but not all' in r.json()['canonical_definition']

def test_f4d_lock_hashes():
    lock=read(U2/'content-lock-f4d.json')
    for rel,digest in lock['files'].items():
        p=U2/rel; assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
