from __future__ import annotations
import json, hashlib
from pathlib import Path
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[1]
U6=ROOT/'content'/'ap-biology'/'unit-6'
BRIEFS=U6/'briefs'; BRIEFS.mkdir(parents=True,exist_ok=True)
GEN='2026-09-08T00:20:00+00:00'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,obj): Path(p).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

src=read(U6/'source/canonical-unit6-f1.json')
canon={r['knowledge_id']:r for r in src['canonical_catalog']}
f2=read(U6/'architecture/palace-architecture-f2.json')
cls=read(U6/'architecture/learning-classification-f2.json')
class_by_id={r['knowledge_id']:r for r in cls['records']}
flag_by_id={f['review_flag_id']:f for f in src['review_flags']}

unit_guide={
 'name':'Dr. Sora Han',
 'role':'molecular-information systems director who accompanies the learner through all six Unit 6 journeys',
 'visual_identity':'dark-cobalt lab coat, clear gloves, transparent 5′→3′ compass tablet, and a narrow copper information ledger that can track one DNA, RNA, protein, regulatory, mutation, or biotechnology state at a time',
 'behavior_rule':'Sora fixes the learner in a stable left/center/right scientific layout, identifies the real molecules or structures first, changes only the feature needed to reveal the mechanism, and names the term only after its defining action or comparison is visible.',
 'continuity_rule':'Sora is a guide and recorder, never a substitute for a biological entity. DNA, RNA, polymerases, ribosomes, regulatory proteins, chromosomes, mutations, plasmids, gels, and sequence data retain conventional scientific geometry and jobs.'
}

