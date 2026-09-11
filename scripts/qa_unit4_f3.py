from __future__ import annotations
import json, hashlib, re, sys
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content/ap-biology/unit-4'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

problems=[]
src=read(U4/'source/canonical-unit4-f1.json'); recs={r['knowledge_id']:r for r in src['canonical_catalog']}
f2=read(U4/'architecture/palace-architecture-f2.json')
cls=read(U4/'architecture/learning-classification-f2.json'); class_by_id={r['knowledge_id']:r for r in cls['records']}
js=read(U4/'briefs/journey-briefs-f3.json'); sb=read(U4/'briefs/scene-briefs-f3.json')
status=read(U4/'status-f3.json'); release=read(U4/'f3-release-manifest.json'); lock=read(U4/'content-lock-f3.json')

if len(recs)!=180: problems.append(f'canonical count {len(recs)} != 180')
expected_counts={'journeys':7,'scene_briefs':51,'palace_managed_records':162,'term_introductions':162,'optional_first_exposure_recalls':18}
if sb.get('counts')!=expected_counts: problems.append(f"scene-brief counts {sb.get('counts')} != {expected_counts}")
if js.get('journey_count')!=7 or len(js.get('journeys',[]))!=7: problems.append('journey brief count is not 7')
if len(sb.get('scene_briefs',[]))!=51: problems.append('scene brief count is not 51')

f2_lids=[l['locus_id'] for l in f2['loci']]
f3_lids=[b['locus_id'] for b in sb['scene_briefs']]
if f2_lids!=f3_lids: problems.append('F3 locus order/coverage differs from F2 architecture')

prohibited=('ppt','college board','the packet','source slide','teacher test','the ced states','campbell says','assessment item')
assigned=[]; recalls=Counter(); scene_index={}
for b,l in zip(sb['scene_briefs'],f2['loci']):
    lid=b.get('locus_id'); scene_index[lid]=b
    if b.get('journey_id')!=l.get('journey_id') or b.get('bundle_id')!=l.get('bundle_id'): problems.append(f'{lid} journey/bundle mismatch')
    if b.get('micro_anchor')!=l.get('micro_anchor'): problems.append(f'{lid} micro-anchor changed from F2')
    if b.get('primary_knowledge_id')!=l.get('primary_knowledge_id'): problems.append(f'{lid} primary record changed from F2')
    if b.get('knowledge_ids')!=l.get('knowledge_ids'): problems.append(f'{lid} knowledge assignment changed from F2')
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
            if len(c.get('visual_identity',''))<80: problems.append(f"{lid} {c.get('position')} visual identity is underspecified")
            if len(c.get('job_in_scene',''))<80: problems.append(f"{lid} {c.get('position')} job is underspecified")
    act=b.get('science_bearing_action',{})
    if len(act.get('before',''))<160: problems.append(f'{lid} before-state is underspecified')
    if len(act.get('trigger',''))<90: problems.append(f'{lid} trigger is underspecified')
    if len(act.get('during',[]))<3: problems.append(f'{lid} has fewer than three action steps')
    for n,x in enumerate(act.get('during',[]),1):
        if len(x)<120: problems.append(f'{lid} action step {n} is too terse')
    if len(act.get('after',''))<160: problems.append(f'{lid} after-state is underspecified')
    terms=b.get('term_introductions',[])
    if len(terms)!=len(l['knowledge_ids']): problems.append(f'{lid} term-introduction count differs from knowledge count')
    if [t.get('knowledge_id') for t in terms]!=l['knowledge_ids']: problems.append(f'{lid} term-introduction order/IDs differ from F2')
    for t in terms:
        kid=t.get('knowledge_id'); r=recs[kid]; c=class_by_id[kid]
        if t.get('canonical_term')!=r['canonical_label']: problems.append(f'{lid}/{kid} canonical label changed')
        if t.get('canonical_science')!=r['canonical_verified_statement']: problems.append(f'{lid}/{kid} canonical science changed')
        if t.get('exact_name_recall')!=r.get('exact_name_recall'): problems.append(f'{lid}/{kid} exact-name state changed')
        if t.get('name_support')!=c.get('name_support'): problems.append(f'{lid}/{kid} name-support class changed')
        if t.get('spelling_policy')!=c.get('spelling_policy'): problems.append(f'{lid}/{kid} spelling policy changed')
        if not t.get('insertion_rule') or not t.get('name_support_rule'): problems.append(f'{lid}/{kid} lacks authoring rules')
    visual=b.get('visual_spec',{})
    if visual.get('conventional_scientific_visual_required') is not True: problems.append(f'{lid} does not require conventional scientific visual')
    if visual.get('visual_mode')!=l.get('visual_mode'): problems.append(f'{lid} visual mode changed from F2')
    if len(visual.get('must_show',[]))<6: problems.append(f'{lid} visual must-show list is too thin')
    if not b.get('misconception_guards'): problems.append(f'{lid} lacks misconception/discrimination guards')
    if not b.get('exit_memory',{}).get('one_sentence_model') or len(b.get('exit_memory',{}).get('redraw_test',''))<80: problems.append(f'{lid} lacks a usable exit-memory reconstruction test')
    if b.get('story_prose_status')!='PROHIBITED_UNTIL_F3_BRIEF_QA_PASS': problems.append(f'{lid} story prose was prematurely enabled')
    if b.get('brief_status')!='LOCKED_F3_SCENE_BRIEF': problems.append(f'{lid} brief status is not LOCKED_F3_SCENE_BRIEF')
    candidate=' '.join([b.get('orientation_sentence',''),act.get('before',''),act.get('trigger',''),act.get('after',''),*act.get('during',[]),b.get('exit_memory',{}).get('one_sentence_model',''),b.get('causal_transition',{}).get('transition_logic','')]).lower()
    bad=[x for x in prohibited if x in candidate]
    if bad: problems.append(f'{lid} future-prose fields expose source-management language {bad}')
    if b.get('quick_recall',{}).get('enabled'):
        recalls[b['journey_id']]+=1
        if not b['quick_recall'].get('candidate_prompt') or not b['quick_recall'].get('answer'): problems.append(f'{lid} enabled recall is incomplete')
    assigned += b['knowledge_ids']

