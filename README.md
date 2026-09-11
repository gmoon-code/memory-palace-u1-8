# Memory Palace V2 · AP Biology

## Complete Units 1–8 with Site UX1 hardening

This repository contains the completed AP Biology Memory Palace V2 course for **Units 1–8**. The curriculum remains frozen at the Unit 8 F6 runtime below.

```text
v2-apbio-0.30.0-u8-f6
```

The current interface revision is **Site UX1** with machine-readable identifier `site-ux1`. Site UX1 hardens the student experience while preserving canonical science, palace architecture, scene briefs, narrative prose, Memory Objects, Review targets, mixed-discrimination content, Challenge Lab science, and scope guards.

The complete course contains **1,561 canonical records, 58 guided journeys, 448 permanent scenes or loci, and 112 Challenge Lab items**. The frozen curriculum history remains documented in `docs/MAINLINE_RELEASE_U1_U8.md`. The post-F6 interface release is documented in `docs/SITE_UX1_RELEASE.md`.

## Live student site

The production student site is deployed directly through GitHub Pages.

**https://gmoon-code.github.io/memory-palace-u1-8/**

Production is intentionally static. Curriculum data is loaded from the frozen JSON artifacts already stored in this repository, while student progress, Review scheduling, completed scenes, and assisted-recall state remain in browser `localStorage`. The production site therefore does not require Vercel, a Python server, a database, or API secrets.

FastAPI remains in the repository as the local development and parity-test server. The same interface can still be run locally against the original `/api/...` routes.

## Student experience

The primary student navigation is **Home · Learn · Review**. Challenge Lab is available from Home for every released unit that includes application tasks.

Home keeps the learner's current unit, journey progress, locations visited, Review due count, journey library, and full eight-unit course map available without crowding the main work area. Learn keeps the current physical location, stable scene layout, scientific actors, story, optional memory anchors, route progress, previous-scene navigation, and previously visited locations available. Review presents one retrieval decision at a time. Challenge Lab presents one application task at a time.

Site UX1 also protects recovery and retrieval quality. First-time learners begin in Unit 1. Invalid or corrupted saved state is normalized safely. Quick Recall keeps a hint-assisted attempt marked as assisted even after a short reload or unit detour. Review hints reveal the hint before the answer. Challenge Lab keeps story hints and answer guides in separate regions so one cannot erase the other.

Released units can be opened with `?unit=unit-1` through `?unit=unit-8` on the live site.

## GitHub Pages production architecture

The browser selects its data layer from the way `frontend/js/api.js` is served. GitHub Pages loads the module from `frontend/js/`, which activates the static adapter and reads the released JSON artifacts with repository-relative URLs. FastAPI serves the same module from `/static/js/`, which keeps the local server-backed API path active.

`scripts/build_github_pages.py` creates a minimal deployment artifact containing only the student runtime files. It excludes source PDFs, spreadsheets, documentation, tests, QA scripts, Python source, databases, caches, Git metadata, and other non-runtime material.

`scripts/qa_github_pages_static.mjs` then loads the exact staged Pages artifact and verifies the complete released course through the same static adapter the browser uses. The gate reaches all **8 units, 58 journeys, 448 scenes, 152 intentional Quick Recalls, 112 Challenge Lab items, 887 exact-name Review targets, 220 mixed-discrimination sets, 600 mixed questions, and every story/checkpoint Memory Object referenced by the released journeys**.

The Pages builder runs twice in CI and the two output trees must match exactly.

## QA-gated deployment

`.github/workflows/qa.yml` runs the complete historical and current curriculum QA chain, whole-site UX checks, the exact GitHub Pages artifact test, contrast validation, live FastAPI HTTP validation, Python tests, JavaScript syntax checks, Python compilation, deterministic packaging, and a final `git diff --exit-code` drift check.

`.github/workflows/pages.yml` runs only after **Memory Palace QA** finishes successfully on `main`. It checks out the exact validated commit SHA, rebuilds the minimal static site, validates that exact artifact again, uploads it to GitHub Pages, and deploys it. A failed QA run therefore cannot publish a new production site.

## Accessibility and responsive behavior

The shell includes skip navigation, keyboard-visible focus, a focusable main-content target, accessible progress semantics, live feedback regions, minimum 44-pixel buttons, reduced-motion handling, mobile stacking, readable small-text contrast, and explicit current-route and current-navigation states.

The global production-renderer audit covers all released student states. Chromium navigation is blocked by the original release sandbox, so the historical Site UX1 release does not claim screenshot-level or pixel-level browser validation. Production render functions, state behavior, responsive CSS contracts, semantic markup, contrast, data loading, and live FastAPI HTTP behavior are validated directly.

## Run locally with FastAPI

```bash
pip install -r requirements.txt
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Then open `http://localhost:8000`.

## Build and test the GitHub Pages artifact locally

Build outside the repository tree.

```bash
python scripts/build_github_pages.py --output /tmp/memory-palace-pages
PAGES_SITE_ROOT=/tmp/memory-palace-pages node scripts/qa_github_pages_static.mjs
```

The main Site UX1 gates remain available with

```bash
python scripts/build_site_ux1.py
node scripts/qa_site_ux.mjs
python scripts/qa_site_contrast.py
python scripts/qa_site_http_live.py
python -m pytest -q
```

Build the deterministic GitHub-ready source archive with

```bash
python scripts/build_site_ux1_release.py --output MemoryPalace_V2_Mainline_Units1-8_Site-UX1.zip
```

## Release boundary

**AP Biology Units 1–8 are complete at F6, and the student shell remains Site UX1 over that frozen curriculum.** The GitHub Pages work changes production hosting and data delivery only. Future curriculum work should begin from the frozen F6 content boundary. Future interface work should create a new site revision without silently rewriting the Site UX1 lock.
