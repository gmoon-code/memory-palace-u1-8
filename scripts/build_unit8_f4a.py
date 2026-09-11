from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
U8 = ROOT / 'content' / 'ap-biology' / 'unit-8'
DOCS = ROOT / 'docs'
SOURCE = U8 / 'narrative-source-f4a.md'
BRIEFS = json.loads((U8 / 'briefs' / 'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS = json.loads((U8 / 'briefs' / 'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J1 = next(j for j in JBRIEFS if j['journey_id'] == 'U8-J1')
B = {b['locus_id']: b for b in BRIEFS if b['journey_id'] == 'U8-J1'}
CANON = {r['Knowledge ID']: r for r in json.loads((U8 / 'canonical-catalog.json').read_text(encoding='utf-8'))}

ROUTE_META = [
    ('U8-L01', 'Institute entry response bay', 'Entry bay', 'Institute entrance', 'CUE'),
    ('U8-L02', 'Two-Level Causation Desk', 'Causation', 'Analysis desk', 'HOW/WHY'),
    ('U8-L03', 'Behavior Origin Comparison Bay', 'Origin', 'Comparison bay', 'INNATE/LEARNED'),
    ('U8-L04', 'Trigger Sequence Chamber', 'Trigger', 'Sequence chamber', 'RED'),
    ('U8-L05', 'Migration Navigation Dome', 'Migration', 'Navigation dome', 'COMPASS'),
    ('U8-L06', 'Movement Gradient Arena', 'Movement', 'Gradient arena', 'TRACKS'),
    ('U8-L07', 'Communication Sender-Receiver Gallery', 'Signals', 'Communication gallery', 'SEND→RECEIVE'),
    ('U8-L08', 'Developmental Learning Timeline Room', 'Sensitive period', 'Timeline room', 'WINDOW'),
    ('U8-L09', 'Learning Modes Wing', 'Learning modes', 'Learning wing', 'MAP/PAIR/OBSERVE'),
    ('U8-L10', 'Fitness Tradeoff Hall', 'Tradeoffs', 'Fitness hall', 'GAIN/RISK'),
    ('U8-L11', 'Inclusive Fitness Ledger Chamber', 'Inclusive fitness', 'Ledger chamber', 'DIRECT+KIN'),
    ('U8-L12', 'Plant Response Greenhouse', 'Plants', 'Greenhouse', 'GROW'),
]

GENERATED_UTC = '2026-09-09T02:55:00+00:00'
TITLE = 'The Institute Where Every Response Looked the Same'
TAGLINE = 'Twelve dark nameplates, one stimulus-response tablet, and one rule. Identify the cue, responder, mechanism, experience, output, and consequence before the institute can separate one biological response from another.'
PREMISE = 'The Behavioral Response Institute has lost the distinctions among behavior, explanation level, learning, movement, communication, social fitness effects, and plant response. Dr. Mira Sen carries one transparent stimulus-response tablet through twelve fixed rooms. Each room can relight only after the visible biological mechanism separates the current concept from its nearest confusable alternative.'
MISSION = 'Travel the locked F2 route in order. Keep cue, responder, immediate mechanism, experience, behavioral output, and fitness or homeostasis consequence visible while separating proximate from ultimate explanation, innate from learned contribution, fixed response from trigger, migration from navigation cue, kinesis from taxis, signal from receiver response, imprinting from other learning, learning modes from one another, mating systems by relationship, altruism from cooperation, and phototaxis from phototropism.'
FINALE = 'The twelve room nameplates relight only after the learner can reconstruct each response from its cue and biological consequence. The route ends in the greenhouse with animal movement still distinct from directional plant growth and with behavioral explanations framed through mechanism, development, experience, survival, reproduction, and evolutionary history without intention or teleology.'


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w’′'-]+\b", text))


def parse_source() -> list[dict]:
    text = SOURCE.read_text(encoding='utf-8')
    parts = re.split(r'^###\s+', text, flags=re.M)[1:]
    if len(parts) != 12:
        raise ValueError(f'Expected 12 scene sections, found {len(parts)}')
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
        'name': J1['unit_guide']['name'],
        'role': J1['unit_guide']['role'],
        'visual': J1['unit_guide']['visual_identity'],
        'story_job': J1['unit_guide']['behavior_rule'],
    }
    continuity = J1['continuity_object']

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
            # Source may bold the term while the locked brief does not.
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
                {'name': 'Transparent stimulus-response tablet', 'kind': 'journey continuity object', 'visual': 'a clear tablet with fixed fields for cue, responder, immediate mechanism, experience, behavioral output, and fitness or homeostasis consequence', 'job': 'keeps the same causal fields visible across all twelve rooms without replacing the real organisms, structures, signals, growth responses, or outcomes'},
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

    if len(all_ids) != 50 or len(set(all_ids)) != 50:
        raise ValueError(f'Expected 50 unique F3-assigned records, got {len(all_ids)} / {len(set(all_ids))}')
    if exact_targets != 35:
        raise ValueError(f'Expected 35 exact-name targets, got {exact_targets}')
    if checkpoints != 2:
        raise ValueError(f'Expected 2 checkpoints, got {checkpoints}')

    journey = {
        'palace_id': 'U8-J1',
        'unit_id': 'unit-8',
        'palace_name': 'Behavioral Response Institute',
        'story_title': TITLE,
        'tagline': TAGLINE,
        'guide': guide,
        'premise': PREMISE,
        'mission': MISSION,
        'finale': FINALE,
        'estimated_minutes': 34,
        'scene_count': 12,
        'checkpoint_count': checkpoints,
        'student_release': 'DEVELOPER_PREVIEW_F4A',
        'preview_release': True,
        'narrative_design': 'U8-F4A-NARRATIVE-1.0',
        'learner_rule': 'Place yourself in the room and fix left, center, and right before following the biological action. The same transparent stimulus-response tablet persists through all twelve locations. Exact terms appear only after the defining mechanism or comparison is visible. Optional Quick Recall appears only twice.',
        'route_orientation': 'The institute follows one continuous black floor line through twelve permanent locations in F2 order. Enter at Institute entry response bay and continue through Two-Level Causation Desk, Behavior Origin Comparison Bay, Trigger Sequence Chamber, Migration Navigation Dome, Movement Gradient Arena, Communication Sender-Receiver Gallery, Developmental Learning Timeline Room, Learning Modes Wing, Fitness Tradeoff Hall, Inclusive Fitness Ledger Chamber, and Plant Response Greenhouse. Every room fixes left, center, and right before the biological state changes.',
        'route': route,
        'scenes': scenes,
        'source_brief_lock': 'LOCKED_F3',
        'scientific_lock': 'LOCKED_F1',
        'architecture_lock': 'LOCKED_F2',
    }

    (U8 / 'journeys').mkdir(exist_ok=True)
    journey_path = U8 / 'journeys' / 'U8-J1.json'
    journey_path.write_text(json.dumps(journey, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    summary = {
        'schema': 'memory-palace-v2-unit8-f4a-journeys-1.0',
        'unit_id': 'unit-8',
        'stage': 'F4A',
        'student_release': False,
        'preview_release': True,
        'journey_count': 1,
        'scene_count': 12,
        'checkpoint_count': checkpoints,
        'guided_journeys': [{k: journey[k] for k in ['palace_id', 'palace_name', 'story_title', 'tagline', 'guide', 'premise', 'mission', 'finale', 'estimated_minutes', 'scene_count', 'checkpoint_count', 'student_release', 'narrative_design']}],
    }
    (U8 / 'journeys-f4a.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    status = {
        'unit_id': 'unit-8', 'number': 8, 'title': 'Ecology',
        'status': 'F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW',
        'pipeline_stage': 'UNIT8_F4A_JOURNEY1_NARRATIVE',
        'canonical_lock': 'LOCKED_F1', 'architecture_lock': 'LOCKED_F2', 'scene_brief_lock': 'LOCKED_F3', 'narrative_lock': 'LOCKED_F4A_J1',
        'student_release': False, 'preview_release': True,
        'journey_count': 1, 'scene_count': 12, 'memory_objects': 0, 'application_challenges': 0,
        'canonical_records': 255, 'architecture_journeys': 8, 'architecture_bundles': 22, 'architecture_loci': 58, 'scene_briefs': 58,
        'palace_managed_records': 211, 'challenge_lab_records': 13, 'scope_guard_records': 31, 'exact_name_review_targets': 135, 'confusable_sets': 40, 'optional_first_exposure_recalls': 18,
        'f4a_journey': 'U8-J1', 'f4a_scene_count': 12, 'f4a_knowledge_records': 50, 'f4a_exact_name_targets': exact_targets, 'f4a_optional_recalls': checkpoints, 'f4a_narrative_words': total_words,
        'next_required_output': 'F4B polished narrative for Journey 2 only after Journey 1 remains frozen and the F4A prose, spatial, scientific, causal, terminology, memorability, and regression gates continue to pass.',
        'next_gate': 'UNIT8_F4B_JOURNEY2_POLISHED_NARRATIVE',
    }
    (U8 / 'status-f4a.json').write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (U8 / 'status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    course_path = ROOT / 'content' / 'ap-biology' / 'course.json'
    course = json.loads(course_path.read_text(encoding='utf-8'))
    unit = next(x for x in course['units'] if x['unit_id'] == 'unit-8')
    unit.update({
        'status': status['status'], 'journey_count': 1, 'scene_count': 12, 'student_release': False, 'preview_release': True,
        'source_status': 'AUDITED_F1_ARCHITECTURE_F2_BRIEFS_F3_NARRATIVE_F4A', 'pipeline_stage': status['pipeline_stage'],
        'narrative_lock': 'LOCKED_F4A_J1', 'narrative_journeys': 1,
    })
    course_path.write_text(json.dumps(course, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    story_doc = SOURCE.read_text(encoding='utf-8').replace('## The Behavioral Response Institute and the Twelve Unlabeled Rooms', f'## {TITLE}', 1)
    (DOCS / 'UNIT8_F4A_JOURNEY1_STORY.md').write_text(story_doc, encoding='utf-8')

    rows = []
    for s in scenes:
        for beat in s['story_beats']:
            rows.append((s['locus_id'], s['locus'], beat['object_id'], beat['term'], 'YES' if beat['exact_name'] else 'NO', beat['scope_class'], beat['science']))
    matrix = [
        '# Unit 8 F4A Journey 1 Story Matrix', '',
        f'Journey **U8-J1 Behavioral Response Institute** contains **12 polished scenes**, **50 locked F3 knowledge records**, **35 exact-name targets**, and **2 optional first-exposure Quick Recalls**.', '',
        '| Locus | Location | Knowledge ID | Term | Exact name | Scope | Locked science |',
        '|---|---|---|---|---:|---|---|',
    ]
    for row in rows:
        matrix.append('| ' + ' | '.join(str(x).replace('|', '\\|') for x in row) + ' |')
    (DOCS / 'UNIT8_F4A_STORY_MATRIX.md').write_text('\n'.join(matrix) + '\n', encoding='utf-8')

    release_manifest = {
        'schema': 'memory-palace-v2-unit8-f4a-release-1.0',
        'generated_utc': GENERATED_UTC,
        'unit_id': 'unit-8', 'release_status': status['status'], 'student_release': False, 'preview_release': True,
        'journey_id': 'U8-J1', 'journeys': 1, 'scenes': 12, 'knowledge_records': 50, 'exact_name_targets': exact_targets,
        'optional_first_exposure_recalls': checkpoints, 'narrative_words': total_words,
        'canonical_records': 255, 'permanent_loci_architecture': 58, 'scene_briefs': 58, 'memory_objects': 0, 'application_challenges': 0,
        'scientific_lock': 'LOCKED_F1', 'architecture_lock': 'LOCKED_F2', 'scene_brief_lock': 'LOCKED_F3', 'narrative_lock': 'LOCKED_F4A_J1',
        'next_stage': 'F4B Journey 2 polished narrative after F4A regression',
    }
    (U8 / 'f4a-release-manifest.json').write_text(json.dumps(release_manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    lock_files = [
        U8 / 'narrative-source-f4a.md',
        U8 / 'journeys' / 'U8-J1.json',
        U8 / 'journeys-f4a.json',
        U8 / 'status-f4a.json',
        U8 / 'f4a-release-manifest.json',
        DOCS / 'UNIT8_F4A_JOURNEY1_STORY.md',
        DOCS / 'UNIT8_F4A_STORY_MATRIX.md',
    ]
    content_lock = {
        'schema': 'memory-palace-v2-unit8-f4a-lock-1.0', 'unit_id': 'unit-8', 'lock_status': 'LOCKED_F4A_J1',
        'student_release': False, 'preview_release': True,
        'protected_prior_locks': ['f1-source-lock.json', 'content-lock-f2.json', 'content-lock-f3.json'],
        'journey_id': 'U8-J1', 'scene_count': 12, 'knowledge_record_count': 50, 'exact_name_target_count': exact_targets, 'checkpoint_count': checkpoints,
        'files': {str(p.relative_to(U8)) if U8 in p.parents else str(p.relative_to(ROOT)): {'bytes': p.stat().st_size, 'sha256': sha256(p)} for p in lock_files},
        'rule': 'Journey 1 polished prose may not change after F4A without a new explicit narrative version. F1 science, F2 classification and geometry, and F3 scene briefs remain authoritative boundaries.',
    }
    (U8 / 'content-lock-f4a.json').write_text(json.dumps(content_lock, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    return {'journey': journey, 'status': status, 'release_manifest': release_manifest}


if __name__ == '__main__':
    result = build()
    print(json.dumps({'status': result['status']['status'], 'scenes': result['status']['f4a_scene_count'], 'records': result['status']['f4a_knowledge_records'], 'words': result['status']['f4a_narrative_words']}, indent=2))
