from __future__ import annotations
import json, hashlib
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'
SRC=U5/'source'/'canonical-unit5-f1.json'
ARCH=U5/'architecture'
ARCH.mkdir(parents=True,exist_ok=True)
GENERATED_UTC='2026-09-04T05:30:00+00:00'

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,obj): Path(p).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# Each tuple: locus, journey, bundle, title, micro-anchor, [left,center,right], primary ID, all IDs, visual mode.
RAW_LOCI=[
 ('U5-L01','U5-J1','U5-B01','Heredity Record Desk','the intake desk where heredity, genetics, genes, chromosomes, and conserved information are filed into one inheritance record',['heredity / genetics record cards','gene-to-chromosome filing rail','conserved DNA/RNA code archive'],'U5-K-036',['U5-K-035','U5-K-036','U5-K-037','U5-K-038','U5-K-064'],'HEREDITY_GENE_CHROMOSOME_MAP'),
 ('U5-L02','U5-J1','U5-B01','Homolog Pair Vault','the chromosome vault contrasting homologous partners, replicated sister chromatids, and their organized karyotype display',['homologous chromosome pair','homolog-versus-sister comparison bench','karyotype display wall'],'U5-K-042',['U5-K-042','U5-K-043','U5-K-044'],'HOMOLOG_SISTER_KARYOTYPE_COMPARISON'),
 ('U5-L03','U5-J1','U5-B02','Ploidy Counter','the cell-entry counter sorting somatic cells, gametes, diploid sets, haploid sets, and typical human chromosome counts',['diploid somatic-cell lane','2n ↔ n chromosome-set counter','haploid gamete lane'],'U5-K-046',['U5-K-045','U5-K-046','U5-K-047','U5-K-048','U5-K-049'],'PLOIDY_CELL_TYPE_COUNTER'),
 ('U5-L04','U5-J1','U5-B02','Reproduction Fork','the fork separating asexual clonal descent from sexual reproduction involving meiosis and gamete fusion',['asexual route and clone line','reproduction comparison fork','sexual reproduction route'],'U5-K-041',['U5-K-039','U5-K-040','U5-K-041'],'SEXUAL_ASEXUAL_REPRODUCTION_COMPARISON'),
 ('U5-L05','U5-J1','U5-B02','Life-Cycle Fusion Loop','the circular life-cycle display where haploid gametes fuse at fertilization to form a diploid zygote and continue the next generation',['haploid gamete entry','fertilization / zygote fusion point','diploid life-cycle continuation'],'U5-K-015',['U5-K-015','U5-K-052','U5-K-053','U5-K-054'],'FERTILIZATION_PLOIDY_LIFE_CYCLE'),

 ('U5-L06','U5-J2','U5-B03','Premeiotic Loading Bay','the predivision loading bay where DNA replication creates sister chromatids before meiosis I begins',['unreplicated chromosome input','S-phase DNA-replication loader','replicated sister-chromatid chromosome output'],'U5-K-055',['U5-K-055'],'PREMEIOTIC_REPLICATION_MODEL'),
 ('U5-L07','U5-J2','U5-B03','Prophase I Pairing Chamber','the prophase-I chamber where homologs synapse into tetrads and nonsister chromatids cross at visible chiasmata',['homolog entry and synapsis','tetrad / crossover interaction zone','chiasmata and recombinant segments'],'U5-K-002',['U5-K-002','U5-K-012','U5-K-056','U5-K-057','U5-K-058'],'PROPHASE_I_SYNAPIS_CROSSOVER'),
 ('U5-L08','U5-J2','U5-B04','Metaphase I Orientation Platform','the metaphase-I platform where homologous pairs align and each pair chooses its orientation independently',['one homologous pair orientation','metaphase plate with paired homologs','different pair orientation'],'U5-K-003',['U5-K-003','U5-K-060'],'METAPHASE_I_INDEPENDENT_ORIENTATION'),
 ('U5-L09','U5-J2','U5-B04','Anaphase I Separation Track','the first-division track where homologous chromosomes move apart while each chromosome keeps its joined sister chromatids',['one homolog moving poleward','homolog-separation track','partner homolog moving to opposite pole'],'U5-K-004',['U5-K-004'],'ANAPHASE_I_HOMOLOG_SEPARATION'),
 ('U5-L10','U5-J2','U5-B04','Telophase I Haploid Landing','the first-division landing where two cells are haploid even though every chromosome still contains two sister chromatids',['first haploid daughter cell','chromosome-set versus DNA-content display','second haploid daughter cell'],'U5-K-005',['U5-K-005','U5-K-063'],'TELOPHASE_I_HAPLOID_DUPLICATED_STATE'),
 ('U5-L11','U5-J2','U5-B05','Interdivision No-Replication Gate','the locked interdivision gate that allows cells into meiosis II without another round of chromosome replication',['meiosis-I daughter cells','NO DNA REPLICATION gate','meiosis-II entry'],'U5-K-062',['U5-K-062'],'NO_REPLICATION_BETWEEN_DIVISIONS'),
 ('U5-L12','U5-J2','U5-B05','Prophase II Restart Bay','the second-division restart bay where a new spindle forms around already-duplicated chromosomes',['haploid duplicated chromosomes','prophase-II spindle formation','opposite-pole microtubule access'],'U5-K-006',['U5-K-006'],'PROPHASE_II_SPINDLE_RESTART'),
 ('U5-L13','U5-J2','U5-B05','Metaphase II Alignment Rail','the metaphase-II rail where individual duplicated chromosomes align and sister kinetochores face opposite poles',['one spindle pole','single-chromosome metaphase-II plate','opposite spindle pole'],'U5-K-007',['U5-K-007'],'METAPHASE_II_SISTER_ALIGNMENT'),
 ('U5-L14','U5-J2','U5-B05','Anaphase II Sister Split','the second-division split where centromeric sister association is released and sister chromatids move to opposite poles',['one sister chromatid','centromeric-release split point','other sister chromatid'],'U5-K-008',['U5-K-008'],'ANAPHASE_II_SISTER_SEPARATION'),
 ('U5-L15','U5-J2','U5-B05','Four-Cell Meiosis Exit','the terminal comparison bay showing four haploid unduplicated products after meiosis and contrasting the outcome with mitosis',['mitosis outcome panel','four-cell haploid meiosis exit','division-number / genetic-outcome comparison'],'U5-K-001',['U5-K-001','U5-K-009','U5-K-010'],'MEIOSIS_FINAL_OUTCOME_COMPARISON'),

 ('U5-L16','U5-J3','U5-B06','Variation Sources Compass','the three-direction compass linking crossover-created recombinant chromosomes, independent meiotic orientation, and random fertilization to genetic diversity',['crossover / recombinant route','three-source diversity compass','random-fertilization route'],'U5-K-013',['U5-K-013','U5-K-059','U5-K-061'],'SEXUAL_VARIATION_SOURCE_SYNTHESIS'),
 ('U5-L17','U5-J3','U5-B07','Segregation Integrity Gate','the checkpoint contrasting correct chromosome segregation with nondisjunction in meiosis I or meiosis II',['correct homolog / sister segregation','segregation integrity checkpoint','nondisjunction failure route'],'U5-K-011',['U5-K-011','U5-K-128'],'SEGREGATION_VS_NONDISJUNCTION'),
 ('U5-L18','U5-J3','U5-B07','Aneuploidy Diagnostic Bench','the chromosome-count diagnostic bench separating extra or missing individual chromosomes from the meiotic error that produced them',['normal chromosome complement','aneuploid count comparison','abnormal karyotype display'],'U5-K-129',['U5-K-129','U5-K-131'],'ANEUPLOIDY_KARYOTYPE_DIAGNOSTIC'),
 ('U5-L19','U5-J3','U5-B07','Trisomy 21 Case Window','the case window showing three copies of chromosome 21 as one illustrative aneuploid outcome of nondisjunction',['paired chromosome-21 reference','three-copy chromosome-21 display','case interpretation / scope reminder'],'U5-K-130',['U5-K-130'],'TRISOMY_21_ANEUPLOIDY_CASE'),

 ('U5-L20','U5-J4','U5-B08','Mendel Breeding Courtyard','the pea-breeding courtyard tracing a true-breeding parental cross through P, F1, and F2 generations',['true-breeding P generation','Mendel cross and F1 offspring','F2 generation outcome'],'U5-K-065',['U5-K-065','U5-K-066','U5-K-067','U5-K-068','U5-K-069'],'MENDEL_GENERATION_CROSS'),
 ('U5-L21','U5-J4','U5-B08','Allele Notation Cabinet','the allele cabinet separating alternate gene forms and the uppercase/lowercase convention from the biological meaning of dominance',['recessive-allele notation','allele pair / gene reference','dominant-allele notation'],'U5-K-071',['U5-K-071','U5-K-072','U5-K-076','U5-K-077'],'ALLELE_DOMINANCE_NOTATION'),
 ('U5-L22','U5-J4','U5-B08','Genotype–Phenotype Bench','the comparison bench linking genotype and homozygous/heterozygous states to phenotype under complete dominance',['homozygous genotype examples','genotype-to-phenotype comparison','heterozygous / complete-dominance outcome'],'U5-K-018',['U5-K-018','U5-K-019','U5-K-073','U5-K-074','U5-K-078'],'GENOTYPE_PHENOTYPE_DOMINANCE_COMPARISON'),
 ('U5-L23','U5-J4','U5-B09','Mendelian Laws Gate','the two-rule gate separating allele segregation within one gene from independent assortment across unlinked genes',['law of segregation lane','Mendelian laws for unlinked genes','law of independent assortment lane'],'U5-K-014',['U5-K-014','U5-K-079','U5-K-081'],'SEGREGATION_INDEPENDENT_ASSORTMENT'),
 ('U5-L24','U5-J4','U5-B09','Cross-Type Arbor','the branching arbor distinguishing monohybrid, dihybrid, and testcross designs before any probabilities are calculated',['monohybrid branch','cross-type decision arbor','dihybrid / testcross branches'],'U5-K-017',['U5-K-017','U5-K-075','U5-K-080','U5-K-082'],'MONOHYBRID_DIHYBRID_TESTCROSS'),
 ('U5-L25','U5-J4','U5-B10','Gamete–Punnett Board','the board where a parent genotype is first converted into possible gametes before those gametes enter a Punnett square',['parent genotype / gamete generator','Punnett-square combination grid','offspring genotype possibilities'],'U5-K-085',['U5-K-070','U5-K-085'],'GAMETE_TO_PUNNETT_WORKFLOW'),
 ('U5-L26','U5-J4','U5-B10','Classic Ratio Balcony','the outcome balcony comparing conditional 3:1 monohybrid and 9:3:3:1 dihybrid phenotype ratios under their required assumptions',['conditional 3:1 panel','assumption / scope banner','conditional 9:3:3:1 panel'],'U5-K-083',['U5-K-083','U5-K-084'],'CLASSIC_RATIO_CONDITIONS'),

 ('U5-L27','U5-J5','U5-B11','Inheritance Probability Hall','the probability hall translating random gamete formation and fertilization into numerical inheritance predictions',['gamete-event probabilities','inheritance probability model','offspring-outcome probabilities'],'U5-K-016',['U5-K-016'],'INHERITANCE_PROBABILITY_MODEL'),
 ('U5-L28','U5-J5','U5-B11','Addition–Multiplication Junction','the probability junction separating OR outcomes that add from independent AND outcomes that multiply',['addition-rule OR lane','event-combination junction','multiplication-rule AND lane'],'U5-K-022',['U5-K-021','U5-K-022'],'ADDITION_MULTIPLICATION_RULE_COMPARISON'),
 ('U5-L29','U5-J5','U5-B12','Pedigree Reading Gallery','the family-symbol gallery teaching pedigree structure, notation, and cautious inheritance clues across generations',['pedigree symbol key','multigeneration pedigree','autosomal-dominant clue panel'],'U5-K-086',['U5-K-086','U5-K-087','U5-K-088'],'PEDIGREE_NOTATION_AND_CLUES'),
 ('U5-L30','U5-J5','U5-B12','Inheritance Pattern Verdict Room','the evidence room where family or offspring patterns are used to infer the inheritance model that best fits the data',['observed inheritance pattern','model-comparison verdict table','supported / unsupported pattern interpretations'],'U5-K-020',['U5-K-020'],'INHERITANCE_PATTERN_INFERENCE'),

 ('U5-L31','U5-J6','U5-B13','Beyond-Mendel Pattern Entrance','the entry display where observed offspring ratios are checked for departures from simple Mendelian expectations before a mechanism is assigned',['simple Mendelian expectation','quantitative ratio comparison','non-Mendelian pattern routes'],'U5-K-023',['U5-K-023','U5-K-089'],'NON_MENDELIAN_RATIO_GATE'),
 ('U5-L32','U5-J6','U5-B13','Dominance Spectrum Studio','the phenotype studio comparing incomplete dominance, codominance, multiple alleles, and the ABO example without blending the mechanisms together',['incomplete-dominance intermediate phenotype','codominance / multiple-allele comparison','ABO allele-system display'],'U5-K-026',['U5-K-025','U5-K-026','U5-K-090','U5-K-091'],'DOMINANCE_MULTIPLE_ALLELE_COMPARISON'),
 ('U5-L33','U5-J6','U5-B13','Gene-Interaction Theater','the trait theater contrasting epistasis, polygenic inheritance, and pleiotropy by asking how many genes and how many phenotypic effects are involved',['epistasis masking interaction','gene-count / effect-count comparison stage','polygenic spectrum and pleiotropic branches'],'U5-K-028',['U5-K-028','U5-K-092','U5-K-093'],'EPISTASIS_POLYGENIC_PLEIOTROPY'),
 ('U5-L34','U5-J6','U5-B14','Chromosome-Linked Inheritance Comparator','the chromosome wall distinguishing autosomes, the stated human XX/XY complement model, and genes located on X or Y chromosomes',['autosome panel','explicit XX/XY chromosome-complement model','X-linked / Y-linked gene panel'],'U5-K-027',['U5-K-027','U5-K-050','U5-K-051','U5-K-094','U5-K-095'],'AUTOSOME_XY_SEX_LINKAGE_COMPARISON'),
 ('U5-L35','U5-J6','U5-B14','Hemizygous Transmission Rail','the explicit XX/XY inheritance rail showing how a single X-linked allele can be expressed when no homologous allele is present',['X-linked allele source','hemizygous transmission rail','offspring inheritance / disorder-example panel'],'U5-K-096',['U5-K-096','U5-K-097','U5-K-100'],'HEMIZYGOUS_X_LINKED_TRANSMISSION'),
 ('U5-L36','U5-J6','U5-B14','X-Inactivation Mosaic Gallery','the cell mosaic gallery where X-chromosome inactivation produces condensed Barr bodies and patchwork expression',['cell with one X active','X-inactivation / Barr-body mechanism','mosaic pattern across many cells'],'U5-K-098',['U5-K-098','U5-K-099'],'X_INACTIVATION_BARR_BODY_MOSAIC'),
 ('U5-L37','U5-J6','U5-B15','Phenotypic Plasticity Conservatory','the environmental conservatory where the same genotype changes phenotype across temperature, soil chemistry, or UV conditions through physiological and gene-expression responses',['temperature-dependent pigmentation','genotype-by-environment / phenotypic-plasticity core','soil-pH and UV-response examples'],'U5-K-034',['U5-K-034','U5-K-120','U5-K-121','U5-K-122','U5-K-123'],'GENOTYPE_ENVIRONMENT_PLASTICITY'),

 ('U5-L38','U5-J7','U5-B16','Linked-Gene Platform','the chromosome platform where nearby loci on the same chromosome tend to travel together through meiosis',['nearby linked loci','same-chromosome linkage platform','less-linked distant loci reference'],'U5-K-024',['U5-K-024','U5-K-104'],'GENETIC_LINKAGE_DISTANCE'),
 ('U5-L39','U5-J7','U5-B16','Recombination Switch','the crossover switch where a recombination event between linked loci can separate parental allele combinations',['parental homolog arrangement','crossover between linked loci','recombinant chromatid output'],'U5-K-101',['U5-K-101','U5-K-105'],'LINKED_GENE_CROSSOVER_RECOMBINATION'),
 ('U5-L40','U5-J7','U5-B16','Parental–Recombinant Sorting Yard','the offspring sorting yard separating parental-type classes from recombinant-type classes before frequencies are calculated',['parental-type bins','offspring-classification sorter','recombinant-type bins'],'U5-K-102',['U5-K-102','U5-K-103'],'PARENTAL_RECOMBINANT_CLASSIFICATION'),
 ('U5-L41','U5-J7','U5-B17','Recombination Frequency Meter','the meter calculating the percentage of recombinant offspring or gametes for two loci',['recombinant count input','recombination-frequency percentage meter','linkage / distance interpretation output'],'U5-K-106',['U5-K-106'],'RECOMBINATION_FREQUENCY_METER'),
 ('U5-L42','U5-J7','U5-B17','Linkage Map Board','the gene-order board converting short-interval recombination percentages into approximate centimorgan distances',['recombination-frequency marks','linkage map / gene-order board','map-unit / centimorgan ruler'],'U5-K-107',['U5-K-107','U5-K-108'],'LINKAGE_MAP_CENTIMORGAN'),
 ('U5-L43','U5-J7','U5-B17','Fifty-Percent Ceiling Gate','the mapping gate showing why recombination frequency cannot exceed about 50% as an observable two-locus measure',['increasing locus separation','50-percent ceiling barrier','independent-assortment-equivalent outcome'],'U5-K-109',['U5-K-109'],'RECOMBINATION_50_PERCENT_CEILING'),

 ('U5-L44','U5-J8','U5-B18','Non-Nuclear Inheritance Dock','the cytoplasmic inheritance dock separating nuclear chromosome logic from mitochondrial and chloroplast genomes that assort through organelles',['nuclear inheritance reference','non-nuclear / organelle inheritance dock','organelle assortment route'],'U5-K-029',['U5-K-029','U5-K-030','U5-K-110'],'NON_NUCLEAR_ORGANELLE_INHERITANCE'),
 ('U5-L45','U5-J8','U5-B18','Mitochondrial Inheritance Route','the animal mitochondrial route emphasizing typical cytoplasmic inheritance from the egg rather than a universal parent-of-origin rule',['sperm mitochondrial contribution reference','zygote mitochondrial pool','typical maternal mitochondrial inheritance route'],'U5-K-031',['U5-K-031'],'MITOCHONDRIAL_INHERITANCE_ROUTE'),
 ('U5-L46','U5-J8','U5-B18','Plant Organelle Inheritance Route','the plant organelle route comparing chloroplast and mitochondrial inheritance patterns without imposing one universal parent-of-origin rule',['paternal / biparental possibility','plant organelle inheritance comparison','maternal inheritance possibility'],'U5-K-032',['U5-K-032'],'PLANT_ORGANELLE_INHERITANCE'),
 ('U5-L47','U5-J8','U5-B18','Inheritance Case Archive','the case archive linking genetic disorder, pathogenic variant, and two teacher examples while keeping named disorders as illustrative enrichment',['Tay-Sachs case file','genetic disorder / pathogenic variant index','sickle-cell disease case file'],'U5-K-124',['U5-K-124','U5-K-125','U5-K-126','U5-K-127'],'GENETIC_DISORDER_VARIANT_CASES'),
 ('U5-L48','U5-J8','U5-B19','Chi-Square Model Bench','the goodness-of-fit bench defining the null-model comparison and restricting the procedure to categorical count data',['null-model expected proportions','chi-square goodness-of-fit / hypothesis-testing bench','categorical count-data requirement'],'U5-K-033',['U5-K-033','U5-K-111','U5-K-114'],'CHI_SQUARE_GOODNESS_OF_FIT_MODEL'),
 ('U5-L49','U5-J8','U5-B19','Observed–Expected Calculation Station','the calculation station pairing observed and expected counts and summing each category contribution (O−E)²/E',['observed-count column','(O−E)²/E contribution calculator','expected-count column'],'U5-K-112',['U5-K-112','U5-K-113','U5-K-115'],'CHI_SQUARE_OBSERVED_EXPECTED_CALCULATION'),
 ('U5-L50','U5-J8','U5-B19','Chi-Square Decision Console','the final decision console combining degrees of freedom, critical value, p-value or alpha criterion, and correct reject/fail-to-reject language',['degrees-of-freedom / critical-value controls','chi-square decision console','p-value / reject-or-fail-to-reject output'],'U5-K-119',['U5-K-116','U5-K-117','U5-K-118','U5-K-119'],'CHI_SQUARE_DECISION_LOGIC'),
]

