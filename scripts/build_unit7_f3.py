from __future__ import annotations
import json, hashlib
from pathlib import Path
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content'/'ap-biology'/'unit-7'
BRIEFS=U7/'briefs'; BRIEFS.mkdir(parents=True,exist_ok=True)
GEN='2026-09-08T06:45:00+00:00'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,obj): Path(p).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

src=read(U7/'source/canonical-unit7-f1.json')
canon={r['knowledge_id']:r for r in src['canonical_catalog']}
f2=read(U7/'architecture/palace-architecture-f2.json')
cls=read(U7/'architecture/learning-classification-f2.json')
class_by_id={r['knowledge_id']:r for r in cls['records']}
flag_by_id={f['review_flag_id']:f for f in src['review_flags']}

unit_guide={
 'name':'Dr. Imani Vale',
 'role':'evolutionary-systems curator who accompanies the learner through all six Unit 7 journeys',
 'visual_identity':'charcoal field jacket, pale-green specimen gloves, a transparent population ledger that can display phenotype counts and allele frequencies, and a slim brass pointer used only to indicate real structures, branches, barriers, or evidence',
 'behavior_rule':'Imani establishes the left/center/right geography first, keeps populations and evidence physically identifiable across time, changes only one evolutionary variable or relationship at a time, and names a scientific term only after the defining pattern or mechanism can be seen.',
 'continuity_rule':'Imani is a guide and recorder, never a substitute for a biological population, allele, fossil, phylogenetic branch, reproductive barrier, or chemical system. Real biological entities retain conventional scientific roles and causal relationships.'
}

journey_specs={
'U7-J1':dict(
 premise='The Selection and Fitness Observatory contains many apparent adaptations, but none of them can be interpreted correctly until population-level change, heritable variation, environmental pressure, and differential reproductive success are separated from need, intention, acclimation, and individual change.',
 mission='Track one population ledger through changing conditions while phenotype counts, offspring contributions, molecular variants, selection distributions, mate success, and human-directed breeding are compared without ever letting a single individual stand in for population evolution.',
 stakes='Natural selection becomes misleading when learners equate fitness with strength, treat mutations as directed by need, confuse survival with reproductive success, or say individual organisms evolve. The brief keeps population, generation, environment, phenotype, and offspring contribution visible at every step.',
 continuity_object='one transparent population ledger showing the same census frame across generations: phenotype categories, offspring contributed to the next generation, and a small allele-frequency strip remain visible even when the biological example changes.',
 recurring_scientific_cast=['transparent population ledger with generation counters','real organisms or phenotype distributions under comparison','offspring/reproductive-success and environmental-pressure readouts'],
 opening_image='The observatory opens with a population display full of visible variation but no explanation for why frequencies change. Historical evidence, environmental pressures, offspring counters, and a molecular case are present but deliberately unresolved.',
 ending_payoff='The learner can reconstruct natural, sexual, and artificial selection as different routes to differential reproduction, distinguish adaptation from acclimation, and explain why fitness depends on reproductive success in a particular environment rather than strength or intention.',
 tone='population-centered, evidence-led, nonteleological, visually comparative'),
'U7-J2':dict(
 premise='A network of island populations begins with the same allele inventory, but chance events, new mutations, migration, and selection-related assumptions threaten to change the gene pools in different ways. The Hardy-Weinberg station can serve as a baseline only if its conditions and quantities remain distinct.',
 mission='Move the same color-coded allele tokens through mutation, drift, bottleneck, founder, and gene-flow events, then carry their counts into a Hardy-Weinberg null-model station without confusing allele frequencies, genotype frequencies, p/q symbols, or observed versus expected values.',
 stakes='Population genetics is often memorized as disconnected vocabulary and equations. If the same allele copies are not visibly counted through every demographic event, students can confuse drift with selection, founder effect with migration, or Hardy-Weinberg algebra with direct observed genotype frequencies.',
 continuity_object='two transparent island gene-pool tanks containing exactly 100 color-coded allele copies each, plus a persistent population-size marker and generation label; tokens move, disappear, or are added only when the specified mechanism permits it.',
 recurring_scientific_cast=['two island gene-pool tanks with persistent colored allele tokens','population-size and migration barriers','Hardy-Weinberg baseline boards using the same counted allele copies'],
 opening_image='Two neighboring island tanks begin with known allele counts and identical labels. A mutation tray, storm bottleneck, founder ferry, pollen bridge, and equilibrium control room are visible downstream, but no token is allowed to move until the mechanism at that station is identified.',
 ending_payoff='The learner can trace exactly why allele frequencies changed or stayed stable, distinguish chance sampling from migration and selection, and connect p, q, p², 2pq, and q² to a two-allele locus while keeping direct genotype counts separate from equilibrium expectations.',
 tone='quantitative, demographic, token-tracking, mechanism-first'),
'U7-J3':dict(
 premise='The Evolution Evidence Museum contains fossils, anatomical models, DNA sequences, cell features, resistance records, and population-diversity cases, but each exhibit supports evolution in a different way and must not be treated as interchangeable evidence.',
 mission='Carry one evidence dossier from deep time through morphology, molecular comparison, conserved eukaryotic features, present-day evolution, and genetic-diversity consequences, adding each line of evidence only after its diagnostic relationship has been shown.',
 stakes='Students can list fossils, homology, DNA, and resistance without explaining what each actually supports. The route must distinguish age evidence from ancestry evidence, homology from analogy, molecular similarity from morphological similarity, and contemporary selection from historical reconstruction.',
 continuity_object='one expanding evidence dossier with separate tabs for time, morphology, molecules, conserved cellular features, contemporary change, and population diversity; evidence is never moved between tabs unless the inference truly applies.',
 recurring_scientific_cast=['evidence dossier with fixed category tabs','fossil/anatomical/molecular specimens','ancestry, time, and population-change interpretation panels'],
 opening_image='The museum receives an unlabeled case file containing fossils, forelimbs, sequence strips, cell diagrams, resistance data, and a condor pedigree. The file is useless until each specimen is placed in the evidence category it can legitimately support.',
 ending_payoff='The evidence dossier now separates time, common ancestry, convergence, molecular similarity, continuing evolution, and population resilience while showing how independent evidence streams converge on evolutionary explanations.',
 tone='forensic, comparative, evidence-specific, synthesis-oriented'),
'U7-J4':dict(
 premise='The Phylogeny Navigation Archive receives a set of taxa and character evidence, but the branching map is only a hypothesis. Nodes, roots, sister relationships, outgroups, character states, and molecular evidence must be interpreted without turning living tips into ancestors or treating one inference method as absolute truth.',
 mission='Keep one six-taxon character-and-sequence dossier fixed while constructing and interpreting a rooted phylogenetic map, identifying branching relationships, mapping derived characters, using an outgroup, comparing evidence sources, and evaluating grouping/parsimony claims.',
 stakes='Tree diagrams are visually deceptive. Learners often read left-to-right order as progress, call early-branching taxa primitive, confuse sister taxa with nearby tips, or treat branch rotation as a changed relationship. The route keeps node identity and ancestry logic stable as the display rotates or evidence is added.',
 continuity_object='one six-taxon dossier with fixed taxon names, a character-state matrix, short DNA/protein sequence strips, and a rooted tree whose node IDs stay constant even when branches rotate or evidence is updated.',
 recurring_scientific_cast=['fixed six-taxon dossier','rooted tree with persistent node labels','character-state and molecular-evidence panels'],
 opening_image='A navigation table displays six taxa, several candidate branchings, and a character matrix. The archive will not accept a route until every node means a common ancestor, every sister relationship is tied to one immediate node, and character evidence is interpreted relative to an outgroup.',
 ending_payoff='The learner can read a tree by ancestry rather than tip position, use shared derived characters and an outgroup, distinguish phylogeny from phylogenetics and taxonomy, and explain why the best-supported tree remains a revisable hypothesis.',
 tone='map-like, branch-stable, inference-focused, anti-misreading'),
'U7-J5':dict(
 premise='One ancestral population spreads across an archipelago, but new species can form only if gene flow is sufficiently reduced and reproductive barriers develop. Geographic separation, mating barriers, hybrid outcomes, and later diversification must stay causally ordered.',
 mission='Track two color-banded descendant populations from shared ancestry through allopatric or sympatric divergence, prezygotic and postzygotic barriers, then outward to evolutionary tempo, divergence, adaptive radiation, convergence, and extinction without assuming every difference automatically creates a species.',
 stakes='Speciation vocabulary is easy to memorize without causal understanding. The route must make reduced gene flow and reproductive isolation the central mechanism, keep allopatric versus sympatric geography distinct, and separate barriers before fertilization from consequences after fertilization.',
 continuity_object='one ancestral population represented by two interbreeding color bands that later separate into lineage A and lineage B; a visible gene-flow meter and mating/fertility outcome panel follow the same two lineages through every barrier.',
 recurring_scientific_cast=['lineage A and lineage B from one ancestral population','gene-flow meter and geographic context','mating, fertilization, hybrid-viability, and fertility outcome panels'],
 opening_image='Both color bands begin in one freely interbreeding population. The archipelago contains a physical barrier, an overlapping habitat, mating gates, a hybrid ward, and a long-timescale overlook, but none can count as speciation until gene flow and reproductive compatibility are evaluated.',
 ending_payoff='The learner can explain how reproductive isolation creates species boundaries, classify major pre- and postzygotic barriers, distinguish allopatric from sympatric pathways, and place divergence, radiation, convergence, stasis, and extinction on longer evolutionary timescales.',
 tone='lineage-tracking, barrier-centered, causal, long-timescale'),
'U7-J6':dict(
 premise='The Origins of Life Geochemistry Lab contains geological dates, atmospheric models, organic molecules, a historical spark apparatus, RNA chemistry, and an endosymbiosis exhibit, but these represent different stages and strengths of evidence and cannot be collapsed into one story of “life being created.”',
 mission='Move one numbered evidence tray from Earth-formation constraints through prebiotic chemistry, historical atmosphere hypotheses, Miller-Urey evidence, RNA-world requirements, and finally a clearly separated later endosymbiosis display.',
 stakes='Origins-of-life explanations become inaccurate when early Earth is given abundant oxygen, Miller-Urey is said to create life, historical atmosphere assumptions are treated as settled fact, or endosymbiosis is confused with the first origin of cells. The route keeps evidence, hypothesis, and later evolutionary events separated.',
 continuity_object='one numbered evidence tray with five slots: geological timing, atmospheric/geochemical conditions, small organic molecules, replicating/catalytic RNA, and later eukaryotic endosymbiosis. Each slot can be filled only by evidence appropriate to that stage.',
 recurring_scientific_cast=['numbered evidence tray','early-Earth atmosphere/geochemistry and organic molecules','RNA replication/catalysis models and later endosymbiosis boundary'],
 opening_image='A sealed evidence tray sits beside a timeline, gas chamber, spark apparatus, RNA station, and organelle display. Every station claims relevance to life’s history, but the tray accepts each claim only if its timing and evidence level are correct.',
 ending_payoff='The learner can distinguish geological constraints, abiotic synthesis of small organics, historical Miller-Urey evidence, RNA-world requirements, and the later endosymbiotic origin of mitochondria/chloroplasts without claiming any single experiment demonstrated the complete origin of life.',
 tone='chronological, geochemical, evidence-qualified, boundary-conscious')
}

