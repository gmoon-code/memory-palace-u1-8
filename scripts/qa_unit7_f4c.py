from __future__ import annotations
import json,re,hashlib,statistics,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content'/'ap-biology'/'unit-7'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

journey=read(U7/'journeys/U7-J3.json')
briefs={b['locus_id']:b for b in read(U7/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U7-J3'}
canon={r['knowledge_id']:r for r in read(U7/'source/canonical-unit7-f1.json')['canonical_catalog']}
lock=read(U7/'content-lock-f4c.json')
problems=[]
expected_loci=[f'U7-L{i:02d}' for i in range(25,34)]

if journey.get('palace_id')!='U7-J3': problems.append('Journey ID is not U7-J3')
if journey.get('scene_count')!=9 or len(journey.get('scenes',[]))!=9: problems.append('Journey 3 does not contain 9 scenes')
if journey.get('checkpoint_count')!=3: problems.append('Journey 3 checkpoint count is not 3')
if [s['locus_id'] for s in journey['scenes']]!=expected_loci: problems.append('Journey 3 route is not U7-L25..U7-L33 in order')
if journey.get('student_release')!='DEVELOPER_PREVIEW_F4C' or journey.get('preview_release') is not True: problems.append('Journey 3 release boundary invalid')

banned=re.compile(r'\b(PPT|CED|College Board|Campbell|source material|content lock|teacher enrichment|exam scope|LOCKED_F|developer preview|F1|F2|F3|F4)\b',re.I)
counts=[]; assigned=[]; exact_targets=0
for s in journey['scenes']:
    lid=s['locus_id']; b=briefs[lid]
    prose=' '.join(s['story_paragraphs']); low=prose.casefold().replace('**','')
    words=len(re.findall(r"\b[\w’′'-]+\b",prose)); counts.append(words); assigned+=s['object_ids']
    if words<450: problems.append(f'{lid} has only {words} narrative words')
    if len(s['story_paragraphs'])<6: problems.append(f'{lid} has fewer than 6 narrative paragraphs')
    opening=s['story_paragraphs'][0].casefold()
    if 'left' not in opening or 'right' not in opening or not ('ahead' in opening or 'center' in opening): problems.append(f'{lid} does not establish left/center/right geography before action')
    if len(s.get('cast',[]))<7: problems.append(f'{lid} cast is too thin')
    if not any(c['name']=='Dr. Imani Vale' for c in s['cast']): problems.append(f'{lid} guide missing')
    if not any(c['name']=='Expanding evidence dossier' for c in s['cast']): problems.append(f'{lid} evidence dossier missing')
    if not any(c['name']=='Observation column' for c in s['cast']): problems.append(f'{lid} observation column missing')
    if not any(c['name']=='Inference column' for c in s['cast']): problems.append(f'{lid} inference column missing')
    if s.get('continuity_object')!=journey['scenes'][0].get('continuity_object'): problems.append(f'{lid} continuity object changed')
    if s['object_ids']!=b['knowledge_ids']: problems.append(f'{lid} knowledge IDs changed from F3')
    if set(z['position'] for z in s['scene_layout']['zones'])!={'left','center','right'}: problems.append(f'{lid} spatial zones invalid')
    terms={t['knowledge_id']:t for t in b['term_introductions']}
    beats={x['object_id']:x for x in s['story_beats']}
    if set(beats)!=set(s['object_ids']): problems.append(f'{lid} story beat coverage mismatch')
    for kid in s['object_ids']:
        t=terms[kid]; beat=beats[kid]
        if beat.get('science')!=canon[kid]['canonical_verified_statement']: problems.append(f'{lid} canonical science changed in beat {kid}')
        if beat.get('term')!=t['canonical_term']: problems.append(f'{lid} canonical term changed in beat {kid}')
        if bool(beat.get('exact_name'))!=bool(t['exact_name_recall']): problems.append(f'{lid} exact-name policy changed {kid}')
        if t['exact_name_recall']:
            exact_targets+=1
            if t['canonical_term'].casefold() not in low: problems.append(f'{lid} exact target absent from prose: {t["canonical_term"]}')
    if banned.search(prose): problems.append(f'{lid} exposes development/source-management language: {banned.search(prose).group(0)}')
    if '—' in prose: problems.append(f'{lid} contains prohibited em dash')
    if ': ' in prose: problems.append(f'{lid} contains colon punctuation in narrative prose')
    if s.get('checkpoint') != bool(b['quick_recall']['enabled']): problems.append(f'{lid} checkpoint status changed from F3')
    if s.get('checkpoint'):
        if s.get('checkpoint_prompt')!=b['quick_recall']['candidate_prompt']: problems.append(f'{lid} checkpoint prompt changed')
        if s.get('checkpoint_answer')!=b['quick_recall']['answer']: problems.append(f'{lid} checkpoint answer changed')
    idx=expected_loci.index(lid)
    expected_next=journey['scenes'][idx+1]['locus'] if idx<len(expected_loci)-1 else None
    if s.get('next_locus')!=expected_next: problems.append(f'{lid} next-locus continuity broken')
    if idx<len(expected_loci)-1 and len(s['story_paragraphs'][-1])<180: problems.append(f'{lid} transition paragraph too thin')

if len(assigned)!=35 or len(set(assigned))!=35: problems.append(f'Journey 3 knowledge coverage is {len(assigned)} refs / {len(set(assigned))} unique, expected 35/35')
if exact_targets!=11: problems.append(f'Journey 3 exact-name target count is {exact_targets}, expected 11')

full=' '.join(' '.join(s['story_paragraphs']) for s in journey['scenes']).casefold().replace('**','')
visible={
 'evidence_specificity':['different evidence types answer different evolutionary questions','independent lines point toward the same history','converging geographical, geological, physical, biochemical, and mathematical evidence'],
 'fossil_and_record':['a fossil is preserved evidence of a past organism','fossil record documents changes in organisms through geologic time','incomplete and biased toward conditions favorable to fossilization'],
 'dating':['radiometric dating estimates ages from predictable radioactive decay','isotope choice must match the age range','carbon-14 has a short geologic half-life'],
 'homology':['homology is similarity caused by shared ancestry','homologous structures share an underlying inherited structural pattern','even when they perform different functions'],
 'vestigial':['vestigial does not mean that every present-day role has disappeared','may retain reduced or modified functions'],
 'analogy':['analogous structures perform similar functions or have similar forms because of independent evolution','bird and bat forelimbs share homologous skeletal elements'],
 'molecular':['comparisons of dna nucleotide sequences and protein amino-acid sequences provide evidence for evolution and common ancestry','molecular homology','does not automatically provide a precise time since divergence'],
 'eukaryotic':['membrane-bound organelles','linear chromosomes','introns','common ancestry among eukaryotes'],
 'continuing_evolution':['populations continue to evolve when evolutionary mechanisms change allele frequencies','bacteria do not decide to become resistant','generation labels visible'],
 'diversity':['low diversity increases vulnerability','more likely to include individuals whose phenotypes tolerate a novel environmental pressure','fitness effects depend on environment','california condor genetic bottleneck'],
}
for name,phrases in visible.items():
    if not all(p in full for p in phrases): problems.append(f'high-risk science guard not visibly satisfied: {name}')

# Protect Journeys 1 and 2 plus F4A/F4B evidence.
for rel,meta in lock.get('f4a_f4b_prior_narrative_protection',{}).items():
    p=ROOT/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'prior narrative artifact changed: {rel}')

# F1/F2/F3 protected science and architecture remain unchanged.
f3=read(U7/'content-lock-f3.json')
for key in ('f1_protected_hashes','f2_protected_hashes'):
    for rel,h in f3.get(key,{}).items():
        p=ROOT/rel
        if not p.exists() or sha(p)!=h: problems.append(f'{key} changed: {rel}')
for rel,meta in f3.get('files',{}).items():
    p=ROOT/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F3 locked brief artifact changed: {rel}')

# Units 1–6 remain byte-identical.
up=read(U7/'upstream-u1-u6-protection-f1.json')
if up.get('baseline_package_sha256')!='ba5ca238d579d7fa733bd6b17613d85dc7685893152ff4bc574ee65a0b7b508a': problems.append('wrong Units 1–6 baseline checksum')
if up.get('protected_file_count')!=356: problems.append('Units 1–6 protection manifest count changed')
for item in up['protected_files']:
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f'protected Units 1–6 file changed: {item["path"]}')

