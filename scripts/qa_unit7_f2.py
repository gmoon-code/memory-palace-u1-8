from __future__ import annotations
import json,hashlib,sys
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content'/'ap-biology'/'unit-7'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

src=read(U7/'source'/'canonical-unit7-f1.json')
cls=read(U7/'architecture'/'learning-classification-f2.json')
arch=read(U7/'architecture'/'palace-architecture-f2.json')
lock=read(U7/'content-lock-f2.json')
status=read(U7/'status-f2.json')
up=read(U7/'upstream-u1-u6-protection-f1.json')
problems=[]

canon={r['knowledge_id'] for r in src['canonical_catalog']}
if len(canon)!=215: problems.append(f'canonical record count {len(canon)} != 215')
if len(cls['records'])!=215: problems.append('classification does not contain 215 records')
if {r['knowledge_id'] for r in cls['records']}!=canon: problems.append('classification IDs do not equal canonical IDs')

palace=[k for l in arch['loci'] for k in l['knowledge_ids']]
challenge=[x['knowledge_id'] for x in arch['challenge_lab']]
scope=[x['knowledge_id'] for x in arch['scope_guards']]
if (len(palace),len(set(palace)),len(challenge),len(scope))!=(174,174,16,25):
    problems.append(f'partition counts incorrect: {len(palace)}/{len(set(palace))}/{len(challenge)}/{len(scope)}')
if set(palace)|set(challenge)|set(scope)!=canon: problems.append('palace + challenge + scope does not cover all 215 canonical records')
if set(palace)&set(challenge) or set(palace)&set(scope) or set(challenge)&set(scope): problems.append('learning destinations overlap')

expected_dest={'PALACE_PRIMARY_LOCUS':55,'PALACE_EMBEDDED':119,'SUPPORTING_NON_RUNTIME_SCOPE_GUARD':25,'CHALLENGE_LAB':16}
if cls['counts']['by_destination']!=expected_dest: problems.append(f"classification destination counts incorrect: {cls['counts']['by_destination']}")

if len(arch['journeys'])!=6 or len(arch['bundles'])!=23 or len(arch['loci'])!=55: problems.append('journey/bundle/locus counts incorrect')
if [l['locus_id'] for l in arch['loci']] != [f'U7-L{i:02d}' for i in range(1,56)]: problems.append('locus IDs are not contiguous U7-L01..U7-L55')
if [j['journey_id'] for j in arch['journeys']] != [f'U7-J{i}' for i in range(1,7)]: problems.append('journey IDs are not U7-J1..U7-J6')
if [b['bundle_id'] for b in arch['bundles']] != [f'U7-B{i:02d}' for i in range(1,24)]: problems.append('bundle IDs are not contiguous U7-B01..U7-B23')

known_loci={l['locus_id'] for l in arch['loci']}
for l in arch['loci']:
    if set(l['scene_geometry'])!={'left','center','right'} or not all(l['scene_geometry'].values()): problems.append(f"{l['locus_id']} missing left/center/right geometry")
    if not l.get('micro_anchor'): problems.append(f"{l['locus_id']} missing micro-anchor")
    if l['primary_knowledge_id'] not in l['knowledge_ids']: problems.append(f"{l['locus_id']} primary anchor missing from knowledge_ids")
    if l['embedded_knowledge_ids']!=l['knowledge_ids'][1:]: problems.append(f"{l['locus_id']} embedded list mismatch")
    if not l['scientific_visual_required']: problems.append(f"{l['locus_id']} must require a scientific visual")
    if l['narrative_status']!='ARCHITECTURE_ONLY_NO_STORY_PROSE_F2': problems.append(f"{l['locus_id']} narrative status invalid")
    if any(k in l for k in ('story_paragraphs','story_open','story_close','cast','dialogue','mnemonic_hook')):
        problems.append(f"{l['locus_id']} contains F3/F4 narrative fields")

# Journey/bundle accounting.
for j in arch['journeys']:
    expected=[l['locus_id'] for l in arch['loci'] if l['journey_id']==j['journey_id']]
    actual=[x for b in j['bundles'] for x in b['loci']]
    if actual!=expected: problems.append(f"{j['journey_id']} bundle locus order mismatch")
for b in arch['bundles']:
    expected=[l['locus_id'] for l in arch['loci'] if l['bundle_id']==b['bundle_id']]
    if b['loci']!=expected: problems.append(f"{b['bundle_id']} locus membership mismatch")

if len(arch['confusable_sets'])!=33: problems.append('confusable set count not 33')
pset=set(palace)
for c in arch['confusable_sets']:
    if len(set(c['knowledge_ids']))<2 or not set(c['knowledge_ids'])<=pset: problems.append(f"{c['set_id']} invalid confusable membership")
if [c['set_id'] for c in arch['confusable_sets']] != [f'U7-D{i:02d}' for i in range(1,34)]: problems.append('confusable IDs are not U7-D01..U7-D33')