# Three precise science-bearing actions per locus. These are briefing instructions, not polished story prose.
A={
'U7-L01':['Place Darwin/voyage context and Galápagos biogeography on the evidence side without using them as a complete mechanism of evolution.','Compare mainland and island forms so geographic pattern supports descent with modification and diversification from ancestral populations.','Close by separating historical evidence from the modern population-genetic definition that will govern the rest of the unit.'],
'U7-L02':['Hold one individual constant while advancing the population ledger across several generations.','Change frequencies only in the population columns, never by visually transforming one organism during its lifetime.','Name natural selection only after the population-level mechanism and generational timescale are explicit.'],
'U7-L03':['Display several heritable phenotypes in the same population before any environmental pressure is applied.','Connect a heritable phenotype to underlying molecular/genetic variation when relevant, without implying every visible difference is heritable.','Identify adaptation only for a heritable trait that increases reproductive success in the specified environment.'],
'U7-L04':['Increase offspring production beyond the resource limit while keeping food/space finite.','Track which phenotype classes contribute different numbers of surviving reproductive offspring under competition.','Use the unequal offspring contribution—not strength alone—as the mechanism that can change trait frequencies.'],
'U7-L05':['Place two phenotype classes on the same reproductive-success scale under one defined environment.','Measure relative offspring contribution to the next generation and then change the environment while keeping the phenotypes identifiable.','Show that the fitness ranking can change with environment, making fitness relative and context dependent.'],
'U7-L06':['Change one abiotic or biotic environmental factor while keeping the starting population composition visible.','Contrast a reversible within-lifetime response with a heritable difference that changes reproductive output across generations.','Require the learner to classify acclimation and evolutionary change by inheritance and generational frequency change, not by whether the organism looks different.'],
'U7-L07':['Place a molecular variant on the left and trace its physiological/phenotypic consequence before discussing reproductive success.','Use the sickle-cell case to compare heterozygous and homozygous states in a malaria-endemic environment without calling sickle-cell disease protective.','Connect molecular variation to environment-dependent fitness only after the genotype/phenotype distinctions are visible.'],
'U7-L08':['Start with the same bell-shaped heritable trait distribution in all three panels.','Apply three different relative-fitness patterns: favor one extreme, favor the intermediate, or favor both extremes.','Update the next-generation distributions so directional, stabilizing, and disruptive selection are distinguished by distributional consequence.'],
'U7-L09':['Hold survival cost and mating success on separate readouts for the same heritable trait.','Increase mate acquisition through mate choice or competition and calculate the net reproductive consequence.','Name sexual selection only after increased mating/reproductive success is visible, avoiding the claim that the trait is biologically useless.'],
'U7-L10':['Place human-selected breeding pairs on one side and environmentally filtered reproduction on the other.','Track trait-frequency change across generations in both systems while identifying who or what determines reproductive opportunity.','Compare artificial and natural selection without saying either causes an individual organism to evolve.'],
'U7-L11':['Define one population boundary and place every allele copy from its reproducing members into the central gene pool.','Compare a locus with two alleles against a locus where one allele has frequency 1.0.','Use the number and distribution of alleles to distinguish gene pool, fixed allele, and genetic diversity.'],
'U7-L12':['Count the same locus at generation 1 and generation 2 using identical allele symbols.','Convert allele-copy counts to frequencies for both generations without invoking a specific mechanism yet.','Classify a frequency change across generations as population evolution/microevolution while keeping mechanism determination for later loci.'],
'U7-L13':['Introduce one new allele by mutation without changing it because the organism “needs” the variant.','Show that the new allele can be beneficial, neutral, or harmful depending on molecular consequence and environment.','Increase calendar-time opportunities by shortening generation time while explicitly keeping per-replication mutation probability conceptually separate.'],
'U7-L14':['Place mutation occurrence and random sampling on the chance-driven side while keeping natural selection physically outside this turntable.','Allow chance events to change which allele copies are represented in the next generation.','Name random evolutionary processes after the allele-frequency outcome is visible, preserving the distinction from nonrandom differential reproductive success.'],
'U7-L15':['Shrink population size while keeping the allele tokens individually visible.','Randomly sample which alleles reproduce and compare the proportional frequency shift with the same sampling event in a large population.','Show that drift can reduce diversity and drive divergence by chance without consistently increasing adaptation.'],
'U7-L16':['Begin with a large gene pool, then pass only a small chance sample through a severe population-size bottleneck.','Allow the population to recover numerically while preserving the reduced/nonrepresentative allele set of the survivors.','Use the black robin and trout cases as context after the sampling mechanism is already clear.'],
'U7-L17':['Select a small subset of source-population individuals by chance and move only their allele copies onto a new island.','Build the new colony from that subset and compare its starting allele frequencies with the source population.','Use the founder-effect label only after the nonrepresentative founding sample is visible; keep the Amish example as context, not mutation generation.'],
'U7-L18':['Keep two gene pools separated, then move fertile individuals or gametes across the bridge.','Add/remove the actual allele copies and recalculate frequencies in both populations.','Show that continued gene flow tends to reduce genetic differences between populations and can oppose divergence.'],
'U7-L19':['Freeze a two-allele locus and record its current allele frequencies before any model assumptions are imposed.','Generate the genotype frequencies expected under an idealized non-evolving Hardy-Weinberg null model.','Use deviations as evidence to investigate assumptions; do not equate every genotype-frequency deviation with allele-frequency evolution.'],
'U7-L20':['Place the five conditions in fixed spatial controls: large population, no migration, no mutation, random mating, and no natural selection.','Toggle one condition at a time while holding the other four visibly constant.','Emphasize that the model is locus-specific and that nonrandom mating alone can alter genotype frequencies without necessarily changing allele frequencies.'],
'U7-L21':['Count all allele copies at one two-allele locus and define p and q as allele frequencies.','Keep dominance labels off the p/q symbols and contrast allele frequency with genotype frequency on separate panels.','Use p + q = 1 only after the two-allele condition and complete allele accounting are visible.'],
'U7-L22':['Use the same p and q from the prior locus and construct expected mating combinations under Hardy-Weinberg assumptions.','Map expected genotype frequencies to p², 2pq, and q² without re-labeling p as dominant or q as recessive.','Verify that p² + 2pq + q² = 1 and distinguish the equation from directly observed genotype proportions.'],
'U7-L23':['Load observed AA, Aa, and aa genotype counts into separate bins.','Count copies of the chosen allele as 2 per relevant homozygote plus 1 per heterozygote, then divide by 2N.','Compute the second allele by direct counting or 1 minus the first frequency; prohibit square-rooting arbitrary observed homozygote frequencies.'],
'U7-L24':['Place observed genotype frequencies and Hardy-Weinberg expected frequencies on separate sides.','Compare them while identifying which model assumptions might plausibly be violated.','Allow recessive-phenotype frequency to stand in for q² only when phenotype-genotype mapping and Hardy-Weinberg assumptions are explicitly justified.'],
'U7-L25':['Sort the evidence dossier into fossil/geological, biogeographic, morphological, molecular/genetic, and quantitative tabs.','Ask what evolutionary claim each evidence type can support before combining them.','Show stronger inference when independent evidence streams converge on the same ancestry or change-over-time explanation.'],
'U7-L26':['Place fossils in stratigraphic/geologic context before assigning ages.','Use an isotope whose half-life/timescale fits the material or surrounding rocks, separating relative context from radiometric estimates.','Restrict carbon-14 to relatively recent organic remains rather than treating it as a universal fossil clock.'],
'U7-L27':['Compare anatomical structures with the same underlying inherited pattern but different current functions.','Use comparative morphology to identify shared structural correspondence before naming homology.','Connect homologous structures to common ancestry without requiring present-day function to be similar.'],
'U7-L28':['Show an embryological feature shared by related lineages and a reduced adult structure inherited from an ancestor.','Compare ancestral function with current reduced or modified function instead of erasing current function.','Use vestigial structure and embryological homology as distinct forms of ancestry evidence.'],
'U7-L29':['Compare structures that perform similar functions in distantly related lineages.','Separate independently evolved wing function from the homologous tetrapod forelimb skeleton shared by birds and bats.','Name analogous structures only for similarity produced by independent evolution/convergent selective pressures, not recent shared ancestry of the feature.'],
'U7-L30':['Align homologous DNA or protein sequences from multiple lineages.','Count/locate sequence similarities and differences while controlling which molecules/regions are being compared.','Use molecular similarity as evidence of common ancestry and relative relatedness, without claiming sequence similarity alone proves an exact divergence time.'],
'U7-L31':['Reactivate membrane-bound organelles, linear chromosomes, and intron-containing genes from prior units.','Place the conserved features across multiple eukaryotic lineages rather than assigning them to one derived species.','Interpret the shared cellular/molecular architecture as evidence supporting common ancestry of eukaryotes.'],
'U7-L32':['Place genomic changes, fossil changes, resistance data, and pathogen-change records on a shared present-to-past monitor.','Trace resistance evolution through heritable variants and differential reproduction under treatment, not through organisms intentionally adapting.','Use contemporary genomic/pathogen/resistance changes as evidence that evolutionary mechanisms continue to operate.'],
'U7-L33':['Compare a genetically low-diversity population with a more diverse population under the same novel environmental pressure.','Track the probability that at least some individuals carry tolerant phenotypes, while avoiding the claim that every variant is beneficial.','Use the condor bottleneck as context for why demographic recovery may not immediately restore lost genetic diversity.'],
'U7-L34':['Place taxonomy, systematics, phylogenetics, and phylogeny on separate labeled work surfaces.','Use the same evidence dossier to infer one branching hypothesis, then add new evidence that could revise it.','Name the phylogeny as the evolutionary relationship/history hypothesis and phylogenetics as the methods used to infer/test it.'],
'U7-L35':['Display one cladogram with branch lengths carrying no scale and one phylogenetic tree calibrated to time or amount of change.','Rotate branches around a node without changing the underlying ancestry relationships.','Require the learner to interpret only the scale information actually encoded and not read left-to-right tip order as evolutionary progress.'],
'U7-L36':['Fix the root at the ancestral lineage and label internal nodes with persistent IDs.','Trace descendant lineages from each node to define clades and locate the most recent common ancestor represented by a node.','Keep extant tips as descendants, never as the ancestors of other extant taxa.'],
'U7-L37':['Choose one internal node and identify its two immediate descendant lineages as sister taxa/clades.','Contrast that pair with an extant lineage that branches closer to the root.','Describe the early-branching lineage without calling it primitive, less evolved, or the ancestor of the other living taxa.'],
'U7-L38':['Start with an ancestral character state inferred for the relevant comparison.','Map a character-state change onto the branch where the derived state first appears.','Identify a synapomorphy/shared derived character only when descendants inherit that derived state from their common ancestor.'],
'U7-L39':['Place a taxon outside the ingroup as the outgroup without making it an ancestor of the ingroup.','Compare character states between outgroup and ingroup to infer which states are ancestral versus derived.','Use the outgroup as a reference for polarity, then carry the inferred character states back onto the ingroup tree.'],
'U7-L40':['Construct candidate phylogenies from morphological/fossil evidence and then add DNA/protein sequence evidence.','Compare which relationships are supported or contradicted when different evidence sources are considered.','Give molecular evidence appropriate weight while keeping every resulting tree a revisable hypothesis rather than a final fact.'],
'U7-L41':['Draw one group containing an ancestor and all descendants, one omitting descendants, and one combining taxa without their most recent common ancestor.','Use parsimony to compare the number of character-state changes required by candidate trees.','Keep monophyletic/paraphyletic/polyphyletic and parsimony as teacher enrichment and avoid claiming parsimony is the only or infallible phylogenetic method.'],
'U7-L42':['Begin with one freely interbreeding population and a high gene-flow meter.','Reduce successful gene exchange while monitoring whether members can still produce viable, fertile offspring.','Use reproductive isolation as the causal boundary for speciation and apply the biological species concept only where sexual reproduction makes it meaningful.'],
'U7-L43':['Split one population with a geographic barrier while keeping lineage A and B visibly derived from the same ancestral population.','Reduce gene flow and allow genetic differences to accumulate independently.','Name allopatric speciation only when geographic separation is part of the pathway and reproductive isolation eventually develops.'],
'U7-L44':['Keep lineage A and B in geographic overlap while introducing a mechanism that reduces mating/gene flow within the shared area.','Allow reproductive isolation to strengthen without inserting a physical geographic barrier.','Name sympatric speciation from the overlap condition while avoiding the claim that niche exploitation is the only mechanism.'],
'U7-L45':['Place the mating/fertilization sequence in causal order from encounter through gamete fusion.','Block the process before zygote formation and contrast that timing with the untouched postzygotic ward.','Use prezygotic barrier only when mating or fertilization is prevented.'],
'U7-L46':['Keep lineages reproductively capable in principle but place them in different habitats or breeding times.','Reduce encounters by spatial/habitat use in one panel and by reproductive timing in the other.','Distinguish habitat isolation from temporal isolation by what prevents potential mates from encountering each other.'],
'U7-L47':['Run the same two lineages through courtship-signal mismatch, structural incompatibility, and gamete-recognition/fusion failure.','Stop at the exact stage where each barrier acts while preserving the same lineage identities.','Name behavioral, mechanical, and gametic isolation only after the diagnostic failure point is visible.'],
'U7-L48':['Allow fertilization to occur so a zygote forms before any barrier is diagnosed.','Compare failure to develop/survive, survival with reduced fertility, and later-generation decline after an initially viable fertile F1.','Distinguish reduced hybrid viability, reduced hybrid fertility, and hybrid breakdown by timing and outcome; do not reduce all hybrid sterility to chromosome-number mismatch.'],
'U7-L49':['Place one lineage on a continuous gradual-change timeline and another with long stasis interrupted by relatively rapid change.','Keep the total time axis visible so “rapid” remains relative to geological timescales.','Distinguish gradualism, punctuated equilibrium, and stasis without treating one tempo as the universal evolutionary pattern.'],
'U7-L50':['Branch related lineages into different environments to show divergence and possible adaptive radiation.','Independently expose distant lineages to similar selective pressures to show convergence and analogous traits.','Add extinction as lineage loss and keep divergence separate from guaranteed speciation; reproductive isolation remains necessary for species formation.'],
'U7-L51':['Place Earth formation near 4.6 billion years ago, later habitability near 3.9 billion years ago, and earliest fossil evidence near 3.5 billion years ago on one timeline.','Use geological evidence to constrain when different origin-of-life models are plausible.','Avoid assigning all earliest evidence definitively to cyanobacteria; keep the claim at the evidence level supported by the lock.'],
'U7-L52':['Set the early atmosphere/geochemistry with little free molecular oxygen and visible non-oxygen energy sources such as lightning, UV, volcanism, or gradients.','Generate small organic molecules abiotically under plausible prebiotic conditions and separately add extraterrestrial organics as a possible source.','Keep monomer formation separate from polymerization, compartments, replication, and life itself.'],
'U7-L53':['Display the Oparin-Haldane strongly reducing atmosphere as a historical hypothesis, not a settled reconstruction.','Compare that hypothesis with modern evidence for an early atmosphere containing substantial nitrogen/carbon dioxide and little oxygen, allowing local reducing environments.','Use the historical model to set up the question Miller tested without presenting it as the only plausible early-Earth chemistry.'],
'U7-L54':['Run the historical Miller-Urey apparatus with simulated gases, water cycling, and an energy source.','Collect amino acids and other small organic compounds in the product trap.','State precisely that the experiment demonstrated abiotic synthesis of small organics under simulated conditions, not creation of macromolecules, cells, or life.'],
'U7-L55':['Place complementary RNA strands and catalytic RNA in the origin-of-life slot before any genetically encoded protein catalyst is required.','Show templated copying through complementary base pairing and connect replication to genetic continuity across generations of replicating systems.','Move mitochondria/chloroplast endosymbiosis to a clearly later eukaryotic-evolution panel so it cannot be mistaken for the origin of the first life.']
}

