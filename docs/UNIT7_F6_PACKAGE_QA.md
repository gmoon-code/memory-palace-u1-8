# Unit 7 F6 Package QA

## Result

**PASS**

Unit 7 F6 completes the final functional browser-facing/classroom validation gate for Natural Selection while preserving the F1 scientific catalog, F2 architecture, F3 scene briefs, all six F4 narratives, and the F5 runtime curriculum.

## Package

`MemoryPalace_V2_Mainline_Units1-7_Unit7-F6.zip`

The final archive contains **993 entries** and passes ZIP integrity checking.

## Final Unit 7 accounting

- canonical records **215 / 215 accounted**
- runtime Memory Objects **174**
- guided journeys **6**
- permanent scenes/loci **55**
- optional first-exposure Quick Recalls **18**
- Challenge Lab items **16**
- scope guards **25**
- exact-name Review targets **94**
- meaning/mechanism-only palace records **80**
- mandatory spelling targets **0**
- mixed-discrimination sets **33**
- mixed-discrimination questions **102**
- unaccounted canonical records **0**

The zero-loss partition remains **174 story/runtime records + 16 Challenge Lab records + 25 scope guards = 215 canonical records**.

## Browser-facing validation

- production scene renders **55 / 55**
- hidden Quick Recall renders **18 / 18**
- responsive target contracts **desktop, tablet, phone**
- scene/viewport checks **165**
- recall/viewport checks **54**
- released-unit switching among Units 1–7 **PASS**
- refresh/resume persistence **PASS**
- unit-scoped Review **PASS**
- five-item visible Review cap **PASS**
- 48-hour mixed-discrimination delay **PASS**
- Challenge Lab **16 / 16 PASS**
- speech preparation **PASS**
- Chromium screenshot/pixel validation **not executed because Chromium timed out during an 8-second headless `about:blank` probe**

## Regression gates

- Unit 1 full QA **PASS**
- Unit 2 F5 QA **PASS**
- Unit 3 F6 QA **PASS**
- Unit 4 F6 QA **PASS**
- Unit 5 F6 QA **PASS**
- Unit 6 F6 QA **PASS**
- Unit 7 F1 through F6 **PASS**
- current Units 1–6 mainline QA **PASS**
- current Units 1–7 mainline QA **PASS**
- Unit 3 through Unit 7 UI-logic QA **PASS**
- Python suite **372 / 372 PASS**
- frontend JavaScript syntax checks **PASS**
- Python compilation **PASS**
- live FastAPI/HTTP behavior **PASS**
- deterministic Unit 7 F6 rebuild **9 checked artifacts / 0 changes**

## Runtime correction

Speech-only normalization was extended for frequent Unit 7 population-genetics, phylogeny, and age notation. Visible science and all six frozen narratives are unchanged.

## Mainline runtime

The live API reports `v2-apbio-0.28.0-u7-f6`. Units 1–7 remain student released. Unit 7 reports `STUDENT_READY`, `UNIT7_CLASSROOM_BROWSER_VALIDATED_F6`, and `PASS_F6`.

## Protected curriculum

All Unit 7 F5 curriculum artifacts remain byte-identical to the F5 content lock. The six narrative hashes remain unchanged from their frozen releases. The only intentional shared runtime changes after F5 are the F6 version label in `backend/main.py` and speech preparation in `frontend/js/audio.js`.

## Forbidden-file scan

The repository and final archive contain zero forbidden release artifacts in these categories.

- source PDFs
- `.git`
- exact `.env`
- SQLite/database files
- Python `__pycache__`
- `.pyc` / `.pyo`
- `.pytest_cache`

`.env.example` remains intentionally included as a safe configuration template.

## Integrity

The final ZIP is opened and every member is tested with the archive integrity checker before release.

## Next curriculum stage

Begin Unit 8 source inventory and scientific locking from the frozen Units 1–7 F6 baseline.

## GitHub CI compatibility correction · 2026-09-09

A historical-gate compatibility defect was found after the original F6 archive was exercised in GitHub Actions. `scripts/qa_unit6_f5.py` accepted the Unit 7 F5 lock as a later runtime state but did not yet accept the subsequent Unit 7 F6 runtime lock. The corrected gate now accepts a changed shared runtime file only when the file's exact current SHA-256 is explicitly recorded by a content lock belonging to a later unit. This fixes the Unit 6 F5 CI failure for `backend/main.py` and `frontend/js/audio.js` without weakening byte-lock validation or changing curriculum/runtime content.

The corrected package passes `qa_unit6_f5.py`, the complete Unit 1–7 QA chain, 372/372 Python tests, JavaScript syntax checks, Python compilation, and a clean `git diff --exit-code` reproducibility check.
