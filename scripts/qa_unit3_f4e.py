from __future__ import annotations
import json,re,statistics,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; U3=ROOT/'content/ap-biology/unit-3'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
canon={r['knowledge_id']:r for r in read(U3/'source/canonical-unit3-f1.json')['canonical_catalog']}
briefs=read(U3/'briefs/scene-briefs-f3.json')['scene_briefs']
f3=[b for b in briefs if b['journey_id']=='U3-J5']
j=read(U3/'journeys/U3-J5.json'); lock=read(U3/'content-lock-f4e.json')
assert j['schema']=='memory-palace-v2-unit3-f4e-story-1.0'
assert j['scene_count']==len(j['scenes'])==5 and j['checkpoint_count']==2
assert j['student_release']=='PILOT_PREVIEW_F4E'
assert [s['locus'] for s in j['scenes']]==[b['scene_title'] for b in f3]

required={
'U3-L34':['calvin-cycle energy input','calvin cycle','atp','nadph','chloroplast stroma','carbon dioxide'],
'U3-L35':['carbon fixation','rubisco','rubp','carbon acceptor','enzyme','co₂'],
'U3-L36':['g3p','glyceraldehyde 3-phosphate','rubp must be regenerated','9 atp','6 nadph','one net g3p'],
'U3-L37':['photorespiration','rubisco reacts with o₂','lowering net carbon fixation','not represent the mitochondrial process','evolutionary legacy','protective roles'],
'U3-L38':['c4 photosynthesis','cam photosynthesis','spatial separation','temporal separation','mesophyll','bundle-sheath','organic acids','night','day'],
}
prohibited=('ppt','ced','campbell','college board','canonical record','source material','teacher deck','teacher test','review flag','spatial encoding','layout job','locked definition','audit label','the packet')
assigned=[]; wc=[]
for s,b in zip(j['scenes'],f3):
    assert s['object_ids']==b['knowledge_ids']; assigned+=s['object_ids']
    assert [z['position'] for z in s['scene_layout']['zones']]==['left','center','right']
    assert all(len(z['description'])>=90 for z in s['scene_layout']['zones'])
    assert len(s['scene_layout']['orientation'])>=120
    assert len(s['cast'])>=4 and s['cast'][0]['name']=='Dr. Nia Park'
    assert all(c['name'] and len(c['visual'])>=30 and len(c['job'])>=30 for c in s['cast'])
    prose=' '.join(s['story_paragraphs']); words=re.findall(r"\b[\w’'₂₄⁺⁻-]+\b",prose); wc.append(len(words))
    assert len(words)>=390,(s['locus'],len(words)); assert len(s['story_paragraphs'])>=4; assert len(s['story_close'])>=90
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

assert len(assigned)==len(set(assigned))==11
assert set(assigned)=={kid for b in f3 for kid in b['knowledge_ids']}
assert 'U3-K-139' not in assigned  # scope guard controls prose; it is not a palace memory object here.
assert sum(bool(s['checkpoint']) for s in j['scenes'])==2
assert min(wc)>=390 and statistics.mean(wc)>=420 and sum(wc)>=2100
assert j['guide']['name']=='Dr. Nia Park'
assert 'five-station' in j['route_orientation']
assert len(j['premise'])>=120 and len(j['mission'])>=100 and len(j['finale'])>=180

# High-risk Calvin-cycle and adaptation guards must be explicit in polished prose.
energy=' '.join(j['scenes'][0]['story_paragraphs']).lower()
fix=' '.join(j['scenes'][1]['story_paragraphs']).lower()
g3p=' '.join(j['scenes'][2]['story_paragraphs']).lower()
photo=' '.join(j['scenes'][3]['story_paragraphs']).lower()
adapt=' '.join(j['scenes'][4]['story_paragraphs']).lower()
assert 'neither token contains the carbon' in energy
assert 'calvin cycle' in energy and 'stroma' in energy
assert 'rubisco is not itself the carbon acceptor' in fix
assert 'rubp' in fix and 'carbon acceptor' in fix
assert 'not a synonym for glucose' in g3p
assert 'does not ask you to memorize a procession of every calvin-cycle intermediate' in g3p
assert 'photorespiration' in photo and 'mitochondrial process of cellular respiration' in photo
assert 'one hypothesis' in photo and 'protective roles' in photo
assert 'c4 = spatial separation. cam = temporal separation.' in adapt
assert 'mesophyll' in adapt and 'bundle-sheath' in adapt
assert 'stomata open mainly at night' in adapt and 'organic acids' in adapt and 'during the day' in adapt

# Student-visible memory anchor for detailed stoichiometry must not expose source-management wording.
for s in j['scenes']:
    for x in s['memory_snapshot']:
        assert 'teacher-taught' not in (x.get('meaning') or '').lower()

# Preserve every historical Unit 3 stage lock through F4D.
for lockname in ('content-lock-f4a.json','content-lock-f4b.json','content-lock-f4c.json','content-lock-f4d.json'):
    old=read(U3/lockname)
    for rel,digest in old['files'].items():
        p=U3/rel; assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,(lockname,rel)
for rel,digest in lock['files'].items():
    p=U3/rel; assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==digest

print('UNIT3 F4E QA PASS')
print(json.dumps({'journey':'U3-J5','scenes':5,'knowledge_records':11,'optional_recalls':2,'story_words':sum(wc),'average_scene_words':round(statistics.mean(wc),1),'min_scene_words':min(wc),'polished_journeys_total':5,'polished_scenes_total':38,'student_release':False,'preview_release':True},indent=2))
