from __future__ import annotations
import json, hashlib, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content'/'ap-biology'/'unit-7'
AP=ROOT/'content'/'ap-biology'
COURSE=AP/'course.json'


def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,d): Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def significant_tokens(text):
    stop={'a','an','and','or','the','of','to','in','on','for','with','from','as','at','by','is','are','be','via','vs','versus','into','across','over','through','population','populations','evolution','evolutionary','effect','example','review','principle'}
    out=[]
    for t in re.findall(r"[A-Za-z0-9²β′'-]+",text):
        low=t.casefold()
        if low in stop or len(low)<3: continue
        out.append(low)
    return out

def redact(text,terms):
    out=text
    for term in sorted(set(terms),key=len,reverse=True):
        if term: out=re.sub(re.escape(term),'_____',out,flags=re.I)
    toks=[]
    for term in terms: toks.extend(significant_tokens(term))
    for tok in sorted(set(toks),key=len,reverse=True):
        stem=tok[:5] if len(tok)>=6 else tok[:max(3,len(tok)-1)]
        if re.match(r'^[A-Za-z0-9]+$',stem):
            out=re.sub(rf'\b{re.escape(stem)}[A-Za-z0-9-]*\b','_____',out,flags=re.I)
    out=re.sub(r'(_____\s*){2,}','_____ ',out)
    out=re.sub(r'\s+([,.;:])',r'\1',out)
    return re.sub(r'\s{2,}',' ',out).strip()

source=read(U7/'source'/'canonical-unit7-f1.json')
canon={r['knowledge_id']:r for r in source['canonical_catalog']}
classification=read(U7/'architecture'/'learning-classification-f2.json')
arch=read(U7/'architecture'/'palace-architecture-f2.json')
class_by={r['knowledge_id']:r for r in classification['records']}
journeys=[read(U7/'journeys'/f'U7-J{i}.json') for i in range(1,7)]
beat_by={}; scene_by={}
for j in journeys:
    for s in j['scenes']:
        for b in s['story_beats']:
            kid=b['object_id']
            if kid in beat_by: raise RuntimeError(f'duplicate story record {kid}')
            beat_by[kid]=b
            scene_by[kid]={'journey_id':j['palace_id'],'journey_title':j['story_title'],'scene_index':s['scene_index'],'scene_title':s['locus'],'locus_id':s['locus_id']}

story_ids=sorted(beat_by)
challenge_ids=[r['knowledge_id'] for r in classification['records'] if r['destination']=='CHALLENGE_LAB']
scope_ids=[r['knowledge_id'] for r in classification['records'] if r['scope_class']=='SCOPE_GUARD']
assert len(canon)==215 and len(story_ids)==174 and len(challenge_ids)==16 and len(scope_ids)==25
assert set(story_ids)|set(challenge_ids)|set(scope_ids)==set(canon)
assert not(set(story_ids)&set(challenge_ids) or set(story_ids)&set(scope_ids) or set(challenge_ids)&set(scope_ids))

# Runtime Memory Objects.
conf_sets_by_id={kid:[] for kid in story_ids}
for s in arch['confusable_sets']:
    for kid in s['knowledge_ids']:
        if kid in conf_sets_by_id: conf_sets_by_id[kid].append(s['set_id'])
memory_objects=[]
for kid in story_ids:
    c=canon[kid]; cl=class_by[kid]; b=beat_by[kid]; sc=scene_by[kid]
    exact=bool(cl.get('exact_name_recall'))
    memory_objects.append({
      'memory_object_id':kid,'source_knowledge_id':kid,'object_type':'UNIT7_STORY_MEMORY_OBJECT',
      'canonical_term':b['term'],'canonical_definition':c['canonical_verified_statement'],'canonical_scientific_language':'English',
      'topic':c['topic'],'scope_class':c['scope_class'],'exact_name_required':'YES' if exact else 'NO','exact_spelling_required':'NO',
      'name_support':cl['name_support'],'spelling_policy':cl['spelling_policy'],'retrieval_modes':cl['retrieval_modes'],
      'visual_mode':cl['visual_mode'],'palace_zone':sc['journey_title'],'primary_palace_locus':sc['scene_title'],'locus_id':sc['locus_id'],
      'scene_index':sc['scene_index'],'confusable_set_ids':conf_sets_by_id.get(kid,[]),'story_hint':b.get('hint',''),
      'forward_prompt_name_to_meaning':f"Explain the scientific meaning of '{b['term']}' without relying on the story.",
      'reverse_prompt_meaning_to_name':(f"Retrieve the exact Unit 7 term or named relationship for this scientific role: {redact(c['canonical_verified_statement'],[b['term']])}" if exact else None),
      'productive_retrieval_target':b['term'],'scientific_lock_status':'LOCKED_F1','narrative_lock_status':'LOCKED_F4F',
      'student_runtime':True,
      'ai_mutability':'AI may vary mnemonic wording, hints, practice phrasing, language, pacing, and distractors. AI may not change canonical term, locked scientific meaning, AP scope, confusable distinction, misconception guardrail, or the frozen F4F narrative.',
      'source_trace':c.get('source_reference',''),'content_version':1,'version_status':'STUDENT_READY_F5'
    })
assert sum(x['exact_name_required']=='YES' for x in memory_objects)==94
write(U7/'memory-objects-f5.json',{'schema':'memory-palace-v2-unit7-f5-memory-objects-1.0','unit_id':'unit-7','count':174,'exact_name_required_count':94,'memory_objects':memory_objects})

