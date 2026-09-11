# Memory Palace V2 · Unit 7 F5 Package QA

## Result

**PASS**

## Package role

This release preserves the validated Units 1–6 curriculum and every Unit 7 F1–F4F scientific, architectural, scene-brief, and narrative lock, then adds the Unit 7 F5 student-ready curriculum/runtime integration.

## F5 curriculum accounting

- Canonical Unit 7 records: **215 / 215 accounted**
- Runtime story Memory Objects: **174**
- Challenge Lab records/tasks: **16 / 16**
- Non-runtime scope guards: **25 / 25**
- Unaccounted canonical records: **0**
- Guided journeys: **6 / 6**
- Permanent scenes: **55 / 55**
- Optional first-exposure Quick Recalls: **18 / 18**
- Exact-name delayed Review targets: **94 / 94**
- Meaning/mechanism-only palace records: **80**
- Mixed-discrimination sets: **33**
- Mixed-discrimination questions: **102**
- Mandatory spelling targets: **0**

The zero-loss partition is **174 + 16 + 25 = 215**.

## Scientific and narrative protection

- Unit 7 F1 scientific lock: **PASS**
- Unit 7 F2 learning architecture lock: **PASS**
- Unit 7 F3 science-bearing scene-brief lock: **PASS**
- Unit 7 F4A–F4F narrative locks: **PASS**
- All six frozen Journey JSON files remain protected by the F5 lock.
- Released Units 1–6 protection remains **PASS** against the historical release locks.

## Deterministic build

The corrected F5 builder was executed twice against the same repository state.

```text
Core artifacts checked     15
Changed artifacts           0
Duplicate Unit 7 helpers    0
```

The F5 build is therefore reproducible and idempotent.

## Complete regression

- Unit 1 full QA: **PASS**
- Unit 2 F5 QA: **PASS**
- Unit 3 F6 QA: **PASS**
- Unit 4 F6 QA: **PASS**
- Unit 5 F6 QA: **PASS**
- Unit 6 F6 QA: **PASS**
- Units 1–6 mainline QA: **PASS**
- Unit 7 F1 QA: **PASS**
- Unit 7 F2 QA: **PASS**
- Unit 7 F3 QA: **PASS**
- Unit 7 F4A QA: **PASS**
- Unit 7 F4B QA: **PASS**
- Unit 7 F4C QA: **PASS**
- Unit 7 F4D QA: **PASS**
- Unit 7 F4E QA: **PASS**
- Unit 7 F4F QA: **PASS**
- Unit 7 F5 QA: **PASS**
- Units 1–7 mainline QA: **PASS**
- Python tests: **367 / 367 PASS**
- Unit 3–6 UI-logic QA: **PASS**
- JavaScript syntax checks: **PASS**
- Python compilation: **PASS**

The Unit 6 UI regression was also advanced to recognize Unit 7 as a released switchable unit while continuing to hide Unit 8.

## Live HTTP/API validation

The live FastAPI application reports

```text
runtime                         v2-apbio-0.27.0-u7-f5
student-ready units             7
Unit 7 guided journeys          6
Unit 7 scene route lengths      10, 14, 9, 8, 9, 5
Unit 7 Challenge Lab tasks      16
Unit 7 Review targets           94
non-exact palace records        80
mixed-discrimination sets       33
mixed questions                 102
scope guards                    25
canonical records               215
unaccounted records             0
```

The root page, course API, Unit 7 status, all six Journey endpoints, Challenge Lab, Review manifest, mixed-discrimination manifest, scope-guard endpoint, finalization endpoint, and a released Unit 7 Memory Object all returned successfully.

## Archive hygiene

The final archive contains **981 entries**.

- source PDFs: **0**
- `.git`: **0**
- exact `.env`: **0**
- SQLite/database files: **0**
- Python caches: **0**
- pytest caches: **0**
- compiled Python files: **0**
- ZIP integrity: **PASS**

## Runtime boundary

```text
v2-apbio-0.27.0-u7-f5
```

Unit 7 is student-ready at F5. F6 remains the final classroom/browser-facing validation gate and must not change the frozen curriculum.
