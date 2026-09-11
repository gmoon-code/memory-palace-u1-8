from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
U8 = ROOT / 'content' / 'ap-biology' / 'unit-8'
DOCS = ROOT / 'docs'
SOURCE = U8 / 'narrative-source-f4g.md'
BRIEFS = json.loads((U8 / 'briefs' / 'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS = json.loads((U8 / 'briefs' / 'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J7 = next(j for j in JBRIEFS if j['journey_id'] == 'U8-J7')
B = {b['locus_id']: b for b in BRIEFS if b['journey_id'] == 'U8-J7'}
CANON = {r['Knowledge ID']: r for r in json.loads((U8 / 'canonical-catalog.json').read_text(encoding='utf-8'))}

ROUTE_META = [
    ('U8-L47', 'Community Composition Counter', 'Richness, relative abundance, and species diversity', 'composition counter', 'COUNT→PROPORTION→DIVERSITY'),
    ('U8-L48', 'Simpson Index Calculation Table', 'Simpson diversity index', 'index table', 'n→N→1−Σ(n/N)²→INTERPRET'),
    ('U8-L49', 'Biodiversity Resilience Observatory', 'Biodiversity and resilience', 'resilience dome', 'LEVELS→DISTURBANCE→CONDITIONAL RECOVERY'),
    ('U8-L50', 'Community Influence Removal Test', 'Keystone and foundation effects', 'removal test', 'ABUNDANCE→REMOVAL→COMMUNITY EFFECT'),
]

TITLE = 'The Observatory Where Equal Counts Told Different Stories'
TAGLINE = 'Four fixed stations, one community sample card, and one rule. No count, index, recovery curve, or famous species name is allowed to stand in for the ecological relationship it measures.'
PREMISE = 'The Diversity and Resilience Observatory receives communities that look identical when only species counts are considered. Dr. Mira Sen carries one fixed community sample card through four stations so richness, relative abundance, Simpson diversity, biodiversity, resilience, and species influence can be separated by visible evidence.'
MISSION = 'Travel the locked F2 route in order. Keep one community sample visible while moving from composition to the AP Simpson index, then to biodiversity and disturbance response, and finally to species-removal evidence that separates keystone from foundation effects.'
FINALE = 'The observatory becomes readable when the learner can explain why equal richness can hide different abundance structure, why n and N occupy different roles in the AP Simpson equation, why biodiversity-resilience claims must remain conditional, and why keystone status depends on effect relative to abundance within a specific interaction network.'
CONTINUITY_NAME = 'community sample card'
CONTINUITY_VISUAL = 'one fixed community sample card carrying species counts, total N, the diversity readout, and an intervention panel for disturbance or species removal through all four locations'
CONTINUITY_JOB = 'preserves the same community evidence while the question changes from composition to index interpretation to resilience and species influence'


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w’′'-]+\b", text))


def parse_source() -> list[dict]:
    text = SOURCE.read_text(encoding='utf-8')
    parts = re.split(r'^###\s+', text, flags=re.M)[1:]
    if len(parts) != 4:
        raise ValueError(f'Expected 4 scene sections, found {len(parts)}')
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
        'name': J7['unit_guide']['name'],
        'role': J7['unit_guide']['role'],
        'visual': J7['unit_guide']['visual_identity'],
        'story_job': J7['unit_guide']['behavior_rule'],
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
                'story': f"the {b['micro_anchor']} where the ecological measurement, equation meaning, disturbance response, or community effect becomes visible before the term is named",
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
            'next_locus': ROUTE_META[idx+1][0] if idx + 1 < len(ROUTE_META) else None,
            'f3_scene_brief_id': b['scene_brief_id'],
            'narrative_word_count': wc,
        })

    if len(all_ids) != 15 or len(set(all_ids)) != 15:
        raise ValueError(f'Expected 15 unique Journey 7 knowledge records, got {len(all_ids)} refs and {len(set(all_ids))} unique')
    if exact_targets != 9:
        raise ValueError(f'Expected 9 exact-name targets, got {exact_targets}')
    if checkpoints != 2:
        raise ValueError(f'Expected 2 checkpoints, got {checkpoints}')

    journey = {
        'palace_id': 'U8-J7',
        'unit_id': 'unit-8',
        'palace_name': 'Diversity and Resilience Observatory',
        'story_title': TITLE,
        'tagline': TAGLINE,
        'guide': guide,
        'premise': PREMISE,
        'mission': MISSION,
        'finale': FINALE,
        'estimated_minutes': 17,
        'scene_count': 4,
        'checkpoint_count': checkpoints,
        'student_release': 'DEVELOPER_PREVIEW_F4G',
        'preview_release': True,
        'narrative_design': 'U8-F4G-NARRATIVE-1.0',
        'learner_rule': 'Keep one community sample card visible through all four stations. Separate species count from proportional composition, species-specific n from total N, species diversity from broader biodiversity, conditional resilience from guaranteed recovery, and disproportionate keystone effect from high-abundance or habitat-forming foundation influence.',
        'route_orientation': 'The observatory follows one continuous route in F2 order through Community Composition Counter, Simpson Index Calculation Table, Biodiversity Resilience Observatory, and Community Influence Removal Test. Every location fixes left, center, and right before the ecological measurement or intervention changes.',
        'route': route,
        'scenes': scenes,
        'source_brief_lock': 'LOCKED_F3',
        'scientific_lock': 'LOCKED_F1',
        'architecture_lock': 'LOCKED_F2',
        'prior_narrative_locks': ['LOCKED_F4A_J1', 'LOCKED_F4B_J2', 'LOCKED_F4C_J3', 'LOCKED_F4D_J4', 'LOCKED_F4E_J5', 'LOCKED_F4F_J6'],
    }

    (U8 / 'journeys').mkdir(exist_ok=True)
    (U8 / 'journeys/U8-J7.json').write_text(json.dumps(journey, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    prior = [json.loads((U8 / f'journeys/U8-J{i}.json').read_text(encoding='utf-8')) for i in (1, 2, 3, 4, 5, 6)]
    summaries = []
    for j in [*prior, journey]:
        summaries.append({k: j[k] for k in ['palace_id', 'palace_name', 'story_title', 'tagline', 'guide', 'premise', 'mission', 'finale', 'estimated_minutes', 'scene_count', 'checkpoint_count', 'student_release', 'narrative_design']})
    total_scene_count = sum(j['scene_count'] for j in [*prior, journey])
    total_checkpoint_count = sum(j['checkpoint_count'] for j in [*prior, journey])
    summary = {
        'schema': 'memory-palace-v2-unit8-f4g-journeys-1.0',
        'unit_id': 'unit-8', 'stage': 'F4G', 'student_release': False, 'preview_release': True,
        'journey_count': 7, 'scene_count': total_scene_count, 'checkpoint_count': total_checkpoint_count,
        'guided_journeys': summaries,
    }
    (U8 / 'journeys-f4g.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    prior_words = [sum(s['narrative_word_count'] for s in j['scenes']) for j in prior]
    prior_records = [sum(len(s['object_ids']) for s in j['scenes']) for j in prior]
    polished_records = sum(prior_records) + len(all_ids)
    cumulative_words = sum(prior_words) + total_words
    prior_exact = [35, 24, 11, 18, 8, 23]
    prior_recalls = [2, 3, 2, 2, 2, 3]
    status = {
        'unit_id': 'unit-8', 'number': 8, 'title': 'Ecology',
        'status': 'F4G_JOURNEY7_POLISHED_DEVELOPER_PREVIEW',
        'pipeline_stage': 'UNIT8_F4G_JOURNEY7_NARRATIVE',
        'canonical_lock': 'LOCKED_F1', 'architecture_lock': 'LOCKED_F2', 'scene_brief_lock': 'LOCKED_F3',
        'narrative_lock_j1': 'LOCKED_F4A_J1', 'narrative_lock_j2': 'LOCKED_F4B_J2', 'narrative_lock_j3': 'LOCKED_F4C_J3', 'narrative_lock_j4': 'LOCKED_F4D_J4', 'narrative_lock_j5': 'LOCKED_F4E_J5', 'narrative_lock_j6': 'LOCKED_F4F_J6', 'narrative_lock_j7': 'LOCKED_F4G_J7',
        'student_release': False, 'preview_release': True,
        'journey_count': 7, 'scene_count': total_scene_count, 'memory_objects': 0, 'application_challenges': 0,
        'canonical_records': 255, 'architecture_journeys': 8, 'architecture_bundles': 22, 'architecture_loci': 58, 'scene_briefs': 58,
        'palace_managed_records': 211, 'challenge_lab_records': 13, 'scope_guard_records': 31, 'exact_name_review_targets': 135, 'confusable_sets': 40, 'optional_first_exposure_recalls': 18,
    }
    for idx, letter in enumerate('abcdef'):
        key = f'f4{letter}'
        status.update({
            f'{key}_journey': f'U8-J{idx+1}',
            f'{key}_scene_count': prior[idx]['scene_count'],
            f'{key}_knowledge_records': prior_records[idx],
            f'{key}_exact_name_targets': prior_exact[idx],
            f'{key}_optional_recalls': prior_recalls[idx],
            f'{key}_narrative_words': prior_words[idx],
        })
    status.update({
        'f4g_journey': 'U8-J7', 'f4g_scene_count': 4, 'f4g_knowledge_records': 15, 'f4g_exact_name_targets': exact_targets, 'f4g_optional_recalls': checkpoints, 'f4g_narrative_words': total_words,
        'polished_journey_count': 7, 'polished_scene_count': total_scene_count, 'polished_knowledge_records': polished_records, 'polished_narrative_words': cumulative_words,
        'next_required_output': 'F4H polished narrative for Journey 8 only after Journeys 1 through 7 remain frozen and all F1 through F4G regression gates continue to pass.',
        'next_gate': 'UNIT8_F4H_JOURNEY8_POLISHED_NARRATIVE',
    })
    (U8 / 'status-f4g.json').write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (U8 / 'status.json').write_text(json.dumps(status, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    course_path = ROOT / 'content/ap-biology/course.json'
    course = json.loads(course_path.read_text(encoding='utf-8'))
    unit = next(x for x in course['units'] if x['unit_id'] == 'unit-8')
    unit.update({
        'status': status['status'], 'journey_count': 7, 'scene_count': total_scene_count, 'student_release': False, 'preview_release': True,
        'source_status': 'AUDITED_F1_ARCHITECTURE_F2_BRIEFS_F3_NARRATIVE_F4A_F4B_F4C_F4D_F4E_F4F_F4G', 'pipeline_stage': status['pipeline_stage'],
        'narrative_lock': 'LOCKED_F4A_J1_LOCKED_F4B_J2_LOCKED_F4C_J3_LOCKED_F4D_J4_LOCKED_F4E_J5_LOCKED_F4F_J6_LOCKED_F4G_J7', 'narrative_journeys': 7,
    })
    course_path.write_text(json.dumps(course, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    story_doc = SOURCE.read_text(encoding='utf-8')
    (DOCS / 'UNIT8_F4G_JOURNEY7_STORY.md').write_text(story_doc, encoding='utf-8')

    rows = []
    for s in scenes:
        for beat in s['story_beats']:
            rows.append((s['locus_id'], s['locus'], beat['object_id'], beat['term'], 'YES' if beat['exact_name'] else 'NO', beat['scope_class'], beat['science']))
    matrix = [
        '# Unit 8 F4G Journey 7 Story Matrix', '',
        f'Journey **U8-J7 Diversity and Resilience Observatory** contains **4 polished scenes**, **15 locked F3 knowledge records**, **{exact_targets} exact-name targets**, and **2 optional first-exposure Quick Recalls**.', '',
        '| Locus | Location | Knowledge ID | Term | Exact name | Scope | Locked science |',
        '|---|---|---|---|---:|---|---|',
    ]
    for row in rows:
        matrix.append('| ' + ' | '.join(str(x).replace('|', '\\|') for x in row) + ' |')
    (DOCS / 'UNIT8_F4G_STORY_MATRIX.md').write_text('\n'.join(matrix) + '\n', encoding='utf-8')

    generated_utc = '2026-09-09T04:35:00+00:00'
    release_manifest = {
        'schema': 'memory-palace-v2-unit8-f4g-release-1.0', 'generated_utc': generated_utc,
        'unit_id': 'unit-8', 'release_status': status['status'], 'student_release': False, 'preview_release': True,
        'journey_id': 'U8-J7', 'journeys_polished': 7, 'f4g_scenes': 4, 'f4g_knowledge_records': 15, 'f4g_exact_name_targets': exact_targets,
        'f4g_optional_first_exposure_recalls': checkpoints, 'f4g_narrative_words': total_words,
        'cumulative_polished_scenes': total_scene_count, 'cumulative_polished_knowledge_records': polished_records, 'cumulative_narrative_words': cumulative_words,
        'canonical_records': 255, 'permanent_loci_architecture': 58, 'scene_briefs': 58, 'memory_objects': 0, 'application_challenges': 0,
        'scientific_lock': 'LOCKED_F1', 'architecture_lock': 'LOCKED_F2', 'scene_brief_lock': 'LOCKED_F3',
        'prior_narrative_locks': ['LOCKED_F4A_J1', 'LOCKED_F4B_J2', 'LOCKED_F4C_J3', 'LOCKED_F4D_J4', 'LOCKED_F4E_J5', 'LOCKED_F4F_J6'], 'narrative_lock': 'LOCKED_F4G_J7',
        'next_stage': 'F4H Journey 8 polished narrative after F4G regression',
    }
    (U8 / 'f4g-release-manifest.json').write_text(json.dumps(release_manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    lock_files = [
        U8 / 'narrative-source-f4g.md', U8 / 'journeys/U8-J7.json', U8 / 'journeys-f4g.json', U8 / 'status-f4g.json', U8 / 'f4g-release-manifest.json',
        DOCS / 'UNIT8_F4G_JOURNEY7_STORY.md', DOCS / 'UNIT8_F4G_STORY_MATRIX.md',
    ]
    content_lock = {
        'schema': 'memory-palace-v2-unit8-f4g-lock-1.0', 'unit_id': 'unit-8', 'lock_status': 'LOCKED_F4G_J7',
        'student_release': False, 'preview_release': True,
        'protected_prior_locks': ['f1-source-lock.json', 'content-lock-f2.json', 'content-lock-f3.json', 'content-lock-f4a.json', 'content-lock-f4b.json', 'content-lock-f4c.json', 'content-lock-f4d.json', 'content-lock-f4e.json', 'content-lock-f4f.json'],
        'journey_id': 'U8-J7', 'scene_count': 4, 'knowledge_record_count': 15, 'exact_name_target_count': exact_targets, 'checkpoint_count': checkpoints,
        'files': {str(p.relative_to(U8)) if U8 in p.parents else str(p.relative_to(ROOT)): {'bytes': p.stat().st_size, 'sha256': sha256(p)} for p in lock_files},
        'rule': 'Journey 7 polished prose may not change after F4G without a new explicit narrative version. Journeys 1 through 6 remain frozen. F1 science, F2 classification and geometry, and F3 scene briefs remain authoritative boundaries.',
    }
    (U8 / 'content-lock-f4g.json').write_text(json.dumps(content_lock, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    return {'journey': journey, 'status': status, 'release_manifest': release_manifest}


if __name__ == '__main__':
    result = build()
    print(json.dumps({'status': result['status']['status'], 'scenes': result['status']['f4g_scene_count'], 'records': result['status']['f4g_knowledge_records'], 'words': result['status']['f4g_narrative_words']}, indent=2))
