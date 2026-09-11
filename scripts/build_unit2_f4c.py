from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
briefs=json.loads((U2/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
jbriefs=json.loads((U2/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
B={s['locus_id']:s for s in briefs if s['journey_id']=='U2-J3'}
J3=next(j for j in jbriefs if j['journey_id']=='U2-J3')
canon={r['knowledge_id']:r for r in json.loads((U2/'source'/'canonical-unit2-f1.json').read_text(encoding='utf-8'))['canonical_catalog']}

GUIDE={
 'name':'Dr. Nia Park','role':'cell-systems investigator',
 'visual':'navy field jacket, clear safety glasses, and a compact tablet displaying a transparent map of the cell',
 'story_job':'Nia keeps the route physically clear, asks you to predict what will happen, and names scientific terms only after the defining structure or action is visible.'
}

route=[
 {'scene_index':0,'locus':'Cell Size Cube Gallery','short':'Cube Gallery','floor':'Observatory modeling hall','symbol':'◫'},
 {'scene_index':1,'locus':'Exchange-Surface Fold Deck','short':'Fold Deck','floor':'Observatory rescue platform','symbol':'≋'},
 {'scene_index':2,'locus':'Organism Scaling Terrace','short':'Scaling Terrace','floor':'Outdoor thermal terrace','symbol':'△'},
]

ZONE_COPY={
 'U2-L19':[
  ('left','Small cell models','◫','A small transparent cube and sphere glow green as nutrients cross their surfaces and reach the center quickly.'),
  ('center','SA:V calculation table','▦','A live glass table displays surface-area and volume formulas, then converts them into a surface-area-to-volume ratio as each model changes size.'),
  ('right','Large cell models','▣','Geometrically similar enlarged models have more total surface area, yet their deep interiors dim red as exchange fails to keep pace with volume.'),
 ],
 'U2-L20':[
  ('left','Flat membrane panel','▭','A smooth boundary of fixed material spans the left side and provides only a limited number of simultaneous exchange sites.'),
  ('center','Folded membrane panel','≋','The same amount of boundary material is pulled into ridges and projections, exposing much more surface while enclosing nearly the same volume.'),
  ('right','Exchange-flow display','⇄','Nutrient and waste markers cross at many more locations once the surface is folded, turning the failing exchange meter back toward green.'),
 ],
 'U2-L21':[
  ('left','Small organism thermal model','◉','A compact animal model is surrounded by dense heat-loss arrows and a high mass-specific energy-use reading.'),
  ('center','Body-size comparison scale','▥','A central scale enlarges the same general body form while tracking surface-area-to-volume ratio, proportional heat exchange, and mass-specific metabolic rate.'),
  ('right','Large organism thermal model','⬤','A much larger animal model shows fewer heat-loss arrows relative to its mass and a lower mass-specific energy-use reading.'),
 ],
}

NARR={
'U2-L19':{
 'title':'The Giant Cell That Could Not Feed Its Center',
 'kicker':'The enormous model has more membrane than the tiny one, yet its interior is the first place to run out of oxygen and nutrients.',
 'paragraphs':[
  'The doors of the **Scaling Observatory** slide apart and reveal a long white modeling hall. On your **left**, a transparent cube no bigger than your fist glows green from edge to edge. Tiny blue nutrient markers touch its surface, cross the boundary, and reach the center almost immediately. Beside it, a glass sphere of similar small scale does the same. In the **center**, a black calculation table waits beneath a suspended exchange meter. On your **right** stands the problem that brought Nia here. A cube built to exactly the same shape has been enlarged until it fills most of the room. Its outer surface is enormous. Its center is dark red. The meter above it reads INTERIOR EXCHANGE FAILURE.',
  'Nia walks to the giant cube and presses her palm against its wall. “Look carefully before you decide what is wrong.” She sends the same kind of nutrient markers toward both cubes. The large cube receives particles across a much larger total surface, yet the distance and amount of interior that must be served have increased even more dramatically. The red center keeps spreading. Nia taps the table and gives the relationship a name only after the failure is visible. **Surface-area-to-volume ratio**, often written **SA:V**, compares the amount of exchange surface with the volume that surface must serve. Plasma-membrane surface area has to be sufficient for the living volume behind it. That ratio influences nutrient acquisition, waste elimination, chemical and energy exchange, and thermal exchange.',
  'The table lights with a one-unit cube. Its side length is 1. Surface area appears as **6s²**, so the cube has 6 square units of surface. Volume appears as **s³**, so it has 1 cubic unit of volume. The ratio is 6:1. Nia doubles the side length to 2. The cube now has more total surface area, 24 square units, but its volume has jumped to 8 cubic units. The ratio falls to 3:1. She enlarges it again to side length 3. Surface area becomes 54 while volume becomes 27. The ratio falls again to 2:1. The giant cube never lost surface area. Its problem is that **volume grows faster than surface area as linear size increases**, so less exchange surface is available relative to the amount of interior that depends on it.',
  'To prove that the rule is not a special trick of cubes, Nia rolls the small sphere onto the center table. Its surface area is **4πr²** and its volume is **4/3πr³**. When the radius doubles, both quantities increase, yet volume again grows faster. The sphere’s SA:V drops as radius increases. Now the green small models and the red large models tell the same story in two shapes. Smaller cells typically have a higher surface-area-to-volume ratio and can exchange materials with their surroundings more efficiently than geometrically similar larger cells. This relationship can constrain cell size and shape because internal demand rises with volume while the exchange boundary does not keep pace.',
  'Nia looks back at the giant cube. “We are not allowed to shrink this model,” she says. “The observatory needs the same internal volume for the next experiment. So if size is fixed, what else could we change?” A section of the giant model’s membrane unlocks and swings toward the next platform. It is perfectly flat. Beside it, mechanical arms wait to bend that same surface into deep folds. The exchange meter remains red, as though daring you to make more usable surface without adding a second giant cell.'
 ],
 'close':'The giant model stays the same overall size while one flat section of its boundary moves onto the rescue platform, where shape itself becomes the next variable.',
 'images':{
  'SA:V exchange':'small green models exchanging efficiently beside a giant red-centered model whose larger volume overwhelms its relative exchange surface',
  'Membrane area requirement':'one plasma-membrane boundary trying to supply the entire volume behind it while the interior demand meter rises',
  'Cell size limitation':'the same-shaped small and large cells showing the small model with a higher SA:V and faster access to its center',
  'Scaling with volume':'a size slider making volume rise faster than surface area and driving the SA:V display downward',
  'Surface area formula for cube':'a transparent cube labeled surface area 6s², volume s³, and a ratio that falls as side length increases',
  'Surface area and volume of sphere':'a glass sphere labeled 4πr² for surface area and 4/3πr³ for volume while SA:V falls as radius increases'
 }
},
'U2-L20':{
 'title':'Rescuing Exchange Without Shrinking the Cell',
 'kicker':'The volume must stay. The membrane chemistry must stay. The only tool left is shape.',
 'paragraphs':[
  'A narrow bridge carries you from the Cube Gallery to the **Exchange-Surface Fold Deck**. The failing giant cell remains visible through the glass behind you, its center still glowing red. On your **left**, the removed membrane section has been stretched into one smooth flat panel. In the **center**, an identical panel is clamped into a folding frame. On your **right**, streams of blue nutrient markers and yellow waste markers wait behind a digital counter. Nia locks the enclosed model volume at its current value and disables every permeability control. “We are changing geometry,” she says. “Nothing about the membrane’s chemical selectivity is being upgraded.”',
  'She releases the first particle stream. The flat panel admits particles across its available surface, but the exchange counter rises too slowly to meet the demand of the volume behind it. The giant model remains red. Then the central frame pulls the second panel outward into ridges. More ridges appear, followed by narrow projections, all made from the same kind of membrane. The boundary now occupies more actual surface while the volume it serves changes very little. The number of exposed crossing sites multiplies in front of you.',
  'Nia releases the particle stream again. Nutrient markers cross at many points at once. Waste markers leave through equally numerous regions. The counter on the right climbs rapidly and the giant model’s interior begins returning from red to amber, then green. The scientific principle is now visible. **Membrane folds and other complex surface structures increase exchange surface area relative to volume.** These are **exchange-surface adaptations**. Their benefit comes from geometry. A folded boundary can provide more membrane area to serve a given volume.',
  'Nia projects several biological silhouettes above the folding frame. Some cells use surface projections. Some internal membranes form extensive folds. The exact structures differ, yet the geometric advantage is shared. She leaves one warning beside the model. Folding alone does not magically change what the membrane is chemically permeable to. If a substance cannot cross a particular membrane by the relevant mechanism, adding folds does not rewrite that mechanism. The folds provide **more surface on which the existing transport machinery can operate**.',
  'The exchange meter finally turns fully green. The giant model has not been made smaller, and its chemistry has not been replaced. Its boundary simply offers more usable area. As the alarm clears, the observatory roof retracts above you. Cold outside air pours across a terrace where two animal models are waiting under thermal cameras. Nia points toward them. “SA:V does not stop mattering when we leave the scale of one cell,” she says. “Now watch what size does to heat exchange across a whole body.”'
 ],
 'close':'With the giant cell stabilized by added surface folds, the observatory opens onto the thermal terrace, where the same geometry will be tested at organism scale.',
 'images':{
  'Exchange-surface adaptations':'the same approximate volume served first by a flat membrane and then by a deeply folded membrane with many more simultaneous crossing sites'
 }
},
'U2-L21':{
 'title':'The Cold Wind Test',
 'kicker':'Two bodies face the same cold wind, but their size changes how much surface is exposed relative to the amount of tissue inside.',
 'paragraphs':[
  'You step onto the **Organism Scaling Terrace** and the temperature drops sharply. On your **left**, a compact animal model about the size of a small mammal stands beneath a thermal camera. Bright heat arrows stream away from nearly every part of its surface. In the **center**, a body-size scale and two gauges track proportional heat exchange and energy use per unit mass. On your **right**, a much larger animal model faces the same moving air. Its body holds far more volume and mass, yet the heat arrows are sparse when viewed relative to that mass. The terrace has taken the same geometry you saw in the cell models and made it impossible to ignore.',
  'Nia activates the size slider. As the modeled organism grows, total surface area still increases. Total volume also increases. The ratio between them falls. A smaller body therefore exposes relatively more surface to the environment for each unit of internal volume than a larger, similarly shaped body. The thermal camera converts that geometry into a biological consequence. **As organism size increases, surface-area-to-volume ratio and proportional heat exchange with the environment generally decrease.** The smaller model exchanges heat more rapidly relative to its body size because more surface is available per unit of internal volume.',
  'A second gauge begins to pulse. It reports metabolic rate per unit body mass. The smaller model’s gauge runs higher. The larger model’s gauge settles lower. Nia marks the result as a broad biological scaling trend, not a universal law that predicts every species or every physiological state. **Metabolic rate per unit body mass is generally higher in smaller multicellular organisms than in larger ones.** Many factors influence metabolism, but body-size scaling helps explain why small organisms often need proportionally rapid energy turnover while losing heat relatively quickly.',
  'The terrace wind slows. Behind the glass wall, the giant cell model remains green because its folded surface restored exchange capacity. The continuity meter now shows three linked images. A small cell has high SA:V. A large same-shaped cell has lower SA:V. A folded surface can recover more exchange area without requiring a proportional increase in volume. Outside, the small organism sheds heat relatively rapidly while the large organism exchanges heat more slowly relative to its mass. The same geometric relationship has traveled from a microscopic cell boundary to a whole-body thermal problem.',
  'Nia closes the scaling display and points below the terrace. A flexible molecular border stretches across the next terminal. Several particles are slipping through when they should not, while others that need passage are being blocked. “Size told us how much exchange surface a system has,” she says. “Now we need to understand what that surface is made of and why some substances cross more easily than others.” The doors to the **Membrane Border Terminal** unlock beneath your feet.'
 ],
 'close':'The scaling problem is solved, and the next failure shifts from how much surface exists to how the membrane itself controls what can cross it.',
 'images':{
  'Body size and heat exchange':'a small organism covered in dense heat-loss arrows beside a much larger organism with fewer arrows relative to its mass',
  'Body size and metabolic rate':'a mass-specific energy-use gauge running generally higher for the small multicellular organism and lower for the larger one'
 }
}
}

CAST={
'U2-L19':[
 ('small cell models','scientific part','small transparent cube and sphere glowing green','show high surface-area-to-volume ratio and rapid access between surface and center'),
 ('large cell models','scientific part','enlarged matching cube and sphere with red dim centers','show lower surface-area-to-volume ratio and exchange limitation'),
 ('SA:V calculation table','scientific instrument','glass table showing formulas, values, and a live ratio','make the scaling relationship quantitative and compare shapes')],
'U2-L20':[
 ('flat exchange surface','scientific part','smooth membrane panel with few simultaneous particle crossings','provide the baseline surface area'),
 ('folded exchange surface','scientific part','the same membrane bent into ridges and projections','increase surface area without a proportional volume increase'),
 ('exchange particles','scientific part','blue nutrient markers and yellow waste markers crossing the boundary','make exchange capacity visibly measurable')],
'U2-L21':[
 ('small organism model','scientific model','compact animal model surrounded by dense thermal arrows','show high proportional heat exchange'),
 ('large organism model','scientific model','much larger animal model with fewer thermal arrows relative to mass','show lower proportional heat exchange'),
 ('scaling gauges','scientific instrument','paired SA:V, heat-exchange, and mass-specific metabolic-rate meters','connect body size with thermal exchange and broad metabolic scaling')]
}

scene_meta={
'U2-L19':('Cell Size Cube Gallery','The giant cell cannot feed its center','Observatory modeling hall','Cell Size Cube Gallery — the side-by-side cube-and-sphere modeling table where a tiny green cell model is compared with a giant red-centered model.'),
'U2-L20':('Exchange-Surface Fold Deck','Changing shape restores exchange','Observatory rescue platform','Exchange-Surface Fold Deck — the membrane-rescue platform beside the giant cell, where a flat boundary is folded while volume stays nearly constant.'),
'U2-L21':('Organism Scaling Terrace','The same geometry reaches organism scale','Outdoor thermal terrace','Organism Scaling Terrace — the cold outdoor deck where small and large organism models are compared under thermal cameras and metabolic gauges.')
}

scenes=[]
for idx,lid in enumerate(['U2-L19','U2-L20','U2-L21']):
    b=B[lid]; n=NARR[lid]; locus,title_floor,_,locdesc=scene_meta[lid]
    zones=[{'position':pos,'label':lab,'symbol':sym,'description':desc} for pos,lab,sym,desc in ZONE_COPY[lid]]
    cast=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    cast += [{'name':name,'kind':kind,'visual':visual,'job':job} for name,kind,visual,job in CAST[lid]]
    beats=[]; snaps=[]
    for t in b['term_introductions']:
        kid=t['knowledge_id']; term=t['canonical_term']; science=t['canonical_science']
        image=n['images'].get(term, b['science_bearing_action']['during'][0])
        beats.append({'object_id':kid,'term':term,'story':image,'science':science,'exact_name':t['exact_name_recall'],'hint':image})
        snaps.append({'term':term,'meaning':science,'image':image})
    qr=b['quick_recall']; checkpoint=bool(qr.get('enabled'))
    answer='It decreases.' if lid=='U2-L19' else ''
    scene={
      'scene_index':idx,'locus':locus,'title':n['title'],'scene_kicker':n['kicker'],'location_description':locdesc,
      'scene_layout':{'orientation':b['orientation_sentence'].replace('At the observatory table','At the Cell Size Cube Gallery').replace('On the fold deck','At the Exchange-Surface Fold Deck').replace('On the terrace','At the Organism Scaling Terrace'),'zones':zones},
      'cast':cast,'story_open':n['paragraphs'][0],'story_paragraphs':n['paragraphs'],'story_close':n['close'],
      'object_ids':b['knowledge_ids'],'story_beats':beats,'memory_snapshot':snaps,
      'checkpoint':checkpoint,'checkpoint_object_id':b['primary_knowledge_id'],'checkpoint_prompt':qr.get('candidate_prompt','') if checkpoint else '',
      'checkpoint_answer':answer,'checkpoint_hint':'Picture the small and giant versions of the same shape. The giant one has more total surface, yet its volume increased even faster.' if checkpoint else '',
      'next_locus':B[b['causal_transition']['to_locus_id']]['scene_title'] if b['causal_transition']['to_locus_id'] in B else None,
      'misconception_guards':b['misconception_guards'],'required_visual':b['visual_spec'],'carry_forward':b['carry_forward']
    }
    scenes.append(scene)

journey={
 'schema':'memory-palace-v2-unit2-f4c-story-1.0','unit_id':'unit-2','palace_id':'U2-J3','journey_id':'U2-J3','palace_name':'Scaling Observatory',
 'story_title':'The Giant Cell That Starved at the Center','tagline':'Rescue an oversized cell by discovering why volume outruns exchange surface, then carry the same scaling rule onto a cold organism terrace.',
 'guide':GUIDE,'premise':J3['premise'],'mission':J3['mission'],
 'finale':'The giant cell regains exchange capacity only after its surface is folded, and the thermal terrace shows the same size relationship at organism scale. The final alarm then shifts attention from how much surface exists to how a membrane controls passage.',
 'estimated_minutes':8,'scene_count':3,'checkpoint_count':sum(bool(s['checkpoint']) for s in scenes),
 'learner_rule':'Read or listen and build each scale model in your mind. Watch the exchange failure happen before naming the rule. Quick Recall is optional during the first pass.',
 'route_orientation':'The Scaling Observatory is one continuous route. Begin in the indoor Cube Gallery with small models on the left and giant matching models on the right, move one platform forward to the Fold Deck where shape is changed without shrinking the model, then step outside onto the thermal terrace to compare whole organisms at different sizes.',
 'route':route,'scenes':scenes,'student_release':'PILOT_PREVIEW_F4C','narrative_standard':'V2-NARRATIVE-3.0-F4C'
}

(U2/'journeys').mkdir(parents=True,exist_ok=True)
(U2/'journeys'/'U2-J3.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

j1=json.loads((U2/'journeys'/'U2-J1.json').read_text(encoding='utf-8'))
j2=json.loads((U2/'journeys'/'U2-J2.json').read_text(encoding='utf-8'))
def card(j): return {k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
registry={
 'schema':'memory-palace-v2-unit2-f4c-registry-1.0','course_id':'ap-biology','unit_id':'unit-2','unit_title':'Cells','narrative_standard':'V2-NARRATIVE-3.0-F4C',
 'journey_count':3,'scene_count':sum(j['scene_count'] for j in [j1,j2,journey]),'checkpoint_count':sum(j['checkpoint_count'] for j in [j1,j2,journey]),
 'guided_journeys':[card(j1),card(j2),card(journey)]
}
(U2/'journeys-f4c.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U2/'status-f4b.json').read_text(encoding='utf-8'))
status.update({
 'status':'F4C_JOURNEY3_POLISHED_PREVIEW','pipeline_stage':'POLISHED_NARRATIVE_JOURNEY3_F4C','student_release':False,'preview_release':True,
 'polished_journeys':3,'polished_scenes':21,'polished_checkpoint_count':7,'narrative_story_files':3,
 'next_required_output':'F4D polished narrative for Journey 4 after F4C prose QA and developer/classroom review',
 'next_gate':'F4D polish Journey 4 only after F4C prose QA and developer/classroom review'
})
(U2/'status-f4c.json').write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; c=json.loads(cp.read_text(encoding='utf-8'))
for u in c['units']:
    if u['unit_id']=='unit-2':
        u.update({'status':'F4C_JOURNEY3_POLISHED_PREVIEW','journey_count':3,'scene_count':21,'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEYS1_3_POLISHED_F4C','polished_journeys':3,'polished_scenes':21})
cp.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
files=['journeys/U2-J3.json','journeys-f4c.json','status-f4c.json']
lock={'schema':'memory-palace-v2-unit2-f4c-content-lock-1.0','unit_id':'unit-2','stage':'F4C','student_release':False,'files':{f:sha(U2/f) for f in files}}
(U2/'content-lock-f4c.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit2-f4c-release-manifest-1.0','unit_id':'unit-2','stage':'F4C','student_release':False,'preview_release':True,'polished_journeys':3,'polished_scenes':21,'journey_3_records':sum(len(s['object_ids']) for s in scenes),'journey_3_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'next_stage':'F4D_JOURNEY4'}
(U2/'f4c-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Built Unit 2 F4C:',len(scenes),'Journey 3 scenes',sum(len(s['object_ids']) for s in scenes),'knowledge records',sum(bool(s['checkpoint']) for s in scenes),'checkpoints')
