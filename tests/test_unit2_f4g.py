import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U2=ROOT/'content'/'ap-biology'/'unit-2'; client=TestClient(app)
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_f4g_journey7_complete_and_preview_only():
    j=read(U2/'journeys/U2-J7.json')
    assert j['scene_count']==4 and j['checkpoint_count']==2 and j['student_release']=='PILOT_PREVIEW_F4G'
    assert sum(len(s['object_ids']) for s in j['scenes'])==11
    assert len({x for s in j['scenes'] for x in s['object_ids']})==11

def test_f4g_origins_story_is_substantive_and_spatially_clear():
    j=read(U2/'journeys/U2-J7.json'); counts=[]
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=90 for z in s['scene_layout']['zones'])
        n=len(re.findall(r"\b[\w’'+₂⁺⁻Ψ=-]+\b",' '.join(s['story_paragraphs']))); counts.append(n)
        assert n>=350
        assert s['cast'][0]['name']=='Dr. Nia Park' and len(s['cast'])>=4
    assert sum(counts)>=1600

def test_f4g_api_exposes_all_seven_polished_unit2_journeys():
    d=client.get('/api/units/unit-2').json()
    assert d['preview_release'] is False and d['student_release'] is True
    assert d['polished_journeys']==7 and d['polished_scenes']==49
    reg=client.get('/api/units/unit-2/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in reg]==[f'U2-J{i}' for i in range(1,8)]
    assert client.get('/api/units/unit-2/journeys/U2-J7').status_code==200
    assert client.get('/api/units/unit-2/journeys/U2-J8').status_code==404

def test_f4g_endosymbiosis_guards_are_present():
    j=read(U2/'journeys/U2-J7.json')
    whole=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).lower().replace('**','')
    assert 'no one watched the original events happen' in whole
    assert 'a plausible story is not enough' in whole
    assert 'none of the cards alone' in whole
    assert 'not generally capable of independent free-living existence' in whole
    assert 'circular dna' in whole and 'binary fission' in whole and 'ribosomes' in whole and 'double membranes' in whole

def test_f4g_all_133_palace_records_are_covered_once():
    ids=[]
    for i in range(1,8):
        j=read(U2/'journeys'/f'U2-J{i}.json')
        ids += [kid for s in j['scenes'] for kid in s['object_ids']]
    assert len(ids)==133 and len(set(ids))==133

def test_f4g_lock_hashes():
    lock=read(U2/'content-lock-f4g.json')
    for rel,digest in lock['files'].items():
        p=U2/rel; assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
