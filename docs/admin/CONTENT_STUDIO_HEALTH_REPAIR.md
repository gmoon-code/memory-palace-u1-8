# Content Studio System Health and Repair

This stage adds a local system-health layer to the completed Content Studio administrator workspace. It keeps the project on the zero-cost local architecture and gives the owner a bounded way to inspect and maintain the private administrative environment before the full administrator capability audit.

## Administrator surface

Settings now opens System Health Check rather than a reserved placeholder. Security and Audit also receives a shortcut into the same workspace.

The report checks the local-only network binding, owner authentication configuration, publication locks, absence of paid-hosting blueprints, writable private state, media and publication workspaces, free disk space, SQLite integrity, newest local backup, private Python environment, exact Git origin, updater-ready branch, current commit, and Git ignore coverage for private state.

Each finding is classified as healthy, warning, or error. Errors indicate a local safety boundary that should be resolved before administrative work continues. Warnings can represent optional state that has not been created yet, such as an unused database, or local tooling that needs attention.

## In-app repair boundary

The authenticated owner can invoke only the following allowlisted maintenance actions through the API.

- Create missing private directories
- Run passive SQLite WAL checkpoints and SQLite optimize
- Remove stale `.tmp`, `.part`, and editor-backup files older than 24 hours inside `server_data`
- Create a new local state backup
- Run the combined safe maintenance sequence

Every mutation requires the existing Content Studio session and CSRF protections. Repair actions are recorded in the server-side audit log.

The repair API never deletes drafts, revision history, snapshots, staged media, credentials, canonical AP Biology content, or student-facing files. It has no action for enabling publication.

## Environment-level repair

A running server should not replace the Python interpreter that is executing it. Environment repair is therefore deliberately outside the web request path.

`Repair Content Studio.cmd` first requires the local server to be stopped. The helper then creates a local state backup, recreates missing private directories, restores the loopback and publication-lock settings in the ignored local environment file, and validates the private Python environment. If the environment must be rebuilt, the old `.venv` is retained until the replacement environment and free dependencies install successfully. A failed rebuild restores the previous `.venv`.

The helper does not rotate owner credentials and does not intentionally modify `server_data`. It does not change AP Biology curriculum files.

## Zero-cost boundary

The local architecture continues to require no hosting account, cloud database, paid API, subscription, or billing method. Content Studio binds to `127.0.0.1`, stores its administrative state in ignored local files, and keeps controlled publication, GitHub publication, and server-side merge disabled in the zero-cost operating mode.

## Validation

`tests/test_admin_health.py` exercises the local safety report, publication-lock detection, allowlisted repair behavior, CSRF requirement, and rejection of unapproved repair actions.

`scripts/qa_content_studio_health_repair.py` statically verifies route registration, Settings integration, zero-cost markers, backup-first environment repair, publication locks, and the absence of destructive repair paths. The main GitHub Actions workflow runs this QA and checks the new browser module syntax.

## Next administrator stage

With local operating health visible and recoverable, the next work item is the full administrator capability audit. That audit should test every Content Studio navigation area against the original administrator-capability matrix and then close any remaining placeholder, disconnected workflow, CRUD, dependency, validation, preview, or recovery gaps.
