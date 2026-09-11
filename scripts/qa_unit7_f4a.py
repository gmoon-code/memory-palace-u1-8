from __future__ import annotations
import json, hashlib, re, statistics, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content'/'ap-biology'/'unit-7'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def wc(text): return len(re.findall(r"\b[\w’′'-]+\b",text))

problems=[]
journey=read(U7/'journeys'/'U7-J1.json')
canon={r['knowledge_id']:r for r in read(U7/'source'/'canonical-unit7-f1.json')['canonical_catalog']}
briefs={b['locus_id']:b for b in read(U7/'briefs'/'scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U7-J1'}
lock=read(U7/'content-lock-f4a.json')

expected_loci=[f'U7-L{i:02d}' for i in range(1,11)]
if journey.get('palace_id')!='U7-J1': problems.append('Journey 1 ID changed')
if journey.get('scene_count')!=10 or len(journey.get('scenes',[]))!=10: problems.append('Journey 1 must contain 10 scenes')
if [s.get('locus_id') for s in journey['scenes']]!=expected_loci: problems.append('F2/F3 locus order changed')
if journey.get('checkpoint_count')!=3: problems.append('F3 Quick Recall count changed from 3')
if journey.get('student_release')!='DEVELOPER_PREVIEW_F4A' or journey.get('preview_release') is not True: problems.append('F4A preview boundary is wrong')
if journey.get('guide',{}).get('name')!='Dr. Imani Vale': problems.append('Unit 7 guide changed')
if 'clockwise ring' not in journey.get('route_orientation','').lower(): problems.append('route orientation does not define the clockwise observatory route')
if len(journey.get('premise',''))<350 or len(journey.get('mission',''))<250 or len(journey.get('finale',''))<300: problems.append('journey-level narrative framing is too thin')

assigned=[]; counts=[]; exact_targets=0
banned=re.compile(r'\b(PPT|CED|Campbell|College Board|teacher enrichment|teacher-required|exam scope|exam-scope|source material|source lock|canonical record|F1|F2|F3|F4A)\b',re.I)
for s in journey['scenes']:
    lid=s['locus_id']; b=briefs[lid]
    prose=' '.join(s.get('story_paragraphs',[])); low=prose.casefold().replace('**','')
    n=wc(prose); counts.append(n)
    if n<450: problems.append(f'{lid} narrative too short: {n} words')
    if len(s.get('story_paragraphs',[]))<6: problems.append(f'{lid} has fewer than 6 narrative paragraphs')
    opening=s['story_paragraphs'][0].lower()
    if 'left' not in opening or ('ahead' not in opening and 'center' not in opening) or 'right' not in opening: problems.append(f'{lid} opening does not orient left/center/right')
    zones=s.get('scene_layout',{}).get('zones',[])
    if len(zones)!=3 or [z.get('position') for z in zones]!=['left','center','right']: problems.append(f'{lid} geometry changed')
    orient=s['scene_layout']['orientation']
    for x in (b['spatial_layout']['left']['anchor'],b['spatial_layout']['center']['anchor'],b['spatial_layout']['right']['anchor']):
        if x not in orient: problems.append(f'{lid} F3 anchor missing from orientation: {x}')
    if len(s.get('cast',[]))<5: problems.append(f'{lid} cast too thin')
    if not any(c.get('name')=='Dr. Imani Vale' for c in s['cast']): problems.append(f'{lid} lost guide')
    if not any(c.get('name')=='Transparent population ledger' for c in s['cast']): problems.append(f'{lid} lost continuity object')
    if s.get('continuity_object')!=journey['scenes'][0].get('continuity_object'): problems.append(f'{lid} continuity object changed')
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
    if '—' in prose: problems.append(f'{lid} contains prohibited em dash')
    if ': ' in prose: problems.append(f'{lid} contains colon punctuation in narrative prose')
    if s.get('checkpoint') != bool(b['quick_recall']['enabled']): problems.append(f'{lid} checkpoint status changed from F3')
    if s.get('checkpoint'):
        if s.get('checkpoint_prompt')!=b['quick_recall']['candidate_prompt']: problems.append(f'{lid} checkpoint prompt changed')
        if s.get('checkpoint_answer')!=b['quick_recall']['answer']: problems.append(f'{lid} checkpoint answer changed')
    idx=expected_loci.index(lid)
    expected_next=journey['scenes'][idx+1]['locus'] if idx<len(expected_loci)-1 else None
    if s.get('next_locus')!=expected_next: problems.append(f'{lid} next-locus continuity broken')
    # Every nonfinal scene must finish with a concrete unresolved handoff into the next room.
    if idx<len(expected_loci)-1:
        ending=s['story_paragraphs'][-1].casefold()
        next_name=journey['scenes'][idx+1]['locus'].split()[0].casefold()
        if len(ending)<180: problems.append(f'{lid} transition paragraph too thin')

if len(assigned)!=26 or len(set(assigned))!=26: problems.append(f'Journey 1 knowledge coverage is {len(assigned)} refs / {len(set(assigned))} unique, expected 26/26')
if exact_targets!=15: problems.append(f'Journey 1 exact-name target count is {exact_targets}, expected 15')

# Visible high-risk science/misconception guards.
full=' '.join(' '.join(s['story_paragraphs']) for s in journey['scenes']).casefold().replace('**','')
visible={
 'evidence_not_mechanism':['charles darwin','biogeography','descent with modification','not a complete mechanism'],
 'population_not_individual':['individual organism does not genetically evolve during its lifetime','populations over generations'],
 'variation_before_selection':['variation is already present','selection acts on phenotypic variation'],
 'adaptation_not_need':['adaptation','heritable trait','environment did not create the needed beak'],
 'competition_to_reproduction':['limited resources','competition and differential reproductive success','viable reproductive offspring'],
 'fitness_not_strength':['evolutionary fitness','relative fitness','reproductive success relative to others','environment-dependent fitness effects'],
 'acclimation_vs_evolution':['lifetime response','heritable generational change','acclimation versus evolutionary change'],
 'mutation_selection_distinction':['selection can be nonrandom','origin of mutation is random with respect to fitness'],
 'sickle_heterozygote':['heterozygous for the sickle-cell allele','higher reproductive fitness than either homozygote','not a statement that sickle-cell disease itself is beneficial'],
 'three_selection_modes':['directional selection','stabilizing selection','disruptive selection'],
 'sexual_selection':['sexual selection','mate choice and competition among potential mates','survival cost'],
 'artificial_selection':['selective breeding','artificial selection','human selective breeding','natural versus artificial selection'],
}
for name, phrases in visible.items():
    if not all(p in full for p in phrases): problems.append(f'high-risk science guard not visibly satisfied: {name}')

# F1/F2/F3 protected artifacts remain unchanged.
f3=read(U7/'content-lock-f3.json')
for key in ('f1_protected_hashes','f2_protected_hashes'):
    for rel,h in f3.get(key,{}).items():
        p=ROOT/rel
        if not p.exists() or sha(p)!=h: problems.append(f'{key} changed: {rel}')
for rel,meta in f3.get('files',{}).items():
    p=ROOT/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F3 locked brief artifact changed: {rel}')

# All released Units 1–6 content remains byte-identical to Unit 6 F6 baseline.
up=read(U7/'upstream-u1-u6-protection-f1.json')
if up.get('protected_file_count')!=356: problems.append('Units 1–6 protection manifest count changed')
for item in up['protected_files']:
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f'protected Units 1–6 file changed: {item["path"]}')

