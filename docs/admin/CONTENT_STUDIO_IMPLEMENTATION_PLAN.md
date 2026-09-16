# The Story Method Content Studio

## Step 1 foundation

This branch establishes the isolated Content Studio foundation for the current eight-unit AP Biology release.

The production `main` branch remains unchanged. The foundation starts from production commit `6d561f19a19b07b9a386442d327db3ca12299bef`.

Step 1 adds a teacher-facing admin shell while deliberately withholding every content-writing operation. The shell reads the existing course registry through the current read API and exposes the planned information architecture. The interface is disabled by default and is not copied into the GitHub Pages student deployment.

## Safety rules

1. Student runtime content remains authoritative until a later validated publication workflow replaces it.
2. Admin editing must operate on drafts before publication.
3. No direct browser write to production content files is permitted.
4. Authentication and server-side authorization must exist before any write API is enabled.
5. Every destructive-looking action must preserve recoverability through version history or archive state.
6. Complete story replacement must preserve the old version and validate required scientific coverage before publication.
7. GitHub Pages remains a student-only static artifact.
8. The public student runtime must never depend on admin-only code.

## Planned modules

The permanent navigation reserves these workspaces.

- Dashboard
- Course Map
- Units
- Journeys
- Scenes
- Stories
- Complete Story Replacement
- Concept Library
- Memory Objects
- Question Bank
- Review System
- Challenge Lab
- Media Library
- Student Preview
- Content Health
- Version History
- Import and Export
- Publishing
- Settings

## Editing capabilities

### Course structure

The editor will support adding, renaming, duplicating, moving, archiving, restoring, and validating units, journeys, and scenes. Reordering must preserve stable identifiers unless the teacher explicitly creates a new record.

### Story editing

The story editor will support paragraph editing, insertion, movement, duplication, deletion, focused writing, scene context, linked concepts, linked characters, linked locations, teacher notes, comments, word counts, reading load indicators, continuity checks, and student preview.

### Complete story replacement

Complete replacement is a first-class workflow with four scopes.

- Narrative only
- Narrative plus scene design
- Complete scene replacement
- Complete journey replacement

Before replacement, the system must snapshot the current version and calculate the knowledge, Memory Objects, questions, review targets, characters, locations, and dependencies attached to the existing content. After replacement, the system must show coverage retained, coverage missing, new unmatched terms, removed dependencies, and downstream references that require review.

A replacement cannot publish while required validation errors remain.

### Concept Library

Canonical concepts will track definitions, mechanisms, functions, prerequisites, relationships, misconceptions, confusable terms, source notes, first teaching location, later uses, questions, review targets, and AP framework mapping.

### Memory Objects

The editor will expose canonical term, exact definition, pronunciation, word structure, phonological keyword, mnemonic actor or object, function interaction, palace locus, confusable terms, productive retrieval, spelling retrieval, and application targets without requiring ordinary JSON editing.

### Questions

The Question Bank will support multiple choice, multiple select, true or false, short answer, fill in the blank, matching, ordering, diagram labeling, graph interpretation, data analysis, experimental design, claim-evidence-reasoning, AP-style free response, vocabulary recall, spelling recall, application, misconception checks, and scenario questions.

Each question can track answer choices, correct answer, explanations, distractor reasoning, linked concepts, unit, journey, scene, difficulty, cognitive demand, AP Science Practice, misconception target, media, publication state, and usage locations.

### Review System

Review planning will expose immediate recall, journey review, unit review, delayed retrieval, mixed discrimination, exact-name retrieval, spelling retrieval, and later-unit reactivation on a visible timeline for each concept.

### Challenge Lab

Challenge Lab editing will support instructions, scenarios, background information, datasets, tables, graphs, images, variables, expected reasoning, questions, model answers, scoring guidance, prerequisite concepts, and extension prompts.

### Media and audio

The Media Library will track files, thumbnails, descriptions, alt text, source information, dimensions, size, usage locations, replacement history, and orphan status. Audio records will track duration and whether narration is stale after story text changes.

## Teacher workflow

The Content Studio will support autosaved drafts, publication status, private teacher notes, comments, task markers, recent work, filters, global search, controlled search and replace, bulk actions, duplication, archive and restore, revision history, side-by-side comparison, and release notes.

## Validation and dependency protection

Validation will eventually cover required fields, duplicate identifiers, broken references, invalid routes, missing answers, missing explanations, deleted dependencies, unpublished dependencies, orphan records, possible duplicates, concept coverage gaps, scene overload indicators, accessibility requirements, and media integrity.

Dependency inspection must show every affected scene, Memory Object, question, review target, Challenge Lab item, character, location, and media item before a structural change is published.

## Publication model

The intended publication sequence is

`Edit → Save Draft → Preview → Validate → Review Dependencies → Review Changes → Create Version → Publish`

Publication will generate a human-readable change summary and a recoverable version. GitHub integration will preserve repository history without exposing repository operations to the ordinary teacher interface.

## Step sequence

### Step 1

Foundation shell, isolated branch, disabled-by-default admin route, student deployment separation, course inventory dashboard, permanent module map, and QA guardrails.

### Step 2

Teacher authentication, authorization, protected admin API namespace, session handling, CSRF protection, write-request audit records, and explicit separation between read-only student APIs and admin APIs.

### Step 3

Normalized admin content catalog and dependency index across all eight units. This creates a stable editing layer over the current heterogeneous Unit 1 through Unit 8 files.

### Step 4

Draft store, revision records, autosave, archive state, comparison data, and recoverable snapshots.

### Step 5

Unit, Journey, Scene, Story, Character, Location, Concept, and Memory Object editors.

### Step 6

Complete Story Replacement with required-knowledge preservation and dependency review.

### Step 7

Question Bank, Review System, Challenge Lab, media, audio, import, export, search, filters, and bulk editing.

### Step 8

Student preview, device preview, content health, accessibility checks, continuity checks, reading-load indicators, and curriculum coverage views.

### Step 9

Validated publication, version creation, release summaries, GitHub-backed publication candidates, rollback, and full regression QA.

## Step 1 acceptance criteria

Step 1 is complete only when all of the following are true.

- `main` still points to the frozen production commit.
- The admin work exists only on an isolated branch.
- `/admin` returns 404 unless explicitly enabled.
- Enabling the admin shell exposes only read functionality.
- No write endpoint is present.
- GitHub Pages build logic still excludes the admin directory.
- The student runtime files and course content files remain unchanged.
- The admin shell can read the eight-unit course registry and display unit, journey, scene, canonical-record, and application-challenge totals.
- The full planned module map is visible in the admin navigation.
- Complete Story Replacement is represented as a dedicated module.
- CI validates the admin foundation and JavaScript syntax.
