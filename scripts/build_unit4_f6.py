from __future__ import annotations
import json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content'/'ap-biology'/'unit-4'
AP=ROOT/'content'/'ap-biology'
COURSE=AP/'course.json'
MAINLINE=AP/'mainline-release-u1-u4.json'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,d): Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

f5=read(U4/'finalization-f5.json')
status=read(U4/'status-f5.json')
assert f5['canonical_records']==180 and f5['accounted_records']==180 and f5['unaccounted_records']==0
assert f5['runtime_memory_objects']==162 and f5['challenge_lab_records']==15 and f5['scope_guard_records']==3
assert f5['guided_journeys']==7 and f5['permanent_loci']==51

ux={
  'schema':'memory-palace-v2-unit4-f6-browser-classroom-validation-1.0',
  'unit_id':'unit-4','stage':'F6','release_status':'STUDENT_READY_F6_VALIDATED',
  'curriculum_content_changed':False,
  'canonical_records':180,'guided_journeys':7,'scenes_validated':51,'recall_scenes_validated':18,
  'runtime_memory_objects':162,'challenge_lab_items':15,'scope_guards':3,
  'exact_name_review_targets':162,'mixed_discrimination_sets':33,'mixed_discrimination_questions':99,
  'target_viewports':[
    {'name':'desktop','width':1440,'height':1000},
    {'name':'tablet','width':820,'height':1180},
    {'name':'mobile','width':390,'height':844}
  ],
  'browser_facing_validation':{
    'validation_mode':'runtime HTML render + state-machine interaction QA + responsive CSS contract + live FastAPI smoke',
    'scene_render_checks':51,
    'recall_render_checks':18,
    'scene_viewport_contract_checks':153,
    'recall_viewport_contract_checks':54,
    'route_lengths':[6,6,7,6,8,8,10],
    'scene_geometry_findings':0,
    'recall_content_leak_findings':0,
    'broken_interpolation_findings':0,
    'unit_switch_findings':0,
    'refresh_resume_findings':0,
    'review_scheduler_findings':0,
    'challenge_lab_findings':0,
    'result':'PASS',
    'pixel_screenshot_validation':'NOT_EXECUTED_IN_THIS_CONTAINER',
    'pixel_screenshot_note':'The installed Chromium executable does not complete even an about:blank headless render in this sandbox. F6 therefore records functional browser-facing and responsive-contract validation without claiming screenshot/pixel validation.'
  },
  'f6_runtime_fixes':[
    {'id':'U4-F6-UI-001','finding':'After an exact-name Review hint revealed the answer, the item was rescheduled but the learner had no direct control to advance to the next due review.','resolution':'Hinted exact-name Review now provides a Continue review button that immediately advances to the next due item.'},
    {'id':'U4-F6-UI-002','finding':'Browser speech synthesis could read frequent Unit 4 abbreviations and phase labels awkwardly.','resolution':'Speech-only normalization now covers DNA, GPCR, GDP, GTP, cAMP, CDK/CDKs, APC/APCs, G1, G2, and G0 without changing visible scientific text.'}
  ],
  'review_validation':{
    'exact_name_targets':162,'mixed_sets':33,'mixed_questions':99,'visible_due_limit':5,
    'mixed_initial_delay_hours_minimum':48,'unit_scoped_review_isolation':True,'hinted_review_continuation':True
  },
  'first_exposure_policy':{
    'story_first':True,'optional_quick_recall':True,'memory_anchors_collapsed_by_default':True,
    'recall_hides_story_location_route_cast_and_anchors':True
  },
  'resume_validation':{'active_unit_persists':True,'active_journey_persists':True,'scene_index_persists':True,'refresh_returns_to_home_with_continue_action':True},
  'f5_lock_sha256':sha(U4/'content-lock-f5.json'),
  'runtime_file_sha256':{
    'frontend/js/app.js':sha(ROOT/'frontend/js/app.js'),
    'frontend/js/audio.js':sha(ROOT/'frontend/js/audio.js'),
    'frontend/js/state.js':sha(ROOT/'frontend/js/state.js'),
    'frontend/js/views/learn.js':sha(ROOT/'frontend/js/views/learn.js'),
    'frontend/js/views/review.js':sha(ROOT/'frontend/js/views/review.js'),
    'frontend/js/views/practice.js':sha(ROOT/'frontend/js/views/practice.js')
  },
  'next_gate':'Begin Unit 5 source inventory, scientific atomization, AP scope mapping, conflict/misconception audit, and canonical scientific lock before any Unit 5 palace or narrative generation.'
}
write(U4/'ux-validation-f6.json',ux)

