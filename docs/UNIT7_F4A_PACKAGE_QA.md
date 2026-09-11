# Unit 7 F4A Package QA

## Result

**PASS**

## Curriculum state

- Unit 7 F1 canonical records **215**
- Unit 7 F2 permanent loci **55**
- Unit 7 F3 scene briefs **55**
- Unit 7 F4A polished journeys **1**
- Unit 7 F4A polished scenes **10**
- Journey 1 locked records represented **26 / 26**
- Journey 1 exact-name targets introduced **15 / 15**
- Journey 1 Quick Recalls **3**
- Journey 1 narrative words **5,374**
- Student release **false**
- Final Unit 7 Memory Objects **0**
- Live Unit 7 Challenge Lab tasks **0**

## Regression state

- Unit 1 full QA **PASS**
- Unit 2 F5 **PASS**
- Unit 3 F6 **PASS**
- Unit 4 F6 **PASS**
- Unit 5 F6 **PASS**
- Unit 6 F1–F6 **PASS**
- Units 1–6 mainline QA **PASS**
- Unit 7 F1 **PASS**
- Unit 7 F2 **PASS**
- Unit 7 F3 **PASS**
- Unit 7 F4A **PASS**
- Python tests **333 / 333 PASS**
- Unit 3–6 UI logic **PASS**
- JavaScript syntax **PASS**
- Python compilation **PASS**

## Upstream protection

The Unit 7 upstream protection manifest still verifies **356 / 356 protected Units 1–6 content files** byte-for-byte against the supplied Unit 6 F6 baseline.

The public learner runtime remains Unit 6 F6. Unit 7 F4A does not modify the validated student runtime.

## Deterministic F4A build

The generated F4A narrative and release artifacts are rebuilt with `scripts/build_unit7_f4a.py`. A pre/post hash comparison checked **8** generated F4A artifacts and changed **0**.

## Live API boundary

Live FastAPI smoke must confirm

- health endpoint responds
- Unit 6 remains student ready
- Unit 7 reports `F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW`
- Unit 7 `student_release` remains `false`
- Unit 7 `preview_release` is `true`
- Unit 7 public journey registry remains empty
- direct public fetch of U7-J1 returns 404
- Unit 7 public Challenge Lab remains empty
- canonical Unit 7 object lookup remains available for development

## Forbidden-file policy

The release archive must contain no source PDFs, `.git`, exact `.env`, SQLite/database files, Python bytecode, `__pycache__`, or pytest cache directories.

## Final archive

The deterministic release archive contains **900 entries**, passes ZIP integrity checking, and contains **0 forbidden files**. The SHA-256 is distributed in the adjacent `.sha256` file so the checksum does not recursively alter the archive it describes.
