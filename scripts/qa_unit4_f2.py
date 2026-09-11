from __future__ import annotations
import hashlib,json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content'/'ap-biology'/'unit-4'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

problems=[]
src=read(U4/'source'/'canonical-unit4-f1.json')
cls=read(U4/'architecture'/'learning-classification-f2.json')
arch=read(U4/'architecture'/'palace-architecture-f2.json')
status=read(U4/'status-f2.json')
release=read(U4/'f2-release-manifest.json')
canon={r['knowledge_id']:r for r in src['canonical_catalog']}
canonical_ids=set(canon)

if len(canon)!=180: problems.append(f'canonical count {len(canon)} != 180')
if len(cls.get('records',[]))!=180: problems.append('classification does not contain 180 records')
expected_dest={'PALACE_PRIMARY_LOCUS':51,'PALACE_EMBEDDED':111,'CHALLENGE_LAB':15,'SUPPORTING_NON_RUNTIME_SCOPE_GUARD':3}
actual_dest=Counter(r.get('destination') for r in cls.get('records',[]))
if dict(actual_dest)!=expected_dest: problems.append(f'classification destination counts {dict(actual_dest)} != {expected_dest}')
if cls.get('counts',{}).get('exact_name_targets')!=162: problems.append('exact-name palace target count is not 162')
if cls.get('counts',{}).get('mandatory_spelling_targets')!=0: problems.append('F2 introduced mandatory spelling gates')

loci=arch.get('loci',[]); journeys=arch.get('journeys',[]); challenges=arch.get('challenge_lab',[]); guards=arch.get('scope_guards',[]); conf=arch.get('confusable_sets',[])
if len(loci)!=51: problems.append(f'locus count {len(loci)} != 51')
if len(journeys)!=7: problems.append(f'journey count {len(journeys)} != 7')
if sum(len(j.get('bundles',[])) for j in journeys)!=17: problems.append('bundle count != 17')
if len(challenges)!=15: problems.append('challenge destination count != 15')
if len(guards)!=3: problems.append('scope guard count != 3')
if len(conf)!=33: problems.append('confusable-set count != 33')

locus_ids=[l.get('locus_id') for l in loci]
if len(locus_ids)!=len(set(locus_ids)): problems.append('locus IDs are duplicated')
if locus_ids != [f'U4-L{i:02d}' for i in range(1,52)]: problems.append('locus IDs are not sequential U4-L01..U4-L51')
journey_ids=[j.get('journey_id') for j in journeys]
if journey_ids != [f'U4-J{i}' for i in range(1,8)]: problems.append('journey IDs are not sequential U4-J1..U4-J7')

palace=[]; primary=[]
for l in loci:
    kids=l.get('knowledge_ids',[]); palace.extend(kids); primary.append(l.get('primary_knowledge_id'))
    if l.get('primary_knowledge_id') not in kids: problems.append(f"{l.get('locus_id')} primary is not inside its knowledge set")
    if set(l.get('scene_geometry',{}))!={'left','center','right'}: problems.append(f"{l.get('locus_id')} does not have left/center/right geometry")
    if not all(str(v).strip() for v in l.get('scene_geometry',{}).values()): problems.append(f"{l.get('locus_id')} contains blank scene geometry")
    if not l.get('micro_anchor') or not l.get('title'): problems.append(f"{l.get('locus_id')} lacks title or micro-anchor")
    if l.get('scientific_visual_required') is not True: problems.append(f"{l.get('locus_id')} does not require a scientific visual")
    if l.get('narrative_status')!='ARCHITECTURE_ONLY_NO_STORY_PROSE_F2': problems.append(f"{l.get('locus_id')} has unexpected narrative state")
if len(palace)!=162 or len(set(palace))!=162: problems.append(f'palace mapping is {len(palace)} refs / {len(set(palace))} unique instead of 162/162')
if len(primary)!=51 or len(set(primary))!=51: problems.append('primary anchors are not unique across 51 loci')

challenge_ids={x.get('knowledge_id') for x in challenges}; guard_ids={x.get('knowledge_id') for x in guards}; palace_ids=set(palace)
if palace_ids|challenge_ids|guard_ids != canonical_ids: problems.append('palace + challenge + scope partitions do not cover all 180 canonical records')
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
for c in conf:
    kids=c.get('knowledge_ids',[])
    if len(kids)<2 or len(c.get('terms',[]))<2: problems.append(f"{c.get('set_id')} is not a genuine discrimination set")
    bad=set(kids)-palace_ids
    if bad: problems.append(f"{c.get('set_id')} includes non-palace IDs {sorted(bad)}")

