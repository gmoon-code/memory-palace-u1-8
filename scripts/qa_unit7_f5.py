from __future__ import annotations
import json, hashlib, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
AP=ROOT/'content'/'ap-biology'
U7=AP/'unit-7'

def read(name): return json.loads((U7/name).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

canon={r['knowledge_id']:r for r in read('source/canonical-unit7-f1.json')['canonical_catalog']}
cls=read('architecture/learning-classification-f2.json')
arch=read('architecture/palace-architecture-f2.json')
mem=read('memory-objects-f5.json'); lab=read('application-lab.json'); review=read('review-manifest-f5.json')
mixed=read('mixed-discrimination-f5.json'); guards=read('scope-guards-f5.json'); final=read('finalization-f5.json')
reg=read('journeys-f5.json'); status=read('status.json'); lock=read('content-lock-f5.json'); release=read('f5-release-manifest.json')
problems=[]

story={x['knowledge_id'] for x in cls['records'] if x['destination'] in {'PALACE_PRIMARY_LOCUS','PALACE_EMBEDDED'}}
challenge={x['knowledge_id'] for x in cls['records'] if x['destination']=='CHALLENGE_LAB'}
scope={x['knowledge_id'] for x in cls['records'] if x['scope_class']=='SCOPE_GUARD'}
if (len(canon),len(story),len(challenge),len(scope))!=(215,174,16,25): problems.append('canonical destination accounting mismatch')
parts=[story,challenge,scope]
if any(parts[i]&parts[j] for i in range(3) for j in range(i+1,3)): problems.append('destination overlap')
if set().union(*parts)!=set(canon): problems.append('zero-loss union failed')

if mem.get('count')!=174 or len(mem.get('memory_objects',[]))!=174 or mem.get('exact_name_required_count')!=94: problems.append('Memory Object accounting mismatch')
mo={x['memory_object_id']:x for x in mem['memory_objects']}
if set(mo)!=story: problems.append('Memory Object IDs do not equal palace-managed records')
for kid,x in mo.items():
    c=canon[kid]
    if x['canonical_definition']!=c['canonical_verified_statement']: problems.append(f'canonical definition mismatch {kid}')
    if x['scientific_lock_status']!='LOCKED_F1' or x['narrative_lock_status']!='LOCKED_F4F': problems.append(f'lock status mismatch {kid}')
    if x['student_runtime'] is not True: problems.append(f'Memory Object not in runtime {kid}')

if review.get('target_count')!=94 or review.get('non_exact_palace_records')!=80 or review.get('mandatory_spelling_targets')!=0 or review.get('visible_review_limit')!=5: problems.append('Review manifest accounting mismatch')
if {x['knowledge_id'] for x in review['targets']}!={kid for kid in story if next(r for r in cls['records'] if r['knowledge_id']==kid).get('exact_name_recall')}: problems.append('Review target IDs mismatch exact-name classification')
for x in review['targets']:
    if x['target_answer'].casefold() in x['prompt'].casefold(): problems.append(f'review prompt leaks answer {x["knowledge_id"]}')
    if x['canonical_science']!=canon[x['knowledge_id']]['canonical_verified_statement']: problems.append(f'review science mismatch {x["knowledge_id"]}')

if mixed.get('set_count')!=33 or mixed.get('question_count')!=102: problems.append('mixed discrimination accounting mismatch')
if {s['set_id'] for s in mixed['sets']}!={s['set_id'] for s in arch['confusable_sets']}: problems.append('mixed set IDs mismatch F2')
for s in mixed['sets']:
    if len(s['questions'])!=len(s['terms']) or s['initial_delay_hours']<48: problems.append(f'mixed set structure mismatch {s["set_id"]}')
    for q in s['questions']:
        if q['answer'] not in q['choices'] or q['answer'].casefold() in q['prompt'].casefold(): problems.append(f'mixed prompt/answer problem {q["question_id"]}')
        if q['explanation']!=canon[q['knowledge_id']]['canonical_verified_statement']: problems.append(f'mixed science mismatch {q["question_id"]}')

if lab.get('challenge_count')!=16 or lab.get('practice_only_runtime_count')!=16 or len(lab.get('items',[]))!=16: problems.append('Challenge Lab accounting mismatch')
if set(lab.get('practice_only_runtime_object_ids',[]))!=challenge: problems.append('Challenge Lab IDs mismatch F2')
for x in lab['items']:
    if x['knowledge_id'] not in challenge: problems.append(f'non-practice record in Challenge Lab {x["knowledge_id"]}')
    if x['canonical_statement']!=canon[x['knowledge_id']]['canonical_verified_statement']: problems.append(f'challenge science mismatch {x["knowledge_id"]}')
    if min(len(x['prompt']),len(x['answer_guide']))<150 or len(x['story_hint'])<70: problems.append(f'challenge too thin {x["challenge_id"]}')
    if not x['practice_only_runtime']: problems.append(f'challenge not marked practice-only {x["challenge_id"]}')

if guards.get('guard_count')!=25 or len(guards.get('guards',[]))!=25 or {x['knowledge_id'] for x in guards['guards']}!=scope: problems.append('Scope guard accounting mismatch')
for x in guards['guards']:
    if x['student_runtime'] or x['permanent_palace'] or x['challenge_lab']: problems.append(f'scope guard became runtime target {x["knowledge_id"]}')
    if x['canonical_statement']!=canon[x['knowledge_id']]['canonical_verified_statement']: problems.append(f'scope guard science mismatch {x["knowledge_id"]}')

expected={'canonical_records':215,'runtime_memory_objects':174,'story_records':174,'challenge_lab_records':16,'scope_guard_records':25,'accounted_records':215,'unaccounted_records':0,'guided_journeys':6,'permanent_loci':55,'optional_first_exposure_recalls':18,'exact_name_review_targets':94,'non_exact_palace_records':80,'mandatory_spelling_targets':0,'mixed_discrimination_sets':33,'mixed_discrimination_questions':102}
for k,v in expected.items():
    if final.get(k)!=v: problems.append(f'finalization {k}={final.get(k)} expected {v}')
if final.get('release_status')!='STUDENT_READY_F5': problems.append('finalization release status wrong')

if reg.get('journey_count')!=6 or reg.get('scene_count')!=55 or reg.get('checkpoint_count')!=18 or reg.get('student_release') is not True or reg.get('preview_release') is not False: problems.append('F5 journey registry wrong')
if [x['palace_id'] for x in reg['guided_journeys']]!=[f'U7-J{i}' for i in range(1,7)]: problems.append('F5 journey order wrong')
if any(x.get('student_release')!='STUDENT_READY_F5' or x.get('preview_release') is not False for x in reg['guided_journeys']): problems.append('journey release flags wrong')

if status.get('status')!='STUDENT_READY' or status.get('student_release') is not True or status.get('preview_release') is not False: problems.append('Unit 7 student release state wrong')
if status.get('pipeline_stage') not in {'UNIT7_FINALIZED_F5','UNIT7_CLASSROOM_BROWSER_VALIDATED_F6'} or status.get('canonical_records_accounted')!=215 or status.get('runtime_memory_objects')!=174 or status.get('application_challenges')!=16: problems.append('Unit 7 status accounting wrong')
if release.get('student_release') is not True or release.get('preview_release') is not False or release.get('unaccounted_canonical_records')!=0: problems.append('F5 release manifest flags/accounting wrong')

# Frozen F4F narratives and locks.
f4=read('content-lock-f4f.json')
for i in range(1,7):
    rel=f'journeys/U7-J{i}.json'; p=U7/rel
    # J6 hash is directly in F4F files, J1-J5 are transitive through prior narrative protection.
    expected_hash=None
    if rel in f4.get('files',{}): expected_hash=f4['files'][rel]['sha256']
    fullrel=f'content/ap-biology/unit-7/{rel}'
    if fullrel in f4.get('prior_narrative_protection',{}): expected_hash=f4['prior_narrative_protection'][fullrel]['sha256']
    if expected_hash and sha(p)!=expected_hash: problems.append(f'narrative changed after F4F {rel}')
for rel,digest in lock.get('protected_narratives',{}).items():
    if sha(U7/rel)!=digest: problems.append(f'protected narrative mismatch {rel}')
for rel,digest in lock.get('protected_upstream_locks',{}).items():
    if sha(U7/rel)!=digest: problems.append(f'protected upstream lock mismatch {rel}')
for rel,digest in lock.get('files',{}).items():
    if sha(U7/rel)!=digest: problems.append(f'F5 lock mismatch {rel}')

# High-risk science boundaries remain explicit scope guards.
joined=' '.join(x['canonical_statement'] for x in guards['guards']).casefold()
phrases=['natural selection as knowing what organisms need','fitness is reproductive success','individual organism evolves genetically','natural selection itself with random evolutionary change','nonrandom mating can alter genotype frequencies without changing allele frequencies','p as dominant and q as recessive','carbon-14 as a universal fossil-dating method','vestigial structures as necessarily useless','primitive, less evolved, or the direct ancestor','divergent evolution automatically produces a new species','miller-urey experiment produced life','endosymbiotic theory as a model for the initial origin of life']
for phrase in phrases:
    if phrase not in joined: problems.append(f'missing Unit 7 scope/science protection: {phrase}')

# Course and mainline.
course=json.loads((AP/'course.json').read_text(encoding='utf-8')); cu7=next(u for u in course['units'] if u['unit_id']=='unit-7')
if cu7.get('status')!='STUDENT_READY' or cu7.get('student_release') is not True or cu7.get('runtime_memory_objects')!=174 or cu7.get('application_challenges')!=16: problems.append('course registry Unit 7 not student-ready')
main=json.loads((AP/'mainline-release-u1-u7.json').read_text(encoding='utf-8'))
if main.get('units')!=['unit-1','unit-2','unit-3','unit-4','unit-5','unit-6','unit-7']: problems.append('mainline Unit list wrong')
if main.get('runtime_version') not in {'v2-apbio-0.27.0-u7-f5','v2-apbio-0.28.0-u7-f6'}: problems.append('mainline runtime version wrong')
if main.get('totals')!={'canonical_records_units_1_7':1306,'guided_journeys':50,'permanent_scenes':390,'challenge_lab_items':99}: problems.append(f'mainline totals wrong {main.get("totals")}')

if problems:
    print('UNIT7 F5 QA FAIL')
    print('\n'.join(f'- {x}' for x in problems))
    sys.exit(1)
print('UNIT7 F5 QA PASS')
print(json.dumps({'canonical_records':215,'runtime_memory_objects':174,'challenge_records':16,'scope_guards':25,'journeys':6,'loci':55,'optional_recalls':18,'exact_name_review_targets':94,'non_exact_palace_records':80,'mixed_sets':33,'mixed_questions':102,'unaccounted':0,'student_release':True},indent=2))
