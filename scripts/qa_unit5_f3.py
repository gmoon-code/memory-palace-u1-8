from __future__ import annotations
import json, hashlib, sys
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

problems=[]
src=read(U5/'source/canonical-unit5-f1.json'); recs={r['knowledge_id']:r for r in src['canonical_catalog']}
f2=read(U5/'architecture/palace-architecture-f2.json')
cls=read(U5/'architecture/learning-classification-f2.json'); class_by_id={r['knowledge_id']:r for r in cls['records']}
sc=read(U5/'briefs/scene-briefs-f3.json'); js=read(U5/'briefs/journey-briefs-f3.json')
status=read(U5/'status-f3.json'); release=read(U5/'f3-release-manifest.json'); lock=read(U5/'content-lock-f3.json')

expected_counts={'journeys':8,'scene_briefs':50,'palace_managed_records':131,'term_introductions':131,'optional_first_exposure_recalls':18}
if sc.get('counts')!=expected_counts: problems.append(f"scene brief counts mismatch: {sc.get('counts')}")
if js.get('journey_count')!=8 or len(js.get('journeys',[]))!=8: problems.append('journey brief count is not 8')
briefs=sc.get('scene_briefs',[])
if len(briefs)!=50: problems.append('scene brief list length is not 50')
if [b.get('locus_id') for b in briefs]!=[f'U5-L{i:02d}' for i in range(1,51)]: problems.append('F3 scene-brief order/IDs changed from U5-L01..U5-L50')

f2_loci={l['locus_id']:l for l in f2['loci']}
scene_index={b['locus_id']:b for b in briefs}
prohibited=['ppt','college board','campbell','course and exam description','source lock','canonical record','review flag','assessment semantic crosswalk','teacher slide']
recalls=Counter(); assigned=[]
for b in briefs:
    lid=b['locus_id']; l=f2_loci.get(lid)
    if not l:
        problems.append(f'{lid} missing from F2 architecture'); continue
    if b.get('scene_title')!=l.get('title') or b.get('micro_anchor')!=l.get('micro_anchor'): problems.append(f'{lid} changed F2 title or micro-anchor')
    if len(b.get('orientation_sentence',''))<180: problems.append(f'{lid} orientation is too terse')
    layout=b.get('spatial_layout',{})
    if set(layout)!={'left','center','right'}: problems.append(f'{lid} lacks exact left/center/right layout')
    else:
        actual=[layout[z].get('anchor') for z in ('left','center','right')]
        expected=[l['scene_geometry'][z] for z in ('left','center','right')]
        if actual!=expected: problems.append(f'{lid} scene geometry changed from F2')
    cast=b.get('stable_cast',[])
    if len(cast)!=3: problems.append(f'{lid} does not have exactly three fixed scientific cast/zone entries')
    else:
        if [c.get('position') for c in cast]!=['left','center','right']: problems.append(f'{lid} cast positions are not left/center/right')
        for c in cast:
            if len(c.get('visual_identity',''))<90: problems.append(f"{lid} {c.get('position')} visual identity is underspecified")
            if len(c.get('job_in_scene',''))<90: problems.append(f"{lid} {c.get('position')} job is underspecified")
    act=b.get('science_bearing_action',{})
    if len(act.get('before',''))<180: problems.append(f'{lid} before-state is underspecified')
    if len(act.get('trigger',''))<120: problems.append(f'{lid} trigger is underspecified')
    if len(act.get('during',[]))!=3: problems.append(f'{lid} does not have exactly three core action steps')
    for n,x in enumerate(act.get('during',[]),1):
        if len(x)<125: problems.append(f'{lid} action step {n} is too terse')
    if len(act.get('after',''))<185: problems.append(f'{lid} after-state is underspecified')
    terms=b.get('term_introductions',[])
    if len(terms)!=len(l['knowledge_ids']): problems.append(f'{lid} term-introduction count differs from knowledge count')
    if [t.get('knowledge_id') for t in terms]!=l['knowledge_ids']: problems.append(f'{lid} term-introduction order/IDs differ from F2')
    for t in terms:
        kid=t.get('knowledge_id'); r=recs[kid]; c=class_by_id[kid]
        if t.get('canonical_term')!=r['canonical_label']: problems.append(f'{lid}/{kid} canonical label changed')
        if t.get('canonical_science')!=r['canonical_verified_statement']: problems.append(f'{lid}/{kid} canonical science changed')
        if t.get('exact_name_recall')!=bool(r.get('exact_name_recall')): problems.append(f'{lid}/{kid} exact-name state changed')
        if t.get('name_support')!=c.get('name_support'): problems.append(f'{lid}/{kid} name-support class changed')
        if t.get('spelling_policy')!=c.get('spelling_policy'): problems.append(f'{lid}/{kid} spelling policy changed')
        if not t.get('insertion_rule') or not t.get('name_support_rule'): problems.append(f'{lid}/{kid} lacks authoring rules')
    visual=b.get('visual_spec',{})
    if visual.get('conventional_scientific_visual_required') is not True: problems.append(f'{lid} does not require conventional scientific visual')
    if visual.get('visual_mode')!=l.get('visual_mode'): problems.append(f'{lid} visual mode changed from F2')
    if len(visual.get('must_show',[]))<6: problems.append(f'{lid} visual must-show list is too thin')
    if len(b.get('misconception_guards',[]))<1: problems.append(f'{lid} lacks misconception/discrimination guards')
    if len(b.get('exit_memory',{}).get('one_sentence_model',''))<100 or len(b.get('exit_memory',{}).get('redraw_test',''))<130: problems.append(f'{lid} lacks a usable exit-memory reconstruction test')
    if b.get('story_prose_status')!='PROHIBITED_UNTIL_F3_BRIEF_QA_PASS': problems.append(f'{lid} story prose was prematurely enabled')
    if b.get('brief_status')!='LOCKED_F3_SCENE_BRIEF': problems.append(f'{lid} brief status is not LOCKED_F3_SCENE_BRIEF')
    candidate=' '.join([b.get('orientation_sentence',''),act.get('before',''),act.get('trigger',''),act.get('after',''),*act.get('during',[]),b.get('exit_memory',{}).get('one_sentence_model',''),b.get('causal_transition',{}).get('transition_logic','')]).lower()
    bad=[x for x in prohibited if x in candidate]
    if bad: problems.append(f'{lid} future-prose fields expose source-management language {bad}')
    if b.get('quick_recall',{}).get('enabled'):
        recalls[b['journey_id']]+=1
        if not b['quick_recall'].get('candidate_prompt') or not b['quick_recall'].get('answer'): problems.append(f'{lid} enabled recall is incomplete')
    assigned += b['knowledge_ids']

