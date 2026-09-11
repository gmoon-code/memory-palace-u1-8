from __future__ import annotations
import json, hashlib, re
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content'/'ap-biology'/'unit-4'
SRC=U4/'source'/'canonical-unit4-f1.json'
ARCH=U4/'architecture'
ARCH.mkdir(parents=True,exist_ok=True)
GENERATED_UTC='2026-09-03T07:00:00+00:00'

RAW_LOCI=[
 ('U4-L01','U4-J1','U4-B01','Communication Compass','the central communication map separating contact, nearby chemical signaling, and distant chemical signaling',['direct-contact lane','communication-scale map','distance-signaling lane'],'U4-K-001',['U4-K-001','U4-K-039'],'COMMUNICATION_MODE_MAP'),
 ('U4-L02','U4-J1','U4-B01','Contact Junction Gallery','the side-by-side animal and plant cell-contact wall with a surface-recognition station',['animal gap-junction channel','direct surface-recognition contact','plant plasmodesmata channel'],'U4-K-040',['U4-K-040','U4-K-041','U4-K-042','U4-K-043'],'JUNCTION_AND_CONTACT_COMPARISON'),
 ('U4-L03','U4-J1','U4-B02','Local Signal Courtyard','the short-range signaling courtyard where a released ligand reaches only nearby receptor-bearing cells',['signal-emitting cell and local regulator','ligand-to-target-cell radius','nearby paracrine target cells'],'U4-K-044',['U4-K-002','U4-K-044','U4-K-045','U4-K-046','U4-K-047','U4-K-048','U4-K-049'],'LOCAL_SIGNAL_RADIUS'),
 ('U4-L04','U4-J1','U4-B02','Synaptic Dock','the neuron terminal dock where neurotransmitter crosses a narrow cleft to a receptor-bearing target',['presynaptic terminal','synaptic cleft and neurotransmitter release','postsynaptic target membrane'],'U4-K-050',['U4-K-050','U4-K-051','U4-K-052'],'SYNAPSE_CUTAWAY'),
 ('U4-L05','U4-J1','U4-B03','Endocrine Transit Hub','the circulation hub carrying hormones from endocrine cells to distant receptor-bearing targets',['hormone-releasing endocrine cell','bloodstream transport route','distant target cell and insulin example'],'U4-K-055',['U4-K-003','U4-K-013','U4-K-053','U4-K-054','U4-K-055','U4-K-057'],'ENDOCRINE_TRANSPORT_ROUTE'),
 ('U4-L06','U4-J1','U4-B03','Plant Hormone Route','the plant transport display showing tissue movement, vascular transport, and volatile ethylene diffusion',['source tissue','plant transport pathways','target tissue / volatile ethylene route'],'U4-K-056',['U4-K-056'],'PLANT_HORMONE_TRANSPORT'),

 ('U4-L07','U4-J2','U4-B04','Reception Checkpoint','the molecular checkpoint where only a chemically compatible ligand activates its receptor and changes receptor state',['approaching ligand candidates','receptor binding and state-change gate','activated receptor interior face'],'U4-K-058',['U4-K-004','U4-K-006','U4-K-007','U4-K-011','U4-K-058','U4-K-059','U4-K-060','U4-K-061'],'RECEPTION_SPECIFICITY_GATE'),
 ('U4-L08','U4-J2','U4-B04','Receptor Location Split','the plasma-membrane divide comparing cell-surface reception with signals that cross the bilayer to intracellular receptors',['extracellular ligand / surface receptor','plasma-membrane permeability boundary','cytoplasmic or nuclear receptor'],'U4-K-009',['U4-K-009','U4-K-062','U4-K-063','U4-K-064'],'RECEPTOR_LOCATION_COMPARISON'),
 ('U4-L09','U4-J2','U4-B04','Intracellular Signal Suite','the interior receptor suite comparing steroid, thyroid-hormone, and nitric-oxide signaling routes',['steroid-hormone receptor route','intracellular/nuclear target area','thyroid-hormone and nitric-oxide routes'],'U4-K-065',['U4-K-065','U4-K-066','U4-K-067'],'INTRACELLULAR_SIGNALING_COMPARISON'),
 ('U4-L10','U4-J2','U4-B05','GPCR Receptor Door','the seven-pass membrane receptor door that changes conformation when ligand binds',['extracellular ligand-binding face','seven-pass GPCR body','cytoplasmic G-protein interface'],'U4-K-081',['U4-K-008','U4-K-081'],'GPCR_MEMBRANE_MODEL'),
 ('U4-L11','U4-J2','U4-B05','G-Protein Switchboard','the membrane switchboard where GDP/GTP state changes control effector interaction and reset',['inactive GDP-bound G protein','GPCR-triggered GDP-to-GTP switch','effector activation and GTP-hydrolysis reset'],'U4-K-082',['U4-K-082','U4-K-083','U4-K-084','U4-K-085'],'G_PROTEIN_MOLECULAR_SWITCH'),
 ('U4-L12','U4-J2','U4-B05','Ligand-Gated Channel Gate','the ion-channel doorway whose open or closed state changes when ligand binds',['closed channel / ligand approach','ligand-binding channel gate','ion-flow response after channel-state change'],'U4-K-086',['U4-K-014','U4-K-086','U4-K-087'],'LIGAND_GATED_CHANNEL'),

 ('U4-L13','U4-J3','U4-B06','Transduction Relay Map','the intracellular route map carrying information from an activated receptor through interacting molecular components',['activated receptor input','signal-transduction pathway','downstream target branch'],'U4-K-068',['U4-K-068','U4-K-069'],'TRANSDUCTION_PATHWAY_MAP'),
 ('U4-L14','U4-J3','U4-B06','Kinase–Phosphatase Switchboard','the reversible protein-control board where kinases add phosphate and phosphatases remove it',['protein kinase / ATP phosphate transfer','target-protein state panel','protein phosphatase / phosphate removal'],'U4-K-070',['U4-K-070','U4-K-072','U4-K-073'],'PHOSPHORYLATION_SWITCH_COMPARISON'),
 ('U4-L15','U4-J3','U4-B06','Phosphorylation Cascade Staircase','the multi-step kinase staircase where one activated protein changes the state of the next',['upstream activated kinase','multi-step phosphorylation cascade','downstream activated targets'],'U4-K-071',['U4-K-005','U4-K-071'],'KINASE_CASCADE'),
 ('U4-L16','U4-J3','U4-B06','Second-Messenger Amplifier','the amplification chamber where enzymes generate many small intracellular messengers such as cAMP',['upstream enzyme / receptor input','second-messenger production and amplification','many downstream relay targets'],'U4-K-075',['U4-K-010','U4-K-012','U4-K-074','U4-K-075','U4-K-076'],'SECOND_MESSENGER_AMPLIFICATION'),
 ('U4-L17','U4-J3','U4-B07','Cellular Response Dispatch','the branching dispatch room where one pathway can change membrane transport, metabolism, gene expression, phenotype, or apoptosis',['membrane and metabolic response branches','cellular-response dispatch center','gene-expression / phenotype / apoptosis branches'],'U4-K-077',['U4-K-015','U4-K-077','U4-K-078','U4-K-079','U4-K-080','U4-K-088','U4-K-089'],'RESPONSE_BRANCHING'),
 ('U4-L18','U4-J3','U4-B07','Mutation Breakpoint Lab','the pathway test bench comparing receptor mutations, downstream-component mutations, and failed phosphatase control',['receptor-level mutation','signaling pathway breakpoint','downstream-component / phosphatase defect'],'U4-K-016',['U4-K-016','U4-K-090','U4-K-091','U4-K-093'],'MUTATION_PERTURBATION'),
 ('U4-L19','U4-J3','U4-B07','Agonist–Antagonist Console','the chemical perturbation console where pathway activity can be increased or inhibited without changing the DNA sequence',['pathway-activating chemical input','signaling activity readout','pathway-inhibiting chemical input'],'U4-K-017',['U4-K-017','U4-K-092'],'AGONIST_ANTAGONIST_PERTURBATION'),

 ('U4-L20','U4-J4','U4-B08','Homeostasis Control Map','the homeostatic control map organized around a regulated condition, reference range, and feedback path',['regulated variable / disturbance','homeostatic set-point or reference range','feedback path supporting internal stability'],'U4-K-094',['U4-K-018','U4-K-094','U4-K-095','U4-K-096','U4-K-108'],'HOMEOSTATIC_LOOP_MAP'),
 ('U4-L21','U4-J4','U4-B08','Sensor–Integrator–Effector Loop','the feedback circuit carrying a disturbance from sensor to integration and effector response',['stimulus and sensor/receptor','control / integration function','effector and response return path'],'U4-K-099',['U4-K-097','U4-K-098','U4-K-099','U4-K-100','U4-K-101'],'SENSOR_INTEGRATOR_EFFECTOR_LOOP'),
 ('U4-L22','U4-J4','U4-B09','Negative-Feedback Thermostat','the temperature-control loop where a deviation triggers responses that oppose the original change',['temperature deviation','negative-feedback control response','return toward regulated range'],'U4-K-019',['U4-K-019','U4-K-102'],'NEGATIVE_FEEDBACK_LOOP'),
 ('U4-L23','U4-J4','U4-B09','Blood-Glucose Regulator','the blood-glucose loop showing signaling-driven responses that counter a rise or fall in circulating glucose',['blood-glucose disturbance','hormonal feedback signaling','target-tissue response restoring range'],'U4-K-103',['U4-K-103'],'GLUCOSE_FEEDBACK_MODEL'),
 ('U4-L24','U4-J4','U4-B10','Positive-Feedback Amplifier','the reinforcing loop comparing childbirth, clotting, and fruit-ripening examples',['initial stimulus','self-reinforcing positive-feedback loop','amplified childbirth / clotting / ripening response'],'U4-K-020',['U4-K-020','U4-K-104','U4-K-105','U4-K-106'],'POSITIVE_FEEDBACK_LOOP'),
 ('U4-L25','U4-J4','U4-B10','Dysregulation Alarm','the failed-control display where disrupted feedback permits regulated conditions to move outside healthy ranges',['normally regulated condition','failed or inadequate feedback control','dysregulated state / disease risk'],'U4-K-107',['U4-K-107'],'HOMEOSTATIC_DYSREGULATION'),

 ('U4-L26','U4-J5','U4-B11','Genome Packing Archive','the DNA-packing archive moving from histones and nucleosomes into chromatin while preserving the whole genome',['DNA and histone components','nucleosome / chromatin packing hierarchy','genome-scale organization'],'U4-K-112',['U4-K-109','U4-K-110','U4-K-111','U4-K-112','U4-K-138'],'CHROMATIN_PACKING_HIERARCHY'),
 ('U4-L27','U4-J5','U4-B11','Chromosome Anatomy Workbench','the replicated-chromosome workbench labeling sister chromatids, centromere, and kinetochore on one physical chromosome',['one sister chromatid','centromere / kinetochore region','second sister chromatid'],'U4-K-113',['U4-K-113','U4-K-114','U4-K-115','U4-K-116','U4-K-117'],'CHROMOSOME_ANATOMY_MODEL'),
 ('U4-L28','U4-J5','U4-B11','Chromosome Sets Gallery','the comparison gallery separating prokaryotic and eukaryotic chromosome organization, homologs, ploidy, somatic cells, and gametes',['prokaryotic / haploid-side examples','homologous chromosome-set comparison','diploid somatic / gamete relationships'],'U4-K-120',['U4-K-118','U4-K-119','U4-K-120','U4-K-121','U4-K-122','U4-K-123','U4-K-124'],'CHROMOSOME_SET_AND_PLOIDY_COMPARISON'),
 ('U4-L29','U4-J5','U4-B12','Cell-Cycle Clock','the full circular cell-cycle clock separating interphase from M phase and locating G1, S, and G2 in sequence',['G1-S-G2 interphase arc','cell-cycle control clock','M-phase division arc'],'U4-K-022',['U4-K-021','U4-K-022','U4-K-125','U4-K-126'],'CELL_CYCLE_CLOCK'),
 ('U4-L30','U4-J5','U4-B12','G1 Growth Gate','the first interphase gate where a newly formed cell grows and performs normal functions before DNA synthesis',['post-division cell','G1 growth / cellular activity zone','commitment toward DNA synthesis'],'U4-K-023',['U4-K-023'],'G1_PHASE_SCENE'),
 ('U4-L31','U4-J5','U4-B12','S-Phase Replication Room','the DNA-copying room where DNA content and chromatid number double while centromere-counted chromosome number stays constant',['unreplicated chromosome set','S-phase DNA replication','replicated chromosome set / unchanged centromere count'],'U4-K-024',['U4-K-024','U4-K-134'],'S_PHASE_REPLICATION_AND_COUNT'),
 ('U4-L32','U4-J5','U4-B12','G2 Preparation Bay','the second interphase bay where the cell prepares for mitosis after DNA replication',['completed DNA replication','G2 growth and mitotic preparation','entry toward mitosis'],'U4-K-025',['U4-K-025'],'G2_PHASE_SCENE'),
 ('U4-L33','U4-J5','U4-B12','G0 Side Chamber','the side chamber outside the active division cycle showing reversible and long-term nondividing states',['cell-cycle exit','G0 nondividing state','possible reentry or long-term differentiated state'],'U4-K-026',['U4-K-026','U4-K-027'],'G0_BRANCH'),

 ('U4-L34','U4-J6','U4-B13','Mitosis Mission Control','the mitosis route overview showing replicated chromosomes segregated into daughter nuclei for growth, repair, or asexual reproduction',['replicated genome before mitosis','mitotic sequence control map','equivalent chromosome sets in daughter nuclei'],'U4-K-028',['U4-K-028','U4-K-029','U4-K-030'],'MITOSIS_SEQUENCE_OVERVIEW'),
 ('U4-L35','U4-J6','U4-B13','Prophase Spindle Setup','the early mitosis bay where chromosomes condense and centrosomes organize the forming spindle',['condensing replicated chromosomes','forming mitotic spindle','separating animal-cell centrosomes'],'U4-K-031',['U4-K-031','U4-K-127','U4-K-128'],'SPINDLE_FORMATION'),
 ('U4-L36','U4-J6','U4-B13','Prometaphase Kinetochore Access','the open-nucleus interval where spindle microtubules gain access to chromosome kinetochores',['nuclear-envelope breakdown','prometaphase attachment zone','spindle microtubules engaging kinetochores'],'U4-K-129',['U4-K-129'],'KINETOCHORE_ATTACHMENT_SEQUENCE'),
 ('U4-L37','U4-J6','U4-B13','Metaphase Plate Station','the equatorial alignment station where spindle forces position chromosomes at the metaphase plate',['one spindle pole','chromosomes aligned at metaphase plate','opposite spindle pole'],'U4-K-032',['U4-K-032','U4-K-130'],'METAPHASE_ALIGNMENT'),
 ('U4-L38','U4-J6','U4-B13','Anaphase Separation Track','the chromosome-separation track where sister chromatids become daughter chromosomes and move toward opposite poles',['one set of separating daughter chromosomes','anaphase spindle-dynamics zone','opposite daughter-chromosome set'],'U4-K-033',['U4-K-033','U4-K-135','U4-K-137'],'ANAPHASE_DYNAMICS_AND_COUNT'),
 ('U4-L39','U4-J6','U4-B13','Telophase Reassembly Room','the late-mitosis room where chromosomes decondense as spindle structures disappear and new nuclei form',['one chromosome set / reforming envelope','telophase reassembly zone','second chromosome set / reforming envelope'],'U4-K-034',['U4-K-034'],'TELOPHASE_REASSEMBLY'),
 ('U4-L40','U4-J6','U4-B14','Animal Cytokinesis Ring','the animal-cell division station where an actin–myosin contractile ring drives a cleavage furrow inward',['cell cortex and contractile ring','cleavage furrow constriction','two separating animal daughter cells'],'U4-K-035',['U4-K-035','U4-K-131','U4-K-132'],'ANIMAL_CYTOKINESIS'),
 ('U4-L41','U4-J6','U4-B14','Plant Cell-Plate Works','the plant-cell division station where Golgi-derived vesicles assemble a cell plate between daughter cells',['Golgi-derived vesicles','growing cell plate','new separating wall and membranes'],'U4-K-133',['U4-K-133'],'PLANT_CYTOKINESIS'),

 ('U4-L42','U4-J7','U4-B15','Checkpoint Command Map','the cell-cycle security map showing decision points where internal and external information can pause or permit progression',['incoming cellular / environmental information','checkpoint decision control','proceed, pause, exit, repair, or death outcomes'],'U4-K-141',['U4-K-036','U4-K-141'],'CHECKPOINT_DECISION_MAP'),
 ('U4-L43','U4-J7','U4-B15','G1 Commitment Gate','the G1 decision gate integrating growth conditions, signaling, and DNA integrity before S phase or G0',['G1 cell and external cues','G1 checkpoint commitment gate','S-phase entry or G0 branch'],'U4-K-142',['U4-K-142','U4-K-143'],'G1_COMMITMENT_DECISION'),
 ('U4-L44','U4-J7','U4-B15','G2 DNA-Integrity Gate','the premitotic checkpoint where incomplete replication or DNA damage can trigger arrest and repair responses',['DNA replication / damage status','G2 checkpoint and arrest control','repair / delayed mitotic entry / other response'],'U4-K-144',['U4-K-144','U4-K-146','U4-K-147'],'G2_DNA_DAMAGE_DECISION'),
 ('U4-L45','U4-J7','U4-B15','Spindle-Assembly Checkpoint','the metaphase security gate that blocks anaphase until kinetochore–microtubule attachments and alignment are adequate',['unattached / misattached chromosome','spindle-assembly checkpoint','permission for anaphase only after adequate attachment'],'U4-K-145',['U4-K-145'],'SPINDLE_CHECKPOINT'),
 ('U4-L46','U4-J7','U4-B15','Apoptosis Safety Exit','the regulated cell-death route that removes cells with severe damage or other dangerous states',['damage / death signal','regulated apoptosis program','orderly removal of the cell'],'U4-K-148',['U4-K-148'],'APOPTOSIS_SEQUENCE'),
 ('U4-L47','U4-J7','U4-B16','Cyclin–CDK Control Rack','the oscillating regulator rack where changing cyclin levels control CDK activity and phosphorylation of cell-cycle targets',['changing cyclin concentration','cyclin–CDK complex / kinase activity','phosphorylated targets driving cycle events'],'U4-K-037',['U4-K-037','U4-K-149','U4-K-150','U4-K-151'],'CYCLIN_CDK_OSCILLATION'),
 ('U4-L48','U4-J7','U4-B16','Growth and Attachment Signals Bay','the external-cue bay comparing growth-factor signaling, crowding signals, and anchorage requirements for normal proliferation',['growth-factor signaling','cell-density / contact environment','substrate / extracellular-matrix anchorage'],'U4-K-154',['U4-K-154','U4-K-155','U4-K-156'],'EXTRACELLULAR_GROWTH_CONSTRAINTS'),
 ('U4-L49','U4-J7','U4-B17','Cancer Control-Failure Board','the control-failure board linking accumulated driver alterations to checkpoint evasion, apoptosis evasion, and uncontrolled proliferation',['driver alterations / DNA-control failures','dysregulated cancer-cell control network','checkpoint and apoptosis evasion / proliferation'],'U4-K-157',['U4-K-038','U4-K-157','U4-K-158','U4-K-159','U4-K-160'],'CANCER_CONTROL_FAILURE'),
 ('U4-L50','U4-J7','U4-B17','Tumor Progression Corridor','the progression corridor distinguishing tumor formation, benign localization, malignant invasion, metastasis, and extended proliferative capacity',['localized tumor / benign state','malignant invasive progression','metastatic spread / extensive proliferation'],'U4-K-162',['U4-K-161','U4-K-162','U4-K-163','U4-K-164','U4-K-165'],'TUMOR_PROGRESSION'),
 ('U4-L51','U4-J7','U4-B17','Carcinogen Risk Bay','the DNA-damage risk bay comparing ultraviolet exposure with tobacco-smoke carcinogens',['UV exposure and DNA damage','cancer-risk reduction / damage context','tobacco-smoke carcinogens and DNA damage'],'U4-K-166',['U4-K-166','U4-K-167'],'CARCINOGEN_RISK_COMPARISON'),
]

