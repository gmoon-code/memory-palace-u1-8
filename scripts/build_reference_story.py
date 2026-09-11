from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'content/ap-biology/unit-1/reference-journey-water.json'

journey={
  'palace_id':'Z3',
  'palace_name':'Water Atrium',
  'story_title':'The Flooded Sky Hotel',
  'tagline':'Follow one runaway stream of water from the hotel lobby to the roof, and learn why water behaves the way it does.',
  'guide':{
    'name':'Mara Vale',
    'role':'chief systems engineer of the Sky Hotel',
    'visual':'dark raincoat, brass tool belt, and a palm-sized glass scanner that can magnify molecules',
    'story_job':'Mara keeps the emergency moving. She opens doors, activates molecular views, and asks you to notice what the water itself is doing.'
  },
  'premise':'A midnight storm has knocked out the Sky Hotel’s water-control system. One ruptured line now feeds the lobby fountain, rooftop greenhouse, spa, aquarium, and life-support reservoir. The same water is moving through all of them, but at each level a different property of water determines what happens next.',
  'mission':'Stay with Mara and follow the runaway water line upward through eleven connected locations. At the roof, stabilize the reservoir before its pH swings far enough to shut down the hotel’s living systems.',
  'finale':'At the Buffer Gate, the pH alarm settles. Water begins flowing normally again to the greenhouse, aquarium, and hotel systems below. Looking down through the glass tower, you can retrace the entire emergency as one chain of water properties rather than eleven isolated facts.',
  'estimated_minutes':14,
  'scene_count':11,
  'checkpoint_count':3,
  'learner_rule':'Read or listen and picture the scene. The important terms are introduced inside the action. Stop only when a Quick Recall appears.',
  'route_orientation':'The hotel is a vertical glass tower. You begin on the ground-floor lobby and keep moving upward, following the same water line until you reach the roof.',
  'route':[ 
    {'scene_index':0,'locus':'Life Fountain','short':'Lobby','floor':'Ground floor','symbol':'⛲'},
    {'scene_index':1,'locus':'Polar Waterfall','short':'Waterfall','floor':'Mezzanine','symbol':'💧'},
    {'scene_index':2,'locus':'Cohesion Pool','short':'Pool','floor':'Level 2','symbol':'🌊'},
    {'scene_index':3,'locus':'Xylem Tower','short':'Tower','floor':'Levels 3–5','symbol':'🌿'},
    {'scene_index':4,'locus':'Thermal Bath','short':'Bath','floor':'Level 6','symbol':'♨'},
    {'scene_index':5,'locus':'Evaporation Balcony','short':'Balcony','floor':'Level 7','symbol':'☁'},
    {'scene_index':6,'locus':'Ice Lake','short':'Ice Lake','floor':'Level 8','symbol':'❄'},
    {'scene_index':7,'locus':'Solution Bar','short':'Bar','floor':'Level 9','symbol':'🥛'},
    {'scene_index':8,'locus':'Hydration Aquarium','short':'Aquarium','floor':'Level 9 rear','symbol':'◉'},
    {'scene_index':9,'locus':'pH Staircase','short':'pH Stairs','floor':'Levels 10–11','symbol':'↕'},
    {'scene_index':10,'locus':'Buffer Gate','short':'Roof','floor':'Roof','symbol':'◎'}
  ],
  'scenes':[]
}

scenes=[]

def beat(object_id,term,story,meaning,exact,hint):
    return {'object_id':object_id,'term':term,'story':story,'science':meaning,'exact_name':exact,'hint':hint}

def scene(index,locus,title,kicker,where,layout,cast,paragraphs,beats,close,checkpoint=False,checkpoint_object_id=None,checkpoint_prompt=None,next_locus=None,snapshot=None):
    return {
      'scene_index':index,'locus':locus,'title':title,'scene_kicker':kicker,
      'location_description':where,'scene_layout':layout,'cast':cast,
      'story_open':paragraphs[0],'story_paragraphs':paragraphs,'story_close':close,
      'object_ids':[b['object_id'] for b in beats],'story_beats':beats,
      'memory_snapshot':snapshot or [{'term':b['term'],'meaning':b['science'],'image':b['hint']} for b in beats],
      'checkpoint':checkpoint,'checkpoint_object_id':checkpoint_object_id or beats[0]['object_id'],
      'checkpoint_prompt':checkpoint_prompt or '', 'next_locus':next_locus
    }

