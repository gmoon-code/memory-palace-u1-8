import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit5_f3_scene_brief_accounting():
    scenes=read(U5/'briefs/scene-briefs-f3.json')
    assert scenes['counts']=={'journeys':8,'scene_briefs':50,'palace_managed_records':131,'term_introductions':131,'optional_first_exposure_recalls':18}
    assert len(scenes['scene_briefs'])==50
    assigned=[kid for b in scenes['scene_briefs'] for kid in b['knowledge_ids']]
    assert len(assigned)==len(set(assigned))==131

def test_unit5_f3_journey_continuity_is_locked():
    doc=read(U5/'briefs/journey-briefs-f3.json')
    assert doc['journey_count']==8
    assert [j['journey_id'] for j in doc['journeys']]==[f'U5-J{i}' for i in range(1,9)]
    assert all(j['unit_guide']['name']=='Dr. Imani Reyes' for j in doc['journeys'])
    assert all(j['continuity_object'] and j['opening_image'] and j['ending_payoff'] for j in doc['journeys'])
    assert all(j['status']=='JOURNEY_BRIEF_LOCKED_F3_NO_POLISHED_STORY_PROSE' for j in doc['journeys'])

def test_unit5_f3_preserves_f2_geometry_and_f1_science():
    scenes=read(U5/'briefs/scene-briefs-f3.json')['scene_briefs']
    arch=read(U5/'architecture/palace-architecture-f2.json')['loci']
    canon={r['knowledge_id']:r for r in read(U5/'source/canonical-unit5-f1.json')['canonical_catalog']}
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

def test_unit5_f3_has_no_student_runtime_at_f3():
    status=read(U5/'status-f3.json')
    assert status['status']=='SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED'
    assert status['student_release'] is False and status['preview_release'] is False
    assert (status['journey_count'],status['scene_count'],status['memory_objects'],status['application_challenges'])==(0,0,0,0)
    assert not (U5/'memory-objects.json').exists()
    # Later F4 narrative-stage artifacts may coexist in a mainline repository. Their own
    # stage locks must keep student_release false until finalization.

def test_unit5_f3_recall_distribution_is_sparse():
    scenes=read(U5/'briefs/scene-briefs-f3.json')['scene_briefs']
    per={f'U5-J{i}':0 for i in range(1,9)}
    for b in scenes:
        if b['quick_recall']['enabled']: per[b['journey_id']]+=1
    assert per=={'U5-J1':2,'U5-J2':3,'U5-J3':2,'U5-J4':2,'U5-J5':2,'U5-J6':2,'U5-J7':2,'U5-J8':3}
