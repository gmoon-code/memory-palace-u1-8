# Content Studio integration and deployment gate

## Purpose

Steps 1 through 9 established the Content Studio foundation, security boundary, normalized catalog, draft and revision system, editors, complete replacement workflow, management tools, quality and preview system, and controlled publication engine. This gate treats those pieces as one product before any merge into the production `main` branch or any trusted-server deployment.

The gate is deliberately separate from the nine implementation steps. It does not add another content feature. It verifies that the completed system can be packaged, deployed, authenticated, exercised, backed up, and released without weakening the frozen student runtime.

## Current branch model

The integration branch begins from the validated Step 9 head. Production `main` remains unchanged until an explicit release decision is made. No integration-gate file should modify AP Biology curriculum content or the existing student application runtime.

## Whole-system invariants

The integration gate preserves these invariants.

- GitHub Pages remains a student-only static deployment.
- `frontend/admin` is never copied into the public Pages artifact.
- Content Studio remains disabled unless `MEMORY_PALACE_ADMIN_ENABLED=true` is supplied on a trusted server.
- Authentication credentials, session secrets, GitHub tokens, SQLite databases, draft stores, media stores, candidate packages, and release records remain outside Git.
- Drafts and replacement work remain non-destructive until controlled publication completes.
- Controlled publication, GitHub delivery, and server-side merge remain three independent gates.
- A publication candidate cannot bypass blocking Step 8 quality findings, stale-draft checks, source-hash checks, or GitHub Actions verification.
- Rollback creates another validated candidate and does not rewrite repository history.
- Student content files remain authoritative until the publication workflow verifies the exact released hashes.

## Integration evidence added by this gate

The repository now contains a production-oriented container definition under `deploy/content-studio`, an explicit container build exclusion file, a private-deployment runbook, a read-only deployment smoke test, and a whole-system integration QA script. The normal GitHub Actions QA workflow runs the integration check alongside every previous Content Studio and Unit 1 through Unit 8 regression.

The container itself remains safe when launched with no private configuration. It uses `MEMORY_PALACE_ENV=production`, runs as a non-root user, exposes the existing health endpoint, and starts with the admin, publication, GitHub-delivery, and server-side-merge gates disabled.

## Deployment rehearsal gate

A trusted deployment is ready for an end-to-end rehearsal only after all of the following are true.

1. The deployment serves only HTTPS to the teacher-facing browser.
2. A persistent volume is mounted at `/app/server_data` and survives a container restart.
3. Owner credentials are generated locally with `scripts/generate_admin_credentials.py` and stored only in the provider's secret manager.
4. Content Studio authentication, session expiration, logout, audit history, draft saving, revision history, snapshots, preview, and Step 8 quality checks work on the deployed instance.
5. `scripts/smoke_content_studio.py` passes against the deployed HTTPS URL.
6. A disposable draft can be created and deleted or archived without changing the published student files.
7. Controlled publication can create and validate a disposable candidate while GitHub delivery is still disabled.
8. GitHub delivery can create a temporary candidate branch and pull request whose exact commit passes the repository QA workflow.
9. Source-hash drift blocks submission when the remote base changes.
10. A disposable release can be verified and a rollback candidate can restore its captured pre-release state.

## Release decision gate

A merge into `main` should occur only after the full repository QA is green on the integration head and the deployment rehearsal has passed. The merge itself does not enable Content Studio on GitHub Pages. The public Pages workflow still produces only the student artifact, while the private FastAPI service requires a separate trusted deployment and private environment configuration.

Server-side merging should remain disabled unless there is a specific operational reason to allow the private Content Studio service to merge its own validated pull requests. A normal pull-request review and manual merge remains compatible with the publication system.

## Recovery requirements

Before the first real publication, preserve a backup of `/app/server_data` and verify that it can be restored into a fresh container. Keep the GitHub repository as the authoritative published history and the server-side publication database as operational evidence. If the private service is lost, published student content remains intact in GitHub and GitHub Pages.

## Acceptance criteria

The integration gate passes when the full GitHub Actions workflow succeeds with the new integration QA included, the integration branch contains no curriculum-content changes, production `main` remains untouched, the deployment package defaults every administrative publication gate to off, and the repository contains enough documentation and tooling to perform a controlled private-server rehearsal without exposing secrets or admin assets to the student site.
