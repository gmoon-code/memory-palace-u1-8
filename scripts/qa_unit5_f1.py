from __future__ import annotations
import hashlib,json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content/ap-biology/unit-5'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
problems=[]
canonical=read(U5/'source/canonical-unit5-f1.json')
coverage=read(U5/'source/coverage-manifest-f1.json')
lock=read(U5/'content-lock-f1.json')
release=read(U5/'f1-release-manifest.json')
status=read(U5/'status.json')
records=canonical['canonical_catalog']; slides=canonical['ppt_raw_slides']; ced=canonical['ced_current_atoms']; flags=canonical['review_flags']; assess=canonical['assessment_semantic_crosswalk']
if len(records)!=152: problems.append(f'canonical record count {len(records)} != 152')
if len(slides)!=112: problems.append(f'PPT slide count {len(slides)} != 112')
if len(ced)!=34: problems.append(f'CED atom count {len(ced)} != 34')
if len(flags)!=37: problems.append(f'review flag count {len(flags)} != 37')
if len(assess)!=10: problems.append(f'assessment crosswalk count {len(assess)} != 10')
ids=[r['knowledge_id'] for r in records]
if ids!=[f'U5-K-{i:03d}' for i in range(1,153)]: problems.append('canonical IDs are not sequential U5-K-001..U5-K-152')
if len(ids)!=len(set(ids)): problems.append('duplicate canonical IDs')
if any(r.get('canonical_lock')!='LOCKED_F1' for r in records): problems.append('one or more canonical records are not LOCKED_F1')
if any(not r.get('canonical_label') or not r.get('canonical_verified_statement') for r in records): problems.append('one or more canonical records lack label or verified statement')
expected={'AP_REQUIRED':34,'TEACHER_REQUIRED_ENRICHMENT':97,'PRACTICE_ONLY':16,'SCOPE_GUARD':5}
sc=dict(Counter(r['scope_class'] for r in records))
if sc!=expected: problems.append(f'scope accounting {sc} != {expected}')
if [s['slide'] for s in slides]!=list(range(1,113)): problems.append('PPT raw slide ledger is not slides 1..112')
allowed={'MAPPED','MAPPED_VISUAL','PRESERVED_METADATA','PRESERVED_RAW'}
if any(s['coverage_status'] not in allowed for s in slides): problems.append('invalid slide coverage status')
if any((not s['mapped_knowledge_ids']) and s['coverage_status'] not in {'PRESERVED_METADATA','PRESERVED_RAW'} for s in slides): problems.append('mapped slide missing canonical mappings')
known=set(ids)
for s in slides:
    bad=set(s.get('mapped_knowledge_ids',[]))-known
    if bad: problems.append(f"slide {s['slide']} maps unknown IDs {sorted(bad)}")
ced_topics={a['topic'] for a in ced}
if ced_topics!={'5.1','5.2','5.3','5.4','5.5'}: problems.append(f'CED topics incomplete: {sorted(ced_topics)}')
if any(a['scope_class']!='AP_REQUIRED' for a in ced): problems.append('one or more current CED atoms are not AP_REQUIRED')
for f in flags:
    if f.get('status')!='RESOLVED' or not f.get('resolution'): problems.append(f"unresolved/incomplete flag {f.get('review_flag_id')}")
if len({f['review_flag_id'] for f in flags})!=37: problems.append('review flag IDs are incomplete or duplicated')
assess_topics={t for a in assess for t in a['current_topics']}
if assess_topics!={'5.1','5.2','5.3','5.4','5.5'}: problems.append(f'assessment crosswalk misses topics: {sorted(assess_topics)}')
for a in assess:
    if a['source']!='APBIO-U5-PPT.pdf': problems.append(f"unexpected assessment source {a['source']}")
    if not a['mapped_knowledge_ids']: problems.append(f"assessment {a['assessment_id']} has no mappings")
    bad=set(a['mapped_knowledge_ids'])-known
    if bad: problems.append(f"assessment {a['assessment_id']} maps unknown IDs {sorted(bad)}")