JOURNEYS=[
 {'journey_id':'U5-J1','working_title':'Heredity and Chromosome Registry','content_focus':'Foundational heredity language, genes on chromosomes, homologous chromosomes versus sister chromatids, ploidy, reproduction modes, fertilization, and life-cycle continuity','setting_logic':'A registry/archive makes inherited information, chromosome identity, chromosome-set number, and reproductive transitions physically separate before meiosis begins.','bundles':[{'bundle_id':'U5-B01','title':'Heredity information and chromosome identity','loci':['U5-L01','U5-L02']},{'bundle_id':'U5-B02','title':'Ploidy, reproduction, and life-cycle transitions','loci':['U5-L03','U5-L04','U5-L05']}]},
 {'journey_id':'U5-J2','working_title':'Meiosis Transit Hall','content_focus':'Premeiotic replication, prophase-I pairing and crossing over, meiosis-I homolog segregation, no interdivision replication, meiosis-II sister-chromatid segregation, and final haploid products','setting_logic':'A transit hall follows the same chromosomes continuously from premeiotic replication through two divisions so chromosome identity, ploidy, and chromatid state never reset between phases.','bundles':[{'bundle_id':'U5-B03','title':'Replication and prophase-I pairing','loci':['U5-L06','U5-L07']},{'bundle_id':'U5-B04','title':'Meiosis-I homolog segregation','loci':['U5-L08','U5-L09','U5-L10']},{'bundle_id':'U5-B05','title':'Interdivision passage and meiosis II','loci':['U5-L11','U5-L12','U5-L13','U5-L14','U5-L15']}]},
 {'journey_id':'U5-J3','working_title':'Diversity and Chromosome Error Center','content_focus':'Sources of variation, recombinant chromosomes, random fertilization, correct segregation, nondisjunction, aneuploidy, and chromosome-number examples','setting_logic':'A quality-control center first synthesizes the normal diversity-producing mechanisms, then contrasts correct chromosome movement with segregation failures and their count-level outcomes.','bundles':[{'bundle_id':'U5-B06','title':'Genetic-diversity synthesis','loci':['U5-L16']},{'bundle_id':'U5-B07','title':'Segregation errors and chromosome-number outcomes','loci':['U5-L17','U5-L18','U5-L19']}]},
 {'journey_id':'U5-J4','working_title':'Mendelian Inheritance Estate','content_focus':'Mendel experiments, alleles, dominance vocabulary, genotype and phenotype, Mendelian laws, cross types, gamete generation, Punnett squares, and classic conditional ratios','setting_logic':'A breeding estate follows information from parental lines to allele notation, genotype/phenotype, meiotic laws, gamete production, and offspring-combination models without turning Punnett squares into the biology itself.','bundles':[{'bundle_id':'U5-B08','title':'Mendel, alleles, genotype, and phenotype','loci':['U5-L20','U5-L21','U5-L22']},{'bundle_id':'U5-B09','title':'Mendelian laws and cross design','loci':['U5-L23','U5-L24']},{'bundle_id':'U5-B10','title':'Gametes, Punnett models, and ratio conditions','loci':['U5-L25','U5-L26']}]},
 {'journey_id':'U5-J5','working_title':'Probability and Pedigree Court','content_focus':'Inheritance probability, addition and multiplication rules, pedigree notation, and evidence-based inference of inheritance patterns','setting_logic':'A court separates probability rules from family-data evidence, then requires an inheritance model to be justified from the observed pattern rather than guessed from one clue.','bundles':[{'bundle_id':'U5-B11','title':'Probability rules for inheritance','loci':['U5-L27','U5-L28']},{'bundle_id':'U5-B12','title':'Pedigree reading and inheritance-model inference','loci':['U5-L29','U5-L30']}]},
 {'journey_id':'U5-J6','working_title':'Beyond-Mendel Trait Gallery','content_focus':'Non-Mendelian ratios, incomplete dominance, codominance, multiple alleles, ABO, epistasis, polygenic inheritance, pleiotropy, chromosome-linked inheritance, X inactivation, and environmental effects on phenotype','setting_logic':'A trait gallery compares mechanisms by what changes the phenotype pattern: allelic interaction, number of alleles, interaction among genes, chromosome location, dosage regulation, or environment.','bundles':[{'bundle_id':'U5-B13','title':'Non-Mendelian allelic and gene-interaction patterns','loci':['U5-L31','U5-L32','U5-L33']},{'bundle_id':'U5-B14','title':'Chromosome-linked inheritance and X dosage','loci':['U5-L34','U5-L35','U5-L36']},{'bundle_id':'U5-B15','title':'Environmental effects and phenotypic plasticity','loci':['U5-L37']}]},
 {'journey_id':'U5-J7','working_title':'Chromosome Mapping Rail Yard','content_focus':'Genetic linkage, crossing-over separation of linked alleles, parental and recombinant classes, recombination frequency, linkage maps, centimorgans, and the 50-percent ceiling','setting_logic':'A rail yard makes linked loci travel together on the same chromosome, uses crossover switches to reroute allele combinations, and converts recombinant traffic into map-distance estimates.','bundles':[{'bundle_id':'U5-B16','title':'Linkage, recombination, and offspring classes','loci':['U5-L38','U5-L39','U5-L40']},{'bundle_id':'U5-B17','title':'Recombination frequency and linkage mapping','loci':['U5-L41','U5-L42','U5-L43']}]},
 {'journey_id':'U5-J8','working_title':'Inheritance Evidence Laboratory','content_focus':'Non-nuclear inheritance, mitochondrial and plant organelle transmission, illustrative genetic-disorder cases, and chi-square goodness-of-fit reasoning','setting_logic':'An evidence lab keeps cytoplasmic inheritance separate from nuclear Mendelian logic, then ends with a statistical workflow where observed counts are compared with a defined inheritance model.','bundles':[{'bundle_id':'U5-B18','title':'Organelle inheritance and illustrative inheritance cases','loci':['U5-L44','U5-L45','U5-L46','U5-L47']},{'bundle_id':'U5-B19','title':'Chi-square model, calculation, and decision','loci':['U5-L48','U5-L49','U5-L50']}]},
]

