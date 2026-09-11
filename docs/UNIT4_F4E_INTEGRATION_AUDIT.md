# Unit 4 F4E Mainline Integration Audit

## Release boundary

Unit 4 remains an unreleased developer preview. F4E adds only Journey 5, **Cell-Cycle Preparation Archive**, while Journeys 1–4 remain protected byte-for-byte by the F4D predecessor lock. Units 1–3 remain the only student-ready course units.

## Unit 4 F4E accounting

- Canonical scientific records protected: **180**
- F2 architecture: **7 journeys / 51 loci**
- F3 scene briefs: **51 / 51**
- Polished preview journeys: **5 / 7**
- Polished preview scenes: **33 / 51**
- Journey 5 records: **27 / 27**
- Journey 5 optional Quick Recalls: **3**
- Journey 5 narrative words: **3,967**
- Journey 5 mean scene length: **495.9 words**
- Journey 5 shortest scene: **435 words**
- Unit 4 student release: **false**
- Unit 4 preview release: **true**

## Narrative continuity

Journey 5 carries one transparent tracked chromosome archive case through Genome Packing Archive → Chromosome Anatomy Workbench → Chromosome Sets Gallery → Cell-Cycle Clock → G1 Growth Gate → S-Phase Replication Room → G2 Preparation Bay → G0 Side Chamber. Artificial tracing colors follow identity only; they are explicitly not biological chromosome colors.

The narrative preserves the distinctions that make later mitosis reasoning possible. Histone, nucleosome, chromatin, and chromosome remain different structural levels. A replicated chromosome contains sister chromatids joined before separation. Centromere remains a chromosome region while kinetochore remains a protein complex assembled there. Homologous chromosomes remain distinct from sister chromatids. Somatic/gamete describe cell roles while diploid/haploid describe chromosome-set number. Interphase remains active G1, S, and G2. S phase doubles DNA content and chromatid number without doubling chromosome number counted by centromeres before sister-chromatid separation. G2 prepares a replicated cell for mitosis without replicating DNA again. G0 remains a nondividing state with variable reversibility.

## Regression

The historical build sequence through Units 1–3 completed successfully in this F4E work session, followed by the complete Unit 4 F1 → F4E sequence. The integrated Python suite passed **180 / 180** tests. Unit 3 F6 UI logic passed. Python compilation and frontend JavaScript syntax passed. A temporary Git QA baseline was then used to rebuild Unit 4 F1 → F4E; the rebuild returned **zero Git diff**, confirming deterministic output for the current Unit 4 stage.

## Live preview

A live FastAPI smoke test returned HTTP 200 for Unit 4 metadata, the five-journey registry, each Journey 1–5 endpoint, and `/?unit=unit-4`.

The developer API exposes exactly five Unit 4 journeys in the current preview registry.

- `/api/units/unit-4/journeys/U4-J1`
- `/api/units/unit-4/journeys/U4-J2`
- `/api/units/unit-4/journeys/U4-J3`
- `/api/units/unit-4/journeys/U4-J4`
- `/api/units/unit-4/journeys/U4-J5`

The student release flag remains false.

## Next gate

F4F may author **Journey 6, Mitosis Transit Hall** only. Journeys 1–5 must remain unchanged.
