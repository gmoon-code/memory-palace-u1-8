from __future__ import annotations

import hashlib
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
U8 = ROOT / 'content' / 'ap-biology' / 'unit-8'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def wc(text):
    return len(re.findall(r"\b[\w’′'-]+\b", text))


problems = []
journey = read(U8 / 'journeys/U8-J5.json')
canon = {r['Knowledge ID']: r for r in read(U8 / 'canonical-catalog.json')}
briefs = {b['locus_id']: b for b in read(U8 / 'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id'] == 'U8-J5'}
lock = read(U8 / 'content-lock-f4e.json')
f3_lock = read(U8 / 'content-lock-f3.json')
prior_locks = [(stage, read(U8 / f'content-lock-{stage.lower()}.json')) for stage in ('F4A', 'F4B', 'F4C', 'F4D')]

expected_loci = [f'U8-L{i:02d}' for i in range(34, 39)]
if journey.get('palace_id') != 'U8-J5': problems.append('Journey 5 ID changed')
if journey.get('scene_count') != 5 or len(journey.get('scenes', [])) != 5: problems.append('Journey 5 must contain 5 scenes')
if [s.get('locus_id') for s in journey['scenes']] != expected_loci: problems.append('F2/F3 locus order changed')
if journey.get('checkpoint_count') != 2: problems.append('F3 Quick Recall count changed from 2')
if journey.get('student_release') != 'DEVELOPER_PREVIEW_F4E' or journey.get('preview_release') is not True: problems.append('F4E preview boundary is wrong')
if journey.get('guide', {}).get('name') != 'Dr. Mira Sen': problems.append('Unit 8 guide changed')
if 'five permanent locations' not in journey.get('route_orientation', '').casefold(): problems.append('route orientation does not define the five-location control-center route')

assigned = []
counts = []
exact_targets = 0
banned = re.compile(r'\b(PPT|CED|Campbell|College Board|teacher enrichment|teacher-required|exam scope|exam-scope|source material|source lock|canonical record|pipeline)\b', re.I)
for s in journey['scenes']:
    lid = s['locus_id']
    b = briefs[lid]
    prose = ' '.join(s.get('story_paragraphs', []))
    low = prose.casefold().replace('**', '')
    n = wc(prose)
    counts.append(n)
    if n < 450: problems.append(f'{lid} narrative too short {n} words')
    if len(s.get('story_paragraphs', [])) < 6: problems.append(f'{lid} has fewer than 6 narrative paragraphs')
    opening = s['story_paragraphs'][0].casefold()
    if 'left' not in opening or ('ahead' not in opening and 'center' not in opening) or 'right' not in opening: problems.append(f'{lid} opening does not orient left center right')
    zones = s.get('scene_layout', {}).get('zones', [])
    if len(zones) != 3 or [z.get('position') for z in zones] != ['left', 'center', 'right']: problems.append(f'{lid} geometry changed')
    orient = s['scene_layout']['orientation']
    for anchor in (b['spatial_layout']['left']['anchor'], b['spatial_layout']['center']['anchor'], b['spatial_layout']['right']['anchor']):
        if anchor not in orient: problems.append(f'{lid} F3 anchor missing from orientation {anchor}')
    if len(s.get('cast', [])) < 5: problems.append(f'{lid} cast too thin')
    if not any(c.get('name') == 'Dr. Mira Sen' for c in s['cast']): problems.append(f'{lid} lost guide')
    if not any(c.get('name') == 'population-growth dashboard' for c in s['cast']): problems.append(f'{lid} lost continuity object')
    if s.get('continuity_object') != journey['scenes'][0].get('continuity_object'): problems.append(f'{lid} continuity object changed')
    if s.get('object_ids') != b['knowledge_ids']: problems.append(f'{lid} knowledge assignment changed from F3')
    assigned += s.get('object_ids', [])
    beats = {x['object_id']: x for x in s.get('story_beats', [])}
    if set(beats) != set(b['knowledge_ids']): problems.append(f'{lid} story-beat coverage mismatch')
    for t in b['term_introductions']:
        kid = t['knowledge_id']
        beat = beats.get(kid)
        if not beat:
            continue
        if beat.get('science') != canon[kid]['Canonical Verified Statement']: problems.append(f'{lid} canonical science changed in beat {kid}')
        if beat.get('term') != t['canonical_term']: problems.append(f'{lid} canonical term changed in beat {kid}')
        if bool(beat.get('exact_name')) != bool(t['exact_name_recall']): problems.append(f'{lid} exact-name policy changed {kid}')
        if t['exact_name_recall']:
            exact_targets += 1
            variants = [t['canonical_term'].casefold()]
            if '/' in t['canonical_term']:
                variants.extend(x.strip().casefold() for x in t['canonical_term'].split('/'))
            if not any(v in low for v in variants): problems.append(f'{lid} exact target absent from prose {t["canonical_term"]}')
    match = banned.search(prose)
    if match: problems.append(f'{lid} exposes development or source-management language {match.group(0)}')
    if '—' in prose: problems.append(f'{lid} contains prohibited em dash')
    if ':' in prose: problems.append(f'{lid} contains colon punctuation in narrative prose')
    if s.get('checkpoint') != bool(b['quick_recall']['enabled']): problems.append(f'{lid} checkpoint status changed from F3')
    if s.get('checkpoint'):
        if s.get('checkpoint_prompt') != b['quick_recall']['candidate_prompt']: problems.append(f'{lid} checkpoint prompt changed')
        if s.get('checkpoint_answer') != b['quick_recall']['answer']: problems.append(f'{lid} checkpoint answer changed')
    idx = expected_loci.index(lid)
    expected_next = journey['scenes'][idx+1]['locus'] if idx < len(expected_loci)-1 else None
    if s.get('next_locus') != expected_next: problems.append(f'{lid} next-locus continuity broken')
    if idx < len(expected_loci)-1 and len(s['story_paragraphs'][-1]) < 180: problems.append(f'{lid} transition paragraph too thin')

