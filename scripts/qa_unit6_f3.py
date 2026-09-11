from __future__ import annotations
import json,hashlib,sys,re
from pathlib import Path
from collections import Counter,defaultdict
ROOT=Path(__file__).resolve().parents[1]
U6=ROOT/'content'/'ap-biology'/'unit-6'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

src=read(U6/'source/canonical-unit6-f1.json'); canon={r['knowledge_id']:r for r in src['canonical_catalog']}
cls=read(U6/'architecture/learning-classification-f2.json'); class_by={r['knowledge_id']:r for r in cls['records']}
arch=read(U6/'architecture/palace-architecture-f2.json'); loci={l['locus_id']:l for l in arch['loci']}
scenes=read(U6/'briefs/scene-briefs-f3.json'); journeys=read(U6/'briefs/journey-briefs-f3.json')
status=read(U6/'status-f3.json'); release=read(U6/'f3-release-manifest.json'); lock=read(U6/'content-lock-f3.json')
up=read(U6/'upstream-u1-u5-protection-f1.json')
problems=[]
expected={'journeys':6,'scene_briefs':53,'palace_managed_records':161,'term_introductions':161,'optional_first_exposure_recalls':18}
if scenes.get('counts')!=expected: problems.append(f"scene counts {scenes.get('counts')} != {expected}")
if len(scenes.get('scene_briefs',[]))!=53: problems.append('scene brief count not 53')
if len(journeys.get('journeys',[]))!=6: problems.append('journey brief count not 6')

assigned=[]; intro_ids=[]; scene_index={}
for b in scenes.get('scene_briefs',[]):
    lid=b.get('locus_id'); scene_index[lid]=b; l=loci.get(lid)
    if not l: problems.append(f'{lid} not found in F2 architecture'); continue
    if b.get('journey_id')!=l['journey_id'] or b.get('bundle_id')!=l['bundle_id']: problems.append(f'{lid} journey/bundle changed from F2')
    if b.get('scene_title')!=l['title'] or b.get('micro_anchor')!=l['micro_anchor']: problems.append(f'{lid} title/micro anchor changed from F2')
    if b.get('knowledge_ids')!=l['knowledge_ids'] or b.get('primary_knowledge_id')!=l['primary_knowledge_id']: problems.append(f'{lid} knowledge assignment changed from F2')
    assigned.extend(b.get('knowledge_ids',[]))
    if len(b.get('orientation_sentence',''))<180: problems.append(f'{lid} orientation is too terse')
    layout=b.get('spatial_layout',{})
    if set(layout)!={'left','center','right'}: problems.append(f'{lid} missing left/center/right layout')
    else:
        for z in ('left','center','right'):
            if layout[z].get('anchor')!=l['scene_geometry'][z]: problems.append(f'{lid} {z} anchor changed from F2')
    cast=b.get('stable_cast',[])
    if len(cast)!=3 or [x.get('position') for x in cast]!=['left','center','right']: problems.append(f'{lid} stable cast invalid')
    if any(len(x.get('visual_identity',''))<90 or len(x.get('job_in_scene',''))<70 for x in cast): problems.append(f'{lid} cast descriptions too terse')
    action=b.get('science_bearing_action',{})
    if any(len(action.get(k,''))<150 for k in ('before','trigger','after')): problems.append(f'{lid} before/trigger/after too terse')
    steps=action.get('during',[])
    if len(steps)<3 or any(len(x)<70 for x in steps): problems.append(f'{lid} mechanism steps insufficient')
    intros=b.get('term_introductions',[])
    if len(intros)!=len(l['knowledge_ids']): problems.append(f'{lid} term introduction count mismatch')
    for t in intros:
        kid=t.get('knowledge_id'); intro_ids.append(kid)
        if kid not in canon: problems.append(f'{lid} unknown term intro {kid}'); continue
        r=canon[kid]; c=class_by[kid]
        if t.get('canonical_term')!=r['canonical_label'] or t.get('canonical_science')!=r['canonical_verified_statement']: problems.append(f'{lid} changed F1 canonical science for {kid}')
        if t.get('exact_name_recall')!=bool(c['exact_name_recall']) or t.get('delayed_review_target')!=bool(c['delayed_review_target']): problems.append(f'{lid} changed F2 recall policy for {kid}')
        if t.get('name_support')!=c['name_support'] or t.get('spelling_policy')!=c['spelling_policy']: problems.append(f'{lid} changed F2 name/spelling support for {kid}')
    # Every resolved review flag that touches a scene record must appear in guards.
    guard_text=' '.join(b.get('misconception_guards',[]))
    for kid in l['knowledge_ids']:
        for fid in canon[kid].get('review_flag_ids',[]):
            if fid and fid not in guard_text: problems.append(f'{lid} missing resolved review guard {fid}')
    # Every F2 discrimination set touching a scene must appear in guards.
    set_ids={s for kid in l['knowledge_ids'] for s in class_by[kid].get('discrimination_sets',[])}
    for sid in set_ids:
        if sid not in guard_text: problems.append(f'{lid} missing confusable guard {sid}')
    # Reactivation count/policy.
    expected_react={kid for kid in l['knowledge_ids'] if class_by[kid]['reactivation_mode']=='PRIOR_UNIT_REACTIVATION'}
    actual_react={x['knowledge_id'] for x in b.get('prior_unit_reactivation',[])}
    if actual_react!=expected_react: problems.append(f'{lid} prior-unit reactivation mismatch')
    if b.get('story_prose_status')!='PROHIBITED_UNTIL_F3_BRIEF_QA_PASS' or b.get('brief_status')!='LOCKED_F3_SCENE_BRIEF': problems.append(f'{lid} story prose/brief status invalid')
    if any(k in b for k in ('story_paragraphs','story_open','story_close','story_beats')): problems.append(f'{lid} contains premature polished narrative fields')

