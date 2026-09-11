import json,re
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U5=ROOT/'content'/'ap-biology'/'unit-5'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit5_f4f_journey6_accounting_and_route():
    j=read(U5/'journeys/U5-J6.json')
    assert j['palace_id']=='U5-J6'
    assert j['scene_count']==7 and j['checkpoint_count']==2
    assert [s['locus_id'] for s in j['scenes']]==[f'U5-L{i:02d}' for i in range(31,38)]
    assert sum(len(s['object_ids']) for s in j['scenes'])==24
    assert len({x for s in j['scenes'] for x in s['object_ids']})==24
    assert j['student_release']=='DEVELOPER_PREVIEW_F4F'

def test_unit5_f4f_scene_density_layout_and_style():
    j=read(U5/'journeys/U5-J6.json'); counts=[]
    for s in j['scenes']:
        prose=' '.join(s['story_paragraphs']); counts.append(len(re.findall(r"\b[\w’'-]+\b",prose)))
        assert counts[-1]>=640
        assert len(s['story_paragraphs'])>=6
        opening=s['story_paragraphs'][0].casefold()
        assert 'left' in opening and 'right' in opening and ('ahead' in opening or 'center' in opening)
        names={c['name'] for c in s['cast']}
        for required in ('Dr. Imani Reyes','Phenotype-comparison frame','Mechanism identity cards','Gold generation ledger'):
            assert required in names
        assert '—' not in prose and ':' not in prose
        low=prose.casefold()
        for phrase in ('rather than','instead of','not only'):
            assert phrase not in low
    assert sum(counts)/len(counts)>=675

def test_unit5_f4f_exact_science_terms_and_guards_match_f1_f3():
    canon={r['knowledge_id']:r for r in read(U5/'source/canonical-unit5-f1.json')['canonical_catalog']}
    briefs={b['locus_id']:b for b in read(U5/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U5-J6'}
    j=read(U5/'journeys/U5-J6.json')
    for s in j['scenes']:
        text=' '.join(s['story_paragraphs']).casefold().replace('**','')
        assert s['misconception_guards']==briefs[s['locus_id']]['misconception_guards']
        assert s['object_ids']==briefs[s['locus_id']]['knowledge_ids']
        for beat in s['story_beats']:
            assert beat['science']==canon[beat['object_id']]['canonical_verified_statement']
            assert beat['term'].casefold() in text

def test_unit5_f4f_discrimination_boundaries_are_visible():
    j=read(U5/'journeys/U5-J6.json')
    text=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
    for phrase in [
        'incomplete dominance','codominance','multiple alleles','abo blood-group allele system',
        'epistasis','polygenic inheritance','pleiotropy','the geometry is many genes feeding one character',
        'the second right-side branch reverses the geometry','human x/y chromosome-complement model',
        'does not define gender','other sex-determination systems exist','hemizygous',
        'x-linked transmission in an xx/xy model','x-chromosome inactivation','barr body',
        'some genes can escape','phenotypic plasticity','hold genotype constant first',
        'all phenotypic variation is environmental'
    ]:
        assert phrase in text

def test_unit5_f4f_api_preview_without_student_release():
    client=TestClient(app)
    status=client.get('/api/units/unit-5').json()
    assert status['status'] in {'F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW','F4G_JOURNEYS1_7_POLISHED_DEVELOPER_PREVIEW','F4H_JOURNEYS1_8_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
    if status['status']=='STUDENT_READY':
        assert status['student_release'] is True and status['preview_release'] is False
    else:
        assert status['student_release'] is False and status['preview_release'] is True
    journeys=client.get('/api/units/unit-5/journeys').json()['guided_journeys']
    assert [j['palace_id'] for j in journeys] in [['U5-J1','U5-J2','U5-J3','U5-J4','U5-J5','U5-J6'],['U5-J1','U5-J2','U5-J3','U5-J4','U5-J5','U5-J6','U5-J7'],['U5-J1','U5-J2','U5-J3','U5-J4','U5-J5','U5-J6','U5-J7','U5-J8']]
    for jid in ['U5-J1','U5-J2','U5-J3','U5-J4','U5-J5','U5-J6']:
        assert client.get(f'/api/units/unit-5/journeys/{jid}').status_code==200
    assert client.get('/api/units/unit-5/journeys/U5-J7').status_code in {200,404}
    assert client.get('/api/units/unit-5/application-lab').json()['challenge_count'] in {0,16}
