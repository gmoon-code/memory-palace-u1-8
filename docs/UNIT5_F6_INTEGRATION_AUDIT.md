# Unit 5 F6 Integration Audit

## Release state

Unit 5 · Heredity remains student-ready after F6 functional browser-facing/classroom validation.

- Runtime version `v2-apbio-0.24.0-u5-f6`
- Canonical records 152 / 152 accounted
- Runtime story Memory Objects 131
- Challenge Lab items 16
- Scope guards 5
- Guided journeys 8
- Permanent scenes/loci 50
- Optional first-exposure Quick Recalls 18
- Exact-name Review targets 130
- Meaning/mechanism-only palace records 1
- Mixed-discrimination sets 32
- Mixed-discrimination questions 79

F6 changes no Unit 5 scientific curriculum or narrative text.

## F6 functional browser-facing checks

- Production scene renders 50 / 50
- Production hidden-recall renders 18 / 18
- Target responsive contracts desktop 1440×1000, tablet 820×1180, phone 390×844
- Scene/viewport contract checks 150
- Recall/viewport contract checks 54
- Three-zone spatial-layout findings 0
- Recall content-leak findings 0
- Broken interpolation findings 0
- Refresh/resume state PASS
- Released-unit switching among Units 1–5 PASS
- Unit-scoped Review isolation PASS
- Exact-name Review queue 130 / 130
- Mixed-discrimination queue after eligibility 32 / 32
- Mixed-discrimination questions 79
- Minimum mixed-review delay 48 hours
- Visible due-review cap 5
- Challenge Lab progression 16 / 16

### Browser rendering limitation

The installed Chromium executable in this sandbox timed out even on an `about:blank` headless render. F6 therefore does not claim screenshot-level or pixel-level browser validation. The checks above use production HTML rendering functions, state-machine interaction tests, responsive CSS contracts, and live FastAPI/browser-facing HTTP behavior.

## F6 runtime correction

Browser speech-only normalization now covers RNA, F1/F2, XX/XY, ABO, IA/IB, UV, HBB, 2n, χ², and common genotype notation while preserving visible scientific text.

## Historical regression

- Unit 1 full QA PASS
- Unit 2 F5 PASS
- Unit 3 F6 PASS
- Unit 4 F6 PASS
- Unit 5 F1–F6 PASS
- Units 1–3 mainline gate PASS
- Units 1–4 mainline gate PASS
- Units 1–5 mainline gate PASS
- Unit 3 UI-logic QA PASS
- Unit 4 UI-logic QA PASS
- Unit 5 F6 UI-logic QA PASS
- Python automated tests **256 / 256 PASS**
- Frontend JavaScript syntax checks PASS
- Python compilation PASS
- Unit 5 F6 deterministic rebuild **7 checked artifacts / 0 changes**
- Released Units 1–4 protected files **216 / 216 unchanged**

## Live server smoke

A live FastAPI process served the F6 repository successfully.

- `/api/health` PASS, `v2-apbio-0.24.0-u5-f6`
- `/api/units/unit-5` PASS, `STUDENT_READY`, `PASS_F6`
- `/api/units/unit-5/journeys` PASS, 8 journeys
- `/api/units/unit-5/review-manifest` PASS, 130 targets
- `/api/units/unit-5/mixed-discrimination` PASS, 32 sets / 79 questions
- `/api/units/unit-5/application-lab` PASS, 16 challenges
- `/api/units/unit-5/scope-guards` PASS, 5 guards
- `/` HTTP 200

## Decision

**PASS. Unit 5 is complete through F6.**

The next curriculum-development gate is Unit 6 scientific locking. No Unit 6 narrative should be generated before source inventory, scientific atomization, AP scope mapping, conflict/misconception audit, and canonical locking pass.