if len(assigned)!=131 or len(set(assigned))!=131: problems.append(f'F3 assignment is {len(assigned)} refs / {len(set(assigned))} unique, expected 131/131')
palace={k for l in f2['loci'] for k in l['knowledge_ids']}
if set(assigned)!=palace: problems.append('F3 palace records do not equal the locked F2 palace partition')
expected_recall={'U5-J1':2,'U5-J2':3,'U5-J3':2,'U5-J4':2,'U5-J5':2,'U5-J6':2,'U5-J7':2,'U5-J8':3}
if dict(recalls)!=expected_recall: problems.append(f'recall distribution {dict(recalls)} != {expected_recall}')

for j,f2j in zip(js['journeys'],f2['journeys']):
    route=[lid for bundle in f2j['bundles'] for lid in bundle['loci']]
    if j.get('route')!=route: problems.append(f"{j.get('journey_id')} route changed from F2")
    if j.get('unit_guide',{}).get('name')!='Dr. Imani Reyes': problems.append(f"{j.get('journey_id')} lost the common guide")
    if len(j.get('premise',''))<180 or len(j.get('mission',''))<140 or len(j.get('stakes',''))<140: problems.append(f"{j.get('journey_id')} continuity brief is too thin")
    if len(j.get('continuity_object',''))<150 or len(j.get('opening_image',''))<150 or len(j.get('ending_payoff',''))<130: problems.append(f"{j.get('journey_id')} continuity object/opening/payoff is underspecified")
    if len(j.get('recurring_scientific_cast',[]))<3: problems.append(f"{j.get('journey_id')} recurring scientific cast is incomplete")
    if len(j.get('narrative_constraints',[]))<12: problems.append(f"{j.get('journey_id')} has too few narrative constraints")
    if j.get('status')!='JOURNEY_BRIEF_LOCKED_F3_NO_POLISHED_STORY_PROSE': problems.append(f"{j.get('journey_id')} journey brief status incorrect")
    for i,lid in enumerate(route):
        expected_next=route[i+1] if i+1<len(route) else None
        if scene_index[lid].get('causal_transition',{}).get('to_locus_id')!=expected_next: problems.append(f'{lid} causal transition points to wrong next locus')
        if len(scene_index[lid].get('causal_transition',{}).get('transition_logic',''))<130: problems.append(f'{lid} causal transition is too terse')

