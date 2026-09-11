from __future__ import annotations
import json,re,statistics,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; U3=ROOT/'content/ap-biology/unit-3'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
canon={r['knowledge_id']:r for r in read(U3/'source/canonical-unit3-f1.json')['canonical_catalog']}
briefs=read(U3/'briefs/scene-briefs-f3.json')['scene_briefs']
f3=[b for b in briefs if b['journey_id']=='U3-J6']
j=read(U3/'journeys/U3-J6.json'); lock=read(U3/'content-lock-f4f.json')
assert j['schema']=='memory-palace-v2-unit3-f4f-story-1.0'
assert j['scene_count']==len(j['scenes'])==12 and j['checkpoint_count']==3
assert j['student_release']=='PILOT_PREVIEW_F4F'
assert [s['locus'] for s in j['scenes']]==[b['scene_title'] for b in f3]

required={
'U3-L39':['respiration and atp synthesis','aerobic respiration as coordinated pathway','glycolysis','pyruvate oxidation','citric acid cycle','oxidative phosphorylation','c₆h₁₂o₆ + 6 o₂','carbohydrates, fats, and proteins','oxidized','oxygen is ultimately reduced'],
'U3-L40':['glycolysis outputs','cytosol','two three-carbon pyruvate','two atp','four atp','net gain is two atp','substrate-level phosphorylation','direct enzymatic phosphate transfer','no co₂ vent opens here'],
'U3-L41':['nad+ and nadh','fad and fadh2','citric acid cycle','not a claim that glycolysis just produced fadh₂','electron carrier'],
'U3-L42':['pyruvate oxidation and krebs inputs','pyruvate oxidation','acetyl-coa','co₂','nadh','two-carbon acetyl group','fADH₂'.lower()],
'U3-L43':['krebs-cycle location and outputs','citric acid cycle','mitochondrial matrix','4 co₂','2 atp','6 nadh','2 fadh₂','detailed intermediate'],
'U3-L44':['cristae and atp-production surface','mitochondrial structural review','intermembrane space','inner mitochondrial membrane','matrix','glycolysis remains outside the mitochondrion'],
'U3-L45':['respiratory electron transfer','reduced coenzymes feed etc','respiratory electron transport chain','nadh','fadh₂','terminal acceptor','fermentation'],
'U3-L46':['mitochondrial proton gradient','matrix-intermembrane ph difference','respiratory proton pumping','matrix across the inner membrane into the intermembrane space','higher proton concentration','matrix is higher in ph'],
'U3-L47':['oxygen terminal reduction','terminal electron acceptor','o₂ + 4 e⁻ + 4 h⁺ → 2 h₂o','atp counter, which remains unchanged'],
'U3-L48':['oxidative phosphorylation','oxidative phosphorylation components','chemiosmosis','atp synthase','proton-motive force','rotational and conformational changes','26 to 28 atp','30 to 32 atp','does not show a fixed universal integer'],
'U3-L49':['respiratory uncoupling and heat','bypass','heat','atp-production efficiency falls','proton leak'],
'U3-L50':['prokaryotic respiratory membrane','plasma membrane','no mitochondrial organelle','proton-translocation','cytoplasm','fermentation waits for journey 7'],
}
prohibited=('ppt','ced','campbell','college board','canonical record','source material','teacher deck','teacher test','review flag','spatial encoding','layout job','locked definition','audit label','the packet')
assigned=[]; wc=[]
for s,b in zip(j['scenes'],f3):
    assert s['object_ids']==b['knowledge_ids']; assigned+=s['object_ids']
    assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
    assert all(len(z['description'])>=100 for z in s['scene_layout']['zones'])
    assert len(s['scene_layout']['orientation'])>=120
    assert len(s['cast'])>=4 and s['cast'][0]['name']=='Dr. Nia Park'
    assert all(c['name'] and len(c['visual'])>=35 and len(c['job'])>=35 for c in s['cast'])
    prose=' '.join(s['story_paragraphs']); words=re.findall(r"\b[\w’'₂₄⁺⁻-]+\b",prose); wc.append(len(words))
    assert len(words)>=350,(s['locus'],len(words)); assert len(s['story_paragraphs'])>=4; assert len(s['story_close'])>=100
    low=prose.lower().replace('**','')
    hits=[x for x in prohibited if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',low)]
    assert not hits,(s['locus'],hits)
    for term in required[b['locus_id']]: assert term in low,(s['locus'],term)
    assert len(s['story_beats'])==len(b['term_introductions'])
    for beat,t in zip(s['story_beats'],b['term_introductions']):
        assert beat['object_id']==t['knowledge_id']
        assert beat['science']==t['canonical_science']==canon[t['knowledge_id']]['canonical_verified_statement']
        assert beat['exact_name']==t['exact_name_recall']
        assert beat['term'] and len(beat['hint'])>=25
        if t['exact_name_recall']: assert t['canonical_term'].lower() in low,(s['locus'],t['canonical_term'])
    assert s['misconception_guards']==b['misconception_guards']; assert s['carry_forward']==b['carry_forward']
    exp=f3[s['scene_index']+1]['scene_title'] if s['scene_index']+1<len(f3) else None
    assert s['next_locus']==exp
    if s['checkpoint']:
        assert s['checkpoint_prompt'] and s['checkpoint_answer'] and len(s['checkpoint_hint'])>=80

assert len(assigned)==len(set(assigned))==35
assert set(assigned)=={kid for b in f3 for kid in b['knowledge_ids']}
assert sum(bool(s['checkpoint']) for s in j['scenes'])==3
assert min(wc)>=350 and statistics.mean(wc)>=400 and sum(wc)>=4800
assert j['guide']['name']=='Dr. Nia Park'
assert 'twelve-station' in j['route_orientation']
assert len(j['premise'])>=120 and len(j['mission'])>=100 and len(j['finale'])>=200

# High-risk causal guards in polished prose.
intake=' '.join(j['scenes'][0]['story_paragraphs']).lower()
gly=' '.join(j['scenes'][1]['story_paragraphs']).lower()
carrier=' '.join(j['scenes'][2]['story_paragraphs']).lower()
airlock=' '.join(j['scenes'][3]['story_paragraphs']).lower()
arch=' '.join(j['scenes'][5]['story_paragraphs']).lower()
etc=' '.join(j['scenes'][6]['story_paragraphs']).lower()
pump=' '.join(j['scenes'][7]['story_paragraphs']).lower()
o2=' '.join(j['scenes'][8]['story_paragraphs']).lower()
turb=' '.join(j['scenes'][9]['story_paragraphs']).lower()
heat=' '.join(j['scenes'][10]['story_paragraphs']).lower()
prok=' '.join(j['scenes'][11]['story_paragraphs']).lower()
assert 'accounting, not choreography' in intake
assert 'blue electron tracer therefore has its own route' in intake and 'amber carbon tracer has another' in intake
assert 'no co₂ vent opens here' in gly and 'cytosol' in gly
assert 'not a claim that glycolysis just produced fadh₂' in carrier
assert 'the airlock therefore does not get credit for fadh₂' in airlock
assert 'glycolysis remains outside the mitochondrion in the cytosol' in arch
assert 'it does not move toward an atp molecule' in etc
assert 'electrons are not pumped into the intermembrane space' in pump
assert 'oxygen does not donate atp' in o2
assert 'the protons do not become phosphate groups or atp molecules' in turb
assert 'does not show a fixed universal integer' in turb
assert 'atp-production efficiency falls' in heat
assert 'no mitochondrial organelle' in prok and 'prokaryotic respiratory membrane' in prok

# Student-visible memory anchors must remove source-management phrasing from enrichment bookkeeping.
for s in j['scenes']:
    for x in s['memory_snapshot']:
        meaning=(x.get('meaning') or '').lower()
        assert 'teacher-taught' not in meaning
        assert 'modern textbook estimates' not in meaning

# Preserve every historical Unit 3 stage lock through F4E.
for lockname in ('content-lock-f4a.json','content-lock-f4b.json','content-lock-f4c.json','content-lock-f4d.json','content-lock-f4e.json'):
    old=read(U3/lockname)
    for rel,digest in old['files'].items():
        p=U3/rel; assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,(lockname,rel)
for rel,digest in lock['files'].items():
    p=U3/rel; assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest

print('UNIT3 F4F QA PASS')
print(json.dumps({'journey':'U3-J6','scenes':12,'knowledge_records':35,'optional_recalls':3,'story_words':sum(wc),'average_scene_words':round(statistics.mean(wc),1),'min_scene_words':min(wc),'polished_journeys_total':6,'polished_scenes_total':50,'student_release':False,'preview_release':True},indent=2))
