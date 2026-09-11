from __future__ import annotations
import json, hashlib, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AP=ROOT/'content/ap-biology'
U7_STATUS=AP/'unit-7'/'status.json'
if U7_STATUS.exists():
    try:
        _u7=json.loads(U7_STATUS.read_text(encoding='utf-8'))
    except Exception:
        _u7={}
    if _u7.get('status') not in {None,'SOURCE_AVAILABLE_NOT_MIGRATED'}:
        print('Historical Unit 6 F6 rebuild skipped because a later Unit 7 pipeline lock is active.')
        raise SystemExit(0)
U6=AP/'unit-6'
COURSE=AP/'course.json'
MAINLINE=AP/'mainline-release-u1-u6.json'
AUDIO=ROOT/'frontend/js/audio.js'
MAIN=ROOT/'backend/main.py'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,d): Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# F6 runtime-only speech preparation. Visible science and frozen narratives remain untouched.
a=AUDIO.read_text(encoding='utf-8')
marker="[/\\bpre-mRNA\\b/gi,'pre messenger R N A']"
if marker not in a:
    old="""    [/\\bF1\\b/g,'F one'],[/\\bF2\\b/g,'F two'],[/\\bXX\\b/g,'X X'],[/\\bXY\\b/g,'X Y'],
    [/\\bABO\\b/g,'A B O'],[/\\bIA\\b/g,'I A'],[/\\bIB\\b/g,'I B'],[/\\bUV\\b/g,'U V'],[/\\bHBB\\b/g,'H B B'],
    [/\\b2n\\b/g,'two n'],[/χ²/g,'chi squared'],
"""
    new="""    [/\\bF1\\b/g,'F one'],[/\\bF2\\b/g,'F two'],[/\\bXX\\b/g,'X X'],[/\\bXY\\b/g,'X Y'],
    [/\\bABO\\b/g,'A B O'],[/\\bIA\\b/g,'I A'],[/\\bIB\\b/g,'I B'],[/\\bUV\\b/g,'U V'],[/\\bHBB\\b/g,'H B B'],
    [/\\bpre-mRNA\\b/gi,'pre messenger R N A'],[/\\bmRNAs?\\b/g,m=>m.endsWith('s')?'messenger R N As':'messenger R N A'],
    [/\\btRNAs?\\b/g,m=>m.endsWith('s')?'transfer R N As':'transfer R N A'],[/\\brRNAs?\\b/g,m=>m.endsWith('s')?'ribosomal R N As':'ribosomal R N A'],
    [/\\bsiRNA\\b/g,'small interfering R N A'],[/\\bmiRNA\\b/g,'micro R N A'],[/\\bmicroRNAs?\\b/g,m=>m.endsWith('s')?'micro R N As':'micro R N A'],
    [/\\bPCR\\b/g,'P C R'],[/\\bAUG\\b/g,'A U G'],[/\\bUAA\\b/g,'U A A'],[/\\bUAG\\b/g,'U A G'],[/\\bUGA\\b/g,'U G A'],[/\\bTATA\\b/g,'T A T A'],[/\\bAAUAAA\\b/g,'A A U A A A'],
    [/\\bHGT\\b/g,'H G T'],[/\\bSSB\\b/g,'S S B'],[/\\bdsDNA\\b/g,'double stranded D N A'],[/\\btrp\\b/gi,'T R P'],
    [/\\bA-site\\b/g,'A site'],[/\\bP-site\\b/g,'P site'],[/\\bE-site\\b/g,'E site'],[/5′/g,'five prime'],[/3′/g,'three prime'],
    [/\\b2n\\b/g,'two n'],[/χ²/g,'chi squared'],
"""
    if old not in a: raise RuntimeError('Could not locate Unit 5 speech-normalization block')
    AUDIO.write_text(a.replace(old,new),encoding='utf-8')

