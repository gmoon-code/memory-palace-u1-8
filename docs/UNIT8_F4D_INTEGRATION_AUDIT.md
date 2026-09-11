# Unit 8 F4D Integration Audit

## Baseline

F4D was built directly from `MemoryPalace_V2_Mainline_Units1-7_Unit8-F4C.zip` with SHA-256 `6a4e40124e5efadab51ddee109416667654f0c79e045ca9bfab3c25f604cb98f`.

## Protected upstream content

- Units 1–7 content files identical **421 / 421**
- Backend/frontend runtime source files identical **15 / 15**
- F4A locked files identical **7 / 7**
- F4B locked files identical **7 / 7**
- F4C locked files identical **7 / 7**
- Removed baseline files **0**

## Expected compatibility updates

The current Unit 8 status moved from F4C to F4D, so `content/ap-biology/course.json` and `content/ap-biology/unit-8/status.json` changed. The F4C QA script and F4C browser-facing test were widened to accept later F4 developer-preview stages while continuing to verify the immutable F4C lock. No F4C locked narrative artifact changed.

Changed baseline files

- `content/ap-biology/course.json`
- `content/ap-biology/unit-8/status.json`
- `scripts/qa_unit8_f4c.py`
- `tests/test_unit8_f4c.py`


New F4D files were added for the Journey 4 narrative, lock, manifests, tests, QA, and release documentation. No source PDF is included in the repository package.

## Runtime boundary

Unit 8 remains a developer preview. Student-facing journey endpoints still return no Unit 8 guided journeys, no Unit 8 journey artifact is exposed through the student runtime, and the Unit 8 application lab remains at zero live Challenge Lab tasks. The public learner runtime remains `v2-apbio-0.28.0-u7-f6`.
