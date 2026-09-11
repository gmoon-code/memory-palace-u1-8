from __future__ import annotations
import json,hashlib
from pathlib import Path
from collections import Counter,defaultdict

ROOT=Path(__file__).resolve().parents[1]
U6=ROOT/'content'/'ap-biology'/'unit-6'
SRC=U6/'source'/'canonical-unit6-f1.json'
ARCH=U6/'architecture'; ARCH.mkdir(parents=True,exist_ok=True)
GENERATED_UTC='2026-09-07T01:00:00+00:00'

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,obj): Path(p).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# locus_id, journey_id, bundle_id, title, micro_anchor, [left,center,right], primary, all ids, visual_mode
RAW_LOCI=[
('U6-L01','U6-J1','U6-B01','Hereditary Information Intake','the archive intake where DNA and RNA are filed as hereditary information while the discovery evidence remains contextual rather than becoming the main memorization target',['Franklin / Chargaff evidence panel','DNA/RNA hereditary-information registry','historical model-building context'],'U6-K-001',['U6-K-001','U6-K-090','U6-K-093'],'HEREDITARY_INFORMATION_EVIDENCE_ARCHIVE'),
('U6-L02','U6-J1','U6-B01','Chromosome Storage Gallery','the storage gallery separating typical prokaryotic circular chromosomes, eukaryotic linear chromosomes, and condensation states',['prokaryotic circular chromosome bay','chromosome-form comparison platform','eukaryotic linear / condensed chromosome bay'],'U6-K-002',['U6-K-002','U6-K-003','U6-K-004'],'CHROMOSOME_FORM_CONDENSATION_COMPARISON'),
('U6-L03','U6-J1','U6-B01','Plasmid Ring Vault','the small-ring vault where plasmids replicate independently, carry conditionally useful genes, and can be engineered or transferred',['independent plasmid replication rack','plasmid identity / recombinant ring bench','gene-transfer and conditional-value display'],'U6-K-005',['U6-K-005','U6-K-096','U6-K-097','U6-K-098','U6-K-099'],'PLASMID_IDENTITY_REPLICATION_TRANSFER'),
('U6-L04','U6-J1','U6-B02','Base-Class Reading Table','the base table sorting purines and pyrimidines while Chargaff relationships constrain complementary pairing',['purine two-ring drawer','base-class / composition comparison table','pyrimidine one-ring drawer'],'U6-K-006',['U6-K-006','U6-K-007','U6-K-091'],'PURINE_PYRIMIDINE_CHARGAFF_TABLE'),
('U6-L05','U6-J1','U6-B02','Antiparallel Pairing Bridge','the double-strand bridge reconnecting 5′/3′ directionality, antiparallel geometry, complementary pairing, and typical DNA/RNA architecture',['5′/3′ backbone direction rail','antiparallel complementary-pair bridge','DNA-versus-RNA architecture panel'],'U6-K-008',['U6-K-008','U6-K-092','U6-K-094','U6-K-095','U6-K-100'],'ANTIPARALLEL_BASE_PAIRING_REACTIVATION'),
('U6-L06','U6-J1','U6-B03','Replication Continuity Gate','the entry gate linking S phase and DNA copying to hereditary continuity before the fork machinery begins',['S-phase reactivation marker','replication-preserves-information gate','daughter-DNA destination'],'U6-K-009',['U6-K-009','U6-K-101'],'REPLICATION_CONTINUITY_S_PHASE'),
('U6-L07','U6-J1','U6-B03','Replication Model Test Chamber','the evidence chamber comparing conservative, semiconservative, and dispersive predictions against the Meselson–Stahl result',['conservative / dispersive model panels','semiconservative model and evidence bench','Meselson–Stahl isotope outcome display'],'U6-K-011',['U6-K-011','U6-K-102','U6-K-103','U6-K-104'],'REPLICATION_MODEL_EVIDENCE_DISCRIMINATION'),
('U6-L08','U6-J1','U6-B04','Origin and Fork Launch','the launch platform where replication begins at origins, helicase opens the duplex, topoisomerase relieves twisting, and the fork becomes visible',['origin / topoisomerase side','replication-fork opening platform','helicase and exposed-template side'],'U6-K-012',['U6-K-012','U6-K-013','U6-K-105','U6-K-106'],'ORIGIN_HELICASE_TOPOISOMERASE_FORK'),
('U6-L09','U6-J1','U6-B04','Primer–Polymerase Dock','the synthesis dock where exposed templates are stabilized, primase supplies RNA primers, and DNA polymerase extends only from a primer in the allowed direction',['single-strand stabilization / primase side','RNA-primer and DNA-polymerase dock','template movement / synthesis-direction rail'],'U6-K-014',['U6-K-014','U6-K-107','U6-K-108','U6-K-109'],'PRIMER_POLYMERASE_SYNTHESIS_DOCK'),
('U6-L10','U6-J1','U6-B04','Leading–Lagging Split Track','the fork track separating continuous leading-strand synthesis from discontinuous lagging-strand synthesis and Okazaki fragments',['continuous leading track','5′→3′ synthesis-direction divider','lagging track with Okazaki fragments'],'U6-K-015',['U6-K-010','U6-K-015','U6-K-110'],'LEADING_LAGGING_DIRECTIONAL_FORK'),
('U6-L11','U6-J1','U6-B05','Fragment Joining and Repair Bench','the post-fork bench where primer replacement is contextual, ligase seals lagging-strand fragments, and proofreading/repair preserve sequence accuracy',['primer-replacement / proofreading side','ligase fragment-joining bench','mismatch / excision-repair overview'],'U6-K-016',['U6-K-016','U6-K-111','U6-K-114','U6-K-115'],'LIGASE_PROOFREADING_REPAIR_BENCH'),
('U6-L12','U6-J1','U6-B05','Chromosome-End Dock','the chromosome-end dock distinguishing telomeres from telomerase while keeping the detailed end-replication mechanism as enrichment',['telomere protective end','chromosome-end maintenance dock','telomerase extension tool'],'U6-K-112',['U6-K-112','U6-K-113'],'TELOMERE_TELOMERASE_END_DOCK'),

('U6-L13','U6-J2','U6-B06','RNA Function Desk','the RNA desk where sequence and structure are tied to RNA function and mRNA, tRNA, and rRNA receive distinct jobs',['mRNA message lane','RNA sequence/structure function desk','rRNA ribosome-component lane'],'U6-K-018',['U6-K-018','U6-K-019','U6-K-023'],'RNA_FUNCTION_MRNA_RRNA'),
('U6-L14','U6-J2','U6-B06','tRNA Courier Bay','the courier bay where each tRNA carries a specific amino acid, pairs its anticodon with mRNA, and is recruited during translation',['amino-acid attachment side','tRNA anticodon courier','mRNA pairing / recruitment side'],'U6-K-020',['U6-K-020','U6-K-021','U6-K-022'],'TRNA_AMINO_ACID_ANTICODON_COURIER'),
('U6-L15','U6-J2','U6-B07','Gene Expression Junction','the junction separating transcription from translation while reactivating protein structure as the downstream functional destination',['transcription DNA→RNA lane','gene-expression junction','translation RNA→polypeptide lane'],'U6-K-117',['U6-K-116','U6-K-117','U6-K-118','U6-K-119'],'GENE_EXPRESSION_TRANSCRIPTION_TRANSLATION'),
('U6-L16','U6-J2','U6-B07','Template–Promoter Entry Gate','the transcription entry gate where one DNA template strand is distinguished from the opposite strand and promoter/TATA context is placed before transcription begins',['template-strand selection side','promoter entry gate','TATA-box contextual panel'],'U6-K-024',['U6-K-024','U6-K-120','U6-K-123','U6-K-124'],'TEMPLATE_PROMOTER_INITIATION_GATE'),
('U6-L17','U6-J2','U6-B07','Transcription Direction Rail','the rail that locks RNA synthesis direction to the template orientation and carries initiation, elongation, and termination in sequence',['initiation station','template 3′→5′ / RNA 5′→3′ rail','elongation and termination stations'],'U6-K-025',['U6-K-025','U6-K-122','U6-K-125'],'TRANSCRIPTION_DIRECTION_SEQUENCE'),
('U6-L18','U6-J2','U6-B08','Prokaryotic Transcript Exit','the prokaryotic exit showing why a transcript can become usable without the eukaryotic nucleus-based processing route',['DNA transcription area','usable prokaryotic transcript exit','ribosome-access side'],'U6-K-126',['U6-K-126'],'PROKARYOTIC_TRANSCRIPT_USABILITY'),
('U6-L19','U6-J2','U6-B08','Pre-mRNA Processing Counter','the eukaryotic processing counter where pre-mRNA receives a 5′ cap and poly-A tail before export',['5′ cap / recognition side','pre-mRNA processing counter','poly-A tail / stability side'],'U6-K-026',['U6-K-026','U6-K-027','U6-K-028','U6-K-127','U6-K-128'],'PREMRNA_CAP_POLYA_PROCESSING'),
('U6-L20','U6-J2','U6-B08','Splice and Isoform Chamber','the chamber where introns are removed, exons are joined, alternative splicing changes exon combinations, and mature mRNA exits',['intron excision side','exon-splicing / alternative-splicing chamber','mature-mRNA exit'],'U6-K-029',['U6-K-029','U6-K-030','U6-K-129'],'INTRON_EXON_ALTERNATIVE_SPLICING'),

('U6-L21','U6-J3','U6-B09','Translation Geography Platform','the platform contrasting eukaryotic translation location with coupled transcription–translation in prokaryotes',['eukaryotic cytosolic/rough-ER ribosome side','translation-location comparison platform','prokaryotic coupled-transcription/translation side'],'U6-K-031',['U6-K-031','U6-K-032'],'PROK_EUK_TRANSLATION_LOCATION'),
('U6-L22','U6-J3','U6-B09','Reading-Frame Start Gate','the start gate that establishes a reading frame at AUG and launches the initiation–elongation–termination sequence',['reading-frame alignment side','AUG start gate','translation-stage route'],'U6-K-034',['U6-K-033','U6-K-034','U6-K-121'],'READING_FRAME_AUG_START'),
('U6-L23','U6-J3','U6-B10','Codon Code Wall','the code wall linking triplet codons to amino acids while showing redundancy and near universality without requiring code-table memorization',['codon triplet examples','codon-to-amino-acid mapping wall','redundancy / near-universality display'],'U6-K-035',['U6-K-035','U6-K-036','U6-K-037','U6-K-038'],'CODON_CODE_REDUNDANCY_UNIVERSALITY'),
('U6-L24','U6-J3','U6-B10','tRNA Charging Dock','the dock where aminoacyl-tRNA synthetase links the correct amino acid to tRNA before the charged tRNA delivers that amino acid to the ribosome',['amino acid / synthetase side','tRNA charging dock','charged-tRNA delivery route'],'U6-K-039',['U6-K-039','U6-K-130'],'TRNA_CHARGING_DELIVERY'),
('U6-L25','U6-J3','U6-B10','Ribosome A–P–E Platform','the ribosome platform locating tRNAs at A, P, and E sites while corrected subunit-size values remain teacher enrichment',['A-site entry','P-site peptide / ribosome platform','E-site exit / subunit-size context'],'U6-K-132',['U6-K-131','U6-K-132'],'RIBOSOME_APE_SITES'),
('U6-L26','U6-J3','U6-B11','Polypeptide Elongation Conveyor','the conveyor where codon recognition, peptide-bond growth, and translocation repeat to lengthen the polypeptide',['incoming codon–anticodon match','polypeptide elongation conveyor','translocation to next codon'],'U6-K-040',['U6-K-040','U6-K-133'],'TRANSLATION_ELONGATION_TRANSLOCATION'),
('U6-L27','U6-J3','U6-B11','Stop and Release Dock','the termination dock where a stop codon ends translation, the product is released, and protein folding continues afterward',['stop-codon arrival','termination / product-release dock','post-translation folding side'],'U6-K-041',['U6-K-041','U6-K-042','U6-K-134','U6-K-135'],'STOP_CODON_TERMINATION_RELEASE'),
('U6-L28','U6-J3','U6-B11','Retroviral Reverse-Flow Gate','the exception gate where reverse transcriptase copies retroviral RNA into DNA before that DNA can integrate into a host genome',['retroviral RNA input','reverse-transcription gate','DNA product toward host-genome integration'],'U6-K-045',['U6-K-045'],'RETROVIRAL_REVERSE_TRANSCRIPTION'),

('U6-L29','U6-J4','U6-B12','Expression Control Room','the control room where regulatory DNA and proteins determine constitutive versus inducible output instead of treating every gene as always on',['constitutive-expression channel','regulatory DNA/protein control room','inducible-expression channel'],'U6-K-046',['U6-K-046','U6-K-047'],'REGULATORY_DNA_CONSTITUTIVE_INDUCIBLE'),
('U6-L30','U6-J4','U6-B12','Operon Architecture Board','the bacterial control board separating promoter, operator, structural genes, and repressor protein while showing coordinated operon regulation',['promoter / operator inputs','operon architecture board','structural genes / coordinated output'],'U6-K-053',['U6-K-053','U6-K-136','U6-K-137','U6-K-138'],'OPERON_PROMOTER_OPERATOR_REPRESSOR'),
('U6-L31','U6-J4','U6-B13','trp Repressible Chamber','the feedback chamber where tryptophan binds the repressor as a corepressor and switches a repressible operon toward lower transcription',['low-tryptophan inactive-repressor side','trp operon repressible switch','tryptophan corepressor / active-repressor side'],'U6-K-140',['U6-K-139','U6-K-140','U6-K-141'],'TRP_REPRESSIBLE_COREPRESSOR'),
('U6-L32','U6-J4','U6-B13','lac Inducible Chamber','the inducible chamber where allolactose changes repressor behavior and permits lac-operon transcription when the substrate signal is present',['repressor-blocked operator side','lac operon inducible switch','allolactose inducer / structural-gene output side'],'U6-K-142',['U6-K-142','U6-K-143','U6-K-144'],'LAC_INDUCIBLE_ALLOLACTOSE'),
('U6-L33','U6-J4','U6-B14','Eukaryotic Regulation Layers','the layered control wall showing that eukaryotic gene expression can be coordinated at chromatin, transcriptional, RNA-processing, translational, and post-translational stages',['chromatin / transcription layer','multi-stage regulation stack','RNA / translation / post-translation layer'],'U6-K-054',['U6-K-054','U6-K-145'],'EUKARYOTIC_MULTI_STAGE_REGULATION'),
('U6-L34','U6-J4','U6-B14','Epigenetic Chromatin Room','the chromatin room connecting reversible DNA/histone modifications with gene-expression state while keeping their effects context dependent',['histone-acetylation side','reversible epigenetic chromatin state','DNA-methylation / inherited-state side'],'U6-K-048',['U6-K-048','U6-K-146','U6-K-147','U6-K-148'],'EPIGENETIC_HISTONE_DNA_METHYLATION'),
('U6-L35','U6-J4','U6-B15','Promoter–Enhancer Recruitment Hall','the regulatory hall where promoter and enhancer/control elements recruit transcription machinery from positions that may lie upstream, downstream, or within genes',['promoter / nearby control side','transcription-machinery recruitment hall','enhancer / distant-position side'],'U6-K-055',['U6-K-055','U6-K-056','U6-K-149'],'PROMOTER_ENHANCER_RECRUITMENT'),
('U6-L36','U6-J4','U6-B15','Activator–Repressor Balance Gate','the balance gate where positive and negative regulators change transcriptional output rather than simply labeling genes on or off',['activator / positive regulation side','transcriptional output balance','repressor / negative regulation side'],'U6-K-057',['U6-K-057'],'ACTIVATOR_REPRESSOR_NEGATIVE_REGULATION'),
('U6-L37','U6-J4','U6-B15','RNA-Level Regulation Suite','the RNA regulation suite where alternative splicing and small RNAs such as miRNA/siRNA change which messages persist or are used',['alternative-splicing side','RNA-level regulation suite','miRNA / siRNA small-RNA side'],'U6-K-059',['U6-K-059','U6-K-150','U6-K-151'],'SMALL_RNA_ALTERNATIVE_SPLICING_REGULATION'),
('U6-L38','U6-J4','U6-B16','Expression Profile Console','the console connecting gene-expression profiles and gene-product amount/function to phenotype',['gene-product amount / function input','expression-profile phenotype console','phenotypic output'],'U6-K-049',['U6-K-049','U6-K-052'],'GENE_EXPRESSION_PROFILE_PHENOTYPE'),
('U6-L39','U6-J4','U6-B16','Cell Specialization Gallery','the gallery where differential gene expression produces tissue-specific proteins and differentiated cell identities',['shared genome / inactive genes side','differential-expression specialization gallery','tissue-specific protein / cell-identity side'],'U6-K-058',['U6-K-050','U6-K-058','U6-K-152'],'DIFFERENTIAL_EXPRESSION_CELL_DIFFERENTIATION'),
('U6-L40','U6-J4','U6-B16','Developmental Sequence Hall','the developmental hall where sequential gene expression is linked with morphogenesis, cytoplasmic determinants, induction, pattern formation, homeotic genes, and apoptosis as teacher-enrichment mechanisms',['early determinants / induction side','sequential developmental gene-expression route','patterning / morphogenesis / apoptosis side'],'U6-K-051',['U6-K-051','U6-K-153','U6-K-154','U6-K-155','U6-K-156','U6-K-157'],'DEVELOPMENTAL_GENE_EXPRESSION_SEQUENCE'),

('U6-L41','U6-J5','U6-B17','Mutation Consequence Desk','the triage desk where a DNA change is interpreted through its molecular consequence, environmental context, and possible connection from genotype to phenotype and selection',['molecular-change input','mutation-consequence triage desk','phenotype / environment / selection output'],'U6-K-060',['U6-K-060','U6-K-067','U6-K-074'],'MUTATION_CONSEQUENCE_CONTEXT_SELECTION'),
('U6-L42','U6-J5','U6-B17','Substitution Sorter','the sorter comparing point substitution outcomes including silent, missense, and nonsense changes without assuming every substitution has the same effect',['silent / missense lanes','point-substitution sorter','nonsense / altered-protein lane'],'U6-K-061',['U6-K-061','U6-K-063','U6-K-064','U6-K-158'],'SUBSTITUTION_SILENT_MISSENSE_NONSENSE'),
('U6-L43','U6-J5','U6-B17','Frameshift Reading Track','the reading track where insertion/deletion changes the downstream reading frame when the net change is not a multiple of three',['original reading frame','insertion/deletion frameshift point','shifted downstream codons'],'U6-K-062',['U6-K-062'],'FRAMESHIFT_READING_FRAME'),
('U6-L44','U6-J5','U6-B18','Mutation Source and Variation Yard','the yard connecting replication errors and mutagens to random DNA change, then placing mutation alongside conserved reproductive processes as sources of variation',['replication-error / mutagen inputs','mutation-to-variation yard','meiosis / recombination / fertilization variation sources'],'U6-K-066',['U6-K-066','U6-K-068','U6-K-080'],'MUTATION_VARIATION_SOURCES'),
('U6-L45','U6-J5','U6-B18','Chromosome Number Error Bay','the bay where cell-division errors such as nondisjunction alter chromosome number and can disrupt phenotype or development',['normal segregation side','nondisjunction / chromosome-number error bay','aneuploid developmental-effect side'],'U6-K-070',['U6-K-069','U6-K-070','U6-K-071','U6-K-163'],'NONDISJUNCTION_CHROMOSOME_NUMBER_EFFECT'),
('U6-L46','U6-J5','U6-B18','Chromosome Rearrangement Garage','the garage sorting deletion, duplication, inversion, and translocation as structural chromosome alterations',['deletion / duplication bays','chromosome-structure alteration garage','inversion / translocation bays'],'U6-K-072',['U6-K-072','U6-K-159','U6-K-160','U6-K-161','U6-K-162'],'CHROMOSOME_REARRANGEMENT_TYPES'),
('U6-L47','U6-J5','U6-B19','Horizontal Gene Transfer Hub','the microbial transfer hub distinguishing transformation, transduction, and conjugation as routes of horizontal gene transfer',['transformation uptake route','horizontal-gene-transfer hub','transduction / conjugation routes'],'U6-K-075',['U6-K-075','U6-K-076','U6-K-077','U6-K-164'],'HORIZONTAL_GENE_TRANSFER_MODES'),
('U6-L48','U6-J5','U6-B19','Mobile DNA and Viral Recombination Yard','the yard where transposable elements move within genomes and coinfecting viruses can recombine genetic material',['transposition / mobile-element side','genetic-rearrangement yard','viral coinfection / recombination side'],'U6-K-078',['U6-K-078','U6-K-079'],'TRANSPOSITION_VIRAL_RECOMBINATION'),

('U6-L49','U6-J6','U6-B20','Genetic Engineering Intake','the laboratory intake defining genetic engineering as purposeful manipulation or analysis of nucleic acids before individual techniques are chosen',['DNA manipulation tools','genetic-engineering intake bench','analysis / comparison tools'],'U6-K-081',['U6-K-081'],'GENETIC_ENGINEERING_SCOPE'),
('U6-L50','U6-J6','U6-B20','Gel Electrophoresis Lane','the gel lane where charged DNA fragments migrate through a matrix and produce band patterns used for comparison',['sample wells / DNA loading side','gel migration lane','separated band-pattern side'],'U6-K-082',['U6-K-082','U6-K-167'],'GEL_ELECTROPHORESIS_MIGRATION'),
('U6-L51','U6-J6','U6-B21','PCR Thermal Cycler','the thermal cycler repeating denaturation, primer annealing, and extension to amplify a selected DNA region',['denaturation high-temperature side','primer-annealing stage','extension / amplified-copy output'],'U6-K-083',['U6-K-083','U6-K-084','U6-K-085','U6-K-166'],'PCR_THREE_STAGE_AMPLIFICATION'),
('U6-L52','U6-J6','U6-B21','Transformation Expression Bench','the bacterial bench connecting uptake of engineered DNA with recombinant expression while distinguishing laboratory transformation from natural HGT context',['engineered plasmid / bacterial uptake side','transformation bench','recombinant gene-expression output'],'U6-K-086',['U6-K-086','U6-K-165'],'BACTERIAL_TRANSFORMATION_RECOMBINANT_EXPRESSION'),
('U6-L53','U6-J6','U6-B21','Sequence and Profile Analysis Desk','the analysis desk where DNA sequencing determines nucleotide order and DNA profiles compare patterns among samples',['DNA sequence readout','sequence/profile analysis desk','profile/fingerprint comparison panel'],'U6-K-087',['U6-K-087','U6-K-088'],'DNA_SEQUENCING_PROFILE_COMPARISON'),
]

