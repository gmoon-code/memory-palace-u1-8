from __future__ import annotations
import json,re,hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content'/'ap-biology'/'unit-7'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()

CANON={r['knowledge_id']:r for r in read(U7/'source/canonical-unit7-f1.json')['canonical_catalog']}
F3=read(U7/'briefs/scene-briefs-f3.json')
B={b['locus_id']:b for b in F3['scene_briefs'] if b['journey_id']=='U7-J3'}
JB=read(U7/'briefs/journey-briefs-f3.json')
J3=next(j for j in JB['journeys'] if j['journey_id']=='U7-J3')
J1=read(U7/'journeys/U7-J1.json')
J2=read(U7/'journeys/U7-J2.json')

GUIDE={
 'name':'Dr. Imani Vale',
 'role':'evolutionary-systems curator',
 'visual':'charcoal field jacket, pale-green specimen gloves, a slim brass pointer, and a transparent evidence dossier tucked beneath her left arm',
 'story_job':'keeps each specimen physically attached to the observation it provides and records the specific evolutionary inference on the correct dossier tab without allowing one evidence type to inherit the job of another'
}
CONTINUITY=J3['continuity_object']

ROUTE=[
 {'scene_index':0,'locus':'Evidence Convergence Atrium','short':'Convergence','floor':'Atrium','symbol':'EVIDENCE'},
 {'scene_index':1,'locus':'Fossil Timeline and Dating Vault','short':'Fossil time','floor':'Time vault','symbol':'TIME'},
 {'scene_index':2,'locus':'Homology Morphology Hall','short':'Homology','floor':'Morphology hall','symbol':'HOMOLOGY'},
 {'scene_index':3,'locus':'Vestigial and Embryology Alcove','short':'Vestigial','floor':'Development alcove','symbol':'REMNANT'},
 {'scene_index':4,'locus':'Analogous Structure Wing','short':'Analogy','floor':'Flight wing','symbol':'ANALOGY'},
 {'scene_index':5,'locus':'Molecular Evidence Scanner','short':'Molecules','floor':'Sequence lab','symbol':'DNA'},
 {'scene_index':6,'locus':'Eukaryotic Common-Ancestry Archive','short':'Cell features','floor':'Cell archive','symbol':'EUK'},
 {'scene_index':7,'locus':'Continuing Evolution Monitor','short':'Evolution now','floor':'Live monitor','symbol':'NOW'},
 {'scene_index':8,'locus':'Genetic-Diversity Resilience Conservatory','short':'Resilience','floor':'Conservatory','symbol':'VARIATION'},
]

ZONES={
'U7-L25':[
 ('left','Extinct and fossil evidence wing','PAST','A dark stone gallery holds fossils, strata diagrams, and extinct-lineage evidence whose job is to document organisms and change through geological time.'),
 ('center','Multiple-evidence convergence table','INFERENCE','A circular glass table has six dossier slots so observations remain separated until several independent lines support the same evolutionary explanation.'),
 ('right','Extant geographic and molecular evidence wing','LIVING','Living populations, island-mainland maps, anatomical specimens, and sequence strips provide evidence from organisms that still exist.')],
'U7-L26':[
 ('left','Fossil-record timeline','OLDER → YOUNGER','A floor-to-ceiling stratigraphic wall keeps fossils embedded within visibly ordered geological layers before numerical ages are assigned.'),
 ('center','Radiometric-dating vault','ISOTOPE CLOCK','A shielded glass vault pairs datable material or surrounding rock with isotope clocks chosen for appropriate timescales.'),
 ('right','Carbon-14 range boundary','RECENT ONLY','A short illuminated timeline ends far before the deep-time fossil wall and prevents carbon-14 from being used as a universal fossil clock.')],
'U7-L27':[
 ('left','Comparative-morphology specimens','FORM','A row of forelimb models preserves the same underlying bone positions while current shapes and functions differ.'),
 ('center','Homology framework','SHARED PATTERN','A transparent overlay aligns corresponding structural elements and traces the inherited pattern through a common-ancestry diagram.'),
 ('right','Homologous-structure comparison','DIFFERENT JOBS','Matched structures remain side by side with different present-day functions so shared ancestry is not confused with identical use.')],
'U7-L28':[
 ('left','Embryological-homology display','DEVELOPMENT','Related-lineage embryo models illuminate shared developmental structures before their adult forms diverge.'),
 ('center','Vestigial-structure alcove','ANCESTRAL REMNANT','A reduced inherited structure is shown beside its larger ancestral counterpart so loss or modification of ancestral function remains visible.'),
 ('right','Reduced or modified present-day functions','STILL HAS ROLES','A function panel records any retained or modified role and blocks the museum from labeling vestigial structures simply useless.')],
'U7-L29':[
 ('left','Bird, bat, and insect flight comparison','FLIGHT','Three suspended flight models share the same broad function while their structural histories remain visibly different.'),
 ('center','Analogous-structure wing','INDEPENDENT ORIGIN','The flight surfaces align by function while separate lineage paths show that similar flight structures can arise independently.'),
 ('right','Homology-versus-analogy discriminator','ANCESTRY / FUNCTION','A split panel keeps the homologous tetrapod forelimb skeleton of bird and bat separate from independently evolved flight function.')],
'U7-L30':[
 ('left','DNA sequence comparison','DNA','Aligned homologous DNA regions preserve taxon names and nucleotide positions so similarities and differences are compared position by position.'),
 ('center','Molecular-homology scanner','MATCH','A scanner highlights shared sequence positions only after homologous regions are aligned across the same comparison set.'),
 ('right','Protein sequence comparison','PROTEIN','Aligned amino-acid sequences provide a second molecular comparison using the same taxa and labeled homologous molecules.')],
'U7-L31':[
 ('left','Membrane-bound organelle archive','ORGANELLES','Cell models from multiple eukaryotic lineages display conserved membrane-bound organelles in the same evidence case.'),
 ('center','Eukaryotic common-ancestry registry','SHARED CELL PLAN','A central registry overlays conserved structural and molecular features across eukaryotic lineages.'),
 ('right','Linear chromosome and intron archive','CHROMOSOMES / INTRONS','Linear chromosome models and intron-containing gene diagrams remain beside the cell architecture as conserved molecular features.')],
'U7-L32':[
 ('left','Genomic and fossil change feed','THROUGH TIME','A scrolling record combines dated fossil change with genomic differences measured across generations and lineages.'),
 ('center','Continuing-evolution monitor','EVOLUTION CONTINUES','A central population monitor updates only when evolutionary mechanisms produce heritable population change across generations.'),
 ('right','Resistance and pathogen evolution feed','SELECTION NOW','Bacterial, pest, and pathogen population panels track heritable variants and changing frequencies under antibiotics, pesticides, or changing host environments.')],
'U7-L33':[
 ('left','Low-diversity vulnerability enclosure','LOW VARIATION','A population with very few heritable variants faces the same new environmental pressure as the comparison population.'),
 ('center','Genetic-variation resilience conservatory','VARIATION','A larger set of inherited variants is displayed across one population without labeling every variant beneficial.'),
 ('right','Tolerant-variant and changing-fitness enclosure','CONTEXT','A novel pressure changes which variants confer higher reproductive success, while a condor case records diversity lost during a bottleneck.')],
}