JOURNEYS=[
 {'journey_id':'U4-J1','working_title':'Cellular Communications Exchange','content_focus':'Direct contact, local signals, synaptic communication, endocrine signaling, hormones, and plant long-distance signaling','setting_logic':'A communications exchange makes distance, medium, signal type, and target-cell access physically distinct before receptor mechanisms begin.','bundles':[
   {'bundle_id':'U4-B01','title':'Communication scale and direct contact','loci':['U4-L01','U4-L02']},
   {'bundle_id':'U4-B02','title':'Local and synaptic communication','loci':['U4-L03','U4-L04']},
   {'bundle_id':'U4-B03','title':'Long-distance communication','loci':['U4-L05','U4-L06']},]},
 {'journey_id':'U4-J2','working_title':'Signal Reception Gateway','content_focus':'Reception, ligand-receptor specificity, receptor location, intracellular receptors, GPCRs, G proteins, and ligand-gated channels','setting_logic':'A receptor gateway keeps extracellular signal recognition, membrane crossing constraints, receptor state change, and two membrane-receptor mechanisms spatially separate.','bundles':[
   {'bundle_id':'U4-B04','title':'Reception and receptor location','loci':['U4-L07','U4-L08','U4-L09']},
   {'bundle_id':'U4-B05','title':'Membrane-receptor mechanisms','loci':['U4-L10','U4-L11','U4-L12']},]},
 {'journey_id':'U4-J3','working_title':'Signal Relay Tower','content_focus':'Transduction, phosphorylation, kinases and phosphatases, second messengers, amplification, cellular responses, and pathway disruption','setting_logic':'A relay tower follows information after receptor activation through molecular switches and amplification before branching into responses and experimentally disrupted pathways.','bundles':[
   {'bundle_id':'U4-B06','title':'Intracellular relay and amplification','loci':['U4-L13','U4-L14','U4-L15','U4-L16']},
   {'bundle_id':'U4-B07','title':'Responses and pathway perturbation','loci':['U4-L17','U4-L18','U4-L19']},]},
 {'journey_id':'U4-J4','working_title':'Feedback Regulation Center','content_focus':'Homeostasis, feedback-loop components, negative feedback, positive feedback, and dysregulation','setting_logic':'A control center makes regulated variables, sensors, integrators, effectors, and reinforcing or opposing response directions visible as a single control-system logic.','bundles':[
   {'bundle_id':'U4-B08','title':'Homeostatic control-loop anatomy','loci':['U4-L20','U4-L21']},
   {'bundle_id':'U4-B09','title':'Negative-feedback control','loci':['U4-L22','U4-L23']},
   {'bundle_id':'U4-B10','title':'Positive feedback and failed regulation','loci':['U4-L24','U4-L25']},]},
 {'journey_id':'U4-J5','working_title':'Cell-Cycle Preparation Archive','content_focus':'Genome and chromosome organization, ploidy, interphase, G1, S, G2, G0, and chromosome-count logic across replication','setting_logic':'An archive-to-clock route prepares the learner to understand mitosis by first making chromosome identity, replicated structure, ploidy, and cell-cycle phase changes stable and visible.','bundles':[
   {'bundle_id':'U4-B11','title':'Genome and chromosome organization','loci':['U4-L26','U4-L27','U4-L28']},
   {'bundle_id':'U4-B12','title':'Interphase and cell-cycle states','loci':['U4-L29','U4-L30','U4-L31','U4-L32','U4-L33']},]},
 {'journey_id':'U4-J6','working_title':'Mitosis Transit Hall','content_focus':'Mitosis purpose and sequence, spindle formation, prometaphase, metaphase, anaphase, telophase, chromosome counting, and animal/plant cytokinesis','setting_logic':'A physical transit hall follows the same replicated chromosomes from condensation through attachment, alignment, separation, nuclear reassembly, and cytoplasmic division.','bundles':[
   {'bundle_id':'U4-B13','title':'Mitotic chromosome movement','loci':['U4-L34','U4-L35','U4-L36','U4-L37','U4-L38','U4-L39']},
   {'bundle_id':'U4-B14','title':'Cytokinesis mechanisms','loci':['U4-L40','U4-L41']},]},
 {'journey_id':'U4-J7','working_title':'Cell-Cycle Security Headquarters','content_focus':'Checkpoints, arrest, DNA-damage response, apoptosis, cyclin-CDK control, extracellular growth constraints, cancer, tumors, metastasis, and carcinogen risk','setting_logic':'A security headquarters treats cell-cycle progression as a sequence of permission decisions, then shows how signaling and regulatory failures can produce uncontrolled proliferation and cancer progression.','bundles':[
   {'bundle_id':'U4-B15','title':'Checkpoint decisions and cell safety','loci':['U4-L42','U4-L43','U4-L44','U4-L45','U4-L46']},
   {'bundle_id':'U4-B16','title':'Cyclin control and external proliferation cues','loci':['U4-L47','U4-L48']},
   {'bundle_id':'U4-B17','title':'Cancer-control failure and progression','loci':['U4-L49','U4-L50','U4-L51']},]},
]

