# Unit 6 F4C Integration Audit

## Result

**PASS**

## Protected upstream curriculum

- Units 1–5 protected files: **291 / 291 unchanged**
- Unit 1 full QA: **PASS**
- Unit 2 F5: **PASS**
- Unit 3 F6: **PASS**
- Unit 4 F6: **PASS**
- Unit 5 F6: **PASS**
- Units 1–5 mainline QA: **PASS**

## Unit 6 cumulative gates

- F1 scientific lock: **PASS**
- F2 learning architecture: **PASS**
- F3 scene-brief lock: **PASS**
- F4A Journey 1: **frozen byte-for-byte**
- F4B Journey 2: **frozen byte-for-byte**
- F4C Journey 3: **PASS**

## Unit 6 current narrative state

- Locked F1 records: **202**
- F2 palace-managed records: **161**
- F2 permanent loci: **53**
- F3 scene briefs: **53**
- Polished journeys: **3**
- Polished scenes: **28**
- Journey 1 knowledge records: **42**
- Journey 2 knowledge records: **26**
- Journey 3 knowledge records: **20**
- Journey 3 exact-name targets: **16**
- Unit 6 final Memory Objects: **0**
- Unit 6 live Challenge Lab tasks: **0**
- Student release: **false**

## Runtime isolation

The validated Unit 5 F6 public runtime remains authoritative. Unit 6 reports developer-preview status in unit metadata, while its public journey registry remains empty and its public Challenge Lab remains empty.

Live FastAPI smoke confirmed:

- health endpoint returns `v2-apbio-0.24.0-u5-f6`
- Unit 5 remains `STUDENT_READY`
- Unit 6 reports `F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW`
- Unit 6 `student_release` remains `false`
- Unit 6 public journey registry remains empty
- direct public request for U6-J3 returns 404
- Unit 6 public Challenge Lab remains empty

## Deterministic generation

Eight F4C-generated/affected artifacts were hashed, `scripts/build_unit6_f4c.py` was rerun, and all eight hashes remained identical.

- Checked artifacts: **8**
- Changed artifacts: **0**

## Test state

- Python tests: **286 / 286 PASS**
- Python compilation: **PASS**
- JavaScript syntax checks: **PASS**
- Unit 3 F6 UI logic: **PASS**
- Unit 4 F6 UI logic: **PASS**
- Unit 5 F6 UI logic: **PASS**
- Live FastAPI boundary: **PASS**