scenes.append(scene(0,'Life Fountain','The Alarm Beneath the Fountain','The hotel wakes up all at once.',
'You are in the circular ground-floor lobby. A black marble fountain fills the center. Directly above it, a transparent service shaft rises through the middle of the hotel. The only open route is upward.',
{'orientation':'You enter from the south doors. The fountain is in the center. Mara stands at its control pedestal on the east side. The glass water shaft rises straight overhead.',
 'zones':[{'position':'left','label':'West wall','symbol':'🌿','description':'A living-wall display is wilting as its water feed stops.'},{'position':'center','label':'Life Fountain','symbol':'⛲','description':'The runaway water begins here and feeds every location above.'},{'position':'right','label':'Control pedestal','symbol':'🔧','description':'Mara’s map shows the greenhouse, spa, aquarium, and roof reservoir all sharing the same water system.'}]},
[{'name':'Mara Vale','kind':'guide','visual':'chief engineer in a dark raincoat','job':'leads you along the damaged water line and keeps the route clear'},
 {'name':'Water','kind':'central substance','visual':'the same clear stream running through the entire hotel','job':'supports the hotel’s living systems because its molecular properties produce many useful behaviors'}],
[
'Thunder shakes the glass ceiling. Every light in the lobby dies for half a second, then the fountain erupts high enough to strike the chandelier. Mara Vale, the hotel’s chief systems engineer, runs across the wet floor and slaps a brass panel open. “The main water controller is gone. If the roof reservoir shuts down, the greenhouse and aquarium go with it.”',
'She turns the panel toward you. A vertical map of the hotel glows red. One water line connects the lobby fountain to every living system above. Small warning icons blink beside temperature, ice, dissolving salts, and pH. They look like separate problems, but Mara points to the single blue line running through all of them. “Same water. Different behavior.”',
'At the fountain, the idea is simple enough to hold onto before anything else happens: **living systems depend on water**, and the useful behaviors of water come from the way water molecules are built and interact. You do not need to memorize the list yet. You are about to watch each property cause the next part of the emergency.',
'A pipe behind the fountain ruptures. The escaping stream shoots into a glass chute on the north wall. As you and Mara run toward it, her molecular scanner flickers on and enlarges a single water molecule inside the falling sheet.'
],
[
 beat('MO-APBIO-U1-W001','Properties of water overview','The hotel map previews the families of water behavior you will encounter as you move upward.','Water’s polarity and hydrogen bonding contribute to cohesion, adhesion, capillary action, temperature moderation, evaporative cooling, the unusual density of ice, solvent behavior, and pH-related chemistry.',False,'one blue water line feeding many different hotel systems'),
 beat('MO-APBIO-U1-W002','Living systems depend on water','When the shared water line fails, the living-wall, greenhouse, and aquarium all begin shutting down.','Living systems depend on the properties of water to sustain life.',False,'the same water line feeding every living display in the hotel')
],
'The stream hits the glass chute and becomes a silver waterfall. The scanner locks onto one molecule, and the next problem becomes visible at the scale of electrons.',next_locus='Polar Waterfall'))

scenes.append(scene(1,'Polar Waterfall','The Molecule with an Uneven Pull','Zoom in until the flood becomes one molecule.',
'You are on the mezzanine beside a floor-to-ceiling sheet of falling water. A molecular scanner projects one water molecule above the railing: one oxygen atom in the middle and two hydrogen atoms forming a bent V shape.',
{'orientation':'The waterfall covers the north wall. You and Mara stand on the central viewing bridge. The exit to the Cohesion Pool is down a ramp to the west.',
 'zones':[{'position':'left','label':'Electron display','symbol':'e⁻','description':'Shared electrons shift closer to oxygen.'},{'position':'center','label':'Water molecule model','symbol':'H–O–H','description':'One oxygen and two hydrogens form the molecule you are following.'},{'position':'right','label':'Neighboring molecule','symbol':'···','description':'A second water molecule turns so opposite partial charges face one another.'}]},
[{'name':'Oxygen atom','kind':'part of water','visual':'large red center of the molecular model','job':'pulls shared electrons more strongly than hydrogen does'},
 {'name':'Hydrogen atoms','kind':'parts of water','visual':'two small white ends of the V-shaped molecule','job':'share electrons with oxygen in O–H covalent bonds'},
 {'name':'Hydrogen bond','kind':'interaction','visual':'a dotted attraction between neighboring water molecules','job':'links opposite partial-charge regions of different molecules without replacing the covalent O–H bonds'}],
[
'Mara holds the scanner over the waterfall. The roaring sheet of water disappears from the display and one molecule fills the air between you. A red **oxygen** sphere sits in the middle. Two smaller **hydrogen** spheres angle away from it like the arms of a V. Thin glowing bands between O and H mark the covalent bonds where electrons are shared.',
'Then the glow shifts. The shared electrons spend more time near oxygen because oxygen attracts them more strongly. Mara does not move the atoms; she simply freezes the model at that instant. The oxygen side now carries a **partial negative charge, δ−**, while each hydrogen side carries a **partial positive charge, δ+**. The molecule has an uneven distribution of charge. That unevenness is **water polarity**.',
'A second water molecule drifts into the projection. Its δ+ hydrogen turns toward the δ− region of the first molecule. A dotted line snaps into place between them. “That dotted attraction is a **hydrogen bond**,” Mara says. “Keep it separate from the solid O–H covalent bonds inside each water molecule.”',
'Now the waterfall makes sense at a larger scale. Millions of polar water molecules can attract one another because opposite partial-charge regions keep meeting. The scanner zooms out, and the falling water begins gathering into thick ropes instead of scattering into isolated droplets.'
],
[
 beat('MO-APBIO-U1-W003','Water polarity','The electron cloud shifts toward oxygen, leaving an uneven charge distribution across each water molecule.','Water is polar because oxygen and hydrogen share electrons unequally in polar covalent O–H bonds.',True,'oxygen pulling the shared electron cloud closer, leaving δ− near O and δ+ near H'),
 beat('MO-APBIO-U1-W004','Partial charges','The oxygen end becomes δ− and the hydrogen ends become δ+; these are partial charges, not full ionic charges.','Unequal electron sharing gives oxygen a partial negative charge and the hydrogens partial positive charges.',False,'δ− on oxygen and δ+ on each hydrogen'),
 beat('MO-APBIO-U1-W005','Water polarity enables hydrogen bonding','Opposite partial-charge regions of neighboring water molecules attract, creating hydrogen bonds between molecules.','Water polarity contributes to hydrogen bonding between water molecules and within or between biological molecules.',False,'dotted attraction between neighboring molecules while the O–H covalent bonds remain intact')
],
'The ropes of water tumble off the mezzanine and land together in the pool below. Instead of behaving as separate droplets, they cling to one another.',next_locus='Cohesion Pool'))

