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
3. Teacher-provided PowerPoints establish the intended student understanding depth, examples, emphases, classroom terminology, and expected reasoning. Their U1 through U15 labels do not establish course sequence.
4. Zumdahl, Zumdahl, and DeCoste, Chemistry, 11th edition, provides the chemistry-accuracy and explanatory reference within CED scope.
5. Teacher-provided lab materials, when supplied, establish the intended experimental contexts and inquiry sequence.
6. Teacher-supplied scoring guides inform assessment reasoning, representation, calculation, experimental-analysis, and explanation demands. Their source questions and scoring language are not copied verbatim into Story Method content.

No source conflict is silently resolved. Conflicts are recorded and brought forward into the crosswalk.

## F0A intake state

F0A Source Inventory is complete. The received source set contains the Fall 2024 AP Chemistry CED, Zumdahl Chemistry 11e, fifteen teacher PowerPoint decks, and ten scoring-guide PDFs covering CED Units 1 through 9.

The source inventory is `docs/ap-chemistry/AP_CHEMISTRY_F0A_SOURCE_INVENTORY.json`, with a human-readable audit at `docs/ap-chemistry/AP_CHEMISTRY_F0A_SOURCE_INVENTORY.md`.

A separate teacher laboratory collection remains pending. A separate pacing guide is no longer required because the user explicitly directed the final course to follow CED organization and order.

Additional sources may still be added before F0D. Each new source must be inventoried before it influences the crosswalk.

## F0B crosswalk state

F0B Framework Crosswalk is complete. All 91 CED topics are represented in exact CED Unit 1 through Unit 9 order, with CED suggested science-practice skills, teacher-PPT depth sources, Zumdahl 11e chemistry references, and unit-aligned scoring-guide evidence recorded.

Eighty-four topics have complete teacher-depth/source mappings. Six topics retain partial teacher-PPT coverage and one topic has no direct teacher-PPT source. The seven topics carried forward as explicit source gaps are 1.4, 2.2, 7.8, 8.10, 8.11, 9.6, and 9.7. These gaps are not silently filled from textbook depth or general model knowledge.

The College Board AP Chemistry Clarifications and Corrections document implemented as of June 2026 was checked during F0B. Its listed changes concern front matter, resource locations, and Progress Check language. It does not list topic-level content, unit-order, or science-practice changes that alter the crosswalk.

The machine-readable crosswalk is `docs/ap-chemistry/AP_CHEMISTRY_F0B_FRAMEWORK_CROSSWALK.json`, with a human-readable audit at `docs/ap-chemistry/AP_CHEMISTRY_F0B_FRAMEWORK_CROSSWALK.md`.

A separate teacher laboratory collection remains pending and is carried into F0C/F0D as an unresolved source state.

## F0C science-component state

F0C Science Component Coverage Plan is complete. Each of the 91 CED topics now has a source-bounded classification for concepts, Memory Objects, equations, calculations, graphs, diagrams, data tables, particulate models, laboratory contexts, and vectors.

The plan preserves the seven F0B source-gap topics and adds explicit scope guards where the CED or teacher materials set a boundary. Topic 8.11 remains qualitative with solubility-as-a-function-of-pH calculations excluded. Topic 9.10 does not require Nernst-equation calculations. Topic 7.8 retains the CED-required particulate-model treatment despite partial teacher-PPT coverage. Topic 9.7 retains its direct teacher-PPT depth gap.

The CED laboratory requirement is recorded as a course-level constraint. A separate teacher laboratory collection is still pending, so F0C does not claim topic-specific lab assignments or invent teacher procedures. This unresolved lab source remains an F0D readiness blocker.

The machine-readable plan is `docs/ap-chemistry/AP_CHEMISTRY_F0C_SCIENCE_COMPONENT_PLAN.json`, with a human-readable audit at `docs/ap-chemistry/AP_CHEMISTRY_F0C_SCIENCE_COMPONENT_PLAN.md`.

## F0D readiness state

F0D Readiness Gate has been executed and is **blocked pending the teacher laboratory source basis**.

The academic structure is otherwise ready for production planning. The nine CED units and all 91 topic boundaries are locked, the seven F0B source gaps have bounded production dispositions, and the F0C component plan is complete. Topic 9.7 retains a visible teacher-depth warning because no direct teacher-PPT treatment was located.

The gate does not authorize the real AP Chemistry package, scientific records, Memory Objects, narratives, questions, review records, Challenge Lab content, teacher editing, or student visibility. The source register therefore remains at `F0C_COMPLETE`.

The blocker can be cleared by inventorying the teacher's AP Chemistry lab procedures/manual/sequence, or by an explicit user directive to use the CED/public College Board laboratory guidance as the lab-source basis followed by inventory of that basis.

The machine-readable gate is `docs/ap-chemistry/AP_CHEMISTRY_F0D_READINESS_GATE.json`, with a human-readable report at `docs/ap-chemistry/AP_CHEMISTRY_F0D_READINESS_GATE.md`.

## Fixture discrepancies already identified

The architecture fixture currently contains only Units 1 and 2. Its Unit 2 title is `Molecular and Ionic Compound Structure and Properties`. The current official framework title is `Compound Structure and Properties`.

F0 records that discrepancy without changing the fixture. Units 3 through 9 are also absent by design. No fixture file is promoted into the real curriculum during source intake.

## F0 deliverables

F0 will close through four linked artifacts.

- F0A Source Inventory records each supplied source, its role, coverage, version or edition, ingestion status, file size, page count, and SHA-256 fingerprint. F0A is complete.
- F0B Framework Crosswalk maps every College Board topic and suggested science-practice skill to the teacher materials, textbook, assessment evidence, and pending lab-source state. F0B is complete with seven explicitly recorded teacher-depth gaps.
- F0C Science Component Coverage Plan identifies where equations, calculations, graphs, diagrams, data tables, particulate models, and lab contexts are required or supporting. F0C is complete with the teacher-lab mapping still pending.
- F0D Readiness Gate verifies source coverage, records unresolved blockers, locks unit titles and topic boundaries, and authorizes construction only when every hard blocker is cleared. The current F0D run is blocked pending the laboratory source basis.

Narrative writing begins only after a later F0D run reaches `COMPLETE`.

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
