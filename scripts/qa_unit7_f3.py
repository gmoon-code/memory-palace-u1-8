from __future__ import annotations
import json,hashlib,sys
from pathlib import Path
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content'/'ap-biology'/'unit-7'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

src=read(U7/'source/canonical-unit7-f1.json')
arch=read(U7/'architecture/palace-architecture-f2.json')
cls=read(U7/'architecture/learning-classification-f2.json')
journeys=read(U7/'briefs/journey-briefs-f3.json')
scenes=read(U7/'briefs/scene-briefs-f3.json')
lock=read(U7/'content-lock-f3.json')
status=read(U7/'status-f3.json')
release=read(U7/'f3-release-manifest.json')
up=read(U7/'upstream-u1-u6-protection-f1.json')
problems=[]
canon={r['knowledge_id']:r for r in src['canonical_catalog']}
class_by={r['knowledge_id']:r for r in cls['records']}
scene_index={b['locus_id']:b for b in scenes['scene_briefs']}

expected={'journeys':6,'scene_briefs':55,'palace_managed_records':174,'term_introductions':174,'optional_first_exposure_recalls':18}
if scenes.get('counts')!=expected: problems.append(f"scene counts {scenes.get('counts')} != {expected}")
if len(scenes['scene_briefs'])!=55: problems.append('scene brief count is not 55')
if len(journeys['journeys'])!=6: problems.append('journey brief count is not 6')
if [b['locus_id'] for b in scenes['scene_briefs']] != [f'U7-L{i:02d}' for i in range(1,56)]: problems.append('F3 locus order is not U7-L01..U7-L55')

assigned=[]; intro_ids=[]
for b,l in zip(scenes['scene_briefs'],arch['loci']):
    if b['locus_id']!=l['locus_id']: problems.append(f"scene/F2 locus mismatch {b['locus_id']} vs {l['locus_id']}")
    if b['knowledge_ids']!=l['knowledge_ids']: problems.append(f"{b['locus_id']} knowledge assignment changed from F2")
    assigned.extend(b['knowledge_ids'])
    if b['primary_knowledge_id']!=l['primary_knowledge_id']: problems.append(f"{b['locus_id']} primary anchor changed")
    if [b['spatial_layout'][z]['anchor'] for z in ('left','center','right')] != [l['scene_geometry'][z] for z in ('left','center','right')]: problems.append(f"{b['locus_id']} spatial geometry changed")
    if len(b.get('orientation_sentence',''))<180: problems.append(f"{b['locus_id']} orientation too terse")
    if len(b.get('stable_cast',[]))!=3: problems.append(f"{b['locus_id']} stable cast count not 3")
    if any(not x.get('visual_identity') or not x.get('job_in_scene') for x in b.get('stable_cast',[])): problems.append(f"{b['locus_id']} cast identity/job incomplete")
    act=b.get('science_bearing_action',{})
    if len(act.get('during',[]))!=3 or any(len(x)<90 for x in act.get('during',[])): problems.append(f"{b['locus_id']} science-bearing action incomplete")
    if len(act.get('before',''))<160 or len(act.get('after',''))<180: problems.append(f"{b['locus_id']} before/after state too terse")
    if b.get('story_prose_status')!='PROHIBITED_UNTIL_F3_BRIEF_QA_PASS' or b.get('brief_status')!='LOCKED_F3_SCENE_BRIEF': problems.append(f"{b['locus_id']} F3 status invalid")
    for forbidden in ('story_paragraphs','story_open','story_close','dialogue','narrative_prose'):
        if forbidden in b: problems.append(f"{b['locus_id']} contains prohibited polished-prose field {forbidden}")
    if set(b.get('spatial_layout',{}))!={'left','center','right'}: problems.append(f"{b['locus_id']} spatial keys invalid")
    if not b.get('continuity_object'): problems.append(f"{b['locus_id']} continuity object missing")
    if not b.get('visual_spec',{}).get('conventional_scientific_visual_required'): problems.append(f"{b['locus_id']} scientific visual not required")
    if len(b.get('visual_spec',{}).get('must_show',[]))<6: problems.append(f"{b['locus_id']} must_show incomplete")
    terms=b.get('term_introductions',[]); intro_ids.extend(t['knowledge_id'] for t in terms)
    if [t['knowledge_id'] for t in terms]!=b['knowledge_ids']: problems.append(f"{b['locus_id']} term introduction order mismatch")
    for t in terms:
        r=canon[t['knowledge_id']]; c=class_by[t['knowledge_id']]
        if t['canonical_term']!=r['canonical_label'] or t['canonical_science']!=r['canonical_verified_statement']: problems.append(f"{b['locus_id']} altered F1 science for {t['knowledge_id']}")
        if bool(t['delayed_review_target'])!=bool(c['delayed_review_target']): problems.append(f"{b['locus_id']} review target changed for {t['knowledge_id']}")
        if t['reactivation_mode']!=c['reactivation_mode']: problems.append(f"{b['locus_id']} reactivation changed for {t['knowledge_id']}")
    # Guards should be present whenever a record carries F1 flags or confusable membership.
    flagged=any(canon[k].get('review_flag_ids') for k in b['knowledge_ids'])
    conf=any(class_by[k].get('discrimination_sets') for k in b['knowledge_ids'])
    if (flagged or conf) and not b.get('misconception_guards'): problems.append(f"{b['locus_id']} missing misconception/discrimination guards")
    if len(b.get('causal_transition',{}).get('transition_logic',''))<260: problems.append(f"{b['locus_id']} causal transition too terse")

