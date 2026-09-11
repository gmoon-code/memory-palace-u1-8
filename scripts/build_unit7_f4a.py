from __future__ import annotations
import json, hashlib, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content'/'ap-biology'/'unit-7'
BRIEFS=json.loads((U7/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS=json.loads((U7/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J1=next(j for j in JBRIEFS if j['journey_id']=='U7-J1')
B={b['locus_id']:b for b in BRIEFS if b['journey_id']=='U7-J1'}
CANON={r['knowledge_id']:r for r in json.loads((U7/'source'/'canonical-unit7-f1.json').read_text(encoding='utf-8'))['canonical_catalog']}

GUIDE={
 'name':'Dr. Imani Vale',
 'role':'evolutionary-systems curator',
 'visual':'charcoal field jacket, pale-green specimen gloves, a transparent population ledger that can display phenotype counts and allele frequencies, and a slim brass pointer used only to indicate real biological evidence',
 'story_job':'Imani keeps the same population ledger visible across generations, changes only one evolutionary variable or comparison at a time, and names a scientific term only after the defining population-level pattern or mechanism can be seen.'
}

CONTINUITY='the same transparent population ledger, always divided into phenotype categories, offspring contributed to the next generation, and a narrow allele-frequency strip; the biological example may change, but the ledger never replaces the organisms or evidence it records'

ROUTE=[
 {'scene_index':0,'locus':'Darwin Evidence Intake','short':'Evidence','floor':'Observatory entrance','symbol':'MAP'},
 {'scene_index':1,'locus':'Population Change Platform','short':'Population','floor':'Generation deck','symbol':'G→G'},
 {'scene_index':2,'locus':'Heritable Variation Field','short':'Variation','floor':'Field chamber','symbol':'VAR'},
 {'scene_index':3,'locus':'Competition and Offspring Gate','short':'Competition','floor':'Resource gate','symbol':'OFF'},
 {'scene_index':4,'locus':'Fitness Scale','short':'Fitness','floor':'Measurement hall','symbol':'FIT'},
 {'scene_index':5,'locus':'Changing Pressure Chamber','short':'Pressure','floor':'Environment chamber','symbol':'ENV'},
 {'scene_index':6,'locus':'Molecular Fitness Case Bench','short':'Molecular','floor':'Case laboratory','symbol':'DNA'},
 {'scene_index':7,'locus':'Selection Distribution Gallery','short':'Distributions','floor':'Graph gallery','symbol':'CURVES'},
 {'scene_index':8,'locus':'Sexual Selection Arena','short':'Mating','floor':'Arena','symbol':'MATE'},
 {'scene_index':9,'locus':'Artificial Selection Breeding Yard','short':'Breeding','floor':'Breeding yard','symbol':'HUMAN'},
]

ZONES={
'U7-L01':[
 ('left','Darwin voyage evidence wall','MAP','A wall-length voyage chart holds fossil sketches, island/mainland specimen comparisons, and Galápagos locations as historical evidence rather than as the mechanism of natural selection.'),
 ('center','Descent-with-modification registry','TREE','A brass-framed registry places ancestral and descendant population cards on a branching timeline so inherited continuity and accumulated difference can be seen together.'),
 ('right','Biogeography and Galápagos map','ISLANDS','A raised relief map connects nearby mainland and island populations with colonization arrows while keeping geographic distribution visible.')],
'U7-L02':[
 ('left','Individual-lifetime boundary','ONE','A glass lane holds one tagged adult medium ground finch whose body and beak remain the same individual while the population timeline advances.'),
 ('center','Population-across-generations platform','G1→G4','A circular platform projects four generations of the same simulated finch population as separate census rings.'),
 ('right','Natural-selection mechanism gate','SELECT','A locked gate opens toward the next room only when change is described at the population level across generations.')],
'U7-L03':[
 ('left','Phenotypic-variation aviary','BEAKS','A line of medium ground finches already differs in beak depth before any environmental pressure is applied.'),
 ('center','Heritable variation field','PEDIGREE','Parent-offspring lines connect similar beak-depth categories across generations while nonheritable body-condition tags remain detachable.'),
 ('right','Molecular-variation bridge','DNA→TRAIT','A narrow bridge links inherited genetic variation to phenotype without claiming that every visible difference is genetic.')],
'U7-L04':[
 ('left','Overproduction and limited-resource pen','MANY/FEW','Many young finches enter while a finite tray contains fewer usable seed patches and nesting spaces than individuals.'),
 ('center','Competition gate','LIMIT','A narrow feeding and nesting gate forces individuals to compete for limited resources while their phenotype identities stay visible.'),
 ('right','Offspring contribution scoreboard','OFFSPRING','A large scoreboard records how many viable reproductive offspring each phenotype category contributes to the next generation.')],
'U7-L05':[
 ('left','Relative reproductive-success tray','COUNT','Two phenotype categories place their viable reproductive-offspring totals side by side instead of using body size or survival alone.'),
 ('center','Evolutionary fitness scale','FIT','A balance-like digital scale converts relative offspring contribution into a comparison of fitness within the same population and environment.'),
 ('right','Environment-dependent outcome tray','DRY/WET','Two environmental panels switch between hard-seed drought conditions and a wetter soft-seed condition while the same phenotype categories remain identifiable.')],
'U7-L06':[
 ('left','Environmental-pressure controls','RAIN/HEAT/FOOD','Dials change one abiotic or biotic condition at a time while the initial population composition stays displayed above them.'),
 ('center','Selection-pressure chamber','PRESSURE','A clear chamber contains both an individual-response lane and a multi-generation population lane so short-term body change cannot be mistaken for evolution.'),
 ('right','Acclimation-versus-evolution board','LIFETIME/GENERATIONS','A two-column board compares reversible or environmentally induced within-lifetime change with heritable frequency change across generations.')],
'U7-L07':[
 ('left','Molecular-variant pathway','DNA→PROTEIN→CELL','A compact pathway reactivates the familiar relation from genetic variant to altered molecular/cellular phenotype without creating a new mnemonic identity for it.'),
 ('center','Sickle-cell heterozygote case','AA/AS/SS','Three genotype-state displays sit beneath a malaria-endemic environment indicator, with heterozygous and homozygous states kept visibly distinct.'),
 ('right','Reproductive-fitness outcome ledger','OFFSPRING','The population ledger records relative reproductive outcomes under the specified environment and never labels sickle-cell disease itself as protective.')],
'U7-L08':[
 ('left','Directional-selection panel','SHIFT','A bell-shaped beak-depth distribution is paired with a fitness profile favoring one extreme and a next-generation curve shifted toward that extreme.'),
 ('center','Stabilizing-selection panel','NARROW','An identical starting distribution is paired with highest fitness near the intermediate phenotype and a narrower next-generation curve.'),
 ('right','Disruptive-selection panel','TWO PEAKS','An identical starting distribution is paired with high fitness at both extremes and a next-generation distribution that separates toward two peaks.')],
'U7-L09':[
 ('left','Mate-choice lane','CHOICE','A stalk-eyed-fly display records mating opportunities associated with a heritable eye-span trait.'),
 ('center','Sexual-selection arena','MATES','The same trait is tracked through mate acquisition and reproductive output, making offspring number the final common measure.'),
 ('right','Competition and survival-cost lane','COST','A second readout records competition and survival costs separately so a trait can be costly yet still increase net reproductive success.')],
'U7-L10':[
 ('left','Human breeding-choice pens','BREEDER','Domestic pigeon pairs are chosen by a human breeder according to a heritable feather trait, and only selected pairs contribute to the next breeding generation.'),
 ('center','Artificial-selection yard','GENERATIONS','Successive pigeon generations pass through the same population ledger so human-directed reproductive choice can be watched changing trait frequencies.'),
 ('right','Natural-versus-artificial comparison board','WHO SELECTS?','A final board compares human-directed breeding opportunity with environment-dependent differential reproductive success in natural selection.')],
}

NARR={
'U7-L01':{
 'title':'The Observatory Has Lost the Difference Between Evidence and Mechanism',
 'kicker':'Historical observations can support descent and diversification without, by themselves, explaining the modern population mechanism of natural selection.',
 'paragraphs':[
  "The glass doors of the **Selection and Fitness Observatory** open into a high entrance gallery shaped like a shallow triangle, so the route is impossible to miss. On your **left**, a wall-length voyage chart carries specimen sketches, fossil notes, island names, and a dark line tracing an ocean route. Directly **ahead**, a brass registry stands beneath a branching timeline labeled ANCESTOR and DESCENDANTS. On your **right**, a raised relief map shows a mainland coast facing a chain of islands. Dr. Imani Vale waits beside the center registry in a charcoal field jacket. A transparent population ledger floats at her elbow, its three columns still blank: PHENOTYPE, OFFSPRING TO NEXT GENERATION, and ALLELE FREQUENCY. Above the gallery doors, a red warning flashes: OBSERVATORY CALIBRATION FAILED — EVERY CHANGE IS BEING CALLED EVOLUTION.",
  "Imani points first to the left wall, not to the warning. The route, specimens, and notes belong to **Charles Darwin**, the English naturalist whose observations and synthesis of evidence helped establish descent with modification by natural selection. She does not let the wall become a magic origin story. Darwin's voyage and Galápagos observations were important evidence among many lines of evidence; they are not a complete mechanism that makes populations change. The distinction matters enough that Imani leaves the brass pointer resting against the word EVIDENCE. 'We will not let a place name do the work of a mechanism,' she says, and slides a mainland bird card and several related island bird cards toward the map on your right.",
  "The map makes the geographic pattern visible. The island forms resemble the nearby mainland form more than they resemble organisms from distant continents, yet the island populations are not identical to one another. Imani names the kind of evidence only after you can see the distribution: **biogeography**, the study of the geographic distributions of organisms. Geographic patterns can support explanations involving descent, dispersal, and diversification. On the relief map, a single colonization arrow crosses from mainland to island, then branches across separate islands. Nothing on the map says an organism changed because it needed a new trait. The map shows where related populations occur and how a colonization-and-divergence hypothesis can fit that pattern.",
  "Now Imani turns to the center registry. She places an ancestral population card at the base of the brass timeline, then copies it into descendant population cards farther up the branches. A thin gold thread remains continuous from ancestor to descendant, but each later card accumulates small inherited differences. When that pattern is physically clear, she gives it its historical name: **descent with modification**. Descendant populations inherit traits from ancestors while accumulating heritable differences over generations. The Galápagos example on the right can therefore be read as colonization followed by divergence from ancestral populations. The registry preserves continuity and change together; it does not say that descendants are trying to become better, more advanced, or more suited to a future they can foresee.",
  "The red warning above the doors dims, but it does not disappear. A second message replaces it: HISTORICAL PATTERN VERIFIED — POPULATION MECHANISM STILL UNRESOLVED. Imani opens the transparent ledger and enters the first permanent rule along its top edge: TRACK POPULATIONS ACROSS GENERATIONS. The phrase is not yet a definition of natural selection. It is a boundary that will keep later scenes from sliding back into the idea that a single animal transforms itself. She leaves the voyage wall on the left, the descent registry in the center, and the biogeography map on the right exactly where they are, then carries the same blank ledger through a narrow door behind the registry.",
  "Beyond that door, a circular platform is already turning. One living finch stands motionless behind glass on the left while four population rings glow in the floor ahead. The observatory's damaged system has drawn an arrow directly from the single bird to a different-looking bird in the next ring, as if one lifetime were enough to become a new population. Imani stops the platform with her brass pointer before the animation can continue. The historical evidence has brought you to the right question, but it cannot answer it alone. To repair the observatory, the next room must establish where evolutionary change is actually measured."
 ]},
'U7-L02':{
 'title':'One Bird Cannot Become a Population',
 'kicker':'Natural selection is a population-level mechanism operating across generations, not a transformation that happens to one individual during its lifetime.',
 'paragraphs':[
  "You step onto the **Population Change Platform**, a round room divided by three bright floor arcs. On your **left**, the same tagged adult medium ground finch stands inside a narrow glass lane labeled ONE LIFETIME. Directly **ahead**, the center floor forms four concentric census rings marked GENERATION 1 through GENERATION 4. On your **right**, a heavy gate is stamped NATURAL SELECTION AS MECHANISM, but its lock is red. Imani sets the transparent population ledger on a stand at the edge of the center platform. The finch remains visible in the left lane while the ledger projects a population of many finches into the first ring. That physical separation is the whole point of the room: one individual on the left, a population through time in the center.",
  "The faulty observatory immediately tries its old trick. It enlarges the beak of the single finch in the left lane and flashes EVOLVED. Imani kills the animation. The individual is still the same individual. It may grow, lose mass, change behavior, or experience physiological effects during its life, but **evolutionary change is measured across generations in populations; an individual organism does not genetically evolve during its lifetime**. She freezes the left lane so the bird cannot be visually morphed again. Then she advances the center rings one generation at a time. Individuals disappear, reproduce, and are replaced by descendants, while only the population columns are allowed to change.",
  "At first, Imani does not tell you why any frequency changes. She simply makes the correct scale of observation unavoidable. Generation 1 contains several beak-depth categories. Generation 2 is a new set of individuals. Generation 3 is another. When the center display changes a phenotype percentage, the ledger changes only in the population row and only between generations. The left finch does not grow into the next generation. The correction seems simple, yet it prevents one of the most damaging misconceptions in evolutionary reasoning: saying that an organism evolved because the environment changed around it.",
  "Only after the generational boundary is secure does Imani unlock the gate on your right. The title now marks the relationship, **Natural selection as mechanism**. Natural selection is a major mechanism that changes populations over generations. Imani emphasizes the word *mechanism*. Nothing in this room has yet established which heritable differences matter, how the environment affects them, or why some descendants become more common. Those pieces are still missing. What the room has established is where the mechanism must leave its evidence: not as a purposeful change inside one body, but as a change in the composition of descendant populations across generations.",
  "The ledger now gains a permanent generation bar. Every later phenotype count and offspring total will sit under a specific generation number. Imani moves the left finch's tag onto the first-generation row only, preventing it from reappearing as if it lived through every future generation. The red calibration warning shrinks again. A new message runs across the gate: POPULATION SCALE VERIFIED — SOURCE OF DIFFERENTIAL REPRODUCTION UNKNOWN. The right gate opens into a wide sunlit chamber where a flock of finches is already waiting before any drought, predator, mate choice, or breeder has acted.",
  "Imani leaves the single-individual lane behind and carries the same ledger forward. 'Now we can ask what selection can actually act on,' she says. The next room is filled with visible differences that existed before any challenge began. If those differences are not heritable, the observatory cannot use them to explain evolutionary change."
 ]},
'U7-L03':{
 'title':'Variation Must Be There Before Selection Can Sort It',
 'kicker':'Natural selection acts on phenotypic variation, while adaptation requires a heritable trait whose effect on reproductive success depends on the environment.',
 'paragraphs':[
  "The next door opens into the **Heritable Variation Field**, an indoor aviary under a bright glass roof. On your **left**, twelve medium ground finches perch along a measuring rail. Their beaks are visibly different in depth and width before any food tray has been opened. Directly **ahead**, the center floor is marked with parent-offspring lines that connect several beak-depth categories across generations. On your **right**, a narrow bridge carries a simple DNA-to-phenotype diagram beside removable tags for body mass and recent feeding condition. Imani places the population ledger at the center rail and copies the starting phenotype counts into it. No environmental pressure has been applied. The variation is already present.",
  "Imani walks down the left rail and points to the range of beak forms. **Natural selection acts on phenotypic variation among individuals in a population.** The sentence is visible before anything is favored. Some differences may be inherited; some may come from age, nutrition, injury, or other environmental effects. The observatory's broken system tries to color every visible difference gold, but Imani removes the color from a bird whose lower body mass reflects recent food shortage. A visible difference is not automatically a heritable evolutionary variant. That is why the center pedigree lines matter: they allow the room to ask whether a phenotype has an inherited component that can persist across generations.",
  "The right bridge briefly activates a prior relationship without creating a new memory palace for it. Genetic and molecular variation can contribute to phenotype, but the bridge does not claim that every phenotype has one simple genetic cause. Imani lets the beak-depth categories remain the main visual anchor. Parents and offspring show statistical resemblance in the simulated lineage, enough for the observatory to treat beak depth as a heritable trait in this model population. The detached body-condition tag remains off to the side, deliberately excluded from that inference.",
  "Only then does a hard-seed tray rise in the center field. Some beak forms can process the available seeds more effectively than others, and the ledger later records different reproductive contributions among the heritable phenotype categories. Imani waits until the relationship is visible before naming the term **adaptation**. An adaptation is a heritable trait that increases reproductive success in a particular environment relative to alternative traits. The hard-seed condition is part of that definition. A beak form is not simply 'good' in the abstract, and the environment did not create the needed beak because the birds wanted it. The population already contained heritable variation before the condition began filtering reproductive success.",
  "Imani resets the seed tray and asks you to redraw the field from memory: visible phenotype variation on the left, heritable parent-offspring continuity in the center, and molecular/genetic support on the right. The ledger now has a second permanent rule: VARIATION FIRST; DIFFERENTIAL REPRODUCTION AFTER. That sequence will keep mutation and selection from being confused later. A trait can become more common through selection only if relevant heritable variation exists and different variants contribute differently to future generations.",
  "A loud metal shutter opens at the far end of the aviary. Beyond it, far more young finches are crowding toward a limited set of feeding stations and nesting spaces. The birds are not yet ranked as 'fit' or 'unfit.' The next room must show the missing causal bridge between limited resources and unequal contribution to the next generation."
 ]},
'U7-L04':{
 'title':'The Gate Counts Offspring, Not Winners',
 'kicker':'Limited resources can create competition, but selection changes populations through unequal reproductive contribution to later generations.',
 'paragraphs':[
  "The **Competition and Offspring Gate** is narrower and noisier than the aviary. On your **left**, a broad holding pen contains more young finches than the room can support at once. Above them, a counter climbs while the number of seed patches and nesting spaces remains fixed. Directly **ahead**, the center feeding gate admits only a limited number of individuals at a time. On your **right**, a wall-sized scoreboard has separate rows for each beak-depth category and a final column labeled VIABLE REPRODUCTIVE OFFSPRING CONTRIBUTED TO NEXT GENERATION. Imani locks the population ledger beneath that final column. The same starting phenotype counts from the variation field remain visible.",
  "The left pen makes **overproduction and competition** concrete. More offspring enter the system than the limited food, space, or other resources can support equally. That shortage creates competition, but Imani refuses to let the observatory stop at a dramatic picture of struggle. A finch can survive a difficult week and still leave no offspring. Another may not be the largest or strongest bird in the room yet may contribute more descendants. The central gate therefore records access to resources only as an intermediate event. The causal measure that matters for evolutionary change waits on the right scoreboard.",
  "As the simulation advances, the finches retain their phenotype tags. Under the current seed conditions, some beak categories obtain enough resources to survive and reproduce more successfully than others. The scoreboard does not simply mark SURVIVED or DIED. It counts viable reproductive offspring that enter the next generation. Imani names the relationship in full: **competition and differential reproductive success**. When resources are limited, individuals with favorable heritable phenotypes can leave more offspring, and that unequal contribution can change trait frequencies across generations.",
  "A misleading label drops from the ceiling: STRONGEST WINS. Imani catches it before it reaches the scoreboard. Strength is not the common currency here. Neither is survival by itself. She points to two birds that both survived; one contributed four offspring to the next generation, the other none. The ledger records those contributions, then advances the population one generation. The category with greater reproductive contribution now occupies a larger fraction of the descendant population. The change appears in the population ledger, not as a transformation of any individual bird.",
  "The center gate closes and the right scoreboard freezes its final counts. Imani has you trace the causal chain backward: limited resources on the left, competition at the center gate, unequal viable reproductive offspring on the right, and changed population composition in the next-generation ledger. No step requires intention. No bird chooses to evolve. The environment creates conditions in which existing heritable differences can have different reproductive consequences.",
  "A brass rail carries the filled offspring-count cards into the next hall. There, two phenotype categories will be placed on an enormous scale. The observatory still has one dangerous error left in this sequence: it currently labels the heavier, faster-looking bird as 'more fit.' Imani follows the cards through the doorway. 'Now we find out what fitness actually measures.'"
 ]},
'U7-L05':{
 'title':'The Scale That Refuses to Weigh Strength',
 'kicker':'Evolutionary fitness is relative reproductive success, and the same phenotype can have different fitness consequences in different environments.',
 'paragraphs':[
  "The **Fitness Scale** is a long rectangular hall with a digital balance built into its floor. On your **left**, two shallow trays hold the offspring-count cards from the previous room for two beak-depth categories. Directly **ahead**, the center balance is labeled REPRODUCTIVE CONTRIBUTION, with no scale for body mass, speed, aggression, or size. On your **right**, a split environmental chamber shows two different conditions for the same simulated finch population: one side contains mostly large, hard seeds after a dry period; the other contains a wetter condition with a broader supply of smaller, softer seeds. Imani places the transparent ledger above all three zones so phenotype identity, offspring number, and generation remain visible together.",
  "The broken observatory tries to lower a brass weight marked STRONGEST onto the center scale. Imani removes it. Then she takes the actual offspring cards from the left tray. Under the first defined environment, one phenotype category has contributed more viable reproductive offspring than the other. Only after the scale displays that difference does she name **evolutionary fitness**. Evolutionary fitness is evaluated through reproductive success relative to others in the population. A bird is not fit merely because it is large, healthy-looking, long-lived, or physically powerful. Those features matter evolutionarily only when they affect reproductive contribution under the conditions being measured.",
  "Imani then places both phenotype categories on the same comparison bar and names **relative fitness**. Relative fitness compares an individual's genetic contribution to the next generation with that of other individuals in the population. The word *relative* remains illuminated because there is no universal fitness score that follows a phenotype everywhere. The center scale compares reproductive contribution within a population under specified conditions. The ledger records that comparison as a ratio of contribution, not as a moral ranking of better and worse organisms.",
  "Now Imani changes only the environment on the right. The dry hard-seed tray retracts and a wetter, softer-seed condition appears. The phenotype labels remain the same. The observatory recalculates reproductive outcomes, and the ranking is allowed to change. Imani points to the right-side title **environment-dependent fitness effects**. A phenotype can increase or decrease fitness depending on the environment in which it occurs. The trait did not change its essence; the selective context changed which consequences mattered for reproductive success. That is why an allele or phenotype advantageous in one environment can be neutral or harmful in another.",
  "The ledger now carries three connected entries: phenotype, environment, and offspring contribution. Imani draws a triangle around them. Remove any corner, and the word *fitness* becomes dangerously vague. She returns the STRONGEST weight to a locked drawer and leaves the scale displaying reproductive success only. The observatory's calibration warning finally stops equating fitness with strength.",
  "Before the next door opens, the room offers an optional recall. The scale is covered, but the left offspring tray and right environmental panels remain visible as hints. If you can reconstruct why the center scale measures reproductive contribution relative to others, you can retrieve the term without seeing it. When the cover lifts, a pressure chamber beyond the hall begins altering temperature and food conditions around a single animal. The next danger is subtler: a body can change within one lifetime without the population evolving."
 ]},
'U7-L06':{
 'title':'A Changed Body Is Not Automatically an Evolved Population',
 'kicker':'Environmental change can create selective pressure, yet within-lifetime responses must be distinguished from heritable frequency change across generations.',
 'paragraphs':[
  "The **Changing Pressure Chamber** is divided into three glass bays. On your **left**, environmental controls adjust temperature, rainfall, food type, and a predator signal one at a time. Directly **ahead**, the center chamber has two horizontal lanes: the upper lane follows one tagged organism through its lifetime, while the lower lane follows a population through several generations. On your **right**, a large comparison board is split into LIFETIME RESPONSE and HERITABLE GENERATIONAL CHANGE. Imani mounts the transparent ledger above the lower lane only. That placement is intentional. The ledger is for population history; the single-individual lane has its own temporary physiological record.",
  "Imani first turns one environmental dial without changing heredity. Food becomes scarce for a period, and one tagged finch loses body mass. When normal food returns, its body condition improves. The organism changed visibly, but its short-term body-condition response does not by itself show that the population evolved. The observatory tries to stamp EVOLUTION onto the upper lane. Imani blocks the stamp and moves the card to the right-side LIFETIME RESPONSE column. An environmentally induced change in body condition is not evidence of evolution unless heritable genetic composition changes across generations.",
  "Next she resets the population and changes a condition that affects reproductive outcomes among existing heritable phenotypes. The left control panel makes that condition visible as a **selective pressure**: an environmental factor that changes which variants leave more offspring. The population composition is still the same at the start. No new useful trait appears because the environment demanded it. Across several generations, however, the ledger can record changing frequencies if heritable variants differ in reproductive success under the new condition. **Changing environments change selection** because biotic and abiotic conditions can alter which genetic variants are favored and can change the rate or direction of evolution.",
  "The right comparison board now shows the diagnostic difference. In the upper column, one individual's state changes within a lifetime and can reverse when conditions reverse. In the lower column, inherited variants differ in reproductive contribution and the population's heritable composition changes across generations. Imani calls the contrast **acclimation versus evolutionary change** only after both timelines are visible. The distinction is based on inheritance and generational frequency change, not on whether the organism looks different.",
  "The pressure controls click back to neutral. Imani leaves one rule glowing above the chamber: ENVIRONMENT CHANGES CONSEQUENCES; IT DOES NOT CREATE A NEEDED MUTATION. The sentence protects the route ahead. Selection can be nonrandom even though the origin of mutation is random with respect to fitness. Existing heritable variation, new mutation, recombination, and other sources can supply variation; selection changes reproductive success among phenotypes under particular conditions.",
  "A small drawer opens under the right comparison board. Inside is a human genetic case card marked MALARIA-ENDEMIC ENVIRONMENT. The ledger changes its phenotype categories to three genotype states but keeps the same three columns: identifiable variants, offspring contribution, and population frequency. Imani carries the case card into the next laboratory. The observatory can now separate lifetime response from inherited variation; next it must connect molecular variation to fitness without confusing disease with advantage."
 ]},
'U7-L07':{
 'title':'The Molecular Variant Does Not Have One Fitness Value Everywhere',
 'kicker':'A molecular variant can alter phenotype, but its fitness consequence depends on genotype and environment.',
 'paragraphs':[
  "The **Molecular Fitness Case Bench** is a compact laboratory with three clearly separated stations. On your **left**, a short pathway runs from a DNA-variant card to an altered hemoglobin state and then to a red-blood-cell phenotype. Directly **ahead**, the center bench holds three genotype-state trays, with the heterozygous state physically between the two homozygous states. Above them, a malaria-endemic environment indicator can be switched on or off. On your **right**, the transparent population ledger has changed categories for this case, but its structure is unchanged: genotype/phenotype state, reproductive contribution, and frequency. Imani keeps the finch records clipped to the back of the ledger so the new example does not erase the population logic learned earlier.",
  "The left pathway is a brief reactivation, not a new mnemonic identity. A genetic variant can change a molecular product, and molecular change can contribute to a physiological phenotype. Imani lets that causal chain remain visible, then moves immediately to the center bench. The important Unit 7 extension is the bridge from molecular difference to reproductive outcome under a specified environment. She labels that relationship **molecular variation and organismal fitness**. Variation in the number or types of cellular molecules can contribute to differences in survival and reproductive success across environments.",
  "The malaria indicator turns on. Imani refuses to label one tray simply 'sickle-cell anemia protects.' Instead, she keeps the three genotype states separate. In malaria-endemic environments, individuals heterozygous for the sickle-cell allele can have higher reproductive fitness than either homozygote. Heterozygosity can reduce severe malaria risk without producing the full sickle-cell disease phenotype. The advantage belongs to the heterozygous state under particular environmental conditions; it is not a statement that sickle-cell disease itself is beneficial.",
  "The right ledger makes the logic measurable. Reproductive outcomes are compared among genotype states in the malaria-endemic environment. If the environment indicator changes, the fitness relationships can change as well. Imani circles the same triangle from the Fitness Scale: inherited variation, environment, reproductive contribution. The molecular path on the left explains how a variant can influence phenotype. The center genotype comparison prevents a vague 'sickle allele is good' conclusion. The right population ledger returns the case to the level where evolution is measured.",
  "For a moment, the observatory's damaged system tries to award a universal gold badge to the heterozygous tray. Imani removes it. 'No allele carries a permanent fitness value in isolation,' she says. The environment and genetic context matter. The case is memorable precisely because one allele can be harmful in one genotype while contributing to higher relative fitness in another genotype under malaria pressure.",
  "When the malaria indicator dims, three enormous graph panels unfold from the laboratory wall. Each begins with exactly the same bell-shaped trait distribution. The case bench has shown why fitness can differ among variants; the next gallery will show what different patterns of relative fitness do to the shape of a population distribution across generations."
 ]},
'U7-L08':{
 'title':'Three Identical Populations, Three Different Selection Shapes',
 'kicker':'Directional, stabilizing, and disruptive selection are distinguished by which phenotypes have higher relative fitness and how the next-generation distribution changes.',
 'paragraphs':[
  "The **Selection Distribution Gallery** opens like a triptych. On your **left**, the first wall holds a bell-shaped beak-depth distribution with its mean marked by a vertical brass line. Directly **ahead**, the center wall holds an identical copy of that starting distribution. On your **right**, a third identical copy glows under the same scale. The starting mean, range, and sample size match across all three panels. Imani locks the transparent population ledger beneath the gallery so none of the three simulations can quietly begin with a different population. Only the pattern of relative fitness is allowed to change.",
  "On the left, the gallery raises the reproductive-success bar steadily toward one end of the trait range. Individuals closer to that extreme contribute more offspring, and the next-generation curve shifts in the same direction. Only after the shift is visible does Imani name **directional selection**. Directional selection favors phenotypes toward one end of a trait distribution, shifting the population mean when the trait is heritable. She leaves the old mean line in place so the movement is unmistakable: the entire distribution has moved relative to its starting position.",
  "At the center panel, the highest reproductive contribution belongs to intermediate phenotypes, while both extremes contribute fewer offspring. The next-generation curve narrows around the middle. Imani names **stabilizing selection** after the narrowing occurs. Stabilizing selection favors intermediate phenotypes and selects against extremes, tending to reduce phenotypic variation around the mean. The mean need not march toward one side; the signature is the relative loss of extremes and concentration near the intermediate phenotype.",
  "On the right, the highest reproductive contribution belongs to both extremes and the intermediate forms contribute less. The single starting bell begins to hollow in the center and develop two high regions. Imani names **disruptive selection**. Disruptive selection favors phenotypes at both extremes over intermediate phenotypes and can increase variation within a population. The gallery does not announce speciation; a two-peaked distribution is not automatically a new species boundary. It shows a distinct selection pattern within a population.",
  "Imani now has you compare the three walls without their labels. Left: one extreme favored and the mean shifts. Center: intermediate favored and the distribution narrows. Right: both extremes favored and the middle declines. The physical placement prevents the names from collapsing into one generic idea of 'selection.' All three begin with heritable variation and differential reproductive success; what differs is the shape of relative fitness across the trait range and therefore the distributional consequence in later generations.",
  "An optional recall curtain descends over the left title while leaving its shifted curve visible. If the curve alone lets you reconstruct which selection pattern favors one end of a heritable trait distribution, the name has become attached to the mechanism without relying on a word list. When the curtain rises, the center wall opens into an arena where the common currency is still offspring contribution, but the immediate route to reproduction is access to mates."
 ]},
'U7-L09':{
 'title':'A Costly Trait Can Still Win Through Reproduction',
 'kicker':'Sexual selection operates through differences in obtaining mates, and its reproductive benefit can outweigh survival costs.',
 'paragraphs':[
  "The **Sexual Selection Arena** is circular, but its three stations remain fixed. On your **left**, a mate-choice lane contains a simulated population of stalk-eyed flies whose eye-span trait varies among individuals. Directly **ahead**, the center arena records how many mating opportunities and offspring each trait category obtains. On your **right**, a separate panel records energetic and survival costs associated with carrying an exaggerated trait, alongside a competition lane where potential mates can be won through contests. Imani hangs the transparent population ledger above the center scoreboard. The ledger has the same final currency it has used since the Competition Gate: contribution of offspring to the next generation.",
  "The observatory first highlights mate choice. Individuals carrying one heritable trait value obtain more mating opportunities than others. Then the competition lane activates and shows a second route by which some individuals gain greater access to mates. Imani refuses to reduce the mechanism to 'females choose pretty males.' Mate choice and competition among potential mates can both generate differences in reproductive success, and the exact pattern varies across species and mating systems.",
  "Only after those differences appear on the offspring counter does Imani name **sexual selection**. Sexual selection is differential reproductive success caused by variation in obtaining mates, including mate choice and competition among potential mates. The definition ends at reproductive success, not ornament size. A conspicuous trait matters evolutionarily when its effects on mating and reproduction change contribution to later generations.",
  "The right panel now makes the trade-off visible. The exaggerated trait carries a survival or energetic cost. The observatory's faulty label tries to stamp USELESS onto it because it makes survival harder. Imani removes the label and compares the two readouts. A trait favored through mating success can persist even if it carries a survival cost, provided its net effect increases reproductive success. Survival cost and mating benefit are separate components; the population-level result depends on their combined effect on offspring contribution.",
  "Imani turns the arena lights down and points back toward the Fitness Scale through the glass corridor. The same rule holds: reproductive contribution is the common currency. Sexual selection is not an exception to evolution by selection; it is a particular route by which heritable variation produces differential reproductive success through access to mates. The arena also stays distinct from the earlier natural-selection gate because the diagnostic comparison here is mate acquisition, and it stays distinct from the next yard because no human has chosen who breeds.",
  "At the far side of the arena, a wooden gate swings open. Rows of domestic pigeons wait in paired pens, and a human breeder's clipboard is already marking which birds will be allowed to reproduce. The population ledger rolls forward. The next room will keep the generational outcome but change who determines reproductive opportunity."
 ]},
'U7-L10':{
 'title':'The Breeder Changes the Population Without Changing a Bird',
 'kicker':'Artificial selection changes populations when humans choose which individuals reproduce, providing a direct comparison with natural selection.',
 'paragraphs':[
  "The final room, the **Artificial Selection Breeding Yard**, sits under the observatory's main glass dome. On your **left**, domestic pigeons occupy human breeding-choice pens, each bird carrying a visible heritable feather-trait tag. Directly **ahead**, the center yard contains a breeding line marked GENERATION 1, GENERATION 2, GENERATION 3, and GENERATION 4. On your **right**, a tall comparison board is divided into HUMAN CHOOSES BREEDERS and ENVIRONMENT AFFECTS REPRODUCTIVE SUCCESS. Imani locks the transparent population ledger into the center rail. Through the dome behind you, the entire ten-room route can now be seen as one clockwise circuit.",
  "A breeder enters the left pens and deliberately chooses which pigeons will reproduce according to the heritable feather trait. The unchosen birds do not become different pigeons; they simply contribute fewer or no offspring to the breeding population. Generation 1 produces Generation 2, and the selected trait becomes more common because the reproductive contribution has been intentionally filtered by a human choice. After the pattern is visible, Imani names **selective breeding**: the human-directed choice of which individuals reproduce so desired heritable traits become more common in later generations.",
  "The center generation line runs again, and Imani gives the broader process its name: **artificial selection**. Human selective breeding can change variation and trait frequencies in other species. The population ledger records the same kind of generational frequency change you have tracked all journey long. Nothing about the mechanism requires an individual organism to evolve during its lifetime. The change appears because some heritable variants are repeatedly allowed to contribute more descendants than others.",
  "Now Imani turns on the right comparison board. On the HUMAN side, reproductive opportunity is determined by breeder choice. On the ENVIRONMENT side, natural selection results from environmental differences in reproductive success. Both can change population trait frequencies across generations, but the source of differential reproduction is different. The board labels the relationship **natural versus artificial selection** only after the comparison is physically complete. Sexual selection remains a third diagnostic route from the arena behind you, where access to mates altered reproductive success without a human breeder.",
  "The red calibration warning at the top of the dome flashes one last time. Instead of clearing it immediately, Imani asks you to reconstruct the whole circuit from the population ledger. Historical evidence and biogeography supported descent with modification. Population change belonged across generations. Heritable phenotypic variation existed before selection. Limited resources created competition, but offspring contribution—not strength—drove frequency change. Fitness was relative and environment dependent. Within-lifetime change was separated from evolution. Molecular variants gained meaning through genotype and environment. Selection distributions differed by which phenotypes had higher relative fitness. Mate acquisition could drive sexual selection. Human breeding choice could drive artificial selection.",
  "Only when the route is complete does Imani turn the key. The warning changes to CALIBRATION VERIFIED. The final optional recall covers the words ARTIFICIAL SELECTION while leaving the human breeding pens, generation line, and changing trait frequencies visible. If those relationships recover the term, the story has done its job. Imani closes the transparent ledger, but she does not erase it. Its same three columns—phenotype or genotype, offspring contributed to the next generation, and population frequency—will travel into the Population Genetics Island Network, where selection will be joined by mutation, drift, bottlenecks, founder effects, gene flow, and Hardy-Weinberg reasoning."
 ]},
}

BEAT_IMAGES={
'U7-K-079':'the center registry showing descendant populations inheriting continuity from an ancestor while accumulating heritable differences',
'U7-K-076':'the left voyage evidence wall attached to Charles Darwin as historical observer and synthesizer rather than as a magical mechanism',
'U7-K-077':'the right island-mainland distribution map used as geographic evidence',
'U7-K-078':'the colonization arrow from mainland to islands followed by branching descendant populations',
'U7-K-001':'the center generation platform changing population composition across generations while the left individual remains the same individual',
'U7-K-082':'the frozen individual-lifetime lane contrasted with changing descendant population rings',
'U7-K-005':'the left aviary showing phenotypic variation already present before pressure begins',
'U7-K-080':'the heritable beak-depth line that increases reproductive success under a specified seed environment',
'U7-K-002':'the finite-resource gate followed by unequal viable reproductive offspring on the right scoreboard',
'U7-K-081':'the overcrowded left pen and finite food/nesting stations that create competition',
'U7-K-003':'the center fitness scale using relative reproductive offspring contribution rather than strength',
'U7-K-083':'the two phenotype categories compared by relative contribution to the next generation',
'U7-K-007':'the right environmental panels changing which phenotype has the higher reproductive outcome',
'U7-K-004':'the environmental controls changing which genetic variants are favored without creating needed variants',
'U7-K-006':'the left environmental factor becoming a selective pressure only when it changes differential reproductive success',
'U7-K-084':'the right board separating reversible within-lifetime change from heritable population change across generations',
'U7-K-008':'the left DNA-to-molecular-to-phenotype pathway connected to reproductive outcomes under a specified environment',
'U7-K-214':'the center heterozygous sickle-cell case under malaria pressure, kept distinct from both homozygous states and from sickle-cell disease itself',
'U7-K-085':'the left curve shifting toward one favored extreme',
'U7-K-086':'the center curve narrowing around an intermediate phenotype',
'U7-K-087':'the right curve losing intermediates and increasing at both extremes',
'U7-K-088':'the center arena converting differences in mate acquisition into differences in offspring contribution',
'U7-K-089':'the separate survival-cost and mating-benefit readouts for the same heritable trait',
'U7-K-009':'the center pigeon generations changing trait frequency after humans choose which birds reproduce',
'U7-K-090':'the left human breeder selecting breeding pairs by a heritable trait',
'U7-K-091':'the right comparison board separating human-directed breeding from environment-dependent differential reproduction',
}

CHECKPOINTS={'U7-L05','U7-L08','U7-L10'}

def clean_prose(text):
    text=text.replace(' — ', '. ').replace('—','-')
    text=re.sub(r': (?=\*\*[a-z])', ', ', text)
    text=text.replace(': ', '. ')
    text=re.sub(r'(?<=\. )([a-z])', lambda m:m.group(1).upper(), text)
    return text

def word_count(paragraphs):
    return len(re.findall(r"\b[\w’′'-]+\b",' '.join(paragraphs)))

def zone_objs(lid):
    out=[]
    for position,label,symbol,description in ZONES[lid]:
        out.append({'position':position,'label':label,'symbol':symbol,'description':description})
    return out

def cast_for(lid):
    items=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    for position,label,symbol,description in ZONES[lid]:
        items.append({'name':label,'kind':'scientific population, evidence display, comparison, or process','visual':description,'job':f"Remain fixed on the learner's {position} and carry the {position}-side scientific role required by the locked F3 geometry."})
    items.append({'name':'Transparent population ledger','kind':'journey continuity object','visual':'a clear floating ledger divided into phenotype or genotype category, viable reproductive offspring contributed to the next generation, and a narrow population-frequency strip','job':'keeps population identity, generation, reproductive contribution, and frequency reconstructable across all ten scenes without replacing the organisms or evidence'})
    return items

def beats_for(lid):
    b=B[lid]
    terms={t['knowledge_id']:t for t in b['term_introductions']}
    out=[]
    for kid in b['knowledge_ids']:
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
    b=B[lid]; n=NARR[lid]; route=ROUTE[i]; paragraphs=[clean_prose(p) for p in n['paragraphs']]; cp=lid in CHECKPOINTS
    scenes.append({
      'scene_index':i,'locus_id':lid,'locus':route['locus'],'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['micro_anchor'],
      'scene_layout':{'orientation':b['orientation_sentence'],'zones':zone_objs(lid)},
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
 'palace_id':'U7-J1','unit_id':'unit-7','palace_name':'Selection and Fitness Observatory',
 'story_title':'The Observatory That Mistook Change for Evolution',
 'tagline':'A damaged observatory is calling every visible change evolution. Carry one population ledger through ten rooms until heredity, generations, environment, and reproductive success all agree.',
 'guide':GUIDE,
 'premise':'A calibration failure has caused the Selection and Fitness Observatory to label individual body changes, strength, geographic patterns, disease states, and human breeding as if they all meant the same thing. Dr. Imani Vale must reopen the route before the observatory can certify any evolutionary explanation. The only instrument she trusts is a transparent population ledger that keeps phenotype or genotype categories, reproductive offspring, and population frequencies visible across generations.',
 'mission':'Travel clockwise through ten permanent locations. Separate historical evidence from mechanism, population change from individual change, heritable variation from temporary condition, competition from reproductive success, fitness from strength, acclimation from evolution, molecular phenotype from environmental fitness consequence, three selection distributions from one another, sexual selection from survival alone, and artificial selection from natural selection.',
 'finale':'The observatory clears its calibration warning only after the learner can reconstruct the entire causal route. Natural, sexual, and artificial selection all change descendant populations through differential reproduction, while their immediate sources of reproductive difference remain distinct. Fitness is relative and environment dependent, and no individual organism needs, chooses, or performs its own genetic evolution.',
 'estimated_minutes':30,'scene_count':10,'checkpoint_count':len(CHECKPOINTS),
 'student_release':'DEVELOPER_PREVIEW_F4A','preview_release':True,'narrative_design':'U7-F4A-NARRATIVE-1.0',
 'learner_rule':'Read or listen and place yourself in each room before following the population-level action. The same transparent ledger persists through all ten locations. Exact terms appear only after their defining evidence, mechanism, or comparison is visible. Optional Quick Recall appears only three times.',
 'route_orientation':'The observatory is one clockwise ring beneath a glass dome. Enter at Darwin Evidence Intake, then continue through Population Change Platform, Heritable Variation Field, Competition and Offspring Gate, Fitness Scale, Changing Pressure Chamber, Molecular Fitness Case Bench, Selection Distribution Gallery, Sexual Selection Arena, and Artificial Selection Breeding Yard. Every room keeps left, center, and right anchors fixed before the biological state changes.',
 'route':ROUTE,'scenes':scenes,
 'source_brief_lock':'LOCKED_F3','scientific_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2',
}

(U7/'journeys').mkdir(exist_ok=True)
(U7/'journeys'/'U7-J1.json').write_text(json.dumps(journey,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary={
 'schema':'memory-palace-v2-unit7-f4a-journeys-1.0','unit_id':'unit-7','stage':'F4A','student_release':False,'preview_release':True,
 'journey_count':1,'scene_count':10,'checkpoint_count':len(CHECKPOINTS),
 'guided_journeys':[ {k:journey[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']} ]
}
(U7/'journeys-f4a.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

status={
 'unit_id':'unit-7','number':7,'title':'Natural Selection','status':'F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','pipeline_stage':'F4A_JOURNEY1_NARRATIVE',
 'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','narrative_lock':'LOCKED_F4A_J1',
 'student_release':False,'preview_release':True,'journey_count':1,'scene_count':10,'memory_objects':0,'application_challenges':0,
 'canonical_records':215,'architecture_journeys':6,'architecture_bundles':23,'architecture_loci':55,'scene_briefs':55,'palace_managed_records':174,
 'challenge_lab_records':16,'scope_guard_records':25,'exact_name_review_targets':94,'confusable_sets':33,'optional_first_exposure_recalls':18,
 'f4a_journey':'U7-J1','f4a_scene_count':10,'f4a_knowledge_records':26,'f4a_exact_name_targets':15,'f4a_optional_recalls':len(CHECKPOINTS),
 'next_required_output':'F4B polished narrative for Journey 2 only after Journey 1 remains frozen and the F4A prose, spatial, science, and regression gates continue to pass.'
}
(U7/'status-f4a.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(U7/'status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'
course=json.loads(cp.read_text(encoding='utf-8'))
u=next(x for x in course['units'] if x['unit_id']=='unit-7')
u.update({
 'status':'F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','journey_count':1,'scene_count':10,'student_release':False,'preview_release':True,
 'source_status':'AUDITED_F1_ARCHITECTURE_F2_BRIEFS_F3_NARRATIVE_F4A','narrative_lock':'LOCKED_F4A_J1','narrative_journeys':1,
 'pipeline_stage':'F4A_JOURNEY1_NARRATIVE'
})
cp.write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Reviewer-facing story document.
doc=['# Unit 7 F4A · Journey 1 Narrative','','## The Observatory That Mistook Change for Evolution','',journey['tagline'],'',
     '### Physical route','', ' → '.join(x['locus'] for x in ROUTE),'',
     '### Continuity rule','',CONTINUITY,'']
for s in scenes:
    doc += [f"## {s['scene_index']+1}. {s['locus']} · {s['title']}",'',f"*{s['scene_kicker']}*",'']
    doc += s['story_paragraphs']+['']
    if s['checkpoint']:
        doc += ['**Optional Quick Recall**','',s['checkpoint_prompt'],'']
(ROOT/'docs'/'UNIT7_F4A_JOURNEY1_STORY.md').write_text('\n'.join(doc),encoding='utf-8')

# Release manifest and narrative lock.
def sha(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()
locked_rel=['journeys/U7-J1.json','journeys-f4a.json','status-f4a.json']
lock_files={rel:{'bytes':(U7/rel).stat().st_size,'sha256':sha(U7/rel)} for rel in locked_rel}
lock={
 'schema':'memory-palace-v2-unit7-f4a-lock-1.0','unit_id':'unit-7','lock_status':'LOCKED_F4A_J1','student_release':False,'preview_release':True,
 'protected_prior_locks':['content-lock-f1.json','content-lock-f2.json','content-lock-f3.json'],
 'journey_id':'U7-J1','scene_count':10,'knowledge_record_count':26,'exact_name_target_count':15,'checkpoint_count':len(CHECKPOINTS),'files':lock_files,
 'rule':'Journey 1 polished prose may not change after F4A without a new explicit narrative version. F1 science, F2 classification/geometry, and F3 scene briefs remain authoritative boundaries.'
}
(U7/'content-lock-f4a.json').write_text(json.dumps(lock,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
release={
 'schema':'memory-palace-v2-unit7-f4a-release-1.0','generated_utc':'2026-09-08T04:30:00+00:00','unit_id':'unit-7',
 'release_status':'F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','student_release':False,'preview_release':True,'journey_id':'U7-J1',
 'journeys':1,'scenes':10,'knowledge_records':26,'exact_name_targets':15,'optional_first_exposure_recalls':len(CHECKPOINTS),
 'canonical_records':215,'permanent_loci_architecture':55,'scene_briefs':55,'memory_objects':0,'application_challenges':0,
 'scientific_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','narrative_lock':'LOCKED_F4A_J1',
 'next_stage':'F4B Journey 2 polished narrative after F4A regression'
}
(U7/'f4a-release-manifest.json').write_text(json.dumps(release,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

print(json.dumps({'journey':'U7-J1','scenes':10,'knowledge_records':26,'exact_name_targets':15,'checkpoints':len(CHECKPOINTS),'words':sum(s['narrative_word_count'] for s in scenes),'mean_words':round(sum(s['narrative_word_count'] for s in scenes)/10,1),'min_words':min(s['narrative_word_count'] for s in scenes),'max_words':max(s['narrative_word_count'] for s in scenes)},indent=2))
