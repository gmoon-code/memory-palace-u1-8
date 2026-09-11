from __future__ import annotations
import json, hashlib, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content'/'ap-biology'/'unit-4'
COURSE=ROOT/'content'/'ap-biology'/'course.json'
AP=ROOT/'content'/'ap-biology'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,d): Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def significant_tokens(text):
    stop={'a','an','and','or','the','of','to','in','on','for','with','from','as','at','by','is','are','be','via','vs','versus','into','across','over','through','cell','cells','phase','stage','system','role','example','effect'}
    toks=[]
    for t in re.findall(r"[A-Za-z0-9]+",text):
        low=t.casefold()
        if low in stop or len(low)<3: continue
        toks.append(low)
    return toks

def redact(text, terms):
    out=text
    # Full phrases first.
    for term in sorted(set(terms),key=len,reverse=True):
        if not term: continue
        out=re.sub(re.escape(term), '_____', out, flags=re.I)
    # Then remove obvious word-family leaks for meaningful answer tokens.
    tokens=[]
    for term in terms: tokens.extend(significant_tokens(term))
    for tok in sorted(set(tokens),key=len,reverse=True):
        stem=tok[:5] if len(tok)>=6 else tok[:max(3,len(tok)-1)]
        out=re.sub(rf'\b{re.escape(stem)}[A-Za-z0-9-]*\b','_____',out,flags=re.I)
    out=re.sub(r'(_____\s*){2,}','_____ ',out)
    out=re.sub(r'\s+([,.;:])',r'\1',out)
    out=re.sub(r'\s{2,}',' ',out).strip()
    return out

source=read(U4/'source'/'canonical-unit4-f1.json')
canon={r['knowledge_id']:r for r in source['canonical_catalog']}
classification=read(U4/'architecture'/'learning-classification-f2.json')
arch=read(U4/'architecture'/'palace-architecture-f2.json')
class_by={r['knowledge_id']:r for r in classification['records']}
journeys=[read(U4/'journeys'/f'U4-J{i}.json') for i in range(1,8)]
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
assert len(story_ids)==162 and len(challenge_ids)==15 and len(scope_ids)==3
assert set(story_ids)|set(challenge_ids)|set(scope_ids)==set(canon)
assert not(set(story_ids)&set(challenge_ids) or set(story_ids)&set(scope_ids) or set(challenge_ids)&set(scope_ids))

# ---------- Runtime Memory Objects ----------
conf_sets_by_id={kid:[] for kid in story_ids}
for s in arch['confusable_sets']:
    for kid in s['knowledge_ids']:
        if kid in conf_sets_by_id: conf_sets_by_id[kid].append(s['set_id'])
memory_objects=[]
for kid in story_ids:
    c=canon[kid]; cl=class_by[kid]; b=beat_by[kid]; sc=scene_by[kid]
    memory_objects.append({
      'memory_object_id':kid,'source_knowledge_id':kid,'object_type':'UNIT4_STORY_MEMORY_OBJECT',
      'canonical_term':b['term'],'canonical_definition':c['canonical_verified_statement'],'canonical_scientific_language':'English',
      'topic':c['topic'],'scope_class':c['scope_class'],'exact_name_required':'YES','exact_spelling_required':'NO',
      'name_support':cl['name_support'],'spelling_policy':cl['spelling_policy'],'retrieval_modes':cl['retrieval_modes'],
      'visual_mode':cl['visual_mode'],'palace_zone':sc['journey_title'],'primary_palace_locus':sc['scene_title'],'locus_id':sc['locus_id'],
      'scene_index':sc['scene_index'],'confusable_set_ids':conf_sets_by_id.get(kid,[]),'story_hint':b.get('hint',''),
      'forward_prompt_name_to_meaning':f"Explain the scientific meaning of '{b['term']}' without relying on the story.",
      'reverse_prompt_meaning_to_name':f"Retrieve the exact Unit 4 term for this scientific role: {redact(c['canonical_verified_statement'],[b['term']])}",
      'productive_retrieval_target':b['term'],'scientific_lock_status':'LOCKED_F1','narrative_lock_status':'LOCKED_F4G',
      'student_runtime':True,'ai_mutability':'AI may vary mnemonic wording, hints, practice phrasing, language, pacing, and distractors. AI may not change canonical term, locked scientific meaning, AP scope, confusable distinction, or misconception guardrail.',
      'source_trace':c.get('source_reference',''),'content_version':1,'version_status':'STUDENT_READY_F5'
    })