PRACTICE=[
 {'challenge_id':'U4-CH-01','knowledge_id':'U4-K-170','title':'Communication-mode discrimination','type':'SCENARIO_CLASSIFICATION','prerequisite_loci':['U4-L02','U4-L03','U4-L04','U4-L05','U4-L06']},
 {'challenge_id':'U4-CH-02','knowledge_id':'U4-K-171','title':'Receptor structure-function inference','type':'STRUCTURE_FUNCTION_FRQ','prerequisite_loci':['U4-L07','U4-L08','U4-L10','U4-L12']},
 {'challenge_id':'U4-CH-03','knowledge_id':'U4-K-172','title':'Signaling-stage diagram interpretation','type':'MODEL_INTERPRETATION','prerequisite_loci':['U4-L07','U4-L13','U4-L16','U4-L17']},
 {'challenge_id':'U4-CH-04','knowledge_id':'U4-K-173','title':'Pathway-disruption prediction','type':'CAUSAL_PATHWAY_FRQ','prerequisite_loci':['U4-L14','U4-L15','U4-L16','U4-L18','U4-L19']},
 {'challenge_id':'U4-CH-05','knowledge_id':'U4-K-174','title':'Feedback graph and data reasoning','type':'DATA_MODEL_INTERPRETATION','prerequisite_loci':['U4-L20','U4-L22','U4-L24','U4-L25']},
 {'challenge_id':'U4-CH-06','knowledge_id':'U4-K-136','title':'Mitosis-stage visual identification','type':'IMAGE_STAGE_IDENTIFICATION','prerequisite_loci':['U4-L35','U4-L36','U4-L37','U4-L38','U4-L39','U4-L40','U4-L41']},
 {'challenge_id':'U4-CH-07','knowledge_id':'U4-K-139','title':'Diploid-from-gamete calculation','type':'QUANTITATIVE','prerequisite_loci':['U4-L28']},
 {'challenge_id':'U4-CH-08','knowledge_id':'U4-K-140','title':'Mitosis segregation error prediction','type':'CHROMOSOME_SEGREGATION_FRQ','prerequisite_loci':['U4-L27','U4-L38']},
 {'challenge_id':'U4-CH-09','knowledge_id':'U4-K-169','title':'Vinblastine spindle mechanism','type':'MECHANISM_PREDICTION','prerequisite_loci':['U4-L35','U4-L36','U4-L37','U4-L38','U4-L45']},
 {'challenge_id':'U4-CH-10','knowledge_id':'U4-K-175','title':'Cell-cycle phase data interpretation','type':'DATA_INTERPRETATION','prerequisite_loci':['U4-L29','U4-L30','U4-L31','U4-L32','U4-L33']},
 {'challenge_id':'U4-CH-11','knowledge_id':'U4-K-176','title':'Cell-cycle quantitative reasoning','type':'QUANTITATIVE_DATA','prerequisite_loci':['U4-L29','U4-L31','U4-L34']},
 {'challenge_id':'U4-CH-12','knowledge_id':'U4-K-177','title':'Chromosome-count reasoning','type':'QUANTITATIVE_MODEL_REASONING','prerequisite_loci':['U4-L27','U4-L31','U4-L38']},
 {'challenge_id':'U4-CH-13','knowledge_id':'U4-K-178','title':'Checkpoint disruption prediction','type':'CHECKPOINT_MECHANISM_FRQ','prerequisite_loci':['U4-L42','U4-L43','U4-L44','U4-L45','U4-L46']},
 {'challenge_id':'U4-CH-14','knowledge_id':'U4-K-179','title':'Cyclin-CDK graph interpretation','type':'GRAPH_INTERPRETATION','prerequisite_loci':['U4-L47']},
 {'challenge_id':'U4-CH-15','knowledge_id':'U4-K-180','title':'Cancer-control application','type':'EVIDENCE_MECHANISM_FRQ','prerequisite_loci':['U4-L48','U4-L49','U4-L50','U4-L51']},
]