if len(assigned)!=162 or len(set(assigned))!=162: problems.append(f'F3 assignment is {len(assigned)} refs / {len(set(assigned))} unique, expected 162/162')
palace={k for l in f2['loci'] for k in l['knowledge_ids']}
if set(assigned)!=palace: problems.append('F3 palace records do not equal the locked F2 palace partition')
expected_recall={'U4-J1':2,'U4-J2':3,'U4-J3':3,'U4-J4':2,'U4-J5':3,'U4-J6':2,'U4-J7':3}
if dict(recalls)!=expected_recall: problems.append(f'recall distribution {dict(recalls)} != {expected_recall}')

for j,f2j in zip(js['journeys'],f2['journeys']):
    route=[lid for bundle in f2j['bundles'] for lid in bundle['loci']]
    if j.get('route')!=route: problems.append(f"{j.get('journey_id')} route changed from F2")
    if j.get('unit_guide',{}).get('name')!='Dr. Mira Chen': problems.append(f"{j.get('journey_id')} lost the common guide")
    if len(j.get('premise',''))<150 or len(j.get('mission',''))<110 or len(j.get('stakes',''))<110: problems.append(f"{j.get('journey_id')} continuity brief is too thin")
    if len(j.get('continuity_object',''))<120 or len(j.get('opening_image',''))<120 or len(j.get('ending_payoff',''))<110: problems.append(f"{j.get('journey_id')} continuity object/opening/payoff is underspecified")
    if len(j.get('recurring_scientific_cast',[]))<3: problems.append(f"{j.get('journey_id')} recurring scientific cast is incomplete")
    if len(j.get('narrative_constraints',[]))<10: problems.append(f"{j.get('journey_id')} has too few narrative constraints")
    if j.get('status')!='JOURNEY_BRIEF_LOCKED_F3_NO_POLISHED_STORY_PROSE': problems.append(f"{j.get('journey_id')} journey brief status incorrect")
    for i,lid in enumerate(route):
        expected_next=route[i+1] if i+1<len(route) else None
        if scene_index[lid].get('causal_transition',{}).get('to_locus_id')!=expected_next: problems.append(f'{lid} causal transition points to wrong next locus')
        if len(scene_index[lid].get('causal_transition',{}).get('transition_logic',''))<110: problems.append(f'{lid} causal transition is too terse')