# Brief-depth supplements keep terse action instructions explicit enough for F4 writers.
step_supplements={
 ('U7-L04',0):' Keep the original phenotype counts visible so the resource shortage, rather than an unexplained trait change, is the only new condition.',
 ('U7-L08',0):' Mark the same mean and range in each copy so later changes can be attributed to different selection patterns rather than different starting populations.',
 ('U7-L09',0):' Keep offspring number as the final common currency so survival and mating effects can be compared through reproductive success.',
 ('U7-L11',1):' Keep total allele-copy number visible so fixation means frequency 1.0 at that locus, not simply that one phenotype looks common.',
 ('U7-L12',0):' Keep population size and sampling method constant enough that the learner can compare frequencies across generations rather than raw counts alone.',
 ('U7-L14',1):' Keep the environmental fitness display unchanged during this step so the frequency shift cannot be misread as natural selection.',
 ('U7-L15',0):' Preserve the pre-drift allele frequencies beside the smaller sample so proportional changes remain visible rather than being hidden by raw population size.',
 ('U7-L18',1):' Keep migrant/gamete origin visible so the frequency change is tied to movement between populations, not mutation or random sampling within one population.',
 ('U7-L20',1):' Record which assumption was changed and which population quantity changes afterward so violations are not treated as interchangeable.',
 ('U7-L21',0):' Show the total number of allele copies as 2N for diploids so the symbols are grounded in counted alleles rather than dominance labels.',
 ('U7-L23',0):' Keep the observed sample size N and the resulting total of 2N allele copies visible before any allele-frequency calculation begins.',
 ('U7-L24',1):' Keep observed allele frequencies on screen while inspecting assumptions so genotype-pattern differences are not automatically called allele-frequency evolution.',
 ('U7-L25',1):' Require a one-sentence inference for each tab so evidence type and evolutionary claim remain connected rather than becoming a vocabulary list.',
 ('U7-L26',0):' Keep older and younger strata visible around the specimen so relative geological context remains distinct from any numerical date estimate.',
 ('U7-L29',0):' Keep lineage relationships visible beside the functional similarity so similar function is not automatically mistaken for recent common ancestry of that structure.',
 ('U7-L30',0):' Keep taxon names and sequence positions aligned so similarity is compared across homologous regions rather than unrelated stretches of sequence.',
 ('U7-L35',1):' Keep node labels fixed during rotation so the learner can verify that ancestry relationships remain unchanged despite a different drawing orientation.',
 ('U7-L36',0):' Keep the same node IDs on every branch so later references to clades and common ancestors remain spatially stable.',
 ('U7-L36',2):' Keep every tip at the same present-time boundary unless the diagram explicitly encodes time, preventing living taxa from being mistaken for ancestors.',
 ('U7-L37',1):' Keep the sister pair highlighted at their shared node while the early-branching lineage remains connected to a different, deeper node.',
 ('U7-L38',0):' Keep the outgroup/reference state available so “ancestral” is defined relative to the comparison rather than assumed from appearance.',
 ('U7-L38',1):' Mark the exact branch where the change occurs so descendants can inherit the derived state from a specified common ancestor.',
 ('U7-L42',0):' Keep mating compatibility and viable-fertile offspring outcomes visible so species boundaries are evaluated biologically rather than by appearance alone.',
 ('U7-L43',1):' Keep the geographic barrier visible throughout divergence so reduced migration remains the defining allopatric condition.',
 ('U7-L45',2):' Stop the sequence before zygote formation and leave the postzygotic ward untouched so timing alone distinguishes this barrier class.',
 ('U7-L48',0):' Keep the successful fertilization event visible so every later failure is unambiguously postzygotic rather than a hidden prezygotic barrier.',
 ('U7-L49',1):' Keep identical time units on both timelines so the learner compares tempo without treating punctuated change as instantaneous.',
 ('U7-L51',1):' Keep the dated markers visible while evaluating hypotheses so a chemical model cannot be placed earlier or later than the evidence permits.',
 ('U7-L54',1):' Keep the product trap chemically labeled as small organic molecules so the result cannot be inflated into polymers, cells, or living systems.'
}
for (lid,idx),extra in step_supplements.items():
    A[lid][idx]+=extra

