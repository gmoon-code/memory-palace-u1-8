# Content Studio Admin Capability Completion

## Why this pass exists

Content Studio Steps 1 through 9 established the protected catalog, drafts, field editors, complete story replacement, assessment and media management, student preview, quality checks, and controlled publication. The later zero-cost work established local startup, persistent state, backup and restore, and a fail-safe updater.

The original implementation plan also promised broader administrator and teacher workflow abilities. This completion pass reconciles the running interface against that original promise before more operational tooling is added.

Production `main` remains separate. This pass starts from the validated zero-cost updater head `ed456683ea507143b51d8f74be006818295c46cf`.

## First integration correction

The Step 9 publication interface existed as `frontend/admin/publication.js`, but the Content Studio bootstrap did not import that module. The protected publication backend and QA existed while the ordinary admin shell could not activate the Step 9 publication workspace.

This completion branch fixes that integration boundary. `frontend/admin/drafts.js` is now a small bootstrap that loads the unchanged working-copy implementation from `drafts_core.js` and also loads `publication.js`. Publishing and verified release history therefore become part of the same teacher-facing Content Studio runtime as Steps 4 through 8.

## Capability inventory

### Implemented and retained

- teacher authentication, server-side sessions, CSRF protection, login throttling, and security audit records
- normalized eight-unit course catalog and dependency graph
- Course Map, global catalog search, dependency inspection, and release alignment
- protected drafts, autosave, optimistic concurrency, revisions, named snapshots, archive, restore, and comparison
- field-specific Unit, Journey, Scene, Story, Character, Location, Concept, and Memory Object editors
- paragraph-level story editing, scene layout controls, cast controls, source-enriched working copies, and narrative snapshots
- complete story replacement with narrative-only, scene-design, complete-scene, and complete-journey scopes
- required-knowledge inventory, replacement comparison, dependency warnings, and recovery snapshots
- Question Bank management, review planning, Challenge Lab management, private media staging, import/export, workspace search, and controlled bulk text replacement
- draft-aware Student Preview and device preview
- structural, curriculum-coverage, retrieval, continuity, readability, density, and accessibility health checks
- isolated release candidates, validation, GitHub-backed delivery controls, exact-hash verification, immutable releases, and rollback candidates
- local zero-cost startup, persistent private state, backup and restore, Windows launch workflow, and fail-safe local code updater

## Remaining administrator capability gaps

### A. Admin shell integration and truthful status

Every navigation item must resolve to the current working module. No completed capability may remain hidden behind an old placeholder, stale Step label, or obsolete description. Publishing and Version History are the first correction in this pass.

### B. Settings and teacher workflow

The original Settings workspace is still a reserved shell. A real administrator workspace is still needed for safe editor preferences, validation policy, local configuration visibility, and protected operational settings.

Teacher workflow also needs first-class private notes, comments, task markers, review status, recently edited records, and a work queue. Existing entity fields provide some teacher-note support, but they do not yet constitute the promised cross-record workflow system.

### C. Course-structure administration

The original plan promised adding, duplicating, moving, reordering, archiving, restoring, and validating Units, Journeys, and Scenes while preserving stable identifiers. Current field editors primarily edit existing records. Structural create and move operations need a dedicated draft transaction, dependency review, publication compiler support, and rollback coverage.

### D. Assessment, Challenge Lab, and media parity

The current management layer supports existing questions, mixed sets, review records, Challenge Lab records, proposals, media staging, import/export, search, and bulk replacement. The completion pass must verify the full promised authoring surface for all question formats and the richer Challenge Lab fields such as datasets, tables, graph definitions, variables, scoring guidance, and extension prompts.

Media administration still needs a complete publication mapping for staged assets, replacement history, usage inspection, orphan reporting, and narration-freshness tracking before staged files can safely become student-facing.

### E. Roles, permissions, and write-action audit coverage

The current local deployment intentionally authenticates one owner. The implementation plan reserved roles and permissions as a broader access-control capability. Before multi-user access is ever enabled, permissions must be explicit and enforced server-side for every protected operation.

The completion pass must also verify that all meaningful administrator mutations produce useful audit events, not only authentication and CSRF events.

### F. Local system health and repair

After the admin-authoring gaps above are closed, Content Studio should gain the planned one-click local health view. It should verify private databases, backup integrity, local credentials configuration, publication locks, repository state, Python environment, dependencies, loopback networking, writable local storage, and updater readiness. Repair actions must be narrow, reversible, and unable to delete drafts, media, credentials, release history, or AP Biology content.

## Completion order

The safe order is

`UI integration → Settings and teacher workflow → Structural administration → Assessment/Challenge/media parity → Permissions and audit completion → Local health/repair → final whole-system browser acceptance`

This order keeps the original administrator goal ahead of additional deployment convenience work.

## Non-negotiable boundaries

- Published student content remains authoritative until a validated release is merged and verified.
- Browser editing never writes directly to `content/ap-biology`.
- Structural operations begin as recoverable drafts or proposals.
- Stable identifiers cannot be silently rewritten by movement or reordering.
- Every destructive-looking action must remain recoverable.
- GitHub Pages remains student-only.
- Content Studio private state, credentials, candidate packages, databases, and staged media remain outside the public Pages artifact.
- Production `main` remains untouched until the complete admin capability branch passes the full regression and an explicit publication or integration decision is made.

## Current next implementation

The next implementation after the publication bootstrap correction is the Settings and Teacher Workflow layer. That work should make Settings real, add cross-record notes/comments/tasks/recent-work views, expose configuration and safety gates truthfully, and retain the same authenticated CSRF-protected draft boundary used by the rest of Content Studio.
