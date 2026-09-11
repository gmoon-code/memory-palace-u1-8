# Unit 4 F6 Release

Unit 4 · Cell Communication and Cell Cycle has completed F6 functional browser-facing/classroom validation. F6 changes no scientific curriculum, permanent palace architecture, F3 scene briefs, or F4 narrative science.

## Final Unit 4 state

- 180 / 180 canonical records accounted
- 162 runtime story Memory Objects
- 15 Challenge Lab application records
- 3 non-runtime AP scope guards
- 7 guided journeys
- 51 permanent loci
- 18 optional first-exposure Quick Recalls
- 162 exact-name delayed Review targets
- 33 mixed-discrimination sets with 99 questions
- 0 mandatory spelling gates
- student release remains enabled

## F6 browser-facing validation

The production rendering functions were exercised for all 51 scenes and all 18 Quick Recall scenes. The responsive CSS contract was checked against desktop 1440×1000, tablet 820×1180, and phone 390×844 targets, producing 153 scene/viewport and 54 recall/viewport contract checks. State-machine tests cover unit switching, refresh/resume persistence, exact Review scheduling, mixed-discrimination eligibility and delay, the five-item visible Review limit, and all 15 Challenge Lab items.

The installed Chromium executable in this execution sandbox does not complete even an `about:blank` headless render. This release therefore does **not** claim screenshot-level or pixel-level browser validation. F6 uses production HTML rendering, state-machine interaction QA, responsive CSS contract checks, and live FastAPI/browser-facing HTTP smoke tests.

## F6 runtime corrections

1. After a learner requests a hint on an exact-name Review item, the revealed answer now includes a **Continue review** button so the learner can advance directly to the next due item.
2. Browser speech-only normalization now covers frequent Unit 4 abbreviations and labels including DNA, GPCR, GDP, GTP, cAMP, CDK/CDKs, APC/APCs, G1, G2, and G0. Visible scientific text is unchanged.

## Release decision

**PASS. Unit 4 remains student-ready and has completed F6 functional browser-facing/classroom validation.**

The next curriculum gate is Unit 5 scientific locking. Unit 5 narratives must not be generated before its source inventory, atomization, AP-scope mapping, conflict/misconception audit, and canonical scientific lock pass.