NARR={
'U7-L25':{
 'title':'The Museum Has Evidence Everywhere and an Argument Nowhere',
 'kicker':'Evolutionary evidence becomes useful only when each observation is connected to the specific inference it can support.',
 'paragraphs':[
  "The doors of the **Evolution Evidence Museum** open into a circular stone atrium where a storm of labels has gone wrong. On your **left**, the extinct and fossil wing is stacked with fossil casts, layer diagrams, and cards from organisms that no longer exist. Directly **ahead**, a circular glass convergence table has six empty slots arranged around one blank inference column. On your **right**, the living-evidence wing contains island maps, anatomical models, DNA strips, and specimens from extant populations. Dr. Imani Vale stands at the center with a thick transparent dossier whose tabs read TIME, MORPHOLOGY, MOLECULES, CONSERVED CELL FEATURES, CONTEMPORARY CHANGE, and POPULATION DIVERSITY. A red museum warning flashes above her. EVERY OBJECT HAS BEEN FILED UNDER PROOF OF EVOLUTION.",
  "Imani lifts the first fossil card from the left wing and refuses to place it on the center table until its job is stated. A fossil can tell you that an organism or trace existed in the past and can contribute to a record of change through geological time. It cannot, by itself, tell you everything about how closely two living species are related. She places the fossil under the TIME tab. Then she takes a DNA strip from the right wing. Sequence similarity can support common ancestry when homologous sequences are compared appropriately. She files that under MOLECULES. The physical separation makes a basic rule visible. Different evidence types answer different evolutionary questions.",
  "The center table now lights the relationship **Extant and extinct evidence**. Molecular, morphological, genetic, and fossil evidence from living and extinct organisms informs evolutionary history. The word *informs* matters. Each specimen contributes an observation that has to be interpreted. An extinct organism can contribute fossil and morphological evidence. A living organism can contribute morphology, geography, DNA, proteins, and present-day population data. Imani writes the observation on the left side of each dossier card and the inference on the right side so the two can never merge into one vague statement.",
  "She then opens an island map from the right wing. A lineage on an island resembles a lineage from a nearby mainland more closely than distant alternatives in the display. The geography supports a colonization-and-divergence hypothesis. Imani places it under a geographic evidence tab and names the **Biogeographic island-mainland pattern**. Similarity between island organisms and nearby mainland lineages can support hypotheses of colonization followed by divergence. The map does not claim that geography alone reconstructs every branch. It contributes one line of evidence whose strength grows when independent evidence agrees.",
  "That agreement is what the center table is built to show. Imani places geological, geographic, morphological, molecular, biochemical, and quantitative evidence into separate illuminated slots. When several independent lines point toward the same history of ancestry or change, the center ring brightens. This is **Multiple independent evidence streams**. Evolution is supported by converging geographical, geological, physical, biochemical, and mathematical evidence. Convergence strengthens an explanation because independent observations reach compatible conclusions through different routes.",
  "The museum warning drops from red to amber, yet the TIME slot begins pulsing. A fossil card has been stamped 92 MILLION YEARS OLD even though no dating method or geological context is attached to it. Imani closes the convergence table and slides the fossil into the dossier without accepting the number. The next corridor descends into a vault where fossils remain inside their rock context and every numerical age must earn its place through an appropriate clock."
 ]},
'U7-L26':{
 'title':'The Fossil Vault Refuses to Put One Clock on All of Deep Time',
 'kicker':'Fossil ages depend on geological context and timescale-appropriate radiometric evidence, with carbon-14 restricted to relatively recent organic remains.',
 'paragraphs':[
  "The **Fossil Timeline and Dating Vault** runs downward like a canyon cut through stone. On your **left**, a floor-to-ceiling wall preserves older and younger layers around a fossil specimen so its stratigraphic position remains visible. Directly **ahead**, the center radiometric vault contains sealed isotope clocks beside samples of datable material and surrounding rock. On your **right**, a short illuminated timeline marked CARBON-14 stops far before the deep-time wall continues. Imani clips the TIME tab of the dossier to the railing and places the unverified fossil card beneath the rock-layer display.",
  "She first removes the false numerical age and leaves the specimen inside its geological context. The museum now recognizes the object itself as a **Fossil**. A fossil is preserved evidence of a past organism, including body remains, mineralized structures, impressions, or traces of activity. The important point is wider than bones. A preserved trace can count as fossil evidence when it records past biological activity. Imani keeps the fossil physically embedded in context so the object never floats free of the rock history that helps constrain its age.",
  "The left wall scrolls through many such specimens and traces. Together they form the **Fossil record**. The fossil record documents changes in organisms through geologic time while remaining incomplete and biased toward conditions favorable to fossilization. Gaps therefore do not mean that no organisms existed during every missing interval. Fossilization is selective in the ordinary physical sense that some environments, tissues, and events preserve evidence more readily than others. The dossier receives an observation about change through time and a limitation about incompleteness on the same card.",
  "Imani then turns to the center vault. A sample is paired with an isotope whose decay behavior matches the relevant timescale. Only after that match is visible does she name **Radiometric dating**. Radiometric dating estimates ages from predictable radioactive decay, and isotope choice must match the age range being studied. The vault refuses to accept a clock simply because it is radioactive. The method has to fit the material, the geological setting, and the timescale. Relative rock context and numerical radiometric evidence remain separate forms of age information that can support one another.",
  "The right-hand carbon-14 strip flashes as the system tries to date a very old fossil with the same clock used for recent organic remains. Imani stops it at the boundary. Carbon-14 has a short geologic half-life and is useful for relatively recent organic remains. It is not the standard isotope for very old fossils. Older fossils are commonly constrained using surrounding rock layers and longer-lived radioisotopes. The broader process is **Dating fossils**. Fossil ages can be inferred using rock context, radiometric methods appropriate to the timescale, and geographic or geologic information.",
  "The dossier TIME tab now contains four separate entries. FOSSIL OBSERVATION. FOSSIL-RECORD PATTERN. GEOLOGICAL CONTEXT. APPROPRIATE RADIOMETRIC ESTIMATE. The original age stamp is replaced by a supported age range, and the warning disappears from the vault. As the door opens, a row of forelimb models rises in the next hall. They perform different jobs, yet the same bones keep appearing in the same underlying order. The next evidence question is no longer when an organism lived. It is what a repeated structural pattern can reveal about ancestry."
 ]},
'U7-L27':{
 'title':'Different Limbs Keep Hiding the Same Structural Blueprint',
 'kicker':'Homology is similarity from shared ancestry, and comparative morphology makes that inherited structural correspondence visible even when present-day functions differ.',
 'paragraphs':[
  "The **Homology Morphology Hall** is long, bright, and almost empty except for three suspended forelimb models. On your **left**, comparative specimens display the forelimbs of different tetrapod lineages with corresponding bones tagged by position. Directly **ahead**, a transparent center framework can slide the models over one another until matching structural elements align. On your **right**, the same limbs remain separated again under labels for different present-day functions. Imani lays the MORPHOLOGY tab of the dossier flat beneath the display and asks you to ignore function long enough to compare structure.",
  "The left specimens do not have identical proportions. One limb is lengthened in one region, another is shortened, and another carries a different current function. Imani aligns the corresponding elements in the center framework. The same underlying relationship among major bones remains recognizable. This comparison is **Comparative morphology**. Comparative morphology uses structural similarities and differences among organisms to infer functional and evolutionary relationships. The task begins with correspondence among structures, not with a judgment that two organisms look generally alike. She has you follow each matched element from proximal to distal position so the inference comes from an organized structural pattern. A single superficial resemblance would carry much less weight than multiple corresponding elements arranged in the same inherited relationship.",
  "Once the shared structural pattern is visible, Imani names **Homology**. Homology is similarity caused by shared ancestry, even when descendant structures or sequences have different functions. The center overlay traces the corresponding bones back toward a common ancestral pattern. The right-side function labels are allowed to differ because inherited structure can be modified over evolutionary time. A shared ancestral origin does not require every descendant structure to perform the same job.",
  "The right display now names the anatomical case more specifically. **Homologous structures** share an underlying inherited structural pattern because of common ancestry, even when they perform different functions. Imani rotates the models slowly while the correspondence lines remain attached. Changing orientation cannot erase the shared arrangement. The relationship is structural and historical, not a trick of viewing angle.",
  "She files the result under **Morphological homology**. Homologous and vestigial structures provide evidence of common ancestry. The wording deliberately leaves a second kind of structural evidence waiting. A structure can be inherited from an ancestor even after much of its ancestral function has been reduced or altered. The museum had previously labeled such structures USELESS, which erased both their evolutionary history and any present-day role they still retain.",
  "The optional recall shutter lowers across the hall, leaving only the aligned bone pattern visible through a narrow window. When the shutter rises, a side door opens into a quieter alcove. Embryo models glow on the left. A reduced inherited structure sits in the center beside a larger ancestral counterpart. On the right, a function panel has been crossed out by the broken museum system. The next scene will repair the idea that evolutionary remnants must have no function at all."
 ]},
'U7-L28':{
 'title':'A Reduced Structure Can Carry History Without Being Useless',
 'kicker':'Embryological homology and vestigial structures are distinct ancestry evidence, and vestigial structures may retain reduced or modified functions.',
 'paragraphs':[
  "The **Vestigial and Embryology Alcove** is smaller and darker than the morphology hall. On your **left**, related-lineage embryo models illuminate comparable developmental structures before their adult forms diverge. Directly **ahead**, a reduced adult structure is displayed beside a larger ancestral version so the inherited relationship can be seen. On your **right**, a present-day function panel lists reduced or modified roles instead of an empty box. Imani opens the MORPHOLOGY tab to a fresh page and keeps the three zones separate before any inference is entered.",
  "The embryo display activates first. Comparable structures appear during development across related lineages, then contribute to different adult outcomes. Imani records **Embryological homology**. Shared developmental structures can provide evidence of common ancestry when homologous embryonic features develop into different adult structures. The evidence comes from a conserved developmental relationship. It does not require the adult structures to remain identical.",
  "The center alcove then compares an inherited remnant with the larger ancestral feature from which it descended. Much of the ancestral function has been reduced or altered over evolutionary time, yet the structure itself remains part of the descendant organism. Imani names a **Vestigial structure** only after that ancestry relationship is visible. A vestigial structure is an inherited remnant of an ancestral feature that has lost much or all of its original function and may retain reduced or modified functions.",
  "The museum system tries to replace the right panel with the word FUNCTIONLESS. Imani blocks the change. Vestigial does not mean that every present-day role has disappeared. A structure can retain a reduced function, a modified function, or another biological role while still being vestigial with respect to an ancestral function. The dossier records ANCESTRAL FUNCTION REDUCED OR MODIFIED and PRESENT-DAY ROLE MAY REMAIN on separate lines. She then covers the ancestral comparison and asks whether the present-day structure alone would justify calling it vestigial. The answer remains incomplete until ancestry and the reduction or modification of ancestral function are part of the evidence. The label is historical as well as structural.",
  "Imani places the embryology card and vestigial card side by side without merging them. Both can support common ancestry, yet they do so through different observations. Embryological homology uses shared developmental structures. Vestigial evidence uses an inherited remnant whose ancestral role has been reduced or modified. The distinction keeps the evidence specific and prevents the museum from turning every anatomical similarity into the same argument.",
  "A moving shadow crosses the alcove wall as three wing models begin circling in the next room. Bird, bat, and insect all fly, and the broken museum has stamped their wings HOMOLOGOUS because the function looks similar. Imani closes the vestigial case and carries the dossier forward. The next exhibit will force function and ancestry apart before the word analogous can be earned."
 ]},
'U7-L29':{
 'title':'Three Animals Fly, Yet Flight Does Not Give Their Wings One History',
 'kicker':'Analogous structures share function or form through independent evolution, while homologous components can still exist within a broader analogous comparison.',
 'paragraphs':[
  "The **Analogous Structure Wing** is built around three suspended flight models. On your **left**, a bird wing, a bat wing, and an insect wing sweep through the same arc above a wind tunnel. Directly **ahead**, the center display aligns the broad flight surfaces by function while separate lineage paths remain visible behind them. On your **right**, a split discriminator has one side labeled SHARED ANCESTRY OF STRUCTURE and the other INDEPENDENT EVOLUTION OF SIMILAR FUNCTION. Imani keeps the MORPHOLOGY tab open and removes the museum's old HOMOLOGOUS label from the center.",
  "The left display makes the temptation obvious. All three structures contribute to flight. Similar function alone, however, does not establish that the flight structure was inherited from a recent common ancestor. The lineage paths show that similar selective pressures can produce similar functional solutions in distantly related groups. Only after that independent history is visible does Imani name **Analogous structures**. Analogous structures perform similar functions or have similar forms because of independent evolution under similar selective pressures, not because the feature was inherited from a recent common ancestor.",
  "The bird and bat models then rotate to expose their internal forelimb skeletons. Corresponding tetrapod bones align in the familiar pattern from the Homology Morphology Hall. Imani leaves those correspondence lines intact. Bird and bat forelimbs share homologous skeletal elements because of common ancestry, even though powered flight evolved independently. The same organisms can therefore participate in different comparisons at different structural levels. She traces the comparison boundary with her pointer. The skeletal framework answers an ancestry question. The broad flight surface answers a functional convergence question. Keeping the level of comparison visible prevents one correct statement from being used to erase another.",
  "The insect model remains on the left side of the functional comparison without being forced into a tetrapod bone pattern it does not possess. Imani has you trace the evidence claim carefully. Broad flight function across bird, bat, and insect can illustrate analogy. The bird and bat forelimb skeletons can simultaneously illustrate homology. The inference depends on exactly which feature is being compared.",
  "The right discriminator now accepts the dossier card. FUNCTIONAL SIMILARITY THROUGH INDEPENDENT EVOLUTION goes under ANALOGY. SHARED UNDERLYING FORELIMB PATTERN THROUGH COMMON ANCESTRY remains under HOMOLOGY. The two claims stand beside each other, which makes them easier to remember than a vocabulary rule detached from the structures themselves.",
  "A thin blue light appears along the floor and leads toward a laboratory. The museum has another comparison problem waiting there. Two organisms have sequences that look similar, yet the scanner has been matching unrelated stretches simply because some letters happen to repeat. Imani closes the morphology tab. The next room will compare DNA and proteins only after homologous regions and positions are aligned."
 ]},
'U7-L30':{
 'title':'The Sequence Scanner Will Not Compare Letters Until the Molecules Are Aligned',
 'kicker':'Molecular similarity supports common ancestry when homologous DNA or protein sequences are compared appropriately.',
 'paragraphs':[
  "The **Molecular Evidence Scanner** glows blue behind a glass laboratory wall. On your **left**, aligned DNA sequences from several labeled taxa run horizontally with nucleotide positions marked above them. Directly **ahead**, the center scanner highlights matching and differing positions only within homologous regions. On your **right**, corresponding protein sequences from the same comparison set are aligned by amino-acid position. Imani opens the MOLECULES tab of the dossier and deletes a previous museum score that had compared unrelated sequence fragments simply because they shared a few letters.",
  "The left sequences enter the scanner without losing their taxon labels or positional alignment. Shared nucleotides light up one color and differences another. Imani then repeats the process with homologous protein sequences on the right. This establishes **Sequence similarity as evidence**. Comparisons of DNA nucleotide sequences and protein amino-acid sequences provide evidence for evolution and common ancestry. The comparison is meaningful because the sequences represent corresponding molecules or regions.",
  "The scanner next calculates relative similarity across the same set of lineages. A pair with more sequence similarity often supports a more recent common ancestor than a pair with substantially more differences when the comparison is appropriate. Imani names **Molecular homology**. Similarity in DNA or protein sequences can indicate common ancestry, with greater sequence similarity often supporting a more recent common ancestor when compared appropriately.",
  "She pauses the machine before it prints an exact divergence date. Sequence similarity alone does not automatically provide a precise time since divergence. Molecular-clock reasoning requires additional assumptions, calibration, and model choices that are outside this simple evidence comparison. The dossier therefore records RELATIVE RELATEDNESS SUPPORT and COMMON ANCESTRY SUPPORT without inventing a numerical date. Imani also prevents the scanner from comparing one gene in one taxon with an unrelated gene in another. Homology of the sequence region has to be established first. Only then can counts of similarities and differences contribute meaningfully to the evolutionary inference.",
  "Imani places the molecular card beside the earlier morphology card on the convergence table preview. Morphological homology and molecular homology are separate evidence streams. When they support compatible relationships, the evolutionary inference becomes stronger. The museum is finally beginning to behave like an argument built from independent evidence rather than a collection of objects that all receive the same label.",
  "The optional recall light fades, leaving only the aligned sequence positions visible. When the lab door opens again, the floor path leads into a cell archive. Membrane-bound organelles glow on the left. Linear chromosomes and intron-containing genes are displayed on the right. These features were learned in earlier units for their cellular roles. Here they will be reactivated for a different evidentiary question, what conserved cellular architecture can support about common ancestry among eukaryotes."
 ]},
'U7-L31':{
 'title':'The Cell Archive Turns Familiar Features Into Ancestry Evidence',
 'kicker':'Shared eukaryotic cellular and molecular features can support common ancestry when their conservation across lineages is made explicit.',
 'paragraphs':[
  "The **Eukaryotic Common-Ancestry Archive** resembles a circular library built from giant transparent cell models. On your **left**, membrane-bound organelles glow inside cells from several eukaryotic lineages. Directly **ahead**, the center registry overlays a shared cellular plan across the specimens. On your **right**, long linear chromosome models hang beside gene diagrams containing introns. Imani opens the CONSERVED CELL FEATURES tab and keeps the familiar structures exactly what they were in earlier units. Their biological identities do not change simply because the question now concerns ancestry.",
  "She begins with the left archive. Multiple eukaryotic lineages contain membrane-bound organelles. The dossier records **Membrane-bound organelles as common-ancestry evidence**. Shared membrane-bound organelles contribute structural evidence for common ancestry of eukaryotes. The organelles still carry their normal cellular functions. The new step is evidentiary interpretation across lineages.",
  "On the right, Imani lowers the chromosome models. **Linear chromosomes as common-ancestry evidence** records that linear chromosomes are a conserved feature supporting common ancestry of eukaryotes. Beside them, gene diagrams open to show introns within transcribed regions. **Introns as common-ancestry evidence** identifies genes containing introns as a conserved molecular feature that contributes evidence for common ancestry of eukaryotes.",
  "The center registry now places those features across multiple eukaryotic lineages rather than assigning them to a single derived group. Imani records **Conserved eukaryotic cellular features**. Membrane-bound organelles, linear chromosomes, and intron-containing genes are among conserved features used as evidence for common ancestry of eukaryotes. The word *among* remains visible because these are examples of conserved features, not an exhaustive list of everything eukaryotes share. She then reopens one cell model and one gene diagram from earlier units. Their original functions remain unchanged. What changes here is the comparison across lineages. A familiar cellular feature becomes evolutionary evidence only when its conserved distribution is placed into an ancestry argument.",
  "With the three evidence cards aligned, the center registry states the broader inference **Common ancestry of eukaryotes**. Shared structural and functional features support common ancestry among eukaryotes. Imani places the statement under an ancestry heading, not under a time estimate. These features support a historical relationship. They do not by themselves tell the museum an exact date for the common ancestor. The dossier therefore preserves two separate fields, one for the conserved feature that was observed and one for the ancestry inference supported by its distribution across lineages.",
  "A wall of the archive turns transparent. Beyond it, screens are updating in real time. A bacterial population changes under antibiotic exposure. A pest population responds across generations to pesticide treatment. Pathogen sequence data shift over time. The museum had treated evolution as something belonging only to fossils and deep history. Imani closes the cell archive and opens the CONTEMPORARY CHANGE tab. The next room will show that evolutionary mechanisms continue to operate in populations now."
 ]},
'U7-L32':{
 'title':'The Museum’s Live Feed Shows Evolution Still Running',
 'kicker':'Genomic change, fossil change, resistance, and pathogen evolution connect historical evidence with evolutionary mechanisms acting in contemporary populations.',
 'paragraphs':[
  "The **Continuing Evolution Monitor** fills an entire dark room with moving timelines. On your **left**, a genomic and fossil feed scrolls from deep time toward the present, keeping dated fossil changes and genomic changes in separate tracks. Directly **ahead**, the center population monitor updates only when heritable population change is documented across generations. On your **right**, three live panels follow bacterial resistance, pesticide resistance, and pathogen change. Imani opens the CONTEMPORARY CHANGE tab and disables the museum's old message that evolution ended once modern species appeared.",
  "The left feed first connects old and new records. Change observed through the fossil record provides **Continuity of fossil change**, evidence that evolution has continued through time. Alongside it, measured changes in genomes over generations establish **Genomic change over time**. Changes in genomes over generations provide evidence of continuing evolution. The two tracks differ in material and timescale, yet both document change through time.",
  "The center monitor names the broad relationship **Evolution continues**. All living lineages have evolutionary histories and populations continue to evolve when evolutionary mechanisms change allele frequencies. The screen uses populations and generations, never an individual transforming itself because conditions changed. Historical evolution and contemporary evolution belong to one continuing process.",
  "On the right, an antibiotic panel begins with both susceptible and heritable resistant bacterial variants already present or arising by mutation. Antibiotic exposure changes reproductive success. Resistant variants leave more descendants under treatment, and resistance-associated alleles increase across generations. Imani records **Evolution of resistance** and the specific case **Antibiotic resistance evolution**. Resistance can evolve when heritable variants differ in reproductive success under treatment. The bacteria do not decide to become resistant because the drug appears. The monitor keeps generation labels visible so a surviving individual is not confused with an evolving population. The evidence of evolution is the changing representation of heritable variants across descendant generations under the treatment environment.",
  "The pesticide panel repeats the causal logic with a pest population. Pesticides can impose selection that increases frequencies of heritable resistance variants. The dossier records **Pesticide resistance evolution** without treating the chemical as a creator of needed mutations. The pathogen panel then tracks heritable changes that alter transmissibility, host interactions, drug resistance, or other traits. **Pathogen evolution and emerging disease** and **Emerging-disease evolution** connect population evolution to changing disease patterns without implying that every new outbreak has one evolutionary cause.",
  "The monitor stabilizes, yet the final museum alarm remains yellow. One case file shows a population that has recovered in number after a severe decline while its genetic variation remains low. Another population contains many more inherited variants. Both are about to face the same novel environmental pressure. Imani carries the evidence dossier into a glass conservatory. The final question is whether genetic diversity changes the probability that a population contains variants capable of tolerating a new pressure."
 ]},
'U7-L33':{
 'title':'Two Populations Face the Same New Pressure With Different Genetic Options',
 'kicker':'Genetic diversity influences population resilience by changing the probability that some individuals already carry phenotypes that tolerate a new environmental pressure.',
 'paragraphs':[
  "The **Genetic-Diversity Resilience Conservatory** is divided into three connected glass enclosures. On your **left**, a low-diversity population contains many individuals yet only a narrow range of inherited variants. Directly **ahead**, the center conservatory holds a comparison population with a broader distribution of genetic variation. On your **right**, a novel environmental-pressure chamber contains several phenotype response lanes and a California condor case file. Imani opens the final POPULATION DIVERSITY tab and applies the same pressure to both populations at the same time.",
  "The left population has few heritable alternatives. When the environment changes, a large fraction of individuals perform poorly because the population contains few variants that tolerate the new condition. Imani records **Low diversity increases vulnerability**. Populations with little genetic diversity are more vulnerable to decline or extinction when environments change. The claim concerns probability and population capacity. A low-diversity population is not guaranteed to disappear under every environmental change.",
  "The center population contains more genetic variation before the pressure arrives. Some variants confer no special advantage under the old conditions. Under the new pressure, at least one inherited phenotype performs better and leaves more descendants. Imani records **Diversity increases probability of tolerant variants**. Genetically diverse populations are more likely to include individuals whose phenotypes tolerate a novel environmental pressure. Greater variation increases the chance that useful variants are already present.",
  "The right chamber then changes the environment again. The variant that performed best under the first pressure loses its advantage and another phenotype performs better. This makes **Fitness effects depend on environment** visible. An allele that is advantageous under one set of conditions can be neutral or harmful under another because selective pressures differ. The conservatory therefore refuses the idea that more genetic variation means every allele is beneficial. Variation supplies alternatives whose fitness effects depend on context.",
  "Imani places the California condor case file beneath the low-diversity enclosure. The severe historical decline of California condors illustrates a demographic bottleneck that reduced genetic diversity. Even after conservation increased population numbers, lost variation could not be restored simply by counting more individuals. The case is filed as **California condor genetic bottleneck** and supports the broader relationship **Genetic variation affects population resilience**. The amount and distribution of genetic variation influence population dynamics and the capacity to respond to environmental change.",
  "The final optional recall light turns off every label except the two population enclosures and the changing environmental-pressure chamber. When the labels return, Imani carries the completed dossier back to the center convergence table. TIME contains fossils and dating evidence. MORPHOLOGY contains homology, vestigial evidence, embryology, and analogy. MOLECULES contains sequence comparisons. CONSERVED CELL FEATURES contains eukaryotic architecture. CONTEMPORARY CHANGE contains genomic, resistance, and pathogen records. POPULATION DIVERSITY contains resilience evidence. The museum alarm finally turns green because each line of evidence now has a specific job and several independent lines can converge on the same evolutionary explanation without becoming interchangeable."
 ]},
}