CONFUSABLES=[
 ('U4-CF-01','Communication scale',['direct-contact signaling','local signaling','long-distance signaling'],['U4-K-040','U4-K-044','U4-K-053']),
 ('U4-CF-02','Direct intercellular channels',['gap junction','plasmodesmata'],['U4-K-041','U4-K-042']),
 ('U4-CF-03','Local signaling vocabulary',['local regulator','ligand','target cell'],['U4-K-045','U4-K-046','U4-K-047']),
 ('U4-CF-04','Named signaling modes',['paracrine signaling','synaptic signaling','endocrine signaling'],['U4-K-048','U4-K-050','U4-K-055']),
 ('U4-CF-05','Synaptic vocabulary',['neurotransmitter','synaptic cleft'],['U4-K-051','U4-K-052']),
 ('U4-CF-06','Chemical messenger categories',['local regulator','neurotransmitter','hormone'],['U4-K-045','U4-K-051','U4-K-054']),
 ('U4-CF-07','Core signaling stages',['reception','transduction','cellular response'],['U4-K-058','U4-K-068','U4-K-077']),
 ('U4-CF-08','Signal recognition roles',['ligand','receptor','target cell'],['U4-K-046','U4-K-059','U4-K-047']),
 ('U4-CF-09','Receptor location',['cell-surface receptor','intracellular receptor'],['U4-K-062','U4-K-063']),
 ('U4-CF-10','GPCR machinery',['G protein-coupled receptor (GPCR)','heterotrimeric G protein'],['U4-K-081','U4-K-082']),
 ('U4-CF-11','G-protein switch directions',['GDP-to-GTP exchange','GTP hydrolysis and switch reset'],['U4-K-083','U4-K-084']),
 ('U4-CF-12','Protein phosphorylation control',['protein kinase','protein phosphatase','dephosphorylation'],['U4-K-070','U4-K-072','U4-K-073']),
 ('U4-CF-13','Intracellular relay terms',['phosphorylation cascade','second messenger','signal amplification'],['U4-K-071','U4-K-075','U4-K-074']),
 ('U4-CF-14','First signal versus intracellular messenger',['ligand','second messenger','cyclic AMP (cAMP)'],['U4-K-046','U4-K-075','U4-K-076']),
 ('U4-CF-15','Cellular response branches',['membrane-permeability response','metabolic response','gene-expression response'],['U4-K-078','U4-K-079','U4-K-080']),
 ('U4-CF-16','Pathway mutation location',['receptor mutation effect','downstream-component mutation effect'],['U4-K-090','U4-K-091']),
 ('U4-CF-17','Feedback direction',['negative feedback','positive feedback'],['U4-K-019','U4-K-020']),
 ('U4-CF-18','Feedback-loop roles',['stimulus','sensor/receptor','control/integration function','effector','feedback response'],['U4-K-097','U4-K-098','U4-K-099','U4-K-100','U4-K-101']),
 ('U4-CF-19','Homeostatic reference terms',['homeostasis','set point'],['U4-K-094','U4-K-095']),
 ('U4-CF-20','Genome packing hierarchy',['histone','nucleosome','chromatin','chromosome'],['U4-K-110','U4-K-111','U4-K-112','U4-K-113']),
 ('U4-CF-21','Replicated chromosome relationships',['replicated chromosome','sister chromatid','homologous chromosomes'],['U4-K-114','U4-K-115','U4-K-120']),
 ('U4-CF-22','Chromosome attachment structures',['centromere','kinetochore'],['U4-K-116','U4-K-117']),
 ('U4-CF-23','Ploidy and cell type',['somatic cell','diploid','gamete','haploid'],['U4-K-121','U4-K-122','U4-K-123','U4-K-124']),
 ('U4-CF-24','Cell-cycle intervals',['interphase','M phase'],['U4-K-125','U4-K-126']),
 ('U4-CF-25','Cell-cycle states',['G1 phase','S phase','G2 phase','G0'],['U4-K-023','U4-K-024','U4-K-025','U4-K-143']),
 ('U4-CF-26','Mitotic stages',['prophase','prometaphase','metaphase','anaphase','telophase'],['U4-K-031','U4-K-129','U4-K-032','U4-K-033','U4-K-034']),
 ('U4-CF-27','Spindle geography',['mitotic spindle','centrosome','kinetochore','metaphase plate'],['U4-K-127','U4-K-128','U4-K-117','U4-K-130']),
 ('U4-CF-28','Cytokinesis structures',['cleavage furrow','contractile ring','cell plate'],['U4-K-131','U4-K-132','U4-K-133']),
 ('U4-CF-29','Cell-cycle checkpoints',['G1 checkpoint','G2 checkpoint','spindle assembly checkpoint'],['U4-K-142','U4-K-144','U4-K-145']),
 ('U4-CF-30','Cell-safety outcomes',['checkpoint','cell-cycle arrest','apoptosis'],['U4-K-141','U4-K-146','U4-K-148']),
 ('U4-CF-31','Cyclin-CDK vocabulary',['cyclin','cyclin-dependent kinase (CDK)','cyclin-CDK complex'],['U4-K-149','U4-K-150','U4-K-151']),
 ('U4-CF-32','External proliferation constraints',['growth-factor signaling','density-dependent inhibition','anchorage dependence'],['U4-K-154','U4-K-155','U4-K-156']),
 ('U4-CF-33','Tumor terminology',['cancer','tumor','benign tumor','malignant tumor','metastasis'],['U4-K-157','U4-K-162','U4-K-163','U4-K-164','U4-K-165']),
]
SCOPE_IDS={'U4-K-152','U4-K-153','U4-K-168'}

