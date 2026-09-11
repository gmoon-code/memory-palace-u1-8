# Unit 6 F4B Package QA

## Result

**PASS**

## Curriculum state

- Unit 6 F1 canonical records: **202**
- Unit 6 F2 permanent loci: **53**
- Unit 6 F3 scene briefs: **53**
- Unit 6 polished journeys: **2 / 6**
- Unit 6 polished scenes: **20 / 53**
- Journey 2 records represented: **26 / 26**
- Journey 2 exact-name targets introduced: **21 / 21**
- Journey 2 Quick Recalls: **3**
- Journey 2 narrative words: **4,504**
- Journey 1 frozen: **PASS**
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
- Unit 6 F4B: **PASS**
- Python tests: **281 / 281 PASS**
- Unit 3 F6 UI logic: **PASS**
- Unit 4 F6 UI logic: **PASS**
- Unit 5 F6 UI logic: **PASS**
- JavaScript syntax: **PASS**
- Python compilation: **PASS**
- Live FastAPI boundary: **PASS**

## Upstream protection

The Unit 6 protection manifest verifies **291 / 291 protected Units 1–5 content files** byte-for-byte against the supplied Unit 5 F6 baseline.

Journey 1 is also frozen byte-for-byte at its F4A SHA-256.

## Deterministic F4B build

- Checked artifacts: **9**
- Changed artifacts: **0**

## Live API boundary

Live FastAPI smoke confirmed:

- health endpoint responds
- Unit 5 remains student ready
- Unit 6 reports `F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW`
- Unit 6 `student_release` remains `false`
- Unit 6 public journey registry remains empty
- Unit 6 public Challenge Lab remains empty

## Forbidden-file policy

The release archive contains no source PDFs, `.git`, `.env`, SQLite databases, Python bytecode, `__pycache__`, or pytest cache directories.

## Final archive

- Archive entries: **757**
- Archive integrity: **PASS**
- Forbidden files found: **0**

The SHA-256 is distributed in the adjacent `.sha256` file so the checksum does not recursively alter the archive it describes.
