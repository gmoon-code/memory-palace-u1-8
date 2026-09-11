from __future__ import annotations
import json, hashlib, re, statistics, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content/ap-biology/unit-4'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

f3=read(U4/'briefs/scene-briefs-f3.json')
f3j2=[b for b in f3['scene_briefs'] if b['journey_id']=='U4-J2']
canon={r['knowledge_id']:r for r in read(U4/'source/canonical-unit4-f1.json')['canonical_catalog']}
j1=read(U4/'journeys/U4-J1.json'); journey=read(U4/'journeys/U4-J2.json')
registry=read(U4/'journeys-f4b.json'); status=read(U4/'status-f4b.json'); manifest=read(U4/'f4b-release-manifest.json'); lock=read(U4/'content-lock-f4b.json')
f4a_lock=read(U4/'content-lock-f4a.json')

problems=[]
if journey.get('palace_id')!='U4-J2': problems.append('wrong Journey 2 id')
if journey.get('scene_count')!=6 or len(journey.get('scenes',[]))!=6: problems.append('Journey 2 must contain exactly 6 scenes')
if journey.get('checkpoint_count')!=3: problems.append('Journey 2 must contain exactly 3 optional first-exposure recalls')
if journey.get('student_release')!='DEVELOPER_PREVIEW_F4B': problems.append('Journey 2 must remain developer preview only')
if registry.get('journey_count')!=2 or registry.get('scene_count')!=12 or registry.get('checkpoint_count')!=5: problems.append('F4B registry accounting mismatch')
if [x.get('palace_id') for x in registry.get('guided_journeys',[])]!=['U4-J1','U4-J2']: problems.append('F4B registry order must preserve Journey 1 then Journey 2')
if status.get('student_release') is not False or status.get('preview_release') is not True: problems.append('Unit 4 F4B release boundary is wrong')
if status.get('narrative_lock')!='LOCKED_F4B_J1_J2': problems.append('F4B narrative lock missing')
if status.get('polished_journeys')!=2 or status.get('polished_scenes')!=12: problems.append('F4B status prose accounting mismatch')
if any(status.get(k,0)!=0 for k in ['memory_objects','application_challenges']): problems.append('F4B prematurely created student runtime artifacts')

# Journey 1 must be byte-for-byte identical to F4A.
meta=f4a_lock['files']['journeys/U4-J1.json']; p=U4/'journeys/U4-J1.json'
if p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append('F4B changed locked Journey 1')

expected_loci=[b['scene_title'] for b in f3j2]
if [s['locus'] for s in journey['scenes']]!=expected_loci: problems.append('F4B Journey 2 route changed from F3')