HIGH_NAME_TERMS={
 'U4-K-042','U4-K-048','U4-K-050','U4-K-055','U4-K-067','U4-K-073','U4-K-076','U4-K-081','U4-K-082','U4-K-083','U4-K-084','U4-K-086',
 'U4-K-094','U4-K-111','U4-K-112','U4-K-116','U4-K-117','U4-K-122','U4-K-124','U4-K-125','U4-K-127','U4-K-128','U4-K-129','U4-K-130',
 'U4-K-131','U4-K-132','U4-K-133','U4-K-141','U4-K-142','U4-K-144','U4-K-145','U4-K-148','U4-K-149','U4-K-150','U4-K-151','U4-K-155',
 'U4-K-156','U4-K-163','U4-K-164','U4-K-165'
}
MEDIUM_NAME_TERMS={
 'U4-K-041','U4-K-045','U4-K-046','U4-K-047','U4-K-051','U4-K-052','U4-K-054','U4-K-058','U4-K-059','U4-K-060','U4-K-061','U4-K-062',
 'U4-K-063','U4-K-068','U4-K-069','U4-K-070','U4-K-071','U4-K-072','U4-K-074','U4-K-075','U4-K-077','U4-K-095','U4-K-096','U4-K-098',
 'U4-K-099','U4-K-100','U4-K-109','U4-K-110','U4-K-113','U4-K-114','U4-K-115','U4-K-120','U4-K-121','U4-K-123','U4-K-126',
 'U4-K-031','U4-K-032','U4-K-033','U4-K-034','U4-K-035','U4-K-143','U4-K-146','U4-K-147','U4-K-154','U4-K-157','U4-K-158','U4-K-159',
 'U4-K-160','U4-K-161','U4-K-162','U4-K-166','U4-K-167'
}