exact=sum(bool(r['delayed_review_target']) for r in cls['records'])
if exact!=94: problems.append(f'exact-name review targets {exact} != 94')
react=sum(r['reactivation_mode']=='PRIOR_UNIT_REACTIVATION' for r in cls['records'])
if react!=6: problems.append(f'prerequisite reactivations {react} != 6')
if len(arch.get('prerequisite_reactivations',[]))!=6: problems.append('architecture prerequisite reactivation count not 6')
if cls['counts']['mandatory_spelling_targets']!=0: problems.append('mandatory spelling target count must remain zero')

# Challenge architecture is procedure/application only and points to real loci.
if len(arch['challenge_lab'])!=16: problems.append('challenge lab architecture count not 16')
for x in arch['challenge_lab']:
    if not set(x['prerequisite_loci'])<=known_loci: problems.append(f"{x['knowledge_id']} challenge prerequisite locus invalid")
    if x['runtime_status']!='ARCHITECTURE_ONLY_NO_TASK_PROSE_F2': problems.append(f"{x['knowledge_id']} challenge runtime status invalid")

if len(arch['scope_guards'])!=25: problems.append('scope guard architecture count not 25')
if any(x['runtime_status']!='NON_RUNTIME_SCOPE_BOUNDARY' for x in arch['scope_guards']): problems.append('one or more scope guards became runtime targets')

# F1 scientific lock files must remain unchanged.
for rel,h in lock['f1_protected_hashes'].items():
    p=ROOT/rel
    if not p.exists() or sha(p)!=h: problems.append(f'F1 protected file changed: {rel}')

# Released Units 1–6 stay byte-identical to the exact Unit 6 F6 baseline.
if up.get('baseline_package_sha256')!='ba5ca238d579d7fa733bd6b17613d85dc7685893152ff4bc574ee65a0b7b508a':
    problems.append('wrong Units 1–6 baseline checksum')
if up.get('protected_file_count')!=356: problems.append('Units 1–6 protection manifest does not contain 356 files')
for x in up['protected_files']:
    p=ROOT/x['path']
    if not p.exists() or sha(p)!=x['sha256']: problems.append(f"upstream released file changed: {x['path']}")

if status['student_release'] or status['preview_release']: problems.append('Unit 7 must remain unreleased at F2')
if (status['journey_count'],status['scene_count'],status['memory_objects'],status['application_challenges'])!=(0,0,0,0):
    problems.append('Unit 7 student runtime boundary is not zero')
if status['status'] not in {'LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}: problems.append('Unit 7 F2-or-later status incorrect')
if (status['architecture_journeys'],status['architecture_bundles'],status['architecture_loci'])!=(6,23,55):
    problems.append('Unit 7 architecture status counts incorrect')

course=read(ROOT/'content/ap-biology/course.json')
u7=next((u for u in course['units'] if u['unit_id']=='unit-7'),None)
if not u7 or u7.get('status') not in {'LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}:
    problems.append('course registry Unit 7 F2 state mismatch')
elif u7.get('status')=='STUDENT_READY' and u7.get('student_release') is not True:
    problems.append('course registry Unit 7 F5 release invalid while preserving F2')
elif u7.get('status')!='STUDENT_READY' and u7.get('student_release') is not False:
    problems.append('course registry Unit 7 pre-F5 release invalid while preserving F2')
for n in range(1,7):
    u=next((u for u in course['units'] if u['unit_id']==f'unit-{n}'),None)
    if not u or u.get('status')!='STUDENT_READY': problems.append(f'upstream Unit {n} is no longer STUDENT_READY')

for p in ROOT.rglob('*.pdf'):
    problems.append(f'forbidden source PDF in repository: {p.relative_to(ROOT)}')

required=[
    U7/'architecture/learning-classification-f2.json',
    U7/'architecture/palace-architecture-f2.json',
    U7/'audit/APBIO_Unit7_F2_Classification.xlsx',
    U7/'content-lock-f2.json',
    U7/'f2-release-manifest.json',
    U7/'status-f2.json',
    ROOT/'docs/UNIT7_F2_ARCHITECTURE.md',
    ROOT/'docs/UNIT7_F2_CLASSIFICATION_MATRIX.md',
    ROOT/'docs/UNIT7_F2_QA.md',
    ROOT/'docs/UNIT7_F2_RELEASE.md',
]
for p in required:
    if not p.exists(): problems.append(f'missing required artifact: {p.relative_to(ROOT)}')

if problems:
    print('UNIT 7 F2 QA FAIL')
    for p in problems: print('-',p)
    sys.exit(1)
print('UNIT 7 F2 QA PASS')
print({'canonical_records':215,'palace_managed_records':174,'scope_guards':25,'challenge_lab_records':16,'journey_blueprints':6,'bundle_blueprints':23,'permanent_loci':55,'confusable_sets':33,'exact_name_targets':94,'prerequisite_reactivations':6,'student_release':False})
