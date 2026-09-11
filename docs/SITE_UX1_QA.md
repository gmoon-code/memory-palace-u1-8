# Site UX1 Quality Assurance

## Frozen curriculum guard

Expected content files `527`

Expected content-tree SHA-256 `6ae355ca5ef69cbef7f3fc539c66b1ead8120efbf001ebb268e0919bd4235ec2`

Expected curriculum runtime `v2-apbio-0.30.0-u8-f6`

The Site UX1 builder refuses to proceed when this content boundary changes.

## Global production-renderer QA

`node scripts/qa_site_ux.mjs`

Expected coverage includes all 8 units, 58 journeys, 448 scenes, 152 Quick Recalls, 112 Challenge Lab items, 887 exact-name Review targets, 220 mixed-discrimination sets, and 600 mixed questions. The gate also checks first-run recovery, malformed-state recovery, assisted-recall persistence, route behavior, accessibility contracts, and dynamic-content escaping.

## Contrast QA

`python scripts/qa_site_contrast.py`

The gate checks the hardened shell's principal normal-text and control combinations against a 4.5 to 1 minimum. The lowest currently audited combination is 5.21 to 1.

## Live HTTP QA

`python scripts/qa_site_http_live.py`

The gate starts Uvicorn on a local free port and validates the complete released journey registry through HTTP together with Challenge Lab, GZip, security headers, cache policy, disabled developer docs, API 404 behavior, SPA fallback, and traversal protection.

## Historical and current regression

The GitHub workflow reruns the historical curriculum QA chain without invoking frozen F6 builders. Historical gates are allowed to recognize the Site UX1 runtime hashes only through the valid site release lock. Their original curriculum locks remain authoritative.

The Python test suite includes Site UX1 protection, server behavior, accessibility/navigation source contracts, retrieval-integrity source contracts, and CI policy checks in addition to the existing curriculum suite.

## Syntax and compilation

Every production JavaScript module is checked with Node syntax validation. Backend, scripts, and tests are compiled with Python `compileall`.

## Determinism and drift

The workflow builds the deterministic Site UX1 release ZIP twice and requires byte-for-byte equality. It ends with `git diff --exit-code`, which catches any QA or build command that rewrites a tracked release artifact.

## Browser validation boundary

Real screenshot or pixel-level Chromium validation is not claimed because Chromium navigation cannot complete in this sandbox. Functional render, state, responsive-contract, accessibility, static-contrast, and live-network testing remain required release gates.
