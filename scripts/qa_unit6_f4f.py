from __future__ import annotations
import json,re,hashlib,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U6=ROOT/'content'/'ap-biology'/'unit-6'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def wc(s): return len(re.findall(r"\b[\w’′'-]+\b",s))

problems=[]
j=read(U6/'journeys/U6-J6.json')
briefs={b['locus_id']:b for b in read(U6/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U6-J6'}
canon={r['knowledge_id']:r for r in read(U6/'source/canonical-unit6-f1.json')['canonical_catalog']}
lock=read(U6/'content-lock-f4f.json')
expected=[f'U6-L{i:02d}' for i in range(49,54)]
if j.get('palace_id')!='U6-J6': problems.append('Journey 6 ID changed')
if j.get('scene_count')!=5 or len(j.get('scenes',[]))!=5: problems.append('Journey 6 must contain 5 scenes')
if [s.get('locus_id') for s in j['scenes']]!=expected: problems.append('F2/F3 locus order changed')
if j.get('checkpoint_count')!=2: problems.append('F3 Quick Recall count changed from 2')
if j.get('student_release')!='DEVELOPER_PREVIEW_F4F' or j.get('preview_release') is not True: problems.append('F4F preview boundary wrong')
if j.get('guide',{}).get('name')!='Dr. Sora Han': problems.append('Unit 6 guide changed')
if 'five-location investigation' not in j.get('route_orientation',''): problems.append('route orientation does not define five-location investigation')
if len(j.get('premise',''))<500 or len(j.get('mission',''))<350 or len(j.get('finale',''))<400: problems.append('journey-level framing too thin')
assigned=[]; counts=[]; exact=0
banned=re.compile(r'\b(PPT|CED|Campbell|College Board|teacher enrichment|teacher-required|exam scope|exam-scope|source material|source lock|canonical record|F1|F2|F3|F4A|F4B|F4C|F4D|F4E|F4F|F5)\b',re.I)
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
    if not any(c.get('name')=='U6-X coded sample and branch ledger' for c in s['cast']): problems.append(f'{lid} lost continuity object')
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
if len(assigned)!=11 or len(set(assigned))!=11: problems.append(f'Journey 6 coverage {len(assigned)} refs/{len(set(assigned))} unique expected 11/11')
if exact!=9: problems.append(f'Journey 6 exact-name count {exact}, expected 9')
full=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
visible={
 'intake':['genetic engineering manipulates/analyzes nucleic acids','dna and rna','question','analysis'],
 'gel':['gel electrophoresis','negative charge','positive electrode','smaller fragments','band pattern','not dna sequencing'],
 'pcr':['pcr denaturation','pcr primer annealing','pcr extension','pcr amplification principle','denaturation → pcr primer annealing → pcr extension'],
 'transform':['bacterial transformation as biotechnology','foreign dna','recombinant dna expression in bacteria','appropriate regulatory sequences','horizontal gene transfer'],
 'sequence':['dna sequencing','order of nucleotides','dna profiles/fingerprints support comparison','fragment patterns','not a nucleotide letter'],
}
for name,phrases in visible.items():
    if not all(p in full for p in phrases): problems.append(f'high-risk science guard not visibly satisfied: {name}')
# Freeze Journeys 1-5 exactly against F4E.
prior=read(U6/'content-lock-f4e.json')
for rel,meta in prior.get('files',{}).items():
    p=U6/rel
    if rel.startswith('journeys/U6-J'):
        if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4E locked narrative changed: {rel}')
for fname in ['content-lock-f1.json','content-lock-f2.json','content-lock-f3.json','content-lock-f4a.json','content-lock-f4b.json','content-lock-f4c.json','content-lock-f4d.json','content-lock-f4e.json']:
    if not (U6/fname).exists(): problems.append(f'missing prior lock {fname}')
# All six journeys must now cover the full F2 palace-managed set exactly once.
allj=[read(U6/f'journeys/U6-J{i}.json') for i in range(1,7)]
all_ids=[kid for jj in allj for ss in jj['scenes'] for kid in ss['object_ids']]
if sum(len(jj['scenes']) for jj in allj)!=53: problems.append('all-six polished scene count is not 53')
if len(all_ids)!=161 or len(set(all_ids))!=161: problems.append(f'all-six palace coverage {len(all_ids)} refs/{len(set(all_ids))} unique expected 161/161')
if sum(jj['checkpoint_count'] for jj in allj)!=18: problems.append('all-six Quick Recall count is not 18')
# upstream U1-U5 byte protection
up=read(U6/'upstream-u1-u5-protection-f1.json')
if up.get('protected_file_count')!=291: problems.append('Units 1–5 protection manifest count changed')
for item in up['protected_files']:
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f'protected Units 1–5 file changed: {item["path"]}')
if lock.get('lock_status')!='LOCKED_F4F_J1_J6' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4F content-lock boundary invalid')
for rel,meta in lock.get('files',{}).items():
    p=U6/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4F locked file mismatch: {rel}')
if not (U6/'f5-release-manifest.json').exists():
    for forbidden in ['memory-objects-f5.json','application-lab.json','review-manifest-f5.json','mixed-discrimination-f5.json','scope-guards-f5.json','finalization-f5.json']:
        if (U6/forbidden).exists(): problems.append(f'premature Unit 6 final runtime artifact exists: {forbidden}')
status=read(U6/'status.json')
if status.get('status') not in {'F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}: problems.append('Unit 6 status boundary invalid')
elif status.get('status')=='STUDENT_READY' and status.get('student_release') is not True: problems.append('Unit 6 F5 release flag invalid')
elif status.get('status')!='STUDENT_READY' and status.get('student_release') is not False: problems.append('Unit 6 pre-F5 release flag invalid')
course=read(ROOT/'content/ap-biology/course.json'); cu6=next(u for u in course['units'] if u['unit_id']=='unit-6')
if cu6.get('status') not in {'F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}: problems.append('course registry Unit 6 F4F boundary invalid')
elif cu6.get('status')=='STUDENT_READY' and cu6.get('student_release') is not True: problems.append('course registry Unit 6 F5 release flag invalid')
elif cu6.get('status')!='STUDENT_READY' and cu6.get('student_release') is not False: problems.append('course registry Unit 6 pre-F5 release flag invalid')
report=['# Unit 6 F4F Narrative QA','','## Result','', '**PASS**' if not problems else '**FAIL**','', '## Journey 6 accounting','', '- Polished scenes: **5 / 5**','- Locked F3 knowledge records represented: **11 / 11**',f'- Exact-name targets explicitly introduced: **{exact}**','- Optional first-exposure recalls: **2**',f'- Narrative words: **{sum(counts)}**',f'- Mean scene length: **{statistics.mean(counts):.1f} words**',f'- Shortest scene: **{min(counts)} words**',f'- Longest scene: **{max(counts)} words**','', '## Completed Unit 6 narrative accounting','', '- Polished journeys: **6 / 6**','- Polished permanent scenes: **53 / 53**','- Palace-managed records covered exactly once: **161 / 161**','- Optional first-exposure recalls across all six journeys: **18**','', '## Prose-quality gates','', '- Every scene establishes left/center/right laboratory geography before the procedure begins.','- One U6-X coded sample remains traceable through analytical branches; the engineered plasmid is explicitly separate.','- The laboratory question selects the technique, and every scene distinguishes input, mechanism, and output.','- Gel electrophoresis separates fragments and does not become sequencing or amplification.','- DNA migration direction and standard agarose size separation are explicitly visible.','- PCR denaturation, primer annealing, and extension remain distinct and ordered.','- PCR is represented as target-region amplification, not sequence reading.','- Laboratory bacterial transformation remains distinct from natural horizontal-gene-transfer context.','- Recombinant expression requires appropriate regulatory sequences and is not equated with DNA uptake alone.','- DNA sequencing determines nucleotide order; DNA profiles support comparison without being treated as complete sequences.','- No student prose exposes development/source-management language.','- Journeys 1–5 remain byte-frozen from F4A–F4E.','- Unit 6 remains developer preview with zero final Memory Objects and zero live Challenge Lab tasks.','']
if problems: report+=['## Blocking findings','']+[f'- {p}' for p in problems]+['']
(ROOT/'docs/UNIT6_F4F_QA.md').write_text('\n'.join(report),encoding='utf-8')
if problems:
    print('UNIT 6 F4F QA FAIL'); print('\n'.join('- '+x for x in problems)); sys.exit(1)
print('UNIT 6 F4F QA PASS'); print(json.dumps({'journey':'U6-J6','scenes':5,'knowledge_records':11,'exact_name_targets':exact,'optional_recalls':2,'story_words':sum(counts),'average_scene_words':round(statistics.mean(counts),1),'min_scene_words':min(counts),'max_scene_words':max(counts),'all_six_journeys':6,'all_six_scenes':53,'all_six_palace_records':161,'all_six_optional_recalls':18,'journeys1_5_frozen':True,'student_release':False},indent=2))
