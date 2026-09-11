import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U3=ROOT/'content/ap-biology/unit-3'; client=TestClient(app)
def read(rel): return json.loads((U3/rel).read_text())

def test_unit3_f4g_journey7_complete_preview_only():
    j=read('journeys/U3-J7.json')
    assert j['scene_count']==len(j['scenes'])==4
    assert j['checkpoint_count']==1
    assert j['student_release']=='PILOT_PREVIEW_F4G'
    ids=[x for s in j['scenes'] for x in s['object_ids']]
    assert len(ids)==len(set(ids))==11

def test_unit3_f4g_prose_geometry_and_route():
    j=read('journeys/U3-J7.json')
    assert [s['locus'] for s in j['scenes']]==['Respiration Across Life Junction','Fermentation NAD⁺ Recycling Gate','Alcohol Fermentation Vat','Lactate Fermentation Track']
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=95 for z in s['scene_layout']['zones'])
        assert len(re.findall(r"\b[\w’'⁺₂-]+\b",' '.join(s['story_paragraphs'])))>=350
        assert s['cast'][0]['name']=='Dr. Nia Park' and len(s['cast'])>=4

def test_unit3_f4g_all_seven_journeys_remain_intact_in_later_release():
    reg=client.get('/api/units/unit-3/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in reg][:7]==[f'U3-J{i}' for i in range(1,8)]
    for i in range(1,8): assert client.get(f'/api/units/unit-3/journeys/U3-J{i}').status_code==200
    f4g=read('journeys-f4g.json')['guided_journeys']
    assert [x['palace_id'] for x in f4g]==[f'U3-J{i}' for i in range(1,8)]

def test_unit3_f4g_key_fermentation_guards():
    j=read('journeys/U3-J7.json')
    junction=' '.join(j['scenes'][0]['story_paragraphs']).lower()
    gate=' '.join(j['scenes'][1]['story_paragraphs']).lower()
    alcohol=' '.join(j['scenes'][2]['story_paragraphs']).lower()
    lactate=' '.join(j['scenes'][3]['story_paragraphs']).lower()
    assert 'anaerobic respiration' in junction and 'still uses an etc' in junction
    assert 'fermentation takes a different route' in junction
    assert 'without using an electron-transport chain' in gate
    assert 'does not provide a large extra atp harvest' in gate
    assert 'some cells can run fermentation even when oxygen is present' in gate
    assert 'acetaldehyde' in alcohol and 'atp display still does not jump upward' in alcohol
    assert 'oxygen is present' in lactate
    assert 'not the cause of the acute burning sensation' in lactate
    assert 'not the cause of delayed-onset muscle soreness' in lactate
    assert 'transportable metabolic intermediate' in lactate

def test_unit3_f4g_lock_hashes():
    lock=read('content-lock-f4g.json')
    for rel,digest in lock['files'].items():
        p=U3/rel; assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
