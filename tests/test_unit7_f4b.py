import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content'/'ap-biology'/'unit-7'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit7_f4b_journey2_accounting_and_boundary():
    j=read(U7/'journeys/U7-J2.json')
    assert j['palace_id']=='U7-J2'
    assert j['scene_count']==14 and len(j['scenes'])==14
    assert j['checkpoint_count']==4
    assert j['student_release']=='DEVELOPER_PREVIEW_F4B'
    assert j['preview_release'] is True
    assert [s['locus_id'] for s in j['scenes']]==[f'U7-L{i:02d}' for i in range(11,25)]
    assert len({kid for s in j['scenes'] for kid in s['object_ids']})==47

def test_unit7_f4b_prose_is_substantive_spatial_and_continuous():
    j=read(U7/'journeys/U7-J2.json')
    continuity=j['scenes'][0]['continuity_object']
    for s in j['scenes']:
        prose=' '.join(s['story_paragraphs'])
        assert len(re.findall(r"\b[\w’′'-]+\b",prose))>=450
        assert len(s['story_paragraphs'])>=6
        opening=s['story_paragraphs'][0].lower()
        assert 'left' in opening and ('ahead' in opening or 'center' in opening) and 'right' in opening
        assert len(s['cast'])>=7
        assert any(c['name']=='Dr. Imani Vale' for c in s['cast'])
        assert any(c['name']=='Island A gene-pool tank' for c in s['cast'])
        assert any(c['name']=='Island B gene-pool tank' for c in s['cast'])
        assert any(c['name']=='Transparent population ledger' for c in s['cast'])
        assert s['continuity_object']==continuity
        assert '—' not in prose and ': ' not in prose

def test_unit7_f4b_exact_targets_and_story_beat_science_match_locks():
    canon={r['knowledge_id']:r for r in read(U7/'source/canonical-unit7-f1.json')['canonical_catalog']}
    briefs={b['locus_id']:b for b in read(U7/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U7-J2'}
    j=read(U7/'journeys/U7-J2.json')
    exact=0
    for s in j['scenes']:
        text=' '.join(s['story_paragraphs']).casefold().replace('**','')
        assert s['object_ids']==briefs[s['locus_id']]['knowledge_ids']
        for beat in s['story_beats']:
            assert beat['science']==canon[beat['object_id']]['canonical_verified_statement']
            if beat['exact_name']:
                exact+=1
                assert beat['term'].casefold() in text
    assert exact==21

def test_unit7_f4b_high_risk_population_genetics_guards_are_explicit():
    j=read(U7/'journeys/U7-J2.json')
    text=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
    for phrase in [
        'microevolution is change in allele frequencies within a population across generations',
        'copying event is random with respect to whether the resulting variant will improve fitness',
        'selection is nonrandom differential reproductive success',
        'genetic drift is a nonselective change in allele frequency caused by chance',
        'drift is nonadaptive',
        'bottleneck is genetic drift following a severe population-size reduction',
        'founder effect is genetic drift when a new population is established by a small subset',
        'gene flow between populations tends to reduce genetic differences',
        'not inherently the dominant allele',
        'not inherently recessive',
        'nonrandom mating by itself can change genotype frequencies without changing allele frequencies',
        'square root of an arbitrary observed aa frequency',
        'frequency of that recessive phenotype can be treated as q²',
    ]:
        assert phrase in text

def test_unit7_f4b_journey1_is_byte_frozen():
    lock=read(U7/'content-lock-f4b.json')
    for rel,meta in lock['f4a_journey1_protection'].items():
        p=ROOT/rel
        assert p.stat().st_size==meta['bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']

def test_unit7_f4b_preview_is_not_public_student_runtime():
    client=TestClient(app)
    status=client.get('/api/units/unit-7').json()
    assert status['status'] in {'F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
    if status['status']=='STUDENT_READY':
        assert status['student_release'] is True and status['preview_release'] is False
        assert len(client.get('/api/units/unit-7/journeys').json()['guided_journeys'])==6
    else:
        assert status['student_release'] is False and status['preview_release'] is True
        assert client.get('/api/units/unit-7/journeys').json()['guided_journeys']==[]
    assert client.get('/api/units/unit-7/journeys/U7-J1').status_code==(200 if status['status']=='STUDENT_READY' else 404)
    assert client.get('/api/units/unit-7/journeys/U7-J2').status_code==(200 if status['status']=='STUDENT_READY' else 404)
    assert client.get('/api/units/unit-7/application-lab').json()['challenge_count']==(16 if status['status']=='STUDENT_READY' else 0)
