# Unit 8 F6 Package QA

## Result

**PASS**

Unit 8 F6 completes the final functional browser-facing/classroom validation gate for Ecology while preserving the F1 scientific catalog, F2 architecture, F3 scene briefs, all eight F4 narratives, and the complete F5 runtime curriculum.

## Package

`MemoryPalace_V2_Mainline_Units1-8_Unit8-F6.zip`

The final repository contains **1,148 files**. With **61 directory entries including the repository root**, the ZIP contains **1,209 entries** and passes full archive integrity checking.

## Final Unit 8 accounting

- canonical records **255 / 255 accounted**
- runtime Memory Objects **211**
- guided journeys **8**
- permanent scenes/loci **58**
- optional first-exposure Quick Recalls **18**
- Challenge Lab items **13**
- scope guards **31**
- exact-name Review targets **135**
- meaning/mechanism-only palace records **76**
- mandatory spelling targets **0**
- mixed-discrimination sets **40**
- mixed-discrimination questions **104**
- unaccounted canonical records **0**

The zero-loss partition remains **211 story/runtime records + 13 Challenge Lab records + 31 scope guards = 255 canonical records**.

## Browser-facing validation

- production scene renders **58 / 58**
- hidden Quick Recall renders **18 / 18**
- responsive target contracts **desktop, tablet, phone**
- scene/viewport checks **174**
- recall/viewport checks **54**
- released-unit switching among Units 1–8 **PASS**
- refresh/resume persistence **PASS**
- unit-scoped Review **PASS**
- five-item visible Review cap **PASS**
- 48-hour mixed-discrimination delay **PASS**
- Challenge Lab **13 / 13 PASS**
- speech preparation **PASS**
- live Uvicorn/FastAPI HTTP/API **PASS**
- Chromium screenshot/pixel validation **not claimed because Chromium timed out during a 12-second headless `about:blank` probe**

## Regression gates

- Unit 1 full QA **PASS**
- Unit 2 F5 QA **PASS**
- Unit 3 F6 QA **PASS**
- Unit 4 F6 QA **PASS**
- Unit 5 F6 QA **PASS**
- Unit 6 F6 QA **PASS**
- Unit 7 F6 QA **PASS**
- Unit 8 F3 through F6 **PASS**
- current Units 1–8 mainline QA **PASS**
- Unit 3 through Unit 8 UI-logic QA **PASS**
- Python suite **433 / 433 PASS**
- frontend JavaScript syntax checks **PASS**
- Python compilation **PASS**
- deterministic Unit 8 F6 rebuild **9 checked artifacts / 0 changes**
- clean GitHub Actions command-sequence probe **0 tracked-file drift**

## Protected curriculum

Comparison against the exact Unit 8 F5 package baseline confirms **421 / 421 Units 1–7 content files are byte-identical**.

The Unit 8 F5 content lock also remains intact

- F5 locked files **9 / 9 unchanged**
- protected narratives **8 / 8 unchanged**
- protected upstream locks **11 / 11 unchanged**

The only intentional shared runtime changes from the F5 runtime lock are `backend/main.py` for the F6 version and `frontend/js/audio.js` for speech-only preparation.

## Historical QA compatibility

Later-state compatibility changes are limited to QA scripts, tests, workflow ordering, and current release documentation/metadata. Historical curriculum hashes remain enforced. The final workflow validates F5 without rebuilding it, then performs the deterministic F6 build and final F6/mainline gates.

## Forbidden-file scan

The repository and final archive contain zero forbidden release artifacts in these categories

- source PDFs
- `.git`
- exact `.env`
- SQLite/database files
- Python `__pycache__`
- `.pyc` / `.pyo`
- `.pytest_cache`

`.env.example` remains intentionally included as a safe configuration template.

## Integrity

The final ZIP is assembled deterministically, opened, and every member is tested with the ZIP integrity checker. A second independently assembled archive produces the same SHA-256 checksum.

## Release boundary

**AP Biology Units 1–8 are complete at F6. Freeze this package as the completed AP Biology baseline.**
