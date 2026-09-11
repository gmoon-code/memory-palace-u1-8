from __future__ import annotations
import json,re,hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content'/'ap-biology'/'unit-7'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()

CANON={r['knowledge_id']:r for r in read(U7/'source/canonical-unit7-f1.json')['canonical_catalog']}
F3=read(U7/'briefs/scene-briefs-f3.json')
B={b['locus_id']:b for b in F3['scene_briefs'] if b['journey_id']=='U7-J2'}
JB=read(U7/'briefs/journey-briefs-f3.json')
J2=next(j for j in JB['journeys'] if j['journey_id']=='U7-J2')
J1=read(U7/'journeys/U7-J1.json')

GUIDE={
 'name':'Dr. Imani Vale',
 'role':'evolutionary-systems curator',
 'visual':'charcoal field jacket, pale-green specimen gloves, a slim brass pointer, and a transparent population ledger clipped to her left forearm',
 'story_job':'keeps every population boundary, allele identity, population-size marker, generation, and movement event visible while allowing only the mechanism at the current station to change the gene pool'
}
CONTINUITY=J2['continuity_object']

ROUTE=[
 {'scene_index':0,'locus':'Population Gene-Pool Registry','short':'Gene pool','floor':'Island intake','symbol':'POOL'},
 {'scene_index':1,'locus':'Allele-Frequency Evolution Meter','short':'Frequency','floor':'Census bridge','symbol':'Δf'},
 {'scene_index':2,'locus':'Mutation Source Dock','short':'Mutation','floor':'Mutation dock','symbol':'MUT'},
 {'scene_index':3,'locus':'Random-Process Turntable','short':'Randomness','floor':'Sampling deck','symbol':'RND'},
 {'scene_index':4,'locus':'Genetic Drift Chamber','short':'Drift','floor':'Small-population chamber','symbol':'DRIFT'},
 {'scene_index':5,'locus':'Bottleneck Gate','short':'Bottleneck','floor':'Storm gate','symbol':'NARROW'},
 {'scene_index':6,'locus':'Founder Ferry','short':'Founder','floor':'Colony dock','symbol':'FERRY'},
 {'scene_index':7,'locus':'Gene-Flow Bridge','short':'Gene flow','floor':'Migration bridge','symbol':'FLOW'},
 {'scene_index':8,'locus':'Hardy-Weinberg Null-Model Station','short':'Null model','floor':'Model station','symbol':'HWE'},
 {'scene_index':9,'locus':'Five-Condition Control Room','short':'Conditions','floor':'Control tower','symbol':'5'},
 {'scene_index':10,'locus':'Allele-Frequency p/q Board','short':'p and q','floor':'Allele board','symbol':'p+q'},
 {'scene_index':11,'locus':'Genotype-Frequency Equation Board','short':'Genotypes','floor':'Expectation board','symbol':'p²'},
 {'scene_index':12,'locus':'Genotype-Count Allele Counter','short':'Count alleles','floor':'Counting desk','symbol':'2N'},
 {'scene_index':13,'locus':'Observed–Expected Comparison Desk','short':'Compare','floor':'Final audit desk','symbol':'OBS/EXP'},
]

ZONES={
'U7-L11':[
 ('left','Population membership counter','50 + 50','Two glass island enclosures each display exactly fifty reproducing diploid finches, keeping the population boundary visible before any allele tokens are pooled.'),
 ('center','Gene-pool registry','100 ALLELES','Two transparent tanks collect one hundred color-coded allele copies from each island at the focal two-allele locus while every token keeps its allele identity.'),
 ('right','Fixed-versus-variable allele shelves','FIXED / VARIABLE','One shelf shows a two-allele locus with both blue A and amber a copies, while a second shelf shows a different locus containing only one allele at frequency 1.0.')],
'U7-L12':[
 ('left','Generation-one allele counter','60 / 40','A sealed census window shows Island A at generation one with sixty blue A copies and forty amber a copies.'),
 ('center','Allele-frequency change meter','0.60 → 0.66','A vertical meter compares the proportion of blue A across two generations without assigning a mechanism yet.'),
 ('right','Generation-two allele counter','66 / 34','The second census window shows the descendant generation with sixty-six blue A copies and thirty-four amber a copies.')],
'U7-L13':[
 ('left','New-mutation input','NEW TOKEN','A separate marked locus feeds one ordinary allele copy through a replication window where a new violet allele identity can arise without reference to whether it will help or harm.'),
 ('center','Mutation source dock','NEW ALLELE','The dock records the change in allele identity and inserts the new violet copy into the relevant island gene pool while preserving the focal blue/amber Hardy-Weinberg locus untouched.'),
 ('right','Fitness-effect and generation-time panel','CONTEXT / CLOCK','Three context trays compare neutral, deleterious, and beneficial effects while two clocks separate per-replication mutation probability from number of generations per calendar time.')],
'U7-L14':[
 ('left','Mutation and sampling randomness side','BLIND','An opaque mutation window and a blind sampling hopper both operate without reading which allele would be useful in the current environment.'),
 ('center','Random-process turntable','CHANCE','A circular turntable mixes color-coded allele copies and draws them without phenotype or fitness labels.'),
 ('right','Allele-frequency outcome side','NEW COUNTS','A descendant tank displays whatever allele frequencies result from the chance draw, while the natural-selection comparison remains physically separate.')],
'U7-L15':[
 ('left','Small-population sampling side','SMALL N','Island A is reduced to a small breeding sample whose allele copies are drawn from the larger gene pool by chance.'),
 ('center','Genetic-drift chamber','SAMPLE','A transparent sampling cylinder converts the finite sample into the next generation without sorting by adaptive value.'),
 ('right','Variation-loss and nonadaptive outcome side','LOSS','The descendant gene pool can shift in frequency or lose an allele even though the chamber never examines phenotype or environmental advantage.')],
'U7-L16':[
 ('left','Large pre-bottleneck population','BEFORE STORM','Island B begins with a visibly large breeding population and a known focal allele distribution.'),
 ('center','Bottleneck gate','STORM','A storm shutter narrows passage to a small survivor sample while its blind filter ignores the focal allele identity.'),
 ('right','Survivor gene pool and examples','AFTER','The survivor gene pool is displayed beside black-robin and marble-trout evidence panels that emphasize severe demographic reduction and lost variation.')],
'U7-L17':[
 ('left','Source population dock','SOURCE','The large source island remains standing with its gene pool visible while only a small group prepares to leave.'),
 ('center','Founder ferry','FEW FOUNDERS','A small ferry carries a chance subset of reproducing individuals to an empty island without shrinking the source population into a bottleneck.'),
 ('right','New-colony gene pool and Amish example','COLONY','The new island begins with the founders’ nonrepresentative allele sample beside an Amish-community example of rare alleles becoming unusually common by chance.')],
'U7-L18':[
 ('left','Population A gene pool','ISLAND A','The first island displays its blue and amber focal alleles and a population-size marker before any migrant crosses.'),
 ('center','Gene-flow bridge and pollen transfer','MOVE','A bridge physically carries migrants or gametes across the population boundary, with a parallel plant panel showing pollen as another route of allele movement.'),
 ('right','Population B gene pool','ISLAND B','The second island receives the incoming allele copies and updates its frequency toward the source population when the populations began different.')],
'U7-L19':[
 ('left','Observed population input','p = 0.70','Island A freezes one two-allele locus with seventy blue copies and thirty amber copies as the actual observed allele input.'),
 ('center','Hardy-Weinberg equilibrium baseline','NULL MODEL','A neutral glass model generates the genotype proportions expected if the locus met the idealized non-evolving assumptions.'),
 ('right','Model-comparison output','COMPARE','Observed population data and model expectations remain in separate frames so disagreement triggers investigation rather than automatic claims of a particular mechanism.')],
'U7-L20':[
 ('left','Large-population and no-migration controls','N LARGE / NO FLOW','Two locked controls keep random sampling effects negligible and prevent allele copies from entering or leaving the modeled population.'),
 ('center','Random-mating control console','MATE RANDOMLY','A mating carousel mixes individuals with respect to the focal locus and can be switched to nonrandom mating for a controlled contrast.'),
 ('right','No-mutation and no-selection controls','NO MUT / NO SEL','Two additional controls keep allele identity fixed and remove genotype-dependent reproductive differences at the focal locus.')],
'U7-L21':[
 ('left','Allele-frequency p side','p = 0.70','Seventy blue allele copies occupy the left panel and are counted as one allele frequency at the focal two-allele locus.'),
 ('center','p + q = 1 board','TOTAL = 1','A central board receives the two allele frequencies and verifies that the complete two-allele inventory sums to one.'),
 ('right','Allele-frequency q side and genotype-frequency contrast','q = 0.30','Thirty amber allele copies remain distinct from a lower strip that groups whole individuals by AA, Aa, or aa genotype.')],
'U7-L22':[
 ('left','p² homozygote panel','0.49','The left expected panel represents the homozygous genotype containing two copies of the p-designated allele.'),
 ('center','2pq heterozygote panel','0.42','The center expected panel represents heterozygotes formed by the two possible p-by-q mating combinations.'),
 ('right','q² homozygote panel','0.09','The right expected panel represents the homozygous genotype containing two copies of the q-designated allele.')],
'U7-L23':[
 ('left','AA genotype-count bin','26 AA','Twenty-six observed AA individuals enter a bin that exposes both allele copies in every genotype.'),
 ('center','2N allele-copy counter','100 COPIES','Fifty diploid individuals are converted into one hundred total allele copies before any frequency is calculated.'),
 ('right','Aa and aa bins with allele-frequency output','18 Aa / 6 aa','Observed heterozygotes and aa homozygotes feed the same allele counter, producing seventy A copies and thirty a copies directly.')],
'U7-L24':[
 ('left','Observed genotype distribution','0.52 / 0.36 / 0.12','The actual sample remains visible as AA, Aa, and aa genotype frequencies derived directly from the observed counts.'),
 ('center','Observed-versus-expected comparison desk','OBS ≠ EXP','The center desk places observed frequencies beside the Hardy-Weinberg expectations of 0.49, 0.42, and 0.09 without declaring a cause.'),
 ('right','Recessive-phenotype inference panel','ONLY IF JUSTIFIED','A conditional panel permits a recessive phenotype to stand in for q² only when phenotype maps reliably to aa and Hardy-Weinberg assumptions are appropriate.')],
}

