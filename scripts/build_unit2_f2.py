from __future__ import annotations
import json, hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U2=ROOT/'content'/'ap-biology'/'unit-2'
SRC=U2/'source'/'canonical-unit2-f1.json'
ARCH=U2/'architecture'
ARCH.mkdir(parents=True,exist_ok=True)

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def dump(p,obj): Path(p).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

src=load(SRC)
records={r['knowledge_id']:r for r in src['canonical_catalog']}

journeys=[
  {
    'journey_id':'U2-J1','working_title':'Cell Operations Complex','content_focus':'Cell identity, nucleus, ribosomes, endomembrane flow, recycling/storage, and cytoskeleton','setting_logic':'A coherent operations complex supports physical movement from information control to protein production, processing, recycling, storage, and internal structural support.','bundles':[
      {'bundle_id':'U2-B01','title':'Cell identity and information control','loci':['U2-L01','U2-L02','U2-L03']},
      {'bundle_id':'U2-B02','title':'Protein production and endomembrane flow','loci':['U2-L04','U2-L05','U2-L06','U2-L07','U2-L08','U2-L09']},
      {'bundle_id':'U2-B03','title':'Recycling, storage, and internal support','loci':['U2-L10','U2-L11','U2-L12','U2-L13']},
    ]
  },
  {
    'journey_id':'U2-J2','working_title':'Energy Conversion Annex','content_focus':'Mitochondrial and chloroplast structure-function relationships','setting_logic':'A power-conversion annex makes nested membranes, compartments, surface area, and energy-conversion structures spatially explicit without mixing them into the already dense endomembrane route.','bundles':[
      {'bundle_id':'U2-B04','title':'Mitochondrial architecture','loci':['U2-L14','U2-L15','U2-L16']},
      {'bundle_id':'U2-B05','title':'Chloroplast architecture','loci':['U2-L17','U2-L18']},
    ]
  },
  {
    'journey_id':'U2-J3','working_title':'Scaling Observatory','content_focus':'Surface-area-to-volume relationships, cell-size constraints, exchange surfaces, and organism scaling','setting_logic':'A modeling observatory lets learners compare geometrically similar objects at different scales and watch exchange and thermal consequences change with size.','bundles':[
      {'bundle_id':'U2-B06','title':'Scale, exchange, and geometry','loci':['U2-L19','U2-L20','U2-L21']},
    ]
  },
  {
    'journey_id':'U2-J4','working_title':'Membrane Border Terminal','content_focus':'Membrane structure, fluidity, proteins, recognition, selective permeability, cell walls, and plasmodesmata','setting_logic':'A border terminal gives the membrane one stable spatial metaphor: a dynamic boundary with a molecular fabric, embedded workers, recognition markers, selective lanes, and an external plant-cell wall.','bundles':[
      {'bundle_id':'U2-B07','title':'Bilayer organization and fluidity','loci':['U2-L22','U2-L23','U2-L24']},
      {'bundle_id':'U2-B08','title':'Membrane proteins and recognition','loci':['U2-L25','U2-L26']},
      {'bundle_id':'U2-B09','title':'Selectivity and outer boundaries','loci':['U2-L27','U2-L28','U2-L29']},
    ]
  },
  {
    'journey_id':'U2-J5','working_title':'Gradient Transit Hub','content_focus':'Diffusion, passive/active transport, facilitated diffusion, channels/carriers, bulk transport, electrochemical gradients, pumps, and cotransport','setting_logic':'A multilevel transit hub makes direction, gradients, energy use, transport proteins, vesicles, and coupled movement visible as different ways of crossing the same boundary.','bundles':[
      {'bundle_id':'U2-B10','title':'Downhill and protein-assisted transport','loci':['U2-L30','U2-L31','U2-L32','U2-L33','U2-L34','U2-L35']},
      {'bundle_id':'U2-B11','title':'Vesicle transport','loci':['U2-L36','U2-L37']},
      {'bundle_id':'U2-B12','title':'Electrochemical active transport','loci':['U2-L38','U2-L39']},
    ]
  },
  {
    'journey_id':'U2-J6','working_title':'Osmosis Conservatory','content_focus':'Tonicity, osmosis, water potential, plant-cell water responses, and osmoregulation','setting_logic':'A glass conservatory with controlled solution chambers makes water movement and plant-cell responses visible while separating conceptual tonicity from quantitative water-potential work.','bundles':[
      {'bundle_id':'U2-B13','title':'Tonicity outcomes','loci':['U2-L40','U2-L41','U2-L42','U2-L43']},
      {'bundle_id':'U2-B14','title':'Water potential and osmoregulation','loci':['U2-L44','U2-L45']},
    ]
  },
  {
    'journey_id':'U2-J7','working_title':'Compartment Origins Archive','content_focus':'Compartmentalization and endosymbiotic origins','setting_logic':'An origins archive lets learners first compare internal organization, then examine endosymbiosis as an evidence-supported historical explanation rather than a decorative fantasy event.','bundles':[
      {'bundle_id':'U2-B15','title':'Why cells compartmentalize','loci':['U2-L46','U2-L47']},
      {'bundle_id':'U2-B16','title':'Endosymbiotic origins and evidence','loci':['U2-L48','U2-L49']},
    ]
  },
]