JOURNEYS=[
('U6-J1','Genome Archive and Replication Works','6.1–6.2','DNA/RNA information architecture, chromosome/plasmid organization, replication evidence, fork mechanics, synthesis direction, and chromosome-end maintenance','An archive transitions into a copying works: hereditary information is stored first, then duplicated through a physically directional production line without turning extra enzyme names into AP requirements',[('U6-B01','Hereditary information, chromosome forms, and plasmids',['U6-L01','U6-L02','U6-L03']),('U6-B02','Base classes and nucleic-acid structural reactivation',['U6-L04','U6-L05']),('U6-B03','Replication purpose and evidence',['U6-L06','U6-L07']),('U6-B04','Replication fork mechanics and direction',['U6-L08','U6-L09','U6-L10']),('U6-B05','Joining, repair, and chromosome ends',['U6-L11','U6-L12'])]),
('U6-J2','RNA Transcript Workshop','6.3','RNA roles, gene expression, transcription, promoter/template logic, directionality, pre-mRNA processing, and alternative splicing','A transcript workshop follows information from a selected DNA template through RNA synthesis and eukaryotic processing while keeping prokaryotic transcript use distinct',[('U6-B06','RNA identities and tRNA function',['U6-L13','U6-L14']),('U6-B07','Gene expression and transcription mechanics',['U6-L15','U6-L16','U6-L17']),('U6-B08','Transcript use and eukaryotic RNA processing',['U6-L18','U6-L19','U6-L20'])]),
('U6-J3','Translation Assembly Hall','6.4','Translation location, reading frames, codons, tRNA charging, ribosome operation, elongation, termination, and reverse transcription','A protein-assembly hall turns a readable mRNA message into a polypeptide through ordered ribosome stations, then places retroviral reverse transcription in a clearly separate exception gate',[('U6-B09','Translation geography and initiation',['U6-L21','U6-L22']),('U6-B10','Genetic code, tRNA, and ribosome organization',['U6-L23','U6-L24','U6-L25']),('U6-B11','Elongation, termination, and reverse information flow',['U6-L26','U6-L27','U6-L28'])]),
('U6-J4','Gene Control and Differentiation Center','6.5–6.6','Prokaryotic operons, eukaryotic regulation, epigenetics, promoters/enhancers, small RNA, gene-expression profiles, specialization, and development','A control center compares bacterial switch logic with multi-layer eukaryotic regulation, then follows differential expression into specialized cell identities and developmental sequences',[('U6-B12','Gene-expression control and operon architecture',['U6-L29','U6-L30']),('U6-B13','Repressible and inducible operon models',['U6-L31','U6-L32']),('U6-B14','Eukaryotic regulation and epigenetics',['U6-L33','U6-L34']),('U6-B15','Regulatory DNA, transcription factors, and RNA-level control',['U6-L35','U6-L36','U6-L37']),('U6-B16','Expression profiles, specialization, and development',['U6-L38','U6-L39','U6-L40'])]),
('U6-J5','Mutation and Gene Exchange Yard','6.7','Mutation consequences, substitution and frameshift types, mutation sources, chromosome-number and structural changes, HGT, transposition, and viral recombination','A diagnostic yard first classifies DNA and chromosome changes by mechanism and consequence, then opens into microbial and viral transfer routes that create new genetic combinations',[('U6-B17','Sequence-level mutation consequences',['U6-L41','U6-L42','U6-L43']),('U6-B18','Mutation sources and chromosome-scale change',['U6-L44','U6-L45','U6-L46']),('U6-B19','Horizontal transfer and mobile/recombined DNA',['U6-L47','U6-L48'])]),
('U6-J6','Biotechnology Investigation Lab','6.8','Genetic engineering, gel electrophoresis, PCR, bacterial transformation, sequencing, and DNA-profile comparison','An investigation laboratory chooses biotechnology tools by function: amplify, separate, transform, sequence, or compare nucleic acids, keeping technique details tied to what the method accomplishes',[('U6-B20','Genetic engineering and DNA separation',['U6-L49','U6-L50']),('U6-B21','Amplification, transformation, sequencing, and comparison',['U6-L51','U6-L52','U6-L53'])]),
]