scenes.append(scene(2,'Cohesion Pool','The Pool That Refuses to Come Apart','Watch what water sticks to—and what it does not.',
'You are on Level 2 at a shallow glass pool directly beneath the waterfall. The water surface is broad and flat. One wall of the pool is clear glass, so you can see droplets clinging to it above the waterline.',
{'orientation':'The waterfall enters from the north. The pool fills the center. A clear glass wall is on the east. A narrow green service tube rises from the far end toward Xylem Tower.',
 'zones':[{'position':'left','label':'Water surface','symbol':'≈','description':'Surface molecules are pulled inward by neighboring water molecules.'},{'position':'center','label':'Water cluster','symbol':'💧💧','description':'Water molecules attract other water molecules.'},{'position':'right','label':'Glass wall','symbol':'▥','description':'Water droplets cling to a different polar surface.'}]},
[{'name':'Cohesion','kind':'water-to-water attraction','visual':'water molecules holding onto other water molecules','job':'keeps water molecules associated with one another'},
 {'name':'Surface tension','kind':'surface effect','visual':'the top of the pool pulled tight like a flexible skin','job':'makes the water surface resist disruption because of cohesive interactions'},
 {'name':'Adhesion','kind':'water-to-other-surface attraction','visual':'droplets clinging to the glass wall','job':'keeps water attached to other polar or charged materials'}],
[
'The waterfall slams into the pool, but the water does not explode into independent beads. Molecule after molecule pulls on neighboring water molecules through hydrogen bonding. Mara cups her hands in the pool and lifts them. A single sheet stretches between her fingers before it breaks. **Cohesion** is the attraction among molecules of the same kind; here, it is water holding onto water.',
'At the very top of the pool, the molecules have water beside and below them but not above them. The combined cohesive pull is directed inward. The surface tightens and resists being disturbed. That surface effect is **surface tension**. Picture the top layer as a stretched, flexible skin created by the molecules pulling together beneath it.',
'Mara points to a different clue on the glass wall. A ribbon of water has climbed several centimeters above the pool and refuses to fall. Those droplets are not holding onto other water molecules alone. They are attracted to the polar surface of the glass. Attraction between water and another polar or charged material is **adhesion**.',
'Two attractions are now operating at once. Cohesion keeps water connected to water. Adhesion helps water cling to a surface. At the far end of the pool, both effects begin pulling water into a narrow green tube that disappears upward through the ceiling.'
],
[
 beat('MO-APBIO-U1-W006','Cohesion','Water molecules remain associated with other water molecules.','Cohesion is attraction among molecules of the same kind; hydrogen bonding contributes strongly to cohesion among water molecules.',True,'water holding onto water'),
 beat('MO-APBIO-U1-W007','Surface tension','The surface resists disruption because cohesive interactions pull surface molecules inward.','Surface tension results from cohesive interactions among water molecules at the surface.',True,'the top layer of the pool pulled tight by water-to-water attraction'),
 beat('MO-APBIO-U1-W008','Adhesion','Water clings to the glass wall, a different polar surface.','Adhesion is attraction of water to other polar or charged substances.',True,'water clinging to the glass wall instead of another water molecule')
],
'The thin green tube fills from the bottom. A connected column of water begins climbing inside it. Mara opens the maintenance door beside the tube. “That’s our way up.”',next_locus='Xylem Tower'))

