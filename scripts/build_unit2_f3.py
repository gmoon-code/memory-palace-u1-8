from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
ARCH=U2/'architecture'
BRIEFS=U2/'briefs'
BRIEFS.mkdir(parents=True,exist_ok=True)
GEN='2026-09-02T06:40:00+00:00'

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,obj): Path(p).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

src=load(U2/'source/canonical-unit2-f1.json')
records={r['knowledge_id']:r for r in src['canonical_catalog']}
f2=load(ARCH/'palace-architecture-f2.json')
loci={l['locus_id']:l for l in f2['loci']}

unit_guide={
  'name':'Dr. Nia Park',
  'role':'cell-systems investigator who accompanies the learner through every Unit 2 journey',
  'visual_identity':'navy field jacket, clear safety glasses, compact tablet with a glowing cell-map display',
  'behavior_rule':'Nia points to structures, asks the learner to predict what should happen next, and names a scientific term only after the relevant action has become visible.',
  'continuity_rule':'Nia remains the same person across all seven journeys. She never becomes a mnemonic for a scientific term.'
}

journey_specs={
'U2-J1':{
 'final_working_title':'Cell Operations Complex',
 'premise':'A living-cell operations complex has suffered a routing failure. Protein cargo is being sent to the wrong places, damaged material is accumulating, and the internal support network is destabilizing.',
 'mission':'Enter through cell identity control, trace information and protein handling from nucleus to ribosome to ER to Golgi, then restore recycling, storage, oxidation, and cytoskeletal support.',
 'stakes':'If the routes remain confused, the learner cannot explain how organelle structure produces cell function.',
 'continuity_object':'a single red protein-cargo case that begins as an mRNA-directed product and is followed through the endomembrane route',
 'opening_image':'A transparent building shaped like a eukaryotic cell flickers above Nia’s tablet; several internal routes are flashing red.',
 'ending_payoff':'The red cargo case reaches its destination, damaged components are recycled, reservoirs stabilize, and the cytoskeletal rails relight across the complex.',
 'tone':'investigative, concrete, lightly suspenseful, never frantic',
},
'U2-J2':{
 'final_working_title':'Energy Conversion Annex',
 'premise':'The complex has power, but the output is unstable. Nia takes the learner into two transparent energy-conversion chambers to inspect exactly where membrane geometry supports cellular energy transformations.',
 'mission':'Map mitochondrial compartments and cristae, compare energy demand with mitochondrial abundance, then inspect chloroplast membranes, thylakoids, grana, stroma, and chlorophyll.',
 'stakes':'The learner must distinguish the two organelles by internal architecture and location of major processes, not by vague “powerhouse” or “photosynthesis organelle” slogans.',
 'continuity_object':'a pulsing energy-demand meter that changes as the learner moves between cell types and organelles',
 'opening_image':'Two enormous transparent organelles sit behind glass like working power plants, one orange and folded within, one green and stacked within.',
 'ending_payoff':'The demand meter stabilizes after the learner correctly routes each process to the membrane or compartment that supports it.',
 'tone':'industrial-scientific, visual, precise',
},
'U2-J3':{
 'final_working_title':'Scaling Observatory',
 'premise':'An observatory has enlarged a cell model until its interior is starving even though the outer surface looks enormous.',
 'mission':'Use geometric models to discover why surface area and volume scale differently, then restore exchange by changing shape and compare thermal consequences across organism sizes.',
 'stakes':'The learner must see why “bigger” does not mean proportionally more exchange surface.',
 'continuity_object':'a glowing exchange meter that turns from green to red as model size increases and back toward green when surface folds are added',
 'opening_image':'A tiny cube cell glows bright green beside an enormous identical cube whose center is dim and oxygen-starved.',
 'ending_payoff':'The giant model regains exchange capacity after the learner adds surface folds and explains the scaling rule.',
 'tone':'discovery-driven, visual, mathematical without feeling like a worksheet',
},
'U2-J4':{
 'final_working_title':'Membrane Border Terminal',
 'premise':'A molecular border terminal is admitting the wrong travelers. Nia freezes the terminal so the learner can inspect the membrane fabric, embedded proteins, identity tags, and outer plant-cell wall.',
 'mission':'Rebuild the bilayer orientation, restore fluidity, place membrane proteins correctly, distinguish recognition markers, and reopen selective passage lanes.',
 'stakes':'The learner must understand that selectivity comes from molecular properties and membrane structure, not from a membrane “deciding” what it wants.',
 'continuity_object':'a tray of test travelers—O2, CO2, H2O, NH3, glucose, Na+, and K+—used at successive checkpoints',
 'opening_image':'A flexible two-layer border ripples under bright lights while a line of differently shaped molecules waits for entry.',
 'ending_payoff':'Each traveler reaches the correct lane and the neighboring plant-cell wall reconnects through a plasmodesma.',
 'tone':'busy border-terminal mystery with clear molecular rules',
},
'U2-J5':{
 'final_working_title':'Gradient Transit Hub',
 'premise':'The transport hub has lost its direction signs. Molecules are moving randomly, pumps are stalled, and vesicle docks are jammed.',
 'mission':'Reconstruct concentration gradients, passive and active transport, facilitated diffusion, channels, carriers, aquaporins, vesicle transport, membrane potential, electrogenic pumps, and cotransport.',
 'stakes':'The learner must track direction, energy use, and the transport structure used in each case.',
 'continuity_object':'a set of colored cargo tokens whose position and energy tags are followed across every transport system',
 'opening_image':'A sloped concourse is crowded on one side and almost empty on the other; powered lifts and membrane gates stand dark.',
 'ending_payoff':'The hub runs again with downhill lanes, ATP-powered routes, vesicle docks, and coupled transport all moving in their correct directions.',
 'tone':'kinetic and mechanical, with strong directional logic',
},
'U2-J6':{
 'final_working_title':'Osmosis Conservatory',
 'premise':'A glass conservatory contains living cells in solution chambers. Several are swelling, shrinking, or losing contact with their walls because the solution controls have been mixed up.',
 'mission':'Diagnose tonicity, observe isotonic/hypertonic/hypotonic outcomes, then use water potential and osmoregulation controls to explain water movement quantitatively and conceptually.',
 'stakes':'The learner must distinguish solution labels from the direction of water movement and understand why plant and animal cells respond differently.',
 'continuity_object':'one transparent reference cell and one plant cell that reappear in each solution chamber',
 'opening_image':'Three glass rooms fog with condensation while one cell shrinks, another swells, and a plant cell presses hard against its wall.',
 'ending_payoff':'The chambers stabilize when the learner predicts water movement from water potential and restores internal balance.',
 'tone':'calm but visually dramatic laboratory greenhouse',
},
'U2-J7':{
 'final_working_title':'Compartment Origins Archive',
 'premise':'The final archive asks two linked questions: why eukaryotic cells divide chemistry into internal compartments, and where mitochondria and chloroplasts came from.',
 'mission':'Demonstrate the advantages of compartmentalization, compare prokaryotic and eukaryotic internal organization, then reconstruct endosymbiosis and examine multiple independent lines of evidence.',
 'stakes':'The learner must leave with an evidence-based evolutionary explanation, not a fantasy of organelles simply “choosing” to live inside cells.',
 'continuity_object':'an evidence case that receives one new card at each station and is sealed only when all lines of evidence agree',
 'opening_image':'Rows of archive drawers surround two illuminated cell models, one relatively open inside and one divided by internal membranes.',
 'ending_payoff':'The evidence case closes only after genomes, division, ribosomes, membranes, and modern host dependence form one coherent explanation.',
 'tone':'historical investigation grounded in visible evidence',
},
}

