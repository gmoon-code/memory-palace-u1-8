from __future__ import annotations
import json, hashlib, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

problems=[]
src=read(U5/'source'/'canonical-unit5-f1.json')
canon={r['knowledge_id']:r for r in src['canonical_catalog']}
canonical_ids=set(canon)
cls=read(U5/'architecture'/'learning-classification-f2.json')
arch=read(U5/'architecture'/'palace-architecture-f2.json')
status=read(U5/'status-f2.json')
release=read(U5/'f2-release-manifest.json')

if arch.get('counts')!={'canonical_records':152,'palace_managed_records':131,'scope_guard_records':5,'practice_only_records':16,'journeys':8,'bundles':19,'permanent_loci':50,'confusable_sets':32}:
    problems.append(f"architecture counts mismatch: {arch.get('counts')}")
if cls.get('counts',{}).get('by_destination')!={'PALACE_PRIMARY_LOCUS':50,'PALACE_EMBEDDED':81,'CHALLENGE_LAB':16,'SUPPORTING_NON_RUNTIME_SCOPE_GUARD':5}:
    problems.append(f"classification destination counts mismatch: {cls.get('counts',{}).get('by_destination')}")
if cls.get('counts',{}).get('exact_name_targets')!=130: problems.append('exact-name target count is not 130')
if cls.get('counts',{}).get('mandatory_spelling_targets')!=0: problems.append('mandatory spelling gate was introduced in F2')

loci=arch.get('loci',[]); journeys=arch.get('journeys',[]); challenges=arch.get('challenge_lab',[]); guards=arch.get('scope_guards',[]); conf=arch.get('confusable_sets',[])
if [j.get('journey_id') for j in journeys] != [f'U5-J{i}' for i in range(1,9)]: problems.append('journey IDs are not U5-J1..U5-J8')
if [l.get('locus_id') for l in loci] != [f'U5-L{i:02d}' for i in range(1,51)]: problems.append('locus IDs are not U5-L01..U5-L50')

palace=[]; primary=[]; locus_ids=[]
for l in loci:
    locus_ids.append(l.get('locus_id')); palace += l.get('knowledge_ids',[]); primary.append(l.get('primary_knowledge_id'))
    if l.get('primary_knowledge_id') not in l.get('knowledge_ids',[]): problems.append(f"{l.get('locus_id')} primary ID is not in its knowledge IDs")
    if set(l.get('scene_geometry',{}))!={'left','center','right'}: problems.append(f"{l.get('locus_id')} lacks left/center/right geometry")
    if not all(str(v).strip() for v in l.get('scene_geometry',{}).values()): problems.append(f"{l.get('locus_id')} contains blank scene geometry")
    if not l.get('micro_anchor') or not l.get('title'): problems.append(f"{l.get('locus_id')} lacks title or micro-anchor")
    if l.get('scientific_visual_required') is not True: problems.append(f"{l.get('locus_id')} does not require a scientific visual")
    if l.get('narrative_status')!='ARCHITECTURE_ONLY_NO_STORY_PROSE_F2': problems.append(f"{l.get('locus_id')} has unexpected narrative state")
    if any(k in l for k in ['story_paragraphs','story_open','story_close','narrative_text']): problems.append(f"{l.get('locus_id')} contains story prose during F2")
if len(palace)!=131 or len(set(palace))!=131: problems.append(f'palace mapping is {len(palace)} refs / {len(set(palace))} unique instead of 131/131')
if len(primary)!=50 or len(set(primary))!=50: problems.append('primary anchors are not unique across 50 loci')

challenge_ids={x.get('knowledge_id') for x in challenges}; guard_ids={x.get('knowledge_id') for x in guards}; palace_ids=set(palace)
if palace_ids|challenge_ids|guard_ids != canonical_ids: problems.append('palace + challenge + scope partitions do not cover all 152 canonical records')
if palace_ids&challenge_ids or palace_ids&guard_ids or challenge_ids&guard_ids: problems.append('F2 learning-destination partitions overlap')
if any(canon[k]['scope_class']!='PRACTICE_ONLY' for k in challenge_ids): problems.append('Challenge Lab contains non-PRACTICE_ONLY records')
if any(canon[k]['scope_class']!='SCOPE_GUARD' for k in guard_ids): problems.append('scope-guard partition contains non-scope records')
if any(canon[k]['scope_class'] in {'PRACTICE_ONLY','SCOPE_GUARD'} for k in palace_ids): problems.append('palace mapping consumes practice-only or scope-guard records')

locus_set=set(locus_ids)
for j in journeys:
    if not j.get('working_title') or not j.get('content_focus') or not j.get('setting_logic'): problems.append(f"{j.get('journey_id')} lacks architecture rationale")
    for b in j.get('bundles',[]):
        if not b.get('title') or not b.get('loci'): problems.append(f"{b.get('bundle_id')} is incomplete")
        bad=set(b.get('loci',[]))-locus_set
        if bad: problems.append(f"{b.get('bundle_id')} refers to unknown loci {sorted(bad)}")
for ch in challenges:
    bad=set(ch.get('prerequisite_loci',[]))-locus_set
    if bad: problems.append(f"{ch.get('challenge_id')} has unknown prerequisite loci {sorted(bad)}")
for g in guards:
    bad=set(g.get('supporting_loci',[]))-locus_set
    if bad: problems.append(f"scope guard {g.get('knowledge_id')} has unknown supporting loci {sorted(bad)}")
