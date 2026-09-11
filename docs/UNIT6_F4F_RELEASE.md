# Unit 6 F4F Release

## Release state

**F4F complete · all six Unit 6 narratives polished · developer preview only**

Unit 6 remains student-unreleased. The validated public runtime remains Units 1–5 at `v2-apbio-0.24.0-u5-f6`.

F4F completes the narrative-development portion of Unit 6 without creating final Memory Objects, live Challenge Lab tasks, or student-visible Unit 6 routes.

## New F4F work

Journey 6 is now fully written from the five F3-locked biotechnology loci.

**Story title**

`The Lab That Kept Using the Wrong Tool`

**Route**

Genetic Engineering Intake → Gel Electrophoresis Lane → PCR Thermal Cycler → Transformation Expression Bench → Sequence and Profile Analysis Desk

**Journey 6 accounting**

- scenes: **5 / 5**
- locked F3 records represented: **11 / 11**
- exact-name targets explicitly introduced: **9 / 9**
- optional first-exposure Quick Recalls: **2**
- narrative words: **2,919**
- mean scene length: **583.8 words**
- shortest scene: **550 words**
- longest scene: **625 words**

## Journey 6 narrative contract

The story keeps one coded DNA sample, **U6-X**, identifiable throughout the investigation. Derived analytical aliquots retain that code. When recombinant bacterial expression is needed, a separate engineered plasmid is introduced and never substituted for the original sample.

The five scenes require students to distinguish what each technique physically does.

- genetic engineering can manipulate or analyze DNA and RNA
- gel electrophoresis separates DNA fragments in an electric field and produces a band pattern
- negatively charged DNA moves toward the positive electrode, with smaller fragments generally moving farther/faster in common agarose gels
- PCR uses ordered denaturation, primer annealing, and extension cycles to amplify a selected DNA region
- laboratory bacterial transformation introduces engineered DNA into bacteria and can support propagation or expression under appropriate regulatory conditions
- DNA sequencing determines nucleotide order
- DNA profile/fingerprint evidence supports comparison among samples without being treated as equivalent to a complete nucleotide sequence

Gel electrophoresis, PCR, transformation, sequencing, and profile comparison remain different operations with different inputs, mechanisms, and outputs.

## Completed Unit 6 narrative state

F4F completes all permanent Unit 6 narrative loci.

| Journey | Scenes | Locked records | Exact-name targets | Quick Recalls | Narrative words |
|---|---:|---:|---:|---:|---:|
| U6-J1 · The Archive That Could Not Make a Copy | 12 | 42 | 34 | 3 | 6,492 |
| U6-J2 · The Message That Was Not Ready to Leave | 8 | 26 | 21 | 3 | 4,504 |
| U6-J3 · The Assembly Line That Lost Its Reading Frame | 8 | 20 | 16 | 3 | 4,258 |
| U6-J4 · The Control Center That Forgot Its Cell Identities | 12 | 36 | 29 | 4 | 5,995 |
| U6-J5 · The Mutation Yard Where Every Change Was Blamed | 8 | 26 | 25 | 3 | 4,187 |
| U6-J6 · The Lab That Kept Using the Wrong Tool | 5 | 11 | 9 | 2 | 2,919 |
| **Total** | **53** | **161** | **134** | **18** | **28,355** |

The **161 palace-managed records are represented exactly once** across the 53 permanent scenes.

## Frozen narrative hashes

```text
U6-J1  fe01ed27cd6a8830022f131c22bcce74f9ad094aef189c991effb66f09741b83
U6-J2  62745c2fdcf98af10667a7cefa9907b420036952050d59aea7231dbd66de1ec6
U6-J3  91995e5f1e8f30072d511701556214fa16ba28b8533b460719bfe5b136722715
U6-J4  e074f28b35de6fe96de2015b1d8732055bc238235fa87367cf1976cb1df30b89
U6-J5  23b21efa45badeaef8db794af47f6fed87a623758e3c87487de2dcd68326aac1
U6-J6  cbb16bdd2ca5e9f386150860c5b802c93fadae25ff918db7bc366190f1f6c95c
```

Journeys 1–5 are byte-frozen from their prior F4 gates. Journey 6 is newly frozen by `content-lock-f4f.json`.

## Regression

The F4F branch passed

- Unit 1 full QA
- Unit 2 F5 QA
- Unit 3 F6 QA
- Unit 4 F6 QA
- Unit 5 F6 QA
- Units 1–3, Units 1–4, and Units 1–5 mainline QA
- Unit 6 F1 through F4F QA
- **301 / 301 Python tests**
- Unit 3 F6 UI-logic QA
- Unit 4 F6 UI-logic QA
- Unit 5 F6 UI-logic QA
- JavaScript syntax checks
- Python compilation
- live FastAPI boundary checks
- deterministic F4F rebuild with **8 checked generated artifacts and 0 changes**

The Unit 6 public API continues to return zero guided journeys and zero Challenge Lab tasks, and direct requests for `U6-J6` remain unavailable through the public student journey endpoint.

## Next gate

Proceed to **Unit 6 F5 runtime finalization**.

F5 should create the final Unit 6 runtime while preserving all F1–F4F locks. The locked architecture already specifies 161 palace-managed records, 134 delayed exact-name Review targets, 37 confusable sets, 16 Challenge Lab architecture records, and 25 non-runtime scope guards.