# locus_id, journey_id, bundle_id, title, micro_anchor, layout(left,center,right), primary, records, visual_mode
raw_loci=[
('U2-L01','U2-J1','U2-B01','Cell Entry Atrium','the three-way identity gate immediately inside the entrance', ['prokaryote inspection bay','shared-cell essentials turntable','eukaryote inspection bay'],'U2-K-067',['U2-K-067','U2-K-068','U2-K-069'],'COMPARISON_SCENE'),
('U2-L02','U2-J1','U2-B01','Nuclear Archive','the sealed archive door with a pore-controlled checkpoint', ['double nuclear-envelope wall','chromosome archive chamber','nuclear pore checkpoint'],'U2-K-070',['U2-K-070','U2-K-071'],'STRUCTURE_FUNCTION_CUTAWAY'),
('U2-L03','U2-J1','U2-B01','Nucleolus Assembly Room','the dense circular assembly bench at the center of the archive', ['rRNA transcription desk','ribosomal-subunit assembly bench','subunit exit lane'],'U2-K-072',['U2-K-072','U2-K-001','U2-K-002'],'ASSEMBLY_PROCESS'),
('U2-L04','U2-J1','U2-B02','Ribosome Platforms','the paired free and membrane-bound translation platforms', ['free-ribosome platform','mRNA translation stage','bound-ribosome platform'],'U2-K-003',['U2-K-003','U2-K-073','U2-K-074'],'SPLIT_DESTINATION_SCENE'),
('U2-L05','U2-J1','U2-B02','Endomembrane Map Room','the wall-sized route map connecting the nuclear envelope, ER, Golgi, vesicles, lysosomes, vacuoles, and plasma membrane', ['incoming synthesis routes','endomembrane route map','outgoing transport routes'],'U2-K-004',['U2-K-004','U2-K-005','U2-K-006'],'SYSTEM_MAP'),
('U2-L06','U2-J1','U2-B02','Rough ER Assembly Hall','the ribosome-studded cisterna beside the map room', ['cytosolic ribosome surface','rough-ER cisterna and lumen','transport-vesicle exit'],'U2-K-007',['U2-K-007','U2-K-075'],'STRUCTURE_FUNCTION_PROCESS'),
('U2-L07','U2-J1','U2-B02','Smooth ER Detox Lab','the smooth tubular bench with no attached ribosomes', ['lipid-synthesis station','smooth-ER tubule network','detoxification/calcium/carbohydrate stations'],'U2-K-008',['U2-K-008','U2-K-076'],'FUNCTION_LAB'),
('U2-L08','U2-J1','U2-B02','Golgi Receiving Stack','the cis-facing side of a stack of flattened cisternae', ['ER transport-vesicle arrival','stacked Golgi cisternae','cis-face receiving dock'],'U2-K-009',['U2-K-009','U2-K-079','U2-K-077'],'STRUCTURE_ORIENTATION_SCENE'),
('U2-L09','U2-J1','U2-B02','Golgi Dispatch Floor','the trans-facing sorting and shipping side of the Golgi stack', ['modification/sorting tables','tagged cargo staging area','trans-face dispatch dock'],'U2-K-011',['U2-K-010','U2-K-011','U2-K-078'],'PROCESS_SEQUENCE'),
('U2-L10','U2-J1','U2-B03','Lysosome Recycling Bay','the enzyme-filled digestion chamber beside the Golgi shipping floor', ['incoming damaged/captured material','lysosomal digestion chamber','recycled products and apoptosis control'],'U2-K-014',['U2-K-014','U2-K-015','U2-K-080'],'DIGESTION_RECYCLING_SEQUENCE'),
('U2-L11','U2-J1','U2-B03','Vacuole Reservoir Gallery','the row of differently sized membrane-bound reservoirs', ['food/animal vacuole cases','large plant central reservoir','contractile-vacuole pump'],'U2-K-016',['U2-K-016','U2-K-017','U2-K-018','U2-K-082','U2-K-083'],'COMPARISON_GALLERY'),
('U2-L12','U2-J1','U2-B03','Peroxisome Oxidation Booth','the small isolated oxidation chamber marked with a peroxide hazard symbol', ['oxidation enzyme station','peroxisome chamber','catalase/peroxide safety station'],'U2-K-081',['U2-K-081'],'DISTINCTION_SCENE'),
('U2-L13','U2-J1','U2-B03','Cytoskeleton Framework','the exposed structural framework spanning the final hall', ['actin tension network','microtubule rail network and organizing center','intermediate-filament support cables'],'U2-K-092',['U2-K-092','U2-K-093','U2-K-094','U2-K-095','U2-K-096'],'STRUCTURE_FUNCTION_NETWORK'),

('U2-L14','U2-J2','U2-B04','Mitochondrial Membrane Airlock','the cutaway double-membrane entrance to the mitochondrial chamber', ['outer membrane','intermembrane space','inner membrane enclosing matrix'],'U2-K-012',['U2-K-012','U2-K-084','U2-K-085'],'NESTED_STRUCTURE_CUTAWAY'),
('U2-L15','U2-J2','U2-B04','Cristae Generator Deck','the deeply folded inner-membrane generator surface', ['smooth outer boundary','cristae-rich inner membrane','matrix-facing reaction side'],'U2-K-086',['U2-K-013','U2-K-086'],'SURFACE_AREA_STRUCTURE_FUNCTION'),
('U2-L16','U2-J2','U2-B04','Energy-Demand Control Bay','the cell-demand dashboard overlooking several mitochondria', ['low-demand cell display','mitochondrial abundance dashboard','high-demand cell display'],'U2-K-087',['U2-K-087'],'COMPARATIVE_DEMAND_SCENE'),
('U2-L17','U2-J2','U2-B05','Chloroplast Entry Chamber','the double-membrane chloroplast cutaway at the annex greenhouse entrance', ['outer/inner chloroplast membranes','chloroplast interior','plant/algal cell context display'],'U2-K-020',['U2-K-019','U2-K-020'],'STRUCTURE_FUNCTION_CUTAWAY'),
('U2-L18','U2-J2','U2-B05','Thylakoid and Stroma Gallery','the transparent chloroplast interior showing stacked thylakoids surrounded by stroma', ['granum/thylakoid stacks','chlorophyll-bearing thylakoid membranes','stroma space'],'U2-K-088',['U2-K-088','U2-K-089','U2-K-090','U2-K-091'],'NESTED_STRUCTURE_FUNCTION'),

('U2-L19','U2-J3','U2-B06','Cell Size Cube Gallery','the side-by-side cube-and-sphere modeling table', ['small-cell models','SA:V calculation/display table','large-cell models'],'U2-K-023',['U2-K-021','U2-K-022','U2-K-023','U2-K-024','U2-K-097','U2-K-098'],'QUANTITATIVE_SCALE_MODEL'),
('U2-L20','U2-J3','U2-B06','Exchange-Surface Fold Deck','the foldable membrane model mounted beside the scaling table', ['flat membrane panel','folded high-area membrane panel','exchange-flow indicators'],'U2-K-025',['U2-K-025'],'STRUCTURE_ADAPTATION_SCENE'),
('U2-L21','U2-J3','U2-B06','Organism Scaling Terrace','the outdoor thermal terrace with small and large organism models', ['small-organism heat/metabolism display','size-comparison scale','large-organism heat/metabolism display'],'U2-K-026',['U2-K-026','U2-K-027'],'SCALE_COMPARISON_SCENE'),

('U2-L22','U2-J4','U2-B07','Phospholipid Bilayer Gate','the magnified bilayer turnstile at the terminal entrance', ['aqueous exterior with hydrophilic heads','hydrophobic tail-to-tail membrane interior','aqueous interior with hydrophilic heads'],'U2-K-028',['U2-K-028','U2-K-029'],'MOLECULAR_ORIENTATION_SCENE'),
('U2-L23','U2-J4','U2-B07','Fluid Mosaic Concourse','the broad moving membrane floor containing lipids, proteins, and carbohydrate-bearing components', ['mobile lipid region','fluid-mosaic membrane concourse','mobile embedded proteins/components'],'U2-K-032',['U2-K-032','U2-K-033'],'DYNAMIC_MEMBRANE_MODEL'),
('U2-L24','U2-J4','U2-B07','Fluidity Climate Control','the hot/cold membrane-packing demonstration chamber', ['cold unsaturated-tail demonstration','temperature-controlled bilayer model','warm cholesterol-buffer demonstration'],'U2-K-099',['U2-K-099','U2-K-100'],'TEMPERATURE_PACKING_SEQUENCE'),
('U2-L25','U2-J4','U2-B08','Membrane Protein Checkpoint','the protein-placement scanner crossing the membrane floor', ['peripheral surface proteins','integral/transmembrane placement scanner','aqueous-exposed protein regions'],'U2-K-101',['U2-K-030','U2-K-031','U2-K-101','U2-K-102'],'PROTEIN_PLACEMENT_SCENE'),
('U2-L26','U2-J4','U2-B08','Recognition Counter','the membrane-carbohydrate identification desk', ['glycolipid badge rack','cell-recognition counter','glycoprotein badge rack'],'U2-K-104',['U2-K-103','U2-K-104'],'RECOGNITION_INTERACTION_SCENE'),
('U2-L27','U2-J4','U2-B09','Selective Barrier Lane','the hydrophobic-core security lane through the bilayer', ['aqueous approach','hydrophobic membrane interior','aqueous exit'],'U2-K-034',['U2-K-034','U2-K-037'],'SELECTIVE_BARRIER_SCENE'),
('U2-L28','U2-J4','U2-B09','Molecule Passport Lanes','the three neighboring lanes for nonpolar, small polar, and charged/large polar travelers', ['small nonpolar direct-pass lane','small uncharged polar limited-pass lane','protein-required ion/large-polar lane'],'U2-K-035',['U2-K-035','U2-K-036','U2-K-038'],'PERMEABILITY_SORT_SCENE'),
('U2-L29','U2-J4','U2-B09','Plant Wall and Plasmodesmata Exterior','the rigid plant-cell wall outside the plasma membrane with a channel linking the neighboring cell', ['cellulose-rich wall matrix','plasma membrane beneath wall','plasmodesma channel to adjacent cell'],'U2-K-039',['U2-K-039','U2-K-105','U2-K-106','U2-K-107'],'BOUNDARY_AND_CHANNEL_SCENE'),

('U2-L30','U2-J5','U2-B10','Concentration Ramp','the sloped particle platform running from crowded to sparse regions', ['high-concentration platform','random molecular motion ramp','low-concentration platform'],'U2-K-108',['U2-K-040','U2-K-108','U2-K-041'],'PARTICLE_MOTION_SEQUENCE'),
('U2-L31','U2-J5','U2-B10','Active Transport Lift','the powered lift carrying cargo against the concentration slope', ['low-concentration loading bay','ATP-powered transport-protein lift','high-concentration unloading bay'],'U2-K-042',['U2-K-042','U2-K-058','U2-K-059'],'ENERGY_COUPLED_TRANSPORT_SCENE'),
('U2-L32','U2-J5','U2-B10','Facilitated Diffusion Corridor','the no-ATP protein-assisted downhill corridor', ['high-concentration cargo','transport-protein corridor','low-concentration destination'],'U2-K-046',['U2-K-046','U2-K-049'],'PROTEIN_ASSISTED_DOWNHILL_SCENE'),
('U2-L33','U2-J5','U2-B10','Channel Turnstiles','the gated hydrophilic pores crossing the membrane wall', ['ions waiting outside','channel-protein pore/gate','charge-separation indicator'],'U2-K-110',['U2-K-047','U2-K-110','U2-K-048'],'GATED_CHANNEL_SEQUENCE'),
('U2-L34','U2-J5','U2-B10','Carrier Shuttle','the binding-and-conformation shuttle in the membrane wall', ['solute binding site','carrier conformation chamber','solute release side'],'U2-K-111',['U2-K-111'],'CARRIER_CONFORMATION_SEQUENCE'),
('U2-L35','U2-J5','U2-B10','Aquaporin Floodgate','the water-only channel bank beside the carrier shuttle', ['bulk water reservoir','aquaporin channel bank','receiving water reservoir'],'U2-K-050',['U2-K-050'],'WATER_CHANNEL_SEQUENCE'),
('U2-L36','U2-J5','U2-B11','Bulk Cargo Dock','the membrane-remodeling loading dock for vesicles', ['membrane invagination area','vesicle cargo dock','vesicle-fusion release area'],'U2-K-044',['U2-K-043','U2-K-044','U2-K-045'],'VESICLE_BEFORE_AFTER_SEQUENCE'),
('U2-L37','U2-J5','U2-B11','Endocytosis Intake Bays','the three adjacent intake bays for particles, fluid, and receptor-selected cargo', ['phagocytosis bay','pinocytosis bay','receptor-mediated endocytosis bay'],'U2-K-118',['U2-K-118','U2-K-119','U2-K-120'],'ENDOCYTOSIS_SUBTYPE_COMPARISON'),
('U2-L38','U2-J5','U2-B12','Electrical Pump Control','the charged-membrane control board centered on the Na+/K+ ATPase', ['Na+ export side','ATPase/electrogenic pump and voltage meter','K+ import side'],'U2-K-112',['U2-K-060','U2-K-112','U2-K-113','U2-K-114'],'ELECTROCHEMICAL_PUMP_SEQUENCE'),
('U2-L39','U2-J5','U2-B12','Proton Cotransport Platform','the H+ gradient platform feeding a coupled sucrose transporter', ['ATP-powered proton pump','H+ electrochemical-gradient reservoir','H+/sucrose cotransporter'],'U2-K-116',['U2-K-115','U2-K-116','U2-K-117'],'GRADIENT_COUPLING_SEQUENCE'),

('U2-L40','U2-J6','U2-B13','Tonicity Orientation Hall','the central comparison tank with three external-solution doors', ['hypotonic door','cell reference tank','hypertonic/isotonic comparison doors'],'U2-K-121',['U2-K-051','U2-K-121'],'RELATIVE_SOLUTION_COMPARISON'),
('U2-L41','U2-J6','U2-B13','Isotonic Balance Pool','the transparent cell chamber showing equal opposing water movement', ['water entering','cell in isotonic solution','water leaving'],'U2-K-122',['U2-K-122'],'DYNAMIC_EQUILIBRIUM_SCENE'),
('U2-L42','U2-J6','U2-B13','Hypertonic Withdrawal Chamber','the high-solute external chamber that draws water from cells', ['hypertonic external solution','shrinking animal-cell model','water-flow path outward'],'U2-K-123',['U2-K-123'],'SHRINKAGE_SEQUENCE'),
('U2-L43','U2-J6','U2-B13','Hypotonic Plant Greenhouse','the low-solute chamber containing paired animal and plant cells', ['swelling animal-cell model','turgid plant-cell model against wall','plasmolyzed-versus-turgid comparison panel'],'U2-K-124',['U2-K-124','U2-K-125','U2-K-126'],'SWELLING_TURGOR_SEQUENCE'),
('U2-L44','U2-J6','U2-B14','Osmosis and Water-Potential River','the channel connecting two compartments with a selectively permeable divider', ['higher-water-potential compartment','selectively permeable divider/osmosis path','lower-water-potential compartment'],'U2-K-109',['U2-K-052','U2-K-056','U2-K-109','U2-K-054'],'WATER_POTENTIAL_FLOW_SCENE'),
('U2-L45','U2-J6','U2-B14','Water-Potential Control Room','the pressure-and-solute control console above the river', ['pressure-potential control','Ψ = Ψp + Ψs and Ψs = −iCRT console','solute-potential/osmoregulation control'],'U2-K-055',['U2-K-053','U2-K-057','U2-K-127','U2-K-128','U2-K-055'],'QUANTITATIVE_CONTROL_MODEL'),

('U2-L46','U2-J7','U2-B15','Compartmentalization Lab','the divided reaction chamber with separate enzyme stations and expanded internal membranes', ['reaction compartment A','internal membrane/surface-area divider','reaction compartment B'],'U2-K-061',['U2-K-061','U2-K-062','U2-K-063'],'COMPARTMENT_CAUSAL_MODEL'),
('U2-L47','U2-J7','U2-B15','Internal Organization Comparison Room','the side-by-side prokaryotic and eukaryotic organization models', ['prokaryotic specialized regions','comparison table','eukaryotic membrane-bound compartments'],'U2-K-065',['U2-K-065','U2-K-066'],'COMPARISON_SCENE'),
('U2-L48','U2-J7','U2-B16','Endosymbiosis Origin Theater','the staged engulfment model showing a host cell retaining a formerly free-living prokaryote', ['ancestral host cell','engulfment/retention stage','integrated descendant organelle'],'U2-K-064',['U2-K-064'],'ORIGIN_SEQUENCE'),
('U2-L49','U2-J7','U2-B16','Endosymbiotic Evidence Vault','the four-panel evidence wall with a modern-dependence exit panel', ['genome/division evidence','ribosome/membrane evidence','modern host-dependence panel'],'U2-K-129',['U2-K-129','U2-K-130','U2-K-131','U2-K-132','U2-K-133'],'EVIDENCE_MATRIX'),
]

