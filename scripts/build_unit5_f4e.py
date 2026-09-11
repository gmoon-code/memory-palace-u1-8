from __future__ import annotations
import json, hashlib, re, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'
subprocess.run([sys.executable,str(ROOT/'scripts'/'build_unit5_f4d.py')],check=True,stdout=subprocess.DEVNULL)
F3=json.loads((U5/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS=json.loads((U5/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J5=next(j for j in JBRIEFS if j['journey_id']=='U5-J5')
B={b['locus_id']:b for b in F3 if b['journey_id']=='U5-J5'}
CANON={r['knowledge_id']:r for r in json.loads((U5/'source'/'canonical-unit5-f1.json').read_text(encoding='utf-8'))['canonical_catalog']}
J1=json.loads((U5/'journeys'/'U5-J1.json').read_text(encoding='utf-8'))
J2=json.loads((U5/'journeys'/'U5-J2.json').read_text(encoding='utf-8'))
J3=json.loads((U5/'journeys'/'U5-J3.json').read_text(encoding='utf-8'))
J4=json.loads((U5/'journeys'/'U5-J4.json').read_text(encoding='utf-8'))

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

GUIDE={
 'name':'Dr. Imani Reyes','role':'inheritance-systems geneticist',
 'visual':'deep-green field coat, clear gloves, compact chromosome tablet preserving the blue and amber parental-origin chromosome identities, and the narrow gold generation ledger',
 'story_job':'Imani keeps calculation, observed evidence, and inferred inheritance models in separate places. She makes every probability rule follow the event structure and every pedigree verdict follow the evidence before a model is named.'
}
DOCKET={
 'name':'Two-sided evidence docket','kind':'continuity record',
 'visual':'a dark-blue court folder with two hinged pages. The left page is ruled for event structure and numerical probability, while the right page is ruled for pedigree observations, candidate models, and model-comparison notes',
 'job':'keeps probability logic separate from family evidence while preserving one continuous inheritance case from the first probability hall to the final verdict room.'
}
EVENT_CARDS={
 'name':'Event-probability cards','kind':'continuity scientific object',
 'visual':'small cream cards labeled with biological events such as a gamete carrying a particular allele or a defined offspring outcome. Each card has a probability window that can be combined only after its event relationship is identified',
 'job':'makes the event itself visible before addition or multiplication is selected, preventing arithmetic from being chosen from the appearance of fractions alone.'
}
MODEL_CARDS={
 'name':'Candidate inheritance-model cards','kind':'continuity scientific object',
 'visual':'sealed gray cards labeled with candidate inheritance models. They remain closed during the probability rooms and open only after pedigree evidence has been organized',
 'job':'preserves the distinction between observed data and an inferred inheritance mechanism, then allows several models to be compared against the same evidence.'
}

route=[
 {'scene_index':0,'locus':'Inheritance Probability Hall','short':'Probability','floor':'West probability hall','symbol':'P'},
 {'scene_index':1,'locus':'Addition–Multiplication Junction','short':'OR / AND','floor':'Central probability junction','symbol':'OR / AND'},
 {'scene_index':2,'locus':'Pedigree Reading Gallery','short':'Pedigree','floor':'East family gallery','symbol':'I II III'},
 {'scene_index':3,'locus':'Inheritance Pattern Verdict Room','short':'Verdict','floor':'North evidence chamber','symbol':'evidence → model'}
]

BEAT_IMAGES={
 'U5-K-016':'the probability hall where repeated random gamete formation and fertilization feed numerical event cards into offspring-outcome bins without promising one exact small-family result',
 'U5-K-021':'the left OR lane where mutually exclusive outcome cards are combined by addition only after the event language has been identified',
 'U5-K-022':'the right AND lane where independent event cards are combined by multiplication only after both events are required for the joint outcome',
 'U5-K-086':'the multigeneration family diagram in the gallery that organizes relationships and phenotype observations across generations',
 'U5-K-087':'the left symbol key showing generation labels, individual symbols, horizontal parent lines, and vertical descent lines before any inheritance mechanism is inferred',
 'U5-K-088':'the right clue panel where an affected parent across generations can support a simple fully penetrant autosomal-dominant model while caveat cards prevent the clue from becoming an absolute rule',
 'U5-K-020':'the final verdict table where observed family or offspring patterns are compared with predictions from several candidate inheritance models before any model is supported or weakened'
}

ZONE_COPY={
'U5-L27':[
 ('left','Gamete-event probability rack','gamete P','Transparent drawers hold event cards for alternative gametes from a modeled parent. Each drawer shows the biological event first and its probability second.'),
 ('center','Inheritance probability chamber','repeated trials','A clear central chamber repeatedly models random gamete production and fertilization. It links defined event probabilities to possible offspring outcomes without claiming that a short run must match the expected proportions exactly.'),
 ('right','Offspring-outcome probability wall','offspring P','Outcome bins collect the modeled possibilities and display their expected probabilities across repeated events while actual short samples remain free to vary.')],
'U5-L28':[
 ('left','Addition-rule OR lane','OR +','Two mutually exclusive event cards enter separate left channels and merge into one OR total only after the court verifies that the alternatives cannot occur in the same trial.'),
 ('center','Event-language turntable','OR or AND','A rotating decision table forces each problem to state whether it asks for either of mutually exclusive alternatives or for independent events that must occur together before arithmetic begins.'),
 ('right','Multiplication-rule AND lane','AND ×','Independent event cards pass through two sequential gates. The joint outcome receives a probability only after the court verifies that both events are required and the independence condition is appropriate.')],
'U5-L29':[
 ('left','Pedigree symbol key','key','A fixed legend defines the generation labels, individual symbols, horizontal parent lines, vertical descent lines, and phenotype markings used by the family diagram before any inheritance conclusion is attempted.'),
 ('center','Multigeneration pedigree wall','I II III','A large family diagram spans several generations. Relationships and affected or unaffected phenotype observations can be read directly from the diagram while genotype remains unknown unless evidence supports an inference.'),
 ('right','Autosomal-dominant clue panel','clue ≠ proof','A comparison panel highlights the common affected-parent pattern of a simple fully penetrant autosomal-dominant model, then displays caveat cards for new variants, penetrance, family size, and uncertain phenotype classification.')],
'U5-L30':[
 ('left','Observed-pattern evidence board','observed','The cleaned pedigree and any offspring data are pinned here exactly as observed, with no inferred genotype or inheritance label written into the evidence itself.'),
 ('center','Model-comparison verdict table','compare','Candidate inheritance-model cards open across a large table. Each model generates expected patterns that are compared with the same observed evidence.'),
 ('right','Supported and weakened model shelves','support','Cards move to supported, still-plausible, or weakened shelves according to how well their predictions fit the evidence. A final docket note records uncertainty and the assumptions needed for later probability modeling.')]
}

NARR={
'U5-L27':{
 'title':'The Hall Where an Expected Fraction Had Been Stamped as a Promise',
 'kicker':'Inheritance probability describes the distribution of repeated random outcomes, so an expected value can guide prediction without dictating the exact composition of one small family.',
 'paragraphs':[
  "The bronze doors of the **Inheritance Probability Hall** swing inward and reveal a courtroom wing arranged around a long white marble floor. On your **left**, transparent drawers hold gamete-event cards beside small probability windows. Directly **ahead**, a clear cylindrical chamber contains two parent stations and a central fertilization tray. On your **right**, a wall of offspring-outcome bins waits beneath an enormous red stamp that reads GUARANTEED. Dr. Imani Reyes stops before the stamp can fall. She places a dark-blue **two-sided evidence docket** on the center rail. Its left page is ruled for event structure and probability. Its right page is still blank because no family evidence has been examined yet. A bundle of **event-probability cards** rests beside it, while several sealed gray **candidate inheritance-model cards** remain untouched at the back of the folder.",
  "Imani opens the tracked Mendelian case from the previous estate and chooses one heterozygous parent for a single modeled gene. The chromosome tablet shows the two alleles at the homologous locus, and the gamete drawers on the left receive the alternative gamete events produced by segregation. Each drawer is labeled with the biological event first. One card represents a gamete carrying one allele and another card represents a gamete carrying the alternative allele. Numerical probabilities are written only after the event has been defined. Imani records them on the probability page of the docket and then slides copies of the event cards toward the central chamber. The hall is making the connection from meiosis to probability visible. Random gamete formation produces events whose long-run frequencies can be represented numerically.",
  "The central chamber begins running repeated modeled fertilizations. A gamete is sampled from one parent station, another is sampled from the other station, and the pair moves into the fertilization tray. The resulting offspring combination is sent to one of the bins on the right. The chamber repeats the process again and again. Some short runs look uneven. A small cluster can contain several identical outcomes in a row even when the underlying event probabilities have not changed. As more trials accumulate, the distribution can approach the probabilities predicted by the model, though any particular finite sample can still differ. Imani points to the movement from left to center to right and names the relationship **Probability in inheritance**. Rules of probability can be applied to analyze transmission of single-gene traits from parents to offspring.",
  "The red GUARANTEED stamp begins to descend over the right wall. Imani blocks it with the docket. A predicted probability describes how likely an outcome is under the stated model. It does not force a specific number of children, seeds, or experimental offspring to appear in a small sample. The wall demonstrates this directly. The expected probability remains fixed above each bin while the counts from one short run fluctuate below it. She starts a second run with the same parental model, and the counts differ again even though the event probabilities have not changed. The court therefore records expected probability and observed count in different boxes. One is a property of the model. The other is the result of a particular sample.",
  "Imani then traces the causal route backward. The offspring probability on the right did not arise from a decorative fraction. It depends on which gametes the parental genotypes can produce, how often those gamete events occur under the model, and how gametes combine at fertilization. The biological mechanism remains meiosis and fertilization. Probability summarizes the uncertainty in which allowed event occurs on any one trial. That distinction keeps the court from giving the mathematics credit for creating the inheritance outcome. It also keeps the chromosome mechanism visible beneath every number the court later calculates.",
  "When the hall has been repaired, Imani tears the GUARANTEED stamp from its hinge and clips a smaller label to the docket. It reads expected under the model. The left probability page now has clearly defined event cards, the center chamber shows repeated random combinations, and the right wall shows outcome probabilities beside variable sample counts. A pair of floor lights then appears at the far end of the hall. The left light is marked OR and the right light AND. The court understands a single event now, yet it still has no rule for combining events. Imani carries the same docket and event cards into the **Addition–Multiplication Junction**."
 ],
 'close':'Probability now summarizes random inheritance events without promising an exact small-sample outcome. The unresolved question is how different events combine, so the docket moves to the OR and AND junction.'
},
'U5-L28':{
 'title':'The Junction Where Every Pair of Fractions Had Been Treated the Same',
 'kicker':'The arithmetic follows the event relationship. Mutually exclusive alternatives use addition, while independent events required together use multiplication.',
 'paragraphs':[
  "The marble floor narrows into the **Addition–Multiplication Junction**. On your **left**, a blue lane marked OR ends at a wide plus-shaped gate. Directly **ahead**, a circular event-language turntable holds two empty slots labeled either and together. On your **right**, a gold lane marked AND passes through two sequential gates before reaching a multiplication panel. The same two-sided evidence docket rests at the edge of the turntable, and the event-probability cards from the first hall remain clipped to its left page. An old clerk has been routing every pair of fractions to whichever arithmetic sign is closer. Imani locks both lanes until the event language is stated first.",
  "She begins on the left with a single-trial question involving two outcomes that cannot both occur in the same defined trial. One event card is placed in the first OR slot and a different mutually exclusive outcome goes into the second. Imani verifies the relationship before touching the plus gate. The question asks for event A **or** event B. Since the alternatives are mutually exclusive in this modeled trial, their probabilities can be combined by the **Addition rule of probability**. For mutually exclusive events A and B, P(A or B) equals P(A) plus P(B). The cards physically merge only after the court confirms that the two alternatives cannot both occupy the same outcome slot on that trial.",
  "The turntable rotates toward the right lane. This time the desired outcome requires one defined event from one source and another independent event from a second source. The first card passes the first gate, and the second card must pass the next gate for the joint result to be completed. Imani asks the court to say the relationship aloud before the multiplication panel activates. The question requires event A **and** event B. When the events are independent under the model, the joint probability follows the **Multiplication rule of probability**. For independent events A and B, P(A and B) equals P(A) multiplied by P(B). The two gates make the logic visible because both required events must occur for the combined outcome to reach the end of the lane.",
  "Imani deliberately swaps the cards between lanes without changing their fractions. The arithmetic does not follow the numbers. A pair of one-half probabilities can belong to an OR question in one context and an AND question in another. The court must identify whether the problem describes mutually exclusive alternatives or independent events required together. She also adds an independence latch to the AND lane. Multiplication is justified by the modeled relationship between the events. A genetics problem cannot assume independence merely because two probabilities appear side by side. The biology and the stated model determine whether that condition is appropriate.",
  "The docket receives a simple language check before any calculation. OR points left toward addition when the alternatives are mutually exclusive. AND points right toward multiplication when the required events are independent. Imani leaves those words larger than the arithmetic signs because they carry the decision. The court will later send actual calculations to Challenge Lab practice, where students must identify event structure in unfamiliar crosses. This permanent scene keeps only the reusable logic. It teaches which relationship calls for which rule and why.",
  "The turntable finally unlocks both lanes. The quick-recall light above it flashes once. Imani covers the answer panels and asks which probability rule is used for mutually exclusive A OR B and which is used for independent A AND B. After the attempt, she restores the labels and closes the probability page of the docket. A tall glass door beyond the junction now reveals rows of family symbols extending across three generations. Probability rules can combine events, yet the court cannot infer an inheritance mechanism from fractions alone. The docket flips to its still-empty right page as you enter the **Pedigree Reading Gallery**."
 ],
 'close':'The event relationship now selects the probability rule. The court next has to read family evidence accurately before any inheritance model can be considered.'
},
'U5-L29':{
 'title':'The Gallery Where One Family Clue Had Been Turned Into a Verdict',
 'kicker':'A pedigree organizes relationships and phenotypes across generations, while inheritance clues remain evidence whose strength depends on the model and the available family data.',
 'paragraphs':[
  "The **Pedigree Reading Gallery** opens as a long east wing with family records mounted from floor to ceiling. On your **left**, a fixed symbol key explains the notation used by the gallery. Directly **ahead**, a multigeneration family diagram spans an illuminated wall marked I, II, and III. On your **right**, a clue panel already carries a bright autosomal-dominant stamp even though several family branches are still covered. Dr. Imani Reyes places the two-sided evidence docket on a waist-high reading rail. The probability page stays closed. The right page now opens for observed evidence. The sealed candidate inheritance-model cards remain in their envelope because the family relationships must be read before a model is proposed.",
  "Imani starts at the left key. Generation labels organize rows of the family. Individual symbols identify people or individuals according to the notation defined for this pedigree. Horizontal parent or mating lines connect parents, and vertical descent lines lead to offspring and later generations. Filled or otherwise marked symbols identify the phenotype being traced, while unmarked symbols identify the comparison state used by the diagram. She names this organized family diagram a **Pedigree**. A pedigree is a family diagram used to trace phenotypes and infer possible genotypes or inheritance patterns across generations. The key and relationship lines together form **Pedigree notation**, the standardized visual system that makes the family structure readable.",
  "Only after the notation is clear does she move to the center wall. You follow one descent line from generation I to generation II, then another to generation III. The diagram tells you which individuals are related and which display the phenotype of interest. It does not directly reveal every genotype. Imani writes observed affected or unaffected phenotype beside each relevant individual on the docket and leaves genotype cells blank. That empty space is deliberate. A pedigree contains observed family relationships and phenotype data. Genotypes and mechanisms are inferences that require an inheritance model and evidence.",
  "The right clue panel focuses on a familiar pattern. In a simple fully penetrant autosomal-dominant model, affected individuals often have an affected parent. Imani labels this an **Autosomal-dominant pedigree clue**. The phrase clue stays printed in large letters. It can support a candidate model when the broader family pattern fits, yet one visual feature cannot settle the case by itself. She uncovers the hidden branches and shows why. A new variant can produce an affected individual without an affected parent. Incomplete penetrance can leave a person carrying a relevant genotype without the expected phenotype. A small family can fail to display an outcome that is possible under the model. Phenotype classification can also be uncertain.",
  "Another old note claims that an inheritance pattern must be X-linked whenever more affected males appear. Imani removes it from the wall. Male-biased occurrence is especially associated with particular X-linked recessive models under their assumptions, and it is not a universal diagnostic feature of every X-linked trait. The gallery therefore records each pattern as evidence whose meaning depends on the candidate model, penetrance assumptions, family size, and the actual observed relationships. The physical separation between the center pedigree and the right clue panel keeps observed family data from turning automatically into a mechanism label.",
  "By the time the gallery is repaired, the right page of the docket contains three clean columns. One lists family relationships from the notation. One lists the observed phenotype pattern. The last column is still titled candidate interpretations and remains blank. Imani finally unseals the gray model cards, but she does not place any card on the pedigree itself. A heavy door at the north end opens into a chamber with an evidence board on the left, a comparison table in the center, and three verdict shelves on the right. The court is finally ready to move from observation to **Inheritance Pattern Verdict Room** without confusing a clue with proof."
 ],
 'close':'The pedigree now provides organized family evidence and cautious clues. Candidate models can finally be tested against that evidence in the verdict room.'
},
'U5-L30':{
 'title':'The Verdict Room Where the Model Had to Earn Its Label',
 'kicker':'Inheritance-pattern inference compares predictions from candidate models with observed data, so the conclusion can be supported, weakened, or left uncertain without pretending that a pedigree directly reveals genotype.',
 'paragraphs':[
  "The north door closes behind you in the **Inheritance Pattern Verdict Room**. On your **left**, the cleaned multigeneration pedigree and any accompanying offspring counts are pinned to an observed-pattern evidence board. Directly **ahead**, a broad model-comparison table has empty spaces for several candidate inheritance models. On your **right**, three shelves are labeled supported, still plausible, and weakened. The two-sided evidence docket lies open between the board and the table. Its left probability page contains the event rules from the first two rooms. Its right page contains the pedigree relationships and phenotype observations from the gallery. For the first time, Dr. Imani Reyes opens the sealed candidate inheritance-model cards.",
  "She places several candidates across the center table. The set can include autosomal inheritance models, chromosome-linked inheritance models, genetically linked loci when the data involve multiple genes, and different dominance relationships. Imani does not ask which label looks most familiar. Each card must generate predictions under its own assumptions. A model may predict which kinds of parent-offspring patterns are likely, whether a phenotype can appear after unaffected parents under the modeled conditions, whether the pattern differs among chromosome categories, or how genotype and phenotype probabilities should behave in a defined cross. Those predicted patterns are written beneath the candidate card before the observed evidence is compared with them.",
  "The evidence board on the left remains unchanged while the model cards are tested one by one. When a candidate prediction conflicts with a clear observed pattern under the stated assumptions, that model moves toward the weakened shelf. When a candidate remains compatible with the available evidence, it stays on the supported or still-plausible side depending on how strongly the data distinguish it from alternatives. Imani refuses to convert compatibility into certainty. Two different models can sometimes fit the same small pedigree. Missing relatives, uncertain phenotype classification, penetrance, new variants, and limited family size can reduce how strongly the data discriminate among candidates.",
  "Imani names this evidence process **Inheritance-pattern inference**. Autosomal, genetically linked, and sex-linked inheritance patterns and dominance relationships can often be inferred from data such as pedigrees. The word inference is crucial because the mechanism is concluded from patterns in evidence. The observed pedigree itself contains family relationships and phenotypes. It does not directly display every genotype or molecular cause. The court therefore keeps the observed-pattern board on the left and model interpretations on the right, with the comparison table physically between them.",
  "Once a candidate model has enough support to be used for a defined cross, Imani reopens the probability page. Punnett squares and probability rules can now generate genotype and phenotype probabilities under that specified model. The order matters. The model assumptions are stated first, possible gametes are determined from the parental genotypes and biology, and the probability tools summarize expected outcomes. If new pedigree or offspring evidence conflicts with those expectations, the model can be reconsidered. The tools help test and extend an inheritance explanation. They do not transform one visual clue into a guaranteed genotype.",
  "The final quick-recall light appears above the verdict shelves. Imani covers the model labels and asks what pedigree evidence should be used to infer. The intended reconstruction is a supported inheritance model or a set of plausible models, with uncertainty preserved when the evidence cannot distinguish them. When the answer panel is restored, the court seal changes from CERTAIN to SUPPORTED BY CURRENT EVIDENCE. The two-sided docket now tells the complete journey. Its left page separates single-event probability, OR logic, and independent AND logic. Its right page separates pedigree notation, observed family patterns, cautious clues, candidate models, and the final evidence-based inference.",
  "Imani closes the docket and places it beside the chromosome tablet. Probability and pedigree evidence now occupy different pages because they answer different questions. Probability tells how likely defined inheritance events are under a model. A pedigree organizes family observations across generations. Model comparison asks which inheritance mechanisms remain compatible with those observations. The verdict room doors unlock toward the next wing of the heredity complex, where traits that depart from simple complete-dominance patterns will be compared directly. Journey 5 ends with one rule that the court can no longer ignore. Evidence comes first, the model earns its support, and probability operates inside clearly stated assumptions."
 ],
 'close':'The court now distinguishes probability structure, pedigree observation, and inheritance-model inference. A verdict is supported by explicit evidence and assumptions, leaving later journeys free to compare more complex inheritance mechanisms.'
}
}

def zones_for(b):
    out=[]
    for pos,(position,label,symbol,desc) in zip(('left','center','right'),ZONE_COPY[b['locus_id']]):
        assert pos==position
        out.append({'position':position,'label':label,'symbol':symbol,'description':desc})
    return out

def make_cast(b):
    cast=[GUIDE,DOCKET,EVENT_CARDS,MODEL_CARDS]
    for z in zones_for(b):
        cast.append({'name':z['label'],'kind':'scientific structure or reference zone','visual':z['description'],'job':next(x['job_in_scene'] for x in b['stable_cast'] if x['position']==z['position'])})
    return cast

def make_beats(b):
    return [{'object_id':t['knowledge_id'],'term':t['canonical_term'],'story':BEAT_IMAGES[t['knowledge_id']],'science':t['canonical_science'],'exact_name':bool(t['exact_name_recall']),'hint':BEAT_IMAGES[t['knowledge_id']],'name_support':t['name_support']} for t in b['term_introductions']]

def make_snapshot(b):
    return [{'term':t['canonical_term'],'meaning':t['canonical_science'],'image':BEAT_IMAGES[t['knowledge_id']]} for t in b['term_introductions']]

briefs=[B[f'U5-L{i:02d}'] for i in range(27,31)]
scenes=[]
for idx,b in enumerate(briefs):
    n=NARR[b['locus_id']]; q=b['quick_recall']; checkpoint=bool(q['enabled'])
    cp={'U5-L28':'U5-K-021','U5-L30':'U5-K-020'}.get(b['locus_id']) if checkpoint else None
    scenes.append({
      'scene_index':idx,'locus_id':b['locus_id'],'locus':b['scene_title'],'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['micro_anchor'],'scene_layout':{'orientation':b['orientation_sentence'],'zones':zones_for(b)},
      'cast':make_cast(b),'continuity_object':J5['continuity_object'],
      'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':make_beats(b),'memory_snapshot':make_snapshot(b),
      'misconception_guards':b['misconception_guards'],'exit_memory':b['exit_memory'],
      'checkpoint':checkpoint,'checkpoint_object_id':cp,'checkpoint_prompt':q.get('candidate_prompt','') if checkpoint else '',
      'checkpoint_answer':q.get('answer','') if checkpoint else '',
      'checkpoint_hint':('Return to the fixed OR and AND lanes or the observed-evidence board and reconstruct what relationship the court evaluated before naming the rule or model.' if checkpoint else ''),
      'next_locus':briefs[idx+1]['scene_title'] if idx+1<len(briefs) else None,'causal_transition':b['causal_transition']['transition_logic'],
    })

journey={
 'palace_id':'U5-J5','unit_id':'unit-5','palace_name':'Probability and Pedigree Court','story_title':'The Court That Mistook a Clue for a Verdict',
 'tagline':'Repair one inheritance court so probabilities follow event logic, pedigrees remain organized evidence, and inheritance models earn support through explicit comparison.',
 'guide':GUIDE,
 'premise':'The Probability and Pedigree Court has begun issuing confident inheritance decisions from isolated clues. Expected probabilities are stamped as guarantees, addition and multiplication are chosen from the appearance of fractions, pedigree symbols are read without a key, and one family pattern receives an inheritance label before competing models are tested. The court can be repaired only by carrying one two-sided evidence docket from event probability through family observation to model comparison.',
 'mission':'Follow Dr. Imani Reyes through four connected locations. Separate expected probability from observed counts, choose addition or multiplication from the event relationship, read pedigree notation before interpreting the pattern, and compare candidate inheritance models with observed evidence before issuing a supported verdict.',
 'finale':'The court now keeps probability structure and family evidence on different pages of the same case. Defined inheritance events receive probabilities, OR and independent AND relationships select the correct probability rule, pedigrees organize observations across generations, and candidate models are compared with those observations before an inheritance pattern is inferred. A clue can support a model without becoming proof by itself.',
 'estimated_minutes':15,'scene_count':4,'checkpoint_count':2,'student_release':'DEVELOPER_PREVIEW_F4E',
 'learner_rule':'Follow the same two-sided evidence docket through the court. Define the biological event before using probability, read the family diagram before inferring a mechanism, and keep observed evidence separate from the model that explains it. Optional Quick Recall appears only twice.',
 'route_orientation':'This is one continuous west-to-north court route. Begin in the west Inheritance Probability Hall, pass through the central OR and AND junction, enter the east Pedigree Reading Gallery, and finish in the north Inheritance Pattern Verdict Room. The same docket, event cards, and sealed model cards remain visible throughout.',
 'route':route,'scenes':scenes,'narrative_design':'U5-F4E-NARRATIVE-1.0'
}
(U5/'journeys').mkdir(exist_ok=True)
(U5/'journeys'/'U5-J5.json').write_text(json.dumps(journey,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
registry={
 'schema':'memory-palace-v2-unit5-f4e-journeys-1.0','unit_id':'unit-5','stage':'F4E','student_release':False,'preview_release':True,
 'journey_count':5,'scene_count':30,'checkpoint_count':11,
 'guided_journeys':[{k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']} for j in [J1,J2,J3,J4,journey]]
}
(U5/'journeys-f4e.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
status={
 'unit_id':'unit-5','unit_number':5,'title':'Heredity','status':'F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','pipeline_status':'POLISHED_NARRATIVE_J1_J2_J3_J4_J5_F4E',
 'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','student_release':False,'preview_release':True,
 'canonical_records':152,'review_flags_resolved':37,'teacher_ppt_slides':112,'ced_topics':5,'ced_atoms':34,'architecture_journeys':8,'architecture_loci':50,
 'scene_briefs':50,'preview_journeys':5,'preview_scenes':30,'preview_checkpoints':11,'journey_1_records':20,'journey_2_records':18,'journey_3_records':8,'journey_4_records':25,'journey_5_records':7,
 'next_gate':'F4F_JOURNEY6_ONLY_AFTER_F4E_PROSE_QA'
}
(U5/'status-f4e.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(U5/'status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
words=sum(len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs']))) for s in scenes)
manifest={'schema':'memory-palace-v2-unit5-f4e-release-manifest-1.0','unit_id':'unit-5','stage':'F4E','student_release':False,'preview_release':True,'journey_count':5,'scene_count':30,'checkpoint_count':11,'journey_5_records':7,'journey_5_narrative_words':words,'f1_canonical_records':152,'f2_permanent_loci':50,'f3_scene_briefs':50,'next_gate':'F4F'}
(U5/'f4e-release-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

course_path=ROOT/'content'/'ap-biology'/'course.json'; course=json.loads(course_path.read_text(encoding='utf-8'))
cu5=next(u for u in course['units'] if u['unit_id']=='unit-5')
cu5.update({'status':'F4E_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW','journey_count':5,'scene_count':30,'canonical_lock':'LOCKED_F1','source_status':'AUDITED_SCIENCE_LOCKED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVE_J1_F4A_J2_F4B_J3_F4C_J4_F4D_J5_F4E','canonical_records':152,'review_flags_resolved':37,'ced_atoms':34,'teacher_ppt_slides':112,'student_release':False,'preview_release':True,'pipeline_stage':'UNIT5_JOURNEYS1_5_POLISHED_DEVELOPER_PREVIEW_F4E'})
course_path.write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lock_files=['journeys/U5-J5.json','journeys-f4e.json','status-f4e.json','f4e-release-manifest.json']
lock={'schema':'memory-palace-v2-unit5-content-lock-f4e-1.0','unit_id':'unit-5','stage':'F4E','lock_status':'LOCKED_F4E_J5','student_release':False,'preview_release':True,'files':{}}
for rel in lock_files:
    p=U5/rel; lock['files'][rel]={'bytes':p.stat().st_size,'sha256':sha(p)}
(U5/'content-lock-f4e.json').write_text(json.dumps(lock,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines=['# Unit 5 F4E · Journey 5 Narrative','',f'## {journey["story_title"]}','',journey['tagline'],'','**Palace**  Probability and Pedigree Court  ','**Guide**  Dr. Imani Reyes  ','**Route**  '+' → '.join(x['locus'] for x in route),'']
for s in scenes:
    lines += [f"## {s['scene_index']+1}. {s['locus']} — {s['title']}",'',f"*{s['scene_kicker']}*",'']+s['story_paragraphs']+['']
(ROOT/'docs'/'UNIT5_F4E_JOURNEY5_STORY.md').write_text('\n'.join(lines),encoding='utf-8')
release=['# Unit 5 F4E Release','', 'Unit 5 F4E authors and locks Journey 5 only while preserving Journeys 1–4 byte-for-byte against their earlier narrative locks. Unit 5 remains a developer preview and is not student released.','', '## Accounting','', '- Journeys 1–4 preserved: **26 scenes / 71 records / 9 optional recalls**', '- Journey 5 authored: **4 scenes / 7 records / 2 optional recalls**', f'- Journey 5 narrative words: **{words}**', '- Total Unit 5 preview: **5 journeys / 30 scenes / 11 optional recalls**','', '## Scientific continuity','', '- Probability remains a model of repeated random inheritance events and never guarantees the exact composition of one small family.', '- The addition rule is restricted to mutually exclusive OR events.', '- The multiplication rule is restricted to independent AND events under the stated model.', '- Pedigree notation is read before inheritance-mechanism inference.', '- Pedigree observations remain separate from inferred genotype and inheritance mechanism.', '- Autosomal-dominant family patterns remain clues with explicit caveats for new variants, penetrance, family size, and phenotype classification.', '- Candidate inheritance models generate predictions and are compared with the same observed evidence before receiving support.', '- Punnett and probability tools are used only after a candidate model and its assumptions are specified.','', '## Release boundary','', 'No Unit 5 Memory Objects, Review runtime, Challenge Lab runtime, or student-facing Unit 5 release is created in F4E. Journeys 6–8 remain at the F3 scene-brief stage.','']
(ROOT/'docs'/'UNIT5_F4E_RELEASE.md').write_text('\n'.join(release),encoding='utf-8')
print(json.dumps({'journey':'U5-J5','scenes':4,'records':7,'checkpoints':2,'narrative_words':words,'student_release':False,'preview_release':True},indent=2))
