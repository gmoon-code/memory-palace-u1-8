import json
import re
from pathlib import Path
from fastapi.testclient import TestClient
from backend.main import app

ROOT = Path(__file__).resolve().parents[1]
U8 = ROOT / 'content/ap-biology/unit-8'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def test_unit8_f4h_journey8_accounting_and_boundary():
    j = read(U8 / 'journeys/U8-J8.json')
    assert j['palace_id'] == 'U8-J8'
    assert j['scene_count'] == 8 and len(j['scenes']) == 8
    assert j['checkpoint_count'] == 2
    assert j['student_release'] == 'DEVELOPER_PREVIEW_F4H'
    assert j['preview_release'] is True
    assert [s['locus_id'] for s in j['scenes']] == [f'U8-L{i:02d}' for i in range(51, 59)]
    ids = [kid for s in j['scenes'] for kid in s['object_ids']]
    assert len(ids) == 19 and len(set(ids)) == 19


def test_unit8_f4h_prose_is_substantive_spatial_and_continuous():
    j = read(U8 / 'journeys/U8-J8.json')
    continuity = j['scenes'][0]['continuity_object']
    assert j['guide']['name'] == 'Dr. Mira Sen'
    for s in j['scenes']:
        prose = ' '.join(s['story_paragraphs'])
        assert len(re.findall(r"\b[\w’′'-]+\b", prose)) >= 450
        assert len(s['story_paragraphs']) >= 6
        opening = s['story_paragraphs'][0].casefold()
        assert 'left' in opening and ('ahead' in opening or 'center' in opening) and 'right' in opening
        assert any(c['name'] == 'Dr. Mira Sen' for c in s['cast'])
        assert any(c['name'] == 'baseline landscape record' for c in s['cast'])
        assert s['continuity_object'] == continuity
        assert '—' not in prose and ':' not in prose
        lower = prose.casefold()
        for meta in ['the ppt states', 'the ced says', 'the course requires', 'locked definition', 'source material shows', 'teacher enrichment', 'pipeline language']:
            assert meta not in lower


def test_unit8_f4h_exact_targets_and_story_beat_science_match_locks():
    canon = {r['Knowledge ID']: r for r in read(U8 / 'canonical-catalog.json')}
    briefs = {b['locus_id']: b for b in read(U8 / 'briefs/scene-briefs-f3.json')['scene_briefs'] if b['journey_id'] == 'U8-J8'}
    j = read(U8 / 'journeys/U8-J8.json')
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
    assert exact == 7


def test_unit8_f4h_high_risk_environmental_change_distinctions_are_explicit():
    j = read(U8 / 'journeys/U8-J8.json')
    text = ' '.join(' '.join(s['story_paragraphs']) for s in j['scenes']).casefold().replace('**', '')
    phrases = [
        'mutations do not arise because an organism needs a particular adaptation',
        'heterozygote advantage occurs when heterozygotes have higher relative fitness than either homozygote in a particular environment',
        'introduction alone does not make it invasive',
        'an introduced species is considered invasive when it establishes and spreads with harmful ecological, economic, or health effects',
        'habitat loss and fragmentation are major drivers of biodiversity decline because they reduce available habitat and can isolate populations',
        'larger habitat areas generally support more species than smaller comparable areas',
        'overharvesting occurs when organisms are removed faster than populations can replace themselves',
        'exact classification of the present interval as a completed mass extinction depends on definitions and time scale',
        'some persistent substances become more concentrated at successive trophic levels through biological magnification',
        'effects depend on the pollutant, exposure, and ecosystem buffering',
        'excess nutrient input can stimulate primary production and decomposition, reducing dissolved oxygen and changing aquatic communities',
        'dissolved anthropogenic co₂ lowers seawater ph by shifting carbonate chemistry and can reduce carbonate ion availability for calcifying organisms',
        'species richness often increases toward the tropics, a broad pattern explained by multiple historical, climatic, and ecological mechanisms rather than a single cause',
        'low biodiversity or novel habitat alone does not universally predict the greatest disease impact',
    ]
    for phrase in phrases:
        assert phrase in text


def test_unit8_f4h_only_two_first_exposure_recalls():
    j = read(U8 / 'journeys/U8-J8.json')
    cps = [s for s in j['scenes'] if s['checkpoint']]
    assert [s['locus_id'] for s in cps] == ['U8-L52', 'U8-L57']
    assert cps[0]['checkpoint_prompt'].startswith('Without looking back, identify or explain Invasive species')
    assert cps[1]['checkpoint_prompt'].startswith('Without looking back, identify or explain Ocean acidification')


def test_unit8_f4h_prior_journeys_frozen_and_preview_hidden():
    expected = [('U8-J1',12,2),('U8-J2',9,3),('U8-J3',5,2),('U8-J4',7,2),('U8-J5',5,2),('U8-J6',8,3),('U8-J7',4,2)]
    for jid, scenes, cps in expected:
        j = read(U8 / f'journeys/{jid}.json')
        assert j['scene_count'] == scenes and j['checkpoint_count'] == cps
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
        assert unit['journey_count'] >= 8 and unit['scene_count'] >= 58
        assert client.get('/api/units/unit-8/journeys').json()['guided_journeys'] == []
        for jid in ['U8-J1', 'U8-J2', 'U8-J3', 'U8-J4', 'U8-J5', 'U8-J6', 'U8-J7', 'U8-J8']:
            assert client.get(f'/api/units/unit-8/journeys/{jid}').status_code == 404
        assert client.get('/api/units/unit-8/application-lab').json()['challenge_count'] == 0
    # Unit 7 remains student ready after Unit 8 advances.
    u7 = client.get('/api/units/unit-7').json()
    assert u7['student_release'] is True
    assert len(client.get('/api/units/unit-7/journeys').json()['guided_journeys']) == 6