# Per-locus design. These are briefs, not polished student prose.
S={
'U2-L01':dict(
 orientation='You enter the ground-floor atrium. The prokaryote bay is fixed on your left, a rotating platform of features shared by all cells is directly ahead, and the eukaryote bay is fixed on your right.',
 cast=[('shared-cell essentials','four illuminated objects: plasma membrane ring, cytosol pool, genetic-material coil, ribosome dots','establish the structures found in every cell'),('prokaryotic model','small cell with no membrane-bound nucleus; DNA occupies an open nucleoid region','show the organization of Bacteria and Archaea'),('eukaryotic model','larger cutaway with DNA enclosed in a nucleus and multiple membrane-bound organelles','show eukaryotic compartmentalization')],
 before='Both inspection bays are dark, so the two cell models initially look like unlabeled silhouettes.',
 during=['Nia lights the center turntable first, revealing the four structures shared by all cells.','The left model opens to reveal DNA in a nucleoid region with no membrane-bound nucleus; the right model opens to reveal a nucleus and membrane-bound organelles.','The same plasma membrane, cytosol, genetic material, and ribosomes remain highlighted in both models so the contrast never erases their shared cellular features.'],
 after='The learner can identify a cell by shared essentials and distinguish prokaryotic from eukaryotic organization by the nucleus and membrane-bound organelles.',
 transition='The eukaryotic model’s nucleus begins flashing because its archive door is locked, pulling the route into the Nuclear Archive.',
 must_show=['all-cell common features','nucleoid without membrane-bound nucleus','nucleus plus membrane-bound organelles'],
 guards=['Do not portray prokaryotes as primitive or incomplete cells.','Do not imply only eukaryotes have DNA or ribosomes.'],
 recall=('Which feature most clearly separates the two models at this checkpoint?','Eukaryotic cells enclose DNA in a nucleus and contain membrane-bound organelles; prokaryotic cells do not have a membrane-bound nucleus.'),
 carry='All cells share core structures; internal organization distinguishes prokaryotic and eukaryotic cells.'),
'U2-L02':dict(
 orientation='Inside the right-hand cell model, you stand at a sealed nuclear archive. A double membrane is on the left wall, chromosomes fill the central chamber, and a pore-controlled checkpoint is on the right.',
 cast=[('nuclear envelope','two closely spaced membrane layers surrounding the archive','separate nuclear contents from cytoplasm'),('chromosome archive','coiled genetic material stored inside the chamber','represent most of the eukaryotic cell’s genetic material'),('nuclear pore complex','large protein-lined gate spanning the envelope','regulate movement of macromolecules between nucleus and cytoplasm')],
 before='The archive is sealed and cargo is piling up on both sides of the envelope.',
 during=['A cutaway light reveals that the boundary is a double-membrane nuclear envelope, not a single wall.','The pore complex opens selectively: permitted macromolecular cargo crosses while the chromosome archive itself remains inside.','Nia traces traffic in both directions to emphasize regulated exchange between nucleus and cytoplasm.'],
 after='The archive operates as a protected genetic compartment with controlled macromolecular traffic through nuclear pore complexes.',
 transition='A dense round workshop inside the nucleus starts sending unfinished ribosomal parts toward the pore, leading to the Nucleolus Assembly Room.',
 must_show=['double nuclear envelope','chromosomes inside nucleus','pore spanning both membranes','regulated two-way macromolecular movement'],
 guards=['Do not say DNA must leave the nucleus to be used.','Do not describe nuclear pores as permanently open holes.'],
 recall=None,
 carry='Nucleus stores most eukaryotic genetic material; nuclear pores regulate exchange.'),
'U2-L03':dict(
 orientation='Deeper inside the nucleus, a dense circular nucleolus fills the center. An rRNA desk is on the left, a subunit assembly bench is ahead, and an exit lane to nuclear pores runs right.',
 cast=[('rRNA transcripts','fresh RNA strands emerging at the left desk','supply the RNA component of ribosomes'),('imported ribosomal proteins','protein pieces delivered from the cytoplasm','combine with rRNA during subunit assembly'),('ribosomal subunits','large and small unfinished ribosome pieces','leave the nucleus and later assemble into functional ribosomes')],
 before='The assembly bench has protein parts but no rRNA, so no ribosomal subunits can be completed.',
 during=['rRNA is transcribed in the nucleolus and fed onto the center bench.','Imported proteins join the rRNA to form ribosomal subunits; Nia identifies ribosomes as structures made of rRNA and protein.','Completed subunits move toward nuclear pores, while a wall display shows ribosomes across all forms of life as evidence of common ancestry.'],
 after='The learner sees the nucleolus as an assembly region, not a membrane-bound organelle, and connects ribosome composition to universal cellular ancestry.',
 transition='The subunits exit and snap together on two translation platforms outside the nucleus.',
 must_show=['nucleolus inside nucleus','rRNA plus protein assembly','subunit export','ribosomes represented across diverse life'],
 guards=['Do not depict the nucleolus as membrane-bound.','Do not imply complete ribosomes are manufactured as finished units and stored in the nucleolus.'],
 recall=('What two kinds of material are combined to build ribosomal subunits?','rRNA and proteins'),
 carry='Nucleolus transcribes rRNA and assembles ribosomal subunits; ribosomes contain rRNA and protein.'),
'U2-L04':dict(
 orientation='Outside the nucleus, two translation platforms face each other: free ribosomes on the left, an mRNA stage in the center, and ER-bound ribosomes on the right.',
 cast=[('mRNA ribbon','long coded ribbon passing through each ribosome','provide the sequence read during protein synthesis'),('free ribosomes','ribosomes suspended in cytosol','make proteins that mainly function in cytosol or are targeted after translation to certain organelles'),('bound ribosomes','ribosomes attached to rough ER or nuclear envelope','make proteins destined for secretion, membranes, or endomembrane compartments')],
 before='The red cargo case is only an mRNA instruction ribbon; no protein product exists yet.',
 during=['Both free and bound ribosomes read mRNA and assemble amino acids into proteins.','Products from the left platform remain mainly cytosolic or receive later targeting signals.','Products from the right platform enter the endomembrane route, so the red cargo case is placed into the rough-ER pathway.'],
 after='The learner separates ribosome function from ribosome location: both synthesize proteins, while location helps determine where products go.',
 transition='The red cargo case rolls toward a wall-sized map showing the entire endomembrane route.',
 must_show=['mRNA passing through ribosome','free versus ER-bound placement','different destination arrows'],
 guards=['Do not imply free and bound ribosomes are different types of ribosome.','Do not say every free-ribosome protein remains in cytosol.'],
 recall=('Which ribosome location is most associated with proteins for secretion or membranes?','Ribosomes bound to rough ER or the nuclear envelope.'),
 carry='All ribosomes translate mRNA; location is linked to protein destination.'),
'U2-L05':dict(
 orientation='You enter a map room. Incoming synthesis routes occupy the left wall, the full endomembrane network fills the center, and outgoing transport routes branch to the right.',
 cast=[('endomembrane route map','connected diagram of nuclear envelope, ER, Golgi, vesicles, lysosomes, vacuoles, and plasma membrane','make system membership and trafficking relationships visible'),('red cargo case','the same protein product from the ribosome platform','provide one continuous object to follow through modification, packaging, and transport')],
 before='The map’s route lights are scrambled, making each organelle look isolated.',
 during=['Nia reconnects the nuclear envelope, ER, Golgi, transport vesicles, lysosomes, vacuoles, and plasma membrane as one trafficking system.','The red cargo case is routed through the system while labels show that proteins, lipids, and polysaccharides can be modified, packaged, and transported.','The ER network is shown extending through the cell, contributing to internal organization, shape, and transport.'],
 after='The route is visible as a coordinated system rather than a memorized list of organelles.',
 transition='The map highlights the first processing stop: a ribosome-studded rough-ER cisterna.',
 must_show=['all major endomembrane members','vesicle connections','ER network extending through cell'],
 guards=['Do not include mitochondria, chloroplasts, or peroxisomes as endomembrane-system members.'],
 recall=None,
 carry='Endomembrane components cooperate to modify, package, and transport cellular products.'),
'U2-L06':dict(
 orientation='At the rough-ER hall, ribosomes stud the cytosolic surface on the left, a flattened cisterna and its lumen occupy the center, and budding transport vesicles exit on the right.',
 cast=[('rough ER','flattened membrane network covered with bound ribosomes','support protein synthesis and compartmentalization'),('cisterna','one flattened ER membrane sac','create an enclosed ER lumen separate from cytosol'),('ER lumen','internal space inside the cisterna','keep newly entering material physically separated from cytosol')],
 before='The red protein cargo is exposed on the cytosolic side with no protected route forward.',
 during=['A bound ribosome feeds the growing product into/through the rough-ER membrane as the surrounding cisterna encloses a distinct lumen.','Nia traces the membrane boundary between lumen and cytosol so the learner can see compartmentalization.','A transport vesicle buds from the ER carrying cargo toward the Golgi route.'],
 after='The rough ER is recognizable by bound ribosomes and by its membranous cisternae enclosing a lumen.',
 transition='A smooth tubular branch without ribosomes runs off the hall toward a detoxification laboratory.',
 must_show=['ribosomes on cytosolic surface','cisterna membrane','ER lumen','vesicle budding'],
 guards=['Do not place ribosomes inside the ER lumen.','Do not treat “cisterna” as a separate organelle.'],
 recall=('What makes this ER region look rough?','Ribosomes bound to its cytosolic membrane surface.'),
 carry='Rough ER combines membrane-bound ribosomes with a separate lumen for protein processing/transport.'),
'U2-L07':dict(
 orientation='The route enters a smooth tubular laboratory with no ribosomes attached. Lipid synthesis is left, smooth ER tubules run through center, and detoxification, calcium, and carbohydrate stations occupy the right.',
 cast=[('smooth ER tubules','branching membrane tubes with a clean surface','provide ER membrane without attached ribosomes'),('lipid synthesis enzymes','workstations embedded in/near the smooth ER','synthesize lipids'),('detox/calcium/carbohydrate stations','cell-type-specific modules connected to the tubules','show additional smooth-ER functions')],
 before='A toxin warning is flashing while a membrane-lipid order sits unfilled.',
 during=['The smooth ER synthesizes lipid components while detoxification enzymes process the incoming chemical.','A calcium-storage module fills, and a carbohydrate-metabolism panel activates to show that additional functions depend on cell type.','Nia contrasts the smooth surface with the ribosome-studded rough ER just visited.'],
 after='Smooth ER is anchored to lipid synthesis and detoxification, with calcium storage and carbohydrate metabolism as context-dependent functions.',
 transition='A vesicle from the rough ER rolls past the lab toward a stack of flattened receiving sacs.',
 must_show=['no ribosomes on smooth ER','tubular membrane network','multiple function modules'],
 guards=['Do not imply every smooth ER performs every additional function equally.'],
 recall=None,
 carry='Smooth ER lacks bound ribosomes and supports lipid synthesis, detoxification, and other cell-specific functions.'),
'U2-L08':dict(
 orientation='At the Golgi entrance, an ER vesicle approaches from the left, a stack of distinct flattened sacs rises in the center, and the cis receiving face is fixed on the right side of the incoming route.',
 cast=[('Golgi cisternae','separate flattened membrane sacs stacked like shallow curved trays','form the Golgi structure'),('cis face','receiving side oriented toward incoming ER traffic','accept vesicles arriving from the ER'),('ER transport vesicle','small membrane sphere carrying the red cargo case','deliver newly synthesized cargo')],
 before='The red cargo vesicle is waiting outside the stack with no receiving dock identified.',
 during=['The vesicle docks at the cis face, establishing direction through the stack.','Nia separates one flattened sac visually from the next so “cisternae” means distinct sacs, not one continuous maze.','The red cargo case enters the stack and begins moving toward processing stations.'],
 after='The learner can identify Golgi structure and the cis face by both shape and incoming direction.',
 transition='The cargo advances across the stack toward modification tables and the opposite trans side.',
 must_show=['stack of separate flattened cisternae','incoming ER vesicle','cis face orientation'],
 guards=['Do not imply Golgi cisternae are one continuous internal chamber.','Do not reverse cis and trans faces.'],
 recall=('Which Golgi face receives vesicles from the ER?','The cis face.'),
 carry='Golgi = stacked cisternae with directional traffic from cis receiving face toward trans dispatch face.'),
'U2-L09':dict(
 orientation='On the far side of the Golgi stack, modification tables line the left, tagged cargo waits in the center, and the trans-face dispatch dock opens to multiple destinations on the right.',
 cast=[('Golgi processing stations','sequential worktables across the stack','fold and chemically modify newly synthesized products'),('molecular tags','small destination labels attached to cargo','support sorting'),('trans face','outgoing side of the Golgi','sort and dispatch vesicles to cellular destinations or plasma membrane')],
 before='The red cargo case has arrived but has no final modifications or destination tag.',
 during=['Processing stations modify the cargo as it moves through the Golgi.','A destination tag is attached and the product is packaged into a new vesicle.','At the trans face, the vesicle is dispatched toward its correct cellular destination rather than back toward the ER entry side.'],
 after='Golgi processing, packaging, sorting, and trans-face dispatch form one directional sequence.',
 transition='A second vesicle carries damaged material to the nearby recycling bay, where digestion becomes the next problem.',
 must_show=['modification sequence','tagged cargo','vesicle packaging','trans-face destination branches'],
 guards=['Do not present the Golgi as only a shipping center; modification is also part of its function.'],
 recall=None,
 carry='Golgi modifies products, packages them, and sends them from the trans face.'),
'U2-L10':dict(
 orientation='Beside the Golgi dispatch floor, damaged material enters from the left, an enzyme-filled lysosomal chamber occupies center, and recycled products plus an apoptosis control panel sit on the right.',
 cast=[('lysosome','membrane-enclosed acidic digestive compartment with hydrolytic enzymes','break down macromolecules and cellular material'),('autophagy vesicle','double-membrane packet containing a damaged cell component','deliver damaged material to lysosomes for recycling'),('apoptosis control','regulated cell-death indicator linked to lysosomal function','show lysosomal participation in programmed cell death')],
 before='A damaged organelle is leaking and unusable material is accumulating.',
 during=['The damaged component is enclosed during autophagy and delivered to a lysosome.','Hydrolytic enzymes break the material into smaller reusable products inside the membrane-enclosed compartment.','Nia points to the separate apoptosis panel to show that lysosomes also participate in regulated programmed cell death.'],
 after='The learner connects lysosomes to digestion and recycling while distinguishing autophagy as the delivery/recycling process.',
 transition='Recovered materials are stored or moved onward through a gallery of membrane-bound reservoirs.',
 must_show=['lysosomal membrane','digestive enzymes inside','autophagy cargo delivery','recycled monomers/products'],
 guards=['Do not describe lysosomes as “suicide bags” that simply burst to kill cells.','Do not confuse autophagy with apoptosis.'],
 recall=('What process delivers damaged cellular material to lysosomes for breakdown and recycling?','Autophagy.'),
 carry='Lysosomes digest; autophagy delivers damaged material for lysosomal recycling.'),
'U2-L11':dict(
 orientation='A reservoir gallery opens ahead: smaller food/animal vacuoles are left, a huge plant central vacuole dominates center, and a pulsing contractile vacuole pump is right.',
 cast=[('general vacuoles','membrane-bound storage sacs of varied size','store or manage different materials'),('central vacuole','very large plant-cell reservoir filled with water and solutes','support storage and turgor pressure'),('food vacuole','vesicle containing engulfed food','hold material that can later meet digestive compartments'),('contractile vacuole','repeatedly filling and expelling water','remove excess water in many freshwater protists')],
 before='All reservoirs are mislabeled as if “vacuole” meant one identical structure and function.',
 during=['Nia compares small animal vacuoles with the dominant central vacuole typical of plant cells.','A food vacuole forms around engulfed material and is routed toward digestion.','The contractile vacuole repeatedly fills and contracts, ejecting excess water to maintain osmotic balance.'],
 after='Vacuole becomes a category of membrane-bound sacs with different specialized roles rather than a single plant-only structure.',
 transition='A peroxide hazard alarm sounds from a small oxidation booth beyond the reservoirs.',
 must_show=['size contrast plant vs animal vacuoles','food vacuole formation','contractile vacuole cycle'],
 guards=['Do not imply animal cells never have vacuoles.','Do not equate contractile vacuoles with central vacuoles.'],
 recall=None,
 carry='Vacuoles are diverse membrane-bound sacs; central, food, and contractile vacuoles have different jobs.'),
'U2-L12':dict(
 orientation='The oxidation booth is a small isolated chamber. Oxidation enzymes work on the left, the peroxisome compartment is center, and a catalase safety station handling peroxide is right.',
 cast=[('peroxisome','small membrane-bound oxidative compartment','carry out oxidation reactions distinct from lysosomal digestion'),('oxidation enzymes','enzymes transferring hydrogen to oxygen','produce hydrogen peroxide during certain reactions'),('catalase','enzyme stationed beside the peroxide hazard indicator','break down hydrogen peroxide')],
 before='Hydrogen peroxide begins accumulating in the isolated chamber.',
 during=['Oxidative enzymes transfer hydrogen to oxygen, producing peroxide as part of the chemistry.','Catalase rapidly breaks down hydrogen peroxide before it accumulates dangerously.','Nia physically points back toward the lysosome bay to emphasize that this is oxidative metabolism, not hydrolytic digestion.'],
 after='The peroxisome is remembered by oxidative chemistry and peroxide handling, clearly separated from lysosomal digestion.',
 transition='The booth’s support frame vibrates, revealing the larger cytoskeletal framework that holds the complex together.',
 must_show=['separate peroxisome membrane','oxidation reaction','H2O2 indicator','catalase breakdown'],
 guards=['Do not merge peroxisomes and lysosomes.','Do not imply catalase is the only peroxisomal enzyme.'],
 recall=('Which compartment uses oxidative enzymes and catalase to manage hydrogen peroxide?','Peroxisome.'),
 carry='Peroxisomes perform oxidative metabolism and manage hydrogen peroxide; lysosomes digest with hydrolytic enzymes.'),
'U2-L13':dict(
 orientation='The final hall exposes the cell’s framework: thin actin tension fibers span the left, microtubule rails radiate from an organizing center through the middle, and rope-like intermediate filaments brace the right.',
 cast=[('microtubules','hollow tubulin tubes forming long tracks','maintain shape, carry motor-protein traffic, form spindle and cilia/flagella cores'),('centrosome/MTOC','central nucleation hub for microtubules in many animal cells','organize microtubule growth'),('actin microfilaments','thin flexible tension-bearing filaments','support shape, motility, contraction, and cytokinetic ring formation'),('intermediate filaments','stable rope-like fibers','reinforce shape, anchor organelles, and support structures such as nuclear lamina')],
 before='The complex sags because its rails, tension fibers, and support cables have been treated as one generic scaffold.',
 during=['Microtubules regrow outward from the organizing center and motor cargo begins moving along them.','Actin fibers tighten under tension and a contractile-ring demonstration constricts.','Intermediate filaments remain comparatively stable while bracing organelles and the nuclear envelope.'],
 after='The cytoskeleton is understood as a dynamic network of different filament systems with different structures and functions.',
 transition='The complex stabilizes and Nia follows an energy-demand alarm into the separate Energy Conversion Annex.',
 must_show=['hollow microtubule','actin network','intermediate filament','organizing center','motor cargo track'],
 guards=['Do not portray all cytoskeletal elements as interchangeable.','Do not imply centrosomes are present in all eukaryotic cells.'],
 recall=('Which cytoskeletal element forms hollow tracks for motor proteins and the mitotic spindle?','Microtubules.'),
 carry='Microtubules, actin microfilaments, and intermediate filaments are distinct parts of one cytoskeletal system.'),
'U2-L14':dict(
 orientation='At the mitochondrial airlock, the outer membrane is fixed left, the narrow intermembrane space runs through center, and the inner membrane encloses the matrix on the right.',
 cast=[('outer mitochondrial membrane','smooth outer boundary','form the external membrane of the organelle'),('intermembrane space','narrow region between the two membranes','create a distinct compartment important to respiration'),('inner mitochondrial membrane','second membrane enclosing matrix','separate matrix from intermembrane space and support respiratory processes'),('matrix','innermost fluid compartment','contain enzymes for pyruvate oxidation and citric acid cycle plus mitochondrial DNA and ribosomes')],
 before='The organelle appears as one undifferentiated orange oval.',
 during=['A cutaway separates the outer membrane from the inner membrane, revealing the intermembrane space between them.','The inner membrane closes around the matrix, making two internal compartments visible.','Nia activates labels for matrix enzymes, mitochondrial DNA, and ribosomes so location is tied to function.'],
 after='The mitochondrial double membrane is a compartment-forming architecture, not merely two decorative outlines.',
 transition='The inner membrane folds inward into the next generator deck.',
 must_show=['outer membrane','inner membrane','intermembrane space','matrix'],
 guards=['Do not say cristae themselves create the matrix/intermembrane-space boundary; the inner membrane does.'],
 recall=None,
 carry='Mitochondrial double membrane separates intermembrane space from matrix.'),
'U2-L15':dict(
 orientation='The inner membrane opens into a generator deck. A smooth outer boundary remains left, densely folded inner membrane fills center, and the matrix-facing side is visible right.',
 cast=[('cristae','deep folds of the inner mitochondrial membrane','increase inner-membrane surface area'),('inner-membrane machinery','protein complexes distributed across the folded membrane','support ATP-generating processes of aerobic respiration')],
 before='A flat inner membrane offers relatively little working surface.',
 during=['The inner membrane folds repeatedly into cristae, greatly increasing available membrane area without enlarging the organelle to the same degree.','Respiratory membrane machinery spreads across the expanded surface.','Nia traces one continuous inner membrane through every fold so the learner sees that cristae are folds of the membrane, not separate internal walls.'],
 after='Cristae are remembered as inner-membrane folds whose geometry increases surface supporting ATP synthesis.',
 transition='A demand monitor above the deck compares cells that need very different amounts of sustained energy.',
 must_show=['continuous inner membrane through folds','surface-area increase','matrix/intermembrane sides'],
 guards=['Do not describe cristae as separate membranes or compartments.'],
 recall=('What are cristae?','Folds of the mitochondrial inner membrane that increase membrane surface area.'),
 carry='Cristae increase the working surface of the inner mitochondrial membrane.'),
'U2-L16':dict(
 orientation='At the control bay, a low-demand cell is displayed left, a mitochondrial-count dashboard is center, and a high-demand cell with many mitochondria is displayed right.',
 cast=[('energy-demand meter','dial measuring sustained cellular ATP demand','connect cell activity to mitochondrial abundance'),('mitochondrial population displays','variable numbers and shapes of mitochondria in different cells','show that abundance and morphology vary by cell type and state')],
 before='Both sample cells are shown with the same number of mitochondria, producing a mismatch with their energy demands.',
 during=['The high-demand cell’s meter rises and additional mitochondria appear, while the low-demand display remains lower.','Nia changes physiological state and morphology to show that mitochondrial number and shape are responsive and variable rather than fixed identity markers.'],
 after='The learner links high sustained energy demand with often greater mitochondrial abundance without turning that pattern into an absolute rule.',
 transition='A green light from the neighboring greenhouse signals a second energy-conversion organelle: the chloroplast.',
 must_show=['low versus high demand','different mitochondrial abundance','variation caveat'],
 guards=['Do not claim every high-energy cell always contains a fixed number of mitochondria.'],
 recall=None,
 carry='Mitochondrial abundance often tracks sustained energy demand, but varies with cell type and state.'),
'U2-L17':dict(
 orientation='At the greenhouse entrance, the chloroplast double membrane is left, the transparent organelle interior is center, and a plant/algal cell context display is right.',
 cast=[('chloroplast','green double-membrane organelle','carry out photosynthesis in plants and photosynthetic algae'),('chloroplast envelope','outer and inner membranes around the organelle','separate chloroplast interior from cytosol'),('plant/algal context panel','cells containing chloroplasts','anchor where chloroplasts occur')],
 before='The green organelle floats without context and looks like a generic photosynthesis icon.',
 during=['Nia places the chloroplast inside plant and photosynthetic-algal cells.','A cutaway reveals two envelope membranes and then opens the interior for closer inspection.','The photosynthesis indicator activates inside the chloroplast rather than on the cell surface.'],
 after='Chloroplast identity is tied to organism context, double-membrane structure, and photosynthetic function.',
 transition='The cutaway zooms inward to stacked internal membranes and surrounding fluid.',
 must_show=['double chloroplast envelope','plant/algal context','internal thylakoid system visible but not yet labeled in detail'],
 guards=['Do not imply all eukaryotes or all plant tissues contain chloroplasts.'],
 recall=None,
 carry='Chloroplasts are double-membrane photosynthetic organelles of plants and photosynthetic algae.'),
'U2-L18':dict(
 orientation='Inside the chloroplast, stacked thylakoids form grana on the left, chlorophyll-bearing thylakoid membrane fills center, and the surrounding stroma occupies the right.',
 cast=[('thylakoid','flattened membrane sac','house photosynthetic electron-transfer components in its membrane'),('granum','stack of thylakoids','organize many thylakoid membranes together'),('chlorophyll','green pigment embedded in thylakoid membranes','absorb light used in photosynthesis'),('stroma','fluid outside thylakoids but inside inner chloroplast membrane','host the Calvin cycle')],
 before='The chloroplast interior is a green blur with no distinction between membrane and fluid compartments.',
 during=['Individual thylakoid sacs come into focus and stack into a granum.','Light strikes chlorophyll in the thylakoid membrane and the light-reaction indicator activates on that membrane.','The camera pulls back to the stroma around the stacks, where a separate Calvin-cycle indicator activates.'],
 after='The learner can place light-dependent chemistry on thylakoid membranes and the Calvin cycle in stroma while distinguishing thylakoid from granum.',
 transition='The energy meter closes and Nia leads to a geometric observatory where cell size itself has become the problem.',
 must_show=['individual thylakoid','granum stack','chlorophyll in membrane','stroma around stacks'],
 guards=['Do not place the Calvin cycle inside thylakoids.','Do not use granum and thylakoid as synonyms.'],
 recall=('What is a granum?','A stack of thylakoids.'),
 carry='Thylakoid = membrane sac; granum = stack; chlorophyll is in thylakoid membrane; stroma surrounds thylakoids.'),
'U2-L19':dict(
 orientation='At the observatory table, small cubes and spheres are left, a calculation/display surface is center, and geometrically similar large models are right.',
 cast=[('small cell models','small cube and sphere with brightly lit surface','show high surface-area-to-volume ratio'),('large cell models','scaled-up versions with dim centers','show lower surface-area-to-volume ratio'),('SA:V display','live formulas and exchange meter','connect geometry to exchange capacity')],
 before='The large model is assumed to have proportionally enough membrane simply because it has more total surface area.',
 during=['The cube formula 6s² and volume s³ are calculated for small and large cubes; the sphere formulas 4πr² and 4/3πr³ are shown for comparison.','As linear size increases, volume grows faster than surface area, so the SA:V display falls.','Nutrient/waste exchange lights fail first in the enlarged model’s center, linking membrane area to the volume it must serve.'],
 after='The learner sees why increasing size lowers SA:V and can constrain cell size, shape, nutrient uptake, waste removal, and thermal exchange.',
 transition='Nia unfolds a membrane panel beside the failing giant model to test whether shape can restore exchange surface.',
 must_show=['small and large same-shape models','surface area and volume formulas','ratio falling with size','exchange consequence'],
 guards=['Do not say large cells have less total surface area; they have less surface area relative to volume.'],
 recall=('As a geometrically similar cell gets larger, what happens to its surface-area-to-volume ratio?','It decreases.'),
 carry='Volume outpaces surface area as size increases, lowering SA:V and constraining exchange.'),
'U2-L20':dict(
 orientation='On the fold deck, a flat membrane panel is left, a deeply folded panel is center, and exchange-flow indicators are right.',
 cast=[('flat exchange surface','smooth membrane with limited area','provide baseline exchange area'),('folded exchange surface','same boundary material bent into many folds','increase surface area without proportional volume increase'),('exchange particles','nutrient/waste markers crossing the surface','make exchange capacity visible')],
 before='The flat panel cannot move enough material to serve the model behind it.',
 during=['The membrane folds into ridges and projections while the enclosed volume changes little.','More exchange particles cross simultaneously because more membrane surface is exposed.','Nia connects the geometry to biological structures such as folded membranes and surface projections without turning one specific example into the definition.'],
 after='Complex membrane shape is understood as a way to increase exchange surface area relative to volume.',
 transition='The observatory opens onto a terrace comparing whole organisms of different sizes and heat exchange.',
 must_show=['same approximate volume with flat vs folded surface','increased crossing sites'],
 guards=['Do not imply folding changes the chemical permeability of the membrane by itself.'],
 recall=None,
 carry='Folding increases available exchange surface without needing a proportional increase in volume.'),
'U2-L21':dict(
 orientation='On the terrace, a small organism thermal model is left, a size-comparison scale is center, and a larger organism model is right.',
 cast=[('small organism model','compact body with rapidly flashing heat-loss arrows','show high proportional heat exchange'),('large organism model','larger body with fewer heat arrows per unit mass','show lower proportional heat exchange'),('metabolic-rate gauge','mass-specific energy-use meter','compare general scaling trend')],
 before='Both organisms are assigned the same proportional heat exchange and mass-specific metabolic rate.',
 during=['The small model loses heat across a relatively large surface compared with its volume.','The larger model has lower SA:V and lower proportional heat exchange.','The mass-specific metabolic gauge is generally higher for the smaller multicellular organism, with Nia marking this as a broad biological trend rather than an absolute rule.'],
 after='Surface-area scaling is connected from cells to organismal heat exchange and mass-specific metabolic rate.',
 transition='A flexible molecular border below the terrace begins admitting incorrect particles, drawing Nia toward the Membrane Border Terminal.',
 must_show=['size contrast','relative surface heat arrows','mass-specific rate gauge'],
 guards=['Do not claim body size alone determines metabolic rate in every species or circumstance.'],
 recall=None,
 carry='Larger size generally lowers SA:V and proportional heat exchange; smaller organisms often have higher mass-specific metabolic rates.'),
'U2-L22':dict(
 orientation='At the membrane terminal entrance, water is visible on both sides. Hydrophilic heads face the left aqueous exterior and right aqueous interior, while paired hydrophobic tails meet in the center.',
 cast=[('phospholipid heads','polar phosphate-containing circles','interact with surrounding water'),('fatty-acid tails','nonpolar hydrocarbon chains','avoid water and face one another inside the membrane'),('bilayer','two phospholipid layers arranged tail-to-tail','create the membrane framework')],
 before='Loose phospholipids are scattered randomly in water.',
 during=['The polar heads rotate toward the aqueous environments while nonpolar tails turn away from water.','Two layers self-organize tail-to-tail, creating a hydrophobic interior and hydrophilic surfaces.','Nia names the molecule amphipathic only after both polar and nonpolar regions are visibly contrasted.'],
 after='Bilayer orientation follows directly from phospholipid amphipathic structure.',
 transition='The assembled bilayer begins to ripple sideways, revealing that the membrane is a moving mosaic rather than a rigid wall.',
 must_show=['phosphate heads toward water','fatty-acid tails inward','two aqueous sides'],
 guards=['Do not depict phospholipids as fixed in place or tails facing water in a stable bilayer.'],
 recall=('Which part of a phospholipid faces the membrane interior?','The nonpolar hydrophobic fatty-acid tails.'),
 carry='Amphipathic phospholipids self-organize into a bilayer with hydrophobic interior and hydrophilic surfaces.'),
'U2-L23':dict(
 orientation='The bilayer expands into a broad concourse. Mobile lipids drift on the left, the mixed membrane fabric spans center, and embedded proteins move laterally on the right.',
 cast=[('phospholipids','mobile bilayer molecules','form the fluid framework'),('membrane proteins','embedded or associated proteins of varied shapes','contribute transport, signaling, anchoring, and other functions'),('cholesterol/glycolipids/glycoproteins','additional membrane components distributed through the mosaic','complete the mixed membrane composition')],
 before='The membrane is frozen like a tiled floor with every component locked in one position.',
 during=['Lipids begin drifting laterally within their layer.','Many proteins also shift sideways while maintaining membrane orientation.','Cholesterol, glycoproteins, and glycolipids remain interspersed, so the learner sees a changing mosaic of components rather than a static sandwich.'],
 after='“Fluid mosaic” is grounded in both composition and lateral movement.',
 transition='Temperature controls suddenly swing cold and hot, sending the concourse into the Fluidity Climate Control chamber.',
 must_show=['mixed components','lateral movement','bilayer remains intact'],
 guards=['Do not imply all membrane components move freely without constraints.','Do not depict routine flip-flop of phospholipids between leaflets as the main movement.'],
 recall=None,
 carry='Fluid mosaic = diverse membrane components with substantial lateral mobility.'),
'U2-L24':dict(
 orientation='The climate chamber has a cold membrane demonstration on the left, a temperature-controlled bilayer in center, and a warm cholesterol demonstration on the right.',
 cast=[('unsaturated tails','fatty-acid tails with visible cis-double-bond kinks','reduce tight packing and help preserve fluidity in cold conditions'),('cholesterol','rigid steroid molecules inserted between phospholipids','buffer fluidity across temperature changes'),('temperature control','cold-to-hot slider','reveal different effects on membrane packing')],
 before='Straight lipid tails pack tightly in the cold, while the warm model becomes excessively mobile.',
 during=['Kinked unsaturated tails prevent tight packing as temperature falls.','At low temperature, cholesterol hinders tight phospholipid packing; at higher temperature, it restrains phospholipid movement.','Nia moves the temperature slider back and forth so cholesterol is seen as a buffer, not simply a fluidity increaser or decreaser.'],
 after='Membrane fluidity is linked to tail unsaturation and temperature-dependent cholesterol effects.',
 transition='A membrane-protein placement scanner activates at the next checkpoint.',
 must_show=['cis kink in unsaturated tails','cholesterol between phospholipids','different low/high temperature effects'],
 guards=['Do not say cholesterol always increases fluidity or always decreases fluidity.'],
 recall=('Why do unsaturated phospholipid tails help membranes remain fluid at lower temperatures?','Their cis double-bond kinks reduce tight packing.'),
 carry='Unsaturation reduces packing; cholesterol buffers fluidity differently at low versus high temperature.'),
'U2-L25':dict(
 orientation='At the protein checkpoint, peripheral proteins sit on the left surface, a scanner through center reveals integral and transmembrane placement, and water-exposed protein regions are visible right.',
 cast=[('integral protein','protein penetrating the bilayer hydrophobic interior','embed within membrane; some span the full bilayer'),('transmembrane protein','integral protein crossing from one aqueous side to the other','illustrate the subset that spans the membrane'),('peripheral protein','protein loosely attached to membrane surface or integral protein','associate without entering hydrophobic core'),('hydrophobic/hydrophilic protein regions','differently shaded protein surfaces','match protein chemistry to membrane and aqueous environments')],
 before='Every membrane protein is incorrectly drawn as a full-width channel.',
 during=['The scanner places hydrophobic protein surfaces into the bilayer interior and hydrophilic regions toward aqueous environments.','One integral protein penetrates only partway, another spans fully as a transmembrane protein, while a peripheral protein remains on the surface.','Nia explicitly separates “integral” from “transmembrane” so the terms do not collapse into synonyms.'],
 after='Protein placement is explained by polarity and the integral/peripheral/transmembrane distinctions are spatially clear.',
 transition='Carbohydrate identity tags appear on selected lipids and proteins at the recognition counter.',
 must_show=['partial integral protein','full transmembrane protein','surface peripheral protein','hydrophobic/hydrophilic regions'],
 guards=['Do not state that all integral proteins are transmembrane.','Do not place peripheral proteins inside the hydrophobic core.'],
 recall=('Are all integral membrane proteins transmembrane proteins?','No. Transmembrane proteins are integral proteins that span the entire membrane; other integral proteins penetrate the bilayer without spanning it.'),
 carry='Integral proteins penetrate the hydrophobic core; peripheral proteins do not; only some integral proteins are transmembrane.'),
'U2-L26':dict(
 orientation='At the recognition counter, carbohydrate-tagged lipids are displayed left, the identity-scanning desk is center, and carbohydrate-tagged proteins are displayed right.',
 cast=[('glycolipid','membrane lipid with covalently attached carbohydrate','participate in recognition and interactions'),('glycoprotein','membrane protein with covalently attached carbohydrate','participate prominently in cell-cell recognition'),('carbohydrate tags','branched chains projecting from the membrane exterior','provide recognizable external molecular patterns')],
 before='Identity tags are present but the learner cannot tell whether each is attached to a lipid or protein.',
 during=['Nia traces one carbohydrate chain down to a lipid anchor and names it a glycolipid.','A second chain is traced to a protein anchor and named a glycoprotein.','The recognition scanner responds to the outward-projecting carbohydrate patterns, tying structure to cell-cell recognition.'],
 after='Glycolipid and glycoprotein are distinguished by what the carbohydrate is covalently attached to.',
 transition='The test-traveler tray arrives at the membrane’s hydrophobic security lane.',
 must_show=['carbohydrate attached to lipid','carbohydrate attached to protein','external projection'],
 guards=['Do not define glycolipid/glycoprotein only as “sugar on membrane” without identifying the anchor molecule.'],
 recall=None,
 carry='Glycolipid = carbohydrate on lipid; glycoprotein = carbohydrate on protein; both can support recognition.'),
'U2-L27':dict(
 orientation='The selective barrier lane has an aqueous approach left, the nonpolar membrane interior center, and the aqueous cell side right.',
 cast=[('hydrophobic core','dense field of nonpolar fatty-acid tails','impede direct passage of ions and many polar molecules'),('test travelers','molecules with different polarity/charge','reveal which substances can cross directly')],
 before='The border is assumed to be selective because an invisible guard chooses molecules.',
 during=['An ion enters the hydrophobic core and is energetically excluded, while a nonpolar molecule slips through.','A polar molecule hesitates, making the physical basis of selective permeability visible.','Nia removes the imaginary “guard” and points to the hydrophobic interior as the main barrier responsible for these differences.'],
 after='Selective permeability is grounded in molecular interactions with the membrane interior.',
 transition='The travelers are sorted into three passport lanes for a more precise permeability comparison.',
 must_show=['aqueous sides','hydrophobic core','contrasting traveler behavior'],
 guards=['Do not anthropomorphize selective permeability as intentional choice.'],
 recall=('What membrane feature creates the main barrier to ions and many polar molecules?','The hydrophobic interior formed by nonpolar phospholipid tails.'),
 carry='Membrane selectivity largely emerges from the hydrophobic bilayer interior.'),
'U2-L28':dict(
 orientation='Three neighboring passport lanes are fixed left-to-right: direct passage for small nonpolar molecules, limited passage for small uncharged polar molecules, and protein-required passage for ions and large polar molecules.',
 cast=[('O2/CO2/N2','small nonpolar travelers','cross the lipid bilayer readily'),('H2O/NH3','small uncharged polar travelers','cross directly in small amounts, with water often using aquaporins for high flux'),('ions/large polar molecules','charged or bulky hydrophilic travelers','generally require membrane transport proteins')],
 before='Every molecule is placed in one universal membrane crossing lane.',
 during=['Small nonpolar gases pass directly through the bilayer.','Small uncharged polar molecules cross more slowly/limitedly.','Ions and large polar molecules are redirected to protein-assisted routes, setting up the later transport hub.'],
 after='Permeability categories are tied to size, polarity, and charge rather than memorized as isolated examples.',
 transition='The terminal exterior opens onto a rigid plant-cell wall with a channel piercing through to the next cell.',
 must_show=['three molecule classes','relative passage differences','protein-required redirect'],
 guards=['Do not say water cannot cross the bilayer at all.','Do not say every polar molecule behaves identically.'],
 recall=None,
 carry='Small nonpolar molecules cross readily; small uncharged polar molecules cross to a limited extent; ions and large polar molecules generally need proteins.'),
'U2-L29':dict(
 orientation='Outside a plant cell, the cellulose-rich wall matrix fills the left, the plasma membrane lies directly beneath it in center, and a membrane-lined plasmodesma passes through the wall to an adjacent cell on the right.',
 cast=[('plant cell wall','cellulose microfibrils in a polysaccharide/protein matrix','support shape, resist excessive expansion, and protect'),('plasma membrane','flexible membrane beneath the wall','provide the primary selective transport boundary into cytoplasm'),('plasmodesma','membrane-lined channel crossing the wall','connect cytoplasm of neighboring plant cells for transport and communication')],
 before='The wall is incorrectly treated as the cell’s main selective gate and as a solid barrier between neighboring cells.',
 during=['Water presses the plant contents outward; the rigid wall resists excessive expansion without replacing the membrane’s selective role.','Nia separates wall composition from plasma-membrane selectivity.','A plasmodesma opens through the wall, revealing continuous communication between adjacent cells.'],
 after='Plant wall support, membrane selectivity, and plasmodesmatal communication are distinct but spatially related.',
 transition='A concentration alarm from the neighboring transit hub shows particles piling up on one side of a membrane.',
 must_show=['cellulose microfibrils','plasma membrane beneath wall','plasmodesma connecting adjacent cytoplasm'],
 guards=['Do not say the plant cell wall regulates selective water entry into cytoplasm.','Do not imply only plants have cell walls; bacteria, archaea, and fungi also have cell walls with different compositions.'],
 recall=('Which structure is the primary selective barrier controlling entry into a plant cell’s cytoplasm?','The plasma membrane.'),
 carry='Plant cell wall supports and protects; plasma membrane controls selective entry; plasmodesmata connect neighboring cells.'),
'U2-L30':dict(
 orientation='At the transit hub, a crowded high-concentration platform is left, a sloped region of random molecular motion is center, and a sparse low-concentration platform is right.',
 cast=[('solute particles','many identical moving particles','demonstrate random molecular motion and net diffusion'),('concentration gradient','visible difference in particle concentration across space','provide direction for net movement'),('passive route indicator','unpowered downhill arrow','show transport without direct metabolic-energy input')],
 before='Particles are frozen in place, so a concentration difference exists but no diffusion occurs.',
 during=['Random motion begins in every direction, but because more particles start on the crowded side, more cross toward the sparse side than return.','Net movement continues down the concentration gradient until the distribution approaches dynamic equilibrium.','The route remains unpowered, establishing passive transport as downhill net movement without direct metabolic energy.'],
 after='Diffusion is understood as net movement emerging from random motion, not particles intentionally moving “where there is room.”',
 transition='A cargo token must now travel uphill against the gradient, forcing the learner to activate a powered lift.',
 must_show=['random motion both directions','net downhill movement','dynamic equilibrium with continued motion'],
 guards=['Do not say molecules stop moving at equilibrium.','Do not describe diffusion as purposeful movement.'],
 recall=('At dynamic equilibrium, do molecules stop moving?','No. Molecular motion continues, but there is no net movement in one direction.'),
 carry='Diffusion is net downhill movement produced by random molecular motion; passive transport requires no direct metabolic energy.'),
'U2-L31':dict(
 orientation='The active-transport lift loads cargo at low concentration on the left, an ATP-powered membrane transporter occupies center, and the high-concentration unloading bay is right.',
 cast=[('ATP','glowing energy token','provide direct metabolic energy'),('active transport protein','membrane protein changing conformation as ATP is used','move cargo across the membrane against a gradient in appropriate cases'),('cargo','solute token moving from low to high concentration','make uphill transport visible')],
 before='The cargo rolls back downhill whenever it is placed on the high-concentration side.',
 during=['ATP is consumed at the transporter and the protein changes state.','The cargo is moved from the lower-concentration side to the higher-concentration side, building/maintaining a gradient.','Nia contrasts this powered route with the passive concentration ramp.'],
 after='Active transport is anchored to energy input and membrane proteins, with uphill movement as a key example.',
 transition='A different traveler needs protein assistance but is already moving downhill, leading to the facilitated diffusion corridor.',
 must_show=['ATP use','transport protein','low-to-high example','gradient maintenance'],
 guards=['Do not define all active transport solely as low-to-high concentration; electrochemical gradients can matter.'],
 recall=('What distinguishes this route from passive transport?','It requires direct energy input, such as ATP, and uses membrane transport proteins.'),
 carry='Active transport uses energy and membrane proteins to establish or maintain gradients.'),
'U2-L32':dict(
 orientation='The facilitated-diffusion corridor starts with high-concentration cargo left, a membrane transport-protein corridor center, and a low-concentration destination right.',
 cast=[('large polar cargo','solute that cannot readily cross the hydrophobic bilayer','require a protein route'),('channel/carrier route','protein-assisted passage through membrane','enable downhill movement without direct energy input')],
 before='The large polar traveler has a downhill gradient but still cannot enter the hydrophobic core.',
 during=['The traveler enters a specific membrane protein instead of crossing the lipid interior.','It emerges on the lower-concentration side without ATP being consumed.','Nia labels the process facilitated diffusion and points forward to the two major protein strategies: channels and carriers.'],
 after='The learner separates “needs a protein” from “needs energy.”',
 transition='The corridor splits into channel turnstiles and a carrier shuttle.',
 must_show=['downhill gradient','protein route','no ATP'],
 guards=['Do not classify facilitated diffusion as active transport simply because a protein is used.'],
 recall=None,
 carry='Facilitated diffusion is protein-assisted but still passive when movement is downhill.'),
'U2-L33':dict(
 orientation='At the channel turnstiles, ions wait on the left, a gated hydrophilic pore spans center, and a voltage/charge-separation indicator is right.',
 cast=[('channel protein','hydrophilic pore through the membrane','provide selective passage for specific ions or molecules'),('gate','movable part of the channel','open or close in response to chemical or physical stimuli'),('Na+ and K+ ions','charged travelers','demonstrate why ions need hydrophilic routes through the membrane')],
 before='Charged ions collide with the hydrophobic membrane and cannot cross directly.',
 during=['A gate opens and selected ions move through the hydrophilic channel down their electrochemical/concentration driving force.','The gate closes in response to a stimulus change.','As unequal charges redistribute, the membrane-polarization indicator changes.'],
 after='Channel proteins are remembered as selective hydrophilic passageways, many of which are gated, and ion movement is linked to polarization.',
 transition='A solute that cannot use an open pore arrives at a neighboring binding shuttle.',
 must_show=['hydrophilic pore','specific ion passage','gating','charge separation'],
 guards=['Do not depict ion channels as ATP-driven pumps.'],
 recall=('What is the key structural difference between a channel and the lipid bilayer for an ion?','The channel provides a hydrophilic passageway through the membrane.'),
 carry='Channels provide selective hydrophilic pores; ion movement can alter membrane polarization.'),
'U2-L34':dict(
 orientation='At the carrier shuttle, a solute binding site is left, the carrier’s conformational-change chamber is center, and the release side is right.',
 cast=[('carrier protein','membrane protein with a specific binding site','bind a solute and change conformation to move it across'),('solute','shape-matched cargo','demonstrate specificity and one-at-a-time binding/change/release logic')],
 before='The carrier faces left with an empty binding site.',
 during=['The solute binds specifically to the exposed site.','Binding triggers a conformational change that closes one side and opens the other.','The solute is released on the opposite side and the carrier resets.'],
 after='A carrier is distinguished from a continuously open channel by binding and conformational change.',
 transition='A flood of water overwhelms ordinary crossing routes, activating a bank of water channels.',
 must_show=['specific binding','alternating exposure/conformational change','release'],
 guards=['Do not draw a carrier as an open tunnel.'],
 recall=('How does a carrier protein move its solute?','It binds the solute and changes conformation to expose it to the other side of the membrane.'),
 carry='Carriers bind specific solutes and change conformation; channels provide pores.'),
'U2-L35':dict(
 orientation='At the aquaporin floodgate, a water reservoir is left, a bank of narrow aquaporin channels spans center, and a receiving reservoir is right.',
 cast=[('aquaporin','water-selective membrane channel','permit rapid movement of large quantities of water'),('water molecules','small polar molecules moving through the channel','make high water flux visible')],
 before='Water crosses the bare bilayer too slowly to meet the sudden demand.',
 during=['Aquaporin channels open a high-throughput route for water across the membrane.','Large numbers of water molecules move rapidly through the channels while ions remain excluded from this demonstration.'],
 after='Aquaporins are anchored as channels specialized for high water permeability.',
 transition='A cargo too large for any channel arrives at the bulk-vesicle dock.',
 must_show=['many water molecules','narrow water-selective channel','high throughput'],
 guards=['Do not imply water can cross membranes only through aquaporins.'],
 recall=None,
 carry='Aquaporins greatly increase membrane water permeability.'),
'U2-L36':dict(
 orientation='At the bulk cargo dock, membrane invagination occurs on the left, vesicle handling occupies center, and vesicle fusion/release occurs on the right.',
 cast=[('plasma membrane','flexible boundary that bends and fuses','form and merge with vesicles'),('endocytic vesicle','membrane packet formed inward from the surface','bring external material into the cell'),('exocytic vesicle','internal membrane packet approaching the surface','fuse and release cargo outside')],
 before='Oversized cargo cannot pass through channels or carriers.',
 during=['The plasma membrane bends inward around external material and pinches off a vesicle: endocytosis.','A separate internal vesicle moves to the plasma membrane, fuses with it, and releases cargo: exocytosis.','An energy indicator remains active for both bulk-transport processes.'],
 after='Endocytosis and exocytosis are mirror-like membrane-remodeling processes that require energy and move large cargo/quantities.',
 transition='The intake side divides into three specialized forms of endocytosis.',
 must_show=['invagination and pinch-off','vesicle fusion','cargo direction','energy use'],
 guards=['Do not depict endocytosis/exocytosis as transport through protein channels.'],
 recall=('Which process releases internal vesicle contents outside the cell?','Exocytosis.'),
 carry='Endocytosis brings material in by vesicle formation; exocytosis releases it by vesicle fusion.'),
'U2-L37':dict(
 orientation='Three intake bays sit side-by-side: phagocytosis left, pinocytosis center, and receptor-mediated endocytosis right.',
 cast=[('phagocytosis bay','cell membrane wrapping around a large particle','engulf large particles into vesicles'),('pinocytosis bay','small vesicles sampling extracellular fluid','take up fluid and dissolved solutes nonspecifically'),('receptor-mediated bay','specific ligands binding clustered membrane receptors','concentrate selected cargo before invagination')],
 before='All endocytosis is represented by one generic inward bubble.',
 during=['A large particle is engulfed in the phagocytosis bay and the resulting vesicle is routed toward lysosomal digestion.','Small fluid droplets are internalized nonspecifically by pinocytosis.','Specific ligands bind receptors, cluster, and enter together during receptor-mediated endocytosis.'],
 after='The three forms are distinguished by cargo size/selectivity and mechanism rather than by three arbitrary names.',
 transition='The hub lights dim as a voltage-control alarm signals failure of an electrogenic pump.',
 must_show=['large particle engulfment','fluid uptake','specific receptor-ligand binding'],
 guards=['Do not define pinocytosis by one mandatory coat protein.','Do not equate all endocytosis with phagocytosis.'],
 recall=('Which form of endocytosis selectively concentrates ligands after they bind membrane receptors?','Receptor-mediated endocytosis.'),
 carry='Phagocytosis = large particles; pinocytosis = nonspecific fluid; receptor-mediated endocytosis = selected ligands.'),
'U2-L38':dict(
 orientation='At electrical pump control, Na+ export is left, the Na+/K+ ATPase and voltage meter occupy center, and K+ import is right.',
 cast=[('Na+/K+ ATPase','ATP-powered membrane pump','export 3 Na+ and import 2 K+ per ATP in animal cells'),('membrane potential meter','voltage display across the membrane','show charge separation from unequal ion distributions'),('electrogenic-pump indicator','net-charge counter','show that net charge movement can generate voltage')],
 before='Na+ and K+ gradients decay and the voltage meter drifts toward zero.',
 during=['One ATP powers the pump cycle: 3 Na+ move out and 2 K+ move in.','The net outward movement of one positive charge registers on the electrogenic indicator.','The restored unequal ion distributions contribute to membrane potential and provide stored electrochemical energy.'],
 after='The pump’s stoichiometry, electrogenic effect, and connection to membrane potential are one visible cycle.',
 transition='A separate proton gradient is being built on the next platform to power coupled sucrose uptake.',
 must_show=['3 Na+ out','2 K+ in','1 ATP','voltage meter','net +1 outward'],
 guards=['Do not reverse Na+/K+ directions.','Do not imply the Na+/K+ pump alone creates the entire resting membrane potential.'],
 recall=('For each ATP, how many Na+ move out and K+ move in through the Na+/K+ ATPase?','3 Na+ out and 2 K+ in.'),
 carry='Electrogenic pumps move net charge; Na+/K+ ATPase uses ATP to maintain ion gradients and contributes to membrane potential.'),
'U2-L39':dict(
 orientation='At the proton platform, an ATP-powered proton pump is left, a high-H+ electrochemical reservoir is center, and an H+/sucrose cotransporter is right.',
 cast=[('proton pump','ATP-driven H+ transporter','build an H+ electrochemical gradient'),('H+ gradient','stored difference in proton concentration and charge','hold potential energy for secondary transport'),('H+/sucrose symporter','coupled transporter carrying H+ and sucrose together','use downhill H+ movement to drive uphill sucrose uptake')],
 before='Sucrose needs to enter against its concentration gradient but has no direct ATP-powered sucrose pump in this demonstration.',
 during=['ATP powers the proton pump to move H+ and build a gradient.','H+ then flows downhill through the cotransporter.','The transporter couples that favorable H+ movement to sucrose moving uphill into the plant cell.'],
 after='Cotransport is understood as using energy already stored in an electrochemical gradient rather than hydrolyzing ATP at the cotransporter itself.',
 transition='The transport hub stabilizes, but the next greenhouse contains cells with water-balance problems caused by different external solutions.',
 must_show=['ATP at proton pump','H+ gradient','same-direction H+ and sucrose symport','sucrose uphill'],
 guards=['Do not show ATP being hydrolyzed directly by the sucrose symporter in this example.'],
 recall=('What provides the immediate energy for sucrose uptake through the H+/sucrose symporter?','H+ moving down its electrochemical gradient.'),
 carry='A proton pump builds the gradient; cotransport spends gradient energy to move another solute uphill.'),
'U2-L40':dict(
 orientation='At the conservatory entrance, a hypotonic solution door is left, a reference cell tank is center, and isotonic/hypertonic comparison doors are right.',
 cast=[('reference cell','transparent cell with marked internal nonpenetrating solute concentration','provide the comparison point'),('external solution controls','three doors with different nonpenetrating solute concentrations','define hypotonic, isotonic, or hypertonic relative to the cell'),('tonicity gauge','water-gain/loss prediction meter','connect relative solute concentration to cell water response')],
 before='The three terms are displayed as absolute properties of solutions with no reference cell.',
 during=['Nia locks the reference cell’s internal composition and changes only the outside solution.','The external solution is labeled hypotonic, isotonic, or hypertonic relative to that cell based on nonpenetrating solutes.','The tonicity gauge predicts whether the cell will gain, lose, or show no net water movement.'],
 after='Tonicity becomes a relationship between a solution and a cell, not a permanent label attached to a beaker.',
 transition='The isotonic door opens first into a chamber where water movement is visible in both directions.',
 must_show=['reference cell interior','three relative solution states','water-response gauge'],
 guards=['Do not label a solution hypotonic/hypertonic without a comparison context.'],
 recall=('Tonicity predicts what aspect of a cell’s behavior?','Whether a solution containing nonpenetrating solutes causes the cell to gain or lose water.'),
 carry='Hypotonic, isotonic, and hypertonic are relative to the cell and predict water gain/loss.'),
'U2-L41':dict(
 orientation='In the isotonic pool, water arrows enter from the left, the cell floats in center, and equal water arrows leave to the right.',
 cast=[('isotonic solution','external solution producing no net water movement','maintain cell volume on average'),('water molecules','moving continuously in both directions','show dynamic exchange despite zero net flow')],
 before='The word “isotonic” is mistakenly represented by water molecules frozen in place.',
 during=['Water molecules cross inward and outward continuously.','The inward and outward rates balance, so the cell’s average volume remains stable and the net water movement is zero.'],
 after='No net movement is distinguished from no molecular movement.',
 transition='The next door contains a higher effective external solute concentration and the cell begins losing water.',
 must_show=['bidirectional arrows','equal net balance','stable cell size'],
 guards=['Do not say osmosis stops in isotonic conditions.'],
 recall=None,
 carry='Isotonic = water still moves both ways, but there is no net water movement.'),
'U2-L42':dict(
 orientation='In the hypertonic chamber, concentrated external solution is left, a shrinking animal cell is center, and water-flow arrows point outward to the right.',
 cast=[('hypertonic external solution','solution with greater effective nonpenetrating solute concentration than the cell','draw net water out of the cell'),('animal-cell model','flexible cell with no cell wall','shrink as water is lost')],
 before='The animal cell begins at normal volume.',
 during=['Net water movement leaves the cell toward the hypertonic environment.','The flexible animal cell shrinks as volume falls.','Nia flags that water loss does not automatically mean instant cell death and previews that a plant cell can plasmolyze under similar conditions.'],
 after='Hypertonic conditions are tied to net water loss and cell shrinkage rather than to the vague idea of “more water outside.”',
 transition='The route turns to a low-solute chamber containing both animal and plant cells so their different boundaries can be compared.',
 must_show=['higher external effective solute','outward net water movement','animal cell shrinking'],
 guards=['Do not claim every hypertonic exposure immediately kills the cell.'],
 recall=('What is the net water response of a cell in a hypertonic environment?','The cell loses water.'),
 carry='Hypertonic outside → net water loss from the cell.'),
'U2-L43':dict(
 orientation='In the hypotonic greenhouse, a swelling animal cell is left, a turgid plant cell pressing against its wall is center, and a comparison panel showing plasmolyzed versus turgid plant states is right.',
 cast=[('hypotonic solution','external solution with lower effective nonpenetrating solute concentration','drive net water into cells'),('animal cell','membrane-only boundary in this comparison','swell and potentially lyse as water enters'),('plant cell wall','rigid external boundary around the plant plasma membrane','resist expansion and create turgor pressure'),('plasmolysis comparison','plant cell with membrane pulled away from wall after water loss','contrast the hypertonic plant-cell state')],
 before='Both animal and plant cells are shown responding identically to incoming water.',
 during=['Net water enters both cells in the hypotonic solution.','The animal cell swells because it lacks a cell wall; the plant cell becomes turgid as its contents press against the wall, generating turgor pressure.','The comparison panel reverses the water direction to show plasmolysis when a plant cell loses water and its membrane pulls away from the wall.'],
 after='The same osmotic input produces different outcomes because plant cells have walls that resist expansion.',
 transition='Nia opens a channel connecting two water-potential compartments to explain the general rule behind all three tonicity chambers.',
 must_show=['animal swelling','plant turgidity','wall resistance','plasmolyzed comparison'],
 guards=['Do not say healthy plant cells burst in ordinary hypotonic conditions.','Do not define plasmolysis as a hypotonic response.'],
 recall=('What creates turgor pressure in a plant cell?','Water entry causes cell contents to press against the cell wall, which resists expansion.'),
 carry='Hypotonic water entry swells animal cells but makes healthy plant cells turgid because the wall resists expansion.'),
'U2-L44':dict(
 orientation='A transparent river connects two compartments. Higher water potential is left, a selectively permeable divider is center, and lower water potential is right.',
 cast=[('free water','water molecules able to cross the divider','move net from higher to lower water potential'),('selectively permeable membrane','divider allowing water movement while restricting selected solutes','create conditions for osmosis'),('water-potential markers','Ψ labels on each side','provide the general directional rule')],
 before='The learner has only “water moves toward more solute” as a memorized slogan.',
 during=['Nia labels the two sides by water potential and water moves net from higher Ψ to lower Ψ across the selective divider.','When pressure conditions are held equal, the lower-solute side generally has higher water potential and water moves toward the higher-solute/osmolarity side.','The same continual membrane movement is linked to growth and homeostasis, while Nia warns that water potential is the governing rule when pressure also differs.'],
 after='Osmosis is defined by free-water diffusion down a water-potential gradient, with osmolarity as a useful special-case cue.',
 transition='The river flows beneath a control room where pressure and solute contributions to Ψ can be adjusted separately.',
 must_show=['higher and lower Ψ labels','selectively permeable divider','net water direction','osmolarity special-case comparison'],
 guards=['Do not use “water always moves to higher solute concentration” when pressure potential differs.','Do not describe osmosis as solute movement.'],
 recall=('What is the most general direction rule for osmosis?','Water moves net from higher water potential to lower water potential.'),
 carry='Osmosis follows water potential; higher solute concentration predicts direction only when other components are equal.'),
'U2-L45':dict(
 orientation='Above the river, pressure controls are left, a central console displays Ψ = Ψp + Ψs and Ψs = −iCRT, and solute/osmoregulation controls are right.',
 cast=[('pressure potential control','piston/pressure gauge labeled Ψp','change the physical pressure component of water potential'),('solute potential control','solute injector and Ψs display','show that dissolved solute lowers solute potential'),('water-potential console','equation display combining Ψp and Ψs','calculate total water potential'),('osmoregulation controller','feedback system adjusting water/solute balance','maintain internal water balance and solute composition')],
 before='The river direction is predicted from solute concentration alone even when pressure changes.',
 during=['Nia sets an open beaker at relative pressure potential zero, then changes pressure to show Ψp can shift total Ψ.','Solute is added and Ψs becomes more negative; the console shows Ψs = −iCRT with i, C, R, and T labeled.','Total Ψ is recomputed as Ψp + Ψs, and the osmoregulation controller adjusts water/solute conditions to stabilize the internal environment.'],
 after='Pressure potential and solute potential are separate contributors to total water potential, and osmoregulation manages the resulting water balance.',
 transition='With transport and water balance restored, the final route asks why internal membranes and compartments are useful in the first place.',
 must_show=['Ψ equation','solute-potential equation','pressure gauge','solute changes making Ψs more negative','osmoregulation feedback'],
 guards=['Do not omit the negative sign in Ψs = −iCRT.','Do not treat pressure potential as always zero; that convention applies to open systems at atmospheric pressure.'],
 recall=('What two components are added to calculate total water potential?','Pressure potential (Ψp) and solute potential (Ψs).'),
 carry='Ψ = Ψp + Ψs; adding solute lowers Ψs; pressure can also change total water potential.'),
'U2-L46':dict(
 orientation='The compartmentalization lab contains reaction chamber A on the left, an internal membrane divider with expanded surface in center, and reaction chamber B on the right.',
 cast=[('internal membrane divider','membrane separating two enzyme environments','keep different reactions physically separated'),('enzyme set A/B','different reaction systems on opposite sides','demonstrate minimized competing interactions'),('folded membrane surface','expanded internal membrane area','provide more surface on which membrane-associated reactions can occur')],
 before='Two incompatible reaction systems are mixed in one open chamber and interfere with one another.',
 during=['An internal membrane partitions the reactions into separate spaces and interference falls.','The membrane folds, adding reaction surface without requiring a proportional increase in cell volume.','Nia connects the physical arrangement to membrane-bound organelles as specialized metabolic compartments.'],
 after='Compartmentalization is understood as both separation of reactions and expansion of useful internal reaction surface.',
 transition='A comparison room next door asks how prokaryotic and eukaryotic cells achieve internal organization differently.',
 must_show=['separated reaction environments','reduced interference','folded internal membrane surface'],
 guards=['Do not imply prokaryotes have no spatial organization at all.'],
 recall=('What are two major advantages of internal membrane compartmentalization?','It separates potentially competing reactions and increases membrane surface area for cellular processes.'),
 carry='Internal membranes organize chemistry by separating reactions and increasing usable reaction surface.'),
'U2-L47':dict(
 orientation='The comparison room places a prokaryotic model left, a side-by-side organization table center, and a eukaryotic model with membrane-bound compartments right.',
 cast=[('prokaryotic model','cell without membrane-bound organelles but with localized structures/regions','show specialized internal organization without eukaryotic-style organelles'),('eukaryotic model','cell partitioned by internal membranes into organelles','show membrane-bound specialized regions')],
 before='The prokaryotic model is incorrectly shown as an empty bag with no organization.',
 during=['Localized prokaryotic structures and regions light up despite the absence of typical membrane-bound organelles.','The eukaryotic model partitions many functions into membrane-bound compartments.','Nia compares organization strategies without treating one as simply organized and the other as unorganized.'],
 after='Both cell types have internal organization, while eukaryotes extensively use membrane-bound compartments.',
 transition='The comparison table shifts into a historical theater showing how two eukaryotic organelles may have originated.',
 must_show=['organized prokaryotic regions','membrane-bound eukaryotic organelles','side-by-side comparison'],
 guards=['Do not say prokaryotes lack compartmentalization or specialized internal regions entirely.'],
 recall=None,
 carry='Prokaryotes can have specialized internal organization; eukaryotes extensively partition functions with internal membranes.'),
'U2-L48':dict(
 orientation='In the origin theater, an ancestral host cell is left, an engulfment-and-retention stage is center, and an integrated descendant organelle appears right.',
 cast=[('ancestral host cell','larger ancestral cell membrane surrounding the stage','represent the host lineage'),('free-living prokaryote','smaller bacterium-like cell with its own DNA and ribosomes','represent the ancestral endosymbiont'),('retained endosymbiont','engulfed cell that persists rather than being digested','show the key endosymbiotic transition')],
 before='The smaller prokaryote is outside the host and independently living.',
 during=['The host membrane surrounds the prokaryote, but instead of digestion the engulfed cell persists.','Across generations, the retained partner becomes increasingly integrated with host-cell function.','Nia identifies endosymbiosis as the evolutionary explanation for mitochondrial and chloroplast origins, while keeping the event a historical model rather than a literal one-time cartoon.'],
 after='Endosymbiosis is a host–symbiont evolutionary process leading to organelle origins.',
 transition='The theater doors open into an evidence vault that tests the hypothesis using multiple independent observations.',
 must_show=['host','free-living prokaryote','engulfment/retention','integrated descendant organelle'],
 guards=['Do not imply modern mitochondria/chloroplasts are still free-living cells.','Do not present the cartoon as direct observation of the ancient event.'],
 recall=('What evolutionary process explains the origins of mitochondria and chloroplasts from once free-living prokaryotes?','Endosymbiosis.'),
 carry='Endosymbiosis proposes that ancestral free-living prokaryotes were retained and became integrated organelles.'),
'U2-L49':dict(
 orientation='The evidence vault has genome/division evidence on the left, ribosome/membrane evidence in center, and a modern host-dependence panel on the right.',
 cast=[('circular organelle DNA','small circular genomes inside mitochondria/chloroplasts','support bacterial ancestry'),('division sequence','organelle constricting and dividing','show division similarities to bacterial binary fission'),('organelle ribosomes','ribosomes with bacterial-like features','provide molecular evidence of ancestry'),('double membranes','outer and inner organelle membranes plus bacterial similarities','support an engulfment/integration history'),('host-dependence panel','genes/functions split between organelle and nucleus','show modern organelles are integrated and generally not independently free-living')],
 before='Endosymbiosis is represented as a single story with no evidence cards.',
 during=['The learner adds a circular-DNA card and a bacterial-like division card to the evidence case.','Bacterial-like ribosome features and double-membrane/inner-membrane similarities add independent support.','The final panel shows extensive gene/function integration with the host, preventing the false conclusion that modern mitochondria or chloroplasts can simply live independently.'],
 after='The endosymbiotic explanation is supported by converging genomic, reproductive, ribosomal, and membrane evidence while acknowledging modern organelle dependence.',
 transition='Nia seals the evidence case, completing the Unit 2 conceptual journeys and unlocking later application challenges only after narrative QA.',
 must_show=['circular DNA','division','ribosome comparison','double membrane','host dependence'],
 guards=['Do not claim any one evidence line alone proves endosymbiosis.','Do not imply modern organelles are autonomous free-living organisms.'],
 recall=('Name two independent lines of evidence supporting endosymbiotic origins.','Examples include circular organelle DNA, bacterial-like division, bacterial-like ribosome features, and double-membrane/inner-membrane similarities.'),
 carry='Endosymbiosis is supported by multiple converging evidence lines, and modern organelles are deeply integrated with their host cells.'),
}