if len(assigned)!=174 or len(set(assigned))!=174: problems.append(f'assigned story records {len(assigned)}/{len(set(assigned))} != 174/174')
if len(intro_ids)!=174 or len(set(intro_ids))!=174: problems.append(f'term introductions {len(intro_ids)}/{len(set(intro_ids))} != 174/174')
palace_f2=[kid for l in arch['loci'] for kid in l['knowledge_ids']]
if assigned!=palace_f2: problems.append('F3 scene assignment order differs from F2 architecture')

# Sparse Quick Recall distribution.
per=defaultdict(int)
for b in scenes['scene_briefs']:
    if b['quick_recall']['enabled']:
        per[b['journey_id']]+=1
        if not b['quick_recall']['candidate_prompt'] or not b['quick_recall']['answer']: problems.append(f"{b['locus_id']} enabled recall is incomplete")
expected_q={'U7-J1':3,'U7-J2':4,'U7-J3':3,'U7-J4':3,'U7-J5':3,'U7-J6':2}
if dict(per)!=expected_q: problems.append(f'quick recall distribution {dict(per)} != {expected_q}')

# Journey continuity and route.
for j in journeys['journeys']:
    jid=j['journey_id']; f2j=next(x for x in arch['journeys'] if x['journey_id']==jid)
    route=[lid for b in f2j['bundles'] for lid in b['loci']]
    if j.get('route')!=route: problems.append(f'{jid} route changed from F2')
    if any(len(j.get(k,''))<260 for k in ('premise','mission','stakes','continuity_object','opening_image','ending_payoff')): problems.append(f'{jid} journey brief field too terse')
    if len(j.get('recurring_scientific_cast',[]))<3: problems.append(f'{jid} recurring scientific cast incomplete')
    if len(j.get('narrative_constraints',[]))<20: problems.append(f'{jid} narrative constraints incomplete')
    if j.get('status')!='JOURNEY_BRIEF_LOCKED_F3_NO_POLISHED_STORY_PROSE': problems.append(f'{jid} journey status invalid')
    for i,lid in enumerate(route):
        expected_next=route[i+1] if i+1<len(route) else None
        trans=scene_index[lid].get('causal_transition',{})
        if trans.get('to_locus_id')!=expected_next: problems.append(f'{lid} transition points to wrong next locus')

# Prior-unit reactivation remains six and not duplicated.
react=[(b['locus_id'],x['knowledge_id']) for b in scenes['scene_briefs'] for x in b.get('prior_unit_reactivation',[])]
if len(react)!=6 or len({kid for _,kid in react})!=6: problems.append(f'prior-unit reactivation accounting {len(react)} != 6')