loci=[]
for lid,jid,bid,title,anchor,zones,primary,kids,visual in raw_loci:
    loci.append({
      'locus_id':lid,'journey_id':jid,'bundle_id':bid,'title':title,
      'micro_anchor':anchor,
      'scene_geometry':{'left':zones[0],'center':zones[1],'right':zones[2]},
      'primary_knowledge_id':primary,
      'knowledge_ids':kids,
      'embedded_knowledge_ids':[k for k in kids if k!=primary],
      'visual_mode':visual,
      'scientific_visual_required':True,
      'narrative_status':'ARCHITECTURE_ONLY_NO_STORY_PROSE_F2'
    })

practice_ids=[f'U2-K-{i:03d}' for i in range(134,143)]
practice=[
 {'challenge_id':'U2-CH-01','knowledge_id':'U2-K-134','title':'Albumin organelle inference','type':'STRUCTURE_FUNCTION_FRQ','prerequisite_loci':['U2-L06','U2-L08','U2-L09']},
 {'challenge_id':'U2-CH-02','knowledge_id':'U2-K-135','title':'Insulin secretory pathway','type':'PATHWAY_FRQ','prerequisite_loci':['U2-L04','U2-L06','U2-L08','U2-L09','U2-L36']},
 {'challenge_id':'U2-CH-03','knowledge_id':'U2-K-136','title':'Alcohol detoxification and autophagy','type':'STRUCTURE_FUNCTION_FRQ','prerequisite_loci':['U2-L07','U2-L10']},
 {'challenge_id':'U2-CH-04','knowledge_id':'U2-K-137','title':'Surface-area-to-volume calculations','type':'QUANTITATIVE','prerequisite_loci':['U2-L19','U2-L20']},
 {'challenge_id':'U2-CH-05','knowledge_id':'U2-K-138','title':'Cold-water fish membrane fluidity','type':'MECHANISM_FRQ','prerequisite_loci':['U2-L23','U2-L24']},
 {'challenge_id':'U2-CH-06','knowledge_id':'U2-K-139','title':'Diffusion diagrams','type':'MODEL_INTERPRETATION','prerequisite_loci':['U2-L27','U2-L28','U2-L30']},
 {'challenge_id':'U2-CH-07','knowledge_id':'U2-K-140','title':'Sucrose uptake versus pH','type':'DATA_MECHANISM_FRQ','prerequisite_loci':['U2-L38','U2-L39']},
 {'challenge_id':'U2-CH-08','knowledge_id':'U2-K-141','title':'Macrophage phagocytosis','type':'PROCESS_FRQ','prerequisite_loci':['U2-L26','U2-L37']},
 {'challenge_id':'U2-CH-09','knowledge_id':'U2-K-142','title':'Water-potential calculations','type':'QUANTITATIVE','prerequisite_loci':['U2-L44','U2-L45']},
]

