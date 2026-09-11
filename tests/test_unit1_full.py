import json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U1=ROOT/'content'/'ap-biology'/'unit-1'

def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))

def test_story_coverage_and_practice_only_partition():
    mos=read(U1/'memory-objects.json')['memory_objects']
    all_ids={o['memory_object_id'] for o in mos}
    story=[]
    for i in range(1,10):
        j=read(U1/'journeys'/f'Z{i}.json')
        for s in j['scenes']: story.extend(s['object_ids'])
    assert len(story)==199
    assert len(set(story))==199
    lab=read(U1/'application-lab.json')
    practice=set(lab['practice_only_runtime_object_ids'])
    assert len(practice)==8
    assert set(story)|practice==all_ids
    assert set(story)&practice==set()

def test_every_scene_has_clear_geometry_cast_and_substantive_story():
    for i in range(1,10):
        j=read(U1/'journeys'/f'Z{i}.json')
        assert len(j['route'])==len(j['scenes'])
        for idx,s in enumerate(j['scenes']):
            assert s['scene_index']==idx
            assert s['locus']==j['route'][idx]['locus']
            assert len(s['location_description'].split())>=16
            assert len(s['scene_layout']['orientation'].split())>=10
            zones=s['scene_layout']['zones']
            assert len(zones)==3
            assert {z['position'] for z in zones}=={'left','center','right'}
            assert all(z['label'] and z['description'] for z in zones)
            assert len(s['cast'])>=2
            assert all(c['name'] and c['visual'] and c['job'] for c in s['cast'])
            paragraphs=s['story_paragraphs']
            assert len(paragraphs)>=3
            words=len(re.findall(r"\b[\w’'-]+\b",' '.join(paragraphs)))
            assert words>=130,(j['palace_id'],idx,s['locus'],words)

def test_exact_name_targets_are_introduced_in_story_text():
    mos={o['memory_object_id']:o for o in read(U1/'memory-objects.json')['memory_objects']}
    for i in range(1,10):
        j=read(U1/'journeys'/f'Z{i}.json')
        for s in j['scenes']:
            text=' '.join(s['story_paragraphs']).casefold()
            for oid in s['object_ids']:
                o=mos[oid]
                if str(o.get('exact_name_required','')).upper()=='YES':
                    assert o['canonical_term'].casefold() in text,(j['palace_id'],s['locus'],oid,o['canonical_term'])

def test_no_source_management_language_in_student_visible_story_or_practice():
    banned=re.compile(r'\b(PPT|CED|College Board|Campbell|course notes|class notes|classroom source|source material|locked definition|canonical record|teacher material|the packet)\b',re.I)
    for i in range(1,10):
        j=read(U1/'journeys'/f'Z{i}.json')
        for s in j['scenes']:
            visible=json.dumps({
              'title':s['title'],'kicker':s['scene_kicker'],'location':s['location_description'],
              'layout':s['scene_layout'],'cast':s['cast'],'story':s['story_paragraphs'],
              'snapshot':s['memory_snapshot'],'prompt':s['checkpoint_prompt']
            },ensure_ascii=False)
            assert not banned.search(visible),(j['palace_id'],s['locus'],banned.search(visible).group(0) if banned.search(visible) else '')
    lab=read(U1/'application-lab.json')
    for x in lab['items']:
        visible=' '.join([x['title'],x['prompt'],x['answer_guide'],x['story_hint']])
        assert not banned.search(visible),(x['challenge_id'],banned.search(visible).group(0) if banned.search(visible) else '')
