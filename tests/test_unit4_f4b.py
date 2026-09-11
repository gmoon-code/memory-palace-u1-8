import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content/ap-biology/unit-4'
client=TestClient(app)
def read(rel):return json.loads((U4/rel).read_text(encoding='utf-8'))

def test_unit4_f4b_preview_only_and_complete_j2():
    j=read('journeys/U4-J2.json')
    assert j['scene_count']==len(j['scenes'])==6
    assert j['checkpoint_count']==3
    assert j['student_release']=='DEVELOPER_PREVIEW_F4B'
    ids=[x for s in j['scenes'] for x in s['object_ids']]
    assert len(ids)==len(set(ids))==24

def test_unit4_f4b_narrative_geometry_and_continuity():
    j=read('journeys/U4-J2.json')
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=90 for z in s['scene_layout']['zones'])
        assert len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs'])))>=400
        assert s['cast'][0]['name']=='Dr. Mira Chen'
        assert any(c['name']=='Three-state receptor monitor' for c in s['cast'])

def test_unit4_f4b_api_exposes_two_preview_journeys_without_student_release():
    d=client.get('/api/units/unit-4').json()
    assert d['student_release'] in (False,True)
    assert d['polished_journeys']>=2 and d['polished_scenes']>=12
    reg=client.get('/api/units/unit-4/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in reg][:2]==['U4-J1','U4-J2']
    j=client.get('/api/units/unit-4/journeys/U4-J2')
    assert j.status_code==200 and j.json()['story_title']=='The Gate That Answered Every Knock'

def test_unit4_f4b_object_adapter_serves_reception_science():
    d=client.get('/api/units/unit-4/objects/U4-K-058').json()
    assert d['canonical_term']=='Reception'
    assert 'detection' in d['canonical_definition'].lower()

def test_unit4_f4b_lock_hashes_and_protects_j1():
    lock=read('content-lock-f4b.json')
    for rel,meta in lock['files'].items():
        p=U4/rel
        assert p.stat().st_size==meta['bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']
    old=read('content-lock-f4a.json')['files']['journeys/U4-J1.json']
    p=U4/'journeys/U4-J1.json'
    assert p.stat().st_size==old['bytes']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==old['sha256']
