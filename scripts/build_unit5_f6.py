from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'
AP=ROOT/'content'/'ap-biology'
COURSE=AP/'course.json'
MAINLINE=AP/'mainline-release-u1-u5.json'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,d): Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

f5=read(U5/'finalization-f5.json')
status=read(U5/'status-f5.json')
assert f5['canonical_records']==152 and f5['accounted_records']==152 and f5['unaccounted_records']==0
assert f5['runtime_memory_objects']==131 and f5['challenge_lab_records']==16 and f5['scope_guard_records']==5
assert f5['guided_journeys']==8 and f5['permanent_loci']==50
assert f5['exact_name_review_targets']==130 and f5['mixed_discrimination_sets']==32 and f5['mixed_discrimination_questions']==79

ux={
  'schema':'memory-palace-v2-unit5-f6-browser-classroom-validation-1.0',
  'unit_id':'unit-5','stage':'F6','release_status':'STUDENT_READY_F6_VALIDATED',
  'curriculum_content_changed':False,
  'canonical_records':152,'guided_journeys':8,'scenes_validated':50,'recall_scenes_validated':18,
  'runtime_memory_objects':131,'challenge_lab_items':16,'scope_guards':5,
  'exact_name_review_targets':130,'mixed_discrimination_sets':32,'mixed_discrimination_questions':79,
  'target_viewports':[
    {'name':'desktop','width':1440,'height':1000},
    {'name':'tablet','width':820,'height':1180},
    {'name':'mobile','width':390,'height':844}
  ],
  'browser_facing_validation':{
    'validation_mode':'runtime HTML render + state-machine interaction QA + responsive CSS contract + live FastAPI smoke',
    'scene_render_checks':50,
    'recall_render_checks':18,
    'scene_viewport_contract_checks':150,
    'recall_viewport_contract_checks':54,
    'route_lengths':[5,10,4,7,4,7,6,7],
    'scene_geometry_findings':0,
    'recall_content_leak_findings':0,
    'broken_interpolation_findings':0,
    'unit_switch_findings':0,
    'refresh_resume_findings':0,
    'review_scheduler_findings':0,
    'mixed_review_findings':0,
    'challenge_lab_findings':0,
    'result':'PASS',
    'pixel_screenshot_validation':'NOT_EXECUTED_IN_THIS_CONTAINER',
    'pixel_screenshot_note':'The installed Chromium executable times out even on an about:blank headless render in this sandbox. F6 therefore records functional browser-facing and responsive-contract validation without claiming screenshot or pixel validation.'
  },
  'f6_runtime_fixes':[
    {
      'id':'U5-F6-AUDIO-001',
      'finding':'Browser speech synthesis could read frequent Unit 5 genetics and statistics notation awkwardly or ambiguously.',
      'resolution':'Speech-only normalization now covers RNA, F1, F2, XX, XY, ABO, IA, IB, UV, HBB, 2n, chi-square notation, and common genotype strings such as AA, Aa, aa, and AaBb without changing visible scientific text.'
    }
  ],
  'review_validation':{
    'exact_name_targets':130,'mixed_sets':32,'mixed_questions':79,'visible_due_limit':5,
    'mixed_initial_delay_hours_minimum':48,'unit_scoped_review_isolation':True,
    'hinted_review_continuation':True,'non_exact_palace_records':1
  },
  'first_exposure_policy':{
    'story_first':True,'optional_quick_recall':True,'memory_anchors_collapsed_by_default':True,
    'recall_hides_story_location_route_cast_and_anchors':True
  },
  'resume_validation':{
    'active_unit_persists':True,'active_journey_persists':True,'scene_index_persists':True,
    'refresh_returns_to_home_with_continue_action':True
  },
  'f5_lock_sha256':sha(U5/'content-lock-f5.json'),
  'runtime_file_sha256':{
    'backend/main.py':sha(ROOT/'backend/main.py'),
    'frontend/js/app.js':sha(ROOT/'frontend/js/app.js'),
    'frontend/js/api.js':sha(ROOT/'frontend/js/api.js'),
    'frontend/js/audio.js':sha(ROOT/'frontend/js/audio.js'),
    'frontend/js/state.js':sha(ROOT/'frontend/js/state.js'),
    'frontend/js/views/home.js':sha(ROOT/'frontend/js/views/home.js'),
    'frontend/js/views/learn.js':sha(ROOT/'frontend/js/views/learn.js'),
    'frontend/js/views/review.js':sha(ROOT/'frontend/js/views/review.js'),
    'frontend/js/views/practice.js':sha(ROOT/'frontend/js/views/practice.js')
  },
  'next_gate':'Begin Unit 6 source inventory, scientific atomization, AP scope mapping, conflict/misconception audit, and canonical scientific lock before any Unit 6 palace or narrative generation.'
}
write(U5/'ux-validation-f6.json',ux)

