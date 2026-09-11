from __future__ import annotations
import json, hashlib, re, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'
subprocess.run([sys.executable,str(ROOT/'scripts'/'build_unit5_f4c.py')],check=True,stdout=subprocess.DEVNULL)
F3=json.loads((U5/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS=json.loads((U5/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J4=next(j for j in JBRIEFS if j['journey_id']=='U5-J4')
B={b['locus_id']:b for b in F3 if b['journey_id']=='U5-J4'}
CANON={r['knowledge_id']:r for r in json.loads((U5/'source'/'canonical-unit5-f1.json').read_text(encoding='utf-8'))['canonical_catalog']}
J1=json.loads((U5/'journeys'/'U5-J1.json').read_text(encoding='utf-8'))
J2=json.loads((U5/'journeys'/'U5-J2.json').read_text(encoding='utf-8'))
J3=json.loads((U5/'journeys'/'U5-J3.json').read_text(encoding='utf-8'))

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

GUIDE={
 'name':'Dr. Imani Reyes','role':'inheritance-systems geneticist',
 'visual':'deep-green field coat, clear gloves, compact chromosome tablet preserving the blue and amber parental-origin chromosome identities, and the narrow gold generation ledger',
 'story_job':'Imani keeps the biological mechanism separate from the symbols used to describe it. She makes the same allele records travel from parental plants into gametes and offspring so genotype notation, Mendelian laws, cross labels, Punnett grids, and ratios never replace the chromosome and gamete processes they summarize.'
}
LEDGER={
 'name':'Pea-line breeding ledger','kind':'continuity record',
 'visual':'a long cream-and-gold ledger with one tracked pea line running across every page. The same parental records, allele symbols, gamete entries, and offspring records are carried forward from room to room',
 'job':'links the same modeled inheritance system across the estate while keeping phenotype observations, allele notation, parental genotypes, gamete types, and offspring probabilities in separate columns.'
}
ALLELE_CASE={
 'name':'Tracked allele case','kind':'continuity scientific object',
 'visual':'a slim glass case holding two allele cards for one modeled gene locus. The cards remain the same biological alleles even when the estate changes how they are written or combined',
 'job':'keeps allele identity stable from the notation cabinet through genotype construction, gamete formation, Punnett modeling, and the final ratio panels.'
}

route=[
 {'scene_index':0,'locus':'Mendel Breeding Courtyard','short':'Generations','floor':'South courtyard','symbol':'P→F1→F2'},
 {'scene_index':1,'locus':'Allele Notation Cabinet','short':'Alleles','floor':'Record gallery','symbol':'A/a'},
 {'scene_index':2,'locus':'Genotype–Phenotype Bench','short':'Genotype','floor':'Glasshouse bench','symbol':'AA/Aa/aa'},
 {'scene_index':3,'locus':'Mendelian Laws Gate','short':'Laws','floor':'North gate','symbol':'1↔2'},
 {'scene_index':4,'locus':'Cross-Type Arbor','short':'Cross type','floor':'Hedge arbor','symbol':'1/2/?'},
 {'scene_index':5,'locus':'Gamete–Punnett Board','short':'Gametes','floor':'Model room','symbol':'□'},
 {'scene_index':6,'locus':'Classic Ratio Balcony','short':'Ratios','floor':'Upper balcony','symbol':'3:1'}
]

BEAT_IMAGES={
 'U5-K-065':'the courtyard plaque beside the controlled pea crosses that identifies Mendel as the investigator whose experiments revealed predictable particulate inheritance patterns',
 'U5-K-066':'the left greenhouse row that keeps producing the same scored phenotype generation after generation under self-fertilization within the modeled line',
 'U5-K-067':'the first ledger page marked P beside the two parental lines used to begin the cross',
 'U5-K-068':'the center terrace of offspring produced directly from the parental cross and labeled F1',
 'U5-K-069':'the right terrace produced from F1 individuals and labeled F2',
 'U5-K-071':'the two DNA-version cards occupying the same gene-locus drawer in the allele cabinet',
 'U5-K-072':'the removable uppercase and lowercase letter sleeves placed over the allele cards as a classroom notation convention',
 'U5-K-076':'the allele whose effect is visible in the heterozygous phenotype under the complete-dominance model',
 'U5-K-077':'the allele whose phenotype is masked in the heterozygote under the complete-dominance model and appears in the corresponding homozygote',
 'U5-K-018':'the genotype rail arranging two allele cards into AA, Aa, or aa while separately labeling homozygous and heterozygous states',
 'U5-K-019':'the phenotype window showing the observable or measurable trait state produced from the genotype in context',
 'U5-K-073':'the AA drawer containing two copies of the dominant allele in the modeled two-allele complete-dominance system',
 'U5-K-074':'the aa drawer containing two copies of the recessive allele',
 'U5-K-078':'the phenotype panel where AA and Aa produce the same scored dominant phenotype while aa produces the recessive phenotype',
 'U5-K-014':'the two-lane Mendelian gate that keeps segregation for one gene distinct from independent assortment for unlinked genes and sends linked genes to a later mapping route',
 'U5-K-079':'the left gate where the two alleles of one diploid locus separate during gamete formation so each gamete receives one allele',
 'U5-K-081':'the right gate where allele pairs for two unlinked genes segregate independently during gamete formation',
 'U5-K-017':'the branching arbor that classifies one-gene, two-gene, and tester crosses from the parental genotypes and the genetic question before any grid is drawn',
 'U5-K-075':'the testcross branch pairing an unknown dominant-phenotype genotype with a homozygous recessive tester and using offspring evidence to distinguish the unknown genotype',
 'U5-K-080':'the one-gene branch following a monohybrid heterozygous at one gene of interest',
 'U5-K-082':'the two-gene branch following a dihybrid heterozygous at two genes of interest',
 'U5-K-070':'the Punnett grid receiving one parent’s possible gametes across the top and the other parent’s possible gametes down the side, then showing possible offspring genotype combinations',
 'U5-K-085':'the gamete generator splitting a diploid parent genotype so each gamete receives one allele per locus and only biologically possible multilocus allele combinations enter the grid',
 'U5-K-083':'the left balcony panel showing a conditional 3:1 dominant-to-recessive phenotype expectation for the appropriate Aa × Aa complete-dominance monohybrid cross',
 'U5-K-084':'the right balcony panel showing a conditional 9:3:3:1 phenotype expectation for the appropriate AaBb × AaBb cross when both loci show complete dominance and assort independently'
}

ZONE_COPY={
'U5-L20':[
 ('left','True-breeding P greenhouse row','P','Two pea lines occupy separate glasshouse beds. Each line repeatedly produces the same scored phenotype under the modeled breeding conditions and serves as a stable parental reference.'),
 ('center','Controlled cross bridge and F1 terrace','F1','A narrow pollination bridge links the parental beds to the first offspring terrace. The estate ledger records exactly which parental lines entered the cross and which offspring belong to the first filial generation.'),
 ('right','F2 terrace','F2','A second terrace receives offspring produced from F1 individuals. The physical sequence P to F1 to F2 stays visible across the whole courtyard.')],
'U5-L21':[
 ('left','Recessive allele drawer','a','One allele card for the tracked gene sits in a left drawer beneath a removable lowercase sleeve. The letter is a symbol placed on the allele card and never changes the DNA version itself.'),
 ('center','Gene-locus and allele-pair cabinet','locus','Two alternative DNA-version cards occupy the same modeled gene-locus drawer so allele identity is established before dominance labels or letter case are applied.'),
 ('right','Dominant allele drawer','A','The alternate allele card sits beneath a removable uppercase sleeve. A heterozygote comparison window beside it shows the phenotype context that defines the dominance relationship.')],
'U5-L22':[
 ('left','Homozygous genotype drawers','AA / aa','Two fixed drawers hold same-allele pairs so homozygous dominant and homozygous recessive states can be compared without moving the phenotype panel.'),
 ('center','Genotype-to-phenotype comparison bench','genotype → phenotype','The tracked allele cards are combined into genotypes on the center rail, then passed through a separate phenotype window so inherited allele combination and observable outcome never share one label.'),
 ('right','Heterozygous complete-dominance window','Aa','A heterozygous pair enters the right window. Its scored phenotype matches the dominant homozygote in this complete-dominance model while its genotype remains different.')],
'U5-L23':[
 ('left','Law of segregation lane','one gene','One diploid locus with two alleles enters the left lane. Meiosis sends the two alleles into different gametes so each gamete receives one allele at that locus.'),
 ('center','Mendelian laws gatehouse','unlinked genes','A gatehouse compares the two inheritance rules and keeps a clearly marked side route for linked genes, preventing independent assortment from being treated as universal.'),
 ('right','Law of independent assortment lane','two genes','Two unlinked gene pairs enter the right lane. Their allele pairs segregate independently during gamete formation under the modeled conditions.')],
'U5-L24':[
 ('left','Monohybrid branch','1 gene','A single-vine branch accepts a cross that follows one gene of interest. The branch label comes from the genetic question and genotype structure, not the size of a future Punnett grid.'),
 ('center','Cross-type decision arbor','choose first','The pea-line ledger is read before any calculation. Parent genotypes and the question determine which branch the cross belongs to.'),
 ('right','Dihybrid and testcross branches','2 genes / tester','A double-vine route follows two genes, while a separate tester route pairs an unknown dominant-phenotype individual with a homozygous recessive tester.')],
'U5-L25':[
 ('left','Parent genotype and gamete generator','parent → gametes','The parent genotype enters a conventional meiosis-based generator that lists only allele combinations that can actually appear in that parent’s gametes.'),
 ('center','Punnett combination board','□','One parent’s possible gametes are placed across the top and the other parent’s down the side. Each cell combines one gamete from each parent.'),
 ('right','Offspring genotype and phenotype possibilities','probability','The grid’s cells are read as possible offspring genotypes. Phenotype probabilities are derived only after the appropriate genotype-to-phenotype rule is applied.')],
'U5-L26':[
 ('left','Conditional 3:1 panel','3:1','A monohybrid outcome panel appears only when the parental cross and complete-dominance assumptions justify the classic three-to-one phenotype expectation.'),
 ('center','Assumption banner','conditions','A large banner lists the cross and inheritance assumptions that must hold before either classic ratio panel is allowed to illuminate.'),
 ('right','Conditional 9:3:3:1 panel','9:3:3:1','A dihybrid outcome panel appears only for the appropriate heterozygote cross with complete dominance at both loci and independent assortment.')],
}

NARR={
'U5-L20':{
 'title':'The Courtyard Where the Generations Had Been Shuffled',
 'kicker':'The estate can breed peas, but the records mean nothing until parental, first-filial, and second-filial generations stay tied to the crosses that produced them.',
 'paragraphs':[
  "A wrought-iron gate opens into the **Mendel Breeding Courtyard**, and the estate immediately feels wrong. On your **left**, two long greenhouse beds hold pea plants that have been bred within their own lines for many generations. Directly **ahead**, a narrow glass pollination bridge crosses a reflecting channel and ends at a terrace of young plants. On your **right**, a second terrace rises one level higher, crowded with another generation of offspring. The architecture should make the sequence obvious, yet every brass generation sign has been piled at the center fountain. P, F1, and F2 are stacked together like interchangeable labels. Dr. Imani Reyes sets the cream-and-gold pea-line breeding ledger on the fountain rim. The first page is blank because the estate cannot call a plant F1 or F2 until it knows which cross produced it.",
  "Imani walks left first. One greenhouse bed has produced the same scored flower-color phenotype through repeated self-fertilization within that line under the modeled conditions. The neighboring bed has done the same for the alternate phenotype. She names each stable line a **True-breeding line**. The important feature is consistency for the trait being studied under the breeding design. The term does not mean every gene in the organism is identical across all individuals. Imani clips one brass tag to each line and carries those two tags to the ledger. These plants are the starting parents of the modeled cross, so she places the P sign beside them. The **P generation** is the parental generation used to begin a genetic cross.",
  "At the center bridge, pollen from one parental line is transferred according to the controlled cross and the first offspring terrace lights. Imani places the next sign only after the offspring exist. The **F1 generation**, the first filial generation, consists of offspring from the parental cross. The ledger now has a visible chain from the two P-generation lines on the left to the F1 terrace directly ahead. No allele letters have appeared yet. The courtyard is teaching generational identity before symbolic notation, because F1 means first-generation offspring of the specified parental cross, not a particular genotype or phenotype by itself.",
  "The estate then opens a second set of pollination doors. F1 individuals are allowed to produce the next generation in the classic design. Seeds travel up the stone stair to the terrace on your right, and Imani finally places the F2 sign there. The **F2 generation**, the second filial generation, is produced from crosses or selfing involving F1 individuals in the classic Mendelian design. The three terraces now form a route you can physically retrace. P begins the cross on the left, F1 comes directly from that parental cross in the center, and F2 follows from the F1 generation on the right.",
  "A bronze portrait plaque beside the bridge identifies **Gregor Mendel**. Imani points out why his controlled pea-plant crosses matter. They provided the experimental foundation for principles of particulate inheritance, including patterns later described through segregation and independent assortment. The estate keeps the historical experiment separate from modern molecular explanation. Mendel could track predictable phenotype patterns without knowing DNA structure, chromosome behavior, or the modern concept of alleles as DNA sequence variants. The later rooms will supply that mechanism. His pea experiments give the journey its experimental frame, not a complete modern chromosome model by themselves.",
  "When the generation signs are restored, the courtyard’s central fountain begins pumping again. Water pushes a locked drawer key out through a brass channel and sends it toward the record gallery beyond the F2 terrace. Imani closes the first breeding-ledger page. It now shows the exact sequence of crosses, but the offspring records still use vague phrases such as strong trait and weak trait. She refuses to carry those phrases forward. The same inherited factor can only be followed through the estate if its alternative versions receive precise biological identities. She leads you through the gallery door toward the **Allele Notation Cabinet**, taking the same pea-line ledger with her."
 ],
 'close':'With P, F1, and F2 restored to the crosses that produced them, the unresolved inheritance record becomes an allele-identification problem. The breeding ledger opens the Allele Notation Cabinet.'
},
'U5-L21':{
 'title':'The Cabinet That Thought a Capital Letter Meant Stronger Biology',
 'kicker':'The biological allele exists before the letter symbol, and dominance is defined by phenotype in a heterozygote rather than by frequency, strength, or value.',
 'paragraphs':[
  "The record-gallery door closes behind you inside the **Allele Notation Cabinet**. The room is narrow and perfectly symmetrical. On your **left**, a shallow drawer holds one DNA-version card beneath a removable lowercase sleeve marked a. Directly **ahead**, a glass cabinet displays a single gene locus with two slots for alternative DNA sequences. On your **right**, a matching drawer holds the alternate DNA-version card beneath an uppercase sleeve marked A. Above the cabinet, an old estate sign claims CAPITAL = STRONG and lowercase = weak. Imani takes the sign down before touching anything else. The tracked pea-line breeding ledger lies open across the center counter so the same inherited factor from the courtyard remains visible.",
  "She removes both letter sleeves and slides the two bare cards into the center locus. They occupy the same modeled gene position while carrying alternative DNA sequence versions. Imani names each alternative version an **Allele**. An allele is an alternative DNA sequence or version of a gene at a locus. The two cards can differ biologically even when no uppercase or lowercase symbol has been assigned. Their identity comes from the underlying DNA version, not from the typography the classroom later uses to represent it.",
  "Only after the biological relationship is clear does Imani return the letter sleeves. The estate chooses A for one allele and a for the other in this simple two-allele model. She labels this a **Dominance notation convention**. Uppercase and lowercase letters are a classroom convention used to distinguish alleles in simple problems. The letter case is not a molecular property. Imani swaps the sleeves for a moment while leaving the DNA cards fixed in place. The cards do not transform when the symbols change. That deliberate mismatch makes the point visible. A notation system can describe a biological model, while the notation itself does not create the allele or its effect.",
  "A heterozygote window opens beside the right drawer. One A card and one a card enter together. Under the modeled complete-dominance conditions, the scored phenotype associated with A is expressed. Imani names A the **Dominant allele** in this defined phenotype relationship. A dominant allele is one whose effect on the defined phenotype is expressed in a heterozygote under complete-dominance conditions. The word dominant says nothing about how common the allele is in a population, how beneficial it is, how physically strong the organism is, or whether evolution will favor it.",
  "The same heterozygote keeps the a card visible even though its associated recessive phenotype is not expressed in that heterozygous condition. Imani names a the **Recessive allele**. Its effect on the defined phenotype is masked in the heterozygote under complete dominance and can be expressed in the corresponding homozygote. She places frequency counters beside both alleles and deliberately gives the recessive allele the larger count. Nothing about the dominance relationship changes. Dominance and frequency occupy different drawers because they answer different biological questions.",
  "The cabinet now has three layers that can no longer be collapsed. The center holds biological allele identity, the removable letter sleeves hold notation, and the heterozygote window reveals the dominance relationship for a particular phenotype model. Imani clips the same A and a cards into the pea-line ledger and carries them through a glass door at the back of the gallery. On the other side, a long workbench has three genotype trays labeled AA, Aa, and aa, but the phenotype lamps above them are still dark. The next problem is no longer what the alleles are. It is how allele combinations relate to what can actually be observed."
 ],
 'close':'Allele identity, notation, and dominance are now separate. The same A and a cards move to the Genotype–Phenotype Bench so inherited combinations can be compared with observable outcomes.'
},
'U5-L22':{
 'title':'The Bench With Two Labels for One Organism',
 'kicker':'An allele combination and an observable trait state are connected, yet they are not interchangeable descriptions.',
 'paragraphs':[
  "You enter the warm central glasshouse and stop at the **Genotype–Phenotype Bench**. On your **left**, two brass drawers are labeled AA and aa. Directly **ahead**, a rail accepts pairs of allele cards and carries them through a clear observation chamber. On your **right**, a third drawer marked Aa sits beneath a phenotype lamp that can be compared with the AA lamp. The pea-line breeding ledger is clamped along the front edge of the bench, still carrying the same A and a allele cards from the notation cabinet. Imani positions the tracked allele case beside it so no new alleles can quietly appear while the estate changes the way it describes an organism.",
  "She begins with the allele combination itself. Two allele copies placed together for the modeled diploid locus form a **Genotype**. For a diploid locus, that genotype can be **homozygous** when the two allele copies are the same or **heterozygous** when the two copies differ. Imani places AA in the upper left drawer, aa in the lower left drawer, and Aa in the right drawer. She then covers the phenotype lamps. You can still classify the genotypes perfectly because genotype refers to the inherited allele combination, not to the trait appearance visible outside the cabinet.",
  "The AA drawer opens first. It contains two copies of the allele that is dominant in this complete-dominance model. Imani names this state **Homozygous dominant**. The aa drawer contains two copies of the recessive allele and is labeled **Homozygous recessive**. The two homozygous states share the same structural idea, two identical alleles at the modeled locus, while their allele identities differ. The Aa drawer remains visibly different because its two allele cards are not the same. Imani keeps the word heterozygous beside that mixed pair.",
  "Now she turns on the observation chamber. Each genotype moves through without changing its allele cards. AA activates the scored dominant phenotype lamp. aa activates the recessive phenotype lamp. Aa then enters, and its lamp matches the AA phenotype under the modeled conditions. Imani names this relationship **Complete dominance**. Complete dominance occurs when the heterozygote has the same phenotype as the dominant homozygote for the trait being scored. The shared phenotype does not make AA and Aa the same genotype. The bench keeps their allele cards visible even while their phenotype lamps match.",
  "Imani finally labels the lamps **Phenotype**. Phenotype is the observable expression of inherited traits, and phenotype can also be influenced by environmental conditions. She places a transparent environmental-control cover over the lamps to foreshadow a later journey. The cover changes no allele cards. This keeps the direction clear. Genotype describes inherited allele composition. Phenotype describes the observable or measurable trait state produced when that genotype is expressed in context. A phenotype cannot be read backward into a unique genotype whenever more than one genotype can produce the same observable state.",
  "The estate tests the distinction by showing the same dominant phenotype lamp over both AA and Aa. The ledger groups the vocabulary under **Genotype, homozygous, heterozygous** so the three related ideas stay linked without becoming synonyms. It must record the visible phenotype in one column and the genotype in another. If you place the phenotype word in the genotype column, the bench locks. If you place AA and Aa under one genotype label because their lamps match, it locks again. Imani releases the mechanism only when the four ideas stay separate. genotype, phenotype, homozygous state, and heterozygous state. At that moment the back wall opens into a wrought-iron gate with two lanes. The allele cards have been identified and combined. The unresolved question is how they reach different gametes during meiosis."
 ],
 'close':'The bench separates genotype from phenotype and homozygous from heterozygous states. The same allele pairs now approach the Mendelian Laws Gate to show how meiosis distributes them into gametes.'
},
'U5-L23':{
 'title':'The Gate With Two Laws and One Forbidden Shortcut',
 'kicker':'Segregation concerns the two alleles of one gene, while independent assortment concerns how unlinked gene pairs behave relative to one another.',
 'paragraphs':[
  "The glasshouse path reaches the **Mendelian Laws Gate**, a tall iron gatehouse built over two parallel lanes. On your **left**, one modeled diploid locus carries A on one homolog and a on the other. Directly **ahead**, the gatehouse holds the pea-line breeding ledger and a chromosome tablet showing where each allele sits. On your **right**, a second chromosome pair introduces another gene with B and b alleles. A small side door marked LINKED GENES remains closed and points toward the future chromosome-mapping rail yard. The arrangement is deliberate. One-gene allele separation can be watched on the left, while the relationship between two unlinked gene pairs can be watched on the right.",
  "Imani activates the left lane first. The A-bearing homolog and a-bearing homolog enter meiosis as a pair. When homologous chromosomes segregate during the first meiotic division, the two allele copies move into different future gamete lineages. By the end of gamete formation, each gamete receives one allele at that locus. Imani names this principle the **Law of segregation**. The law states that the two alleles for a gene in a diploid individual separate during gamete formation so each gamete receives one allele at that locus. The rule describes the inheritance consequence of chromosome segregation that you already watched physically in Journey 2.",
  "The right lane now adds the B and b locus on a different chromosome pair. Imani lets the A/a homolog pair orient one way and the B/b homolog pair orient independently at metaphase I. When the model runs, the particular allele from one gene that enters a gamete does not force a particular allele from the other unlinked gene to accompany it. She names this the **Law of independent assortment**. Allele pairs for unlinked genes segregate independently during gamete formation. The rule applies cleanly when the genes are on different chromosomes or otherwise behave as effectively unlinked in the modeled context.",
  "The center gatehouse then lights a joint label, **Mendelian laws for unlinked genes**. Imani places segregation and independent assortment side by side without merging them. Segregation answers what happens to the two alleles of one gene. Independent assortment answers how allele pairs at different unlinked genes behave relative to one another. Both can be applied to genes on different chromosomes, while linkage can alter the independent-assortment expectation. The small LINKED GENES door remains visibly closed because those cases belong to a later journey where recombination and map distance can be handled directly.",
  "To make the contrast durable, Imani runs a deliberate error. She sends A and a into the same gamete and calls it independent assortment. The gate sounds an alarm because the one-gene segregation rule has already been violated. She resets the model, segregates A from a correctly, then forces B to accompany A in every gamete even though the genes are modeled as unlinked. A different alarm sounds because the relationship between the two gene pairs no longer follows independent assortment. The two alarms come from different lanes, which makes the laws easier to reconstruct than two memorized sentences with similar wording.",
  "The second optional recall panel slides from the gatehouse only after both mechanisms have been visible. It asks which Mendelian law separates the two alleles of one gene and which concerns unlinked genes. The answer follows the physical route. **Law of segregation** belongs to the one-gene left lane. **Law of independent assortment** belongs to the two-unlinked-gene right lane. When the panel retracts, the gate opens onto a garden arbor with three branches. The laws now explain how alleles can reach gametes. The estate’s next question is what kind of cross the breeding ledger is actually asking you to model."
 ],
 'close':'Segregation and independent assortment now have different physical jobs. The opened gate leads to the Cross-Type Arbor, where the genetic question and parental genotypes determine which cross design applies.'
},
'U5-L24':{
 'title':'The Arbor That Chose the Grid Before Reading the Parents',
 'kicker':'A cross is classified from the genes being followed and the parental genotypes, not from the size of a Punnett square drawn afterward.',
 'paragraphs':[
  "Beyond the gate, the path enters the **Cross-Type Arbor**. On your **left**, a single grapevine-like branch carries one gene tag and one pair of allele symbols. Directly **ahead**, the pea-line breeding ledger rests on a stone decision pedestal with slots for parental genotypes and the question being asked. On your **right**, the arbor divides again. One branch carries two gene tags, while a narrower tester branch ends beside a plant marked homozygous recessive. The old estate system has been choosing a cross type by counting future grid boxes. Imani erases the box counts from the signs. She makes the ledger read the biology first.",
  "A parent heterozygous at one gene of interest enters the left branch. Imani labels the individual a **Monohybrid**. A monohybrid is heterozygous at one gene of interest, and a monohybrid cross follows inheritance of that one gene, classically represented by a cross such as Aa × Aa. The label belongs to the gene focus and genotype structure. A four-cell Punnett grid may later be convenient for a simple two-allele cross, but the grid size does not define the word monohybrid.",
  "The double-vine route on the right accepts a parent heterozygous at two genes of interest, such as AaBb in the classic model. Imani names that individual a **Dihybrid**. A dihybrid cross follows inheritance of both genes, classically AaBb × AaBb. Again, the arbor makes the classification before any probabilities are calculated. The two-gene biological question creates the dihybrid route. A sixteen-cell grid is one possible representation of gamete combinations under a simple independent-assortment model; it is not the biological definition.",
  "The narrower branch serves a different purpose. A plant with a dominant phenotype arrives with an unknown genotype. The ledger records two possibilities under the simple complete-dominance model. It could be homozygous dominant or heterozygous. Imani pairs that unknown individual with a homozygous recessive tester. This is the classic **Testcross mechanics**. Offspring phenotypes provide evidence about the unknown genotype because the tester contributes only the recessive allele at the modeled locus. The testcross is a design strategy for resolving an unknown genotype under appropriate conditions, not a universal procedure that every inheritance question must use.",
  "Imani then labels the full branching structure **Monohybrid, dihybrid, and test crosses**. These cross types help analyze inheritance and, in suitable systems, provide evidence about dominance relationships or unknown genotypes. The three paths remain physically separate. One follows one gene, one follows two genes, and one is designed around a homozygous recessive tester. She hands you three blank Punnett boards and asks where they belong. You cannot place them yet because the parent genotypes have not been converted into gametes. The arbor refuses every board that arrives before the gamete step.",
  "That refusal creates the transition. The ledger sends the selected parental genotypes down a narrow covered walkway to a large modeling room. At the doorway, each parent record passes through a meiosis symbol and emerges as a rack of possible gamete cards. Imani keeps the boards folded until those gametes are identified. The estate is finally following causal order. First define the cross and parental genotypes. Then determine the gametes those parents can produce. Only after that can a Punnett square organize possible combinations."
 ],
 'close':'Cross type is now chosen from the biological question and parental genotypes. Those parents move next to the Gamete–Punnett Board, where possible gametes must be generated before any offspring grid can be built.'
},
'U5-L25':{
 'title':'The Board That Had Been Taking Credit for Meiosis',
 'kicker':'The grid organizes gamete combinations after meiosis has defined the possible gametes. It models probability and does not cause allele segregation.',
 'paragraphs':[
  "The covered walkway opens into the **Gamete–Punnett Board** room. On your **left**, the same parental genotype records from the arbor feed into a transparent gamete generator. Directly **ahead**, a large empty Punnett grid is built into the floor. On your **right**, a bank of offspring genotype cards waits beneath phenotype lamps. The estate’s old instruction plate says THE SQUARE SEPARATES THE ALLELES. Imani removes it and places the pea-line ledger between the parent generator and the grid. The room will remain dark until the genotype-to-gamete step is finished in the correct order.",
  "She starts with one modeled diploid parent. At each locus, the parent carries two alleles, while each gamete receives one allele per diploid locus after meiosis. For a multilocus parent, the possible gamete types depend on the parent genotype and on whether the genes assort independently, are linked, or have another specified relationship. Imani labels this step **Gametes from a genotype**. She makes the generator display only biologically possible gamete allele combinations under the stated model. Nothing has entered the Punnett square yet. The possible gametes come from meiosis and the parental genotype, not from the grid.",
  "Once the gamete racks are complete, Imani unfolds the board. One parent’s possible gametes are placed across the top edge. The other parent’s possible gametes are placed down the left edge. Each cell inside the board receives one gamete from the top and one from the side. Their alleles are combined to represent one possible offspring genotype. Imani names the structure a **Punnett square**. A Punnett square organizes possible gamete combinations to predict genotype and phenotype probabilities for a genetic cross. The cells are a model of combinations, not miniature offspring and not commands that force fertilization to occur in equal numbers.",
  "The right-side offspring bank now activates. Genotype possibilities move from the grid into clearly labeled categories. Only after that does Imani apply the appropriate genotype-to-phenotype relationship from the earlier bench. If the modeled locus shows complete dominance, different genotypes may map to the same phenotype category. If the inheritance relationship changes in a later journey, the phenotype interpretation will change even if the genotype probabilities in the grid are the same. The board therefore separates two operations. It first organizes genotype probabilities from gamete combinations, then phenotype probabilities are derived from the relevant biological relationship.",
  "Imani runs a small demonstration without asking you to solve a practice problem. A parent genotype enters the generator, the possible gametes appear, and the board combines them with the other parent’s gametes. She then covers the grid and asks what biological events made the allele combinations possible. The answer lies behind you in the Mendelian Laws Gate. Segregation separated the alleles of one gene into gametes. Independent assortment described the relationship among unlinked genes. Fertilization later combines one gamete from each parent. The Punnett square merely organizes those possible combinations on paper or screen.",
  "A probability counter at the edge of the board flashes a warning that predicted probabilities are not guaranteed offspring counts. A cross with a one-quarter predicted genotype probability does not promise that exactly one of every four actual offspring will have that genotype. Random sampling produces variation, especially in small families or experiments. Imani leaves the counter visible because the next balcony contains famous phenotype ratios that students often treat as automatic laws. The grid now sends its modeled probabilities upward along a brass staircase. The next room will decide when the classic summaries are actually justified."
 ],
 'close':'The Punnett board has been reduced to its real job as a probability model of gamete combinations. Its outcome cards climb to the Classic Ratio Balcony, where assumptions decide whether familiar ratios are valid summaries.'
},
'U5-L26':{
 'title':'The Balcony Where the Famous Ratios Would Not Turn On',
 'kicker':'Classic Mendelian ratios appear only when the cross and inheritance assumptions justify them.',
 'paragraphs':[
  "A spiral stair brings you onto the **Classic Ratio Balcony**, which overlooks the entire Mendelian estate. On your **left**, a large panel is divided into dominant and recessive phenotype sectors and bears the ratio **3:1**. Directly **ahead**, a bronze assumption banner hangs from the roof beam but every condition line is blank. On your **right**, a larger four-category panel bears **9:3:3:1**. Both ratio panels are dark. Below you, the courtyard, allele cabinet, genotype bench, laws gate, cross arbor, and Punnett room line up in the exact order you traveled. Imani sets the pea-line breeding ledger on the railing and says the panels will illuminate only when the whole inheritance chain below supports them.",
  "She begins with the left panel. The ledger specifies the appropriate classic monohybrid heterozygote cross, Aa × Aa, under complete dominance and the standard Mendelian segregation assumptions. The Punnett model below produces the expected genotype probabilities, and the complete-dominance phenotype rule groups those genotypes into dominant and recessive phenotype categories. Only then does the left panel light. Imani names the result the **Classic 3:1 F2 ratio**. A three-to-one dominant-to-recessive phenotype ratio is the expected large-sample pattern for that specified cross under the stated conditions. It is not a universal ratio attached to the word dominance.",
  "The right panel requires more conditions. The ledger now specifies the classic AaBb × AaBb dihybrid cross. Both loci must show complete dominance in the modeled phenotype categories, and the genes must assort independently. When those assumptions are satisfied, the gamete combinations and phenotype grouping produce the familiar **Classic 9:3:3:1 ratio**. Imani leaves the linked-gene side door from the Mendelian Laws Gate visible far below. If the genes are linked strongly enough to depart from independent assortment, the right panel loses permission to glow. The ratio is a conditional expectation, not a fingerprint that every two-gene cross must display.",
  "The center assumption banner now fills line by line. It lists the cross, the dominance relationship, the segregation and assortment conditions, and the idea that the ratio describes an expected distribution across many outcomes. Imani deliberately places the banner between the panels so neither number can be remembered without its requirements. She then changes one condition at a time. When the left cross is no longer Aa × Aa, the three-to-one panel dims. When complete dominance is replaced by another genotype-to-phenotype relationship, the phenotype grouping changes. When the two genes on the right no longer assort independently, the nine-to-three-to-three-to-one panel dims.",
  "A final sampling display scatters a small number of offspring dots across the balcony floor. Even with the classic assumptions intact, the observed dots do not line up perfectly with the expected ratio. Imani keeps the expectation panel lit while allowing the sample to vary. Expected probability and observed count are related without being identical. The statistics journey later in this unit will ask whether deviations from an expected distribution are large enough to require further explanation. For now, the estate’s job is simpler. The famous ratios summarize conditional probabilities produced by a defined cross and inheritance model.",
  "Imani closes the breeding ledger and points back over the estate. The route can now be reconstructed as one causal chain. Mendel’s controlled generations established the experimental pattern. Alleles gave the inherited alternatives precise identities. Genotype described allele combinations, while phenotype described observable expression in context. Segregation and independent assortment described how alleles enter gametes. Cross type identified the genetic design. Gamete generation preceded the Punnett model. The grid organized possible offspring combinations. The ratio panels summarized only the outcomes justified by the stated assumptions.",
  "The balcony doors unlock. A second estate wing is visible beyond the hedge, filled with probability wheels, pedigree charts, and evidence boards. Imani leaves the classic ratio panels behind because they belong to the specific assumptions displayed on this balcony. The next journey will use Mendelian reasoning as a starting point while asking students to interpret probability and family evidence directly. Journey 4 ends with the biology and the model finally in the correct order. Chromosomes and gametes generate inheritance outcomes, notation describes them, and probability tools help us reason about what may be observed."
 ],
 'close':'The complete Mendelian workflow is now causal and assumption-bound. The next journey can use probability and pedigree evidence without treating classic ratios as universal templates.'
}
}

def zones_for(b):
    out=[]
    for pos,(position,label,symbol,desc) in zip(('left','center','right'),ZONE_COPY[b['locus_id']]):
        assert pos==position
        out.append({'position':position,'label':label,'symbol':symbol,'description':desc})
    return out

def make_cast(b):
    cast=[GUIDE,LEDGER,ALLELE_CASE]
    for z in zones_for(b):
        cast.append({'name':z['label'],'kind':'scientific structure or reference zone','visual':z['description'],'job':next(x['job_in_scene'] for x in b['stable_cast'] if x['position']==z['position'])})
    return cast

def make_beats(b):
    return [{'object_id':t['knowledge_id'],'term':t['canonical_term'],'story':BEAT_IMAGES[t['knowledge_id']],'science':t['canonical_science'],'exact_name':bool(t['exact_name_recall']),'hint':BEAT_IMAGES[t['knowledge_id']],'name_support':t['name_support']} for t in b['term_introductions']]

def make_snapshot(b):
    return [{'term':t['canonical_term'],'meaning':t['canonical_science'],'image':BEAT_IMAGES[t['knowledge_id']]} for t in b['term_introductions']]

briefs=[B[f'U5-L{i:02d}'] for i in range(20,27)]
scenes=[]
for idx,b in enumerate(briefs):
    n=NARR[b['locus_id']]; q=b['quick_recall']; checkpoint=bool(q['enabled'])
    cp={'U5-L22':'U5-K-018','U5-L23':'U5-K-079'}.get(b['locus_id']) if checkpoint else None
    scenes.append({
      'scene_index':idx,'locus_id':b['locus_id'],'locus':b['scene_title'],'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['micro_anchor'],'scene_layout':{'orientation':b['orientation_sentence'],'zones':zones_for(b)},
      'cast':make_cast(b),'continuity_object':J4['continuity_object'],
      'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':make_beats(b),'memory_snapshot':make_snapshot(b),
      'misconception_guards':b['misconception_guards'],'exit_memory':b['exit_memory'],
      'checkpoint':checkpoint,'checkpoint_object_id':cp,'checkpoint_prompt':q.get('candidate_prompt','') if checkpoint else '',
      'checkpoint_answer':q.get('answer','') if checkpoint else '',
      'checkpoint_hint':('Return to the fixed genotype/phenotype bench or the two-law gate and reconstruct what the allele cards physically did before naming the term.' if checkpoint else ''),
      'next_locus':briefs[idx+1]['scene_title'] if idx+1<len(briefs) else None,'causal_transition':b['causal_transition']['transition_logic'],
    })

journey={
 'palace_id':'U5-J4','unit_id':'unit-5','palace_name':'Mendelian Inheritance Estate','story_title':'The Estate That Mistook the Grid for Inheritance',
 'tagline':'Repair one breeding estate so allele biology, meiosis, cross design, gamete formation, Punnett models, and classic ratios return to their proper causal order.',
 'guide':GUIDE,
 'premise':'The Mendelian Inheritance Estate still produces pea offspring, but its record system has made symbols and grids look like the causes of inheritance. Generation labels are shuffled, letter case is treated as biological strength, phenotype is confused with genotype, the two Mendelian laws share one gate, cross types are chosen by grid size, and the Punnett board claims that it separates alleles. The estate can be repaired only by following one pea-line breeding ledger from parental cross to offspring probabilities while the real chromosome and gamete processes stay visible.',
 'mission':'Follow Dr. Imani Reyes through seven connected locations. Rebuild the P, F1, and F2 sequence, identify alleles before assigning notation, separate genotype from phenotype, distinguish segregation from independent assortment, classify monohybrid, dihybrid, and testcross designs from the biological question, generate gametes before using a Punnett square, and finish by allowing the classic 3:1 and 9:3:3:1 phenotype ratios to appear only when their assumptions are satisfied.',
 'finale':'The breeding estate finally runs in causal order. Controlled crosses produce generations. Alleles occupy gene loci and can be represented by conventional symbols. Genotypes combine alleles, phenotypes express measurable outcomes in context, meiosis distributes alleles into gametes, cross design defines the question, Punnett squares organize possible gamete combinations, and classic ratios remain conditional probability summaries. The grid no longer receives credit for the biology that happens in chromosomes, gametes, and fertilization.',
 'estimated_minutes':23,'scene_count':7,'checkpoint_count':2,'student_release':'DEVELOPER_PREVIEW_F4D',
 'learner_rule':'Follow the same pea-line breeding ledger through the estate. Let chromosomes and gametes do the biological work first, then use notation, cross labels, Punnett grids, and ratios to describe or model what happened. Optional Quick Recall appears only twice.',
 'route_orientation':'This is one continuous south-to-north estate route. Begin in the south breeding courtyard, enter the record gallery, cross the central glasshouse bench, pass through the north Mendelian Laws Gate, follow the hedge arbor into the modeling room, and climb to the upper ratio balcony. The same allele case and breeding ledger remain visible throughout.',
 'route':route,'scenes':scenes,'narrative_design':'U5-F4D-NARRATIVE-1.0'
}
(U5/'journeys').mkdir(exist_ok=True)
(U5/'journeys'/'U5-J4.json').write_text(json.dumps(journey,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
registry={
 'schema':'memory-palace-v2-unit5-f4d-journeys-1.0','unit_id':'unit-5','stage':'F4D','student_release':False,'preview_release':True,
 'journey_count':4,'scene_count':26,'checkpoint_count':9,
 'guided_journeys':[{k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']} for j in [J1,J2,J3,journey]]
}
(U5/'journeys-f4d.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
status={
 'unit_id':'unit-5','unit_number':5,'title':'Heredity','status':'F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','pipeline_status':'POLISHED_NARRATIVE_J1_J2_J3_J4_F4D',
 'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','student_release':False,'preview_release':True,
 'canonical_records':152,'review_flags_resolved':37,'teacher_ppt_slides':112,'ced_topics':5,'ced_atoms':34,'architecture_journeys':8,'architecture_loci':50,
 'scene_briefs':50,'preview_journeys':4,'preview_scenes':26,'preview_checkpoints':9,'journey_1_records':20,'journey_2_records':18,'journey_3_records':8,'journey_4_records':25,
 'next_gate':'F4E_JOURNEY5_ONLY_AFTER_F4D_PROSE_QA'
}
(U5/'status-f4d.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(U5/'status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
words=sum(len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs']))) for s in scenes)
manifest={'schema':'memory-palace-v2-unit5-f4d-release-manifest-1.0','unit_id':'unit-5','stage':'F4D','student_release':False,'preview_release':True,'journey_count':4,'scene_count':26,'checkpoint_count':9,'journey_4_records':25,'journey_4_narrative_words':words,'f1_canonical_records':152,'f2_permanent_loci':50,'f3_scene_briefs':50,'next_gate':'F4E'}
(U5/'f4d-release-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

course_path=ROOT/'content'/'ap-biology'/'course.json'; course=json.loads(course_path.read_text(encoding='utf-8'))
cu5=next(u for u in course['units'] if u['unit_id']=='unit-5')
cu5.update({'status':'F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','journey_count':4,'scene_count':26,'canonical_lock':'LOCKED_F1','source_status':'AUDITED_SCIENCE_LOCKED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVE_J1_F4A_J2_F4B_J3_F4C_J4_F4D','canonical_records':152,'review_flags_resolved':37,'ced_atoms':34,'teacher_ppt_slides':112,'student_release':False,'preview_release':True,'pipeline_stage':'UNIT5_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW_F4D'})
course_path.write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lock_files=['journeys/U5-J4.json','journeys-f4d.json','status-f4d.json','f4d-release-manifest.json']
lock={'schema':'memory-palace-v2-unit5-content-lock-f4d-1.0','unit_id':'unit-5','stage':'F4D','lock_status':'LOCKED_F4D_J4','student_release':False,'preview_release':True,'files':{}}
for rel in lock_files:
    p=U5/rel; lock['files'][rel]={'bytes':p.stat().st_size,'sha256':sha(p)}
(U5/'content-lock-f4d.json').write_text(json.dumps(lock,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines=['# Unit 5 F4D · Journey 4 Narrative','',f'## {journey["story_title"]}','',journey['tagline'],'','**Palace**  Mendelian Inheritance Estate  ','**Guide**  Dr. Imani Reyes  ','**Route**  '+' → '.join(x['locus'] for x in route),'']
for s in scenes:
    lines += [f"## {s['scene_index']+1}. {s['locus']} — {s['title']}",'',f"*{s['scene_kicker']}*",'']+s['story_paragraphs']+['']
(ROOT/'docs'/'UNIT5_F4D_JOURNEY4_STORY.md').write_text('\n'.join(lines),encoding='utf-8')
release=['# Unit 5 F4D Release','', 'Unit 5 F4D authors and locks Journey 4 only while preserving Journeys 1–3 byte-for-byte against their earlier narrative locks. Unit 5 remains a developer preview and is not student released.','', '## Accounting','', '- Journeys 1–3 preserved: **19 scenes / 46 records / 7 optional recalls**', '- Journey 4 authored: **7 scenes / 25 records / 2 optional recalls**', f'- Journey 4 narrative words: **{words}**', '- Total Unit 5 preview: **4 journeys / 26 scenes / 9 optional recalls**','', '## Scientific continuity','', '- Generation labels P, F1, and F2 remain tied to the crosses that produce them.', '- Allele identity remains distinct from uppercase/lowercase notation and from dominance.', '- Dominant does not mean common, stronger, better, or more evolutionarily successful.', '- Genotype remains distinct from phenotype, and phenotype retains environmental context.', '- The law of segregation remains a one-gene allele-separation principle; independent assortment remains conditional for unlinked or effectively independently assorting genes.', '- Cross type is classified from the genetic question and parental genotypes before a Punnett grid is built.', '- Gametes are generated from parental genotypes and meiotic rules before entering the Punnett square.', '- A Punnett square remains a probability model of possible gamete combinations and never becomes the inheritance mechanism.', '- The classic 3:1 and 9:3:3:1 ratios remain conditional predictions under specified crosses and assumptions.','', '## Release boundary','', 'No Unit 5 Memory Objects, Review runtime, Challenge Lab runtime, or student-facing Unit 5 release is created in F4D. Journeys 5–8 remain at the F3 scene-brief stage.','']
(ROOT/'docs'/'UNIT5_F4D_RELEASE.md').write_text('\n'.join(release),encoding='utf-8')
print(json.dumps({'journey':'U5-J4','scenes':7,'records':25,'checkpoints':2,'narrative_words':words,'student_release':False,'preview_release':True},indent=2))