scenes.append(scene(3,'Xylem Tower','The Climb Inside the Glass Stem','Follow a continuous column of water upward.',
'You are inside the hotel’s vertical greenhouse shaft. A transparent model of a plant stem runs through its center. Narrow xylem tubes rise beside a spiral maintenance staircase, carrying water toward the rooftop plants.',
{'orientation':'You enter at the bottom of a tall cylindrical shaft. The staircase spirals around the outside. The xylem tube runs vertically through the center, from the root tank below to the greenhouse above.',
 'zones':[{'position':'left','label':'Xylem wall','symbol':'│','description':'Water molecules cling to the hydrophilic inner surface.'},{'position':'center','label':'Water column','symbol':'↑💧','description':'Connected water molecules remain associated as the column rises.'},{'position':'right','label':'Narrow side tube','symbol':'↟','description':'The combined effects are especially visible in a narrow space.'}]},
[{'name':'Xylem','kind':'plant transport tissue','visual':'long transparent tubes running upward through the stem model','job':'provides the pathway through which water moves upward in plants'},
 {'name':'Cohesion','kind':'same-substance attraction','visual':'water molecules holding together in a continuous column','job':'helps keep the water column connected'},
 {'name':'Adhesion','kind':'water-to-surface attraction','visual':'water molecules clinging along the tube wall','job':'helps water interact with the xylem wall rather than simply slipping downward'},
 {'name':'Capillary action','kind':'movement in narrow spaces','visual':'water rising through a very narrow tube','job':'results from the combined effects of cohesion and adhesion in a narrow space'}],
[
'The maintenance door closes behind you, and the hotel becomes a vertical tunnel of glass and leaves. In the center stands a giant transparent stem. Inside it, a narrow **xylem** tube carries water upward toward the roof garden. The water is not a set of isolated droplets. It forms a connected column.',
'Look at the middle of that column. Water molecules keep attracting neighboring water molecules. The **cohesion** you saw in the pool helps the column remain connected as it moves upward. Now look at the edge. Some water molecules are pressed against the inner wall of the tube and remain attracted to that hydrophilic surface. That is **adhesion** acting inside the xylem.',
'Mara shines her light on an even narrower side tube. Water has crept farther upward there. In a narrow space, water-to-water cohesion and water-to-surface adhesion work together to produce **capillary action**. The useful picture is not “one force wins.” It is the combination: water stays connected while also interacting with the surface around it.',
'You climb the spiral stairs beside the rising water. By the time you reach Level 6, the xylem line bends out of the greenhouse shaft and passes through the hotel spa. The metal pipes are hot enough to glow on Mara’s scanner.'
],
[
 beat('MO-APBIO-U1-W009','Cohesion and plant transport','Water molecules remain connected in a column as water moves upward through plant tissue.','Water cohesion contributes to the upward transport of water in plants.',False,'a continuous column of water rising through xylem'),
 beat('MO-APBIO-U1-W010','Adhesion in xylem','Water molecules cling to hydrophilic surfaces along the xylem wall.','Adhesion contributes to water interacting with xylem and cell walls and helps oppose downward movement due to gravity.',False,'water clinging along the inside wall of the xylem tube'),
 beat('MO-APBIO-U1-W011','Capillary action','Water rises through a narrow tube as cohesion and adhesion act together.','Cohesion among water molecules and adhesion to hydrophilic surfaces together contribute to capillary movement in narrow spaces and to water transport in plants.',True,'a connected water column climbing a narrow tube while also clinging to its walls')
],
'The rising water line disappears through a copper doorway marked THERMAL BATH. When Mara opens it, a wave of hot air rolls into the stairwell.',checkpoint=True,checkpoint_object_id='MO-APBIO-U1-W011',checkpoint_prompt='Water molecules stay connected to one another while also clinging to the wall of a narrow tube. What is the upward movement produced by those combined effects called?',next_locus='Thermal Bath'))

scenes.append(scene(4,'Thermal Bath','The Pool That Heats Too Slowly','Energy pours in, but the water temperature resists the change.',
'You are in the Level 6 spa. A large rectangular bath fills the room. Heating coils run beneath it. Temperature screens line the far wall, and the water line from Xylem Tower passes directly through the bath.',
{'orientation':'You enter from the greenhouse stairs on the west. The bath occupies the center. Heating coils are beneath it. The open-air Evaporation Balcony lies beyond the east doors.',
 'zones':[{'position':'left','label':'Heat input','symbol':'🔥','description':'The heating system is dumping energy into the bath.'},{'position':'center','label':'Water bath','symbol':'♨','description':'The water temperature rises only gradually despite continued energy input.'},{'position':'right','label':'Temperature screens','symbol':'🌡','description':'Nearby water-linked systems avoid rapid temperature swings.'}]},
[{'name':'High specific heat capacity','kind':'thermal property','visual':'a thermometer that moves slowly even while heat continues entering','job':'allows water to absorb substantial energy with a relatively small temperature change'},
 {'name':'Hydrogen bonds','kind':'intermolecular interactions','visual':'temporary links among neighboring water molecules repeatedly disrupting and forming','job':'absorb energy when disrupted and release energy when formed'},
 {'name':'Temperature moderation','kind':'biological/environmental consequence','visual':'body, lake, and air-temperature indicators changing more gradually beside large amounts of water','job':'reduces rapid temperature fluctuation'}],
[
'The spa should be boiling. Heating coils glow beneath the bath, and the room itself feels painfully hot, yet the giant water thermometer crawls upward one small division at a time. Mara taps the screen. “Watch the water, not the heater.” Water has a **high specific heat capacity**: changing its temperature requires a large amount of energy compared with substances whose temperature changes more readily.',
'Her scanner magnifies the bath again. The water molecules are moving faster as energy enters, but some of that energy is also involved in disrupting hydrogen-bond interactions among neighboring molecules. Those interactions can form again, releasing energy. This constant molecular rearrangement helps explain why water can absorb or release substantial energy while its temperature changes relatively slowly.',
'The consequence is larger than this room. On the wall, three systems are connected to water: a body-temperature monitor, an outdoor-air monitor near a large body of water, and an aquatic-temperature monitor. None swings as wildly as the emergency heat input does. Large amounts of water can **moderate temperature**, helping living systems and environments avoid abrupt changes.',
'A hiss rises from the bath. At last, some molecules at the surface have enough energy to escape into the air. The steam alarms open the doors to the balcony automatically.'
],
[
 beat('MO-APBIO-U1-W012','High specific heat capacity','The bath absorbs substantial energy while its temperature changes relatively slowly.','Water resists rapid temperature change because it has a high specific heat capacity, a property that contributes to temperature stability in organisms and environments.',True,'a large bath receiving heat while its thermometer moves slowly'),
 beat('MO-APBIO-U1-W013','Hydrogen-bond mechanism for specific heat','Energy is involved in disrupting hydrogen-bond interactions, and energy is released when those interactions form.','Hydrogen bonding contributes to water’s high specific heat because energy is absorbed when hydrogen-bond interactions are disrupted and released when they form.',False,'hydrogen-bond interactions repeatedly disrupting and reforming as heat moves through water'),
 beat('MO-APBIO-U1-W014','Environmental moderation','Large amounts of water reduce rapid temperature fluctuations in nearby systems.','Water’s high specific heat contributes to moderation of environmental temperatures and reduced temperature fluctuations in organisms.',False,'body, lake, and air-temperature displays changing gradually beside water')
],
'The balcony doors fly open. Wind tears steam from the bath and carries it outside, where a broken misting line has soaked the deck.',next_locus='Evaporation Balcony'))