MODEL_IDS={'U4-K-064','U4-K-083','U4-K-084','U4-K-087','U4-K-093','U4-K-103','U4-K-134','U4-K-135','U4-K-137','U4-K-147','U4-K-151'}

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,obj): Path(p).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

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
practice_ids={x['knowledge_id'] for x in PRACTICE}
classification=[]
for kid in sorted(records,key=lambda x:int(x.split('-')[-1])):
    r=records[kid]
    if kid in practice_ids:
        dest='CHALLENGE_LAB'; locus=None; role='APPLIED_TRANSFER'; visual='APPLICATION_PROMPT'; retrieval=['APPLIED_TRANSFER']
    elif kid in SCOPE_IDS:
        dest='SUPPORTING_NON_RUNTIME_SCOPE_GUARD'; locus=None; role='SCOPE_BOUNDARY'; visual='SCOPE_GUARD'; retrieval=['SCOPE_BOUNDARY_RECOGNITION']
    else:
        locus=loc_for[kid]
        dest='PALACE_PRIMARY_LOCUS' if kid in primary_set else 'PALACE_EMBEDDED'
        role='PRIMARY_ANCHOR' if kid in primary_set else 'EMBEDDED_SCIENCE'
        visual=next(l['visual_mode'] for l in loci if l['locus_id']==locus)
        retrieval=[]
        if r['exact_name_recall']: retrieval.append('EXACT_NAME_FROM_SCIENTIFIC_ROLE')
        retrieval.append('MEANING_OR_MECHANISM')
        if kid in MODEL_IDS: retrieval.append('MODEL_OR_CAUSAL_INTERPRETATION')
    if dest in {'CHALLENGE_LAB','SUPPORTING_NON_RUNTIME_SCOPE_GUARD'}:
        ns='NO_EXACT_NAME_GATE'
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

