from __future__ import annotations
import json, hashlib, sys
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def fail(msg): raise AssertionError(msg)

src=read(U2/'source/canonical-unit2-f1.json')
recs={x['knowledge_id']:x for x in src['canonical_catalog']}
cls=read(U2/'architecture/learning-classification-f2.json')
arch=read(U2/'architecture/palace-architecture-f2.json')
status=read(U2/'status.json')
lock=read(U2/'content-lock-f2.json')

assert len(recs)==142
assert len(cls['records'])==142
assert {x['knowledge_id'] for x in cls['records']}==set(recs)
assert Counter(x['destination'] for x in cls['records'])==Counter({'PALACE_EMBEDDED':84,'PALACE_PRIMARY_LOCUS':49,'CHALLENGE_LAB':9})
assert sum(x['exact_name_recall'] for x in cls['records'])==106
assert all(x['spelling_policy']=='ADAPTIVE_SUPPORT_ONLY_NO_MANDATORY_SPELLING_GATE' for x in cls['records'])

assert arch['counts']=={'canonical_records':142,'palace_managed_records':133,'practice_only_records':9,'journeys':7,'bundles':16,'permanent_loci':49,'confusable_sets':17}
assert len(arch['journeys'])==7
assert len(arch['loci'])==49
assert len(arch['challenge_lab'])==9
assert len(arch['confusable_sets'])==17

lids=[x['locus_id'] for x in arch['loci']]
assert len(lids)==len(set(lids))==49
assigned=[]
for l in arch['loci']:
    assert l['primary_knowledge_id'] in l['knowledge_ids']
    assert l['embedded_knowledge_ids']==[k for k in l['knowledge_ids'] if k!=l['primary_knowledge_id']]
    assert set(l['scene_geometry'])=={'left','center','right'}
    assert all(str(v).strip() for v in l['scene_geometry'].values())
    assert l['scientific_visual_required'] is True
    assert l['narrative_status']=='ARCHITECTURE_ONLY_NO_STORY_PROSE_F2'
    for kid in l['knowledge_ids']:
        assert kid in recs
        assert recs[kid]['retrieval_demand']!='APPLIED_TRANSFER'
    assigned += l['knowledge_ids']
assert len(assigned)==len(set(assigned))==133

challenge_ids=[x['knowledge_id'] for x in arch['challenge_lab']]
assert len(challenge_ids)==len(set(challenge_ids))==9
assert set(challenge_ids)=={x['knowledge_id'] for x in src['canonical_catalog'] if x['retrieval_demand']=='APPLIED_TRANSFER'}
assert set(assigned)|set(challenge_ids)==set(recs)
assert not (set(assigned)&set(challenge_ids))
assert all(all(l in set(lids) for l in x['prerequisite_loci']) for x in arch['challenge_lab'])

journey_loci=[]
bundle_ids=[]
for j in arch['journeys']:
    assert j['working_title'] and j['setting_logic'] and j['content_focus']
    for b in j['bundles']:
        bundle_ids.append(b['bundle_id']); journey_loci.extend(b['loci'])
        assert b['title'] and b['loci']
assert len(bundle_ids)==len(set(bundle_ids))==16
assert journey_loci==lids, 'journey/bundle route order must exactly match locus list order'

for cf in arch['confusable_sets']:
    assert len(cf['terms'])>=2
    assert len(cf['terms'])==len(set(cf['terms']))
    assert all(k in recs for k in cf['knowledge_ids'])

assert status['status']=='LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED'
assert status['pipeline_stage']=='LEARNING_CLASSIFICATION_AND_PALACE_ARCHITECTURE_COMPLETE'
assert status['student_release'] is False
assert status['journey_blueprints']==7 and status['permanent_locus_blueprints']==49

assert lock['lock_status']=='LOCKED_F2' and lock['student_release'] is False
for rel,meta in lock['files'].items():
    p=ROOT/rel
    assert p.exists(), rel
    assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256'], rel

# F2 itself released no runtime/story content. Later-stage finalization artifacts are allowed.
if not (U2/'finalization-f5.json').exists():
    for forbidden in ['memory-objects.json','journeys.json','application-lab.json']:
        assert not (U2/forbidden).exists(), forbidden

print('UNIT2 F2 QA PASS')
print(json.dumps({'canonical':142,'palace_managed':133,'challenge_lab':9,'journeys':7,'bundles':16,'loci':49,'confusables':17,'exact_name_targets':106,'mandatory_spelling':0},indent=2))
