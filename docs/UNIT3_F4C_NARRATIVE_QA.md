# Unit 3 F4C Narrative QA

## Release gate

**PASS**

Unit 3 F4C adds one polished preview journey only. Unit 3 remains `student_release = false` and `preview_release = true`.

## Journey under review

- Journey ID: `U3-J3`
- Palace: **Cellular Energy Exchange Hall**
- Story: **The Energy Ledger That Would Not Balance**
- Scenes: **10**
- Locked knowledge records represented: **37**
- Optional first-exposure recalls: **3**
- Narrative words: **4,147**
- Average scene length: **414.7 words**
- Shortest scene: **348 words**

## Narrative route

1. **Metabolism Route Map** — The Map With Two Opposite Roads
2. **Energy Forms Gallery** — The Gallery Where Energy Changes Its Appearance
3. **First-Law Ledger** — The Ledger That Refuses to Lose a Joule
4. **Entropy and Living Order Chamber** — The Cell That Stays Ordered Only While Energy Flows
5. **Free-Energy Terrain** — The Terrain With a Downhill Path and an Uphill Path
6. **Cellular Work Dock** — The Dock Where Energy Has to Do Something
7. **ATP Structure Station** — The Three-Phosphate Coupling Molecule
8. **ATP Hydrolysis Forge** — The Forge That Exposes the ATP Shortcut
9. **ATP Regeneration Wheel** — The Wheel That Never Gets to Stop
10. **Conserved Metabolism Archive** — The Archive Where Different Cells Share the Same Old Logic

## Scientific and narrative safeguards

The journey preserves the F3 geometry at every locus. Each scene fixes a left reference, center mechanism, and right consequence or comparison before any animated action begins. The same glowing tracker persists across the hall, but student prose explicitly identifies it as an accounting marker so energy is never represented as a material substance or molecule.

The thermodynamics sequence keeps the first and second laws distinct. The first-law ledger conserves total energy across transfers and transformations. The entropy chamber then shows that living systems can maintain local organization while energy disperses and total entropy of system plus surroundings increases.

The free-energy terrain separates thermodynamic favorability from reaction rate. Exergonic reactions are described as thermodynamically spontaneous without implying fast kinetics, and the activation-energy barrier reconnects this journey to the enzyme-catalysis workshop. The full Gibbs free-energy equation remains outside required student memorization, consistent with the locked scope guard.

ATP receives two explicit misconception guards. The structure station presents ATP first as a nucleotide composed of adenine, ribose, and three phosphates. The hydrolysis forge states that energy is required to break chemical bonds and that the favorable net energy change comes from the complete ATP + H2O reaction ending in lower-free-energy products. No scene claims that usable energy simply bursts from a broken phosphate bond.

The final archive presents conservation across lineages without implying that every pathway detail or cellular location is identical. Glycolytic and chemiosmotic logic is compared across Archaea, Bacteria, and Eukarya as evidence consistent with common ancestry.

## Zero-loss checks

- All **37 / 37** F3 Journey 3 knowledge records occur exactly once.
- Story-beat scientific statements match the locked F1 canonical statements exactly.
- F4A and F4B content hashes remain unchanged.
- F4C has its own independent content lock.
- No Unit 3 student release was enabled.
- Journey 4 remains unavailable.

## Automated verification

The exact historical build sequence from Unit 1 through Unit 3 F4C passed. The repository finished at **108 / 108 automated tests**. Python compilation and frontend JavaScript syntax checks passed.

A live FastAPI smoke test reported `v2-apbio-0.14.0-u3-f4c`, exposed exactly `U3-J1`, `U3-J2`, and `U3-J3`, served Journey 3 successfully, and returned 404 for `U3-J4`.

## Decision

**F4C narrative gate passed.** The next permitted narrative stage is **F4D, Journey 4 — Light Capture Conservatory**. Unit 3 remains preview-only.