required={
'U4-L07':['ligand','receptor','target cell','ligand-binding specificity','ligand-receptor specificity','reception','receptor conformational or state change','reception to a later cellular response'],
'U4-L08':['receptor location','cell-surface receptor','intracellular receptor','hydrophobic ligand principle','membrane permeability'],
'U4-L09':['steroid-hormone intracellular signaling','thyroid-hormone intracellular signaling','nitric-oxide intracellular signaling','nuclear receptor','soluble guanylyl cyclase'],
'U4-L10':['g protein-coupled receptor','gpcr','heterotrimeric g protein','seven-pass','separate'],
'U4-L11':['heterotrimeric g protein','gdp-to-gtp exchange','gtp hydrolysis and switch reset','effector enzyme or channel','molecular switch'],
'U4-L12':['ligand-gated ion channel','ligand-gated channels','ion-channel signaling response','electrochemical driving forces','ion flux'],
}
prohibited=('ppt','ced','campbell','college board','canonical record','source material','teacher deck','teacher test','review flag','locked definition','scope guard','f1','f2','f3','f4a','f4b')
assigned=[]; word_counts=[]
for i,(s,b) in enumerate(zip(journey['scenes'],f3j2)):
    lid=b['locus_id']
    if s.get('locus_id')!=lid: problems.append(f'{lid} locus id mismatch')
    if s.get('object_ids')!=b.get('knowledge_ids'): problems.append(f'{lid} knowledge assignment changed from F3')
    assigned += s.get('object_ids',[])
    zones=s.get('scene_layout',{}).get('zones',[])
    if [z.get('position') for z in zones]!=['left','center','right']: problems.append(f'{lid} left/center/right geometry missing')
    if any(len(z.get('description',''))<90 for z in zones): problems.append(f'{lid} zone descriptions are too thin')
    if len(s.get('scene_layout',{}).get('orientation',''))<150: problems.append(f'{lid} orientation is too thin')
    cast=s.get('cast',[])
    if len(cast)<5: problems.append(f'{lid} cast does not preserve guide, three scientific parts, and receptor monitor')
    if not cast or cast[0].get('name')!='Dr. Mira Chen': problems.append(f'{lid} lost persistent guide')
    if not any(c.get('name')=='Three-state receptor monitor' for c in cast): problems.append(f'{lid} lost continuity receptor monitor')
    if any(not c.get('visual') or len(c.get('visual',''))<25 or not c.get('job') or len(c.get('job',''))<25 for c in cast): problems.append(f'{lid} cast identity/job is underspecified')
    paras=s.get('story_paragraphs',[]); prose=' '.join(paras); low=prose.lower().replace('**','')
    wc=len(re.findall(r"\b[\w’'-]+\b",prose)); word_counts.append(wc)
    if wc<400: problems.append(f'{lid} has only {wc} narrative words')
    if len(paras)<4: problems.append(f'{lid} has fewer than 4 narrative paragraphs')
    p0=paras[0].lower()
    if 'left' not in p0 or ('ahead' not in p0 and 'center' not in p0) or 'right' not in p0: problems.append(f'{lid} opening paragraph does not establish left/center/right geography')
    if 'mira' not in low: problems.append(f'{lid} does not visibly use the recurring guide')
    if 'receptor monitor' not in low and 'three-state monitor' not in low: problems.append(f'{lid} does not use the continuity receptor monitor')
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
    expected_next=f3j2[i+1]['scene_title'] if i+1<len(f3j2) else None
    if s.get('next_locus')!=expected_next: problems.append(f'{lid} next locus does not follow locked route')
    if len(s.get('causal_transition',''))<100: problems.append(f'{lid} causal transition is too thin')
    if bool(s.get('checkpoint'))!=bool(b.get('quick_recall',{}).get('enabled')): problems.append(f'{lid} checkpoint placement changed from F3')
    if s.get('checkpoint') and (not s.get('checkpoint_prompt') or not s.get('checkpoint_answer') or len(s.get('checkpoint_hint',''))<80): problems.append(f'{lid} optional recall is incomplete')

expected={kid for b in f3j2 for kid in b['knowledge_ids']}
if len(assigned)!=24 or len(set(assigned))!=24: problems.append(f'Journey 2 coverage is {len(assigned)} refs / {len(set(assigned))} unique, expected 24/24')
if set(assigned)!=expected: problems.append('Journey 2 record set differs from locked F3 assignment')
if min(word_counts)<400 or statistics.mean(word_counts)<450: problems.append(f'prose density below F4B target min={min(word_counts)} avg={statistics.mean(word_counts):.1f}')
if sum(bool(s['checkpoint']) for s in journey['scenes'])!=3: problems.append('checkpoint count differs from F3')
if journey.get('guide',{}).get('name')!='Dr. Mira Chen': problems.append('journey guide changed')
if 'six-location route' not in journey.get('route_orientation',''): problems.append('journey route orientation does not declare the six-location route')
if len(journey.get('premise',''))<250 or len(journey.get('mission',''))<180 or len(journey.get('finale',''))<220: problems.append('journey-level narrative framing is too thin')

# Preserve every earlier Unit 4 lock.
for lock_name in ('content-lock-f1.json','content-lock-f2.json','content-lock-f3.json','content-lock-f4a.json'):
    earlier=read(U4/lock_name)
    entries=earlier.get('protected_files') or [{'path':rel,**meta} for rel,meta in earlier.get('files',{}).items()]
    for item in entries:
        rel=item['path']; q=ROOT/rel if rel.startswith('content/') else U4/rel
        if not q.exists(): problems.append(f'{lock_name} protected file missing {rel}'); continue
        if item.get('bytes') is not None and q.stat().st_size!=item['bytes']: problems.append(f'{lock_name} protected file size changed {rel}')
        if item.get('sha256') and sha(q)!=item['sha256']: problems.append(f'{lock_name} protected file hash changed {rel}')

