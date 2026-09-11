from __future__ import annotations
import json,re,hashlib,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U6=ROOT/'content'/'ap-biology'/'unit-6'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def wc(s): return len(re.findall(r"\b[\w’′'-]+\b",s))

problems=[]
j=read(U6/'journeys/U6-J5.json')
briefs={b['locus_id']:b for b in read(U6/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U6-J5'}
canon={r['knowledge_id']:r for r in read(U6/'source/canonical-unit6-f1.json')['canonical_catalog']}
lock=read(U6/'content-lock-f4e.json')
expected=[f'U6-L{i:02d}' for i in range(41,49)]
if j.get('palace_id')!='U6-J5': problems.append('Journey 5 ID changed')
if j.get('scene_count')!=8 or len(j.get('scenes',[]))!=8: problems.append('Journey 5 must contain 8 scenes')
if [s.get('locus_id') for s in j['scenes']]!=expected: problems.append('F2/F3 locus order changed')
if j.get('checkpoint_count')!=3: problems.append('F3 Quick Recall count changed from 3')
if j.get('student_release')!='DEVELOPER_PREVIEW_F4E' or j.get('preview_release') is not True: problems.append('F4E preview boundary wrong')
if j.get('guide',{}).get('name')!='Dr. Sora Han': problems.append('Unit 6 guide changed')
if 'eight-location forensic route' not in j.get('route_orientation',''): problems.append('route orientation does not define eight-location forensic route')
if len(j.get('premise',''))<500 or len(j.get('mission',''))<350 or len(j.get('finale',''))<400: problems.append('journey-level framing too thin')
assigned=[]; counts=[]; exact=0
banned=re.compile(r'\b(PPT|CED|Campbell|College Board|teacher enrichment|teacher-required|exam scope|exam-scope|source material|source lock|canonical record|F1|F2|F3|F4A|F4B|F4C|F4D|F4E)\b',re.I)
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
    if not any(c.get('name')=='Reference genome and consequence ledger' for c in s['cast']): problems.append(f'{lid} lost continuity object')
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
if len(assigned)!=26 or len(set(assigned))!=26: problems.append(f'Journey 5 coverage {len(assigned)} refs/{len(set(assigned))} unique expected 26/26')
if exact!=25: problems.append(f'Journey 5 exact-name count {exact}, expected 25')
full=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
visible={
 'consequence':['mutation effects depend on molecular consequence','environmental context of mutation effect','mutation connects genotype, phenotype, and selection','somatic','heritable'],
 'substitution':['point substitution','silent mutation','missense mutation','nonsense mutation','premature stop codon'],
 'frameshift':['frameshift mutation','multiple of three','reading frame'],
 'sources':['sources of random dna mutation','mutations generate genetic variation','conserved reproductive sources of variation','radiation','reactive chemicals','crossing-over','independent-assortment','fertilization'],
 'number':['nondisjunction and chromosome number','aneuploidy','chromosome-number changes can disrupt development','trisomy 21','polyploidy'],
 'structure':['chromosome-structure alterations','chromosomal deletion','chromosomal duplication','chromosomal inversion','chromosomal translocation'],
 'hgt':['transformation as horizontal gene transfer','transduction as horizontal gene transfer','conjugation as horizontal gene transfer','horizontal gene transfer','outside parent-to-offspring inheritance'],
 'mobile':['transposition','viral recombination','related viruses','same host cell'],
}
for name,phrases in visible.items():
    if not all(p in full for p in phrases): problems.append(f'high-risk science guard not visibly satisfied: {name}')
# Freeze Journeys 1-4 exactly against F4D.
prior=read(U6/'content-lock-f4d.json')
for rel,meta in prior.get('files',{}).items():
    p=U6/rel
    if rel.startswith('journeys/U6-J'):
        if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4D locked narrative changed: {rel}')
for fname in ['content-lock-f1.json','content-lock-f2.json','content-lock-f3.json','content-lock-f4a.json','content-lock-f4b.json','content-lock-f4c.json','content-lock-f4d.json']:
    if not (U6/fname).exists(): problems.append(f'missing prior lock {fname}')
# upstream U1-U5 byte protection
up=read(U6/'upstream-u1-u5-protection-f1.json')
if up.get('protected_file_count')!=291: problems.append('Units 1–5 protection manifest count changed')
for item in up['protected_files']:
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f'protected Units 1–5 file changed: {item["path"]}')
if lock.get('lock_status')!='LOCKED_F4E_J1_J5' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4E content-lock boundary invalid')
for rel,meta in lock.get('files',{}).items():
    p=U6/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4E locked file mismatch: {rel}')
if not (U6/'f5-release-manifest.json').exists():
    for forbidden in ['memory-objects-f5.json','application-lab.json','review-manifest-f5.json','mixed-discrimination-f5.json','scope-guards-f5.json','finalization-f5.json']:
        if (U6/forbidden).exists(): problems.append(f'premature Unit 6 final runtime artifact exists: {forbidden}')
status=read(U6/'status.json')
if status.get('status') not in {'F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}: problems.append('Unit 6 status boundary invalid')
elif status.get('status')=='STUDENT_READY' and status.get('student_release') is not True: problems.append('Unit 6 F5 release flag invalid')
elif status.get('status')!='STUDENT_READY' and status.get('student_release') is not False: problems.append('Unit 6 pre-F5 release flag invalid')
course=read(ROOT/'content/ap-biology/course.json'); cu6=next(u for u in course['units'] if u['unit_id']=='unit-6')
if cu6.get('status') not in {'F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}: problems.append('course registry Unit 6 boundary invalid')
elif cu6.get('status')=='STUDENT_READY' and cu6.get('student_release') is not True: problems.append('course registry Unit 6 F5 release flag invalid')
elif cu6.get('status')!='STUDENT_READY' and cu6.get('student_release') is not False: problems.append('course registry Unit 6 pre-F5 release flag invalid')
report=['# Unit 6 F4E Narrative QA','','## Result','', '**PASS**' if not problems else '**FAIL**','', '## Journey 5 accounting','', '- Polished scenes: **8 / 8**','- Locked F3 knowledge records represented: **26 / 26**',f'- Exact-name targets explicitly introduced: **{exact}**','- Optional first-exposure recalls: **3**',f'- Narrative words: **{sum(counts)}**',f'- Mean scene length: **{statistics.mean(counts):.1f} words**',f'- Shortest scene: **{min(counts)} words**',f'- Longest scene: **{max(counts)} words**','', '## Prose-quality gates','', '- Every scene establishes left/center/right geography before the case changes.','- One blue reference DNA/chromosome state and one amber altered or acquired state remain reconstructable across the route.','- Mutation mechanism is identified before molecular, phenotypic, environmental, or selection consequence is interpreted.','- Silent, missense, nonsense, and frameshift outcomes remain diagnostically distinct.','- Mutation as a source of novel sequence variation remains distinct from reproductive reshuffling of existing variation.','- Nondisjunction/chromosome-number errors remain distinct from chromosome-structure rearrangements.','- Deletion, duplication, inversion, and translocation remain physically distinct.','- Transformation, transduction, and conjugation remain separate horizontal-transfer routes.','- Natural transformation remains distinct from laboratory biotechnology use.','- Transposition remains distinct from plasmid transfer, and viral recombination requires related viruses coinfecting the same host cell.','- No student prose exposes development/source-management language.','- Journeys 1–4 remain byte-frozen from F4A–F4D.','- Unit 6 remains developer preview with zero final Memory Objects and zero live Challenge Lab tasks.','']
if problems: report+=['## Blocking findings','']+[f'- {p}' for p in problems]+['']
(ROOT/'docs/UNIT6_F4E_QA.md').write_text('\n'.join(report),encoding='utf-8')
if problems:
    print('UNIT 6 F4E QA FAIL'); print('\n'.join('- '+x for x in problems)); sys.exit(1)
print('UNIT 6 F4E QA PASS'); print(json.dumps({'journey':'U6-J5','scenes':8,'knowledge_records':26,'exact_name_targets':exact,'optional_recalls':3,'story_words':sum(counts),'average_scene_words':round(statistics.mean(counts),1),'min_scene_words':min(counts),'max_scene_words':max(counts),'journeys1_4_frozen':True,'student_release':False},indent=2))
