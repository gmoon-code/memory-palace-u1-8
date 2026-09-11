from __future__ import annotations
import json, hashlib
from pathlib import Path
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'
BRIEFS=U5/'briefs'; BRIEFS.mkdir(parents=True,exist_ok=True)
GEN='2026-09-04T06:30:00+00:00'

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,obj): Path(p).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

src=load(U5/'source/canonical-unit5-f1.json')
records={r['knowledge_id']:r for r in src['canonical_catalog']}
f2=load(U5/'architecture/palace-architecture-f2.json')
classif=load(U5/'architecture/learning-classification-f2.json')
class_by_id={r['knowledge_id']:r for r in classif['records']}
flag_by_id={f['review_flag_id']:f for f in src['review_flags']}

unit_guide={
 'name':'Dr. Imani Reyes',
 'role':'inheritance-systems geneticist who accompanies the learner through all eight Unit 5 journeys',
 'visual_identity':'deep-green field coat, clear gloves, compact chromosome tablet showing two persistent homolog colors and a narrow gold generation ledger',
 'behavior_rule':'Imani first fixes the learner in a stable location, identifies the real chromosome, allele, cell, or data structures, then changes only the feature needed to reveal the inheritance mechanism before naming the scientific term.',
 'continuity_rule':'Imani is a guide, never a substitute for a scientific term. Chromosomes, chromatids, alleles, gametes, pedigrees, organelles, and statistical quantities retain conventional biological geometry and their real jobs.'
}

journey_specs={
'U5-J1':dict(
 premise='The inheritance registry has mixed genes, chromosomes, homologs, chromatids, chromosome-set number, reproductive routes, and life-cycle transitions into one undifferentiated record, so later meiosis cannot begin with stable identities.',
 mission='Rebuild the registry by tying heredity to genes on chromosomes, separating homologs from sister chromatids, distinguishing diploid from haploid cells, and tracing how reproduction and fertilization move chromosome sets across generations.',
 stakes='If chromosome identity, ploidy, and reproductive transitions are vague here, every later meiosis and Mendelian scene will inherit the same bookkeeping errors.',
 continuity_object='Imani’s gold generation ledger, which keeps four fields visible—chromosome set, cell type, reproductive transition, and generation—and is updated only when the actual biological state changes.',
 recurring_scientific_cast=['tracked homologous chromosome pair','cell/ploidy marker','gene or allele positions on the chromosome pair'],
 opening_image='The registry opens with gene cards, chromosome models, somatic cells, gametes, clone records, and a zygote diagram stacked together under one label, making it impossible to tell what is inherited versus what is merely a stage or cell type.',
 ending_payoff='The registry closes with genes fixed to chromosome loci, homologs distinct from sisters, diploid and haploid states separated, and fertilization restoring a diploid zygote within a life-cycle loop.',
 tone='foundational, archival, exact, chromosome-bookkeeping focused'),
'U5-J2':dict(
 premise='A chromosome transit hall must reduce chromosome-set number and generate haploid products, but its phase gates have lost track of whether homologous chromosomes or sister chromatids are supposed to move.',
 mission='Carry the same color-coded chromosome set continuously through premeiotic replication, prophase-I pairing and crossing over, meiosis-I homolog segregation, the no-replication interval, and meiosis-II sister-chromatid separation.',
 stakes='Meiosis is easily reduced to phase-name memorization. The route must instead make chromosome identity, chromatid state, ploidy, and the two different segregation events physically undeniable.',
 continuity_object='one persistent two-color homolog set on Imani’s chromosome tablet; the same chromosomes are never replaced between stations, and their replication, pairing, recombination, and separation state is updated in place.',
 recurring_scientific_cast=['tracked maternal/paternal homolog pair','sister chromatids and their centromeric connections','spindle poles and chromosome-position markers'],
 opening_image='Two unreplicated homologs enter a long transit hall with two division gates. The hall’s warning panel asks the same question at every station: what is duplicated, what is paired, what separates, and how many chromosome sets remain?',
 ending_payoff='Four haploid products leave the hall after homologs separate in meiosis I and sister chromatids separate in meiosis II, with no DNA replication between the divisions.',
 tone='sequential, structural, mechanically explicit'),
'U5-J3':dict(
 premise='The diversity and error center is misclassifying every unusual gamete as “genetic variation,” even when the outcome arose from chromosome-segregation failure rather than normal recombination and assortment.',
 mission='Synthesize the normal sources of genetic diversity, then contrast correct segregation with nondisjunction, aneuploidy, karyotype evidence, and one trisomy 21 case.',
 stakes='Students must distinguish diversity-producing mechanisms from chromosome-number errors and must not treat a named human condition as the definition of aneuploidy.',
 continuity_object='a chromosome-outcome scanner that first reads allele combinations and then chromosome counts; its mode visibly switches from diversity mode to segregation-integrity mode before error cases begin.',
 recurring_scientific_cast=['gamete or chromosome outcome cards','segregation checkpoint','chromosome-count/karyotype display'],
 opening_image='Normal recombinant products and abnormal chromosome-count products are arriving on the same conveyor, and the center has no reliable way to tell normal variation from segregation error.',
 ending_payoff='The center can now identify crossing over, independent orientation, and random fertilization as diversity sources while tracing nondisjunction to aneuploid chromosome counts and interpreting trisomy 21 as one example.',
 tone='diagnostic, comparison-driven, medically careful'),
'U5-J4':dict(
 premise='A Mendelian breeding estate can produce offspring, yet its records cannot explain how allele states, genotype, phenotype, segregation, cross design, gametes, and Punnett models fit together as one causal inheritance workflow from parental cells to offspring outcomes.',
 mission='Rebuild the inheritance workflow from Mendel’s generation crosses through allele notation, genotype and phenotype, segregation and independent assortment, cross types, gamete generation, Punnett models, and conditional classic ratios.',
 stakes='The learner must understand that Punnett squares summarize possible gamete combinations and that 3:1 or 9:3:3:1 ratios depend on specific assumptions rather than being universal laws of inheritance.',
 continuity_object='one pea-line breeding ledger that follows the same allele symbols from parental plants into gametes and offspring without allowing the notation to become the biological mechanism itself.',
 recurring_scientific_cast=['parental genotype/allele records','gamete outputs','offspring genotype and phenotype records'],
 opening_image='The estate shows pea plants, allele letters, Punnett squares, and phenotype ratios on separate boards, but the boards disagree about where alleles separate and what the grid actually predicts.',
 ending_payoff='The estate links alleles to genotypes, genotypes to phenotypes, Mendelian laws to gamete formation, and Punnett squares to conditional probability outcomes under stated assumptions.',
 tone='inheritance-model, evidence-linked, calculation-aware'),
'U5-J5':dict(
 premise='The probability and pedigree court is issuing inheritance verdicts from isolated clues without distinguishing OR from AND probability or testing multiple models against multigeneration family evidence.',
 mission='Separate inheritance probability from pedigree evidence, apply addition and multiplication rules to the correct event structures, read pedigree notation, and infer inheritance patterns from patterns rather than one visual shortcut.',
 stakes='A pedigree is evidence, not proof from one clue, and probability rules must match whether outcomes are mutually exclusive or independent; otherwise the court can reach confident inheritance conclusions from the wrong event logic or from one misleading family pattern.',
 continuity_object='a two-sided evidence docket: the left page records probability structure, while the right page records pedigree observations and candidate inheritance models.',
 recurring_scientific_cast=['event-probability cards','multigeneration pedigree','candidate inheritance-model cards'],
 opening_image='The court bench contains a pedigree, several probability fractions, and an autosomal-dominant label already stamped on the file before the evidence has been evaluated.',
 ending_payoff='The verdict is based on explicit probability logic and a model comparison that separates observed pedigree patterns from the inheritance mechanism inferred from them.',
 tone='evidence-based, probabilistic, cautious'),
'U5-J6':dict(
 premise='A trait gallery has labeled every pattern as simple dominance, collapsing incomplete dominance, codominance, multiple alleles, gene interactions, chromosome linkage, X inactivation, and environmental effects into one display.',
 mission='Rebuild the gallery by asking what kind of biological mechanism changes the phenotype pattern: allelic interaction, population allele number, interaction among genes, chromosome location, dosage regulation, or environment.',
 stakes='The learner must discriminate similarly named inheritance patterns and avoid turning XX/XY chromosome transmission examples into claims about gender or complete human sex development.',
 continuity_object='one phenotype-comparison frame that always shows genotype/context on the left, the mechanism in the center, and the resulting phenotype pattern on the right.',
 recurring_scientific_cast=['alleles or genotype/context input','mechanism-specific interaction panel','phenotype pattern output'],
 opening_image='Every exhibit ends at a phenotype, yet the mechanisms producing those phenotypes have been erased, leaving intermediate, simultaneous, quantitative, chromosome-linked, mosaic, and environment-dependent patterns indistinguishable.',
 ending_payoff='The gallery separates dominance relationships, multiple alleles, epistasis, polygenic inheritance, pleiotropy, chromosome-linked transmission, X inactivation, and phenotypic plasticity by mechanism.',
 tone='comparative, phenotype-mechanism focused, terminology precise'),
'U5-J7':dict(
 premise='A chromosome mapping rail yard assumes genes assort independently even when they travel close together on the same chromosome, so parental and recombinant offspring are being routed and measured incorrectly.',
 mission='Track linked loci on one chromosome, use crossing over to create recombinant chromatids, classify parental and recombinant outcomes, calculate the meaning of recombination frequency, and convert short-interval data into linkage-map estimates while respecting the 50% ceiling.',
 stakes='Recombination frequency is a genetic mapping measure, not direct physical base-pair distance, and a 50% value cannot distinguish far-apart same-chromosome loci from unlinked loci.',
 continuity_object='one two-locus chromosome railcar whose allele arrangement remains visible as it passes crossover switches, offspring sorting, frequency meters, and the final map board.',
 recurring_scientific_cast=['two tracked loci on one homolog pair','crossover/recombination switch','parental/recombinant outcome bins and map readouts'],
 opening_image='Two allele markers ride the same chromosome railcar, but the yard’s sorting system has placed every offspring into an independent-assortment bin and erased the distance between loci.',
 ending_payoff='The yard now links physical crossover between loci to recombinant classes, recombination percentage, approximate short-interval centimorgan distance, and the observable 50% ceiling.',
 tone='spatial, quantitative, chromosome-linked'),
'U5-J8':dict(
 premise='An inheritance evidence laboratory is treating every trait as nuclear Mendelian inheritance and every mismatch as experimental error, while organelle inheritance, genetic case evidence, and chi-square reasoning are mixed together.',
 mission='Separate nuclear from non-nuclear inheritance, compare animal and plant organelle transmission patterns, use named disorders only as illustrative cases, and finish with a correct chi-square goodness-of-fit workflow from model to statistical decision.',
 stakes='The learner must preserve parent-of-origin qualifications, distinguish illustrative disorders from universal rules, and interpret chi-square as evidence about a null model rather than a probability that the null is true.',
 continuity_object='an evidence tray with three compartments—inheritance route, biological case evidence, and statistical model—so each later conclusion can be traced to the type of evidence that supports it.',
 recurring_scientific_cast=['nuclear versus organelle inheritance routes','case evidence records','observed/expected count and chi-square decision displays'],
 opening_image='The lab has one large Mendelian chromosome diagram covering mitochondrial, chloroplast, disorder-case, and chi-square stations, even though those stations answer fundamentally different inheritance questions.',
 ending_payoff='The laboratory separates organelle-genome transmission from nuclear segregation, keeps disorder cases contextual, and reaches chi-square decisions using observed/expected categorical counts and correct reject/fail-to-reject language.',
 tone='evidence-lab, statistically careful, scope-aware')
}