# Journey briefs need enough detail to guide later prose without becoming story prose themselves.
journey_field_supplements={
 ('U7-J1','continuity_object'):' The ledger never replaces the organisms; it only preserves the same population-level measures while different mechanisms are compared.',
 ('U7-J1','opening_image'):' The learner can see every category at once, which prevents later terminology from floating free of a physical population and measurable reproductive outcomes.',
 ('U7-J2','continuity_object'):' Each token retains its allele identity across every island movement or sampling event so frequency change can always be reconstructed from the actual copies.',
 ('U7-J3','premise'):' The museum therefore treats evidence as a structured argument, not as a collection of objects that all prove the same thing in the same way.',
 ('U7-J3','mission'):' The dossier must record both the observation and the specific inference it supports before another evidence type is added.',
 ('U7-J3','continuity_object'):' The tab structure prevents fossil age, common ancestry, convergence, and contemporary evolution from being collapsed into one undifferentiated “evidence” category.',
 ('U7-J3','opening_image'):' A blank inference column beside every specimen makes clear that identifying the object is only the first step; the learner must say what the evidence means.',
 ('U7-J3','ending_payoff'):' The final case file can be used to defend an evolutionary claim with multiple independent lines of evidence while still stating the limitation of each line.',
 ('U7-J4','continuity_object'):' Because the same node labels survive every branch rotation and evidence update, visual rearrangement cannot masquerade as a change in ancestry.',
 ('U7-J4','ending_payoff'):' The final tree can be redrawn in a different orientation with the same clades, sister relationships, and common ancestors intact.',
 ('U7-J5','continuity_object'):' The two color bands keep their lineage identity after separation so every later barrier and hybrid outcome can be traced back to the same ancestral population.',
 ('U7-J6','mission'):' Every claim must be placed in the correct evidence slot before the route advances, preventing plausible chemistry, experimental results, and later cell evolution from being treated as equivalent events.',
 ('U7-J6','continuity_object'):' The tray preserves chronology as well as evidence type, so later evolutionary events cannot be mistaken for earlier prebiotic stages.',
 ('U7-J6','opening_image'):' The evidence slots are arranged chronologically so a later event cannot be used as an explanation for an earlier stage of life’s origin.'
}
for (jid,field),extra in journey_field_supplements.items():
    journey_specs[jid][field]+=extra

