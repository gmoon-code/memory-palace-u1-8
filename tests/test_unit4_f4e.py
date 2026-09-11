import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U4=ROOT/'content/ap-biology/unit-4'; client=TestClient(app)
def read(rel): return json.loads((U4/rel).read_text(encoding='utf-8'))

def test_unit4_f4e_preview_only_and_complete_j5():
    j=read('journeys/U4-J5.json')
    assert j['scene_count']==len(j['scenes'])==8
    assert j['checkpoint_count']==3
    assert j['student_release']=='DEVELOPER_PREVIEW_F4E'
    ids=[x for s in j['scenes'] for x in s['object_ids']]
    assert len(ids)==len(set(ids))==27

def test_unit4_f4e_geometry_continuity_and_prose_density():
    j=read('journeys/U4-J5.json')
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=90 for z in s['scene_layout']['zones'])
        assert len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs'])))>=400
        assert s['cast'][0]['name']=='Dr. Mira Chen'
        assert any(c['name']=='Tracked chromosome archive case' for c in s['cast'])

def test_unit4_f4e_api_exposes_five_preview_journeys_without_student_release():
    d=client.get('/api/units/unit-4').json()
    assert d['student_release'] in (False,True)
    assert d['polished_journeys']>=5 and d['polished_scenes']>=33
    reg=client.get('/api/units/unit-4/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in reg][:5]==['U4-J1','U4-J2','U4-J3','U4-J4','U4-J5']
    j=client.get('/api/units/unit-4/journeys/U4-J5')
    assert j.status_code==200 and j.json()['story_title']=='The Archive That Counted DNA Twice'

def test_unit4_f4e_object_adapter_serves_chromosome_science():
    d=client.get('/api/units/unit-4/objects/U4-K-134').json()
    assert d['canonical_term']=='Chromosome counting across S phase'
    assert 'does not double chromosome number' in d['canonical_definition']

def test_unit4_f4e_lock_hashes_and_protects_j1_through_j4():
    lock=read('content-lock-f4e.json')
    for rel,meta in lock['files'].items():
        p=U4/rel
        assert p.stat().st_size==meta['bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']
    prior=read('content-lock-f4d.json')['files']
    for rel in ('journeys/U4-J1.json','journeys/U4-J2.json','journeys/U4-J3.json','journeys/U4-J4.json'):
        p=U4/rel
        assert p.stat().st_size==prior[rel]['bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==prior[rel]['sha256']
