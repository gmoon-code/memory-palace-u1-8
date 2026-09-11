from __future__ import annotations
import json, hashlib, re, statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content/ap-biology/unit-3'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
source=read(U3/'source/canonical-unit3-f1.json'); canon={r['knowledge_id']:r for r in source['canonical_catalog']}
f3=read(U3/'briefs/scene-briefs-f3.json'); f3j4=[b for b in f3['scene_briefs'] if b['journey_id']=='U3-J4']
j=read(U3/'journeys/U3-J4.json'); reg=read(U3/'journeys-f4d.json'); status=read(U3/'status-f4d.json'); lock=read(U3/'content-lock-f4d.json')
assert j['palace_id']=='U3-J4' and j['scene_count']==len(j['scenes'])==12 and j['checkpoint_count']==4
assert reg['journey_count']==4 and reg['scene_count']==33 and reg['checkpoint_count']==12
assert [x['palace_id'] for x in reg['guided_journeys']]==['U3-J1','U3-J2','U3-J3','U3-J4']
assert status['polished_journeys']==4 and status['polished_scenes']==33 and status['student_release'] is False and status['preview_release'] is True
assert [s['locus'] for s in j['scenes']]==[b['scene_title'] for b in f3j4]

required={
'U3-L22':['autotroph','photoautotroph','heterotroph','photosynthesis overall process','solar energy capture','carbon source','energy source'],
'U3-L23':['prokaryotic origin of photosynthesis','atmospheric oxygenation','foundation of eukaryotic photosynthesis','cyanobacteria and oxygenic photosynthesis'],
'U3-L24':['leaf photosynthesis','stomata','mesophyll','carbon dioxide','water vapor'],
'U3-L25':['chloroplast','stroma','thylakoid','grana','light reactions','carbon fixation'],
'U3-L26':['photosynthesis equation as model','photosynthetic oxygen comes from water','photosynthesis as redox','light reactions and calvin cycle','water is oxidized','carbon dioxide is ultimately reduced'],
'U3-L27':['photon','wavelength','shorter wavelength','higher-energy photon','pigment absorption and reflection'],
'U3-L28':['light excitation of chlorophyll','chlorophyll a','chlorophyll b','carotenoids','accessory pigments'],
'U3-L29':['photosystem','reaction center','light-harvesting complex','excitation-energy transfer','same electron is not passed'],
'U3-L30':['photosystem ii','water supplies psii electrons','water-splitting products','protons into the thylakoid lumen','molecular oxygen'],
'U3-L31':['photosystem linkage','thylakoid proton gradient','electron transport chain','higher proton concentration','etc locations across life'],
'U3-L32':['photosystem i','nadph formation','p680 and p700 reaction-center labels','nadp⁺','reducing power'],
'U3-L33':['photophosphorylation','light-reaction energy products','light-reaction inputs and outputs','electrochemical proton gradient','atp synthase','nadph'],
}
prohibited=('ppt','ced','campbell','college board','canonical record','source material','teacher deck','teacher test','review flag','spatial encoding','layout job','locked definition','audit label','the packet')
assigned=[]; wc=[]
for s,b in zip(j['scenes'],f3j4):
    assert s['object_ids']==b['knowledge_ids']; assigned+=s['object_ids']
    assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
    assert all(len(z['description'])>=70 for z in s['scene_layout']['zones'])
    assert len(s['scene_layout']['orientation'])>=120
    assert len(s['cast'])>=4 and s['cast'][0]['name']=='Dr. Nia Park'
    assert all(c['name'] and len(c['visual'])>=20 and len(c['job'])>=20 for c in s['cast'])
    prose=' '.join(s['story_paragraphs']); words=re.findall(r"\b[\w’'-]+\b",prose); wc.append(len(words))
    assert len(words)>=340,(s['locus'],len(words)); assert len(s['story_paragraphs'])>=4; assert len(s['story_close'])>=80
    low=prose.lower().replace('**','')
    hits=[x for x in prohibited if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',low)]
    assert not hits,(s['locus'],hits)
    for term in required[b['locus_id']]: assert term in low,(s['locus'],term)
    assert len(s['story_beats'])==len(b['term_introductions'])
    for beat,t in zip(s['story_beats'],b['term_introductions']):
        assert beat['object_id']==t['knowledge_id']
        assert beat['science']==t['canonical_science']==canon[t['knowledge_id']]['canonical_verified_statement']
        assert beat['exact_name']==t['exact_name_recall']; assert beat['term'] and len(beat['hint'])>=20
        if t['exact_name_recall']:
            assert t['canonical_term'].lower() in low,(s['locus'],t['canonical_term'])
    assert s['misconception_guards']==b['misconception_guards']; assert s['carry_forward']==b['carry_forward']
    exp=f3j4[s['scene_index']+1]['scene_title'] if s['scene_index']+1<len(f3j4) else None
    assert s['next_locus']==exp
    if s['checkpoint']:
        assert s['checkpoint_prompt'] and s['checkpoint_answer'] and len(s['checkpoint_hint'])>=70

assert len(assigned)==len(set(assigned))==44
assert set(assigned)=={kid for b in f3j4 for kid in b['knowledge_ids']}
assert sum(bool(s['checkpoint']) for s in j['scenes'])==4
assert min(wc)>=340 and statistics.mean(wc)>=360
assert j['guide']['name']=='Dr. Nia Park'
assert 'twelve-station route' in j['route_orientation']
assert len(j['premise'])>=120 and len(j['mission'])>=100 and len(j['finale'])>=180

# High-risk photosynthesis guards must be explicit in polished student prose.
ant=' '.join(j['scenes'][7]['story_paragraphs']).lower()
redox=' '.join(j['scenes'][4]['story_paragraphs']).lower()
psii=' '.join(j['scenes'][8]['story_paragraphs']).lower()
etc=' '.join(j['scenes'][9]['story_paragraphs']).lower()
psi=' '.join(j['scenes'][10]['story_paragraphs']).lower()
atp=' '.join(j['scenes'][11]['story_paragraphs']).lower()
assert 'same electron is not passed from antenna pigment to antenna pigment' in ant
assert 'photosynthetic oxygen comes from water' in redox
assert 'co₂ gas released' not in redox and 'co2 gas released' not in redox
assert 'water is oxidized' in redox and 'carbon dioxide is ultimately reduced' in redox
assert 'releases protons into the thylakoid lumen' in psii
assert 'electron does not become atp' in j['scenes'][9]['scene_kicker'].lower()
assert 'higher proton concentration in the thylakoid lumen than in the stroma' in etc
assert 'p680' in psi and 'p700' in psi and 'not additional photosystems' in psi
assert 'a photon is not about to spin this enzyme' in atp
assert 'immediate driver now is the electrochemical proton gradient' in atp

# Historical Unit 3 narrative stage locks stay intact.
for lockname in ('content-lock-f4a.json','content-lock-f4b.json','content-lock-f4c.json'):
    old=read(U3/lockname)
    for rel,digest in old['files'].items():
        p=U3/rel; assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest
for rel,digest in lock['files'].items():
    p=U3/rel; assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest

print('UNIT3 F4D QA PASS')
print(json.dumps({'journey':'U3-J4','scenes':12,'knowledge_records':44,'optional_recalls':4,'story_words':sum(wc),'average_scene_words':round(statistics.mean(wc),1),'min_scene_words':min(wc),'polished_journeys_total':4,'polished_scenes_total':33,'student_release':False,'preview_release':True},indent=2))