assert set(S)==set(loci), (set(loci)-set(S), set(S)-set(loci))

# Rich journey briefs preserve F2 order and add story continuity without student prose.
journey_briefs=[]
for j in f2['journeys']:
    spec=journey_specs[j['journey_id']]
    route=[lid for b in j['bundles'] for lid in b['loci']]
    journey_briefs.append({
      'journey_id':j['journey_id'],
      'working_title':spec['final_working_title'],
      'content_focus':j['content_focus'],
      'setting_logic':j['setting_logic'],
      'unit_guide':unit_guide,
      'premise':spec['premise'],
      'mission':spec['mission'],
      'stakes':spec['stakes'],
      'continuity_object':spec['continuity_object'],
      'opening_image':spec['opening_image'],
      'route':route,
      'ending_payoff':spec['ending_payoff'],
      'tone':spec['tone'],
      'narrative_constraints':[
        'The learner always knows where they are relative to the previous locus.',
        'Scientific parts keep stable visual identities within a journey.',
        'A scientific term is named only after its defining action or structure is visible.',
        'No source-management language appears in future student prose.',
        'No arbitrary character, joke, or spectacle may compete with the science-bearing action.',
        'Transitions must be caused by the preceding scene problem or continuity object, not by generic movement narration.'
      ],
      'status':'JOURNEY_BRIEF_LOCKED_F3_NO_POLISHED_STORY_PROSE'
    })

