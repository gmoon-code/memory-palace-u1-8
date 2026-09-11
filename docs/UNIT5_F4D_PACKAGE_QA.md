# Unit 5 F4D Package QA

## Release state

Unit 5 F4D adds polished developer-preview Journey 4 only. Journeys 1–3 remain protected by their F4A, F4B, and F4C locks. Unit 5 remains student-unreleased and the production runtime remains `v2-apbio-0.22.0-u4-f6`.

## Journey 4 accounting

- Journey 4: **Mendelian Inheritance Estate**
- Polished scenes: **7 / 7**
- Locked Journey 4 records: **25 / 25**
- Optional first-exposure Quick Recalls: **2**
- Narrative words: **4,267**
- Mean scene length: **609.6 words**
- Shortest scene: **532 words**
- Total Unit 5 developer preview after F4D: **4 journeys / 26 scenes / 9 optional recalls / 71 locked records represented across Journeys 1–4**

## Narrative and scientific checks

F4D requires every scene to establish stable left, center, and right geography before the inheritance model changes. Dr. Imani Reyes, the same pea-line breeding ledger, and the tracked allele case persist across all seven locations.

The gate explicitly verifies that P, F1, and F2 remain tied to the crosses that produce them, allele identity stays separate from notation and dominance, genotype remains separate from phenotype, segregation remains distinct from independent assortment, cross type is chosen before a Punnett grid, gametes are generated before the Punnett model, and classic ratios remain conditional on their stated crosses and inheritance assumptions.

The Punnett square is treated as a probability model of possible gamete combinations. It does not replace meiosis, segregation, assortment, fertilization, or genotype-to-phenotype biology.

Student-facing narrative prose is scanned for source-management language and em dashes. Colon punctuation is prohibited except where it is scientifically necessary inside the canonical ratio notation `3:1` and `9:3:3:1`.

## Regression

- Unit 1 full/content QA: **PASS**
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
- Units 1–3 mainline gate: **PASS**
- Units 1–4 mainline gate: **PASS**
- Unit 3 F6 UI-logic QA: **PASS**
- Unit 4 F6 UI-logic QA: **PASS**
- Python tests: **231 / 231 PASS**
- F4D deterministic rebuild: **PASS, 10 generated files checked, 0 changed**
- Live FastAPI Unit 5 preview: **PASS**
- Units 1–4 protected content files: **216 / 216 unchanged**

## Live API state

The live preview check reports four Unit 5 developer-preview journeys, `U5-J1`, `U5-J2`, `U5-J3`, and `U5-J4`. Journey 4 returns seven scenes and two checkpoints. The Unit 5 Challenge Lab remains empty because its runtime is not created at F4D.

## Packaging boundary

The clean release archive excludes source PDFs, `.git`, `.env`, SQLite databases, Python bytecode, Python cache directories, and pytest caches.

No screenshot-level browser validation is claimed for F4D. The new Unit 5 material remains a developer-preview content/API layer and is not part of the student runtime yet.
