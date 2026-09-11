# Unit 4 F4G Mainline Integration Audit

## Release state

Unit 4 F4G completes the polished narrative layer for all seven Unit 4 journeys while keeping Unit 4 outside the student release runtime. Journeys 1–6 are protected byte-for-byte from the F4F content lock. Journey 7 is locked by F4G.

## Unit 4 F4G accounting

- F1 canonical records protected: **180**
- F2 palace-managed records: **162**
- F2 practice-only Challenge Lab records reserved: **15**
- F2 non-runtime scope guards: **3**
- F2/F3 permanent loci: **51**
- Polished journeys: **7 / 7**
- Polished scenes: **51 / 51**
- Optional first-exposure Quick Recalls: **18**
- Journey 7 locked records: **28 / 28**
- Journey 7 scenes: **10 / 10**
- Journey 7 Quick Recalls: **3**
- Journey 7 narrative words: **4,385**
- Mean Journey 7 scene length: **438.5 words**
- Shortest Journey 7 scene: **404 words**
- Student release: **false**
- Developer preview: **true**

## Narrative protections

Journey 7 preserves fixed left/center/right geography in all ten scenes and carries one model-cell security file through the complete route. Checkpoints, cell-cycle arrest, and apoptosis remain distinct. G1, G2, and spindle-assembly checkpoints inspect different evidence. DNA-damage outcomes remain context-dependent. Cyclin, CDK, cyclin–CDK complex, and phosphorylated targets remain distinct. Growth factors are not universally classified as hormones. Cancer is represented as accumulated regulatory dysregulation without a universal fixed mutation count. Tumor, benign tumor, malignant tumor, metastasis, and replicative immortality remain distinct. UV exposure is connected specifically to DNA damage and skin-cancer risk, while tobacco-smoke carcinogens are connected to DNA damage and cancer risk and nicotine remains identified primarily as the addictive agent.

## Historical regression

The project build/QA sequence was rerun from Unit 1 through Unit 4 F4G from a temporary Git baseline. The local sandbox has no need to reinstall already-present Python dependencies for this verification.

- Unit 1 historical build and source lock: **PASS**
- Unit 2 F1–F5: **PASS**
- Unit 3 F1–F6: **PASS**
- Unit 4 F1–F4G: **PASS**
- Units 1–3 mainline release gate: **PASS**
- Unit 3 F6 UI-logic QA: **PASS**
- Python automated tests: **190 / 190 PASS**
- Python compilation/build execution: **PASS**
- Frontend JavaScript syntax checks: **PASS**
- Deterministic rebuild after F4G baseline: **PASS, zero Git diff**

## Live preview smoke test

A local FastAPI server successfully returned:

- Unit 4 metadata: **200**
- Unit 4 journey registry: **200**
- U4-J1 through U4-J7: **200 each**
- Unit 4 developer preview route `/?unit=unit-4`: **200**

The registry exposed exactly U4-J1 through U4-J7, and Unit 4 remained `student_release: false`.

## Packaging gate

The release package contains no source PDFs, SQLite databases, Python bytecode/caches, pytest caches, `.git` development folder, or `.env` secret file.

## Next gate

**F5 finalization** must preserve Journeys 1–7 and build the runtime learning layer: Memory Objects, exact-name Review targets, mixed/confusable discrimination practice, the 15-item Challenge Lab, scope-guard handling, full 180-record accounting, student-release status, API/runtime wiring, and final Unit 4 QA.
