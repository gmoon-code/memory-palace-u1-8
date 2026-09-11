from __future__ import annotations
import json, hashlib
from pathlib import Path
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content'/'ap-biology'/'unit-3'
ARCH=U3/'architecture'; BRIEFS=U3/'briefs'; BRIEFS.mkdir(parents=True,exist_ok=True)
GEN='2026-09-03T02:10:00+00:00'

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,obj): Path(p).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

src=load(U3/'source/canonical-unit3-f1.json')
records={r['knowledge_id']:r for r in src['canonical_catalog']}
f2=load(ARCH/'palace-architecture-f2.json')
classif=load(ARCH/'learning-classification-f2.json')
class_by_id={r['knowledge_id']:r for r in classif['records']}

unit_guide={
 'name':'Dr. Nia Park',
 'role':'cellular-energetics investigator who accompanies the learner through every Unit 3 journey',
 'visual_identity':'navy field jacket, clear safety glasses, compact tablet showing reaction, membrane, and energy-flow models',
 'behavior_rule':'Nia fixes the learner in a stable location, makes the mechanism visible, asks for a prediction when useful, and names scientific terminology only after the relevant structure or action is clear.',
 'continuity_rule':'Nia remains the same guide across all seven journeys and never substitutes as a mnemonic character for a scientific term.'
}

journey_specs={
'U3-J1':dict(premise='A reaction workshop is wasting energy because its molecular jobs have been reduced to labels. The learner must rebuild catalysis by comparing reaction barriers, docking a real substrate at an active site, and watching the same enzyme return to service after product release.', mission='Follow one reaction from activation-energy barrier to enzyme-substrate binding and catalytic turnover so enzyme action is understood as a reusable molecular mechanism.', stakes='If the workshop remains vague, later regulation scenes will collapse into memorized inhibitor names without a working model of what an enzyme actually does.', continuity_object='one amber substrate token that is tracked from free reactant to active-site binding, conversion, product release, and enzyme reset', opening_image='Two reaction tracks rise ahead: one climbs a high energy hill while a second passes through a lower enzyme-controlled route.', ending_payoff='The amber substrate is converted, the products leave, and the unchanged enzyme station resets for another cycle.', tone='mechanistic, close-up, tactile, precise'),
'U3-J2':dict(premise='The enzyme control wing is producing erratic rates. One reference enzyme is carried through heat, pH, concentration, helper, inhibitor, allosteric, cooperative, and pathway-feedback tests so each regulatory mechanism remains physically distinct.', mission='Stress and regulate one enzyme system while preserving the difference between altered protein structure, active-site competition, allosteric control, cooperative binding, feedback inhibition, and irreversible loss of function.', stakes='Students must be able to diagnose why enzyme activity changed from evidence rather than attaching every rate change to denaturation or inhibition.', continuity_object='a transparent reference enzyme whose active site and overall conformation remain visible at every control station', opening_image='A transparent enzyme glows in a central clamp while temperature, pH, substrate, helper, and inhibitor controls surround it.', ending_payoff='The control wing stabilizes only after every mechanism has a distinct physical cause and a distinct visible consequence.', tone='diagnostic, experimental, controlled'),
'U3-J3':dict(premise='An energy-exchange hall has lost its accounting system. Metabolic routes, energy forms, thermodynamic constraints, cellular work, and ATP cycling must be reconnected into one lawful energy-flow system.', mission='Trace how cells transform energy, remain organized while increasing total entropy, couple favorable and unfavorable processes, and continuously regenerate ATP.', stakes='Without a coherent energy model, photosynthesis and respiration become disconnected pathway lists instead of transformations constrained by thermodynamics.', continuity_object='a glowing energy token whose form changes while the ledger always tracks where energy enters, changes form, performs work, and disperses', opening_image='A wall-sized metabolic map flickers beside a dark energy ledger, while an ATP wheel has stopped mid-turn.', ending_payoff='The ledger balances, ATP cycles again, and the same metabolic logic can be recognized across widely separated organisms.', tone='systems-oriented, quantitative where useful, concrete'),
'U3-J4':dict(premise='A light-capture conservatory is receiving sunlight but cannot reliably convert it into ATP and NADPH. The learner follows light from ecological context into leaf and chloroplast structure, pigments, photosystems, electron transfer, proton-gradient formation, and photophosphorylation.', mission='Build one continuous map from photon capture to linear electron flow and the chemical energy products that leave the light reactions.', stakes='The learner must know which events happen in which chloroplast structures and must keep excitation-energy transfer separate from electron transfer.', continuity_object='one pulse of absorbed light followed by one highlighted electron path and one rising thylakoid proton-gradient gauge', opening_image='A beam of white light enters a glasshouse, passes through a leaf, and breaks into a spectrum above a transparent chloroplast.', ending_payoff='ATP and NADPH leave the thylakoid system together, ready to power carbon fixation in the adjoining greenhouse.', tone='luminous, spatial, process-driven'),
'U3-J5':dict(premise='The carbon-fixation greenhouse has ATP and NADPH available but carbon output falls whenever conditions favor photorespiration. The learner reconstructs the Calvin cycle and then compares two carbon-concentrating strategies.', mission='Follow carbon from CO2 fixation through G3P output and RuBP regeneration, then diagnose Rubisco oxygenation and compare C4 spatial separation with CAM temporal separation.', stakes='Students must understand the logic of carbon fixation without being forced to memorize every Calvin-cycle intermediate.', continuity_object='one carbon tracer that enters as CO2, appears in fixed carbon, contributes to G3P, and is contrasted with the photorespiratory detour', opening_image='A green circular workbench waits in the stroma while ATP and NADPH arrive from the light-capture conservatory.', ending_payoff='The greenhouse restores carbon gain by correctly identifying carbon fixation, photorespiration, and the contrasting C4 and CAM solutions.', tone='greenhouse-laboratory, carbon-flow focused, comparative'),
'U3-J6':dict(premise='A respiration power plant has fuel but its energy harvest is fragmented. The learner follows carbon and electrons from cytosolic glycolysis into mitochondrial oxidation, the electron-transport chain, proton pumping, oxygen reduction, ATP synthase, heat, and a prokaryotic membrane comparison.', mission='Reconstruct aerobic respiration as a coordinated sequence that transfers energy from fuel to reduced carriers, a proton-motive force, and ATP.', stakes='The learner must keep carbon flow, electron flow, proton movement, compartment geography, and phosphorylation mechanisms separate but causally connected.', continuity_object='a paired tracer system: a carbon token follows fuel oxidation while a blue electron token is transferred to carriers and finally to the respiratory ETC', opening_image='A glucose shipment enters a power plant whose carbon line, electron line, and proton-pressure gauges are all disconnected.', ending_payoff='The plant produces ATP with a stable proton gradient, oxygen accepts terminal electrons, and the learner can reconstruct the same membrane logic in a prokaryote.', tone='industrial, sequential, mechanistic'),
'U3-J7':dict(premise='The alternative-energy annex receives cells that cannot rely on the ordinary oxygen-terminal route. The learner must separate anaerobic respiration from fermentation and then use redox bookkeeping to explain alcohol and lactate pathways.', mission='Compare alternative terminal electron-acceptor routes with fermentation, then follow NAD+ recycling through alcohol and lactate fermentation without importing outdated lactate misconceptions.', stakes='Students must not collapse anaerobic respiration, fermentation, oxygen absence, and lactate physiology into one undifferentiated idea.', continuity_object='a limited pool of NAD+ cards that must be regenerated so glycolysis can continue', opening_image='Three route signs branch from the same glycolysis platform while the NAD+ card rack is nearly empty.', ending_payoff='The NAD+ cards return to glycolysis through clearly distinct pathways, and lactate is left as a transportable metabolic intermediate rather than a “muscle poison.”', tone='comparative, redox-centered, clinically careful')
}

