from __future__ import annotations
import json,hashlib,sys,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; U5=ROOT/'content/ap-biology/unit-5'
def read(rel): return json.loads((U5/rel).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
problems=[]
source=read('source/canonical-unit5-f1.json'); canon={r['knowledge_id']:r for r in source['canonical_catalog']}
cls=read('architecture/learning-classification-f2.json'); arch=read('architecture/palace-architecture-f2.json')
mem=read('memory-objects-f5.json'); lab=read('application-lab.json'); review=read('review-manifest-f5.json'); mixed=read('mixed-discrimination-f5.json'); guards=read('scope-guards-f5.json'); final=read('finalization-f5.json'); status=read('status-f5.json'); reg=read('journeys-f5.json'); lock=read('content-lock-f5.json')

story=[]; exact={}; nonexact=[]
for i in range(1,9):
    j=read(f'journeys/U5-J{i}.json')
    for s in j['scenes']:
        story.extend(s['object_ids'])
        for b in s['story_beats']:
            if b.get('exact_name'): exact[b['object_id']]=b['term']
            else: nonexact.append(b['object_id'])
if len(story)!=131 or len(set(story))!=131: problems.append(f'story accounting {len(story)}/{len(set(story))} != 131')
if set(story)!={r['knowledge_id'] for r in cls['records'] if r['destination'] in {'PALACE_PRIMARY_LOCUS','PALACE_EMBEDDED'}}: problems.append('story records no longer equal F2 palace-managed records')
if len(exact)!=130 or nonexact!=['U5-K-115']: problems.append(f'exact-name partition wrong {len(exact)} exact / {nonexact} nonexact')

if mem.get('count')!=131 or len(mem.get('memory_objects',[]))!=131: problems.append('runtime Memory Object count != 131')
if mem.get('exact_name_required_count')!=130: problems.append('Memory Object exact-name count != 130')
if {x['memory_object_id'] for x in mem['memory_objects']}!=set(story): problems.append('Memory Objects do not exactly match story records')
for x in mem['memory_objects']:
    kid=x['source_knowledge_id']
    if x['canonical_definition']!=canon[kid]['canonical_verified_statement']: problems.append(f'canonical mismatch {kid}')
    expected='YES' if cls['records'][int(kid.split('-')[-1])-1].get('exact_name_recall') else 'NO'
    if x['exact_name_required']!=expected: problems.append(f'exact-name policy mismatch {kid}')
    if x.get('scientific_lock_status')!='LOCKED_F1' or x.get('narrative_lock_status')!='LOCKED_F4H' or not x.get('student_runtime'): problems.append(f'runtime lock problem {kid}')

challenge_expected={r['knowledge_id'] for r in cls['records'] if r['destination']=='CHALLENGE_LAB'}
challenge_ids={x['knowledge_id'] for x in lab['items']}
if lab.get('challenge_count')!=16 or lab.get('practice_only_runtime_count')!=16 or challenge_ids!=challenge_expected: problems.append('Challenge Lab does not cover exactly 16 practice records')
for x in lab['items']:
    if x['canonical_statement']!=canon[x['knowledge_id']]['canonical_verified_statement']: problems.append(f"challenge canonical mismatch {x['knowledge_id']}")
    if len(x['prompt'])<150 or len(x['answer_guide'])<150 or len(x['story_hint'])<70: problems.append(f"challenge too thin {x['knowledge_id']}")

scope_expected={r['knowledge_id'] for r in cls['records'] if r['scope_class']=='SCOPE_GUARD'}
if guards.get('guard_count')!=5 or {x['knowledge_id'] for x in guards['guards']}!=scope_expected: problems.append('scope guards mismatch')
if any(x['student_runtime'] or x['permanent_palace'] or x['challenge_lab'] for x in guards['guards']): problems.append('scope guard leaked into runtime')

if review.get('target_count')!=130 or len(review.get('targets',[]))!=130 or review.get('non_exact_palace_records')!=1 or review.get('mandatory_spelling_targets')!=0 or review.get('visible_review_limit')!=5: problems.append('review manifest accounting mismatch')
if {x['knowledge_id'] for x in review['targets']}!=set(exact): problems.append('review targets do not equal the F2 exact-name subset')
for x in review['targets']:
    if x['target_answer']!=exact[x['knowledge_id']]: problems.append(f"review answer mismatch {x['knowledge_id']}")
    if x['target_answer'].casefold() in x['prompt'].casefold(): problems.append(f"review prompt leaks answer {x['knowledge_id']}")
    if x['canonical_science']!=canon[x['knowledge_id']]['canonical_verified_statement']: problems.append(f"review science mismatch {x['knowledge_id']}")

if mixed.get('set_count')!=32 or mixed.get('question_count')!=79: problems.append(f"mixed accounting {mixed.get('set_count')}/{mixed.get('question_count')} != 32/79")
if {s['set_id'] for s in mixed['sets']}!={s['set_id'] for s in arch['confusable_sets']}: problems.append('confusable sets mismatch F2 architecture')
for s in mixed['sets']:
    if len(s['questions'])!=len(s['terms']) or s['initial_delay_hours']<48: problems.append(f"mixed set structure problem {s['set_id']}")
    for q in s['questions']:
        if q['answer'] not in q['choices'] or q['answer'].casefold() in q['prompt'].casefold(): problems.append(f"mixed prompt/answer problem {q['question_id']}")
        if q['explanation']!=canon[q['knowledge_id']]['canonical_verified_statement']: problems.append(f"mixed science mismatch {q['question_id']}")

parts=[set(story),challenge_ids,scope_expected]
if any(parts[i]&parts[j] for i in range(3) for j in range(i+1,3)): problems.append('destination overlap')
if set().union(*parts)!=set(canon): problems.append('canonical zero-loss union failed')
if final.get('accounted_records')!=152 or final.get('unaccounted_records')!=0 or final.get('runtime_memory_objects')!=131: problems.append('finalization counts wrong')
if final.get('mixed_discrimination_questions')!=79 or final.get('exact_name_review_targets')!=130 or final.get('non_exact_palace_records')!=1: problems.append('finalization review counts wrong')
if status.get('status')!='STUDENT_READY' or status.get('student_release') is not True or status.get('preview_release') is not False: problems.append('student release state wrong')
if status.get('canonical_records_accounted')!=152 or status.get('runtime_memory_objects')!=131 or status.get('application_challenges')!=16: problems.append('status accounting wrong')
if reg.get('journey_count')!=8 or reg.get('scene_count')!=50 or reg.get('checkpoint_count')!=18 or reg.get('student_release') is not True or reg.get('preview_release') is not False: problems.append('F5 journey registry wrong')

# F4H narratives and all earlier locks remain frozen.
f4=read('content-lock-f4h.json')
for rel,meta in f4['files'].items():
    if rel.startswith('journeys/U5-J'):
        p=U5/rel
        if p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'narrative changed after F4H {rel}')
