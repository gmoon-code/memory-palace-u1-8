import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content/ap-biology/unit-4'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit4_f3_scene_brief_accounting():
    scenes=read(U4/'briefs/scene-briefs-f3.json')
    assert scenes['counts']=={'journeys':7,'scene_briefs':51,'palace_managed_records':162,'term_introductions':162,'optional_first_exposure_recalls':18}
    assert len(scenes['scene_briefs'])==51
    assigned=[kid for b in scenes['scene_briefs'] for kid in b['knowledge_ids']]
    assert len(assigned)==len(set(assigned))==162

def test_unit4_f3_journey_continuity_is_locked():
    doc=read(U4/'briefs/journey-briefs-f3.json')
    assert doc['journey_count']==7
    assert [j['journey_id'] for j in doc['journeys']]==[f'U4-J{i}' for i in range(1,8)]
    assert all(j['unit_guide']['name']=='Dr. Mira Chen' for j in doc['journeys'])
    assert all(j['continuity_object'] and j['opening_image'] and j['ending_payoff'] for j in doc['journeys'])
    assert all(j['status']=='JOURNEY_BRIEF_LOCKED_F3_NO_POLISHED_STORY_PROSE' for j in doc['journeys'])

def test_unit4_f3_preserves_f2_geometry_and_f1_science():
    scenes=read(U4/'briefs/scene-briefs-f3.json')['scene_briefs']
    arch=read(U4/'architecture/palace-architecture-f2.json')['loci']
    canon={r['knowledge_id']:r for r in read(U4/'source/canonical-unit4-f1.json')['canonical_catalog']}
    for b,l in zip(scenes,arch):
        assert b['locus_id']==l['locus_id']
        assert [b['spatial_layout'][z]['anchor'] for z in ('left','center','right')]==[l['scene_geometry'][z] for z in ('left','center','right')]
        assert b['knowledge_ids']==l['knowledge_ids']
        assert len(b['stable_cast'])==3
        assert b['story_prose_status']=='PROHIBITED_UNTIL_F3_BRIEF_QA_PASS'
        for t in b['term_introductions']:
            r=canon[t['knowledge_id']]
            assert t['canonical_term']==r['canonical_label']
            assert t['canonical_science']==r['canonical_verified_statement']

def test_unit4_f3_historical_lock_remains_preserved_after_later_preview_stages():
    status=read(U4/'status-f3.json')
    assert status['status']=='SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED'
    assert status['student_release'] is False
    assert status['journey_count']==status['scene_count']==status['memory_objects']==status['application_challenges']==0
    assert not (U4/'memory-objects.json').exists()
    latest=read(U4/'status.json')
    assert latest['student_release'] in (False,True)
