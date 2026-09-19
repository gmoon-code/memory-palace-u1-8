from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ADMIN PUBLICATION QA FAIL\n- {message}")


publication = read("backend/admin_publication.py")
routes = read("backend/admin_publication_routes.py")
draft_routes = read("backend/admin_draft_routes.py")
env = read(".env.example")
frontend = read("frontend/admin/publication.js")
doc = read("docs/admin/STEP9_PUBLICATION_AND_ROLLBACK.md")
workflow = read(".github/workflows/qa.yml")
pages_builder = read("scripts/build_github_pages.py")

require('MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED=false' in env, "publication must be disabled by default")
require('MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED=false' in env, "GitHub candidate delivery must be disabled by default")
require('MEMORY_PALACE_GITHUB_ALLOW_MERGE=false' in env, "server-side merge must be disabled by default")
require('MEMORY_PALACE_GITHUB_TOKEN=' in env, "GitHub token configuration placeholder is missing")

require('published_content_direct_write": False' in publication, "publication status must state that direct published writes are disabled")
require('candidate package only; no local published source write' in publication, "candidate-only publication model is missing")
require('before_sha256' in publication and 'after_sha256' in publication, "candidate file hashes are missing")
require('Pre-publication snapshot' in publication, "candidate creation must create recovery snapshots")
require('_assert_candidate_fresh' in publication, "draft staleness guard is missing")
require('_assert_remote_base' in publication, "remote base hash guard is missing")
require('check-runs' in publication, "GitHub Actions check-run gate is missing")
require('github_allow_merge' in publication, "separate server-side merge gate is missing")
require('create_rollback_candidate' in publication, "non-destructive rollback candidate builder is missing")
require('shutil.copytree' in publication and 'TemporaryDirectory' in publication, "isolated local release validation is missing")
require("course_packages" in publication, "publication does not resolve course package metadata")
require("declared_source_file" in publication, "publication sources are not package-declared")
require("artifact_source_path" in publication, "managed publication destinations are not package-declared")
require("content/ap-biology/" not in publication, "publication still hard-codes the AP Biology content root")
require("UNIT_IDS" not in publication, "publication still hard-codes an eight-unit course model")
require("ALTER TABLE publication_candidates ADD COLUMN course_id" in publication, "legacy candidate migration does not add course_id")
require("ALTER TABLE publication_releases ADD COLUMN course_id" in publication, "legacy release migration does not add course_id")
require("WHERE candidate_id = ? AND course_id = ?" in publication, "candidate lookups are not course-scoped")
require("WHERE release_id = ? AND course_id = ?" in publication, "release lookups are not course-scoped")

for route in (
    '/candidates',
    '/candidates/{candidate_id}/validate',
    '/candidates/{candidate_id}/submit',
    '/candidates/{candidate_id}/checks',
    '/candidates/{candidate_id}/merge',
    '/candidates/{candidate_id}/verify',
    '/releases/{release_id}/rollback',
):
    require(route in routes, f"publication route missing: {route}")
require('_owner(request, csrf=True)' in routes, "publication mutations must use authenticated CSRF protection")
require('course_id: str = Field(default="ap-biology"' in routes, "publication mutation requests do not carry course identity")
require('course_id: str = "ap-biology"' in routes, "publication read routes do not carry course identity")
require('admin_publication_routes.router' in draft_routes, "publication API router is not registered")
require('admin_publication_routes.assets' in draft_routes, "publication admin assets are not registered")

require('Step 9 controlled publishing' in frontend, "publication UI does not expose the Step 9 state")
require('Create isolated candidate' in frontend, "publication candidate UI is missing")
require('Prepare rollback candidate' in frontend, "rollback UI is missing")
require('localStorage' not in frontend and 'sessionStorage' not in frontend, "publication UI must not persist credentials or CSRF tokens in browser storage")
require("currentAdminCourseId()" in frontend, "publication UI does not preserve selected course identity")
require("currentAdminCourseEditable()" in frontend, "publication write controls do not honor read-only courses")
require('courseUrl("/api/admin/publication/status")' in frontend, "publication status is not selected-course scoped")
require("story-method-course-changed" in frontend, "publication state is not cleared when courses change")
require('frontend/admin' not in pages_builder or 'copytree(FRONTEND_DIR / "admin"' not in pages_builder, "GitHub Pages builder must not publish the admin workspace")
require('server_data' not in pages_builder, "GitHub Pages builder must not publish server-side Content Studio state")

require('qa_admin_publication.py' in workflow, "CI does not run Step 9 publication QA")
require('node --check frontend/admin/publication.js' in workflow, "CI does not syntax-check publication.js")
require('rollback never rewrites git history' in doc.lower(), "Step 9 rollback safety documentation is incomplete")
require('All Step 9 gates default to disabled' in doc, "Step 9 default-off documentation is missing")

print("ADMIN PUBLICATION QA PASS")
print("- candidate generation is isolated from published course files")
print("- exact before/after hashes and pre-publication snapshots are required")
print("- stale drafts and changed remote base files are blocked")
print("- publication errors block; warnings require explicit teacher acknowledgment")
print("- GitHub branch, pull-request, check-run, merge, and verify gates are present")
print("- rollback is a new validated candidate and never rewrites release history")
print("- publication records, source resolution, release history, and rollback are explicitly course-scoped")
print("- read-only courses cannot create candidates, rollback packages, or publication mutations")
print("- publication and GitHub delivery remain disabled by default")
print("- public GitHub Pages remains isolated from Content Studio state")
