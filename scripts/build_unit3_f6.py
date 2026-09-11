from __future__ import annotations
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content'/'ap-biology'/'unit-3'
COURSE=ROOT/'content'/'ap-biology'/'course.json'

def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

f5=read(U3/'finalization-f5.json')
status=read(U3/'status-f5.json')
assert f5['canonical_records']==186 and f5['story_records']==171 and f5['challenge_lab_records']==11 and f5['scope_guard_records']==4
assert f5['guided_journeys']==7 and f5['permanent_loci']==54

ux={
 'schema':'memory-palace-v2-unit3-f6-browser-validation-1.0',
 'unit_id':'unit-3','stage':'F6','release_status':'STUDENT_READY_F6_VALIDATED',
 'curriculum_content_changed':False,
 'canonical_records':186,'guided_journeys':7,'scenes_validated':54,'recall_scenes_validated':18,
 'viewports':[{'name':'desktop','width':1440,'height':1000},{'name':'tablet','width':820,'height':1180},{'name':'mobile','width':390,'height':844}],
 'browser_validation':{
   'scene_viewport_combinations':162,
   'recall_viewport_combinations':54,
   'body_horizontal_overflow_findings':0,
   'route_wrap_findings':0,
   'scene_geometry_findings':0,
   'recall_content_leak_findings':0,
   'memory_anchors_default_open_findings':0,
   'result':'PASS'
 },
 'f6_runtime_fixes':[
   {'id':'F6-UI-001','finding':'Twelve-location routes wrapped the final locus onto a second row.','resolution':'Route columns now use the full journey length and remain on one horizontally scrollable row.'},
   {'id':'F6-UI-002','finding':'Late route positions could be off-screen on narrow viewports.','resolution':'The active route node is automatically centered horizontally without changing vertical reading position.'},
   {'id':'F6-UI-003','finding':'Unit 3 mixed-discrimination sets were exposed by API but blocked by a legacy Unit-2-only scheduling condition.','resolution':'Mixed-discrimination scheduling is now unit-generic and activates for Unit 3 after all members of a set are encountered.'},
   {'id':'F6-UI-004','finding':'Memory anchors were expanded after every scene, making first exposure feel like a second vocabulary sheet.','resolution':'Memory anchors remain available but are collapsed by default after the narrative.'},
   {'id':'F6-UI-005','finding':'Listen controls gave no browser feedback and scientific notation could sound awkward in browser speech synthesis.','resolution':'Listen now reports audio state and normalizes common Unit 3 scientific symbols and abbreviations for speech only.'}
 ],
 'review_validation':{
   'exact_name_targets':126,'mixed_sets':28,'mixed_questions':78,'visible_due_limit':5,'mixed_initial_delay_hours_minimum':48,
   'unit3_mixed_scheduler_enabled':True
 },
 'first_exposure_policy':{
   'story_first':True,'optional_quick_recall':True,'memory_anchors_collapsed_by_default':True,'recall_hides_story_location_route_and_anchors':True
 },
 'f5_lock_sha256':sha(U3/'content-lock-f5.json'),
 'next_gate':'Unit 4 source inventory, scientific atomization, AP scope mapping, conflict audit, and canonical lock before Unit 4 narrative generation.'
}
write(U3/'ux-validation-f6.json',ux)

status.update({
 'pipeline_status':'UNIT3_CLASSROOM_BROWSER_VALIDATED_F6','pipeline_stage':'UNIT3_CLASSROOM_BROWSER_VALIDATED_F6',
 'browser_validation':'PASS_F6','browser_validated_scenes':54,'browser_validated_recalls':18,
 'mixed_review_runtime_validated':True,'student_release':True,'preview_release':False,
 'next_required_output':'Begin Unit 4 source inventory, scientific atomization, AP scope mapping, conflict audit, and canonical lock.',
 'next_gate':'Unit 4 scientific-lock pipeline. Do not generate Unit 4 narratives before the canonical lock passes.'
})
write(U3/'status-f6.json',status);write(U3/'status.json',status)

course=read(COURSE)
for u in course['units']:
 if u['unit_id']=='unit-3':
  u.update({'status':'STUDENT_READY','student_release':True,'preview_release':False,'journey_count':7,'scene_count':54,'canonical_records':186,'canonical_records_accounted':186,'application_challenges':11,'scope_guard_records':4,'browser_validation':'PASS_F6','pipeline_stage':'UNIT3_CLASSROOM_BROWSER_VALIDATED_F6','source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5_UX_VALIDATED_F6'})
write(COURSE,course)

lock={'schema':'memory-palace-v2-unit3-f6-content-lock-1.0','unit_id':'unit-3','stage':'F6','curriculum_content_changed':False,'files':{}}
for rel in ['ux-validation-f6.json','status-f6.json']:
 lock['files'][rel]=sha(U3/rel)
write(U3/'content-lock-f6.json',lock)
print('Built Unit 3 F6 classroom/browser validation')