PRACTICE=[
 {'challenge_id':'U5-CH-01','knowledge_id':'U5-K-132','title':'Meiosis phase identification practice','type':'MODEL_PHASE_IDENTIFICATION','prerequisite_loci':['U5-L06','U5-L07','U5-L08','U5-L09','U5-L10','U5-L11','U5-L12','U5-L13','U5-L14','U5-L15']},
 {'challenge_id':'U5-CH-02','knowledge_id':'U5-K-133','title':'Genetic-diversity mechanism practice','type':'MECHANISM_DISCRIMINATION','prerequisite_loci':['U5-L07','U5-L08','U5-L16']},
 {'challenge_id':'U5-CH-03','knowledge_id':'U5-K-134','title':'Monohybrid Punnett-square practice','type':'GENETIC_CROSS','prerequisite_loci':['U5-L21','U5-L22','U5-L23','U5-L24','U5-L25']},
 {'challenge_id':'U5-CH-04','knowledge_id':'U5-K-135','title':'Gamete-generation practice','type':'GAMETE_GENERATION','prerequisite_loci':['U5-L23','U5-L25']},
 {'challenge_id':'U5-CH-05','knowledge_id':'U5-K-136','title':'Dihybrid Punnett-square practice','type':'GENETIC_CROSS','prerequisite_loci':['U5-L23','U5-L24','U5-L25']},
 {'challenge_id':'U5-CH-06','knowledge_id':'U5-K-137','title':'Multiplication-rule genetics practice','type':'PROBABILITY_CALCULATION','prerequisite_loci':['U5-L27','U5-L28']},
 {'challenge_id':'U5-CH-07','knowledge_id':'U5-K-138','title':'Addition-rule genetics practice','type':'PROBABILITY_CALCULATION','prerequisite_loci':['U5-L27','U5-L28']},
 {'challenge_id':'U5-CH-08','knowledge_id':'U5-K-139','title':'Pedigree inference practice','type':'PEDIGREE_INFERENCE','prerequisite_loci':['U5-L29','U5-L30']},
 {'challenge_id':'U5-CH-09','knowledge_id':'U5-K-140','title':'Incomplete-dominance and codominance cross practice','type':'NON_MENDELIAN_CROSS','prerequisite_loci':['U5-L31','U5-L32']},
 {'challenge_id':'U5-CH-10','knowledge_id':'U5-K-141','title':'ABO genotype inference practice','type':'MULTIPLE_ALLELE_CROSS','prerequisite_loci':['U5-L32']},
 {'challenge_id':'U5-CH-11','knowledge_id':'U5-K-142','title':'X-linked inheritance practice','type':'CHROMOSOME_LINKED_CROSS','prerequisite_loci':['U5-L34','U5-L35']},
 {'challenge_id':'U5-CH-12','knowledge_id':'U5-K-143','title':'Linked-gene recombinant classification practice','type':'RECOMBINANT_CLASSIFICATION','prerequisite_loci':['U5-L38','U5-L39','U5-L40']},
 {'challenge_id':'U5-CH-13','knowledge_id':'U5-K-144','title':'Genetic map-distance practice','type':'LINKAGE_MAP_CALCULATION','prerequisite_loci':['U5-L41','U5-L42','U5-L43']},
 {'challenge_id':'U5-CH-14','knowledge_id':'U5-K-145','title':'Chi-square expected-count setup','type':'CHI_SQUARE_SETUP','prerequisite_loci':['U5-L48','U5-L49']},
 {'challenge_id':'U5-CH-15','knowledge_id':'U5-K-146','title':'Chi-square calculation and hypothesis decision','type':'CHI_SQUARE_CALCULATION_DECISION','prerequisite_loci':['U5-L48','U5-L49','U5-L50']},
 {'challenge_id':'U5-CH-16','knowledge_id':'U5-K-147','title':'Environmental phenotype application','type':'GENOTYPE_ENVIRONMENT_REASONING','prerequisite_loci':['U5-L37']},
]

