from pathlib import Path
import json, hashlib, sys
ROOT=Path(__file__).resolve().parents[1]
lock=json.loads((ROOT/'content/ap-biology/unit-1/content-lock.json').read_text())
failed=[]
for rel,meta in lock['files'].items():
    p=ROOT/rel
    actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
    if actual!=meta['sha256']: failed.append((rel,meta['sha256'],actual))
if failed:
    print('CONTENT LOCK FAILED')
    for x in failed: print(*x)
    sys.exit(1)
print('Content lock PASS')
print(lock['expected_counts'])
