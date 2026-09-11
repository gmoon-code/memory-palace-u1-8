import json
from pathlib import Path

def test_unit3_f2_architecture():
    repo_root=Path(__file__).resolve().parents[1]
    u3=repo_root/'content'/'ap-biology'/'unit-3'
    arch=json.loads((u3/'architecture'/'palace-architecture-f2.json').read_text())
    cls=json.loads((u3/'architecture'/'learning-classification-f2.json').read_text())
    assert arch['counts']['permanent_loci']==54
    assert arch['counts']['journeys']==7
    assert arch['counts']['bundles']==20
    assert arch['counts']['palace_managed_records']==171
    assert arch['counts']['practice_only_records']==11
    assert arch['counts']['scope_guard_records']==4
    assert len(cls['records'])==186
    assert cls['counts']['exact_name_targets']==126
    assert cls['counts']['mandatory_spelling_targets']==0

def test_unit3_f2_zero_loss():
    repo_root=Path(__file__).resolve().parents[1]
    u3=repo_root/'content'/'ap-biology'/'unit-3'
    src=json.loads((u3/'source'/'canonical-unit3-f1.json').read_text())
    arch=json.loads((u3/'architecture'/'palace-architecture-f2.json').read_text())
    canonical={r['knowledge_id'] for r in src['canonical_catalog']}
    palace={k for l in arch['loci'] for k in l['knowledge_ids']}
    challenge={x['knowledge_id'] for x in arch['challenge_lab']}
    scope={x['knowledge_id'] for x in arch['scope_guards']}
    assert len(palace)==171 and len(challenge)==11 and len(scope)==4
    assert palace|challenge|scope==canonical
    assert not (palace&challenge or palace&scope or challenge&scope)

def test_unit3_f2_not_student_released():
    repo_root=Path(__file__).resolve().parents[1]
    u3=repo_root/'content'/'ap-biology'/'unit-3'
    status=json.loads((u3/'status-f2.json').read_text())
    assert status['student_release'] is False
    assert status['journey_count']==0
    assert status['scene_count']==0
