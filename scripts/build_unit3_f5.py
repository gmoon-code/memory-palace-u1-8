from __future__ import annotations
import json,hashlib,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content'/'ap-biology'/'unit-3'
COURSE=ROOT/'content'/'ap-biology'/'course.json'

def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path,data): Path(path).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

source=read(U3/'source'/'canonical-unit3-f1.json')
canon={r['knowledge_id']:r for r in source['canonical_catalog']}
classification=read(U3/'architecture'/'learning-classification-f2.json')
arch=read(U3/'architecture'/'palace-architecture-f2.json')
class_by_id={r['knowledge_id']:r for r in classification['records']}
journeys=[read(U3/'journeys'/f'U3-J{i}.json') for i in range(1,8)]
beat_by_id={}; scene_by_id={}
for j in journeys:
    for s in j['scenes']:
        for b in s['story_beats']:
            beat_by_id[b['object_id']]=b
            scene_by_id[b['object_id']]={'journey_id':j['palace_id'],'journey_title':j['story_title'],'scene_index':s['scene_index'],'scene_title':s['locus']}

# ---------- Unit 3 Challenge Lab: the 11 deliberately non-palace practice records ----------
CHALLENGES=[
 {'challenge_id':'U3-APP-01','knowledge_id':'U3-K-176','domain':'Enzyme temperature response','title':'Fever and enzyme-function reasoning',
  'prompt':'A human enzyme works efficiently near normal body temperature. During a prolonged high fever, its reaction rate first changes and then falls sharply. Explain why moderate warming can initially increase reaction rate and why sufficiently high temperature can eventually reduce enzyme function.',
  'answer_guide':'Moderate warming increases molecular kinetic energy and can increase the frequency of productive enzyme-substrate encounters. At sufficiently high temperature, interactions that stabilize the enzyme’s three-dimensional structure can be disrupted. Altered active-site structure can then reduce substrate binding and catalysis, so reaction rate falls even though molecules are moving rapidly.',
  'story_hint':'Return to the enzyme stress-test room: collision frequency can rise before structural disruption dominates and the active site loses a functional shape.'},
 {'challenge_id':'U3-APP-02','knowledge_id':'U3-K-177','domain':'Enzyme helpers','title':'Vitamin-derived cofactor deficiency',
  'prompt':'A metabolic enzyme requires an organic helper derived from a dietary vitamin. A patient becomes severely deficient in that vitamin even though the enzyme protein is still produced normally. Predict how the enzyme-dependent pathway could be affected and explain the mechanism.',
  'answer_guide':'The pathway can slow because some enzymes require a nonprotein helper for catalytic activity. An organic cofactor is a coenzyme, and many coenzymes are vitamin-derived. Normal production of the enzyme protein does not guarantee a functional holoenzyme if its required helper is unavailable.',
  'story_hint':'Picture the helper dock where an enzyme becomes fully operational only after its required cofactor is associated; an organic vitamin-derived helper is a coenzyme.'},
 {'challenge_id':'U3-APP-03','knowledge_id':'U3-K-178','domain':'Enzyme data interpretation','title':'Peroxidase pH data',
  'prompt':'Peroxidase activity is measured at pH 3, 5, 7, 9, and 11. Relative activities are 12, 58, 100, 46, and 8 units. Identify the apparent optimum among the tested conditions, describe the pattern, and explain why activity can decline on either side of the optimum.',
  'answer_guide':'The apparent optimum among the tested treatments is pH 7 because it has the highest measured activity. Activity decreases as conditions become more acidic or more basic relative to that treatment. Changes in pH can alter ionization and interactions that help maintain enzyme structure and active-site chemistry, reducing catalytic efficiency. The experiment supports an optimum among the tested values; it does not prove that exactly pH 7 is the universal optimum under every condition.',
  'story_hint':'Picture the pH stress lane bending the enzyme away from its most functional conformation as conditions move away from the tested activity peak.'},
 {'challenge_id':'U3-APP-04','knowledge_id':'U3-K-179','domain':'Enzyme inhibition','title':'Penicillin and transpeptidase',
  'prompt':'A penicillin molecule reacts covalently with the active site of a bacterial transpeptidase required for peptidoglycan cross-linking. Predict the consequence for cell-wall construction and classify the inhibition mechanism relative to ordinary reversible competitive inhibition.',
  'answer_guide':'Peptidoglycan cross-linking should decrease because persistently inactivated transpeptidase cannot catalyze its normal reaction. Covalent active-site modification is an irreversible-inhibition mechanism. Although the inhibitor occupies or modifies the active-site region, this should not be described as the standard reversible competitive model in which inhibitor and substrate simply compete through reversible binding.',
  'story_hint':'Return to the inhibitor control room: reversible active-site competition can clear, while a covalent irreversible inhibitor leaves the enzyme persistently inactivated.'},
 {'challenge_id':'U3-APP-05','knowledge_id':'U3-K-180','domain':'Enzyme kinetics','title':'Recognize enzyme saturation',
  'prompt':'An enzyme is tested at increasing substrate concentrations. Reaction rate rises steeply at first, then approaches a plateau even though more substrate is added. Explain the plateau using enzyme occupancy.',
  'answer_guide':'At low substrate concentration, adding substrate increases the frequency of enzyme-substrate complex formation and raises reaction rate. At sufficiently high substrate concentration, most available active sites are occupied much of the time. Enzyme availability becomes limiting, so adding more substrate produces little additional increase in rate. This is enzyme saturation.',
  'story_hint':'Picture every active-site docking station occupied while extra substrate waits outside; the number of working enzyme sites has become the limiting factor.'},
 {'challenge_id':'U3-APP-06','knowledge_id':'U3-K-181','domain':'Photosynthetic pigments and evidence','title':'Light wavelength and plant growth',
  'prompt':'Identical seedlings are grown under equal photon exposure at blue, green, or red wavelengths. After two weeks, the blue- and red-light groups show greater biomass gain than the green-light group. Explain one photosynthetic mechanism consistent with the pattern and state one reason the data do not prove that pigment absorption is the only factor controlling plant growth.',
  'answer_guide':'Chlorophyll pigments absorb blue and red wavelengths strongly and reflect/transmit more green light, so blue and red treatments can support greater light capture for photosynthesis under otherwise comparable conditions. Plant growth also depends on many other factors such as nutrient availability, water, temperature, respiration, developmental state, and the exact light environment, so biomass is not a direct measurement of pigment absorption alone.',
  'story_hint':'Return to the pigment spectrum bench: absorption spectrum affects usable light, while the whole plant still has other physiological limits beyond pigment absorption.'},
 {'challenge_id':'U3-APP-07','knowledge_id':'U3-K-182','domain':'Photorespiration and evidence','title':'Evaluate a photorespiration claim',
  'prompt':'A student claims, “Photorespiration exists only because rubisco evolved when atmospheric O₂ was lower, so the pathway has no useful effect in modern plants.” Evaluate the claim using rubisco chemistry and the evidence boundaries established in Unit 3.',
  'answer_guide':'An evolutionary-legacy explanation is plausible as one hypothesis because rubisco can catalyze reactions with CO₂ or O₂ and atmospheric conditions have changed through evolutionary time. The conclusion that photorespiration has no useful modern effect is too strong. Photorespiratory metabolism lowers net carbon fixation when rubisco reacts with O₂, yet evidence also supports context-dependent protective roles when Calvin-cycle carbon processing is limited. The evolutionary interpretation should therefore remain qualified rather than treated as a complete proof of present function.',
  'story_hint':'Picture the photorespiration detour beside rubisco: O₂ competition lowers net carbon gain, while the historical explanation and possible protective roles remain separate claims.'},
 {'challenge_id':'U3-APP-08','knowledge_id':'U3-K-183','domain':'Photosynthetic electron transport','title':'Bentazon blocks photosystem II output',
  'prompt':'A herbicide prevents effective electron transfer from photosystem II into the downstream thylakoid electron-transport chain. Predict effects on the thylakoid proton gradient, ATP production, NADPH production, carbon fixation, and risk of excitation-related damage.',
  'answer_guide':'Blocking electron transfer after photosystem II reduces downstream electron flow. Less electron transport means less proton-gradient formation by the light-reaction system, which lowers photophosphorylation and ATP production. Electron supply to photosystem I and NADP+ reduction also falls, lowering NADPH production. With less ATP and NADPH, Calvin-cycle carbon fixation is constrained. Excitation energy can also accumulate in the photosynthetic apparatus, increasing risk of damaging reactive processes unless protective dissipation mechanisms compensate.',
  'story_hint':'Follow the Light Capture Conservatory sequence: PSII electron transfer → ETC/proton gradient → ATP synthase, while PSI supports NADPH; blocking the early transfer backs up the whole route.'},
 {'challenge_id':'U3-APP-09','knowledge_id':'U3-K-184','domain':'Fermentation data analysis','title':'Yeast sugar-fermentation comparison',
  'prompt':'Yeast are given equal concentrations of glucose, sucrose, or a no-sugar control. After 20 minutes, accumulated CO₂ volumes are 24 mL, 15 mL, and 1 mL respectively. Identify the independent and dependent variables, compare the fermentation responses, and evaluate the claim that glucose supports faster fermentation under these conditions.',
  'answer_guide':'The independent variable is sugar treatment and the dependent variable is CO₂ production over the measured interval. Glucose produced the most CO₂, sucrose produced less, and the no-sugar control produced very little. The data support the claim that glucose supported a higher fermentation-associated CO₂ production rate under these experimental conditions. The conclusion should stay limited to the tested yeast, concentrations, time interval, and conditions.',
  'story_hint':'Picture the alcohol-fermentation vat where CO₂ leaves during pyruvate decarboxylation; more accumulated CO₂ can serve as an experimental indicator of that pathway under controlled conditions.'},
 {'challenge_id':'U3-APP-10','knowledge_id':'U3-K-185','domain':'Oxygen limitation and ATP','title':'Fish under severe oxygen deprivation',
  'prompt':'A fish tissue experiences severe oxygen limitation. Explain why oxidative phosphorylation falls, how glycolysis can temporarily continue, and why fermentation helps even though it does not provide a large extra ATP yield.',
  'answer_guide':'Oxygen is the terminal electron acceptor in aerobic respiration. Severe oxygen limitation restricts respiratory electron flow and oxidative phosphorylation, so ATP production from chemiosmosis falls. Glycolysis can continue producing a small amount of ATP by substrate-level phosphorylation if NAD+ is available. Fermentation oxidizes NADH back to NAD+, allowing glycolytic oxidation to continue temporarily; its key role is carrier regeneration, not a large additional ATP-producing stage.',
  'story_hint':'Use the end of Respiration Power Plant and the NAD⁺ Recycling Gate together: loss of the O₂ terminal basin stops the respiratory route, while fermentation returns NAD⁺ to glycolysis.'},
 {'challenge_id':'U3-APP-11','knowledge_id':'U3-K-186','domain':'Chemiosmosis and experimental design','title':'Mitochondrial pH-gradient model',
  'prompt':'Isolated mitochondria are first equilibrated at pH 7, then rapidly transferred to pH 4 buffer containing ADP and Pi. Assume the inner mitochondrial membrane remains relatively impermeable to H⁺ except through ATP synthase. Predict the immediate direction of H⁺ movement through ATP synthase and explain how this can drive ATP formation even without first running the respiratory ETC in the new buffer.',
  'answer_guide':'The external/intermembrane-space side becomes much more acidic, so H⁺ concentration is higher outside the matrix than inside. If the inner membrane preserves that gradient, H⁺ moves down its electrochemical gradient through ATP synthase toward the matrix. That chemiosmotic flow can drive ATP synthase to form ATP from ADP and Pi. The experiment demonstrates that a proton-motive force can directly drive ATP synthesis; normally the respiratory ETC establishes the gradient in living mitochondria.',
  'story_hint':'Picture the mitochondrial architecture bay and turbine: the ETC normally builds the intermembrane-space H⁺ reservoir, but an experimentally imposed pH difference can provide the gradient directly.'}
]
for item in CHALLENGES:
    item['canonical_statement']=canon[item['knowledge_id']]['canonical_verified_statement']
    item['success_criterion']='Solve the novel problem and justify the mechanism from ordinary scientific information. Recognition of a palace image alone is not sufficient.'
    item['practice_only_runtime']=True