if status.get('status')!='SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED': problems.append(f"unexpected F3 status {status.get('status')}")
if status.get('canonical_lock')!='LOCKED_F1' or status.get('architecture_lock')!='LOCKED_F2' or status.get('scene_brief_lock')!='LOCKED_F3': problems.append('F1/F2/F3 lock state incorrect')
if status.get('student_release') is not False or status.get('preview_release') is not False: problems.append('Unit 5 became student-visible during F3')
if any(status.get(k)!=0 for k in ['journey_count','scene_count','memory_objects','application_challenges']): problems.append('student runtime fields are nonzero during F3')
if (status.get('architecture_journeys'),status.get('architecture_loci'),status.get('scene_briefs'))!=(8,50,50): problems.append('status F3 architecture/brief counts mismatch')
if release.get('student_release') is not False or release.get('polished_story_files')!=0 or release.get('student_runtime_memory_objects')!=0: problems.append('F3 release manifest exposes runtime content')

# Earlier locks must remain byte-identical.
for lock_name in ('content-lock-f1.json','content-lock-f2.json'):
    earlier=read(U5/lock_name)
    entries=earlier.get('protected_files') or [{'path':rel,**meta} for rel,meta in earlier.get('files',{}).items()]
    for item in entries:
        rel=item['path']; p=U5/rel
        if not p.exists(): problems.append(f'{lock_name} protected file missing: {rel}'); continue
        if item.get('bytes') is not None and p.stat().st_size!=item['bytes']: problems.append(f'{lock_name} protected file size changed: {rel}')
        if item.get('sha256') and sha(p)!=item['sha256']: problems.append(f'{lock_name} protected file hash changed: {rel}')

# Released Units 1-4 remain protected.
prot=read(U5/'upstream-u1-u4-protection-f1.json')
if prot.get('protected_file_count')!=216: problems.append('upstream protection manifest no longer contains 216 files')
for item in prot.get('protected_files',[]):
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f"released Units 1-4 file changed: {item['path']}")

if lock.get('lock_status')!='LOCKED_F3' or lock.get('student_release') is not False: problems.append('F3 content lock state incorrect')
for rel,meta in lock.get('files',{}).items():
    p=ROOT/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F3 locked file changed: {rel}')

required=[U5/'briefs'/'journey-briefs-f3.json',U5/'briefs'/'scene-briefs-f3.json',U5/'status-f3.json',U5/'f3-release-manifest.json',U5/'content-lock-f3.json',U5/'audit'/'APBIO_Unit5_F3_Scene_Briefs.xlsx',ROOT/'docs'/'UNIT5_F3_SCENE_BRIEFS.md',ROOT/'docs'/'UNIT5_F3_QA.md',ROOT/'docs'/'UNIT5_F3_RELEASE.md']
for p in required:
    if not p.exists(): problems.append(f'missing required F3 artifact: {p.relative_to(ROOT)}')

# No Unit 5 student runtime at F3.
for forbidden in [U5/'memory-objects.json']:
    if forbidden.exists(): problems.append(f'premature Unit 5 student-runtime artifact exists: {forbidden.relative_to(ROOT)}')
# Later F4 narrative-preview artifacts may coexist after the F3 lock; they remain non-student runtime until finalization.

course=read(ROOT/'content/ap-biology/course.json'); u5=next((u for u in course['units'] if u['unit_id']=='unit-5'),None)
if not u5: problems.append('Unit 5 missing from course registry')
else:
    if u5.get('status')=='STUDENT_READY':
        if u5.get('student_release') is not True or u5.get('preview_release') is not False: problems.append('course registry F5 state invalid after F3')
    elif u5.get('status') not in {'SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW','F4G_JOURNEYS1_7_POLISHED_DEVELOPER_PREVIEW','F4H_JOURNEYS1_8_POLISHED_DEVELOPER_PREVIEW'}: problems.append('course registry Unit 5 F3-compatible status mismatch')
    if u5.get('scene_brief_lock')!='LOCKED_F3' or u5.get('scene_briefs')!=50: problems.append('course registry F3 brief accounting mismatch')
    if u5.get('status')=='SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED' and (u5.get('journey_count')!=0 or u5.get('scene_count')!=0): problems.append('course registry contains narrative scenes before F4')

if problems:
    print('UNIT 5 F3 QA FAIL')
    print('\n'.join(f'- {p}' for p in problems))
    sys.exit(1)
print('UNIT 5 F3 QA PASS')
print(json.dumps(expected_counts,indent=2))