if len(assigned)!=161 or len(set(assigned))!=161: problems.append(f'assigned story records {len(assigned)}/{len(set(assigned))} != 161/161')
if len(intro_ids)!=161 or len(set(intro_ids))!=161: problems.append(f'term introductions {len(intro_ids)}/{len(set(intro_ids))} != 161/161')
palace_f2=[kid for l in arch['loci'] for kid in l['knowledge_ids']]
if assigned!=palace_f2: problems.append('F3 scene assignment order differs from F2 architecture')

# Quick recall distribution.
per=defaultdict(int)
for b in scenes['scene_briefs']:
    if b['quick_recall']['enabled']: per[b['journey_id']]+=1
expected_q={'U6-J1':3,'U6-J2':3,'U6-J3':3,'U6-J4':4,'U6-J5':3,'U6-J6':2}
if dict(per)!=expected_q: problems.append(f'quick recall distribution {dict(per)} != {expected_q}')

# Journey continuity and route.
for j in journeys['journeys']:
    jid=j['journey_id']; f2j=next(x for x in arch['journeys'] if x['journey_id']==jid)
    route=[lid for b in f2j['bundles'] for lid in b['loci']]
    if j.get('route')!=route: problems.append(f'{jid} route changed from F2')
    if any(len(j.get(k,''))<180 for k in ('premise','mission','stakes','continuity_object','opening_image','ending_payoff')): problems.append(f'{jid} journey brief field too terse')
    if len(j.get('recurring_scientific_cast',[]))<3: problems.append(f'{jid} recurring scientific cast incomplete')
    if len(j.get('narrative_constraints',[]))<15: problems.append(f'{jid} narrative constraints incomplete')
    if j.get('status')!='JOURNEY_BRIEF_LOCKED_F3_NO_POLISHED_STORY_PROSE': problems.append(f'{jid} journey status invalid')
    for i,lid in enumerate(route):
        expected_next=route[i+1] if i+1<len(route) else None
        trans=scene_index[lid].get('causal_transition',{})
        if trans.get('to_locus_id')!=expected_next: problems.append(f'{lid} transition points to wrong next locus')
        if len(trans.get('transition_logic',''))<180: problems.append(f'{lid} transition is too terse')

