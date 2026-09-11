from __future__ import annotations
import hashlib,json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U6=ROOT/'content/ap-biology/unit-6'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
problems=[]
canonical=read(U6/'source/canonical-unit6-f1.json')
coverage=read(U6/'source/coverage-manifest-f1.json')
lock=read(U6/'content-lock-f1.json')
release=read(U6/'f1-release-manifest.json')
status=read(U6/'status.json')
records=canonical['canonical_catalog']; slides=canonical['ppt_raw_slides']; ced=canonical['ced_current_atoms']; flags=canonical['review_flags']; assess=canonical['assessment_semantic_crosswalk']; cross=canonical['cross_unit_dependencies']
if len(records)!=202: problems.append(f'canonical record count {len(records)} != 202')
if len(slides)!=121: problems.append(f'PPT slide count {len(slides)} != 121')
if len(ced)!=89: problems.append(f'CED atom count {len(ced)} != 89')
if len(flags)!=39: problems.append(f'review flag count {len(flags)} != 39')
if len(assess)!=12: problems.append(f'assessment crosswalk count {len(assess)} != 12')
if len(cross)!=5: problems.append(f'cross-unit dependency count {len(cross)} != 5')
ids=[r['knowledge_id'] for r in records]
if ids!=[f'U6-K-{i:03d}' for i in range(1,203)]: problems.append('canonical IDs are not sequential U6-K-001..U6-K-202')
if len(ids)!=len(set(ids)): problems.append('duplicate canonical IDs')
if any(r.get('canonical_lock')!='LOCKED_F1' for r in records): problems.append('one or more canonical records are not LOCKED_F1')
if any(not r.get('canonical_label') or not r.get('canonical_verified_statement') for r in records): problems.append('one or more canonical records lack label or verified statement')
expected={'AP_REQUIRED':83,'TEACHER_REQUIRED_ENRICHMENT':78,'PRACTICE_ONLY':16,'SCOPE_GUARD':25}
sc=dict(Counter(r['scope_class'] for r in records))
if sc!=expected: problems.append(f'scope accounting {sc} != {expected}')
if [s['slide'] for s in slides]!=list(range(1,122)): problems.append('PPT raw slide ledger is not slides 1..121')
allowed={'MAPPED','MAPPED_VISUAL','PRESERVED_METADATA'}
if any(s['coverage_status'] not in allowed for s in slides): problems.append('invalid slide coverage status')
metadata=set(coverage['ppt_coverage']['metadata_only_slides'])
if any((not s['mapped_knowledge_ids']) and s['slide'] not in metadata for s in slides): problems.append('substantive slide missing canonical mappings')
known=set(ids)
for s in slides:
    bad=set(s.get('mapped_knowledge_ids',[]))-known
    if bad: problems.append(f"slide {s['slide']} maps unknown IDs {sorted(bad)}")
ced_topics={a['topic'] for a in ced}
if ced_topics!={'6.1','6.2','6.3','6.4','6.5','6.6','6.7','6.8'}: problems.append(f'CED topics incomplete: {sorted(ced_topics)}')
cedids={a['ced_id'] for a in ced}
record_cedids={r['ced_id'] for r in records if r.get('ced_id')}
if cedids-record_cedids: problems.append(f'CED atoms missing canonical lock records: {sorted(cedids-record_cedids)}')
for f in flags:
    if f.get('status')!='RESOLVED' or not f.get('resolution'): problems.append(f"unresolved/incomplete flag {f.get('review_flag_id')}")
if len({f['review_flag_id'] for f in flags})!=39: problems.append('review flag IDs are incomplete or duplicated')
assess_topics={t for a in assess for t in a['current_topics']}
if assess_topics!={'6.1','6.2','6.3','6.4','6.5','6.7','6.8'}: problems.append(f'assessment crosswalk topic set unexpected: {sorted(assess_topics)}')
for a in assess:
    if a['source']!='APBIO-U6-PPT.pdf': problems.append(f"unexpected assessment source {a['source']}")
    if not a['mapped_knowledge_ids']: problems.append(f"assessment {a['assessment_id']} has no mappings")
    bad=set(a['mapped_knowledge_ids'])-known
    if bad: problems.append(f"assessment {a['assessment_id']} maps unknown IDs {sorted(bad)}")
if coverage['ppt_coverage']['unmapped']!=0: problems.append('coverage reports unmapped slides')
if coverage['student_runtime']!={'journeys':0,'scenes':0,'memory_objects':0,'application_challenges':0,'student_release':False}: problems.append('F1 runtime boundary broken')
if release.get('student_release') is not False: problems.append('Unit 6 F1 release manifest incorrectly exposes students')
for k in ('journeys','scenes','memory_objects','application_challenges'):
    if release.get(k)!=0: problems.append(f'F1 runtime field {k} is not zero')
