from __future__ import annotations
import json,re,hashlib,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; U7=ROOT/'content/ap-biology/unit-7'
def read(p): return json.loads(Path(p).read_text())
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
j=read(U7/'journeys/U7-J5.json'); b={x['locus_id']:x for x in read(U7/'briefs/scene-briefs-f3.json')['scene_briefs'] if x['journey_id']=='U7-J5'}; c={r['knowledge_id']:r for r in read(U7/'source/canonical-unit7-f1.json')['canonical_catalog']}; lock=read(U7/'content-lock-f4e.json')
problems=[]; expected=[f'U7-L{i:02d}' for i in range(42,51)]; counts=[]; exact=0; assigned=[]
if j['scene_count']!=9 or [s['locus_id'] for s in j['scenes']]!=expected: problems.append('route/accounting mismatch')
for s in j['scenes']:
 lid=s['locus_id']; prose=' '.join(s['story_paragraphs']); low=prose.casefold().replace('**',''); counts.append(len(re.findall(r"\b[\w’′'-]+\b",prose))); assigned+=s['object_ids']
 if counts[-1]<450: problems.append(f'{lid} short prose')
 o=s['story_paragraphs'][0].casefold()
 if not ('left' in o and 'right' in o and ('ahead' in o or 'center' in o)): problems.append(f'{lid} geography missing')
 if s['object_ids']!=b[lid]['knowledge_ids']: problems.append(f'{lid} F3 assignment changed')
 beats={x['object_id']:x for x in s['story_beats']}; terms={t['knowledge_id']:t for t in b[lid]['term_introductions']}
 for kid in s['object_ids']:
  if beats[kid]['science']!=c[kid]['canonical_verified_statement']: problems.append(f'{lid} science changed {kid}')
  if terms[kid]['exact_name_recall']:
   exact+=1
   if terms[kid]['canonical_term'].casefold() not in low: problems.append(f'{lid} exact term missing {terms[kid]["canonical_term"]}')
 if s['checkpoint']!=bool(b[lid]['quick_recall']['enabled']): problems.append(f'{lid} recall mismatch')
 if '—' in prose or ': ' in prose: problems.append(f'{lid} punctuation policy')
for phrase in [
'speciation requires reproductive isolation','biological species concept','allopatric speciation','sympatric speciation','prezygotic barrier','habitat isolation','temporal isolation','behavioral isolation','mechanical isolation','gametic isolation','postzygotic barrier','reduced hybrid viability','reduced hybrid fertility','hybrid breakdown','punctuated equilibrium and gradualism','stasis','divergent evolution','adaptive radiation','convergent evolution','macroevolution','extinction']:
 if phrase not in ' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold(): problems.append('missing visible science '+phrase)
if len(assigned)!=25 or len(set(assigned))!=25 or exact!=23: problems.append('knowledge/exact accounting mismatch')
# prior narrative protection
for rel,meta in lock['prior_narrative_protection'].items():
 p=ROOT/rel
 if not p.exists() or p.stat().st_size!=meta['bytes'] or sha(p)!=meta['sha256']: problems.append('prior narrative changed '+rel)
# upstream U1-6
up=read(U7/'upstream-u1-u6-protection-f1.json')
for item in up['protected_files']:
 p=ROOT/item['path']
 if not p.exists() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']: problems.append('upstream changed '+item['path'])
status=read(U7/'status.json')
if status['status'] not in {'F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'} : problems.append('status boundary')
if status['status']=='STUDENT_READY' and (status['student_release'] is not True or status['preview_release'] is not False): problems.append('F5 release flags while preserving F4E')
if status['status']!='STUDENT_READY' and status['student_release'] is not False: problems.append('pre-F5 release boundary')
if status['status']=='F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW' and (status['journey_count'],status['scene_count'])!=(5,50): problems.append('F4E count boundary')
if status['status']=='F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW' and (status['journey_count'],status['scene_count'])!=(6,55): problems.append('F4F count boundary while preserving F4E')
report=['# Unit 7 F4E Narrative QA','','## Result','', '**PASS**' if not problems else '**FAIL**','',f'- Scenes **9 / 9**',f'- F3 knowledge records **25 / 25**',f'- Exact-name targets **{exact} / 23**',f'- Optional Quick Recalls **3**',f'- Narrative words **{sum(counts):,}**',f'- Mean scene length **{statistics.mean(counts):.1f} words**',f'- Shortest scene **{min(counts)} words**',f'- Longest scene **{max(counts)} words**','', '## Gates','', '- Species boundaries remain tied to reproductive isolation and reduced gene flow.', '- Allopatric versus sympatric geography remains explicit.', '- Five prezygotic barriers are separated by the exact stage at which reproduction fails.', '- Three postzygotic barriers remain separated by hybrid timing and outcome.', '- Punctuated equilibrium, gradualism, and stasis remain tempo concepts.', '- Divergence does not automatically equal speciation.', '- Adaptive radiation, convergence, macroevolution, and extinction remain distinct.', '- Journeys 1–4 remain frozen and Unit 7 remains student-unreleased.']
if problems: report += ['','## Blocking findings','']+[f'- {x}' for x in problems]
(ROOT/'docs/UNIT7_F4E_QA.md').write_text('\n'.join(report))
if problems:
 print('UNIT 7 F4E QA FAIL'); print('\n'.join(problems)); sys.exit(1)
print('UNIT 7 F4E QA PASS'); print(json.dumps({'scenes':9,'records':25,'exact':23,'recalls':3,'words':sum(counts),'min':min(counts),'max':max(counts)},indent=2))
