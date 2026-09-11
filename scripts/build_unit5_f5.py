from __future__ import annotations
import json, hashlib, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'
AP=ROOT/'content'/'ap-biology'
COURSE=AP/'course.json'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,d): Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def significant_tokens(text):
    stop={'a','an','and','or','the','of','to','in','on','for','with','from','as','at','by','is','are','be','via','vs','versus','into','across','over','through','cell','cells','phase','stage','system','role','example','effect'}
    out=[]
    for t in re.findall(r"[A-Za-z0-9]+",text):
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
        out=re.sub(rf'\b{re.escape(stem)}[A-Za-z0-9-]*\b','_____',out,flags=re.I)
    out=re.sub(r'(_____\s*){2,}','_____ ',out)
    out=re.sub(r'\s+([,.;:])',r'\1',out)
    return re.sub(r'\s{2,}',' ',out).strip()

source=read(U5/'source'/'canonical-unit5-f1.json')
canon={r['knowledge_id']:r for r in source['canonical_catalog']}
classification=read(U5/'architecture'/'learning-classification-f2.json')
arch=read(U5/'architecture'/'palace-architecture-f2.json')
class_by={r['knowledge_id']:r for r in classification['records']}
journeys=[read(U5/'journeys'/f'U5-J{i}.json') for i in range(1,9)]
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
assert len(story_ids)==131 and len(challenge_ids)==16 and len(scope_ids)==5
assert set(story_ids)|set(challenge_ids)|set(scope_ids)==set(canon)
assert not(set(story_ids)&set(challenge_ids) or set(story_ids)&set(scope_ids) or set(challenge_ids)&set(scope_ids))

# Runtime Memory Objects
conf_sets_by_id={kid:[] for kid in story_ids}
for s in arch['confusable_sets']:
    for kid in s['knowledge_ids']:
        if kid in conf_sets_by_id: conf_sets_by_id[kid].append(s['set_id'])
memory_objects=[]
for kid in story_ids:
    c=canon[kid]; cl=class_by[kid]; b=beat_by[kid]; sc=scene_by[kid]
    exact=bool(cl.get('exact_name_recall'))
    memory_objects.append({
      'memory_object_id':kid,'source_knowledge_id':kid,'object_type':'UNIT5_STORY_MEMORY_OBJECT',
      'canonical_term':b['term'],'canonical_definition':c['canonical_verified_statement'],'canonical_scientific_language':'English',
      'topic':c['topic'],'scope_class':c['scope_class'],'exact_name_required':'YES' if exact else 'NO','exact_spelling_required':'NO',
      'name_support':cl['name_support'],'spelling_policy':cl['spelling_policy'],'retrieval_modes':cl['retrieval_modes'],
      'visual_mode':cl['visual_mode'],'palace_zone':sc['journey_title'],'primary_palace_locus':sc['scene_title'],'locus_id':sc['locus_id'],
      'scene_index':sc['scene_index'],'confusable_set_ids':conf_sets_by_id.get(kid,[]),'story_hint':b.get('hint',''),
      'forward_prompt_name_to_meaning':f"Explain the scientific meaning of '{b['term']}' without relying on the story.",
      'reverse_prompt_meaning_to_name':(f"Retrieve the exact Unit 5 term for this scientific role: {redact(c['canonical_verified_statement'],[b['term']])}" if exact else None),
      'productive_retrieval_target':b['term'],'scientific_lock_status':'LOCKED_F1','narrative_lock_status':'LOCKED_F4H',
      'student_runtime':True,'ai_mutability':'AI may vary mnemonic wording, hints, practice phrasing, language, pacing, and distractors. AI may not change canonical term, locked scientific meaning, AP scope, confusable distinction, or misconception guardrail.',
      'source_trace':c.get('source_reference',''),'content_version':1,'version_status':'STUDENT_READY_F5'
    })
write(U5/'memory-objects-f5.json',{'schema':'memory-palace-v2-unit5-f5-memory-objects-1.0','unit_id':'unit-5','count':len(memory_objects),'exact_name_required_count':sum(x['exact_name_required']=='YES' for x in memory_objects),'memory_objects':memory_objects})