if lock.get('lock_status')!='LOCKED_F4C_J1_J3' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4C content-lock boundary invalid')
for rel,meta in lock.get('files',{}).items():
    p=U7/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4C locked file mismatch: {rel}')

for forbidden in ['memory-objects-f5.json','application-lab.json','review-manifest-f5.json','mixed-discrimination-f5.json','scope-guards-f5.json','finalization-f5.json']:
    if read(U7/'status.json').get('status')!='STUDENT_READY' and (U7/forbidden).exists(): problems.append(f'premature Unit 7 final runtime artifact exists: {forbidden}')

required=[
    U7/'journeys/U7-J3.json',U7/'journeys-f4c.json',U7/'status-f4c.json',U7/'content-lock-f4c.json',U7/'f4c-release-manifest.json',
    ROOT/'docs/UNIT7_F4C_JOURNEY3_STORY.md',ROOT/'docs/UNIT7_F4C_RELEASE.md',ROOT/'docs/UNIT7_F4C_PACKAGE_QA.md'
]
for p in required:
    if not p.exists(): problems.append(f'missing F4C artifact: {p.relative_to(ROOT)}')

status=read(U7/'status.json')
allowed_status={'F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
if status.get('status') not in allowed_status: problems.append('Unit 7 F4C-or-later status boundary invalid')
if status.get('status')=='STUDENT_READY' and (status.get('student_release') is not True or status.get('preview_release') is not False): problems.append('Unit 7 F5 release flags invalid while preserving F4C')
if status.get('status')!='STUDENT_READY' and (status.get('student_release') is not False or status.get('preview_release') is not True): problems.append('Unit 7 pre-F5 status flags invalid while preserving F4C')
if status.get('status')=='F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW' and (status.get('journey_count'),status.get('scene_count'),status.get('memory_objects'),status.get('application_challenges'))!=(3,33,0,0): problems.append('Unit 7 F4C runtime-development counts invalid')
if status.get('status')=='F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW' and (status.get('journey_count'),status.get('scene_count'),status.get('memory_objects'),status.get('application_challenges'))!=(4,41,0,0): problems.append('Unit 7 F4D runtime-development counts invalid while preserving F4C')
if status.get('status')=='F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW' and (status.get('journey_count'),status.get('scene_count'),status.get('memory_objects'),status.get('application_challenges'))!=(6,55,0,0): problems.append('Unit 7 F4F runtime-development counts invalid while preserving F4C')
course=read(ROOT/'content/ap-biology/course.json'); cu7=next(u for u in course['units'] if u['unit_id']=='unit-7')
if cu7.get('status') not in allowed_status: problems.append('course registry Unit 7 F4C-or-later boundary invalid')
if cu7.get('status')=='STUDENT_READY' and (cu7.get('student_release') is not True or cu7.get('preview_release') is not False): problems.append('course registry Unit 7 F5 release invalid while preserving F4C')
if cu7.get('status')!='STUDENT_READY' and (cu7.get('student_release') is not False or cu7.get('preview_release') is not True): problems.append('course registry Unit 7 pre-F5 release invalid while preserving F4C')

report=['# Unit 7 F4C Narrative QA','', '## Result','', '**PASS**' if not problems else '**FAIL**','',
'## Journey 3 accounting','', '- Polished scenes: **9 / 9**', '- Locked F3 knowledge records represented: **35 / 35**', f'- Exact-name targets explicitly introduced: **{exact_targets} / 11**', '- Optional first-exposure recalls: **3**', f'- Narrative words: **{sum(counts)}**', f'- Mean scene length: **{statistics.mean(counts):.1f} words**', f'- Shortest scene: **{min(counts)} words**', f'- Longest scene: **{max(counts)} words**','',
'## Prose and science gates','',
'- Every scene fixes left / center / right geography before evidence is interpreted.',
'- Dr. Imani Vale and the same six-tab evidence dossier remain physically identifiable across all nine locations.',
'- Every dossier card separates observation from inference so evidence is never treated as a vocabulary list.',
'- Geological age evidence remains distinct from common-ancestry evidence.',
'- Fossil, fossil record, radiometric dating, and carbon-14 limits remain scientifically distinct.',
'- Homology, homologous structures, vestigial evidence, embryological homology, and analogy remain diagnostically distinct.',
'- Vestigial structures are never reduced to a functionless definition.',
'- Bird and bat flight preserves independently evolved flight while retaining homologous tetrapod forelimb ancestry.',
'- DNA and protein comparisons require homologous sequence alignment and do not generate an exact divergence date by themselves.',
'- Conserved eukaryotic features are reactivated from earlier units without creating duplicate scientific identities.',
'- Contemporary resistance and pathogen examples remain population-level evolution across generations and never intentional adaptation.',
'- Genetic diversity changes the probability of tolerant variants and does not make every variant beneficial.',
'- Fitness effects remain environment dependent.',
'- Student prose contains no development/source-management language, em dashes, or colon punctuation.',
'- Journeys 1 and 2 remain byte-frozen and Unit 7 remains a developer preview with zero final Memory Objects or live Challenge Lab tasks.','']
if problems: report += ['## Blocking findings','']+[f'- {p}' for p in problems]+['']

if status.get('status')!='STUDENT_READY': (ROOT/'docs'/'UNIT7_F4C_QA.md').write_text('\n'.join(report),encoding='utf-8')

if problems:
    print('UNIT 7 F4C QA FAIL')
    print('\n'.join(f'- {p}' for p in problems))
    sys.exit(1)
print('UNIT 7 F4C QA PASS')
print(json.dumps({'journey':'U7-J3','scenes':9,'knowledge_records':35,'exact_name_targets':exact_targets,'optional_recalls':3,'story_words':sum(counts),'average_scene_words':round(statistics.mean(counts),1),'min_scene_words':min(counts),'max_scene_words':max(counts),'journeys1_2_frozen':True,'student_release':False,'preview_release':True},indent=2))
