from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
briefs=json.loads((U2/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
jbriefs=json.loads((U2/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
B={s['locus_id']:s for s in briefs if s['journey_id']=='U2-J7'}
J7=next(j for j in jbriefs if j['journey_id']=='U2-J7')

GUIDE={
 'name':'Dr. Nia Park','role':'cell-systems investigator',
 'visual':'navy field jacket, clear safety glasses, and a compact tablet displaying a transparent map of the cell',
 'story_job':'Nia keeps the route physically clear, asks you to predict what will happen, and names scientific terms only after the defining structure or action is visible.'
}

route=[
 {'scene_index':0,'locus':'Compartmentalization Lab','short':'Compartment Lab','floor':'Archive ground floor','symbol':'▦'},
 {'scene_index':1,'locus':'Internal Organization Comparison Room','short':'Cell Comparison','floor':'Comparative records hall','symbol':'◧'},
 {'scene_index':2,'locus':'Endosymbiosis Origin Theater','short':'Origin Theater','floor':'Historical reconstruction theater','symbol':'◎'},
 {'scene_index':3,'locus':'Endosymbiotic Evidence Vault','short':'Evidence Vault','floor':'Sealed evidence chamber','symbol':'◆'},
]

SCENE_META={
'U2-L46':('Compartmentalization Lab','Archive ground floor','Compartmentalization Lab, the archive’s ground-floor reaction laboratory where reaction chamber A fills the left wall, a transparent folding membrane system occupies the center bench, and reaction chamber B remains fixed against the right wall.'),
'U2-L47':('Internal Organization Comparison Room','Comparative records hall','Internal Organization Comparison Room, directly beyond the reaction lab, where a magnified prokaryotic cell model occupies the left platform, a comparison table runs through the center, and a eukaryotic cell opened into membrane-bound rooms stands on the right.'),
'U2-L48':('Endosymbiosis Origin Theater','Historical reconstruction theater','Endosymbiosis Origin Theater, a dark semicircular archive theater where an ancestral host cell is projected on the left, the engulfment-and-retention reconstruction occurs on the center stage, and the descendant organelle condition appears on the illuminated right screen.'),
'U2-L49':('Endosymbiotic Evidence Vault','Sealed evidence chamber','Endosymbiotic Evidence Vault, the final steel-lined archive room where genome and division evidence fill the left case, ribosome and membrane evidence occupy the central wall, and a host-dependence display seals the right side of the room.')
}

ZONE_COPY={
'U2-L46':[
 ('left','Reaction chamber A','A','A transparent chamber contains one enzyme system and its substrates, isolated on the left so its reactions can be watched without the second system interfering.'),
 ('center','Internal membrane divider','FOLDED MEMBRANE','A flexible internal membrane rises through the center bench, first separating the chambers and then folding repeatedly to create additional membrane surface for reaction machinery.'),
 ('right','Reaction chamber B','B','A second transparent chamber contains a different enzyme system on the right, allowing both reaction environments to operate side by side while remaining physically separated.')],
'U2-L47':[
 ('left','Prokaryotic cell model','PROKARYOTE','A magnified prokaryotic cell shows localized internal regions, ribosomes, DNA-containing space, and organized structures without the extensive membrane-bound organelles seen across the room.'),
 ('center','Organization comparison table','COMPARE','A lit table connects functions to their locations in each cell type so internal organization can be compared without reducing the prokaryote to an empty bag.'),
 ('right','Eukaryotic cell model','EUKARYOTE','A cutaway eukaryotic cell contains numerous membrane-bound compartments whose boundaries partition different cellular processes into distinct internal regions.')],
'U2-L48':[
 ('left','Ancestral host cell','HOST','A large ancestral host-cell reconstruction waits on the left side of the theater while a smaller independently living prokaryotic cell remains outside it.'),
 ('center','Engulfment and retention stage','RETAINED','The host membrane curves around the smaller cell at center; the engulfed cell remains intact and persists rather than being immediately broken down.'),
 ('right','Integrated descendant organelle','INTEGRATED','A sequence of later generations appears on the right, showing the once-independent partner becoming increasingly integrated with the host lineage and its cellular functions.')],
'U2-L49':[
 ('left','Genome and division case','DNA + DIVISION','Circular organelle DNA sits beside a time-lapse sequence of mitochondria and chloroplasts dividing in ways similar to bacterial binary fission.'),
 ('center','Ribosome and membrane wall','RIBOSOMES + MEMBRANES','A molecular display compares organelle ribosomes with bacterial-like features and places double organelle membranes beside structural similarities consistent with an engulfment history.'),
 ('right','Modern host-dependence panel','HOST INTEGRATION','A final network map shows genes and functions distributed between organelles and the host nucleus, making modern mitochondria and chloroplasts visibly dependent on the cell that contains them.')],
}

CAST={
'U2-L46':[
 ('internal membrane divider','scientific part','a transparent membrane sheet that can rise, seal, and fold between two reaction chambers','separate different reaction environments and then expand the available membrane surface'),
 ('enzyme system A','scientific part','blue enzyme complexes operating only in the left reaction chamber','carry out one modeled reaction sequence without colliding with the second system'),
 ('enzyme system B','scientific part','amber enzyme complexes operating only in the right reaction chamber','carry out a different modeled reaction sequence in its own compartment'),
 ('folded membrane surface','scientific structure','the same central membrane folded into a long series of ridges','provide additional membrane area where membrane-associated reaction machinery can be placed')],
'U2-L47':[
 ('prokaryotic model','scientific model','a large transparent cell lacking typical eukaryotic membrane-bound organelles but showing DNA, ribosomes, localized regions, and organized structures','show that prokaryotic cells possess internal organization without extensive eukaryotic-style membrane compartments'),
 ('comparison table','scientific instrument','a central illuminated table that links cellular jobs to locations in both models','force a function-by-function comparison instead of an organized-versus-unorganized caricature'),
 ('eukaryotic model','scientific model','a cutaway cell divided by internal membranes into visibly distinct organelles','show extensive membrane-bound compartmentalization of cellular functions')],
'U2-L48':[
 ('ancestral host cell','historical model','a large ancestral cell projected with a flexible outer membrane','represent the host lineage in the reconstructed evolutionary sequence'),
 ('free-living prokaryote','historical model','a smaller bacterium-like cell with its own DNA and ribosomes, initially living independently outside the host','represent an ancestral endosymbiont before engulfment'),
 ('retained endosymbiont','continuity object','the same small cell now enclosed inside the host but still intact','make persistence after engulfment visible before long-term integration is introduced'),
 ('evidence case','continuity object','a black archival case carried by you from the theater to the vault','collect the evidence needed to judge the historical explanation rather than accepting the reconstruction on appearance alone')],
'U2-L49':[
 ('evidence case','continuity object','the black case from the origin theater with five empty illuminated slots','hold independent evidence cards until the endosymbiotic explanation is supported by converging observations'),
 ('circular organelle DNA','scientific evidence','small circular DNA molecules displayed inside mitochondria and chloroplasts','support ancestry from bacterial endosymbionts'),
 ('division sequence','scientific evidence','a time-lapse of an organelle elongating, constricting, and dividing','show similarities between organelle replication and bacterial binary fission'),
 ('organelle ribosomes','scientific evidence','ribosomes whose features are compared directly with bacterial and eukaryotic cytosolic ribosomes','provide molecular evidence consistent with bacterial ancestry'),
 ('double membranes','scientific evidence','outer and inner organelle membranes displayed as nested boundaries','provide structural evidence consistent with engulfment and later integration'),
 ('host-dependence network','scientific evidence','a web connecting organelle genes and functions to genes and products supplied by the host nucleus','show that modern mitochondria and chloroplasts are deeply integrated organelles, not autonomous free-living cells')],
}

NARR={
'U2-L46':{
 'title':'The room where every reaction is colliding','kicker':'The archive’s first experiment has been stripped of its internal walls, and two reaction systems are now interfering in the same crowded chamber.',
 'paragraphs':[
  'The final wing of the Cell Operations Complex does not look like an archive at first. It looks like a laboratory after someone removed every interior wall. On your left, blue enzyme complexes race around a transparent chamber marked A. On your right, amber enzyme complexes are supposed to run a different reaction in chamber B. But there is no chamber B anymore. Both systems have spilled into one open space. Blue substrates drift into amber machinery. Amber products wander through the blue reaction line. Warning lights flash whenever one process disrupts the other. In the center of the room, a clear membrane sheet lies collapsed on the floor like a divider that someone deliberately took down.',
  'Dr. Nia Park kneels beside the membrane and raises it with both hands. The sheet rises through the center bench until it seals from floor to ceiling. Blue enzymes and their substrates remain on the left. Amber enzymes and theirs remain on the right. Almost immediately, the interference alarms stop. Nothing magical happened to the enzymes. The change was spatial. The membrane created two different internal environments, allowing different reaction systems to operate without constantly mixing. Nia taps the barrier. “When membranes divide a eukaryotic cell into specialized internal spaces, that organization is **compartmentalization**.” Membranes and membrane-bound organelles compartmentalize intracellular metabolic processes and specific enzymatic reactions in eukaryotic cells.',
  'She does not leave the divider flat. A motor catches its lower edge and pushes more membrane upward. Instead of expanding the whole room, the membrane folds back and forth into deep transparent ridges. Nia clips rows of reaction complexes onto the new folds. The room’s outside dimensions have barely changed, yet far more membrane-associated machinery now fits inside. The first advantage is therefore separation. Internal membranes can keep potentially competing reactions apart, **minimizing competing interactions**. The second advantage is geometric. Folding internal membranes can provide **increasing reaction surface**, giving membrane-associated cellular processes more surface area on which to occur.',
  'You step between the two chambers and look through the clear divider. The left reaction is still visible. The right reaction is still visible. Their separation has not made the cell less active; it has made different activities easier to organize. Nia points toward a door that has just unlocked beyond chamber B. Its sign reads INTERNAL ORGANIZATION COMPARISON. “One caution before we leave,” she says. “Membrane-bound organelles are a powerful form of compartmentalization in eukaryotes. They are not the only way a cell can have spatial organization.” The door opens onto two giant cell models waiting side by side.'
 ],
 'close':'The useful image is a divided laboratory whose central membrane does two jobs at once: it separates reaction environments and, when folded, creates more usable membrane surface without requiring a matching increase in cell volume.',
 'images':{
  'Compartmentalization':'the transparent divider rising between the blue and amber reaction systems until the interference alarms stop',
  'Minimizing competing interactions':'blue and amber enzyme systems continuing separately on opposite sides of the membrane instead of colliding in one chamber',
  'Increasing reaction surface':'the same internal membrane folding into many ridges so additional reaction complexes can attach without enlarging the room'
 }},
'U2-L47':{
 'title':'The cell that was mislabeled empty','kicker':'One comparison model has been reduced to an empty sack simply because it lacks the extensive membrane-bound organelles of the cell beside it.',
 'paragraphs':[
  'The next room is long and white, with two cell models facing one another across an illuminated comparison table. The right model is unmistakably eukaryotic. Its interior is divided into membrane-bound compartments, each outlined in a different color. The left model is labeled PROKARYOTE, but someone has rendered its inside as a blank gray bag. Nia stops so abruptly that you nearly walk into her. “That picture would make the comparison easy,” she says, “and wrong.” She switches off the blank rendering.',
  'The left cell becomes transparent. DNA occupies a defined region. Ribosomes fill the cytoplasm. Other localized structures and organized regions become visible. There still are no typical eukaryotic membrane-bound organelles dividing the interior into a nucleus, Golgi complex, mitochondria, and the other rooms you have already visited. But the cell is not unorganized. Nia places the first comparison card on the center table: **prokaryotic compartmentalization**. Prokaryotes typically lack internal membrane-bound organelles but have internal regions with specialized structures and functions. The exact form of organization differs from the extensive membrane-bound architecture across the room.',
  'Now the right model opens wider. Internal membranes partition the eukaryotic cell into specialized spaces. The nucleus encloses genetic material. Other membrane-bound organelles create distinct environments for different processes. Nia places a second card beside the first: **eukaryotic compartmentalization**. Eukaryotic cells maintain internal membranes that partition the cell into specialized regions. The table draws a line between the two models and replaces the labels ORGANIZED and UNORGANIZED with two more accurate questions: “Where is the function localized?” and “Is it enclosed by a membrane-bound compartment?”',
  'You walk once around the table. From the back, the difference is even clearer. The prokaryotic model uses organized internal regions without the extensive internal membrane system of the eukaryotic model. The eukaryotic model uses membranes again and again to make distinct internal spaces. Nia closes the comparison display, but the two cards stay in the black evidence case you are carrying. A wall ahead darkens and becomes a theater screen. On the left appears a large ancestral host cell. Beside it, outside the host, glows a much smaller independently living prokaryotic cell. “Now we can ask a different question,” Nia says. “Where did some of those eukaryotic compartments come from?”'
 ],
 'close':'Both models are organized cells. The memorable difference is that eukaryotes extensively partition functions into membrane-bound organelles, while prokaryotes usually lack those typical membrane-bound organelles yet still contain specialized internal regions and structures.',
 'images':{
  'Prokaryotic compartmentalization':'the supposedly empty prokaryotic model lighting up with DNA, ribosomes, and localized internal regions despite lacking typical eukaryotic membrane-bound organelles',
  'Eukaryotic compartmentalization':'the neighboring eukaryotic model opening into many membrane-bound internal rooms that partition different cellular functions'
 }},
'U2-L48':{
 'title':'The cell inside the cell','kicker':'A historical reconstruction begins with two separate cells and ends with one partner permanently integrated inside the other, but the reconstruction must still be tested against evidence.',
 'paragraphs':[
  'The lights drop until the **Endosymbiosis Origin Theater** is almost black. Your evidence case rests on your knees. On the left side of the stage, a large ancestral host cell turns slowly in projection. Several meters away from it, a smaller prokaryotic cell moves independently through the surrounding environment. The two are unmistakably separate organisms in the opening reconstruction. Nia stands beside the projector controls. “What you are about to see is a model of an ancient evolutionary process,” she says. “No one watched the original events happen. The reconstruction is useful only if evidence from living cells supports it.”',
  'The smaller cell approaches the host. At center stage, the host membrane bends inward and surrounds it. For a moment the image resembles ordinary engulfment. Then the expected destruction never comes. The engulfed cell remains intact inside the host. Its own internal machinery continues functioning. The theater advances through many generations rather than jumping directly to a modern organelle. The retained partner is passed along as host cells reproduce. Over evolutionary time, the relationship becomes increasingly integrated. The once-independent cell no longer appears as a visitor that can simply leave. It has become part of the host cell’s internal system.',
  'Nia freezes the sequence with three images visible at once: independent cell on the left, retained cell inside the host at center, integrated descendant condition on the right. “This evolutionary relationship is **endosymbiosis**,” she says. Mitochondria and chloroplasts evolved from once free-living prokaryotic cells through endosymbiosis. The theater does not portray one modern mitochondrion or chloroplast deciding to move into a cell. It portrays an evolutionary explanation involving ancestral lineages and long-term integration across generations.',
  'The reconstruction rewinds. This time you watch only the boundaries. The smaller cell begins with its own membrane. The host membrane surrounds it during engulfment. Then the screen goes dark before showing any evidence for the historical claim. A red question appears over the stage: HOW WOULD YOU KNOW? Nia lifts the black case. It still contains only the two organization cards from the previous room. “A plausible story is not enough,” she says. “We need independent observations that converge on the same explanation.” The theater doors open directly into a steel evidence vault. Five empty slots glow inside your case.'
 ],
 'close':'Endosymbiosis is the evolutionary explanation that ancestral free-living prokaryotic cells were retained inside host cells and, across generations, became integrated organelles. The theater is a reconstruction; the next room determines whether multiple lines of evidence support it.',
 'images':{
  'Endosymbiosis':'the same smaller prokaryotic cell shown first living independently, then retained inside a host after engulfment, and finally integrated across later generations'
 }},
'U2-L49':{
 'title':'Five locks on one evolutionary case','kicker':'The vault will not seal the endosymbiosis case until several independent observations fit the same ancestry hypothesis and the final panel explains why modern organelles are no longer free-living cells.',
 'paragraphs':[
  'The **Endosymbiotic Evidence Vault** closes behind you with a heavy metallic thud. Your black evidence case unfolds on a central pedestal. Five empty slots glow along its lid. The first wall, on your left, contains a mitochondrion and chloroplast enlarged until you can see small DNA molecules inside them. Their DNA is circular. Nia slides the first card into the case: **endosymbiotic evidence from genomes**. Mitochondria and chloroplasts contain their own circular DNA, a feature consistent with descent from bacterial endosymbionts. One slot turns green. The other four remain dark.',
  'Beside the DNA display, a time-lapse begins. An organelle elongates, constricts through the middle, and separates. Another does the same. The sequence is compared with bacterial division. Nia inserts the second card: **endosymbiotic evidence from division**. Mitochondria and chloroplasts replicate by division processes similar to bacterial binary fission. A second lock releases. Nia does not close the case. “Circular DNA plus division is stronger than either observation alone,” she says, “but we are still building a converging argument.”',
  'You move to the central evidence wall. Three ribosome models appear side by side: a bacterial ribosome, an organelle ribosome, and a eukaryotic cytosolic ribosome. Molecular features align more closely between the bacterial and organelle models. The third card slides into place: **endosymbiotic evidence from ribosomes**. Mitochondrial and chloroplast ribosomes have features more similar to bacterial ribosomes than to eukaryotic cytosolic ribosomes. Below them, a structural model reveals the organelles’ double membranes and inner-membrane characteristics consistent with an engulfment-and-integration history. The fourth card becomes **endosymbiotic evidence from membranes**. The case now holds genomic, reproductive, ribosomal, and membrane evidence that point in the same evolutionary direction.',
  'Only the right side remains. A final display tries to show a mitochondrion leaving a modern eukaryotic cell and surviving independently. It fails immediately. Nia replaces the animation with a network. Some genes and functions remain in the organelle. Many others are supplied through the host cell and its nucleus. Proteins and regulatory systems cross the network in both directions. The last card reads **modern organelle dependence**. Modern mitochondria and chloroplasts are deeply integrated with their host cells and are not generally capable of independent free-living existence. Their bacterial ancestry does not make them modern free-living bacteria trapped inside a cell.',
  'All five slots turn green, and the case finally closes. Nia lays the theater reconstruction beside the evidence cards. None of the cards alone is treated as a complete proof. Together, circular organelle DNA, bacterial-like division, bacterial-like ribosome features, membrane evidence, and extensive modern host integration create a coherent explanation for organelle origins. The vault lights change from red to white. Through the glass behind the pedestal you can see fragments of every Unit 2 journey: internal membranes, mitochondria, chloroplasts, cell-size models, membrane travelers, pumps, water-potential chambers. The final archive has connected them. Cells organize space, exchange matter across boundaries, maintain gradients, balance water, and in eukaryotes carry organelles whose evolutionary history is written into their structure and molecular machinery.'
 ],
 'close':'Seal the case with converging evidence, not with a single clue: circular organelle DNA, bacterial-like division, bacterial-like ribosome features, membrane evidence, and modern host dependence together support the endosymbiotic origin of mitochondria and chloroplasts while showing how thoroughly those organelles are now integrated with eukaryotic cells.',
 'images':{
  'Endosymbiotic evidence: genomes':'the first vault slot turning green when circular DNA is revealed inside mitochondria and chloroplasts',
  'Endosymbiotic evidence: division':'the second slot opening beside a time-lapse of organelles constricting and dividing in a bacteria-like pattern',
  'Endosymbiotic evidence: ribosomes':'the bacterial and organelle ribosome models aligning more closely than the eukaryotic cytosolic ribosome beside them',
  'Endosymbiotic evidence: membranes':'the fourth evidence card placed beneath a model of double organelle membranes and inner-membrane similarities consistent with engulfment history',
  'Modern organelle dependence':'the final network showing genes and functions shared between organelles and the host nucleus, preventing the organelle from being pictured as an autonomous free-living cell'
 }}
}

CHECKPOINT_HINTS={
'U2-L48':'Return to the theater’s three frozen images: a smaller prokaryotic cell begins outside a host, is surrounded and retained inside the host, and appears in later generations as an increasingly integrated cellular partner.',
'U2-L49':'Picture the black evidence case in the final vault. Separate slots light for circular organelle DNA, bacteria-like division, bacteria-like ribosome features, and double-membrane evidence; no single slot closes the case by itself.'
}

lids=[f'U2-L{i}' for i in range(46,50)]
scenes=[]
for idx,lid in enumerate(lids):
    b=B[lid]; n=NARR[lid]; locus,floor,locdesc=SCENE_META[lid]
    zones=[{'position':pos,'label':lab,'symbol':sym,'description':desc} for pos,lab,sym,desc in ZONE_COPY[lid]]
    cast=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    cast += [{'name':name,'kind':kind,'visual':visual,'job':job} for name,kind,visual,job in CAST[lid]]
    beats=[]; snaps=[]
    for t in b['term_introductions']:
        image=n['images'].get(t['canonical_term'], b['science_bearing_action']['during'][0])
        beats.append({'object_id':t['knowledge_id'],'term':t['canonical_term'],'story':image,'science':t['canonical_science'],'exact_name':t['exact_name_recall'],'hint':image})
        snaps.append({'term':t['canonical_term'],'meaning':t['canonical_science'],'image':image})
    qr=b['quick_recall']; checkpoint=bool(qr.get('enabled'))
    next_id=b['causal_transition']['to_locus_id']
    scenes.append({
      'scene_index':idx,'locus':locus,'title':n['title'],'scene_kicker':n['kicker'],'location_description':locdesc,
      'scene_layout':{'orientation':b['orientation_sentence'],'zones':zones},'cast':cast,
      'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':beats,'memory_snapshot':snaps,
      'checkpoint':checkpoint,'checkpoint_object_id':b['primary_knowledge_id'],'checkpoint_prompt':qr.get('candidate_prompt','') if checkpoint else '',
      'checkpoint_answer':qr.get('answer','') if checkpoint else '','checkpoint_hint':CHECKPOINT_HINTS.get(lid,'') if checkpoint else '',
      'next_locus':B[next_id]['scene_title'] if next_id in B else None,'misconception_guards':b['misconception_guards'],
      'required_visual':b['visual_spec'],'carry_forward':b['carry_forward']
    })

journey={
 'schema':'memory-palace-v2-unit2-f4g-story-1.0','unit_id':'unit-2','palace_id':'U2-J7','journey_id':'U2-J7','palace_name':'Compartment Origins Archive',
 'story_title':'The Case of the Cell Within the Cell','tagline':'Repair a laboratory whose reactions have lost their internal boundaries, compare two forms of cellular organization, then carry an evidence case through a reconstruction of endosymbiosis and a vault of independent clues.',
 'guide':GUIDE,'premise':J7['premise'],'mission':J7['mission'],
 'finale':'The archive closes only after compartmentalization is understood as useful cellular organization and the endosymbiosis case is supported by converging genomic, division, ribosomal, membrane, and host-integration evidence rather than by the historical reconstruction alone.',
 'estimated_minutes':11,'scene_count':len(scenes),'checkpoint_count':sum(bool(s['checkpoint']) for s in scenes),
 'learner_rule':'Read or listen while keeping the black evidence case with you. First understand why cells organize chemistry in space. Then treat the endosymbiosis theater as a historical reconstruction whose explanation must be tested against several independent observations. Quick Recall is optional during the first pass.',
 'route_orientation':'The Compartment Origins Archive is a four-room route. Begin in the ground-floor reaction laboratory, pass directly into the side-by-side cell comparison hall, enter the dark historical reconstruction theater, then carry the same black evidence case through the steel doors into the final evidence vault.',
 'route':route,'scenes':scenes,'student_release':'PILOT_PREVIEW_F4G','narrative_standard':'V2-NARRATIVE-3.0-F4G'
}

(U2/'journeys').mkdir(parents=True,exist_ok=True)
(U2/'journeys'/'U2-J7.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

js=[json.loads((U2/'journeys'/f'U2-J{i}.json').read_text(encoding='utf-8')) for i in range(1,7)]+[journey]
def card(j): return {k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
registry={'schema':'memory-palace-v2-unit2-f4g-registry-1.0','course_id':'ap-biology','unit_id':'unit-2','unit_title':'Cells','narrative_standard':'V2-NARRATIVE-3.0-F4G','journey_count':7,'scene_count':sum(j['scene_count'] for j in js),'checkpoint_count':sum(j['checkpoint_count'] for j in js),'guided_journeys':[card(j) for j in js]}
(U2/'journeys-f4g.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U2/'status-f4f.json').read_text(encoding='utf-8'))
status.update({'status':'F4G_ALL_7_JOURNEYS_POLISHED_PREVIEW','pipeline_stage':'ALL_POLISHED_NARRATIVES_COMPLETE_F4G','student_release':False,'preview_release':True,'polished_journeys':7,'polished_scenes':49,'polished_checkpoint_count':17,'narrative_story_files':7,'palace_managed_records_covered':133,'next_required_output':'F5 Unit 2 finalization: Challenge Lab, mixed discrimination/review integration, full release audit, and student-release gate','next_gate':'F5 finalization only after all seven F4 narratives pass prose QA and full regression testing'})
(U2/'status-f4g.json').write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; c=json.loads(cp.read_text(encoding='utf-8'))
for u in c['units']:
    if u['unit_id']=='unit-2':
        u.update({'status':'F4G_ALL_7_JOURNEYS_POLISHED_PREVIEW','journey_count':7,'scene_count':49,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_ALL_7_JOURNEYS_POLISHED_F4G','polished_journeys':7,'polished_scenes':49})
cp.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
files=['journeys/U2-J7.json','journeys-f4g.json','status-f4g.json']
lock={'schema':'memory-palace-v2-unit2-f4g-content-lock-1.0','unit_id':'unit-2','stage':'F4G','student_release':False,'files':{f:sha(U2/f) for f in files}}
(U2/'content-lock-f4g.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit2-f4g-release-manifest-1.0','unit_id':'unit-2','stage':'F4G','student_release':False,'preview_release':True,'polished_journeys':7,'polished_scenes':49,'palace_managed_records_covered':133,'journey_7_records':sum(len(s['object_ids']) for s in scenes),'journey_7_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'next_stage':'F5_UNIT2_FINALIZATION'}
(U2/'f4g-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Built Unit 2 F4G:',len(scenes),'Journey 7 scenes',sum(len(s['object_ids']) for s in scenes),'knowledge records',sum(bool(s['checkpoint']) for s in scenes),'checkpoints')
