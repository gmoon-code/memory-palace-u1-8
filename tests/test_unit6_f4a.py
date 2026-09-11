import json,re
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]
U6=ROOT/'content'/'ap-biology'/'unit-6'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit6_f4a_journey1_accounting_and_boundary():
    j=read(U6/'journeys/U6-J1.json')
    assert j['palace_id']=='U6-J1'
    assert j['scene_count']==12 and len(j['scenes'])==12
    assert j['checkpoint_count']==3
    assert j['student_release']=='DEVELOPER_PREVIEW_F4A'
    assert j['preview_release'] is True
    assert [s['locus_id'] for s in j['scenes']]==[f'U6-L{i:02d}' for i in range(1,13)]
    assert len({kid for s in j['scenes'] for kid in s['object_ids']})==42

def test_unit6_f4a_prose_is_substantive_spatial_and_continuous():
    j=read(U6/'journeys/U6-J1.json')
    for s in j['scenes']:
        prose=' '.join(s['story_paragraphs'])
        assert len(re.findall(r"\b[\w’′'-]+\b",prose))>=450
        assert len(s['story_paragraphs'])>=5
        opening=s['story_paragraphs'][0].lower()
        assert 'left' in opening and ('ahead' in opening or 'center' in opening) and 'right' in opening
        assert len(s['cast'])>=5
        assert any(c['name']=='Dr. Sora Han' for c in s['cast'])
        assert any(c['name']=='Persistent blue-and-gold DNA duplex' for c in s['cast'])

def test_unit6_f4a_exact_targets_and_story_beat_science_match_locks():
    canon={r['knowledge_id']:r for r in read(U6/'source/canonical-unit6-f1.json')['canonical_catalog']}
    briefs={b['locus_id']:b for b in read(U6/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U6-J1'}
    j=read(U6/'journeys/U6-J1.json')
    exact=0
    for s in j['scenes']:
        text=' '.join(s['story_paragraphs']).casefold().replace('**','')
        assert s['object_ids']==briefs[s['locus_id']]['knowledge_ids']
        for beat in s['story_beats']:
            assert beat['science']==canon[beat['object_id']]['canonical_verified_statement']
            if beat['exact_name']:
                exact+=1
                assert beat['term'].casefold() in text
    assert exact==34

def test_unit6_f4a_preview_api_without_student_release():
    client=TestClient(app)
    status=client.get('/api/units/unit-6').json()
    if status['status']=='STUDENT_READY':
        assert status['student_release'] is True and status['preview_release'] is False
        assert len(client.get('/api/units/unit-6/journeys').json()['guided_journeys'])==6
        assert client.get('/api/units/unit-6/journeys/U6-J1').status_code==200
        assert client.get('/api/units/unit-6/application-lab').json()['challenge_count']==16
    else:
        assert status['student_release'] is False and status['preview_release'] is True
        assert client.get('/api/units/unit-6/journeys').json()['guided_journeys']==[]
        assert client.get('/api/units/unit-6/journeys/U6-J1').status_code==404
        assert client.get('/api/units/unit-6/application-lab').json()['challenge_count']==0