CONFUSABLES=[
('U6-D01','DNA versus RNA architecture',['U6-K-001','U6-K-100','U6-K-094','U6-K-095']),
('U6-D02','Purines versus pyrimidines',['U6-K-006','U6-K-007']),
('U6-D03','Chromosome versus plasmid',['U6-K-002','U6-K-003','U6-K-005']),
('U6-D04','Complementary base pairing versus backbone direction',['U6-K-008','U6-K-094','U6-K-095']),
('U6-D05','Conservative versus semiconservative versus dispersive replication',['U6-K-011','U6-K-102','U6-K-103']),
('U6-D06','Helicase versus topoisomerase versus ligase',['U6-K-012','U6-K-013','U6-K-016']),
('U6-D07','Primase versus DNA polymerase',['U6-K-014','U6-K-108']),
('U6-D08','Leading versus lagging strand',['U6-K-015','U6-K-110']),
('U6-D09','Telomere versus telomerase',['U6-K-112','U6-K-113']),
('U6-D10','Transcription versus translation',['U6-K-118','U6-K-119']),
('U6-D11','mRNA versus tRNA versus rRNA',['U6-K-019','U6-K-020','U6-K-023']),
('U6-D12','Template strand versus transcript direction',['U6-K-024','U6-K-025','U6-K-120']),
('U6-D13','Promoter versus TATA box',['U6-K-123','U6-K-124']),
('U6-D14','5′ cap versus poly-A tail',['U6-K-027','U6-K-028']),
('U6-D15','Intron versus exon/spliced product',['U6-K-029','U6-K-030','U6-K-129']),
('U6-D16','Codon versus anticodon',['U6-K-035','U6-K-021']),
('U6-D17','Start codon versus stop codon',['U6-K-034','U6-K-041']),
('U6-D18','Reading frame versus codon',['U6-K-121','U6-K-035']),
('U6-D19','Ribosomal A versus P versus E sites',['U6-K-132','U6-K-039','U6-K-040']),
('U6-D20','Prokaryotic versus eukaryotic expression geography',['U6-K-031','U6-K-032','U6-K-126']),
('U6-D21','Operon promoter versus operator versus structural genes',['U6-K-136','U6-K-137','U6-K-138']),
('U6-D22','trp repressible versus lac inducible operon',['U6-K-140','U6-K-142']),
('U6-D23','Corepressor versus inducer',['U6-K-141','U6-K-143']),
('U6-D24','Histone acetylation versus DNA methylation',['U6-K-146','U6-K-147']),
('U6-D25','Activator versus repressor / positive versus negative regulation',['U6-K-055','U6-K-057','U6-K-149']),
('U6-D26','microRNA versus siRNA / small-RNA regulation',['U6-K-059','U6-K-151']),
('U6-D27','Differentiation versus morphogenesis',['U6-K-152','U6-K-153']),
('U6-D28','Point substitution outcomes',['U6-K-061','U6-K-063','U6-K-064','U6-K-158']),
('U6-D29','Point substitution versus frameshift',['U6-K-061','U6-K-062']),
('U6-D30','Chromosomal deletion, duplication, inversion, translocation',['U6-K-159','U6-K-160','U6-K-161','U6-K-162']),
('U6-D31','Nondisjunction versus structural chromosome alteration',['U6-K-070','U6-K-072']),
('U6-D32','Transformation versus transduction versus conjugation',['U6-K-075','U6-K-076','U6-K-077']),
('U6-D33','Transposition versus viral recombination',['U6-K-078','U6-K-079']),
('U6-D34','Natural transformation versus biotechnology transformation',['U6-K-075','U6-K-086']),
('U6-D35','PCR stages',['U6-K-083','U6-K-084','U6-K-085']),
('U6-D36','PCR versus gel electrophoresis versus sequencing',['U6-K-082','U6-K-083','U6-K-087']),
('U6-D37','DNA sequence versus DNA profile',['U6-K-087','U6-K-088']),
]