confdocs=[{'set_id':sid,'title':title,'terms':terms,'knowledge_ids':kids} for sid,title,terms,kids in CONFUSABLES]
architecture={
 'schema':'memory-palace-v2-unit4-f2-architecture-1.0','generated_utc':GENERATED_UTC,
 'unit':{'unit_id':'unit-4','title':'Cell Communication and Cell Cycle','canonical_source_lock':'F1','student_release':False,'narrative_generation_allowed':False},
 'design_rules':{
   'student_simplicity':'The learner will eventually see guided journeys, Review, and Challenge Lab; F2 classification machinery remains hidden.',
   'locus_rule':'A permanent locus represents one coherent causal, spatial, sequence, or comparison model rather than one vocabulary item.',
   'embedded_rule':'Closely related definitions, mechanisms, AP relationships, and teacher-required enrichment are embedded in the locus whose scientific action makes them intelligible.',
   'practice_rule':'Applied-transfer records remain in Challenge Lab and do not consume permanent palace locations.',
   'scope_guard_rule':'Scope guards protect AP boundaries and remain non-runtime support metadata.',
   'signal_rule':'Communication and transduction scenes must preserve signal source, distance/medium, receptor location, membrane boundaries, causal direction, and distinction between extracellular ligand and intracellular relay.',
   'cell_cycle_rule':'Cell-cycle scenes must preserve chromosome/chromatid identity, centromere/kinetochore distinction, DNA amount versus chromosome count, spindle geometry, and animal-versus-plant cytokinesis.',
   'regulation_rule':'Checkpoint, cyclin-CDK, apoptosis, and cancer scenes must represent regulation as conditional control rather than a deterministic one-factor script.',
   'narrative_gate':'No polished Unit 4 story prose may be authored until F3 scene briefs pass spatial, scientific, causal, and misconception-control QA.',
   'spelling_rule':'No mandatory spelling gate. Exact-name support is adaptive and optional sound cues are used only when they improve retrieval.'
 },
 'counts':{'canonical_records':len(records),'palace_managed_records':len(loc_for),'scope_guard_records':len(SCOPE_IDS),'practice_only_records':len(PRACTICE),
           'journeys':len(JOURNEYS),'bundles':sum(len(j['bundles']) for j in JOURNEYS),'permanent_loci':len(loci),'confusable_sets':len(confdocs)},
 'journeys':JOURNEYS,'loci':loci,'challenge_lab':PRACTICE,'confusable_sets':confdocs,
 'scope_guards':[{'knowledge_id':k,'canonical_label':records[k]['canonical_label'],'policy':'NON_RUNTIME_AP_SCOPE_BOUNDARY'} for k in sorted(SCOPE_IDS)]
}
classdoc={
 'schema':'memory-palace-v2-unit4-f2-classification-1.0','generated_utc':GENERATED_UTC,'unit_id':'unit-4','canonical_source_lock':'F1','counts':{},'records':classification
}
classdoc['counts']={
 'total':len(classification),'by_destination':dict(Counter(x['destination'] for x in classification)),
 'by_name_support':dict(Counter(x['name_support'] for x in classification)),
 'exact_name_targets':sum(bool(x['exact_name_recall']) and x['destination'].startswith('PALACE') for x in classification),
 'mandatory_spelling_targets':0
}
dump(ARCH/'learning-classification-f2.json',classdoc)
dump(ARCH/'palace-architecture-f2.json',architecture)

