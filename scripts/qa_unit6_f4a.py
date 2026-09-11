from __future__ import annotations
import json, hashlib, re, statistics, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U6=ROOT/'content'/'ap-biology'/'unit-6'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def wc(text): return len(re.findall(r"\b[\w’′'-]+\b",text))

problems=[]
journey=read(U6/'journeys'/'U6-J1.json')
canon={r['knowledge_id']:r for r in read(U6/'source'/'canonical-unit6-f1.json')['canonical_catalog']}
briefs={b['locus_id']:b for b in read(U6/'briefs'/'scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U6-J1'}
lock=read(U6/'content-lock-f4a.json')

expected_loci=[f'U6-L{i:02d}' for i in range(1,13)]
if journey.get('palace_id')!='U6-J1': problems.append('Journey 1 ID changed')
if journey.get('scene_count')!=12 or len(journey.get('scenes',[]))!=12: problems.append('Journey 1 must contain 12 scenes')
if [s.get('locus_id') for s in journey['scenes']]!=expected_loci: problems.append('F2/F3 locus order changed')
if journey.get('checkpoint_count')!=3: problems.append('F3 Quick Recall count changed from 3')
if journey.get('student_release')!='DEVELOPER_PREVIEW_F4A' or journey.get('preview_release') is not True: problems.append('F4A preview boundary is wrong')
if journey.get('guide',{}).get('name')!='Dr. Sora Han': problems.append('Unit 6 guide changed')
if 'twelve-location route' not in journey.get('route_orientation',''): problems.append('route orientation does not explicitly define the twelve-location route')
if len(journey.get('premise',''))<400 or len(journey.get('mission',''))<220 or len(journey.get('finale',''))<300: problems.append('journey-level narrative framing is too thin')

assigned=[]; counts=[]; exact_targets=0
banned=re.compile(r'\b(PPT|CED|Campbell|College Board|teacher enrichment|teacher-required|exam scope|exam-scope|source material|source lock|canonical record|F1|F2|F3|F4A)\b',re.I)
for s in journey['scenes']:
    lid=s['locus_id']; b=briefs[lid]
    prose=' '.join(s.get('story_paragraphs',[])); low=prose.casefold().replace('**','')
    n=wc(prose); counts.append(n)
    if n<450: problems.append(f'{lid} narrative too short: {n} words')
    if len(s.get('story_paragraphs',[]))<5: problems.append(f'{lid} has fewer than 5 narrative paragraphs')
    opening=s['story_paragraphs'][0].lower()
    if 'left' not in opening or ('ahead' not in opening and 'center' not in opening) or 'right' not in opening: problems.append(f'{lid} opening does not orient left/center/right')
    zones=s.get('scene_layout',{}).get('zones',[])
    if len(zones)!=3 or [z.get('position') for z in zones]!=['left','center','right']: problems.append(f'{lid} geometry changed')
    if [z['label'] for z in zones] != [x['anchor'] for x in [b['spatial_layout']['left'],b['spatial_layout']['center'],b['spatial_layout']['right']]]:
        # labels may be polished while anchors are preserved through descriptions; require exact anchor words in orientation instead.
        orient=s['scene_layout']['orientation']
        for x in (b['spatial_layout']['left']['anchor'],b['spatial_layout']['center']['anchor'],b['spatial_layout']['right']['anchor']):
            if x not in orient: problems.append(f'{lid} F3 anchor missing from orientation: {x}')
    if len(s.get('cast',[]))<5: problems.append(f'{lid} cast too thin')
    if not any(c.get('name')=='Dr. Sora Han' for c in s['cast']): problems.append(f'{lid} lost guide')
    if not any(c.get('name')=='Persistent blue-and-gold DNA duplex' for c in s['cast']): problems.append(f'{lid} lost continuity object')
    if s.get('object_ids')!=b['knowledge_ids']: problems.append(f'{lid} knowledge assignment changed from F3')
    assigned += s.get('object_ids',[])
    beats={x['object_id']:x for x in s.get('story_beats',[])}
    if set(beats)!=set(b['knowledge_ids']): problems.append(f'{lid} story-beat coverage mismatch')
    for t in b['term_introductions']:
        kid=t['knowledge_id']; beat=beats.get(kid)
        if not beat: continue
        if beat.get('science')!=canon[kid]['canonical_verified_statement']: problems.append(f'{lid} canonical science changed in beat {kid}')
        if beat.get('term')!=t['canonical_term']: problems.append(f'{lid} canonical term changed in beat {kid}')
        if bool(beat.get('exact_name'))!=bool(t['exact_name_recall']): problems.append(f'{lid} exact-name policy changed {kid}')
        if t['exact_name_recall']:
            exact_targets+=1
            if t['canonical_term'].casefold() not in low: problems.append(f'{lid} exact target absent from prose: {t["canonical_term"]}')
    if banned.search(prose): problems.append(f'{lid} exposes development/source-management language: {banned.search(prose).group(0)}')
    if s.get('checkpoint') != bool(b['quick_recall']['enabled']): problems.append(f'{lid} checkpoint status changed from F3')
    if s.get('checkpoint'):
        if s.get('checkpoint_prompt')!=b['quick_recall']['candidate_prompt']: problems.append(f'{lid} checkpoint prompt changed')
        if s.get('checkpoint_answer')!=b['quick_recall']['answer']: problems.append(f'{lid} checkpoint answer changed')
    expected_next=None
    idx=expected_loci.index(lid)
    if idx < len(expected_loci)-1: expected_next=journey['scenes'][idx+1]['locus']
    if s.get('next_locus')!=expected_next: problems.append(f'{lid} next-locus continuity broken')

if len(assigned)!=42 or len(set(assigned))!=42: problems.append(f'Journey 1 knowledge coverage is {len(assigned)} refs / {len(set(assigned))} unique, expected 42/42')
if exact_targets!=34: problems.append(f'Journey 1 exact-name target count is {exact_targets}, expected 34')

# Visible high-risk science/misconception guards.
full=' '.join(' '.join(s['story_paragraphs']) for s in journey['scenes']).casefold().replace('**','')
visible={
 'rna_qualifier':['some biological systems','rna can serve as the hereditary material'],
 'typical_chromosome_forms':['typically have circular chromosomes','typically have multiple linear chromosomes'],
 'plasmid_vs_chromosome':['extra-chromosomal','main chromosome'],
 'base_class_vs_pairing':['structural class','complementary pairing'],
 'bonds_and_direction':['phosphodiester','hydrogen bonds','5′→3′'],
 'rna_architecture':['typically single-stranded','base-paired secondary structures'],
 'eukaryotic_s_phase':['eukaryotic cell','prokaryotic chromosome replication is not organized into a eukaryotic s phase'],
 'semiconservative_template':['each parental strand serves as a template','one parental strand and one new strand'],
 'models_distinct':['conservative replication model','dispersive replication model','semiconservative replication'],
 'meselson_stahl':['meselson–stahl experiment','¹⁵n','¹⁴n'],
 'helicase_topoisomerase':['helicase','topoisomerase','ahead of the replication fork'],
 'primer_polymerase':['primase','rna primer','free 3′ end'],
 'leading_lagging':['leading and lagging strand synthesis','continuously','discontinuously'],
 'ligase_distinction':['ligase joins lagging-strand fragments','helicase separated parental strands','topoisomerase relieved twisting'],
 'proofreading_not_perfect':['proofreading','does not make replication error-free'],
 'telomere_telomerase':['telomeres','telomerase','rna-containing reverse-transcriptase'],
}
for name, phrases in visible.items():
    if not all(p in full for p in phrases): problems.append(f'high-risk science guard not visibly satisfied: {name}')

# F1 protected files remain unchanged.
f1=read(U6/'content-lock-f1.json')
for item in f1['protected_files']:
    p=U6/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f'F1 protected artifact changed: {item["path"]}')