NARR={
'U7-L11':{
 'title':'Two Islands, Two Populations, and One Gene-Pool Alarm',
 'kicker':'Population genetics begins by fixing the population boundary and counting the alleles that actually belong to that population.',
 'paragraphs':[
  "A salt-bright wind seems to cross the room when the doors open onto the **Population Genetics Island Network**. The network is an indoor archipelago built around two enormous transparent tanks. On your **left**, a membership counter faces two glass island enclosures, each containing fifty tagged reproducing finches and a bright population-size marker. Directly **ahead**, the center registry holds two empty gene-pool tanks, each etched with one hundred narrow slots for allele copies. On your **right**, shelves are split into VARIABLE and FIXED sections. Dr. Imani Vale is already beside the center registry. She clips the transparent population ledger to the railing, checks the generation labels, and points to a red alarm flashing above the islands. GENE-POOL AUDIT FAILED. ALLELES ARE BEING COUNTED WITHOUT A POPULATION BOUNDARY.",
  "Imani does not touch the colored allele tokens yet. She first closes a glass boundary around the fifty reproducing finches on Island A. The birds outside that boundary disappear from the census screen. Only after the membership counter shows the same species, the same island area, and reproducing membership does she name the unit you are actually following. A **Population** is a group of individuals of the same species living in the same area that can contribute to a shared gene pool. The boundary is physical enough to remember. Individuals can enter or leave later, but the network must know which population each allele copy belongs to before a frequency has any meaning.",
  "The center registry now opens a small port beneath every bird. Two allele copies from the focal locus slide from each diploid individual into the transparent tank. Blue tokens carry allele A and amber tokens carry allele a. Island A begins with sixty blue copies and forty amber copies. Island B begins with the same count. Imani waits until all one hundred slots are filled and only then names the **Gene pool**. A gene pool consists of all alleles at all loci present in the reproducing members of a population. The tank is a representation of those alleles, not a replacement for the organisms. The population remains on the left. Its alleles are being inventoried in the center.",
  "On the right shelves, Imani pulls down two small locus trays. One tray contains both blue and amber copies. The other contains one hundred green copies and no alternative color at all. She points to the second tray. An allele is **Fixed allele** at a locus when its frequency is 1.0 and no alternative allele is present in that population at that locus. She keeps the word fixed attached to a frequency, not to how common a phenotype looks. The two-color tray beside it carries more allelic variation. A population with more allelic variation has greater genetic diversity than a population in which many loci are fixed. The shelves make fixation and diversity visible without pretending every locus must contain the same number of alleles.",
  "The alarm above the islands dims from red to amber. Imani writes three lines into the ledger. POPULATION BOUNDARY. GENE POOL. ALLELE INVENTORY. Then she places a transparent cover over both gene-pool tanks so no token can drift, migrate, mutate, or disappear without leaving a recorded event. The main focal locus remains blue A and amber a. A second marked locus will be available later if the network needs to demonstrate the origin of a new allele without destroying the two-allele model required downstream.",
  "A narrow bridge rises from the registry and points toward two census windows. The left window is stamped GENERATION ONE. The right window is stamped GENERATION TWO. Island A still shows sixty blue copies and forty amber copies in the first window, but the archived descendant census on the far side reads sixty-six blue and thirty-four amber. The network has detected a change and is demanding a verdict. The next station will decide what that change proves before anyone is allowed to guess what caused it."
 ]},
'U7-L12':{
 'title':'The Meter Can Detect Evolution Before It Knows the Cause',
 'kicker':'A change in allele frequency across generations is evidence that a population evolved, even when the mechanism has not yet been identified.',
 'paragraphs':[
  "The **Allele-Frequency Evolution Meter** stands on a glass bridge between two census towers. On your **left**, the generation-one counter freezes Island A at sixty blue A copies and forty amber a copies. Directly **ahead**, a tall center meter has a blue column marked 0.60 and an amber column marked 0.40. On your **right**, the generation-two counter shows the archived descendant population with sixty-six blue copies and thirty-four amber copies. Imani locks both generation labels in place before touching the meter. The birds themselves are not carried from one tower into the other. The two windows represent different generations of the population.",
  "Imani converts the token counts into proportions. In generation one, blue A is sixty out of one hundred allele copies, so its frequency is 0.60. In the descendant generation, blue A is sixty-six out of one hundred, so its frequency is 0.66. The center column rises. Amber a falls from 0.40 to 0.34. The meter makes only one claim. **Allele-frequency change as evidence of evolution** means that a change in allele frequencies across generations is evidence that a population is evolving. The evidence is population-level and generational. No single finch has changed from one allele into another merely because time passed.",
  "Only after the two censuses are visibly different does Imani use the shorter term **Microevolution**. Microevolution is change in allele frequencies within a population across generations. The word is attached to the measurable population change on the meter. The network still has no permission to label the cause. Natural selection could alter allele frequencies under some conditions. Chance sampling could alter them. Gene flow could add or remove copies. Mutation could introduce a new allele. The meter does not decide among those mechanisms simply by noticing that 0.60 became 0.66.",
  "The broken network tries to flash NATURAL SELECTION above the center column. Imani removes the label and replaces it with MECHANISM UNKNOWN. She points back toward Journey 1 on a distant wall where selection required heritable phenotypic variation and differential reproductive success. None of that evidence has been supplied here. The meter is deliberately modest. It tells you what changed, not why. That separation matters whenever population data are interpreted. Observing evolution and identifying the mechanism are different inferential jobs.",
  "Imani copies the two frequencies into the transparent ledger and circles the generation numbers. The original sixty-to-forty census remains preserved as a reference. The sixty-six-to-thirty-four descendant census becomes the current Island A state. Island B remains at sixty blue and forty amber, giving the network a second population whose gene pool has not followed the same trajectory. The difference between the islands is now visible but unexplained.",
  "A metal dock door opens below the bridge. On its left side sits a replication window with a row of ordinary allele copies. One copy is about to acquire a new violet identity at a separate marked locus. On the right, three trays wait under the labels NEUTRAL, DELETERIOUS, and BENEFICIAL, while two clocks tick at different generation speeds. The next room will show how a new allele can enter a population without allowing the environment to order the mutation it needs."
 ]},
'U7-L13':{
 'title':'The Mutation Dock Makes a New Allele Without Asking Whether It Helps',
 'kicker':'Mutation introduces new alleles, while the fitness effect of a mutation depends on context and generation time must not be confused with mutation probability per replication.',
 'paragraphs':[
  "The **Mutation Source Dock** is built beside the island tanks like a customs station for new genetic variants. On your **left**, a narrow replication window holds a row of ordinary green allele copies from a second marked locus. Directly **ahead**, the center dock has one empty slot glowing violet. On your **right**, three shallow trays are labeled NEUTRAL, DELETERIOUS, and BENEFICIAL, and above them two clocks run at different speeds. Imani keeps the main blue A and amber a Hardy-Weinberg locus sealed behind clear glass. The network can demonstrate mutation here without turning the later two-allele model into a three-allele equation.",
  "The replication window closes around one green allele copy. No environmental label enters with it. A small copying change occurs and the token emerges violet. Imani slides the violet token into Island B's second-locus gene pool. Only after the new identity is visible does she state the relationship. **Mutation adds genetic variation** because mutation can introduce a genetic variant that was not previously present. The new allele was not produced because the island needed it. The copying event is random with respect to whether the resulting variant will improve fitness in the current environment.",
  "Imani places the violet copy under the center title **Mutation creates new alleles**. Mutation is the ultimate source of new alleles. Recombination and sexual reproduction can create new combinations of existing alleles, but they do not manufacture a brand-new allele sequence in the same sense. She then moves the token toward the right trays but refuses to let the network choose a tray before an environment and phenotype consequence are specified. Mutations can be neutral, deleterious, or beneficial with respect to fitness, and their effects can depend on genomic context and environment. Many are neutral or nearly neutral, deleterious mutations occur, and beneficial mutations are comparatively rare.",
  "The dock next displays **Mutation supplies selectable variation**. A new allele can eventually contribute to phenotypic variation on which natural selection can act. The sequence matters. Mutation introduces variation first. Selection can later change the frequency of a heritable variant if that variant affects reproductive success in a given environment. Imani keeps the mutation window on the left and the selection-related consequence trays on the right so the origin of a variant cannot be confused with the later process that may favor or remove it.",
  "The two clocks above the right panel begin racing. One is labeled GENERATIONS PER YEAR and the other MUTATION PROBABILITY PER REPLICATION. A bacterial example on the fast clock cycles through many generations while the per-replication dial stays unchanged. Imani names the final relationship, **Generation time and evolutionary rate**. Short generation times can allow more generations, and therefore more opportunities for mutation and selection, to occur per unit calendar time. That does not mean every prokaryote has a universally higher mutation probability per nucleotide each time DNA is copied.",
  "The violet mutation remains on the second-locus tray as a permanent record of where a new allele came from. The focal blue and amber locus is still untouched. Ahead, a circular metal platform is spinning in darkness. Its scoops cannot see allele color, phenotype, or reproductive success. The network has been calling every random outcome natural selection. The next station will separate randomness itself from the nonrandom sorting logic you repaired in Journey 1."
 ]},
'U7-L14':{
 'title':'The Turntable Is Blind to What Would Be Useful',
 'kicker':'Random processes can alter genetic composition, but natural selection is not random differential change.',
 'paragraphs':[
  "The **Random-Process Turntable** occupies a round room whose floor rotates slowly beneath a black canopy. On your **left**, two devices sit side by side. One is the mutation window from the previous dock. The other is an opaque sampling hopper connected to Island A's focal blue and amber allele tank. Directly **ahead**, the center turntable has ten covered cups that spin too quickly for anyone to track which color enters which cup. On your **right**, a descendant-frequency panel waits with blank blue and amber columns. Imani fixes the Island A starting count above the room so the reference cannot disappear while chance operates.",
  "She starts with the conceptual boundary. Some evolutionary changes involve stochastic events. Mutation occurrence is random with respect to fitness. Finite sampling of allele copies from one generation into another can also be random. Imani names the broad relationship **Random processes in evolution** only after both blind devices are visible. Random processes can alter the genetic composition of populations. The word random describes how the relevant event occurs with respect to fitness or which copies happen to be sampled. It does not mean the population has no biological rules or that every mechanism of evolution is random.",
  "The turntable now receives a set of blue and amber copies from Island A. No phenotype label is attached to any cup. The apparatus does not ask which allele would improve seed handling, mate attraction, or survival. It simply samples. When the cups open on the right, the frequency can differ from the starting value because the sample contains a chance excess of one color. Imani marks the relationship **Random processes change allele frequencies**. Chance processes can change allele frequencies and thereby contribute to population evolution.",
  "A second screen tries to place NATURAL SELECTION under the same rotating table. Imani shuts it off. Natural selection is different. Selection is nonrandom differential reproductive success among heritable phenotypes under environmental conditions. It does not operate by blindly drawing colored tokens. The origin of mutation can be random with respect to fitness, and genetic drift is a chance sampling process. Gene flow, which you have not reached yet, depends on actual movement of individuals or gametes across population boundaries. Keeping those mechanisms physically separate is more useful than memorizing them as one undifferentiated list.",
  "Imani runs the turntable twice with the same starting frequencies. The two descendant panels do not match exactly. In one run blue increases. In another amber increases. There is no consistent direction toward an adaptive outcome because the apparatus never measures fitness. That variability is the signature the next room will magnify. If the reproducing population is small, each sampled allele copy represents a larger fraction of the next generation, so chance can push frequencies much farther.",
  "The canopy lifts and reveals a narrow door marked SMALL POPULATION. Island A's population-size marker, which had shown fifty diploid breeders, begins dropping toward eight. The blue and amber tokens do not know which copies will be included in the small reproductive sample. Imani carries the ledger into the chamber. The next station will give this finite-sampling process its specific name and show why it can erase genetic variation without making the population better adapted."
 ]},
'U7-L15':{
 'title':'Eight Breeders Are Enough for Chance to Move the Whole Population',
 'kicker':'Genetic drift is chance allele-frequency change, strongest in small populations, capable of reducing diversity and producing divergence without being adaptive.',
 'paragraphs':[
  "The **Genetic Drift Chamber** is smaller than every room before it. On your **left**, Island A's full reference gene pool remains visible behind glass, but the population-size marker drops from fifty diploid breeders to only eight. Directly **ahead**, a clear sampling cylinder receives allele copies from those few breeders and prepares the descendant generation. On your **right**, two narrow displays wait. One tracks loss of allelic variation and the other compares Island A with Island B. Imani pins the starting frequency above the chamber and turns off every phenotype and fitness label. The chamber is allowed to sample. It is not allowed to select.",
  "A blind gate admits the allele copies contributed by the small breeding sample. By chance, the sample contains a higher proportion of blue A than the larger population did. The cylinder amplifies that sample into the displayed next-generation gene pool, and Island A settles at seventy blue copies and thirty amber copies. Only now does Imani name **Genetic drift**. Genetic drift is a nonselective change in allele frequency caused by chance, especially influential in small populations. Nothing in the chamber identified blue as useful or amber as harmful.",
  "Imani repeats the simulation beside the first result. In a large population, an unusual sample of a few allele copies changes the total frequency only slightly because each copy represents a small fraction of the population. In the eight-breeder run, every sampled copy carries more proportional weight. The chamber therefore demonstrates why **Drift is strongest in small populations**. Random sampling effects have larger proportional impacts on allele frequencies in small populations than in large populations.",
  "On the right, a third trial starts with a rare violet allele at another locus. The random sample happens to omit it completely. The descendant population contains no violet copy. Imani marks **Drift can reduce genetic variation**. Genetic drift can randomly eliminate alleles and thereby reduce within-population genetic variation. She immediately adds the second guard. **Drift is nonadaptive**. Genetic drift changes allele frequencies by chance and does not consistently increase adaptation. A lost allele might have been useful, harmful, or neutral under a later environment. Drift does not inspect that future.",
  "The second right-side display compares the two island tanks. Island B did not pass through the small-population chamber and still carries a different focal frequency. Island A now stands at seventy blue and thirty amber. The populations have diverged even though no selective pressure was imposed. This is **Drift can drive population divergence**. Genetic drift can make a small population diverge genetically from other populations of the same species.",
  "The chamber shutters close for the optional recall. The left reference tank remains visible, the center blind sampler is covered, and the right frequency shift stays on screen. If you can explain why a small population changed without any phenotype being favored, you can retrieve the mechanism. When the cover opens, a storm siren begins outside. Island B's large population is about to be forced through a gate so narrow that only a few survivors will remain. The next room will show how a demographic crash can produce a specific kind of drift without pretending every death in a disaster is automatically random."
 ]},
'U7-L16':{
 'title':'The Storm Shrinks the Population Before the Gene Pool Can Recover',
 'kicker':'A bottleneck is genetic drift when a severe population reduction leaves a chance, nonrepresentative sample of the previous gene pool.',
 'paragraphs':[
  "The **Bottleneck Gate** is built into a concrete seawall. On your **left**, Island B appears as a broad enclosure with its large pre-storm population and known allele counts still illuminated. Directly **ahead**, a heavy center gate has narrowed to a slot just wide enough for a handful of survivors. Wind and rain hammer the glass, but the gate's focal-allele sensor is deliberately switched off. On your **right**, the survivor gene pool sits beside two evidence panels showing the Chatham Island black robin and marble trout. Imani records the pre-storm population size before the alarm reaches its peak.",
  "The storm model forces a severe demographic reduction. At the focal blue and amber locus, the gate does not preferentially admit one color. The small survivor group is therefore a chance, nonrepresentative sample of the earlier gene pool. In this run, the survivor-derived display expands back to one hundred visible copies as eighty-five blue and fifteen amber, preserving the survivors' altered frequency while the population-size history stays marked as a crash. Imani names the specific process **Bottleneck effect**. A bottleneck is genetic drift following a severe population-size reduction that leaves a nonrepresentative sample of the original gene pool.",
  "Imani stops the storm and makes a qualification visible. A real population decline can contain selective and nonselective components. If a disease kills one genotype more often because of a heritable susceptibility, that part of the change can involve selection. The sampling component is genetic drift when survival with respect to the focal alleles is effectively chance. The network is not allowed to label every disaster a bottleneck-driven genetic change simply because many organisms died. The mechanism depends on how the surviving gene pool was sampled.",
  "On the right, the black-robin panel shows how a population reduced to only a few individuals can lose genetic variation even if later conservation increases census size. The marble-trout panel shows repeated mortality events that can likewise create severe bottlenecks and reduce diversity when the surviving population is a small sample. Imani keeps both examples beside the survivor tank so the important consequence is not the drama of the disaster. It is the altered representation of alleles among the survivors and their descendants.",
  "The storm clears. Island B's survivor-derived display now differs sharply from its pre-storm state. Imani leaves the original large population frozen on the left for comparison and locks the narrow gate in the center. Then she points toward a calm harbor on the far side of the seawall. A small ferry is boarding individuals from a population that is not collapsing at all.",
  "That difference is the next diagnostic task. A bottleneck begins with a severe reduction of an existing population. The **Founder effect** begins when a small subset leaves or otherwise establishes a new population. Both are chance sampling and both can make allele frequencies unlike the source, but the physical histories are different. The ferry horn sounds. The source island remains full behind you while a few colonists depart."
 ]},
'U7-L17':{
 'title':'The Source Island Stays Full While a Tiny Colony Carries Away a Chance Sample',
 'kicker':'Founder effect occurs when a small founding group establishes a new population with allele frequencies that can differ by chance from the source population.',
 'paragraphs':[
  "The **Founder Ferry** waits at a bright wooden dock. On your **left**, the source population remains large, its finches and allele tank still visible behind the railing. No storm has reduced it. Directly **ahead**, the center ferry has room for only a few reproducing individuals, each carrying the alleles that happen to be present in that small group. On your **right**, an empty island tank is labeled NEW COLONY, and beside it a historical population-genetics panel describes rare alleles in particular Amish communities. Imani makes you look back at the intact source population before anyone boards.",
  "Five breeding pairs are selected for the ferry without sorting them by the focal allele. Their twenty focal-locus allele copies are a small sample of the source gene pool. By chance, twelve are blue and eight are amber, so the founders begin at 0.60 and 0.40 even though the source display behind them remains at 0.85 and 0.15. When the ferry reaches the right island, those few individuals become the starting gene pool for the colony. Only after the population boundary is established does Imani name the **Founder effect**. The founder effect is genetic drift when a new population is established by a small subset whose allele frequencies differ by chance from the source population.",
  "The source population on the left remains nearly unchanged because it was not forced through a severe demographic crash. That makes the contrast with the bottleneck gate easy to reconstruct. In a bottleneck, an existing population becomes very small. In a founder event, a small group establishes a new population elsewhere or otherwise becomes reproductively separated. Both involve chance sampling. Neither process consistently makes the new gene pool more adaptive.",
  "The new colony grows in the display. Because all descendants initially inherit alleles from the small set of founders, an allele that was rare in the source can become relatively common in the colony. Imani points to the Amish-community example on the right. High frequencies of some rare alleles in particular communities can illustrate a founder effect when the original founding population carried a nonrepresentative set of alleles. The explanation is not that the founders had an unusually high number of new mutations. The frequency difference can arise because of which alleles the small founding group happened to carry.",
  "The ferry returns empty and the two island tanks remain side by side. Their allele frequencies are now more different than the network began with. A warning appears between them. DIVERGENCE INCREASING. Imani does not call this speciation. The populations have different gene pools, but gene flow could still reconnect them if individuals or gametes move across the boundary.",
  "A steel bridge unfolds from Island A toward Island B. Unlike the blind drift chamber, the bridge has transparent lanes. Every allele copy that crosses will have a visible carrier. A plant panel above the bridge releases a cloud of fluorescent pollen toward a second population. The next station will show a mechanism that changes allele frequencies through movement rather than blind sampling and that often pulls diverging populations back toward one another."
 ]},
'U7-L18':{
 'title':'This Time the Alleles Cross the Boundary in Plain Sight',
 'kicker':'Gene flow changes population allele frequencies through movement of fertile individuals or gametes and tends to reduce genetic differences between connected populations.',
 'paragraphs':[
  "The **Gene-Flow Bridge** spans two illuminated island tanks. On your **left**, Population A displays its current focal allele frequency, with blue and amber copies still individually countable. Directly **ahead**, the center bridge is transparent from end to end. Every migrant that crosses carries visible allele tags, and an upper channel shows fluorescent pollen moving from one plant population toward another. On your **right**, Population B begins with a different allele frequency left by its earlier demographic history. Imani places the drift turntable's opaque scoop on a shelf behind you. Nothing in this room is allowed to move invisibly.",
  "A fertile finch leaves Population A and settles in Population B, later contributing alleles to the recipient population. The corresponding token copies physically cross the bridge. Imani lets the receiving gene-pool tank update and then names **Gene flow**. Migration of fertile individuals or gametes can add or remove alleles from a population through gene flow. The diagnostic evidence is movement across a population boundary. The change is not being produced by a blind sample from within one population.",
  "The upper channel repeats the idea with plants. Pollen carries alleles from one plant population to another, demonstrating **Pollen-mediated gene flow**. The pollen grain is not a whole migrant plant, yet it can transport genetic material that enters the recipient gene pool through reproduction. Imani keeps the finch lane and pollen lane parallel so the learner remembers that gene flow can occur through fertile individuals or through gametes.",
  "Population A enters the bridge at 0.70 blue and 0.30 amber, while Population B remains at 0.85 blue and 0.15 amber after its bottleneck history. Several fertile migrants from the larger Population A contribute alleles to B, including amber copies that were rarer there. The B display shifts toward 0.80 blue and 0.20 amber, while A remains 0.70 and 0.30 to the displayed precision because the modeled migrant group is small relative to the source population. Imani marks **Gene flow counteracts divergence**. Gene flow between populations tends to reduce genetic differences and can hinder divergence into separate species. The word *tends* remains visible because the effect depends on movement direction and the allele frequencies of the connected populations.",
  "The network flashes a false comparison. DRIFT EQUALS GENE FLOW. Imani clears it. Drift changes frequencies through chance sampling within populations and is especially powerful when populations are small. Gene flow requires actual movement across a population boundary. Both can change allele frequencies, but the physical event is different. She has you point first to the opaque drift sampler behind you, then to the transparent bridge in front of you. One is chance sampling. The other is migration.",
  "The bridge locks after the optional recall. Population A is left with a clean focal two-allele census of seventy blue copies and thirty amber copies. Imani circles that island in the ledger. From this point forward, the network will stop imposing storms, ferries, mutation, and migration on that focal locus. A white control tower rises ahead with the words NULL MODEL illuminated across its center. The next station will ask what genotype distribution would be expected if the focal locus were placed under an idealized set of non-evolving conditions."
 ]},
'U7-L19':{
 'title':'The Baseline Is a Question, Not a Claim That Nature Must Obey',
 'kicker':'Hardy-Weinberg equilibrium is an idealized, locus-specific null model used to generate expectations for a non-evolving population.',
 'paragraphs':[
  "The **Hardy-Weinberg Null-Model Station** is quiet after the storms and bridges. On your **left**, the observed Island A input is sealed at the focal two-allele locus with seventy blue copies and thirty amber copies. Directly **ahead**, a clear model chamber is labeled HARDY-WEINBERG BASELINE. On your **right**, an empty comparison frame waits for observed and expected genotype distributions. Imani removes the second-locus violet mutation tray from the working table. The model now focuses only on the blue and amber two-allele locus, preserving exactly the condition the later equations require.",
  "Imani begins with what the model is for. The center chamber does not describe every real population. It creates an idealized baseline. **Hardy-Weinberg equilibrium as null model** provides a null model for allele and genotype frequencies expected at a locus in a non-evolving population. The phrase *at a locus* stays illuminated because the assumptions and evidence apply to the focal locus being modeled, not automatically to an organism's entire genome or every population trait.",
  "The seventy-to-thirty allele input enters the model without changing. The chamber calculates what genotype frequencies would be expected if the relevant Hardy-Weinberg conditions were satisfied. Imani names the related **Hardy-Weinberg null hypothesis**. Hardy-Weinberg expectations provide a baseline against which observed genotype and allele data can be compared to evaluate whether evolutionary mechanisms may be acting at a locus. The model gives the network something precise to compare against.",
  "A red detector tries to interpret any observed-versus-expected difference as proof of natural selection. Imani disables it. A deviation from Hardy-Weinberg expectations is a signal to investigate the model assumptions and data. It does not identify one mechanism automatically. The population might be small, migration might occur, mutation might alter alleles, mating might be nonrandom, or reproductive success might differ among genotypes. Some assumption violations can alter genotype proportions without changing allele frequencies.",
  "Imani leaves the observed seventy blue and thirty amber copies visible on the left. The center model remains transparent rather than prophetic. On the right, two empty slots are labeled OBSERVED and EXPECTED. The separation is permanent. Actual counts come from a population sample. Expected values come from the model under specified assumptions. Mixing those categories would make every later equation meaningless. The baseline is therefore a disciplined comparison question, not a target that real populations are expected to approach on purpose. If the observed pattern fits the model closely, the model remains a useful null description for that locus. If it does not, the next step is to investigate assumptions and evidence rather than invent a mechanism from the difference alone.",
  "Five locks click open above the station. Two controls slide toward the left wall, one appears in the center, and two move to the right wall. The model cannot be interpreted until every condition is understood separately. Imani carries the unchanged p and q input into the next room, where the network will test what happens when one assumption is changed while the other four remain visible."
 ]},
'U7-L20':{
 'title':'Five Controls Hold the Null Model Still',
 'kicker':'Hardy-Weinberg equilibrium depends on five model conditions, and nonrandom mating alone can change genotype frequencies without necessarily changing allele frequencies.',
 'paragraphs':[
  "The **Five-Condition Control Room** surrounds the null-model chamber like a control tower. On your **left**, two large switches read LARGE POPULATION and NO MIGRATION. Directly **ahead**, the center console controls mating pattern at the focal locus. On your **right**, two more switches read NO MUTATION and NO NATURAL SELECTION. Imani places Island A's seventy blue and thirty amber allele copies on a locked strip above the room. The aim is not to memorize five phrases as floating rules. Each control must visibly prevent one process from disturbing the model.",
  "Imani engages the first left switch. The **Hardy-Weinberg condition large population** means the model assumes a sufficiently large population so random sampling effects are negligible. The drift chamber you visited earlier showed why this matters. A small reproducing population can move allele frequencies by chance. The second left switch establishes the **Hardy-Weinberg condition no migration**. No individuals or gametes cross the population boundary, so gene flow cannot add or remove alleles at the focal locus.",
  "On the right, the first switch establishes the **Hardy-Weinberg condition no mutation**. No new mutation changes the alleles at the modeled locus. The second right switch establishes the **Hardy-Weinberg condition no natural selection**. Genotypes at that locus do not differ in reproductive success. Imani keeps the mutation dock and fitness scale mentally separate. One control prevents allele identity from changing by mutation. The other prevents differential reproductive contribution from changing the representation of genotypes through selection.",
  "The center mating console is the subtle one. The **Hardy-Weinberg condition random mating** means mating is random with respect to the locus. Imani first lets the carousel mix genotypes randomly. Then she deliberately switches to assortative mating while keeping the allele-copy totals locked at seventy blue and thirty amber. The genotype pattern changes. More like-with-like matings can change the proportions of homozygotes and heterozygotes, yet the p and q allele frequencies can remain the same. This is why nonrandom mating alone does not automatically prove allele-frequency evolution.",
  "Imani toggles each control one at a time while the other four remain fixed. The network logs which process was permitted and which population quantity changed. She refuses to let the conditions collapse into a single sentence that says any violation equals microevolution. A violation tells you the null model may not apply as written. You still have to determine whether allele frequencies changed, genotype frequencies changed, or both, and which mechanism can explain the pattern.",
  "The five controls go dark for the optional recall, but their physical positions remain. Large population and no migration stay on the left, random mating stays in the center, and no mutation plus no natural selection stay on the right. When the labels return, the model chamber sends the same seventy blue and thirty amber copies into a long counting board. The next room will give those two allele frequencies names, but it will not let dominance decide which symbol is p and which is q."
 ]},
'U7-L21':{
 'title':'p and q Are Labels for Allele Frequencies, Not Dominance Badges',
 'kicker':'For a two-allele locus, p and q describe allele frequencies that sum to one, while genotype frequency remains a different population quantity.',
 'paragraphs':[
  "The **Allele-Frequency p/q Board** stretches across a narrow counting hall. On your **left**, seventy blue A tokens fill a transparent panel. Directly **ahead**, a central equation board waits with two empty boxes joined by a plus sign and an equals-one marker. On your **right**, thirty amber a tokens occupy a second panel, while a lower strip groups whole individuals into AA, Aa, and aa boxes. Imani places the population-size marker at fifty diploid individuals so the one hundred total allele copies remain visible throughout the room.",
  "She begins on the left by dividing seventy blue copies by the one hundred total allele copies. The result is 0.70. That proportion is an **Allele frequency**, the proportion of all allele copies at a locus represented by a particular allele. The population boundary and locus are part of the meaning. The number is not the fraction of individuals that look dominant. It is a count of allele copies within the gene pool.",
  "On the lower right strip, Imani groups the same fifty individuals by genotype. The proportions of AA, Aa, and aa individuals are **Genotype frequency**, the proportion of individuals in a population with a particular genotype. She keeps the genotype boxes physically below the allele-copy panels. An allele frequency counts copies of an allele. A genotype frequency counts individuals carrying a particular pair of alleles. The two quantities are related, but they are not interchangeable.",
  "Imani now assigns the blue allele the symbol p. The left label reads **p as allele-1 frequency**. In Hardy-Weinberg notation, p is the frequency of one allele at a two-allele locus. It is not inherently the dominant allele. She assigns amber the symbol q. The right label reads **q as allele-2 frequency**. q is the frequency of the other allele and is not inherently recessive. If you swapped the letters used for the two alleles consistently, the biology would not change.",
  "The two frequencies slide into the center board. 0.70 plus 0.30 equals 1. The board names the **Allele-frequency equation p + q = 1**. For a two-allele locus, the allele frequencies sum to one because the two categories account for every allele copy at that locus. Imani leaves a bright TWO-ALLELE condition above the equation so the learner does not carry the formula into a locus with three or more alleles without modification.",
  "The center board now sends p and q forward without doing any genotype counting from the observed sample. Ahead, three expected-frequency panels rise from the floor. The left is labeled p², the center 2pq, and the right q². The next station will show what those expressions mean under Hardy-Weinberg assumptions. The network will be allowed to generate expectations, but it will not be allowed to quietly replace the observed genotype distribution with them."
 ]},
'U7-L22':{
 'title':'The Equation Board Builds Expected Genotypes From the Same p and q',
 'kicker':'Under Hardy-Weinberg equilibrium, p², 2pq, and q² are expected genotype frequencies and must remain distinct from directly observed genotype proportions.',
 'paragraphs':[
  "The **Genotype-Frequency Equation Board** opens into three luminous panels. On your **left**, the p² panel receives the blue allele symbol twice. Directly **ahead**, the center 2pq panel displays one blue and one amber copy in two possible mating-order combinations. On your **right**, the q² panel receives two amber symbols. Imani keeps p equal to 0.70 and q equal to 0.30 along the upper rail. A second rail below remains blank and is labeled OBSERVED GENOTYPE COUNTS. Nothing may enter that lower rail yet.",
  "The model uses the same allele frequencies from the previous room and applies the Hardy-Weinberg assumptions. The left panel computes 0.70 multiplied by 0.70 and displays 0.49. The center combines the two p-by-q orders and displays 2 times 0.70 times 0.30, or 0.42. The right panel displays 0.30 multiplied by 0.30, or 0.09. Only after all three model values are visible does Imani name the **Hardy-Weinberg genotype equation**. Under Hardy-Weinberg equilibrium for a two-allele locus, expected genotype frequencies are p² + 2pq + q² = 1.",
  "Imani points left. **p² expected homozygote frequency** is the expected frequency of the homozygous genotype containing two copies of the p-designated allele. She points to the center. **2pq expected heterozygote frequency** is the expected heterozygote frequency. Then she points right. **q² expected homozygote frequency** is the expected frequency of the homozygous genotype containing two copies of the q-designated allele. None of those labels contains the words dominant or recessive because p and q themselves do not.",
  "The three expected proportions sum to one. Imani allows the board to print an expected genotype distribution of 0.49, 0.42, and 0.09. Then she covers it with transparent glass and taps the empty observed rail below. The values came from a model using p and q under Hardy-Weinberg conditions. They were not counted directly from the fifty individuals in the actual island sample.",
  "The network tries to copy 0.49, 0.42, and 0.09 into the observed boxes. Imani blocks the transfer. If observed genotype counts happen to match those expectations closely, that is an empirical comparison. The equation cannot declare the observed population to have those genotype frequencies before the individuals are counted. That distinction also protects the later recessive-phenotype shortcut. q² can represent a recessive homozygote frequency only under the relevant model assumptions and phenotype-genotype mapping.",
  "The three panels darken for the optional recall. Their positions remain visible as empty outlines. If you can reconstruct which expected genotype frequency belongs on the left, center, and right and why the three add to one, the relationship is secure. When the values return, a physical counting desk rolls into view. Fifty actual genotype cards are waiting to be sorted. The next room will count allele copies directly and will not use a square root to guess frequencies from an arbitrary observed homozygote count."
 ]},
'U7-L23':{
 'title':'Count the Alleles You Actually Observed Before You Touch a Model',
 'kicker':'Allele frequencies from genotype counts come from direct allele-copy counting across 2N copies in a diploid sample.',
 'paragraphs':[
  "The **Genotype-Count Allele Counter** looks more like a sorting desk than an equation room. On your **left**, a bin holds twenty-six observed AA genotype cards. Directly **ahead**, the center counter is marked 2N and has one hundred narrow slots. On your **right**, two bins hold eighteen Aa cards and six aa cards, followed by a blue-and-amber allele-frequency output. Imani places a large N = 50 marker above the desk. These are observed individuals from Island A. No Hardy-Weinberg expectation has been used to create their genotype counts.",
  "Imani opens the twenty-six AA cards first. Each diploid AA individual contributes two A copies, so the left bin releases fifty-two blue tokens. The eighteen Aa cards contribute one blue A and one amber a each, adding eighteen of each color. The six aa cards contribute twelve amber copies. The center counter fills to exactly one hundred allele copies because fifty diploid individuals contain 2N allele copies at an autosomal locus.",
  "The blue total is seventy. The amber total is thirty. Imani names the relationship **Allele frequencies from genotype data**. Allele frequencies can be calculated from genotype frequencies or genotype counts in a population. The underlying act is direct allele accounting. Count the copies of the chosen allele and divide by the total number of allele copies.",
  "The counter then displays the more explicit rule **Allele frequency from genotype counts**. From observed diploid genotype counts, an allele frequency is found by counting copies of that allele and dividing by the total number of allele copies, 2N. For A, the numerator is two times the AA count plus the Aa count. For a, the numerator is two times the aa count plus the Aa count. The desk therefore recovers p = 0.70 and q = 0.30 directly from the observed genotype cards.",
  "A square-root button begins flashing beneath the aa bin. Imani removes its power. You cannot take the square root of an arbitrary observed aa frequency and automatically call the result q. That shortcut works only when the observed recessive phenotype reliably identifies aa and Hardy-Weinberg genotype proportions are justified. Here the allele copies are available directly, so direct counting is the scientifically secure method. She has you physically recount one heterozygote to reinforce the logic. Its A copy belongs in the blue total and its a copy belongs in the amber total. The heterozygote is one individual, yet it contributes two different allele copies to the 2N inventory. That is why genotype counts and allele counts cannot be substituted for one another without conversion.",
  "The desk sends two packets forward. One contains the observed genotype frequencies from twenty-six AA, eighteen Aa, and six aa individuals. The other contains the allele frequencies recovered directly from those same cards. The Hardy-Weinberg expected distribution from the previous room is carried separately under a transparent cover. The final audit desk ahead will compare the observed and expected genotype patterns without letting a difference identify its own cause."
 ]},
'U7-L24':{
 'title':'Observed and Expected Can Disagree Without Telling You Why',
 'kicker':'Hardy-Weinberg comparisons are diagnostic, and genotype-frequency departures must be interpreted separately from allele-frequency evolution.',
 'paragraphs':[
  "The **Observed–Expected Comparison Desk** occupies the highest platform in the island network. On your **left**, the actual sample remains visible as twenty-six AA, eighteen Aa, and six aa individuals, giving observed genotype frequencies of 0.52, 0.36, and 0.12. Directly **ahead**, the center desk displays the Hardy-Weinberg expected frequencies generated from the same p = 0.70 and q = 0.30, which are 0.49, 0.42, and 0.09. On your **right**, a conditional recessive-phenotype panel is locked behind two switches. PHENOTYPE MAPS RELIABLY TO aa and HARDY-WEINBERG ASSUMPTIONS APPROPRIATE.",
  "Imani places observed and expected distributions side by side without merging them. The relationship is **Observed versus expected genotype frequencies**. Observed genotype frequencies can be compared with Hardy-Weinberg expected frequencies, but interpretation requires attention to the model assumptions and the locus being tested. The difference tells you to investigate. It does not announce whether selection, migration, mutation, drift, nonrandom mating, sampling error, or another issue is responsible.",
  "The network tries one last shortcut. GENOTYPE DEVIATION EQUALS EVOLUTION. Imani freezes the focal allele-copy strip above the desk. p remains 0.70 and q remains 0.30 in a controlled projection while the mating console from the Five-Condition Control Room switches from random to assortative mating. The genotype proportions change, with homozygotes becoming more common and heterozygotes less common, yet the allele-copy totals remain fixed. This demonstrates **Nonrandom mating and allele frequency**. Nonrandom mating by itself can change genotype frequencies without changing allele frequencies.",
  "Imani turns to the right panel. If a phenotype is caused only by the aa genotype and the population is appropriately modeled by Hardy-Weinberg equilibrium, the frequency of that recessive phenotype can be treated as q² and used to estimate q. This is **Recessive phenotype inference under Hardy-Weinberg**. The two switches remain physically required. If phenotype does not uniquely identify aa, or if Hardy-Weinberg assumptions are not justified, the shortcut cannot be used safely.",
  "The red audit alarm that followed you from the first registry finally changes to green. Imani opens the ledger and traces the whole island route. A population boundary defined whose alleles belonged in the gene pool. Allele-frequency change established microevolution without naming a cause. Mutation introduced new alleles without asking what would be useful. Blind sampling created drift, bottlenecks, and founder effects. Migration created gene flow. The Hardy-Weinberg station then froze one two-allele locus and used p, q, p², 2pq, and q² only as model quantities under explicit conditions.",
  "Before the network closes, the two island tanks illuminate together. Every remaining blue and amber token still carries a traceable history. Imani does not ask you to calculate another problem here. Those procedures belong in later application practice. The permanent journey ends with a more important distinction. Observed allele copies, observed genotype counts, model assumptions, and expected genotype frequencies are different kinds of information. If you keep those categories separate, the equations stop being tricks and become what they were meant to be, a disciplined way to ask whether a population fits a non-evolving null model and what evidence should be investigated when it does not."
 ]},
}

