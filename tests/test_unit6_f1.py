import hashlib,json
from collections import Counter
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U6=ROOT/'content/ap-biology/unit-6'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))

def test_unit6_f1_accounting_and_lock():
    d=read(U6/'source/canonical-unit6-f1.json')
    assert len(d['ppt_raw_slides'])==121
    assert len(d['ced_current_atoms'])==89
    assert len(d['canonical_catalog'])==202
    assert len(d['review_flags'])==39
    assert len(d['assessment_semantic_crosswalk'])==12
    assert len(d['cross_unit_dependencies'])==5
    assert Counter(r['scope_class'] for r in d['canonical_catalog'])==Counter({'AP_REQUIRED':83,'TEACHER_REQUIRED_ENRICHMENT':78,'PRACTICE_ONLY':16,'SCOPE_GUARD':25})
    assert all(r['canonical_lock']=='LOCKED_F1' for r in d['canonical_catalog'])

def test_unit6_all_slides_preserved_and_ced_topics_complete():
    d=read(U6/'source/canonical-unit6-f1.json'); cov=read(U6/'source/coverage-manifest-f1.json')
    assert [x['slide'] for x in d['ppt_raw_slides']]==list(range(1,122))
    assert cov['ppt_coverage']['unmapped']==0
    assert {x['topic'] for x in d['ced_current_atoms']}=={'6.1','6.2','6.3','6.4','6.5','6.6','6.7','6.8'}

def test_unit6_high_risk_science_repairs_present():
    rows={r['canonical_label']:r for r in read(U6/'source/canonical-unit6-f1.json')['canonical_catalog']}
    assert '50S' in rows['Ribosomal subunit sizes']['canonical_verified_statement']
    assert 'host genome' in rows['Retroviral reverse transcription']['canonical_verified_statement']
    assert 'corepressor' in rows['Tryptophan as corepressor']['canonical_verified_statement']
    assert 'β-galactosidase' in rows['lac structural gene products']['canonical_verified_statement']
    assert 'Nearly all' in rows['Near universality of genetic code']['canonical_verified_statement']
    assert 'not in a multiple of three' in rows['Frameshift mutation']['canonical_verified_statement']

def test_unit6_current_ced_coverage_repairs_present():
    rows={r['canonical_label']:r for r in read(U6/'source/canonical-unit6-f1.json')['canonical_catalog']}
    for label in ['Constitutive and inducible expression','Promoter/enhancer recruitment of transcription machinery','Regulatory-sequence position','Viral recombination','PCR denaturation','PCR primer annealing','PCR extension','Bacterial transformation as biotechnology','Conserved reproductive sources of variation']:
        assert rows[label]['scope_class']=='AP_REQUIRED'

def test_unit6_f1_historical_boundary_is_preserved_after_later_gates():
    r=read(U6/'f1-release-manifest.json')
    assert r['student_release'] is False
    assert (r['journeys'],r['scenes'],r['memory_objects'],r['application_challenges'])==(0,0,0,0)
    client=TestClient(app)
    current=client.get('/api/units/unit-6').json()
    assert current['status'] in {'SCIENCE_LOCKED_F1_NOT_STUDENT_RELEASED','LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
    if current['status']=='STUDENT_READY':
        assert current['student_release'] is True and current['preview_release'] is False
        assert len(client.get('/api/units/unit-6/journeys').json()['guided_journeys'])==6
        assert client.get('/api/units/unit-6/application-lab').json()['challenge_count']==16
    else:
        assert current['student_release'] is False
        assert client.get('/api/units/unit-6/journeys').json()['guided_journeys']==[]
        assert client.get('/api/units/unit-6/application-lab').json()['challenge_count']==0

def test_unit6_upstream_units_1_5_byte_protection():
    up=read(U6/'upstream-u1-u5-protection-f1.json')
    assert up['baseline_package_sha256']=='453d82f55947cad203025e52b50f3dd41adf624fdef465fdddcf29cf4bc80b74'
    assert up['protected_file_count']==291
    for x in up['protected_files']:
        p=ROOT/x['path']; assert p.stat().st_size==x['bytes']; assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
