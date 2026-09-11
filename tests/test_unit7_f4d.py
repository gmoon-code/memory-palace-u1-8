import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content/ap-biology'/'unit-7'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit7_f4d_journey4_accounting_and_boundary():
    j=read(U7/'journeys/U7-J4.json')
    assert j['palace_id']=='U7-J4'
    assert j['scene_count']==8 and len(j['scenes'])==8
    assert j['checkpoint_count']==3
    assert j['student_release']=='DEVELOPER_PREVIEW_F4D'
    assert j['preview_release'] is True
    assert [s['locus_id'] for s in j['scenes']]==[f'U7-L{i:02d}' for i in range(34,42)]
    assert len({kid for s in j['scenes'] for kid in s['object_ids']})==26
    assert [t['name'] for t in j['taxa']]==['Lancelet','Shark','Salamander','Mouse','Lizard','Pigeon']
    assert set(j['node_map'])=={'N0','N1','N2','N3','N4'}

def test_unit7_f4d_prose_is_substantive_spatial_and_continuous():
    j=read(U7/'journeys/U7-J4.json')
    continuity=j['scenes'][0]['continuity_object']
    for s in j['scenes']:
        prose=' '.join(s['story_paragraphs'])
        assert len(re.findall(r"\b[\w’′'-]+\b",prose))>=450
        assert len(s['story_paragraphs'])>=6
        opening=s['story_paragraphs'][0].lower()
        assert 'left' in opening and ('ahead' in opening or 'center' in opening) and 'right' in opening
        for name in ['Dr. Imani Vale','Six-taxon badge rail','Persistent node map','Six-taxon navigation dossier']:
            assert any(c['name']==name for c in s['cast'])
        assert s['continuity_object']==continuity
        assert [t['name'] for t in s['taxa']]==['Lancelet','Shark','Salamander','Mouse','Lizard','Pigeon']
        assert set(s['node_map'])=={'N0','N1','N2','N3','N4'}
        assert '—' not in prose and ': ' not in prose

def test_unit7_f4d_exact_targets_and_story_beat_science_match_locks():
    canon={r['knowledge_id']:r for r in read(U7/'source/canonical-unit7-f1.json')['canonical_catalog']}
    briefs={b['locus_id']:b for b in read(U7/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U7-J4'}
    j=read(U7/'journeys/U7-J4.json')
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

def test_unit7_f4d_high_risk_tree_reading_guards_are_explicit():
    j=read(U7/'journeys/U7-J4.json')
    text=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
    for phrase in [
        'trees and cladograms are testable hypotheses',
        'branch lengths have no numerical legend',
        'nodes represent common ancestors',
        'neither lizard nor pigeon is being used as the ancestor of the other',
        'sister taxa or sister clades are the two descendant lineages that share the same immediate common ancestor',
        'it is not less evolved, unfinished, or the living ancestor',
        'synapomorphy',
        'outgroup is a lineage outside the focal ingroup',
        'tree changed because the evidence changed',
        'principle of parsimony',
        'not the only phylogenetic method',
    ]:
        assert phrase in text

def test_unit7_f4d_prior_journeys_are_byte_frozen():
    lock=read(U7/'content-lock-f4d.json')
    assert len(lock['f4a_f4c_prior_narrative_protection'])==27
    for rel,meta in lock['f4a_f4c_prior_narrative_protection'].items():
        p=ROOT/rel
        assert p.stat().st_size==meta['bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']

def test_unit7_f4d_preview_is_not_public_student_runtime():
    client=TestClient(app)
    status=client.get('/api/units/unit-7').json()
    assert status['status'] in {'F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
    if status['status']=='STUDENT_READY':
        assert status['student_release'] is True and status['preview_release'] is False
        assert len(client.get('/api/units/unit-7/journeys').json()['guided_journeys'])==6
    else:
        assert status['student_release'] is False and status['preview_release'] is True
        assert client.get('/api/units/unit-7/journeys').json()['guided_journeys']==[]
    for jid in ['U7-J1','U7-J2','U7-J3','U7-J4']:
        assert client.get(f'/api/units/unit-7/journeys/{jid}').status_code==(200 if status['status']=='STUDENT_READY' else 404)
    assert client.get('/api/units/unit-7/application-lab').json()['challenge_count']==(16 if status['status']=='STUDENT_READY' else 0)