SCOPE_GUARDS=[
 {'knowledge_id':'U5-K-148','canonical_label':'Sexual-life-cycle detail scope guard','policy':'NON_RUNTIME_AP_SCOPE_BOUNDARY','supporting_loci':['U5-L04','U5-L05']},
 {'knowledge_id':'U5-K-149','canonical_label':'Chromosome complement terminology scope guard','policy':'NON_RUNTIME_TERMINOLOGY_BOUNDARY','supporting_loci':['U5-L34','U5-L35']},
 {'knowledge_id':'U5-K-150','canonical_label':'Classic Mendelian ratio scope guard','policy':'NON_RUNTIME_CONDITIONAL_RATIO_BOUNDARY','supporting_loci':['U5-L23','U5-L26']},
 {'knowledge_id':'U5-K-151','canonical_label':'Named-disorder scope guard','policy':'NON_RUNTIME_AP_SCOPE_BOUNDARY','supporting_loci':['U5-L19','U5-L35','U5-L47']},
 {'knowledge_id':'U5-K-152','canonical_label':'Null-hypothesis language scope guard','policy':'NON_RUNTIME_STATISTICAL_LANGUAGE_BOUNDARY','supporting_loci':['U5-L48','U5-L50']},
]

CONFUSABLES=[
 ('U5-CF-01','Chromosome relationship',['homologous chromosomes','sister chromatids'],['U5-K-042','U5-K-043']),
 ('U5-CF-02','Ploidy',['diploid','haploid'],['U5-K-046','U5-K-047']),
 ('U5-CF-03','Cell type and chromosome set',['somatic cell','gamete'],['U5-K-045','U5-K-048']),
 ('U5-CF-04','Reproduction mode',['asexual reproduction','sexual reproduction'],['U5-K-039','U5-K-041']),
 ('U5-CF-05','Prophase-I structures',['synapsis','tetrad','chiasma'],['U5-K-056','U5-K-057','U5-K-058']),
 ('U5-CF-06','Meiosis-I phase sequence',['prophase I','metaphase I','anaphase I','telophase I'],['U5-K-002','U5-K-003','U5-K-004','U5-K-005']),
 ('U5-CF-07','Meiosis-II phase sequence',['prophase II','metaphase II','anaphase II','telophase II'],['U5-K-006','U5-K-007','U5-K-008','U5-K-009']),
 ('U5-CF-08','What separates in meiosis',['homologous chromosomes in anaphase I','sister chromatids in anaphase II'],['U5-K-004','U5-K-008']),
 ('U5-CF-09','Chromosome-set versus duplication state',['haploid after meiosis I','no DNA replication between meiosis I and II'],['U5-K-063','U5-K-062']),
 ('U5-CF-10','Sources of sexual variation',['crossing over','independent orientation','random fertilization'],['U5-K-012','U5-K-060','U5-K-061']),
 ('U5-CF-11','Segregation error vocabulary',['nondisjunction','aneuploidy'],['U5-K-128','U5-K-129']),
 ('U5-CF-12','Inheritance information vocabulary',['gene','allele'],['U5-K-037','U5-K-071']),
 ('U5-CF-13','Observable versus genetic state',['genotype','phenotype'],['U5-K-018','U5-K-019']),
 ('U5-CF-14','Zygosity states',['homozygous dominant','heterozygous','homozygous recessive'],['U5-K-073','U5-K-018','U5-K-074']),
 ('U5-CF-15','Allele interaction under complete dominance',['dominant allele','recessive allele','complete dominance'],['U5-K-076','U5-K-077','U5-K-078']),
 ('U5-CF-16','Mendelian laws',['law of segregation','law of independent assortment'],['U5-K-079','U5-K-081']),
 ('U5-CF-17','Genetic cross types',['monohybrid','dihybrid','testcross'],['U5-K-080','U5-K-082','U5-K-075']),
 ('U5-CF-18','Probability rules',['addition rule','multiplication rule'],['U5-K-021','U5-K-022']),
 ('U5-CF-19','Dominance patterns',['complete dominance','incomplete dominance','codominance'],['U5-K-078','U5-K-026','U5-K-025']),
 ('U5-CF-20','Complex inheritance mechanisms',['multiple alleles','epistasis','polygenic inheritance','pleiotropy'],['U5-K-090','U5-K-092','U5-K-093','U5-K-028']),
 ('U5-CF-21','Chromosome categories',['autosome','X-linked gene','Y-linked gene'],['U5-K-050','U5-K-094','U5-K-095']),
 ('U5-CF-22','X-linked dosage vocabulary',['hemizygous','X-chromosome inactivation','Barr body'],['U5-K-096','U5-K-098','U5-K-099']),
 ('U5-CF-23','Linkage versus recombination',['genetic linkage','genetic recombination'],['U5-K-024','U5-K-101']),
 ('U5-CF-24','Offspring linkage classes',['parental type','recombinant type'],['U5-K-102','U5-K-103']),
 ('U5-CF-25','Mapping measures',['recombination frequency','linkage map','centimorgan'],['U5-K-106','U5-K-107','U5-K-108']),
 ('U5-CF-26','Nuclear versus non-nuclear inheritance',['Mendelian nuclear inheritance','non-nuclear inheritance'],['U5-K-014','U5-K-030']),
 ('U5-CF-27','Organelle inheritance',['mitochondrial inheritance','plant organelle inheritance'],['U5-K-031','U5-K-032']),
 ('U5-CF-28','Clinical genetics terms',['genetic disorder','pathogenic variant'],['U5-K-124','U5-K-125']),
 ('U5-CF-29','Chi-square counts',['observed count','expected count'],['U5-K-112','U5-K-113']),
 ('U5-CF-30','Chi-square thresholds',['critical value','p-value / significance level'],['U5-K-117','U5-K-118']),
 ('U5-CF-31','Significance evidence and decision',['p-value / significance level','reject or fail to reject the null'],['U5-K-118','U5-K-119']),
 ('U5-CF-32','Phenotype source distinction',['inherited genotype difference','environmental effect on phenotype'],['U5-K-018','U5-K-034']),
]

