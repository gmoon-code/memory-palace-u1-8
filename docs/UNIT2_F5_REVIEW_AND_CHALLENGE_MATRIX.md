# Unit 2 F5 Review and Challenge Matrix

## Review policy

Unit 2 uses three layers of retrieval without exposing three separate student modes.

**Story Quick Recall** is optional during first exposure and occurs only 17 times across 49 scenes.

**Exact-name Review** schedules 106 named targets after they are encountered. Prompts are generated from locked scientific descriptions with the target wording removed.

**Mixed discrimination** is delayed and conditional. A confusable set becomes eligible only after all associated records have been encountered, then waits at least 48 hours before entering the ordinary Review queue.

## Mixed discrimination sets

1. Prokaryotic cell / eukaryotic cell
2. Free ribosomes / bound ribosomes
3. Rough ER / smooth ER
4. Cis face / trans face
5. Lysosome / peroxisome
6. Microtubule / microfilament / intermediate filament
7. Thylakoid / granum / stroma
8. Integral membrane protein / peripheral membrane protein / transmembrane protein
9. Glycolipid / glycoprotein
10. Passive transport / facilitated diffusion / active transport
11. Channel protein / carrier protein / aquaporin
12. Endocytosis / exocytosis
13. Phagocytosis / pinocytosis / receptor-mediated endocytosis
14. Hypotonic / isotonic / hypertonic
15. Water potential / pressure potential / solute potential
16. Electrogenic pump / Na+/K+ ATPase / proton pump / cotransport
17. Mitochondrion / chloroplast

The machine-readable questions and answer explanations are stored in `content/ap-biology/unit-2/mixed-discrimination-f5.json`.

## Challenge Lab destinations

The nine practice-only canonical records are stored in `content/ap-biology/unit-2/application-lab.json`. Each item contains a fresh prompt, an answer guide, a story hint, the exact source-locked canonical statement, and a success criterion requiring scientific reasoning beyond palace recognition.

## Overload guardrails

- No mandatory Unit 2 spelling gate.
- No separate student navigation item for mixed discrimination.
- At most five due Review items shown at once.
- Mixed sets wait until their terms have been learned.
- Mixed sets wait at least 48 hours before first presentation.
- Failed mixed discrimination returns sooner; successfully completed sets return after a longer interval.
- Challenge Lab presents one problem at a time.
