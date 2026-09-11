# Unit 7 F6 Classroom and Browser-Facing QA

## Scope

F6 changes no Unit 7 canonical science, F2 learning architecture, F3 scene briefs, F4A–F4F narrative bytes, F5 Memory Objects, Challenge Lab science, Review targets, mixed-discrimination content, or scope guards. It validates the released learner experience across Home, Learn, Quick Recall, Review, mixed discrimination, Challenge Lab, unit switching, persistence, responsive UI contracts, and browser speech text.

## Runtime render and responsive contract matrix

- Permanent scenes rendered through the production view function: **55 / 55**
- Quick Recall states rendered through the production view function: **18 / 18**
- Target responsive contracts: **1440×1000 desktop, 820×1180 tablet, 390×844 phone**
- Scene/viewport contract checks: **165**
- Recall/viewport contract checks: **54**
- Three-zone scene geometry findings: **0**
- Quick Recall story/location/route/cast/anchor leaks: **0**
- Broken interpolation findings: **0**

### Rendering limitation

Chromium was directly probed with an 8-second headless `about:blank` render and timed out without DOM output in this sandbox. F6 therefore does **not** claim screenshot-level or pixel-level browser validation. The release uses production HTML rendering functions, state-machine interaction tests, responsive CSS contract checks, and live FastAPI/browser-facing HTTP smoke tests.

## F6 runtime correction

Browser speech text now normalizes Unit 7 population-genetics and phylogeny notation including p², q², 2pq, N0–N4, and bya/mya age abbreviations. This changes speech preparation only; visible scientific text and all six narratives remain unchanged.

## Learning-system validation

- Exact-name delayed-review targets: **94**
- Meaning/mechanism-only palace records: **80**
- Mixed-discrimination sets: **33**
- Mixed-discrimination questions: **102**
- Mixed review waits at least **48 hours** after eligibility.
- Visible Review remains capped at **5** due items.
- Unit-scoped Review isolation: **PASS**
- Refresh/resume state: **PASS**
- Unit 7 Challenge Lab: **16 / 16** tasks
- Released-unit switching among Units 1–7: **PASS**

## Release decision

**PASS — Unit 7 remains student-ready and has completed F6 functional browser-facing/classroom validation.**
