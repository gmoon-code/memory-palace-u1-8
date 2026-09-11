import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U2=ROOT/'content'/'ap-biology'/'unit-2'; client=TestClient(app)
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_f4e_journey5_complete_and_preview_only():
    j=read(U2/'journeys/U2-J5.json')
    assert j['scene_count']==10 and j['checkpoint_count']==3 and j['student_release']=='PILOT_PREVIEW_F4E'
    assert sum(len(s['object_ids']) for s in j['scenes'])==26
    assert len({x for s in j['scenes'] for x in s['object_ids']})==26

def test_f4e_transport_story_is_substantive_and_spatially_clear():
    j=read(U2/'journeys/U2-J5.json')
    counts=[]
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=90 for z in s['scene_layout']['zones'])
        n=len(re.findall(r"\b[\w’'+₂⁺⁻-]+\b",' '.join(s['story_paragraphs'])))
        counts.append(n)
        assert n>=300
        assert s['cast'][0]['name']=='Dr. Nia Park' and len(s['cast'])>=4
    assert sum(counts)>=3500

def test_f4e_api_preserves_first_five_polished_unit2_journeys():
    d=client.get('/api/units/unit-2').json()
    assert d['preview_release'] is False and d['student_release'] is True
    assert d['polished_journeys']>=5 and d['polished_scenes']>=39
    reg=client.get('/api/units/unit-2/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in reg[:5]]==['U2-J1','U2-J2','U2-J3','U2-J4','U2-J5']
    assert client.get('/api/units/unit-2/journeys/U2-J5').status_code==200

def test_f4e_transport_guards_are_present():
    j=read(U2/'journeys/U2-J5.json')
    whole=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).lower().replace('**','')
    assert 'motion has not stopped' in whole
    assert 'carrier never forms an open tunnel' in whole
    assert 'water can cross a lipid bilayer to some extent' in whole
    assert '3 na⁺ out' in whole and '2 k⁺ in' in whole
    assert 'atp is not hydrolyzed directly at the sucrose symporter' in whole

def test_f4e_lock_hashes():
    lock=read(U2/'content-lock-f4e.json')
    for rel,digest in lock['files'].items():
        p=U2/rel; assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