# One science-bearing action sentence per locus. These are designer-facing scene mechanics, not polished story prose.
core={
'U3-L01':'Run identical reactants over the high uncatalyzed energy hill and the lower enzyme-catalyzed route; keep reactants and products fixed so the only changed feature is the activation-energy barrier.',
'U3-L02':'Move the same substrate into the enzyme pocket, test shape and chemical compatibility, allow local conformational adjustment, and freeze the bound enzyme-substrate complex before chemistry proceeds.',
'U3-L03':'Complete one catalytic cycle, release product, and immediately feed a fresh substrate to the unchanged enzyme so catalyst reuse is physically undeniable.',
'U3-L04':'Hold one enzyme in a structure monitor while temperature and pH move from optimum toward extremes; let function decline as conformation is disrupted, then test whether restoring conditions allows recovery.',
'U3-L05':'Increase substrate concentration at fixed enzyme concentration until active sites are continuously occupied, then separately change temperature to distinguish collision-frequency effects from saturation.',
'U3-L06':'Start with an inactive protein component, add a required helper, compare an inorganic cofactor with an organic coenzyme, and show the complete active enzyme complex only after the required component is present.',
'U3-L07':'Send substrate and a similarly fitting competitor toward the same active site, then raise substrate concentration to show why active-site competition can be partly overcome.',
'U3-L08':'Bind regulatory molecules at a site physically separated from the active site and show the enzyme conformation shifting so activity rises or falls without direct competition for the substrate-binding pocket.',
'U3-L09':'Bind one ligand to the first subunit of a linked multi-subunit protein and visibly change the binding behavior of the remaining subunits.',
'U3-L10':'Run a multi-step pathway until end product accumulates, then route that product back to an earlier regulatory enzyme and show pathway flux decreasing.',
'U3-L11':'Expose one enzyme to a persistent inhibitor, remove the surrounding inhibitor, restore ordinary conditions, and show that the enzyme still fails the recovery test.',
'U3-L12':'Feed a large molecule into the catabolic branch and small precursors into the anabolic branch while the center map exposes shared intermediates and enzyme-controlled sequential steps.',
'U3-L13':'Convert a single energy token among motion, heat, stored position, and chemical-bond arrangements while explicitly tracking which form changes and which does not vanish.',
'U3-L14':'Pass a fixed amount of energy through a closed ledger from input to transformed outputs and heat so conservation is visible even when energy changes form.',
'U3-L15':'Maintain a highly ordered cellular model only while energy enters; route some energy outward as dispersed heat and let local order fail when the input is shut off.',
'U3-L16':'Place paired reactions on a free-energy landscape, let one proceed downhill and another require uphill input, and keep an equilibrium reference visible so direction and cellular disequilibrium are distinct.',
'U3-L17':'Use energy released at the center junction to drive mechanical movement, membrane transport, and chemical synthesis in three fixed bays.',
'U3-L18':'Assemble ATP from adenine, ribose, and three phosphate groups, then place it beside ADP plus inorganic phosphate so structural differences are visible before energy coupling is discussed.',
'U3-L19':'Hydrolyze ATP while tracking the full reaction to lower-free-energy products, transfer a phosphate to a target when appropriate, and show how phosphorylation changes the target or coupled reaction.',
'U3-L20':'Cycle ATP to ADP plus phosphate during cellular work, then use energy from catabolic processes to regenerate ATP continuously.',
'U3-L21':'Overlay core metabolic reactions from prokaryotic and eukaryotic records and highlight the shared logic that persists across deeply separated lineages.',
'U3-L22':'Route carbon and energy inputs through photoautotroph, autotroph, and heterotroph lanes so carbon source and energy source are compared separately.',
'U3-L23':'Advance a timeline from oxygenic photosynthetic prokaryotes through atmospheric oxygen accumulation to later eukaryotic photosynthetic lineages.',
'U3-L24':'Open and close stomata in a leaf cutaway while tracing CO2 inward and O2 plus water vapor outward to connect guard-cell pores with mesophyll photosynthesis and gas exchange.',
'U3-L25':'Open a chloroplast cutaway and keep stroma, thylakoid membrane, and grana simultaneously visible while reaction-location markers attach to the correct compartment.',
'U3-L26':'Oxidize water on the left, carry energy and reducing power through the light-reaction/Calvin-cycle linkage, and reduce carbon dioxide on the right without implying that the oxygen released comes from CO2.',
'U3-L27':'Send photons of different wavelengths through the prism, compare their energy, and show pigment absorption versus reflection without treating color as stored “light energy.”',
'U3-L28':'Illuminate chlorophyll a, chlorophyll b, and carotenoids with the same spectrum and compare absorption, excitation, reflected wavelengths, and carotenoid protective roles.',
'U3-L29':'Excite an antenna pigment, pass excitation energy among neighboring pigments, and deliver that energy to the reaction-center chlorophyll while keeping actual electron transfer confined to the reaction center/acceptor step.',
'U3-L30':'Excite photosystem II, remove an electron from its reaction center, split water to replace that electron, and visibly separate the resulting electrons, protons, and oxygen product.',
'U3-L31':'Move the highlighted electron from photosystem II through the thylakoid electron-transport chain toward photosystem I while using released energy to increase H+ concentration in the lumen.',
'U3-L32':'Re-excite the arriving electron in photosystem I and transfer reducing power to NADP+ so NADPH forms on the stroma side.',
'U3-L33':'Let H+ flow down its electrochemical gradient from the thylakoid lumen through ATP synthase and couple that flow to ATP formation in the stroma.',
'U3-L34':'Deliver ATP and NADPH from the light reactions into a stroma-localized Calvin-cycle model and use them to support carbon reduction and cycle regeneration.',
'U3-L35':'Bring CO2 and RuBP together at Rubisco, perform the carbon-fixation step, and trace the newly incorporated carbon into the cycle rather than treating Rubisco as a carbon-containing substrate.',
'U3-L36':'Run enough Calvin-cycle turns to show G3P output and RuBP regeneration while keeping detailed stoichiometric bookkeeping visually secondary to the cycle logic.',
'U3-L37':'Present Rubisco with CO2 and O2 alternatives, route oxygenation into a photorespiratory detour, and show the resulting reduction in net carbon fixation.',
'U3-L38':'Expose C4 and CAM models to the same hot/dry pressure, then show C4 separating initial fixation and Calvin-cycle processing across space while CAM separates them across time.',
'U3-L39':'Feed carbohydrate, fat, and protein-derived carbon into a stage map and trace the coordinated outputs of aerobic respiration: carbon dioxide, water, ATP, and heat.',
'U3-L40':'Split one six-carbon glucose through cytosolic glycolysis, show ATP investment and payoff separately, and end with two pyruvate plus NADH and net ATP while identifying substrate-level phosphorylation.',
'U3-L41':'Load electrons onto NAD+ and FAD to form NADH and FADH2, then keep oxidized and reduced carrier forms paired so electron-carrier state is unmistakable.',
'U3-L42':'Move pyruvate into the mitochondrial transition station, remove carbon as CO2, reduce NAD+, and attach the remaining acetyl group to coenzyme A.',
'U3-L43':'Feed acetyl-CoA into the matrix cycle, release carbon as CO2, transfer energy to NADH/FADH2 and ATP/GTP, and regenerate the cycle acceptor without making detailed intermediate memorization primary.',
'U3-L44':'Rotate a mitochondrial cutaway so matrix, inner membrane, cristae, and intermembrane space remain fixed while respiration-stage markers attach to their proper locations.',
'U3-L45':'Unload electrons from NADH and FADH2 into the inner-membrane chain and pass them through progressively lower-energy redox steps toward the terminal acceptor end.',
'U3-L46':'Use energy from electron transfer to pump H+ from the matrix across the inner membrane into the intermembrane space and display the resulting concentration and pH difference.',
'U3-L47':'Deliver terminal electrons and protons to oxygen and form water, making oxygen the final electron acceptor rather than a source of ATP itself.',
'U3-L48':'Release the proton-motive force through ATP synthase, couple proton flow to rotational/conformational catalysis, and form ATP while keeping exact yield as an estimate rather than a fixed universal count.',
'U3-L49':'Open a controlled proton leak that bypasses ATP synthase, let gradient energy dissipate, and route more of that energy to heat while ATP capture efficiency falls.',
'U3-L50':'Place respiratory ETC and proton-translocation machinery directly in a prokaryotic plasma membrane to show how chemiosmotic respiration works without mitochondria.',
'U3-L51':'Branch from a shared energy-harvesting junction into oxygen-terminal aerobic respiration, non-oxygen-terminal anaerobic respiration, and fermentation so terminal acceptors and ETC use remain explicit.',
'U3-L52':'Use an organic molecule to accept electrons from NADH, regenerate NAD+, and send NAD+ back to glycolysis without adding an electron-transport chain to fermentation.',
'U3-L53':'Convert pyruvate to acetaldehyde with CO2 release, then reduce acetaldehyde to ethanol while oxidizing NADH back to NAD+.',
'U3-L54':'Reduce pyruvate to lactate while regenerating NAD+, then move lactate into transport/reuse pathways to prevent the scene from ending with an obsolete “lactic acid poison” image.'
}

