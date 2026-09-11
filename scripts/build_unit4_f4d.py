from __future__ import annotations
import json, hashlib, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content'/'ap-biology'/'unit-4'
F3=json.loads((U4/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS=json.loads((U4/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J4=next(j for j in JBRIEFS if j['journey_id']=='U4-J4')
B={b['locus_id']:b for b in F3 if b['journey_id']=='U4-J4'}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# F4D extends F4C. Journeys 1-3 are protected predecessors and are never regenerated here.
LOCK_C=json.loads((U4/'content-lock-f4c.json').read_text(encoding='utf-8'))
PREV=[]
for jid in ('U4-J1','U4-J2','U4-J3'):
    rel=f'journeys/{jid}.json'; p=U4/rel
    if not p.exists(): raise RuntimeError(f'F4D requires locked predecessor {rel}')
    expected=LOCK_C['files'][rel]
    if p.stat().st_size!=expected['bytes'] or sha(p)!=expected['sha256']:
        raise RuntimeError(f'F4D refuses to proceed because locked predecessor changed: {rel}')
    PREV.append(json.loads(p.read_text(encoding='utf-8')))
J1,J2,J3=PREV

GUIDE={
 'name':'Dr. Mira Chen','role':'cellular-systems investigator',
 'visual':'charcoal field jacket, clear protective glasses, and a compact white tablet whose amber cursor tracks one regulated-variable gauge',
 'story_job':'Mira keeps the regulated variable, reference range, sensor/control/effector roles, and response direction physically separate. She never labels a loop positive or negative until the learner can see whether the response reinforces or opposes the initiating change.'
}
GAUGE={
 'name':'Regulated-variable gauge','kind':'continuity instrument',
 'visual':'a waist-high circular gauge with a pale green reference band, a black needle that can drift above or below it, and a movable disturbance marker on the rim',
 'job':'carries one regulated condition through all six rooms so the learner can see the initial deviation, the response direction, and whether the condition returns toward range, moves farther away, or remains dysregulated'
}

route=[
 {'scene_index':0,'locus':'Homeostasis Control Map','short':'Homeostasis','floor':'Control-center entrance','symbol':'◎'},
 {'scene_index':1,'locus':'Sensor–Integrator–Effector Loop','short':'Loop parts','floor':'Circuit floor','symbol':'↻'},
 {'scene_index':2,'locus':'Negative-Feedback Thermostat','short':'Negative feedback','floor':'Thermostat chamber','symbol':'−↻'},
 {'scene_index':3,'locus':'Blood-Glucose Regulator','short':'Glucose','floor':'Metabolic control room','symbol':'G'},
 {'scene_index':4,'locus':'Positive-Feedback Amplifier','short':'Positive feedback','floor':'Amplifier hall','symbol':'+↻'},
 {'scene_index':5,'locus':'Dysregulation Alarm','short':'Dysregulation','floor':'Failure-analysis room','symbol':'!'},
]

ZONE_COPY={
'U4-L20':[
 ('left','Regulated variable and disturbance','↕','The regulated-variable gauge sits on the left with a disturbance marker that can push its needle above or below the pale green reference band.'),
 ('center','Reference range control map','◎','A large central display shows the target range or set point used by the regulatory system, with room for ordinary fluctuations inside the acceptable band.'),
 ('right','Feedback path to stability','↻','A return path on the right shows responses feeding back to influence the condition that initiated them and helping maintain internal stability.')],
'U4-L21':[
 ('left','Stimulus and sensor station','S','A disturbance reaches a sensor or receptor on the left, which detects a relevant change and sends information forward without being confused with the response itself.'),
 ('center','Control and integration desk','C','The center receives and evaluates incoming information and coordinates what should happen next; the role can be molecular, cellular, or organismal rather than requiring a brain.'),
 ('right','Effector and return path','E→','An effector on the right changes the regulated variable, and the resulting response loops back toward the original condition so the system can be evaluated again.')],
'U4-L22':[
 ('left','Temperature deviation','↑↓','The gauge is pushed above or below its regulated temperature range so the direction of the disturbance is unmistakable.'),
 ('center','Opposing control response','−↻','A thermostat-like control station activates heat-loss or heat-conserving/producing responses that oppose the direction of the initial deviation.'),
 ('right','Return toward regulated range','→◎','The right-side gauge shows the condition moving back toward its regulated range as the original stimulus diminishes and the corrective drive weakens.')],
'U4-L23':[
 ('left','Blood-glucose disturbance','G↑↓','The same style of gauge now shows blood glucose rising after nutrient input or falling below its regulated range.'),
 ('center','Opposing hormonal signals','I / G','Insulin-associated and glucagon-associated responses occupy opposite sides of one control panel so both can be seen as responses to deviations of the same regulated variable.'),
 ('right','Target-tissue response','liver / tissue','Responsive tissues alter glucose uptake, storage, or release so circulating glucose moves back toward its regulated range.')],
'U4-L24':[
 ('left','Initial triggering event','→','A small initiating stimulus begins on the left, such as cervical stretch, vessel injury, or an initial pulse of ethylene during fruit ripening.'),
 ('center','Self-reinforcing loop','+↻','The central loop sends each response back in a direction that strengthens the process that produced it, so the cycle grows until an endpoint changes the system.'),
 ('right','Amplified endpoint process','≫','Childbirth, clot formation, or ripening visibly intensifies on the right until delivery, vessel sealing, or another changed condition terminates the loop.')],
'U4-L25':[
 ('left','Normally regulated condition','◎','A healthy reference case on the left shows a variable remaining within a workable range while control mechanisms respond appropriately.'),
 ('center','Failed or inadequate feedback','✕↻','The central control loop is weakened, disconnected, or unable to generate an adequate response, so the disturbance persists instead of being corrected.'),
 ('right','Dysregulated state and disease risk','!','The right side shows accumulating physiological consequences while preserving the distinction between regulatory failure as a contributor to disease and disease as a broader category.')],
}

NARR={
'U4-L20':{
 'title':'The Gauge That Would Not Stay Still','kicker':'Homeostasis is not a frozen number. It is active regulation that keeps a changing condition within a workable range.',
 'paragraphs':[
  "The elevator from the Signal Relay Tower opens into a low circular room called the **Homeostasis Control Map**. The room is quiet except for a sharp alarm from a waist-high gauge on your **left**. Its black needle has drifted above a pale green band and is still climbing. Directly **ahead**, a wall-sized control map shows that same green band as a target region, not as one hairline mark. On your **right**, a feedback path curves from the system output back toward the gauge, but its arrows are dark and disconnected. Mira sets her tablet beside the gauge and points to the needle. ‘The relay tower can send signals correctly now,’ she says, ‘but this center still does not know what counts as regulated.’",
  "She pushes the disturbance marker on the rim, and the needle rises farther. Then she moves it in the opposite direction and the needle falls below the green band. The important feature is not the exact number. It is the deviation from a workable internal range. Mira names the broader process **homeostasis** only after you have watched the gauge move. Homeostasis is dynamic regulation of internal conditions within ranges compatible with function despite internal and external change. The needle is allowed to move. The system’s job is to keep that movement within biologically useful limits or return a disturbance toward them.",
  "At the center map, Mira highlights the pale green region. The control system uses a **set point** or regulated target as a reference. Sometimes that target is described as a value; often it is better pictured as a range that can shift with physiological context. The display deliberately refuses to print one universal human body-temperature number across the center. Time of day, measurement site, activity, hormones, and individual variation can all influence measured temperature. The target is a control reference, not a magical number that every healthy body must match at every instant.",
  "Mira reconnects the right-hand arrows. A response now feeds back toward the process that produced it. That closed regulatory arrangement is a **feedback loop**. The system’s output or response influences the process that generated the output. As the right-hand path activates, the needle begins moving toward the green range and then continues to wobble slightly inside it. Mira leaves the wobble visible. Organisms use feedback mechanisms to **maintain internal environments** in the face of internal and external change. In multicellular organisms, **cell signaling supports homeostasis** by coordinating the activities of cells and tissues that participate in those regulatory responses.",
  "The control map is no longer trying to freeze the needle. It is trying to regulate it. But when Mira asks the system which component detected the deviation, which component evaluated it, and which component actually changed the variable, three warning lights flash at once. The feedback arrows are working, yet their jobs have been merged together. A cable marked INPUT leaves the left gauge and disappears into the next room. Mira lifts the gauge by its handle. ‘Now we separate the roles,’ she says, and carries the same needle into the Sensor–Integrator–Effector Loop."
 ],
 'close':'The first room leaves one durable image behind: a black needle fluctuating around a green reference range while feedback acts to maintain internal stability. The unresolved wiring leads directly into the Sensor–Integrator–Effector Loop.'
},
'U4-L21':{
 'title':'Three Jobs Inside One Loop','kicker':'A disturbance must be detected, information must be evaluated, and an effector must change the system. Those roles are related but not interchangeable.',
 'paragraphs':[
  "You enter the **Sensor–Integrator–Effector Loop** with the same regulated-variable gauge in Mira’s hands. The room is arranged as a broad horseshoe. On your **left**, the gauge sits beside a detector station. Directly **ahead**, a control and integration desk receives incoming signals. On your **right**, an effector station connects back to the gauge through a return pipe. The three stations are physically separated by floor markings because the center’s earlier failure came from treating them as one object. Mira introduces a disturbance at the gauge and waits. Nothing moves until the left station detects it.",
  "The changed condition is the **stimulus**. In a feedback system, a stimulus is a change in a regulated variable or condition that can be detected. The left detector is the **sensor/receptor in feedback**. It detects a relevant change and generates information used by the regulatory system. Mira deliberately swaps the detector icon from a whole-organism receptor to a molecular sensor embedded in a small cell model. The loop still works. A sensor does not have to be a sense organ, and the next step does not have to be a brain.",
  "The sensor sends information to the desk directly ahead. The desk compares or integrates the incoming information and determines which downstream response should be coordinated. Mira names this the **control/integration function**. It can exist at molecular, cellular, tissue, or organismal scales. The center therefore performs a regulatory role without being defined as a nervous-system command center. This matters because the same control logic appears inside signaling pathways, metabolic networks, endocrine systems, and other biological regulation.",
  "The center sends an instruction to the right. An **effector** changes activity and actually alters the regulated variable or system output. The return pipe carries the consequence back toward the gauge. That change is the **feedback response**. Mira resets the loop and asks you to point to the parts in order. Stimulus on the left. Sensor detects it. Control/integration function evaluates or coordinates. Effector acts on the right. Response changes the system and feeds back toward the original condition. The words stop feeling like a list because each has a different location and job.",
  "For one final pass, Mira shrinks the entire horseshoe into a molecular model. A protein senses a chemical state, an intracellular regulatory component integrates that information, and another protein changes the system output. No brain, muscle, or gland appears, yet the roles remain recognizable. The room has established the anatomy of feedback without trapping it at one biological scale. Mira then turns the disturbance dial sharply upward. The return pipe points toward a chamber glowing red with heat. ‘We know the parts,’ she says. ‘Now we ask which direction the response pushes.’"
 ],
 'close':'The loop is now anatomically separated into stimulus, sensor, control/integration, effector, and response. The next room tests the defining direction of negative feedback.'
},
'U4-L22':{
 'title':'The Response That Pushes Back','kicker':'Negative feedback is defined by direction. The response opposes the initiating deviation and reduces the stimulus that called it into action.',
 'paragraphs':[
  "A wave of dry heat meets you as the door opens into the **Negative-Feedback Thermostat**. The room is rectangular and easy to map. On your **left**, the regulated-variable gauge is now a temperature gauge whose needle has been driven above the green reference band. Directly **ahead**, a thermostat-like control panel has two opposing response levers. On your **right**, a second display shows the same variable after the response acts. Mira keeps the left needle high and asks you to ignore the word printed on the center panel. ‘Watch the direction first.’",
  "The high-temperature deviation activates responses that promote heat loss, represented here by a sweating display and increased heat transfer away from the body model. The right-hand needle begins moving downward toward the regulated range. Mira then resets the chamber and drives the left needle below the band. This time the control system activates responses such as shivering and heat conservation that push body temperature upward. In both cases, the response moves opposite to the direction of the initiating deviation. Only now does Mira name the mechanism **negative feedback**.",
  "Negative feedback reduces the initial stimulus and helps return a perturbed system toward a regulated target or set point. As the right-hand needle approaches the green range, the corrective drive weakens because the condition that triggered the response is being reduced. The system is therefore self-limiting. Mira circles the minus sign on the panel and crosses out two words someone had written underneath it: BAD and HARMFUL. ‘Negative’ describes the direction of the feedback effect on the initial deviation. It does not mean the mechanism is biologically bad.",
  "The temperature example becomes **thermoregulation** when Mira makes its biological roles explicit. Sweating can promote heat loss when temperature is high. Shivering can increase heat production when temperature is low, and other responses can alter heat conservation. The precise response depends on the organism and context, but the control logic is stable: a deviation triggers responses that oppose that deviation. Mira leaves small fluctuations inside the green band to preserve the earlier lesson that regulated temperature is dynamic rather than perfectly constant.",
  "Before you leave, Mira covers every label except the arrows. The left needle rises. The center response points downward. The right needle returns toward range. Then the left needle falls. The response points upward. Again the right needle moves toward range. If you can recognize that geometry, you can identify negative feedback even when the biological variable changes. The next door proves it. The temperature symbols fade, and a glucose molecule appears on the same gauge."
 ],
 'close':'The thermostat has established negative feedback as an opposing, self-limiting response. The same control logic is now transferred to blood glucose without changing the meaning of negative feedback.'
},
'U4-L23':{
 'title':'Two Hormones, One Regulated Variable','kicker':'Insulin-associated and glucagon-associated responses point in opposite physiological directions, yet both participate in negative-feedback control of blood glucose.',
 'paragraphs':[
  "The **Blood-Glucose Regulator** resembles a metabolic control room built around one long horizontal gauge. On your **left**, blood glucose rises after a simulated nutrient input, then later falls below the green reference band in a separate trial. Directly **ahead**, two hormonal response tracks sit on opposite sides of the same control console. One is labeled insulin-associated; the other glucagon-associated. On your **right**, liver and other responsive tissue models show what happens to glucose uptake, storage, and release. Mira clips the regulated-variable gauge into the left rail so the same needle from the thermostat now measures glucose concentration.",
  "In the first trial, the needle rises above the regulated range. Insulin-associated signaling increases. Responsive tissues increase processes that promote glucose uptake and storage, and the right-hand tissue display pulls glucose out of the circulating pool. The gauge moves downward toward the green band. Mira resets the model. In the second trial, the needle falls below the regulated range. Glucagon-associated signaling increases, and responsive tissues such as the liver increase processes that make glucose more available to the blood. The gauge moves upward toward the same regulated range.",
  "The two hormonal responses point in opposite physiological directions, but Mira places both inside one bracket labeled **blood-glucose feedback example**. Insulin and glucagon participate in negative-feedback regulation of blood glucose because each helps oppose a deviation of the same regulated variable. The word negative does not belong exclusively to one hormone. The determining question is whether the response tends to counter the initial change in blood glucose.",
  "Mira then removes the hormone names and leaves only the arrows. High variable → response that lowers it. Low variable → response that raises it. The pattern is identical to the thermostat even though the effectors and signals are different. This is why feedback is useful as a transferable control concept. You should be able to diagnose the direction of a new biological loop from the relationship between disturbance and response, not from memorizing one example.",
  "She runs both trials once more without changing the position of the three zones. The glucose disturbance stays on the left, the hormonal control remains in the center, and responsive tissues stay on the right. That repetition makes the causal map stable: what changes between trials is the direction of the disturbance and which physiological response is recruited, not the underlying logic of feedback.",
  "As the second trial stabilizes, an alarm sounds from the hall. The gauge is still near its green band, but another display is behaving in the exact opposite way. A small change is producing a larger response, which produces an even larger change. Mira turns the glucose console off. ‘That loop is not trying to restore a range,’ she says. The door ahead opens onto the Positive-Feedback Amplifier."
 ],
 'close':'Blood-glucose control has shown that different signals can participate in the same negative-feedback logic. The next room contrasts that stabilizing direction with a loop that reinforces its initiating change.'
},
'U4-L24':{
 'title':'The Loop That Builds Until Something Ends It','kicker':'Positive feedback reinforces an ongoing change. It grows the process instead of restoring a set point, and an endpoint must eventually break the cycle.',
 'paragraphs':[
  "The **Positive-Feedback Amplifier** is a long hall with three demonstration lanes but one shared control loop. On your **left**, each lane begins with a small initiating event. Directly **ahead**, a bright circular arrow sends each response back toward the process that produced it. On your **right**, the corresponding biological process grows larger with every cycle. The regulated-variable gauge sits beside Mira, but this time its needle is not being pushed back toward a green range. Mira starts with the smallest input and says the same thing she said in the thermostat room. ‘Watch the direction before you read the label.’",
  "In the childbirth lane, cervical stretch begins on the left. That stretch promotes oxytocin release. Oxytocin strengthens uterine contractions, stronger contractions increase cervical stretch, and the increased stretch promotes further oxytocin signaling. The central loop visibly feeds the response back in the same direction as the initiating process. This is **positive feedback**. Positive feedback amplifies a response so the initiating variable is driven further in the same direction until another event ends the loop. Here, delivery changes the system and terminates the reinforcing cycle.",
  "The second lane begins with vessel damage. Activated platelets and clotting factors help recruit or activate additional components, causing clot formation to build at the site of injury. Mira labels this the **blood-clotting positive feedback example**. The loop intensifies until the breach is sealed and the initiating condition changes. The third lane contains ripening fruit. Ethylene promotes ripening processes that can stimulate additional ethylene production, creating a **fruit-ripening positive feedback example** in many fruits. Again, the reinforcing loop does not restore a set point while it is running.",
  "Mira walks back to the childbirth display and gives the detailed example its proper name, **childbirth positive feedback**. Cervical stretch can promote oxytocin release, which strengthens uterine contractions and increases stretch until delivery terminates the loop. Then she places a large plus sign above the center arrow and crosses out GOOD and BENEFICIAL. Positive feedback is not defined by whether the result is desirable. The plus sign describes a response that reinforces the initiating change.",
  "The three loops now accelerate side by side. Mira stops each one differently. Delivery ends the childbirth cycle. Sealing the damaged vessel changes the clotting condition. A changed ripening state eventually changes the context of the ethylene loop. Positive feedback does not automatically stabilize itself. An external endpoint or changed condition terminates the reinforcing cycle. Mira then disables the endpoint sensors entirely. The amplified processes disappear from the hall, and the regulated-variable gauge begins drifting without an effective correction. A red alarm flashes in the final room."
 ],
 'close':'The amplifier has established positive feedback as reinforcing rather than “good.” When the regulation system itself fails, the learner enters the Dysregulation Alarm to see the consequences.'
},
'U4-L25':{
 'title':'When the Control System Stops Correcting the Drift','kicker':'Regulatory failure can contribute to disease, but disease is broader than a single failure of homeostasis.',
 'paragraphs':[
  "The final room, the **Dysregulation Alarm**, is darker than the rest of the center. On your **left**, a healthy reference system keeps the familiar gauge within its green working range. Directly **ahead**, an identical feedback loop has a broken sensor connection, a weakened control signal, or an inadequate effector response. On your **right**, the same regulated condition drifts farther from its workable range while warning indicators accumulate. Mira places the continuity gauge beside the failed loop and deliberately applies the same disturbance to both systems.",
  "The healthy loop detects the change, coordinates an appropriate response, and brings the condition back toward range. The impaired loop does not. The needle remains displaced despite the continuing disturbance. Mira names the result **homeostatic dysregulation and disease** only after the contrast is visible. Disrupted regulatory mechanisms can contribute to disease, including dysregulated glucose control or dysregulated cell proliferation. The important word is contribute. Disease is a broader biological category with many possible causes and mechanisms; it should not be defined simply as ‘loss of homeostasis.’",
  "Mira switches the center model to glucose regulation. Inadequate control allows the glucose gauge to remain outside its healthy range. Then she changes the model to cell proliferation. Regulatory failures can permit growth and division to proceed abnormally. The examples share a loss of effective regulation, yet their molecular causes and pathological outcomes are not identical. The display therefore keeps the general principle and the specific disease mechanisms at different levels of explanation.",
  "For the final reconstruction, Mira carries the gauge back through miniature models of every room. First you identify **homeostasis** as dynamic regulation around a useful range. Then the loop separates into stimulus, sensor, control/integration, effector, and response. At the thermostat, the response opposes a deviation, so the loop is **negative feedback**. At the amplifier, the response reinforces the initiating change, so it is **positive feedback**. At the final alarm, inadequate regulation allows a condition to remain outside a healthy range and can contribute to disease. The meanings now come from response direction and control logic, not from the everyday emotional meanings of positive and negative.",
  "Mira shuts off the alarms and leaves the gauge floating in its green band with small natural fluctuations still visible. The regulation center is repaired, but the next corridor displays something new: a long DNA molecule being packed into a chromosome while a cell-cycle clock waits beside it. The problem ahead is no longer whether a variable returns toward range. It is how a cell prepares its genetic material and itself for division. Mira picks up the gauge one last time, sets it on the completed control map, and opens the door toward the Cell-Cycle Preparation Archive."
 ],
 'close':'The Feedback Regulation Center closes with one coherent control model: regulated condition, reference range, sensor/control/effector roles, response direction, and the consequences of failed regulation are all distinguishable. The next journey moves into cell-cycle preparation.'
}
}

TERM_IMAGES={
'U4-K-018':'the gauge returning toward a regulated internal range after feedback responds to a disturbance',
'U4-K-094':'the black gauge needle fluctuating within and returning toward a pale green reference range',
'U4-K-095':'the pale green target range on the center control map used as a regulatory reference',
'U4-K-096':'the right-side response path looping back to influence the process that generated the response',
'U4-K-108':'cell-signaling routes coordinating multiple cells and tissues to support internal regulation',
'U4-K-097':'the disturbance that moves the regulated-variable gauge away from its reference range',
'U4-K-098':'the left sensor detecting the relevant change and sending information toward control',
'U4-K-099':'the center control/integration desk evaluating information and coordinating downstream action without requiring a brain',
'U4-K-100':'the right effector changing the regulated variable or system output',
'U4-K-101':'the resulting system change looping back toward the original regulated condition',
'U4-K-019':'the response arrow pointing opposite the initial deviation and reducing the stimulus',
'U4-K-102':'high temperature triggering heat-loss responses and low temperature triggering heat-producing or conserving responses',
'U4-K-103':'high glucose activating insulin-associated responses and low glucose activating glucagon-associated responses that move one variable toward range',
'U4-K-020':'the center loop feeding each response back in the same direction so the initiating change grows',
'U4-K-104':'cervical stretch → oxytocin → stronger uterine contractions → greater cervical stretch until delivery',
'U4-K-105':'activated clotting components recruiting or activating additional components until the breach is sealed',
'U4-K-106':'ethylene-promoted ripening stimulating additional ethylene production in a reinforcing loop',
'U4-K-107':'the failed feedback system leaving the gauge outside its healthy range while physiological consequences accumulate'
}

HINTS={
'U4-L22':'Picture the temperature needle above or below range. In each case, the response points in the opposite direction and reduces the original deviation.',
'U4-L24':'Picture one small initiating event feeding into a loop that makes the same process grow larger until an endpoint breaks the cycle.'
}

def scene_layout(b):
    zones=[]
    for pos in ('left','center','right'):
        label,symbol,desc=next((x[1],x[2],x[3]) for x in ZONE_COPY[b['locus_id']] if x[0]==pos)
        zones.append({'position':pos,'label':label,'symbol':symbol,'description':desc})
    return {'orientation':f"On your left is {zones[0]['label']}. Directly ahead is {zones[1]['label']}. On your right is {zones[2]['label']}. These anchors stay fixed while the control logic runs.", 'zones':zones}

def cast_for(b):
    casts=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    for part in b['stable_cast']:
        casts.append({'name':part['name'],'kind':part['type'].lower(),'visual':part['visual_identity'],'job':part['job_in_scene']})
    casts.append(dict(GAUGE))
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
      'scene_layout':scene_layout(b),'cast':cast_for(b),'continuity_object':J4['continuity_object'],
      'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':beats,'memory_snapshot':snaps,
      'misconception_guards':b['misconception_guards'],'exit_memory':b['exit_memory'],
      'checkpoint':cp,'checkpoint_object_id':b['primary_knowledge_id'],'checkpoint_prompt':qr.get('candidate_prompt','') if cp else '',
      'checkpoint_answer':qr.get('answer','') if cp else '','checkpoint_hint':HINTS.get(lid,'') if cp else '',
      'next_locus':B[b['causal_transition']['to_locus_id']]['scene_title'] if b['causal_transition']['to_locus_id'] else None,
      'causal_transition':b['causal_transition']['transition_logic']
    }

lids=J4['route']; scenes=[make_scene(lid,i) for i,lid in enumerate(lids)]
journey={
 'palace_id':'U4-J4','palace_name':'Feedback Regulation Center','story_title':'The Control Room That Forgot Which Way to Push',
 'tagline':'The signals arrive, but the regulation center has confused sensor, controller, effector, and response direction. Repair the loop by following one drifting gauge through opposing, reinforcing, and failed control.',
 'guide':GUIDE,
 'premise':'The repaired signaling system can now carry information reliably, but the Feedback Regulation Center is allowing internal conditions to drift. Its reference range is being treated as a single frozen number, sensor and effector roles are mixed together, and the response arrows no longer distinguish opposing control from reinforcing control. Mira brings one regulated-variable gauge whose black needle can move above or below a pale green reference band. The same gauge remains visible through every room so the learner can judge the direction of the disturbance and the direction of the response.',
 'mission':'Rebuild regulation from the inside out. Establish homeostasis as dynamic regulation around a useful range, separate stimulus, sensor, control/integration, effector, and response, diagnose negative feedback from a response that opposes deviation, transfer that logic to blood-glucose control, contrast it with positive feedback that reinforces a process until an endpoint changes the system, and finish by showing how failed regulation can contribute to disease without defining all disease as homeostatic failure.',
 'finale':'At the final alarm, the learner can reconstruct one complete control-system model. A regulated variable moves relative to a reference range. A stimulus is detected by a sensor, information is integrated, an effector acts, and the response feeds back. If the response opposes the initiating deviation, the loop is negative feedback and tends to restore regulation. If the response reinforces the initiating change, the loop is positive feedback and requires an endpoint or changed condition to stop. If control is inadequate, dysregulation can persist and contribute to disease. The gauge ends with small fluctuations inside the regulated range, preserving homeostasis as dynamic rather than perfectly constant.',
 'estimated_minutes':22,'scene_count':len(scenes),'checkpoint_count':sum(bool(s['checkpoint']) for s in scenes),
 'learner_rule':'Read or listen and place the regulated-variable gauge first. Keep left, center, and right fixed. Judge the direction of the disturbance and response before naming the feedback type. Quick Recall is optional during first exposure.',
 'route_orientation':'The Feedback Regulation Center is one continuous six-location control circuit. Begin at the Homeostasis Control Map, pass through the Sensor–Integrator–Effector Loop, test opposing response direction in the Negative-Feedback Thermostat, transfer that logic to the Blood-Glucose Regulator, contrast it with the Positive-Feedback Amplifier, and finish at the Dysregulation Alarm. The same regulated-variable gauge travels through all six locations.',
 'route':route,'scenes':scenes,'student_release':'DEVELOPER_PREVIEW_F4D','narrative_standard':'V2-NARRATIVE-4.3-U4-F4D'
}

(U4/'journeys'/'U4-J4.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def card(j): return {k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
registry={'schema':'memory-palace-v2-unit4-f4d-registry-1.0','course_id':'ap-biology','unit_id':'unit-4','unit_title':'Cell Communication and Cell Cycle','narrative_standard':'V2-NARRATIVE-4.x-U4-F4D','journey_count':4,'scene_count':sum(x['scene_count'] for x in (J1,J2,J3,journey)),'checkpoint_count':sum(x['checkpoint_count'] for x in (J1,J2,J3,journey)),'guided_journeys':[card(J1),card(J2),card(J3),card(journey)]}
(U4/'journeys-f4d.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U4/'status-f4c.json').read_text(encoding='utf-8'))
status.update({'status':'F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','pipeline_status':'POLISHED_NARRATIVE_F4D','narrative_lock':'LOCKED_F4D_J1_J2_J3_J4','student_release':False,'preview_release':True,'journey_count':4,'scene_count':25,'polished_journeys':4,'polished_scenes':25,'polished_checkpoint_count':10,'narrative_story_files':4,'next_required_output':'F4E polished narrative for Journey 5 only after F4D prose QA; Journeys 1–4 remain locked unchanged'})
(U4/'status-f4d.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(U4/'status.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; course=json.loads(cp.read_text(encoding='utf-8'))
for u in course['units']:
    if u['unit_id']=='unit-4':
        u.update({'status':'F4D_JOURNEYS1_4_POLISHED_DEVELOPER_PREVIEW','journey_count':4,'scene_count':25,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEYS1_4_POLISHED_F4D','polished_journeys':4,'polished_scenes':25,'student_release':False,'preview_release':True,'canonical_records':180})
cp.write_text(json.dumps(course,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# The backend already prefers the newest available Unit 4 registry through F4G fallbacks.
# F4D therefore becomes active automatically when journeys-f4d.json exists; no backend source rewrite is needed.

files=['journeys/U4-J1.json','journeys/U4-J2.json','journeys/U4-J3.json','journeys/U4-J4.json','journeys-f4d.json','status-f4d.json']
lock={'schema':'memory-palace-v2-unit4-f4d-content-lock-1.0','unit_id':'unit-4','stage':'F4D','lock_status':'LOCKED_F4D_J1_J2_J3_J4','student_release':False,'preview_release':True,'protected_predecessors':{rel:LOCK_C['files'][rel] for rel in ('journeys/U4-J1.json','journeys/U4-J2.json','journeys/U4-J3.json')},'files':{f:{'bytes':(U4/f).stat().st_size,'sha256':sha(U4/f)} for f in files}}
(U4/'content-lock-f4d.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit4-f4d-release-manifest-1.0','unit_id':'unit-4','stage':'F4D','student_release':False,'preview_release':True,'canonical_records_protected':180,'polished_journeys':4,'polished_scenes':25,'journey_4_records':sum(len(s['object_ids']) for s in scenes),'journey_4_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'journey_4_narrative_words':sum(len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs']))) for s in scenes),'next_stage':'F4E_JOURNEY5_AFTER_F4D_QA'}
(U4/'f4d-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')

# Human-readable story and release artifacts.
doc=['# Unit 4 F4D · Journey 4 Narrative','',f"## {journey['story_title']}",'',journey['tagline'],'',f"**Guide**  {GUIDE['name']}, {GUIDE['role']}",'',f"**Premise**  {journey['premise']}",'',f"**Mission**  {journey['mission']}",'',f"**Route**  {' → '.join(r['locus'] for r in route)}",'', '> F4D is a developer narrative preview. Unit 4 remains `student_release: false`. Journeys 1–3 are protected byte-for-byte from F4C.','']
for s in scenes:
    doc += [f"## {s['scene_index']+1}. {s['locus']}",'',f"### {s['title']}",'',f"*{s['scene_kicker']}*",'',f"**Physical layout**  {s['scene_layout']['orientation']}",'']
    for p in s['story_paragraphs']: doc += [p,'']
    doc += [f"**Exit**  {s['story_close']}",'']
    if s['checkpoint']: doc += [f"**Optional Quick Recall**  {s['checkpoint_prompt']}",'']
doc += ['## Journey payoff','',journey['finale'],'']
(ROOT/'docs'/'UNIT4_F4D_JOURNEY4_STORY.md').write_text('\n'.join(doc),encoding='utf-8')

release_doc=f'''# Unit 4 F4D Release

## Scope

F4D adds only **Journey 4, Feedback Regulation Center**. Journeys 1–3 remain protected byte-for-byte from F4C. F1 science, F2 architecture, and F3 scene briefs remain locked. Journeys 5–7 are not polished in this stage.

## Narrative release

- Journey 4 title: **{journey['story_title']}**
- Polished journeys: **4 / 7**
- Polished scenes: **25 / 51**
- Journey 4 knowledge records: **{manifest['journey_4_records']}**
- Journey 4 narrative words: **{manifest['journey_4_narrative_words']}**
- Journey 4 optional first-exposure recalls: **{manifest['journey_4_checkpoints']}**
- Student release: **false**
- Developer preview: **true**

## Narrative standard

Journey 4 carries one regulated-variable gauge through all six locations. The gauge preserves disturbance direction, reference range, response direction, and regulatory outcome. Feedback terminology is introduced only after the learner can see whether a response opposes or reinforces the initiating change. Sensor, integration, effector, response, set point, homeostasis, negative feedback, positive feedback, and dysregulation remain physically distinguishable.

## Next gate

F4E may author **Journey 5, Cell-Cycle Preparation Archive** only after F4D passes prose QA. Journeys 1–4 must remain unchanged.
'''
(ROOT/'docs'/'UNIT4_F4D_RELEASE.md').write_text(release_doc,encoding='utf-8')
print('Built Unit 4 F4D',json.dumps(manifest,indent=2))
