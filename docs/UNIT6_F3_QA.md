# Unit 6 F3 QA

**PASS — SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED**

## Coverage and lock checks

- 53 / 53 permanent F2 loci have a scene brief.
- 161 / 161 palace-managed records are assigned once and introduced once.
- Every left/center/right anchor is byte-for-byte consistent with the F2 geometry.
- Every term introduction preserves its F1 canonical label and canonical science.
- Every record-level exact-name, delayed-review, name-support, spelling, and prior-unit-reactivation policy matches F2.
- Every applicable F1 review flag is carried into the scene's misconception guards.
- Every applicable F2 discrimination set is carried into scene-level confusable guards.
- Each scene contains three stable scientific actors/parts, a before/trigger/during/after mechanism, a conventional-visual contract, an exit-memory reconstruction target, and a causal handoff.
- 18 optional Quick Recall candidates are distributed as 3 / 3 / 3 / 4 / 3 / 2 across Journeys 1–6.
- Unit 6 remains at zero student runtime.

## Narrative boundary

F3 intentionally does not contain polished story paragraphs. The next gate is F4A Journey 1 only. Polished prose must retain the locked science, geometry, part identities, and causal action defined here.

## Regression result

The final F3 branch passed the full repository regression at the time of packaging.

```text
Python tests                         272 / 272 PASS
Unit 1 full QA                       PASS
Unit 2 F5                            PASS
Unit 3 F6                            PASS
Unit 4 F6                            PASS
Unit 5 F6                            PASS
Unit 6 F1                            PASS
Unit 6 F2                            PASS
Unit 6 F3                            PASS
Unit 3 UI logic                      PASS
Unit 4 UI logic                      PASS
Unit 5 UI logic                      PASS
Python compilation                   PASS
JavaScript syntax                    PASS
Live FastAPI boundary                PASS
F3 deterministic rebuild             PASS
Protected Units 1–5 files            291 / 291 unchanged
```

The live API reports Unit 6 as `SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED`, with zero guided journeys and zero Challenge Lab tasks. The public runtime version remains `v2-apbio-0.24.0-u5-f6`.
