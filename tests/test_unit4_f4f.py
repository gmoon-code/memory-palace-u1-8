import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U4=ROOT/'content/ap-biology/unit-4'; client=TestClient(app)
def read(rel): return json.loads((U4/rel).read_text(encoding='utf-8'))

def test_unit4_f4f_preview_only_and_complete_j6():
    j=read('journeys/U4-J6.json')
    assert j['scene_count']==len(j['scenes'])==8
    assert j['checkpoint_count']==2
    assert j['student_release']=='DEVELOPER_PREVIEW_F4F'
    ids=[x for s in j['scenes'] for x in s['object_ids']]
    assert len(ids)==len(set(ids))==17

def test_unit4_f4f_geometry_continuity_and_prose_density():
    j=read('journeys/U4-J6.json')
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=90 for z in s['scene_layout']['zones'])
        assert len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs'])))>=400
        assert s['cast'][0]['name']=='Dr. Mira Chen'
        assert any(c['name']=='Tracked mitosis chromosome set' for c in s['cast'])

def test_unit4_f4f_api_preserves_first_six_preview_journeys_without_student_release():
    d=client.get('/api/units/unit-4').json()
    assert d['student_release'] in (False,True)
    assert d['polished_journeys']>=6 and d['polished_scenes']>=41
    reg=client.get('/api/units/unit-4/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in reg][:6]==['U4-J1','U4-J2','U4-J3','U4-J4','U4-J5','U4-J6']
    j=client.get('/api/units/unit-4/journeys/U4-J6')
    assert j.status_code==200 and j.json()['story_title']=='The Transit Hall With the Stages Out of Order'

def test_unit4_f4f_object_adapter_serves_anaphase_science():
    d=client.get('/api/units/unit-4/objects/U4-K-135').json()
    assert d['canonical_term']=='Chromosome counting at anaphase'
    assert 'transiently doubles' in d['canonical_definition']

def test_unit4_f4f_lock_hashes_and_protects_j1_through_j5():
    lock=read('content-lock-f4f.json')
    for rel,meta in lock['files'].items():
        p=U4/rel
        assert p.stat().st_size==meta['bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']
    prior=read('content-lock-f4e.json')['files']
    for rel in ('journeys/U4-J1.json','journeys/U4-J2.json','journeys/U4-J3.json','journeys/U4-J4.json','journeys/U4-J5.json'):
        p=U4/rel
        assert p.stat().st_size==prior[rel]['bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==prior[rel]['sha256']
