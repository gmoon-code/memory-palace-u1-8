# Unit 3 F4D Narrative QA

## Release gate

**PASS**

Unit 3 F4D adds one polished developer-preview journey only. Unit 3 remains `student_release = false` and `preview_release = true`.

## Journey under review

- Journey ID: `U3-J4`
- Palace: **Light Capture Conservatory**
- Story: **The Light That Could Not Reach the Greenhouse**
- Scenes: **12**
- Locked knowledge records represented: **44**
- Optional first-exposure recalls: **4**
- Narrative words: **4,490**
- Average scene length: **374.2 words**
- Shortest scene: **351 words**

## Narrative route

1. **Carbon Strategy Entrance** — The Door With Three Different Ways to Get Carbon
2. **Oxygenation Timeline** — The Timeline That Fills an Atmosphere
3. **Leaf Gas-Exchange Balcony** — The Balcony Where the Leaf Breathes With the Air
4. **Chloroplast Compartment Gallery** — The Chloroplast With Two Different Workspaces
5. **Photosynthesis Redox Board** — The Board That Separates Water From Carbon Dioxide
6. **Photon and Wavelength Prism** — The Prism Where Shorter Waves Carry More Per Photon
7. **Pigment Spectrum Bench** — The Bench Where Pigments Divide the Work
8. **Photosystem Antenna Theater** — The Antenna Where Energy Moves Before an Electron Does
9. **Photosystem II Water Splitter** — The Water Splitter That Replaces a Missing Electron
10. **Thylakoid Electron-Transport Bridge** — The Bridge That Builds a Gradient While Electrons Move
11. **Photosystem I NADPH Station** — The Second Light Lift and the NADPH Exit
12. **Photophosphorylation Turbine** — The Turbine Driven by Protons, Not by Photons

## High-risk scientific safeguards

The narrative explicitly separates **carbon source** from **energy source** at the entrance. Autotroph, photoautotroph, and heterotroph are therefore learned through distinct resource routes instead of through vague producer/consumer labels.

The redox board separates water oxidation from carbon-dioxide reduction. Student prose states that photosynthetic oxygen comes from water and blocks the incorrect CO2-to-O2 arrow. The overall photosynthesis equation remains a net model and is not portrayed as one literal biochemical step.

The photon/pigment sequence distinguishes a photon from the excitation state created after absorption. At the Photosystem Antenna Theater, excitation energy moves among pigments while the same electron is explicitly **not** passed from antenna pigment to antenna pigment. An actual highlighted electron path begins only when the reaction center transfers an electron to the primary acceptor.

Photosystem II keeps three water-oxidation consequences physically separate. Replacement electrons return to PSII, protons enter the thylakoid lumen, and molecular oxygen leaves through its own outlet.

The electron-transport bridge keeps electron motion separate from proton-gradient formation. The electron does not become ATP. Redox transfer is coupled to increasing H+ concentration in the lumen, and the gradient is carried forward as a distinct continuity gauge.

Photosystem I keeps P680 and P700 attached to their correct reaction-center chlorophyll pairs. They are labels associated with PSII and PSI, not separate photosystems. NADPH is formed on the stroma side and remains distinct from ATP.

The final ATP-synthase scene states that the immediate driver of ATP synthase is **H+ moving down its electrochemical gradient**, not photons directly striking or spinning ATP synthase. ATP and NADPH then leave together as distinct light-reaction products for carbon fixation.

## Zero-loss checks

- All **44 / 44** F3 Journey 4 knowledge records occur exactly once.
- Story-beat scientific statements match the locked F1 canonical statements exactly.
- F4A, F4B, and F4C content hashes remain unchanged.
- F4D has its own independent content lock.
- All four F3-approved first-exposure recalls are preserved.
- No Unit 3 student release was enabled.
- Journey 5 remains unavailable.

## Decision

**F4D narrative gate passed.** The next permitted narrative stage is **F4E, Journey 5 — Carbon Fixation Greenhouse**. Unit 3 remains preview-only.

## Automated verification

The exact historical build sequence from Unit 1 through Unit 3 F4D passed. The repository finished at **113 / 113 automated tests**. Python compilation and frontend JavaScript syntax checks passed.

A live FastAPI smoke test reported `v2-apbio-0.15.0-u3-f4d`, exposed exactly `U3-J1` through `U3-J4`, served Journey 4 successfully, and returned 404 for `U3-J5`. A second F4D rebuild produced identical hashes for the Journey 4 story, registry, status, and content-lock files.
