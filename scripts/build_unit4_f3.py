from __future__ import annotations
import json, hashlib
from pathlib import Path
from collections import Counter, defaultdict

ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content'/'ap-biology'/'unit-4'
ARCH=U4/'architecture'; BRIEFS=U4/'briefs'; BRIEFS.mkdir(parents=True,exist_ok=True)
GEN='2026-09-04T01:10:00+00:00'

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,obj): Path(p).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

src=load(U4/'source/canonical-unit4-f1.json')
records={r['knowledge_id']:r for r in src['canonical_catalog']}
f2=load(ARCH/'palace-architecture-f2.json')
classif=load(ARCH/'learning-classification-f2.json')
class_by_id={r['knowledge_id']:r for r in classif['records']}

unit_guide={
 'name':'Dr. Mira Chen',
 'role':'cellular-systems investigator who accompanies the learner through all seven Unit 4 journeys',
 'visual_identity':'charcoal field jacket, clear protective glasses, compact white tablet with an amber route cursor and a thin violet tracing light',
 'behavior_rule':'Mira first fixes the learner in a stable physical location, then identifies the biological parts, activates only one diagnostic interaction at a time, and names terminology after the defining structure or action is visible.',
 'continuity_rule':'Mira is a guide, never a mnemonic substitute for a scientific term. Scientific structures retain conventional geometry and their real biological jobs.'
}

journey_specs={
'U4-J1':dict(
 premise='A multicellular communications exchange is misrouting messages because direct contact, local secretion, synaptic release, endocrine transport, and plant hormone movement have been collapsed into one generic idea of “cell signaling.”',
 mission='Rebuild the routing system by comparing who sends the message, how far it travels, what medium carries it, and which receptor-bearing target can respond.',
 stakes='If signaling distance and delivery mode remain vague, later receptor and pathway scenes will be memorized as names without a reliable way to distinguish how a message actually reaches its target.',
 continuity_object='Mira’s transparent route card, which always shows four fields—sender, messenger/contact, travel route or distance, and target—and is updated after every communication mode without pretending the card itself is a biological molecule.',
 recurring_scientific_cast=['signal-emitting or contacting cell','receptor-bearing target cell','the route or junction that connects them'],
 opening_image='The exchange floor is divided into a contact wall, a nearby signaling courtyard, a synaptic dock, a circulation rail, and a plant transport route, but every route is flashing the same undifferentiated SIGNAL label.',
 ending_payoff='The route card now separates direct contact, local paracrine and synaptic signaling, animal endocrine signaling, and plant long-distance signaling by mechanism and distance.',
 tone='comparative, spatial, communication-system focused'),
'U4-J2':dict(
 premise='Signals are arriving at a membrane gateway, yet inappropriate cells are responding and some receptors are activating without the correct ligand. The failure lies at the boundary between signal arrival and intracellular activation.',
 mission='Repair reception by making ligand-receptor specificity, receptor location, receptor state change, intracellular receptor routes, GPCR signaling, G-protein switching, and ligand-gated channels physically distinct.',
 stakes='Without a stable reception model, students can confuse ligand with receptor, GPCR with G protein, surface receptors with intracellular receptors, and ligand binding with the entire downstream response.',
 continuity_object='one receptor-state monitor that remains beside the membrane and records only three states—unbound/inactive, ligand-bound, and activated/changed—while different receptor mechanisms are tested.',
 recurring_scientific_cast=['ligand or signal molecule','receptor protein in its correct location','the intracellular interface or target affected after receptor activation'],
 opening_image='A membrane wall spans the gateway. Several ligand shapes approach from outside while receptor monitors on the surface and inside the cell disagree about which signal belongs where.',
 ending_payoff='The gateway responds only when the appropriate ligand reaches a compatible receptor in the correct location, and GPCR/G-protein and ligand-gated-channel mechanisms remain visibly different.',
 tone='molecular, boundary-focused, diagnostic'),
'U4-J3':dict(
 premise='The receptor gateway is repaired, but signals entering the intracellular relay tower still produce inconsistent responses. Some pathways fail to relay information, some over-amplify it, and others remain active after a mutation or chemical perturbation.',
 mission='Trace information from activated receptor through transduction, reversible phosphorylation, cascades, second messengers, amplification, cellular responses, and pathway perturbations.',
 stakes='The learner must understand how information is relayed without imagining that the extracellular ligand itself travels through the entire cytoplasm or that phosphorylation always means “on.”',
 continuity_object='a thin violet tracing light that marks where signaling information is being carried. It is explicitly a visualization overlay, not a molecule, and it moves only when the actual pathway component changes state.',
 recurring_scientific_cast=['activated receptor input','intracellular relay proteins or second messengers','cellular response machinery'],
 opening_image='At the base of the tower, an activated receptor glows at the membrane while the internal relay floors above it are dark and disconnected.',
 ending_payoff='The tracing light reaches a defined cellular response through a mechanistically correct relay, and mutation/chemical consoles can now predict where the pathway will fail or overactivate.',
 tone='mechanistic, sequential, perturbation-aware'),
'U4-J4':dict(
 premise='A regulation center is allowing internal conditions to drift because its sensor, control, effector, and feedback directions have been mixed together. Some loops oppose change while others reinforce it.',
 mission='Reconstruct homeostatic control from regulated variable and reference range through sensor, integration, effector, negative feedback, positive feedback, and dysregulation.',
 stakes='Feedback must be understood as directional control logic, not as “negative = bad” and “positive = good,” and homeostasis must remain dynamic rather than a perfectly fixed state.',
 continuity_object='one regulated-variable gauge whose needle can move above or below a reference range; the same gauge is carried through every feedback scene so response direction remains visible.',
 recurring_scientific_cast=['regulated-variable gauge','sensor/control/effector loop','response arrow that either opposes or reinforces the initial change'],
 opening_image='The central gauge needle is drifting outside its reference band while several response arrows point in contradictory directions.',
 ending_payoff='The gauge is held within a dynamic regulated range because the learner can identify each loop component and predict whether a response opposes or reinforces the disturbance.',
 tone='control-system, causal, homeostasis focused'),
'U4-J5':dict(
 premise='The cell-division archive cannot agree on what counts as a chromosome before and after DNA replication. Chromatin packing, sister chromatids, homologs, ploidy, and cell-cycle phases have been filed under conflicting labels.',
 mission='Build one stable chromosome model from DNA packaging through chromosome anatomy and chromosome sets, then carry the same identity through G1, S, G2, G0, and chromosome-count changes.',
 stakes='If chromosome identity and counting are wrong before mitosis starts, every later stage, ploidy calculation, and segregation prediction will inherit the error.',
 continuity_object='one color-coded eukaryotic chromosome set that begins as chromatin, is tracked as homologous chromosomes, and is followed through replication without changing chromosome identity merely because DNA amount changes.',
 recurring_scientific_cast=['tracked chromosome set','chromatin/chromosome structural model','cell-cycle phase clock'],
 opening_image='An archive table shows loose DNA, nucleosomes, condensed chromosomes, homologs, and replicated chromatids, but every object has been assigned the same CHROMOSOME COPY label.',
 ending_payoff='The archive now distinguishes genome, chromatin, chromosome, replicated chromosome, sister chromatid, homolog, ploidy, and the G1–S–G2–G0 states with correct chromosome-count logic.',
 tone='structural, bookkeeping-oriented, precise'),
'U4-J6':dict(
 premise='A mitosis transit hall must deliver equivalent chromosome sets to opposite daughter nuclei, but spindle attachment, stage order, chromosome counting, and cytokinesis mechanisms are out of sequence.',
 mission='Follow the same replicated chromosomes through prophase, prometaphase, metaphase, anaphase, telophase, and then compare animal and plant cytokinesis.',
 stakes='The learner must see what physically changes at each stage and must keep chromosome movement, nuclear division, and cytoplasmic division distinct.',
 continuity_object='the same small set of replicated chromosomes from Journey 5, with sister chromatids visibly connected until anaphase and then tracked as daughter chromosomes to opposite poles.',
 recurring_scientific_cast=['tracked replicated chromosomes','mitotic spindle and attachment structures','cell boundary or division machinery'],
 opening_image='Replicated chromosomes enter the transit hall at one end while spindle poles, attachment tracks, an equatorial alignment line, and two cytokinesis exits wait ahead.',
 ending_payoff='Equivalent chromosome sets occupy newly formed daughter nuclei, and the learner can distinguish the animal contractile-ring route from the plant cell-plate route.',
 tone='kinetic, spatial, same-chromosome continuity'),
'U4-J7':dict(
 premise='The cell-cycle security headquarters is issuing division permission even when DNA is damaged, chromosomes are unattached, growth conditions are poor, or malignant control failures are accumulating.',
 mission='Restore checkpoint decisions, arrest and repair options, apoptosis, cyclin-CDK regulation, external growth constraints, and the distinction between normal proliferation control and cancer progression.',
 stakes='Students must understand cancer as accumulated failure of regulatory systems rather than a single mutation, a fixed mutation count, or an inevitable progression from every benign tumor.',
 continuity_object='one model-cell security file that carries DNA status, spindle-attachment status, growth cues, cyclin/CDK state, and the current decision—proceed, pause, repair, exit, die, or progress abnormally.',
 recurring_scientific_cast=['model cell security file','checkpoint or regulatory control machinery','cell fate/proliferation outcome'],
 opening_image='A model cell arrives with a damaged-DNA warning and an incomplete attachment report, yet the headquarters has stamped PROCEED across its file.',
 ending_payoff='Normal cells receive context-dependent permission or safety responses, while cancer progression is recognized as a multistep loss of control involving proliferation, survival, invasion, and spread.',
 tone='decision-system, safety-oriented, medically careful')
}

