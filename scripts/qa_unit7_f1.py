from __future__ import annotations
import hashlib, json, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
U7 = ROOT / "content/ap-biology/unit-7"

def read(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

problems = []

canonical = read(U7/"source/canonical-unit7-f1.json")
coverage = read(U7/"source/coverage-manifest-f1.json")
lock = read(U7/"content-lock-f1.json")
release = read(U7/"f1-release-manifest.json")
status = read(U7/"status.json")

records = canonical["canonical_catalog"]
slides = canonical["ppt_raw_slides"]
ced = canonical["ced_current_atoms"]
flags = canonical["review_flags"]
assess = canonical["assessment_semantic_crosswalk"]
cross = canonical["cross_unit_dependencies"]

if len(records) != 215:
    problems.append(f"canonical record count {len(records)} != 215")
if len(slides) != 107:
    problems.append(f"PPT slide count {len(slides)} != 107")
if len(ced) != 68:
    problems.append(f"CED atom count {len(ced)} != 68")
if len(flags) != 39:
    problems.append(f"review flag count {len(flags)} != 39")
if len(assess) != 13:
    problems.append(f"assessment crosswalk count {len(assess)} != 13")
if len(cross) != 5:
    problems.append(f"cross-unit dependency count {len(cross)} != 5")

ids = [r["knowledge_id"] for r in records]
if ids != [f"U7-K-{i:03d}" for i in range(1, 216)]:
    problems.append("canonical IDs are not sequential U7-K-001..U7-K-215")
if len(ids) != len(set(ids)):
    problems.append("duplicate canonical IDs")
if any(r.get("canonical_lock") != "LOCKED_F1" for r in records):
    problems.append("one or more canonical records are not LOCKED_F1")
if any(not r.get("canonical_label") or not r.get("canonical_verified_statement") for r in records):
    problems.append("one or more canonical records lack label or verified statement")

expected = {
    "AP_REQUIRED": 76,
    "TEACHER_REQUIRED_ENRICHMENT": 98,
    "PRACTICE_ONLY": 16,
    "SCOPE_GUARD": 25,
}
sc = dict(Counter(r["scope_class"] for r in records))
if sc != expected:
    problems.append(f"scope accounting {sc} != {expected}")

if [s["slide"] for s in slides] != list(range(1,108)):
    problems.append("PPT raw slide ledger is not slides 1..107")
allowed = {"MAPPED","MAPPED_VISUAL","PRESERVED_METADATA"}
if any(s["coverage_status"] not in allowed for s in slides):
    problems.append("invalid slide coverage status")
metadata = set(coverage["ppt_coverage"]["metadata_only_slides"])
if any((not s["mapped_knowledge_ids"]) and s["slide"] not in metadata for s in slides):
    problems.append("substantive slide missing canonical mappings")

known = set(ids)
for s in slides:
    bad = set(s.get("mapped_knowledge_ids",[])) - known
    if bad:
        problems.append(f"slide {s['slide']} maps unknown IDs {sorted(bad)}")

expected_topics = {f"7.{i}" for i in range(1,13)}
ced_topics = {a["topic"] for a in ced}
if ced_topics != expected_topics:
    problems.append(f"CED topics incomplete: {sorted(ced_topics)}")

cedids = {a["ced_id"] for a in ced}
record_cedids = {r["ced_id"] for r in records if r.get("ced_id")}
if cedids - record_cedids:
    problems.append(f"CED atoms missing canonical lock records: {sorted(cedids-record_cedids)}")

if not any(a["ced_id"] == "7.9.A.3-outgroup" for a in ced):
    problems.append("current-CED outgroup requirement is missing from atomization")

for f in flags:
    if f.get("status") != "RESOLVED" or not f.get("resolution"):
        problems.append(f"unresolved/incomplete flag {f.get('review_flag_id')}")
if [f["review_flag_id"] for f in flags] != [f"RF-U7-{i:03d}" for i in range(1,40)]:
    problems.append("review flag IDs are not sequential RF-U7-001..RF-U7-039")

for a in assess:
    if a["source"] != "APBIO-U7-PPT.pdf":
        problems.append(f"unexpected assessment source {a['source']}")
    if not a["mapped_knowledge_ids"]:
        problems.append(f"assessment {a['assessment_id']} has no mappings")
    bad = set(a["mapped_knowledge_ids"]) - known
    if bad:
        problems.append(f"assessment {a['assessment_id']} maps unknown IDs {sorted(bad)}")

if coverage["ppt_coverage"]["unmapped"] != 0:
    problems.append("coverage reports unmapped slides")
if coverage["student_runtime"] != {
    "journeys":0,
    "scenes":0,
    "memory_objects":0,
    "application_challenges":0,
    "student_release":False,
}:
    problems.append("F1 runtime boundary broken")

if release.get("student_release") is not False:
    problems.append("Unit 7 F1 release manifest incorrectly exposes students")
for k in ("journeys","scenes","memory_objects","application_challenges"):
    if release.get(k) != 0:
        problems.append(f"F1 runtime field {k} is not zero")
if release.get("scientific_content_lock") != "LOCKED_F1" or lock.get("lock_status") != "LOCKED_F1":
    problems.append("F1 lock is not LOCKED_F1")

allowed_current={"SCIENCE_LOCKED_F1_NOT_STUDENT_RELEASED","LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED","SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED","F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW","F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW","F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW","F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW","F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW","F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW","STUDENT_READY"}
if status.get("status") not in allowed_current:
    problems.append("Unit 7 status boundary invalid for preserved F1 science")
if status.get('status')!='STUDENT_READY' and status.get("student_release") is not False:
    problems.append("Unit 7 pre-runtime status incorrectly student-releases Unit 7")
if status.get('status')=='STUDENT_READY' and (status.get('student_release') is not True or status.get('preview_release') is not False):
    problems.append('Unit 7 F5 release flags invalid while preserving F1')

# High-risk source repairs that must never regress into future mnemonics.
labels = {r["canonical_label"]: r for r in records}
checks = {
    "Sickle-cell heterozygote advantage": ["heterozygous", "malaria"],
    "Populations evolve, individuals do not": ["population", "individual"],
    "Drift is nonadaptive": ["chance", "does not consistently increase adaptation"],
    "p as allele-1 frequency": ["not inherently the dominant allele"],
    "q as allele-2 frequency": ["not inherently the recessive allele"],
    "Allele frequency from genotype counts": ["2N"],
    "Vestigial structure": ["reduced or modified functions"],
    "Analogous structures": ["not because"],
    "Sister taxa": ["immediate common ancestor"],
    "Outgroup in phylogenetic inference": ["ancestral", "derived"],
    "Early Earth had little free oxygen": ["little free molecular oxygen"],
    "Miller-Urey experiment": ["small organic compounds"],
    "Endosymbiosis is later than life's origin": ["later event than the origin of the first cellular life"],
}
for label, needles in checks.items():
    r = labels.get(label)
    if not r:
        problems.append(f"missing corrected record: {label}")
        continue
    text = r["canonical_verified_statement"]
    for needle in needles:
        if needle.casefold() not in text.casefold():
            problems.append(f"corrected record {label} missing {needle}")

rna = labels.get("RNA world hypothesis")
if not rna or rna["scope_class"] != "AP_REQUIRED":
    problems.append("RNA world hypothesis is not AP_REQUIRED")
for required in [
    "RNA replication and genetic continuity",
    "Base pairing in RNA replication",
    "Catalysis before encoded proteins",
]:
    r = labels.get(required)
    if not r or r["scope_class"] != "AP_REQUIRED":
        problems.append(f"missing AP-required RNA-world relationship: {required}")

hwe = labels.get("Hardy-Weinberg equilibrium as null model")
if not hwe or "idealized null model" not in hwe["canonical_verified_statement"]:
    problems.append("Hardy-Weinberg null-model correction missing")

# Protected Unit 7 F1 science.
for item in lock["protected_files"]:
    p = U7/item["path"]
    if not p.exists():
        problems.append(f"protected Unit 7 file missing: {item['path']}")
        continue
    if p.stat().st_size != item["bytes"] or sha(p) != item["sha256"]:
        problems.append(f"protected Unit 7 file changed: {item['path']}")

# Exact supplied Units 1-6 baseline remains intact.
up = read(U7/"upstream-u1-u6-protection-f1.json")
expected_baseline = "ba5ca238d579d7fa733bd6b17613d85dc7685893152ff4bc574ee65a0b7b508a"
if up.get("baseline_package_sha256") != expected_baseline:
    problems.append("wrong Units 1-6 baseline checksum")
if up.get("protected_file_count") != 356:
    problems.append("Units 1-6 protection manifest does not contain 356 files")
for item in up.get("protected_files",[]):
    p = ROOT/item["path"]
    if not p.exists():
        problems.append(f"released U1-U6 file missing: {item['path']}")
        continue
    if p.stat().st_size != item["bytes"] or sha(p) != item["sha256"]:
        problems.append(f"released U1-U6 file changed: {item['path']}")

# Unit 7 F1 integration bytes were exact at the F1 release. Later gates may intentionally
# advance status/course integration while preserving the protected F1 scientific artifacts.
course_path = ROOT/"content/ap-biology/course.json"
if status.get("status")=="SCIENCE_LOCKED_F1_NOT_STUDENT_RELEASED":
    for rel,digest in lock.get("runtime_file_sha256",{}).items():
        p = ROOT/rel
        if not p.exists() or sha(p) != digest:
            problems.append(f"Unit 7 F1 runtime integration hash mismatch: {rel}")
    if lock.get("course_registry_sha256") != sha(course_path):
        problems.append("Unit 7 F1 course registry hash mismatch")

# Course registry and source-PDF hygiene.
course = read(course_path)
u7 = next((u for u in course["units"] if u["unit_id"]=="unit-7"),None)
if not u7:
    problems.append("Unit 7 missing from course registry")
elif u7.get("status") not in allowed_current or u7.get("canonical_records")!=215:
    problems.append("course registry Unit 7 F1 state mismatch")
elif u7.get('status')=='STUDENT_READY' and u7.get('student_release') is not True:
    problems.append('course registry Unit 7 F5 release invalid while preserving F1')
elif u7.get('status')!='STUDENT_READY' and u7.get('student_release') is not False:
    problems.append('course registry Unit 7 pre-F5 release invalid while preserving F1')

for n in range(1,7):
    u = next((u for u in course["units"] if u["unit_id"]==f"unit-{n}"),None)
    if not u or u.get("status") != "STUDENT_READY":
        problems.append(f"upstream Unit {n} is no longer STUDENT_READY")

for p in ROOT.rglob("*.pdf"):
    problems.append(f"forbidden source PDF in repository: {p.relative_to(ROOT)}")

required = [
    U7/"source/canonical-unit7-f1.json",
    U7/"source/coverage-manifest-f1.json",
    U7/"audit/F1_SOURCE_AUDIT.md",
    U7/"audit/F1_REVIEW_FLAGS.md",
    U7/"audit/APBIO_Unit7_F1_Source_Lock.xlsx",
    U7/"content-lock-f1.json",
    U7/"f1-release-manifest.json",
    U7/"status.json",
    U7/"upstream-u1-u6-protection-f1.json",
    ROOT/"docs/UNIT7_F1_QA.md",
    ROOT/"docs/UNIT7_F1_RELEASE.md",
]
for p in required:
    if not p.exists():
        problems.append(f"missing required artifact: {p.relative_to(ROOT)}")

if problems:
    print("UNIT 7 F1 QA FAIL")
    print("\n".join(f"- {p}" for p in problems))
    sys.exit(1)

print("UNIT 7 F1 QA PASS")
print({
    "slides":107,
    "ced_topics":12,
    "ced_atoms":68,
    "canonical_records":215,
    "scope_counts":sc,
    "flags":39,
    "assessments":13,
    "cross_unit":5,
    "runtime":0,
    "upstream_protected":356,
})
