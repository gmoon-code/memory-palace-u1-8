import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U2=ROOT/'content'/'ap-biology'/'unit-2'; client=TestClient(app)
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_f4f_journey6_complete_and_preview_only():
    j=read(U2/'journeys/U2-J6.json')
    assert j['scene_count']==6 and j['checkpoint_count']==2 and j['student_release']=='PILOT_PREVIEW_F4F'
    assert sum(len(s['object_ids']) for s in j['scenes'])==16
    assert len({x for s in j['scenes'] for x in s['object_ids']})==16

def test_f4f_osmosis_story_is_substantive_and_spatially_clear():
    j=read(U2/'journeys/U2-J6.json')
    counts=[]
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=90 for z in s['scene_layout']['zones'])
        n=len(re.findall(r"\b[\w’'+₂⁺⁻Ψ=-]+\b",' '.join(s['story_paragraphs'])))
        counts.append(n)
        assert n>=320
        assert s['cast'][0]['name']=='Dr. Nia Park' and len(s['cast'])>=4
    assert sum(counts)>=2450

def test_f4f_api_preserves_first_six_polished_unit2_journeys():
    d=client.get('/api/units/unit-2').json()
    assert d['preview_release'] is False and d['student_release'] is True
    assert d['polished_journeys']>=6 and d['polished_scenes']>=45
    reg=client.get('/api/units/unit-2/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in reg][:6]==['U2-J1','U2-J2','U2-J3','U2-J4','U2-J5','U2-J6']
    assert client.get('/api/units/unit-2/journeys/U2-J6').status_code==200
    assert client.get('/api/units/unit-2/journeys/U2-J6').status_code==200

def test_f4f_osmosis_and_water_potential_guards_are_present():
    j=read(U2/'journeys/U2-J6.json')
    whole=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).lower().replace('**','')
    assert 'no net movement is not the same as no movement' in whole
    assert 'plasmolysis is therefore a water-loss response' in whole
    assert 'cannot always be predicted from solute concentration alone when pressure also differs' in whole
    assert 'ψ = ψp + ψs' in whole and 'ψs = −icrt' in whole
    assert 'the negative sign remains fixed' in whole

def test_f4f_lock_hashes():
    lock=read(U2/'content-lock-f4f.json')
    for rel,digest in lock['files'].items():
        p=U2/rel; assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