# Delayed exact-name Review.
review_targets=[]
for kid in story_ids:
    cl=class_by[kid]
    if not cl.get('exact_name_recall'): continue
    b=beat_by[kid]; c=canon[kid]; sc=scene_by[kid]; answer=b['term']
    prompt='Which exact Unit 7 term or named relationship matches this scientific description? '+redact(c['canonical_verified_statement'],[answer])
    hint_source=b.get('hint') or f"Return to {sc['scene_title']} and reconstruct the defining scientific action."
    hint=redact(hint_source,[answer])
    if len(hint)<25: hint=f"Return to {sc['scene_title']} and reconstruct the defining action before naming it."
    review_targets.append({'knowledge_id':kid,'target_answer':answer,'prompt':prompt,'hint':hint,'journey_id':sc['journey_id'],'scene_index':sc['scene_index'],'scene_title':sc['scene_title'],'canonical_science':c['canonical_verified_statement'],'spelling_policy':cl['spelling_policy'],'initial_review_window_hours':[18,72]})
assert len(review_targets)==94
write(U7/'review-manifest-f5.json',{'schema':'memory-palace-v2-unit7-f5-review-manifest-1.0','unit_id':'unit-7','target_count':94,'non_exact_palace_records':80,'mandatory_spelling_targets':0,'visible_review_limit':5,'targets':review_targets})

# Mixed discrimination.
mixed=[]
for base in arch['confusable_sets']:
    choices=base['terms']; qs=[]
    for qi,(kid,answer) in enumerate(zip(base['knowledge_ids'],choices),1):
        clue='Which option best matches this scientific description? '+redact(canon[kid]['canonical_verified_statement'],choices)
        if answer.casefold() in clue.casefold(): raise RuntimeError(f'mixed clue leaked answer {answer}')
        qs.append({'question_id':f"{base['set_id']}-Q{qi:02d}",'prompt':clue,'choices':choices,'answer':answer,'explanation':canon[kid]['canonical_verified_statement'],'knowledge_id':kid})
    mixed.append({'set_id':base['set_id'],'title':base['title'],'knowledge_ids':base['knowledge_ids'],'terms':choices,'unlock_rule':'Schedule only after every associated Unit 7 knowledge record has been encountered in a story.','initial_delay_hours':48,'questions':qs})
mixed_q=sum(len(s['questions']) for s in mixed)
assert len(mixed)==33 and mixed_q==102
write(U7/'mixed-discrimination-f5.json',{'schema':'memory-palace-v2-unit7-f5-mixed-discrimination-1.0','unit_id':'unit-7','set_count':33,'question_count':102,'sets':mixed})

