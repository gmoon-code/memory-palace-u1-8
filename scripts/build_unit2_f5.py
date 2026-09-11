from __future__ import annotations
import json, hashlib, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
COURSE=ROOT/'content'/'ap-biology'/'course.json'

def read(path): return json.loads(Path(path).read_text(encoding='utf-8'))
def write(path,data): Path(path).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

source=read(U2/'source'/'canonical-unit2-f1.json')
canon={r['knowledge_id']:r for r in source['canonical_catalog']}
classification=read(U2/'architecture'/'learning-classification-f2.json')
arch=read(U2/'architecture'/'palace-architecture-f2.json')
class_by_id={r['knowledge_id']:r for r in classification['records']}

journeys=[read(U2/'journeys'/f'U2-J{i}.json') for i in range(1,8)]
beat_by_id={}
scene_by_id={}
for j in journeys:
    for s in j['scenes']:
        for b in s['story_beats']:
            beat_by_id[b['object_id']]=b
            scene_by_id[b['object_id']]={'journey_id':j['palace_id'],'journey_title':j['story_title'],'scene_index':s['scene_index'],'scene_title':s['locus']}

# ---------- Challenge Lab: the nine records intentionally kept outside permanent palace loci ----------
CHALLENGES=[
 {
  'challenge_id':'U2-APP-01','knowledge_id':'U2-K-134','domain':'Cell structure and secretion','title':'Albumin production under organelle disruption',
  'prompt':'A liver cell continues transcribing an albumin gene normally, but extensive damage disrupts rough endoplasmic reticulum and Golgi function. Predict how secretion of albumin into the blood would change and explain the cellular pathway responsible.',
  'answer_guide':'Albumin secretion should decrease. A secreted protein is translated by ribosomes associated with the rough ER, enters the endomembrane trafficking pathway, is transported to and processed/sorted by the Golgi, and is ultimately delivered in secretory vesicles for exocytosis. Disruption of rough ER and Golgi function therefore interferes with production/processing/trafficking even if transcription remains normal.',
  'story_hint':'Picture the red protein-cargo case moving from bound ribosomes into rough ER, then through receiving and dispatch sides of the Golgi before a secretory vesicle can leave the cell.'},
 {
  'challenge_id':'U2-APP-02','knowledge_id':'U2-K-135','domain':'Cell structure and secretion','title':'Trace a newly made insulin molecule',
  'prompt':'A pancreatic cell has just begun producing a molecule of insulin for secretion. Trace the major cellular structures the protein uses from translation to release outside the cell.',
  'answer_guide':'Translation occurs on ribosomes bound to the rough ER. The protein enters the ER for folding/processing, moves in transport vesicles to the Golgi, is further processed and sorted there, is packaged into secretory vesicles, and is released when those vesicles fuse with the plasma membrane by exocytosis.',
  'story_hint':'Follow one secreted protein through the same route as the red-tracked cargo in Cell Operations Complex: bound ribosome → rough ER → vesicle → Golgi → secretory vesicle → plasma membrane.'},
 {
  'challenge_id':'U2-APP-03','knowledge_id':'U2-K-136','domain':'Organelle function','title':'Detoxification and damaged-organelle cleanup',
  'prompt':'A liver cell is exposed repeatedly to a chemical that requires detoxification, and some of its organelles become damaged. Identify the organelle system expected to increase detoxification activity and the cellular process that can deliver damaged organelles for degradation.',
  'answer_guide':'Smooth ER is associated with detoxification of drugs and poisons in liver cells. Damaged organelles can be enclosed and delivered to lysosomes through autophagy, where lysosomal hydrolytic enzymes break down the material for recycling.',
  'story_hint':'Return to the smooth ER detoxification bench, then picture the recycling bay receiving a membrane-wrapped damaged organelle through autophagy.'},
 {
  'challenge_id':'U2-APP-04','knowledge_id':'U2-K-137','domain':'Cell size and geometry','title':'Surface area-to-volume calculation',
  'prompt':'Compare two cube-shaped cells. Cell A has side length 1 μm and Cell B has side length 4 μm. Calculate surface area, volume, and surface-area-to-volume ratio for each. Which has more membrane surface available relative to the amount of cytoplasm it must support?',
  'answer_guide':'For a cube, SA = 6s² and V = s³. Cell A: SA = 6 μm², V = 1 μm³, SA:V = 6:1. Cell B: SA = 96 μm², V = 64 μm³, SA:V = 1.5:1. Cell B has more total surface area, but Cell A has much more surface area relative to its volume and therefore a more favorable exchange ratio.',
  'story_hint':'Picture the small bright cube beside the enlarged cube whose center darkens even though its total outside surface is larger.'},
 {
  'challenge_id':'U2-APP-05','knowledge_id':'U2-K-138','domain':'Membrane fluidity','title':'Cold-water membrane adaptation',
  'prompt':'Two closely related fish populations live at different temperatures. The cold-water population has a greater proportion of unsaturated fatty-acid tails in its membrane phospholipids. Explain how this difference can help membrane function in the colder environment.',
  'answer_guide':'Cis double bonds in unsaturated fatty-acid tails introduce kinks that prevent phospholipids from packing as tightly. In cold conditions, this helps preserve membrane fluidity when lower temperature would otherwise reduce molecular movement and promote tighter packing.',
  'story_hint':'Picture the cold end of Fluidity Climate Control, where kinked unsaturated tails keep neighboring phospholipids from packing into a rigid wall.'},
 {
  'challenge_id':'U2-APP-06','knowledge_id':'U2-K-139','domain':'Diffusion','title':'Read a diffusion diagram',
  'prompt':'A membrane is permeable to molecule X. At time 0, the left side contains 90 X molecules and the right side contains 10. Predict the initial net direction of diffusion. Later both sides contain equal concentrations. Describe molecular movement at that later time.',
  'answer_guide':'Initially there is net diffusion from left to right, down the concentration gradient. At equal concentrations, X molecules still move randomly across the membrane in both directions, but the opposing rates are equal so there is no net movement in either direction.',
  'story_hint':'Return to the Concentration Ramp: particles never stop moving, but the crowd difference determines the net direction until dynamic equilibrium is reached.'},
 {
  'challenge_id':'U2-APP-07','knowledge_id':'U2-K-140','domain':'Cotransport','title':'Sucrose uptake and external pH',
  'prompt':'A plant cell uses an H⁺/sucrose symporter to import sucrose. An ATP-driven proton pump maintains a higher H⁺ concentration outside the cell. Predict what would happen to sucrose uptake if the external solution becomes less acidic while the other conditions remain similar, and justify the prediction.',
  'answer_guide':'Sucrose uptake would generally decrease because a less acidic external solution has a lower H⁺ concentration, weakening the H⁺ electrochemical gradient that supplies the immediate energy for H⁺/sucrose cotransport. The symporter itself does not directly hydrolyze ATP in this mechanism; ATP was used by the proton pump to establish the gradient.',
  'story_hint':'Picture the final transit platform: ATP powers the proton pump first, the stored H⁺ gradient forms, and downhill H⁺ movement then carries sucrose uphill through the symporter.'},
 {
  'challenge_id':'U2-APP-08','knowledge_id':'U2-K-141','domain':'Cell recognition and bulk transport','title':'Macrophage recognition and engulfment',
  'prompt':'A macrophage recognizes molecular features on the surface of a bacterium, extends its membrane around the bacterium, and encloses it in an internal vesicle. Name the transport process and explain how cell-surface recognition contributes to the response.',
  'answer_guide':'The uptake process is phagocytosis, a form of endocytosis for large particles. Cell-surface recognition molecules and receptors help the macrophage distinguish and bind relevant external targets; membrane remodeling then engulfs the bacterium into a vesicle for intracellular processing.',
  'story_hint':'Picture the recognition counter identifying an external surface pattern, followed by the phagocytosis bay wrapping membrane around one large particle.'},
 {
  'challenge_id':'U2-APP-09','knowledge_id':'U2-K-142','domain':'Water potential','title':'Calculate water potential and predict movement',
  'prompt':'A plant cell has a 0.20 M sucrose solution at 300 K and pressure potential Ψp = +2.0 bar. Use i = 1 and R = 0.0831 L·bar·mol⁻¹·K⁻¹. Calculate Ψs using Ψs = −iCRT, calculate total Ψ, and predict the net direction of water movement if the cell is placed in pure water at Ψ = 0 bar.',
  'answer_guide':'Ψs = −(1)(0.20)(0.0831)(300) = −4.986 bar. Total Ψ = Ψp + Ψs = +2.0 + (−4.986) = −2.986 bar, approximately −3.0 bar. Water moves net from the higher water potential outside (0 bar) toward the lower water potential inside the cell (about −3.0 bar).',
  'story_hint':'Picture the final conservatory control panel: calculate the negative solute component first, add the pressure component, then move water from the chamber with higher total Ψ toward the chamber with lower total Ψ.'}
]
for item in CHALLENGES:
    item['canonical_statement']=canon[item['knowledge_id']]['canonical_verified_statement']
    item['success_criterion']='Solve the fresh problem and justify the mechanism using ordinary scientific information. Recognition of a palace image alone is not sufficient.'
    item['practice_only_runtime']=True
