import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U7=ROOT/'content/ap-biology/unit-7'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_f4f_journey6_accounting_and_chronology():
    j=read(U7/'journeys/U7-J6.json')
    assert j['scene_count']==5 and j['checkpoint_count']==2
    assert [s['locus_id'] for s in j['scenes']]==[f'U7-L{i:02d}' for i in range(51,56)]
    assert len({k for s in j['scenes'] for k in s['object_ids']})==15
    assert [x['slot'] for x in j['chronology_slots']]==[1,2,3,4,5]
    assert all(len(re.findall(r"\b[\w’′'-]+\b",' '.join(s['story_paragraphs'])))>=450 for s in j['scenes'])

def test_f4f_locked_science_and_exact_terms():
    j=read(U7/'journeys/U7-J6.json')
    briefs={b['locus_id']:b for b in read(U7/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U7-J6'}
    canon={r['knowledge_id']:r for r in read(U7/'source/canonical-unit7-f1.json')['canonical_catalog']}
    exact=0
    for s in j['scenes']:
        text=' '.join(s['story_paragraphs']).casefold().replace('**','')
        assert s['object_ids']==briefs[s['locus_id']]['knowledge_ids']
        for beat in s['story_beats']:
            assert beat['science']==canon[beat['object_id']]['canonical_verified_statement']
            if beat['exact_name']:
                exact+=1
                assert beat['term'].casefold() in text
    assert exact==3

def test_f4f_high_risk_origin_of_life_guards():
    j=read(U7/'journeys/U7-J6.json')
    text=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
    for phrase in [
        'little free molecular oxygen',
        'oparin-haldane hypothesis',
        'historical hypothesis',
        'miller-urey experiment',
        'small organic compounds could form abiotically under the simulated conditions',
        'rna world hypothesis',
        'complementary base pairing',
        'genetically encoded proteins were not initially required as catalysts',
        'catalytic rna and ribozymes',
        'endosymbiosis is later than life',
        'the host must already be a cell',
    ]:
        assert phrase in text

def test_f4f_prior_journeys_frozen():
    lock=read(U7/'content-lock-f4f.json')
    assert len(lock['prior_narrative_protection'])==45
    for rel,meta in lock['prior_narrative_protection'].items():
        p=ROOT/rel
        assert p.stat().st_size==meta['bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']

def test_f4f_runtime_hidden():
    c=TestClient(app)
    u=c.get('/api/units/unit-7').json()
    assert u['status'] in {'F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
    if u['status']=='STUDENT_READY':
        assert u['student_release'] is True and u['preview_release'] is False
        assert len(c.get('/api/units/unit-7/journeys').json()['guided_journeys'])==6
        for jid in ['U7-J1','U7-J2','U7-J3','U7-J4','U7-J5','U7-J6']:
            assert c.get(f'/api/units/unit-7/journeys/{jid}').status_code==200
        assert c.get('/api/units/unit-7/application-lab').json()['challenge_count']==16
    else:
        assert u['student_release'] is False and u['preview_release'] is True
        assert c.get('/api/units/unit-7/journeys').json()['guided_journeys']==[]
        for jid in ['U7-J1','U7-J2','U7-J3','U7-J4','U7-J5','U7-J6']:
            assert c.get(f'/api/units/unit-7/journeys/{jid}').status_code==404
        assert c.get('/api/units/unit-7/application-lab').json()['challenge_count']==0
