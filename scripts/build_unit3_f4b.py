from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content'/'ap-biology'/'unit-3'
briefs=json.loads((U3/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
jbriefs=json.loads((U3/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
B={s['locus_id']:s for s in briefs if s['journey_id']=='U3-J2'}
J2=next(j for j in jbriefs if j['journey_id']=='U3-J2')

GUIDE={
 'name':'Dr. Nia Park',
 'role':'cellular-energetics investigator',
 'visual':'navy field jacket, clear safety glasses, and a compact tablet showing enzyme shape, reaction-rate, and pathway-control models',
 'story_job':'Nia keeps the control-wing geography fixed, changes one variable at a time, asks you to diagnose the cause of each rate change, and names scientific terms after the mechanism is visible.'
}

route=[
 {'scene_index':0,'locus':'Enzyme Stability Chamber','short':'Stability Chamber','floor':'Control wing entrance','symbol':'⌁'},
 {'scene_index':1,'locus':'Collision and Saturation Track','short':'Saturation Track','floor':'Rate-testing corridor','symbol':'↗'},
 {'scene_index':2,'locus':'Cofactor Assembly Station','short':'Cofactor Station','floor':'Assembly bay','symbol':'⊕'},
 {'scene_index':3,'locus':'Competitive Inhibitor Gate','short':'Competitive Gate','floor':'Active-site checkpoint','symbol':'⇥'},
 {'scene_index':4,'locus':'Allosteric Control Panel','short':'Allosteric Panel','floor':'Regulation console','symbol':'⌘'},
 {'scene_index':5,'locus':'Cooperative Binding Array','short':'Cooperative Array','floor':'Linked-subunit gallery','symbol':'⛓'},
 {'scene_index':6,'locus':'Feedback Loop Control Room','short':'Feedback Room','floor':'Pathway control center','symbol':'↩'},
 {'scene_index':7,'locus':'Irreversible Inhibition Lockout','short':'Lockout Bay','floor':'Recovery bay','symbol':'⛔'},
]

ZONE_COPY={
'U3-L04':[
 ('left','Temperature control','°C','A fixed temperature dial holds the reference enzyme at its optimum, then moves toward colder and hotter conditions while the enzyme remains in the center monitor.'),
 ('center','Enzyme structure monitor','⌁','A transparent folded enzyme shows its active-site geometry and overall conformation while catalytic output is measured beneath it.'),
 ('right','pH and chemical-environment control','pH','A pH panel changes hydrogen-ion conditions independently and includes a recovery setting that can restore ordinary conditions after the stress test.')],
'U3-L05':[
 ('left','Substrate concentration feeder','◆◆','Amber substrate enters from a calibrated feeder whose concentration can be raised while the amount of enzyme stays fixed.'),
 ('center','Reaction-rate conveyor','↗','Identical transparent enzymes process substrate along a central conveyor while a rate graph rises and eventually approaches a ceiling.'),
 ('right','Temperature and collision control','⇆','A separate temperature dial changes molecular speed below the damaging range so collision-frequency effects can be distinguished from substrate saturation.')],
'U3-L06':[
 ('left','Protein component','E','A folded enzyme protein sits inactive with an empty helper-binding position clearly visible on its surface.'),
 ('center','Helper-binding assembly bench','⊕','Removable inorganic and organic helper models can be placed into the enzyme assembly one at a time while catalytic activity is tested.'),
 ('right','Active holoenzyme output','✓','The completed active enzyme complex moves to a green output platform only when its required nonprotein helper is associated correctly.')],
'U3-L07':[
 ('left','Substrate lane','◆','Amber substrate molecules approach the enzyme active site from the left in an adjustable stream.'),
 ('center','Shared active-site gate','⊂','One enzyme active site can be occupied by either the substrate or a similarly fitting reversible competitor, never both at the same instant.'),
 ('right','Competitive inhibitor lane','◇','A look-alike inhibitor enters from the right and repeatedly competes with substrate for the same active-site pocket.')],
'U3-L08':[
 ('left','Active-site reaction zone','⊂','The substrate-binding pocket remains visible on the left side of the same transparent enzyme so its activity can be watched while regulation occurs elsewhere.'),
 ('center','Enzyme body','⌁','The enzyme spans the center console and visibly shifts between more-active and less-active conformations.'),
 ('right','Allosteric regulatory site','●','A separate regulatory pocket on the right accepts activator or inhibitor molecules without occupying the substrate-binding active site.')],
'U3-L09':[
 ('left','First binding site','1','The first substrate-binding site sits on the left subunit of one linked multisubunit enzyme complex.'),
 ('center','Linked subunit array','⛓','Several protein subunits remain physically connected, allowing a conformational change in one part of the complex to propagate across the array.'),
 ('right','Later binding sites','2 3 4','The remaining active sites change their binding behavior after the first substrate binds on the left.')],
'U3-L10':[
 ('left','Pathway input and early enzyme','A→','A starting substrate enters an early regulatory enzyme before moving into the central sequence of metabolic reactions.'),
 ('center','Multi-step metabolic pathway','→→→','A visible chain of enzyme-catalyzed steps converts the starting material through intermediates toward one final product.'),
 ('right','End-product feedback line','↩','Accumulating final product enters a return channel that leads back to the earlier regulatory enzyme and decreases pathway flow.')],
'U3-L11':[
 ('left','Functional reference enzyme','✓','An untreated transparent enzyme continues catalysis normally and provides a side-by-side recovery reference.'),
 ('center','Persistently inhibited enzyme','⛔','A second enzyme receives a persistent inhibitor interaction and remains inactive after the surrounding inhibitor is washed away.'),
 ('right','Recovery test','↻','Fresh substrate, ordinary temperature, ordinary pH, and clean solution are restored, yet the treated enzyme still fails to resume catalysis.')],
}

CAST={
'U3-L04':[
 ('transparent reference enzyme','continuity object','a clear folded enzyme with its active-site pocket outlined in amber and a green activity lamp below it','remain the same enzyme system while temperature and pH are changed independently'),
 ('temperature dial','scientific control','a blue-to-red calibrated dial mounted permanently on the left wall','change molecular temperature while keeping the enzyme visible in the center'),
 ('pH control','scientific control','a numbered acid-to-base slider mounted permanently on the right wall','change the chemical environment and restore the starting pH during recovery tests')],
'U3-L05':[
 ('transparent reference enzyme','continuity object','the recovered enzyme from the stability chamber, now repeated in identical copies along the central conveyor','hold enzyme concentration fixed while substrate and temperature variables are tested'),
 ('amber substrate','scientific input','small amber molecular models entering from the left concentration feeder','provide the reactant whose abundance changes collision frequency and active-site occupancy'),
 ('rate graph','scientific output','a live graph above the conveyor plotting reaction rate as conditions change','show rising reaction rate and the plateau that appears when available active sites are saturated')],
'U3-L06':[
 ('enzyme protein component','scientific part','a folded protein with an empty helper-binding position and no catalytic output','show that some enzyme proteins require a nonprotein helper before the complete complex is active'),
 ('metal-ion helper','scientific part','a small inorganic ion model that fits one helper position on the assembly bench','represent an inorganic cofactor'),
 ('organic helper','scientific part','an organic molecular helper tagged as vitamin-derived on the comparison tray','represent a coenzyme, which is an organic cofactor')],
'U3-L07':[
 ('amber substrate','continuity object','the same amber substrate stream used on the saturation track','compete for access to the enzyme active site'),
 ('reversible competitor','scientific comparison','a pale molecular model with enough active-site compatibility to occupy the same pocket temporarily','reduce substrate access by reversibly occupying the active site'),
 ('shared active site','scientific structure','one pocket in the transparent enzyme at the center gate','make active-site competition physically explicit')],
'U3-L08':[
 ('transparent reference enzyme','continuity object','the same enzyme with its active site glowing on the left and a separate regulatory pocket glowing on the right','show how regulation at one site changes activity at another'),
 ('allosteric activator','regulatory molecule','a green regulator that binds the right-side regulatory pocket','stabilize a more active enzyme conformation'),
 ('allosteric inhibitor','regulatory molecule','a red regulator that binds the same separate regulatory region in the comparison test','stabilize a less active enzyme conformation without occupying the active site')],
'U3-L09':[
 ('multisubunit enzyme','scientific structure','four linked protein subunits arranged in one conventional enzyme complex with four visible active sites','transmit a binding-associated conformational change across connected subunits'),
 ('first substrate','scientific input','one amber substrate approaching the leftmost active site','trigger the first binding event'),
 ('later substrates','scientific inputs','additional amber substrates waiting beside the right-side active sites','reveal how the first binding event changes later binding behavior')],
'U3-L10':[
 ('early regulatory enzyme','scientific structure','the first major control enzyme at the left entrance of a multi-step pathway','adjust pathway flow when a downstream product feeds back'),
 ('pathway intermediates','scientific process','distinct molecular products passed from one central enzyme-catalyzed step to the next','make the pathway a sequence rather than one single reaction'),
 ('final product','continuity output','a blue product accumulating at the right end of the pathway','feed back to the earlier regulatory enzyme when enough product has accumulated')],
'U3-L11':[
 ('functional reference enzyme','scientific control','an untreated transparent enzyme with a working active site and green activity lamp','show what recovery looks like under ordinary conditions'),
 ('treated enzyme','scientific comparison','an otherwise identical enzyme carrying a persistent inhibitor interaction and a dark activity lamp','test whether activity returns after inhibitor removal'),
 ('washout and recovery station','scientific control','a clean-solution rinse followed by fresh substrate and restored temperature and pH','distinguish persistent irreversible inhibition from reversible inhibition or a reversible environmental disturbance')],
}

NARR={
'U3-L04':{
 'title':'The Enzyme That Lost Its Shape',
 'kicker':'The control wing blames every slowdown on temperature. The transparent enzyme lets you see when that explanation is actually true.',
 'paragraphs':[
  "You leave the catalytic workshop through a narrow service door and enter the **Enzyme Stability Chamber**. A transparent version of the same enzyme is clamped directly ahead at chest height, its folded outline lit in pale green and its active-site pocket traced in amber. The room is easy to redraw. On your **left** is one large temperature dial. Directly **ahead** is the enzyme-shape monitor and a reaction counter. On your **right** is a pH slider beside a recovery switch. Every alarm in the wing is flashing at once, yet Nia covers all but these three controls. ‘One variable at a time,’ she says. ‘First we find out whether the protein itself has changed.’",
  "At the starting setting, substrate reaches the active site and products leave at a steady pace. A green line marks the enzyme’s current three-dimensional conformation. Nia nudges the temperature away from the setting where this enzyme works fastest. The rate changes. She then pushes the temperature much farther. The green structural outline begins to distort, the active-site geometry shifts, and catalytic output falls sharply. Nia points to the shape monitor before naming the relationship. Nia names that visible link a **structure-function disruption**. A change in molecular **structure** can change enzyme **function** or efficiency. When temperature, pH, or another chemical condition disrupts the interactions that help maintain protein shape strongly enough to eliminate catalytic ability, the enzyme has undergone **denaturation**.",
  "She resets the temperature and turns to the right-side pH control. The same enzyme is tested across several pH values. Activity is highest within a particular range, then drops as the environment moves farther from it. Nia labels the best-performing temperature and pH as this enzyme’s **optimal conditions**. The display immediately adds a warning. Different enzymes can have different optima. An enzyme adapted to one cellular compartment or organism does not inherit a universal optimum from the word enzyme itself. Nia labels the outer settings **temperature and pH outside the optimum** once they move beyond the range that supports highest activity. The important image is still the transparent protein in the center, because temperature and pH matter through their effects on molecular interactions, collision behavior, and, at damaging extremes, protein conformation.",
  "Nia now performs the recovery test. She applies a moderate structural disturbance, then returns the chamber to the starting conditions. The enzyme’s outline moves back toward its earlier conformation and the reaction counter restarts. ‘This is **reversible denaturation**,’ she says. ‘Some denaturation can be reversible when the disturbance has not produced persistent structural damage.’ ‘Recovery depends on what changed and how severely.’ The screen stores that result beside the earlier failed shape. A temporary rate change and a destroyed enzyme are not automatically the same event. The diagnosis comes from the visible structure and the recovery test.",
  "The chamber alarms finally quiet, yet the control wing’s main rate gauge still swings even while the enzyme shape remains stable. A conveyor door opens beyond the center monitor. Amber substrates are piling up behind it. Nia releases the clamp and the transparent reference enzyme slides forward with you. ‘Its shape is stable now,’ she says. ‘So the next question is how often substrate reaches an available active site.’ You follow the enzyme into the **Collision and Saturation Track**."
 ],
 'close':'You carry forward one intact reference enzyme and the rule that environmental effects must be diagnosed from their molecular consequence, especially whether protein conformation is disrupted and whether activity can recover.',
 'images':{
  'Structure-function disruption':'the center enzyme changing conformation as its catalytic output falls',
  'Enzyme denaturation':'the transparent folded enzyme losing the active-site geometry required for catalysis under an extreme condition',
  'Temperature and pH outside optimum':'the left temperature dial and right pH slider moving away from the settings that give the highest activity',
  'Reversible denaturation':'the disturbed enzyme regaining its working conformation and catalytic output after ordinary conditions are restored',
  'Optimal conditions':'the temperature and pH range where the center reaction counter reaches its highest activity for this enzyme'
 }},
'U3-L05':{
 'title':'The Conveyor That Hit a Ceiling',
 'kicker':'The enzyme is folded correctly, yet the reaction rate still changes. Now the problem is how often reactants meet available active sites.',
 'paragraphs':[
  "The **Collision and Saturation Track** is a straight testing corridor. On your **left**, an amber-substrate feeder has a concentration dial and a transparent hopper. Directly **ahead**, identical copies of the reference enzyme ride on a central reaction conveyor. On your **right**, a separate temperature control changes molecular speed without entering the damaging range you just tested. A rate graph hangs above the center lane. Nia fixes the amount of enzyme and leaves it unchanged. ‘This room is about encounters,’ she says. ‘Do not change the number of active sites while we change the substrate supply.’",
  "She starts with only a few amber substrates. Some enzyme active sites wait empty between collisions. The feeder increases substrate concentration. More substrate molecules move through the same volume, encounters with active sites become more frequent, and the reaction-rate graph rises. Nia points to the two labeled reservoirs at the ends of the conveyor and names the variable **substrate and product concentrations**. The **relative concentrations of substrates and products** influence how efficiently an enzymatic reaction proceeds. The exact effect depends on the reaction and conditions, but concentration changes alter the molecular context in which forward and reverse processes occur.",
  "The feeder keeps increasing substrate while enzyme concentration remains fixed. The graph rises again, then bends. Soon nearly every enzyme on the central conveyor is occupied whenever it becomes available. Nia doubles the incoming substrate once more. The hopper becomes crowded, yet the graph barely rises. You can see why. There are no large stretches of unused active sites left to recruit. At sufficiently high substrate concentration, the available enzymes approach **substrate saturation**, so reaction rate approaches a maximum for that fixed enzyme concentration.",
  "Nia returns the substrate feeder to an unsaturated level and moves to the right-side temperature dial. She raises temperature gradually while staying below the range that disrupts the enzyme’s structure. The particles move faster and enzyme-substrate encounters become more frequent, so reaction rate rises toward the enzyme’s optimum. This is a **temperature and collision-frequency** effect. The center enzyme has not gained more active sites, and the protein is not being denatured in this part of the test. A later rise beyond the optimum would require you to consider the structural damage you saw in the previous room.",
  "One enzyme at the far end of the conveyor still shows zero activity despite plenty of substrate, an appropriate temperature, and an open active site. A small socket on its surface is empty. The machine labels it REQUIRED HELPER. Nia lifts that enzyme off the track. ‘Concentration cannot solve a missing component,’ she says. You follow the inactive protein through the next door into the **Cofactor Assembly Station**."
 ],
 'close':'The rate ceiling stays behind as a visible reminder that more substrate cannot create more active sites once the available enzyme population is saturated.',
 'images':{
  'Substrate and product concentrations':'the calibrated left feeder and product reservoir changing the concentration context around a fixed amount of enzyme',
  'Temperature and collision frequency':'the right-side temperature control increasing molecular speed and encounter frequency while enzyme structure stays intact',
  'Substrate saturation':'the rate graph flattening while nearly every central active site remains continuously occupied'
 }},
'U3-L06':{
 'title':'The Missing Helper Slot',
 'kicker':'One enzyme has substrate, a stable shape, and an open active site. It still cannot work until the missing nonprotein helper is identified.',
 'paragraphs':[
  "The **Cofactor Assembly Station** looks like a repair bench built around one incomplete enzyme. On your **left**, the folded protein component rests under a lamp with its active site intact and a second, smaller helper position left empty. Directly **ahead**, a circular assembly platform holds two removable helper trays. On your **right**, a green output pad is labeled ACTIVE COMPLEX. Nia places the protein on the center bench and sends substrate toward it. Nothing happens. The missing helper socket flashes.",
  "From the first tray, Nia lifts a small metal-ion model and seats it into the required position. The enzyme becomes catalytically active and moves toward the green pad. ‘A nonprotein helper required by some enzymes is a **cofactor**,’ she says. The bench identifies this example as inorganic. Metal ions can function as cofactors for some enzymes. Nia removes it and the output falls again, keeping the relationship visible. The protein alone is not always the complete active catalytic system.",
  "She opens the second tray. This helper is an organic molecule, and a tag shows that many molecules of this general kind are derived from vitamins. Once the organic helper is associated correctly, the activity light returns. Nia names the category **coenzyme**. The hierarchy matters. A coenzyme is an **organic cofactor**. The two words are not competing boxes where a helper must be one or the other. Cofactor is the broader helper category; coenzyme identifies the organic members of that category.",
  "The bench now outlines the entire working assembly in green. The protein component plus its required associated cofactor forms the catalytically active **holoenzyme**. Nia keeps the term attached to the complete active complex on the right output pad, not to every enzyme protein in the building. You compare the three physical states one last time. Protein component alone on the left. Helper added at the center. Active holoenzyme on the right.",
  "The restored holoenzyme moves out through a narrow gate. Before it can enter the next reaction lane, a pale molecule approaches from the opposite side and slips into the enzyme’s active site. The amber substrate stops at the threshold. Nia looks at the occupied pocket. ‘The helper problem is fixed. This is a different kind of control.’ You follow both molecules into the **Competitive Inhibitor Gate**."
 ],
 'close':'You leave with a three-part hierarchy that can be redrawn from the bench itself: cofactor is the broad nonprotein-helper category, coenzyme is an organic cofactor, and a holoenzyme is the active enzyme complex with its required helper associated.',
 'images':{
  'Cofactor':'an inorganic helper such as a metal ion completing a required nonprotein helper position on the enzyme',
  'Coenzyme':'an organic, often vitamin-derived helper occupying the same conceptual helper category',
  'Holoenzyme':'the complete catalytically active enzyme complex glowing green only after its required cofactor is associated'
 }},
'U3-L07':{
 'title':'Two Molecules, One Door',
 'kicker':'The substrate and inhibitor are approaching from opposite sides, yet both need the same active-site pocket.',
 'paragraphs':[
  "You enter the **Competitive Inhibitor Gate** and stop exactly where three lanes meet. On your **left**, amber substrate molecules advance in a steady line. Directly **ahead**, the transparent enzyme presents one active-site pocket. On your **right**, pale competitor molecules wait in a second lane. The competitors resemble the substrate closely enough to fit the same pocket, though they are not converted into the intended product. The geometry makes the conflict immediate. One pocket cannot hold both molecules at the same time.",
  "Nia releases equal streams from both sides. An amber substrate reaches the active site first and the reaction proceeds. On the next cycle, a pale molecule arrives first and occupies the pocket. The substrate stops outside. The competitor later leaves, and the pocket becomes available again. Nia names the mechanism **competitive inhibition**. In the standard reversible model shown here, the inhibitor reduces substrate access by binding the enzyme’s **active site**. Nothing has happened at a distant regulatory pocket. The competition is local and visible at the shared gate.",
  "The reaction-rate display falls because some active-site opportunities are being captured by the competitor. Nia leaves the inhibitor stream unchanged and turns up only the substrate feeder on the left. Amber molecules now reach the gate much more frequently. The competitor can still bind, but substrate occupies the active site in a larger fraction of encounters. For a **reversible competitive inhibitor**, increasing substrate concentration can reduce the inhibitor’s effect by increasing the probability that substrate occupies the shared active site.",
  "She lowers substrate again and the competitor regains more gate time. The inhibitor has not vanished, and increasing substrate did not chemically destroy it. You are watching a probability shift caused by two molecules competing for the same site. Nia saves a frozen image of the three lanes because you will need it for comparison. Left substrate. Center active site. Right competitor. ‘When we enter the next room,’ she says, ‘the regulator will no longer need this door.’",
  "A side panel on the enzyme body begins flashing several centimeters away from the active site. Even with the center pocket empty, catalytic activity falls. The competitive model can no longer explain the slowdown. A door opens on the right wall, aligned with that distant panel. You carry the same transparent enzyme into the **Allosteric Control Panel**."
 ],
 'close':'The shared gate remains behind as the defining image of reversible competitive inhibition, two molecules changing occupancy probabilities at the same active site.',
 'images':{
  'Competitive inhibition':'amber substrate and a reversible competitor approaching the same central active-site pocket from opposite lanes',
  'Competitive inhibition and substrate concentration':'the left substrate stream becoming denser so substrate occupies the shared active site more often while inhibitor concentration stays unchanged'
 }},
'U3-L08':{
 'title':'The Switch Far from the Active Site',
 'kicker':'The active site is empty, yet enzyme activity changes when a molecule binds on the opposite side of the protein.',
 'paragraphs':[
  "The **Allosteric Control Panel** keeps the entire enzyme in one transparent display. On your **left**, the familiar active site receives amber substrate. Directly **ahead**, the folded enzyme body spans the center console. On your **right**, a second pocket glows blue several molecular regions away from the substrate-binding site. Nia locks the left active site open so you can see that the regulator never enters it. ‘Keep your eyes on both pockets,’ she says.",
  "A red regulator binds the right-side pocket. The central protein shifts. The left active site changes enough that substrate binding or catalysis becomes less effective, and the reaction-rate lamp dims. The right pocket is an **allosteric site**, a regulatory binding site distinct from the active site. Regulation produced by a molecule binding noncovalently at such a separate site and changing activity through a conformational shift is **allosteric regulation**. The molecule does not have to block the substrate-binding pocket directly to control the reaction.",
  "Nia repeats the test with two regulators. The green regulator binds on the right and stabilizes a conformation with higher activity. It is an **allosteric activator**. The red regulator stabilizes a less-active conformation. It is an **allosteric inhibitor**. The center enzyme rocks between the two conformational states while the active site stays on the left and the regulatory site stays on the right. The location of binding and the resulting conformational change are the retrieval anchors.",
  "A comparison screen now places the previous room beside this one. In competitive inhibition, the reversible competitor occupied the active site itself. Here, the inhibitor binds a separate allosteric region and changes the enzyme’s behavior through conformation. A **noncompetitive inhibitor** can act through an allosteric site and reduce enzyme activity without competing for occupancy of the active site. Nia keeps that example tied to this separate-site mechanism and warns against treating every allosteric interaction as if it were active-site competition.",
  "The right-side regulator releases, but the center console remains connected to a larger protein assembly beyond the wall. Four linked subunits light up in sequence. Nia sends one amber substrate toward the first subunit and watches the others shift before they have bound anything. ‘A regulatory change can travel through one protein complex,’ she says. You follow the linked structure into the **Cooperative Binding Array**."
 ],
 'close':'You leave the room with two sites held apart in space, the substrate-binding active site on the left and the allosteric regulatory site on the right, connected through a conformational change in the enzyme body.',
 'images':{
  'Noncompetitive inhibition':'a red regulator binding the separate right-side site while activity falls at the left active site',
  'Allosteric site':'the blue regulatory pocket physically separated from the substrate-binding active site',
  'Allosteric regulation':'a regulator binding on the right, shifting the center enzyme conformation, and changing activity on the left',
  'Allosteric activator':'a green regulator stabilizing the more-active enzyme conformation',
  'Allosteric inhibitor':'a red regulator stabilizing the less-active enzyme conformation'
 }},
'U3-L09':{
 'title':'The First Binding Changes the Rest',
 'kicker':'One substrate binds at the far left of a multisubunit enzyme, and the remaining active sites change before they bind anything themselves.',
 'paragraphs':[
  "The **Cooperative Binding Array** is a long glass case containing one multisubunit enzyme complex. On your **left**, the first active site is empty. Directly **ahead**, four linked protein subunits form one connected structure. On your **right**, three later active sites wait beside amber substrates. Thin alignment lines make the subunits’ shapes easy to compare. Nia asks you to watch the right side before she allows the first substrate to bind.",
  "At the starting moment, all four sites have one conformation. The first amber substrate enters the left site. As it binds, the left subunit shifts slightly. That shift propagates through the connected center array. The remaining subunits change conformation as well, and the right-side sites now bind subsequent substrate more readily. The first binding event has altered the behavior of later sites in the same protein complex.",
  "Nia names this pattern **cooperativity**. In some multisubunit enzymes, substrate binding at one active site promotes a conformation that increases activity or substrate affinity at other active sites. The important feature is the linkage among subunits. The first substrate is not traveling through the protein to occupy the other sites. Its binding changes the shared protein conformation, and that conformational change alters later binding behavior.",
  "The allosteric control panel is still visible through the doorway behind you, which makes the distinction useful. Both rooms involve conformational communication within a protein. In the previous room, a separate regulatory molecule bound an allosteric site and altered activity. Here, substrate binding at one active site changes the behavior of other active sites in a multisubunit enzyme. Nia leaves the two images side by side so **cooperativity** does not collapse into the broader idea of allosteric regulation.",
  "The rightmost substrate is converted into a blue product and drops into a channel under the case. Instead of leaving the building, the blue product travels along a pipe toward a large pathway map. More copies begin to accumulate at the far end of that map. Nia follows the return pipe with her finger. ‘Now the signal is not staying inside one enzyme,’ she says. You follow the blue product into the **Feedback Loop Control Room**."
 ],
 'close':'The multisubunit array freezes with the first site bound on the left and the later sites altered on the right, giving cooperativity one distinct physical signature.',
 'images':{
  'Cooperativity':'one substrate binding to the first subunit and a linked conformational change making later active sites more active or more receptive'
 }},
'U3-L10':{
 'title':'The Product That Shut Down Its Own Line',
 'kicker':'The pathway is producing exactly what the cell needs. The problem begins when the final product keeps accumulating.',
 'paragraphs':[
  "The **Feedback Loop Control Room** spans an entire wall. On your **left**, a starting substrate enters an early regulatory enzyme. Directly **ahead**, the product of that reaction moves through a visible chain of additional enzyme-catalyzed steps. On your **right**, blue final product collects in a transparent reservoir. A return pipe curves from that reservoir all the way back to the early enzyme. At first the pipe is empty, and the pathway runs continuously from left to right.",
  "Nia allows the final product to accumulate. When the right reservoir reaches its marked level, blue product enters the return pipe and reaches the earlier regulatory enzyme. That enzyme’s activity decreases. The center pathway slows, and less final product is made. Nia names the mechanism **feedback inhibition**. A downstream product inhibits an enzyme acting earlier in the same metabolic pathway, reducing further production when enough product has accumulated.",
  "The diagram matters as a route. The final product is not simply blocking the last reaction. It travels conceptually from the right-side endpoint back toward an earlier control point on the left. As the product level later falls, the pathway can resume according to the regulatory system involved. This creates a self-regulating flow that helps prevent unnecessary overproduction and conserves cellular resources.",
  "Nia opens a second layer of the control board. Feedback inhibition is only one way cells regulate metabolic pathways. Cells can alter the **activity** of enzymes already present, place enzymes in particular cellular **locations**, change enzyme **abundance**, and regulate the **gene expression** that determines how much enzyme is produced. She calls this broader control **metabolic pathway regulation**. She keeps these controls secondary to the main return loop so the central mental picture remains simple. Pathway output can influence an earlier enzyme and change pathway flux.",
  "Most alarms in the wing turn green. One remains red in a recovery bay beyond the right wall. The display says the inhibitor has already been removed, temperature and pH are normal, substrate is available, and the enzyme still does nothing. Nia closes the feedback valve. ‘That failure does not behave like the reversible controls we have tested.’ You follow her into the **Irreversible Inhibition Lockout**."
 ],
 'close':'You carry forward the right-to-left return loop, a downstream product feeding back to an earlier enzyme and reducing the pathway’s own output.',
 'images':{
  'Feedback inhibition':'blue final product accumulating on the right and returning through a loop to inhibit an earlier enzyme on the left',
  'Metabolic pathway regulation':'a secondary control board adjusting enzyme activity, location, abundance, and gene expression around the main feedback-regulated pathway'
 }},
'U3-L11':{
 'title':'The Enzyme That Would Not Recover',
 'kicker':'Every ordinary condition has been restored, yet one enzyme remains inactive. The recovery test reveals a fundamentally different kind of inhibition.',
 'paragraphs':[
  "The final room, **Irreversible Inhibition Lockout**, contains two enzyme bays. On your **left**, an untreated reference enzyme repeatedly converts amber substrate and flashes green. Directly **ahead**, an identical enzyme sits dark after exposure to a persistent inhibitor. On your **right**, the recovery station is already prepared with clean solution, fresh substrate, ordinary temperature, and ordinary pH. Nia places the two enzymes side by side so you can compare recovery under the same conditions.",
  "First she washes all free inhibitor out of the center bay. The solution sensor confirms that the surrounding inhibitor is gone. Fresh substrate enters. The treated enzyme still produces no product. Nia restores every environmental control you used in the stability chamber. The active-site region remains persistently inactivated. In many cases, irreversible inhibitors form covalent or otherwise very stable interactions with an enzyme. The defining result in this room is persistence after the inhibitor has been removed.",
  "Nia names the mechanism **irreversible enzyme inhibition**. She then points back through three windows in the corridor. At the competitive gate, a reversible inhibitor could leave the active site, and greater substrate concentration could reduce its effect. At the allosteric panel, regulatory molecules changed activity through reversible binding and conformational control. In the stability chamber, some structurally disturbed enzymes recovered when ordinary conditions returned. Here, the center enzyme fails the washout and recovery test. ‘Irreversible’ describes persistent loss of activity, not merely an inhibitor that feels unusually strong.",
  "The room also separates irreversible inhibition from denaturation. Both can produce an inactive enzyme, so the word inactive is not enough for diagnosis. In the earlier chamber, you manipulated temperature and pH and watched protein conformation respond to environmental stress. In this lockout, the key evidence is a persistent inhibitor-associated inactivation that remains after free inhibitor is removed. The cause and the recovery behavior distinguish the mechanisms.",
  "Nia turns off the last red alarm. A route map lights across the floor behind you. It traces the entire control wing from the stability chamber to saturation, helper assembly, active-site competition, allosteric control, cooperativity, feedback, and finally irreversible lockout. The transparent reference enzyme appears above the map in each diagnostic state. ‘An enzyme can speed up, slow down, or stop for many different reasons,’ she says. ‘Your job is to read the evidence and identify the mechanism.’ The final door opens toward the cellular energy hall, where reactions will be connected to energy transfer rather than enzyme regulation alone."
 ],
 'close':'The control wing stabilizes with each failure tied to its own mechanism, leaving you with a diagnostic route instead of one vague rule for every change in enzyme activity.',
 'images':{
  'Irreversible enzyme inhibition':'the treated center enzyme remaining inactive after inhibitor washout, fresh substrate, and restoration of ordinary temperature and pH'
 }},
}

CHECKPOINT_HINTS={
'U3-L04':'Look at the transparent enzyme in the center chamber. The temperature and pH controls matter here when they alter the conformation required for catalytic function.',
'U3-L07':'Return to the three-lane gate. Substrate enters from the left and competitor from the right, and both are trying to occupy the same center active-site pocket.',
'U3-L08':'Keep the two enzyme pockets separate. Substrate binds on the left, while the regulator binds the distinct right-side site and changes the center protein conformation.'
}

scenes=[]
for idx,lid in enumerate(J2['route']):
    b=B[lid]; n=NARR[lid]
    zones=[{'position':pos,'label':lab,'symbol':sym,'description':desc} for pos,lab,sym,desc in ZONE_COPY[lid]]
    cast=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    cast += [{'name':name,'kind':kind,'visual':visual,'job':job} for name,kind,visual,job in CAST[lid]]
    beats=[]; snaps=[]
    for t in b['term_introductions']:
        term=t['canonical_term']
        image=n['images'].get(term, b['carry_forward'])
        beats.append({'object_id':t['knowledge_id'],'term':term,'story':image,'science':t['canonical_science'],'exact_name':bool(t.get('exact_name_recall')),'hint':image})
        snaps.append({'term':term,'meaning':t['canonical_science'],'image':image})
    qr=b['quick_recall']; cp=bool(qr.get('enabled'))
    scene={
      'scene_index':idx,'locus':b['scene_title'],'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['exact_location']+' — '+b['micro_anchor']+'.',
      'scene_layout':{'orientation':b['orientation_sentence'],'zones':zones},'cast':cast,
      'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':beats,'memory_snapshot':snaps,
      'checkpoint':cp,'checkpoint_object_id':b['primary_knowledge_id'],'checkpoint_prompt':qr.get('candidate_prompt','') if cp else '',
      'checkpoint_answer':qr.get('answer','') if cp else '','checkpoint_hint':CHECKPOINT_HINTS.get(lid,'') if cp else '',
      'next_locus':B[b['causal_transition']['to_locus_id']]['scene_title'] if b['causal_transition']['to_locus_id'] else None,
      'misconception_guards':b['misconception_guards'],'required_visual':b['visual_spec'],'carry_forward':b['carry_forward']
    }
    scenes.append(scene)

journey={
 'schema':'memory-palace-v2-unit3-f4b-story-1.0','unit_id':'unit-3','palace_id':'U3-J2','journey_id':'U3-J2',
 'palace_name':'Enzyme Regulation Control Wing','story_title':'The Control Wing That Would Not Hold a Steady Rate',
 'tagline':'Carry one transparent enzyme through eight diagnostic stations and learn to identify why enzyme activity changes from visible molecular evidence.',
 'guide':GUIDE,'premise':J2['premise'],'mission':J2['mission'],
 'finale':'The control wing stabilizes only after every rate change is tied to a distinct physical cause. Environmental stress, saturation, helper requirements, active-site competition, allosteric regulation, cooperative subunits, feedback inhibition, and irreversible inactivation can now be diagnosed from what happens to the enzyme or pathway.',
 'estimated_minutes':22,'scene_count':len(scenes),'checkpoint_count':sum(bool(s['checkpoint']) for s in scenes),
 'learner_rule':'Read or listen while holding the left, center, and right anchors of each station in mind. Diagnose the visible mechanism first, then attach the scientific term. Quick Recall is optional during the first pass.',
 'route_orientation':'The Enzyme Regulation Control Wing is an eight-station route. Enter at the stability chamber, follow the same transparent enzyme through the saturation track and helper assembly bench, then move through active-site competition, allosteric control, cooperative binding, pathway feedback, and the final irreversible-inhibition recovery bay. Left, center, and right anchors remain fixed within every station.',
 'route':route,'scenes':scenes,'student_release':'PILOT_PREVIEW_F4B','narrative_standard':'V2-NARRATIVE-3.0-U3-F4B'
}

(U3/'journeys').mkdir(parents=True,exist_ok=True)
(U3/'journeys'/'U3-J2.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

j1=json.loads((U3/'journeys'/'U3-J1.json').read_text(encoding='utf-8'))
def card(j): return {k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
registry={'schema':'memory-palace-v2-unit3-f4b-registry-1.0','course_id':'ap-biology','unit_id':'unit-3','unit_title':'Cellular Energetics','narrative_standard':'V2-NARRATIVE-3.0-U3-F4B','journey_count':2,'scene_count':j1['scene_count']+journey['scene_count'],'checkpoint_count':j1['checkpoint_count']+journey['checkpoint_count'],'guided_journeys':[card(j1),card(journey)]}
(U3/'journeys-f4b.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U3/'status-f4a.json').read_text(encoding='utf-8'))
status.update({'status':'F4B_JOURNEY2_POLISHED_PREVIEW','pipeline_status':'POLISHED_NARRATIVE_JOURNEYS_1_2_F4B','student_release':False,'preview_release':True,'journey_count':2,'scene_count':11,'polished_journeys':2,'polished_scenes':11,'polished_checkpoint_count':5,'narrative_story_files':2,'next_required_output':'F4C polished narrative for Journey 3 Cellular Energy Exchange Hall after F4B prose QA'})
(U3/'status-f4b.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(U3/'status.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; c=json.loads(cp.read_text(encoding='utf-8'))
for u in c['units']:
    if u['unit_id']=='unit-3':
        u.update({'status':'F4B_JOURNEY2_POLISHED_PREVIEW','journey_count':2,'scene_count':11,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEYS1_2_POLISHED_F4B','polished_journeys':2,'polished_scenes':11,'student_release':False})
cp.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# Prefer newest Unit 3 registry without weakening historical stage files.
bc=ROOT/'backend'/'content.py'
s=bc.read_text(encoding='utf-8')
s=s.replace('''    if unit_id == "unit-3":\n        path=UNIT3_DIR / "journeys-f4a.json"\n        return _read_json(path)["guided_journeys"] if path.exists() else []''','''    if unit_id == "unit-3":\n        path=UNIT3_DIR / "journeys-f4b.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4a.json"\n        return _read_json(path)["guided_journeys"] if path.exists() else []''')
bc.write_text(s,encoding='utf-8')

mainp=ROOT/'backend'/'main.py'
ms=mainp.read_text(encoding='utf-8')
ms=ms.replace('0.12.0-u3-f4a','0.13.0-u3-f4b').replace('v2-apbio-0.12.0-u3-f4a','v2-apbio-0.13.0-u3-f4b')
mainp.write_text(ms,encoding='utf-8')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
files=['journeys/U3-J2.json','journeys-f4b.json','status-f4b.json']
lock={'schema':'memory-palace-v2-unit3-f4b-content-lock-1.0','unit_id':'unit-3','stage':'F4B','student_release':False,'files':{f:sha(U3/f) for f in files}}
(U3/'content-lock-f4b.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit3-f4b-release-manifest-1.0','unit_id':'unit-3','stage':'F4B','student_release':False,'preview_release':True,'polished_journeys':2,'polished_scenes':11,'journey_2_records':sum(len(s['object_ids']) for s in scenes),'journey_2_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'next_stage':'F4C_JOURNEY3'}
(U3/'f4b-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Built Unit 3 F4B:',len(scenes),'scenes',sum(len(s['object_ids']) for s in scenes),'knowledge records',sum(bool(s['checkpoint']) for s in scenes),'checkpoints')
