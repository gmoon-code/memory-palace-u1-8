from __future__ import annotations

import hashlib
import json
from pathlib import Path

SITE_LOCK_REL = Path('site-release/site-ux1-lock.json')
SITE_REVISION = 'site-ux1'
FROZEN_CONTENT_FILE_COUNT = 527
FROZEN_CONTENT_TREE_SHA256 = '6ae355ca5ef69cbef7f3fc539c66b1ead8120efbf001ebb268e0919bd4235ec2'
CURRICULUM_RUNTIME = 'v2-apbio-0.30.0-u8-f6'


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def content_tree(root: Path) -> tuple[int, str]:
    rows = []
    for path in sorted(p for p in (root / 'content').rglob('*') if p.is_file()):
        rel = path.relative_to(root).as_posix()
        rows.append(f'{rel}\t{sha256(path)}\n')
    return len(rows), hashlib.sha256(''.join(rows).encode('utf-8')).hexdigest()


def load_site_lock(root: Path) -> dict:
    path = root / SITE_LOCK_REL
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def site_lock_is_valid(root: Path, verify_runtime: bool = True) -> bool:
    lock = load_site_lock(root)
    if lock.get('site_revision') != SITE_REVISION:
        return False
    if lock.get('curriculum_runtime_version') != CURRICULUM_RUNTIME:
        return False
    if lock.get('frozen_content_file_count') != FROZEN_CONTENT_FILE_COUNT:
        return False
    if lock.get('frozen_content_tree_sha256') != FROZEN_CONTENT_TREE_SHA256:
        return False
    count, digest = content_tree(root)
    if count != FROZEN_CONTENT_FILE_COUNT or digest != FROZEN_CONTENT_TREE_SHA256:
        return False
    if verify_runtime:
        runtime = lock.get('runtime_file_sha256', {})
        if not isinstance(runtime, dict) or not runtime:
            return False
        for rel, expected in runtime.items():
            path = root / rel
            if not path.is_file() or sha256(path) != expected:
                return False
    return True


def site_runtime_hash_allowed(root: Path, rel: str, current: str | None = None) -> bool:
    if not site_lock_is_valid(root, verify_runtime=False):
        return False
    lock = load_site_lock(root)
    expected = lock.get('runtime_file_sha256', {}).get(rel)
    if expected is None:
        return False
    path = root / rel
    if current is None:
        if not path.is_file():
            return False
        current = sha256(path)
    return current == expected

PACKAGE_MANIFEST_REL = Path('docs/SITE_UX1_PACKAGE_MANIFEST.json')


def is_packaged_file(root: Path, path: Path) -> bool:
    rel = path.relative_to(root)
    parts = set(rel.parts)
    if {'.git', '__pycache__', '.pytest_cache'} & parts:
        return False
    if path.name in {'.env', '.DS_Store', '.gitattributes'}:
        return False
    if path.suffix.lower() in {'.pyc', '.pyo', '.db', '.sqlite', '.sqlite3', '.zip'}:
        return False
    if rel == PACKAGE_MANIFEST_REL:
        return False
    return path.is_file()


def packaged_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob('*') if is_packaged_file(root, p))
