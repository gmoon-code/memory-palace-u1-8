from __future__ import annotations
import json,re,hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content'/'ap-biology'/'unit-7'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()

CANON={r['knowledge_id']:r for r in read(U7/'source/canonical-unit7-f1.json')['canonical_catalog']}
F3=read(U7/'briefs/scene-briefs-f3.json')
B={b['locus_id']:b for b in F3['scene_briefs'] if b['journey_id']=='U7-J4'}
JB=read(U7/'briefs/journey-briefs-f3.json')
J4=next(j for j in JB['journeys'] if j['journey_id']=='U7-J4')
J1=read(U7/'journeys/U7-J1.json')
J2=read(U7/'journeys/U7-J2.json')
J3=read(U7/'journeys/U7-J3.json')

GUIDE={
 'name':'Dr. Imani Vale',
 'role':'evolutionary-systems curator',
 'visual':'charcoal field jacket, pale-green specimen gloves, a slim brass pointer, and a transparent six-taxon navigation dossier clipped beneath her left arm',
 'story_job':'keeps taxon identities, node IDs, character states, sequence strips, and evidence sources fixed while allowing branch orientation and candidate hypotheses to change only when the evidence justifies it'
}
CONTINUITY=J4['continuity_object']

ROUTE=[
 {'scene_index':0,'locus':'Phylogeny Hypothesis Desk','short':'Hypothesis','floor':'Archive intake','symbol':'HYP'},
 {'scene_index':1,'locus':'Tree–Cladogram Scale Gallery','short':'Scale','floor':'Scale gallery','symbol':'SCALE'},
 {'scene_index':2,'locus':'Tree Anatomy Board','short':'Anatomy','floor':'Tree board','symbol':'N0–N4'},
 {'scene_index':3,'locus':'Sister and Early-Branching Fork','short':'Relationships','floor':'Branch fork','symbol':'SISTER'},
 {'scene_index':4,'locus':'Character Mapping Wall','short':'Characters','floor':'Character wall','symbol':'STATE'},
 {'scene_index':5,'locus':'Outgroup Reference Gate','short':'Outgroup','floor':'Reference gate','symbol':'OUT'},
 {'scene_index':6,'locus':'Phylogeny Evidence Construction Lab','short':'Evidence','floor':'Construction lab','symbol':'BUILD'},
 {'scene_index':7,'locus':'Grouping and Parsimony Wing','short':'Grouping','floor':'Final wing','symbol':'CLADE'},
]

TAXA=[
 {'name':'Lancelet','badge':'silver lance-shaped chordate badge','role':'fixed outside reference lineage used as the outgroup when the vertebrate ingroup is analyzed'},
 {'name':'Shark','badge':'blue triangular fin badge','role':'fixed vertebrate lineage that branches earlier than the sampled tetrapod lineages'},
 {'name':'Salamander','badge':'green four-footed badge','role':'fixed tetrapod lineage branching before the sampled amniote lineages'},
 {'name':'Mouse','badge':'gray round-eared badge','role':'fixed sampled mammalian lineage'},
 {'name':'Lizard','badge':'rust scaled-tail badge','role':'fixed sampled sauropsid lineage and sister sampled lineage to pigeon on node N4'},
 {'name':'Pigeon','badge':'white feather badge','role':'fixed sampled sauropsid lineage and sister sampled lineage to lizard on node N4'},
]

NODE_MAP={
 'N0':'root node for all six sampled taxa; one branch leads to Lancelet and the other to N1',
 'N1':'vertebrate ingroup ancestor; one branch leads to Shark and the other to N2',
 'N2':'sampled tetrapod ancestor; one branch leads to Salamander and the other to N3',
 'N3':'sampled amniote ancestor; one branch leads to Mouse and the other to N4',
 'N4':'immediate common-ancestor node of the sampled Lizard and Pigeon lineages',
}

