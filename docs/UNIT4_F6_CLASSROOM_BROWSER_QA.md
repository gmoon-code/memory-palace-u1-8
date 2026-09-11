# Unit 4 F6 Classroom and Browser-Facing QA

## Scope

F6 changes no Unit 4 curriculum, scientific lock, permanent palace architecture, or narrative science. It validates the released learner experience across Home, Learn, Quick Recall, Review, mixed discrimination, Challenge Lab, unit switching, persistence, responsive UI contracts, and browser speech text.

## Runtime render and responsive contract matrix

- Permanent scenes rendered through the production view function: **51 / 51**
- Quick Recall scenes rendered through the production view function: **18 / 18**
- Target responsive contracts: **1440×1000 desktop, 820×1180 tablet, 390×844 phone**
- Scene/viewport contract checks: **153**
- Recall/viewport contract checks: **54**
- Three-zone scene geometry findings: **0**
- Quick Recall story/location/route/cast/anchor leaks: **0**
- Broken interpolation findings: **0**

### Rendering limitation

The Chromium executable installed in this sandbox did not complete even an `about:blank` headless render. F6 therefore does **not** claim screenshot-level or pixel-level browser validation. The release uses production HTML rendering functions, state-machine interaction tests, responsive CSS contract checks, and live FastAPI/browser-facing HTTP smoke tests.

## F6 runtime corrections

1. Exact-name Review now provides **Continue review** after a learner reveals a hint/answer, so the learner can advance directly to the next due item.
2. Browser speech text now normalizes frequent Unit 4 abbreviations and phase labels including DNA, GPCR, GDP, GTP, cAMP, CDK, APC, G1, G2, and G0 while leaving visible scientific text unchanged.

## Learning-system validation

- Exact-name delayed-review targets: **162**
- Mixed-discrimination sets: **33**
- Mixed-discrimination questions: **99**
- Mixed review waits at least **48 hours** after eligibility.
- Visible Review remains capped at **5** due items.
- Unit-scoped Review isolation: **PASS**
- Refresh/resume state: **PASS**
- Unit 4 Challenge Lab: **15 / 15** tasks
- Released-unit switching among Units 1–4: **PASS**

## Release decision

**PASS — Unit 4 remains student-ready and has completed F6 functional browser-facing/classroom validation.**
