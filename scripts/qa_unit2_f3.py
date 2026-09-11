from __future__ import annotations
import json, hashlib, re
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

src=read(U2/'source/canonical-unit2-f1.json')
recs={r['knowledge_id']:r for r in src['canonical_catalog']}
f2=read(U2/'architecture/palace-architecture-f2.json')
journeys=read(U2/'briefs/journey-briefs-f3.json')
scenes=read(U2/'briefs/scene-briefs-f3.json')
status=read(U2/'status-f3.json')
lock=read(U2/'content-lock-f3.json')

assert len(recs)==142
assert journeys['journey_count']==7 and len(journeys['journeys'])==7
assert scenes['counts']=={'journeys':7,'scene_briefs':49,'palace_managed_records':133,'term_introductions':133,'optional_first_exposure_recalls':17}
assert len(scenes['scene_briefs'])==49
assert status['status']=='SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED'
assert status['student_release'] is False and status['narrative_story_files']==0

f2_lids=[l['locus_id'] for l in f2['loci']]
f3_lids=[b['locus_id'] for b in scenes['scene_briefs']]
assert f3_lids==f2_lids

assigned=[]
prohibited=('ppt','ced','campbell','college board','locked definition','canonical record','source material','class notes','the packet')
recall_by_journey=Counter()
for b,l in zip(scenes['scene_briefs'],f2['loci']):
    assert b['journey_id']==l['journey_id'] and b['bundle_id']==l['bundle_id']
    assert b['micro_anchor']==l['micro_anchor']
    assert len(b['orientation_sentence'])>=100
    assert set(b['spatial_layout'])=={'left','center','right'}
    assert [b['spatial_layout'][z]['anchor'] for z in ('left','center','right')]==[l['scene_geometry'][z] for z in ('left','center','right')]
    assert len(b['stable_cast'])>=2
    for c in b['stable_cast']:
        assert c['name'] and len(c['visual_identity'])>=10 and len(c['job_in_scene'])>=10
    action=b['science_bearing_action']
    assert len(action['before'])>=40 and len(action['during'])>=2 and len(action['after'])>=40
    assert all(len(x)>=40 for x in action['during'])
    assert b['knowledge_ids']==l['knowledge_ids']
    assert b['primary_knowledge_id']==l['primary_knowledge_id']
    assert len(b['term_introductions'])==len(l['knowledge_ids'])
    assert [t['knowledge_id'] for t in b['term_introductions']]==l['knowledge_ids']
    for t in b['term_introductions']:
        r=recs[t['knowledge_id']]
        assert t['canonical_term']==r['canonical_label']
        assert t['canonical_science']==r['canonical_verified_statement']
        assert t['exact_name_recall']==r['exact_name_recall']
    assert b['visual_spec']['conventional_scientific_visual_required'] is True
    assert len(b['visual_spec']['must_show'])>=2
    assert b['misconception_guards']
    assert len(b['carry_forward'])>=35
    assert b['story_prose_status']=='PROHIBITED_UNTIL_F3_BRIEF_QA_PASS'
    assert b['brief_status']=='LOCKED_F3_SCENE_BRIEF'
    student_future=' '.join([
        b['orientation_sentence'], action['before'], action['after'], b['carry_forward'],
        b['causal_transition']['transition_logic'], *action['during'],
        *[c['visual_identity']+' '+c['job_in_scene'] for c in b['stable_cast']]
    ]).lower()
    hits=[x for x in prohibited if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])', student_future)]
    assert not hits, (b['locus_id'], hits)
    if b['quick_recall'].get('enabled'):
        recall_by_journey[b['journey_id']]+=1
        assert b['quick_recall']['candidate_prompt'] and b['quick_recall']['answer']
    assigned+=b['knowledge_ids']
assert len(assigned)==len(set(assigned))==133
assert set(assigned)=={r['knowledge_id'] for r in src['canonical_catalog'] if r['retrieval_demand']!='APPLIED_TRANSFER'}
assert sum(recall_by_journey.values())==17
assert recall_by_journey['U2-J1']==4
assert all(v<=3 for k,v in recall_by_journey.items() if k!='U2-J1')

# Every journey has coherent fixed guide and exact route.
for j,f2j in zip(journeys['journeys'],f2['journeys']):
    route=[lid for bundle in f2j['bundles'] for lid in bundle['loci']]
    assert j['route']==route
    assert j['unit_guide']['name']=='Dr. Nia Park'
    assert len(j['premise'])>=100 and len(j['mission'])>=80 and len(j['ending_payoff'])>=80
    assert j['continuity_object'] and j['opening_image'] and j['stakes']
    assert len(j['narrative_constraints'])>=6
    assert j['status']=='JOURNEY_BRIEF_LOCKED_F3_NO_POLISHED_STORY_PROSE'

# Transitions point to the next locus inside a journey; finals end the route.
by_journey={j['journey_id']:j['route'] for j in journeys['journeys']}
brief_index={b['locus_id']:b for b in scenes['scene_briefs']}
for jid,route in by_journey.items():
    for i,lid in enumerate(route):
        expected=route[i+1] if i+1<len(route) else None
        assert brief_index[lid]['causal_transition']['to_locus_id']==expected

# Locks and no premature release.
assert lock['lock_status']=='LOCKED_F3' and lock['student_release'] is False
for rel,meta in lock['files'].items():
    p=ROOT/rel
    assert p.exists(), rel
    assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256'], rel
if not (U2/'finalization-f5.json').exists():
    for forbidden in ['memory-objects.json','application-lab.json']:
        assert not (U2/forbidden).exists(), forbidden

print('UNIT2 F3 QA PASS')
print(json.dumps({'canonical':142,'journeys':7,'scene_briefs':49,'palace_managed':133,'term_introductions':133,'optional_first_exposure_recalls':17,'polished_story_files':0},indent=2))