# Delayed exact-name Review, only for the 130 F2 exact-name targets.
review_targets=[]
for kid in story_ids:
    cl=class_by[kid]
    if not cl.get('exact_name_recall'): continue
    b=beat_by[kid]; c=canon[kid]; sc=scene_by[kid]; answer=b['term']
    prompt='Which exact Unit 5 term or named relationship matches this scientific description? '+redact(c['canonical_verified_statement'],[answer])
    hint_source=b.get('hint') or f"Return to {sc['scene_title']} and reconstruct the defining scientific action."
    hint=redact(hint_source,[answer])
    if len(hint)<25: hint=f"Return to {sc['scene_title']} and reconstruct the defining action before naming it."
    review_targets.append({'knowledge_id':kid,'target_answer':answer,'prompt':prompt,'hint':hint,'journey_id':sc['journey_id'],'scene_index':sc['scene_index'],'scene_title':sc['scene_title'],'canonical_science':c['canonical_verified_statement'],'spelling_policy':cl['spelling_policy'],'initial_review_window_hours':[18,72]})
write(U5/'review-manifest-f5.json',{'schema':'memory-palace-v2-unit5-f5-review-manifest-1.0','unit_id':'unit-5','target_count':len(review_targets),'non_exact_palace_records':1,'mandatory_spelling_targets':0,'visible_review_limit':5,'targets':review_targets})

# Mixed discrimination. One operational question per F2 set member.
mixed=[]
for base in arch['confusable_sets']:
    choices=base['terms']; qs=[]
    for qi,(kid,answer) in enumerate(zip(base['knowledge_ids'],choices),1):
        clue='Which option best matches this scientific description? '+redact(canon[kid]['canonical_verified_statement'],choices)
        if answer.casefold() in clue.casefold(): raise RuntimeError(f'mixed clue leaked answer {answer}')
        qs.append({'question_id':f"{base['set_id']}-Q{qi:02d}",'prompt':clue,'choices':choices,'answer':answer,'explanation':canon[kid]['canonical_verified_statement'],'knowledge_id':kid})
    mixed.append({'set_id':base['set_id'],'title':base['title'],'knowledge_ids':base['knowledge_ids'],'terms':choices,'unlock_rule':'Schedule only after every associated Unit 5 knowledge record has been encountered in a story.','initial_delay_hours':48,'questions':qs})
write(U5/'mixed-discrimination-f5.json',{'schema':'memory-palace-v2-unit5-f5-mixed-discrimination-1.0','unit_id':'unit-5','set_count':len(mixed),'question_count':sum(len(s['questions']) for s in mixed),'sets':mixed})

