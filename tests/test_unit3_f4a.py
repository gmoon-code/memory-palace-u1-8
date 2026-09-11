import json, re, hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content/ap-biology/unit-3'
client=TestClient(app)
def read(rel): return json.loads((U3/rel).read_text())

def test_unit3_f4a_journey1_complete_preview_only():
    j=read('journeys/U3-J1.json')
    assert j['scene_count']==len(j['scenes'])==3
    assert j['checkpoint_count']==2
    assert j['student_release']=='PILOT_PREVIEW_F4A'
    ids=[x for s in j['scenes'] for x in s['object_ids']]
    assert len(ids)==len(set(ids))==11

def test_unit3_f4a_prose_and_geometry():
    j=read('journeys/U3-J1.json')
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=70 for z in s['scene_layout']['zones'])
        assert len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs'])))>=350
        assert s['cast'][0]['name']=='Dr. Nia Park'

def test_unit3_f4a_api_preserves_journey1_in_later_previews():
    d=client.get('/api/units/unit-3').json()
    assert d['polished_journeys']>=1 and d['polished_scenes']>=3
    reg=client.get('/api/units/unit-3/journeys').json()['guided_journeys']
    assert reg and reg[0]['palace_id']=='U3-J1'
    j=client.get('/api/units/unit-3/journeys/U3-J1')
    assert j.status_code==200 and j.json()['story_title']=='The Reaction That Would Not Start'

def test_unit3_f4a_object_adapter_supports_recall():
    r=client.get('/api/units/unit-3/objects/U3-K-085')
    assert r.status_code==200
    d=r.json(); assert d['memory_object_id']=='U3-K-085'; assert d['canonical_term']=='Active site'; assert 'compatible substrate binds' in d['canonical_definition']

def test_unit3_f4a_lock_hashes():
    lock=read('content-lock-f4a.json')
    for rel,digest in lock['files'].items():
        p=U3/rel; assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
