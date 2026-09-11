# Memory Palace V2 · Unit 2 F5 Finalization and Release Audit

## Release decision

**PASS — Unit 2 is student-ready at the content/runtime architecture level.**

This decision does not mean the entire software product is production-ready. Classroom/browser usability, accessibility, finished visual assets, authentication hardening, and production hosting remain separate product-validation concerns.

## Canonical accounting

- Locked Unit 2 canonical records: **142**
- Records taught through guided stories: **133**
- Records assigned to Challenge Lab: **9**
- Explicitly accounted records: **142 / 142**
- Unaccounted records: **0**
- Guided journeys: **7 / 7**
- Permanent loci: **49 / 49**
- Optional first-exposure recalls: **17**

No canonical scientific record was added, removed, or rewritten during F5. F5 changes the learner/runtime destination and retrieval layer only.

## Student learning flow

The visible student flow remains intentionally small.

1. **Learn** — read or listen to a guided story. Quick Recall is optional.
2. **Review** — complete a short delayed retrieval session. At most five due items are displayed at once.
3. **Challenge Lab** — solve one transfer/application problem at a time after learning the relevant stories.

The 17 confusable sets do not appear as a new navigation mode. They enter **Review** automatically only after all associated terms have been encountered.

## Challenge Lab

The nine records classified as `CHALLENGE_LAB` in F2 are now implemented one-to-one.

| ID | Challenge | Primary demand |
|---|---|---|
| U2-K-134 | Albumin production under organelle disruption | infer secretion consequences from rough ER/Golgi function |
| U2-K-135 | Trace a newly made insulin molecule | trace the secretory pathway |
| U2-K-136 | Detoxification and damaged-organelle cleanup | smooth ER + lysosome/autophagy reasoning |
| U2-K-137 | Surface area-to-volume calculation | calculate SA, V, SA:V and interpret exchange consequences |
| U2-K-138 | Cold-water membrane adaptation | justify unsaturated-tail effects on fluidity |
| U2-K-139 | Read a diffusion diagram | predict net diffusion and preserve dynamic equilibrium |
| U2-K-140 | Sucrose uptake and external pH | interpret proton-gradient-driven cotransport |
| U2-K-141 | Macrophage recognition and engulfment | connect recognition with phagocytosis |
| U2-K-142 | Calculate water potential and predict movement | calculate Ψs and Ψ and predict net water movement |

The Challenge Lab does not create new permanent palace locations and does not grant story mastery from image recognition alone.

## Exact-name Review

F2 classified **106** records as exact-name retrieval targets. F5 verifies that all 106 occur in the seven story files with `exact_name: true` and creates one delayed Review target for each.

The normal Review prompt uses an answer-redacted scientific description. Target words and close morphological forms are removed from the cue so a student must retrieve the name instead of reading it inside the definition.

- Exact-name targets: **106 / 106**
- Missing story targets: **0**
- Mandatory spelling gates: **0**
- Default exact-name prompt leaks detected by F5 QA: **0**

Hints remain optional and are derived from the story image after target-name redaction.

## Delayed mixed discrimination

All **17** confusable sets locked in F2 are operationalized in F5.

- Confusable sets: **17 / 17**
- Mixed questions: **44**
- Initial delay after all members are encountered: **48 hours minimum**
- Visible Review load: **maximum five due items**

A set is not scheduled merely because it exists in the curriculum. Every associated knowledge record must first be encountered in a story. Correct responses advance through the set's questions and then reschedule the set after a longer delay. Incorrect responses return sooner.

Examples include rough versus smooth ER, lysosome versus peroxisome, thylakoid versus granum versus stroma, integral versus peripheral versus transmembrane proteins, passive versus facilitated versus active transport, tonicity terms, water-potential components, and electrochemical transport terms.

## Historical-lock preservation

The source/science and architecture stages remain immutable artifacts.

- F1 scientific/source lock — preserved
- F2 learning architecture lock — preserved
- F3 scene-brief lock — preserved
- F4A–F4G individual narrative locks — preserved
- F5 finalization artifacts — separately locked

F5 does not rewrite the F4 journey files to change their historical `PILOT_PREVIEW_*` metadata. The F5 registry and `status-f5.json` promote the already locked narratives to student-ready status without invalidating earlier hashes.

## Runtime/API release state

The live Unit 2 API reports:

- `status: STUDENT_READY`
- `student_release: true`
- `preview_release: false`
- `canonical_records: 142`
- `application_challenges: 9`
- `exact_name_review_targets: 106`
- `mixed_discrimination_sets: 17`

Student-ready Unit 1 and Unit 2 can be opened from the course-development area on Home. Unit 1 remains the default route when no unit is specified.

## Automated QA result

- Unit 1 content lock — PASS
- Unit 1 full narrative QA — PASS
- Unit 2 F1 scientific lock — PASS
- Unit 2 F2 architecture lock — PASS
- Unit 2 F3 scene-brief lock — PASS
- Unit 2 F4A–F4G narrative QA — PASS
- Unit 2 F5 finalization QA — PASS
- Full Python test suite — **78 / 78 PASS**
- JavaScript syntax — PASS
- Python compilation — PASS
- Live FastAPI smoke test — PASS
- ZIP integrity — PASS

## Next curriculum gate

Do not begin Unit 3 mnemonic/narrative generation directly. The next curriculum stage is **Unit 3 source inventory and scientific lock**, using the Unit 3 classroom source, current AP Biology CED, and Campbell Biology as the authority stack before learning architecture is designed.