# Challenge Lab. The 16 PRACTICE_ONLY records remain outside the permanent palace.
C={
'U7-K-173':('Natural selection','Diagnose natural-selection misconceptions',
 'Four students explain why a finch population developed deeper beaks after several generations of drought. Student A says the birds needed deeper beaks, so their bodies produced them. Student B says the strongest individual birds survived and therefore the species improved. Student C says heritable beak-depth variation already existed, drought changed which phenotypes left more offspring, and descendant phenotype frequencies changed. Student D says every surviving bird became genetically better adapted during its lifetime. Identify the scientifically defensible explanation and correct the specific errors in the other three claims.',
 'Student C gives the defensible explanation. Natural selection acts on existing heritable phenotypic variation, and the environment changes relative reproductive success among variants. Student A is teleological because need does not cause a directed adaptive variant to appear. Student B confuses fitness with physical strength and treats species improvement as a goal; evolutionary fitness is relative reproductive success in the relevant environment. Student D incorrectly assigns population-level genetic evolution to individuals within one lifetime. Individuals can survive, develop, or acclimate, while evolutionary genetic change is tracked across generations in populations.',
 'Return to the Population Change Platform, Competition and Offspring Gate, and Fitness Scale. Reconstruct heredity, differential reproduction, and population change before judging any claim about need or strength.'),
'U7-K-174':('Natural selection','Separate paca body-mass response from evolutionary change',
 'A wildfire sharply reduces fruit availability in a paca population. During the following dry season, many surviving pacas lose body mass because food is scarce. Researchers later compare offspring born after food supplies recover and find no inherited shift in adult body mass relative to the prefire population. A student says the fire caused the population to evolve smaller bodies. Evaluate that claim. State what evidence would be needed to support a heritable evolutionary interpretation and distinguish it from an environmentally induced within-lifetime response.',
 'The observed body-mass loss alone does not demonstrate evolution. Reduced food availability can cause individuals to lose mass within their lifetimes, which is an environmentally induced phenotypic response. To support evolutionary change, researchers would need evidence that heritable variants related to body mass differed in reproductive success and that the frequencies of those heritable variants or associated phenotypes changed across generations. The later absence of an inherited shift after food recovery supports a temporary environmental response rather than a demonstrated genetic evolutionary change in the population.',
 'Use the Changing Pressure Chamber. Keep the environmental change, an individual body response, heritable variation, and descendant-generation frequencies in separate places before deciding whether evolution occurred.'),
'U7-K-175':('Population genetics','Classify drift and gene-flow scenarios',
 'Classify each scenario as bottleneck effect, founder effect, or gene flow and justify the mechanism. Scenario 1. A hurricane reduces an island lizard population from 8,000 individuals to 35 survivors whose allele frequencies differ by chance from the original population. Scenario 2. Twelve birds from a large mainland population colonize a previously unoccupied island, and a rare source-population allele is unusually common among their descendants. Scenario 3. Pollen from a mainland plant population repeatedly fertilizes plants on a nearby island, causing the two populations to become more similar at several loci. For each case, identify the diagnostic evidence that rules out the other two mechanisms.',
 'Scenario 1 is a bottleneck effect because an existing population undergoes a severe demographic reduction and the survivors are a chance, nonrepresentative sample of the original gene pool. Scenario 2 is a founder effect because a small subset establishes a new population while the source population need not collapse. Scenario 3 is gene flow because alleles physically move between existing populations through gametes, here pollen, and the exchange tends to reduce genetic differences. Bottleneck and founder effects are forms of genetic drift driven by sampling; gene flow requires migration of individuals or gametes across a population boundary.',
 'Reconstruct the Genetic Drift Chamber, Bottleneck Gate, Founder Ferry, and Gene-Flow Bridge. Ask first whether the event is chance sampling within a demographic history or actual movement across a population boundary.'),
'U7-K-176':('Natural selection','Interpret selection-mode distributions',
 'A trait is measured in three separate populations before and after selection. In population A, the postselection distribution shifts toward larger trait values. In population B, intermediate values increase while both extremes become less common. In population C, both extremes increase while intermediate values decline. Identify the selection pattern for A, B, and C. For each population, describe the implied relative-fitness pattern without assuming that the same phenotype would be favored in every environment.',
 'Population A shows directional selection because one end of the phenotypic distribution has higher relative fitness and the distribution shifts toward that extreme. Population B shows stabilizing selection because intermediate phenotypes have higher relative fitness than the extremes, narrowing the distribution around the middle. Population C shows disruptive selection because both extremes have higher relative fitness than intermediate phenotypes, increasing representation at both ends. These patterns are environment dependent; the phenotype with higher reproductive success in one environment is not universally the fittest phenotype.',
 'Return to the Selection Distribution Gallery. Rebuild the before-and-after distributions first, then identify where relative reproductive success was highest rather than relying on the graph shape alone.'),
'U7-K-177':('Hardy-Weinberg','Reason from Hardy-Weinberg assumptions',
 'A diploid population is very large, has no migration or mutation at locus A, and genotypes have equal reproductive success. Individuals mate assortatively by genotype at locus A. Over one generation, homozygotes become more common and heterozygotes become less common, while the measured frequencies of the two alleles remain 0.60 and 0.40. Explain why this population can deviate from Hardy-Weinberg genotype expectations without demonstrating allele-frequency evolution. Then predict how your conclusion would change if one genotype also produced more surviving offspring.',
 'Random mating is a Hardy-Weinberg condition, so assortative mating can alter genotype frequencies and produce a departure from p², 2pq, and q² expectations. Nonrandom mating by itself does not necessarily change allele frequencies, which is consistent with p remaining 0.60 and q remaining 0.40 in the scenario. Therefore genotype-frequency deviation alone is not proof of microevolution defined as allele-frequency change. If one genotype also had higher reproductive success, natural selection could change allele frequencies across generations, and the population would then show evolutionary allele-frequency change as well as genotype-frequency differences.',
 'Use the Hardy-Weinberg Null-Model Station and Five-Condition Control Room. Keep allele frequencies on one strip and genotype frequencies on another, then ask which assumption was violated and which quantity actually changed.'),
'U7-K-178':('Hardy-Weinberg','Translate Hardy-Weinberg symbols correctly',
 'At a two-allele locus that meets Hardy-Weinberg assumptions, allele R has frequency 0.65 and allele r has frequency 0.35. Without treating R as dominant merely because it is assigned to p, identify p, q, p², 2pq, and q² and state what biological quantity each symbol represents. Then explain why the same symbols could be reassigned if the investigator chose the other allele as p, provided the notation was used consistently.',
 'One consistent assignment is p = 0.65 for allele R and q = 0.35 for allele r. p² = 0.4225 is the expected frequency of RR, 2pq = 0.455 is the expected frequency of Rr, and q² = 0.1225 is the expected frequency of rr under Hardy-Weinberg equilibrium. p and q are labels for allele frequencies, not universal dominance and recessiveness labels. The investigator could instead designate r as p and R as q, which would swap the symbol assignments while leaving the underlying allele and genotype frequencies unchanged.',
 'Return to the p/q Board and Genotype-Frequency Equation Board. Keep allele-copy frequencies above the board and expected whole-genotype frequencies below it, with no dominance labels attached to p or q.'),
'U7-K-179':('Hardy-Weinberg','Solve a recessive-phenotype Hardy-Weinberg problem',
 'In a large randomly mating population with no migration, mutation, or selection at a two-allele locus, 9% of individuals express a recessive phenotype known to occur only in genotype aa. Use Hardy-Weinberg reasoning to calculate q², q, p, p², and 2pq. State the assumption that permits the recessive phenotype frequency to be treated as q², and give the expected percentages of AA, Aa, and aa individuals.',
 'Because the phenotype is known to correspond uniquely to aa and Hardy-Weinberg assumptions are stated, q² = 0.09. Therefore q = sqrt(0.09) = 0.30. Since p + q = 1, p = 0.70. The expected AA frequency is p² = 0.49, or 49%. The expected heterozygote frequency is 2pq = 2(0.70)(0.30) = 0.42, or 42%. The expected aa frequency remains q² = 0.09, or 9%. The square-root step is justified here only because the observed recessive phenotype reliably identifies aa and Hardy-Weinberg genotype proportions are appropriate.',
 'Use the p/q Board, Genotype-Frequency Equation Board, and conditional recessive-phenotype panel. Do not take a square root until the phenotype-to-aa mapping and Hardy-Weinberg assumptions are explicitly satisfied.'),
'U7-K-180':('Hardy-Weinberg','Calculate allele frequencies directly from genotype counts',
 'A sample contains 100 diploid individuals with genotypes 45 AA, 40 Aa, and 15 aa. Calculate the frequencies of alleles A and a directly from genotype counts by counting allele copies. Then calculate the observed genotype frequencies. Do not assume Hardy-Weinberg equilibrium during the direct allele count. Finally state what additional step would be needed if you wanted to compare the observed genotype frequencies with Hardy-Weinberg expectations.',
 'There are 200 total allele copies because 100 diploid individuals contribute 2N copies. A copies equal 2(45) + 40 = 130, so f(A) = 130/200 = 0.65. a copies equal 2(15) + 40 = 70, so f(a) = 70/200 = 0.35. The observed genotype frequencies are 0.45 AA, 0.40 Aa, and 0.15 aa. These values come directly from the sample. To compare with Hardy-Weinberg expectations, separately use p = 0.65 and q = 0.35 to compute p², 2pq, and q², then compare expected and observed genotype frequencies.',
 'Return to the Genotype-Count Allele Counter. Open every genotype card into its two allele copies, fill the 2N counter, and only afterward move to a separate expected-frequency model if the question asks for it.'),
'U7-K-181':('Hardy-Weinberg','Distinguish allele and genotype frequencies',
 'A population sample has allele frequencies A = 0.70 and a = 0.30. Its observed genotype frequencies are AA = 0.60, Aa = 0.20, and aa = 0.20. Explain why the allele-frequency statement and genotype-frequency statement describe different population quantities. Calculate the Hardy-Weinberg expected genotype frequencies from the given allele frequencies and compare them with the observed values. Explain what the mismatch does and does not allow you to conclude.',
 'Allele frequencies count the proportions of allele copies in the gene pool, while genotype frequencies count the proportions of individuals with particular allele pairs. From p = 0.70 and q = 0.30, Hardy-Weinberg expectations are AA = p² = 0.49, Aa = 2pq = 0.42, and aa = q² = 0.09. The observed genotype distribution differs substantially from those expectations. That mismatch indicates that the locus or sample does not fit the stated Hardy-Weinberg null expectation and prompts investigation of assumptions or sampling. It does not, by itself, identify which evolutionary mechanism is responsible or prove that allele frequencies changed.',
 'Use the p/q Board and Observed-Expected Comparison Desk. Keep allele-copy proportions, observed genotype proportions, and model-generated expected genotype proportions in three separate visual layers.'),
'U7-K-182':('Evidence of evolution','Synthesize independent evidence for evolution',
 'Researchers investigate whether two island bird populations share a recent common ancestor. They have four data sets. Fossils from dated rock layers show related ancestral forms through time. The island birds resemble a nearby mainland lineage in skeletal structure. Homologous forelimb elements occur in the same underlying arrangement despite different functions. Aligned mitochondrial DNA sequences are highly similar between the island and nearby mainland populations. Identify the evidence category represented by each data set and explain how the lines can converge on a common-ancestry hypothesis without treating any single observation as complete proof.',
 'The dated fossils provide geological and fossil-record evidence of organisms and change through time. The island-mainland relationship provides biogeographic evidence. The corresponding skeletal pattern is morphological homology and supports shared ancestry. The aligned DNA similarity provides molecular evidence and can support closer relationship when homologous sequences are compared appropriately. These independent evidence streams answer somewhat different questions, but their compatible inferences strengthen a common-ancestry hypothesis. None of the individual observations alone is a complete reconstruction of evolutionary history, and dating evidence should not be confused with relationship evidence.',
 'Return to the Evidence Convergence Atrium, Fossil Timeline and Dating Vault, Homology Morphology Hall, and Molecular Evidence Scanner. Put each observation on its own evidence card before combining the inferences.'),
'U7-K-183':('Phylogeny','Read a phylogenetic tree from nodes',
 'A rooted tree has topology (Lancelet,(Shark,(Salamander,(Mouse,(Lizard,Pigeon))))). Identify the sister taxa in the most recent pair, identify an early-branching vertebrate lineage relative to the sampled tetrapods, and identify the most recent common ancestor shared by Mouse, Lizard, and Pigeon as an internal node rather than a living taxon. Then explain why rotating the Lizard-Pigeon branch would not change any of those ancestry relationships.',
 'Lizard and Pigeon are sister taxa because they descend immediately from the same most recent internal node. Shark is an early-branching sampled vertebrate lineage relative to the sampled tetrapod clade because its lineage splits before the node uniting Salamander, Mouse, Lizard, and Pigeon. The most recent common ancestor of Mouse, Lizard, and Pigeon is the internal node that gives rise to Mouse and to the Lizard-Pigeon lineage, not Mouse or any other living tip. Rotating a branch around an internal node changes display order only; the connections among nodes and descendants remain the same.',
 'Use the Tree Anatomy Board and Sister and Early-Branching Fork. Trace every relationship backward to the first shared internal node and ignore the left-to-right or top-to-bottom order of living tips.'),
'U7-K-184':('Phylogeny','Construct a cladogram from a character matrix',
 'An outgroup O lacks all four listed derived characters. Taxon A has character 1 only. Taxon B has characters 1 and 2. Taxon C has characters 1, 2, and 3. Taxon D has characters 1, 2, 3, and 4. Construct or choose the rooted cladogram that places each shared derived character on the fewest supported branches. State where characters 1 through 4 would be mapped, identify which taxa form nested clades, and explain how the outgroup helps infer character-state polarity.',
 'A parsimonious arrangement is (O,(A,(B,(C,D)))) if the matrix is interpreted as nested acquisition of characters. Character 1 maps on the branch leading to A, B, C, and D; character 2 maps on the branch leading to B, C, and D; character 3 maps on the branch leading to C and D; character 4 maps on the branch leading to D. O serves as an outgroup because it lies outside the focal ingroup and lacks the listed derived states, helping identify the absent state as ancestral for this comparison. The matrix supports nested clades because shared derived characters are inherited by descendants of the branch on which the change is mapped.',
 'Return to the Character Mapping Wall, Outgroup Reference Gate, and Phylogeny Evidence Construction Lab. Map one state change at a time and keep the outgroup outside the ingroup rather than making it an ancestor.'),
'U7-K-185':('Speciation','Discriminate prezygotic barriers',
 'Classify five reproductive-isolation scenarios and justify each classification. A. Two frog populations breed in different ponds and rarely encounter one another. B. Two plant populations flower in different months. C. Two bird populations overlap, but females respond only to their own population-specific courtship song. D. Closely related snail populations attempt to mate, but reproductive structures do not align effectively. E. Two sea-urchin species release gametes into the same water, but sperm cannot bind successfully to eggs of the other species. Name the barrier in each case and identify the reproductive step that is blocked.',
 'A is habitat isolation because the populations use different breeding habitats and therefore rarely encounter one another. B is temporal isolation because reproduction occurs at different times. C is behavioral isolation because courtship recognition prevents mating. D is mechanical isolation because structural incompatibility prevents effective mating or gamete transfer. E is gametic isolation because gametes are released into the same environment but recognition, survival, or fusion fails before zygote formation. All five are prezygotic barriers because they act before a zygote is successfully formed.',
 'Use the Prezygotic Barrier Entry, Habitat and Temporal Isolation Gates, and Behavioral-Mechanical-Gametic Gates. Place each scenario on the encounter-to-fertilization sequence and ask exactly which step fails.'),
'U7-K-186':('Speciation','Apply gene flow and reproductive isolation in an FRQ',
 'A river changes course and divides one lizard population into eastern and western populations for 20,000 generations. Genetic differences accumulate. When the river later dries, the populations come back into contact. They occupy the same habitat, but eastern females rarely respond to western courtship displays, and crosses that do occur produce viable F1 offspring with very low fertility. Explain the likely geographic mode of divergence, identify the reproductive barriers now present, and justify whether the evidence supports speciation more strongly than geographic separation alone would.',
 'The initial divergence is consistent with an allopatric history because a geographic barrier separated the populations and reduced gene flow. After secondary contact, behavioral isolation acts prezygotically because courtship differences reduce mating between the populations. Reduced hybrid fertility acts postzygotically because viable hybrids form but reproduce poorly. These reproductive barriers provide evidence of reproductive isolation after the geographic barrier disappears, so the evidence supports speciation more strongly than mere geographic separation would. Geographic isolation can initiate divergence, but speciation additionally requires sufficient reproductive isolation to maintain independent gene pools.',
 'Reconstruct the Species Boundary Desk, Allopatric Barrier Island, Sympatric Overlap Island, and Postzygotic Outcome Ward. Keep geographic separation, current overlap, prezygotic behavior, and hybrid fertility as separate evidence.'),
'U7-K-187':('Origins of life','Separate prebiotic evidence from later endosymbiosis',
 'Evaluate three claims. Claim 1. Miller and Urey showed that early-Earth conditions could produce small organic molecules abiotically, so their apparatus created the first living cells. Claim 2. An RNA-world model is scientifically interesting because RNA can store sequence information through complementary base pairing and some RNA molecules can catalyze reactions. Claim 3. Endosymbiosis explains how the first life arose when one nonliving chemical droplet engulfed another. For each claim, identify what evidence or model is actually supported and correct any chronological or mechanistic error.',
 'Claim 1 begins with a supported point but overstates the result. Miller-Urey-type experiments demonstrated abiotic production of small organic molecules under simulated conditions; they did not create cells, life, proteins, or nucleic acids. Claim 2 captures the logic of the RNA-world hypothesis because RNA can support information storage or copying through complementary base pairing and catalytic RNA molecules exist, making a combined informational and catalytic role plausible in early systems. Claim 3 is chronologically wrong. Endosymbiosis concerns later evolution of mitochondria and chloroplasts through interactions among already-living cells, not the initial origin of the first life from nonliving chemistry.',
 'Use the Early Earth Timeline Deck, Prebiotic Chemistry Chamber, Miller-Urey Simulation Rig, and RNA World and Later Endosymbiosis Archive. Keep small-molecule synthesis, RNA-based hypotheses, first cellular life, and later organelle evolution on different chronology slots.'),
'U7-K-213':('Speciation','Discriminate postzygotic barriers',
 'Classify each hybrid outcome as reduced hybrid viability, reduced hybrid fertility, or hybrid breakdown. Scenario A. Fertilization succeeds, but most hybrid embryos fail to develop to adulthood. Scenario B. F1 hybrids survive normally but produce very few functional gametes and rarely reproduce. Scenario C. F1 hybrids are viable and fertile, but when F1 individuals reproduce, many F2 offspring show severe developmental defects or greatly reduced fertility. Explain why all three are postzygotic barriers and identify the generation or life-history stage where each barrier becomes visible.',
 'Scenario A is reduced hybrid viability because a zygote forms but hybrid development or survival is impaired before normal reproductive adulthood. Scenario B is reduced hybrid fertility because viable F1 hybrids form yet fertility is low or absent. Scenario C is hybrid breakdown because F1 hybrids can be viable and fertile, while reduced viability or fertility appears in later hybrid generations such as F2. All three are postzygotic barriers because fertilization and zygote formation occur before the reproductive isolation becomes evident.',
 'Return to the Postzygotic Outcome Ward. Start at the zygote box and follow the same sequence through development, adult fertility, and later generations; classify the barrier by the first stage where failure appears.'),
}
assert set(C)==set(challenge_ids)
locus_title={x['locus_id']:x['title'] for x in arch['loci']}
arch_ch={x['knowledge_id']:x for x in arch['challenge_lab']}
items=[]
for idx,kid in enumerate(challenge_ids,1):
    domain,title,prompt,answer,hint=C[kid]; a=arch_ch[kid]
    items.append({'challenge_id':f'U7-CL-{idx:02d}','knowledge_id':kid,'domain':domain,'title':title,'type':a['retrieval_demand'],'prerequisite_loci':a['prerequisite_loci'],'prerequisite_scene_titles':[locus_title[x] for x in a['prerequisite_loci']],'prompt':prompt,'answer_guide':answer,'story_hint':hint,'canonical_statement':canon[kid]['canonical_verified_statement'],'success_criterion':'Solve the unfamiliar problem from ordinary scientific information, show the requested reasoning or mechanism, and keep the named distinctions separate. Recognition of a palace image alone is not sufficient.','practice_only_runtime':True})
