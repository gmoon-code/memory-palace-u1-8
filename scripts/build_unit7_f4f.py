from __future__ import annotations
import json,re,hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U7=ROOT/'content'/'ap-biology'/'unit-7'

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()

CANON={r['knowledge_id']:r for r in read(U7/'source/canonical-unit7-f1.json')['canonical_catalog']}
F3=read(U7/'briefs/scene-briefs-f3.json')
B={b['locus_id']:b for b in F3['scene_briefs'] if b['journey_id']=='U7-J6'}
JB=read(U7/'briefs/journey-briefs-f3.json')
J6=next(j for j in JB['journeys'] if j['journey_id']=='U7-J6')
J1=read(U7/'journeys/U7-J1.json')
J2=read(U7/'journeys/U7-J2.json')
J3=read(U7/'journeys/U7-J3.json')
J4=read(U7/'journeys/U7-J4.json')
J5=read(U7/'journeys/U7-J5.json')

GUIDE={
 'name':'Dr. Imani Vale',
 'role':'evolutionary-systems curator',
 'visual':'charcoal field jacket, pale-green specimen gloves, a slim brass pointer, and a five-slot transparent chronology tray secured beneath her left arm',
 'story_job':'keeps evidence type and timing visible so a plausible chemical process, a historical hypothesis, an experimental result, and a later evolutionary event cannot be treated as the same claim'
}
CONTINUITY=J6['continuity_object']

ROUTE=[
 {'scene_index':0,'locus':'Early Earth Timeline Deck','short':'Timeline','floor':'Timeline deck','symbol':'4.6 → 3.9 → 3.5'},
 {'scene_index':1,'locus':'Prebiotic Chemistry Chamber','short':'Prebiotic chemistry','floor':'Chemistry chamber','symbol':'SMALL ORGANICS'},
 {'scene_index':2,'locus':'Oparin–Haldane Historical Bench','short':'Historical hypothesis','floor':'Historical bench','symbol':'HYPOTHESIS'},
 {'scene_index':3,'locus':'Miller–Urey Simulation Rig','short':'Experiment','floor':'Simulation rig','symbol':'TEST'},
 {'scene_index':4,'locus':'RNA World and Later Endosymbiosis Archive','short':'RNA and later cells','floor':'Final archive','symbol':'RNA → LATER EUK'},
]

SLOTS=[
 {'slot':1,'label':'GEOLOGICAL TIMING','rule':'accepts only evidence constraining when Earth, habitability, and earliest life occur'},
 {'slot':2,'label':'ATMOSPHERIC / GEOCHEMICAL CONDITIONS','rule':'accepts environmental conditions and historical atmosphere models without upgrading hypotheses into settled reconstructions'},
 {'slot':3,'label':'SMALL ORGANIC MOLECULES','rule':'accepts amino acids and other small organics without calling them polymers, cells, or life'},
 {'slot':4,'label':'REPLICATING / CATALYTIC RNA','rule':'accepts RNA-world requirements for templated copying, continuity, and catalysis'},
 {'slot':5,'label':'LATER EUKARYOTIC ENDOSYMBIOSIS','rule':'accepts mitochondria and chloroplast origin only after first cellular life already exists'},
]