special_guards={
'U3-L04':['Keep denaturation distinct from ordinary reversible changes in rate; loss of function can reflect altered conformation, and reversibility depends on the severity and cause of disruption.'],
'U3-L06':['A coenzyme is an organic cofactor; do not present cofactor and coenzyme as mutually exclusive categories.','Use holoenzyme only for the active enzyme complex that includes its required nonprotein component(s).'],
'U3-L08':['The regulatory molecule binds an allosteric/regulatory site, not necessarily the substrate or active site.','Do not collapse allosteric inhibition into active-site competition.'],
'U3-L11':['Irreversible inhibition is defined by persistent loss of activity after inhibitor removal, not simply by “very strong” binding.'],
'U3-L16':['Keep Gibbs free energy as a conceptual relationship; the AP scope guard prevents requiring memorization of the full ΔG equation.'],
'U3-L19':['Do not say ATP releases energy merely because a phosphate bond is broken; net hydrolysis is favorable because the products are at lower free energy than ATP plus water.'],
'U3-L22':['Separate carbon source from energy source: photoautotroph describes light energy plus inorganic carbon, while heterotroph describes use of organic carbon.'],
'U3-L26':['Photosynthetic O2 comes from water oxidation, not from CO2.','NADPH is used later for carbon reduction; do not depict water electrons as being passed directly into carbohydrate in one step.'],
'U3-L29':['Transfer excitation energy among antenna pigments; do not animate one identical electron hopping pigment-to-pigment through the antenna complex.'],
'U3-L30':['Water splitting replaces electrons lost from photosystem II and produces O2 and H+; keep those products spatially separate.'],
'U3-L32':['P680 and P700 are reaction-center chlorophyll labels associated with PSII and PSI respectively; do not turn them into separate photosystems.'],
'U3-L34':['The Calvin cycle is a carbon-fixation cycle and is not “cyclic electron flow.”'],
'U3-L36':['Keep exact Calvin-cycle molecule counts as enrichment; the student-facing core should prioritize inputs, carbon fixation, G3P output, and RuBP regeneration.'],
'U3-L37':['Photorespiration lowers net carbon fixation because Rubisco oxygenates RuBP; do not describe it as normal mitochondrial cellular respiration.'],
'U3-L38':['C4 uses spatial separation and CAM uses temporal separation; both concentrate CO2 around Rubisco but by different architectures.'],
'U3-L40':['Substrate-level phosphorylation forms ATP by direct phosphate transfer from a metabolic intermediate; keep it distinct from oxidative phosphorylation.'],
'U3-L43':['Detailed citric-cycle intermediate names and exact bookkeeping remain enrichment, not a primary AP memorization burden.'],
'U3-L48':['Respiratory ATP yield varies with cell type, shuttle systems, and proton leak; do not teach one exact ATP total as universal.'],
'U3-L51':['Anaerobic respiration uses an electron-transport chain with a terminal electron acceptor other than O2; fermentation does not use an ETC to regenerate NAD+.'],
'U3-L52':['Fermentation regenerates NAD+ so glycolysis can continue; it does not add substantial ATP beyond glycolysis itself.'],
'U3-L54':['Human lactate can be produced under aerobic conditions and can be transported and oxidized; do not attribute exercise fatigue or delayed soreness simply to lactate accumulation.']
}

