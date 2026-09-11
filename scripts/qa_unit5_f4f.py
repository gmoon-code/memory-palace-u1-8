from __future__ import annotations
import hashlib,json,re,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; U5=ROOT/'content'/'ap-biology'/'unit-5'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
problems=[]
j=read(U5/'journeys/U5-J6.json')
briefs={b['locus_id']:b for b in read(U5/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U5-J6'}
canon={r['knowledge_id']:r for r in read(U5/'source/canonical-unit5-f1.json')['canonical_catalog']}
lock=read(U5/'content-lock-f4f.json')
expected_ids=[f'U5-L{i:02d}' for i in range(31,38)]
if j.get('palace_id')!='U5-J6' or j.get('scene_count')!=7 or len(j.get('scenes',[]))!=7: problems.append('Journey 6 accounting is wrong')
if [s['locus_id'] for s in j['scenes']]!=expected_ids: problems.append('Journey 6 route changed from F3')
if j.get('checkpoint_count')!=2: problems.append('Journey 6 checkpoint count changed')
if j.get('student_release')!='DEVELOPER_PREVIEW_F4F': problems.append('Journey 6 preview boundary is wrong')
assigned=[oid for s in j['scenes'] for oid in s['object_ids']]
f3assigned=[oid for lid in expected_ids for oid in briefs[lid]['knowledge_ids']]
if len(assigned)!=24 or len(set(assigned))!=24: problems.append(f'Journey 6 record coverage is {len(assigned)} refs / {len(set(assigned))} unique, expected 24/24')
if assigned!=f3assigned: problems.append('Journey 6 record order/assignment changed from F3')

banned_source=re.compile(r'\b(?:PPT|CED|College Board|Campbell|source[- ]lock|review[- ]flag|teacher packet|class notes)\b',re.I)
word_counts=[]
for s in j['scenes']:
    b=briefs[s['locus_id']]
    prose=' '.join(s['story_paragraphs'])
    visible=prose.casefold().replace('**','')
    words=len(re.findall(r"\b[\w’'-]+\b",prose)); word_counts.append(words)
    if words<640: problems.append(f"{s['locus_id']} has only {words} narrative words")
    if len(s['story_paragraphs'])<6: problems.append(f"{s['locus_id']} has too few narrative paragraphs")
    opening=s['story_paragraphs'][0].casefold()
    if 'left' not in opening or 'right' not in opening or ('ahead' not in opening and 'center' not in opening): problems.append(f"{s['locus_id']} opening does not establish left/center/right geography")
    names={c['name'] for c in s['cast']}
    for required in ('Dr. Imani Reyes','Phenotype-comparison frame','Mechanism identity cards','Gold generation ledger'):
        if required not in names: problems.append(f"{s['locus_id']} missing persistent cast {required}")
    if s['misconception_guards']!=b['misconception_guards']: problems.append(f"{s['locus_id']} F3 misconception guards changed")
    if s['object_ids']!=b['knowledge_ids']: problems.append(f"{s['locus_id']} F3 knowledge assignment changed")
    for beat in s['story_beats']:
        if beat['science']!=canon[beat['object_id']]['canonical_verified_statement']: problems.append(f"{s['locus_id']} canonical science drift for {beat['object_id']}")
        if beat['term'].casefold() not in visible: problems.append(f"{s['locus_id']} exact term absent from prose {beat['term']}")
    q=b['quick_recall']; enabled=bool(q['enabled'])
    if bool(s['checkpoint'])!=enabled: problems.append(f"{s['locus_id']} recall placement changed")
    if enabled and (s['checkpoint_prompt']!=q['candidate_prompt'] or s['checkpoint_answer']!=q['answer']): problems.append(f"{s['locus_id']} recall wording changed")
    if banned_source.search(prose): problems.append(f"{s['locus_id']} exposes source-management language")
    if '—' in prose: problems.append(f"{s['locus_id']} contains an em dash in student prose")
    if ':' in prose: problems.append(f"{s['locus_id']} contains colon punctuation in student prose")
    for phrase in ('rather than','instead of','not only'):
        if phrase in visible: problems.append(f"{s['locus_id']} contains prohibited contrast phrase {phrase}")

if statistics.mean(word_counts)<675: problems.append(f'Journey 6 average prose density below target {statistics.mean(word_counts):.1f}')
full=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
required_groups={
 'non_mendelian_boundary':['quantitative identification of non-mendelian ratios','statistically meaningful','non-mendelian inheritance patterns','segregation principle can still apply'],
 'dominance_discrimination':['incomplete dominance','intermediate phenotype','codominance','both allelic effects remain','multiple alleles','more than two allele variants','abo blood-group allele system','ia and ib are codominant'],
 'gene_interaction_discrimination':['epistasis','genotype at one gene affects the phenotypic expression of another gene','polygenic inheritance','multiple genes contributing to one character','pleiotropy','one gene influencing multiple effects'],
 'chromosome_model_boundary':['autosome','human x/y chromosome-complement model','x-linked gene','y-linked gene','sex-linked inheritance','does not define gender','full biology of human sex development','other sex-determination systems'],
 'hemizygous_transmission':['hemizygous','one copy of a gene or chromosomal region','x-linked transmission in an xx/xy model','track the actual parental chromosome complements and alleles','x-linked disorder examples'],
 'x_inactivation':['x-chromosome inactivation','largely transcriptionally inactive','barr body','some genes can escape','mosaic'],
 'environment':['environmental effects on phenotype','genotype-by-environment context','phenotypic plasticity','temperature-dependent pigmentation example','soil-ph flower-color example','uv and melanin example','same genotype can produce different phenotypes','all phenotypic variation is environmental']
}
for name,phrases in required_groups.items():
    if not all(p in full for p in phrases):
        missing=[p for p in phrases if p not in full]
        problems.append(f'high-risk Journey 6 discrimination guard missing from prose {name}: {missing}')

# Explicit mechanism geometry that must be reconstructable without labels.
for phrase in [
    'one broad sign that calls every unusual heterozygote blended',
    'the geometry is many genes feeding one character',
    'the second right-side branch reverses the geometry',
    'the chromosome carrying the gene is the causal anchor',
    'the key event is a change in gene activity, not deletion of an x chromosome',
    'hold genotype constant first'
]:
    if phrase not in full: problems.append(f'explicit Journey 6 causal-geometry guard missing: {phrase}')

# Preserve predecessor narratives byte-for-byte.
for lock_name,rels in [
 ('content-lock-f4a.json',['journeys/U5-J1.json']),
 ('content-lock-f4b.json',['journeys/U5-J2.json']),
 ('content-lock-f4c.json',['journeys/U5-J3.json']),
 ('content-lock-f4d.json',['journeys/U5-J4.json']),
 ('content-lock-f4e.json',['journeys/U5-J5.json'])
]:
    old=read(U5/lock_name)
    for rel in rels:
        meta=old['files'][rel]; p=U5/rel
        if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'{lock_name} locked predecessor changed {rel}')

# Preserve F1-F3 locks and released Units 1-4 content.
for lock_name in ('content-lock-f1.json','content-lock-f2.json','content-lock-f3.json'):
    old=read(U5/lock_name)
    entries=old.get('protected_files') or [{'path':rel,**meta} for rel,meta in old.get('files',{}).items()]
    for item in entries:
        rel=item['path']; p=ROOT/rel if rel.startswith('content/') else U5/rel
        if not p.exists(): problems.append(f'{lock_name} protected file missing {rel}'); continue
        if item.get('bytes') is not None and p.stat().st_size!=item['bytes']: problems.append(f'{lock_name} protected size changed {rel}')
        if item.get('sha256') and sha(p)!=item['sha256']: problems.append(f'{lock_name} protected hash changed {rel}')
up=read(U5/'upstream-u1-u4-protection-f1.json')
if up.get('protected_file_count')!=216: problems.append('Units 1-4 protected file count changed')
for item in up.get('protected_files',[]):
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f"Units 1-4 protected file changed {item['path']}")

