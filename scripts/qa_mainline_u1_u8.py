import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from fastapi.testclient import TestClient
from backend.main import app
AP=ROOT/'content/ap-biology'
client=TestClient(app)
problems=[]
main=json.loads((AP/'mainline-release-u1-u8.json').read_text(encoding='utf-8'))
expected_units=[f'unit-{i}' for i in range(1,9)]
if main.get('units')!=expected_units: problems.append(f"unit list mismatch {main.get('units')}")
if main.get('runtime_version')!='v2-apbio-0.30.0-u8-f6': problems.append('mainline runtime version mismatch')
if main.get('totals')!={'canonical_records_units_1_8':1561,'guided_journeys':58,'permanent_scenes':448,'challenge_lab_items':112}: problems.append(f"mainline totals mismatch {main.get('totals')}")
health=client.get('/api/health').json()
if health.get('version')!='v2-apbio-0.30.0-u8-f6': problems.append(f"health version mismatch {health.get('version')}")
course=client.get('/api/course').json()
ready=[u['unit_id'] for u in course['units'] if u.get('status')=='STUDENT_READY' and u.get('student_release',True)]
if ready!=expected_units: problems.append(f'student-ready units {ready} != {expected_units}')
for i in range(1,9):
    uid=f'unit-{i}'
    unit=client.get(f'/api/units/{uid}')
    if unit.status_code!=200: problems.append(f'{uid} summary unavailable')
    js=client.get(f'/api/units/{uid}/journeys').json().get('guided_journeys',[])
    if len(js)==0: problems.append(f'{uid} has no released journeys')
if problems:
    print('UNITS 1-8 MAINLINE QA FAIL')
    print('\n'.join('- '+p for p in problems))
    sys.exit(1)
print('UNITS 1-8 MAINLINE QA PASS')
print(json.dumps({'units':8,'canonical_records':1561,'guided_journeys':58,'permanent_scenes':448,'challenge_lab_items':112,'runtime_version':'v2-apbio-0.30.0-u8-f6'},indent=2))
