from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content'/'ap-biology'/'unit-3'
briefs=json.loads((U3/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
jbriefs=json.loads((U3/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
B={s['locus_id']:s for s in briefs if s['journey_id']=='U3-J6'}
J6=next(j for j in jbriefs if j['journey_id']=='U3-J6')

GUIDE={
 'name':'Dr. Nia Park',
 'role':'cellular-energetics investigator',
 'visual':'navy field jacket, clear safety glasses, and a compact tablet now split into three synchronized traces labeled carbon, electrons, and proton gradient',
 'story_job':'Nia keeps carbon flow, electron transfer, proton movement, oxygen reduction, and ATP formation on separate visual tracks while the learner follows one continuous respiration route from cytosol to mitochondrial membrane and then to a prokaryotic comparison.'
}

route=[
 {'scene_index':0,'locus':'Respiration Fuel Intake','short':'Fuel Intake','floor':'Cytosolic entrance','symbol':'fuel'},
 {'scene_index':1,'locus':'Glycolysis Floor','short':'Glycolysis','floor':'Cytosolic processing floor','symbol':'3C'},
 {'scene_index':2,'locus':'Electron Carrier Charging Bay','short':'Carriers','floor':'Carrier bay','symbol':'e⁻'},
 {'scene_index':3,'locus':'Pyruvate Oxidation Airlock','short':'Pyruvate','floor':'Mitochondrial entry','symbol':'2C'},
 {'scene_index':4,'locus':'Citric Acid Cycle Chamber','short':'Citric Cycle','floor':'Matrix cycle room','symbol':'cycle'},
 {'scene_index':5,'locus':'Mitochondrial Architecture Bay','short':'Mitochondrion','floor':'Cutaway bay','symbol':'mt'},
 {'scene_index':6,'locus':'Respiratory Electron-Transport Descent','short':'ETC','floor':'Inner-membrane descent','symbol':'e⁻↓'},
 {'scene_index':7,'locus':'Proton Pumping Wall','short':'H⁺ Gradient','floor':'Inner membrane','symbol':'H⁺'},
 {'scene_index':8,'locus':'Oxygen Terminal-Acceptor Basin','short':'Oxygen','floor':'ETC terminus','symbol':'O₂'},
 {'scene_index':9,'locus':'Oxidative-Phosphorylation Turbine','short':'OxPhos','floor':'ATP turbine hall','symbol':'ATP'},
 {'scene_index':10,'locus':'Uncoupling Heat Vent','short':'Heat Vent','floor':'Bypass chamber','symbol':'heat'},
 {'scene_index':11,'locus':'Prokaryotic Respiratory Membrane','short':'Prokaryote','floor':'Comparison annex','symbol':'PM'},
]

ZONE_COPY={
'U3-L39':[
 ('left','Fuel receiving lanes','fuel','Carbohydrate-, fat-, and protein-derived molecules enter through separate left-side lanes so glucose can remain a central example without being treated as the only respiratory fuel.'),
 ('center','Aerobic respiration stage map','route','A large center map connects cytosolic glycolysis, mitochondrial carbon oxidation, and oxidative phosphorylation into one coordinated energy-harvesting pathway.'),
 ('right','Respiration output board','CO₂ H₂O ATP heat','Carbon dioxide, water, ATP, and heat appear only after the relevant stages operate, keeping the overall equation as net accounting rather than one literal reaction.')],
'U3-L40':[
 ('left','Glucose and ATP investment gate','6C + 2 ATP','A conventional six-carbon glucose model enters from the left beside two ATP tokens that are visibly spent during the investment portion of glycolysis.'),
 ('center','Glycolytic splitting line','6C → 3C + 3C','The center line remains in the cytosol and converts one six-carbon glucose through enzyme-catalyzed steps into two three-carbon pyruvate molecules.'),
 ('right','Glycolysis output platform','pyruvate NADH ATP','Two pyruvate models, charged NADH carriers, and the ATP payoff appear separately on the right so carbon, electrons, and ATP accounting remain distinct.')],
'U3-L41':[
 ('left','NAD⁺ / NADH carrier pair','NAD⁺ ⇄ NADH','The left station keeps oxidized NAD⁺ physically paired with reduced NADH and uses a blue electron marker to show when the carrier is loaded.'),
 ('center','Electron-loading station','e⁻ transfer','A center transfer platform moves representative high-energy electrons from oxidized fuel intermediates onto mobile electron carriers without portraying electrons as stored ATP.'),
 ('right','FAD / FADH₂ carrier pair','FAD ⇄ FADH₂','The right station previews the FAD carrier pair used later in the citric acid cycle and keeps its reduced FADH₂ form distinct from NADH.')],
'U3-L42':[
 ('left','Pyruvate entry rail','3C pyruvate','Two three-carbon pyruvate molecules arrive from the cytosol and cross into the mitochondrial processing route.'),
 ('center','Oxidation and decarboxylation airlock','3C → 2C','The central transition station removes carbon as CO₂, transfers electrons to NAD⁺, and attaches the remaining two-carbon acetyl group to coenzyme A.'),
 ('right','Acetyl-CoA output dock','acetyl-CoA + NADH + CO₂','Acetyl-CoA, NADH, and carbon dioxide leave through separate right-side channels so the carbon product and electron carrier are never collapsed into one output.')],
'U3-L43':[
 ('left','Acetyl-CoA entry gate','2C acetyl','The two-carbon acetyl group carried by coenzyme A enters from the left while coenzyme A itself remains visually identifiable as the carrier.'),
 ('center','Citric acid cycle in matrix','cycle','A circular center pathway in the mitochondrial matrix oxidizes acetyl-derived carbon while regenerating the cycle acceptor and transferring energy to reduced carriers.'),
 ('right','Cycle output rack','CO₂ ATP NADH FADH₂','Carbon dioxide, a small amount of ATP or equivalent substrate-level product, NADH, and FADH₂ accumulate on distinct right-side shelves.')],
'U3-L44':[
 ('left','Intermembrane space','high-H⁺ side later','The left compartment lies between the outer and inner mitochondrial membranes and will become the higher-proton side once the respiratory ETC is running.'),
 ('center','Cristae-rich inner membrane','folded membrane','The center inner membrane folds into recognizable cristae, increasing membrane surface available for electron transport and ATP-synthesis machinery.'),
 ('right','Mitochondrial matrix','matrix','The right compartment contains the pyruvate-oxidation and citric-cycle machinery already visited and stays visually distinct from the intermembrane space.')],
'U3-L45':[
 ('left','Reduced-carrier electron entry','NADH FADH₂','NADH and FADH₂ arrive from earlier reactions and release representative blue electron tracers into different entry points of the respiratory electron-transfer system.'),
 ('center','Respiratory electron-transport chain','redox descent','A conventional series of inner-membrane electron carriers passes electrons through successive redox reactions toward lower-free-energy states.'),
 ('right','Terminal-acceptor end','O₂ ahead','The chain ends beside an oxygen-marked acceptor basin that remains inactive until terminal electrons actually arrive.')],
'U3-L46':[
 ('left','Matrix low-H⁺ side','matrix','The matrix side remains on the left of this membrane cross-section and loses protons as selected ETC complexes move H⁺ away from it.'),
 ('center','Inner-membrane proton-pumping complexes','pump','Certain center membrane complexes couple energy released by electron transfer to active proton translocation across the inner membrane.'),
 ('right','Intermembrane high-H⁺ side','H⁺ H⁺ H⁺','Protons accumulate on the right in the intermembrane space, creating both a concentration difference and an electrical contribution to proton-motive force.')],
'U3-L47':[
 ('left','Incoming terminal electrons','e⁻','The final blue electron tracers arrive from the respiratory ETC on the left after their energy has already been used along the chain.'),
 ('center','Oxygen terminal-acceptor basin','O₂','Molecular oxygen sits at the center as the terminal electron acceptor and receives electrons together with protons.'),
 ('right','Water product channel','H₂O','Water forms on the right after oxygen is reduced, making oxygen consumption a terminal redox event rather than a direct ATP-forming reaction.')],
'U3-L48':[
 ('left','Proton-gradient reservoir','H⁺ reservoir','The high-proton intermembrane side feeds H⁺ toward ATP synthase while the lower-proton matrix side waits beyond the membrane.'),
 ('center','ATP synthase and chemiosmosis turbine','ATP synthase','A conventional membrane-spanning ATP synthase uses proton-motive force as H⁺ moves through it, driving rotational and conformational changes linked to ATP formation.'),
 ('right','ATP and yield dashboard','ATP ≈ variable','ATP appears beside a yield dashboard that presents approximate respiratory totals while keeping variable shuttle costs and proton leak visible.')],
'U3-L49':[
 ('left','Stored proton gradient','H⁺ pressure','The same proton gradient from oxidative phosphorylation remains intact on the left before any bypass is opened.'),
 ('center','Uncoupling proton bypass','leak','A controlled center leak lets protons cross the membrane without passing through ATP synthase, disconnecting part of proton flow from ATP production.'),
 ('right','Heat and efficiency display','heat ↑ ATP capture ↓','More gradient energy is dissipated as heat on the right while the amount captured as ATP falls, making the energy-partition tradeoff visible on two separate gauges.')],
'U3-L50':[
 ('left','Cytoplasmic side','cytoplasm','The left side represents the cytoplasm of a prokaryotic cell, where no mitochondrial matrix is available because the cell has no mitochondria.'),
 ('center','Prokaryotic plasma-membrane ETC','plasma membrane','Respiratory electron carriers, proton-translocation machinery, and ATP-synthesis machinery are embedded directly in the prokaryotic plasma membrane.'),
 ('right','External or periplasmic proton side','H⁺ outside','The right side represents the proton-enriched side outside the cytoplasm, which may be external or periplasmic depending on prokaryotic cell organization.')],
}

CAST={
'U3-L39':[
 ('fuel shipment','respiratory input','a rack of glucose, fatty-acid, and amino-acid derived fuel models entering through three labeled chutes','supplies oxidizable biological molecules whose chemical energy can be harvested by cellular respiration'),
 ('amber carbon tracer','carbon continuity marker','one amber-highlighted carbon atom embedded in the glucose model and retained on Nia’s carbon ledger','lets the learner follow carbon through oxidation and eventual carbon-dioxide release without confusing carbon flow with electron transfer'),
 ('blue electron tracer','electron continuity marker','a blue glowing electron-pair marker shown on Nia’s separate electron ledger beside the fuel','will be transferred onto reduced carriers and later through the respiratory ETC while remaining separate from the carbon tracer')],
'U3-L40':[
 ('glucose','six-carbon fuel','a conventional six-carbon glucose model carrying the amber carbon tracer','enters glycolysis as the carbon substrate that is split into two three-carbon pyruvate products'),
 ('ATP investment and payoff','energy accounting','two red ATP tokens disappear at the investment gate while four green ATP tokens appear later at payoff stations','separates gross ATP production from the net gain of two ATP in the classroom bookkeeping model'),
 ('pyruvate pair','carbon output','two matching three-carbon pyruvate models exiting the line','carry glucose-derived carbon from cytosolic glycolysis toward mitochondrial oxidation')],
'U3-L41':[
 ('NAD⁺ / NADH','electron-carrier pair','an oxidized NAD⁺ carrier that closes around transferred electrons and becomes NADH','accepts high-energy electrons and a proton equivalent and carries reducing power toward later reactions including the respiratory ETC'),
 ('FAD / FADH₂','electron-carrier pair','an FAD carrier on the right that becomes FADH₂ when loaded during later citric-cycle reactions','provides a second reduced electron carrier that can feed the respiratory ETC'),
 ('blue electron tracer','electron continuity marker','a blue marker moving from an oxidized fuel intermediate into the carrier dock','keeps electron transfer visible without implying that NADH or FADH₂ is itself energy in material form')],
'U3-L42':[
 ('pyruvate','three-carbon substrate','a three-carbon pyruvate model arriving from the glycolysis floor','is transported into mitochondrial processing and converted to an acetyl group carried by coenzyme A'),
 ('coenzyme A','acetyl carrier','a recognizable coenzyme A handle waiting beside the two-carbon product','accepts the remaining two-carbon acetyl group to form acetyl-CoA'),
 ('NAD⁺ carrier','electron acceptor','an NAD⁺ carrier positioned beside the oxidation station','is reduced to NADH as pyruvate oxidation transfers electrons away from the carbon substrate')],
'U3-L43':[
 ('acetyl-CoA','two-carbon entry carrier','a two-carbon acetyl unit held by a coenzyme A handle at the cycle entrance','delivers acetyl carbon into the citric acid cycle'),
 ('NAD⁺ and FAD carriers','electron acceptors','empty NAD⁺ and FAD carriers circulating along the outer rail of the chamber','accept electrons during oxidation steps to form NADH and FADH₂'),
 ('carbon-dioxide vents','carbon output','CO₂ vents opening above the right-side output rack as carbon is oxidized','show carbon leaving the pathway separately from the electron carriers and ATP output')],
'U3-L44':[
 ('mitochondrial cutaway','organelle map','a conventional double-membrane mitochondrion cut open so matrix, inner membrane, cristae, and intermembrane space remain visible at once','anchors each stage of eukaryotic aerobic respiration to the correct cellular compartment'),
 ('cristae','inner-membrane folds','deep folds of the inner mitochondrial membrane extending through the central bay','increase membrane surface available for respiratory electron transport and ATP-synthesis machinery'),
 ('stage markers','location labels','small markers for glycolysis, pyruvate oxidation/citric cycle, and oxidative phosphorylation attached to their actual locations','prevent the entire respiration pathway from being incorrectly placed inside the mitochondrion')],
'U3-L45':[
 ('NADH','reduced electron carrier','a reduced carrier arriving at a high-energy entry point with blue electron tracers','donates electrons to the respiratory electron-transfer system and returns to an oxidized carrier form'),
 ('FADH₂','reduced electron carrier','a second reduced carrier entering the chain at a different point','delivers electrons to the respiratory ETC through a route that does not create the same proton-pumping opportunity as NADH entry'),
 ('inner-membrane redox carriers','electron-transfer chain','a series of conventional membrane complexes and mobile carriers arranged along the descent','undergo successive oxidation-reduction reactions and pass electrons toward the terminal acceptor')],
'U3-L46':[
 ('proton pumps','membrane transport machinery','selected ETC complexes spanning the inner mitochondrial membrane with arrows from matrix to intermembrane space','couple energy released during electron transfer to proton translocation'),
 ('H⁺ gradient','electrochemical gradient','a rising concentration of red H⁺ markers on the intermembrane side and a lower concentration in the matrix','stores potential energy as an electrochemical proton gradient across the inner membrane'),
 ('pH gauges','chemical comparison','two fixed pH gauges showing a more acidic intermembrane side and a relatively higher-pH matrix','connect proton concentration to the matrix-intermembrane pH difference')],
'U3-L47':[
 ('oxygen','terminal electron acceptor','a conventional O₂ molecule waiting in a basin at the end of the ETC','accepts terminal electrons and is reduced during aerobic respiration'),
 ('terminal electrons','electron input','blue electron tracers arriving from the final ETC carrier','complete the electron-transfer route that began when fuel molecules were oxidized'),
 ('protons','reaction partners','H⁺ markers approaching the oxygen basin from the surrounding aqueous compartment','combine with reduced oxygen during water formation')],
'U3-L48':[
 ('ATP synthase','membrane enzyme complex','a conventional F-type ATP synthase spanning the inner mitochondrial membrane with a rotor-like central stalk','uses proton-motive force to catalyze ATP formation from ADP and inorganic phosphate'),
 ('proton-motive force','stored gradient energy','the combined concentration and charge difference represented by the high-H⁺ reservoir','drives proton flow through ATP synthase during chemiosmosis'),
 ('ATP yield dashboard','variable accounting display','a dashboard showing oxidative phosphorylation near 26–28 ATP and total aerobic yield near 30–32 ATP per glucose with a visible variability bracket','keeps useful modern estimates available without presenting one exact ATP total as universal')],
'U3-L49':[
 ('uncoupling bypass','proton leak path','a membrane channel opening beside ATP synthase and carrying H⁺ across without ATP production','dissipates part of the proton gradient independently of ATP synthase'),
 ('heat sensor','energy consequence','a thermal gauge rising as the bypass opens','shows gradient energy appearing as heat when proton flow is decoupled from ATP production'),
 ('ATP capture meter','efficiency consequence','an ATP-production meter dropping as more H⁺ avoids ATP synthase','shows that uncoupling reduces the fraction of gradient energy captured in ATP')],
'U3-L50':[
 ('prokaryotic plasma membrane','respiratory membrane','a conventional bacterial-style plasma membrane containing respiratory electron carriers and ATP synthase','provides the membrane across which prokaryotic respiration can establish a proton gradient without mitochondria'),
 ('cytoplasm','low-proton side','the aqueous cell interior fixed on the left of the membrane model','serves as one side of the chemiosmotic gradient and contains many metabolic reactions'),
 ('proton-enriched side','gradient destination','the region outside the cytoplasm fixed on the right, labeled external/periplasmic as appropriate','receives protons translocated across the plasma membrane and supports the same general chemiosmotic logic')],
}

NARR={
'U3-L39':{
 'title':'The Plant With Fuel and No Power',
 'kicker':'A glucose shipment has arrived, yet the ATP grid remains dark because carbon, electrons, protons, and energy capture have been disconnected from one another.',
 'paragraphs':[
  "The service hatch from the Carbon Fixation Greenhouse opens onto an industrial hall built around a transparent mitochondrial block. The organic-carbon crate from Journey 5 rolls in beside you, but Dr. Nia Park stops it before it reaches the machinery. The **left** wall holds three fuel lanes marked carbohydrate-derived, fat-derived, and protein-derived. The **center** is a stage map whose three major sections are dark. The **right** wall carries four output gauges for CO₂, H₂O, ATP, and heat. Nothing moves between them. Nia’s tablet splits into three traces. An amber carbon marker sits inside a glucose model. A separate blue electron marker glows on the electron ledger. A red H⁺ pressure gauge stays at zero. ‘If those traces blur together,’ she says, ‘the plant may run in your imagination while the biology falls apart.’",
  "Nia feeds glucose into the center map first, then points back to the other fuel lanes. Cells can harvest energy from **carbohydrates, fats, and proteins**. Glucose is a central respiratory substrate and the cleanest molecule for following this route, yet the plant does not label starch as a universal major fuel for animals. The center map now illuminates three broad stages. The first is **glycolysis** in the cytosol. The second combines **pyruvate oxidation and the citric acid cycle** in mitochondrial carbon oxidation. The third is **oxidative phosphorylation** at the inner mitochondrial membrane. Nia names the overall organization **Aerobic respiration as coordinated pathway**. It is a connected series of enzyme-catalyzed reactions, not one giant combustion event inside a mitochondrion.",
  "The right board displays a familiar net model, **C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + usable energy captured in ATP plus heat**. Nia keeps it above the stage map as accounting, not choreography. Six oxygen molecules do not collide with one glucose molecule in a single cellular step. Carbon compounds derived from glucose are progressively **oxidized**, while oxygen is ultimately **reduced** as electrons move toward lower-free-energy states. The blue electron tracer therefore has its own route. The amber carbon tracer has another. The red proton gauge will appear only after electron transfer is coupled to membrane pumping. ATP remains an output of energy coupling, not a destination into which carbon or electrons literally transform.",
  "With those distinctions fixed, Nia names the mission **respiration and ATP synthesis**. Cellular respiration uses energy from biological macromolecules to synthesize ATP. The plant’s output board flickers, but only the first stage of the center map opens. It is outside the mitochondrial block in a broad cytosolic processing floor. The amber tracer enters as one carbon within six-carbon glucose, and the blue electron marker is clipped to the same fuel ledger without being fused to it. ‘We start where a eukaryotic cell actually starts,’ Nia says. ‘Before the mitochondrion.’ You follow the glucose model down the ramp to the Glycolysis Floor while the other fuel lanes remain visible behind you as alternate inputs to the larger respiratory network."
 ],
 'close':'The stage map has stopped pretending respiration is one reaction. Glucose and its separate carbon and electron tracers descend into the cytosolic Glycolysis Floor, where ATP investment, carbon splitting, and electron capture can be watched independently.'
},
'U3-L40':{
 'title':'The Six-Carbon Line Splits in Two',
 'kicker':'Glycolysis must account for carbon, electron carriers, ATP investment, and ATP payoff without placing any of those events inside the mitochondrion.',
 'paragraphs':[
  "The ramp ends on a wide **cytosolic** factory floor. There is no mitochondrial membrane around you. On your **left**, one conventional six-carbon glucose model waits beside two ATP tokens at an investment gate. Directly **ahead**, an enzyme-controlled splitting line runs through the center. On your **right**, three output shelves are empty and labeled PYRUVATE, NADH, and ATP. Nia places the amber carbon tracer on one carbon within glucose and keeps the blue electron marker on a separate readout above the line. The geography is simple enough to redraw. Input and investment stay left. The carbon-processing line stays center. Products stay right. This is where **glycolysis** occurs, in the cytosol.",
  "The first section consumes two ATP in the standard bookkeeping model. Nia lets the ATP tokens disappear into phosphorylation steps and then keeps the investment counter visible instead of suggesting that glycolysis simply makes ATP from its first instant. Farther along, the six-carbon carbon skeleton is reorganized and split so the line ultimately produces **two three-carbon pyruvate molecules**. The amber carbon tracer rides into one of them. No CO₂ vent opens here. The six glucose carbons are still represented in the two three-carbon products at the end of glycolysis. That absence matters because carbon dioxide release begins later in mitochondrial carbon oxidation, not during this cytosolic splitting stage.",
  "A second set of events charges NAD⁺ carriers while the payoff portion generates ATP. Four ATP tokens appear during the payoff in the classroom accounting model. With two ATP invested and four produced, the **net gain is two ATP per glucose**. Nia points to the small mechanical transfer that makes those ATP molecules. A high-energy phosphate is transferred directly from an organic metabolic intermediate to ADP. She names that mechanism **substrate-level phosphorylation**. ATP forms by direct enzymatic phosphate transfer from a substrate. No proton gradient and no ATP synthase is required for this particular ATP-making mechanism. Nia pins a label over it so it will remain physically separate from oxidative phosphorylation later and photophosphorylation from Journey 4.",
  "The right platform finally fills. Two pyruvate models arrive on the carbon shelf. Reduced NADH carriers appear on the electron shelf. The net ATP counter settles at two. Nia names the complete visible result **glycolysis outputs**. Glycolysis releases energy from glucose to form ATP, NADH, and pyruvate. The phrase now belongs to three separate shelves rather than one vague bag of ‘energy products.’ The carbon tracer is still inside pyruvate. The representative blue electron tracer now sits on an NADH carrier. The ATP tokens remain on their own accounting display. When the pyruvate carts start toward the mitochondrial airlock, the NADH carrier takes a different overhead rail toward the electron-carrier system. You follow both routes into the next bay before the carbon line crosses the mitochondrial boundary."
 ],
 'close':'Glycolysis ends in the cytosol with two pyruvate, NADH, and a net gain of ATP. The carbon cart and the electron-carrier rail now diverge long enough for the next bay to make oxidized and reduced carrier states unmistakable.',
},
'U3-L41':{
 'title':'The Carriers That Leave Empty and Return Loaded',
 'kicker':'Electron carriers must be understood as reversible oxidized/reduced pairs before their electrons enter the respiratory chain.',
 'paragraphs':[
  "A narrow side bay sits between the Glycolysis Floor and the mitochondrial airlock. On your **left**, an empty carrier frame is labeled NAD⁺. On your **right**, a second carrier pair is labeled FAD and FADH₂. The **center** loading station has only one moving object, the blue electron tracer. The pyruvate carbon cart waits behind a glass gate, deliberately paused. Nia says this room is about carrier state, not another carbon reaction. She also points to the right-side FAD pair before it has received anything. FADH₂ is important later in the citric acid cycle. Its presence here is a comparison model, not a claim that glycolysis just produced FADH₂.",
  "Nia brings an NAD⁺ carrier to the center dock. Electrons transferred from an oxidized fuel intermediate load onto the carrier, along with the associated proton chemistry represented by the model. The carrier closes and its label changes to NADH. She names the pair **NAD+ and NADH**. The familiar NAD⁺ notation on the carrier means the same oxidized form. NAD⁺ accepts electrons and a proton to become NADH, and NADH can carry high-energy electrons to other reactions, including the respiratory electron transport chain. The blue tracer sits on NADH like cargo. The carrier did not become an electron, and the electron did not become ATP. This is transfer of reducing power from one reaction to another.",
  "The right station now demonstrates the second pair. **FAD and FADH2** remain physically paired, with FADH₂ shown as the reduced notation on the model, so their oxidation state is always visible. During the citric acid cycle, FAD accepts electrons and protons to form FADH₂. FADH₂ can then deliver those electrons to the respiratory electron transport chain. Nia loads the demonstration carrier and immediately marks its future origin on the matrix-cycle map. NADH and FADH₂ are both reduced electron carriers, yet their later entry into the respiratory ETC is not identical. Keeping the two carrier pairs on opposite sides of the bay will make that difference easier to reconstruct when they arrive at the inner membrane.",
  "Nia zooms her tablet out. Many carrier molecules will be reduced over the course of respiration, so the single blue tracer is only a representative electron marker that helps you follow transfer. It does not mean one literal electron pair completes every step of the entire pathway. The carbon ledger remains separate. The pyruvate cart begins moving again and reaches a sealed mitochondrial entry station. As the airlock opens, the NADH rail branches away toward storage for the later ETC. You follow the three-carbon pyruvate and amber carbon tracer into the transition station, where the first carbon-dioxide vent is already attached to the ceiling."
 ],
 'close':'The carrier bay leaves NAD⁺/NADH on the left and FAD/FADH₂ on the right as permanent redox pairs. The carbon route now resumes at the mitochondrial Pyruvate Oxidation Airlock while reduced carriers wait to deliver electrons later.'
},
'U3-L42':{
 'title':'The Three-Carbon Cart Loses Carbon at the Airlock',
 'kicker':'Pyruvate oxidation is a transition step that releases CO₂, charges NADH, and converts the remaining carbon into acetyl-CoA before the cycle begins.',
 'paragraphs':[
  "The next station is built as an airlock between the cytosolic intake wing and the mitochondrial processing block. Two three-carbon pyruvate carts arrive on your **left**. The **center** chamber contains oxidation machinery, a CO₂ vent, an NAD⁺ docking arm, and a coenzyme A handle. On your **right**, three output lanes are labeled ACETYL-CoA, NADH, and CO₂. Nia leaves the outer architecture visible enough to remind you that pyruvate came from cytosolic glycolysis. In standard eukaryotic aerobic respiration, pyruvate is transported into the mitochondrion before this transition chemistry proceeds. The amber carbon tracer remains on one pyruvate as the chamber closes.",
  "Inside the airlock, the three-carbon substrate is oxidized. One carbon is removed and leaves through a CO₂ vent. Electrons are transferred to NAD⁺, creating NADH. The remaining two-carbon acetyl group is attached to coenzyme A. Nia names this transition **pyruvate oxidation**. During standard aerobic eukaryotic respiration, pyruvate is oxidized to an acetyl group carried by coenzyme A, with CO₂ and NADH produced. She keeps the right lanes separate. Carbon dioxide is carbon that has left the organic fuel pathway. NADH carries transferred electrons. Coenzyme A carries the remaining acetyl group. None of these three outputs is interchangeable with the others.",
  "The product on the main right rail is **acetyl-CoA**, short for acetyl coenzyme A. It carries a two-carbon acetyl group into the citric acid cycle. Nia points to the amber tracer, which in this model remains with the acetyl carbon entering the cycle. The exact fate of a particular carbon atom across repeated cycle turns depends on carbon position and cycle chemistry, so the tracer is an accounting aid for following carbon oxidation, not a claim that every carbon exits at one predetermined moment. What matters for the route is that glucose-derived carbon is progressively released as CO₂ as respiration proceeds.",
  "Above the airlock, Nia opens a broader sign labeled **pyruvate oxidation and Krebs inputs**. The name connects this transition to the matrix oxidation stage that follows. Pyruvate enters mitochondrial processing, carbon dioxide is released, NAD⁺ is reduced here, and the acetyl group becomes the input to the Krebs or citric acid cycle. During the cycle itself, additional electron transfer reduces NAD⁺ and FAD. The airlock therefore does not get credit for FADH₂ that forms later. The acetyl-CoA rail now continues directly into a circular chamber embedded in the mitochondrial matrix. The CO₂ vent remains behind you as the first visible proof that the carbon ledger has started to empty."
 ],
 'close':'Pyruvate oxidation has converted three-carbon pyruvate into a two-carbon acetyl group carried by coenzyme A while producing CO₂ and NADH. Acetyl-CoA now enters the matrix cycle where much more reducing power will be harvested.'
},
'U3-L43':{
 'title':'The Cycle That Empties the Carbon Ledger',
 'kicker':'The citric acid cycle oxidizes acetyl-derived carbon, releases CO₂, reduces electron carriers, and regenerates its acceptor without requiring a memorized parade of intermediates.',
 'paragraphs':[
  "The acetyl-CoA rail enters a round room deep in the **mitochondrial matrix**. On your **left**, the two-carbon acetyl group waits at an entry gate. The **center** floor is a circular pathway whose individual intermediate names are deliberately small. On your **right**, four shelves are labeled CO₂, ATP, NADH, and FADH₂. Nia parks the carbon ledger beside the cycle and spreads empty NAD⁺ and FAD carriers around the outer rail. ‘Keep your attention on what the cycle accomplishes,’ she says. ‘The detailed intermediate sequence can support understanding, but the main route is carbon oxidation, carrier reduction, a small direct ATP contribution, and regeneration of the cycle acceptor.’",
  "The acetyl group enters the circular pathway and its carbons become part of the cycle’s carbon pool. As oxidation reactions proceed, carbon dioxide leaves through vents and electron carriers are reduced. NAD⁺ becomes NADH. FAD becomes FADH₂. A small amount of ATP, or an energetically equivalent nucleotide product depending on context, is formed through substrate-level phosphorylation. The center pathway returns to a regenerated acceptor so another acetyl group can enter. Nia names the mechanism the **citric acid cycle**, also called the **Krebs cycle**. It oxidizes acetyl groups in the mitochondrial matrix and transfers energy to ATP, NADH, and FADH₂ while releasing CO₂.",
  "Nia then activates a fixed sign reading **Krebs-cycle location and outputs**. The location is the mitochondrial matrix. The outputs emphasized here are carbon dioxide, ATP, NADH, and FADH₂. The amber carbon tracer eventually reaches a CO₂ vent as carbon oxidation continues, so the carbon route that began in glucose can end as carbon dioxide. The blue electron ledger goes the opposite conceptual direction. Electrons removed from carbon compounds are now carried away on NADH and FADH₂ instead of leaving with CO₂. Carbon flow and electron flow are therefore visibly separating even as both arise from oxidation of the same fuel.",
  "A small accounting panel appears under the right shelves. In the per-glucose classroom model, the two cycle turns associated with one glucose yield **4 CO₂, 2 ATP, 6 NADH, and 2 FADH₂**. Nia keeps the figures smaller than the structural map. They are useful bookkeeping for this model, while the central idea is the repeated transfer of energy from acetyl-derived carbon into reduced carriers and a small amount of ATP. The room begins to fill with NADH and FADH₂ carts. They have nowhere useful to unload in the matrix. A door opens into a huge transparent mitochondrial cutaway, and every reduced carrier turns toward the folded inner membrane."
 ],
 'close':'The matrix cycle has released carbon as CO₂ and concentrated much of the harvested energy in reduced carriers. NADH and FADH₂ now leave the cycle chamber toward the mitochondrial inner membrane, forcing the next question of where electron transport and ATP synthesis actually occur.'
},
'U3-L44':{
 'title':'The Folded Wall Where the Next Stage Must Happen',
 'kicker':'Mitochondrial compartments become memorable when each respiration stage is attached to its actual location.',
 'paragraphs':[
  "You and Nia step onto a platform beside a giant conventional mitochondrial cutaway. The organelle is no longer a generic bean. The **left** compartment is the **intermembrane space** between the outer and inner membranes. The **center** is the inner mitochondrial membrane, folded repeatedly into **cristae**. The **right** compartment is the **matrix**, the room you just left. Nia rotates the cutaway until those three regions stay fixed relative to you. Then she brings the earlier route back onto the model. Glycolysis remains outside the mitochondrion in the cytosol. Pyruvate oxidation and the citric acid cycle attach to the matrix. The upcoming electron-transport and ATP-synthesis machinery attaches to the inner membrane.",
  "Nia names the display **mitochondrial structural review**. Eukaryotic aerobic respiration uses distinct mitochondrial compartments including the matrix, inner membrane, cristae, and intermembrane space. The value of the cutaway is causal. A membrane can maintain different conditions on its two sides. The matrix and intermembrane space can therefore support an electrochemical gradient once proton pumping begins. If those spaces are mentally collapsed into one interior, chemiosmosis becomes impossible to reconstruct correctly.",
  "She runs a light across the folded center membrane. Each fold is a **crista** and the set of folds are **cristae**. Their effect is captured by the term **cristae and ATP-production surface**. Folding of the inner mitochondrial membrane into cristae increases membrane surface area available for electron transport and ATP synthesis. Nia does not claim that folding creates energy by itself. It creates more membrane area in which the protein complexes that perform these processes can be embedded. The surface supports the machinery. The fuel-derived electron carriers supply the reducing power that will operate it.",
  "The NADH and FADH₂ carts from the matrix cycle now line up along the inner membrane. The left intermembrane space is still nearly empty of the red H⁺ markers that will later accumulate there. The right matrix contains the reduced carriers and a relatively low proton concentration. Nia clips the blue electron tracer to one NADH cart and opens a descending catwalk embedded in the center membrane. The catwalk ends near an oxygen basin, but ATP synthase is still locked behind another gate. ‘First the electrons have to move,’ she says. ‘Then we ask what that electron transfer does to the membrane.’"
 ],
 'close':'The mitochondrial cutaway fixes the geography. Matrix on one side, intermembrane space on the other, and cristae-rich inner membrane between them. Reduced carriers now enter the respiratory electron-transfer machinery embedded in that membrane.'
},
'U3-L45':{
 'title':'The Electron Descent That Charges the Membrane',
 'kicker':'NADH and FADH₂ donate electrons to an inner-membrane redox chain, and the electron path ends at a terminal acceptor rather than at ATP.',
 'paragraphs':[
  "The inner-membrane catwalk slopes through a row of conventional respiratory complexes. On your **left**, NADH and FADH₂ carts arrive carrying blue electron tracers. Directly **ahead**, the **respiratory electron transport chain** runs through the center membrane. On your **right**, an oxygen-marked terminal basin waits at the end, still separated from the ATP turbine. Nia unloads the representative blue tracer from NADH and leaves the carrier in its oxidized form. Another route shows FADH₂ contributing electrons through a different entry point. The two reduced carriers therefore feed the same larger electron-transfer system without being treated as identical in how they enter it.",
  "Nia names the input relationship **reduced coenzymes feed ETC**. NADH and FADH₂ produced during glycolysis and mitochondrial oxidation reactions transfer electrons to the inner-membrane electron transport chain. The carriers are shuttle systems between fuel oxidation and the membrane machinery. Once they donate their electrons, they can return in oxidized forms to participate in earlier reactions again. The blue tracer enters the center chain. It does not move toward an ATP molecule. It moves from one redox carrier to another.",
  "The center pathway is the **respiratory electron transport chain**, a series of inner-membrane electron carriers that undergo oxidation-reduction reactions and transfer electrons toward a terminal acceptor. As the blue tracer progresses, Nia’s energy indicator steps downward. The sequence lets electrons move through successively lower-free-energy states. Energy released along appropriate portions of that transfer can be coupled to other work, especially proton pumping. The electron itself remains an electron. Its route is an electron-transfer route. The red proton gauge beside the membrane is still a separate measurement.",
  "Nia labels the complete motion **respiratory electron transfer**. NADH and FADH₂ deliver electrons to an electron transport chain. In aerobic respiration, those electrons move toward oxygen as the terminal acceptor. She leaves one side panel showing that some anaerobic prokaryotic respiratory systems can use terminal acceptors other than oxygen, which keeps **aerobic respiration**, **anaerobic respiration**, and **fermentation** from collapsing into one category. Fermentation does not use this kind of respiratory ETC to pass electrons to an external terminal acceptor. As the blue tracer approaches the oxygen end, selected membrane complexes begin flashing arrows from the matrix toward the intermembrane space. The unresolved consequence pulls you to the Proton Pumping Wall."
 ],
 'close':'The blue electron tracer has descended through the respiratory ETC toward the terminal acceptor. Its transfer has activated membrane proton-pumping machinery, so the next scene follows H⁺ movement rather than pretending the electron itself becomes ATP.',
},
'U3-L46':{
 'title':'The Wall That Builds Pressure From Electron Transfer',
 'kicker':'Energy released by electron transfer is coupled to proton pumping, creating an electrochemical gradient across the inner mitochondrial membrane.',
 'paragraphs':[
  "You turn one corner and face the inner membrane as a vertical wall. For this cross-section, the **matrix** is fixed on your **left** and the **intermembrane space** on your **right**. The **center** wall contains selected ETC complexes with proton-pumping arrows. Nia deliberately reverses the left-right view from the earlier organelle cutaway only once, then locks it for this scene and marks the labels in large lettering. The blue electron tracer continues through the membrane complexes along a horizontal track. Red H⁺ markers occupy their own vertical route. The two paths cross at the machinery, yet they never merge.",
  "As electron transfer proceeds through certain ETC complexes, those complexes use released free energy to move H⁺ from the matrix across the inner membrane into the intermembrane space. Nia names this relationship **respiratory proton pumping**. The electron-transfer chain supplies the energy change that makes proton translocation possible. Electrons are not pumped into the intermembrane space, and protons do not travel along the electron-carrier sequence. One process is redox transfer within the membrane. The coupled process is active proton movement across it.",
  "The right-hand intermembrane space fills with red H⁺ markers. The left matrix loses them. Nia labels the resulting difference the **mitochondrial proton gradient**. Electron transfer through the respiratory ETC is coupled to formation of a proton gradient across the inner mitochondrial membrane, with a higher proton concentration in the intermembrane space than in the matrix. A charge indicator also shifts because H⁺ carries positive charge. Together, the concentration and electrical differences contribute to proton-motive force. Nia stores that term for the turbine room, where the gradient will actually do work.",
  "Two pH gauges now become legible. The high-H⁺ intermembrane side has the lower pH. The lower-H⁺ matrix has the higher pH. Nia calls the comparison the **matrix-intermembrane pH difference**. The matrix is higher in pH than the intermembrane space while this respiratory gradient is maintained. The pH labels are consequences of proton concentration, not an independent chemical trick. The gradient gauge reaches a stable pressure, yet the oxygen basin at the end of the electron chain still has unanswered electron cargo. Nia follows the blue tracer to that basin while leaving the red H⁺ reservoir stored behind the wall for later use."
 ],
 'close':'Electron transfer has built a high-H⁺ intermembrane side and a lower-H⁺, higher-pH matrix. The gradient is stored, while the blue electron tracer continues separately to oxygen at the end of the chain.'
},
'U3-L47':{
 'title':'The Basin Where Oxygen Finally Receives the Electrons',
 'kicker':'Oxygen’s job in aerobic respiration is terminal electron acceptance and reduction to water, not direct ATP production.',
 'paragraphs':[
  "The respiratory chain ends at a shallow basin cut into the inner-membrane terminus. On your **left**, the last electron carrier delivers the blue tracer. In the **center**, a conventional O₂ molecule waits under a sign marked TERMINAL ACCEPTOR. On your **right**, an empty water channel leads away from the basin. The red proton-gradient reservoir remains visible through a window behind you, still stored across the membrane. ATP synthase has not yet opened. Nia keeps the timing deliberate. Oxygen acts here at the end of the electron-transfer chain before the stored proton gradient is released through the ATP turbine.",
  "The incoming electrons are transferred to oxygen. Protons participate in the terminal chemistry, and oxygen is reduced to water. The balanced terminal reaction appears briefly above the basin as **O₂ + 4 e⁻ + 4 H⁺ → 2 H₂O**. Nia sends four blue electron markers into the model so the stoichiometry has visible meaning, while your representative tracer is one member of that set. Two water molecules leave through the right channel. The oxygen molecule has served as the **terminal electron acceptor** because it accepts the electrons at the end of the aerobic respiratory chain.",
  "Nia names the event **oxygen terminal reduction**. In aerobic respiration, O₂ is the terminal electron acceptor and is reduced to water. She points at the ATP counter, which remains unchanged during the basin demonstration. Oxygen does not donate ATP, and the act of oxygen reduction does not mechanically stamp ATP molecules into existence. Oxygen’s terminal acceptance allows the electron-transfer pathway to continue operating. Earlier electron transfer helped establish the proton gradient. That stored electrochemical gradient will be the immediate energy source used by ATP synthase in the next room.",
  "The water channel begins to flow and the blue electron tracer disappears into the completed reduction product. Its route is finished. Nia closes the electron tab on her tablet for the first time since the Fuel Intake and enlarges the red H⁺ gradient tab. The carbon ledger has already reached CO₂ vents. The electron ledger has reached H₂O through oxygen reduction. The remaining unspent potential is now spatial, stored as unequal H⁺ distribution across the inner membrane. A turbine gate opens beside the basin. You follow the pressure gauge, not the electron, into the Oxidative-Phosphorylation Turbine."
 ],
 'close':'Oxygen has accepted terminal electrons and been reduced to water. The electron journey ends here, while the proton gradient created earlier remains available to drive ATP synthesis through a separate membrane mechanism.'
},
'U3-L48':{
 'title':'The Turbine Driven by a Gradient',
 'kicker':'Oxidative phosphorylation couples respiratory electron transport to chemiosmotic ATP synthesis, with proton-motive force driving ATP synthase and ATP yield remaining an estimate.',
 'paragraphs':[
  "The turbine hall is built directly into the inner mitochondrial membrane. On your **left**, the intermembrane-side reservoir is crowded with H⁺. The **center** is dominated by a conventional membrane-spanning **ATP synthase** complex. On your **right**, the matrix side contains ADP, inorganic phosphate, newly formed ATP, and a yield dashboard. The blue electron tracer is gone because its terminal route ended at oxygen. Nia makes that absence part of the scene. ‘If you are waiting for an electron to enter this turbine, you are following the wrong continuity object,’ she says. The active tracer now is the proton gradient itself.",
  "H⁺ begins moving down its electrochemical gradient through ATP synthase toward the matrix. Nia names this use of gradient energy **chemiosmosis**. Chemiosmosis uses energy stored in an electrochemical proton gradient as protons move through a membrane-associated process such as ATP synthase. The proton-motive force drives motion and conformational changes within the enzyme complex. Nia lets the rotor-like elements turn while catalytic sites change shape. Those **rotational and conformational changes** support formation and release of ATP from ADP and inorganic phosphate. The protons do not become phosphate groups or ATP molecules. Their downhill movement supplies the energy that the enzyme couples to ATP synthesis.",
  "Nia places the exact name **ATP synthase** on the center complex. ATP synthase is a membrane enzyme complex that uses proton-motive force to catalyze ATP formation from ADP and inorganic phosphate. Then she widens the label to include the entire system. **Oxidative phosphorylation** is the aerobic respiratory process in which electron transport establishes the proton gradient and chemiosmosis through ATP synthase uses that gradient to drive ATP formation. The phrase **oxidative phosphorylation components** therefore belongs to two linked pieces, the electron-transport machinery that builds the gradient and ATP synthase-mediated chemiosmosis that spends it. This is distinct from the direct phosphate transfer of substrate-level phosphorylation and from light-driven photophosphorylation in chloroplasts.",
  "The right dashboard **does not show a fixed universal integer**. It shows a common modern estimate of roughly **26 to 28 ATP from oxidative phosphorylation** and roughly **30 to 32 ATP total per glucose** in many eukaryotic cells, then widens into a range. Shuttle systems, cell type, membrane leak, and other conditions change the exact yield. Nia labels the panel **respiratory ATP-yield estimate** so the number remains useful without becoming a law. The plant’s ATP grid finally turns on across the ceiling. Then a bypass valve beside ATP synthase starts glowing. ‘A functioning gradient can be spent another way,’ Nia says. ‘Watch what happens when H⁺ gets across without using this turbine.’"
 ],
 'close':'Chemiosmosis through ATP synthase now converts proton-motive force into ATP production as part of oxidative phosphorylation. The ATP grid is restored, but a side valve is about to reveal where gradient energy goes when proton flow bypasses ATP synthase.'
},
'U3-L49':{
 'title':'The Bypass That Turns Gradient Energy Into Heat',
 'kicker':'A proton leak can uncouple part of respiration from ATP production, lowering ATP capture efficiency while increasing heat release.',
 'paragraphs':[
  "The turbine hall narrows into a test chamber. The **left** reservoir contains the same stored proton gradient you just used for ATP synthesis. The **center** membrane holds a bypass channel beside ATP synthase. The **right** side has two gauges, one for ATP capture and one for heat. Nia closes ATP synthase temporarily so you can see the bypass by itself. The H⁺ markers remain high on one side and low on the other. The gradient still stores potential energy. Only the route by which protons return has changed.",
  "Nia opens the bypass. H⁺ flows down its electrochemical gradient through the leak without passing through ATP synthase. The proton difference shrinks, but the ATP counter barely moves. The heat sensor rises. Nia names the mechanism **respiratory uncoupling and heat**. Decoupling proton flow from ATP production can release stored gradient energy as heat. In endotherms, regulated uncoupling can contribute to thermoregulation. The model does not imply that every proton leak is beneficial or that all respiratory energy becomes heat. It demonstrates what happens to energy capture when some gradient dissipation is separated from ATP synthesis.",
  "The right display makes the tradeoff explicit. As more of the gradient is dissipated through the bypass, less of its potential energy is captured through ATP synthase. ATP-production efficiency falls, while heat output rises. Nia reconnects ATP synthase and lets both routes exist as possible fates for proton-motive force. The earlier yield dashboard now makes more sense. Proton leak is one reason a respiratory ATP total is not a fixed universal integer. The gradient is a real energetic intermediate whose fate depends on membrane processes, not a guaranteed packet of a predetermined number of ATP molecules.",
  "When the test ends, Nia powers down the giant mitochondrial display. A wall slides aside to reveal a much smaller cell with no mitochondrial organelle at all. The membrane is conventional and simple, yet respiratory ETC complexes and ATP synthase are embedded directly in it. Nia carries only the mechanism, not the mitochondrion, into the comparison annex. ‘If membrane chemiosmosis is the core logic,’ she says, ‘a cell does not need a mitochondrion to use that logic.’ You follow her toward the prokaryotic model."
 ],
 'close':'The uncoupling test shows that proton-motive force can be dissipated as heat when H⁺ bypasses ATP synthase. The final annex now asks whether the same electron-transfer and proton-gradient logic can operate in a cell that has no mitochondria.'
},
'U3-L50':{
 'title':'The Same Membrane Logic Without a Mitochondrion',
 'kicker':'Prokaryotes can perform respiratory electron transport and proton translocation across the plasma membrane, showing that chemiosmotic logic does not depend on a mitochondrial organelle.',
 'paragraphs':[
  "The final annex contains no mitochondrial cutaway. The prokaryotic cell has **no mitochondrial organelle**. Instead, an enlarged prokaryotic cell membrane stretches from floor to ceiling. For this scene, the **cytoplasmic side** is fixed on your **left**. The **center** is the prokaryotic plasma membrane itself, containing respiratory electron carriers, proton-translocation machinery, and ATP synthase. The **right** side is labeled external or periplasmic proton side, depending on the cell’s organization. Nia places the earlier mitochondrial cutaway on a small comparison screen but keeps it physically secondary. The question is no longer where a mitochondrion is. The question is what a membrane must do to support respiratory chemiosmosis.",
  "Reduced electron carriers feed electrons into the membrane respiratory chain. As redox transfer proceeds, proton-translocation machinery moves H⁺ away from the cytoplasmic side, creating an electrochemical gradient across the plasma membrane. H⁺ can then return through ATP synthase and drive ATP formation. Nia names the structure-function relationship **prokaryotic respiratory membrane**. In prokaryotes, electron transport and proton translocation associated with respiration occur across the plasma membrane. The machinery has a different cellular location from the eukaryotic inner mitochondrial membrane, while the broader logic of electron transfer, proton gradient formation, and ATP synthase remains recognizable.",
  "Nia turns the comparison screen sideways. On the eukaryotic model, the inner mitochondrial membrane separates matrix from intermembrane space. On the prokaryotic model, the plasma membrane separates cytoplasm from the external or periplasmic side. The labels cannot be swapped carelessly, yet both systems use membrane compartmentalization to maintain a proton-motive force. This comparison also protects an earlier distinction. Prokaryotic respiration can be aerobic or, in some organisms, use other terminal electron acceptors. That differs from fermentation, which regenerates electron carriers without operating a respiratory ETC and proton-gradient system of this kind. Fermentation waits for Journey 7.",
  "The three traces on Nia’s tablet finally collapse into a completed ledger. The amber carbon route began in organic fuel and was released as CO₂ through carbon oxidation. The blue electron route moved from fuel-derived intermediates onto NADH and FADH₂, through the respiratory ETC, and finally to a terminal acceptor, with oxygen reduced to water in the aerobic route. The red H⁺ route was created by electron-transfer-driven proton pumping, stored as proton-motive force, and spent through ATP synthase or dissipated partly as heat. ATP was produced by more than one mechanism, with substrate-level phosphorylation earlier and oxidative phosphorylation dominating the membrane-coupled harvest. The power plant is no longer one vague ‘energy-making’ room. It is a connected set of transfers that can be reconstructed from the route.",
  "Nia closes the respiration map only after you can walk it backward. Cytosolic glycolysis produces pyruvate, NADH, and net ATP. Pyruvate oxidation makes acetyl-CoA, CO₂, and NADH. The citric acid cycle in the matrix releases more CO₂ and loads NADH and FADH₂. Reduced carriers feed the inner-membrane ETC. Electron transfer builds the proton gradient. Oxygen accepts terminal electrons in aerobic respiration. Proton-motive force drives chemiosmosis through ATP synthase. The same membrane principle can operate across a prokaryotic plasma membrane. A final emergency door unlocks beyond the annex. Its sign reads OXYGEN LIMITED. The next journey will ask how cells keep glycolysis running when respiratory electron transfer cannot proceed normally."
 ],
 'close':'The Respiration Power Plant is restored. Carbon flow, electron transfer, proton pumping, oxygen reduction, ATP synthesis, heat release, and membrane location now form one causal route, and the oxygen-limited door leads directly toward fermentation and metabolic flexibility.'
},
}

TERM_IMAGES={
'U3-K-040':'the center respiration map turning fuel-derived chemical energy into a coordinated route that ultimately supports ATP synthesis',
'U3-K-042':'the three-stage center map linking cytosolic glycolysis, mitochondrial carbon oxidation, and oxidative phosphorylation',
'U3-K-145':'the net equation board showing glucose and oxygen on the input side and carbon dioxide, water, ATP-captured energy, and heat on the output side',
'U3-K-146':'three separate left intake lanes for carbohydrate-, fat-, and protein-derived respiratory fuels',
'U3-K-147':'the amber carbon ledger losing carbon as CO₂ while the blue electron ledger moves toward oxygen reduction',
'U3-K-150':'the stage map grouping glycolysis, pyruvate oxidation plus citric acid cycle, and oxidative phosphorylation',
'U3-K-049':'the right glycolysis platform holding two pyruvate, charged NADH carriers, and net ATP',
'U3-K-151':'one six-carbon glucose splitting in the cytosol into two three-carbon pyruvate molecules',
'U3-K-152':'two ATP spent at the left investment gate and four ATP appearing later for a net gain of two',
'U3-K-153':'a phosphate transferred directly from an organic substrate intermediate to ADP without ATP synthase',
'U3-K-148':'the NAD⁺ carrier closing around transferred electrons and becoming NADH',
'U3-K-149':'the FAD carrier becoming FADH₂ when loaded with electrons and protons during the citric acid cycle',
'U3-K-050':'the mitochondrial transition route linking pyruvate oxidation to later Krebs-cycle carrier reduction and CO₂ release',
'U3-K-154':'three-carbon pyruvate entering the airlock, losing CO₂, reducing NAD⁺, and leaving as a two-carbon acetyl group',
'U3-K-155':'the two-carbon acetyl group attached to a coenzyme A handle and entering the cycle',
'U3-K-051':'the mitochondrial matrix cycle venting CO₂ while ATP, NADH, and FADH₂ collect on separate shelves',
'U3-K-156':'the circular matrix pathway oxidizing acetyl-derived carbon and regenerating its acceptor',
'U3-K-157':'the small per-glucose cycle-accounting panel showing 4 CO₂, 2 ATP, 6 NADH, and 2 FADH₂ across two turns',
'U3-K-045':'the cristae-rich inner membrane providing expanded surface for respiratory ETC and ATP-synthesis machinery',
'U3-K-144':'the conventional mitochondrial cutaway keeping matrix, inner membrane, cristae, and intermembrane space distinct',
'U3-K-043':'the blue electron tracer moving from reduced carriers through the respiratory ETC toward the terminal acceptor',
'U3-K-052':'NADH and FADH₂ unloading high-energy electrons into the inner-membrane electron-transfer system',
'U3-K-159':'the series of inner-membrane redox carriers passing electrons stepwise toward a terminal acceptor',
'U3-K-044':'red H⁺ markers accumulating in the intermembrane space while the matrix becomes the lower-proton side',
'U3-K-053':'paired pH gauges showing higher pH in the matrix and lower pH in the proton-rich intermembrane space',
'U3-K-160':'selected ETC complexes using electron-transfer energy to pump H⁺ from matrix to intermembrane space',
'U3-K-161':'oxygen accepting terminal electrons and protons to form water at the end of the aerobic ETC',
'U3-K-047':'the full inner-membrane system in which electron transport establishes a gradient and proton flow through ATP synthase drives ATP formation',
'U3-K-158':'the two linked components of oxidative phosphorylation, respiratory electron transport and ATP-synthase chemiosmosis',
'U3-K-162':'H⁺ moving down an electrochemical gradient through the membrane-associated ATP synthase process',
'U3-K-163':'the membrane-spanning ATP synthase complex using proton-motive force to form ATP from ADP and inorganic phosphate',
'U3-K-164':'proton flow driving rotational and conformational changes in ATP synthase catalytic machinery',
'U3-K-165':'the variable yield dashboard showing about 26–28 ATP from oxidative phosphorylation and about 30–32 total in many eukaryotic cells',
'U3-K-048':'the center proton bypass dissipating gradient energy as heat while ATP capture falls',
'U3-K-046':'respiratory ETC and proton-translocation machinery embedded directly in a prokaryotic plasma membrane',
}

LEARNER_MEANING={
'U3-K-152':'In the bookkeeping model used here, glycolysis spends 2 ATP and produces 4 ATP by substrate-level phosphorylation, giving a net gain of 2 ATP per glucose.',
'U3-K-157':'Across the two citric-acid-cycle turns associated with one glucose in this bookkeeping model, the cycle yields 4 CO₂, 2 ATP, 6 NADH, and 2 FADH₂.',
'U3-K-165':'A useful modern estimate places oxidative phosphorylation near 26–28 ATP and total aerobic yield near 30–32 ATP per glucose in many eukaryotic cells. Exact yield varies with cell type, shuttle systems, and proton leak.'
}

CHECKPOINT_HINTS={
'U3-L40':'Return to the right side of the cytosolic splitting floor. The three output shelves separate the carbon product, the reduced electron carrier, and the net ATP payoff.',
'U3-L45':'Look to the left entrance of the inner-membrane descent. The two reduced carriers arrive carrying the same kind of cargo that moves through the center redox chain.',
'U3-L48':'Ignore the old electron path and look at the left reservoir. The immediate driving force is stored across the membrane and is released only when H⁺ passes through the center enzyme.'
}

scenes=[]
for idx,lid in enumerate(J6['route']):
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
 'schema':'memory-palace-v2-unit3-f4f-story-1.0','unit_id':'unit-3','palace_id':'U3-J6','journey_id':'U3-J6',
 'palace_name':'Respiration Power Plant','story_title':'The Power Plant With Fuel but No Power',
 'tagline':'Follow separate carbon, electron, and proton traces from cytosolic glycolysis through mitochondrial oxidation, the respiratory ETC, oxygen reduction, chemiosmosis, ATP synthase, heat release, and a prokaryotic membrane comparison.',
 'guide':GUIDE,'premise':J6['premise'],'mission':J6['mission'],
 'finale':'The power plant succeeds when fuel carbon is oxidized and released as CO₂, electrons are transferred through reduced carriers to a respiratory ETC and terminal acceptor, electron-transfer energy establishes a proton-motive force, H⁺ flow through ATP synthase supports oxidative phosphorylation, proton leak can release heat, and the same membrane logic is reconstructed across a prokaryotic plasma membrane without requiring mitochondria.',
 'estimated_minutes':34,'scene_count':len(scenes),'checkpoint_count':sum(bool(s['checkpoint']) for s in scenes),
 'learner_rule':'Follow the paired tracer system. Amber marks carbon accounting, blue marks representative electron transfer, and the red H⁺ gauge marks the proton gradient. Keep these traces separate even when one process causes the next. Quick Recall is optional during the first pass.',
 'route_orientation':'The Respiration Power Plant is a twelve-station cytosol-to-membrane route. Begin outside the mitochondrion at fuel intake and glycolysis, pause at the carrier bay, cross the pyruvate airlock into matrix carbon oxidation, orient inside the mitochondrial cutaway, descend the inner-membrane ETC, build the intermembrane proton gradient, finish terminal electron transfer at oxygen, spend proton-motive force through ATP synthase, test uncoupling, and end by rebuilding the same chemiosmotic logic across a prokaryotic plasma membrane.',
 'route':route,'scenes':scenes,'student_release':'PILOT_PREVIEW_F4F','narrative_standard':'V2-NARRATIVE-3.0-U3-F4F'
}

(U3/'journeys').mkdir(parents=True,exist_ok=True)
(U3/'journeys'/'U3-J6.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

js=[json.loads((U3/'journeys'/f'U3-J{i}.json').read_text(encoding='utf-8')) for i in range(1,6)]+[journey]
def card(j): return {k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
registry={'schema':'memory-palace-v2-unit3-f4f-registry-1.0','course_id':'ap-biology','unit_id':'unit-3','unit_title':'Cellular Energetics','narrative_standard':'V2-NARRATIVE-3.0-U3-F4F','journey_count':6,'scene_count':sum(x['scene_count'] for x in js),'checkpoint_count':sum(x['checkpoint_count'] for x in js),'guided_journeys':[card(x) for x in js]}
(U3/'journeys-f4f.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U3/'status-f4e.json').read_text(encoding='utf-8'))
status.update({'status':'F4F_JOURNEY6_POLISHED_PREVIEW','pipeline_status':'POLISHED_NARRATIVE_JOURNEYS_1_6_F4F','student_release':False,'preview_release':True,'journey_count':6,'scene_count':registry['scene_count'],'polished_journeys':6,'polished_scenes':registry['scene_count'],'polished_checkpoint_count':registry['checkpoint_count'],'narrative_story_files':6,'next_required_output':'F4G polished narrative for Journey 7 Fermentation and Metabolic Flexibility after F4F prose QA'})
(U3/'status-f4f.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(U3/'status.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; c=json.loads(cp.read_text(encoding='utf-8'))
for u in c['units']:
    if u['unit_id']=='unit-3':
        u.update({'status':'F4F_JOURNEY6_POLISHED_PREVIEW','journey_count':6,'scene_count':registry['scene_count'],'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEYS1_6_POLISHED_F4F','polished_journeys':6,'polished_scenes':registry['scene_count'],'student_release':False})
cp.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

bc=ROOT/'backend'/'content.py'; bs=bc.read_text(encoding='utf-8')
old='    if unit_id == "unit-3":\n        path=UNIT3_DIR / "journeys-f4e.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4d.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4c.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4b.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4a.json"\n        return _read_json(path)["guided_journeys"] if path.exists() else []'
new='    if unit_id == "unit-3":\n        path=UNIT3_DIR / "journeys-f4f.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4e.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4d.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4c.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4b.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4a.json"\n        return _read_json(path)["guided_journeys"] if path.exists() else []'
if old in bs: bs=bs.replace(old,new)
elif 'journeys-f4f.json' not in bs: raise RuntimeError('Could not patch Unit 3 journey registry preference to F4F')
bc.write_text(bs,encoding='utf-8')

mainp=ROOT/'backend'/'main.py'; ms=mainp.read_text(encoding='utf-8')
ms=ms.replace('0.16.0-u3-f4e','0.17.0-u3-f4f').replace('v2-apbio-0.16.0-u3-f4e','v2-apbio-0.17.0-u3-f4f')
mainp.write_text(ms,encoding='utf-8')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
files=['journeys/U3-J6.json','journeys-f4f.json','status-f4f.json']
lock={'schema':'memory-palace-v2-unit3-f4f-content-lock-1.0','unit_id':'unit-3','stage':'F4F','student_release':False,'files':{f:sha(U3/f) for f in files}}
(U3/'content-lock-f4f.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit3-f4f-release-manifest-1.0','unit_id':'unit-3','stage':'F4F','student_release':False,'preview_release':True,'polished_journeys':6,'polished_scenes':registry['scene_count'],'journey_6_records':sum(len(s['object_ids']) for s in scenes),'journey_6_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'next_stage':'F4G_JOURNEY7'}
(U3/'f4f-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Built Unit 3 F4F:',len(scenes),'scenes',sum(len(s['object_ids']) for s in scenes),'knowledge records',sum(bool(s['checkpoint']) for s in scenes),'checkpoints')