CHECKPOINTS={'U7-L27','U7-L30','U7-L33'}

def clean_prose(text):
    return text.replace(' — ', '. ').replace('—','-').replace(': ','. ')

def word_count(paragraphs):
    return len(re.findall(r"\b[\w’′'-]+\b",' '.join(paragraphs)))

def zone_objs(lid):
    return [{'position':p,'label':label,'symbol':symbol,'description':description} for p,label,symbol,description in ZONES[lid]]

def cast_for(lid):
    items=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    for position,label,symbol,description in ZONES[lid]:
        items.append({'name':label,'kind':'scientific evidence zone or comparison apparatus','visual':description,'job':f"Remain fixed on the learner's {position} and carry the {position}-side evidentiary role required by the locked F3 geometry."})
    items.append({'name':'Expanding evidence dossier','kind':'journey continuity object','visual':'a transparent case file with fixed tabs for time, morphology, molecules, conserved cell features, contemporary change, and population diversity; every card has an observation field and an inference field','job':'keeps evidence types separate until independent lines legitimately converge on the same evolutionary explanation'})
    items.append({'name':'Observation column','kind':'evidence recorder','visual':'the left half of every dossier card, reserved for what was actually measured, seen, dated, aligned, or compared','job':'prevents an inference from being mistaken for a raw observation'})
    items.append({'name':'Inference column','kind':'evidence recorder','visual':'the right half of every dossier card, reserved for the specific evolutionary claim supported by the observation','job':'forces every specimen to state what it can support and what it cannot establish by itself'})
    return items