if coverage['ppt_coverage']['unmapped']!=0: problems.append('coverage reports unmapped slides')
if coverage['student_runtime']!={'journeys':0,'scenes':0,'memory_objects':0,'application_challenges':0,'student_release':False}: problems.append('F1 runtime boundary broken')
if release.get('student_release') is not False: problems.append('Unit 5 F1 release manifest incorrectly exposes students')
if status.get('status')!='STUDENT_READY' and status.get('student_release') is not False: problems.append('Unit 5 pre-F5 status boundary invalid')
for k in ('journeys','scenes','memory_objects','application_challenges'):
    if release.get(k)!=0: problems.append(f'F1 runtime field {k} is not zero')
if release.get('scientific_content_lock')!='LOCKED_F1' or lock.get('lock_status')!='LOCKED_F1': problems.append('F1 lock is not LOCKED_F1')
# Pleiotropy coverage repair.
pleio=[r for r in records if r['canonical_label'].strip().casefold()=='pleiotropy']
if not pleio or not any(r['scope_class']=='AP_REQUIRED' and r['topic']=='5.4' for r in pleio): problems.append('AP-required pleiotropy coverage repair missing')
# Protected F1 science files.
for item in lock['protected_files']:
    p=U5/item['path']
    if not p.exists(): problems.append(f"protected Unit 5 file missing: {item['path']}"); continue
    if p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f"protected Unit 5 file changed: {item['path']}")
# Exact supplied U1-U4 baseline bytes must remain intact.
up=read(U5/'upstream-u1-u4-protection-f1.json')
if up.get('baseline_package_sha256')!='e372a71832ca74997fb827b222a8666d9d0c06abbb34a6b9f856c261a14bc9bb': problems.append('wrong Units 1–4 baseline checksum')
if up.get('protected_file_count')!=216: problems.append('Units 1–4 protection manifest does not contain 216 files')
for item in up.get('protected_files',[]):
    p=ROOT/item['path']
    if not p.exists(): problems.append(f"released U1-U4 file missing: {item['path']}"); continue
    if p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f"released U1-U4 file changed: {item['path']}")
# Course registry and required artifacts.
course=read(ROOT/'content/ap-biology/course.json'); u5=next((u for u in course['units'] if u['unit_id']=='unit-5'),None)
if not u5: problems.append('Unit 5 missing from course registry')
elif u5.get('status')=='STUDENT_READY':
    if u5.get('student_release') is not True or u5.get('canonical_records')!=152: problems.append('course registry Unit 5 F5 state invalid after F1')
elif u5.get('status') not in {'SCIENCE_LOCKED_F1_NOT_STUDENT_RELEASED','LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW','F4G_JOURNEYS1_7_POLISHED_DEVELOPER_PREVIEW','F4H_JOURNEYS1_8_POLISHED_DEVELOPER_PREVIEW'} or u5.get('student_release') is not False or u5.get('canonical_records')!=152: problems.append('course registry Unit 5 F1-compatible state mismatch')
required=[U5/'source/canonical-unit5-f1.json',U5/'source/coverage-manifest-f1.json',U5/'audit/F1_SOURCE_AUDIT.md',U5/'audit/F1_REVIEW_FLAGS.md',U5/'audit/APBIO_Unit5_F1_Source_Lock.xlsx',U5/'content-lock-f1.json',U5/'f1-release-manifest.json',U5/'status.json',U5/'upstream-u1-u4-protection-f1.json',ROOT/'docs/UNIT5_F1_QA.md',ROOT/'docs/UNIT5_F1_RELEASE.md']
for p in required:
    if not p.exists(): problems.append(f'missing required artifact: {p.relative_to(ROOT)}')
if problems:
    print('UNIT 5 F1 QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT 5 F1 QA PASS')
print({'ppt_slides':112,'ced_topics':5,'ced_atoms':34,'canonical_records':152,'scope_counts':expected,'review_flags_resolved':37,'assessment_semantic_crosswalks':10,'protected_u1_u4_files':216,'student_release':False})
