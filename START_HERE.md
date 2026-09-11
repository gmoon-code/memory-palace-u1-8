# Start Here · AP Biology Units 1–8 · Site UX1

This package is the complete `memory-palace-v2` AP Biology course with the post-F6 **Site UX1** student-interface hardening release.

## Frozen curriculum runtime

```text
v2-apbio-0.30.0-u8-f6
```

The student-shell revision is `site-ux1`. The curriculum and the interface revision are intentionally separate. Site UX1 changes navigation, state handling, accessibility, error recovery, HTTP behavior, and release engineering while preserving all frozen AP Biology scientific and narrative content.

## Course accounting

- **1,561** canonical records across Units 1–8
- **58** guided journeys
- **448** permanent scenes or loci
- **112** Challenge Lab items
- **152** intentional Quick Recall checkpoints across the complete student course
- **887** exact-name Review targets
- **220** mixed-discrimination sets
- **600** mixed-discrimination questions

The machine-readable curriculum manifest is `content/ap-biology/mainline-release-u1-u8.json`. The machine-readable Site UX1 lock is `site-release/site-ux1-lock.json`.

## What students see

The main navigation is **Home · Learn · Review**.

Home shows the current unit, the next useful journey, unit progress, locations already visited, Review due count, the journey library, Challenge Lab, and a collapsible map of all eight units. Learn shows the physical scene layout, scientific actors, narrative, route progress, optional memory anchors, audio controls, previous-scene navigation, and previously visited route locations. Review uses delayed retrieval and mixed discrimination. Challenge Lab keeps application work separate from the permanent story route.

First-run routing begins in Unit 1. Completed journeys point toward the next incomplete journey. Previously visited locations can be reopened. Unit switching and refresh/resume behavior preserve meaningful progress. Invalid saved state and unavailable browser storage recover safely.

Quick Recall keeps assisted attempts honest. If a hint is used, the attempt remains marked as assisted across a short reload or unit detour and cannot immediately be reclassified as an unassisted success. The marker expires after two hours or clears when the learner moves forward from that scene.

## Whole-site QA

The final global UI gate renders and inspects every student-facing content state in the released course. It covers all 8 units, all 58 journeys, all 448 scenes, all 152 Quick Recall states, all 112 Challenge Lab items, all 887 exact-name Review targets, all 220 mixed sets, and all 600 mixed questions.

The live HTTP gate launches a real Uvicorn process and reaches all released units and journeys through the network layer. It also checks static delivery, GZip, browser-security headers, cache policy, JSON API 404 behavior, SPA fallback, and path-traversal protection.

The contrast gate verifies the important normal-sized text and control combinations against a minimum 4.5 to 1 contrast ratio. The lowest audited normal-text combination in the release is 5.21 to 1. The shell also checks keyboard focus, skip navigation, 44-pixel minimum controls, reduced motion, progress semantics, named buttons, duplicate IDs, dynamic-content escaping, loading states, and error recovery.

Chromium navigation is blocked by the sandbox used for release validation. The package therefore does **not** claim screenshot-level or pixel-level browser validation.

## Run the website

```bash
pip install -r requirements.txt
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Open `http://localhost:8000`.

## Run the final Site UX1 gates

```bash
python scripts/build_site_ux1.py
node scripts/qa_site_ux.mjs
python scripts/qa_site_contrast.py
python scripts/qa_site_http_live.py
python -m pytest -q
```

The complete GitHub workflow in `.github/workflows/qa.yml` additionally reruns the historical curriculum QA chain, Unit 3–8 UI checks, JavaScript syntax validation, Python compilation, deterministic double packaging, and repository-drift detection.

## Build the release archive

```bash
python scripts/build_site_ux1_release.py --output MemoryPalace_V2_Mainline_Units1-8_Site-UX1.zip
```

The package manifest is `docs/SITE_UX1_PACKAGE_MANIFEST.json`. Detailed release records are in

- `docs/SITE_UX1_RELEASE.md`
- `docs/SITE_UX1_AUDIT.md`
- `docs/SITE_UX1_QA.md`
- `docs/SITE_UX1_PACKAGE_QA.md`

## Frozen boundary

The AP Biology curriculum remains frozen at Unit 8 F6. Site UX1 is the current hardened shell layered over that curriculum. Do not rerun historical F6 builders as part of ordinary validation. Use their QA gates to verify the frozen release, and create a new named site revision for future interface changes.
