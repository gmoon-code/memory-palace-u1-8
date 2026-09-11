import json,re
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content'/'ap-biology'/'unit-7'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit7_f4a_journey1_accounting_and_boundary():
    j=read(U7/'journeys/U7-J1.json')
    assert j['palace_id']=='U7-J1'
    assert j['scene_count']==10 and len(j['scenes'])==10
    assert j['checkpoint_count']==3
    assert j['student_release']=='DEVELOPER_PREVIEW_F4A'
    assert j['preview_release'] is True
    assert [s['locus_id'] for s in j['scenes']]==[f'U7-L{i:02d}' for i in range(1,11)]
    assert len({kid for s in j['scenes'] for kid in s['object_ids']})==26

def test_unit7_f4a_prose_is_substantive_spatial_and_continuous():
    j=read(U7/'journeys/U7-J1.json')
    continuity=j['scenes'][0]['continuity_object']
    for s in j['scenes']:
        prose=' '.join(s['story_paragraphs'])
        assert len(re.findall(r"\b[\w’′'-]+\b",prose))>=450
        assert len(s['story_paragraphs'])>=6
        opening=s['story_paragraphs'][0].lower()
        assert 'left' in opening and ('ahead' in opening or 'center' in opening) and 'right' in opening
        assert len(s['cast'])>=5
        assert any(c['name']=='Dr. Imani Vale' for c in s['cast'])
        assert any(c['name']=='Transparent population ledger' for c in s['cast'])
        assert s['continuity_object']==continuity
        assert '—' not in prose and ': ' not in prose

def test_unit7_f4a_exact_targets_and_story_beat_science_match_locks():
    canon={r['knowledge_id']:r for r in read(U7/'source/canonical-unit7-f1.json')['canonical_catalog']}
    briefs={b['locus_id']:b for b in read(U7/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U7-J1'}
    j=read(U7/'journeys/U7-J1.json')
    exact=0
    for s in j['scenes']:
        text=' '.join(s['story_paragraphs']).casefold().replace('**','')
        assert s['object_ids']==briefs[s['locus_id']]['knowledge_ids']
        for beat in s['story_beats']:
            assert beat['science']==canon[beat['object_id']]['canonical_verified_statement']
            if beat['exact_name']:
                exact+=1
                assert beat['term'].casefold() in text
    assert exact==15

def test_unit7_f4a_high_risk_misconceptions_are_explicitly_blocked():
    j=read(U7/'journeys/U7-J1.json')
    text=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
    for phrase in [
        'individual organism does not genetically evolve during its lifetime',
        'variation is already present',
        'environment did not create the needed beak',
        'reproductive success relative to others',
        'origin of mutation is random with respect to fitness',
        'not a statement that sickle-cell disease itself is beneficial',
        'mate choice and competition among potential mates',
        'human selective breeding can change variation and trait frequencies',
    ]:
        assert phrase in text

def test_unit7_f4a_preview_is_not_public_student_runtime():
    client=TestClient(app)
    status=client.get('/api/units/unit-7').json()
    assert status['status'] in {'F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
    if status['status']=='STUDENT_READY':
        assert status['student_release'] is True and status['preview_release'] is False
        assert len(client.get('/api/units/unit-7/journeys').json()['guided_journeys'])==6
    else:
        assert status['student_release'] is False and status['preview_release'] is True
        assert client.get('/api/units/unit-7/journeys').json()['guided_journeys']==[]
    assert client.get('/api/units/unit-7/journeys/U7-J1').status_code==(200 if status['status']=='STUDENT_READY' else 404)
    assert client.get('/api/units/unit-7/application-lab').json()['challenge_count']==(16 if status['status']=='STUDENT_READY' else 0)
    obj=client.get('/api/units/unit-7/objects/U7-K-001')
    assert obj.status_code==200
    assert obj.json().get('canonical_lock',obj.json().get('scientific_lock_status'))=='LOCKED_F1'
