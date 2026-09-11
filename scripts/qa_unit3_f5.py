from __future__ import annotations
import json,hashlib,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content'/'ap-biology'/'unit-3'
DOC=ROOT/'docs'/'UNIT3_F5_RELEASE_AUDIT.md'
MATRIX=ROOT/'docs'/'UNIT3_F5_REVIEW_AND_CHALLENGE_MATRIX.md'

def read(rel): return json.loads((U3/rel).read_text(encoding='utf-8'))
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
problems=[]
canon=read('source/canonical-unit3-f1.json')['canonical_catalog']; canon_by={r['knowledge_id']:r for r in canon}
cls=read('architecture/learning-classification-f2.json')['records']; cls_by={r['knowledge_id']:r for r in cls}
arch=read('architecture/palace-architecture-f2.json')
journeys=[read(f'journeys/U3-J{i}.json') for i in range(1,8)]
lab=read('application-lab.json'); review=read('review-manifest-f5.json'); mixed=read('mixed-discrimination-f5.json'); guards=read('scope-guards-f5.json'); final=read('finalization-f5.json'); status=read('status-f5.json'); lock=read('content-lock-f5.json'); release=read('f5-release-manifest.json')

# Canonical partition
story_ids=[oid for j in journeys for s in j['scenes'] for oid in s['object_ids']]
challenge_ids=[x['knowledge_id'] for x in lab['items']]
guard_ids=[x['knowledge_id'] for x in guards['guards']]
all_ids={r['knowledge_id'] for r in canon}
if len(canon)!=186: problems.append(f'Canonical count {len(canon)} != 186')
if len(story_ids)!=171 or len(set(story_ids))!=171: problems.append(f'Story accounting {len(story_ids)} refs / {len(set(story_ids))} unique != 171/171')
if len(challenge_ids)!=11 or len(set(challenge_ids))!=11: problems.append('Challenge accounting is not 11/11 unique')
if len(guard_ids)!=4 or len(set(guard_ids))!=4: problems.append('Scope-guard accounting is not 4/4 unique')
parts=[set(story_ids),set(challenge_ids),set(guard_ids)]
if any(parts[i]&parts[j] for i in range(3) for j in range(i+1,3)): problems.append('Canonical destination partitions overlap')
if set().union(*parts)!=all_ids: problems.append('Story + challenge + scope guards do not account for all canonical records')
# Classification must agree with final disposition.
for kid in story_ids:
    if not cls_by[kid]['destination'].startswith('PALACE_'): problems.append(f'{kid} is in story but architecture destination is {cls_by[kid]["destination"]}')
for kid in challenge_ids:
    if cls_by[kid]['destination']!='CHALLENGE_LAB': problems.append(f'{kid} challenge destination mismatch')
for kid in guard_ids:
    if cls_by[kid]['scope_class']!='SCOPE_GUARD' or cls_by[kid]['destination']!='SUPPORTING_NON_RUNTIME_SCOPE_GUARD': problems.append(f'{kid} scope guard destination mismatch')

# Challenge Lab content integrity
if lab['challenge_count']!=11 or lab['practice_only_runtime_count']!=11: problems.append('Challenge Lab counts are not 11')
for x in lab['items']:
    kid=x['knowledge_id']
    if x['canonical_statement']!=canon_by[kid]['canonical_verified_statement']: problems.append(f'{kid} challenge canonical statement drift')
    for fld in ('prompt','answer_guide','story_hint','success_criterion'):
        if len(str(x.get(fld,'')))<25: problems.append(f'{kid} challenge {fld} is too thin')

# Exact-name review completeness and leakage protection.
expected_exact=[r['knowledge_id'] for r in cls if r['exact_name_recall']]
if len(expected_exact)!=126: problems.append(f'Architecture exact-name count {len(expected_exact)} != 126')
if review['target_count']!=126 or len(review['targets'])!=126: problems.append('Review manifest target count is not 126')
review_ids=[x['knowledge_id'] for x in review['targets']]
if set(review_ids)!=set(expected_exact) or len(review_ids)!=len(set(review_ids)): problems.append('Review manifest does not exactly match architecture exact-name targets')
for x in review['targets']:
    answer=x['target_answer'].strip()
    prompt=x['prompt']; hint=x['hint']
    if not prompt.startswith('Which exact Unit 3 name matches this scientific description?'): problems.append(f'{x["knowledge_id"]} review prompt format mismatch')
    if answer.casefold() in prompt.casefold(): problems.append(f'{x["knowledge_id"]} review prompt leaks full target answer')
    if answer.casefold() in hint.casefold(): problems.append(f'{x["knowledge_id"]} review hint leaks full target answer')
    if x['spelling_policy']!='ADAPTIVE_SUPPORT_ONLY_NO_MANDATORY_SPELLING_GATE': problems.append(f'{x["knowledge_id"]} unexpected spelling policy')
