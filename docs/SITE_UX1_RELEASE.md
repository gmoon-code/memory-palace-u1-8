# Site UX1 Release

## Release status

Site UX1 is the post-F6 student-shell hardening release for the completed AP Biology Memory Palace V2 course. The curriculum runtime remains frozen at `v2-apbio-0.30.0-u8-f6`. The site revision is `site-ux1`.

No frozen AP Biology curriculum content is changed by this release. The protected `content` tree contains 527 files and has deterministic tree SHA-256 `6ae355ca5ef69cbef7f3fc539c66b1ead8120efbf001ebb268e0919bd4235ec2`.

## Course surface covered

The release validates all 8 units, 58 guided journeys, 448 permanent scenes, 152 intentional Quick Recall states, 112 Challenge Lab items, 887 exact-name Review targets, 220 mixed-discrimination sets, and 600 mixed questions.

## Student experience changes

Site UX1 fixes first-run routing, backward scene navigation, visited-route reopening, next-incomplete-journey selection, meaningful unit resume behavior, scroll and focus restoration, Quick Recall assistance tracking, Review hint sequencing, Challenge Lab completion behavior, local-state recovery, application error recovery, dynamic-content escaping, and responsive navigation behavior.

Home now emphasizes student progress and the course route. Learn preserves the physical scene, route position, previous-scene access, and previously visited locations. Review presents one retrieval decision at a time and separates hints from answers. Challenge Lab provides previous-task navigation and a clear final completion action.

## Accessibility and resilience

The hardened shell includes skip navigation, keyboard-visible focus, a focusable main region, accessible progress semantics, live feedback regions, named controls, 44-pixel minimum targets, reduced-motion handling, responsive mobile layouts, and contrast-safe normal text.

Saved state uses schema version 4 with migration and normalization. Malformed saved values, invalid unit identifiers, unavailable browser storage, invalid scene indexes, and failed storage writes recover without exposing developer instructions to students.

## Server and API hardening

The FastAPI application adds GZip, strict API 404 behavior, protected SPA/static path resolution, explicit cache policy, Content Security Policy, `nosniff`, frame denial, no-referrer behavior, permissions restrictions, and same-origin opener/resource policies. Public Swagger, ReDoc, and OpenAPI routes are disabled.

## Validation boundary

Chromium navigation cannot complete inside the release sandbox, including a direct local `about:blank`/local-server headless probe. Site UX1 therefore makes no screenshot-level or pixel-level browser claim. Production render functions, complete course-state rendering, interaction/state contracts, responsive CSS contracts, accessibility semantics, static contrast, JavaScript syntax, Python behavior, and live Uvicorn HTTP/API behavior are validated directly.

## Release boundary

Site UX1 is layered over the frozen Units 1–8 F6 curriculum. Future science or curriculum work must begin from the frozen curriculum boundary. Future interface work should use a new named site revision and preserve this release lock.
