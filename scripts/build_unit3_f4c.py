from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content'/'ap-biology'/'unit-3'
briefs=json.loads((U3/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
jbriefs=json.loads((U3/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
B={s['locus_id']:s for s in briefs if s['journey_id']=='U3-J3'}
J3=next(j for j in jbriefs if j['journey_id']=='U3-J3')

GUIDE={
 'name':'Dr. Nia Park',
 'role':'cellular-energetics investigator',
 'visual':'navy field jacket, clear safety glasses, and a compact tablet showing energy-flow, reaction, and ATP-coupling models',
 'story_job':'Nia keeps the energy hall spatially stable, makes each energy transformation visible, asks you to track where usable energy goes, and names scientific terms only after the relationship is clear.'
}

route=[
 {'scene_index':0,'locus':'Metabolism Route Map','short':'Route Map','floor':'Energy hall entrance','symbol':'⇄'},
 {'scene_index':1,'locus':'Energy Forms Gallery','short':'Energy Gallery','floor':'Conversion gallery','symbol':'◈'},
 {'scene_index':2,'locus':'First-Law Ledger','short':'First-Law Ledger','floor':'Accounting corridor','symbol':'Σ'},
 {'scene_index':3,'locus':'Entropy and Living Order Chamber','short':'Entropy Chamber','floor':'Order-maintenance room','symbol':'≈'},
 {'scene_index':4,'locus':'Free-Energy Terrain','short':'Free-Energy Terrain','floor':'Reaction landscape','symbol':'⌁'},
 {'scene_index':5,'locus':'Cellular Work Dock','short':'Work Dock','floor':'Three-bay work station','symbol':'⚙'},
 {'scene_index':6,'locus':'ATP Structure Station','short':'ATP Station','floor':'Molecular assembly bay','symbol':'ATP'},
 {'scene_index':7,'locus':'ATP Hydrolysis Forge','short':'Hydrolysis Forge','floor':'Coupling forge','symbol':'Pi'},
 {'scene_index':8,'locus':'ATP Regeneration Wheel','short':'ATP Wheel','floor':'Regeneration chamber','symbol':'↻'},
 {'scene_index':9,'locus':'Conserved Metabolism Archive','short':'Metabolism Archive','floor':'Cross-species archive','symbol':'∞'},
]

ZONE_COPY={
'U3-L12':[
 ('left','Catabolic breakdown branch','↓','A fixed left branch accepts a large molecular model and carries it through enzyme-controlled breakdown steps toward smaller products.'),
 ('center','Shared metabolic pathway map','→','A wall-sized central pathway map shows sequential enzyme-catalyzed reactions and the intermediate molecules that connect one reaction to the next.'),
 ('right','Anabolic synthesis branch','↑','A fixed right branch accepts small precursor molecules and assembles them into a larger product while an energy-input meter remains visible.')],
'U3-L13':[
 ('left','Kinetic and thermal displays','⇆','Moving carts and a chamber of randomly moving molecular particles remain fixed on the left as examples of motion-associated energy.'),
 ('center','Energy-conversion turntable','◈','A central turntable carries one glowing tracking token through controlled transformations while a ledger records the form being represented.'),
 ('right','Potential and chemical displays','▲','A raised mass and a conventional molecular model remain fixed on the right to represent stored energy associated with position, structure, and chemical arrangement.')],
'U3-L14':[
 ('left','Energy input ledger','IN','A calibrated left-side ledger records a fixed energy input before any transformation begins.'),
 ('center','Transformation and accounting panel','Σ','The central accounting wall follows the input through work, stored forms, and heat without allowing any energy to appear or disappear from the total.'),
 ('right','Energy output ledger','OUT','A matching right-side ledger records the transformed outputs and heat that leave the modeled system.')],
'U3-L15':[
 ('left','Organized cellular system','▦','A highly ordered cell model with maintained gradients, macromolecular organization, and directed processes remains fixed on the left.'),
 ('center','Maintenance-energy input','⚡','A central supply conduit delivers usable energy to the cell model and can be opened, reduced, or shut off.'),
 ('right','Dispersed heat and environmental entropy','≈','A right-side thermal display records energy dispersing to the surroundings as heat while the total entropy indicator rises.')],
'U3-L16':[
 ('left','Exergonic downhill path','↘','A leftward reaction path descends from a higher-free-energy reactant state toward a lower-free-energy product state.'),
 ('center','Free-energy and equilibrium reference','G','A central reference plane marks relative Gibbs free energy and the equilibrium basin without requiring the full Gibbs free-energy equation.'),
 ('right','Endergonic uphill path','↗','A rightward reaction path rises toward products with higher free energy and remains stalled until coupled energy is supplied.')],
'U3-L17':[
 ('left','Mechanical-work bay','↔','A molecular motor and a contractile filament model occupy the left bay and move only when the center coupling junction supplies usable energy.'),
 ('center','Energy-coupling junction','⚙','The central junction receives energy from a favorable process and routes that energy into work that would otherwise be thermodynamically unfavorable.'),
 ('right','Transport and chemical-work bays','⇧','A membrane pump and a polymer-building station occupy two fixed right-side platforms and activate from the same center coupling junction.')],
'U3-L18':[
 ('left','Adenine-ribose body','AR','A conventional adenine-plus-ribose model remains fixed on the left as the adenosine portion of ATP.'),
 ('center','Triphosphate chain','P-P-P','Three phosphate groups extend from the adenosine model at center so ATP structure is recognizable before hydrolysis is discussed.'),
 ('right','ADP plus inorganic phosphate comparison','ADP + Pi','A side-by-side ADP and inorganic phosphate model remains fixed on the right for direct structural comparison with ATP.')],
'U3-L19':[
 ('left','ATP hydrolysis input','ATP + H₂O','ATP and water enter from the left while an energy profile records the free-energy state before reaction.'),
 ('center','Coupling and phosphorylation forge','⇢Pi','The central forge can either display ATP hydrolysis to ADP plus inorganic phosphate or transfer a phosphate group directly to a target in a coupled reaction.'),
 ('right','Altered phosphorylated target','P-target','A target molecule or protein remains fixed on the right so the learner can see how phosphorylation changes its free energy, reactivity, or conformation.')],
'U3-L20':[
 ('left','ADP plus Pi return path','ADP + Pi','ADP and inorganic phosphate return from completed cellular work along a fixed left-side track.'),
 ('center','ATP regeneration wheel','↻','A central wheel uses energy released by exergonic processes to reform ATP from ADP and inorganic phosphate.'),
 ('right','ATP use for cellular work','ATP→work','Newly regenerated ATP exits on the right toward chemical, transport, and mechanical work before returning as ADP and phosphate.')],
'U3-L21':[
 ('left','Prokaryotic pathway record','B/A','Bacterial and archaeal records occupy the fixed left archive and show core energy pathways operating without mitochondria.'),
 ('center','Conserved core reactions display','∞','A central overlay highlights shared pathway logic such as glycolysis and chemiosmotic ATP production across deeply separated lineages.'),
 ('right','Eukaryotic pathway record','E','A eukaryotic record remains fixed on the right and shows the same core logic organized within eukaryotic cellular compartments.')],
}

CAST={
'U3-L12':[
 ('glowing energy tracker','continuity object','a small luminous disk carried beside the pathway map as a bookkeeping marker, never portrayed as a literal particle of energy','track where usable energy is released, required, transformed, or transferred as metabolism proceeds'),
 ('large molecular substrate','scientific input','a conventional large molecular model entering the left breakdown branch','be broken into smaller products through sequential enzyme-catalyzed reactions'),
 ('small precursor set','scientific input','several small molecular building blocks entering the right synthesis branch','be assembled into a larger product when energy input is supplied')],
'U3-L13':[
 ('glowing energy tracker','continuity object','the same luminous bookkeeping disk from the metabolism map, now riding the center turntable','mark the form of energy being represented without implying that energy itself is a material token'),
 ('moving cart','scientific model','a small cart whose speed can be measured on the left motion track','make kinetic energy visible through motion'),
 ('molecular-motion chamber','scientific model','a transparent chamber filled with particles moving randomly at measurable speeds','represent thermal energy as kinetic energy associated with random molecular motion')],
'U3-L14':[
 ('glowing energy tracker','continuity object','the same bookkeeping marker entering the left ledger with a fixed recorded amount','follow the accounted energy through transformation and transfer'),
 ('input counter','scientific measurement','a fixed calibrated display on the left ledger','record energy entering the modeled system'),
 ('output counter','scientific measurement','a matched display on the right ledger','record energy leaving as work, stored forms, or heat')],
'U3-L15':[
 ('organized cell model','scientific system','a transparent cell model whose gradients, structures, and directed processes are visibly maintained only while energy flows','show that local biological order requires continuing energy input'),
 ('energy supply conduit','scientific control','a glowing central conduit whose flow can be reduced or stopped','control the usable-energy input to the organized cell model'),
 ('heat dispersal display','scientific output','a broad right-side thermal field that spreads outward into the surroundings','show that energy transformations disperse energy and increase total entropy')],
'U3-L16':[
 ('reaction pair','scientific comparison','two conventional reactant-to-product energy diagrams placed on opposite sides of one shared free-energy reference','compare favorable and unfavorable free-energy changes'),
 ('equilibrium marker','scientific reference','a central basin marker showing the equilibrium condition for the modeled reaction system','separate thermodynamic direction from the living cell state that continually maintains disequilibrium'),
 ('glowing energy tracker','continuity object','the same bookkeeping disk resting at the central reference plane','show whether a process releases usable free energy or requires coupling to another process')],
'U3-L17':[
 ('energy-coupling junction','scientific mechanism','a transparent center coupling module that connects one energy-releasing process to a separate work-requiring process','make energy coupling visible as a relationship between processes'),
 ('molecular motor','scientific example','a motor-protein model in the left bay that changes conformation and moves a load','represent mechanical cellular work'),
 ('membrane pump and polymer station','scientific examples','a membrane transporter and a monomer-assembly bench on the right','represent transport work and chemical work')],
'U3-L18':[
 ('ATP model','scientific structure','an enlarged conventional nucleotide model with adenine, ribose, and three phosphates','establish ATP structure before any claim about hydrolysis or coupling'),
 ('ADP model','scientific comparison','the corresponding adenosine diphosphate model on the right','make the structural change from ATP to ADP visible'),
 ('inorganic phosphate','scientific comparison','a separate Pi model beside ADP','show the phosphate product or reactant involved in ATP cycling')],
'U3-L19':[
 ('ATP and water','scientific inputs','conventional ATP and H₂O molecular models entering the left side of the forge','undergo the complete hydrolysis reaction whose products have lower free energy'),
 ('phosphate-transfer arm','scientific mechanism','a central reaction display that can transfer ATP-derived phosphate to a target molecule','show phosphorylation as a chemical change that can alter target behavior'),
 ('target molecule','scientific output','a conventional molecule or protein model on the right with a visible phosphate-attachment site','show how ATP-driven phosphorylation can change reactivity, free energy, or conformation')],
'U3-L20':[
 ('ADP and Pi return stream','continuity input','ADP and inorganic phosphate models returning from the work dock','provide the substrates for ATP regeneration'),
 ('catabolic energy feed','scientific input','a separate center-side conduit carrying usable energy released by exergonic catabolic reactions','drive ATP regeneration without implying that ATP is created from nothing'),
 ('ATP output stream','scientific output','fresh ATP models leaving the wheel toward cellular work','show continuous ATP turnover and reuse of ADP and phosphate')],
'U3-L21':[
 ('bacterial and archaeal records','evolutionary evidence','left-side pathway diagrams from bacterial and archaeal cells with conventional membrane and cytosolic locations','show core metabolic logic in prokaryotic lineages'),
 ('eukaryotic record','evolutionary evidence','a right-side pathway diagram with glycolysis in cytosol and oxidative phosphorylation associated with mitochondria','show comparable core metabolic logic in eukaryotes'),
 ('conserved overlay','scientific comparison','a transparent center overlay that aligns homologous pathway logic across all three domains','highlight conservation consistent with common ancestry')],
}

NARR={
'U3-L12':{
 'title':'The Map With Two Opposite Roads',
 'kicker':'The hall cannot balance its energy ledger because breakdown and synthesis have been merged into one meaningless arrow.',
 'paragraphs':[
  "You leave the enzyme control wing through a wide steel door and enter the **Metabolism Route Map**. The room is circular, but its working wall is simple enough to redraw. On your **left**, a dark-blue branch slopes downward through a series of reaction stations. Directly **ahead**, a wall-sized pathway map shows connected boxes joined by arrows. On your **right**, a green branch climbs upward toward a large molecular product. Nia places a small glowing disk beside the center map. ‘This is only an accounting marker,’ she says. ‘It helps us track energy. Energy itself is not a little object that travels around the cell.’ The hall’s ledger is dark because the two branches have been labeled as if they were the same process.",
  "Nia sends one large molecular model into the **left** branch. An enzyme at the first station changes it into smaller products. One of those products rolls directly into the next station and becomes a reactant there. The sequence continues, step after step. Nia traces the connected reactions on the **center** wall. This is a **metabolic pathway**, a sequence of enzyme-catalyzed reactions in which **pathway intermediates** connect an initial substrate to later products. The product of one reaction can become the reactant for the next. These **sequential metabolic pathways** allow cells to transfer and control energy through a series of manageable chemical steps. The enzymes at each station are the same kind of catalysts you studied in the workshop. Here they are catalyzing reactions inside a larger route.",
  "The large molecule continues down the left branch and finishes as several smaller products. As that happens, the ledger beside the glowing disk records usable energy becoming available. Nia names this branch a **catabolic pathway**. Catabolic pathways break complex molecules into simpler products and typically release usable energy. She taps the enzyme symbols along the branch. **Enzymes in catabolic reactions** catalyze those breakdown steps. The word catabolic describes the direction of the pathway. It does not mean that the reactions happen without enzymes or without regulation.",
  "Now Nia activates the **right** branch. Small precursor molecules enter from below. They do not assemble themselves into a larger product. The branch draws energy from the center ledger while enzyme-controlled reactions join and modify the precursors step by step. Nia names this an **anabolic pathway**. Anabolic pathways build complex molecules from simpler components and require energy input. **Enzymes in anabolic reactions** catalyze these biosynthetic steps just as enzymes can catalyze catabolic steps. The two branches therefore point in opposite chemical directions while sharing the same general logic of controlled, enzyme-catalyzed reactions.",
  "The center wall finally lights as both branches connect into one larger network. Nia labels the complete network **metabolism**, the full set of chemical reactions occurring within a cell or organism. The ledger now makes sense. Breakdown can supply smaller molecules and usable energy. Synthesis can consume precursors and energy. Intermediates can connect one reaction to another. The glowing accounting disk flashes, then rolls through a doorway directly ahead. On the far side you can already see a cart moving, molecules jittering in a glass chamber, a raised weight, and a molecular model. ‘Before we can balance metabolism,’ Nia says, ‘you need to know what we mean when we say energy changes form.’"
 ],
 'close':'The two metabolic branches remain fixed behind you, and the glowing tracker leads forward into a gallery where the same energy ledger must recognize several different forms.',
 'images':{}
},
'U3-L13':{
 'title':'The Gallery Where Energy Changes Its Appearance',
 'kicker':'The ledger keeps treating motion, heat, position, and chemical arrangement as unrelated currencies.',
 'paragraphs':[
  "You follow the glowing tracker into the **Energy Forms Gallery**. The floor narrows into three permanent zones. On your **left**, a small cart circles a track beside a clear chamber filled with rapidly moving particles. Directly **ahead**, a round turntable carries the glowing tracker beneath a ceiling display. On your **right**, a metal weight hangs high above the floor beside a conventional molecular model. Nia keeps the tracker on the center turntable. ‘Remember what it represents,’ she says. ‘We are following the capacity to cause change or perform work. That capacity is **energy**.’",
  "She sends the cart across the left track. As its speed increases, the motion meter rises. Nia names this **kinetic energy**, energy associated with motion. She then points to the neighboring particle chamber. The particles move in random directions, continually colliding and changing speed. Their collective microscopic motion is **thermal energy**, kinetic energy associated with the random movement of atoms and molecules. The two displays share motion, yet they are not identical pictures. One makes organized visible motion easy to see. The other makes random molecular motion visible.",
  "The turntable rotates toward the **right**. Nia raises the metal weight and locks it in place. It is no longer moving, yet the display still records stored capacity to produce change if the weight is released. This is **potential energy**, stored energy associated with position or structure. She then moves the glowing tracker to the molecular model beside it. The molecule is not a container with a yellow packet of energy hidden inside a single bond. Its molecular structure and chemical arrangement contribute to a free-energy state that can change during reactions. Nia names **chemical energy** as potential energy associated with molecular structure that can be transformed through chemical reactions.",
  "The gallery now runs one continuous conversion. The raised weight falls and turns a wheel. Some organized motion becomes random molecular motion in the machinery and surroundings. A chemical reaction on the right changes molecular structure and drives another moving part. The glowing disk changes its label each time the representation changes. Nothing about the disk is meant to suggest that a material substance called energy is being passed from hand to hand. It is the ledger’s marker for tracking energy transformations.",
  "At the end of the demonstration, the ceiling display asks a harder question. If energy can appear as motion, thermal motion, stored position, or chemical arrangement, can the total simply disappear when a transformation becomes messy? Nia walks through the center doorway before the gallery can answer. Beyond it is a black wall with two columns marked IN and OUT and a large total sign between them. ‘Now we balance the account,’ she says."
 ],
 'close':'Motion, thermal motion, stored position, and molecular structure remain distinguishable behind you as the tracker enters the accounting wall that tests whether any energy was created or lost.',
 'images':{}
},
'U3-L14':{
 'title':'The Ledger That Refuses to Lose a Joule',
 'kicker':'The hall reports missing energy whenever useful output becomes heat.',
 'paragraphs':[
  "The doorway opens into the **First-Law Ledger**. On your **left**, a bright input counter waits at zero. Directly **ahead**, a glass accounting panel branches into several transformation channels. On your **right**, a matching output counter records work, stored energy, and heat leaving the modeled system. Nia places the glowing tracker on the left scale and enters a fixed amount of energy. ‘This room studies energy transformations in matter,’ she says. That field is **thermodynamics**.",
  "The center panel starts. Part of the input drives a molecular motor. Another part changes the chemical state of a molecule. A third part spreads into the surroundings as heat. Each output appears separately on the right, and the total climbs until it matches the input. Nia deliberately covers the labels and makes you watch the numbers. The forms have changed. The locations have changed. The total has not appeared from nowhere and has not vanished. She names the relationship the **first law of thermodynamics**. Energy cannot be created or destroyed. It can be transferred or transformed.",
  "Nia reruns the model with a living cell displayed in the center panel. Chemical energy enters through metabolism. The cell performs transport, chemical, and mechanical work. Heat spreads outward. The right ledger still closes. ‘A living cell is organized,’ Nia says, ‘but it does not sit outside physics.’ She names the broader relationship **life and thermodynamics**. The high degree of order in living systems is consistent with both thermodynamic laws. The first law tells you that cells cannot manufacture energy from nothing. Every cellular transformation must remain part of an energy account.",
  "The accounting wall now produces a strange result. The input and output totals match perfectly, yet the second run leaves more of the recorded energy dispersed as heat and less available to power another round of directed work. The first law is satisfied, but the ledger flashes a second warning. Nia points through a narrow opening beside the output column. On the other side, a beautifully organized cell model is being maintained by a glowing supply conduit while heat spreads across the room. ‘Conservation is only half of the story,’ she says.",
  "You leave the balanced ledger intact. It has answered whether energy disappears. It has not answered why every transformation changes how available that energy is for future work, or how a cell can remain locally organized while the universe still obeys the second law. Those questions wait in the next chamber."
 ],
 'close':'The first account balances exactly, yet the spreading heat leads you into a chamber where the quality and dispersal of energy become as important as the conserved total.',
 'images':{}
},
'U3-L15':{
 'title':'The Cell That Stays Ordered Only While Energy Flows',
 'kicker':'The first law balances, but the organized cell still collapses when the energy supply is shut off.',
 'paragraphs':[
  "You enter the **Entropy and Living Order Chamber** and stop between three fixed displays. On your **left**, a transparent cell model holds ion gradients, organized membranes, moving vesicles, and carefully maintained molecular arrangements. Directly **ahead**, a bright supply conduit feeds usable energy into the model. On your **right**, a broad thermal field spreads outward into the surroundings. Nothing in the room is hidden. The cell looks highly ordered, and heat is already leaving it.",
  "Nia opens the center conduit. The cell maintains its gradients, repairs structures, drives reactions, and keeps material moving in controlled directions. At the same time, the right-side heat field continues to expand. Nia names the governing relationship the **second law of thermodynamics**. Every energy transfer or transformation increases the entropy of the universe, and some energy becomes less available to perform work, often dispersing as heat. The cell’s order does not violate that law. The system includes the cell and its surroundings.",
  "She highlights the cell on the left and the thermal field on the right at the same time. The cell can become or remain more ordered locally while total entropy of the system plus surroundings increases. Nia names this **entropy and living order**. The useful mental image is the whole room. Local organization on the left is sustained through energy flow in the center while dispersed heat expands on the right. The cell does not need the universe to become more ordered around it in order to maintain its own internal organization.",
  "Nia now narrows the center conduit. Repair slows first. Then transport gradients begin to weaken. When the energy input falls below what the model needs to offset losses and power cellular processes, ordered activity deteriorates. The display labels the requirement **energy input and maintenance**. Energy input must exceed energy loss to maintain biological order and power cellular processes. She closes the conduit completely. The cell’s coordinated processes fail, gradients collapse, and the organized display darkens. A severe **loss of energy flow** or biological order is incompatible with continued life and can result in death.",
  "The right-side heat field continues to glow after the cell has gone dark. Nia does not call entropy a synonym for messiness. She leaves the second-law statement on the wall and points instead to a reaction landscape opening ahead. Two paths run away from a central reference. One slopes downward. One climbs upward. ‘We have tracked total energy and its dispersal,’ she says. ‘Now we ask which chemical changes can supply usable free energy for work.’"
 ],
 'close':'The organized cell teaches that life requires continuous energy flow, and the next room asks which reactions can provide that usable energy under cellular conditions.',
 'images':{}
},
'U3-L16':{
 'title':'The Terrain With a Downhill Path and an Uphill Path',
 'kicker':'Two reactions can obey both thermodynamic laws while differing completely in whether they can drive cellular work.',
 'paragraphs':[
  "The floor opens into the **Free-Energy Terrain**. The geography stays fixed. On your **left**, a reaction path descends from a higher platform to a lower one. Directly **ahead**, a transparent reference plane marks relative free energy and an equilibrium basin. On your **right**, a second reaction path climbs toward a higher product platform. Nia places the glowing tracker at the center reference. ‘This display is a model of chemical free-energy relationships,’ she says. ‘Molecules are not literally rolling down a hill.’",
  "She activates the left reaction. The product state lies lower in free energy than the reactant state. The sign over the path reads negative change in free energy. Nia names it an **exergonic reaction**. An exergonic reaction has a negative change in free energy and can proceed spontaneously in the thermodynamic sense. She immediately places a small activation barrier near the start, linking the terrain back to the enzyme workshop. Thermodynamic spontaneity does not guarantee a fast reaction. A favorable reaction can still proceed slowly when a substantial activation-energy barrier exists.",
  "The right path behaves differently. Its products sit at higher free energy than its reactants. The model refuses to proceed unless another process supplies usable energy. Nia names this an **endergonic reaction**. An endergonic reaction has a positive change in free energy and requires coupling to an energy-releasing process to proceed in cells. The left and right paths remain visible together, so the distinction is spatial. One can release free energy as it proceeds toward a lower-free-energy state. The other requires an input or coupling that makes the combined process thermodynamically favorable.",
  "Nia then labels the vertical reference **Gibbs free energy**. Gibbs free energy describes the portion of a system’s energy that can perform work under specified conditions. The display deliberately withholds the full Gibbs free-energy equation. You need the relationship here, not a memorized formula. The equilibrium basin remains at center as a warning. If every coupled reaction in a living cell simply settled into equilibrium and stayed there, there would be no sustained directional flow left to power cellular work.",
  "The whole terrain begins to flatten toward the equilibrium basin. Nia stops it before the process finishes. Living cells maintain flows of matter and energy and remain **far from equilibrium**. Reaching equilibrium is incompatible with sustained cellular work. A door on the far side of the left slope unlocks. Through it, you can see a molecular motor, a membrane pump, and a polymer-building station waiting in three separate bays. ‘A favorable process becomes biologically useful when cells connect it to work,’ Nia says."
 ],
 'close':'The downhill exergonic path and uphill endergonic path remain fixed behind you as the tracker moves to a junction where favorable processes are connected directly to cellular work.',
 'images':{}
},
'U3-L17':{
 'title':'The Dock Where Energy Has to Do Something',
 'kicker':'The ledger has usable free energy, but the cell gains nothing until that energy is coupled to actual work.',
 'paragraphs':[
  "You enter the **Cellular Work Dock** and stop at a three-bay station. On your **left**, a molecular motor grips a filament but does not move. Directly **ahead**, a transparent coupling junction waits between an energy-releasing process and the three work bays. On your **right**, a membrane pump faces an unfavorable concentration gradient beside a polymer-building bench. Nia sets the glowing tracker in the center junction. ‘Every living system requires an **energy input**,’ she says. ‘The next question is how cells connect that energy to tasks that need it.’",
  "Nia activates an energy-releasing process at the center. The junction does not send an invisible force into the room. It couples a favorable chemical change to another process. The left motor changes conformation and pulls its load along the filament. Nia names this **mechanical cellular work**. Mechanical work includes processes such as ciliary movement, chromosome movement, and muscle contraction. The important feature is a physical change in position driven by molecular machinery.",
  "She diverts the center coupling to the membrane pump on the **right**. Solute begins moving across the membrane in a direction that is not thermodynamically favored by the existing gradient. This is **transport work**, the movement of substances across membranes against thermodynamically favored directions. Then the polymer station activates beside it. Separate monomers are joined into a larger molecule through an endergonic synthesis process. Nia names this **chemical work**. Chemical work drives endergonic reactions such as polymer synthesis from monomers.",
  "All three bays stop when Nia disconnects the center junction, even though the machines themselves are intact. She reconnects it and the work resumes. This relationship is **energy coupling**. Cellular processes that release energy can be coupled to processes that require energy. The room therefore turns the free-energy terrain into a working system. A favorable process can help drive an unfavorable one when the processes are chemically or mechanically coupled so the combined change can proceed.",
  "The dock is operating, but its central junction is too large and cumbersome to carry from one cellular process to another. Nia opens a small molecular cabinet beside the exit. Inside sits one enlarged nucleotide with three phosphates and, beside it, an ADP model plus a separate inorganic phosphate. ‘Cells use several coupling mechanisms,’ she says. ‘One molecule is especially common as an immediate energy-coupling currency.’ You follow her into the assembly station."
 ],
 'close':'Mechanical, transport, and chemical work are now tied to energy coupling, and the next station introduces the molecular structure cells repeatedly use to make many of those couplings portable.',
 'images':{}
},
'U3-L18':{
 'title':'The Three-Phosphate Coupling Molecule',
 'kicker':'Before the hall can explain what ATP does, you have to be able to recognize what ATP actually is.',
 'paragraphs':[
  "The **ATP Structure Station** is bright and almost empty. On your **left**, an adenine ring system is attached to a ribose sugar. Directly **ahead**, three phosphate groups extend from that adenosine body in a conventional molecular model. On your **right**, an ADP model sits beside a separate inorganic phosphate labeled Pi. Nia leaves every piece stationary. ‘No metaphors yet,’ she says. ‘First learn the structure you will see in real diagrams.’",
  "She points from adenine to ribose and then along the three phosphates. Together they form **adenosine triphosphate**, or **ATP**. ATP is a nucleotide used as an immediate energy-coupling molecule for many forms of cellular work. The structure explains the name. Adenosine is adenine plus ribose. Triphosphate indicates the chain of three phosphate groups. Nia rotates the model once so you can recognize the same components from another angle, then returns it to the fixed center position.",
  "The right-side comparison now slides closer. ADP retains adenine, ribose, and two phosphates. Pi is shown separately. Nia labels the comparison **ATP structure** and leaves the three-part pattern visible. ATP contains adenine, ribose, and three phosphate groups. The station does not label one phosphate bond as a tiny packet of stored energy. The useful chemistry will come from the overall reaction and the different free-energy states of reactants and products.",
  "Nia places miniature icons from the work dock beneath the ATP model. A motor, a membrane pump, and a synthesis reaction all light when ATP is connected to them. The icons do not claim that ATP is the only energy-coupling molecule in biology. They show why ATP is so useful as an immediate coupling molecule across many cellular processes. The enlarged molecular structure stays visible above the icons, keeping the name attached to a real nucleotide rather than to a vague symbol for energy.",
  "A water molecule appears beside the center ATP model. The floor beneath the third phosphate opens into a forge where a complete reaction-energy display is waiting. Nia carries the same ATP model forward. ‘Now we can ask what hydrolysis does,’ she says, ‘and we can answer it without the shortcut that breaking a bond somehow releases energy by itself.’"
 ],
 'close':'ATP remains recognizable as adenine, ribose, and three phosphates while the molecule moves into the forge where its complete hydrolysis reaction and coupling chemistry can be watched.',
 'images':{}
},
'U3-L19':{
 'title':'The Forge That Exposes the ATP Shortcut',
 'kicker':'The hall’s old sign says energy bursts out when a phosphate bond breaks. Nia makes you test the entire reaction instead.',
 'paragraphs':[
  "You enter the **ATP Hydrolysis Forge**. On your **left**, a conventional ATP molecule and water wait above an input tray. Directly **ahead**, a transparent reaction chamber shows bond changes and a free-energy trace. On your **right**, a target molecule rests beneath a phosphate-attachment arm. An old sign above the forge flashes ENERGY RELEASED WHEN PHOSPHATE BOND BREAKS. Nia switches the sign off. ‘A bond does not hand you energy merely because you break it,’ she says. ‘Track the complete chemical change.’",
  "ATP and water enter the center chamber. The reaction produces ADP and inorganic phosphate. The free-energy trace finishes lower than it began under cellular conditions. Nia names the full process **ATP hydrolysis**. ATP hydrolysis converts ATP and water to ADP and inorganic phosphate and has a negative free-energy change under cellular conditions. She pauses the chamber at the instant a bond is being broken. Energy is required to break chemical bonds. The favorable net result comes from the entire set of bond changes, product stabilization, and interactions that leave the products at lower free energy than ATP plus water.",
  "Nia labels that correction **ATP hydrolysis energy source**. Energy released by ATP hydrolysis comes from the overall chemical change to lower-free-energy products, not from energy released by breaking a phosphate bond itself. The free-energy terrain from the earlier room appears faintly behind the forge. ATP hydrolysis is an exergonic process in this cellular context. That makes it useful for coupling when the chemistry links it to an endergonic target process.",
  "The right-side target now enters the reaction. In one coupled demonstration, a phosphate group derived from ATP is transferred directly to the target while ATP becomes ADP. Nia names the chemical change **phosphorylation**, the transfer or addition of a phosphate group to a molecule. The target’s shape and free-energy state change after the phosphate is attached. ATP-driven phosphorylation can alter a molecule’s reactivity, free energy, or protein conformation. A second target uses the changed phosphorylation state to drive a process that would not proceed on its own.",
  "The forge links the two reactions into one combined process. Nia names this **ATP energy coupling**. Cells couple exergonic ATP hydrolysis to endergonic cellular processes so the combined process can proceed. She leaves ATP, ADP, Pi, and the phosphorylated target all visible at once. The door beyond the forge does not lead to a warehouse of preloaded ATP. It leads to a wheel turning ADP and phosphate back into ATP. ‘A cell cannot spend ATP once and be finished,’ she says. ‘It has to regenerate it continuously.’"
 ],
 'close':'The old bond-breaking shortcut is gone, and ATP hydrolysis is now connected to lower-free-energy products, phosphorylation, and coupled cellular work before ADP and Pi move into the regeneration wheel.',
 'images':{}
},
'U3-L20':{
 'title':'The Wheel That Never Gets to Stop',
 'kicker':'ATP is useful only if the cell can continually rebuild it from the products left after ATP use.',
 'paragraphs':[
  "The **ATP Regeneration Wheel** fills the next chamber. On your **left**, ADP and inorganic phosphate return along a metal track from the work dock and hydrolysis forge. Directly **ahead**, the large regeneration wheel has two input ports. One accepts ADP plus Pi. The other receives usable energy released by exergonic processes such as catabolic reactions. On your **right**, newly formed ATP exits toward cellular work. The wheel is already turning when you arrive.",
  "Nia sends one ATP molecule from the right toward a work station. After ATP is used in a coupled reaction, ADP and phosphate return along the left track. The center wheel then uses energy from an exergonic process to drive the endergonic formation of ATP from ADP and Pi. Fresh ATP leaves on the right and enters another round of work. The same pattern repeats. Nia names it the **ATP regeneration cycle**. ATP is continually regenerated from ADP and inorganic phosphate using energy released by exergonic processes.",
  "She slows the wheel so you can see the accounting. ATP hydrolysis and ATP regeneration are opposite parts of a cycle, and they are powered in opposite thermodynamic directions. Hydrolysis can help drive cellular work. Regeneration requires an energy input. The cell therefore does not create ATP energy from nothing and does not treat ATP as a permanent storage vault. ATP is continually turned over as an immediate coupling molecule.",
  "Nia stops one ATP model on the right and traces its short route. It enters a cellular process, becomes ADP plus Pi, returns on the left track, and is rebuilt at the center wheel using energy supplied by another exergonic process. Then she releases it for another cycle. The same molecules do not have to follow one literal circular track inside a cell. The wheel is a bookkeeping model that keeps ATP use and ATP regeneration connected in one repeatable relationship.",
  "The glowing tracker from the first metabolism map returns to the center wheel. It enters with the energy supplied by catabolic processes, then follows ATP toward cellular work, then reappears in the ledger as energy changes form and disperses. Nia leaves the wheel turning and opens the final archive door. Inside are pathway records from bacteria, archaea, and eukaryotes. ‘This logic is older than any one organelle,’ she says. ‘Now compare how widely it is conserved.’"
 ],
 'close':'ADP, Pi, exergonic energy input, ATP regeneration, and cellular work now form one continuous cycle, which leads directly into an archive comparing the same core energy logic across life.',
 'images':{}
},
'U3-L21':{
 'title':'The Archive Where Different Cells Share the Same Old Logic',
 'kicker':'The final question is whether the energy system you rebuilt is unique to one kind of cell or part of a much older biological inheritance.',
 'paragraphs':[
  "The **Conserved Metabolism Archive** is the quietest room in the hall. On your **left**, pathway records from bacterial and archaeal cells are projected onto a broad screen. Directly **ahead**, a transparent overlay waits to align equivalent pieces of metabolic logic. On your **right**, a eukaryotic record shows cytosolic reactions and mitochondrial energy transformations. Nia places the glowing tracker at the center overlay and removes every decorative symbol from the display. Only the scientific pathway relationships remain.",
  "She begins with glycolytic logic. The records differ in cellular context and detail, yet central steps of glucose breakdown and energy capture can be aligned across deeply separated lineages. The overlay then shifts to chemiosmotic ATP production. Bacteria can establish proton gradients across their plasma membrane. Eukaryotic cells carry out oxidative phosphorylation across the inner mitochondrial membrane. The membrane locations differ, yet the core logic of electron transport, proton gradients, and ATP synthase can be compared across lineages.",
  "Nia names the pattern **conserved core metabolism**. Core metabolic pathways such as glycolysis and oxidative phosphorylation are conserved across Archaea, Bacteria, and Eukarya, supporting common ancestry. The archive does not claim that every metabolic detail is identical in every organism. It highlights deeply shared pathway logic that persists despite enormous evolutionary divergence.",
  "The wall behind you now reconstructs the entire Cellular Energy Exchange Hall. Catabolic and anabolic routes reappear first. Energy changes form. The first law balances the total. The second law remains visible as energy disperses and total entropy increases. Exergonic processes connect to endergonic work. ATP cycles between hydrolysis and regeneration. Finally, the conserved archive places these processes inside evolutionary history. The hall’s dark ledger turns green from end to end.",
  "Nia picks up her tablet and turns toward a glass corridor filled with green light. At its far end you can see chloroplasts, pigment spectra, thylakoid membranes, and two photosystems waiting in sequence. ‘You now have the accounting rules,’ she says. ‘Next we follow a real biological system that captures incoming light energy and converts it into chemical forms a cell can use.’ The doors to the **Light Capture Conservatory** unlock."
 ],
 'close':'The energy ledger now connects metabolism, thermodynamics, free energy, work, ATP cycling, and evolutionary conservation, creating the conceptual foundation for photosynthesis and respiration.',
 'images':{}
},
}

TERM_IMAGES={
'U3-K-019':'the center pathway map showing enzyme-controlled reactions arranged in a sequence',
'U3-K-020':'one intermediate leaving a reaction and entering the next as a reactant',
'U3-K-055':'the full left-center-right reaction network representing all cellular chemical reactions',
'U3-K-056':'a connected sequence of enzyme-catalyzed steps from starting substrate to products',
'U3-K-057':'the left branch breaking a large molecule into smaller products while usable energy becomes available',
'U3-K-058':'the right branch building a larger molecule from smaller precursors while requiring energy input',
'U3-K-089':'enzyme stations catalyzing the left-side breakdown sequence',
'U3-K-090':'enzyme stations catalyzing the right-side biosynthetic sequence',
'U3-K-059':'the glowing accounting marker tracking the capacity to cause change or perform work',
'U3-K-060':'the moving cart whose motion makes kinetic energy visible',
'U3-K-061':'the randomly moving particles whose microscopic kinetic energy appears as thermal energy',
'U3-K-062':'the raised stationary weight retaining stored potential energy',
'U3-K-063':'the conventional molecular model whose structure is associated with transformable chemical potential energy',
'U3-K-015':'the living-cell energy account obeying the same thermodynamic laws as every other physical system',
'U3-K-064':'the center accounting panel tracking transformations of energy in matter',
'U3-K-065':'equal total input and output despite transfers and transformations',
'U3-K-016':'the organized cell maintaining gradients and processes only while energy continues to enter',
'U3-K-018':'the cell model losing coordinated function after the energy supply is shut off',
'U3-K-066':'heat spreading into the surroundings while the total entropy indicator rises',
'U3-K-067':'local cellular order maintained on the left while the combined system and surroundings obey the second law',
'U3-K-068':'the central free-energy reference locating reaction states by their capacity to perform work under specified conditions',
'U3-K-070':'the left reaction path descending toward lower free energy',
'U3-K-071':'the right reaction path requiring coupling to reach a higher-free-energy product state',
'U3-K-072':'the living-cell model prevented from settling into equilibrium because sustained work requires continuing flows',
'U3-K-014':'the work dock remaining inactive until usable energy enters the coupling junction',
'U3-K-017':'the center coupling junction connecting an energy-releasing process to an energy-requiring process',
'U3-K-073':'the molecular motor moving a load in the left bay',
'U3-K-074':'the membrane pump moving solute against a thermodynamically favored direction',
'U3-K-075':'the polymer station using energy to drive biosynthetic chemical work',
'U3-K-076':'the complete adenosine triphosphate molecule serving as an immediate energy-coupling molecule',
'U3-K-077':'adenine, ribose, and three phosphate groups arranged in conventional ATP structure',
'U3-K-078':'ATP plus water becoming ADP plus inorganic phosphate with a negative free-energy change',
'U3-K-079':'the complete hydrolysis reaction ending with lower-free-energy products instead of a fictional burst from one broken bond',
'U3-K-080':'ATP hydrolysis chemically coupled to an endergonic cellular process so the combined process proceeds',
'U3-K-081':'a phosphate group transferred to a target molecule and altering its chemical state',
'U3-K-082':'the wheel repeatedly using exergonic energy to reform ATP from ADP and inorganic phosphate',
'U3-K-021':'the center overlay aligning conserved metabolic logic across bacterial, archaeal, and eukaryotic records',
}

CHECKPOINT_HINTS={
'U3-L12':'Picture the left branch breaking a large molecule into smaller products and the right branch using small precursors plus energy to build a larger product.',
'U3-L16':'Picture the free-energy terrain. The left path ends at a lower free-energy state, while the right path climbs and stalls without coupling.',
'U3-L19':'Picture the whole forge reaction. ATP and water enter, lower-free-energy products emerge, and a phosphate can be transferred to a target during coupling.',
}

scenes=[]
for idx,lid in enumerate(J3['route']):
    b=B[lid]; n=NARR[lid]
    zones=[{'position':pos,'label':lab,'symbol':sym,'description':desc} for pos,lab,sym,desc in ZONE_COPY[lid]]
    cast=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    cast += [{'name':name,'kind':kind,'visual':visual,'job':job} for name,kind,visual,job in CAST[lid]]
    beats=[]; snaps=[]
    for t in b['term_introductions']:
        image=TERM_IMAGES.get(t['knowledge_id'],b['carry_forward'])
        beats.append({'object_id':t['knowledge_id'],'term':t['canonical_term'],'story':image,'science':t['canonical_science'],'exact_name':bool(t.get('exact_name_recall')),'hint':image})
        snaps.append({'term':t['canonical_term'],'meaning':t['canonical_science'],'image':image})
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
 'schema':'memory-palace-v2-unit3-f4c-story-1.0','unit_id':'unit-3','palace_id':'U3-J3','journey_id':'U3-J3',
 'palace_name':'Cellular Energy Exchange Hall','story_title':'The Energy Ledger That Would Not Balance',
 'tagline':'Follow one energy-accounting marker from metabolic pathways through thermodynamic constraints, cellular work, ATP hydrolysis, and ATP regeneration until the hall can account for every transformation.',
 'guide':GUIDE,'premise':J3['premise'],'mission':J3['mission'],
 'finale':'The hall balances only after metabolism is separated into catabolic and anabolic routes, energy forms are tracked under both thermodynamic laws, exergonic processes are coupled to cellular work, ATP hydrolysis is explained through the full reaction, ATP is regenerated continuously, and conserved metabolic logic is recognized across life.',
 'estimated_minutes':30,'scene_count':len(scenes),'checkpoint_count':sum(bool(s['checkpoint']) for s in scenes),
 'learner_rule':'Read or listen while holding the left, center, and right anchors of each room in mind. Track the visible energy relationship first, then attach the scientific term. Quick Recall is optional during the first pass.',
 'route_orientation':'The Cellular Energy Exchange Hall is a ten-station route. Enter at the metabolism map, follow the glowing accounting marker through energy forms and the two thermodynamic-law rooms, cross the free-energy terrain into the work dock, then inspect ATP structure, hydrolysis, regeneration, and the final conserved-metabolism archive. Left, center, and right anchors remain fixed within every station.',
 'route':route,'scenes':scenes,'student_release':'PILOT_PREVIEW_F4C','narrative_standard':'V2-NARRATIVE-3.0-U3-F4C'
}

(U3/'journeys').mkdir(parents=True,exist_ok=True)
(U3/'journeys'/'U3-J3.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

j1=json.loads((U3/'journeys'/'U3-J1.json').read_text(encoding='utf-8'))
j2=json.loads((U3/'journeys'/'U3-J2.json').read_text(encoding='utf-8'))
def card(j): return {k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
registry={'schema':'memory-palace-v2-unit3-f4c-registry-1.0','course_id':'ap-biology','unit_id':'unit-3','unit_title':'Cellular Energetics','narrative_standard':'V2-NARRATIVE-3.0-U3-F4C','journey_count':3,'scene_count':sum(x['scene_count'] for x in (j1,j2,journey)),'checkpoint_count':sum(x['checkpoint_count'] for x in (j1,j2,journey)),'guided_journeys':[card(j1),card(j2),card(journey)]}
(U3/'journeys-f4c.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U3/'status-f4b.json').read_text(encoding='utf-8'))
status.update({'status':'F4C_JOURNEY3_POLISHED_PREVIEW','pipeline_status':'POLISHED_NARRATIVE_JOURNEYS_1_3_F4C','student_release':False,'preview_release':True,'journey_count':3,'scene_count':registry['scene_count'],'polished_journeys':3,'polished_scenes':registry['scene_count'],'polished_checkpoint_count':registry['checkpoint_count'],'narrative_story_files':3,'next_required_output':'F4D polished narrative for Journey 4 Light Capture Conservatory after F4C prose QA'})
(U3/'status-f4c.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(U3/'status.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; c=json.loads(cp.read_text(encoding='utf-8'))
for u in c['units']:
    if u['unit_id']=='unit-3':
        u.update({'status':'F4C_JOURNEY3_POLISHED_PREVIEW','journey_count':3,'scene_count':registry['scene_count'],'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEYS1_3_POLISHED_F4C','polished_journeys':3,'polished_scenes':registry['scene_count'],'student_release':False})
cp.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# Prefer newest Unit 3 registry while preserving historical stage files.
bc=ROOT/'backend'/'content.py'
bs=bc.read_text(encoding='utf-8')
bs=bs.replace('''    if unit_id == "unit-3":
        path=UNIT3_DIR / "journeys-f4b.json"
        if not path.exists(): path=UNIT3_DIR / "journeys-f4a.json"
        return _read_json(path)["guided_journeys"] if path.exists() else []''','''    if unit_id == "unit-3":
        path=UNIT3_DIR / "journeys-f4c.json"
        if not path.exists(): path=UNIT3_DIR / "journeys-f4b.json"
        if not path.exists(): path=UNIT3_DIR / "journeys-f4a.json"
        return _read_json(path)["guided_journeys"] if path.exists() else []''')
bc.write_text(bs,encoding='utf-8')

mainp=ROOT/'backend'/'main.py'
ms=mainp.read_text(encoding='utf-8')
ms=ms.replace('0.13.0-u3-f4b','0.14.0-u3-f4c').replace('v2-apbio-0.13.0-u3-f4b','v2-apbio-0.14.0-u3-f4c')
mainp.write_text(ms,encoding='utf-8')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
files=['journeys/U3-J3.json','journeys-f4c.json','status-f4c.json']
lock={'schema':'memory-palace-v2-unit3-f4c-content-lock-1.0','unit_id':'unit-3','stage':'F4C','student_release':False,'files':{f:sha(U3/f) for f in files}}
(U3/'content-lock-f4c.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit3-f4c-release-manifest-1.0','unit_id':'unit-3','stage':'F4C','student_release':False,'preview_release':True,'polished_journeys':3,'polished_scenes':registry['scene_count'],'journey_3_records':sum(len(s['object_ids']) for s in scenes),'journey_3_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'next_stage':'F4D_JOURNEY4'}
(U3/'f4c-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Built Unit 3 F4C:',len(scenes),'scenes',sum(len(s['object_ids']) for s in scenes),'knowledge records',sum(bool(s['checkpoint']) for s in scenes),'checkpoints')