status.update({
  'pipeline_status':'UNIT5_CLASSROOM_BROWSER_VALIDATED_F6','pipeline_stage':'UNIT5_CLASSROOM_BROWSER_VALIDATED_F6',
  'browser_validation':'PASS_F6','browser_validation_mode':ux['browser_facing_validation']['validation_mode'],
  'browser_validated_scenes':50,'browser_validated_recalls':18,'mixed_review_runtime_validated':True,
  'refresh_resume_validated':True,'challenge_lab_runtime_validated':True,'unit_switching_validated':True,
  'student_release':True,'preview_release':False,
  'next_required_output':'Begin Unit 6 source inventory, scientific atomization, AP scope mapping, conflict/misconception audit, and canonical lock.',
  'next_gate':'Unit 6 scientific-lock pipeline. Do not generate Unit 6 narratives before the canonical lock passes.'
})
write(U5/'status-f6.json',status); write(U5/'status.json',status)

course=read(COURSE)
for u in course['units']:
    if u['unit_id']=='unit-5':
        u.update({
          'status':'STUDENT_READY','student_release':True,'preview_release':False,
          'journey_count':8,'scene_count':50,'canonical_records':152,'canonical_records_accounted':152,
          'application_challenges':16,'scope_guard_records':5,'runtime_memory_objects':131,
          'mixed_discrimination_sets':32,'mixed_discrimination_questions':79,'exact_name_review_targets':130,
          'browser_validation':'PASS_F6','pipeline_stage':'UNIT5_CLASSROOM_BROWSER_VALIDATED_F6',
          'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5_UX_VALIDATED_F6'
        })
write(COURSE,course)

manifest=read(MAINLINE)
manifest['schema']='memory-palace-v2-mainline-u1-u5-f6-1.0'
manifest['release_status']='STUDENT_READY_UNITS_1_5_UNIT5_F6_VALIDATED'
manifest['unit5']={
  'schema':'memory-palace-v2-unit5-f6-release-manifest-1.0','unit_id':'unit-5','stage':'F6',
  'student_release':True,'preview_release':False,'browser_validation':'PASS_F6',
  'canonical_records':152,'canonical_records_accounted':152,'unaccounted_canonical_records':0,
  'runtime_memory_objects':131,'story_records':131,'practice_only_records':16,'scope_guard_records':5,
  'guided_journeys':8,'permanent_loci':50,'challenge_count':16,'exact_name_review_targets':130,
  'non_exact_palace_records':1,'mandatory_spelling_targets':0,'mixed_discrimination_sets':32,
  'mixed_discrimination_questions':79,'next_stage':'UNIT6_SOURCE_INVENTORY_AND_SCIENTIFIC_LOCK'
}
write(MAINLINE,manifest)
write(U5/'f6-release-manifest.json',manifest['unit5'])

lock={
  'schema':'memory-palace-v2-unit5-f6-content-lock-1.0','unit_id':'unit-5','stage':'F6',
  'curriculum_content_changed':False,'files':{},
  'runtime_file_sha256':ux['runtime_file_sha256'],'f5_lock_sha256':ux['f5_lock_sha256']
}
for rel in ['ux-validation-f6.json','status-f6.json','f6-release-manifest.json']:
    lock['files'][rel]=sha(U5/rel)
write(U5/'content-lock-f6.json',lock)
print('Built Unit 5 F6 classroom/browser-facing validation')
print(json.dumps(manifest['unit5'],indent=2))
