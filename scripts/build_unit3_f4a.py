from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content'/'ap-biology'/'unit-3'
briefs=json.loads((U3/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
jbriefs=json.loads((U3/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
B={s['locus_id']:s for s in briefs if s['journey_id']=='U3-J1'}
J1=next(j for j in jbriefs if j['journey_id']=='U3-J1')

GUIDE={
 'name':'Dr. Nia Park',
 'role':'cellular-energetics investigator',
 'visual':'navy field jacket, clear safety glasses, and a compact tablet showing reaction-energy and molecular models',
 'story_job':'Nia keeps the workshop geography fixed, asks you to predict the molecular consequence, and names scientific terms only after the defining action is visible.'
}

route=[
 {'scene_index':0,'locus':'Catalyst Energy Ramp','short':'Energy Ramp','floor':'Workshop entrance','symbol':'∩'},
 {'scene_index':1,'locus':'Active-Site Dock','short':'Active-Site Dock','floor':'Molecular docking bay','symbol':'⊂'},
 {'scene_index':2,'locus':'Catalytic Turnover Bench','short':'Turnover Bench','floor':'Reaction floor','symbol':'↻'},
]

ZONE_COPY={
'U3-L01':[
 ('left','Uncatalyzed energy hill','∩','A conventional reaction-energy profile rises to a tall activation barrier while the amber substrate remains at the same reactant starting level.'),
 ('center','Enzyme-catalyzed route','⌒','A second energy profile begins at the same reactant level and ends at the same product level, but its activation barrier is visibly lower.'),
 ('right','Product-side exit','→','The same product state waits at the right end of both profiles, making it clear that catalysis changes the barrier rather than the reaction endpoints.')],
'U3-L02':[
 ('left','Free-substrate approach lane','◆','The same amber substrate approaches beside several decoy molecules whose shapes or chemical patches do not match the enzyme pocket.'),
 ('center','Active-site docking pocket','⊂','A conventional globular enzyme model presents one active-site pocket with matching shape and chemical properties, then shifts slightly around the bound substrate.'),
 ('right','Enzyme-substrate complex display','◎','The substrate is held temporarily inside the adjusted active site as one bound enzyme-substrate complex before product chemistry proceeds.')],
'U3-L03':[
 ('left','Fresh substrate queue','◆','A new amber substrate waits at the left while the previous reaction products have already moved toward the release side.'),
 ('center','Catalytic turnover bench','↻','The same enzyme completes catalysis, releases products, and returns its active site to a usable state without being consumed by the reaction.'),
 ('right','Product release and enzyme reset','⇢','Products separate to the right while the enzyme remains available for another catalytic cycle, beside enzyme-name examples that show the -ase pattern and its exceptions.')],
}

CAST={
'U3-L01':[
 ('reaction-energy profiles','scientific model','two side-by-side energy-versus-reaction-progress curves with identical reactant and product levels','compare the activation barrier for the same reaction with and without enzyme catalysis'),
 ('amber substrate','continuity object','one amber molecular model held at the reactant side of both energy profiles','keep the reactant identity constant while the reaction pathway is compared'),
 ('enzyme station','scientific part','a folded protein catalyst shown beside the lower central energy route','provide the biological catalyst whose presence lowers the activation-energy barrier')],
'U3-L02':[
 ('amber substrate','continuity object','the same amber molecular model with a distinctive outline and visible polar and charged surface patches','serve as the reactant whose compatibility with the active site is tested'),
 ('enzyme active site','scientific part','a pocket in a conventional folded protein model with complementary geometry and chemical groups','bind a compatible substrate and create the local environment for catalysis'),
 ('decoy molecules','comparison models','nearby molecular models with mismatched shapes or chemical surface properties','show that binding depends on more than a vague idea of molecules simply touching')],
'U3-L03':[
 ('reusable enzyme','scientific part','the same folded protein and active-site pocket seen in the docking bay','complete a catalytic cycle and remain available for repeated use'),
 ('reaction products','scientific output','separated product molecules leaving the right side of the bench','show the products leaving after catalysis'),
 ('fresh substrate','continuity object','a second amber substrate arriving from the left immediately after product release','demonstrate that the enzyme can enter another catalytic cycle')],
}

NARR={
'U3-L01':{
 'title':'The Reaction That Would Not Climb',
 'kicker':'The reactants and products are already in place. The problem is the energy barrier between them.',
 'paragraphs':[
  "The doors of the **Enzyme Catalysis Workshop** open onto a narrow platform with two reaction tracks running from left to right. You stop at a brass rail bolted to the floor. On your **left**, the first track rises into a steep black hill before dropping toward a product platform on the far right. Directly **ahead**, a second track starts at exactly the same height and ends at exactly the same product platform, yet its hill is much lower. A single amber molecular model rests at the reactant end. Nia places a second identical amber model beside it. ‘Same reactants. Same products,’ she says. ‘Watch the barrier.’",
  "She releases the model on the left track. A meter above the hill climbs sharply as the reaction model approaches the crest, then flashes red before the model can pass. Nia freezes it near the top. ‘A reaction can be thermodynamically possible and still require an initial input before its reactants reach a transition state.’ She taps the tall crest. That initial barrier is the **activation energy**. The hill is an energy-profile model, so you are not meant to picture a molecule literally hiking over a physical mountain. Its height represents how much energy the reacting system must acquire to reach the transition state.",
  "Nia resets the amber model and activates the center track. A folded protein appears beside the lower route. The second model now reaches a much smaller crest and continues toward the same product platform. Nothing about the reactant label changes. Nothing about the product platform changes. The visible difference is the lower barrier. ‘This protein is an **enzyme**, a biological catalyst,’ Nia says. ‘Enzymes facilitate reactions by lowering **activation energy**.’ The center display overlays the two curves so the tall uncatalyzed peak and the lower enzyme-catalyzed peak can be compared without moving the starting or ending levels.",
  "A bank of workshop machines begins to wake as more amber models pass through the lower route. Nia turns the enzyme station down and the downstream machines slow. She restores activity and the pathway accelerates again. The workshop is showing a broader biological consequence. Enzyme structure and function help regulate biological processes because changing enzyme activity changes the rates at which many cellular reactions proceed. The enzyme does not supply a new set of products. It changes how readily the existing reaction pathway can proceed by lowering the barrier that must be crossed.",
  "The first amber substrate reaches the product-side exit, but Nia catches the second before it follows. ‘You have seen what the catalyst changes,’ she says. ‘Now we need to see how a protein can act on one reactant at molecular scale.’ A door opens beside the center track. Through it, you can see a large protein model with a pocket cut into its surface. You carry the amber molecule into the **Active-Site Dock**."
 ],
 'close':'You leave the energy profiles fixed behind you and carry the same amber reactant toward the enzyme pocket that must recognize and bind it.',
 'images':{
  'Enzyme regulation role':'a pathway-rate panel slowing when enzyme activity is reduced and accelerating when activity is restored',
  'Enzymes are protein catalysts':'a folded protein positioned beside the lower reaction-energy route',
  'Activation-energy reduction':'two identical reaction endpoints connected by a tall uncatalyzed peak and a lower enzyme-catalyzed peak',
  'Activation energy':'the height from the reactant energy level to the crest of the reaction-energy barrier'
 }
},
'U3-L02':{
 'title':'The Pocket That Adjusts Around Its Substrate',
 'kicker':'A substrate has reached the enzyme, yet binding still depends on the geometry and chemistry of one precise region.',
 'paragraphs':[
  "You enter the **Active-Site Dock** and stop at a yellow floor line. The room is much smaller than the energy ramp. On your **left**, the amber molecule sits in an approach lane beside three decoys. One is too bulky for the pocket ahead. Another has the right general outline but carries mismatched charged and polar patches. Directly **ahead**, the enzyme fills the center bay as a folded protein with one recessed pocket on its surface. On your **right**, an empty glass display is labeled BOUND STATE. The three zones stay fixed while Nia lifts the amber molecule with a magnetic molecular arm.",
  "‘The amber molecule is the **substrate**,’ Nia says after you have seen it positioned as the reactant the enzyme will act on. She first guides the bulky decoy toward the pocket. It cannot settle into the site. The second decoy approaches more closely, but mismatched chemical groups prevent a stable interaction. Then the amber substrate moves forward. Its overall shape can enter the pocket, and its chemical features meet compatible groups inside. For an enzyme-mediated reaction to proceed, substrate shape and charge, along with other chemical properties, must be compatible with this local region of the enzyme.",
  "Nia touches the rim of the pocket. ‘This region is the **active site**.’ It is the part of the enzyme where a compatible substrate binds and catalysis occurs. The name refers to a region of the folded protein, not a separate object attached to it. As the amber substrate settles, the display zooms in on temporary interactions between the substrate and amino acid side chains lining the site. The fit is specific, yet the enzyme has not remained perfectly rigid.",
  "The pocket closes slightly around the substrate. One side chain rotates inward, another shifts position, and the catalytic groups become better aligned with bonds in the substrate. Nia freezes the movement halfway. This binding-triggered conformational adjustment is **induced fit**. The substrate does not force the enzyme into an unrelated shape. Binding stabilizes a conformation that improves catalytic interactions within the active site. The center model now makes specificity and flexibility visible at the same time.",
  "When the adjustment is complete, the entire bound pair is copied into the glass case on your **right**. The enzyme remains the large protein. The amber substrate is still identifiable inside its active site. Together, this temporary bound state is the **enzyme-substrate complex**. Nia leaves the complex frozen before any product appears. ‘Keep these pieces separate in your mind,’ she says. ‘The substrate is the reactant. The active site is a region of the enzyme. The enzyme-substrate complex exists when the compatible substrate is bound there.’ The right-hand case then slides open into the next room, carrying the bound complex intact."
 ],
 'close':'The bound enzyme-substrate complex moves forward exactly as you last saw it, ready for chemistry, product release, and one final test of whether the enzyme itself survives the cycle.',
 'images':{
  'Active-site compatibility':'a compatible amber substrate settling into a pocket while mismatched decoys fail because of shape or chemical properties',
  'Enzyme-substrate complex':'the folded enzyme and amber substrate frozen together as one temporary bound complex',
  'Substrate':'the amber reactant molecule approaching the enzyme before binding',
  'Active site':'the specific recessed region of the folded enzyme where compatible substrate binds and catalysis occurs',
  'Induced fit':'the enzyme pocket changing conformation around the bound substrate to improve catalytic interactions'
 }
},
'U3-L03':{
 'title':'The Enzyme That Returns to Work',
 'kicker':'The products can leave only if the catalyst finishes the cycle without being used up.',
 'paragraphs':[
  "The glass case rolls into the **Catalytic Turnover Bench** and locks into the center of a long reaction table. On your **left**, a fresh amber substrate waits in a short queue. Directly **ahead**, the enzyme-substrate complex from the docking bay sits enlarged under white light. On your **right**, two product channels lead away from an empty release platform. Nia closes the door behind you so the three positions cannot be confused. ‘We have watched binding,’ she says. ‘Now keep your eyes on the enzyme through the entire catalytic cycle.’",
  "The reaction resumes. Within the active site, bonds in the substrate are rearranged and the chemical state changes. The amber substrate is no longer the same reactant that entered the pocket. Two product models separate within the site, then leave through the right-hand channels. As the products move away, the enzyme relaxes from its bound conformation. The protein remains at the center bench. It has participated in the reaction without becoming one of the products and without being consumed as a reactant.",
  "Nia immediately sends the fresh amber substrate from the **left** toward the same enzyme. The active site accepts it, adjusts again, and begins a second cycle. A counter above the bench changes from 1 to 2, then 3 as the demonstration repeats. This is why enzymes can function as **reusable catalysts**. A single enzyme molecule can participate in repeated reaction cycles as substrates bind, chemistry occurs, products leave, and the enzyme becomes available again. The workshop would be impossible to sustain if every catalytic event destroyed its enzyme.",
  "A small naming board lights beside the release platform. Several common enzyme names appear, including lactase and amylase, with **-ase** highlighted. Then two additional names, pepsin and trypsin, appear beneath them. Nia leaves all four visible. ‘Many enzyme names end in **-ase**,’ she says. ‘That is a useful naming convention, not a universal rule.’ The examples stay side by side so the pattern is memorable without turning it into an absolute shortcut.",
  "The workshop finally runs smoothly. On the wall behind you, the three rooms compress into one route map. First, the same reaction gained a lower activation-energy pathway. Next, a compatible substrate bound at an active site and induced a conformational adjustment. Finally, products left and the enzyme returned to service. Nia points to a bank of control dials beyond the exit. Temperature, pH, substrate concentration, inhibitors, and regulatory molecules are all waiting there. ‘Now that you know what an enzyme actually does,’ she says, ‘we can investigate what changes its activity.’ The doors to the **Enzyme Regulation Control Wing** unlock."
 ],
 'close':'The catalyst is still intact, the substrate-to-product cycle is complete, and the next journey can now ask how cells and environments change the rate of that same mechanism.',
 'images':{
  'Enzymes are reusable catalysts':'products leave while the same enzyme resets and accepts a fresh substrate for another cycle',
  'Enzyme naming convention':'enzyme names ending in -ase displayed beside pepsin and trypsin as visible exceptions to the naming pattern'
 }
}
}

TERM_OVERRIDES={
 'Enzyme regulation role':'Enzyme regulation role',
 'Enzymes are protein catalysts':'Enzyme',
 'Activation-energy reduction':'Activation-energy reduction',
 'Active-site compatibility':'Active-site compatibility',
 'Enzyme-substrate complex':'Enzyme-substrate complex',
 'Enzymes are reusable catalysts':'Reusable enzyme catalyst',
 'Enzyme naming convention':'Enzyme naming convention',
}

CHECKPOINT_HINTS={
 'U3-L01':'Picture the two reaction-energy profiles. Their reactant and product levels match, while the center enzyme-controlled route has the lower peak.',
 'U3-L02':'Picture the amber substrate entering the center pocket. Its shape and chemical surface features must match the active-site environment well enough to bind.',
}

scenes=[]
for idx,lid in enumerate(J1['route']):
    b=B[lid]; n=NARR[lid]
    zones=[{'position':pos,'label':lab,'symbol':sym,'description':desc} for pos,lab,sym,desc in ZONE_COPY[lid]]
    cast=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    cast += [{'name':name,'kind':kind,'visual':visual,'job':job} for name,kind,visual,job in CAST[lid]]
    beats=[]; snaps=[]
    for t in b['term_introductions']:
        term=TERM_OVERRIDES.get(t['canonical_term'],t['canonical_term'])
        image=n['images'].get(t['canonical_term'], b['carry_forward'])
        beats.append({'object_id':t['knowledge_id'],'term':term,'story':image,'science':t['canonical_science'],'exact_name':bool(t.get('exact_name_recall')),'hint':image})
        snaps.append({'term':term,'meaning':t['canonical_science'],'image':image})
    qr=b['quick_recall']; cp=bool(qr.get('enabled'))
    scene={
      'scene_index':idx,'locus':b['scene_title'],'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['exact_location']+' — '+b['micro_anchor']+'.',
      'scene_layout':{'orientation':b['orientation_sentence'],'zones':zones},'cast':cast,
      'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':beats,'memory_snapshot':snaps,
      'checkpoint':cp,'checkpoint_object_id':b['primary_knowledge_id'],'checkpoint_prompt':qr.get('candidate_prompt','') if cp else '',
      'checkpoint_answer':qr.get('answer','') if cp else '','checkpoint_hint':CHECKPOINT_HINTS.get(lid,'') if cp else '',
      'next_locus':B[b['causal_transition']['to_locus_id']]['scene_title'] if b['causal_transition']['to_locus_id'] else None,
      'misconception_guards':b['misconception_guards'],'required_visual':b['visual_spec'],'carry_forward':b['carry_forward']
    }
    scenes.append(scene)

journey={
 'schema':'memory-palace-v2-unit3-f4a-story-1.0','unit_id':'unit-3','palace_id':'U3-J1','journey_id':'U3-J1',
 'palace_name':'Enzyme Catalysis Workshop','story_title':'The Reaction That Would Not Start',
 'tagline':'Follow one amber substrate across an energy barrier, into an active site, and through repeated catalytic cycles until enzyme action becomes a visible mechanism.',
 'guide':GUIDE,'premise':J1['premise'],'mission':J1['mission'],
 'finale':'The workshop runs again after the same reaction receives a lower activation-energy pathway, the amber substrate binds a compatible active site through induced fit, products leave, and the unchanged enzyme returns to service. The restored catalyst then unlocks the control wing where enzyme activity can be regulated.',
 'estimated_minutes':9,'scene_count':len(scenes),'checkpoint_count':sum(bool(s['checkpoint']) for s in scenes),
 'learner_rule':'Read or listen and hold the three fixed zones of each room in mind. Watch the molecular event first, then attach the scientific term. Quick Recall is optional during the first pass.',
 'route_orientation':'The Enzyme Catalysis Workshop is a three-room route. Enter at the reaction-energy ramp, carry the same amber substrate through the door into the active-site docking bay, then follow the bound enzyme-substrate complex straight into the catalytic turnover bench. Left, center, and right anchors stay fixed within every room.',
 'route':route,'scenes':scenes,'student_release':'PILOT_PREVIEW_F4A','narrative_standard':'V2-NARRATIVE-3.0-U3-F4A'
}

(U3/'journeys').mkdir(parents=True,exist_ok=True)
(U3/'journeys'/'U3-J1.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
card={k:journey[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
registry={'schema':'memory-palace-v2-unit3-f4a-registry-1.0','course_id':'ap-biology','unit_id':'unit-3','unit_title':'Cellular Energetics','narrative_standard':'V2-NARRATIVE-3.0-U3-F4A','journey_count':1,'scene_count':3,'checkpoint_count':2,'guided_journeys':[card]}
(U3/'journeys-f4a.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U3/'status-f3.json').read_text(encoding='utf-8'))
status.update({'status':'F4A_JOURNEY1_POLISHED_PREVIEW','pipeline_status':'POLISHED_NARRATIVE_PILOT_F4A','student_release':False,'preview_release':True,'journey_count':1,'scene_count':3,'polished_journeys':1,'polished_scenes':3,'polished_checkpoint_count':2,'narrative_story_files':1,'next_required_output':'F4B polished narrative for Journey 2 after F4A prose QA and developer/classroom review'})
(U3/'status-f4a.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(U3/'status.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; c=json.loads(cp.read_text(encoding='utf-8'))
for u in c['units']:
    if u['unit_id']=='unit-3':
        u.update({'status':'F4A_JOURNEY1_POLISHED_PREVIEW','journey_count':1,'scene_count':3,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEY1_POLISHED_F4A','polished_journeys':1,'polished_scenes':3,'student_release':False})
cp.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
files=['journeys/U3-J1.json','journeys-f4a.json','status-f4a.json']
lock={'schema':'memory-palace-v2-unit3-f4a-content-lock-1.0','unit_id':'unit-3','stage':'F4A','student_release':False,'files':{f:sha(U3/f) for f in files}}
(U3/'content-lock-f4a.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit3-f4a-release-manifest-1.0','unit_id':'unit-3','stage':'F4A','student_release':False,'preview_release':True,'polished_journeys':1,'polished_scenes':3,'journey_1_records':sum(len(s['object_ids']) for s in scenes),'journey_1_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'next_stage':'F4B_JOURNEY2'}
(U3/'f4a-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Built Unit 3 F4A:',len(scenes),'scenes',sum(len(s['object_ids']) for s in scenes),'knowledge records',sum(bool(s['checkpoint']) for s in scenes),'checkpoints')
