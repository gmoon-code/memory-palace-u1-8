from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content'/'ap-biology'/'unit-3'
briefs=json.loads((U3/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
jbriefs=json.loads((U3/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
B={s['locus_id']:s for s in briefs if s['journey_id']=='U3-J7'}
J7=next(j for j in jbriefs if j['journey_id']=='U3-J7')

GUIDE={
 'name':'Dr. Nia Park',
 'role':'cellular-energetics investigator',
 'visual':'navy field jacket, clear safety glasses, and a compact tablet now showing a nearly empty NAD⁺ card rack beside separate ETC and fermentation route indicators',
 'story_job':'Nia keeps electron-carrier recycling visible across every branch so aerobic respiration, anaerobic respiration, alcohol fermentation, and lactate formation remain mechanistically distinct.'
}

route=[
 {'scene_index':0,'locus':'Respiration Across Life Junction','short':'Route Junction','floor':'Annex entrance','symbol':'3 routes'},
 {'scene_index':1,'locus':'Fermentation NAD⁺ Recycling Gate','short':'NAD⁺ Gate','floor':'Cytosolic loop','symbol':'NAD⁺'},
 {'scene_index':2,'locus':'Alcohol Fermentation Vat','short':'Alcohol','floor':'Fermentation bay A','symbol':'EtOH'},
 {'scene_index':3,'locus':'Lactate Fermentation Track','short':'Lactate','floor':'Fermentation bay B','symbol':'Lac'},
]

ZONE_COPY={
'U3-L51':[
 ('left','Aerobic oxygen-terminal route','O₂ + ETC','A conventional respiratory ETC runs on the left and ends at oxygen, preserving the aerobic route from Journey 6 as the reference condition.'),
 ('center','Shared energy-harvesting junction','glycolysis → NADH','A cytosolic glycolysis platform in the center keeps producing pyruvate, ATP, and NADH while the finite rack of oxidized NAD⁺ cards visibly empties.'),
 ('right','Anaerobic and fermentative alternatives','ETC / no ETC','Two clearly separated right-side branches show anaerobic respiration using an ETC with a non-oxygen terminal acceptor and fermentation regenerating NAD⁺ without an ETC.')],
'U3-L52':[
 ('left','Glycolysis NADH output','NADH','Reduced NADH cards arrive from glycolysis on the left after NAD⁺ accepted electrons during substrate oxidation.'),
 ('center','Fermentation redox gate','organic acceptor','The center gate transfers electrons from NADH to an organic molecule without routing those electrons through an electron-transport chain.'),
 ('right','Regenerated NAD⁺ return path','NAD⁺ → glycolysis','Oxidized NAD⁺ cards leave on a return conveyor to glycolysis, restoring the carrier required for continued oxidation and ATP production by substrate-level phosphorylation.')],
'U3-L53':[
 ('left','Pyruvate decarboxylation station','3C → 2C + CO₂','Pyruvate enters on the left, loses one carbon as CO₂, and becomes the two-carbon intermediate acetaldehyde.'),
 ('center','Acetaldehyde intermediate vat','acetaldehyde','The center vat holds acetaldehyde as a real intermediate between pyruvate and ethanol, preventing the pathway from being remembered as one unexplained jump.'),
 ('right','Ethanol and NAD⁺ output','ethanol + NAD⁺','NADH reduces acetaldehyde to ethanol on the right, returning NAD⁺ to the shared carrier rack while the carbon product leaves as ethanol.')],
'U3-L54':[
 ('left','Pyruvate and NADH input','pyruvate + NADH','Pyruvate and reduced NADH enter together from the left with no decarboxylation step and no CO₂-release chute.'),
 ('center','Lactate-forming reaction','pyruvate → lactate','The center reaction directly reduces the full three-carbon pyruvate molecule to lactate while NADH is simultaneously oxidized back to reusable NAD⁺.'),
 ('right','Lactate transport and reuse','lactate shuttle','Lactate leaves on transport routes toward tissues that can oxidize it or toward liver and kidney pathways where its carbon can contribute to glucose synthesis.')],
}

CAST={
'U3-L51':[
 ('NAD⁺ card rack','redox continuity object','a nearly empty rack of white NAD⁺ cards mounted beside the central glycolysis platform','shows that glycolysis depends on a reusable oxidized electron carrier and creates the problem the annex must solve'),
 ('aerobic route','reference pathway','a left-side inner-membrane ETC ending at a clearly labeled O₂ basin','provides the oxygen-terminal respiratory reference already established in Journey 6'),
 ('anaerobic-respiration branch','alternative respiratory pathway','an upper-right ETC ending at a terminal-acceptor socket labeled nitrate / sulfate / other','shows that respiration can use an ETC even when oxygen is not the terminal electron acceptor'),
 ('fermentation branch','non-ETC redox pathway','a lower-right redox loop with an organic molecule accepting electrons directly from NADH','shows the fundamentally different strategy used to regenerate NAD⁺ without an ETC')],
'U3-L52':[
 ('NADH cards','reduced electron carriers','blue-edged NADH cards arriving from glycolysis with electron markers attached','carry reducing power away from glycolytic oxidation and must be reoxidized if the NAD⁺ supply is to be restored'),
 ('organic electron acceptor','fermentation reactant','an organic carbon molecule positioned inside the central redox gate','accepts electrons from NADH during fermentation rather than serving as a terminal acceptor at the end of an ETC'),
 ('NAD⁺ return conveyor','carrier-recycling route','a right-side conveyor carrying white NAD⁺ cards back toward the glycolysis platform','makes NAD⁺ regeneration the immediate functional payoff of fermentation')],
'U3-L53':[
 ('pyruvate','three-carbon fermentation input','a conventional three-carbon pyruvate model entering the left station','provides the carbon starting material for the alcohol-fermentation sequence'),
 ('acetaldehyde','two-carbon intermediate','a two-carbon acetaldehyde model held in the center vat after CO₂ is removed','serves as the intermediate that receives electrons from NADH before becoming ethanol'),
 ('NADH / NAD⁺ carrier pair','redox carrier','a blue-edged NADH card that returns white as NAD⁺ beside the ethanol outlet','makes the redox purpose of the second step visible separately from the carbon conversion')],
'U3-L54':[
 ('pyruvate','three-carbon acceptor','a conventional pyruvate model entering from the left beside NADH','receives electrons directly from NADH during lactate formation'),
 ('lactate','reduced organic product','a lactate molecule leaving the center reaction with all three pyruvate carbons still present','shows the reduced product of the pathway without implying that lactate is a toxic metabolic dead end'),
 ('transport network','lactate reuse routes','right-side arrows leading toward oxidative tissues and toward liver/kidney glucose-synthesis pathways','keeps lactate connected to transport, oxidation, and carbon recycling after it leaves the producing cell')],
}

PROSE={
'U3-L51':[
"The emergency door from the Prokaryotic Respiratory Membrane opens into a low, branching annex. Dr. Nia Park does not let you enter immediately. She points to a rack beside the **center** platform. Only three white **NAD⁺ cards** remain. On the platform, glycolysis is still feeding two ATP tokens, pyruvate, and blue-edged NADH cards onto a conveyor. To your **left**, the aerobic respiratory route from Journey 6 is reconstructed in miniature: an electron-transport chain ends at an oxygen basin. To your **right**, two separate corridors branch from the same problem. The upper corridor contains another ETC but no oxygen basin. The lower corridor contains no ETC at all. Nia locks your feet at the junction. “All three routes can be discussed in low-oxygen contexts,” she says, “but that does not make them the same mechanism.”",
"She activates the left reference first. NADH donates electrons to the aerobic respiratory ETC, the chain ultimately transfers them to oxygen, and oxidized NAD⁺ is recovered for continued metabolism. Then she darkens the O₂ basin. The upper-right corridor remains capable of running because its ETC ends at a different terminal electron acceptor. Nia inserts a nitrate model into one socket and a sulfate model into another. Some organisms use nitrate, sulfate, or other molecules as **non-oxygen terminal acceptors**. These examples are not an exhaustive list. The defining feature is the continued use of an electron-transport chain with a terminal acceptor other than oxygen. Only after the whole upper route is visible does Nia name it **anaerobic respiration**.",
"Now she turns to the lower-right corridor. It has no membrane chain, no series of ETC carriers, and no terminal-acceptor basin. Instead, a reduced organic product waits beside the NADH cards. This is a different solution to the carrier problem. **Respiration and fermentation across life** are characteristic energy-harvesting processes across diverse organisms, but respiration and fermentation are not synonyms. Aerobic respiration uses an ETC and oxygen as terminal electron acceptor. Anaerobic respiration still uses an ETC but finishes with a terminal acceptor other than oxygen. Fermentation takes a different route: it regenerates oxidized carrier without sending the electrons through an ETC.",
"The center rack drops to two NAD⁺ cards. That depletion becomes the reason you cannot remain at the comparison junction. Glycolysis needs NAD⁺ to accept electrons during oxidation. If the oxidized carrier is not returned, the pathway cannot simply keep filling an unlimited pile of NADH cards. Nia pulls the last spare NAD⁺ card from the rack and walks through the lower-right corridor. “Journey 6 showed how respiration can reoxidize carriers through an electron-transport chain,” she says. “Now we solve the same redox bookkeeping problem without one.” The next gate is built directly into the cytosol, and a large return arrow points from it back toward glycolysis."
],
'U3-L52':[
"You enter the **Fermentation NAD⁺ Recycling Gate** with the nearly empty carrier rack still in view behind you. The scene stays entirely cytosolic. On your **left**, blue-edged NADH cards arrive from glycolysis. In the **center**, an organic carbon molecule waits inside a redox gate. On your **right**, a white-card conveyor points straight back toward the glycolysis platform. Nia places one NADH card into the gate but leaves the ATP counter untouched. “Watch the carrier,” she says. “If you watch only the carbon product, you will miss why this pathway matters.”",
"The gate transfers reducing power from NADH to the organic molecule. The blue electron marker leaves the NADH card, and the carrier flips back to its oxidized form, **NAD⁺**. The regenerated card immediately travels right and returns to glycolysis. This process is **fermentation**: a pathway that regenerates NAD⁺ without using an electron-transport chain so glycolysis can continue when oxidative reoxidation of NADH cannot meet demand. Nia runs the gate again. NADH becomes NAD⁺; the organic acceptor becomes more reduced; the NAD⁺ card goes back to glycolysis. She points to the label above the loop: **Fermentation and NAD+ recycling**. The wording ties the pathway to the carrier problem it solves. The loop is the mechanism you are meant to remember.",
"She now covers a misleading sign above the ATP counter. Fermentation does not provide a large extra ATP harvest after glycolysis. The ATP that allows this emergency route to support the cell is the ATP glycolysis can keep producing by substrate-level phosphorylation because NAD⁺ has been regenerated. Fermentation’s critical job here is redox recycling. In the broader statement **fermentation and NAD⁺ recycling**, those two ideas belong together: reoxidizing NADH restores NAD⁺, and restored NAD⁺ permits glycolytic oxidation to continue.",
"Nia also removes an absolute sign that says FERMENTATION = NO OXYGEN PRESENT. Fermentation does not require oxygen and is especially important when oxygen-dependent oxidative reoxidation cannot meet demand. Yet some cells can run fermentation even when oxygen is present, particularly when glycolytic flux exceeds the rate at which other pathways can reoxidize NADH. Oxygen availability therefore influences pathway use, but the mechanistic definition of fermentation is not “a cell with zero oxygen.” The returned NAD⁺ cards refill the rack, and two exit lights come on. One is marked ETHANOL + CO₂. The other is marked LACTATE. The carrier problem is shared; the carbon products will now diverge."
],
'U3-L53':[
"The first exit opens into the **Alcohol Fermentation Vat**, a warm stainless-steel bay with three fixed stations. On your **left**, three-carbon pyruvate arrives from glycolysis and stops beneath a carbon-counting arch. In the **center**, a smaller two-carbon container is labeled acetaldehyde. On your **right**, an ethanol outlet stands beside a white NAD⁺ return slot. Nia keeps the NAD⁺ rack mounted above all three stations so you never forget why the sequence exists. “This branch changes carbon twice,” she says. “Only the second change directly returns the carrier.”",
"Pyruvate enters the left station with all three carbons visible. One carbon leaves through a dedicated CO₂ vent. The remaining two-carbon molecule moves into the center vat. That intermediate is **acetaldehyde**. The pathway has therefore not jumped directly from pyruvate to ethanol: pyruvate is first decarboxylated, releasing CO₂ and producing acetaldehyde. Nia freezes the vat long enough for you to count the carbon atoms. The carbon leaving as CO₂ is physically separate from the two carbons continuing toward ethanol.",
"A blue-edged NADH card then docks beside acetaldehyde. The electron marker moves from NADH onto the organic intermediate. Acetaldehyde is reduced to ethanol, while NADH is oxidized back to NAD⁺. The white NAD⁺ card immediately rises to the shared return rail. Nia finally names the complete sequence **alcohol fermentation**: pyruvate is converted to ethanol and CO₂ while NADH is oxidized to regenerate NAD⁺. The ethanol product and the returned carrier leave by separate outlets so you cannot mistake the product itself for the regenerated electron carrier. The ATP display still does not jump upward during these two fermentation steps. Their immediate redox payoff is the regenerated NAD⁺ that lets glycolysis continue producing its own substrate-level ATP.",
"Nia opens a small observation window showing yeast cells carrying out the same redox logic, then closes it before the example can become the definition. The essential pathway remains on the three stations in front of you: **pyruvate decarboxylation → acetaldehyde → ethanol**, with NAD⁺ regenerated during reduction of acetaldehyde. The NAD⁺ rack is healthy again, but the adjacent branch has no CO₂ vent and no acetaldehyde vat. Nia points through the next door. “Same carrier problem. Different carbon route.”"
],
'U3-L54':[
"The final door opens onto the **Lactate Fermentation Track**. Its geometry deliberately contrasts with the alcohol vat. On your **left**, pyruvate enters beside NADH. There is no carbon-removal arch and no CO₂ chute. In the **center**, one direct reaction chamber connects pyruvate to lactate. On your **right**, lactate does not fall into a waste bin. Instead, transport arrows split toward oxidative tissues and toward liver and kidney pathways. Nia hangs the same NAD⁺ rack above the center chamber. “If this scene ends with lactate labeled poison,” she says, “we have taught physiology from an obsolete cartoon.”",
"The reaction begins. NADH donates reducing power directly to pyruvate. The three-carbon pyruvate becomes three-carbon lactate, and NADH returns to its oxidized form, NAD⁺. This is **lactate formation** in lactate-producing fermentation: pyruvate is reduced by NADH to lactate while NAD⁺ is regenerated. Unlike alcohol fermentation, this step does not first remove a carbon as CO₂ and does not pass through acetaldehyde. The two pathways therefore solve the same NAD⁺-recycling problem with different carbon products and different reaction sequences.",
"Nia then sends the scene into a human skeletal-muscle model under high glycolytic demand. Lactate production rises even though a small oxygen indicator is still on. That matters. Human skeletal muscle can produce lactate during high glycolytic flux even when oxygen is present. Lactate itself is not the cause of the acute burning sensation during intense exercise, and it is not the cause of delayed-onset muscle soreness. Nia peels both labels off an old warning poster and leaves the poster blank. The point is not that oxygen never matters; the point is that “lactate means no oxygen” and “lactate poisons muscle” are both too crude to describe the physiology.",
"The right-side transport network now activates. Some lactate travels to tissues that can oxidize it and use its carbon as fuel. Another route carries lactate toward liver and kidney, where its carbon can contribute to glucose synthesis. This broader **lactate shuttle and Cori-cycle connection** prevents the product from being remembered as a dead end. Lactate is a transportable metabolic intermediate whose carbon can be reused. The exact tissue traffic depends on physiological conditions, but the molecule remains part of metabolism after it leaves the producing cell.",
"Nia returns the final white NAD⁺ card to the rack. All three route lights from the entrance junction are now visible through the annex glass. One route used oxygen at the end of an ETC. Another used an ETC with a different terminal electron acceptor. Fermentation used no ETC for NAD⁺ regeneration and could finish with ethanol or lactate depending on the pathway. The unit’s final accounting board closes around one durable idea: cells are metabolically flexible, but mechanisms still matter. Different pathways can solve a shared redox constraint without becoming the same pathway. Nia shuts her tablet. The NAD⁺ rack is full, glycolysis continues, and the Cellular Energetics unit finally has no unresolved emergency door."
]
}

CHECKPOINTS={
 'U3-L52':{
   'object_id':'U3-K-054',
   'prompt':'Why must fermentation regenerate NAD⁺?',
   'answer':'So glycolysis can continue oxidizing substrate and producing ATP when the available NAD⁺ pool would otherwise become depleted.',
   'hint':'Picture the nearly empty NAD⁺ rack. NADH enters the center redox gate, an organic molecule accepts its reducing power, and a white NAD⁺ card returns to the glycolysis platform.'
 }
}

TERM_IMAGES={
'U3-K-041':'the three-route junction where aerobic respiration, anaerobic respiration, and fermentation remain visibly distinct while sharing the need to harvest energy',
'U3-K-167':'the upper-right ETC route ending at a non-oxygen terminal acceptor rather than the oxygen basin',
'U3-K-168':'the nitrate, sulfate, and open “other acceptor” sockets at the end of the anaerobic respiratory ETC',
'U3-K-054':'the nearly empty NAD⁺ rack refilling as white cards return from the fermentation gate to glycolysis',
'U3-K-169':'the cytosolic redox gate where NADH transfers reducing power to an organic molecule without an ETC',
'U3-K-170':'the oxygen sign that Nia removes because fermentation can occur without oxygen yet is not defined simply by total oxygen absence',
'U3-K-171':'the three-station alcohol route: pyruvate loses CO₂, acetaldehyde forms, then NADH reduction produces ethanol and NAD⁺',
'U3-K-172':'the two-carbon acetaldehyde vat positioned between pyruvate decarboxylation and ethanol formation',
'U3-K-173':'the direct three-carbon pyruvate-to-lactate reaction returning NADH to NAD⁺ without a CO₂ vent',
'U3-K-174':'the exercising muscle display producing lactate while its oxygen indicator remains on, beside the removed “burn” and “soreness” labels',
'U3-K-175':'the lactate transport network splitting toward oxidative tissues and toward liver/kidney carbon recycling into glucose synthesis',
}

def scene(locus_id,idx):
    b=B[locus_id]
    terms=b['term_introductions']
    zones=[{'position':pos,'label':lab,'symbol':sym,'description':desc} for pos,lab,sym,desc in ZONE_COPY[locus_id]]
    cast=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    for name,kind,visual,job in CAST[locus_id]: cast.append({'name':name,'kind':kind,'visual':visual,'job':job})
    paras=PROSE[locus_id]
    beats=[]; snapshot=[]
    for t in terms:
        kid=t['knowledge_id']; image=TERM_IMAGES[kid]
        beats.append({'object_id':kid,'term':t['canonical_term'],'story':image,'science':t['canonical_science'],'exact_name':t['exact_name_recall'],'hint':image})
        snapshot.append({'term':t['canonical_term'],'meaning':t['canonical_science'],'image':image})
    cp=CHECKPOINTS.get(locus_id)
    nxt=route[idx+1]['locus'] if idx+1<len(route) else None
    return {
      'scene_index':idx,'locus':route[idx]['locus'],'title':b['scene_title'],
      'scene_kicker':{
       'U3-L51':'Three pathways can solve energy-harvesting problems under different conditions, but ETC use and terminal electron acceptors keep respiration distinct from fermentation.',
       'U3-L52':'The emergency is a carrier shortage: fermentation matters because it returns oxidized NAD⁺ to glycolysis without using an electron-transport chain.',
       'U3-L53':'Alcohol fermentation solves NAD⁺ recycling through a two-step carbon route that releases CO₂, forms acetaldehyde, and ends with ethanol.',
       'U3-L54':'Lactate formation directly reduces pyruvate, regenerates NAD⁺, and feeds a transportable metabolite into continued physiology rather than a toxic dead end.'
      }[locus_id],
      'location_description':b['exact_location']+' — '+b['micro_anchor']+'.',
      'scene_layout':{'orientation':b['orientation_sentence'],'zones':zones},'cast':cast,
      'story_open':paras[0],'story_paragraphs':paras,'story_close':paras[-1],
      'object_ids':b['knowledge_ids'],'story_beats':beats,'memory_snapshot':snapshot,
      'checkpoint':bool(cp),'checkpoint_object_id':cp['object_id'] if cp else None,
      'checkpoint_prompt':cp['prompt'] if cp else '', 'checkpoint_answer':cp['answer'] if cp else '', 'checkpoint_hint':cp['hint'] if cp else '',
      'next_locus':nxt,'misconception_guards':b['misconception_guards'],'required_visual':b['visual_spec']['must_show'],'carry_forward':b['carry_forward']
    }

scenes=[scene(lid,i) for i,lid in enumerate(['U3-L51','U3-L52','U3-L53','U3-L54'])]
journey={
 'schema':'memory-palace-v2-unit3-f4g-story-1.0','unit_id':'unit-3','palace_id':'U3-J7','journey_id':'U3-J7',
 'palace_name':'Alternative Energy Annex','story_title':'The NAD⁺ Cards That Would Not Return',
 'tagline':'Follow one shrinking pool of NAD⁺ through aerobic and anaerobic respiratory comparisons, fermentation redox recycling, alcohol fermentation, and lactate metabolism until glycolysis can run again.',
 'guide':GUIDE,
 'premise':'The oxygen-terminal emergency door from Journey 6 opens onto an annex where glycolysis is still running but its finite pool of oxidized NAD⁺ is nearly exhausted. The learner must determine which alternative routes use an ETC and which regenerate NAD⁺ through fermentation.',
 'mission':'Separate aerobic respiration, anaerobic respiration, and fermentation mechanistically, then follow NAD⁺ regeneration through alcohol and lactate pathways while keeping their carbon products and human physiological meaning distinct.',
 'finale':'The annex closes only after the NAD⁺ rack has been refilled by clearly distinguished mechanisms: respiration reoxidizes carriers through electron-transport chains with different terminal acceptors, while fermentation regenerates NAD⁺ without an ETC and can produce ethanol or lactate. Lactate remains a transportable, reusable metabolite rather than a metabolic poison.',
 'estimated_minutes':13,'scene_count':4,'checkpoint_count':1,
 'learner_rule':'Keep the NAD⁺ card rack in view. Ask how NADH is being oxidized back to NAD⁺ in each route, and use ETC presence plus terminal electron acceptor to distinguish respiration from fermentation. Quick Recall is optional on the first pass.',
 'route_orientation':'The Alternative Energy Annex is a four-station branch-and-return route. Begin at the three-route respiration junction, move into the cytosolic NAD⁺ recycling gate, then compare alcohol and lactate fermentation in neighboring bays. The nearly empty NAD⁺ rack follows you through every station and returns full at the final track.',
 'route':route,'scenes':scenes,'student_release':'PILOT_PREVIEW_F4G','narrative_standard':'V2-NARRATIVE-3.0-U3-F4G'
}
(U3/'journeys'/'U3-J7.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

js=[json.loads((U3/'journeys'/f'U3-J{i}.json').read_text(encoding='utf-8')) for i in range(1,8)]
def card(j): return {k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
registry={'schema':'memory-palace-v2-unit3-f4g-registry-1.0','course_id':'ap-biology','unit_id':'unit-3','unit_title':'Cellular Energetics','narrative_standard':'V2-NARRATIVE-3.0-U3-F4G','journey_count':7,'scene_count':sum(x['scene_count'] for x in js),'checkpoint_count':sum(x['checkpoint_count'] for x in js),'guided_journeys':[card(x) for x in js]}
(U3/'journeys-f4g.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U3/'status-f4f.json').read_text(encoding='utf-8'))
status.update({'status':'F4G_JOURNEY7_POLISHED_PREVIEW','pipeline_status':'POLISHED_NARRATIVE_JOURNEYS_1_7_F4G','student_release':False,'preview_release':True,'journey_count':7,'scene_count':registry['scene_count'],'polished_journeys':7,'polished_scenes':registry['scene_count'],'polished_checkpoint_count':registry['checkpoint_count'],'narrative_story_files':7,'next_required_output':'F5 Unit 3 release audit, delayed-review plan, and application/challenge integration after all seven polished narratives pass regression'})
(U3/'status-f4g.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(U3/'status.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; c=json.loads(cp.read_text(encoding='utf-8'))
for u in c['units']:
    if u['unit_id']=='unit-3':
        u.update({'status':'F4G_JOURNEY7_POLISHED_PREVIEW','journey_count':7,'scene_count':registry['scene_count'],'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEYS1_7_POLISHED_F4G','polished_journeys':7,'polished_scenes':registry['scene_count'],'student_release':False})
cp.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

bc=ROOT/'backend'/'content.py'; bs=bc.read_text(encoding='utf-8')
old='    if unit_id == "unit-3":\n        path=UNIT3_DIR / "journeys-f4f.json"'
new='    if unit_id == "unit-3":\n        path=UNIT3_DIR / "journeys-f4g.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4f.json"'
if old in bs: bs=bs.replace(old,new)
elif 'journeys-f4g.json' not in bs: raise RuntimeError('Could not patch Unit 3 journey registry preference to F4G')
bc.write_text(bs,encoding='utf-8')

mainp=ROOT/'backend'/'main.py'; ms=mainp.read_text(encoding='utf-8')
ms=ms.replace('0.17.0-u3-f4f','0.18.0-u3-f4g').replace('v2-apbio-0.17.0-u3-f4f','v2-apbio-0.18.0-u3-f4g')
mainp.write_text(ms,encoding='utf-8')

# Home status label.
home=ROOT/'frontend'/'js'/'views'/'home.js'; hs=home.read_text(encoding='utf-8')
if "includes('F4G')" not in hs:
    hs=hs.replace("if(String(u.status||'').includes('F4F'))return 'Journeys 1–6 narrative preview';", "if(String(u.status||'').includes('F4G'))return 'Journeys 1–7 narrative preview';\n if(String(u.status||'').includes('F4F'))return 'Journeys 1–6 narrative preview';")
home.write_text(hs,encoding='utf-8')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
files=['journeys/U3-J7.json','journeys-f4g.json','status-f4g.json']
lock={'schema':'memory-palace-v2-unit3-f4g-content-lock-1.0','unit_id':'unit-3','stage':'F4G','student_release':False,'files':{f:sha(U3/f) for f in files}}
(U3/'content-lock-f4g.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit3-f4g-release-manifest-1.0','unit_id':'unit-3','stage':'F4G','student_release':False,'preview_release':True,'polished_journeys':7,'polished_scenes':registry['scene_count'],'journey_7_records':sum(len(s['object_ids']) for s in scenes),'journey_7_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'all_unit3_narratives_polished':True,'next_stage':'F5_UNIT3_RELEASE_AUDIT_REVIEW_AND_CHALLENGE_INTEGRATION'}
(U3/'f4g-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Built Unit 3 F4G:',len(scenes),'scenes',sum(len(s['object_ids']) for s in scenes),'knowledge records',sum(bool(s['checkpoint']) for s in scenes),'checkpoints')
