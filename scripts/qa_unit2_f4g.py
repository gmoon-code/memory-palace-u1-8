from __future__ import annotations
import json, hashlib, re, statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
source=read(U2/'source/canonical-unit2-f1.json'); canon={r['knowledge_id']:r for r in source['canonical_catalog']}
f3=read(U2/'briefs/scene-briefs-f3.json'); briefs=[b for b in f3['scene_briefs'] if b['journey_id']=='U2-J7']
j=read(U2/'journeys/U2-J7.json'); reg=read(U2/'journeys-f4g.json'); status=read(U2/'status-f4g.json'); lock=read(U2/'content-lock-f4g.json')
arch=read(U2/'architecture/palace-architecture-f2.json')

assert j['palace_id']=='U2-J7' and j['scene_count']==len(j['scenes'])==4 and j['checkpoint_count']==2
assert reg['journey_count']==7 and reg['scene_count']==49 and reg['checkpoint_count']==17
assert [x['palace_id'] for x in reg['guided_journeys']]==[f'U2-J{i}' for i in range(1,8)]
assert status['polished_journeys']==7 and status['polished_scenes']==49 and status['student_release'] is False and status['preview_release'] is True
assert [s['locus'] for s in j['scenes']]==[b['scene_title'] for b in briefs]

required={
'U2-L46':['compartmentalization','minimizing competing interactions','increasing reaction surface','internal membranes','separation'],
'U2-L47':['prokaryotic compartmentalization','eukaryotic compartmentalization','membrane-bound organelles','organized internal regions'],
'U2-L48':['endosymbiosis','free-living prokaryotic cells','retained','integrated','historical'],
'U2-L49':['circular dna','binary fission','ribosomes','double membranes','modern organelle dependence','host cell and its nucleus','converging']
}
prohibited=('ppt','ced','campbell','college board','locked definition','canonical record','source material','class notes','the packet','spatial encoding','layout job','fixed visual zone','must remain visible','source-facing','teacher deck','worksheet')
assigned=[]; wc=[]
for s,b in zip(j['scenes'],briefs):
    assert s['object_ids']==b['knowledge_ids']; assigned += s['object_ids']
    assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
    assert all(len(z['description'])>=90 for z in s['scene_layout']['zones'])
    assert len(s['location_description'])>=120
    assert len(s['scene_layout']['orientation'])>=100
    assert len(s['cast'])>=4 and s['cast'][0]['name']=='Dr. Nia Park'
    assert all(c['name'] and len(c['visual'])>=18 and len(c['job'])>=18 for c in s['cast'])
    prose=' '.join(s['story_paragraphs']); words=re.findall(r"\b[\w’'+₂⁺⁻Ψ=-]+\b",prose); wc.append(len(words))
    assert len(words)>=350,(s['locus'],len(words)); assert len(s['story_paragraphs'])>=4; assert len(s['story_close'])>=110
    low=prose.lower().replace('**','')
    hits=[x for x in prohibited if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',low)]
    assert not hits,(s['locus'],hits)
    for term in required[b['locus_id']]: assert term in low,(s['locus'],term)
    assert len(s['story_beats'])==len(b['term_introductions'])
    for beat,t in zip(s['story_beats'],b['term_introductions']):
        assert beat['object_id']==t['knowledge_id']
        assert beat['science']==t['canonical_science']==canon[t['knowledge_id']]['canonical_verified_statement']
        assert beat['exact_name']==t['exact_name_recall']
        assert beat['term'] and len(beat['hint'])>=35
    assert s['misconception_guards']==b['misconception_guards']; assert s['carry_forward']==b['carry_forward']
    expected=briefs[s['scene_index']+1]['scene_title'] if s['scene_index']+1<len(briefs) else None
    assert s['next_locus']==expected
    if s['checkpoint']:
        assert s['checkpoint_prompt'] and s['checkpoint_answer'] and len(s['checkpoint_hint'])>=100

assert len(assigned)==len(set(assigned))==11
assert set(assigned)=={kid for b in briefs for kid in b['knowledge_ids']}
assert sum(bool(s['checkpoint']) for s in j['scenes'])==2
assert min(wc)>=350 and statistics.mean(wc)>=400
assert j['guide']['name']=='Dr. Nia Park'
assert 'evidence case' in j['learner_rule'].lower() and 'historical reconstruction' in j['learner_rule'].lower()
assert len(j['premise'])>=100 and len(j['mission'])>=80 and len(j['finale'])>=180
whole=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).lower().replace('**','')
assert 'not unorganized' in whole
assert 'no one watched the original events happen' in whole
assert 'a plausible story is not enough' in whole
assert 'none of the cards alone' in whole
assert 'not generally capable of independent free-living existence' in whole

# Across all 7 polished journeys, every palace-managed F2 record appears exactly once.
all_story=[]
for i in range(1,8):
    ji=read(U2/'journeys'/f'U2-J{i}.json')
    all_story += [kid for s in ji['scenes'] for kid in s['object_ids']]
assert len(all_story)==133 and len(set(all_story))==133
palace_ids={l['primary_knowledge_id'] for l in arch['loci']}
for l in arch['loci']:
    palace_ids.update(l.get('embedded_knowledge_ids',[]))
assert set(all_story)==palace_ids

for rel,digest in lock['files'].items():
    p=U2/rel; assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest

print('UNIT2 F4G QA PASS')
print(json.dumps({'journey':'U2-J7','scenes':4,'knowledge_records':11,'optional_recalls':2,'story_words':sum(wc),'average_scene_words':round(statistics.mean(wc),1),'min_scene_words':min(wc),'polished_journeys_total':7,'polished_scenes_total':49,'palace_managed_records_covered':len(all_story),'student_release':False,'preview_release':True},indent=2))