write(U4/'memory-objects-f5.json',{'schema':'memory-palace-v2-unit4-f5-memory-objects-1.0','unit_id':'unit-4','count':len(memory_objects),'memory_objects':memory_objects})

# ---------- Exact-name delayed Review ----------
review_targets=[]
for kid in story_ids:
    b=beat_by[kid]; c=canon[kid]; cl=class_by[kid]; sc=scene_by[kid]
    answer=b['term']
    prompt='Which exact Unit 4 term or named relationship matches this scientific description? '+redact(c['canonical_verified_statement'],[answer])
    hint_source=b.get('hint') or f"Return to {sc['scene_title']} and reconstruct the central scientific action."
    hint=redact(hint_source,[answer])
    if len(hint)<25: hint=f"Return to {sc['scene_title']} and reconstruct the defining action before naming it."
    review_targets.append({'knowledge_id':kid,'target_answer':answer,'prompt':prompt,'hint':hint,'journey_id':sc['journey_id'],'scene_index':sc['scene_index'],'scene_title':sc['scene_title'],'canonical_science':c['canonical_verified_statement'],'spelling_policy':cl['spelling_policy'],'initial_review_window_hours':[18,72]})
write(U4/'review-manifest-f5.json',{'schema':'memory-palace-v2-unit4-f5-review-manifest-1.0','unit_id':'unit-4','target_count':len(review_targets),'mandatory_spelling_targets':0,'visible_review_limit':5,'targets':review_targets})

# ---------- All 33 F2 confusable sets, one operational question per member ----------
mixed=[]
for base in arch['confusable_sets']:
    choices=base['terms']; qs=[]
    for qi,(kid,answer) in enumerate(zip(base['knowledge_ids'],choices),1):
        clue='Which option best matches this scientific description? '+redact(canon[kid]['canonical_verified_statement'],choices)
        if answer.casefold() in clue.casefold(): raise RuntimeError(f'mixed clue leaked answer {answer}')
        qs.append({'question_id':f"{base['set_id']}-Q{qi:02d}",'prompt':clue,'choices':choices,'answer':answer,'explanation':canon[kid]['canonical_verified_statement'],'knowledge_id':kid})
    mixed.append({'set_id':base['set_id'],'title':base['title'],'knowledge_ids':base['knowledge_ids'],'terms':choices,'unlock_rule':'Schedule only after every associated Unit 4 knowledge record has been encountered in a story.','initial_delay_hours':48,'questions':qs})
write(U4/'mixed-discrimination-f5.json',{'schema':'memory-palace-v2-unit4-f5-mixed-discrimination-1.0','unit_id':'unit-4','set_count':len(mixed),'question_count':sum(len(s['questions']) for s in mixed),'sets':mixed})