SCOPE_IDS={x['knowledge_id'] for x in SCOPE_GUARDS}
PRACTICE_IDS={x['knowledge_id'] for x in PRACTICE}

HIGH_NAME_TERMS={
 'U5-K-042','U5-K-044','U5-K-046','U5-K-047','U5-K-056','U5-K-057','U5-K-058','U5-K-063','U5-K-128','U5-K-129',
 'U5-K-071','U5-K-075','U5-K-079','U5-K-081','U5-K-086','U5-K-092','U5-K-093','U5-K-028','U5-K-096','U5-K-098','U5-K-099',
 'U5-K-101','U5-K-106','U5-K-107','U5-K-108','U5-K-111','U5-K-116','U5-K-117','U5-K-118','U5-K-119','U5-K-120'
}
MEDIUM_NAME_TERMS={
 'U5-K-001','U5-K-002','U5-K-003','U5-K-004','U5-K-005','U5-K-006','U5-K-007','U5-K-008','U5-K-009','U5-K-010','U5-K-011','U5-K-012','U5-K-013',
 'U5-K-035','U5-K-036','U5-K-037','U5-K-039','U5-K-040','U5-K-041','U5-K-043','U5-K-045','U5-K-048','U5-K-052','U5-K-053','U5-K-054','U5-K-055',
 'U5-K-059','U5-K-060','U5-K-061','U5-K-065','U5-K-066','U5-K-070','U5-K-073','U5-K-074','U5-K-076','U5-K-077','U5-K-078','U5-K-080','U5-K-082',
 'U5-K-089','U5-K-090','U5-K-094','U5-K-095','U5-K-102','U5-K-103','U5-K-104','U5-K-105','U5-K-109','U5-K-110','U5-K-124','U5-K-125'
}
MODEL_IDS={
 'U5-K-001','U5-K-002','U5-K-003','U5-K-004','U5-K-005','U5-K-006','U5-K-007','U5-K-008','U5-K-009','U5-K-010','U5-K-011','U5-K-012','U5-K-013',
 'U5-K-015','U5-K-017','U5-K-020','U5-K-023','U5-K-024','U5-K-027','U5-K-029','U5-K-030','U5-K-031','U5-K-032','U5-K-033','U5-K-034','U5-K-038',
 'U5-K-055','U5-K-059','U5-K-060','U5-K-061','U5-K-062','U5-K-063','U5-K-079','U5-K-081','U5-K-085','U5-K-097','U5-K-104','U5-K-105','U5-K-109','U5-K-110','U5-K-119','U5-K-120'
}

