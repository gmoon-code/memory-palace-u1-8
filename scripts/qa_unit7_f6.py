from __future__ import annotations
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from scripts.site_release_guard import site_runtime_hash_allowed
from fastapi.testclient import TestClient
from backend.main import app
AP=ROOT/'content/ap-biology'; U7=AP/'unit-7'; DOC=ROOT/'docs/UNIT7_F6_CLASSROOM_BROWSER_QA.md'; client=TestClient(app)
def read(rel): return json.loads((U7/rel).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
problems=[]
ux=read('ux-validation-f6.json'); status=read('status.json'); lock=read('content-lock-f6.json'); f5=read('finalization-f5.json'); f5lock=read('content-lock-f5.json')
expected={'canonical_records':215,'guided_journeys':6,'scenes_validated':55,'recall_scenes_validated':18,'runtime_memory_objects':174,'challenge_lab_items':16,'scope_guards':25,'exact_name_review_targets':94,'non_exact_palace_records':80,'mixed_discrimination_sets':33,'mixed_discrimination_questions':102}
if ux.get('curriculum_content_changed') is not False: problems.append('F6 incorrectly reports curriculum changes')
for k,v in expected.items():
    if ux.get(k)!=v: problems.append(f'UX artifact {k}={ux.get(k)} expected {v}')
b=ux.get('browser_facing_validation',{})
for k in ['scene_geometry_findings','recall_content_leak_findings','broken_interpolation_findings','unit_switch_findings','refresh_resume_findings','review_scheduler_findings','mixed_review_findings','challenge_lab_findings','speech_preparation_findings']:
    if b.get(k)!=0: problems.append(f'Browser-facing finding {k}={b.get(k)}')
if b.get('scene_render_checks')!=55 or b.get('recall_render_checks')!=18: problems.append('Runtime render matrix incomplete')
if b.get('scene_viewport_contract_checks')!=165 or b.get('recall_viewport_contract_checks')!=54: problems.append('Responsive viewport contract matrix incomplete')
if b.get('route_lengths')!=[10,14,9,8,9,5]: problems.append('Route-length matrix drifted')
if b.get('result')!='PASS': problems.append('Browser-facing validation result is not PASS')
if b.get('pixel_screenshot_validation')!='NOT_EXECUTED_IN_THIS_CONTAINER': problems.append('Pixel-validation limitation is not recorded transparently')
if status.get('pipeline_stage')!='UNIT7_CLASSROOM_BROWSER_VALIDATED_F6' or status.get('browser_validation')!='PASS_F6': problems.append('Current Unit 7 status is not F6 validated')
if not status.get('student_release') or status.get('preview_release'): problems.append('F6 changed Unit 7 student-release flags incorrectly')
if not (f5.get('accounted_records')==215 and f5.get('unaccounted_records')==0 and f5.get('runtime_memory_objects')==174 and f5.get('challenge_lab_records')==16 and f5.get('scope_guard_records')==25): problems.append('F5 canonical accounting drifted')
if ux.get('f5_lock_sha256')!=sha(U7/'content-lock-f5.json'): problems.append('F5 content lock changed under F6')
for rel,digest in lock.get('files',{}).items():
    p=U7/rel
    if not p.exists() or sha(p)!=digest: problems.append(f'F6 lock mismatch: {rel}')
for rel,digest in f5lock.get('files',{}).items():
    p=U7/rel
    if not p.exists() or sha(p)!=digest: problems.append(f'F5 locked artifact changed during F6: {rel}')
for rel,digest in f5lock.get('protected_narratives',{}).items():
    p=U7/rel
    if not p.exists() or sha(p)!=digest: problems.append(f'Protected Unit 7 narrative changed during F6: {rel}')
for rel,digest in f5lock.get('protected_upstream_locks',{}).items():
    p=U7/rel
    if not p.exists() or sha(p)!=digest: problems.append(f'Protected upstream Unit 7 lock changed during F6: {rel}')

# F6 changes only release version and speech preparation among the F5 runtime files.
allowed={'backend/main.py','frontend/js/audio.js'}
f6_runtime=lock.get('runtime_file_sha256',{})
changed=[rel for rel,digest in f5lock.get('runtime_file_sha256',{}).items() if f6_runtime.get(rel)!=digest]
if set(changed)!=allowed: problems.append(f'F6 runtime-change set {changed} != expected {sorted(allowed)}')
u8lock6=AP/'unit-8'/'content-lock-f6.json'; u8lock5=AP/'unit-8'/'content-lock-f5.json'
u8lock=u8lock6 if u8lock6.exists() else u8lock5
u8_runtime=json.loads(u8lock.read_text(encoding='utf-8')).get('runtime_file_sha256',{}) if u8lock.exists() else {}
for rel,digest in f6_runtime.items():
    current=sha(ROOT/rel)
    if current!=digest and u8_runtime.get(rel)!=current and not site_runtime_hash_allowed(ROOT,rel,current): problems.append(f'F6 runtime hash mismatch without compatible Unit 8 lock: {rel}')

health=client.get('/api/health').json()
if health.get('version') not in {'v2-apbio-0.28.0-u7-f6','v2-apbio-0.29.0-u8-f5','v2-apbio-0.30.0-u8-f6'}: problems.append(f"Unexpected API version: {health.get('version')}")
u=client.get('/api/units/unit-7').json()
if u.get('browser_validation')!='PASS_F6' or u.get('status')!='STUDENT_READY' or u.get('pipeline_stage')!='UNIT7_CLASSROOM_BROWSER_VALIDATED_F6': problems.append('Live Unit 7 API does not expose F6 validation status')
if len(client.get('/api/units/unit-7/journeys').json()['guided_journeys'])!=6: problems.append('Live Unit 7 journey count is not 6')
if client.get('/api/units/unit-7/application-lab').json().get('challenge_count')!=16: problems.append('Challenge Lab API drift')
if client.get('/api/units/unit-7/review-manifest').json().get('target_count')!=94: problems.append('Review manifest API drift')
md=client.get('/api/units/unit-7/mixed-discrimination').json()
if md.get('set_count')!=33 or md.get('question_count')!=102: problems.append('Mixed-discrimination API drift')
if client.get('/api/units/unit-7/scope-guards').json().get('guard_count')!=25: problems.append('Scope-guard API drift')
if client.get('/api/units/unit-7/finalization').json().get('unaccounted_records')!=0: problems.append('Finalization zero-loss accounting API drift')
for i in range(1,7):
    if client.get(f'/api/units/unit-7/journeys/U7-J{i}').status_code!=200: problems.append(f'Journey U7-J{i} live API failed')

learn=(ROOT/'frontend/js/views/learn.js').read_text(encoding='utf-8'); statejs=(ROOT/'frontend/js/state.js').read_text(encoding='utf-8'); appjs=(ROOT/'frontend/js/app.js').read_text(encoding='utf-8'); audio=(ROOT/'frontend/js/audio.js').read_text(encoding='utf-8')
if '<details class="memory-panel" open>' in learn: problems.append('Memory anchors open by default')
if 'centerCurrentRoute' not in appjs: problems.append('Active route auto-centering missing')
if 'data-action="review-next"' not in appjs or 'Continue review' not in appjs: problems.append('Hinted exact Review lacks direct continuation')
if "if(unitId!=='unit-2')return" in statejs: problems.append('Legacy unit-specific mixed scheduler gate remains')
for token in ['p²','q²','2pq','N0','N1','N2','N3','N4','bya','mya']:
    if token not in audio: problems.append(f'Unit 7 speech normalization missing source token {token}')

course=json.loads((AP/'course.json').read_text(encoding='utf-8')); cu7=next(x for x in course['units'] if x['unit_id']=='unit-7')
if cu7.get('browser_validation')!='PASS_F6' or cu7.get('pipeline_stage')!='UNIT7_CLASSROOM_BROWSER_VALIDATED_F6': problems.append('Course registry Unit 7 F6 status mismatch')
main=json.loads((AP/'mainline-release-u1-u7.json').read_text(encoding='utf-8'))
if main.get('schema')!='memory-palace-v2-mainline-u1-u7-f6-1.0' or main.get('release_status')!='STUDENT_READY_UNITS_1_7_UNIT7_F6_VALIDATED': problems.append('Units 1-7 mainline manifest is not F6')
if main.get('runtime_version')!='v2-apbio-0.28.0-u7-f6': problems.append('Units 1-7 mainline runtime version mismatch')
if main.get('totals')!={'canonical_records_units_1_7':1306,'guided_journeys':50,'permanent_scenes':390,'challenge_lab_items':99}: problems.append('Units 1-7 mainline totals drifted')

lines=['# Unit 7 F6 Classroom and Browser-Facing QA','',
'## Scope','',
'F6 changes no Unit 7 canonical science, F2 learning architecture, F3 scene briefs, F4A–F4F narrative bytes, F5 Memory Objects, Challenge Lab science, Review targets, mixed-discrimination content, or scope guards. It validates the released learner experience across Home, Learn, Quick Recall, Review, mixed discrimination, Challenge Lab, unit switching, persistence, responsive UI contracts, and browser speech text.','',
'## Runtime render and responsive contract matrix','',
'- Permanent scenes rendered through the production view function: **55 / 55**',
'- Quick Recall states rendered through the production view function: **18 / 18**',
'- Target responsive contracts: **1440×1000 desktop, 820×1180 tablet, 390×844 phone**',
'- Scene/viewport contract checks: **165**',
'- Recall/viewport contract checks: **54**',
'- Three-zone scene geometry findings: **0**',
'- Quick Recall story/location/route/cast/anchor leaks: **0**',
'- Broken interpolation findings: **0**','',
'### Rendering limitation','',
'Chromium was directly probed with an 8-second headless `about:blank` render and timed out without DOM output in this sandbox. F6 therefore does **not** claim screenshot-level or pixel-level browser validation. The release uses production HTML rendering functions, state-machine interaction tests, responsive CSS contract checks, and live FastAPI/browser-facing HTTP smoke tests.','',
'## F6 runtime correction','',
'Browser speech text now normalizes Unit 7 population-genetics and phylogeny notation including p², q², 2pq, N0–N4, and bya/mya age abbreviations. This changes speech preparation only; visible scientific text and all six narratives remain unchanged.','',
'## Learning-system validation','',
'- Exact-name delayed-review targets: **94**',
'- Meaning/mechanism-only palace records: **80**',
'- Mixed-discrimination sets: **33**',
'- Mixed-discrimination questions: **102**',
'- Mixed review waits at least **48 hours** after eligibility.',
'- Visible Review remains capped at **5** due items.',
'- Unit-scoped Review isolation: **PASS**',
'- Refresh/resume state: **PASS**',
'- Unit 7 Challenge Lab: **16 / 16** tasks',
'- Released-unit switching among Units 1–7: **PASS**','',
'## Release decision','',
('**PASS — Unit 7 remains student-ready and has completed F6 functional browser-facing/classroom validation.**' if not problems else '**FAIL — blocking findings remain.**')]
if problems: lines+=['','### Blocking findings','']+[f'- {p}' for p in problems]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
if problems:
    print('UNIT7 F6 QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT7 F6 QA PASS')
print(json.dumps({'scenes':55,'recalls':18,'responsive_contract_viewports':3,'scene_viewport_checks':165,'recall_viewport_checks':54,'exact_name_targets':94,'mixed_sets':33,'mixed_questions':102,'challenge_lab_items':16,'route_lengths':[10,14,9,8,9,5],'refresh_resume':True,'released_unit_switching':'Units 1-7','pixel_screenshot_validation':False},indent=2))
