from __future__ import annotations
import json, hashlib, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U6=ROOT/'content'/'ap-biology'/'unit-6'
AP=ROOT/'content'/'ap-biology'
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from scripts.site_release_guard import site_runtime_hash_allowed
def read(rel): return json.loads((U6/rel).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
problems=[]
canon={r['knowledge_id']:r for r in read('source/canonical-unit6-f1.json')['canonical_catalog']}
cls=read('architecture/learning-classification-f2.json'); cls_by={r['knowledge_id']:r for r in cls['records']}
arch=read('architecture/palace-architecture-f2.json')
mem=read('memory-objects-f5.json'); lab=read('application-lab.json'); review=read('review-manifest-f5.json'); mixed=read('mixed-discrimination-f5.json'); guards=read('scope-guards-f5.json'); final=read('finalization-f5.json'); status=read('status-f5.json'); reg=read('journeys-f5.json'); lock=read('content-lock-f5.json'); release=read('f5-release-manifest.json')

story=[]; exact={}; beat_terms={}
for i in range(1,7):
    j=read(f'journeys/U6-J{i}.json')
    for s in j['scenes']:
        story.extend(s['object_ids'])
        for b in s['story_beats']:
            beat_terms[b['object_id']]=b['term']
            if b.get('exact_name'): exact[b['object_id']]=b['term']
if len(story)!=161 or len(set(story))!=161: problems.append(f'story accounting {len(story)}/{len(set(story))} != 161/161')
if len(exact)!=134: problems.append(f'exact-name story count {len(exact)} != 134')

if mem.get('count')!=161 or len(mem.get('memory_objects',[]))!=161: problems.append('runtime Memory Object count != 161')
if mem.get('exact_name_required_count')!=134: problems.append('Memory Object exact-name count != 134')
if {x['memory_object_id'] for x in mem['memory_objects']}!=set(story): problems.append('Memory Objects do not exactly match story records')
for x in mem['memory_objects']:
    kid=x['source_knowledge_id']; c=canon[kid]
    if x['canonical_definition']!=c['canonical_verified_statement']: problems.append(f'canonical mismatch {kid}')
    expected='YES' if cls_by[kid].get('exact_name_recall') else 'NO'
    if x['exact_name_required']!=expected: problems.append(f'exact-name policy mismatch {kid}')
    if x.get('scientific_lock_status')!='LOCKED_F1' or x.get('narrative_lock_status')!='LOCKED_F4F' or not x.get('student_runtime'): problems.append(f'runtime lock problem {kid}')

challenge_expected={r['knowledge_id'] for r in cls['records'] if r['destination']=='CHALLENGE_LAB'}
challenge_ids={x['knowledge_id'] for x in lab['items']}
if lab.get('challenge_count')!=16 or lab.get('practice_only_runtime_count')!=16 or challenge_ids!=challenge_expected: problems.append('Challenge Lab does not cover exactly 16 practice records')
for x in lab['items']:
    kid=x['knowledge_id']
    if x['canonical_statement']!=canon[kid]['canonical_verified_statement']: problems.append(f'challenge canonical mismatch {kid}')
    if len(x.get('prompt',''))<150 or len(x.get('answer_guide',''))<150 or len(x.get('story_hint',''))<70: problems.append(f'challenge too thin {kid}')
    if not x.get('practice_only_runtime'): problems.append(f'challenge runtime flag missing {kid}')

scope_expected={r['knowledge_id'] for r in cls['records'] if r['scope_class']=='SCOPE_GUARD'}
if guards.get('guard_count')!=25 or {x['knowledge_id'] for x in guards['guards']}!=scope_expected: problems.append('scope guards mismatch')
for x in guards['guards']:
    if x['canonical_statement']!=canon[x['knowledge_id']]['canonical_verified_statement']: problems.append(f"scope guard wording drift {x['knowledge_id']}")
    if x['student_runtime'] or x['permanent_palace'] or x['challenge_lab']: problems.append(f"scope guard leaked into runtime {x['knowledge_id']}")

if review.get('target_count')!=134 or len(review.get('targets',[]))!=134 or review.get('non_exact_palace_records')!=27 or review.get('mandatory_spelling_targets')!=0 or review.get('visible_review_limit')!=5: problems.append('review manifest accounting mismatch')
if {x['knowledge_id'] for x in review['targets']}!=set(exact): problems.append('review targets do not equal F2 exact-name subset')
for x in review['targets']:
    if x['target_answer']!=exact[x['knowledge_id']]: problems.append(f"review answer mismatch {x['knowledge_id']}")
    if x['target_answer'].casefold() in x['prompt'].casefold(): problems.append(f"review prompt leaks answer {x['knowledge_id']}")
    if x['canonical_science']!=canon[x['knowledge_id']]['canonical_verified_statement']: problems.append(f"review science mismatch {x['knowledge_id']}")

if mixed.get('set_count')!=37 or mixed.get('question_count')!=94: problems.append(f"mixed accounting {mixed.get('set_count')}/{mixed.get('question_count')} != 37/94")
if {s['set_id'] for s in mixed['sets']}!={s['set_id'] for s in arch['confusable_sets']}: problems.append('confusable sets mismatch F2 architecture')
for s in mixed['sets']:
    if len(s['questions'])!=len(s['terms']) or s['initial_delay_hours']<48: problems.append(f"mixed set structure problem {s['set_id']}")
    for q in s['questions']:
        if q['answer'] not in q['choices'] or q['answer'].casefold() in q['prompt'].casefold(): problems.append(f"mixed prompt/answer problem {q['question_id']}")
        if q['explanation']!=canon[q['knowledge_id']]['canonical_verified_statement']: problems.append(f"mixed science mismatch {q['question_id']}")

parts=[set(story),challenge_ids,scope_expected]
if any(parts[i]&parts[j] for i in range(3) for j in range(i+1,3)): problems.append('destination overlap')
if set().union(*parts)!=set(canon): problems.append('canonical zero-loss union failed')
expected_final={'canonical_records':202,'runtime_memory_objects':161,'story_records':161,'challenge_lab_records':16,'scope_guard_records':25,'accounted_records':202,'unaccounted_records':0,'guided_journeys':6,'permanent_loci':53,'optional_first_exposure_recalls':18,'exact_name_review_targets':134,'non_exact_palace_records':27,'mandatory_spelling_targets':0,'mixed_discrimination_sets':37,'mixed_discrimination_questions':94}
for k,v in expected_final.items():
    if final.get(k)!=v: problems.append(f'finalization {k}={final.get(k)} expected {v}')
if status.get('status')!='STUDENT_READY' or status.get('student_release') is not True or status.get('preview_release') is not False: problems.append('student release state wrong')
if status.get('canonical_records_accounted')!=202 or status.get('runtime_memory_objects')!=161 or status.get('application_challenges')!=16: problems.append('status accounting wrong')
if reg.get('journey_count')!=6 or reg.get('scene_count')!=53 or reg.get('checkpoint_count')!=18 or reg.get('student_release') is not True or reg.get('preview_release') is not False: problems.append('F5 journey registry wrong')
if release.get('student_release') is not True or release.get('preview_release') is not False: problems.append('F5 release flags wrong')

# F4F narrative bytes and prior content locks remain frozen.
f4=read('content-lock-f4f.json')
for rel,meta in f4['files'].items():
    if rel.startswith('journeys/U6-J'):
        p=U6/rel
        if p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'narrative changed after F4F {rel}')