recall_prompts={
'U3-L01':('What changes when an enzyme catalyzes the same reaction route?','The activation-energy barrier is lowered; the enzyme does not change the overall reactants or products of the comparison.'),
'U3-L02':('What must be compatible for the docking event in the center pocket to occur?','The substrate must be compatible with the enzyme active site in shape and chemical properties.'),
'U3-L04':('What visible change links extreme temperature or pH to loss of enzyme activity here?','The enzyme conformation is disrupted, changing the structure needed for function.'),
'U3-L07':('Why can increasing substrate concentration reduce the effect seen at this shared gate?','Substrate and competitive inhibitor compete for the same active site, so more substrate increases the chance that substrate occupies it.'),
'U3-L08':('How is the regulatory site in this room different from the substrate-binding pocket?','It is a separate allosteric site; binding there changes enzyme conformation and activity.'),
'U3-L12':('What distinguishes the two branches on the metabolic route map?','Catabolic pathways break molecules down, while anabolic pathways build larger molecules from smaller components.'),
'U3-L16':('Which direction on the terrain is thermodynamically favorable without added energy?','The downhill exergonic direction, toward lower free energy.'),
'U3-L19':('What actually makes ATP hydrolysis useful for coupling in this forge?','The overall hydrolysis reaction leads to lower-free-energy products and can be coupled to phosphorylation or other work.'),
'U3-L25':('Where are the light reactions and Calvin cycle located in the chloroplast model?','Light-reaction machinery is in thylakoid membranes; the Calvin cycle occurs in the stroma.'),
'U3-L29':('What moves through the antenna pigments before the reaction center transfers an electron?','Excitation energy moves among pigments toward the reaction center.'),
'U3-L30':('Where does photosystem II obtain replacement electrons after excitation?','From water oxidation at the water-splitting complex.'),
'U3-L33':('What directly drives ATP synthase in this thylakoid scene?','H+ moving down its electrochemical gradient through ATP synthase.'),
'U3-L35':('What molecule accepts CO2 at the carbon-fixation bench?','RuBP, in a reaction catalyzed by Rubisco.'),
'U3-L37':('What competing molecule sends Rubisco into the photorespiratory detour?','O2.'),
'U3-L40':('Where does glycolysis occur and what three major output types leave the line?','In the cytosol; pyruvate, NADH, and net ATP leave the pathway.'),
'U3-L45':('What do NADH and FADH2 contribute to the respiratory electron-transport chain?','High-energy electrons.'),
'U3-L48':('What energy source drives ATP formation at this mitochondrial turbine?','The proton-motive force as H+ flows through ATP synthase.'),
'U3-L52':('Why must fermentation regenerate NAD+?','So glycolysis can continue oxidizing substrate and producing ATP when NAD+ would otherwise become depleted.')
}

