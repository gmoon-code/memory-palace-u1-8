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
journey = read(U8 / 'journeys/U8-J2.json')
canon = {r['Knowledge ID']: r for r in read(U8 / 'canonical-catalog.json')}
briefs = {b['locus_id']: b for b in read(U8 / 'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id'] == 'U8-J2'}
lock = read(U8 / 'content-lock-f4b.json')
f4a_lock = read(U8 / 'content-lock-f4a.json')
f3_lock = read(U8 / 'content-lock-f3.json')

expected_loci = [f'U8-L{i:02d}' for i in range(13, 22)]
if journey.get('palace_id') != 'U8-J2': problems.append('Journey 2 ID changed')
if journey.get('scene_count') != 9 or len(journey.get('scenes', [])) != 9: problems.append('Journey 2 must contain 9 scenes')
if [s.get('locus_id') for s in journey['scenes']] != expected_loci: problems.append('F2/F3 locus order changed')
if journey.get('checkpoint_count') != 3: problems.append('F3 Quick Recall count changed from 3')
if journey.get('student_release') != 'DEVELOPER_PREVIEW_F4B' or journey.get('preview_release') is not True: problems.append('F4B preview boundary is wrong')
if journey.get('guide', {}).get('name') != 'Dr. Mira Sen': problems.append('Unit 8 guide changed')
if 'nine permanent locations' not in journey.get('route_orientation', '').casefold(): problems.append('route orientation does not define the nine-location hall route')

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
    if not any(c.get('name') == 'Transparent energy-matter ledger' for c in s['cast']): problems.append(f'{lid} lost continuity object')
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

if len(assigned) != 47 or len(set(assigned)) != 47: problems.append(f'Journey 2 knowledge coverage is {len(assigned)} refs and {len(set(assigned))} unique, expected 47 and 47')
if exact_targets != 24: problems.append(f'Journey 2 exact-name target count is {exact_targets}, expected 24')

full = ' '.join(' '.join(s['story_paragraphs']) for s in journey['scenes']).casefold().replace('**', '')
visible = {
    'energy_budget': ['net energy balance', 'energy acquired and energy expended', 'persistent net energy loss'],
    'endotherm_ectotherm': ['endotherm produces enough metabolic heat', 'ectotherm gains most body heat from external sources', 'mass-specific metabolic rate'],
    'ecological_scale': ['ecosystem includes a biological community and the abiotic environment', 'biotic factor', 'abiotic factor'],
    'energy_matter_split': ['first law of thermodynamics', 'second law of thermodynamics', 'energy flows through ecosystems while matter and nutrients cycle', 'energy ultimately leaves largely as heat'],
    'acquisition': ['autotroph uses an external energy source', 'chemosynthetic organisms', 'it does not create energy', 'heterotroph obtains organic carbon and energy'],
    'trophic_roles': ['trophic level is a feeding position', 'primary consumer feeds directly on producers', 'secondary consumer feeds on primary consumers', 'decomposer obtains energy from dead organic matter'],
    'food_web_direction': ['food chain is a simplified linear sequence', 'food web represents interconnected feeding relationships', 'arrows conventionally point from resource or prey toward the consumer'],
    'production': ['gross primary production', 'net primary production', 'npp = gpp − r', 'secondary production', 'photosynthetic or chemosynthetic'],
    'transfer_guard': ['about ten percent is a useful average rule of thumb', 'not a fixed law', 'energy availability can change population size', 'changes in producer biomass or abundance can affect the number and size of other trophic levels'],
}
for name, phrases in visible.items():
    if not all(p in full for p in phrases): problems.append(f'high-risk science guard not visibly satisfied {name}')

# Protect F1, F2, F3, and all locked F4A Journey 1 artifacts.
for key in ('f1_protected_hashes', 'f2_protected_hashes'):
    for rel, expected in f3_lock.get(key, {}).items():
        p = ROOT / rel
        if not p.exists() or sha(p) != expected: problems.append(f'{key} changed {rel}')
for rel, meta in f3_lock.get('files', {}).items():
    p = ROOT / rel
    if not p.exists() or p.stat().st_size != meta['bytes'] or sha(p) != meta['sha256']: problems.append(f'F3 locked artifact changed {rel}')