ZONES={
'U7-L34':[
 ('left','Taxonomy and systematics catalog','NAME / CLASSIFY / RELATE','A brass card catalog keeps organism names, classifications, and broader relationship records on separate drawers so naming is never confused with the methods used to infer ancestry.'),
 ('center','Phylogeny-hypothesis desk','TREE H1','A glass desk projects one rooted six-taxon branching hypothesis whose internal nodes are permanently labeled N0 through N4.'),
 ('right','Phylogenetics and revision evidence board','TEST / REVISE','An evidence wall accepts character matrices, fossils, DNA, and protein strips and can revise the candidate tree without erasing the taxon identities or node labels.')],
'U7-L35':[
 ('left','Unscaled cladogram','ORDER ONLY','A white branching diagram preserves branching order while every branch has arbitrary visual length.'),
 ('center','Tree-versus-cladogram comparison rail','WHAT IS ENCODED','A rotating rail holds two representations by the same node IDs so branch orientation can change without changing ancestry.'),
 ('right','Time or change scaled phylogenetic tree','SCALE SHOWN','A second tree carries an explicit time or evolutionary-change scale and keeps its scale marks physically attached to the branches.')],
'U7-L36':[
 ('left','Root and early-branch side','N0 → N1','The root N0 sits on the far left and leads into the earlier internal nodes while all six extant taxon badges remain on the same present-time boundary.'),
 ('center','Node-and-clade board','N0 N1 N2 N3 N4','Five illuminated internal nodes stay labeled while tracing lights can follow every descendant branch from a selected ancestor.'),
 ('right','Descendant lineages','TIPS','Lancelet, Shark, Salamander, Mouse, Lizard, and Pigeon remain fixed as descendant tips and never move into an ancestral node.')],
'U7-L37':[
 ('left','Early-branching lineage','SHARK','The Shark badge remains attached to the branch leaving N1 before the sampled tetrapod clade begins at N2.'),
 ('center','Shared immediate node','N4','The N4 node remains lit at the exact fork producing the sampled Lizard and Pigeon descendant lineages.'),
 ('right','Sister-taxon pair','LIZARD + PIGEON','The Lizard and Pigeon badges remain side by side only because their two branches descend immediately from the same N4 node.')],
'U7-L38':[
 ('left','Ancestral-character state','STATE 0','The character matrix displays a reference state for each trait before any state change is mapped onto a branch.'),
 ('center','Shared-derived-character and synapomorphy wall','CHANGE ON BRANCH','A magnetic branch map accepts one character-state change at a specific node-to-node segment and sends the derived state only to its descendants.'),
 ('right','Derived-character descendants','STATE 1','Descendant taxon badges light only when they inherit the mapped derived state from the indicated common ancestor.')],
'U7-L39':[
 ('left','Outgroup reference lineage','LANCELET','The Lancelet badge stands outside the focal vertebrate ingroup and keeps its character states available as a comparison.'),
 ('center','Ancestral-versus-derived inference gate','POLARITY','A gate compares outgroup and ingroup states before labeling a state ancestral or derived for the focal comparison.'),
 ('right','Ingroup character map','VERTEBRATES','Shark, Salamander, Mouse, Lizard, and Pigeon remain inside the ingroup while the inferred character polarity is carried back onto their rooted tree.')],
'U7-L40':[
 ('left','Morphological and fossil evidence bench','FORM / FOSSIL','A character matrix and fossil-context cards generate one set of relationship constraints without erasing uncertainty.'),
 ('center','Phylogeny-construction lab','CANDIDATE A / B','Two candidate trees retain the same taxon names and node-ID scheme while their competing relationships are tested against evidence.'),
 ('right','DNA and protein sequence evidence bench','SEQUENCE','Aligned homologous DNA and protein strips add an independent evidence stream and can strengthen or revise the best-supported branching hypothesis.')],
'U7-L41':[
 ('left','Monophyletic grouping','ANCESTOR + ALL','A transparent enclosure surrounds node N3 and all sampled descendants Mouse, Lizard, and Pigeon.'),
 ('center','Parsimony comparison table','FEWER CHANGES','A character-state counter compares how many state changes each candidate tree requires for the same matrix.'),
 ('right','Paraphyletic and polyphyletic groupings','MISSING DESCENDANTS / MISSING MRCA','Two red outlines show one group that leaves out a descendant of its included ancestor and another that gathers taxa without including their most recent common ancestor.')],
}