write(U7/'application-lab.json',{'schema':'memory-palace-v2-unit7-f5-challenge-lab-1.0','unit_id':'unit-7','title':'Unit 7 Challenge Lab','student_intro':'Use these after the related journeys. One challenge appears at a time so natural selection, population genetics, Hardy-Weinberg reasoning, evolutionary evidence, phylogeny, speciation, and origins-of-life evidence are practiced without depending on the mnemonic story.','challenge_count':16,'practice_only_runtime_count':16,'practice_only_runtime_object_ids':[x['knowledge_id'] for x in items],'items':items})

# Scope guards.
guards=[]
for kid in scope_ids:
    c=canon[kid]
    guards.append({'knowledge_id':kid,'canonical_label':c['canonical_label'],'policy':'NON_RUNTIME_AP_SCOPE_OR_SCIENTIFIC_BOUNDARY','canonical_statement':c['canonical_verified_statement'],'student_runtime':False,'permanent_palace':False,'challenge_lab':False,'enforcement':'May support teacher explanation, prevent misconceptions or over-teaching, and constrain student-facing wording, but must not become a required student memorization target, exact-name Review target, or Challenge Lab requirement.'})
write(U7/'scope-guards-f5.json',{'schema':'memory-palace-v2-unit7-f5-scope-guards-1.0','unit_id':'unit-7','guard_count':25,'guards':guards})