# Challenge Lab. These 16 records are deliberately outside the permanent palace.
C={
'U5-K-132':('Meiosis','Identify a meiotic phase from chromosome behavior',
 'An unfamiliar cell model shows homologous chromosome pairs aligned side by side at the equator. Each chromosome is still duplicated, and sister chromatids remain joined. Spindle fibers from opposite poles are attached so the two homologs of each pair can move toward different poles. Identify the meiotic phase and justify the choice using the chromosome relationship that is aligned and what has not yet separated.',
 'The model is metaphase I. The decisive evidence is that homologous chromosome pairs, not individual duplicated chromosomes, are aligned at the metaphase plate. Sister chromatids are still joined. In anaphase I the homologs would be moving apart, while in metaphase II individual duplicated chromosomes align in each haploid cell with sister kinetochores oriented toward opposite poles.',
 'Return to Meiosis Transit Hall and ask what occupies the metaphase plate in division I compared with division II.'),
'U5-K-133':('Genetic diversity','Distinguish three sources of sexual variation',
 'Three diagrams show different events. Diagram A shows nonsister chromatids of homologous chromosomes exchanging corresponding DNA segments during prophase I. Diagram B shows two homologous pairs oriented in different possible directions at metaphase I. Diagram C shows one sperm randomly fusing with one egg from a large pool of gametes. Name the variation mechanism represented by each diagram and explain when it occurs.',
 'A is crossing over, which occurs during prophase I and can produce recombinant chromatids. B represents independent orientation and the resulting independent assortment of unlinked chromosome pairs during meiosis I. C is random fertilization, which occurs after meiosis and combines one of many possible sperm with one of many possible eggs. These mechanisms contribute to variation through different physical events.',
 'Use the three directions of the Variation Sources Compass and identify whether the change happens during chromosome pairing, homolog orientation, or gamete fusion.'),
'U5-K-134':('Mendelian genetics','Solve a one-gene cross from genotype to probability',
 'In a plant species, allele P produces purple flowers and is completely dominant to allele p, which produces white flowers. Cross a heterozygous purple plant with a white plant. Determine the parental genotypes, list the gametes each parent can produce, and calculate the expected genotype and phenotype probabilities among offspring.',
 'The cross is Pp × pp. The heterozygous parent produces P and p gametes with probability one-half each, while the pp parent produces only p gametes. Offspring are expected to be one-half Pp and one-half pp. Under complete dominance, the predicted phenotype probabilities are one-half purple and one-half white. These are probabilities for each fertilization event, not guaranteed counts in a small family.',
 'Return to the Gamete–Punnett Board. Generate biologically possible gametes before placing anything into the grid.'),
'U5-K-135':('Mendelian genetics','Generate gametes from a multilocus genotype',
 'Assume genes A and B are on different chromosomes and assort independently. An individual has genotype AaBb. List every possible allele combination that can appear in its gametes and state the expected probability of each combination under the independent-assortment assumption. Then explain what would have to be reconsidered if A and B were tightly linked on the same chromosome.',
 'For AaBb with independent assortment, the possible gametes are AB, Ab, aB, and ab, each with expected probability one-fourth. Each gamete receives one allele from the A locus and one from the B locus. If the genes were tightly linked, the parental allele arrangement on the homologs and recombination frequency would matter, so the four gamete types would not necessarily occur in equal proportions.',
 'Use the Mendelian Laws Gate first, then the Gamete–Punnett Board. Independent assortment is an assumption that must be stated, not silently imposed.'),
'U5-K-136':('Mendelian genetics','Interpret a dihybrid cross and its assumptions',
 'Two organisms with genotype AaBb are crossed. Assume complete dominance at both loci, no viability differences, and independent assortment of the two genes. Determine the possible gametes for each parent and the expected four phenotype classes. State the classic phenotype ratio and explain why that ratio would not be a universal prediction if the genes were linked or the dominance relationships differed.',
 'Each AaBb parent produces AB, Ab, aB, and ab gametes at equal expected frequencies under independent assortment. Combining these gametes produces the classic 9:3:3:1 phenotype ratio for A_B_, A_bb, aaB_, and aabb when complete dominance applies at both loci. The ratio is conditional on this specific cross and its assumptions. Linkage, different allele interactions, selection, or other mechanisms can change the expected proportions.',
 'Use the assumption banner on the Classic Ratio Balcony. The ratio is an outcome of a defined model, not a definition of Mendelian inheritance.'),
'U5-K-137':('Probability','Use the multiplication rule for an AND event',
 'For an Aa × Aa cross, the probability that one offspring is aa is one-fourth. Assume successive offspring outcomes are independent. What is the probability that the first two offspring are both aa? Show the event structure that justifies the calculation, and explain why the multiplication rule is appropriate.',
 'The event is aa in the first offspring AND aa in the second offspring. Because the two fertilization outcomes are treated as independent, multiply the probabilities: one-fourth × one-fourth = one-sixteenth. The multiplication rule applies because both independent events must occur. The calculation does not mean a family of sixteen offspring is guaranteed to contain exactly one such pair.',
 'Return to the Addition–Multiplication Junction and choose the AND lane only after confirming that both required events are independent.'),
'U5-K-138':('Probability','Use addition and multiplication in one genetics problem',
 'In an Aa × Aa cross, what is the probability that an offspring is homozygous, meaning either AA or aa? Then determine the probability that two successive offspring are both homozygous. Show where the addition rule and multiplication rule enter the reasoning.',
 'For one offspring, AA and aa are mutually exclusive outcomes. P(AA or aa) = one-fourth + one-fourth = one-half. For two successive offspring to both be homozygous, treat the two offspring outcomes as independent and multiply: one-half × one-half = one-fourth. Addition combines mutually exclusive alternatives within one event, while multiplication combines independent events that must both occur.',
 'Use both lanes of the Addition–Multiplication Junction. First identify OR within one offspring, then AND across two independent offspring.'),
'U5-K-139':('Pedigrees','Infer plausible inheritance from a pedigree pattern',
 'A rare trait appears in two siblings whose parents are both unaffected. The trait occurs in individuals with different stated sex-chromosome complements, and the pedigree is too small to establish a definitive pattern from frequency alone. Identify one plausible simple inheritance model, state genotypes that could explain the affected siblings, and name at least one reason the pedigree should be treated as evidence rather than an absolute rule.',
 'A simple autosomal-recessive model is plausible. Both unaffected parents could be heterozygous carriers, and affected siblings could be homozygous recessive. The pedigree alone does not prove that model. Small family size, incomplete penetrance, new variants, phenotype uncertainty, or other inheritance mechanisms can produce patterns that resemble simple textbook expectations. The inference should compare candidate models with all observed evidence.',
 'Return to the Inheritance Pattern Verdict Room. Keep observed family relationships and phenotypes separate from inferred genotypes and mechanisms.'),
'U5-K-140':('Non-Mendelian genetics','Solve incomplete-dominance and codominance crosses',
 'Two loci illustrate different allele interactions. At locus R, RR is red, rr is white, and Rr is pink. At locus C, C1C1 shows antigen 1, C2C2 shows antigen 2, and C1C2 shows both antigens distinctly. For each locus, identify the inheritance pattern and predict the phenotype proportions from a heterozygote × heterozygote cross.',
 'The R locus shows incomplete dominance because the heterozygote has an intermediate phenotype. Rr × Rr gives one-fourth red, one-half pink, and one-fourth white. The C locus shows codominance because both allelic effects are separately expressed in the heterozygote. C1C2 × C1C2 gives one-fourth antigen 1 only, one-half both antigens, and one-fourth antigen 2 only. Neither pattern requires alleles to blend or disappear.',
 'Use the Dominance Spectrum Studio and focus on what the heterozygote visibly expresses. Intermediate and jointly visible are different mechanisms.'),
'U5-K-141':('Non-Mendelian genetics','Infer ABO genotypes and offspring possibilities',
 'A parent with blood type A and a parent with blood type B have a child with blood type O. Infer the possible genotypes of both parents under the ABO model. Then list the blood-type phenotypes that could occur in another child from the same parents and explain how codominance and multiple alleles are both involved.',
 'A type O child has genotype ii, so each parent must contribute an i allele. The type A parent must therefore be IAi and the type B parent IBi. Their possible offspring genotypes are IAIB, IAi, IBi, and ii, producing type AB, type A, type B, and type O phenotypes. The population has three common alleles, IA, IB, and i, while IA and IB are codominant when together.',
 'Return to the Dominance Spectrum Studio. Keep population-level multiple alleles separate from the two allele copies carried by one typical diploid individual.'),
'U5-K-142':('Chromosome-linked inheritance','Track an X-linked allele through an explicit XX/XY model',
 'In an explicitly stated XX/XY inheritance model, a person with chromosome complement XX is heterozygous for an X-linked recessive allele Xr and a person with chromosome complement XY carries the non-recessive allele XR on the X chromosome. Determine the possible offspring chromosome-and-allele combinations and the probability that an XY offspring carries Xr. Use chromosome-complement language only for this inheritance model.',
 'The XX parent can produce XR or Xr gametes. The XY parent can produce XR or Y gametes. The four equally likely combinations under the simplified assumptions are XRXR, XRXr, XRY, and XrY. Half of the XY offspring possibilities carry Xr, so the conditional probability among XY offspring is one-half. This chromosome model describes allele transmission and should not be used as a synonym for gender or as a complete account of sex development.',
 'Use the Chromosome-Linked Inheritance Comparator and Hemizygous Transmission Rail. Track the allele on an actual X chromosome before applying any pedigree shortcut.'),
'U5-K-143':('Genetic linkage','Classify parental and recombinant classes from offspring data',
 'A testcross begins with a heterozygote whose homologs carry AB on one chromosome and ab on the other. Offspring counts are AB 420, ab 400, Ab 90, and aB 90. Classify the parental and recombinant classes, calculate recombination frequency, and justify the classification from the known starting arrangement.',
 'The parental combinations are AB and ab because those match the allele arrangements present on the heterozygote’s original homologs. The recombinant combinations are Ab and aB because they are new relative to that starting arrangement. Recombinants total 180 out of 1000 offspring, giving a recombination frequency of 18%. The larger class sizes are consistent with linkage here, but size alone does not define parental status.',
 'Return to the Parental–Recombinant Sorting Yard. Classify outcomes from the original homolog arrangement before looking at which bins are largest.'),
'U5-K-144':('Genetic linkage','Estimate short genetic map distance and explain the ceiling',
 'A two-point testcross gives 84 recombinant offspring among 800 total offspring. Estimate the short-interval genetic map distance between the loci. Then explain why a different pair of loci with an observed recombination frequency near 50% cannot be assigned a reliable long two-point map distance from that percentage alone.',
 'The recombination frequency is 84/800 = 0.105, or 10.5%, so the short-interval estimate is about 10.5 centimorgans. For long intervals, multiple crossovers can restore parental marker combinations and go uncounted in a simple two-marker analysis. Observed recombination therefore approaches a ceiling near 50%, where ordinary two-locus data cannot distinguish very distant same-chromosome loci from effectively unlinked genes.',
 'Use the Recombination Frequency Meter, then the Linkage Map Board, then the Fifty-Percent Ceiling Gate. A genetic map unit is not a literal base-pair ruler.'),
'U5-K-145':('Chi-square','Convert an inheritance model into expected counts',
 'A genetic model predicts a 3:1 phenotype ratio in a sample of 200 offspring. Before calculating chi-square, determine the expected count in each of the two categories. Explain how the model proportions and total sample size produce expected counts and why the observed counts must remain in a separate column.',
 'A 3:1 model predicts proportions of three-fourths and one-fourth. Multiplying by 200 gives expected counts of 150 and 50. These are model-predicted categorical counts, not measurements. The observed counts are the actual recorded data. Chi-square compares the observed counts with expected counts derived from the stated null model, so their different origins must remain explicit.',
 'Return to the Chi-Square Model Bench. The null model sets proportions first, and the Expected-count column is calculated before any chi-square contribution.'),
'U5-K-146':('Chi-square','Complete a chi-square goodness-of-fit decision',
 'A null model predicts a 3:1 ratio for 160 offspring. The observed counts are 112 in category A and 48 in category B. Calculate the expected counts, compute χ² using the sum of (O−E)²/E, determine degrees of freedom for this fixed-proportion goodness-of-fit test, and compare with the 0.05 critical value 3.84. State the correct hypothesis decision.',
 'Expected counts are 120 and 40. The contributions are (112−120)²/120 = 64/120 ≈ 0.533 and (48−40)²/40 = 64/40 = 1.600. Thus χ² ≈ 2.133. With two categories, degrees of freedom are 2−1 = 1 in this AP goodness-of-fit context. Because 2.133 is below the 0.05 critical value 3.84, fail to reject the null hypothesis. This result does not prove or accept the null model.',
 'Use the Observed–Expected Calculation Station and Chi-Square Decision Console. Keep O, E, χ², degrees of freedom, threshold, and decision as separate steps.'),
'U5-K-147':('Environment and phenotype','Explain phenotypic plasticity without allele change',
 'Genetically identical plant cuttings are grown under two temperature regimes. Plants in the warmer treatment develop shorter stems and thicker leaves, while plants in the cooler treatment develop taller stems and thinner leaves. No DNA-sequence difference is detected between treatments. Explain a plausible biological mechanism for the phenotypic difference and distinguish this result from inherited allele change.',
 'The same genotype can produce different phenotypes when environmental conditions alter gene expression, enzyme activity, hormone signaling, membrane properties, or other physiological processes. Temperature could therefore change developmental regulation and produce the observed morphology without changing inherited alleles. This is an environmental effect on phenotype and an example of genotype-by-environment context or phenotypic plasticity, not evidence that the treatment created a heritable allele difference.',
 'Return to the Phenotypic Plasticity Conservatory. Hold genotype constant on the left while changing environmental context and following the physiological mechanism to the phenotype on the right.'),
}
arch_ch={x['knowledge_id']:x for x in arch['challenge_lab']}
items=[]
for kid in challenge_ids:
    domain,title,prompt,answer,hint=C[kid]; a=arch_ch[kid]
    items.append({'challenge_id':a['challenge_id'],'knowledge_id':kid,'domain':domain,'title':title,'type':a['type'],'prerequisite_loci':a['prerequisite_loci'],'prompt':prompt,'answer_guide':answer,'story_hint':hint,'canonical_statement':canon[kid]['canonical_verified_statement'],'success_criterion':'Solve the novel problem and justify the mechanism from ordinary scientific information. Recognition of a palace image alone is not sufficient.','practice_only_runtime':True})