briefs=[]
for idx,l in enumerate(f2['loci']):
    sp=S[l['locus_id']]
    kids=l['knowledge_ids']
    # Each term appears after a visible science action; primary comes first, embedded follow as relevant.
    term_intros=[]
    for n,kid in enumerate(kids):
        r=records[kid]
        term_intros.append({
          'knowledge_id':kid,
          'canonical_term':r['canonical_label'],
          'exact_name_recall':bool(r['exact_name_recall']),
          'canonical_science':r['canonical_verified_statement'],
          'insertion_rule':f"Name the term after action step {min(n+1,len(sp['during']))} has made its defining structure/function visible; then state the canonical science without source-facing meta language.",
        })
    next_locus=f2['loci'][idx+1]['locus_id'] if idx+1<len(f2['loci']) and f2['loci'][idx+1]['journey_id']==l['journey_id'] else None
    cast=[{'name':name,'visual_identity':visual,'job_in_scene':job,'type':'SCIENTIFIC_PART'} for name,visual,job in sp['cast']]
    first_exposure_recall_loci={
      'U2-L01','U2-L04','U2-L08','U2-L13',
      'U2-L15','U2-L18',
      'U2-L19',
      'U2-L22','U2-L25','U2-L29',
      'U2-L30','U2-L38','U2-L39',
      'U2-L40','U2-L44',
      'U2-L48','U2-L49'
    }
    qr=None
    if sp['recall']:
        qr={'enabled':l['locus_id'] in first_exposure_recall_loci,'candidate_prompt':sp['recall'][0],'answer':sp['recall'][1],'timing':'If enabled, ask only after the science-bearing action and canonical term have been encountered. Otherwise schedule retrieval later in Review.','hint_rule':'Return to one concrete visual/action from this scene without displaying the answer term.'}
    else:
        qr={'enabled':False,'reason':'No first-exposure interruption at this locus; retrieval can be scheduled later in Review.'}
    briefs.append({
      'scene_brief_id':f"F3-{l['locus_id']}",
      'locus_id':l['locus_id'],'journey_id':l['journey_id'],'bundle_id':l['bundle_id'],
      'scene_title':l['title'],'exact_location':l['title'],'micro_anchor':l['micro_anchor'],
      'orientation_sentence':sp['orientation'],
      'spatial_layout':{
        'left':{'anchor':l['scene_geometry']['left'],'layout_job':'fixed left visual zone; must remain visible long enough for spatial encoding'},
        'center':{'anchor':l['scene_geometry']['center'],'layout_job':'primary action/focal zone; the central science-bearing change occurs here'},
        'right':{'anchor':l['scene_geometry']['right'],'layout_job':'fixed right visual zone; typically consequence, comparison, or destination'}
      },
      'stable_cast':cast,
      'science_bearing_action':{
        'before':sp['before'],
        'trigger':'Nia identifies the local failure/question and directs attention to the fixed micro-anchor.',
        'during':sp['during'],
        'after':sp['after']
      },
      'knowledge_ids':kids,
      'primary_knowledge_id':l['primary_knowledge_id'],
      'term_introductions':term_intros,
      'visual_spec':{
        'visual_mode':l['visual_mode'],'conventional_scientific_visual_required':True,
        'must_show':sp['must_show'],
        'composition_rule':'The illustration must preserve the left/center/right geography and recognizable biological geometry. Narrative styling may increase salience but may not alter scientific structure.'
      },
      'misconception_guards':sp['guards'],
      'adaptive_name_support':{
        'default':'No phonological keyword is shown during the first pass unless needed for a difficult exact name.',
        'fallback':'If later retrieval fails, use the F2 name-support classification for the specific knowledge record; never replace the scientific image with a disconnected mnemonic spectacle.'
      },
      'quick_recall':qr,
      'carry_forward':sp['carry'],
      'causal_transition':{'to_locus_id':next_locus,'transition_logic':sp['transition']},
      'story_prose_status':'PROHIBITED_UNTIL_F3_BRIEF_QA_PASS',
      'brief_status':'LOCKED_F3_SCENE_BRIEF'
    })