ZONES={
'U7-L51':[
 ('left','4.6-bya Earth-formation marker','4.6 BYA','A black basalt marker fixes Earth formation near 4.6 billion years ago at the beginning of the chronological deck.'),
 ('center','Early-Earth and earliest-life timeline','HABITABILITY','A long illuminated center timeline separates Earth formation, later habitable conditions, and evidence for early life.'),
 ('right','3.9- and 3.5-bya evidence markers','3.9 / 3.5','Two fixed markers constrain later habitability near 3.9 billion years ago and earliest fossil evidence for life near 3.5 billion years ago without assigning every earliest fossil to cyanobacteria.')],
'U7-L52':[
 ('left','Low-free-oxygen early-atmosphere side','LITTLE O₂','A gas chamber shows little free molecular oxygen while lightning, ultraviolet radiation, volcanism, and geochemical gradients remain available as energy sources.'),
 ('center','Abiotic organic-synthesis chamber','ABIOTIC','A reaction chamber permits small organic molecules to form from nonliving chemistry under plausible prebiotic conditions.'),
 ('right','Monomer-versus-macromolecule boundary','SMALL ≠ LIFE','A hard glass boundary keeps amino acids and other small organics separate from polymers, protocells, self-replicating systems, and cellular life.')],
'U7-L53':[
 ('left','Oparin-Haldane hypothesis card','HISTORICAL','A dated card presents a strongly reducing atmosphere as the historical Oparin-Haldane model rather than a settled modern reconstruction.'),
 ('center','Historical atmosphere model bench','MODEL','A bench reconstructs the reducing-atmosphere scenario and its energy sources as a hypothesis about abiotic organic synthesis.'),
 ('right','Modern-evidence qualification panel','QUALIFY','A modern panel shows substantial nitrogen and carbon dioxide, little oxygen, and possible locally reducing volcanic environments as a better-qualified evidence picture.')],
'U7-L54':[
 ('left','Simulated gases and energy input','INPUT','A sealed flask train contains the historical gas mixture, circulating water, and electrical energy used to model prebiotic chemistry.'),
 ('center','Miller-Urey apparatus','SIMULATION','A glass circulation apparatus cycles water vapor and gases through an electrical spark while remaining visibly an experiment, not an early Earth time machine.'),
 ('right','Small-organic-molecule product trap','PRODUCTS','A collection trap receives amino acids and other small organic compounds while a red boundary blocks labels for proteins, nucleic acids, cells, or life.')],
'U7-L55':[
 ('left','RNA replication and complementary-base-pairing side','COPY','RNA strands align by complementary bases so information can be copied into descendant replicating systems.'),
 ('center','RNA-world catalytic archive','RNA + CATALYSIS','Catalytic RNA models and ribozyme examples occupy the center so information storage and some catalytic activity can coexist before genetically encoded protein catalysts are required.'),
 ('right','Later endosymbiosis boundary','MUCH LATER','A separate eukaryotic panel contains mitochondria and chloroplast endosymbiosis behind a chronological barrier that first requires already-existing cellular life.')],
}

