# Start Here · AP Biology Units 1–8 · Site UX1

This repository is the complete `memory-palace-v2` AP Biology course with the post-F6 **Site UX1** student-interface hardening release.

## Frozen curriculum runtime

```text
v2-apbio-0.30.0-u8-f6
```

The student-shell revision is `site-ux1`. The curriculum and the interface revision remain separate. Site UX1 changes navigation, state handling, accessibility, error recovery, HTTP behavior, and release engineering while preserving all frozen AP Biology scientific and narrative content.

## Live website

Students can use the released course at

**https://gmoon-code.github.io/memory-palace-u1-8/**

The production site is hosted entirely through GitHub Pages. It does not depend on Vercel or another application host. The browser reads the frozen curriculum JSON directly from the deployed site, while progress and Review state remain in browser `localStorage`.

FastAPI remains available for local development and parity testing. It is not required by the GitHub Pages production site.

## Course accounting

- **1,561** canonical records across Units 1–8
- **58** guided journeys
- **448** permanent scenes or loci
- **112** Challenge Lab items
- **152** intentional Quick Recall checkpoints
- **887** exact-name Review targets
- **220** mixed-discrimination sets
- **600** mixed-discrimination questions

The machine-readable curriculum manifest is `content/ap-biology/mainline-release-u1-u8.json`. The machine-readable Site UX1 lock is `site-release/site-ux1-lock.json`.

## What students see

The main navigation is **Home · Learn · Review**.

Home shows the current unit, the next useful journey, unit progress, locations already visited, Review due count, the journey library, Challenge Lab, and a collapsible map of all eight units. Learn shows the physical scene layout, scientific actors, narrative, route progress, optional memory anchors, audio controls, previous-scene navigation, and previously visited route locations. Review uses delayed retrieval and mixed discrimination. Challenge Lab keeps application work separate from the permanent story route.

First-run routing begins in Unit 1. Completed journeys point toward the next incomplete journey. Previously visited locations can be reopened. Unit switching and refresh/resume behavior preserve meaningful progress. Invalid saved state and unavailable browser storage recover safely.

Quick Recall keeps assisted attempts honest. If a hint is used, the attempt remains marked as assisted across a short reload or unit detour and cannot immediately be reclassified as an unassisted success. The marker expires after two hours or clears when the learner moves forward from that scene.

## How production deployment works

`scripts/build_github_pages.py` creates the production artifact outside the repository tree. It copies only the student runtime shell and the exact released curriculum files needed by the static data adapter.

`scripts/qa_github_pages_static.mjs` loads that staged artifact through the same static adapter used by GitHub Pages. It verifies all 8 units, 58 journeys, 448 scenes, 152 Quick Recalls, 112 Challenge Lab items, 887 Review targets, 220 mixed sets, 600 mixed questions, and every story/checkpoint Memory Object referenced by the journeys.

The main QA workflow builds the Pages artifact twice and requires the two directory trees to be identical. It also preserves the historical curriculum QA chain, current whole-site UX validation, Python tests, JavaScript syntax checks, Python compilation, deterministic source packaging, and final repository-drift detection.

The deployment workflow in `.github/workflows/pages.yml` is gated by that QA result. A deployment occurs only when **Memory Palace QA** succeeds on `main`. The deployment job checks out the exact validated commit, rebuilds and revalidates the artifact, and then publishes it with GitHub Pages.

## Run the website locally with FastAPI

```bash
pip install -r requirements.txt
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Open `http://localhost:8000`.

## Build the production static artifact locally

```bash
python scripts/build_github_pages.py --output /tmp/memory-palace-pages
PAGES_SITE_ROOT=/tmp/memory-palace-pages node scripts/qa_github_pages_static.mjs
```

## Run the Site UX1 gates

```bash
python scripts/build_site_ux1.py
node scripts/qa_site_ux.mjs
python scripts/qa_site_contrast.py
python scripts/qa_site_http_live.py
python -m pytest -q
```

The contrast gate verifies the important normal-sized text and control combinations against a minimum 4.5 to 1 contrast ratio. The lowest audited normal-text combination in the release is 5.21 to 1. The shell also checks keyboard focus, skip navigation, 44-pixel minimum controls, reduced motion, progress semantics, named buttons, duplicate IDs, dynamic-content escaping, loading states, and error recovery.

Chromium navigation was blocked by the sandbox used for the historical Site UX1 release validation. That release therefore does **not** claim screenshot-level or pixel-level browser validation.

## Build the source release archive

```bash
python scripts/build_site_ux1_release.py --output MemoryPalace_V2_Mainline_Units1-8_Site-UX1.zip
```

Detailed release records remain in

- `docs/SITE_UX1_RELEASE.md`
- `docs/SITE_UX1_AUDIT.md`
- `docs/SITE_UX1_QA.md`
- `docs/SITE_UX1_PACKAGE_QA.md`

## Frozen boundary

The AP Biology curriculum remains frozen at Unit 8 F6. Site UX1 remains the hardened shell layered over that curriculum. The GitHub Pages adaptation changes hosting and runtime data delivery without changing the curriculum. Do not rerun historical F6 builders as part of ordinary validation. Use their QA gates to verify the frozen release, and create a new named site revision for future interface changes.
