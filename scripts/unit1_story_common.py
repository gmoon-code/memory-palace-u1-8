from __future__ import annotations
import json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
UNIT=ROOT/'content'/'ap-biology'/'unit-1'
MEM=json.loads((UNIT/'memory-objects.json').read_text(encoding='utf-8'))['memory_objects']
SOURCE=json.loads((UNIT/'source'/'guided-journeys.json').read_text(encoding='utf-8'))['guided_journeys']
OBJ={o['memory_object_id']:o for o in MEM}
SOURCE_J={j['palace_id']:j for j in SOURCE}

# Student-facing definitions should sound like biology, not provenance notes.
OVERRIDES={
 'MO-APBIO-U1-C014':'Across the main-group region commonly emphasized in introductory biology, electronegativity generally increases from left to right across a period and decreases down a group.',
 'MO-APBIO-U1-C022':'In liquid water, hydrogen bonds continually form, break, and reform as water molecules move.',
 'MO-APBIO-U1-C025':'Sulfur occurs in some amino acids, including cysteine and methionine, so sulfur is present in some proteins but not every protein.',
 'MO-APBIO-U1-C026':'Phosphorus is part of the phosphate groups in nucleic acids and the phosphate-containing head regions of phospholipids.',
 'MO-APBIO-U1-C027':'Nitrogen occurs in the nitrogenous bases of nucleic acids.',
 'MO-APBIO-U1-C028':'Nitrogen is present in the amino groups and peptide backbones of proteins because amino acids contain nitrogen.',
 'MO-APBIO-U1-CA010':'Recognize hydroxyl, carbonyl, carboxyl, amino, phosphate, sulfhydryl, and methyl groups and connect each group with how it changes the molecule that carries it.',
 'MO-APBIO-U1-PA001':'Carbohydrates, proteins, nucleic acids, and lipids are four major classes of large biological molecules. Carbohydrates, proteins, and nucleic acids include polymers; lipids do not form true polymers.',
 'MO-APBIO-U1-PA007':'Compare the four major macromolecule classes by their building units, covalent connections, elements, structures, and biological roles.',
 'MO-APBIO-U1-CG001':'Carbohydrates contain carbon, hydrogen, and oxygen and commonly include carbonyl and multiple hydroxyl groups.',
 'MO-APBIO-U1-CG004':'Glucose is a common monosaccharide that cells can use as fuel, including during cellular respiration.',
 'MO-APBIO-U1-CG005':'Monosaccharides can be used as building blocks for larger carbohydrates and can also contribute carbon skeletons used to build other molecules.',
 'MO-APBIO-U1-CG007':'Sucrose is a disaccharide made from glucose and fructose and is an important transport sugar in plants.',
 'MO-APBIO-U1-CG012':'Chitin is a structural polysaccharide found in arthropod exoskeletons and in fungal cell walls.',
 'MO-APBIO-U1-CG013':'A glycosidic linkage is a covalent bond that joins monosaccharides. In common 1→4 linkages, carbon 1 of one glucose connects to carbon 4 of the next.',
 'MO-APBIO-U1-CG014':'Alpha and beta glucose differ in the orientation of the hydroxyl group attached to carbon 1 in the ring form, a difference that contributes to different carbohydrate structures.',
 'MO-APBIO-U1-CG015':'Starch uses alpha-glucose linkages and can form coiled or branched storage structures. Cellulose uses beta-glucose linkages, forming straight unbranched chains that align into strong fibers.',
 'MO-APBIO-U1-PF002':'The common amino-acid backbone contains carbon, hydrogen, oxygen, and nitrogen. Sulfur occurs in some amino acids and therefore in some proteins.',
 'MO-APBIO-U1-PF003':'An amino acid has a central carbon bonded to a hydrogen atom, an amino group, a carboxyl group, and a variable R group. The R group differs among amino acids and helps determine their chemical properties.',
 'MO-APBIO-U1-PF004':'Proteins are built from a standard set of 20 amino acids.',
 'MO-APBIO-U1-PF009':'A peptide bond is the covalent bond that links amino acids, forming between the carboxyl group of one amino acid and the amino group of the next.',
 'MO-APBIO-U1-PF010':'Peptide-bond formation is a dehydration reaction: the covalent link forms while components equivalent to water are removed.',
 'MO-APBIO-U1-PF012':'A polypeptide has directionality, with a chemically distinct N-terminus and C-terminus.',
 'MO-APBIO-U1-PF013':'A protein’s amino-acid sequence determines its primary structure and strongly influences how the chain folds into its final shape.',
 'MO-APBIO-U1-PF014':'Interactions among amino-acid R groups help drive and stabilize protein folding.',
 'MO-APBIO-U1-PF015':'Gene information specifies the amino-acid sequence of a polypeptide.',
 'MO-APBIO-U1-PF017':'Primary structure is the linear order of amino acids in a polypeptide. That sequence influences every higher level of folding.',
 'MO-APBIO-U1-PF018':'Secondary structure consists of local folds of the polypeptide backbone stabilized by hydrogen bonds, especially alpha helices and beta-pleated sheets.',
 'MO-APBIO-U1-PF022':'Tertiary structure is stabilized by side-chain interactions including hydrophobic interactions, van der Waals interactions, hydrogen bonds, ionic interactions, and covalent disulfide bridges.',
 'MO-APBIO-U1-PF028':'Protein denaturation is the loss of a protein’s native three-dimensional structure when conditions disrupt the interactions that stabilize it, often causing loss of function.',
 'MO-APBIO-U1-NA003':'A nucleotide consists of a nitrogenous base, a five-carbon sugar, and phosphate. In a nucleic-acid strand, each incorporated nucleotide contributes one phosphate to the sugar-phosphate backbone.',
 'MO-APBIO-U1-NA004':'Within a nucleic-acid strand, phosphate groups connect adjacent nucleotide units as part of the sugar-phosphate backbone.',
 'MO-APBIO-U1-NA005':'Cytosine, thymine, and uracil are pyrimidines, nitrogenous bases with a single-ring framework.',
 'MO-APBIO-U1-NA006':'Adenine and guanine are purines, nitrogenous bases with a two-ring framework.',
 'MO-APBIO-U1-NA011':'A nucleoside is a nitrogenous base joined to a sugar without a phosphate group.',
 'MO-APBIO-U1-NA012':'The 5′ end of a nucleic-acid strand is associated with the phosphate attached to the sugar’s 5′ carbon.',
 'MO-APBIO-U1-NA014':'A phosphodiester linkage is the covalent connection that joins adjacent nucleotides through the sugar-phosphate backbone.',
 'MO-APBIO-U1-NA017':'Biological information is encoded in the linear sequence of nucleotides. In genes, nucleotide sequence ultimately specifies amino-acid sequence and can therefore affect protein structure.',
 'MO-APBIO-U1-LIP002':'Major lipid types emphasized here include fats, phospholipids, and steroids; cholesterol is a steroid lipid.',
 'MO-APBIO-U1-LIP003':'A fat consists of glycerol joined to three fatty acids.',
 'MO-APBIO-U1-LIP004':'Glycerol is a three-carbon alcohol with hydroxyl groups that can connect to fatty acids.',
 'MO-APBIO-U1-LIP005':'A fatty acid has a long hydrocarbon chain with a carboxyl group at one end.',
 'MO-APBIO-U1-LIP006':'In fats, fatty acids are covalently joined to glycerol by ester linkages formed through dehydration reactions.',
 'MO-APBIO-U1-LIP007':'A saturated fatty acid has no carbon-carbon double bonds in its hydrocarbon chain.',
 'MO-APBIO-U1-LIP012':'Fats provide long-term energy storage. Adipose tissue can also cushion organs and subcutaneous fat can provide thermal insulation.',
 'MO-APBIO-U1-LIP013':'A phospholipid has glycerol connected to two fatty acids and a phosphate-containing head region.',
 'MO-APBIO-U1-LIP014':'A phospholipid has a hydrophilic head that interacts with water and hydrophobic fatty-acid tails that avoid water.',
 'MO-APBIO-U1-LIP016':'A steroid has a characteristic framework of four fused carbon rings; different attached groups produce different steroid molecules.',
 'MO-APBIO-U1-LIP017':'Testosterone is one example of a steroid hormone.',
}

