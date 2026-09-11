# Unit 2 F4E Narrative QA

## Release state

- Stage: **F4E**
- Journey: **U2-J5 · Gradient Transit Hub**
- Story title: **The Transit Hub With No Direction Signs**
- Student release: **false**
- Developer preview: **true**
- Polished Unit 2 journeys after this stage: **5 of 7**

## Narrative totals

- Scenes: **10**
- Locked knowledge records taught: **26**
- Optional first-exposure Quick Recalls: **3**
- Narrative words: **3,533**
- Average narrative words per scene: **353.3**
- Shortest scene: **309 words**
- Longest scene: **452 words**

## Required QA results

- All ten F3 loci appear in locked route order: **PASS**
- All 26 Journey 5 knowledge records appear exactly once: **PASS**
- Canonical scientific statements match the F1 lock exactly in story-beat metadata: **PASS**
- Every scene has explicit left / center / right geography: **PASS**
- Every scene has Dr. Nia Park plus stable scientific parts with visual identities and jobs: **PASS**
- Every scene contains at least 300 words of narrative prose: **PASS**
- Mean scene length is at least 340 words: **PASS**
- Only the three F3-approved Quick Recall points interrupt first exposure: **PASS**
- Student-facing source-management language scan: **PASS**
- Dynamic equilibrium retains molecular motion: **PASS**
- Facilitated diffusion remains passive despite protein use: **PASS**
- Carrier protein is represented by binding and conformational change, not an open pore: **PASS**
- Aquaporin scene preserves some direct water permeability through the bilayer: **PASS**
- Endocytosis and exocytosis use membrane remodeling and energy, not protein channels: **PASS**
- Na⁺/K⁺ ATPase direction and 3-out / 2-in stoichiometry: **PASS**
- Na⁺/K⁺ ATPase is not presented as the sole origin of resting membrane potential: **PASS**
- Proton pump spends ATP upstream; H⁺ gradient provides immediate energy to sucrose symport: **PASS**
- F4E content-lock hashes: **PASS**
- Full repository automated tests: **61 / 61 PASS**

## Scene-level results

| # | Locus | Words | Records | Quick Recall | Terms / relationships |
|---:|---|---:|---:|:---:|---|
| 1 | Concentration Ramp | 452 | 3 | Yes | Concentration gradients, Diffusion, Passive transport |
| 2 | Active Transport Lift | 368 | 3 | No | Active transport, Energy for active transport, Active transport proteins |
| 3 | Facilitated Diffusion Corridor | 309 | 2 | No | Facilitated diffusion proteins, Large polar facilitated diffusion |
| 4 | Channel Turnstiles | 324 | 3 | No | Ion channels, Channel protein, Membrane polarization |
| 5 | Carrier Shuttle | 310 | 1 | No | Carrier protein |
| 6 | Aquaporin Floodgate | 317 | 1 | No | Aquaporins |
| 7 | Bulk Cargo Dock | 326 | 3 | No | Bulk transport energy, Endocytosis, Exocytosis |
| 8 | Endocytosis Intake Bays | 326 | 3 | No | Phagocytosis, Pinocytosis, Receptor-mediated endocytosis |
| 9 | Electrical Pump Control | 366 | 4 | Yes | Na+/K+ pump, Membrane potential, Electrogenic pump, Na+/K+ ATPase stoichiometry |
| 10 | Proton Cotransport Platform | 435 | 3 | Yes | Proton pump, Cotransport, Sucrose-H+ symport |

## Narrative design decision

Journey 5 uses one colored cargo case to keep comparisons stable while the physical cause of transport changes. The learner repeatedly asks three questions without seeing them as a checklist. Which direction is the cargo moving? What structure provides the route? Where does the usable energy come from?

The story deliberately avoids treating the transit-hub slope, signs, or characters as forces on molecules. Random molecular motion produces diffusion. Gradients determine net driving direction. Membrane chemistry limits direct passage. Proteins provide selective routes. ATP powers specified active processes. Electrochemical gradients store potential energy that can later drive coupled transport.

## Release gate

F4E remains a developer preview. Journey 6 must pass its own prose and scientific QA before it is added to the Unit 2 preview.