# Designer-facing science-bearing mechanics. These are NOT polished student story sentences.
core={
'U4-L01':[
 'Place the same sender and target on the communication-scale map, first touching, then separated by a short local distance, then separated by a body-scale distance; change only the communication route so distance is the diagnostic feature.',
 'Make the contact lane work without a secreted long-range messenger, make the local lane deliver only within a nearby radius, and make the distance lane require transport or another long-range route before the target can receive the signal.',
 'Update Mira’s route card after each case so the learner leaves with sender, route, distance, and target as the four comparison dimensions rather than one vague category called signaling.'
],
'U4-L02':[
 'Open the animal gap-junction model and pass only suitable ions/small signaling molecules through the intercellular channel; keep large cargo blocked so “direct connection” never becomes “anything passes freely.”',
 'On the plant side, show plasmodesmata crossing the cell wall and connecting neighboring cytoplasms while preserving regulated, selective transport rather than an unrestricted hole.',
 'At the center contact station, bring an antigen-presenting cell and T cell surface molecules together to demonstrate direct surface recognition without requiring material to cross an intercellular channel.'
],
'U4-L03':[
 'Release a local regulator from one signaling cell and draw a short diffusion radius that reaches several nearby cells while leaving a more distant cell outside the effective local field.',
 'Give only one nearby cell the appropriate receptor and downstream machinery; the ligand may reach several cells, but only the receptor-bearing target cell produces the response.',
 'Run a growth-factor example through the same geometry so paracrine signaling is encoded as local signaling to nearby targets, not as a requirement for membranes to be directly adjacent.'
],
'U4-L04':[
 'Trigger vesicular neurotransmitter release from the presynaptic terminal and let the molecules diffuse across the narrow extracellular synaptic cleft rather than along the neuron as the neurotransmitter itself.',
 'Bind neurotransmitter to receptors on the postsynaptic target membrane and show the target response beginning only after receptor interaction.',
 'Freeze the dock with presynaptic terminal, cleft, and postsynaptic target in separate zones so neurotransmitter and synaptic cleft cannot collapse into the same vocabulary item.'
],
'U4-L05':[
 'Release a hormone from an endocrine cell into the bloodstream route and carry it past many nonresponsive cells before it reaches a distant cell with the appropriate receptor.',
 'Overlay insulin as one specific endocrine example: pancreatic beta-cell release follows elevated blood glucose, and receptor-bearing target tissues respond; do not turn insulin into the definition of hormone.',
 'Compare this body-scale transport with the short-range courtyard route so endocrine signaling is distinguished by long-distance distribution through circulation, not merely by the word hormone.'
],
'U4-L06':[
 'Release a plant hormone from source tissue and show one route moving through adjacent tissues and vascular pathways toward a target region without claiming every plant hormone uses the same transport tissue.',
 'Run ethylene through a separate volatile route where the gaseous signal diffuses through air spaces or surrounding air to responsive tissue.',
 'End with plant long-distance signaling as a family of movement strategies: tissue/vascular transport for many signals and airborne diffusion as a special case for volatile ethylene.'
],
'U4-L07':[
 'Present several ligand candidates to one receptor binding domain and allow only the chemically and structurally compatible ligand to bind, establishing specificity before any intracellular event occurs.',
 'After binding, change the receptor conformation or functional state at the center gate and illuminate the intracellular face to mark the transition from reception toward transduction.',
 'Keep ligand outside the downstream pathway and label the target cell as responsive because it possesses the suitable receptor and intracellular machinery; reception is detection, not the entire response.'
],
'U4-L08':[
 'Place a hydrophilic/large signal at the left surface-receptor route and prevent it from freely crossing the lipid bilayer, while a sufficiently small or hydrophobic signal is allowed to enter the cell in the comparison route.',
 'Position one receptor in the plasma membrane and another in the cytoplasm or nucleus, then connect each ligand only to the receptor location compatible with membrane permeability.',
 'Treat permeability as a governing principle rather than an absolute memorization rule about every molecule; receptor location is the central distinction.'
],
'U4-L09':[
 'Let a steroid-hormone example cross the membrane and bind an intracellular receptor that can influence gene expression, preserving the receptor as the signaling target rather than the hormone acting directly on DNA by itself.',
 'Place thyroid hormone at a nuclear-receptor route and nitric oxide at a small-gas route that diffuses through membranes and activates an intracellular target such as soluble guanylyl cyclase.',
 'Keep these as three scientifically valid examples of intracellular signaling while making clear that the AP-level principle is receptor location and membrane permeability, not memorization of every example class.'
],
'U4-L10':[
 'Embed a conventional seven-transmembrane GPCR in the membrane, bind ligand to the extracellular-facing region, and visibly change receptor conformation without allowing the ligand to cross through the receptor.',
 'Transmit the receptor state change to the cytoplasmic G-protein interface and leave the heterotrimeric G protein separate from the receptor body.',
 'Keep other membrane-receptor silhouettes in the background so GPCR remains an important example rather than being taught as one of only two possible membrane-receptor categories.'
],
'U4-L11':[
 'Start the heterotrimeric G protein in the inactive GDP-bound state beside an activated GPCR, then use receptor activation to promote GDP release and GTP binding.',
 'Allow the GTP-bound active component to regulate an effector enzyme or channel, making the nucleotide state a molecular switch that changes downstream signaling.',
 'Hydrolyze GTP to GDP and reset the switch; explicitly preserve GTP’s role here as switch control rather than portraying it mainly as an ATP-like energy fuel.'
],
'U4-L12':[
 'Keep the ligand-gated ion channel closed while no ligand is bound, then bind the ligand and change the channel’s open probability or gate state.',
 'Allow only the channel’s relevant ions to move down their electrochemical driving forces after the gate opens, or reduce ion flux when the gate closes.',
 'Show the resulting membrane/electrical or ionic change on the right so receptor activation, ion movement, and cellular response remain causally ordered.'
],
'U4-L13':[
 'Start with an activated receptor at the membrane and activate a sequence of intracellular relay components one after another without moving the extracellular ligand through the cytoplasm.',
 'Use the violet tracing light only as an information-flow overlay that advances when an actual molecular component changes state, never as a substitute molecule inside the pathway.',
 'Branch the transduction route toward a downstream target so the learner can separate reception at the receptor from transduction through the pathway and the later cellular response.'
],
'U4-L14':[
 'Use ATP at the left kinase station to transfer a phosphate group to a target protein, then show that phosphorylation changes the target’s state or activity without assuming the change must be activation.',
 'Move the same target to the phosphatase station and remove the phosphate group through dephosphorylation, again allowing the effect to depend on the specific protein rather than forcing “off.”',
 'Hold kinase and phosphatase on opposite sides of the same target-state panel so addition and removal of phosphate are retrieved as opposite chemical actions, not as universal on/off meanings.'
],
'U4-L15':[
 'Activate one upstream protein kinase and let it phosphorylate multiple copies of the next kinase layer, then continue the relay through at least one additional kinase layer.',
 'Show each layer changing the state of the next through protein modification while keeping the original receptor physically upstream and outside the staircase.',
 'At the bottom, reveal multiple downstream activated targets to make a phosphorylation cascade both a relay and a possible amplification mechanism while preserving target-dependent effects.'
],
'U4-L16':[
 'Activate an upstream enzyme such as adenylyl cyclase and convert a relatively small input into many molecules of a small intracellular messenger, using cAMP as the named example.',
 'Distribute the cAMP molecules to multiple downstream targets so one receptor-level event can influence many intracellular components and visibly amplify the signal.',
 'Keep the extracellular ligand at the membrane and the second messenger inside the cell so ligand, second messenger, cAMP, and amplification remain physically distinguishable.'
],
'U4-L17':[
 'Send the same completed signaling input into separate response branches and change membrane permeability or transport in one branch, metabolic enzyme activity in another, and gene expression in a third.',
 'Add phenotype/function as the integrated consequence of these molecular changes rather than treating phenotype as a separate messenger traveling through the pathway.',
 'Include regulated apoptosis as one possible signaling outcome while keeping it distinct from the general definition of cellular response.'
],
'U4-L18':[
 'Introduce a receptor mutation that changes signal detection or receptor activation while leaving downstream components intact, then record how pathway output changes.',
 'Reset the system and introduce a downstream-component mutation so reception remains normal but the relay or response changes after the breakpoint.',
 'Finally alter phosphatase function and predict pathway state from the specific target relationship instead of assuming every phosphatase defect simply increases signaling in all pathways.'
],
'U4-L19':[
 'Apply a pathway-activating chemical input and observe increased signaling activity without changing the DNA sequence, then wash/reset the system.',
 'Apply a pathway-inhibiting chemical input at a defined receptor or downstream step and observe reduced pathway activity, again without requiring a mutation.',
 'Use the activity readout to separate chemical agonism/activation and antagonism/inhibition from genetic pathway alterations introduced in the previous lab.'
],
'U4-L20':[
 'Move the regulated-variable gauge above and below its reference range and show that homeostatic control responds to deviation rather than holding the variable at one mathematically fixed value.',
 'Connect cell signaling to the feedback path that coordinates internal stability, using the reference range/set point as a control target rather than a single universal number.',
 'Return the gauge toward the regulated range and leave small normal fluctuations visible so homeostasis is encoded as dynamic regulation, not static constancy.'
],
'U4-L21':[
 'Introduce a stimulus or disturbance and let a sensor/receptor detect a relevant change, then pass information to a control/integration function that evaluates the condition.',
 'Activate an effector that produces a response capable of changing the regulated variable, then loop the consequence back toward the original condition.',
 'Run the loop once with a molecular/cellular example so sensor, integrator, and effector are not restricted to sensory organ, brain, and muscle/gland anatomy.'
],
'U4-L22':[
 'Move the temperature gauge away from its regulated range and trigger a response whose direction opposes the initial deviation, whether the deviation is upward or downward.',
 'As the response succeeds, reduce the original stimulus and weaken the corrective drive, creating a self-limiting negative-feedback loop.',
 'Keep “negative” attached to direction of effect on the original change, not to biological harm, badness, or low numerical value.'
],
'U4-L23':[
 'Raise blood glucose and activate insulin-associated responses that promote glucose uptake/storage in responsive tissues, moving the gauge back toward its regulated range.',
 'Lower blood glucose and activate glucagon-associated responses that increase glucose availability, again moving the gauge back toward the regulated range.',
 'Place the opposing hormonal responses on opposite sides of the same glucose gauge so both are recognized as negative-feedback control of one regulated variable.'
],
'U4-L24':[
 'Start a small triggering event and make each response increase the process that generated the response, producing a visibly reinforcing loop rather than restoring a set point.',
 'Run childbirth through cervical stretch, oxytocin release, stronger uterine contractions, and greater stretch until delivery ends the loop; run clotting as recruitment/activation until the breach is sealed.',
 'Use fruit ripening as a separate ethylene example and make every loop stop because an external endpoint changes the system, not because positive feedback automatically stabilizes itself.'
],
'U4-L25':[
 'Disable or weaken an appropriate feedback response and allow the regulated-variable gauge to remain outside its healthy range despite continued disturbance.',
 'Show downstream physiological consequences accumulating as regulation fails, while preserving disease as a broader category with many possible causes.',
 'Connect dysregulated glucose control and dysregulated cell proliferation as examples of failed regulation without defining all disease as nothing more than loss of homeostasis.'
],
'U4-L26':[
 'Wrap eukaryotic DNA around histone protein cores to form nucleosomes, then fold many nucleosomes into higher-order chromatin while leaving the DNA-protein composition visible.',
 'Zoom from one nucleosome to a longer chromatin fiber and then to chromosome-scale organization without implying that DNA becomes a chromosome only when mitosis begins.',
 'Frame the genome as the complete genetic material and preserve chromatin as the DNA-protein material of eukaryotic chromosomes throughout the cell cycle.'
],
'U4-L27':[
 'Place one replicated chromosome on the workbench with two sister chromatids side by side, joined at the centromere region but still counted as one chromosome before separation.',
 'Assemble a kinetochore protein complex at the centromere of each chromatid and mark it as the future spindle-microtubule attachment site.',
 'Rotate the model so sister chromatid, centromere, and kinetochore remain physically distinct, and keep homologous chromosomes out of this workbench until the next gallery.'
],
'U4-L28':[
 'Compare a common prokaryotic main circular chromosome pattern with eukaryotic linear nuclear chromosomes while leaving visible notes that real species show exceptions in number and topology.',
 'Place homologous chromosomes as a pair with corresponding gene loci but potentially different alleles; contrast that pair with the identical-copy relationship of sister chromatids from the previous workbench.',
 'Build diploid somatic cells with two chromosome sets and haploid gametes with one set, while showing gametes as products of meiosis rather than cells that themselves perform meiosis.'
],
'U4-L29':[
 'Run the cell-cycle clock through G1, S, and G2 as interphase, then through M phase, keeping the phases in one continuous circular sequence.',
 'Show interphase as commonly the longest portion without assigning a universal fixed percentage, and define M phase as mitosis plus usually cytokinesis.',
 'Place regulatory decision markers around the clock to prepare for later checkpoint control without turning the phase names themselves into checkpoints.'
],
'U4-L30':[
 'Begin with a newly divided cell containing unreplicated chromosomes and let it grow, synthesize cellular components, and carry out normal functions during G1.',
 'Keep DNA synthesis physically outside the G1 zone and leave the chromosome set unreplicated throughout this room, so ordinary growth and cellular function cannot be confused with the DNA-copying chemistry that begins only in S phase.',
 'At the exit, place the cell near a future commitment decision without equating the entire G1 phase with the G1 checkpoint.'
],
'U4-L31':[
 'Start with unreplicated chromosomes and replicate each DNA molecule during S phase so each chromosome now consists of two sister chromatids.',
 'Double the DNA-content and chromatid gauges while keeping the centromere-counted chromosome-number gauge unchanged before sister-chromatid separation.',
 'Leave the replicated chromosomes visibly prepared for later mitosis so “DNA doubled” and “chromosome number doubled” cannot be treated as equivalent statements.'
],
'U4-L32':[
 'Bring the cell into G2 only after DNA replication is complete and continue growth, protein synthesis, and preparation for mitosis.',
 'Keep the replicated chromosomes unchanged while the cell prepares the machinery and conditions needed for M phase rather than replicating DNA a second time.',
 'Route the prepared cell toward the premitotic integrity gate that will later decide whether entry into mitosis is permitted.'
],
'U4-L33':[
 'Branch one cell out of the active cycle from a G1-associated decision into G0 and stop division while ordinary specialized cellular functions continue.',
 'Allow one example cell to receive appropriate cues and reenter the cycle, while a second terminally differentiated example remains nondividing for a long period.',
 'Keep G0 outside the active G1–S–G2–M loop so it is remembered as a nondividing state with variable reversibility, not as an inevitable permanent fate.'
],
'U4-L34':[
 'Place replicated chromosomes before mitosis on the left and equivalent chromosome sets in two future daughter nuclei on the right, then reveal the prophase-to-telophase route between them.',
 'Connect mitosis to growth, tissue repair, and asexual reproduction without defining mitosis as the process that creates diploid cells in every organism or context.',
 'Keep cytokinesis outside the nuclear-segregation map until the final transit stations so mitosis and cytoplasmic division remain distinct processes.'
],
'U4-L35':[
 'Condense the tracked replicated chromosomes into visibly compact structures and begin assembling the microtubule-based mitotic spindle.',
 'Move animal-cell centrosomes toward opposite poles while preserving centrosomes as an animal-cell organizing example rather than a universal plant-cell requirement.',
 'Leave the nuclear boundary not yet fully opened so the next station has a clear mechanistic reason to exist: spindle microtubules still need access to kinetochores.'
],
'U4-L36':[
 'Break down the nuclear envelope and allow spindle microtubules to enter the chromosome region where the kinetochores are exposed.',
 'Attach microtubules to kinetochores on sister chromatids and begin dynamic chromosome movement without prematurely aligning every chromosome at the equator.',
 'Label this interval prometaphase as valid teacher enrichment while keeping the current AP stage framework capable of grouping this detail within the broader mitotic sequence.'
],
'U4-L37':[
 'Use microtubule attachments from opposite poles to position the tracked replicated chromosomes with their centromere regions near the cell equator.',
 'Draw the metaphase plate as an imaginary equatorial plane rather than a physical cellular structure and align chromosomes relative to that plane.',
 'Hold the system at alignment until attachments are adequate, creating a direct handoff to the later spindle-assembly checkpoint and to anaphase separation.'
],
'U4-L38':[
 'Release sister-chromatid cohesion and separate each pair so every former sister chromatid now counts as an individual daughter chromosome.',
 'Move daughter chromosomes toward opposite poles through kinetochore-microtubule dynamics and spindle forces while also allowing spindle elongation processes to contribute.',
 'Update the chromosome-count gauge to show the transient doubling within the still-undivided cell, then preserve equal sets at opposite poles for telophase.'
],
'U4-L39':[
 'Disassemble much of the mitotic spindle as the two separated daughter-chromosome sets arrive at opposite ends of the cell, while keeping the chromosome sets visibly distinct and already separated before nuclear envelopes begin to re-form.',
 'Re-form nuclear envelopes around each chromosome set and allow chromosomes to begin decondensing back toward less compact chromatin.',
 'Keep the cytoplasm still continuous so completion of nuclear reassembly does not falsely imply that cytokinesis has already occurred.'
],
'U4-L40':[
 'Assemble an actin–myosin contractile ring beneath the animal-cell cortex at the division plane and begin constricting the ring.',
 'Pull the plasma membrane inward to form a cleavage furrow and continue constriction until the cytoplasm separates into two daughter cells.',
 'Keep cytokinesis labeled as cytoplasmic division after/overlapping late mitosis, not as another mitotic chromosome-segregation stage.'
],
'U4-L41':[
 'Deliver Golgi-derived vesicles toward the center of a plant cell, where they fuse into a growing cell plate rather than pulling the existing wall inward.',
 'Expand the cell plate outward until it connects with the existing plasma membrane and contributes new membranes and wall material between daughters.',
 'Hold the rigid parent cell wall in place while the new cell plate expands from the center outward, making the contrast with an animal cleavage furrow physically unavoidable and preventing the learner from imagining that plant cytokinesis pinches inward.'
],
'U4-L42':[
 'Feed internal and external information into a checkpoint decision node and allow the cell to proceed, pause, exit, repair, or activate another safety response depending on the information.',
 'Place decision nodes at different parts of the cycle without turning “checkpoint” into a new phase or a single universal molecular mechanism.',
 'Use the model-cell security file to record the decision and the evidence that produced it, preparing the learner for specific G1, G2, and spindle checkpoints.'
],
'U4-L43':[
 'Present the G1 cell with growth conditions, external signaling cues, and a DNA-integrity report before permitting commitment toward S phase.',
 'When conditions are unsuitable, branch the file toward pause or G0; when conditions are appropriate, authorize progression toward DNA synthesis.',
 'Treat the G1 checkpoint as a major commitment decision without ranking it as universally the “most important” checkpoint in every biological context.'
],
'U4-L44':[
 'Present incomplete DNA replication or a persistent DNA-damage signal to the G2 checkpoint and visibly block immediate entry into mitosis, so the learner sees the checkpoint as a permission decision made before chromosome segregation begins.',
 'Route the cell into cycle arrest and a DNA-damage response that can support repair, continued arrest, senescence, apoptosis, or other context-dependent outcomes.',
 'Permit mitotic entry only after the premitotic status is acceptable; do not encode irreparable damage as deterministically producing apoptosis in every cell.'
],
'U4-L45':[
 'Place one chromosome with inadequate kinetochore-microtubule attachment at metaphase and keep the anaphase permission gate closed.',
 'Correct the attachment/alignment state and then release the gate, showing that the spindle assembly checkpoint protects chromosome segregation before anaphase begins.',
 'Keep microtubule-disrupting drugs conceptually upstream of failed attachment/checkpoint activation so anaphase is understood as prevented rather than as the first stage directly damaged.'
],
'U4-L46':[
 'Send a severely damaged or otherwise dangerous model cell into a regulated death program rather than allowing uncontrolled rupture or continued division.',
 'Show orderly dismantling and removal features as a programmed cell-fate response while keeping the molecular details only as needed for the canonical Unit 4 scope.',
 'Return the security file with DIVISION STOPPED / CELL REMOVED so apoptosis is retrieved as regulated programmed cell death, not simply “cell death” in general.'
],
'U4-L47':[
 'Raise cyclin concentration on the left and allow cyclin binding to increase activity of the corresponding cyclin-dependent kinase in the central rack.',
 'Use the active cyclin–CDK complex to phosphorylate specific target proteins that promote or regulate cell-cycle events, then reduce activity as regulatory conditions change.',
 'Keep the general cyclin–CDK interaction as the required mechanism while blocking memorization of arbitrary specific cyclin/CDK pair catalogs as an AP requirement.'
],
'U4-L48':[
 'Apply a growth-factor signal and route it through signaling pathways that can influence cyclin/CDK activity and proliferation decisions.',
 'Increase cell density/contact and reduce proliferation in a normal-cell model, then test an attached versus unattached substrate to demonstrate anchorage dependence.',
 'Keep growth factors as extracellular signaling molecules rather than universal hormones, and mark density-dependent inhibition and anchorage dependence as teacher enrichment rather than universal AP exact-term requirements.'
],
'U4-L49':[
 'Accumulate multiple driver alterations affecting proliferation control, genome maintenance, cell death, or related regulatory systems rather than assigning cancer a fixed mutation threshold.',
 'Let checkpoint evasion and reduced apoptosis remove two normal restraints, allowing abnormal proliferation and additional malignant properties to emerge over time.',
 'Use the control-failure board to define cancer as dysregulated cell behavior arising from genetic/epigenetic alterations, not simply “cells divide fast.”'
],
'U4-L50':[
 'Begin with a localized abnormal mass and distinguish a benign tumor that remains noninvasive from a malignant tumor that invades surrounding tissue.',
 'Allow malignant cells to enter a transport route, leave the primary site, and establish a secondary growth at a distant location to demonstrate metastasis.',
 'Show extensive/indefinite proliferative capacity as a property many transformed populations can acquire without claiming every individual cancer cell literally divides forever or that every benign tumor is “cancer later.”'
],
'U4-L51':[
 'Expose one DNA model to ultraviolet radiation and display DNA damage that can increase skin-cancer risk, then reduce exposure with appropriate protective behavior.',
 'Expose a second DNA model to tobacco-smoke carcinogens and show increased DNA-damage/mutation risk while keeping nicotine labeled primarily as the addictive agent rather than the principal mutagenic carcinogen.',
 'Remove unsupported generic claims about dehydration or “fatty foods” as direct cancer mechanisms and leave the bay focused on evidence-based carcinogen risk and risk reduction.'
]
}

