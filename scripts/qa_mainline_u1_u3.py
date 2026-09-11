from __future__ import annotations
import json, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
AP=ROOT/'content'/'ap-biology'

def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))

problems=[]
course=read(AP/'course.json')
units={u['unit_id']:u for u in course['units']}
for uid in ('unit-1','unit-2','unit-3'):
    if units.get(uid,{}).get('status')!='STUDENT_READY':
        problems.append(f'{uid} is not STUDENT_READY')
# Later units may be legitimately released by subsequent mainline gates.

# Unit 4 may now be either in development or legitimately released by a later mainline gate.

manifest=read(AP/'mainline-release-u1-u3.json')
expected={'canonical_records_units_1_3':557,'guided_journeys':23,'permanent_scenes':181,'challenge_lab_items':36}
if manifest.get('totals')!=expected:
    problems.append(f"mainline totals changed: {manifest.get('totals')} != {expected}")

u1=read(AP/'unit-1'/'v2-release-manifest.json')
u2=read(AP/'unit-2'/'finalization-f5.json')
u3=read(AP/'unit-3'/'finalization-f5.json')
actual={
 'canonical_records_units_1_3':u1['canonical_records']+u2['canonical_records']+u3['canonical_records'],
 'guided_journeys':u1['journeys']+u2['guided_journeys']+u3['guided_journeys'],
 'permanent_scenes':u1['scenes']+u2['permanent_loci']+u3['permanent_loci'],
 'challenge_lab_items':read(AP/'unit-1'/'application-lab.json')['challenge_count']+read(AP/'unit-2'/'application-lab.json')['challenge_count']+read(AP/'unit-3'/'application-lab.json')['challenge_count'],
}
if actual!=expected:
    problems.append(f'integrated content totals changed: {actual} != {expected}')
if u2['unaccounted_records']!=0 or u3['unaccounted_records']!=0:
    problems.append('Unit 2 or Unit 3 has unaccounted canonical records')

main=(ROOT/'backend'/'main.py').read_text(encoding='utf-8')
if 'v2-apbio-' not in main:
    problems.append('backend runtime version marker missing')

# Packaging safety checks should inspect repository-tracked source, not ephemeral caches
# created by Python while QA itself is running. Final release packaging separately removes caches.
import subprocess
try:
    tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).splitlines()
except Exception:
    ignored={'__pycache__','.pytest_cache','browser_probe','u3_f6_probe','.git'}
    tracked=[str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and not any(part in ignored for part in p.relative_to(ROOT).parts)]
for rel in tracked:
    low=rel.lower()
    if low.endswith(('.pdf','.sqlite3','.sqlite3-shm','.sqlite3-wal','.pyc')):
        problems.append(f'forbidden tracked artifact: {rel}')
    parts=Path(rel).parts
    if any(part in {'__pycache__','.pytest_cache','browser_probe','u3_f6_probe'} for part in parts):
        problems.append(f'forbidden tracked cache/probe artifact: {rel}')
    if Path(rel).name=='.env':
        problems.append('forbidden tracked secret file: .env')

if problems:
    print('MAINLINE U1-U3 QA FAIL')
    print('\n'.join(f'- {p}' for p in problems))
    sys.exit(1)
print('MAINLINE U1-U3 QA PASS')
print(expected)
