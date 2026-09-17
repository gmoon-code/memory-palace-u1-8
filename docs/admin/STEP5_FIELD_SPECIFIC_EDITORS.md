# Content Studio Step 5 · Field-Specific Editors

Step 5 turns the protected Content Studio into a practical teacher editing workspace. It builds friendly forms on top of the Step 3 normalized catalog and Step 4 draft and revision system.

Published AP Biology files remain locked. Every edit in this stage is stored in a protected working copy until a later validation and publication stage explicitly compiles approved drafts back into runtime content.

## Editor coverage

Step 5 adds field-specific editors for

- Units
- Journeys
- Scenes
- Stories
- Characters and scene objects
- Locations
- Canonical concepts
- Memory Objects

Stories use the Scene entity as their structural parent. Opening the Stories workspace brings the narrative-story group to the front while preserving the scene location, cast, retrieval target, Memory Object links, and downstream dependency context.

## Source-enriched working copies

The Step 3 catalog intentionally stores a compact normalized representation. That is sufficient for browsing and dependency analysis, but a story editor needs the complete source narrative.

Step 5 therefore adds a source-enriched editor projection. When a teacher opens a scene for editing, the server safely reads the scene's known source JSON and adds the complete narrative fields to the working representation. These include

- `story_paragraphs`
- `story_open`
- `story_beats`
- `story_close`
- full `scene_layout`
- scene `cast`
- continuity object
- Quick Recall fields
- Memory Object or concept IDs attached to the scene

Journey working copies similarly receive their full premise, mission, finale, learner rule, route orientation, guide record, and route metadata. Concepts and Memory Objects receive additional editable scientific, mnemonic, relationship, and retrieval fields when those fields exist in their source records.

The source-enriched representation becomes both the immutable draft base and the initial draft payload. This prevents the full story from appearing as a false addition in the before-and-after comparison.

## Narrative editor

The narrative editor treats paragraphs as ordered objects in the interface while preserving the runtime's ordered list of strings.

A teacher can

- edit individual paragraphs
- add a paragraph
- move a paragraph up or down
- duplicate a paragraph
- delete a paragraph from the draft
- see paragraph, word, and character counts
- edit the scene kicker and continuity object
- edit the next locus transition

Each change is made in the working copy. Autosave creates a recoverable revision through the Step 4 draft system.

## Scene layout and cast

Scene zones and cast records use repeatable structured controls. A teacher can add, remove, and reorder zones or cast entries without editing JSON.

Scene-zone controls expose position, label, symbol, and description. Cast controls expose name, kind, visual description, and the character or object's job in the scene.

Locations have a separate editor for locus title, description, orientation, and zone structure. Characters and recurring scene objects have a separate editor for name, kind, role, visual description, and job.

## Journey editor

Journey editing exposes

- story title
- palace or route name
- tagline
- estimated time
- premise
- mission
- finale
- learner rule
- route orientation
- guide name
- guide role
- guide visual description
- guide story job

Stable identifiers and source paths remain outside the ordinary editable field set.

## Canonical concept editor

The concept editor exposes canonical term, canonical definition, topic, scope class, source reference, scientific lock status, prerequisites, related concepts, misconceptions, and teacher notes.

The Step 3 dependency graph remains available beside these records so later validation can identify scenes, Memory Objects, questions, and Challenge Lab items that depend on a proposed scientific change.

## Memory Object editor

The Memory Object workspace exposes the structured memory model through ordinary fields. Current fields include

- canonical term
- exact definition
- pronunciation
- word structure
- confusable terms
- phonological keyword
- mnemonic actor
- mnemonic object
- function or interaction
- palace zone
- primary palace locus
- productive retrieval target
- exact-name requirement
- exact-spelling requirement
- spelling retrieval target
- application question
- locus ID
- scene index
- source trace
- version status

Fields that do not exist in a legacy source record can be added to the working copy without requiring raw JSON editing.

## Autosave and concurrency

Field editors use the same optimistic concurrency contract as Step 4. Each request includes the draft version that the editor loaded. A stale editor cannot silently overwrite a newer revision.

Text changes autosave after a short idle period. Manual Save remains available. If additional edits occur while a save request is in progress, the later changes remain marked as pending and are saved after the first request completes.

## Recovery snapshots

The field editor includes a named snapshot action. Teachers can create a recovery point immediately before a substantial narrative or structural change. Snapshots and revisions remain available through Draft Workspace and Version History.

## Server-side validation

Friendly editor writes use a dedicated `/api/admin/editors/*` API. Authentication and CSRF protection are required for all mutations.

The server validates the editor payload by entity type before saving. Validation covers expected field types, required text, numeric ranges, booleans, lists, paragraph structure, repeatable structured items, paragraph size limits, and item-count limits.

The advanced Step 4 structured-payload editor remains available for development and recovery work. Ordinary teacher editing now uses the field-specific interface.

## Published-content boundary

Step 5 does not write AP Biology source JSON. The editor reads source files only to prepare a complete working-copy baseline. All mutations are written to the server-side draft database.

This boundary means a teacher can rewrite a scene, alter a character description, change a concept explanation, or modify a Memory Object without changing what students currently see.

## Preparation for complete story replacement

The Complete Story Replacement workflow remains a separate Step 6 feature. Step 5 supplies the editor primitives it needs

- complete source-enriched story payloads
- paragraph-level editing
- scene layout editing
- cast editing
- scientific and Memory Object editing
- dependency context
- autosaved revisions
- recovery snapshots
- typed server-side validation

Step 6 will add replacement scope selection, required-knowledge preservation, old-versus-new coverage analysis, dependency-impact review, and a dedicated replacement transaction.

## Step 5 acceptance criteria

Step 5 is complete when field-specific editors exist for all planned Step 5 entity types, complete scene narratives can be loaded into protected working copies, the story editor provides paragraph-level controls, scene layout and cast can be edited without JSON, Memory Objects expose their structured retrieval and mnemonic fields, editor writes are authenticated and CSRF protected, autosave and snapshots work through Step 4, malformed editor payloads are rejected, published AP Biology source files remain unchanged during editor tests, existing Unit 1 through Unit 8 regression QA remains green, and production `main` remains unchanged.