META_PATTERNS=[
 r'\bPPT\s+(?:states|describes|identifies|classifies|emphasizes|connects|shows|represents|prompts students to)\s+(?:that\s+)?',
 r'\bThe current CED\s+(?:explicitly\s+)?(?:requires|excludes|frames)\s+',
 r'\b(?:The\s+)?CED\s+(?:explicitly\s+)?(?:requires|notes|links|includes|specifies|states|describes)\s+(?:that\s+)?',
 r'\bCampbell\s+(?:uses|groups)\s+',
 r'\bIn the packet(?:\'s)?\s+[^,]+,\s*',
 r'\bteacher-enrichment\b',r'\bteacher-supporting material\b',r'\bAP-required\b',r'\bAP Exam\b',
]

def student_science(o):
    oid=o['memory_object_id']
    if oid in OVERRIDES:return OVERRIDES[oid]
    s=str(o.get('canonical_definition') or '').strip()
    for pat in META_PATTERNS:s=re.sub(pat,'',s,flags=re.I)
    s=re.sub(r'\s+',' ',s).strip()
    s=s.replace('Exact drawing requirements are enrichment unless separately required.','')
    s=s.replace('This exact structural detail is enrichment because specific carbohydrate-polymer molecular structures are outside current exam scope.','')
    s=s.replace('Exact lipid molecular structures are not required structural memorization.','')
    s=re.sub(r'\s+',' ',s).strip(' ;')
    return s

