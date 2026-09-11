from pathlib import Path
import json, hashlib, sys
ROOT=Path(__file__).resolve().parents[1]; U8=ROOT/'content/ap-biology/unit-8'
read=lambda p: json.loads(Path(p).read_text(encoding='utf-8'))
sha=lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
problems=[]
sc=read(U8/'briefs/scene-briefs-f3.json'); jb=read(U8/'briefs/journey-briefs-f3.json'); arch=read(U8/'architecture/palace-architecture-f2.json'); cls=read(U8/'architecture/learning-classification-f2.json'); canon={r['Knowledge ID']:r for r in read(U8/'canonical-catalog.json')}
if sc['counts']!={'journeys':8,'scene_briefs':58,'palace_managed_records':211,'term_introductions':211,'optional_first_exposure_recalls':18}: problems.append('F3 counts mismatch')
if len(sc['scene_briefs'])!=58 or len(jb['journeys'])!=8: problems.append('journey/scene count mismatch')
assigned=[k for b in sc['scene_briefs'] for k in b['knowledge_ids']]
if len(assigned)!=211 or len(set(assigned))!=211: problems.append('palace record assignment not exact')
expected=[r['knowledge_id'] for r in cls['records'] if r['destination'] in {'PALACE_PRIMARY_LOCUS','PALACE_EMBEDDED'}]
if set(assigned)!=set(expected): problems.append('F3 assigned record set differs from F2 palace set')
for b,l in zip(sc['scene_briefs'],arch['loci']):
    if b['locus_id']!=l['locus_id'] or b['primary_knowledge_id']!=l['primary_knowledge_id']: problems.append(f"locus identity mismatch {l['locus_id']}")
    if b['knowledge_ids']!=[l['primary_knowledge_id']]+l['embedded_knowledge_ids']: problems.append(f"knowledge order mismatch {l['locus_id']}")
    if b['visual_spec']['visual_mode']!=l['scientific_visual'] or b['f2_spatial_anchor']!=l['spatial_anchor']: problems.append(f"F2 visual/anchor mismatch {l['locus_id']}")
    if len(b['stable_cast'])!=3 or len(b['science_bearing_action']['during'])!=3: problems.append(f"brief structure mismatch {l['locus_id']}")
    if b['story_prose_status']!='PROHIBITED_UNTIL_F3_BRIEF_QA_PASS': problems.append(f"story gate missing {l['locus_id']}")
    for t in b['term_introductions']:
        r=canon[t['knowledge_id']]
        if t['canonical_term']!=r['Canonical Label'] or t['canonical_science']!=r['Canonical Verified Statement']: problems.append(f"canonical science changed {t['knowledge_id']}")
per={j['journey_id']:0 for j in arch['journeys']}
for b in sc['scene_briefs']:
    if b['quick_recall']['enabled']: per[b['journey_id']]+=1
if per!={'U8-J1':2,'U8-J2':3,'U8-J3':2,'U8-J4':2,'U8-J5':2,'U8-J6':3,'U8-J7':2,'U8-J8':2}: problems.append(f'quick recall distribution wrong {per}')
lock=read(U8/'content-lock-f3.json')
for rel,h in lock['f1_protected_hashes'].items():
    if sha(ROOT/rel)!=h: problems.append(f'F1 protected hash changed {rel}')
for rel,h in lock['f2_protected_hashes'].items():
    if sha(ROOT/rel)!=h: problems.append(f'F2 protected hash changed {rel}')
s=read(U8/'status-f3.json'); r=read(U8/'f3-release-manifest.json')
if s['student_release'] or s['journey_count'] or s['scene_count'] or s['memory_objects'] or s['application_challenges']: problems.append('student runtime boundary violated')
if r['polished_story_files']!=0 or r['student_runtime_memory_objects']!=0: problems.append('release boundary violated')
course=read(ROOT/'content/ap-biology/course.json'); e=next(x for x in course['units'] if x['unit_id']=='unit-8')
is_later_f5 = (
    e.get('status') == 'STUDENT_READY'
    and e.get('pipeline_stage') in {'UNIT8_FINALIZED_F5','UNIT8_CLASSROOM_BROWSER_VALIDATED_F6'}
    and e.get('student_release') is True
    and e.get('preview_release') is False
)
if is_later_f5:
    if e.get('journey_count') != 8 or e.get('scene_count') != 58 or e.get('runtime_memory_objects') != 211 or e.get('application_challenges') != 13:
        problems.append('course registry Unit 8 later runtime counts do not preserve the finalized release')
    if e.get('architecture_journeys') != 8 or e.get('architecture_loci') != 58 or e.get('scene_briefs') != 58 or e.get('scene_brief_lock') != 'LOCKED_F3':
        problems.append('course registry Unit 8 later release no longer preserves the locked F3 architecture/brief layer')
else:
    if e.get('student_release') is not False or e.get('architecture_journeys')!=8 or e.get('architecture_loci')!=58 or e.get('scene_briefs')!=58:
        problems.append('course registry Unit 8 no longer preserves the F3 architecture/brief boundary')
for n in range(1,8):
    x=next((q for q in course['units'] if q['unit_id']==f'unit-{n}'),None)
    if not x or x.get('status')!='STUDENT_READY' or ('student_release' in x and x.get('student_release') is not True): problems.append(f'upstream unit {n} release changed')
for p in ROOT.rglob('*.pdf'): problems.append(f'forbidden PDF in repo {p.relative_to(ROOT)}')
req=[U8/'briefs/journey-briefs-f3.json',U8/'briefs/scene-briefs-f3.json',U8/'status-f3.json',U8/'content-lock-f3.json',U8/'f3-release-manifest.json',ROOT/'docs/UNIT8_F3_SCENE_BRIEFS.md',ROOT/'docs/UNIT8_F3_QA.md',ROOT/'docs/UNIT8_F3_RELEASE.md',U8/'audit/APBIO_Unit8_F3_Scene_Briefs.xlsx']
for p in req:
    if not p.exists(): problems.append(f'missing F3 artifact {p.relative_to(ROOT)}')
if problems:
    print('UNIT 8 F3 QA FAIL')
    for p in problems: print('-',p)
    sys.exit(1)
print('UNIT 8 F3 QA PASS')
print(json.dumps(sc['counts'],indent=2))