application_lab={
 'schema':'memory-palace-v2-unit2-f5-challenge-lab-1.0','unit_id':'unit-2','title':'Unit 2 Challenge Lab',
 'student_intro':'Use these after the related journeys. One challenge appears at a time so calculation and application practice stays manageable.',
 'challenge_count':len(CHALLENGES),'practice_only_runtime_count':9,
 'practice_only_runtime_object_ids':[x['knowledge_id'] for x in CHALLENGES], 'items':CHALLENGES
}
write(U2/'application-lab.json',application_lab)

# ---------- Exact-name review manifest with target leakage removed ----------
STOP={'and','the','with','from','into','that','this','than','versus','for','of','to','in','as','a','an','or'}
def redact_target(text:str,answer:str)->str:
    out=text
    # full answer phrase first
    out=re.sub(re.escape(answer), '_____', out, flags=re.I)
    words=[w.lower() for w in re.findall(r"[A-Za-z]+",answer) if w.lower() not in STOP]
    for w in sorted(set(words),key=len,reverse=True):
        if len(w)<=2: continue
        stem=w[:5] if len(w)>=6 else w[:max(3,len(w)-1)]
        out=re.sub(rf'\b{re.escape(stem)}[A-Za-z]*\b','_____',out,flags=re.I)
    out=re.sub(r'\s+',' ',out).strip()
    return out