src=load(SRC)
records={r['knowledge_id']:r for r in src['canonical_catalog']}
loci=[]
for lid,jid,bid,title,anchor,zones,primary,kids,visual in RAW_LOCI:
    loci.append({
      'locus_id':lid,'journey_id':jid,'bundle_id':bid,'title':title,'micro_anchor':anchor,
      'scene_geometry':{'left':zones[0],'center':zones[1],'right':zones[2]},
      'primary_knowledge_id':primary,'knowledge_ids':kids,'embedded_knowledge_ids':[k for k in kids if k!=primary],
      'visual_mode':visual,'scientific_visual_required':True,'narrative_status':'ARCHITECTURE_ONLY_NO_STORY_PROSE_F2'
    })
loc_for={kid:l['locus_id'] for l in loci for kid in l['knowledge_ids']}
primary_set={l['primary_knowledge_id'] for l in loci}
classification=[]
for kid in sorted(records,key=lambda x:int(x.split('-')[-1])):
    r=records[kid]
    if kid in PRACTICE_IDS:
        dest='CHALLENGE_LAB'; locus=None; role='APPLIED_TRANSFER'; visual='APPLICATION_PROMPT'; retrieval=['APPLIED_TRANSFER']
    elif kid in SCOPE_IDS:
        dest='SUPPORTING_NON_RUNTIME_SCOPE_GUARD'; locus=None; role='SCOPE_BOUNDARY'; visual='SCOPE_GUARD'; retrieval=['SCOPE_BOUNDARY_RECOGNITION']
    else:
        if kid not in loc_for: raise RuntimeError(f'No permanent locus mapping for {kid} {r["canonical_label"]}')
        locus=loc_for[kid]
        dest='PALACE_PRIMARY_LOCUS' if kid in primary_set else 'PALACE_EMBEDDED'
        role='PRIMARY_ANCHOR' if kid in primary_set else 'EMBEDDED_SCIENCE'
        visual=next(l['visual_mode'] for l in loci if l['locus_id']==locus)
        retrieval=[]
        if r['exact_name_recall']: retrieval.append('EXACT_NAME_FROM_SCIENTIFIC_ROLE')
        retrieval.append('MEANING_OR_MECHANISM')
        if kid in MODEL_IDS: retrieval.append('MODEL_OR_CAUSAL_INTERPRETATION')
    if dest in {'CHALLENGE_LAB','SUPPORTING_NON_RUNTIME_SCOPE_GUARD'} or not r['exact_name_recall']:
        ns='NO_EXACT_NAME_GATE' if not r['exact_name_recall'] or not dest.startswith('PALACE') else 'SEMANTIC_SCIENCE_CUE_SUFFICIENT'
    elif kid in HIGH_NAME_TERMS:
        ns='PHONOLOGICAL_SUPPORT_RECOMMENDED_IF_NEEDED'
    elif kid in MEDIUM_NAME_TERMS or len(r['canonical_label'].split())>=4:
        ns='SEMANTIC_PLUS_OPTIONAL_SOUND_CUE'
    else:
        ns='SEMANTIC_SCIENCE_CUE_SUFFICIENT'
    classification.append({
      'knowledge_id':kid,'canonical_label':r['canonical_label'],'topic':r['topic'],'scope_class':r['scope_class'],
      'destination':dest,'locus_id':locus,'scene_role':role,'visual_mode':visual,
      'exact_name_recall':bool(r['exact_name_recall']) if dest.startswith('PALACE') else False,
      'name_support':ns,'spelling_policy':'ADAPTIVE_SUPPORT_ONLY_NO_MANDATORY_SPELLING_GATE',
      'retrieval_modes':retrieval,'canonical_lock':r['canonical_lock'],'review_flag_id':r.get('review_flag_id')
    })