for rel,digest in lock['files'].items():
    p=U6/rel
    if not p.exists() or sha(p)!=digest: problems.append(f'F5 lock mismatch {rel}')
for rel,digest in lock.get('protected_narratives',{}).items():
    if sha(U6/rel)!=digest: problems.append(f'protected narrative mismatch {rel}')
for rel,digest in lock.get('protected_upstream_locks',{}).items():
    if sha(U6/rel)!=digest: problems.append(f'protected upstream lock mismatch {rel}')
later=U6/'content-lock-f6.json'
later_runtime=read('content-lock-f6.json').get('runtime_file_sha256',{}) if later.exists() else {}

# Historical Unit 6 F5 runs inside later mainline releases. Shared runtime files may
# legitimately differ after Unit 6 if a later unit/stage explicitly locks those bytes.
# Collect all later-unit runtime locks instead of hard-coding one Unit 7 stage, so this
# historical gate remains valid after Unit 7 F6 and future locked unit integrations.
later_unit_runtime={}
for unit_dir in sorted(AP.glob('unit-*')):
    try:
        unit_number=int(unit_dir.name.split('-',1)[1])
    except (IndexError,ValueError):
        continue
    if unit_number<=6:
        continue
    for lock_path in sorted(unit_dir.glob('content-lock-f*.json')):
        try:
            runtime=json.loads(lock_path.read_text(encoding='utf-8')).get('runtime_file_sha256',{})
        except (OSError,json.JSONDecodeError):
            continue
        for rel,digest in runtime.items():
            later_unit_runtime.setdefault(rel,set()).add(digest)

for rel,digest in lock.get('runtime_file_sha256',{}).items():
    p=ROOT/rel; current=sha(p) if p.exists() else None
    later_locked=current in later_unit_runtime.get(rel,set())
    if current!=digest and later_runtime.get(rel)!=current and not later_locked and not site_runtime_hash_allowed(ROOT,rel,current):
        problems.append(f'F5 runtime file mismatch without later locked runtime state {rel}')

# High-risk scientific boundaries must survive as non-runtime guards.
joined=' '.join(x['canonical_statement'] for x in guards['guards']).casefold()
for phrase in ['phosphodiester bonds','not universal','host genomic dna','regulatory protein','in-frame indels do not shift the frame','selection changes frequencies','do not require unnecessary procedural details']:
    if phrase.casefold() not in joined: problems.append(f'missing Unit 6 scope/science protection: {phrase}')

# Course and mainline release.
course=json.loads((AP/'course.json').read_text(encoding='utf-8')); cu6=next(u for u in course['units'] if u['unit_id']=='unit-6')
if cu6.get('status')!='STUDENT_READY' or cu6.get('student_release') is not True or cu6.get('runtime_memory_objects')!=161: problems.append('course registry Unit 6 not student-ready')
main=json.loads((AP/'mainline-release-u1-u6.json').read_text(encoding='utf-8'))
if main.get('units')!=['unit-1','unit-2','unit-3','unit-4','unit-5','unit-6'] or main.get('totals',{}).get('canonical_records_units_1_6')!=1091 or main.get('totals',{}).get('guided_journeys')!=44 or main.get('totals',{}).get('permanent_scenes')!=335 or main.get('totals',{}).get('challenge_lab_items')!=83: problems.append('Units 1-6 mainline totals wrong')

if problems:
    print('UNIT6 F5 QA FAIL'); print('\n'.join(f'- {x}' for x in problems)); sys.exit(1)
print('UNIT6 F5 QA PASS')
print(json.dumps({'canonical_records':202,'runtime_memory_objects':161,'challenge_records':16,'scope_guards':25,'journeys':6,'loci':53,'optional_recalls':18,'exact_name_review_targets':134,'non_exact_palace_records':27,'mixed_sets':37,'mixed_questions':94,'unaccounted':0,'student_release':True},indent=2))
