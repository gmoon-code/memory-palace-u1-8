from __future__ import annotations
import json, hashlib, re
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
U6=ROOT/'content'/'ap-biology'/'unit-6'
BRIEFS=json.loads((U6/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS=json.loads((U6/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J1=next(j for j in JBRIEFS if j['journey_id']=='U6-J1')
B={b['locus_id']:b for b in BRIEFS if b['journey_id']=='U6-J1'}
CANON={r['knowledge_id']:r for r in json.loads((U6/'source'/'canonical-unit6-f1.json').read_text(encoding='utf-8'))['canonical_catalog']}

GUIDE={
 'name':'Dr. Sora Han',
 'role':'molecular-information systems director',
 'visual':'dark-cobalt lab coat, clear gloves, transparent 5′→3′ compass tablet, and a narrow copper information ledger',
 'story_job':'Sora keeps the same blue-and-gold DNA duplex, its original strand identities, and every 5′/3′ direction marker visible as the molecule moves from storage into replication. She points to real biological structures, changes only the feature needed for the mechanism, and names terms after their defining action is visible.'
}

ROUTE=[
 {'scene_index':0,'locus':'Hereditary Information Intake','short':'Information','floor':'Archive entrance','symbol':'DNA'},
 {'scene_index':1,'locus':'Chromosome Storage Gallery','short':'Chromosomes','floor':'Storage gallery','symbol':'○│'},
 {'scene_index':2,'locus':'Plasmid Ring Vault','short':'Plasmids','floor':'Ring vault','symbol':'◯'},
 {'scene_index':3,'locus':'Base-Class Reading Table','short':'Bases','floor':'Reading room','symbol':'1/2'},
 {'scene_index':4,'locus':'Antiparallel Pairing Bridge','short':'Pairing','floor':'Bridge','symbol':'5′⇅3′'},
 {'scene_index':5,'locus':'Replication Continuity Gate','short':'Purpose','floor':'Copying gate','symbol':'→→'},
 {'scene_index':6,'locus':'Replication Model Test Chamber','short':'Evidence','floor':'Model chamber','symbol':'½'},
 {'scene_index':7,'locus':'Origin and Fork Launch','short':'Fork','floor':'Launch deck','symbol':'Y'},
 {'scene_index':8,'locus':'Primer–Polymerase Dock','short':'Primer','floor':'Synthesis dock','symbol':'3′+'},
 {'scene_index':9,'locus':'Leading–Lagging Split Track','short':'Strands','floor':'Split track','symbol':'⇉'},
 {'scene_index':10,'locus':'Fragment Joining and Repair Bench','short':'Repair','floor':'Repair bench','symbol':'⌁'},
 {'scene_index':11,'locus':'Chromosome-End Dock','short':'Ends','floor':'End dock','symbol':'▥'},
]

ZONES={
'U6-L01':[
 ('left','Franklin and Chargaff evidence wall','✧','A black diffraction panel and a base-composition table occupy the left wall. They remain evidence about DNA structure rather than becoming substitutes for the DNA molecule itself.'),
 ('center','Hereditary-information registry','DNA/RNA','A blue-and-gold DNA duplex rests in a transparent registry cradle beside a smaller RNA record. The tagged duplex will remain the journey’s continuity object.'),
 ('right','Model-building case','⌬','A glass case on the right contains a double-helix model assembled from structural constraints. It records how evidence can constrain a molecular model without turning the history into the main mnemonic target.')],
'U6-L02':[
 ('left','Circular chromosome bay','○','A large circular DNA chromosome occupies the left bay as the typical prokaryotic comparison.'),
 ('center','Chromosome-form platform','↕','The tagged DNA molecule crosses a central platform where chromosome form and packaging can be compared without changing the underlying DNA information.'),
 ('right','Linear chromosome and condensation bay','│→X','Several linear eukaryotic chromosome models occupy the right bay. One can compact around histone-associated packaging into a visibly condensed chromosome form.')],
'U6-L03':[
 ('left','Independent plasmid rack','◯◯','Small circular plasmids sit on a rack separate from the main chromosome, each with its own replication-origin marker.'),
 ('center','Recombinant plasmid bench','✂◯','A circular plasmid lies open on a center bench where a defined DNA segment can be inserted while the molecule remains recognizable as a plasmid.'),
 ('right','Transfer and conditional-value channel','→','A transfer channel carries plasmid DNA toward a recipient bacterial cell beside an environment panel showing that the usefulness of plasmid-carried genes depends on conditions.')],
'U6-L04':[
 ('left','Purine drawer','2 rings','Adenine and guanine cards sit in a left drawer, each drawn with a two-ring nitrogenous-base framework.'),
 ('center','Composition table','A≈T; G≈C','A center table compares base percentages in double-stranded DNA samples and keeps composition relationships separate from base-class identity.'),
 ('right','Pyrimidine drawer','1 ring','Cytosine, thymine, and uracil cards sit in a right drawer, each drawn with a single-ring framework.')],
'U6-L05':[
 ('left','5′/3′ direction rail','5′→3′','A floor rail shows sugar-phosphate backbones with explicit 5′ phosphate-associated and 3′ hydroxyl ends.'),
 ('center','Antiparallel pairing bridge','⇅','The same blue and gold DNA strands span a central bridge in opposite directions, with complementary bases facing inward and hydrogen bonds crossing the gap.'),
 ('right','DNA/RNA architecture panel','DNA | RNA','A right-side panel contrasts typical cellular double-stranded DNA with typically single-stranded RNA that can fold into internally base-paired regions.')],
'U6-L06':[
 ('left','Eukaryotic S-phase marker','S','A eukaryotic-cell timeline lights S phase on the left, while a separate prokaryotic marker prevents that cell-cycle label from being imposed on bacterial chromosome replication.'),
 ('center','Hereditary-continuity gate','COPY','The tagged DNA duplex enters a gate that opens only when its sequence can be copied accurately before transmission to daughter cells or later generations.'),
 ('right','Daughter-DNA destination','2 copies','Two destination cradles wait on the right for copied DNA, making replication a preservation-and-transmission problem rather than a gene-expression process.')],
'U6-L07':[
 ('left','Conservative and dispersive model panels','C/D','Two transparent model boxes on the left predict different ways parental and newly synthesized DNA could be distributed after copying.'),
 ('center','Semiconservative evidence bench','½+½','A center bench keeps the original blue and gold parental strands identifiable while new complementary strands are added beside them.'),
 ('right','Meselson–Stahl density display','15N/14N','A density-gradient display on the right tracks labeled bacterial DNA through generations after transfer from heavy nitrogen to light nitrogen.')],
'U6-L08':[
 ('left','Origin and topoisomerase side','◎ / swivel','The tagged origin sits on the left side of the duplex while a topoisomerase model acts ahead of an opening fork where torsional strain accumulates.'),
 ('center','Replication-fork launch platform','Y','A replication bubble opens at center, exposing two Y-shaped fork boundaries whose positions can move away from the origin.'),
 ('right','Helicase and exposed-template side','unzipped','A helicase complex sits directly at the right-side fork where it separates the parental strands and exposes template DNA.')],
'U6-L09':[
 ('left','Single-strand support and primase side','SSB / RNA','Exposed template DNA is held apart on the left while a primase model lays a short RNA primer with a free 3′ end.'),
 ('center','DNA-polymerase dock','Pol III','A DNA polymerase model locks onto the primer-template junction at center and can add DNA nucleotides only to the primer’s 3′ end.'),
 ('right','Template and synthesis-direction rail','3′→5′ / 5′→3′','Arrows on the right connect polymerase movement along the template with growth of the new DNA strand in the opposite directional sense.')],
'U6-L10':[
 ('left','Leading-strand track','continuous','One branch runs smoothly alongside the opening fork, allowing continuous synthesis of new DNA.'),
 ('center','5′→3′ direction divider','5′→3′','A central direction board forces both new strands to obey 5′→3′ synthesis even though the parental templates are antiparallel.'),
 ('right','Lagging-strand track','fragments','The other branch contains repeated primer starts and short newly synthesized DNA pieces that remain separated as Okazaki fragments.')],
'U6-L11':[
 ('left','Primer replacement and proofreading side','check','RNA-primer positions and a polymerase proofreading window occupy the left, showing cleanup and error checking without expanding into a list of extra enzyme names.'),
 ('center','Ligase joining bench','seal','Lagging-strand DNA fragments meet at a center bench where ligase seals remaining backbone interruptions after primer replacement.'),
 ('right','Mismatch and excision-repair overview','repair','A right-side repair panel shows a mismatched or damaged segment being recognized, removed, and restored using intact sequence information as a guide.')],
'U6-L12':[
 ('left','Telomere chromosome end','repeat','A linear chromosome end on the left terminates in repetitive telomeric DNA and associated protective structure.'),
 ('center','Chromosome-end maintenance dock','END','The copied chromosome is placed at center so the physical DNA end can be distinguished from any enzyme that acts on it.'),
 ('right','Telomerase extension tool','RNA+RT','A telomerase complex sits on the right as an RNA-containing reverse-transcriptase enzyme capable of extending telomeric DNA in cells where it is active.')],
}

NARR={
'U6-L01':{
 'title':'The Archive Refuses to Copy an Unverified Molecule',
 'kicker':'Before the copying works can start, the archive must establish what molecule carries hereditary information and what evidence constrains its structure.',
 'paragraphs':[
  "The entrance to the **Genome Archive and Replication Works** feels less like a museum than a secure records facility built around one molecular object. The room is long and rectangular. On your **left**, a black diffraction panel hangs above a base-composition table, its pale X-shaped pattern and columns of A, T, G, and C values lit from below. Directly **ahead**, in the center of the room, a transparent cradle holds a blue-and-gold DNA double helix. Small arrowheads mark every 5′ and 3′ end, and one copper tag marks a single future replication origin. On your **right**, a glass model-building case contains a double-helix framework assembled from measured constraints. Dr. Sora Han stands beside the center cradle in a dark-cobalt coat, one hand on a transparent 5′→3′ compass tablet and the other on a narrow copper ledger. The copying doors behind the cradle are locked. A red line across them reads: INFORMATION CARRIER NOT VERIFIED.",
  "Sora does not begin with a name. She places a second, smaller nucleic-acid record beside the DNA cradle and asks what the archive must actually preserve from one biological generation to the next. The answer is information encoded in nucleic-acid sequence. In cells, that hereditary information is stored in DNA; in some biological systems, including some viruses, RNA can serve as the hereditary material. Only after the two records are physically filed under the same function does Sora write **DNA/RNA as hereditary information** in the copper ledger: genetic information is stored in and passed to subsequent generations through DNA molecules and, in some cases, RNA molecules. The wording matters. DNA is the usual cellular hereditary material, while the existence of RNA genomes prevents the broader statement from being made absolute.",
  "The left wall now brightens. Sora points first to the diffraction panel. The image is not treated as a magic photograph that contains a finished double helix. **Rosalind Franklin and X-ray diffraction** belong here as evidence: Franklin’s diffraction work supplied critical structural constraints about DNA, including its helical organization and dimensions. The panel gives the model-building case on the right something it must obey. Beside it, the composition table shows another constraint: the measured amounts of particular bases in double-stranded DNA follow relationships that the final model will have to explain. Sora keeps the names on a small brass plaque rather than turning the people into cartoon stand-ins for DNA. Their role in this room is evidentiary.",
  "She crosses to the right-hand case and rotates the physical model. The base pairs fit inside; the sugar-phosphate backbones remain outside. The model is a synthesis of constraints, not the product of one isolated clue. Sora labels this contextual panel **Watson–Crick model-building history**. Watson and Crick constructed a double-helix model by integrating multiple lines of evidence, including base-composition relationships and X-ray diffraction evidence. The case lights only when the model is compatible with what the left wall already showed. That makes the historical sequence useful without confusing the act of model building with the molecule’s biological function.",
  "Now Sora returns to the center cradle. She closes the glass around the blue-and-gold duplex and slides its registry card into the copying system. The red lock changes to amber. The archive has established that a physical nucleic-acid molecule can store hereditary information, but the machine still refuses to copy it. A message appears beneath the duplex: STORAGE FORM UNKNOWN. The same DNA sequence could be packaged as different chromosome architectures, and a copier that cannot distinguish a large chromosome from a small extra-chromosomal circle will misroute the material before replication even begins.",
  "The floor rail activates under the cradle. The blue-and-gold DNA molecule remains tagged and visible as it glides through a wide door into the next gallery. Sora walks beside it, leaving the diffraction and model-building panels behind. Nothing historical follows you. What follows is the molecule itself, still carrying the same 5′/3′ arrows and copper origin tag. The next room is built to answer a more physical question: what form does this hereditary DNA take when a cell stores it as a chromosome?"
 ]},
'U6-L02':{
 'title':'The Gallery of Two Very Different Storage Shapes',
 'kicker':'Chromosome architecture changes across cellular contexts, and packaging must be separated from the DNA sequence being stored.',
 'paragraphs':[
  "The sliding cradle enters the **Chromosome Storage Gallery** and stops on a circular floor platform. The geometry is immediate. On your **left**, a large circular DNA chromosome hangs inside a clear cylindrical bay like a closed loop of cable. Directly **ahead**, the center platform holds the same blue-and-gold DNA sequence from the intake room, now projected as a comparison model whose shape can be changed without changing its sequence. On your **right**, several long linear DNA molecules extend vertically from floor to ceiling; one of them can be compacted around histone-associated packaging until it becomes a dense chromosome form. Sora plants the copper ledger at the edge of the center platform. “Same information problem,” she says. “Different storage architecture.”",
  "She opens the left bay first. The circular chromosome is large and unmistakably separate from the small plasmid rings visible through a locked side window farther down the hall. Sora labels this the **typical prokaryotic chromosome form**. Prokaryotic organisms typically have circular chromosomes. The word *typically* remains on the bay in bright white letters. It prevents the learner from turning a common cellular architecture into a universal rule for every prokaryotic chromosome, viral genome, organelle, or exceptional case. The important image is the scale and role: this is the main chromosome bay, not a tiny accessory ring.",
  "On the right, Sora releases the tall linear models. They do not close into circles. Instead, several distinct linear DNA molecules remain separated from one another, each representing a chromosome. She names the contrast **typical eukaryotic chromosome form**: eukaryotic organisms typically have multiple linear chromosomes composed of DNA. Again, *typically* matters. The point is to recognize the common eukaryotic architecture and its contrast with the left bay, not to memorize an exceptionless slogan.",
  "Then the right-side mechanism changes only one feature. The linear DNA stays linear, but the long molecule progressively associates with histones and other proteins and compacts into a much denser chromosome form. Sora calls the process **eukaryotic chromosome condensation**. Eukaryotic chromosomes are condensed using histones and associated proteins. She keeps a thin uncondensed section visible beside the compacted form so “linear DNA molecule” and “highly condensed chromosome” do not become separate substances in your mind. The DNA information is continuous; the level of packaging changes.",
  "The center platform now freezes a three-part comparison. Left: a typical large circular prokaryotic chromosome. Center: the tracked hereditary DNA sequence whose information has not changed. Right: typical multiple linear eukaryotic chromosomes, one shown in a condensed state. Sora draws a line through the ledger entry labeled STORAGE FORM and checks it off. The copier can now recognize major chromosome architectures without confusing packaging state with sequence identity.",
  "A metallic click comes from the side window. Several small circular rings have begun replicating on their own rack. They are too small to be the main chromosome displayed on the left, yet they are unquestionably DNA. One carries a bright resistance-gene tag; another contains an inserted fluorescent-gene segment. The storage scanner flashes a new warning: EXTRA-CHROMOSOMAL RINGS UNCLASSIFIED. Sora releases the center cradle and follows the smallest ring through the narrow vault door. The next problem is to identify what those circles are and why a cell might keep them at all."
 ]},
'U6-L03':{
 'title':'The Small Rings That Refuse to Stay With the Chromosome',
 'kicker':'A plasmid is extra-chromosomal DNA with its own replication logic, and the genes it carries can matter differently in different environments.',
 'paragraphs':[
  "The **Plasmid Ring Vault** is lower and narrower than the chromosome gallery. On your **left**, a steel rack holds several small circular DNA molecules, each clearly separated from the main chromosome and each marked with a tiny origin symbol. Directly **ahead**, a round glass bench holds one plasmid opened at a defined site, its circular map still visible even while the ring is temporarily cut for engineering. On your **right**, a transparent transfer channel connects a donor bacterial cell to a recipient cell beside an environment display that can change from ordinary medium to antibiotic-containing medium. The blue-and-gold chromosomal duplex remains parked behind you in the gallery doorway. Sora carries only one small ring to the center bench so its identity cannot be mistaken for the chromosome you just left.",
  "She lifts the ring from the left rack. It is DNA, but it is extra-chromosomal and circular. Only after that spatial separation is obvious does she name **plasmids**: prokaryotes and eukaryotes can contain plasmids, extra-chromosomal circular DNA molecules. The vault emphasizes what defines the object here. A plasmid is not simply “small bacterial DNA,” and it is not the bacterial chromosome. Its extra-chromosomal location and circular form are visible before the word appears.",
  "A light pulses at the origin marker on the plasmid. The ring duplicates on the left rack even though the main chromosome is not being copied on this machine. Sora writes **plasmid independent replication** beside the origin symbol. Plasmids are extra-chromosomal DNA molecules with their own origins that can replicate independently of the main chromosome. The phrase *independently* does not mean the plasmid is metabolically independent of the cell; it means its DNA replication is organized from its own origin rather than simply being a segment of the chromosome’s replication program.",
  "The right-side environment panel now changes. One plasmid carries a gene that makes little visible difference in ordinary medium. When the environment switches, that gene becomes useful to the cell. Sora calls this the **conditional value of plasmid genes**. Plasmids can carry genes that provide context-dependent advantages, such as traits useful in particular environments, without being universally required for cell survival. The gene is not painted with a permanent GOOD label. Its value depends on the conditions in which the cell lives.",
  "At the center bench, Sora inserts a defined DNA segment into the open ring and closes it again. The plasmid remains a plasmid, but its sequence now contains an engineered gene of interest. She names the product **recombinant plasmid DNA**: a plasmid can be engineered to contain a gene of interest, creating recombinant plasmid DNA that can be introduced into cells for propagation or expression. This is the first time in the journey that the DNA sequence itself is deliberately altered, and the change is visible as an inserted colored segment rather than as an abstract label.",
  "Finally, the right transfer channel activates. A plasmid copy moves from one bacterial cell into another. The recipient cell now possesses plasmid-borne genetic information it did not previously carry. Sora marks this as **plasmid-mediated gene exchange**: bacteria can acquire plasmid-borne genes from other bacteria, changing the recipient genotype and potentially its phenotype. The words *potentially* and *context-dependent* remain visible on the environment panel so gene acquisition does not automatically become a guaranteed phenotypic advantage.",
  "The ring vault clears its warning. Sora returns the engineered plasmid to its rack and turns back toward the persistent chromosome. Before any DNA molecule can be copied accurately, however, the copying works must know how the nitrogenous bases are classified and what numerical relationships paired DNA produces. A door at the far end opens onto a reading table split into a two-ring drawer on the left and a one-ring drawer on the right."
 ]},
'U6-L04':{
 'title':'The Table That Separates Shape From Pairing',
 'kicker':'Purine and pyrimidine describe base structure; Chargaff’s relationships describe composition in double-stranded DNA.',
 'paragraphs':[
  "The **Base-Class Reading Table** is arranged like a quiet archive study room. On your **left**, a deep drawer is labeled TWO RINGS and contains enlarged adenine and guanine cards, each with its fused double-ring nitrogenous-base framework drawn in black. Directly **ahead**, a broad composition table displays base percentages from several double-stranded DNA samples. On your **right**, a shallow drawer labeled ONE RING contains cytosine, thymine, and uracil cards, each with a single-ring framework. The blue-and-gold DNA duplex rests along the front edge of the center table, still closed. Sora keeps the drawers separated because this room must answer two different questions: what structural class is each base, and which bases are present in matching amounts when double-stranded DNA is measured?",
  "Sora begins with structure alone. She places adenine and guanine into the left drawer and traces the two fused rings on each model. Only then does she write **purines** above them. Adenine and guanine are purines with double-ring structures. She crosses the room and places cytosine, thymine, and uracil into the right drawer. Each has a single-ring framework, so she labels them **pyrimidines**. Cytosine, thymine, and uracil are pyrimidines with single-ring structures. Nothing has paired yet. The classification depends on molecular ring structure, not on which letter a base happens to face across a DNA helix.",
  "Now the center table matters. Sora loads one double-stranded DNA sample. The screen reports that adenine is approximately matched by thymine and guanine by cytosine. A second organism has different overall percentages, yet the same within-sample relationships appear. Sora labels the pattern **Chargaff’s composition observations**: across double-stranded DNA samples, the amount of adenine approximates thymine and guanine approximates cytosine, a relationship explained by complementary base pairing. The table does not claim that every organism has the same percentage of adenine or the same GC content. It shows relationships within paired double-stranded DNA.",
  "She deliberately moves an adenine card toward a thymine card but stops before they touch. “Do not confuse the two systems,” she says. Purine versus pyrimidine classifies molecular structure. A versus T or G versus C will describe complementary pairing. Adenine is a purine and thymine is a pyrimidine, yet the fact that they pair is a separate relationship. The same is true for guanine and cytosine. The drawers stay fixed on opposite sides of the room while the composition table sits between them as evidence.",
  "Sora closes the drawers. The center table now projects the blue-and-gold duplex onto a narrow bridge beyond the reading room. The percentages can be explained only if the bases pair in a specific geometry, and that geometry depends on the direction of the sugar-phosphate backbones. The next door opens. Two floor rails run through it in opposite directions, one marked 5′→3′ and the other 3′→5′. Before the replication works can copy a strand, you must be able to walk the molecule in the same direction the polymerase will later read it."
 ]},
'U6-L05':{
 'title':'The Bridge Where the Two Strands Run Opposite Ways',
 'kicker':'Complementary base pairing only makes sense when base identity, hydrogen bonds, backbone bonds, and strand direction remain physically distinct.',
 'paragraphs':[
  "The **Antiparallel Pairing Bridge** spans a dark open shaft between the archive and the copying works. On your **left**, a metal direction rail carries explicit 5′ and 3′ labels beside a sugar-phosphate backbone model. Directly **ahead**, the blue-and-gold DNA strands cross the shaft as two parallel bridge rails, but their arrowheads point in opposite directions. On your **right**, a large comparison panel shows typical cellular DNA beside typical cellular RNA. Sora clips the copper origin tag to the center of the DNA bridge so the exact same molecule can later enter the replication machinery. Nothing else in the route will matter if the directions here become vague.",
  "She begins with the left rail, briefly reactivating chemistry you have already seen. A nucleic-acid strand has chemically distinct ends, conventionally described by a 5′ phosphate-associated end and a 3′ hydroxyl end. Sora writes **5′ and 3′ end chemistry review** beside the rail, then refuses to build a new mnemonic character for it. The chemistry is the same prerequisite. What changes in Unit 6 is what that directionality allows enzymes to do.",
  "The two center rails now light. One DNA strand runs 5′→3′ from left to right; its partner runs 5′→3′ from right to left. Sora names this **DNA antiparallel structural review**. The two DNA strands run antiparallel; each strand has a sugar-phosphate backbone, with paired bases oriented toward the helix interior. The blue and gold colors identify the original strands, and the arrowheads remain attached to them for the rest of the journey.",
  "Sora brings bases toward the middle. Adenine pairs with thymine in DNA, or with uracil when RNA is the partner; guanine pairs with cytosine. She calls the relationship **conserved complementary base pairing**: purines pair with pyrimidines, with A–T in DNA or A–U in RNA, and G–C. The purine and pyrimidine drawers from the previous room stay mentally separate from this rule. Structural class tells you how many rings the base has. Complementary pairing tells you which base fits across from it.",
  "The bridge magnifies its bonds. Solid covalent connections run continuously along each sugar-phosphate backbone. Across the gap, dotted hydrogen bonds link paired bases. A–T shows two dotted lines; G–C shows three. Sora labels the comparison **base-pair hydrogen-bond counts**. In standard Watson–Crick base pairing, A–T forms two hydrogen bonds and G–C forms three. The dotted connections do not become phosphodiester bonds, and the strong backbone bonds do not jump across the helix. The two bond systems have different positions and jobs.",
  "Finally, the right panel animates. Cellular DNA is shown in its typical double-stranded form using thymine. Cellular RNA is shown as typically single-stranded using uracil, then the RNA bends so complementary regions within the same molecule form paired secondary structure. Sora writes **typical RNA versus DNA architecture** and keeps the qualifier visible. Cellular DNA is typically double-stranded and uses thymine; cellular RNA is typically single-stranded, uses uracil, and can fold into base-paired secondary structures. Typical architecture is a pattern, not an exceptionless law for every biological genome.",
  "When the bridge locks into place, the copying works finally recognize the molecule’s geometry. The blue and gold strands remain antiparallel, their 5′/3′ arrows fixed, their complementary bases facing inward. Across the shaft, a heavy gate marked HEREDITARY CONTINUITY begins to open. On its left edge a eukaryotic cell-cycle dial has stopped at S phase. On the right, two empty daughter-DNA cradles wait. Sora slides the same tagged duplex forward. Now the question is no longer what DNA looks like. It is why the cell must copy it at all."
 ]},
'U6-L06':{
 'title':'The Gate That Opens Only for a Faithful Copy',
 'kicker':'Replication serves continuity of hereditary information, and S phase is specifically the eukaryotic cell-cycle context for nuclear DNA replication.',
 'paragraphs':[
  "Beyond the bridge stands the **Replication Continuity Gate**, a tall chamber with three unmistakable stations. On your **left**, a eukaryotic cell-cycle dial highlights S phase between the surrounding cycle stages; beside it, a separate bacterial chromosome icon sits outside that dial. Directly **ahead**, the tagged blue-and-gold DNA duplex enters a scanner labeled HEREDITARY CONTINUITY. On your **right**, two empty daughter-DNA cradles wait beyond the gate. The 5′ and 3′ arrows remain attached to the parental strands. Sora places the copper ledger beneath the scanner and leaves the page for gene expression closed. This machine has a different purpose: preserve genetic information so it can be transmitted.",
  "The left timeline lights first. In a eukaryotic cell, nuclear DNA replication occurs during S phase before cell division. Sora labels this **eukaryotic S-phase replication context**. She immediately points to the bacterial icon beside the dial. The S-phase label belongs to the eukaryotic cell-cycle framework; prokaryotic chromosome replication is not organized into a eukaryotic S phase. The distinction prevents a useful eukaryotic timing cue from being turned into a universal description of all DNA replication.",
  "At center, the gate reads the tagged duplex and projects its sequence toward the two empty cradles. If the sequence cannot be copied, a daughter cell or later organismal generation cannot receive an equivalent set of hereditary information. Sora names the core relationship **replication preserves hereditary continuity**. DNA replication copies genetic information so it can be transmitted between cell and organismal generations. The gate therefore treats replication as an information-preservation process, not as the process by which a gene is expressed into RNA or protein. The molecule’s role here is duplication for continuity: its sequence must be reproduced before the genetic record can be distributed onward.",
  "The scanner briefly separates the blue and gold strands without allowing new DNA to appear. Each parental strand exposes a sequence that could direct a complementary partner. Sora keeps the word *template* on the display. The future copy will be built by complementary synthesis on each parental strand. This is the causal idea needed for the next rooms: the old strands are not merely duplicated as whole objects by a photocopier; their sequences guide construction of new complementary strands.",
  "The continuity gate remains locked because it still does not know how parental and newly synthesized DNA should be distributed in the products. Three model symbols appear over the door: one keeps the entire parental duplex together, one places old and new segments in mixed patches, and one separates the two parental strands so each can guide a new partner. Sora moves the tagged duplex into a test chamber where those three predictions can be compared against actual evidence. The question now is not whether DNA is copied. It is which replication model matches what real DNA does."
 ]},
'U6-L07':{
 'title':'Three Replication Models Enter the Test Chamber',
 'kicker':'The correct replication model must survive evidence across generations, not merely look plausible on paper.',
 'paragraphs':[
  "The **Replication Model Test Chamber** has the shape of a triangular courtroom. On your **left**, two transparent panels display competing predictions. The upper panel keeps the entire parental blue-and-gold duplex intact and builds a second duplex entirely from new material. The lower panel produces daughter strands that are patchworks of old and new segments. Directly **ahead**, the center bench separates the original blue and gold strands and gives each one a newly synthesized complementary partner. On your **right**, a tall density-gradient display is labeled ¹⁵N at the bottom and ¹⁴N at the top. Sora lays the copper ledger between the models and the data. The chamber will accept only the model whose predicted DNA distribution matches the evidence.",
  "She starts with the upper-left panel. In the **conservative replication model**, the rejected prediction is that the parental double helix remains together while a wholly new double helix is synthesized. The blue-and-gold parental duplex stays intact as one product; the other product contains two new strands. The model is easy to picture, which is exactly why Sora insists that plausibility is not enough.",
  "The lower-left panel shows the **dispersive replication model**. Here the predicted daughter DNA strands contain interspersed segments of parental and newly synthesized DNA. Blue or gold parental material is chopped conceptually into segments and mixed through each daughter strand. Sora keeps this panel physically separated from the center so “pieces of old DNA mixed with new DNA” cannot be mistaken for “one intact old strand paired with one new strand.”",
  "At center, Sora opens the tracked duplex. The blue parental strand remains intact and receives one new complementary strand. The gold parental strand does the same. Only now does she name **semiconservative replication**: each parental strand serves as a template for a complementary new strand, so each daughter DNA duplex contains one parental strand and one new strand. The parental duplex as a whole is not conserved, but each daughter conserves one of its two parental strands.",
  "The right-side evidence display begins the **Meselson–Stahl experiment**. Bacterial cells first contain DNA labeled with heavy ¹⁵N. They are then moved to ¹⁴N medium, and DNA density is analyzed across generations. After one round of replication, the DNA appears at an intermediate density. That observation rejects the conservative model’s prediction of separate heavy parental and light new duplex populations after the first generation. The dispersive and semiconservative models can both still produce intermediate-density DNA at that point, so the chamber advances to another generation.",
  "After the second round, the display separates into a lighter DNA population and an intermediate population. The semiconservative model predicts exactly this: some daughter duplexes contain one original heavy strand paired with a light strand, while others contain two light strands descended from templates made in the first generation. A purely dispersive model instead predicts DNA molecules that remain mixed within strands and shift progressively in density. The observed generational pattern therefore supports semiconservative replication. Sora writes **Meselson–Stahl experiment** beside the density column: density labeling with ¹⁵N and ¹⁴N in bacteria, followed across generations, distinguishes the models and supports semiconservative replication.",
  "The left panels go dark. The center model remains lit, with one parental strand in each daughter duplex. The continuity gate behind you finally unlocks, but a new mechanical problem appears immediately. A chromosome cannot copy itself everywhere at once without a place to begin and a region where the strands are actively opening. The copper origin tag on the blue-and-gold duplex starts flashing. Ahead, a circular mark on the DNA expands into a bubble with two Y-shaped edges. Sora follows it onto the fork-launch deck."
 ]},
'U6-L08':{
 'title':'The Origin Opens and the Forks Begin to Move',
 'kicker':'Origin, replication fork, helicase, and topoisomerase occupy different positions because they perform different jobs.',
 'paragraphs':[
  "The floor drops into the **Origin and Fork Launch** deck, where the tracked duplex is stretched horizontally across three work zones. On your **left**, the copper origin tag sits on intact DNA beside a swivel-like topoisomerase model positioned farther ahead where twisting strain can build. Directly **ahead**, a replication bubble opens around the tagged origin, creating two Y-shaped boundaries. On your **right**, a helicase complex sits directly at one Y-shaped boundary, where the parental strands are being separated and exposed as templates. Sora keeps the origin marker fixed even as the forks begin moving away from it. That single choice prevents four closely related ideas from collapsing into one flashing “replication starts here” image.",
  "Sora points to the copper tag. **Origins of replication** are positions where chromosomal DNA replication begins; opening at an origin produces replication forks where parental DNA is exposed and copied. The origin is a starting region, not the moving Y-shaped structure itself. As the bubble expands, the two edges travel away from the starting point while the origin remains where it was on the chromosome.",
  "At the right edge of the bubble, Sora zooms in on the Y shape and names the **replication fork**. A replication fork is the Y-shaped region where parental DNA strands are separated and new complementary strands are synthesized. The fork is a region of active replication, not an enzyme. The helicase protein is one actor located at that region.",
  "The helicase complex begins moving with the fork. It disrupts the interactions holding the paired parental strands together so the templates can separate. Sora names **helicase** only after the two blue-and-gold strands visibly part. Helicase unwinds the DNA strands at replication forks. The enzyme’s job is therefore physically located at the fork, where the double-stranded DNA becomes two exposed templates.",
  "But opening one region creates strain elsewhere. Ahead of the moving fork, the still-double-stranded DNA twists more tightly. On the left-side comparison, the swivel-like enzyme acts before that strain can accumulate excessively. Sora names **topoisomerase**. Topoisomerase relaxes supercoiling ahead of the replication fork. She freezes helicase and topoisomerase at the same moment: helicase at the Y-shaped opening, topoisomerase ahead of it on still-double-stranded DNA. Their positions make their different jobs visible.",
  "The fork is now open, but the exposed strands are not yet being copied. The blue and gold templates flex apart, and the polymerase dock ahead remains inactive. A display beside it reads NO FREE 3′ STARTING END. Sora follows the exposed DNA to the next station. There, single-strand support proteins hold the templates apart, a primase model waits beside a tray of RNA nucleotides, and DNA polymerase is locked behind a gate that will not open until a primer appears."
 ]},
'U6-L09':{
 'title':'The Polymerase Dock Has No Place to Start',
 'kicker':'DNA polymerase can extend DNA only from an existing primer 3′ end, so primase and synthesis direction must be visible together.',
 'paragraphs':[
  "The **Primer–Polymerase Dock** sits immediately beside the moving fork. On your **left**, the exposed single-stranded templates are held apart by small stabilizing proteins while a primase model faces a tray of RNA nucleotides. Directly **ahead**, a large DNA polymerase model is aligned with the template but cannot yet move because the starting junction is empty. On your **right**, two illuminated arrows run in opposite directions: TEMPLATE 3′→5′ and NEW DNA 5′→3′. The original blue and gold strands remain color-coded from the pairing bridge, so the direction rail refers to real strands rather than floating arrows.",
  "The first problem is physical stability. Once helicase separates the strands, **single-strand binding proteins** can bind the exposed templates and help keep them separated. Sora keeps these proteins small and contextual. Their role is support after the helix opens; they are not the central directional enzyme that synthesizes new DNA.",
  "Primase now moves to the exposed template and synthesizes a short RNA segment. Sora names **primase** after the RNA piece appears. Primase synthesizes short RNA primers that provide a 3′ end from which DNA polymerase can extend. The RNA segment is visibly different from the DNA that will follow, and the free 3′ end is highlighted at its terminus.",
  "Only then does the center gate release DNA polymerase. The enzyme docks at the primer-template junction and begins adding DNA nucleotides to the free 3′ end. Sora writes **DNA polymerase requires RNA primers**: DNA polymerase requires an RNA primer with an available 3′ end to initiate new DNA synthesis. The wording is deliberately mechanistic. The primer does not “tell polymerase where the gene is”; it provides the chemical starting end that DNA polymerase needs for extension.",
  "As polymerase moves, the right-side arrows illuminate. New DNA grows by nucleotide addition at its 3′ end, so the new strand extends **5′→3′**. To accomplish that, polymerase progresses along the antiparallel template in the **3′→5′ direction**. Sora labels this relationship **DNA polymerase movement on template**. Because new DNA grows 5′→3′, DNA polymerase progresses along the template 3′→5′. The two arrows are linked: polymerase movement and product growth are opposite directional descriptions of the same local process. Sora traces one template nucleotide at a time so the direction is anchored to a real polymerase-template junction rather than memorized as two unrelated arrow rules.",
  "The polymerase dock begins copying both parental templates, but the fork geometry immediately produces a contradiction. On one template, synthesis can follow the opening fork continuously. On the other, the requirement for 5′→3′ synthesis points away from the fork, forcing repeated starts instead of one uninterrupted run. Sora rolls the entire fork assembly onto a split track. The next room is designed so both strands obey the same chemistry even though they cannot be synthesized in the same pattern."
 ]},
'U6-L10':{
 'title':'The Fork Splits Into a Smooth Track and a Fragment Track',
 'kicker':'Both daughter strands are synthesized 5′→3′, yet antiparallel templates force continuous leading synthesis and discontinuous lagging synthesis.',
 'paragraphs':[
  "The **Leading–Lagging Split Track** opens like a rail junction around the same replication fork. On your **left**, one track runs smoothly beside the advancing fork, with DNA polymerase moving continuously as new DNA lengthens. Directly **ahead**, a large direction board displays 5′→3′ for *both* new strands. On your **right**, the second track is broken into repeated work sections. New primers appear near the fork, and short DNA pieces extend away from it before another primer must be started closer to the newly opened region. The blue and gold parental templates remain visible under both tracks, preserving the antiparallel geometry that created the difference.",
  "Sora begins at the center divider because the rule is common to both branches. **DNA synthesis direction** is 5′→3′: new DNA is synthesized in the 5′→3′ direction. No branch is allowed to reverse this chemistry merely to make the fork diagram look symmetrical. The central sign remains fixed while the two tracks solve the directional problem differently.",
  "On the left, the template orientation allows DNA polymerase to synthesize in the same overall direction that the fork is opening. The new strand can therefore grow continuously. On the right, the template orientation makes 5′→3′ synthesis proceed away from the fork. New template DNA becomes exposed as the fork opens, so synthesis must restart repeatedly from new primers. Sora labels the complete comparison **leading and lagging strand synthesis**. DNA polymerase synthesizes the leading strand continuously and the lagging strand discontinuously because both new strands must be synthesized 5′→3′ on antiparallel templates.",
  "The terms attach to patterns, not to arbitrary left and right positions. The **leading strand** is the continuously synthesized new strand in this fork geometry. The **lagging strand** is the discontinuously synthesized new strand. If the diagram were rotated, the names would follow the synthesis pattern and template orientation, not the page side. Sora turns the compass tablet ninety degrees to prove it; the chemical arrows remain correct even though the visual left-right orientation changes.",
  "On the lagging track, each short DNA section is allowed to finish. Sora highlights the separate pieces and names **Okazaki fragments**: short DNA segments synthesized discontinuously on the lagging strand before being joined into a continuous strand. The name identifies these short pieces, while the crucial mechanism remains the discontinuous fragment pattern and the later need to join those fragments. Each piece is DNA, and each was itself synthesized 5′→3′.",
  "The fork advances. The leading track produces a continuous daughter strand, but the right track leaves a row of fragments separated by primer-associated interruptions. The copier cannot certify the daughter DNA in that state. A repair light turns red over the next bench. Sora sends the unfinished lagging strand forward while the continuous leading strand runs beside it as a comparison. The next task is to replace temporary primer material, seal the remaining breaks, and catch sequence errors before the copy leaves the replication works."
 ]},
'U6-L11':{
 'title':'The Copy Cannot Leave With Gaps or Unchecked Errors',
 'kicker':'Post-synthesis processing turns discontinuous lagging-strand pieces into a continuous DNA backbone and protects sequence accuracy.',
 'paragraphs':[
  "The unfinished daughter DNA reaches the **Fragment Joining and Repair Bench**. On your **left**, RNA-primer positions are marked along the lagging strand beside a proofreading window that enlarges the newest nucleotide pair. Directly **ahead**, the separated DNA fragments are aligned end to end across a bench marked LIGASE. On your **right**, a broad repair panel displays a mismatched or damaged DNA segment being identified, removed, and restored using intact sequence information. The continuous leading strand runs along the back wall as a completed comparison. Sora keeps the central question simple: how does the cell turn the fragmented copy into continuous, more accurate DNA without turning this room into a memorization list of every repair enzyme?",
  "She begins on the left with **primer replacement detail**. The temporary RNA-primer material cannot simply remain as the final DNA sequence in the textbook bacterial replication model. RNA primer nucleotides are removed and replaced with DNA before the remaining backbone interruptions are sealed. Sora deliberately keeps the extra enzyme identities off the wall. The mechanism matters here; named proteins beyond the required set are not needed to understand why a temporary primer must be replaced before the strand becomes continuous DNA.",
  "At center, the fragments now consist of DNA but still contain breaks in the sugar-phosphate backbone between adjacent sections. A ligase model closes those remaining nicks. Sora names the core relationship **ligase joins lagging-strand fragments**: DNA ligase joins DNA fragments on the lagging strand into a continuous strand. She briefly overlays the earlier fork scene. Helicase separated parental strands at the fork; topoisomerase relieved twisting ahead of the fork; ligase acts later on the newly synthesized lagging strand. Their different locations prevent the three enzyme names from becoming interchangeable “replication helpers.”",
  "The left proofreading window catches a mispaired newly added nucleotide. Sora labels **DNA polymerase proofreading**: many DNA polymerases proofread newly added nucleotides, reducing replication errors. The phrase *many DNA polymerases* stays on the display. Proofreading is an accuracy mechanism associated with polymerase activity, but it does not make replication error-free.",
  "On the right, the repair panel demonstrates a broader second line of protection. A mismatched or damaged section is recognized, erroneous or damaged nucleotides are removed, and intact sequence information guides restoration. Sora labels this **mismatch and excision repair overview**. DNA repair systems can recognize damaged or mismatched DNA, remove erroneous or damaged nucleotides, and use intact sequence information to restore DNA. The panel deliberately avoids exploding into a dozen named pathways. What you need to see is the logic of recognition, removal, and restoration.",
  "The red repair light turns green. The lagging strand is now continuous, and both daughter DNA products can be traced back to the semiconservative model: one parental strand paired with one newly synthesized strand. But the right-side quality scanner stops at the physical end of a linear chromosome. There is no DNA beyond that end to continue into. Sora closes the repair ledger and rolls the copied chromosome to the final dock, where repetitive end DNA and an RNA-containing enzyme are kept on opposite sides of the room so their names cannot be confused."
 ]},
'U6-L12':{
 'title':'The Final Dock Separates the Chromosome End From the Enzyme That Extends It',
 'kicker':'Telomeres are chromosome-end DNA and associated structures; telomerase is an enzyme that can extend telomeric DNA in cells where it is active.',
 'paragraphs':[
  "The journey ends at the **Chromosome-End Dock**, a quiet bay built around the end of a linear chromosome. On your **left**, the chromosome terminates in a visibly repetitive stretch of telomeric DNA, shown as repeated sequence blocks with associated protective structure. Directly **ahead**, the fully copied chromosome lies in a center maintenance cradle, its internal genes safely separated from the physical end. On your **right**, a distinct protein-RNA complex is parked in its own tool station. Its label is covered for the moment. Sora places the blue-and-gold daughter DNA records beside the dock and points to the spatial separation: the end region is part of the chromosome; the tool that can extend it is a different biological entity.",
  "She begins on the left. The repeated DNA sequence and associated end structure are **telomeres**. Telomeres are repetitive DNA sequences and associated structures at chromosome ends that buffer loss of coding sequence and help maintain chromosome-end integrity. Sora keeps the repeats physically attached to the chromosome model. A telomere is not an enzyme, not a free-floating cap, and not a signal that all chromosome DNA is repetitive. It is a specialized chromosome-end region.",
  "Only after the end region is fixed does Sora uncover the right-side complex. **Telomerase** is an enzyme capable of extending telomeric DNA in cells where it is active. More specifically, telomerase can extend telomeric DNA using an RNA-containing reverse-transcriptase mechanism. The tool station shows both components: an internal RNA template and reverse-transcriptase activity. Sora moves the enzyme toward the chromosome end, but she never swaps their identities. Telomere stays on the chromosome; telomerase is the enzyme that can act on telomeric DNA.",
  "The maintenance cradle deliberately avoids turning the room into a full molecular derivation of the end-replication problem. What matters for this journey is the diagnostic distinction and its biological consequence. Linear chromosome ends require specialized maintenance logic, and telomerase provides a mechanism for extending telomeric repeats in cell types where the enzyme is active. The presence and activity of telomerase vary among cell types and biological contexts; the right-side tool is therefore shown as available in some cells, not permanently active in every cell.",
  "Sora now opens the copper ledger to its first page and walks backward through the route without moving the objects. Hereditary information entered as a real nucleic-acid molecule. Chromosome forms established how DNA can be stored. Plasmids were separated from main chromosomes. Purines and pyrimidines were classified before complementary pairing rebuilt the antiparallel duplex. Replication was tied to hereditary continuity, the semiconservative model survived density evidence, origins launched forks, helicase and topoisomerase took distinct positions, primase supplied a starting 3′ end, DNA polymerase extended 5′→3′, the fork split into leading and lagging synthesis, ligase and repair systems finished the copy, and chromosome ends remained a distinct maintenance problem.",
  "The final display shows two semiconservative daughter DNA molecules. The original blue parental strand is paired with a new strand in one daughter; the original gold parental strand is paired with a new strand in the other. Their direction arrows still point correctly, and the copper origin tag can be traced back to the place where the fork first opened. The copying works certify both molecules. Sora closes the ledger, but she does not file the DNA away. A new conveyor beyond the dock leads toward an RNA workshop. The next Unit 6 problem will no longer be how hereditary DNA is copied. It will be how selected information in that DNA is transcribed into RNA."
 ]},
}

# Beat imagery tied to conventional biological scene objects, not whimsical substitutes.
BEAT_IMAGES={
'U6-K-001':'the center registry filing both the tagged DNA duplex and an RNA record under hereditary information',
'U6-K-090':'the left diffraction panel constraining the shape and dimensions of the DNA model',
'U6-K-093':'the right model case integrating diffraction and base-composition constraints into a double helix',
'U6-K-002':'the large circular chromosome in the left storage bay',
'U6-K-003':'the multiple linear chromosome models in the right storage bay',
'U6-K-004':'the right-side linear eukaryotic DNA compacting with histones and associated proteins',
'U6-K-005':'the small extra-chromosomal circular DNA ring kept separate from the main chromosome',
'U6-K-096':'the plasmid origin flashing as the ring replicates independently of the main chromosome',
'U6-K-097':'the environment panel changing whether a plasmid-carried gene provides an advantage',
'U6-K-098':'the center plasmid ring receiving a defined inserted DNA segment and closing again',
'U6-K-099':'the right transfer channel moving plasmid-borne DNA into a recipient bacterium',
'U6-K-006':'the left drawer containing adenine and guanine as two-ring bases',
'U6-K-007':'the right drawer containing cytosine, thymine, and uracil as single-ring bases',
'U6-K-091':'the center dsDNA composition table showing A approximately T and G approximately C within samples',
'U6-K-008':'complementary bases pairing across the center antiparallel bridge',
'U6-K-092':'two dotted hydrogen bonds across A–T and three across G–C',
'U6-K-094':'the blue and gold DNA backbones running in opposite 5′→3′ directions across the bridge',
'U6-K-095':'the left rail marking a 5′ phosphate-associated end and a 3′ hydroxyl end',
'U6-K-100':'the right panel showing typical cellular double-stranded DNA beside typically single-stranded, foldable RNA',
'U6-K-009':'the continuity gate requiring copied DNA before hereditary information can move to daughter destinations',
'U6-K-101':'the left eukaryotic cell-cycle dial highlighting S phase while the bacterial icon remains outside that framework',
'U6-K-011':'each intact parental strand ending in a daughter duplex paired with one new complementary strand',
'U6-K-102':'the upper-left model keeping the whole parental duplex together and building a wholly new duplex',
'U6-K-103':'the lower-left model mixing parental and new segments within daughter strands',
'U6-K-104':'the 15N/14N density-gradient display across successive bacterial generations',
'U6-K-012':'helicase sitting at the Y-shaped fork where the parental strands separate',
'U6-K-013':'topoisomerase acting ahead of the fork on overwound double-stranded DNA',
'U6-K-105':'the copper-tagged origin remaining fixed while a replication bubble opens around it',
'U6-K-106':'the Y-shaped replication fork moving away from the origin',
'U6-K-014':'DNA polymerase remaining locked until an RNA primer exposes a free 3′ end',
'U6-K-107':'small proteins stabilizing the exposed single-stranded DNA templates',
'U6-K-108':'primase synthesizing a short RNA primer on exposed template DNA',
'U6-K-109':'DNA polymerase moving 3′→5′ along template while new DNA grows 5′→3′',
'U6-K-010':'the central 5′→3′ sign applying to both newly synthesized strands',
'U6-K-015':'the left continuous leading track beside the right discontinuous lagging track',
'U6-K-110':'short DNA pieces accumulating on the lagging track before joining',
'U6-K-016':'ligase sealing remaining backbone nicks between lagging-strand DNA fragments',
'U6-K-111':'temporary RNA-primer positions being replaced with DNA before final sealing',
'U6-K-114':'the proofreading window catching an incorrect newly added nucleotide',
'U6-K-115':'the repair panel recognizing, removing, and restoring mismatched or damaged DNA',
'U6-K-112':'the repetitive chromosome-end DNA and associated protective structure fixed on the left',
'U6-K-113':'the distinct RNA-containing reverse-transcriptase enzyme acting at telomeric DNA',
}

# The exact F3 candidate recalls remain unchanged.
CHECKPOINTS={lid for lid,b in B.items() if b['quick_recall']['enabled']}

def word_count(paragraphs): return len(re.findall(r"\b[\w’′'-]+\b",' '.join(paragraphs)))

def zone_objs(lid):
    return [{'position':p,'label':label,'symbol':sym,'description':desc} for p,label,sym,desc in ZONES[lid]]

def cast_for(lid):
    items=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    for p,label,sym,desc in ZONES[lid]:
        items.append({'name':label,'kind':'scientific structure, process, evidence display, or comparison','visual':desc,'job':next(x['job_in_scene'] for x in B[lid]['stable_cast'] if x['position']==p)})
    items.append({'name':'Persistent blue-and-gold DNA duplex','kind':'journey continuity object','visual':'the same blue-and-gold DNA molecule with permanent 5′/3′ arrowheads and a copper origin tag carried from the archive entrance through the replication works','job':'keeps original strand identity, directionality, and replication origin traceable across the entire journey; it never substitutes for a biological term'})
    return items

def beats_for(lid):
    out=[]
    terms={t['knowledge_id']:t for t in B[lid]['term_introductions']}
    for kid in B[lid]['knowledge_ids']:
        t=terms[kid]; c=CANON[kid]
        out.append({
          'object_id':kid,'term':t['canonical_term'],'story':BEAT_IMAGES[kid],
          'science':c['canonical_verified_statement'],'exact_name':bool(t['exact_name_recall']),
          'hint':BEAT_IMAGES[kid],'name_support':t['name_support'],
          'reactivation_mode':t['reactivation_mode'],'scope_class':t['scope_class']
        })
    return out

scenes=[]
for i,lid in enumerate(J1['route']):
    b=B[lid]; n=NARR[lid]; route=ROUTE[i]
    paragraphs=n['paragraphs']
    cp=lid in CHECKPOINTS
    scenes.append({
      'scene_index':i,'locus_id':lid,'locus':route['locus'],'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['micro_anchor'],
      'scene_layout':{'orientation':b['orientation_sentence'],'zones':zone_objs(lid)},
      'cast':cast_for(lid),'continuity_object':J1['continuity_object'],
      'story_open':paragraphs[0],'story_paragraphs':paragraphs,'story_close':paragraphs[-1],
      'object_ids':list(b['knowledge_ids']),'story_beats':beats_for(lid),
      'prior_unit_reactivation':b['prior_unit_reactivation'],
      'misconception_guards':b['misconception_guards'],
      'checkpoint':cp,
      'checkpoint_object_id':b['primary_knowledge_id'] if cp else None,
      'checkpoint_prompt':b['quick_recall']['candidate_prompt'] if cp else '',
      'checkpoint_answer':b['quick_recall']['answer'] if cp else '',
      'next_locus':ROUTE[i+1]['locus'] if i+1<len(ROUTE) else None,
      'f3_scene_brief_id':b['scene_brief_id'],
      'narrative_word_count':word_count(paragraphs),
    })

journey={
 'palace_id':'U6-J1','unit_id':'unit-6','palace_name':'Genome Archive and Replication Works',
 'story_title':'The Archive That Could Not Make a Copy',
 'tagline':'One tagged DNA molecule has been cleared as hereditary information, but the replication works will not certify a copy until its chromosome form, base geometry, replication model, directional machinery, repair, and chromosome ends all agree.',
 'guide':GUIDE,
 'premise':'The Genome Archive has received a blue-and-gold DNA molecule for long-term hereditary storage, yet the attached replication works refuse to copy it. The archive records disagree about chromosome form, extra-chromosomal plasmids are mixed with the main chromosome, base classes are being confused with pairing partners, and the copying machinery has lost the strand directions that determine how replication can proceed. Dr. Sora Han must carry the same tagged duplex through the archive and replication works, resolving each physical inconsistency before the next machine can activate.',
 'mission':'Follow Dr. Sora Han through twelve connected locations. Keep the same parental DNA strands, 5′/3′ arrows, and copper origin tag visible from the hereditary-information registry through semiconservative replication, fork opening, primer-dependent synthesis, leading/lagging geometry, fragment joining, repair, and chromosome-end maintenance.',
 'finale':'The archive certifies two semiconservative daughter DNA molecules only after every step remains physically consistent with the original molecule. One parental strand persists in each daughter duplex, all new DNA was synthesized 5′→3′, the lagging strand was completed and repaired, and telomeres remain chromosome-end DNA distinct from telomerase. The same DNA information can now leave the copying works and enter the later RNA-expression route without losing its molecular history.',
 'estimated_minutes':34,'scene_count':12,'checkpoint_count':len(CHECKPOINTS),
 'student_release':'DEVELOPER_PREVIEW_F4A','preview_release':True,'narrative_design':'U6-F4A-NARRATIVE-1.0',
 'learner_rule':'Read or listen and place yourself in the room before following the biological action. The same DNA molecule persists across all twelve locations. Exact terms are attached to structures and mechanisms after their defining feature is visible. Optional Quick Recall appears only three times.',
 'route_orientation':'This is one continuous twelve-location route through the Genome Archive and Replication Works. Enter at Hereditary Information Intake, move through chromosome and plasmid storage, cross the base-class table and antiparallel bridge, pass the hereditary-continuity and replication-model gates, then follow the tagged origin through the fork, primer dock, leading/lagging split, repair bench, and final chromosome-end dock. The same blue-and-gold parental strands, 5′/3′ arrowheads, and copper origin tag remain reconstructable throughout.',
 'route':ROUTE,'scenes':scenes,
 'source_brief_lock':'LOCKED_F3','scientific_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2',
}

(U6/'journeys').mkdir(exist_ok=True)
(U6/'journeys'/'U6-J1.json').write_text(json.dumps(journey,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary={
 'schema':'memory-palace-v2-unit6-f4a-journeys-1.0','unit_id':'unit-6','stage':'F4A','student_release':False,'preview_release':True,
 'journey_count':1,'scene_count':12,'checkpoint_count':len(CHECKPOINTS),
 'guided_journeys':[ {k:journey[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']} ]
}
(U6/'journeys-f4a.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Developer-preview status only; no Unit 6 final runtime artifacts are created.
status={
 'unit_id':'unit-6','number':6,'title':'Gene Expression and Regulation','status':'F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','pipeline_stage':'F4A_JOURNEY1_NARRATIVE',
 'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','narrative_lock':'LOCKED_F4A_J1',
 'student_release':False,'preview_release':True,'journey_count':1,'scene_count':12,'memory_objects':0,'application_challenges':0,
 'canonical_records':202,'architecture_journeys':6,'architecture_loci':53,'scene_briefs':53,'palace_managed_records':161,
 'challenge_lab_records':16,'scope_guard_records':25,'exact_name_review_targets':134,'confusable_sets':37,'optional_first_exposure_recalls':18,
 'f4a_journey':'U6-J1','f4a_scene_count':12,'f4a_knowledge_records':42,'f4a_optional_recalls':len(CHECKPOINTS),
 'next_required_output':'F4B polished narrative for Journey 2 only after Journey 1 remains frozen and the F4A prose-quality gate continues to pass.'
}
(U6/'status-f4a.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(U6/'status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Update course registry to expose a preview, not student release.
cp=ROOT/'content'/'ap-biology'/'course.json'
course=json.loads(cp.read_text(encoding='utf-8'))
u=next(x for x in course['units'] if x['unit_id']=='unit-6')
u.update({
 'status':'F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','journey_count':1,'scene_count':12,'student_release':False,'preview_release':True,
 'source_status':'AUDITED_F1_ARCHITECTURE_F2_BRIEFS_F3_NARRATIVE_F4A','narrative_lock':'LOCKED_F4A_J1','narrative_journeys':1,
})
cp.write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Reviewer-facing story document.
doc=['# Unit 6 F4A · Journey 1 Narrative','','## The Archive That Could Not Make a Copy','',journey['tagline'],'',
     '### Route','', ' → '.join(x['locus'] for x in ROUTE),'']
for s in scenes:
    doc += [f"## {s['scene_index']+1}. {s['locus']} · {s['title']}",'',f"*{s['scene_kicker']}*",'']
    doc += s['story_paragraphs']+['']
    if s['checkpoint']:
        doc += ['**Optional Quick Recall**','',s['checkpoint_prompt'],'']
(ROOT/'docs'/'UNIT6_F4A_JOURNEY1_STORY.md').write_text('\n'.join(doc),encoding='utf-8')

# Release manifest and lock.
def sha(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()
locked_rel=['journeys/U6-J1.json','journeys-f4a.json','status-f4a.json']
lock_files={rel:{'bytes':(U6/rel).stat().st_size,'sha256':sha(U6/rel)} for rel in locked_rel}
lock={
 'schema':'memory-palace-v2-unit6-f4a-lock-1.0','unit_id':'unit-6','lock_status':'LOCKED_F4A_J1','student_release':False,'preview_release':True,
 'protected_prior_locks':['content-lock-f1.json','content-lock-f2.json','content-lock-f3.json'],
 'journey_id':'U6-J1','scene_count':12,'knowledge_record_count':42,'checkpoint_count':len(CHECKPOINTS),'files':lock_files,
 'rule':'Journey 1 polished prose may not change after F4A without a new explicit narrative version. F1 science, F2 classification/geometry, and F3 briefs remain authoritative boundaries.'
}
(U6/'content-lock-f4a.json').write_text(json.dumps(lock,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
release={
 'schema':'memory-palace-v2-unit6-f4a-release-1.0','generated_utc':'2026-09-08T00:30:00+00:00','unit_id':'unit-6',
 'release_status':'F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','student_release':False,'preview_release':True,'journey_id':'U6-J1',
 'journeys':1,'scenes':12,'knowledge_records':42,'optional_first_exposure_recalls':len(CHECKPOINTS),
 'canonical_records':202,'permanent_loci_architecture':53,'scene_briefs':53,'memory_objects':0,'application_challenges':0,
 'scientific_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','narrative_lock':'LOCKED_F4A_J1',
 'next_stage':'F4B Journey 2 polished narrative after F4A regression'
}
(U6/'f4a-release-manifest.json').write_text(json.dumps(release,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

print(json.dumps({'journey':'U6-J1','scenes':12,'knowledge_records':42,'checkpoints':len(CHECKPOINTS),'words':sum(s['narrative_word_count'] for s in scenes),'min_words':min(s['narrative_word_count'] for s in scenes)},indent=2))
