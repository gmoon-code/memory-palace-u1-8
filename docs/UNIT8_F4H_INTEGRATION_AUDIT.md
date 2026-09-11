# Unit 8 F4H Integration Audit

## Baseline

F4H was built directly from `MemoryPalace_V2_Mainline_Units1-7_Unit8-F4G.zip` with SHA-256 `5f06ae2717b32a0b11fb258d920a8b5f636828e4833a9a06dcb73edd8a705fad`.

## Protected upstream content

- Units 1–7 content files identical **421 / 421**
- Backend/frontend runtime source files identical **15 / 15**
- F4A locked files identical **7 / 7**
- F4B locked files identical **7 / 7**
- F4C locked files identical **7 / 7**
- F4D locked files identical **7 / 7**
- F4E locked files identical **7 / 7**
- F4F locked files identical **7 / 7**
- F4G locked files identical **7 / 7**
- Removed baseline files **0**

## Expected compatibility updates

The current Unit 8 status moved from F4G to F4H, so `content/ap-biology/course.json` and `content/ap-biology/unit-8/status.json` changed. The F4F and F4G QA scripts were widened to accept the later F4H developer-preview state while still verifying their frozen artifacts and zero-runtime-content boundary. The GitHub Actions workflow now runs Unit 8 F4H QA.

Changed baseline files

- `.github/workflows/qa.yml`
- `content/ap-biology/course.json`
- `content/ap-biology/unit-8/status.json`
- `scripts/qa_unit8_f4f.py`
- `scripts/qa_unit8_f4g.py`

New F4H files were added for the Journey 8 narrative source, journey artifact, cumulative eight-journey index, content lock, status, release manifest, build and QA scripts, regression tests, and release documentation. No source PDF is included in the repository package.

## F4 completion boundary

The eight polished journeys now cover **58 / 58 permanent loci** and **211 / 211 palace-managed records**. F4H does not create final Memory Objects or application tasks. The 13 F1/F2 practice-only records remain reserved for the Challenge Lab/application layer, and the 31 scope guards remain non-runtime protections.

## Runtime boundary

Unit 8 remains a developer preview. Student-facing journey endpoints still return no Unit 8 guided journeys, no Unit 8 journey artifact is exposed through the learner runtime, and the Unit 8 application lab remains at zero live Challenge Lab tasks. The public learner runtime remains `v2-apbio-0.28.0-u7-f6`.
