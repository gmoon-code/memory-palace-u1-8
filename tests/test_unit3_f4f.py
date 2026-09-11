import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U3=ROOT/'content/ap-biology/unit-3'; client=TestClient(app)
def read(rel): return json.loads((U3/rel).read_text())

def test_unit3_f4f_journey6_complete_preview_only():
    j=read('journeys/U3-J6.json')
    assert j['scene_count']==len(j['scenes'])==12
    assert j['checkpoint_count']==3
    assert j['student_release']=='PILOT_PREVIEW_F4F'
    ids=[x for s in j['scenes'] for x in s['object_ids']]
    assert len(ids)==len(set(ids))==35

def test_unit3_f4f_prose_geometry_and_respiration_route():
    j=read('journeys/U3-J6.json')
    assert [s['locus'] for s in j['scenes']]==[
        'Respiration Fuel Intake','Glycolysis Floor','Electron Carrier Charging Bay','Pyruvate Oxidation Airlock',
        'Citric Acid Cycle Chamber','Mitochondrial Architecture Bay','Respiratory Electron-Transport Descent',
        'Proton Pumping Wall','Oxygen Terminal-Acceptor Basin','Oxidative-Phosphorylation Turbine',
        'Uncoupling Heat Vent','Prokaryotic Respiratory Membrane']
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=95 for z in s['scene_layout']['zones'])
        assert len(re.findall(r"\b[\w’'₂₄⁺⁻-]+\b",' '.join(s['story_paragraphs'])))>=350
        assert s['cast'][0]['name']=='Dr. Nia Park' and len(s['cast'])>=4

def test_unit3_f4f_first_six_journeys_remain_intact_in_later_previews():
    reg=client.get('/api/units/unit-3/journeys').json()['guided_journeys']
    ids=[x['palace_id'] for x in reg]
    assert ids[:6]==['U3-J1','U3-J2','U3-J3','U3-J4','U3-J5','U3-J6']
    assert client.get('/api/units/unit-3/journeys/U3-J6').status_code==200
    f4f=read('journeys-f4f.json')['guided_journeys']
    assert [x['palace_id'] for x in f4f]==['U3-J1','U3-J2','U3-J3','U3-J4','U3-J5','U3-J6']

def test_unit3_f4f_key_respiration_guards():
    j=read('journeys/U3-J6.json')
    gly=' '.join(j['scenes'][1]['story_paragraphs']).lower()
    carrier=' '.join(j['scenes'][2]['story_paragraphs']).lower()
    pump=' '.join(j['scenes'][7]['story_paragraphs']).lower()
    o2=' '.join(j['scenes'][8]['story_paragraphs']).lower()
    turbine=' '.join(j['scenes'][9]['story_paragraphs']).lower()
    prok=' '.join(j['scenes'][11]['story_paragraphs']).lower()
    assert 'no co₂ vent opens here' in gly
    assert 'not a claim that glycolysis just produced fadh₂' in carrier
    assert 'electrons are not pumped into the intermembrane space' in pump
    assert 'oxygen does not donate atp' in o2
    assert 'the protons do not become phosphate groups or atp molecules' in turbine
    assert 'does not show a fixed universal integer' in turbine
    assert 'no mitochondrial organelle' in prok

def test_unit3_f4f_lock_hashes():
    lock=read('content-lock-f4f.json')
    for rel,digest in lock['files'].items():
        p=U3/rel; assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