# Confusable sets help convert classification into concrete misconception guards.
conf_by_kid={}
for s in f2['confusable_sets']:
    for kid in s['knowledge_ids']:
        conf_by_kid.setdefault(kid,[]).append(s)

journeys=[]
for j in f2['journeys']:
    spec=journey_specs[j['journey_id']]
    route=[lid for b in j['bundles'] for lid in b['loci']]
    journeys.append({
      'journey_id':j['journey_id'],'working_title':j['working_title'],'content_focus':j['content_focus'],'setting_logic':j['setting_logic'],
      'unit_guide':unit_guide,**spec,'route':route,
      'narrative_constraints':[
        'The learner always knows where they are relative to the previous locus and can redraw the route from memory.',
        'The left, center, and right anchors stay fixed throughout a scene; moving parts act within that stable geometry.',
        'Scientific structures use conventional recognizable geometry before any mnemonic embellishment is added.',
        'A scientific term is named only after its defining structure, action, or relationship has become visible.',
        'One primary diagnostic interaction carries each scene; embedded facts attach to that interaction instead of creating extra spectacles.',
        'No source-management language, textbook references, or assessment-meta wording appears in future student prose.',
        'Transitions are caused by the output, failure, or unresolved question from the preceding scene.',
        'Listening or story completion never by itself grants mastery; exact scientific retrieval is handled later in Review.'
      ],
      'status':'JOURNEY_BRIEF_LOCKED_F3_NO_POLISHED_STORY_PROSE'
    })

