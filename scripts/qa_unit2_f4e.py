from __future__ import annotations
import json, hashlib, re, statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
source=read(U2/'source/canonical-unit2-f1.json'); canon={r['knowledge_id']:r for r in source['canonical_catalog']}
f3=read(U2/'briefs/scene-briefs-f3.json'); briefs=[b for b in f3['scene_briefs'] if b['journey_id']=='U2-J5']
j=read(U2/'journeys/U2-J5.json'); reg=read(U2/'journeys-f4e.json'); status=read(U2/'status-f4e.json'); lock=read(U2/'content-lock-f4e.json')

assert j['palace_id']=='U2-J5' and j['scene_count']==len(j['scenes'])==10 and j['checkpoint_count']==3
assert reg['journey_count']==5 and reg['scene_count']==39 and reg['checkpoint_count']==13
assert [x['palace_id'] for x in reg['guided_journeys']]==['U2-J1','U2-J2','U2-J3','U2-J4','U2-J5']
assert status['polished_journeys']==5 and status['polished_scenes']==39 and status['student_release'] is False and status['preview_release'] is True
assert [s['locus'] for s in j['scenes']]==[b['scene_title'] for b in briefs]

required={
'U2-L30':['concentration gradient','diffusion','dynamic equilibrium','passive transport','random molecular motion','net movement'],
'U2-L31':['active transport','atp','energy for active transport','active transport proteins','conformation','electrochemical'],
'U2-L32':['facilitated diffusion','facilitated diffusion proteins','large polar','down','atp'],
'U2-L33':['ion channel','channel protein','hydrophilic','gated','membrane polarization','electrochemical'],
'U2-L34':['carrier protein','binding','conformation','release','reset','open tunnel'],
'U2-L35':['aquaporins','water','large quantities','bilayer','ions'],
'U2-L36':['bulk transport','endocytosis','exocytosis','vesicle','energy','plasma membrane'],
'U2-L37':['phagocytosis','pinocytosis','receptor-mediated endocytosis','large particle','extracellular fluid','ligands','receptors'],
'U2-L38':['na⁺/k⁺ pump','membrane potential','electrogenic pump','3 na⁺ out','2 k⁺ in','one atp','net outward'],
'U2-L39':['proton pump','cotransport','sucrose-h⁺ symport','electrochemical gradient','h⁺','sucrose','symporter','atp']
}
prohibited=('ppt','ced','campbell','college board','locked definition','canonical record','source material','class notes','the packet','spatial encoding','layout job','fixed visual zone','must remain visible','source-facing','teacher deck','worksheet')
assigned=[]; wc=[]
for s,b in zip(j['scenes'],briefs):
    assert s['object_ids']==b['knowledge_ids']; assigned += s['object_ids']
    assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
    assert all(len(z['description'])>=90 for z in s['scene_layout']['zones'])
    assert len(s['location_description'])>=120
    assert len(s['scene_layout']['orientation'])>=110
    assert len(s['cast'])>=4 and s['cast'][0]['name']=='Dr. Nia Park'
    assert all(c['name'] and len(c['visual'])>=18 and len(c['job'])>=18 for c in s['cast'])
    prose=' '.join(s['story_paragraphs']); words=re.findall(r"\b[\w’'+₂⁺⁻-]+\b",prose); wc.append(len(words))
    assert len(words)>=300,(s['locus'],len(words)); assert len(s['story_paragraphs'])>=5; assert len(s['story_close'])>=110
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

assert len(assigned)==len(set(assigned))==26
assert set(assigned)=={kid for b in briefs for kid in b['knowledge_ids']}
assert sum(bool(s['checkpoint']) for s in j['scenes'])==3
assert min(wc)>=300 and statistics.mean(wc)>=340
assert j['guide']['name']=='Dr. Nia Park'
assert 'colored cargo case' in j['route_orientation'].lower()
assert 'concentration ramp' in j['route_orientation'].lower() and 'cotransport platform' in j['route_orientation'].lower()
assert len(j['premise'])>=100 and len(j['mission'])>=80 and len(j['finale'])>=180
whole=' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).lower().replace('**','')
# Continuity and conceptual guards.
assert whole.count('cargo case')>=5
assert 'motion has not stopped' in whole
assert 'does not act like the atp-powered lift' in whole
assert 'carrier never forms an open tunnel' in whole
assert 'water can cross a lipid bilayer to some extent' in whole
assert 'atp is not hydrolyzed directly at the sucrose symporter' in whole
assert 'the entire resting membrane potential reflects more than this pump alone' in whole
for rel,digest in lock['files'].items():
    p=U2/rel; assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest

print('UNIT2 F4E QA PASS')
print(json.dumps({'journey':'U2-J5','scenes':10,'knowledge_records':26,'optional_recalls':3,'story_words':sum(wc),'average_scene_words':round(statistics.mean(wc),1),'min_scene_words':min(wc),'polished_journeys_total':5,'student_release':False,'preview_release':True},indent=2))
