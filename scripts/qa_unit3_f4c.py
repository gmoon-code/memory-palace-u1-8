from __future__ import annotations
import json, hashlib, re, statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content/ap-biology/unit-3'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
source=read(U3/'source/canonical-unit3-f1.json'); canon={r['knowledge_id']:r for r in source['canonical_catalog']}
f3=read(U3/'briefs/scene-briefs-f3.json'); f3j3=[b for b in f3['scene_briefs'] if b['journey_id']=='U3-J3']
j=read(U3/'journeys/U3-J3.json'); reg=read(U3/'journeys-f4c.json'); status=read(U3/'status-f4c.json'); lock=read(U3/'content-lock-f4c.json')
assert j['palace_id']=='U3-J3' and j['scene_count']==len(j['scenes'])==10 and j['checkpoint_count']==3
assert reg['journey_count']==3 and reg['scene_count']==21 and reg['checkpoint_count']==8
assert [x['palace_id'] for x in reg['guided_journeys']]==['U3-J1','U3-J2','U3-J3']
assert status['polished_journeys']==3 and status['polished_scenes']==21 and status['student_release'] is False and status['preview_release'] is True
assert [s['locus'] for s in j['scenes']]==[b['scene_title'] for b in f3j3]

required={
'U3-L12':['metabolism','metabolic pathway','catabolic pathway','anabolic pathway','pathway intermediates','sequential metabolic pathways'],
'U3-L13':['energy','kinetic energy','thermal energy','potential energy','chemical energy'],
'U3-L14':['thermodynamics','first law of thermodynamics','energy cannot be created or destroyed','living cell'],
'U3-L15':['second law of thermodynamics','entropy','energy input','loss of energy flow','local'],
'U3-L16':['gibbs free energy','exergonic reaction','endergonic reaction','far from equilibrium','spontaneity'],
'U3-L17':['energy coupling','mechanical cellular work','transport work','chemical work','energy input'],
'U3-L18':['adenosine triphosphate','atp','adenine','ribose','three phosphate'],
'U3-L19':['atp hydrolysis','lower-free-energy products','phosphorylation','energy coupling','break chemical bonds'],
'U3-L20':['atp regeneration cycle','adp','inorganic phosphate','exergonic'],
'U3-L21':['conserved core metabolism','archaea','bacteria','eukarya','common ancestry'],
}
prohibited=('ppt','ced','campbell','college board','canonical record','source material','teacher deck','teacher test','review flag','spatial encoding','layout job','locked definition','audit label','the packet')
assigned=[]; wc=[]
for s,b in zip(j['scenes'],f3j3):
    assert s['object_ids']==b['knowledge_ids']; assigned+=s['object_ids']
    assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
    assert all(len(z['description'])>=70 for z in s['scene_layout']['zones'])
    assert len(s['scene_layout']['orientation'])>=120
    assert len(s['cast'])>=4 and s['cast'][0]['name']=='Dr. Nia Park'
    assert all(c['name'] and len(c['visual'])>=20 and len(c['job'])>=20 for c in s['cast'])
    prose=' '.join(s['story_paragraphs']); words=re.findall(r"\b[\w’'-]+\b",prose); wc.append(len(words))
    assert len(words)>=340,(s['locus'],len(words)); assert len(s['story_paragraphs'])>=4; assert len(s['story_close'])>=90
    low=prose.lower().replace('**','')
    hits=[x for x in prohibited if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',low)]
    assert not hits,(s['locus'],hits)
    for term in required[b['locus_id']]: assert term in low,(s['locus'],term)
    assert len(s['story_beats'])==len(b['term_introductions'])
    for beat,t in zip(s['story_beats'],b['term_introductions']):
        assert beat['object_id']==t['knowledge_id']
        assert beat['science']==t['canonical_science']==canon[t['knowledge_id']]['canonical_verified_statement']
        assert beat['exact_name']==t['exact_name_recall']; assert beat['term'] and len(beat['hint'])>=20
    assert s['misconception_guards']==b['misconception_guards']; assert s['carry_forward']==b['carry_forward']
    exp=f3j3[s['scene_index']+1]['scene_title'] if s['scene_index']+1<len(f3j3) else None
    assert s['next_locus']==exp
    if s['checkpoint']:
        assert s['checkpoint_prompt'] and s['checkpoint_answer'] and len(s['checkpoint_hint'])>=70

assert len(assigned)==len(set(assigned))==37
assert set(assigned)=={kid for b in f3j3 for kid in b['knowledge_ids']}
assert sum(bool(s['checkpoint']) for s in j['scenes'])==3
assert min(wc)>=340 and statistics.mean(wc)>=395
assert j['guide']['name']=='Dr. Nia Park'
assert 'ten-station route' in j['route_orientation']
assert len(j['premise'])>=120 and len(j['mission'])>=100 and len(j['finale'])>=180
assert 'accounting marker' in ' '.join(j['scenes'][0]['story_paragraphs']).lower()
assert 'energy itself is not a little object' in ' '.join(j['scenes'][0]['story_paragraphs']).lower()
assert 'energy is required to break chemical bonds' in ' '.join(j['scenes'][7]['story_paragraphs']).lower()
assert 'not from energy released by breaking a phosphate bond itself' in ' '.join(j['scenes'][7]['story_paragraphs']).lower()
assert 'full gibbs free-energy equation' in ' '.join(j['scenes'][4]['story_paragraphs']).lower()

# Historical F4A and F4B locks stay intact.
for lockname in ('content-lock-f4a.json','content-lock-f4b.json'):
    old=read(U3/lockname)
    for rel,digest in old['files'].items():
        p=U3/rel; assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest
for rel,digest in lock['files'].items():
    p=U3/rel; assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest

print('UNIT3 F4C QA PASS')
print(json.dumps({'journey':'U3-J3','scenes':10,'knowledge_records':37,'optional_recalls':3,'story_words':sum(wc),'average_scene_words':round(statistics.mean(wc),1),'min_scene_words':min(wc),'polished_journeys_total':3,'student_release':False,'preview_release':True},indent=2))
