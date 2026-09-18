# Content Studio teacher handoff and distribution

Content Studio v1.0.0 has completed a live teacher acceptance rehearsal on Windows using the supported local-only installation model. The validated teacher runtime is commit `f5d4fe65d56797803e324f5a66805765a6c07714`, tree `5b2ff607bf5c4077a86bc059a0493b166c76828a`.

## Acceptance record

The live rehearsal covered first installation, owner setup, login, Dashboard, Course Map, Units 1 through 8, protected draft editing, Student Preview, Content Health, Version History, restart persistence, local backup, validated restore, Health and Repair, safe updater behavior, automatic updater rollback, repository integrity, the remaining administrator workspaces, publication-off state, Security and Audit, and Complete Story Replacement.

Complete Story Replacement was exercised on a protected Unit 8 scene draft. The required-knowledge inventory, dependency counts, permanent route lock, Question Bank lock, review lock, old-versus-new analysis, recovery snapshot, new draft revision, Version History, and Student Preview all passed. No publication action was performed.

The final integrity check showed a clean tracked worktree, no diff under the published AP Biology student-content paths, Content Studio version `1.0.0`, and the tracked `server_data/.gitkeep` placeholder.

## Windows maintenance discovered during acceptance

The live rehearsal identified three Windows-specific maintenance defects that Linux CI did not expose.

1. Backup and Restore launchers required fully quoted virtual-environment Python paths when the repository folder contained spaces.
2. SQLite backup connections required explicit closure before Windows temporary-directory cleanup.
3. The zero-cost runtime QA required explicit closure of its SQLite verification connection before Windows temporary-directory cleanup.

The restore workflow also exposed that `server_data/.gitkeep` needed to be tracked so a valid restore would not leave the repository dirty and block the safe updater.

Each issue was corrected through a controlled branch and pull request, followed by full Memory Palace QA and post-merge validation. The final accepted runtime commit is the one locked in `release/content-studio/teacher-distribution-v1.0.0.json`.

## Distribution model

The teacher onboarding ZIP is a small bootstrap package. It contains the Windows installer and teacher-facing setup/recovery instructions. It does not contain the repository, credentials, private Content Studio state, a virtual environment, or Git metadata.

The installer requires free Python 3.10 or newer and free Git for Windows. It validates its own extracted package before installation, clones only the official repository, leaves the local checkout on branch `main`, resets that new clone to the locked validated runtime commit, verifies the Content Studio version and required launchers, then starts the normal local launcher.

An existing non-empty installation directory is never reset or overwritten by the installer. Existing installations use the supported Backup, Restore, Repair, and Update launchers.

The local Content Studio runtime remains bound to `127.0.0.1`. Publication, GitHub publication, and GitHub merge controls remain disabled in the supported local zero-cost workflow.

## Package generation

Run

```bash
python scripts/build_content_studio_teacher_distribution.py --output /tmp/ContentStudio_v1.0.0_Teacher_Onboarding.zip
```

The builder creates the onboarding ZIP and a SHA-256 sidecar. The archive is deterministic for the same tracked source files. `PACKAGE_MANIFEST.json` records every packaged file with its size and SHA-256 digest.

Run

```bash
python scripts/qa_content_studio_teacher_distribution.py
```

to validate the distribution lock, runtime target, source invariants, deterministic package build, archive membership, manifest hashes, package self-validation, zero-cost boundary, and exclusion of credentials and private state.

The earlier pre-acceptance onboarding ZIP that pinned commit `4727a86b3670f0375b66191849e76c2912a40e46` is obsolete and must not be distributed.
