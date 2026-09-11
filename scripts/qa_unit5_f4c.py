from __future__ import annotations
import json,hashlib,re,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

problems=[]
j3=read(U5/'journeys/U5-J3.json')
f3=[b for b in read(U5/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U5-J3']
canon={r['knowledge_id']:r for r in read(U5/'source/canonical-unit5-f1.json')['canonical_catalog']}
lock=read(U5/'content-lock-f4c.json')

if j3.get('palace_id')!='U5-J3' or j3.get('scene_count')!=4 or len(j3.get('scenes',[]))!=4: problems.append('Journey 3 accounting is not 4 scenes')
if j3.get('checkpoint_count')!=2: problems.append('Journey 3 checkpoint count is not 2')
if [s.get('locus_id') for s in j3.get('scenes',[])]!=[f'U5-L{i:02d}' for i in range(16,20)]: problems.append('Journey 3 route differs from locked F3 order')
if j3.get('guide',{}).get('name')!='Dr. Imani Reyes': problems.append('Journey 3 guide changed')
if 'four-location diagnostic center' not in j3.get('route_orientation',''): problems.append('Journey 3 route orientation is not explicit')
if len(j3.get('premise',''))<300 or len(j3.get('mission',''))<350 or len(j3.get('finale',''))<350: problems.append('Journey 3 framing is too thin')

prohibited=['ppt','ced','campbell','source lock','source-lock','review flag','assessment-management','teacher slide','canonical catalog']
assigned=[]; word_counts=[]
for idx,(s,b) in enumerate(zip(j3['scenes'],f3)):
    lid=b['locus_id']; assigned.extend(s.get('object_ids',[]))
    if s.get('locus_id')!=lid: problems.append(f'{lid} locus id changed')
    if s.get('object_ids')!=b.get('knowledge_ids'): problems.append(f'{lid} record assignment differs from F3')
    zones=s.get('scene_layout',{}).get('zones',[])
    if [z.get('position') for z in zones]!=['left','center','right']: problems.append(f'{lid} geometry order is not left/center/right')
    if len(zones)!=3 or any(len(z.get('description',''))<120 for z in zones): problems.append(f'{lid} spatial zone descriptions are too thin')
    cast=s.get('cast',[])
    if not cast or cast[0].get('name')!='Dr. Imani Reyes': problems.append(f'{lid} loses recurring guide')
    if not any(c.get('name')=='Chromosome-outcome scanner' for c in cast): problems.append(f'{lid} loses outcome scanner continuity object')
    if not any(c.get('name')=='Gold generation ledger' for c in cast): problems.append(f'{lid} loses gold ledger continuity')
    text=' '.join(s.get('story_paragraphs',[])); low=text.casefold().replace('**','')
    words=len(re.findall(r"\b[\w’'-]+\b",text)); word_counts.append(words)
    if words<550: problems.append(f'{lid} has only {words} narrative words')
    if len(s.get('story_paragraphs',[]))<7: problems.append(f'{lid} has fewer than 7 narrative paragraphs')
    opening=s['story_paragraphs'][0].casefold()
    if 'left' not in opening or ('ahead' not in opening and 'center' not in opening) or 'right' not in opening: problems.append(f'{lid} opening does not establish left/center/right geography')
    if 'chromosome-outcome scanner' not in low: problems.append(f'{lid} does not visibly carry the outcome scanner')
    if 'gold ledger' not in low: problems.append(f'{lid} does not visibly carry the ledger')
    if ':' in text: problems.append(f'{lid} uses colon punctuation in narrative prose')
    if '—' in text: problems.append(f'{lid} uses em dash in narrative prose')
    bad=[x for x in prohibited if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',low)]
    if bad: problems.append(f'{lid} exposes source/development language {bad}')
    if len(s.get('story_close',''))<120: problems.append(f'{lid} story close is too terse')
    if s.get('misconception_guards')!=b.get('misconception_guards'): problems.append(f'{lid} misconception guards changed from F3')
    if s.get('causal_transition')!=b.get('causal_transition',{}).get('transition_logic'): problems.append(f'{lid} causal transition changed from F3')
    expected_next=f3[idx+1]['scene_title'] if idx+1<len(f3) else None
    if s.get('next_locus')!=expected_next: problems.append(f'{lid} next locus changed from F3 route')
    if bool(s.get('checkpoint'))!=bool(b.get('quick_recall',{}).get('enabled')): problems.append(f'{lid} checkpoint placement changed from F3')
    if s.get('checkpoint'):
        if s.get('checkpoint_prompt')!=b['quick_recall'].get('candidate_prompt'): problems.append(f'{lid} checkpoint prompt changed')
        if s.get('checkpoint_answer')!=b['quick_recall'].get('answer'): problems.append(f'{lid} checkpoint answer changed')
        if len(s.get('checkpoint_hint',''))<90: problems.append(f'{lid} checkpoint hint is too thin')
    if len(s.get('story_beats',[]))!=len(b.get('term_introductions',[])): problems.append(f'{lid} story beat count differs from F3 terms')
    else:
        for beat,t in zip(s['story_beats'],b['term_introductions']):
            kid=t['knowledge_id']
            if beat.get('object_id')!=kid: problems.append(f'{lid} story beat order changed for {kid}')
            if beat.get('science')!=t['canonical_science'] or beat.get('science')!=canon[kid]['canonical_verified_statement']: problems.append(f'{lid} canonical science changed for {kid}')
            if beat.get('term','').casefold() not in low: problems.append(f"{lid} exact term/relationship missing from prose: {beat.get('term')}")
            if bool(beat.get('exact_name'))!=bool(t.get('exact_name_recall')): problems.append(f'{lid} exact-name flag changed for {kid}')

expected={kid for b in f3 for kid in b['knowledge_ids']}
if len(assigned)!=8 or len(set(assigned))!=8 or set(assigned)!=expected: problems.append(f'Journey 3 record coverage mismatch refs={len(assigned)} unique={len(set(assigned))}')
if statistics.mean(word_counts)<620 or min(word_counts)<550: problems.append(f'Journey 3 prose density below F4C target avg={statistics.mean(word_counts):.1f}, min={min(word_counts)}')
if sum(bool(s['checkpoint']) for s in j3['scenes'])!=2: problems.append('Journey 3 recall count differs from F3')

full=' '.join(' '.join(s['story_paragraphs']) for s in j3['scenes']).casefold().replace('**','')
required_groups={
 'three_diversity_sources':['crossing over','independent orientation','random fertilization'],
 'recombinant_not_count_error':['recombinant chromosome','chromosome number is abnormal'],
 'scanner_mode_switch':['diversity mode','segregation-integrity mode'],
 'nondisjunction_cause':['nondisjunction','failure','segregate'],
 'aneuploidy_outcome':['aneuploidy','extra or missing','individual chromosomes'],
 'ploidy_distinction':['ploidy','complete chromosome sets'],
 'karyotype_limit':['karyotype','does not replay','nondisjunction'],
 'trisomy_case':['trisomy 21','three copies of chromosome 21','down syndrome'],
 'case_not_definition':['one specific','aneuploid','definition'],
}
for name,phrases in required_groups.items():
    if not all(p in full for p in phrases): problems.append(f'high-risk Journey 3 continuity guard missing from prose: {name}')
# Timing of mechanisms must be explicit.
if 'crossing over and independent orientation occur during meiosis' not in full: problems.append('timing guard missing: crossing over and independent orientation during meiosis')
if 'random fertilization happens afterward' not in full: problems.append('timing guard missing: random fertilization after meiosis')
# Cause vs evidence distinction must be explicit.
if 'nondisjunction is the segregation failure' not in full: problems.append('cause guard missing: nondisjunction is segregation failure')
if 'karyotype shows the resulting chromosome complement' not in full: problems.append('evidence guard missing: karyotype shows result')

# Preserve F4A Journey 1 and F4B Journey 2 byte-for-byte against their locks.
f4a=read(U5/'content-lock-f4a.json')
f4b=read(U5/'content-lock-f4b.json')
for rel in ('journeys/U5-J1.json',):
    meta=f4a['files'][rel]; p=U5/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4A locked predecessor changed {rel}')
for rel in ('journeys/U5-J2.json',):
    meta=f4b['files'][rel]; p=U5/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4B locked predecessor changed {rel}')

# Preserve all earlier F1-F3 locks and Units 1-4 baseline.
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

if lock.get('lock_status')!='LOCKED_F4C_J3' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4C content-lock boundary is wrong')
for rel,meta in lock.get('files',{}).items():
    p=U5/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4C locked file mismatch {rel}')

if not (U5/'f5-release-manifest.json').exists():
    for forbidden in [U5/'memory-objects.json',U5/'application-lab.json',U5/'review-manifest-f5.json',U5/'finalization-f5.json']:
        if forbidden.exists(): problems.append(f'premature Unit 5 student runtime artifact exists {forbidden.relative_to(ROOT)}')

course=read(ROOT/'content/ap-biology/course.json'); cu5=next(u for u in course['units'] if u['unit_id']=='unit-5')
if cu5.get('status')=='STUDENT_READY':
    if cu5.get('student_release') is not True or cu5.get('preview_release') is not False: problems.append('course registry F5 release state invalid after F4C')
elif cu5.get('status') not in {'F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW','F4G_JOURNEYS1_7_POLISHED_DEVELOPER_PREVIEW','F4H_JOURNEYS1_8_POLISHED_DEVELOPER_PREVIEW'} or cu5.get('student_release') is not False or cu5.get('preview_release') is not True: problems.append('course registry F4C preview state mismatch')
if cu5.get('journey_count',0)<3 or cu5.get('scene_count',0)<19: problems.append('course registry lost F4C accounting')

report=['# Unit 5 F4C Narrative QA','', '## Result','', '**PASS**' if not problems else '**FAIL**','', '## Journey 3 accounting','', '- Journeys 1–2 protected from F4A/F4B: **PASS**' if not any('predecessor' in p for p in problems) else '- Journeys 1–2 protected from F4A/F4B: **FAIL**', '- Polished Journey 3 scenes: **4 / 4**', f'- Locked Journey 3 knowledge records represented: **{len(set(assigned))} / 8**', '- Optional first-exposure recalls: **2**', f'- Journey 3 narrative words: **{sum(word_counts)}**', f'- Mean Journey 3 scene length: **{statistics.mean(word_counts):.1f} words**', f'- Shortest Journey 3 scene: **{min(word_counts)} words**','', '## Prose-level gates','', '- Every scene establishes left/center/right geography before the diagnostic mechanism moves.', '- Dr. Imani Reyes, the chromosome-outcome scanner, and the gold generation ledger persist through all four locations.', '- The scanner visibly switches from diversity mode to segregation-integrity mode before chromosome-number errors are introduced.', '- Crossing over, independent orientation/assortment, and random fertilization remain three physically separate diversity mechanisms.', '- Recombinant chromosome structure is separated from abnormal chromosome count.', '- Nondisjunction remains the segregation failure; aneuploidy remains the chromosome-number outcome.', '- Aneuploidy is distinguished from whole-set ploidy change.', '- Karyotype evidence displays the resulting chromosome complement and does not claim to directly show the earlier nondisjunction event.', '- Trisomy 21 remains one specific aneuploid example involving three copies of chromosome 21 and does not replace the general definitions.', '- All F3 misconception guards and both sparse recall placements remain unchanged.', '- Every assigned F3 knowledge record retains its exact F1 canonical science in the story-beat layer.', '- Student-visible narrative prose contains no source-management language, colon punctuation, or em dashes.', '- Unit 5 remains developer preview only.','']
if problems: report += ['## Blocking findings','']+[f'- {p}' for p in problems]+['']
(ROOT/'docs'/'UNIT5_F4C_QA.md').write_text('\n'.join(report),encoding='utf-8')
if problems:
    print('UNIT 5 F4C QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT 5 F4C QA PASS')
print(json.dumps({'journey':'U5-J3','scenes':4,'knowledge_records':8,'optional_recalls':2,'story_words':sum(word_counts),'average_scene_words':round(statistics.mean(word_counts),1),'min_scene_words':min(word_counts),'journeys_1_2_unchanged':True,'student_release':False,'preview_release':True},indent=2))
