# GitHub and Codespaces Setup

The repository is prepared for GitHub Codespaces and GitHub Actions.

## Codespaces

`.devcontainer/devcontainer.json` uses Python 3.12, installs `requirements.txt`, and forwards port 8000. After the Codespace opens, start the application with:

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

## GitHub Actions

`.github/workflows/qa.yml` runs on pushes and pull requests. It verifies:

- the F6.9 authoritative content hashes,
- the 229 / 207 / 9 / 78 expected content counts,
- the Water Atrium reference-journey integrity,
- FastAPI endpoints,
- JavaScript syntax.

A failed content-lock check should be treated as a blocking problem unless the scientific/content source is being intentionally versioned through a reviewed migration.

## Recommended branch workflow

Keep `main` stable. Use focused branches such as:

```text
feature/water-story-ui
feature/review-scheduler
feature/student-auth
feature/progress-database
```

Merge through pull requests after QA passes.

## Secrets and student data

Never commit `.env`, SQLite databases, student accounts, student progress, or deployment credentials. The included `.gitignore` excludes these by default.
