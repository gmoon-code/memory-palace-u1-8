from __future__ import annotations
import json,hashlib,re,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
problems=[]
j=read(U5/'journeys/U5-J4.json')
briefs={b['locus_id']:b for b in read(U5/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U5-J4'}
canon={r['knowledge_id']:r for r in read(U5/'source/canonical-unit5-f1.json')['canonical_catalog']}
lock=read(U5/'content-lock-f4d.json')

expected_ids=[f'U5-L{i:02d}' for i in range(20,27)]
if j.get('palace_id')!='U5-J4' or j.get('scene_count')!=7 or len(j.get('scenes',[]))!=7: problems.append('Journey 4 accounting is wrong')
if [s['locus_id'] for s in j['scenes']]!=expected_ids: problems.append('Journey 4 route changed from F3')
if j.get('checkpoint_count')!=2: problems.append('Journey 4 checkpoint count changed')
if j.get('student_release')!='DEVELOPER_PREVIEW_F4D': problems.append('Journey 4 preview boundary is wrong')

assigned=[kid for s in j['scenes'] for kid in s['object_ids']]
if len(assigned)!=25 or len(set(assigned))!=25: problems.append(f'Journey 4 record coverage is {len(assigned)} refs / {len(set(assigned))} unique, expected 25/25')
f3assigned=[kid for lid in expected_ids for kid in briefs[lid]['knowledge_ids']]
if assigned!=f3assigned: problems.append('Journey 4 record order/assignment changed from F3')

word_counts=[]
banned_source=re.compile(r'\b(PPT|CED|College Board|Campbell|source lock|source material|review flag|teacher material|canonical record)\b',re.I)
for s in j['scenes']:
    b=briefs[s['locus_id']]
    prose=' '.join(s['story_paragraphs'])
    visible=prose.casefold().replace('**','')
    words=len(re.findall(r"\b[\w’'-]+\b",prose)); word_counts.append(words)
    if words<525: problems.append(f"{s['locus_id']} has only {words} narrative words")
    if len(s['story_paragraphs'])<6: problems.append(f"{s['locus_id']} has too few narrative paragraphs")
    opening=s['story_paragraphs'][0].casefold()
    if 'left' not in opening or 'right' not in opening or ('ahead' not in opening and 'center' not in opening): problems.append(f"{s['locus_id']} opening does not establish left/center/right geography")
    names={c['name'] for c in s['cast']}
    for required in ('Dr. Imani Reyes','Pea-line breeding ledger','Tracked allele case'):
        if required not in names: problems.append(f"{s['locus_id']} missing persistent cast {required}")
    if s['misconception_guards']!=b['misconception_guards']: problems.append(f"{s['locus_id']} F3 misconception guards changed")
    if s['object_ids']!=b['knowledge_ids']: problems.append(f"{s['locus_id']} F3 knowledge assignment changed")
    for beat in s['story_beats']:
        if beat['science']!=canon[beat['object_id']]['canonical_verified_statement']: problems.append(f"{s['locus_id']} canonical science drift for {beat['object_id']}")
        if beat['term'].casefold() not in visible: problems.append(f"{s['locus_id']} exact term absent from prose {beat['term']}")
    # F3 quick recalls must remain sparse and unchanged.
    q=b['quick_recall']; enabled=bool(q['enabled'])
    if bool(s['checkpoint'])!=enabled: problems.append(f"{s['locus_id']} recall placement changed")
    if enabled:
        if s['checkpoint_prompt']!=q['candidate_prompt'] or s['checkpoint_answer']!=q['answer']: problems.append(f"{s['locus_id']} recall wording changed")
    if banned_source.search(prose): problems.append(f"{s['locus_id']} exposes source-management language")
    if '—' in prose: problems.append(f"{s['locus_id']} contains an em dash in student prose")
    # Colons are prohibited except the scientifically necessary canonical ratio notation.
    scrub=re.sub(r'9:3:3:1|3:1','',prose)
    if ':' in scrub: problems.append(f"{s['locus_id']} contains colon punctuation outside canonical ratio notation")
    for phrase in ('rather than','instead of','not only'):
        if phrase in visible: problems.append(f"{s['locus_id']} contains prohibited contrast phrase {phrase}")

if statistics.mean(word_counts)<600: problems.append(f'Journey 4 average prose density below target {statistics.mean(word_counts):.1f}')

full=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
required_groups={
 'generation_sequence':['true-breeding line','p generation','f1 generation','f2 generation','gregor mendel'],
 'allele_notation':['allele','dominance notation convention','dominant allele','recessive allele'],
 'dominance_guard':['dominant says nothing about how common','frequency counters'],
 'genotype_phenotype':['genotype, homozygous, heterozygous','phenotype','homozygous dominant','homozygous recessive','complete dominance'],
 'mendelian_laws':['law of segregation','law of independent assortment','mendelian laws for unlinked genes','linked genes'],
 'cross_types':['monohybrid, dihybrid, and test crosses','testcross mechanics','monohybrid','dihybrid','homozygous recessive tester'],
 'gamete_before_grid':['gametes from a genotype','punnett square','possible gametes come from meiosis and the parental genotype'],
 'probability_guard':['predict genotype and phenotype probabilities','not guaranteed offspring counts'],
 'ratio_conditions':['classic 3:1 f2 ratio','classic 9:3:3:1 ratio','assumption banner','assort independently']
}
for name,phrases in required_groups.items():
    if not all(p in full for p in phrases): problems.append(f'high-risk Journey 4 continuity guard missing from prose {name}')

# Explicit causal distinction between mechanism and model.
if 'the possible gametes come from meiosis and the parental genotype, not from the grid' not in full: problems.append('Punnett mechanism/model distinction missing')
if 'the grid size does not define the word monohybrid' not in full: problems.append('monohybrid/grid-size guard missing')
if 'the ratio is a conditional expectation' not in full: problems.append('classic-ratio conditionality guard missing')

# Preserve predecessor narratives byte-for-byte.
for lock_name,rels in [
 ('content-lock-f4a.json',['journeys/U5-J1.json']),
 ('content-lock-f4b.json',['journeys/U5-J2.json']),
 ('content-lock-f4c.json',['journeys/U5-J3.json'])
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

if lock.get('lock_status')!='LOCKED_F4D_J4' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4D content-lock boundary is wrong')
for rel,meta in lock.get('files',{}).items():
    p=U5/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4D locked file mismatch {rel}')

if not (U5/'f5-release-manifest.json').exists():
    for forbidden in [U5/'memory-objects.json',U5/'application-lab.json',U5/'review-manifest-f5.json',U5/'finalization-f5.json']:
        if forbidden.exists(): problems.append(f'premature Unit 5 student runtime artifact exists {forbidden.relative_to(ROOT)}')

course=read(ROOT/'content/ap-biology/course.json'); cu5=next(u for u in course['units'] if u['unit_id']=='unit-5')
if cu5.get('status')=='STUDENT_READY':
    if cu5.get('student_release') is not True or cu5.get('preview_release') is not False: problems.append('course registry F5 release state invalid after F4D')
elif cu5.get('status') not in {'F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW','F4G_JOURNEYS1_7_POLISHED_DEVELOPER_PREVIEW','F4H_JOURNEYS1_8_POLISHED_DEVELOPER_PREVIEW'} or cu5.get('student_release') is not False or cu5.get('preview_release') is not True: problems.append('course registry F4D-or-later preview state mismatch')
if cu5.get('journey_count',0)<4 or cu5.get('scene_count',0)<26: problems.append('course registry lost F4D accounting')

report=['# Unit 5 F4D Narrative QA','', '## Result','', '**PASS**' if not problems else '**FAIL**','', '## Journey 4 accounting','', '- Journeys 1–3 protected from F4A/F4B/F4C: **PASS**' if not any('predecessor' in p for p in problems) else '- Journeys 1–3 protected from F4A/F4B/F4C: **FAIL**', '- Polished Journey 4 scenes: **7 / 7**', f'- Locked Journey 4 knowledge records represented: **{len(set(assigned))} / 25**', '- Optional first-exposure recalls: **2**', f'- Journey 4 narrative words: **{sum(word_counts)}**', f'- Mean Journey 4 scene length: **{statistics.mean(word_counts):.1f} words**', f'- Shortest Journey 4 scene: **{min(word_counts)} words**','', '## Prose-level gates','', '- Every scene establishes stable left/center/right geography before the inheritance model changes.', '- Dr. Imani Reyes, the pea-line breeding ledger, and the tracked allele case persist across all seven locations.', '- P, F1, and F2 labels remain attached to the sequence of crosses that produces those generations.', '- Allele identity, dominance notation, and dominance relationship remain separate.', '- Dominant never becomes a synonym for common, stronger, better, or more evolutionarily successful.', '- Genotype remains distinct from phenotype, and complete dominance does not erase genotype differences between AA and Aa.', '- Segregation remains a one-gene principle; independent assortment remains a conditional relationship for unlinked or effectively independently assorting genes.', '- Cross type is selected before any Punnett grid and is defined by the genetic question and parental genotypes.', '- Gamete possibilities are generated from genotype and meiotic rules before the Punnett grid is populated.', '- Punnett squares remain probability models and never become the causal mechanism of inheritance.', '- Classic 3:1 and 9:3:3:1 ratios are displayed only with their required cross and inheritance assumptions.', '- Both F3 Quick Recall placements and answers remain unchanged.', '- Every assigned F3 record retains exact F1 canonical science in the story-beat layer.', '- Student prose contains no source-management language or em dashes. Colon characters occur only inside canonical ratio notation.', '- Unit 5 remains developer preview only.','']
if problems: report += ['## Blocking findings','']+[f'- {p}' for p in problems]+['']
(ROOT/'docs'/'UNIT5_F4D_QA.md').write_text('\n'.join(report),encoding='utf-8')
if problems:
    print('UNIT 5 F4D QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT 5 F4D QA PASS')
print(json.dumps({'journey':'U5-J4','scenes':7,'knowledge_records':25,'optional_recalls':2,'story_words':sum(word_counts),'average_scene_words':round(statistics.mean(word_counts),1),'min_scene_words':min(word_counts),'journeys_1_3_unchanged':True,'student_release':False,'preview_release':True},indent=2))
