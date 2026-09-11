from __future__ import annotations
import json,re,statistics,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content/ap-biology/unit-4'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

journey=read(U4/'journeys/U4-J3.json')
registry=read(U4/'journeys-f4c.json'); status=read(U4/'status-f4c.json'); manifest=read(U4/'f4c-release-manifest.json'); lock=read(U4/'content-lock-f4c.json')
f3=[b for b in read(U4/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U4-J3']
canon={r['knowledge_id']:r for r in read(U4/'source/canonical-unit4-f1.json')['canonical_catalog']}
problems=[]

if journey.get('student_release')!='DEVELOPER_PREVIEW_F4C': problems.append('Journey 3 must remain developer preview only')
if journey.get('scene_count')!=7 or len(journey.get('scenes',[]))!=7: problems.append('Journey 3 scene count must be 7')
if journey.get('checkpoint_count')!=3: problems.append('Journey 3 checkpoint count must be 3')
if registry.get('journey_count')!=3 or registry.get('scene_count')!=19 or registry.get('checkpoint_count')!=8: problems.append('F4C registry accounting mismatch')
if [x.get('palace_id') for x in registry.get('guided_journeys',[])]!=['U4-J1','U4-J2','U4-J3']: problems.append('F4C registry order must preserve Journeys 1–3')
if status.get('student_release') is not False or status.get('preview_release') is not True: problems.append('Unit 4 F4C release boundary is wrong')
if status.get('narrative_lock')!='LOCKED_F4C_J1_J2_J3': problems.append('F4C narrative lock missing')
if status.get('polished_journeys')!=3 or status.get('polished_scenes')!=19: problems.append('F4C status prose accounting mismatch')
if any(status.get(k,0)!=0 for k in ['memory_objects','application_challenges']): problems.append('F4C prematurely created student runtime artifacts')

# Locked predecessors from F4B must remain byte-identical.
old=read(U4/'content-lock-f4b.json')
for rel in ('journeys/U4-J1.json','journeys/U4-J2.json'):
    p=U4/rel; meta=old['files'][rel]
    if p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4C changed locked predecessor {rel}')

expected_loci=[b['scene_title'] for b in f3]
if [s['locus'] for s in journey['scenes']]!=expected_loci: problems.append('F4C Journey 3 route changed from F3')
assigned=[]; word_counts=[]
prohibited=('ppt','ced','campbell','college board','canonical record','source material','teacher deck','teacher test','review flag','locked definition','scope guard','f1','f2','f3','f4a','f4b','f4c')
aliases={
 'U4-K-076':['cyclic amp','camp','cyclic adenosine monophosphate'],
 'U4-K-089':['apoptosis as a signaling outcome','apoptosis as one possible cellular response','programmed cell death'],
}
for i,(s,b) in enumerate(zip(journey['scenes'],f3)):
    lid=b['locus_id']; assigned.extend(s.get('object_ids',[]))
    words=len(re.findall(r"\b[\w’'-]+\b",' '.join(s.get('story_paragraphs',[])))); word_counts.append(words)
    if s.get('locus_id')!=lid: problems.append(f'{lid} locus id changed')
    zones=s.get('scene_layout',{}).get('zones',[])
    if [z.get('position') for z in zones]!=['left','center','right']: problems.append(f'{lid} geometry order is not left/center/right')
    if any(len(z.get('description',''))<90 for z in zones): problems.append(f'{lid} spatial zone description is too thin')
    if s.get('cast',[{}])[0].get('name')!='Dr. Mira Chen': problems.append(f'{lid} loses recurring guide')
    if not any(c.get('name')=='Violet information trace' for c in s.get('cast',[])): problems.append(f'{lid} loses continuity trace')
    text=' '.join(s.get('story_paragraphs',[])); low=text.casefold()
    if 'left' not in low or ('ahead' not in low and 'center' not in low) or 'right' not in low: problems.append(f'{lid} prose does not reconstruct left/center/right geography')
    if 'violet' not in low: problems.append(f'{lid} does not visibly carry the information trace')
    if words<400: problems.append(f'{lid} has only {words} narrative words')
    bad=[x for x in prohibited if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',low)]
    if bad: problems.append(f'{lid} exposes source/development language {bad}')
    for t in b['term_introductions']:
        opts=aliases.get(t['knowledge_id'],[t['canonical_term'].casefold()])
        if not any(o in low for o in opts): problems.append(f"{lid} does not naturally introduce {t['canonical_term']}")
    if len(s.get('story_close',''))<100: problems.append(f'{lid} close is too terse')
    if s.get('misconception_guards')!=b.get('misconception_guards'): problems.append(f'{lid} misconception guards changed from F3')
    if len(s.get('story_beats',[]))!=len(b.get('term_introductions',[])): problems.append(f'{lid} story beat count differs from F3 term introductions')
    else:
        for beat,t in zip(s['story_beats'],b['term_introductions']):
            if beat.get('object_id')!=t.get('knowledge_id'): problems.append(f'{lid} story beat id order changed')
            if beat.get('science')!=t.get('canonical_science'): problems.append(f"{lid} altered canonical science for {t.get('knowledge_id')}")
            if beat.get('science')!=canon[t['knowledge_id']]['canonical_verified_statement']: problems.append(f"{lid} science no longer matches F1 for {t.get('knowledge_id')}")
            if bool(beat.get('exact_name'))!=bool(t.get('exact_name_recall')): problems.append(f"{lid} exact-name flag changed for {t.get('knowledge_id')}")
    expected_next=f3[i+1]['scene_title'] if i+1<len(f3) else None
    if s.get('next_locus')!=expected_next: problems.append(f'{lid} next locus does not follow locked route')
    if len(s.get('causal_transition',''))<100: problems.append(f'{lid} causal transition is too thin')
    if bool(s.get('checkpoint'))!=bool(b.get('quick_recall',{}).get('enabled')): problems.append(f'{lid} checkpoint placement changed from F3')
    if s.get('checkpoint') and (not s.get('checkpoint_prompt') or not s.get('checkpoint_answer') or len(s.get('checkpoint_hint',''))<80): problems.append(f'{lid} optional recall is incomplete')

expected={kid for b in f3 for kid in b['knowledge_ids']}
if len(assigned)!=25 or len(set(assigned))!=25: problems.append(f'Journey 3 coverage is {len(assigned)} refs / {len(set(assigned))} unique, expected 25/25')
if set(assigned)!=expected: problems.append('Journey 3 record set differs from locked F3 assignment')
if min(word_counts)<400 or statistics.mean(word_counts)<450: problems.append(f'prose density below F4C target min={min(word_counts)} avg={statistics.mean(word_counts):.1f}')
if sum(bool(s['checkpoint']) for s in journey['scenes'])!=3: problems.append('checkpoint count differs from F3')
if journey.get('guide',{}).get('name')!='Dr. Mira Chen': problems.append('journey guide changed')
if 'seven-location climb' not in journey.get('route_orientation',''): problems.append('journey route orientation does not declare seven-location climb')
if len(journey.get('premise',''))<300 or len(journey.get('mission',''))<250 or len(journey.get('finale',''))<300: problems.append('journey-level narrative framing is too thin')

# Journey-specific scientific narrative guards.
full=' '.join(' '.join(s['story_paragraphs']) for s in journey['scenes']).casefold()
if 'ligand remains' not in full and 'ligand is still' not in full: problems.append('journey does not repeatedly keep extracellular ligand outside relay')
if 'not a molecule' not in full and 'non-molecular' not in full: problems.append('violet trace is not explicitly identified as non-molecular in prose')
if 'phosphorylation' not in full or 'dephosphorylation' not in full: problems.append('reversible phosphorylation pair is not explicit')
if 'second messenger' not in full or 'cyclic adenosine monophosphate' not in full: problems.append('second messenger/cAMP mechanism is incomplete')
if 'amplification' not in full: problems.append('signal amplification missing')
if 'receptor mutation effect' not in full or 'downstream-component mutation effect' not in full: problems.append('mutation breakpoint discrimination missing')
if 'chemical pathway agonism/antagonism' not in full: problems.append('chemical perturbation distinction missing')

# Preserve earlier Unit 4 locks.
for lock_name in ('content-lock-f1.json','content-lock-f2.json','content-lock-f3.json','content-lock-f4a.json','content-lock-f4b.json'):
    earlier=read(U4/lock_name)
    entries=earlier.get('protected_files') or [{'path':rel,**meta} for rel,meta in earlier.get('files',{}).items()]
    for item in entries:
        rel=item['path']; q=ROOT/rel if rel.startswith('content/') else U4/rel
        if not q.exists(): problems.append(f'{lock_name} protected file missing {rel}'); continue
        if item.get('bytes') is not None and q.stat().st_size!=item['bytes']: problems.append(f'{lock_name} protected file size changed {rel}')
        if item.get('sha256') and sha(q)!=item['sha256']: problems.append(f'{lock_name} protected file hash changed {rel}')

if lock.get('lock_status')!='LOCKED_F4C_J1_J2_J3' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4C content lock boundary is wrong')
for rel,meta in lock.get('files',{}).items():
    q=U4/rel
    if not q.exists() or q.stat().st_size!=meta['bytes'] or sha(q)!=meta['sha256']: problems.append(f'F4C locked file mismatch {rel}')

for forbidden in [U4/'memory-objects.json']:
    if forbidden.exists(): problems.append(f'premature later-stage artifact exists {forbidden.relative_to(ROOT)}')

required_files=[U4/'journeys/U4-J1.json',U4/'journeys/U4-J2.json',U4/'journeys/U4-J3.json',U4/'journeys-f4c.json',U4/'status-f4c.json',U4/'content-lock-f4c.json',U4/'f4c-release-manifest.json',ROOT/'docs/UNIT4_F4C_JOURNEY3_STORY.md',ROOT/'docs/UNIT4_F4C_RELEASE.md']
for q in required_files:
    if not q.exists(): problems.append(f'missing F4C artifact {q.relative_to(ROOT)}')

course=read(ROOT/'content/ap-biology/course.json'); cu4=next(u for u in course['units'] if u['unit_id']=='unit-4')
if cu4.get('status')!='F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW' or cu4.get('student_release') is not False or cu4.get('preview_release') is not True: problems.append('course registry F4C preview state mismatch')
if cu4.get('journey_count')!=3 or cu4.get('scene_count')!=19: problems.append('course registry F4C journey accounting mismatch')

report=['# Unit 4 F4C Narrative QA','', '## Result','', '**PASS**' if not problems else '**FAIL**','', '## Journey 3 accounting','', '- Journeys 1–2 protected byte-for-byte from F4B: **PASS**' if not any('predecessor' in p or 'F4B' in p and 'hash' in p for p in problems) else '- Journeys 1–2 protected from F4B: **FAIL**', '- Polished Journey 3 scenes: **7 / 7**', f'- Locked Journey 3 knowledge records represented: **{len(set(assigned))} / 25**', '- Optional first-exposure recalls: **3**', f'- Journey 3 narrative words: **{sum(word_counts)}**', f'- Mean Journey 3 scene length: **{statistics.mean(word_counts):.1f} words**', f'- Shortest Journey 3 scene: **{min(word_counts)} words**','', '## Prose-level gates','', '- Every scene fixes left/center/right geography before the diagnostic mechanism moves.', '- Dr. Mira Chen and the non-molecular violet information trace persist through all seven locations.', '- The extracellular ligand remains at the receptor while intracellular components carry the relay through molecular state changes.', '- Protein kinase and protein phosphatase are retrieved as phosphate-addition versus phosphate-removal chemistry, without universal on/off claims.', '- Phosphorylation cascade, second messenger, cAMP, amplification, and cellular response remain physically and verbally distinct.', '- Cellular response branches keep membrane transport, metabolism, gene expression, phenotype, and apoptosis as different outcomes.', '- Receptor mutations and downstream-component mutations have different breakpoint locations.', '- Defective-phosphatase reasoning stays target-dependent.', '- Chemical activation/inhibition is distinguished from genetic mutation.', '- Every F3 knowledge record retains its exact F1 canonical science in the story-beat layer.', '- F1 misconception corrections remain attached to corresponding scenes.', '- Every scene ends with a causal reason to enter the next locus.', '- Unit 4 remains a developer preview and is not student released.','']
if problems: report += ['## Blocking findings','']+[f'- {p}' for p in problems]+['']
(ROOT/'docs/UNIT4_F4C_QA.md').write_text('\n'.join(report),encoding='utf-8')
if problems:
    print('UNIT 4 F4C QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT 4 F4C QA PASS')
print(json.dumps({'journey':'U4-J3','scenes':7,'knowledge_records':25,'optional_recalls':3,'story_words':sum(word_counts),'average_scene_words':round(statistics.mean(word_counts),1),'min_scene_words':min(word_counts),'journeys_1_2_unchanged':True,'student_release':False,'preview_release':True},indent=2))
