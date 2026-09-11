from __future__ import annotations
import json, hashlib, re, statistics, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

f3=read(U5/'briefs/scene-briefs-f3.json')
f3j1=[b for b in f3['scene_briefs'] if b['journey_id']=='U5-J1']
canon={r['knowledge_id']:r for r in read(U5/'source/canonical-unit5-f1.json')['canonical_catalog']}
journey=read(U5/'journeys/U5-J1.json')
registry=read(U5/'journeys-f4a.json')
status=read(U5/'status-f4a.json')
manifest=read(U5/'f4a-release-manifest.json')
lock=read(U5/'content-lock-f4a.json')
problems=[]

if journey.get('palace_id')!='U5-J1': problems.append('wrong journey id')
if journey.get('scene_count')!=5 or len(journey.get('scenes',[]))!=5: problems.append('Journey 1 must contain exactly 5 scenes')
if journey.get('checkpoint_count')!=2: problems.append('Journey 1 must contain exactly 2 optional first-exposure recalls')
if journey.get('student_release')!='DEVELOPER_PREVIEW_F4A': problems.append('Journey 1 must remain developer preview only')
if registry.get('journey_count')!=1 or registry.get('scene_count')!=5 or registry.get('checkpoint_count')!=2: problems.append('F4A registry accounting mismatch')
if status.get('student_release') is not False or status.get('preview_release') is not True: problems.append('Unit 5 F4A release boundary is wrong')
if status.get('narrative_lock')!='LOCKED_F4A_J1': problems.append('F4A narrative lock missing')
if status.get('polished_journeys')!=1 or status.get('polished_scenes')!=5: problems.append('F4A status prose accounting mismatch')
if any(status.get(k,0)!=0 for k in ['memory_objects','application_challenges']): problems.append('F4A prematurely created Unit 5 runtime artifacts')

expected_loci=[b['scene_title'] for b in f3j1]
if [s['locus'] for s in journey['scenes']]!=expected_loci: problems.append('F4A scene route changed from F3')

