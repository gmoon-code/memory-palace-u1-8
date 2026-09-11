from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
briefs=json.loads((U2/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
jbriefs=json.loads((U2/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
B={s['locus_id']:s for s in briefs if s['journey_id']=='U2-J5'}
J5=next(j for j in jbriefs if j['journey_id']=='U2-J5')

GUIDE={
 'name':'Dr. Nia Park','role':'cell-systems investigator',
 'visual':'navy field jacket, clear safety glasses, and a compact tablet displaying a transparent map of the cell',
 'story_job':'Nia keeps the route physically clear, asks you to predict what will happen, and names scientific terms only after the defining structure or action is visible.'
}

route=[
 {'scene_index':0,'locus':'Concentration Ramp','short':'Concentration Ramp','floor':'Upper concourse','symbol':'↘'},
 {'scene_index':1,'locus':'Active Transport Lift','short':'Active Lift','floor':'Powered crossing deck','symbol':'⇧'},
 {'scene_index':2,'locus':'Facilitated Diffusion Corridor','short':'Facilitated Corridor','floor':'Protein-assisted passage','symbol':'⇢'},
 {'scene_index':3,'locus':'Channel Turnstiles','short':'Channel Turnstiles','floor':'Ion gate bank','symbol':'║'},
 {'scene_index':4,'locus':'Carrier Shuttle','short':'Carrier Shuttle','floor':'Binding shuttle bay','symbol':'⇄'},
 {'scene_index':5,'locus':'Aquaporin Floodgate','short':'Aquaporin Floodgate','floor':'Water express gate','symbol':'💧'},
 {'scene_index':6,'locus':'Bulk Cargo Dock','short':'Bulk Cargo Dock','floor':'Vesicle freight deck','symbol':'◉'},
 {'scene_index':7,'locus':'Endocytosis Intake Bays','short':'Intake Bays','floor':'Specialized intake deck','symbol':'⊂'},
 {'scene_index':8,'locus':'Electrical Pump Control','short':'Pump Control','floor':'Voltage control room','symbol':'⚡'},
 {'scene_index':9,'locus':'Proton Cotransport Platform','short':'Cotransport Platform','floor':'Plant transport platform','symbol':'H⁺'},
]

ZONE_COPY={
'U2-L30':[
 ('left','Crowded platform','●●●','A dense crowd of identical green solute particles fills the left platform. A concentration meter above them reads HIGH, but no directional arrow pushes the particles.'),
 ('center','Random-motion ramp','↔','A transparent middle zone lets the same particles jitter in every direction. Counters record crossings left-to-right and right-to-left without changing the particles’ motion.'),
 ('right','Sparse platform','●','Only a few green particles occupy the right platform. Its concentration meter reads LOW, creating a visible difference between the two sides.'),
],
'U2-L31':[
 ('left','Low-concentration loading bay','●','A blue cargo token waits among relatively few identical tokens on the low-concentration side of the membrane.'),
 ('center','ATP-powered transporter lift','ATP','A membrane protein spans the barrier like a lift. An ATP socket and moving protein panels make the energy use and conformational change visible.'),
 ('right','High-concentration unloading bay','●●●','Many matching cargo tokens already occupy the destination, so adding another token here builds or maintains the concentration difference.'),
],
'U2-L32':[
 ('left','High-concentration cargo line','▰▰▰','Large polar blue cargo tokens crowd the left side. The concentration display points downhill toward the right, yet the hydrophobic membrane blocks direct passage.'),
 ('center','Protein-assisted corridor','▥','A specific membrane transport protein provides a protected route through the hydrophobic interior. No ATP socket lights during this crossing.'),
 ('right','Low-concentration destination','▰','Only a few matching cargo tokens wait on the right side, so movement through the protein follows the existing concentration gradient.'),
],
'U2-L33':[
 ('left','Ion waiting rail','Na⁺ K⁺','Charged sodium and potassium tokens stop at the membrane surface because the hydrophobic interior does not provide a favorable route for them.'),
 ('center','Gated hydrophilic pore','║','A narrow water-friendly channel spans the membrane. A gate can open or close in response to a stimulus while preserving a hydrophilic passage through the bilayer.'),
 ('right','Polarization meter','⚡','A voltage and charge-separation display changes as ions redistribute across the membrane, linking ion movement to membrane polarization.'),
],
'U2-L34':[
 ('left','Specific binding pocket','◇','One solute fits into a shaped binding site exposed on the left side of the carrier protein. Other cargo tokens do not fit the same site.'),
 ('center','Conformation chamber','⟳','The carrier closes around the bound solute and changes shape. At no point does it become a continuously open tunnel through the membrane.'),
 ('right','Release platform','◆','The binding site opens toward the opposite side, releases the solute, and the carrier returns to its starting conformation.'),
],
'U2-L35':[
 ('left','Water reservoir','💧💧💧','A large reservoir of silver water droplets presses against the membrane. Some water can cross the bilayer, but the current demand is far higher.'),
 ('center','Aquaporin bank','||||','Many narrow aquaporin channels create high-throughput water pathways across the membrane while preserving channel selectivity.'),
 ('right','Receiving reservoir','💧💧💧','Water rapidly accumulates on the receiving side through the aquaporin routes while the ion tokens remain outside this demonstration.'),
],
'U2-L36':[
 ('left','Endocytosis dock','⊂','The plasma membrane bends inward around an oversized external cargo crate until the membrane edges meet and pinch off a vesicle inside the cell.'),
 ('center','Vesicle freight lane','○','Membrane-bound vesicles move through the freight lane while an energy indicator remains active for the bulk-transport machinery.'),
 ('right','Exocytosis dock','⊃','An internal vesicle approaches the plasma membrane, fuses with it, and releases its cargo into the extracellular space.'),
],
'U2-L37':[
 ('left','Phagocytosis bay','◉','A large solid particle is surrounded by the cell membrane and enclosed in a large vesicle that can later be routed toward lysosomal digestion.'),
 ('center','Pinocytosis bay','••','Small portions of extracellular fluid and dissolved solutes enter in many tiny vesicles without selecting one specific dissolved ligand.'),
 ('right','Receptor-mediated bay','Y•','Specific ligands bind matching membrane receptors, become concentrated together, and enter after the receptor-rich membrane region invaginates.'),
],
'U2-L38':[
 ('left','Sodium export counter','3 Na⁺ →','A counter flashes three yellow Na⁺ tokens moving from the cytoplasmic side to the extracellular side during each completed pump cycle.'),
 ('center','Na⁺/K⁺ ATPase and voltage meter','ATP ⚡','The membrane-spanning pump hydrolyzes ATP, changes conformation, and sits beside a voltage meter that tracks charge separation across the membrane.'),
 ('right','Potassium import counter','← 2 K⁺','A second counter flashes two violet K⁺ tokens moving from the extracellular side into the cytoplasm during the same cycle.'),
],
'U2-L39':[
 ('left','ATP-powered proton pump','ATP → H⁺','A proton pump in the plant-cell membrane uses ATP to move red H⁺ tokens outward, building a proton difference across the membrane.'),
 ('center','High-H⁺ energy reservoir','H⁺H⁺H⁺','The outside of the membrane accumulates H⁺ and positive charge. The concentration and electrical differences together store electrochemical potential energy.'),
 ('right','H⁺/sucrose symporter','H⁺ + sucrose →','H⁺ flows back into the cell through one coupled transporter, and a green sucrose token travels inward with it even when sucrose is moving uphill.'),
],
}

CAST={
'U2-L30':[
 ('green solute particles','scientific parts','many identical green spheres moving continuously and unpredictably','make random molecular motion visible while crossing counters reveal net movement'),
 ('concentration meters','scientific instrument','large HIGH and LOW displays above the two platforms','make the concentration difference visible without acting as a force'),
 ('colored cargo case','continuity object','a clear case containing green solute, blue polar cargo, Na⁺, K⁺, water, H⁺, and sucrose tokens','travel through the hub so direction, energy use, and transport structure can be compared across the same route')],
'U2-L31':[
 ('blue cargo token','continuity object','a large blue polar token marked with a destination on the crowded side','make movement against a concentration difference visible'),
 ('ATP token','scientific part','a glowing ATP disk that fits into the transporter control','provide direct metabolic energy for the powered transport cycle'),
 ('active transport protein','scientific part','a membrane-spanning protein whose shape changes after ATP use','move cargo across the membrane in a powered process and help maintain gradients')],
'U2-L32':[
 ('large polar cargo','continuity object','blue polar cargo tokens that cannot enter the hydrophobic membrane interior directly','show why a downhill gradient can still require protein assistance'),
 ('facilitated-diffusion protein','scientific part','a membrane protein forming a selective route through the bilayer','allow a suitable solute to cross down its gradient without direct ATP use'),
 ('ATP monitor','scientific instrument','a dark energy panel beside the corridor','make the absence of direct metabolic-energy input visible during this passive process')],
'U2-L33':[
 ('Na⁺ and K⁺ tokens','scientific parts','bright charged ion tokens that stop at the hydrophobic membrane surface','show why ions need hydrophilic protein routes'),
 ('gated channel protein','scientific part','a membrane-spanning pore with a water-friendly interior and a movable gate','provide selective ion passage when the gate is open'),
 ('polarization meter','scientific instrument','a membrane voltage display with charge markers on both sides','show that ion redistribution can change charge separation across the membrane')],
'U2-L34':[
 ('specific solute','continuity object','one shaped cargo token that fits the carrier binding pocket','demonstrate selective binding before transport'),
 ('carrier protein','scientific part','a membrane protein with an alternating-access binding pocket','bind a solute, change conformation, release it on the other side, and reset'),
 ('open-pore warning sign','misconception guard','a crossed-out drawing of a permanently open tunnel','keep the carrier distinct from a channel')],
'U2-L35':[
 ('water molecules','scientific parts','many silver droplets moving rapidly and continuously','make high-volume water movement visible'),
 ('aquaporins','scientific parts','a bank of narrow water-channel proteins spanning the membrane','greatly increase membrane permeability to water'),
 ('ion tokens','comparison parts','Na⁺ and K⁺ markers held beside the water channels','show that the water-channel demonstration does not become a general ion pore')],
'U2-L36':[
 ('oversized cargo crate','continuity object','a red crate far larger than any protein channel or carrier','force the system to use membrane remodeling and vesicles'),
 ('plasma membrane','scientific part','a flexible phospholipid boundary that can bend inward or fuse with vesicles','form vesicles during endocytosis and merge with vesicles during exocytosis'),
 ('vesicles','scientific parts','small membrane-bound freight bubbles carrying cargo','move bulk material into or out of the cell'),
 ('energy indicator','scientific instrument','a glowing cellular-energy meter beside the freight lane','show that bulk transport requires energy')],
'U2-L37':[
 ('large solid particle','scientific cargo','a dark bead much larger than dissolved molecules','trigger engulfment in the phagocytosis bay'),
 ('extracellular fluid droplets','scientific cargo','small clear droplets containing mixed dissolved solutes','show nonspecific fluid uptake during pinocytosis'),
 ('specific ligand and receptor','scientific parts','matching red ligand tokens and Y-shaped membrane receptors','show selective concentration before receptor-mediated endocytosis')],
'U2-L38':[
 ('Na⁺ tokens','scientific parts','three yellow sodium ions loaded from the cytoplasmic side each cycle','be exported by the Na⁺/K⁺ ATPase'),
 ('K⁺ tokens','scientific parts','two violet potassium ions loaded from the extracellular side each cycle','be imported by the Na⁺/K⁺ ATPase'),
 ('Na⁺/K⁺ ATPase','scientific part','a membrane-spanning ATPase that alternates access after phosphorylation changes','use one ATP per cycle to maintain Na⁺ and K⁺ gradients'),
 ('voltage meter','scientific instrument','a membrane-potential display coupled to charge-separation markers','show the electrogenic effect and the contribution of unequal ion distributions to membrane potential')],
'U2-L39':[
 ('proton pump','scientific part','an ATP-driven membrane protein moving red H⁺ tokens outward','build a proton electrochemical gradient'),
 ('H⁺ gradient','scientific state','many red H⁺ tokens concentrated on the outside with a positive-charge indicator','store potential energy in concentration and charge differences'),
 ('H⁺/sucrose symporter','scientific part','one carrier binding H⁺ and sucrose for coupled inward movement','use downhill H⁺ movement to drive uphill sucrose uptake'),
 ('sucrose token','continuity object','a green sugar block that cannot reach its required intracellular concentration alone','make the uphill coupled transport visible')],
}

NARR={
'U2-L30':{
 'title':'When random motion creates a direction','kicker':'The station looks sloped, but no invisible force is pushing molecules downhill.',
 'paragraphs':[
  'The doors from the Membrane Border Terminal open onto a high glass concourse called the **Gradient Transit Hub**. The first thing you notice is the crowd. Hundreds of identical green particles pack the platform on your left. Only a handful occupy the platform on your right. Between them stretches a transparent middle zone painted with a dark-to-light gradient so the difference is easy to see. Dr. Nia Park sets a clear cargo case beside you. Inside are the colored tokens you will use throughout the hub. She points to the crowded left platform, then the sparse right one. “Before we touch a pump or a protein,” she says, “we need to understand what movement does by itself.”',
  'Nia freezes the green particles. The left side remains crowded and the right side remains sparse. That difference in concentration across space is a **concentration gradient**. Across real cell membranes, selective permeability can allow solute concentration gradients to form and persist. The colored floor here is only a map of that difference. It does not pull anything. Nia taps her tablet and releases the particles. Every green sphere begins jittering unpredictably. Some move right. Some move left. Some reverse direction almost immediately. Nothing in the motion looks purposeful.',
  'Two counters begin recording crossings through the center. Because so many more particles start on the crowded side, more particles happen to cross from left to right during each interval than cross from right to left. The individual motions remain random, yet the population develops a clear **net movement** toward the lower-concentration side. Nia waits until the counters make the pattern undeniable. “That net movement produced by random molecular motion is **diffusion**,” she says. “The concentration gradient gives us the direction of the net change even though individual molecules keep moving in every direction.”',
  'As the right platform fills, the difference between the two sides shrinks. Eventually the crossing counters settle into a new pattern. Green particles still dart left and right continuously, but the number crossing one way is matched by the number crossing the other way. The distribution has approached **dynamic equilibrium**. Motion has not stopped. The net directional change has. Nia leaves both counters running so you can watch the equal traffic continue.',
  'No ATP light has turned on anywhere in the scene. Net movement down the concentration gradient occurs without direct metabolic-energy input. This is **passive transport** when it occurs across a membrane. Nia lifts one blue cargo token from the case and places it on the sparse side. Its destination display flashes on the crowded platform. “Now the easy direction is wrong for our goal,” she says. A powered lift rises from the floor ahead. “We need a different kind of transport.”'
 ],
 'close':'The hub’s first rule is fixed in your mind. Random molecular motion produces diffusion, downhill net movement can be passive, and equilibrium still contains constant molecular motion.',
 'images':{
  'Concentration gradients':'a crowded green platform opposite a sparse green platform with no force arrow between them',
  'Diffusion':'green particles moving randomly both directions while the crossing counter shows greater net movement from crowded to sparse',
  'Passive transport':'the unpowered crossing route carrying net traffic down the concentration gradient while the ATP panel remains dark'
 }
},
'U2-L31':{
 'title':'The lift that spends ATP','kicker':'A cargo token must reach the crowded side, so the hub has to pay for the trip.',
 'paragraphs':[
  'The blue cargo token rolls onto the **Active Transport Lift**. The loading bay on your left contains only a few matching tokens. The unloading bay on your right is already crowded with them. A concentration display above the two sides makes the problem obvious. If this cargo were allowed to follow the same downhill pattern you just watched, net movement would favor the opposite direction. Nia locks the token into the lift’s membrane transporter. “This route has work to do,” she says.',
  'At the center of the barrier, the transporter looks like a protein-shaped elevator with doors that can face only one side at a time. Nia inserts a glowing ATP disk into the control socket. The protein changes conformation. Its left-facing pocket closes around the cargo, internal panels shift, and the pocket opens toward the crowded right side. The blue token is released among many identical tokens. The ATP indicator dims as the cycle completes.',
  'Nia runs the cycle again so the relationship is visible rather than merely stated. Direct metabolic-energy input changes the transporter’s state and allows cargo movement that builds or maintains a gradient. This is **active transport**. ATP is one common source of the **energy for active transport**, and **active transport proteins** provide the membrane machinery that performs the crossing. The protein itself remains part of the membrane. Only its conformation changes during the cycle.',
  'The concentration display is useful, but Nia adds another panel showing electrical charge. “Low concentration to high concentration is a common way to recognize active transport,” she says. “For ions, the full driving force can include both concentration and electrical differences.” She leaves the electrochemical panel glowing beside the lift. The central rule is energy input, not a single oversimplified arrow.',
  'The blue token reaches its destination, and the lift shuts down. A second blue traveler arrives with a completely different problem. Its concentration is high on the left and low on the right, so its net movement can be downhill. Even so, the traveler stops at the hydrophobic membrane interior because it is large and polar. Nia points toward a protein-lined corridor. “This one has the right direction already,” she says. “It needs a route through the barrier.”'
 ],
 'close':'The powered lift leaves one clean distinction. Active transport uses metabolic energy and membrane proteins to perform work such as building or maintaining concentration and electrochemical gradients.',
 'images':{
  'Active transport':'a blue cargo token carried by a membrane-protein lift from a sparse side toward a crowded side after ATP is used',
  'Energy for active transport':'a glowing ATP disk consumed as the transport protein changes conformation',
  'Active transport proteins':'a membrane-spanning transporter changing shape around cargo during a powered cycle'
 }
},
'U2-L32':{
 'title':'A protein route with no ATP toll','kicker':'The cargo is already moving downhill, yet the bilayer itself is still an obstacle.',
 'paragraphs':[
  'The **Facilitated Diffusion Corridor** begins with a line of large polar blue travelers on your left. Only a few matching travelers wait on the right. The concentration gradient points clearly toward the right. Nia lets one token approach the membrane without assistance. It reaches the phospholipid surface and stops. The traveler has a favorable downhill direction, but the hydrophobic core of the bilayer still presents an unfavorable chemical environment.',
  'A membrane protein in the center opens an internal route. The blue token enters the protein instead of entering the fatty-acid interior. It emerges on the low-concentration side. A second follows. Then a third. The concentration display steadily moves toward a more even distribution. Beside the corridor, the ATP monitor remains completely dark. No ATP is being consumed at this route.',
  'Nia taps the protein. “Movement down a gradient can still need help crossing the membrane,” she says. **Facilitated diffusion** uses membrane proteins to enable substances that cannot readily cross the lipid bilayer to move down their gradient. These **facilitated diffusion proteins** include channels and other transport proteins. Large polar molecules can therefore cross by facilitated diffusion without direct energy input when their movement is downhill.',
  'The scene makes two ideas separate. Protein assistance answers the question “How does this substance get through the hydrophobic membrane?” Energy use answers the question “Is the cell directly spending metabolic energy to drive this transport?” Here the answer to the first is a membrane protein. The ATP panel shows that the answer to the second is no. The process remains passive.',
  'Ahead, the corridor splits into two visibly different machines. On the left, charged ions wait before a narrow gated pore. On the right, a shaped binding shuttle turns from side to side. Nia rolls the cargo case toward the fork. “Both are proteins,” she says. “Their mechanisms are different. Watch the geometry.”'
 ],
 'close':'Facilitated diffusion is now anchored to a specific combination. The solute moves down its gradient, receives protein assistance through the membrane, and does not require direct ATP use.',
 'images':{
  'Facilitated diffusion proteins':'a large polar blue traveler crossing through a membrane transport protein while the ATP monitor stays dark',
  'Large polar facilitated diffusion':'many large polar travelers moving from a crowded side to a sparse side through protein-assisted passage without ATP consumption'
 }
},
'U2-L33':{
 'title':'The water-lined gate for charged travelers','kicker':'An ion cannot enter the hydrophobic core, so the membrane opens a selective hydrophilic path.',
 'paragraphs':[
  'You take the left branch into the **Channel Turnstiles**. Bright yellow Na⁺ tokens and violet K⁺ tokens line the waiting rail. Each token carries an obvious charge mark. Nia releases one toward the phospholipid bilayer. It reaches the membrane surface and stops at the hydrophobic interior. The problem is no longer size alone. A charged ion interacts strongly with water and does not readily enter the nonpolar core of the lipid bilayer.',
  'At the center, a membrane-spanning protein contains a narrow water-friendly passage. Its interior is lined with polar regions instead of fatty-acid tails. Nia activates the gate. A selected ion passes through the hydrophilic pore while an unmatched token remains outside. This is an **ion channel**, a type of **channel protein**. Channel proteins provide hydrophilic passageways for specific ions or molecules, and many channels are gated by chemical or physical stimuli.',
  'The gate closes when Nia changes the signal. It opens again when the signal is restored. The ATP display beside the channel never lights. The ions move according to their electrochemical driving force through the open pore. The channel provides the route. It does not act like the ATP-powered lift from the previous deck.',
  'On the right wall, a polarization meter begins to shift as ions redistribute. One side of the membrane becomes relatively more positive or negative than the other. Nia points from the moving ions to the changing meter. Ion movement can contribute to **membrane polarization**, meaning a separation of charge across the membrane. The exact voltage depends on multiple ion gradients and permeabilities, but this scene shows how moving charged particles can alter the electrical difference.',
  'A new cargo token reaches the fork behind you. It is uncharged and fits no open pore. Beside the channel bank, a solid protein shuttle rotates one face toward the incoming solute. Nia gestures to the moving pocket. “Now compare an open passageway with a protein that has to bind its traveler first.”'
 ],
 'close':'The ion turnstile leaves a precise image. A channel is a selective hydrophilic passage through the membrane, many channels can gate open or closed, and ion movement can change membrane polarization.',
 'images':{
  'Ion channels':'charged Na⁺ and K⁺ tokens using a selective membrane channel instead of entering the hydrophobic lipid core',
  'Channel protein':'a membrane-spanning water-lined pore with a visible gate opening and closing',
  'Membrane polarization':'a voltage meter changing as unequal charged ions redistribute across the membrane'
 }
},
'U2-L34':{
 'title':'The shuttle that changes shape','kicker':'This protein never becomes an open tunnel. It binds, turns, releases, and resets.',
 'paragraphs':[
  'The **Carrier Shuttle** sits immediately beside the channel bank, which makes the comparison easy. The channel behind you still looks like a pore through the membrane. The carrier in front of you looks solid. On its left-facing surface is a shaped binding pocket. Nia places several different cargo tokens near it. Only one fits the pocket closely enough to bind.',
  'The moment the correct solute settles into the site, the carrier closes around it. The left opening disappears. Internal sections of the protein shift, and the entire protein changes conformation. For a moment the solute is enclosed within the protein. Then a new opening appears on the right side. The solute is released there, and the protein returns to its original left-facing state.',
  'Nia repeats the cycle in slow motion. Bind. Change conformation. Expose the binding site to the opposite side. Release. Reset. This is the defining action of a **carrier protein**. Carrier proteins bind specific solutes and change conformation to move them across the membrane. The important mental picture is alternating access. The carrier never forms an open tunnel through the membrane.',
  'In this particular corridor, the carrier is participating in facilitated diffusion, so the solute is traveling down its concentration gradient and no ATP is consumed at the carrier. Nia leaves a small note on the display that carrier-shaped transporters can also participate in other transport mechanisms elsewhere. The structure alone does not automatically tell you whether a process is passive or active. The direction, energy source, and mechanism matter together.',
  'A sudden alarm interrupts the demonstration. A wall of silver water droplets surges into the next chamber. The bare membrane allows some water movement, but the flow meter says the system needs much faster exchange. A bank of narrow channels opens ahead like floodgates. Nia points to the water. “Same membrane,” she says. “Very different throughput problem.”'
 ],
 'close':'The carrier is fixed as a binding machine rather than a pore. Specific solute binding triggers a conformational change that exposes the solute to the opposite side and then resets the protein.',
 'images':{
  'Carrier protein':'one solute binding a shaped pocket, becoming enclosed as the protein changes conformation, and being released when the pocket opens to the opposite side'
 }
},
'U2-L35':{
 'title':'The water express gates','kicker':'Water already has some direct permeability, but the cell suddenly needs far more flow.',
 'paragraphs':[
  'The floor slopes into the **Aquaporin Floodgate**. A reservoir of silver water droplets fills the left side. On the right, another reservoir is draining rapidly. Between them lies a membrane with only its phospholipid bilayer exposed. A few water molecules cross, but the flow meter stays far below the demand line. Nia does not label the bilayer “waterproof.” Instead, she points to the slow trickle. Water can cross a lipid bilayer to some extent, yet many cells need much faster water movement.',
  'A bank of narrow membrane channels rises through the center. Their gates open together, and the scene changes immediately. Water molecules stream through the channels in large numbers. The receiving reservoir fills so quickly that the flow meter jumps into the safe range. These specialized water channels are **aquaporins**. Aquaporins facilitate movement of large quantities of water across membranes.',
  'Nia holds a Na⁺ token beside one of the channels. It does not join the water stream in this demonstration. The nearby Na⁺ and K⁺ ions remain outside the route. The aquaporin’s job here is high water permeability, not a general open doorway for every dissolved substance. The visual distinction matters because “channel” describes a structural strategy while each channel still has its own selectivity.',
  'You compare the current scene with the previous ones. The carrier shuttle bound one solute at a time and changed shape. The ion channel provided a hydrophilic pore for selected charged travelers. The aquaporin bank now provides high-throughput water passage. Three proteins, three visibly different transport problems, all embedded in the same basic membrane.',
  'Then the water alarm stops and a red cargo crate arrives. It is enormous, far larger than any channel or carrier. The crate bumps against the membrane and blocks the walkway. Nia looks toward a freight dock where the plasma membrane itself can bend and fuse. “For cargo this large,” she says, “the membrane has to move.”'
 ],
 'close':'Aquaporins remain easy to recover as specialized water channels that greatly increase water movement across membranes while leaving the bilayer itself only partly permeable to water.',
 'images':{
  'Aquaporins':'a bank of narrow membrane water channels carrying a rapid stream of silver water molecules while ion tokens remain outside the route'
 }
},
'U2-L36':{
 'title':'When the membrane becomes the vehicle','kicker':'The cargo is too large for any protein passage, so the boundary bends, pinches, and fuses.',
 'paragraphs':[
  'The colored cargo case clicks into a rail at the **Bulk Cargo Dock**, and the red crate inside it is released onto the platform. It is so large that the channel and carrier models from the previous rooms look microscopic beside it. On the left, the plasma membrane begins to curve inward around the external crate. The indentation deepens until the edges of membrane nearly meet above it. Then the membrane pinches off, sealing the crate inside a new membrane-bound vesicle in the cell.',
  'Nia freezes the image at the moment the vesicle separates. “The plasma membrane folded inward and formed a vesicle around material from outside,” she says. The process is **endocytosis**. The cargo did not pass through a protein pore. A portion of the membrane itself became the vesicle boundary.',
  'The new vesicle enters the center freight lane. An energy indicator remains active while cytoskeletal and membrane-remodeling machinery handles the cargo. Bulk transport moves large substances or large quantities of material and requires cellular energy. That requirement connects both directions of the freight system.',
  'On the right, a different vesicle approaches the plasma membrane from inside the cell. Its membrane makes contact with the plasma membrane, the two membranes fuse, and the vesicle opens to the exterior. The internal cargo spills into the extracellular space while the vesicle membrane becomes part of the plasma membrane. This outward process is **exocytosis**. Internal vesicles fuse with the plasma membrane and release material from the cell.',
  'Nia runs the two events side by side. Left, membrane bends inward and pinches off around external material. Right, an internal vesicle fuses outward and releases its contents. Both are energy-requiring bulk-transport processes. The route forward then divides the intake side into three smaller bays. The signs above them show a large solid particle, extracellular fluid, and a ligand bound to a receptor. “Endocytosis has several forms,” Nia says. “The cargo and selectivity will tell you which one you are watching.”'
 ],
 'close':'The freight dock makes bulk transport a membrane-remodeling event. Endocytosis forms inward vesicles, exocytosis fuses outward vesicles, and both require cellular energy.',
 'images':{
  'Bulk transport energy':'an active energy meter glowing while vesicles bud, move, and fuse during bulk transport',
  'Endocytosis':'the plasma membrane wrapping an external red cargo crate and pinching off a vesicle inside the cell',
  'Exocytosis':'an internal vesicle fusing with the plasma membrane and releasing its cargo outside the cell'
 }
},
'U2-L37':{
 'title':'Three ways to bring material in','kicker':'All three bays use endocytosis, but the cargo and selectivity make the mechanisms distinct.',
 'paragraphs':[
  'The **Endocytosis Intake Bays** are arranged side by side so you can compare them without changing locations. The left bay contains one large dark particle. The center bay contains only extracellular fluid with many dissolved substances mixed together. The right bay contains a small number of bright red ligands that match Y-shaped receptors in the membrane. Nia asks you to keep the three cargo types in view before any names appear.',
  'The left membrane extends around the large particle until it encloses the whole object in a large vesicle. The vesicle moves inward toward a lysosome-routing sign. Nia labels this form **phagocytosis**. Phagocytosis is endocytosis of large particles, and in many animal cells the resulting vesicle can fuse with a lysosome for digestion. The memorable feature is the large solid cargo being engulfed.',
  'At the center bay, the membrane repeatedly forms small inward vesicles containing samples of the extracellular fluid and whatever dissolved solutes happen to be present in those samples. No single ligand is selected for concentration. Nia names this **pinocytosis**, the nonspecific uptake of extracellular fluid and dissolved solutes into small vesicles. She leaves the membrane machinery visually generic because pinocytosis can occur through several molecular mechanisms and is not defined by one mandatory coat protein.',
  'At the right bay, the story changes before the membrane bends. Red ligands bind matching membrane receptors. The receptor-ligand complexes gather into the same region, concentrating those particular ligands. Only then does the membrane invaginate and form a vesicle. This is **receptor-mediated endocytosis**. The defining feature is selective concentration through receptor binding before internalization.',
  'All three bays close at once. Nia points left to right. Large particle engulfment. Nonspecific fluid uptake. Specific ligand concentration through receptors. The names are now attached to visible differences in cargo and mechanism. As the last vesicle disappears into the hub, the lights flicker. The voltage map on Nia’s tablet collapses toward zero, and an alarm points to the electrical pump control room.'
 ],
 'close':'The intake deck separates three forms of endocytosis by what actually happens. Phagocytosis engulfs large particles, pinocytosis samples extracellular fluid nonspecifically, and receptor-mediated endocytosis selectively concentrates receptor-bound ligands.',
 'images':{
  'Phagocytosis':'a cell membrane engulfing one large solid particle into a large vesicle routed toward lysosomal digestion',
  'Pinocytosis':'many small vesicles taking in samples of extracellular fluid and dissolved solutes without selecting one specific ligand',
  'Receptor-mediated endocytosis':'specific ligands binding membrane receptors, clustering together, and entering in a receptor-rich vesicle'
 }
},
'U2-L38':{
 'title':'Three sodium out, two potassium in','kicker':'One ATP-powered cycle moves unequal charge and helps rebuild the membrane’s electrical landscape.',
 'paragraphs':[
  'The **Electrical Pump Control** room is dark except for a voltage meter drifting toward zero. A transparent animal-cell membrane fills the center wall. Inside, the normal Na⁺ and K⁺ distributions are fading. On the left, a sodium export counter waits at zero. On the right, a potassium import counter does the same. Nia opens the cargo case and releases yellow Na⁺ tokens and violet K⁺ tokens into the demonstration.',
  'Three Na⁺ ions bind the pump from the cytoplasmic side. One ATP is hydrolyzed. The membrane protein changes conformation and releases all three sodium ions to the extracellular side. The left counter flashes **3 Na⁺ out**. Then two K⁺ ions bind from the extracellular side. The pump changes state again and releases both potassium ions into the cytoplasm. The right counter flashes **2 K⁺ in**. The protein resets for another cycle.',
  'Nia lets the cycle repeat until the numbers become rhythmic. Three out. Two in. One ATP. This protein is the **Na⁺/K⁺ pump**, also called the Na⁺/K⁺ ATPase. The **Na⁺/K⁺ ATPase stoichiometry** is three sodium ions exported and two potassium ions imported for each ATP hydrolyzed. Because three positive charges move out while only two positive charges move in, each cycle produces a net outward movement of one positive charge.',
  'The voltage meter responds. A pump that generates voltage by moving net charge is an **electrogenic pump**. Unequal ion distributions and separation of charge across a membrane contribute to the **membrane potential**, the voltage across that membrane. Nia leaves other ion channels visible on the side of the model. “The sodium-potassium pump contributes to these gradients and to membrane voltage,” she says. “The entire resting membrane potential reflects more than this pump alone.”',
  'The room brightens as the ion gradients recover. The restored gradients also represent stored electrochemical energy that other cellular processes can use. A final alarm points to a plant-cell platform farther down the hub. There, a sucrose token needs to move into a cell against its concentration gradient, yet the sucrose transporter has no ATP socket. Nia picks up a red H⁺ token. “The cell can spend energy earlier,” she says, “store it in a gradient, and use that gradient later.”'
 ],
 'close':'Pump control leaves one repeating cycle and one electrical consequence. Each ATP moves 3 Na⁺ out and 2 K⁺ in, producing net outward positive charge while maintaining ion gradients that contribute to membrane potential.',
 'images':{
  'Na+/K+ pump':'a membrane ATPase cycling three yellow Na⁺ outward and two violet K⁺ inward',
  'Membrane potential':'a voltage meter responding to unequal ion distributions and charge separation across the membrane',
  'Electrogenic pump':'the pump moving a net one positive charge outward per completed cycle',
  'Na+/K+ ATPase stoichiometry':'a synchronized display reading one ATP, 3 Na⁺ out, 2 K⁺ in, net +1 outward'
 }
},
'U2-L39':{
 'title':'Spend ATP first, spend the gradient later','kicker':'The sucrose transporter has no ATP socket, yet sucrose still moves uphill by coupling to H⁺ moving downhill.',
 'paragraphs':[
  'The final platform belongs to a plant cell. A green sucrose token waits outside the membrane, but the concentration display shows that sucrose must enter a side where sucrose is already more concentrated. Direct diffusion will not accomplish that. Nia points to the sucrose transporter on the right. There is no ATP socket on it. Instead, the left side of the platform contains a different ATP-powered protein and the center contains a reservoir crowded with red H⁺ tokens.',
  'Nia starts at the left. ATP powers the first membrane protein, which moves H⁺ from the cytoplasmic side to the outside of the cell. As the pump repeats, H⁺ becomes more concentrated outside, and the charge display also changes because protons carry positive charge. This ATP-driven protein is a **proton pump**. Proton pumps use energy to move H⁺ across membranes and establish electrochemical proton gradients.',
  'Now Nia turns off the visual noise everywhere except the center reservoir. The high external H⁺ concentration and electrical difference together represent stored potential energy. H⁺ has a favorable downhill route back into the cell. When the H⁺/sucrose transporter opens on the right, one H⁺ binds along with sucrose. The transporter changes conformation, and both move into the cell together. H⁺ travels downhill along its electrochemical gradient while sucrose is carried uphill against its own concentration gradient.',
  'The coupled process is **cotransport**. Cotransport uses the downhill movement of one solute to drive the uphill movement of another by using energy already stored in an electrochemical gradient. In this plant-cell example, the transporter is an **H⁺/sucrose symporter**, and the process is **sucrose-H⁺ symport** because H⁺ and sucrose move in the same direction through the carrier. The immediate energy for the sucrose uptake comes from H⁺ moving down its electrochemical gradient.',
  'Nia traces the energy path with one finger. ATP is hydrolyzed at the proton pump. That pump builds the H⁺ gradient. The H⁺ gradient stores potential energy. The symporter then allows H⁺ to move downhill and couples that favorable movement to uphill sucrose uptake. ATP is not hydrolyzed directly at the sucrose symporter in this example. The distinction makes the entire hub click into place.',
  'Behind you, every route lights up in sequence. Random diffusion on the concentration ramp. ATP-powered active transport. Protein-assisted facilitated diffusion. Channels, carriers, and aquaporins. Vesicle-based endocytosis and exocytosis. The electrogenic sodium-potassium pump. Finally, a proton gradient powering cotransport. The colored cargo case closes. Ahead, glass doors fog with water droplets and reveal the entrance to the Osmosis Conservatory, where the next problem is no longer simply how solutes cross, but how water movement changes entire cells.'
 ],
 'close':'The transport hub is restored with a complete energy chain. ATP powers the proton pump, the proton gradient stores electrochemical energy, and H⁺ moving downhill through a symporter drives sucrose uphill into the plant cell.',
 'images':{
  'Proton pump':'an ATP-powered membrane protein moving red H⁺ tokens outward to build a proton electrochemical gradient',
  'Cotransport':'H⁺ moving downhill through a coupled transporter while its movement drives a second solute uphill',
  'Sucrose-H+ symport':'a green sucrose token entering the plant cell in the same direction as H⁺ through an H⁺/sucrose symporter'
 }
},
}

SCENE_META={
'U2-L30':('Concentration Ramp','Upper concourse','Concentration Ramp, the upper hub concourse where a crowded high-concentration platform is fixed on your left, a transparent random-motion zone runs through the center, and a sparse low-concentration platform is fixed on your right.'),
'U2-L31':('Active Transport Lift','Powered crossing deck','Active Transport Lift, the powered crossing deck with a low-concentration loading bay on the left, an ATP-driven membrane transporter in the center, and a crowded high-concentration unloading bay on the right.'),
'U2-L32':('Facilitated Diffusion Corridor','Protein-assisted passage','Facilitated Diffusion Corridor, a membrane passage where large polar cargo starts at high concentration on the left, crosses through a transport protein in the center, and arrives at lower concentration on the right.'),
'U2-L33':('Channel Turnstiles','Ion gate bank','Channel Turnstiles, an ion-gate bank where charged travelers wait on the left, a gated hydrophilic pore spans the center membrane, and a polarization meter records charge separation on the right.'),
'U2-L34':('Carrier Shuttle','Binding shuttle bay','Carrier Shuttle, a binding bay where the carrier exposes a specific solute-binding site on the left, changes conformation in the center, and opens toward the release side on the right.'),
'U2-L35':('Aquaporin Floodgate','Water express gate','Aquaporin Floodgate, a high-flow water passage with a water reservoir on the left, a bank of narrow aquaporin channels in the center, and the receiving reservoir on the right.'),
'U2-L36':('Bulk Cargo Dock','Vesicle freight deck','Bulk Cargo Dock, the vesicle freight deck where the membrane bends inward around external cargo on the left, vesicles move through the center freight lane, and internal vesicles fuse outward on the right.'),
'U2-L37':('Endocytosis Intake Bays','Specialized intake deck','Endocytosis Intake Bays, three neighboring stations with phagocytosis fixed on the left, pinocytosis in the center, and receptor-mediated endocytosis on the right.'),
'U2-L38':('Electrical Pump Control','Voltage control room','Electrical Pump Control, a transparent animal-cell membrane station with the 3 Na⁺ export counter on the left, the Na⁺/K⁺ ATPase and voltage meter in the center, and the 2 K⁺ import counter on the right.'),
'U2-L39':('Proton Cotransport Platform','Plant transport platform','Proton Cotransport Platform, a plant-cell membrane station with an ATP-powered proton pump on the left, the stored H⁺ electrochemical gradient in the center, and an H⁺/sucrose symporter on the right.'),
}

CHECKPOINT_HINTS={
'U2-L30':'Picture the two crossing counters after the concentrations have evened out. Green particles still move left and right continuously, but the number crossing each direction is balanced, so there is no net movement.',
'U2-L38':'Return to the synchronized pump display. One ATP lights the cycle, three yellow sodium ions leave the cell, two violet potassium ions enter, and the net charge counter shows one positive charge moved outward.',
'U2-L39':'Trace the energy path from left to right. ATP is spent at the proton pump, H⁺ accumulates outside and stores electrochemical energy, then H⁺ flows downhill through the symporter while sucrose travels with it uphill.'
}

lids=[f'U2-L{i}' for i in range(30,40)]
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
    scene={
      'scene_index':idx,'locus':locus,'title':n['title'],'scene_kicker':n['kicker'],'location_description':locdesc,
      'scene_layout':{'orientation':b['orientation_sentence'],'zones':zones},
      'cast':cast,'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':beats,'memory_snapshot':snaps,
      'checkpoint':checkpoint,'checkpoint_object_id':b['primary_knowledge_id'],'checkpoint_prompt':qr.get('candidate_prompt','') if checkpoint else '',
      'checkpoint_answer':qr.get('answer','') if checkpoint else '',
      'checkpoint_hint':CHECKPOINT_HINTS.get(lid,'') if checkpoint else '',
      'next_locus':B[next_id]['scene_title'] if next_id in B else None,
      'misconception_guards':b['misconception_guards'],'required_visual':b['visual_spec'],'carry_forward':b['carry_forward']
    }
    scenes.append(scene)

journey={
 'schema':'memory-palace-v2-unit2-f4e-story-1.0','unit_id':'unit-2','palace_id':'U2-J5','journey_id':'U2-J5','palace_name':'Gradient Transit Hub',
 'story_title':'The Transit Hub With No Direction Signs','tagline':'Follow the same colored cargo through downhill diffusion, powered transport, protein-assisted routes, vesicle docks, ion pumps, and gradient-powered cotransport until every movement has a visible cause.',
 'guide':GUIDE,'premise':J5['premise'],'mission':J5['mission'],
 'finale':'The hub runs again only after each route is matched to its actual driving force and structure. Random motion produces diffusion, ATP powers active transport and pumps, membrane proteins provide selective routes, vesicles move bulk cargo, and electrochemical gradients store energy that can drive cotransport.',
 'estimated_minutes':20,'scene_count':len(scenes),'checkpoint_count':sum(bool(s['checkpoint']) for s in scenes),
 'learner_rule':'Read or listen and keep the colored cargo case moving with you. For every crossing, first notice the direction, then the structure used, then whether energy is spent directly or stored in a gradient. Quick Recall is optional during the first pass.',
 'route_orientation':'The Gradient Transit Hub is one continuous multilevel station. Begin with the crowded and sparse platforms of the Concentration Ramp, descend to the ATP-powered lift, pass through the facilitated-diffusion corridor, compare channels and carriers, cross the aquaporin and vesicle decks, then finish in the electrical pump room and plant cotransport platform. The same colored cargo case keeps direction, energy use, and transport mechanism comparable from scene to scene.',
 'route':route,'scenes':scenes,'student_release':'PILOT_PREVIEW_F4E','narrative_standard':'V2-NARRATIVE-3.0-F4E'
}

(U2/'journeys').mkdir(parents=True,exist_ok=True)
(U2/'journeys'/'U2-J5.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

js=[json.loads((U2/'journeys'/f'U2-J{i}.json').read_text(encoding='utf-8')) for i in range(1,5)]+[journey]
def card(j): return {k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
registry={
 'schema':'memory-palace-v2-unit2-f4e-registry-1.0','course_id':'ap-biology','unit_id':'unit-2','unit_title':'Cells','narrative_standard':'V2-NARRATIVE-3.0-F4E',
 'journey_count':5,'scene_count':sum(j['scene_count'] for j in js),'checkpoint_count':sum(j['checkpoint_count'] for j in js),
 'guided_journeys':[card(j) for j in js]
}
(U2/'journeys-f4e.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U2/'status-f4d.json').read_text(encoding='utf-8'))
status.update({
 'status':'F4E_JOURNEY5_POLISHED_PREVIEW','pipeline_stage':'POLISHED_NARRATIVE_JOURNEY5_F4E','student_release':False,'preview_release':True,
 'polished_journeys':5,'polished_scenes':39,'polished_checkpoint_count':13,'narrative_story_files':5,
 'next_required_output':'F4F polished narrative for Journey 6 after F4E prose QA and developer/classroom review',
 'next_gate':'F4F polish Journey 6 only after F4E prose QA and developer/classroom review'
})
(U2/'status-f4e.json').write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; c=json.loads(cp.read_text(encoding='utf-8'))
for u in c['units']:
    if u['unit_id']=='unit-2':
        u.update({'status':'F4E_JOURNEY5_POLISHED_PREVIEW','journey_count':5,'scene_count':39,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEYS1_5_POLISHED_F4E','polished_journeys':5,'polished_scenes':39})
cp.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
files=['journeys/U2-J5.json','journeys-f4e.json','status-f4e.json']
lock={'schema':'memory-palace-v2-unit2-f4e-content-lock-1.0','unit_id':'unit-2','stage':'F4E','student_release':False,'files':{f:sha(U2/f) for f in files}}
(U2/'content-lock-f4e.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit2-f4e-release-manifest-1.0','unit_id':'unit-2','stage':'F4E','student_release':False,'preview_release':True,'polished_journeys':5,'polished_scenes':39,'journey_5_records':sum(len(s['object_ids']) for s in scenes),'journey_5_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'next_stage':'F4F_JOURNEY6'}
(U2/'f4e-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Built Unit 2 F4E:',len(scenes),'Journey 5 scenes',sum(len(s['object_ids']) for s in scenes),'knowledge records',sum(bool(s['checkpoint']) for s in scenes),'checkpoints')
