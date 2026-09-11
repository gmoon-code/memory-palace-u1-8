import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
UNIT=ROOT/'content/ap-biology/unit-1'

def load():
    return json.loads((UNIT/'reference-journey-water.json').read_text())

def test_water_reference_journey_is_complete():
    j=load()
    assert j['palace_id']=='Z3'
    assert j['story_title']=='The Flooded Sky Hotel'
    assert j['scene_count']==11
    assert j['checkpoint_count']==3
    assert len(j['scenes'])==11
    assert len(j['route'])==11
    assert [s['scene_index'] for s in j['scenes']]==list(range(11))
    assert [s['locus'] for s in j['scenes']]==[r['locus'] for r in j['route']]

def test_water_scene_objects_exist_and_all_30_are_covered_once():
    j=load()
    objs=json.loads((UNIT/'memory-objects.json').read_text())['memory_objects']
    ids={o['memory_object_id'] for o in objs}
    used=[]
    for scene in j['scenes']:
        assert set(scene['object_ids']) <= ids
        used.extend(scene['object_ids'])
        if scene['checkpoint']:
            assert scene['checkpoint_object_id'] in ids
    assert len(used)==30
    assert len(set(used))==30

def test_every_scene_has_clear_spatial_layout_cast_and_story():
    j=load()
    for scene in j['scenes']:
        assert scene['location_description'].strip()
        layout=scene['scene_layout']
        assert layout['orientation'].strip()
        assert len(layout['zones'])==3
        assert {z['position'] for z in layout['zones']}=={'left','center','right'}
        assert all(z['label'].strip() and z['description'].strip() for z in layout['zones'])
        assert scene['cast'] and all(c['name'].strip() and c['visual'].strip() and c['job'].strip() for c in scene['cast'])
        assert len(scene['story_paragraphs'])>=3
        assert all(p.strip() for p in scene['story_paragraphs'])
        assert len(scene['memory_snapshot'])==len(scene['story_beats'])

def test_student_facing_story_has_no_source_meta_language():
    j=load()
    visible=[]
    for key in ['tagline','premise','mission','finale','learner_rule','route_orientation']:
        visible.append(str(j.get(key,'')))
    for s in j['scenes']:
        visible += [s['title'],s['scene_kicker'],s['location_description'],s['scene_layout']['orientation'],s.get('checkpoint_prompt','')]
        visible += s['story_paragraphs']
        visible += [z['description'] for z in s['scene_layout']['zones']]
        visible += [c['job'] for c in s['cast']]
        visible += [b['science'] for b in s['story_beats']]
    text='\n'.join(visible).casefold()
    for forbidden in ['the ppt','the ced','locked course','locked scientific','the source states','source says','teacher material']:
        assert forbidden not in text, forbidden
    assert not re.search(r'\bppt\b',text)
    assert not re.search(r'\bced\b',text)
    assert '..' not in text

def test_story_is_chunked_but_substantive():
    j=load()
    for s in j['scenes']:
        words=len(re.findall(r"\b[\w⁺⁻₃]+\b",' '.join(s['story_paragraphs']),flags=re.UNICODE))
        assert 120 <= words <= 260,(s['locus'],words)

def test_checkpoints_are_natural_questions():
    j=load()
    checks=[s for s in j['scenes'] if s['checkpoint']]
    assert [s['locus'] for s in checks]==['Xylem Tower','Evaporation Balcony','Buffer Gate']
    for s in checks:
        q=s['checkpoint_prompt']
        assert q.endswith('?')
        assert 'locked' not in q.casefold()
        assert 'definition' not in q.casefold()