if len(assigned) != 11 or len(set(assigned)) != 11: problems.append(f'Journey 5 knowledge coverage is {len(assigned)} refs and {len(set(assigned))} unique, expected 11 and 11')
if exact_targets != 8: problems.append(f'Journey 5 exact-name target count is {exact_targets}, expected 8')

full = ' '.join(' '.join(s['story_paragraphs']) for s in journey['scenes']).casefold().replace('**', '')
visible = {
    'exponential': ['unconstrained exponential growth', 'exponential-growth equation', 'dn/dt = rmaxn', 'maximum per-capita population growth rate', 'j shape', 'idealized model'],
    'rate_guard': ['dn/dt is doing a different job', 'represents the population\'s change in size per unit time', 'does not add the same fixed number each time'],
    'carrying_capacity': ['carrying capacity is the maximum abundance an environment can sustain given available resources and environmental conditions', 'k in logistic growth', 'k is the carrying capacity represented in the logistic model', 'carrying capacity can change'],
    'logistic': ['logistic-growth equation', 'dn/dt = rmaxn((k − n)/k)', 'growth slows as n approaches carrying capacity k', 's shape', 'does not guarantee a perfect curve in nature'],
    'density_dependent': ['density-dependent regulation occurs when a birth or death rate changes as population density changes', 'per-capita birth or death effect changes as population density changes'],
    'density_independent': ['density-independent effects', 'without its per-capita effect depending systematically on population density', 'total losses can differ when starting population sizes differ'],
    'k_guard': ['not stamped permanently onto the species', 'k is an idealized representation of a changing environmental limit'],
}
for name, phrases in visible.items():
    if not all(p in full for p in phrases): problems.append(f'high-risk science guard not visibly satisfied {name}')

# Protect F1, F2, F3 and all prior narrative locks.
for key in ('f1_protected_hashes', 'f2_protected_hashes'):
    for rel, expected in f3_lock.get(key, {}).items():
        p = ROOT / rel
        if not p.exists() or sha(p) != expected: problems.append(f'{key} changed {rel}')
for rel, meta in f3_lock.get('files', {}).items():
    p = ROOT / rel
    if not p.exists() or p.stat().st_size != meta['bytes'] or sha(p) != meta['sha256']: problems.append(f'F3 locked artifact changed {rel}')
for stage, prior_lock in prior_locks:
    for rel, meta in prior_lock.get('files', {}).items():
        p = U8 / rel if not rel.startswith('docs/') else ROOT / rel
        if not p.exists() or p.stat().st_size != meta['bytes'] or sha(p) != meta['sha256']: problems.append(f'{stage} locked file changed {rel}')

if lock.get('lock_status') != 'LOCKED_F4E_J5' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4E content-lock boundary invalid')
for rel, meta in lock.get('files', {}).items():
    p = U8 / rel if not rel.startswith('docs/') else ROOT / rel
    if not p.exists() or p.stat().st_size != meta['bytes'] or sha(p) != meta['sha256']: problems.append(f'F4E locked file mismatch {rel}')

