# Content Studio deployment

This directory packages the private FastAPI Content Studio service. The public GitHub Pages student site remains a separate static deployment and must never receive `frontend/admin`, server databases, credentials, publication candidates, or GitHub tokens.

## Deployment contract

Build from the repository root so the Dockerfile can copy the complete application and frozen AP Biology content.

```bash
docker build -f deploy/content-studio/Dockerfile -t story-method-content-studio .
```

The image deliberately starts with every administrative and publication gate disabled. A trusted deployment must provide its own environment variables and persistent storage before Content Studio is enabled.

Mount durable storage at `/app/server_data`. The authentication database, draft database, media records, publication database, candidate packages, release history, and audit records must survive container replacement and restart.

Terminate TLS before traffic reaches the application and expose Content Studio only through HTTPS. Set `MEMORY_PALACE_ENV=production` so the admin session cookie is marked Secure. Do not publish the container directly on an unencrypted public endpoint.

## Required private configuration

Generate the owner credential material locally with

```bash
python scripts/generate_admin_credentials.py
```

Store the generated values only in the deployment provider's secret or environment-variable manager. Never commit them to the repository.

At minimum, an enabled private Content Studio deployment needs

```text
MEMORY_PALACE_ENV=production
MEMORY_PALACE_ADMIN_ENABLED=true
MEMORY_PALACE_ADMIN_USERNAME=<private value>
MEMORY_PALACE_ADMIN_PASSWORD_HASH=<private value>
MEMORY_PALACE_ADMIN_SESSION_SECRET=<private value>
MEMORY_PALACE_ADMIN_DB=/app/server_data/admin-security.sqlite3
MEMORY_PALACE_ADMIN_DRAFT_DB=/app/server_data/content-studio-drafts.sqlite3
MEMORY_PALACE_ADMIN_MEDIA_DB=/app/server_data/content-studio-media.sqlite3
MEMORY_PALACE_ADMIN_MEDIA_DIR=/app/server_data/content-studio-media
MEMORY_PALACE_ADMIN_PUBLICATION_DB=/app/server_data/content-studio-publication.sqlite3
MEMORY_PALACE_ADMIN_PUBLICATION_DIR=/app/server_data/content-studio-publications
```

Keep controlled publication disabled during the first deployment rehearsal.

```text
MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED=false
MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED=false
MEMORY_PALACE_GITHUB_ALLOW_MERGE=false
```

After authentication, draft persistence, preview, quality checks, and backup restoration have been verified on the deployed service, publication can be enabled separately. GitHub delivery requires its own repository-scoped token. Automated merge remains a third independent gate and should stay disabled until a disposable end-to-end rehearsal has passed.

## Persistent-storage requirement

Do not deploy Content Studio on ephemeral storage without a durable volume or equivalent persistent disk. A container restart must retain the complete `/app/server_data` directory. Back up that directory before enabling GitHub publication and before any platform migration.

## First deployment sequence

1. Deploy the container with `MEMORY_PALACE_ADMIN_ENABLED=false` and verify `/api/health`.
2. Attach persistent `/app/server_data` storage and configure owner credentials.
3. Enable only `MEMORY_PALACE_ADMIN_ENABLED=true` and verify authenticated access, session expiry, logout, audit history, drafts, preview, and recovery snapshots.
4. Run `scripts/smoke_content_studio.py` against the HTTPS deployment.
5. Create a disposable draft and confirm that published student content is unchanged.
6. Enable `MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED=true` while GitHub delivery and merge remain disabled. Create and validate a disposable candidate.
7. Configure a repository-scoped GitHub token and enable `MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED=true`. Submit a disposable candidate to a temporary branch and pull request, then verify exact hash gating and CI.
8. Leave `MEMORY_PALACE_GITHUB_ALLOW_MERGE=false` until the pull-request path has been inspected manually. Enable it only if server-side merging is actually wanted.
9. Rehearse rollback from a disposable release before treating the deployment as production-ready.

The public student site remains served by the existing GitHub Pages workflow. This private service does not replace that deployment.
