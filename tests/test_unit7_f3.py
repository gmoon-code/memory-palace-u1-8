import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content/ap-biology/unit-7'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit7_f3_scene_brief_accounting():
    d=read(U7/'briefs/scene-briefs-f3.json')
    assert d['counts']=={'journeys':6,'scene_briefs':55,'palace_managed_records':174,'term_introductions':174,'optional_first_exposure_recalls':18}
    assert len(d['scene_briefs'])==55
    assigned=[kid for b in d['scene_briefs'] for kid in b['knowledge_ids']]
    assert len(assigned)==len(set(assigned))==174

def test_unit7_f3_preserves_f2_geometry_and_f1_science():
    scenes=read(U7/'briefs/scene-briefs-f3.json')['scene_briefs']
    arch=read(U7/'architecture/palace-architecture-f2.json')['loci']
    canon={r['knowledge_id']:r for r in read(U7/'source/canonical-unit7-f1.json')['canonical_catalog']}
    for b,l in zip(scenes,arch):
        assert b['locus_id']==l['locus_id']
        assert [b['spatial_layout'][z]['anchor'] for z in ('left','center','right')]==[l['scene_geometry'][z] for z in ('left','center','right')]
        assert b['knowledge_ids']==l['knowledge_ids']
        assert len(b['stable_cast'])==3
        assert len(b['science_bearing_action']['during'])==3
        assert b['story_prose_status']=='PROHIBITED_UNTIL_F3_BRIEF_QA_PASS'
        for t in b['term_introductions']:
            r=canon[t['knowledge_id']]
            assert t['canonical_term']==r['canonical_label']
            assert t['canonical_science']==r['canonical_verified_statement']

def test_unit7_f3_journey_continuity_is_locked():
    d=read(U7/'briefs/journey-briefs-f3.json')
    assert d['journey_count']==6
    assert [j['journey_id'] for j in d['journeys']]==[f'U7-J{i}' for i in range(1,7)]
    assert all(j['unit_guide']['name']=='Dr. Imani Vale' for j in d['journeys'])
    assert all(j['continuity_object'] and j['opening_image'] and j['ending_payoff'] for j in d['journeys'])
    assert all(j['status']=='JOURNEY_BRIEF_LOCKED_F3_NO_POLISHED_STORY_PROSE' for j in d['journeys'])

def test_unit7_f3_quick_recall_is_sparse():
    d=read(U7/'briefs/scene-briefs-f3.json')['scene_briefs']
    per={f'U7-J{i}':0 for i in range(1,7)}
    for b in d:
        if b['quick_recall']['enabled']: per[b['journey_id']]+=1
    assert per=={'U7-J1':3,'U7-J2':4,'U7-J3':3,'U7-J4':3,'U7-J5':3,'U7-J6':2}

def test_unit7_f3_reactivations_and_runtime_boundary():
    d=read(U7/'briefs/scene-briefs-f3.json')['scene_briefs']
    react=[x for b in d for x in b['prior_unit_reactivation']]
    assert len(react)==6
    assert len({x['knowledge_id'] for x in react})==6
    s=read(U7/'status-f3.json'); r=read(U7/'f3-release-manifest.json')
    assert s['status']=='SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED'
    assert s['student_release'] is False and s['preview_release'] is False
    assert (s['journey_count'],s['scene_count'],s['memory_objects'],s['application_challenges'])==(0,0,0,0)
    assert (s['architecture_journeys'],s['architecture_loci'],s['scene_briefs'])==(6,55,55)
    assert r['polished_story_files']==0 and r['student_runtime_memory_objects']==0
