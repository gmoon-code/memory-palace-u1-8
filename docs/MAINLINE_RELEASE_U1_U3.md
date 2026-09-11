> **Historical release note:** This document records the Units 1–3 mainline at the moment before Unit 4 F1. Unit 4 has since completed its F1 scientific lock, F2 learning architecture, F3 scene briefs, and F4D Journeys 1–4 developer narrative preview while remaining unreleased. See `UNIT4_F4D_RELEASE.md`.

# Memory Palace V2 Mainline Release · AP Biology Units 1–3

This repository state is the first consolidated V2 mainline release containing three student-ready AP Biology units.

## Student-ready course state

| Unit | Title | Canonical records | Journeys | Permanent scenes | Challenge Lab | Release state |
|---|---|---:|---:|---:|---:|---|
| 1 | Chemistry of Life | 229 | 9 | 78 | 16 | STUDENT_READY |
| 2 | Cells | 142 | 7 | 49 | 9 | STUDENT_READY |
| 3 | Cellular Energetics | 186 | 7 | 54 | 11 | STUDENT_READY · F6 browser validated |
| **Total** |  | **557** | **23** | **181** | **36** |  |

Units 4–8 remain registered as `SOURCE_AVAILABLE_NOT_MIGRATED`. Their presence in the course registry must not make them visible as student-ready content.

## Integration rule

This package is a **full repository root**, not a Unit-3-only patch. It already contains the final Unit 1 and Unit 2 states used by the Unit 3 regression chain. When updating the GitHub repository, copy the contents of this repository root over the existing `memory-palace-v2` root so matching files are replaced together.

Do not upload the historical F4/F5/F6 ZIP files or source PDFs into the repository.

## Current runtime release

The backend reports:

```text
v2-apbio-0.20.0-u3-f6
```

Unit 3 is `student_release = true` and `preview_release = false`.

## Mainline release gate

The integrated release must satisfy all of the following:

- Units 1, 2, and 3 are `STUDENT_READY`.
- Units 4–8 are not student-ready.
- Unit 1 remains scientifically locked and fully accounted.
- Unit 2 F1–F5 locks and finalization pass.
- Unit 3 F1–F6 locks, finalization, and classroom/browser validation pass.
- The full Python test suite passes.
- Frontend JavaScript syntax checks pass.
- No PDF, SQLite, secret `.env`, Python cache, or browser-probe artifact is packaged.

## Next curriculum gate

The next content branch is **Unit 4 · Cell Communication and Cell Cycle**. Begin with scientific source inventory, atomization, current AP scope mapping, conflict/misconception audit, and canonical lock. Do not write Unit 4 palace narratives before that lock passes.