# Name-support is adaptive. It never blocks first exposure and never creates an extra visible student step.
high_name_terms={
'U2-K-004','U2-K-014','U2-K-071','U2-K-072','U2-K-075','U2-K-079','U2-K-080','U2-K-081','U2-K-083','U2-K-086','U2-K-088','U2-K-089','U2-K-090','U2-K-092','U2-K-093','U2-K-094','U2-K-095','U2-K-096','U2-K-107','U2-K-113','U2-K-116','U2-K-117','U2-K-118','U2-K-119','U2-K-120','U2-K-125','U2-K-129','U2-K-130','U2-K-131','U2-K-132'
}
medium_name_terms={
'U2-K-007','U2-K-008','U2-K-009','U2-K-016','U2-K-019','U2-K-050','U2-K-051','U2-K-052','U2-K-055','U2-K-064','U2-K-068','U2-K-069','U2-K-073','U2-K-074','U2-K-077','U2-K-078','U2-K-084','U2-K-085','U2-K-091','U2-K-099','U2-K-100','U2-K-101','U2-K-102','U2-K-103','U2-K-104','U2-K-109','U2-K-112','U2-K-114','U2-K-121','U2-K-122','U2-K-123','U2-K-124','U2-K-126','U2-K-127','U2-K-128'
}