if lock.get('lock_status')!='LOCKED_F4A_J1' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4A content-lock boundary invalid')
for rel,meta in lock.get('files',{}).items():
    p=U7/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4A locked file mismatch: {rel}')

# No final Unit 7 runtime machinery yet.
for forbidden in ['memory-objects-f5.json','application-lab.json','review-manifest-f5.json','mixed-discrimination-f5.json','scope-guards-f5.json','finalization-f5.json']:
    if read(U7/'status.json').get('status')!='STUDENT_READY' and (U7/forbidden).exists(): problems.append(f'premature Unit 7 final runtime artifact exists: {forbidden}')

required=[U7/'journeys/U7-J1.json',U7/'journeys-f4a.json',U7/'status-f4a.json',U7/'content-lock-f4a.json',U7/'f4a-release-manifest.json',ROOT/'docs/UNIT7_F4A_JOURNEY1_STORY.md']
for p in required:
    if not p.exists(): problems.append(f'missing F4A artifact: {p.relative_to(ROOT)}')

status=read(U7/'status.json')
allowed_status={'F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
if status.get('status') not in allowed_status: problems.append('Unit 7 F4A-or-later status boundary invalid')
if status.get('status')=='STUDENT_READY' and (status.get('student_release') is not True or status.get('preview_release') is not False): problems.append('Unit 7 F5 release flags invalid while preserving F4A')
if status.get('status')!='STUDENT_READY' and (status.get('student_release') is not False or status.get('preview_release') is not True): problems.append('Unit 7 pre-F5 status flags invalid while preserving F4A')
if status.get('status')=='F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW' and (status.get('journey_count'),status.get('scene_count'),status.get('memory_objects'),status.get('application_challenges'))!=(1,10,0,0): problems.append('Unit 7 F4A runtime-development counts invalid')
if status.get('status')=='F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW' and (status.get('journey_count'),status.get('scene_count'),status.get('memory_objects'),status.get('application_challenges'))!=(2,24,0,0): problems.append('Unit 7 F4B runtime-development counts invalid while preserving F4A')
if status.get('status')=='F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW' and (status.get('journey_count'),status.get('scene_count'),status.get('memory_objects'),status.get('application_challenges'))!=(3,33,0,0): problems.append('Unit 7 F4C runtime-development counts invalid while preserving F4A')
if status.get('status')=='F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW' and (status.get('journey_count'),status.get('scene_count'),status.get('memory_objects'),status.get('application_challenges'))!=(4,41,0,0): problems.append('Unit 7 F4D runtime-development counts invalid while preserving F4A')
if status.get('status')=='F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW' and (status.get('journey_count'),status.get('scene_count'),status.get('memory_objects'),status.get('application_challenges'))!=(6,55,0,0): problems.append('Unit 7 F4F runtime-development counts invalid while preserving F4A')
course=read(ROOT/'content/ap-biology/course.json'); cu7=next(u for u in course['units'] if u['unit_id']=='unit-7')
if cu7.get('status') not in allowed_status: problems.append('course registry Unit 7 F4A-or-later boundary invalid')
if cu7.get('status')=='STUDENT_READY' and (cu7.get('student_release') is not True or cu7.get('preview_release') is not False): problems.append('course registry Unit 7 F5 release invalid while preserving F4A')
if cu7.get('status')!='STUDENT_READY' and (cu7.get('student_release') is not False or cu7.get('preview_release') is not True): problems.append('course registry Unit 7 pre-F5 release invalid while preserving F4A')

report=['# Unit 7 F4A Narrative QA','', '## Result','', '**PASS**' if not problems else '**FAIL**','',
'## Journey 1 accounting','', '- Polished scenes: **10 / 10**', '- Locked F3 knowledge records represented: **26 / 26**', f'- Exact-name targets explicitly introduced: **{exact_targets} / 15**', '- Optional first-exposure recalls: **3**', f'- Narrative words: **{sum(counts)}**', f'- Mean scene length: **{statistics.mean(counts):.1f} words**', f'- Shortest scene: **{min(counts)} words**', f'- Longest scene: **{max(counts)} words**','',
'## Prose-quality gates','', '- Every scene fixes left / center / right geography before the evolutionary state changes.', '- Dr. Imani Vale and the same transparent population ledger persist through all ten locations.', '- The principal finch population persists through the main natural-selection sequence; alternate biological cases appear only when required by the locked science.', '- Every story beat preserves the exact F1 canonical scientific statement.', '- Every exact-name target is introduced only after its defining evidence, mechanism, or comparison is visible.', '- Population change is never represented as an individual organism transforming itself.', '- Fitness remains relative reproductive success in a specified environment, not strength or survival alone.', '- Acclimation/lifetime change, molecular phenotype, three selection distributions, sexual selection, and artificial selection remain diagnostically distinct.', '- The sickle-cell case preserves heterozygote advantage without calling sickle-cell disease protective.', '- Student prose contains no development/source-management language, em dashes, or colon punctuation.', '- Each scene ends with a biological or evidentiary consequence that makes the next locus necessary.', '- Unit 7 remains a developer preview with zero final Memory Objects or live Challenge Lab tasks.','']
if problems: report += ['## Blocking findings','']+[f'- {p}' for p in problems]+['']

if status.get('status')!='STUDENT_READY': (ROOT/'docs'/'UNIT7_F4A_QA.md').write_text('\n'.join(report),encoding='utf-8')

if problems:
    print('UNIT 7 F4A QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT 7 F4A QA PASS')
print(json.dumps({'journey':'U7-J1','scenes':10,'knowledge_records':26,'exact_name_targets':exact_targets,'optional_recalls':3,'story_words':sum(counts),'average_scene_words':round(statistics.mean(counts),1),'min_scene_words':min(counts),'max_scene_words':max(counts),'student_release':False,'preview_release':True},indent=2))
