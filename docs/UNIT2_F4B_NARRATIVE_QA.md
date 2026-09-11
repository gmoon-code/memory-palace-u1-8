# Memory Palace V2 · Unit 2 F4B Narrative QA

## Scope

F4B writes and integrates **Unit 2 Journey 2 — Energy Conversion Annex** while preserving Journey 1 unchanged. Journeys 3–7 remain blocked behind their F3 scene briefs.

## Release state

- Unit 2 canonical records: **142**
- Unit 2 palace-managed records: **133**
- Polished journeys: **2 / 7**
- Polished scenes: **18 / 49**
- Journey 2 assigned knowledge records represented: **12 / 12**
- Journey 2 optional first-exposure Quick Recalls: **2**
- Total optional recalls across polished Unit 2 journeys: **6**
- Student release: **false**
- Developer preview: **true**

The default application still opens Unit 1. Unit 2 preview is available with `/?unit=unit-2` and now contains Journeys 1 and 2.

## Journey 2

**Energy Conversion Annex — The Power Map Blackout**

The story begins immediately after the Cell Operations Complex is repaired. A new energy-output alarm leads Dr. Nia Park and the learner into an annex containing two transparent organelle chambers. The story deliberately avoids vague organelle slogans. The learner must restore the energy map by locating structures and processes precisely.

### Route

1. Mitochondrial Membrane Airlock
2. Cristae Generator Deck
3. Energy-Demand Control Bay
4. Chloroplast Entry Chamber
5. Thylakoid and Stroma Gallery

## Narrative quality gate

Every Journey 2 scene must:

- orient the learner to a concrete physical location before new terminology appears,
- maintain explicit **left / center / right** geography,
- use biological structures themselves as the memorable actors,
- keep Dr. Nia Park stable as a guide rather than using her as a mnemonic,
- contain at least four connected narrative paragraphs,
- contain at least **280 narrative words**,
- reveal the defining structure or action before naming the scientific term,
- preserve the F1 canonical scientific statement exactly in the memory-anchor layer,
- preserve F3 misconception guards,
- end with a causal transition into the next locus,
- contain no student-facing source-management language or internal design jargon.

## Prose statistics

- Journey 2 story prose: **1,724 words**
- Mean scene length: **344.8 words**
- Shortest scene: **300 words**
- Longest scene: **411 words**
- Journey 1 + Journey 2 polished prose: **5,207 words**

These totals exclude route labels, cast cards, memory anchors, and Quick Recall text.

## Spatial and conceptual clarity

### Mitochondrial Membrane Airlock

The scene fixes the smooth outer mitochondrial membrane on the left, the narrow intermembrane space in the center, and the inner membrane enclosing the matrix on the right. Matrix enzymes, mitochondrial DNA, and ribosomes become visible only after the compartments are spatially separated.

### Cristae Generator Deck

A smooth outer boundary remains visible while one continuous inner membrane folds repeatedly through the center. Respiratory membrane machinery expands across the enlarged surface. The learner can follow the same membrane line through every fold, preventing cristae from being mistaken for independent membranes or compartments.

### Energy-Demand Control Bay

A lower-demand cell is displayed on the left, a demand meter in the center, and a higher-demand cell on the right. The number and morphology of mitochondria change with biological context, preventing a rigid “high-energy cell = fixed number of mitochondria” rule.

### Chloroplast Entry Chamber

The chloroplast envelope is fixed left, the transparent organelle interior is central, and plant/photosynthetic-algal context is fixed right. Distribution, double-membrane structure, and photosynthetic function are therefore separated from the deeper thylakoid vocabulary.

### Thylakoid and Stroma Gallery

A granum stack is fixed left, one chlorophyll-bearing thylakoid membrane is isolated in the center, and stroma fills the right. This allows the learner to distinguish:

- **thylakoid** = one membranous sac,
- **granum** = a stack of thylakoids,
- **chlorophyll** = light-absorbing pigment in thylakoid membranes,
- **stroma** = fluid around thylakoids where the Calvin cycle occurs.

## Story continuity

The continuity object is a pulsing energy-demand meter.

1. The meter first reveals that simply seeing a mitochondrion as an orange oval is inadequate.
2. Separating its two membranes reveals intermembrane space and matrix.
3. The inner membrane then folds into cristae, increasing working surface.
4. The meter shifts from organelle architecture to whole-cell demand, showing that mitochondrial abundance varies with context.
5. Green light from the neighboring chamber introduces chloroplasts as a second energy-conversion organelle.
6. The chloroplast is first placed in plant/photosynthetic-algal context and opened through its double envelope.
7. The learner then enters the interior and separates thylakoid, granum, chlorophyll, and stroma.
8. The meter stabilizes only after the two organelles have distinct internal maps. The next alarm is a scale problem, leading naturally to Journey 3.

## Quick Recall

Only two optional first-exposure recalls occur:

1. **Cristae** — identify the folds of the mitochondrial inner membrane that increase membrane surface area.
2. **Granum** — identify a stack of thylakoids.

All other exact-name retrieval is scheduled later through Review.

## Scientific guardrails retained

The story explicitly avoids several common misconceptions:

- cristae do not independently create the matrix/intermembrane-space boundary,
- cristae are folds of one continuous inner membrane,
- mitochondrial abundance is context-dependent and not a fixed cell-type number,
- chloroplasts do not occur in all eukaryotes or all plant tissues,
- granum and thylakoid are not synonyms,
- the Calvin cycle is placed in the stroma, not inside thylakoids.

## Regression results

- Unit 1 content lock: **PASS**
- Unit 1 full narrative QA: **PASS**
- Unit 2 F1 scientific lock: **PASS**
- Unit 2 F2 architecture lock: **PASS**
- Unit 2 F3 scene-brief lock: **PASS**
- Unit 2 F4A Journey 1 prose QA: **PASS**
- Unit 2 F4B Journey 2 prose QA: **PASS**
- Automated Python tests: **46 / 46 PASS**
- JavaScript syntax: **PASS**
- Unit 2 API exposes Journeys 1–2 only: **PASS**
- Journey 3 remains blocked: **PASS**

## Gate decision

**PASS — Journey 2 is suitable for developer/classroom narrative review.**

F4C may now write Journey 3 — Scaling Observatory — from its locked F3 briefs while preserving Journeys 1 and 2 unchanged.