status.update({
  'pipeline_status':'UNIT4_CLASSROOM_BROWSER_VALIDATED_F6','pipeline_stage':'UNIT4_CLASSROOM_BROWSER_VALIDATED_F6',
  'browser_validation':'PASS_F6','browser_validation_mode':ux['browser_facing_validation']['validation_mode'],
  'browser_validated_scenes':51,'browser_validated_recalls':18,'mixed_review_runtime_validated':True,
  'refresh_resume_validated':True,'challenge_lab_runtime_validated':True,'unit_switching_validated':True,
  'student_release':True,'preview_release':False,
  'next_required_output':'Begin Unit 5 source inventory, scientific atomization, AP scope mapping, conflict/misconception audit, and canonical lock.',
  'next_gate':'Unit 5 scientific-lock pipeline. Do not generate Unit 5 narratives before the canonical lock passes.'
})
write(U4/'status-f6.json',status); write(U4/'status.json',status)

course=read(COURSE)
for u in course['units']:
    if u['unit_id']=='unit-4':
        u.update({
          'status':'STUDENT_READY','student_release':True,'preview_release':False,
          'journey_count':7,'scene_count':51,'canonical_records':180,'canonical_records_accounted':180,
          'application_challenges':15,'scope_guard_records':3,'runtime_memory_objects':162,
          'browser_validation':'PASS_F6','pipeline_stage':'UNIT4_CLASSROOM_BROWSER_VALIDATED_F6',
          'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5_UX_VALIDATED_F6'
        })
write(COURSE,course)

manifest=read(MAINLINE)
manifest['schema']='memory-palace-v2-mainline-u1-u4-f6-1.0'
manifest['release_status']='STUDENT_READY_UNITS_1_4_U4_F6_VALIDATED'
manifest['unit4']={
  'schema':'memory-palace-v2-unit4-f6-release-manifest-1.0','unit_id':'unit-4','stage':'F6',
  'student_release':True,'preview_release':False,'browser_validation':'PASS_F6',
  'canonical_records':180,'canonical_records_accounted':180,'unaccounted_canonical_records':0,
  'runtime_memory_objects':162,'story_records':162,'practice_only_records':15,'scope_guard_records':3,
  'guided_journeys':7,'permanent_loci':51,'challenge_count':15,'exact_name_review_targets':162,
  'mandatory_spelling_targets':0,'mixed_discrimination_sets':33,'mixed_discrimination_questions':99,
  'next_stage':'UNIT5_SOURCE_INVENTORY_AND_SCIENTIFIC_LOCK'
}
write(MAINLINE,manifest)

lock={'schema':'memory-palace-v2-unit4-f6-content-lock-1.0','unit_id':'unit-4','stage':'F6','curriculum_content_changed':False,'files':{}}
for rel in ['ux-validation-f6.json','status-f6.json']:
    lock['files'][rel]=sha(U4/rel)
lock['runtime_file_sha256']=ux['runtime_file_sha256']
lock['f5_lock_sha256']=ux['f5_lock_sha256']
write(U4/'content-lock-f6.json',lock)
print('Built Unit 4 F6 classroom/browser-facing validation')