# Designer-facing mechanics only. These are not student-facing prose.
core={
'U5-L01':[
 'Place heredity and genetics cards on the left, then route one gene card to a specific locus on a chromosome model so “gene,” “chromosome,” “genetics,” and “heredity” cannot collapse into one interchangeable label.',
 'Transmit the chromosome through a reproductive-cell record to a descendant record and keep the allele physically attached to the chromosome, making chromosome behavior the carrier of inherited gene variants.',
 'Open the conserved-information archive only after the gene/chromosome relationship is clear, then connect DNA/RNA information systems and the nearly universal genetic code with deep common ancestry without implying that every sequence is identical across life.'
],
'U5-L02':[
 'Place two homologous chromosomes side by side with the same gene loci aligned but allow different allele labels at corresponding loci; preserve them as chromosome partners rather than replicated copies of one chromosome.',
 'Replicate one homolog on the center bench to produce two sister chromatids and compare that sister relationship directly with the homologous pair, noting that crossing over later can make sisters no longer sequence-identical across exchanged regions.',
 'Arrange a conventional karyotype on the right by paired chromosomes and visible structural features so karyotype is encoded as an organized chromosome display, not as another word for homologous pair.'
],
'U5-L03':[
 'Send a typical diploid somatic-cell model into the left lane with two chromosome sets and mark it 2n; keep homologous partners visible as the basis of the two-set designation.',
 'Move the chromosome-set counter from 2n to n without changing the meaning of chromosome set, then place one-set gametes in the right lane as haploid reproductive cells capable of participating in fertilization.',
 'Use the human example only as a count check—typical somatic cells 46 chromosomes and typical sperm or egg cells 23—while keeping diploid/haploid as general chromosome-set concepts rather than human-specific definitions.'
],
'U5-L04':[
 'Run an asexual route from one genetic source without gamete fusion and produce a clone line whose members are genetically very similar while still allowing mutation or other genetic change to introduce differences over time.',
 'On the comparison fork, keep “clone” tied to common ancestry through asexual processes and remove any absolute “perfectly identical” label so the concept does not require literal genetic identity forever.',
 'Run the sexual route through meiotic processes and gamete fusion to create new allele combinations, while explicitly allowing self-fertilization or other systems so sexual reproduction is not defined as requiring two separate parents.'
],
'U5-L05':[
 'Bring two haploid gametes into the fusion point and combine their chromosome sets during fertilization, showing restoration of diploidy in the standard diploid sexual life-cycle model.',
 'Label the immediate fusion product zygote and carry that diploid cell into the developmental/life-cycle continuation rather than treating fertilization as synonymous with all of reproduction.',
 'Close the loop from one generation to the next while leaving a route marker that sexual life cycles vary among organisms; the fixed relationship is gamete fusion and chromosome-set combination, not one universal organismal life-cycle diagram.'
],
'U5-L06':[
 'Begin with an unreplicated homolog pair and pass each chromosome through S-phase DNA replication so every chromosome now contains two sister chromatids before meiosis I begins.',
 'Keep chromosome number based on centromere-defined chromosomes while DNA content and chromatid number increase, preventing “DNA doubled” from becoming “chromosome-set number doubled.”',
 'Lock the replicated state onto Imani’s persistent chromosome tablet so the same duplicated homologs enter prophase I and can later demonstrate that no second replication occurs between meiosis I and II.'
],
'U5-L07':[
 'Bring replicated homologous chromosomes together and perform synapsis so the two homologs form a four-chromatid tetrad; keep homolog identity and sister relationships visible with persistent colors.',
 'Cross only nonsister chromatids at corresponding regions and exchange matching DNA segments, creating recombinant chromatids while leaving the homolog pair physically associated.',
 'Mark the visible association region as a chiasma after crossover and include spindle formation, chromosome condensation, centrosome movement, and nuclear-envelope breakdown as prophase-I context without letting those features replace the defining homolog-pairing/crossover mechanism.'
],
'U5-L08':[
 'Move each homologous pair to the metaphase plate as a paired unit and attach the pair so homologs face opposite poles while sister chromatids remain joined within each chromosome.',
 'Flip one homologous pair relative to the poles while leaving another pair in its original orientation, demonstrating that each pair can orient independently of the others.',
 'Freeze several possible maternal/paternal orientation combinations so metaphase I is retrieved as paired-homolog alignment plus independent orientation, not as single replicated chromosomes aligning as in metaphase II.'
],
'U5-L09':[
 'Release the homolog-pair connection needed for first-division segregation and move one homolog toward the left pole while its partner homolog moves toward the right pole.',
 'Keep each chromosome visibly duplicated with its two sister chromatids still attached throughout the movement so anaphase I cannot be confused with sister-chromatid separation.',
 'Update the tracked chromosome tablet to show that homologous chromosome sets are now partitioned to opposite poles, setting up haploid daughter cells even though DNA remains duplicated.'
],
'U5-L10':[
 'Complete the first division by placing one homolog from each pair into each daughter-cell region and allow the spindle to break down and nuclear envelopes to reform where appropriate.',
 'Mark both daughter cells haploid because each contains one homologous chromosome set, while keeping every chromosome drawn as two sister chromatids so ploidy is separated from DNA content.',
 'Show cytokinesis as cleavage furrow in an animal-cell example and cell plate in a plant-cell example without making either mechanism part of the definition of haploid state or of telophase I in every organism.'
],
'U5-L11':[
 'Bring the two haploid meiosis-I daughter cells to the interdivision gate with duplicated chromosomes still visible and explicitly block any new S-phase DNA replication event.',
 'Carry the existing sister chromatids unchanged through the gate into meiosis II so the second division begins with replicated chromosomes but only one homologous set per cell.',
 'Use the locked gate as a state transition, not as a new DNA-copying phase: chromosome duplication happened before meiosis I and does not repeat between the two meiotic divisions.'
],
'U5-L12':[
 'Restart spindle organization separately in each haploid cell while the duplicated chromosomes condense or remain visible and new spindle poles gain access to the chromosomes.',
 'Preserve the one-set haploid state during prophase II and keep homologous-pair synapsis absent, since homolog partners were already segregated during meiosis I.',
 'Position the duplicated chromosomes for the next alignment step without crossing over or replicating DNA again, making prophase II a second-division setup rather than a repeat of prophase I.'
],
'U5-L13':[
    "Align individual duplicated chromosomes, not homologous pairs, at the metaphase-II plate inside each haploid cell, keeping each chromosome\'s two sister chromatids visibly joined while homolog partners remain absent after meiosis I.",
 'Orient sister kinetochores toward opposite spindle poles so the mechanical setup predicts sister-chromatid separation at the next station.',
 'Contrast the single-chromosome alignment with the paired-homolog orientation from metaphase I and leave ploidy unchanged at n throughout the metaphase-II alignment.'
],
'U5-L14':[
 'Release sister-chromatid association at the centromeric region and move the two former sisters toward opposite poles within each meiosis-II cell.',
 'As separation occurs, count each former chromatid as an individual chromosome while preserving the haploid chromosome-set state of each future product.',
 'Keep this motion physically distinct from anaphase I: anaphase II separates sister chromatids, whereas the first division separated homologous chromosomes with sisters still joined.'
],
'U5-L15':[
 'Complete telophase II and cytokinesis so the two meiosis-I cells yield four haploid products with unduplicated chromosomes, while preserving possible genetic differences among products.',
 'Place a mitosis outcome beside the meiosis outcome and compare division number, chromosome-set consequences, and genetic similarity without treating either process as universally tied to one organismal purpose.',
 'Close the route by tracing how meiosis reduces chromosome-set number and, together with crossing over and independent orientation, contributes to genetically varied haploid cells.'
],
'U5-L16':[
 'Feed crossover-generated recombinant chromatids into the left route and independent metaphase-I orientations into the center compass as two meiosis-based sources of new allele combinations.',
 'Add random fertilization on the right by allowing different haploid gametes to fuse in many possible combinations, keeping fertilization separate from the chromosome-recombination events that occurred during meiosis.',
 'Compare the three mechanisms side by side so genetic diversity is retrieved as crossing over, independent orientation/assortment, and random fertilization rather than one vague process called “mixing genes.”'
],
'U5-L17':[
 'Run one chromosome set through correct meiosis-I homolog segregation and one through correct meiosis-II sister-chromatid segregation to establish the reference movements at the left checkpoint.',
 'Introduce nondisjunction by failing homologs to separate in meiosis I or failing sisters to separate in meiosis II, then route the resulting gametes into visibly different chromosome-count outcomes.',
 'Keep “nondisjunction” attached to the segregation failure itself and reserve “aneuploidy” for the abnormal chromosome-number state that can result after such errors.'
],
'U5-L18':[
 'Place a normal chromosome complement on the left, then add or remove one individual chromosome at the center comparison so the total no longer contains the normal copy number for that chromosome.',
 'Label the resulting state aneuploidy and distinguish it from whole-set ploidy changes by keeping the other chromosome pairs unchanged.',
 'Transfer the abnormal count into a karyotype-style display on the right so the learner can use chromosome number evidence diagnostically without treating every unusual karyotype as the same condition.'
],
'U5-L19':[
 'Show a paired chromosome-21 reference first, then add a third chromosome-21 copy to create the trisomy 21 karyotype pattern while leaving the other displayed chromosome pairs unchanged.',
 'Connect the three-copy state to aneuploidy and to possible nondisjunction origins without claiming that one visible karyotype explains every phenotypic feature or developmental outcome.',
 'Keep trisomy 21 as one illustrative human chromosome-number case and preserve the broader concepts—nondisjunction and aneuploidy—as the durable AP-relevant mechanisms.'
],
'U5-L20':[
 'Begin with true-breeding parental lines that consistently produce the tracked phenotype under the modeled conditions, and label the initial parental cross as the P generation.',
 'Cross the P generation to produce an F1 generation, then allow F1 individuals to produce the F2 generation so the generational labels remain tied to an actual sequence of crosses.',
 'Use Mendel’s pea experiments as the historical model for discovering predictable inheritance patterns while keeping modern gene/allele language separate from what Mendel directly knew mechanistically.'
],
'U5-L21':[
 'Place two alternative allele forms at the same gene locus and use uppercase/lowercase symbols only as a notation convention for a chosen dominance model, not as a statement that dominant alleles are more common or biologically stronger.',
 'Define dominant and recessive in terms of heterozygous phenotype under complete dominance: the dominant allele affects the heterozygous phenotype while the recessive phenotype is masked in that context.',
 'Keep allele identity, dominance relationship, and letter notation in separate cabinet slots so changing the symbol does not change the biological allele and dominance is not confused with frequency or fitness.'
],
'U5-L22':[
 'Build homozygous and heterozygous genotype examples from allele pairs and label genotype as the allele combination carried at the modeled locus.',
 'Pass each genotype through a complete-dominance phenotype panel so two genotypes can produce the same dominant phenotype while the homozygous recessive genotype produces the recessive phenotype.',
 'Keep phenotype as the observable/measurable trait state produced from genotype in context, and preserve genotype versus phenotype plus homozygous versus heterozygous as separate retrieval contrasts.'
],
'U5-L23':[
 'At the segregation lane, begin with two alleles of one gene in a diploid parent and separate them into different gametes during meiosis, preserving the law of segregation as a one-gene allele-separation principle.',
 'At the independent-assortment lane, track two unlinked genes and vary the orientation/segregation of one gene pair independently of the other during gamete formation.',
 'Keep the independent-assortment rule conditional on genes that are unlinked or effectively assort independently; linked genes belong to a later chromosome-mapping route and must not be forced into a 9:3:3:1 model.'
],
'U5-L24':[
 'Route a one-gene cross into the monohybrid branch, a two-gene cross into the dihybrid branch, and a cross to a homozygous recessive tester into the testcross branch.',
 'Make the decision arbor classify the cross from the genetic question and parental genotypes before any Punnett-square grid is drawn, so “monohybrid” and “dihybrid” are not defined by grid size.',
 'Use the testcross branch to reveal an unknown genotype from offspring evidence under an appropriate dominance model, while keeping testcross as a design strategy rather than a universal inheritance procedure.'
],
'U5-L25':[
 'Start from each parent genotype and first generate the allele combinations that can actually occur in that parent’s gametes under the modeled segregation/assortment conditions.',
 'Place one parent’s possible gametes across the top and the other parent’s down the side of the Punnett grid, then combine one gamete from each parent in each cell.',
 'Read the grid as a probability model of possible offspring genotypes and derive phenotype probabilities only after applying the relevant genotype-to-phenotype rule; the square does not cause inheritance.'
],
'U5-L26':[
 'Build the 3:1 phenotype panel only for the appropriate monohybrid heterozygote cross under complete dominance, large-sample expectation, and the modeled segregation assumptions.',
 'Build the 9:3:3:1 panel only for an appropriate dihybrid heterozygote cross with complete dominance and genes that assort independently, leaving linkage as an explicit disqualifying condition.',
 'Place a large assumption banner between the panels so classic ratios are remembered as conditional predictions, not as universal fingerprints that every observed family or experiment must match exactly.'
],
'U5-L27':[
 'Assign numerical probabilities to alternative gametes produced by a modeled parent and carry those probabilities forward to possible offspring outcomes after fertilization.',
 'Connect inheritance probability to random gamete formation and gamete combination without portraying one predicted probability as a guaranteed outcome in a small family or experiment.',
 'Use a single-gene example to show how probability summarizes repeated random outcomes while remaining compatible with Mendelian segregation of alleles.'
],
'U5-L28':[
 'On the OR lane, identify two mutually exclusive outcomes and add their probabilities to calculate the probability that either one occurs.',
 'On the AND lane, identify independent events that must both occur and multiply their probabilities to calculate the joint outcome.',
 'Force the event-language decision before arithmetic—OR for mutually exclusive alternatives, AND for independent joint events—so the rule follows the logical structure rather than the appearance of the fractions.'
],
'U5-L29':[
 'Build the pedigree key with generation labels, individual symbols, parent/mating lines, and descent lines, then use it to read relationships before inferring any inheritance mechanism.',
 'Mark affected and unaffected phenotypes across several generations and show why an affected parent can be a clue for a simple fully penetrant autosomal-dominant model without making that clue an absolute diagnostic rule.',
 'Add exceptions such as small family size, new variants, penetrance, or uncertain classification to the clue panel so pedigree interpretation remains evidence-based rather than a one-pattern shortcut.'
],
'U5-L30':[
 'Place the observed pedigree or offspring pattern on the left and several candidate models—autosomal, genetically linked, chromosome-linked, and different dominance relationships—on the center verdict table.',
 'Generate predictions from each candidate model and compare those predictions with the observed data, eliminating or weakening models that conflict with the pattern while retaining models that remain plausible.',
 'Issue a supported-model verdict with explicit uncertainty and use Punnett/probability tools only after the model assumptions are specified, preventing a pedigree label from being treated as direct observation of genotype.'
],
'U5-L31':[
 'Start with a simple one-gene complete-dominance expectation, then introduce observed counts that depart from that expected ratio and keep “difference” separate from “statistically meaningful difference.”',
 'Open routes for linkage, altered dominance relationships, multiple alleles, gene interactions, polygenic inheritance, chromosome linkage, and organelle inheritance as different mechanisms that can produce non-simple ratios.',
 'Preserve Mendel’s segregation principle where it still applies to allele separation, showing that “non-Mendelian pattern” does not mean every Mendelian principle has failed.'
],
'U5-L32':[
 'Place an incomplete-dominance heterozygote beside its two homozygotes and show an intermediate phenotype, then reset the frame and show codominance where both allelic effects remain separately distinguishable in the heterozygote.',
 'Add a population-level multiple-allele rack with more than two allele variants while limiting each diploid individual to the allele copies actually present at that locus.',
 'Use the ABO system to combine both ideas correctly: IA and IB are codominant to one another, and each is dominant over i, while the population contains three common alleles.'
],
'U5-L33':[
 'At the epistasis stage, change genotype at one gene and visibly alter or mask the phenotypic expression associated with another gene, preserving interaction between genes as the defining relationship.',
 'At the polygenic branch, combine variation at two or more genes into one phenotypic character and show a quantitative spectrum rather than one single-gene category.',
 'At the pleiotropy branch, start from one gene and send its effect to multiple traits or biological consequences, physically reversing the many-genes-to-one-trait geometry used for polygenic inheritance.'
],
'U5-L34':[
 'Place autosomes on the left and an explicit human XX/XY chromosome-complement inheritance model at the center, then locate example genes on X or Y rather than using “sex-linked” as a synonym for every trait related to sex.',
 'Track eggs as usually X-bearing and sperm as usually X- or Y-bearing in this model while displaying a boundary note that chromosome complement does not by itself define gender or the full biology of human sex development.',
 'Move an X-linked gene and a Y-linked gene through separate inheritance panels so transmission follows the chromosome carrying the gene, while noting that other species use different chromosomal sex-determination systems.'
],
'U5-L35':[
 'Give a modeled XY individual one copy of an X-linked locus and label that single-copy state hemizygous, distinguishing it from homozygous or heterozygous diploid allele pairs.',
 'Track the actual X chromosomes and allele states through gamete formation and offspring combinations instead of using memorized “mother-to-son” shortcuts that ignore parental chromosome complements.',
 'Place Duchenne muscular dystrophy, hemophilia A/B, and common red-green color-vision deficiencies on an enrichment panel as examples of X-linked inheritance without turning those disease names into required AP definitions.'
],
'U5-L36':[
 'Begin with an XX somatic-cell model and make one X chromosome become largely transcriptionally inactive early in development while the other remains active for many X-linked genes.',
 'Condense the largely inactive X into a Barr-body representation and keep “largely inactive” rather than “completely silent,” preserving escape from inactivation as a biological qualification.',
 'Repeat the early random choice across many descendant cell lineages to create a mosaic pattern in which different cell populations retain different active-X origins.'
],
'U5-L37':[
 'Hold genotype constant while changing an environmental condition and allow gene expression or physiology to change so the same genotype produces different phenotypes across conditions.',
 'Use temperature-dependent pigmentation and soil-pH flower color as separate examples of environment-dependent phenotype, making the environmental variable and biological response visible rather than treating the environment as a vague modifier.',
 'Use UV-induced melanin production as a regulated human cellular-response example and close with genotype-by-environment context plus phenotypic plasticity, without implying that all phenotypic variation is environmental.'
],
'U5-L38':[
 'Place two loci close together on the same chromosome and carry their allele combination as one railcar, making co-transmission more common because a crossover is less likely to occur between nearby loci.',
 'Move a second pair of loci farther apart on the same chromosome and increase the opportunity for crossover between them while preserving same-chromosome location.',
 'Use the platform to distinguish “linked” from “always inherited together”: recombination can separate linked alleles, and linkage strength depends on relative position rather than a binary permanent bond.'
],
'U5-L39':[
 'Start with a known parental arrangement of alleles on homologous chromosomes and preserve that phase/arrangement visibly before any crossover occurs.',
 'Introduce a crossover between nonsister chromatids at a position between the two tracked loci and exchange corresponding chromosome segments.',
 'Send the altered chromatids to the recombinant output and keep unaffected chromatids as parental arrangements, linking recombination to new allele combinations without changing which loci exist.'
],
'U5-L40':[
 'Sort offspring or gamete classes whose tracked allele/phenotype combinations match the original parental classes into the parental bins.',
 'Sort classes with new combinations of the tracked alleles/phenotypes into recombinant bins, using the original parental arrangement as the reference rather than assuming the largest classes are parental by definition.',
 'Freeze the classified counts before any percentage is calculated so parental/recombinant classification remains a conceptual step distinct from recombination-frequency arithmetic.'
],
'U5-L41':[
 'Feed the recombinant count and total offspring/gamete count into the recombination-frequency meter and calculate recombinant percentage as the fraction of recombinant outcomes among the total.',
 'Interpret a lower frequency as evidence of tighter genetic linkage under the mapping model and a higher frequency as evidence of greater relative separation up to the observable ceiling.',
 'Keep the meter labeled genetic/recombination distance evidence rather than physical DNA distance, preparing the learner to use the percentage for relative mapping rather than direct base-pair measurement.'
],
'U5-L42':[
 'Place pairwise recombination-frequency marks onto a gene-order board and arrange loci so the ordering is consistent with the observed relative genetic distances.',
 'For short intervals, align about 1% recombination with approximately 1 map unit or centimorgan and display cM as a genetic-map unit, not a physical-length unit.',
 'Add a multiple-crossover warning as interval length grows so recombination percentage is not treated as a perfectly linear ruler across large chromosome distances.'
],
'U5-L43':[
 'Increase separation between two loci and allow recombination frequency to rise toward the observable two-locus ceiling while multiple crossover events increasingly obscure direct detection of every exchange.',
 'Stop the meter at about 50% and show that this outcome is indistinguishable from effective independent assortment in ordinary two-locus offspring data.',
 'Place two alternatives on the right—different chromosomes versus very distant loci on the same chromosome—to encode why a 50% recombination value cannot by itself discriminate those situations.'
],
'U5-L44':[
 'Place nuclear chromosome inheritance on the left as the reference, then move mitochondrial and chloroplast genomes into a separate cytoplasmic/organelle inheritance dock.',
 'Partition organelle copies among daughter cells or gametes independently of nuclear chromosome segregation so their transmission does not have to follow Mendelian nuclear ratios.',
 'Keep “non-nuclear inheritance” tied to genomes in organelles rather than to traits with no DNA basis, and preserve mitochondria/chloroplasts as the main organelle examples.'
],
'U5-L45':[
 'Compare sperm and egg mitochondrial contributions in a typical animal fertilization model and build the zygote mitochondrial pool primarily from mitochondria transmitted through the egg.',
 'Carry mitochondrial-DNA variants through descendants along the typical maternal route while leaving a visible “usually/typically” qualifier rather than an absolute parent-of-origin law.',
 'Keep the rule limited to animal mitochondrial inheritance patterns and avoid transferring it automatically to chloroplasts, all plants, or every exceptional mitochondrial transmission case.'
],
'U5-L46':[
 'Place maternal, paternal, and biparental organelle-transmission possibilities around the plant comparison so the model does not begin from a universal maternal assumption.',
 'Emphasize that many plants transmit mitochondria and chloroplasts predominantly through the ovule rather than pollen, producing often-maternal organelle-DNA inheritance patterns.',
 'Leave the alternative routes visible as biological exceptions and species variation, so “often maternally inherited” is remembered as a common pattern rather than an invariant rule.'
],
'U5-L47':[
 'Index “genetic disorder” broadly as a condition in which genetic variation contributes causally to phenotype, leaving room for single-gene, chromosome, polygenic, environmental, and combined mechanisms.',
 'Replace vague “mutated allele” language with pathogenic variant when evidence supports a disease-contributing DNA variant, while keeping variant pathogenicity as an evidence-based classification.',
 'Use Tay-Sachs and sickle cell disease as two separate teacher-enrichment case files with their correct inheritance/molecular mechanisms, and keep the named disorders illustrative rather than definitions of recessive inheritance.'
],
'U5-L48':[
 'Start with a null inheritance model that supplies expected category proportions and convert those proportions into expected categorical counts for the sample size under consideration.',
 'Place observed categorical counts beside the model and define chi-square goodness-of-fit as a comparison of observed versus model-expected counts, not as a test for continuous measurements directly.',
 'Display χ² = Σ((O−E)²/E) as the statistic used in the workflow and reserve the final hypothesis decision for the later console after degrees of freedom and a significance criterion are supplied.'
],
'U5-L49':[
 'Place the actually recorded categorical frequencies in the observed-count column and calculate the model-based frequencies in the expected-count column from the specified null proportions and total sample size.',
 'For each category, subtract expected from observed, square the difference, divide by expected, and keep that value as the category’s chi-square contribution.',
 'Sum the category contributions into one χ² statistic while keeping observed and expected counts physically distinct so “expected” is never mistaken for another measured data column.'
],
'U5-L50':[
 'Set degrees of freedom to number of outcome categories minus one for the AP fixed-proportion goodness-of-fit setup and use the chosen significance level with df to identify the relevant critical threshold or p-value decision criterion.',
 'Compare the calculated χ² with the critical value or evaluate the p-value relative to alpha, remembering that alpha such as 0.05 is a decision threshold and not a 95% probability that the null hypothesis is true.',
 'Send the conclusion to exactly two outputs: reject the null when evidence exceeds the chosen threshold, or fail to reject the null when it does not; never label the null “accepted” or proven.'
]
}

