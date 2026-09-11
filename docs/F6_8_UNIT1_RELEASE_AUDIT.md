# F6.8 Unit 1 Finalization and Release Audit

## Release decision

F6.8 promotes AP Biology Unit 1 — Chemistry of Life to **UNIT 1 RELEASE CANDIDATE** status. The scientific layer remains the previously locked 229-record corpus. F6.8 changes release destinations, learner verification, route/audio QA, and finalization infrastructure; it does not rewrite canonical scientific statements.

## Lossless 229-record accounting

Every canonical record now has one explicit destination:

- **207** student-runtime records
- **18** course/meta-framework records retained outside the Unit 1 palace
- **4** active AP scope guards
- **0** unaccounted records

The four records that were still `SCIENCE_LOCKED_PRACTICE_BUILD_PENDING` in F6.7 are now released at the Transfer Bench:

- PK-WAT-001 — Biological consequences of altered electronegativity
- PK-WAT-002 — Water-property examples
- PK-CHO-020 — Antibiotics and rumen microbiota
- PK-U1-002 — Unit 1 experimental-design FRQ

All **16 / 16** records in the locked Transfer Bench specification now have runtime treatment.

## Scientific preservation

F6.7 and F6.8 were compared across all 229 records for canonical scientific statement, canonical label, AP scope, scientific-lock status, source reference, retrieval demand, exact-name requirement, exact-spelling requirement, and confusable set.

**Scientific/source changes: 0.**

The four new Transfer Bench objects copy their `canonical_definition` directly from the locked canonical statement. Their fresh scenario wording is practice-layer content only and may not alter the approved answer basis.

All **203 / 203** pre-existing F6.7 Memory Objects are structurally unchanged in F6.8.

## Embedded exact-name finalization

The locked embedded-name bank contains **48 cue records representing 46 unique exact scientific terms**. Two terms appear in more than one parent context: `carboxyl group` and `phosphate group`.

Earlier releases displayed embedded terms inside parent Memory Objects but did not keep an independent mastery state. F6.8 adds a separate embedded-target engine in **Unit 1 Check**. Each unique embedded target now requires:

1. exact-name production from a scientific-role prompt without the mnemonic cue,
2. a self-checked explanation of the locked scientific role, and
3. a due delayed exact-name retrieval.

Parent-object mastery no longer counts as evidence that the embedded term itself is mastered.

## Cross-palace interference audit

F6.8 adds **10 mixed interference sets**, including **6 sets that deliberately cross palace boundaries**. The sets are built only from released exact-name Memory Objects and use the objects' locked canonical definitions.

High-value cross-palace contrasts include:

- glycosidic linkage / peptide bond / phosphodiester linkage / ester linkage,
- polar covalent bond / hydrogen bond / cohesion / adhesion,
- dehydration synthesis / hydrolysis / denaturation,
- glucose / monosaccharide / ribose / deoxyribose,
- monomer / polymer / polypeptide,
- alpha and beta glucose / alpha helix / beta-pleated sheet.

A set is complete only after every member has been correctly selected from scientific context and the learner self-confirms the defining distinction. Palace position alone cannot pass the mixed test.

## AP scope-guard audit

All four established Unit 1 structural exclusions remain active and unreleased as Memory Objects:

- K-CHO-013 — specific carbohydrate polymer molecular structures
- K-PRO-026 — specific amino-acid molecular structures
- K-NA-025 — specific nucleotide molecular structures
- K-LIP-020 — specific lipid molecular structures

The new Unit 1 Check view presents all four as explicit boundaries with allowed and prohibited uses. Acknowledging a boundary is not a mastery score and does not turn the excluded structure into required recall.

## Answer-leak audit

Every released exact-name object's Level-4 default cue was checked for literal inclusion of the complete canonical answer.

**Complete target leaks in default Level-4 cue text: 0.**

The F6.7 protection that hides global palace/locus names during exact-name Produce, Reverse, and Spell remains active. Local micro-anchors continue to pass through canonical-term redaction.

## Route and Eyes Closed audio audit

Unit 1 contains **9 permanent palaces, 78 permanent loci, and 27 Eyes Closed variants**. F6.8 checks every rapid, standard, and detailed audio script against its palace route.

Final result:

- **27 / 27** audio variants present
- **78 / 78** locus labels represented in every relevant route
- all locus mentions occur in route order
- **0** audio variants with missing route locations after repair

The finalization pass corrected route-label shorthand in four older scripts:

- Z1 Rapid
- Z1 Standard
- Z2 Rapid
- Z6 Rapid

Only location labels were clarified. No scientific claim was added or changed.

## Runtime completeness

- Permanent palaces live: **9 / 9**
- Permanent loci live: **78 / 78**
- Student runtime records: **207**
- Transfer Bench records represented: **16 / 16**
- Embedded unique targets independently trackable: **46 / 46**
- AP scope guards represented: **4 / 4**
- Canonical records explicitly accounted for: **229 / 229**

## Backend and state integrity

Authenticated backend integration passed with:

- health slice `F6.8`
- 229 canonical records
- 207 student-released records
- 22 non-runtime records, all intentionally classified as 18 course/meta + 4 scope guards
- 0 remaining permanent scene blueprints
- student access to teacher content controls blocked
- F6.8 `finalizationState` surviving server sanitization and round-trip synchronization
- append-only finalization attempt events accepted
- all four F6.8 practice records visible as released in Teacher Mode

A real **F6.7 → F6.8 SQLite migration** was also tested. A learner-state probe at revision 37 survived the migration unchanged while the content release catalog synchronized to 207 student-runtime records.

## Static QA

- `node --check app.js` — PASS
- Python compile for server/build/QA/test modules — PASS
- HTML parsing — PASS
- `runtime-data.js` equals `runtime-data.json` — PASS
- 207 runtime objects have non-empty canonical definition, conventional-science cue specification, text-only prompt, application question, application answer basis, and source trace
- literal `...` truncation in those required fields — 0

## Remaining limitations before calling the software production-ready

F6.8 makes the **content architecture** a Unit 1 release candidate. It does not claim that the entire software product is production-finished. The following limitations remain intentionally visible:

1. Phase 6 scientific visuals are still specifications/placeholders, not a complete QA-approved illustration set.
2. Free-response reasoning and application tasks still rely on structured learner self-check rather than a validated automatic scorer.
3. Embedded-target delayed mastery becomes meaningful only after real learners accumulate delayed attempts.
4. Cross-palace interference sets are curated from the locked Unit 1 corpus but still require classroom usability testing for difficulty and pacing.
5. Automated browser click-through remains less complete than the server/content test suite in this environment.

## Unit 2 gate

Unit 2 should begin through the same lossless pipeline used for Unit 1: complete source audit → canonical scientific lock → mnemonic classification → locus architecture → exact-name/confusable design → NR-1.1 narration → Memory Objects → retrieval/application QA → staged release.
