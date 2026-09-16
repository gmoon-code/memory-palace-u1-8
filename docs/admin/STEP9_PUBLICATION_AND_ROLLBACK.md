# Content Studio Step 9

## Controlled publication, release history, and rollback

Step 9 connects the protected Content Studio working-copy system to a release workflow without giving browser editing code a direct path to the published AP Biology files.

The student release remains authoritative until an owner deliberately creates a candidate, validates it, submits it through the configured GitHub repository, and verifies that the configured publication branch contains the exact candidate hashes.

## Safety boundary

Step 9 keeps three layers separate.

1. Published AP Biology source files remain under `content/ap-biology`.
2. Teacher drafts, revisions, snapshots, media staging, and Content Studio state remain under server-side storage.
3. Publication candidates are immutable before/after packages under the configured Step 9 publication directory.

Creating a candidate does not modify any published course file. Candidate creation reads the current source records, applies selected working-copy changes in memory, writes before and after copies into the isolated publication package, records SHA-256 hashes, and creates a named pre-publication snapshot for every included working copy.

## Release sequence

The teacher workflow is

`Edit → Save Draft → Student Preview → Content Health → Review Dependencies → Review Changes → Create Candidate → Validate Candidate → Submit GitHub Candidate → GitHub Actions → Merge → Verify Release`

Publication-blocking Step 8 errors cannot be acknowledged away. Teacher-review warnings can enter a candidate only after the owner explicitly confirms that they were reviewed.

Each candidate stores the exact draft version and payload fingerprint used to create it. Validation or submission stops if any included draft changed afterward.

## Local release validation

The candidate package is overlaid onto a temporary copy of the repository. Step 9 runs a fixed release-validation command set there. The temporary validation tree is discarded afterward. The real repository working tree and the published source files are not rewritten by this process.

The local release gate currently checks the AP Biology content lock, the Units 1–8 mainline, global student UI logic, contrast, the Python regression suite, and Python compilation. GitHub Actions remains the complete external regression gate before merge.

## GitHub publication

GitHub delivery is a separate server configuration gate. When enabled, Step 9 verifies that every affected file on the configured base branch still matches the candidate's captured before hash. If any source changed after candidate creation, submission stops.

A successful submission creates

- Git blobs for the candidate after files
- a tree based on the current configured base branch
- a candidate commit
- a `content-studio/candidate-...` branch
- a pull request back to the configured publication branch

The repository's existing push and pull-request QA then runs against the candidate branch.

Server-side merge is disabled independently by default. When enabled, Content Studio permits merge only after GitHub check runs for the exact candidate commit are complete and successful. A teacher can leave server-side merge disabled and review or merge the pull request in GitHub.

## Release verification

A merge is not treated as a recorded Content Studio release until verification succeeds. Verification re-downloads each affected file from the configured publication branch and compares its SHA-256 hash with the candidate after hash.

After exact verification, Step 9

- creates an immutable release record
- records the candidate and GitHub merge information
- archives included working copies only when they still match the exact candidate versions
- clears server-side catalog and quality caches

This protects newer draft work from being archived by an older candidate.

## Rollback

Rollback never rewrites Git history and never force-resets the publication branch.

A rollback action creates a new candidate whose expected before files are the verified release files and whose after files are the pre-release copies captured in the original candidate. That rollback candidate must pass the same local validation, GitHub branch, pull-request, check-run, merge, and verification process as a forward release.

If the live publication branch has moved away from the release being rolled back, the before-hash check blocks the rollback candidate from overwriting newer work.

## Supported publication destinations

Step 9 can publish current source-backed Unit, Journey, Scene, Location, Character, Concept, Memory Object, Question Bank, Review System, mixed-discrimination, and Challenge Lab records when the current student runtime has an explicit JSON destination for the edited field.

New proposals are currently supported for Challenge Lab items, mixed-discrimination question sets, delayed-review questions, and questions that explicitly target an existing mixed-discrimination set. Standalone teacher-created questions without a student-runtime destination stay safely in the draft system and are reported as unsupported for publication.

Staged media remains private server-side material. Step 9 does not copy staged media into the public student release until a separate runtime-supported asset publication mapping exists.

## Configuration

All Step 9 gates default to disabled.

```text
MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED=false
MEMORY_PALACE_ADMIN_PUBLICATION_DB=server_data/content-studio-publication.sqlite3
MEMORY_PALACE_ADMIN_PUBLICATION_DIR=server_data/content-studio-publications
MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED=false
MEMORY_PALACE_GITHUB_REPOSITORY=gmoon-code/memory-palace-u1-8
MEMORY_PALACE_GITHUB_TOKEN=
MEMORY_PALACE_GITHUB_BASE_BRANCH=main
MEMORY_PALACE_GITHUB_ALLOW_MERGE=false
MEMORY_PALACE_GITHUB_API_URL=https://api.github.com
```

No real GitHub credential belongs in the repository. The deployment environment supplies credentials.

## Public student-site isolation

The static GitHub Pages builder continues to exclude `frontend/admin`, all `server_data`, publication databases, draft databases, candidate packages, audit records, and credentials. The student Pages artifact remains independent from Content Studio.

## Step 9 acceptance conditions

Step 9 is complete only when automated QA verifies that

- publication is disabled by default
- mutating publication endpoints require owner authentication and CSRF
- candidate creation leaves published AP Biology files byte-for-byte unchanged
- candidate before and after hashes are recorded
- pre-publication draft snapshots are created
- stale draft candidates are rejected
- teacher-review warnings require explicit acknowledgment
- blocking errors cannot enter a candidate
- GitHub submission checks remote base hashes before creating a branch or pull request
- server-side merge is separately gated and requires successful checks
- release verification compares exact remote hashes
- rollback creates a new candidate and never rewrites source history
- Content Studio files remain absent from the GitHub Pages student artifact
- all existing Unit 1–8 and student-runtime regressions still pass