quick={
'U7-L05','U7-L08','U7-L10',
'U7-L15','U7-L18','U7-L20','U7-L22',
'U7-L27','U7-L30','U7-L33',
'U7-L36','U7-L39','U7-L41',
'U7-L43','U7-L47','U7-L48',
'U7-L54','U7-L55'
}

base_constraints=[
 'Begin every scene by orienting the learner to the fixed left/center/right geography before any population, evidence, tree, barrier, or chemical system changes state.',
 'Keep populations explicitly population-level: individuals may survive, reproduce, migrate, or carry variants, but allele/trait-frequency evolution is tracked across generations in populations.',
 'The recurring guide may point, record counts, or activate a display, but must never replace a population, allele, fossil, phylogenetic branch, reproductive barrier, or chemical system.',
 'Introduce an exact scientific term only after the defining pattern, mechanism, comparison, or evidence relationship is visible.',
 'Preserve F1 qualifiers such as can, may, tends to, relative, under Hardy-Weinberg assumptions, and context dependent whenever they are scientifically necessary.',
 'Do not expose PPT, CED, Campbell, source, lock, enrichment, exam-scope, or teacher-management language in student narrative.',
 'Do not convert teacher enrichment or scope guards into mandatory AP recall; F2 retrieval destinations remain authoritative.',
 'Reuse prior-unit concepts only as brief reactivation when F2 says PRIOR_UNIT_REACTIVATION; do not create a second mnemonic identity for the same prerequisite science.',
 'Keep confusable mechanisms physically separated until their diagnostic difference is visible, then compare them directly.',
 'Avoid teleology: environments do not create needed mutations, selection does not try to improve organisms, and fitness is never shorthand for strength.',
 'For Hardy-Weinberg scenes, keep observed allele/genotype counts, model assumptions, p/q symbols, and expected p²/2pq/q² values visually distinct.',
 'For phylogeny scenes, preserve node identity and common-ancestor logic even if branches rotate; never make extant tips ancestors of other extant taxa.',
 'For speciation scenes, keep gene flow and reproductive isolation visible as causal variables; divergence alone does not guarantee speciation.',
 'For origin-of-life scenes, distinguish evidence, historical hypotheses, small-organic synthesis, RNA-world models, and later endosymbiosis by timing and evidentiary claim.',
 'Animate only the relationship required at the locus; avoid decorative absurdity that competes with the evolutionary mechanism or evidence.',
 'Carry one stable continuity object through each journey so route memory and causal/evidentiary memory reinforce one another.',
 'End every scene with a visible unresolved consequence that makes the next locus necessary, not with a narrator merely announcing a new vocabulary term.',
 'Quick Recall is optional during first exposure and appears only at F3-approved candidate loci after the scientific relationship has already been encountered.',
 'Later exact-name retrieval must be possible from the biological role and spatial evidence first; phonological support is an adaptive fallback only.',
 'No polished story sentence may alter F1 science, F2 destination, causal direction, mathematical condition, phylogenetic interpretation, or scope boundary.'
]