journey_specs={
'U6-J1':dict(
 premise='The genome archive can store hereditary information, but its copying works cannot open until chromosome form, base pairing, strand direction, replication evidence, and fork machinery are all physically consistent.',
 mission='Carry one tagged DNA molecule from storage through a semiconservative replication cycle, keeping the same strands, 5′/3′ directions, origin, forks, primers, polymerases, fragments, repair steps, and chromosome ends visible as each new mechanism becomes necessary.',
 stakes='If strand identity or direction is lost, leading/lagging synthesis, primer use, ligase action, and telomere logic become memorized labels instead of a causal replication system. The brief therefore keeps the original strands and every 5′/3′ arrow visible through the complete copying route.',
 continuity_object='one persistent blue-and-gold DNA duplex with arrowheads marking 5′ and 3′ ends and a single tagged replication origin; the original strands remain identifiable as the molecule moves through the archive and copying works.',
 recurring_scientific_cast=['blue-and-gold DNA duplex with persistent strand identities','replication fork/origin machinery','daughter DNA or chromosome-end output'],
 opening_image='A DNA archive ledger shows chromosome and plasmid records, but the same tagged duplex cannot be copied until its base classes, antiparallel geometry, and replication model are reconciled.',
 ending_payoff='The same tagged duplex finishes as semiconservative daughter DNA with directional synthesis resolved, fragments joined, sequence accuracy protected, and chromosome ends distinguished from the enzyme that extends them.',
 tone='precise, mechanical, directional, evidence-driven'),
'U6-J2':dict(
 premise='A gene has been selected for expression, but the transcript workshop cannot ship a usable message until the correct DNA strand, promoter, RNA-synthesis direction, and eukaryotic processing steps are resolved.',
 mission='Track one tagged gene from transcription entry through RNA synthesis and, where appropriate, pre-mRNA processing, while keeping mRNA, tRNA, rRNA, template direction, promoter identity, caps, tails, introns, exons, and mature transcript roles distinct.',
 stakes='Without a stable template strand and RNA direction, students commonly reverse base-reading logic or collapse transcription, translation, and RNA processing into one undifferentiated event.',
 continuity_object='one tagged gene with its template strand marked in violet and a single RNA transcript ribbon that lengthens 5′→3′ and then receives only the processing steps appropriate to its cellular context.',
 recurring_scientific_cast=['tagged DNA template/promoter region','growing RNA transcript','RNA-processing or transcript-destination structures'],
 opening_image='The workshop receives one tagged gene beside mRNA, tRNA, and rRNA role markers, but none can be routed correctly until the same DNA molecule is oriented, one template strand is selected, a promoter is identified, and the growing transcript is tied to one directional synthesis path.',
 ending_payoff='A mature eukaryotic mRNA exits with its 5′ cap, poly-A tail, and resolved exon structure while the prokaryotic route remains visibly different. The learner can retrace which RNA molecule was made, which strand directed it, which processing steps were context-specific, and how mRNA, tRNA, and rRNA retain distinct jobs.',
 tone='editorial, directional, molecule-tracking focused'),
'U6-J3':dict(
 premise='A mature mRNA has reached the translation hall, but the ribosome cannot build a meaningful polypeptide until the reading frame, start signal, codon logic, tRNA charging, A/P/E movement, elongation, and stop logic are synchronized.',
 mission='Carry one mature mRNA from its start codon through a ribosome while charged tRNAs deliver amino acids, the polypeptide grows in sequence, and termination releases a product that begins folding.',
 stakes='If codon, anticodon, tRNA charging, ribosomal sites, and stop logic are taught as isolated vocabulary, learners can recite names while failing to translate a sequence or explain the mechanism.',
 continuity_object='one mature mRNA ribbon with its AUG start codon highlighted, fixed triplet spacing, and one growing polypeptide chain whose amino-acid order is updated only when the ribosome advances by exactly one codon; neither the reading frame nor the original mRNA sequence is replaced between scenes.',
 recurring_scientific_cast=['mature mRNA with fixed reading frame','charged tRNAs and ribosomal A/P/E sites','growing/released polypeptide'],
 opening_image='The mature mRNA lies across an idle ribosome with its bases visible but no agreed reading frame. Charged and uncharged tRNAs, free amino acids, and ribosomal sites wait around it, making clear that translation cannot begin until AUG establishes a starting position and a codon-by-codon route.',
 ending_payoff='The ribosome reaches a stop codon, release occurs without a stop-codon tRNA, the polypeptide exits in the encoded order, and reverse transcription remains a separate retroviral exception to the usual information-flow route.',
 tone='assembly-line precise, sequential, code-to-product focused'),
'U6-J4':dict(
 premise='A cell contains the same genome as many neighboring cells, yet its expression-control center must decide which genes are on, how strongly they are expressed, and how those decisions become a specialized phenotype.',
 mission='Use one tracked gene and expression meter to compare constitutive/inducible control, operons, repressible and inducible systems, eukaryotic regulatory layers, epigenetic state, enhancer/promoter recruitment, RNA-level control, and developmental specialization.',
 stakes='Regulation is easily reduced to “genes turn on and off.” The route must make the regulatory DNA, regulatory proteins, chromatin state, RNA processing, and expression outputs visible as distinct causal layers.',
 continuity_object='one tracked gene with a promoter-linked expression meter and a chromatin state strip; its DNA sequence stays fixed while regulatory inputs, chromatin accessibility, transcript amount, and cell phenotype change.',
 recurring_scientific_cast=['tracked gene/promoter or operon DNA','regulatory proteins/chromatin/RNA regulators','expression meter and differentiated-cell output'],
 opening_image='Several model cells display the same tracked gene sequence, yet their expression meters and protein outputs differ sharply. Promoter DNA, regulatory proteins, chromatin marks, RNA-processing controls, and developmental signals are all visible but inactive, forcing the learner to locate which regulatory layer changes before phenotype changes.',
 ending_payoff='The same DNA sequence produces different expression profiles and specialized cell states through coordinated regulation, while developmental cues and programmed cell death remain mechanistically distinguishable.',
 tone='control-system, layered, causal, phenotype-linked'),
'U6-J5':dict(
 premise='A reference genome enters the mutation yard, where sequence changes, chromosome errors, mobile DNA, and horizontal transfer can alter information in different ways and with different consequences.',
 mission='Compare one reference sequence with mutated or rearranged versions, trace consequences from DNA to product/phenotype, and separate substitution, frameshift, chromosome-number, chromosome-structure, horizontal-transfer, transposition, and viral-recombination mechanisms.',
 stakes='Mutation terminology becomes misleading if every DNA change is assumed harmful, every indel is called a frameshift, or horizontal transfer is confused with ordinary vertical inheritance.',
 continuity_object='one reference DNA sequence and phenotype readout on Sora’s copper ledger; each station changes only one feature so the molecular consequence can be compared with the unchanged reference.',
 recurring_scientific_cast=['reference DNA/chromosome state','single altered DNA/chromosome or transfer mechanism','molecular/phenotypic consequence readout'],
 opening_image='The yard receives one intact reference DNA sequence beside altered copies and chromosome models, but all mutation labels have been removed. The only way to classify each case is to compare exactly what nucleotide, reading frame, chromosome number, chromosome segment, or DNA-transfer route physically changed and then trace its consequence.',
 ending_payoff='Each altered sequence or chromosome is classified by mechanism and consequence, and externally acquired/mobile/recombined DNA remains distinct from replication error and meiotic inheritance.',
 tone='forensic, comparative, consequence-focused'),
'U6-J6':dict(
 premise='An unknown DNA sample enters the biotechnology lab, but no conclusion can be trusted until DNA manipulation, amplification, separation, transformation, sequencing, and profile comparison are tied to what each technique actually measures or changes.',
 mission='Carry one coded DNA sample through a minimal investigation pipeline, using PCR, gel electrophoresis, transformation/recombinant expression, sequencing, and profile comparison without turning laboratory tools into decorative vocabulary.',
 stakes='Biotechnology questions often test interpretation. Learners must understand what material enters each technique, what physical process occurs, and what type of evidence or product exits.',
 continuity_object='one coded DNA sample tube labeled U6-X that is amplified or analyzed without changing identity; when recombinant expression is required, a separate clearly labeled plasmid receives the intended insert.',
 recurring_scientific_cast=['coded DNA sample U6-X','laboratory mechanism or vector','measured band/sequence/expression output'],
 opening_image='The lab receives a tiny DNA sample that is insufficient for several analyses, forcing the learner to choose an operation based on the question rather than from a memorized list of techniques.',
 ending_payoff='The sample has been amplified, separated, introduced into bacteria when expression is needed, sequenced, and compared, with each output interpreted according to the mechanism that produced it.',
 tone='investigative, procedural, evidence-focused')
}

