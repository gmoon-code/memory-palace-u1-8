from __future__ import annotations
import json, hashlib, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content'/'ap-biology'/'unit-4'
F3=json.loads((U4/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS=json.loads((U4/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J3=next(j for j in JBRIEFS if j['journey_id']=='U4-J3')
B={b['locus_id']:b for b in F3 if b['journey_id']=='U4-J3'}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# F4C extends F4B. Journeys 1 and 2 are protected predecessors and are never regenerated here.
LOCK_B=json.loads((U4/'content-lock-f4b.json').read_text(encoding='utf-8'))
J1_PATH=U4/'journeys'/'U4-J1.json'; J2_PATH=U4/'journeys'/'U4-J2.json'
for rel,p in [('journeys/U4-J1.json',J1_PATH),('journeys/U4-J2.json',J2_PATH)]:
    if not p.exists(): raise RuntimeError(f'F4C requires locked predecessor {rel}')
    expected=LOCK_B['files'][rel]
    if p.stat().st_size!=expected['bytes'] or sha(p)!=expected['sha256']:
        raise RuntimeError(f'F4C refuses to proceed because locked predecessor changed: {rel}')
J1=json.loads(J1_PATH.read_text(encoding='utf-8')); J2=json.loads(J2_PATH.read_text(encoding='utf-8'))

GUIDE={
 'name':'Dr. Mira Chen','role':'cellular-systems investigator',
 'visual':'charcoal field jacket, clear protective glasses, and a compact white tablet with a thin violet tracing light projected from one edge',
 'story_job':'Mira keeps the extracellular ligand, activated receptor, intracellular relay components, and response machinery physically separate. The violet light marks information flow only when a real pathway component changes state.'
}
TRACE={
 'name':'Violet information trace','kind':'non-molecular visualization overlay',
 'visual':'a thin violet line projected across the floor and molecular models; it never occupies a binding site or replaces a biological molecule',
 'job':'marks where signaling information has reached after an actual receptor, protein, enzyme, second messenger, or response component changes state; it is never treated as material moving through the pathway'
}

route=[
 {'scene_index':0,'locus':'Transduction Relay Map','short':'Relay map','floor':'Tower base','symbol':'↝'},
 {'scene_index':1,'locus':'Kinase–Phosphatase Switchboard','short':'Phosphate switch','floor':'Control floor','symbol':'P'},
 {'scene_index':2,'locus':'Phosphorylation Cascade Staircase','short':'Cascade','floor':'Relay stair','symbol':'P↓'},
 {'scene_index':3,'locus':'Second-Messenger Amplifier','short':'Amplifier','floor':'Amplifier chamber','symbol':'cAMP'},
 {'scene_index':4,'locus':'Cellular Response Dispatch','short':'Responses','floor':'Dispatch floor','symbol':'⇢'},
 {'scene_index':5,'locus':'Mutation Breakpoint Lab','short':'Mutations','floor':'Test lab','symbol':'✕'},
 {'scene_index':6,'locus':'Agonist–Antagonist Console','short':'Chemicals','floor':'Perturbation deck','symbol':'+/−'},
]

ZONE_COPY={
'U4-L13':[
 ('left','Activated receptor input','▥','The activated receptor remains fixed at the membrane on the learner’s left. The extracellular ligand stays outside the cell and does not travel into the tower.'),
 ('center','Signal-transduction pathway','↝','A vertical route map contains a sequence of real intracellular relay components. Each component changes state in order before the violet information trace is allowed to advance.'),
 ('right','Downstream target branch','⇢','A separate downstream target remains inactive until the central relay reaches it, making transduction distinct from both receptor reception and the eventual cellular response.')],
'U4-L14':[
 ('left','Protein kinase and ATP station','ATP→P','A protein kinase receives ATP and transfers a phosphate group to the same target protein used throughout the comparison.'),
 ('center','Target-protein state panel','P?','One target protein is held in the center so its phosphorylated and dephosphorylated states can be compared without assuming either state is universally active.'),
 ('right','Protein phosphatase station','P→','A protein phosphatase removes the phosphate from the center target, reversing the chemical modification while leaving the functional consequence target-dependent.')],
'U4-L15':[
 ('left','Upstream activated kinase','K1','One activated kinase supplies the first input and can act on multiple copies of the next kinase layer.'),
 ('center','Phosphorylation cascade staircase','K1→K2→K3','Several kinase layers rise through the center. Each activated layer phosphorylates downstream proteins so the relay can continue through repeated protein modification.'),
 ('right','Downstream activated targets','•••','Many downstream target molecules remain dark until the staircase reaches them, making relay and possible amplification visible as separate consequences of the cascade.')],
'U4-L16':[
 ('left','Upstream enzyme input','AC','An activated upstream enzyme such as adenylyl cyclase receives a limited input from the preceding signaling step.'),
 ('center','Second-messenger chamber','cAMP × many','The chamber generates many small intracellular cAMP molecules and keeps them physically inside the cell, separate from the extracellular ligand left behind at the receptor.'),
 ('right','Many downstream relay targets','•••••','Multiple downstream targets receive the intracellular messenger, showing how one upstream event can influence many molecules without making any single molecule physically stronger.')],
'U4-L17':[
 ('left','Membrane and metabolic branches','⇅ / ⚙','One branch changes a membrane channel or transporter while another changes the activity of a metabolic enzyme.'),
 ('center','Cellular-response dispatch center','⇢','A central switchyard receives the completed intracellular signal and routes its consequences into distinct cellular processes.'),
 ('right','Gene-expression, phenotype, and apoptosis branches','DNA / cell / apoptosis','Separate response routes change gene expression, contribute to phenotype or function, or trigger regulated apoptosis when the signaling context calls for programmed cell death.')],
'U4-L18':[
 ('left','Receptor-level mutation','✕R','A mutated receptor changes detection or activation before the pathway enters the intracellular relay.'),
 ('center','Signaling pathway breakpoint','│✕│','The complete pathway is laid out as a test bench so the exact point where normal information flow fails or changes can be located.'),
 ('right','Downstream-component and phosphatase defects','✕D / ✕P','A separate downstream mutation leaves reception intact, while a phosphatase defect changes phosphorylation persistence according to the target protein and pathway.')],
'U4-L19':[
 ('left','Pathway-activating chemical input','+','A reversible chemical perturbation increases pathway activity through a defined interaction without altering the DNA sequence.'),
 ('center','Signaling activity readout','▥','A central pathway meter reports the current signaling output after each chemical is applied, washed away, and reset.'),
 ('right','Pathway-inhibiting chemical input','−','A second reversible chemical perturbation decreases pathway activity at a defined receptor or downstream step without requiring a mutation.')],
}

NARR={
'U4-L13':{
 'title':'The Light That Refused to Leave the Receptor','kicker':'Reception is working, yet the tower still cannot relay the information inward without confusing the message with the messenger.',
 'paragraphs':[
  "The Ligand-Gated Channel Gate from the previous journey opens onto the **base of the Signal Relay Tower**, a tall cylindrical chamber whose floors are visible through a hollow central shaft. Before you move, the room fixes itself around three landmarks. On your **left**, the activated receptor from the repaired gateway is embedded in a vertical strip of plasma membrane. The ligand is still attached on the extracellular face, visibly outside the cell. Directly **ahead**, a dark route map climbs through the center of the tower, with several intracellular relay proteins arranged like stations on a vertical line. On your **right**, a downstream target branch waits behind a clear panel. Nothing there has changed. Mira stands beside the receptor and projects a hair-thin violet line from her tablet. The line stops at the receptor and refuses to climb.",
  "Mira points first to the ligand outside the membrane. It has completed its job in reception by binding the receptor. She does not move it. Then she touches the activated receptor on its cytoplasmic side, and the first intracellular relay protein changes state. Only after that real molecular change does the violet line extend from the receptor to the first relay station. A second protein interacts with the first and changes state, so the line advances again. Then a third component changes. The violet trace climbs one step at a time, always after the biology has changed. Mira names the process **transduction**. Signal transduction converts information from receptor activation into intracellular molecular changes that can produce a cellular response.",
  "The central route is now alive, yet the ligand remains visibly stranded on the left side of the membrane. Mira taps the violet line with two fingers. It is a tracing overlay, not a molecule. It marks where information has reached. The actual relay is carried by changes in the states and interactions of pathway components. The ordered sequence of those interacting molecular components is a **signal transduction pathway**. The route begins with information from an activated receptor and passes that information to intracellular targets. You can therefore point to three separate stages without letting one term swallow the others. Reception occurred at the receptor on the left. Transduction is happening through the center. A cellular response will occur only when downstream cellular machinery actually changes.",
  "Mira opens a branch in the center map. One relay component can feed a downstream target on the right while another branch continues upward through the tower. The right-hand target changes only when the route reaches it. This makes the pathway a causal chain rather than a glowing tunnel. If the first relay component never changes state, the violet trace stops there. If the second changes, the trace can advance. The line therefore cannot jump over a broken step or drift into the cytoplasm on its own. The route map finally reports a clean sequence from activated receptor to intracellular relay to downstream target.",
  "The newly lit target immediately sends a narrow cable into the next floor. At the top of the cable sits a single protein whose state can be changed by adding or removing a phosphate group. Two opposite workstations face it. Mira retracts the violet trace until it rests on the cable. The tower has proved that information can move without the ligand moving. Now it must show how one of its most common reversible protein-control mechanisms actually works."
 ],
 'close':'The relay map now separates reception from transduction and response. The first control cable rises directly into the Kinase–Phosphatase Switchboard, where one target protein waits between phosphate addition and phosphate removal.'
},
'U4-L14':{
 'title':'One Protein Between Two Opposite Hands','kicker':'A phosphate can be added or removed reversibly, yet neither chemical action carries a universal meaning of on or off.',
 'paragraphs':[
  "You climb one short flight into the **Kinase–Phosphatase Switchboard**. The room is narrow enough that all three stations fit in one glance. On your **left**, a protein kinase sits beside an ATP rack and a bright phosphate-transfer arm. Directly **ahead**, the same target protein is held in a transparent state panel so every change to it remains visible. On your **right**, a protein phosphatase waits beside a phosphate-removal tray. Mira places the violet information trace along the floor from the previous relay cable to the center target, then locks the trace in place. It cannot move again until one of the two enzymes performs a real chemical action.",
  "Mira sends the target protein to the left station first. ATP binds at the kinase station, and the enzyme transfers a phosphate group from ATP to the target protein. The center panel now marks the protein as phosphorylated and shows that its functional state has changed. Mira names the enzyme a **protein kinase**. A protein kinase transfers a phosphate group, usually from ATP, to a target protein. The chemistry is precise. A phosphate has been added. The effect on activity depends on the target protein. On this demonstration target, the phosphorylated state happens to increase one activity meter, yet a second comparison target beside it shows phosphorylation decreasing activity. Mira leaves both meters visible so the word phosphorylation never becomes a synonym for activation.",
  "The same target moves across the center panel to the station on your right. The **protein phosphatase** removes the phosphate group. This removal is **dephosphorylation**. The phosphate appears in the removal tray, and the target protein changes state again. Mira runs the same two-target comparison in reverse. One protein becomes less active when dephosphorylated, while another becomes more active. The chemical contrast stays stable even though the functional outcomes differ. Kinase adds phosphate. Phosphatase removes phosphate. Phosphorylation and dephosphorylation change protein state or activity according to the specific target and pathway.",
  "Mira now positions both enzymes on opposite sides of the center protein and cycles the target back and forth. ATP supplies the phosphate donor for the kinase reaction on the left. The phosphatase reverses the modification on the right. The center panel records the target's current phosphorylation state but refuses to label either state universally ON or OFF. The violet trace advances only when the target's state change affects the next relay component. This makes reversible phosphorylation a controllable molecular switch without turning phosphate into a magic activation sticker.",
  "A small staircase unfolds from the back of the target-protein panel. The top step carries one activated kinase. Below it sit rows of inactive kinase molecules waiting to be modified. Mira looks up the staircase and then back at the single target you just followed. One reversible switch is now clear. The tower's next problem is scale. The same type of modification has to be repeated across several relay layers without losing track of who acts on whom."
 ],
 'close':'The single reversible switch is repaired. Its output becomes the first step of the Phosphorylation Cascade Staircase, where one activated kinase can modify multiple downstream proteins.'
},
'U4-L15':{
 'title':'The Staircase That Multiplied the Relay','kicker':'Repeated phosphorylation can pass information through several protein layers and can increase the number of downstream molecules affected.',
 'paragraphs':[
  "The **Phosphorylation Cascade Staircase** rises through the middle of the tower like a wide spiral stair built from three molecular landings. On your **left**, one upstream activated kinase stands on a small starting platform. Directly **ahead**, the staircase contains rows of kinase molecules arranged in successive levels. On your **right**, a bank of downstream target proteins remains dark. The activated receptor from below is still visible through the central shaft, far beneath you. The extracellular ligand is even farther outside the membrane. Mira stretches the violet trace from the left starting kinase to the first central landing and stops it there.",
  "The upstream kinase acts on several copies of the next kinase layer. Each target kinase receives a phosphate group and changes state. The violet trace does not become several new molecules. It splits into several thin projected branches only to show that information has reached multiple real proteins. Those newly activated kinases then phosphorylate proteins on the next landing. The relay repeats. Mira calls this a **phosphorylation cascade**, a series in which activated protein kinases phosphorylate downstream proteins, allowing the signal to be relayed through several molecular steps and often amplified along the way.",
  "You can now see why the broader phrase **protein modification and phosphorylation cascades** belongs here. Many signal transduction pathways depend on protein modifications, and phosphorylation is a common reversible modification used in cascades. Each stair does real chemistry to the next protein. The pathway does not advance because the violet trace flows downhill. The trace advances because an activated kinase changes the state of downstream proteins. Mira briefly turns the overlay off, leaving only the actual kinases and phosphate marks. The biological sequence remains completely readable without the visual aid.",
  "At the final landing, several activated kinases act on many downstream targets on your right. The output is larger than the single kinase input at the beginning. Mira marks this as one possible source of amplification, while keeping the concepts separate. A phosphorylation cascade describes the multi-step kinase relay. **Signal amplification** describes the increase in the number of activated downstream molecules or events. A cascade can contribute to amplification, yet the two phrases do not mean the same thing.",
  "The downstream targets illuminate a circular door at the top of the stairs. Beyond it is a chamber whose center contains no staircase at all. Instead, one upstream enzyme faces a reservoir that can suddenly fill with hundreds of small intracellular molecules. Mira follows the violet trace to the threshold. Protein relays are only one way to move information inside a cell. The next room will use a small intracellular messenger and make amplification impossible to miss."
 ],
 'close':'The staircase now relays information through repeated protein modification. Its amplified output opens the Second-Messenger Amplifier, where one upstream event can generate many intracellular messenger molecules.'
},
'U4-L16':{
 'title':'One Input, a Chamber Full of cAMP','kicker':'A small intracellular second messenger can spread information from an upstream signaling event to many downstream targets.',
 'paragraphs':[
  "The door opens into the round **Second-Messenger Amplifier**, a chamber with three unmistakable zones. On your **left**, an upstream enzyme station is built into the inner face of the membrane. The label ADENYLYL CYCLASE sits above it as a concrete example of an enzyme that can be activated by an upstream signaling step. Directly **ahead**, a clear cylindrical vessel fills the center of the room. It is empty at first. On your **right**, dozens of downstream relay targets are arranged in rows. Through a small window behind you, the original extracellular ligand is still visible at the receptor far below. It never enters this chamber.",
  "Mira lets the violet information trace reach the left enzyme only after that upstream component changes state. She gives the enzyme a limited activating input. The central vessel immediately begins producing many small molecules. Each has the same ring-shaped molecular label, cAMP. Mira waits until the vessel contains a dense cloud before naming the class. A **second messenger** is a small intracellular molecule or ion that relays information from an activated receptor or an upstream signaling component to downstream targets. The messenger here is **cyclic AMP**, written **cAMP**, short for **cyclic adenosine monophosphate**. It is generated inside the cell. It is therefore physically and conceptually different from the extracellular ligand that initiated reception.",
  "The chamber opens ports toward the right-hand target bank. Many cAMP molecules distribute to downstream signaling targets. One upstream event has now influenced many intracellular components. Mira names this **signal amplification**. Amplification occurs when activation of one signaling component leads to activation of many downstream molecules or events, increasing the magnitude of the intracellular response. Nothing about an individual cAMP molecule has become stronger. The increased magnitude comes from number and branching. One upstream input has produced many intracellular messengers, and those messengers can affect many downstream targets.",
  "Mira resets the chamber and runs the whole route more slowly. The receptor-level event occurs upstream. An enzyme participates in the intracellular relay. Many cAMP molecules appear. Downstream targets change state. This is why **enzymes and second messengers** can relay and amplify intracellular signals. She then switches on a side panel labeled RELAY, AMPLIFICATION, RESPONSE. The first two lights are active, while RESPONSE remains dark. **Relay, amplification, and response** are connected stages or properties of signaling, yet a larger internal signal is still incomplete until some cellular process actually changes.",
  "The right-hand target bank now sends several thick conduits through the wall. One turns downward toward membrane channels. Another enters a room filled with metabolic enzymes. A third heads toward the nucleus. A fourth narrow route ends at a regulated cell-death symbol. Mira drains the central cAMP vessel and leaves one molecule under glass as a reference. The amplifier is repaired. Its output has somewhere to go, and the next floor is built to show how different cellular responses can emerge from signaling information."
 ],
 'close':'The cAMP chamber now separates extracellular ligand from intracellular second messenger and makes amplification visible as multiplication of downstream events. Its output conduits lead into Cellular Response Dispatch.'
},
'U4-L17':{
 'title':'The Same Signal Reaches Different Cellular Workrooms','kicker':'Transduction ends in changes to real cellular processes, from transport and metabolism to gene expression, phenotype, or regulated cell death.',
 'paragraphs':[
  "You enter **Cellular Response Dispatch**, the widest floor in the tower. Its fixed geometry is drawn directly into the floor. On your **left**, two short branches lead to a membrane-transport panel and a metabolic-enzyme bench. Directly **ahead**, the central dispatch table receives the completed signaling input from the amplifier below. On your **right**, three longer branches lead toward a nuclear gene-expression room, a whole-cell phenotype display, and a quiet chamber marked PROGRAMMED CELL DEATH. Mira lays the violet trace across the center table but keeps every branch dark until a specific cellular process changes.",
  "She routes the completed signal left first. At the membrane branch, a channel or transport protein changes state, altering the movement of material across the membrane. Mira names this a **membrane-permeability response**. Signaling pathways can change membrane permeability by modifying channels or transport proteins. The violet trace then returns to the central table and enters the metabolic branch. An enzyme changes activity, altering the rate of a metabolic process. This is a **metabolic response**. The response is the change in cellular activity, not the path of the information trace itself.",
  "Mira resets the table and sends the same upstream signaling input toward the right. A regulatory protein reaches the nuclear branch and changes transcriptional activity. That change is a **gene-expression response**. Signaling pathways can activate or repress proteins that regulate transcription and therefore change gene expression. The dispatch table now labels the broader idea **cellular response**. A cellular response is the change in cell activity produced by a signaling pathway, such as altered membrane transport, enzyme activity, secretion, growth, or gene expression. Reception detected the signal. Transduction relayed the information. Response is what the cell actually does differently.",
  "The gene-expression branch remains active long enough for the whole-cell display beside it to change. Cell shape, protein abundance, and functional behavior shift together. Mira identifies this as a **phenotypic signaling outcome**. Sustained changes in signaling can alter gene expression and cellular function, so they can alter phenotype. She places a card beside the whole display reading **signal response changes phenotype/function**. The phrase refers to an integrated consequence of molecular changes. Phenotype is not another messenger traveling down the pathway. It is what becomes different about the cell as signaling changes cellular processes.",
  "Finally, Mira activates the quiet chamber at the far right under an appropriate damage-related signaling condition. The cell begins an orderly programmed dismantling process. She names **apoptosis as a signaling outcome**. Programmed cell death can be triggered by signaling pathways in developmental or damage-related contexts. Apoptosis is therefore one possible cellular response, not the definition of response itself. Mira keeps the membrane, metabolic, gene-expression, phenotype, and apoptosis branches separate so each outcome retains its own mechanism and scale.",
  "All five routes now respond normally, which gives Mira the baseline she needs for a harsher test. She copies the complete pathway onto a rolling transparent bench and wheels it through a door labeled BREAKPOINT LAB. If a mutation changes the receptor, the relay, or a regulatory enzyme, the position of the failure should reveal what kind of component has been altered."
 ],
 'close':'The dispatch floor now shows what a cellular response actually is. With normal outputs established, the same pathway moves intact into the Mutation Breakpoint Lab so altered signaling can be localized instead of guessed.'
},
'U4-L18':{
 'title':'Find the Break Before You Blame the Whole Pathway','kicker':'Mutations at different pathway levels create different patterns, so the location of the breakpoint matters.',
 'paragraphs':[
  "The **Mutation Breakpoint Lab** is arranged around one full-length signaling pathway mounted under glass. On your **left**, a receptor model is fixed in the membrane with a small mutation marker attached to one of its domains. Directly **ahead**, the normal signaling pathway runs through the center bench from receptor to response, with every relay component individually numbered. On your **right**, a downstream relay protein and a protein phosphatase sit in separate mutation bays. Mira projects the violet trace along the normal pathway once so you have a baseline, then turns it off. The lab will now introduce one alteration at a time.",
  "First, Mira changes the receptor on the left while leaving every downstream component normal. Depending on the altered domain, ligand binding, receptor activation, membrane behavior, or communication with intracellular signaling components can change. The fault occurs at reception, so downstream output changes even though the downstream machinery itself is intact. Mira labels this a **receptor mutation effect**. A receptor mutation can alter whether and how the pathway responds by changing ligand-binding, membrane, or intracellular signaling domains. The violet trace stops or behaves abnormally at the receptor because the first relevant state transition has changed.",
  "She resets the receptor and instead changes one numbered relay component in the center-right portion of the pathway. Ligand binding and receptor activation now occur normally. The trace reaches the mutated component and then fails to propagate correctly beyond that point. This is a **downstream-component mutation effect**. Mutations in intracellular signaling components can change propagation, amplification, termination, or output even when ligand binding is normal. Mira places the two trials side by side. One breaks the pathway at reception. The other breaks it after reception. Together they demonstrate the broader rule that **mutations alter signaling** when receptor domains or other pathway components are changed.",
  "The final mutation bay targets the phosphatase on your right. Mira disables its normal function and watches phosphorylated pathway proteins persist longer than they did in the baseline run. She refuses to label the outcome automatically MORE SIGNALING. The correct **defective phosphatase prediction** depends on the particular phosphorylated target. A defective phosphatase can prolong or alter phosphorylation states, while the functional consequence depends on whether those phosphorylated targets are active or inactive in that pathway. The chemistry is phosphate removal. The pathway meaning remains target-specific.",
  "Mira restores the original DNA sequence in every model and reruns the pathway. Normal signaling returns. Then she points to a neighboring console with two chemical reservoirs. “A pathway can also be perturbed without changing DNA,” she says. One reservoir is labeled ACTIVATE and the other INHIBIT. Because the mutation experiments established permanent genetic alterations at defined breakpoints, the next test can cleanly compare them with reversible chemical effects on the same signaling machinery."
 ],
 'close':'The lab now distinguishes receptor mutations, downstream mutations, and target-dependent phosphatase defects by where normal information flow changes. The intact pathway slides next into the Agonist–Antagonist Console for reversible chemical perturbation.'
},
'U4-L19':{
 'title':'Change the Pathway Without Rewriting the DNA','kicker':'Chemicals can increase or decrease signaling by interacting with pathway components, and the effect can be reversible without a mutation.',
 'paragraphs':[
  "The final floor is the **Agonist–Antagonist Console**, a clean perturbation deck built around the same pathway model from the mutation lab. On your **left**, a reservoir contains a pathway-activating chemical input. Directly **ahead**, a tall signaling-activity readout reports receptor state, relay activity, and final output on one continuous scale. On your **right**, a second reservoir contains a pathway-inhibiting chemical input. The DNA sequence display above the pathway is locked and unchanged. Mira runs one untreated baseline while the violet trace moves through the normal pathway and the activity meter settles at its reference level.",
  "She applies the left-hand chemical at a defined signaling component. Pathway activity rises above baseline. No DNA sequence changes. Mira washes the chemical away, resets the system, and the activity meter returns toward its original state. She then applies the right-hand chemical at a defined receptor or downstream step. Pathway activity falls. Again, the DNA sequence remains unchanged. These trials demonstrate that **chemicals activate or inhibit pathways** when they interact with signaling components in ways that alter pathway activity.",
  "Mira names the more specific comparison **chemical pathway agonism/antagonism**. A chemical that binds or modifies a signaling-pathway component can increase or decrease pathway activity depending on its interaction. An agonistic or activating effect raises the relevant pathway activity in this test. An antagonistic or inhibitory effect reduces it. The labels describe functional effects in the defined system. They do not require that every chemical bind the receptor, and they do not imply a mutation has occurred.",
  "For the final comparison, Mira places the mutation-lab results beside the chemical trials. The receptor mutation remained present until the genetic model was restored. The downstream mutation likewise followed the altered component. The chemical perturbations could be applied, removed, and reapplied while the DNA display stayed unchanged. You can now diagnose a pathway by asking where normal information flow changes, whether the altered state persists as a genetic change or follows a chemical exposure, and whether the measured output rises or falls.",
  "Mira turns off every display except the violet information trace. It begins at an activated receptor, then stops. She looks at you and waits. You reconstruct the tower in order. **Transduction** relays information through intracellular molecular changes. Kinases add phosphate and phosphatases remove it. A phosphorylation cascade can relay through multiple protein layers. A **second messenger** such as **cAMP** can spread and amplify an intracellular signal. A **cellular response** changes what the cell actually does. Mutations can alter signaling at distinct breakpoints, and chemicals can activate or inhibit pathway components without changing DNA. Only after the sequence is complete does Mira allow the violet trace to climb through all seven floors. The ligand remains outside the membrane exactly where the journey began."
 ],
 'close':'The Signal Relay Tower is repaired. The learner can now follow information from receptor activation through intracellular relay, amplification, response, genetic breakpoints, and reversible chemical perturbation without turning the extracellular ligand into the intracellular signal.'
}
}

TERM_IMAGES={
'U4-K-068':'the violet information trace advancing only after real intracellular relay components change state while the ligand remains outside the membrane',
'U4-K-069':'the center tower map containing an ordered sequence of interacting intracellular molecular components from activated receptor to target',
'U4-K-070':'the left kinase station transferring a phosphate group from ATP to the center target protein',
'U4-K-072':'the right phosphatase station removing the phosphate from the same center target protein',
'U4-K-073':'the phosphate leaving the target protein at the right-side phosphatase station',
'U4-K-005':'multiple protein layers in the staircase changing state through repeated phosphorylation',
'U4-K-071':'the center kinase staircase where one activated layer phosphorylates downstream kinase layers',
'U4-K-010':'the route panel separating intracellular relay, multiplication of downstream events, and the eventual cellular response',
'U4-K-012':'the upstream enzyme generating many intracellular cAMP molecules that carry information to downstream targets',
'U4-K-074':'one upstream event producing many downstream activated molecules or events across the amplifier chamber',
'U4-K-075':'small intracellular messenger molecules carrying information from an upstream signaling step to downstream targets',
'U4-K-076':'the central vessel filled with cyclic adenosine monophosphate, cAMP, generated inside the cell',
'U4-K-015':'the whole-cell phenotype display changing after signaling alters gene expression and cell function',
'U4-K-077':'the dispatch center routing a completed signaling input into a real change in cell activity',
'U4-K-078':'the left membrane branch changing a channel or transporter and therefore membrane permeability or transport',
'U4-K-079':'the left metabolic bench changing enzyme activity and metabolic output',
'U4-K-080':'the right nuclear branch changing transcriptional regulation and gene expression',
'U4-K-088':'the whole-cell display showing sustained signaling changes reflected in phenotype or function',
'U4-K-089':'the separate programmed-cell-death chamber carrying out regulated apoptosis as one signaling outcome',
'U4-K-016':'the complete pathway test bench showing that changes in receptor or relay components alter downstream signaling',
'U4-K-090':'the left receptor mutation changing detection or receptor activation before the intracellular relay',
'U4-K-091':'the downstream mutation allowing normal reception before the information trace breaks later in the pathway',
'U4-K-093':'the defective phosphatase allowing altered phosphorylation states to persist with target-dependent functional consequences',
'U4-K-017':'the activity meter rising or falling after reversible chemicals interact with signaling components',
'U4-K-092':'the left activating chemical and right inhibiting chemical producing opposite pathway effects without changing DNA'
}

HINTS={
'U4-L14':'Picture one target protein between two enzyme stations. The left enzyme transfers phosphate from ATP; the right enzyme removes phosphate.',
'U4-L16':'Keep the extracellular ligand at the membrane. Inside the amplifier, the central vessel fills with cAMP, a small intracellular messenger.',
'U4-L18':'Find the first abnormal point. A receptor mutation changes reception; a downstream mutation leaves reception normal and breaks the pathway later.'
}

def scene_layout(b):
    zones=[]
    for pos in ('left','center','right'):
        label,symbol,desc=next((x[1],x[2],x[3]) for x in ZONE_COPY[b['locus_id']] if x[0]==pos)
        zones.append({'position':pos,'label':label,'symbol':symbol,'description':desc})
    return {'orientation':f"On your left is {zones[0]['label']}. Directly ahead is {zones[1]['label']}. On your right is {zones[2]['label']}. These anchors stay fixed while the mechanism runs.", 'zones':zones}

def cast_for(b):
    casts=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    for part in b['stable_cast']:
        casts.append({'name':part['name'],'kind':part['type'].lower(),'visual':part['visual_identity'],'job':part['job_in_scene']})
    casts.append(dict(TRACE))
    return casts

def make_scene(lid,idx):
    b=B[lid]; n=NARR[lid]
    beats=[]; snaps=[]
    for t in b['term_introductions']:
        term=t['canonical_term']; image=TERM_IMAGES[t['knowledge_id']]
        beats.append({'object_id':t['knowledge_id'],'term':term,'story':image,'science':t['canonical_science'],'exact_name':bool(t.get('exact_name_recall')),'hint':image,'name_support':t['name_support']})
        snaps.append({'term':term,'meaning':t['canonical_science'],'image':image})
    qr=b['quick_recall']; cp=bool(qr.get('enabled'))
    return {
      'scene_index':idx,'locus':b['scene_title'],'locus_id':lid,'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['exact_location']+' — '+b['micro_anchor']+'.',
      'scene_layout':scene_layout(b),'cast':cast_for(b),'continuity_object':J3['continuity_object'],
      'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':beats,'memory_snapshot':snaps,
      'misconception_guards':b['misconception_guards'],'exit_memory':b['exit_memory'],
      'checkpoint':cp,'checkpoint_object_id':b['primary_knowledge_id'],'checkpoint_prompt':qr.get('candidate_prompt','') if cp else '',
      'checkpoint_answer':qr.get('answer','') if cp else '','checkpoint_hint':HINTS.get(lid,'') if cp else '',
      'next_locus':B[b['causal_transition']['to_locus_id']]['scene_title'] if b['causal_transition']['to_locus_id'] else None,
      'causal_transition':b['causal_transition']['transition_logic']
    }

lids=J3['route']; scenes=[make_scene(lid,i) for i,lid in enumerate(lids)]
journey={
 'palace_id':'U4-J3','palace_name':'Signal Relay Tower','story_title':'The Tower That Lost the Signal Without Losing the Ligand',
 'tagline':'The receptor receives correctly, yet the intracellular tower relays, amplifies, and terminates signals inconsistently. Trace information through real molecular state changes and find every breakpoint.',
 'guide':GUIDE,
 'premise':'Reception is repaired, but the intracellular Signal Relay Tower is failing. Some receptor inputs vanish before reaching a target, some are multiplied into excessive downstream activity, and other routes persist after mutations or chemical perturbations. Mira brings one thin violet information trace that can advance only when an actual pathway component changes state. The trace is never a molecule, and the extracellular ligand remains at the receptor throughout the journey.',
 'mission':'Repair the tower from transduction to response. Keep receptor activation separate from intracellular relay, use kinase and phosphatase chemistry correctly, follow a phosphorylation cascade, distinguish an intracellular second messenger from the extracellular ligand, make amplification visible as multiplication of downstream events, route signaling into distinct cellular responses, and diagnose mutation versus chemical perturbation by where and how pathway activity changes.',
 'finale':'At the final console, the same pathway can be reconstructed from activated receptor through transduction, reversible phosphorylation, cascading protein modification, cAMP-mediated second-messenger signaling, amplification, and a defined cellular response. Receptor and downstream mutations produce distinguishable breakpoints, chemical inputs reversibly increase or decrease pathway activity without rewriting DNA, and the extracellular ligand remains outside the cytoplasmic relay. The repaired tower can now hand a correctly regulated output to the feedback systems of Journey 4.',
 'estimated_minutes':24,'scene_count':len(scenes),'checkpoint_count':sum(bool(s['checkpoint']) for s in scenes),
 'learner_rule':'Read or listen and fix the room in your mind before the relay moves. Keep left, center, and right stable. The violet trace is only an information overlay. Watch the actual molecular component change state first, then attach the scientific term. Quick Recall is optional during first exposure.',
 'route_orientation':'The Signal Relay Tower is one continuous seven-location climb. Begin at the Transduction Relay Map on the tower base, move upward through the Kinase–Phosphatase Switchboard and Phosphorylation Cascade Staircase, enter the Second-Messenger Amplifier, branch through Cellular Response Dispatch, carry the same pathway into the Mutation Breakpoint Lab, and finish at the Agonist–Antagonist Console. The violet information trace travels with Mira through all seven locations but advances only after a real biological state change.',
 'route':route,'scenes':scenes,'student_release':'DEVELOPER_PREVIEW_F4C','narrative_standard':'V2-NARRATIVE-4.2-U4-F4C'
}

(U4/'journeys'/'U4-J3.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def card(j): return {k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
registry={'schema':'memory-palace-v2-unit4-f4c-registry-1.0','course_id':'ap-biology','unit_id':'unit-4','unit_title':'Cell Communication and Cell Cycle','narrative_standard':'V2-NARRATIVE-4.x-U4-F4C','journey_count':3,'scene_count':J1['scene_count']+J2['scene_count']+journey['scene_count'],'checkpoint_count':J1['checkpoint_count']+J2['checkpoint_count']+journey['checkpoint_count'],'guided_journeys':[card(J1),card(J2),card(journey)]}
(U4/'journeys-f4c.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U4/'status-f4b.json').read_text(encoding='utf-8'))
status.update({'status':'F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','pipeline_status':'POLISHED_NARRATIVE_F4C','narrative_lock':'LOCKED_F4C_J1_J2_J3','student_release':False,'preview_release':True,'journey_count':3,'scene_count':19,'polished_journeys':3,'polished_scenes':19,'polished_checkpoint_count':8,'narrative_story_files':3,'next_required_output':'F4D polished narrative for Journey 4 only after F4C prose QA; Journeys 1–3 remain locked unchanged'})
(U4/'status-f4c.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(U4/'status.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; course=json.loads(cp.read_text(encoding='utf-8'))
for u in course['units']:
    if u['unit_id']=='unit-4':
        u.update({'status':'F4C_JOURNEYS1_3_POLISHED_DEVELOPER_PREVIEW','journey_count':3,'scene_count':19,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEYS1_3_POLISHED_F4C','polished_journeys':3,'polished_scenes':19,'student_release':False,'preview_release':True,'canonical_records':180})
cp.write_text(json.dumps(course,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

files=['journeys/U4-J1.json','journeys/U4-J2.json','journeys/U4-J3.json','journeys-f4c.json','status-f4c.json']
lock={'schema':'memory-palace-v2-unit4-f4c-content-lock-1.0','unit_id':'unit-4','stage':'F4C','lock_status':'LOCKED_F4C_J1_J2_J3','student_release':False,'preview_release':True,'protected_predecessors':{'journeys/U4-J1.json':LOCK_B['files']['journeys/U4-J1.json'],'journeys/U4-J2.json':LOCK_B['files']['journeys/U4-J2.json']},'files':{f:{'bytes':(U4/f).stat().st_size,'sha256':sha(U4/f)} for f in files}}
(U4/'content-lock-f4c.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit4-f4c-release-manifest-1.0','unit_id':'unit-4','stage':'F4C','student_release':False,'preview_release':True,'canonical_records_protected':180,'polished_journeys':3,'polished_scenes':19,'journey_1_records':sum(len(s['object_ids']) for s in J1['scenes']),'journey_2_records':sum(len(s['object_ids']) for s in J2['scenes']),'journey_3_records':sum(len(s['object_ids']) for s in scenes),'journey_3_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'journey_3_narrative_words':sum(len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs']))) for s in scenes),'next_stage':'F4D_JOURNEY4_AFTER_F4C_QA'}
(U4/'f4c-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')

# Human-readable narrative artifact.
doc=['# Unit 4 F4C · Journey 3 Narrative','',f"## {journey['story_title']}",'',journey['tagline'],'',f"**Guide**  {GUIDE['name']}, {GUIDE['role']}",'',f"**Premise**  {journey['premise']}",'',f"**Mission**  {journey['mission']}",'',f"**Route**  {' → '.join(r['locus'] for r in route)}",'', '> F4C is a developer narrative preview. Unit 4 remains `student_release: false`. Journeys 1 and 2 are protected byte-for-byte from F4B. The violet tracing light in Journey 3 is explicitly non-molecular and exists only to visualize information flow through real state changes.','']
for s in scenes:
    doc += [f"## {s['scene_index']+1}. {s['locus']}",'',f"### {s['title']}",'',f"*{s['scene_kicker']}*",'',f"**Physical layout**  {s['scene_layout']['orientation']}",'']
    for p in s['story_paragraphs']: doc += [p,'']
    doc += [f"**Exit**  {s['story_close']}",'']
    if s['checkpoint']: doc += [f"**Optional Quick Recall**  {s['checkpoint_prompt']}",'']
doc += ['## Journey payoff','',journey['finale'],'']
(ROOT/'docs'/'UNIT4_F4C_JOURNEY3_STORY.md').write_text('\n'.join(doc),encoding='utf-8')

release_doc=f'''# Unit 4 F4C Release

## Scope

F4C adds only **Journey 3, Signal Relay Tower**. Journeys 1 and 2 remain protected byte-for-byte from F4B. F1 science, F2 architecture, and F3 scene briefs remain locked. Journeys 4–7 are not polished in this stage.

## Narrative release

- Journey 3 title: **{journey['story_title']}**
- Polished journeys: **3 / 7**
- Polished scenes: **19 / 51**
- Journey 3 knowledge records: **{manifest['journey_3_records']}**
- Journey 3 narrative words: **{manifest['journey_3_narrative_words']}**
- Journey 3 optional first-exposure recalls: **{manifest['journey_3_checkpoints']}**
- Student release: **false**
- Developer preview: **true**

## Narrative standard

Journey 3 uses one non-molecular violet tracing light to mark information flow while real molecular state changes carry the biology. The extracellular ligand remains at the receptor. Each scene preserves F3 left/center/right geography, introduces terminology after the defining mechanism is visible, and keeps receptor activation, intracellular relay, amplification, cellular response, mutation, and chemical perturbation distinct.

## Next gate

F4D may author **Journey 4, Feedback Regulation Center** only after F4C passes prose QA. Journeys 1–3 must remain unchanged.
'''
(ROOT/'docs'/'UNIT4_F4C_RELEASE.md').write_text(release_doc,encoding='utf-8')
print('Built Unit 4 F4C',json.dumps(manifest,indent=2))
