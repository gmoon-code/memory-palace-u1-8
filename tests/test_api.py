from fastapi.testclient import TestClient
from backend.main import app

client=TestClient(app)

def test_health():
    data=client.get('/api/health').json()
    assert data['ok'] is True
    assert data['version']=='v2-apbio-0.30.0-u8-f6'

def test_course_registers_all_eight_units():
    data=client.get('/api/course').json()
    assert len(data['units'])==8
    assert data['units'][0]['status']=='STUDENT_READY'
    u2=next(x for x in data['units'] if x['unit_id']=='unit-2')
    assert u2['status']=='STUDENT_READY'
    assert u2['source_status']=='AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5'
    u3=next(x for x in data['units'] if x['unit_id']=='unit-3')
    assert u3['status']=='STUDENT_READY'
    assert u3['source_status']=='AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5_UX_VALIDATED_F6'
    u4=next(x for x in data['units'] if x['unit_id']=='unit-4')
    assert u4['status']=='STUDENT_READY'
    assert u4['source_status']=='AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5_UX_VALIDATED_F6'
    assert u4['architecture_journeys']==7
    assert u4['architecture_loci']==51
    assert u4['student_release'] is True
    u5=next(x for x in data['units'] if x['unit_id']=='unit-5')
    assert u5['status']=='STUDENT_READY'
    assert u5['source_status']=='AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5_UX_VALIDATED_F6'
    assert u5['student_release'] is True and u5['preview_release'] is False
    assert u5['browser_validation']=='PASS_F6' and u5['pipeline_stage']=='UNIT5_CLASSROOM_BROWSER_VALIDATED_F6'
    assert u5['runtime_memory_objects']==131 and u5['application_challenges']==16
    u6=next(x for x in data['units'] if x['unit_id']=='unit-6')
    assert u6['status']=='STUDENT_READY'
    assert u6['source_status']=='AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5_UX_VALIDATED_F6'
    assert u6['student_release'] is True and u6['preview_release'] is False
    assert u6['canonical_lock']=='LOCKED_F1' and u6['pipeline_stage']=='UNIT6_CLASSROOM_BROWSER_VALIDATED_F6'
    assert u6['runtime_memory_objects']==161 and u6['application_challenges']==16
    u7=next(x for x in data['units'] if x['unit_id']=='unit-7')
    assert u7['status']=='STUDENT_READY'
    assert u7['student_release'] is True and u7['preview_release'] is False
    assert u7['journey_count']==6 and u7['scene_count']==55
    assert u7['source_status']=='AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5_UX_VALIDATED_F6'
    assert u7['canonical_lock']=='LOCKED_F1' and u7['pipeline_stage']=='UNIT7_CLASSROOM_BROWSER_VALIDATED_F6'
    assert u7['canonical_records']==215 and u7['ced_atoms']==68
    assert u7['scene_brief_lock']=='LOCKED_F3' and u7['scene_briefs']==55
    assert u7['runtime_memory_objects']==174 and u7['application_challenges']==16
    u8=next(x for x in data['units'] if x['unit_id']=='unit-8')
    assert u8['source_status']=='AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5_UX_VALIDATED_F6'
    assert u8['status']=='STUDENT_READY'
    assert u8['student_release'] is True and u8['preview_release'] is False
    assert u8['pipeline_stage']=='UNIT8_CLASSROOM_BROWSER_VALIDATED_F6'
    assert u8['journey_count']==8 and u8['scene_count']==58
    assert u8['canonical_records']==255 and u8['canonical_records_accounted']==255
    assert u8['runtime_memory_objects']==211 and u8['application_challenges']==13
    assert u8['exact_name_review_targets']==135 and u8['non_exact_palace_records']==76
    assert u8['mixed_discrimination_sets']==40 and u8['mixed_discrimination_questions']==104
    assert u8['architecture_journeys']==8 and u8['architecture_loci']==58 and u8['scene_briefs']==58
    assert u8['narrative_lock'].startswith('LOCKED_F4A_J1_') and u8['narrative_lock'].endswith('LOCKED_F4H_J8') and u8['narrative_journeys']==8

def test_unit1_summary():
    data=client.get('/api/units/unit-1').json()
    assert data['canonical_records']==229
    assert data['memory_objects']==207
    assert data['journeys']==9
    assert data['permanent_loci']==78
    assert data['checkpoint_count']==27
    assert data['application_challenges']==16
    assert data['practice_only_runtime_objects']==8

