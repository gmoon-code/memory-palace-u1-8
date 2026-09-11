import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content/ap-biology/unit-4'
client=TestClient(app)
def read(rel):return json.loads((U4/rel).read_text(encoding='utf-8'))

def test_unit4_f4a_preview_only_and_complete_j1():
    j=read('journeys/U4-J1.json')
    assert j['scene_count']==len(j['scenes'])==6
    assert j['checkpoint_count']==2
    assert j['student_release']=='DEVELOPER_PREVIEW_F4A'
    ids=[x for s in j['scenes'] for x in s['object_ids']]
    assert len(ids)==len(set(ids))==23

def test_unit4_f4a_narrative_geometry_and_continuity():
    j=read('journeys/U4-J1.json')
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=90 for z in s['scene_layout']['zones'])
        assert len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs'])))>=400
        assert s['cast'][0]['name']=='Dr. Mira Chen'
        assert any(c['name']=='Transparent route card' for c in s['cast'])

def test_unit4_f4a_journey_remains_available_in_later_preview_stages():
    d=client.get('/api/units/unit-4').json()
    assert d['student_release'] in (False,True)
    assert d['polished_journeys']>=1 and d['polished_scenes']>=6
    reg=client.get('/api/units/unit-4/journeys').json()['guided_journeys']
    assert reg and reg[0]['palace_id']=='U4-J1'
    j=client.get('/api/units/unit-4/journeys/U4-J1')
    assert j.status_code==200 and j.json()['story_title']=='The Exchange With No Addresses'

def test_unit4_f4a_object_adapter_still_serves_locked_science():
    d=client.get('/api/units/unit-4/objects/U4-K-041').json()
    assert d['memory_object_id']=='U4-K-041'
    assert d['canonical_term']=='Gap junction'
    assert 'regulated passage' in d['canonical_definition']

def test_unit4_f4a_lock_hashes():
    lock=read('content-lock-f4a.json')
    for rel,meta in lock['files'].items():
        p=U4/rel
        assert p.stat().st_size==meta['bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']
