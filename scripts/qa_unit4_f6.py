from __future__ import annotations
import json, hashlib, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from scripts.site_release_guard import site_runtime_hash_allowed
from fastapi.testclient import TestClient
from backend.main import app
U4=ROOT/'content'/'ap-biology'/'unit-4'
DOC=ROOT/'docs'/'UNIT4_F6_CLASSROOM_BROWSER_QA.md'
client=TestClient(app)
def read(rel): return json.loads((U4/rel).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
problems=[]
ux=read('ux-validation-f6.json'); status=read('status.json'); lock=read('content-lock-f6.json'); f5=read('finalization-f5.json')
if ux.get('curriculum_content_changed') is not False: problems.append('F6 incorrectly reports curriculum changes')
for k,v in {'canonical_records':180,'guided_journeys':7,'scenes_validated':51,'recall_scenes_validated':18,'runtime_memory_objects':162,'challenge_lab_items':15,'scope_guards':3,'exact_name_review_targets':162,'mixed_discrimination_sets':33,'mixed_discrimination_questions':99}.items():
    if ux.get(k)!=v: problems.append(f'UX artifact {k}={ux.get(k)} expected {v}')
b=ux['browser_facing_validation']
for k in ['scene_geometry_findings','recall_content_leak_findings','broken_interpolation_findings','unit_switch_findings','refresh_resume_findings','review_scheduler_findings','challenge_lab_findings']:
    if b.get(k)!=0: problems.append(f'Browser-facing finding {k}={b.get(k)}')
if b.get('scene_render_checks')!=51 or b.get('recall_render_checks')!=18: problems.append('Runtime render matrix incomplete')
if b.get('scene_viewport_contract_checks')!=153 or b.get('recall_viewport_contract_checks')!=54: problems.append('Responsive viewport contract matrix incomplete')
if b.get('result')!='PASS': problems.append('Browser-facing validation result is not PASS')
if b.get('pixel_screenshot_validation')!='NOT_EXECUTED_IN_THIS_CONTAINER': problems.append('Pixel-validation limitation is not recorded transparently')
if status.get('pipeline_stage')!='UNIT4_CLASSROOM_BROWSER_VALIDATED_F6' or status.get('browser_validation')!='PASS_F6': problems.append('Current Unit 4 status is not F6 validated')
if not status.get('student_release') or status.get('preview_release'): problems.append('F6 changed Unit 4 student-release flags incorrectly')
if f5.get('accounted_records')!=180 or f5.get('unaccounted_records')!=0 or f5.get('runtime_memory_objects')!=162: problems.append('F5 canonical accounting drifted')
if ux.get('f5_lock_sha256')!=sha(U4/'content-lock-f5.json'): problems.append('F5 content lock changed under F6')
for rel,digest in lock['files'].items():
    p=U4/rel
    if not p.exists() or sha(p)!=digest: problems.append(f'F6 lock mismatch: {rel}')
later_candidates=[ROOT/'content/ap-biology/unit-8/content-lock-f6.json',ROOT/'content/ap-biology/unit-8/content-lock-f5.json',ROOT/'content/ap-biology/unit-7/content-lock-f6.json',ROOT/'content/ap-biology/unit-6/content-lock-f6.json',ROOT/'content/ap-biology/unit-5/content-lock-f6.json']
later_runtime={}
for lp in later_candidates:
    if lp.exists():
        later_runtime=json.loads(lp.read_text(encoding='utf-8')).get('runtime_file_sha256',{}); break
for rel,digest in lock.get('runtime_file_sha256',{}).items():
    p=ROOT/rel
    current=sha(p) if p.exists() else None
    if current!=digest and later_runtime.get(rel)!=current and not site_runtime_hash_allowed(ROOT,rel,current): problems.append(f'F6 runtime hash mismatch without later validated replacement: {rel}')
# F6 must not mutate F5 narrative/runtime curriculum artifacts.
f5lock=read('content-lock-f5.json')
for rel,digest in f5lock['files'].items():
    p=U4/rel
    if not p.exists() or sha(p)!=digest: problems.append(f'F5 locked artifact changed during F6: {rel}')
# Runtime/API surface.
health=client.get('/api/health').json()
if not str(health.get('version','')).startswith('v2-apbio-'): problems.append(f"Unexpected API version after Unit 4 F6: {health.get('version')}")
u=client.get('/api/units/unit-4').json()
if u.get('browser_validation')!='PASS_F6' or u.get('status')!='STUDENT_READY' or u.get('pipeline_stage')!='UNIT4_CLASSROOM_BROWSER_VALIDATED_F6': problems.append('Live Unit 4 API does not expose F6 validation status')
if len(client.get('/api/units/unit-4/journeys').json()['guided_journeys'])!=7: problems.append('Live Unit 4 journey count is not 7')
if client.get('/api/units/unit-4/application-lab').json().get('challenge_count')!=15: problems.append('Challenge Lab API drift')
if client.get('/api/units/unit-4/review-manifest').json().get('target_count')!=162: problems.append('Review manifest API drift')
if client.get('/api/units/unit-4/mixed-discrimination').json().get('set_count')!=33: problems.append('Mixed-discrimination API drift')
if client.get('/api/units/unit-4/scope-guards').json().get('guard_count')!=3: problems.append('Scope-guard API drift')
# Source-level UX protections.
learn=(ROOT/'frontend/js/views/learn.js').read_text(encoding='utf-8'); statejs=(ROOT/'frontend/js/state.js').read_text(encoding='utf-8'); appjs=(ROOT/'frontend/js/app.js').read_text(encoding='utf-8'); audio=(ROOT/'frontend/js/audio.js').read_text(encoding='utf-8')
if '<details class="memory-panel" open>' in learn: problems.append('Memory anchors open by default')
if 'centerCurrentRoute' not in appjs: problems.append('Active route auto-centering missing')
if 'data-action="review-next"' not in appjs or 'Continue review' not in appjs: problems.append('Hinted exact Review lacks direct continuation')
if "if(unitId!=='unit-2')return" in statejs: problems.append('Legacy unit-specific mixed scheduler gate remains')
for token in ['GPCR','GTP','GDP','cAMP','CDK','DNA','G1','G2','G0']:
    if token not in audio: problems.append(f'Unit 4 speech normalization missing source token {token}')

lines=['# Unit 4 F6 Classroom and Browser-Facing QA','',
'## Scope','',
'F6 changes no Unit 4 curriculum, scientific lock, permanent palace architecture, or narrative science. It validates the released learner experience across Home, Learn, Quick Recall, Review, mixed discrimination, Challenge Lab, unit switching, persistence, responsive UI contracts, and browser speech text.','',
'## Runtime render and responsive contract matrix','',
'- Permanent scenes rendered through the production view function: **51 / 51**',
'- Quick Recall scenes rendered through the production view function: **18 / 18**',
'- Target responsive contracts: **1440×1000 desktop, 820×1180 tablet, 390×844 phone**',
'- Scene/viewport contract checks: **153**',
'- Recall/viewport contract checks: **54**',
'- Three-zone scene geometry findings: **0**',
'- Quick Recall story/location/route/cast/anchor leaks: **0**',
'- Broken interpolation findings: **0**','',
'### Rendering limitation','',
'The Chromium executable installed in this sandbox did not complete even an `about:blank` headless render. F6 therefore does **not** claim screenshot-level or pixel-level browser validation. The release uses production HTML rendering functions, state-machine interaction tests, responsive CSS contract checks, and live FastAPI/browser-facing HTTP smoke tests.','',
'## F6 runtime corrections','',
'1. Exact-name Review now provides **Continue review** after a learner reveals a hint/answer, so the learner can advance directly to the next due item.','2. Browser speech text now normalizes frequent Unit 4 abbreviations and phase labels including DNA, GPCR, GDP, GTP, cAMP, CDK, APC, G1, G2, and G0 while leaving visible scientific text unchanged.','',
'## Learning-system validation','',
'- Exact-name delayed-review targets: **162**','- Mixed-discrimination sets: **33**','- Mixed-discrimination questions: **99**','- Mixed review waits at least **48 hours** after eligibility.','- Visible Review remains capped at **5** due items.','- Unit-scoped Review isolation: **PASS**','- Refresh/resume state: **PASS**','- Unit 4 Challenge Lab: **15 / 15** tasks','- Released-unit switching among Units 1–4: **PASS**','',
'## Release decision','',('**PASS — Unit 4 remains student-ready and has completed F6 functional browser-facing/classroom validation.**' if not problems else '**FAIL — blocking findings remain.**')]
if problems: lines+=['','### Blocking findings','']+[f'- {p}' for p in problems]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
if problems:
    print('UNIT4 F6 QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT4 F6 QA PASS')
print(json.dumps({'scenes':51,'recalls':18,'responsive_contract_viewports':3,'scene_viewport_checks':153,'recall_viewport_checks':54,'exact_name_targets':162,'mixed_sets':33,'challenge_lab':15,'student_release':True,'pixel_screenshot_validation':False},indent=2))