# Diagnostic mechanism steps for each locus. These are design instructions, not polished learner prose.
A={
'U6-L01':['File DNA and RNA under hereditary information only after showing that genetic information can be carried by DNA and, in some cases, RNA.','Use Franklin and model-building evidence as contextual panels that constrain DNA structure without making historical names the main retrieval target.','Close the intake by linking hereditary information to a physical nucleic-acid molecule that can be stored and copied.'],
'U6-L02':['Place a typical prokaryotic circular chromosome on the left and a typical eukaryotic linear chromosome on the right.','Change only the eukaryotic chromosome condensation state so linear DNA versus condensed chromosome form remain distinct ideas.','Freeze a comparison that states these are typical cellular architectures, not exceptionless rules across all organisms or organelles.'],
'U6-L03':['Track a small circular plasmid independently of the main chromosome and show independent replication.','Insert a defined DNA segment into a plasmid model to create recombinant plasmid DNA without changing the meaning of plasmid itself.','Route the plasmid through a transfer channel and show that plasmid-carried genes can have conditional value depending on environment.'],
'U6-L04':['Sort adenine/guanine into a two-ring purine drawer and cytosine/thymine/uracil into a one-ring pyrimidine drawer.','Use a composition table to impose Chargaff relationships in double-stranded DNA without claiming all organisms have identical base percentages.','Require the learner to discriminate base class from base-pairing partner.'],
'U6-L05':['Lay the two DNA backbones in opposite 5′→3′ directions and pair complementary bases across them.','Keep phosphodiester backbone bonds visually separate from hydrogen bonds between paired bases and display A–T versus G–C hydrogen-bond counts.','Contrast typical double-stranded DNA with typically single-stranded RNA while allowing RNA to form internal paired regions.'],
'U6-L06':['Reactivate the eukaryotic S-phase context only for eukaryotic cells, keeping prokaryotic chromosome replication outside a falsely imposed eukaryotic cell-cycle phase structure.','Pass the tagged DNA duplex through a continuity gate that requires accurate copying before cell division or inheritance can proceed.','Keep replication purpose tied to preservation of hereditary information rather than to gene expression.'],
'U6-L07':['Build conservative, semiconservative, and dispersive model outputs from visibly different strand-distribution predictions.','Run the Meselson–Stahl isotope outcome through the center evidence bench.','Reject the models whose predicted density pattern conflicts with the observed generations and retain semiconservative replication.'],
'U6-L08':['Mark a specific origin of replication on the tagged duplex and open a replication bubble with two fork boundaries so the origin and the moving forks cannot be treated as the same structure.','Use helicase at the fork to separate strands while topoisomerase acts ahead of the fork to relieve torsional strain.','Keep origin, helicase, topoisomerase, and replication fork spatially distinct so enzyme names map to different physical jobs.'],
'U6-L09':['Stabilize exposed single-stranded DNA with single-strand binding proteins as contextual support.','Use primase to place an RNA primer, then allow DNA polymerase to extend only from the primer’s 3′ end.','Move DNA polymerase along its template so template reading and new-strand 5′→3′ synthesis are directionally linked.'],
'U6-L10':['Keep new DNA synthesis 5′→3′ on both branches while fork geometry forces different synthesis patterns.','Show continuous synthesis on the leading-strand track and discontinuous synthesis on the lagging-strand track.','Build lagging-strand DNA as distinct Okazaki fragments that remain unfinished until the next bench.'],
'U6-L11':['Show RNA-primer removal/replacement only as contextual mechanism, not as an extra AP enzyme-name memorization list.','Use ligase to seal remaining nicks between lagging-strand DNA fragments after replacement.','Use proofreading and broad mismatch/excision repair as accuracy-preserving processes without over-expanding named repair pathways.'],
'U6-L12':['Place repetitive telomere DNA at the physical ends of a linear chromosome.','Use telomerase as an enzyme that can extend telomeric DNA in relevant cells.','Require explicit telomere-versus-telomerase discrimination: DNA end sequence/region versus enzyme.'],
'U6-L13':['Keep RNA sequence/structure at center and route different RNA molecules to different functions.','Send mRNA to a message role and rRNA into the ribosome structural/catalytic complex.','Make RNA function depend on sequence and folded structure rather than on the generic label RNA.'],
'U6-L14':['Attach a specific amino acid to the correct tRNA identity while leaving the anticodon visible, so amino-acid specificity and later codon recognition remain two distinct features of the same tRNA.','Pair the tRNA anticodon with a complementary mRNA codon using antiparallel base-pairing geometry.','Route the tRNA toward the ribosome only after both amino-acid identity and anticodon role are clear.'],
'U6-L15':['Place transcription on the DNA→RNA lane and translation on the RNA→polypeptide lane.','Reactivate protein structure only as the downstream functional destination of gene expression.','Keep gene expression as the larger process that includes transcription and, for protein-coding genes, translation.'],
'U6-L16':['Select one DNA strand as the transcription template and keep the opposite strand visibly separate.','Position a promoter before the transcribed region and recruit transcription machinery to that regulatory DNA.','Display a TATA box only as one promoter element found in many eukaryotic genes, never as the universal promoter definition.'],
'U6-L17':['Lock RNA synthesis to 5′→3′ while RNA polymerase reads the template 3′→5′.','Sequence initiation, elongation, and termination along one uninterrupted transcript rail.','Allow multiple RNA polymerases to occupy the same gene when appropriate, illustrating increased transcript output without changing synthesis direction.'],
'U6-L18':['Keep a prokaryotic transcript in the same cellular compartment as ribosomes.','Show that the transcript can become usable for translation without the eukaryotic nucleus-based cap/poly-A/splicing route.','Preserve the distinction between “no eukaryotic pre-mRNA processing requirement” and “no RNA processing ever occurs in prokaryotes.”'],
'U6-L19':['Receive eukaryotic pre-mRNA before export and attach a 5′ cap at one end.','Recognize the polyadenylation signal and add a poly-A tail at the 3′ end.','Tie cap/tail features to transcript stability, processing/export/translation recognition functions without treating either feature as part of the encoded protein sequence.'],
'U6-L20':['Mark intron and exon regions on the same pre-mRNA with persistent boundaries so the learner can track exactly which RNA segments are removed and which remain in the mature transcript.','Excise the marked intron regions and join the remaining exon segments into one continuous mature mRNA, preserving the original 5′→3′ orientation throughout the operation.','Re-run the splice selection with a different exon combination to demonstrate alternative splicing without changing the underlying gene DNA.'],
'U6-L21':['Place eukaryotic translation on cytosolic or rough-ER-associated ribosomes according to protein destination context.','Place prokaryotic transcription and translation in the same compartment so ribosomes can begin translating an emerging transcript.','Make cellular geography, not mnemonic wording, explain why coupling is possible in prokaryotes.'],
'U6-L22':['Align the mRNA into triplets and establish a reading frame from an AUG start codon.','Use initiation as the gate that positions the ribosome and initiator tRNA correctly.','Carry the established reading frame forward into elongation and termination; do not allow arbitrary re-grouping of bases.'],
'U6-L23':['Divide mRNA into three-nucleotide codons and map each codon to an amino acid or stop instruction.','Show multiple codons mapping to the same amino acid to encode redundancy.','Show broad conservation of the genetic code as near universality while avoiding the false claim of absolute universality.'],
'U6-L24':['Match each tRNA with the correct amino acid using aminoacyl-tRNA synthetase.','Create a charged tRNA only after the amino acid is covalently attached.','Deliver the charged tRNA to the ribosome so synthetase charging stays distinct from anticodon-codon pairing.'],
'U6-L25':['Use corrected bacterial 30S/50S and eukaryotic 40S/60S subunit values only as teacher enrichment.','Place incoming aminoacyl-tRNA in A, peptidyl-tRNA in P, and exiting uncharged tRNA in E.','Keep A/P/E as functional positions, not as names for ribosomal subunits.'],
'U6-L26':['Match the next charged tRNA anticodon to the complementary mRNA codon in the A site while the growing polypeptide remains attached to the tRNA occupying the P site.','Form the next peptide bond and transfer the growing chain according to ribosome chemistry.','Translocate the ribosome one codon so tRNAs shift through A→P→E while the reading frame stays fixed.'],
'U6-L27':['Continue elongation until a stop codon occupies the decoding position.','Use a release factor rather than a stop-codon tRNA to terminate translation and release the polypeptide.','Allow the released chain to begin/continue folding while keeping translation termination distinct from protein maturation.'],
'U6-L28':['Introduce a retroviral RNA genome as the starting information molecule.','Use reverse transcriptase to synthesize a complementary DNA product from the retroviral RNA template, keeping the RNA-to-DNA information direction visible throughout synthesis.','Route the DNA product toward integration/host-DNA context rather than falsely depicting DNA becoming part of RNA.'],
'U6-L29':['Place regulatory DNA sequences and regulatory proteins around one tracked gene.','Compare constitutive expression with expression that changes when regulatory conditions change.','Use the expression meter to show that regulation changes gene-product output without requiring a change in the gene’s DNA sequence.'],
'U6-L30':['Lay out promoter, operator, and structural genes as physically distinct parts of one operon model.','Bind or release a repressor at the operator to alter transcription of the coordinated gene set.','Keep “operon” as the DNA/regulatory unit and “repressor protein” as the diffusible regulator.'],
'U6-L31':['Reactivate allosteric regulation only as the logic of ligand-dependent protein conformation.','Use tryptophan as a corepressor that activates the trp repressor for operator binding when tryptophan is abundant.','Reduce trp operon transcription in the high-tryptophan state and release repression when tryptophan is low.'],
'U6-L32':['Start with the lac repressor blocking transcription in the absence of inducer.','Use allolactose as the inducer that changes repressor behavior so transcription can proceed when lactose is available.','Identify lac structural-gene products as bacterial lactose-use proteins including β-galactosidase, not simply “lactase.”'],
'U6-L33':['Display regulation at chromatin/transcription, RNA processing/stability, translation, and protein-level stages.','Change one layer at a time while keeping the same tracked gene and expression meter.','Show coordinated eukaryotic control as multi-layer regulation rather than one universal on/off switch.'],
'U6-L34':['Alter histone acetylation and DNA methylation states on the same chromatin region.','Associate these reversible epigenetic marks with changes in chromatin accessibility/expression while avoiding absolute rules.','Show that some epigenetic states can persist through cell divisions without equating epigenetic inheritance with a DNA-sequence mutation.'],
'U6-L35':['Place promoter and enhancer/control elements at physically separate regulatory DNA positions that may be upstream or downstream.','Recruit activators/repressors and transcription machinery through DNA looping/contact logic.','Keep promoter, enhancer/control element, activator, and repressor as distinct entities with distinct jobs.'],
'U6-L36':['Hold the tracked gene sequence and promoter position constant while the expression meter remains at its baseline level, so any later decrease can be assigned to the negative regulatory input.','Add a negative regulator/repressor that reduces transcription through its specific regulatory interaction.','Remove or counter the negative input and show expression recover, proving negative regulation through the expression meter.'],
'U6-L37':['Use small regulatory RNAs to alter transcript stability or translation after transcription.','Run alternative splicing as a separate RNA-level regulatory mechanism that changes isoform output.','Distinguish microRNA and siRNA as small-RNA regulatory categories without requiring mechanistic over-detail beyond the locked scope.'],
'U6-L38':['Hold the genome constant while changing which genes are expressed and how much product accumulates.','Update an expression-profile console across multiple genes so the learner can compare which products increase, decrease, or remain unchanged while the underlying genome stays constant.','Connect product amount/function to phenotype while avoiding the idea that phenotype is determined by transcript amount alone.'],
'U6-L39':['Place two cells with the same genome on opposite sides of the gallery.','Activate different gene-expression programs so different tissue-specific proteins accumulate.','Show cell differentiation/specialization as a consequence of differential gene expression, not different inherited genomes in ordinary somatic cells.'],
'U6-L40':['Sequence developmental gene-expression changes over time rather than activating all developmental genes at once.','Use cytoplasmic determinants and induction as distinct sources of developmental information that alter downstream expression.','Connect pattern formation/homeotic-gene logic and apoptosis to organized development without making one regulator responsible for all morphogenesis.'],
'U6-L41':['Compare one reference DNA sequence with a changed version while keeping environment and phenotype readout visible.','Trace the change through molecular product/function before judging phenotypic effect.','Allow the same mutation to have neutral, harmful, or beneficial consequences depending on molecular and environmental context, then connect heritable variation with selection.'],
'U6-L42':['Make a single-nucleotide substitution in the reference coding sequence.','Translate the altered codon and classify the result as silent, missense, or nonsense according to protein consequence.','Keep “point substitution” as the DNA-level change and silent/missense/nonsense as possible coding consequences.'],
'U6-L43':['Insert or delete nucleotides in a coding sequence by an amount not divisible by three.','Shift every downstream codon grouping after the insertion or deletion and show the altered reading frame continuing until a new stop or the end of the modeled sequence.','Keep indels divisible by three out of the frameshift category, preserving the definition.'],
'U6-L44':['Expose the reference DNA to replication errors or mutagenic physical/chemical sources without implying directed need-based mutation.','Add the resulting new sequence variant to a population-variation pool.','Keep mutation-generated variation distinct from meiotic recombination/independent assortment/fertilization reactivation.'],
'U6-L45':['Mis-segregate chromosomes during cell division to produce abnormal chromosome number.','Show nondisjunction as the segregation error mechanism and separate it from structural rearrangement.','Use trisomy 21 only as a contextual example of chromosome-number change, not a required named-disorder memorization target.'],
'U6-L46':['Begin with one intact chromosome and alter structure without changing the mechanism into nondisjunction.','Create deletion, duplication, inversion, and translocation as visually distinct rearrangements.','Require the learner to identify which segment was lost, copied, reversed, or moved before naming the rearrangement.'],
'U6-L47':['Start with DNA outside a recipient cell, inside a bacteriophage, or in a directly connected donor cell so the three horizontal-transfer routes begin from visibly different physical sources.','Compare transformation, transduction, and conjugation by the physical route through which DNA reaches the recipient.','Unify all three under horizontal gene transfer while keeping their mechanisms distinct from vertical inheritance.'],
'U6-L48':['Move a transposable element from one genomic position to another without equating it with plasmid transfer.','Co-infect a viral host/cell model with distinguishable genomes and show recombination producing new viral sequence combinations.','Keep transposition and viral recombination as separate mechanisms that can generate genomic variation.'],
'U6-L49':['Define a concrete DNA question and identify what information or molecular product is missing before selecting any biotechnology tool, preventing technique names from becoming detached from investigative purpose.','Manipulate or analyze the nucleic acid only through a method whose physical mechanism can produce the required evidence or product, and keep the original sample identity visible through the step.','Require every later tool to identify its input, mechanism, and output rather than being memorized as a detached procedure name.'],
'U6-L50':['Load DNA samples into wells of a gel matrix and apply an electric field.','Use the negatively charged DNA backbone to drive DNA toward the positive electrode while the matrix separates fragments primarily by size.','Read band position/pattern as an analysis output without claiming gel electrophoresis reveals nucleotide sequence directly.'],
'U6-L51':['Begin with a small amount of target DNA and heat to denature template strands.','Cool the reaction so short primers anneal to their complementary target sequences on the separated template strands, defining the boundaries of the DNA region that will be amplified.','Extend primers with DNA polymerase and repeat cycles to amplify the region exponentially in principle.'],
'U6-L52':['Introduce recombinant plasmid DNA into competent bacteria as a transformation step.','Allow transformed bacteria to maintain/express the engineered DNA under appropriate conditions.','Separate bacterial transformation as a technique from ordinary gene expression and from horizontal transfer terminology used in ecological/evolutionary contexts.'],
'U6-L53':['Determine nucleotide sequence from the DNA sample using a sequencing method at the appropriate abstraction level.','Convert sequence/profile data into comparable records for identification, relationship, or similarity questions.','Keep sequence determination distinct from fragment-size gel patterns and explain what evidence a DNA profile can and cannot establish.']
}

