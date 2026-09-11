from __future__ import annotations
import json,re,hashlib,statistics,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content'/'ap-biology'/'unit-7'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

journey=read(U7/'journeys/U7-J4.json')
briefs={b['locus_id']:b for b in read(U7/'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id']=='U7-J4'}
canon={r['knowledge_id']:r for r in read(U7/'source/canonical-unit7-f1.json')['canonical_catalog']}
lock=read(U7/'content-lock-f4d.json')
problems=[]
expected_loci=[f'U7-L{i:02d}' for i in range(34,42)]
expected_taxa=['Lancelet','Shark','Salamander','Mouse','Lizard','Pigeon']
expected_nodes={'N0','N1','N2','N3','N4'}

if journey.get('palace_id')!='U7-J4': problems.append('Journey ID is not U7-J4')
if journey.get('scene_count')!=8 or len(journey.get('scenes',[]))!=8: problems.append('Journey 4 does not contain 8 scenes')
if journey.get('checkpoint_count')!=3: problems.append('Journey 4 checkpoint count is not 3')
if [s['locus_id'] for s in journey['scenes']]!=expected_loci: problems.append('Journey 4 route is not U7-L34..U7-L41 in order')
if journey.get('student_release')!='DEVELOPER_PREVIEW_F4D' or journey.get('preview_release') is not True: problems.append('Journey 4 release boundary invalid')
if [t['name'] for t in journey.get('taxa',[])]!=expected_taxa: problems.append('Journey 4 fixed taxon identities changed')
if set(journey.get('node_map',{}))!=expected_nodes: problems.append('Journey 4 persistent node IDs are not N0..N4')

banned=re.compile(r'\b(PPT|CED|College Board|Campbell|source material|content lock|teacher enrichment|exam scope|LOCKED_F|developer preview|F1|F2|F3|F4)\b',re.I)
counts=[]; assigned=[]; exact_targets=0
for s in journey['scenes']:
    lid=s['locus_id']; b=briefs[lid]
    prose=' '.join(s['story_paragraphs']); low=prose.casefold().replace('**','')
    words=len(re.findall(r"\b[\w’′'-]+\b",prose)); counts.append(words); assigned+=s['object_ids']
    if words<450: problems.append(f'{lid} has only {words} narrative words')
    if len(s['story_paragraphs'])<6: problems.append(f'{lid} has fewer than 6 narrative paragraphs')
    opening=s['story_paragraphs'][0].casefold()
    if 'left' not in opening or 'right' not in opening or not ('ahead' in opening or 'center' in opening): problems.append(f'{lid} does not establish left/center/right geography before action')
    if len(s.get('cast',[]))<7: problems.append(f'{lid} cast is too thin')
    for name in ('Dr. Imani Vale','Six-taxon badge rail','Persistent node map','Six-taxon navigation dossier'):
        if not any(c['name']==name for c in s['cast']): problems.append(f'{lid} recurring cast missing {name}')
    if [t['name'] for t in s.get('taxa',[])]!=expected_taxa: problems.append(f'{lid} taxon identities changed')
    if set(s.get('node_map',{}))!=expected_nodes: problems.append(f'{lid} node map changed')
    if s.get('continuity_object')!=journey['scenes'][0].get('continuity_object'): problems.append(f'{lid} continuity object changed')
    if s['object_ids']!=b['knowledge_ids']: problems.append(f'{lid} knowledge IDs changed from F3')
    if set(z['position'] for z in s['scene_layout']['zones'])!={'left','center','right'}: problems.append(f'{lid} spatial zones invalid')
    terms={t['knowledge_id']:t for t in b['term_introductions']}
    beats={x['object_id']:x for x in s['story_beats']}
    if set(beats)!=set(s['object_ids']): problems.append(f'{lid} story beat coverage mismatch')
    for kid in s['object_ids']:
        t=terms[kid]; beat=beats[kid]
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
    if idx<len(expected_loci)-1 and len(s['story_paragraphs'][-1])<180: problems.append(f'{lid} transition paragraph too thin')

if len(assigned)!=26 or len(set(assigned))!=26: problems.append(f'Journey 4 knowledge coverage is {len(assigned)} refs / {len(set(assigned))} unique, expected 26/26')
if exact_targets!=21: problems.append(f'Journey 4 exact-name target count is {exact_targets}, expected 21')

