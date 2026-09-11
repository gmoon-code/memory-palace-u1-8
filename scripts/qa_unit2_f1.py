from __future__ import annotations
import hashlib, json, sys
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
CATALOG=U2/'source'/'canonical-unit2-f1.json'
LOCK=U2/'content-lock-f1.json'
STATUS=U2/'status.json'
COURSE=ROOT/'content'/'ap-biology'/'course.json'
DOC=ROOT/'docs'/'UNIT2_F1_QA.md'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

d=read(CATALOG); lock=read(LOCK); status=read(STATUS); course=read(COURSE)
problems=[]

# Locked-file integrity
for rel,meta in lock['files'].items():
    p=ROOT/rel
    if not p.exists():
        problems.append(f'Locked file missing: {rel}')
        continue
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    if actual!=meta['sha256']:
        problems.append(f'Locked file hash mismatch: {rel}')

# Required counts
checks={
    'ppt_raw_slides':109,
    'packet_current_ced_crosswalk':11,
    'ced_current_atoms':66,
    'review_flags':20,
    'canonical_catalog':142,
}
for key,expected in checks.items():
    actual=len(d.get(key,[]))
    if actual!=expected: problems.append(f'{key}: {actual}, expected {expected}')

ced_topics={x['topic'] for x in d['ced_current_atoms']}
expected_topics={f'2.{i}' for i in range(1,11)}
if ced_topics!=expected_topics:
    problems.append(f'Current CED topic coverage is {sorted(ced_topics)}, expected 2.1–2.10')

packet_numbers={x['packet_topic'] for x in d['packet_current_ced_crosswalk']}
if packet_numbers!=set(range(1,12)):
    problems.append(f'Legacy packet topic coverage is {sorted(packet_numbers)}, expected 1–11')
if any(x.get('status')!='MAPPED_TO_CURRENT_CED' for x in d['packet_current_ced_crosswalk']):
    problems.append('Not every legacy packet topic is mapped to the current CED')

# Canonical-record integrity
records=d['canonical_catalog']; ids=[x.get('knowledge_id') for x in records]
if len(ids)!=len(set(ids)) or any(not x for x in ids): problems.append('Canonical knowledge IDs are missing or duplicated')
valid_scopes={'AP_REQUIRED','TEACHER_REQUIRED_ENRICHMENT','AP_REQUIRED_EQUATION','AP_REQUIRED_SUPPORT','PRACTICE_ONLY'}
for r in records:
    for field in ['knowledge_id','topic','canonical_label','canonical_verified_statement','scope_class','source_reference','retrieval_demand','canonical_lock']:
        if r.get(field) in ('',None): problems.append(f"{r.get('knowledge_id','?')} missing {field}")
    if r.get('canonical_lock') not in {'LOCKED_F1','LOCKED_WITH_CORRECTION_OR_SCOPE_NOTE'}: problems.append(f"{r.get('knowledge_id')} has invalid F1 lock state {r.get('canonical_lock')}")
    if r.get('canonical_lock')=='LOCKED_WITH_CORRECTION_OR_SCOPE_NOTE' and not r.get('review_flag_id'): problems.append(f"{r.get('knowledge_id')} is correction-locked without a review flag")
    if r.get('scope_class') not in valid_scopes: problems.append(f"{r.get('knowledge_id')} unknown scope {r.get('scope_class')}")
    if r.get('topic') not in expected_topics: problems.append(f"{r.get('knowledge_id')} invalid topic {r.get('topic')}")

flag_ids={x['flag_id'] for x in d['review_flags']}
if len(flag_ids)!=20 or any(x.get('status')!='RESOLVED' for x in d['review_flags']): problems.append('Review flags are not 20 unique resolved records')
for r in records:
    fid=r.get('review_flag_id')
    if fid and fid not in flag_ids: problems.append(f"{r['knowledge_id']} points to unknown review flag {fid}")

scope_counts=Counter(x['scope_class'] for x in records)
expected_scope={'AP_REQUIRED':66,'TEACHER_REQUIRED_ENRICHMENT':64,'AP_REQUIRED_EQUATION':2,'AP_REQUIRED_SUPPORT':1,'PRACTICE_ONLY':9}
if dict(scope_counts)!=expected_scope: problems.append(f'Scope counts {dict(scope_counts)} do not match {expected_scope}')
topic_counts=Counter(x['topic'] for x in records)
expected_topic={'2.1':53,'2.2':10,'2.3':13,'2.4':9,'2.5':12,'2.6':7,'2.7':17,'2.8':10,'2.9':3,'2.10':8}
if dict(topic_counts)!=expected_topic: problems.append(f'Topic counts {dict(topic_counts)} do not match {expected_topic}')

