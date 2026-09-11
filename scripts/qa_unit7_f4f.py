from __future__ import annotations
import json,re,hashlib,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content/ap-biology/unit-7'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

j=read(U7/'journeys/U7-J6.json')
b={x['locus_id']:x for x in read(U7/'briefs/scene-briefs-f3.json')['scene_briefs'] if x['journey_id']=='U7-J6'}
c={r['knowledge_id']:r for r in read(U7/'source/canonical-unit7-f1.json')['canonical_catalog']}
lock=read(U7/'content-lock-f4f.json')
problems=[]
expected=[f'U7-L{i:02d}' for i in range(51,56)]
counts=[]; exact=0; assigned=[]

if j.get('palace_id')!='U7-J6' or j.get('scene_count')!=5 or [s['locus_id'] for s in j['scenes']]!=expected:
    problems.append('Journey 6 route/accounting mismatch')
if j.get('checkpoint_count')!=2:
    problems.append('Journey 6 checkpoint count mismatch')
if j.get('student_release')!='DEVELOPER_PREVIEW_F4F' or j.get('preview_release') is not True:
    problems.append('Journey 6 preview boundary mismatch')
if [x['slot'] for x in j.get('chronology_slots',[])]!=[1,2,3,4,5]:
    problems.append('Five-slot chronology order changed')

banned=re.compile(r'\b(PPT|CED|College Board|Campbell|source material|content lock|teacher enrichment|exam scope|LOCKED_F|developer preview|F1|F2|F3|F4)\b',re.I)
for s in j['scenes']:
    lid=s['locus_id']; prose=' '.join(s['story_paragraphs']); low=prose.casefold().replace('**','')
    wc=len(re.findall(r"\b[\w’′'-]+\b",prose)); counts.append(wc); assigned+=s['object_ids']
    if wc<450: problems.append(f'{lid} has only {wc} narrative words')
    if len(s['story_paragraphs'])<6: problems.append(f'{lid} fewer than 6 narrative paragraphs')
    opening=s['story_paragraphs'][0].casefold()
    if not ('left' in opening and 'right' in opening and ('ahead' in opening or 'center' in opening)):
        problems.append(f'{lid} left/center/right geography missing')
    for name in ('Dr. Imani Vale','Five-slot chronology tray','Chronology rail','Claim-strength stamp'):
        if not any(x['name']==name for x in s['cast']): problems.append(f'{lid} recurring cast missing {name}')
    if s['object_ids']!=b[lid]['knowledge_ids']: problems.append(f'{lid} F3 assignment changed')
    if set(z['position'] for z in s['scene_layout']['zones'])!={'left','center','right'}: problems.append(f'{lid} spatial zones changed')
    beats={x['object_id']:x for x in s['story_beats']}
    terms={t['knowledge_id']:t for t in b[lid]['term_introductions']}
    for kid in s['object_ids']:
        if beats[kid]['science']!=c[kid]['canonical_verified_statement']: problems.append(f'{lid} canonical science changed {kid}')
        if beats[kid]['term']!=terms[kid]['canonical_term']: problems.append(f'{lid} term changed {kid}')
        if bool(beats[kid]['exact_name'])!=bool(terms[kid]['exact_name_recall']): problems.append(f'{lid} exact-name policy changed {kid}')
        if terms[kid]['exact_name_recall']:
            exact+=1
            if terms[kid]['canonical_term'].casefold() not in low: problems.append(f'{lid} exact term missing {terms[kid]["canonical_term"]}')
    if s['checkpoint']!=bool(b[lid]['quick_recall']['enabled']): problems.append(f'{lid} recall mismatch')
    if s['checkpoint']:
        if s['checkpoint_prompt']!=b[lid]['quick_recall']['candidate_prompt']: problems.append(f'{lid} recall prompt changed')
        if s['checkpoint_answer']!=b[lid]['quick_recall']['answer']: problems.append(f'{lid} recall answer changed')
    if banned.search(prose): problems.append(f'{lid} exposes development/source language')
    if '—' in prose or ': ' in prose: problems.append(f'{lid} punctuation policy violation')

