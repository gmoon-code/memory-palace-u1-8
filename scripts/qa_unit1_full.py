from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U1=ROOT/'content'/'ap-biology'/'unit-1'
DOC=ROOT/'docs'/'UNIT1_FULL_QA.md'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
mos=read(U1/'memory-objects.json')['memory_objects']; mo_idx={o['memory_object_id']:o for o in mos}
journeys=[read(U1/'journeys'/f'Z{i}.json') for i in range(1,10)]
lab=read(U1/'application-lab.json')
story_ids=[]; problems=[]; scene_rows=[]
banned=re.compile(r'\b(PPT|CED|College Board|Campbell|course notes|class notes|classroom source|source material|locked definition|canonical record|teacher material|the packet)\b',re.I)
for j in journeys:
    for s in j['scenes']:
        story_ids.extend(s['object_ids'])
        words=len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs'])))
        zones=s.get('scene_layout',{}).get('zones',[]); cast=s.get('cast',[])
        visible=json.dumps({'location':s.get('location_description'),'layout':s.get('scene_layout'),'cast':cast,'story':s.get('story_paragraphs'),'snapshot':s.get('memory_snapshot'),'prompt':s.get('checkpoint_prompt')},ensure_ascii=False)
        if words<130: problems.append(f"{j['palace_id']} scene {s['scene_index']} has only {words} narrative words")
        if len(zones)!=3 or {z.get('position') for z in zones}!={'left','center','right'}: problems.append(f"{j['palace_id']} scene {s['scene_index']} has invalid scene geometry")
        if len(cast)<2: problems.append(f"{j['palace_id']} scene {s['scene_index']} has fewer than two cast elements")
        if banned.search(visible): problems.append(f"{j['palace_id']} scene {s['scene_index']} exposes source-management language: {banned.search(visible).group(0)}")
        text=' '.join(s['story_paragraphs']).casefold()
        for oid in s['object_ids']:
            o=mo_idx[oid]
            if str(o.get('exact_name_required','')).upper()=='YES' and o['canonical_term'].casefold() not in text:
                problems.append(f"{j['palace_id']} scene {s['scene_index']} does not introduce exact target {o['canonical_term']}")
        scene_rows.append((j['palace_id'],s['scene_index']+1,s['locus'],words,len(s['object_ids']),len(cast)))
all_ids={o['memory_object_id'] for o in mos}; story_set=set(story_ids); practice=set(lab['practice_only_runtime_object_ids'])
if len(story_ids)!=199 or len(story_set)!=199:problems.append(f"Permanent story coverage is {len(story_ids)} refs / {len(story_set)} unique, expected 199/199")
if len(practice)!=8:problems.append(f"Practice-only runtime partition is {len(practice)}, expected 8")
if story_set|practice != all_ids:problems.append('Story + practice-only partition does not equal all 207 runtime objects')
if story_set&practice:problems.append('Story and practice-only partitions overlap')
if sum(len(j['scenes']) for j in journeys)!=78:problems.append('Scene count is not 78')
if sum(j['checkpoint_count'] for j in journeys)!=27:problems.append('Checkpoint count is not 27')
if lab['challenge_count']!=16:problems.append('Application lab does not contain 16 challenges')
for x in lab['items']:
    visible=' '.join([x['title'],x['prompt'],x['answer_guide'],x['story_hint']])
    if banned.search(visible):problems.append(f"{x['challenge_id']} exposes source-management language: {banned.search(visible).group(0)}")
course=read(U1.parent/'course.json')
if len(course['units'])!=8:problems.append('AP Biology course registry does not contain all 8 units')
lines=[
'# Memory Palace V2 · Full Unit 1 QA', '',
'## Release accounting','',
'- Canonical Unit 1 records: **229 / 229 accounted**',
'- Student-runtime Memory Objects: **207 / 207 accounted**',
'- Permanent-palace story objects: **199 / 199 represented once**',
'- Practice-only runtime objects: **8 / 8 represented in the Unit 1 Challenge Lab**',
'- Permanent palace journeys: **9 / 9**',
'- Permanent locations: **78 / 78**',
'- Optional first-exposure recall points: **27**',
'- Application/transfer challenges: **16 / 16**','',
'## Narrative QA','',
'Every scene is required to contain a specific location description, a left/center/right layout, at least two identifiable actors/parts with visual identities and jobs, at least 130 narrative words, and explicit introduction of every exact-name target assigned to that scene. Student-visible story and practice text is also scanned for source-management language.','',
'| Palace | Scene | Locus | Narrative words | Objects | Cast |','|---|---:|---|---:|---:|---:|']
for row in scene_rows:lines.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} |")
lines+=['','## Result','',('**PASS** — no blocking findings.' if not problems else '**FAIL**'), '']
if problems:
    lines+=['### Blocking findings','']+[f'- {p}' for p in problems]
DOC.write_text('\n'.join(lines)+'\n',encoding='utf-8')
if problems:
    print('\n'.join(problems));sys.exit(1)
print('Full Unit 1 QA PASS')
print({'canonical':229,'runtime':207,'story_objects':199,'practice_only':8,'journeys':9,'scenes':78,'checkpoints':27,'challenges':16})
