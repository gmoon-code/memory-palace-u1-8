# Unit 8 F1 Source Audit

## Authority order

- **AP Biology CED 2025** controls required exam scope, current topics, equations, and exclusion statements.
- **APBIO-U8-PPT.pdf** controls the teacher's complete classroom sequence, enrichment, examples, and embedded practice.
- **Campbell Biology 13e** verifies biological accuracy and qualifies oversimplified classroom wording before mnemonic locking.

## Source integrity

| Source | Pages | SHA-256 | Included in release? |
|---|---:|---|---|
| APBIO-U8-PPT.pdf | 96 | `2696e2e6daecb01a64f3072f344266b809a1e96d7245495c6837741f1b064818` | No |
| AP Biology CED | 240 | `30db56cdd81a231b17d48aeda420364794b285beedfd1f1a1c256de0939b793c` | No |
| Campbell Biology 13e | 1505 | `f918b65468142a17826c360a303497a1fe00a9f5e14f14c7c5a139402a1cc0cc` | No |

All 96 teacher pages are represented in `teacher-slide-inventory.json`. Image/diagram-dependent pages have explicit visual notes, including the four biogeochemical-cycle diagrams and the population/diversity equation slides.

## Current CED lock

Unit 8 contains **7 topics (8.1–8.7)** and **50 granular essential-knowledge atoms** in this F1 representation. Every atom maps one-to-one to an AP-required canonical record through `ced-coverage.json`. Current AP quantitative relationships add 11 separate equation/symbol/interpretation records, giving **61 AP-required canonical records** in total.

## Teacher-material atomization

Teacher-required content is atomized into **150 enrichment records**. Embedded practice is separated into **13 practice-only records** so a practice prompt is never misclassified as a factual memory target.

## Conflict review

**31 review flags** are all resolved before F1 lock. Full decisions are stored in `review-flags.json`. No unresolved flag remains and no flagged teacher oversimplification is permitted to become a future mnemonic statement without the locked qualification.

## Runtime boundary

F1 contains **zero** Unit 8 student journeys, scenes, Memory Objects, Review runtime records, mixed-review records, or Challenge Lab runtime tasks. The frozen Units 1–7 runtime label remains `v2-apbio-0.28.0-u7-f6`.