if review.get('mandatory_spelling_targets')!=0: problems.append('Unit 3 must not have a mandatory spelling gate')

# Mixed discrimination: exact architecture sets, valid choices, no answer in question prompt.
arch_sets={x['set_id']:x for x in arch['confusable_sets']}
if len(arch_sets)!=28 or mixed['set_count']!=28 or len(mixed['sets'])!=28: problems.append('Mixed discrimination set count != 28')
if mixed['question_count']!=78: problems.append(f'Mixed discrimination question count {mixed["question_count"]} != 78')
for s in mixed['sets']:
    base=arch_sets.get(s['set_id'])
    if not base: problems.append(f'Unknown mixed set {s["set_id"]}'); continue
    if s['knowledge_ids']!=base['knowledge_ids'] or s['terms']!=base['terms']: problems.append(f'{s["set_id"]} differs from F2 architecture')
    if s['initial_delay_hours']<48: problems.append(f'{s["set_id"]} mixed practice begins too early')
    if len(s['questions'])!=len(s['terms']): problems.append(f'{s["set_id"]} does not contain one question per target term')
    for q in s['questions']:
        if q['answer'] not in q['choices']: problems.append(f'{q["question_id"]} answer missing from choices')
        if q['answer'].casefold() in q['prompt'].casefold(): problems.append(f'{q["question_id"]} prompt leaks answer')
        if q['explanation']!=canon_by[q['knowledge_id']]['canonical_verified_statement']: problems.append(f'{q["question_id"]} explanation drift')

# Four scope guards are non-runtime and preserve locked wording.
expected_guards={'U3-K-069','U3-K-129','U3-K-139','U3-K-166'}
if set(guard_ids)!=expected_guards: problems.append(f'Scope guard IDs mismatch: {guard_ids}')
for g in guards['guards']:
    kid=g['knowledge_id']
    if g['canonical_statement']!=canon_by[kid]['canonical_verified_statement']: problems.append(f'{kid} scope guard wording drift')
    if g['student_runtime'] or g['permanent_palace'] or g['challenge_lab']: problems.append(f'{kid} scope guard was incorrectly made runtime')

# Narrative totals remain as the already-locked F4 result.
if len(journeys)!=7 or sum(len(j['scenes']) for j in journeys)!=54: problems.append('Journey/scene counts changed')
if sum(j['checkpoint_count'] for j in journeys)!=18: problems.append('Quick Recall count changed from 18')
if sum(len(s['object_ids']) for j in journeys for s in j['scenes'])!=171: problems.append('Story record total changed')

# Historical Unit 3 locks F1-F4G remain immutable after deterministic rebuild.
def check_historical_lock(lockname):
    old=read(lockname)
    if 'protected_files' in old:
        entries=[(U3/x['path'],x['sha256'],x['path']) for x in old['protected_files']]
    else:
        entries=[]
        for rel,meta in old.get('files',{}).items():
            expected=meta['sha256'] if isinstance(meta,dict) else meta
            path=(ROOT/rel) if rel.startswith('content/') else (U3/rel)
            entries.append((path,expected,rel))
    for path,expected,label in entries:
        if not path.exists() or digest(path)!=expected: problems.append(f'Historical lock changed: {lockname} {label}')
for lockname in ['content-lock-f1.json','content-lock-f2.json','content-lock-f3.json','content-lock-f4a.json','content-lock-f4b.json','content-lock-f4c.json','content-lock-f4d.json','content-lock-f4e.json','content-lock-f4f.json','content-lock-f4g.json']:
    check_historical_lock(lockname)
