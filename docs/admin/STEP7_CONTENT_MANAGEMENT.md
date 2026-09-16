# Content Studio Step 7

## Content management expansion

Step 7 extends the protected Content Studio beyond narrative editing. It adds assessment management, review planning, Challenge Lab management, private media staging, portable import and export, workspace search, and controlled bulk text replacement.

The student runtime remains locked. Step 7 does not publish, rewrite, or delete any file under `content/ap-biology` or the public student frontend.

## Question Bank

The Question Bank presents Quick Recall, delayed review, mixed-discrimination questions, mixed-discrimination sets, active working copies, and teacher-created proposals through one interface.

Existing assessment records are source-enriched before a working copy is created. Their complete prompt, choices, answer, explanation, knowledge references, and timing fields remain available when the source file contains them.

Teachers can create new questions and question sets. New records receive a `new:` proposal ID and live only in the protected draft database. They are deliberately absent from the normalized published catalog until a later publication workflow accepts them.

Question changes support autosave, explicit save, optimistic concurrency protection, named snapshots, and the revision history already introduced in Step 4.

## Review System

The Review System assembles current retrieval records into four instructional phases.

- Immediate retrieval contains scene Quick Recall events.
- Delayed retrieval contains review-manifest prompts and their configured review windows.
- Discrimination contains mixed-discrimination sets and their initial delays.
- Application contains Challenge Lab items.

The view also identifies explicitly taught scene object IDs that have no indexed later assessment or application event. This is a coverage signal for teacher inspection. It does not claim that an unlinked concept is pedagogically deficient, since some retrieval can be embedded in narrative or activities that are not represented by the current structured records.

## Challenge Lab

Existing Challenge Lab items can be opened as protected working copies. The editor exposes title, domain, challenge type, prompt, answer guide, knowledge references, prerequisite loci, prerequisite scene titles, and source-assessment metadata.

Teachers can also create new Challenge Lab proposals. Like new Question Bank items, these remain draft-only until the future publication stage.

## Media and audio staging

The Media Library has two distinct inventories.

The published inventory is read-only and scans recognized image, audio, video, and PDF files already present in the repository. The staged inventory stores new teacher uploads under private `server_data` paths that are excluded from Git and the public GitHub Pages build.

Supported staged file types include PNG, JPEG, WebP, GIF, MP3, WAV, OGG, M4A, MP4, WebM, and PDF. Step 7 applies extension checks, browser MIME checks, basic file-signature validation, a 25 MB per-file limit, SHA-256 hashing, exclusive file creation, and safe server-side path resolution.

Staged assets can carry alt text or an accessibility description, a caption, a transcript or narration text, an optional unit association, and an optional Content Studio entity association. Metadata writes use optimistic version checks. Assets can be archived and restored without destructive deletion.

Staging an asset never places it in the student frontend and never makes it public.

## Portable import and export

Content Studio can export selected editable curriculum records as a JSON bundle using schema `story-method-content-studio-portable-1.0`.

The export contains curriculum payloads, record identities, source state, draft versions, scope metadata, and a SHA-256 fingerprint over the exported records. Authentication credentials, session tokens, CSRF tokens, security audit records, and server databases are outside the export model.

Imports require the same portable schema. Before any change is made, the server validates record count, entity type, unit, envelope-to-payload identity, current catalog membership or valid `new:` proposal identity, and active-draft conflicts. Invalid bundles cannot be applied.

Valid imports create or update protected working copies only. The teacher can skip active-draft conflicts or explicitly replace an existing draft. A conflicting draft receives a recovery snapshot before replacement.

Step 7 imposes a 500-record limit on a single import operation.

## Global search and controlled replacement

Workspace search covers the normalized published catalog, active working copies, teacher-created proposals, and staged media metadata.

Controlled find and replace is intentionally narrower than ordinary search. The server traverses only an allowlist of human-readable fields such as titles, narrative paragraphs, prompts, answers, explanations, descriptions, teacher notes, and captions. Stable IDs, unit IDs, palace IDs, locus IDs, source paths, and other structural identity fields are never bulk-rewritten.

Every bulk operation has a preview phase. The preview records each affected entity, matching field paths, occurrence count, current source state, and expected draft version. Application is limited to 75 selected records in one operation. If a draft changed after the preview was produced, optimistic concurrency protection blocks the stale write.

Before changing each selected working copy, Step 7 creates a named recovery snapshot. Published source files remain unchanged.

## Security boundary

All Step 7 endpoints live under `/api/admin/management` and require the authenticated owner session from Step 2. Every mutating operation requires the session CSRF token.

The public GitHub Pages build continues to omit `frontend/admin`. The teacher workspace still requires the trusted FastAPI service and remains independent of the static student site.

## Publication boundary

Step 7 does not implement publication. Drafts, proposals, imported records, bulk replacements, and staged media cannot reach students from this stage.

Step 8 adds draft-aware student preview, stronger content-health checks, accessibility review, narrative continuity and readability review, and coverage inspection. Step 9 will add the controlled validation, release-version, publication, rollback, and full regression workflow needed before any approved teacher changes can become student-facing content.