scenes.append(scene(5,'Evaporation Balcony','The Wind That Steals Heat','The fastest molecules leave—and take energy with them.',
'You are on an open-air balcony seven floors above the lobby. Rain has stopped, but a broken misting pipe sprays the deck. Wind moves across the wet surface toward the cold-storage level above.',
{'orientation':'The spa doors are behind you to the west. The wet balcony deck fills the center. The cold-storage corridor and Ice Lake are through the north stairwell.',
 'zones':[{'position':'left','label':'Wet surface','symbol':'💦','description':'Liquid water molecules have a range of kinetic energies.'},{'position':'center','label':'Vapor edge','symbol':'↑','description':'Higher-energy molecules escape from the liquid into the air.'},{'position':'right','label':'Cooling surface','symbol':'❄','description':'The remaining surface loses energy and becomes cooler.'}]},
[{'name':'High heat of vaporization','kind':'thermal property','visual':'water molecules needing substantial energy before they can escape the liquid','job':'makes evaporation require a large energy input'},
 {'name':'Evaporative cooling','kind':'consequence of evaporation','visual':'higher-energy molecules leaving while the remaining surface cools','job':'removes heat from a surface as water evaporates'}],
[
'The wind catches the water on the deck and turns it into a fine mist. Mara holds out her forearm. Within seconds the wet skin feels colder than the dry skin beside it. “Follow the energy,” she says.',
'For a water molecule to leave the liquid and become vapor, it must overcome the attractions holding it among neighboring molecules. That takes substantial energy. Water therefore has a **high heat of vaporization**: a large amount of energy is required for liquid water to become water vapor.',
'The molecules most able to escape are among the higher-energy molecules at the surface. When they leave, they carry energy away with them. The average energy of the water left behind decreases, so the surface cools. That is **evaporative cooling**. The same relationship helps explain cooling when sweat evaporates from skin and when water evaporates from plant surfaces.',
'Mara wipes her arm dry and points toward the north stairwell. Vapor blown from the balcony has condensed along the refrigerated service level above. The emergency door is rimmed with frost.'
],
[
 beat('MO-APBIO-U1-W015','High heat of vaporization','Liquid water needs substantial energy before molecules can escape into the vapor phase.','Water requires substantial energy to evaporate; this high heat of vaporization supports evaporative cooling and temperature maintenance.',True,'water molecules needing a large energy input before leaving the liquid'),
 beat('MO-APBIO-U1-W016','Evaporative cooling','Higher-energy molecules escape and carry energy away, lowering the average energy of the remaining liquid surface.','As water molecules evaporate, the surface they leave behind cools.',True,'the fastest molecules leaving the wet surface while the thermometer falls'),
 beat('MO-APBIO-U1-W017','Biological and environmental cooling examples','The same evaporation-and-energy-loss relationship can cool organisms and water-exposed surfaces.','Evaporation of water contributes to cooling in biological and environmental contexts, including sweating and water loss from leaves.',False,'Mara’s wet forearm cooling as water evaporates')
],
'The frost-covered door opens into a dark blue chamber. A sheet of ice floats on a clear indoor lake, and living fish move beneath it.',checkpoint=True,checkpoint_object_id='MO-APBIO-U1-W015',checkpoint_prompt='Water molecules must gain a large amount of energy to escape from liquid water into vapor. What property of water describes that large energy requirement?',next_locus='Ice Lake'))

