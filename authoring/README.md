# Story Method narrative editor foundation

This is a **local-first development authoring tool** for the frozen AP Biology Story Method curriculum. It is not part of the public student experience and is intentionally excluded from `scripts/build_github_pages.py`.

## Run locally

Serve the repository root using a local static server and open `/authoring/visual-editor.html`. The editor loads the released course registry, the eight unit journey registries, and the original journey JSON files. It does not read or change learner progress.

## Current capabilities

- Select an AP Biology unit, journey, and scene.
- Click scene titles, kickers, location descriptions, or narrative paragraphs to edit them directly.
- Use the inspector for longer edits.
- Preview the scene at desktop or mobile width.
- Save local drafts in browser storage, undo, reset, revert a field, and review before-and-after text.
- Export a complete journey JSON with stable indentation that matches the repository's source format.

**No edit is sent to the public site or GitHub.** JSON files must be reviewed, checked for scientific accuracy, and validated through the existing frozen-curriculum QA chain before any release.

## Protected records

The editor validates the complete journey against its original file. The following are preserved exactly

- palace, journey, scene, and route identities
- scene counts, ordering, locations, route geometry, and scene layouts
- canonical scientific statements and memory object references
- checkpoints, answers, hints, review targets, and misconception guards
- guided narrative metadata outside the selected scene fields

The only editable scene fields in the first release are `title`, `scene_kicker`, `location_description`, and the existing elements of `story_paragraphs`. When `story_open` or `story_close` originally duplicated the first or last paragraph, the editor keeps the duplicate synchronized. Where those fields originally differ, they remain protected.

The number and order of narrative paragraphs cannot be changed. Editing them does not update canonical definitions, challenge items, or review records.

## Testing

`node tests/story-visual-editor-smoke.mjs` runs a Chromium smoke test against a locally served repository. It edits genuine Unit 1 and Unit 2 journeys, checks local drafts and JSON export, and compares protected structures against the released content. GitHub Actions runs this test on the draft pull request.

The previous course's full QA suite remains authoritative for any curriculum release. This isolated editor test does not replace frozen scientific-content checks.

## Limitations and next milestones

This is an authoring foundation, not a complete Squarespace-style editor. Images, scene geometry, story actors, scientific statements, scene ordering, and review/Challenge Lab content are not editable here yet.

An eventual approved publishing workflow needs a separate private authentication and review boundary and must run the full frozen curriculum QA before updating the public student site. The portfolio's HTML page publisher must not be reused to write arbitrary Story Method JSON.

Do not add secrets, publishing tokens, or privileged API endpoints to the public student site.
