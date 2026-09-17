# Content Studio Step 3 · Normalized Content Catalog and Dependency Graph

Step 3 creates the stable read-only content model that future Content Studio editors will use. The existing AP Biology runtime remains the publication source. No source content is rewritten in this stage.

## Why this layer exists

The eight-unit release was produced across several development generations. Unit 1 and later units do not store every artifact in identical files or schemas. A browser editor that writes directly into those heterogeneous files would make structural edits, story replacement, review changes, and dependency protection fragile.

The normalized catalog reads the frozen runtime and projects it into one consistent model. Future draft editors can work against that model while the publication compiler remains responsible for producing valid runtime files.

## Normalized entity types

The catalog currently indexes these entity types.

- Course
- Unit
- Journey
- Scene
- Location
- Character or scene object
- Canonical concept
- Memory Object
- Question
- Mixed-discrimination question set
- Challenge Lab item

Each entity has a stable Content Studio identifier that is separate from the source file path. Existing identifiers such as `U8-K-063`, `MO-APBIO-U1-P003`, `U8-J1`, and `U8-L01` are retained as aliases so source references can be resolved without changing the runtime.

## Dependency graph

Relationships are represented as explicit graph edges. Current relationships include containment, concept definition, Memory Object representation, journey guide, scene location, scene cast, teaching links, Quick Recall attachment, review assessment, mixed-discrimination membership, Challenge Lab assessment, and Challenge Lab prerequisite scenes.

The dependency inspector can traverse both inbound and outbound relationships. This is the foundation for later warnings such as a story replacement removing a Memory Object that is still used by review questions or a Challenge Lab prerequisite.

## Release alignment

The normalized catalog compares its structural totals against `content/ap-biology/mainline-release-u1-u8.json`. The frozen release declares

- 8 units
- 58 guided journeys
- 448 permanent scenes
- 1,561 canonical records
- 112 Challenge Lab items

A mismatch is treated as a catalog error. The Content Health screen exposes these checks directly.

## Read-only administration API

All Step 3 catalog endpoints live under the authenticated `/api/admin/catalog/*` namespace. They require an active owner session and do not expose POST, PUT, PATCH, or DELETE content operations.

The available read operations provide a catalog summary, Course Map, paginated entity lists, global search, source-reference resolution, individual entity lookup, dependency reports, and catalog health.

## Content Studio user interface

Step 3 activates several previously reserved administration surfaces.

The Dashboard now reports normalized totals, release alignment, and indexed content types. The Course Map renders the complete Unit → Journey → Scene route and allows a scene to open in the dependency inspector. Units, Journeys, Scenes, Concepts, Memory Objects, Questions, and Challenge Lab screens can browse their normalized records with unit filtering. Global search spans the normalized catalog. Content Health reports release mismatches and unresolved source references.

These are inspection tools. Editing remains deliberately disabled until the draft and revision layer exists.

## Complete Story Replacement preparation

The replacement workflow will eventually use this graph before accepting a new story. For a selected scene or journey, the system can identify current Memory Objects, canonical concepts, characters, locations, Quick Recall items, review questions, mixed-discrimination relationships, Challenge Lab dependencies, and other directly or indirectly linked records.

This allows replacement to preserve the source version, compare required knowledge coverage, identify missing dependencies, and block publication when structural references would break.

## Step 3 acceptance criteria

Step 3 is complete when the normalized model covers all eight released units, the frozen structural totals match, protected read-only catalog APIs are available, the Course Map and dependency inspector use the catalog, global search can find linked records, Content Health exposes alignment and unresolved references, automated catalog regression tests pass, existing Unit 1–8 QA remains green, and production `main` remains unchanged.

## Boundary for Step 4

Step 4 adds the draft store and revision model. It will introduce working copies, autosave, revision records, archive state, comparisons, and recoverable snapshots. No publication write should be added before that layer is validated.