if release.get('scientific_content_lock')!='LOCKED_F1' or lock.get('lock_status')!='LOCKED_F1': problems.append('F1 lock is not LOCKED_F1')

allowed_current={'SCIENCE_LOCKED_F1_NOT_STUDENT_RELEASED','LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
if status.get('status') not in allowed_current: problems.append('Unit 6 status boundary invalid')
elif status.get('status')=='STUDENT_READY' and status.get('student_release') is not True: problems.append('Unit 6 later-stage student release flag invalid')
elif status.get('status')!='STUDENT_READY' and status.get('student_release') is not False: problems.append('Unit 6 pre-F5 student release flag invalid')
# Required current-CED coverage repairs and scientific corrections.
labels={r['canonical_label']:r for r in records}
required_labels=['Constitutive and inducible expression','Promoter/enhancer recruitment of transcription machinery','Regulatory-sequence position','Viral recombination','PCR denaturation','PCR primer annealing','PCR extension','Bacterial transformation as biotechnology','Conserved reproductive sources of variation']
for label in required_labels:
    r=labels.get(label)
    if not r or r['scope_class']!='AP_REQUIRED': problems.append(f'missing AP-required coverage repair: {label}')
checks={
 'Ribosomal subunit sizes':['30S','50S','40S','60S'],
 'Retroviral reverse transcription':['host genome'],
 'Tryptophan as corepressor':['corepressor'],
 'lac structural gene products':['β-galactosidase'],
 'Near universality of genetic code':['Nearly all'],
 'Frameshift mutation':['not in a multiple of three'],
}
for label,needles in checks.items():
    r=labels.get(label)
    if not r: problems.append(f'missing corrected record: {label}'); continue
    text=r['canonical_verified_statement']
    for n in needles:
        if n.casefold() not in text.casefold(): problems.append(f'corrected record {label} missing {n}')
# Protected F1 science files.
for item in lock['protected_files']:
    p=U6/item['path']
    if not p.exists(): problems.append(f"protected Unit 6 file missing: {item['path']}"); continue
    if p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f"protected Unit 6 file changed: {item['path']}")
# Exact supplied U1-U5 baseline bytes remain intact.
up=read(U6/'upstream-u1-u5-protection-f1.json')
if up.get('baseline_package_sha256')!='453d82f55947cad203025e52b50f3dd41adf624fdef465fdddcf29cf4bc80b74': problems.append('wrong Units 1–5 baseline checksum')
if up.get('protected_file_count')!=291: problems.append('Units 1–5 protection manifest does not contain 291 files')
for item in up.get('protected_files',[]):
    p=ROOT/item['path']
    if not p.exists(): problems.append(f"released U1-U5 file missing: {item['path']}"); continue
    if p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f"released U1-U5 file changed: {item['path']}")
# Course registry and source-PDF hygiene.
course=read(ROOT/'content/ap-biology/course.json'); u6=next((u for u in course['units'] if u['unit_id']=='unit-6'),None)
if not u6: problems.append('Unit 6 missing from course registry')
elif u6.get('status') not in allowed_current or u6.get('canonical_records')!=202: problems.append('course registry Unit 6 F1 state mismatch')
elif u6.get('status')=='STUDENT_READY' and u6.get('student_release') is not True: problems.append('course registry Unit 6 later-stage release mismatch')
elif u6.get('status')!='STUDENT_READY' and u6.get('student_release') is not False: problems.append('course registry Unit 6 pre-F5 release mismatch')
for n in range(1,6):
    u=next((u for u in course['units'] if u['unit_id']==f'unit-{n}'),None)
    if not u or u.get('status')!='STUDENT_READY': problems.append(f'upstream Unit {n} is no longer STUDENT_READY')
for p in ROOT.rglob('*.pdf'):
    problems.append(f'forbidden source PDF in repository: {p.relative_to(ROOT)}')
required=[U6/'source/canonical-unit6-f1.json',U6/'source/coverage-manifest-f1.json',U6/'audit/F1_SOURCE_AUDIT.md',U6/'audit/F1_REVIEW_FLAGS.md',U6/'audit/APBIO_Unit6_F1_Source_Lock.xlsx',U6/'content-lock-f1.json',U6/'f1-release-manifest.json',U6/'status.json',U6/'upstream-u1-u5-protection-f1.json',ROOT/'docs/UNIT6_F1_QA.md',ROOT/'docs/UNIT6_F1_RELEASE.md']
for p in required:
    if not p.exists(): problems.append(f'missing required artifact: {p.relative_to(ROOT)}')
if problems:
    print('UNIT 6 F1 QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('UNIT 6 F1 QA PASS')
print({'slides':121,'ced_topics':8,'ced_atoms':89,'canonical_records':202,'scope_counts':sc,'flags':39,'assessments':12,'cross_unit':5,'runtime':0,'upstream_protected':291})