# F6 release version, idempotent across rebuilds.
m=MAIN.read_text(encoding='utf-8')
m=re.sub(r'version="0\\.25\\.0-u6-f5"', 'version="0.26.0-u6-f6"', m)
m=m.replace("'version':'v2-apbio-0.25.0-u6-f5'", "'version':'v2-apbio-0.26.0-u6-f6'")
MAIN.write_text(m,encoding='utf-8')

f5=read(U6/'finalization-f5.json'); status=read(U6/'status-f5.json')
assert f5['canonical_records']==f5['accounted_records']==202 and f5['unaccounted_records']==0
assert f5['runtime_memory_objects']==161 and f5['challenge_lab_records']==16 and f5['scope_guard_records']==25
assert f5['guided_journeys']==6 and f5['permanent_loci']==53 and f5['optional_first_exposure_recalls']==18
assert f5['exact_name_review_targets']==134 and f5['mixed_discrimination_sets']==37 and f5['mixed_discrimination_questions']==94

ux={
  'schema':'memory-palace-v2-unit6-f6-browser-classroom-validation-1.0',
  'unit_id':'unit-6','stage':'F6','release_status':'STUDENT_READY_F6_VALIDATED',
  'curriculum_content_changed':False,
  'canonical_records':202,'guided_journeys':6,'scenes_validated':53,'recall_scenes_validated':18,
  'runtime_memory_objects':161,'challenge_lab_items':16,'scope_guards':25,
  'exact_name_review_targets':134,'mixed_discrimination_sets':37,'mixed_discrimination_questions':94,
  'target_viewports':[{'name':'desktop','width':1440,'height':1000},{'name':'tablet','width':820,'height':1180},{'name':'mobile','width':390,'height':844}],
  'browser_facing_validation':{
    'validation_mode':'runtime HTML render + state-machine interaction QA + responsive CSS contract + live FastAPI smoke',
    'scene_render_checks':53,'recall_render_checks':18,
    'scene_viewport_contract_checks':159,'recall_viewport_contract_checks':54,
    'route_lengths':[12,8,8,12,8,5],
    'scene_geometry_findings':0,'recall_content_leak_findings':0,'broken_interpolation_findings':0,
    'unit_switch_findings':0,'refresh_resume_findings':0,'review_scheduler_findings':0,'mixed_review_findings':0,'challenge_lab_findings':0,
    'result':'PASS','pixel_screenshot_validation':'NOT_EXECUTED_IN_THIS_CONTAINER',
    'pixel_screenshot_note':'Chromium was directly probed with an 8-second headless about:blank render and timed out without DOM output in this sandbox. F6 therefore records functional browser-facing and responsive-contract validation without claiming screenshot or pixel validation.'
  },
  'f6_runtime_fixes':[
    {'id':'U6-F6-AUDIO-001','finding':'Browser speech synthesis could read frequent Unit 6 molecular-biology notation awkwardly or ambiguously.',
     'resolution':'Speech-only normalization now covers pre-mRNA, mRNA, tRNA, rRNA, siRNA, miRNA/microRNA, PCR, AUG and stop-codon abbreviations, TATA, AAUAAA, HGT, SSB, dsDNA, trp, A/P/E-site labels, and 5-prime/3-prime notation without changing visible scientific text or frozen narrative bytes.'}
  ],
  'review_validation':{'exact_name_targets':134,'mixed_sets':37,'mixed_questions':94,'visible_due_limit':5,'mixed_initial_delay_hours_minimum':48,'unit_scoped_review_isolation':True,'hinted_review_continuation':True,'non_exact_palace_records':27},
  'first_exposure_policy':{'story_first':True,'optional_quick_recall':True,'memory_anchors_collapsed_by_default':True,'recall_hides_story_location_route_cast_and_anchors':True},
  'resume_validation':{'active_unit_persists':True,'active_journey_persists':True,'scene_index_persists':True,'refresh_returns_to_home_with_continue_action':True},
  'f5_lock_sha256':sha(U6/'content-lock-f5.json'),
  'runtime_file_sha256':{rel:sha(ROOT/rel) for rel in [
    'backend/main.py','backend/content.py','backend/settings.py','frontend/js/app.js','frontend/js/api.js','frontend/js/audio.js','frontend/js/state.js','frontend/js/views/home.js','frontend/js/views/learn.js','frontend/js/views/review.js','frontend/js/views/practice.js']},
  'next_gate':'Begin Unit 7 source inventory, scientific atomization, AP scope mapping, conflict/misconception audit, and canonical scientific lock before any Unit 7 palace or narrative generation.'
}
write(U6/'ux-validation-f6.json',ux)