application_lab={'schema':'memory-palace-v2-unit3-f5-challenge-lab-1.0','unit_id':'unit-3','title':'Unit 3 Challenge Lab','student_intro':'Use these after the related journeys. One challenge appears at a time so data interpretation, experimental reasoning, and transfer practice stay manageable.','challenge_count':11,'practice_only_runtime_count':11,'practice_only_runtime_object_ids':[x['knowledge_id'] for x in CHALLENGES],'items':CHALLENGES}
write(U3/'application-lab.json',application_lab)

# ---------- Exact-name delayed review ----------
STOP={'and','the','with','from','into','that','this','than','versus','for','of','to','in','as','a','an','or','is','are'}
def redact_target(text:str,answer:str)->str:
    out=text
    out=re.sub(re.escape(answer),'_____',out,flags=re.I)
    words=[w.lower() for w in re.findall(r"[A-Za-z]+",answer) if w.lower() not in STOP]
    for w in sorted(set(words),key=len,reverse=True):
        if len(w)<=2: continue
        stem=w[:6] if len(w)>=7 else w[:max(3,len(w)-1)]
        out=re.sub(rf'\b{re.escape(stem)}[A-Za-z]*\b','_____',out,flags=re.I)
    return re.sub(r'\s+',' ',out).strip()