# Locus order and confusables.
route_by_j={}
for j in f2['journeys']:
    route_by_j[j['journey_id']]=[lid for b in j['bundles'] for lid in b['loci']]
conf_by_kid=defaultdict(list)
for c in f2['confusable_sets']:
    for kid in c['knowledge_ids']: conf_by_kid[kid].append(c)

# Journey briefs.
journey_briefs=[]
for j in f2['journeys']:
    jid=j['journey_id']; spec=journey_specs[jid]
    journey_briefs.append({
      'journey_id':jid,'f2_working_title':j['working_title'],'topics':j['topics'],
      'premise':spec['premise'],'mission':spec['mission'],'stakes':spec['stakes'],'unit_guide':unit_guide,
      'continuity_object':spec['continuity_object'],'recurring_scientific_cast':spec['recurring_scientific_cast'],
      'opening_image':spec['opening_image'],'ending_payoff':spec['ending_payoff'],'tone':spec['tone'],
      'route':route_by_j[jid],
      'route_rule':'Travel the F2 locus order exactly. A scene may foreshadow the next locus but may not reorder, merge, or skip permanent loci without a new architecture version.',
      'narrative_constraints':base_constraints,
      'status':'JOURNEY_BRIEF_LOCKED_F3_NO_POLISHED_STORY_PROSE'
    })