# High-risk authoring constraints that must survive into eventual student prose.
special_guards={
'U4-L02':['Direct intercellular connections are regulated/selective; never say cytoplasmic material passes “freely” without qualification.','Gap junctions are animal intercellular channels; plasmodesmata are plant cell-wall-spanning channels with different structure.'],
'U4-L03':['Paracrine means local signaling to nearby target cells, not necessarily immediately adjacent cells.','A cell is a target only if it has a suitable receptor and downstream machinery; ligand exposure alone does not make every nearby cell respond.'],
'U4-L05':['Hormone is a signaling molecule category, not a synonym for protein and not a guarantee that every cell encountered will respond.'],
'U4-L06':['Airborne ethylene is a special volatile route; do not generalize air transport to all plant hormones.'],
'U4-L07':['The ligand carries extracellular information but usually does not itself travel through the intracellular transduction cascade.','Reception, transduction, and cellular response must remain three distinguishable stages.'],
'U4-L08':['Use membrane permeability as a principle, not a rigid rule that every hydrophobic molecule enters and every hydrophilic molecule never does.'],
'U4-L10':['GPCR is one important membrane-receptor family, not half of an exhaustive two-family receptor taxonomy.','GPCR and heterotrimeric G protein are separate structures with separate jobs.'],
'U4-L11':['GDP/GTP binding is a molecular switch in this mechanism; do not teach GTP primarily as an ATP-like energy source.'],
'U4-L13':['The violet tracing light is explicitly non-molecular and only marks information flow; the ligand stays outside the intracellular relay.'],
'U4-L14':['Phosphorylation can activate or inhibit a target depending on the protein; dephosphorylation also has target-dependent effects.','Protein kinase adds phosphate; protein phosphatase removes phosphate. Do not equate those chemical actions with universal on/off outcomes.'],
'U4-L16':['A second messenger is intracellular and distinct from the extracellular ligand/first signal; cAMP is one example.','Amplification means one upstream event produces many downstream activated molecules/events, not that each molecule becomes physically “stronger.”'],
'U4-L18':['A receptor mutation and a downstream-component mutation must have different breakpoint locations in the visual model.'],
'U4-L20':['Homeostasis is dynamic regulation within useful ranges, not a perfectly constant internal state.','Set point/reference language must allow physiological variability rather than encoding 98.6°F as a universal exact set point.'],
'U4-L21':['Sensor, integration/control, and effector roles can exist at molecular/cellular levels; do not require nervous-system anatomy.'],
'U4-L22':['Negative feedback means the response opposes the initial deviation; “negative” does not mean harmful.'],
'U4-L24':['Positive feedback reinforces the initiating change; “positive” does not mean beneficial.','Positive-feedback loops usually stop when an external endpoint or changed condition terminates the reinforcing cycle.'],
'U4-L25':['Dysregulated homeostasis can contribute to disease, but disease must not be defined solely as failure of homeostasis.'],
'U4-L26':['Chromosomes exist throughout the cell cycle; condensation changes packaging, not whether the DNA “becomes” a chromosome.'],
'U4-L27':['Sister chromatids are replicated copies of one chromosome; homologous chromosomes are corresponding maternal/paternal-type chromosome partners and are not sister chromatids.','The centromere is a chromosome region; the kinetochore is a protein complex assembled at the centromere.'],
'U4-L28':['Many prokaryotes have a main circular chromosome, but exceptions exist.','Gametes are products of meiosis or meiotic processes; do not say mature gametes divide by meiosis.'],
'U4-L29':['Interphase is commonly long but not universally 90% of every cell cycle.'],
'U4-L31':['DNA content and chromatid number double during S phase; centromere-counted chromosome number does not double.'],
'U4-L33':['G0 can be reversible for some cells and long-term for others; avoid “forever” as a universal rule.'],
'U4-L34':['Mitosis segregates replicated chromosomes; it does not universally mean production of diploid daughter cells.','Cytokinesis is separate from nuclear chromosome segregation.'],
'U4-L35':['Centrosomes are a useful animal-cell spindle-organizing example; do not imply higher-plant cells require the same centrosome/centriole arrangement.'],
'U4-L36':['Prometaphase is valid teacher enrichment; current AP framework can treat the broader mitotic sequence without requiring separate prometaphase recall.'],
'U4-L37':['The metaphase plate is an imaginary equatorial plane, not a physical plate inside the cell.'],
'U4-L38':['After sister chromatids separate, each former chromatid is an individual daughter chromosome.','Chromosome movement involves kinetochore-microtubule dynamics and spindle forces; do not reduce all movement to microtubule shortening alone.'],
'U4-L40':['Cytokinesis divides cytoplasm; cleavage furrow/contractile ring are animal-cell mechanisms and should not be generalized to plants.'],
'U4-L43':['The G1 checkpoint is a major decision point, but do not rank it as universally the single “most important” checkpoint.'],
'U4-L44':['Persistent DNA damage can lead to repair, arrest, senescence, apoptosis, or other outcomes depending on context; apoptosis is not automatic.'],
'U4-L45':['The spindle checkpoint blocks anaphase until adequate attachment/alignment; microtubule-disrupting drugs often prevent proper progression into anaphase rather than simply “damaging anaphase.”'],
'U4-L46':['Apoptosis is regulated programmed cell death and must remain distinct from accidental necrotic cell death.'],
'U4-L47':['Teach the general cyclin–CDK interaction; specific named cyclin/CDK pairs are outside current AP required memorization.'],
'U4-L48':['Growth factors are extracellular signaling molecules and are not universally hormones.','Density-dependent inhibition and anchorage dependence are useful teacher enrichment, not universal definitions of normal versus cancer cells.'],
'U4-L49':['Cancer does not have a universal mutation-count threshold and is not defined only by rapid division.'],
'U4-L50':['A benign tumor is nonmalignant, not “cancerous later.”','Malignancy is defined by invasive cancer behavior, with metastasis as distant spread; loss of anchorage dependence alone is not the definition.','Replicative immortality is a common acquired property of many transformed populations, not a literal property of every cancer cell.'],
'U4-L51':['UV radiation causes DNA damage and increases skin-cancer risk; use specific UV mechanism rather than vague sunlight language.','Nicotine is primarily the addictive component of tobacco; tobacco smoke contains carcinogens that drive DNA damage.','Do not encode hydration or generic “avoid fatty foods” claims as direct cancer-prevention mechanisms.']
}