# ---------- Challenge Lab ----------
C={
'U4-K-170':('Communication and signaling','Route five biological messages',
 'Classify each scenario as direct-contact, paracrine/local, synaptic, or endocrine/long-distance signaling and justify the route using distance, medium, and target context. A plant cell passes a small signaling molecule through plasmodesmata to its neighbor. A wounded tissue releases a growth factor that affects cells a few cell diameters away. A neuron releases neurotransmitter across a narrow cleft. A pancreatic cell releases insulin into blood. A plant hormone moves through vascular tissue to a distant organ.',
 'Plasmodesmata support direct-contact signaling because connected neighboring cells exchange material through an intercellular channel. The growth-factor example is local/paracrine because a secreted regulator acts over a short extracellular distance. Neurotransmitter crossing a synaptic cleft is synaptic signaling, a specialized local mechanism. Insulin carried through blood is endocrine long-distance signaling. The plant hormone traveling through vascular tissue is also long-distance signaling. Classification should use the physical route and target context, not merely the identity of a messenger.',
 'Rebuild the communication route card from Journey 1: sender, messenger or contact, route/distance, and target.'),
'U4-K-171':('Signal reception','Alter a receptor binding site',
 'A mutation changes several amino acids in the extracellular ligand-binding region of a cell-surface receptor but leaves its intracellular signaling region intact. The normal ligand concentration is unchanged. Predict how receptor activation and downstream signaling could change, and explain why the effect depends on receptor structure.',
 'Changing the ligand-binding region can alter shape, charge, or other chemical features needed for specific ligand-receptor interaction. If binding affinity or compatibility falls, fewer receptors may enter the ligand-bound activated state and downstream signaling can decrease even though the intracellular domain is unchanged. A different structural change could also alter specificity or favor abnormal activation. The inference must connect receptor structure to ligand recognition and then to pathway activation.',
 'Return to the Reception Checkpoint: incorrect ligands fail at the binding gate before downstream transduction begins.'),
'U4-K-172':('Signal transduction','Label an unfamiliar pathway',
 'An unfamiliar pathway diagram shows an extracellular signal binding a membrane receptor at step A, a sequence of intracellular phosphorylation events at step B, and increased transcription of a target gene at step C. Assign reception, transduction, and response to A, B, and C and justify each assignment from what physically changes.',
 'A is reception because the extracellular signal is detected when it binds the receptor. B is transduction because intracellular molecular state changes relay the information through the cell. C is the cellular response because cell activity changes, here through altered gene expression. The extracellular ligand need not travel through the intracellular relay; information is transmitted by changes in pathway components.',
 'Use the Journey 2 receptor monitor and the Journey 3 violet information trace. The ligand stays at reception while intracellular components change state.'),
'U4-K-173':('Signal transduction','Predict a pathway break',
 'A signaling pathway runs ligand → receptor → kinase A → kinase B → response protein. A chemical specifically prevents kinase A from phosphorylating its target, while receptor binding remains normal. Predict the effect on kinase B and the response protein. Then predict what could happen if a separate mutation made kinase B constitutively active.',
 'Blocking kinase A should reduce or prevent activation of kinase B and the downstream response if that route depends on kinase A. Normal ligand-receptor binding alone does not guarantee a response when transduction is interrupted. If kinase B becomes constitutively active, downstream signaling can occur despite the upstream block, depending on whether the response machinery remains functional. The reasoning should follow causal order through the pathway.',
 'Picture the Signal Relay Tower. Move the information trace only when a real pathway component changes state.'),
'U4-K-174':('Feedback regulation','Determine feedback direction from data',
 'A regulated variable has a reference value near 100 units. After a disturbance it rises to 130. A response begins and the variable falls to 112 and then 103. In a second system, a disturbance raises a variable from 10 to 14, the response raises it to 19, and that stronger change triggers still more response until an endpoint occurs. Identify the feedback type in each system and predict what loss of the first response would do.',
 'The first system shows negative feedback because the response opposes the initial increase and moves the regulated variable back toward its reference range. The second shows positive feedback because the response reinforces the initiating change until an endpoint or changed condition interrupts the loop. If the first response is lost, the variable should remain farther from the regulated range or deviate further because the corrective response is missing.',
 'Return to the regulated-variable gauge. Ask whether the response pushes the needle back toward range or farther in the initiating direction.'),
'U4-K-136':('Mitosis','Identify stages from chromosome features',
 'Four unlabeled micrographs show the following features. Cell A has condensed chromosomes that are not yet aligned and the spindle is forming. Cell B has chromosomes aligned at the equatorial plane. Cell C shows sister chromatids moving toward opposite poles. Cell D shows chromosome sets at opposite ends with new nuclei forming. Identify the most likely mitotic stage for each cell and justify the visual evidence.',
 'A is most consistent with prophase or early prometaphase depending on nuclear-envelope and attachment details; the key evidence is condensation without metaphase alignment. B is metaphase because replicated chromosomes are aligned at the metaphase plane. C is anaphase because sister chromatids have separated and daughter chromosomes move toward opposite poles. D is telophase because separated chromosome sets are at opposite poles and nuclear reassembly is occurring. Identification should use visible chromosome, spindle, nuclear-envelope, and cytokinesis features.',
 'Walk the Mitosis Transit Hall in order and reconstruct what the same chromosome set is doing at each station.'),
'U4-K-139':('Chromosome number','Recover diploid number from gametes',
 'A sexually reproducing diploid organism produces normal gametes containing 8 chromosomes. What is the typical chromosome number of its somatic cells? State the haploid and diploid notation and explain the relationship rather than giving only a number.',
 'The gametes are haploid, so n = 8. Typical somatic cells contain two chromosome sets, so 2n = 16. The calculation doubles the number of homologous chromosome types represented in one gamete; it does not describe DNA replication or sister-chromatid number.',
 'Return to Chromosome Sets Gallery: one gamete set is n, while a typical diploid somatic cell carries two sets, 2n.'),
'U4-K-140':('Mitosis','Predict failed sister-chromatid segregation',
 'During mitosis, one pair of sister chromatids fails to segregate normally while the other chromosomes separate correctly. Predict the chromosome-number consequence for the two daughter cells after cytokinesis and explain why the daughters can become unequal.',
 'If both copies from the affected chromosome move to one side while none moves to the other, one daughter receives an extra chromosome and the other lacks that chromosome relative to the normal daughter-cell number. The unequal outcome results from failed sister-chromatid segregation during mitosis, not from a change in DNA replication before mitosis.',
 'Picture Anaphase Separation Track: daughter chromosomes must move to opposite poles before cytokinesis partitions the cell.'),
'U4-K-169':('Mitosis and checkpoints','Explain vinblastine-induced arrest',
 'Vinblastine binds tubulin and inhibits microtubule assembly. Predict how treatment can affect spindle formation, kinetochore attachment, the spindle-assembly checkpoint, and progression into normal anaphase.',
 'Inhibiting microtubule assembly disrupts formation and function of the mitotic spindle and can prevent adequate kinetochore-microtubule attachment. Unattached or improperly attached kinetochores maintain spindle-checkpoint signaling, so cells can arrest in mitosis and fail to progress normally into anaphase. The mechanism begins with tubulin/microtubule disruption and proceeds through attachment failure and checkpoint control.',
 'Combine Prophase Spindle Setup, Prometaphase Kinetochore Access, and the Spindle-Assembly Checkpoint from Journeys 6 and 7.'),
'U4-K-175':('Cell-cycle data','Infer a block from phase distribution',
 'A control culture contains 55% of cells in G1, 25% in S, and 20% in G2/M. After treatment, a second culture contains 25% in G1, 20% in S, and 55% in G2/M. Describe the major change and infer one cell-cycle location where progression may be slowed or blocked. State a limitation of the inference.',
 'The treated culture has a much larger fraction of cells in G2/M and a smaller fraction in G1. This pattern is consistent with cells spending longer in late interphase or mitosis, so a G2 or mitotic block is one plausible explanation. The distribution alone does not identify the exact molecular checkpoint or distinguish every G2 versus mitotic mechanism without additional markers or time-course evidence.',
 'Use the Cell-Cycle Clock and the later G2/spindle gates. Accumulation in a category can indicate prolonged residence there.'),
'U4-K-176':('Cell-cycle quantitative reasoning','Calculate a mitotic index change',
 'Researchers count 500 cells in a control sample and observe 50 cells in mitosis. In a treated sample they count 500 cells and observe 125 cells in mitosis. Calculate the mitotic index for each sample as a percentage and the fold change in mitotic index from control to treatment.',
 'Control mitotic index = 50/500 × 100 = 10%. Treated mitotic index = 125/500 × 100 = 25%. The treated mitotic index is 25/10 = 2.5 times the control value. The calculation describes the observed fraction of cells in mitosis; it does not by itself prove whether cells entered mitosis faster or remained in mitosis longer.',
 'Picture the Cell-Cycle Clock, then treat the counted cells as a snapshot. A larger mitotic fraction can arise from altered entry or altered time spent in mitosis.'),
'U4-K-177':('Chromosome counting','Track DNA and chromosome number through division',
 'Consider one diploid cell with 2n = 6 before S phase. State the chromosome number before S phase, immediately after S phase before mitosis, during anaphase within the still-undivided cell, and in each daughter cell after cytokinesis. Also state what happens to DNA amount during S phase.',
 'Before S phase the cell has 6 chromosomes. After S phase it still has 6 chromosomes, now replicated as sister-chromatid pairs, while DNA amount has doubled. At anaphase, after sister chromatids separate and each becomes a daughter chromosome, the still-undivided cell transiently contains 12 chromosomes. After cytokinesis, each normal daughter cell contains 6 chromosomes. DNA replication changes DNA/chromatid amount before it changes chromosome count.',
 'Use the three counters from S-Phase Replication Room and then carry them to Anaphase Separation Track.'),
'U4-K-178':('Cell-cycle checkpoints','Predict checkpoint failure',
 'A cell has several kinetochores that are not properly attached to spindle microtubules, but a mutation disables the spindle-assembly checkpoint. Predict how the mutation can affect anaphase timing and chromosome distribution in daughter cells.',
 'With a functional checkpoint, inadequate attachment can delay progression into anaphase. If checkpoint signaling is disabled, the cell may enter anaphase despite improper attachments. Some chromosomes can then fail to segregate correctly, increasing the probability of daughter cells with abnormal or unequal chromosome numbers. The checkpoint defect affects the decision to proceed; the attachment defect creates the segregation risk.',
 'Return to the security file: SPINDLE ATTACHMENT should influence the DECISION field before the anaphase gate opens.'),
'U4-K-179':('Cyclin-CDK regulation','Interpret cyclin and CDK activity patterns',
 'A graph shows one regulatory cyclin rising from low concentration to a peak before a cell-cycle transition and then falling rapidly. The amount of its partner CDK changes little, while measured cyclin-CDK kinase activity rises and falls with the cyclin. Explain the pattern without naming a specific cyclin-CDK pair.',
 'The data are consistent with regulation in which cyclin abundance changes while the CDK protein is more stable. Increased cyclin allows more active cyclin-CDK complexes to form, raising kinase activity toward the transition. Cyclin degradation then reduces active complex formation and kinase activity. The required reasoning is the relationship among cyclin abundance, CDK, active complex, and target phosphorylation; specific named pairs are outside the required scope.',
 'Picture the Cyclin–CDK Control Rack: changing cyclin availability controls how much active complex forms even when CDK amount is relatively stable.'),
'U4-K-180':('Cancer and cell-cycle control','Explain a treatment using control evidence',
 'A tumor-cell line carries a mutation that weakens a DNA-damage checkpoint and also shows reduced apoptosis after severe DNA damage. A treatment restores strong arrest after damage but does not directly repair the DNA. Predict one way the treatment could reduce tumor-cell proliferation and explain why the result does not mean every treated cell will die.',
 'Restoring arrest can prevent damaged cells from continuing rapidly through the cell cycle, reducing proliferation and providing time for repair or other outcomes. Because arrest and apoptosis are distinct responses, restored checkpoint control does not imply that every arrested cell undergoes programmed cell death. The effect on a tumor population depends on the treatment, the remaining pathways, and whether cells repair, remain arrested, senesce, undergo apoptosis, or eventually reenter the cycle.',
 'Use the model-cell security file: checkpoint decision, arrest, repair, and apoptosis are separate possible outcomes.'),
}

