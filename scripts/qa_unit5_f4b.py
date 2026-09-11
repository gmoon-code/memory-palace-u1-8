from __future__ import annotations
import json,re,statistics,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
problems=[]
canon={r['knowledge_id']:r for r in read(U5/'source/canonical-unit5-f1.json')['canonical_catalog']}
f3=read(U5/'briefs/scene-briefs-f3.json')['scene_briefs']; f3j2=[b for b in f3 if b['journey_id']=='U5-J2']
j1=read(U5/'journeys/U5-J1.json'); j2=read(U5/'journeys/U5-J2.json'); lock=read(U5/'content-lock-f4b.json')

if j2.get('palace_id')!='U5-J2' or j2.get('scene_count')!=10 or len(j2.get('scenes',[]))!=10: problems.append('Journey 2 scene accounting mismatch')
if j2.get('checkpoint_count')!=3: problems.append('Journey 2 checkpoint count differs from F3')
if [s.get('locus_id') for s in j2['scenes']] != [f'U5-L{i:02d}' for i in range(6,16)]: problems.append('Journey 2 route differs from F2/F3')
if j2.get('guide',{}).get('name')!='Dr. Imani Reyes': problems.append('Journey 2 guide changed')
if j2.get('student_release')!='DEVELOPER_PREVIEW_F4B': problems.append('Journey 2 preview boundary is wrong')

banned=re.compile(r'\b(PPT|CED|College Board|Campbell|source lock|canonical record|review flag|teacher slide|assessment management)\b',re.I)
assigned=[]; word_counts=[]
for idx,(s,b) in enumerate(zip(j2['scenes'],f3j2)):
    lid=s['locus_id']; prose=' '.join(s.get('story_paragraphs',[])); low=prose.casefold().replace('**','')
    words=len(re.findall(r"\b[\w’'-]+\b",prose)); word_counts.append(words)
    assigned += s.get('object_ids',[])
    if words<450: problems.append(f'{lid} narrative too short: {words}')
    if len(s.get('story_paragraphs',[]))<6: problems.append(f'{lid} has fewer than 6 narrative paragraphs')
    opening=s['story_paragraphs'][0].lower()
    if 'left' not in opening or ('ahead' not in opening and 'center' not in opening) or 'right' not in opening: problems.append(f'{lid} opening does not establish left/center/right geography')
    if len(s.get('scene_layout',{}).get('zones',[]))!=3: problems.append(f'{lid} does not preserve three-zone geometry')
    if {z.get('position') for z in s['scene_layout']['zones']}!={'left','center','right'}: problems.append(f'{lid} zone positions changed')
    if len(s.get('cast',[]))<6: problems.append(f'{lid} cast is too thin')
    if s['cast'][0].get('name')!='Dr. Imani Reyes': problems.append(f'{lid} guide is not first cast member')
    if not any(c.get('name')=='Tracked chromosome set' for c in s['cast']): problems.append(f'{lid} missing persistent chromosome set')
    if not any(c.get('name')=='Gold generation ledger' for c in s['cast']): problems.append(f'{lid} missing gold ledger')
    if banned.search(prose): problems.append(f'{lid} exposes source/development language: {banned.search(prose).group(0)}')
    if s.get('object_ids')!=b.get('knowledge_ids'): problems.append(f'{lid} F3 knowledge assignment changed')
    for beat in s.get('story_beats',[]):
        kid=beat['object_id']
        if beat.get('science')!=canon[kid]['canonical_verified_statement']: problems.append(f'{lid} canonical science changed for {kid}')
        if beat.get('term','').casefold() not in low: problems.append(f"{lid} exact term/relationship missing from prose: {beat.get('term')}")
    if s.get('misconception_guards')!=b.get('misconception_guards'): problems.append(f'{lid} misconception guards changed from F3')
    if bool(s.get('checkpoint'))!=bool(b.get('quick_recall',{}).get('enabled')): problems.append(f'{lid} checkpoint placement changed from F3')
    if s.get('checkpoint'):
        if s.get('checkpoint_prompt')!=b['quick_recall'].get('candidate_prompt'): problems.append(f'{lid} checkpoint prompt changed')
        if s.get('checkpoint_answer')!=b['quick_recall'].get('answer'): problems.append(f'{lid} checkpoint answer changed')
        if len(s.get('checkpoint_hint',''))<100: problems.append(f'{lid} checkpoint hint too thin')
    if s.get('causal_transition')!=b['causal_transition']['transition_logic']: problems.append(f'{lid} causal transition changed from F3')

expected={kid for b in f3j2 for kid in b['knowledge_ids']}
if len(assigned)!=18 or len(set(assigned))!=18 or set(assigned)!=expected: problems.append(f'Journey 2 record coverage mismatch refs={len(assigned)} unique={len(set(assigned))}')
if statistics.mean(word_counts)<480 or min(word_counts)<450: problems.append(f'Journey 2 prose density below F4B target avg={statistics.mean(word_counts):.1f}, min={min(word_counts)}')
if sum(bool(s['checkpoint']) for s in j2['scenes'])!=3: problems.append('Journey 2 recall count is not 3')
if len(j2.get('premise',''))<300 or len(j2.get('mission',''))<250 or len(j2.get('finale',''))<300: problems.append('Journey 2 framing is too thin')

