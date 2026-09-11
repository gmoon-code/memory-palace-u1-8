from __future__ import annotations
import json, hashlib, re, statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
source=read(U2/'source/canonical-unit2-f1.json')
canon={r['knowledge_id']:r for r in source['canonical_catalog']}
f3=read(U2/'briefs/scene-briefs-f3.json')
f3j1=[b for b in f3['scene_briefs'] if b['journey_id']=='U2-J1']
journey=read(U2/'journeys/U2-J1.json')
registry=read(U2/'journeys-f4a.json')
status=read(U2/'status-f4a.json')
lock=read(U2/'content-lock-f4a.json')

assert journey['palace_id']=='U2-J1'
assert journey['scene_count']==len(journey['scenes'])==13
assert journey['checkpoint_count']==4
assert registry['journey_count']==1 and registry['scene_count']==13 and registry['checkpoint_count']==4
assert status['polished_journeys']==1 and status['polished_scenes']==13 and status['student_release'] is False and status['preview_release'] is True

route=[b['locus_id'] for b in f3j1]
assert route==[b['locus_id'] for b in f3j1]
assert [s['locus'] for s in journey['scenes']]==[b['scene_title'] for b in f3j1]
assigned=[]
word_counts=[]
prohibited=(
 'ppt','ced','campbell','college board','locked definition','canonical record','source material','class notes','the packet',
 'spatial encoding','layout job','fixed visual zone','must remain visible','source-facing','teacher deck'
)
# Scientific terms that must appear in the prose of each scene. These are student-facing concepts, not internal record labels.
required={
'U2-L01':['cell','prokaryotic cell','eukaryotic cell','nucleoid region','plasma membrane','cytosol','ribosomes'],
'U2-L02':['nucleus','nuclear envelope','nuclear pore complex','chromosomes'],
'U2-L03':['nucleolus','rrna','ribosomes','ribosomal subunits','common ancestry'],
'U2-L04':['ribosome','messenger rna','free ribosome','rough er','protein'],
'U2-L05':['endomembrane system','nuclear envelope','endoplasmic reticulum','golgi complex','lysosomes','vacuoles','plasma membrane'],
'U2-L06':['rough er','cisterna','er lumen','ribosomes','transport vesicle'],
'U2-L07':['smooth er','lipid synthesis','detoxification','calcium','carbohydrate metabolism'],
'U2-L08':['golgi','cisterna','cis face','er'],
'U2-L09':['golgi','trans face','modify','sort','package','vesicle'],
'U2-L10':['lysosome','autophagy','hydrolytic enzymes','apoptosis'],
'U2-L11':['vacuoles','central vacuole','turgor pressure','food vacuole','contractile vacuole'],
'U2-L12':['peroxisome','hydrogen peroxide','catalase','oxidative'],
'U2-L13':['cytoskeleton','microtubules','centrosome','microfilaments','actin','intermediate filaments','mitotic spindle']
}
for s,b in zip(journey['scenes'],f3j1):
    assert s['object_ids']==b['knowledge_ids']
    assigned+=s['object_ids']
    assert len(s['scene_layout']['zones'])==3
    assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
    assert all(len(z['description'])>=55 for z in s['scene_layout']['zones'])
    assert len(s['scene_layout']['orientation'])>=100
    assert len(s['cast'])>=3 and s['cast'][0]['name']=='Dr. Nia Park'
    assert all(c['name'] and len(c['visual'])>=10 and len(c['job'])>=10 for c in s['cast'])
    prose=' '.join(s['story_paragraphs'])
    words=re.findall(r"\b[\w’'-]+\b",prose)
    word_counts.append(len(words))
    assert len(words)>=220, (s['locus'],len(words))
    assert len(s['story_paragraphs'])>=4
    assert len(s['story_close'])>=70
    low=prose.lower().replace('**','')
    hits=[x for x in prohibited if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',low)]
    assert not hits,(s['locus'],hits)
    for term in required[b['locus_id']]:
        assert term in low,(s['locus'],term)
    assert len(s['story_beats'])==len(b['term_introductions'])
    for beat,t in zip(s['story_beats'],b['term_introductions']):
        assert beat['object_id']==t['knowledge_id']
        assert beat['science']==t['canonical_science']==canon[t['knowledge_id']]['canonical_verified_statement']
        assert beat['exact_name']==t['exact_name_recall']
        assert beat['term'] and beat['hint']
    assert s['misconception_guards']==b['misconception_guards']
    assert s['carry_forward']==b['carry_forward']
    expected_next=f3j1[s['scene_index']+1]['scene_title'] if s['scene_index']+1<len(f3j1) else None
    assert s['next_locus']==expected_next
    if s['checkpoint']:
        assert s['checkpoint_prompt'] and s['checkpoint_answer'] and s['checkpoint_hint']
        assert len(s['checkpoint_hint'])>=40

assert len(assigned)==len(set(assigned))==38
assert set(assigned)=={kid for b in f3j1 for kid in b['knowledge_ids']}
assert sum(bool(s['checkpoint']) for s in journey['scenes'])==4
assert min(word_counts)>=220 and statistics.mean(word_counts)>=250
assert journey['guide']['name']=='Dr. Nia Park'
assert 'transparent eukaryotic-cell facility' in journey['route_orientation']
assert len(journey['premise'])>=100 and len(journey['mission'])>=80 and len(journey['finale'])>=120

for rel,digest in lock['files'].items():
    p=U2/rel
    assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest

print('UNIT2 F4A QA PASS')
print(json.dumps({'journey':'U2-J1','scenes':13,'knowledge_records':38,'optional_recalls':4,'story_words':sum(word_counts),'average_scene_words':round(statistics.mean(word_counts),1),'min_scene_words':min(word_counts),'student_release':False,'preview_release':True},indent=2))