status={
 'unit_id':'unit-4','number':4,'title':'Cell Communication and Cell Cycle','status':'LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED',
 'pipeline_stage':'UNIT4_LEARNING_CLASSIFICATION_AND_PALACE_ARCHITECTURE_COMPLETE_F2','canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2',
 'source_status':'AUDITED_SCIENCE_LOCKED_F1_AND_ARCHITECTURE_LOCKED_F2','student_release':False,'preview_release':False,
 'canonical_records':180,'ced_atoms':38,'review_flags_resolved':39,'teacher_ppt_slides':85,'assessment_semantic_crosswalks':9,
 'journey_count':0,'scene_count':0,'memory_objects':0,'application_challenges':0,
 'architecture_journeys':len(JOURNEYS),'architecture_bundles':sum(len(j['bundles']) for j in JOURNEYS),'architecture_loci':len(loci),
 'palace_managed_records':len(loc_for),'scope_guard_records':len(SCOPE_IDS),'practice_only_records':len(PRACTICE),'confusable_sets':len(confdocs),
 'next_required_output':'F3 science-bearing scene briefs for all 51 loci; no polished Unit 4 narrative prose before F3 brief QA'
}
dump(U4/'status-f2.json',status)
dump(U4/'status.json',status)
course=load(ROOT/'content'/'ap-biology'/'course.json')
for u in course['units']:
    if u['unit_id']=='unit-4':
        u.update({'status':status['status'],'journey_count':0,'scene_count':0,'canonical_lock':'LOCKED_F1','canonical_records':180,'review_flags_resolved':39,
                  'architecture_journeys':len(JOURNEYS),'architecture_loci':len(loci),'architecture_lock':'LOCKED_F2','student_release':False,
                  'pipeline_stage':status['pipeline_stage'],'source_status':status['source_status']})
dump(ROOT/'content'/'ap-biology'/'course.json',course)
manifest={
 'schema':'memory-palace-v2-unit4-f2-release-1.0','generated_utc':GENERATED_UTC,'unit_id':'unit-4','release':'F2_LEARNING_ARCHITECTURE_LOCK',
 'student_release':False,'canonical_records':180,'palace_managed_records':len(loc_for),'scope_guard_records':len(SCOPE_IDS),'challenge_lab_records':len(PRACTICE),
 'journey_blueprints':len(JOURNEYS),'bundle_blueprints':sum(len(j['bundles']) for j in JOURNEYS),'permanent_locus_blueprints':len(loci),'confusable_sets':len(confdocs),
 'narrative_story_files':0,'student_runtime_memory_objects':0,
 'gate':'F2 fixes Unit 4 learning destinations and spatial architecture. F3 may specify science-bearing scene actions; polished story prose remains gated until F3 brief QA.'
}
dump(U4/'f2-release-manifest.json',manifest)
locked=[
 'source/canonical-unit4-f1.json',
 'source/coverage-manifest-f1.json',
 'architecture/learning-classification-f2.json',
 'architecture/palace-architecture-f2.json',
 'status-f2.json',
 'f2-release-manifest.json',
 'audit/APBIO_Unit4_F2_Classification.xlsx',
]
lock={'schema':'memory-palace-v2-unit4-f2-lock-1.0','lock_status':'LOCKED_F2','student_release':False,'files':{}}
for rel in locked:
    p=U4/rel
    if p.exists(): lock['files'][rel]={'sha256':sha(p),'bytes':p.stat().st_size}
dump(U4/'content-lock-f2.json',lock)
print('built Unit 4 F2',architecture['counts'],classdoc['counts'])