special_guards={
'U5-L02':['Homologous chromosomes carry corresponding genes at the same loci but may carry different alleles; sister chromatids are replicated copies of one chromosome, not homologs.'],
'U5-L04':['Do not encode asexual descendants as literally identical forever or sexual reproduction as requiring two separate parents.'],
'U5-L07':['Crossing over occurs between nonsister chromatids of homologous chromosomes; tetrad and chiasma are related structures/regions but are not synonyms.'],
'U5-L08':['Metaphase I aligns homologous pairs; metaphase II aligns individual duplicated chromosomes.'],
'U5-L09':['Anaphase I separates homologous chromosomes while sister chromatids remain attached.'],
'U5-L10':['Cells after meiosis I are haploid even though each chromosome is still duplicated; ploidy and DNA content are different quantities.'],
'U5-L11':['No DNA replication occurs between meiosis I and meiosis II.'],
'U5-L14':['Anaphase II separates sister chromatids; do not reuse the homolog-separation action from anaphase I.'],
'U5-L17':['Nondisjunction is the segregation failure; aneuploidy is an abnormal chromosome-number state that can result.'],
'U5-L19':['Trisomy 21 is one illustrative aneuploid outcome and must not become the definition of nondisjunction or aneuploidy.'],
'U5-L21':['Dominant does not mean common, stronger, better, or more evolutionarily successful; letter case is only notation.'],
'U5-L23':['Independent assortment is conditional for unlinked or effectively independently assorting genes; linked genes are handled separately.'],
'U5-L26':['The 3:1 and 9:3:3:1 ratios require specified crosses and assumptions; they are not universal phenotype ratios.'],
'U5-L29':['Pedigree clues are probabilistic/model-based and can be disrupted by penetrance, family size, new variants, or uncertain phenotype classification.'],
'U5-L32':['Incomplete dominance is not blending inheritance; codominance shows distinguishable contributions from both alleles in the heterozygote.'],
'U5-L33':['Pleiotropy is one gene influencing multiple traits/effects; polygenic inheritance is multiple genes contributing to one character; epistasis is interaction between genes.'],
'U5-L34':['XX/XY is an explicit chromosome-complement inheritance model. Do not equate chromosome complement with gender or with the complete biology of sex development.'],
'U5-L35':['Track actual X chromosomes and alleles instead of using oversimplified parent-to-child slogans.'],
'U5-L36':['X inactivation is largely, not absolutely, transcriptionally inactive; some genes can escape inactivation.'],
'U5-L38':['Linked genes tend to be inherited together but can be separated by crossing over.'],
'U5-L42':['Centimorgans are genetic-map units inferred from recombination, not direct physical base-pair distances; large intervals are complicated by multiple crossovers.'],
'U5-L43':['Observed recombination frequency has an approximate 50% ceiling and cannot distinguish unlinked genes from very distant loci on the same chromosome.'],
'U5-L45':['Animal mitochondrial inheritance is usually/typically maternal, not an absolute universal rule.'],
'U5-L46':['Plant organelle inheritance varies among species; often-maternal transmission is not universal.'],
'U5-L47':['Named disorders are illustrative enrichment and should not be used as universal definitions of inheritance categories.'],
'U5-L50':['Use reject or fail to reject the null; alpha is a significance threshold, not the probability that the null hypothesis is true.']
}