# Finalization accounting.
finalization={
 'schema':'memory-palace-v2-unit7-f5-finalization-1.0','unit_id':'unit-7','release_status':'STUDENT_READY_F5',
 'canonical_records':215,'runtime_memory_objects':174,'story_records':174,'challenge_lab_records':16,'scope_guard_records':25,'accounted_records':215,'unaccounted_records':0,
 'guided_journeys':6,'permanent_loci':55,'optional_first_exposure_recalls':18,
 'exact_name_review_targets':94,'non_exact_palace_records':80,'mandatory_spelling_targets':0,'mixed_discrimination_sets':33,'mixed_discrimination_questions':102,
 'review_policy':{'first_exposure':'Story-first. Quick Recall remains optional and sparse.','exact_name':'Only the 94 F2 records marked for exact-name retrieval enter the delayed exact-name manifest. The 80 meaning/mechanism-only palace records remain learnable in the stories without a required exact-name gate.','mixed_discrimination':'A confusable set becomes eligible only after every associated Unit 7 knowledge record has been encountered; first mixed practice is delayed by 48 hours.','visible_review_load':'At most five due review items are shown at a time.','spelling':'No mandatory Unit 7 spelling gate; spelling support remains adaptive.'},
 'destinations':{'story':sorted(story_ids),'challenge_lab':sorted(challenge_ids),'scope_guards':sorted(scope_ids)},
 'release_gate':{'science_lock':'PASS_F1','architecture_lock':'PASS_F2','scene_brief_lock':'PASS_F3','narratives':'PASS_F4A_F4F','runtime_memory_objects':'PASS_F5','challenge_lab':'PASS_F5','scope_guards':'PASS_F5','mixed_discrimination':'PASS_F5','exact_name_review':'PASS_F5','zero_loss_accounting':'PASS_F5'}
}
write(U7/'finalization-f5.json',finalization)

