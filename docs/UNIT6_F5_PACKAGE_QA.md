# Unit 6 F5 Package QA

## Result

**PASS**

## Package

`MemoryPalace_V2_Mainline_Units1-6_Unit6-F5.zip`

The archive contains **831 entries** and passes ZIP integrity checking.

## Included release state

- Units 1–6 student-ready runtime
- Unit 6 F1 scientific lock preserved
- Unit 6 F2 learning architecture preserved
- Unit 6 F3 scene briefs preserved
- all six Unit 6 F4 narratives polished and byte-frozen
- Unit 6 canonical records **202 / 202 accounted**
- Unit 6 runtime Memory Objects **161**
- Unit 6 guided journeys **6**
- Unit 6 permanent scenes/loci **53**
- Unit 6 optional first-exposure Quick Recalls **18**
- Unit 6 delayed exact-name Review targets **134**
- Unit 6 mixed-discrimination sets **37**
- Unit 6 mixed-discrimination questions **94**
- Unit 6 Challenge Lab tasks **16**
- Unit 6 non-runtime scope guards **25**
- Unit 6 unaccounted canonical records **0**
- Unit 6 student release **true**

The zero-loss Unit 6 partition is **161 story/runtime records + 16 Challenge Lab records + 25 scope guards = 202 canonical records**.

## Mainline accounting

Units 1–6 contain **1,091 canonical records, 44 guided journeys, 335 permanent scenes/loci, and 83 Challenge Lab tasks**.

## Regression

- Unit 1 full QA: **PASS**
- Unit 2 F5: **PASS**
- Unit 3 F6: **PASS**
- Unit 4 F6: **PASS**
- Unit 5 F6: **PASS**
- historical Units 1–3 mainline QA: **PASS**
- historical Units 1–4 mainline QA: **PASS**
- historical Units 1–5 mainline QA: **PASS**
- current Units 1–6 mainline QA: **PASS**
- Unit 6 F1 through F5: **PASS**
- Python tests: **306 / 306 PASS**
- Unit 3 F6 UI-logic QA: **PASS**
- Unit 4 F6 UI-logic QA: **PASS**
- Unit 5 F6 UI-logic QA: **PASS**
- Unit 6 F5 UI-logic QA: **PASS**
- JavaScript syntax: **PASS**
- Python compilation: **PASS**
- live FastAPI behavior: **PASS**
- deterministic Unit 6 F2 → F5 rebuild: **74 checked artifacts / 0 changes**

## Runtime validation

The live API reports `v2-apbio-0.25.0-u6-f5` and serves all six Unit 6 journeys, 16 Challenge Lab tasks, 134 exact-name Review targets, 37 mixed sets containing 94 questions, 25 scope guards, and 161 runtime Memory Objects.

The Unit 6 UI-logic gate rendered all **53 production scene states** and all **18 hidden Quick Recall states**, queued all **134 exact-name targets**, scheduled all **37 mixed sets**, preserved the **five-item visible Review limit**, and exposed all **16 Challenge Lab tasks**.

## Frozen narrative hashes

- U6-J1 `fe01ed27cd6a8830022f131c22bcce74f9ad094aef189c991effb66f09741b83`
- U6-J2 `62745c2fdcf98af10667a7cefa9907b420036952050d59aea7231dbd66de1ec6`
- U6-J3 `91995e5f1e8f30072d511701556214fa16ba28b8533b460719bfe5b136722715`
- U6-J4 `e074f28b35de6fe96de2015b1d8732055bc238235fa87367cf1976cb1df30b89`
- U6-J5 `23b21efa45badeaef8db794af47f6fed87a623758e3c87487de2dcd68326aac1`
- U6-J6 `cbb16bdd2ca5e9f386150860c5b802c93fadae25ff918db7bc366190f1f6c95c`

## Protected upstream state

The Unit 6 upstream-protection manifest covers **291 Units 1–5 content files**. Those files remain protected by the cumulative regression gates. Unit 6 F5 extends shared runtime files only through the current Unit 6 runtime content lock.

## Forbidden-file scan

The repository and final archive contain zero forbidden release artifacts in these categories.

- source PDFs
- `.git`
- `.env`
- SQLite/database files
- Python `__pycache__`
- `.pyc` / `.pyo`
- `.pytest_cache`

`.env.example` remains intentionally included as a safe configuration template.

## Validation boundary

F5 is the student-ready runtime-finalization gate. It does not claim screenshot-level or pixel-level browser validation. Responsive classroom/browser-facing validation is reserved for Unit 6 F6.

## Integrity

The final ZIP was opened and every member was tested with the archive integrity checker before release.