NARR={
'U7-L51':{
 'title':'The Lab Has Put the Last Event at the Beginning of the Timeline',
 'kicker':'Origins-of-life models must fit geological timing before chemical hypotheses are allowed onto the evidence tray.',
 'paragraphs':[
  "The doors of the **Origins of Life Geochemistry Lab** open onto a long black timeline suspended above a floor of volcanic glass. On your **left**, a basalt marker reads 4.6 BILLION YEARS AGO. Directly **ahead**, the center timeline runs through a dark interval toward later habitable conditions. On your **right**, two illuminated markers read roughly 3.9 BILLION YEARS AGO and roughly 3.5 BILLION YEARS AGO. Dr. Imani Vale stands beside a transparent tray divided into five numbered slots. The first is GEOLOGICAL TIMING. The second is ATMOSPHERIC AND GEOCHEMICAL CONDITIONS. The third is SMALL ORGANIC MOLECULES. The fourth is REPLICATING AND CATALYTIC RNA. The fifth is LATER EUKARYOTIC ENDOSYMBIOSIS. A red alarm flashes because the fifth slot has been placed at the beginning of the timeline.",
  "Imani removes the endosymbiosis card and leaves the tray empty. The first task is chronology. She locks the left marker at Earth formation near 4.6 billion years ago. The center timeline then advances to conditions that became less hostile for persistent liquid water and life roughly 3.9 billion years ago. Farther right, the earliest fossil evidence for life is placed near 3.5 billion years ago. Imani keeps the wording at the evidence level. Ancient microbial fossils and stromatolite-like evidence support very early life, but the route does not require every earliest fossil to be identified definitively as cyanobacterial.",
  "Only after the dates are visible does she state **Earth and earliest-life dates**. Earth formed about 4.6 billion years ago, conditions were too hostile for life until roughly 3.9 billion years ago, and the earliest fossil evidence for life dates to about 3.5 billion years ago. The timeline is deliberately approximate. It constrains plausible histories without pretending that every step between nonliving chemistry and cellular life has a precise date stamped onto it.",
  "Imani slides the three dated markers into the first tray slot and names **Geological evidence for origin-of-life timing**. Geological evidence constrains models of when and under what conditions life could have originated. Any chemical model proposed later has to fit inside those broad constraints. A hypothesis that requires stable life before Earth was habitable is chronologically impossible. A hypothesis that concerns later eukaryotic organelles belongs much farther to the right than the origin of the first cellular life.",
  "The center timeline now receives the broader label **Evidence-based origin-of-life models**. Models for the origin of life are evaluated using evidence from geology, chemistry, physics, and experiments on plausible prebiotic processes. Imani points to the word models. The lab is not reconstructing one filmed sequence of events. It is comparing hypotheses against constraints and experimental plausibility. Each later room will earn a different type of evidence and place it in a different tray slot.",
  "The first slot locks with a click. The second slot begins flashing as the wall ahead fills with gases. A broken oxygen gauge shoots toward modern atmospheric levels, and a spark coil begins firing beside it. Imani stops the machine before it can call oxygen the fuel of prebiotic organic synthesis. The next chamber will correct the early atmosphere, identify plausible energy sources, and keep small organic molecules physically separate from polymers and life."
 ]},
'U7-L52':{
 'title':'The Chemistry Chamber Keeps Turning Small Molecules Into Life',
 'kicker':'Abiotic production of small organic molecules is chemically plausible under several prebiotic conditions, but it is only one step in a much longer origin-of-life problem.',
 'paragraphs':[
  "The **Prebiotic Chemistry Chamber** is split into three glass compartments. On your **left**, an atmosphere tank glows under a gauge reading LITTLE FREE OXYGEN. Lightning arcs, ultraviolet lamps, volcanic heat, and a mineral-gradient column surround it. Directly **ahead**, the center reaction chamber contains simple starting chemicals and a collector for products formed without living cells. On your **right**, a thick glass boundary separates SMALL ORGANIC MOLECULES from four locked boxes labeled POLYMERS, COMPARTMENTS, SELF-REPLICATION, and CELLULAR LIFE. Imani places the five-slot tray beneath the center chamber and opens slot two.",
  "She first drains the modern oxygen level from the left tank. The display names **Early Earth had little free oxygen**. Earth's early atmosphere contained little free molecular oxygen. Proposed prebiotic organic synthesis relied on other atmospheric and geochemical conditions plus energy sources such as lightning, ultraviolet radiation, volcanism, or chemical gradients. Imani makes the oxygen gauge stay visibly low so the learner cannot remember an oxygen-rich early atmosphere simply because modern life depends heavily on oxygen today.",
  "The center chamber then runs several plausible nonliving chemical scenarios. Small organic products appear without any organism producing them. Imani records **Abiotic synthesis of organic molecules**. Laboratory and geochemical evidence shows that small organic molecules can form abiotically under multiple plausible prebiotic conditions. The phrase multiple plausible conditions remains visible. The origin-of-life question is not restricted to one exact flask mixture or one universally accepted atmospheric recipe.",
  "A meteorite drawer opens beneath the left wall and releases a sealed sample card containing amino acids and other organics. Imani places it beside the terrestrial chemistry evidence and records **Meteorites as an organic-molecule source**. Meteorites contain amino acids and other organic compounds, supporting extraterrestrial delivery as one possible contributor to the prebiotic organic inventory. The meteorite card goes into the SMALL ORGANIC MOLECULES slot with a label reading POSSIBLE CONTRIBUTOR. It is not allowed to become the entire origin-of-life explanation.",
  "The right boundary is the critical safeguard. The center chamber produces amino acids and other small organic compounds, but the four locked boxes stay closed. Imani records **Organic monomers and macromolecule formation are separate steps**. The abiotic formation of small organic molecules does not by itself demonstrate the formation of proteins, nucleic acids, cells, or life. Polymerization, compartmentalization, and self-replicating systems require additional processes. The lab therefore refuses to move a small organic molecule directly into the LIFE box.",
  "Slots two and three of the tray now contain qualified evidence. Slot two carries low oxygen and plausible geochemical conditions. Slot three carries small organics from terrestrial chemistry and meteorite delivery. A historical card rises from the next bench and claims that Earth's entire early atmosphere was strongly reducing. Imani recognizes the name attached to it but does not accept the model as settled fact. The next room will place that historical hypothesis in context before the experiment built from it is allowed to run."
 ]},
'U7-L53':{
 'title':'A Historical Atmosphere Model Is Useful Without Becoming the Modern Atmosphere',
 'kicker':'The Oparin-Haldane reducing-atmosphere model is historically important and testable, yet modern evidence requires a more qualified reconstruction of early Earth.',
 'paragraphs':[
  "The **Oparin-Haldane Historical Bench** looks like a courtroom for old scientific ideas. On your **left**, a dated card bears the names Oparin and Haldane beside a diagram of a strongly reducing atmosphere supplied with energy. Directly **ahead**, the center bench reconstructs that historical atmosphere model under a glass hood. On your **right**, a modern-evidence panel shows substantial nitrogen and carbon dioxide, little free oxygen, and a separate volcanic zone labeled LOCALLY REDUCING CONDITIONS POSSIBLE. Imani places the chronology tray along the front rail so historical hypothesis and modern evidence occupy visibly different positions.",
  "She begins with the left card and introduces the exact term **Oparin-Haldane hypothesis**. Oparin and Haldane historically proposed that organic molecules could arise abiotically in a reducing early atmosphere supplied with energy. The proposal was important because it converted a broad origin question into a chemical hypothesis that could be explored experimentally. The card therefore earns a place in the evidence route, but Imani stamps it HISTORICAL HYPOTHESIS rather than EARLY ATMOSPHERE CONFIRMED.",
  "The center bench displays the logic of the model. If a strongly reducing gas mixture were exposed to energy, could small organic molecules arise abiotically? That is the chemical question the model helps pose. Imani keeps the product expectation limited to small organics because the earlier chamber already established the monomer boundary. Nothing about the historical model itself demonstrates proteins, nucleic acids, protocells, self-replication, or living cells.",
  "She then turns to the right panel. Current evidence does not require the whole early atmosphere to match the strongly reducing mixture used in the historical model. A better-qualified picture includes substantial nitrogen and carbon dioxide, little oxygen, and the possibility of locally reducing volcanic environments. Imani leaves both panels standing at once. The historical model remains scientifically important without being treated as the only plausible reconstruction of early Earth chemistry.",
  "The tray records two separate lines. HISTORICAL MODEL and MODERN QUALIFICATION. This distinction protects the next experiment from a common exaggeration. An experiment can test whether chemistry works under specified simulated conditions even if those conditions do not perfectly reconstruct the whole planet. Its result supports a claim about chemical possibility under the tested conditions. It does not prove that the exact same atmosphere existed everywhere on early Earth. Imani also places a small LOCAL CONDITIONS tag beside the volcanic zone. A planet can contain chemically distinct environments, so evidence for local reducing conditions does not require the entire atmosphere to share the same composition at the same time.",
  "A glass conduit opens from the center bench into the next room. Water begins circulating through a flask, the historical gas mixture enters a chamber, and an electrical spark gap starts clicking. Imani carries the tray forward with the Oparin-Haldane card still marked hypothesis. The next room will ask what the experiment actually produced and will refuse to upgrade amino acids into life."
 ]},
'U7-L54':{
 'title':'The Spark Apparatus Produces Organics and the Lab Tries to Call Them Cells',
 'kicker':'The Miller-Urey experiment demonstrated abiotic formation of small organic compounds under simulated conditions and did not create life.',
 'paragraphs':[
  "The **Miller-Urey Simulation Rig** fills a bright glass room with circulating tubes. On your **left**, a flask of water connects to a chamber containing the historical gas mixture and an electrical spark source. Directly **ahead**, the center apparatus cycles vapor through the spark chamber and back through a condenser. On your **right**, a product trap slowly collects brownish solution beneath the label SMALL ORGANIC MOLECULES. Four red lights above it read NOT POLYMERS, NOT PROTOCELLS, NOT SELF-REPLICATING SYSTEMS, and NOT LIFE. Imani places the Oparin-Haldane hypothesis card beside the input so the tested historical model remains visible.",
  "The apparatus begins cycling. Water vapor moves into the simulated atmosphere. Electrical energy passes through the gas mixture. Condensed products drain into the trap where they are protected from repeated sparking. After the simulated run, the trap contains amino acids and other small organic compounds. Only after the products are chemically identified does Imani introduce the **Miller-Urey experiment**. Miller, working with Urey, tested a historical early-atmosphere model and demonstrated that amino acids and other small organic compounds could form abiotically under the simulated conditions.",
  "The experiment earns a strong but narrow claim. Under the specified simulated conditions, nonliving chemistry produced small organic molecules. Imani places that result in slot three beside the earlier abiotic-synthesis and meteorite evidence. Multiple evidence routes can contribute to a prebiotic organic inventory. The tray does not require the Miller-Urey mixture to be accepted as a perfect modern reconstruction of Earth's entire early atmosphere for the chemical result to remain historically and conceptually informative.",
  "The broken lab then tries to print LIFE CREATED across the product trap. Imani kills the printer. The collected amino acids are not proteins. The apparatus did not generate a nucleic-acid replication system. It did not create a membrane-bounded cell. It did not establish heredity, metabolism, or biological evolution. Those missing transitions matter because an origin-of-life model requires more than a supply of small organic building blocks.",
  "She also blocks the opposite mistake. Correcting the historical atmosphere does not make the experiment meaningless. It still demonstrated that abiotic organic synthesis is chemically possible under the simulated conditions, and later experiments and geochemical work explore other plausible environments. The evidence belongs exactly where the tray places it. CHEMICAL POSSIBILITY FOR SMALL ORGANICS. Nothing stronger is needed for the lesson and nothing weaker accurately represents the result.",
  "The optional recall light covers the apparatus labels while the input flask, spark chamber, and product trap remain visible. When the labels return, slot four begins flashing. A set of RNA strands slides into the final archive beside catalytic RNA models. Far to the right, mitochondria and chloroplasts appear behind a barrier labeled MUCH LATER. The final room must now solve two different problems without merging them. How could an early genetic system support copying and catalysis, and why does endosymbiosis belong much later than the origin of the first cellular life?"
 ]},
'U7-L55':{
 'title':'RNA Enters the Early-Life Slot While Endosymbiosis Is Locked Far Downstream',
 'kicker':'RNA-world models address early heredity and catalysis, while endosymbiosis explains a much later step in eukaryotic evolution.',
 'paragraphs':[
  "The **RNA World and Later Endosymbiosis Archive** is the only room divided by a chronological wall. On your **left**, complementary RNA strands lie on a replication table with matching bases aligned. Directly **ahead**, the center archive contains folded catalytic RNA models and a ribozyme reaction display. On your **right**, a distant eukaryotic panel shows an ancestral host cell with bacterial endosymbionts that later correspond to mitochondria and chloroplasts. A floor line between center and right reads FIRST CELLULAR LIFE MUST ALREADY EXIST BEFORE THIS BOUNDARY. Imani opens slot four of the evidence tray but keeps slot five closed.",
  "She begins at the left replication table and introduces the **RNA world hypothesis** only after the molecules are visible. The RNA world hypothesis proposes that RNA could have served as an early genetic material before modern DNA-protein systems evolved. The hypothesis does not claim that scientists have recovered the exact first RNA system. It proposes a plausible stage in which one type of molecule could participate in both information storage and functions now divided among DNA, RNA, and proteins.",
  "The complementary strands align. One strand provides a template for another through base matching. Imani records **Base pairing in RNA replication**. Complementary base pairing provides the informational template needed for replication in an RNA-world model. The copied sequence then moves into a descendant tray, demonstrating **RNA replication and genetic continuity**. An RNA-world model requires a mechanism by which RNA sequences could be copied so genetic information persisted across generations of replicating systems. The word continuity is tied to copied information across successive replicating systems, not to one molecule simply surviving for a long time.",
  "At the center archive, a folded RNA molecule accelerates a model reaction. Imani records **Catalytic RNA and ribozymes**. Some RNA molecules can catalyze reactions, supporting the plausibility of an early stage in which RNA served both informational and catalytic roles. She then adds **Catalysis before encoded proteins**. An RNA-world model assumes that genetically encoded proteins were not initially required as catalysts. Catalytic RNA could perform some functions. The scene does not require RNA to perform every reaction needed by a modern cell. It establishes the plausibility of catalytic activity before a full encoded protein system.",
  "Only after slot four is complete does Imani unlock the far-right panel. A formerly free-living prokaryotic cell becomes incorporated into an ancestral host lineage and persists as an endosymbiont. The display records **Endosymbiosis is later than life's origin**. Endosymbiosis explains the evolutionary origin of mitochondria and chloroplasts from formerly free-living prokaryotes within ancestral host cells. It is a later event than the origin of the first cellular life. The host must already be a cell, and the bacterial partner must already be a living cell, so this event cannot explain how life first began.",
  "The final optional recall darkens the labels while all five tray slots remain visible in chronological order. When the lights return, Imani reconstructs the route. Geological evidence constrained timing. Early geochemistry permitted abiotic small-organic synthesis under multiple plausible conditions. The Oparin-Haldane model remained a historical hypothesis. Miller-Urey demonstrated small-organic synthesis under simulated conditions. RNA-world reasoning addressed a possible early system for copying information and catalysis. Endosymbiosis stayed far downstream as an explanation for mitochondria and chloroplasts in eukaryotic evolution. The alarm turns green because the lab finally distinguishes evidence, hypothesis, experiment, plausible prebiotic mechanism, and later cellular evolution without pretending that any single station created life."
 ]},
}

