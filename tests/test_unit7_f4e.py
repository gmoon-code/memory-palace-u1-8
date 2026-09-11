import json,re,hashlib
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app
ROOT=Path(__file__).resolve().parents[1]; U7=ROOT/'content/ap-biology/unit-7'
def read(p): return json.loads(Path(p).read_text())
def test_f4e_journey5_accounting():
 j=read(U7/'journeys/U7-J5.json'); assert j['scene_count']==9 and j['checkpoint_count']==3; assert len({k for s in j['scenes'] for k in s['object_ids']})==25; assert all(len(re.findall(r"\b[\w’′'-]+\b",' '.join(s['story_paragraphs'])))>=450 for s in j['scenes'])
def test_f4e_prior_journeys_frozen():
 lock=read(U7/'content-lock-f4e.json')
 for rel,meta in lock['prior_narrative_protection'].items():
  p=ROOT/rel; assert p.stat().st_size==meta['bytes']; assert hashlib.sha256(p.read_bytes()).hexdigest()==meta['sha256']
def test_f4e_runtime_hidden():
 c=TestClient(app); u=c.get('/api/units/unit-7').json(); assert u['status'] in {'F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','STUDENT_READY'}
 if u['status']=='STUDENT_READY': assert u['student_release'] is True and len(c.get('/api/units/unit-7/journeys').json()['guided_journeys'])==6
 else: assert u['student_release'] is False and c.get('/api/units/unit-7/journeys').json()['guided_journeys']==[]
 for jid in ['U7-J1','U7-J2','U7-J3','U7-J4','U7-J5']: assert c.get(f'/api/units/unit-7/journeys/{jid}').status_code==(200 if u['status']=='STUDENT_READY' else 404)
