from __future__ import annotations
import json, hashlib, re, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'
subprocess.run([sys.executable,str(ROOT/'scripts'/'build_unit5_f4e.py')],check=True,stdout=subprocess.DEVNULL)
F3=json.loads((U5/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS=json.loads((U5/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J6=next(j for j in JBRIEFS if j['journey_id']=='U5-J6')
B={b['locus_id']:b for b in F3 if b['journey_id']=='U5-J6'}
CANON={r['knowledge_id']:r for r in json.loads((U5/'source'/'canonical-unit5-f1.json').read_text(encoding='utf-8'))['canonical_catalog']}
J1=json.loads((U5/'journeys'/'U5-J1.json').read_text(encoding='utf-8'))
J2=json.loads((U5/'journeys'/'U5-J2.json').read_text(encoding='utf-8'))
J3=json.loads((U5/'journeys'/'U5-J3.json').read_text(encoding='utf-8'))
J4=json.loads((U5/'journeys'/'U5-J4.json').read_text(encoding='utf-8'))
J5=json.loads((U5/'journeys'/'U5-J5.json').read_text(encoding='utf-8'))

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

GUIDE={
 'name':'Dr. Imani Reyes','role':'inheritance-systems geneticist',
 'visual':'deep-green field coat, clear gloves, compact chromosome tablet preserving the blue and amber parental-origin chromosome identities, and the narrow gold generation ledger',
 'story_job':'Imani keeps the phenotype-comparison frame stable while changing one biological mechanism at a time. She names each inheritance pattern only after the genotype, chromosome, gene interaction, dosage state, or environmental input that produces it is visible.'
}
FRAME={
 'name':'Phenotype-comparison frame','kind':'continuity scientific display',
 'visual':'a tall brass frame with three fixed windows. The left window always holds genotype, chromosome state, or environmental context, the center window exposes the mechanism, and the right window shows the resulting phenotype or inheritance pattern',
 'job':'forces every gallery comparison to preserve the same input to mechanism to outcome geometry so different non-simple inheritance patterns can be discriminated by cause rather than by a shared label.'
}
MECHANISM_CARDS={
 'name':'Mechanism identity cards','kind':'continuity scientific object',
 'visual':'small ivory cards labeled only after a mechanism has been demonstrated. Each card clips beneath the center window of the phenotype-comparison frame and carries the exact biological relationship that produced the observed pattern',
 'job':'prevents a phenotype shape from receiving a mechanism label before the causal relationship is established.'
}
GENERATION_LEDGER={
 'name':'Gold generation ledger','kind':'continuity record',
 'visual':'the same narrow gold ledger carried through earlier Unit 5 journeys, now ruled for genotype or context, mechanism, phenotype pattern, chromosome model, and evidence limits',
 'job':'preserves chromosome and inheritance context while keeping mechanism-specific conclusions separate from broad claims about people, sex development, or environmental causation.'
}

route=[
 {'scene_index':0,'locus':'Beyond-Mendel Pattern Entrance','short':'Pattern entrance','floor':'South gallery entrance','symbol':'expected → observed'},
 {'scene_index':1,'locus':'Dominance Spectrum Studio','short':'Dominance spectrum','floor':'West phenotype studio','symbol':'allele interaction'},
 {'scene_index':2,'locus':'Gene-Interaction Theater','short':'Gene interactions','floor':'Central trait theater','symbol':'genes ↔ effects'},
 {'scene_index':3,'locus':'Chromosome-Linked Inheritance Comparator','short':'Chromosome linked','floor':'North chromosome wall','symbol':'autosome X Y'},
 {'scene_index':4,'locus':'Hemizygous Transmission Rail','short':'Hemizygous rail','floor':'Northeast transmission rail','symbol':'single X-linked copy'},
 {'scene_index':5,'locus':'X-Inactivation Mosaic Gallery','short':'X inactivation','floor':'East mosaic gallery','symbol':'active X mosaic'},
 {'scene_index':6,'locus':'Phenotypic Plasticity Conservatory','short':'Environment','floor':'Sunlit conservatory','symbol':'genotype + environment'}
]

BEAT_IMAGES={
 'U5-K-023':'the entrance frame where a simple Mendelian expected ratio and observed offspring counts are compared before any mechanism label is chosen',
 'U5-K-089':'the branching gallery map where several different mechanisms can produce non-simple inheritance patterns while allele segregation can still remain valid',
 'U5-K-025':'the codominance panel where two allelic effects remain separately visible in the heterozygous phenotype',
 'U5-K-026':'the incomplete-dominance panel where the heterozygote has an intermediate phenotype while the two alleles remain genetically discrete',
 'U5-K-090':'the population allele rack holding more than two allele variants while each diploid individual still carries no more than the copies present at its own locus',
 'U5-K-091':'the ABO display where IA and IB are codominant to each other and both are dominant over i within a three-allele population system',
 'U5-K-028':'the pleiotropy branch where one gene sends effects toward several traits or biological consequences',
 'U5-K-092':'the epistasis stage where genotype at one gene changes or masks the phenotypic expression associated with another gene',
 'U5-K-093':'the polygenic spectrum where variation at multiple genes contributes to one quantitative phenotypic character',
 'U5-K-027':'the chromosome wall where X-linked and Y-linked inheritance follows genes physically located on those chromosomes within an explicit chromosome-complement model',
 'U5-K-050':'the autosome panel separating chromosomes outside the designated sex-chromosome set in the stated model',
 'U5-K-051':'the explicit human X/Y chromosome-complement model where eggs are usually X-bearing and sperm are usually X- or Y-bearing without treating chromosome complement as gender or complete sex-development biology',
 'U5-K-094':'the X-linked gene marker physically attached to an X chromosome so inheritance follows the chromosome carrying the gene',
 'U5-K-095':'the Y-linked gene marker physically attached to a Y chromosome and transmitted through Y-bearing lineages in the XX/XY model',
 'U5-K-096':'the hemizygous rail where one copy of an X-linked locus is present in an otherwise diploid modeled XY genome',
 'U5-K-097':'the transmission rail that tracks actual X chromosomes, gametes, and alleles through offspring combinations in the stated XX/XY model',
 'U5-K-100':'the side case panel showing named X-linked disorders as examples of the inheritance mechanism without making the disease names the mechanism itself',
 'U5-K-098':'the XX somatic-cell lineage display where one X becomes largely transcriptionally inactive early in development and different cell lineages can retain different active-X origins',
 'U5-K-099':'the condensed Barr body representation of a largely inactive X chromosome in an interphase nucleus',
 'U5-K-034':'the conservatory where changing environmental conditions can alter gene expression or physiology so one genotype can produce different phenotypes',
 'U5-K-120':'the central genotype-by-environment frame where phenotype depends on both inherited genotype and environmental context',
 'U5-K-121':'the cool and warm pigmentation chambers showing temperature-dependent pigment pathway activity',
 'U5-K-122':'the soil-chemistry plant beds where pH and associated ion availability influence flower color in susceptible genotypes',
 'U5-K-123':'the UV-response panel where ultraviolet exposure increases regulated melanin production in human skin cells'
}

ZONE_COPY={
'U5-L31':[
 ('left','Simple Mendelian expectation wall','expected','A clean one-gene complete-dominance display holds the expected phenotypic ratio for a defined cross. It remains fixed as the reference model.'),
 ('center','Observed-count comparison table','compare','A long glass table receives observed offspring counts and compares them with the expected pattern without deciding that every numerical difference is biologically meaningful.'),
 ('right','Mechanism route doors','many causes','Several labeled doors lead to altered dominance relationships, multiple alleles, gene interactions, chromosome-linked inheritance, organelle inheritance, linkage, and environmental phenotype mechanisms.')],
'U5-L32':[
 ('left','Incomplete-dominance phenotype alcove','intermediate','Three matched phenotype columns show the two homozygotes and an intermediate heterozygote while the underlying alleles remain discrete.'),
 ('center','Codominance and allele-number bench','distinct effects','A split phenotype panel displays both allelic effects in the heterozygote beside a population rack that can hold more than two allele variants.'),
 ('right','ABO allele-system display','IA IB i','Three allele plaques feed genotype combinations into blood-group phenotype windows so codominance and multiple-allele logic can be seen in one real genetic system.')],
'U5-L33':[
 ('left','Epistasis masking stage','gene affects gene','Two gene-control panels feed one phenotype lamp. Changing one gene can alter or block the visible effect associated with another gene.'),
 ('center','Gene-count and effect-count turntable','count genes and effects','A rotating brass table asks how many genes contribute and how many traits or effects emerge before a mechanism card can be attached.'),
 ('right','Polygenic spectrum and pleiotropy branches','many to one or one to many','One branch combines inputs from several genes into one quantitative phenotype scale. The neighboring branch begins with one gene and splits toward several phenotypic effects.')],
'U5-L34':[
 ('left','Autosome panel','autosomes','A chromosome rack holds the chromosomes classified as autosomes under the stated human XX/XY model, physically separate from the X and Y comparison display.'),
 ('center','Human XX/XY chromosome-complement model','explicit model','A central model tracks X and Y chromosome transmission through gametes while a boundary placard states that chromosome complement describes this inheritance model and does not define gender or the full biology of sex development.'),
 ('right','X-linked and Y-linked gene panel','gene location','Gene markers are fixed directly onto an X or Y chromosome so inheritance follows chromosome location. A smaller species panel reminds the learner that other sex-determination systems exist.')],
'U5-L35':[
 ('left','X-linked allele source','single locus','A modeled X chromosome carries one marked allele at a defined locus before the chromosome enters the transmission rail.'),
 ('center','Hemizygous transmission rail','one copy','A typical modeled XY genome displays one copy of many X-linked loci and then sends actual X-bearing gametes and allele states through offspring combinations.'),
 ('right','Offspring and example case panel','trace outcomes','Offspring chromosome combinations are displayed beside a small panel of familiar X-linked disorder examples whose names remain examples of the mechanism, not definitions of it.')],
'U5-L36':[
 ('left','Early XX somatic-cell panel','two X chromosomes','A modeled early mammalian XX somatic cell shows two X chromosomes before stable lineage-specific inactivation patterns are established.'),
 ('center','X-inactivation and Barr-body chamber','largely inactive X','One X becomes largely transcriptionally inactive and condenses into a Barr-body representation while a small escape window remains open for genes that can escape inactivation.'),
 ('right','Descendant-cell mosaic wall','mosaic','Many descendant cell patches retain different active-X origins, producing a visible mosaic across cell lineages without changing the inherited chromosome complement.')],
'U5-L37':[
 ('left','Temperature pigmentation chamber','temperature','Matched genotype panels enter cool and warm environments so temperature-sensitive pigment pathways produce different visible patterns.'),
 ('center','Genotype-by-environment core','same genotype different context','The phenotype-comparison frame locks genotype while environmental conditions change gene expression or physiology, revealing phenotypic plasticity.'),
 ('right','Soil chemistry and UV response bays','pH and UV','Hydrangea soil-chemistry beds and a regulated human skin-cell UV response show two more environment-dependent phenotype mechanisms with their biological responses made explicit.')]
}

NARR={
'U5-L31':{
 'title':'The Entrance Where Every Unusual Ratio Had Been Given the Same Name',
 'kicker':'A non-simple offspring pattern is evidence that the simple reference model may be incomplete, yet the mechanism still has to be identified from biology and data.',
 'paragraphs':[
  "The doors of the **Beyond-Mendel Pattern Entrance** open into a long gallery whose floor is divided into three permanent zones. On your **left**, a white wall holds one clean simple Mendelian expectation for a defined one-gene complete-dominance cross. Directly **ahead**, a glass comparison table is covered with trays for observed offspring counts. On your **right**, a fan of narrow doors leads deeper into the gallery, each door marked by a different kind of biological mechanism. Dr. Imani Reyes sets the brass **phenotype-comparison frame** across the three zones so its left window shows the reference model, its center window shows the comparison process, and its right window points toward possible mechanisms. She clips the **gold generation ledger** beneath it and keeps the ivory **mechanism identity cards** face down. Nothing receives a mechanism name yet.",
  "The left wall displays an expected phenotypic pattern under a simple Mendelian model with complete dominance. Imani then pours a set of observed offspring counters onto the center table. The observed counts do not match the expected proportions perfectly. She does not treat that difference as an automatic discovery. Real samples vary, especially when sample size is limited. The center table therefore separates two questions. First, are the observed counts numerically different from the predicted counts. Second, is the departure large enough to be statistically meaningful under the model being tested. Imani writes **Quantitative identification of non-Mendelian ratios** on the ledger only after those two questions are visible. Quantitative analysis can test whether observed phenotypic counts differ statistically from predicted counts. The calculation itself remains for later application work, while this room preserves what the calculation is supposed to decide.",
  "A brass lever opens the right-side doors one at a time. Behind one is altered dominance between alleles. Another reveals more than two alleles in the population. A third contains interacting genes. Farther along are chromosome-linked inheritance, linkage between loci on the same chromosome, organelle inheritance, and environment-dependent phenotype displays. Several of these mechanisms can make an offspring pattern depart from the simple ratio on the left, yet they do so for different biological reasons. Imani turns over the first mechanism card and writes **Non-Mendelian inheritance patterns** beneath the route map. Many inheritance patterns depart from simple one-gene complete-dominance ratios because the inheritance mechanism contains additional structure. The gallery will identify that structure room by room.",
  "Imani returns to the blue and amber homologs on her chromosome tablet and watches one modeled allele pair enter meiosis. The alleles still separate when homologous chromosomes segregate. She taps the segregation line on the ledger and leaves it intact. A non-simple phenotypic ratio does not mean every Mendelian principle has disappeared. Mendel's segregation principle can still apply while dominance relationships, chromosome linkage, gene interaction, allele number, or other features change the expected phenotype distribution. The distinction is important because the phenotype pattern is an outcome. The mechanism that produced it may preserve some familiar chromosome behavior while changing another relationship.",
  "You look back across the three windows of the phenotype-comparison frame. The left window is the simple reference. The center window holds the observed counts and the question of statistical departure. The right window contains several biologically different routes. If every unexpected ratio were simply labeled non-Mendelian and left there, the label would conceal the mechanism the learner actually needs to understand. Imani therefore leaves the mechanism cards separated and clips only one rule to the frame. First identify what biological relationship changed. Then use the observed pattern as evidence for that mechanism.",
  "At the far end of the entrance, the first right-side door glows with three phenotype panels. One looks intermediate between two homozygotes. Another shows two allelic effects side by side. A rack beside them holds three population alleles. Imani closes the general route map and carries the same phenotype-comparison frame through that door. The unresolved question has narrowed from why a ratio differs to how alleles at one locus can relate to one another and how many allele variants can exist in a population."
 ],
 'close':'The gallery entrance now separates an observed departure from the mechanism that explains it. The next room tests altered allelic relationships directly.'
},
'U5-L32':{
 'title':'The Studio Where Intermediate and Simultaneous Effects Had Been Blended Together',
 'kicker':'Incomplete dominance changes the heterozygous phenotype toward an intermediate state, while codominance keeps both allelic effects distinguishable and multiple alleles describe population-level allele number.',
 'paragraphs':[
  "You enter the **Dominance Spectrum Studio** with the phenotype-comparison frame still locked into three windows. On your **left**, three tall phenotype columns hold the two homozygotes and an empty heterozygote position between them. Directly **ahead**, a split display waits beside a population allele rack. On your **right**, a glass case marked ABO contains three allele plaques labeled IA, IB, and i. Dr. Imani Reyes places the **gold generation ledger** under the center bench and sets the **mechanism identity cards** along its edge. The studio has been damaged by one broad sign that calls every unusual heterozygote blended. Imani removes the sign and leaves the underlying alleles visible before any phenotype panel is activated.",
  "At the left alcove, the two homozygous genotypes produce two different endpoint phenotypes. Imani places a heterozygous genotype between them. Its phenotype settles at an intermediate state relative to the two homozygotes. The alleles themselves do not merge into a new permanent allele. They remain distinct genetic variants that can segregate in later gametes. Once that geometry is clear, Imani clips the card **Incomplete dominance** beneath the left window. In incomplete dominance, neither allele is completely dominant and the heterozygote has an intermediate phenotype relative to the two homozygotes. The intermediate appearance therefore describes phenotype, not genetic blending of the alleles.",
  "The center display resets. This time the heterozygote activates two separate phenotype signals at once. Neither signal disappears into an intermediate value. Both allelic effects remain individually distinguishable in the same heterozygous phenotype. Imani clips a second card under the center window and names **Codominance**. In codominance, both alleles affect the heterozygous phenotype in separate, distinguishable ways, so the heterozygote differs from either homozygote. She places the incomplete-dominance and codominance cards side by side. One shows an intermediate heterozygote. The other shows both effects distinctly. Their alleles remain discrete in both mechanisms.",
  "Beside the codominance display stands a circular rack with more than two allele plaques for one gene. Imani rotates the rack so the whole population is visible, then chooses one modeled diploid individual. Only two allele copies move into that individual's genotype slots because a diploid individual ordinarily carries two copies of the locus. She names the population-level condition **Multiple alleles**. A gene has multiple alleles when more than two allele variants exist in the population, even though one diploid individual usually carries at most two alleles at that locus. The rack makes the level of description impossible to miss. Multiple alleles describes the collection of variants available in the population. It does not mean one ordinary diploid individual carries every variant at once.",
  "The right ABO case now lights up. Three common alleles enter the population rack, IA, IB, and i. Imani pairs IA with IB and the phenotype window preserves the effects associated with both alleles. She pairs IA with i and then IB with i. In the standard model, IA and IB are each dominant over i. She clips the label **ABO blood-group allele system** beneath the case. The human ABO blood-group gene has three common alleles, IA, IB, and i. IA and IB are codominant to one another and each is dominant over i. The same genetic system therefore demonstrates two separate ideas at once. The population has multiple alleles, and one particular heterozygous combination shows codominance.",
  "Imani asks you to look across the studio without reading the cards. The left alcove can be identified from an intermediate heterozygous phenotype. The center codominance panel can be identified because both allelic effects remain distinguishable. The allele rack can be identified because more than two variants exist in the population while one individual carries only the copies present in its genotype. The ABO case combines the latter two ideas without turning them into synonyms. The frame now preserves three different questions. What phenotype does a heterozygote show. How many allele variants exist in the population. What relationship holds among particular alleles.",
  "A side curtain opens toward the next room. Beyond it, the number of genes and the number of phenotypic effects change in opposite directions. One stage shows one gene interfering with another. Another combines several genes into one quantitative trait. A third begins with one gene and branches toward several effects. Imani carries the same frame forward. Allele interaction at one locus is now stable enough that the gallery can compare interactions among genes themselves."
 ],
 'close':'The studio now keeps incomplete dominance, codominance, multiple alleles, and the ABO system distinct by mechanism. The next room changes the question from allele relationship to gene interaction and effect count.'
},
'U5-L33':{
 'title':'The Theater Where One Gene, Many Genes, and Many Effects Had Swapped Roles',
 'kicker':'Epistasis is interaction between genes, polygenic inheritance is multiple genes contributing to one character, and pleiotropy is one gene influencing multiple effects.',
 'paragraphs':[
  "The curtain lifts on the **Gene-Interaction Theater**. On your **left**, two gene-control consoles feed one phenotype lamp and a movable shutter can block part of the signal. Directly **ahead**, a round brass turntable is engraved with two questions, how many genes contribute and how many phenotypic effects emerge. On your **right**, the stage divides into two branches. One branch receives inputs from several genes and ends at a continuous phenotype scale. The other begins with a single gene and splits toward several trait panels. Dr. Imani Reyes locks the **phenotype-comparison frame** around the theater so the left input, center mechanism, and right outcome remain fixed. The **gold generation ledger** opens to a fresh page labeled gene count and effect count.",
  "Imani activates the left stage first. Gene A sends a visible signal toward a pigment output. Gene B controls a shutter positioned in that pathway. When the genotype at gene B changes, the shutter closes and the pigment effect associated with gene A can no longer appear in the same way. Imani names this interaction **Epistasis**. Epistasis occurs when genotype at one gene affects the phenotypic expression of another gene. The defining relationship is interaction between genes. The scene does not require gene B to erase gene A from the genome. Gene A remains present. Its phenotypic expression is altered by the state of another gene in the pathway.",
  "The turntable rotates to the first right-side branch. Three gene inputs feed the same phenotype scale. Each input contributes to one phenotypic character, and their combined effects create a broader range of possible values. The output looks quantitative because different combinations across multiple contributing genes can shift the phenotype along the scale. Imani places the card **Polygenic inheritance** beneath this branch. Polygenic inheritance occurs when variation at two or more genes contributes to one phenotypic character, often producing quantitative variation. The geometry is many genes feeding one character. That directional picture stays visible on the ledger.",
  "The second right-side branch reverses the geometry. Imani begins with one gene at the top of a branching track. Its expression influences several downstream biological outcomes, so one genetic change can be associated with multiple traits or effects. She clips the card **Pleiotropy** beneath the branch. Pleiotropy occurs when expression of one gene influences multiple traits or effects. The ledger now holds the two diagrams beside each other. Polygenic inheritance shows multiple genes contributing to one character. Pleiotropy shows one gene influencing multiple effects. The arrows point in opposite organizational directions even though both mechanisms can make phenotype patterns more complex than a simple one-gene category.",
  "Imani returns the turntable to the center and adds the earlier multiple-allele rack as a comparison card. More than two allele variants in a population does not mean multiple genes contribute to the trait. Epistasis requires interaction between genes. Polygenic inheritance requires contributions from two or more genes to one character. Pleiotropy begins with one gene and reaches multiple effects. The same words one, many, gene, and trait appear across these ideas, so the theater relies on visible direction and causal role. A label cannot substitute for counting what enters the mechanism and what emerges from it.",
  "The phenotype lamp on the left changes one last time as Imani reopens the epistasis shutter. The output returns because the interacting gene state has changed, not because either gene has vanished. On the polygenic scale, several gene inputs remain active at once. On the pleiotropic branch, the single starting gene still feeds multiple outcomes. You can now identify each mechanism from its geometry before reading its card. That is the test Imani wants the gallery to pass.",
  "At the back of the theater, the floor rises toward a chromosome wall. The next exhibit replaces the gene-count turntable with actual chromosome locations. Blue and amber autosomes occupy one rack, while X and Y chromosome models stand in a separate central case. Imani closes the gene-interaction page and carries the frame upstairs. The next distinction depends on where a gene is physically located on a chromosome and on which chromosome-complement model is being used."
 ],
 'close':'The theater now separates gene interaction, many-gene contribution, and one-gene multiple effects by causal geometry. The route next moves from gene interaction to chromosome location.'
},
'U5-L34':{
 'title':'The Comparator Where Chromosome Location Had Been Confused With Identity',
 'kicker':'X-linked and Y-linked inheritance follow genes physically located on those chromosomes within an explicit chromosome-complement model, while autosomes remain a separate chromosome class.',
 'paragraphs':[
  "A wide steel doorway leads into the **Chromosome-Linked Inheritance Comparator**. On your **left**, a tall rack holds matched autosome pairs. Directly **ahead**, a central glass model displays X and Y chromosomes within an explicitly labeled human XX/XY inheritance model. On your **right**, two gene panels wait, one attached to an X chromosome and one attached to a Y chromosome. Dr. Imani Reyes places the **phenotype-comparison frame** around all three zones and slides the **gold generation ledger** beneath the center model. A boundary placard sits above the case. It states that this room is modeling chromosome transmission in a common human XX/XY system. The model does not define gender and does not capture the full biology of human sex development.",
  "Imani begins on the left rack. She points to the chromosome pairs that are outside the X and Y set designated in this model. She labels the class **Autosome**. In a given chromosome-based sex-determination model, an autosome is a chromosome other than the chromosome or chromosomes designated as sex chromosomes. Humans typically have 22 autosome pairs. The definition belongs to the stated chromosome model. The rack therefore does not imply that every species uses the same chromosome system. A smaller panel at the edge of the room shows that other sex-determination systems exist and that chromosomal sex-determination systems vary among species.",
  "The center case activates. A modeled XX parent produces gametes that are usually X-bearing. A modeled XY parent produces gametes that are usually X-bearing or Y-bearing. Imani writes **Human X/Y chromosome-complement model** on the ledger only after the chromosome movements are visible. In the common human XX/XY inheritance model, eggs usually carry an X chromosome and sperm usually carry an X or Y chromosome. The model describes chromosome transmission. Imani keeps the boundary placard lit throughout the scene so the chromosome complement is never used as a shortcut for gender or for every component of sex development.",
  "The right-side panels now move into position. A gene marker is clipped directly onto the X chromosome. Imani follows that marker through gamete formation and offspring chromosome combinations. Because the gene is physically located on the X chromosome, its inheritance follows the transmission of X chromosomes in the model. She names the marker **X-linked gene**. Beside it, a second marker sits directly on the Y chromosome. Its transmission follows Y-bearing lineages in the XX/XY model, and Imani names it **Y-linked gene**. The chromosome carrying the gene is the causal anchor. The terms do not describe every trait associated with biological sex or every trait that differs among people.",
  "With both right-side panels active, Imani clips the broader mechanism card **Sex-linked inheritance** beneath the frame. X-linked or Y-linked traits are determined by genes on those chromosomes, and inheritance patterns can be predicted from genotype and phenotype data including pedigrees. The phrase is being used here for genes on the designated sex chromosomes in the stated model. The species comparison panel stays visible because other organisms can use different chromosomal systems. That prevents the gallery from treating the human XX/XY example as a universal blueprint for sexual reproduction.",
  "Imani asks you to reconstruct the room from location alone. Autosomes remain on the left rack. The explicit human XX/XY chromosome-complement model remains in the center. Genes physically located on X or Y remain on the right. If a gene marker is moved from an autosome onto the X chromosome, the inheritance logic changes because chromosome location changes. If the marker remains on an autosome, calling it X-linked would be biologically wrong even if the phenotype happens to differ between groups. The mechanism identity card therefore follows gene location and chromosome transmission, not a superficial association with sex.",
  "A narrow rail leaves the X-linked panel and curves into the next room. One X chromosome carries a marked locus into a modeled XY genome, where no homologous copy of that region appears on the Y model. Imani carries the same frame along the rail. The next problem is no longer whether a gene is X-linked. The next problem is what one copy of an X-linked locus means in a typical modeled XY individual and how actual X chromosomes and alleles should be tracked through inheritance."
 ],
 'close':'The comparator now ties autosomal, X-linked, and Y-linked inheritance to explicit chromosome location and an explicit chromosome-complement model. The next rail follows one X-linked locus through transmission.'
},
'U5-L35':{
 'title':'The Rail Where a Single Copy Had Been Treated Like a Hidden Pair',
 'kicker':'Hemizygous means one copy of a gene or chromosomal region is present in an otherwise diploid genome, so X-linked transmission must track the actual chromosome and allele present.',
 'paragraphs':[
  "The X-linked panel feeds directly into the **Hemizygous Transmission Rail**. On your **left**, one modeled X chromosome carries a clearly marked allele at a defined locus. Directly **ahead**, a transparent carriage holds an otherwise diploid modeled XY genome with that single X-linked locus visible. On your **right**, offspring chromosome combinations line a sorting wall beside a small case of named disorder examples. Dr. Imani Reyes mounts the **phenotype-comparison frame** over the rail. The left window shows the X-linked allele source, the center window shows copy number and chromosome transmission, and the right window shows the offspring chromosome outcomes. The **gold generation ledger** keeps the parental chromosome complements and allele states visible through every step.",
  "Imani zooms in on the center carriage. At this X-linked locus, the modeled XY individual has one copy of the gene region on the X chromosome and no corresponding homologous allele at that locus on the Y model. She labels the single-copy state **Hemizygous**. Hemizygous describes having only one copy of a gene or chromosomal region in an otherwise diploid genome, as for many X-linked loci in typical XY individuals. Imani places homozygous and heterozygous comparison cards beside the carriage, then leaves them outside the mechanism window. Those terms describe relationships between two allele copies. The hemizygous state here contains one copy at the modeled region.",
  "The rail begins moving. The X chromosome with its marked allele enters gamete formation exactly as a chromosome, not as a verbal shortcut. Imani tracks which gametes carry that X and which gametes in the modeled XY parent carry a Y. On the other parent station, X-bearing gametes are tracked with their own allele states. The offspring wall fills only after the gametes combine. Imani then writes **X-linked transmission in an XX/XY model** beneath the center window. In a typical XX/XY model, an X-bearing parent transmits that X chromosome to offspring that inherit it according to gamete type. Pedigree predictions must therefore track the actual parental chromosome complements and alleles.",
  "A worn sign above the rail claims that X-linked inheritance can be solved with one mother-to-son slogan. Imani takes it down. The actual chromosome path is more reliable. An X-linked allele can move through different family relationships depending on which parent carries it, which gamete is formed, the offspring chromosome complement in the model, and whether the phenotype is dominant, recessive, penetrant, or affected by other biology. In a standard simple X-linked recessive pedigree model, a typical modeled XY individual can express a recessive phenotype with one relevant X-linked allele because only one copy of that locus is present. A typical modeled XX individual usually requires the corresponding recessive allele on both X chromosomes for that classic affected pattern, although real biology can include X-inactivation, chromosome variation, penetrance, and other complications.",
  "The right case opens to a small panel labeled **X-linked disorder examples**. It includes Duchenne muscular dystrophy, hemophilia A and B, and common red-green color-vision deficiencies. Imani keeps the examples physically to the side of the transmission rail. Their names are useful contexts for tracing X-linked inheritance, yet none of those disease names defines what X-linked means. The mechanism remains the physical location of the gene on X and the transmission of that chromosome and allele through the stated model.",
  "The phenotype-comparison frame now shows one continuous causal path. The left window contains the allele on an X chromosome. The center window contains a hemizygous modeled state and the actual chromosome transmission through gametes. The right window contains offspring chromosome and allele combinations, with example phenotypes interpreted only after the genotype is known. The learner can reconstruct the path without memorizing a family-role slogan. Imani closes the offspring case and keeps the marked X chromosome on her tablet.",
  "A mosaic of illuminated cell tiles appears through the next doorway. The question changes again. The next room is not tracing which parent transmitted an X chromosome. It begins within an XX somatic-cell lineage after inheritance has already occurred. Imani carries the frame toward the mosaic so the gallery can separate chromosome transmission from dosage regulation inside descendant cells."
 ],
 'close':'The rail now ties hemizygosity and X-linked transmission to actual chromosome copies and gametes. The next gallery examines what happens to X-chromosome activity within XX somatic-cell lineages.'
},
'U5-L36':{
 'title':'The Mosaic Where an Inactive X Had Been Mistaken for a Missing X',
 'kicker':'X-chromosome inactivation changes transcriptional activity and chromatin state in typical mammalian XX somatic cells while the chromosome remains present, creating lineage mosaics when different cells retain different active-X origins.',
 'paragraphs':[
  "The rail ends in the **X-Inactivation Mosaic Gallery**, a quiet circular room tiled with hundreds of cell-shaped panels. On your **left**, one enlarged early mammalian XX somatic-cell model shows two X chromosomes before a stable lineage pattern has been established. Directly **ahead**, a glass chamber surrounds one nucleus and can alter the transcriptional state of one X chromosome. On your **right**, the wall contains many descendant-cell patches, some illuminated blue and others amber according to which parental-origin X remains more transcriptionally active in that lineage. Dr. Imani Reyes centers the **phenotype-comparison frame** on the chamber and opens the **gold generation ledger** to a dosage-regulation page. The inherited chromosome complement remains written at the top so no one can mistake altered activity for chromosome loss.",
  "Imani begins with the left cell. Both X chromosomes are physically present. Early in development, one X in the modeled typical mammalian XX somatic cell becomes largely transcriptionally inactive for many X-linked genes while the other remains active. Imani dims the transcription lights around one chromosome but leaves the chromosome itself visible inside the nucleus. She names the process **X-chromosome inactivation**. In typical mammalian XX somatic cells, one X chromosome becomes largely transcriptionally inactive early in development, contributing to dosage compensation. Which X becomes inactive can vary among cells. The key event is a change in gene activity, not deletion of an X chromosome.",
  "The center chamber tightens the chromatin around the largely inactive X. It becomes a dense body at the nuclear edge in the model. Imani labels that condensed representation **Barr body**. A Barr body is the condensed form of a largely inactive X chromosome visible in some interphase nuclei. She leaves several tiny transcription windows glowing on the condensed chromosome because inactivation is not absolute. Some genes can escape X-chromosome inactivation. The wording on the ledger therefore says largely transcriptionally inactive. The gallery never converts that qualification into completely silent.",
  "Imani lets the modeled cell divide. Its descendant lineage retains the same active-X origin. She repeats the early choice in another starting cell, where the other parental-origin X remains active. That lineage expands with the opposite color. As many lineages spread across the right wall, the tiles form a patchwork. The mosaic does not require each mature cell to make a new random decision every time it divides. The pattern reflects early choices that are then propagated through descendant cell lineages. The physical X chromosomes remain present in the cells while their relative transcriptional activity differs.",
  "The phenotype-comparison frame now separates three concepts that appeared close together in the previous room. Hemizygous described one copy of a gene or region in an otherwise diploid genome. X-chromosome inactivation describes a regulatory state affecting one X in typical mammalian XX somatic cells. Barr body names the condensed chromatin form of a largely inactive X visible in some interphase nuclei. Imani places all three mechanism cards side by side but keeps their pictures different. One is copy number. One is regulation. One is a condensed structural manifestation of that regulation.",
  "At the edge of the room, a warning plaque repeats the boundary from the chromosome comparator. This is a model of dosage regulation in typical mammalian XX somatic cells. It is not a universal statement that every cell with two X chromosomes behaves identically or that every gene on the inactive X is silent. It also does not turn chromosome complement into a definition of gender. The gallery is preserving a specific cellular mechanism and the limits of that mechanism.",
  "The mosaic wall fades into a sunlit greenhouse corridor. The same phenotype-comparison frame rolls forward, but the chromosome activity controls remain behind. The next room will hold genotype constant and change temperature, soil chemistry, or ultraviolet exposure. Imani points to the ledger. The gallery has finished asking how chromosome location and dosage alter phenotype. It will now ask how environmental context can change phenotype without changing the inherited genotype."
 ],
 'close':'The mosaic gallery now distinguishes X-chromosome inactivation, Barr bodies, and hemizygosity by copy number, regulation, and chromatin state. The final route holds genotype constant while changing environmental context.'
},
'U5-L37':{
 'title':'The Conservatory Where the Same Genotype Kept Changing Its Display',
 'kicker':'Environmental conditions can alter physiology and gene expression so the same genotype can produce different phenotypes, a form of phenotypic plasticity that still depends on biological context.',
 'paragraphs':[
  "Glass doors slide open into the **Phenotypic Plasticity Conservatory**. On your **left**, two climate chambers hold matched genotype cards under cool and warm conditions. Directly **ahead**, the brass **phenotype-comparison frame** has been rebuilt around one locked genotype card and a set of adjustable environmental controls. On your **right**, plant beds with controlled soil chemistry sit beside a human skin-cell display under regulated ultraviolet exposure. Dr. Imani Reyes places the **gold generation ledger** under the center controls and writes one instruction across the top. Hold genotype constant first. The room can then show what changes when environmental conditions alter physiology or gene expression.",
  "Imani begins at the left climate chambers with a temperature-sensitive pigment pathway model based on examples such as Himalayan rabbits and Siamese cats. The genotype card remains identical in both chambers. The temperature changes the activity of pigment-producing processes in different body regions, and the phenotype pattern changes with that environmental condition. She labels the mechanism card **Temperature-dependent pigmentation example**. Temperature can influence pigment-producing pathways in some mammals, producing environment-dependent coat-color patterns. The example is useful because the same inherited genotype is present while the environmental temperature changes the activity of the biological pathway.",
  "At the center frame, Imani locks the genotype card in place and changes one environmental control. A gene-expression meter and a physiology meter respond. The phenotype window shifts even though the genotype card has not changed. She writes **Genotype-by-environment context** beneath the mechanism window. The phenotype expressed by a genotype can depend on environmental conditions because environmental inputs can alter physiology and gene expression. She then adds the broader term **Environmental effects on phenotype**. Environmental conditions can influence gene expression so the same genotype can produce different phenotypes, a property called phenotypic plasticity. The important relationship is not that environment replaces genotype. Phenotype emerges from biological processes operating in a particular inherited and environmental context.",
  "The right plant bed becomes the next comparison. Imani keeps a susceptible plant genotype represented on the frame while the soil chemistry changes. Differences in pH and associated ion availability alter the conditions experienced by the plant and can influence flower color in examples such as hydrangeas. She clips the card **Soil-pH flower-color example** beneath the bed. The plant is not choosing a new allele when the soil changes. The environmental chemistry affects the biological processes that contribute to the expressed phenotype.",
  "Beside the plant bed, the ultraviolet panel activates. Human skin cells receive increased ultraviolet exposure and a regulated cellular response increases melanin production. Imani names this the **UV and melanin example**. Ultraviolet exposure can increase melanin production in human skin through regulated cellular responses, making it another environmental effect on phenotype. The mechanism window shows signaling and gene-regulatory responses feeding pigment production. The response is physiological and regulated. The ultraviolet exposure does not rewrite a person's inherited genotype in order to produce the short-term pigmentation response being modeled here.",
  "Imani now divides the frame into two final comparison rows. In one row, two different genotypes can produce different phenotypes under the same environment. In the second row, the same genotype can produce different phenotypes across different environments. The first reminds you that inherited variation still matters. The second makes phenotypic plasticity visible. The conservatory therefore blocks an equally misleading conclusion that all phenotypic variation is environmental. Environmental context can shape phenotype, yet genotype, developmental history, physiology, gene regulation, and environmental inputs all remain part of the causal system.",
  "The gallery route behind you illuminates one room at a time. Incomplete dominance changed the heterozygous phenotype. Codominance preserved two distinguishable allelic effects. Multiple alleles changed population-level allele number. Epistasis changed how one gene affected another gene's phenotypic expression. Polygenic inheritance combined several genes into one character. Pleiotropy sent one gene toward several effects. Chromosome-linked inheritance followed gene location. X-chromosome inactivation changed dosage regulation across cell lineages. The conservatory changed environmental context while holding genotype fixed. Imani closes the last mechanism card. The phrase non-Mendelian no longer hides a pile of exceptions. Each pattern now has a specific biological cause that can be reconstructed from the fixed input, mechanism, and output windows."
 ],
 'close':'The trait gallery is repaired. Similar-looking phenotype patterns now separate cleanly by allelic interaction, gene interaction, chromosome location and dosage, or environmental context.'
}
}


def zones_for(b):
    vals=ZONE_COPY[b['locus_id']]
    return [{'position':p,'name':name,'memory_anchor':anchor,'description':desc} for p,name,anchor,desc in vals]

def make_cast(b):
    casts=[GUIDE,FRAME,MECHANISM_CARDS,GENERATION_LEDGER]
    for p,name,anchor,desc in ZONE_COPY[b['locus_id']]:
        casts.append({'name':name,'kind':'scientific zone','visual':desc,'job':f'occupies the {p} zone and preserves the fixed scientific role of {anchor}.'})
    return casts

def make_beats(b):
    return [{'object_id':t['knowledge_id'],'term':t['canonical_term'],'story':f"The {b['scene_title']} makes {t['canonical_term']} visible through its fixed input, mechanism, and outcome geometry before the exact name is attached.",'science':CANON[t['knowledge_id']]['canonical_verified_statement'],'exact_name':bool(t['exact_name_recall']),'hint':BEAT_IMAGES[t['knowledge_id']],'name_support':t['name_support']} for t in b['term_introductions']]

def make_snapshot(b):
    return [{'term':t['canonical_term'],'meaning':t['canonical_science'],'image':BEAT_IMAGES[t['knowledge_id']]} for t in b['term_introductions']]

briefs=[B[f'U5-L{i:02d}'] for i in range(31,38)]
scenes=[]
for idx,b in enumerate(briefs):
    n=NARR[b['locus_id']]; q=b['quick_recall']; checkpoint=bool(q['enabled'])
    cp={'U5-L32':'U5-K-025','U5-L34':'U5-K-027'}.get(b['locus_id']) if checkpoint else None
    scenes.append({
      'scene_index':idx,'locus_id':b['locus_id'],'locus':b['scene_title'],'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['micro_anchor'],'scene_layout':{'orientation':b['orientation_sentence'],'zones':zones_for(b)},
      'cast':make_cast(b),'continuity_object':J6['continuity_object'],
      'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':make_beats(b),'memory_snapshot':make_snapshot(b),
      'misconception_guards':b['misconception_guards'],'exit_memory':b['exit_memory'],
      'checkpoint':checkpoint,'checkpoint_object_id':cp,'checkpoint_prompt':q.get('candidate_prompt','') if checkpoint else '',
      'checkpoint_answer':q.get('answer','') if checkpoint else '',
      'checkpoint_hint':('Return to the fixed phenotype-comparison frame and identify what changed in the heterozygote or where the gene physically sits on the chromosome before naming the mechanism.' if checkpoint else ''),
      'next_locus':briefs[idx+1]['scene_title'] if idx+1<len(briefs) else None,'causal_transition':b['causal_transition']['transition_logic'],
    })

journey={
 'palace_id':'U5-J6','unit_id':'unit-5','palace_name':'Beyond-Mendel Trait Gallery','story_title':'The Gallery That Labeled Every Pattern the Same Way',
 'tagline':'Repair one phenotype gallery by keeping genotype or context, mechanism, and outcome in fixed positions until each non-simple inheritance pattern can be identified from its biological cause.',
 'guide':GUIDE,
 'premise':'The Beyond-Mendel Trait Gallery has erased the mechanisms from its exhibits. Intermediate phenotypes, simultaneous allelic effects, gene interactions, chromosome-linked patterns, X-inactivation mosaics, and environment-dependent phenotypes have all been filed under one vague label. The gallery can be repaired only by carrying the same phenotype-comparison frame through every room and changing one biological mechanism at a time.',
 'mission':'Follow Dr. Imani Reyes through seven connected locations. Separate altered allelic relationships from population allele number, distinguish epistasis from polygenic inheritance and pleiotropy, tie X-linked and Y-linked patterns to explicit chromosome location and chromosome-complement models, separate hemizygosity from X inactivation, and finish by holding genotype constant while environmental context changes phenotype.',
 'finale':'The gallery now classifies patterns by mechanism. Allelic interaction, population allele number, interaction among genes, chromosome location, dosage regulation, and environmental context each produce a different visible relationship between input and phenotype. The phrase non-Mendelian remains a broad description of departures from simple one-gene complete-dominance expectations and no longer substitutes for the specific biological cause.',
 'estimated_minutes':27,'scene_count':7,'checkpoint_count':2,'student_release':'DEVELOPER_PREVIEW_F4F',
 'learner_rule':'Keep the same three-window phenotype-comparison frame in mind. The left window holds genotype, chromosome state, or context. The center window reveals the mechanism. The right window shows the phenotype or inheritance pattern. Name the mechanism only after that causal relationship is visible. Optional Quick Recall appears only twice.',
 'route_orientation':'This is one continuous south-to-east gallery route. Begin at the south pattern entrance, turn west into the dominance studio, cross the central gene-interaction theater, climb to the north chromosome comparator, follow the northeast hemizygous rail, enter the east X-inactivation mosaic gallery, and finish in the sunlit conservatory. The same phenotype-comparison frame, mechanism cards, and gold ledger remain visible throughout.',
 'route':route,'scenes':scenes,'narrative_design':'U5-F4F-NARRATIVE-1.0'
}
(U5/'journeys').mkdir(exist_ok=True)
(U5/'journeys'/'U5-J6.json').write_text(json.dumps(journey,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
registry={
 'schema':'memory-palace-v2-unit5-f4f-journeys-1.0','unit_id':'unit-5','stage':'F4F','student_release':False,'preview_release':True,
 'journey_count':6,'scene_count':37,'checkpoint_count':13,
 'guided_journeys':[{k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']} for j in [J1,J2,J3,J4,J5,journey]]
}
(U5/'journeys-f4f.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
status={
 'unit_id':'unit-5','unit_number':5,'title':'Heredity','status':'F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW','pipeline_status':'POLISHED_NARRATIVE_J1_J2_J3_J4_J5_J6_F4F',
 'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','student_release':False,'preview_release':True,
 'canonical_records':152,'review_flags_resolved':37,'teacher_ppt_slides':112,'ced_topics':5,'ced_atoms':34,'architecture_journeys':8,'architecture_loci':50,
 'scene_briefs':50,'preview_journeys':6,'preview_scenes':37,'preview_checkpoints':13,
 'journey_1_records':20,'journey_2_records':18,'journey_3_records':8,'journey_4_records':25,'journey_5_records':7,'journey_6_records':24,
 'next_gate':'F4G_JOURNEY7_ONLY_AFTER_F4F_PROSE_QA'
}
(U5/'status-f4f.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(U5/'status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
words=sum(len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs']))) for s in scenes)
manifest={'schema':'memory-palace-v2-unit5-f4f-release-manifest-1.0','unit_id':'unit-5','stage':'F4F','student_release':False,'preview_release':True,'journey_count':6,'scene_count':37,'checkpoint_count':13,'journey_6_records':24,'journey_6_narrative_words':words,'f1_canonical_records':152,'f2_permanent_loci':50,'f3_scene_briefs':50,'next_gate':'F4G'}
(U5/'f4f-release-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

course_path=ROOT/'content'/'ap-biology'/'course.json'; course=json.loads(course_path.read_text(encoding='utf-8'))
cu5=next(u for u in course['units'] if u['unit_id']=='unit-5')
cu5.update({'status':'F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW','journey_count':6,'scene_count':37,'canonical_lock':'LOCKED_F1','source_status':'AUDITED_SCIENCE_LOCKED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVE_J1_F4A_J2_F4B_J3_F4C_J4_F4D_J5_F4E_J6_F4F','canonical_records':152,'review_flags_resolved':37,'ced_atoms':34,'teacher_ppt_slides':112,'student_release':False,'preview_release':True,'pipeline_stage':'UNIT5_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW_F4F'})
course_path.write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Prefer F4F in the developer-preview API while leaving released runtime version unchanged.
backend=ROOT/'backend'/'content.py'
text=backend.read_text(encoding='utf-8')
old='    if unit_id == "unit-5":\n        path=UNIT5_DIR / "journeys-f4e.json"\n        if not path.exists(): path=UNIT5_DIR / "journeys-f4d.json"'
new='    if unit_id == "unit-5":\n        path=UNIT5_DIR / "journeys-f4f.json"\n        if not path.exists(): path=UNIT5_DIR / "journeys-f4e.json"\n        if not path.exists(): path=UNIT5_DIR / "journeys-f4d.json"'
if old in text:
    text=text.replace(old,new)
elif 'path=UNIT5_DIR / "journeys-f4f.json"' not in text:
    raise RuntimeError('Could not patch Unit 5 developer-preview registry preference to F4F')
backend.write_text(text,encoding='utf-8')

lock_files=['journeys/U5-J6.json','journeys-f4f.json','status-f4f.json','f4f-release-manifest.json']
lock={'schema':'memory-palace-v2-unit5-content-lock-f4f-1.0','unit_id':'unit-5','stage':'F4F','lock_status':'LOCKED_F4F_J6','student_release':False,'preview_release':True,'files':{}}
for rel in lock_files:
    p=U5/rel; lock['files'][rel]={'bytes':p.stat().st_size,'sha256':sha(p)}
(U5/'content-lock-f4f.json').write_text(json.dumps(lock,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines=['# Unit 5 F4F · Journey 6 Narrative','',f'## {journey["story_title"]}','',journey['tagline'],'','**Palace**  Beyond-Mendel Trait Gallery  ','**Guide**  Dr. Imani Reyes  ','**Route**  '+' → '.join(x['locus'] for x in route),'']
for s in scenes:
    lines += [f"## {s['scene_index']+1}. {s['locus']} — {s['title']}",'',f"*{s['scene_kicker']}*",'']+s['story_paragraphs']+['']
(ROOT/'docs'/'UNIT5_F4F_JOURNEY6_STORY.md').write_text('\n'.join(lines),encoding='utf-8')
release=['# Unit 5 F4F Release','', 'Unit 5 F4F authors and locks Journey 6 only while preserving Journeys 1–5 byte-for-byte against their earlier narrative locks. Unit 5 remains a developer preview and is not student released.','', '## Accounting','', '- Journeys 1–5 preserved: **30 scenes / 78 records / 11 optional recalls**', '- Journey 6 authored: **7 scenes / 24 records / 2 optional recalls**', f'- Journey 6 narrative words: **{words}**', '- Total Unit 5 preview: **6 journeys / 37 scenes / 13 optional recalls**','', '## Scientific continuity','', '- Non-simple ratios are separated from the biological mechanism that produces them, and statistical departure is not inferred from visual difference alone.', '- Incomplete dominance, codominance, and multiple alleles remain distinct by heterozygous phenotype and population allele number.', '- The ABO system combines a three-allele population model with codominance of IA and IB and dominance of each over i.', '- Epistasis, polygenic inheritance, and pleiotropy remain distinct through gene-to-gene interaction, many-genes-to-one-character geometry, and one-gene-to-many-effects geometry.', '- X-linked and Y-linked inheritance are tied to explicit chromosome location within an explicit chromosome-complement model.', '- The XX/XY model is never treated as a definition of gender or a complete model of human sex development, and other sex-determination systems remain acknowledged.', '- Hemizygosity remains a copy-number state, X-chromosome inactivation remains a regulatory process, and Barr body remains a condensed chromatin state.', '- Environmental effects on phenotype hold genotype constant while context changes physiology or gene expression; phenotypic plasticity is not treated as evidence that all variation is environmental.','', '## Release boundary','', 'No Unit 5 Memory Objects, Review runtime, Challenge Lab runtime, or student-facing Unit 5 release is created in F4F. Journeys 7–8 remain at the F3 scene-brief stage.','']
(ROOT/'docs'/'UNIT5_F4F_RELEASE.md').write_text('\n'.join(release),encoding='utf-8')
print(json.dumps({'journey':'U5-J6','scenes':7,'records':24,'checkpoints':2,'narrative_words':words,'student_release':False,'preview_release':True},indent=2))
