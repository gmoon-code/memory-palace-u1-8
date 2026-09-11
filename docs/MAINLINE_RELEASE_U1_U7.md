# Memory Palace V2 · Units 1–7 Mainline Release Audit

## Release state

AP Biology Units **1 through 7** are student ready. Unit 8 remains source-ready and unreleased. Unit 7 has completed its final F6 classroom/browser-facing validation gate.

Current runtime

```text
v2-apbio-0.28.0-u7-f6
```

## Consolidated accounting

| Measure | Units 1–7 |
|---|---:|
| Canonical records | **1,306** |
| Guided journeys | **50** |
| Permanent scenes | **390** |
| Challenge Lab items | **99** |

## Unit 7 contribution

Unit 7 contributes **215** canonical records, **174** runtime Memory Objects, **6** guided journeys, **55** permanent scenes, **18** optional first-exposure Quick Recalls, **16** Challenge Lab tasks, **94** exact-name Review targets, **80** meaning/mechanism-only palace records, **33** mixed-discrimination sets with **102** questions, and **25** non-runtime scope guards.

The Unit 7 zero-loss partition remains **174 + 16 + 25 = 215**.

## F6 validation state

Unit 7 F6 validated all **55 production scenes** and **18 hidden recall states** through the production rendering functions. Responsive contracts were checked against desktop, tablet, and phone targets, producing **165 scene/viewport** and **54 recall/viewport** checks. Review scheduling, the five-item visible cap, 48-hour mixed discrimination delay, unit isolation, refresh/resume persistence, Units 1–7 switching, all 16 Challenge Lab tasks, speech preparation, and live HTTP/API behavior passed.

Chromium timed out during an 8-second headless `about:blank` probe without DOM output. The release therefore makes no screenshot-level or pixel-level validation claim.

## Machine validation

- Unit 7 F1–F6 historical/current gates **PASS**
- Units 1–7 mainline gate **PASS**
- Python tests **372 / 372 PASS**
- Unit 3–7 UI-logic gates **PASS**
- JavaScript syntax **PASS**
- Python compilation **PASS**
- live HTTP/API **PASS**
- deterministic F6 rebuild **9 artifacts checked, 0 changed**
- Unit 7 F5 runtime curriculum and six frozen narratives **byte-preserved**

The machine-readable manifest is `content/ap-biology/mainline-release-u1-u7.json`.

## Next curriculum stage

Begin Unit 8 source inventory and scientific locking from this frozen Units 1–7 F6 baseline.