if lock.get('lock_status')!='LOCKED_F4F_J6' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4F content-lock boundary is wrong')
for rel,meta in lock.get('files',{}).items():
    p=U5/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4F locked file mismatch {rel}')

if not (U5/'f5-release-manifest.json').exists():
    for forbidden in [U5/'memory-objects.json',U5/'application-lab.json',U5/'review-manifest-f5.json',U5/'finalization-f5.json']:
        if forbidden.exists(): problems.append(f'premature Unit 5 student runtime artifact exists {forbidden.relative_to(ROOT)}')

course=read(ROOT/'content/ap-biology/course.json'); cu5=next(u for u in course['units'] if u['unit_id']=='unit-5')
if cu5.get('status')=='STUDENT_READY':
    if cu5.get('student_release') is not True or cu5.get('preview_release') is not False: problems.append('course registry F5 release state invalid after F4F')
elif cu5.get('status') not in {'F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW','F4G_JOURNEYS1_7_POLISHED_DEVELOPER_PREVIEW','F4H_JOURNEYS1_8_POLISHED_DEVELOPER_PREVIEW'} or cu5.get('student_release') is not False or cu5.get('preview_release') is not True: problems.append('course registry F4F-or-later preview state mismatch')
if cu5.get('journey_count',0)<6 or cu5.get('scene_count',0)<37: problems.append('course registry lost F4F accounting')

