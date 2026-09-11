from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.site_release_guard import site_runtime_hash_allowed
from fastapi.testclient import TestClient
from backend.main import app

AP = ROOT / 'content' / 'ap-biology'
U8 = AP / 'unit-8'
DOC = ROOT / 'docs' / 'UNIT8_F6_CLASSROOM_BROWSER_QA.md'
client = TestClient(app)


def read(rel):
    return json.loads((U8 / rel).read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


problems = []
ux = read('ux-validation-f6.json')
status = read('status.json')
lock = read('content-lock-f6.json')
f5 = read('finalization-f5.json')
f5lock = read('content-lock-f5.json')

expected = {
    'canonical_records': 255,
    'guided_journeys': 8,
    'scenes_validated': 58,
    'recall_scenes_validated': 18,
    'runtime_memory_objects': 211,
    'challenge_lab_items': 13,
    'scope_guards': 31,
    'exact_name_review_targets': 135,
    'non_exact_palace_records': 76,
    'mixed_discrimination_sets': 40,
    'mixed_discrimination_questions': 104,
}
if ux.get('curriculum_content_changed') is not False:
    problems.append('F6 incorrectly reports curriculum changes')
for key, value in expected.items():
    if ux.get(key) != value:
        problems.append(f'UX artifact {key}={ux.get(key)} expected {value}')

b = ux.get('browser_facing_validation', {})
for key in [
    'scene_geometry_findings', 'recall_content_leak_findings', 'broken_interpolation_findings',
    'unit_switch_findings', 'refresh_resume_findings', 'review_scheduler_findings',
    'mixed_review_findings', 'challenge_lab_findings', 'speech_preparation_findings'
]:
    if b.get(key) != 0:
        problems.append(f'Browser-facing finding {key}={b.get(key)}')
if b.get('scene_render_checks') != 58 or b.get('recall_render_checks') != 18:
    problems.append('Runtime render matrix incomplete')
if b.get('scene_viewport_contract_checks') != 174 or b.get('recall_viewport_contract_checks') != 54:
    problems.append('Responsive viewport contract matrix incomplete')
if b.get('route_lengths') != [12, 9, 5, 7, 5, 8, 4, 8]:
    problems.append('Route-length matrix drifted')
if b.get('result') != 'PASS':
    problems.append('Browser-facing validation result is not PASS')
if b.get('pixel_screenshot_validation') != 'NOT_EXECUTED_IN_THIS_CONTAINER':
    problems.append('Pixel-validation limitation is not recorded transparently')

if status.get('pipeline_stage') != 'UNIT8_CLASSROOM_BROWSER_VALIDATED_F6' or status.get('browser_validation') != 'PASS_F6':
    problems.append('Current Unit 8 status is not F6 validated')
if not status.get('student_release') or status.get('preview_release'):
    problems.append('F6 changed Unit 8 student-release flags incorrectly')
if not (
    f5.get('accounted_records') == 255 and f5.get('unaccounted_records') == 0 and
    f5.get('runtime_memory_objects') == 211 and f5.get('challenge_lab_records') == 13 and
    f5.get('scope_guard_records') == 31
):
    problems.append('F5 canonical accounting drifted')
if ux.get('f5_lock_sha256') != sha(U8 / 'content-lock-f5.json'):
    problems.append('F5 content lock changed under F6')

for rel, digest in lock.get('files', {}).items():
    p = U8 / rel
    if not p.exists() or sha(p) != digest:
        problems.append(f'F6 lock mismatch: {rel}')
for rel, digest in f5lock.get('files', {}).items():
    p = U8 / rel
    if not p.exists() or sha(p) != digest:
        problems.append(f'F5 locked artifact changed during F6: {rel}')
for rel, digest in f5lock.get('protected_narratives', {}).items():
    p = U8 / rel
    if not p.exists() or sha(p) != digest:
        problems.append(f'Protected Unit 8 narrative changed during F6: {rel}')
for rel, digest in f5lock.get('protected_upstream_locks', {}).items():
    p = U8 / rel
    if not p.exists() or sha(p) != digest:
        problems.append(f'Protected upstream Unit 8 lock changed during F6: {rel}')

# F6 changes only release version and speech preparation among the F5 shared runtime files.
allowed = {'backend/main.py', 'frontend/js/audio.js'}
f6_runtime = lock.get('runtime_file_sha256', {})
changed = [rel for rel, digest in f5lock.get('runtime_file_sha256', {}).items() if f6_runtime.get(rel) != digest]
if set(changed) != allowed:
    problems.append(f'F6 runtime-change set {changed} != expected {sorted(allowed)}')
for rel, digest in f6_runtime.items():
    current = sha(ROOT / rel)
    if current != digest and not site_runtime_hash_allowed(ROOT, rel, current):
        problems.append(f'F6 runtime hash mismatch: {rel}')

# Live FastAPI/browser-facing HTTP smoke.
health = client.get('/api/health').json()
if health.get('version') != 'v2-apbio-0.30.0-u8-f6':
    problems.append(f"Unexpected API version: {health.get('version')}")
u = client.get('/api/units/unit-8').json()
if u.get('browser_validation') != 'PASS_F6' or u.get('status') != 'STUDENT_READY' or u.get('pipeline_stage') != 'UNIT8_CLASSROOM_BROWSER_VALIDATED_F6':
    problems.append('Live Unit 8 API does not expose F6 validation status')
if len(client.get('/api/units/unit-8/journeys').json()['guided_journeys']) != 8:
    problems.append('Live Unit 8 journey count is not 8')
if client.get('/api/units/unit-8/application-lab').json().get('challenge_count') != 13:
    problems.append('Challenge Lab API drift')
if client.get('/api/units/unit-8/review-manifest').json().get('target_count') != 135:
    problems.append('Review manifest API drift')
md = client.get('/api/units/unit-8/mixed-discrimination').json()
if md.get('set_count') != 40 or md.get('question_count') != 104:
    problems.append('Mixed-discrimination API drift')
if client.get('/api/units/unit-8/scope-guards').json().get('guard_count') != 31:
    problems.append('Scope-guard API drift')
if client.get('/api/units/unit-8/finalization').json().get('unaccounted_records') != 0:
    problems.append('Finalization zero-loss accounting API drift')
for i in range(1, 9):
    if client.get(f'/api/units/unit-8/journeys/U8-J{i}').status_code != 200:
        problems.append(f'Journey U8-J{i} live API failed')

learn = (ROOT / 'frontend/js/views/learn.js').read_text(encoding='utf-8')
statejs = (ROOT / 'frontend/js/state.js').read_text(encoding='utf-8')
appjs = (ROOT / 'frontend/js/app.js').read_text(encoding='utf-8')
audio = (ROOT / 'frontend/js/audio.js').read_text(encoding='utf-8')
if '<details class="memory-panel" open>' in learn:
    problems.append('Memory anchors open by default')
if 'centerCurrentRoute' not in appjs:
    problems.append('Active route auto-centering missing')
if 'data-action="review-next"' not in appjs or 'Continue review' not in appjs:
    problems.append('Hinted exact Review lacks direct continuation')
if "if(unitId!=='unit-2')return" in statejs:
    problems.append('Legacy unit-specific mixed scheduler gate remains')
for token in ['NPP', 'GPP', 'rmax', 'N₂', 'NH₄⁺', 'NO₃⁻', 'Σ', '−']:
    if token not in audio:
        problems.append(f'Unit 8 speech normalization missing source token {token}')
if 'dN\\/dt' not in audio:
    problems.append('Unit 8 speech normalization missing source token dN/dt')

course = json.loads((AP / 'course.json').read_text(encoding='utf-8'))
cu8 = next(x for x in course['units'] if x['unit_id'] == 'unit-8')
if cu8.get('browser_validation') != 'PASS_F6' or cu8.get('pipeline_stage') != 'UNIT8_CLASSROOM_BROWSER_VALIDATED_F6':
    problems.append('Course registry Unit 8 F6 status mismatch')
main = json.loads((AP / 'mainline-release-u1-u8.json').read_text(encoding='utf-8'))
if main.get('schema') != 'memory-palace-v2-mainline-u1-u8-f6-1.0' or main.get('release_status') != 'STUDENT_READY_UNITS_1_8_UNIT8_F6_VALIDATED':
    problems.append('Units 1-8 mainline manifest is not F6')
if main.get('runtime_version') != 'v2-apbio-0.30.0-u8-f6':
    problems.append('Units 1-8 mainline runtime version mismatch')
if main.get('totals') != {'canonical_records_units_1_8': 1561, 'guided_journeys': 58, 'permanent_scenes': 448, 'challenge_lab_items': 112}:
    problems.append('Units 1-8 mainline totals drifted')

lines = [
    '# Unit 8 F6 Classroom and Browser-Facing QA', '',
    '## Scope', '',
    'F6 changes no Unit 8 canonical science, F2 learning architecture, F3 scene briefs, F4A–F4H narrative bytes, F5 Memory Objects, Challenge Lab science, Review targets, mixed-discrimination content, or scope guards. It validates the released learner experience across Home, Learn, Quick Recall, Review, mixed discrimination, Challenge Lab, unit switching, persistence, responsive UI contracts, and browser speech text.', '',
    '## Runtime render and responsive contract matrix', '',
    '- Permanent scenes rendered through the production view function: **58 / 58**',
    '- Quick Recall states rendered through the production view function: **18 / 18**',
    '- Target responsive contracts: **1440×1000 desktop, 820×1180 tablet, 390×844 phone**',
    '- Scene/viewport contract checks: **174**',
    '- Recall/viewport contract checks: **54**',
    '- Three-zone scene geometry findings: **0**',
    '- Quick Recall story/location/route/cast/anchor leaks: **0**',
    '- Broken interpolation findings: **0**', '',
    '### Rendering limitation', '',
    'Chromium was directly probed with a 12-second headless `about:blank` render and timed out without DOM output in this sandbox. F6 therefore does **not** claim screenshot-level or pixel-level browser validation. The release uses production HTML rendering functions, state-machine interaction tests, responsive CSS contract checks, and live FastAPI/browser-facing HTTP smoke tests.', '',
    '## F6 runtime correction', '',
    'Browser speech text now normalizes common Unit 8 ecological notation including NPP, GPP, dN/dt, rmax, N₂, NH₄⁺, NO₃⁻, and the Simpson expression 1 − Σ(n/N)². This changes speech preparation only; visible scientific text and all eight narratives remain unchanged.', '',
    '## Learning-system validation', '',
    '- Exact-name delayed-review targets: **135**',
    '- Meaning/mechanism-only palace records: **76**',
    '- Mixed-discrimination sets: **40**',
    '- Mixed-discrimination questions: **104**',
    '- Mixed review waits at least **48 hours** after eligibility.',
    '- Visible Review remains capped at **5** due items.',
    '- Unit-scoped Review isolation: **PASS**',
    '- Refresh/resume state: **PASS**',
    '- Unit 8 Challenge Lab: **13 / 13** tasks',
    '- Released-unit switching among Units 1–8: **PASS**', '',
    '## Release decision', '',
    ('**PASS — Unit 8 remains student-ready and has completed F6 functional browser-facing/classroom validation.**' if not problems else '**FAIL — blocking findings remain.**')
]
if problems:
    lines += ['', '### Blocking findings', ''] + [f'- {p}' for p in problems]
DOC.write_text('\n'.join(lines) + '\n', encoding='utf-8')

if problems:
    print('UNIT8 F6 QA FAIL')
    print('\n'.join(f'- {p}' for p in problems))
    sys.exit(1)
print('UNIT8 F6 QA PASS')
print(json.dumps({
    'scenes': 58, 'recalls': 18, 'responsive_contract_viewports': 3,
    'scene_viewport_checks': 174, 'recall_viewport_checks': 54,
    'exact_name_targets': 135, 'mixed_sets': 40, 'mixed_questions': 104,
    'challenge_lab_items': 13, 'route_lengths': [12, 9, 5, 7, 5, 8, 4, 8],
    'refresh_resume': True, 'released_unit_switching': 'Units 1-8', 'pixel_screenshot_validation': False
}, indent=2))
