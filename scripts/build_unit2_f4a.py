from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
U2 = ROOT/'content'/'ap-biology'/'unit-2'
BRIEFS = json.loads((U2/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS = json.loads((U2/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J1 = next(j for j in JBRIEFS if j['journey_id']=='U2-J1')
B = {s['locus_id']:s for s in BRIEFS if s['journey_id']=='U2-J1'}

GUIDE = {
    'name':'Dr. Nia Park',
    'role':'cell-systems investigator',
    'visual':'navy field jacket, clear safety glasses, and a compact tablet displaying a transparent map of the cell',
    'story_job':'Nia keeps the route physically clear, asks you to notice what each structure is doing, and gives the scientific name only after the defining action is visible.'
}

route = [
 {'scene_index':0,'locus':'Cell Entry Atrium','short':'Entry Atrium','floor':'Ground floor','symbol':'◉'},
 {'scene_index':1,'locus':'Nuclear Archive','short':'Nucleus','floor':'Inner east wing','symbol':'◎'},
 {'scene_index':2,'locus':'Nucleolus Assembly Room','short':'Nucleolus','floor':'Inside nucleus','symbol':'●'},
 {'scene_index':3,'locus':'Ribosome Platforms','short':'Ribosomes','floor':'Cytoplasmic floor','symbol':'••'},
 {'scene_index':4,'locus':'Endomembrane Map Room','short':'Route Map','floor':'Central concourse','symbol':'↻'},
 {'scene_index':5,'locus':'Rough ER Assembly Hall','short':'Rough ER','floor':'North processing wing','symbol':'≋'},
 {'scene_index':6,'locus':'Smooth ER Detox Lab','short':'Smooth ER','floor':'North processing wing','symbol':'∿'},
 {'scene_index':7,'locus':'Golgi Receiving Stack','short':'Golgi cis','floor':'West stack entrance','symbol':'☰'},
 {'scene_index':8,'locus':'Golgi Dispatch Floor','short':'Golgi trans','floor':'West stack exit','symbol':'⇢'},
 {'scene_index':9,'locus':'Lysosome Recycling Bay','short':'Lysosome','floor':'Recycling wing','symbol':'♻'},
 {'scene_index':10,'locus':'Vacuole Reservoir Gallery','short':'Vacuoles','floor':'Reservoir gallery','symbol':'◯'},
 {'scene_index':11,'locus':'Peroxisome Oxidation Booth','short':'Peroxisome','floor':'Isolated safety booth','symbol':'⚗'},
 {'scene_index':12,'locus':'Cytoskeleton Framework','short':'Cytoskeleton','floor':'Outer framework hall','symbol':'⌗'},
]


ZONE_COPY = {
'U2-L01':[
 ('left','Prokaryote bay','◌','A compact prokaryotic cell model with DNA exposed in a nucleoid region and no membrane-bound nucleus.'),
 ('center','Shared essentials turntable','◎','Plasma membrane, cytosol, genetic material, and ribosomes rotate under one white inspection light.'),
 ('right','Eukaryote bay','◉','A larger cutaway cell with DNA enclosed in a nucleus and multiple membrane-bound organelles.')],
'U2-L02':[
 ('left','Double nuclear envelope','║','Two closely spaced membranes form the protective wall around the genetic archive.'),
 ('center','Chromosome archive','≋','Coiled chromosomes remain protected inside the central nuclear chamber.'),
 ('right','Nuclear pore checkpoint','⊙','A protein-lined pore spans the envelope and regulates macromolecular traffic in both directions.')],
'U2-L03':[
 ('left','rRNA transcription desk','≈','Fresh ribosomal RNA strands emerge within the dense nucleolus.'),
 ('center','Subunit assembly bench','●','rRNA and imported proteins combine into large and small ribosomal subunits.'),
 ('right','Pore exit lane','→','Completed ribosomal subunits move out of the nucleus toward the cytoplasm.')],
'U2-L04':[
 ('left','Free-ribosome platform','••','Ribosomes suspended in cytosol translate mRNA and release proteins into the cytosolic side.'),
 ('center','mRNA translation stage','≈','A coded mRNA ribbon passes through a ribosome as amino acids join into a growing protein.'),
 ('right','Bound-ribosome platform','≋','Ribosomes attached to rough ER feed many membrane, secreted, and endomembrane proteins into the ER route.')],
'U2-L05':[
 ('left','Synthesis side','←','Nuclear envelope and ER begin the connected internal membrane route.'),
 ('center','Endomembrane network map','↻','ER, Golgi, vesicles, lysosomes, vacuoles, nuclear envelope, and plasma membrane connect into one trafficking system.'),
 ('right','Destination branches','→','Transport routes split toward lysosomes, vacuoles, the plasma membrane, and secretion.')],
'U2-L06':[
 ('left','Ribosome-studded surface','••','Bound ribosomes sit on the cytosolic face of rough-ER membrane.'),
 ('center','Flattened cisterna and lumen','▱','A flattened ER membrane sac encloses a lumen physically separated from the cytosol.'),
 ('right','Budding vesicle dock','○','A patch of ER membrane buds away carrying the red-tracked protein cargo toward the Golgi.')],
'U2-L07':[
 ('left','Lipid synthesis bench','◇','Smooth-ER membrane enzymes assemble lipid molecules along the left workbench.'),
 ('center','Smooth tubular ER','∿','Branching membrane tubules have no bound ribosomes on their surface.'),
 ('right','Detox and storage modules','⚗','Detoxification chemistry runs beside calcium-storage and carbohydrate-metabolism modules.')],
'U2-L08':[
 ('left','Incoming ER vesicle lane','○','The red-tracked protein cargo arrives inside a transport vesicle from the ER.'),
 ('center','Stacked Golgi cisternae','☰','Distinct flattened membrane sacs remain visibly separate while forming the Golgi stack.'),
 ('right','Cis receiving face','⇥','The side facing incoming ER traffic receives the vesicle.')],
'U2-L09':[
 ('left','Modification stations','⚙','Cargo is chemically processed as it advances through the Golgi.'),
 ('center','Tag-and-package station','▣','The red protein receives destination information and is enclosed in a new vesicle.'),
 ('right','Trans dispatch face','⇢','Outgoing vesicles leave toward specific cellular destinations or the plasma membrane.')],
'U2-L10':[
 ('left','Autophagy delivery lane','◫','A damaged cellular component is enclosed and brought toward the lysosome.'),
 ('center','Lysosomal chamber','♻','Hydrolytic enzymes digest delivered material inside a membrane-enclosed compartment.'),
 ('right','Recycling bins and apoptosis panel','→','Reusable breakdown products exit while a separate panel marks lysosomal participation in programmed cell death.')],
'U2-L11':[
 ('left','Small vacuole gallery','○','Small storage sacs and a newly formed food vacuole illustrate several animal-cell roles.'),
 ('center','Plant central reservoir','◯','A huge central vacuole stores water and solutes and presses outward to support turgor.'),
 ('right','Contractile vacuole pump','◉','A freshwater-protist vacuole repeatedly fills, contracts, and expels excess water.')],
'U2-L12':[
 ('left','Oxidation enzymes','⚗','Peroxisomal enzymes transfer hydrogen to oxygen during oxidative reactions.'),
 ('center','Peroxisome chamber','◌','A small membrane-bound compartment keeps oxidative chemistry localized.'),
 ('right','Catalase safety station','✦','Catalase breaks down accumulating hydrogen peroxide before it reaches dangerous levels.')],
'U2-L13':[
 ('left','Actin tension field','╱','Thin actin microfilaments bear tension, change cell shape, and form a contractile ring.'),
 ('center','Microtubule rail hub','⊛','Hollow microtubules radiate from an organizing center and carry motor-protein cargo.'),
 ('right','Intermediate-filament braces','#','Stable rope-like fibers reinforce shape and brace organelles and the nuclear envelope.')],
}

NARR = {
'U2-L01': {
 'title':'Two Cells at the Gate',
 'kicker':'Before you repair the complex, decide what kind of cell you have entered.',
 'paragraphs':[
  "The outer doors seal behind you with a soft hiss. Dr. Nia Park raises her tablet, and the dark atrium becomes a three-part inspection hall. On your **left**, a small cell model sits in a low glass bay. Directly **ahead**, four objects rotate on a bright circular platform. On your **right**, a larger cutaway cell rises almost to the ceiling. Nia does not name either model yet. \"First find what makes both of them cells,\" she says.",
  "The center platform lights one object at a time. A thin **plasma membrane** ring forms the boundary. Inside it, a clear **cytosol** pool fills the interior. A coil of **genetic material** appears, followed by clusters of tiny **ribosomes**. The same four features glow inside both the left and right models. Nia taps the platform. \"Any structure we call a **cell** has these core features. Cells are the basic structural and functional units of organisms.\" The first distinction is therefore not that one model is a cell and the other is something less complete. Both are fully functioning cells.",
  "Now the left bay opens. Its DNA coil lies in an open **nucleoid region** with no membrane wrapped around it. There are no membrane-bound organelles inside. Nia finally gives it a name: **prokaryotic cell**. Bacteria and Archaea have this organization. The right model opens next. Its DNA is enclosed inside a clearly bounded nucleus, and membrane-bound compartments occupy the cytoplasm. This is a **eukaryotic cell**.",
  "The difference stays visible because the shared features remain lit in both models while the nucleus glows only on the right. Then that nucleus begins flashing red. A warning on Nia's tablet reads ARCHIVE TRAFFIC BLOCKED. \"That is our first real failure,\" she says. The right-hand model expands until its nuclear boundary becomes a doorway large enough to enter."
 ],
 'close':'You cross into the eukaryotic model with the shared-cell essentials still glowing behind you. Ahead, the double boundary of the nucleus is locked around its genetic archive.',
 'images':{
   'Cell':'the four shared essentials glowing in both models',
   'Prokaryotic cell':'DNA lying in an open nucleoid region on the left',
   'Eukaryotic cell':'DNA enclosed by a nucleus with membrane-bound organelles on the right'
 }
},
'U2-L02': {
 'title':'The Locked Genetic Archive',
 'kicker':'The nucleus protects information without cutting itself off from the rest of the cell.',
 'paragraphs':[
  "You are now inside the right-hand cell model, standing directly in front of the **Nuclear Archive**. The boundary fills your view. It is not one wall. Two closely spaced membrane layers wrap the entire chamber, like a double glass shell. Through the transparent layers you can see thick coils of chromosomes stored safely inside. Nia runs one finger along both membranes. \"This double boundary is the **nuclear envelope**,\" she says. \"The compartment inside is the **nucleus**, where most of a eukaryotic cell's genetic material is kept.\"",
  "Cargo is jammed on both sides of the envelope. On the cytoplasmic side, large proteins wait to enter. On the nuclear side, RNA-containing cargo waits to leave. Then a circular gate spanning the two membranes opens. It is not a tear in the envelope. It is a built structure made of proteins: a **nuclear pore complex**. One permitted cargo passes through, then another. The chromosomes themselves remain inside the archive while selected macromolecules move between nucleus and cytoplasm.",
  "Nia reverses the traffic arrows on her tablet so you can see movement in both directions. \"A pore is regulated traffic, not a permanently open hole,\" she says. The image matters: the nucleus is a protected compartment, yet it still communicates with the cytoplasm through controlled exchange. The cell does not need to send its DNA out through the door in order to use genetic information.",
  "A low mechanical hum begins deeper in the archive. Past the chromosomes, a dense round region glows like a workshop inside the nucleus. Small unfinished pieces are piling up there, and the pile is growing. Nia points toward it. \"Those pieces belong to the machines that will read RNA outside this archive. We need to see how they are built.\""
 ],
 'close':'You leave the pore gate behind and move deeper into the nucleus toward the dense circular workshop at its center.',
 'images':{
   'Nucleus':'chromosomes protected inside a double-membrane archive',
   'Nuclear pore complex':'a protein-lined gate spanning both nuclear-envelope membranes and regulating two-way macromolecular traffic'
 }
},
'U2-L03': {
 'title':'Building the Protein-Making Machines',
 'kicker':'Inside the nucleus, one dense region assembles the parts of ribosomes.',
 'paragraphs':[
  "The **Nucleolus Assembly Room** is unmistakable once you step inside. It has no membrane around it. Instead, it is a dense working zone within the nucleus. On your left, fresh strands of ribosomal RNA slide from an rRNA transcription desk. At the center bench, protein pieces arriving from the cytoplasm are sorted into trays. On the right, two sizes of unfinished ribosomal subunits line up beside a lane leading back to the nuclear pores.",
  "Nia picks up one new RNA strand. \"This region is the **nucleolus**. Ribosomal RNA, or **rRNA**, is transcribed here.\" She lays the rRNA onto the central bench. Imported proteins lock around it, and the assembly resolves into a small subunit and a large subunit. The point is visible before the label appears: ribosomes are not made only of protein. **Ribosomes are composed of rRNA and protein.**",
  "The two subunits remain separate as they move toward a nuclear pore. Nia stops you from picturing a warehouse full of finished ribosomes inside the nucleolus. \"The nucleolus assembles ribosomal subunits. Those subunits are exported, and functional ribosomes operate outside this room.\" A wall panel then lights up with cells from bacteria, archaea, plants, fungi, and animals. Every one contains ribosomes. Their universal presence is one line of evidence connecting known life through **common ancestry**.",
  "The subunits pass through the pore and disappear into the cytoplasm. Nia's tablet tracks them as two bright dots. Outside the nucleus, a messenger RNA strand arrives. The dots move toward it from opposite directions. \"Now we get to watch what a ribosome actually does,\" Nia says, following them through the exit lane."
 ],
 'close':'The ribosomal subunits leave the nucleus and approach an mRNA strand on the cytoplasmic production floor.',
 'images':{
   'Nucleolus':'a dense, non-membrane-bound nuclear workshop where rRNA is transcribed and subunits are assembled',
   'Ribosome composition':'rRNA and protein pieces combining into large and small ribosomal subunits',
   'Ribosomes and common ancestry':'ribosomes glowing inside cells across Bacteria, Archaea, and Eukarya'
 }
},
'U2-L04': {
 'title':'Two Ribosome Platforms, One Job',
 'kicker':'The same protein-making machine can work in different places, and location changes where many products go.',
 'paragraphs':[
  "You emerge from the nucleus onto a broad cytoplasmic floor. Two translation platforms face one another. **Free ribosomes** float in the cytosol on your left. On your right, ribosomes sit on the outer surface of a folded membrane system. Between them, a long **mRNA** ribbon moves slowly across a central stage. The ribosomal subunits from the nucleolus meet the mRNA and form a working ribosome around it.",
  "The mRNA ribbon begins feeding through the ribosome. Amino acids arrive one after another and are joined into a growing polypeptide. Nia lets the action run on both platforms at once. \"This is the basic **ribosome function** wherever the ribosome is located: ribosomes synthesize proteins according to messenger RNA sequences.\" The machinery is fundamentally the same on both sides.",
  "Now the destinations split. A protein made by a **free ribosome** on the left is released into the cytosol; many such proteins function there, while others can later be targeted to organelles such as the nucleus, mitochondria, chloroplasts, or peroxisomes. On the right, a ribosome attached to rough ER produces a protein destined for secretion, a membrane, or another compartment of the endomembrane system. Nia colors that newly forming protein bright red on her tablet so you can follow it. The red color is only a tracking aid; the molecule itself is the protein cargo.",
  "The red protein begins entering the rough-ER route as it is synthesized. An alarm changes from ROUTING UNKNOWN to ROUTING IDENTIFIED. But the path beyond the ribosome is still scrambled. A wall panel lights up with disconnected organelles and vesicles. \"We know where the cargo starts,\" Nia says. \"Now we need to restore the system that moves it.\""
 ],
 'close':'The red protein cargo leaves the ribosome platform and rolls toward a wall-sized map of the cell’s internal membrane-traffic system.',
 'images':{
   'Ribosome function':'mRNA passing through a ribosome while amino acids are assembled into a protein',
   'Free ribosomes':'a cytosolic ribosome releasing protein into the cytosol with later targeting arrows',
   'Bound ribosomes':'a ribosome attached to rough ER feeding a red-tracked protein into the endomembrane route'
 }
},
'U2-L05': {
 'title':'The Route That Makes Organelles a System',
 'kicker':'A list of compartments becomes useful when you can see how material moves among them.',
 'paragraphs':[
  "The **Endomembrane Map Room** is circular, with one enormous cell diagram wrapped around the walls. At first it is useless. The nuclear envelope glows in one corner, the ER in another, the Golgi far away, and vesicles drift without arrows. Lysosomes, vacuoles, and the plasma membrane appear as isolated icons. The red protein cargo sits motionless at the bottom of the map because no complete route exists.",
  "Nia begins reconnecting the diagram. A line runs from the **nuclear envelope** into the **endoplasmic reticulum**, then toward the **Golgi complex**. Small **transport vesicles** carry material between stations. Branches lead to **lysosomes**, **vacuoles**, and the **plasma membrane**. \"Together, these components form the **endomembrane system**,\" she says. The central idea is cooperation: these membrane-bound components work together to modify, package, and transport proteins, lipids, and polysaccharides within the cell and, for some products, out of it.",
  "The map changes from a list into a moving network. The red protein travels along the restored arrows. Nearby lipid and polysaccharide cargo take their own routes. Across the center of the room, the ER is drawn not as one tiny bag but as a widespread membrane network extending through the cell. That network helps organize internal space, contributes to cell shape, and participates in intracellular transport.",
  "One route on the map begins flashing more brightly than the others. It leads to a set of flattened membranes covered with ribosomes. The red protein is already approaching that station. Nia points to the first processing stop. \"If we want to understand why this route works, we need to step inside the membrane network itself.\""
 ],
 'close':'The map zooms into the ribosome-studded portion of the ER, and the wall opens into a full-sized rough-ER assembly hall.',
 'images':{
   'Endomembrane system membership':'nuclear envelope, ER, Golgi, vesicles, lysosomes, vacuoles, and plasma membrane connected by traffic arrows',
   'Endomembrane system function':'protein, lipid, and polysaccharide cargo moving through modification, packaging, and transport routes',
   'ER support and transport':'a broad ER membrane network extending through the cell interior'
 }
},
'U2-L06': {
 'title':'Inside the Rough ER',
 'kicker':'The rough ER is both a protein-production surface and a membrane-enclosed compartment.',
 'paragraphs':[
  "The **Rough ER Assembly Hall** looks like a series of wide, flattened corridors stacked beside one another. Tiny ribosomes cover the membrane surface facing the cytosol, giving the hall its rough appearance. At the center, Nia shines her tablet through one membrane sac so you can see the enclosed interior. \"Each flattened sac is a **cisterna**,\" she says. \"The space enclosed by the ER membrane is the **ER lumen**.\"",
  "A bound ribosome on the cytosolic surface resumes translating the mRNA from the previous room. The red protein grows while being directed into or through the rough-ER membrane. Nia freezes the view at the membrane boundary. Cytosol remains outside the cisterna; the ER lumen remains inside. The separation is the point. The **rough ER** contributes to protein synthesis while its membranes create a distinct compartment where newly synthesized products can enter the endomembrane pathway.",
  "Dozens of ribosomes continue working on the outer surface, but none are floating inside the lumen. Nia taps one dark dot on the membrane. \"The ribosomes make this region look rough because they are attached to the cytosolic face. The lumen is the enclosed space on the other side.\" A small patch of ER membrane curves outward with the red cargo inside, pinches off, and becomes a transport vesicle.",
  "The vesicle starts toward the Golgi, but a side branch of the ER remains lit. Its membrane is tubular rather than flattened, and its surface is smooth because no ribosomes are attached. A chemical hazard alarm flashes above that branch. The next problem is not protein routing at all."
 ],
 'close':'The red cargo vesicle continues toward the Golgi while you and Nia turn briefly into the ribosome-free tubular branch of the ER.',
 'images':{
   'Rough ER':'ribosomes attached to the cytosolic surface of flattened ER cisternae',
   'ER cisternae/lumen':'a membrane sac enclosing an ER lumen clearly separated from the surrounding cytosol'
 }
},
'U2-L07': {
 'title':'The Smooth ER’s Quiet Chemistry',
 'kicker':'Removing ribosomes changes the appearance, and this branch specializes in a different set of jobs.',
 'paragraphs':[
  "The **Smooth ER Detox Lab** branches from the rough-ER hall like a network of clean, curved tubes. The first thing you notice is what is missing: there are no ribosomes attached to the membrane. Nia runs her light along the unbroken tubular surface. \"This is **smooth ER**. The absence of bound ribosomes makes the surface look smooth, but its functions are biochemical, not cosmetic.\"",
  "On the left, membrane enzymes assemble lipid molecules and feed them into the growing membrane system. A warning container marked TOXIN slides onto the right-hand bench. Detoxification enzymes modify the incoming chemical, making its processing safer for the cell. These two jobs anchor the scene: **lipid synthesis** and **cellular detoxification** are major functions of smooth ER.",
  "Then Nia opens two smaller modules to show why smooth ER can look different in different cell types. One module stores **calcium ions**, a particularly important function in certain cells such as muscle cells. Another displays reactions involved in **carbohydrate metabolism**. Nia leaves the modules side by side rather than presenting them as universal duties. \"Different cells emphasize different smooth-ER functions. Do not imagine every smooth ER doing all of these jobs equally.\"",
  "Through the glass wall you can still see the red protein vesicle from the rough ER moving along the main corridor. It passes the detox lab without stopping and approaches a curved stack of flattened membrane sacs. One side of the stack faces the incoming ER traffic like a receiving dock."
 ],
 'close':'You rejoin the red cargo vesicle just as it reaches the receiving side of the Golgi complex.',
 'images':{
   'Smooth ER':'a ribosome-free tubular membrane network carrying out lipid synthesis and detoxification',
   'Smooth ER additional functions':'separate calcium-storage and carbohydrate-metabolism modules illustrating cell-type-dependent functions'
 }
},
'U2-L08': {
 'title':'Finding the Golgi’s Receiving Side',
 'kicker':'The Golgi has direction. Start by watching where ER cargo arrives.',
 'paragraphs':[
  "The **Golgi Receiving Stack** rises in front of you like a set of shallow curved trays, each one separated from the next. Nia asks you to count the gaps. They matter. Each flattened membrane sac is a distinct **Golgi cisterna**, not one continuous chamber winding through the stack. The red ER transport vesicle approaches from your left and stops at the nearest face.",
  "That incoming vesicle fuses at the receiving side. Nia draws a bright arrow from the ER to this face and only then names it: the **cis face** of the Golgi. The orientation becomes difficult to reverse once you have watched the traffic arrive. Cis is the side that receives vesicles coming from the ER.",
  "As the cargo enters, the whole organelle becomes easier to define. The **Golgi complex** is a membrane-bound structure made of a series of flattened membrane sacs. The stacked geometry creates an ordered processing route. The red protein does not simply appear at a shipping desk; it enters on one side and moves through a structured series of compartments.",
  "A scanner above the stack detects that the protein still lacks its final chemical modifications and destination information. The receiving dock closes behind you. Across the far side of the cisternae, another dock opens toward several possible destinations. Nia points across the stack. \"If cis is where cargo comes in, we now need to see what happens before it leaves.\""
 ],
 'close':'You follow the red protein across the Golgi stack toward modification stations and the outgoing face on the opposite side.',
 'images':{
   'Golgi structure':'a stack of separate, flattened Golgi membrane sacs',
   'Cisternae':'distinct curved sacs with visible spaces between them',
   'Golgi cis face':'an ER-derived vesicle docking at the incoming face of the Golgi'
 }
},
'U2-L09': {
 'title':'Modify, Tag, Package, Dispatch',
 'kicker':'The Golgi is more than a shipping dock; cargo changes while it moves through the stack.',
 'paragraphs':[
  "The **Golgi Dispatch Floor** begins on the far side of the same stack. Modification stations line your left. The red protein arrives still carrying the fluorescent tracking color from Nia's tablet, but its molecular form is being processed as it moves from one Golgi region to the next. Enzymes alter newly synthesized cellular products, and the cargo becomes ready for its final destination.",
  "At the center station, a destination marker is added and the product is sorted. Nia emphasizes the sequence by tracing it with her finger: **modify**, then **sort**, then **package**. A patch of Golgi membrane curves around the red protein and pinches off as a new vesicle. This is why describing the Golgi only as a post office is incomplete. The Golgi also chemically modifies products before trafficking them.",
  "The vesicle reaches the outgoing side of the stack. This is the **trans face**. Unlike the cis face that received ER cargo, the trans face sorts and dispatches vesicles toward cellular destinations or toward the plasma membrane. Nia's map shows several branches. The red protein's tag sends it toward the plasma membrane, restoring one of the missing routes that triggered the complex's alarm.",
  "As the dispatch system returns to normal, a different warning starts flashing beside the Golgi. The problem is no longer a newly made protein. A damaged organelle has been isolated in a double-membrane packet, but the recycling route is stalled. Nia turns toward the adjacent bay. \"New cargo is moving again. Now we deal with old material that needs to be broken down.\""
 ],
 'close':'The red cargo leaves toward its destination while you follow a damaged cellular component into the recycling wing.',
 'images':{
   'Golgi processing':'a red protein moving through sequential modification stations across the Golgi stack',
   'Golgi trafficking':'modified cargo receiving a destination tag and being packaged into a vesicle',
   'Golgi trans face':'the outgoing Golgi face branching toward multiple cellular destinations'
 }
},
'U2-L10': {
 'title':'The Recycling Chamber',
 'kicker':'Damaged material is enclosed, delivered, digested, and reused.',
 'paragraphs':[
  "The **Lysosome Recycling Bay** is darker than the production floors. On your left, a damaged cell component has already been wrapped inside a double-membrane packet. In the center sits a small membrane-enclosed chamber filled with hydrolytic enzymes. On the right, bins marked REUSE wait empty. Nia identifies the central chamber only after you see its job begin: this is a **lysosome**.",
  "The double-membrane packet carries the damaged component to the lysosome. That delivery is part of **autophagy**. During autophagy, damaged cellular material is enclosed and delivered to lysosomes for enzymatic breakdown and recycling. The membranes meet, and the damaged material enters the digestive compartment rather than spilling into the cytosol.",
  "Inside, hydrolytic enzymes break large molecules into smaller products. The reuse bins on the right begin filling with molecules the cell can use again. The lysosome is therefore a membrane-enclosed digestive compartment, not a loose bag of enzymes drifting through the cell. Nia keeps the membrane boundary visible while digestion proceeds so the chemistry remains compartmentalized.",
  "A separate control panel on the wall is labeled **apoptosis**, or programmed cell death. It is not the same process as autophagy. Nia points to it without turning the lysosome into a cartoon 'suicide bag.' Lysosomes can participate in regulated programmed cell death, while the scene you just watched was autophagic recycling. As the recycled products leave, reservoir doors open farther down the corridor."
 ],
 'close':'The damaged component has been broken down and reusable products move onward toward storage and other cellular needs.',
 'images':{
   'Lysosome digestion':'a membrane-enclosed lysosome containing hydrolytic enzymes and digesting delivered material',
   'Lysosome apoptosis':'a separate regulated programmed-cell-death control linked to lysosomal function',
   'Autophagy':'a damaged organelle enclosed and delivered to a lysosome for breakdown and recycling'
 }
},
'U2-L11': {
 'title':'Reservoirs with Different Jobs',
 'kicker':'“Vacuole” names a family of membrane-bound sacs, not one identical structure in every cell.',
 'paragraphs':[
  "The corridor opens into the **Vacuole Reservoir Gallery**. Three very different reservoirs occupy the room. On the left, several small membrane-bound sacs hold stored materials. In the center, one enormous water-filled chamber rises several stories high. On the right, a small reservoir repeatedly fills with water, contracts, and empties through an outlet. Nia lets all three cycle at once before giving them a shared name: **vacuoles** are membrane-bound sacs with diverse roles.",
  "The giant central chamber represents the **central vacuole** typical of a mature plant cell. Water and dissolved substances fill most of its volume. As water accumulates, the chamber presses outward and helps support **turgor pressure** against the cell wall. Storage and mechanical support are linked here: the central vacuole can store water, ions, pigments, and other materials while contributing to the pressure that keeps many plant tissues firm.",
  "The smaller sacs on the left represent the smaller, more numerous vacuoles commonly found in animal cells. One membrane pocket forms around engulfed food, creating a **food vacuole**. Nia routes it toward a digestive compartment, showing how a food vacuole can later fuse with a lysosome in animal cells. The important distinction is that vacuoles are not plant-exclusive structures and do not all have the same size or function.",
  "Finally, the right-hand reservoir fills until an alarm sounds, then contracts and ejects water. This is a **contractile vacuole**, used by many freshwater protists to expel excess water and maintain osmotic balance. When its cycle stabilizes, another alarm begins in a small sealed booth beyond the gallery: hydrogen peroxide is accumulating. Nia heads for the isolation door."
 ],
 'close':'You leave the varied vacuole reservoirs behind and enter a small oxidative compartment built to handle a very different chemical problem.',
 'images':{
   'Vacuole general':'several membrane-bound sacs of different sizes performing different storage or water-management roles',
   'Plant central vacuole':'a huge plant-cell reservoir filled with water and solutes and pressing outward to support turgor',
   'Animal vacuoles':'smaller, more numerous membrane sacs in an animal cell',
   'Food vacuole':'engulfed food enclosed in a vacuole and routed toward digestive compartments',
   'Contractile vacuole':'a freshwater-protist vacuole repeatedly filling and expelling excess water'
 }
},
'U2-L12': {
 'title':'The Peroxide Safety Booth',
 'kicker':'This compartment handles oxidation, not the hydrolytic digestion you just saw in lysosomes.',
 'paragraphs':[
  "The **Peroxisome Oxidation Booth** is deliberately isolated from the recycling bay. Its membrane encloses a compact set of oxidative enzymes. On the left, those enzymes transfer hydrogen from substrates to oxygen during specific metabolic reactions. A warning meter in the center immediately begins climbing as **hydrogen peroxide, H2O2**, appears as a product of the chemistry.",
  "Before the meter reaches the red zone, an enzyme station on the right activates. **Catalase** breaks down hydrogen peroxide, preventing dangerous accumulation. Nia lets you watch peroxide appear and disappear several times. The compartment's name now has something concrete attached to it: a **peroxisome** is an oxidative metabolic compartment containing enzymes that carry out oxidation reactions and enzymes such as catalase that handle hydrogen peroxide.",
  "Nia opens a window back toward the lysosome bay. In the lysosome, hydrolytic enzymes digested cellular material. Here, oxidative enzymes carry out a different kind of chemistry. The two compartments are both small and membrane-bound, which is exactly why students often confuse them, but their central jobs are not interchangeable. Lysosome means digestion and recycling. Peroxisome means oxidative metabolism and peroxide management.",
  "The peroxide meter settles to green, but the floor beneath you begins to tremble. The vibration travels through visible fibers in the walls. Cargo tracks bend, the nuclear boundary shifts slightly, and the entire operations complex seems to sag. Nia looks down at the structural map. \"Routing and chemistry are working again. The framework holding all of this in place is not.\""
 ],
 'close':'A hidden wall retracts, exposing the filament network that spans the entire cell interior.',
 'images':{
   'Peroxisome':'a membrane-bound oxidation chamber where H2O2 is generated during oxidation reactions and catalase breaks it down'
 }
},
'U2-L13': {
 'title':'The Framework That Moves',
 'kicker':'The cell’s internal support is not one scaffold; it is a dynamic network of different protein filaments.',
 'paragraphs':[
  "The final hall exposes the **cytoskeleton** instead of hiding it behind organelles. Thin tension fibers span the left wall. Hollow rails radiate through the center from an organizing hub. Rope-like cables brace the right wall and wrap around the nuclear boundary. Nia's tablet overlays the same network throughout the whole cell. \"The **cytoskeleton** is a dynamic network of protein fibers that supports cell shape, organizes contents, and contributes to intracellular and whole-cell movement.\"",
  "The center rails rebuild first. Each one is a hollow tube made of tubulin. These are **microtubules**. Motor proteins begin walking along them with vesicle cargo, turning the rails into intracellular transport tracks. A second demonstration forms a mitotic spindle, and a third shows the same kind of microtubule architecture supporting eukaryotic cilia and flagella. In this animal-cell model, many microtubules grow outward from a central **centrosome**, a microtubule-organizing center. Nia adds one caution: other eukaryotic cells can use other microtubule-organizing centers, so centrosomes are not universal to every eukaryote.",
  "On the left, the thin fibers tighten. These **microfilaments**, or **actin filaments**, bear tension and reshape the cell surface. A contraction demonstration pulls against them; then an actin ring constricts like a drawstring to model the contractile ring used during animal-cell cytokinesis. They are thinner and more flexible than the hollow microtubule tracks.",
  "The rope-like fibers on the right barely move while everything else shifts. These are **intermediate filaments**. They reinforce cell shape, help anchor organelles, and contribute to stable structures such as the nuclear lamina. The distinction is now spatial: hollow transport rails in the center, thin actin tension fibers on the left, stable rope-like intermediate filaments on the right. As each system returns to its job, the sagging complex straightens. The red protein has reached its destination, damaged material is recycled, reservoirs are stable, peroxide is controlled, and vesicles move cleanly along restored tracks. Nia's tablet finally clears the routing alarm. A new alert appears from another wing: ENERGY OUTPUT UNSTABLE. She turns toward a separate annex containing two transparent organelles—one orange and folded inside, one green and stacked."
 ],
 'close':'Cell Operations Complex is stable again. The next investigation begins in the Energy Conversion Annex, where membrane geometry controls how cells transform energy.',
 'images':{
   'Cytoskeleton':'a cell-wide network of microtubules, actin filaments, and intermediate filaments supporting organization and movement',
   'Microtubule':'a hollow tubulin rail carrying motor-protein cargo and forming spindle/cilia structures',
   'Microtubule-organizing center / centrosome':'a central animal-cell hub from which many microtubules radiate',
   'Microfilament / actin filament':'thin tension-bearing actin fibers forming a contractile ring',
   'Intermediate filament':'stable rope-like fibers bracing organelles and the nuclear envelope'
 }
},
}

# Map from brief scientific labels to student-facing beat terms. Preserve canonical science exactly.
TERM_OVERRIDES = {
 'Ribosome function':'Ribosome',
 'Ribosome composition':'Ribosome composition',
 'Ribosomes and common ancestry':'Ribosomes and common ancestry',
 'Endomembrane system membership':'Endomembrane system',
 'Endomembrane system function':'Endomembrane system function',
 'ER support and transport':'Endoplasmic reticulum (ER)',
 'ER cisternae/lumen':'Cisternae and ER lumen',
 'Smooth ER additional functions':'Smooth ER additional functions',
 'Golgi structure':'Golgi complex',
 'Golgi processing':'Golgi processing',
 'Golgi trafficking':'Golgi trafficking',
 'Lysosome digestion':'Lysosome',
 'Lysosome apoptosis':'Lysosomes and apoptosis',
 'Vacuole general':'Vacuole',
 'Plant central vacuole':'Central vacuole',
 'Animal vacuoles':'Animal-cell vacuoles',
 'Food vacuole':'Food vacuole',
 'Contractile vacuole':'Contractile vacuole',
 'Microtubule-organizing center / centrosome':'Microtubule-organizing center / centrosome',
 'Microfilament / actin filament':'Microfilament / actin filament',
}

def scene_layout_from_brief(b):
    zones=[{'position':pos,'label':label,'symbol':symbol,'description':description} for pos,label,symbol,description in ZONE_COPY[b['locus_id']]]
    return {'orientation':b['orientation_sentence'],'zones':zones}

def cast_from_brief(b):
    out=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    for c in b['stable_cast']:
        out.append({'name':c['name'],'kind':'scientific part','visual':c['visual_identity'],'job':c['job_in_scene']})
    return out

def make_scene(lid,idx):
    b=B[lid]; n=NARR[lid]
    beats=[]; snaps=[]
    for t in b['term_introductions']:
        term=TERM_OVERRIDES.get(t['canonical_term'],t['canonical_term'])
        img=n['images'].get(t['canonical_term'], n['images'].get(term, b['carry_forward']))
        beat={'object_id':t['knowledge_id'],'term':term,'story':img,'science':t['canonical_science'],'exact_name':bool(t.get('exact_name_recall')),'hint':img}
        beats.append(beat)
        snaps.append({'term':term,'meaning':t['canonical_science'],'image':img})
    qr=b['quick_recall']; cp=bool(qr.get('enabled'))
    cp_id=b['primary_knowledge_id']
    # Prefer answer-bearing target if a prompt is about a specific later term.
    if cp:
        prompt=qr['candidate_prompt']
        if lid=='U2-L04': cp_id='U2-K-074'
        if lid=='U2-L08':
            for x in b['term_introductions']:
                if 'cis face' in x['canonical_term'].lower(): cp_id=x['knowledge_id']
        if lid=='U2-L13':
            for x in b['term_introductions']:
                if x['canonical_term']=='Microtubule': cp_id=x['knowledge_id']
    else: prompt=''
    return {
      'scene_index':idx,'locus':b['scene_title'],'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['exact_location']+' — '+b['micro_anchor']+'.',
      'scene_layout':scene_layout_from_brief(b),'cast':cast_from_brief(b),
      'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':beats,'memory_snapshot':snaps,
      'checkpoint':cp,'checkpoint_object_id':cp_id,'checkpoint_prompt':prompt,'checkpoint_answer':qr.get('answer','') if cp else '','checkpoint_hint':('Picture the left cell with DNA open in the nucleoid and the right cell with DNA enclosed inside a nucleus.' if lid=='U2-L01' else 'Picture the ribosome physically attached to rough ER feeding protein into the membrane route.' if lid=='U2-L04' else 'Watch the ER vesicle arrive at the receiving side of the Golgi stack.' if lid=='U2-L08' else 'Picture the hollow center rails carrying motor-protein cargo and forming the spindle.' if lid=='U2-L13' else ''),
      'next_locus':B[b['causal_transition']['to_locus_id']]['scene_title'] if b['causal_transition']['to_locus_id'] else None,
      'misconception_guards':b['misconception_guards'],'required_visual':b['visual_spec'],
      'carry_forward':b['carry_forward']
    }

scenes=[make_scene(r['locus'].replace('','') if False else lid,i) for i,lid in enumerate(J1['route'])]
journey={
 'schema':'memory-palace-v2-unit2-f4a-story-1.0','unit_id':'unit-2','palace_id':'U2-J1','journey_id':'U2-J1',
 'palace_name':'Cell Operations Complex','story_title':'The Cell That Lost Its Routes','tagline':'Trace one protein from genetic control to processing and dispatch while repairing the cell’s recycling, storage, oxidation, and structural systems.',
 'guide':GUIDE,'premise':J1['premise'],'mission':J1['mission'],
 'finale':'The red-tracked protein reaches its destination, damaged material is recycled, water-storage systems stabilize, peroxide is controlled, and the cytoskeletal network straightens the complex. A new energy alarm then opens the route to the Energy Conversion Annex.',
 'estimated_minutes':22,'scene_count':len(scenes),'checkpoint_count':sum(1 for s in scenes if s['checkpoint']),
 'learner_rule':'Read or listen and build the room in your mind. The scientific name appears only after its structure or job becomes visible. Quick Recall is optional during the first pass.',
 'route_orientation':'The Cell Operations Complex is a transparent eukaryotic-cell facility. Enter at the ground-floor identity atrium, move inward through the nucleus, return to the cytoplasmic production floor, follow the endomembrane route through ER and Golgi, then finish in the recycling, storage, oxidation, and structural-support wings.',
 'route':route,'scenes':scenes,'student_release':'PILOT_PREVIEW_F4A','narrative_standard':'V2-NARRATIVE-3.0-F4A'
}

(U2/'journeys').mkdir(parents=True,exist_ok=True)
(U2/'journeys'/'U2-J1.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+"\n",encoding='utf-8')
registry={
 'schema':'memory-palace-v2-unit2-f4a-registry-1.0','course_id':'ap-biology','unit_id':'unit-2','unit_title':'Cells',
 'narrative_standard':'V2-NARRATIVE-3.0-F4A','journey_count':1,'scene_count':13,'checkpoint_count':4,
 'guided_journeys':[ {k:journey[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']} ]
}
(U2/'journeys-f4a.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+"\n",encoding='utf-8')
status=json.loads((U2/'status-f3.json').read_text(encoding='utf-8'))
status.update({
 'status':'F4A_JOURNEY1_POLISHED_PREVIEW','pipeline_stage':'POLISHED_NARRATIVE_PILOT_F4A','student_release':False,'preview_release':True,
 'polished_journeys':1,'polished_scenes':13,'polished_checkpoint_count':4,'narrative_story_files':1,
 'next_required_output':'F4B polished narrative for Journey 2 after F4A prose QA and developer/classroom review',
 'next_gate':'F4B polish Journey 2 only after F4A prose QA and classroom/developer review'
})
(U2/'status-f4a.json').write_text(json.dumps(status,indent=2)+"\n",encoding='utf-8')

# Update course registry status without touching Unit 1.
cp=ROOT/'content'/'ap-biology'/'course.json'
c=json.loads(cp.read_text(encoding='utf-8'))
for u in c['units']:
    if u['unit_id']=='unit-2':
        u.update({'status':'F4A_JOURNEY1_POLISHED_PREVIEW','journey_count':1,'scene_count':13,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEY1_POLISHED_F4A','polished_journeys':1,'polished_scenes':13})
cp.write_text(json.dumps(c,indent=2,ensure_ascii=False)+"\n",encoding='utf-8')

# Lock the F4A artifacts only; F1-F3 locks remain independent.
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
files=['journeys/U2-J1.json','journeys-f4a.json','status-f4a.json']
lock={'schema':'memory-palace-v2-unit2-f4a-content-lock-1.0','unit_id':'unit-2','stage':'F4A','student_release':False,'files':{f:sha(U2/f) for f in files}}
(U2/'content-lock-f4a.json').write_text(json.dumps(lock,indent=2)+"\n",encoding='utf-8')
print('Built Unit 2 F4A:', len(scenes), 'scenes', sum(1 for s in scenes if s['checkpoint']), 'checkpoints')