# Status/runtime boundary.
if status.get('status') not in {'SCIENCE_LOCKED_F1_NOT_STUDENT_RELEASED','LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}: problems.append(f"unexpected F3 status {status.get('status')}")
if (status.get('canonical_lock'),status.get('architecture_lock'),status.get('scene_brief_lock'))!=('LOCKED_F1','LOCKED_F2','LOCKED_F3'): problems.append('F1/F2/F3 lock state incorrect')
if status.get('status')!='STUDENT_READY':
    if status.get('student_release') or status.get('preview_release'): problems.append('Unit 6 became visible before F5')
    if status.get('status')=='SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED' and any(status.get(k)!=0 for k in ['journey_count','scene_count','memory_objects','application_challenges']): problems.append('Unit 6 student runtime is nonzero at F3')
if (status.get('architecture_journeys'),status.get('architecture_loci'),status.get('scene_briefs'))!=(6,53,53): problems.append('status architecture/brief counts mismatch')
if release.get('student_release') is not False or release.get('polished_story_files')!=0 or release.get('student_runtime_memory_objects')!=0: problems.append('F3 release manifest exposes runtime content')

# Earlier locks byte-identical to hashes captured by F3 lock.
for key in ('f1_protected_hashes','f2_protected_hashes'):
    for rel,h in lock.get(key,{}).items():
        p=ROOT/rel
        if not p.exists() or sha(p)!=h: problems.append(f'{key} changed: {rel}')
# Released Units 1-5 protected.
if up.get('protected_file_count')!=291: problems.append(f"upstream protection count {up.get('protected_file_count')} != 291")
for item in up.get('protected_files',[]):
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f"released Units 1-5 file changed: {item['path']}")
# F3 lock core files.
if lock.get('lock_status')!='LOCKED_F3' or lock.get('student_release') is not False: problems.append('F3 lock state invalid')
for rel,meta in lock.get('files',{}).items():
    p=ROOT/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F3 locked file changed: {rel}')

# Course registry.
course=read(ROOT/'content/ap-biology/course.json'); e=next((u for u in course['units'] if u['unit_id']=='unit-6'),None)
if not e: problems.append('Unit 6 missing from course registry')
else:
    allowed_status={'SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
    if e.get('status') not in allowed_status: problems.append('course registry Unit 6 F3-or-later state invalid')
    elif e.get('status')=='STUDENT_READY' and e.get('student_release') is not True: problems.append('course registry Unit 6 F5 release flag invalid')
    elif e.get('status')!='STUDENT_READY' and e.get('student_release') is not False: problems.append('course registry Unit 6 pre-F5 release flag invalid')
    if e.get('scene_brief_lock')!='LOCKED_F3' or e.get('scene_briefs')!=53: problems.append('course registry F3 accounting mismatch')
    if e.get('status')=='SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED' and (e.get('journey_count')!=0 or e.get('scene_count')!=0): problems.append('course registry contains Unit 6 runtime scenes before F4')
    if e.get('status')=='F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW' and (e.get('journey_count')!=1 or e.get('scene_count')!=12 or e.get('preview_release') is not True): problems.append('course registry F4A preview accounting invalid')
    if e.get('status')=='F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW' and (e.get('journey_count')!=2 or e.get('scene_count')!=20 or e.get('preview_release') is not True): problems.append('course registry F4B preview accounting invalid')
    if e.get('status')=='F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW' and (e.get('journey_count')!=3 or e.get('scene_count')!=28 or e.get('preview_release') is not True): problems.append('course registry F4C preview accounting invalid')
    if e.get('status')=='F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW' and (e.get('journey_count')!=4 or e.get('scene_count')!=40 or e.get('preview_release') is not True): problems.append('course registry F4D preview accounting invalid')

required=[U6/'briefs/journey-briefs-f3.json',U6/'briefs/scene-briefs-f3.json',U6/'status-f3.json',U6/'f3-release-manifest.json',U6/'content-lock-f3.json']
for p in required:
    if not p.exists(): problems.append(f'missing required F3 artifact: {p.relative_to(ROOT)}')

if problems:
    print('UNIT 6 F3 QA FAIL')
    for p in problems: print('-',p)
    sys.exit(1)
print('UNIT 6 F3 QA PASS')
print(json.dumps(expected,indent=2))