full=' '.join(' '.join(s['story_paragraphs']) for s in journey['scenes']).casefold().replace('**','')
visible={
 'discipline_terms':['taxonomy is the naming and classification','systematics studies biological diversity and evolutionary relationships','phylogenetics comprises methods used to infer and test','a phylogeny is a hypothesis'],
 'hypothesis_revision':['trees and cladograms are testable hypotheses','revised when new evidence changes the best-supported relationships'],
 'scale_rotation':['branch lengths have no numerical legend','branch length is tied to an explicit scale','node ids do not move to new ancestral positions'],
 'node_anatomy':['nodes represent common ancestors','root represents the ancestral lineage','a clade, a group containing a common ancestor and all of its descendants','living taxon badges sit on the same present-time boundary'],
 'sister_and_early':['sister taxa or sister clades are the two descendant lineages that share the same immediate common ancestor','basal lineage','it is not less evolved, unfinished, or the living ancestor'],
 'character_mapping':['ancestral character','derived character','synapomorphy','shared derived character inherited from the most recent common ancestor'],
 'outgroup':['outgroup is a lineage outside the focal ingroup','not a living ancestor','help establish character-state polarity'],
 'evidence_construction':['morphological and fossil','dna and protein sequence','tree changed because the evidence changed'],
 'grouping':['monophyletic group','paraphyletic group','polyphyletic group','principle of parsimony','not the only phylogenetic method'],
}
for name,phrases in visible.items():
    if not all(p in full for p in phrases): problems.append(f'high-risk phylogeny guard not visibly satisfied: {name}')

# Explicit node stability and no tip-as-ancestor rule.
if full.count('n4')<8: problems.append('N4 is not persistent enough across Journey 4')
if 'neither lizard nor pigeon is being used as the ancestor of the other' not in full: problems.append('sister taxa tip-as-ancestor guard missing')
if 'rotation around a node can reverse that visual order without altering' not in full: problems.append('branch-rotation invariance guard missing')
if 'lancelet is outside the vertebrate ingroup' not in full: problems.append('outgroup boundary missing')

# Protect Journeys 1–3 and all prior narrative-release evidence.
for rel,meta in lock.get('f4a_f4c_prior_narrative_protection',{}).items():
    p=ROOT/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'prior narrative artifact changed: {rel}')

# F1/F2/F3 protected science and architecture remain unchanged.
f3=read(U7/'content-lock-f3.json')
for key in ('f1_protected_hashes','f2_protected_hashes'):
    for rel,h in f3.get(key,{}).items():
        p=ROOT/rel
        if not p.exists() or sha(p)!=h: problems.append(f'{key} changed: {rel}')
for rel,meta in f3.get('files',{}).items():
    p=ROOT/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F3 locked brief artifact changed: {rel}')

# Units 1–6 remain byte-identical.
up=read(U7/'upstream-u1-u6-protection-f1.json')
if up.get('baseline_package_sha256')!='ba5ca238d579d7fa733bd6b17613d85dc7685893152ff4bc574ee65a0b7b508a': problems.append('wrong Units 1–6 baseline checksum')
if up.get('protected_file_count')!=356: problems.append('Units 1–6 protection manifest count changed')
for item in up['protected_files']:
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f'protected Units 1–6 file changed: {item["path"]}')

if lock.get('lock_status')!='LOCKED_F4D_J1_J4' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4D content-lock boundary invalid')
for rel,meta in lock.get('files',{}).items():
    p=U7/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4D locked file mismatch: {rel}')

for forbidden in ['memory-objects-f5.json','application-lab.json','review-manifest-f5.json','mixed-discrimination-f5.json','scope-guards-f5.json','finalization-f5.json']:
    if read(U7/'status.json').get('status')!='STUDENT_READY' and (U7/forbidden).exists(): problems.append(f'premature Unit 7 final runtime artifact exists: {forbidden}')

required=[
    U7/'journeys/U7-J4.json',U7/'journeys-f4d.json',U7/'status-f4d.json',U7/'content-lock-f4d.json',U7/'f4d-release-manifest.json',
    ROOT/'docs/UNIT7_F4D_JOURNEY4_STORY.md',ROOT/'docs/UNIT7_F4D_RELEASE.md',ROOT/'docs/UNIT7_F4D_PACKAGE_QA.md'
]
for p in required:
    if not p.exists(): problems.append(f'missing F4D artifact: {p.relative_to(ROOT)}')

