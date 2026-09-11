from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U3=ROOT/'content'/'ap-biology'/'unit-3'
briefs=json.loads((U3/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
jbriefs=json.loads((U3/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
B={s['locus_id']:s for s in briefs if s['journey_id']=='U3-J4'}
J4=next(j for j in jbriefs if j['journey_id']=='U3-J4')

GUIDE={
 'name':'Dr. Nia Park',
 'role':'cellular-energetics investigator',
 'visual':'navy field jacket, clear safety glasses, and a compact tablet showing a chloroplast cutaway, electron path, and thylakoid proton-gradient gauge',
 'story_job':'Nia keeps the conservatory route spatially stable, separates light capture from electron transfer, keeps every chloroplast compartment visible, and names scientific terms only after their structure or action is clear.'
}

route=[
 {'scene_index':0,'locus':'Carbon Strategy Entrance','short':'Carbon Strategy','floor':'Glasshouse entrance','symbol':'C'},
 {'scene_index':1,'locus':'Oxygenation Timeline','short':'Oxygenation','floor':'Evolution corridor','symbol':'O₂'},
 {'scene_index':2,'locus':'Leaf Gas-Exchange Balcony','short':'Leaf Balcony','floor':'Leaf pavilion','symbol':'↕'},
 {'scene_index':3,'locus':'Chloroplast Compartment Gallery','short':'Chloroplast','floor':'Organelle gallery','symbol':'◎'},
 {'scene_index':4,'locus':'Photosynthesis Redox Board','short':'Redox Board','floor':'Reaction hall','symbol':'e⁻'},
 {'scene_index':5,'locus':'Photon and Wavelength Prism','short':'Photon Prism','floor':'Spectrum corridor','symbol':'λ'},
 {'scene_index':6,'locus':'Pigment Spectrum Bench','short':'Pigments','floor':'Pigment laboratory','symbol':'◐'},
 {'scene_index':7,'locus':'Photosystem Antenna Theater','short':'Photosystem','floor':'Antenna theater','symbol':'✳'},
 {'scene_index':8,'locus':'Photosystem II Water Splitter','short':'PSII','floor':'Thylakoid line A','symbol':'II'},
 {'scene_index':9,'locus':'Thylakoid Electron-Transport Bridge','short':'ETC Bridge','floor':'Thylakoid bridge','symbol':'→'},
 {'scene_index':10,'locus':'Photosystem I NADPH Station','short':'PSI','floor':'Thylakoid line B','symbol':'I'},
 {'scene_index':11,'locus':'Photophosphorylation Turbine','short':'ATP Turbine','floor':'Stroma exit','symbol':'ATP'},
]

ZONE_COPY={
'U3-L22':[
 ('left','Photoautotroph light-input lane','☀','A fixed left lane supplies light while an inorganic-carbon inlet remains visible, making energy source and carbon source independently traceable.'),
 ('center','Autotroph carbon-building center','CO₂→C','The center station accepts inorganic carbon and uses an external energy input to build organic carbon, keeping carbon acquisition separate from the identity of the energy source.'),
 ('right','Heterotroph organic-carbon lane','food C','A fixed right lane receives preexisting organic molecules made by other organisms and routes that organic carbon directly into the consumer side of the comparison.')],
'U3-L23':[
 ('left','Ancestral photosynthetic prokaryotes','prok','A deep-time display on the left shows photosynthesis operating in prokaryotic cells before eukaryotic photosynthetic lineages existed.'),
 ('center','Atmospheric oxygen rise','O₂↑','A central atmosphere column gradually accumulates molecular oxygen as oxygenic photosynthesis continues across immense spans of time.'),
 ('right','Eukaryotic photosynthetic lineage','euk','A later right-side lineage display shows eukaryotic photosynthesis built on an older prokaryotic photosynthetic foundation without erasing differences in cellular organization.')],
'U3-L24':[
 ('left','Stomatal pore and guard-cell opening','◌','A magnified epidermal pore bordered by two guard cells opens and closes on the left while the rest of the leaf remains fixed.'),
 ('center','Leaf and mesophyll photosynthetic tissue','leaf','A transparent leaf cross-section at center exposes mesophyll cells containing chloroplasts as a major site of photosynthesis in most plants.'),
 ('right','CO₂, O₂, and water-vapor diffusion paths','⇄','Three labeled diffusion paths on the right show carbon dioxide moving inward while oxygen and water vapor can move outward under typical photosynthetic conditions.')],
'U3-L25':[
 ('left','Chloroplast envelope and stroma','stroma','A conventional chloroplast cutaway on the left preserves its two-membrane envelope and the fluid stroma surrounding the thylakoid system.'),
 ('center','Thylakoid membrane and granum stack','grana','A central stack of disk-shaped thylakoids keeps the thylakoid membrane, internal thylakoid space, and granum architecture continuously visible.'),
 ('right','Reaction-location labels','map','Fixed right-side markers attach light-reaction machinery to thylakoid membranes and carbon-fixation reactions to the stroma so the two locations cannot be swapped.')],
'U3-L26':[
 ('left','Water oxidation and oxygen release','H₂O→O₂','A left reaction chamber removes electrons from water and releases molecular oxygen while keeping the water-derived products visually separate.'),
 ('center','Light-reaction and Calvin-cycle linkage','ATP/NADPH','The center board routes ATP and NADPH from the light reactions toward carbon fixation without depicting them as carbon atoms or as oxygen sources.'),
 ('right','Carbon-dioxide reduction to carbohydrate model','CO₂→CH','A right-side carbon model begins with carbon dioxide and ends in reduced organic carbon, emphasizing the reduction side of photosynthetic redox chemistry.')],
'U3-L27':[
 ('left','Short-wavelength, higher-energy photons','short λ','A fixed left beam contains shorter-wavelength photons and an energy meter that reads higher per photon.'),
 ('center','Visible-spectrum prism','spectrum','White light enters the central prism and spreads into visible wavelengths whose spacing and energy can be compared without treating color itself as stored energy.'),
 ('right','Long-wavelength, lower-energy photons','long λ','A fixed right beam contains longer-wavelength photons and an energy meter that reads lower per photon than the short-wavelength beam.')],
'U3-L28':[
 ('left','Chlorophyll a and b absorption panels','Chl a/b','Two fixed absorption panels compare chlorophyll a and chlorophyll b under the same incident spectrum.'),
 ('center','Pigment excitation bench','excite','A central thylakoid-membrane bench shows absorbed light exciting pigment electrons while reflected or transmitted wavelengths leave the pigment model.'),
 ('right','Carotenoid absorption and protection panel','carot','A right-side carotenoid panel broadens the usable light range and visibly dissipates excess excitation that could otherwise damage the photosynthetic apparatus.')],
'U3-L29':[
 ('left','Light-harvesting pigments','antenna','A fixed left antenna array contains multiple pigment molecules bound to proteins around the photosystem core.'),
 ('center','Reaction-center chlorophyll and primary acceptor','RC','The central reaction center contains a special chlorophyll pair beside a primary electron acceptor where excitation finally produces actual electron transfer.'),
 ('right','Excitation-energy transfer path','energy→','A right-side tracing display follows excitation energy toward the reaction center while explicitly refusing to draw one identical electron hopping from pigment to pigment.')],
'U3-L30':[
 ('left','Water-splitting input','H₂O','A water-oxidation complex on the left supplies replacement electrons while separating the resulting protons and molecular oxygen into distinct outputs.'),
 ('center','Photosystem II reaction center','PSII','The center photosystem II model absorbs light and transfers an excited reaction-center electron to an acceptor, leaving an electron vacancy that must be replaced.'),
 ('right','Electron, oxygen, and proton outputs','e⁻/O₂/H⁺','Three fixed right-side paths keep the outgoing electron, released oxygen, and lumen-directed protons physically separated so their roles cannot be merged.')],
'U3-L31':[
 ('left','Photosystem II electron departure','PSII e⁻','The highlighted electron leaves photosystem II from a fixed left-side donor point and enters the membrane electron-transfer route.'),
 ('center','Electron-transport and proton-gradient bridge','ETC','The central thylakoid-membrane bridge couples a series of redox transfers to increasing proton concentration in the thylakoid lumen.'),
 ('right','Photosystem I arrival','PSI e⁻','The electron reaches a fixed photosystem I receiving point on the right after some of its transferred energy has been used to help establish the proton gradient.')],
'U3-L32':[
 ('left','Incoming electron from the thylakoid ETC','e⁻ in','The electron arriving from the inter-photosystem chain enters from the left at a lower energy state than immediately after photosystem II excitation.'),
 ('center','Photosystem I and P700 reaction center','PSI/P700','A central photosystem I model uses another light input to re-excite the reaction-center system before electron transfer continues.'),
 ('right','NADP+ to NADPH output','NADPH','The stroma-side right station accepts reducing power and converts NADP+ to NADPH, keeping this reducing carrier distinct from ATP.')],
'U3-L33':[
 ('left','High-H+ thylakoid lumen','H⁺ high','A fixed left reservoir inside the thylakoid holds the higher proton concentration established during the light reactions.'),
 ('center','ATP synthase turbine','ATP synthase','A membrane-spanning ATP synthase at center provides the controlled route for protons to move down their electrochemical gradient.'),
 ('right','Stroma ATP and NADPH departure gate','ATP + NADPH','ATP is formed on the stroma side and joins NADPH at the fixed right exit leading toward the adjoining carbon-fixation greenhouse.')],
}

CAST={
'U3-L22':[
 ('sunlight beam','energy input','a narrow white beam entering the conservatory roof and illuminating only the left strategy lane','supply light energy to the photoautotroph comparison without being confused with a carbon source'),
 ('inorganic carbon inlet','carbon source','a labeled CO₂ inlet feeding the central carbon-building station','supply inorganic carbon that autotrophs can incorporate into organic molecules'),
 ('organic-carbon crate','comparison input','a crate of preexisting organic molecules arriving on the right lane','show how heterotrophs obtain organic carbon from molecules made by other organisms')],
'U3-L23':[
 ('cyanobacterial panel','evolutionary reference','a conventional prokaryotic cell panel connected to an oxygenic-photosynthesis indicator','represent cyanobacteria as prokaryotes capable of oxygenic photosynthesis'),
 ('atmosphere column','time-dependent output','a transparent atmospheric column whose oxygen gauge rises only as oxygenic photosynthesis persists','make atmospheric oxygenation a long-term consequence rather than a single-cell event'),
 ('lineage timeline','evolutionary continuity model','a horizontal timeline extending from ancient prokaryotic photosynthesis toward later eukaryotic photosynthetic lineages','preserve the evolutionary foundation without claiming identical organization across lineages')],
'U3-L24':[
 ('leaf cross-section','organ model','a conventional leaf cutaway showing epidermis, internal photosynthetic tissue, and air spaces','keep the path from atmosphere to mesophyll cells visible'),
 ('guard-cell pair','adjustable structure','two curved guard cells bordering one epidermal pore','change the stomatal opening and thereby alter the diffusion path'),
 ('gas tracers','molecular movement markers','separate CO₂, O₂, and H₂O-vapor labels following diffusion arrows','show the typical directions of gas exchange without merging the molecules')],
'U3-L25':[
 ('transparent chloroplast','organelle model','a conventional green chloroplast cutaway with a two-membrane envelope, stroma, and thylakoid stacks','hold every compartment in one stable visual frame'),
 ('granum stack','membrane structure','several disk-shaped thylakoids stacked in the center of the cutaway','provide abundant thylakoid membrane carrying light-reaction machinery'),
 ('reaction-location markers','spatial labels','two fixed markers reading LIGHT REACTIONS and CARBON FIXATION','attach each process to the correct chloroplast region')],
'U3-L26':[
 ('water molecule set','redox input','conventional water molecules entering the left oxidation chamber','donate electrons during light-reaction water oxidation and yield oxygen as a product'),
 ('NADPH carrier','reducing-power carrier','a labeled NADPH model moving from the light-reaction side toward the carbon-reduction side','carry reducing power without being portrayed as carbon or oxygen itself'),
 ('carbon dioxide model','carbon input','a conventional CO₂ model entering the right reduction side','supply carbon that will ultimately be incorporated into reduced organic molecules')],
'U3-L27':[
 ('white-light beam','radiation source','a white beam entering the prism from above','provide photons spanning visible wavelengths'),
 ('photon marker','scientific tracer','a small pulse marker attached to one photon path only until that photon is absorbed','help compare wavelength and photon energy without turning light energy into a persistent material token'),
 ('wavelength ruler','measurement reference','a ruler measuring crest-to-crest spacing on stylized waves','make wavelength a spatially measurable property')],
'U3-L28':[
 ('chlorophyll a panel','pigment model','a thylakoid-embedded pigment panel labeled chlorophyll a with its absorption trace','show the primary reaction-center pigment while also participating in broader light absorption'),
 ('chlorophyll b panel','accessory pigment model','a neighboring chlorophyll b panel with a different absorption trace','broaden the range of wavelengths usable by plants and green algae'),
 ('carotenoid panel','accessory/protective pigment model','orange-yellow pigment models with an excess-energy dissipation indicator','broaden absorption and help protect the photosynthetic apparatus from excess excitation')],
'U3-L29':[
 ('antenna pigment array','light-harvesting structure','a ring of pigments bound to proteins around a central reaction center','absorb photons and transfer excitation energy toward the center'),
 ('reaction-center chlorophyll pair','reaction center','a special paired chlorophyll model at the center of the photosystem','become excited and donate an electron to the primary acceptor'),
 ('primary electron acceptor','electron destination','a conventional acceptor positioned directly beside the reaction-center pair','receive the actual transferred electron after reaction-center excitation')],
'U3-L30':[
 ('photosystem II complex','membrane complex','a conventional photosystem II complex embedded in a thylakoid membrane cross-section','absorb light and transfer an excited electron to an acceptor'),
 ('water-oxidation complex','electron replacement system','a water-splitting complex beside photosystem II on the lumen side','replace electrons lost from photosystem II while producing H+ and O₂'),
 ('rising lumen H+ gauge','continuity gauge','the first illuminated segment of a proton-concentration gauge inside the thylakoid lumen','begin tracking the proton gradient that will later drive ATP synthase')],
'U3-L31':[
 ('highlighted electron','electron tracer','the same highlighted electron path leaving photosystem II and entering the chain','keep electron transfer distinct from the earlier antenna excitation-energy transfer'),
 ('thylakoid membrane bridge','membrane route','a conventional membrane segment containing electron-transfer proteins between photosystem II and photosystem I','couple stepwise redox transfer to proton-gradient formation'),
 ('lumen proton gauge','continuity gauge','the same H+ gauge now rising along the lumen side of the bridge','show that the thylakoid lumen becomes more proton-rich than the stroma')],
'U3-L32':[
 ('photosystem I complex','membrane complex','a conventional photosystem I complex centered around its reaction-center chlorophyll pair','use a new light input to raise electron energy again'),
 ('P680/P700 label cards','reaction-center labels','two small reference cards assigning P680 to photosystem II and P700 to photosystem I','keep the labels attached to reaction-center chlorophyll pairs rather than inventing extra photosystems'),
 ('NADP+ reduction station','carrier-forming output','a stroma-side station where NADP+ receives reducing power and becomes NADPH','form the light-reaction reducing carrier used later in carbon fixation')],
'U3-L33':[
 ('proton gradient gauge','continuity gauge','the completed gauge showing more H+ in the thylakoid lumen than in the stroma','provide the electrochemical gradient that directly powers proton flow through ATP synthase'),
 ('ATP synthase','membrane enzyme complex','a conventional ATP synthase spanning the thylakoid membrane with its catalytic side facing the stroma','couple downhill proton movement to ATP formation from ADP and inorganic phosphate'),
 ('ATP and NADPH exit pair','light-reaction products','separate ATP and NADPH models waiting together at the stroma-side greenhouse door','carry energy and reducing power toward carbon fixation while remaining chemically distinct')],
}

NARR={
'U3-L22':{
 'title':'The Door With Three Different Ways to Get Carbon',
 'kicker':'The conservatory cannot even begin its light route until carbon source and energy source stop being treated as the same question.',
 'paragraphs':[
  "A glass door slides open from the Cellular Energy Exchange Hall into the **Carbon Strategy Entrance**. Sunlight pours through the conservatory roof, but the ATP and NADPH indicators above the far greenhouse remain dark. The entrance is divided into three permanent lanes. On your **left**, a bright lane receives a white beam of light and a separate CO₂ inlet. Directly **ahead**, a carbon-building station accepts inorganic carbon and waits for an energy source. On your **right**, a delivery belt carries crates of preexisting organic molecules. Nia stops beside the center station and draws two headings on her tablet: CARBON SOURCE and ENERGY SOURCE. ‘If those two questions get blended together,’ she says, ‘the rest of photosynthesis becomes a vocabulary list instead of a mechanism.’",
  "She opens the center CO₂ inlet. Carbon dioxide enters, but no organic product appears until the station is also supplied with energy. An organism that builds organic molecules from inorganic carbon such as CO₂ is an **autotroph**. The term tells you where the carbon comes from. It does not, by itself, tell you whether the energy comes from sunlight or from chemical reactions. Nia then activates the **left** lane. Light reaches the carbon-building center while inorganic carbon continues to enter. This combination defines a **photoautotroph**: an organism that uses light energy to build organic molecules from inorganic carbon. The beam is the energy input; CO₂ is the carbon input. They remain on separate pipes so you cannot accidentally turn light into matter or CO₂ into an energy source.",
  "Now the **right** belt starts. Instead of feeding inorganic carbon into a building station, it delivers organic molecules that already contain reduced carbon. Nia labels this strategy **heterotroph**. A heterotroph obtains organic carbon from preexisting organic molecules made by other organisms. The comparison now has a stable geometry: photoautotrophic light input on the left, autotrophic carbon construction in the center, heterotrophic organic-carbon acquisition on the right. A plant is a familiar photoautotroph, but the categories are broader than plants and animals. The crucial distinction is what carbon source and energy source an organism uses.",
  "A large glass panel above the entrance finally lights. It summarizes **photosynthesis overall process** as the use of carbon dioxide, water, and light energy to produce carbohydrates and oxygen. Beside it, a storage shelf fills with sugar models. Nia names **solar energy capture**: photosynthetic organisms capture solar energy and produce sugars that can be used in biological processes or stored. She does not let the panel become a one-step cartoon. ‘This is a net process,’ she says. ‘We still have to discover where the oxygen comes from, where the light is captured, and how ATP and NADPH are actually made.’ The unanswered oxygen indicator begins pulsing and pulls a thin line of light down a corridor marked DEEP TIME."
 ],
 'close':"You follow the pulsing oxygen line into the next gallery, where the conservatory’s history is laid out as a timeline rather than a reaction pathway."
},
'U3-L23':{
 'title':'The Timeline That Fills an Atmosphere',
 'kicker':'Before chloroplasts appear, the light route begins in prokaryotic life and changes the planet around it.',
 'paragraphs':[
  "The corridor opens into the **Oxygenation Timeline**. Its floor is a dark band stretching from an ancient left wall toward a brighter right wall. On your **left**, conventional prokaryotic cell models glow beneath a label reading PHOTOSYNTHESIS PRESENT. Directly **ahead**, a transparent atmosphere column begins with a very low oxygen reading. On your **right**, a later branch contains eukaryotic photosynthetic cells. The white light pulse from the entrance does not travel literally through billions of years. Instead, Nia pins a small luminous marker above the timeline to show which photosynthetic innovation the display is following. ‘This is a history marker now,’ she says. ‘We are tracking the origin and consequences of the process, not a single photon.’",
  "She activates the **left** panel first. Photosynthetic chemistry is already operating in prokaryotic cells. Nia names the **prokaryotic origin of photosynthesis**: photosynthesis first evolved in prokaryotic organisms. The display then highlights cyanobacterial cells. These are not tiny chloroplasts floating freely; they are prokaryotes in their own right. The panel labels **cyanobacteria and oxygenic photosynthesis**. Cyanobacteria perform oxygenic photosynthesis, meaning their light reactions ultimately release molecular oxygen. The same broad light-capture logic that will later appear in chloroplasts has deep prokaryotic roots.",
  "As the cyanobacterial panel remains active, the **center** atmosphere column changes slowly. Its oxygen gauge rises over the timeline rather than jumping after one reaction. Nia names **atmospheric oxygenation**. Scientific evidence supports the claim that cyanobacterial photosynthesis contributed substantially to oxygenation of Earth’s atmosphere. The display is careful with scale. One cell does not ‘make the atmosphere oxygen-rich.’ Repeated oxygenic photosynthesis across enormous populations and spans of time contributes to a planetary change. The accumulating O₂ in the center therefore represents an ecological and geochemical consequence of biological metabolism.",
  "Only after the center atmosphere has changed does the **right** lineage illuminate. Eukaryotic photosynthetic organisms appear later on the timeline, carrying photosynthetic machinery organized inside chloroplasts. Nia labels the relationship **foundation of eukaryotic photosynthesis**: prokaryotic photosynthetic pathways formed the evolutionary foundation of eukaryotic photosynthesis. The right display does not claim that every modern photosynthetic organism uses every pathway in an identical way. It preserves the older biochemical foundation while allowing cellular organization to change. A leaf silhouette now grows out of the right-hand lineage, and the conservatory’s light beam passes directly into it."
 ],
 'close':"The leaf silhouette becomes a real suspended leaf ahead of you, and a tiny pore on its lower surface expands until it is large enough to walk toward."
},
'U3-L24':{
 'title':'The Balcony Where the Leaf Breathes With the Air',
 'kicker':'Light capture inside the leaf depends on a route for carbon dioxide to reach photosynthetic tissue while other gases can leave.',
 'paragraphs':[
  "You step onto the **Leaf Gas-Exchange Balcony**, built around a suspended leaf cross-section the size of a room. On your **left**, two curved guard-cell models surround a single adjustable epidermal pore. Directly **ahead**, layers of mesophyll tissue contain dozens of visible chloroplasts. On your **right**, three separate tracer paths are labeled CO₂, O₂, and H₂O VAPOR. Nia keeps the white light beam fixed above the leaf so the atmospheric input and the internal photosynthetic tissue can be seen at the same time. The conservatory’s problem is now more local: light reaches the leaf, but carbon dioxide still has to cross from air into the tissue where photosynthesis occurs.",
  "Nia opens the left pore. A CO₂ tracer moves inward through the opening and into the internal air spaces of the leaf. The center mesophyll cells light as the tracer approaches their chloroplasts. Nia names **leaf photosynthesis**. Leaves are major photosynthetic organs in most plants, and much of that photosynthesis occurs in mesophyll cells. She taps one chloroplast inside a mesophyll cell. The leaf itself is not one giant reaction chamber. Its tissue organization brings light, gases, water, and photosynthetic organelles into a geometry that supports the chemistry.",
  "The adjustable opening on the **left** is a **stoma**; the plural is **stomata**. Stomata are epidermal pores whose opening can be adjusted by surrounding guard cells. Under typical photosynthetic conditions, carbon dioxide can diffuse inward through these pores, while oxygen and water vapor can diffuse outward. On the **right**, the CO₂ path points toward the mesophyll, while O₂ and water-vapor paths point toward the atmosphere. Nia narrows the pore, and all three diffusion routes become more restricted. She opens it again, and the gas-exchange paths widen. The structure therefore connects photosynthetic carbon demand with water loss as well as oxygen release.",
  "The center mesophyll wall now becomes transparent. One chloroplast enlarges until its double envelope fills the doorway ahead. Nia points back once to the right-side gas paths. ‘We have brought carbon dioxide to the photosynthetic tissue,’ she says. ‘Now we need to put every reaction in the correct part of the chloroplast.’ The white beam follows you toward the enlarged organelle, while the CO₂ tracer stops at the stroma entrance instead of being allowed to wander through every compartment."
 ],
 'close':"You pass through the enlarged chloroplast envelope and enter a cutaway gallery where stroma and thylakoids remain visible at the same time."
},
'U3-L25':{
 'title':'The Chloroplast With Two Different Workspaces',
 'kicker':'The light route fails if the thylakoid membrane and stroma are treated as interchangeable places.',
 'paragraphs':[
  "The **Chloroplast Compartment Gallery** is built inside a transparent organelle model. On your **left**, a two-membrane envelope surrounds a broad fluid region labeled STROMA. Directly **ahead**, flattened thylakoid sacs rise in stacks like green coins. On your **right**, two movable location tags read LIGHT REACTIONS and CARBON FIXATION. Nia locks the whole cutaway in place before anything moves. ‘This room is about geography,’ she says. ‘If you know the process but put it in the wrong compartment, you do not actually know the mechanism.’ The light beam from the leaf balcony strikes the thylakoid stack at center, while the CO₂ tracer waits in the stroma on the left.",
  "Nia outlines the entire organelle. A **chloroplast** is a photosynthetic organelle bounded by an envelope of two membranes and containing stroma and thylakoids. She then traces the **chloroplast compartments** separately. The **stroma** is the fluid inside the inner chloroplast membrane and outside the thylakoids. Carbon-fixation reactions of the Calvin cycle occur there, so Nia attaches the CARBON FIXATION marker to the **left** stroma. This is **stroma and carbon fixation**: the carbon-building reactions use the stroma as their compartment, not the interior of the thylakoid.",
  "At the **center**, Nia magnifies the membrane of one thylakoid. Chlorophyll molecules are embedded there as parts of photosystems, alongside proteins that transfer electrons. She labels this **thylakoid membrane machinery**. Thylakoid membranes contain chlorophyll organized into photosystems together with electron-transport proteins. The flattened sacs are not empty green disks; their membrane surface is the platform that organizes the light-reaction machinery. The internal space enclosed by the membrane will later become important because protons can accumulate there.",
  "The camera pulls back enough to show multiple thylakoids stacked together. These stacks are **grana**; one stack is a granum. Nia fixes the LIGHT REACTIONS marker onto the thylakoid membranes and names **grana and light reactions**: thylakoids form stacks called grana, and the light reactions occur on thylakoid membranes in these stacks. The two right-side markers now have permanent homes. Light-reaction machinery belongs on thylakoid membranes; Calvin-cycle carbon fixation belongs in the stroma. A redox board unlocks at the far end of the gallery because location alone still does not explain what is oxidized and what is reduced."
 ],
 'close':"The chloroplast cutaway remains behind you as a reference map while water enters the left side of the next redox board and carbon dioxide enters the right."
},
'U3-L26':{
 'title':'The Board That Separates Water From Carbon Dioxide',
 'kicker':'The overall photosynthesis equation hides two different redox stories, so the board pulls them apart before reconnecting them.',
 'paragraphs':[
  "The **Photosynthesis Redox Board** spans the next wall. On your **left**, water molecules enter an oxidation chamber beneath a small O₂ outlet. Directly **ahead**, a central bridge connects LIGHT REACTIONS to CALVIN CYCLE with separate ATP and NADPH carriers. On your **right**, carbon dioxide enters a carbon-reduction model that ends in organic carbohydrate material. Nia places the familiar net equation across the top: 6 CO₂ + 6 H₂O + light → C₆H₁₂O₆ + 6 O₂. Then she draws a large bracket around it. ‘Useful summary,’ she says. ‘Dangerous if you imagine it as one literal step.’",
  "She labels the display **photosynthesis equation as model**. The common overall equation is a simplified net model of photosynthesis. It accounts for major inputs and outputs, but the direct carbon-fixation product is not glucose itself, and the pathway contains many linked reactions. Nia therefore keeps the equation above the room as bookkeeping while the actual chemistry runs below it. Water goes to the **left** chamber. CO₂ goes to the **right** chamber. ATP and NADPH move through the **center** connection between the light reactions and carbon-fixation chemistry.",
  "The left chamber now oxidizes water. Electrons are removed from water, and molecular oxygen appears at the O₂ outlet. Nia names **photosynthetic oxygen comes from water**. The O₂ released by oxygenic photosynthesis is derived from oxidation of water during the light reactions. She physically blocks an incorrect arrow that had connected CO₂ directly to the oxygen outlet. Carbon dioxide is the carbon source for carbohydrate production; it is not the source of the O₂ gas released by the light reactions. This distinction will matter again when we reach photosystem II.",
  "Nia zooms out to the whole board and labels **photosynthesis as redox**. Water is oxidized, while carbon dioxide is ultimately reduced to carbohydrate using reducing power carried by NADPH. She then names the two linked phases on the center bridge: **light reactions and Calvin cycle**. The light reactions capture light energy and produce ATP and NADPH. The Calvin cycle uses ATP and NADPH to reduce carbon dioxide toward carbohydrate production. The board still cannot explain how a photon becomes an excited electron, so the light inlet above the board opens into a prism corridor."
 ],
 'close':"A narrow beam of white light leaves the redox board and enters a glass prism, while the electron and proton parts of the mechanism remain deliberately unresolved."
},
'U3-L27':{
 'title':'The Prism Where Shorter Waves Carry More Per Photon',
 'kicker':'Before a pigment can capture light, the conservatory has to distinguish photon energy from wavelength and color.',
 'paragraphs':[
  "You enter the **Photon and Wavelength Prism**. On your **left**, tightly spaced wave crests run beneath a SHORT λ label and a higher-energy meter. Directly **ahead**, white light enters a large glass prism and separates into visible colors. On your **right**, widely spaced crests run beneath a LONG λ label and a lower-energy meter. Nia clips a tiny luminous marker to one incoming light path. ‘This marker follows a photon only until it is absorbed,’ she says. ‘After absorption, we will change what we track. We will not pretend a little glowing bead of “light energy” keeps traveling through the chloroplast.’",
  "Nia names a **photon** as a discrete quantum of electromagnetic radiation. The energy carried by a photon is inversely related to wavelength. She directs one short-wavelength photon down the **left** path and one longer-wavelength photon down the **right** path. The left energy meter reads higher per photon. The right reads lower. A shorter wavelength therefore corresponds to a higher-energy photon than a longer wavelength. This does not mean a visible color is itself a stored fuel molecule. It describes the energy associated with individual photons of different wavelengths.",
  "She stretches a ruler between corresponding crests on the wave model. That crest-to-crest distance is **wavelength**. The left ruler is shorter; the right ruler is longer. The prism makes the abstract measurement visible as different regions of the spectrum, but Nia keeps the wavelength ruler in place so you remember that wavelength is a physical property of the radiation. As wavelength decreases, photon energy increases. As wavelength increases, photon energy decreases. The exact biological effect still depends on whether a pigment can absorb that wavelength.",
  "Pigment screens descend across the spectrum. Some wavelengths disappear into a pigment model, while others continue through or bounce toward your eyes. Nia labels **pigment absorption and reflection**. Photosynthetic pigments absorb some wavelengths of visible light and reflect or transmit others; reflected wavelengths contribute to perceived color. Absorbed photons can drive electronic excitation in the pigment. Reflected light does not enter that pigment’s photochemistry. The photon marker vanishes the instant its photon is absorbed by the next bench, and a new EXCITATION indicator flashes in its place."
 ],
 'close':"With the original photon now absorbed, you follow the excitation indicator into the Pigment Spectrum Bench rather than carrying a fictional light particle forward."
},
'U3-L28':{
 'title':'The Bench Where Pigments Divide the Work',
 'kicker':'The same spectrum reaches several pigments, but they do not absorb, excite, or protect the photosynthetic system in exactly the same way.',
 'paragraphs':[
  "The **Pigment Spectrum Bench** is arranged like a three-station laboratory. On your **left**, chlorophyll a and chlorophyll b absorption panels face the same incoming spectrum. Directly **ahead**, a thylakoid-membrane bench contains pigment molecules under a controlled light source. On your **right**, orange and yellow carotenoid models sit beside an excess-excitation warning lamp. The luminous photon marker from the prism is gone because its photon was absorbed. In its place, Nia activates a thin glow around one pigment molecule to represent an excited electronic state. ‘From this point on,’ she says, ‘we have to distinguish the light that was absorbed from what happens inside the pigment after absorption.’",
  "When the central pigment absorbs an appropriate photon, one of its electrons is raised to a higher energy level. Nia labels this **light excitation of chlorophyll**. Chlorophyll absorbs light energy, raising electrons to higher energy levels in photosystems I and II. She then names **chlorophyll** itself: a photosynthetic pigment embedded in thylakoid membranes that absorbs light used to excite electrons in photosystems. The important visual is not simply that chlorophyll is green. Its biological role here is that absorption changes the energy state of electrons associated with the pigment.",
  "On the **left**, the two chlorophyll panels do not have identical absorption patterns. Nia highlights **chlorophyll a** as the primary reaction-center pigment in oxygenic photosynthesis. Beside it, **chlorophyll b** is labeled as an accessory chlorophyll that broadens the wavelengths usable for photosynthesis in plants and green algae. The word accessory does not mean unnecessary. By absorbing light in somewhat different regions and transferring excitation into the photosynthetic system, chlorophyll b expands the portion of the incident spectrum that can contribute to light capture.",
  "The **right** carotenoid panel now absorbs additional wavelengths and the warning lamp flashes when the central bench receives more excitation than the system can safely use. The carotenoid model dissipates part of that excess excitation. Nia names **carotenoids** as accessory pigments that broaden light absorption and can dissipate excess light energy, helping protect the photosynthetic apparatus. All three pigment types therefore contribute to light handling, but not in identical roles. A circular array of pigment-protein complexes rises from the bench, arranging these pigments around a central pair."
 ],
 'close':"The pigment panels fold inward into a complete photosystem, and the excitation indicator begins moving toward the center without any electron yet leaving one antenna pigment for another."
},
'U3-L29':{
 'title':'The Antenna Where Energy Moves Before an Electron Does',
 'kicker':'The conservatory’s most dangerous shortcut is exposed here: excitation can move through an antenna without one electron hopping from pigment to pigment.',
 'paragraphs':[
  "You enter the **Photosystem Antenna Theater**, a circular thylakoid-membrane stage. On your **left**, many pigments are bound to proteins in a broad antenna array. Directly **ahead**, a special chlorophyll pair sits beside a primary electron acceptor. On your **right**, a tracing wall can display either EXCITATION ENERGY or ELECTRON TRANSFER, but never both with the same symbol. Nia dims the room and sends one photon into a pigment near the edge of the left antenna. The pigment becomes excited. The photon itself is absorbed and is no longer shown traveling. A wave of excitation begins moving inward instead.",
  "Nia names the whole membrane complex a **photosystem**. A photosystem contains a reaction center surrounded by light-harvesting pigments and proteins. The broad left array is the **light-harvesting complex**. Its pigment molecules absorb photons and transfer excitation energy toward the reaction center. Each pigment remains fixed in its protein environment, so the theater looks like a receiving dish funneling excitation inward, not a chain of pigments handing electrons to one another. The tracing wall deliberately shows the excitation as a changing glow that appears on neighboring pigments in sequence. It does not draw a single labeled electron leaving one antenna pigment, entering the next, and continuing around the ring.",
  "That distinction becomes explicit when Nia labels **excitation-energy transfer**. In light-harvesting complexes, excitation energy is transferred among pigment molecules until reaction-center chlorophyll is excited; the same electron is not passed from antenna pigment to antenna pigment. The glowing excitation reaches the central chlorophyll pair. Only now does the electron-transfer display on the **right** activate. The antenna stage has delivered energy to the reaction center, not delivered one traveling antenna electron to it.",
  "The center is the **reaction center**. It contains a special chlorophyll pair and a primary electron acceptor. Once the reaction-center chlorophyll is excited, an electron can be transferred from that chlorophyll system to the primary acceptor. Nia changes the continuity marker at this exact moment. The soft excitation glow stops. A sharply outlined blue electron path begins at the reaction center and points to the acceptor. ‘Now we are following an actual electron transfer,’ she says. The acceptor gate opens onto the first large membrane complex in the linear electron-flow route: photosystem II."
 ],
 'close':"You follow the newly highlighted electron path into photosystem II, while the antenna theater remains behind as the place where excitation energy and electron transfer were permanently separated."
},
'U3-L30':{
 'title':'The Water Splitter That Replaces a Missing Electron',
 'kicker':'Photosystem II can send an excited electron onward only if the reaction center is supplied with a replacement, and water provides it.',
 'paragraphs':[
  "The **Photosystem II Water Splitter** is embedded in a full thylakoid-membrane cross-section. On your **left**, water molecules enter a water-oxidation complex facing the thylakoid lumen. Directly **ahead**, photosystem II spans the membrane with its reaction center connected to an electron acceptor. On your **right**, three output tracks are physically separated: a blue electron path leading into the electron transport chain, an O₂ outlet, and a proton path emptying into the lumen. The proton-gradient gauge introduced in the briefs is dark except for its first segment. Nia keeps all three outputs visible before she turns on the light.",
  "A photon is absorbed by the photosystem II antenna system and excitation reaches the reaction center. The reaction-center system transfers an excited electron to an acceptor, and the blue electron tracer moves onto the **right** electron track. Nia names **photosystem II**. Photosystem II absorbs light, transfers an excited electron to an acceptor, and receives replacement electrons from water oxidation. The electron leaving the reaction center creates a vacancy. Without replacement electrons, the photosystem could not continue sending electrons into linear electron flow.",
  "The **left** water-oxidation complex now acts. Water is oxidized, and electrons from that oxidation replace electrons lost from photosystem II. Nia labels the relationship **water supplies PSII electrons**. Water is split during the light reactions and supplies electrons that replace those lost from photosystem II. The display prevents a common mix-up by keeping the replacement electron moving toward the reaction center while the already-excited electron continues away through the acceptor route. They are part of one continuous electron-flow system, but they occupy different moments in the cycle.",
  "The other products of water oxidation separate visibly. Nia names **water-splitting products**. Oxidation of water associated with photosystem II supplies electrons, releases protons into the thylakoid lumen, and produces molecular oxygen. The O₂ leaves through its own outlet. The H⁺ markers accumulate inside the lumen and the proton-gradient gauge rises for the first time. The blue electron continues along the membrane toward the next complex. Nia points back to the redox board: this is the molecular event that explains why photosynthetic O₂ comes from water."
 ],
 'close':"The oxygen outlet vents away, the lumen keeps its new protons, and you follow the highlighted electron onto the thylakoid electron-transport bridge."
},
'U3-L31':{
 'title':'The Bridge That Builds a Gradient While Electrons Move',
 'kicker':'The electron does not become ATP; its transfer through membrane machinery helps establish the proton gradient that will later power ATP synthase.',
 'paragraphs':[
  "The **Thylakoid Electron-Transport Bridge** stretches across the conservatory like a membrane walkway. Photosystem II remains fixed on your **left**. Directly **ahead**, a chain of membrane electron-transfer components crosses the bridge. Photosystem I waits on your **right**. Beneath the walkway is the thylakoid lumen, where the H⁺ gauge has already risen because of water oxidation. Above it is the stroma, with a lower proton concentration. The blue electron tracer enters the first transfer step. Nia places a separate red arrow on the proton gauge so electron movement and proton accumulation are never represented by the same marker.",
  "The electron moves through a sequence of redox transfers from one component to another. The blue tracer advances carrier by carrier while the red proton gauge changes separately, making it impossible to mistake the electron itself for a proton or for ATP. As electron transfer proceeds, some of the available energy associated with that transfer is coupled to processes that increase proton concentration in the thylakoid lumen. Nia names the relationship **photosystem linkage**: photosystems II and I are embedded in the thylakoid membrane and linked by electron transfer through an electron transport chain. The chain is a route for stepwise electron transfer, not a pipe that directly pours ATP into the stroma.",
  "The red H⁺ gauge rises further. Nia labels the result the **thylakoid proton gradient**. Electron-transfer redox reactions establish an electrochemical proton gradient across the thylakoid membrane, with a higher proton concentration in the thylakoid lumen than in the stroma. The two sides of the membrane remain visible at once. H⁺ accumulation is spatially inside the thylakoid lumen. ATP has not yet been formed at this bridge; the gradient is stored potential for the chemiosmotic step still ahead.",
  "A side display briefly compares the same general membrane logic across forms of life. Nia names **ETC locations across life**. Electron transport chain reactions occur in chloroplasts, mitochondria, and across prokaryotic plasma membranes. The membranes and associated pathways are not identical in every organism, but membrane-bound electron transfer coupled to electrochemical gradients is a recurring biological strategy. On the main bridge, the highlighted electron reaches photosystem I on the **right**. Its energy state is now lower than it was immediately after photosystem II excitation, so another light input is required."
 ],
 'close':"The electron arrives at photosystem I and pauses beside a second light receiver, while the elevated lumen H+ gauge remains behind as a separate product of the bridge."
},
'U3-L32':{
 'title':'The Second Light Lift and the NADPH Exit',
 'kicker':'Photosystem I raises electron energy again and directs reducing power into NADPH on the stroma side.',
 'paragraphs':[
  "The **Photosystem I NADPH Station** keeps the thylakoid membrane horizontal across the room. On your **left**, the highlighted electron arrives from the inter-photosystem electron transport chain. Directly **ahead**, photosystem I surrounds its central reaction-center chlorophyll pair. On your **right**, a stroma-side station holds NADP⁺ beside an empty NADPH output slot. Two small reference cards are mounted above the membrane: P680 under photosystem II and P700 under photosystem I. Nia does not let those labels become new actors. ‘They name reaction-center chlorophyll pairs,’ she says, ‘not additional photosystems.’",
  "A new photon is absorbed by the photosystem I light-harvesting system, and excitation energy reaches its reaction center. Nia names **photosystem I**. Photosystem I re-excites electrons arriving from the thylakoid electron transport chain and supports reduction of NADP⁺ to NADPH. The blue electron path leaves the reaction-center system again at a higher energy state and continues toward the stroma-side reducing pathway. This second light input is why the electron can finish at a high-energy reducing carrier after losing transferable energy along the bridge from photosystem II.",
  "Nia points to the two reference cards and names **P680 and P700 reaction-center labels**. P680 and P700 are conventional labels for the reaction-center chlorophyll pairs of photosystem II and photosystem I, respectively, named for characteristic absorption peaks. She keeps the mapping physically fixed: PSII with P680, PSI with P700. The numbers do not tell the order in which the photosystems act in linear electron flow, and P680 or P700 should not be pictured as independent photosystems roaming the membrane. The two label cards remain bolted above their own complexes so the names cannot drift away from the reaction centers they describe.",
  "At the **right** station, NADP⁺ receives reducing power and NADPH appears in the output slot. Nia labels **NADPH formation**. In photosynthesis, electrons passing through the thylakoid electron transport system ultimately reduce NADP⁺ to NADPH in association with photosystem I. The NADPH model moves to a waiting shelf on the stroma side. It is not ATP. It carries reducing power that will be used in carbon reduction. The proton-gradient gauge is still high, however, and no ATP has yet left the light-reaction system. A doorway opens beside a membrane-spanning turbine."
 ],
 'close':"NADPH waits at the stroma-side exit while you follow the still-unresolved proton gradient to ATP synthase for the final light-reaction step."
},
'U3-L33':{
 'title':'The Turbine Driven by Protons, Not by Photons',
 'kicker':'The final conversion becomes clear only when the learner sees that H+ movement through ATP synthase directly drives ATP formation.',
 'paragraphs':[
  "The route ends at the **Photophosphorylation Turbine**. On your **left**, the thylakoid lumen is crowded with H⁺ markers and the proton-gradient gauge reads high. Directly **ahead**, ATP synthase spans the thylakoid membrane. On your **right**, the stroma contains ADP and inorganic phosphate, an empty ATP slot, and the NADPH model produced at the previous station. Nia turns off every decorative light except the gradient gauge. ‘A photon is not about to spin this enzyme,’ she says. ‘The immediate driver now is the electrochemical proton gradient built by the light reactions.’",
  "A gate through ATP synthase opens. Protons move from the higher-H⁺ thylakoid lumen through ATP synthase toward the lower-H⁺ stroma, down their electrochemical gradient. The enzyme couples that flow to formation of ATP from ADP and inorganic phosphate on the stroma side. Nia names this **photophosphorylation**. Protons flow through membrane-bound ATP synthase by chemiosmosis, driving ATP formation from ADP and inorganic phosphate; in photosynthesis this ATP-producing process is photophosphorylation. The proton-gradient gauge falls as the controlled flow proceeds.",
  "The new ATP molecule joins NADPH at the **right** exit. Nia labels them **light-reaction energy products**. The light reactions capture light energy to produce ATP and NADPH, which provide energy and reducing power for carbohydrate production in the Calvin cycle. ATP and NADPH remain separate models because they do different chemical jobs. ATP is an energy-coupling molecule. NADPH carries high-energy electrons and reducing power. Both are produced on the stroma side where the Calvin-cycle reactions can use them.",
  "Nia then activates a final input-output board. This is **light-reaction inputs and outputs**. The light reactions use light, water, ADP plus inorganic phosphate, and NADP⁺. They produce O₂, ATP, and NADPH. The path behind you is now reconstructable: pigments capture light; photosystem II sends an electron onward and water replaces it; water oxidation adds H⁺ to the lumen and releases O₂; the electron transport chain helps build the proton gradient while delivering electrons to photosystem I; photosystem I re-excites electrons and supports NADPH formation; H⁺ then flows through ATP synthase to make ATP. The conservatory’s ATP and NADPH indicators finally turn green, and the adjoining carbon-fixation greenhouse unlocks."
 ],
 'close':"ATP and NADPH leave together through the stroma-side greenhouse door, completing the Light Capture Conservatory and setting up the next journey through carbon fixation."
},
}

TERM_IMAGES={
'U3-K-022':'the overhead net-process panel connecting CO₂, water, and light to carbohydrate production and O₂ release',
'U3-K-023':'the left sunlight lane filling the sugar-storage shelf only after light capture is connected to carbon building',
'U3-K-105':'the center station building organic carbon from a CO₂ inlet using an external energy source',
'U3-K-106':'the left lane combining light energy with inorganic carbon at the autotroph center',
'U3-K-107':'the right belt delivering preexisting organic-carbon crates',
'U3-K-024':'the ancient left timeline showing photosynthesis operating in prokaryotic cells',
'U3-K-025':'the center atmosphere column slowly increasing its O₂ reading',
'U3-K-026':'the right eukaryotic photosynthetic lineage built on an older prokaryotic foundation',
'U3-K-108':'the cyanobacterial panel coupling a prokaryotic cell model to oxygenic photosynthesis',
'U3-K-109':'the center leaf cross-section with photosynthetic mesophyll cells',
'U3-K-110':'the adjustable epidermal pore bordered by guard cells and connected to gas-diffusion arrows',
'U3-K-027':'the chloroplast cutaway keeping stroma and thylakoids physically distinct',
'U3-K-028':'the stroma marker holding carbon-fixation reactions outside the thylakoids',
'U3-K-029':'the thylakoid membrane carrying chlorophyll, photosystems, and electron-transfer proteins',
'U3-K-030':'the granum stack whose thylakoid membranes carry the light reactions',
'U3-K-111':'the whole two-membrane chloroplast containing stroma and thylakoids',
'U3-K-113':'the net photosynthesis equation suspended above the detailed two-part reaction board',
'U3-K-114':'the left water-oxidation chamber feeding the O₂ outlet while the CO₂ chamber stays separate',
'U3-K-115':'water being oxidized on the left while carbon dioxide is ultimately reduced on the right',
'U3-K-116':'the central ATP/NADPH bridge linking thylakoid light reactions to stroma carbon fixation',
'U3-K-117':'one discrete light pulse compared across short- and long-wavelength paths',
'U3-K-118':'the crest-to-crest ruler showing shorter versus longer wavelength',
'U3-K-119':'the pigment screen absorbing selected wavelengths while others are reflected or transmitted',
'U3-K-034':'the central chlorophyll electron indicator rising to an excited state after photon absorption',
'U3-K-112':'the thylakoid-embedded chlorophyll model absorbing light used for electron excitation',
'U3-K-120':'the chlorophyll a panel connected to the reaction-center role',
'U3-K-121':'the chlorophyll b panel broadening usable wavelengths',
'U3-K-122':'the carotenoid panel broadening absorption and dissipating excess excitation',
'U3-K-123':'the complete antenna-plus-reaction-center complex embedded in thylakoid membrane',
'U3-K-124':'the central special chlorophyll pair beside a primary electron acceptor',
'U3-K-125':'the surrounding pigment-protein antenna transferring excitation toward the center',
'U3-K-131':'the excitation glow moving pigment-to-pigment without one identical electron hopping through the antenna',
'U3-K-035':'the left water-oxidation complex supplying replacement electrons to photosystem II',
'U3-K-126':'the photosystem II reaction center transferring an excited electron to an acceptor',
'U3-K-130':'the three separated water-oxidation outputs: replacement electrons, lumen H⁺, and O₂',
'U3-K-032':'the comparison panel showing membrane electron transport in chloroplasts, mitochondria, and prokaryotic plasma membranes',
'U3-K-036':'the highlighted electron path linking photosystem II to photosystem I through the thylakoid chain',
'U3-K-037':'the lumen H⁺ gauge rising above the stroma H⁺ level across the thylakoid membrane',
'U3-K-033':'the stroma-side NADP⁺ station becoming NADPH after photosystem I electron transfer',
'U3-K-127':'the photosystem I reaction center re-exciting the incoming electron with a second light input',
'U3-K-128':'the fixed P680 label under PSII and P700 label under PSI',
'U3-K-031':'ATP and NADPH waiting together at the stroma-side greenhouse exit',
'U3-K-038':'H⁺ flowing from the thylakoid lumen through ATP synthase and driving ATP formation in the stroma',
'U3-K-132':'the final board listing light, water, ADP + Pi, and NADP⁺ as inputs and O₂, ATP, and NADPH as outputs',
}

CHECKPOINT_HINTS={
'U3-L25':'Picture the transparent chloroplast: thylakoid membranes and grana are at the center, while the surrounding stroma is on the left.',
'U3-L29':'Picture the antenna theater. A glow of excitation moves among pigments, but the blue electron path begins only at the reaction center and primary acceptor.',
'U3-L30':'Picture the water splitter on the left of photosystem II. It refills the missing electron while O₂ leaves and H⁺ enters the lumen.',
'U3-L33':'Picture the crowded H⁺ lumen on the left and ATP synthase in the membrane. The protons themselves move through the enzyme toward the stroma.'
}

scenes=[]
for idx,lid in enumerate(J4['route']):
    b=B[lid]; n=NARR[lid]
    zones=[{'position':pos,'label':lab,'symbol':sym,'description':desc} for pos,lab,sym,desc in ZONE_COPY[lid]]
    cast=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    cast += [{'name':name,'kind':kind,'visual':visual,'job':job} for name,kind,visual,job in CAST[lid]]
    beats=[]; snaps=[]
    for t in b['term_introductions']:
        image=TERM_IMAGES.get(t['knowledge_id'],b['carry_forward'])
        beats.append({'object_id':t['knowledge_id'],'term':t['canonical_term'],'story':image,'science':t['canonical_science'],'exact_name':bool(t.get('exact_name_recall')),'hint':image})
        snaps.append({'term':t['canonical_term'],'meaning':t['canonical_science'],'image':image})
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
 'schema':'memory-palace-v2-unit3-f4d-story-1.0','unit_id':'unit-3','palace_id':'U3-J4','journey_id':'U3-J4',
 'palace_name':'Light Capture Conservatory','story_title':'The Light That Could Not Reach the Greenhouse',
 'tagline':'Follow light from organism-level carbon strategy into a leaf and chloroplast, then separate photon capture, excitation transfer, electron flow, proton-gradient formation, NADPH production, and photophosphorylation until ATP and NADPH can reach carbon fixation.',
 'guide':GUIDE,'premise':J4['premise'],'mission':J4['mission'],
 'finale':'The conservatory succeeds only after carbon and energy sources are separated, photosynthesis is located in the correct chloroplast compartments, oxygen is traced to water oxidation, pigments transfer excitation correctly, photosystem II and photosystem I are linked by electron transfer, the thylakoid proton gradient is established, and ATP plus NADPH leave the light reactions together for carbon fixation.',
 'estimated_minutes':34,'scene_count':len(scenes),'checkpoint_count':sum(bool(s['checkpoint']) for s in scenes),
 'learner_rule':'Read or listen while holding the fixed left, center, and right anchors of each scene in mind. Follow the physical output that causes the transition to the next locus. Quick Recall is optional during the first pass.',
 'route_orientation':'The Light Capture Conservatory is a twelve-station route. Enter through carbon strategy and deep-time oxygenation, cross a leaf into the chloroplast, separate the overall redox process, then follow light through wavelength and pigments. At the photosystem theater, the continuity marker changes from absorbed light to excitation energy and then to a highlighted electron path. Follow that electron from photosystem II through the thylakoid electron-transport bridge to photosystem I while the lumen proton-gradient gauge rises, then finish at ATP synthase on the stroma side.',
 'route':route,'scenes':scenes,'student_release':'PILOT_PREVIEW_F4D','narrative_standard':'V2-NARRATIVE-3.0-U3-F4D'
}

(U3/'journeys').mkdir(parents=True,exist_ok=True)
(U3/'journeys'/'U3-J4.json').write_text(json.dumps(journey,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

j1=json.loads((U3/'journeys'/'U3-J1.json').read_text(encoding='utf-8'))
j2=json.loads((U3/'journeys'/'U3-J2.json').read_text(encoding='utf-8'))
j3=json.loads((U3/'journeys'/'U3-J3.json').read_text(encoding='utf-8'))
def card(j): return {k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_standard']}
registry={'schema':'memory-palace-v2-unit3-f4d-registry-1.0','course_id':'ap-biology','unit_id':'unit-3','unit_title':'Cellular Energetics','narrative_standard':'V2-NARRATIVE-3.0-U3-F4D','journey_count':4,'scene_count':sum(x['scene_count'] for x in (j1,j2,j3,journey)),'checkpoint_count':sum(x['checkpoint_count'] for x in (j1,j2,j3,journey)),'guided_journeys':[card(j1),card(j2),card(j3),card(journey)]}
(U3/'journeys-f4d.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

status=json.loads((U3/'status-f4c.json').read_text(encoding='utf-8'))
status.update({'status':'F4D_JOURNEY4_POLISHED_PREVIEW','pipeline_status':'POLISHED_NARRATIVE_JOURNEYS_1_4_F4D','student_release':False,'preview_release':True,'journey_count':4,'scene_count':registry['scene_count'],'polished_journeys':4,'polished_scenes':registry['scene_count'],'polished_checkpoint_count':registry['checkpoint_count'],'narrative_story_files':4,'next_required_output':'F4E polished narrative for Journey 5 Carbon Fixation Greenhouse after F4D prose QA'})
(U3/'status-f4d.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(U3/'status.json').write_text(json.dumps(status,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

cp=ROOT/'content'/'ap-biology'/'course.json'; c=json.loads(cp.read_text(encoding='utf-8'))
for u in c['units']:
    if u['unit_id']=='unit-3':
        u.update({'status':'F4D_JOURNEY4_POLISHED_PREVIEW','journey_count':4,'scene_count':registry['scene_count'],'source_status':'AUDITED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_JOURNEYS1_4_POLISHED_F4D','polished_journeys':4,'polished_scenes':registry['scene_count'],'student_release':False})
cp.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# Prefer newest Unit 3 registry while preserving historical stage artifacts and hashes.
bc=ROOT/'backend'/'content.py'; bs=bc.read_text(encoding='utf-8')
old_block='    if unit_id == "unit-3":\n        path=UNIT3_DIR / "journeys-f4c.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4b.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4a.json"\n        return _read_json(path)["guided_journeys"] if path.exists() else []'
new_block='    if unit_id == "unit-3":\n        path=UNIT3_DIR / "journeys-f4d.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4c.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4b.json"\n        if not path.exists(): path=UNIT3_DIR / "journeys-f4a.json"\n        return _read_json(path)["guided_journeys"] if path.exists() else []'
if old_block in bs: bs=bs.replace(old_block,new_block)
elif 'journeys-f4d.json' not in bs: raise RuntimeError('Could not patch Unit 3 journey registry preference to F4D')
bc.write_text(bs,encoding='utf-8')

mainp=ROOT/'backend'/'main.py'; ms=mainp.read_text(encoding='utf-8')
ms=ms.replace('0.14.0-u3-f4c','0.15.0-u3-f4d').replace('v2-apbio-0.14.0-u3-f4c','v2-apbio-0.15.0-u3-f4d')
mainp.write_text(ms,encoding='utf-8')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
files=['journeys/U3-J4.json','journeys-f4d.json','status-f4d.json']
lock={'schema':'memory-palace-v2-unit3-f4d-content-lock-1.0','unit_id':'unit-3','stage':'F4D','student_release':False,'files':{f:sha(U3/f) for f in files}}
(U3/'content-lock-f4d.json').write_text(json.dumps(lock,indent=2)+'\n',encoding='utf-8')
manifest={'schema':'memory-palace-v2-unit3-f4d-release-manifest-1.0','unit_id':'unit-3','stage':'F4D','student_release':False,'preview_release':True,'polished_journeys':4,'polished_scenes':registry['scene_count'],'journey_4_records':sum(len(s['object_ids']) for s in scenes),'journey_4_checkpoints':sum(bool(s['checkpoint']) for s in scenes),'next_stage':'F4E_JOURNEY5'}
(U3/'f4d-release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Built Unit 3 F4D:',len(scenes),'scenes',sum(len(s['object_ids']) for s in scenes),'knowledge records',sum(bool(s['checkpoint']) for s in scenes),'checkpoints')