NARR={
'U7-L34':{
 'title':'The Archive Keeps Calling Every Diagram a Fact',
 'kicker':'A phylogeny is a testable hypothesis about evolutionary history, while taxonomy, systematics, and phylogenetics perform different scientific jobs.',
 'paragraphs':[
  "The doors of the **Phylogeny Navigation Archive** open onto a high circular room where branching maps float in the air like broken transit routes. On your **left**, a brass catalog has separate drawers for names, classifications, and relationship records. Directly **ahead**, a glass hypothesis desk projects six fixed taxon badges. Lancelet, Shark, Salamander, Mouse, Lizard, and Pigeon. On your **right**, an evidence board holds a character-state matrix, fossil cards, and short DNA and protein strips. Dr. Imani Vale clips a transparent six-taxon navigation dossier to the desk. Inside it, every taxon name is fixed and every internal node slot is labeled N0 through N4. A red warning above the room reads TREE LOADED. EVOLUTIONARY HISTORY FINAL.",
  "Imani begins on the left because the archive has mixed four different jobs together. She opens the drawer labeled **Taxonomy**. Taxonomy is the naming and classification of organisms. The six badges keep their scientific identities no matter how the later tree is drawn. She then opens **Systematics**. Systematics studies biological diversity and evolutionary relationships and includes classification informed by phylogeny. The systematics drawer can use relationship evidence to inform classification, yet naming organisms and testing a branching history are still different tasks.",
  "At the right evidence board, Imani places the matrix and sequence strips beneath **Phylogenetics**. Phylogenetics comprises methods used to infer and test evolutionary relationships among organisms or lineages. The methods can compare characters, fossils, DNA, proteins, and other evidence. The methods are not the evolutionary history itself. They are the tools used to evaluate competing relationship hypotheses.",
  "Only after those jobs are separated does she point to the center projection and name **Phylogeny**. A phylogeny is a hypothesis about the evolutionary history and relationships of a group of organisms or genes. The word *hypothesis* remains illuminated above the tree. The branching pattern is an inference supported by evidence. It is not a photograph of every ancestral population that ever existed.",
  "The archive immediately tries to lock the projected tree. Imani inserts a second evidence card and allows one relationship to be reconsidered. The tree changes, but the six taxon badges and the dossier remain the same. This demonstrates **Phylogenies are revisable**. Phylogenetic trees and cladograms are hypotheses that are revised when new evidence changes the best-supported relationships. The broader rule **Trees and cladograms are testable hypotheses** now appears above the desk. They are testable hypotheses about evolutionary relationships among lineages.",
  "The red warning fades, yet another error appears. The archive compares two diagrams and declares the one with longer branches more evolved. Imani carries the same six taxon badges into the next gallery while keeping N0 through N4 attached to the dossier. One diagram has arbitrary branch lengths. The other has a printed scale. Before any branch can be interpreted, the archive must learn whether its length actually encodes information."
 ]},
'U7-L35':{
 'title':'A Long Branch Means Nothing Until the Diagram Says What Length Means',
 'kicker':'Cladograms show branching order, while some phylogenetic trees explicitly scale branches to time or amount of evolutionary change.',
 'paragraphs':[
  "The **Tree–Cladogram Scale Gallery** contains two enormous branching diagrams. On your **left**, an unscaled cladogram uses the same six taxon badges and node IDs N0 through N4, but some branches are drawn long and others short simply to fit the wall. Directly **ahead**, a rotating comparison rail holds both diagrams by their node labels. On your **right**, a phylogenetic tree carries an explicit scale bar for time or amount of evolutionary change. Imani keeps every taxon badge on the same present-time boundary and points to the scale bar before allowing any branch length to be interpreted.",
  "She starts with the left diagram. Its branch lengths have no numerical legend. The only information guaranteed by the drawing is branching order. Imani rotates the branch descending from N3 so Mouse appears above the Lizard-Pigeon pair. Then she rotates N4 so Pigeon appears above Lizard. The tip order changes dramatically, yet N3 still gives rise to Mouse and N4, and N4 still gives rise to Lizard and Pigeon. No ancestry relationship has changed.",
  "The comparison rail now places the right diagram beside the cladogram. Here, branch length is tied to an explicit scale. Some phylogenetic trees can represent amounts of evolutionary change or time when calibrated with fossils or molecular clocks. Imani names **Tree versus cladogram scale** only after the scale distinction is visible. Cladograms show branching order without implying a time or change scale. Scaled phylogenetic trees can encode additional quantitative information when the diagram explicitly defines it.",
  "The archive tries to read the tips from left to right as a march from primitive to advanced. Imani slides all six extant badges onto the same vertical present-time line. Lancelet, Shark, Salamander, Mouse, Lizard, and Pigeon are living sampled taxa in this display. Their horizontal or vertical order on the page is not an evolutionary ranking. A rotation around a node can reverse that visual order without altering which descendants share a common ancestor.",
  "She makes the test harder by rotating the entire N2 subtree. Salamander moves to the top of the drawing, Mouse moves below it, and Lizard and Pigeon swing to the bottom. The node IDs do not move to new ancestral positions. N2 still marks the same inferred common ancestor of the sampled tetrapod descendants. The visual map can be rearranged, but the topology remains the same because the connection pattern among nodes and descendants is unchanged.",
  "The comparison rail locks the scale labels in place and opens a door into the archive's anatomy board. The next error is more dangerous. The system has begun treating whichever taxon is drawn closest to the root as the ancestor of the others. Imani carries the same rotated tree forward. The next scene will label the root, internal nodes, lineages, clades, and descendant tips so no living taxon can slide backward into an ancestral node."
 ]},
'U7-L36':{
 'title':'The Nodes Are Ancestors and the Living Tips Are Not',
 'kicker':'Roots, nodes, lineages, and clades describe positions and ancestry on a tree, while extant tips remain descendants rather than ancestors of other living taxa.',
 'paragraphs':[
  "The **Tree Anatomy Board** fills a wall from left to right. On your **left**, root node N0 glows at the base of the six-taxon tree, followed by the early internal branch toward N1. Directly **ahead**, the center board displays N0, N1, N2, N3, and N4 as permanent illuminated circles. On your **right**, all six living taxon badges sit on the same present-time boundary. Lancelet, Shark, Salamander, Mouse, Lizard, and Pigeon. Imani clips the node map from the dossier beneath the center board and turns off every label that calls a living tip an ancestor.",
  "She traces one continuous branch from N2 toward Salamander. That path represents a **Lineage**, a line of descent through time connecting ancestors and descendants. A lineage can continue through internal ancestral populations and into a sampled descendant tip. The line is not the same thing as the name printed at the endpoint. The Salamander badge identifies the sampled descendant lineage at the tip.",
  "Imani then taps N4. Two branches leave it, one ending at Lizard and one at Pigeon. **Nodes represent common ancestors**. Nodes on phylogenetic trees or cladograms represent inferred most recent common ancestors of descendant lineages. N4 therefore represents the inferred common ancestor of the sampled Lizard and Pigeon lineages. Neither Lizard nor Pigeon is being used as the ancestor of the other.",
  "She returns to N0 and names the **Root of a phylogenetic tree**. The root represents the ancestral lineage from which all taxa shown in the rooted tree descend. In this six-taxon display, N0 is the root for the complete sampled set. The root gives direction to the ancestry interpretation. It does not mean the taxon badge drawn nearest N0 is the oldest living organism. Imani has you trace from N0 to each of the six tips without skipping an internal node. Every path begins at the root and moves through the branching history toward a sampled descendant. The exercise makes the direction of ancestry physical rather than dependent on whichever side of the page looks oldest.",
  "The center board now draws a transparent boundary around node N3 and every branch descending from it. Mouse, Lizard, and Pigeon fall inside the boundary. This is a **Clade**, a group containing a common ancestor and all of its descendants. The clade can be defined from the node outward. If one descendant is deliberately left outside, the outlined set no longer represents that complete clade.",
  "The optional recall shutter hides the labels while N0 through N4 and the six tip badges remain glowing. When the labels return, N4 begins flashing. The archive claims Shark and Salamander are sister taxa because they appear next to each other on the page after the last rotation. Imani carries the same node map into a branching fork. The next scene will decide sister relationships from a shared immediate node, not from visual proximity."
 ]},
'U7-L37':{
 'title':'Standing Next to Each Other on the Page Does Not Make Two Taxa Sisters',
 'kicker':'Sister taxa share the same immediate common-ancestor node, while an early-branching lineage is defined by branching position and is never a primitive living ancestor.',
 'paragraphs':[
  "The **Sister and Early-Branching Fork** is built around one enlarged copy of the same tree. On your **left**, the Shark lineage leaves node N1 before the sampled tetrapod clade begins at N2. Directly **ahead**, node N4 glows where exactly two branches separate. On your **right**, the Lizard and Pigeon badges sit at the ends of those two branches. Imani rotates N4 once more so the two tips exchange vertical positions. Their shared node remains fixed in the center.",
  "She traces from Lizard backward and stops at the first node encountered, N4. She traces from Pigeon backward and reaches that same node immediately. Only then does she name **Sister taxa**. Sister taxa or sister clades are the two descendant lineages that share the same immediate common ancestor. Their relationship comes from N4. It does not depend on whether the two names happen to be printed side by side after a branch rotation.",
  "The archive next highlights Shark and labels it PRIMITIVE. Imani removes the word. Relative to the focal tetrapod group, the Shark lineage branches earlier from the sampled vertebrate tree. The canonical term **Basal lineage** appears in the dossier, but Imani attaches it to branching position only. An early-branching or basal lineage diverges near the root of a focal group. It is not less evolved, unfinished, or the living ancestor of the later-branching taxa.",
  "She moves the Shark badge higher and lower on the page while its branch remains attached to N1. Nothing about its evolutionary status changes. The sampled Shark lineage has been evolving through time just as the sampled Mouse, Lizard, and Pigeon lineages have. Early branching describes where a lineage splits in the tree relative to the focal comparison. Imani then places a transparent present-time bar across all six tips. Shark touches the same present boundary as Salamander, Mouse, Lizard, and Pigeon. The branch began diverging earlier in the sampled history, yet the extant lineage did not stop evolving when that split occurred.",
  "Imani then places Shark visually beside Salamander. The archive again tries to call them sisters. She asks for the immediate shared node. Shark first reaches N1. Salamander first reaches N2. Their most recent common ancestor in the sampled tree is deeper than the node uniting Lizard and Pigeon, so page adjacency cannot define the relationship. The node test wins every time.",
  "The center N4 light sends a pulse backward through N3 and N2 until it reaches a wall covered in character-state squares. Some squares are labeled state 0 and others state 1. The archive has begun marking every visually unusual trait as derived without checking the reference condition. The next scene will map character changes onto exact branches and make ancestral, derived, and shared-derived states depend on the comparison being analyzed."
 ]},
'U7-L38':{
 'title':'A Character Becomes Derived Only After Its Change Is Placed on a Branch',
 'kicker':'Ancestral and derived states are relative to a comparison, and a synapomorphy is a shared derived character inherited from a common ancestor.',
 'paragraphs':[
  "The **Character Mapping Wall** is covered with a six-row character matrix. On your **left**, state 0 columns display reference character conditions for Lancelet and the vertebrate ingroup. Directly **ahead**, a magnetic branch map shows N0 through N4 with empty slots along each branch segment. On your **right**, descendant badges light whenever they inherit a mapped state change. Imani places the character matrix beside the tree and keeps the Lancelet reference column visible even though the formal outgroup gate is still one room away.",
  "She selects one character, the amniotic egg condition, and marks the earlier reference state on the left. The dossier labels an **Ancestral character** as a character state inferred to have been present in the ancestor for the focal comparison. Ancestral does not mean simpler, weaker, or universally older in every possible comparison. The label is tied to a particular character and the group being analyzed.",
  "Imani then places a state change on the branch leading into N3, the sampled amniote ancestor. Mouse, Lizard, and Pigeon illuminate on the right because they descend from that branch. The new condition is a **Derived character**, a character state that differs from the inferred ancestral state in the focal comparison. The archive cannot call a trait derived merely because it looks unusual. The state has to be interpreted relative to the comparison and mapped history.",
  "Because Mouse, Lizard, and Pigeon share that derived condition through the common ancestor represented by N3, the wall names **Shared derived characters** as evidence that can inform phylogeny. Imani then introduces the exact term **Synapomorphy**. A synapomorphy is a shared derived character inherited from the most recent common ancestor of the group in question. The branch position matters because it explains why the descendant set shares the state. She adds a second mapped example to the wall. A four-limbed tetrapod state is placed deeper, on the branch leading into N2, so Salamander joins Mouse, Lizard, and Pigeon in inheriting it. The two branch positions create two nested descendant sets and make character mapping feel like inheritance through a branching route rather than labels pasted onto tips.",
  "The wall now demonstrates **Character changes inform phylogeny**. Changes in heritable character states can be mapped onto branches and used to infer relationships among lineages. Imani deliberately removes one character and shows that another may support a different candidate arrangement. Character evidence contributes to a relationship hypothesis. A single trait does not become an infallible tree.",
  "A gate opens at the far end of the wall and the Lancelet badge slides onto a separate rail. The character matrix already used its states as a reference, but the archive has never formally established why an outside lineage is useful. The next scene will define the outgroup, keep it outside the vertebrate ingroup, and use its character states to infer polarity without ever turning the outgroup into the ancestor of the ingroup."
 ]},
'U7-L39':{
 'title':'The Outgroup Stands Outside the Question Without Becoming the Ancestor',
 'kicker':'An outgroup is an external comparison lineage used to infer ancestral and derived character states for a focal ingroup.',
 'paragraphs':[
  "The **Outgroup Reference Gate** divides the navigation archive into three clear zones. On your **left**, the silver Lancelet badge stands on its own reference rail. Directly **ahead**, an inference gate compares character states from that rail with the states found across the focal group. On your **right**, the vertebrate ingroup contains Shark, Salamander, Mouse, Lizard, and Pigeon on the rooted tree with N1 through N4 still labeled. Imani keeps N0 visible behind the gate so the Lancelet can remain related to the ingroup without being placed inside it.",
  "She names the relationship **Outgroup use**. An outgroup is a lineage outside the focal ingroup that helps infer which character states are ancestral and which are derived. Lancelet is outside the vertebrate ingroup in this analysis. It is a comparison lineage, not a living ancestor of Shark, Salamander, Mouse, Lizard, or Pigeon.",
  "The gate compares one character state in Lancelet with the states across the ingroup. A state shared with the outgroup can support an inference that the state is ancestral for the ingroup, while a different state appearing within an ingroup branch can be interpreted as derived in the focal comparison. Imani labels this broader relationship **Outgroup in phylogenetic inference**. Outgroups help establish character-state polarity by providing a reference outside the ingroup. The gate demonstrates the comparison with the vertebral-column character. Lancelet remains on the outside reference rail while the vertebrate ingroup shares the derived condition. That comparison helps place the change on the branch entering the ingroup rather than on an arbitrary living tip.",
  "She then moves the Lancelet badge farther left on the display. The archive tries to interpret the physical distance as more ancient. Imani blocks that reading. The outgroup relationship is defined by branching outside the focal ingroup, not by how far the badge is drawn from it. A diagram can rotate or stretch without turning an extant outgroup into an ancestral species. She returns the badge to the same present-time boundary as the vertebrate tips so its role remains unmistakably comparative rather than ancestral.",
  "The character-state gate sends its polarity decisions back to the right-side ingroup map. The amniotic egg state remains mapped to N3 because the reference comparison supports its derived status within the sampled tree. Imani records the outgroup evidence in the dossier beside the character matrix so the basis of the ancestral-versus-derived inference remains visible.",
  "The optional recall light hides the labels but leaves Lancelet alone on the left and the five vertebrate taxa on the right. When the gate reopens, two candidate trees rise in the next laboratory. One fits several morphological characters, while the other gains stronger support after aligned DNA and protein evidence is added. The next scene will use multiple evidence sources to build and revise a phylogeny without pretending that any tree has become permanent fact."
 ]},
'U7-L40':{
 'title':'The Tree Must Survive More Than One Kind of Evidence',
 'kicker':'Phylogenies are constructed from multiple evidence sources, and molecular evidence can strengthen or revise relationships while every tree remains a testable hypothesis.',
 'paragraphs':[
  "The **Phylogeny Evidence Construction Lab** resembles a courtroom with three benches. On your **left**, a morphological and fossil bench holds the same character matrix plus dated fossil-context cards. Directly **ahead**, two candidate trees, A and B, use the same six taxon names and the same persistent node-ID scheme. On your **right**, aligned homologous DNA and protein sequence strips wait beneath the same taxon labels. Imani places the navigation dossier between the candidate trees so no evidence source can quietly rename a taxon or move a tip into an ancestor.",
  "She begins with the left bench. Morphological characters and fossil evidence constrain which candidate relationships are plausible. Some characters support the Lizard-Pigeon grouping, while other characters may be shared more broadly. The fossil cards add historical context. Imani records **Sources used to construct phylogenies**. Phylogenies can be constructed using morphological, fossil, molecular, developmental, behavioral, and other evidence when those data are appropriate to the comparison.",
  "The center lab then evaluates the candidate trees against the character matrix. Candidate A and candidate B each explain some observations, but neither is declared final. The archive keeps the hypothesis label visible because a tree remains an inference that can be revised as evidence changes. Imani runs the same character row across both candidates. On one tree the observed state can be explained by one mapped change. On the other it requires repeated independent changes. That comparison does not settle the entire tree, yet it gives the evidence a measurable consequence that can be combined with the fossil and molecular records.",
  "Imani activates the right bench and aligns homologous DNA and protein sequences from the same six taxa. She records **Molecular evidence in phylogeny**. DNA and protein sequence comparisons can provide powerful evidence for evolutionary relationships and may support or revise relationships inferred from morphology. Molecular evidence receives appropriate weight because it supplies many heritable characters, yet the lab does not turn the word molecular into a command to ignore every other evidence source.",
  "The sequence evidence gives stronger support to one candidate relationship. Candidate B becomes the current best-supported tree, and the center projection updates while all six taxon badges remain fixed. Imani points to the revision. The tree changed because the evidence changed, not because someone rotated a branch or reordered the tips. That distinction links the lab back to the first two archive rooms.",
  "The winning candidate moves into the final wing, where the archive begins drawing colored circles around different sets of taxa. One circle contains an ancestor and every descendant. Another omits a descendant. A third gathers distant taxa while excluding their most recent common ancestor. Beside them, a change counter begins tallying how many character-state transitions different candidate trees require. The next scene will separate grouping terms from the **Principle of parsimony** and keep parsimony in its proper role as one inference criterion."
 ]},
'U7-L41':{
 'title':'The Final Map Fails When a Group Leaves Out the Branches That Define It',
 'kicker':'Monophyletic, paraphyletic, and polyphyletic groups describe different relationships to common ancestry, while parsimony compares candidate explanations by required character-state changes.',
 'paragraphs':[
  "The **Grouping and Parsimony Wing** surrounds the final rooted tree with three transparent enclosures. On your **left**, a green boundary begins at N3 and surrounds Mouse, Lizard, and Pigeon. Directly **ahead**, a parsimony table compares candidate trees using the same character matrix from the archive. On your **right**, two red boundaries create deliberately incomplete or disconnected groupings. Imani places the six-taxon dossier beneath the tree and locks the node labels so the grouping terms must be judged from ancestry, not from which names look similar.",
  "She starts with the green enclosure. It contains N3 and every sampled descendant of N3. Mouse, Lizard, and Pigeon all remain inside. Imani names a **Monophyletic group**. A monophyletic group contains a common ancestor and all of its descendants. The boundary can be reconstructed by choosing a node and following every descendant branch outward.",
  "The first red boundary includes N3, Mouse, and Lizard but deliberately leaves Pigeon outside even though Pigeon also descends from N3. Imani names a **Paraphyletic group**. A paraphyletic group contains a common ancestor and some, but not all, of its descendants. The missing descendant is the diagnostic visual. The group starts from a real ancestral node yet does not include the complete descendant set.",
  "The second red boundary circles Shark and Pigeon while excluding the other descendants of their most recent common ancestor in the sampled tree. Imani names a **Polyphyletic group**. A polyphyletic grouping combines taxa without including their most recent common ancestor as part of that group. The line has to jump across the tree to gather the chosen tips, which makes the ancestry problem physically obvious.",
  "At the center table, Imani compares the candidate trees against the same character matrix. One tree requires more independent character-state changes to explain the observed distribution. The other requires fewer. She introduces the **Principle of parsimony**. Parsimony favors the explanation requiring fewer evolutionary changes when comparing hypotheses under the chosen character model. It is a useful criterion, yet it is not the only phylogenetic method and does not guarantee that the simplest tree is always the true history.",
  "The final optional recall light removes every term while leaving N3, the green complete-descendant enclosure, the two red error boundaries, and the change counter visible. When the labels return, the navigation archive finally clears its warning. Imani reconstructs the whole route with the same six taxa and the same N0 through N4 node IDs. Taxonomy named and classified. Systematics connected diversity and relationships. Phylogenetics supplied methods. A phylogeny remained a revisable hypothesis. Scale information was read only when encoded. Nodes represented ancestors, living tips remained descendants, sister taxa shared an immediate node, characters gained polarity through comparison and outgroup evidence, multiple evidence sources tested candidate trees, and grouping boundaries were judged from common ancestry. The archive can rotate a branch now without ever claiming that ancestry itself has moved."
 ]},
}

