from __future__ import annotations
import json,sys,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; AP=ROOT/'content/ap-biology'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
problems=[]
course=read(AP/'course.json'); units={u['unit_id']:u for u in course['units']}
for uid in ('unit-1','unit-2','unit-3','unit-4'):
    if units.get(uid,{}).get('status')!='STUDENT_READY' or units.get(uid,{}).get('student_release',True) is False: problems.append(f'{uid} is not student-ready')
# Later units may be legitimately released by subsequent mainline gates.
manifest=read(AP/'mainline-release-u1-u4.json')
if manifest.get('unit4',{}).get('stage')!='F6' or manifest.get('unit4',{}).get('browser_validation')!='PASS_F6': problems.append('mainline manifest does not record Unit 4 F6 validation')
expected={'canonical_records_units_1_4':737,'guided_journeys':30,'permanent_scenes':232,'challenge_lab_items':51}
if manifest.get('totals')!=expected: problems.append(f"mainline totals {manifest.get('totals')} != {expected}")
u4=read(AP/'unit-4/finalization-f5.json')

u4status=read(AP/'unit-4/status.json')
if u4status.get('pipeline_stage')!='UNIT4_CLASSROOM_BROWSER_VALIDATED_F6' or u4status.get('browser_validation')!='PASS_F6': problems.append('Unit 4 is not F6 validated in current mainline')
if not (u4['canonical_records']==u4['accounted_records']==180 and u4['unaccounted_records']==0 and u4['runtime_memory_objects']==162 and u4['challenge_lab_records']==15 and u4['scope_guard_records']==3): problems.append('Unit 4 F5 accounting mismatch')
main=(ROOT/'backend/main.py').read_text(encoding='utf-8')
if 'v2-apbio-' not in main: problems.append('runtime version marker missing')
try: tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).splitlines()
except Exception:
    ignored={'__pycache__','.pytest_cache','browser_probe','u3_f6_probe','.git'}
    tracked=[str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and not any(part in ignored for part in p.relative_to(ROOT).parts)]
for rel in tracked:
    low=rel.lower(); parts=Path(rel).parts
    if low.endswith(('.pdf','.sqlite3','.sqlite3-shm','.sqlite3-wal','.pyc')): problems.append(f'forbidden tracked artifact: {rel}')
    if any(x in {'__pycache__','.pytest_cache','browser_probe','u3_f6_probe'} for x in parts): problems.append(f'forbidden cache/probe: {rel}')
    if Path(rel).name=='.env': problems.append('forbidden tracked .env')
if problems:
    print('MAINLINE U1-U4 QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('MAINLINE U1-U4 QA PASS'); print(expected)
