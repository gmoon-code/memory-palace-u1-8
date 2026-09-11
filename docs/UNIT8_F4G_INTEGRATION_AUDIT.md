# Unit 8 F4G Integration Audit

## Baseline

F4G was built directly from `MemoryPalace_V2_Mainline_Units1-7_Unit8-F4F.zip` with SHA-256 `9e69addb9e44e6c4eb7dd66a7717a90243ca609585c4c676719e9a2371cfc1e4`.

## Protected upstream content

- Units 1–7 content files identical **421 / 421**
- Backend/frontend runtime source files identical **15 / 15**
- F4A locked files identical **7 / 7**
- F4B locked files identical **7 / 7**
- F4C locked files identical **7 / 7**
- F4D locked files identical **7 / 7**
- F4E locked files identical **7 / 7**
- F4F locked files identical **7 / 7**
- Removed baseline files **0**

## Expected compatibility updates

The current Unit 8 status moved from F4F to F4G, so `content/ap-biology/course.json` and `content/ap-biology/unit-8/status.json` changed. The F4F QA script was widened to accept the later F4G developer-preview state while still verifying every F4F locked artifact and the zero-runtime-content boundary. The GitHub Actions workflow was extended to run Unit 8 F4D through F4G QA as part of continuous integration.

Changed baseline files

- `.github/workflows/qa.yml`
- `content/ap-biology/course.json`
- `content/ap-biology/unit-8/status.json`
- `scripts/qa_unit8_f4f.py`

New F4G files were added for the Journey 7 narrative source, journey artifact, cumulative journey index, content lock, status, release manifest, build and QA scripts, regression tests, and release documentation. No source PDF is included in the repository package.

## Runtime boundary

Unit 8 remains a developer preview. Student-facing journey endpoints still return no Unit 8 guided journeys, no Unit 8 journey artifact is exposed through the learner runtime, and the Unit 8 application lab remains at zero live Challenge Lab tasks. The public learner runtime remains `v2-apbio-0.28.0-u7-f6`.
