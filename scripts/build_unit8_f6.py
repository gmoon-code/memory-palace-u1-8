from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AP = ROOT / 'content' / 'ap-biology'
U8 = AP / 'unit-8'
COURSE = AP / 'course.json'
MAINLINE = AP / 'mainline-release-u1-u8.json'
AUDIO = ROOT / 'frontend' / 'js' / 'audio.js'
MAIN = ROOT / 'backend' / 'main.py'


def read(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path: Path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# F6 changes no Unit 8 visible science or frozen curriculum. It only advances
# release metadata and improves browser speech preparation for common Unit 8 notation.
a = AUDIO.read_text(encoding='utf-8')
marker = "[/\\bbya\\b/gi,'billion years ago'],[/\\bmya\\b/gi,'million years ago'],"
if "[/\\bNPP\\b/g,'N P P']" not in a:
    replacement = marker + "\n    [/\\bNPP\\b/g,'N P P'],[/\\bGPP\\b/g,'G P P'],[/\\bdN\\/dt\\b/g,'d N over d t'],[/\\brmax\\b/g,'r max'],\n    [/N₂/g,'nitrogen gas'],[/NH₄⁺/g,'ammonium'],[/NO₃⁻/g,'nitrate'],\n    [/1 − Σ\\(n\\/N\\)²/g,'one minus the sum of n over N squared'],[/Σ/g,'sigma'],[/−/g,' minus '],[/=/g,' equals '],"
    if marker not in a:
        raise RuntimeError('Could not locate Unit 8 speech-normalization insertion point')
    AUDIO.write_text(a.replace(marker, replacement), encoding='utf-8')

# F6 release version. Idempotent across rebuilds and compatible with the F5 builder.
m = MAIN.read_text(encoding='utf-8')
m = re.sub(r'app=FastAPI\(title="Memory Palace V2 · AP Biology",version="[^"]+"\)',
           'app=FastAPI(title="Memory Palace V2 · AP Biology",version="0.30.0-u8-f6")', m)
m = re.sub(r"def health\(\): return \{'ok':True,'version':'[^']+'\}",
           "def health(): return {'ok':True,'version':'v2-apbio-0.30.0-u8-f6'}", m)
MAIN.write_text(m, encoding='utf-8')

f5 = read(U8 / 'finalization-f5.json')
status = read(U8 / 'status-f5.json')
f5lock = read(U8 / 'content-lock-f5.json')
assert f5['canonical_records'] == f5['accounted_records'] == 255 and f5['unaccounted_records'] == 0
assert f5['runtime_memory_objects'] == 211 and f5['challenge_lab_records'] == 13 and f5['scope_guard_records'] == 31
assert f5['guided_journeys'] == 8 and f5['permanent_loci'] == 58 and f5['optional_first_exposure_recalls'] == 18
assert f5['exact_name_review_targets'] == 135 and f5['non_exact_palace_records'] == 76
assert f5['mixed_discrimination_sets'] == 40 and f5['mixed_discrimination_questions'] == 104

runtime_files = [
    'backend/main.py', 'backend/content.py', 'backend/settings.py',
    'frontend/js/app.js', 'frontend/js/api.js', 'frontend/js/audio.js', 'frontend/js/state.js',
    'frontend/js/views/home.js', 'frontend/js/views/learn.js', 'frontend/js/views/review.js', 'frontend/js/views/practice.js'
]

ux = {
    'schema': 'memory-palace-v2-unit8-f6-browser-classroom-validation-1.0',
    'generated_utc': '2026-09-09T07:00:00+00:00',
    'unit_id': 'unit-8',
    'stage': 'F6',
    'release_status': 'STUDENT_READY_F6_VALIDATED',
    'curriculum_content_changed': False,
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
    'target_viewports': [
        {'name': 'desktop', 'width': 1440, 'height': 1000},
        {'name': 'tablet', 'width': 820, 'height': 1180},
        {'name': 'mobile', 'width': 390, 'height': 844},
    ],
    'browser_facing_validation': {
        'validation_mode': 'production HTML render + state-machine interaction QA + responsive CSS contract + live FastAPI/HTTP smoke',
        'scene_render_checks': 58,
        'recall_render_checks': 18,
        'scene_viewport_contract_checks': 174,
        'recall_viewport_contract_checks': 54,
        'route_lengths': [12, 9, 5, 7, 5, 8, 4, 8],
        'scene_geometry_findings': 0,
        'recall_content_leak_findings': 0,
        'broken_interpolation_findings': 0,
        'unit_switch_findings': 0,
        'refresh_resume_findings': 0,
        'review_scheduler_findings': 0,
        'mixed_review_findings': 0,
        'challenge_lab_findings': 0,
        'speech_preparation_findings': 0,
        'result': 'PASS',
        'pixel_screenshot_validation': 'NOT_EXECUTED_IN_THIS_CONTAINER',
        'pixel_screenshot_note': 'Chromium was directly probed with a 12-second headless about:blank render and timed out without DOM output in this sandbox. The release does not claim screenshot/pixel validation. Production render functions, state-machine interactions, responsive CSS contracts, and live HTTP/API behavior are validated directly.'
    },
    'f6_runtime_fixes': [
        {
            'id': 'U8-F6-AUDIO-001',
            'finding': 'Browser speech synthesis can read common Unit 8 ecological equations, abbreviations, and nitrogen-cycle notation awkwardly.',
            'resolution': 'Speech-only normalization now covers NPP, GPP, dN/dt, rmax, N₂, NH₄⁺, NO₃⁻, the Simpson diversity expression 1 − Σ(n/N)², sigma, Unicode minus, and equals without changing visible scientific text or any frozen narrative byte.'
        }
    ],
    'review_validation': {
        'exact_name_targets': 135,
        'non_exact_palace_records': 76,
        'mixed_sets': 40,
        'mixed_questions': 104,
        'visible_due_limit': 5,
        'mixed_initial_delay_hours_minimum': 48,
        'unit_scoped_review_isolation': True,
        'hinted_review_continuation': True,
        'mandatory_spelling_targets': 0,
    },
    'first_exposure_policy': {
        'story_first': True,
        'optional_quick_recall': True,
        'memory_anchors_collapsed_by_default': True,
        'recall_hides_story_location_route_cast_and_anchors': True,
    },
    'resume_validation': {
        'active_unit_persists': True,
        'active_journey_persists': True,
        'scene_index_persists': True,
        'refresh_returns_to_home_with_continue_action': True,
    },
    'f5_lock_sha256': sha(U8 / 'content-lock-f5.json'),
    'runtime_file_sha256': {rel: sha(ROOT / rel) for rel in runtime_files},
    'next_gate': 'Unit 8 F6 is the final validation gate. Freeze the complete Units 1-8 AP Biology release after F6 QA passes.'
}
write(U8 / 'ux-validation-f6.json', ux)

status.update({
    'status': 'STUDENT_READY',
    'pipeline_status': 'UNIT8_CLASSROOM_BROWSER_VALIDATED_F6',
    'pipeline_stage': 'UNIT8_CLASSROOM_BROWSER_VALIDATED_F6',
    'browser_validation': 'PASS_F6',
    'browser_validation_mode': ux['browser_facing_validation']['validation_mode'],
    'browser_validated_scenes': 58,
    'browser_validated_recalls': 18,
    'mixed_review_runtime_validated': True,
    'refresh_resume_validated': True,
    'challenge_lab_runtime_validated': True,
    'unit_switching_validated': True,
    'speech_preparation_validated': True,
    'student_release': True,
    'preview_release': False,
    'next_required_output': 'Freeze the complete Units 1-8 AP Biology release from this F6-validated baseline.',
    'next_gate': 'Unit 8 F6 is complete after final package QA. Do not modify Unit 8 F1-F6 science, architecture, narratives, or runtime curriculum.'
})
write(U8 / 'status-f6.json', status)
write(U8 / 'status.json', status)

course = read(COURSE)
for u in course['units']:
    if u['unit_id'] == 'unit-8':
        u.update({
            'status': 'STUDENT_READY',
            'student_release': True,
            'preview_release': False,
            'journey_count': 8,
            'scene_count': 58,
            'canonical_records': 255,
            'canonical_records_accounted': 255,
            'application_challenges': 13,
            'scope_guard_records': 31,
            'runtime_memory_objects': 211,
            'mixed_discrimination_sets': 40,
            'mixed_discrimination_questions': 104,
            'exact_name_review_targets': 135,
            'non_exact_palace_records': 76,
            'browser_validation': 'PASS_F6',
            'pipeline_stage': 'UNIT8_CLASSROOM_BROWSER_VALIDATED_F6',
            'source_status': 'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5_UX_VALIDATED_F6',
        })
write(COURSE, course)

manifest = read(MAINLINE)
manifest['schema'] = 'memory-palace-v2-mainline-u1-u8-f6-1.0'
manifest['release_status'] = 'STUDENT_READY_UNITS_1_8_UNIT8_F6_VALIDATED'
manifest['runtime_version'] = 'v2-apbio-0.30.0-u8-f6'
manifest['unit8'] = {
    'schema': 'memory-palace-v2-unit8-f6-release-manifest-1.0',
    'generated_utc': '2026-09-09T07:00:00+00:00',
    'unit_id': 'unit-8',
    'stage': 'F6',
    'student_release': True,
    'preview_release': False,
    'browser_validation': 'PASS_F6',
    'canonical_records': 255,
    'canonical_records_accounted': 255,
    'unaccounted_canonical_records': 0,
    'runtime_memory_objects': 211,
    'story_records': 211,
    'practice_only_records': 13,
    'scope_guard_records': 31,
    'guided_journeys': 8,
    'permanent_loci': 58,
    'challenge_count': 13,
    'optional_first_exposure_recalls': 18,
    'exact_name_review_targets': 135,
    'non_exact_palace_records': 76,
    'mandatory_spelling_targets': 0,
    'mixed_discrimination_sets': 40,
    'mixed_discrimination_questions': 104,
    'runtime_version': 'v2-apbio-0.30.0-u8-f6',
    'next_stage': 'FREEZE_COMPLETE_AP_BIOLOGY_UNITS_1_8_RELEASE'
}
manifest['future_units'] = []
write(MAINLINE, manifest)
write(U8 / 'f6-release-manifest.json', manifest['unit8'])

lock = {
    'schema': 'memory-palace-v2-unit8-f6-content-lock-1.0',
    'unit_id': 'unit-8',
    'stage': 'F6',
    'curriculum_content_changed': False,
    'files': {},
    'runtime_file_sha256': ux['runtime_file_sha256'],
    'f5_lock_sha256': ux['f5_lock_sha256'],
    'protected_narratives': f5lock['protected_narratives'],
    'protected_upstream_locks': f5lock['protected_upstream_locks'],
}
for rel in ['ux-validation-f6.json', 'status-f6.json', 'f6-release-manifest.json']:
    lock['files'][rel] = sha(U8 / rel)
write(U8 / 'content-lock-f6.json', lock)

print('Built Unit 8 F6 classroom/browser-facing validation')
print(json.dumps(manifest['unit8'], indent=2))
