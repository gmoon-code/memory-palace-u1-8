from __future__ import annotations
import json, hashlib, re, statistics, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content/ap-biology/unit-4'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

f3=read(U4/'briefs/scene-briefs-f3.json')
f3j1=[b for b in f3['scene_briefs'] if b['journey_id']=='U4-J1']
canon={r['knowledge_id']:r for r in read(U4/'source/canonical-unit4-f1.json')['canonical_catalog']}
journey=read(U4/'journeys/U4-J1.json')
registry=read(U4/'journeys-f4a.json')
status=read(U4/'status-f4a.json')
manifest=read(U4/'f4a-release-manifest.json')
lock=read(U4/'content-lock-f4a.json')

problems=[]
if journey.get('palace_id')!='U4-J1': problems.append('wrong journey id')
if journey.get('scene_count')!=6 or len(journey.get('scenes',[]))!=6: problems.append('Journey 1 must contain exactly 6 scenes')
if journey.get('checkpoint_count')!=2: problems.append('Journey 1 must contain exactly 2 optional first-exposure recalls')
if journey.get('student_release')!='DEVELOPER_PREVIEW_F4A': problems.append('Journey 1 must remain developer preview only')
if registry.get('journey_count')!=1 or registry.get('scene_count')!=6 or registry.get('checkpoint_count')!=2: problems.append('F4A registry accounting mismatch')
if status.get('student_release') is not False or status.get('preview_release') is not True: problems.append('Unit 4 F4A release boundary is wrong')
if status.get('narrative_lock')!='LOCKED_F4A_J1': problems.append('F4A narrative lock missing')
if status.get('polished_journeys')!=1 or status.get('polished_scenes')!=6: problems.append('F4A status prose accounting mismatch')
if any(status.get(k,0)!=0 for k in ['memory_objects','application_challenges']): problems.append('F4A prematurely created student runtime artifacts')

expected_loci=[b['scene_title'] for b in f3j1]
if [s['locus'] for s in journey['scenes']]!=expected_loci: problems.append('F4A scene route changed from F3')