src=load(SRC); recs=src['canonical_catalog']; byid={r['knowledge_id']:r for r in recs}
all_ids={r['knowledge_id'] for r in recs}
practice=[r for r in recs if r['scope_class']=='PRACTICE_ONLY']
scope=[r for r in recs if r['scope_class']=='SCOPE_GUARD']
palace_expected=all_ids-{r['knowledge_id'] for r in practice}-{r['knowledge_id'] for r in scope}

# validate loci partition
seen=[]
for row in RAW_LOCI:
    seen.extend(row[7])
assert len(seen)==len(set(seen)), [x for x,c in Counter(seen).items() if c>1]
assert set(seen)==palace_expected, {'missing':sorted(palace_expected-set(seen)),'extra':sorted(set(seen)-palace_expected)}

loci=[]; kid_to_locus={}
for locus_id,jid,bid,title,micro,zones,primary,kids,visual in RAW_LOCI:
    assert len(zones)==3 and primary in kids
    for k in kids:kid_to_locus[k]=locus_id
    loci.append({'locus_id':locus_id,'journey_id':jid,'bundle_id':bid,'title':title,'micro_anchor':micro,
      'scene_geometry':{'left':zones[0],'center':zones[1],'right':zones[2]},'primary_knowledge_id':primary,
      'knowledge_ids':kids,'embedded_knowledge_ids':[k for k in kids if k!=primary], 'visual_mode':visual,
      'scientific_visual_required':True,'narrative_status':'ARCHITECTURE_ONLY_NO_STORY_PROSE_F2'})