CHECKPOINTS={'U7-L36','U7-L39','U7-L41'}

def clean_prose(text):
    return text.replace(' — ', '. ').replace('—','-').replace(': ','. ')

def word_count(paragraphs):
    return len(re.findall(r"\b[\w’′'-]+\b",' '.join(paragraphs)))

def zone_objs(lid):
    return [{'position':p,'label':label,'symbol':symbol,'description':description} for p,label,symbol,description in ZONES[lid]]

def cast_for(lid):
    items=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    for position,label,symbol,description in ZONES[lid]:
        items.append({'name':label,'kind':'phylogeny evidence, tree, or comparison zone','visual':description,'job':f"Remain fixed on the learner's {position} and carry the {position}-side phylogenetic role required by the locked F3 geometry."})
    items.append({'name':'Six-taxon badge rail','kind':'persistent phylogeny object','visual':'six fixed specimen badges for Lancelet, Shark, Salamander, Mouse, Lizard, and Pigeon, each with a distinct icon and the same name in every room','job':'prevents visual rearrangement from changing taxon identity or turning one extant taxon into another'})
    items.append({'name':'Persistent node map','kind':'persistent phylogeny object','visual':'five illuminated internal-node labels N0, N1, N2, N3, and N4 that remain attached to the same inferred common-ancestor positions through every branch rotation','job':'keeps common-ancestor identity stable even when tree orientation changes'})
    items.append({'name':'Six-taxon navigation dossier','kind':'journey continuity object','visual':'a transparent folder containing the taxon list, node map, character-state matrix, fossil cards, and aligned DNA/protein strips','job':'keeps evidence and identities traceable while candidate phylogenetic hypotheses are compared or revised'})
    return items

