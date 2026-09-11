# Unit 8 F4E Integration Audit

## Baseline

F4E was built directly from `MemoryPalace_V2_Mainline_Units1-7_Unit8-F4D.zip` with SHA-256 `d0ca1e064b1cd8a5adb02ac10259efc0cf3a988a4cf474a4eba4466b1baa1e61`.

## Protected upstream content

- Units 1–7 content files identical **421 / 421**
- Backend/frontend runtime source files identical **15 / 15**
- F4A locked files identical **7 / 7**
- F4B locked files identical **7 / 7**
- F4C locked files identical **7 / 7**
- F4D locked files identical **7 / 7**
- Removed baseline files **0**

## Expected compatibility updates

The current Unit 8 status moved from F4D to F4E, so `content/ap-biology/course.json` and `content/ap-biology/unit-8/status.json` changed. No prior narrative QA script or browser-facing test required widening because the F4D compatibility checks already accept later F4 developer-preview states while continuing to verify the immutable F4D lock.

Changed baseline files

- `content/ap-biology/course.json`
- `content/ap-biology/unit-8/status.json`

New F4E files were added for the Journey 5 narrative, lock, manifests, build and QA scripts, tests, and release documentation. No source PDF is included in the repository package.

## Runtime boundary

Unit 8 remains a developer preview. Student-facing journey endpoints still return no Unit 8 guided journeys, no Unit 8 journey artifact is exposed through the learner runtime, and the Unit 8 application lab remains at zero live Challenge Lab tasks. The public learner runtime remains `v2-apbio-0.28.0-u7-f6`.
