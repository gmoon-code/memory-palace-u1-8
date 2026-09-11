# Unit 3 F4A Narrative QA

## Release gate

**PASS — Journey 1 polished narrative preview only**

Unit 3 remains `student_release: false`. F4A exposes only **U3-J1 Enzyme Catalysis Workshop** for developer/classroom narrative review. Journeys 2–7 remain blocked.

## Pilot accounting

| Metric | Result |
|---|---:|
| Polished journeys | 1 |
| Polished scenes | 3 |
| Locked knowledge records represented | 11 / 11 |
| Optional first-exposure recalls | 2 |
| Narrative words | 1,359 |
| Average words per scene | 453 |
| Shortest scene | 431 words |
| Student release | No |
| Preview release | Yes |

## Narrative route

1. **Catalyst Energy Ramp** — compare the same reaction with a high uncatalyzed activation barrier and a lower enzyme-catalyzed barrier.
2. **Active-Site Dock** — carry the same amber substrate into an active-site pocket, test shape and chemical compatibility, then observe induced fit and the enzyme-substrate complex.
3. **Catalytic Turnover Bench** — complete catalysis, release products, and immediately reuse the same enzyme for another cycle.

The continuity object is one amber substrate model that persists from free reactant through binding, catalytic conversion, and product release.

## Spatial-clarity gate

Every scene contains three stable, explicitly visible zones. The positions never swap while the scientific action occurs.

### U3-L01

- **Left** — uncatalyzed energy hill
- **Center** — enzyme-catalyzed lower barrier
- **Right** — product-side exit

### U3-L02

- **Left** — free-substrate approach lane
- **Center** — active-site docking pocket
- **Right** — enzyme-substrate complex display

### U3-L03

- **Left** — fresh substrate queue
- **Center** — catalytic turnover bench
- **Right** — product release and enzyme reset

Each scene also supplies an explicit cast whose visual identity and scientific job are rendered separately by the learner interface.

## Scientific-mechanism gate

### Catalyst Energy Ramp

The story holds reactants and products fixed while comparing two reaction-energy profiles. The enzyme-catalyzed profile has a lower activation-energy barrier. The story explicitly treats the hill as an energy-profile representation, avoiding the misconception that molecules literally climb a physical hill.

Required concepts represented exactly once

- U3-K-001 Enzyme regulation role
- U3-K-002 Enzymes are protein catalysts
- U3-K-003 Activation-energy reduction
- U3-K-083 Activation energy

### Active-Site Dock

The story separates substrate identity, active-site location, compatibility, induced fit, and the enzyme-substrate complex. Mismatched comparison molecules fail to bind before the correct substrate enters. The active site then changes conformation around the bound substrate before chemistry occurs.

Required concepts represented exactly once

- U3-K-004 Active-site compatibility
- U3-K-005 Enzyme-substrate complex
- U3-K-084 Substrate
- U3-K-085 Active site
- U3-K-086 Induced fit

### Catalytic Turnover Bench

The story follows the enzyme through product release and immediately supplies a fresh substrate to the same enzyme. Catalyst reuse is therefore visible as a complete cycle. The naming convention is qualified with `-ase` examples alongside pepsin and trypsin so the pattern is never presented as universal.

Required concepts represented exactly once

- U3-K-087 Enzymes are reusable catalysts
- U3-K-088 Enzyme naming convention

## Retrieval-interruption gate

Only two first-exposure pauses are enabled.

1. After the energy-profile comparison — what changes when an enzyme catalyzes the same reaction route?
2. After active-site docking — what must be compatible for docking to occur?

The final catalyst-reuse scene flows directly into the regulation wing without another interruption.

## Misconception QA

F4A prose and visuals preserve the following distinctions.

- Activation energy is the initial reaction barrier, not the energy contained in the enzyme.
- The enzyme lowers the activation-energy barrier while the reaction comparison keeps the same reactants and products.
- A substrate is the reactant acted on by the enzyme.
- The active site is a region of the enzyme, not a separate molecule.
- Shape and chemical compatibility both matter for binding.
- Induced fit is a binding-triggered conformational adjustment, not a permanently rigid lock-and-key model.
- The enzyme-substrate complex is the temporary bound state before product release.
- Enzymes participate in repeated catalytic cycles without being consumed by the catalyzed reaction.
- Many enzyme names end in `-ase`; the suffix is a convention rather than a universal rule.

## Source/meta-language gate

Student prose contains no PPT, CED, Campbell, College Board, source-audit, canonical-record, review-flag, teacher-test, or internal layout-management language.

## Regression gate

The exact CI chain passes in repository order.

- Unit 1 build and narrative QA
- Unit 2 F1–F5
- Unit 3 F1 scientific lock
- Unit 3 F2 architecture lock
- Unit 3 F3 scene-brief lock
- Unit 3 F4A narrative QA
- **98 / 98 automated tests**
- JavaScript syntax checks
- Python compilation
- live API smoke test

## Next gate

F4B may polish **Journey 2 Enzyme Regulation Control Wing only**. The remaining Unit 3 journeys stay blocked until each preceding journey passes its prose-quality gate.