def beats_for(lid):
    b=B[lid]
    terms={t['knowledge_id']:t for t in b['term_introductions']}
    scene_hint={
      'U7-L25':'the dossier tabs separating fossil, geographic, morphological, molecular, and quantitative observations before the convergence table combines compatible inferences',
      'U7-L26':'the fossil remaining inside older and younger strata while an isotope-appropriate clock is chosen and the carbon-14 timeline stops at recent organic remains',
      'U7-L27':'the aligned forelimb structures preserving the same underlying inherited pattern while current functions differ',
      'U7-L28':'the embryo-development display beside a reduced inherited structure whose present-day role can remain modified rather than absent',
      'U7-L29':'the bird, bat, and insect flight comparison separated into independent flight function and homologous bird-bat forelimb ancestry',
      'U7-L30':'the homologous DNA and protein sequences aligned by taxon and position before molecular similarity is interpreted',
      'U7-L31':'the conserved membrane-bound organelles, linear chromosomes, and intron-containing genes displayed across multiple eukaryotic lineages',
      'U7-L32':'the population-level live feeds showing genomic change, resistance, and pathogen evolution across generations',
      'U7-L33':'the low-diversity and high-diversity populations facing the same new pressure while fitness changes with environmental context',
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
for i,lid in enumerate(J3['route']):
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
 'palace_id':'U7-J3','unit_id':'unit-7','palace_name':'Evolution Evidence Museum',
 'story_title':'The Museum That Had Evidence Everywhere and an Argument Nowhere',
 'tagline':'A museum has filled one giant case with fossils, skeletons, DNA, cell features, resistance records, and population histories, then labeled all of it proof. Sort every observation into the evidence job it can actually perform until independent lines finally converge on a defensible evolutionary explanation.',
 'guide':GUIDE,
 'premise':'The Evolution Evidence Museum has collapsed every exhibit into one vague category called proof of evolution. Fossil ages are being inferred without appropriate clocks, homologous and analogous structures are mixed together, sequence similarity is being overinterpreted, vestigial structures are labeled functionless, contemporary resistance is treated as intentional adaptation, and population diversity is treated as universally beneficial. Dr. Imani Vale seals the museum and opens one evidence dossier with fixed tabs and separate observation and inference columns.',
 'mission':'Carry the same dossier through nine permanent locations. Add fossil, morphological, molecular, conserved-cellular, contemporary, and population-diversity evidence only after the observation and the inference it supports are both visible. Keep time evidence separate from ancestry evidence, homology separate from analogy, present-day evolution population-level, and genetic diversity probabilistic and environment dependent.',
 'finale':'The museum clears its audit when every dossier tab contains a specific observation, an appropriately limited inference, and a record of which independent evidence streams converge. The completed case file can support evolutionary explanations without pretending that every line of evidence answers the same question.',
 'estimated_minutes':30,'scene_count':9,'checkpoint_count':len(CHECKPOINTS),
 'student_release':'DEVELOPER_PREVIEW_F4C','preview_release':True,'narrative_design':'U7-F4C-NARRATIVE-1.0',
 'learner_rule':'Read or listen while keeping the museum route and the six evidence-dossier tabs stable in your mind. Each exact term appears after its diagnostic observation or comparison is visible. The dossier records observation and inference separately so evidence types remain distinct even when several converge.',
 'route_orientation':'The museum is one continuous clockwise evidence route. Begin at the convergence atrium, descend into fossil time, cross morphology and developmental evidence, separate analogy from homology, enter the molecular scanner and eukaryotic archive, then finish at the live-evolution monitor and genetic-diversity conservatory before returning the completed dossier to the atrium.',
 'route':ROUTE,'scenes':scenes,
 'source_brief_lock':'LOCKED_F3','scientific_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2',
 'frozen_prior_journey_lock':'LOCKED_F4B_J1_J2'
}

