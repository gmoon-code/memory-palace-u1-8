import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content/ap-biology/unit-7'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit7_f2_architecture_accounting():
    arch=read(U7/'architecture/palace-architecture-f2.json')
    cls=read(U7/'architecture/learning-classification-f2.json')
    assert arch['counts']=={
        'canonical_records':215,'palace_managed_records':174,'scope_guard_records':25,
        'practice_only_records':16,'journeys':6,'bundles':23,'permanent_loci':55,'confusable_sets':33
    }
    assert len(cls['records'])==215
    assert cls['counts']['by_destination']=={
        'PALACE_PRIMARY_LOCUS':55,'PALACE_EMBEDDED':119,
        'SUPPORTING_NON_RUNTIME_SCOPE_GUARD':25,'CHALLENGE_LAB':16
    }
    assert cls['counts']['exact_name_targets']==94
    assert cls['counts']['prerequisite_reactivations']==6
    assert cls['counts']['mandatory_spelling_targets']==0

def test_unit7_f2_zero_loss_and_no_overlap():
    src=read(U7/'source/canonical-unit7-f1.json')
    arch=read(U7/'architecture/palace-architecture-f2.json')
    canonical={r['knowledge_id'] for r in src['canonical_catalog']}
    palace={k for l in arch['loci'] for k in l['knowledge_ids']}
    challenge={x['knowledge_id'] for x in arch['challenge_lab']}
    scope={x['knowledge_id'] for x in arch['scope_guards']}
    assert (len(palace),len(challenge),len(scope))==(174,16,25)
    assert palace|challenge|scope==canonical
    assert not (palace&challenge or palace&scope or challenge&scope)

def test_unit7_f2_spatial_architecture_is_complete_without_story_prose():
    arch=read(U7/'architecture/palace-architecture-f2.json')
    assert [j['journey_id'] for j in arch['journeys']]==[f'U7-J{i}' for i in range(1,7)]
    assert [l['locus_id'] for l in arch['loci']]==[f'U7-L{i:02d}' for i in range(1,56)]
    for l in arch['loci']:
        assert set(l['scene_geometry'])=={'left','center','right'}
        assert all(l['scene_geometry'].values())
        assert l['micro_anchor']
        assert l['primary_knowledge_id'] in l['knowledge_ids']
        assert l['scientific_visual_required'] is True
        assert l['narrative_status']=='ARCHITECTURE_ONLY_NO_STORY_PROSE_F2'
        for key in ('story_paragraphs','story_open','story_close','cast','dialogue','mnemonic_hook'):
            assert key not in l

def test_unit7_f2_challenge_lab_confusables_and_reactivations():
    arch=read(U7/'architecture/palace-architecture-f2.json')
    loci={l['locus_id'] for l in arch['loci']}
    palace={k for l in arch['loci'] for k in l['knowledge_ids']}
    assert len(arch['challenge_lab'])==16
    assert all(set(x['prerequisite_loci'])<=loci for x in arch['challenge_lab'])
    assert len(arch['confusable_sets'])==33
    assert all(len(set(x['knowledge_ids']))>=2 for x in arch['confusable_sets'])
    assert all(set(x['knowledge_ids'])<=palace for x in arch['confusable_sets'])
    assert len(arch['prerequisite_reactivations'])==6

def test_unit7_f2_is_not_student_release():
    s=read(U7/'status-f2.json'); r=read(U7/'f2-release-manifest.json')
    assert s['status'] in {'LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED'}
    assert s['student_release'] is False and s['preview_release'] is False
    assert (s['journey_count'],s['scene_count'],s['memory_objects'],s['application_challenges'])==(0,0,0,0)
    assert (s['architecture_journeys'],s['architecture_bundles'],s['architecture_loci'])==(6,23,55)
    assert r['student_release'] is False and r['narrative_story_files']==0 and r['student_runtime_memory_objects']==0
