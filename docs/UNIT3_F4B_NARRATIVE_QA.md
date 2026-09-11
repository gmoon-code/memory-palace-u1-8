# Unit 3 F4B Narrative QA

## Release state

- Stage: F4B
- Journey: U3-J2 Enzyme Regulation Control Wing
- Story: The Control Wing That Would Not Hold a Steady Rate
- Student release: false
- Developer preview: true
- Polished Unit 3 journeys after this stage: 2

## Narrative accounting

- Scenes: 8
- Locked knowledge records represented: 22
- Optional first-exposure recalls: 3
- Narrative words: 3,239
- Average scene words: 404.9
- Shortest scene: 356 words
- Longest scene: 539 words

## Zero-loss checks

All 22 F3 knowledge IDs assigned to U3-J2 are represented exactly once across the eight polished scenes. Scene order matches the locked F3 route U3-L04 through U3-L11. Each story beat preserves the exact F1 canonical verified statement carried through the F3 term introduction. No F4A content-lock file is modified by the F4B lock.

## Spatial clarity gate

Every scene preserves a fixed left, center, and right arrangement. Each zone has a concrete scientific object or control, and the primary action occurs in the center without moving the learner's orientation anchors. Dr. Nia Park remains the stable guide and the transparent reference enzyme remains the continuity object through the diagnostic wing.

## Scientific distinction gate

The prose explicitly protects the following distinctions.

- environmental rate changes versus denaturation
- reversible denaturation versus irreversible inhibition
- substrate saturation versus denaturation
- cofactor versus coenzyme versus holoenzyme
- reversible competitive inhibition versus allosteric/noncompetitive inhibition
- active site versus allosteric site
- allosteric activator versus allosteric inhibitor
- allosteric regulation versus cooperativity
- cooperativity versus feedback inhibition
- feedback inhibition versus general metabolic-pathway regulation
- persistent irreversible inhibition versus a reversible inhibitor that is merely strongly bound at one moment

## Narrative-flow gate

The route is causal. Stabilizing the enzyme exposes a concentration problem; saturation reveals a missing helper; the restored holoenzyme encounters an active-site competitor; a separate-site slowdown forces an allosteric explanation; conformational communication leads to cooperativity; a product leaving the cooperative system enters a pathway-feedback loop; the final unresolved alarm is an enzyme that fails a washout-and-recovery test.

## First-exposure retrieval

Only three F3-approved Quick Recall pauses are enabled, at the Stability Chamber, Competitive Inhibitor Gate, and Allosteric Control Panel. All other retrieval is deferred to Review.

## Automated QA

`python scripts/qa_unit3_f4b.py` validates scene order, geometry, canonical statement equality, 22/22 unique knowledge coverage, misconception guards, transition integrity, prose length, checkpoints, historical F4A lock integrity, and the new F4B content lock. The complete repository test suite is run separately after the historical build chain.

## Full regression and live-server result

The complete historical build chain from Unit 1 through Unit 3 F4B passed. The Python suite finished at **103 / 103 tests**. Python compilation and all frontend JavaScript syntax checks passed. A live FastAPI smoke test reported `v2-apbio-0.13.0-u3-f4b`, exposed exactly U3-J1 and U3-J2, served the Unit 3 preview page, and returned 404 for U3-J3.
