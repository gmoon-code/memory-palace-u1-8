# Unit 8 F6 Integration Audit

## Runtime surface

- runtime version `v2-apbio-0.30.0-u8-f6`
- Unit 8 API status `STUDENT_READY`
- Unit 8 pipeline stage `UNIT8_CLASSROOM_BROWSER_VALIDATED_F6`
- Unit 8 browser validation `PASS_F6`
- 8 Unit 8 journeys served
- 58 Unit 8 scenes served
- 13 Challenge Lab tasks served
- 135 exact-name Review targets served
- 40 mixed-discrimination sets and 104 questions served
- 31 scope guards served through the development API
- zero unaccounted Unit 8 canonical records

## Browser-facing functional matrix

- 58 / 58 production scene renders **PASS**
- 18 / 18 hidden Quick Recall renders **PASS**
- 174 scene/viewport responsive-contract checks **PASS**
- 54 recall/viewport responsive-contract checks **PASS**
- three stable stage zones per scene **PASS**
- hidden recall does not expose story, route, cast, location panel, or memory anchors **PASS**
- active route auto-centering contract **PASS**
- responsive desktop/tablet/phone CSS contract **PASS**
- refresh/resume persistence **PASS**
- released-unit switching among Units 1–8 **PASS**
- unit-scoped Review isolation **PASS**
- five-item visible Review cap **PASS**
- 48-hour mixed-discrimination delay **PASS**
- 13 / 13 Challenge Lab progression and answer-guide renders **PASS**
- Unit 8 speech preparation normalization **PASS**

## Frozen curriculum protection

All F5 curriculum artifacts remain byte-identical to the Unit 8 F5 content lock. All eight narrative files remain byte-identical to their protected F4/F5 hashes. All protected Unit 8 F1–F4 content locks remain unchanged.

The only shared runtime files intentionally changed from the F5 runtime lock are

- `backend/main.py` for the F6 runtime version label
- `frontend/js/audio.js` for speech-only normalization

No visible scientific text changed.

Comparison with the F5 release baseline confirms **421 / 421 Units 1–7 content files remain byte-identical**.

## Browser limitation

The installed Chromium executable timed out during a 12-second headless `about:blank` probe and produced no DOM output. The release records this limitation explicitly and makes no screenshot-level or pixel-level claim.

## Live HTTP/API smoke

A real Uvicorn process was started on localhost. HTTP 200 was confirmed for

- `/api/health`
- `/api/units/unit-8`
- `/api/units/unit-8/journeys`
- `/api/units/unit-8/journeys/U8-J1` through `U8-J8`
- `/api/units/unit-8/application-lab`
- `/api/units/unit-8/review-manifest`
- `/api/units/unit-8/mixed-discrimination`
- `/api/units/unit-8/scope-guards`
- `/api/units/unit-8/finalization`

The health endpoint returned `v2-apbio-0.30.0-u8-f6`.

## Deterministic build

The F6 builder was rerun against nine core generated/runtime artifacts and produced **0 changes**.

## Historical compatibility corrections

Historical QA/tests that had hard-coded the Unit 8 F5 runtime or status now accept the later F6 state only when the exact F6 lock/runtime is present. This affects QA/test compatibility code and does not modify prior unit curriculum artifacts.

The GitHub Actions sequence validates historical Unit 8 F5 without invoking the F5 builder, then runs the Unit 8 F6 builder, F6 Python QA, F6 UI-logic QA, and the final Units 1–8 mainline gate before repository-cleanliness verification.

## Decision

**PASS. Unit 8 is integrated as the final F6-validated AP Biology release without curriculum or narrative drift.**