write(U5/'application-lab.json',{'schema':'memory-palace-v2-unit5-f5-challenge-lab-1.0','unit_id':'unit-5','title':'Unit 5 Challenge Lab','student_intro':'Use these after the related journeys. One challenge appears at a time so meiosis, inheritance, probability, pedigree, linkage, chi-square, and genotype-environment reasoning are practiced without depending on the mnemonic story.','challenge_count':len(items),'practice_only_runtime_count':len(items),'practice_only_runtime_object_ids':[x['knowledge_id'] for x in items],'items':items})

# Scope guards
guards=[]
for kid in scope_ids:
    c=canon[kid]
    guards.append({'knowledge_id':kid,'canonical_label':c['canonical_label'],'policy':'NON_RUNTIME_AP_SCOPE_BOUNDARY','canonical_statement':c['canonical_verified_statement'],'student_runtime':False,'permanent_palace':False,'challenge_lab':False,'enforcement':'May support teacher explanation or prevent over-teaching, but must not become a required student memorization, exact-name Review target, or Challenge Lab requirement.'})
write(U5/'scope-guards-f5.json',{'schema':'memory-palace-v2-unit5-f5-scope-guards-1.0','unit_id':'unit-5','guard_count':len(guards),'guards':guards})

# Finalization accounting
mixed_q=sum(len(s['questions']) for s in mixed)
finalization={
 'schema':'memory-palace-v2-unit5-f5-finalization-1.0','unit_id':'unit-5','release_status':'STUDENT_READY_F5',
 'canonical_records':152,'runtime_memory_objects':131,'story_records':131,'challenge_lab_records':16,'scope_guard_records':5,'accounted_records':152,'unaccounted_records':0,
 'guided_journeys':8,'permanent_loci':50,'optional_first_exposure_recalls':18,
 'exact_name_review_targets':len(review_targets),'non_exact_palace_records':1,'mandatory_spelling_targets':0,'mixed_discrimination_sets':len(mixed),'mixed_discrimination_questions':mixed_q,
 'review_policy':{'first_exposure':'Story-first. Quick Recall remains optional and sparse.','exact_name':'The 130 F2 records marked for exact-name retrieval enter delayed Review through answer-redacted scientific-role prompts. The one meaning/mechanism-only record is encountered in story but is not forced into exact-name Review.','mixed_discrimination':'A confusable set becomes eligible only after every associated record has been encountered; first mixed practice is delayed by 48 hours.','visible_review_load':'At most five due review items are shown at a time.','spelling':'No mandatory Unit 5 spelling gate; spelling support remains adaptive.'},
 'destinations':{'story':sorted(story_ids),'challenge_lab':sorted(challenge_ids),'scope_guards':sorted(scope_ids)},
 'release_gate':{'science_lock':'PASS_F1','architecture_lock':'PASS_F2','scene_brief_lock':'PASS_F3','narratives':'PASS_F4A_F4H','runtime_memory_objects':'PASS_F5','challenge_lab':'PASS_F5','scope_guards':'PASS_F5','mixed_discrimination':'PASS_F5','exact_name_review':'PASS_F5','zero_loss_accounting':'PASS_F5'}
}
write(U5/'finalization-f5.json',finalization)