# Sparse first-exposure recall candidates.
quick={
'U6-L04','U6-L07','U6-L10',
'U6-L14','U6-L17','U6-L20',
'U6-L22','U6-L25','U6-L27',
'U6-L30','U6-L32','U6-L34','U6-L39',
'U6-L42','U6-L45','U6-L47',
'U6-L50','U6-L51'
}

# Journey-level constraints used by F4 writers.
base_constraints=[
 'Begin every scene by orienting the learner to the fixed left/center/right geometry before the central mechanism changes anything.',
 'Use conventional molecular and cellular geometry for DNA, RNA, chromosomes, polymerases, ribosomes, operons, chromatin, mutations, gels, plasmids, and sequence data.',
 'The recurring guide may point, carry the continuity ledger, or trigger a display, but must never replace a scientific molecule, structure, enzyme, or term.',
 'Introduce the exact scientific term only after its defining structure, comparison, or mechanism is visible.',
 'Preserve F1 qualifiers such as typical, usually, can, may, and context-dependent when they are scientifically necessary.',
 'Do not expose PPT, CED, Campbell, source, lock, enrichment, exam-scope, or teacher-management language in student narrative.',
 'Do not convert contextual enrichment or scope guards into mandatory student recall.',
 'Reuse prior-unit knowledge as reactivation when F2 says PRIOR_UNIT_REACTIVATION; do not create a second mnemonic identity for the same prerequisite fact.',
 'Keep confusable terms physically separated until their diagnostic difference has been shown, then compare them directly.',
 'Animate only the relationship needed for the locus; avoid decorative absurdity that competes with the scientific mechanism.',
 'Carry one stable continuity object through the journey so route memory and causal memory reinforce one another.',
 'End each scene with a visible consequence that naturally creates the problem solved by the next locus.',
 'Quick Recall is optional during first exposure and appears only at F3-approved candidate loci after the science has already been encountered.',
 'Exact-name retrieval later must be possible from the biological role and scene, with phonological support used only as F2-approved adaptive fallback.',
 'No polished story sentence may alter a canonical F1 statement, causal direction, formula, base-pairing rule, strand direction, or scope boundary.'
]

