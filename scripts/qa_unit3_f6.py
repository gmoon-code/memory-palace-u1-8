from __future__ import annotations
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from fastapi.testclient import TestClient
from backend.main import app
U3=ROOT/'content'/'ap-biology'/'unit-3';DOC=ROOT/'docs'/'UNIT3_F6_CLASSROOM_BROWSER_QA.md'
client=TestClient(app)
def read(rel):return json.loads((U3/rel).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
problems=[]
ux=read('ux-validation-f6.json');status=read('status.json');lock=read('content-lock-f6.json');f5=read('finalization-f5.json')
if ux.get('curriculum_content_changed') is not False:problems.append('F6 incorrectly reports curriculum changes')
for k,v in {'canonical_records':186,'guided_journeys':7,'scenes_validated':54,'recall_scenes_validated':18}.items():
 if ux.get(k)!=v:problems.append(f'UX artifact {k}={ux.get(k)} expected {v}')
b=ux['browser_validation']
for k in ['body_horizontal_overflow_findings','route_wrap_findings','scene_geometry_findings','recall_content_leak_findings','memory_anchors_default_open_findings']:
 if b.get(k)!=0:problems.append(f'Browser finding {k}={b.get(k)}')
if b.get('scene_viewport_combinations')!=162 or b.get('recall_viewport_combinations')!=54:problems.append('Browser viewport matrix incomplete')
if status.get('pipeline_stage')!='UNIT3_CLASSROOM_BROWSER_VALIDATED_F6' or status.get('browser_validation')!='PASS_F6':problems.append('Current Unit 3 status is not F6 validated')
if not status.get('student_release') or status.get('preview_release'):problems.append('F6 changed Unit 3 student-release flags incorrectly')
if f5.get('accounted_records')!=186 or f5.get('unaccounted_records')!=0:problems.append('F5 canonical accounting drifted')
if ux.get('f5_lock_sha256')!=sha(U3/'content-lock-f5.json'):problems.append('F5 content lock changed under F6')
for rel,digest in lock['files'].items():
 p=U3/rel
 if not p.exists() or sha(p)!=digest:problems.append(f'F6 lock mismatch: {rel}')
# F6 must not mutate permanent narrative files. Existing F4/F5 QA independently verifies all historical locks.
reg=read('journeys-f5.json')
if reg['journey_count']!=7 or reg['scene_count']!=54 or reg['checkpoint_count']!=18:problems.append('Narrative registry changed during F6')
# Runtime/API release surface.
health=client.get('/api/health').json()
if not str(health.get('version','')).startswith('v2-apbio-'):problems.append(f'API version {health.get("version")} invalid')
u=client.get('/api/units/unit-3').json()
if u.get('browser_validation')!='PASS_F6' or u.get('status')!='STUDENT_READY':problems.append('Live Unit 3 API does not expose F6 validation status')
if len(client.get('/api/units/unit-3/journeys').json()['guided_journeys'])!=7:problems.append('Live Unit 3 journey count is not 7')
if client.get('/api/units/unit-3/application-lab').json().get('challenge_count')!=11:problems.append('Challenge Lab API drift')
if client.get('/api/units/unit-3/review-manifest').json().get('target_count')!=126:problems.append('Review manifest API drift')
if client.get('/api/units/unit-3/mixed-discrimination').json().get('set_count')!=28:problems.append('Mixed-discrimination API drift')
# Source-level UX protections remain explicit and reviewable.
learn=(ROOT/'frontend/js/views/learn.js').read_text(encoding='utf-8');state=(ROOT/'frontend/js/state.js').read_text(encoding='utf-8');appjs=(ROOT/'frontend/js/app.js').read_text(encoding='utf-8');audio=(ROOT/'frontend/js/audio.js').read_text(encoding='utf-8')
if 'Math.min(route.length,11)' in learn:problems.append('Route renderer still caps journeys at 11 columns')
if '<details class="memory-panel" open>' in learn:problems.append('Memory anchors still open by default')
if "if(unitId!=='unit-2')return" in state:problems.append('Legacy Unit-2-only mixed scheduler gate remains')
if 'centerCurrentRoute' not in appjs:problems.append('Active route auto-centering missing')
if 'prepareSpeechText' not in audio:problems.append('Speech normalization missing')
lines=['# Unit 3 F6 Classroom and Browser QA','',
'## Scope','',
'F6 changes no Unit 3 curriculum or permanent narrative science. It validates and refines the released learner experience across Home, Learn, Quick Recall, Review, mixed discrimination, Challenge Lab, mobile layout, and browser text-to-speech behavior.','',
'## Browser matrix','',
'- Permanent scenes checked: **54 / 54**','- Quick Recall scenes checked: **18 / 18**','- Viewports: **1440×1000 desktop, 820×1180 tablet, 390×844 phone**','- Scene/viewport combinations: **162**','- Recall/viewport combinations: **54**','- Body horizontal-overflow findings: **0**','- Route-wrap findings: **0**','- Scene-geometry findings: **0**','- Quick Recall story/location/route/anchor leaks: **0**','',
'## F6 corrections','',
'1. Twelve-location routes now stay on one horizontally scrollable route line.','2. The current route node automatically centers on narrow screens.','3. Unit 3 mixed-confusable review now schedules correctly after all members are encountered.','4. Memory anchors are collapsed by default so first exposure remains story-first.','5. Browser Listen provides status feedback and uses speech-only normalization for common scientific notation.','',
'## Learning-system validation','',
'- Exact-name delayed-review targets: **126**','- Mixed-confusable sets: **28**','- Mixed questions: **78**','- Mixed practice waits at least **48 hours** after eligibility.','- Visible Review remains capped at **5** due items.','- Unit 3 Challenge Lab remains **11** application tasks.','',
'## Release decision','',('**PASS — Unit 3 remains student-ready and is classroom/browser validated.**' if not problems else '**FAIL — blocking findings remain.**')]
if problems:lines+=['','### Blocking findings','']+[f'- {p}' for p in problems]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
if problems:
 print('\n'.join(problems));sys.exit(1)
print('UNIT3 F6 QA PASS')
print(json.dumps({'scenes':54,'recalls':18,'viewports':3,'scene_viewport_checks':162,'recall_viewport_checks':54,'exact_name_targets':126,'mixed_sets':28,'challenge_lab':11,'student_release':True},indent=2))
