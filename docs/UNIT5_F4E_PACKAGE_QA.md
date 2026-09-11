# Unit 5 F4E Package QA

## Release boundary

Unit 5 F4E adds polished developer-preview Journey 5 only, **Probability and Pedigree Court**. Journeys 1–4 remain protected by their F4A, F4B, F4C, and F4D locks. Unit 5 remains student-unreleased and the production runtime remains `v2-apbio-0.22.0-u4-f6`.

## F4E accounting

- Journey 5 scenes: **4 / 4**
- Journey 5 locked records: **7 / 7**
- Journey 5 optional Quick Recalls: **2**
- Journey 5 narrative words: **2,713**
- Average scene length: **678.2 words**
- Shortest scene: **640 words**
- Total Unit 5 developer preview after F4E: **5 journeys / 30 scenes / 11 optional recalls / 78 locked records represented across Journeys 1–5**
- Unit 5 student runtime Memory Objects: **0**
- Unit 5 student Challenge Lab runtime items: **0**

## Narrative and scientific gates

Every Journey 5 scene establishes stable left, center, and right geography before probability or pedigree interpretation changes. Dr. Imani Reyes, the two-sided evidence docket, event-probability cards, and candidate inheritance-model cards remain visible throughout the court.

The story preserves these distinctions explicitly.

- Probability models repeated random inheritance events and does not guarantee the exact composition of one small family.
- The addition rule is used for mutually exclusive OR events.
- The multiplication rule is used for independent AND events under the stated model.
- Event language is identified before arithmetic.
- Pedigree notation is decoded before inheritance-pattern inference.
- Observed family relationships and phenotypes remain distinct from inferred genotype and inheritance mechanism.
- Autosomal-dominant pedigree clues remain heuristic, with explicit caveats for new variants, penetrance, family size, and uncertain phenotype classification.
- Male-biased occurrence is not treated as a universal indicator of every X-linked trait.
- Candidate inheritance models generate predictions that are compared with the same observed evidence before support is assigned.
- Punnett and probability tools are used only after the candidate model and assumptions are specified.
- Both F3 Quick Recall placements and answers remain unchanged.
- Every assigned F3 record retains exact F1 canonical science in the story-beat layer.
- Student-facing Journey 5 prose contains no source-management language, colons, em dashes, `rather than`, `instead of`, or `not only`.

## Regression

The final release checks passed.

- Unit 1 full scientific/runtime QA: **PASS**
- Unit 2 F5: **PASS**
- Unit 3 F6: **PASS**
- Unit 4 F6: **PASS**
- Unit 5 F1: **PASS**
- Unit 5 F2: **PASS**
- Unit 5 F3: **PASS**
- Unit 5 F4A: **PASS**
- Unit 5 F4B: **PASS**
- Unit 5 F4C: **PASS**
- Unit 5 F4D: **PASS**
- Unit 5 F4E: **PASS**
- Units 1–3 mainline gate: **PASS**
- Units 1–4 mainline gate: **PASS**
- Unit 3 F6 UI logic: **PASS**
- Unit 4 F6 UI logic: **PASS**
- Python tests: **236 / 236 PASS**
- Frontend JavaScript syntax: **PASS**
- Python compilation: **PASS**
- Released Units 1–4 SHA-256 protection: **216 / 216 files unchanged**
- F4E deterministic rebuild: **PASS, 9 generated files checked, 0 changed**

The mainline QA scripts print a harmless `fatal: not a git repository` message when run inside this clean archive workspace because `.git` is intentionally excluded. Both gates still complete with PASS after their content checks.

## Live API smoke test

The live FastAPI server passed `/api/health`, `/`, Unit 5 summary, Unit 5 journey registry, Journey 5 retrieval, and Unit 5 Challenge Lab requests.

- Runtime version: `v2-apbio-0.22.0-u4-f6`
- Unit 5 status: `F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW`
- Unit 5 preview journeys: `U5-J1` through `U5-J5`
- Journey 5 scenes: **4**
- Journey 5 checkpoints: **2**
- `U5-J6`: **404**, as required before F4F
- Unit 5 Challenge Lab runtime count: **0**
- Unit 5 `student_release`: **false**
- Unit 5 `preview_release`: **true**

No screenshot-level or pixel-level browser validation is claimed for F4E. Unit 5 remains a developer-preview content/API layer and is not part of the student runtime yet.

## Next gate

F4F may author **Journey 6 only, Beyond-Mendel Trait Gallery**. Journeys 1–5 must remain protected, and Journeys 7–8 remain at the F3 scene-brief stage until Journey 6 passes the same prose-level gate.
