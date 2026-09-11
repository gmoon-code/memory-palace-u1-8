from __future__ import annotations
import json, hashlib, re, statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
source=read(U2/'source/canonical-unit2-f1.json'); canon={r['knowledge_id']:r for r in source['canonical_catalog']}
f3=read(U2/'briefs/scene-briefs-f3.json'); briefs=[b for b in f3['scene_briefs'] if b['journey_id']=='U2-J4']
j=read(U2/'journeys/U2-J4.json'); reg=read(U2/'journeys-f4d.json'); status=read(U2/'status-f4d.json'); lock=read(U2/'content-lock-f4d.json')
assert j['palace_id']=='U2-J4' and j['scene_count']==len(j['scenes'])==8 and j['checkpoint_count']==3
assert reg['journey_count']==4 and reg['scene_count']==29 and reg['checkpoint_count']==10
assert [x['palace_id'] for x in reg['guided_journeys']]==['U2-J1','U2-J2','U2-J3','U2-J4']
assert status['polished_journeys']==4 and status['polished_scenes']==29 and status['student_release'] is False and status['preview_release'] is True
assert [s['locus'] for s in j['scenes']]==[b['scene_title'] for b in briefs]
required={
'U2-L22':['amphipathic','polar','hydrophilic','nonpolar','hydrophobic','phospholipid bilayer','bilayer orientation'],
'U2-L23':['fluid mosaic model','phospholipids','proteins','cholesterol','glycolipids','glycoproteins','laterally'],
'U2-L24':['unsaturated','cis double-bond','kink','cholesterol','fluidity buffer','higher temperatures','lower temperatures'],
'U2-L25':['integral membrane protein','transmembrane protein','peripheral membrane protein','hydrophobic','hydrophilic'],
'U2-L26':['glycolipid','glycoprotein','carbohydrate','lipid','protein','cell-cell recognition'],
'U2-L27':['selective permeability','hydrophobic barrier','nonpolar','ion','h₂o'],
'U2-L28':['small nonpolar','small uncharged polar','ions and large polar molecules','o₂','co₂','h₂o','nh₃','na⁺','k⁺','glucose'],
'U2-L29':['cell wall','cellulose microfibrils','plasma membrane','plasmodesma','plasmodesmata','selective boundary']
}
prohibited=('ppt','ced','campbell','college board','locked definition','canonical record','source material','class notes','the packet','spatial encoding','layout job','fixed visual zone','must remain visible','source-facing','teacher deck','worksheet')
assigned=[]; wc=[]
for s,b in zip(j['scenes'],briefs):
    assert s['object_ids']==b['knowledge_ids']; assigned += s['object_ids']
    assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
    assert all(len(z['description'])>=85 for z in s['scene_layout']['zones'])
    assert len(s['scene_layout']['orientation'])>=110
    assert len(s['cast'])>=4 and s['cast'][0]['name']=='Dr. Nia Park'
    assert all(c['name'] and len(c['visual'])>=18 and len(c['job'])>=18 for c in s['cast'])
    prose=' '.join(s['story_paragraphs']); words=re.findall(r"\b[\w’'+₂⁺-]+\b",prose); wc.append(len(words))
    assert len(words)>=320,(s['locus'],len(words)); assert len(s['story_paragraphs'])>=5; assert len(s['story_close'])>=100
    low=prose.lower().replace('**','')
    hits=[x for x in prohibited if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',low)]
    assert not hits,(s['locus'],hits)
    for term in required[b['locus_id']]: assert term in low,(s['locus'],term)
    assert len(s['story_beats'])==len(b['term_introductions'])
    for beat,t in zip(s['story_beats'],b['term_introductions']):
        assert beat['object_id']==t['knowledge_id']; assert beat['science']==t['canonical_science']==canon[t['knowledge_id']]['canonical_verified_statement']; assert beat['exact_name']==t['exact_name_recall']; assert beat['term'] and len(beat['hint'])>=35
    assert s['misconception_guards']==b['misconception_guards']; assert s['carry_forward']==b['carry_forward']
    expected=briefs[s['scene_index']+1]['scene_title'] if s['scene_index']+1<len(briefs) else None
    assert s['next_locus']==expected
    if s['checkpoint']:
        assert s['checkpoint_prompt'] and s['checkpoint_answer'] and len(s['checkpoint_hint'])>=90
assert len(assigned)==len(set(assigned))==21
assert set(assigned)=={kid for b in briefs for kid in b['knowledge_ids']}
assert sum(bool(s['checkpoint']) for s in j['scenes'])==3
assert min(wc)>=320 and statistics.mean(wc)>=380
assert j['guide']['name']=='Dr. Nia Park' and 'traveler tray' in j['route_orientation'].lower() and 'plant cell wall' in j['route_orientation'].lower()
assert len(j['premise'])>=100 and len(j['mission'])>=80 and len(j['finale'])>=180
# Continuity object appears across the journey and chemistry, not an intentional guard, explains selective passage.
whole=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).lower().replace('**','')
assert whole.count('traveler tray')>=6
assert 'membrane has not rejected the ion on purpose' in whole
assert 'some integral proteins are transmembrane. not all integral proteins are' in whole
assert 'cholesterol is not an “always more fluid” switch' in whole
assert 'water cannot cross' in whole  # appears only as an explicitly rejected misconception
for rel,digest in lock['files'].items():
    p=U2/rel; assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest
print('UNIT2 F4D QA PASS')
print(json.dumps({'journey':'U2-J4','scenes':8,'knowledge_records':21,'optional_recalls':3,'story_words':sum(wc),'average_scene_words':round(statistics.mean(wc),1),'min_scene_words':min(wc),'polished_journeys_total':4,'student_release':False,'preview_release':True},indent=2))