def beats_for(lid):
    b=B[lid]
    terms={t['knowledge_id']:t for t in b['term_introductions']}
    scene_hint={
      'U7-L34':'the taxonomy and systematics drawers separated from the phylogenetics evidence board and the revisable center phylogeny',
      'U7-L35':'the same N0–N4 topology surviving branch rotations while only the scaled tree carries time or change information',
      'U7-L36':'the N0 root, persistent internal nodes, descendant lineages, and node-defined clades with all living tips on one present-time boundary',
      'U7-L37':'the N4 immediate node uniting Lizard and Pigeon while Shark remains an early-branching sampled lineage relative to tetrapods',
      'U7-L38':'the character matrix mapping a state change onto a branch so descendants inherit a derived state from a specified common ancestor',
      'U7-L39':'the Lancelet outgroup standing outside the vertebrate ingroup while its states help infer ancestral-versus-derived polarity',
      'U7-L40':'the same candidate trees tested against morphological, fossil, DNA, and protein evidence without changing taxon identity',
      'U7-L41':'the N3 monophyletic enclosure, incomplete paraphyletic boundary, disconnected polyphyletic boundary, and parsimony change counter',
    }[lid]
    out=[]
    for kid in b['knowledge_ids']:
        t=terms[kid]; c=CANON[kid]
        out.append({
          'object_id':kid,'term':t['canonical_term'],'story':scene_hint,
          'science':c['canonical_verified_statement'],'exact_name':bool(t['exact_name_recall']),
          'hint':scene_hint,'name_support':t['name_support'],'reactivation_mode':t['reactivation_mode'],'scope_class':t['scope_class']
        })
    return out