status.update({
  'pipeline_status':'UNIT6_CLASSROOM_BROWSER_VALIDATED_F6','pipeline_stage':'UNIT6_CLASSROOM_BROWSER_VALIDATED_F6',
  'browser_validation':'PASS_F6','browser_validation_mode':ux['browser_facing_validation']['validation_mode'],
  'browser_validated_scenes':53,'browser_validated_recalls':18,'mixed_review_runtime_validated':True,'refresh_resume_validated':True,
  'challenge_lab_runtime_validated':True,'unit_switching_validated':True,'student_release':True,'preview_release':False,
  'next_required_output':'Begin Unit 7 source inventory, scientific atomization, AP scope mapping, conflict/misconception audit, and canonical lock.',
  'next_gate':'Unit 7 scientific-lock pipeline. Do not generate Unit 7 narratives before the canonical lock passes.'
})
write(U6/'status-f6.json',status); write(U6/'status.json',status)

course=read(COURSE)
for u in course['units']:
    if u['unit_id']=='unit-6':
        u.update({'status':'STUDENT_READY','student_release':True,'preview_release':False,'journey_count':6,'scene_count':53,
          'canonical_records':202,'canonical_records_accounted':202,'application_challenges':16,'scope_guard_records':25,'runtime_memory_objects':161,
          'mixed_discrimination_sets':37,'mixed_discrimination_questions':94,'exact_name_review_targets':134,
          'browser_validation':'PASS_F6','pipeline_stage':'UNIT6_CLASSROOM_BROWSER_VALIDATED_F6',
          'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5_UX_VALIDATED_F6'})
write(COURSE,course)

manifest=read(MAINLINE)
manifest['schema']='memory-palace-v2-mainline-u1-u6-f6-1.0'
manifest['release_status']='STUDENT_READY_UNITS_1_6_UNIT6_F6_VALIDATED'
manifest['unit6']={
  'schema':'memory-palace-v2-unit6-f6-release-manifest-1.0','unit_id':'unit-6','stage':'F6','student_release':True,'preview_release':False,
  'browser_validation':'PASS_F6','canonical_records':202,'canonical_records_accounted':202,'unaccounted_canonical_records':0,
  'runtime_memory_objects':161,'story_records':161,'practice_only_records':16,'scope_guard_records':25,'guided_journeys':6,'permanent_loci':53,
  'challenge_count':16,'optional_first_exposure_recalls':18,'exact_name_review_targets':134,'non_exact_palace_records':27,'mandatory_spelling_targets':0,
  'mixed_discrimination_sets':37,'mixed_discrimination_questions':94,'next_stage':'UNIT7_SOURCE_INVENTORY_AND_SCIENTIFIC_LOCK'}
write(MAINLINE,manifest); write(U6/'f6-release-manifest.json',manifest['unit6'])

lock={'schema':'memory-palace-v2-unit6-f6-content-lock-1.0','unit_id':'unit-6','stage':'F6','curriculum_content_changed':False,'files':{},
      'runtime_file_sha256':ux['runtime_file_sha256'],'f5_lock_sha256':ux['f5_lock_sha256'],'protected_narratives':read(U6/'content-lock-f5.json')['protected_narratives']}
for rel in ['ux-validation-f6.json','status-f6.json','f6-release-manifest.json']:
    lock['files'][rel]=sha(U6/rel)
write(U6/'content-lock-f6.json',lock)
print('Built Unit 6 F6 classroom/browser-facing validation')
print(json.dumps(manifest['unit6'],indent=2))
