from __future__ import annotations
import json,hashlib,sys
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
U6=ROOT/'content'/'ap-biology'/'unit-6'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

src=read(U6/'source'/'canonical-unit6-f1.json')
cls=read(U6/'architecture'/'learning-classification-f2.json')
arch=read(U6/'architecture'/'palace-architecture-f2.json')
lock=read(U6/'content-lock-f2.json')
status=read(U6/'status-f2.json')
up=read(U6/'upstream-u1-u5-protection-f1.json')
problems=[]

canon={r['knowledge_id'] for r in src['canonical_catalog']}
if len(canon)!=202: problems.append(f'canonical record count {len(canon)} != 202')
if len(cls['records'])!=202: problems.append('classification does not contain 202 records')
if {r['knowledge_id'] for r in cls['records']}!=canon: problems.append('classification IDs do not equal canonical IDs')

palace=[k for l in arch['loci'] for k in l['knowledge_ids']]
challenge=[x['knowledge_id'] for x in arch['challenge_lab']]
scope=[x['knowledge_id'] for x in arch['scope_guards']]
if (len(palace),len(set(palace)),len(challenge),len(scope))!=(161,161,16,25): problems.append(f'partition counts incorrect: {len(palace)}/{len(set(palace))}/{len(challenge)}/{len(scope)}')
if set(palace)|set(challenge)|set(scope)!=canon: problems.append('palace + challenge + scope does not cover all 202 canonical records')
if set(palace)&set(challenge) or set(palace)&set(scope) or set(challenge)&set(scope): problems.append('learning destinations overlap')

if len(arch['journeys'])!=6 or len(arch['bundles'])!=21 or len(arch['loci'])!=53: problems.append('journey/bundle/locus counts incorrect')
if [l['locus_id'] for l in arch['loci']] != [f'U6-L{i:02d}' for i in range(1,54)]: problems.append('locus IDs are not contiguous U6-L01..U6-L53')
if [j['journey_id'] for j in arch['journeys']] != [f'U6-J{i}' for i in range(1,7)]: problems.append('journey IDs are not U6-J1..U6-J6')
for l in arch['loci']:
    if set(l['scene_geometry'])!={'left','center','right'} or not all(l['scene_geometry'].values()): problems.append(f"{l['locus_id']} missing left/center/right geometry")
    if l['primary_knowledge_id'] not in l['knowledge_ids']: problems.append(f"{l['locus_id']} primary anchor missing from knowledge_ids")
    if l['narrative_status']!='ARCHITECTURE_ONLY_NO_STORY_PROSE_F2': problems.append(f"{l['locus_id']} narrative status invalid")
    if any(k in l for k in ('story_paragraphs','story_open','story_close','cast')): problems.append(f"{l['locus_id']} contains F3/F4 narrative fields")

if len(arch['confusable_sets'])!=37: problems.append('confusable set count not 37')
pset=set(palace)
for c in arch['confusable_sets']:
    if len(c['knowledge_ids'])<2 or not set(c['knowledge_ids'])<=pset: problems.append(f"{c['set_id']} invalid confusable membership")

exact=sum(bool(r['delayed_review_target']) for r in cls['records'])
if exact!=134: problems.append(f'exact-name review targets {exact} != 134')
react=sum(r['reactivation_mode']=='PRIOR_UNIT_REACTIVATION' for r in cls['records'])
if react!=5: problems.append(f'prerequisite reactivations {react} != 5')
if cls['counts']['mandatory_spelling_targets']!=0: problems.append('mandatory spelling target count must remain zero')

# F1 scientific lock files must be unchanged from hashes captured in F2 lock.
for rel,h in lock['f1_protected_hashes'].items():
    p=ROOT/rel
    if not p.exists() or sha(p)!=h: problems.append(f'F1 protected file changed: {rel}')
# Released Units 1–5 files remain byte-identical to the F1 baseline protection manifest.
for x in up['protected_files']:
    p=ROOT/x['path']
    if not p.exists() or sha(p)!=x['sha256']: problems.append(f"upstream released file changed: {x['path']}")

if status['student_release'] or status['preview_release']: problems.append('Unit 6 must remain unreleased at F2')
if (status['journey_count'],status['scene_count'],status['memory_objects'],status['application_challenges'])!=(0,0,0,0): problems.append('Unit 6 student runtime boundary is not zero')
if status['status'] not in {'SCIENCE_LOCKED_F1_NOT_STUDENT_RELEASED','LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW'}: problems.append('Unit 6 status incorrect')

if problems:
    print('UNIT 6 F2 QA FAIL')
    for p in problems: print('-',p)
    sys.exit(1)
print('UNIT 6 F2 QA PASS')
print({'canonical_records':202,'palace_managed_records':161,'scope_guards':25,'challenge_lab_records':16,'journey_blueprints':6,'bundle_blueprints':21,'permanent_loci':53,'confusable_sets':37,'exact_name_targets':134,'prerequisite_reactivations':5,'student_release':False})