loc_for={kid:l['locus_id'] for l in loci for kid in l['knowledge_ids']}
primary_set={l['primary_knowledge_id'] for l in loci}
classification=[]
for kid,r in records.items():
    if kid in practice_ids:
        dest='CHALLENGE_LAB'
        locus=None
        role='APPLIED_TRANSFER'
        visual='APPLICATION_PROMPT'
    else:
        locus=loc_for[kid]
        dest='PALACE_PRIMARY_LOCUS' if kid in primary_set else 'PALACE_EMBEDDED'
        role='PRIMARY_ANCHOR' if kid in primary_set else 'EMBEDDED_SCIENCE'
        visual=next(l['visual_mode'] for l in loci if l['locus_id']==locus)
    if not r['exact_name_recall']:
        ns='NO_EXACT_NAME_GATE'
    elif kid in high_name_terms:
        ns='PHONOLOGICAL_SUPPORT_RECOMMENDED_IF_NEEDED'
    elif kid in medium_name_terms:
        ns='SEMANTIC_PLUS_OPTIONAL_SOUND_CUE'
    else:
        ns='SEMANTIC_SCIENCE_CUE_SUFFICIENT'
    retrieval=[]
    if r['exact_name_recall']:
        retrieval.append('EXACT_NAME_FROM_SCIENTIFIC_ROLE')
    retrieval.append('MEANING_OR_MECHANISM')
    if dest=='CHALLENGE_LAB': retrieval=['APPLIED_TRANSFER']
    if kid in {'U2-K-097','U2-K-098','U2-K-053','U2-K-057','U2-K-114'}:
        retrieval.append('FORMULA_OR_STOICHIOMETRY_RECALL')
    classification.append({
      'knowledge_id':kid,'canonical_label':r['canonical_label'],'topic':r['topic'],'scope_class':r['scope_class'],
      'destination':dest,'locus_id':locus,'scene_role':role,'visual_mode':visual,
      'exact_name_recall':r['exact_name_recall'],'name_support':ns,
      'spelling_policy':'ADAPTIVE_SUPPORT_ONLY_NO_MANDATORY_SPELLING_GATE',
      'retrieval_modes':retrieval,
      'canonical_lock':r['canonical_lock'], 'review_flag_id':r.get('review_flag_id')
    })

