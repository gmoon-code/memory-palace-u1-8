# Unit 2 F4F Narrative QA

## Release gate

F4F polishes only Unit 2 Journey 6, **Osmosis Conservatory**. Unit 2 remains a developer preview and is not student-released.

## Journey result

- Journey ID: `U2-J6`
- Story title: **The Conservatory That Could Not Hold Its Water**
- Permanent scenes: 6
- Locked knowledge records represented: 16 / 16
- Optional first-exposure Quick Recalls: 2
- Narrative words: 2,513
- Average narrative words per scene: 418.8
- Shortest scene: 333 words
- Stable guide: Dr. Nia Park
- Student release: false
- Preview release: true

## Route

1. Tonicity Orientation Hall
2. Isotonic Balance Pool
3. Hypertonic Withdrawal Chamber
4. Hypotonic Plant Greenhouse
5. Osmosis and Water-Potential River
6. Water-Potential Control Room

## Narrative-quality checks

Every scene has:

- a specific physical location;
- a stable left / center / right spatial arrangement;
- Dr. Nia Park plus at least three identifiable scientific parts, instruments, or continuity objects;
- explicit jobs for every scene component;
- substantive narrative prose rather than a glossary paragraph;
- exact scientific terminology introduced after the defining relationship or action becomes visible;
- canonical science copied exactly into the story-beat layer;
- misconception guards inherited unchanged from the locked F3 scene brief;
- a causal transition into the next location;
- a carry-forward statement for later retrieval.

## Major conceptual guards preserved

### Tonicity remains relational

The same transparent reference cell is moved among external solutions. Hypotonic, isotonic, and hypertonic are therefore taught as descriptions of an external solution **relative to that cell interior**, not as permanent labels attached to a beaker.

### Isotonic remains dynamic

Water molecules continue crossing the membrane in both directions. The scene explicitly distinguishes **no net water movement** from **no molecular movement**.

### Hypertonic does not automatically mean immediate death

The animal cell visibly shrinks as net water leaves. The story explicitly avoids turning any water loss into an instant-death rule.

### Plant and animal outcomes are separated by boundary structure

The hypotonic greenhouse places an animal cell and a plant cell in the same net water-entry condition. The animal cell swells without a rigid wall. The plant cell becomes turgid as its contents press against the cell wall, generating turgor pressure. A comparison panel then reverses water movement to demonstrate plasmolysis as a water-loss response.

### Water potential controls the general direction of osmosis

The water-potential river replaces the slogan “water moves toward more solute” with the general rule that water moves net from **higher Ψ to lower Ψ** across a selectively permeable membrane. Osmolarity is retained as a useful directional clue only when other contributors, especially pressure, are held equal.

### Pressure and solute potential remain distinct

The final control room separates `Ψp` from `Ψs`, displays `Ψ = Ψp + Ψs`, and keeps the negative sign visible in `Ψs = −iCRT`. Pressure potential is not treated as always zero. The open-beaker zero is identified as a relative convention at atmospheric pressure.

### Osmoregulation closes the story as a control problem

The final feedback system adjusts water and solute conditions to stabilize the modeled internal environment, keeping osmoregulation tied to maintenance of water balance, solute composition, and water potential.

## First-exposure load

Only two scenes interrupt the first pass with optional Quick Recall:

- Tonicity Orientation Hall
- Osmosis and Water-Potential River

The remaining exact-name targets are available for later Review without forcing repeated interruptions through the guided narrative.

## Integration QA

- Unit 1 regression: PASS
- Unit 2 F1 scientific lock: PASS
- Unit 2 F2 architecture lock: PASS
- Unit 2 F3 scene-brief lock: PASS
- Unit 2 Journeys 1–5 regression: PASS
- F4F dedicated QA: PASS
- Automated tests: 66 / 66 PASS
- Unit 2 developer preview journeys exposed: 6
- Journey 7 remains blocked
