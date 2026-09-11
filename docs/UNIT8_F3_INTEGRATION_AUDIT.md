# AP Biology Unit 8 F3 Integration Audit

## Baseline

The build used the uploaded Unit 7 F6 CI-fix archive as the Units 1–7 baseline. Its runtime manifest remains `v2-apbio-0.28.0-u7-f6`, and the baseline completed 372 pytest checks before Unit 8 integration.

## Protected upstream content

All files under `content/ap-biology/unit-1` through `content/ap-biology/unit-7` remain byte-identical to the uploaded baseline. Backend and frontend runtime source files remain byte-identical. Unit 8 changes are developer content plus course-registry/documentation/QA metadata; no Unit 8 learner runtime route is enabled.

## Unit 8 locks

- F1 canonical science remains protected by F3 content-lock hashes.
- F2 classification and palace architecture remain protected by F3 content-lock hashes.
- F3 adds 8 journey briefs and 58 scene briefs covering 211 palace-managed records exactly once.
- 211 term introductions reproduce F1 canonical labels and verified statements exactly.
- 18 optional first-exposure Quick Recalls are distributed 2 / 3 / 2 / 2 / 2 / 3 / 2 / 2 across the eight journeys.
- Unit 8 student runtime journeys, scenes, Memory Objects, and Challenge Lab tasks remain zero.

## Runtime boundary

Units 1–7 remain the only student-ready units. The API runtime version remains `v2-apbio-0.28.0-u7-f6`. Unit 8 is registered as `SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED`.

## Next gate

Unit 8 F4A may write Journey 1 only from the locked Behavioral Response Institute briefs.