CHECKPOINTS={'U7-L15','U7-L18','U7-L20','U7-L22'}

def clean_prose(text):
    text=text.replace(' — ', '. ').replace('—','-')
    text=text.replace(': ', '. ')
    return text

def word_count(paragraphs):
    return len(re.findall(r"\b[\w’′'-]+\b",' '.join(paragraphs)))

def zone_objs(lid):
    return [{'position':p,'label':label,'symbol':symbol,'description':description} for p,label,symbol,description in ZONES[lid]]

def cast_for(lid):
    items=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    for position,label,symbol,description in ZONES[lid]:
        items.append({'name':label,'kind':'scientific population, allele display, comparison, sampling mechanism, or model control','visual':description,'job':f"Remain fixed on the learner's {position} and carry the {position}-side scientific role required by the locked F3 geometry."})
    items.append({'name':'Island A gene-pool tank','kind':'persistent population genetics object','visual':'a clear tank of individually countable blue A and amber a allele copies with a population-size marker and generation label','job':'keeps the focal two-allele population history reconstructable through sampling, migration, and Hardy-Weinberg modeling'})
    items.append({'name':'Island B gene-pool tank','kind':'persistent population genetics object','visual':'a second clear tank with the same color and label conventions as Island A so divergence and gene flow can be compared directly','job':'provides a persistent comparison population whose allele copies move only through an explicitly shown mechanism'})
    items.append({'name':'Transparent population ledger','kind':'journey continuity recorder','visual':'a clear floating ledger with population boundary, generation, population size, allele counts, genotype counts, and movement history in separate fields','job':'records evidence without replacing the real population, allele copies, demographic event, or Hardy-Weinberg model'})
    return items