for rel,expected in lock['files'].items():
    p=U3/rel
    if not p.exists() or digest(p)!=expected: problems.append(f'F5 content lock mismatch: {rel}')

# Release status and finalization.
for k,v in {'canonical_records':186,'story_records':171,'challenge_lab_records':11,'scope_guard_records':4,'accounted_records':186,'unaccounted_records':0,'guided_journeys':7,'permanent_loci':54,'optional_first_exposure_recalls':18,'exact_name_review_targets':126,'mixed_discrimination_sets':28,'mixed_discrimination_questions':78}.items():
    if final.get(k)!=v: problems.append(f'Finalization {k}={final.get(k)} expected {v}')
if status.get('status')!='STUDENT_READY' or status.get('student_release') is not True or status.get('preview_release') is not False: problems.append('Unit 3 release status is not student-ready')
if release.get('student_release') is not True or release.get('preview_release') is not False: problems.append('F5 release manifest flags are wrong')

lines=['# Unit 3 F5 Release Audit','',
'## Canonical disposition','',
'- Canonical Unit 3 records: **186 / 186 accounted**',
'- Permanent-story records: **171 / 171**',
'- Challenge Lab records: **11 / 11**',
'- Non-runtime AP scope guards: **4 / 4**',
'- Unaccounted canonical records: **0**','',
'## Student learning system','',
'- Guided journeys: **7 / 7**',
'- Permanent loci: **54 / 54**',
'- Optional first-exposure Quick Recalls: **18**',
'- Exact-name delayed-review targets: **126 / 126**',
'- Mandatory spelling targets: **0**',
'- Mixed-confusable sets: **28 / 28**',
'- Mixed-discrimination questions: **78**',
'- Application/transfer challenges: **11 / 11**','',
'## Scope guards','',
'- **Gibbs free-energy equation** remains teacher enrichment and is not required AP Exam memorization.',
'- **Specific photosynthetic electron-carrier names** remain supporting context, not required name memorization.',
'- **Detailed Calvin-cycle steps/intermediates/enzyme names** remain outside required memorization.',
'- **Detailed glycolysis/Krebs steps, structures, enzyme names, and exact intermediate sequences** remain outside required memorization.','',
'## Review release policy','',
'First exposure remains story-first with sparse optional recall. Exact-name targets enter delayed retrieval only after encounter. Mixed-confusable practice unlocks only after all members of the set have been encountered and waits at least 48 hours. The visible Review surface remains capped at five due items. Unit 3 has no mandatory spelling gate.','',
'## Result','', '**PASS — Unit 3 is eligible for student release.**' if not problems else '**FAIL — blocking findings remain.**']
if problems: lines+=['','### Blocking findings','']+[f'- {p}' for p in problems]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')

mat=['# Unit 3 F5 Review and Challenge Matrix','',
'## Challenge Lab','',
'| Challenge | Locked record | Domain | Student task |','|---|---|---|---|']
for x in lab['items']: mat.append(f"| {x['challenge_id']} | {x['knowledge_id']} · {x['title']} | {x['domain']} | {x['prompt']} |")
mat+=['','## Mixed discrimination','', '| Set | Confusable targets | Questions | First eligible |','|---|---|---:|---|']
for s in mixed['sets']: mat.append(f"| {s['set_id']} · {s['title']} | {', '.join(s['terms'])} | {len(s['questions'])} | after all targets encountered + {s['initial_delay_hours']} h |")
mat+=['','## Exact-name review','',f"**{review['target_count']} targets** are scheduled from answer-redacted scientific descriptions after story encounter. The student sees no more than **{review['visible_review_limit']} due items** at a time.",'','## Canonical non-runtime scope guards','']
for g in guards['guards']: mat.append(f"- **{g['canonical_label']}** — {g['canonical_statement']}")
MATRIX.write_text('\n'.join(mat)+'\n',encoding='utf-8')

if problems:
    print('\n'.join(problems)); sys.exit(1)
print('UNIT3 F5 QA PASS')
print(json.dumps({'canonical_records':186,'story_records':171,'challenge_lab_records':11,'scope_guards':4,'journeys':7,'scenes':54,'optional_recalls':18,'exact_name_targets':126,'confusable_sets':28,'mixed_questions':78,'student_release':True},indent=2))