# Index F2 routes and confusables.
journey_routes={j['journey_id']:[lid for b in j['bundles'] for lid in b['loci']] for j in f2['journeys']}
conf_by_kid=defaultdict(list)
for c in f2['confusable_sets']:
    for kid in c['knowledge_ids']: conf_by_kid[kid].append(c)

# Journey briefs.
journey_briefs=[]
for j in f2['journeys']:
    spec=journey_specs[j['journey_id']]
    route=journey_routes[j['journey_id']]
    journey_briefs.append({
      'journey_id':j['journey_id'],'f2_working_title':j['working_title'],'topics':j['topics'],
      'premise':spec['premise'],'mission':spec['mission'],'stakes':spec['stakes'],
      'unit_guide':unit_guide,'continuity_object':spec['continuity_object'],
      'recurring_scientific_cast':spec['recurring_scientific_cast'],
      'opening_image':spec['opening_image'],'ending_payoff':spec['ending_payoff'],'tone':spec['tone'],
      'route':route,'route_rule':'Travel the F2 locus order exactly. A scene may foreshadow the next locus but may not reorder, merge, or skip permanent loci without a new architecture version.',
      'narrative_constraints':base_constraints,
      'status':'JOURNEY_BRIEF_LOCKED_F3_NO_POLISHED_STORY_PROSE'
    })

