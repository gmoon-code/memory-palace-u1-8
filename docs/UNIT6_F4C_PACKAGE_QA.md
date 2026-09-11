# Unit 6 F4C Package QA

## Result

**PASS**

## Curriculum state

- Unit 6 F1 canonical records: **202**
- Unit 6 F2 permanent loci: **53**
- Unit 6 F3 scene briefs: **53**
- Unit 6 polished journeys: **3 / 6**
- Unit 6 polished scenes: **28 / 53**
- Journey 3 records represented: **20 / 20**
- Journey 3 exact-name targets introduced: **16 / 16**
- Journey 3 Quick Recalls: **3**
- Journey 3 narrative words: **4,258**
- Journeys 1–2 frozen: **PASS**
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
- Unit 6 F4B: **PASS**
- Unit 6 F4C: **PASS**
- Python tests: **286 / 286 PASS**
- Unit 3 F6 UI logic: **PASS**
- Unit 4 F6 UI logic: **PASS**
- Unit 5 F6 UI logic: **PASS**
- JavaScript syntax: **PASS**
- Python compilation: **PASS**
- Live FastAPI boundary: **PASS**

## Upstream protection

The Unit 6 protection manifest verifies **291 / 291 protected Units 1–5 content files** byte-for-byte against the supplied Unit 5 F6 baseline.

Journey 1 remains frozen at its F4A SHA-256 and Journey 2 remains frozen at its F4B SHA-256.

## Deterministic F4C build

- Checked artifacts: **8**
- Changed artifacts: **0**

## Live API boundary

Live FastAPI smoke confirmed:

- health endpoint returns the validated Units 1–5 runtime version
- Unit 5 remains student ready
- Unit 6 reports `F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW`
- Unit 6 `student_release` remains `false`
- Unit 6 public journey registry remains empty
- direct request for public U6-J3 returns 404
- Unit 6 public Challenge Lab remains empty

## Forbidden-file policy

The release archive contains no source PDFs, `.git`, `.env`, SQLite databases, Python bytecode, `__pycache__`, or pytest cache directories.

## Final archive

- Archive entries: **772**
- Archive integrity: **PASS**
- Forbidden files found: **0**

The SHA-256 is distributed in the adjacent `.sha256` file so the checksum does not recursively alter the archive it describes.