review_targets=[]
for r in classification['records']:
    if not r['exact_name_recall']: continue
    kid=r['knowledge_id']; beat=beat_by_id[kid]; loc=scene_by_id[kid]
    answer=beat['term']
    cue=redact_target(beat['science'],answer)
    hint=redact_target(beat.get('hint',''),answer)
    if len(hint)<25: hint='Picture the defining structure or action from the journey and retrieve the scientific name before revealing it.'
    review_targets.append({
      'knowledge_id':kid,'target_answer':answer,
      'prompt':f'Which exact Unit 2 name matches this scientific description? {cue}',
      'hint':hint,'journey_id':loc['journey_id'],'scene_index':loc['scene_index'],'scene_title':loc['scene_title'],
      'canonical_science':beat['science'],'spelling_policy':r['spelling_policy']
    })
review_manifest={'schema':'memory-palace-v2-unit2-f5-review-manifest-1.0','unit_id':'unit-2','target_count':len(review_targets),'mandatory_spelling_targets':0,'targets':review_targets}
write(U2/'review-manifest-f5.json',review_manifest)

# ---------- Delayed mixed discrimination ----------
SETS=[
 ('U2-CF-01','Cell organization',['prokaryotic cell','eukaryotic cell'],[
  ('A cell has DNA in a nucleoid region and lacks a membrane-bound nucleus.','prokaryotic cell','A prokaryotic cell lacks a membrane-bound nucleus.'),
  ('A cell encloses its DNA in a nucleus and contains membrane-bound organelles.','eukaryotic cell','A eukaryotic cell contains a nucleus and membrane-bound organelles.')]),
 ('U2-CF-02','Ribosome location and destination',['free ribosomes','bound ribosomes'],[
  ('These ribosomes generally make proteins that function in the cytosol.','free ribosomes','Free ribosomes are suspended in the cytosol and commonly make proteins used there.'),
  ('These ribosomes are attached to rough ER or the nuclear envelope and commonly make proteins for secretion or membranes.','bound ribosomes','Bound ribosomes direct newly made proteins into the endomembrane pathway.')]),
 ('U2-CF-03','ER identity',['rough ER','smooth ER'],[
  ('This membrane network has ribosomes attached and handles proteins entering the endomembrane pathway.','rough ER','Rough ER has bound ribosomes and participates in protein processing and membrane production.'),
  ('This membrane network lacks bound ribosomes and is associated with lipid synthesis, detoxification, and carbohydrate metabolism.','smooth ER','Smooth ER lacks bound ribosomes and performs these metabolic functions.')]),
 ('U2-CF-04','Golgi directionality',['cis face','trans face'],[
  ('This side of the Golgi receives incoming transport vesicles from the ER.','cis face','The cis face is the receiving side.'),
  ('This side sorts and dispatches vesicles toward other destinations.','trans face','The trans face is the shipping side.')]),
 ('U2-CF-05','Digestive versus oxidative organelles',['lysosome','peroxisome'],[
  ('This acidic digestive compartment contains hydrolytic enzymes and participates in breakdown and recycling.','lysosome','Lysosomes digest macromolecules and damaged material with hydrolytic enzymes.'),
  ('This organelle carries out oxidative reactions and contains enzymes such as catalase that handle hydrogen peroxide.','peroxisome','Peroxisomes perform oxidative chemistry and manage hydrogen peroxide.')]),
 ('U2-CF-06','Cytoskeletal elements',['microtubule','microfilament / actin filament','intermediate filament'],[
  ('This hollow cytoskeletal element forms tracks for motor proteins and contributes to the mitotic spindle.','microtubule','Microtubules are hollow tubulin structures used in transport and chromosome movement.'),
  ('This thin actin-based element supports cell shape changes, contraction, and cell crawling.','microfilament / actin filament','Microfilaments are actin filaments involved in shape and movement.'),
  ('This rope-like element provides durable mechanical strength and helps stabilize cell structure.','intermediate filament','Intermediate filaments provide tensile strength and structural stability.')]),
 ('U2-CF-07','Chloroplast internal structures',['thylakoid','granum','stroma'],[
  ('This is one flattened membrane sac whose membrane contains chlorophyll and supports light-dependent reactions.','thylakoid','A thylakoid is an individual membrane sac.'),
  ('This is a stack of thylakoids.','granum','A granum is a stack of thylakoid membrane sacs inside a chloroplast.'),
  ('This fluid region surrounds thylakoids and contains enzymes used in the Calvin cycle.','stroma','The stroma is the chloroplast fluid outside the thylakoids.')]),
 ('U2-CF-08','Membrane protein placement',['integral membrane protein','peripheral membrane protein','transmembrane protein'],[
  ('This protein penetrates the hydrophobic interior of the bilayer but does not necessarily cross the whole membrane.','integral membrane protein','Integral proteins penetrate the bilayer; some are transmembrane and some are not.'),
  ('This protein is loosely attached to the membrane surface or to exposed portions of another protein.','peripheral membrane protein','Peripheral proteins remain associated with the membrane surface.'),
  ('This integral protein spans the bilayer from one side to the other.','transmembrane protein','A transmembrane protein crosses the entire bilayer.')]),
 ('U2-CF-09','Membrane carbohydrate labels',['glycolipid','glycoprotein'],[
  ('A membrane carbohydrate chain is covalently attached to a lipid.','glycolipid','A glycolipid is a lipid with an attached carbohydrate.'),
  ('A membrane carbohydrate chain is covalently attached to a protein.','glycoprotein','A glycoprotein is a protein with an attached carbohydrate.')]),
 ('U2-CF-10','Transport energy and mechanism',['passive transport','facilitated diffusion','active transport'],[
  ('Net movement occurs down a gradient without direct metabolic-energy input.','passive transport','Passive transport does not directly require metabolic energy.'),
  ('A solute moves down its gradient through a channel or carrier without direct energy input.','facilitated diffusion','Facilitated diffusion is passive but uses a membrane protein.'),
  ('A membrane transport process requires direct energy input and can build or maintain a gradient.','active transport','Active transport uses energy to move substances in ways that can oppose spontaneous movement.')]),
 ('U2-CF-11','Protein-mediated membrane routes',['channel protein','carrier protein','aquaporin'],[
  ('This membrane protein forms a hydrophilic passageway that selected ions or molecules can move through.','channel protein','Channel proteins provide hydrophilic pores.'),
  ('This membrane protein binds a solute and changes conformation to move it across the membrane.','carrier protein','Carrier proteins alternate conformations after binding their solute.'),
  ('This specialized channel greatly increases the rate of water movement across a membrane.','aquaporin','Aquaporins are specialized membrane channels that greatly increase water permeability.')]),
 ('U2-CF-12','Bulk transport direction',['endocytosis','exocytosis'],[
  ('The plasma membrane bends inward and pinches off to bring material into the cell in a vesicle.','endocytosis','Endocytosis brings material into the cell.'),
  ('An internal vesicle fuses with the plasma membrane and releases material outside the cell.','exocytosis','Exocytosis releases vesicle contents outside the cell.')]),
 ('U2-CF-13','Endocytosis subtypes',['phagocytosis','pinocytosis','receptor-mediated endocytosis'],[
  ('A cell engulfs a large particle or microorganism.','phagocytosis','Phagocytosis is uptake of large particles.'),
  ('A cell nonspecifically takes in extracellular fluid and dissolved substances.','pinocytosis','Pinocytosis samples extracellular fluid.'),
  ('Specific ligands bind surface receptors and are concentrated before vesicle uptake.','receptor-mediated endocytosis','Receptor-mediated endocytosis selectively concentrates receptor-bound cargo.')]),
 ('U2-CF-14','Tonicity',['hypotonic','isotonic','hypertonic'],[
  ('Relative to the cell, this solution causes net water entry.','hypotonic','A hypotonic environment drives net water into the cell.'),
  ('Relative to the cell, opposing water movements balance so there is no net change in water amount.','isotonic','An isotonic environment has no net water movement even though water still moves both ways.'),
  ('Relative to the cell, this solution causes net water loss.','hypertonic','A hypertonic environment drives net water out of the cell.')]),
 ('U2-CF-15','Water-potential components',['water potential','pressure potential','solute potential'],[
  ('This total predicts the direction of net water movement and equals the sum of pressure and solute components.','water potential','Water potential combines pressure potential and solute potential: Ψ = Ψp + Ψs.'),
  ('This component represents physical pressure and can be positive in a turgid plant cell.','pressure potential','Pressure potential is the physical-pressure contribution to total water potential.'),
  ('This component becomes more negative as dissolved-solute concentration increases.','solute potential','Solute potential is zero for pure water under the standard convention and negative for solutions.')]),
 ('U2-CF-16','Electrochemical transport',['electrogenic pump','Na+/K+ ATPase','proton pump','cotransport'],[
  ('This general type of pump contributes to membrane voltage because its transport cycle moves net charge across the membrane.','electrogenic pump','Electrogenic pumps create net charge separation.'),
  ('In animal cells, this ATP-driven pump moves 3 Na⁺ out and 2 K⁺ in per cycle.','Na+/K+ ATPase','The sodium-potassium pump has a 3 Na⁺ out / 2 K⁺ in stoichiometry per ATP.'),
  ('This ATP-driven transporter builds an H⁺ electrochemical gradient across a membrane.','proton pump','A proton pump uses energy to move H⁺ and build a gradient.'),
  ('This mechanism couples downhill movement of one substance to uphill movement of another.','cotransport','Cotransport uses energy stored in an existing gradient.')]),
 ('U2-CF-17','Energy organelles',['mitochondrion','chloroplast'],[
  ('This double-membrane organelle contains an intermembrane space, a matrix, and an inner membrane folded into cristae.','mitochondrion','Mitochondria contain cristae and a matrix and participate in aerobic cellular respiration.'),
  ('This double-membrane organelle contains thylakoids, grana, stroma, and chlorophyll and carries out photosynthesis.','chloroplast','Chloroplasts contain thylakoid membranes and stroma and perform photosynthesis.')])
]
arch_sets={x['set_id']:x for x in arch['confusable_sets']}
mixed=[]
for sid,title,choices,qs in SETS:
    base=arch_sets[sid]
    questions=[]
    for qi,(prompt,answer,explanation) in enumerate(qs,1):
        questions.append({'question_id':f'{sid}-Q{qi:02d}','prompt':prompt,'choices':choices,'answer':answer,'explanation':explanation})
    mixed.append({'set_id':sid,'title':title,'knowledge_ids':base['knowledge_ids'],'terms':choices,'unlock_rule':'Schedule only after every associated knowledge record has been encountered in a completed or in-progress story.','initial_delay_hours':48,'questions':questions})

