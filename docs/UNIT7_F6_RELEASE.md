# Unit 7 F6 Release

Unit 7 · Natural Selection has completed F6 functional browser-facing/classroom validation. F6 changes no canonical science, F2 learning architecture, F3 scene briefs, F4A–F4F narrative bytes, F5 Memory Objects, Challenge Lab science, Review targets, mixed-discrimination content, or scope guards.

## Final Unit 7 state

- 215 / 215 canonical records accounted
- 174 runtime story Memory Objects
- 16 Challenge Lab application records
- 25 non-runtime scope guards
- 6 guided journeys
- 55 permanent scenes/loci
- 18 optional first-exposure Quick Recalls
- 94 exact-name delayed Review targets
- 80 meaning/mechanism-only palace records
- 33 mixed-discrimination sets with 102 questions
- 0 mandatory spelling gates
- student release remains enabled

The zero-loss partition remains **174 story/runtime records + 16 Challenge Lab records + 25 scope guards = 215 canonical records**.

## F6 browser-facing validation

The production rendering functions were exercised for all 55 Unit 7 scenes and all 18 hidden Quick Recall states. The responsive CSS contract was checked against desktop 1440×1000, tablet 820×1180, and phone 390×844 targets, producing 165 scene/viewport and 54 recall/viewport contract checks.

State-machine tests cover refresh/resume persistence, switching among released Units 1–7, all 94 delayed exact-name targets, all 33 mixed-discrimination sets and their 48-hour eligibility delay, the five-item visible Review limit, and all 16 Challenge Lab tasks.

Chromium was directly probed with an 8-second headless `about:blank` render and timed out without DOM output in this sandbox. This release therefore does **not** claim screenshot-level or pixel-level browser validation. F6 uses production HTML rendering, state-machine interaction QA, responsive CSS contract checks, and live FastAPI/browser-facing HTTP smoke tests.

## F6 runtime correction

Browser speech-only normalization now covers frequent Unit 7 notation including p², q², 2pq, N0–N4 phylogeny node labels, and bya/mya age abbreviations. Visible scientific wording and all six narrative files remain unchanged.

## Regression

- Unit 1 full QA **PASS**
- Unit 2 F5 **PASS**
- Units 3–6 F6 **PASS**
- Unit 7 F1 through F6 **PASS**
- Units 1–6 mainline **PASS**
- Units 1–7 mainline **PASS**
- Unit 3 through Unit 7 UI-logic QA **PASS**
- Python tests **372 / 372 PASS**
- JavaScript syntax **PASS**
- Python compilation **PASS**
- live HTTP/API **PASS**
- deterministic Unit 7 F6 rebuild **9 artifacts checked / 0 changes**

## Runtime

```text
v2-apbio-0.28.0-u7-f6
```

## Release decision

**PASS. Unit 7 remains student-ready and has completed the final F6 functional browser-facing/classroom validation gate.**

The next curriculum stage is Unit 8 source inventory and scientific locking from this frozen Units 1–7 baseline.