prohibited=('ppt','ced','campbell','college board','canonical record','source material','teacher deck','teacher test','review flag','locked definition','scope guard','f1','f2','f3','assessment crosswalk')
assigned=[]; word_counts=[]
for i,(s,b) in enumerate(zip(journey['scenes'],f3j1)):
    lid=b['locus_id']
    if s.get('locus_id')!=lid: problems.append(f'{lid} locus id mismatch')
    if s.get('object_ids')!=b.get('knowledge_ids'): problems.append(f'{lid} knowledge assignment changed from F3')
    assigned += s.get('object_ids',[])
    zones=s.get('scene_layout',{}).get('zones',[])
    if [z.get('position') for z in zones]!=['left','center','right']: problems.append(f'{lid} left/center/right geometry missing')
    if any(len(z.get('description',''))<100 for z in zones): problems.append(f'{lid} zone descriptions are too thin')
    if len(s.get('scene_layout',{}).get('orientation',''))<180: problems.append(f'{lid} orientation is too thin')
    cast=s.get('cast',[])
    if len(cast)<5: problems.append(f'{lid} cast does not preserve guide, three scientific parts, and generation ledger')
    if not cast or cast[0].get('name')!='Dr. Imani Reyes': problems.append(f'{lid} lost persistent guide')
    if not any(c.get('name')=='Gold generation ledger' for c in cast): problems.append(f'{lid} lost continuity object')
    if any(not c.get('visual') or len(c.get('visual',''))<40 or not c.get('job') or len(c.get('job',''))<60 for c in cast): problems.append(f'{lid} cast identity/job is underspecified')
    paras=s.get('story_paragraphs',[]); prose=' '.join(paras); low=prose.lower().replace('**','')
    wc=len(re.findall(r"\b[\w’'-]+\b",prose)); word_counts.append(wc)
    if wc<450: problems.append(f'{lid} has only {wc} narrative words')
    if len(paras)<5: problems.append(f'{lid} has fewer than 5 narrative paragraphs')
    if 'left' not in paras[0].lower() or ('ahead' not in paras[0].lower() and 'center' not in paras[0].lower()) or 'right' not in paras[0].lower(): problems.append(f'{lid} opening paragraph does not establish left/center/right geography')
    if 'imani' not in low: problems.append(f'{lid} does not visibly use the recurring guide')
    if 'gold generation ledger' not in low and 'generation ledger' not in low: problems.append(f'{lid} does not use the continuity ledger')
    bad=[x for x in prohibited if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',low)]
    if bad: problems.append(f'{lid} exposes source/development language {bad}')
    if len(s.get('story_close',''))<140: problems.append(f'{lid} close is too terse')
    if s.get('misconception_guards')!=b.get('misconception_guards'): problems.append(f'{lid} misconception guards changed from F3')
    if s.get('exit_memory')!=b.get('exit_memory'): problems.append(f'{lid} exit-memory contract changed from F3')
    if len(s.get('story_beats',[]))!=len(b.get('term_introductions',[])): problems.append(f'{lid} story beat count differs from F3 term introductions')
    else:
        for beat,t in zip(s['story_beats'],b['term_introductions']):
            kid=t['knowledge_id']
            if beat.get('object_id')!=kid: problems.append(f'{lid} story beat id order changed')
            if beat.get('science')!=t.get('canonical_science'): problems.append(f'{lid} altered F3 canonical science for {kid}')
            if beat.get('science')!=canon[kid]['canonical_verified_statement']: problems.append(f'{lid} science no longer matches F1 for {kid}')
            if bool(beat.get('exact_name'))!=bool(t.get('exact_name_recall')): problems.append(f'{lid} exact-name flag changed for {kid}')
            if t['canonical_term'].casefold() not in low: problems.append(f"{lid} does not explicitly introduce exact term/relationship {t['canonical_term']}")
    expected_next=f3j1[i+1]['scene_title'] if i+1<len(f3j1) else None
    if s.get('next_locus')!=expected_next: problems.append(f'{lid} next locus does not follow locked route')
    if len(s.get('causal_transition',''))<100: problems.append(f'{lid} causal transition is too thin')
    if bool(s.get('checkpoint'))!=bool(b.get('quick_recall',{}).get('enabled')): problems.append(f'{lid} checkpoint placement changed from F3')
    if s.get('checkpoint'):
        if not s.get('checkpoint_prompt') or not s.get('checkpoint_answer') or len(s.get('checkpoint_hint',''))<100: problems.append(f'{lid} optional recall is incomplete')

if len(assigned)!=20 or len(set(assigned))!=20: problems.append(f'Journey 1 coverage is {len(assigned)} refs / {len(set(assigned))} unique, expected 20/20')
expected={kid for b in f3j1 for kid in b['knowledge_ids']}
if set(assigned)!=expected: problems.append('Journey 1 record set differs from locked F3 assignment')
if min(word_counts)<450 or statistics.mean(word_counts)<500: problems.append(f'prose density below F4A target min={min(word_counts)} avg={statistics.mean(word_counts):.1f}')
if sum(bool(s['checkpoint']) for s in journey['scenes'])!=2: problems.append('checkpoint count differs from F3')
if journey.get('guide',{}).get('name')!='Dr. Imani Reyes': problems.append('journey guide changed')
if 'five-location route' not in journey.get('route_orientation',''): problems.append('journey route orientation does not declare the five-location route')
if len(journey.get('premise',''))<300 or len(journey.get('mission',''))<180 or len(journey.get('finale',''))<220: problems.append('journey-level narrative framing is too thin')

# High-risk science guards must be actually visible in prose, not merely stored as metadata.
full=' '.join(' '.join(s['story_paragraphs']) for s in journey['scenes']).lower().replace('**','')
visible_guards={
 'gene_not_protein_only':['some genes encode proteins','rna products or regulation'],
 'nearly_universal_code':['nearly universal genetic code','known variants'],
 'homolog_not_sister':['homologous chromosomes','sister chromatids','different allele'],
 'ploidy_not_dna_amount':['ploidy and dna amount','not the same measurement'],
 'clone_not_exact_forever':['perfectly identical forever','mutation'],
 'sexual_not_two_parents':['self-fertilization','two separate parent'],
 'life_cycles_vary':['life cycles vary widely among organisms','universal diagram'],
}
for name,phrases in visible_guards.items():
    if not all(p in full for p in phrases): problems.append(f'high-risk guard is not visible in narrative prose: {name}')

# Earlier Unit 5 locks remain byte-protected.
for lock_name in ('content-lock-f1.json','content-lock-f2.json','content-lock-f3.json'):
    earlier=read(U5/lock_name)
    entries=earlier.get('protected_files') or [{'path':rel,**meta} for rel,meta in earlier.get('files',{}).items()]
    for item in entries:
        rel=item['path']
        p=ROOT/rel if rel.startswith('content/') else U5/rel
        if not p.exists(): problems.append(f'{lock_name} protected file missing {rel}'); continue
        if item.get('bytes') is not None and p.stat().st_size!=item['bytes']: problems.append(f'{lock_name} protected file size changed {rel}')
        if item.get('sha256') and sha(p)!=item['sha256']: problems.append(f'{lock_name} protected file hash changed {rel}')

# Released Units 1–4 remain byte-identical to the protected baseline.
up=read(U5/'upstream-u1-u4-protection-f1.json')
if up.get('protected_file_count')!=216: problems.append('Units 1–4 protection manifest count changed')
for item in up.get('protected_files',[]):
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f"upstream Units 1–4 protected file changed {item['path']}")