mixed_manifest={'schema':'memory-palace-v2-unit2-f5-mixed-discrimination-1.0','unit_id':'unit-2','set_count':len(mixed),'question_count':sum(len(x['questions']) for x in mixed),'sets':mixed}
write(U2/'mixed-discrimination-f5.json',mixed_manifest)

# ---------- Full canonical destination / release audit ----------
story_ids=[]
for j in journeys:
    for s in j['scenes']: story_ids.extend(s['object_ids'])
challenge_ids=[x['knowledge_id'] for x in CHALLENGES]
all_ids=set(canon)
assert len(story_ids)==133 and len(set(story_ids))==133
assert len(challenge_ids)==9 and len(set(challenge_ids))==9
assert set(story_ids).isdisjoint(challenge_ids)
assert set(story_ids)|set(challenge_ids)==all_ids

finalization={
 'schema':'memory-palace-v2-unit2-f5-finalization-1.0','unit_id':'unit-2','release_status':'STUDENT_READY_F5',
 'canonical_records':142,'story_records':133,'challenge_lab_records':9,'accounted_records':142,'unaccounted_records':0,
 'guided_journeys':7,'permanent_loci':49,'optional_first_exposure_recalls':17,
 'exact_name_review_targets':len(review_targets),'mandatory_spelling_targets':0,
 'mixed_discrimination_sets':len(mixed),'mixed_discrimination_questions':sum(len(x['questions']) for x in mixed),
 'review_policy':{
   'first_exposure':'Story-first. Quick Recall remains optional.',
   'exact_name':'Encountered exact-name targets enter delayed Review with answer-redacted scientific-role prompts.',
   'mixed_discrimination':'A confusable set becomes eligible only after all associated records have been encountered; its first mixed question is delayed by 48 hours.',
   'visible_review_load':'At most five due review items are shown at a time.',
   'spelling':'No mandatory Unit 2 spelling gate.'
 },
 'destinations':{
   'story':sorted(story_ids),
   'challenge_lab':sorted(challenge_ids)
 },
 'release_gate':{'science_lock':'PASS_F1','architecture_lock':'PASS_F2','scene_brief_lock':'PASS_F3','narratives':'PASS_F4A_F4G','challenge_lab':'PASS_F5','mixed_discrimination':'PASS_F5','exact_name_review':'PASS_F5','zero_loss_accounting':'PASS_F5'}
}
write(U2/'finalization-f5.json',finalization)