# Student-ready journey registry. Journey JSON narrative bytes remain untouched.
f4reg=read(U7/'journeys-f4f.json'); f5reg=dict(f4reg)
ready=[]
for j in f4reg['guided_journeys']:
    x=dict(j); x['student_release']='STUDENT_READY_F5'; x['preview_release']=False; ready.append(x)
f5reg.update({'schema':'memory-palace-v2-unit7-f5-registry-1.0','stage':'F5','narrative_standard':'V2-NARRATIVE-3.0-F5-STUDENT-READY','student_release':True,'preview_release':False,'release_status':'STUDENT_READY_F5','guided_journeys':ready})
write(U7/'journeys-f5.json',f5reg)

# Runtime integration.
content_path=ROOT/'backend/content.py'
content=content_path.read_text(encoding='utf-8')
anchor="@lru_cache(maxsize=1)\ndef unit7_source_lock(): return _read_json(UNIT7_DIR / \"source\" / \"canonical-unit7-f1.json\")\n"
extra="""@lru_cache(maxsize=1)\ndef unit7_source_lock(): return _read_json(UNIT7_DIR / \"source\" / \"canonical-unit7-f1.json\")\n@lru_cache(maxsize=1)\ndef unit7_architecture(): return _read_json(UNIT7_DIR / \"architecture\" / \"palace-architecture-f2.json\")\n@lru_cache(maxsize=1)\ndef unit7_scene_briefs(): return _read_json(UNIT7_DIR / \"briefs\" / \"scene-briefs-f3.json\")\n@lru_cache(maxsize=1)\ndef unit7_journey_briefs(): return _read_json(UNIT7_DIR / \"briefs\" / \"journey-briefs-f3.json\")\n@lru_cache(maxsize=1)\ndef unit7_memory_objects(): return _read_json(UNIT7_DIR / \"memory-objects-f5.json\")\n@lru_cache(maxsize=1)\ndef unit7_application_lab(): return _read_json(UNIT7_DIR / \"application-lab.json\")\n@lru_cache(maxsize=1)\ndef unit7_review_manifest(): return _read_json(UNIT7_DIR / \"review-manifest-f5.json\")\n@lru_cache(maxsize=1)\ndef unit7_mixed_discrimination(): return _read_json(UNIT7_DIR / \"mixed-discrimination-f5.json\")\n@lru_cache(maxsize=1)\ndef unit7_scope_guards(): return _read_json(UNIT7_DIR / \"scope-guards-f5.json\")\n@lru_cache(maxsize=1)\ndef unit7_finalization(): return _read_json(UNIT7_DIR / \"finalization-f5.json\")\n"""
if "def unit7_memory_objects()" not in content and anchor in content:
    content=content.replace(anchor,extra)

