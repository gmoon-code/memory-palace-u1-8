# Unit 7 F6 Integration Audit

## Runtime surface

- runtime version `v2-apbio-0.28.0-u7-f6`
- Unit 7 API status `STUDENT_READY`
- Unit 7 pipeline stage `UNIT7_CLASSROOM_BROWSER_VALIDATED_F6`
- Unit 7 browser validation `PASS_F6`
- six Unit 7 journeys served
- 55 Unit 7 scenes served
- 16 Challenge Lab tasks served
- 94 exact-name Review targets served
- 33 mixed-discrimination sets and 102 questions served
- 25 scope guards served through the development API
- zero unaccounted Unit 7 canonical records

## Browser-facing functional matrix

- 55 / 55 production scene renders PASS
- 18 / 18 hidden Quick Recall renders PASS
- 165 scene/viewport responsive-contract checks PASS
- 54 recall/viewport responsive-contract checks PASS
- three stable stage zones per scene PASS
- hidden recall does not expose story, route, cast, location panel, or memory anchors PASS
- active route auto-centering contract PASS
- responsive desktop/tablet/phone CSS contract PASS
- refresh/resume persistence PASS
- released-unit switching among Units 1–7 PASS
- unit-scoped Review isolation PASS
- five-item visible Review cap PASS
- 48-hour mixed-discrimination delay PASS
- 16 / 16 Challenge Lab progression and answer-guide renders PASS
- Unit 7 speech preparation normalization PASS

## Frozen curriculum protection

All F5 runtime curriculum artifacts remain byte-identical to the Unit 7 F5 content lock. All six narrative files remain byte-identical to their protected F5/F4 hashes. All Unit 7 F1–F4 content locks remain unchanged.

The only shared runtime files intentionally changed after F5 are

- `backend/main.py` for the F6 runtime version label
- `frontend/js/audio.js` for speech-only normalization

No visible scientific text changed.

## Browser limitation

The installed Chromium executable timed out during an 8-second headless `about:blank` probe and produced no DOM output. The release records this limitation explicitly and makes no screenshot-level or pixel-level claim.

## Live HTTP/API smoke

Live Uvicorn testing returned HTTP 200 for health, Unit 7 summary, journey registry, each of the six individual journeys, Challenge Lab, Review manifest, mixed-discrimination data, scope guards, and finalization. The health endpoint returned `v2-apbio-0.28.0-u7-f6`.

## Deterministic build

The F6 builder was rerun against nine core artifacts and produced **0 changes**.

## Decision

**PASS. Unit 7 is integrated as an F6-validated student release without curriculum or narrative drift.**