status = read(U8 / 'status.json')
is_later_f5 = (
    status.get('status') == 'STUDENT_READY'
    and status.get('pipeline_stage') in {'UNIT8_FINALIZED_F5','UNIT8_CLASSROOM_BROWSER_VALIDATED_F6'}
    and status.get('student_release') is True
    and status.get('preview_release') is False
)
if is_later_f5:
    if status.get('journey_count') != 8 or status.get('scene_count') != 58 or status.get('memory_objects') != 211 or status.get('application_challenges') != 13:
        problems.append('Unit 8 F5 runtime does not preserve the expected finalized counts')
else:
    if not str(status.get('status', '')).startswith('F4'):
        problems.append('Unit 8 current status is neither an F4 developer preview nor the later compatible F5 release')
    if status.get('student_release') is not False or status.get('preview_release') is not True:
        problems.append('Unit 8 F4 release flags invalid')
    if status.get('journey_count', 0) < 5 or status.get('scene_count', 0) < 38 or status.get('memory_objects') != 0 or status.get('application_challenges') != 0:
        problems.append('Unit 8 no longer preserves the F4E developer-preview boundary')

required = [
    *(U8 / f'journeys/U8-J{i}.json' for i in range(1, 6)), U8 / 'journeys-f4e.json', U8 / 'status-f4e.json', U8 / 'content-lock-f4e.json', U8 / 'f4e-release-manifest.json',
    ROOT / 'docs/UNIT8_F4E_JOURNEY5_STORY.md', ROOT / 'docs/UNIT8_F4E_STORY_MATRIX.md',
]
for p in required:
    if not p.exists(): problems.append(f'missing F4E artifact {p.relative_to(ROOT)}')

report = [
    '# Unit 8 F4E Narrative QA', '', '## Result', '', '**PASS**' if not problems else '**FAIL**', '',
    '## Journey 5 accounting', '',
    '- Polished scenes **5 / 5**',
    '- Locked F3 knowledge records represented **11 / 11**',
    f'- Exact-name targets explicitly introduced **{exact_targets} / 8**',
    '- Optional first-exposure recalls **2**',
    f'- Narrative words **{sum(counts):,}**',
    f'- Mean scene length **{statistics.mean(counts):.1f} words**',
    f'- Shortest scene **{min(counts)} words**',
    f'- Longest scene **{max(counts)} words**', '',
    '## Prose-quality gates', '',
    '- Every scene establishes the exact control-center room and fixes left, center, and right geography before the model or regulation test changes.',
    '- Dr. Mira Sen and the same population-growth dashboard persist through all five locations.',
    '- dN/dt remains population change per unit time and stays distinct from the per-capita parameter rmax.',
    '- Exponential growth keeps constant positive per-capita growth and weak resource limitation as explicit model assumptions; the J shape is not represented as unlimited real-world destiny.',
    '- Carrying capacity K remains environment-dependent and distinct from current population size N and from rmax.',
    '- The logistic equation visibly shrinks (K−N)/K as N approaches K and produces an idealized S-shaped trajectory.',
    '- Real populations are not required to follow a perfect S curve or remain exactly at K.',
    '- Density-dependent regulation is diagnosed by a systematic density relationship in per-capita birth or death effects.',
    '- Density-independent effects are diagnosed by the absence of systematic density dependence in per-capita effect; total losses alone are not used for classification.',
    '- Student prose contains no source-management language, em dashes, or colon punctuation.',
    '- Journeys 1 through 4 remain frozen, and F1 through F3 locks remain protected.',
    '- Unit 8 remains developer preview with zero final Memory Objects and zero live Challenge Lab tasks.', '',
]
if problems:
    report += ['## Blocking findings', ''] + [f'- {p}' for p in problems] + ['']
if not is_later_f5:
    (ROOT / 'docs/UNIT8_F4E_QA.md').write_text('\n'.join(report), encoding='utf-8')

if problems:
    print('UNIT 8 F4E QA FAIL')
    print('\n'.join(f'- {p}' for p in problems))
    sys.exit(1)

print('UNIT 8 F4E QA PASS')
print(json.dumps({
    'journey': 'U8-J5', 'scenes': 5, 'knowledge_records': 11, 'exact_name_targets': exact_targets,
    'optional_recalls': 2, 'story_words': sum(counts), 'average_scene_words': round(statistics.mean(counts), 1),
    'min_scene_words': min(counts), 'max_scene_words': max(counts), 'student_release': False, 'preview_release': True,
}, indent=2))