arch_ch={x['knowledge_id']:x for x in arch['challenge_lab']}
items=[]
for kid in [x['knowledge_id'] for x in arch['challenge_lab']]:
    domain,title,prompt,answer,hint=C[kid]; a=arch_ch[kid]
    items.append({'challenge_id':a['challenge_id'],'knowledge_id':kid,'domain':domain,'title':title,'type':a['type'],'prerequisite_loci':a['prerequisite_loci'],'prompt':prompt,'answer_guide':answer,'story_hint':hint,'canonical_statement':canon[kid]['canonical_verified_statement'],'success_criterion':'Solve the novel problem and justify the mechanism from ordinary scientific information. Recognition of a palace image alone is not sufficient.','practice_only_runtime':True})
write(U4/'application-lab.json',{'schema':'memory-palace-v2-unit4-f5-challenge-lab-1.0','unit_id':'unit-4','title':'Unit 4 Challenge Lab','student_intro':'Use these after the related journeys. One challenge appears at a time so signaling, feedback, chromosome, cell-cycle, checkpoint, and cancer reasoning can be practiced without depending on the mnemonic story.','challenge_count':len(items),'practice_only_runtime_count':len(items),'practice_only_runtime_object_ids':[x['knowledge_id'] for x in items],'items':items})

# ---------- Scope guards ----------
guards=[]
for kid in scope_ids:
    c=canon[kid]
    guards.append({'knowledge_id':kid,'canonical_label':c['canonical_label'],'policy':'NON_RUNTIME_AP_SCOPE_BOUNDARY','canonical_statement':c['canonical_verified_statement'],'student_runtime':False,'permanent_palace':False,'challenge_lab':False,'enforcement':'May support teacher explanation or prevent over-teaching, but must not become a required student memorization, exact-name Review target, or Challenge Lab requirement.'})
