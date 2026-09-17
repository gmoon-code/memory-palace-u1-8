# Content Studio zero-cost rehearsal

This rehearsal is intentionally local-only and requires no paid hosting service, paid plan, cloud disk, billing account, or payment method.

The earlier hosted rehearsal path is not used here. Content Studio runs on the teacher's own computer and binds only to `127.0.0.1`, so another device cannot reach it during this stage.

## Safety state

The local launcher forces all publication controls off regardless of values in the local environment file.

- `MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED=false`
- `MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED=false`
- `MEMORY_PALACE_GITHUB_ALLOW_MERGE=false`

The existing student website remains independent. This rehearsal does not modify GitHub Pages or published AP Biology content.

## Persistent state

All Content Studio state remains in the repository's ignored `server_data` directory on the teacher's computer. SQLite databases, drafts, revisions, snapshots, media staging, audit history, and publication-candidate state survive application restarts as long as that directory is retained.

The credential file `.env.content-studio-local` is ignored by Git. Real passwords, password hashes, and session secrets must never be committed.

## Windows one-click start

The normal Windows workflow is now a double-click.

1. Keep the repository folder on the computer.
2. Make sure a free Python 3.10 or newer installation is available. No paid Python distribution is required.
3. Double-click `Start Content Studio.cmd` in the repository root.

On the first run, the launcher creates an ignored `.venv` virtual environment inside the repository and installs the repository's existing open-source Python dependencies from `requirements.txt`. This initial dependency installation needs an internet connection, but it does not require an account, payment method, hosting plan, API key, or paid service. Later launches reuse the same virtual environment. Dependencies are installed again only when the requirements file changes.

If `.env.content-studio-local` does not exist, the launcher starts the owner setup automatically. It asks for an owner username and a password of at least 12 characters. The password itself is never written to disk. A scrypt password hash and a random session secret are written to the ignored local environment file.

After setup, Content Studio starts only on `127.0.0.1`. The launcher waits for the local server to respond and then opens the default browser to the local admin page. Publication, GitHub delivery, and merging remain forced off in this mode.

Press `Ctrl+C` in the launcher window to stop Content Studio. Double-click `Start Content Studio.cmd` again later to resume with the same local credentials, drafts, revisions, media staging, and SQLite state.

If Python is missing, the Windows launcher stops before creating Content Studio state and explains that Python must be installed. It never installs a paid product or enrolls the computer in a cloud service.

## Command-line local start

The command-line workflow remains available for troubleshooting or non-Windows use. Install the repository's existing Python requirements in a local virtual environment. No commercial service is involved.

Create the owner credentials interactively.

```bash
python scripts/setup_content_studio_local.py
```

Start Content Studio.

```bash
python scripts/run_content_studio_local.py
```

Open the address printed by the launcher, normally `http://127.0.0.1:8000/admin`.

Stop the service with `Ctrl+C`. Starting it again with the same local environment file and `server_data` directory restores the same local Content Studio state.

## Rehearsal verification

The repository QA performs a fully automated local-only rehearsal with temporary credentials. It starts Content Studio on loopback, performs the authenticated read-only deployment smoke test, stops the process, starts it again, repeats the authenticated smoke test, and checks that the local security database retained audit state across the restart.

A separate Windows-launcher QA verifies that the one-click launcher uses only the local virtual environment, local credential file, loopback server, ignored state directory, and the repository's open-source Python dependencies. It also verifies that publication and merge controls remain locked off.

The rehearsal intentionally does not publish content, create GitHub release branches, merge pull requests, expose Content Studio to the public internet, or require a cloud provider.

## Zero-cost rule

Future infrastructure changes for this project must preserve a zero-cost path. A service that requires payment for persistent storage, a paid tier, usage billing, or a payment method is outside this project's deployment plan unless the project owner explicitly changes that rule in the future.