# Create one scene brief per F2 locus.
scene_briefs=[]
for l in f2['loci']:
    jid=l['journey_id']; route=journey_routes[jid]; idx=route.index(l['locus_id'])
    entrance='JOURNEY_ENTRANCE' if idx==0 else route[idx-1]
    nxt=route[idx+1] if idx+1<len(route) else None
    spec=journey_specs[jid]
    kids=l['knowledge_ids']; records=[canon[k] for k in kids]
    classes=[class_by_id[k] for k in kids]
    steps=A[l['locus_id']]
    left=l['scene_geometry']['left']; center=l['scene_geometry']['center']; right=l['scene_geometry']['right']
    # Term introductions preserve science verbatim; prose writers may translate only later.
    intros=[]
    for n,(r,c) in enumerate(zip(records,classes),1):
        intros.append({
          'knowledge_id':r['knowledge_id'],'canonical_term':r['canonical_label'],'canonical_science':r['canonical_verified_statement'],
          'scope_class':r['scope_class'],'exact_name_recall':bool(c['exact_name_recall']),
          'delayed_review_target':bool(c['delayed_review_target']),'reactivation_mode':c['reactivation_mode'],
          'introduction_after_action_step':min(n,len(steps)),
          'insertion_rule':'Name the term only after its defining structure, relationship, comparison, or mechanism is visible. Student prose may clarify the locked science but may not weaken, broaden, or contradict the F1 statement.',
          'name_support':c['name_support'],'name_support_rule':'Use the scientific scene and semantic role first. Only after delayed exact-name failure may F2-approved semantic/phonological support be added; a sound cue never replaces the biological mechanism.',
          'spelling_policy':c['spelling_policy']
        })
    # Guards from resolved review flags and confusable sets.
    guards=[]
    rfids=[]
    for r in records:
        rfids.extend(r.get('review_flag_ids',[]))
    for fid in dict.fromkeys(rfids):
        if fid in flag_by_id: guards.append(f"Resolved F1 guard {fid}: {flag_by_id[fid]['resolution']}")
    seen_sets=[]
    for kid in kids:
        for c in conf_by_kid.get(kid,[]):
            if c['set_id'] not in seen_sets:
                seen_sets.append(c['set_id'])
                guards.append(f"Discrimination requirement {c['set_id']}: keep {', '.join(c['terms'])} physically and verbally distinct until the diagnostic comparison is complete.")
    reactiv=[{'knowledge_id':r['knowledge_id'],'term':r['canonical_label'],'dependency':r.get('cross_unit_dependencies',[]),'rule':'Reactivate the prior representation briefly; extend it into the Unit 6 mechanism without assigning a new mnemonic identity.'} for r,c in zip(records,classes) if c['reactivation_mode']=='PRIOR_UNIT_REACTIVATION']
    # Stable cast uses actual F2 anchors plus guide.
    cast=[
      {'name':left,'position':'left','visual_identity':f"A conventional scientific representation of {left}, fixed on the learner’s left with only the labels needed for this locus.",'job_in_scene':'Establish the input, reference state, prerequisite, or comparison that must remain visible before the central mechanism acts.','type':'SCIENTIFIC_PART_OR_REFERENCE'},
      {'name':center,'position':'center','visual_identity':f"The largest working scientific model at {l['title']}, centered on {l['micro_anchor']}; the diagnostic biological or analytical action occurs here.",'job_in_scene':f"Execute the defining action sequence: {steps[0]}",'type':'SCIENTIFIC_PROCESS_OR_STRUCTURE'},
      {'name':right,'position':'right','visual_identity':f"A conventional scientific representation of {right}, fixed on the learner’s right and updated only after the central action produces an interpretable consequence.",'job_in_scene':'Display the product, consequence, alternative model, evidence state, or destination that confirms what the center mechanism did.','type':'SCIENTIFIC_PART_OR_OUTPUT'}
    ]
    primary=canon[l['primary_knowledge_id']]
    q_enabled=l['locus_id'] in quick
    scene_briefs.append({
      'scene_brief_id':f"F3-{l['locus_id']}",'locus_id':l['locus_id'],'journey_id':jid,'bundle_id':l['bundle_id'],
      'scene_title':l['title'],'exact_location':l['title'],'micro_anchor':l['micro_anchor'],'entrance_from':entrance,
      'orientation_sentence':f"Enter {l['title']} and stop at {l['micro_anchor']}. The left side is anchored by {left}, the working center is {center}, and the right side is anchored by {right}. Those three anchors remain in fixed positions while only the diagnostic Unit 6 mechanism changes their scientific state.",
      'spatial_layout':{
        'left':{'anchor':left,'layout_job':'fixed input/reference/prerequisite/comparison zone'},
        'center':{'anchor':center,'layout_job':'primary science-bearing action zone'},
        'right':{'anchor':right,'layout_job':'fixed consequence/output/evidence/comparison zone'}
      },
      'unit_guide':unit_guide,'stable_cast':cast,'continuity_object':spec['continuity_object'],
      'scene_problem':f"Resolve the scientific relationship encoded by {l['micro_anchor']} while preserving the F2 geometry and the persistent molecule/data identities for {jid}.",
      'science_bearing_action':{
        'before':f"All three zones are visible but unresolved. The left state ({left}) supplies the starting reference, the center ({center}) has not yet completed its diagnostic action, and the right state ({right}) cannot yet be interpreted.",
        'trigger':'Sora identifies the single unresolved molecular-information question on the copper ledger and activates only the minimum DNA, RNA, protein, regulatory, chromosome, mutation, or biotechnology structures needed to make the relationship observable.',
        'during':steps,
        'after':f"Freeze the resolved state with {left} on the left, {center} in the center, and {right} on the right. The learner must be able to state what changed, what biological mechanism caused the change, and which evidence distinguishes this scene from its closest confusable concept."
      },
      'knowledge_ids':kids,'primary_knowledge_id':l['primary_knowledge_id'],'term_introductions':intros,
      'prior_unit_reactivation':reactiv,
      'visual_spec':{
        'visual_mode':l['visual_mode'],'conventional_scientific_visual_required':True,
        'must_show':[left,center,right,*steps],
        'must_not_show':['source-management labels, textbook references, exam-scope labels, or content-lock language','a mnemonic character replacing a real molecule, chromosome, enzyme, ribosome, regulatory element, mutation, gel band, plasmid, or sequence','decorative actions that imply a scientific causal relationship absent from the F1 lock'],
        'composition_rule':'Preserve the F2 left/center/right geography and conventional scientific geometry. Animate only the biological or analytical relationship that changes; all fixed anchors and persistent molecule/sequence identities must remain reconstructable from memory.'
      },
      'misconception_guards':guards,
      'adaptive_name_support':{
        'first_pass':'Use the conventional scientific structure/action and semantic role. Do not surface a sound cue during first exposure merely because a molecular-biology term is unfamiliar.',
        'fallback':'After exact-name retrieval failure, use only the record-level F2 name-support classification. Phonological support remains subordinate to the real biological structure and role.',
        'spelling':'No Unit 6 F2 target has a mandatory first-pass spelling gate; spelling support remains adaptive.'
      },
      'quick_recall':{
        'enabled':q_enabled,
        'candidate_prompt':f"Without looking back, identify or explain {primary['canonical_label']} from the scientific action you just watched." if q_enabled else None,
        'answer':primary['canonical_verified_statement'] if q_enabled else None,
        'timing':'Optional first-exposure pause only after the defining mechanism and exact term/relationship have already been encountered.' if q_enabled else 'No first-exposure interruption at this locus.',
        'hint_rule':'Point to one fixed spatial anchor or one diagnostic molecular/data action; do not reveal the answer term before the learner attempts retrieval.' if q_enabled else None
      },
      'exit_memory':{
        'one_sentence_model':f"At {l['title']}, reconstruct {left} → {center} → {right} and explain the Unit 6 mechanism that changes or interprets the right-side state.",
        'terms_to_carry':[r['canonical_label'] for r in records if class_by_id[r['knowledge_id']]['delayed_review_target']],
        'redraw_test':f"From memory, place {left} on the left, {center} in the center, and {right} on the right, then redraw or describe the molecule, sequence, regulatory, chromosome, mutation, or data transformation in causal order."
      },
      'causal_transition':{
        'to_locus_id':nxt,
        'transition_logic':(f"Once {l['title']} resolves {primary['canonical_label']}, the same continuity object remains intact and the unresolved consequence moves directly to {next(x['title'] for x in f2['loci'] if x['locus_id']==nxt)}. The transition must arise from the biological or analytical output of this scene, not from a narrator announcing a new vocabulary term." if nxt else f"{l['title']} closes {jid}: the continuity object now displays the resolved final state for the journey, and the learner can reconstruct the full route without adding another permanent locus.")
      },
      'story_prose_status':'PROHIBITED_UNTIL_F3_BRIEF_QA_PASS','brief_status':'LOCKED_F3_SCENE_BRIEF'
    })

