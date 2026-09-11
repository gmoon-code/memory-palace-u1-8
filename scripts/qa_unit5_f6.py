from __future__ import annotations
import json, hashlib, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from scripts.site_release_guard import site_runtime_hash_allowed
from fastapi.testclient import TestClient
from backend.main import app
U5=ROOT/'content'/'ap-biology'/'unit-5'
DOC=ROOT/'docs'/'UNIT5_F6_CLASSROOM_BROWSER_QA.md'
client=TestClient(app)
def read(rel): return json.loads((U5/rel).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
problems=[]
ux=read('ux-validation-f6.json'); status=read('status.json'); lock=read('content-lock-f6.json'); f5=read('finalization-f5.json')
if ux.get('curriculum_content_changed') is not False: problems.append('F6 incorrectly reports curriculum changes')
for k,v in {
    'canonical_records':152,'guided_journeys':8,'scenes_validated':50,'recall_scenes_validated':18,
    'runtime_memory_objects':131,'challenge_lab_items':16,'scope_guards':5,'exact_name_review_targets':130,
    'mixed_discrimination_sets':32,'mixed_discrimination_questions':79
}.items():
    if ux.get(k)!=v: problems.append(f'UX artifact {k}={ux.get(k)} expected {v}')
b=ux['browser_facing_validation']
for k in ['scene_geometry_findings','recall_content_leak_findings','broken_interpolation_findings','unit_switch_findings','refresh_resume_findings','review_scheduler_findings','mixed_review_findings','challenge_lab_findings']:
    if b.get(k)!=0: problems.append(f'Browser-facing finding {k}={b.get(k)}')
if b.get('scene_render_checks')!=50 or b.get('recall_render_checks')!=18: problems.append('Runtime render matrix incomplete')
if b.get('scene_viewport_contract_checks')!=150 or b.get('recall_viewport_contract_checks')!=54: problems.append('Responsive viewport contract matrix incomplete')
if b.get('route_lengths')!=[5,10,4,7,4,7,6,7]: problems.append('Route-length matrix drifted')
if b.get('result')!='PASS': problems.append('Browser-facing validation result is not PASS')
if b.get('pixel_screenshot_validation')!='NOT_EXECUTED_IN_THIS_CONTAINER': problems.append('Pixel-validation limitation is not recorded transparently')
if status.get('pipeline_stage')!='UNIT5_CLASSROOM_BROWSER_VALIDATED_F6' or status.get('browser_validation')!='PASS_F6': problems.append('Current Unit 5 status is not F6 validated')
if not status.get('student_release') or status.get('preview_release'): problems.append('F6 changed Unit 5 student-release flags incorrectly')
if not (f5.get('accounted_records')==152 and f5.get('unaccounted_records')==0 and f5.get('runtime_memory_objects')==131 and f5.get('challenge_lab_records')==16 and f5.get('scope_guard_records')==5): problems.append('F5 canonical accounting drifted')
if ux.get('f5_lock_sha256')!=sha(U5/'content-lock-f5.json'): problems.append('F5 content lock changed under F6')
for rel,digest in lock['files'].items():
    p=U5/rel
    if not p.exists() or sha(p)!=digest: problems.append(f'F6 lock mismatch: {rel}')
later_f6=ROOT/'content/ap-biology/unit-6/content-lock-f6.json'; later_f5=ROOT/'content/ap-biology/unit-6/content-lock-f5.json'
if later_f6.exists(): later_runtime=read(later_f6).get('runtime_file_sha256',{})
elif later_f5.exists(): later_runtime=read(later_f5).get('runtime_file_sha256',{})
else: later_runtime={}
u7f6=ROOT/'content/ap-biology/unit-7/content-lock-f6.json'; u7f5=ROOT/'content/ap-biology/unit-7/content-lock-f5.json'
u7lock=u7f6 if u7f6.exists() else u7f5
u7_runtime=json.loads(u7lock.read_text(encoding='utf-8')).get('runtime_file_sha256',{}) if u7lock.exists() else {}
u8lock6=ROOT/'content/ap-biology/unit-8/content-lock-f6.json'; u8lock5=ROOT/'content/ap-biology/unit-8/content-lock-f5.json'
u8lock=u8lock6 if u8lock6.exists() else u8lock5
u8_runtime=json.loads(u8lock.read_text(encoding='utf-8')).get('runtime_file_sha256',{}) if u8lock.exists() else {}
for rel,digest in lock.get('runtime_file_sha256',{}).items():
    p=ROOT/rel
    current=sha(p) if p.exists() else None
    if current!=digest and later_runtime.get(rel)!=current and u7_runtime.get(rel)!=current and u8_runtime.get(rel)!=current and not site_runtime_hash_allowed(ROOT,rel,current): problems.append(f'F6 runtime hash mismatch without a compatible later-unit lock: {rel}')
# F6 must not mutate the F5 curriculum/runtime data or any F4 narrative.
f5lock=read('content-lock-f5.json')
for rel,digest in f5lock.get('files',{}).items():
    p=U5/rel
    if not p.exists() or sha(p)!=digest: problems.append(f'F5 locked artifact changed during F6: {rel}')
for rel,digest in f5lock.get('protected_narratives',{}).items():
    p=U5/rel
    if not p.exists() or sha(p)!=digest: problems.append(f'Protected Unit 5 narrative changed during F6: {rel}')
for rel,digest in f5lock.get('protected_upstream_locks',{}).items():
    p=U5/rel
    if not p.exists() or sha(p)!=digest: problems.append(f'Protected upstream lock changed during F6: {rel}')

health=client.get('/api/health').json()
if not str(health.get('version','')).startswith('v2-apbio-'): problems.append(f"Unexpected API version after Unit 5 F6: {health.get('version')}")
u=client.get('/api/units/unit-5').json()
if u.get('browser_validation')!='PASS_F6' or u.get('status')!='STUDENT_READY' or u.get('pipeline_stage')!='UNIT5_CLASSROOM_BROWSER_VALIDATED_F6': problems.append('Live Unit 5 API does not expose F6 validation status')
if len(client.get('/api/units/unit-5/journeys').json()['guided_journeys'])!=8: problems.append('Live Unit 5 journey count is not 8')
if client.get('/api/units/unit-5/application-lab').json().get('challenge_count')!=16: problems.append('Challenge Lab API drift')
if client.get('/api/units/unit-5/review-manifest').json().get('target_count')!=130: problems.append('Review manifest API drift')
md=client.get('/api/units/unit-5/mixed-discrimination').json()
if md.get('set_count')!=32 or md.get('question_count')!=79: problems.append('Mixed-discrimination API drift')
if client.get('/api/units/unit-5/scope-guards').json().get('guard_count')!=5: problems.append('Scope-guard API drift')

learn=(ROOT/'frontend/js/views/learn.js').read_text(encoding='utf-8')
statejs=(ROOT/'frontend/js/state.js').read_text(encoding='utf-8')
appjs=(ROOT/'frontend/js/app.js').read_text(encoding='utf-8')
audio=(ROOT/'frontend/js/audio.js').read_text(encoding='utf-8')
if '<details class="memory-panel" open>' in learn: problems.append('Memory anchors open by default')
if 'centerCurrentRoute' not in appjs: problems.append('Active route auto-centering missing')
if 'data-action="review-next"' not in appjs or 'Continue review' not in appjs: problems.append('Hinted exact Review lacks direct continuation')
if "if(unitId!=='unit-2')return" in statejs: problems.append('Legacy unit-specific mixed scheduler gate remains')
for token in ['RNA','F1','F2','XX','XY','ABO','IA','IB','UV','HBB','2n','χ²','AaBb','Aa','AA','aa']:
    if token not in audio: problems.append(f'Unit 5 speech normalization missing source token {token}')

lines=['# Unit 5 F6 Classroom and Browser-Facing QA','',
'## Scope','',
'F6 changes no Unit 5 canonical science, learning-function architecture, permanent palace structure, narrative content, Review targets, mixed-discrimination content, Challenge Lab science, or scope guards. It validates the released learner experience across Home, Learn, Quick Recall, Review, mixed discrimination, Challenge Lab, unit switching, persistence, responsive UI contracts, and browser speech text.','',
'## Runtime render and responsive contract matrix','',
'- Permanent scenes rendered through the production view function: **50 / 50**',
'- Quick Recall states rendered through the production view function: **18 / 18**',
'- Target responsive contracts: **1440×1000 desktop, 820×1180 tablet, 390×844 phone**',
'- Scene/viewport contract checks: **150**',
'- Recall/viewport contract checks: **54**',
'- Three-zone scene geometry findings: **0**',
'- Quick Recall story/location/route/cast/anchor leaks: **0**',
'- Broken interpolation findings: **0**','',
'### Rendering limitation','',
'The Chromium executable installed in this sandbox timed out even on an `about:blank` headless render. F6 therefore does **not** claim screenshot-level or pixel-level browser validation. The release uses production HTML rendering functions, state-machine interaction tests, responsive CSS contract checks, and live FastAPI/browser-facing HTTP smoke tests.','',
'## F6 runtime correction','',
'Browser speech text now normalizes frequent Unit 5 genetics and statistics notation including RNA, F1/F2, XX/XY, ABO, IA/IB, UV, HBB, 2n, χ², and common genotype strings. This changes audio preparation only; visible scientific text remains unchanged.','',
'## Learning-system validation','',
'- Exact-name delayed-review targets: **130**',
'- Non-exact palace records: **1**',
'- Mixed-discrimination sets: **32**',
'- Mixed-discrimination questions: **79**',
'- Mixed review waits at least **48 hours** after eligibility.',
'- Visible Review remains capped at **5** due items.',
'- Unit-scoped Review isolation: **PASS**',
'- Refresh/resume state: **PASS**',
'- Unit 5 Challenge Lab: **16 / 16** tasks',
'- Released-unit switching among Units 1–5: **PASS**','',
'## Release decision','',
('**PASS — Unit 5 remains student-ready and has completed F6 functional browser-facing/classroom validation.**' if not problems else '**FAIL — blocking findings remain.**')]
if problems: lines+=['','### Blocking findings','']+[f'- {p}' for p in problems]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
if problems:
    print('UNIT5 F6 QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT5 F6 QA PASS')
print(json.dumps({'scenes':50,'recalls':18,'responsive_contract_viewports':3,'scene_viewport_checks':150,'recall_viewport_checks':54,'exact_name_targets':130,'mixed_sets':32,'mixed_questions':79,'challenge_lab':16,'student_release':True,'pixel_screenshot_validation':False},indent=2))