journey_doc={
 'schema':'memory-palace-v2-unit2-f3-journey-briefs-1.0','generated_utc':GEN,
 'unit_id':'unit-2','student_release':False,'unit_guide':unit_guide,
 'journey_count':len(journey_briefs),'journeys':journey_briefs
}
scene_doc={
 'schema':'memory-palace-v2-unit2-f3-scene-briefs-1.0','generated_utc':GEN,
 'unit_id':'unit-2','canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','student_release':False,
 'design_standard':'Every permanent locus must be spatially explicit, scientifically diagnostic, causally connected, and narratively usable before polished prose is allowed.',
 'counts':{'journeys':7,'scene_briefs':49,'palace_managed_records':133,'term_introductions':sum(len(x['term_introductions']) for x in briefs),'optional_first_exposure_recalls':sum(x['quick_recall'].get('enabled',False) for x in briefs)},
 'scene_briefs':briefs
}
dump(BRIEFS/'journey-briefs-f3.json',journey_doc)
dump(BRIEFS/'scene-briefs-f3.json',scene_doc)

# F2 status.json is part of the immutable F2 lock. F3 writes a new status artifact.
status=load(U2/'status.json')
status.update({
 'status':'SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED',
 'pipeline_stage':'NARRATIVE_SCENE_BRIEFS_COMPLETE',
 'scene_brief_lock':'LOCKED_F3','student_release':False,
 'scene_briefs':49,'journey_briefs':7,
 'optional_first_exposure_recalls':scene_doc['counts']['optional_first_exposure_recalls'],
 'narrative_story_files':0,
 'next_required_output':'F4 polished Unit 2 narratives written from the locked F3 briefs, followed by prose-level narrative QA before any student release'
})
dump(U2/'status-f3.json',status)

