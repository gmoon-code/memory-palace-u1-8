from __future__ import annotations
import json,re,hashlib,statistics,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content'/'ap-biology'/'unit-7'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

journey=read(U7/'journeys/U7-J2.json')
j1=read(U7/'journeys/U7-J1.json')
briefs={b['locus_id']:b for b in read(U7/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U7-J2'}
canon={r['knowledge_id']:r for r in read(U7/'source/canonical-unit7-f1.json')['canonical_catalog']}
lock=read(U7/'content-lock-f4b.json')
problems=[]
expected_loci=[f'U7-L{i:02d}' for i in range(11,25)]

if journey.get('palace_id')!='U7-J2': problems.append('Journey ID is not U7-J2')
if journey.get('scene_count')!=14 or len(journey.get('scenes',[]))!=14: problems.append('Journey 2 does not contain 14 scenes')
if journey.get('checkpoint_count')!=4: problems.append('Journey 2 checkpoint count is not 4')
if [s['locus_id'] for s in journey['scenes']]!=expected_loci: problems.append('Journey 2 route is not U7-L11..U7-L24 in order')
if journey.get('student_release')!='DEVELOPER_PREVIEW_F4B' or journey.get('preview_release') is not True: problems.append('Journey 2 release boundary invalid')

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
    if not any(c['name']=='Island A gene-pool tank' for c in s['cast']): problems.append(f'{lid} Island A tank missing')
    if not any(c['name']=='Island B gene-pool tank' for c in s['cast']): problems.append(f'{lid} Island B tank missing')
    if not any(c['name']=='Transparent population ledger' for c in s['cast']): problems.append(f'{lid} population ledger missing')
    if s.get('continuity_object')!=journey.get('scenes',[{}])[0].get('continuity_object'): problems.append(f'{lid} continuity object changed')
    if s['object_ids']!=b['knowledge_ids']: problems.append(f'{lid} knowledge IDs changed from F3')
    if set(s['scene_layout']['zones'][i]['position'] for i in range(3))!={'left','center','right'}: problems.append(f'{lid} spatial zones invalid')
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

if len(assigned)!=47 or len(set(assigned))!=47: problems.append(f'Journey 2 knowledge coverage is {len(assigned)} refs / {len(set(assigned))} unique, expected 47/47')
if exact_targets!=21: problems.append(f'Journey 2 exact-name target count is {exact_targets}, expected 21')

full=' '.join(' '.join(s['story_paragraphs']) for s in journey['scenes']).casefold().replace('**','')
visible={
 'population_gene_pool':['a population is a group of individuals of the same species','gene pool consists of all alleles','frequency is 1.0'],
 'microevolution':['microevolution is change in allele frequencies within a population across generations','mechanism unknown'],
 'mutation_before_selection':['copying event is random with respect to whether the resulting variant will improve fitness','mutation is the ultimate source of new alleles','selection can later change the frequency'],
 'random_not_selection':['selection is nonrandom differential reproductive success','apparatus does not ask which allele would improve'],
 'drift':['genetic drift is a nonselective change in allele frequency caused by chance','drift is strongest in small populations','drift is nonadaptive'],
 'bottleneck':['bottleneck is genetic drift following a severe population-size reduction','chance, nonrepresentative sample','demographic reduction'],
 'founder':['founder effect is genetic drift when a new population is established by a small subset','source population on the left remains nearly unchanged','not that the founders had an unusually high number of new mutations'],
 'gene_flow':['migration of fertile individuals or gametes can add or remove alleles','gene flow between populations tends to reduce genetic differences','transparent bridge'],
 'hwe_null':['hardy-weinberg equilibrium as null model','at a locus','baseline against which observed genotype and allele data can be compared'],
 'five_conditions':['hardy-weinberg condition large population','hardy-weinberg condition no migration','hardy-weinberg condition no mutation','hardy-weinberg condition random mating','hardy-weinberg condition no natural selection'],
 'nonrandom_mating':['nonrandom mating by itself can change genotype frequencies without changing allele frequencies'],
 'pq_not_dominance':['not inherently the dominant allele','not inherently recessive','p + q = 1'],
 'expected_not_observed':['expected genotype frequencies are p² + 2pq + q² = 1','they were not counted directly from the fifty individuals'],
 'direct_count':['divide by the total number of allele copies','2n allele copies','square root of an arbitrary observed aa frequency'],
 'conditional_q2':['phenotype is caused only by the aa genotype','hardy-weinberg assumptions are not justified','frequency of that recessive phenotype can be treated as q²'],
}
for name,phrases in visible.items():
    if not all(p in full for p in phrases): problems.append(f'high-risk science guard not visibly satisfied: {name}')

# F4A Journey 1 and its release evidence remain frozen.
for rel,meta in lock.get('f4a_journey1_protection',{}).items():
    p=ROOT/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4A protected artifact changed: {rel}')
if j1.get('story_title')!='The Observatory That Mistook Change for Evolution' or j1.get('scene_count')!=10: problems.append('Journey 1 identity changed')

# F1/F2/F3 protected science and architecture remain unchanged.
f3=read(U7/'content-lock-f3.json')
for key in ('f1_protected_hashes','f2_protected_hashes'):
    for rel,h in f3.get(key,{}).items():
        p=ROOT/rel
        if not p.exists() or sha(p)!=h: problems.append(f'{key} changed: {rel}')
for rel,meta in f3.get('files',{}).items():
    p=ROOT/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F3 locked brief artifact changed: {rel}')

# Units 1–6 remain byte-identical to the Unit 6 F6 baseline.
up=read(U7/'upstream-u1-u6-protection-f1.json')
if up.get('baseline_package_sha256')!='ba5ca238d579d7fa733bd6b17613d85dc7685893152ff4bc574ee65a0b7b508a': problems.append('wrong Units 1–6 baseline checksum')
if up.get('protected_file_count')!=356: problems.append('Units 1–6 protection manifest count changed')
for item in up['protected_files']:
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f'protected Units 1–6 file changed: {item["path"]}')

if lock.get('lock_status')!='LOCKED_F4B_J1_J2' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4B content-lock boundary invalid')
for rel,meta in lock.get('files',{}).items():
    p=U7/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4B locked file mismatch: {rel}')

for forbidden in ['memory-objects-f5.json','application-lab.json','review-manifest-f5.json','mixed-discrimination-f5.json','scope-guards-f5.json','finalization-f5.json']:
    if read(U7/'status.json').get('status')!='STUDENT_READY' and (U7/forbidden).exists(): problems.append(f'premature Unit 7 final runtime artifact exists: {forbidden}')

required=[
    U7/'journeys/U7-J2.json',U7/'journeys-f4b.json',U7/'status-f4b.json',U7/'content-lock-f4b.json',U7/'f4b-release-manifest.json',
    ROOT/'docs/UNIT7_F4B_JOURNEY2_STORY.md',ROOT/'docs/UNIT7_F4B_RELEASE.md',ROOT/'docs/UNIT7_F4B_PACKAGE_QA.md'
]
for p in required:
    if not p.exists(): problems.append(f'missing F4B artifact: {p.relative_to(ROOT)}')

status=read(U7/'status.json')
allowed_status={'F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
if status.get('status') not in allowed_status: problems.append('Unit 7 F4B-or-later status boundary invalid')
if status.get('status')=='STUDENT_READY' and (status.get('student_release') is not True or status.get('preview_release') is not False): problems.append('Unit 7 F5 release flags invalid while preserving F4B')
if status.get('status')!='STUDENT_READY' and (status.get('student_release') is not False or status.get('preview_release') is not True): problems.append('Unit 7 pre-F5 status flags invalid while preserving F4B')
if status.get('status')=='F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW' and (status.get('journey_count'),status.get('scene_count'),status.get('memory_objects'),status.get('application_challenges'))!=(2,24,0,0): problems.append('Unit 7 F4B runtime-development counts invalid')
if status.get('status')=='F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW' and (status.get('journey_count'),status.get('scene_count'),status.get('memory_objects'),status.get('application_challenges'))!=(3,33,0,0): problems.append('Unit 7 F4C runtime-development counts invalid while preserving F4B')
if status.get('status')=='F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW' and (status.get('journey_count'),status.get('scene_count'),status.get('memory_objects'),status.get('application_challenges'))!=(4,41,0,0): problems.append('Unit 7 F4D runtime-development counts invalid while preserving F4B')
if status.get('status')=='F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW' and (status.get('journey_count'),status.get('scene_count'),status.get('memory_objects'),status.get('application_challenges'))!=(6,55,0,0): problems.append('Unit 7 F4F runtime-development counts invalid while preserving F4B')
course=read(ROOT/'content/ap-biology/course.json'); cu7=next(u for u in course['units'] if u['unit_id']=='unit-7')
if cu7.get('status') not in allowed_status: problems.append('course registry Unit 7 F4B-or-later boundary invalid')
if cu7.get('status')=='STUDENT_READY' and (cu7.get('student_release') is not True or cu7.get('preview_release') is not False): problems.append('course registry Unit 7 F5 release invalid while preserving F4B')
if cu7.get('status')!='STUDENT_READY' and (cu7.get('student_release') is not False or cu7.get('preview_release') is not True): problems.append('course registry Unit 7 pre-F5 release invalid while preserving F4B')

report=['# Unit 7 F4B Narrative QA','', '## Result','', '**PASS**' if not problems else '**FAIL**','',
'## Journey 2 accounting','', '- Polished scenes: **14 / 14**', '- Locked F3 knowledge records represented: **47 / 47**', f'- Exact-name targets explicitly introduced: **{exact_targets} / 21**', '- Optional first-exposure recalls: **4**', f'- Narrative words: **{sum(counts)}**', f'- Mean scene length: **{statistics.mean(counts):.1f} words**', f'- Shortest scene: **{min(counts)} words**', f'- Longest scene: **{max(counts)} words**','',
'## Prose and science gates','',
'- Every scene fixes left / center / right geography before population counts or model quantities change.',
'- Dr. Imani Vale, Island A, Island B, and the transparent population ledger remain physically identifiable across all fourteen locations.',
'- The focal blue/amber two-allele locus remains distinct from the separate mutation demonstration so Hardy-Weinberg remains a valid two-allele conceptual model downstream.',
'- Mutation, random sampling, genetic drift, bottleneck effect, founder effect, gene flow, and natural selection remain diagnostically distinct.',
'- Bottleneck and founder events are chance-sampling mechanisms and are never presented as automatically adaptive.',
'- Gene flow requires visible movement across a population boundary and is shown tending to reduce divergence between initially different populations.',
'- Hardy-Weinberg remains a locus-specific null model rather than a claim that real populations must match the expected values.',
'- The five Hardy-Weinberg conditions remain spatially distinct, including the nonrandom-mating qualification.',
'- p and q remain allele-frequency labels with no inherent dominance meaning.',
'- p², 2pq, and q² remain expected genotype frequencies under Hardy-Weinberg assumptions and never overwrite direct observed counts.',
'- Direct allele frequency from genotype counts uses allele-copy counting across 2N and explicitly blocks an unjustified square-root shortcut.',
'- Recessive-phenotype inference as q² remains conditional on phenotype-genotype mapping and Hardy-Weinberg assumptions.',
'- Student prose contains no development/source-management language, em dashes, or colon punctuation.',
'- Journey 1 remains byte-frozen and Unit 7 remains a developer preview with zero final Memory Objects or live Challenge Lab tasks.','']
if problems: report += ['## Blocking findings','']+[f'- {p}' for p in problems]+['']

if status.get('status')!='STUDENT_READY': (ROOT/'docs'/'UNIT7_F4B_QA.md').write_text('\n'.join(report),encoding='utf-8')

if problems:
    print('UNIT 7 F4B QA FAIL')
    print('\n'.join(f'- {p}' for p in problems))
    sys.exit(1)
print('UNIT 7 F4B QA PASS')
print(json.dumps({'journey':'U7-J2','scenes':14,'knowledge_records':47,'exact_name_targets':exact_targets,'optional_recalls':4,'story_words':sum(counts),'average_scene_words':round(statistics.mean(counts),1),'min_scene_words':min(counts),'max_scene_words':max(counts),'journey1_frozen':True,'student_release':False,'preview_release':True},indent=2))
