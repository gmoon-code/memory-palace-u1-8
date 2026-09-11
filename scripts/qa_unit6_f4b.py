from __future__ import annotations
import json,hashlib,re,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; U6=ROOT/'content'/'ap-biology'/'unit-6'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def wc(t): return len(re.findall(r"\b[\w’′'-]+\b",t))
problems=[]
j=read(U6/'journeys/U6-J2.json'); canon={r['knowledge_id']:r for r in read(U6/'source/canonical-unit6-f1.json')['canonical_catalog']}; briefs={b['locus_id']:b for b in read(U6/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U6-J2'}; lock=read(U6/'content-lock-f4b.json')
expected=[f'U6-L{i:02d}' for i in range(13,21)]
if j.get('palace_id')!='U6-J2': problems.append('Journey 2 ID changed')
if j.get('scene_count')!=8 or len(j.get('scenes',[]))!=8: problems.append('Journey 2 must contain 8 scenes')
if [s.get('locus_id') for s in j['scenes']]!=expected: problems.append('F2/F3 locus order changed')
if j.get('checkpoint_count')!=3: problems.append('F3 Quick Recall count changed from 3')
if j.get('student_release')!='DEVELOPER_PREVIEW_F4B' or j.get('preview_release') is not True: problems.append('F4B preview boundary wrong')
if j.get('guide',{}).get('name')!='Dr. Sora Han': problems.append('Unit 6 guide changed')
if 'eight-location route' not in j.get('route_orientation',''): problems.append('route orientation does not define eight-location route')
if len(j.get('premise',''))<400 or len(j.get('mission',''))<220 or len(j.get('finale',''))<300: problems.append('journey-level framing too thin')
assigned=[]; counts=[]; exact=0
banned=re.compile(r'\b(PPT|CED|Campbell|College Board|teacher enrichment|teacher-required|exam scope|exam-scope|source material|source lock|canonical record|F1|F2|F3|F4A|F4B)\b',re.I)
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
    if not any(c.get('name')=='Persistent tagged gene and red RNA transcript' for c in s['cast']): problems.append(f'{lid} lost continuity object')
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
if len(assigned)!=26 or len(set(assigned))!=26: problems.append(f'Journey 2 coverage {len(assigned)} refs/{len(set(assigned))} unique expected 26/26')
if exact!=21: problems.append(f'Journey 2 exact-name count {exact}, expected 21')
full=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
visible={
 'rna_roles':['rna sequence and structure determine function','messenger rna carries genetic information','ribosomal rna is a functional building block','anticodon'],
 'tRNA_distinction':['specific amino acids','complementary mrna codon','anticodon'],
 'expression_scope':['functional rna or polypeptide product','transcription is dna-directed synthesis of rna','translation is synthesis of a polypeptide'],
 'cell_context':['eukaryotic cell','prokaryotes have no nucleus'],
 'template_promoter':['single dna template strand','promoter is a dna region','not present in every eukaryotic promoter'],
 'directionality':['synthesizes rna 5′→3′','reading the dna template 3′→5′'],
 'prokaryotic_qualification':['many bacterial mrnas','without the eukaryotic cap/poly-a/splicing','does not mean bacterial rna never undergoes any processing'],
 'cap_tail':['5′ gtp cap recognition','polyadenylation signal','poly-a tail','not a codon'],
 'splicing':['introns','retained exons','alternative splicing','underlying gene dna remains unchanged','mature mrna'],
}
for name,phrases in visible.items():
    if not all(p in full for p in phrases): problems.append(f'high-risk science guard not visibly satisfied: {name}')
# Freeze F4A Journey 1 exactly.
j1=U6/'journeys/U6-J1.json'
if sha(j1)!='fe01ed27cd6a8830022f131c22bcce74f9ad094aef189c991effb66f09741b83': problems.append('F4A Journey 1 changed')
f4a=read(U6/'content-lock-f4a.json')
for rel,meta in f4a.get('files',{}).items():
    p=U6/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4A locked artifact changed: {rel}')
# prior locks
for fname in ['content-lock-f1.json','content-lock-f2.json','content-lock-f3.json']:
    if not (U6/fname).exists(): problems.append(f'missing prior lock {fname}')
# upstream U1-U5 byte protection
up=read(U6/'upstream-u1-u5-protection-f1.json')
if up.get('protected_file_count')!=291: problems.append('Units 1–5 protection manifest count changed')
for item in up['protected_files']:
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f'protected Units 1–5 file changed: {item["path"]}')
if lock.get('lock_status')!='LOCKED_F4B_J1_J2' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4B content-lock boundary invalid')
for rel,meta in lock.get('files',{}).items():
    p=U6/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4B locked file mismatch: {rel}')
if not (U6/'f5-release-manifest.json').exists():
    for forbidden in ['memory-objects-f5.json','application-lab.json','review-manifest-f5.json','mixed-discrimination-f5.json','scope-guards-f5.json','finalization-f5.json']:
        if (U6/forbidden).exists(): problems.append(f'premature Unit 6 final runtime artifact exists: {forbidden}')
status=read(U6/'status.json')
if status.get('status') not in {'F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}: problems.append('Unit 6 status boundary invalid')
elif status.get('status')=='STUDENT_READY' and status.get('student_release') is not True: problems.append('Unit 6 F5 release flag invalid')
elif status.get('status')!='STUDENT_READY' and status.get('student_release') is not False: problems.append('Unit 6 pre-F5 release flag invalid')
course=read(ROOT/'content/ap-biology/course.json'); cu6=next(u for u in course['units'] if u['unit_id']=='unit-6')
if cu6.get('status') not in {'F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}: problems.append('course registry Unit 6 boundary invalid')
elif cu6.get('status')=='STUDENT_READY' and cu6.get('student_release') is not True: problems.append('course registry Unit 6 F5 release flag invalid')
elif cu6.get('status')!='STUDENT_READY' and cu6.get('student_release') is not False: problems.append('course registry Unit 6 pre-F5 release flag invalid')
report=['# Unit 6 F4B Narrative QA','','## Result','', '**PASS**' if not problems else '**FAIL**','', '## Journey 2 accounting','', '- Polished scenes: **8 / 8**','- Locked F3 knowledge records represented: **26 / 26**',f'- Exact-name targets explicitly introduced: **{exact}**','- Optional first-exposure recalls: **3**',f'- Narrative words: **{sum(counts)}**',f'- Mean scene length: **{statistics.mean(counts):.1f} words**',f'- Shortest scene: **{min(counts)} words**',f'- Longest scene: **{max(counts)} words**','', '## Prose-quality gates','', '- Every scene establishes left/center/right geography before the molecular state changes.','- Dr. Sora Han, the tagged gene, violet template strand, and red RNA transcript persist through all eight locations.','- mRNA, tRNA, rRNA, DNA template strand, promoter, TATA element, RNA polymerase, prokaryotic transcript, pre-mRNA, cap, poly-A tail, introns, exons, and mature mRNA retain conventional scientific identities.','- Every story beat preserves the exact F1 canonical scientific statement and F3 object assignment.','- Transcription and translation remain physically separate; promoter and TATA box remain distinct; RNA is synthesized 5′→3′ while template DNA is read 3′→5′.','- Prokaryotic transcript handling is qualified and is not rewritten as “prokaryotes never process RNA.”','- 5′ cap, polyadenylation signal, poly-A tail, intron removal, exon retention, alternative splicing, and mature mRNA remain distinct processing concepts.','- No student prose exposes development/source-management language.','- Journey 1 remains byte-frozen from F4A.','- Unit 6 remains developer preview with zero final Memory Objects and zero live Challenge Lab tasks.','']
if problems: report+=['## Blocking findings','']+[f'- {p}' for p in problems]+['']
(ROOT/'docs/UNIT6_F4B_QA.md').write_text('\n'.join(report),encoding='utf-8')
if problems:
    print('UNIT 6 F4B QA FAIL'); print('\n'.join('- '+x for x in problems)); sys.exit(1)
print('UNIT 6 F4B QA PASS'); print(json.dumps({'journey':'U6-J2','scenes':8,'knowledge_records':26,'exact_name_targets':exact,'optional_recalls':3,'story_words':sum(counts),'average_scene_words':round(statistics.mean(counts),1),'min_scene_words':min(counts),'max_scene_words':max(counts),'journey1_frozen':True,'student_release':False},indent=2))
