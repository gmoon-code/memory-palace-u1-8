from __future__ import annotations
import json, hashlib, re, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'
# F4C extends the deterministic F4B baseline.
subprocess.run([sys.executable,str(ROOT/'scripts'/'build_unit5_f4b.py')],check=True,stdout=subprocess.DEVNULL)
F3=json.loads((U5/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS=json.loads((U5/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J3=next(j for j in JBRIEFS if j['journey_id']=='U5-J3')
B={b['locus_id']:b for b in F3 if b['journey_id']=='U5-J3'}
CANON={r['knowledge_id']:r for r in json.loads((U5/'source'/'canonical-unit5-f1.json').read_text(encoding='utf-8'))['canonical_catalog']}
J1=json.loads((U5/'journeys'/'U5-J1.json').read_text(encoding='utf-8'))
J2=json.loads((U5/'journeys'/'U5-J2.json').read_text(encoding='utf-8'))

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

GUIDE={
 'name':'Dr. Imani Reyes','role':'inheritance-systems geneticist',
 'visual':'deep-green field coat, clear gloves, compact chromosome tablet preserving the same blue/amber parental-origin chromosome identities from the meiosis hall, plus the narrow gold generation ledger',
 'story_job':'Imani keeps normal diversity mechanisms separate from chromosome-segregation failures. She makes the outcome scanner change modes before the error cases begin, so allele-combination diversity is never confused with abnormal chromosome number.'
}
SCANNER={
 'name':'Chromosome-outcome scanner','kind':'continuity instrument',
 'visual':'a waist-high black-and-glass scanner with two unmistakable settings: violet DIVERSITY MODE reads allele combinations, while red SEGREGATION-INTEGRITY MODE reads chromosome movement and copy number',
 'job':'follows the same chromosome outcomes through the center. It first identifies normal sources of new allele combinations, then switches modes before checking nondisjunction and chromosome-number outcomes.'
}
LEDGER={
 'name':'Gold generation ledger','kind':'continuity record',
 'visual':'the same narrow gold ledger from Journeys 1–2, now carrying separate columns for ALLELE COMBINATION, SEGREGATION EVENT, and CHROMOSOME COUNT',
 'job':'records the causal category of each outcome so normal recombination, segregation failure, and resulting chromosome-number state remain distinct.'
}

route=[
 {'scene_index':0,'locus':'Variation Sources Compass','short':'Three sources','floor':'Diversity floor','symbol':'3↗'},
 {'scene_index':1,'locus':'Segregation Integrity Gate','short':'Movement check','floor':'Integrity floor','symbol':'✓/✕'},
 {'scene_index':2,'locus':'Aneuploidy Diagnostic Bench','short':'Count outcome','floor':'Diagnostics','symbol':'±1'},
 {'scene_index':3,'locus':'Trisomy 21 Case Window','short':'Case example','floor':'Case gallery','symbol':'21×3'},
]

BEAT_IMAGES={
 'U5-K-013':'the three-way compass keeping crossing over, independent orientation/assortment, and random fertilization in three physically separate directions that all increase possible allele combinations',
 'U5-K-059':'a blue chromosome carrying a short amber segment and an amber chromosome carrying the reciprocal blue segment after a crossover between nonsister chromatids',
 'U5-K-061':'two already-produced haploid gametes entering the fertilization dock from different chutes and fusing probabilistically only after meiosis is complete',
 'U5-K-011':'the scanner comparing correct homolog separation in meiosis I and correct sister-chromatid separation in meiosis II with a failed-segregation route',
 'U5-K-128':'a red failure gate where homologs fail to segregate in meiosis I or sister chromatids fail to segregate in meiosis II, producing gametes with abnormal chromosome numbers',
 'U5-K-129':'the count bench showing an otherwise normal complement with one particular chromosome present in an extra or missing copy rather than a whole extra or missing set',
 'U5-K-131':'a karyotype-style board arranging chromosome copies into corresponding groups so an abnormal count can be seen while the earlier meiotic event itself remains offstage',
 'U5-K-130':'the chromosome-21 case window changing from a normal paired reference to three copies of chromosome 21 while other displayed chromosome groups remain unchanged',
}

ZONE_COPY={
'U5-L16':[
 ('left','Crossover / recombinant route','X↔X','The same blue and amber homolog identities appear on the left with visible exchanged DNA segments. This lane represents crossing over that already occurred between nonsister chromatids during prophase I and the recombinant chromosomes produced by that exchange.'),
 ('center','Three-source diversity compass','3↗','A three-direction floor compass compares crossing over, independent orientation/assortment during meiosis, and random fertilization without merging them into one vague “gene mixing” event.'),
 ('right','Random-fertilization dock','n+n','Two completed haploid gametes arrive from separate chutes and may fuse. The dock is visibly downstream of meiosis so fertilization cannot be mistaken for a meiotic event.')],
'U5-L17':[
 ('left','Correct segregation lane','✓','A reference chromosome set repeats the correct mechanics from Journey 2: homologous chromosomes segregate in meiosis I and sister chromatids segregate in meiosis II.'),
 ('center','Segregation-integrity checkpoint','SCAN','The chromosome-outcome scanner is now locked in red segregation-integrity mode and asks one question only: did the chromosome partners that were supposed to separate actually segregate to opposite products?'),
 ('right','Nondisjunction failure route','✕','A branching failure chute shows either homologous chromosomes failing to separate in meiosis I or sister chromatids failing to separate in meiosis II. The failure is kept separate from the later chromosome-count diagnosis.')],
'U5-L18':[
 ('left','Normal chromosome complement','2 copies','A simplified karyotype reference keeps the expected copy number for each displayed chromosome visible on the left so the diagnostic comparison always has a normal count baseline.'),
 ('center','Aneuploid count bench','+1 / −1','The center bench changes the copy number of one particular chromosome while leaving the rest of the displayed complement unchanged, distinguishing extra or missing individual chromosomes from whole-set ploidy changes.'),
 ('right','Karyotype evidence wall','pairs by type','A conventional karyotype-style display organizes chromosome copies so the resulting abnormal chromosome complement can be observed. It shows the outcome, not a replay of the earlier nondisjunction event.')],
'U5-L19':[
 ('left','Paired chromosome-21 reference','21 21','Two copies of chromosome 21 are fixed on the learner’s left as the normal comparison state. They stay visible while the center adds one extra chromosome 21, so the change from two copies to three can be reconstructed without shifting the reference.'),
 ('center','Three-copy chromosome-21 display','21 21 21','A third chromosome 21 is added in the center while the other displayed chromosome groups retain their ordinary copy numbers, making trisomy a count-level condition rather than a vague “different chromosome” label.'),
 ('right','Case interpretation panel','case ≠ definition','The right panel connects trisomy 21 with aneuploidy and possible nondisjunction origins while explicitly keeping this named human case separate from the general definitions of nondisjunction and aneuploidy.')],
}

NARR={
'U5-L16':{
 'title':'The Scanner That Called Every Difference an Error',
 'kicker':'Three normal processes can create new allele combinations, and none of them is a chromosome-count mistake.',
 'paragraphs':[
  "The four haploid products from the Meiosis Transit Hall roll through a short tunnel and enter the **Variation Sources Compass**, the first room of the Diversity and Chromosome Error Center. The room is triangular enough to redraw from memory. On your **left**, a glass lane carries the same blue and amber chromosomes you followed through meiosis, including chromatids whose colored segments show where crossing over occurred. Directly **ahead**, a bronze three-point compass is set into the floor beneath a black-and-glass chromosome-outcome scanner. On your **right**, two separate gamete chutes descend toward a round fertilization dock. Imani places the gold ledger beside the scanner and turns its dial to violet **DIVERSITY MODE**. A warning above the exit explains the center’s problem. NORMAL VARIATION and SEGREGATION ERROR have been dumped into one bin marked DIFFERENT. Nothing can leave until those categories are separated.",
  "Imani starts at the left lane because the chromosome itself already carries evidence of one diversity-producing mechanism. One large blue chromosome contains a short amber segment, and its amber homolog carries the reciprocal blue segment. Those segments were exchanged earlier between **nonsister chromatids of homologous chromosomes** during prophase I. The chromosome now contains a DNA-segment combination that differs from either original homolog. Imani slides it through the scanner and names the structure only after you can see the changed segment pattern. It is a **recombinant chromosome**. The word recombinant belongs to the altered combination of DNA segments produced through crossing over; it does not mean that chromosome number is abnormal.",
  "She then rotates the center compass to its second point. A small model of two homologous chromosome pairs appears exactly as it did at metaphase I. The large pair can face one pole in either parental-origin orientation, and the smaller pair can orient independently of that choice. When the model runs forward, different haploid products receive different combinations of the blue- and amber-origin homologs. Imani keeps the term on the mechanism. Independent orientation, often discussed as part of **independent assortment**, changes which homolog combinations enter gametes. No DNA segment has to cross over for this source of diversity to operate. The scanner reads a new allele combination while its chromosome-count light remains normal.",
  "Only after those meiotic events are complete does Imani open the right-side chutes. Two already-produced haploid gametes descend from separate paths into the dock. The dock does not know which compatible gametes will meet; which gametes fuse is probabilistic. When one pair enters the fusion ring, their allele combinations are brought together in a new diploid zygote. Imani names this third source **random fertilization**. She draws a thick line on the ledger between MEIOSIS and FERTILIZATION so the timing cannot blur. Crossing over and independent orientation occur during meiosis. Random fertilization happens afterward, when gametes fuse.",
  "The compass now holds three arrows that stay physically separate even though they converge on one outcome category. Imani labels the whole panel **Sources of variation in sexual reproduction**. The left arrow is crossing over, which can create recombinant chromosomes. The forward arrow is independent orientation/assortment of homologous pairs during meiosis. The right arrow is random fertilization. Together, these processes can greatly increase the number of possible genetic combinations among offspring. The center does not promise a fixed amount of variation from any one reproductive event, and it does not collapse the three mechanisms into the vague phrase “mixing genes.” You should be able to point to where each process occurs and what it physically changes.",
  "Imani closes the first ledger column with three entries. CROSSOVER → recombinant DNA segment combinations. INDEPENDENT ORIENTATION → different homolog combinations in gametes. RANDOM FERTILIZATION → different combinations of gametes in a zygote. Then she turns the scanner toward you for the optional recall. The actual chromosomes and compass remain visible for a moment, but the term labels dim. If you can reconstruct all three mechanisms from their locations, the diversity side of the center is calibrated.",
  "The exit does not open immediately. Instead, the scanner gives a sharp red tone and flips its own dial from violet DIVERSITY MODE to red **SEGREGATION-INTEGRITY MODE**. The recombinant chromosome remains perfectly acceptable. What the scanner wants to know next is different. During meiosis, did the chromosome partners that were supposed to separate actually go to opposite products? Imani carries the same chromosome-outcome cards through the red gate. The next room will inspect chromosome movement, not allele-combination diversity."
 ],
 'close':'Crossing over, independent orientation/assortment, and random fertilization are now separated as normal sources of genetic diversity. The scanner switches modes before any segregation error is introduced.'
},
'U5-L17':{
 'title':'The Gate Where Separation Either Happens or Fails',
 'kicker':'Nondisjunction is a movement failure during chromosome segregation; the abnormal chromosome count comes afterward.',
 'paragraphs':[
  "You enter the **Segregation Integrity Gate** through a red-lit doorway, and the room immediately divides into three lanes. On your **left**, a correct-segregation track reuses the same blue and amber chromosome geometry from the meiosis hall. Directly **ahead**, the chromosome-outcome scanner sits inside a metal checkpoint arch, now locked in red SEGREGATION-INTEGRITY MODE. On your **right**, a failure chute splits into two branches labeled DIVISION I and DIVISION II. The gold ledger is open to two different columns labeled EVENT and RESULT. Imani places a finger between them. “We are going to keep the thing that goes wrong separate from the chromosome-number state that may result.”",
  "The left lane runs first as the reference. A duplicated blue homolog and its duplicated amber homolog align as a pair, then move to opposite sides during meiosis I while each chromosome keeps its sister chromatids joined. The scanner stamps the event CORRECT HOMOLOG SEGREGATION. A second panel then runs meiosis II. One duplicated chromosome aligns, its sister connection releases, and the sister chromatids move to opposite poles. The scanner stamps CORRECT SISTER-CHROMATID SEGREGATION. Imani names the full reference relationship **Correct chromosome segregation and nondisjunction** because the room is built around that contrast. Correct homolog separation in meiosis I and correct sister-chromatid separation in meiosis II normally distribute one chromosome from each homologous pair into each haploid product.",
  "Now the right-side DIVISION I branch activates. The blue and amber homologs approach the first-division separation gate, but the gate on one side fails to release. Both homologs travel toward the same product while another product receives neither member of that homologous pair. Imani freezes the movement at the moment of failure. She names the event **nondisjunction**. Homologous chromosomes in meiosis I have failed to segregate normally. She does not name the chromosome-count outcome yet. The scanner writes only EVENT = NONDISJUNCTION and leaves the RESULT column blank.",
  "The branch resets and the DIVISION II route lights. This time meiosis I proceeds normally, so the homologous chromosomes are already in different cells. In one meiosis-II cell, however, the sister chromatids of a duplicated chromosome fail to separate. Both sisters move into one product while another product from that division receives no copy of that chromosome. Imani again stops the model at the failed movement. This is also **nondisjunction**, but the partners that failed to segregate are sister chromatids in meiosis II, not homologous chromosomes in meiosis I. The shared scientific idea is failure of the chromosome structures that should separate at that division.",
  "The difference between the two error routes is visually important. A meiosis-I nondisjunction error can affect all gametes produced from that meiotic event for the chromosome being tracked, because the homologs were misdistributed at the first division. A meiosis-II error occurs after homologs have separated correctly, so the pattern of resulting gametes differs. Imani does not turn these pattern differences into a memorized table here; the permanent lesson is more basic and more transferable. Identify what should separate at the division, observe whether it segregates normally, and call the failure **nondisjunction** when it does not.",
  "The scanner now ejects four chromosome-outcome cards onto the floor. Some cards show an ordinary haploid count for the tracked chromosome. Others show an extra copy or a missing copy. Imani refuses to let the red NONDISJUNCTION stamp spread onto those count cards. “Nondisjunction is the segregation failure,” she says, tapping the EVENT column. “The chromosome-number condition belongs in RESULT.” That distinction keeps cause and consequence in separate physical places, exactly as the center was designed to do.",
  "A conveyor under the right chute begins carrying the abnormal-count cards into the next room. The scanner follows, still in red mode, but the movement animation disappears. Ahead, a counting bench and an organized chromosome display are waiting. The question has changed again. Now that a segregation error has produced an unusual chromosome count, what is the chromosome-number state called, and what evidence can a karyotype actually show?"
 ],
 'close':'Nondisjunction has been fixed to the failed segregation event itself. The resulting chromosome-count cards now move to a separate diagnostic bench, where the outcome will receive its own name.'
},
'U5-L18':{
 'title':'The Count Bench With One Chromosome Too Many',
 'kicker':'Aneuploidy changes the copy number of particular chromosomes, and a karyotype can show that resulting state without replaying the meiotic error that produced it.',
 'paragraphs':[
  "The conveyor stops inside the **Aneuploidy Diagnostic Bench**, a bright rectangular laboratory with three fixed displays. On your **left**, a normal chromosome-complement reference is arranged in corresponding groups, with the expected copy number visible for every simplified chromosome type. Directly **ahead**, the black diagnostic bench holds movable chromosome tiles under a large +1 / −1 counter. On your **right**, a wall-sized karyotype-style display is empty, waiting for the final chromosome complement to be organized. Imani places the red-stamped nondisjunction event card behind the bench rather than on it. The cause has already happened. This room diagnoses the resulting chromosome-number state.",
  "She begins with the normal reference on the left and duplicates it at the center bench. Then she adds one additional copy of a single chromosome type while leaving the copy number of the other chromosome types unchanged. The counter flashes +1. She resets the bench and removes one copy of a particular chromosome instead; the counter flashes −1. In both cases the abnormality concerns one or more **individual chromosomes**, not a complete extra or missing set. Imani names the category **aneuploidy**. Aneuploidy is an abnormal chromosome-number condition involving extra or missing particular chromosomes rather than whole additional or missing chromosome sets.",
  "The gold ledger now makes a distinction you already encountered at the Ploidy Counter in Journey 1. Ploidy describes the number of complete chromosome sets. Aneuploidy describes an imbalance in the copy number of particular chromosomes. If one chromosome type appears in three copies while the rest retain their usual copy numbers, that is not simply “3n.” If one copy of a chromosome is missing, the cell has not automatically lost an entire chromosome set. The center +1 / −1 counter is deliberately narrow because it is teaching a different counting question from the earlier n versus 2n gauge.",
  "Imani transfers the +1 outcome to the right wall. The chromosomes are grouped by corresponding type in a **karyotype**-style display, allowing the unusual copy number to be seen. She labels the larger relationship **Karyotype and chromosome-number abnormalities**. A karyotype analysis can reveal some chromosome-number abnormalities, including a trisomic pattern in which a particular chromosome is present in three copies. What the wall cannot show directly is the historical moment during meiosis when the homologs or sister chromatids failed to segregate. The karyotype shows the resulting chromosome complement; the earlier nondisjunction event was a movement in a different room and time.",
  "To make that limit memorable, Imani tries to drag the red nondisjunction animation onto the karyotype wall. The wall rejects it and displays only the final chromosome copies. She can infer that nondisjunction is one possible mechanism that produced certain aneuploid outcomes, but the static organized chromosome display does not replay that event. This protects two distinctions at once. Nondisjunction versus aneuploidy, and a present chromosome-count observation versus the causal history that generated it.",
  "The chromosome-outcome scanner dims every label except the central +1 / −1 counter for the second optional recall. The left reference still shows normal copy numbers; the center shows one particular chromosome in an extra or missing copy; the right organizes the resulting complement. If you can name the abnormal chromosome-number category from that geometry, you have identified the result without confusing it with the segregation failure.",
  "When the labels return, one specific +1 card is highlighted. It shows chromosome 21 in three copies. Imani does not use that card to redefine the general concept you just learned. She carries it through a narrow door marked CASE WINDOW. The general diagnosis remains **aneuploidy**; the next room will examine one named human example and keep its scope deliberately limited."
 ],
 'close':'Aneuploidy is now fixed to an abnormal copy number of particular chromosomes, and the karyotype is fixed to evidence of the resulting complement. One highlighted chromosome-21 case moves forward as an example, not a definition.'
},
'U5-L19':{
 'title':'Three Copies at the Chromosome-21 Window',
 'kicker':'Trisomy 21 is one specific aneuploid chromosome-count pattern, not a substitute for the broader concepts of nondisjunction or aneuploidy.',
 'paragraphs':[
  "The final door opens into the **Trisomy 21 Case Window**, a quiet clinical-style gallery designed to prevent the example from swallowing the rule. On your **left**, two chromosome-21 tiles sit side by side as a paired reference. Directly **ahead**, the case window contains a larger chromosome display with space for an additional copy of chromosome 21. On your **right**, a restrained interpretation panel has three headings labeled CHROMOSOME STATE, POSSIBLE ORIGIN, and CASE SCOPE. The chromosome-outcome scanner parks beneath the center window, and the gold ledger keeps its EVENT and RESULT columns visible from the previous rooms.",
  "Imani begins with the left reference and points to the two chromosome-21 copies. She then takes the highlighted +1 card from the diagnostic bench and adds a third chromosome 21 at the center. The other displayed chromosome groups keep their usual copy numbers. The defining structural fact is now visible before she names it. **Trisomy 21** means three copies of chromosome 21. On the ledger, RESULT reads ANEUPLOIDY → THREE COPIES OF CHROMOSOME 21. The general category remains aneuploidy because one particular chromosome is present in an extra copy rather than an entire extra chromosome set.",
  "Only after the count is clear does Imani fill in the POSSIBLE ORIGIN field. **Nondisjunction** during meiosis can produce a gamete with an abnormal chromosome number; after fertilization, that can contribute to a zygote with three copies of chromosome 21. She deliberately writes CAN RESULT FROM rather than IS. Nondisjunction is still the failed segregation event. Trisomy 21 is a resulting chromosome-count state. The same causal chain you built across the previous rooms now reads from movement failure to abnormal count to one specific case example.",
  "The right interpretation panel then names the full learning target **Trisomy 21 example**. Trisomy 21 is the most common chromosomal cause of **Down syndrome**. Imani keeps that sentence next to the chromosome-count display and nowhere else. The case window is not used to claim that every phenotypic feature of a person can be read directly from a simple karyotype, and it does not turn Down syndrome into the definition of aneuploidy. A karyotype can show the three-copy chromosome-21 pattern; biological development and phenotype involve consequences beyond what this one static chromosome picture alone displays.",
  "Imani steps back and reopens the four-room route on her tablet. At the first compass, normal genetic diversity arose through crossing over, independent orientation/assortment, and random fertilization. At the second gate, nondisjunction was a failure of homologous chromosomes or sister chromatids to segregate normally. At the third bench, aneuploidy was the resulting abnormal number of particular chromosomes, and a karyotype could reveal that chromosome complement without directly showing the earlier meiotic error. Here, trisomy 21 is one concrete aneuploid chromosome-count pattern involving chromosome 21.",
  "The chromosome-outcome scanner now shows both modes side by side. Violet DIVERSITY MODE contains recombinant segments and normal chromosome counts. Red SEGREGATION-INTEGRITY MODE contains the movement failure and its count-level consequences. The center finally stops filing every unusual outcome under one word. A recombinant chromosome can be genetically different while carrying the expected chromosome number. An aneuploid cell can have an abnormal chromosome count because segregation failed. Difference alone never tells you which mechanism occurred; the chromosome action and count evidence do.",
  "Imani closes the gold ledger with three causal lines that can be reconstructed without the room labels. NORMAL VARIATION → crossing over / independent orientation / random fertilization → new allele combinations. SEGREGATION ERROR → nondisjunction → abnormal chromosome-number products. CASE EXAMPLE → aneuploid chromosome complement → three copies of chromosome 21 in trisomy 21. The case-gallery lights fade, leaving the blue and amber chromosome identities on her tablet ready for the next inheritance route, where chromosome mechanics will give way to Mendelian allele tracking."
 ],
 'close':'The center can now distinguish normal diversity mechanisms from segregation failure, resulting aneuploidy, karyotype evidence, and the specific trisomy 21 example without letting any one term replace the others.'
},
}


def zones_for(b):
    rows=ZONE_COPY[b['locus_id']]
    return [{'position':p,'label':label,'symbol':symbol,'description':desc} for p,label,symbol,desc in rows]

def make_cast(b):
    cast=[GUIDE,SCANNER,LEDGER]
    for item in b['stable_cast']:
        cast.append({'name':item['name'],'kind':item['type'].lower(),'visual':item['visual_identity'],'job':item['job_in_scene']})
    return cast

def make_beats(b):
    return [{'object_id':t['knowledge_id'],'term':t['canonical_term'],'story':BEAT_IMAGES[t['knowledge_id']], 'science':t['canonical_science'],'exact_name':bool(t['exact_name_recall']),'hint':BEAT_IMAGES[t['knowledge_id']],'name_support':t['name_support']} for t in b['term_introductions']]

def make_snapshot(b):
    return [{'term':t['canonical_term'],'meaning':t['canonical_science'],'image':BEAT_IMAGES[t['knowledge_id']]} for t in b['term_introductions']]

briefs=[B[f'U5-L{i:02d}'] for i in range(16,20)]
scenes=[]
for idx,b in enumerate(briefs):
    n=NARR[b['locus_id']]; q=b['quick_recall']; checkpoint=bool(q['enabled'])
    cp={'U5-L16':'U5-K-013','U5-L18':'U5-K-129'}.get(b['locus_id']) if checkpoint else None
    scenes.append({
      'scene_index':idx,'locus_id':b['locus_id'],'locus':b['scene_title'],'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['micro_anchor'],'scene_layout':{'orientation':b['orientation_sentence'],'zones':zones_for(b)},
      'cast':make_cast(b),'continuity_object':J3['continuity_object'],
      'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':make_beats(b),'memory_snapshot':make_snapshot(b),
      'misconception_guards':b['misconception_guards'],'exit_memory':b['exit_memory'],
      'checkpoint':checkpoint,'checkpoint_object_id':cp,'checkpoint_prompt':q.get('candidate_prompt','') if checkpoint else '',
      'checkpoint_answer':q.get('answer','') if checkpoint else '',
      'checkpoint_hint':('Return to the fixed three-source compass or chromosome-count bench and reconstruct what physically changed before naming the term.' if checkpoint else ''),
      'next_locus':briefs[idx+1]['scene_title'] if idx+1<len(briefs) else None,'causal_transition':b['causal_transition']['transition_logic'],
    })

journey={
 'palace_id':'U5-J3','unit_id':'unit-5','palace_name':'Diversity and Chromosome Error Center','story_title':'The Scanner That Confused Diversity With Error',
 'tagline':'Calibrate one chromosome-outcome scanner so it can separate normal allele-combination diversity from segregation failure, abnormal chromosome number, and a specific trisomy case.',
 'guide':GUIDE,
 'premise':'The Diversity and Chromosome Error Center has started classifying every unusual genetic outcome as the same kind of “variation.” Recombinant chromosomes with normal copy numbers, gametes created by ordinary assortment, and products of failed chromosome segregation are arriving on one conveyor. The center can work again only if each outcome is traced to the mechanism that produced it.',
 'mission':'Follow Dr. Imani Reyes through four diagnostic stations. First separate crossing over, independent orientation/assortment, and random fertilization as normal sources of genetic diversity. Then switch the chromosome-outcome scanner into segregation-integrity mode, distinguish correct segregation from nondisjunction, name aneuploidy as the resulting abnormal copy number of particular chromosomes, interpret what a karyotype can and cannot show, and finish with trisomy 21 as one specific human chromosome-number example.',
 'finale':'The center finally runs two different diagnostic modes instead of one vague “different” alarm. Normal diversity is reconstructed from crossing over, independent orientation/assortment, and random fertilization. Segregation failure is reconstructed as nondisjunction. Abnormal copy number of particular chromosomes is reconstructed as aneuploidy and can be visible in a karyotype. Trisomy 21 remains one specific aneuploid case involving three copies of chromosome 21 rather than a definition of the broader mechanisms.',
 'estimated_minutes':14,'scene_count':4,'checkpoint_count':2,'student_release':'DEVELOPER_PREVIEW_F4C',
 'learner_rule':'Follow the chromosome outcome from mechanism to evidence. A difference in allele combination and a difference in chromosome number are never treated as the same kind of event. Optional Quick Recall appears only twice.',
 'route_orientation':'This is one continuous four-location diagnostic center. Enter at the Variation Sources Compass in violet diversity mode, switch the same scanner to red segregation-integrity mode at the Segregation Integrity Gate, carry abnormal-count outcome cards to the Aneuploidy Diagnostic Bench, and finish at the Trisomy 21 Case Window. The scanner and ledger preserve cause versus outcome across the route.',
 'route':route,'scenes':scenes,'narrative_design':'U5-F4C-NARRATIVE-1.0'
}
(U5/'journeys').mkdir(exist_ok=True)
(U5/'journeys'/'U5-J3.json').write_text(json.dumps(journey,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
registry={
 'schema':'memory-palace-v2-unit5-f4c-journeys-1.0','unit_id':'unit-5','stage':'F4C','student_release':False,'preview_release':True,
 'journey_count':3,'scene_count':19,'checkpoint_count':7,
 'guided_journeys':[{k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']} for j in [J1,J2,journey]]
}
(U5/'journeys-f4c.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
status={
 'unit_id':'unit-5','unit_number':5,'title':'Heredity','status':'F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','pipeline_status':'POLISHED_NARRATIVE_J1_J2_J3_F4C',
 'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','student_release':False,'preview_release':True,
 'canonical_records':152,'review_flags_resolved':37,'teacher_ppt_slides':112,'ced_topics':5,'ced_atoms':34,'architecture_journeys':8,'architecture_loci':50,
 'scene_briefs':50,'preview_journeys':3,'preview_scenes':19,'preview_checkpoints':7,'journey_1_records':20,'journey_2_records':18,'journey_3_records':8,
 'next_gate':'F4D_JOURNEY4_ONLY_AFTER_F4C_PROSE_QA'
}
(U5/'status-f4c.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(U5/'status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
words=sum(len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs']))) for s in scenes)
manifest={'schema':'memory-palace-v2-unit5-f4c-release-manifest-1.0','unit_id':'unit-5','stage':'F4C','student_release':False,'preview_release':True,'journey_count':3,'scene_count':19,'checkpoint_count':7,'journey_3_records':8,'journey_3_narrative_words':words,'f1_canonical_records':152,'f2_permanent_loci':50,'f3_scene_briefs':50,'next_gate':'F4D'}
(U5/'f4c-release-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

course_path=ROOT/'content'/'ap-biology'/'course.json'; course=json.loads(course_path.read_text(encoding='utf-8'))
cu5=next(u for u in course['units'] if u['unit_id']=='unit-5')
cu5.update({'status':'F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','journey_count':3,'scene_count':19,'canonical_lock':'LOCKED_F1','source_status':'AUDITED_SCIENCE_LOCKED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVE_J1_F4A_J2_F4B_J3_F4C','canonical_records':152,'review_flags_resolved':37,'ced_atoms':34,'teacher_ppt_slides':112,'student_release':False,'preview_release':True,'pipeline_stage':'UNIT5_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW_F4C'})
course_path.write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lock_files=['journeys/U5-J3.json','journeys-f4c.json','status-f4c.json','f4c-release-manifest.json']
lock={'schema':'memory-palace-v2-unit5-content-lock-f4c-1.0','unit_id':'unit-5','stage':'F4C','lock_status':'LOCKED_F4C_J3','student_release':False,'preview_release':True,'files':{}}
for rel in lock_files:
 p=U5/rel; lock['files'][rel]={'bytes':p.stat().st_size,'sha256':sha(p)}
(U5/'content-lock-f4c.json').write_text(json.dumps(lock,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines=['# Unit 5 F4C · Journey 3 Narrative','',f'## {journey["story_title"]}','',journey['tagline'],'','**Palace:** Diversity and Chromosome Error Center  ','**Guide:** Dr. Imani Reyes  ','**Route:** '+' → '.join(x['locus'] for x in route),'']
for s in scenes:
 lines += [f"## {s['scene_index']+1}. {s['locus']} — {s['title']}",'',f"*{s['scene_kicker']}*",'']+s['story_paragraphs']+['']
(ROOT/'docs'/'UNIT5_F4C_JOURNEY3_STORY.md').write_text('\n'.join(lines),encoding='utf-8')
release=['# Unit 5 F4C Release','', 'Unit 5 F4C authors and locks Journey 3 only while preserving the F4A Journey 1 and F4B Journey 2 narratives. Unit 5 remains a developer preview and is not student released.','', '## Accounting','', '- Journeys 1–2 preserved: **15 scenes / 38 records / 5 optional recalls**', '- Journey 3 authored: **4 scenes / 8 records / 2 optional recalls**', f'- Journey 3 narrative words: **{words}**', '- Total Unit 5 preview: **3 journeys / 19 scenes / 7 optional recalls**','', '## Scientific continuity','', '- Crossing over, independent orientation/assortment, and random fertilization remain three distinct normal sources of genetic diversity.', '- Recombinant chromosomes are treated as altered allele/DNA-segment combinations, not chromosome-number errors.', '- The scanner changes from diversity mode to segregation-integrity mode before nondisjunction is introduced.', '- Nondisjunction remains the segregation failure; aneuploidy remains the resulting abnormal number of particular chromosomes.', '- Karyotype evidence shows the resulting chromosome complement rather than directly observing the earlier meiotic event.', '- Trisomy 21 remains one specific aneuploid chromosome-number example and never replaces the general definitions.','', '## Release boundary','', 'No Unit 5 Memory Objects, Review runtime, Challenge Lab runtime, or student-facing Unit 5 release is created in F4C. Journeys 4–8 remain at the F3 scene-brief stage.','']
(ROOT/'docs'/'UNIT5_F4C_RELEASE.md').write_text('\n'.join(release),encoding='utf-8')
print(json.dumps({'journey':'U5-J3','scenes':4,'records':8,'checkpoints':2,'narrative_words':words,'student_release':False,'preview_release':True},indent=2))