# QA/status/release gate
if d['qa'].get('blocking_missing_resources')!=[]: problems.append('Catalog reports blocking missing resources')
expected_stable_status={
    'canonical_lock':'LOCKED_F1',
    'student_release':False,
    'current_ced_topics':10,
    'legacy_packet_topics_crosswalked':11,
    'teacher_ppt_slides_ingested':109,
    'ced_atoms':66,
    'canonical_records':142,
    'review_flags_resolved':20,
    'blocking_missing_resources':0,
}
for key,val in expected_stable_status.items():
    if status.get(key)!=val: problems.append(f'status.json {key}={status.get(key)!r}, expected {val!r}')
if status.get('status') not in {'SCIENCE_LOCKED_F1_NOT_STUDENT_RELEASED','LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','F4A_JOURNEY1_POLISHED_PREVIEW','F4B_JOURNEY2_POLISHED_PREVIEW','F4C_JOURNEY3_POLISHED_PREVIEW','F4D_JOURNEY4_POLISHED_PREVIEW','F4E_JOURNEY5_POLISHED_PREVIEW','F4F_JOURNEY6_POLISHED_PREVIEW','F4G_ALL_7_JOURNEYS_POLISHED_PREVIEW','STUDENT_READY'}:
    problems.append(f"Unit 2 pipeline status no longer preserves a valid F1-or-later locked state: {status.get('status')}")
if status.get('pipeline_stage') not in {'CANONICAL_SCIENTIFIC_LOCK_COMPLETE','LEARNING_CLASSIFICATION_AND_PALACE_ARCHITECTURE_COMPLETE'}:
    problems.append(f"Unexpected Unit 2 pipeline stage: {status.get('pipeline_stage')}")

u2=next((u for u in course['units'] if u['unit_id']=='unit-2'),None)
if not u2: problems.append('Unit 2 missing from course registry')
else:
    if u2.get('status') not in {'SCIENCE_LOCKED_F1_NOT_STUDENT_RELEASED','LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','F4A_JOURNEY1_POLISHED_PREVIEW','F4B_JOURNEY2_POLISHED_PREVIEW','F4C_JOURNEY3_POLISHED_PREVIEW','F4D_JOURNEY4_POLISHED_PREVIEW','F4E_JOURNEY5_POLISHED_PREVIEW','F4F_JOURNEY6_POLISHED_PREVIEW','F4G_ALL_7_JOURNEYS_POLISHED_PREVIEW','STUDENT_READY'}: problems.append('Course registry Unit 2 status mismatch')
    if u2.get('canonical_lock')!='LOCKED_F1': problems.append('Course registry Unit 2 canonical lock mismatch')

# F1 itself released no student runtime. Later-stage artifacts are allowed only when a finalization manifest exists.
if not (U2/'finalization-f5.json').exists():
    for forbidden in ['memory-objects.json','journeys.json','application-lab.json']:
        if (U2/forbidden).exists(): problems.append(f'Premature Unit 2 student-runtime artifact exists: {forbidden}')

lines=[
    '# Memory Palace V2 · Unit 2 F1 QA','',
    '## Gate','',
    '**Stage F1 verifies source ingestion, current-CED mapping, Campbell-supported scientific correction, canonical locking, and non-release of student mnemonic content.**','',
    '## Accounting','',
    '- Teacher PPT slides: **109 / 109**',
    '- Legacy packet topics crosswalked: **11 / 11**',
    '- Current CED topics: **10 / 10**',
    '- Current CED atoms: **66**',
    '- Locked canonical records: **142**',
    '- Resolved scientific/scope review flags: **20**',
    '- Blocking missing resources: **0**',
    '- Student journeys/scenes/Memory Objects released in F1: **0 / 0 / 0**','',
    '## Canonical scope distribution','',
]
for k in ['AP_REQUIRED','AP_REQUIRED_EQUATION','AP_REQUIRED_SUPPORT','TEACHER_REQUIRED_ENRICHMENT','PRACTICE_ONLY']:
    lines.append(f'- {k}: **{scope_counts.get(k,0)}**')
lines += ['', '## Topic distribution','']
for k in sorted(topic_counts,key=lambda x:tuple(map(int,x.split('.')))):
    lines.append(f'- Topic {k}: **{topic_counts[k]} records**')
lines += ['', '## Result','', '**PASS — Unit 2 F1 scientific/source lock is internally consistent and remains blocked from student narrative release.**' if not problems else '**FAIL**','']
if problems:
    lines += ['### Blocking findings','']+[f'- {p}' for p in problems]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
if problems:
    print('\n'.join(problems));sys.exit(1)
print('Unit 2 F1 QA PASS')
print({'ppt_slides':109,'packet_topics':11,'ced_topics':10,'ced_atoms':66,'canonical_records':142,'review_flags':20,'student_release':False})