journeys=[]; bundles=[]
for jid,title,topics,focus,logic,bundlespec in JOURNEYS:
    bs=[]
    for bid,btitle,locids in bundlespec:
        b={'bundle_id':bid,'title':btitle,'loci':locids}; bs.append(b); bundles.append({'journey_id':jid,**b})
    journeys.append({'journey_id':jid,'working_title':title,'topics':topics,'content_focus':focus,'setting_logic':logic,'bundles':bs})

# challenge prerequisites by topic + specific loci
challenge_prereq={
'U6-K-168':['U6-L04','U6-L05'],'U6-K-169':['U6-L04','U6-L05'],'U6-K-170':['U6-L03'],
'U6-K-171':['U6-L05','U6-L10'],'U6-K-172':['U6-L08','U6-L09','U6-L10','U6-L11'],
'U6-K-173':['U6-L16','U6-L17'],'U6-K-174':['U6-L22','U6-L23','U6-L24'],
'U6-K-175':['U6-L16','U6-L17'],'U6-K-176':['U6-L21','U6-L23','U6-L24','U6-L25'],
'U6-K-177':['U6-L15','U6-L17','U6-L20','U6-L22','U6-L27'],'U6-K-178':['U6-L21'],
'U6-K-179':['U6-L31','U6-L32'],'U6-K-180':['U6-L42','U6-L43','U6-L46'],
'U6-K-181':['U6-L50'],'U6-K-182':['U6-L51'],'U6-K-183':['U6-L53']}
challenge=[{'knowledge_id':r['knowledge_id'],'canonical_label':r['canonical_label'],'topic':r['topic'],'retrieval_demand':r['retrieval_demand'],
            'prerequisite_loci':challenge_prereq[r['knowledge_id']], 'runtime_status':'ARCHITECTURE_ONLY_NO_TASK_PROSE_F2'} for r in practice]