if lock.get('lock_status')!='LOCKED_F4B_J1_J2' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4B content lock boundary is wrong')
for rel,meta in lock.get('files',{}).items():
    q=U4/rel
    if not q.exists() or q.stat().st_size!=meta['bytes'] or sha(q)!=meta['sha256']: problems.append(f'F4B locked file mismatch {rel}')

for forbidden in [U4/'memory-objects.json']:
    if forbidden.exists(): problems.append(f'premature student-runtime artifact exists {forbidden.relative_to(ROOT)}')

required_files=[U4/'journeys/U4-J1.json',U4/'journeys/U4-J2.json',U4/'journeys-f4b.json',U4/'status-f4b.json',U4/'content-lock-f4b.json',U4/'f4b-release-manifest.json',ROOT/'docs/UNIT4_F4B_JOURNEY2_STORY.md',ROOT/'docs/UNIT4_F4B_RELEASE.md']
for q in required_files:
    if not q.exists(): problems.append(f'missing F4B artifact {q.relative_to(ROOT)}')

course=read(ROOT/'content/ap-biology/course.json'); cu4=next(u for u in course['units'] if u['unit_id']=='unit-4')
if cu4.get('status')!='F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW' or cu4.get('student_release') is not False or cu4.get('preview_release') is not True: problems.append('course registry F4B preview state mismatch')
if cu4.get('journey_count')!=2 or cu4.get('scene_count')!=12: problems.append('course registry F4B journey accounting mismatch')

report=['# Unit 4 F4B Narrative QA','', '## Result','', '**PASS**' if not problems else '**FAIL**','', '## Journey 2 accounting','', '- Journey 1 protected from F4A: **PASS**' if not any('Journey 1' in p for p in problems) else '- Journey 1 protected from F4A: **FAIL**', f'- Polished Journey 2 scenes: **6 / 6**', f'- Locked Journey 2 knowledge records represented: **{len(set(assigned))} / 24**', '- Optional first-exposure recalls: **3**', f'- Journey 2 narrative words: **{sum(word_counts)}**', f'- Mean Journey 2 scene length: **{statistics.mean(word_counts):.1f} words**', f'- Shortest Journey 2 scene: **{min(word_counts)} words**','', '## Prose-level gates','', '- Every scene opens by fixing the learner in left/center/right geography.', '- Dr. Mira Chen and the three-state receptor monitor persist across all six locations.', '- Ligand, receptor, target cell, GPCR, G protein, effector, and ion channel remain separate scientific parts with distinct jobs.', '- Every F3 knowledge record retains its F1 canonical science statement in the story-beat layer.', '- Receptor location is governed by membrane-permeability reasoning without becoming an absolute hydrophobic/hydrophilic sorting rule.', '- GPCR and heterotrimeric G protein remain visibly separate; GDP/GTP state is represented as a molecular switch, not mainly as fuel.', '- Ligand-gated channel signaling remains structurally distinct from GPCR/G-protein signaling.', '- F1 misconception corrections remain attached to the corresponding scenes.', '- Each scene ends with a causal physical reason to enter the next locus.', '- Source-management and development language is absent from student prose.', '- Unit 4 remains a developer preview and is not student released.','']
if problems: report += ['## Blocking findings','']+[f'- {p}' for p in problems]+['']
(ROOT/'docs/UNIT4_F4B_QA.md').write_text('\n'.join(report),encoding='utf-8')
if problems:
    print('UNIT 4 F4B QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT 4 F4B QA PASS')
print(json.dumps({'journey':'U4-J2','scenes':6,'knowledge_records':24,'optional_recalls':3,'story_words':sum(word_counts),'average_scene_words':round(statistics.mean(word_counts),1),'min_scene_words':min(word_counts),'journey_1_unchanged':True,'student_release':False,'preview_release':True},indent=2))
