from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
U8 = ROOT / 'content' / 'ap-biology' / 'unit-8'
DOCS = ROOT / 'docs'
SOURCE = U8 / 'narrative-source-f4e.md'
BRIEFS = json.loads((U8 / 'briefs' / 'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS = json.loads((U8 / 'briefs' / 'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J5 = next(j for j in JBRIEFS if j['journey_id'] == 'U8-J5')
B = {b['locus_id']: b for b in BRIEFS if b['journey_id'] == 'U8-J5'}
CANON = {r['Knowledge ID']: r for r in json.loads((U8 / 'canonical-catalog.json').read_text(encoding='utf-8'))}

ROUTE_META = [
    ('U8-L34', 'Exponential Growth Console', 'Exponential growth', 'J-curve console', 'dN/dt=rmaxN→J'),
    ('U8-L35', 'Carrying Capacity Resource Ceiling', 'Carrying capacity', 'K ceiling', 'ENVIRONMENT→K'),
    ('U8-L36', 'Logistic Growth Console', 'Logistic growth', 'S-curve console', '(K−N)/K→S'),
    ('U8-L37', 'Density-Dependent Regulation Test Bay', 'Density-dependent regulation', 'Matched-density bay', 'DENSITY→PER-CAPITA EFFECT'),
    ('U8-L38', 'Density-Independent Disturbance Test Bay', 'Density-independent effects', 'Disturbance bay', 'DISTURBANCE⊥DENSITY'),
]

GENERATED_UTC = '2026-09-09T04:30:00+00:00'
TITLE = 'The Curve That Would Not Hold Still'
TAGLINE = 'Five fixed control rooms, one population-growth dashboard, and one rule. Read the assumptions before trusting the curve.'
PREMISE = 'A population-growth control system keeps producing different curves and regulation labels from the same dashboard. Dr. Mira Sen carries N, time, rmax, K, per-capita effects, and graph axes through five rooms so each model or classification can be explained from its assumptions and mechanism.'
MISSION = 'Travel the locked F2 route in order. Keep one population-growth dashboard visible while moving from exponential growth to environment-dependent carrying capacity, logistic slowing, density-dependent regulation, and density-independent effects. Preserve dN/dt, rmax, N, and K as distinct quantities and diagnose regulation from per-capita effects rather than total counts.'
FINALE = 'The control center stabilizes after the learner reconstructs why a J curve follows exponential assumptions, why K moves with environmental conditions, why the logistic term slows growth as N approaches K, and why density dependence is diagnosed from how per-capita effects change with density.'
CONTINUITY_NAME = 'population-growth dashboard'
CONTINUITY_VISUAL = 'one transparent control dashboard that keeps population size N, time, rmax, an environment-dependent K and resource readout, a per-capita effect panel, and fixed population-versus-time graph axes visible across all five control rooms'
CONTINUITY_JOB = 'preserves the same population-growth variables and graph axes while each room changes only the model assumption, environmental ceiling, or regulation test needed for the next distinction'


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w’′'-]+\b", text))


def parse_source() -> list[dict]:
    text = SOURCE.read_text(encoding='utf-8')
    parts = re.split(r'^###\s+', text, flags=re.M)[1:]
    if len(parts) != 5:
        raise ValueError(f'Expected 5 scene sections, found {len(parts)}')
    scenes = []
    for i, part in enumerate(parts, start=1):
        lines = part.strip().splitlines()
        heading = lines[0].strip()
        m = re.match(r'(\d+)\.\s+(.+?)\s+·\s+(.+)', heading)
        if not m:
            raise ValueError(f'Bad scene heading {heading!r}')
        scene_num, locus_name, title = int(m.group(1)), m.group(2).strip(), m.group(3).strip()
        if scene_num != i:
            raise ValueError('Scene numbering mismatch')
        locus_id, expected_name, *_ = ROUTE_META[i-1]
        if locus_name != expected_name:
            raise ValueError(f'Route name mismatch for {locus_id}: {locus_name!r} != {expected_name!r}')
        body = '\n'.join(lines[1:]).strip()
        checkpoint = None
        if '**Optional Quick Recall**' in body:
            story_body, recall_body = body.split('**Optional Quick Recall**', 1)
            recall_lines = [x.strip() for x in recall_body.splitlines() if x.strip()]
            checkpoint = recall_lines[0] if recall_lines else ''
        else:
            story_body = body
        paragraphs = [re.sub(r'\s+', ' ', p.strip()) for p in re.split(r'\n\s*\n', story_body) if p.strip()]
        scenes.append({'locus_id': locus_id, 'locus': locus_name, 'title': title, 'paragraphs': paragraphs, 'checkpoint_source': checkpoint})
    return scenes


def term_present(term: str, prose: str) -> bool:
    normalized = prose.casefold().replace('**', '')
    variants = [term.casefold()]
    if '/' in term:
        variants.extend(x.strip().casefold() for x in term.split('/'))
    return any(v in normalized for v in variants)


def build() -> dict:
    parsed = parse_source()
    route, scenes, all_ids = [], [], []
    exact_targets = checkpoints = total_words = 0

    guide = {
        'name': J5['unit_guide']['name'],
        'role': J5['unit_guide']['role'],
        'visual': J5['unit_guide']['visual_identity'],
        'story_job': J5['unit_guide']['behavior_rule'],
    }

    for idx, scene_source in enumerate(parsed):
        locus_id, locus_name, short, floor, symbol = ROUTE_META[idx]
        b = B[locus_id]
        if b['exact_location'] != locus_name:
            raise ValueError(f'F3 location mismatch at {locus_id}')
        paragraphs = scene_source['paragraphs']
        prose = ' '.join(paragraphs)
        if word_count(prose) < 450:
            raise ValueError(f'{locus_id} prose below 450 words')
        if len(paragraphs) < 6:
            raise ValueError(f'{locus_id} needs at least six narrative paragraphs')
        if '—' in prose or ':' in prose:
            raise ValueError(f'{locus_id} contains prohibited punctuation')
        first = paragraphs[0].casefold()
        if 'left' not in first or ('ahead' not in first and 'center' not in first) or 'right' not in first:
            raise ValueError(f'{locus_id} opening does not establish left/center/right geography')

        story_beats = []
        for t in b['term_introductions']:
            kid = t['knowledge_id']
            c = CANON[kid]
            if c['Canonical Verified Statement'] != t['canonical_science']:
                raise ValueError(f'Canonical science mismatch for {kid}')
            if t['exact_name_recall']:
                exact_targets += 1
                if not term_present(t['canonical_term'], prose):
                    raise ValueError(f'Exact name target missing from prose {kid} {t["canonical_term"]}')
            all_ids.append(kid)
            story_beats.append({
                'object_id': kid,
                'term': t['canonical_term'],
                'story': f"the {b['micro_anchor']} where the population model, resource ceiling, graph relation, or regulation comparison becomes visible before the term is named",
                'science': c['Canonical Verified Statement'],
                'exact_name': bool(t['exact_name_recall']),
                'hint': b['micro_anchor'],
                'name_support': t['name_support'],
                'reactivation_mode': 'NEW_OR_EXTENDED_UNIT8_LEARNING',
                'scope_class': t['scope_class'],
            })

        cp = b['quick_recall']['enabled']
        if cp:
            checkpoints += 1
            expected_prompt = b['quick_recall']['candidate_prompt']
            src = scene_source['checkpoint_source'] or ''
            if re.sub(r'\*\*', '', src).casefold() != expected_prompt.casefold():
                raise ValueError(f'Checkpoint prompt mismatch at {locus_id}')
        elif scene_source['checkpoint_source']:
            raise ValueError(f'Unexpected checkpoint in source at {locus_id}')

        zones = []
        for position in ('left', 'center', 'right'):
            anchor = b['spatial_layout'][position]['anchor']
            cast_match = next((x for x in b['stable_cast'] if x['position'] == position), None)
            zones.append({
                'position': position,
                'label': anchor,
                'symbol': {'left': 'L', 'center': 'C', 'right': 'R'}[position],
                'description': cast_match['visual_identity'] if cast_match else anchor,
            })

        wc = word_count(prose)
        total_words += wc
        route.append({'scene_index': idx, 'locus': locus_name, 'short': short, 'floor': floor, 'symbol': symbol})
        scenes.append({
            'scene_index': idx,
            'locus_id': locus_id,
            'locus': locus_name,
            'title': scene_source['title'],
            'scene_kicker': b['exit_memory']['one_sentence_model'],
            'location_description': b['exact_location'],
            'scene_layout': {'orientation': b['orientation_sentence'], 'zones': zones},
            'cast': [
                {'name': guide['name'], 'kind': 'guide', 'visual': guide['visual'], 'job': guide['story_job']},
                *[{'name': x['name'], 'kind': x['type'].lower(), 'visual': x['visual_identity'], 'job': x['job_in_scene']} for x in b['stable_cast']],
                {'name': CONTINUITY_NAME, 'kind': 'journey continuity object', 'visual': CONTINUITY_VISUAL, 'job': CONTINUITY_JOB},
            ],
            'continuity_object': CONTINUITY_VISUAL,
            'story_open': paragraphs[0],
            'story_paragraphs': paragraphs,
            'story_close': paragraphs[-1],
            'object_ids': b['knowledge_ids'],
            'story_beats': story_beats,
            'prior_unit_reactivation': b.get('cross_unit_links', []),
            'misconception_guards': b['misconception_guards'],
            'checkpoint': cp,
            'checkpoint_object_id': b['primary_knowledge_id'] if cp else None,
            'checkpoint_prompt': b['quick_recall']['candidate_prompt'] if cp else None,
            'checkpoint_answer': b['quick_recall']['answer'] if cp else None,
            'next_locus': ROUTE_META[idx+1][1] if idx + 1 < len(ROUTE_META) else None,
            'f3_scene_brief_id': b['scene_brief_id'],
            'narrative_word_count': wc,
        })

    if len(all_ids) != 11 or len(set(all_ids)) != 11:
        raise ValueError(f'Expected 11 unique Journey 5 knowledge records, got {len(all_ids)} refs and {len(set(all_ids))} unique')
    if exact_targets != 8:
        raise ValueError(f'Expected 8 exact-name targets, got {exact_targets}')
    if checkpoints != 2:
        raise ValueError(f'Expected 2 checkpoints, got {checkpoints}')

    journey = {
        'palace_id': 'U8-J5',
        'unit_id': 'unit-8',
        'palace_name': 'Population Growth Control Center',
        'story_title': TITLE,
        'tagline': TAGLINE,
        'guide': guide,
        'premise': PREMISE,
        'mission': MISSION,
        'finale': FINALE,
        'estimated_minutes': 19,
        'scene_count': 5,
        'checkpoint_count': checkpoints,
        'student_release': 'DEVELOPER_PREVIEW_F4E',
        'preview_release': True,
        'narrative_design': 'U8-F4E-NARRATIVE-1.0',
        'learner_rule': 'Keep one population-growth dashboard visible and change one assumption or tested relationship at a time. dN/dt, N, rmax, and K remain distinct. Exponential and logistic curves must be justified from model assumptions, and density dependence must be diagnosed from per-capita effects. Optional Quick Recall appears only twice.',
        'route_orientation': 'The control center follows one continuous route through five permanent locations in F2 order. Enter at Exponential Growth Console and continue through Carrying Capacity Resource Ceiling, Logistic Growth Console, Density-Dependent Regulation Test Bay, and Density-Independent Disturbance Test Bay. Every location fixes left, center, and right before the population model or regulation test changes.',
        'route': route,
        'scenes': scenes,
        'source_brief_lock': 'LOCKED_F3',
        'scientific_lock': 'LOCKED_F1',
        'architecture_lock': 'LOCKED_F2',
        'prior_narrative_locks': ['LOCKED_F4A_J1', 'LOCKED_F4B_J2', 'LOCKED_F4C_J3', 'LOCKED_F4D_J4'],
    }

    (U8 / 'journeys').mkdir(exist_ok=True)
    (U8 / 'journeys/U8-J5.json').write_text(json.dumps(journey, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    prior = [json.loads((U8 / f'journeys/U8-J{i}.json').read_text(encoding='utf-8')) for i in (1, 2, 3, 4)]
    summaries = []
    for j in [*prior, journey]:
        summaries.append({k: j[k] for k in ['palace_id', 'palace_name', 'story_title', 'tagline', 'guide', 'premise', 'mission', 'finale', 'estimated_minutes', 'scene_count', 'checkpoint_count', 'student_release', 'narrative_design']})
    total_scene_count = sum(j['scene_count'] for j in [*prior, journey])
    total_checkpoint_count = sum(j['checkpoint_count'] for j in [*prior, journey])
    summary = {
        'schema': 'memory-palace-v2-unit8-f4e-journeys-1.0',
        'unit_id': 'unit-8', 'stage': 'F4E', 'student_release': False, 'preview_release': True,
        'journey_count': 5, 'scene_count': total_scene_count, 'checkpoint_count': total_checkpoint_count,
        'guided_journeys': summaries,
    }
    (U8 / 'journeys-f4e.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    prior_words = [sum(s['narrative_word_count'] for s in j['scenes']) for j in prior]
    prior_records = [sum(len(s['object_ids']) for s in j['scenes']) for j in prior]
    polished_records = sum(prior_records) + len(all_ids)
    status = {
        'unit_id': 'unit-8', 'number': 8, 'title': 'Ecology',
        'status': 'F4E_JOURNEY5_POLISHED_DEVELOPER_PREVIEW',
        'pipeline_stage': 'UNIT8_F4E_JOURNEY5_NARRATIVE',
        'canonical_lock': 'LOCKED_F1', 'architecture_lock': 'LOCKED_F2', 'scene_brief_lock': 'LOCKED_F3',
        'narrative_lock_j1': 'LOCKED_F4A_J1', 'narrative_lock_j2': 'LOCKED_F4B_J2', 'narrative_lock_j3': 'LOCKED_F4C_J3', 'narrative_lock_j4': 'LOCKED_F4D_J4', 'narrative_lock_j5': 'LOCKED_F4E_J5',
        'student_release': False, 'preview_release': True,
        'journey_count': 5, 'scene_count': total_scene_count, 'memory_objects': 0, 'application_challenges': 0,
        'canonical_records': 255, 'architecture_journeys': 8, 'architecture_bundles': 22, 'architecture_loci': 58, 'scene_briefs': 58,
        'palace_managed_records': 211, 'challenge_lab_records': 13, 'scope_guard_records': 31, 'exact_name_review_targets': 135, 'confusable_sets': 40, 'optional_first_exposure_recalls': 18,
        'f4a_journey': 'U8-J1', 'f4a_scene_count': 12, 'f4a_knowledge_records': prior_records[0], 'f4a_exact_name_targets': 35, 'f4a_optional_recalls': 2, 'f4a_narrative_words': prior_words[0],
        'f4b_journey': 'U8-J2', 'f4b_scene_count': 9, 'f4b_knowledge_records': prior_records[1], 'f4b_exact_name_targets': 24, 'f4b_optional_recalls': 3, 'f4b_narrative_words': prior_words[1],
        'f4c_journey': 'U8-J3', 'f4c_scene_count': 5, 'f4c_knowledge_records': prior_records[2], 'f4c_exact_name_targets': 11, 'f4c_optional_recalls': 2, 'f4c_narrative_words': prior_words[2],
        'f4d_journey': 'U8-J4', 'f4d_scene_count': 7, 'f4d_knowledge_records': prior_records[3], 'f4d_exact_name_targets': 18, 'f4d_optional_recalls': 2, 'f4d_narrative_words': prior_words[3],
        'f4e_journey': 'U8-J5', 'f4e_scene_count': 5, 'f4e_knowledge_records': 11, 'f4e_exact_name_targets': exact_targets, 'f4e_optional_recalls': checkpoints, 'f4e_narrative_words': total_words,
        'polished_journey_count': 5, 'polished_scene_count': total_scene_count, 'polished_knowledge_records': polished_records, 'polished_narrative_words': sum(prior_words) + total_words,
        'next_required_output': 'F4F polished narrative for Journey 6 only after Journeys 1 through 5 remain frozen and all F1 through F4E regression gates continue to pass.',
        'next_gate': 'UNIT8_F4F_JOURNEY6_POLISHED_NARRATIVE',
    }
    (U8 / 'status-f4e.json').write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (U8 / 'status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    course_path = ROOT / 'content/ap-biology/course.json'
    course = json.loads(course_path.read_text(encoding='utf-8'))
    unit = next(x for x in course['units'] if x['unit_id'] == 'unit-8')
    unit.update({
        'status': status['status'], 'journey_count': 5, 'scene_count': total_scene_count, 'student_release': False, 'preview_release': True,
        'source_status': 'AUDITED_F1_ARCHITECTURE_F2_BRIEFS_F3_NARRATIVE_F4A_F4B_F4C_F4D_F4E', 'pipeline_stage': status['pipeline_stage'],
        'narrative_lock': 'LOCKED_F4A_J1_LOCKED_F4B_J2_LOCKED_F4C_J3_LOCKED_F4D_J4_LOCKED_F4E_J5', 'narrative_journeys': 5,
    })
    course_path.write_text(json.dumps(course, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    story_doc = SOURCE.read_text(encoding='utf-8').replace('## The Curve That Would Not Hold Still', f'## {TITLE}', 1)
    (DOCS / 'UNIT8_F4E_JOURNEY5_STORY.md').write_text(story_doc, encoding='utf-8')

    rows = []
    for s in scenes:
        for beat in s['story_beats']:
            rows.append((s['locus_id'], s['locus'], beat['object_id'], beat['term'], 'YES' if beat['exact_name'] else 'NO', beat['scope_class'], beat['science']))
    matrix = [
        '# Unit 8 F4E Journey 5 Story Matrix', '',
        'Journey **U8-J5 Population Growth Control Center** contains **5 polished scenes**, **11 locked F3 knowledge records**, **8 exact-name targets**, and **2 optional first-exposure Quick Recalls**.', '',
        '| Locus | Location | Knowledge ID | Term | Exact name | Scope | Locked science |',
        '|---|---|---|---|---:|---|---|',
    ]
    for row in rows:
        matrix.append('| ' + ' | '.join(str(x).replace('|', '\\|') for x in row) + ' |')
    (DOCS / 'UNIT8_F4E_STORY_MATRIX.md').write_text('\n'.join(matrix) + '\n', encoding='utf-8')

    release_manifest = {
        'schema': 'memory-palace-v2-unit8-f4e-release-1.0', 'generated_utc': GENERATED_UTC,
        'unit_id': 'unit-8', 'release_status': status['status'], 'student_release': False, 'preview_release': True,
        'journey_id': 'U8-J5', 'journeys_polished': 5, 'f4e_scenes': 5, 'f4e_knowledge_records': 11, 'f4e_exact_name_targets': exact_targets,
        'f4e_optional_first_exposure_recalls': checkpoints, 'f4e_narrative_words': total_words,
        'cumulative_polished_scenes': total_scene_count, 'cumulative_polished_knowledge_records': polished_records, 'cumulative_narrative_words': sum(prior_words) + total_words,
        'canonical_records': 255, 'permanent_loci_architecture': 58, 'scene_briefs': 58, 'memory_objects': 0, 'application_challenges': 0,
        'scientific_lock': 'LOCKED_F1', 'architecture_lock': 'LOCKED_F2', 'scene_brief_lock': 'LOCKED_F3',
        'prior_narrative_locks': ['LOCKED_F4A_J1', 'LOCKED_F4B_J2', 'LOCKED_F4C_J3', 'LOCKED_F4D_J4'], 'narrative_lock': 'LOCKED_F4E_J5',
        'next_stage': 'F4F Journey 6 polished narrative after F4E regression',
    }
    (U8 / 'f4e-release-manifest.json').write_text(json.dumps(release_manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    lock_files = [
        U8 / 'narrative-source-f4e.md', U8 / 'journeys/U8-J5.json', U8 / 'journeys-f4e.json', U8 / 'status-f4e.json', U8 / 'f4e-release-manifest.json',
        DOCS / 'UNIT8_F4E_JOURNEY5_STORY.md', DOCS / 'UNIT8_F4E_STORY_MATRIX.md',
    ]
    content_lock = {
        'schema': 'memory-palace-v2-unit8-f4e-lock-1.0', 'unit_id': 'unit-8', 'lock_status': 'LOCKED_F4E_J5',
        'student_release': False, 'preview_release': True,
        'protected_prior_locks': ['f1-source-lock.json', 'content-lock-f2.json', 'content-lock-f3.json', 'content-lock-f4a.json', 'content-lock-f4b.json', 'content-lock-f4c.json', 'content-lock-f4d.json'],
        'journey_id': 'U8-J5', 'scene_count': 5, 'knowledge_record_count': 11, 'exact_name_target_count': exact_targets, 'checkpoint_count': checkpoints,
        'files': {str(p.relative_to(U8)) if U8 in p.parents else str(p.relative_to(ROOT)): {'bytes': p.stat().st_size, 'sha256': sha256(p)} for p in lock_files},
        'rule': 'Journey 5 polished prose may not change after F4E without a new explicit narrative version. Journeys 1 through 4 remain frozen. F1 science, F2 classification and geometry, and F3 scene briefs remain authoritative boundaries.',
    }
    (U8 / 'content-lock-f4e.json').write_text(json.dumps(content_lock, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    return {'journey': journey, 'status': status, 'release_manifest': release_manifest}


if __name__ == '__main__':
    result = build()
    print(json.dumps({'status': result['status']['status'], 'scenes': result['status']['f4e_scene_count'], 'records': result['status']['f4e_knowledge_records'], 'words': result['status']['f4e_narrative_words']}, indent=2))