recall_prompts={
'U4-L02':('Which animal junction and which plant junction directly connect neighboring cells?','Gap junctions in animals and plasmodesmata in plants.'),
'U4-L05':('What distinguishes endocrine signaling from the local signaling route you just left?','Hormones are released into circulation and can reach distant target cells; only receptor-bearing targets respond.'),
'U4-L07':('What event is reception?','A target cell detects a signal when a compatible ligand binds its receptor and changes the receptor’s state.'),
'U4-L11':('What nucleotide-state change activates the heterotrimeric G-protein switch, and what resets it?','GDP is released and GTP binds to activate the switch; GTP hydrolysis returns it toward the GDP-bound inactive state.'),
'U4-L12':('What directly changes when ligand binds a ligand-gated ion channel?','The channel’s gate/open probability changes, altering ion flux across the membrane.'),
'U4-L14':('What is the chemical difference between a kinase and a phosphatase?','A protein kinase transfers a phosphate group to a target; a protein phosphatase removes a phosphate group.'),
'U4-L16':('How is cAMP different from the ligand at the membrane?','cAMP is an intracellular second messenger generated inside the cell; the ligand is the extracellular signal that initiated reception.'),
'U4-L18':('How can you tell a receptor mutation from a downstream-component mutation in a pathway diagram?','A receptor mutation disrupts detection/activation at reception, while a downstream mutation leaves reception intact but changes relay or response after the breakpoint.'),
'U4-L22':('What makes a feedback loop negative?','Its response opposes the initial deviation and tends to reduce the stimulus that triggered the response.'),
'U4-L24':('What makes a feedback loop positive?','Its response reinforces the initiating change, increasing the process until an endpoint or changed condition stops the loop.'),
'U4-L27':('Where is the kinetochore relative to the centromere on a replicated chromosome?','The kinetochore is a protein complex assembled at the centromere region of each chromatid, where spindle microtubules attach.'),
'U4-L31':('After S phase, what doubles and what does not double?','DNA content and chromatid number double; chromosome number counted by centromeres remains the same until sister chromatids separate.'),
'U4-L33':('What is G0?','A nondividing state outside the active division cycle; some cells can reenter, while others remain nondividing for long periods.'),
'U4-L37':('What is the metaphase plate?','An imaginary equatorial plane where chromosomes align during metaphase.'),
'U4-L38':('What happens to chromosome counting when sister chromatids separate in anaphase?','Each former chromatid becomes a daughter chromosome, so chromosome count transiently doubles within the still-undivided cell.'),
'U4-L43':('What information can influence the G1 checkpoint decision?','Growth conditions, signaling cues, and DNA integrity can influence progression toward S phase versus pause or G0.'),
'U4-L47':('What is the functional relationship among cyclin, CDK, and the cyclin–CDK complex?','Cyclin binding helps regulate/activate a cyclin-dependent kinase; the active complex phosphorylates target proteins that control cell-cycle events.'),
'U4-L50':('What distinguishes benign tumor, malignant tumor, and metastasis?','A benign tumor is localized and noninvasive; a malignant tumor contains invasive cancer cells; metastasis is spread to distant sites where secondary tumors may form.')
}