# Status/runtime boundary.
if status.get('status')!='SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED': problems.append(f"unexpected F3 status {status.get('status')}")
if (status.get('canonical_lock'),status.get('architecture_lock'),status.get('scene_brief_lock'))!=('LOCKED_F1','LOCKED_F2','LOCKED_F3'): problems.append('F1/F2/F3 lock state incorrect')
if status.get('student_release') or status.get('preview_release'): problems.append('Unit 7 became visible at F3')
if any(status.get(k)!=0 for k in ['journey_count','scene_count','memory_objects','application_challenges']): problems.append('Unit 7 student runtime is nonzero at F3')
if (status.get('architecture_journeys'),status.get('architecture_loci'),status.get('scene_briefs'))!=(6,55,55): problems.append('status architecture/brief counts mismatch')
if release.get('student_release') is not False or release.get('polished_story_files')!=0 or release.get('student_runtime_memory_objects')!=0: problems.append('F3 release manifest exposes runtime content')

# Earlier locks byte-identical.
for key in ('f1_protected_hashes','f2_protected_hashes'):
    for rel,h in lock.get(key,{}).items():
        p=ROOT/rel
        if not p.exists() or sha(p)!=h: problems.append(f'{key} changed: {rel}')
# Released Units 1-6 protected.
if up.get('protected_file_count')!=356: problems.append(f"upstream protection count {up.get('protected_file_count')} != 356")
for item in up.get('protected_files',[]):
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f"released Units 1-6 file changed: {item['path']}")
# F3 lock files.
if lock.get('lock_status')!='LOCKED_F3' or lock.get('student_release') is not False: problems.append('F3 lock state invalid')
for rel,meta in lock.get('files',{}).items():
    p=ROOT/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F3 locked file changed: {rel}')

course=read(ROOT/'content/ap-biology/course.json'); e=next((u for u in course['units'] if u['unit_id']=='unit-7'),None)
if not e: problems.append('Unit 7 missing from course registry')
else:
    allowed_course={'SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
    if e.get('status') not in allowed_course: problems.append('course registry Unit 7 F3-or-later state invalid')
    if e.get('status')=='STUDENT_READY' and e.get('student_release') is not True: problems.append('course registry Unit 7 F5 release invalid while preserving F3')
    if e.get('status')!='STUDENT_READY' and e.get('student_release') is not False: problems.append('course registry Unit 7 pre-F5 release invalid while preserving F3')
    if e.get('scene_brief_lock')!='LOCKED_F3' or e.get('scene_briefs')!=55: problems.append('course registry F3 accounting mismatch')
    if e.get('status')=='SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED' and (e.get('journey_count')!=0 or e.get('scene_count')!=0): problems.append('course registry contains Unit 7 runtime scenes before F4')
    if e.get('status')=='F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW' and (e.get('journey_count'),e.get('scene_count'))!=(1,10): problems.append('course registry F4A preview counts invalid')
    if e.get('status')=='F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW' and (e.get('journey_count'),e.get('scene_count'))!=(2,24): problems.append('course registry F4B preview counts invalid')
    if e.get('status')=='F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW' and (e.get('journey_count'),e.get('scene_count'))!=(3,33): problems.append('course registry F4C preview counts invalid')
    if e.get('status')=='F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW' and (e.get('journey_count'),e.get('scene_count'))!=(4,41): problems.append('course registry F4D preview counts invalid')
for n in range(1,7):
    e=next((u for u in course['units'] if u['unit_id']==f'unit-{n}'),None)
    if not e or e.get('status')!='STUDENT_READY': problems.append(f'upstream Unit {n} is no longer STUDENT_READY')
for p in ROOT.rglob('*.pdf'): problems.append(f'forbidden source PDF in repository: {p.relative_to(ROOT)}')

required=[
 U7/'briefs/journey-briefs-f3.json',U7/'briefs/scene-briefs-f3.json',U7/'status-f3.json',U7/'f3-release-manifest.json',U7/'content-lock-f3.json',
 U7/'audit/APBIO_Unit7_F3_Scene_Briefs.xlsx',ROOT/'docs/UNIT7_F3_SCENE_BRIEFS.md',ROOT/'docs/UNIT7_F3_QA.md',ROOT/'docs/UNIT7_F3_RELEASE.md'
]
for p in required:
    if not p.exists(): problems.append(f'missing required F3 artifact: {p.relative_to(ROOT)}')

if problems:
    print('UNIT 7 F3 QA FAIL')
    for p in problems: print('-',p)
    sys.exit(1)
print('UNIT 7 F3 QA PASS')
print(json.dumps(expected,indent=2))
