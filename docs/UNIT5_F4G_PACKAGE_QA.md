# Unit 5 F4G Package QA

## Result

**PASS**

## Release accounting

- Unit 5 canonical records remain **152**.
- F2 permanent loci remain **50**.
- F3 scene briefs remain **50**.
- Journeys 1–6 remain protected by their earlier narrative locks.
- Journey 7 contains **6 scenes**, **10 locked records**, and **2 optional Quick Recalls**.
- Journey 7 contains **3,742 narrative words**, averaging **623.7 words per scene** with a **617-word minimum**.
- Total Unit 5 developer preview now contains **7 journeys**, **43 scenes**, and **15 optional Quick Recalls**.
- Unit 5 remains `student_release = false` and `preview_release = true`.
- Unit 5 Challenge Lab runtime remains empty.
- The production runtime remains `v2-apbio-0.22.0-u4-f6`.

## Regression gates

- Unit 1 full QA **PASS**.
- Unit 2 F5 QA **PASS**.
- Unit 3 F6 QA **PASS**.
- Unit 4 F6 QA **PASS**.
- Unit 5 F1 through F4G QA **PASS**.
- Units 1–3 mainline QA **PASS**.
- Units 1–4 mainline QA **PASS**.
- Unit 3 F6 browser-facing logic QA **PASS**.
- Unit 4 F6 browser-facing logic QA **PASS**.
- Python test suite **241 / 241 PASS**.
- Frontend JavaScript syntax checks **PASS**.
- Python compilation **PASS**.
- F4G deterministic rebuild checked **10 generated artifacts** with **0 changes**.
- Live FastAPI developer-preview smoke test **PASS**.
- The **216 protected Units 1–4 files** remain covered by the F1 upstream SHA-256 protection manifest and F4G QA reports no protected-file changes.

## F4G scientific safeguards

- Genetic linkage remains a same-chromosome inheritance tendency and never becomes a permanent bond.
- Crossing over between nonsister chromatids creates recombinant marker combinations when the exchange changes the tracked interval.
- Parental and recombinant classes are classified against the original parental arrangement before frequency arithmetic.
- Recombination frequency remains recombinant outcomes divided by total scored outcomes.
- Recombination frequency is genetic evidence and not direct physical DNA distance.
- For relatively short intervals, about 1 percent recombination corresponds to approximately 1 centimorgan.
- Centimorgans remain genetic-map units.
- Multiple crossovers can make observed two-locus recombination frequency underestimate longer map distances.
- Observed recombination frequency approaches a 50 percent ceiling.
- A value near 50 percent cannot by itself distinguish genes on different chromosomes from very distant loci on the same chromosome.

## Archive boundary

The release ZIP excludes source PDFs, `.git`, `.env`, SQLite databases, Python caches, pytest caches, compiled Python files, and local temporary artifacts.