recall_prompts={
'U5-L02':('What relationship distinguishes homologous chromosomes from sister chromatids?','Homologs carry corresponding genes at the same loci and may carry different alleles; sister chromatids are replicated copies of one chromosome.'),
'U5-L05':('What process fuses haploid gametes and usually restores diploidy in the standard diploid life cycle?','Fertilization.'),
'U5-L07':('During prophase I, which chromatids exchange corresponding DNA segments during crossing over?','Nonsister chromatids of homologous chromosomes.'),
'U5-L10':('After meiosis I, are the daughter cells haploid or diploid, and are their chromosomes replicated or unreplicated?','Haploid, with chromosomes still replicated as sister chromatids.'),
'U5-L14':('What separates during anaphase II?','Sister chromatids.'),
'U5-L16':('Name the three major sources of genetic diversity emphasized across meiosis and fertilization.','Crossing over, independent orientation/assortment, and random fertilization.'),
'U5-L18':('What term describes an abnormal number of particular chromosomes rather than a change in whole chromosome sets?','Aneuploidy.'),
'U5-L22':('What is the difference between genotype and phenotype?','Genotype is the allele combination; phenotype is the observable/measurable trait state produced from genotype in context.'),
'U5-L23':('Which Mendelian law separates alleles of one gene, and which concerns unlinked genes?','Law of segregation; law of independent assortment.'),
'U5-L28':('Which probability rule is used for mutually exclusive A OR B, and which for independent A AND B?','Addition for OR; multiplication for AND.'),
'U5-L30':('What should pedigree evidence be used to infer?','A supported inheritance model or set of plausible models, not a guaranteed genotype from one visual clue.'),
'U5-L32':('How does codominance differ from incomplete dominance in the heterozygote?','Codominance shows both allelic effects distinctly; incomplete dominance produces an intermediate phenotype.'),
'U5-L34':('What does X-linked inheritance mean?','The gene is located on the X chromosome and its transmission follows the X-chromosome inheritance model.'),
'U5-L39':('What event can create recombinant chromatids for linked loci?','Crossing over between nonsister chromatids at a position between the loci.'),
'U5-L42':('For a short interval, about 1% recombination corresponds to approximately what genetic-map distance?','About 1 centimorgan (1 cM).'),
'U5-L44':('Why can mitochondrial or chloroplast traits show non-Mendelian inheritance?','Their genomes are in cytoplasmic organelles that are transmitted/partitioned independently of nuclear chromosome segregation.'),
'U5-L48':('What kinds of data does the Unit 5 chi-square goodness-of-fit procedure compare?','Observed and expected categorical counts.'),
'U5-L50':('What are the two correct hypothesis-decision phrases in this chi-square workflow?','Reject the null or fail to reject the null.')
}