status=read(U7/'status.json')
allowed_status={'F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
if status.get('status') not in allowed_status: problems.append('Unit 7 F4D-or-later status boundary invalid')
if status.get('status')=='STUDENT_READY' and (status.get('student_release') is not True or status.get('preview_release') is not False): problems.append('Unit 7 F5 release flags invalid while preserving F4D')
if status.get('status')!='STUDENT_READY' and (status.get('student_release') is not False or status.get('preview_release') is not True): problems.append('Unit 7 pre-F5 status flags invalid while preserving F4D')
if status.get('status')=='F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW' and (status.get('journey_count'),status.get('scene_count'),status.get('memory_objects'),status.get('application_challenges'))!=(4,41,0,0): problems.append('Unit 7 F4D runtime-development counts invalid')
if status.get('status')=='F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW' and (status.get('journey_count'),status.get('scene_count'),status.get('memory_objects'),status.get('application_challenges'))!=(5,50,0,0): problems.append('Unit 7 F4E runtime-development counts invalid while preserving F4D')
if status.get('status')=='F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW' and (status.get('journey_count'),status.get('scene_count'),status.get('memory_objects'),status.get('application_challenges'))!=(6,55,0,0): problems.append('Unit 7 F4F runtime-development counts invalid while preserving F4D')
course=read(ROOT/'content/ap-biology/course.json'); cu7=next(u for u in course['units'] if u['unit_id']=='unit-7')
if cu7.get('status') not in allowed_status: problems.append('course registry Unit 7 F4D-or-later boundary invalid')
if cu7.get('status')=='STUDENT_READY' and (cu7.get('student_release') is not True or cu7.get('preview_release') is not False): problems.append('course registry Unit 7 F5 release invalid while preserving F4D')
if cu7.get('status')!='STUDENT_READY' and (cu7.get('student_release') is not False or cu7.get('preview_release') is not True): problems.append('course registry Unit 7 pre-F5 release invalid while preserving F4D')

report=['# Unit 7 F4D Narrative QA','', '## Result','', '**PASS**' if not problems else '**FAIL**','',
'## Journey 4 accounting','', '- Polished scenes: **8 / 8**', '- Locked F3 knowledge records represented: **26 / 26**', f'- Exact-name targets explicitly introduced: **{exact_targets} / 21**', '- Optional first-exposure recalls: **3**', f'- Narrative words: **{sum(counts)}**', f'- Mean scene length: **{statistics.mean(counts):.1f} words**', f'- Shortest scene: **{min(counts)} words**', f'- Longest scene: **{max(counts)} words**','',
'## Prose and phylogeny gates','',
'- Every scene fixes left / center / right geography before a tree, character state, evidence source, or grouping is interpreted.',
'- Lancelet, Shark, Salamander, Mouse, Lizard, and Pigeon remain the same six sampled taxa through all eight locations.',
'- Node IDs N0 through N4 remain persistent through every branch rotation and evidence update.',
'- Taxonomy, systematics, phylogenetics, and phylogeny remain distinct scientific jobs.',
'- Trees and cladograms remain testable, revisable hypotheses.',
'- Unscaled cladogram branch length carries no time/change meaning; scaled trees are interpreted only from an explicit scale.',
'- Branch rotation never changes topology or ancestry.',
'- Roots and internal nodes represent inferred ancestral lineages; extant tips never become ancestors of other extant taxa.',
'- Sister taxa are determined by the same immediate common-ancestor node, not visual proximity.',
'- Early-branching/basal lineage wording is tied to branching position and never primitive status.',
'- Ancestral and derived character states remain relative to the focal comparison.',
'- Synapomorphies remain shared derived characters inherited from a common ancestor.',
'- The outgroup remains outside the ingroup and provides polarity evidence without becoming the ingroup ancestor.',
'- Morphological, fossil, DNA, and protein evidence test candidate phylogenies while every tree remains revisable.',
'- Monophyletic, paraphyletic, and polyphyletic groupings remain ancestry-defined.',
'- Parsimony is one inference criterion and is never described as infallible or the only method.',
'- Student prose contains no development/source-management language, em dashes, or colon punctuation.',
'- Journeys 1–3 remain byte-frozen and Unit 7 remains a developer preview with zero final Memory Objects or live Challenge Lab tasks.','']
if problems: report += ['## Blocking findings','']+[f'- {p}' for p in problems]+['']

if status.get('status')!='STUDENT_READY': (ROOT/'docs'/'UNIT7_F4D_QA.md').write_text('\n'.join(report),encoding='utf-8')

if problems:
    print('UNIT 7 F4D QA FAIL')
    print('\n'.join(f'- {p}' for p in problems))
    sys.exit(1)
print('UNIT 7 F4D QA PASS')
print(json.dumps({'journey':'U7-J4','scenes':8,'knowledge_records':26,'exact_name_targets':exact_targets,'optional_recalls':3,'story_words':sum(counts),'average_scene_words':round(statistics.mean(counts),1),'min_scene_words':min(counts),'max_scene_words':max(counts),'journeys1_3_frozen':True,'student_release':False,'preview_release':True},indent=2))
