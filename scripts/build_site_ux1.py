from __future__ import annotations

import json
from pathlib import Path

from site_release_guard import (
    CURRICULUM_RUNTIME,
    FROZEN_CONTENT_FILE_COUNT,
    FROZEN_CONTENT_TREE_SHA256,
    SITE_LOCK_REL,
    SITE_REVISION,
    PACKAGE_MANIFEST_REL,
    content_tree,
    packaged_files,
    sha256,
)

ROOT = Path(__file__).resolve().parents[1]

RUNTIME_PATHS = [
    *sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'backend').glob('*.py')),
    *sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / 'frontend').rglob('*') if p.is_file()),
]

COURSE_COUNTS = {
    'units': 8,
    'guided_journeys': 58,
    'permanent_scenes': 448,
    'quick_recalls': 152,
    'challenge_lab_items': 112,
    'exact_name_review_targets': 887,
    'mixed_discrimination_sets': 220,
    'mixed_discrimination_questions': 600,
}


def main() -> None:
    count, digest = content_tree(ROOT)
    if count != FROZEN_CONTENT_FILE_COUNT or digest != FROZEN_CONTENT_TREE_SHA256:
        raise SystemExit(
            'SITE UX1 BUILD REFUSED: frozen AP Biology content tree drifted '
            f'(files={count}, sha256={digest})'
        )
    runtime = {rel: sha256(ROOT / rel) for rel in RUNTIME_PATHS}
    payload = {
        'schema': 'memory-palace-v2-site-release-1.0',
        'site_revision': SITE_REVISION,
        'release_status': 'SITE_UX1_HARDENED_OVER_FROZEN_U1_U8_F6',
        'curriculum_runtime_version': CURRICULUM_RUNTIME,
        'curriculum_content_changed': False,
        'frozen_content_file_count': count,
        'frozen_content_tree_sha256': digest,
        'course_counts': COURSE_COUNTS,
        'runtime_file_sha256': runtime,
        'browser_screenshot_validation': 'NOT_CLAIMED_SANDBOX_BROWSER_NAVIGATION_BLOCKED',
    }
    out = ROOT / SITE_LOCK_REL
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n', encoding='utf-8')

    package_files = packaged_files(ROOT)
    package_manifest = {
        'schema': 'memory-palace-v2-site-ux1-package-manifest-1.0',
        'site_revision': SITE_REVISION,
        'curriculum_runtime_version': CURRICULUM_RUNTIME,
        'frozen_content_tree_sha256': digest,
        'file_count_excluding_manifest': len(package_files),
        'files': {p.relative_to(ROOT).as_posix(): sha256(p) for p in package_files},
    }
    manifest_path = ROOT / PACKAGE_MANIFEST_REL
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(package_manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print('SITE UX1 LOCK BUILT')
    print(json.dumps({'site_revision': SITE_REVISION, 'runtime_files': len(runtime), 'content_files': count, 'content_tree_sha256': digest, 'package_manifest_files': len(package_files)}, indent=2))


if __name__ == '__main__':
    main()