confusable=[]
for sid,title,kids in CONFUSABLES:
    assert set(kids)<=palace_expected
    confusable.append({'set_id':sid,'title':title,'knowledge_ids':kids,'terms':[byid[k]['canonical_label'] for k in kids],
                       'release_policy':'BUILD_MIXED_DISCRIMINATION_AFTER_STORY_EXPOSURE'})

# classification
hard_sound_tokens=('topoisomerase','pyrimidine','purine','helicase','ligase','plasmid','telomerase','aminoacyl','operon','allolactose','transduction','conjugation','transposition','electrophoresis','morphogenesis','apoptosis','polyadenylation')
records=[]
primary_ids={l['primary_knowledge_id'] for l in loci}
conf_by=defaultdict(list)
for c in confusable:
    for k in c['knowledge_ids']: conf_by[k].append(c['set_id'])
for r in recs:
    k=r['knowledge_id']; exact=bool(r['exact_name_recall'])
    if r['scope_class']=='PRACTICE_ONLY':
        dest='CHALLENGE_LAB'; locus=None; role='APPLICATION_ONLY'; visual='APPLICATION_OR_DATA_MODEL'
    elif r['scope_class']=='SCOPE_GUARD':
        dest='SUPPORTING_NON_RUNTIME_SCOPE_GUARD'; locus=None; role='SCOPE_BOUNDARY'; visual='NO_PERMANENT_MNEMONIC'
    else:
        locus=kid_to_locus[k]; dest='PALACE_PRIMARY_LOCUS' if k in primary_ids else 'PALACE_EMBEDDED'; role='PRIMARY_ANCHOR' if k in primary_ids else ('PREREQUISITE_REACTIVATION' if r['retrieval_demand']=='PREREQUISITE_RECALL' else ('TEACHER_ENRICHMENT_SUPPORT' if r['scope_class']=='TEACHER_REQUIRED_ENRICHMENT' else 'EMBEDDED_SCIENCE'))
        visual=next(x['visual_mode'] for x in loci if x['locus_id']==locus)
    if not exact: name='NO_EXACT_NAME_GATE'
    elif any(t in r['canonical_label'].lower() for t in hard_sound_tokens): name='PHONOLOGICAL_SUPPORT_RECOMMENDED_IF_NEEDED'
    elif r['scope_class']=='TEACHER_REQUIRED_ENRICHMENT': name='SEMANTIC_PLUS_OPTIONAL_SOUND_CUE'
    else: name='SEMANTIC_SCIENCE_CUE_SUFFICIENT'
    retrieval=[]
    if exact and r['scope_class'] not in ('PRACTICE_ONLY','SCOPE_GUARD'): retrieval.append('EXACT_NAME_FROM_SCIENTIFIC_ROLE')
    if r['scope_class'] not in ('PRACTICE_ONLY','SCOPE_GUARD'): retrieval += ['MEANING_OR_MECHANISM','MODEL_OR_CAUSAL_INTERPRETATION']
    elif r['scope_class']=='PRACTICE_ONLY': retrieval=['NOVEL_APPLICATION_OR_DATA_REASONING']
    else: retrieval=['SCOPE_BOUNDARY_ONLY']
    records.append({'knowledge_id':k,'canonical_label':r['canonical_label'],'topic':r['topic'],'scope_class':r['scope_class'],
      'destination':dest,'locus_id':locus,'scene_role':role,'visual_mode':visual,'exact_name_recall':exact,
      'delayed_review_target': bool(exact and r['scope_class'] not in ('PRACTICE_ONLY','SCOPE_GUARD')),
      'reactivation_mode':'PRIOR_UNIT_REACTIVATION' if r['retrieval_demand']=='PREREQUISITE_RECALL' else 'NEW_OR_EXTENDED_UNIT6_LEARNING',
      'name_support':name,'spelling_policy':'ADAPTIVE_SUPPORT_ONLY_NO_MANDATORY_SPELLING_GATE',
      'retrieval_modes':retrieval,'discrimination_sets':conf_by.get(k,[]),'canonical_lock':'LOCKED_F1',
      'review_flag_ids':r.get('review_flag_ids',[])})

