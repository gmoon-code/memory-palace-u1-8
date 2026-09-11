from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from site_release_guard import PACKAGE_MANIFEST_REL, packaged_files, sha256, site_lock_is_valid

ROOT = Path(__file__).resolve().parents[1]
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def build(output: Path) -> str:
    if not site_lock_is_valid(ROOT):
        raise SystemExit('SITE UX1 RELEASE REFUSED: site lock or frozen curriculum verification failed')
    manifest_path = ROOT / PACKAGE_MANIFEST_REL
    if not manifest_path.exists():
        raise SystemExit('SITE UX1 RELEASE REFUSED: package manifest is missing; run scripts/build_site_ux1.py first')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    files = packaged_files(ROOT)
    current = {p.relative_to(ROOT).as_posix(): sha256(p) for p in files}
    if current != manifest.get('files'):
        missing = sorted(set(manifest.get('files', {})) - set(current))
        added = sorted(set(current) - set(manifest.get('files', {})))
        changed = sorted(k for k in set(current) & set(manifest.get('files', {})) if current[k] != manifest['files'][k])
        raise SystemExit(f'SITE UX1 RELEASE REFUSED: package manifest drifted; missing={missing[:5]} added={added[:5]} changed={changed[:5]}')

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        output.unlink()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        # The manifest is included even though it is excluded from its own hash list.
        archive_files = files + [manifest_path]
        for path in sorted(archive_files, key=lambda p: p.relative_to(ROOT).as_posix()):
            rel = path.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(f'memory-palace-v2/{rel}', date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (0o100644 & 0xFFFF) << 16
            info.flag_bits |= 0x800
            zf.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    print('SITE UX1 RELEASE ZIP BUILT')
    print(json.dumps({'output': str(output), 'file_entries': len(files)+1, 'sha256': digest}, indent=2))
    return digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    build(Path(args.output).resolve())


if __name__ == '__main__':
    main()
