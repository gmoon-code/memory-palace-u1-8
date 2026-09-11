# Unit 3 F4E Narrative QA

## Release gate

**PASS**

Unit 3 F4E adds one polished developer-preview journey only. Unit 3 remains `student_release = false` and `preview_release = true`.

## Journey under review

- Journey ID: `U3-J5`
- Palace: **Carbon Fixation Greenhouse**
- Story: **The Greenhouse That Kept Losing Carbon**
- Scenes: **5**
- Locked knowledge records represented: **11**
- Optional first-exposure recalls: **2**
- Narrative words: **2,227**
- Average scene length: **445.4 words**
- Shortest scene: **405 words**

## Narrative route

1. **Calvin Cycle Energy Dock** — The Two Packages Waiting in the Stroma
2. **Carbon Fixation Bench** — The Enzyme, the Acceptor, and the Carbon They Must Not Be Confused With
3. **G3P Output and Regeneration Loop** — The Carbon That Leaves and the Carbon That Must Stay
4. **Photorespiration Detour** — The Oxygen Door at the Rubisco Junction
5. **C4 and CAM Strategy Conservatory** — Two Ways to Keep Carbon Near Rubisco

## High-risk scientific safeguards

The opening scene continues directly from Journey 4. ATP and NADPH enter the stroma through separate delivery paths, but the narrative explicitly states that neither molecule supplies the carbon that becomes carbohydrate. Carbon arrives independently as CO₂.

The carbon-fixation scene keeps **CO₂, rubisco, and RuBP** in three different spatial roles. CO₂ is the inorganic carbon input, rubisco is the enzyme catalyst, and RuBP is the carbon acceptor. Student prose explicitly states that rubisco is not itself the carbon acceptor.

The G3P/regeneration scene prevents the shortcut that the Calvin cycle directly produces one glucose molecule per pass. G3P is identified as a three-carbon sugar that can contribute to synthesis of glucose and other organic molecules. The three-CO₂ / 9-ATP / 6-NADPH accounting model remains visually secondary to the larger logic of carbon fixation, G3P output, and RuBP regeneration.

The F1 scope guard associated with detailed Calvin-cycle memorization is preserved in the student narrative through instructional restraint. The story explicitly avoids requiring a procession of every Calvin-cycle intermediate and does not add unapproved intermediate names or structures.

The photorespiration scene keeps the process distinct from mitochondrial cellular respiration. Photorespiration is tied specifically to rubisco reacting with O₂ rather than CO₂, energy use, and reduced net carbon fixation when internal CO₂ is low relative to O₂.

The evolutionary interpretation of photorespiration remains qualified. The narrative states that an evolutionary-legacy account is **one hypothesis**, while also preserving the locked statement that photorespiratory metabolism may have protective roles under conditions in which Calvin-cycle carbon processing is limited.

The final comparison permanently separates **C4 = spatial separation** from **CAM = temporal separation**. C4 initial fixation occurs in mesophyll cells with concentrated CO₂ delivered to bundle-sheath cells. CAM opens stomata mainly at night, stores fixed carbon in organic acids, and releases CO₂ during the day for the Calvin cycle.

## Zero-loss checks

- All **11 / 11** F3 Journey 5 knowledge records occur exactly once.
- The separate F1 scope-guard record `U3-K-139` remains a scope constraint rather than being turned into a palace retrieval object.
- Story-beat scientific statements match the locked F1 canonical statements exactly.
- F4A, F4B, F4C, and F4D content hashes remain unchanged.
- F4E has its own independent content lock.
- Both F3-approved first-exposure recalls are preserved.
- No Unit 3 student release was enabled.
- Journey 6 remains unavailable.
- Student-visible detailed-stoichiometry memory wording removes source-management phrasing while preserving the underlying locked science.

## Decision

**F4E narrative gate passed.** The next permitted narrative stage is **F4F, Journey 6 — Respiration Power Plant**. Unit 3 remains preview-only.

## Automated verification

The complete historical build sequence from Unit 1 through Unit 3 F4E passed. The repository finished at **118 / 118 automated tests**. Python compilation and frontend JavaScript syntax checks passed.

A live FastAPI smoke test reported `v2-apbio-0.16.0-u3-f4e`, exposed exactly `U3-J1` through `U3-J5`, served Journey 5 successfully, kept `student_release = false`, and returned 404 for `U3-J6`.

A second F4E rebuild produced identical SHA-256 hashes for the Journey 5 story, F4E registry, F4E status file, and F4E content-lock file, confirming deterministic generation for the stage artifacts.