confusables=[
 {'set_id':'U2-CF-01','title':'Cell organization','terms':['prokaryotic cell','eukaryotic cell'],'knowledge_ids':['U2-K-068','U2-K-069']},
 {'set_id':'U2-CF-02','title':'Ribosome location and destination','terms':['free ribosomes','bound ribosomes'],'knowledge_ids':['U2-K-073','U2-K-074']},
 {'set_id':'U2-CF-03','title':'ER identity','terms':['rough ER','smooth ER'],'knowledge_ids':['U2-K-007','U2-K-008']},
 {'set_id':'U2-CF-04','title':'Golgi directionality','terms':['cis face','trans face'],'knowledge_ids':['U2-K-077','U2-K-078']},
 {'set_id':'U2-CF-05','title':'Digestive versus oxidative organelles','terms':['lysosome','peroxisome'],'knowledge_ids':['U2-K-014','U2-K-081']},
 {'set_id':'U2-CF-06','title':'Cytoskeletal elements','terms':['microtubule','microfilament / actin filament','intermediate filament'],'knowledge_ids':['U2-K-093','U2-K-095','U2-K-096']},
 {'set_id':'U2-CF-07','title':'Chloroplast internal structures','terms':['thylakoid','granum','stroma'],'knowledge_ids':['U2-K-088','U2-K-089','U2-K-090']},
 {'set_id':'U2-CF-08','title':'Membrane protein placement','terms':['integral membrane protein','peripheral membrane protein','transmembrane protein'],'knowledge_ids':['U2-K-101','U2-K-102']},
 {'set_id':'U2-CF-09','title':'Membrane carbohydrate labels','terms':['glycolipid','glycoprotein'],'knowledge_ids':['U2-K-103','U2-K-104']},
 {'set_id':'U2-CF-10','title':'Transport energy and mechanism','terms':['passive transport','facilitated diffusion','active transport'],'knowledge_ids':['U2-K-041','U2-K-046','U2-K-042']},
 {'set_id':'U2-CF-11','title':'Protein-mediated membrane routes','terms':['channel protein','carrier protein','aquaporin'],'knowledge_ids':['U2-K-110','U2-K-111','U2-K-050']},
 {'set_id':'U2-CF-12','title':'Bulk transport direction','terms':['endocytosis','exocytosis'],'knowledge_ids':['U2-K-044','U2-K-045']},
 {'set_id':'U2-CF-13','title':'Endocytosis subtypes','terms':['phagocytosis','pinocytosis','receptor-mediated endocytosis'],'knowledge_ids':['U2-K-118','U2-K-119','U2-K-120']},
 {'set_id':'U2-CF-14','title':'Tonicity','terms':['hypotonic','isotonic','hypertonic'],'knowledge_ids':['U2-K-124','U2-K-122','U2-K-123']},
 {'set_id':'U2-CF-15','title':'Water-potential components','terms':['water potential','pressure potential','solute potential'],'knowledge_ids':['U2-K-053','U2-K-127','U2-K-128']},
 {'set_id':'U2-CF-16','title':'Electrochemical transport','terms':['electrogenic pump','Na+/K+ ATPase','proton pump','cotransport'],'knowledge_ids':['U2-K-113','U2-K-114','U2-K-115','U2-K-116']},
 {'set_id':'U2-CF-17','title':'Energy organelles','terms':['mitochondrion','chloroplast'],'knowledge_ids':['U2-K-012','U2-K-020']},
]

