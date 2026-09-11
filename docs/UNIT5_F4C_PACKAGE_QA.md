# Unit 5 F4C Package QA

## Result

**PASS**

Unit 5 F4C packages Journey 3 · Diversity and Chromosome Error Center as a developer preview while preserving Journeys 1–2 and the released Units 1–4 baseline.

## F4C narrative accounting

- Journey 3 scenes: **4 / 4**
- Journey 3 locked knowledge records: **8 / 8**
- Optional first-exposure Quick Recalls: **2**
- Journey 3 narrative words: **2,603**
- Mean scene length: **650.8 words**
- Shortest scene: **601 words**
- Total Unit 5 preview journeys: **3**
- Total Unit 5 preview scenes: **19**
- Total Unit 5 preview Quick Recalls: **7**
- Unit 5 student release: **false**

## Narrative-quality gates

- Every Journey 3 scene establishes left / center / right geography before new scientific action.
- Dr. Imani Reyes remains the recurring guide.
- The chromosome-outcome scanner persists through all four scenes and visibly changes from diversity mode to segregation-integrity mode.
- The gold generation ledger keeps allele-combination diversity, segregation event, and chromosome-count outcome in separate causal columns.
- Crossing over, independent orientation/assortment, and random fertilization remain three distinct normal sources of genetic diversity.
- Recombinant chromosome structure is distinguished from chromosome-number abnormality.
- Nondisjunction is the segregation failure; aneuploidy is the abnormal chromosome-number outcome.
- Aneuploidy is distinguished from whole-set ploidy change.
- Karyotype evidence shows the resulting chromosome complement and does not claim to directly display the earlier nondisjunction event.
- Trisomy 21 remains one specific aneuploid example involving three copies of chromosome 21.
- Trisomy 21 does not replace the broader definitions of nondisjunction or aneuploidy.
- Student-facing Journey 3 prose contains no source-management language, colon punctuation, or em dashes.

## Scientific and predecessor locks

- Unit 5 F1 scientific lock: **PASS**
- Unit 5 F2 learning-architecture lock: **PASS**
- Unit 5 F3 scene-brief lock: **PASS**
- Unit 5 F4A Journey 1 lock: **PASS**
- Unit 5 F4B Journey 2 lock: **PASS**
- Unit 5 F4C Journey 3 lock: **PASS**
- Units 1–4 protected content files: **216 / 216 unchanged**

## Historical regression

- Unit 1 full QA: **PASS**
- Unit 2 F5: **PASS**
- Unit 3 F6: **PASS**
- Unit 4 F6: **PASS**
- Units 1–3 mainline gate: **PASS**
- Units 1–4 mainline gate: **PASS**
- Unit 3 F6 UI-logic QA: **PASS**
- Unit 4 F6 UI-logic QA: **PASS**
- Python test suite: **226 / 226 PASS**
- Python compilation: **PASS**
- JavaScript syntax checks: **PASS**

## Determinism and live API

The F4C build was run again after the release artifacts were created. Eleven generated Unit 5 F4A–F4C/course artifacts were SHA-256 compared before and after the rebuild. **0 files changed**.

Live FastAPI smoke testing returned HTTP 200 for health, Unit 5 summary, Unit 5 journey registry, Journey 3, the Unit 5 application-lab boundary, and the root application page.

The live Unit 5 preview registry contains exactly:

- `U5-J1`
- `U5-J2`
- `U5-J3`

Unit 5 remains `student_release = false`, `preview_release = true`, and its Challenge Lab runtime remains empty at this stage.

## Runtime boundary

The production student runtime remains:

```text
v2-apbio-0.22.0-u4-f6
```

F4C does not create Unit 5 student Memory Objects, Review runtime, Challenge Lab runtime, or finalization artifacts.

## Next gate

The next curriculum gate is **Unit 5 F4D · Journey 4 only · Mendelian Inheritance Estate**. Journeys 5–8 remain at the locked F3 scene-brief stage until Journey 4 passes the same narrative standard.