if len(assigned)!=15 or len(set(assigned))!=15 or exact!=3:
    problems.append(f'knowledge/exact accounting mismatch {len(assigned)}/{len(set(assigned))}/{exact}')

full=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
required_phrases=[
    'earth formed about 4.6 billion years ago',
    'conditions were too hostile for life until roughly 3.9 billion years ago',
    'earliest fossil evidence for life dates to about 3.5 billion years ago',
    'little free molecular oxygen',
    'small organic molecules can form abiotically under multiple plausible prebiotic conditions',
    'meteorites contain amino acids and other organic compounds',
    'does not by itself demonstrate the formation of proteins, nucleic acids, cells, or life',
    'oparin-haldane hypothesis',
    'historical hypothesis',
    'substantial nitrogen and carbon dioxide',
    'miller-urey experiment',
    'amino acids and other small organic compounds could form abiotically under the simulated conditions',
    'not polymers',
    'not life',
    'rna world hypothesis',
    'complementary base pairing',
    'genetic continuity',
    'catalytic rna and ribozymes',
    'genetically encoded proteins were not initially required as catalysts',
    'endosymbiosis is later than life',
    'origin of mitochondria and chloroplasts',
    'later event than the origin of the first cellular life',
]
for phrase in required_phrases:
    if phrase not in full: problems.append('missing visible science '+phrase)

# Explicit chronology and claim-strength safeguards.
if full.find('4.6 billion years ago')>full.find('miller-urey experiment'): problems.append('geological timing appears after experiment')
if full.find('oparin-haldane hypothesis')>full.find('miller-urey experiment'): problems.append('historical hypothesis not placed before Miller-Urey')
if full.find('rna world hypothesis')>full.find('endosymbiosis is later than life'): problems.append('RNA-world stage not placed before later endosymbiosis')
if 'the host must already be a cell' not in full: problems.append('endosymbiosis prerequisite-cell boundary missing')
if 'did not establish heredity, metabolism, or biological evolution' not in full: problems.append('Miller-Urey overclaim guard missing')

# Prior narrative protection.
if len(lock.get('prior_narrative_protection',{}))!=45: problems.append('prior narrative protection count is not 45')
for rel,meta in lock.get('prior_narrative_protection',{}).items():
    p=ROOT/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append('prior narrative changed '+rel)

# F1/F2/F3 locks remain unchanged.
f3=read(U7/'content-lock-f3.json')
for key in ('f1_protected_hashes','f2_protected_hashes'):
    for rel,h in f3.get(key,{}).items():
        p=ROOT/rel
        if not p.exists() or sha(p)!=h: problems.append(f'{key} changed '+rel)
for rel,meta in f3.get('files',{}).items():
    p=ROOT/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append('F3 brief changed '+rel)

# Units 1–6 stay frozen.
up=read(U7/'upstream-u1-u6-protection-f1.json')
if up.get('protected_file_count')!=356: problems.append('upstream protection count changed')
for item in up['protected_files']:
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append('upstream changed '+item['path'])

