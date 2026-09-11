from __future__ import annotations
import hashlib, json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content'/'ap-biology'/'unit-3'
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

src=load(U3/'source'/'canonical-unit3-f1.json')
cls=load(U3/'architecture'/'learning-classification-f2.json')
arch=load(U3/'architecture'/'palace-architecture-f2.json')
lock=load(U3/'content-lock-f2.json')
status=load(U3/'status-f2.json')
records={r['knowledge_id']:r for r in src['canonical_catalog']}
classified=cls['records']
assert len(records)==186
assert len(classified)==186
assert {r['knowledge_id'] for r in classified}==set(records)
assert cls['counts']['by_destination']=={
    'PALACE_EMBEDDED':117,'PALACE_PRIMARY_LOCUS':54,
    'SUPPORTING_NON_RUNTIME_SCOPE_GUARD':4,'CHALLENGE_LAB':11}
assert cls['counts']['exact_name_targets']==126
assert cls['counts']['mandatory_spelling_targets']==0
assert arch['counts']=={
    'canonical_records':186,'palace_managed_records':171,'scope_guard_records':4,
    'practice_only_records':11,'journeys':7,'bundles':20,'permanent_loci':54,'confusable_sets':28}
assert len(arch['journeys'])==7
assert len(arch['loci'])==54
assert sum(len(j['bundles']) for j in arch['journeys'])==20
assert len(arch['challenge_lab'])==11
assert len(arch['scope_guards'])==4
assert len(arch['confusable_sets'])==28
assert len({l['locus_id'] for l in arch['loci']})==54
assert len({l['primary_knowledge_id'] for l in arch['loci']})==54

palace_ids=[k for l in arch['loci'] for k in l['knowledge_ids']]
assert len(palace_ids)==171
assert len(set(palace_ids))==171
assert all(k in records for k in palace_ids)
challenge_ids={x['knowledge_id'] for x in arch['challenge_lab']}
scope_ids={x['knowledge_id'] for x in arch['scope_guards']}
assert len(challenge_ids)==11 and len(scope_ids)==4
assert set(palace_ids).isdisjoint(challenge_ids|scope_ids)
assert set(palace_ids)|challenge_ids|scope_ids==set(records)

locmap={k:l['locus_id'] for l in arch['loci'] for k in l['knowledge_ids']}
primary={l['primary_knowledge_id'] for l in arch['loci']}
for r in classified:
    kid=r['knowledge_id']
    if kid in challenge_ids:
        assert r['destination']=='CHALLENGE_LAB' and r['locus_id'] is None
    elif kid in scope_ids:
        assert r['destination']=='SUPPORTING_NON_RUNTIME_SCOPE_GUARD' and r['locus_id'] is None
    else:
        assert r['locus_id']==locmap[kid]
        assert r['destination']==('PALACE_PRIMARY_LOCUS' if kid in primary else 'PALACE_EMBEDDED')
    assert r['spelling_policy']=='ADAPTIVE_SUPPORT_ONLY_NO_MANDATORY_SPELLING_GATE'

for cf in arch['confusable_sets']:
    assert len(cf['knowledge_ids'])>=2
    assert all(k in records for k in cf['knowledge_ids'])

# F1 scientific files remain byte-identical to the F1 lock.
f1=load(U3/'content-lock-f1.json')
for item in f1['protected_files']:
    p=U3/item['path']
    assert sha(p)==item['sha256'] and p.stat().st_size==item['bytes']

for rel,meta in lock['files'].items():
    p=ROOT/rel
    assert sha(p)==meta['sha256'] and p.stat().st_size==meta['bytes']

assert status['student_release'] is False
assert status['journey_count']==0 and status['scene_count']==0 and status['memory_objects']==0
assert status['architecture_loci']==54 and status['architecture_journeys']==7
manifest=load(U3/'f2-release-manifest.json')
assert manifest['narrative_story_files']==0 and manifest['student_release'] is False
print('Unit 3 F2 QA PASS')
print(json.dumps(arch['counts'],indent=2))
print(json.dumps(cls['counts'],indent=2))
