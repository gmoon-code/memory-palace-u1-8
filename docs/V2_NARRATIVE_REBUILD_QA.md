> **Historical milestone note:** This report documents the earlier Water-only narrative rebuild. Unit 1 has since been fully migrated. See `UNIT1_FULL_QA.md` for the current release status.

# V2 Narrative Rebuild QA

## Scope

This pass rebuilds the active Water Atrium presentation and scene layout while preserving the F6.9 scientific source layer.

## Major corrections

### The V2 app now serves the rewritten Water journey

The starter contained a rewritten `reference-journey-water.json`, but the API still returned the preserved F6.9 journey from `source/guided-journeys.json`. The active student preview therefore continued to show the older narrative.

The backend now serves `reference-journey-water.json` for Z3 while keeping the preserved F6.9 journey bank unchanged for migration and comparison.

### Narrative prose rewritten

All 11 Water Atrium scenes were rewritten as one connected emergency through a vertical hotel. The journey contains approximately 2,200 words of story prose, divided into manageable scene segments.

Every scene now includes:

- exact location description
- route orientation
- three-zone spatial layout
- scientific cast with visual identity and job
- three or more narrative paragraphs
- story-embedded terminology
- concise memory anchors
- causal exit to the next locus

### Stable recurring guide

Mara Vale now has a stable identity and narrative purpose as the Sky Hotel's chief systems engineer. She remains part of the journey without becoming the source of scientific authority. The water's behavior carries the scientific explanation.

### Student-facing meta language removed

The active Water narrative contains no student-facing references to PPT, CED, locked definitions, teacher materials, or source documents.

### Quick Recall corrected

Quick Recall now hides:

- scene prose
- location name
- route labels
- memory-anchor cards

This prevents answer leakage, including the final Buffer checkpoint where the location name itself contains the answer.

Recall is also optional during first exposure. Students can continue the story without completing a forced sequence of retrieval phases.

### Story-specific hints

Hints now come from the current story scene, such as “a connected water column climbing a narrow tube while also clinging to its walls,” rather than exposing legacy implementation/mnemonic metadata.

## Automated QA

The rebuilt repository passes:

- preserved F6.9 SHA-256 content-lock verification
- 229 canonical-record count
- 207 Memory Object count
- 9 preserved journeys
- 78 preserved loci
- 11 Water Atrium scenes
- all 30 Water Atrium Memory Objects represented exactly once
- three intended Quick Recall checkpoints
- scene layout/cast/story completeness checks
- student-visible source-meta-language check
- narrative chunk-size check
- FastAPI reference-journey routing test
- JavaScript syntax checks
- Python compilation
- HTML parsing

## Current release boundary

Only Water Atrium is considered narratively rebuilt. The other eight Unit 1 palaces remain preserved but are intentionally withheld from the student interface until they meet the same scene standard.
