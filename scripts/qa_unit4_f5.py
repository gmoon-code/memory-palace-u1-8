from __future__ import annotations
import json, hashlib, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; U4=ROOT/'content/ap-biology/unit-4'
def read(rel): return json.loads((U4/rel).read_text(encoding='utf-8'))
problems=[]
source=read('source/canonical-unit4-f1.json'); canon={r['knowledge_id']:r for r in source['canonical_catalog']}
cls=read('architecture/learning-classification-f2.json'); arch=read('architecture/palace-architecture-f2.json')
mem=read('memory-objects-f5.json'); lab=read('application-lab.json'); review=read('review-manifest-f5.json'); mixed=read('mixed-discrimination-f5.json'); guards=read('scope-guards-f5.json'); final=read('finalization-f5.json'); status=read('status-f5.json'); reg=read('journeys-f5.json'); lock=read('content-lock-f5.json')

story=[]; exact={}; narrative_hashes={}
for i in range(1,8):
    p=U4/'journeys'/f'U4-J{i}.json'; narrative_hashes[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    j=json.loads(p.read_text(encoding='utf-8'))
    for s in j['scenes']:
        story.extend(s['object_ids'])
        for b in s['story_beats']:
            if b.get('exact_name'): exact[b['object_id']]=b['term']
if len(story)!=162 or len(set(story))!=162: problems.append(f'story accounting {len(story)}/{len(set(story))} != 162')
if mem.get('count')!=162 or len(mem.get('memory_objects',[]))!=162: problems.append('runtime Memory Object count != 162')
if {x['memory_object_id'] for x in mem['memory_objects']}!=set(story): problems.append('Memory Objects do not exactly match story records')
for x in mem['memory_objects']:
    if x['canonical_definition']!=canon[x['source_knowledge_id']]['canonical_verified_statement']: problems.append(f"canonical mismatch {x['memory_object_id']}")
    if x.get('scientific_lock_status')!='LOCKED_F1' or not x.get('student_runtime'): problems.append(f"runtime lock problem {x['memory_object_id']}")

challenge_expected={r['knowledge_id'] for r in cls['records'] if r['destination']=='CHALLENGE_LAB'}
challenge_ids={x['knowledge_id'] for x in lab['items']}
if lab.get('challenge_count')!=15 or lab.get('practice_only_runtime_count')!=15 or challenge_ids!=challenge_expected: problems.append('Challenge Lab does not cover exactly 15 practice records')
for x in lab['items']:
    if x['canonical_statement']!=canon[x['knowledge_id']]['canonical_verified_statement']: problems.append(f"challenge canonical mismatch {x['knowledge_id']}")
    if min(len(x['prompt']),len(x['answer_guide']))<100 or len(x['story_hint'])<60: problems.append(f"challenge too thin {x['knowledge_id']}")

scope_expected={r['knowledge_id'] for r in cls['records'] if r['scope_class']=='SCOPE_GUARD'}
if guards.get('guard_count')!=3 or {x['knowledge_id'] for x in guards['guards']}!=scope_expected: problems.append('scope guards mismatch')
if any(x['student_runtime'] or x['permanent_palace'] or x['challenge_lab'] for x in guards['guards']): problems.append('scope guard leaked into runtime')

if review.get('target_count')!=162 or len(review.get('targets',[]))!=162 or review.get('mandatory_spelling_targets')!=0 or review.get('visible_review_limit')!=5: problems.append('review manifest accounting mismatch')
if {x['knowledge_id'] for x in review['targets']}!=set(story): problems.append('review targets do not equal story objects')
for x in review['targets']:
    if x['target_answer']!=exact[x['knowledge_id']]: problems.append(f"review answer mismatch {x['knowledge_id']}")
    if x['target_answer'].casefold() in x['prompt'].casefold(): problems.append(f"review prompt leaks answer {x['knowledge_id']}")
    if x['canonical_science']!=canon[x['knowledge_id']]['canonical_verified_statement']: problems.append(f"review science mismatch {x['knowledge_id']}")

if mixed.get('set_count')!=33 or mixed.get('question_count')!=99: problems.append(f"mixed accounting {mixed.get('set_count')}/{mixed.get('question_count')} != 33/99")
if {s['set_id'] for s in mixed['sets']}!={s['set_id'] for s in arch['confusable_sets']}: problems.append('confusable sets mismatch F2 architecture')
for s in mixed['sets']:
    if len(s['questions'])!=len(s['terms']) or s['initial_delay_hours']<48: problems.append(f"mixed set structure problem {s['set_id']}")
    for q in s['questions']:
        if q['answer'] not in q['choices'] or q['answer'].casefold() in q['prompt'].casefold(): problems.append(f"mixed prompt/answer problem {q['question_id']}")
        if q['explanation']!=canon[q['knowledge_id']]['canonical_verified_statement']: problems.append(f"mixed science mismatch {q['question_id']}")

parts=[set(story),challenge_ids,scope_expected]
if any(parts[i]&parts[j] for i in range(3) for j in range(i+1,3)): problems.append('destination overlap')
if set().union(*parts)!=set(canon): problems.append('canonical zero-loss union failed')
if final.get('accounted_records')!=180 or final.get('unaccounted_records')!=0 or final.get('runtime_memory_objects')!=162: problems.append('finalization counts wrong')
if final.get('mixed_discrimination_questions')!=99 or final.get('exact_name_review_targets')!=162: problems.append('finalization review counts wrong')
if status.get('status')!='STUDENT_READY' or status.get('student_release') is not True or status.get('preview_release') is not False: problems.append('student release state wrong')
if status.get('canonical_records_accounted')!=180 or status.get('runtime_memory_objects')!=162 or status.get('application_challenges')!=15: problems.append('status accounting wrong')
if reg.get('journey_count')!=7 or reg.get('scene_count')!=51 or reg.get('checkpoint_count')!=18 or reg.get('student_release') is not True: problems.append('F5 journey registry wrong')

# F4G narrative bytes must remain frozen.
f4=read('content-lock-f4g.json')
for rel,meta in f4['files'].items():
    if rel.startswith('journeys/U4-J'):
        p=U4/rel
        if p.stat().st_size!=meta['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=meta['sha256']: problems.append(f'narrative changed after F4G: {rel}')
for rel,digest in lock['files'].items():
    p=U4/rel
    if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest: problems.append(f'F5 lock mismatch {rel}')

if problems:
    print('UNIT4 F5 QA FAIL'); print('\n'.join(f'- {x}' for x in problems)); sys.exit(1)
print('UNIT4 F5 QA PASS')
print(json.dumps({'canonical_records':180,'runtime_memory_objects':162,'challenge_records':15,'scope_guards':3,'journeys':7,'loci':51,'exact_name_review_targets':162,'mixed_sets':33,'mixed_questions':99,'unaccounted':0,'student_release':True},indent=2))
