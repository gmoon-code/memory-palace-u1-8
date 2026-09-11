# Unit 6 F4A Package QA

## Result

**PASS**

## Curriculum state

- Unit 6 F1 canonical records: **202**
- Unit 6 F2 permanent loci: **53**
- Unit 6 F3 scene briefs: **53**
- Unit 6 F4A polished journeys: **1**
- Unit 6 F4A polished scenes: **12**
- Journey 1 locked records represented: **42 / 42**
- Journey 1 exact-name targets introduced: **34 / 34**
- Journey 1 Quick Recalls: **3**
- Journey 1 narrative words: **6,492**
- Student release: **false**
- Final Unit 6 Memory Objects: **0**
- Live Unit 6 Challenge Lab tasks: **0**

## Regression state

- Unit 1 full QA: **PASS**
- Unit 2 F5: **PASS**
- Unit 3 F6: **PASS**
- Unit 4 F6: **PASS**
- Unit 5 F6: **PASS**
- Units 1–5 mainline QA: **PASS**
- Unit 6 F1: **PASS**
- Unit 6 F2: **PASS**
- Unit 6 F3: **PASS**
- Unit 6 F4A: **PASS**
- Python tests: **276 / 276 PASS**
- Unit 3 F6 UI logic: **PASS**
- Unit 4 F6 UI logic: **PASS**
- Unit 5 F6 UI logic: **PASS**
- JavaScript syntax: **PASS**
- Python compilation: **PASS**

## Upstream protection

The Unit 6 F1 protection manifest still verifies **291 / 291 protected Units 1–5 content files** byte-for-byte against the supplied Unit 5 F6 baseline.

The Unit 5 F6 browser/runtime hash gate also passes. Unit 6 F4A does not modify the validated public runtime.

## Deterministic F4A build

Eight generated F4A artifacts were hashed, `scripts/build_unit6_f4a.py` was rerun, and the same eight artifacts were hashed again.

- Checked artifacts: **8**
- Changed artifacts: **0**

## Live API boundary

Live FastAPI smoke confirmed:

- health endpoint responds
- Unit 5 remains student ready
- Unit 6 reports `F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW`
- Unit 6 `student_release` remains `false`
- Unit 6 public journey registry remains empty
- Unit 6 public Challenge Lab remains empty

This intentionally preserves the current runtime boundary while narrative development continues.

## Forbidden-file policy

The release archive must contain no source PDFs, `.git`, `.env`, SQLite databases, Python bytecode, `__pycache__`, or pytest cache directories.

## Final archive

- Archive entries: **744**
- Archive integrity: **PASS**
- Forbidden files found: **0**

The SHA-256 is distributed in the adjacent `.sha256` file so the checksum does not recursively alter the archive it describes.