CHECKPOINTS={'U7-L54','U7-L55'}

def clean_prose(text):
    return text.replace(' — ', '. ').replace('—','-').replace(': ','. ')

def word_count(paragraphs):
    return len(re.findall(r"\b[\w’′'-]+\b",' '.join(paragraphs)))

def zone_objs(lid):
    return [{'position':p,'label':label,'symbol':symbol,'description':description} for p,label,symbol,description in ZONES[lid]]

def cast_for(lid):
    items=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    for position,label,symbol,description in ZONES[lid]:
        items.append({'name':label,'kind':'geological, chemical, experimental, or evolutionary evidence zone','visual':description,'job':f"Remain fixed on the learner's {position} and carry the {position}-side scientific role required by the locked F3 geometry."})
    items.append({'name':'Five-slot chronology tray','kind':'journey continuity object','visual':'a transparent evidence tray with permanently numbered slots for geological timing, atmospheric/geochemical conditions, small organic molecules, replicating/catalytic RNA, and later eukaryotic endosymbiosis','job':'keeps evidence type and chronology fixed so later events cannot migrate into earlier origin-of-life stages'})
    items.append({'name':'Chronology rail','kind':'persistent temporal boundary','visual':'a black-to-gold timeline running from Earth formation through earliest life and onward to later eukaryotic evolution','job':'forces every evidence card or model into a temporal position consistent with geological constraints'})
    items.append({'name':'Claim-strength stamp','kind':'evidence qualifier','visual':'a brass stamp with separate settings for EVIDENCE, HISTORICAL HYPOTHESIS, EXPERIMENTAL RESULT, PLAUSIBLE MODEL, and LATER EVOLUTIONARY EVENT','job':'prevents experimental or historical claims from being inflated into direct demonstration of the complete origin of life'})
    return items

