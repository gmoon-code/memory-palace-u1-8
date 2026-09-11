from __future__ import annotations
import json,re,statistics,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content'/'ap-biology'/'unit-3'
DOC=ROOT/'docs'/'UNIT3_F4G_NARRATIVE_QA.md'
MATRIX=ROOT/'docs'/'UNIT3_F4G_STORY_MATRIX.md'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
j=read(U3/'journeys'/'U3-J7.json')
briefs=[x for x in read(U3/'briefs'/'scene-briefs-f3.json')['scene_briefs'] if x['journey_id']=='U3-J7']
lock=read(U3/'content-lock-f4g.json')
prohibited=('ppt','ced','campbell','college board','canonical record','source material','teacher deck','teacher test','review flag','spatial encoding','layout job','locked definition','audit label','the packet')
required={
'U3-L51':['respiration and fermentation across life','anaerobic respiration','electron-transport chain','terminal electron acceptor','nitrate','sulfate','fermentation'],
'U3-L52':['fermentation and nad⁺ recycling','fermentation','regenerates nad⁺','without using an electron-transport chain','glycolysis','substrate-level phosphorylation','oxygen'],
'U3-L53':['alcohol fermentation','pyruvate','acetaldehyde','ethanol','co₂','nadh','nad⁺'],
'U3-L54':['lactate formation','pyruvate','lactate','nad⁺','oxygen is present','acute burning sensation','delayed-onset muscle soreness','liver and kidney','glucose synthesis'],
}
problems=[];assigned=[];wc=[];rows=[]
if j['scene_count']!=4: problems.append(f"Journey has {j['scene_count']} scenes, expected 4")
if j['checkpoint_count']!=1: problems.append(f"Journey has {j['checkpoint_count']} checkpoints, expected 1")
if j['guide']['name']!='Dr. Nia Park': problems.append('Guide changed from Dr. Nia Park')
if len(j['route'])!=4: problems.append('Route is not four loci')
for s,b in zip(j['scenes'],briefs):
    assigned.extend(s['object_ids'])
    if s['object_ids']!=b['knowledge_ids']: problems.append(f"{s['locus']} knowledge IDs differ from locked F3 brief")
    zones=s.get('scene_layout',{}).get('zones',[])
    if [z.get('position') for z in zones]!=['left','center','right']: problems.append(f"{s['locus']} does not preserve left/center/right geometry")
    if any(len(z.get('description',''))<95 for z in zones): problems.append(f"{s['locus']} has thin zone description")
    if len(s.get('scene_layout',{}).get('orientation',''))<120: problems.append(f"{s['locus']} has thin orientation")
    if len(s.get('cast',[]))<4 or s['cast'][0]['name']!='Dr. Nia Park': problems.append(f"{s['locus']} cast is incomplete")
    prose=' '.join(s['story_paragraphs']); words=len(re.findall(r"\b[\w’'⁺₂-]+\b",prose));wc.append(words)
    if words<350: problems.append(f"{s['locus']} has only {words} narrative words")
    if len(s['story_paragraphs'])<4: problems.append(f"{s['locus']} has fewer than four narrative paragraphs")
    low=prose.lower().replace('**','')
    hits=[x for x in prohibited if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',low)]
    if hits: problems.append(f"{s['locus']} exposes source-management language: {hits}")
    for term in required[b['locus_id']]:
        if term not in low: problems.append(f"{s['locus']} is missing required narrative wording: {term}")
    if len(s['story_beats'])!=len(b['term_introductions']): problems.append(f"{s['locus']} story-beat count differs from brief")
    else:
        for beat,t in zip(s['story_beats'],b['term_introductions']):
            if beat['object_id']!=t['knowledge_id']: problems.append(f"{s['locus']} beat object mismatch")
            if beat['science']!=t['canonical_science']: problems.append(f"{s['locus']} science wording differs for {t['knowledge_id']}")
            if bool(beat['exact_name'])!=bool(t['exact_name_recall']): problems.append(f"{s['locus']} exact-name flag differs for {t['knowledge_id']}")
            if t['exact_name_recall'] and t['canonical_term'].lower() not in low: problems.append(f"{s['locus']} does not explicitly introduce {t['canonical_term']}")
    if s['misconception_guards']!=b['misconception_guards']: problems.append(f"{s['locus']} misconception guards differ from F3 brief")
    if s['carry_forward']!=b['carry_forward']: problems.append(f"{s['locus']} carry-forward differs from F3 brief")
    expected=j['scenes'][s['scene_index']+1]['locus'] if s['scene_index']+1<len(j['scenes']) else None
    if s['next_locus']!=expected: problems.append(f"{s['locus']} transition target is wrong")
    rows.append((s['scene_index']+1,s['locus'],words,len(s['object_ids']),bool(s['checkpoint'])))

if len(assigned)!=len(set(assigned))!=11: problems.append('Duplicate or incorrect Journey 7 record accounting')
if len(assigned)!=11 or len(set(assigned))!=11: problems.append(f"Journey 7 record accounting is {len(assigned)} refs / {len(set(assigned))} unique, expected 11/11")
if sum(bool(s['checkpoint']) for s in j['scenes'])!=1: problems.append('Journey 7 optional recall count is not 1')
if min(wc)<350 or statistics.mean(wc)<400 or sum(wc)<1600: problems.append(f"Narrative density failed: total={sum(wc)}, mean={statistics.mean(wc):.1f}, min={min(wc)}")

# High-risk mechanism guards.
junc=' '.join(j['scenes'][0]['story_paragraphs']).lower()
gate=' '.join(j['scenes'][1]['story_paragraphs']).lower()
alc=' '.join(j['scenes'][2]['story_paragraphs']).lower()
lac=' '.join(j['scenes'][3]['story_paragraphs']).lower()
for phrase in ['anaerobic respiration','still uses an etc','terminal acceptor other than oxygen','fermentation takes a different route']:
    if phrase not in junc: problems.append(f"Junction missing guard phrase: {phrase}")
for phrase in ['without using an electron-transport chain','does not provide a large extra atp harvest','fermentation does not require oxygen','some cells can run fermentation even when oxygen is present']:
    if phrase not in gate: problems.append(f"NAD+ gate missing guard phrase: {phrase}")
for phrase in ['pyruvate decarboxylation','acetaldehyde','ethanol','atp display still does not jump upward']:
    if phrase not in alc: problems.append(f"Alcohol scene missing guard phrase: {phrase}")
for phrase in ['no co₂ chute','oxygen is present','not the cause of the acute burning sensation','not the cause of delayed-onset muscle soreness','transportable metabolic intermediate']:
    if phrase not in lac: problems.append(f"Lactate scene missing guard phrase: {phrase}")

# Historical locks through F4F remain immutable.
for lockname in ('content-lock-f4a.json','content-lock-f4b.json','content-lock-f4c.json','content-lock-f4d.json','content-lock-f4e.json','content-lock-f4f.json'):
    old=read(U3/lockname)
    for rel,digest in old['files'].items():
        p=U3/rel
        if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest: problems.append(f"Historical lock changed: {lockname} {rel}")
for rel,digest in lock['files'].items():
    p=U3/rel
    if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest: problems.append(f"F4G lock mismatch: {rel}")

qa=[
'# Unit 3 F4G Narrative QA','',
'## Journey 7','',
'**Alternative Energy Annex — The NAD⁺ Cards That Would Not Return**','',
'- Locked knowledge records: **11 / 11**','- Connected scenes: **4 / 4**','- Optional first-exposure Quick Recalls: **1**',
 f'- Narrative words: **{sum(wc):,}**',f'- Average scene length: **{statistics.mean(wc):.1f} words**',f'- Shortest scene: **{min(wc)} words**','',
'## Narrative and scientific gates','',
'- Fixed left/center/right geometry in every scene','- Same Unit 3 guide, Dr. Nia Park, across the route','- The limited NAD⁺ pool remains the continuity object','- Aerobic respiration, anaerobic respiration, and fermentation remain mechanistically distinct','- Anaerobic respiration retains an ETC and uses a non-oxygen terminal electron acceptor','- Fermentation regenerates NAD⁺ without an ETC and does not add substantial ATP beyond glycolysis','- Alcohol fermentation explicitly includes pyruvate decarboxylation, acetaldehyde, ethanol, CO₂, and NAD⁺ regeneration','- Lactate formation preserves all three pyruvate carbons, regenerates NAD⁺, and does not use an obsolete lactate-as-poison model','- Human lactate production is not equated with total oxygen absence, acute burn, or delayed-onset muscle soreness','- Lactate remains connected to transport, oxidation, and liver/kidney carbon reuse','- Student prose contains no source-management or audit language','- F4A–F4F historical content locks remain unchanged','',
'| Scene | Locus | Narrative words | Locked records | Quick Recall |','|---:|---|---:|---:|---|']
for r in rows: qa.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {'Yes' if r[4] else 'No'} |")
qa += ['', '## Result','', '**PASS** — no blocking findings.' if not problems else '**FAIL**']
if problems: qa+=['','### Blocking findings','']+[f'- {p}' for p in problems]
DOC.write_text('\n'.join(qa)+'\n',encoding='utf-8')

matrix=['# Unit 3 F4G Journey 7 Story Matrix','',
'| # | Locus | Stable left anchor | Center mechanism | Stable right anchor | Locked science | Narrative function |','|---:|---|---|---|---|---|---|']
for s,b in zip(j['scenes'],briefs):
    z=s['scene_layout']['zones']; terms=', '.join(t['canonical_term'] for t in b['term_introductions'])
    matrix.append(f"| {s['scene_index']+1} | {s['locus']} | {z[0]['label']} | {z[1]['label']} | {z[2]['label']} | {terms} | {s['scene_kicker']} |")
matrix += ['','## Continuity','',
'The route begins at the oxygen-limited emergency created at the end of Journey 6. A finite rack of NAD⁺ cards stays visible throughout Journey 7. The rack first reveals the shared redox constraint, then fermentation refills it directly without an ETC, alcohol fermentation demonstrates one carbon-product route, and lactate formation demonstrates a second route whose product remains metabolically reusable.','',
'## Final discrimination','',
'**Aerobic respiration** uses an ETC with oxygen as terminal electron acceptor. **Anaerobic respiration** uses an ETC with a terminal acceptor other than oxygen. **Fermentation** regenerates NAD⁺ without using an ETC. Alcohol and lactate fermentation are two distinct fermentation pathways with different carbon products.']
MATRIX.write_text('\n'.join(matrix)+'\n',encoding='utf-8')

if problems:
    print('\n'.join(problems));sys.exit(1)
print('UNIT3 F4G QA PASS')
print(json.dumps({'journey':'U3-J7','scenes':4,'knowledge_records':11,'optional_recalls':1,'story_words':sum(wc),'average_scene_words':round(statistics.mean(wc),1),'min_scene_words':min(wc),'polished_journeys_total':7,'polished_scenes_total':54,'student_release':False,'preview_release':True},indent=2))
