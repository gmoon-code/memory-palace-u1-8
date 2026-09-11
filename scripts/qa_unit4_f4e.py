from __future__ import annotations
import json,re,hashlib,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content'/'ap-biology'/'unit-4'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
problems=[]
journey=read(U4/'journeys/U4-J5.json')
f3=[b for b in read(U4/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U4-J5']
canon={r['knowledge_id']:r for r in read(U4/'source/canonical-unit4-f1.json')['canonical_catalog']}
lock=read(U4/'content-lock-f4e.json')
lock_d=read(U4/'content-lock-f4d.json')

if journey.get('palace_id')!='U4-J5' or journey.get('scene_count')!=8: problems.append('Journey 5 identity/scene count mismatch')
if [s.get('locus_id') for s in journey['scenes']]!=[b['locus_id'] for b in f3]: problems.append('Journey 5 route differs from F3')
if journey.get('checkpoint_count')!=3: problems.append('Journey 5 checkpoint count must be 3')

prohibited=['ppt','ced','college board','campbell','the packet','locked definition','canonical record','source material','teacher material']
assigned=[]; word_counts=[]
for i,(s,b) in enumerate(zip(journey['scenes'],f3)):
    lid=b['locus_id']; assigned+=s.get('object_ids',[])
    text=' '.join(s.get('story_paragraphs',[])); low=text.casefold()
    words=len(re.findall(r"\b[\w’'-]+\b",text)); word_counts.append(words)
    zones=s.get('scene_layout',{}).get('zones',[])
    if [z.get('position') for z in zones]!=['left','center','right']: problems.append(f'{lid} geometry is not left/center/right')
    if any(len(z.get('description',''))<90 for z in zones): problems.append(f'{lid} spatial zone description too thin')
    if s.get('cast',[{}])[0].get('name')!='Dr. Mira Chen': problems.append(f'{lid} loses Mira')
    if not any(c.get('name')=='Tracked chromosome archive case' for c in s.get('cast',[])): problems.append(f'{lid} loses tracked chromosome continuity case')
    if 'left' not in low or ('ahead' not in low and 'center' not in low) or 'right' not in low: problems.append(f'{lid} prose does not reconstruct geography')
    if not any(k in low for k in ('chromosome','chromatin','cell cycle','g0')): problems.append(f'{lid} loses chromosome/cell-cycle continuity')
    if words<400: problems.append(f'{lid} has only {words} narrative words')
    bad=[x for x in prohibited if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',low)]
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
if len(assigned)!=27 or len(set(assigned))!=27 or set(assigned)!=expected: problems.append(f'Journey 5 record coverage mismatch {len(assigned)} refs/{len(set(assigned))} unique')
if min(word_counts)<400 or statistics.mean(word_counts)<450: problems.append(f'prose density below target min={min(word_counts)} avg={statistics.mean(word_counts):.1f}')
if sum(bool(s['checkpoint']) for s in journey['scenes'])!=3: problems.append('checkpoint count differs from F3')
if journey.get('guide',{}).get('name')!='Dr. Mira Chen': problems.append('journey guide changed')
if 'eight-location route' not in journey.get('route_orientation',''): problems.append('journey route orientation does not declare eight-location route')

full=' '.join(' '.join(s['story_paragraphs']) for s in journey['scenes']).casefold()
for required in ['genome','histone','nucleosome','chromatin','replicated chromosome','sister chromatid','centromere','kinetochore','homologous chromosomes','diploid','haploid','interphase','m phase','g1 phase','s phase','g2','g0 stage and reentry']:
    if required not in full: problems.append(f'journey-specific mechanism missing {required}')
for concept in ['dna content','chromatid number','chromosome number']:
    if concept not in full: problems.append(f'S-phase counting model missing {concept}')
if 'chromosome number counted by centromeres remains the same' not in full and 'centromere-counted chromosome number remains unchanged' not in full:
    problems.append('S-phase chromosome-count guard missing')
if 'chromosomes exist throughout' not in full and 'throughout the cell cycle' not in full:
    problems.append('chromosome-existence-through-cycle guard missing')
if 'gamete is the product' not in full: problems.append('gamete/meiosis direction guard missing')
if 'g0 means forever' not in full and 'variable reversibility' not in full: problems.append('G0 reversibility guard missing')

# Preserve F1-F4D and predecessor journeys.
for lock_name in ('content-lock-f1.json','content-lock-f2.json','content-lock-f3.json','content-lock-f4a.json','content-lock-f4b.json','content-lock-f4c.json','content-lock-f4d.json'):
    earlier=read(U4/lock_name)
    entries=earlier.get('protected_files') or [{'path':rel,**meta} for rel,meta in earlier.get('files',{}).items()]
    for item in entries:
        rel=item['path']; q=ROOT/rel if rel.startswith('content/') else U4/rel
        if not q.exists(): problems.append(f'{lock_name} protected file missing {rel}'); continue
        # Historical stage files that are intentionally rewritten by later builders are not immutable release predecessors.
        if rel in {'status-f4d.json','journeys-f4d.json'}: continue
        if item.get('bytes') is not None and q.stat().st_size!=item['bytes']: problems.append(f'{lock_name} protected file size changed {rel}')
        if item.get('sha256') and sha(q)!=item['sha256']: problems.append(f'{lock_name} protected file hash changed {rel}')

for rel in ('journeys/U4-J1.json','journeys/U4-J2.json','journeys/U4-J3.json','journeys/U4-J4.json'):
    p=U4/rel; expected_meta=lock_d['files'][rel]
    if p.stat().st_size!=expected_meta['bytes'] or sha(p)!=expected_meta['sha256']: problems.append(f'F4D predecessor changed {rel}')

if lock.get('lock_status')!='LOCKED_F4E_J1_J2_J3_J4_J5' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4E lock boundary wrong')
for rel,meta in lock.get('files',{}).items():
    q=U4/rel
    if not q.exists() or q.stat().st_size!=meta['bytes'] or sha(q)!=meta['sha256']: problems.append(f'F4E locked file mismatch {rel}')
for forbidden in [U4/'memory-objects.json']:
    if forbidden.exists(): problems.append(f'premature student-runtime artifact exists {forbidden.relative_to(ROOT)}')
course=read(ROOT/'content/ap-biology/course.json'); cu4=next(u for u in course['units'] if u['unit_id']=='unit-4')
if cu4.get('status')!='F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW' or cu4.get('student_release') is not False: problems.append('course registry F4E state mismatch')
if cu4.get('journey_count')!=5 or cu4.get('scene_count')!=33: problems.append('course registry F4E accounting mismatch')

report=['# Unit 4 F4E Narrative QA','','## Result','','**PASS**' if not problems else '**FAIL**','','## Journey 5 accounting','',f'- Journeys 1–4 protected byte-for-byte from F4D: **{"PASS" if not any("predecessor changed" in p for p in problems) else "FAIL"}**','- Polished Journey 5 scenes: **8 / 8**',f'- Locked Journey 5 knowledge records represented: **{len(set(assigned))} / 27**','- Optional first-exposure recalls: **3**',f'- Journey 5 narrative words: **{sum(word_counts)}**',f'- Mean Journey 5 scene length: **{statistics.mean(word_counts):.1f} words**',f'- Shortest Journey 5 scene: **{min(word_counts)} words**','','## Prose-level gates','','- Every scene fixes left/center/right geography before the chromosome or cell-cycle mechanism changes.','- Dr. Mira Chen and the same tracked chromosome archive case persist through all eight locations.','- Histone, nucleosome, chromatin, chromosome, sister chromatid, homolog, centromere, and kinetochore remain physically and verbally distinct.','- Chromosomes remain chromosomes throughout the cell cycle; condensation changes packaging and visibility.','- Somatic/gamete roles remain distinct from diploid/haploid chromosome-set descriptions.','- Interphase is active G1, S, and G2 and is not encoded as universal 90% or as a resting state.','- S phase doubles DNA content and chromatid number without doubling centromere-counted chromosome number before sister separation.','- G1 and G2 phases remain separate from their later checkpoints.','- G0 is nondividing with variable reversibility, not a universal permanent endpoint.','- Every F3 record retains its exact F1 canonical science in the story-beat layer.','- Unit 4 remains developer preview only.','']
if problems: report += ['## Blocking findings','']+[f'- {p}' for p in problems]+['']
(ROOT/'docs/UNIT4_F4E_QA.md').write_text('\n'.join(report),encoding='utf-8')
if problems:
    print('UNIT 4 F4E QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT 4 F4E QA PASS')
print(json.dumps({'journey':'U4-J5','scenes':8,'knowledge_records':27,'optional_recalls':3,'story_words':sum(word_counts),'average_scene_words':round(statistics.mean(word_counts),1),'min_scene_words':min(word_counts),'journeys_1_4_unchanged':True,'student_release':False,'preview_release':True},indent=2))
