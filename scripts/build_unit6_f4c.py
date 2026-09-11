from __future__ import annotations
import json, hashlib, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U6=ROOT/'content'/'ap-biology'/'unit-6'
BRIEFS=json.loads((U6/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS=json.loads((U6/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J3=next(j for j in JBRIEFS if j['journey_id']=='U6-J3')
B={b['locus_id']:b for b in BRIEFS if b['journey_id']=='U6-J3'}
CANON={r['knowledge_id']:r for r in json.loads((U6/'source'/'canonical-unit6-f1.json').read_text(encoding='utf-8'))['canonical_catalog']}

GUIDE={
 'name':'Dr. Sora Han','role':'molecular-information systems director',
 'visual':'dark-cobalt lab coat, clear gloves, transparent 5′→3′ compass tablet, and a narrow copper information ledger',
 'story_job':'Sora keeps the same mature red mRNA ribbon, highlighted AUG start codon, fixed triplet spacing, and growing polypeptide visible through the entire translation route. She points to real ribosomes, tRNAs, codons, amino acids, and enzymes and names terms only after their defining structure or action is visible.'
}

ROUTE=[
 {'scene_index':0,'locus':'Translation Geography Platform','short':'Where translation occurs','floor':'Hall entrance','symbol':'RIBO'},
 {'scene_index':1,'locus':'Reading-Frame Start Gate','short':'Start and frame','floor':'Start gate','symbol':'AUG'},
 {'scene_index':2,'locus':'Codon Code Wall','short':'Codon code','floor':'Code gallery','symbol':'3 nt'},
 {'scene_index':3,'locus':'tRNA Charging Dock','short':'Charge tRNA','floor':'Courier dock','symbol':'AA+tRNA'},
 {'scene_index':4,'locus':'Ribosome A–P–E Platform','short':'A P E','floor':'Ribosome platform','symbol':'A|P|E'},
 {'scene_index':5,'locus':'Polypeptide Elongation Conveyor','short':'Elongate','floor':'Assembly line','symbol':'→AA'},
 {'scene_index':6,'locus':'Stop and Release Dock','short':'Stop and release','floor':'Release dock','symbol':'STOP'},
 {'scene_index':7,'locus':'Retroviral Reverse-Flow Gate','short':'Reverse flow','floor':'Exception gate','symbol':'RNA→DNA'},
]

ZONES={
'U6-L21':[
 ('left','eukaryotic cytosolic and rough-ER ribosome side','ER/RIBO','The mature red mRNA exits a nuclear doorway and can meet free cytosolic ribosomes or ribosomes attached to the cytoplasmic surface of rough ER.'),
 ('center','translation-location comparison platform','WHERE?','A raised floor map keeps cell compartments and ribosome positions visible so location itself explains which processes can overlap.'),
 ('right','prokaryotic coupled-transcription and translation side','DNA→RNA→RIBO','A gray bacterial DNA region, an emerging RNA, and a ribosome occupy one open cellular space with no nucleus between them.')],
'U6-L22':[
 ('left','reading-frame alignment side','1|2|3','Three sliding base grids show that the same nucleotide sequence can be grouped into different triplets depending on where reading begins.'),
 ('center','AUG start gate','AUG','The red mRNA passes through a fixed AUG gate where an initiator tRNA and ribosome establish the starting position for translation.'),
 ('right','translation-stage route','I→E→T','Three connected stations labeled initiation, elongation, and termination run forward from the start gate.')],
'U6-L23':[
 ('left','codon triplet examples','XXX','The fixed reading frame divides the same red mRNA into visible three-base blocks that never slide relative to one another.'),
 ('center','codon-to-amino-acid mapping wall','CODE','A genetic-code chart maps each mRNA codon to an amino acid or stop instruction.'),
 ('right','redundancy and near-universality display','≈ALL','Several different codons converge on the same amino acid while organism panels show the code is shared by nearly all living organisms.')],
'U6-L24':[
 ('left','amino acid and synthetase side','AA+ENZ','Free amino acids and real aminoacyl-tRNA synthetase enzymes occupy separate matching stations before any tRNA approaches the ribosome.'),
 ('center','tRNA charging dock','tRNA+AA','A tRNA is loaded with its correct amino acid at the center dock, leaving the anticodon exposed and the amino acid attached at the opposite end.'),
 ('right','charged-tRNA delivery route','→RIBO','Charged tRNAs travel rightward toward the ribosome while the red mRNA remains visible beyond the dock.')],
'U6-L25':[
 ('left','A-site entry','A','A charged aminoacyl-tRNA enters the ribosome at the A site only after its anticodon matches the exposed mRNA codon.'),
 ('center','P-site peptide and ribosome platform','P','The P site holds the tRNA carrying the growing polypeptide while the large and small ribosomal subunits surround the mRNA.'),
 ('right','E-site exit and subunit-size context','E','An uncharged tRNA leaves through the E site beside a small contextual panel showing bacterial and eukaryotic ribosome subunit sizes.')],
'U6-L26':[
 ('left','incoming codon–anticodon match','MATCH','The next charged tRNA is held beside the next exposed mRNA codon until complementary pairing is correct.'),
 ('center','polypeptide elongation conveyor','PEPTIDE','The ribosome catalyzes peptide-bond formation and transfers the growing chain to the amino acid on the incoming tRNA.'),
 ('right','translocation to next codon','+3 nt','The ribosome shifts exactly one codon along the same mRNA, moving tRNAs through their sites without changing the reading frame.')],
'U6-L27':[
 ('left','stop-codon arrival','STOP','A stop codon enters the decoding position at the end of the unchanged mRNA reading frame.'),
 ('center','termination and product-release dock','RELEASE','Termination machinery enters where no amino-acid-carrying stop tRNA exists, releases the completed polypeptide, and allows the translation complex to disassemble.'),
 ('right','post-translation folding side','FOLD','The released chain continues folding while chaperone and processing stations remain available for proteins that require additional help or modification.')],
'U6-L28':[
 ('left','retroviral RNA input','vRNA','A separate silver retroviral RNA genome enters while the completed normal translation route remains visible behind glass.'),
 ('center','reverse-transcription gate','RT','Reverse transcriptase copies information from the viral RNA template into complementary DNA.'),
 ('right','DNA product toward host-genome integration','DNA→HOST','The viral DNA product moves toward host-DNA integration, from which viral information can later be transcribed and translated.')],
}

NARR={
'U6-L21':{
 'title':'The Message Reaches the Wrong Floor',
 'kicker':'Translation can only be understood after the ribosome is placed in the correct cellular geography.',
 'paragraphs':[
  "The mature red mRNA from the RNA Transcript Workshop slides through a nuclear export door and into a vast **Translation Assembly Hall**. Before you is a floor map large enough to walk across. On your **left**, the eukaryotic side holds free ribosomes in the cytosol and another row of ribosomes attached to the cytoplasmic surface of rough endoplasmic reticulum. Directly **ahead**, a raised **translation-location comparison platform** keeps the cell boundaries visible beneath clear glass. On your **right**, a gray bacterial cell model has no nuclear room at all. Its DNA region, a growing RNA transcript, and several ribosomes occupy the same open space. Dr. Sora Han clips the red mRNA to her copper ledger so its 5′ end, highlighted AUG, and fixed triplet spacing cannot be swapped for another message later. The hall has power, amino acids, tRNAs, and ribosomes, but the assembly line refuses to start because every ribosome has been routed as though cellular location made no difference.",
  "Sora first walks you to the left. The red mRNA remains in the cytoplasm, where a free ribosome can bind it. A second copy of the eukaryotic cell map shows ribosomes attached to the **cytoplasmic surface of rough ER**. In either case, the translation machinery itself faces the cytoplasm. Only after those locations are visible does Sora name the relationship **translation location**. Translation occurs on ribosomes in the cytoplasm of both prokaryotic and eukaryotic cells, and eukaryotic translation can also occur on ribosomes associated with the cytoplasmic surface of rough ER. The rough ER is therefore not a separate hidden translation chamber inside the ER lumen. The ribosome reads mRNA from the cytoplasmic side.",
  "She leaves the red eukaryotic mRNA on the left and activates the bacterial comparison on your right. There is no nuclear envelope between the bacterial DNA and cytoplasm. RNA polymerase begins synthesizing a gray mRNA from the DNA, but before the transcript has been fully released, a ribosome binds an exposed part of that same emerging RNA. The ribosome begins moving along the transcript while RNA polymerase is still extending it farther downstream. Sora draws one bracket around both processes and names **coupled transcription and translation in prokaryotes**. In prokaryotes, translation can begin on an mRNA while that mRNA is still being transcribed. The coupling is possible because transcription and translation occur in the same cellular compartment rather than being separated by a nucleus.",
  "The central platform now lights two routes without merging them. On the left, a eukaryotic nuclear gene must first produce RNA in the nucleus; a mature mRNA then reaches ribosomes in the cytoplasm or on rough ER. On the right, a prokaryotic transcript can meet ribosomes while transcription is still underway. Sora keeps the earlier prokaryotic-transcript lesson intact without turning it into the false rule that bacterial RNA never undergoes processing. The defining point here is geography. A prokaryotic cell lacks a nucleus, so a physical barrier does not separate transcription from translation in the way it does for eukaryotic nuclear genes.",
  "A floor sensor finally accepts the location map, and the red mRNA is allowed onto the center walkway. Yet the ribosome still refuses to read it. Its bases run continuously across the ribbon, and three illuminated grids on the next gate group those bases in three different ways. Sora does not let anyone choose a group at random. She carries the same mRNA toward the **Reading-Frame Start Gate**, where translation must establish exactly where the message begins before a single amino acid can be added."
 ]},
'U6-L22':{
 'title':'One Base Too Far Changes Every Word',
 'kicker':'AUG establishes the start, and the start fixes how the entire mRNA is divided into codons.',
 'paragraphs':[
  "The red mRNA enters a narrow gate room and stretches horizontally across the floor. On your **left**, the **reading-frame alignment side** contains three transparent grids, each offset by one nucleotide. Directly **ahead**, the center gate is cut around one glowing **AUG** triplet. On your **right**, a long route is divided into three connected stations labeled initiation, elongation, and termination. The message itself has not changed. Its nucleotide sequence is identical to the one that left the previous room. Only the way the bases are grouped changes when Sora slides the left grids. In the first grid, one set of three-letter groups appears. Shift the grid by one base and every downstream triplet is regrouped. Shift it again and a third series appears. The hall makes the danger visible before it gives the concept a name.",
  "Sora locks the correct grid in place and names the pattern a **reading frame**. A reading frame is the grouping of an mRNA nucleotide sequence into consecutive codons. The bases themselves do not move, but changing the starting position changes which bases belong together in every downstream three-nucleotide group. That is why a reading frame is more than the fact that codons contain three bases. It specifies the continuous grouping that the ribosome must preserve as it travels. Sora leaves the two incorrect offset grids on the wall as a comparison, then guides the unchanged red mRNA into the glowing center gate.",
  "At the gate, the first key triplet is **AUG**. A ribosome assembles around the mRNA, and an initiator tRNA positions methionine at the starting point. Only after the interaction is physically complete does Sora write **start codon AUG** in her ledger. Translation initiates at AUG, the start codon that specifies methionine, through interactions among the mRNA, the ribosome and its rRNA, and an initiator tRNA. AUG is therefore doing two jobs in this context. It marks where translation starts and it is a codon for methionine. The gate does not tell the ribosome to restart at every later AUG it encounters. The established reading frame is already being carried forward from this initiation event.",
  "The right-hand route lights in order. The event you just watched belongs to **initiation**. The center section of the route is **elongation**, during which the polypeptide will grow codon by codon. The far section is **termination**, where the process ends after a stop signal is reached. Sora names the complete sequence **translation stages**. Translation proceeds through initiation, elongation, and termination. The route is sequential, which means elongation does not begin before the starting complex is correctly positioned, and termination is not simply another kind of elongation step.",
  "Before the gate opens, Sora covers the mRNA with a blank strip and asks you to picture the room without looking back. The left side held the offset grids, the center held AUG, and the right side held the three-stage route. The optional recall asks which start codon established the frame. When the cover lifts, the red mRNA keeps its newly locked triplet spacing as it enters the next gallery. The ribosome now knows where to start, but it still needs a way to interpret what each three-base unit means."
 ]},
'U6-L23':{
 'title':'The Wall That Turns Triplets Into Instructions',
 'kicker':'Codons are three-base units in the fixed reading frame, and the genetic code maps those units to amino acids or stop signals.',
 'paragraphs':[
  "The next gallery is built around a wall-sized genetic-code display. On your **left**, the same red mRNA passes through a metal ruler that brackets its bases into permanent three-nucleotide blocks. Directly **ahead**, the **codon-to-amino-acid mapping wall** can accept one mRNA triplet at a time and illuminate the corresponding amino acid or a stop instruction. On your **right**, several different codon cards converge on the same amino-acid tray, while a row of organism silhouettes shares nearly the same mapping system. Sora keeps the highlighted AUG visible at the beginning of the mRNA so the grouping remains anchored to the reading frame established in the previous room.",
  "She feeds one bracketed three-base unit into the wall. Only now does she name those units **codons**. The mRNA nucleotide sequence is read in three-nucleotide units called codons. A codon is therefore a specific triplet within the established reading frame. The word codon does not mean the same thing as reading frame. The reading frame is the continuous grouping rule across the message; a codon is one of the three-nucleotide units created by that grouping. Sora keeps those two ideas physically separate by leaving the frame ruler on the left while individual codons move one at a time into the center wall.",
  "The first sample codon lights an amino-acid tray. Another codon triggers a STOP panel instead of an amino acid. Sora names the relationship **codon specifies amino acid** with one important qualification. A codon specifies an amino acid or a translation stop signal, and amino-acid identity can be determined using a genetic-code chart. The wall is read using **mRNA codons**, so if a DNA sequence is provided in another problem, it first has to be interpreted correctly with respect to strand identity and RNA sequence. The chart is not a machine that converts any arbitrary DNA triplet directly into an amino acid without that reasoning.",
  "On the right, three different codon cards all slide into the same amino-acid tray. Sora does not call the code ambiguous. Each displayed codon has a defined instruction, yet more than one codon can specify the same amino acid. She labels this **genetic-code redundancy**. Many amino acids are encoded by more than one codon. Redundancy helps explain why two different codons can lead to the same amino-acid identity. It does not mean that a single codon normally has several unrelated meanings at once.",
  "Finally, the organism panels illuminate. Bacterium, plant, fungus, and animal examples all interpret the same sample codons the same way. Sora labels the pattern **near universality of genetic code**. Nearly all living organisms use the same genetic code, which supports common ancestry. She deliberately leaves a tiny exception marker at the edge of the display so the phrase does not become the inaccurate claim that the code is absolutely universal without exception. The broad conservation is the biological pattern that matters.",
  "The wall can now tell the assembly hall what amino acid each codon calls for, but no amino acid can travel by itself to the correct codon. A row of tRNAs waits at the far door, each with an exposed anticodon and an empty amino-acid attachment end. Sora points to a charging dock beyond them. The code has supplied the instruction. The next problem is making sure the courier carries the correct cargo before it ever reaches the ribosome."
 ]},
'U6-L24':{
 'title':'The Courier Must Be Loaded Before It Can Read the Address',
 'kicker':'A tRNA can deliver the amino acid specified by a codon only after the correct amino acid has been attached to that tRNA.',
 'paragraphs':[
  "The **tRNA Charging Dock** is narrower than the code gallery and much more mechanical. On your **left**, free amino acids sit in separate trays beside matching enzyme stations. Directly **ahead**, the center charging dock holds one real tRNA at a time, with its amino-acid attachment end raised and its anticodon exposed at the opposite end. On your **right**, a lit delivery route runs toward the ribosome, where the unchanged red mRNA waits behind glass with its codons still fixed in the same reading frame. Sora stops a tRNA from entering the delivery lane because its upper attachment end is empty. The anticodon alone is not cargo. A courier must first be loaded with the correct amino acid.",
  "An enzyme at the left station recognizes the tRNA and its appropriate amino acid. The enzyme attaches that amino acid to the tRNA, producing a charged tRNA. Sora names the enzyme **aminoacyl-tRNA synthetase** only after the loading reaction has been shown. Aminoacyl-tRNA synthetases attach the correct amino acids to their corresponding tRNAs, producing charged tRNAs. The exact enzyme name is additional detail, but the mechanism protects a crucial idea. The ribosome does not inspect a free amino-acid label and decide whether it fits the codon. Accuracy depends in part on the tRNA having been charged correctly before codon recognition at the ribosome.",
  "Sora sends the charged tRNA along the right-hand route. At the ribosome, its anticodon can pair with a complementary mRNA codon while the amino acid remains attached at the other end. She then names the courier’s job **tRNA delivers amino acid**. tRNA brings the amino acid specified by the mRNA codon to the ribosome. The wording specified by the codon describes the information relationship, while the physical amino acid attached to the tRNA reflects the earlier charging step. The same molecule connects two forms of information through two different ends. Its anticodon recognizes the mRNA sequence, and its attached amino acid contributes to the polypeptide.",
  "To keep the roles distinct, Sora places three objects in a straight line. On the left is the charging enzyme with a free amino acid. In the middle is the tRNA. On the right is the mRNA codon at the ribosome. The **aminoacyl-tRNA synthetase** loads the tRNA before delivery. The **tRNA anticodon** later pairs with the codon. The **amino acid** rides as cargo. Neither the synthetase nor the anticodon is the amino acid itself, and a codon is not physically converted into an amino acid. Information in the codon is translated through the adaptor system.",
  "A bank of correctly charged tRNAs now waits beside the red mRNA. The assembly hall finally has a readable message and properly loaded couriers. Yet the ribosome floor ahead still has three unlabeled positions, and tRNAs are trying to enter, hold the growing chain, and leave through the same opening. Sora carries the first charged tRNA toward the **Ribosome A–P–E Platform**, where the ribosome must organize traffic before elongation can proceed."
 ]},
'U6-L25':{
 'title':'Three Ribosome Bays Keep the Couriers From Colliding',
 'kicker':'A, P, and E are functional tRNA-binding positions within the ribosome, not names for ribosomal subunits.',
 'paragraphs':[
  "The red mRNA threads through a large ribosome model at the center of the next room. On your **left**, a charged tRNA waits beside a slot marked **A**. Directly **ahead**, the broad center platform is marked **P** and holds the tRNA associated with the growing peptide. On your **right**, an empty tRNA is aligned with a slot marked **E**, beside a small contextual panel comparing bacterial and eukaryotic ribosomes. The mRNA still carries the same highlighted start codon and unchanged triplet spacing. Sora positions you at the end of the platform so the three letters remain left to right in a stable order. Nothing moves until each tRNA has a distinct place to go.",
  "She begins with the small size panel because one incorrect label would corrupt the geometry. A bacterial ribosome is **70S**, assembled from 30S and 50S subunits. A eukaryotic cytosolic ribosome is **80S**, assembled from 40S and 60S subunits. Sora calls these **ribosomal subunit sizes** and then folds the panel partly closed. The S values are Svedberg sedimentation values, so they are not ordinary additive mass units. This size detail provides context for different ribosome types, but it is not the same thing as the A, P, and E positions that organize tRNAs during elongation.",
  "Now she opens the three bays. A charged aminoacyl-tRNA whose anticodon matches the next mRNA codon enters the **A site** on your left. The tRNA carrying the growing polypeptide occupies the **P site** in the center. After a tRNA has transferred its amino-acid contribution and is no longer carrying the growing chain, it can move toward the **E site** and exit on your right. Only after the three positions are occupied does Sora name the arrangement **ribosomal A, P, and E sites**. The large ribosomal subunit contains functionally defined A, P, and E tRNA-binding sites that organize tRNA entry, peptide-chain transfer, and exit during elongation.",
  "The room makes one distinction deliberately hard to forget. The letters A, P, and E are not ribosomal subunits. They are functional binding sites within the ribosome. The 30S, 50S, 40S, and 60S labels belong to the subunit-size context panel. A, P, and E belong to tRNA traffic. Sora also keeps the term **tRNA delivers amino acid** separate from the platform itself. The tRNA is the courier. The A/P/E sites organize where that courier sits at different moments. The ribosome then performs the chemistry and movement needed to extend the polypeptide.",
  "Sora covers the platform labels for an optional Quick Recall. The charged incoming tRNA was on the left, the peptide-bearing tRNA in the center, and the exiting uncharged tRNA on the right. When the labels return, A, P, and E snap back over those positions. A conveyor belt beyond the P site begins moving one codon at a time. The bays are now organized, but the polypeptide has not yet gained its next amino acid. The next room will show exactly how codon recognition, peptide-bond formation, and translocation repeat as one elongation cycle."
 ]},
'U6-L26':{
 'title':'The Conveyor Advances Exactly Three Bases at a Time',
 'kicker':'Elongation couples codon recognition, peptide-bond formation, and translocation while preserving the reading frame.',
 'paragraphs':[
  "The **Polypeptide Elongation Conveyor** extends the ribosome platform into a long transparent assembly line. On your **left**, the next charged tRNA hovers beside an exposed mRNA codon while its anticodon waits to pair. Directly **ahead**, the center conveyor holds the ribosome with the growing polypeptide attached to the tRNA in the P position. On your **right**, the mRNA track continues to the next codon under a ruler marked in three-base steps. The same red message runs unbroken through the entire apparatus. Sora clips her compass tablet to the mRNA so the reading direction and triplet spacing remain fixed. The only way forward is one codon at a time.",
  "The first event is recognition. The incoming charged tRNA enters the A position only when its anticodon can pair appropriately with the exposed mRNA codon. Sora leaves the codon and anticodon side by side long enough to separate recognition from peptide chemistry. The base-pairing interaction selects the appropriate tRNA for that codon. The amino acid was already attached during the charging step in the previous room. Codon recognition therefore does not create the amino acid or charge the tRNA. It positions a correctly charged tRNA for the next stage of translation.",
  "At the center conveyor, the growing polypeptide is transferred so a new **peptide bond** forms as the chain gains the amino acid carried by the incoming tRNA. Sora names the overall growth process **polypeptide elongation**. During elongation, amino acids are transferred to the growing polypeptide chain as peptide bonds form. The chain’s amino-acid order is therefore tied to the sequence of codons encountered in the fixed reading frame. The mRNA remains unchanged as a template for reading; the growing product is the polypeptide.",
  "Then the entire ribosome advances by one codon. The mRNA ruler moves exactly three nucleotides relative to the decoding positions. tRNAs shift through the ribosomal sites as the next codon enters the A position. Sora names the combined relationship **codon recognition and translocation**. During elongation, codon–anticodon recognition positions the incoming tRNA, peptide-bond formation transfers the growing chain, and translocation advances the ribosome and tRNAs along the mRNA. The steps are connected, but they are not interchangeable. Recognition identifies the incoming adaptor, peptide-bond chemistry lengthens the chain, and translocation moves the machinery to the next codon.",
  "The conveyor repeats the cycle. Match, transfer, move. Match, transfer, move. Each time, the growing polypeptide gains amino acids in the order encoded by the mRNA, while the original reading frame remains unchanged. Sora briefly points back to the protein concepts you already know. The chain being produced has a primary amino-acid sequence, and that sequence will influence later folding. She does not create a new mnemonic for peptide bonds or protein structure here; the purpose of this room is to show how translation generates that sequence from codon order.",
  "After several cycles, a red warning panel appears on the right-hand track. The next codon is not mapped to an amino-acid tray. It is a stop instruction. The conveyor cannot continue by loading another ordinary aminoacyl-tRNA. Sora locks the completed codon-by-codon history into her ledger and follows the mRNA into the **Stop and Release Dock**, where translation must end without inventing a stop-codon amino acid."
 ]},
'U6-L27':{
 'title':'The Last Codon Has No Amino-Acid Cargo',
 'kicker':'A stop codon ends translation by recruiting termination machinery, after which the polypeptide is released and can continue folding.',
 'paragraphs':[
  "The red mRNA enters the final translation dock with its reading frame still intact. On your **left**, the next triplet sits under a bright **STOP** sign. Directly **ahead**, the center termination dock holds the ribosome and the nearly complete polypeptide. On your **right**, a folding area contains an open space for the released chain, with optional chaperone and processing stations farther back. Sora leaves the AUG start marker visible at the far beginning of the mRNA so the journey now has two different landmarks. AUG established where translation began. The stop codon marks where the ribosome must stop adding amino acids. The two signals cannot be treated as the same kind of instruction.",
  "The ribosome advances until the stop codon reaches the decoding position. Sora names the first relationship **translation continues to stop codon**. The ribosome advances along the mRNA until a stop codon is reached. A stop codon is still part of the mRNA reading frame, but it does not specify another amino acid to extend the chain. The red message has therefore carried the ribosome from the start gate to a defined endpoint without the frame changing in between.",
  "No amino-acid-carrying tRNA enters for the stop signal. Termination machinery, including a release factor, occupies the relevant decoding position and promotes release of the completed polypeptide. Sora labels this **stop codons and release**. Stop codons do not encode amino acids; termination machinery promotes release of the completed polypeptide and ribosomal complex disassembly. This distinction protects against a common mental shortcut. There is no special stop amino acid and no stop-codon tRNA delivering one. The stop instruction changes what the translation machinery does.",
  "The chain detaches from the translation complex and the ribosomal components separate from the mRNA. Only after the product is physically free does Sora name **translation termination releases product**. Translation terminates with release of the newly synthesized polypeptide or protein product and disassembly of the translation complex. The wording product does not mean every newly released chain is instantly a fully functional protein. Translation has completed the amino-acid sequence, while later structure and processing can still matter for function.",
  "On the right, the released chain is already beginning to fold. Some regions acquired local structure while synthesis was still occurring, and additional folding continues after release. Sora names this **protein folding during and after translation**. A nascent polypeptide begins folding during and after synthesis, and some proteins require chaperones or additional processing or modification to reach functional form. The folding station therefore follows translation without being confused with termination itself. Release ends the ribosome’s synthesis of the chain. Folding and other maturation processes determine what happens to that chain afterward.",
  "For the optional Quick Recall, Sora covers the stop sign and asks what event the ribosome had to reach before release could occur. When the cover lifts, the stop codon is still on the mRNA and the completed polypeptide is still on the right. A side door then opens in the wall with an arrow that seems to point the wrong way, from RNA back toward DNA. Sora leaves the normal translation route intact behind you and walks to the **Retroviral Reverse-Flow Gate**. The next scene is not another translation stage. It is a separate biological information-flow case that must remain distinguishable from the DNA-to-RNA-to-polypeptide route you just completed."
 ]},
'U6-L28':{
 'title':'The Side Gate Where RNA Is Copied Back Into DNA',
 'kicker':'Retroviruses use reverse transcriptase to make DNA from RNA, after which viral DNA can integrate into the host genome and re-enter ordinary transcription and translation routes.',
 'paragraphs':[
  "The last room is deliberately set apart from the assembly line. Behind you, the completed red mRNA and released polypeptide remain visible through glass as a frozen record of the usual protein-coding route. On your **left**, a separate **silver retroviral RNA** genome enters through a sealed viral-input hatch. Directly **ahead**, the center **reverse-transcription gate** contains an enzyme dock and a growing DNA strand. On your **right**, the new DNA product faces a host-chromosome model and an integration route. Sora places her copper ledger between the two pathways so the ordinary red mRNA is never mistaken for the incoming viral genome. The direction of information in this room is different from transcription, and the physical separation makes that difference visible before she names it.",
  "A real enzyme binds the retroviral RNA template and begins synthesizing complementary DNA. Sora waits until the DNA product is visibly growing before naming the process **retroviral reverse transcription**. In retroviruses, reverse transcriptase copies viral RNA into DNA. This is RNA-to-DNA information transfer. It does not mean that a viral DNA product somehow becomes part of RNA, and it does not reverse translation by converting a protein back into RNA. The substrate in front of you is RNA, and the newly synthesized nucleic-acid product is DNA.",
  "The DNA product then moves to the right toward host DNA. The host chromosome opens at an integration site, and the viral DNA is placed into host-genome context. From that DNA state, viral genes can later be transcribed into RNA and translated to make viral proteins, contributing to production of new viral progeny. Sora traces the full route with one finger. Retroviral RNA can be copied into DNA, the DNA can integrate into the host genome, and information from that DNA can later travel through transcription and translation. Reverse transcription is therefore an additional route into DNA, not a replacement for the downstream transcription and translation mechanisms you already learned.",
  "She turns both pathways on at once. Behind the glass, the normal protein-coding gene followed DNA to RNA to polypeptide. In front of you, the retroviral example begins with RNA and uses reverse transcriptase to generate DNA before viral information can enter the host-genome route. The two pathways share later transcription and translation steps, but their starting direction differs. Keeping them side by side prevents the phrase central dogma from becoming a rigid arrow that erases known biological mechanisms.",
  "The hall powers down one station at a time. You can now reconstruct the entire translation route from geography to product. A mature mRNA reaches a ribosome in the appropriate cellular context. AUG establishes the reading frame. Codons are interpreted through the genetic code. Correctly charged tRNAs carry amino acids. A, P, and E sites organize tRNA traffic. Elongation repeats codon recognition, peptide-bond formation, and translocation. A stop codon recruits termination machinery rather than another amino-acid tRNA. The polypeptide is released and continues folding. Off to the side, the retroviral gate remains a distinct RNA-to-DNA mechanism. Sora closes the copper ledger only when every arrow can be rebuilt from the actual molecules that moved through the rooms."
 ]},
}

BEAT_IMAGES={
 'U6-K-031':'the split floor map with eukaryotic cytosolic/rough-ER ribosomes left and an open prokaryotic translation space right',
 'U6-K-032':'the bacterial ribosome binding an mRNA while RNA polymerase is still transcribing that same RNA',
 'U6-K-033':'the three connected stations initiation → elongation → termination',
 'U6-K-034':'the glowing AUG gate where the initiator tRNA positions methionine and fixes the start',
 'U6-K-121':'the three offset triplet grids showing that a one-base shift changes every downstream grouping',
 'U6-K-035':'the fixed three-nucleotide blocks bracketed along the red mRNA',
 'U6-K-036':'the genetic-code wall mapping one mRNA codon to an amino acid or stop instruction',
 'U6-K-037':'several different codon cards converging on the same amino-acid tray',
 'U6-K-038':'many organism panels interpreting the same codons with a small exception marker at the edge',
 'U6-K-039':'the charged tRNA carrying its amino acid toward a complementary mRNA codon at the ribosome',
 'U6-K-130':'the aminoacyl-tRNA synthetase loading the correct amino acid onto the corresponding tRNA before delivery',
 'U6-K-131':'the small contextual panel comparing bacterial 30S+50S=70S and eukaryotic 40S+60S=80S ribosomes',
 'U6-K-132':'the ribosome platform with charged tRNA entering A, peptide-bearing tRNA in P, and empty tRNA exiting E',
 'U6-K-040':'the growing polypeptide gaining one amino acid as a peptide bond forms at the center conveyor',
 'U6-K-133':'the repeat cycle codon recognition → peptide transfer → one-codon translocation',
 'U6-K-041':'the unchanged reading frame carrying the ribosome forward until a stop codon reaches the decoding position',
 'U6-K-042':'the completed polypeptide releasing from the ribosome as the translation complex disassembles',
 'U6-K-134':'the stop codon recruiting termination machinery instead of an amino-acid-carrying tRNA',
 'U6-K-135':'the released chain continuing to fold beside optional chaperone and processing stations',
 'U6-K-045':'the silver retroviral RNA passing through reverse transcriptase to become DNA that moves toward host-genome integration',
}

CHECKPOINTS={'U6-L22','U6-L25','U6-L27'}

def word_count(pars): return len(re.findall(r"\b[\w’′'-]+\b",' '.join(pars)))

def zone_objs(lid):
    return [{'position':p,'label':label,'symbol':sym,'description':desc} for p,label,sym,desc in ZONES[lid]]

def cast_for(lid):
    items=[{'name':'Dr. Sora Han','kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    for p,label,sym,desc in ZONES[lid]:
        items.append({'name':label,'kind':'scientific anchor','visual':f'{sym} · {desc}','job':B[lid]['spatial_layout'][p]['layout_job']})
    items.append({'name':'Persistent mature mRNA and polypeptide','kind':'continuity object','visual':'one red mature mRNA with highlighted AUG and fixed codon spacing plus one growing polypeptide whose amino-acid order changes only when the ribosome advances by one codon','job':'keeps sequence, reading frame, ribosome position, and product order traceable across all eight scenes; it never substitutes for a biological term'})
    return items

def beats_for(lid):
    out=[]; terms={t['knowledge_id']:t for t in B[lid]['term_introductions']}
    for kid in B[lid]['knowledge_ids']:
        t=terms[kid]; c=CANON[kid]
        out.append({'object_id':kid,'term':t['canonical_term'],'story':BEAT_IMAGES[kid],'science':c['canonical_verified_statement'],'exact_name':bool(t['exact_name_recall']),'hint':BEAT_IMAGES[kid],'name_support':t['name_support'],'reactivation_mode':t['reactivation_mode'],'scope_class':t['scope_class']})
    return out

scenes=[]
for i,lid in enumerate(J3['route']):
    b=B[lid]; n=NARR[lid]; r=ROUTE[i]; pars=n['paragraphs']; cp=lid in CHECKPOINTS
    scenes.append({
      'scene_index':i,'locus_id':lid,'locus':r['locus'],'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['micro_anchor'],'scene_layout':{'orientation':b['orientation_sentence'],'zones':zone_objs(lid)},
      'cast':cast_for(lid),'continuity_object':J3['continuity_object'],'story_open':pars[0],'story_paragraphs':pars,'story_close':pars[-1],
      'object_ids':list(b['knowledge_ids']),'story_beats':beats_for(lid),'prior_unit_reactivation':b['prior_unit_reactivation'],'misconception_guards':b['misconception_guards'],
      'checkpoint':cp,'checkpoint_object_id':b['primary_knowledge_id'] if cp else None,'checkpoint_prompt':b['quick_recall']['candidate_prompt'] if cp else '', 'checkpoint_answer':b['quick_recall']['answer'] if cp else '',
      'next_locus':ROUTE[i+1]['locus'] if i+1<len(ROUTE) else None,'f3_scene_brief_id':b['scene_brief_id'],'narrative_word_count':word_count(pars)
    })

journey={
 'palace_id':'U6-J3','unit_id':'unit-6','palace_name':'Translation Assembly Hall','story_title':'The Assembly Line That Lost Its Reading Frame',
 'tagline':'A mature mRNA has reached the hall intact, but no protein can be built until the start position, codon code, charged tRNAs, ribosome traffic, elongation cycle, and stop logic all agree.',
 'guide':GUIDE,
 'premise':'The mature red mRNA from the previous journey arrives at the Translation Assembly Hall with its sequence intact, AUG highlighted, and triplet spacing visible, yet the assembly line has lost the rules that turn the message into an ordered polypeptide. Ribosomes have been routed without regard to cellular geography, the reading frame can slide, tRNAs are arriving unloaded, the A/P/E positions are mixed together, and the stop signal is being treated as though it should recruit another amino acid. Dr. Sora Han must keep the same mRNA and one growing polypeptide identifiable while each part of translation is restored in causal order.',
 'mission':'Carry one mature mRNA from the correct cellular translation site through start-codon recognition, reading-frame locking, codon interpretation, tRNA charging and delivery, ribosomal A/P/E organization, repeated elongation, and termination. Preserve the same mRNA sequence and triplet spacing while the polypeptide grows only when the ribosome advances by one codon, then keep retroviral reverse transcription physically separate as an RNA-to-DNA information-flow case rather than confusing it with ordinary translation.',
 'finale':'The ribosome reaches a stop codon without inventing a stop amino acid, termination machinery releases the completed polypeptide, and the chain continues folding while the original mRNA remains intact. Through a separate side gate, retroviral RNA is copied into DNA by reverse transcriptase and routed toward host-genome integration. The learner can reconstruct both routes from real molecular direction and function, with the ordinary translation pathway preserved from mature mRNA to amino-acid sequence.',
 'estimated_minutes':25,'scene_count':8,'checkpoint_count':3,'student_release':'DEVELOPER_PREVIEW_F4C','preview_release':True,'narrative_design':'U6-F4C-NARRATIVE-1.0',
 'learner_rule':'Read or listen and first place yourself in each left/center/right room. Follow the same mature red mRNA and growing polypeptide through all eight locations. Exact terms are attached to real structures and actions only after their defining relationship is visible. Optional Quick Recall appears only three times.',
 'route_orientation':'This is one continuous eight-location route through the Translation Assembly Hall. Enter at the Translation Geography Platform, lock the reading frame at AUG, decode triplets at the Codon Code Wall, charge tRNAs at the courier dock, organize A/P/E traffic at the ribosome platform, repeat elongation on the conveyor, terminate at the stop-and-release dock, and finish at the separate Retroviral Reverse-Flow Gate. The same mature red mRNA and growing polypeptide remain reconstructable throughout the ordinary translation route.',
 'route':ROUTE,'scenes':scenes,'source_brief_lock':'LOCKED_F3','scientific_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2'
}

(U6/'journeys').mkdir(exist_ok=True)
(U6/'journeys'/'U6-J3.json').write_text(json.dumps(journey,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
j1=json.loads((U6/'journeys'/'U6-J1.json').read_text(encoding='utf-8'))
j2=json.loads((U6/'journeys'/'U6-J2.json').read_text(encoding='utf-8'))
summary={'schema':'memory-palace-v2-unit6-f4c-journeys-1.0','unit_id':'unit-6','stage':'F4C','student_release':False,'preview_release':True,'journey_count':3,'scene_count':28,'checkpoint_count':j1['checkpoint_count']+j2['checkpoint_count']+journey['checkpoint_count'],'guided_journeys':[{k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']} for j in [j1,j2,journey]]}
(U6/'journeys-f4c.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

status={'unit_id':'unit-6','number':6,'title':'Gene Expression and Regulation','status':'F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','pipeline_stage':'F4C_JOURNEY3_NARRATIVE','canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','narrative_lock':'LOCKED_F4C_J1_J3','student_release':False,'preview_release':True,'journey_count':3,'scene_count':28,'memory_objects':0,'application_challenges':0,'canonical_records':202,'architecture_journeys':6,'architecture_loci':53,'scene_briefs':53,'palace_managed_records':161,'challenge_lab_records':16,'scope_guard_records':25,'exact_name_review_targets':134,'confusable_sets':37,'optional_first_exposure_recalls':18,'f4a_journey':'U6-J1','f4a_scene_count':12,'f4b_journey':'U6-J2','f4b_scene_count':8,'f4c_journey':'U6-J3','f4c_scene_count':8,'f4c_knowledge_records':20,'f4c_optional_recalls':3,'next_required_output':'F4D polished narrative for Journey 4 only after Journeys 1–3 remain frozen and all prior prose-quality gates continue to pass.'}
(U6/'status-f4c.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); (U6/'status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
cp=ROOT/'content'/'ap-biology'/'course.json'; course=json.loads(cp.read_text(encoding='utf-8')); u=next(x for x in course['units'] if x['unit_id']=='unit-6'); u.update({'status':'F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','journey_count':3,'scene_count':28,'student_release':False,'preview_release':True,'source_status':'AUDITED_F1_ARCHITECTURE_F2_BRIEFS_F3_NARRATIVE_F4C','narrative_lock':'LOCKED_F4C_J1_J3','narrative_journeys':3}); cp.write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

doc=['# Unit 6 F4C · Journey 3 Narrative','','## The Assembly Line That Lost Its Reading Frame','',journey['tagline'],'','### Route','', ' → '.join(x['locus'] for x in ROUTE),'']
for s in scenes:
    doc += [f"## {s['scene_index']+1}. {s['locus']} · {s['title']}",'',f"*{s['scene_kicker']}*",'']+s['story_paragraphs']+['']
    if s['checkpoint']: doc += ['**Optional Quick Recall**','',s['checkpoint_prompt'],'']
(ROOT/'docs'/'UNIT6_F4C_JOURNEY3_STORY.md').write_text('\n'.join(doc),encoding='utf-8')

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
locked_rel=['journeys/U6-J1.json','journeys/U6-J2.json','journeys/U6-J3.json','journeys-f4c.json','status-f4c.json']
lock_files={rel:{'bytes':(U6/rel).stat().st_size,'sha256':sha(U6/rel)} for rel in locked_rel}
lock={'schema':'memory-palace-v2-unit6-f4c-lock-1.0','unit_id':'unit-6','lock_status':'LOCKED_F4C_J1_J3','student_release':False,'preview_release':True,'protected_prior_locks':['content-lock-f1.json','content-lock-f2.json','content-lock-f3.json','content-lock-f4a.json','content-lock-f4b.json'],'frozen_f4a_journey_sha256':sha(U6/'journeys/U6-J1.json'),'frozen_f4b_journey_sha256':sha(U6/'journeys/U6-J2.json'),'journey_ids':['U6-J1','U6-J2','U6-J3'],'scene_count':28,'new_journey_scene_count':8,'new_journey_knowledge_record_count':20,'new_journey_checkpoint_count':3,'files':lock_files,'rule':'Journeys 1 and 2 remain byte-frozen from F4A/F4B. Journey 3 polished prose may not change after F4C without a new explicit narrative version. F1 science, F2 classification/geometry, and F3 briefs remain authoritative boundaries.'}
(U6/'content-lock-f4c.json').write_text(json.dumps(lock,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
release={'schema':'memory-palace-v2-unit6-f4c-release-1.0','generated_utc':'2026-09-08T02:15:00+00:00','unit_id':'unit-6','release_status':'F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','student_release':False,'preview_release':True,'journeys':3,'scenes':28,'new_journey_id':'U6-J3','new_journey_scenes':8,'new_journey_knowledge_records':20,'new_journey_optional_first_exposure_recalls':3,'canonical_records':202,'permanent_loci_architecture':53,'scene_briefs':53,'memory_objects':0,'application_challenges':0,'scientific_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','narrative_lock':'LOCKED_F4C_J1_J3','next_stage':'F4D Journey 4 polished narrative after F4A/F4B/F4C regression'}
(U6/'f4c-release-manifest.json').write_text(json.dumps(release,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'journey':'U6-J3','scenes':8,'knowledge_records':20,'checkpoints':3,'words':sum(s['narrative_word_count'] for s in scenes),'min_words':min(s['narrative_word_count'] for s in scenes),'max_words':max(s['narrative_word_count'] for s in scenes)},indent=2))