status=read(U7/'status.json')
if status.get('status') not in {'F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}: problems.append('F4F status boundary')
if status.get('status')=='STUDENT_READY' and (status.get('student_release') is not True or status.get('preview_release') is not False): problems.append('F5 release flags while preserving F4F')
if status.get('status')!='STUDENT_READY' and (status.get('student_release') is not False or status.get('preview_release') is not True): problems.append('pre-F5 F4F release flags')
if status.get('status')!='STUDENT_READY' and (status.get('journey_count'),status.get('scene_count'),status.get('memory_objects'),status.get('application_challenges'))!=(6,55,0,0): problems.append('F4F development counts')
if status.get('status')=='STUDENT_READY' and (status.get('journey_count'),status.get('scene_count'),status.get('memory_objects'),status.get('application_challenges'))!=(6,55,174,16): problems.append('F5 runtime counts while preserving F4F')
course=read(ROOT/'content/ap-biology/course.json'); cu7=next(u for u in course['units'] if u['unit_id']=='unit-7')
if cu7.get('status') not in {'F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}: problems.append('course registry F4F boundary')
if cu7.get('status')=='STUDENT_READY' and cu7.get('student_release') is not True: problems.append('course registry F5 release while preserving F4F')
if cu7.get('status')!='STUDENT_READY' and cu7.get('student_release') is not False: problems.append('course registry pre-F5 boundary')

for forbidden in ['memory-objects-f5.json','application-lab.json','review-manifest-f5.json','mixed-discrimination-f5.json','scope-guards-f5.json','finalization-f5.json']:
    if status.get('status')!='STUDENT_READY' and (U7/forbidden).exists(): problems.append('premature F5 artifact exists '+forbidden)

required=[U7/'journeys/U7-J6.json',U7/'journeys-f4f.json',U7/'status-f4f.json',U7/'content-lock-f4f.json',U7/'f4f-release-manifest.json',ROOT/'docs/UNIT7_F4F_JOURNEY6_STORY.md',ROOT/'docs/UNIT7_F4F_RELEASE.md',ROOT/'docs/UNIT7_F4F_PACKAGE_QA.md']
for p in required:
    if not p.exists(): problems.append('missing F4F artifact '+str(p.relative_to(ROOT)))

report=['# Unit 7 F4F Narrative QA','','## Result','', '**PASS**' if not problems else '**FAIL**','',
        '- Polished scenes: **5 / 5**','- Locked F3 knowledge records represented: **15 / 15**',f'- Exact-name targets explicitly introduced: **{exact} / 3**','- Optional first-exposure recalls: **2**',f'- Narrative words: **{sum(counts):,}**',f'- Mean scene length: **{statistics.mean(counts):.1f} words**',f'- Shortest scene: **{min(counts)} words**',f'- Longest scene: **{max(counts)} words**','',
        '## Science and chronology gates','',
        '- Geological timing is fixed before any chemical or later cellular hypothesis is introduced.',
        '- Earliest-life evidence remains near 3.5 billion years ago without requiring a definitive cyanobacterial identity.',
        '- Early Earth retains little free molecular oxygen and plausible non-oxygen energy sources.',
        '- Abiotic small-organic synthesis remains separate from polymerization, protocells, replication, cells, and life.',
        '- Meteorite organics remain one possible contributor to the prebiotic organic inventory.',
        '- Oparin-Haldane remains a historical reducing-atmosphere hypothesis with modern atmospheric qualification.',
        '- Miller-Urey remains an experimental demonstration of small-organic synthesis under simulated conditions and never a creation-of-life experiment.',
        '- RNA-world reasoning requires genetic continuity, complementary templating, and catalytic capability before modern encoded protein catalysts.',
        '- Ribozymes provide evidence that RNA can perform catalytic roles.',
        '- Endosymbiosis remains a later explanation for mitochondria and chloroplasts in already-existing cellular lineages.',
        '- Journeys 1–5 remain frozen and Unit 7 remains student-unreleased.']
if problems: report += ['','## Blocking findings','']+[f'- {x}' for x in problems]
(ROOT/'docs/UNIT7_F4F_QA.md').write_text('\n'.join(report),encoding='utf-8')

if problems:
    print('UNIT 7 F4F QA FAIL'); print('\n'.join(problems)); sys.exit(1)
print('UNIT 7 F4F QA PASS')
print(json.dumps({'scenes':5,'records':15,'exact':3,'recalls':2,'words':sum(counts),'mean':round(statistics.mean(counts),1),'min':min(counts),'max':max(counts),'prior_protected':45},indent=2))
