# Unit 6 F4F Integration Audit

## Result

**PASS**

## Upstream protection

The Units 1–5 protection manifest still contains **291 protected files** derived from the finished Unit 5 F6 baseline. All protected files remain byte-identical.

The public Units 1–5 runtime therefore remains unchanged during F4F narrative work.

## Unit 6 lock chain

The following locks remain present and authoritative.

- `content-lock-f1.json` · scientific lock
- `content-lock-f2.json` · learning architecture lock
- `content-lock-f3.json` · science-bearing scene-brief lock
- `content-lock-f4a.json` · Journey 1 narrative lock
- `content-lock-f4b.json` · Journeys 1–2 narrative lock
- `content-lock-f4c.json` · Journeys 1–3 narrative lock
- `content-lock-f4d.json` · Journeys 1–4 narrative lock
- `content-lock-f4e.json` · Journeys 1–5 narrative lock
- `content-lock-f4f.json` · all six narrative journeys locked

F4F does not alter the F1 catalog, F2 destination classification, F2 left/center/right locus geometry, or F3 scene briefs.

## Complete narrative coverage

All six journeys now exist as polished developer-preview curriculum files.

- journeys: **6 / 6**
- permanent scenes: **53 / 53**
- palace-managed knowledge records: **161 / 161**
- duplicate palace-managed assignments: **0**
- missing palace-managed assignments: **0**
- optional first-exposure recalls: **18**
- delayed exact-name targets represented by narrative content: **134**

No final F5 runtime artifacts exist yet.

```text
memory-objects-f5.json          absent
application-lab.json            absent
review-manifest-f5.json         absent
mixed-discrimination-f5.json    absent
scope-guards-f5.json            absent
finalization-f5.json            absent
```

## Journey 6 scientific integration

Journey 6 carries one coded sample tube, U6-X, through the analytical route and introduces a separate engineered plasmid only for recombinant bacterial transformation/expression.

The narrative explicitly keeps these distinctions visible.

- gel electrophoresis versus PCR
- gel electrophoresis versus DNA sequencing
- PCR denaturation versus primer annealing versus extension
- laboratory bacterial transformation versus natural horizontal-gene-transfer transformation
- DNA uptake versus recombinant gene expression
- nucleotide sequence data versus DNA profile/fingerprint comparison evidence

The exact F1 canonical scientific statements remain attached to all 11 Journey 6 story beats.

## Public runtime boundary

Live FastAPI checks returned HTTP 200 for

- `/api/health`
- `/api/course`
- `/api/units/unit-6`
- `/api/units/unit-6/journeys`
- `/api/units/unit-6/application-lab`
- `/`

Unit 6 reports

```text
F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW
student_release = false
preview_release = true
```

The public Unit 6 journey list remains empty, the public Challenge Lab remains empty, and a direct public request for Journey 6 returns 404.

## Determinism

`build_unit6_f4f.py` was rerun against its generated outputs.

```text
checked artifacts  8
changed artifacts  0
```

## Regression

- Python tests: **301 / 301 PASS**
- Unit 3 F6 UI logic: **PASS**
- Unit 4 F6 UI logic: **PASS**
- Unit 5 F6 UI logic: **PASS**
- JavaScript syntax: **PASS**
- Python compilation: **PASS**
- Unit 6 F1–F4F QA: **PASS**
- Units 1–5 release QA: **PASS**

F4F is therefore safe to use as the baseline for Unit 6 F5 finalization.
