# AP Biology V2 Source of Truth

Memory Palace V2 keeps scientific authority separate from student narrative and software presentation.

## Unit 1

Unit 1 uses the audited F6.9 corpus as its protected scientific source.

Authoritative preserved files:

- `content/ap-biology/unit-1/source/canonical-unit1.json`
- `content/ap-biology/unit-1/source/guided-journeys.json`
- `content/ap-biology/unit-1/source/coverage-manifest.json`
- `content/ap-biology/unit-1/migration/f6_9-runtime-snapshot.json`

`content/ap-biology/unit-1/content-lock.json` stores SHA-256 hashes and expected counts. Derived V2 projections may reorganize locked content for software use but may not silently change canonical science or AP scope.

## Unit 2

Unit 2 has completed the F1 source/scientific lock but has **not** entered student narrative release.

Authoritative F1 files:

- `content/ap-biology/unit-2/source/canonical-unit2-f1.json`
- `content/ap-biology/unit-2/source/coverage-manifest-f1.json`
- `content/ap-biology/unit-2/audit/F1_SOURCE_AUDIT.md`
- `content/ap-biology/unit-2/audit/F1_REVIEW_FLAGS.md`

`content/ap-biology/unit-2/content-lock-f1.json` protects the canonical F1 JSON artifacts with SHA-256 hashes. Records requiring a scientific correction or scope qualification preserve that provenance through `LOCKED_WITH_CORRECTION_OR_SCOPE_NOTE` plus a review-flag reference.

No Unit 2 journey, scene, Memory Object, or application-lab file may be treated as released until the downstream classification, palace architecture, narrative, and release QA gates pass.

## Authority policy

1. The current AP Biology Course and Exam Description controls AP-required scope and current topic mapping.
2. Teacher PPTs and packets define actual classroom exposure and teacher-required enrichment.
3. Campbell Biology 13th edition verifies mechanisms, terminology, and scientific corrections.
4. Mnemonic/narrative wording is a downstream presentation layer and cannot rewrite locked science.