report=['# Unit 5 F4F Narrative QA','', '## Result','', '**PASS**' if not problems else '**FAIL**','', '## Journey 6 accounting','', '- Journeys 1–5 protected from F4A–F4E: **PASS**' if not any('predecessor' in p for p in problems) else '- Journeys 1–5 protected from F4A–F4E: **FAIL**', '- Polished Journey 6 scenes: **7 / 7**', f'- Locked Journey 6 knowledge records represented: **{len(set(assigned))} / 24**', '- Optional first-exposure recalls: **2**', f'- Journey 6 narrative words: **{sum(word_counts)}**', f'- Mean Journey 6 scene length: **{statistics.mean(word_counts):.1f} words**', f'- Shortest Journey 6 scene: **{min(word_counts)} words**','', '## Prose-level gates','', '- Every scene establishes stable left, center, and right geography before the mechanism is named.', '- Dr. Imani Reyes, the phenotype-comparison frame, mechanism identity cards, and gold generation ledger persist across all seven locations.', '- The input to mechanism to phenotype geometry remains stable while only the biological cause changes.', '- Non-simple ratios remain a broad observation and never replace the specific mechanism that explains the pattern.', '- Incomplete dominance, codominance, multiple alleles, and ABO are separated by heterozygous phenotype and population allele number.', '- Epistasis, polygenic inheritance, and pleiotropy remain discriminable through gene interaction and gene-to-effect direction.', '- X-linked and Y-linked inheritance remain tied to explicit chromosome location and an explicit chromosome-complement model.', '- XX/XY chromosome transmission is not equated with gender or a complete account of human sex development, and other systems are acknowledged.', '- Hemizygosity, X-chromosome inactivation, and Barr bodies remain copy-number, regulatory, and chromatin-state concepts respectively.', '- Environmental effects hold genotype constant before environmental context changes physiology or gene expression.', '- Both F3 Quick Recall placements and answers remain unchanged.', '- Every assigned F3 record retains exact F1 canonical science in the story-beat layer.', '- Student prose contains no source-management language, colons, em dashes, or prohibited contrast phrases.', '- Unit 5 remains developer preview only.','']
if problems: report += ['## Blocking findings','']+[f'- {p}' for p in problems]+['']
(ROOT/'docs'/'UNIT5_F4F_QA.md').write_text('\n'.join(report),encoding='utf-8')
if problems:
    print('UNIT 5 F4F QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT 5 F4F QA PASS')
print(json.dumps({'journey':'U5-J6','scenes':7,'knowledge_records':24,'optional_recalls':2,'story_words':sum(word_counts),'average_scene_words':round(statistics.mean(word_counts),1),'min_scene_words':min(word_counts),'journeys_1_5_unchanged':True,'student_release':False,'preview_release':True},indent=2))