architecture={
 'schema':'memory-palace-v2-unit2-f2-architecture-1.0','generated_utc':'2026-09-02T06:15:00+00:00',
 'unit':{'unit_id':'unit-2','title':'Cells','canonical_source_lock':'F1','student_release':False,'narrative_generation_allowed':False},
 'design_rules':{
   'student_simplicity':'The learner will eventually see guided journeys and short review, not classification machinery.',
   'locus_rule':'A permanent locus is used for a distinct spatial or causal concept cluster, not for every canonical record.',
   'embedded_rule':'Closely related structure/function details share the locus that makes their relationship visible.',
   'practice_rule':'Applied-transfer records remain in Challenge Lab and do not consume palace loci.',
   'narrative_gate':'No story prose may be written until this F2 architecture passes QA and is explicitly locked.',
   'visual_rule':'Conventional scientific geometry must remain recognizable even when narrative imagery is added later.',
   'spelling_rule':'No mandatory spelling gauntlet; spelling support is adaptive and only appears when useful.'
 },
 'counts':{'canonical_records':len(records),'palace_managed_records':len(records)-len(practice_ids),'practice_only_records':len(practice_ids),'journeys':len(journeys),'bundles':sum(len(j['bundles']) for j in journeys),'permanent_loci':len(loci),'confusable_sets':len(confusables)},
 'journeys':journeys,'loci':loci,'challenge_lab':practice,'confusable_sets':confusables
}