if status.get('status')!='SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED': problems.append(f"unexpected F3 status {status.get('status')}")
if status.get('canonical_lock')!='LOCKED_F1' or status.get('architecture_lock')!='LOCKED_F2' or status.get('scene_brief_lock')!='LOCKED_F3': problems.append('F1/F2/F3 lock state incorrect')
if status.get('student_release') is not False or status.get('preview_release') is not False: problems.append('Unit 4 became student-visible during F3')
if any(status.get(k)!=0 for k in ['journey_count','scene_count','memory_objects','application_challenges']): problems.append('student runtime fields are nonzero during F3')
if (status.get('architecture_journeys'),status.get('architecture_loci'),status.get('scene_briefs'))!=(7,51,51): problems.append('status F3 architecture/brief counts mismatch')
if release.get('student_release') is not False or release.get('polished_story_files')!=0 or release.get('student_runtime_memory_objects')!=0: problems.append('F3 release manifest exposes runtime content')

# Protected earlier locks must still verify.
for lock_name in ('content-lock-f1.json','content-lock-f2.json'):
    earlier=read(U4/lock_name)
    entries=earlier.get('protected_files') or [{'path':rel,**meta} for rel,meta in earlier.get('files',{}).items()]
    for item in entries:
        rel=item['path']; p=U4/rel
        if not p.exists(): problems.append(f'{lock_name} protected file missing: {rel}'); continue
        if item.get('bytes') is not None and p.stat().st_size!=item['bytes']: problems.append(f'{lock_name} protected file size changed: {rel}')
        if item.get('sha256') and sha(p)!=item['sha256']: problems.append(f'{lock_name} protected file hash changed: {rel}')

if lock.get('lock_status')!='LOCKED_F3' or lock.get('student_release') is not False: problems.append('F3 content lock state incorrect')
for rel,meta in lock.get('files',{}).items():
    p=ROOT/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F3 locked file changed: {rel}')

required=[U4/'briefs'/'journey-briefs-f3.json',U4/'briefs'/'scene-briefs-f3.json',U4/'status-f3.json',U4/'f3-release-manifest.json',U4/'content-lock-f3.json',U4/'audit'/'APBIO_Unit4_F3_Scene_Briefs.xlsx',ROOT/'docs'/'UNIT4_F3_SCENE_BRIEFS.md',ROOT/'docs'/'UNIT4_F3_QA.md',ROOT/'docs'/'UNIT4_F3_RELEASE.md']
for p in required:
    if not p.exists(): problems.append(f'missing required F3 artifact: {p.relative_to(ROOT)}')

# F3's immutable release manifest proves that F3 itself created no polished story/runtime content.
# Later F4 preview files may coexist in a mainline checkout when this historical gate is rerun.
for forbidden in [U4/'memory-objects.json']:
    if forbidden.exists(): problems.append(f'premature Unit 4 student-runtime artifact exists: {forbidden.relative_to(ROOT)}')

course=read(ROOT/'content/ap-biology/course.json')
u4=next((u for u in course['units'] if u['unit_id']=='unit-4'),None)
if not u4: problems.append('Unit 4 missing from course registry')
else:
    if u4.get('status')!='SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED': problems.append('course registry Unit 4 F3 status mismatch')
    if u4.get('scene_brief_lock')!='LOCKED_F3' or u4.get('scene_briefs')!=51: problems.append('course registry F3 brief accounting mismatch')
    if u4.get('student_release') is not False or u4.get('journey_count')!=0 or u4.get('scene_count')!=0: problems.append('course registry released Unit 4 runtime content')

if problems:
    print('UNIT 4 F3 QA FAIL')
    print('\n'.join(f'- {p}' for p in problems))
    sys.exit(1)
print('UNIT 4 F3 QA PASS')
print(json.dumps(expected_counts,indent=2))
