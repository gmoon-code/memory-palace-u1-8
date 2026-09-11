# Memory Palace V2 · Unit 2 F4A Narrative QA

## Scope

F4A writes and integrates only **Unit 2 Journey 1 — Cell Operations Complex**. The remaining six Unit 2 journeys remain blocked behind their F3 briefs.

## Release state

- Unit 2 canonical records: **142**
- Unit 2 palace-managed records: **133**
- F4A polished journeys: **1 / 7**
- F4A polished scenes: **13 / 49**
- Knowledge records represented in Journey 1: **38 / 38 assigned by the F3 brief**
- Optional first-exposure Quick Recalls: **4**
- Student release: **false**
- Developer preview: **true**

The default application still opens Unit 1. Unit 2 F4A can be previewed with `/?unit=unit-2`.

## Narrative quality gate

Every F4A scene was required to pass the following checks.

- A precise location and route orientation are visible before prose begins.
- The scene contains three concrete spatial zones, always **left / center / right**.
- Zone descriptions identify actual biological structures or events. Internal design language such as “spatial encoding,” “layout job,” or “fixed visual zone” is prohibited from student-visible text.
- Dr. Nia Park remains the same guide throughout the journey.
- Every scientific part has a visual identity and an explicit job in the scene.
- Each scene contains at least four narrative paragraphs and at least **220 narrative words**.
- Scientific names appear after the defining structure or action becomes visible.
- All canonical scientific statements attached to the 38 F3-assigned records are copied unchanged into the memory-anchor layer.
- Misconception guards from F3 remain attached to the scene.
- Each scene ends with a causal reason to enter the next location.
- Source-management language such as `PPT`, `CED`, `Campbell`, `College Board`, `locked definition`, `canonical record`, and `source material` is blocked from student prose.

## Prose statistics

- Total story prose: **3,483 words**
- Mean scene length: **267.9 words**
- Shortest scene: **230 words**
- Longest scene: **345 words**

This word count excludes route labels, cast cards, memory anchors, and Quick Recall text.

## Story continuity

The journey is written as one repair investigation rather than thirteen independent mnemonic sketches.

1. The learner first establishes what all cells share and distinguishes prokaryotic from eukaryotic organization.
2. A traffic failure in the eukaryotic nucleus leads into the nuclear envelope and nuclear pores.
3. Unfinished ribosomal parts lead inward to the nucleolus.
4. Exported ribosomal subunits lead back into the cytoplasm, where translation begins.
5. A red-tracked protein produced on a bound ribosome becomes the continuity object for the endomembrane route.
6. The cargo is followed through rough ER, then past smooth ER, into the Golgi cis face, through modification and packaging, and out the trans face.
7. Secondary alarms then expose damaged material, vacuolar storage/water management, peroxisomal oxidation, and finally cytoskeletal instability.
8. Restoring the cytoskeleton resolves the operations failure and produces the next causal problem: unstable energy output, which points toward Journey 2.

The red color is explicitly introduced as Nia's visual tracking aid so students do not interpret it as a biological structure.

## Spatial clarity

All thirteen locations contain specific left, center, and right anchors. Examples include:

- **Cell Entry Atrium** — prokaryote bay / shared-cell essentials / eukaryote bay
- **Nuclear Archive** — double nuclear envelope / chromosome archive / nuclear pore checkpoint
- **Ribosome Platforms** — free ribosomes / mRNA translation stage / ER-bound ribosomes
- **Rough ER Assembly Hall** — ribosome-studded cytosolic surface / cisterna and lumen / budding vesicle dock
- **Golgi Receiving Stack** — incoming ER vesicle / stacked cisternae / cis receiving face
- **Golgi Dispatch Floor** — modification stations / tag-and-package station / trans dispatch face
- **Cytoskeleton Framework** — actin tension field / microtubule rail hub / intermediate-filament braces

## Character and part clarity

Dr. Nia Park is a guide, not a mnemonic for a scientific term. She directs attention and asks the learner to notice changes.

Biological structures carry the mnemonic burden through their own actions. Examples include:

- a nuclear pore opening selectively while chromosomes remain inside the nucleus,
- rRNA and proteins physically joining into ribosomal subunits,
- an mRNA strand moving through both free and bound ribosomes,
- a rough-ER cisterna visibly separating lumen from cytosol,
- an ER vesicle arriving at the Golgi cis face,
- processed cargo leaving from the trans face,
- a damaged component being delivered to a lysosome during autophagy,
- a contractile vacuole repeatedly filling and expelling water,
- catalase reducing hydrogen-peroxide accumulation in a peroxisome,
- microtubules, actin filaments, and intermediate filaments performing visibly different structural jobs.

## Quick Recall

Only four optional interruptions remain during first exposure:

1. prokaryotic versus eukaryotic organization,
2. bound ribosomes and secreted/membrane protein routing,
3. Golgi cis face,
4. microtubules.

Quick Recall now supports an explicit scene-specific answer and scene-specific visual hint, so conceptual questions do not incorrectly reveal the canonical label of an unrelated primary record.

## Regression results

- Unit 1 content lock: **PASS**
- Unit 1 full narrative QA: **PASS**
- Unit 2 F1 scientific lock: **PASS**
- Unit 2 F2 architecture lock: **PASS**
- Unit 2 F3 scene-brief lock: **PASS**
- Unit 2 F4A prose QA: **PASS**
- Automated Python tests: **41 / 41 PASS**
- JavaScript syntax: **PASS**
- Unit 2 canonical object adapter: **PASS**
- Unit 2 Journey 1 API: **PASS**
- Unit 2 Journey 2 remains unavailable: **PASS**

## Gate decision

**PASS — Journey 1 is suitable for developer/classroom narrative review.**

This is not a full Unit 2 student release. F4B should write Journey 2 from its locked F3 brief, using F4A as the prose and scene-layout reference.