review_targets=[]
for r in classification['records']:
    if not r['exact_name_recall']: continue
    kid=r['knowledge_id']
    if kid not in beat_by_id: raise RuntimeError(f'Exact-name target missing from story beats: {kid}')
    beat=beat_by_id[kid]; loc=scene_by_id[kid]; answer=beat['term']
    cue=redact_target(beat['science'],answer); hint=redact_target(beat.get('hint',''),answer)
    if len(hint)<25: hint='Picture the defining structure, location, or action from the journey and retrieve the exact scientific name before revealing it.'
    review_targets.append({'knowledge_id':kid,'target_answer':answer,'prompt':f'Which exact Unit 3 name matches this scientific description? {cue}','hint':hint,'journey_id':loc['journey_id'],'scene_index':loc['scene_index'],'scene_title':loc['scene_title'],'canonical_science':beat['science'],'spelling_policy':r['spelling_policy'],'initial_review_window_hours':[18,72]})
review_manifest={'schema':'memory-palace-v2-unit3-f5-review-manifest-1.0','unit_id':'unit-3','target_count':len(review_targets),'mandatory_spelling_targets':0,'visible_review_limit':5,'targets':review_targets}
write(U3/'review-manifest-f5.json',review_manifest)

# ---------- Delayed mixed discrimination: all 28 architecture-defined sets ----------
CLUES={
'U3-K-083':'This is the initial energy barrier reactants must overcome to reach the transition state.','U3-K-002':'This protein functions as a biological catalyst in cells.','U3-K-084':'This is the reactant molecule on which a catalyst acts.','U3-K-085':'This is the region of a catalyst where a compatible reactant binds and catalysis occurs.','U3-K-005':'This temporary bound state exists after the reactant has docked at the catalyst before products are released.',
'U3-K-004':'This describes the requirement that reactant shape and charge fit the catalytic binding region.','U3-K-086':'This is the conformational change triggered by binding that improves catalytic interactions.',
'U3-K-007':'This is loss of functional protein structure caused by disruptive temperature, pH, or chemical conditions.','U3-K-009':'This describes structural disruption from which catalytic activity can return when conditions are restored.','U3-K-096':'This occurs when an inhibitor forms a persistent, often covalent interaction that inactivates the catalyst.',
'U3-K-012':'This inhibition occurs when a reversible inhibitor occupies the catalytic binding region and reduces reactant access.','U3-K-013':'This inhibition occurs when binding at a regulatory site away from the catalytic site decreases activity.','U3-K-093':'This is a nonprotein helper required by some catalysts and can include an inorganic metal ion.','U3-K-094':'This is an organic helper, often derived from a vitamin.','U3-K-095':'This is the catalytically active enzyme complex with its required helper or helpers associated.',
'U3-K-098':'This is a regulatory binding location distinct from the catalytic binding region.','U3-K-100':'This regulatory molecule binds away from the catalytic site and stabilizes a more active conformation.','U3-K-101':'This regulatory molecule binds away from the catalytic site and stabilizes a less active conformation.',
'U3-K-102':'This occurs when binding at one site of a multisubunit enzyme increases activity at additional sites.','U3-K-103':'This occurs when a downstream product inhibits an earlier enzyme in the same pathway.','U3-K-099':'This general control mechanism changes enzyme activity through noncovalent regulatory binding away from the active site.',
'U3-K-057':'This pathway breaks complex molecules into simpler products and typically releases usable energy.','U3-K-058':'This pathway builds complex molecules from simpler components and requires energy input.',
'U3-K-060':'This is energy associated with directed or observable motion.','U3-K-061':'This is kinetic energy associated with random molecular motion.','U3-K-062':'This is stored energy associated with position or structure.','U3-K-063':'This is stored molecular energy that can be transformed during reactions.',
'U3-K-065':'This law states that energy is transferred or transformed but is not created or destroyed.','U3-K-066':'This law states that energy transformations increase total entropy and disperse some energy as less-useful heat.',
'U3-K-070':'This reaction has a negative free-energy change and is thermodynamically spontaneous even if it may proceed slowly.','U3-K-071':'This reaction has a positive free-energy change and must be coupled to an energy-releasing process in cells.',
'U3-K-073':'This category includes muscle contraction, ciliary movement, and chromosome movement.','U3-K-074':'This category moves substances across membranes against thermodynamically favored directions.','U3-K-075':'This category drives endergonic synthesis such as building polymers from monomers.',
'U3-K-078':'This reaction converts ATP and water to ADP and inorganic phosphate with a negative free-energy change under cellular conditions.','U3-K-081':'This is transfer or addition of a phosphate group to a molecule, often changing its reactivity or conformation.','U3-K-082':'This continuously reforms ATP from ADP and inorganic phosphate using energy from exergonic processes.',
'U3-K-105':'This organismal strategy builds organic molecules from inorganic carbon using light or chemical energy.','U3-K-106':'This carbon-acquisition strategy uses light energy to build organic molecules from inorganic carbon.','U3-K-107':'This strategy obtains organic carbon from preexisting organic molecules made by other organisms.',
'U3-K-028':'This chloroplast fluid compartment lies outside the thylakoids and contains Calvin-cycle reactions.','U3-K-029':'This chloroplast membrane contains photosystems, pigments, electron-transfer components, and ATP synthase.','U3-K-030':'This is a stack of thylakoids.',
'U3-K-120':'This is the primary reaction-center pigment in oxygenic photosynthesis.','U3-K-121':'This accessory pigment broadens the wavelengths usable for photosynthesis in plants and green algae.','U3-K-122':'These accessory pigments broaden absorption and help dissipate excess excitation energy.',
'U3-K-123':'This thylakoid complex contains both a reaction center and surrounding light-harvesting pigments/proteins.','U3-K-125':'This pigment-protein assembly transfers excitation energy toward a reaction center.','U3-K-124':'This part contains a special chlorophyll pair and primary electron acceptor where excitation becomes electron transfer.',
'U3-K-126':'This light-driven complex receives replacement electrons from water oxidation after transferring an excited electron.','U3-K-127':'This light-driven complex re-excites arriving electrons and supports reduction of NADP+.',
'U3-K-031':'This light-reaction product supplies chemical energy for Calvin-cycle work.','U3-K-033':'This reduced electron carrier supplies reducing power for Calvin-cycle carbon reduction.',
'U3-K-116':'This photosynthetic phase captures light energy and produces ATP and reducing power on thylakoid membranes.','U3-K-133':'This cyclic stromal pathway uses ATP and reducing power to incorporate CO2 into carbohydrate.',
'U3-K-135':'This enzyme catalyzes initial CO2 fixation and can also react with O2.','U3-K-136':'This five-carbon CO2 acceptor is regenerated so the carbon-fixation cycle can continue.','U3-K-137':'This three-carbon sugar product can leave the cycle and contribute to glucose and other organic molecules.',
'U3-K-140':'This process begins when the carbon-fixing enzyme reacts with O2, lowering net carbon fixation.','U3-K-142':'This adaptation reduces photorespiration by initially fixing carbon in mesophyll cells and delivering CO2 to bundle-sheath cells.','U3-K-143':'This adaptation reduces water loss by taking in CO2 mainly at night and releasing stored CO2 during the day.',
'U3-K-148':'This oxidized/reduced carrier pair accepts electrons during fuel oxidation and delivers them to the respiratory ETC.','U3-K-149':'This carrier pair is reduced during the citric acid cycle and feeds electrons into the respiratory ETC at a different entry point.',
'U3-K-153':'This ATP-forming mechanism directly transfers a phosphate from an organic substrate to ADP.','U3-K-047':'This respiratory ATP-forming mechanism couples electron transport, a proton gradient, chemiosmosis, and ATP synthase.','U3-K-038':'This photosynthetic ATP-forming mechanism uses a light-generated proton gradient and ATP synthase.',
'U3-K-151':'This cytosolic stage splits one six-carbon glucose into two three-carbon pyruvate molecules.','U3-K-154':'This stage converts mitochondrial pyruvate to an acetyl group carried by coenzyme A while producing CO2 and NADH.','U3-K-156':'This cyclic matrix pathway oxidizes acetyl groups, releases CO2, and reduces NAD+ and FAD.','U3-K-158':'This stage combines respiratory electron transport that builds a proton gradient with chemiosmosis through ATP synthase.',
'U3-K-144':'This mitochondrial compartment lies inside the inner membrane and contains pyruvate-oxidation and citric-cycle machinery.','U3-K-044':'This mitochondrial compartment accumulates a higher proton concentration than the matrix during respiratory electron transport.',
'U3-K-042':'This energy-harvesting route uses an ETC and oxygen as terminal electron acceptor in its standard oxygen-dependent form.','U3-K-167':'This energy-harvesting route still uses an ETC but ends with a terminal electron acceptor other than oxygen.','U3-K-169':'This route regenerates NAD+ without an ETC so glycolysis can continue when oxidative reoxidation is limited.',
'U3-K-171':'This pathway converts pyruvate to acetaldehyde, releases CO2, then produces ethanol while regenerating NAD+.','U3-K-173':'This pathway reduces pyruvate directly to lactate while regenerating NAD+ and releasing no CO2 in the conversion.'
}
arch_sets=arch['confusable_sets']; mixed=[]
for base in arch_sets:
    choices=base['terms']; questions=[]
    for qi,(kid,answer) in enumerate(zip(base['knowledge_ids'],choices),1):
        clue=CLUES[kid]
        # A mixed question must not simply state the target term in the prompt.
        if answer.casefold() in clue.casefold(): raise RuntimeError(f'Mixed clue leaks target {answer}: {clue}')
        questions.append({'question_id':f"{base['set_id']}-Q{qi:02d}",'prompt':clue,'choices':choices,'answer':answer,'explanation':canon[kid]['canonical_verified_statement'],'knowledge_id':kid})
    mixed.append({'set_id':base['set_id'],'title':base['title'],'knowledge_ids':base['knowledge_ids'],'terms':choices,'unlock_rule':'Schedule only after every associated knowledge record has been encountered in a completed or in-progress Unit 3 story.','initial_delay_hours':48,'questions':questions})
