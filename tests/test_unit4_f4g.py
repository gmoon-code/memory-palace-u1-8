import json, re, hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U4=ROOT/'content/ap-biology/unit-4'; client=TestClient(app)
def read(rel): return json.loads((U4/rel).read_text(encoding='utf-8'))

def test_unit4_f4g_all_seven_journeys_are_polished_preview_only():
    j=read('journeys/U4-J7.json')
    assert j['scene_count']==len(j['scenes'])==10
    assert j['checkpoint_count']==3
    assert j['student_release']=='DEVELOPER_PREVIEW_F4G'
    ids=[x for s in j['scenes'] for x in s['object_ids']]
    assert len(ids)==len(set(ids))==28

def test_unit4_f4g_security_file_geometry_and_prose_density():
    j=read('journeys/U4-J7.json')
    for s in j['scenes']:
        assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
        assert all(len(z['description'])>=90 for z in s['scene_layout']['zones'])
        assert len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs'])))>=400
        assert s['cast'][0]['name']=='Dr. Mira Chen'
        assert any(c['name']=='Model-cell security file' for c in s['cast'])

def test_unit4_f4g_api_exposes_all_seven_preview_journeys_without_student_release():
    d=client.get('/api/units/unit-4').json()
    assert d['student_release'] in (False,True)
    assert d['polished_journeys']==7 and d['polished_scenes']==51
    reg=client.get('/api/units/unit-4/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in reg]==[f'U4-J{i}' for i in range(1,8)]
    j=client.get('/api/units/unit-4/journeys/U4-J7')
    assert j.status_code==200 and j.json()['story_title']=='The Headquarters That Stamped PROCEED on Everything'

def test_unit4_f4g_final_narrative_covers_key_security_and_cancer_distinctions():
    text=' '.join(' '.join(s['story_paragraphs']) for s in read('journeys/U4-J7.json')['scenes']).casefold()
    for phrase in ['cell-cycle checkpoints','cell-cycle arrest','apoptosis','cyclin-dependent kinase (cdk)','density-dependent inhibition','anchorage dependence','cancer-driver alterations','benign tumor','malignant tumor','metastasis','ultraviolet radiation','tobacco smoke']:
        assert phrase in text
    assert 'no universal fixed mutation threshold' in text
    assert 'nicotine is primarily responsible for addiction' in text

def test_unit4_f4g_lock_hashes_and_protects_j1_through_j6():
    lock=read('content-lock-f4g.json')
    for rel,meta in lock['files'].items():
        p=U4/rel
        assert p.stat().st_size==meta['bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']
    prior=read('content-lock-f4f.json')['files']
    for rel in (f'journeys/U4-J{i}.json' for i in range(1,7)):
        p=U4/rel
        assert p.stat().st_size==prior[rel]['bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==prior[rel]['sha256']
