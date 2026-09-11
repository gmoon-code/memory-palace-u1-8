from __future__ import annotations
import json, hashlib, re, statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
source=read(U2/'source/canonical-unit2-f1.json'); canon={r['knowledge_id']:r for r in source['canonical_catalog']}
f3=read(U2/'briefs/scene-briefs-f3.json'); f3j2=[b for b in f3['scene_briefs'] if b['journey_id']=='U2-J2']
j=read(U2/'journeys/U2-J2.json'); reg=read(U2/'journeys-f4b.json'); status=read(U2/'status-f4b.json'); lock=read(U2/'content-lock-f4b.json')
assert j['palace_id']=='U2-J2' and j['scene_count']==len(j['scenes'])==5 and j['checkpoint_count']==2
assert reg['journey_count']==2 and reg['scene_count']==18 and reg['checkpoint_count']==6
assert [x['palace_id'] for x in reg['guided_journeys']]==['U2-J1','U2-J2']
assert status['polished_journeys']==2 and status['polished_scenes']==18 and status['student_release'] is False and status['preview_release'] is True
assert [s['locus'] for s in j['scenes']]==[b['scene_title'] for b in f3j2]
required={
'U2-L14':['mitochondrial double membrane','intermembrane space','mitochondrial matrix','pyruvate oxidation','citric acid cycle'],
'U2-L15':['mitochondrial inner folds','cristae','inner mitochondrial membrane','atp synthesis'],
'U2-L16':['high sustained energy demand','many mitochondria','mitochondrial abundance','physiological state'],
'U2-L17':['chloroplasts','plants','photosynthetic algae','double membrane','photosynthesis'],
'U2-L18':['thylakoid','granum','chlorophyll','stroma','light-dependent','calvin cycle'],
}
prohibited=('ppt','ced','campbell','college board','locked definition','canonical record','source material','class notes','the packet','spatial encoding','layout job','fixed visual zone','must remain visible','source-facing','teacher deck','powerhouse of the cell')
assigned=[]; wc=[]
for s,b in zip(j['scenes'],f3j2):
    assert s['object_ids']==b['knowledge_ids']; assigned+=s['object_ids']
    assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
    assert all(len(z['description'])>=55 for z in s['scene_layout']['zones'])
    assert len(s['scene_layout']['orientation'])>=100
    assert len(s['cast'])>=3 and s['cast'][0]['name']=='Dr. Nia Park'
    assert all(c['name'] and len(c['visual'])>=10 and len(c['job'])>=10 for c in s['cast'])
    prose=' '.join(s['story_paragraphs']); words=re.findall(r"\b[\w’'-]+\b",prose); wc.append(len(words))
    assert len(words)>=280,(s['locus'],len(words)); assert len(s['story_paragraphs'])>=4; assert len(s['story_close'])>=80
    low=prose.lower().replace('**','')
    hits=[x for x in prohibited if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',low)]
    assert not hits,(s['locus'],hits)
    for term in required[b['locus_id']]: assert term in low,(s['locus'],term)
    assert len(s['story_beats'])==len(b['term_introductions'])
    for beat,t in zip(s['story_beats'],b['term_introductions']):
        assert beat['object_id']==t['knowledge_id']; assert beat['science']==t['canonical_science']==canon[t['knowledge_id']]['canonical_verified_statement']; assert beat['exact_name']==t['exact_name_recall']; assert beat['term'] and len(beat['hint'])>=20
    assert s['misconception_guards']==b['misconception_guards']; assert s['carry_forward']==b['carry_forward']
    exp=f3j2[s['scene_index']+1]['scene_title'] if s['scene_index']+1<len(f3j2) else None
    assert s['next_locus']==exp
    if s['checkpoint']: assert s['checkpoint_prompt'] and s['checkpoint_answer'] and len(s['checkpoint_hint'])>=55
assert len(assigned)==len(set(assigned))==12
assert set(assigned)=={kid for b in f3j2 for kid in b['knowledge_ids']}
assert sum(bool(s['checkpoint']) for s in j['scenes'])==2
assert min(wc)>=280 and statistics.mean(wc)>=320
assert j['guide']['name']=='Dr. Nia Park' and 'two transparent organelle chambers' in j['route_orientation']
assert len(j['premise'])>=100 and len(j['mission'])>=80 and len(j['finale'])>=140
for rel,digest in lock['files'].items():
    p=U2/rel; assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest
print('UNIT2 F4B QA PASS')
print(json.dumps({'journey':'U2-J2','scenes':5,'knowledge_records':12,'optional_recalls':2,'story_words':sum(wc),'average_scene_words':round(statistics.mean(wc),1),'min_scene_words':min(wc),'polished_journeys_total':2,'student_release':False,'preview_release':True},indent=2))