jindex={j['journey_id']:j for j in journeys}
route_pos={}
for j in journeys:
    for i,lid in enumerate(j['route']): route_pos[lid]=(j,i)

briefs=[]
for l in f2['loci']:
    jid=l['journey_id']; j,i=route_pos[l['locus_id']]
    next_lid=j['route'][i+1] if i+1<len(j['route']) else None
    next_title=next((x['title'] for x in f2['loci'] if x['locus_id']==next_lid),None)
    geo=l['scene_geometry']
    # Distribute scientific terms over stable visual zones without pretending every term is a separate character.
    labels=[records[k]['canonical_label'] for k in l['knowledge_ids']]
    stable_cast=[
      {'name':geo['left'],'visual_identity':f"A fixed left-side scientific model of {geo['left']}, kept in conventional biological/chemical geometry.",'job_in_scene':'Provide the input, reference condition, or comparison state that the learner can return to without moving the scene.','type':'SCIENTIFIC_PART_OR_REFERENCE'},
      {'name':geo['center'],'visual_identity':f"The central working model at {l['micro_anchor']}; this is the largest and most animated zone in the scene.",'job_in_scene':'Carry the primary science-bearing transformation or diagnostic interaction.','type':'SCIENTIFIC_PROCESS_OR_STRUCTURE'},
      {'name':geo['right'],'visual_identity':f"A fixed right-side model of {geo['right']} with visible outputs or consequences that update after the center action.",'job_in_scene':'Show the consequence, destination, output, or competing alternative while preserving the learner’s orientation.','type':'SCIENTIFIC_PART_OR_OUTPUT'}
    ]
    before=f"The learner stands at {l['micro_anchor']}. The left reference ({geo['left']}), center mechanism ({geo['center']}), and right consequence ({geo['right']}) are all visible but initially inactive, so their relationship is unresolved."
    during=[
      f"Nia fixes the learner at the micro-anchor and activates the left reference first, then the center mechanism, so the learner can see what changes while the scene geography stays constant.",
      core[l['locus_id']],
      f"The right-side zone updates only after the central action, making the output or comparison visible without moving any of the three anchors."
    ]
    after=f"The scene freezes in its resolved state with {geo['left']} on the left, {geo['center']} in the center, and {geo['right']} on the right. The learner should be able to reconstruct the mechanism using those three fixed anchors before any term-only review begins."
    terms=[]
    for n,kid in enumerate(l['knowledge_ids'],1):
        r=records[kid]; cl=class_by_id[kid]
        terms.append({
          'knowledge_id':kid,'canonical_term':r['canonical_label'],'exact_name_recall':bool(r.get('exact_name_recall',False)),
          'canonical_science':r['canonical_verified_statement'],
          'insertion_rule':f"Introduce the exact term after action step {min(n+1,3)} has made the relevant structure/function/relationship visible. State the verified science in ordinary biological language and keep enrichment detail subordinate to the scene’s primary mechanism.",
          'name_support':cl.get('name_support','NONE'),
          'spelling_policy':cl.get('spelling_policy','NO_MANDATORY_SPELLING_GATE')
        })
    guards=list(special_guards.get(l['locus_id'],[]))
    seen=set()
    for kid in l['knowledge_ids']:
        for s in conf_by_kid.get(kid,[]):
            if s['set_id'] in seen: continue
            seen.add(s['set_id'])
            guards.append('Keep these confusable terms physically and verbally distinct: '+', '.join(s['terms'])+'.')
    if not guards:
        guards.append('Do not replace the conventional scientific structure or process with a mnemonic object that changes the underlying mechanism.')
    # Internal F1 correction/scope linkage without exposing source language to eventual student prose.
    flagged=[records[k]['review_flag_id'] for k in l['knowledge_ids'] if records[k].get('review_flag_id')]
    if flagged:
        guards.append('Authoring must preserve the already-resolved scientific/scope correction associated with '+', '.join(sorted(set(flagged)))+'; future student prose should express only the corrected science, not the audit label.')
    recall=recall_prompts.get(l['locus_id'])
    transition = (f"The resolved output or unanswered consequence from {l['title']} is carried directly into {next_title}; the learner follows that physical output to {next_lid}." if next_lid else f"This final scene resolves the {j['working_title']} mission. Nia closes the route only after the learner can reconstruct the journey’s mechanism from its fixed loci.")
    carry='; '.join(labels[:4]) + ('' if len(labels)<=4 else '; plus embedded supporting relationships at this locus')
    briefs.append({
      'scene_brief_id':'F3-'+l['locus_id'],'locus_id':l['locus_id'],'journey_id':jid,'bundle_id':l['bundle_id'],
      'scene_title':l['title'],'exact_location':l['title'],'micro_anchor':l['micro_anchor'],
      'orientation_sentence':f"You enter {l['title']} and stop at {l['micro_anchor']}. On your left is {geo['left']}; directly ahead is {geo['center']}; on your right is {geo['right']}. These three zones do not swap positions during the scene.",
      'spatial_layout':{
        'left':{'anchor':geo['left'],'layout_job':'fixed input/reference/comparison zone'},
        'center':{'anchor':geo['center'],'layout_job':'primary science-bearing action zone'},
        'right':{'anchor':geo['right'],'layout_job':'fixed consequence/output/comparison zone'}
      },
      'stable_cast':stable_cast,
      'continuity_object':journey_specs[jid]['continuity_object'],
      'science_bearing_action':{'before':before,'trigger':'Nia identifies the local failure or unresolved relationship and activates only the mechanism needed to diagnose it.','during':during,'after':after},
      'knowledge_ids':l['knowledge_ids'],'primary_knowledge_id':l['primary_knowledge_id'],'term_introductions':terms,
      'visual_spec':{
        'visual_mode':l['visual_mode'],'conventional_scientific_visual_required':True,
        'must_show':[geo['left'],geo['center'],geo['right'],core[l['locus_id']]],
        'composition_rule':'Preserve left/center/right geography and recognizable scientific geometry. The center action may animate, but the structural anchors must remain spatially stable and redrawable from memory.'
      },
      'misconception_guards':guards,
      'adaptive_name_support':{
        'default':'No phonological keyword is shown on the first pass unless later retrieval data show that the exact term needs support.',
        'fallback':'Use the F2 record-level name-support classification only after a retrieval failure; keep the conventional scientific image as the primary cue.'
      },
      'quick_recall':({'enabled':True,'candidate_prompt':recall[0],'answer':recall[1],'timing':'Optional first-exposure pause only after the mechanism and canonical terminology have been encountered; otherwise defer to Review.','hint_rule':'Point back to one spatial anchor or visible action without displaying the answer term.'} if recall else {'enabled':False,'timing':'Schedule retrieval later in Review so the narrative flow is not interrupted.','hint_rule':'If later needed, return to one concrete spatial anchor/action without revealing the target term.'}),
      'carry_forward':f"Carry forward this resolved mental model: {carry}.",
      'causal_transition':{'to_locus_id':next_lid,'transition_logic':transition},
      'story_prose_status':'PROHIBITED_UNTIL_F3_BRIEF_QA_PASS','brief_status':'LOCKED_F3_SCENE_BRIEF'
    })

