import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U4=ROOT/'content/ap-biology/unit-4'; client=TestClient(app)
def read(rel): return json.loads((U4/rel).read_text(encoding='utf-8'))

def test_unit4_f4d_preview_only_and_complete_j4():
    j=read('journeys/U4-J4.json')
    assert j['scene_count']==len(j['scenes'])==6
    assert j['checkpoint_count']==2
    assert j['student_release']=='DEVELOPER_PREVIEW_F4D'
    ids=[x for s in j['scenes'] for x in s['object_ids']]
    assert len(ids)==len(set(ids))==18

def test_unit4_f4d_geometry_gauge_and_prose_density():
    j=read('journeys/U4-J4.json')
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=90 for z in s['scene_layout']['zones'])
        assert len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs'])))>=400
        assert s['cast'][0]['name']=='Dr. Mira Chen'
        assert any(c['name']=='Regulated-variable gauge' for c in s['cast'])

def test_unit4_f4d_api_exposes_four_preview_journeys_without_student_release():
    d=client.get('/api/units/unit-4').json()
    assert d['student_release'] in (False,True)
    assert d['polished_journeys']>=4 and d['polished_scenes']>=25
    reg=client.get('/api/units/unit-4/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in reg][:4]==['U4-J1','U4-J2','U4-J3','U4-J4']
    j=client.get('/api/units/unit-4/journeys/U4-J4')
    assert j.status_code==200 and j.json()['story_title']=='The Control Room That Forgot Which Way to Push'

def test_unit4_f4d_object_adapter_serves_feedback_science():
    d=client.get('/api/units/unit-4/objects/U4-K-019').json()
    assert d['canonical_term']=='Negative feedback'
    assert 'reduces the initial stimulus' in d['canonical_definition']

def test_unit4_f4d_lock_hashes_and_protects_j1_j2_j3():
    lock=read('content-lock-f4d.json')
    for rel,meta in lock['files'].items():
        p=U4/rel
        assert p.stat().st_size==meta['bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']
    prior=read('content-lock-f4c.json')['files']
    for rel in ('journeys/U4-J1.json','journeys/U4-J2.json','journeys/U4-J3.json'):
        p=U4/rel
        assert p.stat().st_size==prior[rel]['bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==prior[rel]['sha256']
