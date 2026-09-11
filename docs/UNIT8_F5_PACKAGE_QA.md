# Unit 8 F5 Package QA

## Result

**PASS**

This report records the repository-level release checks used immediately before packaging Unit 8 F5.

## Baseline preservation

- F4H baseline ZIP SHA-256: `bedee9a70a3a602ce6320b8456da41625dd526b297af2eb56e124d0e2ab51ad5`
- Units 1–7 content files verified byte-for-byte: **421 / 421**
- Changed Units 1–7 content files: **0**
- Pre-existing Unit 8 content files compared: **80**
- Expected pre-existing Unit 8 content change: `content/ap-biology/unit-8/status.json` only
- Frozen F4 documentation changed: **0**
- Frontend source changed from F4H: **0**
- Backend source changes are limited to the Unit 8 F5 runtime integration in `settings.py`, `content.py`, and `main.py`.

## Final F5 regression

- Python tests: **428 / 428 passing**
- Full GitHub Actions command-sequence probe: **PASS**
- Probe repository drift after cache exclusion: **0 changed / 0 added / 0 removed**
- Deterministic F5 rebuild: **16 checked / 0 changed**
- Unit 8 F5 UI logic: **58 scenes, 18 recalls, 174 scene/viewport checks, 54 recall/viewport checks**

## Packaging exclusions

The final ZIP excludes generated caches and forbidden repository payloads including source PDFs, `.git`, exact `.env`, `.pytest_cache`, `__pycache__`, `.pyc`, `.pyo`, database files, and SQLite files. `.env.example` remains intentionally included.

## Manifest policy

`content/ap-biology/unit-8/unit8-f5-package-manifest.json` hashes every packaged repository file except the manifest itself. The manifest is generated only after this report and the final release documentation are complete.

## Archive assembly

- Packaged repository files: **1,135**
- Directory entries including the repository root: **61**
- Total ZIP entries: **1,196**
- Forbidden packaged artifacts: **0**
- `unzip -t` archive integrity check: **PASS**
- Deterministic ZIP probe: **PASS**, with two independently assembled archives producing identical SHA-256 values before the final documentation hash refresh.

The external `.sha256` companion file records the final archive checksum so the archive does not contain a self-referential checksum.

## Validation boundary

This is the F5 package gate. Unit 8 still requires F6 final classroom/browser-facing validation. No screenshot-level or pixel-level F6 claim is made here.