# Scene briefs.
scene_briefs=[]
for jid in [f'U7-J{i}' for i in range(1,7)]:
    route=route_by_j[jid]; spec=journey_specs[jid]
    for i,lid in enumerate(route):
        l=next(x for x in f2['loci'] if x['locus_id']==lid)
        kids=l['knowledge_ids']; rs=[canon[k] for k in kids]; cs=[class_by_id[k] for k in kids]
        steps=A[lid]; left=l['scene_geometry']['left']; center=l['scene_geometry']['center']; right=l['scene_geometry']['right']
        prev=route[i-1] if i>0 else None; nxt=route[i+1] if i+1<len(route) else None
        entrance='JOURNEY_ENTRANCE' if prev is None else prev
        intros=[]
        for n,(r,c) in enumerate(zip(rs,cs),1):
            intros.append({
              'knowledge_id':r['knowledge_id'],'canonical_term':r['canonical_label'],'canonical_science':r['canonical_verified_statement'],
              'scope_class':r['scope_class'],'exact_name_recall':bool(c['exact_name_recall']),
              'delayed_review_target':bool(c['delayed_review_target']),'reactivation_mode':c['reactivation_mode'],
              'introduction_after_action_step':min(n,len(steps)),
              'insertion_rule':'Name the term only after its defining pattern, relationship, comparison, calculation meaning, or mechanism is visible. Later prose may clarify the locked science but may not weaken, broaden, or contradict the F1 statement.',
              'name_support':c['name_support'],'name_support_rule':'Use the scientific scene, spatial relation, and semantic role first. Only after delayed exact-name failure may F2-approved phonological support be added; a sound cue never replaces the evolutionary mechanism or evidence.',
              'spelling_policy':c['spelling_policy']
            })
        guards=[]; rfids=[]
        for r in rs: rfids.extend(r.get('review_flag_ids',[]))
        for fid in dict.fromkeys(rfids):
            if fid in flag_by_id: guards.append(f"Resolved F1 guard {fid}: {flag_by_id[fid]['resolution']}")
        seen=[]
        for kid in kids:
            for c in conf_by_kid.get(kid,[]):
                if c['set_id'] not in seen:
                    seen.append(c['set_id'])
                    guards.append(f"Discrimination requirement {c['set_id']}: keep {', '.join(c['terms'])} physically and verbally distinct until the diagnostic comparison is complete.")
        reactiv=[]
        for r,c in zip(rs,cs):
            if c['reactivation_mode']=='PRIOR_UNIT_REACTIVATION':
                reactiv.append({'knowledge_id':r['knowledge_id'],'term':r['canonical_label'],'dependency':r.get('cross_unit_dependencies',[]),'rule':'Reactivate the prior representation briefly, then extend it into the Unit 7 evolutionary/evidentiary relationship without assigning a new mnemonic identity.'})
        cast=[
          {'name':left,'position':'left','visual_identity':f"A scientifically conventional representation of {left}, fixed on the learner’s left and kept stable while the diagnostic comparison or mechanism unfolds.",'job_in_scene':'Hold the starting population, reference evidence, ancestral state, assumption, or comparison needed to interpret the center action.','type':'SCIENTIFIC_PART_OR_REFERENCE'},
          {'name':center,'position':'center','visual_identity':f"The largest working model at {l['title']}, centered on {l['micro_anchor']}; the key evolutionary, demographic, inferential, reproductive, or chemical action occurs here.",'job_in_scene':f"Execute the defining action sequence beginning with: {steps[0]}",'type':'SCIENTIFIC_PROCESS_OR_STRUCTURE'},
          {'name':right,'position':'right','visual_identity':f"A scientifically conventional representation of {right}, fixed on the learner’s right and updated only when the central action produces a valid consequence or inference.",'job_in_scene':'Display the changed population, expected/model state, evidence interpretation, descendant relationship, barrier outcome, or chemical product that verifies the mechanism.','type':'SCIENTIFIC_PART_OR_OUTPUT'}
        ]
        primary=canon[l['primary_knowledge_id']]; q=lid in quick
        if nxt:
            next_title=next(x['title'] for x in f2['loci'] if x['locus_id']==nxt)
            trans=(f"Once {l['title']} resolves {primary['canonical_label']}, preserve the same {spec['continuity_object']} and carry forward the specific unresolved consequence produced here into {next_title}. The handoff must be causal: counts, evidence, branch identity, gene-flow state, or chemical evidence from this locus becomes the starting condition for the next locus, while all fixed identities remain reconstructable.")
        else:
            trans=(f"{l['title']} closes {jid}. Freeze the final state of {spec['continuity_object']} and require the learner to reconstruct the complete route in order, explaining how each earlier locus constrained the final population, evidence, phylogeny, species-boundary, or origin-of-life interpretation without inventing an extra permanent locus.")
        scene_briefs.append({
          'scene_brief_id':f'F3-{lid}','locus_id':lid,'journey_id':jid,'bundle_id':l['bundle_id'],
          'scene_title':l['title'],'exact_location':l['title'],'micro_anchor':l['micro_anchor'],'entrance_from':entrance,
          'orientation_sentence':f"Enter {l['title']} and stop at {l['micro_anchor']}. Keep {left} fixed on the left, {center} as the working center, and {right} fixed on the right. The learner should be able to redraw those three positions before any population, evidence, branch, barrier, or chemistry changes state.",
          'spatial_layout':{
            'left':{'anchor':left,'layout_job':'fixed input/reference/ancestral-state/comparison zone'},
            'center':{'anchor':center,'layout_job':'primary science-bearing mechanism or inference zone'},
            'right':{'anchor':right,'layout_job':'fixed consequence/output/descendant/evidence-interpretation zone'}
          },
          'unit_guide':unit_guide,'stable_cast':cast,'continuity_object':spec['continuity_object'],
          'scene_problem':f"Make {primary['canonical_label']} reconstructable from the visible relationship at {l['title']} while preserving the exact F2 geography, F1 qualifiers, population/evidence identities, and the journey continuity object.",
          'science_bearing_action':{
            'before':f"All three zones are visible but scientifically unresolved. {left} supplies the starting state or comparison, {center} has not yet completed the diagnostic action, and {right} cannot yet be interpreted without that action.",
            'trigger':'Imani records the current population/evidence state on the transparent ledger, identifies the one unresolved evolutionary or evidentiary question, and changes only the variable, movement, comparison, or inference needed to make the mechanism observable.',
            'during':steps,
            'after':f"Freeze the resolved state with {left} on the left, {center} in the center, and {right} on the right. The learner must explain what changed or was inferred, which mechanism/evidence justifies it, and how this locus differs from its nearest confusable concept."
          },
          'knowledge_ids':kids,'primary_knowledge_id':l['primary_knowledge_id'],'term_introductions':intros,
          'prior_unit_reactivation':reactiv,
          'visual_spec':{
            'visual_mode':l['visual_mode'],'conventional_scientific_visual_required':True,
            'must_show':[left,center,right,*steps],
            'must_not_show':['source-management labels, textbook references, exam-scope labels, or content-lock language','an anthropomorphic mnemonic character replacing a real population, allele, organism, fossil, branch, reproductive barrier, or chemical species','organisms changing traits because they need them','individual organisms visually transforming to represent population evolution','decorative branch rotations that imply changed ancestry when node relationships are unchanged','Hardy-Weinberg p/q symbols labeled intrinsically as dominant/recessive','Miller-Urey producing cells, macromolecules, or life'],
            'composition_rule':'Preserve the F2 left/center/right geography and conventional evolutionary/biological geometry. Animate only the population change, evidence comparison, branch relationship, reproductive barrier, or chemical process that is scientifically required; keep persistent counts, lineage identities, node IDs, or evidence slots visible when continuity depends on them.'
          },
          'misconception_guards':guards,
          'adaptive_name_support':{
            'first_pass':'Use the visible scientific relationship, mechanism, evidence type, or barrier function first. Do not surface a sound cue during first exposure merely because an evolution term is unfamiliar.',
            'fallback':'After exact-name retrieval failure, use only the record-level F2 name-support classification. Phonological support remains subordinate to the evolutionary mechanism, tree relation, evidence, or reproductive barrier.',
            'spelling':'No Unit 7 F2 target has a mandatory first-pass spelling gate; spelling support remains adaptive.'
          },
          'quick_recall':{
            'enabled':q,
            'candidate_prompt':f"Without looking back, identify or explain {primary['canonical_label']} from the scientific relationship you just reconstructed." if q else None,
            'answer':primary['canonical_verified_statement'] if q else None,
            'timing':'Optional first-exposure pause only after the defining relationship and term have already been encountered.' if q else 'No first-exposure interruption at this locus.',
            'hint_rule':'Point to one fixed spatial anchor, one population/evidence change, or one branch/barrier relationship; do not reveal the answer term before the learner attempts retrieval.' if q else None
          },
          'exit_memory':{
            'one_sentence_model':f"At {l['title']}, reconstruct {left} → {center} → {right} and explain {primary['canonical_label']} using the actual evolutionary mechanism or evidence relationship.",
            'terms_to_carry':[r['canonical_label'] for r in rs if class_by_id[r['knowledge_id']]['delayed_review_target']],
            'redraw_test':f"From memory, place {left} on the left, {center} in the center, and {right} on the right, then redraw or describe the population counts, evidence comparison, tree relation, reproductive barrier, or chemical transformation in causal order."
          },
          'causal_transition':{'to_locus_id':nxt,'transition_logic':trans},
          'story_prose_status':'PROHIBITED_UNTIL_F3_BRIEF_QA_PASS','brief_status':'LOCKED_F3_SCENE_BRIEF'
        })

