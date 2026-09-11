# Memory Palace V2 · Unit 6 F2 Package QA

## Package role

This package preserves the released Units 1–5 student runtime and adds Unit 6 F2 development-only learning architecture.

## Verified F2 state

- Unit 6 F1 canonical catalog: **202 / 202 records**
- Palace-managed records: **161 / 161**
- Permanent locus blueprints: **53 / 53**
- Embedded palace records: **108**
- Journey blueprints: **6**
- Bundle blueprints: **21**
- Challenge Lab architecture records: **16 / 16**
- Non-runtime scope guards: **25 / 25**
- Confusable sets: **37**
- Exact-name delayed Review targets: **134**
- Prior-unit reactivations: **5**
- Student runtime journeys/scenes/Memory Objects/Challenge Lab tasks: **0 / 0 / 0 / 0**

## Scientific and upstream protection

- Unit 6 F1 scientific lock QA: **PASS**
- Unit 6 F2 architecture QA: **PASS**
- Units 1–5 upstream protection: **291 / 291 protected files byte-identical**
- Unit 1 full QA: **PASS**
- Unit 2 F5 QA: **PASS**
- Unit 3 F6 QA: **PASS**
- Unit 4 F6 QA: **PASS**
- Unit 5 F6 QA: **PASS**

## Regression

- Python tests: **267 / 267 PASS**
- Python compilation: **PASS**
- JavaScript syntax checks: **PASS**
- Unit 6 live API status: **LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED**
- Unit 6 live student journey count: **0**
- Unit 6 live Challenge Lab count: **0**
- F2 deterministic rebuild: **PASS** for classification, architecture, lock, status, release manifest, and course registry

## Runtime boundary

The public learner runtime remains

```text
v2-apbio-0.24.0-u5-f6
```

F2 makes no student-facing runtime changes.

## Forbidden-file policy

The release ZIP must contain no source PDFs, `.git`, `.env`, SQLite databases, Python caches, pytest caches, or compiled Python files.
