# Multi-course architecture integration gate

## Purpose

This gate closes the multi-course foundation work after drafts, generic editors, Complete Story Replacement, management, quality and preview, and publication have all been made course-aware. It adds no curriculum and enables no new course for students or teacher editing. Its purpose is to verify that the completed architecture continues to preserve course boundaries as one integrated system.

Production `main` remains untouched until a separate release decision is made.

## Locked course states

The gate treats the current registry state as intentional.

- AP Biology remains `available`, student-visible, catalog-ready, and editable.
- AP Chemistry remains `development`, hidden from students, catalog-ready for architecture inspection, and read-only.
- A catalog-ready course may be inspected without becoming editable.
- Course-local identifiers such as `unit-1`, journey IDs, scene IDs, and entity IDs never provide enough identity for a mutable operation by themselves. Protected writes carry `course_id`.

No real AP Chemistry curriculum expansion belongs in this gate.

## Package and source isolation

Each course is resolved through its package manifest. Every unit source used by the protected editor and publication paths must remain under that course unit's declared `content_root`. Package declarations are the authority for source locations.

AP Biology and AP Chemistry intentionally reuse course-local unit IDs. Resolving `unit-1` through the selected package must therefore return different course-specific records without ambiguity.

## Protected administrator boundaries

The integrated system keeps the following boundaries.

- Draft and revision operations are course-scoped.
- Generic editor source resolution is package-declared and course-scoped.
- Complete Story Replacement carries course identity through analysis, draft creation, validation, and save.
- Question, Review, Challenge Lab, bulk replace, search, import/export, and media operations are course-scoped.
- Media database rows store `course_id`; legacy rows migrate to AP Biology for backward compatibility.
- Quality and Student Preview can inspect catalog-ready courses while write behavior remains governed by `editable`.
- Publication candidates and releases store `course_id`; legacy publication rows migrate to AP Biology.
- Publication source destinations are constrained to the selected package.
- AP Chemistry write actions remain blocked while the course is read-only.

## Student deployment boundary

The GitHub Pages builder continues to publish only registry entries that are both `status=available` and student-visible. The AP Chemistry architecture fixture therefore remains absent from student curriculum output. The administrator frontend, private databases, staged media, credentials, and publication packages remain excluded from Pages.

## Backward compatibility

Historical single-course data predates explicit course identity. Draft, media, candidate, and release migrations preserve those rows as AP Biology. The compatibility default exists only for legacy data and older API callers. New cross-course paths carry course identity explicitly.

## Automated gate

The repository runs

```text
python scripts/qa_multi_course_integration_gate.py
```

inside the normal GitHub Actions workflow. The gate verifies registry state, package validity, source-root isolation, catalog-ready versus editable separation, absence of fixed eight-unit assumptions in the multi-course admin modules, course-aware database migrations, student deployment filtering, and the presence of cross-course regression coverage.

The gate must pass together with the existing package QA, AP Chemistry fixture QA, Steps 1 through 9 administrator QA, deployment integration checks, the complete Python test suite, JavaScript syntax checks, deterministic release packaging, and no-source-drift verification.

## Classroom and browser acceptance

After this architecture gate, the repository also runs the dedicated teacher-facing acceptance documented in `docs/architecture/MULTI_COURSE_CLASSROOM_BROWSER_ACCEPTANCE.md`. That pass exercises course switching, AP Biology authoring, AP Chemistry read-only inspection, cross-course draft rejection, browser workspace resets, and the student deployment boundary.

## Foundation freeze

After the classroom/browser acceptance pass succeeds, the validated implementation is preserved by `release/architecture/multi-course-foundation-v1.0.0.json` and the rollback branch `freeze/multi-course-foundation-2026-09-19`. The freeze QA verifies the exact implementation commit, repository tree, architecture-critical source fingerprints, package blobs, course states, and the absence of protected-source drift in the freeze-evidence commit.

## Completion condition

The multi-course foundation is considered integrated when this gate, the classroom/browser acceptance gate, the foundation freeze gate, and the full repository workflow succeed, AP Chemistry remains hidden and read-only, AP Biology content locks continue to pass, no administrator subsystem can cross course boundaries through reused local IDs, and production `main` remains unmerged.