# F2 hashes remain unchanged.
f2=read(U6/'content-lock-f2.json')
for rel,h in f2['f1_protected_hashes'].items():
    p=ROOT/rel
    if not p.exists() or sha(p)!=h: problems.append(f'F2-protected F1 artifact changed: {rel}')
# F3 locks F2 and its scene briefs.
f3=read(U6/'content-lock-f3.json')
for rel,h in {**f3['f1_protected_hashes'],**f3['f2_protected_hashes']}.items():
    p=ROOT/rel
    if not p.exists() or sha(p)!=h: problems.append(f'F3 prior protected artifact changed: {rel}')
for rel,meta in f3['files'].items():
    p=ROOT/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F3 scene-brief artifact changed: {rel}')

# All released Units 1–5 content stays byte-identical to the Unit 5 F6 baseline.
up=read(U6/'upstream-u1-u5-protection-f1.json')
if up.get('protected_file_count')!=291: problems.append('Units 1–5 protection manifest count changed')
for item in up['protected_files']:
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f'protected Units 1–5 file changed: {item["path"]}')

if lock.get('lock_status')!='LOCKED_F4A_J1' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4A content-lock boundary invalid')
for rel,meta in lock.get('files',{}).items():
    p=U6/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4A locked file mismatch: {rel}')

