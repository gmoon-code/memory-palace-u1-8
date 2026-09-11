import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U3=ROOT/'content/ap-biology/unit-3'; client=TestClient(app)
def read(rel): return json.loads((U3/rel).read_text())

def test_unit3_f4e_journey5_complete_preview_only():
    j=read('journeys/U3-J5.json')
    assert j['scene_count']==len(j['scenes'])==5
    assert j['checkpoint_count']==2
    assert j['student_release']=='PILOT_PREVIEW_F4E'
    ids=[x for s in j['scenes'] for x in s['object_ids']]
    assert len(ids)==len(set(ids))==11

def test_unit3_f4e_prose_geometry_and_carbon_route():
    j=read('journeys/U3-J5.json')
    assert [s['locus'] for s in j['scenes']]==[
      'Calvin Cycle Energy Dock','Carbon Fixation Bench','G3P Output and Regeneration Loop',
      'Photorespiration Detour','C4 and CAM Strategy Conservatory']
    counts=[]
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=90 for z in s['scene_layout']['zones'])
        n=len(re.findall(r"\b[\w’'₂₄⁺⁻-]+\b",' '.join(s['story_paragraphs'])))
        counts.append(n); assert n>=390
        assert s['cast'][0]['name']=='Dr. Nia Park' and len(s['cast'])>=4
    assert sum(counts)>=2100

def test_unit3_f4e_api_preserves_first_five_journeys_in_later_previews():
    d=client.get('/api/units/unit-3').json()
    assert d['polished_journeys']>=5 and d['polished_scenes']>=38
    reg=client.get('/api/units/unit-3/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in reg][:5]==['U3-J1','U3-J2','U3-J3','U3-J4','U3-J5']
    assert client.get('/api/units/unit-3/journeys/U3-J5').status_code==200

def test_unit3_f4e_key_calvin_and_adaptation_guards():
    j=read('journeys/U3-J5.json')
    energy=' '.join(j['scenes'][0]['story_paragraphs']).lower()
    fixation=' '.join(j['scenes'][1]['story_paragraphs']).lower()
    g3p=' '.join(j['scenes'][2]['story_paragraphs']).lower()
    photo=' '.join(j['scenes'][3]['story_paragraphs']).lower()
    adaptations=' '.join(j['scenes'][4]['story_paragraphs']).lower()
    assert 'neither token contains the carbon' in energy
    assert 'rubisco is not itself the carbon acceptor' in fixation
    assert 'not a synonym for glucose' in g3p
    assert 'photorespiration' in photo and 'mitochondrial process of cellular respiration' in photo
    assert 'c4 = spatial separation. cam = temporal separation.' in adaptations

def test_unit3_f4e_lock_hashes():
    lock=read('content-lock-f4e.json')
    for rel,digest in lock['files'].items():
        p=U3/rel; assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
