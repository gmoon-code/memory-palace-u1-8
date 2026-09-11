# Unit 5 F2 Package QA

## Release boundary

The package contains the validated student-ready Units 1–4 mainline plus the Unit 5 F1 scientific lock and Unit 5 F2 learning architecture. Unit 5 remains student-unreleased. The live runtime version therefore remains the validated Units 1–4 runtime `v2-apbio-0.22.0-u4-f6`.

## Unit 5 F2 accounting

- Canonical records: **152**
- Palace-managed records: **131**
- Permanent primary loci: **50**
- Embedded palace records: **81**
- Challenge Lab architecture records: **16**
- Scope guards: **5**
- Journey blueprints: **8**
- Bundle blueprints: **19**
- Permanent loci: **50**
- Mixed-discrimination sets: **32**
- Palace exact-name targets: **130**
- Student runtime journeys/scenes/Memory Objects/application tasks: **0 / 0 / 0 / 0**

## Protected upstream state

The Unit 5 F1 upstream-protection manifest continues to verify **216 released Unit 1–4 content files** against the exact Unit 4 F6 baseline package checksum:

```text
e372a71832ca74997fb827b222a8666d9d0c06abbb34a6b9f856c261a14bc9bb
```

The F1 canonical Unit 5 source lock is also byte-protected. F2 changes classification and architecture metadata only.

## Regression result

- Unit 1 full QA: **PASS**
- Unit 2 F5 QA: **PASS**
- Unit 3 F6 QA: **PASS**
- Unit 4 F6 QA: **PASS**
- Units 1–3 mainline QA: **PASS**
- Units 1–4 mainline QA: **PASS**
- Unit 5 F1 QA: **PASS**
- Unit 5 F2 QA: **PASS**
- Python suite: **208 / 208 PASS**
- Unit 3 F6 UI-logic QA: **PASS**
- Unit 4 F6 UI-logic QA: **PASS**
- JavaScript syntax checks: **PASS**
- Deterministic Unit 5 F2 rebuild: **PASS**

## Live API smoke

The live FastAPI check returned HTTP 200 for health, course registry, Unit 5 status, Unit 5 journey registry, Unit 5 application-lab registry, and the existing Unit 4 home route. Unit 5 reports `LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED`, `architecture_loci = 50`, and `student_release = false`. Its student journey list and application-lab runtime remain empty.

## Runtime boundary

Unit 5 has no story files, student Memory Objects, Review queue, mixed-review runtime, or Challenge Lab runtime in F2. The architecture can be inspected through repository artifacts, while the student-facing released units remain Units 1–4.

## Next gate

**F3 — science-bearing scene briefs for all 50 Unit 5 loci.** The F3 briefs should establish physical setting, left/center/right layout, scientific actors/parts, scientific visual requirements, causal action, exact-name introduction, misconception protection, and transition logic. Polished narrative prose remains gated until F3 brief QA passes.