def old_scene(palace_id,locus):
    for s in SOURCE_J[palace_id]['scenes']:
        if s['locus']==locus:return s
    raise KeyError((palace_id,locus))

def guide_cast(guide):
    return {'name':guide['name'],'kind':'guide','visual':guide['visual'],'job':guide['story_job']}

def memory_items(object_ids, image_by_id=None):
    image_by_id=image_by_id or {}
    out=[]
    for oid in object_ids:
        o=OBJ[oid]
        out.append({'term':o['canonical_term'],'meaning':student_science(o),'image':image_by_id.get(oid) or default_image(o)})
    return out

def default_image(o):
    hint=str(o.get('mnemonic_actor_or_object') or o.get('phonological_keyword') or o.get('scene_action') or '').strip()
    if hint:
        hint=re.sub(r'\bPPT\b','',hint,flags=re.I)
        return re.sub(r'\s+',' ',hint).strip(' .')
    return f"the {o['canonical_term']} action you just watched in the scene"

def story_beats(object_ids, image_by_id=None):
    image_by_id=image_by_id or {}
    beats=[]
    for oid in object_ids:
        o=OBJ[oid]
        beats.append({'object_id':oid,'term':o['canonical_term'],'story':image_by_id.get(oid) or default_image(o),'science':student_science(o),'exact_name':str(o.get('exact_name_required','')).upper()=='YES','hint':image_by_id.get(oid) or default_image(o)})
    return beats

def _narrative_word_count(paragraphs):
    return len(re.findall(r"\b[\w’'-]+\b", ' '.join(paragraphs)))

def _spatial_entry(meta, spec, idx):
    """Create a short story-facing orientation paragraph from already-approved scene geometry.

    This adds no scientific claims. It exists so a learner can place themself in the room before
    the scientific action begins. Templates vary by palace to avoid a mechanical repeated voice.
    """
    zones=spec.get('zones',[])
    if len(zones)!=3:
        return ''
    left,center,right=zones
    guide=meta['guide']['name']
    locus=spec['locus']
    desc=spec['location_description'].rstrip('.')
    variants={
      'Z1':f"You follow {guide} into **{locus}** and the lab door seals behind you. {desc}. On your left is the {left['label']}; straight ahead is the {center['label']}; on your right is the {right['label']}. The arrangement is deliberate: you can keep the evidence, the action, and the comparison in separate places while the investigation unfolds.",
      'Z2':f"The next museum door clicks open and {guide} ushers you into **{locus}**. {desc}. Your left is anchored by the {left['label']}, the {center['label']} sits directly in front of you, and the {right['label']} fixes the far side of the gallery. The escaped carbon token is already moving through that layout, so your eyes have a route to follow before the exhibit wakes up.",
      'Z4':f"You enter **{locus}** with the same carbon frame still in view. {desc}. The {left['label']} is on your left, the {center['label']} is directly ahead, and the {right['label']} holds the opposite side of the room. The workshop is arranged so every change to carbon happens in a place you can mentally return to.",
      'Z5':f"A conveyor alarm pulls you and {guide} into **{locus}**. {desc}. The {left['label']} occupies your left, the {center['label']} is directly ahead on the line, and the {right['label']} waits on your right. The same molecular pieces stay on the belt, so you can watch exactly what changes as the assembly line moves them forward.",
      'Z6':f"The greenhouse path bends into **{locus}**. {desc}. To your left is the {left['label']}; directly ahead, the {center['label']}; to your right, the {right['label']}. Warm glass, hanging vines, and the same sugar cargo keep the scene connected as {guide} leads you toward the next structure.",
      'Z7':f"{guide} wheels the same developing polypeptide into **{locus}**. {desc}. The {left['label']} stays on your left, the {center['label']} is the main work area straight ahead, and the {right['label']} fixes your right side. Because the chain never disappears between rooms, every new fold or bond has a visible before-and-after state.",
      'Z8':f"{guide} carries the damaged genetic manuscript into **{locus}**. {desc}. The {left['label']} is on your left, the {center['label']} is directly ahead, and the {right['label']} marks the other side of the archive. The same strip of nucleic acid remains in your hands, so each repair changes one identifiable part of the manuscript.",
      'Z9':f"{guide}'s membrane tablet flashes and guides you into **{locus}**. {desc}. The {left['label']} is on your left, the {center['label']} is straight ahead, and the {right['label']} is on your right. The repair problem stays visible on the tablet while the room isolates one lipid feature at a time.",
    }
    return variants.get(meta['palace_id'],f"You enter **{locus}**. {desc}. The {left['label']} is on your left, the {center['label']} is ahead, and the {right['label']} is on your right.")