class_by_id={r['knowledge_id']:r for r in cls['records']}
if set(class_by_id)!=canonical_ids: problems.append('classification IDs differ from canonical IDs')
for k in palace_ids:
    c=class_by_id[k]
    if c.get('locus_id') not in locus_set: problems.append(f'{k} missing valid locus in classification')
    if c.get('exact_name_recall') is not True: problems.append(f'{k} lost the locked exact-name target during F2')
    if c.get('name_support')=='NO_EXACT_NAME_GATE': problems.append(f'{k} incorrectly has no exact-name gate')
for k in challenge_ids|guard_ids:
    c=class_by_id[k]
    if c.get('locus_id') is not None: problems.append(f'{k} has a permanent locus despite non-palace destination')
    if c.get('exact_name_recall') is not False: problems.append(f'{k} has a student exact-name gate despite non-palace destination')

if status.get('status')!='LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED': problems.append(f"unexpected F2 status {status.get('status')}")
if status.get('architecture_lock')!='LOCKED_F2' or status.get('canonical_lock')!='LOCKED_F1': problems.append('F1/F2 lock state incorrect')
if status.get('student_release') is not False or status.get('preview_release') is not False: problems.append('Unit 4 became student-visible during F2')
if any(status.get(k)!=0 for k in ['journey_count','scene_count','memory_objects','application_challenges']): problems.append('student runtime fields are nonzero during F2')
if (status.get('architecture_journeys'),status.get('architecture_bundles'),status.get('architecture_loci'))!=(7,17,51): problems.append('status architecture counts do not match F2')
if release.get('student_release') is not False or release.get('narrative_story_files')!=0 or release.get('student_runtime_memory_objects')!=0: problems.append('release manifest exposes runtime content during F2')

f1lock=read(U4/'content-lock-f1.json')
for item in f1lock.get('protected_files',[]):
    p=U4/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']:
        problems.append(f"F1 protected source changed: {item['path']}")

required=[
 U4/'architecture'/'learning-classification-f2.json',U4/'architecture'/'palace-architecture-f2.json',U4/'status-f2.json',U4/'f2-release-manifest.json',
 U4/'audit'/'APBIO_Unit4_F2_Classification.xlsx',U4/'content-lock-f2.json',ROOT/'docs'/'UNIT4_F2_ARCHITECTURE.md',ROOT/'docs'/'UNIT4_F2_CLASSIFICATION_MATRIX.md',ROOT/'docs'/'UNIT4_F2_QA.md'
]
for p in required:
    if not p.exists(): problems.append(f'missing required F2 artifact: {p.relative_to(ROOT)}')
if (U4/'content-lock-f2.json').exists():
    lock=read(U4/'content-lock-f2.json')
    if lock.get('lock_status')!='LOCKED_F2': problems.append('F2 content lock is not LOCKED_F2')
    for rel,item in lock.get('files',{}).items():
        p=U4/rel
        if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']:
            problems.append(f'F2 locked file changed: {rel}')

course=read(ROOT/'content'/'ap-biology'/'course.json')
u4=next((u for u in course['units'] if u['unit_id']=='unit-4'),None)
if not u4: problems.append('Unit 4 missing from course registry')
else:
    if u4.get('status') not in {'LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED'}: problems.append('course registry Unit 4 status mismatch')
    if u4.get('architecture_journeys')!=7 or u4.get('architecture_loci')!=51 or u4.get('architecture_lock')!='LOCKED_F2': problems.append('course registry Unit 4 architecture accounting mismatch')
    if u4.get('student_release') is not False or u4.get('journey_count')!=0 or u4.get('scene_count')!=0: problems.append('course registry released Unit 4 runtime content')

if problems:
    print('UNIT 4 F2 QA FAIL')
    print('\n'.join(f'- {p}' for p in problems))
    sys.exit(1)
print('UNIT 4 F2 QA PASS')
print({'canonical_records':180,'palace_managed_records':162,'scope_guards':3,'challenge_lab_records':15,'journey_blueprints':7,'bundle_blueprints':17,'permanent_loci':51,'confusable_sets':33,'student_release':False})