scenes.append(scene(6,'Ice Lake','The Ice That Refuses to Sink','Freezing spreads the molecules apart.',
'You are inside the Level 8 climate chamber. A clear lake fills the floor from wall to wall. A white sheet of ice floats at the surface, while liquid water and fish remain underneath.',
{'orientation':'The refrigerated stairwell enters from the south. The lake fills the center. A molecular lattice projector stands on the east shore. The service hatch to the Solution Bar is beyond the north edge.',
 'zones':[{'position':'left','label':'Liquid water','symbol':'💧','description':'Molecules move and pack more closely on average than in the frozen lattice.'},{'position':'center','label':'Floating ice','symbol':'🧊','description':'The solid occupies more volume for the same amount of water and remains at the surface.'},{'position':'right','label':'Lattice projector','symbol':'◇','description':'Hydrogen bonds hold water molecules in an open crystalline arrangement.'}]},
[{'name':'Ice','kind':'solid water','visual':'an open hydrogen-bonded lattice','job':'forms a lower-density solid structure that floats on liquid water'},
 {'name':'Hydrogen-bond lattice','kind':'solid arrangement','visual':'each water molecule held in an open network with four neighboring interactions','job':'spaces molecules farther apart than they are in liquid water'},
 {'name':'Aquatic life below ice','kind':'biological consequence','visual':'liquid water and organisms remaining below the floating surface ice','job':'shows why floating ice allows liquid habitat to remain underneath'}],
[
'The lake looks impossible at first. The solid ice is floating on top of its own liquid. Mara kneels at the edge and activates the lattice projector. The image enlarges a patch of freezing water until individual molecules become visible.',
'As water freezes, hydrogen bonds stabilize the molecules in an **open crystalline lattice**. The molecules are held farther apart than they are, on average, in liquid water. The same amount of water therefore occupies more space when it freezes. Its density decreases. That is why **ice is less dense than liquid water** and floats.',
'The projector highlights one water molecule in the solid. Around it, four neighboring water molecules fit into the hydrogen-bonded network. The important picture is the open spacing: the lattice leaves more empty space than the more mobile arrangement in liquid water.',
'Mara shines her light through the ice. Fish are still moving in liquid water beneath the floating sheet. Because the ice remains at the surface rather than sinking through the lake, liquid aquatic habitat can remain below it.',
'At the north edge, the floating ice has lifted a service hatch just enough for Mara to pull it open. Warm light spills out from a quiet bar on the next level.'
],
[
 beat('MO-APBIO-U1-W018','Ice is less dense than liquid water','Freezing produces an open arrangement that spaces water molecules farther apart and lowers density.','Ice is less dense than liquid water because freezing organizes water molecules into an open hydrogen-bonded lattice that spaces them farther apart than in the liquid.',False,'an open ice lattice floating above more densely packed liquid water'),
 beat('MO-APBIO-U1-W019','Ice hydrogen-bond lattice','Hydrogen bonds stabilize an open crystalline network in the solid.','In ice, hydrogen bonds stabilize an open crystalline lattice in which each water molecule can hydrogen-bond with four neighboring water molecules.',False,'one water molecule positioned within an open four-neighbor lattice'),
 beat('MO-APBIO-U1-W020','Floating ice supports aquatic life','Surface ice leaves liquid water habitat below instead of sinking through it.','The lower density of ice allows it to float, leaving liquid water beneath that can support aquatic life.',False,'fish swimming in liquid water below the floating ice sheet')
],
'You climb through the hatch and enter a silent lounge. Behind the bar, three unlabeled containers wait beside a glass of water.',next_locus='Solution Bar'))

scenes.append(scene(7,'Solution Bar','Three Roles in One Glass','Name the medium, the dissolved substance, and the mixture.',
'You are at the Level 9 service bar. A clear pitcher of water stands in the middle. To its left is a dish of salt crystals. To its right is an empty glass. Nothing else is on the counter.',
{'orientation':'The counter runs east to west. Salt crystals begin on the left, the water pitcher is in the center, and the final mixed glass sits on the right. A glass door behind the bar leads to the Hydration Aquarium.',
 'zones':[{'position':'left','label':'Starting substance','symbol':'◇','description':'The salt begins as the substance that will be dissolved.'},{'position':'center','label':'Dissolving medium','symbol':'💧','description':'Water surrounds and disperses the dissolved particles.'},{'position':'right','label':'Final mixture','symbol':'🥛','description':'After mixing, the components are uniformly distributed through the glass.'}]},
[{'name':'Solute','kind':'component of a solution','visual':'the salt crystals before they dissolve','job':'is the substance being dissolved'},
 {'name':'Solvent','kind':'component of a solution','visual':'the water in the pitcher','job':'is the dissolving medium'},
 {'name':'Solution','kind':'mixture','visual':'the final uniform glass after the solute disperses','job':'is the homogeneous mixture formed from solvent and dissolved solute'}],
[
'Mara puts one hand on the salt dish and the other on the water pitcher. “Three words. Three jobs. Keep the jobs separate.” She pours the water into the empty glass first. The water is the **solvent** because it is the dissolving medium.',
'Next she tips in the salt crystals. Before they disappear, you can still see them as the material being dissolved. That material is the **solute**.',
'She stirs. The visible crystals vanish as their particles disperse through the water. Now point to the entire glass—the water together with the dissolved salt. The complete homogeneous mixture is the **solution**.',
'Mara repeats the three roles once while touching the actual objects: solvent, the dissolving medium; solute, the substance dissolved; solution, the homogeneous mixture. Then she slides the glass onto a glowing pad behind the counter. The pad magnifies what happened to the ions inside.'
],
[
 beat('MO-APBIO-U1-W021','Solvent','Water acts as the dissolving medium.','A solvent is the dissolving agent or medium; water can dissolve many ionic and polar substances because of its polarity.',True,'the water pitcher that does the dissolving'),
 beat('MO-APBIO-U1-W022','Solution','The final glass is a homogeneous mixture containing the solvent and dissolved solute.','A solution is a homogeneous mixture of two or more substances.',True,'the entire uniformly mixed glass'),
 beat('MO-APBIO-U1-W023','Solute','The salt is the substance being dissolved.','A solute is the substance dissolved in a solution.',True,'the salt crystals before they disappear into the water')
],
'The glowing pad opens the glass wall behind the bar. Inside is a room-sized molecular display where separated ions hang in clear water like exhibits in an aquarium.',next_locus='Hydration Aquarium'))