# Update the mutable course registry to advertise the newest development gate.
course_path=ROOT/'content'/'ap-biology'/'course.json'
course=load(course_path)
for unit in course['units']:
    if unit['unit_id']=='unit-2':
        unit.update({
          'status':'SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED',
          'source_status':'AUDITED_F1_ARCHITECTURE_LOCKED_F2_SCENE_BRIEFS_LOCKED_F3',
          'scene_brief_lock':'LOCKED_F3','scene_briefs':49,'journey_briefs':7,
          'journey_count':0,'scene_count':0
        })
dump(course_path,course)

# F3 release manifest first (lock intentionally excludes itself)
manifest={
 'schema':'memory-palace-v2-unit2-f3-release-manifest-1.0','generated_utc':GEN,'unit_id':'unit-2','release':'F3_SCENE_BRIEF_LOCK','student_release':False,
 'canonical_records':142,'palace_managed_records':133,'challenge_lab_records':9,'journeys':7,'scene_briefs':49,
 'term_introductions':scene_doc['counts']['term_introductions'],'optional_first_exposure_recalls':scene_doc['counts']['optional_first_exposure_recalls'],
 'polished_story_files':0,
 'gate':'F3 briefs may guide F4 prose generation only after F3 QA passes. Unit 2 remains inaccessible as student journeys.'
}
dump(U2/'f3-release-manifest.json',manifest)

files=[
 'content/ap-biology/unit-2/source/canonical-unit2-f1.json',
 'content/ap-biology/unit-2/architecture/learning-classification-f2.json',
 'content/ap-biology/unit-2/architecture/palace-architecture-f2.json',
 'content/ap-biology/unit-2/briefs/journey-briefs-f3.json',
 'content/ap-biology/unit-2/briefs/scene-briefs-f3.json',
 'content/ap-biology/unit-2/f3-release-manifest.json',
 'content/ap-biology/unit-2/status-f3.json',
]
lock={
 'schema':'memory-palace-v2-unit2-f3-content-lock-1.0','generated_utc':GEN,'unit_id':'unit-2','lock_status':'LOCKED_F3','student_release':False,
 'parents':['LOCKED_F1','LOCKED_F2'],
 'files':{rel:{'sha256':sha(ROOT/rel)} for rel in files},
 'rule':'F3 locks learning scene briefs and journey continuity. It does not authorize changes to F1 canonical science or F2 record/locus assignment.'
}
dump(U2/'content-lock-f3.json',lock)
print('Built Unit 2 F3 scene briefs:',len(briefs),'optional recalls:',scene_doc['counts']['optional_first_exposure_recalls'])
