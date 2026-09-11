# Unit 5 F4F Package QA

## Release boundary

Unit 5 F4F adds polished developer-preview Journey 6 only, **Beyond-Mendel Trait Gallery**. Journeys 1–5 remain protected by their earlier narrative locks. Unit 5 remains student-unreleased and the production runtime remains `v2-apbio-0.22.0-u4-f6`.

## F4F accounting

- Journey 6 scenes: **7 / 7**
- Journey 6 locked records: **24 / 24**
- Journey 6 optional Quick Recalls: **2**
- Journey 6 narrative words: **4,792**
- Average scene length: **684.6 words**
- Shortest scene: **653 words**
- Total Unit 5 developer preview after F4F: **6 journeys / 37 scenes / 13 optional recalls / 102 locked records represented across Journeys 1–6**
- Unit 5 student runtime Memory Objects: **0**
- Unit 5 student Challenge Lab runtime items: **0**

## Narrative and scientific gates

Every Journey 6 scene establishes stable left, center, and right geography before the inheritance mechanism is named. Dr. Imani Reyes, the phenotype-comparison frame, mechanism identity cards, and gold generation ledger remain visible throughout the gallery.

The story preserves these distinctions explicitly.

- A non-simple offspring ratio is separated from the biological mechanism that explains it, and visible numerical difference is not treated as proof of statistical significance.
- Incomplete dominance produces an intermediate heterozygous phenotype while the alleles remain discrete.
- Codominance preserves distinguishable effects of both alleles in the heterozygote.
- Multiple alleles describes population-level allele number while a diploid individual ordinarily carries two copies at the locus.
- The ABO system demonstrates a three-allele population system with IA and IB codominant to one another and each dominant over i in the standard model.
- Epistasis remains interaction in which genotype at one gene affects phenotypic expression associated with another gene.
- Polygenic inheritance retains many-genes-to-one-character geometry.
- Pleiotropy retains one-gene-to-many-effects geometry.
- X-linked and Y-linked inheritance remain tied to the physical chromosome carrying the gene.
- The human XX/XY chromosome-complement model remains an explicit inheritance model and is not used as a definition of gender or a complete account of human sex development.
- Other sex-determination systems remain acknowledged.
- Hemizygosity remains a one-copy condition for a gene or chromosomal region in an otherwise diploid genome.
- X-chromosome inactivation remains a regulatory process in typical mammalian XX somatic cells, with the X described as largely transcriptionally inactive and some genes able to escape inactivation.
- Barr body remains the condensed form of a largely inactive X chromosome visible in some interphase nuclei.
- Environmental effects on phenotype are demonstrated by holding genotype constant while environmental context alters physiology or gene expression.
- Temperature-dependent pigmentation, soil-pH flower color, and UV-regulated melanin production remain examples of environment-dependent phenotype.
- Phenotypic plasticity is not treated as evidence that all phenotypic variation is environmental.
- Both F3 Quick Recall placements and answers remain unchanged.
- Every assigned F3 record retains exact F1 canonical science in the story-beat layer.
- Student-facing Journey 6 prose contains no source-management language, colons, em dashes, `rather than`, `instead of`, or `not only`.

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
- Unit 5 F4F: **PASS**
- Units 1–3 mainline gate: **PASS**
- Units 1–4 mainline gate: **PASS**
- Unit 3 F6 UI logic: **PASS**
- Unit 4 F6 UI logic: **PASS**
- Python tests: **241 / 241 PASS**
- Frontend JavaScript syntax: **PASS**
- Python compilation: **PASS**
- Released Units 1–4 SHA-256 protection: **216 / 216 files unchanged**
- F4F deterministic rebuild: **PASS, 10 generated files checked, 0 changed**

The mainline QA scripts can print a harmless `fatal: not a git repository` message inside the clean archive workspace because `.git` is intentionally excluded. Their content gates still completed with PASS.

## Live API smoke test

A live FastAPI server passed the health, Unit 5 summary, Unit 5 journey registry, Journey 6 retrieval, and Unit 5 Challenge Lab requests.

- Runtime version: `v2-apbio-0.22.0-u4-f6`
- Unit 5 status: `F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW`
- Unit 5 preview journeys: `U5-J1` through `U5-J6`
- Journey 6 scenes: **7**
- Journey 6 checkpoints: **2**
- `U5-J7`: **404**, as required before F4G
- Unit 5 Challenge Lab runtime count: **0**
- Unit 5 `student_release`: **false**
- Unit 5 `preview_release`: **true**

No screenshot-level or pixel-level browser validation is claimed for F4F. Unit 5 remains a developer-preview content/API layer and is not part of the student runtime yet.

## Next gate

F4G may author **Journey 7 only, Chromosome Mapping Rail Yard**. Its locked F3 route contains **6 scenes / 10 records / 2 optional Quick Recalls**. Journeys 1–6 must remain protected, and Journey 8 remains at the F3 scene-brief stage until Journey 7 passes the same prose-level gate.