# Route-specific causal handoffs. The final scene of each journey resolves the journey instead of moving to a new locus.
transitions={
'U4-L01':'The scale map identifies the contact route as the first mechanism that still needs a structural explanation, so Mira follows the direct-contact lane into the Contact Junction Gallery.',
'U4-L02':'Once direct-contact channels and surface recognition are separated, the route card shows a missing nearby-but-not-touching case; the learner exits into the Local Signal Courtyard.',
'U4-L03':'The local radius solves ordinary paracrine delivery but leaves one specialized narrow-gap route flashing; the neuron terminal sign pulls the learner to the Synaptic Dock.',
'U4-L04':'After the neurotransmitter crosses only a microscopic cleft, Mira contrasts that short route with a messenger that must cross the body, opening the circulation doors of the Endocrine Transit Hub.',
'U4-L05':'The animal circulation route is repaired, but the route card still has an empty plant long-distance field; a vascular plant display leads into the Plant Hormone Route.',
'U4-L06':'The final route card now distinguishes every communication scale in Journey 1; Mira closes the exchange only after sender, route, distance, and target can be reconstructed without the labels.',
'U4-L07':'The receptor gate activates correctly, but the monitor now asks where receptors can physically reside; the membrane divider opens into the Receptor Location Split.',
'U4-L08':'The location comparison leaves three intracellular examples waiting beyond the membrane; the receptor-state monitor moves through the right-hand door into the Intracellular Signal Suite.',
'U4-L09':'Intracellular routes are resolved, but the gateway still needs a membrane receptor that controls a cytoplasmic switch; the seven-pass GPCR model illuminates the next door.',
'U4-L10':'Ligand changes the GPCR, yet the cytoplasmic interface has not switched state; the learner follows that interface directly to the G-Protein Switchboard.',
'U4-L11':'The G-protein switch resets successfully, and the monitor flags a second membrane-receptor mechanism whose receptor is itself an ion channel; the learner moves to the Ligand-Gated Channel Gate.',
'U4-L12':'The reception gateway now distinguishes location, GPCR/G-protein switching, and ligand-gated channels; the journey ends with the receptor-state monitor showing correctly ordered receptor activation and downstream effect.',
'U4-L13':'The relay map reaches its first reversible protein-control node, so the violet information trace climbs to the Kinase–Phosphatase Switchboard.',
'U4-L14':'One reversible phosphorylation switch works, but the tower requires the same chemistry repeated through multiple relay layers; the next stair lights as the Phosphorylation Cascade Staircase.',
'U4-L15':'The cascade now relays through proteins, but a chamber above is designed to turn one input into many intracellular signals; the trace continues to the Second-Messenger Amplifier.',
'U4-L16':'Amplification produces many internal relay events that must now do something to the cell; the output conduits branch into Cellular Response Dispatch.',
'U4-L17':'The response branches work under normal conditions, so Mira deliberately breaks the route at different molecular levels and carries the same pathway model into the Mutation Breakpoint Lab.',
'U4-L18':'Genetic breakpoints are now distinct, but the lab still needs reversible non-genetic perturbation; the same pathway slides to the Agonist–Antagonist Console.',
'U4-L19':'The relay tower closes after the learner can predict normal information flow, amplification, response, mutation breakpoints, and chemical activation/inhibition without confusing any of them with the extracellular ligand physically moving through the pathway.',
'U4-L20':'The regulated-variable gauge has a reference range but no mechanism for sensing or acting on deviations; its wiring leads into the Sensor–Integrator–Effector Loop.',
'U4-L21':'With loop anatomy established, Mira deliberately pushes the gauge away from range and routes it into the Negative-Feedback Thermostat to test response direction.',
'U4-L22':'The thermostat proves the logic of opposing a deviation; the same negative-feedback geometry is then transferred to a biochemical variable at the Blood-Glucose Regulator.',
'U4-L23':'Blood-glucose control restores a range by opposing disturbances, but a separate alarm shows a loop whose response reinforces the change; the learner enters the Positive-Feedback Amplifier.',
'U4-L24':'The reinforcing examples terminate only when an endpoint changes the system; Mira then disables regulation entirely to reveal the consequences at the Dysregulation Alarm.',
'U4-L25':'The regulation center closes with the gauge, sensor, controller, effector, negative/positive directions, and dysregulation all distinguishable as parts of one control-system model.',
'U4-L26':'The packing hierarchy ends at chromosome-scale material, so Mira removes one replicated chromosome from the archive and places it on the Chromosome Anatomy Workbench.',
'U4-L27':'Once sister chromatids, centromere, and kinetochore are mapped on one chromosome, the unresolved question becomes how this chromosome relates to homologs and whole chromosome sets; the model moves into the Chromosome Sets Gallery.',
'U4-L28':'The chromosome-set gallery establishes ploidy and cell type, allowing the same tracked set to be placed on the circular Cell-Cycle Clock.',
'U4-L29':'The clock identifies G1 as the first detailed interphase stop; the tracked post-division cell follows the G1 arc into the G1 Growth Gate.',
'U4-L30':'G1 growth ends at the boundary where DNA synthesis begins, so the tracked chromosomes enter the S-Phase Replication Room.',
'U4-L31':'Replication produces sister chromatids without changing centromere-counted chromosome number; the replicated set exits directly into the G2 Preparation Bay.',
'U4-L32':'The cell is prepared for mitosis, but the cycle diagram still contains a side branch for nondividing states; Mira pauses before M phase and opens the G0 Side Chamber.',
'U4-L33':'The preparation archive closes after the learner can rebuild chromosome structure, ploidy, G1/S/G2, replication counting, and G0. The replicated chromosome set is then ready to enter the separate Mitosis Transit Hall.',
'U4-L34':'Mission Control establishes the route from one replicated genome to equivalent daughter nuclei; the tracked chromosomes move into the first active stage at Prophase Spindle Setup.',
'U4-L35':'The spindle forms but cannot yet reach kinetochores through the nuclear boundary, creating the mechanical need for the Prometaphase Kinetochore Access station.',
'U4-L36':'Once microtubules attach to kinetochores, the chromosomes remain scattered, so opposing spindle forces carry them toward the Metaphase Plate Station.',
'U4-L37':'Alignment is complete and the attachments are adequate; the next unresolved event is sister-chromatid separation, so the transit gate opens onto the Anaphase Separation Track.',
'U4-L38':'Daughter chromosomes reach opposite poles, setting the conditions for nuclear reassembly in the Telophase Reassembly Room.',
'U4-L39':'Two nuclei reform inside one shared cytoplasm, so the hall must now divide the cell itself; the animal-cell route opens first at the Animal Cytokinesis Ring.',
'U4-L40':'The animal mechanism uses an inward cleavage furrow, prompting a direct structural comparison with the rigid-walled plant route at the Plant Cell-Plate Works.',
'U4-L41':'The transit hall closes with equivalent chromosome sets in daughter nuclei and two distinct cytokinesis mechanisms; the tracked chromosomes can now be handed to the security system that regulates whether future cycles are allowed to begin.',
'U4-L42':'The command map identifies three major decision classes; Mira sends the model-cell file first to the G1 commitment decision before DNA replication.',
'U4-L43':'The G1 gate can authorize S phase or divert the cell, but the file later needs a second integrity check after replication; the learner advances to the G2 DNA-Integrity Gate.',
'U4-L44':'A repaired file can approach mitosis, yet chromosome attachment still has to be verified before anaphase; the file moves to the Spindle-Assembly Checkpoint.',
'U4-L45':'The spindle checkpoint can stop unsafe chromosome segregation; a separate route is still needed when a cell is too dangerous to retain, so the learner follows the safety exit to Apoptosis.',
'U4-L46':'Programmed removal is one possible safety outcome. Mira now returns to a healthy cycling cell and asks what molecular engine actually drives scheduled progression, opening the Cyclin–CDK Control Rack.',
'U4-L47':'The internal cyclin–CDK engine works, but the cell also needs information from its environment; the security file moves to Growth and Attachment Signals Bay.',
'U4-L48':'External constraints help normal cells decide whether to proliferate. Mira disables several restraints and carries the altered file to the Cancer Control-Failure Board.',
'U4-L49':'The control-failure board explains dysregulated proliferation and survival, but abnormal cells still differ in whether they remain localized, invade, or spread; the learner enters the Tumor Progression Corridor.',
'U4-L50':'Tumor terminology and metastasis are now resolved. The final question is how DNA-damaging exposures can increase the chance of acquiring harmful alterations, leading into the Carcinogen Risk Bay.',
'U4-L51':'The security journey closes only after the learner can reconstruct normal checkpoint permission, cyclin–CDK control, apoptosis, external proliferation constraints, cancer-control failure, tumor progression, metastasis, and evidence-based carcinogen risk without turning any single feature into the definition of cancer.'
}

