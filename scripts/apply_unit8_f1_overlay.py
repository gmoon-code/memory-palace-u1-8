#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, shutil, tempfile, zipfile, sys

EXPECTED_SHA = "d344f3641dd2949fc6824bc6e7d150b681b72511572669524be22af9984a36ed"
EXPECTED_RUNTIME = "v2-apbio-0.28.0-u7-f6"
OVERLAY_ROOT = Path(__file__).resolve().parents[1]
COPY_DIRS = ["content/ap-biology/unit-8", "docs", "reports"]

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def find_repo_root(root):
    candidates=[]
    for p in root.rglob('START_HERE.md'):
        if (p.parent/'content').is_dir() and (p.parent/'frontend').is_dir() and (p.parent/'tests').is_dir():
            candidates.append(p.parent)
    if len(candidates)!=1:
        raise RuntimeError(f"Expected exactly one Memory Palace repository root, found {len(candidates)}")
    return candidates[0]

def merge_dir(src,dst):
    for p in src.rglob('*'):
        rel=p.relative_to(src); q=dst/rel
        if p.is_dir(): q.mkdir(parents=True,exist_ok=True); continue
        q.parent.mkdir(parents=True,exist_ok=True)
        if q.exists() and q.read_bytes()!=p.read_bytes():
            raise RuntimeError(f"Refusing to overwrite conflicting file: {q}")
        shutil.copy2(p,q)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source-zip',required=True)
    ap.add_argument('--output',required=True)
    ap.add_argument('--allow-unverified-baseline',action='store_true')
    args=ap.parse_args()
    source=Path(args.source_zip); out=Path(args.output)
    actual=sha256(source)
    if actual!=EXPECTED_SHA and not args.allow_unverified_baseline:
        raise RuntimeError(f"Baseline checksum mismatch. Expected {EXPECTED_SHA}, got {actual}. Use --allow-unverified-baseline only after manually confirming the baseline.")
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        with zipfile.ZipFile(source) as z: z.extractall(td)
        repo=find_repo_root(td)
        # validate current runtime when manifest is present
        manifest=repo/'content/ap-biology/mainline-release-u1-u7.json'
        if manifest.exists():
            try:
                data=json.loads(manifest.read_text(encoding='utf-8'))
                txt=json.dumps(data,ensure_ascii=False)
                if EXPECTED_RUNTIME not in txt and not args.allow_unverified_baseline:
                    raise RuntimeError('Baseline manifest does not contain expected runtime '+EXPECTED_RUNTIME)
            except json.JSONDecodeError:
                if not args.allow_unverified_baseline: raise
        for rel in COPY_DIRS:
            src=OVERLAY_ROOT/rel
            if src.exists(): merge_dir(src,repo/rel)
        # copy explicit F1 overlay provenance and apply script into repo docs/scripts
        shutil.copy2(OVERLAY_ROOT/'BASELINE_U1_U7_F6.json', repo/'content/ap-biology/unit-8/BASELINE_U1_U7_F6.json')
        (repo/'scripts').mkdir(exist_ok=True)
        shutil.copy2(Path(__file__), repo/'scripts/apply_unit8_f1_overlay.py')
        # zip repository parent preserving its root folder
        out.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
            for p in sorted(repo.rglob('*')):
                if p.is_file(): z.write(p, Path(repo.name)/p.relative_to(repo))
    print(out)
    print(sha256(out))

if __name__=='__main__': main()
