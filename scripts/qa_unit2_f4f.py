from __future__ import annotations
import json, hashlib, re, statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
source=read(U2/'source/canonical-unit2-f1.json'); canon={r['knowledge_id']:r for r in source['canonical_catalog']}
f3=read(U2/'briefs/scene-briefs-f3.json'); briefs=[b for b in f3['scene_briefs'] if b['journey_id']=='U2-J6']
j=read(U2/'journeys/U2-J6.json'); reg=read(U2/'journeys-f4f.json'); status=read(U2/'status-f4f.json'); lock=read(U2/'content-lock-f4f.json')

assert j['palace_id']=='U2-J6' and j['scene_count']==len(j['scenes'])==6 and j['checkpoint_count']==2
assert reg['journey_count']==6 and reg['scene_count']==45 and reg['checkpoint_count']==15
assert [x['palace_id'] for x in reg['guided_journeys']]==['U2-J1','U2-J2','U2-J3','U2-J4','U2-J5','U2-J6']
assert status['polished_journeys']==6 and status['polished_scenes']==45 and status['student_release'] is False and status['preview_release'] is True
assert [s['locus'] for s in j['scenes']]==[b['scene_title'] for b in briefs]

required={
'U2-L40':['hypotonic','isotonic','hypertonic','relative to the cell','tonicity','water gain','water loss'],
'U2-L41':['isotonic solution','no net water movement','both directions','motion'],
'U2-L42':['hypertonic','loses water','animal cell','shrink','does not mean every cell dies instantly'],
'U2-L43':['hypotonic','turgid','turgor pressure','plasmolysis','plasma membrane','cell wall'],
'U2-L44':['water potential','osmosis','higher water potential','lower water potential','selectively permeable membrane','osmolarity','homeostasis'],
'U2-L45':['ψ = ψp + ψs','ψs = −icrt','pressure potential','solute potential','osmoregulation','negative sign','atmospheric pressure']
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
    assert len(words)>=320,(s['locus'],len(words)); assert len(s['story_paragraphs'])>=5; assert len(s['story_close'])>=110
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

assert len(assigned)==len(set(assigned))==16
assert set(assigned)=={kid for b in briefs for kid in b['knowledge_ids']}
assert sum(bool(s['checkpoint']) for s in j['scenes'])==2
assert min(wc)>=320 and statistics.mean(wc)>=390
assert j['guide']['name']=='Dr. Nia Park'
assert 'reference cell' in j['route_orientation'].lower() or 'tonicity orientation hall' in j['route_orientation'].lower()
assert 'water-potential' in j['route_orientation'].lower() and 'control loft' in j['route_orientation'].lower()
assert len(j['premise'])>=100 and len(j['mission'])>=80 and len(j['finale'])>=180
whole=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).lower().replace('**','')
# Narrative continuity and misconception guards.
assert whole.count('reference cell')>=5
assert 'no net movement is not the same as no movement' in whole
assert 'water loss is stressful, but shrinking does not mean every cell dies instantly' in whole
assert 'plasmolysis is therefore a water-loss response' in whole
assert 'cannot always be predicted from solute concentration alone when pressure also differs' in whole
assert 'the negative sign remains fixed' in whole
assert 'it is not always zero' in whole
assert 'ψp = +0.3 mpa' in whole and 'ψs = −0.7 mpa' in whole and 'ψ = −0.4 mpa' in whole
for rel,digest in lock['files'].items():
    p=U2/rel; assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest

print('UNIT2 F4F QA PASS')
print(json.dumps({'journey':'U2-J6','scenes':6,'knowledge_records':16,'optional_recalls':2,'story_words':sum(wc),'average_scene_words':round(statistics.mean(wc),1),'min_scene_words':min(wc),'polished_journeys_total':6,'student_release':False,'preview_release':True},indent=2))
