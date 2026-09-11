# Site UX1 Whole-Site Audit

## Audit scope

The audit treats the website as a first-time student experience and as a production application. It covers navigation, information hierarchy, progress awareness, recovery, retrieval integrity, accessibility, responsive behavior, content rendering, network behavior, security headers, release reproducibility, and frozen-curriculum protection.

## Navigation and orientation

Fresh learners begin in Unit 1 without an arbitrary preselected journey. Home and the global Learn action use the same next-useful-journey rule. Completed journeys lead toward the next unfinished journey. Unit switching attempts to restore meaningful in-progress work. Learn provides a previous-scene control and allows visited route locations to be reopened while future locations remain unavailable.

Every view restores main-content focus after a major transition and scrolls the active work back into view. The route communicates current and visited state through both visible treatment and semantic state.

## Retrieval integrity

Quick Recall separates a hint from the answer. Hint use marks the attempt as assisted, and that assistance state survives a short reload or unit detour for up to two hours. Assisted retrieval cannot be counted immediately as unassisted success. Explicitly skipping a recall schedules it as unsuccessful.

Exact-name Review follows the same hint-before-answer principle. Its text box is identified as an optional retrieval note and is not presented as automatic semantic grading. Mixed discrimination retains the minimum 48-hour delay and per-unit isolation. Review delivery remains capped at five items per session.

## Challenge Lab

Challenge Lab presents one application task at a time, provides previous-task navigation, keeps hint and answer regions separate, and finishes to Home at the end rather than looping unexpectedly to the first item.

## State and recovery

Saved state is normalized before use. The shell recovers from malformed JSON, malformed arrays or maps, negative scene positions, invalid unit identifiers, missing saved journeys, unavailable localStorage, and failed writes. Invalid query parameters fall back to a valid released unit. Startup or data errors render a student-readable recovery screen with Retry and Home actions.

## Accessibility and responsive design

The shell includes a skip-to-content link, visible keyboard focus, semantic primary navigation, a focusable main target, accessible progress bars, live feedback regions, descriptive labels, disabled-state treatment, reduced-motion support, responsive stacking, and minimum 44-pixel interactive targets.

A targeted static contrast audit checks the normal-size text and control combinations used by the hardened shell. The lowest audited ratio is 5.21 to 1, above the 4.5 to 1 target.

## Content safety and rendering

Dynamic route labels, titles, stories, cast text, scientific notation, hints, answers, Review material, mixed questions, and Challenge Lab content are escaped before insertion into HTML. The global renderer additionally injects hostile angle-bracket content to verify escaping behavior.

All released course states are exercised by the global UI gate. This includes 8 units, 58 journeys, 448 scenes, 152 Quick Recall states, 112 Challenge Lab items, 887 exact-name Review targets, 220 mixed sets, and 600 mixed questions.

## Network and server behavior

The live HTTP audit starts a real Uvicorn process and reaches every released unit and journey. It checks static delivery, GZip, security headers, same-origin policies, cache behavior, disabled developer documentation, JSON API 404 semantics, SPA deep-link fallback, and path-traversal protection.

## Known validation limitation

The release environment prevents Chromium from completing local headless navigation. The audit therefore does not claim visual screenshot or pixel comparison coverage. This limitation is recorded in the machine-readable site lock.