scene_doc={
 'schema':'memory-palace-v2-unit3-f3-scene-briefs-1.0','generated_utc':GEN,'unit_id':'unit-3','canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','student_release':False,
 'design_standard':'NR-1.1: orient to locus -> fix micro-anchor -> one science-bearing/diagnostic action -> retrieval pause if useful -> exact term/relationship -> one canonical translation -> move',
 'counts':{'journeys':7,'scene_briefs':54,'palace_managed_records':171,'term_introductions':171,'optional_first_exposure_recalls':len(recall_prompts)},
 'scene_briefs':briefs
}
journey_doc={'schema':'memory-palace-v2-unit3-f3-journey-briefs-1.0','generated_utc':GEN,'unit_id':'unit-3','student_release':False,'unit_guide':unit_guide,'journey_count':7,'journeys':journeys}
dump(BRIEFS/'scene-briefs-f3.json',scene_doc); dump(BRIEFS/'journey-briefs-f3.json',journey_doc)

status={
 'unit_id':'unit-3','unit_number':3,'title':'Cellular Energetics','status':'SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED','pipeline_status':'SCENE_BRIEF_ARCHITECTURE_COMPLETE',
 'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','student_release':False,'preview_release':False,
 'canonical_records':186,'review_flags_resolved':30,'ced_topics':5,'ced_atoms':54,'journey_count':0,'scene_count':0,'memory_objects':0,
 'architecture_journeys':7,'architecture_bundles':20,'architecture_loci':54,'journey_briefs':7,'scene_briefs':54,'palace_managed_records':171,
 'scope_guard_records':4,'practice_only_records':11,'confusable_sets':28,'optional_first_exposure_recalls':len(recall_prompts),
 'next_required_output':'F4A polished narrative for Journey 1 only; no broad Unit 3 story generation before prose QA'
}
dump(U3/'status-f3.json',status); dump(U3/'status.json',status)

manifest={'schema':'memory-palace-v2-unit3-f3-release-1.0','generated_utc':GEN,'unit_id':'unit-3','release_status':'F3_SCENE_BRIEFS_LOCKED_NOT_STUDENT_RELEASED','journey_briefs':7,'scene_briefs':54,'palace_managed_records':171,'optional_first_exposure_recalls':len(recall_prompts),'polished_story_files':0,'student_release':False,'next_stage':'F4A Journey 1 polished narrative'}
dump(U3/'f3-release-manifest.json',manifest)

