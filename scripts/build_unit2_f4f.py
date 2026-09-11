from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
briefs=json.loads((U2/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
jbriefs=json.loads((U2/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
B={s['locus_id']:s for s in briefs if s['journey_id']=='U2-J6'}
J6=next(j for j in jbriefs if j['journey_id']=='U2-J6')

GUIDE={
 'name':'Dr. Nia Park','role':'cell-systems investigator',
 'visual':'navy field jacket, clear safety glasses, and a compact tablet displaying a transparent map of the cell',
 'story_job':'Nia keeps the route physically clear, asks you to predict what will happen, and names scientific terms only after the defining structure or action is visible.'
}

route=[
 {'scene_index':0,'locus':'Tonicity Orientation Hall','short':'Tonicity Hall','floor':'Conservatory entrance','symbol':'◫'},
 {'scene_index':1,'locus':'Isotonic Balance Pool','short':'Isotonic Pool','floor':'Balance chamber','symbol':'↔'},
 {'scene_index':2,'locus':'Hypertonic Withdrawal Chamber','short':'Hypertonic Chamber','floor':'Withdrawal chamber','symbol':'⇢'},
 {'scene_index':3,'locus':'Hypotonic Plant Greenhouse','short':'Hypotonic Greenhouse','floor':'Plant response greenhouse','symbol':'🌿'},
 {'scene_index':4,'locus':'Osmosis and Water-Potential River','short':'Water-Potential River','floor':'Glass river gallery','symbol':'Ψ'},
 {'scene_index':5,'locus':'Water-Potential Control Room','short':'Ψ Control Room','floor':'Conservatory control loft','symbol':'Σ'},
]

ZONE_COPY={
'U2-L40':[
 ('left','Hypotonic door','LOW SOLUTE','A blue glass door is labeled with an outside solution containing fewer effective nonpenetrating solute particles than the transparent reference cell in the center.'),
 ('center','Reference cell tank','CELL','One transparent reference cell sits in a sealed tank with its internal nonpenetrating-solute concentration held constant throughout the comparison.'),
 ('right','Comparison doors','ISO / HYPER','Two additional doors lead to an isotonic room and a hypertonic room, each changing the outside solution while leaving the reference cell itself unchanged.')],
'U2-L41':[
 ('left','Water entering','H₂O →','Silver water molecules continually cross the membrane from the external solution into the reference cell; the inward counter records every crossing.'),
 ('center','Reference cell','BALANCED','The transparent animal cell remains at nearly constant average volume even though individual water molecules keep crossing its plasma membrane.'),
 ('right','Water leaving','← H₂O','A matching stream of water molecules continually leaves the cell; the outward counter balances the inward counter over time.')],
'U2-L42':[
 ('left','Hypertonic solution','MORE EFFECTIVE SOLUTE','The external chamber contains a greater effective concentration of nonpenetrating solute than the animal cell interior, making the comparison visibly unequal.'),
 ('center','Shrinking animal cell','CELL ↓','The same flexible reference cell loses water and decreases in volume because it has no rigid cell wall resisting the change.'),
 ('right','Net water path','H₂O → OUT','A bright stream of water arrows points outward from the cell, showing the net result while smaller arrows still indicate molecular movement in both directions.')],
'U2-L43':[
 ('left','Swelling animal cell','ANIMAL','A membrane-bound animal cell receives net water, expands visibly, and approaches lysis because no cell wall resists continuing expansion.'),
 ('center','Turgid plant cell','PLANT','A plant cell takes in water until its contents press firmly against the cellulose wall; a pressure gauge rises as the wall resists further expansion.'),
 ('right','Plant-state comparison','TURGID ↔ PLASMOLYZED','A split panel compares the same plant cell when turgid with its hypertonic state, where water loss causes the plasma membrane to pull away from the wall.')],
'U2-L44':[
 ('left','Higher water potential','HIGH Ψ','A transparent compartment is marked with the higher total water potential; silver water molecules are free to move from this side toward the divider.'),
 ('center','Selective divider','MEMBRANE','A selectively permeable membrane separates the compartments, allowing free water to cross while the demonstration keeps selected solutes restricted.'),
 ('right','Lower water potential','LOW Ψ','The second compartment is marked with lower water potential; the net water-flow counter points toward this side while individual water molecules still move both ways.')],
'U2-L45':[
 ('left','Pressure control','Ψp','A piston and pressure gauge let Nia raise or lower the physical pressure contribution to water potential; an open beaker reference can be set to relative Ψp = 0.'),
 ('center','Water-potential console','Ψ = Ψp + Ψs','A large transparent console combines pressure potential and solute potential, while a lower display shows the solute-potential equation Ψs = −iCRT.'),
 ('right','Solute and balance controls','Ψs / HOMEOSTASIS','A solute injector makes Ψs more negative and an osmoregulation controller adjusts water and solute conditions to stabilize the modeled internal environment.')],
}

CAST={
'U2-L40':[
 ('reference cell','continuity object','a transparent animal cell with a fixed internal concentration of nonpenetrating solute','serve as the comparison point that makes every outside solution label relative rather than absolute'),
 ('solution doors','scientific parts','three color-coded glass doors containing different external nonpenetrating-solute concentrations','change only the environment around the same reference cell'),
 ('tonicity gauge','scientific instrument','a three-way meter labeled WATER GAIN, NO NET CHANGE, and WATER LOSS','translate the outside solution comparison into the cell response tonicity predicts')],
'U2-L41':[
 ('reference cell','continuity object','the same transparent animal cell from the orientation hall, now floating at stable average volume','show that stable volume can coexist with continual molecular movement'),
 ('water molecules','scientific parts','silver droplets crossing the membrane in both directions','make dynamic water exchange visible at isotonic balance'),
 ('crossing counters','scientific instruments','paired inward and outward counters displaying equal long-term rates','separate zero net water movement from zero molecular movement')],
'U2-L42':[
 ('reference cell','continuity object','the same flexible animal cell, outlined with a volume grid','shrink as net water leaves in the hypertonic environment'),
 ('external nonpenetrating solute','scientific part','dense red solute particles that remain outside the cell during the demonstration','create the hypertonic comparison without crossing the membrane'),
 ('water-flow display','scientific instrument','large net-outward arrow layered over smaller two-way molecular arrows','show net water loss without implying that every water molecule moves only outward')],
'U2-L43':[
 ('animal cell','scientific part','a flexible membrane-bound cell without a rigid wall','swell and potentially lyse as net water enters in the hypotonic environment'),
 ('plant cell','continuity object','a green plant cell with a visible plasma membrane inside a rigid cellulose wall','become turgid when incoming water presses the cell contents against the wall'),
 ('turgor gauge','scientific instrument','a pressure meter between the plant-cell contents and the wall','make turgor pressure rise as the wall resists expansion'),
 ('plasmolysis panel','scientific comparison','the same plant cell shown after water loss with its membrane pulled away from the wall','contrast plasmolysis with the turgid state and keep the directions straight')],
'U2-L44':[
 ('free water','scientific part','silver water molecules that can cross the selectively permeable divider','move net from higher total water potential toward lower total water potential'),
 ('selectively permeable membrane','scientific part','a transparent divider that permits water movement while restricting selected solute particles','create the membrane condition required for the osmosis demonstration'),
 ('water-potential markers','scientific instrument','large Ψ displays showing HIGH on the left and LOW on the right','replace the oversimplified more-solute slogan with the general directional rule'),
 ('reference and plant cells','continuity objects','miniature versions of the cells from the previous chambers placed beside the river','connect the river rule back to the swelling, shrinking, and turgor outcomes already observed')],
'U2-L45':[
 ('pressure-potential piston','scientific instrument','a movable piston connected to a gauge labeled Ψp','change the physical pressure component of total water potential'),
 ('solute injector','scientific instrument','a calibrated injector adding dissolved solute beside a display labeled Ψs','show that adding solute makes solute potential more negative'),
 ('water-potential console','scientific instrument','a central illuminated equation board reading Ψ = Ψp + Ψs and Ψs = −iCRT','combine the two components and make the quantitative relationships explicit'),
 ('osmoregulation controller','scientific system','a feedback panel adjusting water and solute balance around a transparent model cell','show active regulation of internal water balance and solute composition')],
}

NARR={
'U2-L40':{
 'title':'A label that means nothing without the cell','kicker':'The three solution doors look confidently labeled until Nia moves the same cell in front of them and makes the labels depend on the comparison.',
 'paragraphs':[
  'The glass doors of the **Osmosis Conservatory** slide apart and warm, humid air rolls over you. Condensation beads on every surface. Straight ahead, a transparent animal cell floats in a cylindrical tank at the center of a circular hall. Its internal solute particles glow amber and stay fixed at the same concentration. Three doors surround it. The left door opens onto a pale-blue solution with relatively few red nonpenetrating solute particles. On the right are two more doors, one containing an outside solution matched to the cell and another packed with many more red particles. Above the doors, however, someone has bolted the labels HYPOTONIC, ISOTONIC, and HYPERTONIC directly onto the glass as though the words were permanent properties of the beakers.',
  'Dr. Nia Park stops before the labels instead of opening a door. “These words only make sense when we know what the solution is being compared with,” she says. She locks the composition of the center reference cell, then rolls the entire tank toward the pale-blue chamber. The external solution now contains a lower effective concentration of nonpenetrating solute than the cell interior. A gauge predicts net water entry. Nia calls that outside solution **hypotonic relative to this cell**. She returns the same cell to the center and aligns it with the matched chamber. The gauge settles at no net water change. That external solution is **isotonic relative to the cell**. Then she moves the same unchanged cell beside the concentrated red chamber. The gauge predicts net water loss. That solution is **hypertonic relative to the cell**.',
  'The important feature is not the color of the door or the amount of solute in isolation. It is the relationship between the external solution and the cell interior, especially the concentration of solutes that do not freely cross the membrane during the comparison. An outside solution may therefore be hypotonic, isotonic, or hypertonic **relative to a particular cell interior**. Nia pulls the permanent labels off the doors and replaces them with magnetic labels that only snap into place after the reference cell is positioned beside the chamber.',
  'A second dial beneath the tank lights up. It does not ask, “How salty is this beaker?” It asks, “What will happen to the cell’s water?” Nia names the idea **tonicity**. Tonicity describes how a solution containing nonpenetrating solutes causes a cell to gain or lose water. The left chamber predicts water gain, the matched chamber predicts no net water movement, and the concentrated chamber predicts water loss. You now have one stable reference point: the cell stays the same while the outside solution changes.',
  'The matched chamber opens with a soft hiss. Nia pushes the transparent reference tank through first. “Start with the condition that looks least dramatic,” she says. “It hides one of the most common mistakes.” Beyond the door, water arrows are already moving in both directions around a cell whose volume seems perfectly steady.'
 ],
 'close':'The conservatory’s first rule is relational. Hypotonic, isotonic, and hypertonic describe an external solution relative to a cell, and tonicity predicts whether that cell tends to gain water, lose water, or have no net water change.',
 'images':{
  'Tonicity relationships':'the same transparent reference cell rolled beside three different external solution doors so the label changes with the comparison',
  'Tonicity':'the three-way gauge under the same cell predicting WATER GAIN, NO NET CHANGE, or WATER LOSS'
 }},
'U2-L41':{
 'title':'A still cell with moving water','kicker':'The cell looks motionless, but paired counters reveal that water is crossing the membrane continuously in both directions.',
 'paragraphs':[
  'The **Isotonic Balance Pool** is almost silent. The same transparent reference cell floats in the center at the same volume it had in the orientation hall. On the left, silver water molecules cross inward through the plasma membrane. On the right, other silver water molecules cross outward. Two counters click above the tank. At first your eyes are drawn to the stable outline of the cell, and the scene could easily be mistaken for one in which nothing is happening.',
  'Nia dims the room until only the moving water molecules remain bright. They do not pause at the membrane. One passes inward. Another passes outward. Several more follow from both sides. The inward counter climbs, and the outward counter climbs with it. Over time the rates balance closely enough that the average amount of water inside the cell remains stable. There is **no net water movement**, but there is constant molecular exchange.',
  'Only after the two-way motion is unmistakable does Nia name the condition. The cell is in an **isotonic solution**. In an isotonic environment, water continues moving across the membrane in both directions, yet the opposing movements balance so there is no net change in water volume on average. The cell therefore maintains approximately the same volume without requiring water molecules to freeze in place.',
  'Nia reaches behind the cell and turns off a misleading display that had shown a giant STOP sign over the membrane. “No net movement is not the same as no movement,” she says. She replaces it with two arrows of equal thickness pointing in opposite directions. The cell’s size remains steady because the flows balance, not because osmosis has stopped.',
  'A warning light appears over the next chamber. The outside solution there contains a greater effective concentration of nonpenetrating solute than the cell interior. The balanced arrows on the wall tilt toward the outside. Nia keeps the same reference cell with you as the door opens, making the coming change impossible to blame on a different cell.'
 ],
 'close':'Isotonic balance is dynamic. Water molecules keep crossing both directions while the average inward and outward rates balance, producing no net water movement and little change in cell volume.',
 'images':{'Isotonic solution':'the same cell holding steady while equal inward and outward water counters continue climbing'}},
'U2-L42':{
 'title':'When the outside pulls the balance outward','kicker':'The cell shrinks because the net water balance shifts outward, not because every water molecule suddenly moves in only one direction.',
 'paragraphs':[
  'The door seals behind you in the **Hypertonic Withdrawal Chamber**. The same animal cell is suspended at center, its starting outline traced by a white grid. On the left, the external solution is crowded with red nonpenetrating solute particles. On the right, a broad arrow points from the cell toward the external chamber. Smaller silver arrows still flicker both inward and outward across the membrane, but the outward counter now climbs faster.',
  'Nia asks you to watch the cell boundary rather than the solute particles. Water leaves the cell in greater net amount than it enters. The flexible membrane pulls inward. The cell’s volume decreases, and the white starting grid remains behind like the outline of a larger ghost. The outside solution is **hypertonic relative to the cell**, and a cell in a hypertonic environment loses water. In an animal cell, that net water loss causes the cell to shrink.',
  'The red solute particles never grab water molecules or drag them through the membrane. The visual cause is the imbalance in water movement produced by the conditions on the two sides. Nia keeps small two-way arrows visible under the large net-outward arrow so the scene does not turn into another all-or-none picture. Hypertonic describes the relationship that produces net water loss from this cell.',
  'A red skull icon appears automatically on an old control panel the moment the cell shrinks. Nia switches it off. “Water loss is stressful, but shrinking does not mean every cell dies instantly,” she says. The outcome depends on degree, duration, cell type, and physiological context. She then slides a green plant-cell model onto the side bench. Under a hypertonic condition, its plasma membrane begins to pull away from its rigid wall. Nia does not name that event yet. “Keep this image,” she says. “We will compare it with what the same plant cell does when water enters.”',
  'The next greenhouse door glows pale blue. The outside solution beyond it contains fewer effective nonpenetrating solutes than the cells inside. You carry the shrinking-animal-cell image with you as Nia opens the door to a chamber where water balance will reverse.'
 ],
 'close':'Hypertonic conditions shift the net water balance out of the cell. Animal cells shrink as water is lost, while plant cells can show a distinctive membrane-withdrawal response that the next greenhouse will make explicit.',
 'images':{'Hypertonic solution':'the transparent animal cell shrinking inside its original white outline while a large net water arrow points outward and smaller arrows still move both ways'}},
'U2-L43':{
 'title':'The same incoming water, two different boundaries','kicker':'Water enters both cells, but only the plant cell has a rigid wall that can turn swelling into supportive pressure.',
 'paragraphs':[
  'The **Hypotonic Plant Greenhouse** is divided into three bright bays. On the left floats an animal cell with only its plasma membrane outlining the boundary. At center stands a green plant cell with a visible plasma membrane tucked just inside a rigid cellulose wall. On the right, a comparison panel holds two images of that same plant cell: one full and firm, the other with its membrane peeled inward from the wall. The external solution in the entire greenhouse contains a lower effective concentration of nonpenetrating solute than the cell interiors.',
  'Silver water molecules begin entering both cells in net amount. The animal cell on the left swells. Its membrane stretches outward because there is no cell wall to provide rigid resistance. Nia lets the model continue only until a warning line appears. In sufficiently hypotonic conditions, animal cells can swell severely and may lyse. She freezes it before the demonstration ruptures. The plant cell at center receives the same net direction of water movement, but its behavior diverges.',
  'As water enters the plant cell, the plasma membrane and cell contents press outward against the rigid wall. The wall resists further expansion. A pressure gauge between the cell contents and wall rises steadily. The cell becomes firm instead of bursting in the ordinary demonstration. Nia names the outside condition **hypotonic** relative to these cells. A cell in a hypotonic environment gains water; animal cells can swell and lyse, while a healthy plant cell becomes **turgid** because its wall resists expansion.',
  'The rising pressure has a name too. **Turgor pressure** is generated as water enters a plant cell and the cell contents press against the cell wall. That pressure helps support nonwoody plant tissues. Nia touches the right-hand comparison panel and reverses the water balance. Water now leaves the plant cell. The cell contents shrink inward, and the plasma membrane pulls away from the cell wall. This is **plasmolysis**. Plasmolysis is therefore a water-loss response associated with a hypertonic environment, not the swelling response you are watching in the hypotonic greenhouse.',
  'For a moment the two plant states remain side by side: turgid, with the membrane pressed against the wall; plasmolyzed, with the membrane pulled away. Nia draws one line between them and labels it WATER BALANCE. “The tonicity rooms tell us what happens,” she says. “Now we need the general rule that tells us why water moves in the direction it does.” A glass channel opens beneath the floor and becomes a transparent river leading deeper into the conservatory.'
 ],
 'close':'Hypotonic water entry exposes the importance of the boundary. Animal cells swell without a wall, while plant cells develop turgor pressure as the wall resists expansion; water loss in a plant cell can instead produce plasmolysis.',
 'images':{
  'Hypotonic solution':'an animal cell swelling on the left while the plant cell at center gains water but becomes firm against its wall',
  'Plasmolysis':'the plant comparison panel showing the plasma membrane pulled inward away from the cell wall after water loss',
  'Turgor pressure':'the pressure gauge rising between the water-filled plant-cell contents and the resisting cell wall'
 }},
'U2-L44':{
 'title':'Replace the solute slogan with the water-potential rule','kicker':'The river makes the general rule visible: water moves net from higher total water potential toward lower total water potential.',
 'paragraphs':[
  'You descend onto a bridge over the **Osmosis and Water-Potential River**. The river is actually two transparent compartments separated by a selectively permeable membrane. On the left, a large display reads HIGH Ψ. On the right, another reads LOW Ψ. Silver water molecules cross the divider in both directions, just as they did around the isotonic cell, but the net-flow counter points from the higher-Ψ side toward the lower-Ψ side.',
  'Nia places the animal and plant cells from the previous chambers beside the bridge. “You have probably heard a shortcut that water moves toward more solute,” she says. She leaves that slogan on a small sign, then raises a pressure piston under one side of the river. The shortcut sign begins flashing ERROR. The direction of water movement cannot always be predicted from solute concentration alone when pressure also differs. She turns your attention back to the two Ψ displays.',
  'The general rule is **water potential**. Water moves by osmosis from regions of higher water potential toward regions of lower water potential. Nia names the process **osmosis** only after the free-water movement is visible: osmosis is the net diffusion of free water across a selectively permeable membrane from higher water potential toward lower water potential. The membrane is essential to the demonstration, and it is water, not the restricted solute, that is moving in the process being named.',
  'Nia now returns the pressure conditions on the two sides to equality. Under that restricted comparison, adding more dissolved solute lowers the water potential of that side. Water therefore tends to move from the lower-solute, lower-osmolarity side toward the higher-solute, higher-osmolarity side. That **osmolarity direction** is useful when the other components are equal. It explains why the tonicity chambers often look like “water moves toward more solute.” The larger water-potential rule remains the one that survives when pressure is changed.',
  'The river passes under miniature cell membranes where molecules move continually to maintain growth and internal conditions. Nia points out that **growth and homeostasis depend on continual movement of molecules across membranes**. The same membrane traffic you have followed through the transport hub and conservatory is therefore not a one-time event. It is part of maintaining a living system. A staircase rises beside the lower-Ψ compartment toward the conservatory control loft. There, two separate knobs labeled PRESSURE and SOLUTE wait beside a single total-Ψ display.'
 ],
 'close':'Osmosis follows the general water-potential rule: free water moves net across a selectively permeable membrane from higher Ψ toward lower Ψ. Solute concentration is a useful directional clue only when the other contributors to water potential are held equal.',
 'images':{
  'Osmosis and water potential':'silver water moving net across the divider from the HIGH Ψ compartment to the LOW Ψ compartment',
  'Osmolarity direction':'with equal pressure, extra solute lowering the destination-side water potential so net water movement goes toward the higher-osmolarity side',
  'Osmosis':'free water crossing the selectively permeable divider while restricted solute remains in place',
  'Membrane movement and homeostasis':'miniature cell membranes beside the river with continual molecular traffic supporting stable internal conditions'
 }},
'U2-L45':{
 'title':'Two controls determine where the water goes','kicker':'The final console separates pressure from solute so total water potential can be predicted instead of guessed from concentration alone.',
 'paragraphs':[
  'The stairs end in the **Water-Potential Control Room**, a glass loft directly above the river. The left wall holds a piston and pressure gauge labeled Ψp. The center console glows with the equation **Ψ = Ψp + Ψs**. On the right, a calibrated solute injector sits beside a second display labeled Ψs. Beneath the main equation is another formula, **Ψs = −iCRT**. The transparent reference cell and plant cell are visible in a lower chamber, waiting for the control system to restore their water balance.',
  'Nia begins with the pressure side. She places an open beaker at atmospheric pressure under the gauge and sets its relative **pressure potential**, Ψp, to zero by convention. Then she lowers a piston onto a sealed chamber. The pressure gauge rises, and the total water-potential display changes even though the solute concentration has not. Pressure potential is the physical pressure component of water potential. It is not always zero; zero is the conventional relative value for an open beaker at atmospheric pressure.',
  'Next she resets the pressure and activates the solute injector. Dissolved solute enters the right-hand chamber. The Ψs display becomes more negative. This component is **solute potential**. Pure water has Ψs = 0 under the standard convention, while adding dissolved solute lowers solute potential into negative values. The lower display expands the relationship into **Ψs = −iCRT**. Nia points to each symbol: *i* is the ionization or van’t Hoff factor, *C* is molar concentration, *R* is the pressure constant used with the equation, and *T* is absolute temperature in kelvin. The negative sign remains fixed at the front of the expression.',
  'Now the two controls operate together. The console adds the physical-pressure contribution and the solute contribution using the **water potential equation**, Ψ = Ψp + Ψs. Nia sets a demonstration chamber to Ψp = +0.3 MPa and Ψs = −0.7 MPa. The total display reads Ψ = −0.4 MPa. A neighboring chamber reads −0.8 MPa. The river indicator points from −0.4 MPa toward −0.8 MPa because −0.4 is the higher water potential. The numerical example makes the direction rule from the river concrete without changing it.',
  'At the far right, the osmoregulation controller begins cycling. It adjusts water and solute conditions around the model cell while monitoring the internal environment. Nia names the broader process **osmoregulation**. Osmoregulation maintains water balance and permits control of internal solute composition and water potential. In living organisms, the specific organs, transporters, and behaviors vary enormously, but the control problem is recognizable: keep water and dissolved substances within ranges compatible with cellular function.',
  'The warning lights across the conservatory go dark one by one. The isotonic pool continues its two-way water exchange. The hypertonic chamber no longer mistakes shrinkage for instant death. The plant greenhouse keeps turgid and plasmolyzed states distinct. The river follows total water potential, and the control room no longer ignores pressure. Nia closes the reference-cell tank and looks through the glass toward a dark archive beyond the greenhouse. “We can now predict movement across membranes,” she says. “The last Unit 2 journey asks why cells divide their interiors into compartments at all, and what evidence tells us where two of the most important compartments came from.”'
 ],
 'close':'The conservatory stabilizes when both contributors to water potential are visible. Pressure potential and solute potential combine to determine total Ψ, and osmoregulation uses water and solute control to maintain a workable internal environment.',
 'images':{
  'Water potential equation':'the center console adding the pressure gauge value Ψp to the solute display Ψs to produce total Ψ',
  'Solute potential equation':'the illuminated formula Ψs = −iCRT with the negative sign fixed and i, C, R, and T individually labeled',
  'Pressure potential':'the Ψp piston changing total water potential while solute concentration stays unchanged',
  'Solute potential':'the solute injector making the Ψs display more negative as dissolved solute is added',
  'Osmoregulation':'the feedback controller adjusting water and solute conditions around the transparent cell until internal readings stabilize'
 }},
}

SCENE_META={
'U2-L40':('Tonicity Orientation Hall','Conservatory entrance','Tonicity Orientation Hall, the circular conservatory entrance where a pale hypotonic chamber is fixed on your left, the unchanged transparent reference cell sits at center, and isotonic and hypertonic comparison doors remain fixed on your right.'),
'U2-L41':('Isotonic Balance Pool','Balance chamber','Isotonic Balance Pool, a quiet glass chamber where water enters from the left, the same transparent reference cell remains centered at stable average volume, and a matching stream of water exits to the right.'),
'U2-L42':('Hypertonic Withdrawal Chamber','Withdrawal chamber','Hypertonic Withdrawal Chamber, where the concentrated external solution occupies the left side, the same animal cell shrinks at center inside its original outline, and the net water-flow display points outward on the right.'),
'U2-L43':('Hypotonic Plant Greenhouse','Plant response greenhouse','Hypotonic Plant Greenhouse, a three-bay room with a swelling animal cell on the left, a turgid plant cell pressing against its wall at center, and a turgid-versus-plasmolyzed plant comparison fixed on the right.'),
'U2-L44':('Osmosis and Water-Potential River','Glass river gallery','Osmosis and Water-Potential River, a transparent two-compartment channel where the higher-water-potential reservoir is on the left, the selectively permeable divider is centered beneath the bridge, and the lower-water-potential reservoir is on the right.'),
'U2-L45':('Water-Potential Control Room','Conservatory control loft','Water-Potential Control Room, the loft above the river where the Ψp pressure piston is fixed on the left, the equations Ψ = Ψp + Ψs and Ψs = −iCRT fill the center console, and solute/osmoregulation controls occupy the right wall.'),
}

CHECKPOINT_HINTS={
'U2-L40':'Picture the same transparent reference cell rolling in front of three different solution doors. The cell does not change, but the outside nonpenetrating-solute concentration changes, and the water-gain/loss gauge changes with that relationship.',
'U2-L44':'Return to the glass river. The left reservoir is marked HIGH Ψ, the right reservoir LOW Ψ, and silver water crosses the selective divider in both directions while the net-flow counter points from the higher Ψ side toward the lower Ψ side.'
}

lids=[f'U2-L{i}' for i in range(40,46)]
scenes=[]
for idx,lid in enumerate(lids):
    b=B[lid]; n=NARR[lid]; locus,floor,locdesc=SCENE_META[lid]
    zones=[{'position':pos,'label':lab,'symbol':sym,'description':desc} for pos,lab,sym,desc in ZONE_COPY[lid]]
    cast=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    cast += [{'name':name,'kind':kind,'visual':visual,'job':job} for name,kind,visual,job in CAST[lid]]
    beats=[]; snaps=[]
    for t in b['term_introductions']:
        image=n['images'].get(t['canonical_term'], b['science_bearing_action']['during'][0])
        beats.append({'object_id':t['knowledge_id'],'term':t['canonical_term'],'story':image,'science':t['canonical_science'],'exact_name':t['exact_name_recall'],'hint':image})
        snaps.append({'term':t['canonical_term'],'meaning':t['canonical_science'],'image':image})
    qr=b['quick_recall']; checkpoint=bool(qr.get('enabled'))
    next_id=b['causal_transition']['to_locus_id']
    scenes.append({
      'scene_index':idx,'locus':locus,'title':n['title'],'scene_kicker':n['kicker'],'location_description':locdesc,
      'scene_layout':{'orientation':b['orientation_sentence'],'zones':zones},'cast':cast,
      'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':beats,'memory_snapshot':snaps,
      'checkpoint':checkpoint,'checkpoint_object_id':b['primary_knowledge_id'],'checkpoint_prompt':qr.get('candidate_prompt','') if checkpoint else '',
      'checkpoint_answer':qr.get('answer','') if checkpoint else '','checkpoint_hint':CHECKPOINT_HINTS.get(lid,'') if checkpoint else '',
      'next_locus':B[next_id]['scene_title'] if next_id in B else None,'misconception_guards':b['misconception_guards'],
      'required_visual':b['visual_spec'],'carry_forward':b['carry_forward']
    })

journey={
 'schema':'memory-palace-v2-unit2-f4f-story-1.0','unit_id':'unit-2','palace_id':'U2-J6','journey_id':'U2-J6','palace_name':'Osmosis Conservatory',
 'story_title':'The Conservatory That Could Not Hold Its Water','tagline':'Carry the same reference cells through changing solutions, watch water balance reshape them, then climb to the control room where pressure and solute together reveal the general water-potential rule.',
 'guide':GUIDE,'premise':J6['premise'],'mission':J6['mission'],
 'finale':'The conservatory stabilizes when solution labels become relative comparisons, isotonic balance stays dynamic, plant and animal boundaries produce different outcomes, osmosis follows total water potential, and pressure plus solute are treated as separate contributors that cells and organisms must regulate.',
 'estimated_minutes':15,'scene_count':len(scenes),'checkpoint_count':sum(bool(s['checkpoint']) for s in scenes),
 'learner_rule':'Read or listen and keep the transparent reference cell and plant cell with you. First notice which way the net water balance shifts and what boundary the cell has. Use concentration as a clue only when the pressure conditions are comparable. Quick Recall is optional during the first pass.',
 'route_orientation':'The Osmosis Conservatory is one connected glass greenhouse. Begin in the circular Tonicity Orientation Hall, enter the isotonic pool, then the hypertonic withdrawal chamber and hypotonic plant greenhouse. A glass river beneath the greenhouse reveals the general water-potential rule, and stairs from that river lead directly to the final control loft where pressure and solute contributions to Ψ can be changed separately.',
 'route':route,'scenes':scenes,'student_release':'PILOT_PREVIEW_F4F','narrative_standard':'V2-NARRATIVE-3.0-F4F'
}

(U2/'journeys').mkdir(parents=True,exist_ok=True)
(U2/'journeys'/'U2-J6.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

js=[json.loads((U2/'journeys'/f'U2-J{i}.json').read_text(encoding='utf-8')) for i in range(1,6)]+[journey]
def card(j): return {k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
registry={'schema':'memory-palace-v2-unit2-f4f-registry-1.0','course_id':'ap-biology','unit_id':'unit-2','unit_title':'Cells','narrative_standard':'V2-NARRATIVE-3.0-F4F','journey_count':6,'scene_count':sum(j['scene_count'] for j in js),'checkpoint_count':sum(j['checkpoint_count'] for j in js),'guided_journeys':[card(j) for j in js]}
(U2/'journeys-f4f.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U2/'status-f4e.json').read_text(encoding='utf-8'))
status.update({'status':'F4F_JOURNEY6_POLISHED_PREVIEW','pipeline_stage':'POLISHED_NARRATIVE_JOURNEY6_F4F','student_release':False,'preview_release':True,'polished_journeys':6,'polished_scenes':45,'polished_checkpoint_count':15,'narrative_story_files':6,'next_required_output':'F4G polished narrative for Journey 7 after F4F prose QA and developer/classroom review','next_gate':'F4G polish Journey 7 only after F4F prose QA and developer/classroom review'})
(U2/'status-f4f.json').write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; c=json.loads(cp.read_text(encoding='utf-8'))
for u in c['units']:
    if u['unit_id']=='unit-2':
        u.update({'status':'F4F_JOURNEY6_POLISHED_PREVIEW','journey_count':6,'scene_count':45,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEYS1_6_POLISHED_F4F','polished_journeys':6,'polished_scenes':45})
cp.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
files=['journeys/U2-J6.json','journeys-f4f.json','status-f4f.json']
lock={'schema':'memory-palace-v2-unit2-f4f-content-lock-1.0','unit_id':'unit-2','stage':'F4F','student_release':False,'files':{f:sha(U2/f) for f in files}}
(U2/'content-lock-f4f.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit2-f4f-release-manifest-1.0','unit_id':'unit-2','stage':'F4F','student_release':False,'preview_release':True,'polished_journeys':6,'polished_scenes':45,'journey_6_records':sum(len(s['object_ids']) for s in scenes),'journey_6_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'next_stage':'F4G_JOURNEY7'}
(U2/'f4f-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Built Unit 2 F4F:',len(scenes),'Journey 6 scenes',sum(len(s['object_ids']) for s in scenes),'knowledge records',sum(bool(s['checkpoint']) for s in scenes),'checkpoints')
