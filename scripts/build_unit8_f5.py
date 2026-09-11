from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AP = ROOT / 'content' / 'ap-biology'
U8 = AP / 'unit-8'
COURSE = AP / 'course.json'
GEN = '2026-09-09T06:00:00+00:00'
RUNTIME = 'v2-apbio-0.29.0-u8-f5'


def read(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def redact_mixed(text: str, terms: list[str]):
    """Hide direct answer labels while preserving the scientific mechanism needed to discriminate choices.

    Mixed-discrimination items should test conceptual boundaries, so ordinary mechanism words,
    causal operators, and negation remain visible. This is intentionally less aggressive than
    exact-name Review redaction.
    """
    out=text
    for term in sorted(set(terms), key=len, reverse=True):
        cleaned=term.strip()
        if len(cleaned) < 2:
            continue
        out=re.sub(re.escape(cleaned), '_____', out, flags=re.I)
    # Named quantitative relationships can appear in canonical prose without the whole choice label.
    if any('dN/dt' in term for term in terms):
        out=re.sub(r'dN\s*/\s*dt\s*=\s*B\s*[−-]\s*D', '_____', out, flags=re.I)
        out=re.sub(r'dN\s*/\s*dt', '_____', out, flags=re.I)
    # For the Simpson n-versus-N set, hide the variable itself while keeping its biological meaning.
    if any(term.startswith('n in Simpson') or term.startswith('N in Simpson') for term in terms):
        out=re.sub(r'(?<![A-Za-z])n(?![A-Za-z])', '_____', out)
        out=re.sub(r'(?<![A-Za-z])N(?![A-Za-z])', '_____', out)
    out=re.sub(r'(_____\s*){2,}', '_____ ', out)
    out=re.sub(r'\s+([,.;:])', r'\1', out)
    return re.sub(r'\s{2,}', ' ', out).strip()


def canon_dict():
    rows = read(U8 / 'canonical-catalog.json')
    return {r['Knowledge ID']: r for r in rows}


def significant_tokens(text: str):
    stop = {
        'a','an','and','or','the','of','to','in','on','for','with','from','as','at','by','is','are','be','via','vs','versus',
        'into','across','over','through','effect','example','review','principle','model','relationship','equation','process',
        'population','populations','community','communities','ecosystem','ecosystems','species','ecological','biology','unit',
    }
    out=[]
    for t in re.findall(r"[A-Za-z0-9²ΣΔβ′'-]+", text):
        low=t.casefold()
        if low in stop or len(low)<3:
            continue
        out.append(low)
    return out


def redact(text: str, terms: list[str]):
    out=text
    # Long phrase replacements first. Avoid single-character replacements that would destroy ordinary prose.
    for term in sorted(set(terms), key=len, reverse=True):
        if not term or len(term.strip()) < 2:
            continue
        out=re.sub(re.escape(term), '_____', out, flags=re.I)
    toks=[]
    for term in terms:
        toks.extend(significant_tokens(term))
    for tok in sorted(set(toks), key=len, reverse=True):
        if len(tok) < 3:
            continue
        if re.match(r'^[A-Za-z0-9]+$', tok):
            stem=tok[:5] if len(tok)>=6 else tok
            out=re.sub(rf'\b{re.escape(stem)}[A-Za-z0-9-]*\b', '_____', out, flags=re.I)
        else:
            out=re.sub(re.escape(tok), '_____', out, flags=re.I)
    # Formula-sensitive cleanups for Unit 8 named relationships.
    if any('dN/dt' in t for t in terms):
        out=re.sub(r'dN\s*/\s*dt', '_____', out, flags=re.I)
        out=re.sub(r'B\s*[−-]\s*D', '_____', out)
    if any('Simpson' in t for t in terms):
        out=re.sub(r'1\s*[−-]\s*Σ\s*\([^)]*\)\s*[²2]?', '_____', out)
    out=re.sub(r'(_____\s*){2,}', '_____ ', out)
    out=re.sub(r'\s+([,.;:])', r'\1', out)
    return re.sub(r'\s{2,}', ' ', out).strip()


canon = canon_dict()
classification = read(U8 / 'architecture' / 'learning-classification-f2.json')
arch = read(U8 / 'architecture' / 'palace-architecture-f2.json')
class_by = {r['knowledge_id']: r for r in classification['records']}
journeys = [read(U8 / 'journeys' / f'U8-J{i}.json') for i in range(1, 9)]

beat_by={}
scene_by={}
scene_by_locus={}
for j in journeys:
    for s in j['scenes']:
        scene_by_locus[s['locus_id']] = {
            'journey_id': j['palace_id'],
            'journey_title': j['story_title'],
            'scene_index': s['scene_index'],
            'scene_title': s['locus'],
            'scene_heading': s.get('title',''),
            'locus_id': s['locus_id'],
        }
        for b in s['story_beats']:
            kid=b['object_id']
            if kid in beat_by:
                raise RuntimeError(f'duplicate story record {kid}')
            beat_by[kid]=b
            scene_by[kid]=scene_by_locus[s['locus_id']]

story_ids=sorted(beat_by)
challenge_ids=[r['knowledge_id'] for r in classification['records'] if r['destination']=='CHALLENGE_LAB']
scope_ids=[r['knowledge_id'] for r in classification['records'] if r['destination']=='SUPPORTING_NON_RUNTIME_SCOPE_GUARD']
assert len(canon)==255
assert len(story_ids)==211
assert len(challenge_ids)==13
assert len(scope_ids)==31
assert set(story_ids) | set(challenge_ids) | set(scope_ids) == set(canon)
assert not (set(story_ids)&set(challenge_ids) or set(story_ids)&set(scope_ids) or set(challenge_ids)&set(scope_ids))

# Confirm F4 narrative science matches F1 exactly.
for kid,b in beat_by.items():
    c=canon[kid]
    assert b['term']==c['Canonical Label'], (kid,b['term'],c['Canonical Label'])
    assert b['science']==c['Canonical Verified Statement'], kid

conf_sets_by_id={kid:[] for kid in story_ids}
for s in arch['mixed_discrimination_sets']:
    for kid in s['knowledge_ids']:
        if kid in conf_sets_by_id:
            conf_sets_by_id[kid].append(s['set_id'])

memory_objects=[]
for kid in story_ids:
    c=canon[kid]
    cl=class_by[kid]
    b=beat_by[kid]
    sc=scene_by[kid]
    exact=bool(cl.get('exact_name_recall'))
    memory_objects.append({
        'memory_object_id': kid,
        'source_knowledge_id': kid,
        'object_type': 'UNIT8_STORY_MEMORY_OBJECT',
        'canonical_term': b['term'],
        'canonical_definition': c['Canonical Verified Statement'],
        'canonical_scientific_language': 'English',
        'topic': c['Topic'],
        'scope_class': c['Scope Class'],
        'exact_name_required': 'YES' if exact else 'NO',
        'exact_spelling_required': 'NO',
        'name_support': cl['name_support'],
        'spelling_policy': cl['spelling_policy'],
        'retrieval_modes': cl['retrieval_modes'],
        'visual_mode': cl['visual_mode'],
        'palace_zone': sc['journey_title'],
        'primary_palace_locus': sc['scene_title'],
        'locus_id': sc['locus_id'],
        'scene_index': sc['scene_index'],
        'confusable_set_ids': conf_sets_by_id.get(kid, []),
        'story_hint': b.get('hint',''),
        'forward_prompt_name_to_meaning': f"Explain the scientific meaning of '{b['term']}' without relying on the story.",
        'reverse_prompt_meaning_to_name': (
            f"Retrieve the exact Unit 8 term or named relationship for this scientific role: {redact(c['Canonical Verified Statement'], [b['term']])}"
            if exact else None
        ),
        'productive_retrieval_target': b['term'],
        'scientific_lock_status': 'LOCKED_F1',
        'narrative_lock_status': 'LOCKED_F4A_F4H',
        'student_runtime': True,
        'ai_mutability': 'AI may vary mnemonic wording, hints, practice phrasing, language, pacing, and distractors. AI may not change the canonical term, locked scientific meaning, AP scope, confusable distinction, misconception guardrail, or any frozen F4A-F4H narrative.',
        'source_trace': c.get('Source Reference',''),
        'content_version': 1,
        'version_status': 'STUDENT_READY_F5',
    })

assert len(memory_objects)==211
assert sum(x['exact_name_required']=='YES' for x in memory_objects)==135
write(U8/'memory-objects-f5.json', {
    'schema':'memory-palace-v2-unit8-f5-memory-objects-1.0',
    'unit_id':'unit-8',
    'count':211,
    'exact_name_required_count':135,
    'memory_objects':memory_objects,
})

# Delayed exact-name Review.
review_targets=[]
for kid in story_ids:
    cl=class_by[kid]
    if not cl.get('exact_name_recall'):
        continue
    b=beat_by[kid]
    c=canon[kid]
    sc=scene_by[kid]
    answer=b['term']
    clue=redact(c['Canonical Verified Statement'], [answer])
    prompt='Which exact Unit 8 term, quantity, or named relationship matches this scientific description? '+clue
    hint_source=b.get('hint') or f"Return to {sc['scene_title']} and reconstruct the defining scientific action."
    hint=redact(hint_source, [answer])
    if len(hint)<25:
        hint=f"Return to {sc['scene_title']} and reconstruct the defining action before naming it."
    review_targets.append({
        'knowledge_id':kid,
        'target_answer':answer,
        'prompt':prompt,
        'hint':hint,
        'journey_id':sc['journey_id'],
        'scene_index':sc['scene_index'],
        'scene_title':sc['scene_title'],
        'canonical_science':c['Canonical Verified Statement'],
        'spelling_policy':cl['spelling_policy'],
        'initial_review_window_hours':[18,72],
    })
assert len(review_targets)==135
write(U8/'review-manifest-f5.json', {
    'schema':'memory-palace-v2-unit8-f5-review-manifest-1.0',
    'unit_id':'unit-8',
    'target_count':135,
    'non_exact_palace_records':76,
    'mandatory_spelling_targets':0,
    'visible_review_limit':5,
    'targets':review_targets,
})

# Mixed discrimination.
mixed=[]
for base in arch['mixed_discrimination_sets']:
    choices=[canon[kid]['Canonical Label'] for kid in base['knowledge_ids']]
    qs=[]
    for qi,(kid,answer) in enumerate(zip(base['knowledge_ids'],choices),1):
        clue='Which option best matches this scientific description? '+redact_mixed(canon[kid]['Canonical Verified Statement'], choices)
        if answer.casefold() in clue.casefold():
            raise RuntimeError(f'mixed clue leaked answer {answer} in {base["set_id"]}')
        qs.append({
            'question_id':f"{base['set_id']}-Q{qi:02d}",
            'prompt':clue,
            'choices':choices,
            'answer':answer,
            'explanation':canon[kid]['Canonical Verified Statement'],
            'knowledge_id':kid,
        })
    mixed.append({
        'set_id':base['set_id'],
        'title':base['title'],
        'purpose':base['purpose'],
        'knowledge_ids':base['knowledge_ids'],
        'terms':choices,
        'unlock_rule':'Schedule only after every associated Unit 8 knowledge record has been encountered in a story.',
        'initial_delay_hours':48,
        'questions':qs,
    })
mixed_q=sum(len(s['questions']) for s in mixed)
assert len(mixed)==40 and mixed_q==104
write(U8/'mixed-discrimination-f5.json', {
    'schema':'memory-palace-v2-unit8-f5-mixed-discrimination-1.0',
    'unit_id':'unit-8',
    'set_count':40,
    'question_count':104,
    'sets':mixed,
})

# Challenge Lab. These are the 13 F1/F2 PRACTICE_ONLY records. Calculations stay here, outside permanent palace scenes.
CHALLENGES = {
'U8-K-212': {
    'domain':'Behavioral ecology',
    'title':'Separate proximate and ultimate explanations in zebra warning behavior',
    'loci':['U8-L02','U8-L07'],
    'prompt':'At a water hole, some zebras stand watch while others drink. A watching zebra gives a warning call, and the drinking zebras immediately run away. Give one proximate explanation and one ultimate explanation for the running response. Your answer must identify the immediate cue or mechanism at the proximate level and a defensible survival or reproductive consequence at the ultimate level without treating future benefit as an immediate cause.',
    'answer':'A proximate explanation identifies the warning call as the immediate external cue that is detected by the zebras and triggers the running response through their sensory and nervous systems. An ultimate explanation addresses why a response to warning calls can be favored across generations, such as increasing the probability that individuals survive predator encounters and later reproduce. The survival consequence does not cause the individual zebra to run in that moment; it is an evolutionary-level explanation for why the response can persist.',
    'hint':'Return to the Two-Level Causation Desk and the sender-receiver communication gallery. Keep the same behavior visible while separating the immediate cue from the evolutionary consequence.'},
'U8-K-213': {
    'domain':'Behavioral ecology',
    'title':'Design a house-finch song-learning experiment',
    'loci':['U8-L03','U8-L09'],
    'prompt':'Design an experiment to test whether a house-finch song pattern depends on learning from other birds. State a null hypothesis and one alternative hypothesis, identify the independent and dependent variables, include an appropriate comparison or control group, list major constants, describe how young birds would be assigned and raised, predict results that would support each hypothesis, and explain why those results would distinguish an innate contribution from a learned contribution.',
    'answer':'One defensible design randomly assigns young finches before normal song learning to different acoustic environments. A control group hears normal adult conspecific songs, while an experimental group is isolated from adult song or hears a controlled alternative. The independent variable is song exposure and the dependent variable is a quantified feature of the adult song. Age, housing, diet, recording method, and measurement criteria should be held as constant as possible. A null hypothesis can state that song exposure does not change the measured adult song feature. An alternative can state that exposure changes that feature. Similar adult songs across exposure groups would support a strong innate contribution for the measured trait, whereas systematic group differences tied to exposure would support learning. The conclusion should remain limited to the song features actually measured.',
    'hint':'Return to the innate-learned comparison bay and the learning-modes wing. Change experience while keeping the organisms, developmental stage, measurement, and other conditions controlled.'},
'U8-K-214': {
    'domain':'Behavioral ecology',
    'title':'Use a stickleback sign stimulus to separate causal levels',
    'loci':['U8-L02','U8-L04'],
    'prompt':'A territorial male stickleback attacks a model only when a red underside is visible. Explain the behavior at both causal levels. Identify the proximate sign stimulus and resulting response, then propose a biologically plausible ultimate consequence of territorial aggression. Make clear which part of your explanation is an immediate trigger and which part concerns differential survival or reproductive success across generations.',
    'answer':'The red underside functions as a sign stimulus in this classic example and can trigger the male territorial attack response, which is the proximate level of explanation. An ultimate hypothesis asks how territorial aggression could affect reproductive success, for example by reducing access of rival males to a nesting area and thereby increasing the focal male’s opportunity to mate. The red cue is the immediate trigger; the possible reproductive consequence is an evolutionary explanation and is not the physical mechanism that produces the attack in the moment.',
    'hint':'Return to the Trigger Sequence Chamber after the Two-Level Causation Desk. Keep sign stimulus and fixed response together, then move the fitness consequence to the separate ultimate-explanation side.'},
'U8-K-215': {
    'domain':'Behavioral ecology',
    'title':'Analyze duckling imprinting at developmental and evolutionary levels',
    'loci':['U8-L02','U8-L08'],
    'prompt':'Young ducklings form a following response during a sensitive developmental period after exposure to an appropriate moving caregiver cue. Give a proximate explanation for the behavior and an ultimate hypothesis for why such a developmental response can be favored. Your answer must use the sensitive-period idea and must avoid claiming that imprinting universally means following the first organism or object seen.',
    'answer':'At the proximate level, exposure to an appropriate moving and calling caregiver cue during a sensitive developmental period can establish a learned following response. The developmental timing and sensory experience belong to the mechanism and development side of explanation. At the ultimate level, following a caregiver can increase access to protection, food, warmth, or other conditions that improve survival and later reproductive opportunity. The exact cues and developmental details vary by species, so “the first organism seen” should not be treated as a universal rule.',
    'hint':'Return to the Imprinting and Sensitive Period Timeline after the causal-question room. Locate the narrow developmental window first, then move to the separate survival or reproductive consequence panel.'},
'U8-K-216': {
    'domain':'Behavioral ecology',
    'title':'Evaluate raven food-calling explanations without population-good teleology',
    'loci':['U8-L02','U8-L07','U8-L11'],
    'prompt':'A researcher sees ravens feeding on a moose carcass. Loud calls by feeding ravens attract additional ravens, even though many animals defend concentrated food. Give a plausible proximate explanation for the calling, propose one or more testable ultimate hypotheses, and explain one reason food defense can also be favored in another ecological context. Do not assume that attracting others evolved “for the good of the population.”',
    'answer':'A proximate explanation could identify the carcass, nearby ravens, or associated sensory cues as stimuli that trigger calling through the birds’ immediate behavioral mechanisms. Ultimate explanations require evidence about fitness consequences to callers. Calling might provide direct benefits, reciprocal benefits, or inclusive-fitness benefits if attracted birds are relatives, but those possibilities must be tested rather than inferred from group benefit alone. In another species or context, defending food can increase an individual’s access to a limiting resource and thereby improve survival or reproductive success. The same ecological resource can therefore favor different strategies under different costs, benefits, social relationships, and resource conditions.',
    'hint':'Return to the two-level causation desk, the communication gallery, and the inclusive-fitness ledger. Ask who receives the immediate cue and who gains or pays a reproductive cost before proposing an ultimate hypothesis.'},
'U8-K-217': {
    'domain':'Ecosystems',
    'title':'Classify biotic and abiotic ecosystem components',
    'loci':['U8-L15'],
    'prompt':'A pond survey records living algae, dead leaf litter, dissolved nitrate, water temperature, sunlight, bacteria, a fish, and a submerged log that was once part of a tree. Classify each observation as biotic or abiotic using the Unit 8 definitions, and justify the cases that students often find ambiguous. Then explain why both categories can affect the same ecosystem process even though the labels refer to different kinds of components.',
    'answer':'Living algae, bacteria, fish, dead leaf litter, and the submerged log are biotic under the course definition because biotic factors include living or once-living components. Dissolved nitrate, water temperature, and sunlight are abiotic physical or chemical components. Both categories can influence the same process. For example, temperature and nitrate availability can affect algal growth, while algae, bacteria, and detrital material can alter nutrient transfer and oxygen demand. The classification identifies what a component is, not whether it has ecological effects.',
    'hint':'Return to the Ecological Scale Atrium and use the split biotic-abiotic panels. The key ambiguity is that once-living material stays on the biotic side even after it is no longer alive.'},
'U8-K-218': {
    'domain':'Ecosystem energetics',
    'title':'Interpret spatial variation in net primary production',
    'loci':['U8-L20','U8-L13'],
    'prompt':'A global map shows high net primary production in many warm, wet regions and lower values in deserts, polar regions, and some nutrient-limited waters. Explain what net primary production represents, identify at least two environmental constraints that can help account for spatial variation, and explain why the map alone does not justify one universal cause for every high- or low-productivity location.',
    'answer':'Net primary production is the rate at which primary producers store chemical energy as new biomass after subtracting their own respiratory use from gross primary production. Water availability, temperature, light, nutrient availability, and other local conditions can constrain producer growth and energy capture, so different combinations can help explain different regions. A spatial map is evidence of a pattern, while causal explanation requires information about the limiting conditions in each system. The same low NPP value can therefore arise from different constraints in different ecosystems.',
    'hint':'Return to the Production Accounting Ledger and the organism energy-budget counter. Keep GPP, producer respiration, and NPP separate, then ask which environmental input limits capture or biomass production in each region.'},
'U8-K-219': {
    'domain':'Population ecology',
    'title':'Interpret body size and population density without overclaiming causation',
    'loci':['U8-L27'],
    'prompt':'An ecological graph shows that species with larger average adult body size tend to occur at lower population densities than smaller-bodied species. Describe the relationship shown by the graph, give one biologically plausible explanation involving resource use, and state why the graph by itself does not prove that body size directly causes the density pattern in every species or habitat.',
    'answer':'The graph shows a negative association: larger-bodied species tend to have lower population densities in the sampled data. One plausible mechanism is that larger individuals often require more energy, space, or other resources per organism, so a fixed area may support fewer individuals. The graph alone is correlational evidence. Other traits, trophic level, habitat productivity, life history, spatial scale, and sampling can covary with body size, so a causal claim requires additional evidence or experimental and comparative controls.',
    'hint':'Return to the Population Survey Grid. Density is individuals per area or volume, so read the plotted relationship first and keep the proposed resource mechanism separate from what the graph directly demonstrates.'},
'U8-K-220': {
    'domain':'Population growth',
    'title':'Calculate exponential population change',
    'loci':['U8-L34','U8-L31'],
    'prompt':'A bunny population is modeled as growing exponentially with current population size N = 3,000 individuals and maximum per-capita growth rate rmax = 1.5 per year. Use dN/dt = rmaxN to calculate how many individuals are added per year at that moment. Then explain why exponential growth does not mean that the same absolute number of individuals will be added every subsequent year if the per-capita rate remains constant.',
    'answer':'Using dN/dt = rmaxN gives dN/dt = 1.5 × 3,000 = 4,500 individuals per year at that moment. The result is an absolute population change per unit time. Under the exponential model, rmax is a per-capita rate and N changes through time. If N becomes larger while the per-capita rate stays constant, multiplying rmax by the larger N gives a larger absolute increment. Exponential growth therefore produces increasing absolute additions rather than a fixed numerical increment.',
    'hint':'Return to the Exponential Growth Console and the earlier population-change ledger. Keep rmax as a per-capita parameter, N as current population size, and dN/dt as the resulting absolute change per unit time.'},
'U8-K-221': {
    'domain':'Population growth',
    'title':'Calculate and interpret logistic population growth',
    'loci':['U8-L36','U8-L35'],
    'prompt':'A hypothetical population has carrying capacity K = 2,000 individuals, current population size N = 1,200, and rmax = 1.0 per year. Use dN/dt = rmaxN((K − N)/K) to calculate the modeled population change at that moment. Explain what the result means and predict qualitatively what happens to the growth term as N moves closer to K.',
    'answer':'First calculate the unused-capacity fraction: (K − N)/K = (2,000 − 1,200)/2,000 = 800/2,000 = 0.4. Then dN/dt = 1.0 × 1,200 × 0.4 = 480 individuals per year, so the model predicts positive growth because N is below K. As N approaches K, the fraction (K − N)/K approaches zero, so the modeled growth rate approaches zero. K is an environment-dependent carrying capacity and the logistic curve is an idealized model rather than a guarantee of perfect real-world behavior.',
    'hint':'Return to the Logistic Growth Console and the Carrying Capacity Resource Ceiling. Calculate the capacity fraction before multiplying, then watch what happens to that fraction as N approaches K.'},
'U8-K-222': {
    'domain':'Community diversity',
    'title':'Compare species richness and relative abundance',
    'loci':['U8-L47'],
    'prompt':'Community 1 contains 100 trees distributed as 20A, 20B, 20C, 20D, and 20E. Community 2 also contains 100 trees but is distributed as 5A, 25B, 15C, 20D, and 35E. Compare the two communities in species richness and relative abundance. Then explain why richness alone cannot capture the difference in their species-diversity structure.',
    'answer':'Both communities have species richness of five because all five species A through E are present. Their relative abundances differ. Community 1 is evenly distributed at 20% per species, whereas Community 2 has unequal proportions, including only 5% A and 35% E. Richness records how many species occur, while relative abundance records how individuals are distributed among those species. Measures of species diversity incorporate both components, so communities can have equal richness while differing in diversity structure.',
    'hint':'Return to the Community Composition Counter. Keep the number of species in one display and the fraction of all individuals belonging to each species in another before deciding whether the communities are equivalent.'},
'U8-K-223': {
    'domain':'Biodiversity and environmental change',
    'title':'Interpret a diversity-invasion graph cautiously',
    'loci':['U8-L49','U8-L52'],
    'prompt':'A class graph shows lower survival or ecological success of an introduced species in samples with higher native-species biodiversity. Describe the association represented by the graph and state one hypothesis that could explain it. Then explain why the graph should not be converted into the absolute rule that greater biodiversity always prevents invasion or that diversity alone caused the pattern.',
    'answer':'The graph represents a negative association between native biodiversity and the measured success of the introduced species in the displayed data. One hypothesis is that more diverse communities can use resources more completely or contain more competitors, consumers, or enemies that reduce establishment. The graph alone does not establish one causal mechanism, and biodiversity does not guarantee invasion resistance in every ecosystem or under every disturbance. Propagule pressure, traits of the introduced species, resource changes, disturbance, climate, and other factors can also affect invasion outcomes.',
    'hint':'Return to the Biodiversity Resilience Observatory and the Introduced-Invasive Range Gate. Read the plotted association first, then keep the contextual resilience claim separate from the criteria that make an introduced species invasive.'},
'U8-K-224': {
    'domain':'Cross-unit energy transfer',
    'title':'Transfer photosynthesis knowledge to a thylakoid-virus scenario',
    'loci':['U8-L16','U8-L17','U8-L20'],
    'prompt':'In a forest community, a dominant plant species becomes infected with a virus that disrupts thylakoid membranes. Identify the photosynthetic process most directly affected and explain the likely consequences for the infected individual plants. Connect the cellular effect to energy capture and biomass production without treating the detailed thylakoid mechanism as a new Unit 8 permanent-memory target.',
    'answer':'The light-dependent reactions are most directly affected because their photosystems, electron-transfer components, and ATP-producing machinery are associated with thylakoid membranes. Disrupting those membranes reduces the plant’s ability to capture light energy and produce the ATP and reducing power needed to support carbon fixation. As photosynthetic output falls, glucose and other organic-molecule production can decline, limiting growth and potentially causing severe stress or death. In Unit 8 this is a transfer task connecting cellular photosynthesis to primary production; the detailed thylakoid mechanism belongs to the earlier cellular-energetics content.',
    'hint':'Return to the Energy-Matter Split Gate, the autotroph energy-capture workshop, and the Production Accounting Ledger. Trace reduced light-energy capture forward to reduced chemical-energy storage and new biomass.'},
}
assert set(CHALLENGES)==set(challenge_ids)

lab_items=[]
for idx,kid in enumerate(challenge_ids,1):
    spec=CHALLENGES[kid]
    locs=spec['loci']
    lab_items.append({
        'challenge_id':f'U8-CL-{idx:02d}',
        'knowledge_id':kid,
        'domain':spec['domain'],
        'title':spec['title'],
        'type':'APPLICATION_TRANSFER',
        'prerequisite_loci':locs,
        'prerequisite_scene_titles':[scene_by_locus[l]['scene_title'] for l in locs],
        'prompt':spec['prompt'],
        'answer_guide':spec['answer'],
        'story_hint':spec['hint'],
        'canonical_statement':canon[kid]['Canonical Verified Statement'],
        'success_criterion':'Solve the unfamiliar problem from ordinary scientific information, show the requested reasoning, calculation, evidence interpretation, or experimental logic, and preserve the named ecological distinctions. Recognition of a palace image alone is not sufficient.',
        'practice_only_runtime':True,
        'source_assessment':canon[kid].get('Assessment Evidence',''),
    })
write(U8/'application-lab.json', {
    'schema':'memory-palace-v2-unit8-f5-challenge-lab-1.0',
    'unit_id':'unit-8',
    'title':'Unit 8 Challenge Lab',
    'student_intro':'Use these after the related journeys. One challenge appears at a time so behavior, ecosystem energetics, population ecology, community ecology, biodiversity, and environmental-change reasoning are practiced without depending on the mnemonic story.',
    'challenge_count':13,
    'practice_only_runtime_count':13,
    'practice_only_runtime_object_ids':challenge_ids,
    'items':lab_items,
})

# Scope guards remain non-runtime constraints.
guards=[]
for kid in scope_ids:
    c=canon[kid]
    guards.append({
        'knowledge_id':kid,
        'canonical_label':c['Canonical Label'],
        'policy':'NON_RUNTIME_AP_SCOPE_OR_SCIENTIFIC_BOUNDARY',
        'canonical_statement':c['Canonical Verified Statement'],
        'student_runtime':False,
        'permanent_palace':False,
        'challenge_lab':False,
        'enforcement':'May support teacher explanation, prevent misconceptions or over-teaching, and constrain student-facing wording, but must not become a required student memorization target, exact-name Review target, or Challenge Lab requirement.',
    })
write(U8/'scope-guards-f5.json', {
    'schema':'memory-palace-v2-unit8-f5-scope-guards-1.0',
    'unit_id':'unit-8',
    'guard_count':31,
    'guards':guards,
})

# Student-ready journey registry without modifying any frozen Journey JSON.
guided=[]
for j in journeys:
    guided.append({
        'palace_id':j['palace_id'],
        'palace_name':j['palace_name'],
        'story_title':j['story_title'],
        'tagline':j['tagline'],
        'guide':j['guide'],
        'premise':j['premise'],
        'mission':j['mission'],
        'finale':j['finale'],
        'estimated_minutes':j['estimated_minutes'],
        'scene_count':j['scene_count'],
        'checkpoint_count':j['checkpoint_count'],
        'student_release':'STUDENT_READY_F5',
        'narrative_design':j['narrative_design'],
        'preview_release':False,
    })
write(U8/'journeys-f5.json', {
    'schema':'memory-palace-v2-unit8-f5-registry-1.0',
    'unit_id':'unit-8',
    'stage':'F5',
    'student_release':True,
    'preview_release':False,
    'journey_count':8,
    'scene_count':58,
    'checkpoint_count':18,
    'guided_journeys':guided,
    'narrative_standard':'V2-NARRATIVE-3.0-F5-STUDENT-READY',
    'release_status':'STUDENT_READY_F5',
})

# Zero-loss finalization.
finalization={
    'schema':'memory-palace-v2-unit8-f5-finalization-1.0',
    'unit_id':'unit-8',
    'release_status':'STUDENT_READY_F5',
    'canonical_records':255,
    'runtime_memory_objects':211,
    'story_records':211,
    'challenge_lab_records':13,
    'scope_guard_records':31,
    'accounted_records':255,
    'unaccounted_records':0,
    'guided_journeys':8,
    'permanent_loci':58,
    'optional_first_exposure_recalls':18,
    'exact_name_review_targets':135,
    'non_exact_palace_records':76,
    'mandatory_spelling_targets':0,
    'mixed_discrimination_sets':40,
    'mixed_discrimination_questions':104,
    'review_policy':{
        'first_exposure':'Quick Recall remains sparse and optional. The 18 frozen F4 checkpoints are unchanged.',
        'exact_name':'Only the 135 F2 records explicitly marked exact_name_recall enter delayed exact-name Review.',
        'mixed_discrimination':'Confusable-set practice unlocks only after all set members have been encountered and is delayed at least 48 hours.',
        'visible_review_load':'Show no more than five due Review items at one time.',
        'spelling':'No mandatory Unit 8 spelling gate. Spelling support remains adaptive only.',
    },
    'destinations':{
        'story':story_ids,
        'challenge_lab':challenge_ids,
        'scope_guards':scope_ids,
    },
    'release_gate':{
        'science_lock':'PASS_F1',
        'architecture_lock':'PASS_F2',
        'scene_brief_lock':'PASS_F3',
        'narratives':'PASS_F4A_F4H',
        'runtime_memory_objects':'PASS_F5',
        'challenge_lab':'PASS_F5',
        'scope_guards':'PASS_F5',
        'mixed_discrimination':'PASS_F5',
        'exact_name_review':'PASS_F5',
        'zero_loss_accounting':'PASS_F5',
    },
}
write(U8/'finalization-f5.json',finalization)

# Status and course registry.
status=read(U8/'status-f4h.json')
status.update({
    'status':'STUDENT_READY',
    'pipeline_stage':'UNIT8_FINALIZED_F5',
    'pipeline_status':'UNIT8_FINALIZED_F5',
    'narrative_lock':'LOCKED_F4A_F4H_J1_J8',
    'student_release':True,
    'preview_release':False,
    'journey_count':8,
    'scene_count':58,
    'memory_objects':211,
    'runtime_memory_objects':211,
    'application_challenges':13,
    'canonical_records_accounted':255,
    'unaccounted_canonical_records':0,
    'practice_only_records':13,
    'scope_guard_records':31,
    'mixed_discrimination_sets':40,
    'mixed_discrimination_questions':104,
    'exact_name_review_targets':135,
    'non_exact_palace_records':76,
    'mandatory_spelling_targets':0,
    'polished_journeys':8,
    'polished_scenes':58,
    'next_required_output':'Classroom/browser validation of the released Unit 8 experience.',
    'next_gate':'Unit 8 F6 browser/classroom validation.',
})
write(U8/'status-f5.json',status)
write(U8/'status.json',status)

course=read(COURSE)
cu8=next(u for u in course['units'] if u['unit_id']=='unit-8')
cu8.update({
    'status':'STUDENT_READY',
    'journey_count':8,
    'scene_count':58,
    'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5',
    'polished_journeys':8,
    'polished_scenes':58,
    'student_release':True,
    'preview_release':False,
    'application_challenges':13,
    'scope_guard_records':31,
    'canonical_records_accounted':255,
    'runtime_memory_objects':211,
    'mixed_discrimination_sets':40,
    'mixed_discrimination_questions':104,
    'exact_name_review_targets':135,
    'non_exact_palace_records':76,
    'pipeline_stage':'UNIT8_FINALIZED_F5',
})
write(COURSE,course)

# Runtime integration.
settings_path=ROOT/'backend/settings.py'
settings=settings_path.read_text(encoding='utf-8')
if 'UNIT8_DIR' not in settings:
    settings=settings.replace('UNIT7_DIR = APBIO_DIR / "unit-7"\n', 'UNIT7_DIR = APBIO_DIR / "unit-7"\nUNIT8_DIR = APBIO_DIR / "unit-8"\n')
settings_path.write_text(settings,encoding='utf-8')

content_path=ROOT/'backend/content.py'
content=content_path.read_text(encoding='utf-8')
desired_settings_import = 'from .settings import APBIO_DIR, UNIT1_DIR, UNIT2_DIR, UNIT3_DIR, UNIT4_DIR, UNIT5_DIR, UNIT6_DIR, UNIT7_DIR, UNIT8_DIR'
content = re.sub(r'^from \.settings import APBIO_DIR, UNIT1_DIR, UNIT2_DIR, UNIT3_DIR, UNIT4_DIR, UNIT5_DIR, UNIT6_DIR, UNIT7_DIR(?:, UNIT8_DIR)*$',
                 desired_settings_import, content, count=1, flags=re.M)
if 'def unit8_status()' not in content:
    anchor='@lru_cache(maxsize=1)\ndef unit7_finalization(): return _read_json(UNIT7_DIR / "finalization-f5.json")\n'
    extra=anchor+'''\n@lru_cache(maxsize=1)\ndef unit8_status(): return _read_json(UNIT8_DIR / "status.json")\n@lru_cache(maxsize=1)\ndef unit8_canonical_catalog(): return _read_json(UNIT8_DIR / "canonical-catalog.json")\n@lru_cache(maxsize=1)\ndef unit8_architecture(): return _read_json(UNIT8_DIR / "architecture" / "palace-architecture-f2.json")\n@lru_cache(maxsize=1)\ndef unit8_scene_briefs(): return _read_json(UNIT8_DIR / "briefs" / "scene-briefs-f3.json")\n@lru_cache(maxsize=1)\ndef unit8_journey_briefs(): return _read_json(UNIT8_DIR / "briefs" / "journey-briefs-f3.json")\n@lru_cache(maxsize=1)\ndef unit8_memory_objects(): return _read_json(UNIT8_DIR / "memory-objects-f5.json")\n@lru_cache(maxsize=1)\ndef unit8_application_lab(): return _read_json(UNIT8_DIR / "application-lab.json")\n@lru_cache(maxsize=1)\ndef unit8_review_manifest(): return _read_json(UNIT8_DIR / "review-manifest-f5.json")\n@lru_cache(maxsize=1)\ndef unit8_mixed_discrimination(): return _read_json(UNIT8_DIR / "mixed-discrimination-f5.json")\n@lru_cache(maxsize=1)\ndef unit8_scope_guards(): return _read_json(UNIT8_DIR / "scope-guards-f5.json")\n@lru_cache(maxsize=1)\ndef unit8_finalization(): return _read_json(UNIT8_DIR / "finalization-f5.json")\n'''
    if anchor not in content:
        raise RuntimeError('backend/content.py Unit 7 helper anchor missing')
    content=content.replace(anchor,extra)

old='''    if unit_id == "unit-7":\n        path=UNIT7_DIR / "journeys-f5.json"\n        return _read_json(path)["guided_journeys"] if path.exists() and unit7_status().get("student_release") is True else []\n    return []\n'''
new='''    if unit_id == "unit-7":\n        path=UNIT7_DIR / "journeys-f5.json"\n        return _read_json(path)["guided_journeys"] if path.exists() and unit7_status().get("student_release") is True else []\n    if unit_id == "unit-8":\n        path=UNIT8_DIR / "journeys-f5.json"\n        return _read_json(path)["guided_journeys"] if path.exists() and unit8_status().get("student_release") is True else []\n    return []\n'''
if old in content:
    content=content.replace(old,new)

old='''    elif unit_id == "unit-7":\n        if unit7_status().get("student_release") is not True: return None\n        path=UNIT7_DIR / "journeys" / f"{palace_id}.json"\n    else: return None\n'''
new='''    elif unit_id == "unit-7":\n        if unit7_status().get("student_release") is not True: return None\n        path=UNIT7_DIR / "journeys" / f"{palace_id}.json"\n    elif unit_id == "unit-8":\n        if unit8_status().get("student_release") is not True: return None\n        path=UNIT8_DIR / "journeys" / f"{palace_id}.json"\n    else: return None\n'''
if old in content:
    content=content.replace(old,new)

old='''    if unit_id=="unit-7":\n        path=UNIT7_DIR / "memory-objects-f5.json"\n        if path.exists() and unit7_status().get("student_release") is True: return {o["memory_object_id"]:o for o in unit7_memory_objects()["memory_objects"]}\n        records=unit7_source_lock()["canonical_catalog"]\n        return {r["knowledge_id"]:{"memory_object_id":r["knowledge_id"],"canonical_term":r["canonical_label"],"canonical_definition":r["canonical_verified_statement"],"source_reference":r.get("source_reference",""),"canonical_lock":r.get("canonical_lock","")} for r in records}\n    return {}\n'''
new='''    if unit_id=="unit-7":\n        path=UNIT7_DIR / "memory-objects-f5.json"\n        if path.exists() and unit7_status().get("student_release") is True: return {o["memory_object_id"]:o for o in unit7_memory_objects()["memory_objects"]}\n        records=unit7_source_lock()["canonical_catalog"]\n        return {r["knowledge_id"]:{"memory_object_id":r["knowledge_id"],"canonical_term":r["canonical_label"],"canonical_definition":r["canonical_verified_statement"],"source_reference":r.get("source_reference",""),"canonical_lock":r.get("canonical_lock","")} for r in records}\n    if unit_id=="unit-8":\n        path=UNIT8_DIR / "memory-objects-f5.json"\n        if path.exists() and unit8_status().get("student_release") is True: return {o["memory_object_id"]:o for o in unit8_memory_objects()["memory_objects"]}\n        records=unit8_canonical_catalog()\n        return {r["Knowledge ID"]:{"memory_object_id":r["Knowledge ID"],"canonical_term":r["Canonical Label"],"canonical_definition":r["Canonical Verified Statement"],"source_reference":r.get("Source Reference",""),"canonical_lock":r.get("Canonical Lock","")} for r in records}\n    return {}\n'''
if old in content:
    content=content.replace(old,new)

old='''    elif unit_id=="unit-7":\n        out.update(unit7_status())\n    return out\n'''
new='''    elif unit_id=="unit-7":\n        out.update(unit7_status())\n    elif unit_id=="unit-8":\n        out.update(unit8_status())\n    return out\n'''
if old in content:
    content=content.replace(old,new)
content_path.write_text(content,encoding='utf-8')

main_path=ROOT/'backend/main.py'
main=main_path.read_text(encoding='utf-8')
main=re.sub(r'app=FastAPI\(title="Memory Palace V2 · AP Biology",version="[^"]+"\)', 'app=FastAPI(title="Memory Palace V2 · AP Biology",version="0.29.0-u8-f5")', main)
main=re.sub(r"def health\(\): return \{'ok':True,'version':'[^']+'\}", "def health(): return {'ok':True,'version':'v2-apbio-0.29.0-u8-f5'}", main)
for marker,insert in [
    ("    if unit_id=='unit-7': return content.unit7_architecture()\n", "    if unit_id=='unit-7': return content.unit7_architecture()\n    if unit_id=='unit-8': return content.unit8_architecture()\n"),
    ("    if unit_id=='unit-7': return content.unit7_scene_briefs()\n", "    if unit_id=='unit-7': return content.unit7_scene_briefs()\n    if unit_id=='unit-8': return content.unit8_scene_briefs()\n"),
    ("    if unit_id=='unit-7': return content.unit7_journey_briefs()\n", "    if unit_id=='unit-7': return content.unit7_journey_briefs()\n    if unit_id=='unit-8': return content.unit8_journey_briefs()\n"),
    ("    if unit_id=='unit-7': return content.unit7_application_lab()\n", "    if unit_id=='unit-7': return content.unit7_application_lab()\n    if unit_id=='unit-8': return content.unit8_application_lab()\n"),
    ("    if unit_id=='unit-7': return content.unit7_review_manifest()\n", "    if unit_id=='unit-7': return content.unit7_review_manifest()\n    if unit_id=='unit-8': return content.unit8_review_manifest()\n"),
    ("    if unit_id=='unit-7': return content.unit7_mixed_discrimination()\n", "    if unit_id=='unit-7': return content.unit7_mixed_discrimination()\n    if unit_id=='unit-8': return content.unit8_mixed_discrimination()\n"),
    ("    if unit_id=='unit-7': return content.unit7_finalization()\n", "    if unit_id=='unit-7': return content.unit7_finalization()\n    if unit_id=='unit-8': return content.unit8_finalization()\n"),
    ("    if unit_id=='unit-7': return content.unit7_scope_guards()\n", "    if unit_id=='unit-7': return content.unit7_scope_guards()\n    if unit_id=='unit-8': return content.unit8_scope_guards()\n"),
]:
    if "unit_id=='unit-8'" not in main[main.find(marker):main.find(marker)+len(insert)+80] if marker in main else True:
        if marker in main and insert not in main:
            main=main.replace(marker,insert)
main_path.write_text(main,encoding='utf-8')

# Consolidated Units 1-8 mainline manifest.
u17=read(AP/'mainline-release-u1-u7.json')
mainline={
    'schema':'memory-palace-v2-mainline-u1-u8-f5-1.0',
    'release_status':'STUDENT_READY_UNITS_1_8_UNIT8_F5',
    'units':['unit-1','unit-2','unit-3','unit-4','unit-5','unit-6','unit-7','unit-8'],
    'runtime_version':RUNTIME,
    'totals':{
        'canonical_records_units_1_8':u17['totals']['canonical_records_units_1_7']+255,
        'guided_journeys':u17['totals']['guided_journeys']+8,
        'permanent_scenes':u17['totals']['permanent_scenes']+58,
        'challenge_lab_items':u17['totals']['challenge_lab_items']+13,
    },
    'unit8':None,
    'future_units':[],
}

# F5 release manifest is written before the mainline embeds it.
release={
    'schema':'memory-palace-v2-unit8-f5-release-manifest-1.0',
    'generated_utc':GEN,
    'unit_id':'unit-8',
    'stage':'F5',
    'student_release':True,
    'preview_release':False,
    'canonical_records':255,
    'canonical_records_accounted':255,
    'unaccounted_canonical_records':0,
    'runtime_memory_objects':211,
    'story_records':211,
    'practice_only_records':13,
    'scope_guard_records':31,
    'guided_journeys':8,
    'permanent_loci':58,
    'challenge_count':13,
    'optional_first_exposure_recalls':18,
    'exact_name_review_targets':135,
    'non_exact_palace_records':76,
    'mandatory_spelling_targets':0,
    'mixed_discrimination_sets':40,
    'mixed_discrimination_questions':104,
    'runtime_version':RUNTIME,
    'next_stage':'UNIT8_BROWSER_CLASSROOM_VALIDATION_F6',
}
write(U8/'f5-release-manifest.json',release)
mainline['unit8']=release
write(AP/'mainline-release-u1-u8.json',mainline)

# F5 content lock after all runtime and registry files are final.
f5_files=['memory-objects-f5.json','application-lab.json','review-manifest-f5.json','mixed-discrimination-f5.json','scope-guards-f5.json','finalization-f5.json','journeys-f5.json','status-f5.json','f5-release-manifest.json']
runtime_files=['backend/main.py','backend/content.py','backend/settings.py','frontend/js/app.js','frontend/js/api.js','frontend/js/audio.js','frontend/js/state.js','frontend/js/views/home.js','frontend/js/views/learn.js','frontend/js/views/review.js','frontend/js/views/practice.js']
lock={
    'schema':'memory-palace-v2-unit8-f5-content-lock-1.0',
    'unit_id':'unit-8',
    'stage':'F5',
    'student_release':True,
    'files':{f:sha(U8/f) for f in f5_files},
    'protected_narratives':{f'journeys/U8-J{i}.json':sha(U8/'journeys'/f'U8-J{i}.json') for i in range(1,9)},
    'protected_upstream_locks':{
        'f1-source-lock.json':sha(U8/'f1-source-lock.json'),
        'content-lock-f2.json':sha(U8/'content-lock-f2.json'),
        'content-lock-f3.json':sha(U8/'content-lock-f3.json'),
        **{f'content-lock-f4{x}.json':sha(U8/f'content-lock-f4{x}.json') for x in 'abcdefgh'},
    },
    'runtime_file_sha256':{rel:sha(ROOT/rel) for rel in runtime_files},
}
write(U8/'content-lock-f5.json',lock)

print('Built Unit 8 F5')
print(json.dumps(release,indent=2))
