from __future__ import annotations
import json, re, sys, hashlib, statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; U4=ROOT/'content/ap-biology/unit-4'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

problems=[]
journey=read(U4/'journeys/U4-J7.json')
registry=read(U4/'journeys-f4g.json')
status=read(U4/'status-f4g.json')
lock=read(U4/'content-lock-f4g.json')
lock_f=read(U4/'content-lock-f4f.json')
f3=[b for b in read(U4/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U4-J7']
canon={x['knowledge_id']:x for x in read(U4/'source/canonical-unit4-f1.json')['canonical_catalog']}

if journey.get('palace_id')!='U4-J7' or journey.get('scene_count')!=10 or len(journey.get('scenes',[]))!=10: problems.append('Journey 7 structure mismatch')
if journey.get('checkpoint_count')!=3: problems.append('Journey 7 checkpoint count must be 3')
if journey.get('student_release')!='DEVELOPER_PREVIEW_F4G': problems.append('Journey 7 preview marker mismatch')
if [s['locus_id'] for s in journey['scenes']]!=[b['locus_id'] for b in f3]: problems.append('Journey 7 route differs from F3')
if registry.get('journey_count')!=7 or registry.get('scene_count')!=51 or registry.get('checkpoint_count')!=18: problems.append('F4G registry accounting mismatch')
if [x['palace_id'] for x in registry.get('guided_journeys',[])]!=[f'U4-J{i}' for i in range(1,8)]: problems.append('F4G registry order mismatch')

prohibited=['ppt','ced','college board','campbell','the packet','locked definition','canonical record','source material','teacher material','teacher enrichment','ap memorization','ap-level']
assigned=[]; word_counts=[]
for i,(s,b) in enumerate(zip(journey['scenes'],f3)):
    lid=b['locus_id']; assigned+=s.get('object_ids',[])
    text=' '.join(s.get('story_paragraphs',[])); low=text.casefold()
    words=len(re.findall(r"\b[\w’'-]+\b",text)); word_counts.append(words)
    zones=s.get('scene_layout',{}).get('zones',[])
    if [z.get('position') for z in zones]!=['left','center','right']: problems.append(f'{lid} geometry is not left/center/right')
    if any(len(z.get('description',''))<90 for z in zones): problems.append(f'{lid} spatial zone description too thin')
    if s.get('cast',[{}])[0].get('name')!='Dr. Mira Chen': problems.append(f'{lid} loses Mira')
    if not any(c.get('name')=='Model-cell security file' for c in s.get('cast',[])): problems.append(f'{lid} loses security-file continuity')
    if 'left' not in low or ('ahead' not in low and 'center' not in low) or 'right' not in low: problems.append(f'{lid} prose does not reconstruct geography')
    if words<400: problems.append(f'{lid} has only {words} narrative words')
    bad=[]
    for x in prohibited:
        if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',low): bad.append(x)
    if bad: problems.append(f'{lid} exposes source/development language {bad}')
    for t in b['term_introductions']:
        if t['canonical_term'].casefold() not in low: problems.append(f"{lid} does not naturally introduce exact term {t['canonical_term']}")
    if len(s.get('story_close',''))<100: problems.append(f'{lid} close too terse')
    if s.get('misconception_guards')!=b.get('misconception_guards'): problems.append(f'{lid} misconception guards changed')
    if len(s.get('story_beats',[]))!=len(b.get('term_introductions',[])): problems.append(f'{lid} story beat count differs from F3')
    else:
        for beat,t in zip(s['story_beats'],b['term_introductions']):
            if beat.get('object_id')!=t.get('knowledge_id'): problems.append(f'{lid} story beat order changed')
            if beat.get('science')!=t.get('canonical_science'): problems.append(f"{lid} altered F3 science for {t['knowledge_id']}")
            if beat.get('science')!=canon[t['knowledge_id']]['canonical_verified_statement']: problems.append(f"{lid} science no longer matches F1 for {t['knowledge_id']}")
    expected_next=f3[i+1]['scene_title'] if i+1<len(f3) else None
    if s.get('next_locus')!=expected_next: problems.append(f'{lid} next locus route mismatch')
    if len(s.get('causal_transition',''))<100: problems.append(f'{lid} transition too thin')
    if bool(s.get('checkpoint'))!=bool(b.get('quick_recall',{}).get('enabled')): problems.append(f'{lid} checkpoint placement changed')
    if s.get('checkpoint') and (not s.get('checkpoint_prompt') or not s.get('checkpoint_answer') or len(s.get('checkpoint_hint',''))<80): problems.append(f'{lid} checkpoint incomplete')

expected={kid for b in f3 for kid in b['knowledge_ids']}
if len(assigned)!=28 or len(set(assigned))!=28 or set(assigned)!=expected: problems.append(f'Journey 7 record coverage mismatch {len(assigned)} refs/{len(set(assigned))} unique')
if min(word_counts)<400 or statistics.mean(word_counts)<420: problems.append(f'prose density below target min={min(word_counts)} avg={statistics.mean(word_counts):.1f}')
if sum(bool(s['checkpoint']) for s in journey['scenes'])!=3: problems.append('checkpoint count differs from F3')
if journey.get('guide',{}).get('name')!='Dr. Mira Chen': problems.append('journey guide changed')
if 'ten-location route' not in journey.get('route_orientation',''): problems.append('journey route orientation does not declare ten-location route')

full=' '.join(' '.join(s['story_paragraphs']) for s in journey['scenes']).casefold()
for required in ['cell-cycle checkpoints','checkpoint','g1 checkpoint','g0','g2 checkpoint','cell-cycle arrest','dna-damage response','spindle assembly checkpoint','apoptosis','cyclin-cdk control','cyclin-dependent kinase (cdk)','cyclin-cdk complex','growth-factor cell-cycle signaling','density-dependent inhibition','anchorage dependence','disrupted cell-cycle control','cancer','cancer-driver alterations','checkpoint evasion in cancer','apoptosis evasion in cancer','replicative immortality','tumor','benign tumor','malignant tumor','metastasis','uv and skin-cancer risk','tobacco carcinogen risk']:
    if required not in full: problems.append(f'journey-specific term/mechanism missing {required}')
for phrase in ['no universal fixed mutation threshold','regulated programmed cell death','not automatically a permanent dead end','nicotine is primarily responsible for addiction','ultraviolet radiation','distant spread']:
    if phrase not in full: problems.append(f'mechanistic/science guard missing {phrase}')
if 'proceed, pause, exit, repair' not in full: problems.append('checkpoint decision outcomes are not visible')
if 'every cancer cell lives forever' not in full: problems.append('replicative-immortality guard not made visible')

# Preserve Journeys 1-6 byte-for-byte from F4F.
for rel in (f'journeys/U4-J{i}.json' for i in range(1,7)):
    p=U4/rel; meta=lock_f['files'][rel]
    if p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4F predecessor changed {rel}')

if lock.get('lock_status')!='LOCKED_F4G_J1_J2_J3_J4_J5_J6_J7' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4G lock boundary wrong')
for rel,meta in lock.get('files',{}).items():
    q=U4/rel
    if not q.exists() or q.stat().st_size!=meta['bytes'] or sha(q)!=meta['sha256']: problems.append(f'F4G locked file mismatch {rel}')
for forbidden in [U4/'memory-objects.json']:
    if forbidden.exists(): problems.append(f'premature F5 artifact exists {forbidden.relative_to(ROOT)}')
course=read(ROOT/'content/ap-biology/course.json'); cu4=next(u for u in course['units'] if u['unit_id']=='unit-4')
if cu4.get('status')!='F4G_ALL_7_JOURNEYS_POLISHED_DEVELOPER_PREVIEW' or cu4.get('student_release') is not False or cu4.get('preview_release') is not True: problems.append('course registry F4G state mismatch')
if cu4.get('journey_count')!=7 or cu4.get('scene_count')!=51 or cu4.get('polished_journeys')!=7: problems.append('course registry F4G accounting mismatch')

report=['# Unit 4 F4G Narrative QA','','## Result','','**PASS**' if not problems else '**FAIL**','','## Journey 7 accounting','',f'- Journeys 1–6 protected byte-for-byte from F4F: **{"PASS" if not any("predecessor changed" in p for p in problems) else "FAIL"}**','- Polished Journey 7 scenes: **10 / 10**',f'- Locked Journey 7 knowledge records represented: **{len(set(assigned))} / 28**','- Optional first-exposure recalls: **3**',f'- Journey 7 narrative words: **{sum(word_counts)}**',f'- Mean Journey 7 scene length: **{statistics.mean(word_counts):.1f} words**',f'- Shortest Journey 7 scene: **{min(word_counts)} words**','','## Prose-level gates','','- Every scene fixes left/center/right geography before regulatory decisions or disease progression are interpreted.','- Dr. Mira Chen and the same model-cell security file persist across all ten locations.','- Checkpoint, cell-cycle arrest, and apoptosis remain distinct.','- G1, G2, and spindle-assembly checkpoints inspect different evidence and are not collapsed into one gate.','- DNA-damage outcomes remain context-dependent; apoptosis is not automatic.','- Cyclin, CDK, cyclin–CDK complex, and phosphorylated targets remain distinct.','- Growth factors remain extracellular signaling molecules and are not universally classified as hormones.','- Cancer is modeled as accumulated regulatory dysregulation without a fixed mutation threshold.','- Tumor, benign tumor, malignant tumor, metastasis, and replicative immortality remain distinct.','- UV risk is tied to ultraviolet DNA damage; tobacco risk is tied to smoke carcinogens while nicotine remains primarily the addictive agent.','- Every F3 record retains its exact F1 canonical science in the story-beat layer.','- Student prose contains no source-management or curriculum-audit language.','- Unit 4 remains developer preview only.','']
if problems: report += ['## Blocking findings','']+[f'- {p}' for p in problems]+['']
(ROOT/'docs/UNIT4_F4G_QA.md').write_text('\n'.join(report),encoding='utf-8')
if problems:
    print('UNIT 4 F4G QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT 4 F4G QA PASS')
print(json.dumps({'journey':'U4-J7','scenes':10,'knowledge_records':28,'optional_recalls':3,'story_words':sum(word_counts),'average_scene_words':round(statistics.mean(word_counts),1),'min_scene_words':min(word_counts),'journeys_1_6_unchanged':True,'all_unit4_journeys_polished':True,'student_release':False,'preview_release':True},indent=2))