def test_all_nine_journeys_are_served():
    items=client.get('/api/units/unit-1/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in items]==[f'Z{i}' for i in range(1,10)]
    assert sum(x['scene_count'] for x in items)==78
    for item in items:
        data=client.get(f"/api/units/unit-1/journeys/{item['palace_id']}")
        assert data.status_code==200
        body=data.json()
        assert body['scene_count']==len(body['scenes'])
        assert body['narrative_design']=='V2-NARRATIVE-2.0'

def test_water_reference_is_the_rewritten_story():
    data=client.get('/api/units/unit-1/journeys/Z3').json()
    assert data['story_title']=='The Flooded Sky Hotel'
    assert data['scene_count']==11
    assert data['guide']['name']=='Mara Vale'
    assert data['scenes'][0]['story_paragraphs']
    assert len(data['scenes'][0]['scene_layout']['zones'])==3

def test_application_lab_is_complete():
    data=client.get('/api/units/unit-1/application-lab').json()
    assert data['challenge_count']==16
    assert data['practice_only_runtime_count']==8
    assert len(data['practice_only_runtime_object_ids'])==8
    assert len(data['items'])==16

def test_unit2_student_release_and_future_units_are_registered():
    assert client.get('/api/units/unit-2').status_code==200
    u2=client.get('/api/units/unit-2/journeys').json()['guided_journeys']
    assert [x['palace_id'] for x in u2]==['U2-J1','U2-J2','U2-J3','U2-J4','U2-J5','U2-J6','U2-J7']
    assert client.get('/api/units/unit-2/application-lab').json()['challenge_count']==9

def test_unknown_resources_404():
    assert client.get('/api/units/nope').status_code==404
    assert client.get('/api/units/unit-1/journeys/NOPE').status_code==404
    assert client.get('/api/units/unit-1/objects/NOPE').status_code==404


def test_unit3_released_api_state():
    data=client.get('/api/units/unit-3').json()
    assert data['status']=='STUDENT_READY'
    assert data['canonical_records']==186
    assert data['ced_atoms']==54
    assert data['review_flags_resolved']==30
    assert data['student_release'] is True and data['preview_release'] is False
    assert data['browser_validation']=='PASS_F6'
    assert data['architecture_loci']==54
    assert data['architecture_journeys']==7
    assert data['canonical_records_accounted']==186
    arch=client.get('/api/units/unit-3/architecture')
    assert arch.status_code==200
    assert arch.json()['counts']['permanent_loci']==54
    assert data['scene_briefs']==54
    assert client.get('/api/units/unit-3/scene-briefs').json()['counts']['scene_briefs']==54
    assert client.get('/api/units/unit-3/journey-briefs').json()['journey_count']==7
    journeys=client.get('/api/units/unit-3/journeys').json()['guided_journeys']
    assert [j['palace_id'] for j in journeys]==['U3-J1','U3-J2','U3-J3','U3-J4','U3-J5','U3-J6','U3-J7']
    for i in range(1,8): assert client.get(f'/api/units/unit-3/journeys/U3-J{i}').status_code==200
    assert client.get('/api/units/unit-3/application-lab').json()['challenge_count']==11
    assert client.get('/api/units/unit-3/review-manifest').json()['target_count']==126
    assert client.get('/api/units/unit-3/mixed-discrimination').json()['set_count']==28
    assert client.get('/api/units/unit-3/scope-guards').json()['guard_count']==4
    obj=client.get('/api/units/unit-3/objects/U3-K-001')
    assert obj.status_code==200
    assert obj.json()['canonical_lock']=='LOCKED_F1'


def test_unit4_f5_student_release_preserves_f3_briefs_and_all_seven_journeys():
    data=client.get('/api/units/unit-4').json()
    assert data['status']=='STUDENT_READY'
    assert data['canonical_records']==180
    assert data['ced_atoms']==38
    assert data['review_flags_resolved']==39
    assert data['teacher_ppt_slides']==85
    assert data['student_release'] is True and data['preview_release'] is False
    assert data['runtime_memory_objects']==162 and data['application_challenges']==15
    journeys=client.get('/api/units/unit-4/journeys').json()['guided_journeys']
    assert [j['palace_id'] for j in journeys]==[f'U4-J{i}' for i in range(1,8)]
    for i in range(1,8): assert client.get(f'/api/units/unit-4/journeys/U4-J{i}').status_code==200
    assert client.get('/api/units/unit-4/application-lab').json()['challenge_count']==15
    assert client.get('/api/units/unit-4/review-manifest').json()['target_count']==162
    assert client.get('/api/units/unit-4/mixed-discrimination').json()['set_count']==33
    assert client.get('/api/units/unit-4/scope-guards').json()['guard_count']==3
    assert client.get('/api/units/unit-4/finalization').json()['unaccounted_records']==0
    obj=client.get('/api/units/unit-4/objects/U4-K-001')
    assert obj.status_code==200 and obj.json()['scientific_lock_status']=='LOCKED_F1'
    arch=client.get('/api/units/unit-4/architecture')
    assert arch.status_code==200 and arch.json()['counts']['permanent_loci']==51
    assert client.get('/api/units/unit-4/scene-briefs').json()['counts']['scene_briefs']==51
    assert client.get('/api/units/unit-4/journey-briefs').json()['journey_count']==7


def test_unit5_f5_released_api_state():
    data=client.get('/api/units/unit-5').json()
    assert data['status']=='STUDENT_READY' and data['student_release'] is True and data['preview_release'] is False
    assert data['canonical_records_accounted']==152 and data['runtime_memory_objects']==131 and data['application_challenges']==16
    journeys=client.get('/api/units/unit-5/journeys').json()['guided_journeys']
    assert [j['palace_id'] for j in journeys]==[f'U5-J{i}' for i in range(1,9)]
    assert client.get('/api/units/unit-5/review-manifest').json()['target_count']==130
    assert client.get('/api/units/unit-5/mixed-discrimination').json()['set_count']==32
    assert client.get('/api/units/unit-5/scope-guards').json()['guard_count']==5
    assert client.get('/api/units/unit-5/finalization').json()['unaccounted_records']==0