scenes.append(scene(8,'Hydration Aquarium','Water Turns Around the Ions','Polarity tells each water molecule which way to face.',
'You are behind the bar inside a room-sized molecular display. A positive ion is suspended in a tank on the left and a negative ion in a tank on the right. Hundreds of enlarged water molecules move around them.',
{'orientation':'Two transparent tanks face you. The cation tank is left, the anion tank is right, and a polar-solute display runs along the center aisle. The exit drains toward the pH Staircase.',
 'zones':[{'position':'left','label':'Positive ion','symbol':'+','description':'Water turns its partial-negative oxygen side toward the cation.'},{'position':'center','label':'Polar solute aisle','symbol':'±','description':'Polar water can interact favorably with other charged or polar regions.'},{'position':'right','label':'Negative ion','symbol':'−','description':'Water turns its partial-positive hydrogen sides toward the anion.'}]},
[{'name':'Water polarity','kind':'molecular property','visual':'δ− oxygen end and δ+ hydrogen ends','job':'lets water orient differently around positive and negative charges'},
 {'name':'Hydration shell','kind':'arrangement around dissolved ions','visual':'water molecules surrounding an ion with charge-compatible orientation','job':'stabilizes separated ions in water'},
 {'name':'Like dissolves like','kind':'useful heuristic','visual':'polar water interacting with ions and other polar regions','job':'reminds you that substances with compatible polarity or charge interactions tend to mix more readily'}],
[
'In the left tank, a positive ion hangs motionless. Water molecules rush toward it, but they do not approach randomly. Each one turns so the **partial-negative oxygen side** faces the positive charge. Around the ion, a shell of oriented water molecules forms.',
'In the right tank, the orientation reverses. The ion is negative, so the **partial-positive hydrogen sides** of nearby water molecules point inward. The water molecules surround both kinds of ions, but the direction they face depends on charge.',
'This is one reason ionic substances can dissolve in water: polar water interacts with the separated charged particles. The same general idea supports the useful heuristic **“like dissolves like.”** Polar water interacts well with ions and many polar substances because its own partial charges can make favorable interactions with them.',
'Mara taps the bottom of the tank. Two drains open—one glowing red and one blue. The water flows into a stairwell whose steps are numbered from low pH at the bottom to high pH at the top.'
],
[
 beat('MO-APBIO-U1-W024','Like dissolves like','Polar water interacts favorably with ions and many polar solutes.','A useful solubility heuristic is “like dissolves like”: polar solvents such as water tend to interact well with ions and polar substances.',False,'polar water turning toward charged or polar regions'),
 beat('MO-APBIO-U1-W025','Hydration of ions','Water surrounds dissolved ions with charge-dependent orientation.','Around cations, water’s oxygen side is oriented inward; around anions, water’s hydrogen sides are oriented inward.',False,'oxygen toward +, hydrogens toward −')
],
'The two drains meet at the foot of the staircase. A pH alarm flashes overhead, and the numbers on the steps begin changing color.',next_locus='pH Staircase'))