def enrich_paragraphs(meta, spec, paragraphs, idx):
    paragraphs=list(paragraphs)
    # Water's hand-written benchmark is not built through this function. For other palaces,
    # only short scenes receive an added orientation beat so pacing remains compact.
    if _narrative_word_count(paragraphs) < 130:
        opening=_spatial_entry(meta,spec,idx)
        if opening:
            paragraphs.insert(0,opening)
    return paragraphs

EXACT_TERM_BRIDGES={
 'MO-APBIO-U1-P031':"Rowan physically separates the two ideas on the bench. The comparison is **constants versus controls**: constants are conditions kept the same across groups, while a control group is the comparison condition used to evaluate the independent variable. They solve different experimental-design problems.",
 'MO-APBIO-U1-P014':"The small dials are the **controlled variables / constants**. Temperature, light, time, and cell number stay fixed across the comparison so they do not become competing explanations for the brightness change.",
 'MO-APBIO-U1-P032':"The graph screen turns the panel into **graphing variables**: the independent variable goes on the x-axis and the dependent variable on the y-axis when that convention fits the data, while the graph type still has to match what was measured.",
 'MO-APBIO-U1-P029':"The final display is a lesson in **confidence intervals and error bars**. An uncertainty bar has meaning only after you identify what it represents; overlap or non-overlap of SEM bars by itself is not a formal test of statistical significance.",
 'MO-APBIO-U1-CA010':"The pegboard now becomes a **functional-group recognition** test. Hydroxyl, carbonyl, carboxyl, amino, phosphate, sulfhydryl, and methyl groups keep their recognizable chemical patterns, and each can change how the larger molecule behaves.",
 'MO-APBIO-U1-PA007':"Pip flips the shipping board into a **macromolecule comparison table**. Carbohydrates, proteins, nucleic acids, and lipids can now be compared by building units, covalent connections, elements, structures, and biological roles without pretending that all four are true polymers.",
 'MO-APBIO-U1-CG014':"At the arch, the crucial distinction is **alpha and beta glucose**. The two ring forms differ in the orientation of the hydroxyl group attached to carbon 1, a small directional change that can lead to very different carbohydrate structures.",
 'MO-APBIO-U1-CG018':"The barn wall opens into a four-room model labeled **ruminant stomach compartments**: rumen, reticulum, omasum, and abomasum. Cellulose-digesting microorganisms work mainly in the rumen and reticulum; water is removed in the omasum; the abomasum carries out digestion with the cow's own enzymes.",
 'MO-APBIO-U1-PF026':"Milo holds the raw chain beside the finished folded machine to make **polypeptide versus protein** unmistakable. A polypeptide is the amino-acid chain itself; a functional protein contains one or more polypeptide chains organized into a specific three-dimensional structure.",
 'MO-APBIO-U1-NA002':"Nia places the two manuscript types side by side and names them together: **DNA and RNA**. DNA is deoxyribonucleic acid; RNA is ribonucleic acid. The rest of the archive will show why their structural differences matter.",
 'MO-APBIO-U1-NA025':"The one-way tool demonstrates **nucleotide addition to 3′ end**: each incoming nucleotide is attached at the growing strand's free 3′ end, so synthesis proceeds in the 5′→3′ direction.",
 'MO-APBIO-U1-NA026':"Nia calls the side-by-side cards a **base-pair hydrogen-bond count comparison**. A–T forms two hydrogen bonds and G–C forms three, although that count is only one contributor to overall DNA duplex stability.",
}

