# Content Studio Step 4 · Draft and Revision Layer

Step 4 introduces the first Content Studio write capability. These writes are limited to a separate server-side draft database. Published AP Biology content files remain locked and unchanged.

## Working-copy model

A draft begins from one normalized Step 3 catalog entity. The draft stores an immutable base payload and fingerprint together with a separate mutable working payload. The catalog entity ID, entity type, and unit identity are protected from mutation inside the working copy.

Only one active draft can exist for the same catalog entity at a time. Archived drafts remain recoverable and do not block a new active working copy.

## Storage boundary

Drafts live in `server_data/content-studio-drafts.sqlite3` by default. The path can be changed with `MEMORY_PALACE_ADMIN_DRAFT_DB`.

The `server_data` directory is already excluded from Git. The draft layer never imports the AP Biology publication directory as a writable destination and never writes JSON, JavaScript, HTML, or other course source files.

No Step 4 endpoint can publish a draft.

## Draft records

Every working copy stores

- draft ID
- normalized catalog entity ID
- entity type
- unit ID
- working title
- active or archived status
- immutable base payload
- immutable base fingerprint
- current working payload
- monotonic draft version
- creation and update timestamps
- creating and updating administrator
- archive timestamp when applicable

## Optimistic concurrency

Every mutation carries the version the editor originally loaded. The server rejects stale writes with HTTP 409 when another save has already advanced that draft.

This prevents two browser tabs or delayed autosave requests from silently overwriting a newer revision.

## Revision history

Each content-changing save creates an immutable revision row. Revision records store the full working payload, fingerprint, action, note, actor, timestamp, and sequential revision number.

Current revision actions include

- created
- saved
- autosaved
- snapshot created
- restored revision
- restored snapshot
- archived
- restored from archive

Restoring a revision never deletes later history. The restored payload becomes a new current revision and records which earlier revision supplied it.

## Snapshots

A named snapshot captures the current working payload together with the current draft version, administrator, timestamp, and fingerprint.

Snapshots are intended for deliberate recovery points before large rewrites, complete story replacements, structural edits, and other high-impact changes.

Restoring a snapshot creates a new revision. It does not rewind or erase history.

## Archive and restore

Content Studio uses archive-first behavior. Archiving a draft disables editing while retaining the entire revision and snapshot history. An archived draft can later be restored to active status when no other active draft exists for the same entity.

Step 4 does not expose permanent deletion.

## Comparisons

The server can compare the current working payload with

- the immutable normalized catalog base
- any stored revision
- any named snapshot

The comparison returns field-level paths and before/current values. This comparison engine will later power story-replacement review, editor change summaries, and pre-publication release review.

## Protected API

All Step 4 routes live under `/api/admin/drafts` and require the Step 2 owner session.

Read operations require authentication. Every mutation also requires the session-specific CSRF token and same-origin validation.

Available operations include draft creation and listing, working-copy save, archive and restore, revision history, revision restoration, named snapshots, snapshot restoration, comparisons, and draft-state summary.

## Autosave

The Step 4 interface demonstrates autosave on the generic working title. Autosave uses the same server-side version check as explicit saves and creates a recoverable revision whenever the payload actually changes.

Invalid or unchanged payloads do not advance the working version.

## Step 4 interface

The Content Studio now includes a Draft Workspace and an active Version History surface.

Teachers can create a working copy from a normalized catalog entity ID, browse active and archived drafts, open a working copy, see its current version, autosave a title change, inspect the structured payload, explicitly save a structured payload, create recovery snapshots, inspect revision history, restore a revision, restore a snapshot, archive or unarchive the draft, and compare the current working copy with its catalog base.

The structured JSON editor is an advanced temporary Step 4 fallback. Step 5 replaces ordinary JSON editing with field-specific Unit, Journey, Scene, Story, Character, Location, Concept, and Memory Object forms.

## Publication boundary

The published student runtime remains the only published state. Step 4 cannot alter it.

A future publishing step must consume validated draft data through a deliberate compile and release transaction. Direct browser writes into publication files remain prohibited.

## Step 4 acceptance criteria

Step 4 is complete when all of the following are true.

- draft writes are stored outside published content files
- draft creation is based on normalized Step 3 catalog entities
- immutable base snapshots and fingerprints are retained
- autosave and explicit save create recoverable revisions
- stale writes are rejected through optimistic concurrency
- named snapshots are available
- revision and snapshot restoration are non-destructive
- archive and restore preserve history
- current-versus-base comparison is available
- all mutations require authenticated CSRF-protected requests
- the admin interface exposes Draft Workspace and Version History
- GitHub Pages continues to exclude all admin assets
- existing Unit 1 through Unit 8 QA remains green
- production `main` remains unchanged

## Boundary for Step 5

Step 5 builds the field-specific editors on top of this draft service. The first editor set covers Units, Journeys, Scenes, Stories, Characters, Locations, Canonical Concepts, and Memory Objects.

Those editors will write only to Step 4 working copies. Published files remain locked until the later validation and publication stages are implemented.