# Structural/scientific continuity must be expressed in prose itself.
full=' '.join(' '.join(s['story_paragraphs']) for s in j2['scenes']).lower().replace('**','')
visible={
 'same_chromosomes':['same blue and amber','same chromosomes'],
 'one_replication':['premeiotic interphase','no dna replication between meiosis i and ii'],
 'prophase_i':['synapsis','tetrad','chiasma','nonsister chromatids of homologous chromosomes'],
 'metaphase_contrast':['metaphase i aligns homologous pairs','metaphase ii aligns individual duplicated chromosomes'],
 'anaphase_i':['anaphase i separates homologous chromosomes while sister chromatids remain attached'],
 'haploid_duplicated':['haploid because homologous pairs have separated','each chromosome is still duplicated'],
 'anaphase_ii':['anaphase ii','sister chromatids separate'],
 'final_four':['four haploid products','telophase ii and cytokinesis'],
}
for name,phrases in visible.items():
    if not all(p in full for p in phrases): problems.append(f'high-risk meiosis continuity guard missing from prose: {name}')

# J1 must remain byte-identical to its F4A lock.
f4a=read(U5/'content-lock-f4a.json')
for rel,meta in f4a.get('files',{}).items():
    p=U5/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4A locked file changed {rel}')

# Earlier F1-F3 locks and released Units 1-4 remain protected.
for lock_name in ('content-lock-f1.json','content-lock-f2.json','content-lock-f3.json'):
    earlier=read(U5/lock_name)
    entries=earlier.get('protected_files') or [{'path':rel,**meta} for rel,meta in earlier.get('files',{}).items()]
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

if lock.get('lock_status')!='LOCKED_F4B_J2' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4B content lock boundary is wrong')
for rel,meta in lock.get('files',{}).items():
    p=U5/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4B locked file mismatch {rel}')

if not (U5/'f5-release-manifest.json').exists():
    for forbidden in [U5/'memory-objects.json',U5/'application-lab.json',U5/'review-manifest-f5.json',U5/'finalization-f5.json']:
        if forbidden.exists(): problems.append(f'premature Unit 5 student runtime artifact exists {forbidden.relative_to(ROOT)}')

course=read(ROOT/'content/ap-biology/course.json'); cu5=next(u for u in course['units'] if u['unit_id']=='unit-5')
if cu5.get('status')=='STUDENT_READY':
    if cu5.get('student_release') is not True or cu5.get('preview_release') is not False: problems.append('course registry F5 release state invalid after F4B')
elif cu5.get('status') not in {'F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW','F4G_JOURNEYS1_7_POLISHED_DEVELOPER_PREVIEW','F4H_JOURNEYS1_8_POLISHED_DEVELOPER_PREVIEW'} or cu5.get('student_release') is not False or cu5.get('preview_release') is not True: problems.append('course registry F4B-or-later preview state mismatch')
if cu5.get('journey_count',0)<2 or cu5.get('scene_count',0)<15: problems.append('course registry lost F4B accounting')

report=['# Unit 5 F4B Narrative QA','', '## Result','', '**PASS**' if not problems else '**FAIL**','', '## Journey 2 accounting','', '- Polished scenes: **10 / 10**', f'- Locked knowledge records represented: **{len(set(assigned))} / 18**', '- Optional first-exposure recalls: **3**', f'- Narrative words: **{sum(word_counts)}**', f'- Mean scene length: **{statistics.mean(word_counts):.1f} words**', f'- Shortest scene: **{min(word_counts)} words**','', '## Prose-level gates','', '- Every scene fixes left/center/right geography before new terminology is introduced.', '- Dr. Imani Reyes, the gold ledger, and persistent chromosome identities remain visible across all ten stations.', '- The same chromosome state is updated in place from premeiotic replication through the four final products.', '- F1 canonical science remains exact in the story-beat layer, and every assigned F3 term/relationship is explicitly introduced in prose.', '- Prophase-I synapsis/tetrad/chiasma/crossing-over distinctions remain explicit.', '- Metaphase-I homolog-pair alignment is physically distinguished from metaphase-II individual-chromosome alignment.', '- Anaphase-I homolog segregation is physically distinguished from anaphase-II sister-chromatid segregation.', '- Cells are explicitly haploid after meiosis I while chromosomes remain duplicated.', '- No DNA replication occurs between meiosis I and meiosis II.', '- All three F3 optional Quick Recall placements and answers remain unchanged.', '- Unit 5 remains developer preview only.','']
if problems: report += ['## Blocking findings','']+[f'- {p}' for p in problems]+['']
(ROOT/'docs'/'UNIT5_F4B_QA.md').write_text('\n'.join(report),encoding='utf-8')
if problems:
    print('UNIT 5 F4B QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT 5 F4B QA PASS')
print(json.dumps({'journey':'U5-J2','scenes':10,'knowledge_records':18,'optional_recalls':3,'story_words':sum(word_counts),'average_scene_words':round(statistics.mean(word_counts),1),'min_scene_words':min(word_counts),'student_release':False,'preview_release':True},indent=2))
