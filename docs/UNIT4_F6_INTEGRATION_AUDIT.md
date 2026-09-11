# Unit 4 F6 Integration Audit

## Release state

Unit 4 · Cell Communication and Cell Cycle remains student-ready after F6 functional browser-facing/classroom validation.

- Runtime version: `v2-apbio-0.22.0-u4-f6`
- Canonical records: 180 / 180 accounted
- Runtime story Memory Objects: 162
- Challenge Lab items: 15
- Scope guards: 3
- Guided journeys: 7
- Permanent scenes/loci: 51
- Optional first-exposure Quick Recalls: 18
- Exact-name Review targets: 162
- Mixed-discrimination sets: 33
- Mixed-discrimination questions: 99

F6 changes no Unit 4 scientific curriculum or narrative text.

## F6 functional browser-facing checks

- Production scene renders: 51 / 51
- Production hidden-recall renders: 18 / 18
- Target responsive contracts: desktop 1440×1000, tablet 820×1180, phone 390×844
- Scene/viewport contract checks: 153
- Recall/viewport contract checks: 54
- Three-zone spatial-layout findings: 0
- Recall content-leak findings: 0
- Broken interpolation findings: 0
- Refresh/resume state: PASS
- Released-unit switching: PASS
- Unit-scoped Review isolation: PASS
- Exact-name Review queue: 162 / 162
- Mixed-discrimination queue after eligibility: 33 / 33
- Minimum mixed-review delay: 48 hours
- Visible due-review cap: 5
- Challenge Lab progression: 15 / 15

### Browser rendering limitation

The installed Chromium executable in this sandbox does not complete even an `about:blank` headless render. F6 therefore does not claim screenshot-level or pixel-level browser validation. The checks above use the production HTML rendering functions, state-machine interaction tests, responsive CSS contracts, and live FastAPI/browser-facing HTTP behavior.

## F6 runtime corrections

1. Exact-name Review hints now reveal a **Continue review** button so learners can move directly to the next due item.
2. Browser speech-only normalization now covers DNA, GPCR, GDP, GTP, cAMP, CDK/CDKs, APC/APCs, G1, G2, and G0 while preserving the visible scientific text.

## Historical regression

The GitHub Actions build sequence was run from a temporary Git baseline, excluding only the package-install step because dependencies were already present in this sandbox. The project build itself returned to zero Git diff.

- Unit 1 historical build and QA: PASS
- Unit 2 F1–F5: PASS
- Unit 3 F1–F6: PASS
- Unit 4 F1–F6: PASS
- Units 1–3 mainline gate: PASS
- Units 1–4 mainline gate: PASS
- Unit 3 UI-logic QA: PASS
- Unit 4 F6 UI-logic QA: PASS
- Python automated tests: **198 / 198 PASS**
- Frontend JavaScript syntax checks: PASS
- Deterministic generated-content rebuild: PASS
- Git diff after rebuild: zero

## Live server smoke

A live FastAPI process served the F6 repository successfully.

- `/api/health`: PASS, `v2-apbio-0.22.0-u4-f6`
- `/api/units/unit-4`: PASS, `STUDENT_READY`, `PASS_F6`
- `/api/units/unit-4/journeys`: PASS, 7 journeys
- `/api/units/unit-4/review-manifest`: PASS, 162 targets
- `/api/units/unit-4/mixed-discrimination`: PASS, 33 sets / 99 questions
- `/api/units/unit-4/application-lab`: PASS, 15 challenges
- `/?unit=unit-4`: HTTP 200
- `/static/js/app.js`: HTTP 200 and F6 Review continuation present

## Decision

**PASS. Unit 4 is complete through F6.**

The next curriculum-development gate is Unit 5 scientific locking. No Unit 5 narrative should be generated before source inventory, scientific atomization, AP scope mapping, conflict/misconception audit, and canonical locking pass.