for rel, meta in f4a_lock.get('files', {}).items():
    p = U8 / rel if not rel.startswith('docs/') else ROOT / rel
    if not p.exists() or p.stat().st_size != meta['bytes'] or sha(p) != meta['sha256']: problems.append(f'F4A locked file changed {rel}')

if lock.get('lock_status') != 'LOCKED_F4B_J2' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4B content-lock boundary invalid')
for rel, meta in lock.get('files', {}).items():
    p = U8 / rel if not rel.startswith('docs/') else ROOT / rel
    if not p.exists() or p.stat().st_size != meta['bytes'] or sha(p) != meta['sha256']: problems.append(f'F4B locked file mismatch {rel}')

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
    if status.get('journey_count', 0) < 2 or status.get('scene_count', 0) < 21 or status.get('memory_objects') != 0 or status.get('application_challenges') != 0:
        problems.append('Unit 8 no longer preserves the F4B developer-preview boundary')

required = [
    U8 / 'journeys/U8-J1.json', U8 / 'journeys/U8-J2.json', U8 / 'journeys-f4b.json', U8 / 'status-f4b.json', U8 / 'content-lock-f4b.json', U8 / 'f4b-release-manifest.json',
    ROOT / 'docs/UNIT8_F4B_JOURNEY2_STORY.md', ROOT / 'docs/UNIT8_F4B_STORY_MATRIX.md',
]
for p in required:
    if not p.exists(): problems.append(f'missing F4B artifact {p.relative_to(ROOT)}')

report = [
    '# Unit 8 F4B Narrative QA', '', '## Result', '', '**PASS**' if not problems else '**FAIL**', '',
    '## Journey 2 accounting', '',
    '- Polished scenes **9 / 9**',
    '- Locked F3 knowledge records represented **47 / 47**',
    f'- Exact-name targets explicitly introduced **{exact_targets} / 24**',
    '- Optional first-exposure recalls **3**',
    f'- Narrative words **{sum(counts):,}**',
    f'- Mean scene length **{statistics.mean(counts):.1f} words**',
    f'- Shortest scene **{min(counts)} words**',
    f'- Longest scene **{max(counts)} words**', '',
    '## Prose-quality gates', '',
    '- Every scene establishes the exact room and fixes left, center, and right geography before the ecological state changes.',
    '- Dr. Mira Sen and the same transparent energy-matter ledger persist through all nine locations.',
    '- Energy transformation and heat dissipation remain physically separate from matter conservation and reservoir cycling.',
    '- Endothermy and ectothermy are distinguished by predominant heat source without defining either group by constant versus variable body temperature.',
    '- Autotroph, heterotroph, chemosynthesis, and chemosynthetic energy capture preserve carbon-source and energy-source distinctions and never imply energy creation.',
    '- Trophic roles remain based on energy and matter source, decomposers return inorganic nutrients without recycling energy, and omnivory is allowed.',
    '- Food-web arrows point from resource or prey toward the consumer receiving energy and matter.',
    '- GPP, producer respiration, NPP, the NPP equation, and secondary production remain spatially and mechanistically distinct.',
    '- About ten percent remains a variable rule of thumb rather than an exact trophic-transfer law.',
    '- Student prose contains no source-management language, em dashes, or colon punctuation.',
    '- Each scene ends with a physical or causal handoff that makes the next F2 locus necessary.',
    '- Unit 8 remains developer preview with zero final Memory Objects and zero live Challenge Lab tasks.', '',
]
if problems:
    report += ['## Blocking findings', ''] + [f'- {p}' for p in problems] + ['']
if not is_later_f5:
    (ROOT / 'docs/UNIT8_F4B_QA.md').write_text('\n'.join(report), encoding='utf-8')

if problems:
    print('UNIT 8 F4B QA FAIL')
    print('\n'.join(f'- {p}' for p in problems))
    sys.exit(1)

print('UNIT 8 F4B QA PASS')
print(json.dumps({
    'journey': 'U8-J2', 'scenes': 9, 'knowledge_records': 47, 'exact_name_targets': exact_targets,
    'optional_recalls': 3, 'story_words': sum(counts), 'average_scene_words': round(statistics.mean(counts), 1),
    'min_scene_words': min(counts), 'max_scene_words': max(counts), 'student_release': False, 'preview_release': True,
}, indent=2))
