import json
import re
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app

ROOT = Path(__file__).resolve().parents[1]
U8 = ROOT / 'content' / 'ap-biology' / 'unit-8'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def test_unit8_f4b_journey2_accounting_and_boundary():
    j = read(U8 / 'journeys/U8-J2.json')
    assert j['palace_id'] == 'U8-J2'
    assert j['scene_count'] == 9 and len(j['scenes']) == 9
    assert j['checkpoint_count'] == 3
    assert j['student_release'] == 'DEVELOPER_PREVIEW_F4B'
    assert j['preview_release'] is True
    assert [s['locus_id'] for s in j['scenes']] == [f'U8-L{i:02d}' for i in range(13, 22)]
    ids = [kid for s in j['scenes'] for kid in s['object_ids']]
    assert len(ids) == 47 and len(set(ids)) == 47


def test_unit8_f4b_prose_is_substantive_spatial_and_continuous():
    j = read(U8 / 'journeys/U8-J2.json')
    continuity = j['scenes'][0]['continuity_object']
    assert j['guide']['name'] == 'Dr. Mira Sen'
    for s in j['scenes']:
        prose = ' '.join(s['story_paragraphs'])
        assert len(re.findall(r"\b[\w’′'-]+\b", prose)) >= 450
        assert len(s['story_paragraphs']) >= 6
        opening = s['story_paragraphs'][0].casefold()
        assert 'left' in opening and ('ahead' in opening or 'center' in opening) and 'right' in opening
        assert len(s['cast']) >= 5
        assert any(c['name'] == 'Dr. Mira Sen' for c in s['cast'])
        assert any(c['name'] == 'Transparent energy-matter ledger' for c in s['cast'])
        assert s['continuity_object'] == continuity
        assert '—' not in prose and ':' not in prose
        lower = prose.casefold()
        for meta in ['the ppt states', 'the ced says', 'the course requires', 'locked definition', 'source material shows', 'teacher enrichment', 'pipeline language']:
            assert meta not in lower


def test_unit8_f4b_exact_targets_and_story_beat_science_match_locks():
    canon = {r['Knowledge ID']: r for r in read(U8 / 'canonical-catalog.json')}
    briefs = {b['locus_id']: b for b in read(U8 / 'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id'] == 'U8-J2'}
    j = read(U8 / 'journeys/U8-J2.json')
    exact = 0
    for s in j['scenes']:
        text = ' '.join(s['story_paragraphs']).casefold().replace('**', '')
        assert s['object_ids'] == briefs[s['locus_id']]['knowledge_ids']
        for beat in s['story_beats']:
            assert beat['science'] == canon[beat['object_id']]['Canonical Verified Statement']
            if beat['exact_name']:
                exact += 1
                variants = [beat['term'].casefold()]
                if '/' in beat['term']:
                    variants.extend(x.strip().casefold() for x in beat['term'].split('/'))
                assert any(v in text for v in variants)
    assert exact == 24


def test_unit8_f4b_high_risk_ecology_distinctions_are_explicit():
    j = read(U8 / 'journeys/U8-J2.json')
    text = ' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**', '')
    phrases = [
        'absolute metabolic rate generally rises with body size',
        'mass-specific metabolic rate generally falls as body size increases',
        'an ecosystem includes a biological community and the abiotic environment',
        'energy can be transferred or transformed, but it is not created or destroyed',
        'energy flows through ecosystems while matter and nutrients cycle',
        'energy ultimately leaves largely as heat',
        'the reaction transforms energy from chemical sources',
        'it does not create energy',
        'arrows conventionally point from resource or prey toward the consumer',
        'npp = gpp − r',
        'primary production is the rate at which autotrophs convert energy and inorganic carbon into organic matter',
        'about ten percent is a useful average rule of thumb',
        'not a fixed law',
    ]
    for phrase in phrases:
        assert phrase in text


def test_unit8_f4b_only_three_first_exposure_recalls():
    j = read(U8 / 'journeys/U8-J2.json')
    cps = [s for s in j['scenes'] if s['checkpoint']]
    assert [s['locus_id'] for s in cps] == ['U8-L16', 'U8-L20', 'U8-L21']
    assert cps[0]['checkpoint_prompt'].startswith('Without looking back, identify or explain First law of thermodynamics')
    assert cps[1]['checkpoint_prompt'].startswith('Without looking back, identify or explain Net primary production')
    assert cps[2]['checkpoint_prompt'].startswith('Without looking back, identify or explain Trophic transfer efficiency')


def test_unit8_f4b_journey1_remains_frozen_and_preview_hidden():
    j1 = read(U8 / 'journeys/U8-J1.json')
    assert j1['scene_count'] == 12
    assert j1['checkpoint_count'] == 2
    client = TestClient(app)
    unit = client.get('/api/units/unit-8').json()
    if unit['status'] == 'STUDENT_READY':
        # F5 may expose the frozen F4 journey artifacts through the student runtime.
        assert unit['student_release'] is True and unit['preview_release'] is False
        assert unit['pipeline_stage'] in {'UNIT8_FINALIZED_F5','UNIT8_CLASSROOM_BROWSER_VALIDATED_F6'}
        assert unit['journey_count'] == 8 and unit['scene_count'] == 58
        assert len(client.get('/api/units/unit-8/journeys').json()['guided_journeys']) == 8
        for jid in [f'U8-J{i}' for i in range(1, 9)]:
            assert client.get(f'/api/units/unit-8/journeys/{jid}').status_code == 200
        assert client.get('/api/units/unit-8/application-lab').json()['challenge_count'] == 13
    else:
        # Historical F4 developer-preview state remains a valid context for this frozen gate.
        assert unit['status'].startswith('F4')
        assert unit['student_release'] is False and unit['preview_release'] is True
        assert unit['journey_count'] >= 2 and unit['scene_count'] >= 21
        assert client.get('/api/units/unit-8/journeys').json()['guided_journeys'] == []
        for jid in ['U8-J1', 'U8-J2']:
            assert client.get(f'/api/units/unit-8/journeys/{jid}').status_code == 404
        assert client.get('/api/units/unit-8/application-lab').json()['challenge_count'] == 0
    # Unit 7 remains student ready after Unit 8 advances.
    u7 = client.get('/api/units/unit-7').json()
    assert u7['student_release'] is True
    assert len(client.get('/api/units/unit-7/journeys').json()['guided_journeys']) == 6
