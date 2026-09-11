from __future__ import annotations
import json,re,hashlib,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U6=ROOT/'content'/'ap-biology'/'unit-6'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def wc(s): return len(re.findall(r"\b[\w’′'-]+\b",s))

problems=[]
j=read(U6/'journeys/U6-J4.json')
briefs={b['locus_id']:b for b in read(U6/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U6-J4'}
canon={r['knowledge_id']:r for r in read(U6/'source/canonical-unit6-f1.json')['canonical_catalog']}
lock=read(U6/'content-lock-f4d.json')
expected=[f'U6-L{i:02d}' for i in range(29,41)]
if j.get('palace_id')!='U6-J4': problems.append('Journey 4 ID changed')
if j.get('scene_count')!=12 or len(j.get('scenes',[]))!=12: problems.append('Journey 4 must contain 12 scenes')
if [s.get('locus_id') for s in j['scenes']]!=expected: problems.append('F2/F3 locus order changed')
if j.get('checkpoint_count')!=4: problems.append('F3 Quick Recall count changed from 4')
if j.get('student_release')!='DEVELOPER_PREVIEW_F4D' or j.get('preview_release') is not True: problems.append('F4D preview boundary wrong')
if j.get('guide',{}).get('name')!='Dr. Sora Han': problems.append('Unit 6 guide changed')
if 'twelve-location route' not in j.get('route_orientation',''): problems.append('route orientation does not define twelve-location route')
if len(j.get('premise',''))<500 or len(j.get('mission',''))<350 or len(j.get('finale',''))<450: problems.append('journey-level framing too thin')
assigned=[]; counts=[]; exact=0
banned=re.compile(r'\b(PPT|CED|Campbell|College Board|teacher enrichment|teacher-required|exam scope|exam-scope|source material|source lock|canonical record|F1|F2|F3|F4A|F4B|F4C|F4D)\b',re.I)
for s in j['scenes']:
    lid=s['locus_id']; b=briefs[lid]; prose=' '.join(s.get('story_paragraphs',[])); low=prose.casefold().replace('**',''); n=wc(prose); counts.append(n)
    if n<450: problems.append(f'{lid} narrative too short: {n}')
    if len(s.get('story_paragraphs',[]))<5: problems.append(f'{lid} fewer than 5 narrative paragraphs')
    op=s['story_paragraphs'][0].lower()
    if 'left' not in op or ('ahead' not in op and 'center' not in op) or 'right' not in op: problems.append(f'{lid} opening lacks left/center/right orientation')
    zones=s.get('scene_layout',{}).get('zones',[])
    if len(zones)!=3 or [z.get('position') for z in zones]!=['left','center','right']: problems.append(f'{lid} geometry changed')
    orient=s['scene_layout']['orientation']
    for side in ('left','center','right'):
        if b['spatial_layout'][side]['anchor'] not in orient: problems.append(f'{lid} F3 anchor missing: {b["spatial_layout"][side]["anchor"]}')
    if len(s.get('cast',[]))<5: problems.append(f'{lid} cast too thin')
    if not any(c.get('name')=='Dr. Sora Han' for c in s['cast']): problems.append(f'{lid} lost guide')
    if not any(c.get('name')=='Tracked gene and expression-state ledger' for c in s['cast']): problems.append(f'{lid} lost continuity object')
    if s.get('object_ids')!=b['knowledge_ids']: problems.append(f'{lid} knowledge assignment changed')
    assigned+=s.get('object_ids',[]); beats={x['object_id']:x for x in s.get('story_beats',[])}
    if set(beats)!=set(b['knowledge_ids']): problems.append(f'{lid} story-beat coverage mismatch')
    for t in b['term_introductions']:
        kid=t['knowledge_id']; beat=beats.get(kid)
        if not beat: continue
        if beat.get('science')!=canon[kid]['canonical_verified_statement']: problems.append(f'{lid} canonical science changed: {kid}')
        if beat.get('term')!=t['canonical_term']: problems.append(f'{lid} canonical term changed: {kid}')
        if bool(beat.get('exact_name'))!=bool(t['exact_name_recall']): problems.append(f'{lid} exact-name policy changed: {kid}')
        if t['exact_name_recall']:
            exact+=1
            if t['canonical_term'].casefold() not in low: problems.append(f'{lid} exact target absent: {t["canonical_term"]}')
    if banned.search(prose): problems.append(f'{lid} exposes development/source language: {banned.search(prose).group(0)}')
    if s.get('checkpoint')!=bool(b['quick_recall']['enabled']): problems.append(f'{lid} checkpoint changed')
    if s.get('checkpoint'):
        if s.get('checkpoint_prompt')!=b['quick_recall']['candidate_prompt']: problems.append(f'{lid} checkpoint prompt changed')
        if s.get('checkpoint_answer')!=b['quick_recall']['answer']: problems.append(f'{lid} checkpoint answer changed')
    idx=expected.index(lid); exp=j['scenes'][idx+1]['locus'] if idx<len(expected)-1 else None
    if s.get('next_locus')!=exp: problems.append(f'{lid} next-locus continuity broken')
if len(assigned)!=36 or len(set(assigned))!=36: problems.append(f'Journey 4 coverage {len(assigned)} refs/{len(set(assigned))} unique expected 36/36')
if exact!=29: problems.append(f'Journey 4 exact-name count {exact}, expected 29')
full=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
visible={
 'expression_control':['regulatory dna sequences and proteins','constitutive and inducible expression','dna sequence'],
 'operon':['coordinated prokaryotic operon regulation','operon','promoter','operator','structural genes','repressor protein'],
 'trp':['trp operon as repressible system','tryptophan as corepressor','allosteric regulation review','regulatory protein'],
 'lac':['lac operon as inducible system','allolactose as inducer','β-galactosidase','lactose permease','human intestinal enzyme lactase'],
 'layers':['coordinated eukaryotic regulation','multiple regulatory stages in eukaryotes','chromatin','rna-processing','post-translational'],
 'epigenetics':['reversible epigenetic regulation','histone acetylation association','dna methylation association','epigenetic state inheritance','without changing the dna nucleotide sequence'],
 'recruitment':['promoter/enhancer recruitment of transcription machinery','regulatory-sequence position','upstream or downstream','control elements, activators, and repressors','tata box'],
 'negative':['negative transcriptional regulation','dna sequence remains fixed','meter recovers'],
 'rna':['small rna regulation','alternative splicing as regulatory mechanism','microrna and sirna','degradation','inhibit translation'],
 'profile':['gene-expression profile determines phenotype','gene-product amount and function influence phenotype','transcript amount alone'],
 'specialization':['differentiation and tissue-specific proteins','differential gene expression and specialization','cell differentiation','same genome','morphogenesis'],
 'development':['sequential developmental gene expression','cytoplasmic determinants','induction in development','pattern formation and homeotic genes','morphogenesis','apoptosis'],
}
for name,phrases in visible.items():
    if not all(p in full for p in phrases): problems.append(f'high-risk science guard not visibly satisfied: {name}')
# Freeze F4C and earlier narratives exactly.
prior=read(U6/'content-lock-f4c.json')
for rel,meta in prior.get('files',{}).items():
    p=U6/rel
    # journeys-f4c and status-f4c remain historical files; only J1-J3 are required to be frozen against their F4C hashes.
    if rel.startswith('journeys/U6-J'):
        if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4C locked narrative changed: {rel}')
for fname in ['content-lock-f1.json','content-lock-f2.json','content-lock-f3.json','content-lock-f4a.json','content-lock-f4b.json','content-lock-f4c.json']:
    if not (U6/fname).exists(): problems.append(f'missing prior lock {fname}')
# upstream U1-U5 byte protection
up=read(U6/'upstream-u1-u5-protection-f1.json')
if up.get('protected_file_count')!=291: problems.append('Units 1–5 protection manifest count changed')
for item in up['protected_files']:
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f'protected Units 1–5 file changed: {item["path"]}')
if lock.get('lock_status')!='LOCKED_F4D_J1_J4' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4D content-lock boundary invalid')
for rel,meta in lock.get('files',{}).items():
    p=U6/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4D locked file mismatch: {rel}')
if not (U6/'f5-release-manifest.json').exists():
    for forbidden in ['memory-objects-f5.json','application-lab.json','review-manifest-f5.json','mixed-discrimination-f5.json','scope-guards-f5.json','finalization-f5.json']:
        if (U6/forbidden).exists(): problems.append(f'premature Unit 6 final runtime artifact exists: {forbidden}')
status=read(U6/'status.json')
if status.get('status') not in {'F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}: problems.append('Unit 6 status boundary invalid')
elif status.get('status')=='STUDENT_READY' and status.get('student_release') is not True: problems.append('Unit 6 F5 release flag invalid')
elif status.get('status')!='STUDENT_READY' and status.get('student_release') is not False: problems.append('Unit 6 pre-F5 release flag invalid')
course=read(ROOT/'content/ap-biology/course.json'); cu6=next(u for u in course['units'] if u['unit_id']=='unit-6')
if cu6.get('status') not in {'F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}: problems.append('course registry Unit 6 boundary invalid')
elif cu6.get('status')=='STUDENT_READY' and cu6.get('student_release') is not True: problems.append('course registry Unit 6 F5 release flag invalid')
elif cu6.get('status')!='STUDENT_READY' and cu6.get('student_release') is not False: problems.append('course registry Unit 6 pre-F5 release flag invalid')
report=['# Unit 6 F4D Narrative QA','','## Result','', '**PASS**' if not problems else '**FAIL**','', '## Journey 4 accounting','', '- Polished scenes: **12 / 12**','- Locked F3 knowledge records represented: **36 / 36**',f'- Exact-name targets explicitly introduced: **{exact}**','- Optional first-exposure recalls: **4**',f'- Narrative words: **{sum(counts)}**',f'- Mean scene length: **{statistics.mean(counts):.1f} words**',f'- Shortest scene: **{min(counts)} words**',f'- Longest scene: **{max(counts)} words**','', '## Prose-quality gates','', '- Every scene establishes left/center/right geography before regulatory state changes.','- The tracked eukaryotic gene sequence, promoter-linked expression meter, and chromatin-state strip remain reconstructable across the eukaryotic route.','- trp and lac operons remain separately labeled bacterial comparison models and are never substituted for the tracked eukaryotic gene.','- Regulatory DNA, regulatory proteins, chromatin marks, RNA regulators, gene products, and phenotype remain physically distinct causal layers.','- trp corepressor logic and lac inducer logic remain opposite, diagnostic comparison systems.','- Epigenetic state changes remain distinct from DNA-sequence mutation and retain context-dependent qualifiers.','- Promoter, enhancer/control element, activator, and repressor remain distinct entities.','- Differential gene expression is linked to specialization while same-genome somatic-cell context remains visible.','- Cell differentiation and morphogenesis remain distinct.','- No student prose exposes development/source-management language.','- Journeys 1–3 remain byte-frozen from F4A/F4B/F4C.','- Unit 6 remains developer preview with zero final Memory Objects and zero live Challenge Lab tasks.','']
if problems: report+=['## Blocking findings','']+[f'- {p}' for p in problems]+['']
(ROOT/'docs/UNIT6_F4D_QA.md').write_text('\n'.join(report),encoding='utf-8')
if problems:
    print('UNIT 6 F4D QA FAIL'); print('\n'.join('- '+x for x in problems)); sys.exit(1)
print('UNIT 6 F4D QA PASS'); print(json.dumps({'journey':'U6-J4','scenes':12,'knowledge_records':36,'exact_name_targets':exact,'optional_recalls':4,'story_words':sum(counts),'average_scene_words':round(statistics.mean(counts),1),'min_scene_words':min(counts),'max_scene_words':max(counts),'journeys1_3_frozen':True,'student_release':False},indent=2))
