from __future__ import annotations
import json, hashlib, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content'/'ap-biology'/'unit-4'
F3=json.loads((U4/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS=json.loads((U4/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J1=next(j for j in JBRIEFS if j['journey_id']=='U4-J1')
B={b['locus_id']:b for b in F3 if b['journey_id']=='U4-J1'}

GUIDE={
 'name':'Dr. Mira Chen',
 'role':'cellular-systems investigator',
 'visual':'charcoal field jacket, clear protective glasses, and a compact white tablet holding a transparent four-field route card',
 'story_job':'Mira keeps sender, route, distance, and target visible while each communication mechanism is repaired. She names the biology after the defining action can be seen.'
}

route=[
 {'scene_index':0,'locus':'Communication Compass','short':'Compass','floor':'Exchange rotunda','symbol':'◎'},
 {'scene_index':1,'locus':'Contact Junction Gallery','short':'Contact','floor':'Contact wing','symbol':'⇄'},
 {'scene_index':2,'locus':'Local Signal Courtyard','short':'Local','floor':'Courtyard','symbol':'◌'},
 {'scene_index':3,'locus':'Synaptic Dock','short':'Synapse','floor':'Neural dock','symbol':'···'},
 {'scene_index':4,'locus':'Endocrine Transit Hub','short':'Endocrine','floor':'Circulation hub','symbol':'↝'},
 {'scene_index':5,'locus':'Plant Hormone Route','short':'Plant route','floor':'Glasshouse wing','symbol':'🌿'},
]

ZONE_COPY={
'U4-L01':[
 ('left','Direct-contact lane','⇄','Two neighboring cells can be moved together until their membranes touch. No long-range transport route passes through this lane.'),
 ('center','Communication-scale map','◎','A floor-sized map holds the same sender and target while their separation changes from touching, to nearby, to body-scale distance.'),
 ('right','Distance-signaling lane','↝','A long illuminated route remains dark until a chemical message is given a transport path to a distant target.')],
'U4-L02':[
 ('left','Animal gap-junction channel','⊙','Two animal-cell membranes meet across a narrow intercellular channel fitted with a size gate that admits ions and selected small signaling molecules.'),
 ('center','Surface-recognition station','▥','An antigen-presenting cell and a T cell meet face to face so complementary surface molecules can interact directly without a channel between their cytoplasms.'),
 ('right','Plant plasmodesmata wall','║','A thick plant cell wall is crossed by membrane-lined channels that connect neighboring cell cytoplasms while preserving regulated transport.')],
'U4-L03':[
 ('left','Signal-emitting cell','●','A nearby signaling cell releases a small set of chemical messengers from one side of the courtyard.'),
 ('center','Local diffusion radius','◌','Concentric floor rings mark how a secreted local regulator spreads only through the nearby extracellular space.'),
 ('right','Nearby target-cell row','▣','Several cells sit inside the local radius, but only the cell carrying the appropriate receptor and downstream machinery changes state.')],
'U4-L04':[
 ('left','Presynaptic terminal','◉','The end of a neuron contains vesicles filled with neurotransmitter and faces a separate target cell across a microscopic gap.'),
 ('center','Synaptic cleft','···','A narrow extracellular space separates the neuronal terminal from the target membrane and becomes the route across which released neurotransmitter diffuses.'),
 ('right','Postsynaptic target membrane','▥','Receptors on the target membrane remain inactive until neurotransmitter reaches and binds them.')],
'U4-L05':[
 ('left','Endocrine release platform','●','A specialized endocrine cell releases hormone molecules into a vessel instead of keeping the message within a local courtyard.'),
 ('center','Bloodstream transit rail','≈','A long transparent vessel carries hormone past many cells and tissues over a body-scale distance.'),
 ('right','Distant receptor-bearing target','▣','A distant target cell responds only when it carries the appropriate receptor. An insulin example can be overlaid without redefining the whole hormone category.')],
'U4-L06':[
 ('left','Plant source tissue','🌱','A cutaway plant organ releases a hormone into neighboring tissue at the start of the plant route.'),
 ('center','Tissue and vascular pathways','║','The plant cross-section shows hormone movement through tissues and vascular pathways toward another region of the plant.'),
 ('right','Target tissue and ethylene chamber','◌','Responsive plant tissue sits beside a separate clear air chamber where volatile ethylene can diffuse through air to another responsive tissue.')],
}

NARR={
'U4-L01':{
 'title':'The Exchange With No Addresses',
 'kicker':'Every message is marked SIGNAL, so none of the routes knows how far it is supposed to travel.',
 'paragraphs':[
  "The doors of the **Cellular Communications Exchange** slide apart, and you step onto a circular control floor bright with warning lights. The room is easy to map before anything moves. On your **left**, a short lane ends at two cell models that can be pushed until their membranes touch. Directly **ahead**, a floor-sized communication map holds one glowing sender cell and one dark target cell. On your **right**, a long illuminated track disappears through a wall toward a target station far beyond the room. Above all three routes, the same red word flashes again and again, SIGNAL.",
  "Dr. Mira Chen is waiting beside the center map in a charcoal field jacket, clear protective glasses catching the warning lights. She lifts a transparent card divided into four blank fields labeled sender, messenger or contact, route or distance, and target. The exchange has been failing because every message has been treated as if it traveled the same way. Growth instructions reach the wrong tissue. Nearby repair signals vanish into the long-distance line. Messages meant for touching cells are being sent through transport routes they never needed. Mira sets the card on the edge of the map. \"We repair the routes by changing one thing at a time,\" she says. \"Watch how the same two cells communicate when their distance changes.\"",
  "She brings the sender and target together until the two membranes touch. The left-hand contact lane lights immediately. No distant transport line activates. Mira moves the same cells apart by a short distance across the center map. Now the contact light dies, and a small local chemical field appears around the sender. She moves the target to the far end of the map. The local field no longer reaches it. The right-hand track stays dark until a long-range chemical route is switched on. The contrast gives the first organizing idea its shape. Cells use **direct or distance communication**. Some messages depend on contact, while others are carried by chemical signaling across short or long distances.",
  "The map around you expands into a faint outline of a multicellular organism. Different tissues pulse in different rhythms, yet their activity has to remain coordinated. Mira points from a growing tissue to a repair zone, then to a distant organ. **Cell communication** coordinates survival, growth, development, and other functions that require cells in a multicellular organism to act as parts of one system. A message has meaning only when the appropriate target receives it through the appropriate route. The exchange is therefore more than a collection of signal molecules. It is a routing problem involving sender, path, distance, and target.",
  "Mira fills the first line of the route card, then turns it toward you. CONTACT, LOCAL, and DISTANT now occupy separate rows. One row is still incomplete. The contact route tells you that two cells can communicate without sending a messenger across the body, but the map does not yet show what direct contact physically looks like. The left lane unlocks with a metallic click. Through the opening you can see an animal-cell channel on one wall, a thick plant cell wall on the other, and two immune-cell surfaces waiting face to face in the center."
 ],
 'close':'You leave the compass with the three distance scales fixed in your mind and follow the direct-contact lane into the Contact Junction Gallery.',
},
'U4-L02':{
 'title':'Three Ways to Communicate While Touching',
 'kicker':'Direct contact can use an intercellular channel or a precise meeting between surface molecules.',
 'paragraphs':[
  "The **Contact Junction Gallery** is a long rectangular room with three displays that never trade places. On your **left**, two animal cells press their plasma membranes close together around a narrow channel. Straight **ahead**, an antigen-presenting cell faces a T cell across a small open platform, their surfaces almost touching. On your **right**, two plant cells are separated by a thick cell wall pierced by slender membrane-lined tunnels. Mira clips the transparent route card to a rail at the entrance and marks the distance field TOUCHING.",
  "She begins on the left. A gate opens through the paired animal membranes, creating a direct passage from one cell to the next. Tiny ions and small signaling molecules move through. A larger cargo sphere reaches the entrance and stops. Mira deliberately leaves it there so the image stays clear. The connection is a **gap junction**, an intercellular channel in animals that permits regulated passage of ions and selected small signaling molecules between adjacent cells. Direct connection does not mean unrestricted flow. The size and state of the channel constrain what can pass.",
  "Across the room, the plant wall glows. The right-hand tunnels run through the rigid cell wall and are lined by plasma membrane, linking the cytoplasm of one plant cell with that of its neighbor. Small transported material moves through a tunnel while another gate narrows. These channels are **plasmodesmata**. Their structure differs from an animal gap junction, even though both create direct routes between neighboring cells. The thick plant wall, the membrane-lined channel, and the regulated movement belong together in one mental picture. Mira writes PLANT CHANNEL beside plasmodesmata and ANIMAL CHANNEL beside gap junction on the route card.",
  "The center platform now activates. No channel opens between the two immune cells. The antigen-presenting cell displays molecules on its surface, and complementary molecules on the T cell meet them directly. The interaction itself carries the information. This is another form of **direct contact**, where cell-surface molecules interact between touching cells. The antigen-presenting cell and T cell provide a concrete example of contact-dependent communication. Their cytoplasms never need to merge, and a gap junction does not appear between them.",
  "Mira steps back so all three displays remain visible at once. Left is the animal gap junction, center is surface recognition, right is plant plasmodesmata. She taps the route card. Direct-contact signaling includes communication through cell junctions and communication through direct interactions between cell-surface molecules. The key relationship is physical contact, while the structures that accomplish it can differ.",
  "A green check finally appears over the CONTACT row. Then another warning lights beneath it. NEARBY, NOT TOUCHING. Mira points to a side door opening onto an outdoor courtyard. A single signaling cell stands at one end, several cells are scattered nearby, and one distant cell is barely visible beyond the courtyard wall. The exchange has found the next route it cannot classify."
 ],
 'close':'With gap junctions, plasmodesmata, and surface recognition separated, you follow the new nearby-signal alert into the Local Signal Courtyard.',
},
'U4-L03':{
 'title':'The Courtyard With a Short Reach',
 'kicker':'A chemical signal can spread to several nearby cells while only one becomes the true target.',
 'paragraphs':[
  "Warm light spills across the **Local Signal Courtyard**, a square open space bounded by low walls. Its geography is simple enough to redraw. On your **left**, a signal-emitting cell sits beside a reservoir of small chemical messengers. In the **center**, pale rings are embedded in the paving stones around that cell like the ripples of a target. On your **right**, four nearby cells stand at different points inside those rings. A fifth cell waits beyond the far wall. Mira places the route card on a pedestal and circles the word NEARBY.",
  "The left-hand cell releases a chemical messenger. The molecules spread through the nearby extracellular space, and the center rings illuminate only where the signal reaches. Mira names this kind of short-range messenger a **local regulator**. Cells can communicate over short distances by releasing **short-distance local regulators** that act in the vicinity of the signal-emitting cell. The pattern of travel defines **local signaling**. The message is secreted and moves over a short distance, so the cells do not need to be touching.",
  "At first, three of the cells on the right are bathed in the chemical signal. Only one changes. Its membrane carries a receptor whose binding site fits the signal molecule, and its interior contains the machinery needed to continue the response. The other nearby cells remain unchanged even though the messenger reaches them. Mira lifts one of the signaling molecules into the light. A signaling molecule that binds specifically to a receptor and can initiate a signaling response is a **ligand**. The responding cell is a **target cell** because it has the appropriate receptor and downstream machinery. Exposure alone does not make every nearby cell a target.",
  "The local field pulses again, and Mira labels the route **paracrine signaling**. In paracrine signaling, secreted regulators act on nearby target cells. She deliberately rolls one target cell a little farther away while keeping it inside the illuminated local field. It still responds. The picture prevents a common error. Paracrine does not mean that two membranes must be directly adjacent. It means the signal acts locally on nearby targets.",
  "For a final test, the sender releases a **growth factor**. The receptor-bearing target cell activates a growth-related response. Mira explains that growth factors are extracellular signals that can stimulate nearby cells to grow, divide, survive, or differentiate depending on the biological context. Many growth factors act locally, so the courtyard keeps them with paracrine signaling instead of automatically sending them to the endocrine rail.",
  "The route card now has a complete LOCAL row. Sender on the left, a secreted local regulator moving across a short radius, receptor-bearing target on the right. A narrow gate opens in the far wall. Beyond it, the end of a neuron hangs over a tiny gap, and a separate target membrane waits on the opposite side. Mira looks from the broad courtyard to that microscopic gap. \"Local again,\" she says, \"but this route is specialized.\""
 ],
 'close':'You leave the open courtyard and step into the Synaptic Dock, where the entire local route has been compressed into the tiny space between a neuron and its target.',
},
'U4-L04':{
 'title':'Across the Microscopic Dock',
 'kicker':'A neuron delivers a local chemical message across one narrow extracellular gap.',
 'paragraphs':[
  "The **Synaptic Dock** feels narrow after the courtyard. On your **left**, the bulb-shaped end of a neuron hangs over the edge of a platform. Directly **ahead**, a hairline gap separates that terminal from another cell. On your **right**, the target membrane faces the gap with receptor proteins embedded in its surface. Mira slides the route card into a holder beneath the central gap. The LOCAL row remains selected, but the route field is blank.",
  "Inside the presynaptic terminal, small vesicles move toward the membrane. When the terminal is triggered, the vesicles release their chemical contents into the space ahead. The released molecules do not race down the length of the neuron. Here, at the terminal, they enter the extracellular gap and diffuse across it. The narrow gap is the **synaptic cleft**, the extracellular space between a presynaptic neuron and its target cell.",
  "Mira freezes one released molecule halfway across. It is a **neurotransmitter**, a chemical signal released by a neuron that diffuses across the synaptic cleft and binds receptors on a target cell. She lets it continue. The neurotransmitter reaches a receptor on the **postsynaptic target membrane**, binds, and the target cell begins a response. The left presynaptic terminal, center cleft, and right postsynaptic target remain visibly separate, so the name of the messenger cannot collapse into the name of the space it crosses.",
  "The complete mechanism is **synaptic signaling**. It is a specialized form of local signaling in which a neuron releases neurotransmitter across a narrow synaptic cleft to a target cell. Mira places the courtyard route beside the dock route on her card. Both are local. In the courtyard, a secreted local regulator spreads through nearby extracellular space. At the dock, a neuron releases neurotransmitter across a sharply defined microscopic cleft. The distinction comes from the specialized cellular arrangement and messenger delivery, not from turning every local signal into the same category.",
  "The target membrane lights once, then goes quiet. Mira closes the LOCAL section of the card. Across the back wall, enormous doors part to reveal a transparent vessel stretching out of sight through the exchange. A hormone icon enters the vessel at one end and passes dozens of dark cell stations without stopping. The route card automatically expands its distance scale from micrometers to the length of an animal body. The next failure is obvious. The exchange knows how to cross a cleft, but it still cannot route a message that must travel far beyond the neighborhood."
 ],
 'close':'You cross from the tiny synaptic cleft into the Endocrine Transit Hub, where the next messenger must survive a body-scale journey before finding its target.',
},
'U4-L05':{
 'title':'The Messenger That Crosses the Body',
 'kicker':'Endocrine signals enter circulation and pass many cells before a receptor-bearing target responds.',
 'paragraphs':[
  "The **Endocrine Transit Hub** opens around a transparent vessel as wide as a train platform. The room keeps three fixed stations. On your **left**, a specialized endocrine cell sits at a release dock. Through the **center**, the clear bloodstream route curves away through miniature tissues representing the body. On your **right**, a distant target cell waits with a receptor displayed on its membrane. Mira places the route card on the central railing and selects DISTANT.",
  "The endocrine cell releases chemical messengers into the vessel. The current carries them away from their source and past many cells. Several cells are physically exposed to the molecules, yet their status lights remain dark. Farther along the route, the receptor-bearing target on the right recognizes the messenger and responds. This is **long-distance signaling**. A signal released by one cell type can travel far from its source to a target cell elsewhere in the organism.",
  "Mira catches one messenger in a transparent sampling chamber. It is a **hormone**, a signaling molecule produced by cells and transported to target cells, often over long distances. In animals, specialized endocrine cells can release hormones into circulation. That route is **endocrine signaling**. The bloodstream distributes the hormone widely, while receptor specificity determines which cells can respond. The hormone can pass a nonresponsive cell without turning that cell into a target.",
  "A second track lights beneath the vessel to show a familiar example. A pancreatic beta cell appears on the left and releases **insulin** after blood glucose rises. The protein hormone enters circulation and reaches tissues containing cells with insulin receptors. Those receptor-bearing cells can respond to insulin. Mira keeps the example in a small overlay so its role stays proportional. Insulin is one hormone and one endocrine pathway; it does not define what every hormone is or how every hormone works.",
  "The route card now shows a clean contrast. Local regulators act nearby. Neurotransmitters cross a synaptic cleft. Hormones in animal endocrine signaling can be carried through circulation to distant targets. Mira asks you to look again at the right-hand cell. The long travel distance explains how the messenger arrived, while the receptor explains why that particular cell can respond.",
  "A green check appears over the animal DISTANT row. One empty field remains beneath it, marked PLANT. The floor ahead slopes upward into a glasshouse wing filled with a cutaway stem, vascular bundles, and a sealed air chamber. Mira lifts the card from the railing. \"Plants signal over long distances too,\" she says. \"Their routes do not all look like this vessel.\""
 ],
 'close':'With animal endocrine transport repaired, you enter the glasshouse wing to complete the final long-distance route in the exchange.',
},
'U4-L06':{
 'title':'The Plant Route With More Than One Road',
 'kicker':'Plant hormones can move through tissues and vascular pathways, while volatile ethylene has a special route through air.',
 'paragraphs':[
  "Humidity fogs the glass above the **Plant Hormone Route**. A whole plant has been opened lengthwise across the room. On your **left**, source tissue glows where a hormone is produced or released. In the **center**, the stem exposes living tissues and vascular pathways running upward and downward through the plant. On your **right**, distant target tissue sits beside a separate clear chamber filled with air. Mira locks the route card into the final pedestal. Every earlier row is complete except PLANT DISTANT.",
  "A plant hormone leaves the source tissue on the left and enters a pathway through the plant. The model shows movement through tissues and along vascular routes toward another region. Mira keeps the central pathway broad instead of assigning one universal pipe to every plant signal. **Plant long-distance hormone signaling** can involve movement through tissues and vascular pathways, and different hormones can use different transport patterns within the plant.",
  "Then the right-hand air chamber activates. A ripening fruit releases a gas that spreads through the chamber and reaches responsive tissue without entering the central vascular route. The volatile signal is **ethylene**. Its ability to diffuse through air gives it a special long-distance route available to a gaseous plant hormone. Mira leaves the vascular pathway glowing at the same time so the distinction cannot disappear. Ethylene's airborne movement is a special case, not a rule that all plant hormones travel through air.",
  "Mira brings the transparent route card into the center of the room. Six locations are now compressed into one comparison you can reconstruct. Direct-contact communication requires cells to touch through junctions or surface interactions. Local signaling uses secreted regulators acting over a short distance. Paracrine signaling is one local arrangement. Synaptic signaling is another specialized local arrangement where neurotransmitter crosses a narrow cleft. Animal endocrine signaling uses hormones distributed through circulation to distant receptor-bearing targets. Plant hormones can move through tissues and vascular pathways, while volatile ethylene can also diffuse through air.",
  "The red SIGNAL labels that greeted you at the entrance are gone. In their place, each route has an address. Mira turns the route card over. The back contains only four empty headings, sender, messenger or contact, route or distance, and target. No vocabulary list remains. She asks you to rebuild each route from those four questions. The exchange floor answers with its geography. Contact lies behind you on one side, local routes occupy the courtyard and synaptic dock, animal distance runs through circulation, and plant distance climbs through the glasshouse.",
  "When the final target tissue responds, the exchange lights settle to green. Mira closes the route card, but another warning appears on her tablet. The routes now deliver messages correctly. The next problem is more precise. One target cell is receiving a ligand, yet its receptor will not change state. Mira looks toward a sealed membrane gate beyond the glasshouse. The journey through communication distance is complete, and the next investigation will begin at the moment a target cell actually receives a signal."
 ],
 'close':'The Cellular Communications Exchange is repaired. You leave knowing how sender, distance, delivery route, and receptor-bearing target distinguish the major communication modes before receptor signaling begins.',
},
}

# Literal visible term names used in prose when canonical labels are awkward duplicates.
TERM_OVERRIDES={
 'Direct or distance communication':'Direct or distance communication',
 'Cell communication importance':'Cell communication',
 'Antigen-presenting cell contact example':'Antigen-presenting cell contact example',
 'Short-distance local regulators':'Short-distance local regulators',
 'Growth factor as local signal':'Growth factor as local signal',
 'Hormones as long-distance messengers':'Hormones as long-distance messengers',
 'Insulin signaling example':'Insulin signaling example',
 'Plant long-distance hormone signaling':'Plant long-distance hormone signaling',
}

IMAGE_MAP={
'U4-L01':{
 'Direct or distance communication':'the same sender and target moved from touching, to nearby, to body-scale separation while the route changes',
 'Cell communication importance':'the multicellular organism outline whose growth, repair, and tissue activity pulse only when the correct routes are restored',
},
'U4-L02':{
 'Direct contact':'the three fixed direct-contact mechanisms visible in one gallery',
 'Gap junction':'the gated animal intercellular channel allowing ions and selected small signals while a large cargo sphere remains blocked',
 'Plasmodesmata':'the membrane-lined plant channels crossing the cell wall between neighboring cytoplasms',
 'Antigen-presenting cell contact example':'the antigen-presenting cell and T cell meeting through complementary surface molecules at the center station',
},
'U4-L03':{
 'Short-distance local regulators':'the short illuminated radius around the signal-emitting cell',
 'Local signaling':'a secreted messenger spreading only through the nearby courtyard',
 'Local regulator':'one secreted chemical messenger moving within the local radius',
 'Ligand':'the signaling molecule that fits and binds the target-cell receptor',
 'Target cell':'the nearby cell that alone has the matching receptor and downstream response machinery',
 'Paracrine signaling':'the local field reaching nearby receptor-bearing cells without requiring membrane contact',
 'Growth factor as local signal':'the growth-factor pulse activating a growth-related response in one nearby target cell',
},
'U4-L04':{
 'Synaptic signaling':'the presynaptic terminal, narrow cleft, and receptor-bearing target arranged left to right',
 'Neurotransmitter':'the chemical messenger released from the neuron terminal and diffusing across the cleft',
 'Synaptic cleft':'the narrow extracellular gap between the presynaptic terminal and target membrane',
},
'U4-L05':{
 'Long-distance signaling':'a chemical messenger traveling through the body-scale vessel from its source to a distant target',
 'Hormones as long-distance messengers':'hormone molecules riding the circulation route to distant tissues',
 'Hormone':'one signaling molecule carried from the endocrine source through circulation',
 'Endocrine signaling':'the endocrine cell releasing hormone into the bloodstream route',
 'Insulin signaling example':'a pancreatic beta-cell insulin overlay reaching distant cells with insulin receptors',
},
'U4-L06':{
 'Plant long-distance hormone signaling':'a plant hormone moving from source tissue through tissue or vascular pathways, beside a separate ethylene-in-air route',
},
}

def scene_layout(b):
    return {'orientation':b['orientation_sentence'],'zones':[{'position':p,'label':lab,'symbol':sym,'description':desc} for p,lab,sym,desc in ZONE_COPY[b['locus_id']]]}

def cast_for(b):
    cast=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    for c in b['stable_cast']:
        cast.append({'name':c['name'],'kind':'scientific part or process','visual':c['visual_identity'],'job':c['job_in_scene']})
    cast.append({'name':'Transparent route card','kind':'continuity tool','visual':'a clear four-field card labeled sender, messenger/contact, route/distance, and target','job':'keeps the comparison dimensions visible as communication mechanisms are repaired; it is a guide device and never represents a biological molecule'})
    return cast

def make_scene(lid,idx):
    b=B[lid]; n=NARR[lid]
    beats=[]; snaps=[]
    for t in b['term_introductions']:
        term=TERM_OVERRIDES.get(t['canonical_term'],t['canonical_term'])
        image=IMAGE_MAP[lid].get(t['canonical_term'],IMAGE_MAP[lid].get(term,b['micro_anchor']))
        beats.append({'object_id':t['knowledge_id'],'term':term,'story':image,'science':t['canonical_science'],'exact_name':bool(t.get('exact_name_recall')),'hint':image,'name_support':t['name_support']})
        snaps.append({'term':term,'meaning':t['canonical_science'],'image':image})
    qr=b['quick_recall']; cp=bool(qr.get('enabled'))
    cp_id=b['primary_knowledge_id']
    prompt=qr.get('candidate_prompt','') if cp else ''
    answer=qr.get('answer','') if cp else ''
    hint=''
    if cp:
        if lid=='U4-L02': hint='Return to the contact gallery. The animal channel is on the left and the membrane-lined plant wall channels are on the right.'
        elif lid=='U4-L05': hint='Picture the center bloodstream rail carrying the messenger far beyond the nearby courtyard before a receptor-bearing cell responds.'
        else: hint='Return to the fixed left, center, and right mechanism in this location.'
    return {
      'scene_index':idx,'locus':b['scene_title'],'locus_id':lid,'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['exact_location']+' — '+b['micro_anchor']+'.',
      'scene_layout':scene_layout(b),'cast':cast_for(b),'continuity_object':J1['continuity_object'],
      'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':beats,'memory_snapshot':snaps,
      'misconception_guards':b['misconception_guards'],'exit_memory':b['exit_memory'],
      'checkpoint':cp,'checkpoint_object_id':cp_id,'checkpoint_prompt':prompt,'checkpoint_answer':answer,'checkpoint_hint':hint,
      'next_locus':B[b['causal_transition']['to_locus_id']]['scene_title'] if b['causal_transition']['to_locus_id'] else None,
      'causal_transition':b['causal_transition']['transition_logic']
    }

lids=J1['route']
scenes=[make_scene(lid,i) for i,lid in enumerate(lids)]
journey={
 'palace_id':'U4-J1','palace_name':'Cellular Communications Exchange','story_title':'The Exchange With No Addresses',
 'tagline':'Every cellular message has been routed as the same generic signal. Rebuild the exchange by separating contact, local, synaptic, endocrine, and plant long-distance communication.',
 'guide':GUIDE,
 'premise':'A multicellular communications exchange is failing because every message has been stamped SIGNAL and sent without a reliable address. Messages meant for touching cells, nearby targets, neural synapses, distant animal tissues, and plant targets are being mixed together. Mira brings one transparent four-field route card so every route can be rebuilt from sender, messenger or contact, travel distance, and target.',
 'mission':'Repair the exchange from shortest to longest communication route. Keep the same comparison fields visible while each mechanism is activated, then leave each location able to reconstruct who sends the message, how it travels, how far it moves, and which target can respond.',
 'finale':'At the glasshouse exit, the red generic SIGNAL labels disappear. The route card now separates direct contact, local paracrine signaling, specialized synaptic signaling, animal endocrine signaling, and plant long-distance hormone movement. A new receptor-state alarm then opens the way to Journey 2, where delivery gives way to reception.',
 'estimated_minutes':18,'scene_count':len(scenes),'checkpoint_count':sum(bool(s['checkpoint']) for s in scenes),
 'learner_rule':'Read or listen and picture the room before the mechanism moves. Keep left, center, and right fixed. Watch the biological action first, then attach the exact term. Quick Recall is optional during first exposure.',
 'route_orientation':'The Cellular Communications Exchange is one continuous six-location route. Begin in the circular Communication Compass. Follow its left contact lane into the Contact Junction Gallery, exit into the Local Signal Courtyard, pass through the narrow Synaptic Dock, expand into the body-scale Endocrine Transit Hub, and finish in the glasshouse Plant Hormone Route. The transparent route card travels with Mira through every location while each room keeps its own fixed left, center, and right anchors.',
 'route':route,'scenes':scenes,'student_release':'DEVELOPER_PREVIEW_F4A','narrative_standard':'V2-NARRATIVE-4.0-U4-F4A'
}

(U4/'journeys').mkdir(parents=True,exist_ok=True)
(U4/'journeys'/'U4-J1.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
card={k:journey[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
registry={'schema':'memory-palace-v2-unit4-f4a-registry-1.0','course_id':'ap-biology','unit_id':'unit-4','unit_title':'Cell Communication and Cell Cycle','narrative_standard':'V2-NARRATIVE-4.0-U4-F4A','journey_count':1,'scene_count':6,'checkpoint_count':2,'guided_journeys':[card]}
(U4/'journeys-f4a.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U4/'status-f3.json').read_text(encoding='utf-8'))
status.update({'status':'F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','pipeline_status':'POLISHED_NARRATIVE_PILOT_F4A','canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3','narrative_lock':'LOCKED_F4A_J1','student_release':False,'preview_release':True,'journey_count':1,'scene_count':6,'polished_journeys':1,'polished_scenes':6,'polished_checkpoint_count':2,'narrative_story_files':1,'next_required_output':'F4B polished narrative for Journey 2 only after F4A prose QA and human narrative review'})
(U4/'status-f4a.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(U4/'status.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; course=json.loads(cp.read_text(encoding='utf-8'))
for u in course['units']:
    if u['unit_id']=='unit-4':
        u.update({'status':'F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','journey_count':1,'scene_count':6,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEY1_POLISHED_F4A','polished_journeys':1,'polished_scenes':6,'student_release':False,'preview_release':True,'canonical_records':180})
cp.write_text(json.dumps(course,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=['journeys/U4-J1.json','journeys-f4a.json','status-f4a.json']
lock={'schema':'memory-palace-v2-unit4-f4a-content-lock-1.0','unit_id':'unit-4','stage':'F4A','lock_status':'LOCKED_F4A_J1','student_release':False,'preview_release':True,'files':{f:{'bytes':(U4/f).stat().st_size,'sha256':sha(U4/f)} for f in files}}
(U4/'content-lock-f4a.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit4-f4a-release-manifest-1.0','unit_id':'unit-4','stage':'F4A','student_release':False,'preview_release':True,'canonical_records_protected':180,'polished_journeys':1,'polished_scenes':6,'journey_1_records':sum(len(s['object_ids']) for s in scenes),'journey_1_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'narrative_words':sum(len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs']))) for s in scenes),'next_stage':'F4B_JOURNEY2_AFTER_F4A_HUMAN_REVIEW'}
(U4/'f4a-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Built Unit 4 F4A',manifest)

# Human-readable narrative artifact for classroom/developer review.
doc=['# Unit 4 F4A · Journey 1 Narrative','',f"## {journey['story_title']}",'',journey['tagline'],'',f"**Guide**  {GUIDE['name']}, {GUIDE['role']}",'',f"**Premise**  {journey['premise']}",'',f"**Mission**  {journey['mission']}",'',f"**Route**  {' → '.join(r['locus'] for r in route)}",'', '> F4A is a developer narrative preview. Unit 4 remains `student_release: false`. The purpose of this artifact is to evaluate spatial clarity, scientific action, continuity, and prose quality before Journey 2 is authored.','']
for s in scenes:
    doc += [f"## {s['scene_index']+1}. {s['locus']}",'',f"### {s['title']}",'',f"*{s['scene_kicker']}*",'',f"**Physical layout**  {s['scene_layout']['orientation']}",'']
    for p in s['story_paragraphs']: doc += [p,'']
    doc += [f"**Exit**  {s['story_close']}",'']
    if s['checkpoint']:
        doc += [f"**Optional Quick Recall**  {s['checkpoint_prompt']}",'']
doc += ['## Journey payoff','',journey['finale'],'']
(ROOT/'docs'/'UNIT4_F4A_JOURNEY1_STORY.md').write_text('\n'.join(doc),encoding='utf-8')

release_doc=f'''# Unit 4 F4A Release\n\n## Scope\n\nF4A authors only **Journey 1, Cellular Communications Exchange**. The F1 scientific lock, F2 learning architecture, and F3 scene briefs remain protected. No Journey 2–7 polished prose is present.\n\n## Narrative release\n\n- Journey title: **{journey['story_title']}**\n- Polished journeys: **1 / 7**\n- Polished scenes: **6 / 51**\n- Journey 1 knowledge records: **{manifest['journey_1_records']}**\n- Narrative words: **{manifest['narrative_words']}**\n- Optional first-exposure recalls: **{manifest['journey_1_checkpoints']}**\n- Student release: **false**\n- Developer preview: **true**\n\n## Narrative standard\n\nEach scene preserves the locked F3 left/center/right geography and uses Dr. Mira Chen plus the transparent four-field route card for continuity. The scientific action must remain the memorable event. The polished prose is required to make the location reconstructable before the mechanism begins, keep biological parts visually distinct, state corrected science without source-management language, and end with a causal reason to enter the next locus.\n\n## Next gate\n\nF4B is blocked until Journey 1 passes automated prose QA and human narrative review. F4B will author **Journey 2, Signal Reception Gateway**, while Journey 1 remains locked unchanged.\n'''
(ROOT/'docs'/'UNIT4_F4A_RELEASE.md').write_text(release_doc,encoding='utf-8')