(U7/'journeys'/'U7-J3.json').write_text(json.dumps(journey,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

summary={
 'schema':'memory-palace-v2-unit7-f4c-journeys-1.0','unit_id':'unit-7','stage':'F4C','student_release':False,'preview_release':True,
 'journey_count':3,'scene_count':33,'checkpoint_count':J1['checkpoint_count']+J2['checkpoint_count']+len(CHECKPOINTS),
 'guided_journeys':[
   {k:J1[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']},
   {k:J2[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']},
   {k:journey[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']}
 ]
}
(U7/'journeys-f4c.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

status={
 'unit_id':'unit-7','number':7,'title':'Natural Selection','status':'F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','pipeline_stage':'F4C_JOURNEY3_NARRATIVE',
 'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3',
 'narrative_lock':'LOCKED_F4C_J1_J3','student_release':False,'preview_release':True,
 'journey_count':3,'scene_count':33,'memory_objects':0,'application_challenges':0,
 'canonical_records':215,'architecture_journeys':6,'architecture_bundles':23,'architecture_loci':55,'scene_briefs':55,'palace_managed_records':174,
 'challenge_lab_records':16,'scope_guard_records':25,'exact_name_review_targets':94,'confusable_sets':33,'optional_first_exposure_recalls':18,
 'f4a_journey':'U7-J1','f4a_scene_count':10,'f4b_journey':'U7-J2','f4b_scene_count':14,
 'f4c_journey':'U7-J3','f4c_scene_count':9,'f4c_knowledge_records':35,'f4c_exact_name_targets':11,'f4c_optional_recalls':len(CHECKPOINTS),
 'next_required_output':'F4D polished narrative for Journey 4 only after Journeys 1 through 3 remain frozen and all F1-F4C gates continue to pass.'
}
(U7/'status-f4c.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(U7/'status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'
course=read(cp)
u=next(x for x in course['units'] if x['unit_id']=='unit-7')
u.update({
 'status':'F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','journey_count':3,'scene_count':33,'student_release':False,'preview_release':True,
 'source_status':'AUDITED_F1_ARCHITECTURE_F2_BRIEFS_F3_NARRATIVE_F4A_F4B_F4C','narrative_lock':'LOCKED_F4C_J1_J3','narrative_journeys':3,
 'pipeline_stage':'F4C_JOURNEY3_NARRATIVE'
})
cp.write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

doc=['# Unit 7 F4C · Journey 3 Narrative','','## The Museum That Had Evidence Everywhere and an Argument Nowhere','',journey['tagline'],'',
     '### Physical route','', ' → '.join(x['locus'] for x in ROUTE),'',
     '### Continuity rule','',CONTINUITY,'']
for s in scenes:
    doc += [f"## {s['scene_index']+1}. {s['locus']} · {s['title']}",'',f"*{s['scene_kicker']}*",'']
    doc += s['story_paragraphs']+['']
    if s['checkpoint']:
        doc += ['**Optional Quick Recall**','',s['checkpoint_prompt'],'']
(ROOT/'docs'/'UNIT7_F4C_JOURNEY3_STORY.md').write_text('\n'.join(doc),encoding='utf-8')

# Freeze F4B and earlier Journey narrative evidence.
f4b=read(U7/'content-lock-f4b.json')
prior_files={}
for rel,meta in f4b.get('f4a_journey1_protection',{}).items():
    prior_files[rel]=meta
for rel in [
    'content/ap-biology/unit-7/journeys/U7-J1.json',
    'content/ap-biology/unit-7/journeys/U7-J2.json',
    'content/ap-biology/unit-7/journeys-f4b.json',
    'content/ap-biology/unit-7/status-f4b.json',
    'content/ap-biology/unit-7/content-lock-f4b.json',
    'content/ap-biology/unit-7/f4b-release-manifest.json',
    'docs/UNIT7_F4B_JOURNEY2_STORY.md',
    'docs/UNIT7_F4B_RELEASE.md',
    'docs/UNIT7_F4B_QA.md',
    'docs/UNIT7_F4B_PACKAGE_QA.md',
]:
    rp=ROOT/rel
    if rp.exists():
        prior_files[rel]={'bytes':rp.stat().st_size,'sha256':sha(rp)}

locked_rel=['journeys/U7-J3.json','journeys-f4c.json','status-f4c.json']
lock_files={rel:{'bytes':(U7/rel).stat().st_size,'sha256':sha(U7/rel)} for rel in locked_rel}
lock={
 'schema':'memory-palace-v2-unit7-f4c-lock-1.0','unit_id':'unit-7','lock_status':'LOCKED_F4C_J1_J3','student_release':False,'preview_release':True,
 'protected_prior_locks':['content-lock-f1.json','content-lock-f2.json','content-lock-f3.json','content-lock-f4a.json','content-lock-f4b.json'],
 'f4a_f4b_prior_narrative_protection':prior_files,
 'journey_id':'U7-J3','scene_count':9,'knowledge_record_count':35,'exact_name_target_count':11,'checkpoint_count':len(CHECKPOINTS),
 'files':lock_files,
 'rule':'Journeys 1 and 2 remain frozen byte-for-byte. Journey 3 polished prose may not change after F4C without a new explicit narrative version. F1 science, F2 classification/geometry, and F3 scene briefs remain authoritative.'
}
(U7/'content-lock-f4c.json').write_text(json.dumps(lock,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

release={
 'schema':'memory-palace-v2-unit7-f4c-release-1.0','generated_utc':'2026-09-08T14:20:00+00:00','unit_id':'unit-7',
 'release_status':'F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','student_release':False,'preview_release':True,
 'completed_journeys':['U7-J1','U7-J2','U7-J3'],'journeys':3,'scenes':33,
 'f4c_journey_id':'U7-J3','f4c_scenes':9,'f4c_knowledge_records':35,'f4c_exact_name_targets':11,'f4c_optional_first_exposure_recalls':len(CHECKPOINTS),
 'canonical_records':215,'permanent_loci_architecture':55,'scene_briefs':55,'memory_objects':0,'application_challenges':0,
 'scientific_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','narrative_lock':'LOCKED_F4C_J1_J3',
 'next_stage':'F4D Journey 4 polished narrative after F4C regression'
}
(U7/'f4c-release-manifest.json').write_text(json.dumps(release,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

print(json.dumps({
 'journey':'U7-J3','scenes':9,'knowledge_records':35,'exact_name_targets':11,'checkpoints':len(CHECKPOINTS),
 'words':sum(s['narrative_word_count'] for s in scenes),
 'mean_words':round(sum(s['narrative_word_count'] for s in scenes)/9,1),
 'min_words':min(s['narrative_word_count'] for s in scenes),
 'max_words':max(s['narrative_word_count'] for s in scenes),
},indent=2))
