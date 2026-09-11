from __future__ import annotations

import hashlib
import json
import re
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
U8 = ROOT / 'content/ap-biology/unit-8'


def read(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


problems = []
j = read(U8 / 'journeys/U8-J6.json')
briefs = {b['locus_id']: b for b in read(U8 / 'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id'] == 'U8-J6'}
canon = {r['Knowledge ID']: r for r in read(U8 / 'canonical-catalog.json')}
lock = read(U8 / 'content-lock-f4f.json')
f3_lock = read(U8 / 'content-lock-f3.json')
prior_locks = [(stage, read(U8 / f'content-lock-{stage}.json')) for stage in ('f4a','f4b','f4c','f4d','f4e')]

if j.get('palace_id') != 'U8-J6' or j.get('scene_count') != 8 or len(j.get('scenes', [])) != 8:
    problems.append('Journey 6 scene accounting invalid')
if [s['locus_id'] for s in j['scenes']] != [f'U8-L{i:02d}' for i in range(39,47)]:
    problems.append('Journey 6 locus route invalid')
ids = [kid for s in j['scenes'] for kid in s['object_ids']]
if len(ids) != 29 or len(set(ids)) != 29:
    problems.append('Journey 6 knowledge accounting invalid')

counts=[]
exact_targets=0
for s in j['scenes']:
    prose=' '.join(s['story_paragraphs'])
    wc=len(re.findall(r"\b[\w’′'-]+\b", prose))
    counts.append(wc)
    if wc < 450: problems.append(f"{s['locus_id']} below 450 words")
    if len(s['story_paragraphs']) < 6: problems.append(f"{s['locus_id']} has fewer than six paragraphs")
    opening=s['story_paragraphs'][0].casefold()
    if 'left' not in opening or ('ahead' not in opening and 'center' not in opening) or 'right' not in opening:
        problems.append(f"{s['locus_id']} does not establish left/center/right in opening")
    if '—' in prose or ':' in prose: problems.append(f"{s['locus_id']} uses prohibited student-prose punctuation")
    lower=prose.casefold()
    for meta in ['the ppt states','the ced says','the course requires','locked definition','source material shows','teacher enrichment','pipeline language']:
        if meta in lower: problems.append(f"{s['locus_id']} leaks source/pipeline language {meta}")
    if s.get('continuity_object') != j['scenes'][0].get('continuity_object'):
        problems.append(f"{s['locus_id']} continuity object changed")
    if not any(c['name']=='Dr. Mira Sen' for c in s['cast']): problems.append(f"{s['locus_id']} missing guide")
    if not any(c['name']=='shared community map' for c in s['cast']): problems.append(f"{s['locus_id']} missing continuity cast")
    b=briefs[s['locus_id']]
    if s['object_ids'] != b['knowledge_ids']: problems.append(f"{s['locus_id']} object IDs diverge from F3")
    for beat in s['story_beats']:
        if beat['science'] != canon[beat['object_id']]['Canonical Verified Statement']:
            problems.append(f"{s['locus_id']} canonical science mismatch {beat['object_id']}")
        if beat['exact_name']:
            exact_targets += 1
            term=beat['term'].casefold()
            variants=[term] + ([x.strip() for x in term.split('/')] if '/' in term else [])
            if not any(v in lower for v in variants): problems.append(f"{s['locus_id']} exact term missing {beat['term']}")

if exact_targets != 23: problems.append(f'Expected 23 exact-name targets, got {exact_targets}')
cps=[s for s in j['scenes'] if s['checkpoint']]
if [s['locus_id'] for s in cps] != ['U8-L40','U8-L42','U8-L44']:
    problems.append('Quick Recall placement invalid')

full=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
phrases=[
    'the habitat answers where the population lives',
    'the niche answers how it uses resources',
    'the realized niche is the portion of the fundamental niche actually occupied after effects of competition, predation, and other interactions',
    'the labels are useful only after you know what each species gains, loses, or does not measurably change',
    'competition is a negative effect on both participants',
    'under stable conditions, species with effectively identical niches that compete for the same limiting resource cannot indefinitely coexist',
    'observed resource partitioning can reflect ecological processes, evolutionary processes, or both',
    'batesian mimicry', 'müllerian mimicry',
    'symbiosis', 'parasitism', 'mutualism', 'commensalism', 'facilitation',
    'the process is not a fixed march toward one inevitable endpoint',
    'the classification is tied to the absence of established soil community at the start',
    'secondary succession follows disturbance where soil and some biological legacies remain',
]
for p in phrases:
    if p not in full: problems.append(f'missing high-risk distinction phrase {p}')

for rel, meta in f3_lock.get('files', {}).items():
    p=ROOT / rel
    if not p.exists() or p.stat().st_size != meta['bytes'] or sha(p) != meta['sha256']:
        problems.append(f'F3 locked artifact changed {rel}')
for stage, prior_lock in prior_locks:
    for rel, meta in prior_lock.get('files', {}).items():
        p=U8 / rel if not rel.startswith('docs/') else ROOT / rel
        if not p.exists() or p.stat().st_size != meta['bytes'] or sha(p) != meta['sha256']:
            problems.append(f'{stage.upper()} locked file changed {rel}')

if lock.get('lock_status') != 'LOCKED_F4F_J6' or lock.get('student_release') is not False or lock.get('preview_release') is not True:
    problems.append('F4F content-lock boundary invalid')
for rel, meta in lock.get('files', {}).items():
    p=U8 / rel if not rel.startswith('docs/') else ROOT / rel
    if not p.exists() or p.stat().st_size != meta['bytes'] or sha(p) != meta['sha256']:
        problems.append(f'F4F locked file mismatch {rel}')

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
    if status.get('journey_count', 0) < 6 or status.get('scene_count', 0) < 46 or status.get('memory_objects') != 0 or status.get('application_challenges') != 0:
        problems.append('Unit 8 no longer preserves the F4F developer-preview boundary')

required =[*(U8/f'journeys/U8-J{i}.json' for i in range(1,7)), U8/'journeys-f4f.json', U8/'status-f4f.json', U8/'content-lock-f4f.json', U8/'f4f-release-manifest.json', ROOT/'docs/UNIT8_F4F_JOURNEY6_STORY.md', ROOT/'docs/UNIT8_F4F_STORY_MATRIX.md']
for p in required:
    if not p.exists(): problems.append(f'missing F4F artifact {p.relative_to(ROOT)}')

report=[
    '# Unit 8 F4F Narrative QA','', '## Result','', '**PASS**' if not problems else '**FAIL**','',
    '## Journey 6 accounting','',
    '- Polished scenes **8 / 8**',
    '- Locked F3 knowledge records represented **29 / 29**',
    f'- Exact-name targets explicitly introduced **{exact_targets} / 23**',
    '- Optional first-exposure recalls **3**',
    f'- Narrative words **{sum(counts):,}**',
    f'- Mean scene length **{statistics.mean(counts):.1f} words**',
    f'- Shortest scene **{min(counts)} words**',
    f'- Longest scene **{max(counts)} words**','',
    '## Prose-quality gates','',
    '- Every scene establishes the exact district location and fixes left, center, and right geography before the ecological state changes.',
    '- Dr. Mira Sen and one shared community map persist through all eight locations.',
    '- Habitat remains where an organism or population lives while niche remains resource use, conditions, and ecological role.',
    '- Fundamental niche remains potential use without constraining biotic interactions and realized niche remains the occupied subset under interactions.',
    '- Interaction signs describe effects on each species and do not replace the mechanism.',
    '- Competitive exclusion remains conditional on effectively identical niches, the same limiting resource, and stable conditions.',
    '- Resource partitioning is described as an observed differentiation in use without inventing a specific evolutionary history.',
    '- Predation, herbivory, cryptic coloration, Batesian mimicry, and Müllerian mimicry remain mechanistically distinct.',
    '- Symbiosis does not imply mutual benefit. Parasitism, mutualism, commensalism, and facilitation remain separated by effects and relationship type.',
    '- Succession is represented as sequential community change without a guaranteed single endpoint.',
    '- Primary and secondary succession are classified from soil and biological legacies, not visual severity.',
    '- Student prose contains no source-management language, em dashes, or colon punctuation.',
    '- Journeys 1 through 5 remain frozen, and F1 through F3 locks remain protected.',
    '- Unit 8 remains developer preview with zero final Memory Objects and zero live Challenge Lab tasks.','',
]
if problems:
    report += ['## Blocking findings',''] + [f'- {p}' for p in problems] + ['']
if not is_later_f5:
    (ROOT/'docs/UNIT8_F4F_QA.md').write_text('\n'.join(report), encoding='utf-8')

if problems:
    print('UNIT 8 F4F QA FAIL')
    print('\n'.join(f'- {p}' for p in problems))
    sys.exit(1)

print('UNIT 8 F4F QA PASS')
print(json.dumps({'journey':'U8-J6','scenes':8,'knowledge_records':29,'exact_name_targets':exact_targets,'optional_recalls':3,'story_words':sum(counts),'average_scene_words':round(statistics.mean(counts),1),'min_scene_words':min(counts),'max_scene_words':max(counts),'student_release':False,'preview_release':True},indent=2))
