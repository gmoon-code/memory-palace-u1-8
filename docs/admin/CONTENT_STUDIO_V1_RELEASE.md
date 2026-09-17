# Content Studio v1.0.0 Stable Release

Content Studio v1.0.0 promotes the fully validated RC1 into the stable local administrator release without changing the administrator runtime, AP Biology curriculum, or student-facing application.

The stable runtime baseline is production `main` commit `562f09e1d72f3bceaa3f97cf3b19d7683c864877`, created by merging the exact approved RC1 head `0fef459bde6fb913f186c91df8f5492f58f2fa9b`. Both resolve to tree `53e7182c271f0a82a473e527b0f2c77c16a4ae85`. The frozen Content Studio implementation remains `cdf4bb2a1ea91415dd1634323ac5ab40ccba863f` with implementation tree `133a3bc9b00c2149662d4e6dba8517f0706b585c`.

## Validation record

Before promotion, PR-specific Memory Palace QA run 353 passed on the exact RC1 head. After merge, Memory Palace QA run 354 passed on the stable baseline commit, and GitHub Pages build/deployment run 98 passed on the same commit. The integration changed no files under `content/`, `frontend/index.html`, `frontend/css/`, or `frontend/js/`.

The v1.0.0 promotion is release metadata only. The stable-release QA rejects runtime changes after the validated merge commit and verifies the locked runtime Git objects, merge-parent identities, publication-off defaults, student invariants, and zero-cost requirement.

## Operating model

Content Studio remains a local administrator application. The supported launcher binds to `127.0.0.1`, private credentials and `server_data` stay outside Git, and the one-click backup, restore, repair, and updater tools remain part of the supported local workflow.

The repository defaults remain closed. `MEMORY_PALACE_ADMIN_ENABLED`, `MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED`, `MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED`, and `MEMORY_PALACE_GITHUB_ALLOW_MERGE` are all `false` until deliberately changed by the owner in an appropriate environment.

The strict zero-cost requirement remains part of the stable release contract. The supported local workflow requires no paid hosting, paid persistent storage, usage billing, subscription, or payment method.

## Administrator capability baseline

The stable release includes the integrated administrator workspaces for Dashboard, Course Map, Units, Journeys, Scenes, Stories, Characters, Locations, Complete Story Replacement, Concept Library, Memory Objects, Question Bank, Review System, Challenge Lab, Media Library, Student Preview, Content Health, Draft Workspace, Version History, Import and Export, Publishing, Settings, Security and Audit, and the capability audit. The shared workflow remains Browse → Edit → Draft → Preview → Validate → Publish → Recover.

## Recovery baseline

The validated local recovery model includes persistent draft/revision storage, recovery snapshots, local backup and restore archives with integrity checks, Health Check and Repair, and the safe local updater with rollback protection. Publication stays a separate explicit action and remains disabled by default.

`release/content-studio/v1.0.0.json` is the machine-readable stable-release record. `release/content-studio/v1.0.0-rc1.json` remains preserved as historical RC1 evidence.
