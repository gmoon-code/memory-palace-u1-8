# Content Studio Step 6

## Complete Story Replacement

Step 6 adds a dedicated replacement workflow for large narrative changes. It is intentionally separate from ordinary field editing because replacing a complete story can affect scientific coverage, memory cues, spatial continuity, retrieval prompts, and downstream assessment records at the same time.

The workflow remains draft-only. It does not write any published AP Biology JSON file and it does not change the student website. Publication remains a later controlled step.

## Supported replacement targets

Step 6 supports two target classes.

- Scene replacement targets one permanent scene.
- Journey replacement targets one complete guided journey and all of its scene narratives.

Supported scene modes are `narrative_only`, `narrative_plus_scene_design`, and `complete_scene`.

Supported journey mode is `complete_journey`.

The complete journey workflow keeps the published scene count, scene order, stable loci, and route identity locked. A teacher can replace the narrative frame and all scene narratives in one protected operation while the route remains stable.

## Required knowledge inventory

Before a replacement draft is opened, the backend builds a required-knowledge checklist from the published target.

The checklist combines

- Memory Object and concept references attached to the source scene or journey scenes
- Quick Recall knowledge targets
- normalized catalog dependency edges marked as `teaches` or `teaches_concept`
- represented canonical concepts linked through Memory Objects

Each checklist item retains its normalized entity ID, raw source reference where available, canonical term, definition, and record type.

The replacement analysis compares the candidate with the published knowledge references. If a required source reference disappears, the replacement is blocked. This rule is enforced even when a teacher turns off a preservation option. Scientific coverage cannot be silently dropped through the replacement workflow.

The analyzer also checks whether canonical terms are explicitly named in the replacement narrative. Missing wording is reported as a warning because literal term presence cannot prove or disprove conceptual accuracy by itself.

## Stable identity and route locks

Step 6 preserves stable identifiers and the permanent spatial route.

For scenes, locked fields include the normalized entity ID, entity type, unit ID, journey ID, palace ID, scene index, locus ID, and source path.

For journeys, locked fields include the normalized entity ID, entity type, unit ID, palace ID, and source path.

Journey scene order and locus identities are compared with the published route signature. A changed scene count, changed scene index, or changed locus identity blocks the replacement.

This protects review links, student progress references, dependency indexes, and later publication transforms from accidental identity drift.

## Preservation controls

The teacher can choose whether to preserve several current-draft domains while preparing a replacement.

- title and naming
- location and scene layout
- characters and scene objects
- Memory Object links
- Quick Recall configuration
- concept associations

The permanent route, external Question Bank links, and review links are locked as preserved in Step 6.

Preservation controls operate on the protected current draft. They do not mutate the published base.

## Dependency review

For every replacement target, Step 6 asks the normalized dependency engine for a depth-three report. The workflow surfaces linked counts and relevant downstream records such as questions, question sets, Challenge Lab items, later scenes, journeys, canonical concepts, and Memory Objects.

External assessment and application records remain unchanged. Their presence is shown as a warning so the teacher can review whether the rewritten story still prepares students for the same downstream work.

## Old-versus-new analysis

Before Apply is enabled, the replacement candidate is analyzed against the published base.

The analysis includes

- published story text
- current draft story text
- replacement candidate story text
- blocking findings
- warnings
- required-knowledge status
- missing required source references
- terms that are not explicitly named
- route preservation status
- downstream dependency impact

The UI displays the published story and replacement candidate side by side.

## Automatic recovery snapshot

Apply never saves the replacement directly without first creating a recovery point.

The backend creates a named snapshot such as

`Before narrative only replacement · v1`

Only after that snapshot succeeds does the replacement candidate become the next draft revision.

The snapshot and all prior revisions remain available through the Step 4 Draft Workspace and Version History tools. Restoring a prior revision or snapshot creates another revision and does not destroy later history.

## Concurrency and security

Replacement planning is authenticated. Replacement draft creation, analysis, and apply operations use the protected `/api/admin/replacements/*` namespace.

All mutations require

- an authenticated owner session
- the session-specific CSRF token
- the expected current draft version

If another editor changes the draft after the replacement screen loads, the expected-version check returns a conflict and prevents silent overwrite.

## Frontend workflow

The Complete Story Replacement workspace follows this sequence.

1. Choose a scene or journey.
2. Review the required-knowledge checklist.
3. Review connected downstream content.
4. Choose the replacement mode and preservation policy.
5. Open the protected replacement draft.
6. Write the replacement narrative or journey scenes.
7. Analyze the candidate.
8. Review blockers, warnings, required knowledge, and old-versus-new story text.
9. Apply only when structural checks pass.
10. The backend creates a snapshot and saves the replacement as a new draft revision.

## Deliberate Step 6 boundaries

Step 6 does not publish draft content to the student runtime.

Step 6 does not alter external questions or review records as part of a story replacement.

Step 6 does not allow stable route IDs to be changed.

Step 6 does not claim that literal term detection proves scientific adequacy. Term absence is a warning while missing required knowledge references are a blocker.

Student preview, broader content-health checks, accessibility review, and publication gates remain later stages in the Content Studio plan.