if lock.get('lock_status')!='LOCKED_F4A_J1' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4A content lock boundary is wrong')
for rel,meta in lock.get('files',{}).items():
    p=U5/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4A locked file mismatch {rel}')

# F4A itself must not create final student-runtime machinery.
if not (U5/'f5-release-manifest.json').exists():
    for forbidden in [U5/'memory-objects.json',U5/'application-lab.json',U5/'review-manifest-f5.json',U5/'finalization-f5.json']:
        if forbidden.exists(): problems.append(f'premature Unit 5 student-runtime artifact exists {forbidden.relative_to(ROOT)}')
# Later gates may add Journeys 2-8; F4A only verifies Journey 1 and its frozen lock.

required_files=[U5/'journeys'/'U5-J1.json',U5/'journeys-f4a.json',U5/'status-f4a.json',U5/'content-lock-f4a.json',U5/'f4a-release-manifest.json',ROOT/'docs'/'UNIT5_F4A_JOURNEY1_STORY.md',ROOT/'docs'/'UNIT5_F4A_RELEASE.md']
for p in required_files:
    if not p.exists(): problems.append(f'missing F4A artifact {p.relative_to(ROOT)}')

course=read(ROOT/'content/ap-biology/course.json'); cu5=next(u for u in course['units'] if u['unit_id']=='unit-5')
allowed={'F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW','F4G_JOURNEYS1_7_POLISHED_DEVELOPER_PREVIEW','F4H_JOURNEYS1_8_POLISHED_DEVELOPER_PREVIEW'}
if cu5.get('status')=='STUDENT_READY':
    if cu5.get('student_release') is not True or cu5.get('preview_release') is not False: problems.append('course registry F5 release state invalid after F4A')
elif cu5.get('status') not in allowed or cu5.get('student_release') is not False or cu5.get('preview_release') is not True: problems.append('course registry no longer preserves the F4A-or-later preview boundary')
if cu5.get('journey_count',0)<1 or cu5.get('scene_count',0)<5: problems.append('course registry lost F4A Journey 1 accounting')

report=['# Unit 5 F4A Narrative QA','', '## Result','', '**PASS**' if not problems else '**FAIL**','', '## Journey 1 accounting','', '- Polished scenes: **5 / 5**', f'- Locked knowledge records represented: **{len(set(assigned))} / 20**', '- Optional first-exposure recalls: **2**', f'- Narrative words: **{sum(word_counts)}**', f'- Mean scene length: **{statistics.mean(word_counts):.1f} words**', f'- Shortest scene: **{min(word_counts)} words**','', '## Prose-level gates','', '- Every scene opens by fixing the learner in left/center/right geography.', '- Dr. Imani Reyes, the gold generation ledger, and the tracked chromosome identities persist through the five-room route.', '- Real genes, chromosomes, chromosome sets, cells, and reproductive processes carry the memorable action.', '- Every F3 knowledge record retains its exact F1 canonical science in the story-beat layer.', '- Every exact F3 term or relationship is explicitly introduced in the narrative prose after its defining action is visible.', '- High-risk F1 corrections are visible in the story itself rather than existing only as hidden metadata.', '- Each scene ends with a causal reason to enter the next locus.', '- Source-management and development language is absent from student prose.', '- Unit 5 remains a developer preview and is not student released.','']
if problems: report += ['## Blocking findings','']+[f'- {p}' for p in problems]+['']
(ROOT/'docs'/'UNIT5_F4A_QA.md').write_text('\n'.join(report),encoding='utf-8')

if problems:
    print('UNIT 5 F4A QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT 5 F4A QA PASS')
print(json.dumps({'journey':'U5-J1','scenes':5,'knowledge_records':20,'optional_recalls':2,'story_words':sum(word_counts),'average_scene_words':round(statistics.mean(word_counts),1),'min_scene_words':min(word_counts),'student_release':False,'preview_release':True},indent=2))