scenes=[]
for i,lid in enumerate(J4['route']):
    b=B[lid]; n=NARR[lid]; route=ROUTE[i]
    paragraphs=[clean_prose(p) for p in n['paragraphs']]
    cp=lid in CHECKPOINTS
    scenes.append({
      'scene_index':i,'locus_id':lid,'locus':route['locus'],'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['micro_anchor'],'scene_layout':{'orientation':b['orientation_sentence'],'zones':zone_objs(lid)},
      'cast':cast_for(lid),'taxa':TAXA,'node_map':NODE_MAP,'continuity_object':CONTINUITY,
      'story_open':paragraphs[0],'story_paragraphs':paragraphs,'story_close':paragraphs[-1],
      'object_ids':list(b['knowledge_ids']),'story_beats':beats_for(lid),
      'prior_unit_reactivation':b['prior_unit_reactivation'],'misconception_guards':b['misconception_guards'],
      'checkpoint':cp,'checkpoint_object_id':b['primary_knowledge_id'] if cp else None,
      'checkpoint_prompt':b['quick_recall']['candidate_prompt'] if cp else '',
      'checkpoint_answer':b['quick_recall']['answer'] if cp else '',
      'next_locus':ROUTE[i+1]['locus'] if i+1<len(ROUTE) else None,
      'f3_scene_brief_id':b['scene_brief_id'],'narrative_word_count':word_count(paragraphs),
    })

