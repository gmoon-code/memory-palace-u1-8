import json,re
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U5=ROOT/'content'/'ap-biology'/'unit-5'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit5_f4h_journey8_accounting_and_route():
    j=read(U5/'journeys/U5-J8.json')
    assert j['palace_id']=='U5-J8'
    assert j['scene_count']==7 and j['checkpoint_count']==3
    assert [s['locus_id'] for s in j['scenes']]==[f'U5-L{i:02d}' for i in range(44,51)]
    assert sum(len(s['object_ids']) for s in j['scenes'])==19
    assert len({x for s in j['scenes'] for x in s['object_ids']})==19
    assert j['student_release']=='DEVELOPER_PREVIEW_F4H'

def test_unit5_f4h_preserves_f3_assignments_science_and_prose_gate():
    j=read(U5/'journeys/U5-J8.json')
    briefs={b['locus_id']:b for b in read(U5/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U5-J8'}
    canon={r['knowledge_id']:r for r in read(U5/'source/canonical-unit5-f1.json')['canonical_catalog']}
    for s in j['scenes']:
        text=' '.join(s['story_paragraphs']); low=text.casefold().replace('**','')
        assert s['object_ids']==briefs[s['locus_id']]['knowledge_ids']
        assert s['misconception_guards']==briefs[s['locus_id']]['misconception_guards']
        assert len(re.findall(r"\b[\w’'-]+\b",text))>=600
        assert ':' not in text and '—' not in text
        for phrase in ('rather than','instead of','not only'):
            assert phrase not in low
        for beat in s['story_beats']:
            assert beat['science']==canon[beat['object_id']]['canonical_verified_statement']
            assert beat['term'].casefold() in low

def test_unit5_f4h_all_polished_journeys_cover_palace_records_exactly_once():
    ids=[]; scenes=0; recalls=0
    for i in range(1,9):
        j=read(U5/f'journeys/U5-J{i}.json')
        scenes+=len(j['scenes']); recalls+=sum(bool(s['checkpoint']) for s in j['scenes'])
        for s in j['scenes']: ids.extend(s['object_ids'])
    assert scenes==50 and recalls==18
    assert len(ids)==131 and len(set(ids))==131

def test_unit5_f4h_high_risk_evidence_boundaries_are_visible():
    j=read(U5/'journeys/U5-J8.json')
    text=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
    for phrase in [
        'non-nuclear inheritance','organelle assortment','animal mitochondrial inheritance','usually transmitted through the egg',
        'plant organelle inheritance','paternal','biparental','genetic disorder','pathogenic variant',
        'tay-sachs disease example','sickle cell disease example','chi-square goodness-of-fit test','categorical counts',
        'observed count (o)','expected count (e)','chi-square contribution','(o−e)²/e',
        'degrees of freedom for ap goodness-of-fit','chi-square critical value','p-value and significance level',
        'significance threshold','reject or fail to reject the null','no third door labeled accept the null'
    ]:
        assert phrase in text

def test_unit5_f4h_api_preview_without_student_release():
    client=TestClient(app)
    status=client.get('/api/units/unit-5').json()
    assert status['status'] in {'F4H_JOURNEYS1_8_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
    if status['status']=='STUDENT_READY':
        assert status['student_release'] is True and status['preview_release'] is False
    else:
        assert status['student_release'] is False and status['preview_release'] is True
    if status['status']!='STUDENT_READY':
        assert status['preview_journeys']==8 and status['preview_scenes']==50 and status['preview_checkpoints']==18
    journeys=client.get('/api/units/unit-5/journeys').json()['guided_journeys']
    assert [j['palace_id'] for j in journeys]==[f'U5-J{i}' for i in range(1,9)]
    assert client.get('/api/units/unit-5/journeys/U5-J8').status_code==200
    assert client.get('/api/units/unit-5/application-lab').json()['challenge_count'] in {0,16}