scene_doc={
 'schema':'memory-palace-v2-unit7-scene-briefs-f3-1.0','generated_utc':GEN,'unit_id':'unit-7',
 'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','student_release':False,
 'design_standard':'Science-bearing briefs only. No polished learner narrative prose at F3.',
 'counts':{'journeys':6,'scene_briefs':55,'palace_managed_records':174,'term_introductions':174,'optional_first_exposure_recalls':len(quick)},
 'scene_briefs':scene_briefs
}
journey_doc={'schema':'memory-palace-v2-unit7-journey-briefs-f3-1.0','generated_utc':GEN,'unit_id':'unit-7','journey_count':6,'student_release':False,'journeys':journey_briefs}
dump(BRIEFS/'scene-briefs-f3.json',scene_doc); dump(BRIEFS/'journey-briefs-f3.json',journey_doc)

status={
 'unit_id':'unit-7','number':7,'title':'Natural Selection','status':'SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED',
 'pipeline_stage':'UNIT7_SCENE_BRIEFS_LOCKED_F3','canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3',
 'student_release':False,'preview_release':False,'journey_count':0,'scene_count':0,'memory_objects':0,'application_challenges':0,
 'canonical_records':215,'architecture_journeys':6,'architecture_bundles':23,'architecture_loci':55,'scene_briefs':55,'palace_managed_records':174,
 'challenge_lab_records':16,'scope_guard_records':25,'exact_name_review_targets':94,'confusable_sets':33,'optional_first_exposure_recalls':len(quick),
 'next_required_output':'F4A polished narrative for Journey 1 only, generated strictly from the locked F3 briefs and subjected to prose-level spatial, scientific, causal, and memorability QA before Journey 2 is written.',
 'next_gate':'UNIT7_F4A_JOURNEY1_POLISHED_NARRATIVE'
}
dump(U7/'status-f3.json',status); dump(U7/'status.json',status)

f3_files=[
 'content/ap-biology/unit-7/briefs/journey-briefs-f3.json','content/ap-biology/unit-7/briefs/scene-briefs-f3.json',
 'content/ap-biology/unit-7/status-f3.json'
]
lock={
 'schema':'memory-palace-v2-unit7-content-lock-f3-1.0','generated_utc':GEN,'unit_id':'unit-7','lock_status':'LOCKED_F3','student_release':False,
 'f1_protected_hashes':{str((U7/p).relative_to(ROOT)):sha(U7/p) for p in ['source/canonical-unit7-f1.json','source/coverage-manifest-f1.json','content-lock-f1.json','f1-release-manifest.json']},
 'f2_protected_hashes':{str((U7/p).relative_to(ROOT)):sha(U7/p) for p in ['architecture/learning-classification-f2.json','architecture/palace-architecture-f2.json','content-lock-f2.json','f2-release-manifest.json','status-f2.json']},
 'files':{rel:{'bytes':(ROOT/rel).stat().st_size,'sha256':sha(ROOT/rel)} for rel in f3_files},
 'policy':'F3 locks science-bearing journey and scene briefs while leaving F1 science and F2 learning architecture unchanged. F4 may write polished story prose only from these briefs and may not alter protected earlier locks.'
}
dump(U7/'content-lock-f3.json',lock)

release={
 'schema':'memory-palace-v2-unit7-f3-release-1.0','generated_utc':GEN,'unit_id':'unit-7','release_status':'SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','student_release':False,
 'canonical_records':215,'palace_managed_records':174,'journey_briefs':6,'scene_briefs':55,'term_introductions':174,'optional_first_exposure_recalls':len(quick),
 'challenge_lab_records':16,'scope_guard_records':25,'exact_name_review_targets':94,'confusable_sets':33,
 'polished_story_files':0,'student_runtime_memory_objects':0,'student_runtime_journeys':0,'student_runtime_scenes':0,
 'next_gate':'F4A Journey 1 only: polished narrative prose from U7-J1 briefs, with spatial clarity, population-level causal continuity, exact-term integration, misconception protection, and science-lock QA.'
}
dump(U7/'f3-release-manifest.json',release)

course_path=ROOT/'content/ap-biology'/'course.json'; course=read(course_path); e=next(u for u in course['units'] if u['unit_id']=='unit-7')
e.update({'status':'SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','pipeline_stage':'UNIT7_SCENE_BRIEFS_LOCKED_F3','journey_count':0,'scene_count':0,'canonical_lock':'LOCKED_F1','source_status':'AUDITED_F1_ARCHITECTURE_F2_BRIEFS_F3','student_release':False,'preview_release':False,'architecture_journeys':6,'architecture_bundles':23,'architecture_loci':55,'architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','scene_briefs':55,'optional_first_exposure_recalls':len(quick)})
dump(course_path,course)

print('UNIT 7 F3 BUILD PASS')
print(scene_doc['counts'])