journey={
 'palace_id':'U7-J4','unit_id':'unit-7','palace_name':'Phylogeny Navigation Archive',
 'story_title':'The Tree Archive That Changed Its Ancestry Every Time a Branch Rotated',
 'tagline':'A navigation archive keeps mistaking page position for ancestry. Hold six taxon identities and five node IDs steady while branches rotate, character states are mapped, outgroup evidence is added, and candidate trees are revised until the archive can tell a changed drawing from a changed evolutionary hypothesis.',
 'guide':GUIDE,
 'premise':'The Phylogeny Navigation Archive has corrupted its route system. It treats every tree as final fact, reads long branches as more evolved, turns living tips into ancestors, labels nearby names as sister taxa, calls early-branching lineages primitive, assigns derived states by appearance, makes an outgroup the ancestor of the ingroup, and changes ancestry whenever a branch rotates. Dr. Imani Vale freezes six taxon identities and node IDs N0 through N4 before allowing any hypothesis to move.',
 'mission':'Carry one six-taxon navigation dossier through eight permanent locations. Separate taxonomy, systematics, phylogenetics, and phylogeny; interpret scale only when encoded; identify roots, nodes, lineages, clades, sister taxa, and early-branching lineages from connections; map ancestral and derived states; use an outgroup for polarity; test candidate trees with multiple evidence streams; and finish by distinguishing grouping types and parsimony.',
 'finale':'The archive clears its navigation error only after every relationship can be reconstructed from node connections and evidence rather than drawing position. Branches can rotate freely without changing ancestry, while a tree changes only when the evidence supports a different hypothesis.',
 'estimated_minutes':28,'scene_count':8,'checkpoint_count':len(CHECKPOINTS),
 'student_release':'DEVELOPER_PREVIEW_F4D','preview_release':True,'narrative_design':'U7-F4D-NARRATIVE-1.0',
 'learner_rule':'Read or listen while keeping the six taxon badges and N0 through N4 stable. A branch may move visually, but node identity and descendant membership do not change unless the evidence supports a genuinely different phylogenetic hypothesis.',
 'route_orientation':'The archive is one continuous navigation circuit. Begin at the hypothesis desk, move through the scale gallery and anatomy board, enter the sister-lineage fork, map character states, cross the outgroup gate, test candidate trees in the evidence lab, and finish at the grouping and parsimony wing.',
 'route':ROUTE,'taxa':TAXA,'node_map':NODE_MAP,'scenes':scenes,
 'source_brief_lock':'LOCKED_F3','scientific_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2',
 'frozen_prior_journey_lock':'LOCKED_F4C_J1_J3'
}