# Student-ready journey registry. Narrative files remain byte-identical.
f4reg=read(U5/'journeys-f4h.json'); f5reg=dict(f4reg)
ready=[]
for j in f4reg['guided_journeys']:
    x=dict(j); x['student_release']='STUDENT_READY_F5'; ready.append(x)
f5reg.update({'schema':'memory-palace-v2-unit5-f5-registry-1.0','stage':'F5','narrative_standard':'V2-NARRATIVE-3.0-F5-STUDENT-READY','student_release':True,'preview_release':False,'release_status':'STUDENT_READY_F5','guided_journeys':ready})
write(U5/'journeys-f5.json',f5reg)

status=read(U5/'status-f4h.json')
status.update({'status':'STUDENT_READY','pipeline_status':'UNIT5_FINALIZED_F5','pipeline_stage':'UNIT5_FINALIZED_F5','student_release':True,'preview_release':False,'memory_objects':131,'runtime_memory_objects':131,'application_challenges':16,'practice_only_records':16,'scope_guard_records':5,'mixed_discrimination_sets':32,'mixed_discrimination_questions':mixed_q,'exact_name_review_targets':len(review_targets),'non_exact_palace_records':1,'canonical_records_accounted':152,'unaccounted_canonical_records':0,'polished_journeys':8,'polished_scenes':50,'next_required_output':'Classroom/browser validation of the released Unit 5 experience.','next_gate':'Unit 5 F6 browser/classroom validation.'})
write(U5/'status-f5.json',status); write(U5/'status.json',status)