classdoc={
 'schema':'memory-palace-v2-unit2-f2-classification-1.0','generated_utc':architecture['generated_utc'],
 'unit_id':'unit-2','canonical_source_lock':'F1','counts':{},'records':classification
}
from collections import Counter
classdoc['counts']={
 'total':len(classification),
 'by_destination':dict(Counter(x['destination'] for x in classification)),
 'by_name_support':dict(Counter(x['name_support'] for x in classification)),
 'exact_name_targets':sum(bool(x['exact_name_recall']) for x in classification),
 'mandatory_spelling_targets':0
}

dump(ARCH/'learning-classification-f2.json',classdoc)
dump(ARCH/'palace-architecture-f2.json',architecture)

# update status and course registry
status=load(U2/'status.json')
status.update({
 'status':'LEARNING_ARCHITECTURE_LOCKED_F2_NOT_STUDENT_RELEASED',
 'pipeline_stage':'LEARNING_CLASSIFICATION_AND_PALACE_ARCHITECTURE_COMPLETE',
 'architecture_lock':'LOCKED_F2',
 'student_release':False,
 'journey_blueprints':len(journeys),'bundle_blueprints':sum(len(j['bundles']) for j in journeys),'permanent_locus_blueprints':len(loci),
 'palace_managed_records':len(records)-len(practice_ids),'practice_only_records':len(practice_ids),'confusable_sets':len(confusables),
 'next_required_output':'F3 narrative briefs and scene-by-scene science-bearing action specifications; no polished story prose before brief QA'
})
dump(U2/'status.json',status)
course=load(ROOT/'content'/'ap-biology'/'course.json')
for u in course['units']:
 if u['unit_id']=='unit-2':
  u.update({'status':status['status'],'journey_count':0,'scene_count':0,'canonical_lock':'LOCKED_F1','canonical_records':142,'review_flags_resolved':20,'architecture_journeys':len(journeys),'architecture_loci':len(loci),'architecture_lock':'LOCKED_F2','source_status':'AUDITED_SCIENCE_LOCKED_F1_AND_ARCHITECTURE_LOCKED_F2'})
dump(ROOT/'content'/'ap-biology'/'course.json',course)

# release manifest, content lock
manifest={
 'schema':'memory-palace-v2-unit2-f2-release-1.0','generated_utc':architecture['generated_utc'],'unit_id':'unit-2','release':'F2_LEARNING_ARCHITECTURE_LOCK',
 'student_release':False,'canonical_records':len(records),'palace_managed_records':133,'challenge_lab_records':9,'journey_blueprints':7,'bundle_blueprints':16,'permanent_locus_blueprints':49,'confusable_sets':17,
 'narrative_story_files':0,'student_runtime_memory_objects':0,
 'gate':'F2 fixes learning destinations and spatial architecture. F3 may specify science-bearing scene actions, but polished narrative prose remains gated until F3 brief QA.'
}
dump(U2/'f2-release-manifest.json',manifest)

locked=[
 'content/ap-biology/unit-2/source/canonical-unit2-f1.json',
 'content/ap-biology/unit-2/source/coverage-manifest-f1.json',
 'content/ap-biology/unit-2/architecture/learning-classification-f2.json',
 'content/ap-biology/unit-2/architecture/palace-architecture-f2.json',
 'content/ap-biology/unit-2/status.json',
 'content/ap-biology/unit-2/f2-release-manifest.json',
]
lock={'schema':'memory-palace-v2-unit2-f2-lock-1.0','lock_status':'LOCKED_F2','student_release':False,'files':{}}
for rel in locked:
 p=ROOT/rel
 lock['files'][rel]={'sha256':sha(p),'bytes':p.stat().st_size}
dump(U2/'content-lock-f2.json',lock)
print('built F2',architecture['counts'],classdoc['counts'])
