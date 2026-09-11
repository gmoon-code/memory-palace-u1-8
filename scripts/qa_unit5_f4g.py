from __future__ import annotations
import json,hashlib,re,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; U5=ROOT/'content'/'ap-biology'/'unit-5'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
problems=[]
j=read(U5/'journeys'/'U5-J7.json'); lock=read(U5/'content-lock-f4g.json'); f3=read(U5/'briefs'/'scene-briefs-f3.json')['scene_briefs']; canon={r['knowledge_id']:r for r in read(U5/'source'/'canonical-unit5-f1.json')['canonical_catalog']}; B={b['locus_id']:b for b in f3 if b['journey_id']=='U5-J7'}
if j.get('student_release')!='DEVELOPER_PREVIEW_F4G': problems.append('Journey 7 preview boundary wrong')
if len(j.get('scenes',[]))!=6: problems.append('Journey 7 scene count wrong')
assigned=[]; counts=[]
banned=re.compile(r'\b(?:ppt|powerpoint|ced|campbell|source lock|canonical catalog|slide deck|teacher source)\b',re.I)
for s in j['scenes']:
    b=B.get(s['locus_id'])
    if not b: problems.append(f"unknown locus {s['locus_id']}"); continue
    assigned+=s['object_ids']; prose=' '.join(s['story_paragraphs']); visible=prose.casefold().replace('**',''); n=len(re.findall(r"\b[\w’'-]+\b",prose)); counts.append(n)
    if n<600: problems.append(f"{s['locus_id']} too short {n}")
    if len(s['story_paragraphs'])<6: problems.append(f"{s['locus_id']} too few paragraphs")
    if not all(x in s['story_open'].casefold() for x in ('left','ahead','right')): problems.append(f"{s['locus_id']} opening geography unclear")
    names={c['name'] for c in s['cast']}
    for required in ('Dr. Imani Reyes','Two-locus chromosome railcar','Recombination meter','Gold mapping ledger'):
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
if len(set(assigned))!=10 or len(assigned)!=10: problems.append(f'Journey 7 record accounting wrong {len(assigned)} total {len(set(assigned))} unique')
if sum(1 for s in j['scenes'] if s['checkpoint'])!=2: problems.append('Journey 7 recall count wrong')
if statistics.mean(counts)<620: problems.append(f'Average scene prose below target {statistics.mean(counts):.1f}')
full=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**','')
required=[
 'genetic linkage','linked genes tend to be inherited together','can be separated by recombination','genetic recombination','crossing over can separate linked alleles','nonsister chromatids','parental type','recombinant type','original parental arrangement','recombination frequency','recombinant outcomes divided by the total','not a tape measure','linkage map','map unit (centimorgan)','one percent recombination','one centimorgan','multiple crossovers','fifty-percent recombination ceiling','cannot distinguish genes on different chromosomes from very distant loci on the same chromosome'
]
for p in required:
    if p not in full: problems.append(f'high-risk mapping guard absent from prose {p}')
# protect predecessor journeys
for stage,jid in [('f4a',1),('f4b',2),('f4c',3),('f4d',4),('f4e',5),('f4f',6)]:
    old=read(U5/f'content-lock-{stage}.json'); rel=f'journeys/U5-J{jid}.json'; meta=old['files'][rel]; p=U5/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'predecessor journey changed {rel}')
# F1-F3 and U1-U4 protection
up=read(U5/'upstream-u1-u4-protection-f1.json')
if up.get('protected_file_count')!=216: problems.append('upstream protection count changed')
for item in up.get('protected_files',[]):
    p=ROOT/item['path']
    if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append(f"Units 1-4 protected file changed {item['path']}")
if lock.get('lock_status')!='LOCKED_F4G_J7' or lock.get('student_release') is not False or lock.get('preview_release') is not True: problems.append('F4G content lock boundary wrong')
for rel,meta in lock['files'].items():
    p=U5/rel
    if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append(f'F4G lock mismatch {rel}')
if not (U5/'f5-release-manifest.json').exists():
    for forbidden in [U5/'memory-objects.json',U5/'application-lab.json',U5/'review-manifest-f5.json',U5/'finalization-f5.json']:
        if forbidden.exists(): problems.append(f'premature runtime artifact {forbidden.name}')
course=read(ROOT/'content/ap-biology/course.json'); cu5=next(u for u in course['units'] if u['unit_id']=='unit-5')
if cu5.get('status')=='STUDENT_READY':
    if cu5.get('journey_count')!=8 or cu5.get('scene_count')!=50 or cu5.get('student_release') is not True: problems.append('course F5 release state invalid after F4G')
elif (cu5.get('status'),cu5.get('journey_count'),cu5.get('scene_count')) not in {('F4G_JOURNEYS1_7_POLISHED_DEVELOPER_PREVIEW',7,43),('F4H_JOURNEYS1_8_POLISHED_DEVELOPER_PREVIEW',8,50)} or cu5.get('student_release') is not False: problems.append('course F4G-or-later state mismatch')
report=['# Unit 5 F4G Narrative QA','','## Result','', '**PASS**' if not problems else '**FAIL**','','## Accounting','',f'- Journey 7 scenes: **6 / 6**',f'- Locked Journey 7 records: **{len(set(assigned))} / 10**','- Optional first-exposure recalls: **2**',f'- Journey 7 narrative words: **{sum(counts)}**',f'- Average scene length: **{statistics.mean(counts):.1f} words**',f'- Shortest scene: **{min(counts)} words**','','## Scientific and narrative gates','','- One two-locus chromosome railcar persists through all six scenes.','- Genetic linkage is separated from permanent inseparability.','- Crossing over is tied to nonsister chromatids and tracked interval position.','- Parental and recombinant classes are defined from the starting arrangement before arithmetic.','- Recombination frequency is separated from literal physical DNA distance.','- Centimorgans are preserved as genetic-map units.','- Multiple-crossover undercounting over longer intervals is explicit.','- The 50 percent ceiling and its chromosome-arrangement ambiguity are explicit.','- F3 recall placement and wording are unchanged.','- Student prose contains no source-management language, colons, em dashes, or prohibited contrast phrases.','- Unit 5 remains developer preview only.','']
if problems: report+=['## Blocking findings','']+[f'- {x}' for x in problems]+['']
(ROOT/'docs'/'UNIT5_F4G_QA.md').write_text('\n'.join(report),encoding='utf-8')
if problems:
    print('UNIT 5 F4G QA FAIL'); print('\n'.join('- '+x for x in problems)); sys.exit(1)
print('UNIT 5 F4G QA PASS')
print(json.dumps({'journey':'U5-J7','scenes':6,'records':10,'optional_recalls':2,'story_words':sum(counts),'average_scene_words':round(statistics.mean(counts),1),'min_scene_words':min(counts),'student_release':False,'preview_release':True},indent=2))
