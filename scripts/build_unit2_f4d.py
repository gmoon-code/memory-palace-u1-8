from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
briefs=json.loads((U2/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
jbriefs=json.loads((U2/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
B={s['locus_id']:s for s in briefs if s['journey_id']=='U2-J4'}
J4=next(j for j in jbriefs if j['journey_id']=='U2-J4')

GUIDE={
 'name':'Dr. Nia Park','role':'cell-systems investigator',
 'visual':'navy field jacket, clear safety glasses, and a compact tablet displaying a transparent map of the cell',
 'story_job':'Nia keeps the route physically clear, asks you to predict what will happen, and names scientific terms only after the defining structure or action is visible.'
}

route=[
 {'scene_index':0,'locus':'Phospholipid Bilayer Gate','short':'Bilayer Gate','floor':'Terminal entrance','symbol':'◐'},
 {'scene_index':1,'locus':'Fluid Mosaic Concourse','short':'Mosaic Concourse','floor':'Main membrane concourse','symbol':'≈'},
 {'scene_index':2,'locus':'Fluidity Climate Control','short':'Climate Control','floor':'Temperature chamber','symbol':'↕'},
 {'scene_index':3,'locus':'Membrane Protein Checkpoint','short':'Protein Checkpoint','floor':'Placement checkpoint','symbol':'▥'},
 {'scene_index':4,'locus':'Recognition Counter','short':'Recognition Counter','floor':'Identity desk','symbol':'⌁'},
 {'scene_index':5,'locus':'Selective Barrier Lane','short':'Barrier Lane','floor':'Security lane','symbol':'║'},
 {'scene_index':6,'locus':'Molecule Passport Lanes','short':'Passport Lanes','floor':'Traveler sorting hall','symbol':'⇥'},
 {'scene_index':7,'locus':'Plant Wall and Plasmodesmata Exterior','short':'Plant Exterior','floor':'Terminal exterior','symbol':'▦'},
]

ZONE_COPY={
'U2-L22':[
 ('left','Outside water','💧','Clear extracellular water fills the left side. Polar phosphate-containing heads of the outer phospholipid layer face directly into this aqueous space.'),
 ('center','Hydrophobic membrane core','〰','Two rows of nonpolar fatty-acid tails point toward one another in the center, forming a dry-looking hydrocarbon interior that separates the two watery sides.'),
 ('right','Inside water','💧','Cytosol-like water fills the right side. Polar heads of the inner phospholipid layer face this aqueous environment while their tails point inward.'),
],
'U2-L23':[
 ('left','Drifting phospholipids','≈','Phospholipids slide sideways within their own layer like people moving across a crowded platform while the two-layer boundary remains intact.'),
 ('center','Mixed membrane fabric','✣','The center contains the phospholipid framework together with proteins, cholesterol, glycoproteins, and glycolipids distributed through the membrane.'),
 ('right','Moving membrane proteins','↔','Several embedded proteins shift laterally along the membrane while keeping their hydrophobic regions aligned with the bilayer interior.'),
],
'U2-L24':[
 ('left','Cold unsaturated-tail panel','❄','In the cold panel, phospholipids with visibly kinked cis-unsaturated tails cannot pack into a rigid, perfectly ordered wall.'),
 ('center','Temperature slider','↕','A large control moves the same membrane model from cold to warm so you can watch packing and molecular motion change continuously.'),
 ('right','Cholesterol buffer panel','◈','Rigid cholesterol molecules sit between phospholipids and behave differently at the cold and hot ends of the temperature range.'),
],
'U2-L25':[
 ('left','Peripheral-protein ledge','○','Proteins rest on the membrane surface or attach to exposed parts of other proteins without entering the hydrophobic core.'),
 ('center','Integral-protein scanner','▥','A cross-sectional scanner shows one protein penetrating only part of the bilayer and another crossing completely from one aqueous side to the other.'),
 ('right','Water-facing protein surfaces','◌','Hydrophilic protein regions face water while hydrophobic surfaces are buried where they can contact the fatty-acid tails.'),
],
'U2-L26':[
 ('left','Glycolipid badge rack','♢','A branched carbohydrate chain projects outward from the membrane and can be traced all the way down to a lipid anchor.'),
 ('center','Recognition scanner','◎','The scanner reads outward-facing carbohydrate patterns as molecular identity information during cell-cell recognition.'),
 ('right','Glycoprotein badge rack','♧','A second branched carbohydrate chain projects outward, but this one is covalently attached to a membrane protein.'),
],
'U2-L27':[
 ('left','Aqueous approach','●','The test-traveler tray waits in water on the left, carrying O₂, CO₂, H₂O, NH₃, glucose, Na⁺, and K⁺ markers.'),
 ('center','Hydrophobic security core','║','The nonpolar fatty-acid interior forms the actual physical barrier. Charged and strongly hydrophilic travelers experience this region very differently from small nonpolar molecules.'),
 ('right','Aqueous cell side','○','Travelers that successfully cross emerge into water on the cell side while blocked travelers remain at the boundary or wait for a protein route.'),
],
'U2-L28':[
 ('left','Small nonpolar lane','→','O₂, CO₂, and N₂-sized nonpolar travelers move directly through the lipid bilayer with comparatively little resistance.'),
 ('center','Small uncharged polar lane','⇢','H₂O and NH₃ markers cross directly only to a limited extent; a sign points toward aquaporin routes when rapid water movement is needed.'),
 ('right','Protein-required lane','⇥','Na⁺, K⁺, glucose, and other ions or large polar travelers are redirected toward membrane channels or transport proteins.'),
],
'U2-L29':[
 ('left','Cellulose-rich wall','▦','A rigid plant-cell wall fills the left side, its cellulose microfibrils visible as strong crossing fibers embedded in a broader matrix.'),
 ('center','Plasma membrane beneath wall','≈','A flexible plasma membrane lies immediately inside the wall and remains the primary selectively permeable boundary controlling entry into cytoplasm.'),
 ('right','Plasmodesma to neighbor','⊙','A membrane-lined channel pierces the wall and links the cytoplasm of this plant cell with the adjacent cell on the right.'),
],
}

CAST={
'U2-L22':[
 ('phospholipid heads','scientific part','round polar phosphate-containing heads facing water','interact favorably with aqueous environments on either side of the membrane'),
 ('fatty-acid tails','scientific part','paired nonpolar hydrocarbon tails pointing toward the membrane center','avoid water and create the hydrophobic interior'),
 ('test-traveler tray','continuity object','a clear tray labeled O₂, CO₂, H₂O, NH₃, glucose, Na⁺, and K⁺','stay with you through the terminal so the same molecules can be tested against each membrane rule')],
'U2-L23':[
 ('phospholipids','scientific part','two mobile layers of head-and-tail molecules','form the fluid framework and move mainly sideways within each leaflet'),
 ('membrane proteins','scientific part','different-sized proteins embedded in or attached to the membrane','perform transport, signaling, anchoring, recognition, and other membrane functions'),
 ('membrane mosaic components','scientific parts','cholesterol, glycoproteins, and glycolipids scattered among phospholipids and proteins','make the membrane a mixed molecular mosaic instead of a uniform lipid sheet')],
'U2-L24':[
 ('unsaturated phospholipid tails','scientific part','fatty-acid tails bent by visible cis double-bond kinks','reduce tight packing and help preserve membrane fluidity in the cold'),
 ('cholesterol','scientific part','small rigid steroid molecules wedged between phospholipids','buffer membrane fluidity across temperature changes'),
 ('temperature slider','scientific instrument','a floor-to-ceiling cold-to-hot control connected to the same membrane model','show how the same membrane responds at low and high temperature')],
'U2-L25':[
 ('integral membrane protein','scientific part','a protein penetrating the hydrophobic membrane interior','sit within the bilayer; some integral proteins cross only partway'),
 ('transmembrane protein','scientific part','an integral protein spanning the entire bilayer','cross from one aqueous side of the membrane to the other'),
 ('peripheral membrane protein','scientific part','a protein resting on a membrane surface','associate with the surface without entering the hydrophobic core'),
 ('polarity scanner','scientific instrument','a cross-sectional display shading protein regions as hydrophobic or hydrophilic','show why different protein regions occupy different membrane environments')],
'U2-L26':[
 ('glycolipid','scientific part','a membrane lipid carrying an outward-projecting branched carbohydrate','support recognition and interaction through a carbohydrate attached to lipid'),
 ('glycoprotein','scientific part','a membrane protein carrying an outward-projecting branched carbohydrate','support cell-cell recognition through a carbohydrate attached to protein'),
 ('recognition scanner','scientific instrument','a light that reads external carbohydrate patterns','make the recognition role of membrane carbohydrates visible')],
'U2-L27':[
 ('hydrophobic core','scientific part','a dense region of nonpolar fatty-acid tails between two watery spaces','create the main direct-passage barrier to ions and many polar molecules'),
 ('test travelers','continuity object','the same O₂, CO₂, H₂O, NH₃, glucose, Na⁺, and K⁺ markers','reveal that crossing behavior follows molecular properties rather than an intentional gatekeeper'),
 ('crossing sensor','scientific instrument','a light that measures how far each traveler enters the bilayer','show nonpolar passage and hydrophilic exclusion directly')],
'U2-L28':[
 ('small nonpolar travelers','scientific parts','O₂, CO₂, and N₂-sized uncharged nonpolar markers','cross the bilayer readily'),
 ('small uncharged polar travelers','scientific parts','H₂O and NH₃ markers','cross directly in small amounts and more slowly than small nonpolar molecules'),
 ('ions and large polar travelers','scientific parts','Na⁺, K⁺, glucose, and similar hydrophilic markers','generally require membrane channels or transport proteins')],
'U2-L29':[
 ('plant cell wall','scientific part','a rigid mesh of cellulose microfibrils embedded in polysaccharide and protein matrix','support shape, resist excessive expansion during water uptake, and protect the cell'),
 ('plasma membrane','scientific part','a flexible phospholipid bilayer immediately beneath the wall','remain the primary selectively permeable boundary controlling entry into cytoplasm'),
 ('plasmodesma','scientific part','a membrane-lined channel crossing the wall into the neighboring cell','connect adjacent plant-cell cytoplasm for transport and communication')],
}

NARR={
'U2-L22':{
 'title':'Build the border from the water inward','kicker':'Loose lipids find their only stable arrangement.',
 'paragraphs':[
  'The elevator from the Scaling Observatory opens directly into the entrance of the **Membrane Border Terminal**. You stop before taking a single step. Water fills both sides of the transparent boundary: extracellular fluid glows pale blue on your left, and cytosol-like fluid glows on your right. Between them, however, there is no proper membrane. Hundreds of phospholipids tumble randomly like dropped compass needles. Behind you, Dr. Nia Park places a clear tray on a rail. Seven travelers wait inside it: O₂, CO₂, H₂O, NH₃, glucose, Na⁺, and K⁺. “Keep your eye on that tray,” she says. “We will use the same travelers all the way through this terminal. First, we have to rebuild the border they are trying to cross.”',
  'Nia enlarges one phospholipid until it is almost as tall as you. At the top is a round phosphate-containing region that turns eagerly toward the surrounding water. Hanging below are two long fatty-acid chains that recoil from the water and swing inward. The contrast is impossible to miss: one molecule carries both a **polar, hydrophilic region** and **nonpolar, hydrophobic regions**. Nia waits until you have watched the two parts behave differently. “That combination is what **amphipathic** means,” she says. “A phospholipid has a water-interacting head and water-avoiding tails.”',
  'Then the loose phospholipids begin to organize themselves. On the left, heads rotate toward the extracellular water while their tails turn away. On the right, another layer does the same toward the cytosol. The two sets of fatty-acid tails meet in the center, tail against tail, while the phosphate-containing heads remain exposed to water on both surfaces. The result is a **phospholipid bilayer**: hydrophilic surfaces facing the two aqueous environments and a hydrophobic interior buried between them. Nothing in the scene has to “decide” which way to face. The arrangement follows directly from the different chemical properties of the head and tails.',
  'Nia slides one phospholipid sideways with the tip of her tablet. It moves. The neighboring molecules close the gap. “Remember that,” she says. “This is a stable arrangement, not a cement wall.” The rebuilt bilayer now stretches from floor to ceiling. Its watery faces remain on the left and right, and its hydrocarbon interior remains in the center. The traveler tray rolls forward until it stops beside the newly formed gate. The membrane surface suddenly ripples sideways, carrying several lipids with it. A whole concourse beyond the gate begins to move.',
  'You look back once before entering. Water on the left. Polar heads facing it. Hydrophobic tails hidden in the center. Polar heads facing water again on the right. That simple three-part picture explains the basic **bilayer orientation**. Nia taps the center of the membrane. “If you can always recover that layout,” she says, “the next questions become easier. The properties of the border come from what is actually here.”'
 ],
 'close':'The bilayer is rebuilt with its hydrophilic heads facing water and its hydrophobic tails facing one another; the moving surface now pulls you into the next concourse.',
 'images':{
  'Phospholipid amphipathic structure':'one enlarged phospholipid with a water-facing polar head and two water-avoiding nonpolar tails',
  'Bilayer orientation':'two phospholipid layers arranged tail-to-tail between water on the left and water on the right'
 }
},
'U2-L23':{
 'title':'The floor starts moving','kicker':'A membrane that looked like a wall becomes a moving molecular crowd.',
 'paragraphs':[
  'The bilayer gate opens into a broad horizontal concourse made from the membrane itself. For a moment the scene looks wrong. Every phospholipid is frozen in a perfect grid, every protein is locked in one position, and the whole surface resembles a tiled floor. Nia steps onto it and crouches. “This is the picture that causes trouble,” she says. “A membrane has organization, but it is not normally a rigid sheet of molecules bolted in place.” She releases the freeze control.',
  'The left side comes alive first. Phospholipids begin sliding laterally within their layer, passing one another without turning their hydrophobic tails out into the surrounding water. The bilayer stays intact even though individual lipids change neighbors. Across the center, a large transport protein drifts several molecular widths to the side. Another protein remains anchored to an internal support structure and moves far less. Nia points out the difference. Many membrane components can move laterally, but their freedom is not identical and the usual motion is not constant flipping from one leaflet to the other.',
  'Now the lights brighten across the center of the concourse. The membrane is not made of phospholipids alone. Proteins of different shapes interrupt the lipid field. In a vertebrate-animal membrane demonstration, small cholesterol molecules sit among the tails. Branched carbohydrates project from selected lipids and proteins on the outer surface. The mixed composition is why the membrane is described as a **mosaic**. The lateral mobility you just watched is why it is described as **fluid**. Together those ideas form the **fluid mosaic model** of membrane organization.',
  'The traveler tray glides beside you as you walk. O₂ and CO₂ wobble in their slots; Na⁺ and K⁺ remain brightly charged; glucose takes up far more space than the gases. Nia gestures around the concourse. “Later we will test each one against the membrane,” she says. “For now, notice that the border they meet is a changing molecular fabric. Lipids form the framework. Proteins, cholesterol, glycolipids, and glycoproteins are distributed through that framework. Many lipids and proteins can move sideways while preserving the membrane’s basic orientation.”',
  'Without warning, frost blooms across the left rail. At the same moment, heat lamps blaze red on the right. The moving membrane begins to behave differently at the two ends of the hall. Some regions stiffen. Others become excessively loose. Nia grabs the traveler tray before it rolls away. “Composition is only half the story,” she says. “Now we have to keep this membrane fluid while temperature changes.”'
 ],
 'close':'The fluid mosaic is now a moving, mixed membrane rather than a frozen sandwich, and a sudden temperature swing sends you directly into climate control.',
 'images':{
  'Fluid mosaic composition':'a mixed phospholipid membrane containing proteins, cholesterol, glycolipids, and glycoproteins',
  'Fluid mosaic movement':'phospholipids and many proteins sliding laterally while the bilayer remains intact'
 }
},
'U2-L24':{
 'title':'A cold snap and a heat surge','kicker':'Kinked tails and cholesterol keep the membrane from becoming either a brick or a spill.',
 'paragraphs':[
  'You enter a narrow climate chamber with one continuous membrane model running from left to right. The left end is cold enough to frost the glass. The center holds a vertical temperature slider. The right end glows under a heat lamp. Nia points to the cold panel first. Straight saturated fatty-acid tails have packed closely together, making the membrane increasingly stiff. Beside them, phospholipids with **unsaturated tails** look different: each cis double bond produces a visible kink, like a bent knee in an otherwise straight chain.',
  'As the temperature drops, those kinks prevent neighboring tails from lining up as tightly. The membrane region containing more unsaturated phospholipid tails remains more fluid than the tightly packed straight-tail region. Nia traces one bend with her finger. “The useful image is the kink,” she says. “Unsaturation changes packing. The cis double-bond kink creates space and helps a membrane remain fluid at lower temperatures.” The point is not that unsaturated lipids are magical antifreeze; their shape simply makes close packing harder.',
  'Nia then moves the central slider upward. The membrane becomes warmer and molecular motion increases. Small rigid steroid molecules appear between the phospholipids. “This is **cholesterol** in a vertebrate-animal membrane,” she says. At the hot end, cholesterol restrains some phospholipid movement, preventing the membrane from becoming excessively fluid. Nia drags the slider sharply back toward cold. The same cholesterol molecules now interfere with the phospholipids packing too tightly. The effect reverses with temperature.',
  'You watch the slider travel cold to hot and back again. Cholesterol is not an “always more fluid” switch and it is not an “always less fluid” switch. It acts as a **fluidity buffer**: at higher temperatures it restrains phospholipid movement; at lower temperatures it hinders tight packing. Next to it, the kinked unsaturated tails contribute in a different way by reducing how tightly the hydrocarbon chains can pack.',
  'The chamber stabilizes. On the traveler tray, the molecules are unchanged, but the membrane they will cross is now flexible enough to function. A scanner farther down the corridor lights up and projects silhouettes of membrane proteins—some buried, some spanning the entire bilayer, some sitting only on the surface. Nia pushes the tray toward it. “Before we test the travelers,” she says, “we need to stop pretending every membrane protein is the same kind of tunnel.”'
 ],
 'close':'Temperature no longer drives the bilayer toward rigidity or excessive motion; kinked unsaturated tails and cholesterol have different, visible roles in preserving useful membrane fluidity.',
 'images':{
  'Membrane fluidity and unsaturation':'cis-double-bond kinks in unsaturated fatty-acid tails preventing tight packing in the cold',
  'Cholesterol as fluidity buffer':'cholesterol between phospholipids restraining motion when warm and hindering tight packing when cold'
 }
},
'U2-L25':{
 'title':'Not every protein is a tunnel','kicker':'The scanner separates surface proteins, embedded proteins, and proteins that span the whole membrane.',
 'paragraphs':[
  'The next checkpoint is built around a giant cross-section of the bilayer. On the left, several proteins sit loosely against the membrane surface. In the center, a scanner passes a beam through the hydrophobic core. On the right, water surrounds the exposed parts of the proteins. The display begins with a deliberately bad model: every protein is drawn as a full-width pore crossing the membrane from one watery side to the other. Nia shakes her head. “If we keep that picture, several important terms collapse into one.”',
  'She sends the first protein through the scanner. Part of its surface is shaded dark where it enters the bilayer’s hydrophobic interior, while water-facing regions glow blue. Embedded membrane proteins can contain both **hydrophobic and hydrophilic regions**. Hydrophobic surfaces can interact with the nonpolar membrane interior. Hydrophilic regions can remain exposed to water, and hydrophilic regions can also occur within a protein where appropriate. The protein’s orientation therefore reflects chemistry, just as the phospholipid orientation did at the entrance.',
  'A second scan shows a protein penetrating the hydrophobic interior but stopping before it crosses the entire bilayer. Nia labels it an **integral membrane protein**. “Integral means it penetrates the hydrophobic interior,” she says. Then a taller protein slides into view and spans all the way from the extracellular water to the cytosolic water. “This is also integral, and because it spans the whole membrane, it is specifically a **transmembrane protein**.” She leaves the two models side by side: partial penetration in the center-left, full span in the center-right. Some integral proteins are transmembrane. Not all integral proteins are.',
  'Finally, one of the proteins from the left ledge is scanned. It remains on the surface, attached loosely to the membrane or to an exposed portion of an integral protein, but it never enters the hydrophobic core. Nia labels it a **peripheral membrane protein**. The physical distinction is now easy to recover: integral goes into the membrane interior; transmembrane is the integral subset that crosses the entire bilayer; peripheral remains associated with the surface.',
  'The traveler tray rolls past the scanner, but a new alarm stops it at the next desk. Branched carbohydrate chains are sticking out from selected membrane components like identity badges, and the system cannot tell whether each badge belongs to a lipid or a protein. Nia points ahead. “Placement is fixed,” she says. “Now we need to read the labels on the outside surface.”'
 ],
 'close':'The protein checkpoint leaves three distinct spatial categories in view: peripheral at the surface, integral penetrating the hydrophobic core, and transmembrane spanning the entire bilayer.',
 'images':{
  'Membrane-protein polarity':'a protein with hydrophobic surfaces buried in the lipid core and hydrophilic regions exposed to water',
  'Protein orientation':'water-facing hydrophilic protein regions contrasted with membrane-facing hydrophobic regions',
  'Integral membrane protein':'one integral protein entering only part of the hydrophobic core beside another integral protein that spans the bilayer',
  'Peripheral membrane protein':'a protein attached to the membrane surface without entering the hydrophobic interior'
 }
},
'U2-L26':{
 'title':'Read the sugar badges','kicker':'Two similar carbohydrate tags mean different names because they are attached to different anchors.',
 'paragraphs':[
  'The Recognition Counter is quieter than the protein checkpoint. The membrane lies horizontally beneath a bright scanner. On the left, a branched carbohydrate chain projects outward from the membrane like a small tree. On the right, another carbohydrate chain looks almost identical. If you look only at the sugars, there is no obvious reason to give them different names. Nia dims the overhead lights and sends a tracing beam down each chain to its anchor.',
  'The left beam follows its carbohydrate all the way to a membrane lipid. The scanner outlines the lipid anchor in gold. “Carbohydrate covalently attached to a lipid,” Nia says. “That whole structure is a **glycolipid**.” She leaves the word beside the molecule while the carbohydrate continues to project into the extracellular space. Glycolipids can participate in cell recognition and interactions, but the part you must use to identify the term is what the carbohydrate is attached to.',
  'The right beam descends through the second carbohydrate chain and ends on a membrane protein. The protein flashes blue. “Carbohydrate covalently attached to a protein,” Nia says. “That is a **glycoprotein**.” The two structures now sit on opposite sides of the recognition desk: sugar-on-lipid to the left, sugar-on-protein to the right. The visual difference is small but exact.',
  'Nia activates the central recognition scanner. It sweeps across the outward-projecting carbohydrate patterns and responds differently to different molecular arrangements. Membrane carbohydrates are important in **cell-cell recognition** because they present recognizable molecular patterns on the cell surface. The story is not that the sugar chain is a decorative flag. Its molecular pattern can participate in how cells identify and interact with one another.',
  'The scanner clears both badges and releases the traveler tray. This time the tray rolls to a dark security lane where the bilayer’s fatty-acid tails fill the center like a thick nonpolar curtain. Na⁺ glows intensely in its slot. O₂ is almost invisible beside it. Nia turns to you. “Now we stop naming parts and test what this border actually does.”'
 ],
 'close':'The recognition counter leaves one clean distinction: glycolipid means carbohydrate attached to lipid, while glycoprotein means carbohydrate attached to protein; both can contribute to recognition.',
 'images':{
  'Glycolipid':'a branched carbohydrate traced directly to a membrane lipid anchor',
  'Glycoprotein':'a branched carbohydrate traced directly to a membrane protein anchor'
 }
},
'U2-L27':{
 'title':'The barrier has no guard','kicker':'Crossing depends on molecular interactions with the hydrophobic core, not on a membrane making choices.',
 'paragraphs':[
  'The Selective Barrier Lane is arranged as one simple cross-section. Water and the traveler tray are on the left. The fatty-acid interior of the bilayer fills the center. Water on the cell side is on the right. A cartoon guard icon flashes above the lane with the words APPROVE or DENY, as though the membrane were consciously choosing which molecule it wanted. Nia reaches up and switches the icon off. “That picture has to go,” she says. “Selective permeability comes from molecular properties and structure.”',
  'She releases the O₂ marker first. The small nonpolar molecule enters the nonpolar interior without encountering the severe energetic problem faced by a charged particle. It moves through and appears in the water on the right. Then Nia releases Na⁺. The charged ion reaches the hydrophobic core and stops. The crossing sensor spikes red. A charged particle is strongly stabilized by interactions with water; moving it directly into a nonpolar hydrocarbon region is unfavorable. The membrane has not rejected the ion on purpose. The **hydrophobic barrier** created by the nonpolar phospholipid tails makes direct passage difficult.',
  'H₂O is next. It approaches the same center region and crosses far less readily than O₂ in this simplified comparison. Nia does not let the display turn that into “water cannot cross.” Small uncharged polar molecules can cross the bilayer to a limited extent. Rapid water movement in cells is often supported by aquaporins, which you will meet later. Glucose, much larger and polar, remains waiting for a protein-assisted route. Na⁺ and K⁺ remain waiting as charged ions.',
  'Nia draws a line along the membrane itself. “This is **selective permeability**,” she says after you have watched the three behaviors. The plasma membrane separates internal and external environments, and much of its selective behavior arises from the hydrophobic interior of the bilayer. Small nonpolar molecules interact with that interior very differently from ions and many polar molecules. Selectivity therefore emerges from chemistry, size, polarity, charge, and available transport structures.',
  'The security lane opens into a bright sorting hall with three enormous passport signs. The same traveler tray rolls into the center. “You have seen the principle,” Nia says. “Now sort the travelers precisely enough that you can predict which route each one needs.”'
 ],
 'close':'The membrane’s selectivity is now grounded in the nonpolar bilayer interior: it is a physical chemical barrier, not an invisible gatekeeper making intentional decisions.',
 'images':{
  'Selective permeability basis':'one membrane separating two watery environments while different molecules show different crossing behavior',
  'Hydrophobic barrier':'Na⁺ stopping at the nonpolar fatty-acid interior while a small nonpolar O₂ marker crosses'
 }
},
'U2-L28':{
 'title':'Sort the travelers by chemistry','kicker':'The same molecule tray finally reveals three distinct crossing classes.',
 'paragraphs':[
  'Three passport lanes run side by side. Nia places the traveler tray at the starting line and refuses to let you memorize the molecules as a random list. “Use three questions,” she says. “How large is it? Is it polar? Is it charged?” The left lane is marked DIRECT THROUGH LIPID. The center lane is marked LIMITED DIRECT PASSAGE. The right lane leads toward membrane transport proteins.',
  'O₂ and CO₂ go first, joined by a small N₂ marker from the lane’s demonstration kit. All three are **small nonpolar molecules**. They move readily into the hydrophobic interior and emerge on the other side of the bilayer. The left sign lights green. You can now picture the class rather than just one example: small, nonpolar gases can cross the lipid bilayer readily.',
  'Nia moves H₂O and NH₃ into the center lane. They are **small uncharged polar molecules**. They can cross directly in small amounts, but their polarity makes direct passage through the nonpolar interior less favorable than it is for the small nonpolar gases. H₂O reaches the far side slowly in the model. A blue arrow points toward an aquaporin station in the next journey, reminding you that cells can support much higher water flux through specialized channels without changing the fact that some direct diffusion of water through the bilayer is possible.',
  'Now the right lane fills. Na⁺ and K⁺ glow with charge. Glucose is much larger and polar. These travelers do not simply push through the hydrocarbon core. **Ions and large polar molecules generally require embedded channels or transport proteins** to cross plasma membranes efficiently. The right lane therefore does not mean “never crosses.” It means “use a protein-assisted route.” That distinction prepares the entire next transport journey.',
  'Nia resets the tray so the categories remain visible together: small nonpolar on the left, small uncharged polar in the center, ions and large polar on the right. “Keep the rule tied to molecular properties,” she says. “If you only memorize O₂, water, and sodium as three separate facts, you lose the reason.” The terminal doors open to the outside. Beyond them is a rigid plant-cell wall, and a narrow channel runs through it to a neighboring cell.'
 ],
 'close':'The traveler tray is now sorted by size, polarity, and charge, giving you three crossing classes that will become the starting conditions for the Gradient Transit Hub.',
 'images':{
  'Small nonpolar passage':'O₂, CO₂, and N₂ markers crossing directly through the bilayer in the left passport lane',
  'Hydrophilic transport':'Na⁺, K⁺, glucose, and other ions or large polar molecules redirected toward membrane transport proteins',
  'Small polar passage':'H₂O and NH₃ markers crossing directly only to a limited extent in the center lane'
 }
},
'U2-L29':{
 'title':'The wall outside the membrane','kicker':'Support, selectivity, and cell-to-cell connection occupy three different structures in the same view.',
 'paragraphs':[
  'You step outside the terminal and immediately face a plant-cell boundary large enough to walk along. The spatial order matters. On the left is a thick **cell wall**. In the center, immediately beneath that wall, lies the flexible plasma membrane. On the right, a narrow channel pierces the wall and continues into a neighboring plant cell. Nia makes you stop at the threshold. “Do not merge these three structures,” she says. “They are adjacent, but they do different jobs.”',
  'The wall on the left resolves into a mesh of **cellulose microfibrils** embedded in a matrix of other polysaccharides and proteins. Water enters the cell and the cell contents press outward. The plasma membrane pushes against the rigid wall, but the wall resists excessive expansion and helps the cell maintain shape. The wall therefore contributes structural support and protection. Nia also broadens the view: plants are not the only organisms with cell walls. Bacteria, Archaea, and Fungi have cell walls as well, though their compositions differ.',
  'Then she taps the flexible membrane lying just inside the plant wall. The traveler tray is placed against it again. “This is still the primary selective boundary controlling entry into the cytoplasm,” she says. The plant wall can affect movement of some substances and protects against osmotic lysis, but the wall does not replace the selective transport role of the **plasma membrane**. The two layers are physically adjacent yet functionally distinct: rigid support outside, selectively permeable membrane beneath.',
  'A pulse of green light now travels through the narrow channel on the right. The channel is lined by plasma membrane and links the cytoplasm of this cell with the cytoplasm of its neighbor. Nia names a single channel a **plasmodesma**; the plural is **plasmodesmata**. Through these connections, neighboring plant cells can exchange materials and communicate. The wall is therefore not simply an uninterrupted barrier between every adjacent cell.',
  'The border-terminal alarms finally go quiet. Bilayer orientation is restored, the membrane moves as a fluid mosaic, fluidity remains workable across temperature changes, proteins are placed correctly, recognition tags are identified, and each traveler has the right crossing category. Then a new alarm appears beyond the neighboring cell. Colored particles are piling up on one side of a membrane while the other side is nearly empty. Nia looks toward the next station. “Now that we know the border,” she says, “we can finally ask why molecules move in one direction, when they need energy, and when they need a protein.” The **Gradient Transit Hub** lights up ahead.'
 ],
 'close':'The repaired terminal ends with three plant-cell boundary structures separated clearly: cell wall for support and protection, plasma membrane for selective entry, and plasmodesmata for communication between neighboring cells.',
 'images':{
  'Cell walls':'a rigid outer wall supporting the plant cell while the plasma membrane remains visible immediately beneath it',
  'Plant cell wall composition':'cellulose microfibrils embedded in a broader polysaccharide-and-protein matrix',
  'Plant cell wall function':'a water-filled plant cell pressing outward while the rigid wall resists excessive expansion and supports shape',
  'Plasmodesma':'a membrane-lined channel crossing the plant cell wall and linking the cytoplasm of neighboring cells'
 }
},
}

SCENE_META={
'U2-L22':('Phospholipid Bilayer Gate','Terminal entrance','Phospholipid Bilayer Gate — the transparent entrance where extracellular water is on your left, cytosol-like water is on your right, and the hydrophobic membrane interior forms between them.'),
'U2-L23':('Fluid Mosaic Concourse','Main membrane concourse','Fluid Mosaic Concourse — a wide walkway built from the bilayer itself, where lipids and proteins can be watched moving sideways through a mixed membrane fabric.'),
'U2-L24':('Fluidity Climate Control','Temperature chamber','Fluidity Climate Control — one continuous membrane demonstration spanning a frosted cold panel on the left, a temperature slider in the center, and a heated cholesterol panel on the right.'),
'U2-L25':('Membrane Protein Checkpoint','Placement checkpoint','Membrane Protein Checkpoint — a cross-sectional scanner that keeps surface proteins on the left, embedded protein placement in the center, and water-exposed protein regions on the right.'),
'U2-L26':('Recognition Counter','Identity desk','Recognition Counter — a membrane identity desk with carbohydrate-tagged lipids on the left, the recognition scanner in the center, and carbohydrate-tagged proteins on the right.'),
'U2-L27':('Selective Barrier Lane','Security lane','Selective Barrier Lane — a single crossing lane with the traveler tray in water on the left, the hydrophobic fatty-acid core in the center, and aqueous cell interior on the right.'),
'U2-L28':('Molecule Passport Lanes','Traveler sorting hall','Molecule Passport Lanes — three parallel lanes fixed left-to-right for small nonpolar molecules, small uncharged polar molecules, and ions or large polar molecules that require protein-assisted routes.'),
'U2-L29':('Plant Wall and Plasmodesmata Exterior','Terminal exterior','Plant Wall and Plasmodesmata Exterior — the outside of a plant cell where the cellulose-rich wall stands on the left, the plasma membrane lies directly beneath it in the center, and a plasmodesma connects to the neighboring cell on the right.'),
}

lids=['U2-L22','U2-L23','U2-L24','U2-L25','U2-L26','U2-L27','U2-L28','U2-L29']
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
    scene={
      'scene_index':idx,'locus':locus,'title':n['title'],'scene_kicker':n['kicker'],'location_description':locdesc,
      'scene_layout':{'orientation':b['orientation_sentence'],'zones':zones},
      'cast':cast,'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':beats,'memory_snapshot':snaps,
      'checkpoint':checkpoint,'checkpoint_object_id':b['primary_knowledge_id'],'checkpoint_prompt':qr.get('candidate_prompt','') if checkpoint else '',
      'checkpoint_answer':qr.get('answer','') if checkpoint else '',
      'checkpoint_hint':({
          'U2-L22':'Picture the bilayer cross-section: water outside, polar heads facing water, and the long nonpolar tails meeting in the dry-looking center.',
          'U2-L25':'Picture the scanner showing one protein entering only part of the hydrophobic core and a second protein spanning all the way across the bilayer.',
          'U2-L29':'Picture the rigid wall outside and the flexible phospholipid membrane directly beneath it; only one of those is the primary selective boundary into cytoplasm.'
      }.get(lid,'') if checkpoint else ''),
      'next_locus':B[b['causal_transition']['to_locus_id']]['scene_title'] if b['causal_transition']['to_locus_id'] in B else None,
      'misconception_guards':b['misconception_guards'],'required_visual':b['visual_spec'],'carry_forward':b['carry_forward']
    }
    scenes.append(scene)

journey={
 'schema':'memory-palace-v2-unit2-f4d-story-1.0','unit_id':'unit-2','palace_id':'U2-J4','journey_id':'U2-J4','palace_name':'Membrane Border Terminal',
 'story_title':'The Border Terminal Breach','tagline':'Rebuild a molecular border from phospholipids outward, then follow the same travelers through fluidity, protein placement, recognition, permeability, and the plant-cell exterior.',
 'guide':GUIDE,'premise':J4['premise'],'mission':J4['mission'],
 'finale':'The terminal stabilizes only after the membrane is rebuilt as an amphipathic bilayer, restored as a fluid mosaic, temperature-buffered, populated with correctly placed proteins and recognition tags, and tested against one consistent set of molecular travelers. Outside, the plant cell wall, plasma membrane, and plasmodesmata are left as three distinct structures with three distinct jobs.',
 'estimated_minutes':15,'scene_count':len(scenes),'checkpoint_count':sum(bool(s['checkpoint']) for s in scenes),
 'learner_rule':'Read or listen and keep the same membrane cross-section and traveler tray in mind. Let each molecular behavior become visible before attaching the scientific name. Quick Recall is optional during the first pass.',
 'route_orientation':'The Membrane Border Terminal is one continuous route. Begin at the bilayer entrance with water on both sides, cross the moving Fluid Mosaic Concourse, pass through temperature control, protein placement, and recognition, then use the same traveler tray in the selective barrier and passport lanes before stepping outside to the plant cell wall and plasmodesma.',
 'route':route,'scenes':scenes,'student_release':'PILOT_PREVIEW_F4D','narrative_standard':'V2-NARRATIVE-3.0-F4D'
}

(U2/'journeys').mkdir(parents=True,exist_ok=True)
(U2/'journeys'/'U2-J4.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

js=[json.loads((U2/'journeys'/f'U2-J{i}.json').read_text(encoding='utf-8')) for i in range(1,4)]+[journey]
def card(j): return {k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
registry={
 'schema':'memory-palace-v2-unit2-f4d-registry-1.0','course_id':'ap-biology','unit_id':'unit-2','unit_title':'Cells','narrative_standard':'V2-NARRATIVE-3.0-F4D',
 'journey_count':4,'scene_count':sum(j['scene_count'] for j in js),'checkpoint_count':sum(j['checkpoint_count'] for j in js),
 'guided_journeys':[card(j) for j in js]
}
(U2/'journeys-f4d.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U2/'status-f4c.json').read_text(encoding='utf-8'))
status.update({
 'status':'F4D_JOURNEY4_POLISHED_PREVIEW','pipeline_stage':'POLISHED_NARRATIVE_JOURNEY4_F4D','student_release':False,'preview_release':True,
 'polished_journeys':4,'polished_scenes':29,'polished_checkpoint_count':10,'narrative_story_files':4,
 'next_required_output':'F4E polished narrative for Journey 5 after F4D prose QA and developer/classroom review',
 'next_gate':'F4E polish Journey 5 only after F4D prose QA and developer/classroom review'
})
(U2/'status-f4d.json').write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; c=json.loads(cp.read_text(encoding='utf-8'))
for u in c['units']:
    if u['unit_id']=='unit-2':
        u.update({'status':'F4D_JOURNEY4_POLISHED_PREVIEW','journey_count':4,'scene_count':29,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEYS1_4_POLISHED_F4D','polished_journeys':4,'polished_scenes':29})
cp.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
files=['journeys/U2-J4.json','journeys-f4d.json','status-f4d.json']
lock={'schema':'memory-palace-v2-unit2-f4d-content-lock-1.0','unit_id':'unit-2','stage':'F4D','student_release':False,'files':{f:sha(U2/f) for f in files}}
(U2/'content-lock-f4d.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit2-f4d-release-manifest-1.0','unit_id':'unit-2','stage':'F4D','student_release':False,'preview_release':True,'polished_journeys':4,'polished_scenes':29,'journey_4_records':sum(len(s['object_ids']) for s in scenes),'journey_4_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'next_stage':'F4E_JOURNEY5'}
(U2/'f4d-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Built Unit 2 F4D:',len(scenes),'Journey 4 scenes',sum(len(s['object_ids']) for s in scenes),'knowledge records',sum(bool(s['checkpoint']) for s in scenes),'checkpoints')
