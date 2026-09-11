from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
U8 = ROOT / 'content' / 'ap-biology' / 'unit-8'
DOCS = ROOT / 'docs'
SOURCE = U8 / 'narrative-source-f4c.md'
BRIEFS = json.loads((U8 / 'briefs' / 'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS = json.loads((U8 / 'briefs' / 'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J3 = next(j for j in JBRIEFS if j['journey_id'] == 'U8-J3')
B = {b['locus_id']: b for b in BRIEFS if b['journey_id'] == 'U8-J3'}
CANON = {r['Knowledge ID']: r for r in json.loads((U8 / 'canonical-catalog.json').read_text(encoding='utf-8'))}

ROUTE_META = [
    ('U8-L22', 'Watershed Reservoir Map Hub', 'Reservoirs and transfers', 'Map hub', 'POOL→PROCESS'),
    ('U8-L23', 'Water Cycle Watershed', 'Water cycle', 'Glass valley', 'H₂O'),
    ('U8-L24', 'Carbon Cycle Reservoir Terrace', 'Carbon cycle', 'Reservoir terrace', 'CO₂↔C'),
    ('U8-L25', 'Nitrogen Transformation Gallery', 'Nitrogen cycle', 'Transformation gallery', 'N₂→NH₄⁺→NO₃⁻'),
    ('U8-L26', 'Phosphorus Sedimentary Basin', 'Phosphorus cycle', 'Sedimentary basin', 'ROCK→PO₄'),
]

GENERATED_UTC = '2026-09-09T04:15:00+00:00'
TITLE = 'The Watershed with the Missing Arrows'
TAGLINE = 'Five fixed locations, four matter tracers, and one rule. Keep reservoirs stationary and move matter only when a real transfer process earns an arrow.'
PREMISE = 'The Biogeochemical Cycle Watershed has lost the arrows connecting its reservoirs. Dr. Mira Sen carries one transparent watershed reservoir board through five fixed locations. Each pathway returns only when the learner can distinguish where matter is stored from the process that moves it and can preserve the characteristic reservoirs and transformations of water, carbon, nitrogen, and phosphorus.'
MISSION = 'Travel the locked F2 route in order. Keep reservoir boxes and transfer arrows physically distinct, follow the same matter through valid ecological processes, preserve the chemical direction of nitrogen transformations, and explain why the phosphorus cycle is primarily sedimentary without inventing a large atmospheric phosphorus reservoir.'
FINALE = 'The watershed map is restored after the learner can rebuild all four cycles from reservoirs and processes instead of memorized arrow shapes. Water, carbon, nitrogen, and phosphorus share a reservoir-transfer grammar while retaining different dominant reservoirs, transformations, chemical directions, and timescales.'


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
        'name': J3['unit_guide']['name'],
        'role': J3['unit_guide']['role'],
        'visual': J3['unit_guide']['visual_identity'],
        'story_job': J3['unit_guide']['behavior_rule'],
    }
    continuity = J3['continuity_object']

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
                'story': f"the {b['micro_anchor']} where the reservoir, process, or chemical direction is made visible before the term is named",
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
                {'name': 'Transparent watershed reservoir board', 'kind': 'journey continuity object', 'visual': 'a clear watershed map with fixed reservoir boxes and empty transfer-arrow slots; water, carbon, nitrogen, and phosphorus tracers change, while reservoir versus process never changes meaning', 'job': 'keeps reservoirs, transfer processes, and same-material tracers spatially stable without replacing real molecules, organisms, rocks, water, microbes, or conventional process arrows'},
            ],
            'continuity_object': continuity,
            'story_open': paragraphs[0],
            'story_paragraphs': paragraphs,
            'story_close': paragraphs[-1],
            'object_ids': b['knowledge_ids'],
            'story_beats': story_beats,
            'prior_unit_reactivation': b.get('cross_unit_links', []),
            'misconception_guards': b['misconception_guards'],
            'checkpoint': bool(cp),
            'checkpoint_object_id': b['primary_knowledge_id'] if cp else None,
            'checkpoint_prompt': b['quick_recall']['candidate_prompt'] if cp else '',
            'checkpoint_answer': b['quick_recall']['answer'] if cp else '',
            'next_locus': ROUTE_META[idx+1][1] if idx + 1 < len(ROUTE_META) else None,
            'f3_scene_brief_id': b['scene_brief_id'],
            'narrative_word_count': wc,
        })

    if len(all_ids) != 15 or len(set(all_ids)) != 15:
        raise ValueError(f'Expected 15 unique F3-assigned records, got {len(all_ids)} / {len(set(all_ids))}')
    if exact_targets != 11:
        raise ValueError(f'Expected 11 exact-name targets, got {exact_targets}')
    if checkpoints != 2:
        raise ValueError(f'Expected 2 checkpoints, got {checkpoints}')

    journey = {
        'palace_id': 'U8-J3',
        'unit_id': 'unit-8',
        'palace_name': 'Biogeochemical Cycle Watershed',
        'story_title': TITLE,
        'tagline': TAGLINE,
        'guide': guide,
        'premise': PREMISE,
        'mission': MISSION,
        'finale': FINALE,
        'estimated_minutes': 18,
        'scene_count': 5,
        'checkpoint_count': checkpoints,
        'student_release': 'DEVELOPER_PREVIEW_F4C',
        'preview_release': True,
        'narrative_design': 'U8-F4C-NARRATIVE-1.0',
        'learner_rule': 'Fix left, center, and right before moving any tracer. Reservoir boxes remain stationary, process names remain on arrows, and the same material is followed into a destination reservoir. Exact terms appear only after the defining transfer or chemical direction is visible. Optional Quick Recall appears only twice.',
        'route_orientation': 'The watershed follows one continuous route through five permanent locations in F2 order. Enter at Watershed Reservoir Map Hub and continue through Water Cycle Watershed, Carbon Cycle Reservoir Terrace, Nitrogen Transformation Gallery, and Phosphorus Sedimentary Basin. Every location fixes left, center, and right before the matter tracer moves.',
        'route': route,
        'scenes': scenes,
        'source_brief_lock': 'LOCKED_F3',
        'scientific_lock': 'LOCKED_F1',
        'architecture_lock': 'LOCKED_F2',
        'prior_narrative_locks': ['LOCKED_F4A_J1', 'LOCKED_F4B_J2'],
    }

    (U8 / 'journeys').mkdir(exist_ok=True)
    (U8 / 'journeys/U8-J3.json').write_text(json.dumps(journey, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    j1 = json.loads((U8 / 'journeys/U8-J1.json').read_text(encoding='utf-8'))
    j2 = json.loads((U8 / 'journeys/U8-J2.json').read_text(encoding='utf-8'))
    summaries = []
    for j in (j1, j2, journey):
        summaries.append({k: j[k] for k in ['palace_id', 'palace_name', 'story_title', 'tagline', 'guide', 'premise', 'mission', 'finale', 'estimated_minutes', 'scene_count', 'checkpoint_count', 'student_release', 'narrative_design']})
    summary = {
        'schema': 'memory-palace-v2-unit8-f4c-journeys-1.0',
        'unit_id': 'unit-8', 'stage': 'F4C', 'student_release': False, 'preview_release': True,
        'journey_count': 3, 'scene_count': 26, 'checkpoint_count': j1['checkpoint_count'] + j2['checkpoint_count'] + checkpoints,
        'guided_journeys': summaries,
    }
    (U8 / 'journeys-f4c.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    j1_words = sum(s['narrative_word_count'] for s in j1['scenes'])
    j2_words = sum(s['narrative_word_count'] for s in j2['scenes'])
    status = {
        'unit_id': 'unit-8', 'number': 8, 'title': 'Ecology',
        'status': 'F4C_JOURNEY3_POLISHED_DEVELOPER_PREVIEW',
        'pipeline_stage': 'UNIT8_F4C_JOURNEY3_NARRATIVE',
        'canonical_lock': 'LOCKED_F1', 'architecture_lock': 'LOCKED_F2', 'scene_brief_lock': 'LOCKED_F3',
        'narrative_lock_j1': 'LOCKED_F4A_J1', 'narrative_lock_j2': 'LOCKED_F4B_J2', 'narrative_lock_j3': 'LOCKED_F4C_J3',
        'student_release': False, 'preview_release': True,
        'journey_count': 3, 'scene_count': 26, 'memory_objects': 0, 'application_challenges': 0,
        'canonical_records': 255, 'architecture_journeys': 8, 'architecture_bundles': 22, 'architecture_loci': 58, 'scene_briefs': 58,
        'palace_managed_records': 211, 'challenge_lab_records': 13, 'scope_guard_records': 31, 'exact_name_review_targets': 135, 'confusable_sets': 40, 'optional_first_exposure_recalls': 18,
        'f4a_journey': 'U8-J1', 'f4a_scene_count': 12, 'f4a_knowledge_records': 50, 'f4a_exact_name_targets': 35, 'f4a_optional_recalls': 2, 'f4a_narrative_words': j1_words,
        'f4b_journey': 'U8-J2', 'f4b_scene_count': 9, 'f4b_knowledge_records': 47, 'f4b_exact_name_targets': 24, 'f4b_optional_recalls': 3, 'f4b_narrative_words': j2_words,
        'f4c_journey': 'U8-J3', 'f4c_scene_count': 5, 'f4c_knowledge_records': 15, 'f4c_exact_name_targets': exact_targets, 'f4c_optional_recalls': checkpoints, 'f4c_narrative_words': total_words,
        'polished_journey_count': 3, 'polished_scene_count': 26, 'polished_knowledge_records': 112, 'polished_narrative_words': j1_words + j2_words + total_words,
        'next_required_output': 'F4D polished narrative for Journey 4 only after Journeys 1 through 3 remain frozen and all F1 through F4C regression gates continue to pass.',
        'next_gate': 'UNIT8_F4D_JOURNEY4_POLISHED_NARRATIVE',
    }
    (U8 / 'status-f4c.json').write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (U8 / 'status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    course_path = ROOT / 'content/ap-biology/course.json'
    course = json.loads(course_path.read_text(encoding='utf-8'))
    unit = next(x for x in course['units'] if x['unit_id'] == 'unit-8')
    unit.update({
        'status': status['status'], 'journey_count': 3, 'scene_count': 26, 'student_release': False, 'preview_release': True,
        'source_status': 'AUDITED_F1_ARCHITECTURE_F2_BRIEFS_F3_NARRATIVE_F4A_F4B_F4C', 'pipeline_stage': status['pipeline_stage'],
        'narrative_lock': 'LOCKED_F4A_J1_LOCKED_F4B_J2_LOCKED_F4C_J3', 'narrative_journeys': 3,
    })
    course_path.write_text(json.dumps(course, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    story_doc = SOURCE.read_text(encoding='utf-8').replace('## The Watershed with the Missing Arrows', f'## {TITLE}', 1)
    (DOCS / 'UNIT8_F4C_JOURNEY3_STORY.md').write_text(story_doc, encoding='utf-8')

    rows = []
    for s in scenes:
        for beat in s['story_beats']:
            rows.append((s['locus_id'], s['locus'], beat['object_id'], beat['term'], 'YES' if beat['exact_name'] else 'NO', beat['scope_class'], beat['science']))
    matrix = [
        '# Unit 8 F4C Journey 3 Story Matrix', '',
        'Journey **U8-J3 Biogeochemical Cycle Watershed** contains **5 polished scenes**, **15 locked F3 knowledge records**, **11 exact-name targets**, and **2 optional first-exposure Quick Recalls**.', '',
        '| Locus | Location | Knowledge ID | Term | Exact name | Scope | Locked science |',
        '|---|---|---|---|---:|---|---|',
    ]
    for row in rows:
        matrix.append('| ' + ' | '.join(str(x).replace('|', '\\|') for x in row) + ' |')
    (DOCS / 'UNIT8_F4C_STORY_MATRIX.md').write_text('\n'.join(matrix) + '\n', encoding='utf-8')

    release_manifest = {
        'schema': 'memory-palace-v2-unit8-f4c-release-1.0', 'generated_utc': GENERATED_UTC,
        'unit_id': 'unit-8', 'release_status': status['status'], 'student_release': False, 'preview_release': True,
        'journey_id': 'U8-J3', 'journeys_polished': 3, 'f4c_scenes': 5, 'f4c_knowledge_records': 15, 'f4c_exact_name_targets': exact_targets,
        'f4c_optional_first_exposure_recalls': checkpoints, 'f4c_narrative_words': total_words,
        'cumulative_polished_scenes': 26, 'cumulative_polished_knowledge_records': 112, 'cumulative_narrative_words': j1_words + j2_words + total_words,
        'canonical_records': 255, 'permanent_loci_architecture': 58, 'scene_briefs': 58, 'memory_objects': 0, 'application_challenges': 0,
        'scientific_lock': 'LOCKED_F1', 'architecture_lock': 'LOCKED_F2', 'scene_brief_lock': 'LOCKED_F3',
        'prior_narrative_locks': ['LOCKED_F4A_J1', 'LOCKED_F4B_J2'], 'narrative_lock': 'LOCKED_F4C_J3',
        'next_stage': 'F4D Journey 4 polished narrative after F4C regression',
    }
    (U8 / 'f4c-release-manifest.json').write_text(json.dumps(release_manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    lock_files = [
        U8 / 'narrative-source-f4c.md', U8 / 'journeys/U8-J3.json', U8 / 'journeys-f4c.json', U8 / 'status-f4c.json', U8 / 'f4c-release-manifest.json',
        DOCS / 'UNIT8_F4C_JOURNEY3_STORY.md', DOCS / 'UNIT8_F4C_STORY_MATRIX.md',
    ]
    content_lock = {
        'schema': 'memory-palace-v2-unit8-f4c-lock-1.0', 'unit_id': 'unit-8', 'lock_status': 'LOCKED_F4C_J3',
        'student_release': False, 'preview_release': True,
        'protected_prior_locks': ['f1-source-lock.json', 'content-lock-f2.json', 'content-lock-f3.json', 'content-lock-f4a.json', 'content-lock-f4b.json'],
        'journey_id': 'U8-J3', 'scene_count': 5, 'knowledge_record_count': 15, 'exact_name_target_count': exact_targets, 'checkpoint_count': checkpoints,
        'files': {str(p.relative_to(U8)) if U8 in p.parents else str(p.relative_to(ROOT)): {'bytes': p.stat().st_size, 'sha256': sha256(p)} for p in lock_files},
        'rule': 'Journey 3 polished prose may not change after F4C without a new explicit narrative version. Journeys 1 and 2 remain frozen. F1 science, F2 classification and geometry, and F3 scene briefs remain authoritative boundaries.',
    }
    (U8 / 'content-lock-f4c.json').write_text(json.dumps(content_lock, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    return {'journey': journey, 'status': status, 'release_manifest': release_manifest}


if __name__ == '__main__':
    result = build()
    print(json.dumps({'status': result['status']['status'], 'scenes': result['status']['f4c_scene_count'], 'records': result['status']['f4c_knowledge_records'], 'words': result['status']['f4c_narrative_words']}, indent=2))
