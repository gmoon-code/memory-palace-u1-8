from __future__ import annotations
import json, hashlib, re, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'
# Rebuild F4A first so F4B always starts from the locked Journey 1 baseline.
subprocess.run([sys.executable,str(ROOT/'scripts'/'build_unit5_f4a.py')],check=True,stdout=subprocess.DEVNULL)
F3=json.loads((U5/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS=json.loads((U5/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J2=next(j for j in JBRIEFS if j['journey_id']=='U5-J2')
B={b['locus_id']:b for b in F3 if b['journey_id']=='U5-J2'}
CANON={r['knowledge_id']:r for r in json.loads((U5/'source'/'canonical-unit5-f1.json').read_text(encoding='utf-8'))['canonical_catalog']}
J1=json.loads((U5/'journeys'/'U5-J1.json').read_text(encoding='utf-8'))

GUIDE={
 'name':'Dr. Imani Reyes','role':'inheritance-systems geneticist',
 'visual':'deep-green field coat, clear gloves, compact chromosome tablet using blue for one parental homolog and amber for the other, plus the same narrow gold generation ledger from Journey 1',
 'story_job':'Imani keeps chromosome identity, chromosome-set number, chromatid state, spindle attachment, and division number visible. She changes the chromosome model first and names each meiotic phase or relationship only after the defining movement can be seen.'
}

route=[
 {'scene_index':0,'locus':'Premeiotic Loading Bay','short':'Replicate','floor':'Entry level','symbol':'S'},
 {'scene_index':1,'locus':'Prophase I Pairing Chamber','short':'Pair & cross','floor':'Division I','symbol':'X'},
 {'scene_index':2,'locus':'Metaphase I Orientation Platform','short':'Orient pairs','floor':'Division I','symbol':'↕'},
 {'scene_index':3,'locus':'Anaphase I Separation Track','short':'Split homologs','floor':'Division I','symbol':'← →'},
 {'scene_index':4,'locus':'Telophase I Haploid Landing','short':'Haploid','floor':'Division I exit','symbol':'n | n'},
 {'scene_index':5,'locus':'Interdivision No-Replication Gate','short':'No copy','floor':'Interdivision','symbol':'NO S'},
 {'scene_index':6,'locus':'Prophase II Restart Bay','short':'Restart','floor':'Division II','symbol':'II'},
 {'scene_index':7,'locus':'Metaphase II Alignment Rail','short':'Align singles','floor':'Division II','symbol':'—'},
 {'scene_index':8,'locus':'Anaphase II Sister Split','short':'Split sisters','floor':'Division II','symbol':'↔'},
 {'scene_index':9,'locus':'Four-Cell Meiosis Exit','short':'Four haploid','floor':'Exit hall','symbol':'4n'},
]

# Story-facing concrete images stay subordinate to conventional chromosome geometry.
BEAT_IMAGES={
'U5-K-055':'the blue and amber homologs passing through the S-phase loader and leaving as duplicated chromosomes with joined sister chromatids while the chromosome-set counter does not change',
'U5-K-002':'the paired blue and amber replicated homologs inside the prophase-I chamber while the spindle begins forming and the nuclear envelope opens',
'U5-K-012':'one blue nonsister chromatid and one amber nonsister chromatid exchanging corresponding DNA segments inside the paired homologs',
'U5-K-056':'the replicated homologs fastening side by side along matching loci during synapsis',
'U5-K-057':'the four-chromatid unit made by two replicated homologous chromosomes paired together as one tetrad',
'U5-K-058':'the visible chiasma where the homologs remain connected after crossover',
'U5-K-003':'the homologous chromosome pairs aligned together at the first metaphase plate',
'U5-K-060':'the large and small homolog pairs choosing their maternal/paternal orientations independently at metaphase I',
'U5-K-004':'the blue homolog moving to one pole and the amber homolog moving to the opposite pole while each keeps its two sister chromatids joined',
'U5-K-005':'the first meiotic division completing into two daughter cells as the spindle breaks down and cytokinesis separates the cells',
'U5-K-063':'the two daughter cells marked n even though every chromosome is still visibly duplicated as two sister chromatids',
'U5-K-062':'the locked interdivision gate carrying duplicated chromosomes directly into meiosis II without another S phase or DNA replication',
'U5-K-006':'a new spindle forming in each haploid cell around already-duplicated chromosomes with no homolog synapsis',
'U5-K-007':'individual duplicated chromosomes aligned at the metaphase-II plate with sister kinetochores facing opposite poles',
'U5-K-008':'the centromeric sister connection releasing so sister chromatids move to opposite poles in anaphase II',
'U5-K-001':'the completed route ending in four haploid products after two meiotic divisions',
'U5-K-009':'telophase II and cytokinesis forming nuclei and separating the two meiosis-I cells into four haploid products with unduplicated chromosomes',
'U5-K-010':'the final side-by-side panel contrasting one mitotic division with two meiotic divisions, their cell numbers, chromosome-set outcomes, and genetic similarity',
}

NARR={
'U5-L06':{
 'title':'The Loading Bay That Doubled DNA Without Doubling the Set',
 'kicker':'Meiosis begins only after every chromosome has been copied, but copying DNA does not create another homologous chromosome set.',
 'paragraphs':[
  "The inner doors from the chromosome registry open into the **Premeiotic Loading Bay**, a long rectangular room built around one conveyor. On your **left**, the same blue and amber homologous chromosomes from the registry stand upright as single rods in an unreplicated-chromosome rack. Directly **ahead**, a glass S-phase loader spans the center lane, with DNA-copying tracks running along each chromosome. On your **right**, a second rack is shaped to hold duplicated chromosomes, each with two joined sister chromatids. Above all three stations, Imani’s gold ledger displays two separate gauges: CHROMOSOME SETS and DNA AMOUNT. The transit hall will not open until those gauges stop being treated as if they measured the same thing.",
  "Imani first keeps the chromosome identities fixed. The large blue homolog carries one set of locus labels; the large amber homolog carries the corresponding loci. A smaller blue-and-amber homolog pair appears on the lower line of her tablet so later you can see independent orientation across more than one chromosome pair. Nothing has duplicated yet. The cell is still diploid because it contains both homologous sets. Imani slides the chromosomes into the center loader and activates **premeiotic interphase**. During its S phase, DNA replication runs along every chromosome before meiosis I begins.",
  "The center machine does not manufacture a new blue homolog or a new amber homolog. It copies the DNA of each existing chromosome. When the large blue chromosome emerges on the right, it now consists of two nearly identical blue **sister chromatids** joined at the centromeric region. The amber homolog emerges the same way, and so does the smaller pair. The amount of DNA has increased and the number of chromatids has increased, yet the blue and amber homolog identities have not multiplied into extra chromosome sets. The ledger keeps the chromosome-set gauge at 2n while its DNA-content gauge rises.",
  "Imani makes you trace one centromere with your finger on the tablet. Before S phase, that centromere defined one chromosome. After replication, two sister chromatids remain joined as one duplicated chromosome until they later separate. This prevents a common error before it can enter the hall: seeing an X-shaped duplicated chromosome and counting its two chromatids as two homologous chromosomes. The homologous relationship still exists between the blue chromosome and the amber chromosome with corresponding loci. Replication created sisters within each homolog; it did not create another homologous partner.",
  "The loader powers down and a warning strip lights across the floor: ONE REPLICATION ONLY. Imani writes the state into the ledger: diploid cell, duplicated chromosomes, sister chromatids present, meiosis I not yet begun. She also leaves a blank line beneath it labeled BETWEEN I AND II. That blank will matter later, because DNA is **not replicated again between meiosis I and meiosis II**. For now, the duplicated blue and amber homologs are locked onto the same tablet rather than replaced by a fresh diagram.",
  "At the far end of the right rack, the duplicated homologs are too wide for the ordinary transit door. A chamber beyond it has four parallel chromatid slots and matching locus marks running side by side. The door opens only when homologous chromosomes approach as pairs. Imani lifts the tablet, keeps every sister connection visible, and leads the same duplicated blue and amber homologs into the Prophase I Pairing Chamber."
 ],
 'close':'Replication has created sister chromatids without changing chromosome-set identity. The duplicated homologs now enter Prophase I, where homologous partners will pair and nonsister chromatids can exchange DNA.'
},
'U5-L07':{
 'title':'Four Chromatids in the Pairing Chamber',
 'kicker':'Prophase I is the room where homologs find each other, pair, and exchange corresponding DNA through nonsister chromatids.',
 'paragraphs':[
  "The **Prophase I Pairing Chamber** is circular and easy to redraw. On your **left**, the duplicated blue and amber homologs enter on parallel rails, each chromosome still made of two joined sister chromatids. Directly **ahead**, the rails converge inside a brightly lit four-slot interaction table. On your **right**, a magnifying wall shows exchanged chromosome segments and one visible X-shaped contact point. The same large homolog pair remains on Imani’s tablet, while the smaller pair waits below it. No chromosome has been replaced. The problem in this room is relational: which chromosomes pair, which chromatids exchange DNA, and what names belong to the structures created by those actions?",
  "Imani brings the large blue homolog beside the large amber homolog and aligns their corresponding loci. This close pairing of homologous chromosomes during **prophase I** is **synapsis**. She deliberately leaves each chromosome’s two sister chromatids visibly attached. The paired unit therefore contains four chromatids in total. Once you can count those four chromatids, she names the whole paired structure a **tetrad**. A tetrad is not a different chromosome type and it is not the contact point itself; it is the four-chromatid structure formed by two replicated homologs paired together.",
  "The central table then selects one chromatid from the blue homolog and one from the amber homolog. They are not sisters, because they belong to different homologous chromosomes. Matching DNA regions line up, break, and reconnect so corresponding segments are exchanged. This is **crossing over**, or recombination, between **nonsister chromatids of homologous chromosomes**. The swapped segments remain conventional pieces of the real chromatids, colored with short blue-on-amber and amber-on-blue sections so you can trace where the DNA came from. The relationship **crossing over increases diversity** becomes visible because the chromatids can leave with new combinations of alleles along the same chromosome.",
  "After the exchange, the homologs do not instantly fly apart. Imani points to the visible place where the homologous chromosomes remain associated. That region is a **chiasma**. She makes you distinguish all three related names while the structures are still on screen: synapsis is the pairing process, the tetrad is the four-chromatid paired structure, and a chiasma is a visible association region after crossover. None of those words is a synonym for crossing over itself, which is the DNA-segment exchange between nonsister chromatids.",
  "Around the chamber, the rest of **prophase I** becomes visible without stealing attention from the defining pairing event. Chromosomes condense, centrosomes move apart, spindle organization begins, and the nuclear envelope breaks down. Imani keeps these events at the room’s perimeter while the paired homologs remain in the center. The phase is broader than crossing over, and crossing over can occur during prophase I; the memorable core is that homologous chromosomes uniquely pair here and may recombine before first-division alignment.",
  "The right magnifying wall now shows recombinant segments on two chromatids while sister relationships remain traceable. The chamber releases the homolog pair as a paired unit onto a moving platform. Before you step on, Imani asks the optional recall without showing the answer: during prophase I, which chromatids exchanged the corresponding DNA segments? Once you have attempted it, the platform carries the still-paired homologs toward the metaphase plate, where a different source of diversity will depend on how whole homolog pairs face the poles."
 ],
 'close':'Synapsis and crossing over have altered chromatid combinations while homologs remain paired. Those intact homolog pairs move next to the Metaphase I Orientation Platform.'
},
'U5-L08':{
 'title':'The Platform Where Homolog Pairs Choose Sides',
 'kicker':'At metaphase I, the unit that aligns is the homologous pair, and each pair can face the poles independently of the others.',
 'paragraphs':[
  "The moving floor stops inside the **Metaphase I Orientation Platform**, a long chamber with two spindle poles. On your **left**, the large blue-and-amber homolog pair waits on a rotating mount. Directly **ahead**, a bright metaphase plate cuts across the room, and paired homologs are positioned along it. On your **right**, the smaller blue-and-amber homolog pair sits on a second mount that can rotate without moving the large pair. The left and right mounts are deliberately independent. Imani places her tablet above the center line so the recombinant segments from prophase I remain visible on the same chromatids.",
  "Spindle fibers approach the large paired homologs from opposite poles. The blue homolog can face the left pole while the amber homolog faces the right, or the pair can be flipped so those directions reverse. The critical point is that the **homologous chromosome pair** aligns as the first-division unit. Sister chromatids within each duplicated chromosome stay joined. Once the pair is positioned at the metaphase plate, Imani names the phase **metaphase I**: spindle fibers align homologous chromosome pairs at the metaphase plate.",
  "She then leaves the large pair fixed and rotates only the smaller pair on the right. Its blue homolog now faces the opposite side from the large pair’s blue homolog. Nothing in the large pair forces that choice. Each homologous pair can orient independently of the others during metaphase I. Imani names this **independent orientation in metaphase I**. With many homolog pairs in a real diploid cell, independent orientation produces many possible combinations of parental-origin chromosomes in eventual gametes.",
  "The platform displays several possible orientations as ghost outlines, but only one actual state remains solid on the tracked chromosome tablet. That distinction keeps probability from replacing mechanism. Independent orientation is the physical fact that different homolog pairs can face the poles independently; later genetic combinations reflect those possible orientations. It is also different from crossing over, which already exchanged DNA segments between nonsister chromatids, and from random fertilization, which combines gametes later in the life cycle.",
  "Imani shifts the camera down the hall for a preview of metaphase II. There, individual duplicated chromosomes will align, because homologous partners will already have been separated. She immediately returns the view to this first platform: **metaphase I aligns homologous pairs**, while **metaphase II aligns individual duplicated chromosomes**. The paired-homolog geometry in front of you is the diagnostic feature to retrieve, not merely the Roman numeral in the name.",
  "The mounts lock. Once orientation is fixed, the platform can no longer rotate. The spindle tracks extending from the two poles begin pulling in opposite directions, but their release clamps are attached to homologous partners, not to the sister connection within each chromosome. Imani closes the orientation line in the ledger and follows the rails into Anaphase I, where the first division must separate the homologs while leaving every pair of sisters intact."
 ],
 'close':'Homolog-pair orientation is fixed at the first metaphase plate. The spindle now pulls homologous chromosomes toward opposite poles on the Anaphase I Separation Track.'
},
'U5-L09':{
 'title':'The First Separation: Homologs Leave, Sisters Stay',
 'kicker':'Anaphase I reduces the homologous set by separating homologs; it does not split sister chromatids.',
 'paragraphs':[
  "The **Anaphase I Separation Track** is a straight corridor with two destinations. On your **left**, one spindle pole glows blue-white. Directly **ahead**, the paired homologs sit at the center release line. On your **right**, the opposite pole glows amber-white. The large blue and amber homologs from the earlier rooms are still easy to identify because each remains a duplicated chromosome with two joined sister chromatids. The smaller pair is arranged the same way on a lower track. Imani locks the tablet view so no one can mistake a duplicated chromosome for two separate chromosomes during the pull.",
  "At the center line, the connection that keeps homologous partners together is released. The blue homolog begins moving toward the left pole while the amber homolog moves toward the right. The smaller homolog pair also separates according to the orientation fixed in metaphase I. Imani names the motion **anaphase I** only after the direction is visible: homologous chromosomes separate and move toward opposite poles.",
  "She magnifies the blue chromosome as it travels. Its two blue sister chromatids remain joined at the centromeric region. The amber chromosome on the opposite track also keeps its sisters together. This is the defining contrast: **anaphase I separates homologous chromosomes while sister chromatids remain attached**. The first meiotic division is therefore segregating homologous partners, not performing the sister split familiar from mitosis or from anaphase II.",
  "The gold ledger updates chromosome-set distribution rather than pretending DNA has vanished. Before the split, both homologs occupied one cell. As the homologs reach opposite poles, each future daughter-cell region receives one homolog from each pair. Because the homologous partners are being partitioned to opposite sides, the coming cells will contain one homologous chromosome set. Yet each chromosome is still duplicated. The chromosome-set reduction and the later sister separation are two distinct events spread across two divisions.",
  "Imani overlays a transparent anaphase-II silhouette for one second. In that later event, the sister connection itself will release and former sister chromatids will travel apart. She removes the overlay before it becomes a second scene. Here, in anaphase I, the visible travelers are still whole duplicated homologous chromosomes. The distinction is mechanical, not merely verbal: homolog separation now; sister-chromatid separation later.",
  "She also keeps one chromosome-count label attached to the centromeric region of the traveling blue homolog. Even though that chromosome has two chromatids, it still moves as one duplicated chromosome because the sisters remain joined. The first division changes which homologous set reaches each pole, not the sister relationship within each chromosome. That small count tag will stay with the chromosome until anaphase II actually releases the sisters.",
  "The blue and amber homologs reach opposite ends of the track, still X-like because their sisters remain joined. Cell boundaries begin rising around the two chromosome groups. Imani marks the ledger with FIRST DIVISION SEGREGATION COMPLETE and opens the landing doors. The next room must answer a question that often feels paradoxical: how can the two daughter cells already be haploid when every chromosome inside them is still duplicated?"
 ],
 'close':'Homologous chromosomes have reached opposite poles while sister chromatids remain joined. The two chromosome groups enter Telophase I, where haploid state must be separated from DNA content.'
},
'U5-L10':{
 'title':'Haploid, Yet Still Duplicated',
 'kicker':'After meiosis I, each daughter cell has one homologous set even though every chromosome still consists of two sister chromatids.',
 'paragraphs':[
  "The corridor opens onto the **Telophase I Haploid Landing**, which is split into three unmistakable zones. On your **left**, a new daughter-cell boundary surrounds the blue large homolog and the chromosome partners that traveled with it. On your **right**, a second daughter-cell boundary surrounds the amber homolog and its companion chromosomes. Directly **ahead**, a tall comparison display has two separate meters labeled CHROMOSOME-SET NUMBER and DNA CONTENT. Every chromosome drawn inside both cells is still duplicated as two joined sister chromatids. Imani places the gold ledger beneath the meters and refuses to let either reading substitute for the other.",
  "The first meiotic division finishes. Spindle structures break down, nuclear envelopes may reform, and the cell divides by cytokinesis. In an animal-cell example on the display, a cleavage furrow pinches the cell; beside it, a plant-cell example builds a cell plate. Imani identifies the broader stage as **telophase I and cytokinesis**. Those examples show two cellular mechanisms for cytokinesis, while the central genetic result is the same: homologous chromosomes have been partitioned into two daughter cells.",
  "Now she points at the chromosome-set meter. The blue and amber homologs that once occupied the same cell are no longer together. Each daughter cell contains only one homolog from each homologous pair, so each contains one chromosome set. Both cells are therefore **haploid, n**. Imani does not erase the sister chromatids to make the word haploid feel intuitive. She deliberately keeps every chromosome visibly duplicated.",
  "The DNA-content meter remains higher than it will be after meiosis II because each chromosome still contains two sister chromatids. This is the locked relationship called **chromosome-set number versus DNA content**. After meiosis I, the cells are haploid because homologous pairs have separated, even though each chromosome is still duplicated. Ploidy tells you how many homologous chromosome sets are present; it does not simply count DNA molecules or chromatids. A haploid cell can therefore contain duplicated chromosomes.",
  "Imani has you reconstruct the first division without phase names. Replication created sisters before meiosis I. Prophase I paired homologs and could recombine nonsisters. Metaphase I aligned homologous pairs. Anaphase I separated homologs while sisters stayed together. The current landing now holds two haploid cells with duplicated chromosomes. That sequence makes the word haploid a consequence of homolog separation instead of an arbitrary label pasted onto telophase I.",
  "A gate ahead begins scanning the cells. It detects duplicated chromosomes and incorrectly starts warming a new DNA-copying chamber. Imani shuts it down before it can open. The optional recall appears on the landing display: after meiosis I, are these cells haploid or diploid, and are their chromosomes replicated or unreplicated? Once you answer, she points to the locked gate. The next room exists precisely because haploid cells with duplicated chromosomes must enter meiosis II **without another round of DNA replication**."
 ],
 'close':'The first division has produced two haploid cells whose chromosomes are still duplicated. That state forces the route through a no-replication gate before meiosis II.'
},
'U5-L11':{
 'title':'The Gate With No Copy Machine',
 'kicker':'The interval between meiotic divisions carries duplicated chromosomes forward; it does not include another S phase.',
 'paragraphs':[
  "The **Interdivision No-Replication Gate** looks like a security checkpoint between two floors. On your **left**, the two haploid cells from telophase I wait with their duplicated chromosomes clearly visible. Directly **ahead**, a red gate is stamped NO S PHASE / NO DNA REPLICATION and has a disabled replication conveyor beside it. On your **right**, two entrances descend toward meiosis II, one for each haploid cell. Imani keeps the blue and amber chromosome histories on her tablet so you can see that the chromosomes entering the gate are the same duplicated chromosomes that survived meiosis I.",
  "The scanner initially sees two sister chromatids on each chromosome and interprets that duplication as a request to copy again. Imani stops the machine. Those sister chromatids were created once during the premeiotic S phase, before meiosis I. The second division does not require a second round of chromosome duplication. The cells pass through an interval often called interkinesis in some descriptions, but the relationship that must remain fixed is simpler and more important: **no DNA replication between meiosis I and II**.",
  "She moves one duplicated blue chromosome through the center gate without changing it. Its two sister chromatids remain joined. The corresponding amber homolog is already in the other haploid cell and travels through its own gate unchanged. Each cell still has one homologous set, so the cells remain haploid. Nothing at this checkpoint restores a homologous partner, doubles ploidy, or creates another pair of sisters.",
  "The blank line Imani left in the gold ledger back at the first loading bay is finally filled: BETWEEN I AND II — NO REPLICATION. Above it, the earlier line still reads PREMEIOTIC S PHASE — DNA REPLICATED ONCE. Seeing the two entries on the same page matters. The no-replication rule is not a random prohibition to memorize; it follows from the chromosome state. Meiosis II needs to separate the sisters that already exist, so copying the DNA again would create the wrong substrate for the second division.",
  "Imani asks you to compare the three quantities now visible. Chromosome-set number is n in each cell. Chromosomes are duplicated, meaning each still has two sister chromatids. DNA content is therefore greater than it will be in the final products. Those facts can coexist because chromosome-set number and DNA amount are different measurements. The gate preserves all three states unchanged while the cells move into the second-division floor.",
  "On the right, new spindle poles begin unfolding around each cell. There is no matching homolog beside the blue chromosome in its cell and no synapsis chamber ahead. The homologs were already separated in meiosis I. Imani follows the two cells down separate but parallel ramps into the Prophase II Restart Bay, where the machinery restarts around already-duplicated chromosomes rather than repeating the unique pairing events of prophase I."
 ],
 'close':'The duplicated chromosomes pass from meiosis I into meiosis II without another DNA replication event. New spindle machinery now forms around haploid cells whose homologs are already separated.'
},
'U5-L12':{
 'title':'The Second-Division Restart',
 'kicker':'Prophase II rebuilds spindle access around duplicated chromosomes in haploid cells without repeating synapsis, crossing over, or DNA replication.',
 'paragraphs':[
  "The two ramps enter parallel halves of the **Prophase II Restart Bay**. On your **left**, one haploid cell contains the duplicated blue homologs assigned to it after meiosis I. Directly **ahead**, a spindle-assembly frame unfolds around the chromosomes. On your **right**, microtubule-access ports open from opposite poles. A matching bay for the second haploid cell runs behind a glass divider, carrying the corresponding amber homologs. Imani keeps both cells on one tablet view so you remember that meiosis II is occurring in the two products of meiosis I, not in a restored diploid cell.",
  "The chromosomes are already duplicated. No S-phase loader appears in this room. The homologous partner of each chromosome is in the other cell, so there is no homologous pair available for synapsis or tetrad formation. Imani lets the chromosome structures remain condensed and visible while new spindle organization begins. Once this setup is observable, she names the stage **prophase II**.",
  "During prophase II, a spindle forms and the joined sister chromatids become accessible to spindle microtubules. The centromeric sister association is still intact. The cell remains haploid because it contains one homologous chromosome set, even though each chromosome has two chromatids. The defining task of this room is therefore preparation for sister separation, not a repeat of the first division’s homolog pairing.",
  "Imani briefly places a transparent prophase-I image beside the current bay. Prophase I had both homologous partners in the same cell, allowing synapsis, tetrads, crossing over, and visible chiasmata. Prophase II lacks that homolog-pair context. No new crossing over is introduced here, and no new DNA replication occurs. The similar word ‘prophase’ reflects that both stages prepare a division, but the chromosome relationships present in the cell are different.",
  "The spindle poles extend microtubules toward each duplicated chromosome. Imani keeps the sisters joined while arranging access from opposite sides. She updates the gold ledger with DIVISION II SETUP — n, DUPLICATED CHROMOSOMES, NO HOMOLOG PAIRS. The entry is deliberately compact enough to reconstruct without a paragraph of phase vocabulary.",
  "On the mirrored panel, the second haploid cell performs the same restart independently. The amber homolog there does not somehow rejoin the blue homolog in the first cell. This parallel layout matters because meiosis II consists of two simultaneous second divisions, each operating on a haploid chromosome set inherited from meiosis I. The two cells share the same phase name, but they do not merge their chromosomes back into one cell.",
  "As soon as the spindle is ready, the center floor turns into a narrow alignment rail. Each duplicated chromosome moves toward it alone. No amber homolog follows the blue chromosome into the same cell, because that homolog is on the parallel track in the other meiosis-II cell. The next station will make the metaphase-I/metaphase-II distinction visible by changing the unit that aligns: homologous pairs aligned earlier; now individual duplicated chromosomes approach the metaphase II plate."
 ],
 'close':'New spindles are established in the haploid cells around already-duplicated chromosomes. Individual duplicated chromosomes now move to the Metaphase II Alignment Rail.'
},
'U5-L13':{
 'title':'Single Chromosomes at the Second Plate',
 'kicker':'Metaphase II aligns individual duplicated chromosomes, with sister kinetochores connected toward opposite poles.',
 'paragraphs':[
  "The **Metaphase II Alignment Rail** is narrower than the first metaphase platform. On your **left**, one spindle pole anchors a bundle of microtubules. Directly **ahead**, the metaphase plate is a single bright line where duplicated chromosomes arrive one by one. On your **right**, the opposite spindle pole sends microtubules toward the same chromosomes. The blue duplicated chromosome in the front cell remains two joined sister chromatids; the amber homolog is not beside it because meiosis I placed that homolog in the other cell. Imani keeps the second cell visible on a smaller mirrored panel so the two parallel divisions are never mistaken for one diploid cell.",
  "Each duplicated chromosome stops at the center plate as an individual chromosome. The left-facing sister kinetochore connects to microtubules from the left pole, while the other sister kinetochore connects toward the right pole. Once those opposing attachments are visible, Imani names the stage **metaphase II**. During metaphase II, chromosomes align at the metaphase plate and sister-chromatid kinetochores attach to microtubules from opposite poles.",
  "She then projects a faint outline of metaphase I behind the rail. In the first division, blue and amber homologous chromosomes were paired and aligned together; the pair was the unit whose orientation determined which homolog would go to each pole. Here the homologous partner is absent from this cell. The unit at the plate is one duplicated chromosome. This is why **metaphase I aligns homologous pairs**, while **metaphase II aligns individual duplicated chromosomes**.",
  "Ploidy does not change while the chromosomes align. Each cell remains n. The duplicated appearance of a chromosome again does not mean a second chromosome set has appeared. The sisters are copies within one chromosome that are about to be segregated to opposite poles. Imani taps the two opposing kinetochore attachments rather than the X shape itself, because those attachments reveal what will separate next.",
  "The gold ledger now shows DIVISION II — METAPHASE, n, SISTERS JOINED, OPPOSING SPINDLE ATTACHMENTS. Nothing about the entry mentions homolog pairing, because that first-division relationship has already been resolved. This makes metaphase II a mechanical setup for sister separation rather than a second version of independent homolog orientation.",
  "Imani traces the two sister kinetochores as separate attachment sites while the centromeric region still keeps the chromatids associated. Their opposing spindle connections predict the next movement: if the sister association is released, one former sister can move left and the other right. In metaphase I, by contrast, the decisive opposing relationship was between homologous chromosomes. The attachment geometry itself therefore tells you which division you are looking at.",
  "A tension meter along the center rail rises as the two poles pull on opposite sister kinetochores. The centromeric association still resists the force, so the sisters remain together for one final moment. The exit doors ahead open only when that association is released. Imani follows the tension line into the Anaphase II Sister Split, where the second division’s defining movement will finally separate the two sister chromatids."
 ],
 'close':'Individual duplicated chromosomes are aligned with sister kinetochores connected to opposite poles. The next station releases the sister connection and begins anaphase II.'
},
'U5-L14':{
 'title':'The Sister Split',
 'kicker':'Anaphase II releases the sister-chromatid connection; the former sisters then move as individual chromosomes toward opposite poles.',
 'paragraphs':[
  "The **Anaphase II Sister Split** is built around one central release point. On your **left**, one blue sister chromatid is connected toward the left spindle pole. Directly **ahead**, the centromeric sister connection glows at the split point. On your **right**, the other blue sister chromatid is connected toward the opposite pole. The same arrangement occurs for every duplicated chromosome in both meiosis-II cells. Imani freezes the tablet beside the room entrance so you can compare this geometry with anaphase I, where the travelers were whole duplicated homologous chromosomes rather than individual sisters.",
  "The release mechanism opens at the centromeric region. Proteins maintaining sister-chromatid association are released, and the two sisters move apart. Imani names the stage only after that movement begins: **anaphase II**. During anaphase II, sister chromatids separate and move toward opposite poles. This is the second meiotic division’s segregation event.",
  "Once the sisters separate, each former chromatid is counted as an individual chromosome. That change in chromosome count within the separating cell does not mean a new homologous set has appeared. Each future daughter product will still receive one version of each chromosome type, maintaining a haploid chromosome-set state. The key change is that duplicated chromosomes are becoming unduplicated chromosomes as sisters move apart.",
  "Imani places the anaphase-I image on the floor behind you and the anaphase-II image ahead. In **anaphase I**, homologous chromosomes separated while sister chromatids stayed attached. In **anaphase II**, sister chromatids separate after homologous partners have already been placed in different cells. The two movements look different because the structures being separated are different. The hall never needs a mnemonic substitute for that distinction; the tracked blue and amber chromosome histories make it visible.",
  "Recombined chromatids from prophase I now matter again. Some of the sisters moving apart carry small exchanged segments, so the four eventual products need not contain identical chromatid combinations. Imani does not claim crossing over is the only source of diversity; independent homolog orientation from metaphase I also contributed to the chromosome combinations sent into these cells. The route is preserving multiple mechanisms without merging them into one event.",
  "The chromosome-count tags change only at the moment of separation. Before release, the two chromatids belonged to one duplicated chromosome; after release, each former chromatid is an individual chromosome moving toward a pole. Even then, the future cells remain haploid because each receives one chromosome from each chromosome type, not a restored pair of homologous sets. This separates chromosome counting from ploidy one final time before the products form.",
  "Before the sisters reach their poles, an optional recall appears on the center release point: what separates during anaphase II? You answer from the structure in front of you, not from the numeral II. The former sisters then arrive at opposite ends as individual chromosomes. Nuclear-reformation panels and cytokinesis partitions begin rising around the four future products, opening the final Four-Cell Meiosis Exit."
 ],
 'close':'Sister chromatids have separated to opposite poles and now count as individual chromosomes. Telophase II and cytokinesis can form the four terminal haploid products.'
},
'U5-L15':{
 'title':'Four Exits, One Complete Meiosis',
 'kicker':'The terminal hall reveals the result of two divisions: four haploid products whose chromosomes are no longer duplicated.',
 'paragraphs':[
  "The **Four-Cell Meiosis Exit** is the widest room in the transit hall. On your **left**, a comparison panel shows a conventional mitotic division beginning from one cell and producing two cells while maintaining chromosome-set number in the usual comparison model. Directly **ahead**, four exit bays receive the products of the meiotic route you just followed. On your **right**, a tall ledger compares division number, product number, chromosome-set outcome, and genetic similarity. Imani places the original blue-and-amber chromosome tablet beneath the four central bays so every final chromosome can be traced backward through the same route.",
  "At the center, spindles break down and nuclei form around the chromosomes. Chromosomes may decondense, and cytokinesis separates the two meiosis-I cells into four cells. Imani names the stage **telophase II and cytokinesis**. Each final cell is haploid and now contains unduplicated chromosomes because sister chromatids separated during anaphase II. The route has therefore converted one diploid meiotic starting cell, after premeiotic replication and two divisions, into four haploid products.",
  "She writes the broad outcome as **meiosis forms haploid cells**. Meiosis transmits chromosome sets across generations by reducing chromosome-set number in sexually reproducing diploid organisms before fertilization later restores diploidy. The wording stays focused on chromosome transmission rather than pretending every meiotic product in every organism is immediately a mature gamete. The four cells here are the chromosomal products of the meiotic divisions.",
  "The right comparison panel now activates **mitosis versus meiosis**. Both processes use spindle apparatuses to move chromosomes, yet they differ in major ways. Mitosis involves one division and commonly produces two cells with the same chromosome-set number as the parent cell in the standard somatic comparison. Meiosis uses two divisions after one premeiotic DNA replication and produces four haploid products. The products of meiosis can also differ genetically because of mechanisms including crossing over and independent orientation of homologous pairs.",
  "Imani traces the entire route backward with one continuous line. DNA replicated once before meiosis I. Prophase I paired homologs and allowed crossing over between nonsister chromatids. Metaphase I oriented homolog pairs independently. Anaphase I separated homologs while sisters stayed together. Telophase I left two haploid cells with duplicated chromosomes. No DNA replication occurred between divisions. Prophase II rebuilt spindle access, metaphase II aligned individual duplicated chromosomes, and anaphase II separated sisters. The current four-cell exit is the consequence of that sequence, not an isolated picture to memorize.",
  "The four bays illuminate different combinations of blue, amber, and small recombinant chromosome segments. Imani closes the gold ledger only after you can state what was duplicated, what paired, what separated in division I, what did not replicate between divisions, and what separated in division II. The exit doors open toward the Diversity and Chromosome Error Center. Journey 2 is complete because the chromosome story can now be replayed mechanically from the same tracked structures rather than reconstructed from ten disconnected phase names."
 ],
 'close':'Four haploid products leave the hall after homolog segregation in meiosis I and sister-chromatid segregation in meiosis II, with no DNA replication between the divisions.'
},
}

def sha(path:Path): return hashlib.sha256(path.read_bytes()).hexdigest()

def zones_for(b):
    out=[]
    symbols=['L','◎','R']
    for i,pos in enumerate(['left','center','right']):
        src=b['spatial_layout'][pos]
        cast=next(x for x in b['stable_cast'] if x['position']==pos)
        out.append({'position':pos,'label':src['anchor'].title(),'symbol':symbols[i],'description':cast['visual_identity']})
    return out

def make_cast(b):
    cast=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    for pos in ['left','center','right']:
        src=next(x for x in b['stable_cast'] if x['position']==pos)
        cast.append({'name':b['spatial_layout'][pos]['anchor'].title(),'kind':'scientific part or process','visual':src['visual_identity'],'job':src['job_in_scene']})
    cast.append({'name':'Tracked chromosome set','kind':'continuity object','visual':'the same parental-origin color convention throughout the hall: blue homologs from one parental set and amber homologs from the other, with sister chromatids retaining their chromosome color and crossover segments retaining traceable exchanged colors','job':'preserves chromosome identity, sister relationships, recombination segments, ploidy state, and division history from premeiotic replication through the four final products'})
    cast.append({'name':'Gold generation ledger','kind':'continuity tool','visual':'the same narrow gold ledger from Journey 1, now showing chromosome-set number, DNA/chromatid state, division number, and the structure scheduled to separate next','job':'records only actual biological state changes and prevents phase labels from replacing chromosome-state reasoning'})
    return cast

def make_beats(b):
    return [{'object_id':t['knowledge_id'],'term':t['canonical_term'],'story':BEAT_IMAGES[t['knowledge_id']], 'science':t['canonical_science'],'exact_name':bool(t['exact_name_recall']),'hint':BEAT_IMAGES[t['knowledge_id']],'name_support':t['name_support']} for t in b['term_introductions']]

def make_snapshot(b):
    return [{'term':t['canonical_term'],'meaning':t['canonical_science'],'image':BEAT_IMAGES[t['knowledge_id']]} for t in b['term_introductions']]

briefs=[B[f'U5-L{i:02d}'] for i in range(6,16)]
scenes=[]
for idx,b in enumerate(briefs):
    n=NARR[b['locus_id']]; q=b['quick_recall']; checkpoint=bool(q['enabled'])
    cp={'U5-L07':'U5-K-012','U5-L10':'U5-K-063','U5-L14':'U5-K-008'}.get(b['locus_id']) if checkpoint else None
    scenes.append({
      'scene_index':idx,'locus_id':b['locus_id'],'locus':b['scene_title'],'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['micro_anchor'],'scene_layout':{'orientation':b['orientation_sentence'],'zones':zones_for(b)},
      'cast':make_cast(b),'continuity_object':J2['continuity_object'],
      'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':make_beats(b),'memory_snapshot':make_snapshot(b),
      'misconception_guards':b['misconception_guards'],'exit_memory':b['exit_memory'],
      'checkpoint':checkpoint,'checkpoint_object_id':cp,'checkpoint_prompt':q.get('candidate_prompt','') if checkpoint else '',
      'checkpoint_answer':q.get('answer','') if checkpoint else '',
      'checkpoint_hint':('Picture the same blue and amber chromosome set at this exact station and identify which physical chromosome relationship changed before naming the answer.' if checkpoint else ''),
      'next_locus':briefs[idx+1]['scene_title'] if idx+1<len(briefs) else None,'causal_transition':b['causal_transition']['transition_logic'],
    })

journey={
 'palace_id':'U5-J2','unit_id':'unit-5','palace_name':'Meiosis Transit Hall','story_title':'The Chromosome Set That Had to Survive Two Divisions',
 'tagline':'Carry the same chromosome set through one DNA replication and two meiotic divisions, keeping homologs, sisters, ploidy, and recombination visible at every station.',
 'guide':GUIDE,
 'premise':'The Meiosis Transit Hall has lost the state information that tells each division which chromosome relationship should move. A duplicated chromosome is being mistaken for an extra chromosome set, homologs and sister chromatids are being sent to the same release gate, and the interdivision checkpoint is attempting to replicate DNA a second time. The hall can produce correct haploid products only if the same chromosomes remain identifiable through every transition.',
 'mission':'Follow Dr. Imani Reyes through ten connected stations using the same blue and amber parental-origin chromosome identities. Track exactly when DNA replicates, when homologous chromosomes synapse and recombine, how homolog pairs orient, what separates during meiosis I, why the resulting cells are haploid while chromosomes remain duplicated, why DNA is not replicated again, and what separates during meiosis II.',
 'finale':'The hall releases four haploid products only after the complete chromosome history can be replayed without resetting the model: DNA replicated once before meiosis I; homologs paired and could cross over; homologs separated in division I while sisters stayed joined; no DNA replication occurred between divisions; sister chromatids separated in division II; and telophase II plus cytokinesis produced four haploid cells with unduplicated chromosomes.',
 'estimated_minutes':28,'scene_count':10,'checkpoint_count':3,'student_release':'DEVELOPER_PREVIEW_F4B',
 'learner_rule':'Keep watching the same chromosomes. Phase names come after the defining chromosome geometry or movement is visible. Optional Quick Recall appears only three times.',
 'route_orientation':'This is one continuous ten-location transit hall. Enter at the Premeiotic Loading Bay, pass through the five first-division stations, cross the locked no-replication checkpoint, continue through the four second-division stations, and finish at the Four-Cell Meiosis Exit. The same parental-origin chromosome colors and sister relationships are updated in place throughout the route.',
 'route':route,'scenes':scenes,'narrative_design':'U5-F4B-NARRATIVE-1.0'
}
(U5/'journeys').mkdir(exist_ok=True)
(U5/'journeys'/'U5-J2.json').write_text(json.dumps(journey,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
registry={
 'schema':'memory-palace-v2-unit5-f4b-journeys-1.0','unit_id':'unit-5','stage':'F4B','student_release':False,'preview_release':True,
 'journey_count':2,'scene_count':15,'checkpoint_count':5,
 'guided_journeys':[{k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']} for j in [J1,journey]]
}
(U5/'journeys-f4b.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
status={
 'unit_id':'unit-5','unit_number':5,'title':'Heredity','status':'F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','pipeline_status':'POLISHED_NARRATIVE_J1_J2_F4B',
 'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','student_release':False,'preview_release':True,
 'canonical_records':152,'review_flags_resolved':37,'teacher_ppt_slides':112,'ced_topics':5,'ced_atoms':34,'architecture_journeys':8,'architecture_loci':50,
 'scene_briefs':50,'preview_journeys':2,'preview_scenes':15,'preview_checkpoints':5,'journey_1_records':20,'journey_2_records':18,
 'next_gate':'F4C_JOURNEY3_ONLY_AFTER_F4B_PROSE_QA'
}
(U5/'status-f4b.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(U5/'status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
words=sum(len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs']))) for s in scenes)
manifest={'schema':'memory-palace-v2-unit5-f4b-release-manifest-1.0','unit_id':'unit-5','stage':'F4B','student_release':False,'preview_release':True,'journey_count':2,'scene_count':15,'checkpoint_count':5,'journey_2_records':18,'journey_2_narrative_words':words,'f1_canonical_records':152,'f2_permanent_loci':50,'f3_scene_briefs':50,'next_gate':'F4C'}
(U5/'f4b-release-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

course_path=ROOT/'content'/'ap-biology'/'course.json'; course=json.loads(course_path.read_text(encoding='utf-8'))
cu5=next(u for u in course['units'] if u['unit_id']=='unit-5')
cu5.update({'status':'F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','journey_count':2,'scene_count':15,'canonical_lock':'LOCKED_F1','source_status':'AUDITED_SCIENCE_LOCKED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVE_J1_F4A_J2_F4B','canonical_records':152,'review_flags_resolved':37,'ced_atoms':34,'teacher_ppt_slides':112,'student_release':False,'preview_release':True,'pipeline_stage':'UNIT5_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW_F4B'})
course_path.write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lock_files=['journeys/U5-J2.json','journeys-f4b.json','status-f4b.json','f4b-release-manifest.json']
lock={'schema':'memory-palace-v2-unit5-content-lock-f4b-1.0','unit_id':'unit-5','stage':'F4B','lock_status':'LOCKED_F4B_J2','student_release':False,'preview_release':True,'files':{}}
for rel in lock_files:
 p=U5/rel; lock['files'][rel]={'bytes':p.stat().st_size,'sha256':sha(p)}
(U5/'content-lock-f4b.json').write_text(json.dumps(lock,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines=['# Unit 5 F4B · Journey 2 Narrative','',f'## {journey["story_title"]}','',journey['tagline'],'','**Palace:** Meiosis Transit Hall  ','**Guide:** Dr. Imani Reyes  ','**Route:** '+' → '.join(x['locus'] for x in route),'']
for s in scenes:
 lines += [f"## {s['scene_index']+1}. {s['locus']} — {s['title']}",'',f"*{s['scene_kicker']}*",'']+s['story_paragraphs']+['']
(ROOT/'docs'/'UNIT5_F4B_JOURNEY2_STORY.md').write_text('\n'.join(lines),encoding='utf-8')
release=['# Unit 5 F4B Release','', 'Unit 5 F4B authors and locks Journey 2 only while preserving the F4A Journey 1 narrative. Unit 5 remains a developer preview and is not student released.','', '## Accounting','', '- Journey 1 preserved: **5 scenes / 20 records / 2 optional recalls**', '- Journey 2 authored: **10 scenes / 18 records / 3 optional recalls**', f'- Journey 2 narrative words: **{words}**', '- Total Unit 5 preview: **2 journeys / 15 scenes / 5 optional recalls**','', '## Scientific continuity','', '- The same parental-origin color convention persists from Journey 1 into Journey 2.', '- DNA replication occurs once before meiosis I and never between meiosis I and II.', '- Prophase I pairs homologs and allows crossing over between nonsister chromatids.', '- Metaphase I aligns homologous pairs; metaphase II aligns individual duplicated chromosomes.', '- Anaphase I separates homologs while sisters remain joined; anaphase II separates sisters.', '- Cells are haploid after meiosis I even while chromosomes remain duplicated.','', '## Release boundary','', 'No Unit 5 Memory Objects, Review runtime, Challenge Lab runtime, or student-facing Unit 5 release is created in F4B. Journeys 3–8 remain at the F3 scene-brief stage.','']
(ROOT/'docs'/'UNIT5_F4B_RELEASE.md').write_text('\n'.join(release),encoding='utf-8')
print(json.dumps({'journey':'U5-J2','scenes':10,'records':18,'checkpoints':3,'narrative_words':words,'student_release':False,'preview_release':True},indent=2))
