# Site UX1 Package QA

## Packaging contract

The deterministic release builder packages the repository beneath a single `memory-palace-v2/` root. It excludes `.git`, Python and pytest caches, compiled Python files, exact `.env`, database files, temporary ZIP files, and the generated package manifest from its own hash list.

The packaged file list and SHA-256 values are recorded in `docs/SITE_UX1_PACKAGE_MANIFEST.json`. The adjacent release checksum file is intentionally kept outside the ZIP so the archive does not contain a circular checksum dependency.

## Required checks before publication

The frozen content tree must remain exactly 527 files with SHA-256 `6ae355ca5ef69cbef7f3fc539c66b1ead8120efbf001ebb268e0919bd4235ec2`.

The complete historical and current QA workflow must pass. The global Site UX gate, contrast gate, live HTTP gate, Python tests, JavaScript syntax checks, and Python compilation must pass. A clean Git simulation must finish with no tracked-file drift. Two independently produced release archives must be byte-for-byte identical. The final ZIP must pass archive integrity checking and contain no prohibited packaged artifacts.

## Visual-validation boundary

Chromium screenshot or pixel-level validation is not represented as complete. The sandbox prevents Chromium from completing local navigation, so the package records that limitation explicitly while retaining the full functional and semantic validation suite.
