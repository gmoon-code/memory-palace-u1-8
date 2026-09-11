# Unit 3 F4F Narrative QA

## Release boundary

Unit 3 F4F adds one polished developer-preview journey. Unit 3 remains `student_release = false` and `preview_release = true`.

- Journey ID: `U3-J6`
- Palace: **Respiration Power Plant**
- Story: **The Power Plant With Fuel but No Power**
- Scenes: **12**
- Locked knowledge records: **35 / 35**
- Optional first-exposure Quick Recalls: **3**
- Narrative words: **5,025**
- Average scene: **418.8 words**
- Shortest scene: **363 words**

## Narrative quality gate

Every scene passes the following checks.

- stable left/center/right geography
- conventional scientific structure before mnemonic embellishment
- Dr. Nia Park retained as the same Unit 3 guide
- at least four identifiable cast elements including the guide
- at least 350 narrative words
- explicit causal transition to the next location
- exact-name target introduced after the defining mechanism is visible
- no student-facing source-management language
- locked F3 scene geometry and misconception guards preserved

## Scientific mechanism gate

F4F explicitly protects the following high-risk relationships.

- Cellular respiration is a coordinated pathway and the overall equation is net accounting, not one literal cellular reaction.
- Glycolysis occurs in the cytosol and releases no CO₂.
- Glycolysis ends with pyruvate, NADH, and net ATP.
- Substrate-level phosphorylation is direct enzymatic phosphate transfer and is kept distinct from oxidative phosphorylation and photophosphorylation.
- FADH₂ is not portrayed as a glycolysis product.
- Pyruvate oxidation yields acetyl-CoA, CO₂, and NADH before the citric acid cycle.
- The citric acid cycle occurs in the mitochondrial matrix and detailed intermediate memorization remains secondary.
- Glycolysis remains outside the mitochondrion in the cytosol.
- NADH/FADH₂ donate electrons to the respiratory ETC. Electrons do not become ATP.
- Electron-transfer energy is coupled to H⁺ pumping from matrix to intermembrane space. Electrons themselves are not pumped into the intermembrane space.
- The proton-rich intermembrane space has lower pH than the matrix.
- Oxygen is the terminal electron acceptor in aerobic respiration and is reduced to water. Oxygen is not a direct ATP source.
- Chemiosmosis uses proton-motive force as H⁺ moves through ATP synthase.
- H⁺ does not become ATP or phosphate.
- Oxidative phosphorylation includes both gradient-generating electron transport and ATP-synthase chemiosmosis.
- Respiratory ATP yield is a variable estimate rather than one universal integer.
- Proton leak can reduce ATP-capture efficiency and increase heat release.
- Prokaryotes can perform respiratory electron transport and proton translocation across the plasma membrane without mitochondria.

## Content accounting

- All **35 / 35** F3 Journey 6 knowledge records occur exactly once.
- All exact-name targets are explicitly introduced in polished prose.
- All story-beat scientific statements equal the F3 locked canonical statements and F1 canonical catalog.
- All **3 / 3** F3 Quick Recall locations are preserved.
- F4A, F4B, F4C, F4D, and F4E content-lock hashes remain unchanged.
- F4F has its own independent content lock.

## Unit 3 preview after F4F

Journeys 1–6 are polished and available in the Unit 3 developer preview.

- **50 polished scenes**
- **160 locked knowledge records** represented across Journeys 1–6
- **17 optional first-exposure recalls**
- **20,487 narrative words** across the six polished journeys

Journey 7 remains blocked until F4G.

## Result

**F4F narrative gate passed.** The next permitted narrative stage is **F4G, Journey 7 — Fermentation and Metabolic Flexibility**. Unit 3 remains preview-only.

## Historical regression and runtime verification

The complete historical build sequence from Unit 1 through Unit 3 F4F passed after Journey 6 integration. The repository finished at **123 / 123 automated tests**. Python compilation and all frontend JavaScript syntax checks passed.

A live FastAPI smoke test reported `v2-apbio-0.17.0-u3-f4f`, exposed exactly `U3-J1` through `U3-J6`, served Journey 6 successfully, kept `student_release = false` and `preview_release = true`, and returned 404 for `U3-J7`.

A second F4F rebuild produced identical SHA-256 hashes for the Journey 6 story, F4F registry, F4F status file, and F4F content-lock file. F4F generation is deterministic for the stage artifacts.
