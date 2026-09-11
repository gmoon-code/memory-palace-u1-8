from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
U8 = ROOT / 'content' / 'ap-biology' / 'unit-8'
DOCS = ROOT / 'docs'
SOURCE = U8 / 'narrative-source-f4b.md'
BRIEFS = json.loads((U8 / 'briefs' / 'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS = json.loads((U8 / 'briefs' / 'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J2 = next(j for j in JBRIEFS if j['journey_id'] == 'U8-J2')
B = {b['locus_id']: b for b in BRIEFS if b['journey_id'] == 'U8-J2'}
CANON = {r['Knowledge ID']: r for r in json.loads((U8 / 'canonical-catalog.json').read_text(encoding='utf-8'))}

ROUTE_META = [
    ('U8-L13', 'Organism Energy Budget Counter', 'Energy budget', 'Budget counter', 'IN−OUT'),
    ('U8-L14', 'Thermal Regulation Bay', 'Thermal regulation', 'Thermal bay', 'HEAT'),
    ('U8-L15', 'Ecological Scale Atrium', 'Ecological scale', 'Scale atrium', 'NEST'),
    ('U8-L16', 'Energy-Matter Split Gate', 'Energy and matter', 'Split gate', 'FLOW/CYCLE'),
    ('U8-L17', 'Carbon and Energy Acquisition Workshop', 'Acquisition', 'Acquisition workshop', 'C/E'),
    ('U8-L18', 'Trophic Ladder Tower', 'Trophic roles', 'Ladder tower', 'FEED'),
    ('U8-L19', 'Food-Web Projection Room', 'Food webs', 'Projection room', '→CONSUMER'),
    ('U8-L20', 'Production Accounting Ledger', 'Production', 'Production ledger', 'GPP−R=NPP'),
    ('U8-L21', 'Trophic Transfer Pyramid Exit', 'Trophic transfer', 'Pyramid exit', '≈10%'),
]

GENERATED_UTC = '2026-09-09T03:30:00+00:00'
TITLE = 'The Ledger That Would Not Balance'
TAGLINE = 'Nine fixed stations, one two-column ledger, and one rule. Track where energy enters, where it becomes less available, and where matter remains conserved before the hall will let you leave.'
PREMISE = 'The Ecosystem Energy Exchange Hall has begun treating every ecological transfer as though energy and matter obeyed the same route. Dr. Mira Sen carries one transparent two-column ledger through nine fixed stations. The hall can balance only when organism budgets, thermoregulation, ecological scale, energy flow, matter cycling, carbon and energy acquisition, trophic roles, food-web direction, production, and trophic transfer remain causally distinct.'
MISSION = 'Travel the locked F2 route in order. Keep energy and matter in separate visible columns, preserve ecological scale, follow feeding arrows toward the receiving consumer, distinguish producer capture from respiration and heterotroph production, and treat trophic-transfer efficiency as variable rather than a universal ten-percent law.'
FINALE = 'The nine stations relight only after the learner can reconstruct energy input, transformation, respiration, heat dissipation, biomass production, feeding transfer, and matter conservation without recycling energy or losing track of reservoirs. The route ends with energy becoming progressively less available for biological work while matter remains traceable into the biogeochemical-cycle journey.'


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w’′'-]+\b", text))


def parse_source() -> list[dict]:
    text = SOURCE.read_text(encoding='utf-8')
    parts = re.split(r'^###\s+', text, flags=re.M)[1:]
    if len(parts) != 9:
        raise ValueError(f'Expected 9 scene sections, found {len(parts)}')
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
    route = []
    scenes = []
    all_ids = []
    exact_targets = 0
    checkpoints = 0
    total_words = 0

    guide = {
        'name': J2['unit_guide']['name'],
        'role': J2['unit_guide']['role'],
        'visual': J2['unit_guide']['visual_identity'],
        'story_job': J2['unit_guide']['behavior_rule'],
    }
    continuity = J2['continuity_object']

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
                'story': f"the {b['micro_anchor']} where the defining ecological relationship is made visible before the term is named",
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
                {'name': 'Transparent energy-matter ledger', 'kind': 'journey continuity object', 'visual': 'a clear two-column ledger with ENERGY on the left and MATTER on the right, preserving energy dissipation and traceable matter across all nine stations', 'job': 'keeps energy transformation, heat loss, biomass transfer, and matter conservation visible without replacing real organisms, trophic relationships, equations, reservoirs, or arrows'},
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

    if len(all_ids) != 47 or len(set(all_ids)) != 47:
        raise ValueError(f'Expected 47 unique F3-assigned records, got {len(all_ids)} / {len(set(all_ids))}')
    if exact_targets != 24:
        raise ValueError(f'Expected 24 exact-name targets, got {exact_targets}')
    if checkpoints != 3:
        raise ValueError(f'Expected 3 checkpoints, got {checkpoints}')

    journey = {
        'palace_id': 'U8-J2',
        'unit_id': 'unit-8',
        'palace_name': 'Ecosystem Energy Exchange Hall',
        'story_title': TITLE,
        'tagline': TAGLINE,
        'guide': guide,
        'premise': PREMISE,
        'mission': MISSION,
        'finale': FINALE,
        'estimated_minutes': 27,
        'scene_count': 9,
        'checkpoint_count': checkpoints,
        'student_release': 'DEVELOPER_PREVIEW_F4B',
        'preview_release': True,
        'narrative_design': 'U8-F4B-NARRATIVE-1.0',
        'learner_rule': 'Place yourself in the room and fix left, center, and right before following the ecological transfer. The same transparent two-column energy-matter ledger persists through all nine locations. Exact terms appear only after the defining mechanism, equation relation, or transfer is visible. Optional Quick Recall appears only three times.',
        'route_orientation': 'The hall follows one continuous route through nine permanent locations in F2 order. Enter at Organism Energy Budget Counter and continue through Thermal Regulation Bay, Ecological Scale Atrium, Energy-Matter Split Gate, Carbon and Energy Acquisition Workshop, Trophic Ladder Tower, Food-Web Projection Room, Production Accounting Ledger, and Trophic Transfer Pyramid Exit. Every room fixes left, center, and right before the ecological state changes.',
        'route': route,
        'scenes': scenes,
        'source_brief_lock': 'LOCKED_F3',
        'scientific_lock': 'LOCKED_F1',
        'architecture_lock': 'LOCKED_F2',
        'prior_narrative_lock': 'LOCKED_F4A_J1',
    }

    (U8 / 'journeys').mkdir(exist_ok=True)
    journey_path = U8 / 'journeys' / 'U8-J2.json'
    journey_path.write_text(json.dumps(journey, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    j1 = json.loads((U8 / 'journeys/U8-J1.json').read_text(encoding='utf-8'))
    summaries = []
    for j in (j1, journey):
        summaries.append({k: j[k] for k in ['palace_id', 'palace_name', 'story_title', 'tagline', 'guide', 'premise', 'mission', 'finale', 'estimated_minutes', 'scene_count', 'checkpoint_count', 'student_release', 'narrative_design']})
    summary = {
        'schema': 'memory-palace-v2-unit8-f4b-journeys-1.0',
        'unit_id': 'unit-8',
        'stage': 'F4B',
        'student_release': False,
        'preview_release': True,
        'journey_count': 2,
        'scene_count': 21,
        'checkpoint_count': j1['checkpoint_count'] + checkpoints,
        'guided_journeys': summaries,
    }
    (U8 / 'journeys-f4b.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    j1_words = sum(s['narrative_word_count'] for s in j1['scenes'])
    status = {
        'unit_id': 'unit-8', 'number': 8, 'title': 'Ecology',
        'status': 'F4B_JOURNEY2_POLISHED_DEVELOPER_PREVIEW',
        'pipeline_stage': 'UNIT8_F4B_JOURNEY2_NARRATIVE',
        'canonical_lock': 'LOCKED_F1', 'architecture_lock': 'LOCKED_F2', 'scene_brief_lock': 'LOCKED_F3',
        'narrative_lock_j1': 'LOCKED_F4A_J1', 'narrative_lock_j2': 'LOCKED_F4B_J2',
        'student_release': False, 'preview_release': True,
        'journey_count': 2, 'scene_count': 21, 'memory_objects': 0, 'application_challenges': 0,
        'canonical_records': 255, 'architecture_journeys': 8, 'architecture_bundles': 22, 'architecture_loci': 58, 'scene_briefs': 58,
        'palace_managed_records': 211, 'challenge_lab_records': 13, 'scope_guard_records': 31, 'exact_name_review_targets': 135, 'confusable_sets': 40, 'optional_first_exposure_recalls': 18,
        'f4a_journey': 'U8-J1', 'f4a_scene_count': 12, 'f4a_knowledge_records': 50, 'f4a_exact_name_targets': 35, 'f4a_optional_recalls': 2, 'f4a_narrative_words': j1_words,
        'f4b_journey': 'U8-J2', 'f4b_scene_count': 9, 'f4b_knowledge_records': 47, 'f4b_exact_name_targets': exact_targets, 'f4b_optional_recalls': checkpoints, 'f4b_narrative_words': total_words,
        'polished_journey_count': 2, 'polished_scene_count': 21, 'polished_knowledge_records': 97, 'polished_narrative_words': j1_words + total_words,
        'next_required_output': 'F4C polished narrative for Journey 3 only after Journeys 1 and 2 remain frozen and all F1 through F4B regression gates continue to pass.',
        'next_gate': 'UNIT8_F4C_JOURNEY3_POLISHED_NARRATIVE',
    }
    (U8 / 'status-f4b.json').write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (U8 / 'status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    course_path = ROOT / 'content' / 'ap-biology' / 'course.json'
    course = json.loads(course_path.read_text(encoding='utf-8'))
    unit = next(x for x in course['units'] if x['unit_id'] == 'unit-8')
    unit.update({
        'status': status['status'], 'journey_count': 2, 'scene_count': 21, 'student_release': False, 'preview_release': True,
        'source_status': 'AUDITED_F1_ARCHITECTURE_F2_BRIEFS_F3_NARRATIVE_F4A_F4B', 'pipeline_stage': status['pipeline_stage'],
        'narrative_lock': 'LOCKED_F4A_J1_LOCKED_F4B_J2', 'narrative_journeys': 2,
    })
    course_path.write_text(json.dumps(course, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    story_doc = SOURCE.read_text(encoding='utf-8').replace('## The Ecosystem Energy Exchange Hall and the Ledger That Would Not Balance', f'## {TITLE}', 1)
    (DOCS / 'UNIT8_F4B_JOURNEY2_STORY.md').write_text(story_doc, encoding='utf-8')

    rows = []
    for s in scenes:
        for beat in s['story_beats']:
            rows.append((s['locus_id'], s['locus'], beat['object_id'], beat['term'], 'YES' if beat['exact_name'] else 'NO', beat['scope_class'], beat['science']))
    matrix = [
        '# Unit 8 F4B Journey 2 Story Matrix', '',
        f'Journey **U8-J2 Ecosystem Energy Exchange Hall** contains **9 polished scenes**, **47 locked F3 knowledge records**, **24 exact-name targets**, and **3 optional first-exposure Quick Recalls**.', '',
        '| Locus | Location | Knowledge ID | Term | Exact name | Scope | Locked science |',
        '|---|---|---|---|---:|---|---|',
    ]
    for row in rows:
        matrix.append('| ' + ' | '.join(str(x).replace('|', '\\|') for x in row) + ' |')
    (DOCS / 'UNIT8_F4B_STORY_MATRIX.md').write_text('\n'.join(matrix) + '\n', encoding='utf-8')

    release_manifest = {
        'schema': 'memory-palace-v2-unit8-f4b-release-1.0',
        'generated_utc': GENERATED_UTC,
        'unit_id': 'unit-8', 'release_status': status['status'], 'student_release': False, 'preview_release': True,
        'journey_id': 'U8-J2', 'journeys_polished': 2, 'f4b_scenes': 9, 'f4b_knowledge_records': 47, 'f4b_exact_name_targets': exact_targets,
        'f4b_optional_first_exposure_recalls': checkpoints, 'f4b_narrative_words': total_words,
        'cumulative_polished_scenes': 21, 'cumulative_polished_knowledge_records': 97, 'cumulative_narrative_words': j1_words + total_words,
        'canonical_records': 255, 'permanent_loci_architecture': 58, 'scene_briefs': 58, 'memory_objects': 0, 'application_challenges': 0,
        'scientific_lock': 'LOCKED_F1', 'architecture_lock': 'LOCKED_F2', 'scene_brief_lock': 'LOCKED_F3', 'prior_narrative_lock': 'LOCKED_F4A_J1', 'narrative_lock': 'LOCKED_F4B_J2',
        'next_stage': 'F4C Journey 3 polished narrative after F4B regression',
    }
    (U8 / 'f4b-release-manifest.json').write_text(json.dumps(release_manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    lock_files = [
        U8 / 'narrative-source-f4b.md',
        U8 / 'journeys' / 'U8-J2.json',
        U8 / 'journeys-f4b.json',
        U8 / 'status-f4b.json',
        U8 / 'f4b-release-manifest.json',
        DOCS / 'UNIT8_F4B_JOURNEY2_STORY.md',
        DOCS / 'UNIT8_F4B_STORY_MATRIX.md',
    ]
    content_lock = {
        'schema': 'memory-palace-v2-unit8-f4b-lock-1.0', 'unit_id': 'unit-8', 'lock_status': 'LOCKED_F4B_J2',
        'student_release': False, 'preview_release': True,
        'protected_prior_locks': ['f1-source-lock.json', 'content-lock-f2.json', 'content-lock-f3.json', 'content-lock-f4a.json'],
        'journey_id': 'U8-J2', 'scene_count': 9, 'knowledge_record_count': 47, 'exact_name_target_count': exact_targets, 'checkpoint_count': checkpoints,
        'files': {str(p.relative_to(U8)) if U8 in p.parents else str(p.relative_to(ROOT)): {'bytes': p.stat().st_size, 'sha256': sha256(p)} for p in lock_files},
        'rule': 'Journey 2 polished prose may not change after F4B without a new explicit narrative version. Journey 1 F4A prose remains frozen. F1 science, F2 classification and geometry, and F3 scene briefs remain authoritative boundaries.',
    }
    (U8 / 'content-lock-f4b.json').write_text(json.dumps(content_lock, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    return {'journey': journey, 'status': status, 'release_manifest': release_manifest}


if __name__ == '__main__':
    result = build()
    print(json.dumps({'status': result['status']['status'], 'scenes': result['status']['f4b_scene_count'], 'records': result['status']['f4b_knowledge_records'], 'words': result['status']['f4b_narrative_words']}, indent=2))
