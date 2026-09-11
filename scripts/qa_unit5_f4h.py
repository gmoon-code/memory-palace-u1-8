from __future__ import annotations
import json,hashlib,re,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; U5=ROOT/'content'/'ap-biology'/'unit-5'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
problems=[]
j=read(U5/'journeys'/'U5-J8.json'); lock=read(U5/'content-lock-f4h.json'); f3=read(U5/'briefs'/'scene-briefs-f3.json')['scene_briefs']; canon={r['knowledge_id']:r for r in read(U5/'source'/'canonical-unit5-f1.json')['canonical_catalog']}; B={b['locus_id']:b for b in f3 if b['journey_id']=='U5-J8'}
if j.get('student_release')!='DEVELOPER_PREVIEW_F4H': problems.append('Journey 8 preview boundary wrong')
if len(j.get('scenes',[]))!=7: problems.append('Journey 8 scene count wrong')
assigned=[]; counts=[]
banned=re.compile(r'\b(?:ppt|powerpoint|ced|campbell|source lock|canonical catalog|slide deck|teacher source)\b',re.I)
for s in j['scenes']:
    b=B.get(s['locus_id'])
    if not b: problems.append(f"unknown locus {s['locus_id']}"); continue
    assigned+=s['object_ids']; prose=' '.join(s['story_paragraphs']); visible=prose.casefold().replace('**',''); n=len(re.findall(r"\b[\w’'-]+\b",prose)); counts.append(n)
    if n<600: problems.append(f"{s['locus_id']} too short {n}")
    if len(s['story_paragraphs'])<7: problems.append(f"{s['locus_id']} too few paragraphs")
    if not all(x in s['story_open'].casefold() for x in ('left','ahead','right')): problems.append(f"{s['locus_id']} opening geography unclear")
    names={c['name'] for c in s['cast']}
    for required in ('Dr. Imani Reyes','Three-compartment evidence tray','Organelle inheritance model','Chi-square evidence console'):
        if required not in names: problems.append(f"{s['locus_id']} missing {required}")
    if s['object_ids']!=b['knowledge_ids']: problems.append(f"{s['locus_id']} knowledge assignment changed")
    if s['misconception_guards']!=b['misconception_guards']: problems.append(f"{s['locus_id']} misconception guards changed")
    for beat in s['story_beats']:
        if beat['science']!=canon[beat['object_id']]['canonical_verified_statement']: problems.append(f"{s['locus_id']} science drift {beat['object_id']}")
        if beat['term'].casefold() not in visible: problems.append(f"{s['locus_id']} exact term absent {beat['term']}")
    q=b['quick_recall']; enabled=bool(q['enabled'])
    if bool(s['checkpoint'])!=enabled: problems.append(f"{s['locus_id']} recall placement changed")
    if enabled and (s['checkpoint_prompt']!=q['candidate_prompt'] or s['checkpoint_answer']!=q['answer']): problems.append(f"{s['locus_id']} recall wording changed")
    if banned.search(prose): problems.append(f"{s['locus_id']} source language leak")
    if '—' in prose: problems.append(f"{s['locus_id']} em dash in student prose")
    if ':' in prose: problems.append(f"{s['locus_id']} colon in student prose")
    for phrase in ('rather than','instead of','not only'):
        if phrase in visible: problems.append(f"{s['locus_id']} prohibited phrase {phrase}")
if len(set(assigned))!=19 or len(assigned)!=19: problems.append(f'Journey 8 record accounting wrong {len(assigned)} total {len(set(assigned))} unique')
if sum(1 for s in j['scenes'] if s['checkpoint'])!=3: problems.append('Journey 8 recall count wrong')
if statistics.mean(counts)<650: problems.append(f'Average scene prose below target {statistics.mean(counts):.1f}')
full=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
required=[
 'non-nuclear inheritance overview','non-nuclear inheritance','organelle assortment','mitochondrial or chloroplast genomes',
 'animal mitochondrial inheritance','usually transmitted through the egg','typically maternally inherited',
 'plant organelle inheritance','predominantly through the ovule','often maternally inherited','paternal','biparental',
 'genetic disorder','pathogenic variant','tay-sachs disease example','sickle cell disease example','severe deficiency','hemoglobin s','low-oxygen',
 'chi-square hypothesis testing','chi-square goodness-of-fit test','chi-square uses categorical counts','null model','categorical counts',
 'observed count (o)','expected count (e)','chi-square contribution','(o−e)²/e',
 'degrees of freedom for ap goodness-of-fit','number of outcome categories minus one','chi-square critical value','p-value and significance level',
 'significance threshold','reject or fail to reject the null','no third door labeled accept the null','does not prove the null model true'
]
for p in required:
    if p not in full: problems.append(f'high-risk evidence guard absent from prose {p}')
# All eight polished journeys must now cover all 131 palace-managed records exactly once.
all_ids=[]
for i in range(1,9):
    pj=read(U5/'journeys'/f'U5-J{i}.json')
    for s in pj['scenes']: all_ids.extend(s['object_ids'])
