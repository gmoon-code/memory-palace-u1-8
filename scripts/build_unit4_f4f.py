from __future__ import annotations
import json, hashlib, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U4=ROOT/'content'/'ap-biology'/'unit-4'
F3=json.loads((U4/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS=json.loads((U4/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J6=next(j for j in JBRIEFS if j['journey_id']=='U4-J6')
B={b['locus_id']:b for b in F3 if b['journey_id']=='U4-J6'}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

LOCK_E=json.loads((U4/'content-lock-f4e.json').read_text(encoding='utf-8'))
PREV=[]
for jid in ('U4-J1','U4-J2','U4-J3','U4-J4','U4-J5'):
    rel=f'journeys/{jid}.json'; p=U4/rel
    if not p.exists(): raise RuntimeError(f'F4F requires locked predecessor {rel}')
    expected=LOCK_E['files'][rel]
    if p.stat().st_size!=expected['bytes'] or sha(p)!=expected['sha256']:
        raise RuntimeError(f'F4F refuses to proceed because locked predecessor changed: {rel}')
    PREV.append(json.loads(p.read_text(encoding='utf-8')))
J1,J2,J3,J4,J5=PREV

GUIDE={
 'name':'Dr. Mira Chen','role':'cellular-systems investigator',
 'visual':'charcoal field jacket, clear protective glasses, and a compact white tablet whose amber cursor now follows the same replicated chromosome set from one end of the transit hall to the other',
 'story_job':'Mira keeps the same chromosome identities in view through every mitotic stage. She makes the learner distinguish chromosome position, spindle structures, nuclear boundaries, and cytoplasmic division before naming each stage.'
}
TRACKED={
 'name':'Tracked mitosis chromosome set','kind':'continuity model',
 'visual':'the same small replicated chromosome set carried out of Journey 5, with artificial blue-and-gold tracing bands on homolog identities and a thin white seam joining each pair of sister chromatids until anaphase',
 'job':'preserves chromosome identity through condensation, attachment, alignment, separation, nuclear reassembly, and cytokinesis so stage names remain attached to visible chromosome states'
}

route=[
 {'scene_index':0,'locus':'Mitosis Mission Control','short':'Mission Control','floor':'Transit entrance','symbol':'M'},
 {'scene_index':1,'locus':'Prophase Spindle Setup','short':'Prophase','floor':'Spindle bay','symbol':'P'},
 {'scene_index':2,'locus':'Prometaphase Kinetochore Access','short':'Prometaphase','floor':'Attachment zone','symbol':'PK'},
 {'scene_index':3,'locus':'Metaphase Plate Station','short':'Metaphase','floor':'Equator station','symbol':'M'},
 {'scene_index':4,'locus':'Anaphase Separation Track','short':'Anaphase','floor':'Separation track','symbol':'A'},
 {'scene_index':5,'locus':'Telophase Reassembly Room','short':'Telophase','floor':'Reassembly room','symbol':'T'},
 {'scene_index':6,'locus':'Animal Cytokinesis Ring','short':'Animal cytokinesis','floor':'Animal exit','symbol':'◌'},
 {'scene_index':7,'locus':'Plant Cell-Plate Works','short':'Plant cytokinesis','floor':'Plant exit','symbol':'▭'},
]

NARR={
'U4-L34':{
 'title':'The Transit Hall With the Stages Out of Order','kicker':'The same replicated chromosomes must reach two daughter nuclei without losing their identity along the route.',
 'paragraphs':[
  "The transparent chromosome case from the Cell-Cycle Preparation Archive clicks into a rail at the entrance to **Mitosis Mission Control**. You are standing in a long hall that runs straight from one giant cell model to two empty daughter-nucleus bays. On your **left**, the replicated chromosome set from Journey 5 sits inside the starting cell, each chromosome still made of two sister chromatids joined together. Directly **ahead**, a floor-sized route map should lead through the mitotic stages, but its stage panels are flashing in the wrong order. On your **right**, two clear nuclear shells wait at opposite ends of the destination platform. Their chromosome trays are empty. Mira taps the case. The challenge is simple to say and difficult to fake. The same replicated genome that entered this hall has to be distributed into two equivalent chromosome sets without inventing or losing chromosomes along the way.",
  "Mira dims every sign except the physical chromosome models. The left-side chromosomes are already replicated before mitosis begins. She slides a duplicate outline of that same set toward each empty nuclear bay on the right, then locks the outlines in place as the destination. This is the core of **mitosis genome transmission**. Mitosis segregates replicated chromosomes so daughter nuclei receive complete, equivalent genome sets when segregation proceeds normally. The blue-and-gold tracing bands let you verify identity from one side of the hall to the other. They are tracking marks on the model, not biological colors. Nothing in this first room says that mitosis creates diploid cells in every organism. The point is faithful distribution of the chromosome set that entered the process.",
  "The central route map wakes up one panel at a time. A compact chromosome icon appears under **prophase**, then passes through the broader mitotic sequence toward **metaphase**, **anaphase**, and **telophase**. Mira explains the **mitosis sequence** by pointing to physical changes that will occur in the following rooms. Chromosomes condense and a spindle forms. Chromosomes become positioned at the cell equator. Sister chromatids separate and move toward opposite poles. New nuclei form around the separated sets. The map leaves a small attachment interval between prophase and metaphase where the nuclear envelope breaks down and spindle microtubules reach kinetochores. That interval will be named prometaphase when you arrive there, while the larger stage sequence remains easy to reconstruct from the four major stage names.",
  "Three illuminated panels rise above the destination bays. One shows a growing multicellular organism, another shows repaired tissue filling a wound, and a third shows a single-celled eukaryote producing a new individual. These are **mitosis roles**. The same chromosome-segregation mechanism contributes to growth, tissue repair, and asexual reproduction in eukaryotes. Mira keeps the nuclear destination bays separate from two doors farther down the hall marked CYTOPLASM. Those doors stay locked. **Cytokinesis** will divide cytoplasm near the end of the route, but it is not being smuggled into the definition of mitosis here. Mission Control now knows the starting set, the destination sets, and the stage order. What it still lacks is machinery capable of moving the chromosomes. A low vibration begins under the floor as the next spindle bay powers on."
 ],
 'close':'The map now preserves one replicated starting genome and two equivalent daughter-nucleus destinations. The unresolved problem is mechanical, so Mira releases the same chromosome case into Prophase Spindle Setup, where the spindle must begin to form.'
},
'U4-L35':{
 'title':'The Spindle Wakes Up','kicker':'Prophase makes the chromosomes easier to move and begins building the machinery that will move them.',
 'paragraphs':[
  "The rail carries the same chromosome set into **Prophase Spindle Setup**, a wide oval bay whose floor is shaped like an animal cell. Your **left** contains the replicated chromosomes, initially shown as long, loose chromatin regions within the nucleus. Directly **ahead**, a dark lattice of unassembled microtubule components fills the spindle construction zone. On your **right**, two centrosomes sit close together beside the nucleus. A display above them shows one pair of poles at opposite ends of the cell, but the real centrosomes have not moved there yet. Mira locks the transparent tracking bands onto the chromosomes so that condensation can change their shape without changing which chromosomes you are following.",
  "The left-side chromatin begins to compact. Long diffuse threads shorten and thicken until the replicated chromosomes become distinct, visible structures. Their sister chromatids remain joined. This visible change marks **prophase**. At the same time, the central construction zone assembles a microtubule-based apparatus called the **mitotic spindle**. Mira runs one finger along the growing microtubules. The spindle is the machinery that will organize and segregate chromosomes during mitosis. It is not a chromosome and it is not the same structure as the centrosomes sitting on the right. Keeping those objects in separate places makes the vocabulary match the physical system.",
  "The right-side pair now begins to separate. In this animal-cell model, each **centrosome** acts as a major microtubule-organizing center. The centrosomes move toward opposite sides of the cell while spindle microtubules extend through the center. Mira places a small animal-cell badge above them. That badge matters. Centrosomes provide a useful animal-cell model for spindle organization, but the story does not turn this arrangement into a universal requirement for plant cells. The movement of the two organizing centers helps establish opposite spindle poles, giving the future chromosomes two directions in which they can be sorted.",
  "A problem remains. The spindle is forming outside the chromosome region, and the kinetochores on the replicated chromosomes are still shielded by the nuclear boundary. Mira freezes the room before attachment begins. On the left, the chromosomes are condensed. Ahead, the spindle exists but has not yet secured the chromosomes. On the right, the centrosomes are farther apart. Those three visual changes belong together as the prophase setup. Mira does not jump ahead and call this metaphase simply because a spindle is present. She points to the still-intact access barrier around the chromosome region. Until spindle microtubules can physically reach kinetochores, the chromosomes cannot be positioned by the spindle. A section of the nuclear boundary starts to break into fragments, opening the route to the next room."
 ],
 'close':'Prophase has condensed the tracked replicated chromosomes and begun spindle formation while animal-cell centrosomes separate toward opposite poles. The nuclear boundary now becomes the next obstacle, leading directly into Prometaphase Kinetochore Access.'
},
'U4-L36':{
 'title':'The Doors Around the Chromosomes Open','kicker':'Prometaphase gives spindle microtubules physical access to chromosome kinetochores.',
 'paragraphs':[
  "You follow the chromosomes through a short passage into **Prometaphase Kinetochore Access**. The room is arranged like a security gate around the chromosome region. On your **left**, pieces of the nuclear envelope are separating and moving away. Directly **ahead**, the condensed replicated chromosomes drift inside the newly opened attachment zone. On your **right**, spindle microtubules extend inward from the poles and probe the chromosome region. The kinetochores you learned at the Chromosome Anatomy Workbench remain attached to the centromere region of each chromatid. They are now exposed to the spindle for the first time in this journey.",
  "As nuclear-envelope breakdown proceeds, spindle microtubules gain access to those kinetochores. Mira slows the model so you can watch an individual microtubule end contact a kinetochore and establish an attachment. Another microtubule reaches a kinetochore on a different chromatid. This interval is **prometaphase**. The name is attached to an unmistakable mechanical change. The nuclear barrier is gone enough for spindle microtubules to interact directly with chromosome attachment structures. Prometaphase therefore has its own visible job even though the broader AP stage sequence can be taught without requiring this name as a separate exam-recall item.",
  "The chromosomes begin moving, but Mira refuses to line them all up yet. Some are closer to one pole, some are being pulled from both sides, and others are still acquiring stable attachments. That disorder is intentional. It prevents the learner from turning any spindle attachment into metaphase. Prometaphase is the access-and-attachment interval. Metaphase will require a different spatial result, the collective positioning of chromosomes around the cell equator. The distinction also keeps the **mitotic spindle**, centrosomes, kinetochores, and the later metaphase plate from collapsing into one object. The spindle is the overall microtubule apparatus. The centrosomes are organizing centers in this animal-cell example. Kinetochores are chromosome-associated protein complexes where spindle microtubules attach.",
  "A set of tension indicators lights up beside the chromosomes. When opposite spindle poles influence an attached replicated chromosome, the indicator becomes balanced, but the chromosomes are still scattered. Mira turns the entire central floor into a transit track leading forward. At the far end, a thin glowing line appears across the middle of the next room. She warns you that it is only a reference plane, not a biological plate hiding inside the cell. The chromosomes now have spindle access and dynamic attachments. The remaining problem is where those attachments will position the replicated chromosomes before separation is permitted."
 ],
 'close':'Prometaphase opens the chromosome region and establishes spindle-microtubule attachment to kinetochores without completing equatorial alignment. Those attached chromosomes now move into Metaphase Plate Station.'
},
'U4-L37':{
 'title':'The Invisible Line at the Middle','kicker':'Metaphase is a position created by spindle forces, and the metaphase plate is an imaginary plane.',
 'paragraphs':[
  "The attachment track opens into **Metaphase Plate Station**, the most symmetrical room in the hall. A spindle pole is fixed on your **left**. The opposite spindle pole is fixed on your **right**. Directly **ahead**, the same replicated chromosomes occupy the central cell model. A narrow light projection crosses the equator from floor to ceiling. You can walk your hand through it because there is no material plate there. Mira labels the projection **metaphase plate** and immediately turns the projector off. The line disappears while the cell model remains. The term refers to an imaginary equatorial plane used to describe where chromosomes align during metaphase.",
  "Microtubules connected to kinetochores exert forces from opposite sides. One chromosome slides slightly left, another shifts right, and a third rotates until its centromere region is positioned near the middle. The whole replicated set gradually forms an ordered row relative to the invisible equatorial plane. That organized condition is **metaphase**. The important event is not the appearance of a physical plate. The spindle has positioned the chromosomes at the cell equator. The left and right poles therefore become useful fixed anchors. If you can redraw the poles and place the chromosomes between them at the equator, you can reconstruct the stage without relying on the name alone.",
  "Mira briefly scrambles one chromosome so its attachment is inadequate. A warning light appears over the central row and the separation gate stays closed. She restores the attachment and the warning clears. This does not yet teach the full spindle-assembly checkpoint, which belongs in the next security journey, but it gives the alignment room a biological reason to pause before anaphase. The chromosomes cannot simply be flung apart because a stage label changed. Their spindle attachments and positions must support accurate segregation. The sister chromatids themselves remain joined throughout this room, so each replicated chromosome still counts as one chromosome under centromere-based counting.",
  "The Quick Recall screen can now hide the room and ask one question. **What is the metaphase plate?** The answer is an imaginary equatorial plane where chromosomes align during metaphase. When the room returns, Mira draws the plane once more and then erases it. The physical memory is the pair of opposing spindle poles and the replicated chromosomes positioned between them. A low mechanical click travels through every sister-chromatid pair. Their connecting seams are about to release, which means the next room will change both chromosome movement and chromosome counting at the same moment."
 ],
 'close':'Metaphase leaves the replicated chromosomes aligned near an imaginary equatorial plane between opposite spindle poles. The separation system now receives permission to release sister chromatids, sending the same tracked set into Anaphase Separation Track.'
},
'U4-L38':{
 'title':'The Count Changes When the Sisters Part','kicker':'Anaphase changes chromosome identity and position at the instant sister chromatids separate.',
 'paragraphs':[
  "The center doors open onto **Anaphase Separation Track**, a long straight chamber with one pole on each end. On your **left**, one future daughter-chromosome set is marked by an empty receiving frame. Directly **ahead**, the replicated chromosomes remain momentarily paired at the center of the spindle. On your **right**, a matching receiving frame waits at the opposite pole. Three gauges hover above the chromosome set. One reports DNA amount. One reports chromatid state. The third reports chromosome number by centromere-based counting. Mira places her hand over the release control and asks you to watch the gauges at the exact instant the sister chromatids separate.",
  "The connecting seams release. Each sister pair splits, and the former sister chromatids begin moving toward opposite poles. This is **anaphase**. The terminology changes with the physical relationship. Before separation, each sister chromatid was one part of a replicated chromosome. After separation, each former chromatid is an individual **daughter chromosome**. The chromosome-count gauge jumps immediately. Within this still-undivided cell, chromosome count transiently doubles because the separated centromere-bearing structures are now counted as individual chromosomes. This is **chromosome counting at anaphase**. The DNA did not replicate again. The counting change comes from sister-chromatid separation.",
  "The movement itself unfolds through **anaphase spindle dynamics**. Kinetochore-associated microtubule dynamics contribute to movement of daughter chromosomes toward the poles. Spindle forces and motor activity also contribute, while other spindle microtubules can participate in elongating the cell. Mira deliberately disables any caption that says chromosomes move only because microtubules shorten. Shortening is important, but the complete movement is a coordinated spindle process. The left and right receiving frames fill with equivalent chromosome identities as the tracked blue-and-gold bands separate into opposite sets.",
  "The optional Quick Recall hides the gauges and asks what happens to chromosome counting when sister chromatids separate in anaphase. The correct reconstruction is that each former chromatid becomes a daughter chromosome, so chromosome count transiently doubles within the still-undivided cell. Mira then restores the full model. The count is temporarily high only because the cell still contains both daughter sets. No new DNA synthesis occurred. She places one transparent outline around the entire cell and two smaller future-cell outlines beyond it. The temporary chromosome count belongs to the one undivided cell in front of you. Once cytokinesis later produces two cells, each daughter receives the appropriate chromosome set. By the time the two sets settle at opposite ends, the central spindle is stretched between them and the old nuclear region is empty. The next task is no longer separation. Each daughter chromosome set now needs a nuclear environment restored around it while the chromosomes relax from their compact mitotic state."
 ],
 'close':'Anaphase has separated sister chromatids into daughter chromosomes and delivered equivalent sets toward opposite poles while the cell is still one cytoplasm. Those separated sets now enter Telophase Reassembly Room.'
},
'U4-L39':{
 'title':'Two Nuclei Return Before the Cell Splits','kicker':'Telophase rebuilds nuclei around already separated chromosome sets while the shared cytoplasm remains intact.',
 'paragraphs':[
  "The separation track widens into **Telophase Reassembly Room**. On your **left**, one complete daughter-chromosome set rests near one end of the cell. On your **right**, the equivalent set rests at the opposite end. Directly **ahead**, the spindle stretches through a shared central cytoplasm. There is still one continuous cell boundary around the entire room. Mira points to that boundary before anything else moves. The chromosomes have already separated during anaphase, but the cell itself has not yet been divided. This arrangement keeps nuclear reassembly and cytoplasmic division as two different events.",
  "The spindle begins to disassemble. Around the left chromosome set, membrane components organize into a new nuclear envelope. The same process occurs around the right set. Each set was already separate before these envelopes formed. The room now enters **telophase**. As nuclear compartments re-form, the compact daughter chromosomes begin decondensing toward less condensed chromatin. Mira makes the chromosomes fade gradually into a more diffuse state while keeping the artificial identity bands faintly visible. Decondensation changes packaging and visibility. It does not erase the chromosome identities that were tracked through the hall.",
  "A pair of nuclear outlines becomes complete, one on each side. The central spindle has largely disappeared, and the two future nuclei now contain equivalent chromosome sets. Mira walks a slow circle around the entire room so you can see the outer plasma membrane remains one continuous boundary. Two nuclei can therefore exist temporarily inside one shared cytoplasm. This is the critical picture that keeps **telophase** distinct from **cytokinesis**. Telophase concerns late mitotic reassembly around the separated chromosome sets. Cytokinesis will divide the cytoplasm and complete physical separation of the cell.",
  "Before leaving, Mira asks you to redraw the room without stage labels. One chromosome set belongs on the left inside a reforming nuclear envelope. The matching set belongs on the right inside a second reforming envelope. A fading spindle occupies the center, and one continuous cell boundary surrounds both. If that picture is correct, the term telophase has a physical meaning instead of becoming another word in a list. The floor then splits into two exit designs. The left-hand corridor displays a flexible animal-cell membrane with a tightening belt beneath it. The right-hand corridor displays a rigid plant cell wall surrounding a central construction zone. Mira chooses the animal corridor first because its mechanics make a useful contrast. She seals the two telophase nuclei inside a transparent model of one animal cell and rolls it forward. Nothing about the nuclei changes as the model moves. The unresolved problem is outside them. One cytoplasm still surrounds both nuclei, so the cell needs a mechanism that can constrict the flexible boundary and separate that shared cytoplasm into two daughter cells."
 ],
 'close':'Telophase restores nuclear envelopes and begins chromosome decondensation around two already separated chromosome sets while the cytoplasm remains continuous. The animal-cell model now moves into the Animal Cytokinesis Ring.'
},
'U4-L40':{
 'title':'The Cell Pinches From the Outside In','kicker':'Animal cytokinesis uses a contractile ring to draw a cleavage furrow inward through a flexible cell boundary.',
 'paragraphs':[
  "The animal-cell model enters **Animal Cytokinesis Ring**, a circular station built around a flexible plasma membrane. On your **left**, a belt-shaped structure assembles just beneath the cell cortex at the future division plane. Directly **ahead**, the middle of the cell narrows into a shallow indentation. On your **right**, two daughter-cell bays wait for the completed division. The two telophase nuclei remain visible throughout. Mira keeps them behind clear shields so the learner can see that chromosome segregation has already been accomplished. What remains is the division of the cytoplasm.",
  "The belt on the left is the **contractile ring**. It is composed mainly of actin filaments working with myosin motors. As the ring constricts, the plasma membrane is pulled inward at the division plane. The shallow indentation deepens. Mira names that inward groove the **cleavage furrow**. The furrow is a visible consequence of the contractile machinery beneath the cortex. The ring and the furrow therefore occupy separate places in the room. One is the force-generating structure. The other is the inward deformation of the cell surface that results from that constriction.",
  "The constriction continues until the shared cytoplasm becomes physically separated into two daughter cells. This cytoplasmic division is **cytokinesis**. Mira marks the term on the outer wall of the station, outside the mitosis-stage track. Cytokinesis can overlap late mitotic events, yet its defining job is division of the cytoplasm. It is not another chromosome-segregation stage. The tracked daughter nuclei end up one in each daughter cell because chromosome segregation has already positioned equivalent sets on opposite sides before the final cytoplasmic separation is completed.",
  "Mira freezes the two completed animal daughter cells and asks you to point backward through the mechanics. The daughter cells are the outcome on the right. The cleavage furrow was the inward indentation at center. The contractile ring beneath the cortex on the left generated the constricting force. That left-to-center-to-right reconstruction prevents the three terms from becoming interchangeable. Mira then resets the station and replaces the flexible animal-cell boundary with a thick, rigid plant cell wall. She tries to tighten the same contractile belt. Nothing useful happens. A rigid plant wall cannot simply be pinched inward by copying the animal mechanism. The failure is the transition clue. Animal cells commonly use an inward cleavage furrow driven by a contractile ring. Plant cells face a different structural problem, so their cytokinesis must build a new partition from inside the cell. The right wall opens onto a bright construction floor where stacks of Golgi-derived vesicles are already moving toward the center."
 ],
 'close':'Animal cytokinesis has separated the cytoplasm with an actin-myosin contractile ring that drives a cleavage furrow inward. A rigid plant-cell wall cannot use the same geometry, so the comparison moves directly into Plant Cell-Plate Works.'
},
'U4-L41':{
 'title':'The Wall Grows From the Middle Out','kicker':'Plant cytokinesis builds a new partition at the cell center and expands it outward toward the existing boundary.',
 'paragraphs':[
  "The final doors open into **Plant Cell-Plate Works**, a rectangular chamber enclosed by a rigid transparent wall. On your **left**, Golgi-derived vesicles travel along tracks toward the center. Directly **ahead**, the two daughter nuclei occupy opposite halves of one plant-cell model, and a narrow construction zone lies between them. On your **right**, the existing plasma membrane and parent cell wall form a rigid boundary that cannot be pulled inward like the membrane in the previous animal-cell station. Mira places a tiny image of the animal cleavage furrow beside the door and leaves it there as a comparison. The plant mechanism must solve the same cytoplasmic-division problem with a different physical design.",
  "Vesicles from the left arrive at the center and fuse with one another. Their membranes and contents create a growing partition called the **cell plate**. The plate begins near the middle of the cell and expands outward. More Golgi-derived vesicles arrive and add material. The direction is now the reverse of the animal visual you just saw. The animal furrow moved inward from the cell surface. The plant cell plate grows outward from the center. Mira keeps the rigid parent wall fixed while the new structure expands, making the geometry impossible to confuse.",
  "The growing cell plate eventually reaches the existing plasma membrane. Its membranes contribute to new plasma-membrane regions for the daughter cells, while deposited material contributes to the new wall separating them. The cytoplasm is now divided even though no contractile ring pinched the original cell wall inward. Mira places the word **cytokinesis** above both the animal and plant models, then places the mechanism names beneath them. Animal cells commonly form a cleavage furrow through contractile-ring constriction. Plant cells form a cell plate through vesicle fusion and outward growth. The shared concept is cytoplasmic division. The structures that accomplish it are different.",
  "For the final reconstruction, the lights along the whole Mitosis Transit Hall switch off one at a time. Mira asks you to walk the same chromosome identities forward in your mind. Replicated chromosomes condense during prophase as the spindle begins forming. Nuclear-envelope breakdown gives spindle microtubules access to kinetochores during prometaphase. Chromosomes align near the imaginary metaphase plate during metaphase. Sister chromatids separate in anaphase and become daughter chromosomes, changing chromosome counting inside the still-undivided cell. Telophase rebuilds nuclei around the separated sets. Cytokinesis then divides the cytoplasm, through a cleavage furrow in the animal model or a cell plate in the plant model. The daughter chromosome sets are equivalent because the same replicated set was tracked continuously through the route.",
  "At the far wall, two new doors appear above the completed daughter cells. Both are marked **SECURITY CHECK BEFORE ANOTHER CYCLE**. Mira slides the chromosome-tracking case into her tablet and looks back at the hall. Accurate movement is only half the problem. A cell also needs mechanisms that decide whether division should proceed at all. DNA damage, spindle attachment, growth signals, cyclin and CDK activity, apoptosis, and cancer-control failure are waiting behind those doors. The transit hall has delivered the chromosomes. The next journey will decide whether another trip is allowed to begin."
 ],
 'close':'Plant cytokinesis completes the comparison by building a cell plate from the center outward. With chromosome segregation and cytoplasmic division now reconstructed as separate but coordinated processes, the daughter-cell record passes to Cell-Cycle Security Headquarters.'
},
}

HINTS={
 'U4-L37':'Picture the invisible equatorial plane between the two spindle poles. It is a reference position, not a cellular structure.',
 'U4-L38':'Picture the instant the sister pairs split. The count changes because each former chromatid now has its own chromosome identity.'
}

TERM_IMAGES={}
for b in B.values():
    for t in b['term_introductions']:
        TERM_IMAGES[t['knowledge_id']]=f"At {b['scene_title']}, use the fixed {b['spatial_layout']['left']['anchor']} → {b['spatial_layout']['center']['anchor']} → {b['spatial_layout']['right']['anchor']} mechanism to retrieve {t['canonical_term']}."

def scene_layout(b):
    zones=[]
    for pos in ('left','center','right'):
        z=b['spatial_layout'][pos]
        stable=next((x for x in b['stable_cast'] if x['position']==pos),None)
        desc=(stable['visual_identity']+' '+stable['job_in_scene']) if stable else z['layout_job']
        zones.append({'position':pos,'label':z['anchor'],'description':desc})
    return {'orientation':f"Stand at the entrance to {b['scene_title']}. Keep {zones[0]['label']} on your left, {zones[1]['label']} directly ahead in the central action zone, and {zones[2]['label']} on your right. Do not rotate the room while the mechanism runs.",'zones':zones}

def cast_for(b):
    casts=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    for part in b['stable_cast']:
        casts.append({'name':part['name'],'kind':part['type'].lower(),'visual':part['visual_identity'],'job':part['job_in_scene']})
    casts.append(dict(TRACKED))
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
      'scene_layout':scene_layout(b),'cast':cast_for(b),'continuity_object':J6['continuity_object'],
      'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':beats,'memory_snapshot':snaps,
      'misconception_guards':b['misconception_guards'],'exit_memory':b['exit_memory'],
      'checkpoint':cp,'checkpoint_object_id':b['primary_knowledge_id'],'checkpoint_prompt':qr.get('candidate_prompt','') if cp else '',
      'checkpoint_answer':qr.get('answer','') if cp else '','checkpoint_hint':HINTS.get(lid,'') if cp else '',
      'next_locus':B[b['causal_transition']['to_locus_id']]['scene_title'] if b['causal_transition']['to_locus_id'] else None,
      'causal_transition':b['causal_transition']['transition_logic']
    }

lids=J6['route']; scenes=[make_scene(lid,i) for i,lid in enumerate(lids)]
journey={
 'palace_id':'U4-J6','palace_name':'Mitosis Transit Hall','story_title':'The Transit Hall With the Stages Out of Order',
 'tagline':'The same replicated chromosomes must survive one continuous trip through spindle formation, attachment, alignment, separation, nuclear reassembly, and two contrasting forms of cytokinesis.',
 'guide':GUIDE,
 'premise':'The mitosis transit hall has lost the order of its stage signals. Replicated chromosomes are being routed toward daughter nuclei, but attachment, alignment, separation, reassembly, and cytoplasmic division are occurring out of sequence. Mira transfers the same replicated chromosome set from Journey 5 into the hall and refuses to replace it with a new model at any stage.',
 'mission':'Carry one replicated chromosome set from mitotic entry to daughter cells. Preserve chromosome identity while prophase builds the spindle, prometaphase opens kinetochore access, metaphase establishes equatorial alignment, anaphase separates sister chromatids into daughter chromosomes, telophase rebuilds nuclei, and animal and plant cytokinesis divide cytoplasm through different mechanisms.',
 'finale':'At the transit exit, the learner can reconstruct the same chromosome identities through the full route and can explain why stage names correspond to different physical chromosome and spindle states. Mitosis segregates replicated chromosomes into equivalent daughter-nucleus sets, chromosome count changes when sister chromatids separate in anaphase, telophase can produce two nuclei inside one shared cytoplasm, and cytokinesis then divides that cytoplasm through an inward cleavage furrow in the animal model or an outward-growing cell plate in the plant model.',
 'estimated_minutes':34,'scene_count':len(scenes),'checkpoint_count':sum(bool(s['checkpoint']) for s in scenes),
 'learner_rule':'Read or listen while following the same replicated chromosome set. Reconstruct the fixed left, center, and right geometry at each station before naming the stage. Quick Recall is optional during first exposure.',
 'route_orientation':'The Mitosis Transit Hall is one continuous eight-location route. Enter at Mission Control, follow the same replicated chromosomes through prophase, prometaphase, metaphase, anaphase, and telophase, then compare animal cytokinesis with plant cytokinesis before handing the daughter-cell record to Cell-Cycle Security Headquarters.',
 'route':route,'scenes':scenes,'student_release':'DEVELOPER_PREVIEW_F4F','narrative_standard':'V2-NARRATIVE-4.5-U4-F4F'
}
(U4/'journeys'/'U4-J6.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def card(j): return {k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
allj=(J1,J2,J3,J4,J5,journey)
registry={'schema':'memory-palace-v2-unit4-f4f-registry-1.0','course_id':'ap-biology','unit_id':'unit-4','unit_title':'Cell Communication and Cell Cycle','narrative_standard':'V2-NARRATIVE-4.x-U4-F4F','journey_count':6,'scene_count':sum(x['scene_count'] for x in allj),'checkpoint_count':sum(x['checkpoint_count'] for x in allj),'guided_journeys':[card(x) for x in allj]}
(U4/'journeys-f4f.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U4/'status-f4e.json').read_text(encoding='utf-8'))
status.update({'status':'F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW','pipeline_status':'POLISHED_NARRATIVE_F4F','narrative_lock':'LOCKED_F4F_J1_J2_J3_J4_J5_J6','student_release':False,'preview_release':True,'journey_count':6,'scene_count':41,'polished_journeys':6,'polished_scenes':41,'polished_checkpoint_count':15,'narrative_story_files':6,'next_required_output':'F4G polished narrative for Journey 7 only after F4F prose QA; Journeys 1–6 remain locked unchanged'})
(U4/'status-f4f.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(U4/'status.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; course=json.loads(cp.read_text(encoding='utf-8'))
for u in course['units']:
    if u['unit_id']=='unit-4':
        u.update({'status':'F4F_JOURNEYS1_6_POLISHED_DEVELOPER_PREVIEW','journey_count':6,'scene_count':41,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEYS1_6_POLISHED_F4F','polished_journeys':6,'polished_scenes':41,'student_release':False,'preview_release':True,'canonical_records':180})
cp.write_text(json.dumps(course,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

files=['journeys/U4-J1.json','journeys/U4-J2.json','journeys/U4-J3.json','journeys/U4-J4.json','journeys/U4-J5.json','journeys/U4-J6.json','journeys-f4f.json','status-f4f.json']
lock={'schema':'memory-palace-v2-unit4-f4f-content-lock-1.0','unit_id':'unit-4','stage':'F4F','lock_status':'LOCKED_F4F_J1_J2_J3_J4_J5_J6','student_release':False,'preview_release':True,'protected_predecessors':{rel:LOCK_E['files'][rel] for rel in ('journeys/U4-J1.json','journeys/U4-J2.json','journeys/U4-J3.json','journeys/U4-J4.json','journeys/U4-J5.json')},'files':{f:{'bytes':(U4/f).stat().st_size,'sha256':sha(U4/f)} for f in files}}
(U4/'content-lock-f4f.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit4-f4f-release-manifest-1.0','unit_id':'unit-4','stage':'F4F','student_release':False,'preview_release':True,'canonical_records_protected':180,'polished_journeys':6,'polished_scenes':41,'journey_6_records':sum(len(s['object_ids']) for s in scenes),'journey_6_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'journey_6_narrative_words':sum(len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs']))) for s in scenes),'next_stage':'F4G_JOURNEY7_AFTER_F4F_QA'}
(U4/'f4f-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')

doc=['# Unit 4 F4F · Journey 6 Narrative','',f"## {journey['story_title']}",'',journey['tagline'],'',f"**Guide**  {GUIDE['name']}, {GUIDE['role']}",'',f"**Premise**  {journey['premise']}",'',f"**Mission**  {journey['mission']}",'',f"**Route**  {' → '.join(r['locus'] for r in route)}",'', '> F4F is a developer narrative preview. Unit 4 remains `student_release: false`. Journeys 1–5 are protected byte-for-byte from F4E.','']
for s in scenes:
    doc += [f"## {s['scene_index']+1}. {s['locus']}",'',f"### {s['title']}",'',f"*{s['scene_kicker']}*",'',f"**Physical layout**  {s['scene_layout']['orientation']}",'']
    for p in s['story_paragraphs']: doc += [p,'']
    doc += [f"**Exit**  {s['story_close']}",'']
    if s['checkpoint']: doc += [f"**Optional Quick Recall**  {s['checkpoint_prompt']}",'']
doc += ['## Journey payoff','',journey['finale'],'']
(ROOT/'docs'/'UNIT4_F4F_JOURNEY6_STORY.md').write_text('\n'.join(doc),encoding='utf-8')

release_doc=f'''# Unit 4 F4F Release

## Scope

F4F adds only **Journey 6, Mitosis Transit Hall**. Journeys 1–5 remain protected byte-for-byte from F4E. F1 science, F2 architecture, and F3 scene briefs remain locked. Journey 7 is not polished in this stage.

## Narrative release

- Journey 6 title: **{journey['story_title']}**
- Polished journeys: **6 / 7**
- Polished scenes: **41 / 51**
- Journey 6 knowledge records: **{manifest['journey_6_records']}**
- Journey 6 narrative words: **{manifest['journey_6_narrative_words']}**
- Journey 6 optional first-exposure recalls: **{manifest['journey_6_checkpoints']}**
- Student release: **false**
- Developer preview: **true**

## Narrative standard

Journey 6 uses the same replicated chromosome set from Journey 5 throughout the complete mitotic route. Prophase, prometaphase, metaphase, anaphase, and telophase remain spatially distinct. Spindle, centrosome, kinetochore, and metaphase plate remain different structures or reference concepts. Sister chromatids become daughter chromosomes when they separate in anaphase, and cytokinesis remains separate from nuclear chromosome segregation. Animal cleavage-furrow mechanics and plant cell-plate mechanics are compared directly without forcing one mechanism onto the other.

## Next gate

F4G may author **Journey 7, Cell-Cycle Security Headquarters** only after F4F passes prose QA. Journeys 1–6 must remain unchanged.
'''
(ROOT/'docs'/'UNIT4_F4F_RELEASE.md').write_text(release_doc,encoding='utf-8')
print('Built Unit 4 F4F',json.dumps(manifest,indent=2))
