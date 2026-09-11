# Unit 4 F1 QA

## Release gate

**PASS — SCIENCE_LOCKED_F1_NOT_STUDENT_RELEASED**

Unit 4 now has a complete teacher-deck inventory, current-CED atomization, assessment-domain crosswalk, conflict/misconception audit, and locked canonical scientific catalog. No Unit 4 palace, scene, Memory Object, Review manifest, or Challenge Lab runtime has been released.

## Accounting

- Teacher PPT slides ingested: **85 / 85**
- Current CED topics: **6 / 6**
- Current CED atoms: **38**
- Canonical records: **180**
- AP_REQUIRED records: **38**
- PRACTICE_ONLY records: **15**
- SCOPE_GUARD records: **3**
- TEACHER_REQUIRED_ENRICHMENT records: **124**
- Review flags: **39 / 39 resolved**
- Canonical records with correction/scope provenance: **54**
- Assessment semantic crosswalks: **9**
- Blocking missing resources: **0**
- Unmapped teacher PPT slides: **0**
- Student journeys: **0**
- Student scenes: **0**
- Unit 4 Memory Objects: **0**
- Unit 4 Challenge Lab items: **0**

## Scientific review gate

All identified source conflicts are resolved in canonical statements while raw teacher wording remains preserved. Particular attention was given to receptor taxonomy, ligand versus transduced information, phosphorylation/dephosphorylation, G-protein switching, homeostatic set-point wording, chromosome/chromatid language, mitosis versus cytokinesis, G0 and checkpoint claims, cyclin/CDK AP exclusions, and cancer biology.

## Assessment crosswalk gate

The available 85-page Unit 4 scoring guide was used as semantic assessment evidence. Representative items cover all six current CED topics and require pathway reasoning, data interpretation, cell-cycle calculations, checkpoint disruption prediction, and cancer-treatment reasoning.

## Next gate

**F2 — learning-function classification and palace architecture.** The locked catalog must next be classified by learning destination before any Unit 4 narrative prose is authored.

## Integrated mainline regression

The Unit 4 F1 branch was tested against the complete Units 1–3 build chain. The existing student-ready release remained unchanged at **557 canonical records, 23 guided journeys, 181 permanent scenes, and 36 Challenge Lab items**.

Final regression results

- Unit 1 full build and scientific lock — **PASS**
- Unit 2 F1–F5 build chain — **PASS**
- Unit 3 F1–F6 build chain — **PASS**
- Unit 4 F1 scientific lock — **PASS**
- Mainline Units 1–3 release gate — **PASS**
- Unit 3 F6 UI logic — **PASS**
- Automated Python tests — **146 / 146 PASS**
- Frontend JavaScript syntax — **PASS**
- Deterministic repository diff after the full workflow — **PASS**
- Live API smoke test — **PASS**

Unit 4 API metadata is available for development and audit, but its journey registry remains empty and its application lab contains zero items. The student release flag remains `false`.

## Audit workbook

`content/ap-biology/unit-4/audit/APBIO_Unit4_F1_Source_Lock.xlsx` provides six reviewable sheets covering the release summary, all 180 canonical records, all 38 CED atoms, all 85 teacher-PPT slides, all 39 resolved review flags, and the nine representative assessment semantic crosswalks.