bydest=Counter(x['destination'] for x in records); byname=Counter(x['name_support'] for x in records)
classification={'schema':'memory-palace-v2-unit6-f2-learning-classification-1.0','generated_utc':GENERATED_UTC,'unit_id':'unit-6',
 'canonical_source_lock':'canonical-unit6-f1.json','policy':{
  'palace':'Permanent loci carry durable scientific identities, mechanisms, directional relationships, visual models, and teacher-required content that belongs to the taught Unit 6 corpus.',
  'prerequisite_reactivation':'Prior-unit concepts are reactivated inside an appropriate Unit 6 locus and are not given duplicate standalone palaces.',
  'challenge_lab':'Calculations, strand conversion, codon-chart use, FRQ synthesis, visual analysis, and other transfer procedures remain outside permanent loci.',
  'scope_guard':'Scope guards remain non-runtime constraints and may shape wording/QA but are never memorization targets.',
  'review':'Every exact-name palace-managed record is eligible for delayed Review; visible review limits remain a runtime concern for later gates.',
  'spelling':'No Unit 6 item receives a mandatory spelling gate at F2. Adaptive spelling support may be added later when useful.'},
 'counts':{'total':len(records),'by_destination':dict(bydest),'by_name_support':dict(byname),'exact_name_targets':sum(x['delayed_review_target'] for x in records),'mandatory_spelling_targets':0,'prerequisite_reactivations':sum(x['reactivation_mode']=='PRIOR_UNIT_REACTIVATION' for x in records)},
 'records':records}