for c in conf:
    kids=c.get('knowledge_ids',[])
    if len(kids)<2 or len(c.get('terms',[]))<2: problems.append(f"{c.get('set_id')} is not a genuine discrimination set")
    if len(set(kids))<2: problems.append(f"{c.get('set_id')} repeats one knowledge ID instead of contrasting records")
    bad=set(kids)-palace_ids
    if bad: problems.append(f"{c.get('set_id')} includes non-palace IDs {sorted(bad)}")

class_by_id={r['knowledge_id']:r for r in cls['records']}
if set(class_by_id)!=canonical_ids: problems.append('classification IDs differ from canonical IDs')
for k in palace_ids:
    c=class_by_id[k]
    if c.get('locus_id') not in locus_set: problems.append(f'{k} missing valid locus in classification')
    if c.get('exact_name_recall') != bool(canon[k]['exact_name_recall']): problems.append(f'{k} changed F1 exact-name policy during F2')
    if canon[k]['exact_name_recall'] and c.get('name_support')=='NO_EXACT_NAME_GATE': problems.append(f'{k} incorrectly has no exact-name support')
for k in challenge_ids|guard_ids:
    c=class_by_id[k]
    if c.get('locus_id') is not None: problems.append(f'{k} has a permanent locus despite non-palace destination')
    if c.get('exact_name_recall') is not False: problems.append(f'{k} has a student exact-name gate despite non-palace destination')

if status.get('status')!='LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED': problems.append(f"unexpected F2 status {status.get('status')}")
if status.get('architecture_lock')!='LOCKED_F2' or status.get('canonical_lock')!='LOCKED_F1': problems.append('F1/F2 lock state incorrect')
if status.get('student_release') is not False or status.get('preview_release') is not False: problems.append('Unit 5 became student-visible during F2')
if any(status.get(k)!=0 for k in ['journey_count','scene_count','memory_objects','application_challenges']): problems.append('student runtime fields are nonzero during F2')
if (status.get('architecture_journeys'),status.get('architecture_bundles'),status.get('architecture_loci'))!=(8,19,50): problems.append('status architecture counts do not match F2')
if release.get('student_release') is not False or release.get('narrative_story_files')!=0 or release.get('student_runtime_memory_objects')!=0: problems.append('release manifest exposes runtime content during F2')

# F1 scientific lock must remain byte-identical.
f1lock=read(U5/'content-lock-f1.json')
for item in f1lock.get('protected_files',[]):
    p=U5/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']:
        problems.append(f"F1 protected source changed: {item['path']}")
# Units 1-4 released content must remain byte-identical to the supplied U4 F6 baseline.
prot=read(U5/'upstream-u1-u4-protection-f1.json')
if prot.get('protected_file_count')!=216: problems.append('upstream protection manifest no longer contains 216 files')
for item in prot.get('protected_files',[]):
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']:
        problems.append(f"released Units 1-4 file changed: {item['path']}")

required=[
 U5/'architecture'/'learning-classification-f2.json',U5/'architecture'/'palace-architecture-f2.json',U5/'status-f2.json',U5/'f2-release-manifest.json',
 U5/'audit'/'APBIO_Unit5_F2_Classification.xlsx',U5/'content-lock-f2.json',ROOT/'docs'/'UNIT5_F2_ARCHITECTURE.md',ROOT/'docs'/'UNIT5_F2_CLASSIFICATION_MATRIX.md',ROOT/'docs'/'UNIT5_F2_QA.md',ROOT/'docs'/'UNIT5_F2_RELEASE.md'
]
for p in required:
    if not p.exists(): problems.append(f'missing required F2 artifact: {p.relative_to(ROOT)}')
if (U5/'content-lock-f2.json').exists():
    lock=read(U5/'content-lock-f2.json')
    if lock.get('lock_status')!='LOCKED_F2': problems.append('F2 content lock is not LOCKED_F2')
    for rel,item in lock.get('files',{}).items():
        p=U5/rel
        if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']:
            problems.append(f'F2 locked file changed: {rel}')

course=read(ROOT/'content'/'ap-biology'/'course.json')
u5=next((u for u in course['units'] if u['unit_id']=='unit-5'),None)
if not u5: problems.append('Unit 5 missing from course registry')
else:
    if u5.get('status')=='STUDENT_READY':
        if u5.get('student_release') is not True or u5.get('preview_release') is not False: problems.append('course registry F5 state invalid after F2')
    elif u5.get('status') not in {'LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW','F4G_JOURNEYS1_7_POLISHED_DEVELOPER_PREVIEW','F4H_JOURNEYS1_8_POLISHED_DEVELOPER_PREVIEW'}: problems.append('course registry Unit 5 status mismatch')
    if u5.get('architecture_journeys')!=8 or u5.get('architecture_loci')!=50 or u5.get('architecture_lock')!='LOCKED_F2': problems.append('course registry Unit 5 architecture accounting mismatch')
    if u5.get('status') in {'LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED'} and (u5.get('journey_count')!=0 or u5.get('scene_count')!=0): problems.append('pre-F4 course registry contains journey prose')

if problems:
    print('UNIT 5 F2 QA FAIL')
    print('\n'.join(f'- {p}' for p in problems))
    sys.exit(1)
print('UNIT 5 F2 QA PASS')
print({'canonical_records':152,'palace_managed_records':131,'scope_guards':5,'challenge_lab_records':16,'journey_blueprints':8,'bundle_blueprints':19,'permanent_loci':50,'confusable_sets':32,'exact_name_targets':130,'student_release':False})