mixed_manifest={'schema':'memory-palace-v2-unit3-f5-mixed-discrimination-1.0','unit_id':'unit-3','set_count':len(mixed),'question_count':sum(len(x['questions']) for x in mixed),'sets':mixed}
write(U3/'mixed-discrimination-f5.json',mixed_manifest)

# ---------- Explicit scope guards ----------
scope_ids=[r['knowledge_id'] for r in classification['records'] if r['scope_class']=='SCOPE_GUARD']
scope_guards=[]
for kid in scope_ids:
    r=canon[kid]
    scope_guards.append({'knowledge_id':kid,'canonical_label':r['canonical_label'],'policy':'NON_RUNTIME_AP_SCOPE_BOUNDARY','canonical_statement':r['canonical_verified_statement'],'student_runtime':False,'permanent_palace':False,'challenge_lab':False,'enforcement':'May support teacher explanation/context, but must not become a required memorization or retrieval target in the student runtime.'})
write(U3/'scope-guards-f5.json',{'schema':'memory-palace-v2-unit3-f5-scope-guards-1.0','unit_id':'unit-3','guard_count':len(scope_guards),'guards':scope_guards})

# ---------- Zero-loss canonical accounting ----------
story_ids=[oid for j in journeys for s in j['scenes'] for oid in s['object_ids']]
challenge_ids=[x['knowledge_id'] for x in CHALLENGES]
all_ids=set(canon); scope_set=set(scope_ids)
assert len(story_ids)==171 and len(set(story_ids))==171
assert len(challenge_ids)==11 and len(set(challenge_ids))==11
assert len(scope_set)==4
assert set(story_ids).isdisjoint(challenge_ids) and set(story_ids).isdisjoint(scope_set) and set(challenge_ids).isdisjoint(scope_set)
assert set(story_ids)|set(challenge_ids)|scope_set==all_ids

