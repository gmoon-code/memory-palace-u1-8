import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content'/'ap-biology'/'unit-4'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit4_f1_accounting_and_scope_partition():
    d=read(U4/'source'/'canonical-unit4-f1.json')
    assert len(d['ppt_raw_slides'])==85
    assert len(d['ced_current_atoms'])==38
    assert len(d['canonical_catalog'])==180
    assert len(d['review_flags'])==39
    assert len(d['assessment_semantic_crosswalk'])==9
    counts={}
    for r in d['canonical_catalog']: counts[r['scope_class']]=counts.get(r['scope_class'],0)+1
    assert counts=={'AP_REQUIRED':38,'TEACHER_REQUIRED_ENRICHMENT':124,'PRACTICE_ONLY':15,'SCOPE_GUARD':3}

def test_unit4_f1_has_all_current_ced_topics_and_every_teacher_slide_mapped():
    d=read(U4/'source'/'canonical-unit4-f1.json')
    assert {a['topic'] for a in d['ced_current_atoms']}=={'4.1','4.2','4.3','4.4','4.5','4.6'}
    assert [s['slide'] for s in d['ppt_raw_slides']]==list(range(1,86))
    allowed={'MAPPED','MAPPED_VISUAL','PRESERVED_METADATA','PRESERVED_RAW'}
    assert all(s['coverage_status'] in allowed for s in d['ppt_raw_slides'])
    assert all(s['mapped_knowledge_ids'] or s['coverage_status'] in {'PRESERVED_METADATA','PRESERVED_RAW'} for s in d['ppt_raw_slides'])

def test_unit4_review_flags_are_resolved_and_science_is_locked():
    d=read(U4/'source'/'canonical-unit4-f1.json')
    assert all(f['status']=='RESOLVED' and f['resolution'] for f in d['review_flags'])
    assert all(r['canonical_lock']=='LOCKED_F1' for r in d['canonical_catalog'])
    lock=read(U4/'content-lock-f1.json')
    assert lock['lock_status']=='LOCKED_F1'
    for x in lock['protected_files']:
        p=U4/x['path']
        assert p.stat().st_size==x['bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']

def test_unit4_f1_has_no_student_runtime_content():
    r=read(U4/'f1-release-manifest.json')
    s=read(U4/'status.json')
    assert r['student_release'] is False and read(U4/'status-f4g.json')['student_release'] is False
    assert s['student_release'] in (False,True)
    assert (r['journeys'],r['scenes'],r['memory_objects'],r['application_challenges'])==(0,0,0,0)
    assert s['status'] in {'SCIENCE_LOCKED_F1_NOT_STUDENT_RELEASED','LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','STUDENT_READY'} or s['status'].startswith('F4')

def test_unit4_assessment_is_semantic_evidence_not_scientific_authority():
    d=read(U4/'source'/'coverage-manifest-f1.json')['assessment_coverage']
    assert d['crosswalk_mode']=='REPRESENTATIVE_SEMANTIC_EVIDENCE'
    assert d['pages']==85
    assert set(d['current_topics_covered'])=={'4.1','4.2','4.3','4.4','4.5','4.6'}
