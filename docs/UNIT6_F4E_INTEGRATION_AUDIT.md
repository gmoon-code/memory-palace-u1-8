# Unit 6 F4E Integration Audit

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
- F4D Journey 4 **frozen byte-for-byte**
- F4E Journey 5 **PASS**

## Unit 6 current narrative state

- Locked F1 records **202**
- F2 palace-managed records **161**
- F2 permanent loci **53**
- F3 scene briefs **53**
- Polished journeys **5**
- Polished scenes **48**
- Journey 5 knowledge records **26**
- Journey 5 exact-name targets **25**
- Journey 5 optional first-exposure recalls **3**
- Unit 6 final Memory Objects **0**
- Unit 6 live Challenge Lab tasks **0**
- Student release **false**

## Runtime isolation

Live FastAPI smoke confirmed the validated Unit 5 F6 runtime remains authoritative.

- health endpoint returns `v2-apbio-0.24.0-u5-f6`
- Unit 5 remains `STUDENT_READY`
- Unit 6 reports `F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW`
- Unit 6 `student_release` remains `false`
- Unit 6 public journey registry remains empty
- direct public request for U6-J5 returns 404
- Unit 6 public Challenge Lab remains empty

## Test state

- Python tests **296 / 296 PASS**
- Python compilation **PASS**
- JavaScript syntax checks **PASS**
- Unit 3 F6 UI logic **PASS**
- Unit 4 F6 UI logic **PASS**
- Unit 5 F6 UI logic **PASS**
- Live FastAPI boundary **PASS**

## Deterministic generation

Twelve F4E-generated or affected artifacts were hashed, `scripts/build_unit6_f4e.py` was rerun, and all twelve hashes remained identical.

- Checked artifacts **12**
- Changed artifacts **0**
