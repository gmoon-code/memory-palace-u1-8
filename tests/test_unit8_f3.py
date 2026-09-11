import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; U8=ROOT/'content/ap-biology/unit-8'
read=lambda p: json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit8_f3_accounting_and_runtime_boundary():
    d=read(U8/'briefs/scene-briefs-f3.json')
    assert d['counts']=={'journeys':8,'scene_briefs':58,'palace_managed_records':211,'term_introductions':211,'optional_first_exposure_recalls':18}
    assigned=[k for b in d['scene_briefs'] for k in b['knowledge_ids']]
    assert len(assigned)==len(set(assigned))==211
    s=read(U8/'status-f3.json')
    assert s['student_release'] is False
    assert (s['journey_count'],s['scene_count'],s['memory_objects'],s['application_challenges'])==(0,0,0,0)

def test_unit8_f3_preserves_f1_f2_science_and_visuals():
    d=read(U8/'briefs/scene-briefs-f3.json')['scene_briefs']
    a=read(U8/'architecture/palace-architecture-f2.json')['loci']
    c={r['Knowledge ID']:r for r in read(U8/'canonical-catalog.json')}
    for b,l in zip(d,a):
        assert b['locus_id']==l['locus_id']
        assert b['knowledge_ids']==[l['primary_knowledge_id']]+l['embedded_knowledge_ids']
        assert b['visual_spec']['visual_mode']==l['scientific_visual']
        assert b['f2_spatial_anchor']==l['spatial_anchor']
        assert len(b['stable_cast'])==3 and len(b['science_bearing_action']['during'])==3
        for t in b['term_introductions']:
            assert t['canonical_term']==c[t['knowledge_id']]['Canonical Label']
            assert t['canonical_science']==c[t['knowledge_id']]['Canonical Verified Statement']

def test_unit8_f3_journey_routes_and_recall_sparsity():
    j=read(U8/'briefs/journey-briefs-f3.json')['journeys']
    a=read(U8/'architecture/palace-architecture-f2.json')['journeys']
    assert [x['route'] for x in j]==[x['route'] for x in a]
    scenes=read(U8/'briefs/scene-briefs-f3.json')['scene_briefs']
    per={f'U8-J{i}':0 for i in range(1,9)}
    for b in scenes:
        if b['quick_recall']['enabled']: per[b['journey_id']]+=1
    assert per=={'U8-J1':2,'U8-J2':3,'U8-J3':2,'U8-J4':2,'U8-J5':2,'U8-J6':3,'U8-J7':2,'U8-J8':2}
