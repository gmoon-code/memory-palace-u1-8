# Unit 3 F1 QA

## Release gate

**PASS — SCIENCE_LOCKED_F1_NOT_STUDENT_RELEASED**

Unit 3 has a complete source inventory, current-CED atomization, teacher-source coverage ledger, assessment crosswalk, conflict/misconception audit, and locked canonical scientific catalog. No Unit 3 narrative, scene, palace, Memory Object, or application runtime has been released.

## Accounting

- Teacher PPT slides ingested: **136 / 136**
- Teacher assessment items crosswalked: **24 / 24**
- Current CED topics: **5 / 5**
- Current CED atoms: **54**
- Canonical records: **186**
- AP-required records: **54**
- Teacher-required enrichment records: **117**
- Scope-guard records: **4**
- Practice-only records: **11**
- Review flags: **30 / 30 resolved**
- Canonical records with correction/scope provenance: **68**
- Blocking missing resources: **0**
- Unmapped teacher PPT slides: **0**
- Student journeys: **0**
- Student scenes: **0**
- Unit 3 Memory Objects: **0**
- Unit 3 Challenge Lab items: **0**

## Current CED structure

F1 maps the legacy teacher material into the current Effective Fall 2025 structure:

1. 3.1 Enzymes
2. 3.2 Environmental Impacts on Enzyme Function
3. 3.3 Cellular Energy
4. 3.4 Photosynthesis
5. 3.5 Cellular Respiration

The teacher deck's older topic headings remain preserved as source metadata only.

## Scientific review gate

All identified source conflicts were resolved before canonical locking. High-priority corrections include ATP-hydrolysis energy wording, allosteric-regulation wording, separation of water oxidation from Calvin-cycle reduction chemistry, excitation-energy transfer in photosystems, Calvin cycle versus cyclic electron flow, early-atmosphere/photorespiration wording, animal respiratory-fuel wording, and the outdated lactate-causes-burning model.

Current-CED exclusion statements were also preserved as scope guards. Detailed Gibbs free-energy equations, named photosynthetic electron carriers, memorization of detailed Calvin-cycle steps, and detailed respiration bookkeeping remain enrichment or scope-guard content and are not promoted to AP-required status.

## Assessment crosswalk gate

All 24 teacher-test items have an explicit crosswalk. Three are blocked from direct reuse until revised:

- **Question 2** — covalent penicillin/transpeptidase inhibition does not cleanly represent the current CED's reversible competitive-inhibition model.
- **Question 16** — the claim that starch is the major source of fuel for animals is not a defensible universal biology statement.
- **Question 23** — the prompt inherits the outdated model that lactate causes the exercise burning sensation.

Question 4 was specifically audited after the first build and is now explicitly mapped to the locked catabolic-pathway record `U3-K-057`.

## Repository regression gate

The exact historical build/QA chain used by GitHub Actions was executed in order through Unit 3 F1.

- Unit 1 content lock: **PASS**
- Unit 1 narrative QA: **PASS**
- Unit 2 F1 scientific lock: **PASS**
- Unit 2 F2 architecture: **PASS**
- Unit 2 F3 scene briefs: **PASS**
- Unit 2 F4A–F4G narratives: **PASS**
- Unit 2 F5 finalization: **PASS**
- Unit 3 F1 scientific lock: **PASS**
- Automated tests: **86 / 86 passed**
- JavaScript syntax checks: **PASS**
- Python compilation: **PASS**

## Live API smoke gate

The running FastAPI app returned:

- `/api/health` → `v2-apbio-0.9.0-u3-f1`
- `/api/units/unit-3` → 186 canonical records, 54 CED atoms, 30 resolved flags, `student_release=false`
- `/api/units/unit-3/journeys` → empty journey list
- `/api/units/unit-3/application-lab` → 0 items
- `/api/units/unit-3/objects/U3-K-001` → canonical locked object served successfully

## Source completeness note

No separate Unit 3 packet or guided-notes file was located in the available File Library search. This is nonblocking for F1 because the full 136-slide teacher deck and all 24 teacher-assessment items were available and crosswalked. If another required Unit 3 packet is later supplied, it should be audited against this lock before student release.

## Next gate

**F2 — learning-function classification and palace architecture.**

The 186 locked records must next be classified by learning destination before any Unit 3 story prose is authored. Not every record should become a permanent locus.