# Confusable sets convert F2 classification into explicit scene-level discrimination constraints.
conf_by_kid=defaultdict(list)
for s in f2['confusable_sets']:
    for kid in s['knowledge_ids']:
        conf_by_kid[kid].append(s)

# Resolve review-flag IDs to correction text for designer-facing safeguards.
flag_by_id={f['review_flag_id']:f for f in src['review_flags']}

journeys=[]
for j in f2['journeys']:
    spec=journey_specs[j['journey_id']]
    route=[lid for b in j['bundles'] for lid in b['loci']]
    journeys.append({
      'journey_id':j['journey_id'],'working_title':j['working_title'],'content_focus':j['content_focus'],'setting_logic':j['setting_logic'],
      'unit_guide':unit_guide,**spec,'route':route,
      'route_rule':'The learner moves through the listed loci in order. The continuity object may update, but no locus changes its physical left/center/right geometry after F3.',
      'narrative_constraints':[
        'The learner always knows the entrance, the micro-anchor, and the left/center/right geometry before scientific action begins.',
        'One persistent guide and one journey continuity object provide narrative continuity; scientific terms themselves are not replaced by unrelated mascot characters.',
        'Scientific structures use conventional recognizable geometry before any mnemonic name-support cue is introduced.',
        'A scientific term is named only after the defining structure, action, or relationship is visible.',
        'One primary diagnostic interaction carries each scene; embedded records attach to that interaction rather than creating disconnected mini-stories.',
        'Exact-name support can be added later only according to the F2 name-support classification and never changes the scientific visual.',
        'All F1 misconception/scope corrections remain binding; final student prose states corrected science without audit/source-management language.',
        'Transitions are caused by the output, unresolved question, or physical state produced in the preceding scene.',
        'Listening or completing a story scene never by itself grants mastery; delayed exact retrieval belongs in Review.',
        'Final prose must be vivid and readable, but memorability comes from diagnostic biological action and stable place, not scientifically irrelevant bizarre decoration.'
      ],
      'status':'JOURNEY_BRIEF_LOCKED_F3_NO_POLISHED_STORY_PROSE'
    })

route_pos={}
for j in journeys:
    for i,lid in enumerate(j['route']): route_pos[lid]=(j,i)