# Causal handoffs. Final locus in each journey resolves the journey.
transition_reason={
'U5-L01':'Once genes are physically filed on chromosomes, the next unresolved identity problem is whether two similar-looking chromosome structures are homologous partners or replicated sister chromatids, so the ledger moves into the Homolog Pair Vault.',
'U5-L02':'With homologs, sisters, and karyotype display separated, the registry can now count chromosome sets correctly; the tracked cells move to the Ploidy Counter.',
'U5-L03':'Ploidy and cell type are now stable, which makes it possible to compare how chromosome information is transmitted with or without gamete fusion at the Reproduction Fork.',
'U5-L04':'The reproduction routes are distinct, but the sexual route still needs a chromosome-set transition that joins gametes and begins a new generation, leading directly to the Life-Cycle Fusion Loop.',
'U5-L05':'Journey 1 closes after the learner can reconstruct genes on chromosomes, homolog/sister identity, ploidy, reproductive routes, and fertilization as one coherent inheritance registry.',
'U5-L06':'Replication has produced sister chromatids before meiosis I, so the same duplicated homologs can now enter the unique pairing and crossover events of the Prophase I Pairing Chamber.',
'U5-L07':'Synapsis and crossover have altered chromatid combinations while homologs remain paired; the pair must now orient at the Metaphase I Orientation Platform before first-division segregation.',
'U5-L08':'Independent homolog-pair orientation is fixed at the metaphase plate, creating the immediate mechanical setup for homolog separation on the Anaphase I Separation Track.',
'U5-L09':'Homologs have reached opposite poles while sisters remain joined, so the hall can complete the first division and make the chromosome-set/DNA-content distinction explicit at the Telophase I Haploid Landing.',
'U5-L10':'The two cells are haploid but still contain duplicated chromosomes; that exact state explains why the next gate must prohibit another round of DNA replication before meiosis II.',
'U5-L11':'The no-replication gate preserves duplicated chromosomes in haploid cells and releases them into the second-division setup at the Prophase II Restart Bay.',
'U5-L12':'A new spindle is ready around the already-duplicated chromosomes, so individual chromosomes can align for sister separation at the Metaphase II Alignment Rail.',
'U5-L13':'Opposing spindle attachments now position the joined sister chromatids for the second division’s defining segregation event, so the rail opens directly onto the Anaphase II Sister Split where those sisters, not homologous chromosomes, will move apart.',
'U5-L14':'Sister chromatids have separated to opposite poles, allowing telophase II and cytokinesis to generate the terminal products at the Four-Cell Meiosis Exit.',
'U5-L15':'Journey 2 closes only after one persistent chromosome set can be reconstructed through replication, homolog pairing/crossover, homolog segregation, no interdivision replication, sister separation, and four haploid products.',
'U5-L16':'The center now recognizes the three normal diversity sources; Imani switches the scanner from allele-combination mode to chromosome-segregation mode at the Segregation Integrity Gate.',
'U5-L17':'Nondisjunction is now visible as a movement failure, so the next bench examines the chromosome-number state that can result rather than confusing cause with outcome.',
'U5-L18':'The general abnormal chromosome-count concept is clear, allowing one concrete three-copy chromosome-21 pattern to be interpreted at the Trisomy 21 Case Window without replacing the broader mechanism.',
'U5-L19':'Journey 3 closes with normal genetic diversity, segregation integrity, nondisjunction, aneuploidy, karyotype evidence, and trisomy 21 kept in separate causal positions.',
'U5-L20':'Mendel’s generation sequence provides the experimental frame, but the offspring patterns still require precise allele language; the breeding ledger moves to the Allele Notation Cabinet.',
'U5-L21':'Allele identity and dominance notation are now separate, letting the same allele pairs be tested against observable outcomes at the Genotype–Phenotype Bench.',
'U5-L22':'Genotype-to-phenotype logic is stable; the estate can now ask how alleles actually enter different gametes, opening the Mendelian Laws Gate.',
'U5-L23':'Segregation and independent assortment define how allele combinations can reach gametes, so the next decision is what kind of cross is being modeled at the Cross-Type Arbor.',
'U5-L24':'Once the cross type is chosen, the parents must be converted into their possible gametes before offspring combinations can be modeled on the Gamete–Punnett Board.',
'U5-L25':'The Punnett board generates conditional genotype and phenotype probabilities; the balcony ahead tests when the familiar 3:1 and 9:3:3:1 summaries are actually justified.',
'U5-L26':'Journey 4 closes with the entire Mendelian workflow linked from experiment and allele notation through meiosis-based laws, cross design, gametes, Punnett models, and assumption-bound ratios.',
'U5-L27':'Single-event inheritance probabilities are now visible, so the court can distinguish the two logical ways events combine at the Addition–Multiplication Junction.',
'U5-L28':'Probability rules are settled, but family inheritance evidence cannot be reduced to arithmetic alone; the evidence docket moves to the Pedigree Reading Gallery.',
'U5-L29':'The pedigree can now be read accurately, allowing competing inheritance models to be compared against the observed pattern in the Inheritance Pattern Verdict Room.',
'U5-L30':'Journey 5 closes when the learner can separate probability logic, pedigree notation, observed family evidence, and model-based inheritance inference.',
'U5-L31':'The entrance proves that many mechanisms can depart from simple ratios, so the gallery first isolates altered allelic relationships and population allele number in the Dominance Spectrum Studio.',
'U5-L32':'Dominance relationships and multiple alleles are now distinct, revealing a different category of complexity in which genes interact or one gene influences multiple effects at the Gene-Interaction Theater.',
'U5-L33':'Gene-interaction geometry is stable, so the next comparison can move from autosomes to genes carried on X or Y chromosomes without confusing linkage with dominance.',
'U5-L34':'The chromosome-complement model locates X- and Y-linked genes; the rail ahead now follows actual X-chromosome transmission and the special one-copy state called hemizygosity.',
'U5-L35':'X-linked transmission is explicit, allowing dosage regulation across XX somatic-cell lineages to become the central mechanism in the X-Inactivation Mosaic Gallery.',
'U5-L36':'Chromosome-linked dosage patterns are resolved; the final gallery changes environmental context while holding genotype constant at the Phenotypic Plasticity Conservatory.',
'U5-L37':'Journey 6 closes after the learner can explain non-simple phenotype patterns by altered allelic interaction, gene interaction, chromosome location/dosage, or environmental context rather than by one generic “non-Mendelian” label.',
'U5-L38':'The same-chromosome railcar establishes linkage strength as a positional relationship; the next station introduces a physical crossover between the tracked loci at the Recombination Switch.',
'U5-L39':'Crossover has produced altered allele combinations, so offspring/gamete classes can be sorted into parental and recombinant bins before any mapping calculation is attempted.',
'U5-L40':'With classes correctly identified, their counts can enter the Recombination Frequency Meter as a quantitative summary of recombinant outcomes.',
'U5-L41':'The recombination percentage now acts as relative-distance evidence, so the next board can convert short-interval frequencies into gene order and approximate centimorgan spacing.',
'U5-L42':'A linkage map is built, but increasing distance exposes the limit of the two-locus measure; the rail ends at the Fifty-Percent Ceiling Gate.',
'U5-L43':'Journey 7 closes with linkage, crossover, parental/recombinant classification, recombination frequency, map units, multiple-crossover limitations, and the 50% ceiling connected to one chromosome route.',
'U5-L44':'The evidence tray now separates organelle genomes from nuclear chromosomes, allowing a typical animal parent-of-origin pattern to be examined at the Mitochondrial Inheritance Route.',
'U5-L45':'The animal mitochondrial pattern is qualified as usually maternal; the next route tests why plant organelle inheritance needs an even broader set of parental possibilities.',
'U5-L46':'Organelle transmission variability is established, so the lab can move from inheritance route to disease-related genetic evidence without pretending named disorders define the inheritance categories.',
'U5-L47':'The case archive clarifies genetic disorder and pathogenic variant language; the remaining evidence compartment is statistical, beginning with the Chi-Square Model Bench.',
'U5-L48':'The null model, categorical counts, and chi-square purpose are fixed; observed and expected counts can now be processed category by category at the Observed–Expected Calculation Station.',
'U5-L49':'The category contributions sum to a chi-square statistic, which now needs degrees of freedom and a significance criterion before a hypothesis decision can be made at the final console.',
'U5-L50':'Journey 8 closes only after the learner can separate organelle inheritance, qualified parent-of-origin patterns, illustrative disease cases, observed/expected categorical counts, chi-square computation, and reject/fail-to-reject decision logic.'
}

