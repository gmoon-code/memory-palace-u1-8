# AP Chemistry F0 source intake

## Phase purpose

F0 establishes the source basis for the real AP Chemistry course before any fixture replacement, scientific-record production, narrative writing, question generation, review construction, Challenge Lab expansion, or student publication work begins.

The existing AP Chemistry files remain an architecture fixture during this phase. They are useful for proving course isolation and interface behavior. They are not an academic source for the future course.

## Current official framework

The current College Board AP Chemistry Course and Exam Description is the version effective Fall 2024. College Board's current course-change guidance identifies that framework as the Course and Exam Description to use for the 2026–27 school year and lists no announced AP Chemistry framework change after the Fall 2024 update.

The framework contains nine commonly taught units.

| Unit | Official title | Multiple-choice weighting |
| --- | --- | --- |
| 1 | Atomic Structure and Properties | 7%–9% |
| 2 | Compound Structure and Properties | 7%–9% |
| 3 | Properties of Substances and Mixtures | 18%–22% |
| 4 | Chemical Reactions | 7%–9% |
| 5 | Kinetics | 7%–9% |
| 6 | Thermochemistry | 7%–9% |
| 7 | Equilibrium | 7%–9% |
| 8 | Acids and Bases | 11%–15% |
| 9 | Thermodynamics and Electrochemistry | 7%–9% |

The machine-readable source record is `docs/ap-chemistry/AP_CHEMISTRY_SOURCE_REGISTER.json`.

## Source authority

F0 uses the following source hierarchy for different purposes.

1. The College Board Course and Exam Description defines AP Chemistry framework scope, required content, science practices, and unit/topic expectations.
2. College Board clarifications and corrections modify or clarify the framework when applicable.
3. Teacher-provided PowerPoints, guided notes, pacing documents, and handouts establish the intended classroom sequence, examples, emphases, and terminology.
4. The selected textbook provides explanatory depth, worked examples, and reference support.
5. Teacher-provided lab materials establish the intended experimental contexts and inquiry sequence.
6. Public released College Board free-response materials may inform later assessment-format and reasoning coverage. Secure AP Classroom content is outside the repository source-ingestion workflow unless the user explicitly supplies material they are permitted to use.

No source conflict is silently resolved. Conflicts are recorded and brought forward into the crosswalk.

## Materials still required

The following source groups are pending before F0 can close.

- Unit 1–9 AP Chemistry PowerPoints, guided notes, or equivalent teacher-created course materials
- the primary textbook or textbook chapters used for the course
- laboratory procedures, inquiry sequence, or lab manual materials
- public or teacher-authored review and assessment resources that should inform retrieval and application design
- a pacing guide or preferred sequence when the classroom sequence differs from the College Board suggested order

A source can be absent if the user does not use it. The source register will record that absence explicitly.

## Fixture discrepancies already identified

The architecture fixture currently contains only Units 1 and 2. Its Unit 2 title is `Molecular and Ionic Compound Structure and Properties`. The current official framework title is `Compound Structure and Properties`.

F0 records that discrepancy without changing the fixture. Units 3 through 9 are also absent by design. No fixture file is promoted into the real curriculum during source intake.

## F0 deliverables

F0 will close through four linked artifacts.

- F0A Source Inventory records each supplied source, its role, coverage, version or edition, and ingestion status.
- F0B Framework Crosswalk maps every College Board topic and science-practice expectation to the teacher materials, textbook, labs, and later Story Method content components.
- F0C Science Component Coverage Plan identifies where equations, calculations, graphs, diagrams, data tables, particulate models, and lab contexts are required.
- F0D Readiness Gate verifies complete source coverage, records unresolved conflicts, locks unit titles and topic boundaries, and authorizes construction of the real AP Chemistry package.

Narrative writing begins after F0D.

## F0 safety lock

During F0

- `content/ap-chemistry/` remains byte-for-byte at the frozen architecture fixture state.
- `platform/course-packages/ap-chemistry.json` remains unchanged.
- AP Chemistry remains `status=development`.
- AP Chemistry remains hidden from students.
- AP Chemistry remains read-only in Content Studio.
- AP Biology content remains unchanged.
- production `main` remains untouched.

The freeze reference `freeze/multi-course-foundation-2026-09-19` remains the rollback boundary.
