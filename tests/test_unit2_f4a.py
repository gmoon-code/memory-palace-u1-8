import json, re, hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
client=TestClient(app)
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_f4a_journey1_is_complete_and_preview_only():
    j=read(U2/'journeys/U2-J1.json')
    assert j['scene_count']==len(j['scenes'])==13
    assert j['checkpoint_count']==4
    assert j['student_release']=='PILOT_PREVIEW_F4A'
    assert sum(len(s['object_ids']) for s in j['scenes'])==38
    assert len({x for s in j['scenes'] for x in s['object_ids']})==38

def test_f4a_narrative_has_clear_scene_geometry_and_substantive_prose():
    j=read(U2/'journeys/U2-J1.json')
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=55 for z in s['scene_layout']['zones'])
        assert len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs'])))>=220
        assert s['cast'][0]['name']=='Dr. Nia Park'
        assert len(s['cast'])>=3

def test_f4a_api_exposes_only_polished_unit2_journey():
    status=client.get('/api/units/unit-2')
    assert status.status_code==200
    d=status.json()
    assert d['preview_release'] is False and d['student_release'] is True
    assert d['polished_journeys']>=1 and d['polished_scenes']>=13
    reg=client.get('/api/units/unit-2/journeys').json()['guided_journeys']
    assert reg and reg[0]['palace_id']=='U2-J1'
    j=client.get('/api/units/unit-2/journeys/U2-J1')
    assert j.status_code==200 and j.json()['story_title']=='The Cell That Lost Its Routes'

def test_f4a_unit2_canonical_object_adapter_supports_recall():
    r=client.get('/api/units/unit-2/objects/U2-K-093')
    assert r.status_code==200
    d=r.json()
    assert d['memory_object_id']=='U2-K-093'
    assert 'Microtubule' in d['canonical_term']
    assert d['canonical_definition']

def test_f4a_lock_hashes():
    lock=read(U2/'content-lock-f4a.json')
    for rel,digest in lock['files'].items():
        p=U2/rel
        assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