briefs=[]
for l in f2['loci']:
    jid=l['journey_id']; j,i=route_pos[l['locus_id']]
    next_lid=j['route'][i+1] if i+1<len(j['route']) else None
    geo=l['scene_geometry']
    steps=core[l['locus_id']]
    # The cast are scientific parts or fixed comparison states, not a crowd of invented characters.
    stable_cast=[
      {'name':geo['left'],'position':'left','visual_identity':f"A conventional, clearly labeled scientific representation of {geo['left']} fixed on the learner’s left in the {l['visual_mode'].lower().replace('_',' ')} display.",'job_in_scene':'Establish the starting condition, one comparison, or the input that must be interpreted before the central mechanism acts.','type':'SCIENTIFIC_PART_OR_REFERENCE'},
      {'name':geo['center'],'position':'center','visual_identity':f"The largest working scientific model in the room, centered on {l['micro_anchor']}; moving parts are confined to this central action zone.",'job_in_scene':f"Perform the diagnostic mechanism that defines this locus: {steps[0]}",'type':'SCIENTIFIC_PROCESS_OR_STRUCTURE'},
      {'name':geo['right'],'position':'right','visual_identity':f"A conventional scientific representation of {geo['right']} fixed on the learner’s right; its visible state changes only after the center mechanism produces an outcome.",'job_in_scene':'Display the consequence, destination, competing alternative, or resolved state that proves what the central mechanism did.','type':'SCIENTIFIC_PART_OR_OUTPUT'}
    ]
    terms=[]
    by_spoken=defaultdict(list)
    for kid in l['knowledge_ids']:
        by_spoken[records[kid]['canonical_label']].append(kid)
    for n,kid in enumerate(l['knowledge_ids'],1):
        r=records[kid]; cl=class_by_id[kid]
        terms.append({
          'knowledge_id':kid,'canonical_term':r['canonical_label'],'canonical_science':r['canonical_verified_statement'],
          'exact_name_recall':bool(r.get('exact_name_recall',False)),'scope_class':r['scope_class'],
          'introduction_after_action_step':min(n, len(steps)),
          'insertion_rule':'Name the term only after its defining structure/function/relationship has become visible. Translate the canonical science into readable biological language without weakening, expanding, or contradicting the F1 statement.',
          'spoken_term_group':r['canonical_label'],'merge_duplicate_spoken_label':len(by_spoken[r['canonical_label']])>1,
          'name_support':cl.get('name_support','SEMANTIC_SCIENCE_CUE_SUFFICIENT'),
          'name_support_rule':'First attempt uses the scientific scene and semantic role. If later exact-name retrieval fails, add only the F2-approved optional semantic/sound cue; the cue never replaces the real term.',
          'spelling_policy':cl.get('spelling_policy','ADAPTIVE_SUPPORT_ONLY_NO_MANDATORY_SPELLING_GATE')
        })
    guards=list(special_guards.get(l['locus_id'],[]))
    seen=set()
    for kid in l['knowledge_ids']:
        for s in conf_by_kid.get(kid,[]):
            if s['set_id'] in seen: continue
            seen.add(s['set_id'])
            guards.append('Discrimination requirement: keep '+', '.join(s['terms'])+' physically and verbally distinct; do not let one label stand in for the whole set.')
    # Add resolved F1 correction text when a record carries a review flag.
    fids=[]
    for kid in l['knowledge_ids']:
        fid=records[kid].get('review_flag_id')
        if fid and fid not in fids: fids.append(fid)
    for fid in fids:
        if fid in flag_by_id:
            guards.append('Resolved science guard '+fid+': '+flag_by_id[fid]['resolution'])
    if not guards:
        guards.append('Preserve the conventional biological structure/process and do not add a mnemonic action that changes causal direction, location, or mechanism.')
    recall=recall_prompts.get(l['locus_id'])
    labels=[]
    for kid in l['knowledge_ids']:
        lab=records[kid]['canonical_label']
        if lab not in labels: labels.append(lab)
    briefs.append({
      'scene_brief_id':'F3-'+l['locus_id'],'locus_id':l['locus_id'],'journey_id':jid,'bundle_id':l['bundle_id'],
      'scene_title':l['title'],'exact_location':l['title'],'micro_anchor':l['micro_anchor'],
      'entrance_from':j['route'][i-1] if i>0 else 'JOURNEY_ENTRANCE',
      'orientation_sentence':f"Enter {l['title']} and stop at {l['micro_anchor']}. The {geo['left']} is fixed on the left, the {geo['center']} is directly ahead at the working center, and the {geo['right']} is fixed on the right. Those anchors stay in place while the scientific action unfolds.",
      'spatial_layout':{
        'left':{'anchor':geo['left'],'layout_job':'fixed input/reference/comparison zone'},
        'center':{'anchor':geo['center'],'layout_job':'primary science-bearing action zone'},
        'right':{'anchor':geo['right'],'layout_job':'fixed consequence/output/comparison zone'}
      },
      'unit_guide':unit_guide,'stable_cast':stable_cast,
      'continuity_object':journey_specs[jid]['continuity_object'],
      'scene_problem':f"At this location the learner must resolve the relationship represented by {l['micro_anchor']} without changing the fixed left/center/right geometry.",
      'science_bearing_action':{
        'before':f"All three zones are visible but unresolved. The left state ({geo['left']}) supplies the input or comparison, the center ({geo['center']}) is inactive, and the right ({geo['right']}) has not yet updated, so the learner cannot yet infer the mechanism.",
        'trigger':'Mira identifies the unresolved biological relationship and activates only the minimum structures needed to make that mechanism observable.',
        'during':steps,
        'after':f"Freeze the resolved state with {geo['left']} still on the left, {geo['center']} in the center, and {geo['right']} on the right. The learner should be able to reconstruct what changed, what caused the change, and which structure or signal carried the consequence."
      },
      'knowledge_ids':l['knowledge_ids'],'primary_knowledge_id':l['primary_knowledge_id'],'term_introductions':terms,
      'visual_spec':{
        'visual_mode':l['visual_mode'],'conventional_scientific_visual_required':True,
        'must_show':[geo['left'],geo['center'],geo['right'],*steps],
        'must_not_show':['source-management labels or textbook/assessment references','scientifically irrelevant decorative actors that compete with the mechanism','a mnemonic object replacing the real biological structure'],
        'composition_rule':'Preserve the F2 left/center/right geography and recognizable scientific geometry. Animate only the mechanism that changes; fixed anchors must remain redrawable from memory.'
      },
      'misconception_guards':guards,
      'adaptive_name_support':{
        'first_pass':'Use the conventional scientific structure/action plus the semantic role of the term. Do not display a sound cue merely because the term is unfamiliar.',
        'fallback':'After an exact-name retrieval failure, use only the record-level F2 name-support classification. Strong phonological support is reserved for terms flagged PHONOLOGICAL_SUPPORT_RECOMMENDED_IF_NEEDED.',
        'spelling':'No Unit 4 F2 record has a mandatory first-pass spelling gate; spelling support remains adaptive.'
      },
      'quick_recall':({'enabled':True,'candidate_prompt':recall[0],'answer':recall[1],'timing':'Optional first-exposure pause after the mechanism and exact term have already been encountered.','hint_rule':'Point to one spatial anchor or action; do not reveal the answer term before the learner attempts retrieval.'} if recall else {'enabled':False,'timing':'Defer retrieval to Review to preserve story flow.','hint_rule':'If later needed, return to one concrete anchor/action without displaying the target term.'}),
      'exit_memory':{
        'one_sentence_model':f"At {l['title']}, remember the fixed {geo['left']} → {geo['center']} → {geo['right']} relationship and the mechanism that changed the right-side state.",
        'terms_to_carry':labels,
        'redraw_test':f"From memory, place {geo['left']} on the left, {geo['center']} in the center, and {geo['right']} on the right, then describe the causal action in order."
      },
      'causal_transition':{'to_locus_id':next_lid,'transition_logic':transitions[l['locus_id']]},
      'story_prose_status':'PROHIBITED_UNTIL_F3_BRIEF_QA_PASS','brief_status':'LOCKED_F3_SCENE_BRIEF'
    })

scene_doc={
 'schema':'memory-palace-v2-unit4-f3-scene-briefs-1.0','generated_utc':GEN,'unit_id':'unit-4','canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','student_release':False,
 'design_standard':'NR-1.2: ORIENT -> FIX MICRO-ANCHOR -> IDENTIFY SCIENTIFIC PARTS -> ONE DIAGNOSTIC ACTION -> optional QUICK RECALL -> EXACT TERM/RELATIONSHIP -> CANONICAL TRANSLATION -> EXIT MEMORY -> CAUSAL MOVE',
 'counts':{'journeys':7,'scene_briefs':51,'palace_managed_records':162,'term_introductions':162,'optional_first_exposure_recalls':len(recall_prompts)},
 'scene_briefs':briefs
}
journey_doc={'schema':'memory-palace-v2-unit4-f3-journey-briefs-1.0','generated_utc':GEN,'unit_id':'unit-4','student_release':False,'unit_guide':unit_guide,'journey_count':7,'journeys':journeys}
dump(BRIEFS/'scene-briefs-f3.json',scene_doc); dump(BRIEFS/'journey-briefs-f3.json',journey_doc)