# Registry promoted without mutating the locked F4 journey story files.
f4reg=read(U2/'journeys-f4g.json')
f5reg=dict(f4reg)
f5reg.update({'schema':'memory-palace-v2-unit2-f5-registry-1.0','narrative_standard':'V2-NARRATIVE-3.0-F5-STUDENT-READY','student_release':True,'release_status':'STUDENT_READY_F5'})
write(U2/'journeys-f5.json',f5reg)

status=read(U2/'status-f4g.json')
status.update({
 'status':'STUDENT_READY','pipeline_stage':'UNIT2_FINALIZED_F5','student_release':True,'preview_release':False,
 'application_challenges':9,'practice_only_records':9,'mixed_discrimination_sets':17,
 'mixed_discrimination_questions':sum(len(x['questions']) for x in mixed),'exact_name_review_targets':len(review_targets),
 'canonical_records_accounted':142,'unaccounted_canonical_records':0,
 'next_required_output':'Classroom/browser validation of the released Unit 2 experience, then Unit 3 source inventory and scientific lock.',
 'next_gate':'Unit 3 source-lock pipeline after Unit 2 classroom/browser validation.'
})
write(U2/'status-f5.json',status)

course=read(COURSE)
for u in course['units']:
    if u['unit_id']=='unit-2':
        u.update({'status':'STUDENT_READY','journey_count':7,'scene_count':49,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5','polished_journeys':7,'polished_scenes':49,'student_release':True,'application_challenges':9})
write(COURSE,course)

files=['application-lab.json','review-manifest-f5.json','mixed-discrimination-f5.json','finalization-f5.json','journeys-f5.json','status-f5.json']
lock={'schema':'memory-palace-v2-unit2-f5-content-lock-1.0','unit_id':'unit-2','stage':'F5','student_release':True,'files':{f:sha(U2/f) for f in files}}
write(U2/'content-lock-f5.json',lock)
release={
 'schema':'memory-palace-v2-unit2-f5-release-manifest-1.0','unit_id':'unit-2','stage':'F5','student_release':True,'preview_release':False,
 'canonical_records':142,'canonical_records_accounted':142,'unaccounted_canonical_records':0,
 'story_records':133,'practice_only_records':9,'guided_journeys':7,'permanent_loci':49,
 'challenge_count':9,'exact_name_review_targets':len(review_targets),'mandatory_spelling_targets':0,
 'mixed_discrimination_sets':17,'mixed_discrimination_questions':sum(len(x['questions']) for x in mixed),
 'next_stage':'UNIT3_SOURCE_LOCK_AFTER_VALIDATION'
}
write(U2/'f5-release-manifest.json',release)
print('Built Unit 2 F5:',json.dumps({k:release[k] for k in ['canonical_records_accounted','story_records','practice_only_records','challenge_count','exact_name_review_targets','mixed_discrimination_sets','mixed_discrimination_questions']},indent=2))