scene_doc={
 'schema':'memory-palace-v2-unit6-scene-briefs-f3-1.0','generated_utc':GEN,'unit_id':'unit-6',
 'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','student_release':False,
 'design_standard':'Science-bearing briefs only. No polished learner narrative prose at F3.',
 'counts':{'journeys':6,'scene_briefs':53,'palace_managed_records':161,'term_introductions':161,'optional_first_exposure_recalls':len(quick)},
 'scene_briefs':scene_briefs
}
journey_doc={'schema':'memory-palace-v2-unit6-journey-briefs-f3-1.0','generated_utc':GEN,'unit_id':'unit-6','journey_count':6,'student_release':False,'journeys':journey_briefs}
dump(BRIEFS/'scene-briefs-f3.json',scene_doc); dump(BRIEFS/'journey-briefs-f3.json',journey_doc)

status={
 'unit_id':'unit-6','number':6,'title':'Gene Expression and Regulation','status':'SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED',
 'pipeline_stage':'SCENE_BRIEFS_LOCKED_F3','canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3',
 'student_release':False,'preview_release':False,'journey_count':0,'scene_count':0,'memory_objects':0,'application_challenges':0,
 'canonical_records':202,'architecture_journeys':6,'architecture_loci':53,'scene_briefs':53,'palace_managed_records':161,
 'challenge_lab_records':16,'scope_guard_records':25,'exact_name_review_targets':134,'confusable_sets':37,'optional_first_exposure_recalls':len(quick),
 'next_required_output':'F4A polished narrative for Journey 1 only, generated strictly from the locked F3 briefs and subjected to prose-level spatial/scientific QA before Journey 2 is written.'
}
dump(U6/'status-f3.json',status); dump(U6/'status.json',status)