finalization={
 'schema':'memory-palace-v2-unit3-f5-finalization-1.0','unit_id':'unit-3','release_status':'STUDENT_READY_F5',
 'canonical_records':186,'story_records':171,'challenge_lab_records':11,'scope_guard_records':4,'accounted_records':186,'unaccounted_records':0,
 'guided_journeys':7,'permanent_loci':54,'optional_first_exposure_recalls':18,
 'exact_name_review_targets':len(review_targets),'mandatory_spelling_targets':0,
 'mixed_discrimination_sets':len(mixed),'mixed_discrimination_questions':sum(len(x['questions']) for x in mixed),
 'review_policy':{
  'first_exposure':'Story-first. Quick Recall remains optional and sparse.',
  'exact_name':'Every encountered exact-name target enters delayed Review through an answer-redacted scientific-role prompt.',
  'mixed_discrimination':'A confusable set becomes eligible only after every associated record has been encountered; first mixed practice is delayed by 48 hours.',
  'visible_review_load':'At most five due review items are shown at a time.',
  'spelling':'No mandatory Unit 3 spelling gate; spelling support remains adaptive.'},
 'destinations':{'story':sorted(story_ids),'challenge_lab':sorted(challenge_ids),'scope_guards':sorted(scope_ids)},
 'release_gate':{'science_lock':'PASS_F1','architecture_lock':'PASS_F2','scene_brief_lock':'PASS_F3','narratives':'PASS_F4A_F4G','challenge_lab':'PASS_F5','scope_guards':'PASS_F5','mixed_discrimination':'PASS_F5','exact_name_review':'PASS_F5','zero_loss_accounting':'PASS_F5'}
}
write(U3/'finalization-f5.json',finalization)

