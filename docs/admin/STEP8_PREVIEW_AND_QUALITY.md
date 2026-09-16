# Content Studio Step 8

## Student Preview and Content Health

Step 8 adds the inspection layer that sits between protected working-copy editing and the future publication gate.

The published AP Biology files remain authoritative and unchanged. Content Studio can render an active working copy for teacher inspection while the public student site continues to read only the frozen release files.

## Student Preview

The Student Preview workspace can browse current Units 1 through 8 content and active proposals. It supports scenes, journeys, questions, Challenge Lab items, Memory Objects, concepts, and unit records.

For scenes and journeys, Content Studio reuses the real student `learnView` renderer. Quick Recall preview uses the same learner recall renderer. Review and mixed-discrimination questions reuse `reviewView`. Challenge Lab items reuse `practiceView`.

The rendered student view is placed inside a script-disabled iframe. The preview cannot mutate learner progress, local storage, review scheduling, or published content. Teacher-side controls switch scene position, Quick Recall state, Challenge Lab answer visibility, source version, and responsive reference viewport.

Responsive reference sizes are phone 390 × 844, tablet 768 × 1024, laptop 1024 × 768, and desktop 1280 × 900. These are inspection presets and do not replace browser-level accessibility testing.

When a working copy exists, `auto` preview uses it. The teacher can switch to the published baseline for a direct visual comparison. New proposals have no published baseline and remain draft-only.

## Quality model

Step 8 separates findings into three levels.

- Errors are structural or validation failures. They are marked as publication-blocking for the future Step 9 release gate.
- Warnings identify content, coverage, spatial, retrieval, or accessibility risks that require teacher review before publication.
- Advisories are teacher-facing heuristics. They flag possible readability, continuity, screen-density, memory-load, or coverage concerns. Advisories never make the publication decision automatically.

The quality engine evaluates release alignment, unresolved catalog references, editor payload validity, scene story presence, spatial descriptions, scene orientation, cast clarity, story length, paragraph length, sentence density, zone density, cast density, knowledge-reference reduction, journey route integrity, journey scene-index continuity, next-locus continuity, canonical concept coverage, retrieval coverage, Memory Object completeness, assessment links, Challenge Lab prerequisites, and staged-media accessibility metadata.

Readability and density thresholds are deliberately presented as advisories unless a required content field or structural relationship is invalid. Teacher judgment remains authoritative for narrative quality.

## Draft-aware checks

Every active working copy is checked independently from its published baseline. Scene drafts receive an additional coverage comparison. If a working copy removes knowledge references that exist in the published scene, Content Studio raises a warning with the missing references. The draft is preserved and remains editable.

The preview and quality APIs are read-only. They never write to AP Biology source files, never create publication commits, and never change the public Pages artifact.

## Accessibility checks

Staged images are checked for alternative text. Staged audio and video are checked for transcripts. Staged images, video, and documents receive a caption or contextual-description advisory when that field is empty.

Existing public assets remain outside Step 8 metadata mutation. Step 8 reports only evidence available through the current content and media indexes.

## API surface

Protected teacher endpoints are under `/api/admin/quality`.

- `GET /api/admin/quality/devices`
- `GET /api/admin/quality/preview`
- `GET /api/admin/quality/entity`
- `GET /api/admin/quality/report`

All endpoints require an authenticated owner session. There are no Step 8 mutation endpoints.

## Publication boundary

Step 8 does not publish. It does not modify the GitHub Pages builder, AP Biology source files, or the student runtime. GitHub Pages continues to exclude `frontend/admin`.

Step 9 can now build on a complete inspection path

Edit → Save working copy → Preview learner experience → Run Content Health → Review dependencies and changes → Validate publication candidate → Create version → Publish → Roll back if needed.
