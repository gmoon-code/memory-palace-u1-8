import json,re
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit5_f4d_journey4_accounting_and_route():
    j=read(U5/'journeys/U5-J4.json')
    assert j['palace_id']=='U5-J4'
    assert j['scene_count']==7 and len(j['scenes'])==7
    assert j['checkpoint_count']==2
    assert j['student_release']=='DEVELOPER_PREVIEW_F4D'
    assert [s['locus_id'] for s in j['scenes']]==[f'U5-L{i:02d}' for i in range(20,27)]
    ids=[kid for s in j['scenes'] for kid in s['object_ids']]
    assert len(ids)==25 and len(set(ids))==25

def test_unit5_f4d_prose_is_spatial_substantive_and_style_clean():
    j=read(U5/'journeys/U5-J4.json')
    words=[]
    for s in j['scenes']:
        prose=' '.join(s['story_paragraphs']); words.append(len(re.findall(r"\b[\w’'-]+\b",prose)))
        assert words[-1]>=525
        assert len(s['story_paragraphs'])>=6
        opening=s['story_paragraphs'][0].lower()
        assert 'left' in opening and 'right' in opening and ('ahead' in opening or 'center' in opening)
        assert s['cast'][0]['name']=='Dr. Imani Reyes'
        assert any(c['name']=='Pea-line breeding ledger' for c in s['cast'])
        assert any(c['name']=='Tracked allele case' for c in s['cast'])
        assert '—' not in prose
        assert ':' not in re.sub(r'9:3:3:1|3:1','',prose)
    assert sum(words)/len(words)>=600

def test_unit5_f4d_exact_science_terms_and_guards_match_f1_f3():
    canon={r['knowledge_id']:r for r in read(U5/'source/canonical-unit5-f1.json')['canonical_catalog']}
    briefs={b['locus_id']:b for b in read(U5/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U5-J4'}
    j=read(U5/'journeys/U5-J4.json')
    for s in j['scenes']:
        text=' '.join(s['story_paragraphs']).casefold().replace('**','')
        assert s['misconception_guards']==briefs[s['locus_id']]['misconception_guards']
        assert s['object_ids']==briefs[s['locus_id']]['knowledge_ids']
        for beat in s['story_beats']:
            assert beat['science']==canon[beat['object_id']]['canonical_verified_statement']
            assert beat['term'].casefold() in text

def test_unit5_f4d_punnett_and_ratio_boundaries_are_visible():
    j=read(U5/'journeys/U5-J4.json')
    text=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
    for phrase in ['dominant says nothing about how common','law of segregation','law of independent assortment','monohybrid, dihybrid, and test crosses','gametes from a genotype','punnett square','possible gametes come from meiosis and the parental genotype, not from the grid','not guaranteed offspring counts','classic 3:1 f2 ratio','classic 9:3:3:1 ratio','the ratio is a conditional expectation']:
        assert phrase in text

def test_unit5_f4d_api_preview_without_student_release():
    client=TestClient(app)
    status=client.get('/api/units/unit-5').json()
    assert status['status'] in {'F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW','F4G_JOURNEYS1_7_POLISHED_DEVELOPER_PREVIEW','F4H_JOURNEYS1_8_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
    if status['status']=='STUDENT_READY':
        assert status['student_release'] is True and status['preview_release'] is False
    else:
        assert status['student_release'] is False and status['preview_release'] is True
    journeys=client.get('/api/units/unit-5/journeys').json()['guided_journeys']
    assert [j['palace_id'] for j in journeys] in (['U5-J1','U5-J2','U5-J3','U5-J4'],['U5-J1','U5-J2','U5-J3','U5-J4','U5-J5'],['U5-J1','U5-J2','U5-J3','U5-J4','U5-J5','U5-J6'],['U5-J1','U5-J2','U5-J3','U5-J4','U5-J5','U5-J6','U5-J7'],['U5-J1','U5-J2','U5-J3','U5-J4','U5-J5','U5-J6','U5-J7','U5-J8'])
    for jid in ['U5-J1','U5-J2','U5-J3','U5-J4']:
        assert client.get(f'/api/units/unit-5/journeys/{jid}').status_code==200
    assert client.get('/api/units/unit-5/application-lab').json()['challenge_count'] in {0,16}
