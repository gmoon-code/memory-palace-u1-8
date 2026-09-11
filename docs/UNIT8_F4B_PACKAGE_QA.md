# Unit 8 F4B Package QA

## Result

**PASS**

## Curriculum state

- Unit 8 F1 canonical records **255**
- Unit 8 F2 permanent loci **58**
- Unit 8 F3 scene briefs **58**
- Unit 8 polished journeys through F4B **2**
- Unit 8 polished scenes through F4B **21**
- Journey 1 locked records represented **50 / 50**
- Journey 2 locked records represented **47 / 47**
- Journey 2 exact-name targets introduced **24 / 24**
- Journey 2 Quick Recalls **3**
- Journey 2 narrative words **4,940**
- Cumulative polished narrative words **11,009**
- Student release **false**
- Final Unit 8 Memory Objects **0**
- Live Unit 8 Challenge Lab tasks **0**

## Regression state

- Unit 8 F3 QA **PASS**
- Unit 8 F4A QA **PASS**
- Unit 8 F4B QA **PASS**
- Units 1–7 mainline QA **PASS**
- Unit 7 F6 QA **PASS**
- Unit 3 through Unit 7 UI logic QA **PASS**
- Python tests **387 / 387 PASS**
- JavaScript syntax checks **PASS**
- GitHub Actions workflow YAML parse **PASS**
- Python compilation **PASS**

## Upstream protection

- Units 1–7 content files compared with F4A baseline **421 / 421 identical**
- Backend/frontend source files compared with F4A baseline **15 / 15 identical**
- F4A content-lock files **7 / 7 identical**
- F1/F2/F3 protected locks remain valid under Unit 8 F3 and F4B QA

The public learner runtime remains `v2-apbio-0.28.0-u7-f6`.

## Deterministic F4B build

The generated Journey 2 narrative and F4B release layer are rebuilt with `scripts/build_unit8_f4b.py`. A pre/post SHA-256 comparison checked **7 F4B content-lock artifacts** and changed **0**.

## Student-runtime boundary

Unit 8 remains a developer preview only.

- Course registry status `F4B_JOURNEY2_POLISHED_DEVELOPER_PREVIEW`
- `student_release` **false**
- `preview_release` **true**
- Public Unit 8 journey registry **empty**
- Direct public fetch of U8-J1 **404**
- Direct public fetch of U8-J2 **404**
- Public Unit 8 Challenge Lab **0 items**
- Unit 7 remains student-ready with **6 / 6** journeys

## Forbidden-file policy

The release archive contains no source PDFs, `.git`, exact `.env`, SQLite/database files, Python bytecode, `__pycache__`, or pytest cache directories.

## Final archive

The final GitHub-ready ZIP contains **1,016 file entries**. ZIP integrity checking reports no compressed-data errors, and the archive-level forbidden-file scan reports **0** prohibited entries. The SHA-256 checksum is distributed in the adjacent `.sha256` file so the checksum does not recursively alter the archive it describes.