def beats_for(lid):
    b=B[lid]
    terms={t['knowledge_id']:t for t in b['term_introductions']}
    scene_hint={
      'U7-L51':'the 4.6, 3.9, and 3.5 billion-year markers arranged before any chemistry or later cell-evolution event enters the tray',
      'U7-L52':'the low-oxygen atmosphere and abiotic synthesis chamber ending at the hard boundary between small organics and polymers, cells, or life',
      'U7-L53':'the Oparin-Haldane historical card kept separate from the modern-evidence qualification panel',
      'U7-L54':'the simulated gases and spark apparatus feeding only amino acids and other small organics into the product trap',
      'U7-L55':'the complementary RNA copying and catalytic RNA archive kept chronologically separate from later mitochondrial and chloroplast endosymbiosis',
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
for i,lid in enumerate(J6['route']):
    b=B[lid]; n=NARR[lid]; route=ROUTE[i]
    paragraphs=[clean_prose(p) for p in n['paragraphs']]
    cp=lid in CHECKPOINTS
    scenes.append({
      'scene_index':i,'locus_id':lid,'locus':route['locus'],'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['micro_anchor'],'scene_layout':{'orientation':b['orientation_sentence'],'zones':zone_objs(lid)},
      'cast':cast_for(lid),'chronology_slots':SLOTS,'continuity_object':CONTINUITY,
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
 'palace_id':'U7-J6','unit_id':'unit-7','palace_name':'Origins of Life Geochemistry Lab',
 'story_title':'The Geochemistry Lab That Put the Last Event First',
 'tagline':'A five-slot evidence tray has been scrambled so later eukaryotic events appear before the chemistry of early Earth. Restore geological timing, prebiotic chemistry, historical hypotheses, experimental evidence, RNA-world requirements, and later endosymbiosis to their proper places without letting any one station claim it created life.',
 'guide':GUIDE,
 'premise':'The Origins of Life Geochemistry Lab has failed its chronology audit. Endosymbiosis has been placed before the first cells, modern oxygen levels have been copied into the early atmosphere, the Oparin-Haldane model has been labeled settled fact, the Miller-Urey product trap has been labeled life, and RNA-world requirements have been separated from replication and catalysis. Dr. Imani Vale seals one five-slot chronology tray and refuses to accept any claim until its evidence type, timing, and strength are correct.',
 'mission':'Carry one numbered evidence tray through five permanent locations. Fix the broad geological dates, qualify early-Earth chemistry, separate small organic molecules from later polymerization and cellular steps, place the Oparin-Haldane model in historical context, state the Miller-Urey result precisely, reconstruct RNA-world requirements for genetic continuity and catalysis, and keep mitochondrial/chloroplast endosymbiosis far later than the origin of first cellular life.',
 'finale':'The lab clears its audit when all five slots are filled in order and every claim retains its evidentiary strength. Geological constraints, plausible abiotic chemistry, a historical atmosphere hypothesis, a simulation result, an RNA-world model, and later eukaryotic endosymbiosis are connected chronologically without being treated as equivalent evidence or as one demonstrated sequence.',
 'estimated_minutes':20,'scene_count':5,'checkpoint_count':len(CHECKPOINTS),
 'student_release':'DEVELOPER_PREVIEW_F4F','preview_release':True,'narrative_design':'U7-F4F-NARRATIVE-1.0',
 'learner_rule':'Read or listen while keeping the five numbered evidence slots in chronological order. A card cannot move to a new slot unless its timing and claim type justify the move. Exact terms appear after the relevant evidence or model is visible.',
 'route_orientation':'The lab is one chronological route. Begin at the geological timeline, enter prebiotic chemistry, qualify the historical Oparin-Haldane model, run the Miller-Urey simulation, and finish in the RNA-world archive with later endosymbiosis locked beyond a visible temporal boundary.',
 'route':ROUTE,'chronology_slots':SLOTS,'scenes':scenes,
 'source_brief_lock':'LOCKED_F3','scientific_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2',
 'frozen_prior_journey_lock':'LOCKED_F4E_J1_J5'
}

(U7/'journeys'/'U7-J6.json').write_text(json.dumps(journey,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

summary={
 'schema':'memory-palace-v2-unit7-f4f-journeys-1.0','unit_id':'unit-7','stage':'F4F','student_release':False,'preview_release':True,
 'journey_count':6,'scene_count':55,'checkpoint_count':sum(x['checkpoint_count'] for x in [J1,J2,J3,J4,J5])+len(CHECKPOINTS),
 'guided_journeys':[
   {k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']}
   for j in [J1,J2,J3,J4,J5,journey]
 ]
}
(U7/'journeys-f4f.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

status={
 'unit_id':'unit-7','number':7,'title':'Natural Selection','status':'F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','pipeline_stage':'F4F_JOURNEY6_NARRATIVE',
 'canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','narrative_lock':'LOCKED_F4F_J1_J6',
 'student_release':False,'preview_release':True,'journey_count':6,'scene_count':55,'memory_objects':0,'application_challenges':0,
 'canonical_records':215,'architecture_journeys':6,'architecture_bundles':23,'architecture_loci':55,'scene_briefs':55,'palace_managed_records':174,
 'challenge_lab_records':16,'scope_guard_records':25,'exact_name_review_targets':94,'confusable_sets':33,'optional_first_exposure_recalls':18,
 'f4f_journey':'U7-J6','f4f_scene_count':5,'f4f_knowledge_records':15,'f4f_exact_name_targets':3,'f4f_optional_recalls':len(CHECKPOINTS),
 'next_required_output':'F5 curriculum/runtime integration. Build Unit 7 Memory Objects, Challenge Lab tasks, delayed Review targets, mixed-discrimination records, scope-guard runtime protections, and final Unit 7 developer runtime only after all six F4 narratives remain frozen.'
}
(U7/'status-f4f.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(U7/'status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'
course=read(cp)
u=next(x for x in course['units'] if x['unit_id']=='unit-7')
u.update({
 'status':'F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','journey_count':6,'scene_count':55,'student_release':False,'preview_release':True,
 'source_status':'AUDITED_F1_ARCHITECTURE_F2_BRIEFS_F3_NARRATIVE_F4A_F4B_F4C_F4D_F4E_F4F','narrative_lock':'LOCKED_F4F_J1_J6','narrative_journeys':6,
 'pipeline_stage':'F4F_JOURNEY6_NARRATIVE'
})
cp.write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

doc=['# Unit 7 F4F · Journey 6 Narrative','','## The Geochemistry Lab That Put the Last Event First','',journey['tagline'],'',
     '### Physical route','', ' → '.join(x['locus'] for x in ROUTE),'','### Five-slot chronology tray','']
for slot in SLOTS:
    doc.append(f"- **{slot['slot']} · {slot['label']}** — {slot['rule']}")
doc += ['','### Continuity rule','',CONTINUITY,'']
for s in scenes:
    doc += [f"## {s['scene_index']+1}. {s['locus']} · {s['title']}",'',f"*{s['scene_kicker']}*",'']
    doc += s['story_paragraphs']+['']
    if s['checkpoint']:
        doc += ['**Optional Quick Recall**','',s['checkpoint_prompt'],'']
(ROOT/'docs'/'UNIT7_F4F_JOURNEY6_STORY.md').write_text('\n'.join(doc),encoding='utf-8')

# Protect prior Journeys 1–5 and their release evidence.
f4e=read(U7/'content-lock-f4e.json')
prior_files=dict(f4e.get('prior_narrative_protection',{}))
for rel in [
    'content/ap-biology/unit-7/journeys/U7-J5.json',
    'content/ap-biology/unit-7/journeys-f4e.json',
    'content/ap-biology/unit-7/status-f4e.json',
    'content/ap-biology/unit-7/content-lock-f4e.json',
    'content/ap-biology/unit-7/f4e-release-manifest.json',
    'docs/UNIT7_F4E_JOURNEY5_STORY.md',
    'docs/UNIT7_F4E_RELEASE.md',
    'docs/UNIT7_F4E_QA.md',
    'docs/UNIT7_F4E_PACKAGE_QA.md',
]:
    rp=ROOT/rel
    if rp.exists(): prior_files[rel]={'bytes':rp.stat().st_size,'sha256':sha(rp)}

locked_rel=['journeys/U7-J6.json','journeys-f4f.json','status-f4f.json']
lock_files={rel:{'bytes':(U7/rel).stat().st_size,'sha256':sha(U7/rel)} for rel in locked_rel}
lock={
 'schema':'memory-palace-v2-unit7-f4f-lock-1.0','unit_id':'unit-7','lock_status':'LOCKED_F4F_J1_J6','student_release':False,'preview_release':True,
 'protected_prior_locks':['content-lock-f1.json','content-lock-f2.json','content-lock-f3.json','content-lock-f4a.json','content-lock-f4b.json','content-lock-f4c.json','content-lock-f4d.json','content-lock-f4e.json'],
 'prior_narrative_protection':prior_files,
 'journey_id':'U7-J6','scene_count':5,'knowledge_record_count':15,'exact_name_target_count':3,'checkpoint_count':len(CHECKPOINTS),
 'files':lock_files,
 'rule':'Journeys 1 through 5 remain frozen byte-for-byte. Journey 6 polished prose may not change after F4F without a new explicit narrative version. F1 science, F2 classification/geometry, and F3 scene briefs remain authoritative.'
}
(U7/'content-lock-f4f.json').write_text(json.dumps(lock,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

release={
 'schema':'memory-palace-v2-unit7-f4f-release-1.0','generated_utc':'2026-09-09T00:30:00+00:00','unit_id':'unit-7',
 'release_status':'F4F_ALL6_JOURNEYS_POLISHED_DEVELOPER_PREVIEW','student_release':False,'preview_release':True,
 'completed_journeys':['U7-J1','U7-J2','U7-J3','U7-J4','U7-J5','U7-J6'],'journeys':6,'scenes':55,
 'f4f_journey_id':'U7-J6','f4f_scenes':5,'f4f_knowledge_records':15,'f4f_exact_name_targets':3,'f4f_optional_first_exposure_recalls':len(CHECKPOINTS),
 'canonical_records':215,'permanent_loci_architecture':55,'scene_briefs':55,'memory_objects':0,'application_challenges':0,
 'scientific_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','narrative_lock':'LOCKED_F4F_J1_J6',
 'next_stage':'F5 curriculum/runtime integration after all six narratives are frozen'
}
(U7/'f4f-release-manifest.json').write_text(json.dumps(release,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

print(json.dumps({
 'journey':'U7-J6','scenes':5,'knowledge_records':15,'exact_name_targets':3,'checkpoints':len(CHECKPOINTS),
 'words':sum(s['narrative_word_count'] for s in scenes),
 'mean_words':round(sum(s['narrative_word_count'] for s in scenes)/5,1),
 'min_words':min(s['narrative_word_count'] for s in scenes),
 'max_words':max(s['narrative_word_count'] for s in scenes),
},indent=2))
