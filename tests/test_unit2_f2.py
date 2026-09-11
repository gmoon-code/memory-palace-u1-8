import json, hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
client=TestClient(app)
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_f2_architecture_counts_and_lossless_assignment():
    src=read(U2/'source/canonical-unit2-f1.json')
    arch=read(U2/'architecture/palace-architecture-f2.json')
    cls=read(U2/'architecture/learning-classification-f2.json')
    assert len(src['canonical_catalog'])==142
    assert arch['counts']['journeys']==7
    assert arch['counts']['bundles']==16
    assert arch['counts']['permanent_loci']==49
    assert arch['counts']['palace_managed_records']==133
    assert arch['counts']['practice_only_records']==9
    assigned=[k for l in arch['loci'] for k in l['knowledge_ids']]
    challenges=[x['knowledge_id'] for x in arch['challenge_lab']]
    assert len(assigned)==len(set(assigned))==133
    assert len(challenges)==len(set(challenges))==9
    assert set(assigned)|set(challenges)=={r['knowledge_id'] for r in src['canonical_catalog']}
    assert len(cls['records'])==142

def test_f2_has_no_mandatory_spelling_gauntlet():
    cls=read(U2/'architecture/learning-classification-f2.json')
    assert cls['counts']['exact_name_targets']==106
    assert cls['counts']['mandatory_spelling_targets']==0
    assert all(x['spelling_policy']=='ADAPTIVE_SUPPORT_ONLY_NO_MANDATORY_SPELLING_GATE' for x in cls['records'])

def test_f2_loci_have_clear_scene_geometry_but_no_story_prose():
    arch=read(U2/'architecture/palace-architecture-f2.json')
    for l in arch['loci']:
        assert set(l['scene_geometry'])=={'left','center','right'}
        assert all(l['scene_geometry'].values())
        assert l['micro_anchor']
        assert l['narrative_status']=='ARCHITECTURE_ONLY_NO_STORY_PROSE_F2'

def test_f2_content_lock_hashes():
    lock=read(U2/'content-lock-f2.json')
    assert lock['lock_status']=='LOCKED_F2'
    for rel,meta in lock['files'].items():
        p=ROOT/rel
        assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']

def test_f2_api_preserves_architecture_after_final_release():
    d=client.get('/api/units/unit-2').json()
    assert d['status']=='STUDENT_READY' and d['student_release'] is True
    assert d['journey_blueprints']==7
    assert d['permanent_locus_blueprints']==49
    a=client.get('/api/units/unit-2/architecture')
    assert a.status_code==200
    assert a.json()['counts']['permanent_loci']==49
    assert client.get('/api/units/unit-2/journeys').status_code==200