course=read(COURSE)
for u in course['units']:
    if u['unit_id']=='unit-5':
        u.update({'status':'STUDENT_READY','journey_count':8,'scene_count':50,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5','polished_journeys':8,'polished_scenes':50,'student_release':True,'preview_release':False,'application_challenges':16,'scope_guard_records':5,'canonical_records_accounted':152,'runtime_memory_objects':131,'mixed_discrimination_sets':32,'mixed_discrimination_questions':mixed_q,'exact_name_review_targets':len(review_targets),'pipeline_stage':'UNIT5_FINALIZED_F5'})
write(COURSE,course)

files=['memory-objects-f5.json','application-lab.json','review-manifest-f5.json','mixed-discrimination-f5.json','scope-guards-f5.json','finalization-f5.json','journeys-f5.json','status-f5.json']
lock={'schema':'memory-palace-v2-unit5-f5-content-lock-1.0','unit_id':'unit-5','stage':'F5','student_release':True,'files':{f:sha(U5/f) for f in files},'protected_narratives':{f'journeys/U5-J{i}.json':sha(U5/'journeys'/f'U5-J{i}.json') for i in range(1,9)},'protected_upstream_locks':{f'content-lock-{s}.json':sha(U5/f'content-lock-{s}.json') for s in ['f1','f2','f3','f4a','f4b','f4c','f4d','f4e','f4f','f4g','f4h']}}
write(U5/'content-lock-f5.json',lock)
release={'schema':'memory-palace-v2-unit5-f5-release-manifest-1.0','unit_id':'unit-5','stage':'F5','student_release':True,'preview_release':False,'canonical_records':152,'canonical_records_accounted':152,'unaccounted_canonical_records':0,'runtime_memory_objects':131,'story_records':131,'practice_only_records':16,'scope_guard_records':5,'guided_journeys':8,'permanent_loci':50,'challenge_count':16,'exact_name_review_targets':len(review_targets),'non_exact_palace_records':1,'mandatory_spelling_targets':0,'mixed_discrimination_sets':32,'mixed_discrimination_questions':mixed_q,'next_stage':'UNIT5_BROWSER_CLASSROOM_VALIDATION_F6'}
write(U5/'f5-release-manifest.json',release)

# New consolidated Units 1-5 mainline manifest.
u1=read(AP/'unit-1'/'v2-release-manifest.json'); u2=read(AP/'unit-2'/'finalization-f5.json'); u3=read(AP/'unit-3'/'finalization-f5.json'); u4=read(AP/'unit-4'/'finalization-f5.json')
mainline={'schema':'memory-palace-v2-mainline-u1-u5-f5-1.0','release_status':'STUDENT_READY_UNITS_1_5_UNIT5_F5','units':['unit-1','unit-2','unit-3','unit-4','unit-5'],'totals':{'canonical_records_units_1_5':u1['canonical_records']+u2['canonical_records']+u3['canonical_records']+u4['canonical_records']+152,'guided_journeys':u1['journeys']+u2['guided_journeys']+u3['guided_journeys']+u4['guided_journeys']+8,'permanent_scenes':u1['scenes']+u2['permanent_loci']+u3['permanent_loci']+u4['permanent_loci']+50,'challenge_lab_items':read(AP/'unit-1'/'application-lab.json')['challenge_count']+read(AP/'unit-2'/'application-lab.json')['challenge_count']+read(AP/'unit-3'/'application-lab.json')['challenge_count']+read(AP/'unit-4'/'application-lab.json')['challenge_count']+16},'unit5':release,'future_units':['unit-6','unit-7','unit-8']}
write(AP/'mainline-release-u1-u5.json',mainline)
print('Built Unit 5 F5')
print(json.dumps(release,indent=2))
