from __future__ import annotations
import json, hashlib, re, statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
source=read(U2/'source/canonical-unit2-f1.json'); canon={r['knowledge_id']:r for r in source['canonical_catalog']}
f3=read(U2/'briefs/scene-briefs-f3.json'); f3j3=[b for b in f3['scene_briefs'] if b['journey_id']=='U2-J3']
j=read(U2/'journeys/U2-J3.json'); reg=read(U2/'journeys-f4c.json'); status=read(U2/'status-f4c.json'); lock=read(U2/'content-lock-f4c.json')
assert j['palace_id']=='U2-J3' and j['scene_count']==len(j['scenes'])==3 and j['checkpoint_count']==1
assert reg['journey_count']==3 and reg['scene_count']==21 and reg['checkpoint_count']==7
assert [x['palace_id'] for x in reg['guided_journeys']]==['U2-J1','U2-J2','U2-J3']
assert status['polished_journeys']==3 and status['polished_scenes']==21 and status['student_release'] is False and status['preview_release'] is True
assert [s['locus'] for s in j['scenes']]==[b['scene_title'] for b in f3j3]
required={
'U2-L19':['surface-area-to-volume ratio','sa:v','plasma-membrane surface area','6s²','s³','4πr²','4/3πr³','volume grows faster than surface area'],
'U2-L20':['membrane folds','exchange-surface adaptations','more surface','geometry','permeability'],
'U2-L21':['organism size','surface-area-to-volume ratio','proportional heat exchange','metabolic rate per unit body mass','smaller multicellular organisms']
}
prohibited=('ppt','ced','campbell','college board','locked definition','canonical record','source material','class notes','the packet','spatial encoding','layout job','fixed visual zone','must remain visible','source-facing','teacher deck','worksheet')
assigned=[]; wc=[]
for s,b in zip(j['scenes'],f3j3):
    assert s['object_ids']==b['knowledge_ids']; assigned+=s['object_ids']
    assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
    assert all(len(z['description'])>=70 for z in s['scene_layout']['zones'])
    assert len(s['scene_layout']['orientation'])>=100
    assert len(s['cast'])>=4 and s['cast'][0]['name']=='Dr. Nia Park'
    assert all(c['name'] and len(c['visual'])>=10 and len(c['job'])>=10 for c in s['cast'])
    prose=' '.join(s['story_paragraphs']); words=re.findall(r"\b[\w’'-]+\b",prose); wc.append(len(words))
    assert len(words)>=400,(s['locus'],len(words)); assert len(s['story_paragraphs'])>=5; assert len(s['story_close'])>=90
    low=prose.lower().replace('**','')
    hits=[x for x in prohibited if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',low)]
    assert not hits,(s['locus'],hits)
    for term in required[b['locus_id']]: assert term in low,(s['locus'],term)
    assert len(s['story_beats'])==len(b['term_introductions'])
    for beat,t in zip(s['story_beats'],b['term_introductions']):
        assert beat['object_id']==t['knowledge_id']; assert beat['science']==t['canonical_science']==canon[t['knowledge_id']]['canonical_verified_statement']; assert beat['exact_name']==t['exact_name_recall']; assert beat['term'] and len(beat['hint'])>=30
    assert s['misconception_guards']==b['misconception_guards']; assert s['carry_forward']==b['carry_forward']
    expected=f3j3[s['scene_index']+1]['scene_title'] if s['scene_index']+1<len(f3j3) else None
    assert s['next_locus']==expected
    if s['checkpoint']: assert s['checkpoint_prompt'] and s['checkpoint_answer'] and len(s['checkpoint_hint'])>=70
assert len(assigned)==len(set(assigned))==9
assert set(assigned)=={kid for b in f3j3 for kid in b['knowledge_ids']}
assert sum(bool(s['checkpoint']) for s in j['scenes'])==1
assert min(wc)>=400 and statistics.mean(wc)>=450
assert j['guide']['name']=='Dr. Nia Park' and 'Cube Gallery' in j['route_orientation'] and 'thermal terrace' in j['route_orientation']
assert len(j['premise'])>=100 and len(j['mission'])>=80 and len(j['finale'])>=140
# quantitative statements explicitly checked
p=' '.join(j['scenes'][0]['story_paragraphs']).lower()
for exact in ['6 square units','1 cubic unit','24 square units','8 cubic units','54','27','6:1','3:1','2:1']:
    assert exact in p,exact
for rel,digest in lock['files'].items():
    path=U2/rel; assert path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==digest
print('UNIT2 F4C QA PASS')
print(json.dumps({'journey':'U2-J3','scenes':3,'knowledge_records':9,'optional_recalls':1,'story_words':sum(wc),'average_scene_words':round(statistics.mean(wc),1),'min_scene_words':min(wc),'polished_journeys_total':3,'student_release':False,'preview_release':True},indent=2))
