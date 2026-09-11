# Unit 8 F5 Curriculum and Runtime QA

## Result

**PASS**

Unit 8 F5 has completed curriculum finalization and functional runtime integration. The release is student-ready. F6 remains the separate final classroom/browser-facing validation gate.

## Curriculum accounting

- Canonical records: **255 / 255 accounted**
- Runtime story Memory Objects: **211**
- Challenge Lab records: **13**
- Non-runtime scope guards: **31**
- Unaccounted canonical records: **0**
- Guided journeys: **8**
- Permanent scenes: **58**
- Optional first-exposure Quick Recalls: **18**
- Exact-name Review targets: **135**
- Meaning/mechanism-only palace records: **76**
- Mixed-discrimination sets: **40**
- Mixed-discrimination questions: **104**
- Mandatory spelling targets: **0**

## Frozen upstream layers

- F1 canonical science remains locked.
- F2 architecture remains locked at 8 journeys, 22 bundles, and 58 loci.
- F3 remains locked at 58 science-bearing scene briefs and 211 palace-managed records.
- F4A through F4H remain frozen at 8 polished journeys, 58 scenes, 211 represented records, 18 optional recalls, and 32,094 narrative words.
- Historical F3 and F4 QA now accept the later `UNIT8_FINALIZED_F5` runtime state while continuing to verify their original locked artifacts and boundaries.

## Review and Challenge Lab checks

- Every exact-name target is derived from the F2 `exact_name_recall` decision.
- Review prompts hide the direct target answer while preserving the locked scientific meaning.
- Mixed-discrimination prompts preserve negation, causal operators, and mechanism language needed to distinguish scientifically close choices.
- Mixed practice remains delayed at least 48 hours and the visible due queue remains capped at five items.
- All 13 PRACTICE_ONLY records become Challenge Lab tasks and remain outside the 58 permanent loci.
- All 31 scope guards remain non-runtime constraints.

## Runtime checks

- Runtime version: `v2-apbio-0.29.0-u8-f5`
- Unit 8 is exposed through the same unit-generic API and learner interface as prior units.
- Live API checks pass for Unit 8 status, 8 journey records, 13 Challenge Lab items, 135 Review targets, 40 mixed sets, 31 scope guards, zero-loss finalization, and Memory Object lookup.
- Production UI logic renders **58 / 58 scenes** and **18 / 18 hidden recall states**.
- Responsive contracts cover desktop `1440×1000`, tablet `820×1180`, and phone `390×844`, producing **174 scene/viewport checks** and **54 recall/viewport checks**.
- Units 1–8 switching, refresh/resume persistence, Review scheduling, the five-item visible cap, and Challenge Lab routing pass.

## Regression

- Python suite: **428 / 428 passing**.
- Unit 8 F3 and F4A through F4H historical QA: **PASS**.
- Unit 8 F5 QA: **PASS**.
- Units 1–8 mainline QA: **PASS**.
- Unit 7 F6 regression: **PASS**.
- Unit 3 through Unit 8 UI-logic regression: **PASS**.
- JavaScript syntax validation: **PASS**.
- Python compilation: **PASS**.
- GitHub Actions YAML parse: **PASS**.
- Exact GitHub Actions command sequence was executed in a clean probe copy and produced **0 changed, 0 added, and 0 removed tracked repository files** relative to the F5 source tree after cache exclusion.

## Deterministic builder

The F5 builder was stabilized so repeated execution does not duplicate the Unit 8 settings import. A second deterministic rebuild checked **16 generated/runtime integration artifacts** and changed **0**. The F5 content lock therefore remains stable across repeated builds.

## Validation boundary

F5 validates curriculum finalization and functional integration. It does not claim final screenshot-level or classroom/browser-facing validation. That remains the Unit 8 F6 gate.
