import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
UNIT=ROOT/'content/ap-biology/unit-1'
def test_preserved_source_hashes():
    lock=json.loads((UNIT/'content-lock.json').read_text())
    for rel,meta in lock['files'].items():
        p=ROOT/rel
        assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']
def test_expected_counts():
    canonical=json.loads((UNIT/'source/canonical-unit1.json').read_text())
    journeys=json.loads((UNIT/'source/guided-journeys.json').read_text())
    objects=json.loads((UNIT/'memory-objects.json').read_text())
    assert len(canonical['canonical_records'])==229
    assert len(journeys['guided_journeys'])==9
    assert objects['count']==207
    assert sum(j['scene_count'] for j in journeys['guided_journeys'])==78