scenes.append(scene(9,'pH Staircase','The Staircase of Hydrogen Ions','More H⁺ sends you down; less H⁺ sends you up.',
'You are in a narrow stairwell that rises two floors toward the roof. The steps are numbered like a pH scale: lower numbers glow red, the middle landing is neutral, and higher numbers glow blue. A live display tracks hydrogen-ion concentration.',
{'orientation':'The lowest-pH steps descend to the left in red. The neutral landing is in the center. Higher-pH steps rise to the right in blue. The Buffer Gate is at the top landing.',
 'zones':[{'position':'left','label':'Acid side','symbol':'H⁺↑','description':'Greater hydrogen-ion concentration corresponds to lower pH.'},{'position':'center','label':'Water exchange','symbol':'H₃O⁺ / OH⁻','description':'Water molecules can transfer a proton, producing hydronium and hydroxide.'},{'position':'right','label':'Base side','symbol':'H⁺↓','description':'Lower hydrogen-ion concentration corresponds to higher pH.'}]},
[{'name':'pH','kind':'measure','visual':'a numbered staircase linked to hydrogen-ion concentration','job':'expresses hydrogen-ion concentration on a logarithmic scale'},
 {'name':'Acid','kind':'chemical behavior','visual':'an input that increases H⁺ in solution','job':'increases hydrogen-ion concentration'},
 {'name':'Base','kind':'chemical behavior','visual':'a system that lowers H⁺ concentration or contributes OH⁻ that can combine with H⁺','job':'reduces hydrogen-ion concentration'},
 {'name':'Hydronium and hydroxide','kind':'products of water self-ionization','visual':'H₃O⁺ and OH⁻ appearing after a proton transfers between water molecules','job':'show that water can self-ionize and that H⁺ in water is associated with water molecules'}],
[
'The stairwell is built around one relationship: **pH is tied to hydrogen-ion concentration**. Mara releases a cluster of H⁺ markers into the display. The red lower steps brighten. Greater hydrogen-ion concentration means lower pH and greater acidity. The scale is logarithmic, expressed conventionally as **pH = −log[H⁺]**.',
'On the red side, an **acid** input increases the hydrogen-ion concentration. On the blue side, a **base** reduces hydrogen-ion concentration—for example, by accepting H⁺ or by contributing OH⁻ that can combine with H⁺. Keep the direction clear: more H⁺, lower pH; less H⁺, higher pH.',
'At the center landing, Mara switches the scanner to water itself. Two water molecules collide in the display and a proton transfers from one to the other. The products are **hydronium, H₃O⁺**, and **hydroxide, OH⁻**. In biological chemistry, H⁺ is often used as convenient shorthand for the proton-related concentration in aqueous solution, but the proton is associated with water molecules rather than floating alone.',
'The alarm suddenly jerks from the acidic side toward the basic side and back again. The roof reservoir is receiving disturbances faster than the controller can correct them. Mara takes the final stairs two at a time.'
],
[
 beat('MO-APBIO-U1-W026','pH','The staircase links hydrogen-ion concentration to a logarithmic pH value.','pH is a logarithmic measure related to hydrogen-ion concentration, conventionally expressed as pH = −log[H+]. Lower pH corresponds to greater acidity; higher pH corresponds to greater basicity.',True,'more H+ lighting the lower steps and less H+ lighting the higher steps'),
 beat('MO-APBIO-U1-W027','Acid','The acid input raises hydrogen-ion concentration and shifts the display toward lower pH.','An acid increases the hydrogen-ion concentration of a solution, commonly by donating H+.',True,'an input adding H+ and pushing the indicator down the pH staircase'),
 beat('MO-APBIO-U1-W028','Base','The base side reduces hydrogen-ion concentration.','A base reduces hydrogen-ion concentration, for example by accepting H+ or by contributing OH− that combines with H+.',True,'a process removing H+ or supplying OH−, shifting the indicator upward'),
 beat('MO-APBIO-U1-W029','Water dissociation','A proton transfer between water molecules produces hydronium and hydroxide.','Water self-ionizes to hydronium (H3O+) and hydroxide (OH−). In aqueous biological chemistry, H+ is commonly used as shorthand for proton-related concentration.',False,'two water molecules exchanging a proton to form H3O+ and OH−')
],
'Mara reaches the roof landing and throws open a heavy circular door. Behind it, the reservoir pH alarm is swinging from red to blue.',next_locus='Buffer Gate'))

scenes.append(scene(10,'Buffer Gate','The System That Takes the Hit','The final job is to keep pH from swinging wildly.',
'You are on the roof inside the water-control room. A large reservoir sits behind glass. Acid and base disturbance indicators flash on either side of it. The greenhouse and aquarium status lights are dark.',
{'orientation':'The reservoir fills the center of the roof room. Acid disturbance enters from the left and base disturbance from the right. The life-support control panel is directly in front of you.',
 'zones':[{'position':'left','label':'Acid disturbance','symbol':'H⁺','description':'An incoming acid tends to push pH downward.'},{'position':'center','label':'Buffer system','symbol':'◎','description':'The buffer resists a large change in pH when acid or base is added.'},{'position':'right','label':'Base disturbance','symbol':'OH⁻','description':'An incoming base tends to push pH upward.'}]},
[{'name':'Buffer','kind':'pH-stabilizing system','visual':'a central control system that dampens acidic and basic disturbances','job':'resists changes in pH when acid or base is added'}],
[
'The reservoir alarm is impossible to ignore. A pulse from the acid side drives the pH downward. A moment later, a disturbance from the base side pushes it upward. The problem is no longer identifying which direction pH moves. The problem is preventing either disturbance from producing a large swing.',
'Mara opens the final control housing. Inside is the **buffer system**. When acid or base is added, the buffer resists the resulting change in pH. It does not freeze pH at one exact number, and it does not make acids or bases disappear. Its job is to make the change smaller than it would otherwise be.',
'You reset the reservoir through the buffer controller. The alarm’s violent red-blue swings shrink to small movements around the safe range. One by one, the rooftop greenhouse lights return. Below the glass floor, the aquarium pumps restart. The hotel’s living systems have water again.',
'Mara looks down the central shaft. From the roof you can see almost the entire route: ice chamber, balcony, thermal bath, xylem tower, pool, and the fountain far below. The emergency was one connected story. Molecular polarity allowed hydrogen bonding. Those interactions helped produce cohesion and adhesion, thermal properties, unusual freezing behavior, solvent behavior, and the chemistry you followed all the way to pH control.'
],
[
 beat('MO-APBIO-U1-W030','Buffer','The central system reduces the size of pH changes caused by added acid or base.','A buffer resists changes in pH when acid or base is added and helps maintain pH stability in biological systems.',True,'the roof controller dampening red and blue pH swings instead of letting them travel across the full scale')
],
'The pH alarm settles into a steady green line. The Flooded Sky Hotel is stable again—and the route from molecule to organism is now one path you can mentally walk from the lobby to the roof.',checkpoint=True,checkpoint_object_id='MO-APBIO-U1-W030',checkpoint_prompt='Acid and base disturbances hit the reservoir, but its pH changes only a little. What kind of system resists those changes in pH?',next_locus=None))

journey['scenes']=scenes
OUT.write_text(json.dumps(journey,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('wrote',OUT,'scenes',len(scenes),'beats',sum(len(s['story_beats']) for s in scenes))
