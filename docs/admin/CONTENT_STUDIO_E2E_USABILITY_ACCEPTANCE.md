# Content Studio end-to-end administrator usability acceptance

This pass validates Content Studio as one teacher-facing product after the capability and workflow-integration stages.

## Acceptance route

Representative teacher work is exercised through Browse → Edit → Draft → Preview → Validate → Publish preparation → Recover. The automated acceptance suite also covers Complete Story Replacement, Question Bank, Review System, Challenge Lab, and a published student preview from every AP Biology unit.

## Usability changes

The administrator interface now includes a compact first-use workflow guide directly below the Current record bar. It explains working-copy isolation, Preview and Validate, recovery history, deliberate publication, and the local $0 operating boundary.

Staged-development wording left in the original shell is normalized at runtime so the interface no longer tells teachers that editors, previews, media management, version history, import/export, or publishing are future capabilities when those workspaces already exist.

Workspace navigation now protects unfinished local input. Field editors, managed assessment editors, the generic draft editor, and Complete Story Replacement are checked before a teacher leaves the active workspace or closes the browser. Complete Story Replacement receives its own dirty-state tracking because its replacement form can contain meaningful local input before the change is applied to the protected draft.

The guard does not create, save, apply, publish, merge, or roll back content. The teacher still controls those actions through their existing protected workflow.

## Automated acceptance coverage

The acceptance test suite performs the following checks against temporary administrator databases.

- A representative published scene from each of Units 1 through 8 can be opened through Student Preview.
- A Unit 8 scene can move through working-copy creation, field editing, named snapshot creation, draft-aware Student Preview, entity quality inspection, publication eligibility, and isolated release-candidate creation.
- The canonical source journey file is hashed before and after the workflow and must remain unchanged.
- Complete Story Replacement can analyze and apply a narrative-only replacement to the protected working copy while leaving the source file untouched.
- An existing Unit 8 question can be opened, edited in a working copy, and previewed as draft content.
- The Unit 8 review timeline remains available and populated.
- A Unit 8 Challenge Lab item can be resolved through the management layer and previewed with the student practice renderer.
- The publication candidate remains isolated from the live course and creates a pre-publication recovery snapshot.

## Safety boundary

The usability module performs presentation, navigation protection, and guidance only. It contains no administrator POST, PATCH, DELETE, publication, GitHub, or source-file write operation.

The zero-cost local operating rule remains unchanged. No paid hosting, paid storage, paid API, billing account, or payment method is introduced by this pass.

## Production boundary

This branch does not modify `content/ap-biology` or the student runtime. Production `main` remains separate until the consolidated Content Studio release candidate is intentionally prepared and validated.