architecture={'schema':'memory-palace-v2-unit6-f2-palace-architecture-1.0','generated_utc':GENERATED_UTC,'unit_id':'unit-6',
 'architecture_policy':'F2 fixes learning destinations and permanent spatial architecture only. It does not write characters, causal scene actions, mnemonic sound hooks, or polished narrative prose.',
 'counts':{'canonical_records':len(recs),'palace_managed_records':len(palace_expected),'scope_guard_records':len(scope),'practice_only_records':len(practice),'journeys':len(journeys),'bundles':len(bundles),'permanent_loci':len(loci),'confusable_sets':len(confusable)},
 'journeys':journeys,'bundles':bundles,'loci':loci,'challenge_lab':challenge,
 'scope_guards':[{'knowledge_id':r['knowledge_id'],'topic':r['topic'],'canonical_label':r['canonical_label'],'canonical_statement':r['canonical_verified_statement'],'runtime_status':'NON_RUNTIME_SCOPE_BOUNDARY'} for r in scope],
 'confusable_sets':confusable}

dump(ARCH/'learning-classification-f2.json',classification); dump(ARCH/'palace-architecture-f2.json',architecture)

# Locks/status/manifests
f1_files=[U6/'source'/'canonical-unit6-f1.json',U6/'source'/'coverage-manifest-f1.json',U6/'content-lock-f1.json',U6/'f1-release-manifest.json']
f1_hashes={str(p.relative_to(ROOT)):sha(p) for p in f1_files}
lock={'schema':'memory-palace-v2-unit6-f2-lock-1.0','generated_utc':GENERATED_UTC,'unit_id':'unit-6','status':'LEARNING_ARCHITECTURE_LOCKED_F2',
      'f1_scientific_lock':'PRESERVED','f1_protected_hashes':f1_hashes,'classification_file':'architecture/learning-classification-f2.json','architecture_file':'architecture/palace-architecture-f2.json','student_release':False,'narrative_prose_allowed':False}
dump(U6/'content-lock-f2.json',lock)
status={'unit_id':'unit-6','number':6,'title':'Gene Expression and Regulation','status':'LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','pipeline_stage':'F2_COMPLETE','canonical_lock':'LOCKED_F1','learning_architecture_lock':'LOCKED_F2','student_release':False,'preview_release':False,'journey_count':0,'scene_count':0,'memory_objects':0,'application_challenges':0,
'architecture_journeys':len(journeys),'architecture_bundles':len(bundles),'architecture_loci':len(loci),'palace_managed_records':len(palace_expected),'challenge_lab_records':len(practice),'scope_guards':len(scope),'confusable_sets':len(confusable),'exact_name_targets':classification['counts']['exact_name_targets'],'next_required_output':'F3 science-bearing scene briefs for every permanent locus; no polished narrative prose until F3 brief QA passes'}
dump(U6/'status-f2.json',status); dump(U6/'status.json',status)
release={'schema':'memory-palace-v2-unit6-f2-release-1.0','generated_utc':GENERATED_UTC,'unit_id':'unit-6','release':'F2_LEARNING_ARCHITECTURE_LOCK','student_release':False,
'canonical_records':len(recs),'palace_managed_records':len(palace_expected),'scope_guard_records':len(scope),'challenge_lab_records':len(practice),'journey_blueprints':len(journeys),'bundle_blueprints':len(bundles),'permanent_locus_blueprints':len(loci),'confusable_sets':len(confusable),'exact_name_targets':classification['counts']['exact_name_targets'],'prerequisite_reactivations':classification['counts']['prerequisite_reactivations'],'narrative_story_files':0,'student_runtime_memory_objects':0,'gate':'F2 fixes Unit 6 learning destinations and spatial architecture. F3 may specify science-bearing scene actions, actors/parts, visual mechanisms, and transitions; polished story prose remains gated until F3 brief QA.'}
dump(U6/'f2-release-manifest.json',release)

# Development course registry: Unit 6 architecture is locked but still has zero student runtime.
course_path=ROOT/'content'/'ap-biology'/'course.json'
course=load(course_path)
u6entry=next(u for u in course['units'] if u['unit_id']=='unit-6')
u6entry.update({'status':'LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED','journey_count':0,'scene_count':0,'canonical_lock':'LOCKED_F1','source_status':'AUDITED_F1_ARCHITECTURE_F2','student_release':False,'canonical_records':len(recs),'ced_topics':8,'ced_atoms':len(src['ced_current_atoms']),'teacher_ppt_slides':121,'architecture_journeys':len(journeys),'architecture_loci':len(loci),'architecture_lock':'LOCKED_F2','challenge_lab_records':len(practice),'scope_guard_records':len(scope),'exact_name_review_targets':classification['counts']['exact_name_targets'],'confusable_sets':len(confusable)})
dump(course_path,course)

print('UNIT 6 F2 BUILD PASS')
print(architecture['counts']); print(classification['counts'])
