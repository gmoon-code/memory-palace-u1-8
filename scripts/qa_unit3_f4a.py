from __future__ import annotations
import json, hashlib, re, statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content/ap-biology/unit-3'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
source=read(U3/'source/canonical-unit3-f1.json'); canon={r['knowledge_id']:r for r in source['canonical_catalog']}
f3=read(U3/'briefs/scene-briefs-f3.json'); f3j1=[b for b in f3['scene_briefs'] if b['journey_id']=='U3-J1']
journey=read(U3/'journeys/U3-J1.json'); registry=read(U3/'journeys-f4a.json'); status=read(U3/'status-f4a.json'); lock=read(U3/'content-lock-f4a.json')

assert journey['palace_id']=='U3-J1'
assert journey['scene_count']==len(journey['scenes'])==3
assert journey['checkpoint_count']==2
assert registry['journey_count']==1 and registry['scene_count']==3 and registry['checkpoint_count']==2
assert status['polished_journeys']==1 and status['polished_scenes']==3 and status['student_release'] is False and status['preview_release'] is True
assert [s['locus'] for s in journey['scenes']]==[b['scene_title'] for b in f3j1]

assigned=[]; word_counts=[]
prohibited=('ppt','ced','campbell','college board','canonical record','source material','teacher deck','teacher test','review flag','spatial encoding','layout job','locked definition')
required={
'U3-L01':['activation energy','enzyme','biological catalyst','lowering','transition state','regulate biological processes'],
'U3-L02':['substrate','active site','enzyme-substrate complex','induced fit','shape','charge'],
'U3-L03':['reusable catalysts','being consumed','reaction cycles','-ase','pepsin','trypsin']
}
for s,b in zip(journey['scenes'],f3j1):
    assert s['object_ids']==b['knowledge_ids']; assigned += s['object_ids']
    assert len(s['scene_layout']['zones'])==3
    assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
    assert all(len(z['description'])>=70 for z in s['scene_layout']['zones'])
    assert len(s['scene_layout']['orientation'])>=120
    assert len(s['cast'])>=4 and s['cast'][0]['name']=='Dr. Nia Park'
    assert all(c['name'] and len(c['visual'])>=20 and len(c['job'])>=20 for c in s['cast'])
    prose=' '.join(s['story_paragraphs']); words=re.findall(r"\b[\w’'-]+\b",prose); word_counts.append(len(words))
    assert len(words)>=350,(s['locus'],len(words)); assert len(s['story_paragraphs'])>=5; assert len(s['story_close'])>=90
    low=prose.lower().replace('**','')
    hits=[x for x in prohibited if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',low)]
    assert not hits,(s['locus'],hits)
    for term in required[b['locus_id']]: assert term in low,(s['locus'],term)
    assert len(s['story_beats'])==len(b['term_introductions'])
    for beat,t in zip(s['story_beats'],b['term_introductions']):
        assert beat['object_id']==t['knowledge_id']
        assert beat['science']==t['canonical_science']==canon[t['knowledge_id']]['canonical_verified_statement']
        assert beat['exact_name']==t['exact_name_recall']; assert beat['term'] and beat['hint']
    assert s['misconception_guards']==b['misconception_guards']; assert s['carry_forward']==b['carry_forward']
    expected_next=f3j1[s['scene_index']+1]['scene_title'] if s['scene_index']+1<len(f3j1) else None
    assert s['next_locus']==expected_next
    if s['checkpoint']:
        assert s['checkpoint_prompt'] and s['checkpoint_answer'] and len(s['checkpoint_hint'])>=70

assert len(assigned)==len(set(assigned))==11
assert set(assigned)=={kid for b in f3j1 for kid in b['knowledge_ids']}
assert sum(bool(s['checkpoint']) for s in journey['scenes'])==2
assert min(word_counts)>=350 and statistics.mean(word_counts)>=400
assert journey['guide']['name']=='Dr. Nia Park'
assert 'three-room route' in journey['route_orientation']
assert len(journey['premise'])>=120 and len(journey['mission'])>=100 and len(journey['finale'])>=140

for rel,digest in lock['files'].items():
    p=U3/rel; assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest

print('UNIT3 F4A QA PASS')
print(json.dumps({'journey':'U3-J1','scenes':3,'knowledge_records':11,'optional_recalls':2,'story_words':sum(word_counts),'average_scene_words':round(statistics.mean(word_counts),1),'min_scene_words':min(word_counts),'student_release':False,'preview_release':True},indent=2))