# Promote the F4G story registry without mutating any locked story file.
f4reg=read(U3/'journeys-f4g.json'); f5reg=dict(f4reg)
f5reg.update({'schema':'memory-palace-v2-unit3-f5-registry-1.0','narrative_standard':'V2-NARRATIVE-3.0-F5-STUDENT-READY','student_release':True,'preview_release':False,'release_status':'STUDENT_READY_F5'})
write(U3/'journeys-f5.json',f5reg)
status=read(U3/'status-f4g.json')
status.update({'status':'STUDENT_READY','pipeline_status':'UNIT3_FINALIZED_F5','pipeline_stage':'UNIT3_FINALIZED_F5','student_release':True,'preview_release':False,'application_challenges':11,'practice_only_records':11,'scope_guard_records':4,'mixed_discrimination_sets':28,'mixed_discrimination_questions':sum(len(x['questions']) for x in mixed),'exact_name_review_targets':len(review_targets),'canonical_records_accounted':186,'unaccounted_canonical_records':0,'next_required_output':'Classroom/browser validation of released Unit 3, then begin Unit 4 source inventory and scientific lock.','next_gate':'Unit 4 source-lock pipeline after Unit 3 classroom/browser validation.'})
write(U3/'status-f5.json',status); write(U3/'status.json',status)
course=read(COURSE)
for u in course['units']:
    if u['unit_id']=='unit-3':
        u.update({'status':'STUDENT_READY','journey_count':7,'scene_count':54,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5','polished_journeys':7,'polished_scenes':54,'student_release':True,'application_challenges':11,'scope_guard_records':4,'canonical_records_accounted':186})
write(COURSE,course)

files=['application-lab.json','review-manifest-f5.json','mixed-discrimination-f5.json','scope-guards-f5.json','finalization-f5.json','journeys-f5.json','status-f5.json']
lock={'schema':'memory-palace-v2-unit3-f5-content-lock-1.0','unit_id':'unit-3','stage':'F5','student_release':True,'files':{f:sha(U3/f) for f in files}}
write(U3/'content-lock-f5.json',lock)
release={'schema':'memory-palace-v2-unit3-f5-release-manifest-1.0','unit_id':'unit-3','stage':'F5','student_release':True,'preview_release':False,'canonical_records':186,'canonical_records_accounted':186,'unaccounted_canonical_records':0,'story_records':171,'practice_only_records':11,'scope_guard_records':4,'guided_journeys':7,'permanent_loci':54,'challenge_count':11,'exact_name_review_targets':len(review_targets),'mandatory_spelling_targets':0,'mixed_discrimination_sets':28,'mixed_discrimination_questions':sum(len(x['questions']) for x in mixed),'next_stage':'UNIT4_SOURCE_LOCK_AFTER_VALIDATION'}
write(U3/'f5-release-manifest.json',release)
print('Built Unit 3 F5:',json.dumps({k:release[k] for k in ['canonical_records_accounted','story_records','practice_only_records','scope_guard_records','challenge_count','exact_name_review_targets','mixed_discrimination_sets','mixed_discrimination_questions']},indent=2))
