from __future__ import annotations
import json, hashlib, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content'/'ap-biology'/'unit-4'
F3=json.loads((U4/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS=json.loads((U4/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J2=next(j for j in JBRIEFS if j['journey_id']=='U4-J2')
B={b['locus_id']:b for b in F3 if b['journey_id']=='U4-J2'}

# F4B extends F4A. Journey 1 is a protected predecessor and is never regenerated here.
J1_PATH=U4/'journeys'/'U4-J1.json'
if not J1_PATH.exists():
    raise RuntimeError('F4B requires the locked F4A Journey 1 artifact')
J1_LOCK=json.loads((U4/'content-lock-f4a.json').read_text(encoding='utf-8'))
expected_j1=J1_LOCK['files']['journeys/U4-J1.json']
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
if J1_PATH.stat().st_size!=expected_j1['bytes'] or sha(J1_PATH)!=expected_j1['sha256']:
    raise RuntimeError('F4B refuses to proceed because locked Journey 1 changed')
J1=json.loads(J1_PATH.read_text(encoding='utf-8'))

GUIDE={
 'name':'Dr. Mira Chen',
 'role':'cellular-systems investigator',
 'visual':'charcoal field jacket, clear protective glasses, and a compact white tablet clipped beside a three-state receptor monitor',
 'story_job':'Mira keeps ligand, receptor, receptor location, and receptor state separate while the gateway is repaired. She names the biology only after the defining molecular event is visible.'
}

route=[
 {'scene_index':0,'locus':'Reception Checkpoint','short':'Reception','floor':'Gateway entrance','symbol':'◇'},
 {'scene_index':1,'locus':'Receptor Location Split','short':'Location','floor':'Membrane divide','symbol':'║'},
 {'scene_index':2,'locus':'Intracellular Signal Suite','short':'Inside','floor':'Interior suite','symbol':'◉'},
 {'scene_index':3,'locus':'GPCR Receptor Door','short':'GPCR','floor':'Membrane door','symbol':'7'},
 {'scene_index':4,'locus':'G-Protein Switchboard','short':'G switch','floor':'Cytoplasmic board','symbol':'GDP↔GTP'},
 {'scene_index':5,'locus':'Ligand-Gated Channel Gate','short':'Ion gate','floor':'Channel exit','symbol':'⇅'},
]

ZONE_COPY={
'U4-L07':[
 ('left','Ligand candidate rail','◇','Several differently shaped signaling molecules approach from the extracellular side. Only one has the chemical and structural compatibility needed for the receptor displayed at center.'),
 ('center','Receptor binding gate','▥','A membrane receptor with a clearly defined ligand-binding region can move from unbound to ligand-bound and then into an activated conformational or functional state.'),
 ('right','Intracellular receptor face','●','The receptor’s cytoplasmic side changes state only after compatible binding. The downstream pathway remains physically separate so reception is not confused with transduction or response.')],
'U4-L08':[
 ('left','Surface-receptor route','▥','A signaling molecule that does not readily cross the lipid bilayer remains outside and meets a receptor located at the plasma membrane.'),
 ('center','Plasma-membrane divide','║','A large bilayer wall acts as the permeability boundary. One comparison signal is stopped outside while another suitable small or hydrophobic signal can enter.'),
 ('right','Intracellular-receptor route','◉','A receptor in the cytoplasm or nucleus binds a signaling molecule that has crossed the membrane, making receptor location visibly different from the surface route.')],
'U4-L09':[
 ('left','Steroid-hormone route','S','A steroid-hormone example crosses the membrane and binds an intracellular receptor before the receptor complex can influence gene expression.'),
 ('center','Nuclear target suite','◎','The central interior of the cell contains nuclear and intracellular receptor destinations so the receptor, not the free hormone alone, remains the signaling target.'),
 ('right','Thyroid and nitric-oxide routes','T/NO','Thyroid hormone reaches a nuclear receptor while nitric oxide diffuses across membranes and activates an intracellular target such as soluble guanylyl cyclase.')],
'U4-L10':[
 ('left','Extracellular ligand face','◇','A ligand approaches the outside-facing portion of a conventional seven-transmembrane receptor and never passes through the receptor into the cytoplasm.'),
 ('center','Seven-pass GPCR body','7','The G protein-coupled receptor crosses the membrane seven times and changes conformation when ligand binds.'),
 ('right','G-protein interface','G','A heterotrimeric G protein waits on the cytoplasmic side as a separate molecular structure that can be regulated by the activated GPCR.')],
'U4-L11':[
 ('left','GDP-bound G protein','GDP','The heterotrimeric G protein begins in an inactive GDP-bound state beside the activated receptor.'),
 ('center','Nucleotide switch','GDP→GTP','The activated GPCR promotes GDP release and GTP binding, changing the G protein into an active signaling state.'),
 ('right','Effector and reset bay','GTP→GDP','The active G-protein component regulates an effector and then intrinsic GTPase activity hydrolyzes GTP to GDP, helping reset the molecular switch.')],
'U4-L12':[
 ('left','Closed ion channel','▮','A membrane channel waits closed while its ligand approaches from the signaling side, making the inactive starting state visually unmistakable before binding occurs.'),
 ('center','Ligand-binding channel gate','⇅','Ligand binding changes the channel gate or open probability. The receptor and ion channel are the same functional membrane structure in this mechanism.'),
 ('right','Ion-flow response lane','+ −','Specific ions move according to their electrochemical driving forces after the gate changes state, altering membrane or ionic conditions that can initiate a cellular response.')],
}

NARR={
'U4-L07':{
 'title':'The Gate That Answered Every Knock',
 'kicker':'The gateway is treating every arriving signal as a match, so the first repair is to make recognition selective again.',
 'paragraphs':[
  "The route from the Cellular Communications Exchange ends at a second building whose entire front wall resembles an enlarged plasma membrane. You enter the **Signal Reception Gateway** through a narrow observation bay and stop at three fixed stations. On your **left**, a silver rail carries several differently shaped ligand candidates toward the membrane. Directly **ahead**, one receptor stands in the center of the membrane like a molecular gate, its binding pocket facing the incoming signals. On your **right**, the receptor's intracellular face projects into a dark cytoplasmic chamber. Nothing downstream is moving yet. Beside the center gate, a vertical monitor has only three lights: UNBOUND/INACTIVE, LIGAND-BOUND, and ACTIVATED/CHANGED. All three are flashing at once.",
  "Dr. Mira Chen steps in behind you and taps the monitor with the edge of her white tablet. The failure is obvious but dangerous: the gateway has been reporting activation whenever any signal arrives. She clears the display until only UNBOUND/INACTIVE remains. Then she sends the first ligand candidate from the left rail toward the receptor. It bumps against the binding pocket and falls away. A second candidate touches the same site and is also rejected. The monitor does not move. A third candidate reaches the receptor, fits the binding region, and remains attached. Only now does the middle light turn on. Mira points from the matching ligand to the protein. The signaling molecule is the **ligand**; the macromolecule that recognizes it is the **receptor**. Signaling begins when an appropriate ligand is recognized by a receptor in a target cell.",
  "She freezes the matched pair so you can compare it with the rejected candidates still lying on the left rail. The difference is **ligand-binding specificity**. Binding depends on complementary chemical and structural properties, so a receptor does not respond equally to every molecule that happens to collide with it. That relationship also explains **ligand-receptor specificity** at the level of whole cells. Two nearby cells can encounter the same signaling molecule, but only a cell carrying a suitable receptor and the necessary intracellular machinery responds directly to it. That responsive cell is the target cell. The signal is not meaningful merely because it exists outside a membrane; recognition makes it relevant to a particular cell.",
  "Mira releases the matched ligand again. Binding changes the receptor's conformation or functional state. The outside ligand remains where it bound, while the receptor's intracellular face changes shape on your right and the ACTIVATED/CHANGED light turns on. This is **reception**: the target cell detects the signal when the ligand binds its receptor. The visible change is a **ligand-induced receptor shape change**, or more generally a **receptor conformational or state change**. Mira keeps the dark downstream chamber closed. “Reception is the detection step,” she says. “It is not the whole pathway.” A signal transduction pathway can link **reception to a later cellular response**, but the extracellular ligand usually does not physically travel down that intracellular relay.",
  "The three lights finally behave in order: unbound, then ligand-bound, then activated. Yet the monitor immediately displays a new question under the receptor diagram: WHERE IS THE RECEPTOR? The gateway has learned which ligand belongs, but it is still placing every receptor in the membrane. A vertical seam opens through the wall ahead. The left side of the next room remains outside the cell, the right side lies inside the cytoplasm, and the plasma membrane itself forms a bright divider between them. Mira unclips the three-state monitor and carries it through the opening."
 ],
 'close':'The compatibility gate now rejects the wrong ligands, but the monitor cannot complete the diagnosis until receptor location is repaired. You follow the membrane seam into the Receptor Location Split.'
},
'U4-L08':{
 'title':'Which Side of the Membrane Holds the Receptor?',
 'kicker':'A receptor can sit in the membrane or inside the cell, and membrane permeability helps determine which arrangement a signal can use.',
 'paragraphs':[
  "The **Receptor Location Split** is built around one enormous cross-section of a plasma membrane. Its geography is impossible to miss. On your **left**, outside the cell, a large water-soluble signal waits beside a receptor embedded in the membrane. Directly **ahead**, the lipid bilayer rises from floor to ceiling as a translucent two-layer wall. On your **right**, inside the cell, a second receptor sits free in the cytoplasm near a nuclear doorway. Mira clips the three-state receptor monitor to the center membrane so both routes can be compared without moving their positions.",
  "She sends the large hydrophilic signal toward the bilayer first. It reaches the membrane but does not simply pass through the hydrophobic interior. The receptor on the left-facing surface binds it, and the monitor records ligand-bound and then activated. Mira labels that structure a **cell-surface receptor**. Cell-surface receptors span or associate with the plasma membrane and provide a way for signals that do not readily cross the lipid bilayer to be detected without entering the cell. The signal can remain outside while receptor activation produces an intracellular effect. This keeps receptor location and signal movement as separate questions.",
  "Now Mira releases a different comparison signal at the same membrane. This one is sufficiently small or hydrophobic to cross the bilayer. It passes through the center wall and reaches the receptor on the right, inside the cell. That receptor is an **intracellular receptor**, located in the cytoplasm or nucleus and capable of binding a signaling molecule that can cross the plasma membrane. The monitor again records the three states, but this time the binding event occurs on the interior side. The larger principle is **receptor location**: receptors may be located on the cell surface or within the cytoplasm or nucleus of the target cell.",
  "Mira then removes a simplistic sign that has appeared over the membrane: HYDROPHOBIC = ALWAYS ENTERS; HYDROPHILIC = NEVER ENTERS. She replaces it with a permeability meter. The useful **hydrophobic ligand principle** is that hydrophobic or sufficiently small signaling molecules can cross the lipid bilayer and may bind intracellular receptors, while many hydrophilic or sufficiently large signals rely on surface receptors because they do not readily cross. Membrane permeability is a governing principle, not a rigid classification shortcut for every possible signaling molecule. Transport mechanisms, molecular size, charge, and specific cellular context can matter.",
  "With the split repaired, the monitor now displays two legitimate receptor addresses: SURFACE and INTRACELLULAR. The right-hand intracellular door unlocks. Behind it, three illuminated examples are already waiting: a steroid-hormone route on the left, a nuclear receptor station in the middle, and separate thyroid-hormone and nitric-oxide routes on the right. Mira lifts the monitor from the membrane. “We only need these examples to make the location principle concrete,” she says as you step inside. “The principle comes first; the examples show how it can work.”"
 ],
 'close':'The membrane split now places receptors on the correct side of the boundary. The unanswered intracellular examples draw you through the right-hand door into the Intracellular Signal Suite.'
},
'U4-L09':{
 'title':'Signals That Cross the Boundary',
 'kicker':'Some signals enter the cell before they meet their receptor, but the receptor still performs the recognition and regulatory work.',
 'paragraphs':[
  "The **Intracellular Signal Suite** feels like the interior of the target cell made architectural. On your **left**, a steroid-hormone route begins outside a small membrane panel and continues into the cytoplasm. Directly **ahead**, a large nuclear target area occupies the center of the room, its DNA shown behind a protective glass partition. On your **right**, two narrower lanes are marked THYROID HORMONE and NITRIC OXIDE. Mira places the three-state receptor monitor at the edge of the central nuclear station so every example must still pass through receptor recognition rather than jumping directly from signal to response.",
  "She begins with the steroid route. A steroid-hormone example crosses the lipid bilayer and enters the cell. It does not march directly to DNA and issue an instruction by itself. It binds an intracellular receptor first. The monitor moves from unbound to ligand-bound to activated, and only the activated receptor system is then allowed to influence gene expression at the central nuclear area. This is **steroid-hormone intracellular signaling**: many steroid hormones diffuse through the plasma membrane and bind intracellular receptors that can influence gene expression. Keeping the receptor visible prevents the seductive but incorrect picture of a free hormone simply attaching to DNA and acting alone.",
  "On the right, Mira opens the thyroid-hormone lane. Thyroid hormone is lipid-soluble and can enter cells to bind an intracellular **nuclear receptor**. The receptor and ligand are placed together at the nucleus, demonstrating **thyroid-hormone intracellular signaling**. The neighboring lane uses a very different molecule. A small cloud labeled NO diffuses across a membrane with no receptor embedded at the crossing point. Once inside, nitric oxide activates an intracellular target, illustrated here by soluble guanylyl cyclase. This is **nitric-oxide intracellular signaling**. Nitric oxide is a small gaseous signaling molecule, so its route is visually different from the hormone-receptor examples even though all three belong on the intracellular side of the receptor-location comparison.",
  "Mira steps back and lets the three paths remain visible together. Steroid hormone, thyroid hormone, and nitric oxide are useful examples, yet they are not a list every signaling problem must reproduce. The larger model from the previous room still governs the gateway: signal properties affect whether the ligand can cross the membrane, and receptor location determines where recognition occurs. Some intracellular receptors can directly influence gene expression after activation; other intracellular targets can regulate enzymes or other processes. The gateway therefore needs a location rule and a mechanism, not a memorized slogan that every intracellular signal behaves identically.",
  "The receptor monitor clears all three examples and flashes SURFACE RECEPTOR TEST REQUIRED. Across the far wall, a circular membrane door lights up with seven vertical passes through the bilayer. A ligand waits outside that door, while a separate three-part G protein rests on the cytoplasmic side. Mira points to the seven-pass structure. “Now we return to the membrane,” she says. “This receptor does not carry the ligand through. Its shape change controls a separate switch inside.” The seven-pass door opens into the next chamber."
 ],
 'close':'The intracellular examples make receptor location concrete, but a seven-pass surface receptor is now demanding a mechanism test. You follow the monitor back to the membrane and enter the GPCR Receptor Door.'
},
'U4-L10':{
 'title':'The Seven-Pass Door That Never Lets the Ligand Through',
 'kicker':'A GPCR changes its own conformation and regulates a separate G protein on the cytoplasmic side.',
 'paragraphs':[
  "The **GPCR Receptor Door** is a tall membrane chamber organized around one unmistakable structure. On your **left**, outside the cell, a ligand waits at the receptor's extracellular-facing binding region. Directly **ahead**, the receptor body winds back and forth through the membrane seven times like a seven-pass ribbon embedded in the bilayer. On your **right**, inside the cytoplasm, a separate heterotrimeric G protein waits near the receptor's intracellular face. Mira sets the three-state monitor beside the center structure and leaves a clear gap between the receptor and the G protein so they cannot visually collapse into one object.",
  "The ligand binds on the left. The receptor changes conformation across its membrane-spanning structure, and the monitor advances from ligand-bound to activated. The ligand never crosses through the receptor. What crosses the boundary is not the ligand molecule but the consequence of the receptor's changed state. Mira names the structure a **G protein-coupled receptor**, or **GPCR**. A GPCR is a cell-surface receptor that changes conformation when a ligand binds and then regulates a heterotrimeric G protein on the cytoplasmic side. **GPCRs are an important example of receptor proteins in eukaryotes**, which is why this seven-pass model earns its own door.",
  "She then points to the right-hand structure. It is not the GPCR. The G protein is a separate membrane-associated molecular complex waiting to be regulated by the receptor. The receptor remains in the membrane; the G protein remains on the cytoplasmic side. Mira activates the GPCR once more, and only the interface between them lights. The image fixes the causal order: extracellular ligand binds GPCR → GPCR changes conformation → activated GPCR regulates the separate G protein. This is receptor activation leading toward transduction without turning the ligand into the intracellular relay molecule.",
  "Several dim receptor silhouettes appear along the back wall. One resembles an enzyme-linked receptor; another has a different membrane architecture. Mira leaves them unlabelled but visible. “Do not make this door into the whole building,” she says. GPCRs and ligand-gated channels are two important receptor examples, but they are not an exhaustive two-family taxonomy of membrane receptors. The lesson in this room is the specific GPCR mechanism and the physical distinction between receptor and G protein.",
  "The receptor monitor now behaves correctly at the seven-pass door, but the right-hand G protein remains gray. Its GDP label is visible, and a nearby socket holds a GTP token. The next room's switchboard begins flashing GDP RELEASE REQUIRED. Mira follows the cytoplasmic side of the membrane instead of returning outside. The GPCR has done its part; the unresolved problem has moved one molecular step inward."
 ],
 'close':'The GPCR has changed state without carrying the ligand through the membrane. The remaining inactive G protein pulls you directly into the G-Protein Switchboard.'
},
'U4-L11':{
 'title':'The Switch That Runs on State, Not Fuel',
 'kicker':'GDP and GTP mark different states of the G-protein switch, and hydrolysis resets the system after signaling.',
 'paragraphs':[
  "The **G-Protein Switchboard** sits immediately behind the GPCR door, still on the cytoplasmic side of the membrane. On your **left**, the heterotrimeric G protein rests beside the activated receptor with GDP bound and its indicator dark. Directly **ahead**, a central exchange mechanism holds one GDP slot and one GTP slot. On your **right**, an effector enzyme or channel waits beside a reset dial labeled GTP → GDP. Mira clips the three-state receptor monitor to the wall behind you; its receptor light stays ACTIVATED so the switchboard can show what happens after receptor activation without pretending the receptor and G protein are the same molecule.",
  "Mira first identifies the left-hand complex as a **heterotrimeric G protein**. It is membrane-associated and functions as a molecular switch regulated by GDP and GTP binding as well as by interaction with an activated GPCR. In the inactive state, GDP is bound. The activated GPCR engages the G protein and promotes GDP release. The empty nucleotide site does not stay empty for long; GTP binds in its place. The center indicator turns on. This **GDP-to-GTP exchange** changes the G protein into an active signaling state that can regulate downstream effectors.",
  "The active component moves to the right-hand station and interacts with the waiting effector. Mira uses an enzyme silhouette first, then briefly swaps in a channel silhouette to emphasize the general relationship. An activated G-protein component can interact with an **effector enzyme or channel**, altering downstream signaling and potentially amplifying the response. The key is the order: receptor activation changes the G protein's nucleotide state; the GTP-bound state enables effector regulation. The G protein is not a fragment of the receptor, and the effector is another downstream partner.",
  "Then Mira reaches for the reset dial. The G protein has intrinsic GTPase activity, so GTP is hydrolyzed to GDP. The active indicator fades and the switch returns toward its inactive state. This is **GTP hydrolysis and switch reset**. Mira covers a misleading ENERGY TANK label that has appeared under GTP. In this mechanism, GDP/GTP binding functions primarily as a molecular switch. GTP hydrolysis helps terminate the active state. Although GTP is a high-energy nucleotide in biochemical terms, the memorable job here is state control, not an ATP-like picture of GTP being burned simply to power motion.",
  "The switchboard now cycles cleanly: GDP-bound inactive → GDP release and GTP binding → effector regulation → GTP hydrolysis → GDP-bound reset. The receptor monitor marks the GPCR step complete. A second alert appears at the far end of the membrane: RECEPTOR IS THE CHANNEL. The wall opens onto a gate whose central protein contains its own ion pore. Mira leaves the G-protein machinery behind. “Different receptor, different mechanism,” she says. “This time the binding event changes ion flow directly through the receptor-channel itself.”"
 ],
 'close':'The GDP/GTP switch has reset, but a different membrane receptor now demands attention. You leave the separate G protein behind and enter the Ligand-Gated Channel Gate.'
},
'U4-L12':{
 'title':'The Receptor That Opens an Ion Door',
 'kicker':'Here the receptor is also the gate, so ligand binding changes ion flux without using the GPCR/G-protein switch.',
 'paragraphs':[
  "The final room of the **Signal Reception Gateway** is a narrow membrane hall. On your **left**, a ligand approaches a closed ion channel embedded in the membrane. Directly **ahead**, the channel's ligand-binding region and gate form one central protein structure. On your **right**, a row of specific ions waits on one side of the membrane beside a meter that can display ion flux and changes in membrane conditions. Mira sets the three-state receptor monitor beneath the channel. Unlike the previous room, there is no GPCR and no separate G protein anywhere in the mechanism.",
  "With no ligand bound, the channel remains in its initial gate state and ion flow is restricted. Mira allows the compatible ligand to bind. The receptor-channel changes state, and the gate's probability of being open changes. This is a **ligand-gated ion channel**, a membrane receptor and channel whose open probability changes when a ligand binds, thereby allowing or restricting specific ion movement. At the broader level, **ligand-gated channels** can open or close in response to ligand binding. The receptor is not handing the message to a separate G protein here; the receptor's own channel gate is the crucial moving part.",
  "The central gate opens in the model. Only the relevant ions move through the channel, following their electrochemical driving forces. Mira does not add a tiny motor that pushes each ion through. The change in gating alters ion flux across the membrane. On the right, the ion-flux meter rises and the membrane/electrical display changes. This is the **ion-channel signaling response**: opening or closing a ligand-gated ion channel changes ion movement and membrane properties, which can initiate downstream cellular responses. If the gate closes, ion flux falls. The sequence remains ligand binding → channel-state change → altered ion flux → downstream consequence.",
  "Mira places the three receptor mechanisms from the journey on a final wall without merging them. The intracellular-receptor route shows a ligand crossing the membrane to meet its receptor inside. The GPCR route shows an extracellular ligand changing a seven-pass receptor that regulates a separate G protein. The ligand-gated ion-channel route shows ligand binding changing the receptor-channel's gate state directly. All are examples of reception, but their locations and downstream mechanisms differ. The comparison prevents the shortcut that every receptor simply passes a signal to another protein in the same way.",
  "The three-state monitor now works exactly as intended. UNBOUND/INACTIVE lights before the signal arrives. LIGAND-BOUND lights only for a compatible ligand at the proper receptor. ACTIVATED/CHANGED appears only when that receptor's actual mechanism changes state. Mira turns the monitor toward the corridor beyond the gateway. A new violet line has appeared there, branching through several intracellular relay stations. The receptor problem is solved; the next unresolved question is what happens **after** a receptor activates. The doors of the Signal Relay Tower begin to open, ready for transduction, phosphorylation, second messengers, amplification, and response."
 ],
 'close':'The reception gateway is repaired. With ligand, receptor, receptor location, and receptor mechanism now distinct, the only unresolved signal lies downstream in the Signal Relay Tower.'
},
}

TERM_IMAGES={
'U4-K-004':'the dark downstream corridor that lights only after receptor activation, linking reception toward a later response',
'U4-K-006':'the compatible ligand that remains attached to the receptor while rejected candidates fall away',
'U4-K-007':'the receptor binding pocket accepting only the chemically and structurally compatible ligand',
'U4-K-011':'the receptor changing shape at its intracellular face after ligand binding',
'U4-K-058':'the three-state monitor moving from unbound to ligand-bound when the target cell detects the signal',
'U4-K-059':'the receptor protein fixed in the membrane with a distinct ligand-binding region',
'U4-K-060':'wrong ligands rejected on the left while only the compatible ligand activates the target receptor',
'U4-K-061':'the activated receptor interior face visibly changing state while the ligand remains outside',
'U4-K-009':'the split view showing one receptor in the membrane and another in the cytoplasm or nucleus',
'U4-K-062':'the membrane-embedded receptor binding a signal that does not readily cross the bilayer',
'U4-K-063':'the cytoplasmic or nuclear receptor meeting a ligand after the ligand crosses the membrane',
'U4-K-064':'the permeability wall stopping one signal while allowing a suitable small or hydrophobic signal to cross',
'U4-K-065':'the steroid hormone crossing the membrane and binding an intracellular receptor before gene regulation',
'U4-K-066':'the thyroid-hormone lane ending at an intracellular nuclear receptor',
'U4-K-067':'the NO cloud diffusing across the membrane and activating soluble guanylyl cyclase inside',
'U4-K-008':'the seven-pass membrane receptor shown as one important eukaryotic receptor example',
'U4-K-081':'the seven-pass GPCR changing conformation and contacting a separate cytoplasmic G protein',
'U4-K-082':'the separate three-part G protein resting beside the membrane with GDP bound',
'U4-K-083':'GDP leaving and GTP entering the G-protein nucleotide switch',
'U4-K-084':'GTP being hydrolyzed to GDP as the G-protein switch resets',
'U4-K-085':'the GTP-bound G-protein component regulating an effector enzyme or channel',
'U4-K-014':'the membrane receptor-channel changing gate state when its ligand binds',
'U4-K-086':'the central ligand-gated ion channel acting as both receptor and ion pore',
'U4-K-087':'specific ions changing flux after the channel gate changes state',
}

MONITOR={
 'name':'Three-state receptor monitor','kind':'journey continuity object',
 'visual':'a narrow vertical display with exactly three lights labeled UNBOUND/INACTIVE, LIGAND-BOUND, and ACTIVATED/CHANGED; it travels beside the membrane from room to room',
 'job':'records receptor state without becoming a biological molecule, keeping signal arrival, binding, and receptor activation in causal order across all six locations'
}

def scene_layout(b):
    zones=[]
    for side,name,symbol,desc in ZONE_COPY[b['locus_id']]:
        zones.append({'position':side,'label':name,'symbol':symbol,'description':desc})
    return {'orientation':b['orientation_sentence'],'zones':zones}

def cast_for(b):
    casts=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    for part in b['stable_cast']:
        casts.append({'name':part['name'],'kind':part['type'].lower(),'visual':part['visual_identity'],'job':part['job_in_scene']})
    casts.append(dict(MONITOR))
    return casts

def make_scene(lid,idx):
    b=B[lid]; n=NARR[lid]
    beats=[]; snaps=[]
    for t in b['term_introductions']:
        term=t['canonical_term']; image=TERM_IMAGES[t['knowledge_id']]
        beats.append({'object_id':t['knowledge_id'],'term':term,'story':image,'science':t['canonical_science'],'exact_name':bool(t.get('exact_name_recall')),'hint':image,'name_support':t['name_support']})
        snaps.append({'term':term,'meaning':t['canonical_science'],'image':image})
    qr=b['quick_recall']; cp=bool(qr.get('enabled'))
    hints={
      'U4-L07':'Return to the three-state monitor. The matching ligand binds the center receptor before the receptor changes on its intracellular side.',
      'U4-L11':'Picture the left GDP-bound switch, the center GDP-to-GTP exchange, and the right-side GTP hydrolysis reset.',
      'U4-L12':'Picture the central receptor-channel: ligand binding changes the gate first, and the ion-flow meter on the right changes only afterward.'
    }
    return {
      'scene_index':idx,'locus':b['scene_title'],'locus_id':lid,'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['exact_location']+' — '+b['micro_anchor']+'.',
      'scene_layout':scene_layout(b),'cast':cast_for(b),'continuity_object':J2['continuity_object'],
      'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':beats,'memory_snapshot':snaps,
      'misconception_guards':b['misconception_guards'],'exit_memory':b['exit_memory'],
      'checkpoint':cp,'checkpoint_object_id':b['primary_knowledge_id'],'checkpoint_prompt':qr.get('candidate_prompt','') if cp else '',
      'checkpoint_answer':qr.get('answer','') if cp else '','checkpoint_hint':hints.get(lid,'') if cp else '',
      'next_locus':B[b['causal_transition']['to_locus_id']]['scene_title'] if b['causal_transition']['to_locus_id'] else None,
      'causal_transition':b['causal_transition']['transition_logic']
    }

lids=J2['route']; scenes=[make_scene(lid,i) for i,lid in enumerate(lids)]
journey={
 'palace_id':'U4-J2','palace_name':'Signal Reception Gateway','story_title':'The Gate That Answered Every Knock',
 'tagline':'The membrane gateway is activating for the wrong signals. Repair recognition, receptor location, and receptor mechanism before any intracellular relay can be trusted.',
 'guide':GUIDE,
 'premise':'Messages from Journey 1 are reaching the correct cellular destinations, yet the Signal Reception Gateway has developed a new failure: receptors activate for incompatible ligands, every receptor is being placed at the membrane, and distinct receptor mechanisms have been collapsed into one generic switch. Mira brings a three-state receptor monitor that can show only unbound/inactive, ligand-bound, and activated/changed, forcing every room to prove exactly when and where reception occurs.',
 'mission':'Repair the gateway from recognition to receptor mechanism. Use ligand-receptor specificity to stop false activation, separate cell-surface from intracellular receptors through membrane permeability, examine three intracellular-signaling examples, then keep the GPCR, heterotrimeric G protein, GDP/GTP switch, and ligand-gated ion channel physically and causally distinct.',
 'finale':'At the final channel gate, the receptor monitor advances cleanly only when a compatible ligand reaches the correct receptor and that receptor undergoes its actual mechanism of activation. Intracellular receptors, GPCR signaling, and ligand-gated channels remain visibly different. With reception repaired, a violet downstream route illuminates beyond the membrane and leads directly into Journey 3, where signal transduction must be traced without allowing the original extracellular ligand to masquerade as the intracellular relay.',
 'estimated_minutes':20,'scene_count':len(scenes),'checkpoint_count':sum(bool(s['checkpoint']) for s in scenes),
 'learner_rule':'Read or listen and place yourself in the room before anything moves. Keep left, center, and right fixed. Watch the ligand, receptor, and downstream structure as separate parts, then attach the exact terminology after the mechanism is visible. Quick Recall is optional during first exposure.',
 'route_orientation':'The Signal Reception Gateway is one continuous six-location route built along a plasma-membrane boundary. Begin at the Reception Checkpoint, pass through the Receptor Location Split, move inside to the Intracellular Signal Suite, return to the membrane at the GPCR Receptor Door, follow its cytoplasmic interface into the G-Protein Switchboard, and finish at the Ligand-Gated Channel Gate. The same three-state receptor monitor travels through all six locations while each room preserves its own fixed left, center, and right anchors.',
 'route':route,'scenes':scenes,'student_release':'DEVELOPER_PREVIEW_F4B','narrative_standard':'V2-NARRATIVE-4.1-U4-F4B'
}

(U4/'journeys'/'U4-J2.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def card(j): return {k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
registry={'schema':'memory-palace-v2-unit4-f4b-registry-1.0','course_id':'ap-biology','unit_id':'unit-4','unit_title':'Cell Communication and Cell Cycle','narrative_standard':'V2-NARRATIVE-4.x-U4-F4B','journey_count':2,'scene_count':J1['scene_count']+journey['scene_count'],'checkpoint_count':J1['checkpoint_count']+journey['checkpoint_count'],'guided_journeys':[card(J1),card(journey)]}
(U4/'journeys-f4b.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U4/'status-f4a.json').read_text(encoding='utf-8'))
status.update({'status':'F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','pipeline_status':'POLISHED_NARRATIVE_F4B','narrative_lock':'LOCKED_F4B_J1_J2','student_release':False,'preview_release':True,'journey_count':2,'scene_count':12,'polished_journeys':2,'polished_scenes':12,'polished_checkpoint_count':5,'narrative_story_files':2,'next_required_output':'F4C polished narrative for Journey 3 only after F4B prose QA; Journeys 1–2 remain locked unchanged'})
(U4/'status-f4b.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(U4/'status.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; course=json.loads(cp.read_text(encoding='utf-8'))
for u in course['units']:
    if u['unit_id']=='unit-4':
        u.update({'status':'F4B_JOURNEYS1_2_POLISHED_DEVELOPER_PREVIEW','journey_count':2,'scene_count':12,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEYS1_2_POLISHED_F4B','polished_journeys':2,'polished_scenes':12,'student_release':False,'preview_release':True,'canonical_records':180})
cp.write_text(json.dumps(course,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

files=['journeys/U4-J1.json','journeys/U4-J2.json','journeys-f4b.json','status-f4b.json']
lock={'schema':'memory-palace-v2-unit4-f4b-content-lock-1.0','unit_id':'unit-4','stage':'F4B','lock_status':'LOCKED_F4B_J1_J2','student_release':False,'preview_release':True,'protected_predecessor':{'journeys/U4-J1.json':expected_j1},'files':{f:{'bytes':(U4/f).stat().st_size,'sha256':sha(U4/f)} for f in files}}
(U4/'content-lock-f4b.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit4-f4b-release-manifest-1.0','unit_id':'unit-4','stage':'F4B','student_release':False,'preview_release':True,'canonical_records_protected':180,'polished_journeys':2,'polished_scenes':12,'journey_1_records':sum(len(s['object_ids']) for s in J1['scenes']),'journey_2_records':sum(len(s['object_ids']) for s in scenes),'journey_2_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'journey_2_narrative_words':sum(len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs']))) for s in scenes),'next_stage':'F4C_JOURNEY3_AFTER_F4B_QA'}
(U4/'f4b-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')

# Human-readable narrative review artifact.
doc=['# Unit 4 F4B · Journey 2 Narrative','',f"## {journey['story_title']}",'',journey['tagline'],'',f"**Guide**  {GUIDE['name']}, {GUIDE['role']}",'',f"**Premise**  {journey['premise']}",'',f"**Mission**  {journey['mission']}",'',f"**Route**  {' → '.join(r['locus'] for r in route)}",'', '> F4B is a developer narrative preview. Unit 4 remains `student_release: false`. Journey 1 is protected byte-for-byte from F4A; this artifact exists to evaluate Journey 2 spatial clarity, scientific mechanism, continuity, and prose quality before Journey 3 is authored.','']
for s in scenes:
    doc += [f"## {s['scene_index']+1}. {s['locus']}",'',f"### {s['title']}",'',f"*{s['scene_kicker']}*",'',f"**Physical layout**  {s['scene_layout']['orientation']}",'']
    for p in s['story_paragraphs']: doc += [p,'']
    doc += [f"**Exit**  {s['story_close']}",'']
    if s['checkpoint']: doc += [f"**Optional Quick Recall**  {s['checkpoint_prompt']}",'']
doc += ['## Journey payoff','',journey['finale'],'']
(ROOT/'docs'/'UNIT4_F4B_JOURNEY2_STORY.md').write_text('\n'.join(doc),encoding='utf-8')

release_doc=f'''# Unit 4 F4B Release

## Scope

F4B adds only **Journey 2, Signal Reception Gateway**. Journey 1 remains protected byte-for-byte from F4A. F1 science, F2 architecture, and F3 scene briefs remain locked. Journeys 3–7 are not polished in this stage.

## Narrative release

- Journey 2 title: **{journey['story_title']}**
- Polished journeys: **2 / 7**
- Polished scenes: **12 / 51**
- Journey 2 knowledge records: **{manifest['journey_2_records']}**
- Journey 2 narrative words: **{manifest['journey_2_narrative_words']}**
- Journey 2 optional first-exposure recalls: **{manifest['journey_2_checkpoints']}**
- Student release: **false**
- Developer preview: **true**

## Narrative standard

The same three-state receptor monitor travels through all six Journey 2 locations. Every room preserves F3 left/center/right geography and uses the biological mechanism itself as the memorable event. Ligand, receptor, target cell, GPCR, G protein, nucleotide switch, effector, and ion channel remain separate structures with separate jobs.

## Next gate

F4C may author **Journey 3, Signal Relay Tower** only after F4B passes prose QA. Journeys 1 and 2 must remain unchanged.
'''
(ROOT/'docs'/'UNIT4_F4B_RELEASE.md').write_text(release_doc,encoding='utf-8')
print('Built Unit 4 F4B',json.dumps(manifest,indent=2))
