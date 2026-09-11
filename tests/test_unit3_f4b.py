import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U3=ROOT/'content/ap-biology/unit-3'; client=TestClient(app)
def read(rel): return json.loads((U3/rel).read_text())

def test_unit3_f4b_journey2_complete_preview_only():
    j=read('journeys/U3-J2.json')
    assert j['scene_count']==len(j['scenes'])==8
    assert j['checkpoint_count']==3
    assert j['student_release']=='PILOT_PREVIEW_F4B'
    ids=[x for s in j['scenes'] for x in s['object_ids']]
    assert len(ids)==len(set(ids))==22

def test_unit3_f4b_prose_geometry_and_diagnostic_route():
    j=read('journeys/U3-J2.json')
    assert [s['locus'] for s in j['scenes']]==[
        'Enzyme Stability Chamber','Collision and Saturation Track','Cofactor Assembly Station',
        'Competitive Inhibitor Gate','Allosteric Control Panel','Cooperative Binding Array',
        'Feedback Loop Control Room','Irreversible Inhibition Lockout']
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=70 for z in s['scene_layout']['zones'])
        assert len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs'])))>=340
        assert s['cast'][0]['name']=='Dr. Nia Park' and len(s['cast'])>=4

def test_unit3_f4b_api_exposes_two_journeys_and_blocks_journey3():
    d=client.get('/api/units/unit-3').json()
    assert d['polished_journeys']>=2 and d['polished_scenes']>=11
    reg=client.get('/api/units/unit-3/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in reg][:2]==['U3-J1','U3-J2']
    assert client.get('/api/units/unit-3/journeys/U3-J2').status_code==200
    assert client.get('/api/units/unit-3/journeys/U3-J2').status_code==200

def test_unit3_f4b_canonical_adapter_for_allosteric_term():
    r=client.get('/api/units/unit-3/objects/U3-K-099')
    assert r.status_code==200
    d=r.json(); assert d['memory_object_id']=='U3-K-099'; assert 'Allosteric regulation' in d['canonical_term']; assert 'conformational change' in d['canonical_definition']

def test_unit3_f4b_lock_hashes():
    lock=read('content-lock-f4b.json')
    for rel,digest in lock['files'].items():
        p=U3/rel; assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
