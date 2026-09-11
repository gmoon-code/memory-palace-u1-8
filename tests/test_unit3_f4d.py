import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U3=ROOT/'content/ap-biology/unit-3'; client=TestClient(app)
def read(rel): return json.loads((U3/rel).read_text())

def test_unit3_f4d_journey4_complete_preview_only():
    j=read('journeys/U3-J4.json')
    assert j['scene_count']==len(j['scenes'])==12
    assert j['checkpoint_count']==4
    assert j['student_release']=='PILOT_PREVIEW_F4D'
    ids=[x for s in j['scenes'] for x in s['object_ids']]
    assert len(ids)==len(set(ids))==44

def test_unit3_f4d_prose_geometry_and_photosynthetic_route():
    j=read('journeys/U3-J4.json')
    assert [s['locus'] for s in j['scenes']]==[
        'Carbon Strategy Entrance','Oxygenation Timeline','Leaf Gas-Exchange Balcony','Chloroplast Compartment Gallery',
        'Photosynthesis Redox Board','Photon and Wavelength Prism','Pigment Spectrum Bench','Photosystem Antenna Theater',
        'Photosystem II Water Splitter','Thylakoid Electron-Transport Bridge','Photosystem I NADPH Station','Photophosphorylation Turbine']
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=70 for z in s['scene_layout']['zones'])
        assert len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs'])))>=350
        assert s['cast'][0]['name']=='Dr. Nia Park' and len(s['cast'])>=4

def test_unit3_f4d_api_preserves_first_four_journeys_in_later_previews():
    d=client.get('/api/units/unit-3').json()
    assert d['polished_journeys']>=4 and d['polished_scenes']>=33
    reg=client.get('/api/units/unit-3/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in reg][:4]==['U3-J1','U3-J2','U3-J3','U3-J4']
    assert client.get('/api/units/unit-3/journeys/U3-J4').status_code==200

def test_unit3_f4d_key_photosynthesis_guards():
    j=read('journeys/U3-J4.json')
    redox=' '.join(j['scenes'][4]['story_paragraphs']).lower()
    antenna=' '.join(j['scenes'][7]['story_paragraphs']).lower()
    psii=' '.join(j['scenes'][8]['story_paragraphs']).lower()
    psi=' '.join(j['scenes'][10]['story_paragraphs']).lower()
    turbine=' '.join(j['scenes'][11]['story_paragraphs']).lower()
    assert 'photosynthetic oxygen comes from water' in redox
    assert 'same electron is not passed from antenna pigment to antenna pigment' in antenna
    assert 'water-splitting products' in psii and 'thylakoid lumen' in psii
    assert 'p680' in psi and 'p700' in psi and 'not additional photosystems' in psi
    assert 'a photon is not about to spin this enzyme' in turbine
    assert 'electrochemical proton gradient' in turbine

def test_unit3_f4d_lock_hashes():
    lock=read('content-lock-f4d.json')
    for rel,digest in lock['files'].items():
        p=U3/rel; assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
