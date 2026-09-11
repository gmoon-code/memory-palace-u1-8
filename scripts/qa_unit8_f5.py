from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from fastapi.testclient import TestClient
from backend.main import app

AP=ROOT/'content'/'ap-biology'
U8=AP/'unit-8'
client=TestClient(app)


def read(rel): return json.loads((U8/rel).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

canon={r['Knowledge ID']:r for r in read('canonical-catalog.json')}
cls=read('architecture/learning-classification-f2.json')
arch=read('architecture/palace-architecture-f2.json')
mem=read('memory-objects-f5.json')
lab=read('application-lab.json')
review=read('review-manifest-f5.json')
mixed=read('mixed-discrimination-f5.json')
guards=read('scope-guards-f5.json')
final=read('finalization-f5.json')
reg=read('journeys-f5.json')
status=read('status.json')
lock=read('content-lock-f5.json')
release=read('f5-release-manifest.json')
problems=[]

story={x['knowledge_id'] for x in cls['records'] if x['destination'] in {'PALACE_PRIMARY_LOCUS','PALACE_EMBEDDED'}}
challenge={x['knowledge_id'] for x in cls['records'] if x['destination']=='CHALLENGE_LAB'}
scope={x['knowledge_id'] for x in cls['records'] if x['destination']=='SUPPORTING_NON_RUNTIME_SCOPE_GUARD'}
if (len(canon),len(story),len(challenge),len(scope))!=(255,211,13,31): problems.append('canonical destination accounting mismatch')
parts=[story,challenge,scope]
if any(parts[i]&parts[j] for i in range(3) for j in range(i+1,3)): problems.append('destination overlap')
if set().union(*parts)!=set(canon): problems.append('zero-loss union failed')

if mem.get('count')!=211 or len(mem.get('memory_objects',[]))!=211 or mem.get('exact_name_required_count')!=135: problems.append('Memory Object accounting mismatch')
mo={x['memory_object_id']:x for x in mem['memory_objects']}
if set(mo)!=story: problems.append('Memory Object IDs do not equal palace-managed records')
for kid,x in mo.items():
    c=canon[kid]
    if x['canonical_term']!=c['Canonical Label']: problems.append(f'canonical term mismatch {kid}')
    if x['canonical_definition']!=c['Canonical Verified Statement']: problems.append(f'canonical definition mismatch {kid}')
    if x['scientific_lock_status']!='LOCKED_F1' or x['narrative_lock_status']!='LOCKED_F4A_F4H': problems.append(f'lock status mismatch {kid}')
    if x['student_runtime'] is not True: problems.append(f'Memory Object not in runtime {kid}')

if review.get('target_count')!=135 or review.get('non_exact_palace_records')!=76 or review.get('mandatory_spelling_targets')!=0 or review.get('visible_review_limit')!=5: problems.append('Review manifest accounting mismatch')
expected_exact={kid for kid in story if next(r for r in cls['records'] if r['knowledge_id']==kid).get('exact_name_recall')}
if {x['knowledge_id'] for x in review['targets']}!=expected_exact: problems.append('Review target IDs mismatch exact-name classification')
for x in review['targets']:
    if x['target_answer'].casefold() in x['prompt'].casefold(): problems.append(f'review prompt leaks answer {x["knowledge_id"]}')
    if x['canonical_science']!=canon[x['knowledge_id']]['Canonical Verified Statement']: problems.append(f'review science mismatch {x["knowledge_id"]}')
    if x['initial_review_window_hours']!=[18,72]: problems.append(f'review timing drift {x["knowledge_id"]}')

if mixed.get('set_count')!=40 or mixed.get('question_count')!=104: problems.append('mixed discrimination accounting mismatch')
if {s['set_id'] for s in mixed['sets']}!={s['set_id'] for s in arch['mixed_discrimination_sets']}: problems.append('mixed set IDs mismatch F2')
for s in mixed['sets']:
    if len(s['questions'])!=len(s['terms']) or s['initial_delay_hours']<48: problems.append(f'mixed set structure mismatch {s["set_id"]}')
    for q in s['questions']:
        if q['answer'] not in q['choices'] or q['answer'].casefold() in q['prompt'].casefold(): problems.append(f'mixed prompt/answer problem {q["question_id"]}')
        if q['explanation']!=canon[q['knowledge_id']]['Canonical Verified Statement']: problems.append(f'mixed science mismatch {q["question_id"]}')

if lab.get('challenge_count')!=13 or lab.get('practice_only_runtime_count')!=13 or len(lab.get('items',[]))!=13: problems.append('Challenge Lab accounting mismatch')
if set(lab.get('practice_only_runtime_object_ids',[]))!=challenge: problems.append('Challenge Lab IDs mismatch F2')
if {x['knowledge_id'] for x in lab['items']}!=challenge: problems.append('Challenge Lab item IDs mismatch F2')
for x in lab['items']:
    if x['canonical_statement']!=canon[x['knowledge_id']]['Canonical Verified Statement']: problems.append(f'challenge science mismatch {x["knowledge_id"]}')
    if min(len(x['prompt']),len(x['answer_guide']))<150 or len(x['story_hint'])<70: problems.append(f'challenge too thin {x["challenge_id"]}')
    if not x['practice_only_runtime']: problems.append(f'challenge not marked practice-only {x["challenge_id"]}')
    if not x['prerequisite_loci'] or len(x['prerequisite_loci'])!=len(x['prerequisite_scene_titles']): problems.append(f'challenge prerequisites invalid {x["challenge_id"]}')

if guards.get('guard_count')!=31 or len(guards.get('guards',[]))!=31 or {x['knowledge_id'] for x in guards['guards']}!=scope: problems.append('Scope guard accounting mismatch')
for x in guards['guards']:
    if x['student_runtime'] or x['permanent_palace'] or x['challenge_lab']: problems.append(f'scope guard became runtime target {x["knowledge_id"]}')
    if x['canonical_statement']!=canon[x['knowledge_id']]['Canonical Verified Statement']: problems.append(f'scope guard science mismatch {x["knowledge_id"]}')

expected={'canonical_records':255,'runtime_memory_objects':211,'story_records':211,'challenge_lab_records':13,'scope_guard_records':31,'accounted_records':255,'unaccounted_records':0,'guided_journeys':8,'permanent_loci':58,'optional_first_exposure_recalls':18,'exact_name_review_targets':135,'non_exact_palace_records':76,'mandatory_spelling_targets':0,'mixed_discrimination_sets':40,'mixed_discrimination_questions':104}
for k,v in expected.items():
    if final.get(k)!=v: problems.append(f'finalization {k}={final.get(k)} expected {v}')
if final.get('release_status')!='STUDENT_READY_F5': problems.append('finalization release status wrong')

if reg.get('journey_count')!=8 or reg.get('scene_count')!=58 or reg.get('checkpoint_count')!=18 or reg.get('student_release') is not True or reg.get('preview_release') is not False: problems.append('F5 journey registry wrong')
if [x['palace_id'] for x in reg['guided_journeys']]!=[f'U8-J{i}' for i in range(1,9)]: problems.append('F5 journey order wrong')
if any(x.get('student_release')!='STUDENT_READY_F5' or x.get('preview_release') is not False for x in reg['guided_journeys']): problems.append('journey release flags wrong')
if [x['scene_count'] for x in reg['guided_journeys']]!=[12,9,5,7,5,8,4,8]: problems.append('journey scene route lengths wrong')

if status.get('status')!='STUDENT_READY' or status.get('student_release') is not True or status.get('preview_release') is not False: problems.append('Unit 8 student release state wrong')
if status.get('pipeline_stage') not in {'UNIT8_FINALIZED_F5','UNIT8_CLASSROOM_BROWSER_VALIDATED_F6'} or status.get('canonical_records_accounted')!=255 or status.get('runtime_memory_objects')!=211 or status.get('application_challenges')!=13: problems.append('Unit 8 status accounting wrong')
if release.get('student_release') is not True or release.get('preview_release') is not False or release.get('unaccounted_canonical_records')!=0: problems.append('F5 release manifest flags/accounting wrong')

# Frozen F1-F4H artifacts and all eight narratives.
for rel,digest in lock.get('protected_narratives',{}).items():
    if sha(U8/rel)!=digest: problems.append(f'protected narrative mismatch {rel}')
for rel,digest in lock.get('protected_upstream_locks',{}).items():
    if sha(U8/rel)!=digest: problems.append(f'protected upstream lock mismatch {rel}')
for rel,digest in lock.get('files',{}).items():
    if sha(U8/rel)!=digest: problems.append(f'F5 lock mismatch {rel}')

# Every story beat remains exactly F1 science and every palace-managed record occurs once across the frozen narratives.
seen=[]
for i in range(1,9):
    j=read(f'journeys/U8-J{i}.json')
    for s in j['scenes']:
        for b in s['story_beats']:
            seen.append(b['object_id'])
            if b['term']!=canon[b['object_id']]['Canonical Label'] or b['science']!=canon[b['object_id']]['Canonical Verified Statement']:
                problems.append(f'frozen narrative science drift {b["object_id"]}')
if len(seen)!=211 or len(set(seen))!=211 or set(seen)!=story: problems.append('frozen narratives do not cover 211 palace records exactly once')

# High-risk Unit 8 boundaries must remain explicit guards.
joined=' '.join(x['canonical_statement'] for x in guards['guards']).casefold()
phrases=[
    'do not encode a behavior as existing because an organism or population “needed” it',
    'do not explain altruism as natural selection sacrificing individuals for the good of the population',
    'do not say photosynthesis or chemosynthesis creates energy',
    'do not teach energy as recycled through ecosystems',
    'do not label dn/dt as the per-capita rate of increase',
    'do not say exponential growth adds a constant number per unit time',
    'do not treat k as a permanent species constant',
    'do not encode every species as intrinsically and permanently “r-selected” or “k-selected”',
    'do not label every nonnative species invasive',
    'do not say environmental pressure causes the useful mutation that organisms need',
    'do not use species diversity as a complete synonym for biodiversity',
    'do not encode greater diversity as an absolute guarantee',
    'do not duplicate detailed thylakoid/photosynthesis mechanisms as unit 8 permanent memory',
]
for phrase in phrases:
    if phrase not in joined: problems.append(f'missing Unit 8 scope/science protection: {phrase}')

course=json.loads((AP/'course.json').read_text(encoding='utf-8'))
cu8=next(u for u in course['units'] if u['unit_id']=='unit-8')
if cu8.get('status')!='STUDENT_READY' or cu8.get('student_release') is not True or cu8.get('runtime_memory_objects')!=211 or cu8.get('application_challenges')!=13: problems.append('course registry Unit 8 not student-ready')
main=json.loads((AP/'mainline-release-u1-u8.json').read_text(encoding='utf-8'))
if main.get('units')!=['unit-1','unit-2','unit-3','unit-4','unit-5','unit-6','unit-7','unit-8']: problems.append('mainline Unit list wrong')
if main.get('runtime_version') not in {'v2-apbio-0.29.0-u8-f5','v2-apbio-0.30.0-u8-f6'}: problems.append('mainline runtime version wrong')
if main.get('totals')!={'canonical_records_units_1_8':1561,'guided_journeys':58,'permanent_scenes':448,'challenge_lab_items':112}: problems.append(f'mainline totals wrong {main.get("totals")}')

# Live API gate.
health=client.get('/api/health').json()
if health.get('version') not in {'v2-apbio-0.29.0-u8-f5','v2-apbio-0.30.0-u8-f6'}: problems.append(f'health runtime wrong {health}')
unit=client.get('/api/units/unit-8').json()
if unit.get('status')!='STUDENT_READY' or unit.get('student_release') is not True: problems.append('live Unit 8 status not student-ready')
registry=client.get('/api/units/unit-8/journeys').json().get('guided_journeys',[])
if len(registry)!=8 or sum(x['scene_count'] for x in registry)!=58: problems.append('live Unit 8 journey registry wrong')
for i in range(1,9):
    if client.get(f'/api/units/unit-8/journeys/U8-J{i}').status_code!=200: problems.append(f'live Journey U8-J{i} unavailable')
if client.get('/api/units/unit-8/application-lab').json().get('challenge_count')!=13: problems.append('live Challenge Lab count wrong')
if client.get('/api/units/unit-8/review-manifest').json().get('target_count')!=135: problems.append('live Review count wrong')
if client.get('/api/units/unit-8/mixed-discrimination').json().get('set_count')!=40: problems.append('live mixed set count wrong')
if client.get('/api/units/unit-8/scope-guards').json().get('guard_count')!=31: problems.append('live scope guard count wrong')
if client.get('/api/units/unit-8/finalization').json().get('unaccounted_records')!=0: problems.append('live finalization accounting wrong')
obj=client.get('/api/units/unit-8/objects/U8-K-001')
if obj.status_code!=200 or obj.json().get('student_runtime') is not True: problems.append('live Unit 8 Memory Object unavailable')

if problems:
    print('UNIT8 F5 QA FAIL')
    print('\n'.join(f'- {x}' for x in problems))
    sys.exit(1)
print('UNIT8 F5 QA PASS')
print(json.dumps({'canonical_records':255,'runtime_memory_objects':211,'challenge_records':13,'scope_guards':31,'journeys':8,'loci':58,'optional_recalls':18,'exact_name_review_targets':135,'non_exact_palace_records':76,'mixed_sets':40,'mixed_questions':104,'unaccounted':0,'student_release':True,'runtime_version':'v2-apbio-0.29.0-u8-f5'},indent=2))