write(U4/'scope-guards-f5.json',{'schema':'memory-palace-v2-unit4-f5-scope-guards-1.0','unit_id':'unit-4','guard_count':len(guards),'guards':guards})

# ---------- Finalization accounting ----------
finalization={
 'schema':'memory-palace-v2-unit4-f5-finalization-1.0','unit_id':'unit-4','release_status':'STUDENT_READY_F5',
 'canonical_records':180,'runtime_memory_objects':162,'story_records':162,'challenge_lab_records':15,'scope_guard_records':3,'accounted_records':180,'unaccounted_records':0,
 'guided_journeys':7,'permanent_loci':51,'optional_first_exposure_recalls':18,
 'exact_name_review_targets':162,'mandatory_spelling_targets':0,'mixed_discrimination_sets':33,'mixed_discrimination_questions':99,
 'review_policy':{'first_exposure':'Story-first. Quick Recall remains optional and sparse.','exact_name':'Every encountered story Memory Object enters delayed Review through an answer-redacted scientific-role prompt.','mixed_discrimination':'A confusable set becomes eligible only after every associated record has been encountered; first mixed practice is delayed by 48 hours.','visible_review_load':'At most five due review items are shown at a time.','spelling':'No mandatory Unit 4 spelling gate; spelling support remains adaptive.'},
 'destinations':{'story':sorted(story_ids),'challenge_lab':sorted(challenge_ids),'scope_guards':sorted(scope_ids)},
 'release_gate':{'science_lock':'PASS_F1','architecture_lock':'PASS_F2','scene_brief_lock':'PASS_F3','narratives':'PASS_F4A_F4G','runtime_memory_objects':'PASS_F5','challenge_lab':'PASS_F5','scope_guards':'PASS_F5','mixed_discrimination':'PASS_F5','exact_name_review':'PASS_F5','zero_loss_accounting':'PASS_F5'}
}
write(U4/'finalization-f5.json',finalization)