conf_by_kid=defaultdict(list)
for s in f2['confusable_sets']:
    for kid in s['knowledge_ids']: conf_by_kid[kid].append(s)

# F2 routes in fixed order.
journeys=[]
route_for={}
for j in f2['journeys']:
    route=[lid for b in j['bundles'] for lid in b['loci']]
    route_for[j['journey_id']]=route
    spec=journey_specs[j['journey_id']]
    journeys.append({
      'journey_id':j['journey_id'],'working_title':j['working_title'],'content_focus':j['content_focus'],'setting_logic':j['setting_logic'],
      'premise':spec['premise'],'mission':spec['mission'],'stakes':spec['stakes'],'continuity_object':spec['continuity_object'],
      'recurring_scientific_cast':spec['recurring_scientific_cast'],'opening_image':spec['opening_image'],'ending_payoff':spec['ending_payoff'],'tone':spec['tone'],
      'route':route,'unit_guide':unit_guide,
      'route_rule':'Keep the route in the exact F2 locus order. Every move must be caused by the unresolved scientific state left by the previous locus; no teleporting, route-primer quiz, or decorative detour.',
      'narrative_constraints':[
        'Orient the learner in the physical location before introducing new terminology.',
        'Keep left, center, and right anchors stable and redrawable throughout the scene.',
        'Use conventional chromosome, cell, allele, pedigree, organelle, or statistical geometry wherever the scientific visual is required.',
        'Let the scientific mechanism cause the memorable event; do not attach unrelated bizarre imagery to a term.',
        'Name a term only after its defining structure, relationship, or action is visible.',
        'Preserve the F1 canonical science and F2 destination exactly; narrative wording may clarify but may not change the mechanism or scope.',
        'The guide may point, compare, or operate a model but may never personify herself as the scientific term.',
        'Do not expose PPT, CED, Campbell, source-lock, review-flag, or assessment-management language in student prose.',
        'Keep chromosome complement language precise and do not conflate XX/XY inheritance models with gender or complete sex-development biology.',
        'Keep named human disorders and teacher examples contextual rather than universal definitions.',
        'Keep calculations and novel problem solving out of permanent story action when F2 assigns them to Challenge Lab.',
        'End with a compact reconstructable scientific state and a causal handoff to the next locus.'
      ],
      'status':'JOURNEY_BRIEF_LOCKED_F3_NO_POLISHED_STORY_PROSE'
    })

