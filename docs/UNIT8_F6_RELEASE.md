# Unit 8 F6 Release

Unit 8 · Ecology has completed the final F6 functional browser-facing and classroom validation gate. F6 changes no Unit 8 canonical science, F2 architecture, F3 scene briefs, F4A–F4H narrative bytes, F5 Memory Objects, Review targets, mixed-discrimination content, Challenge Lab science, or scope guards.

## Final Unit 8 state

- canonical records **255 / 255 accounted**
- runtime Memory Objects **211**
- Challenge Lab application records **13**
- non-runtime scope guards **31**
- guided journeys **8**
- permanent scenes/loci **58**
- optional first-exposure Quick Recalls **18**
- exact-name delayed Review targets **135**
- meaning/mechanism-only palace records **76**
- mixed-discrimination sets **40**
- mixed-discrimination questions **104**
- mandatory spelling gates **0**
- student release remains enabled

The zero-loss partition remains **211 story/runtime records + 13 Challenge Lab records + 31 scope guards = 255 canonical records**.

## F6 browser-facing validation

The production rendering functions were exercised for all **58 Unit 8 scenes** and all **18 hidden Quick Recall states**. Responsive CSS contracts were checked against **1440×1000 desktop, 820×1180 tablet, and 390×844 phone** targets, producing **174 scene/viewport** and **54 recall/viewport** checks.

State-machine validation covers refresh/resume persistence, switching among released Units 1–8, all 135 delayed exact-name targets, all 40 mixed-discrimination sets and their 48-hour eligibility delay, the five-item visible Review limit, and all 13 Challenge Lab tasks.

A live Uvicorn server was also exercised through HTTP. Health, Unit 8 summary, journey registry, each of the eight individual journeys, Challenge Lab, Review manifest, mixed-discrimination data, scope guards, and finalization all returned HTTP 200. The health endpoint reported `v2-apbio-0.30.0-u8-f6`.

## Browser rendering limitation

Chromium was directly probed with a **12-second headless `about:blank` render** and timed out without DOM output in this sandbox. This release therefore does **not** claim screenshot-level or pixel-level browser validation. The F6 gate uses the production JavaScript rendering functions, state-machine interaction tests, responsive CSS contract checks, and live HTTP/API behavior.

## F6 runtime correction

Browser speech-only normalization now covers common Unit 8 ecological notation including **NPP, GPP, dN/dt, rmax, N₂, NH₄⁺, NO₃⁻, and `1 − Σ(n/N)²`**. Unicode minus, sigma, and equals are also prepared for speech. Visible scientific text and all eight narrative files remain unchanged.

## Historical-gate compatibility

The final F6 runtime legitimately changes `backend/main.py` and `frontend/js/audio.js` relative to the frozen F5 runtime lock. Historical Unit 4–7 F6 gates and Unit 8 F3–F5 gates were updated only so they can recognize the exact later Unit 8 F6 runtime/status when the appropriate later content lock is present. Their original scientific, narrative, architecture, and curriculum hash checks remain in force.

The GitHub Actions workflow no longer rebuilds Unit 8 F5 after the F6 release. It validates the frozen F5 artifacts, then executes the deterministic F6 builder and F6 gates so the final repository returns to the committed F6 state before the cleanliness check.

## Regression

- Unit 1 full QA **PASS**
- Unit 2 F5 **PASS**
- Units 3–7 F6 **PASS**
- Unit 8 F3 through F6 **PASS**
- Units 1–8 mainline **PASS**
- Unit 3 through Unit 8 UI-logic QA **PASS**
- Python tests **433 / 433 PASS**
- JavaScript syntax **PASS**
- Python compilation **PASS**
- live Uvicorn HTTP/API **PASS**
- deterministic Unit 8 F6 rebuild **9 artifacts checked / 0 changes**

## Runtime

```text
v2-apbio-0.30.0-u8-f6
```

## Release decision

**PASS. Unit 8 remains student-ready and has completed the final F6 functional browser-facing/classroom validation gate. AP Biology Units 1–8 are complete at the current release standard.**
