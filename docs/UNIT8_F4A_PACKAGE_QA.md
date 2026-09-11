# Unit 8 F4A Package QA

## Result

**PASS**

## Curriculum state

- Unit 8 F1 canonical records **255**
- Unit 8 F2 permanent loci **58**
- Unit 8 F3 scene briefs **58**
- Unit 8 F4A polished journeys **1**
- Unit 8 F4A polished scenes **12**
- Journey 1 locked records represented **50 / 50**
- Journey 1 exact-name targets introduced **35 / 35**
- Journey 1 Quick Recalls **2**
- Journey 1 narrative words **6,069**
- Student release **false**
- Final Unit 8 Memory Objects **0**
- Live Unit 8 Challenge Lab tasks **0**

## Regression state

- Unit 8 F3 QA **PASS**
- Unit 8 F4A QA **PASS**
- Units 1–7 mainline QA **PASS**
- Unit 7 F6 QA **PASS**
- Unit 7 F6 UI logic **PASS**
- Python tests **381 / 381 PASS**
- JavaScript syntax checks **PASS**
- Python compilation **PASS**

## Upstream protection

- Units 1–7 content files compared with the validated F3 baseline **421 / 421 identical**
- Backend/frontend source files compared with the validated F3 baseline **15 / 15 identical**
- Unit 8 F1/F2/F3 protected core artifacts checked **12 / 12 identical**

The public learner runtime remains `v2-apbio-0.28.0-u7-f6`.

## Deterministic F4A build

The generated F4A narrative and release layer is rebuilt with `scripts/build_unit8_f4a.py`. A pre/post SHA-256 comparison checked **9 generated F4A artifacts** and changed **0**.

## Student-runtime boundary

Unit 8 is a developer preview only.

- Course registry status `F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW`
- `student_release` **false**
- `preview_release` **true**
- Public Unit 8 journey registry **empty**
- Direct public fetch of U8-J1 **404**
- Public Unit 8 Challenge Lab **0 items**
- Unit 7 remains student-ready with **6 / 6** journeys

## Forbidden-file policy

The release archive contains no source PDFs, `.git`, exact `.env`, SQLite/database files, Python bytecode, `__pycache__`, or pytest cache directories.

## Final archive

The final GitHub-ready release contains **1,000 file entries**. Archive integrity and forbidden-file checks pass. The SHA-256 checksum is distributed in the adjacent `.sha256` file so the checksum does not recursively alter the archive it describes.