(U7/'journeys'/'U7-J4.json').write_text(json.dumps(journey,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

summary={
 'schema':'memory-palace-v2-unit7-f4d-journeys-1.0','unit_id':'unit-7','stage':'F4D','student_release':False,'preview_release':True,
 'journey_count':4,'scene_count':41,'checkpoint_count':J1['checkpoint_count']+J2['checkpoint_count']+J3['checkpoint_count']+len(CHECKPOINTS),
 'guided_journeys':[
   {k:J1[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']},
   {k:J2[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']},
   {k:J3[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']},
   {k:journey[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']}
 ]
}
(U7/'journeys-f4d.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

status={
 'unit_id':'unit-7','number':7,'title':'Natural Selection','status':'F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','pipeline_stage':'F4D_JOURNEY4_NARRATIVE',
 'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3',
 'narrative_lock':'LOCKED_F4D_J1_J4','student_release':False,'preview_release':True,
 'journey_count':4,'scene_count':41,'memory_objects':0,'application_challenges':0,
 'canonical_records':215,'architecture_journeys':6,'architecture_bundles':23,'architecture_loci':55,'scene_briefs':55,'palace_managed_records':174,
 'challenge_lab_records':16,'scope_guard_records':25,'exact_name_review_targets':94,'confusable_sets':33,'optional_first_exposure_recalls':18,
 'f4a_journey':'U7-J1','f4a_scene_count':10,'f4b_journey':'U7-J2','f4b_scene_count':14,'f4c_journey':'U7-J3','f4c_scene_count':9,
 'f4d_journey':'U7-J4','f4d_scene_count':8,'f4d_knowledge_records':26,'f4d_exact_name_targets':21,'f4d_optional_recalls':len(CHECKPOINTS),
 'next_required_output':'F4E polished narrative for Journey 5 only after Journeys 1 through 4 remain frozen and all F1-F4D gates continue to pass.'
}
(U7/'status-f4d.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(U7/'status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'
course=read(cp)
u=next(x for x in course['units'] if x['unit_id']=='unit-7')
u.update({
 'status':'F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','journey_count':4,'scene_count':41,'student_release':False,'preview_release':True,
 'source_status':'AUDITED_F1_ARCHITECTURE_F2_BRIEFS_F3_NARRATIVE_F4A_F4B_F4C_F4D','narrative_lock':'LOCKED_F4D_J1_J4','narrative_journeys':4,
 'pipeline_stage':'F4D_JOURNEY4_NARRATIVE'
})
cp.write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

doc=['# Unit 7 F4D · Journey 4 Narrative','','## The Tree Archive That Changed Its Ancestry Every Time a Branch Rotated','',journey['tagline'],'',
     '### Physical route','', ' → '.join(x['locus'] for x in ROUTE),'',
     '### Fixed taxa','', ' · '.join(x['name'] for x in TAXA),'',
     '### Persistent node map','']
for node,meaning in NODE_MAP.items():
    doc.append(f"- **{node}** — {meaning}")
doc += ['','### Continuity rule','',CONTINUITY,'']
for s in scenes:
    doc += [f"## {s['scene_index']+1}. {s['locus']} · {s['title']}",'',f"*{s['scene_kicker']}*",'']
    doc += s['story_paragraphs']+['']
    if s['checkpoint']:
        doc += ['**Optional Quick Recall**','',s['checkpoint_prompt'],'']
(ROOT/'docs'/'UNIT7_F4D_JOURNEY4_STORY.md').write_text('\n'.join(doc),encoding='utf-8')

# Protect prior narrative artifacts.
f4c=read(U7/'content-lock-f4c.json')
prior_files={}
for rel,meta in f4c.get('f4a_f4b_prior_narrative_protection',{}).items():
    prior_files[rel]=meta
for rel in [
    'content/ap-biology/unit-7/journeys/U7-J1.json',
    'content/ap-biology/unit-7/journeys/U7-J2.json',
    'content/ap-biology/unit-7/journeys/U7-J3.json',
    'content/ap-biology/unit-7/journeys-f4c.json',
    'content/ap-biology/unit-7/status-f4c.json',
    'content/ap-biology/unit-7/content-lock-f4c.json',
    'content/ap-biology/unit-7/f4c-release-manifest.json',
    'docs/UNIT7_F4C_JOURNEY3_STORY.md',
    'docs/UNIT7_F4C_RELEASE.md',
    'docs/UNIT7_F4C_QA.md',
    'docs/UNIT7_F4C_PACKAGE_QA.md',
]:
    rp=ROOT/rel
    if rp.exists():
        prior_files[rel]={'bytes':rp.stat().st_size,'sha256':sha(rp)}

locked_rel=['journeys/U7-J4.json','journeys-f4d.json','status-f4d.json']
lock_files={rel:{'bytes':(U7/rel).stat().st_size,'sha256':sha(U7/rel)} for rel in locked_rel}
lock={
 'schema':'memory-palace-v2-unit7-f4d-lock-1.0','unit_id':'unit-7','lock_status':'LOCKED_F4D_J1_J4','student_release':False,'preview_release':True,
 'protected_prior_locks':['content-lock-f1.json','content-lock-f2.json','content-lock-f3.json','content-lock-f4a.json','content-lock-f4b.json','content-lock-f4c.json'],
 'f4a_f4c_prior_narrative_protection':prior_files,
 'journey_id':'U7-J4','scene_count':8,'knowledge_record_count':26,'exact_name_target_count':21,'checkpoint_count':len(CHECKPOINTS),
 'files':lock_files,
 'rule':'Journeys 1 through 3 remain frozen byte-for-byte. Journey 4 polished prose may not change after F4D without a new explicit narrative version. F1 science, F2 classification/geometry, and F3 scene briefs remain authoritative.'
}
(U7/'content-lock-f4d.json').write_text(json.dumps(lock,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

release={
 'schema':'memory-palace-v2-unit7-f4d-release-1.0','generated_utc':'2026-09-08T14:55:00+00:00','unit_id':'unit-7',
 'release_status':'F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','student_release':False,'preview_release':True,
 'completed_journeys':['U7-J1','U7-J2','U7-J3','U7-J4'],'journeys':4,'scenes':41,
 'f4d_journey_id':'U7-J4','f4d_scenes':8,'f4d_knowledge_records':26,'f4d_exact_name_targets':21,'f4d_optional_first_exposure_recalls':len(CHECKPOINTS),
 'canonical_records':215,'permanent_loci_architecture':55,'scene_briefs':55,'memory_objects':0,'application_challenges':0,
 'scientific_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','narrative_lock':'LOCKED_F4D_J1_J4',
 'next_stage':'F4E Journey 5 polished narrative after F4D regression'
}
(U7/'f4d-release-manifest.json').write_text(json.dumps(release,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

print(json.dumps({
 'journey':'U7-J4','scenes':8,'knowledge_records':26,'exact_name_targets':21,'checkpoints':len(CHECKPOINTS),
 'words':sum(s['narrative_word_count'] for s in scenes),
 'mean_words':round(sum(s['narrative_word_count'] for s in scenes)/8,1),
 'min_words':min(s['narrative_word_count'] for s in scenes),
 'max_words':max(s['narrative_word_count'] for s in scenes),
},indent=2))
