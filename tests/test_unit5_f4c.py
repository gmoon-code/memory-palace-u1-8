import json,re
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit5_f4c_journey3_accounting_and_route():
    j=read(U5/'journeys/U5-J3.json')
    assert j['palace_id']=='U5-J3'
    assert j['scene_count']==4 and len(j['scenes'])==4
    assert j['checkpoint_count']==2
    assert j['student_release']=='DEVELOPER_PREVIEW_F4C'
    assert [s['locus_id'] for s in j['scenes']]==[f'U5-L{i:02d}' for i in range(16,20)]
    assert len({kid for s in j['scenes'] for kid in s['object_ids']})==8

def test_unit5_f4c_prose_is_spatial_substantive_and_diagnostic():
    j=read(U5/'journeys/U5-J3.json')
    for s in j['scenes']:
        prose=' '.join(s['story_paragraphs'])
        assert len(re.findall(r"\b[\w’'-]+\b",prose))>=550
        assert len(s['story_paragraphs'])>=7
        opening=s['story_paragraphs'][0].lower()
        assert 'left' in opening and ('ahead' in opening or 'center' in opening) and 'right' in opening
        assert s['cast'][0]['name']=='Dr. Imani Reyes'
        assert any(c['name']=='Chromosome-outcome scanner' for c in s['cast'])
        assert any(c['name']=='Gold generation ledger' for c in s['cast'])
        assert ':' not in prose and '—' not in prose

def test_unit5_f4c_exact_science_terms_and_guards_match_f1_f3():
    canon={r['knowledge_id']:r for r in read(U5/'source/canonical-unit5-f1.json')['canonical_catalog']}
    briefs={b['locus_id']:b for b in read(U5/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U5-J3'}
    j=read(U5/'journeys/U5-J3.json')
    for s in j['scenes']:
        text=' '.join(s['story_paragraphs']).casefold().replace('**','')
        assert s['misconception_guards']==briefs[s['locus_id']]['misconception_guards']
        for beat in s['story_beats']:
            assert beat['science']==canon[beat['object_id']]['canonical_verified_statement']
            assert beat['term'].casefold() in text

def test_unit5_f4c_cause_outcome_and_case_distinctions_are_visible():
    j=read(U5/'journeys/U5-J3.json')
    text=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
    for phrase in ['crossing over','independent orientation','random fertilization','recombinant chromosome','segregation-integrity mode','nondisjunction is the segregation failure','aneuploidy','complete chromosome sets','karyotype shows the resulting chromosome complement','three copies of chromosome 21','down syndrome']:
        assert phrase in text

def test_unit5_f4c_api_preview_without_student_release():
    client=TestClient(app)
    status=client.get('/api/units/unit-5').json()
    assert status['status'] in {'F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW','F4G_JOURNEYS1_7_POLISHED_DEVELOPER_PREVIEW','F4H_JOURNEYS1_8_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
    if status['status']=='STUDENT_READY':
        assert status['student_release'] is True and status['preview_release'] is False
    else:
        assert status['student_release'] is False and status['preview_release'] is True
    journeys=client.get('/api/units/unit-5/journeys').json()['guided_journeys']
    assert [j['palace_id'] for j in journeys] in (['U5-J1','U5-J2','U5-J3'],['U5-J1','U5-J2','U5-J3','U5-J4'],['U5-J1','U5-J2','U5-J3','U5-J4','U5-J5'],['U5-J1','U5-J2','U5-J3','U5-J4','U5-J5','U5-J6'],['U5-J1','U5-J2','U5-J3','U5-J4','U5-J5','U5-J6','U5-J7'],['U5-J1','U5-J2','U5-J3','U5-J4','U5-J5','U5-J6','U5-J7','U5-J8'])
    for jid in ['U5-J1','U5-J2','U5-J3']:
        assert client.get(f'/api/units/unit-5/journeys/{jid}').status_code==200
    assert client.get('/api/units/unit-5/application-lab').json()['challenge_count'] in {0,16}