classdoc={
 'schema':'memory-palace-v2-unit5-f2-classification-1.0','generated_utc':GENERATED_UTC,'unit_id':'unit-5','canonical_source_lock':'F1',
 'policy':{
   'palace':'Use permanent loci for durable biological identities, mechanisms, relationships, and exact terms that benefit from stable spatial retrieval.',
   'embedded':'Embed tightly related definitions/examples inside a locus when a separate locus would fragment one biological mechanism.',
   'challenge_lab':'Keep calculations, novel crosses, model identification, pedigree inference, and transfer problems outside permanent loci.',
   'scope_guard':'Preserve misconception and scope boundaries as non-runtime support rather than memorization targets.',
   'spelling':'No mandatory spelling gate in F2; spelling support remains adaptive.'
 },
 'counts':{
   'total':len(classification),'by_destination':dict(Counter(x['destination'] for x in classification)),
   'by_name_support':dict(Counter(x['name_support'] for x in classification)),
   'exact_name_targets':sum(bool(x['exact_name_recall']) for x in classification),'mandatory_spelling_targets':0
 },
 'records':classification
}
confdocs=[{'set_id':sid,'title':title,'terms':terms,'knowledge_ids':kids} for sid,title,terms,kids in CONFUSABLES]
architecture={
 'schema':'memory-palace-v2-unit5-f2-architecture-1.0','generated_utc':GENERATED_UTC,'unit':{'unit_id':'unit-5','number':5,'title':'Heredity'},
 'design_rules':[
   'F2 defines learning destinations and spatial architecture only; it contains no polished story prose.',
   'The same chromosome set must remain physically traceable across the meiosis route so homolog/sister and ploidy distinctions remain visible.',
   'Punnett-square execution, probability calculation, pedigree inference, recombination calculation, chi-square calculation, and novel crosses remain Challenge Lab functions.',
   'Human X/Y examples use explicit chromosome-complement language and do not equate chromosome complement with gender or the full biology of sex development.',
   'Classic Mendelian ratios are encoded with their assumptions and are never treated as universal inheritance outcomes.',
   'Named human disorders remain illustrative teacher enrichment and do not become AP-scope claims.',
   'Every permanent locus requires a scientific visual in addition to any mnemonic surface imagery later added in F3/F4.'
 ],
 'counts':{
   'canonical_records':len(records),'palace_managed_records':len(loc_for),'scope_guard_records':len(SCOPE_IDS),'practice_only_records':len(PRACTICE),
   'journeys':len(JOURNEYS),'bundles':sum(len(j['bundles']) for j in JOURNEYS),'permanent_loci':len(loci),'confusable_sets':len(confdocs)
 },
 'journeys':JOURNEYS,'loci':loci,'challenge_lab':PRACTICE,'confusable_sets':confdocs,'scope_guards':SCOPE_GUARDS
}
dump(ARCH/'learning-classification-f2.json',classdoc)
dump(ARCH/'palace-architecture-f2.json',architecture)

