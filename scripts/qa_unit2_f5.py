from __future__ import annotations
import json, hashlib, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
source=read(U2/'source/canonical-unit2-f1.json'); canon={r['knowledge_id']:r for r in source['canonical_catalog']}
cls=read(U2/'architecture/learning-classification-f2.json'); class_by={r['knowledge_id']:r for r in cls['records']}
arch=read(U2/'architecture/palace-architecture-f2.json')
lab=read(U2/'application-lab.json'); review=read(U2/'review-manifest-f5.json'); mixed=read(U2/'mixed-discrimination-f5.json'); final=read(U2/'finalization-f5.json'); status=read(U2/'status-f5.json'); lock=read(U2/'content-lock-f5.json'); reg=read(U2/'journeys-f5.json')

assert len(canon)==142
assert status['student_release'] is True and status['preview_release'] is False and status['status']=='STUDENT_READY'
assert reg['journey_count']==7 and reg['scene_count']==49 and reg['checkpoint_count']==17 and reg['student_release'] is True

story=[]; exact_story={}
for i in range(1,8):
    j=read(U2/'journeys'/f'U2-J{i}.json')
    for s in j['scenes']:
        story += s['object_ids']
        for b in s['story_beats']:
            if b.get('exact_name'): exact_story[b['object_id']]=b['term']
assert len(story)==len(set(story))==133

challenge_ids=[x['knowledge_id'] for x in lab['items']]
expected_challenge=[r['knowledge_id'] for r in cls['records'] if r['destination']=='CHALLENGE_LAB']
assert lab['challenge_count']==lab['practice_only_runtime_count']==9
assert set(challenge_ids)==set(expected_challenge) and len(set(challenge_ids))==9
for x in lab['items']:
    assert x['canonical_statement']==canon[x['knowledge_id']]['canonical_verified_statement']
    assert len(x['prompt'])>=100 and len(x['answer_guide'])>=100 and len(x['story_hint'])>=60
    assert x['practice_only_runtime'] is True
assert set(story).isdisjoint(challenge_ids)
assert set(story)|set(challenge_ids)==set(canon)

# All exact-name classifications are represented once in story and have answer-redacted review cues.
expected_exact={r['knowledge_id'] for r in cls['records'] if r['exact_name_recall']}
assert review['target_count']==106 and review['mandatory_spelling_targets']==0
assert {x['knowledge_id'] for x in review['targets']}==expected_exact==set(exact_story)
stop={'and','the','with','from','into','that','this','than','versus','for','of','to','in','as','a','an','or'}
for x in review['targets']:
    assert x['target_answer']==exact_story[x['knowledge_id']]
    assert x['canonical_science']==canon[x['knowledge_id']]['canonical_verified_statement']
    prompt=x['prompt'].lower(); answer=x['target_answer'].lower()
    assert answer not in prompt
    toks=[t for t in re.findall(r'[a-z]+',answer) if t not in stop and len(t)>=4]
    for t in toks:
        stem=t[:5] if len(t)>=6 else t[:max(3,len(t)-1)]
        assert not re.search(rf'\b{re.escape(stem)}[a-z]*\b',prompt),(x['knowledge_id'],x['target_answer'],t,x['prompt'])
    assert len(x['hint'])>=25

# All 17 F2 confusable sets are operationalized, with answer-free prompts and valid choices.
arch_sets={x['set_id']:x for x in arch['confusable_sets']}
assert mixed['set_count']==17 and mixed['question_count']==44
assert {x['set_id'] for x in mixed['sets']}==set(arch_sets)
for s in mixed['sets']:
    assert s['knowledge_ids']==arch_sets[s['set_id']]['knowledge_ids']
    assert s['initial_delay_hours']>=48 and len(s['questions'])>=2
    for q in s['questions']:
        assert q['answer'] in q['choices'] and len(set(q['choices']))==len(q['choices'])
        assert q['answer'].lower() not in q['prompt'].lower()
        assert len(q['explanation'])>=35

assert final['canonical_records']==final['accounted_records']==142 and final['unaccounted_records']==0
assert final['story_records']==133 and final['challenge_lab_records']==9
assert final['guided_journeys']==7 and final['permanent_loci']==49
assert final['exact_name_review_targets']==106 and final['mandatory_spelling_targets']==0
assert final['mixed_discrimination_sets']==17 and final['mixed_discrimination_questions']==44
assert set(final['destinations']['story'])==set(story)
assert set(final['destinations']['challenge_lab'])==set(challenge_ids)
assert all(v.startswith('PASS') for v in final['release_gate'].values())

for rel,digest in lock['files'].items():
    p=U2/rel; assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest

print('UNIT2 F5 QA PASS')
print(json.dumps({'canonical_records':142,'story_records':133,'challenge_records':9,'journeys':7,'loci':49,'exact_name_review_targets':106,'mixed_sets':17,'mixed_questions':44,'unaccounted':0,'student_release':True},indent=2))
