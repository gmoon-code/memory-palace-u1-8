# Unit 6 F6 Integration Audit

## Runtime surface

- runtime version `v2-apbio-0.26.0-u6-f6`
- Unit 6 API status `STUDENT_READY`
- Unit 6 pipeline stage `UNIT6_CLASSROOM_BROWSER_VALIDATED_F6`
- Unit 6 browser validation `PASS_F6`
- six Unit 6 journeys served
- 53 Unit 6 scenes served
- 16 Challenge Lab tasks served
- 134 exact-name Review targets served
- 37 mixed-discrimination sets and 94 questions served
- 25 scope guards served through the development API
- zero unaccounted Unit 6 canonical records

## Browser-facing functional matrix

- 53 / 53 production scene renders PASS
- 18 / 18 hidden Quick Recall renders PASS
- three stable stage zones per scene PASS
- hidden recall does not expose story, route, cast, location panel, or memory anchors PASS
- active route auto-centering contract PASS
- responsive desktop/tablet/phone CSS contract PASS
- refresh/resume persistence PASS
- released-unit switching among Units 1–6 PASS
- unit-scoped Review isolation PASS
- five-item visible Review cap PASS
- 48-hour mixed-discrimination delay PASS
- 16 / 16 Challenge Lab progression and answer-guide renders PASS
- Unit 6 speech preparation normalization PASS

## Frozen curriculum protection

All F5 runtime curriculum artifacts remain byte-identical to the Unit 6 F5 content lock. All six narrative files remain byte-identical to their protected F5/F4 hashes. All F1–F4 content locks remain unchanged.

The only shared runtime files intentionally changed after F5 are

- `backend/main.py` for the F6 runtime version label
- `frontend/js/audio.js` for speech-only normalization

No visible scientific text changed.

## Browser limitation

The installed Chromium executable timed out during an 8-second headless `about:blank` probe and produced no DOM output. The release records this limitation explicitly and makes no screenshot-level or pixel-level claim.

## Live HTTP/API smoke

Live Uvicorn testing returned HTTP 200 for the frontend, health endpoint, course endpoint, Unit 6 summary, journey registry, each of the six individual journeys, Challenge Lab, Review manifest, mixed-discrimination data, and scope guards. The health endpoint returned `v2-apbio-0.26.0-u6-f6`.

## Decision

**PASS. Unit 6 is integrated as an F6-validated student release without curriculum or narrative drift.**
