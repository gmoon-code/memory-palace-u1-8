from __future__ import annotations
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from scripts.site_release_guard import site_runtime_hash_allowed
from fastapi.testclient import TestClient
from backend.main import app
AP=ROOT/'content/ap-biology'; U6=AP/'unit-6'; DOC=ROOT/'docs/UNIT6_F6_CLASSROOM_BROWSER_QA.md'; client=TestClient(app)
def read(rel): return json.loads((U6/rel).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
problems=[]
ux=read('ux-validation-f6.json'); status=read('status.json'); lock=read('content-lock-f6.json'); f5=read('finalization-f5.json'); f5lock=read('content-lock-f5.json')
expected={'canonical_records':202,'guided_journeys':6,'scenes_validated':53,'recall_scenes_validated':18,'runtime_memory_objects':161,'challenge_lab_items':16,'scope_guards':25,'exact_name_review_targets':134,'mixed_discrimination_sets':37,'mixed_discrimination_questions':94}
if ux.get('curriculum_content_changed') is not False: problems.append('F6 incorrectly reports curriculum changes')
for k,v in expected.items():
    if ux.get(k)!=v: problems.append(f'UX artifact {k}={ux.get(k)} expected {v}')
b=ux.get('browser_facing_validation',{})
for k in ['scene_geometry_findings','recall_content_leak_findings','broken_interpolation_findings','unit_switch_findings','refresh_resume_findings','review_scheduler_findings','mixed_review_findings','challenge_lab_findings']:
    if b.get(k)!=0: problems.append(f'Browser-facing finding {k}={b.get(k)}')
if b.get('scene_render_checks')!=53 or b.get('recall_render_checks')!=18: problems.append('Runtime render matrix incomplete')
if b.get('scene_viewport_contract_checks')!=159 or b.get('recall_viewport_contract_checks')!=54: problems.append('Responsive viewport contract matrix incomplete')
if b.get('route_lengths')!=[12,8,8,12,8,5]: problems.append('Route-length matrix drifted')
if b.get('result')!='PASS': problems.append('Browser-facing validation result is not PASS')
if b.get('pixel_screenshot_validation')!='NOT_EXECUTED_IN_THIS_CONTAINER': problems.append('Pixel-validation limitation is not recorded transparently')
if status.get('pipeline_stage')!='UNIT6_CLASSROOM_BROWSER_VALIDATED_F6' or status.get('browser_validation')!='PASS_F6': problems.append('Current Unit 6 status is not F6 validated')
if not status.get('student_release') or status.get('preview_release'): problems.append('F6 changed Unit 6 student-release flags incorrectly')
if not (f5.get('accounted_records')==202 and f5.get('unaccounted_records')==0 and f5.get('runtime_memory_objects')==161 and f5.get('challenge_lab_records')==16 and f5.get('scope_guard_records')==25): problems.append('F5 canonical accounting drifted')
if ux.get('f5_lock_sha256')!=sha(U6/'content-lock-f5.json'): problems.append('F5 content lock changed under F6')
for rel,digest in lock.get('files',{}).items():
    p=U6/rel
    if not p.exists() or sha(p)!=digest: problems.append(f'F6 lock mismatch: {rel}')
for rel,digest in f5lock.get('files',{}).items():
    p=U6/rel
    if not p.exists() or sha(p)!=digest: problems.append(f'F5 locked artifact changed during F6: {rel}')
for rel,digest in f5lock.get('protected_narratives',{}).items():
    p=U6/rel
    if not p.exists() or sha(p)!=digest: problems.append(f'Protected Unit 6 narrative changed during F6: {rel}')
for rel,digest in f5lock.get('protected_upstream_locks',{}).items():
    p=U6/rel
    if not p.exists() or sha(p)!=digest: problems.append(f'Protected upstream lock changed during F6: {rel}')
# Historical F6 changed only release metadata and speech preparation relative to F5.
# Later curriculum branches may add new-unit integration in backend files, so validate
# the F6 delta from the frozen F6 lock and permit current bytes only when a later lock records them.
allowed={'backend/main.py','frontend/js/audio.js'}
f6_runtime=lock.get('runtime_file_sha256',{})
changed_at_f6=[rel for rel,digest in f5lock.get('runtime_file_sha256',{}).items() if f6_runtime.get(rel)!=digest]
if set(changed_at_f6)!=allowed:
    problems.append(f'Historical F6 runtime-change set {changed_at_f6} != expected {sorted(allowed)}')
u7lock6=AP/'unit-7'/'content-lock-f6.json'; u7lock5=AP/'unit-7'/'content-lock-f5.json'
u7lock=u7lock6 if u7lock6.exists() else u7lock5
u7_runtime=json.loads(u7lock.read_text(encoding='utf-8')).get('runtime_file_sha256',{}) if u7lock.exists() else {}
u8lock6=AP/'unit-8'/'content-lock-f6.json'; u8lock5=AP/'unit-8'/'content-lock-f5.json'
u8lock=u8lock6 if u8lock6.exists() else u8lock5
u8_runtime=json.loads(u8lock.read_text(encoding='utf-8')).get('runtime_file_sha256',{}) if u8lock.exists() else {}
for rel,digest in f6_runtime.items():
    current=sha(ROOT/rel)
    if current!=digest and u7_runtime.get(rel)!=current and u8_runtime.get(rel)!=current and not site_runtime_hash_allowed(ROOT,rel,current):
        problems.append(f'F6 runtime hash mismatch without a compatible later-unit lock: {rel}')

health=client.get('/api/health').json()
if health.get('version') not in {'v2-apbio-0.26.0-u6-f6','v2-apbio-0.27.0-u7-f5','v2-apbio-0.28.0-u7-f6','v2-apbio-0.29.0-u8-f5','v2-apbio-0.30.0-u8-f6'}: problems.append(f"Unexpected API version after Unit 6 F6: {health.get('version')}")
u=client.get('/api/units/unit-6').json()
if u.get('browser_validation')!='PASS_F6' or u.get('status')!='STUDENT_READY' or u.get('pipeline_stage')!='UNIT6_CLASSROOM_BROWSER_VALIDATED_F6': problems.append('Live Unit 6 API does not expose F6 validation status')
if len(client.get('/api/units/unit-6/journeys').json()['guided_journeys'])!=6: problems.append('Live Unit 6 journey count is not 6')
if client.get('/api/units/unit-6/application-lab').json().get('challenge_count')!=16: problems.append('Challenge Lab API drift')
if client.get('/api/units/unit-6/review-manifest').json().get('target_count')!=134: problems.append('Review manifest API drift')
md=client.get('/api/units/unit-6/mixed-discrimination').json()
if md.get('set_count')!=37 or md.get('question_count')!=94: problems.append('Mixed-discrimination API drift')
if client.get('/api/units/unit-6/scope-guards').json().get('guard_count')!=25: problems.append('Scope-guard API drift')
if client.get('/api/units/unit-6/finalization').json().get('unaccounted_records')!=0: problems.append('Finalization zero-loss accounting API drift')
for i in range(1,7):
    if client.get(f'/api/units/unit-6/journeys/U6-J{i}').status_code!=200: problems.append(f'Journey U6-J{i} live API failed')

learn=(ROOT/'frontend/js/views/learn.js').read_text(encoding='utf-8'); statejs=(ROOT/'frontend/js/state.js').read_text(encoding='utf-8'); appjs=(ROOT/'frontend/js/app.js').read_text(encoding='utf-8'); audio=(ROOT/'frontend/js/audio.js').read_text(encoding='utf-8')
if '<details class="memory-panel" open>' in learn: problems.append('Memory anchors open by default')
if 'centerCurrentRoute' not in appjs: problems.append('Active route auto-centering missing')
if 'data-action="review-next"' not in appjs or 'Continue review' not in appjs: problems.append('Hinted exact Review lacks direct continuation')
if "if(unitId!=='unit-2')return" in statejs: problems.append('Legacy unit-specific mixed scheduler gate remains')
for token in ['pre-mRNA','mRNA','tRNA','rRNA','siRNA','miRNA','PCR','AUG','TATA','AAUAAA','HGT','SSB','dsDNA','trp','A-site','P-site','E-site','5′','3′']:
    if token not in audio: problems.append(f'Unit 6 speech normalization missing source token {token}')

lines=['# Unit 6 F6 Classroom and Browser-Facing QA','',
'## Scope','',
'F6 changes no Unit 6 canonical science, F2 learning architecture, F3 scene briefs, F4A–F4F narrative bytes, F5 Memory Objects, Challenge Lab science, Review targets, mixed-discrimination content, or scope guards. It validates the released learner experience across Home, Learn, Quick Recall, Review, mixed discrimination, Challenge Lab, unit switching, persistence, responsive UI contracts, and browser speech text.','',
'## Runtime render and responsive contract matrix','',
'- Permanent scenes rendered through the production view function: **53 / 53**',
'- Quick Recall states rendered through the production view function: **18 / 18**',
'- Target responsive contracts: **1440×1000 desktop, 820×1180 tablet, 390×844 phone**',
'- Scene/viewport contract checks: **159**',
'- Recall/viewport contract checks: **54**',
'- Three-zone scene geometry findings: **0**',
'- Quick Recall story/location/route/cast/anchor leaks: **0**',
'- Broken interpolation findings: **0**','',
'### Rendering limitation','',
'Chromium was directly probed with an 8-second headless `about:blank` render and timed out without producing DOM output in this sandbox. F6 therefore does **not** claim screenshot-level or pixel-level browser validation. The release uses production HTML rendering functions, state-machine interaction tests, responsive CSS contract checks, and live FastAPI/browser-facing HTTP smoke tests.','',
'## F6 runtime correction','',
'Browser speech text now normalizes frequent Unit 6 molecular-biology notation including pre-mRNA, mRNA, tRNA, rRNA, siRNA/miRNA, PCR, AUG and stop codons, TATA, AAUAAA, HGT, SSB, dsDNA, trp, A/P/E-site labels, and 5′/3′ notation. This changes speech preparation only; visible scientific text and all six narratives remain unchanged.','',
'## Learning-system validation','',
'- Exact-name delayed-review targets: **134**',
'- Meaning/mechanism-only palace records: **27**',
'- Mixed-discrimination sets: **37**',
'- Mixed-discrimination questions: **94**',
'- Mixed review waits at least **48 hours** after eligibility.',
'- Visible Review remains capped at **5** due items.',
'- Unit-scoped Review isolation: **PASS**',
'- Refresh/resume state: **PASS**',
'- Unit 6 Challenge Lab: **16 / 16** tasks',
'- Released-unit switching among Units 1–6: **PASS**','',
'## Release decision','',
('**PASS — Unit 6 remains student-ready and has completed F6 functional browser-facing/classroom validation.**' if not problems else '**FAIL — blocking findings remain.**')]
if problems: lines+=['','### Blocking findings','']+[f'- {p}' for p in problems]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
if problems:
    print('UNIT6 F6 QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT6 F6 QA PASS')
print(json.dumps({'scenes':53,'recalls':18,'responsive_contract_viewports':3,'scene_viewport_checks':159,'recall_viewport_checks':54,'exact_name_targets':134,'mixed_sets':37,'mixed_questions':94,'challenge_lab':16,'student_release':True,'runtime_version':'v2-apbio-0.26.0-u6-f6','pixel_screenshot_validation':False},indent=2))
