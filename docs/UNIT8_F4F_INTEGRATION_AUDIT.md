# Unit 8 F4F Integration Audit

## Baseline

F4F was built directly from `MemoryPalace_V2_Mainline_Units1-7_Unit8-F4E.zip` with SHA-256 `606e8667336f7e9947daad8f41506a52d4abc8c2e9ae5b731bf0332548079a41`.

## Protected upstream content

- Units 1–7 content files identical **421 / 421**
- Backend/frontend runtime source files identical **15 / 15**
- F4A locked files identical **7 / 7**
- F4B locked files identical **7 / 7**
- F4C locked files identical **7 / 7**
- F4D locked files identical **7 / 7**
- F4E locked files identical **7 / 7**
- Removed baseline files **0**

## Expected compatibility updates

The current Unit 8 status moved from F4E to F4F, so `content/ap-biology/course.json` and `content/ap-biology/unit-8/status.json` changed. The F4E QA script was widened to accept later F4 developer-preview states while still verifying all F4E locked artifacts and the zero-runtime-content boundary. The F4E content lock itself remains byte-for-byte valid.

Changed baseline files

- `content/ap-biology/course.json`
- `content/ap-biology/unit-8/status.json`
- `scripts/qa_unit8_f4e.py`

New F4F files were added for the Journey 6 narrative source, journey artifact, cumulative journey index, lock, status, manifests, build and QA scripts, regression tests, and release documentation. No source PDF is included in the repository package.

## Runtime boundary

Unit 8 remains a developer preview. Student-facing journey endpoints still return no Unit 8 guided journeys, no Unit 8 journey artifact is exposed through the learner runtime, and the Unit 8 application lab remains at zero live Challenge Lab tasks. The public learner runtime remains `v2-apbio-0.28.0-u7-f6`.
