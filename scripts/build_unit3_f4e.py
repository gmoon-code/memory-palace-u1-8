from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content'/'ap-biology'/'unit-3'
briefs=json.loads((U3/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
jbriefs=json.loads((U3/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
B={s['locus_id']:s for s in briefs if s['journey_id']=='U3-J5'}
J5=next(j for j in jbriefs if j['journey_id']=='U3-J5')

GUIDE={
 'name':'Dr. Nia Park',
 'role':'cellular-energetics investigator',
 'visual':'navy field jacket, clear safety glasses, and a compact tablet now showing a chloroplast stroma map, carbon tracer, ATP/NADPH inputs, and a net-carbon-gain gauge',
 'story_job':'Nia keeps the same carbon tracer visible, separates carbon acceptors from enzymes and products, keeps detailed Calvin-cycle bookkeeping subordinate to cycle logic, and compares photorespiration, C4, and CAM without collapsing their mechanisms.'
}

route=[
 {'scene_index':0,'locus':'Calvin Cycle Energy Dock','short':'Energy Dock','floor':'Stroma entrance','symbol':'ATP'},
 {'scene_index':1,'locus':'Carbon Fixation Bench','short':'Fixation Bench','floor':'Stroma workbench','symbol':'CO₂'},
 {'scene_index':2,'locus':'G3P Output and Regeneration Loop','short':'G3P Loop','floor':'Carbon loop','symbol':'G3P'},
 {'scene_index':3,'locus':'Photorespiration Detour','short':'Detour','floor':'Rubisco junction','symbol':'O₂'},
 {'scene_index':4,'locus':'C4 and CAM Strategy Conservatory','short':'C4 / CAM','floor':'Adaptation conservatory','symbol':'C₄'},
]

ZONE_COPY={
'U3-L34':[
 ('left','ATP and NADPH delivery gate','ATP/NADPH','The same ATP and NADPH produced at the end of the light reactions arrive from the left-side stroma gate and remain chemically separate from the incoming carbon tracer.'),
 ('center','Calvin-cycle stroma route','cycle','A broad circular pathway model occupies the center of the chloroplast stroma, showing carbon entering, being processed, and the carbon acceptor being regenerated.'),
 ('right','Carbohydrate-building exit','organic C','A fixed right-side output bay receives reduced organic carbon that can later contribute to glucose and other biological molecules rather than depicting glucose as the direct product of one cycle turn.')],
'U3-L35':[
 ('left','Carbon-dioxide inlet','CO₂','A single carbon tracer enters from the left as an inorganic carbon atom inside a conventional carbon-dioxide molecule and stays visibly marked throughout fixation.'),
 ('center','Rubisco fixation station','rubisco','The central enzyme station brings carbon dioxide together with the carbon acceptor while keeping the enzyme visually separate from both reactants.'),
 ('right','RuBP carbon-acceptor rack','RuBP','A fixed right rack holds regenerated ribulose bisphosphate molecules ready to accept incoming carbon dioxide at the start of another cycle turn.')],
'U3-L36':[
 ('left','G3P output gate','G3P','A left-side gate receives the three-carbon sugar product that can leave the cycle and contribute carbon to glucose and other organic molecules.'),
 ('center','ATP/NADPH accounting loop','3 CO₂','The center loop shows repeated carbon processing powered by ATP and NADPH, with the detailed three-CO₂ accounting displayed as a small bookkeeping layer rather than the main spatial route.'),
 ('right','RuBP regeneration return','RuBP↻','A right-side return track uses part of the processed carbon and energy input to regenerate the RuBP acceptor so the pathway can continue cycling.')],
'U3-L37':[
 ('left','CO₂ fixation route','CO₂','The normal left path delivers carbon dioxide to rubisco and sends successful fixation back toward net organic-carbon gain.'),
 ('center','Rubisco branch point','rubisco','The same central rubisco enzyme can encounter either carbon dioxide or oxygen, turning environmental conditions into a visible branch in carbon-processing outcome.'),
 ('right','O₂ photorespiration detour','O₂','The right-side oxygen route diverts rubisco into photorespiration, consumes energy, and lowers net carbon fixation without being confused with mitochondrial cellular respiration.')],
'U3-L38':[
 ('left','C4 spatial-separation greenhouse','space','A left greenhouse separates initial carbon fixation in mesophyll cells from Calvin-cycle processing in bundle-sheath cells, creating a spatial CO₂-concentrating strategy.'),
 ('center','Hot/dry photorespiration-pressure chamber','heat','The center chamber lowers internal CO₂ availability relative to oxygen as stomatal water-conservation pressure increases, making the rubisco problem from the previous scene visible.'),
 ('right','CAM temporal-separation greenhouse','time','A right greenhouse opens stomata mainly at night, stores fixed carbon in organic acids, and releases carbon dioxide during the day so separation occurs across time rather than cell type.')],
}

CAST={
'U3-L34':[
 ('ATP delivery','energy input','a blue ATP token arriving from the photophosphorylation turbine through the same stroma-side door used in Journey 4','supplies usable chemical energy for carbon-reduction and regeneration work in the Calvin cycle'),
 ('NADPH delivery','reducing-power input','a purple NADPH carrier arriving beside ATP but never merging with it','provides reducing power used in the carbon-fixation pathway'),
 ('carbon tracer','continuity marker','one carbon atom glowing amber inside an incoming CO₂ molecule at the edge of the stroma model','lets the learner follow carbon identity from inorganic CO₂ into fixed organic carbon without pretending energy becomes carbon')],
'U3-L35':[
 ('carbon dioxide','inorganic carbon input','a conventional linear CO₂ molecule whose carbon atom glows amber','provides the inorganic carbon that is incorporated into an organic molecule during fixation'),
 ('rubisco','enzyme','a large enzyme-shaped docking surface fixed at the center bench','catalyzes the initial CO₂-fixation reaction and can also react with oxygen under competing conditions'),
 ('RuBP','carbon acceptor','a five-carbon acceptor model held on the right rack and returned after regeneration','accepts carbon dioxide at the beginning of the Calvin cycle and must be regenerated for the cycle to continue')],
'U3-L36':[
 ('G3P','three-carbon sugar output','a three-carbon organic-carbon card emerging from the left output gate','can leave the Calvin cycle and supply carbon for glucose and other organic molecules'),
 ('RuBP return','regenerated acceptor','a restored RuBP model completing the right-side return track','allows the cyclic pathway to accept new carbon dioxide again'),
 ('bookkeeping ring','cycle accounting model','a small illuminated ring showing three CO₂, nine ATP, six NADPH, one net G3P, and five G3P equivalents routed toward RuBP regeneration','shows the three-CO₂ accounting without turning every intermediate and molecule count into the primary memory route')],
'U3-L37':[
 ('rubisco','branch-point enzyme','the same enzyme model from the fixation bench, now positioned between a CO₂ lane and an O₂ lane','can catalyze CO₂ fixation or react with O₂, producing different consequences for net carbon gain'),
 ('oxygen','competing molecule','an O₂ molecule entering the right side when internal CO₂ is low relative to oxygen','competes at rubisco and sends carbon processing into the photorespiratory detour'),
 ('net-carbon-gain gauge','consequence display','a green carbon-gain meter that rises on the CO₂ path and drops when the O₂ detour is used','makes the cost of photorespiration visible as lower net carbon fixation')],
'U3-L38':[
 ('C4 leaf model','spatial strategy','a leaf cross-section with mesophyll cells on the outside and bundle-sheath cells surrounding vascular tissue deeper inside','separates initial CO₂ fixation from Calvin-cycle processing across different cell locations and concentrates CO₂ around rubisco'),
 ('CAM leaf model','temporal strategy','a succulent-like leaf chamber with a night clock, organic-acid storage tank, and daylight CO₂-release valve','separates initial carbon fixation from Calvin-cycle use across night and day while reducing water loss'),
 ('photorespiration-pressure gauge','shared environmental challenge','a central hot/dry chamber showing stomatal water-loss pressure and a falling internal CO₂-to-O₂ balance','provides the same challenge against which the C4 spatial and CAM temporal solutions can be compared')],
}

NARR={
'U3-L34':{
 'title':'The Two Packages Waiting in the Stroma',
 'kicker':'ATP and NADPH have arrived from the light reactions, but neither package becomes carbohydrate until carbon dioxide enters a separate stroma pathway.',
 'paragraphs':[
  "The door that opened beside the photophosphorylation turbine does not lead outside the chloroplast. You and Dr. Nia Park step through it onto a broad platform in the **stroma**, the fluid region surrounding the thylakoids. The route behind you is still visible through glass: ATP formed on the stroma side of ATP synthase, and NADPH left the photosystem I station through a separate carrier line. Now those two products roll into the greenhouse on your **left**. Directly **ahead**, a circular carbon-processing route is dark. On your **right**, an organic-carbon output gate is empty. Nia fixes all three positions on her tablet. ‘The light reactions solved the energy problem,’ she says. ‘They did not manufacture carbon out of ATP or NADPH. We still need carbon dioxide.’",
  "A blue ATP token and a purple NADPH carrier enter the left delivery gate. Nia calls their relationship to the next process the **Calvin-cycle energy input**: ATP and NADPH generated by the light reactions power carbohydrate production from carbon dioxide in the chloroplast stroma. She separates their jobs visually. ATP feeds energy-requiring steps. NADPH supplies reducing power. Neither token contains the carbon that will become carbohydrate. Above the center route, an amber lamp remains off until an actual CO₂ molecule arrives. The distinction keeps the handoff from Journey 4 honest: light energy has been converted into chemical forms that can support carbon processing, while carbon itself must come from inorganic CO₂.",
  "The central route begins turning only after Nia opens the CO₂ valve. Carbon enters the pathway, ATP and NADPH are used during carbon reduction and regeneration work, and an organic-carbon indicator appears at the right exit. The route loops back toward its starting acceptor instead of running as a one-way assembly belt. Nia finally names the whole pathway: the **Calvin cycle** is a cyclic carbon-fixation pathway in the chloroplast stroma that uses ATP and NADPH to incorporate CO₂ into carbohydrate. The word *cycle* now belongs to the visible return path in front of you, not to electron flow on the thylakoid membrane. Nia points back through the glass toward the light reactions so the two processes remain physically distinct.",
  "The right-side output gate begins to glow, but Nia blocks it before a full glucose model can appear. ‘Do not turn one cycle pass into “CO₂ goes in and glucose pops out,”’ she says. The greenhouse will eventually use fixed carbon to build carbohydrates, but we are going to follow one marked carbon first. She activates a single amber carbon tracer inside an incoming CO₂ molecule and sends it along a narrow rail toward the next bench. The ATP and NADPH lines remain behind at the energy dock, feeding the cycle as needed. The question pulling you forward is now precise: **what physically captures that inorganic carbon and gets it into the cycle?**"
 ],
 'close':'The amber carbon tracer leaves the energy dock still inside CO₂ and follows a floor rail to the Carbon Fixation Bench, where a carbon acceptor and an enzyme wait in different positions.'
},
'U3-L35':{
 'title':'The Enzyme, the Acceptor, and the Carbon They Must Not Be Confused With',
 'kicker':'Carbon fixation becomes clear only when rubisco, RuBP, and CO₂ stay visibly separate and each performs a different job.',
 'paragraphs':[
  "The floor rail carries the glowing CO₂ molecule into the **Carbon Fixation Bench**. The room is deliberately sparse. On your **left**, the CO₂ inlet holds the amber carbon tracer. Directly **ahead**, one large enzyme docking surface is labeled only after Nia stops it from moving. On your **right**, a rack holds identical five-carbon acceptor models ready to enter the center station. Nia makes you point to all three before the reaction begins. ‘Carbon dioxide is the incoming carbon. The center structure is the catalyst. The right-hand molecule is the acceptor. If those roles blur, the rest of the cycle becomes impossible to reconstruct.’",
  "Nia releases one right-side molecule toward the center and names it **RuBP**, short for ribulose bisphosphate. RuBP is the CO₂-acceptor molecule regenerated in the Calvin cycle. The phrase *carbon acceptor* is attached to the molecule on the right, not to the enzyme in the middle. Then the central docking surface opens around RuBP and the incoming CO₂. That enzyme is **rubisco**. Rubisco catalyzes the initial CO₂-fixation reaction of the Calvin cycle. It speeds the reaction by bringing the relevant reactants into the appropriate catalytic environment, but rubisco is not itself the carbon acceptor and it is not consumed as the carbon product.",
  "The amber carbon tracer leaves the CO₂ inlet and becomes incorporated into an organic carbon framework at the center station. Nia freezes the moment and names the event **carbon fixation**: incorporation of inorganic CO₂ into an organic molecule; in the Calvin cycle, CO₂ is added to a carbon acceptor. You can now rebuild the relationship from the geography alone. Left gives CO₂. Right gives RuBP. Center gives rubisco. The enzyme catalyzes the step in which inorganic carbon becomes part of an organic molecule. Nia does not clutter the bench with a parade of every short-lived intermediate because the defining event is already visible.",
  "Before the bench resets, Nia rotates the rubisco model and reveals a second socket marked O₂. She does not activate it yet. ‘Remember this,’ she says. ‘The same enzyme that catalyzes CO₂ fixation can also react with oxygen.’ For now, the carbon tracer has successfully entered the cycle, and the RuBP rack must eventually be replenished if another CO₂ molecule is to be accepted. The fixed-carbon track therefore carries your amber tracer toward a circular accounting room. A green gate on the left is labeled G3P OUTPUT; a return track on the right is labeled RuBP REGENERATION."
 ],
 'close':'The fixed carbon leaves the rubisco bench inside the cycle, pulling you toward the G3P Output and Regeneration Loop where carbon must be divided between net output and rebuilding the acceptor.'
},
'U3-L36':{
 'title':'The Carbon That Leaves and the Carbon That Must Stay',
 'kicker':'The cycle succeeds only if some processed carbon can leave as G3P while enough material and energy are used to regenerate RuBP.',
 'paragraphs':[
  "The next room is circular enough that you can see its beginning and end at the same time. On your **left**, a small output gate is sized for a three-carbon molecule. In the **center**, ATP and NADPH indicators flash around a repeated carbon-processing loop. On your **right**, a return track reconstructs the RuBP acceptor and sends it back toward the fixation bench. Your amber carbon tracer moves with the processed organic carbon instead of jumping straight into a glucose cube. Nia keeps one hand on the right return rail. ‘A cycle cannot keep fixing carbon if it uses up its acceptor and never rebuilds it.’",
  "A three-carbon sugar reaches the left output gate. Nia names it **G3P**, glyceraldehyde 3-phosphate. G3P is a three-carbon sugar produced by the Calvin cycle and can be used to synthesize glucose and other organic molecules. One G3P model exits toward the carbohydrate-building side of the greenhouse while other processed carbon remains within the loop. That image gives G3P the correct place in the story: it is a product that can contribute carbon to larger organic molecules, not a synonym for glucose and not the RuBP acceptor that begins fixation.",
  "The center floor then projects a small accounting ring around the larger pathway. Nia labels it **detailed Calvin-cycle stoichiometry**, but she deliberately shrinks the numbers so they cannot replace the mechanism. In the three-CO₂ accounting model used here, three cycle turns consume **9 ATP and 6 NADPH**, produce **one net G3P**, and route five additional G3P equivalents toward regeneration of **three RuBP** molecules. Nia traces the pattern once, then dims the numbers. ‘Keep the logic larger than the bookkeeping: ATP and NADPH are used, carbon is fixed and reduced, some carbon can leave as G3P, and RuBP must be regenerated.’ The greenhouse does not ask you to memorize a procession of every Calvin-cycle intermediate to understand that core architecture.",
  "The right-side regeneration track completes its work. Three restored RuBP models roll back toward the Carbon Fixation Bench, closing the loop you first saw at the energy dock. At the same moment, your marked G3P exits left and enters a transparent organic-carbon crate. The net-carbon-gain gauge rises. Then the greenhouse climate control abruptly shifts. Hot air dries the leaves in the adjacent chamber. Stomatal openings narrow to reduce water loss, the internal CO₂ indicator begins falling relative to O₂, and an alarm flashes over the rubisco station. Nia looks back at the second socket she showed you earlier. ‘Now we find out what happens when rubisco meets the wrong competitor.’"
 ],
 'close':'With G3P output understood and RuBP regenerated, the climate shift creates a new failure: falling internal CO₂ makes the oxygen route at rubisco impossible to ignore.'
},
'U3-L37':{
 'title':'The Oxygen Door at the Rubisco Junction',
 'kicker':'Photorespiration is not ordinary cellular respiration; it is the costly consequence of rubisco reacting with O₂ instead of CO₂.',
 'paragraphs':[
  "You enter a junction built around the same rubisco model from the fixation bench. Its position has not changed. The **left** lane still delivers CO₂ toward successful fixation. The enzyme sits directly **ahead**. A newly illuminated **right** lane delivers O₂ into the alternate socket. Above all three lanes, a net-carbon-gain gauge shows the consequence of each route. Nia turns the climate dial to the hot, dry condition that began in the previous room. Stomata restrict gas exchange to conserve water, internal CO₂ availability can fall, and the relative opportunity for oxygen at rubisco increases. The left CO₂ lane slows while the right oxygen lane brightens.",
  "An O₂ molecule reaches rubisco. Instead of the normal carbon-fixation path, the system diverts into the right-hand detour. Nia names the process **photorespiration**. Photorespiration occurs when rubisco reacts with O₂ instead of CO₂, consuming energy and lowering net carbon fixation; it is favored when internal CO₂ is low relative to O₂. The carbon-gain gauge drops immediately. This detour does not represent the mitochondrial process of cellular respiration that will appear later in Unit 3. The shared word *respiration* is not permission to merge the mechanisms. Here the defining event is oxygenation by rubisco and the resulting loss of carbon-fixation efficiency.",
  "Nia restores CO₂ to the left lane and the fixation route recovers. Then she lowers CO₂ again and the O₂ detour reappears. The comparison makes the evolutionary question visible without turning one interpretation into settled fact. One hypothesis treats photorespiration as an **evolutionary legacy** from conditions in which rubisco evolved under lower atmospheric O₂ and higher CO₂ than many plants face now. Nia places that hypothesis on an old-atmosphere panel rather than engraving it on the enzyme itself. Beside it she adds a second caution: evidence also suggests that photorespiratory metabolism can have protective roles when Calvin-cycle carbon processing is limited. The process can therefore carry costs for net carbon fixation without being described as a purposeless molecular error in every context.",
  "The greenhouse alarm is not solved by wishing rubisco had perfect specificity. Nia points through the glass at two experimental leaf chambers built to face the same hot, dry pressure. ‘Plants have evolved different ways to raise CO₂ availability around rubisco or reduce the water cost of acquiring it.’ The left chamber contains two spatially distinct cell regions. The right chamber contains one tissue whose behavior changes between night and day. Your amber carbon tracer divides into two duplicate demonstration tracers so you can compare the strategies without pretending the same molecule follows both routes at once."
 ],
 'close':'The rubisco junction has revealed the failure condition. You carry that exact pressure—low internal CO₂ relative to O₂ under hot, dry conditions—into a split conservatory that tests two different solutions.'
},
'U3-L38':{
 'title':'Two Ways to Keep Carbon Near Rubisco',
 'kicker':'C4 and CAM both reduce photorespiration, but one separates carbon handling across space and the other separates it across time.',
 'paragraphs':[
  "The final chamber is split cleanly in two around a shared **center** climate column. The column reproduces the same hot, dry pressure that triggered photorespiration: water-loss risk rises, stomatal opening becomes costly, and the CO₂-to-O₂ balance around rubisco can become unfavorable. On your **left**, a leaf cross-section contains two distinct cell regions connected by a carbon shuttle. On your **right**, a single leaf chamber is paired with a clock that flips from moon to sun. Nia keeps the central pressure constant. ‘Same problem,’ she says. ‘Different architecture. Watch whether the separation is in place or in time.’",
  "The left display activates first. CO₂ enters a **mesophyll cell** and is initially fixed into a **four-carbon compound**. That carbon is then delivered inward toward **bundle-sheath cells**, where concentrated CO₂ is made available for the Calvin cycle. Nia names the strategy **C4 photosynthesis**. C4 plants initially fix CO₂ into four-carbon compounds in mesophyll cells and deliver concentrated CO₂ to bundle-sheath cells, reducing photorespiration through **spatial separation**. She draws one bracket around the mesophyll zone and another around the bundle-sheath zone. The processes are separated across different locations in the leaf, which helps maintain a higher CO₂ environment around rubisco where the Calvin cycle operates.",
  "The right display remains in the same tissue but the clock turns to night. Stomata open mainly at night, when evaporative water loss can be lower. Incoming carbon is fixed and stored in **organic acids**. The chamber then seals its stomata as the clock shifts to daylight. Stored carbon is released as CO₂ during the day and supplied to the Calvin cycle. Nia names this strategy **CAM photosynthesis**. CAM plants reduce water loss through **temporal separation**: carbon acquisition and storage occur mainly at night, while daytime release of CO₂ supports Calvin-cycle carbon fixation behind more closed stomata.",
  "Nia places two large labels under the displays and refuses to let them swap. **C4 = spatial separation. CAM = temporal separation.** Both strategies can reduce photorespiration by improving CO₂ availability around rubisco under challenging conditions, but they do not use the same architecture. C4 separates initial fixation and Calvin-cycle processing across different cell locations. CAM separates carbon capture/storage and Calvin-cycle access across different times of day. The center photorespiration-pressure gauge falls in both demonstrations, but the arrows that solve the problem remain visibly different.",
  "At the far wall, the greenhouse’s net-carbon-gain gauge returns to green. Nia removes the duplication from the carbon tracer and places the original amber marker into the organic-carbon output crate from the G3P room. You can now reconstruct the entire greenhouse without memorizing every Calvin-cycle intermediate: ATP and NADPH arrive in the stroma; CO₂ is fixed by rubisco onto the RuBP acceptor; G3P can leave while RuBP is regenerated; oxygen can divert rubisco into photorespiration; C4 and CAM reduce that pressure using spatial and temporal separation, respectively. A service hatch opens beside the organic-carbon crate. Beyond it, a sign reads RESPIRATION POWER PLANT. The carbon is now stored in organic molecules, and the next question is how cells can extract usable energy from those fuels."
 ],
 'close':'The Carbon Fixation Greenhouse is stable again. The same carbon that entered as inorganic CO₂ has been traced into organic carbon, while the next unopened route waits to examine how cellular respiration harvests energy from fuel.'
},
}

TERM_IMAGES={
'U3-K-039':'ATP and NADPH arriving separately through the left stroma gate and powering the central carbon-fixation route',
'U3-K-133':'the circular stroma pathway using ATP and NADPH while carbon enters and the acceptor is regenerated',
'U3-K-134':'the amber carbon tracer leaving inorganic CO₂ and becoming part of an organic carbon framework at the central bench',
'U3-K-135':'the large central rubisco enzyme docking CO₂ and RuBP without being consumed as either substrate',
'U3-K-136':'the five-carbon RuBP acceptor waiting on the right rack and returning after regeneration',
'U3-K-137':'the three-carbon G3P molecule leaving through the left output gate toward organic-molecule synthesis',
'U3-K-138':'the small three-CO₂ bookkeeping ring showing 9 ATP, 6 NADPH, one net G3P, and RuBP regeneration as secondary accounting',
'U3-K-140':'rubisco at a branch where O₂ sends the reaction into a right-side detour and the net-carbon-gain gauge falls',
'U3-K-141':'the old-atmosphere hypothesis panel beside the photorespiratory branch, paired with a caution about possible protective roles',
'U3-K-142':'the left C4 leaf model separating initial fixation in mesophyll from Calvin-cycle processing in bundle-sheath cells',
'U3-K-143':'the right CAM leaf model opening stomata at night, storing carbon in organic acids, and releasing CO₂ during the day',
}

LEARNER_MEANING={
'U3-K-138':'In a three-CO₂ accounting model, three turns use 9 ATP and 6 NADPH, produce one net G3P, and route five additional G3P equivalents toward regeneration of three RuBP. Keep this bookkeeping secondary to the cycle logic.'
}

CHECKPOINT_HINTS={
'U3-L35':'Look to the fixed right-hand rack at the carbon-fixation bench. The molecule there receives incoming CO₂; the large structure in the center is the enzyme that catalyzes the reaction.',
'U3-L37':'Return to the rubisco junction. CO₂ stays on the successful left fixation route, while the competing molecule enters from the right and sends the system into the carbon-losing detour.'
}

scenes=[]
for idx,lid in enumerate(J5['route']):
    b=B[lid]; n=NARR[lid]
    zones=[{'position':pos,'label':lab,'symbol':sym,'description':desc} for pos,lab,sym,desc in ZONE_COPY[lid]]
    cast=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    cast += [{'name':name,'kind':kind,'visual':visual,'job':job} for name,kind,visual,job in CAST[lid]]
    beats=[]; snaps=[]
    for t in b['term_introductions']:
        image=TERM_IMAGES.get(t['knowledge_id'],b['carry_forward'])
        beats.append({'object_id':t['knowledge_id'],'term':t['canonical_term'],'story':image,'science':t['canonical_science'],'exact_name':bool(t.get('exact_name_recall')),'hint':image})
        snaps.append({'term':t['canonical_term'],'meaning':LEARNER_MEANING.get(t['knowledge_id'],t['canonical_science']),'image':image})
    qr=b['quick_recall']; cp=bool(qr.get('enabled'))
    scenes.append({
      'scene_index':idx,'locus':b['scene_title'],'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['exact_location']+' — '+b['micro_anchor']+'.',
      'scene_layout':{'orientation':b['orientation_sentence'],'zones':zones},'cast':cast,
      'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':beats,'memory_snapshot':snaps,
      'checkpoint':cp,'checkpoint_object_id':b['primary_knowledge_id'],'checkpoint_prompt':qr.get('candidate_prompt','') if cp else '',
      'checkpoint_answer':qr.get('answer','') if cp else '','checkpoint_hint':CHECKPOINT_HINTS.get(lid,'') if cp else '',
      'next_locus':B[b['causal_transition']['to_locus_id']]['scene_title'] if b['causal_transition']['to_locus_id'] else None,
      'misconception_guards':b['misconception_guards'],'required_visual':b['visual_spec'],'carry_forward':b['carry_forward']
    })

journey={
 'schema':'memory-palace-v2-unit3-f4e-story-1.0','unit_id':'unit-3','palace_id':'U3-J5','journey_id':'U3-J5',
 'palace_name':'Carbon Fixation Greenhouse','story_title':'The Greenhouse That Kept Losing Carbon',
 'tagline':'Carry ATP and NADPH from the light reactions into the stroma, follow one carbon tracer through fixation and G3P output, then diagnose photorespiration and compare the spatial C4 and temporal CAM solutions.',
 'guide':GUIDE,'premise':J5['premise'],'mission':J5['mission'],
 'finale':'The greenhouse succeeds when ATP and NADPH are connected to stroma carbon fixation without becoming carbon themselves, CO₂ is fixed through rubisco onto the RuBP acceptor, G3P output is separated from RuBP regeneration, photorespiration is recognized as rubisco oxygenation that lowers net carbon fixation, and C4 spatial separation is kept distinct from CAM temporal separation.',
 'estimated_minutes':18,'scene_count':len(scenes),'checkpoint_count':sum(bool(s['checkpoint']) for s in scenes),
 'learner_rule':'Follow the amber carbon tracer and keep each scene’s fixed left, center, and right anchors stable. Detailed Calvin-cycle bookkeeping remains secondary to the causal route. Quick Recall is optional during the first pass.',
 'route_orientation':'The Carbon Fixation Greenhouse is a five-station stroma-to-adaptation route. Enter where ATP and NADPH arrive from the light reactions, follow one amber carbon tracer through the rubisco fixation bench and the G3P/RuBP loop, then carry the rubisco competition problem into photorespiration and finish in a split conservatory comparing C4 spatial separation with CAM temporal separation.',
 'route':route,'scenes':scenes,'student_release':'PILOT_PREVIEW_F4E','narrative_standard':'V2-NARRATIVE-3.0-U3-F4E'
}

(U3/'journeys').mkdir(parents=True,exist_ok=True)
(U3/'journeys'/'U3-J5.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

js=[json.loads((U3/'journeys'/f'U3-J{i}.json').read_text(encoding='utf-8')) for i in range(1,5)]+[journey]
def card(j): return {k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
registry={'schema':'memory-palace-v2-unit3-f4e-registry-1.0','course_id':'ap-biology','unit_id':'unit-3','unit_title':'Cellular Energetics','narrative_standard':'V2-NARRATIVE-3.0-U3-F4E','journey_count':5,'scene_count':sum(x['scene_count'] for x in js),'checkpoint_count':sum(x['checkpoint_count'] for x in js),'guided_journeys':[card(x) for x in js]}
(U3/'journeys-f4e.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U3/'status-f4d.json').read_text(encoding='utf-8'))
status.update({'status':'F4E_JOURNEY5_POLISHED_PREVIEW','pipeline_status':'POLISHED_NARRATIVE_JOURNEYS_1_5_F4E','student_release':False,'preview_release':True,'journey_count':5,'scene_count':registry['scene_count'],'polished_journeys':5,'polished_scenes':registry['scene_count'],'polished_checkpoint_count':registry['checkpoint_count'],'narrative_story_files':5,'next_required_output':'F4F polished narrative for Journey 6 Respiration Power Plant after F4E prose QA'})
(U3/'status-f4e.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(U3/'status.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; c=json.loads(cp.read_text(encoding='utf-8'))
for u in c['units']:
    if u['unit_id']=='unit-3':
        u.update({'status':'F4E_JOURNEY5_POLISHED_PREVIEW','journey_count':5,'scene_count':registry['scene_count'],'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEYS1_5_POLISHED_F4E','polished_journeys':5,'polished_scenes':registry['scene_count'],'student_release':False})
cp.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

bc=ROOT/'backend'/'content.py'; bs=bc.read_text(encoding='utf-8')
old='    if unit_id == "unit-3":\n        path=UNIT3_DIR / "journeys-f4d.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4c.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4b.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4a.json"\n        return _read_json(path)["guided_journeys"] if path.exists() else []'
new='    if unit_id == "unit-3":\n        path=UNIT3_DIR / "journeys-f4e.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4d.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4c.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4b.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4a.json"\n        return _read_json(path)["guided_journeys"] if path.exists() else []'
if old in bs: bs=bs.replace(old,new)
elif 'journeys-f4e.json' not in bs: raise RuntimeError('Could not patch Unit 3 journey registry preference to F4E')
bc.write_text(bs,encoding='utf-8')

mainp=ROOT/'backend'/'main.py'; ms=mainp.read_text(encoding='utf-8')
ms=ms.replace('0.15.0-u3-f4d','0.16.0-u3-f4e').replace('v2-apbio-0.15.0-u3-f4d','v2-apbio-0.16.0-u3-f4e')
mainp.write_text(ms,encoding='utf-8')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
files=['journeys/U3-J5.json','journeys-f4e.json','status-f4e.json']
lock={'schema':'memory-palace-v2-unit3-f4e-content-lock-1.0','unit_id':'unit-3','stage':'F4E','student_release':False,'files':{f:sha(U3/f) for f in files}}
(U3/'content-lock-f4e.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit3-f4e-release-manifest-1.0','unit_id':'unit-3','stage':'F4E','student_release':False,'preview_release':True,'polished_journeys':5,'polished_scenes':registry['scene_count'],'journey_5_records':sum(len(s['object_ids']) for s in scenes),'journey_5_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'next_stage':'F4F_JOURNEY6'}
(U3/'f4e-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Built Unit 3 F4E:',len(scenes),'scenes',sum(len(s['object_ids']) for s in scenes),'knowledge records',sum(bool(s['checkpoint']) for s in scenes),'checkpoints')