briefs=[]
for l in f2['loci']:
    lid=l['locus_id']; jid=l['journey_id']; geo=l['scene_geometry']; route=route_for[jid]; i=route.index(lid); next_lid=route[i+1] if i+1<len(route) else None
    steps=core[lid]
    stable_cast=[
      {'name':geo['left'],'position':'left','visual_identity':f"A conventional scientific representation of {geo['left']} fixed on the learner’s left, with labels limited to the biological identities needed for this locus.",'job_in_scene':'Establish the starting state, comparison, reference class, or input whose meaning must remain visible before the central mechanism changes anything.','type':'SCIENTIFIC_PART_OR_REFERENCE'},
      {'name':geo['center'],'position':'center','visual_identity':f"The largest working scientific model in the room, centered on {l['micro_anchor']}; any motion, pairing, separation, calculation, or comparison that defines the concept occurs here.",'job_in_scene':f"Perform the diagnostic mechanism that defines this locus: {steps[0]}",'type':'SCIENTIFIC_PROCESS_OR_STRUCTURE'},
      {'name':geo['right'],'position':'right','visual_identity':f"A conventional scientific representation of {geo['right']} fixed on the learner’s right; its visible state changes only after the central mechanism or comparison produces an interpretable outcome.",'job_in_scene':'Display the consequence, destination, alternative, product, or evidence state that proves what the center mechanism did.','type':'SCIENTIFIC_PART_OR_OUTPUT'}
    ]
    by_spoken=defaultdict(list)
    for kid in l['knowledge_ids']: by_spoken[records[kid]['canonical_label']].append(kid)
    terms=[]
    for n,kid in enumerate(l['knowledge_ids'],1):
        r=records[kid]; cl=class_by_id[kid]
        terms.append({
          'knowledge_id':kid,'canonical_term':r['canonical_label'],'canonical_science':r['canonical_verified_statement'],
          'exact_name_recall':bool(r.get('exact_name_recall',False)),'scope_class':r['scope_class'],
          'introduction_after_action_step':min(n,len(steps)),
          'insertion_rule':'Name the term only after its defining structure, relationship, or mechanism is visible. Translate the canonical science into readable biological language without weakening, expanding, or contradicting the F1 statement.',
          'spoken_term_group':r['canonical_label'],'merge_duplicate_spoken_label':len(by_spoken[r['canonical_label']])>1,
          'name_support':cl.get('name_support','SEMANTIC_SCIENCE_CUE_SUFFICIENT'),
          'name_support_rule':'First attempt uses the scientific scene and semantic role. If delayed exact-name retrieval fails, add only the F2-approved semantic/sound support; any phonological cue remains subordinate to the real biological structure and term.',
          'spelling_policy':cl.get('spelling_policy','ADAPTIVE_SUPPORT_ONLY_NO_MANDATORY_SPELLING_GATE')
        })
    guards=list(special_guards.get(lid,[])); seen=set()
    for kid in l['knowledge_ids']:
        for s in conf_by_kid.get(kid,[]):
            if s['set_id'] in seen: continue
            seen.add(s['set_id'])
            guards.append('Discrimination requirement: keep '+', '.join(s['terms'])+' physically and verbally distinct; do not let one label stand in for the full contrast set.')
    fids=[]
    for kid in l['knowledge_ids']:
        fid=records[kid].get('review_flag_id')
        if fid and fid not in fids: fids.append(fid)
    for fid in fids:
        if fid in flag_by_id: guards.append('Resolved science guard '+fid+': '+flag_by_id[fid]['resolution'])
    if not guards: guards.append('Preserve the conventional inheritance structure/process and do not add a mnemonic action that changes chromosome identity, causal direction, probability logic, parent-of-origin qualification, or statistical interpretation.')
    recall=recall_prompts.get(lid)
    labels=[]
    for kid in l['knowledge_ids']:
        lab=records[kid]['canonical_label']
        if lab not in labels: labels.append(lab)
    briefs.append({
      'scene_brief_id':'F3-'+lid,'locus_id':lid,'journey_id':jid,'bundle_id':l['bundle_id'],'scene_title':l['title'],'exact_location':l['title'],'micro_anchor':l['micro_anchor'],
      'entrance_from':route[i-1] if i>0 else 'JOURNEY_ENTRANCE',
      'orientation_sentence':f"Enter {l['title']} and stop at {l['micro_anchor']}. The left side is anchored by {geo['left']}, the working center is {geo['center']}, and the right side is anchored by {geo['right']}. Those anchors remain visible while the inheritance mechanism is resolved.",
      'spatial_layout':{
        'left':{'anchor':geo['left'],'layout_job':'fixed input/reference/comparison zone'},
        'center':{'anchor':geo['center'],'layout_job':'primary science-bearing action zone'},
        'right':{'anchor':geo['right'],'layout_job':'fixed consequence/output/comparison zone'}
      },
      'unit_guide':unit_guide,'stable_cast':stable_cast,'continuity_object':journey_specs[jid]['continuity_object'],
      'scene_problem':f"At this locus the learner must resolve the inheritance relationship represented by {l['micro_anchor']} while preserving the fixed left/center/right geography and the identities of all tracked chromosomes, alleles, cells, or data quantities.",
      'science_bearing_action':{
        'before':f"All three zones are visible but unresolved. The left state ({geo['left']}) provides the input or comparison, the center ({geo['center']}) has not yet executed its diagnostic mechanism, and the right state ({geo['right']}) cannot yet be interpreted reliably.",
        'trigger':'Imani identifies the unresolved inheritance question on the generation ledger and activates only the minimum chromosome, allele, cell, organelle, pedigree, or data structures needed to make the mechanism observable.',
        'during':steps,
        'after':f"Freeze the resolved state with {geo['left']} on the left, {geo['center']} in the center, and {geo['right']} on the right. The learner should be able to reconstruct what changed, which biological structure or rule caused the change, and what evidence distinguishes this locus from its closest confusable concept."
      },
      'knowledge_ids':l['knowledge_ids'],'primary_knowledge_id':l['primary_knowledge_id'],'term_introductions':terms,
      'visual_spec':{
        'visual_mode':l['visual_mode'],'conventional_scientific_visual_required':True,
        'must_show':[geo['left'],geo['center'],geo['right'],*steps],
        'must_not_show':['source-management labels, textbook references, or exam-instruction language','scientifically irrelevant decorative actors that compete with the inheritance mechanism','a mnemonic character replacing a real chromosome, chromatid, allele, gamete, organelle, pedigree symbol, or statistical quantity'],
        'composition_rule':'Preserve the F2 left/center/right geography and conventional scientific geometry. Animate only the biological or statistical relationship that changes; fixed anchors and persistent chromosome identities must remain redrawable from memory.'
      },
      'misconception_guards':guards,
      'adaptive_name_support':{
        'first_pass':'Use the conventional scientific structure/action plus the semantic role of the target. Do not surface a sound cue during first exposure merely because a genetics term is unfamiliar.',
        'fallback':'After an exact-name retrieval failure, use only the record-level F2 name-support classification. Strong phonological support is reserved for terms classified PHONOLOGICAL_SUPPORT_RECOMMENDED_IF_NEEDED.',
        'spelling':'No Unit 5 F2 target has a mandatory first-pass spelling gate; spelling support remains adaptive.'
      },
      'quick_recall':({'enabled':True,'candidate_prompt':recall[0],'answer':recall[1],'timing':'Optional first-exposure pause only after the defining mechanism and exact term/relationship have already been encountered.','hint_rule':'Point to one fixed spatial anchor or one diagnostic chromosome/allele/data action; do not reveal the answer term before the learner attempts retrieval.'} if recall else {'enabled':False,'timing':'Defer retrieval to Review so the story route remains uninterrupted.','hint_rule':'If later needed, return to one concrete scientific anchor/action without displaying the target term first.'}),
      'exit_memory':{
        'one_sentence_model':f"At {l['title']}, reconstruct the fixed {geo['left']} → {geo['center']} → {geo['right']} relationship and state the inheritance mechanism or comparison that changed the right-side interpretation.",
        'terms_to_carry':labels,
        'redraw_test':f"From memory, place {geo['left']} on the left, {geo['center']} in the center, and {geo['right']} on the right, then redraw or describe the chromosome, allele, cell, organelle, pedigree, or data transformation in causal order."
      },
      'causal_transition':{'to_locus_id':next_lid,'transition_logic':transition_reason[lid]},
      'story_prose_status':'PROHIBITED_UNTIL_F3_BRIEF_QA_PASS','brief_status':'LOCKED_F3_SCENE_BRIEF'
    })

scene_doc={
 'schema':'memory-palace-v2-unit5-f3-scene-briefs-1.0','generated_utc':GEN,'unit_id':'unit-5','canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','student_release':False,
 'design_standard':'NR-1.2: ORIENT -> FIX MICRO-ANCHOR -> IDENTIFY SCIENTIFIC PARTS -> ONE DIAGNOSTIC ACTION -> optional QUICK RECALL -> EXACT TERM/RELATIONSHIP -> CANONICAL TRANSLATION -> EXIT MEMORY -> CAUSAL MOVE',
 'counts':{'journeys':8,'scene_briefs':50,'palace_managed_records':131,'term_introductions':131,'optional_first_exposure_recalls':len(recall_prompts)},
 'scene_briefs':briefs
}
journey_doc={'schema':'memory-palace-v2-unit5-f3-journey-briefs-1.0','generated_utc':GEN,'unit_id':'unit-5','student_release':False,'unit_guide':unit_guide,'journey_count':8,'journeys':journeys}
dump(BRIEFS/'scene-briefs-f3.json',scene_doc); dump(BRIEFS/'journey-briefs-f3.json',journey_doc)

