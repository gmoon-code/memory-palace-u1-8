import hashlib, json
from collections import Counter
from pathlib import Path

from fastapi.testclient import TestClient
from backend.main import app

ROOT = Path(__file__).resolve().parents[1]
U7 = ROOT/"content/ap-biology/unit-7"

def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def test_unit7_f1_accounting_and_lock():
    d = read(U7/"source/canonical-unit7-f1.json")
    assert len(d["ppt_raw_slides"]) == 107
    assert len(d["ced_current_atoms"]) == 68
    assert len(d["canonical_catalog"]) == 215
    assert len(d["review_flags"]) == 39
    assert len(d["assessment_semantic_crosswalk"]) == 13
    assert len(d["cross_unit_dependencies"]) == 5
    assert Counter(r["scope_class"] for r in d["canonical_catalog"]) == Counter({
        "AP_REQUIRED":76,
        "TEACHER_REQUIRED_ENRICHMENT":98,
        "PRACTICE_ONLY":16,
        "SCOPE_GUARD":25,
    })
    assert all(r["canonical_lock"] == "LOCKED_F1" for r in d["canonical_catalog"])

def test_unit7_all_slides_preserved_and_ced_topics_complete():
    d = read(U7/"source/canonical-unit7-f1.json")
    cov = read(U7/"source/coverage-manifest-f1.json")
    assert [x["slide"] for x in d["ppt_raw_slides"]] == list(range(1,108))
    assert cov["ppt_coverage"]["unmapped"] == 0
    assert {x["topic"] for x in d["ced_current_atoms"]} == {f"7.{i}" for i in range(1,13)}
    assert any(x["ced_id"] == "7.9.A.3-outgroup" for x in d["ced_current_atoms"])

def test_unit7_high_risk_science_repairs_present():
    rows = {r["canonical_label"]:r for r in read(U7/"source/canonical-unit7-f1.json")["canonical_catalog"]}
    assert "heterozygous" in rows["Sickle-cell heterozygote advantage"]["canonical_verified_statement"]
    assert "not inherently the dominant allele" in rows["p as allele-1 frequency"]["canonical_verified_statement"]
    assert "not inherently the recessive allele" in rows["q as allele-2 frequency"]["canonical_verified_statement"]
    assert "2N" in rows["Allele frequency from genotype counts"]["canonical_verified_statement"]
    assert "reduced or modified functions" in rows["Vestigial structure"]["canonical_verified_statement"]
    assert "little free molecular oxygen" in rows["Early Earth had little free oxygen"]["canonical_verified_statement"]
    assert "small organic compounds" in rows["Miller-Urey experiment"]["canonical_verified_statement"]

def test_unit7_current_ced_repairs_and_rna_world_present():
    rows = {r["canonical_label"]:r for r in read(U7/"source/canonical-unit7-f1.json")["canonical_catalog"]}
    for label in [
        "Outgroup in phylogenetic inference",
        "RNA world hypothesis",
        "RNA replication and genetic continuity",
        "Base pairing in RNA replication",
        "Catalysis before encoded proteins",
    ]:
        assert rows[label]["scope_class"] == "AP_REQUIRED"

def test_unit7_f1_runtime_boundary_and_api():
    client = TestClient(app)
    u7 = client.get("/api/units/unit-7").json()
    assert u7["status"] in {"SCIENCE_LOCKED_F1_NOT_STUDENT_RELEASED","LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED","SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED","F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW","F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW","F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW","F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW","F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW","F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW","STUDENT_READY"}
    assert u7["canonical_records"] == 215
    if u7["status"] == "STUDENT_READY":
        assert u7["student_release"] is True and u7["preview_release"] is False
        assert len(client.get("/api/units/unit-7/journeys").json()["guided_journeys"]) == 6
        assert client.get("/api/units/unit-7/application-lab").json()["challenge_count"] == 16
    else:
        assert u7["student_release"] is False
        assert client.get("/api/units/unit-7/journeys").json()["guided_journeys"] == []
        assert client.get("/api/units/unit-7/application-lab").json()["challenge_count"] == 0
    obj = client.get("/api/units/unit-7/objects/U7-K-001")
    assert obj.status_code == 200
    body=obj.json()
    assert body.get("canonical_lock",body.get("scientific_lock_status")) == "LOCKED_F1"

def test_unit7_upstream_units_1_6_byte_protection():
    up = read(U7/"upstream-u1-u6-protection-f1.json")
    assert up["baseline_package_sha256"] == "ba5ca238d579d7fa733bd6b17613d85dc7685893152ff4bc574ee65a0b7b508a"
    assert up["protected_file_count"] == 356
    for x in up["protected_files"]:
        p = ROOT/x["path"]
        assert p.stat().st_size == x["bytes"]
        assert hashlib.sha256(p.read_bytes()).hexdigest() == x["sha256"]

def test_unit7_release_manifest_remains_nonstudent():
    r = read(U7/"f1-release-manifest.json")
    assert r["scientific_content_lock"] == "LOCKED_F1"
    assert r["student_release"] is False
    assert (r["journeys"],r["scenes"],r["memory_objects"],r["application_challenges"]) == (0,0,0,0)
    assert r["next_gate"] == "UNIT7_F2_LEARNING_FUNCTION_AND_PALACE_ARCHITECTURE"