old='''    if unit_id == "unit-6":\n        path=UNIT6_DIR / "journeys-f5.json"\n        return _read_json(path)["guided_journeys"] if path.exists() and unit6_status().get("student_release") is True else []\n    return []\n'''
new='''    if unit_id == "unit-6":\n        path=UNIT6_DIR / "journeys-f5.json"\n        return _read_json(path)["guided_journeys"] if path.exists() and unit6_status().get("student_release") is True else []\n    if unit_id == "unit-7":\n        path=UNIT7_DIR / "journeys-f5.json"\n        return _read_json(path)["guided_journeys"] if path.exists() and unit7_status().get("student_release") is True else []\n    return []\n'''
if old in content: content=content.replace(old,new)

old='''    elif unit_id == "unit-6":\n        if unit6_status().get("student_release") is not True: return None\n        path=UNIT6_DIR / "journeys" / f"{palace_id}.json"\n    else: return None\n'''
new='''    elif unit_id == "unit-6":\n        if unit6_status().get("student_release") is not True: return None\n        path=UNIT6_DIR / "journeys" / f"{palace_id}.json"\n    elif unit_id == "unit-7":\n        if unit7_status().get("student_release") is not True: return None\n        path=UNIT7_DIR / "journeys" / f"{palace_id}.json"\n    else: return None\n'''
if old in content: content=content.replace(old,new)

old='''    if unit_id=="unit-7":\n        records=unit7_source_lock()["canonical_catalog"]\n        return {r["knowledge_id"]:{"memory_object_id":r["knowledge_id"],"canonical_term":r["canonical_label"],"canonical_definition":r["canonical_verified_statement"],"source_reference":r.get("source_reference",""),"canonical_lock":r.get("canonical_lock","")} for r in records}\n'''
new='''    if unit_id=="unit-7":\n        path=UNIT7_DIR / "memory-objects-f5.json"\n        if path.exists() and unit7_status().get("student_release") is True: return {o["memory_object_id"]:o for o in unit7_memory_objects()["memory_objects"]}\n        records=unit7_source_lock()["canonical_catalog"]\n        return {r["knowledge_id"]:{"memory_object_id":r["knowledge_id"],"canonical_term":r["canonical_label"],"canonical_definition":r["canonical_verified_statement"],"source_reference":r.get("source_reference",""),"canonical_lock":r.get("canonical_lock","")} for r in records}\n'''
if old in content: content=content.replace(old,new)
content_path.write_text(content,encoding='utf-8')

main_path=ROOT/'backend/main.py'
main=main_path.read_text(encoding='utf-8')
main=re.sub(r'app=FastAPI\(title="Memory Palace V2 · AP Biology",version="[^"]+"\)', 'app=FastAPI(title="Memory Palace V2 · AP Biology",version="0.27.0-u7-f5")', main)
main=re.sub(r"def health\(\): return \{'ok':True,'version':'[^']+'\}", "def health(): return {'ok':True,'version':'v2-apbio-0.27.0-u7-f5'}", main)
for marker,insert in [
("    if unit_id=='unit-6': return content.unit6_architecture()\n","    if unit_id=='unit-6': return content.unit6_architecture()\n    if unit_id=='unit-7': return content.unit7_architecture()\n"),
("    if unit_id=='unit-6': return content.unit6_scene_briefs()\n","    if unit_id=='unit-6': return content.unit6_scene_briefs()\n    if unit_id=='unit-7': return content.unit7_scene_briefs()\n"),
("    if unit_id=='unit-6': return content.unit6_journey_briefs()\n","    if unit_id=='unit-6': return content.unit6_journey_briefs()\n    if unit_id=='unit-7': return content.unit7_journey_briefs()\n"),
("    if unit_id=='unit-6': return content.unit6_application_lab()\n","    if unit_id=='unit-6': return content.unit6_application_lab()\n    if unit_id=='unit-7': return content.unit7_application_lab()\n"),
("    if unit_id=='unit-6': return content.unit6_review_manifest()\n","    if unit_id=='unit-6': return content.unit6_review_manifest()\n    if unit_id=='unit-7': return content.unit7_review_manifest()\n"),
("    if unit_id=='unit-6': return content.unit6_mixed_discrimination()\n","    if unit_id=='unit-6': return content.unit6_mixed_discrimination()\n    if unit_id=='unit-7': return content.unit7_mixed_discrimination()\n"),
("    if unit_id=='unit-6': return content.unit6_finalization()\n","    if unit_id=='unit-6': return content.unit6_finalization()\n    if unit_id=='unit-7': return content.unit7_finalization()\n"),
("    if unit_id=='unit-6': return content.unit6_scope_guards()\n","    if unit_id=='unit-6': return content.unit6_scope_guards()\n    if unit_id=='unit-7': return content.unit7_scope_guards()\n"),
]:
    if marker in main and insert not in main: main=main.replace(marker,insert)
