# Memory Palace V2 · Units 1–8 Mainline Release Audit

## Release state

AP Biology Units **1 through 8** are student-ready. Unit 8 has completed the final **F6 classroom/browser-facing validation gate**, completing the current AP Biology Units 1–8 release sequence.

Current runtime

```text
v2-apbio-0.30.0-u8-f6
```

## Consolidated accounting

| Measure | Units 1–8 |
|---|---:|
| Canonical records | **1,561** |
| Guided journeys | **58** |
| Permanent scenes | **448** |
| Challenge Lab items | **112** |

## Unit 8 contribution

Unit 8 contributes **255** canonical records, **211** runtime Memory Objects, **8** guided journeys, **58** permanent scenes, **18** optional first-exposure Quick Recalls, **13** Challenge Lab tasks, **135** exact-name Review targets, **76** meaning/mechanism-only palace records, **40** mixed-discrimination sets with **104** questions, and **31** non-runtime scope guards.

The Unit 8 zero-loss partition is **211 + 13 + 31 = 255**.

## F6 validation

The production rendering layer passes **58 / 58 scene renders** and **18 / 18 hidden Quick Recall renders**. Responsive contracts cover desktop, tablet, and phone targets, producing **174 scene/viewport** and **54 recall/viewport** checks.

State-machine validation passes for Units 1–8 switching, refresh/resume, exact-name Review scheduling, mixed-discrimination eligibility and delay, the five-item visible Review cap, and all 13 Unit 8 Challenge Lab tasks. Live Uvicorn/FastAPI smoke testing returns HTTP 200 for the health endpoint, Unit 8 summary, journey registry, all eight individual journeys, Challenge Lab, Review manifest, mixed-discrimination data, scope guards, and finalization.

Chromium timed out during a 12-second headless `about:blank` probe in the release container, so the release makes no screenshot-level or pixel-level claim.

## Curriculum preservation

The eight F4 narrative journeys remain frozen. F6 does not alter F1 science, F2 architecture, F3 scene briefs, F4 narratives, F5 Memory Objects, Review targets, mixed-discrimination content, Challenge Lab science, or scope guards.

Units 1–7 content remains frozen. Release comparison confirms **421 / 421 Units 1–7 content files unchanged** from the Unit 8 F5 baseline.

## Machine-readable release

The final mainline manifest is `content/ap-biology/mainline-release-u1-u8.json`.

## Release decision

**PASS. Units 1–8 form the completed AP Biology F6-validated mainline.**