def ensure_exact_terms(object_ids, paragraphs):
    paragraphs=list(paragraphs)
    text=' '.join(paragraphs).casefold()
    additions=[]
    for oid in object_ids:
        o=OBJ[oid]
        if str(o.get('exact_name_required','')).upper()!='YES':
            continue
        term=o['canonical_term']
        if term.casefold() in text:
            continue
        bridge=EXACT_TERM_BRIDGES.get(oid)
        if bridge:
            additions.append(bridge)
            text+=' '+bridge.casefold()
    if additions:
        # Put the naming bridge before the transition paragraph so the scene still ends by moving forward.
        if len(paragraphs)>1:
            paragraphs=paragraphs[:-1]+additions+[paragraphs[-1]]
        else:
            paragraphs+=additions
    return paragraphs

def build_journey(meta, scene_specs):
    source=SOURCE_J[meta['palace_id']]
    assert len(scene_specs)==source['scene_count'],(meta['palace_id'],len(scene_specs),source['scene_count'])
    scenes=[]
    checkpoint_indices=set(meta.get('checkpoint_indices',[]))
    for idx,spec in enumerate(scene_specs):
        src=old_scene(meta['palace_id'],spec['locus'])
        object_ids=src['object_ids']
        guide=meta['guide']
        cast=[guide_cast(guide),*spec.get('cast',[])]
        images=spec.get('images',{})
        paragraphs=enrich_paragraphs(meta,spec,spec['paragraphs'],idx)
        paragraphs=ensure_exact_terms(object_ids,paragraphs)
        exacts=[oid for oid in object_ids if str(OBJ[oid].get('exact_name_required','')).upper()=='YES']
        cp_oid=spec.get('checkpoint_object_id') or (exacts[0] if exacts else object_ids[0])
        cp=idx in checkpoint_indices
        cp_prompt=spec.get('checkpoint_prompt') if cp else ''
        if cp and not cp_prompt:
            cp_prompt=f"Without looking back, what term belongs to this image: {images.get(cp_oid) or default_image(OBJ[cp_oid])}?"
        scenes.append({
          'scene_index':idx,'locus':spec['locus'],'title':spec['title'],'scene_kicker':spec['kicker'],
          'location_description':spec['location_description'],
          'scene_layout':{'orientation':spec['orientation'],'zones':spec['zones']},
          'cast':cast,'story_open':paragraphs[0],'story_paragraphs':paragraphs,'story_close':paragraphs[-1],
          'object_ids':object_ids,'story_beats':story_beats(object_ids,images),'memory_snapshot':memory_items(object_ids,images),
          'checkpoint':cp,'checkpoint_object_id':cp_oid,'checkpoint_prompt':cp_prompt,
          'next_locus':scene_specs[idx+1]['locus'] if idx+1<len(scene_specs) else None
        })
    return {
      'palace_id':meta['palace_id'],'palace_name':meta['palace_name'],'story_title':meta['story_title'],'tagline':meta['tagline'],
      'guide':meta['guide'],'premise':meta['premise'],'mission':meta['mission'],'finale':meta['finale'],
      'estimated_minutes':meta['estimated_minutes'],'scene_count':len(scenes),'checkpoint_count':sum(1 for s in scenes if s['checkpoint']),
      'learner_rule':'Read or listen and picture the scene. The important terms are introduced inside the action. Stop only when a Quick Recall appears.',
      'route_orientation':meta['route_orientation'],'route':meta['route'],'scenes':scenes,
      'narrative_design':'V2-NARRATIVE-2.0'
    }

def zone(position,label,symbol,description):return {'position':position,'label':label,'symbol':symbol,'description':description}
def cast(name,kind,visual,job):return {'name':name,'kind':kind,'visual':visual,'job':job}
