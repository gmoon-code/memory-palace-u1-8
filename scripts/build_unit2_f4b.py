from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
briefs=json.loads((U2/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
jbriefs=json.loads((U2/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
B={s['locus_id']:s for s in briefs if s['journey_id']=='U2-J2'}
J2=next(j for j in jbriefs if j['journey_id']=='U2-J2')

GUIDE={
 'name':'Dr. Nia Park','role':'cell-systems investigator',
 'visual':'navy field jacket, clear safety glasses, and a compact tablet displaying a transparent map of the cell',
 'story_job':'Nia keeps the route physically clear, asks you to notice what each structure is doing, and gives the scientific name only after the defining action is visible.'
}

route=[
 {'scene_index':0,'locus':'Mitochondrial Membrane Airlock','short':'Mitochondrial Airlock','floor':'Orange chamber entrance','symbol':'◉'},
 {'scene_index':1,'locus':'Cristae Generator Deck','short':'Cristae Deck','floor':'Inside mitochondrion','symbol':'≋'},
 {'scene_index':2,'locus':'Energy-Demand Control Bay','short':'Demand Control','floor':'Annex central bridge','symbol':'▥'},
 {'scene_index':3,'locus':'Chloroplast Entry Chamber','short':'Chloroplast Entry','floor':'Greenhouse entrance','symbol':'◍'},
 {'scene_index':4,'locus':'Thylakoid and Stroma Gallery','short':'Thylakoid Gallery','floor':'Inside chloroplast','symbol':'▤'},
]

ZONE_COPY={
 'U2-L14':[
  ('left','Outer mitochondrial membrane','◯','A smooth orange outer membrane forms the organelle’s external boundary and stays visibly separate from the inner membrane.'),
  ('center','Intermembrane space','▯','A narrow illuminated gap lies between the outer and inner mitochondrial membranes, making the between-membranes compartment unmistakable.'),
  ('right','Inner membrane and matrix','◎','A second membrane encloses the deep matrix, where enzyme markers, mitochondrial DNA, and mitochondrial ribosomes are visible.'),
 ],
 'U2-L15':[
  ('left','Smooth outer boundary','◯','The mitochondrion’s smooth outer membrane remains visible as a stable reference while the inner architecture changes dramatically.'),
  ('center','Cristae-rich inner membrane','≋','One continuous inner membrane folds back and forth into deep cristae covered with respiratory membrane machinery.'),
  ('right','Matrix-facing side','◎','The matrix lies beside the folded inner membrane, keeping the membrane surface and the enclosed compartment spatially distinct.'),
 ],
 'U2-L16':[
  ('left','Lower-demand cell display','○','A relatively low-demand sample cell shows a modest mitochondrial population beside a low, steady energy-demand reading.'),
  ('center','Energy-demand meter','▥','Nia’s pulsing dashboard compares sustained cellular energy demand with mitochondrial abundance and changing physiological state.'),
  ('right','Higher-demand cell display','●','A high-demand sample cell contains many visible mitochondria, while the display also shows that number and shape can change.'),
 ],
 'U2-L17':[
  ('left','Chloroplast envelope','◉','Two green envelope membranes surround the chloroplast and clearly separate its interior from the surrounding cytosol.'),
  ('center','Transparent chloroplast interior','◇','The opened organelle reveals an internal membrane system waiting to be examined without yet collapsing all green structures into one label.'),
  ('right','Plant and algal context','▧','A plant cell and a photosynthetic algal cell both contain chloroplasts, grounding the organelle in the organisms where it occurs.'),
 ],
 'U2-L18':[
  ('left','Granum stacks','▤','Stacks of flattened green membrane sacs stand on the left so a whole granum can be distinguished from one individual thylakoid.'),
  ('center','Chlorophyll-bearing thylakoid membrane','═','A single thylakoid membrane crosses the center, with chlorophyll pigments embedded where incoming light is absorbed.'),
  ('right','Stroma','≈','Clear fluid surrounds the thylakoid stacks inside the chloroplast inner membrane, with the Calvin-cycle indicator operating in this space.'),
 ],
}

NARR={
'U2-L14':{
 'title':'Opening the Orange Chamber',
 'kicker':'The first energy chamber looks simple until its two membranes separate and reveal two different internal regions.',
 'paragraphs':[
  "The door from Cell Operations Complex closes behind you, and the new annex goes quiet. Through a wall of glass, two enormous organelles are suspended in separate chambers. The one on your **left** is orange and oval, with a surprisingly complicated interior hidden beneath its surface. Farther to the **right**, beyond a central control bridge, a green organelle catches light from the ceiling. Nia’s tablet flashes one problem across both chambers: ENERGY OUTPUT UNSTABLE. She clips a small pulsing meter to the rail. \"We are not going to fix this by calling one a powerhouse and the other a photosynthesis organelle,\" she says. \"We need to know exactly where their reactions can occur.\"",
  "You enter the orange chamber through the **Mitochondrial Membrane Airlock**. At first the mitochondrion in front of you looks like one thick orange oval. Nia activates a cutaway beam. The outer surface peels visually away without breaking, exposing a second membrane beneath it. A narrow glowing gap appears between the two boundaries. Only after you can see that two membranes are present does Nia name the architecture: a **mitochondrial double membrane**. Those two membranes create distinct compartments that support different parts of aerobic cellular respiration.",
  "Nia points into the narrow gap between the membranes. It is not empty decoration between two outlines; it is a real compartment. The illuminated region is the **intermembrane space**, located between the outer and inner mitochondrial membranes. Then your view passes through the second membrane. Beyond it lies the organelle’s deepest fluid-filled region. Enzyme markers for pyruvate oxidation and the citric acid cycle illuminate there, beside a small loop of mitochondrial DNA and mitochondrial ribosomes. This innermost compartment is the **mitochondrial matrix**.",
  "You now have three stable landmarks in one view: smooth outer membrane on the left edge, narrow intermembrane space through the center, and inner membrane enclosing the matrix to the right. Nia traces the inner membrane with a bright line. The energy meter still jitters. Then the line begins bending inward again and again, as if the membrane is unfolding a hidden floor plan. \"The compartments are correct,\" Nia says. \"Now look at what the inner membrane does with its surface.\" The airlock opens directly onto the folded generator deck."
 ],
 'close':'The double membrane remains behind you as the inner membrane folds inward, carrying you onto a much larger working surface without making the mitochondrion itself much larger.',
 'images':{
  'Mitochondrial double membrane':'a cutaway mitochondrion with clearly separated outer and inner membranes creating distinct internal regions',
  'Intermembrane space':'the narrow illuminated compartment specifically between the outer and inner mitochondrial membranes',
  'Mitochondrial matrix':'the compartment enclosed by the inner membrane, containing matrix enzymes, mitochondrial DNA, and ribosomes'
 }
},
'U2-L15':{
 'title':'The Membrane That Makes More Room',
 'kicker':'The inner membrane does not stay flat. Its folds create far more working surface inside the same organelle.',
 'paragraphs':[
  "The **Cristae Generator Deck** feels much larger than the mitochondrion looked from outside. That is the trick of the architecture. The smooth outer boundary remains visible behind glass on your **left**, but the inner membrane in the **center** dives inward, rises, bends again, and returns in repeated folds. On your **right**, the matrix remains beside those folds. Nia switches off every label and asks you to follow one orange line with your eyes. It never breaks. Every ridge and valley belongs to the same continuous inner mitochondrial membrane.",
  "A flat model appears beside it for comparison. On the flat membrane, only a few respiratory protein complexes fit across the surface. The real inner membrane begins folding more deeply. Each fold adds membrane area, and more respiratory machinery can occupy the expanded surface. Now the structural name arrives. The mitochondrial outer membrane is relatively smooth, while the **mitochondrial inner folds** greatly increase the membrane surface that can support efficient ATP synthesis.",
  "Nia stops beside one deep fold and runs her finger from its base to its tip. \"This fold has a specific name,\" she says. A label appears only on the folded inner membrane: **crista**; multiple folds are **cristae**. Cristae are folds of the inner mitochondrial membrane that increase membrane surface area. You can still see the intermembrane side on one side of the membrane and the matrix on the other. The fold does not create a new independent wall. It is the inner membrane itself bending through space.",
  "The energy meter steadies for a moment as the respiratory complexes light along the cristae. Then a second reading appears above the deck: DEMAND MISMATCH. Nia’s tablet projects two cells on the bridge outside. One barely moves. The other is contracting repeatedly and consuming energy at a much higher sustained rate. Strangely, both diagnostic models have been assigned the same mitochondrial population. \"The next error is not inside one mitochondrion,\" Nia says. \"It is how many mitochondria a cell tends to maintain when its demands differ.\""
 ],
 'close':'You leave the folded inner membrane intact and step onto the central control bridge, where two cells with very different energy demands are waiting for comparison.',
 'images':{
  'Mitochondrial inner folds':'a flat inner membrane becoming repeatedly folded, with much more respiratory machinery fitting on the enlarged membrane surface',
  'Cristae':'deep folds traced as one continuous inner mitochondrial membrane, with matrix and intermembrane sides still distinguishable'
 }
},
'U2-L16':{
 'title':'When the Cell Asks for More',
 'kicker':'Mitochondria are not issued to every cell in one fixed number. Their abundance reflects cellular context and demand.',
 'paragraphs':[
  "The **Energy-Demand Control Bay** sits exactly between the orange mitochondrial chamber and the green chloroplast greenhouse. On your **left**, Nia loads a lower-demand sample cell onto a transparent display. In the **center**, the pulsing energy-demand meter shows a modest, steady reading. On your **right**, a second cell is working continuously, and its demand bar climbs much higher. Yet the malfunctioning simulation gives both cells the same small number of mitochondria. The mismatch is obvious before Nia says anything.",
  "She unlocks the mitochondrial-population control. As sustained demand rises in the right-hand cell, more mitochondria become visible throughout its cytoplasm. The left-hand cell remains comparatively sparse. Nia gives the relationship its precise form: cells with high sustained energy demand **often contain many mitochondria**. The pattern links mitochondrial abundance with the amount of aerobic energy conversion a cell commonly needs, but the word *often* stays on the screen in bright letters.",
  "To show why that qualifier matters, Nia changes the physiological state of the same cell. The mitochondrial population shifts, and several mitochondria alter their shape and distribution. The display makes it difficult to imagine mitochondrial number as a permanent badge identifying one cell type. **Mitochondrial abundance and morphology vary with cell type and physiological state.** A high-demand cell may commonly have many mitochondria, but there is no universal fixed count that every high-energy cell must obey.",
  "The demand meter finally settles into a stable pulse. At that moment, green light spills across the bridge from the chamber on your right. Nia turns the meter toward it. \"This organelle also converts energy, but its internal map is different, and it occurs in a different biological context.\" The greenhouse door opens. Inside the glass, the green organelle is still blurred into one generic shape. Nia leaves the orange mitochondrion visible behind you so the two organelles will remain separate in your mental map."
 ],
 'close':'With mitochondrial abundance matched to cellular context, you cross the central bridge into the green chamber to map a second double-membrane energy organelle.',
 'images':{
  'Mitochondrial abundance and energy demand':'a low-demand cell with fewer visible mitochondria compared with a high sustained-demand cell containing many, plus a state-change panel showing variable number and shape'
 }
},
'U2-L17':{
 'title':'The Green Chamber Has an Address',
 'kicker':'Before looking inside a chloroplast, place it in the cells where it actually occurs and identify its outer architecture.',
 'paragraphs':[
  "The **Chloroplast Entry Chamber** is bright enough to make you squint. The organelle hangs in the **center** behind clear glass, deep green and internally complex. On your **left**, its boundary is magnified until two separate envelope membranes are visible. On your **right**, Nia’s context panel shows several eukaryotic cells. She does not begin with the word chloroplast. Instead, she asks you to place the green organelle where it belongs.",
  "The first image is an animal cell. The green organelle does not appear. The next is a plant cell from photosynthetic tissue, and several green organelles become visible. A photosynthetic algal cell appears beside it and contains them as well. Nia then names the distribution you have just seen: **chloroplasts are specialized organelles found in plants and photosynthetic algae**. She leaves one caution on the panel: this does not mean every eukaryote or every plant cell must contain chloroplasts.",
  "Now the magnified boundary on the left opens as a cutaway. You can trace an outer membrane and an inner membrane surrounding the organelle. Only after both are distinct does Nia identify the structural feature: chloroplasts have a **double membrane**. The interior remains separated from the surrounding cytosol by this envelope. A photosynthesis indicator activates inside the green chamber, linking the organelle with its central function: the chloroplast is the location of **photosynthesis** in those photosynthetic eukaryotic cells.",
  "The green interior is still deliberately unresolved. You can see dark stacks and pale fluid, but Nia refuses to label the whole interior as one thing. \"That would erase the most useful part of the map,\" she says. Her tablet zooms through the envelope. Individual flattened sacs sharpen into focus. Some are stacked; others are visible as single membrane sacs. Light begins streaming toward the membrane surfaces, while the surrounding fluid remains clearly separate."
 ],
 'close':'You pass through the chloroplast envelope and enter the final gallery, where stacked membranes, individual sacs, light-absorbing pigment, and surrounding fluid each take a distinct place.',
 'images':{
  'Chloroplast distribution':'plant and photosynthetic-algal cells containing chloroplasts, contrasted with an animal-cell example without them',
  'Chloroplast structure/function':'a chloroplast cutaway showing two envelope membranes around an interior where photosynthesis occurs'
 }
},
'U2-L18':{
 'title':'One Sac, One Stack, One Surrounding Space',
 'kicker':'The last chamber separates four green terms that are easy to blur together: thylakoid, granum, chlorophyll, and stroma.',
 'paragraphs':[
  "Inside the **Thylakoid and Stroma Gallery**, the chloroplast finally stops looking like a green blur. On your **left**, several stacks of flattened membrane sacs rise like short columns. In the **center**, Nia isolates one individual flattened sac and magnifies its membrane until pigment molecules are visible within it. The **right** side of the gallery is not another stack at all; it is the fluid region surrounding the membrane system inside the inner chloroplast membrane. Nia asks you to hold those three regions in place before any terms appear.",
  "The single flattened membrane sac in the center comes first. Photosynthetic electron-transfer components occupy its membrane. Nia names it a **thylakoid**: a membranous sac within a chloroplast whose membrane contains photosynthetic electron-transfer components. Then the left-hand column lights one sac at a time. Several thylakoids together form one stack. That entire stack is a **granum**. The singular terms now stay separate in the scene: one thylakoid is one sac; one granum is a stack of thylakoids.",
  "A beam of light strikes the center thylakoid. Green pigment molecules embedded in its membrane absorb the light, and the light-reaction indicator activates along that membrane. Those pigments are **chlorophyll**. Chlorophyll pigments in thylakoid membranes absorb light used in photosynthesis. Nia keeps the indicator on the membrane so the location is clear: light-dependent reactions occur in thylakoid membranes, including the membranes organized into grana. A granum is therefore not a separate kind of chemical factory; it is a stack that organizes many thylakoid membranes.",
  "Finally, Nia turns down the membrane glow. The clear fluid on your right becomes more obvious because it surrounds every thylakoid stack while remaining inside the chloroplast’s inner membrane. This fluid is the **stroma**. A separate Calvin-cycle indicator activates there. The contrast completes the map: light-dependent chemistry belongs on thylakoid membranes; the Calvin cycle occurs in the stroma. The energy-demand meter that has followed you through the annex gives one steady tone, and both transparent organelles return to normal operation.",
  "Before the gallery doors open, Nia places the two organelles side by side one last time. The mitochondrion is orange, with an outer membrane, intermembrane space, folded inner membrane forming cristae, and matrix. The chloroplast is green, with a double envelope, thylakoids that may stack into grana, chlorophyll in thylakoid membranes, and stroma around those sacs. \"Keep the architecture, not a slogan,\" she says. Beyond the exit, an enormous cube-shaped cell model is glowing red at its center. The next problem is scale."
 ],
 'close':'The Energy Conversion Annex is stable. You leave with two distinct internal maps, and the route continues to the Scaling Observatory where cell size itself begins to limit exchange.',
 'images':{
  'Thylakoid':'one individual flattened chloroplast membrane sac containing photosynthetic electron-transfer machinery',
  'Granum':'a stack composed of multiple thylakoids, with the individual sacs still visibly separable',
  'Stroma':'the fluid region surrounding thylakoids but inside the inner chloroplast membrane, with the Calvin-cycle indicator active',
  'Chlorophyll':'green pigment molecules embedded in thylakoid membrane absorbing incoming light'
 }
}
}

TERM_OVERRIDES={
 'Mitochondrial double membrane':'Mitochondrial double membrane',
 'Mitochondrial inner folds':'Mitochondrial inner folds',
 'Chloroplast distribution':'Chloroplast distribution',
 'Chloroplast structure/function':'Chloroplast structure/function'
}

def scene_layout_from_brief(b):
    return {'orientation':b['orientation_sentence'],'zones':[{'position':p,'label':l,'symbol':s,'description':d} for p,l,s,d in ZONE_COPY[b['locus_id']]]}

def cast_from_brief(b):
    out=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    for c in b['stable_cast']:
        out.append({'name':c['name'],'kind':'scientific part','visual':c['visual_identity'],'job':c['job_in_scene']})
    return out

def make_scene(lid,idx):
    b=B[lid]; n=NARR[lid]
    beats=[]; snaps=[]
    for t in b['term_introductions']:
        term=TERM_OVERRIDES.get(t['canonical_term'],t['canonical_term'])
        img=n['images'].get(t['canonical_term'],n['images'].get(term,b['carry_forward']))
        beats.append({'object_id':t['knowledge_id'],'term':term,'story':img,'science':t['canonical_science'],'exact_name':bool(t.get('exact_name_recall')),'hint':img})
        snaps.append({'term':term,'meaning':t['canonical_science'],'image':img})
    qr=b['quick_recall']; cp=bool(qr.get('enabled'))
    cp_id=b['primary_knowledge_id']; prompt=qr.get('candidate_prompt','') if cp else ''
    if lid=='U2-L15': cp_id='U2-K-086'
    if lid=='U2-L18': cp_id='U2-K-089'
    hint=''
    if lid=='U2-L15': hint='Picture one continuous inner mitochondrial membrane bending into many deep folds while the matrix remains on one side.'
    if lid=='U2-L18': hint='Picture the left side of the gallery: several individual flattened thylakoid sacs stacked together into one column.'
    return {
      'scene_index':idx,'locus':b['scene_title'],'title':n['title'],'scene_kicker':n['kicker'],
      'location_description':b['exact_location']+' — '+b['micro_anchor']+'.',
      'scene_layout':scene_layout_from_brief(b),'cast':cast_from_brief(b),
      'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':beats,'memory_snapshot':snaps,
      'checkpoint':cp,'checkpoint_object_id':cp_id,'checkpoint_prompt':prompt,'checkpoint_answer':qr.get('answer','') if cp else '',
      'checkpoint_hint':hint,
      'next_locus':B[b['causal_transition']['to_locus_id']]['scene_title'] if b['causal_transition']['to_locus_id'] else None,
      'misconception_guards':b['misconception_guards'],'required_visual':b['visual_spec'],'carry_forward':b['carry_forward']
    }

scenes=[make_scene(lid,i) for i,lid in enumerate(J2['route'])]
journey={
 'schema':'memory-palace-v2-unit2-f4b-story-1.0','unit_id':'unit-2','palace_id':'U2-J2','journey_id':'U2-J2',
 'palace_name':'Energy Conversion Annex','story_title':'The Power Map Blackout',
 'tagline':'Restore two failing energy-conversion chambers by mapping the exact membranes, compartments, and structures that make mitochondria and chloroplasts work.',
 'guide':GUIDE,'premise':J2['premise'],'mission':J2['mission'],
 'finale':'The energy-demand meter stabilizes only after mitochondrial compartments and cristae are mapped separately from chloroplast thylakoids, grana, chlorophyll, and stroma; the next alarm then points toward a cell model whose size is overwhelming its exchange surface.',
 'estimated_minutes':10,'scene_count':len(scenes),'checkpoint_count':sum(1 for s in scenes if s['checkpoint']),
 'learner_rule':'Read or listen and build the chamber in your mind. Scientific names appear only after their defining structures or jobs become visible. Quick Recall is optional during the first pass.',
 'route_orientation':'The Energy Conversion Annex has two transparent organelle chambers joined by one central bridge. Enter the orange mitochondrial chamber first, move from its double-membrane airlock to the cristae deck, compare cell energy demand on the bridge, then cross into the green chloroplast chamber and finish inside the thylakoid-and-stroma gallery.',
 'route':route,'scenes':scenes,'student_release':'PILOT_PREVIEW_F4B','narrative_standard':'V2-NARRATIVE-3.0-F4B'
}

(U2/'journeys').mkdir(parents=True,exist_ok=True)
(U2/'journeys'/'U2-J2.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# Registry contains both polished previews.
j1=json.loads((U2/'journeys'/'U2-J1.json').read_text(encoding='utf-8'))
def card(j): return {k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
registry={
 'schema':'memory-palace-v2-unit2-f4b-registry-1.0','course_id':'ap-biology','unit_id':'unit-2','unit_title':'Cells',
 'narrative_standard':'V2-NARRATIVE-3.0-F4B','journey_count':2,'scene_count':j1['scene_count']+journey['scene_count'],'checkpoint_count':j1['checkpoint_count']+journey['checkpoint_count'],
 'guided_journeys':[card(j1),card(journey)]
}
(U2/'journeys-f4b.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U2/'status-f4a.json').read_text(encoding='utf-8'))
status.update({
 'status':'F4B_JOURNEY2_POLISHED_PREVIEW','pipeline_stage':'POLISHED_NARRATIVE_JOURNEY2_F4B','student_release':False,'preview_release':True,
 'polished_journeys':2,'polished_scenes':18,'polished_checkpoint_count':6,'narrative_story_files':2,
 'next_required_output':'F4C polished narrative for Journey 3 after F4B prose QA and developer/classroom review',
 'next_gate':'F4C polish Journey 3 only after F4B prose QA and developer/classroom review'
})
(U2/'status-f4b.json').write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; c=json.loads(cp.read_text(encoding='utf-8'))
for u in c['units']:
    if u['unit_id']=='unit-2':
        u.update({'status':'F4B_JOURNEY2_POLISHED_PREVIEW','journey_count':2,'scene_count':18,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEYS1_2_POLISHED_F4B','polished_journeys':2,'polished_scenes':18})
cp.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
files=['journeys/U2-J2.json','journeys-f4b.json','status-f4b.json']
lock={'schema':'memory-palace-v2-unit2-f4b-content-lock-1.0','unit_id':'unit-2','stage':'F4B','student_release':False,'files':{f:sha(U2/f) for f in files}}
(U2/'content-lock-f4b.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit2-f4b-release-manifest-1.0','unit_id':'unit-2','stage':'F4B','student_release':False,'preview_release':True,'polished_journeys':2,'polished_scenes':18,'journey_2_records':sum(len(s['object_ids']) for s in scenes),'journey_2_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'next_stage':'F4C_JOURNEY3'}
(U2/'f4b-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Built Unit 2 F4B:',len(scenes),'Journey 2 scenes',sum(len(s['object_ids']) for s in scenes),'knowledge records',sum(bool(s['checkpoint']) for s in scenes),'checkpoints')