for rel,digest in lock['files'].items():
    p=U5/rel
    if not p.exists() or sha(p)!=digest: problems.append(f'F5 lock mismatch {rel}')
for rel,digest in lock.get('protected_narratives',{}).items():
    if sha(U5/rel)!=digest: problems.append(f'protected narrative mismatch {rel}')

# Important high-risk policies survive runtime materialization.
if any(x['knowledge_id']=='U5-K-149' and x['student_runtime'] for x in guards['guards']): problems.append('chromosome-complement scope guard leaked')
for phrase in ['does not prove or “accept” the null','not universal definitions','Do not infer gender']:
    if phrase.casefold() not in ' '.join(x['canonical_statement'] for x in guards['guards']).casefold(): problems.append(f'missing scope protection {phrase}')

if problems:
    print('UNIT5 F5 QA FAIL'); print('\n'.join(f'- {x}' for x in problems)); sys.exit(1)
print('UNIT5 F5 QA PASS')
print(json.dumps({'canonical_records':152,'runtime_memory_objects':131,'challenge_records':16,'scope_guards':5,'journeys':8,'loci':50,'optional_recalls':18,'exact_name_review_targets':130,'non_exact_palace_records':1,'mixed_sets':32,'mixed_questions':79,'unaccounted':0,'student_release':True},indent=2))
