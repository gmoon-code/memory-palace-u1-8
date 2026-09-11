# Memory Palace V2 · AP Biology

## Complete Units 1–8 with Site UX1 hardening

This repository contains the completed AP Biology Memory Palace V2 course for **Units 1–8**. The curriculum itself remains frozen at the Unit 8 F6 runtime below.

```text
v2-apbio-0.30.0-u8-f6
```

The current interface revision is **Site UX1** with machine-readable identifier `site-ux1`. Site UX1 hardens the student experience without changing canonical science, palace architecture, scene briefs, narrative prose, Memory Objects, Review targets, mixed-discrimination content, Challenge Lab science, or scope guards.

The complete course contains **1,561 canonical records, 58 guided journeys, 448 permanent scenes or loci, and 112 Challenge Lab items**. The frozen curriculum history remains documented in `docs/MAINLINE_RELEASE_U1_U8.md`. The post-F6 interface release is documented in `docs/SITE_UX1_RELEASE.md`.

## Student experience

The primary student navigation is **Home · Learn · Review**. Challenge Lab is available from Home for every released unit that includes application tasks.

Home keeps the learner's current unit, journey progress, locations visited, Review due count, journey library, and full eight-unit course map available without crowding the main work area. Learn keeps the current physical location, stable scene layout, scientific actors, story, optional memory anchors, route progress, previous-scene navigation, and previously visited locations available. Review presents one retrieval decision at a time. Challenge Lab presents one application task at a time.

Site UX1 also protects recovery and retrieval quality. First-time learners begin in Unit 1. Invalid or corrupted saved state is normalized safely. Quick Recall keeps a hint-assisted attempt marked as assisted even after a short reload or unit detour. Review hints reveal the hint before the answer. Challenge Lab keeps story hints and answer guides in separate regions so one cannot erase the other.

Released units can be opened with `/?unit=unit-1` through `/?unit=unit-8`.

## Accessibility and responsive behavior

The shell includes skip navigation, keyboard-visible focus, a focusable main-content target, accessible progress semantics, live feedback regions, minimum 44-pixel buttons, reduced-motion handling, mobile stacking, readable small-text contrast, and explicit current-route and current-navigation states.

The global production-renderer audit covers **all 8 units, 58 journeys, 448 scenes, 152 intentional Quick Recall states, 112 Challenge Lab items, 887 exact-name Review targets, 220 mixed-discrimination sets, and 600 mixed questions**.

Chromium navigation is blocked by the release sandbox, so screenshot-level and pixel-level browser validation are not claimed. Production render functions, state behavior, responsive CSS contracts, semantic markup, contrast, API behavior, and real Uvicorn HTTP behavior are validated directly.

## Server hardening

The FastAPI shell disables public Swagger, ReDoc, and OpenAPI routes. API responses use explicit JSON 404 behavior. SPA and static path traversal are protected. GZip is enabled. The server adds Content Security Policy, `nosniff`, frame denial, no-referrer, permissions restrictions, same-origin opener/resource policy, and explicit cache behavior for API and static resources.

## Run locally

```bash
pip install -r requirements.txt
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Then open `http://localhost:8000`.

## Final site validation

Run the Site UX1 gates with

```bash
python scripts/build_site_ux1.py
node scripts/qa_site_ux.mjs
python scripts/qa_site_contrast.py
python scripts/qa_site_http_live.py
python -m pytest -q
```

The GitHub Actions workflow also preserves the historical Unit 1–8 QA chain, Unit 3–8 UI-logic checks, JavaScript syntax checks, Python compilation, deterministic double packaging, and a final `git diff --exit-code` repository-drift check. Historical F6 builders are deliberately excluded from routine CI because the F6 curriculum release is frozen.

Build the deterministic GitHub-ready archive with

```bash
python scripts/build_site_ux1_release.py --output MemoryPalace_V2_Mainline_Units1-8_Site-UX1.zip
```

## Release boundary

**AP Biology Units 1–8 are complete at F6, and the student shell is frozen at Site UX1 after whole-course hardening.** Future curriculum work should begin from the frozen F6 content boundary. Future interface work should create a new site revision without silently rewriting the Site UX1 lock.
