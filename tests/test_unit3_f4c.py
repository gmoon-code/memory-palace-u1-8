import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U3=ROOT/'content/ap-biology/unit-3'; client=TestClient(app)
def read(rel): return json.loads((U3/rel).read_text())

def test_unit3_f4c_journey3_complete_preview_only():
    j=read('journeys/U3-J3.json')
    assert j['scene_count']==len(j['scenes'])==10
    assert j['checkpoint_count']==3
    assert j['student_release']=='PILOT_PREVIEW_F4C'
    ids=[x for s in j['scenes'] for x in s['object_ids']]
    assert len(ids)==len(set(ids))==37

def test_unit3_f4c_prose_geometry_and_energy_route():
    j=read('journeys/U3-J3.json')
    assert [s['locus'] for s in j['scenes']]==[
        'Metabolism Route Map','Energy Forms Gallery','First-Law Ledger','Entropy and Living Order Chamber',
        'Free-Energy Terrain','Cellular Work Dock','ATP Structure Station','ATP Hydrolysis Forge',
        'ATP Regeneration Wheel','Conserved Metabolism Archive']
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=70 for z in s['scene_layout']['zones'])
        assert len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs'])))>=340
        assert s['cast'][0]['name']=='Dr. Nia Park' and len(s['cast'])>=4

def test_unit3_f4c_api_preserves_first_three_journeys_in_later_previews():
    d=client.get('/api/units/unit-3').json()
    assert d['polished_journeys']>=3 and d['polished_scenes']>=21
    reg=client.get('/api/units/unit-3/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in reg][:3]==['U3-J1','U3-J2','U3-J3']
    assert client.get('/api/units/unit-3/journeys/U3-J3').status_code==200
    assert client.get('/api/units/unit-3/journeys/U3-J3').status_code==200

def test_unit3_f4c_atp_hydrolysis_guard_and_scope_guard():
    j=read('journeys/U3-J3.json')
    hydro=' '.join(j['scenes'][7]['story_paragraphs']).lower()
    terrain=' '.join(j['scenes'][4]['story_paragraphs']).lower()
    assert 'energy is required to break chemical bonds' in hydro
    assert 'not from energy released by breaking a phosphate bond itself' in hydro
    assert 'full gibbs free-energy equation' in terrain

def test_unit3_f4c_lock_hashes():
    lock=read('content-lock-f4c.json')
    for rel,digest in lock['files'].items():
        p=U3/rel; assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