def beats_for(lid):
    b=B[lid]
    terms={t['knowledge_id']:t for t in b['term_introductions']}
    scene_hint={
      'U7-L11':'the left membership boundary, center allele tanks, and right fixed-versus-variable shelves',
      'U7-L12':'the generation-one and generation-two allele counters separated by the frequency-change meter',
      'U7-L13':'the new violet mutation token appearing before any fitness tray is chosen',
      'U7-L14':'the opaque chance sampler that cannot read phenotype or usefulness',
      'U7-L15':'the small breeding sample shifting allele frequency without any fitness sorting',
      'U7-L16':'the storm bottleneck leaving a chance survivor sample of the earlier gene pool',
      'U7-L17':'the intact source population and the tiny founder ferry establishing a separate colony',
      'U7-L18':'the visible migrant or pollen crossing the population boundary on the bridge',
      'U7-L19':'the observed two-allele input kept separate from the Hardy-Weinberg baseline model',
      'U7-L20':'the five spatial controls surrounding the null model',
      'U7-L21':'the seventy blue and thirty amber allele copies feeding p + q = 1',
      'U7-L22':'the left p², center 2pq, and right q² expected-genotype panels',
      'U7-L23':'the observed AA, Aa, and aa cards being converted directly into 2N allele copies',
      'U7-L24':'the observed genotype distribution kept separate from expected Hardy-Weinberg values and the conditional q² panel',
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
for i,lid in enumerate(J2['route']):
    b=B[lid]; n=NARR[lid]; route=ROUTE[i]
    paragraphs=[clean_prose(p) for p in n['paragraphs']]
    cp=lid in CHECKPOINTS
    scenes.append({
      'scene_index':i,'locus_id':lid,'locus':route['locus'],'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['micro_anchor'],'scene_layout':{'orientation':b['orientation_sentence'],'zones':zone_objs(lid)},
      'cast':cast_for(lid),'continuity_object':CONTINUITY,
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
 'palace_id':'U7-J2','unit_id':'unit-7','palace_name':'Population Genetics Island Network',
 'story_title':'The Island Network That Could Not Explain Its Missing Alleles',
 'tagline':'Two island gene pools keep changing for different reasons. Track every colored allele copy through mutation, chance sampling, migration, and the Hardy-Weinberg control tower until the network can finally tell an observed population from a model.',
 'guide':GUIDE,
 'premise':'The Population Genetics Island Network has failed its mechanism audit. Its automated report calls random sampling natural selection, confuses founder events with migration, labels p as dominant and q as recessive, and copies Hardy-Weinberg expectations into observed genotype boxes. Dr. Imani Vale seals two transparent island gene-pool tanks and requires every allele copy to leave a visible history before the network can reopen.',
 'mission':'Carry the same population identities through fourteen permanent locations. Define population and gene pool, detect microevolution, separate mutation from selection, distinguish drift, bottleneck, founder effect, and gene flow, then freeze one two-allele locus inside the Hardy-Weinberg station while keeping assumptions, allele frequencies, genotype frequencies, observed counts, and expected values physically separate.',
 'finale':'The network clears its audit only after every allele-frequency change has a reconstructable demographic or genetic event and every Hardy-Weinberg quantity is attached to the correct evidence category. Chance sampling, migration, mutation, selection-related assumptions, observed counts, and model expectations are no longer interchangeable.',
 'estimated_minutes':40,'scene_count':14,'checkpoint_count':len(CHECKPOINTS),
 'student_release':'DEVELOPER_PREVIEW_F4B','preview_release':True,'narrative_design':'U7-F4B-NARRATIVE-1.0',
 'learner_rule':'Read or listen while keeping the two island tanks, allele colors, population-size markers, and generation labels stable in your mind. Exact terms appear only after the defining mechanism or quantity is visible. The equations are shown conceptually here; calculation procedures remain application practice.',
 'route_orientation':'The network is one continuous indoor archipelago. Begin at the Population Gene-Pool Registry, cross the census bridge, mutation dock, chance turntable, drift chamber, storm bottleneck, founder ferry, and gene-flow bridge, then climb into the Hardy-Weinberg model station, five-condition control tower, p/q board, expected-genotype board, direct allele-count desk, and final observed-versus-expected audit desk.',
 'route':ROUTE,'scenes':scenes,
 'source_brief_lock':'LOCKED_F3','scientific_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2',
 'frozen_prior_journey_lock':'LOCKED_F4A_J1'
}

(U7/'journeys').mkdir(exist_ok=True)
(U7/'journeys'/'U7-J2.json').write_text(json.dumps(journey,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary={
 'schema':'memory-palace-v2-unit7-f4b-journeys-1.0','unit_id':'unit-7','stage':'F4B','student_release':False,'preview_release':True,
 'journey_count':2,'scene_count':24,'checkpoint_count':J1['checkpoint_count']+len(CHECKPOINTS),
 'guided_journeys':[
   {k:J1[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']},
   {k:journey[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']}
 ]
}
(U7/'journeys-f4b.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

status={
 'unit_id':'unit-7','number':7,'title':'Natural Selection','status':'F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','pipeline_stage':'F4B_JOURNEY2_NARRATIVE',
 'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3',
 'narrative_lock':'LOCKED_F4B_J1_J2','student_release':False,'preview_release':True,
 'journey_count':2,'scene_count':24,'memory_objects':0,'application_challenges':0,
 'canonical_records':215,'architecture_journeys':6,'architecture_bundles':23,'architecture_loci':55,'scene_briefs':55,'palace_managed_records':174,
 'challenge_lab_records':16,'scope_guard_records':25,'exact_name_review_targets':94,'confusable_sets':33,'optional_first_exposure_recalls':18,
 'f4a_journey':'U7-J1','f4a_scene_count':10,'f4a_knowledge_records':26,'f4a_exact_name_targets':15,'f4a_optional_recalls':3,
 'f4b_journey':'U7-J2','f4b_scene_count':14,'f4b_knowledge_records':47,'f4b_exact_name_targets':21,'f4b_optional_recalls':len(CHECKPOINTS),
 'next_required_output':'F4C polished narrative for Journey 3 only after Journeys 1 and 2 remain frozen and all F1-F4B gates continue to pass.'
}
(U7/'status-f4b.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(U7/'status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'
course=read(cp)
u=next(x for x in course['units'] if x['unit_id']=='unit-7')
u.update({
 'status':'F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','journey_count':2,'scene_count':24,'student_release':False,'preview_release':True,
 'source_status':'AUDITED_F1_ARCHITECTURE_F2_BRIEFS_F3_NARRATIVE_F4A_F4B','narrative_lock':'LOCKED_F4B_J1_J2','narrative_journeys':2,
 'pipeline_stage':'F4B_JOURNEY2_NARRATIVE'
})
cp.write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Reviewer story document.
doc=['# Unit 7 F4B · Journey 2 Narrative','','## The Island Network That Could Not Explain Its Missing Alleles','',journey['tagline'],'',
     '### Physical route','', ' → '.join(x['locus'] for x in ROUTE),'',
     '### Continuity rule','',CONTINUITY,'']
for s in scenes:
    doc += [f"## {s['scene_index']+1}. {s['locus']} · {s['title']}",'',f"*{s['scene_kicker']}*",'']
    doc += s['story_paragraphs']+['']
    if s['checkpoint']:
        doc += ['**Optional Quick Recall**','',s['checkpoint_prompt'],'']
(ROOT/'docs'/'UNIT7_F4B_JOURNEY2_STORY.md').write_text('\n'.join(doc),encoding='utf-8')

# Lock and release.
f4a=read(U7/'content-lock-f4a.json')
prior_files={}
for rel,meta in f4a['files'].items():
    prior_files[f'content/ap-biology/unit-7/{rel}']=meta
for rel in [
    'content/ap-biology/unit-7/journeys/U7-J1.json',
    'content/ap-biology/unit-7/content-lock-f4a.json',
    'content/ap-biology/unit-7/f4a-release-manifest.json',
    'docs/UNIT7_F4A_JOURNEY1_STORY.md',
    'docs/UNIT7_F4A_RELEASE.md',
    'docs/UNIT7_F4A_QA.md',
    'docs/UNIT7_F4A_PACKAGE_QA.md',
]:
    rp=ROOT/rel
    if rp.exists():
        prior_files[rel]={'bytes':rp.stat().st_size,'sha256':sha(rp)}
locked_rel=['journeys/U7-J2.json','journeys-f4b.json','status-f4b.json']
lock_files={rel:{'bytes':(U7/rel).stat().st_size,'sha256':sha(U7/rel)} for rel in locked_rel}
lock={
 'schema':'memory-palace-v2-unit7-f4b-lock-1.0','unit_id':'unit-7','lock_status':'LOCKED_F4B_J1_J2','student_release':False,'preview_release':True,
 'protected_prior_locks':['content-lock-f1.json','content-lock-f2.json','content-lock-f3.json','content-lock-f4a.json'],
 'f4a_journey1_protection':prior_files,
 'journey_id':'U7-J2','scene_count':14,'knowledge_record_count':47,'exact_name_target_count':21,'checkpoint_count':len(CHECKPOINTS),
 'files':lock_files,
 'rule':'Journey 1 remains frozen byte-for-byte. Journey 2 polished prose may not change after F4B without a new explicit narrative version. F1 science, F2 classification/geometry, and F3 scene briefs remain authoritative.'
}
(U7/'content-lock-f4b.json').write_text(json.dumps(lock,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
release={
 'schema':'memory-palace-v2-unit7-f4b-release-1.0','generated_utc':'2026-09-08T13:50:00+00:00','unit_id':'unit-7',
 'release_status':'F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','student_release':False,'preview_release':True,
 'completed_journeys':['U7-J1','U7-J2'],'journeys':2,'scenes':24,
 'f4b_journey_id':'U7-J2','f4b_scenes':14,'f4b_knowledge_records':47,'f4b_exact_name_targets':21,'f4b_optional_first_exposure_recalls':len(CHECKPOINTS),
 'canonical_records':215,'permanent_loci_architecture':55,'scene_briefs':55,'memory_objects':0,'application_challenges':0,
 'scientific_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','narrative_lock':'LOCKED_F4B_J1_J2',
 'next_stage':'F4C Journey 3 polished narrative after F4B regression'
}
(U7/'f4b-release-manifest.json').write_text(json.dumps(release,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

print(json.dumps({
 'journey':'U7-J2','scenes':14,'knowledge_records':47,'exact_name_targets':21,'checkpoints':len(CHECKPOINTS),
 'words':sum(s['narrative_word_count'] for s in scenes),
 'mean_words':round(sum(s['narrative_word_count'] for s in scenes)/14,1),
 'min_words':min(s['narrative_word_count'] for s in scenes),
 'max_words':max(s['narrative_word_count'] for s in scenes),
},indent=2))