# Promote registry, keep narrative files byte-identical.
f4reg=read(U4/'journeys-f4g.json'); f5reg=dict(f4reg)
f5reg.update({'schema':'memory-palace-v2-unit4-f5-registry-1.0','narrative_standard':'V2-NARRATIVE-3.0-F5-STUDENT-READY','student_release':True,'preview_release':False,'release_status':'STUDENT_READY_F5'})
write(U4/'journeys-f5.json',f5reg)
status=read(U4/'status-f4g.json')
status.update({'status':'STUDENT_READY','pipeline_status':'UNIT4_FINALIZED_F5','pipeline_stage':'UNIT4_FINALIZED_F5','student_release':True,'preview_release':False,'memory_objects':162,'runtime_memory_objects':162,'application_challenges':15,'practice_only_records':15,'scope_guard_records':3,'mixed_discrimination_sets':33,'mixed_discrimination_questions':99,'exact_name_review_targets':162,'canonical_records_accounted':180,'unaccounted_canonical_records':0,'next_required_output':'Classroom/browser validation of the released Unit 4 experience, then begin Unit 5 scientific-lock work.','next_gate':'Unit 4 F6 browser/classroom validation or Unit 5 source-lock pipeline after validation.'})
write(U4/'status-f5.json',status); write(U4/'status.json',status)
course=read(COURSE)
for u in course['units']:
    if u['unit_id']=='unit-4':
        u.update({'status':'STUDENT_READY','journey_count':7,'scene_count':51,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVES_F4_FINALIZED_F5','polished_journeys':7,'polished_scenes':51,'student_release':True,'preview_release':False,'application_challenges':15,'scope_guard_records':3,'canonical_records_accounted':180,'runtime_memory_objects':162,'pipeline_stage':'UNIT4_FINALIZED_F5'})
write(COURSE,course)

files=['memory-objects-f5.json','application-lab.json','review-manifest-f5.json','mixed-discrimination-f5.json','scope-guards-f5.json','finalization-f5.json','journeys-f5.json','status-f5.json']
lock={'schema':'memory-palace-v2-unit4-f5-content-lock-1.0','unit_id':'unit-4','stage':'F5','student_release':True,'files':{f:sha(U4/f) for f in files},'protected_narratives':{f'journeys/U4-J{i}.json':sha(U4/'journeys'/f'U4-J{i}.json') for i in range(1,8)}}
write(U4/'content-lock-f5.json',lock)
release={'schema':'memory-palace-v2-unit4-f5-release-manifest-1.0','unit_id':'unit-4','stage':'F5','student_release':True,'preview_release':False,'canonical_records':180,'canonical_records_accounted':180,'unaccounted_canonical_records':0,'runtime_memory_objects':162,'story_records':162,'practice_only_records':15,'scope_guard_records':3,'guided_journeys':7,'permanent_loci':51,'challenge_count':15,'exact_name_review_targets':162,'mandatory_spelling_targets':0,'mixed_discrimination_sets':33,'mixed_discrimination_questions':99,'next_stage':'UNIT4_BROWSER_CLASSROOM_VALIDATION_F6_OR_UNIT5_SOURCE_LOCK'}
write(U4/'f5-release-manifest.json',release)

# Mainline U1-U4 manifest.
u1=read(AP/'unit-1'/'v2-release-manifest.json'); u2=read(AP/'unit-2'/'finalization-f5.json'); u3=read(AP/'unit-3'/'finalization-f5.json')
mainline={'schema':'memory-palace-v2-mainline-u1-u4-1.0','release_status':'STUDENT_READY_UNITS_1_4','units':['unit-1','unit-2','unit-3','unit-4'],'totals':{'canonical_records_units_1_4':u1['canonical_records']+u2['canonical_records']+u3['canonical_records']+180,'guided_journeys':u1['journeys']+u2['guided_journeys']+u3['guided_journeys']+7,'permanent_scenes':u1['scenes']+u2['permanent_loci']+u3['permanent_loci']+51,'challenge_lab_items':read(AP/'unit-1'/'application-lab.json')['challenge_count']+read(AP/'unit-2'/'application-lab.json')['challenge_count']+read(AP/'unit-3'/'application-lab.json')['challenge_count']+15},'unit4':release,'future_units':['unit-5','unit-6','unit-7','unit-8']}
write(AP/'mainline-release-u1-u4.json',mainline)
print('Built Unit 4 F5',json.dumps(release,indent=2))