status={
 'unit_id':'unit-4','unit_number':4,'title':'Cell Communication and Cell Cycle','status':'SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','pipeline_status':'SCENE_BRIEF_ARCHITECTURE_COMPLETE',
 'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','student_release':False,'preview_release':False,
 'canonical_records':180,'review_flags_resolved':39,'teacher_ppt_slides':85,'ced_topics':6,'ced_atoms':38,'journey_count':0,'scene_count':0,'memory_objects':0,'application_challenges':0,
 'architecture_journeys':7,'architecture_bundles':17,'architecture_loci':51,'journey_briefs':7,'scene_briefs':51,'palace_managed_records':162,
 'scope_guard_records':3,'practice_only_records':15,'confusable_sets':33,'optional_first_exposure_recalls':len(recall_prompts),
 'next_required_output':'F4A polished narrative for Journey 1 only; no broad Unit 4 story generation before prose-level spatial, scientific, character, and continuity QA'
}
dump(U4/'status-f3.json',status); dump(U4/'status.json',status)
manifest={'schema':'memory-palace-v2-unit4-f3-release-1.0','generated_utc':GEN,'unit_id':'unit-4','release_status':'F3_SCENE_BRIEFS_LOCKED_NOT_STUDENT_RELEASED','journey_briefs':7,'scene_briefs':51,'palace_managed_records':162,'optional_first_exposure_recalls':len(recall_prompts),'polished_story_files':0,'student_runtime_memory_objects':0,'application_challenges':0,'student_release':False,'next_stage':'F4A Journey 1 polished narrative only'}
dump(U4/'f3-release-manifest.json',manifest)

course_path=ROOT/'content/ap-biology/course.json'; course=load(course_path)
for u in course['units']:
    if u['unit_id']=='unit-4':
        u.update({'status':status['status'],'journey_count':0,'scene_count':0,'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','source_status':'AUDITED_SCIENCE_LOCKED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3','canonical_records':180,'review_flags_resolved':39,'student_release':False,'ced_atoms':38,'teacher_ppt_slides':85,'architecture_journeys':7,'architecture_loci':51,'scene_briefs':51,'optional_first_exposure_recalls':len(recall_prompts)})
dump(course_path,course)

# Designer-facing scene-brief document.
lines=['# Unit 4 F3 Scene Briefs','','Status: `SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED`','',
 '- 7 journey continuity briefs','- 51 fixed loci / scene briefs','- 162 palace-managed canonical records represented exactly once','- 18 optional first-exposure Quick Recall candidates','- 0 polished Unit 4 narrative story files','- 15 practice-only records remain reserved for a later Challenge Lab','- 3 scope guards remain non-runtime','',
 '## F3 writing rule','',
 'Every later student scene must follow `ORIENT → FIX MICRO-ANCHOR → IDENTIFY PARTS → SCIENCE-BEARING ACTION → optional QUICK RECALL → EXACT TERM/RELATIONSHIP → CANONICAL TRANSLATION → EXIT MEMORY → CAUSAL MOVE`. The scientific structure and causal action remain primary. Mnemonic name support may be added later only after retrieval failure and may never replace the biology.','']
for j in journeys:
    lines += [f"## {j['journey_id']} · {j['working_title']}",'',j['premise'],'',f"**Mission.** {j['mission']}",'',f"**Continuity object.** {j['continuity_object']}",'',f"**Opening image.** {j['opening_image']}",'',f"**Ending payoff.** {j['ending_payoff']}",'']
    for lid in j['route']:
        b=next(x for x in briefs if x['locus_id']==lid)
        lines += [f"### {lid} · {b['scene_title']}",'',f"**Micro-anchor.** {b['micro_anchor']}",'',f"**Orientation.** {b['orientation_sentence']}",'',f"**Core scientific action.** {' '.join(b['science_bearing_action']['during'])}",'',f"**Exact terms/relationships.** {'; '.join(dict.fromkeys(t['canonical_term'] for t in b['term_introductions']))}",'',f"**Exit memory.** {b['exit_memory']['one_sentence_model']}",'',f"**Move.** {b['causal_transition']['transition_logic']}",'']
        if b['quick_recall']['enabled']:
            lines += [f"**Optional Quick Recall.** {b['quick_recall']['candidate_prompt']}",'']
(ROOT/'docs/UNIT4_F3_SCENE_BRIEFS.md').write_text('\n'.join(lines)+"\n",encoding='utf-8')

release_doc=f'''# Unit 4 F3 Release\n\n**PASS — SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED**\n\nF3 converts the fixed F2 learning architecture into designer-ready journey and scene briefs. It still creates no student-facing Unit 4 journeys.\n\n## Locked F3 accounting\n\n- 180 canonical records remain protected by F1.\n- 162 palace-managed records remain assigned exactly once.\n- 51/51 F2 loci now have one F3 scene brief.\n- 7/7 journeys now have premise, mission, continuity object, recurring scientific cast, opening image, ending payoff, route rule, and narrative constraints.\n- 18 optional first-exposure Quick Recall candidates are distributed across the 7 journeys.\n- 15 practice-only records remain outside the palace for a later Challenge Lab.\n- 3 scope guards remain non-runtime.\n- 0 polished Unit 4 story files exist.\n- 0 Unit 4 student runtime Memory Objects exist.\n- Student release remains `false`.\n\n## Quality boundary\n\nEvery scene brief now fixes exact physical geometry, scientific parts and jobs, before/during/after mechanism, canonical term introduction, name-support policy, misconception controls, an exit-memory reconstruction target, and a causal handoff. Final prose is still blocked.\n\n## Next gate\n\nF4A must write **Journey 1 only — Cellular Communications Exchange** from these six briefs. It must pass prose-level spatial clarity, character/part clarity, scientific fidelity, exact-term integration, narrative continuity, and memorability QA before Journey 2 is authored.\n'''
(ROOT/'docs/UNIT4_F3_RELEASE.md').write_text(release_doc,encoding='utf-8')

qa_doc=f'''# Unit 4 F3 QA\n\n## Release decision\n\n**PASS — scene briefs locked; Unit 4 remains intentionally unreleased.**\n\n- 51/51 F2 loci have exactly one F3 scene brief.\n- 162/162 palace-managed canonical records appear exactly once.\n- 162 term/relationship introductions preserve F1 canonical verified science word-for-word in the designer data.\n- 7/7 journey briefs have a stable route, premise, mission, continuity object, recurring scientific cast, opening image, ending payoff, and narrative constraints.\n- 18 optional first-exposure recalls are distributed across the seven journeys.\n- Every brief fixes entrance, left/center/right geography, micro-anchor, stable scientific parts, before/during/after action, conventional visual requirements, misconception guards, exit-memory target, and causal transition.\n- No polished Unit 4 story file exists.\n- Unit 4 journey/application runtime remains blocked.\n\n## Next gate\n\nF4A should author **U4-J1 only** and then run prose-level narrative QA before any additional Unit 4 journey is written.\n'''
(ROOT/'docs/UNIT4_F3_QA.md').write_text(qa_doc,encoding='utf-8')

# Update repository onboarding while preserving the Units 1–3 runtime version.
start=ROOT/'START_HERE.md'
if start.exists():
    txt=start.read_text(encoding='utf-8')
    txt=txt.replace('Unit 4 — F2 learning architecture locked, intentionally unreleased','Unit 4 — F3 journey/scene briefs locked, intentionally unreleased')
    txt=txt.replace('Lock AP Biology Unit 4 F2 learning architecture','Lock AP Biology Unit 4 F3 scene briefs')
    marker='Unit 3 remains complete and classroom/browser validated. **Unit 4 F2 is now complete as well.** All 180 canonical records have one learning destination, 51 permanent loci are locked across 7 journey blueprints, and Unit 4 still has no student runtime. The next Unit 4 step is **F3 science-bearing scene briefs**. Do not write polished Unit 4 narrative prose until the 51 briefs pass F3 spatial, scientific, causal, exact-name, and misconception-control QA.'
    repl='Unit 3 remains complete and classroom/browser validated. **Unit 4 F3 is now complete.** All 51 permanent loci have locked science-bearing scene briefs and all 7 journeys have continuity briefs, while Unit 4 still has no student runtime. The next Unit 4 step is **F4A, polished narrative for Journey 1 only**. Do not write Journeys 2–7 until Journey 1 passes prose-level spatial, scientific, character, continuity, and memorability QA.'
    txt=txt.replace(marker,repl)
    start.write_text(txt,encoding='utf-8')

# Lock after all F3 artifacts exist.
lock_files=[
 'content/ap-biology/unit-4/source/canonical-unit4-f1.json',
 'content/ap-biology/unit-4/architecture/learning-classification-f2.json',
 'content/ap-biology/unit-4/architecture/palace-architecture-f2.json',
 'content/ap-biology/unit-4/briefs/journey-briefs-f3.json',
 'content/ap-biology/unit-4/briefs/scene-briefs-f3.json',
 'content/ap-biology/unit-4/f3-release-manifest.json','content/ap-biology/unit-4/status-f3.json'
]
lock={'schema':'memory-palace-v2-unit4-f3-content-lock-1.0','generated_utc':GEN,'unit_id':'unit-4','lock_status':'LOCKED_F3','student_release':False,'parents':['LOCKED_F1','LOCKED_F2'],'files':{rel:{'sha256':sha(ROOT/rel),'bytes':(ROOT/rel).stat().st_size} for rel in lock_files},'rule':'F3 locks journey continuity and scene briefs only. F1 canonical science and F2 learning destinations/loci remain immutable; polished Unit 4 story prose remains prohibited until F4A.'}
dump(U4/'content-lock-f3.json',lock)
print(json.dumps(scene_doc['counts'],indent=2))
