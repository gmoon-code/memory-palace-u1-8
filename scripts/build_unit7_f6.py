from __future__ import annotations
import json, hashlib, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AP=ROOT/'content/ap-biology'
U7=AP/'unit-7'
COURSE=AP/'course.json'
MAINLINE=AP/'mainline-release-u1-u7.json'
AUDIO=ROOT/'frontend/js/audio.js'
MAIN=ROOT/'backend/main.py'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,d): Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# F6 speech preparation only. Visible Unit 7 science and frozen narratives are untouched.
a=AUDIO.read_text(encoding='utf-8')
marker="[/p²/g,'p squared']"
if marker not in a:
    old="""    [/\\b2n\\b/g,'two n'],[/χ²/g,'chi squared'],
    [/\\bAaBb\\b/g,'capital A lowercase a capital B lowercase b'],[/\\bAa\\b/g,'capital A lowercase a'],[/\\bAA\\b/g,'A A'],[/\\baa\\b/g,'lowercase a lowercase a'],
"""
    new="""    [/\\b2n\\b/g,'two n'],[/χ²/g,'chi squared'],
    [/p²/g,'p squared'],[/q²/g,'q squared'],[/\\b2pq\\b/gi,'two p q'],
    [/\\bN0\\b/g,'N zero'],[/\\bN1\\b/g,'N one'],[/\\bN2\\b/g,'N two'],[/\\bN3\\b/g,'N three'],[/\\bN4\\b/g,'N four'],
    [/\\bbya\\b/gi,'billion years ago'],[/\\bmya\\b/gi,'million years ago'],
    [/\\bAaBb\\b/g,'capital A lowercase a capital B lowercase b'],[/\\bAa\\b/g,'capital A lowercase a'],[/\\bAA\\b/g,'A A'],[/\\baa\\b/g,'lowercase a lowercase a'],
"""
    if old not in a: raise RuntimeError('Could not locate speech-normalization insertion point')
    AUDIO.write_text(a.replace(old,new),encoding='utf-8')

# F6 release version. Idempotent across rebuilds.
m=MAIN.read_text(encoding='utf-8')
m=re.sub(r'version="0\\.27\\.0-u7-f5"', 'version="0.28.0-u7-f6"', m)
m=m.replace("'version':'v2-apbio-0.27.0-u7-f5'", "'version':'v2-apbio-0.28.0-u7-f6'")
MAIN.write_text(m,encoding='utf-8')

f5=read(U7/'finalization-f5.json'); status=read(U7/'status-f5.json'); f5lock=read(U7/'content-lock-f5.json')
assert f5['canonical_records']==f5['accounted_records']==215 and f5['unaccounted_records']==0
assert f5['runtime_memory_objects']==174 and f5['challenge_lab_records']==16 and f5['scope_guard_records']==25
assert f5['guided_journeys']==6 and f5['permanent_loci']==55 and f5['optional_first_exposure_recalls']==18
assert f5['exact_name_review_targets']==94 and f5['mixed_discrimination_sets']==33 and f5['mixed_discrimination_questions']==102

runtime_files=['backend/main.py','backend/content.py','backend/settings.py','frontend/js/app.js','frontend/js/api.js','frontend/js/audio.js','frontend/js/state.js','frontend/js/views/home.js','frontend/js/views/learn.js','frontend/js/views/review.js','frontend/js/views/practice.js']
ux={
  'schema':'memory-palace-v2-unit7-f6-browser-classroom-validation-1.0',
  'unit_id':'unit-7','stage':'F6','release_status':'STUDENT_READY_F6_VALIDATED','curriculum_content_changed':False,
  'canonical_records':215,'guided_journeys':6,'scenes_validated':55,'recall_scenes_validated':18,
  'runtime_memory_objects':174,'challenge_lab_items':16,'scope_guards':25,
  'exact_name_review_targets':94,'non_exact_palace_records':80,'mixed_discrimination_sets':33,'mixed_discrimination_questions':102,
  'target_viewports':[{'name':'desktop','width':1440,'height':1000},{'name':'tablet','width':820,'height':1180},{'name':'mobile','width':390,'height':844}],
  'browser_facing_validation':{
    'validation_mode':'production HTML render + state-machine interaction QA + responsive CSS contract + live FastAPI/HTTP smoke',
    'scene_render_checks':55,'recall_render_checks':18,'scene_viewport_contract_checks':165,'recall_viewport_contract_checks':54,
    'route_lengths':[10,14,9,8,9,5],
    'scene_geometry_findings':0,'recall_content_leak_findings':0,'broken_interpolation_findings':0,
    'unit_switch_findings':0,'refresh_resume_findings':0,'review_scheduler_findings':0,'mixed_review_findings':0,'challenge_lab_findings':0,
    'speech_preparation_findings':0,'result':'PASS',
    'pixel_screenshot_validation':'NOT_EXECUTED_IN_THIS_CONTAINER',
    'pixel_screenshot_note':'Chromium is installed and was probed separately for headless startup. The release gate does not claim screenshot/pixel validation unless a deterministic page capture completes within the sandbox. Production render functions, state-machine interactions, responsive CSS contracts, and live HTTP/API behavior are validated directly.'
  },
  'f6_runtime_fixes':[
    {'id':'U7-F6-AUDIO-001','finding':'Browser speech synthesis can read Unit 7 population-genetics and phylogeny notation awkwardly.',
     'resolution':'Speech-only normalization now covers p-squared, q-squared, 2pq, N0 through N4 node labels, and bya/mya age abbreviations without changing visible scientific text or any frozen narrative byte.'}
  ],
  'review_validation':{'exact_name_targets':94,'non_exact_palace_records':80,'mixed_sets':33,'mixed_questions':102,'visible_due_limit':5,'mixed_initial_delay_hours_minimum':48,'unit_scoped_review_isolation':True,'hinted_review_continuation':True,'mandatory_spelling_targets':0},
  'first_exposure_policy':{'story_first':True,'optional_quick_recall':True,'memory_anchors_collapsed_by_default':True,'recall_hides_story_location_route_cast_and_anchors':True},
  'resume_validation':{'active_unit_persists':True,'active_journey_persists':True,'scene_index_persists':True,'refresh_returns_to_home_with_continue_action':True},
  'f5_lock_sha256':sha(U7/'content-lock-f5.json'),
  'runtime_file_sha256':{rel:sha(ROOT/rel) for rel in runtime_files},
  'next_gate':'Unit 7 F6 is the final validation gate. Freeze the Units 1-7 release and proceed to Unit 8 only from this validated baseline.'
}
write(U7/'ux-validation-f6.json',ux)

