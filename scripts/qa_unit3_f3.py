from __future__ import annotations
import json, hashlib, re
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content/ap-biology/unit-3'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

src=read(U3/'source/canonical-unit3-f1.json'); recs={r['knowledge_id']:r for r in src['canonical_catalog']}
f2=read(U3/'architecture/palace-architecture-f2.json')
js=read(U3/'briefs/journey-briefs-f3.json'); sb=read(U3/'briefs/scene-briefs-f3.json')
status=read(U3/'status-f3.json'); lock=read(U3/'content-lock-f3.json')
assert len(recs)==186
assert js['journey_count']==7 and len(js['journeys'])==7
assert sb['counts']=={'journeys':7,'scene_briefs':54,'palace_managed_records':171,'term_introductions':171,'optional_first_exposure_recalls':18}
assert len(sb['scene_briefs'])==54
assert status['status']=='SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED'
assert status['student_release'] is False and status['journey_count']==0 and status['scene_count']==0
f2_lids=[l['locus_id'] for l in f2['loci']]; f3_lids=[b['locus_id'] for b in sb['scene_briefs']]
assert f2_lids==f3_lids
assigned=[]; recalls=Counter(); prohibited=('ppt','college board','the packet','source slide','teacher test')
for b,l in zip(sb['scene_briefs'],f2['loci']):
    assert b['journey_id']==l['journey_id'] and b['bundle_id']==l['bundle_id']
    assert b['micro_anchor']==l['micro_anchor']
    assert len(b['orientation_sentence'])>=120
    assert set(b['spatial_layout'])=={'left','center','right'}
    assert [b['spatial_layout'][z]['anchor'] for z in ('left','center','right')]==[l['scene_geometry'][z] for z in ('left','center','right')]
    assert len(b['stable_cast'])==3
    assert all(len(c['visual_identity'])>=40 and len(c['job_in_scene'])>=35 for c in b['stable_cast'])
    act=b['science_bearing_action']; assert len(act['before'])>=100 and len(act['during'])>=3 and len(act['after'])>=100
    assert all(len(x)>=75 for x in act['during'])
    assert b['knowledge_ids']==l['knowledge_ids'] and b['primary_knowledge_id']==l['primary_knowledge_id']
    assert len(b['term_introductions'])==len(l['knowledge_ids'])
    assert [t['knowledge_id'] for t in b['term_introductions']]==l['knowledge_ids']
    for t in b['term_introductions']:
        r=recs[t['knowledge_id']]
        assert t['canonical_term']==r['canonical_label']
        assert t['canonical_science']==r['canonical_verified_statement']
        assert t['exact_name_recall']==r['exact_name_recall']
    assert b['visual_spec']['conventional_scientific_visual_required'] is True
    assert len(b['visual_spec']['must_show'])>=4
    assert b['misconception_guards']
    assert len(b['carry_forward'])>=45
    assert b['story_prose_status']=='PROHIBITED_UNTIL_F3_BRIEF_QA_PASS'
    assert b['brief_status']=='LOCKED_F3_SCENE_BRIEF'
    text=' '.join([b['orientation_sentence'],act['before'],act['after'],*act['during']]).lower()
    assert not [x for x in prohibited if x in text]
    if b['quick_recall'].get('enabled'):
        recalls[b['journey_id']]+=1
        assert b['quick_recall']['candidate_prompt'] and b['quick_recall']['answer']
    assigned += b['knowledge_ids']
assert len(assigned)==len(set(assigned))==171
palace={k for l in f2['loci'] for k in l['knowledge_ids']}
assert set(assigned)==palace
assert sum(recalls.values())==18
assert dict(recalls)=={'U3-J1':2,'U3-J2':3,'U3-J3':3,'U3-J4':4,'U3-J5':2,'U3-J6':3,'U3-J7':1}
for j,f2j in zip(js['journeys'],f2['journeys']):
    route=[lid for b in f2j['bundles'] for lid in b['loci']]
    assert j['route']==route
    assert j['unit_guide']['name']=='Dr. Nia Park'
    assert len(j['premise'])>=120 and len(j['mission'])>=100 and len(j['ending_payoff'])>=90
    assert len(j['narrative_constraints'])>=8
    assert j['status']=='JOURNEY_BRIEF_LOCKED_F3_NO_POLISHED_STORY_PROSE'
index={b['locus_id']:b for b in sb['scene_briefs']}
for j in js['journeys']:
    for i,lid in enumerate(j['route']):
        exp=j['route'][i+1] if i+1<len(j['route']) else None
        assert index[lid]['causal_transition']['to_locus_id']==exp
assert lock['lock_status']=='LOCKED_F3' and lock['student_release'] is False
for rel,meta in lock['files'].items():
    p=ROOT/rel; assert p.exists() and sha(p)==meta['sha256'], rel
manifest=read(U3/'f3-release-manifest.json')
assert manifest['polished_story_files']==0 and manifest['student_release'] is False
assert not (U3/'memory-objects.json').exists()
print('UNIT3 F3 QA PASS')
print(json.dumps(sb['counts'],indent=2))