# Preserve exact F1 and F2 files and lock new F3 files.
f3_files=[
 'content/ap-biology/unit-6/briefs/journey-briefs-f3.json','content/ap-biology/unit-6/briefs/scene-briefs-f3.json',
 'content/ap-biology/unit-6/status-f3.json'
]
f1=read(U6/'content-lock-f1.json'); f2lock=read(U6/'content-lock-f2.json')
lock={
 'schema':'memory-palace-v2-unit6-content-lock-f3-1.0','generated_utc':GEN,'unit_id':'unit-6','lock_status':'LOCKED_F3','student_release':False,
 'f1_protected_hashes':{str((U6/p).relative_to(ROOT)):sha(U6/p) for p in ['source/canonical-unit6-f1.json','source/coverage-manifest-f1.json','content-lock-f1.json','f1-release-manifest.json']},
 'f2_protected_hashes':{str((U6/p).relative_to(ROOT)):sha(U6/p) for p in ['architecture/learning-classification-f2.json','architecture/palace-architecture-f2.json','content-lock-f2.json','f2-release-manifest.json','status-f2.json']},
 'files':{rel:{'bytes':(ROOT/rel).stat().st_size,'sha256':sha(ROOT/rel)} for rel in f3_files},
 'policy':'F3 locks science-bearing journey and scene briefs while leaving F1 science and F2 learning architecture unchanged. F4 may write polished story prose only from these briefs and may not alter protected earlier locks.'
}
dump(U6/'content-lock-f3.json',lock)

release={
 'schema':'memory-palace-v2-unit6-f3-release-1.0','generated_utc':GEN,'unit_id':'unit-6','release_status':'SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','student_release':False,
 'canonical_records':202,'palace_managed_records':161,'journey_briefs':6,'scene_briefs':53,'term_introductions':161,'optional_first_exposure_recalls':len(quick),
 'challenge_lab_records':16,'scope_guard_records':25,'exact_name_review_targets':134,'confusable_sets':37,
 'polished_story_files':0,'student_runtime_memory_objects':0,'student_runtime_journeys':0,'student_runtime_scenes':0,
 'next_gate':'F4A Journey 1 only: polished narrative prose from U6-J1 briefs, with spatial clarity, recurring scientific cast, causal continuity, exact-term integration, and science-lock QA.'
}
dump(U6/'f3-release-manifest.json',release)

# Development course registry only; no student runtime.
course_path=ROOT/'content/ap-biology'/'course.json'; course=read(course_path); e=next(u for u in course['units'] if u['unit_id']=='unit-6')
e.update({'status':'SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','journey_count':0,'scene_count':0,'canonical_lock':'LOCKED_F1','source_status':'AUDITED_F1_ARCHITECTURE_F2_BRIEFS_F3','student_release':False,'architecture_journeys':6,'architecture_loci':53,'architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','scene_briefs':53,'optional_first_exposure_recalls':len(quick)})
dump(course_path,course)

print('UNIT 6 F3 BUILD PASS')
print(scene_doc['counts'])