main_path.write_text(main,encoding='utf-8')

# Status and course registry.
status=read(U7/'status-f4f.json')
status.update({'status':'STUDENT_READY','pipeline_status':'UNIT7_FINALIZED_F5','pipeline_stage':'UNIT7_FINALIZED_F5','student_release':True,'preview_release':False,'canonical_records_accounted':215,'unaccounted_canonical_records':0,'memory_objects':174,'runtime_memory_objects':174,'application_challenges':16,'practice_only_records':16,'scope_guard_records':25,'mixed_discrimination_sets':33,'mixed_discrimination_questions':102,'exact_name_review_targets':94,'non_exact_palace_records':80,'mandatory_spelling_targets':0,'polished_journeys':6,'polished_scenes':55,'next_required_output':'Classroom/browser validation of the released Unit 7 experience.','next_gate':'Unit 7 F6 browser/classroom validation.'})
write(U7/'status-f5.json',status); write(U7/'status.json',status)

course=read(COURSE)
for u in course['units']:
    if u['unit_id']=='unit-7':
        u.update({'status':'STUDENT_READY','journey_count':6,'scene_count':55,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5','polished_journeys':6,'polished_scenes':55,'student_release':True,'preview_release':False,'application_challenges':16,'scope_guard_records':25,'canonical_records_accounted':215,'runtime_memory_objects':174,'mixed_discrimination_sets':33,'mixed_discrimination_questions':102,'exact_name_review_targets':94,'non_exact_palace_records':80,'pipeline_stage':'UNIT7_FINALIZED_F5'})
write(COURSE,course)

# F5 locks and release manifest.
files=['memory-objects-f5.json','application-lab.json','review-manifest-f5.json','mixed-discrimination-f5.json','scope-guards-f5.json','finalization-f5.json','journeys-f5.json','status-f5.json']
runtime_files=['backend/main.py','backend/content.py','backend/settings.py','frontend/js/app.js','frontend/js/api.js','frontend/js/audio.js','frontend/js/state.js','frontend/js/views/home.js','frontend/js/views/learn.js','frontend/js/views/review.js','frontend/js/views/practice.js']
lock={'schema':'memory-palace-v2-unit7-f5-content-lock-1.0','unit_id':'unit-7','stage':'F5','student_release':True,
      'files':{f:sha(U7/f) for f in files},
      'protected_narratives':{f'journeys/U7-J{i}.json':sha(U7/'journeys'/f'U7-J{i}.json') for i in range(1,7)},
      'protected_upstream_locks':{f'content-lock-{s}.json':sha(U7/f'content-lock-{s}.json') for s in ['f1','f2','f3','f4a','f4b','f4c','f4d','f4e','f4f']},
      'runtime_file_sha256':{rel:sha(ROOT/rel) for rel in runtime_files}}
write(U7/'content-lock-f5.json',lock)
release={'schema':'memory-palace-v2-unit7-f5-release-manifest-1.0','unit_id':'unit-7','stage':'F5','student_release':True,'preview_release':False,'canonical_records':215,'canonical_records_accounted':215,'unaccounted_canonical_records':0,'runtime_memory_objects':174,'story_records':174,'practice_only_records':16,'scope_guard_records':25,'guided_journeys':6,'permanent_loci':55,'challenge_count':16,'optional_first_exposure_recalls':18,'exact_name_review_targets':94,'non_exact_palace_records':80,'mandatory_spelling_targets':0,'mixed_discrimination_sets':33,'mixed_discrimination_questions':102,'next_stage':'UNIT7_BROWSER_CLASSROOM_VALIDATION_F6'}
write(U7/'f5-release-manifest.json',release)

# Consolidated Units 1–7 mainline manifest.
u16=read(AP/'mainline-release-u1-u6.json')
mainline={'schema':'memory-palace-v2-mainline-u1-u7-f5-1.0','release_status':'STUDENT_READY_UNITS_1_7_UNIT7_F5','units':['unit-1','unit-2','unit-3','unit-4','unit-5','unit-6','unit-7'],'runtime_version':'v2-apbio-0.27.0-u7-f5','totals':{'canonical_records_units_1_7':u16['totals']['canonical_records_units_1_6']+215,'guided_journeys':u16['totals']['guided_journeys']+6,'permanent_scenes':u16['totals']['permanent_scenes']+55,'challenge_lab_items':u16['totals']['challenge_lab_items']+16},'unit7':release,'future_units':['unit-8']}
write(AP/'mainline-release-u1-u7.json',mainline)

print('Built Unit 7 F5')
print(json.dumps(release,indent=2))
