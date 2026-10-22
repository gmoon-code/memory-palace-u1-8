# Story Method narrative editor foundation

This is a **browser-local narrative authoring tool** for the frozen AP Biology Story Method curriculum. Its standalone HTML, CSS and JavaScript are included in the GitHub Pages build. The public editor bookmark is `https://gmoon-code.github.io/memory-palace-u1-8/editor.html`, which opens the narrative authoring surface at `/authoring/visual-editor.html`. The student navigation and student runtime are unchanged.

GitHub Pages hosts the editor's files publicly, as it does with other static pages. Anyone with the editor URL could open the **local editor interface**, but it does not grant any permission to change the published curriculum or write to GitHub. The editor stores drafts in its own browser storage and only exports a JSON proposal. Real publication requires a separate authorised workflow. A `noindex` tag is not authentication.

## Run locally

Serve the repository root using a local static server and open `/authoring/visual-editor.html`. The editor loads the released course registry, the eight unit journey registries, and the original journey JSON files. It does not read or change learner progress.

## Current capabilities

- Select an AP Biology unit, journey, and scene.
- Search scene titles, kickers, descriptions, and existing narrative paragraphs across the current journey. Each result links directly to its editable field without changing any curriculum data.
- Click scene titles, kickers, location descriptions, or narrative paragraphs to edit them directly.
- Read narrative text with the same bold scientific-term emphasis used in the student interface. While editing, the inspector and selected paragraph expose the original `**term**` Markdown, which is preserved in JSON export.
- Use the inspector for longer edits.
- Preview the scene at desktop or mobile width.
- Save local drafts in browser storage, undo and redo narrative edits, reset, revert a field, and review before-and-after text. New edits clear the redo history; changing journeys also clears the transient undo and redo stacks.
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

`node tests/story-visual-editor-smoke.mjs` runs a Chromium smoke test against a locally served repository. It edits genuine Unit 1 and Unit 2 journeys, checks local drafts and JSON export, and compares protected structures against the released content. GitHub Actions tests both the repository editor and the **complete prospective GitHub Pages build artifact**, including `scripts/qa_github_pages_static.mjs`. This verifies the intended public Pages path before any deployment.

The previous course's full QA suite remains authoritative for any curriculum release. This isolated editor test does not replace frozen scientific-content checks.

## Limitations and next milestones

This is an authoring foundation, not a complete Squarespace-style editor. Images, scene geometry, story actors, scientific statements, scene ordering, and review/Challenge Lab content are not editable here yet.

An eventual approved publishing workflow needs a separate private authentication and review boundary and must run the full frozen curriculum QA before updating the public student site. The portfolio's HTML page publisher must not be reused to write arbitrary Story Method JSON.

Do not add secrets, publishing tokens, or privileged API endpoints to the public student site.