status={
 'unit_id':'unit-5','number':5,'title':'Heredity','status':'LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED',
 'pipeline_stage':'UNIT5_LEARNING_CLASSIFICATION_AND_PALACE_ARCHITECTURE_COMPLETE_F2','canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2',
 'source_status':'AUDITED_SCIENCE_LOCKED_F1_AND_ARCHITECTURE_LOCKED_F2','student_release':False,'preview_release':False,
 'canonical_records':152,'ced_atoms':34,'review_flags_resolved':37,'teacher_ppt_slides':112,'assessment_semantic_crosswalks':10,
 'journey_count':0,'scene_count':0,'memory_objects':0,'application_challenges':0,
 'architecture_journeys':len(JOURNEYS),'architecture_bundles':sum(len(j['bundles']) for j in JOURNEYS),'architecture_loci':len(loci),
 'palace_managed_records':len(loc_for),'scope_guard_records':len(SCOPE_IDS),'practice_only_records':len(PRACTICE),'confusable_sets':len(confdocs),
 'exact_name_targets':sum(bool(x['exact_name_recall']) for x in classification),
 'next_required_output':'F3 science-bearing scene briefs for all 50 loci; no polished Unit 5 narrative prose before F3 brief QA'
}
dump(U5/'status-f2.json',status);dump(U5/'status.json',status)
course=load(ROOT/'content'/'ap-biology'/'course.json')
for u in course['units']:
    if u['unit_id']=='unit-5':
        u.update({'status':status['status'],'journey_count':0,'scene_count':0,'canonical_lock':'LOCKED_F1','canonical_records':152,
                  'review_flags_resolved':37,'architecture_journeys':len(JOURNEYS),'architecture_loci':len(loci),'architecture_lock':'LOCKED_F2',
                  'student_release':False,'pipeline_stage':status['pipeline_stage'],'source_status':status['source_status']})
dump(ROOT/'content'/'ap-biology'/'course.json',course)
manifest={
 'schema':'memory-palace-v2-unit5-f2-release-1.0','generated_utc':GENERATED_UTC,'unit_id':'unit-5','release':'F2_LEARNING_ARCHITECTURE_LOCK',
 'student_release':False,'canonical_records':152,'palace_managed_records':len(loc_for),'scope_guard_records':len(SCOPE_IDS),'challenge_lab_records':len(PRACTICE),
 'journey_blueprints':len(JOURNEYS),'bundle_blueprints':sum(len(j['bundles']) for j in JOURNEYS),'permanent_locus_blueprints':len(loci),
 'confusable_sets':len(confdocs),'exact_name_targets':sum(bool(x['exact_name_recall']) for x in classification),
 'narrative_story_files':0,'student_runtime_memory_objects':0,
 'gate':'F2 fixes Unit 5 learning destinations and spatial architecture. F3 may specify science-bearing scene actions; polished story prose remains gated until F3 brief QA.'
}
dump(U5/'f2-release-manifest.json',manifest)

# Build the F2 lock after the workbook exists. Re-running this builder after workbook export seals it too.
locked=[
 'source/canonical-unit5-f1.json','source/coverage-manifest-f1.json',
 'architecture/learning-classification-f2.json','architecture/palace-architecture-f2.json',
 'status-f2.json','f2-release-manifest.json','audit/APBIO_Unit5_F2_Classification.xlsx'
]
lock={'schema':'memory-palace-v2-unit5-f2-lock-1.0','lock_status':'LOCKED_F2','student_release':False,'files':{}}
for rel in locked:
    p=U5/rel
    if p.exists(): lock['files'][rel]={'sha256':sha(p),'bytes':p.stat().st_size}
dump(U5/'content-lock-f2.json',lock)
print('built Unit 5 F2',architecture['counts'],classdoc['counts'])