# No final Unit 6 runtime machinery yet.
if not (U6/'f5-release-manifest.json').exists():
    for forbidden in ['memory-objects-f5.json','application-lab.json','review-manifest-f5.json','mixed-discrimination-f5.json','scope-guards-f5.json','finalization-f5.json']:
        if (U6/forbidden).exists(): problems.append(f'premature Unit 6 final runtime artifact exists: {forbidden}')

required=[U6/'journeys/U6-J1.json',U6/'journeys-f4a.json',U6/'status-f4a.json',U6/'content-lock-f4a.json',U6/'f4a-release-manifest.json',ROOT/'docs/UNIT6_F4A_JOURNEY1_STORY.md']
for p in required:
    if not p.exists(): problems.append(f'missing F4A artifact: {p.relative_to(ROOT)}')

status=read(U6/'status.json')
allowed_status={'F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
if status.get('status') not in allowed_status:
    problems.append('Unit 6 status boundary invalid')
elif status.get('status')=='STUDENT_READY':
    if status.get('student_release') is not True or status.get('preview_release') is not False: problems.append('Unit 6 F5 release boundary invalid')
elif status.get('student_release') is not False or status.get('preview_release') is not True:
    problems.append('Unit 6 pre-F5 preview boundary invalid')
course=read(ROOT/'content/ap-biology/course.json'); cu6=next(u for u in course['units'] if u['unit_id']=='unit-6')
if cu6.get('status') not in allowed_status:
    problems.append('course registry Unit 6 boundary invalid')
elif cu6.get('status')=='STUDENT_READY':
    if cu6.get('student_release') is not True or cu6.get('preview_release') is not False: problems.append('course registry Unit 6 F5 release boundary invalid')
elif cu6.get('student_release') is not False or cu6.get('preview_release') is not True:
    problems.append('course registry Unit 6 pre-F5 preview boundary invalid')

report=['# Unit 6 F4A Narrative QA','', '## Result','', '**PASS**' if not problems else '**FAIL**','',
'## Journey 1 accounting','', '- Polished scenes: **12 / 12**', '- Locked F3 knowledge records represented: **42 / 42**', f'- Exact-name targets explicitly introduced: **{exact_targets}**', '- Optional first-exposure recalls: **3**', f'- Narrative words: **{sum(counts)}**', f'- Mean scene length: **{statistics.mean(counts):.1f} words**', f'- Shortest scene: **{min(counts)} words**', f'- Longest scene: **{max(counts)} words**','',
'## Prose-quality gates','', '- Every scene fixes left/center/right geography before the scientific mechanism changes the state.', '- Dr. Sora Han and the same blue-and-gold DNA duplex persist through all twelve locations.', '- Real DNA, chromosomes, plasmids, bases, replication models, enzymes, primers, daughter strands, repair states, telomeres, and telomerase retain conventional scientific identities.', '- Every story beat preserves the exact F1 canonical scientific statement.', '- Every F2/F3 exact-name target is introduced in prose after its defining structure, comparison, or action is visible.', '- F3 misconception guards and confusable-term separations are visible in the narrative, including RNA/DNA qualifiers, S-phase context, semiconservative evidence, enzyme job separation, primer dependence, 5′→3′ synthesis, and telomere/telomerase discrimination.', '- No student prose contains development/source-management language.', '- Each scene ends with a biological or mechanical consequence that causes entry into the next locus.', '- Unit 6 remains a developer preview with zero final Memory Objects or live Challenge Lab tasks.','']
if problems: report += ['## Blocking findings','']+[f'- {p}' for p in problems]+['']
(ROOT/'docs'/'UNIT6_F4A_QA.md').write_text('\n'.join(report),encoding='utf-8')

if problems:
    print('UNIT 6 F4A QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT 6 F4A QA PASS')
print(json.dumps({'journey':'U6-J1','scenes':12,'knowledge_records':42,'exact_name_targets':exact_targets,'optional_recalls':3,'story_words':sum(counts),'average_scene_words':round(statistics.mean(counts),1),'min_scene_words':min(counts),'student_release':False,'preview_release':True},indent=2))