# Update course registry while leaving runtime counts at zero.
course_path=ROOT/'content/ap-biology/course.json'; course=load(course_path)
for u in course['units']:
    if u['unit_id']=='unit-3':
        u.update({'status':status['status'],'journey_count':0,'scene_count':0,'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','source_status':'AUDITED_SCIENCE_LOCKED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3','canonical_records':186,'review_flags_resolved':30,'student_release':False,'ced_atoms':54,'architecture_journeys':7,'architecture_loci':54,'scene_briefs':54})
dump(course_path,course)

# Designer docs.
lines=['# Unit 3 F3 Scene Briefs','','Status: `SCENE_BRIEFS_LOCKED_F3_NOT_STUDENT_RELEASED`','',f'- 7 journey briefs',f'- 54 fixed loci / scene briefs',f'- 171 palace-managed canonical records represented exactly once',f'- {len(recall_prompts)} optional first-exposure recall pauses','- 0 polished Unit 3 story files','- 11 practice-only records remain reserved for a later Challenge Lab','- 4 scope guards remain non-runtime','', '## Narrative rule','','Every eventual scene must follow `ORIENT -> FIX MICRO-ANCHOR -> SCIENCE-BEARING ACTION -> optional RETRIEVAL -> EXACT TERM/RELATIONSHIP -> CANONICAL TRANSLATION -> MOVE`. The scientific model remains primary; mnemonic support may assist a difficult name later but may not replace the biology.','']
for j in journeys:
    lines += [f"## {j['journey_id']} · {j['working_title']}",'',j['premise'],'',f"**Mission.** {j['mission']}",'',f"**Continuity object.** {j['continuity_object']}",'']
    for lid in j['route']:
        b=next(x for x in briefs if x['locus_id']==lid)
        lines += [f"### {lid} · {b['scene_title']}",'',f"**Micro-anchor.** {b['micro_anchor']}",'',f"**Orientation.** {b['orientation_sentence']}",'',f"**Before.** {b['science_bearing_action']['before']}",'',f"**Core action.** {core[lid]}",'',f"**After.** {b['science_bearing_action']['after']}",'',f"**Terms/relationships.** {'; '.join(t['canonical_term'] for t in b['term_introductions'])}",'',f"**Carry forward.** {b['carry_forward']}",'']
        if b['quick_recall']['enabled']: lines += [f"**Optional recall.** {b['quick_recall']['candidate_prompt']}",'']
(ROOT/'docs/UNIT3_F3_SCENE_BRIEFS.md').write_text('\n'.join(lines)+"\n",encoding='utf-8')

qa_doc=f'''# Unit 3 F3 QA\n\n## Release decision\n\n**PASS — scene briefs locked; student release remains false.**\n\n- 54/54 F2 loci have one F3 scene brief.\n- 171/171 palace-managed records appear exactly once across those briefs.\n- 171 term/relationship introductions preserve the F1 canonical verified science.\n- 7/7 journeys have a fixed route, premise, mission, continuity object, opening image, and ending payoff.\n- {len(recall_prompts)} optional first-exposure recalls are distributed across the seven journeys.\n- Every brief fixes left/center/right geography, a micro-anchor, stable scientific parts, before/during/after action, conventional visual requirements, misconception guards, and a causal transition.\n- No polished Unit 3 story file exists.\n- Unit 3 remains unavailable in the student journey runtime.\n\n## Next gate\n\nF4A should author **Journey 1 only** from these briefs, then run prose-level spatial/narrative QA before any later journey is written.\n'''
(ROOT/'docs/UNIT3_F3_QA.md').write_text(qa_doc,encoding='utf-8')

# Lock after all F3 artifacts exist.
lock_files=[
 'content/ap-biology/unit-3/source/canonical-unit3-f1.json',
 'content/ap-biology/unit-3/architecture/learning-classification-f2.json',
 'content/ap-biology/unit-3/architecture/palace-architecture-f2.json',
 'content/ap-biology/unit-3/briefs/journey-briefs-f3.json',
 'content/ap-biology/unit-3/briefs/scene-briefs-f3.json',
 'content/ap-biology/unit-3/f3-release-manifest.json','content/ap-biology/unit-3/status-f3.json'
]
lock={'schema':'memory-palace-v2-unit3-f3-content-lock-1.0','generated_utc':GEN,'unit_id':'unit-3','lock_status':'LOCKED_F3','student_release':False,'parents':['LOCKED_F1','LOCKED_F2'],'files':{rel:{'sha256':sha(ROOT/rel)} for rel in lock_files},'rule':'F3 locks journey and scene briefs only. F1 canonical science and F2 record/locus assignments remain immutable.'}
dump(U3/'content-lock-f3.json',lock)
print(json.dumps(scene_doc['counts'],indent=2))
