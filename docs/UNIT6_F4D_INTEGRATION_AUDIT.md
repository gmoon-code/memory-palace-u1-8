# Unit 6 F4D Integration Audit

## Result

**PASS**

## Protected upstream curriculum

- Units 1–5 protected files **291 / 291 unchanged**
- Unit 1 full QA **PASS**
- Unit 2 F5 **PASS**
- Unit 3 F6 **PASS**
- Unit 4 F6 **PASS**
- Unit 5 F6 **PASS**
- Units 1–5 mainline QA **PASS**

## Unit 6 cumulative gates

- F1 scientific lock **PASS**
- F2 learning architecture **PASS**
- F3 scene-brief lock **PASS**
- F4A Journey 1 **frozen byte-for-byte**
- F4B Journey 2 **frozen byte-for-byte**
- F4C Journey 3 **frozen byte-for-byte**
- F4D Journey 4 **PASS**

## Unit 6 current narrative state

- Locked F1 records **202**
- F2 palace-managed records **161**
- F2 permanent loci **53**
- F3 scene briefs **53**
- Polished journeys **4**
- Polished scenes **40**
- Journey 4 knowledge records **36**
- Journey 4 exact-name targets **29**
- Journey 4 optional first-exposure recalls **4**
- Unit 6 final Memory Objects **0**
- Unit 6 live Challenge Lab tasks **0**
- Student release **false**

## Runtime isolation

Live FastAPI smoke confirmed the validated Unit 5 F6 runtime remains authoritative.

- health endpoint returns `v2-apbio-0.24.0-u5-f6`
- Unit 5 remains `STUDENT_READY`
- Unit 6 reports `F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW`
- Unit 6 `student_release` remains `false`
- Unit 6 public journey registry remains empty
- direct public request for U6-J4 returns 404
- Unit 6 public Challenge Lab remains empty

## Deterministic generation

Eleven F4D-generated or affected artifacts were hashed, `scripts/build_unit6_f4d.py` was rerun, and all eleven hashes remained identical.

- Checked artifacts **11**
- Changed artifacts **0**

## Test state

- Python tests **291 / 291 PASS**
- Python compilation **PASS**
- JavaScript syntax checks **PASS**
- Unit 3 F6 UI logic **PASS**
- Unit 4 F6 UI logic **PASS**
- Unit 5 F6 UI logic **PASS**
- Live FastAPI boundary **PASS**
