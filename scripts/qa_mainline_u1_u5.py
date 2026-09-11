from __future__ import annotations
import json,sys,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; AP=ROOT/'content/ap-biology'
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
problems=[]
course=read(AP/'course.json'); units={u['unit_id']:u for u in course['units']}
for uid in ('unit-1','unit-2','unit-3','unit-4','unit-5'):
    if units.get(uid,{}).get('status')!='STUDENT_READY' or units.get(uid,{}).get('student_release',True) is False: problems.append(f'{uid} is not student-ready')
# Later units may be legitimately released by subsequent mainline gates.
manifest=read(AP/'mainline-release-u1-u5.json')
if manifest.get('unit5',{}).get('stage')!='F6' or manifest.get('unit5',{}).get('student_release') is not True or manifest.get('unit5',{}).get('browser_validation')!='PASS_F6': problems.append('mainline manifest does not record Unit 5 F6 validated student release')
expected={'canonical_records_units_1_5':889,'guided_journeys':38,'permanent_scenes':282,'challenge_lab_items':67}
if manifest.get('totals')!=expected: problems.append(f"mainline totals {manifest.get('totals')} != {expected}")
u5=read(AP/'unit-5/finalization-f5.json'); u5status=read(AP/'unit-5/status.json')
if u5status.get('pipeline_stage')!='UNIT5_CLASSROOM_BROWSER_VALIDATED_F6' or u5status.get('browser_validation')!='PASS_F6' or u5status.get('student_release') is not True or u5status.get('preview_release') is not False: problems.append('Unit 5 is not browser/classroom validated F6 in current mainline')
if not (u5['canonical_records']==u5['accounted_records']==152 and u5['unaccounted_records']==0 and u5['runtime_memory_objects']==131 and u5['challenge_lab_records']==16 and u5['scope_guard_records']==5): problems.append('Unit 5 F5 accounting mismatch')
if u5.get('exact_name_review_targets')!=130 or u5.get('mixed_discrimination_sets')!=32 or u5.get('mixed_discrimination_questions')!=79: problems.append('Unit 5 review/discrimination accounting mismatch')
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
    print('MAINLINE U1-U5 QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('MAINLINE U1-U5 QA PASS'); print(expected)
