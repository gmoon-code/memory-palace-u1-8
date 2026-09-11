from __future__ import annotations
import hashlib, json, sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content'/'ap-biology'/'unit-4'

def read(path: Path): return json.loads(path.read_text(encoding='utf-8'))
def sha(path: Path): return hashlib.sha256(path.read_bytes()).hexdigest()

problems=[]
canonical=read(U4/'source'/'canonical-unit4-f1.json')
coverage=read(U4/'source'/'coverage-manifest-f1.json')
lock=read(U4/'content-lock-f1.json')
release=read(U4/'f1-release-manifest.json')
status=read(U4/'status.json')  # latest stage status; F1 zero-runtime accounting comes from the immutable F1 release manifest
records=canonical.get('canonical_catalog',[])
slides=canonical.get('ppt_raw_slides',[])
ced=canonical.get('ced_current_atoms',[])
flags=canonical.get('review_flags',[])
assess=canonical.get('assessment_semantic_crosswalk',[])

if len(records)!=180: problems.append(f'canonical record count {len(records)} != 180')
if len(slides)!=85: problems.append(f'PPT slide count {len(slides)} != 85')
if len(ced)!=38: problems.append(f'CED atom count {len(ced)} != 38')
if len(flags)!=39: problems.append(f'review flag count {len(flags)} != 39')
if len(assess)!=9: problems.append(f'assessment crosswalk count {len(assess)} != 9')

ids=[r.get('knowledge_id') for r in records]
if len(ids)!=len(set(ids)): problems.append('canonical knowledge IDs are not unique')
if ids != [f'U4-K-{i:03d}' for i in range(1,181)]: problems.append('canonical knowledge IDs are not sequential U4-K-001..U4-K-180')
if any(r.get('canonical_lock')!='LOCKED_F1' for r in records): problems.append('one or more canonical records are not LOCKED_F1')
if any(not r.get('canonical_label') or not r.get('canonical_verified_statement') for r in records): problems.append('one or more canonical records lack label or verified statement')

scope=Counter(r.get('scope_class') for r in records)
expected_scope={'AP_REQUIRED':38,'TEACHER_REQUIRED_ENRICHMENT':124,'PRACTICE_ONLY':15,'SCOPE_GUARD':3}
if dict(scope)!=expected_scope: problems.append(f'scope accounting {dict(scope)} != {expected_scope}')

slide_nums=[s.get('slide') for s in slides]
if slide_nums!=list(range(1,86)): problems.append('PPT raw slide ledger is not exactly slides 1..85')
allowed_status={'MAPPED','MAPPED_VISUAL','PRESERVED_METADATA','PRESERVED_RAW'}
if any(s.get('coverage_status') not in allowed_status for s in slides): problems.append('one or more PPT slides are neither mapped nor explicitly preserved')
if any(not s.get('mapped_knowledge_ids') and s.get('coverage_status') not in {'PRESERVED_METADATA','PRESERVED_RAW'} for s in slides): problems.append('one or more mapped PPT slides have no mapped knowledge IDs')
known=set(ids)
for s in slides:
    bad=set(s.get('mapped_knowledge_ids',[]))-known
    if bad: problems.append(f"slide {s.get('slide')} maps unknown knowledge IDs {sorted(bad)}")

ced_topics={a.get('topic') for a in ced}
if ced_topics!={'4.1','4.2','4.3','4.4','4.5','4.6'}: problems.append(f'CED topics incomplete: {sorted(ced_topics)}')
if any(a.get('scope_class')!='AP_REQUIRED' for a in ced): problems.append('one or more current CED atoms are not AP_REQUIRED')

for f in flags:
    if str(f.get('status','')).upper()!='RESOLVED': problems.append(f"unresolved review flag {f.get('flag_id')}")
    if not f.get('resolution'): problems.append(f"review flag {f.get('flag_id')} lacks a resolution")
flag_ids={f.get('review_flag_id') for f in flags}
if len(flag_ids)!=39 or None in flag_ids: problems.append('review flag IDs are incomplete or duplicated')

assess_topics=set()
for a in assess:
    assess_topics.update(a.get('current_topics',[]))
    if a.get('source')!='APBIO-U4-SG.pdf': problems.append(f"unexpected assessment source for {a.get('assessment_id')}")
    if not a.get('mapped_knowledge_ids'): problems.append(f"assessment item {a.get('assessment_id')} has no semantic mappings")
    bad=set(a.get('mapped_knowledge_ids',[]))-known
    if bad: problems.append(f"assessment item {a.get('assessment_id')} maps unknown IDs {sorted(bad)}")
if assess_topics!={'4.1','4.2','4.3','4.4','4.5','4.6'}: problems.append(f'assessment semantic crosswalk misses current topics: {sorted(assess_topics)}')

if coverage.get('ppt_coverage',{}).get('unmapped')!=0: problems.append('coverage manifest reports unmapped PPT slides')
if coverage.get('student_runtime')!={'journeys':0,'scenes':0,'memory_objects':0,'application_challenges':0,'student_release':False}: problems.append('F1 student runtime is not fully blocked')
if release.get('student_release') is not False: problems.append('immutable F1 release manifest incorrectly exposes student runtime')
for k in ('journeys','scenes','memory_objects','application_challenges'):
    if release.get(k)!=0:
        problems.append(f'F1 release manifest runtime field {k} is not zero')
if release.get('scientific_content_lock')!='LOCKED_F1' or lock.get('lock_status')!='LOCKED_F1': problems.append('scientific content lock is not LOCKED_F1')

for item in lock.get('protected_files',[]):
    p=U4/item['path']
    if not p.exists(): problems.append(f"protected file missing: {item['path']}"); continue
    if p.stat().st_size!=item['bytes']: problems.append(f"protected file byte count changed: {item['path']}")
    if sha(p)!=item['sha256']: problems.append(f"protected file hash changed: {item['path']}")

course=read(ROOT/'content'/'ap-biology'/'course.json')
u4=next((u for u in course['units'] if u['unit_id']=='unit-4'),None)
if not u4: problems.append('Unit 4 missing from course registry')
else:
    if u4.get('status') not in {'SCIENCE_LOCKED_F1_NOT_STUDENT_RELEASED','LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','STUDENT_READY'} and not str(u4.get('status','')).startswith('F4'): problems.append(f"unexpected course Unit 4 status {u4.get('status')}")
    if u4.get('canonical_records')!=180 or u4.get('ced_atoms')!=38: problems.append('course registry F1 accounting mismatch')
    if u4.get('status')!='STUDENT_READY' and u4.get('student_release') is not False: problems.append('pre-F5 course registry exposes Unit 4 as student release')

required=[
 U4/'source'/'canonical-unit4-f1.json',U4/'source'/'coverage-manifest-f1.json',U4/'audit'/'F1_SOURCE_AUDIT.md',
 U4/'audit'/'F1_REVIEW_FLAGS.md',U4/'audit'/'APBIO_Unit4_F1_Source_Lock.xlsx',U4/'content-lock-f1.json',U4/'f1-release-manifest.json',U4/'status.json',ROOT/'docs'/'UNIT4_F1_QA.md'
]
for p in required:
    if not p.exists(): problems.append(f'missing required F1 artifact: {p.relative_to(ROOT)}')

if problems:
    print('UNIT 4 F1 QA FAIL')
    print('\n'.join(f'- {p}' for p in problems))
    sys.exit(1)
print('UNIT 4 F1 QA PASS')
print({'ppt_slides':85,'ced_topics':6,'ced_atoms':38,'canonical_records':180,'review_flags_resolved':39,'assessment_semantic_crosswalks':9,'student_release':False})