required={
'U4-L01':['direct or distance communication','cell communication','survival','growth','development'],
'U4-L02':['direct contact','gap junction','plasmodesmata','antigen-presenting cell','t cell'],
'U4-L03':['short-distance local regulators','local signaling','local regulator','ligand','target cell','paracrine signaling','growth factor'],
'U4-L04':['synaptic signaling','neurotransmitter','synaptic cleft','presynaptic','postsynaptic'],
'U4-L05':['long-distance signaling','hormone','endocrine signaling','circulation','insulin','pancreatic beta cell'],
'U4-L06':['plant long-distance hormone signaling','vascular','ethylene','air'],
}
prohibited=('ppt','ced','campbell','college board','canonical record','source material','teacher deck','teacher test','review flag','locked definition','scope guard','f1','f2','f3')
assigned=[]; word_counts=[]
for i,(s,b) in enumerate(zip(journey['scenes'],f3j1)):
    lid=b['locus_id']
    if s.get('locus_id')!=lid: problems.append(f'{lid} locus id mismatch')
    if s.get('object_ids')!=b.get('knowledge_ids'): problems.append(f'{lid} knowledge assignment changed from F3')
    assigned += s.get('object_ids',[])
    zones=s.get('scene_layout',{}).get('zones',[])
    if [z.get('position') for z in zones]!=['left','center','right']: problems.append(f'{lid} left/center/right geometry missing')
    if any(len(z.get('description',''))<90 for z in zones): problems.append(f'{lid} zone descriptions are too thin')
    if len(s.get('scene_layout',{}).get('orientation',''))<150: problems.append(f'{lid} orientation is too thin')
    cast=s.get('cast',[])
    if len(cast)<5: problems.append(f'{lid} cast does not preserve guide, three scientific parts, and route card')
    if not cast or cast[0].get('name')!='Dr. Mira Chen': problems.append(f'{lid} lost persistent guide')
    if not any(c.get('name')=='Transparent route card' for c in cast): problems.append(f'{lid} lost continuity object')
    if any(not c.get('visual') or len(c.get('visual',''))<25 or not c.get('job') or len(c.get('job',''))<25 for c in cast): problems.append(f'{lid} cast identity/job is underspecified')
    paras=s.get('story_paragraphs',[]); prose=' '.join(paras); low=prose.lower().replace('**','')
    wc=len(re.findall(r"\b[\w’'-]+\b",prose)); word_counts.append(wc)
    if wc<400: problems.append(f'{lid} has only {wc} narrative words')
    if len(paras)<5: problems.append(f'{lid} has fewer than 5 narrative paragraphs')
    if 'left' not in paras[0].lower() or ('ahead' not in paras[0].lower() and 'center' not in paras[0].lower()) or 'right' not in paras[0].lower(): problems.append(f'{lid} opening paragraph does not establish left/center/right geography')
    if 'mira' not in low: problems.append(f'{lid} does not visibly use the recurring guide')
    if 'route card' not in low: problems.append(f'{lid} does not use the continuity route card')
    bad=[x for x in prohibited if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',low)]
    if bad: problems.append(f'{lid} exposes source/development language {bad}')
    for term in required[lid]:
        if term not in low: problems.append(f'{lid} does not naturally introduce required term/relationship {term}')
    if len(s.get('story_close',''))<100: problems.append(f'{lid} close is too terse')
    if s.get('misconception_guards')!=b.get('misconception_guards'): problems.append(f'{lid} misconception guards changed from F3')
    if len(s.get('story_beats',[]))!=len(b.get('term_introductions',[])): problems.append(f'{lid} story beat count differs from F3 term introductions')
    else:
        for beat,t in zip(s['story_beats'],b['term_introductions']):
            if beat.get('object_id')!=t.get('knowledge_id'): problems.append(f'{lid} story beat id order changed')
            if beat.get('science')!=t.get('canonical_science'): problems.append(f"{lid} altered canonical science for {t.get('knowledge_id')}")
            if beat.get('science')!=canon[t['knowledge_id']]['canonical_verified_statement']: problems.append(f"{lid} science no longer matches F1 for {t.get('knowledge_id')}")
            if bool(beat.get('exact_name'))!=bool(t.get('exact_name_recall')): problems.append(f"{lid} exact-name flag changed for {t.get('knowledge_id')}")
    expected_next=f3j1[i+1]['scene_title'] if i+1<len(f3j1) else None
    if s.get('next_locus')!=expected_next: problems.append(f'{lid} next locus does not follow locked route')
    if len(s.get('causal_transition',''))<100: problems.append(f'{lid} causal transition is too thin')
    if bool(s.get('checkpoint'))!=bool(b.get('quick_recall',{}).get('enabled')): problems.append(f'{lid} checkpoint placement changed from F3')
    if s.get('checkpoint'):
        if not s.get('checkpoint_prompt') or not s.get('checkpoint_answer') or len(s.get('checkpoint_hint',''))<80: problems.append(f'{lid} optional recall is incomplete')

if len(assigned)!=23 or len(set(assigned))!=23: problems.append(f'Journey 1 coverage is {len(assigned)} refs / {len(set(assigned))} unique, expected 23/23')
expected={kid for b in f3j1 for kid in b['knowledge_ids']}
if set(assigned)!=expected: problems.append('Journey 1 record set differs from locked F3 assignment')
if min(word_counts)<400 or statistics.mean(word_counts)<450: problems.append(f'prose density below F4A target min={min(word_counts)} avg={statistics.mean(word_counts):.1f}')
if sum(bool(s['checkpoint']) for s in journey['scenes'])!=2: problems.append('checkpoint count differs from F3')
if journey.get('guide',{}).get('name')!='Dr. Mira Chen': problems.append('journey guide changed')
if 'six-location route' not in journey.get('route_orientation',''): problems.append('journey route orientation does not declare the six-location route')
if len(journey.get('premise',''))<250 or len(journey.get('mission',''))<150 or len(journey.get('finale',''))<180: problems.append('journey-level narrative framing is too thin')

# Verify earlier Unit 4 locks remain byte-for-byte protected.
for lock_name in ('content-lock-f1.json','content-lock-f2.json','content-lock-f3.json'):
    earlier=read(U4/lock_name)
    entries=earlier.get('protected_files') or [{'path':rel,**meta} for rel,meta in earlier.get('files',{}).items()]
    for item in entries:
        rel=item['path']; p=ROOT/rel if rel.startswith('content/') else U4/rel
        if not p.exists(): problems.append(f'{lock_name} protected file missing {rel}'); continue
        if item.get('bytes') is not None and p.stat().st_size!=item['bytes']: problems.append(f'{lock_name} protected file size changed {rel}')
        if item.get('sha256') and sha(p)!=item['sha256']: problems.append(f'{lock_name} protected file hash changed {rel}')

if lock.get('lock_status')!='LOCKED_F4A_J1' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4A content lock boundary is wrong')
for rel,meta in lock.get('files',{}).items():
    p=U4/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4A locked file mismatch {rel}')

# F4A itself must not create student runtime artifacts. Later narrative-stage artifacts may coexist
# in a mainline repository and are validated by their own stage locks.
for forbidden in [U4/'memory-objects.json']:
    if forbidden.exists(): problems.append(f'premature student-runtime artifact exists {forbidden.relative_to(ROOT)}')

required_files=[U4/'journeys'/'U4-J1.json',U4/'journeys-f4a.json',U4/'status-f4a.json',U4/'content-lock-f4a.json',U4/'f4a-release-manifest.json',ROOT/'docs'/'UNIT4_F4A_JOURNEY1_STORY.md',ROOT/'docs'/'UNIT4_F4A_RELEASE.md']
for p in required_files:
    if not p.exists(): problems.append(f'missing F4A artifact {p.relative_to(ROOT)}')

course=read(ROOT/'content/ap-biology/course.json'); cu4=next(u for u in course['units'] if u['unit_id']=='unit-4')
if cu4.get('status')!='F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW' or cu4.get('student_release') is not False or cu4.get('preview_release') is not True: problems.append('course registry F4A preview state mismatch')
if cu4.get('journey_count')!=1 or cu4.get('scene_count')!=6: problems.append('course registry F4A journey accounting mismatch')

report=['# Unit 4 F4A Narrative QA','', '## Result','', '**PASS**' if not problems else '**FAIL**','', '## Journey 1 accounting','', f'- Polished scenes: **6 / 6**', f'- Locked knowledge records represented: **{len(set(assigned))} / 23**', f'- Optional first-exposure recalls: **2**', f'- Narrative words: **{sum(word_counts)}**', f'- Mean scene length: **{statistics.mean(word_counts):.1f} words**', f'- Shortest scene: **{min(word_counts)} words**','', '## Prose-level gates','', '- Every scene opens by fixing the learner in left/center/right geography.', '- Dr. Mira Chen and the transparent route card persist across all six locations.', '- Biological mechanisms carry the memorable action; no unrelated mnemonic mascot replaces a scientific structure.', '- Every F3 knowledge record retains its F1 canonical science statement in the story-beat layer.', '- F1 misconception corrections remain attached to the corresponding scenes.', '- Each scene ends with a causal physical reason to enter the next locus.', '- Source-management and development language is absent from student prose.', '- Unit 4 remains a developer preview and is not student released.','']
if problems:
    report += ['## Blocking findings','']+[f'- {p}' for p in problems]+['']
(ROOT/'docs'/'UNIT4_F4A_QA.md').write_text('\n'.join(report),encoding='utf-8')

if problems:
    print('UNIT 4 F4A QA FAIL')
    print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT 4 F4A QA PASS')
print(json.dumps({'journey':'U4-J1','scenes':6,'knowledge_records':23,'optional_recalls':2,'story_words':sum(word_counts),'average_scene_words':round(statistics.mean(word_counts),1),'min_scene_words':min(word_counts),'student_release':False,'preview_release':True},indent=2))
