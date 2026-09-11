import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U6=ROOT/'content'/'ap-biology'/'unit-6'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit6_f2_architecture_accounting():
    arch=read(U6/'architecture'/'palace-architecture-f2.json')
    cls=read(U6/'architecture'/'learning-classification-f2.json')
    assert arch['counts']=={'canonical_records':202,'palace_managed_records':161,'scope_guard_records':25,'practice_only_records':16,'journeys':6,'bundles':21,'permanent_loci':53,'confusable_sets':37}
    assert len(cls['records'])==202
    assert cls['counts']['by_destination']=={'PALACE_PRIMARY_LOCUS':53,'PALACE_EMBEDDED':108,'SUPPORTING_NON_RUNTIME_SCOPE_GUARD':25,'CHALLENGE_LAB':16}
    assert cls['counts']['exact_name_targets']==134
    assert cls['counts']['prerequisite_reactivations']==5
    assert cls['counts']['mandatory_spelling_targets']==0

def test_unit6_f2_zero_loss_and_no_overlap():
    src=read(U6/'source'/'canonical-unit6-f1.json')
    arch=read(U6/'architecture'/'palace-architecture-f2.json')
    canonical={r['knowledge_id'] for r in src['canonical_catalog']}
    palace={k for l in arch['loci'] for k in l['knowledge_ids']}
    challenge={x['knowledge_id'] for x in arch['challenge_lab']}
    scope={x['knowledge_id'] for x in arch['scope_guards']}
    assert (len(palace),len(challenge),len(scope))==(161,16,25)
    assert palace|challenge|scope==canonical
    assert not (palace&challenge or palace&scope or challenge&scope)

def test_unit6_f2_spatial_architecture_is_complete_without_story_prose():
    arch=read(U6/'architecture'/'palace-architecture-f2.json')
    assert [j['journey_id'] for j in arch['journeys']]==[f'U6-J{i}' for i in range(1,7)]
    assert [l['locus_id'] for l in arch['loci']]==[f'U6-L{i:02d}' for i in range(1,54)]
    for l in arch['loci']:
        assert set(l['scene_geometry'])=={'left','center','right'}
        assert all(l['scene_geometry'].values())
        assert l['primary_knowledge_id'] in l['knowledge_ids']
        assert l['scientific_visual_required'] is True
        assert l['narrative_status']=='ARCHITECTURE_ONLY_NO_STORY_PROSE_F2'
        assert 'story_paragraphs' not in l and 'story_open' not in l and 'story_close' not in l and 'cast' not in l

def test_unit6_f2_challenge_lab_and_confusables_are_architecture_only():
    arch=read(U6/'architecture'/'palace-architecture-f2.json')
    loci={l['locus_id'] for l in arch['loci']}
    palace={k for l in arch['loci'] for k in l['knowledge_ids']}
    assert len(arch['challenge_lab'])==16
    assert all(set(x['prerequisite_loci'])<=loci for x in arch['challenge_lab'])
    assert len(arch['confusable_sets'])==37
    assert all(len(x['terms'])>=2 and len(set(x['knowledge_ids']))>=2 for x in arch['confusable_sets'])
    assert all(set(x['knowledge_ids'])<=palace for x in arch['confusable_sets'])

def test_unit6_f2_is_not_student_release():
    s=read(U6/'status-f2.json'); r=read(U6/'f2-release-manifest.json')
    assert s['status']=='LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED'
    assert s['student_release'] is False and s['preview_release'] is False
    assert (s['journey_count'],s['scene_count'],s['memory_objects'],s['application_challenges'])==(0,0,0,0)
    assert (s['architecture_journeys'],s['architecture_bundles'],s['architecture_loci'])==(6,21,53)
    assert r['student_release'] is False and r['narrative_story_files']==0 and r['student_runtime_memory_objects']==0