status={
 'unit_id':'unit-5','number':5,'title':'Heredity','status':'SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','pipeline_stage':'UNIT5_SCIENCE_BEARING_SCENE_BRIEFS_COMPLETE_F3',
 'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','source_status':'AUDITED_SCIENCE_LOCKED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3',
 'student_release':False,'preview_release':False,'canonical_records':152,'ced_atoms':34,'review_flags_resolved':37,'teacher_ppt_slides':112,'assessment_semantic_crosswalks':10,
 'journey_count':0,'scene_count':0,'memory_objects':0,'application_challenges':0,'architecture_journeys':8,'architecture_bundles':19,'architecture_loci':50,
 'journey_briefs':8,'scene_briefs':50,'palace_managed_records':131,'scope_guard_records':5,'practice_only_records':16,'confusable_sets':32,'exact_name_targets':130,
 'optional_first_exposure_recalls':len(recall_prompts),'next_required_output':'F4A polished narrative for Journey 1 only; do not author Journeys 2-8 until Journey 1 passes prose-level spatial, scientific, character, continuity, and memorability QA'
}
dump(U5/'status-f3.json',status); dump(U5/'status.json',status)
manifest={
 'schema':'memory-palace-v2-unit5-f3-release-1.0','generated_utc':GEN,'unit_id':'unit-5','release_status':'F3_SCENE_BRIEFS_LOCKED_NOT_STUDENT_RELEASED',
 'journey_briefs':8,'scene_briefs':50,'palace_managed_records':131,'term_introductions':131,'optional_first_exposure_recalls':len(recall_prompts),
 'practice_only_records':16,'scope_guards':5,'polished_story_files':0,'student_runtime_memory_objects':0,'application_challenges':0,'student_release':False,
 'next_stage':'F4A Journey 1 polished narrative only'
}
dump(U5/'f3-release-manifest.json',manifest)

course_path=ROOT/'content/ap-biology/course.json'; course=load(course_path)
for u in course['units']:
    if u['unit_id']=='unit-5':
        u.update({'status':status['status'],'journey_count':0,'scene_count':0,'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3',
                  'source_status':status['source_status'],'canonical_records':152,'review_flags_resolved':37,'student_release':False,'ced_atoms':34,'teacher_ppt_slides':112,
                  'architecture_journeys':8,'architecture_loci':50,'scene_briefs':50,'optional_first_exposure_recalls':len(recall_prompts),'pipeline_stage':status['pipeline_stage']})
dump(course_path,course)

# Designer-facing brief document.
lines=['# Unit 5 F3 Scene Briefs','','Status: `SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED`','',
 '- 8 journey continuity briefs','- 50 fixed loci / scene briefs','- 131 palace-managed canonical records represented exactly once','- 18 optional first-exposure Quick Recall candidates','- 0 polished Unit 5 narrative story files','- 16 practice-only records remain reserved for the later Challenge Lab','- 5 scope guards remain non-runtime','',
 '## F3 writing rule','',
 'Every later student scene must follow `ORIENT → FIX MICRO-ANCHOR → IDENTIFY PARTS → SCIENCE-BEARING ACTION → optional QUICK RECALL → EXACT TERM/RELATIONSHIP → CANONICAL TRANSLATION → EXIT MEMORY → CAUSAL MOVE`. The scientific structure and causal action remain primary. Name mnemonics may be added later only as adaptive retrieval support and may never replace the inheritance mechanism.','']
for j in journeys:
    lines += [f"## {j['journey_id']} · {j['working_title']}",'',j['premise'],'',f"**Mission.** {j['mission']}",'',f"**Continuity object.** {j['continuity_object']}",'',f"**Opening image.** {j['opening_image']}",'',f"**Ending payoff.** {j['ending_payoff']}",'']
    for lid in j['route']:
        b=next(x for x in briefs if x['locus_id']==lid)
        lines += [f"### {lid} · {b['scene_title']}",'',f"**Micro-anchor.** {b['micro_anchor']}",'',f"**Orientation.** {b['orientation_sentence']}",'',f"**Core scientific action.** {' '.join(b['science_bearing_action']['during'])}",'',f"**Exact terms/relationships.** {'; '.join(dict.fromkeys(t['canonical_term'] for t in b['term_introductions']))}",'',f"**Exit memory.** {b['exit_memory']['one_sentence_model']}",'',f"**Move.** {b['causal_transition']['transition_logic']}",'']
        if b['quick_recall']['enabled']: lines += [f"**Optional Quick Recall.** {b['quick_recall']['candidate_prompt']}",'']
(ROOT/'docs/UNIT5_F3_SCENE_BRIEFS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

release_doc='''# Unit 5 F3 Release\n\n**PASS — SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED**\n\nF3 converts the fixed F2 Unit 5 learning architecture into designer-ready journey and scene briefs. It creates no student-facing Unit 5 journeys.\n\n## Locked F3 accounting\n\n- 152 canonical records remain protected by F1.\n- 131 palace-managed records remain assigned exactly once.\n- 50/50 F2 loci now have one F3 scene brief.\n- 8/8 journeys now have premise, mission, stakes, continuity object, recurring scientific cast, opening image, ending payoff, route rule, and narrative constraints.\n- 18 optional first-exposure Quick Recall candidates are distributed across the eight journeys.\n- 16 practice-only records remain outside the palace for the later Challenge Lab.\n- 5 scope guards remain non-runtime.\n- 0 polished Unit 5 story files exist.\n- 0 Unit 5 student runtime Memory Objects exist.\n- Student release remains `false`.\n\n## Quality boundary\n\nEvery scene brief fixes exact physical geometry, scientific parts and jobs, before/during/after mechanism, canonical term introduction, name-support policy, misconception controls, scientific visual requirements, an exit-memory reconstruction target, and a causal handoff. Final narrative prose is still blocked.\n\n## Next gate\n\nF4A must write **Journey 1 only — Heredity and Chromosome Registry** from its five scene briefs. Journey 1 must pass prose-level spatial clarity, recurring-character/part clarity, scientific fidelity, exact-term integration, narrative continuity, and memorability QA before Journey 2 is authored.\n'''
(ROOT/'docs/UNIT5_F3_RELEASE.md').write_text(release_doc,encoding='utf-8')
qa_doc='''# Unit 5 F3 QA\n\n## Release decision\n\n**PASS — scene briefs locked; Unit 5 remains intentionally unreleased.**\n\n- 50/50 F2 loci have exactly one F3 scene brief.\n- 131/131 palace-managed canonical records appear exactly once.\n- 131 term/relationship introductions preserve the F1 canonical verified science verbatim in designer data.\n- 8/8 journey briefs have a stable route, premise, mission, stakes, continuity object, recurring scientific cast, opening image, ending payoff, and narrative constraints.\n- 18 optional first-exposure recalls are distributed across the eight journeys.\n- Every brief fixes entrance, left/center/right geography, micro-anchor, stable scientific parts, before/during/after action, conventional visual requirements, misconception guards, exit-memory target, and causal transition.\n- No polished Unit 5 story file exists.\n- Unit 5 journey/application runtime remains blocked.\n\n## Next gate\n\nF4A should author **U5-J1 only** and run prose-level narrative QA before any additional Unit 5 journey is written.\n'''
(ROOT/'docs/UNIT5_F3_QA.md').write_text(qa_doc,encoding='utf-8')

# Update onboarding text if present.
start=ROOT/'START_HERE.md'
if start.exists():
    txt=start.read_text(encoding='utf-8')
    txt=txt.replace('Unit 5 — F2 learning architecture locked, intentionally unreleased','Unit 5 — F3 journey/scene briefs locked, intentionally unreleased')
    txt=txt.replace('Unit 5 F2', 'Unit 5 F3') if 'Unit 5 F2' in txt and 'scene briefs' in txt else txt
    start.write_text(txt,encoding='utf-8')

lock_files=[
 'content/ap-biology/unit-5/source/canonical-unit5-f1.json',
 'content/ap-biology/unit-5/architecture/learning-classification-f2.json',
 'content/ap-biology/unit-5/architecture/palace-architecture-f2.json',
 'content/ap-biology/unit-5/briefs/journey-briefs-f3.json',
 'content/ap-biology/unit-5/briefs/scene-briefs-f3.json',
 'content/ap-biology/unit-5/f3-release-manifest.json','content/ap-biology/unit-5/status-f3.json'
]
# Workbook is included when it exists; rerunning after workbook export seals it.
wbrel='content/ap-biology/unit-5/audit/APBIO_Unit5_F3_Scene_Briefs.xlsx'
if (ROOT/wbrel).exists(): lock_files.append(wbrel)
lock={'schema':'memory-palace-v2-unit5-f3-content-lock-1.0','generated_utc':GEN,'unit_id':'unit-5','lock_status':'LOCKED_F3','student_release':False,'parents':['LOCKED_F1','LOCKED_F2'],'files':{rel:{'sha256':sha(ROOT/rel),'bytes':(ROOT/rel).stat().st_size} for rel in lock_files},'rule':'F3 locks Unit 5 journey continuity and science-bearing scene briefs only. F1 canonical science and F2 destinations/loci remain immutable; polished Unit 5 story prose remains prohibited until F4A.'}
dump(U5/'content-lock-f3.json',lock)
print(json.dumps(scene_doc['counts'],indent=2))