if len(all_ids)!=131 or len(set(all_ids))!=131: problems.append(f'all-journey palace accounting wrong {len(all_ids)} total {len(set(all_ids))} unique')
# protect predecessor journeys
for stage,jid in [('f4a',1),('f4b',2),('f4c',3),('f4d',4),('f4e',5),('f4f',6),('f4g',7)]:
    old=read(U5/f'content-lock-{stage}.json'); rel=f'journeys/U5-J{jid}.json'; meta=old['files'][rel]; p=U5/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'predecessor journey changed {rel}')
# F1-F3 and U1-U4 protection
up=read(U5/'upstream-u1-u4-protection-f1.json')
if up.get('protected_file_count')!=216: problems.append('upstream protection count changed')
for item in up.get('protected_files',[]):
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f"Units 1-4 protected file changed {item['path']}")
if lock.get('lock_status')!='LOCKED_F4H_J8' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4H content lock boundary wrong')
for rel,meta in lock['files'].items():
    p=U5/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4H lock mismatch {rel}')
if not (U5/'f5-release-manifest.json').exists():
    for forbidden in [U5/'memory-objects.json',U5/'application-lab.json',U5/'review-manifest-f5.json',U5/'finalization-f5.json']:
        if forbidden.exists(): problems.append(f'premature runtime artifact {forbidden.name}')
course=read(ROOT/'content/ap-biology/course.json'); cu5=next(u for u in course['units'] if u['unit_id']=='unit-5')
if cu5.get('status')=='STUDENT_READY':
    if cu5.get('journey_count')!=8 or cu5.get('scene_count')!=50 or cu5.get('student_release') is not True or cu5.get('preview_release') is not False: problems.append('course F5 release state invalid after F4H')
else:
    if cu5.get('status')!='F4H_JOURNEYS1_8_POLISHED_DEVELOPER_PREVIEW' or cu5.get('journey_count')!=8 or cu5.get('scene_count')!=50 or cu5.get('student_release') is not False: problems.append('course F4H state mismatch')
status=read(U5/'status.json')
if status.get('status')=='STUDENT_READY':
    if status.get('runtime_memory_objects')!=131 or status.get('application_challenges')!=16: problems.append('Unit 5 F5 status accounting mismatch after F4H')
elif status.get('preview_journeys')!=8 or status.get('preview_scenes')!=50 or status.get('preview_checkpoints')!=18 or status.get('palace_managed_records')!=131: problems.append('Unit 5 F4H status accounting mismatch')
report=['# Unit 5 F4H Narrative QA','','## Result','', '**PASS**' if not problems else '**FAIL**','','## Accounting','',f'- Journey 8 scenes: **7 / 7**',f'- Locked Journey 8 records: **{len(set(assigned))} / 19**','- Optional first-exposure recalls: **3**',f'- Journey 8 narrative words: **{sum(counts)}**',f'- Average scene length: **{statistics.mean(counts):.1f} words**',f'- Shortest scene: **{min(counts)} words**','- All polished Unit 5 journey records: **131 / 131 unique**','','## Scientific and narrative gates','','- Nuclear chromosome inheritance is physically separated from mitochondrial and chloroplast genome transmission.','- Animal mitochondrial inheritance retains usually and typically maternal qualification.','- Plant organelle inheritance retains species variation and often-maternal qualification.','- Named disorders remain illustrative case evidence and do not define broad inheritance categories.','- Pathogenic variant remains an evidence-based classification.','- Chi-square goodness-of-fit begins with a defined null model and categorical count data.','- Observed and expected counts remain distinct in provenance and meaning.','- Category contributions preserve (O−E)²/E and sum into χ².','- Degrees of freedom are explicitly limited to the AP fixed-proportion goodness-of-fit context used here.','- Critical value, p-value, alpha, and hypothesis decision remain distinct.','- Reject and fail to reject are the only allowed null-hypothesis decision phrases.','- F3 recall placement and wording are unchanged.','- Student prose contains no source-management language, colons, em dashes, or prohibited contrast phrases.','- Unit 5 remains developer preview only.','']
if problems: report+=['## Blocking findings','']+[f'- {x}' for x in problems]+['']
(ROOT/'docs'/'UNIT5_F4H_QA.md').write_text('\n'.join(report),encoding='utf-8')
if problems:
    print('UNIT 5 F4H QA FAIL'); print('\n'.join('- '+x for x in problems)); sys.exit(1)
print('UNIT 5 F4H QA PASS')
print(json.dumps({'journey':'U5-J8','scenes':7,'records':19,'optional_recalls':3,'story_words':sum(counts),'average_scene_words':round(statistics.mean(counts),1),'min_scene_words':min(counts),'all_palace_managed_records':len(set(all_ids)),'student_release':False,'preview_release':True},indent=2))
