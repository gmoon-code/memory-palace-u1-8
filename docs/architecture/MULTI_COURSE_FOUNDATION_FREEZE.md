# Multi-course foundation freeze

## Freeze identity

The completed multi-course foundation is frozen at implementation commit `8d6a94fbab3bec63e53daaf80b949825d7eacccd` with repository tree `e10f742f128c557797ce167c3243879d44b779bd`.

The permanent rollback reference is

```text
freeze/multi-course-foundation-2026-09-19
```

That reference points directly to the validated implementation commit above. The freeze records the architecture before any real AP Chemistry curriculum production begins.

Production `main` was `31da83df397acfe53d03a77bf54dff7b5ab6346c` at the time of the freeze. This freeze does not merge the architecture branch into `main`.

## Validation evidence

Memory Palace QA run `35435465751` completed successfully on the exact frozen implementation commit. That run included the package contract, AP Chemistry architecture fixture, AP Biology Units 1 through 8 release locks, every Content Studio subsystem, the multi-course integration gate, the classroom/browser acceptance gate, the dedicated multi-course acceptance tests, the full Python suite, JavaScript syntax checks, container validation, deterministic GitHub Pages builds, release packaging, and final source-drift verification.

The machine-readable record is `release/architecture/multi-course-foundation-v1.0.0.json`.

## Course-state lock

AP Biology remains the production curriculum course. It is available, student-visible, catalog-ready, and editable.

AP Chemistry remains an architecture fixture. It is development-only, hidden from students, catalog-ready for inspection, and read-only. The fixture demonstrates repeated local IDs, course-scoped source resolution, read-only previews, and course isolation. Its current content is not the future real AP Chemistry curriculum baseline.

## Source fingerprints

The machine-readable freeze stores Git object fingerprints for the complete repository tree and the architecture-critical scopes. These include the backend, full content tree, AP Biology curriculum tree, AP Chemistry fixture tree, complete frontend, administrator frontend, student JavaScript, platform contracts, course packages, package schemas, scripts, and tests.

It also locks the exact Git blobs for the course registry, AP Biology package, AP Chemistry package, and course-package schema.

An expanded tracked-file manifest for the frozen implementation can be generated at any time with

```text
python scripts/export_content_studio_release_manifest.py --ref 8d6a94fbab3bec63e53daaf80b949825d7eacccd --output /tmp/multi-course-foundation-files.json
```

The expanded manifest contains every tracked path, Git object ID, mode, and byte size at the frozen commit.

## Rollback model

The freeze branch is intended as a stable recovery and comparison point. For a non-destructive inspection of the exact baseline, use

```text
git fetch origin freeze/multi-course-foundation-2026-09-19
git switch --detach origin/freeze/multi-course-foundation-2026-09-19
```

Returning an active development branch to the freeze would be a separate deliberate recovery action. The repository does not automate a destructive reset or force update.

## Freeze QA

The repository runs `scripts/qa_multi_course_foundation_freeze.py` in normal CI. The gate checks the manifest against the exact frozen commit, validates all recorded Git object fingerprints, verifies the course registry state at the frozen baseline, confirms the current architecture branch descends from the frozen implementation, and rejects freeze-evidence commits that modify protected runtime, curriculum, platform, or frontend scopes.

Only the freeze evidence files and the workflow registration for the freeze gate may differ from the frozen implementation when this checkpoint is created.

## Boundary for future work

Future AP Chemistry work begins after this checkpoint. The freeze gate validates the historical implementation commit and the historical freeze-evidence checkpoint. It does not require later development heads to remain byte-identical to the frozen implementation.

New AP Chemistry source intake, scope mapping, unit architecture, scientific records, narratives, questions, review records, labs, and student-facing publication state may therefore be developed in later commits while the rollback branch and recorded fingerprints continue to preserve the known-good architecture boundary.

The architecture freeze itself adds no curriculum content and changes no current course permissions.
