from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; AP=ROOT/'content/ap-biology'
problems=[]
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
course=read(AP/'course.json'); units={u['unit_id']:u for u in course['units']}
for i in range(1,7):
    u=units[f'unit-{i}']
    if u.get('status')!='STUDENT_READY': problems.append(f'unit-{i} is not student-ready')
    if i>=2 and u.get('student_release') is not True: problems.append(f'unit-{i} student_release flag is not true')
main=read(AP/'mainline-release-u1-u6.json')
if main.get('schema')!='memory-palace-v2-mainline-u1-u6-f6-1.0': problems.append('mainline schema is not Unit 6 F6')
if main.get('release_status')!='STUDENT_READY_UNITS_1_6_UNIT6_F6_VALIDATED': problems.append('mainline release status is not Unit 6 F6 validated')
if main.get('units')!=[f'unit-{i}' for i in range(1,7)]: problems.append('mainline unit list mismatch')
expected={'canonical_records_units_1_6':1091,'guided_journeys':44,'permanent_scenes':335,'challenge_lab_items':83}
if main.get('totals')!=expected: problems.append(f"mainline totals {main.get('totals')} != {expected}")
u6=AP/'unit-6'
for name in ['memory-objects-f5.json','application-lab.json','review-manifest-f5.json','mixed-discrimination-f5.json','scope-guards-f5.json','finalization-f5.json','journeys-f5.json','status-f5.json','content-lock-f5.json','f5-release-manifest.json','ux-validation-f6.json','status-f6.json','content-lock-f6.json','f6-release-manifest.json']:
    if not (u6/name).exists(): problems.append(f'missing Unit 6 release artifact {name}')
status=read(u6/'status.json')
if status.get('pipeline_stage')!='UNIT6_CLASSROOM_BROWSER_VALIDATED_F6' or status.get('browser_validation')!='PASS_F6': problems.append('Unit 6 current status is not F6 validated')
if main.get('unit6',{}).get('stage')!='F6' or main.get('unit6',{}).get('browser_validation')!='PASS_F6': problems.append('mainline Unit 6 manifest is not F6 validated')
if problems:
    print('MAINLINE U1-U6 QA FAIL'); print('\n'.join(f'- {x}' for x in problems)); sys.exit(1)
print('MAINLINE U1-U6 QA PASS')
print(json.dumps(expected,indent=2))
