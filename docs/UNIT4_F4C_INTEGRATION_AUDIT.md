# Unit 4 F4C Mainline Integration Audit

## Release state

Unit 4 remains an unreleased developer preview. F4C adds only Journey 3, **Signal Relay Tower**, while Journeys 1 and 2 remain protected by their earlier content locks.

- Canonical Unit 4 records protected: **180**
- F2 architecture journeys: **7**
- F2 permanent loci: **51**
- F3 scene briefs: **51**
- Polished preview journeys: **3 / 7**
- Polished preview scenes: **19 / 51**
- Journey 3 locked records represented: **25 / 25**
- Journey 3 optional first-exposure recalls: **3**
- Journey 3 narrative words: **3,406**
- Journey 3 mean scene length: **486.6 words**
- Journey 3 shortest scene: **441 words**
- Unit 4 student release: **false**
- Unit 4 preview release: **true**

## Historical regression

The repository was rebuilt through the complete existing pipeline before packaging.

- Unit 1 historical build and content locks: **PASS**
- Unit 2 F1–F5: **PASS**
- Unit 3 F1–F6: **PASS**
- Unit 4 F1–F4C: **PASS**
- Units 1–3 mainline integration gate: **PASS**
- Unit 3 F6 UI logic QA: **PASS**
- Automated Python tests: **170 / 170 PASS**
- Python compilation: **PASS**
- Frontend JavaScript syntax: **PASS**
- F4B → F4C deterministic rebuild: **PASS, zero Git diff**

## Live preview smoke test

A local FastAPI server was started and the following returned HTTP 200.

- `/api/health`
- `/api/units/unit-4`
- `/api/units/unit-4/journeys`
- `/api/units/unit-4/journeys/U4-J1`
- `/api/units/unit-4/journeys/U4-J2`
- `/api/units/unit-4/journeys/U4-J3`
- `/?unit=unit-4`

The Unit 4 summary reported `F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW`, `student_release: false`, and `preview_release: true`. The journey registry exposed exactly U4-J1, U4-J2, and U4-J3.

## F4C narrative safeguards

Journey 3 keeps the extracellular ligand at the receptor. A violet line is used only as a non-molecular visualization of information flow and advances only after a real pathway component changes state. The story keeps phosphorylation chemistry separate from universal activation/inactivation claims, distinguishes second messenger from ligand, represents amplification as multiplication of downstream events, separates transduction from cellular response, locates receptor versus downstream mutation breakpoints, preserves target-dependent phosphatase reasoning, and distinguishes genetic alteration from reversible chemical pathway perturbation.

## Next gate

F4D may author **Journey 4, Feedback Regulation Center** only. Journeys 1–3 remain locked unchanged until their predecessor hashes pass.
