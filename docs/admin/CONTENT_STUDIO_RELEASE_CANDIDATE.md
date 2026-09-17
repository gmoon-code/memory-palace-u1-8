# Content Studio v1.0.0-rc1 Release Candidate

Content Studio `1.0.0-rc1` freezes the complete local administrator implementation that was accepted on commit `cdf4bb2a1ea91415dd1634323ac5ab40ccba863f`.

## Release identity

- Release ID `content-studio-v1.0.0-rc1`
- Frozen implementation commit `cdf4bb2a1ea91415dd1634323ac5ab40ccba863f`
- Frozen implementation tree `133a3bc9b00c2149662d4e6dba8517f0706b585c`
- Production baseline `main` commit `6d561f19a19b07b9a386442d327db3ca12299bef`
- Release evidence branch `admin/content-studio-release-candidate`

The implementation commit is the runtime freeze. Commits after that point may add release evidence only. The release-candidate QA fails if backend, administrator frontend, local launchers, deployment files, curriculum, or student runtime change after the freeze.

## Included administrator system

The frozen implementation contains the complete Content Studio sequence through the publication system, plus the later integration and local-operation work. This includes authentication, sessions, CSRF protection, audit events, the normalized curriculum catalog and dependency graph, server-side drafts and immutable revision history, field-specific editors, Complete Story Replacement, Question Bank and Review System management, Challenge Lab management, staged media, import and export, Student Preview, Content Health, controlled publication candidates, rollback support, Health Check and Repair, administrator capability auditing, persistent current-record workflow context, end-to-end usability safeguards, and first-use guidance.

The local operating package also includes the one-click Windows launcher, backup, restore, repair, and safe updater workflows. The local edition remains designed for zero-cost operation on the teacher computer.

## Administrator workflow

The accepted administrator route is

`Browse → Edit → Draft → Preview → Validate → Publish → Recover`

The Current record context follows the administrator between those workspaces. Working-copy creation, saving, story replacement, publication candidate creation, GitHub submission, merge, rollback, and destructive recovery remain explicit protected actions. The workflow layer does not perform them automatically.

## Release safety contract

The release candidate locks these conditions.

- Published AP Biology curriculum is unchanged until an explicit publication action occurs.
- Student-facing frontend files remain identical to the production baseline for this administrator release.
- Content Studio is excluded from the public student GitHub Pages build.
- Admin access is disabled by default.
- Content publication is disabled by default.
- GitHub publication is disabled by default.
- Automatic GitHub merge is disabled by default.
- Private credentials and SQLite state remain outside tracked source control.
- The zero-cost local operating requirement remains mandatory.

## Exact manifest

`release/content-studio/v1.0.0-rc1.json` is the release lock. It stores the frozen implementation commit, tree identity, key Git object identities, safety defaults, and the production baseline.

For a complete deterministic tracked-file manifest of the frozen implementation, run

```bash
python scripts/export_content_studio_release_manifest.py \
  --ref cdf4bb2a1ea91415dd1634323ac5ab40ccba863f \
  --output /tmp/content-studio-v1.0.0-rc1-files.json
```

The release-candidate QA runs the same manifest expansion twice and requires byte-identical serialization.

## Acceptance evidence

The release candidate inherits the complete administrator acceptance suite from the frozen implementation. Representative scenes across Units 1 through 8 are exercised through student preview. A real Unit 8 scene is exercised through working-copy editing, snapshots, draft-aware preview, Content Health, publication eligibility, and isolated candidate creation. Complete Story Replacement, Question Bank editing, Review System access, Challenge Lab preview, local runtime, backup and restore, updater behavior, Health Check and Repair, public-site isolation, deterministic release packaging, Python tests, JavaScript syntax validation, and no-source-drift checks are also covered.

The release-specific gate is `scripts/qa_content_studio_release_candidate.py`. It verifies the frozen implementation commit and tree, exact key Git objects, publication-off defaults, zero-cost lock, deterministic manifest expansion, student-site invariants, and the restriction that all post-freeze changes are release evidence only.

## Clean install and recovery rehearsal

The final practical RC1 gate is `scripts/qa_content_studio_rc1_clean_rehearsal.py`. It expands the exact frozen implementation into a clean temporary copy and verifies every tracked path, size, and Git blob before use. It then runs real first-use owner setup, local authentication, CSRF-protected draft editing, process restart persistence, Content Health, an allowlisted database repair, publication-lock enforcement, local backup creation, deliberate post-backup draft mutation, validated restore, post-recovery sign-in, updater-safety acceptance, and final byte-for-byte student-content invariants.

The rehearsal uses no real teacher credentials, no hosted infrastructure, no cloud database, no paid API, no billing account, and no payment method. Publication, GitHub delivery, and merge remain disabled for the entire rehearsal. Details are recorded in `docs/admin/CONTENT_STUDIO_RC1_CLEAN_REHEARSAL.md`.

## Merge status

This file does not authorize a merge into `main`. Production remains frozen until the release candidate has passed the complete GitHub Actions workflow on the exact final evidence head and a separate integration decision is made.
