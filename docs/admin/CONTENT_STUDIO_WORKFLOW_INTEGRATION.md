# Content Studio workflow integration

This pass connects the existing administrator workspaces into one record-centered route. It does not add a new content model and it does not publish curriculum files.

## Persistent record context

Selecting a record in Course Map, catalog/search results, field editors, Question Bank, Challenge Lab, Complete Story Replacement, Student Preview, Content Health, or Draft Workspace updates one session-scoped workflow context. The context contains only the stable entity ID, type, unit, display title, preferred editing workspace, and active draft ID/version when one exists.

The context is stored in browser `sessionStorage`. It survives navigation and same-tab refreshes, and it is cleared when the administrator signs out or explicitly chooses Clear. It contains no password, session cookie, CSRF token, unpublished payload, or student data.

## Integrated route

The workflow bar follows the administrator capability route already defined by Content Studio.

1. Browse opens global catalog search with the current stable record ID.
2. Edit returns to the correct field editor, Question Bank, Challenge Lab, or Complete Story Replacement target.
3. Draft opens the matching active working copy. When no working copy exists, Content Studio fills the stable entity ID into Draft Workspace and leaves creation as an explicit administrator action.
4. Preview opens Student Preview with the current unit and supported entity type selected, then opens the same record.
5. Validate opens Content Health for the current unit and reports record-specific quality counts when available.
6. Publish opens Publishing and selects the current eligible working copy for candidate preparation. Publication safety gates remain unchanged.
7. Recover opens the current working-copy snapshots. When no active draft exists, it opens verified release history and rollback controls.

A separate Version history shortcut opens the current draft revision history directly.

## Safety behavior

`frontend/admin/workflow.js` performs navigation and authenticated read-only lookups. It intentionally contains no `POST`, `PATCH`, `PUT`, or `DELETE` request. Draft creation, saving, replacement application, publication candidate creation, release submission, merge, and rollback remain inside their existing protected workspaces and keep their existing confirmation, CSRF, validation, and server-side safety gates.

The workflow layer does not reference `content/ap-biology` paths and has no filesystem write path. Public GitHub Pages remains student-only.

## Supported direct preview types

Direct Student Preview handoff is available for Unit, Journey, Scene, Concept, Memory Object, Question, and Challenge records. Character, Location, and question-set records keep their context but do not claim a student renderer that does not exist.

## QA

`scripts/qa_admin_workflow.py` verifies the seven workflow stages, record-level Version History, cross-workspace selection capture, draft linking, quality and publication handoffs, canonical loader order, mobile workflow styling, and the absence of automatic mutating requests or direct published-content paths.

The main test suite also verifies that the canonical `/admin/drafts.js` loader imports `workflow.js` after the other late-stage administrator modules and that the workflow asset retains the no-automatic-mutation boundary.