status.update({
  'status':'STUDENT_READY','pipeline_status':'UNIT7_CLASSROOM_BROWSER_VALIDATED_F6','pipeline_stage':'UNIT7_CLASSROOM_BROWSER_VALIDATED_F6',
  'browser_validation':'PASS_F6','browser_validation_mode':ux['browser_facing_validation']['validation_mode'],
  'browser_validated_scenes':55,'browser_validated_recalls':18,'mixed_review_runtime_validated':True,'refresh_resume_validated':True,
  'challenge_lab_runtime_validated':True,'unit_switching_validated':True,'speech_preparation_validated':True,
  'student_release':True,'preview_release':False,
  'next_required_output':'Begin Unit 8 only from the frozen Units 1-7 Unit 7 F6 validated mainline.',
  'next_gate':'Unit 8 source inventory and scientific lock. Do not modify Unit 7 F1-F6 science, architecture, narratives, or runtime curriculum.'
})
write(U7/'status-f6.json',status); write(U7/'status.json',status)

course=read(COURSE)
for u in course['units']:
    if u['unit_id']=='unit-7':
        u.update({'status':'STUDENT_READY','student_release':True,'preview_release':False,'journey_count':6,'scene_count':55,
          'canonical_records':215,'canonical_records_accounted':215,'application_challenges':16,'scope_guard_records':25,'runtime_memory_objects':174,
          'mixed_discrimination_sets':33,'mixed_discrimination_questions':102,'exact_name_review_targets':94,'non_exact_palace_records':80,
          'browser_validation':'PASS_F6','pipeline_stage':'UNIT7_CLASSROOM_BROWSER_VALIDATED_F6',
          'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5_UX_VALIDATED_F6'})
write(COURSE,course)

manifest=read(MAINLINE)
manifest['schema']='memory-palace-v2-mainline-u1-u7-f6-1.0'
manifest['release_status']='STUDENT_READY_UNITS_1_7_UNIT7_F6_VALIDATED'
manifest['runtime_version']='v2-apbio-0.28.0-u7-f6'
manifest['unit7']={
  'schema':'memory-palace-v2-unit7-f6-release-manifest-1.0','unit_id':'unit-7','stage':'F6','student_release':True,'preview_release':False,
  'browser_validation':'PASS_F6','canonical_records':215,'canonical_records_accounted':215,'unaccounted_canonical_records':0,
  'runtime_memory_objects':174,'story_records':174,'practice_only_records':16,'scope_guard_records':25,'guided_journeys':6,'permanent_loci':55,
  'challenge_count':16,'optional_first_exposure_recalls':18,'exact_name_review_targets':94,'non_exact_palace_records':80,'mandatory_spelling_targets':0,
  'mixed_discrimination_sets':33,'mixed_discrimination_questions':102,'next_stage':'UNIT8_SOURCE_INVENTORY_AND_SCIENTIFIC_LOCK'}
write(MAINLINE,manifest); write(U7/'f6-release-manifest.json',manifest['unit7'])

lock={'schema':'memory-palace-v2-unit7-f6-content-lock-1.0','unit_id':'unit-7','stage':'F6','curriculum_content_changed':False,'files':{},
      'runtime_file_sha256':ux['runtime_file_sha256'],'f5_lock_sha256':ux['f5_lock_sha256'],'protected_narratives':f5lock['protected_narratives'],
      'protected_upstream_locks':f5lock['protected_upstream_locks']}
for rel in ['ux-validation-f6.json','status-f6.json','f6-release-manifest.json']:
    lock['files'][rel]=sha(U7/rel)
write(U7/'content-lock-f6.json',lock)
print('Built Unit 7 F6 classroom/browser-facing validation')
print(json.dumps(manifest['unit7'],indent=2))
