import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U2=ROOT/'content'/'ap-biology'/'unit-2'; client=TestClient(app)
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_f4b_journey2_complete_and_preview_only():
    j=read(U2/'journeys/U2-J2.json')
    assert j['scene_count']==5 and j['checkpoint_count']==2 and j['student_release']=='PILOT_PREVIEW_F4B'
    assert sum(len(s['object_ids']) for s in j['scenes'])==12
    assert len({x for s in j['scenes'] for x in s['object_ids']})==12

def test_f4b_journey2_scene_quality():
    j=read(U2/'journeys/U2-J2.json')
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs'])))>=280
        assert s['cast'][0]['name']=='Dr. Nia Park' and len(s['cast'])>=3

def test_f4b_api_exposes_two_polished_unit2_journeys_only():
    d=client.get('/api/units/unit-2').json()
    assert d['preview_release'] is False and d['student_release'] is True
    assert d['polished_journeys']>=2 and d['polished_scenes']>=18
    reg=client.get('/api/units/unit-2/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in reg[:2]]==['U2-J1','U2-J2']
    assert client.get('/api/units/unit-2/journeys/U2-J2').status_code==200
    assert client.get('/api/units/unit-2/journeys/U2-J2').status_code==200

def test_f4b_canonical_adapter_for_chloroplast_term():
    r=client.get('/api/units/unit-2/objects/U2-K-089')
    assert r.status_code==200 and 'Granum' in r.json()['canonical_term'] and r.json()['canonical_definition']

def test_f4b_lock_hashes():
    lock=read(U2/'content-lock-f4b.json')
    for rel,digest in lock['files'].items():
        p=U2/rel; assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
