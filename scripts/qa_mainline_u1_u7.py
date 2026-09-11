from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from fastapi.testclient import TestClient
from backend.main import app
AP=ROOT/'content'/'ap-biology'
problems=[]
main=json.loads((AP/'mainline-release-u1-u7.json').read_text(encoding='utf-8'))
expected_units=[f'unit-{i}' for i in range(1,8)]
if main.get('units')!=expected_units: problems.append(f"mainline units {main.get('units')} != {expected_units}")
expected_totals={'canonical_records_units_1_7':1306,'guided_journeys':50,'permanent_scenes':390,'challenge_lab_items':99}
if main.get('totals')!=expected_totals: problems.append(f"mainline totals {main.get('totals')} != {expected_totals}")
if main.get('runtime_version')!='v2-apbio-0.28.0-u7-f6': problems.append('mainline runtime version mismatch')
client=TestClient(app)
health=client.get('/api/health').json()
if health.get('version') not in {'v2-apbio-0.28.0-u7-f6','v2-apbio-0.29.0-u8-f5','v2-apbio-0.30.0-u8-f6'}: problems.append(f"health version mismatch {health.get('version')}")
course=client.get('/api/course').json()['units']
ready=[u['unit_id'] for u in course if u.get('status')=='STUDENT_READY']
if ready[:7]!=expected_units or any(uid not in expected_units+['unit-8'] for uid in ready): problems.append(f'student-ready units incompatible with frozen U1-U7 mainline: {ready}')
expected_journeys={'unit-1':9,'unit-2':7,'unit-3':7,'unit-4':7,'unit-5':8,'unit-6':6,'unit-7':6}
for uid,n in expected_journeys.items():
    got=len(client.get(f'/api/units/{uid}/journeys').json()['guided_journeys'])
    if got!=n: problems.append(f'{uid} journey count {got} != {n}')
u7=client.get('/api/units/unit-7').json()
if u7.get('status')!='STUDENT_READY' or u7.get('runtime_memory_objects')!=174 or u7.get('application_challenges')!=16: problems.append('Unit 7 student-ready runtime summary mismatch')
if client.get('/api/units/unit-7/review-manifest').json().get('target_count')!=94: problems.append('Unit 7 Review target count mismatch')
if client.get('/api/units/unit-7/mixed-discrimination').json().get('question_count')!=102: problems.append('Unit 7 mixed question count mismatch')
if client.get('/api/units/unit-7/scope-guards').json().get('guard_count')!=25: problems.append('Unit 7 scope guard count mismatch')
if client.get('/api/units/unit-7/finalization').json().get('unaccounted_records')!=0: problems.append('Unit 7 finalization zero-loss mismatch')
if problems:
    print('MAINLINE U1-U7 F6 QA FAIL'); print('\n'.join(f'- {p}' for p in problems)); sys.exit(1)
print('MAINLINE U1-U7 F6 QA PASS')
print(json.dumps({'units':7,'canonical_records':1306,'guided_journeys':50,'permanent_scenes':390,'challenge_lab_items':99,'runtime_version':'v2-apbio-0.28.0-u7-f6'},indent=2))
