import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content'/'ap-biology'/'unit-4'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit4_f2_architecture_accounting():
    arch=read(U4/'architecture'/'palace-architecture-f2.json')
    cls=read(U4/'architecture'/'learning-classification-f2.json')
    assert arch['counts']=={'canonical_records':180,'palace_managed_records':162,'scope_guard_records':3,'practice_only_records':15,'journeys':7,'bundles':17,'permanent_loci':51,'confusable_sets':33}
    assert len(cls['records'])==180
    assert cls['counts']['by_destination']=={'PALACE_PRIMARY_LOCUS':51,'PALACE_EMBEDDED':111,'CHALLENGE_LAB':15,'SUPPORTING_NON_RUNTIME_SCOPE_GUARD':3}
    assert cls['counts']['exact_name_targets']==162
    assert cls['counts']['mandatory_spelling_targets']==0

def test_unit4_f2_zero_loss_and_no_overlap():
    src=read(U4/'source'/'canonical-unit4-f1.json')
    arch=read(U4/'architecture'/'palace-architecture-f2.json')
    canonical={r['knowledge_id'] for r in src['canonical_catalog']}
    palace={k for l in arch['loci'] for k in l['knowledge_ids']}
    challenge={x['knowledge_id'] for x in arch['challenge_lab']}
    scope={x['knowledge_id'] for x in arch['scope_guards']}
    assert (len(palace),len(challenge),len(scope))==(162,15,3)
    assert palace|challenge|scope==canonical
    assert not (palace&challenge or palace&scope or challenge&scope)

def test_unit4_f2_spatial_architecture_is_complete_without_story_prose():
    arch=read(U4/'architecture'/'palace-architecture-f2.json')
    assert [j['journey_id'] for j in arch['journeys']]==[f'U4-J{i}' for i in range(1,8)]
    assert [l['locus_id'] for l in arch['loci']]==[f'U4-L{i:02d}' for i in range(1,52)]
    for l in arch['loci']:
        assert set(l['scene_geometry'])=={'left','center','right'}
        assert all(l['scene_geometry'].values())
        assert l['primary_knowledge_id'] in l['knowledge_ids']
        assert l['scientific_visual_required'] is True
        assert l['narrative_status']=='ARCHITECTURE_ONLY_NO_STORY_PROSE_F2'
        assert 'story_paragraphs' not in l and 'story_open' not in l and 'story_close' not in l

def test_unit4_f2_challenge_lab_and_confusables_are_architecture_only():
    arch=read(U4/'architecture'/'palace-architecture-f2.json')
    loci={l['locus_id'] for l in arch['loci']}
    assert len(arch['challenge_lab'])==15
    assert all(set(x['prerequisite_loci'])<=loci for x in arch['challenge_lab'])
    assert len(arch['confusable_sets'])==33
    assert all(len(x['terms'])>=2 and len(x['knowledge_ids'])>=2 for x in arch['confusable_sets'])

def test_unit4_f2_is_not_student_release():
    s=read(U4/'status-f2.json'); r=read(U4/'f2-release-manifest.json')
    assert s['status']=='LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED'
    assert s['student_release'] is False and s['preview_release'] is False
    assert (s['journey_count'],s['scene_count'],s['memory_objects'],s['application_challenges'])==(0,0,0,0)
    assert (s['architecture_journeys'],s['architecture_bundles'],s['architecture_loci'])==(7,17,51)
    assert r['student_release'] is False and r['narrative_story_files']==0 and r['student_runtime_memory_objects']==0
