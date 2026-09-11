import json,re
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit5_f4e_journey5_accounting_and_route():
    j=read(U5/'journeys/U5-J5.json')
    assert j['palace_id']=='U5-J5'
    assert j['scene_count']==4 and len(j['scenes'])==4
    assert j['checkpoint_count']==2
    assert j['student_release']=='DEVELOPER_PREVIEW_F4E'
    assert [s['locus_id'] for s in j['scenes']]==[f'U5-L{i:02d}' for i in range(27,31)]
    ids=[kid for s in j['scenes'] for kid in s['object_ids']]
    assert len(ids)==7 and len(set(ids))==7

def test_unit5_f4e_prose_is_spatial_substantive_and_style_clean():
    j=read(U5/'journeys/U5-J5.json')
    words=[]
    for s in j['scenes']:
        prose=' '.join(s['story_paragraphs']); words.append(len(re.findall(r"\b[\w’'-]+\b",prose)))
        assert words[-1]>=600
        assert len(s['story_paragraphs'])>=6
        opening=s['story_paragraphs'][0].lower()
        assert 'left' in opening and 'right' in opening and ('ahead' in opening or 'center' in opening)
        assert s['cast'][0]['name']=='Dr. Imani Reyes'
        assert any(c['name']=='Two-sided evidence docket' for c in s['cast'])
        assert any(c['name']=='Event-probability cards' for c in s['cast'])
        assert any(c['name']=='Candidate inheritance-model cards' for c in s['cast'])
        assert '—' not in prose and ':' not in prose
        low=prose.casefold()
        for phrase in ('rather than','instead of','not only'):
            assert phrase not in low
    assert sum(words)/len(words)>=650

def test_unit5_f4e_exact_science_terms_and_guards_match_f1_f3():
    canon={r['knowledge_id']:r for r in read(U5/'source/canonical-unit5-f1.json')['canonical_catalog']}
    briefs={b['locus_id']:b for b in read(U5/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U5-J5'}
    j=read(U5/'journeys/U5-J5.json')
    for s in j['scenes']:
        text=' '.join(s['story_paragraphs']).casefold().replace('**','')
        assert s['misconception_guards']==briefs[s['locus_id']]['misconception_guards']
        assert s['object_ids']==briefs[s['locus_id']]['knowledge_ids']
        for beat in s['story_beats']:
            assert beat['science']==canon[beat['object_id']]['canonical_verified_statement']
            assert beat['term'].casefold() in text

def test_unit5_f4e_probability_pedigree_and_inference_boundaries_are_visible():
    j=read(U5/'journeys/U5-J5.json')
    text=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
    for phrase in [
        'probability in inheritance','expected under the model','addition rule of probability','mutually exclusive',
        'multiplication rule of probability','independent','pedigree notation','autosomal-dominant pedigree clue',
        'new variant','penetrance','x-linked recessive','one visual feature cannot settle the case by itself',
        'inheritance-pattern inference','generate predictions','still plausible','weakened',
        'evidence comes first, the model earns its support, and probability operates inside clearly stated assumptions'
    ]:
        assert phrase in text

def test_unit5_f4e_api_preview_without_student_release():
    client=TestClient(app)
    status=client.get('/api/units/unit-5').json()
    assert status['status'] in {'F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW','F4G_JOURNEYS1_7_POLISHED_DEVELOPER_PREVIEW','F4H_JOURNEYS1_8_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
    if status['status']=='STUDENT_READY':
        assert status['student_release'] is True and status['preview_release'] is False
    else:
        assert status['student_release'] is False and status['preview_release'] is True
    journeys=client.get('/api/units/unit-5/journeys').json()['guided_journeys']
    assert [j['palace_id'] for j in journeys][:5]==['U5-J1','U5-J2','U5-J3','U5-J4','U5-J5']
    for jid in ['U5-J1','U5-J2','U5-J3','U5-J4','U5-J5']:
        assert client.get(f'/api/units/unit-5/journeys/{jid}').status_code==200
    assert client.get('/api/units/unit-5/application-lab').json()['challenge_count'] in {0,16}
