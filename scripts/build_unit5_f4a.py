from __future__ import annotations
import json, hashlib, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
U5=ROOT/'content'/'ap-biology'/'unit-5'
F3=json.loads((U5/'briefs'/'scene-briefs-f3.json').read_text(encoding='utf-8'))['scene_briefs']
JBRIEFS=json.loads((U5/'briefs'/'journey-briefs-f3.json').read_text(encoding='utf-8'))['journeys']
J1=next(j for j in JBRIEFS if j['journey_id']=='U5-J1')
B={b['locus_id']:b for b in F3 if b['journey_id']=='U5-J1'}
CANON={r['knowledge_id']:r for r in json.loads((U5/'source'/'canonical-unit5-f1.json').read_text(encoding='utf-8'))['canonical_catalog']}

GUIDE={
 'name':'Dr. Imani Reyes',
 'role':'inheritance-systems geneticist',
 'visual':'deep-green field coat, clear gloves, compact chromosome tablet showing one blue homolog and one amber homolog, and a narrow gold generation ledger',
 'story_job':'Imani keeps chromosome identity, cell type, chromosome-set number, reproductive transition, and generation visible. She changes the biological model first and names the term only after its defining relationship can be seen.'
}

route=[
 {'scene_index':0,'locus':'Heredity Record Desk','short':'Records','floor':'Registry intake','symbol':'▤'},
 {'scene_index':1,'locus':'Homolog Pair Vault','short':'Homologs','floor':'Chromosome vault','symbol':'Ⅱ'},
 {'scene_index':2,'locus':'Ploidy Counter','short':'Ploidy','floor':'Cell registry','symbol':'2n/n'},
 {'scene_index':3,'locus':'Reproduction Fork','short':'Routes','floor':'Transit fork','symbol':'Y'},
 {'scene_index':4,'locus':'Life-Cycle Fusion Loop','short':'Fusion','floor':'Generation rotunda','symbol':'○'},
]

ZONE_COPY={
'U5-L01':[
 ('left','Heredity and genetics record wall','▤','Two vertical files remain fixed on the learner’s left. One tracks what biological information passes across generations, while the other tracks the scientific study of that inheritance and variation.'),
 ('center','Gene-to-chromosome filing rail','━','A full chromosome model crosses the center desk with marked loci. Individual gene records can be clipped to real positions on the chromosome and carried forward with it.'),
 ('right','Conserved information archive','DNA','A glass archive on the right holds DNA/RNA information-system records and a genetic-code display whose shared logic becomes visible only after gene and chromosome identity are settled.')],
'U5-L02':[
 ('left','Homologous chromosome rack','Ⅱ','A blue chromosome and an amber chromosome stand side by side with matching locus positions. Their corresponding genes line up even when the allele labels at those loci differ.'),
 ('center','Homolog-versus-sister comparison bench','X','A replication cradle can copy one chromosome into two joined sister chromatids, making the sister relationship physically different from the homologous pair on the left.'),
 ('right','Karyotype display wall','▦','A conventional chromosome display arranges chromosome images into matched groups using visible features such as size, centromere position, and banding pattern.')],
'U5-L03':[
 ('left','Diploid somatic-cell lane','2n','A body-cell model enters on the left carrying two chromosome sets. The blue and amber homologs remain visible as members of those two sets.'),
 ('center','Chromosome-set counter','2n↔n','A large mechanical counter changes the number of chromosome sets being tracked while preserving the meaning of a chromosome set and the identity of the chromosomes themselves.'),
 ('right','Haploid gamete lane','n','A reproductive-cell model exits on the right carrying one chromosome set and a clear marker showing that it can participate in fertilization.')],
'U5-L04':[
 ('left','Asexual route and clone line','↘','A single genetic source enters the left route without gamete fusion and produces a line of very similar descendants whose records can still accumulate genetic changes over time.'),
 ('center','Reproduction comparison fork','Y','The center floor splits one inheritance ledger into two routes so the presence or absence of meiotic processes and gamete fusion can be compared without changing the meaning of heredity.'),
 ('right','Sexual reproduction route','↗','The right route passes chromosome records through meiotic processes and gamete fusion, generating new combinations of parental alleles without requiring two separate parent organisms in every biological system.')],
'U5-L05':[
 ('left','Haploid gamete entry','n+n','Two haploid gamete models enter from the left with one chromosome set each. Their chromosome identities remain visible as they approach the center chamber.'),
 ('center','Fertilization and zygote fusion chamber','●','The two gamete membranes meet at the center. Their chromosome sets are brought into the same new cell, and the gold ledger changes from two haploid entries to one diploid zygote entry.'),
 ('right','Diploid life-cycle continuation','2n→','The diploid zygote exits toward development and the next generation, while a circular return path keeps the broader life cycle visible without imposing one universal organismal life-cycle pattern.')],
}

BEAT_IMAGES={
'U5-K-035':'the left-hand genetics file that records the scientific investigation of heredity and hereditary variation',
'U5-K-036':'the heredity file whose gold thread visibly continues from one generation record to the next',
'U5-K-037':'the gene card clipped to one exact locus on the center chromosome rail',
'U5-K-038':'the gene card remaining physically attached to its chromosome as that chromosome passes into a descendant record',
'U5-K-064':'the right-side archive lighting the shared DNA/RNA information system and nearly universal genetic-code pattern across many branches of life',
'U5-K-042':'the blue and amber homologous chromosomes aligned by the same gene loci while carrying different allele labels',
'U5-K-043':'one blue chromosome replicated into two joined sister chromatids on the center bench',
'U5-K-044':'the right-side organized chromosome display arranged by chromosome features into a karyotype',
'U5-K-045':'the left-lane non-gamete body cell carrying two homologous chromosome sets',
'U5-K-046':'the center counter reading 2n while two chromosome sets remain visible',
'U5-K-047':'the center counter reading n while one chromosome set remains visible',
'U5-K-048':'the right-lane haploid reproductive cell approaching the later fertilization chamber',
'U5-K-049':'the human count-check panel pairing 46 with a typical somatic cell and 23 with a typical sperm or egg cell',
'U5-K-039':'the left reproduction route beginning from one genetic source and proceeding without gamete fusion',
'U5-K-040':'the line of genetically very similar descendants whose records remain open to later genetic change',
'U5-K-041':'the right reproduction route passing through meiotic processes and gamete fusion to produce new allele combinations',
'U5-K-015':'the two haploid chromosome sets entering one zygote and restoring the diploid state while combining alleles',
'U5-K-052':'the circular generation route carrying reproductive and developmental stages from one generation toward the next',
'U5-K-053':'the central fusion event where two haploid gametes combine chromosome sets',
'U5-K-054':'the new diploid cell that leaves the fusion chamber immediately after gamete fusion',
}

NARR={
'U5-L01':{
 'title':'The Registry With Everything Filed Under One Name',
 'kicker':'The first repair is identity. A gene, a chromosome, heredity, and genetics cannot all mean the same thing.',
 'paragraphs':[
  "The brass doors of the **Heredity and Chromosome Registry** open onto a long intake hall where thousands of family records should move in orderly lines. Tonight, the hall is jammed. On your **left**, two tall cabinets labeled HEREDITY and GENETICS have spilled gold-edged record cards across the floor. Directly **ahead**, a black chromosome model lies across a waist-high filing rail, its numbered loci glowing like precise addresses. On your **right**, a sealed glass archive holds DNA and RNA information records from many kinds of organisms. Nothing is moving. Every loose card on the floor has been stamped with the same word, INHERITANCE, so the registry can no longer tell a field of study from a biological process, or a gene from the chromosome that carries it.",
  "Dr. Imani Reyes kneels beside the center rail in a deep-green field coat. Her compact tablet shows the same blue and amber homologs that will accompany you through the unit. Beside it she opens a narrow gold generation ledger with four columns labeled chromosome set, cell type, reproductive transition, and generation. She refuses to write anything in the ledger yet. First she hands you two different cards from the left cabinet. **Heredity** belongs to the biological transmission of traits and genetic information across generations. **Genetics** belongs to the scientific study of heredity and hereditary variation. She places the heredity card on a gold thread that runs toward a descendant record and leaves the genetics card at the investigation desk. Two words that had occupied the same pile now have different jobs and different places.",
  "A smaller card still lies loose between them. It reads GENE. Imani clips it onto one glowing address on the chromosome rail. The card fits only at that locus. A **gene** is a DNA sequence at a chromosomal locus whose expression or regulatory function can contribute to a functional product or phenotype. Some genes encode proteins, while others function through RNA products or regulation. The rail makes the relationship concrete. The gene is a defined sequence located on the chromosome. It is not another name for the entire chromosome, and protein coding is not the only way a gene can have biological function.",
  "Imani now slides the whole chromosome along the rail into a reproductive-cell record and then into a descendant file. The gene card never detaches from its chromosomal address. A small allele tab clipped to the gene travels with it. This is the physical basis of the statement that **genes are inherited on chromosomes**. Offspring receive alleles as parts of chromosomes transmitted through reproductive cells, and the later behavior of those chromosomes during meiosis will explain Mendelian segregation. The gold heredity thread advances one generation only when the chromosome itself reaches the descendant file.",
  "Only then does the glass archive on the right unlock. Inside, branches from bacteria, plants, fungi, and animals converge on the same basic DNA/RNA information system. A genetic-code panel lights with the same broad codon logic repeated across distant lineages, with a small marker indicating known variants rather than pretending every code is literally identical. Imani labels the pattern **genetic code conservation and common ancestry**. Deep conservation of DNA/RNA information systems and the nearly universal genetic code supports the inference that living organisms share deep common ancestry. The archive is evidence of shared history, not a claim that every organism carries the same DNA sequence.",
  "The intake hall begins moving again. Heredity cards travel between generations, genetics records stay at the investigation desk, genes remain fixed to chromosome loci, and the conserved-information archive glows at the far right. One problem remains. The rail has delivered two similarly shaped chromosomes to the next security door, and the scanner cannot decide whether they are homologous partners or duplicated copies of one chromosome. Imani closes the first line of the gold ledger and follows the blue and amber chromosomes through the vault door before the registry misfiles them again."
 ],
 'close':'With gene and chromosome identity restored, the blue and amber chromosomes trigger an identity alarm in the next room. Imani carries the gold ledger into the Homolog Pair Vault to separate homologous partners from replicated sister chromatids.'
},
'U5-L02':{
 'title':'The Vault of Look-Alike Chromosomes',
 'kicker':'Two chromosomes can resemble each other for two very different reasons, and the vault will not open until those relationships are separated.',
 'paragraphs':[
  "The **Homolog Pair Vault** is colder and narrower than the intake hall. Its three stations are fixed in a single line. On your **left**, the blue chromosome and the amber chromosome stand upright in separate clamps, their gene loci aligned at matching heights. Directly **ahead**, a replication bench holds an empty X-shaped cradle. On your **right**, a wall-sized chromosome display waits in numbered rows. Imani places the gold generation ledger on the center bench and keeps the two chromosome colors unchanged. The security alarm above the vault door flashes SAME, SAME, SAME, even though the three displays represent different relationships.",
  "She begins with the pair on the left. The blue chromosome carries genes at the same corresponding loci as the amber chromosome. At one locus, however, the blue chromosome carries allele A while the amber chromosome carries allele a. Their structural organization is similar and their corresponding genes line up, yet they can carry **different alleles** at corresponding loci. These are **homologous chromosomes**. Homologs are chromosome partners with corresponding genes at the same loci. They are related by chromosome set and ancestry, not by being fresh copies of each other. Imani leaves the A and a tabs visible so the homolog relationship cannot be mistaken for genetic identity.",
  "At the center bench she removes only the blue homolog and activates the replication cradle. The chromosome is copied, producing two blue chromatids joined together. They share the same chromosome origin and initially contain replicated copies of the same DNA sequence. These joined copies are **sister chromatids**. Imani places the replicated blue chromosome beside the original blue-and-amber homolog pair. The comparison is now impossible to miss. Homologous chromosomes are two corresponding chromosome partners. Sister chromatids are the replicated copies of one chromosome held together after DNA replication. Later crossing over can exchange segments between nonsister chromatids of homologs, so even sister chromatids need not remain sequence-identical across every exchanged region.",
  "The right wall still shows a chaotic pile of chromosome images. Imani sorts them using visible properties such as size, centromere position, and banding pattern, placing corresponding chromosomes together in an organized display. The finished wall is a **karyotype**. It is a chromosome display used for analysis. The display can help compare chromosome number and visible structure, while the word karyotype does not mean homologous pair and does not mean sister chromatids. Those chromosome relationships existed before anyone arranged their images on the wall.",
  "The alarm finally changes from SAME to IDENTITIES VERIFIED. Imani draws three symbols in the gold ledger. Two parallel chromosomes mean homologs. One duplicated chromosome means sisters. An arranged wall of chromosome images means karyotype. She then points through the vault’s exit window. The blue and amber homologs are being loaded into a body-cell model, while a second lane contains a reproductive cell with only one chromosome from each pair. The next registry station is already asking a different question. How many chromosome sets does each cell carry?"
 ],
 'close':'The vault stops confusing chromosome relationships, but the exit scanner still cannot distinguish two chromosome sets from one. Imani follows the tracked homologs to the Ploidy Counter.'
},
'U5-L03':{
 'title':'The Counter That Counts Sets, Not Shapes',
 'kicker':'Ploidy depends on chromosome sets. A duplicated chromosome can still belong to one set, so the counter must track the right quantity.',
 'paragraphs':[
  "The corridor opens into the bright **Ploidy Counter**, built like a three-lane customs station for cells. On your **left**, a large body-cell model rolls into the diploid lane carrying the familiar blue and amber homologs together. Directly **ahead**, a mechanical display can flip between 2n and n while two trays beneath it hold chromosome sets. On your **right**, a smaller reproductive-cell model waits in the haploid lane with only one member from each homologous pair. The gold generation ledger lies across the counter, and Imani circles one field in the ledger. CHROMOSOME SET is the quantity that matters here.",
  "The left cell passes under the scanner. It is a **somatic cell**, a non-gamete body cell. In a diploid organism, most somatic cells carry homologous chromosome pairs, so the blue chromosome and the amber homolog appear together. The counter clicks to **2n**. Imani reads the full label aloud as **diploid (2n)**. A cell or nucleus with two chromosome sets is diploid. Imani places one set marker beneath the blue-origin chromosomes and another beneath the amber-origin homologs. The designation describes sets, not whether each chromosome has been replicated into one chromatid or two. Ploidy and DNA amount are related in cell cycles, but they are not the same measurement.",
  "She now moves the counter from 2n to n and transfers one chromosome from each homologous pair into the cell on the right. One complete chromosome set remains. Imani flips the center label to **haploid (n)**. A cell or nucleus with one chromosome set is haploid. The right-hand cell is also a **gamete**, a haploid reproductive cell capable of fusing with another gamete during fertilization. Imani keeps the two labels separate. Haploid describes chromosome-set number. Gamete describes a reproductive cell type. In the life cycles emphasized here, gametes are haploid, yet the concepts answer different questions.",
  "A small panel titled **human diploid and haploid chromosome numbers** rises from the center counter. It shows a typical human somatic cell with **46 chromosomes**, written 2n = 46, and typical human sperm or egg cells with **23 chromosomes**, written n = 23. Imani uses the panel as a count check and then lowers it again. Forty-six and twenty-three are human chromosome numbers. Diploid and haploid are general biological concepts that apply according to chromosome sets in many organisms. The example also keeps sperm and egg in their proper role as common human gametes, without turning those particular gamete types into the definition of gamete.",
  "The scanner runs one final test. It duplicates every chromosome in the left somatic-cell model without adding another homologous set. The chromosome models now look like joined sister chromatids, but the ploidy display remains 2n. Imani taps the unchanged set markers. Replication changes DNA content and chromatid structure; it does not automatically change the number of chromosome sets. That distinction will become essential when meiosis begins later in the unit.",
  "The gate beyond the counter opens onto a forked transit hall. The diploid and haploid records are now correctly labeled, so the registry can finally ask how inheritance moves from one generation to another. One path begins from a single genetic source without gamete fusion. The other passes toward meiotic processes and a future fusion chamber. Imani closes the chromosome-set field in the ledger and walks to the split."
 ],
 'close':'With somatic cell, gamete, diploid, and haploid separated by their actual biological meanings, the registry can compare how genetic information travels through asexual and sexual reproduction. The route divides at the Reproduction Fork.'
},
'U5-L04':{
 'title':'The Fork With Two Routes Into the Future',
 'kicker':'Both paths transmit biological information, but they use different reproductive mechanisms and create different patterns of genetic similarity.',
 'paragraphs':[
  "The **Reproduction Fork** is a broad hall shaped like a Y. On your **left**, a single parent record feeds into a quiet conveyor that branches into a line of descendant files. Directly **ahead**, a raised comparison platform keeps both routes visible at once. On your **right**, chromosome records pass toward a sign marked MEIOTIC PROCESSES and then toward a distant gamete-fusion chamber. The gold generation ledger hangs from the center railing. Imani keeps the same tracked chromosome information on both sides so the comparison concerns reproductive mechanism rather than a change in what heredity means.",
  "She starts the left conveyor from one genetic source. No gamete fusion occurs. A descendant record appears, then another, then another, each carrying a chromosome record very similar to the original. This route is **asexual reproduction**. It involves one genetic source without gamete fusion and commonly produces clonal descendants that are genetically very similar to the parent. Imani leaves a small change window open on every descendant file. Mutation and other genetic changes can arise over time, and environmental conditions can also make genetically similar organisms look or function differently. The route therefore never receives a stamp that says PERFECTLY IDENTICAL FOREVER.",
  "The descendants on the left are labeled a **clone** line because they derive from one ancestral cell or organism through asexual processes and are genetically very similar. Imani pulls one record from the line and adds a newly arisen genetic variant. It remains part of the clonal lineage even though its genome is no longer literally identical to the founding record. The word clone describes descent and strong genetic similarity in this context. It does not require permanent molecular identity across every descendant and every generation.",
  "She activates the right route next. Chromosome records move toward meiotic processes, generating haploid gametes that can later fuse. When gametes combine, alleles from the contributing chromosome sets enter a new combination. This is **sexual reproduction**. Sexual reproduction includes meiosis or meiotic processes and fusion of gametes, producing new combinations of parental alleles. Imani deliberately opens a side gate labeled SELF-FERTILIZATION. A single organism can contribute gametes in some sexual life cycles. The defining biological mechanism therefore cannot be reduced to a rule that two separate parent organisms are always required.",
  "From the center platform, the contrast becomes stable enough to redraw. The left route begins with one genetic source and proceeds without gamete fusion, often producing highly similar clonal descendants. The right route uses meiotic processes and gamete fusion, creating new combinations of alleles. Both transmit inherited information. Their mechanisms differ, and those mechanisms influence the genetic relationships among descendants.",
  "A warning light appears at the end of the sexual route. The gametes have reached the next chamber, but their ledger entries still read n and n. The registry cannot close the generation until it knows what happens when those haploid cells fuse. Imani follows their chromosome markers through the right-hand door, and the two arms of the Y curve toward a circular room beyond."
 ],
 'close':'The sexual route ends with two haploid gametes still separated. Their chromosome sets must be combined before the next generation can begin, so Imani leads you into the Life-Cycle Fusion Loop.'
},
'U5-L05':{
 'title':'The Loop That Restores the Chromosome Set',
 'kicker':'The generation closes when haploid gametes fuse, their chromosome sets combine, and a diploid zygote begins the next developmental sequence.',
 'paragraphs':[
  "The final doors open into the circular **Life-Cycle Fusion Loop**. The room is arranged like a ring so you can see where one generation hands its chromosome information to the next. On your **left**, two haploid gamete models enter on separate rails, each marked n and each carrying one chromosome set. Directly **ahead**, the rails meet inside a transparent fusion chamber. On your **right**, a new cell exits onto a broad 2n developmental track that curves around the room and eventually points toward the reproductive stages of another generation. Imani clips the gold generation ledger beside the chamber so the chromosome-set change can be watched as it happens.",
  "The two gametes enter the center chamber. Their membranes meet and the chromosome sets that had been separated between the two cells are brought into one new cell. The ledger changes from n + n to 2n. This process is **fertilization**, the fusion of haploid gametes. Sperm and egg are one common example of gametes that fuse in anisogamous organisms, including humans, while the general biological concept is gamete fusion. The chamber summarizes the relationship in one line, **fertilization restores diploidy and creates allele combinations**. In the standard diploid sexual life-cycle model, fertilization restores the diploid chromosome number and creates new allele combinations because the new cell contains chromosome contributions from the two gametes.",
  "A gold light appears around the immediate product of fusion. Imani labels that cell a **zygote**. A zygote is the cell produced by gamete fusion, and in the standard diploid sexual life cycle shown here it is diploid. She moves the zygote onto the right-hand track before anything else is allowed to happen. The distinction matters. Fertilization is the fusion event. Zygote names the cell produced by that event. Sexual reproduction includes a broader sequence of biological processes and cannot be reduced to the instant of fertilization alone.",
  "The right-hand track now carries the zygote toward development. As the circular wall display advances, it shows reproductive and developmental stages leading from one generation toward the next. This sequence is a **life cycle**. Imani leaves several side routes visible beyond the main ring to show that sexual life cycles vary widely among organisms. Some life cycles emphasize different multicellular stages, and the registry does not force them into one universal diagram. The relationship you need to preserve here is narrower and more durable. Haploid gametes can fuse, their chromosome sets combine, and the resulting cell can continue the next generation’s developmental sequence.",
  "Imani turns the ledger back toward the left entrance and traces the completed journey with one gloved finger. Heredity carried information across generations. Genes occupied loci on chromosomes and traveled with those chromosomes. Homologous chromosomes were separated from sister chromatids. Diploid and haploid described chromosome-set number, while somatic cell and gamete described cell types. Asexual and sexual reproduction followed different routes. Finally, fertilization joined haploid gametes and produced a diploid zygote. The five rooms now form one continuous bookkeeping system rather than five disconnected vocabulary displays.",
  "Two chromosome icons appear on Imani’s tablet, one blue and one amber. They are now properly labeled homologs, their loci are stable, and the ledger can account for 2n and n without confusion. The registry’s inner doors unlock. Beyond them lies a much larger transit hall where those same chromosomes will replicate, pair, exchange segments, and separate. Imani does not replace them with a fresh diagram. She carries the same blue and amber identities forward, ready for the next journey through meiosis."
 ],
 'close':'Journey 1 closes with one reconstructable inheritance loop. Genes ride on chromosomes, chromosome relationships and ploidy are distinct, reproductive routes are separated, and fertilization combines haploid chromosome sets in a diploid zygote. The same blue and amber homologs are now ready to enter Meiosis Transit Hall.'
},
}


def sha(path:Path): return hashlib.sha256(path.read_bytes()).hexdigest()

def make_cast(b):
    zones=ZONE_COPY[b['locus_id']]
    cast=[{'name':GUIDE['name'],'kind':'guide','visual':GUIDE['visual'],'job':GUIDE['story_job']}]
    for position,label,symbol,desc in zones:
        source=next(x for x in b['stable_cast'] if x['position']==position)
        cast.append({
          'name':label,'kind':'scientific part or process','visual':desc,
          'job':source['job_in_scene']
        })
    cast.append({
      'name':'Gold generation ledger','kind':'continuity tool',
      'visual':'a narrow gold-edged ledger with four persistent fields labeled chromosome set, cell type, reproductive transition, and generation',
      'job':'records only real biological state changes as the same chromosome information passes through the five registry locations; it never replaces a chromosome, gene, cell, or reproductive process'
    })
    return cast

def make_beats(b):
    beats=[]
    for t in b['term_introductions']:
        kid=t['knowledge_id']
        beats.append({
          'object_id':kid,'term':t['canonical_term'],'story':BEAT_IMAGES[kid],
          'science':t['canonical_science'],'exact_name':bool(t['exact_name_recall']),
          'hint':BEAT_IMAGES[kid],'name_support':t['name_support']
        })
    return beats

def make_snapshot(b):
    return [{'term':t['canonical_term'],'meaning':t['canonical_science'],'image':BEAT_IMAGES[t['knowledge_id']]} for t in b['term_introductions']]

scenes=[]
briefs=[B[f'U5-L{i:02d}'] for i in range(1,6)]
for idx,b in enumerate(briefs):
    narr=NARR[b['locus_id']]
    zones=[{'position':p,'label':label,'symbol':sym,'description':desc} for p,label,sym,desc in ZONE_COPY[b['locus_id']]]
    q=b['quick_recall']
    checkpoint=bool(q['enabled'])
    cp_id=None
    if checkpoint:
        # Choose the most diagnostic exact-name term named in the answer/prompt.
        cp_id='U5-K-042' if b['locus_id']=='U5-L02' else 'U5-K-053'
    scenes.append({
      'scene_index':idx,'locus_id':b['locus_id'],'locus':b['scene_title'],'title':narr['title'],'scene_kicker':narr['kicker'],
      'location_description':b['micro_anchor'],
      'scene_layout':{'orientation':b['orientation_sentence'],'zones':zones},
      'cast':make_cast(b),'continuity_object':J1['continuity_object'],
      'story_open':narr['paragraphs'][0],'story_paragraphs':narr['paragraphs'],'story_close':narr['close'],
      'object_ids':b['knowledge_ids'],'story_beats':make_beats(b),'memory_snapshot':make_snapshot(b),
      'misconception_guards':b['misconception_guards'],'exit_memory':b['exit_memory'],
      'checkpoint':checkpoint,'checkpoint_object_id':cp_id,
      'checkpoint_prompt':q.get('candidate_prompt','') if checkpoint else '',
      'checkpoint_answer':q.get('answer','') if checkpoint else '',
      'checkpoint_hint':('Picture the fixed left, center, and right chromosome structures and recall the relationship that changed at the center before naming it.' if checkpoint else ''),
      'next_locus':briefs[idx+1]['scene_title'] if idx+1<len(briefs) else None,
      'causal_transition':b['causal_transition']['transition_logic'],
    })

journey={
 'palace_id':'U5-J1','unit_id':'unit-5','palace_name':'Heredity and Chromosome Registry',
 'story_title':'The Registry That Lost Its Generations',
 'tagline':'A damaged inheritance registry has mixed genes, chromosomes, cell types, ploidy, and reproductive routes into one record. Rebuild the identities before the chromosomes enter meiosis.',
 'guide':GUIDE,
 'premise':('A power failure has scrambled the Heredity and Chromosome Registry just before a new generation of records is due to be certified. Gene cards have been separated from chromosome addresses, homologous chromosomes are being confused with replicated sister chromatids, cell entries have lost their chromosome-set labels, and the two reproductive routes feed into the same unlabeled corridor. Dr. Imani Reyes cannot open the inner meiosis hall until the registry can account for exactly what is inherited, what biological structure carries it, how many chromosome sets each cell contains, and how those sets move from one generation to the next.'),
 'mission':('Follow Dr. Imani Reyes through five physically connected registry stations. Keep the same blue and amber chromosome identities visible while you restore gene-to-chromosome filing, homolog and sister-chromatid identity, diploid and haploid bookkeeping, reproductive-route differences, and the fertilization step that combines haploid chromosome sets in a diploid zygote.'),
 'finale':('The gold generation ledger closes only after every field can be reconstructed from the five rooms. Genes remain fixed to chromosome loci, homologs remain distinct from sister chromatids, chromosome-set number is separated from cell type, asexual and sexual reproductive mechanisms occupy different routes, and fertilization combines haploid gametes to produce a diploid zygote. The same tracked blue and amber homologs then pass through the unlocked inner doors toward Meiosis Transit Hall.'),
 'estimated_minutes':15,'scene_count':5,'checkpoint_count':2,'student_release':'DEVELOPER_PREVIEW_F4A',
 'learner_rule':'Read or listen and picture the room before following the biological action. The important terms are named only after the structure or process that defines them becomes visible. Optional Quick Recall appears only twice.',
 'route_orientation':('This is a five-location route through one inheritance-registry building. Enter at the Heredity Record Desk, move straight into the Homolog Pair Vault, pass through the Ploidy Counter, follow the hall to the Reproduction Fork, and finish in the circular Life-Cycle Fusion Loop. The gold generation ledger and the same blue and amber chromosome identities persist across all five locations.'),
 'route':route,'scenes':scenes,'narrative_design':'U5-F4A-NARRATIVE-1.0'
}

(U5/'journeys').mkdir(exist_ok=True)
(U5/'journeys'/'U5-J1.json').write_text(json.dumps(journey,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
registry={
 'schema':'memory-palace-v2-unit5-f4a-journeys-1.0','unit_id':'unit-5','stage':'F4A',
 'student_release':False,'preview_release':True,'journey_count':1,'scene_count':5,'checkpoint_count':2,
 'guided_journeys':[{k:journey[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','student_release','narrative_design']}]
}
(U5/'journeys-f4a.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

status={
 'unit_id':'unit-5','unit_number':5,'title':'Heredity','status':'F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW',
 'pipeline_status':'POLISHED_NARRATIVE_PILOT_F4A','canonical_lock':'LOCKED_F1','architecture_lock':'LOCKED_F2','scene_brief_lock':'LOCKED_F3',
 'student_release':False,'preview_release':True,'canonical_records':152,'review_flags_resolved':37,'teacher_ppt_slides':112,'ced_topics':5,'ced_atoms':34,
 'journey_count':1,'scene_count':5,'memory_objects':0,'application_challenges':0,
 'architecture_journeys':8,'architecture_bundles':19,'architecture_loci':50,'journey_briefs':8,'scene_briefs':50,
 'palace_managed_records':131,'scope_guard_records':5,'practice_only_records':16,'confusable_sets':32,'optional_first_exposure_recalls':18,
 'next_required_output':'F4B polished narrative for Journey 2 only after F4A prose QA and human narrative review',
 'narrative_lock':'LOCKED_F4A_J1','polished_journeys':1,'polished_scenes':5,'polished_checkpoint_count':2,'narrative_story_files':1
}
(U5/'status-f4a.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(U5/'status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

manifest={
 'schema':'memory-palace-v2-unit5-f4a-release-manifest-1.0','unit_id':'unit-5','stage':'F4A','student_release':False,'preview_release':True,
 'canonical_records_protected':152,'polished_journeys':1,'polished_scenes':5,'journey_1_records':20,'journey_1_checkpoints':2,
 'narrative_words':sum(len(re.findall(r"\b[\w’'-]+\b",' '.join(s['story_paragraphs']))) for s in scenes),
 'next_stage':'F4B_JOURNEY2_AFTER_F4A_HUMAN_REVIEW'
}
(U5/'f4a-release-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Update course registry to developer-preview state without exposing a student runtime.
course_path=ROOT/'content'/'ap-biology'/'course.json'
course=json.loads(course_path.read_text(encoding='utf-8'))
u5=next(u for u in course['units'] if u['unit_id']=='unit-5')
u5.update({
 'status':'F4A_JOURNEY1_POLISHED_DEVELOPER_PREVIEW','journey_count':1,'scene_count':5,'canonical_lock':'LOCKED_F1',
 'source_status':'AUDITED_SCIENCE_LOCKED_F1_ARCHITECTURE_F2_SCENE_BRIEFS_F3_NARRATIVE_J1_F4A',
 'canonical_records':152,'review_flags_resolved':37,'ced_atoms':34,'teacher_ppt_slides':112,'student_release':False,'preview_release':True,
 'pipeline_stage':'UNIT5_JOURNEY1_POLISHED_DEVELOPER_PREVIEW_F4A','architecture_journeys':8,'architecture_loci':50,'architecture_lock':'LOCKED_F2',
 'scene_brief_lock':'LOCKED_F3','scene_briefs':50,'optional_first_exposure_recalls':18,'polished_journeys':1,'polished_scenes':5
})
course_path.write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Lock F4A outputs only. Earlier locks remain independently protected and QA-verified.
lock_files=['journeys/U5-J1.json','journeys-f4a.json','status-f4a.json','f4a-release-manifest.json']
lock={
 'schema':'memory-palace-v2-unit5-content-lock-f4a-1.0','unit_id':'unit-5','stage':'F4A','lock_status':'LOCKED_F4A_J1',
 'student_release':False,'preview_release':True,
 'files':{rel:{'bytes':(U5/rel).stat().st_size,'sha256':sha(U5/rel)} for rel in lock_files}
}
(U5/'content-lock-f4a.json').write_text(json.dumps(lock,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Developer-facing narrative document.
lines=['# Unit 5 F4A · Journey 1 Narrative','',f"## {journey['story_title']}",'',journey['tagline'],'',f"**Palace.** {journey['palace_name']}",'',f"**Guide.** {GUIDE['name']} · {GUIDE['role']}",'',f"**Premise.** {journey['premise']}",'',f"**Mission.** {journey['mission']}",'']
for s in scenes:
    lines += [f"## {s['scene_index']+1}. {s['locus']} · {s['title']}",'',f"*{s['scene_kicker']}*",'']
    lines += s['story_paragraphs']+['',f"**Causal handoff.** {s['causal_transition']}",'']
    if s['checkpoint']:
        lines += [f"**Optional Quick Recall.** {s['checkpoint_prompt']}",'']
lines += ['## Finale','',journey['finale'],'']
(ROOT/'docs'/'UNIT5_F4A_JOURNEY1_STORY.md').write_text('\n'.join(lines),encoding='utf-8')

release=['# Unit 5 F4A Release','', 'Unit 5 F4A authors and locks Journey 1 only. Unit 5 remains a developer preview and is not student released.','',
 '## Locked output','', '- Journey: **U5-J1 · Heredity and Chromosome Registry**', '- Polished scenes: **5**', '- Locked Journey 1 records: **20**', '- Optional first-exposure recalls: **2**', f"- Narrative words: **{manifest['narrative_words']}**", '',
 '## Narrative rule','', 'The five scenes form one continuous registry story. The same guide, gold generation ledger, and tracked chromosome identities persist from the first record desk through fertilization. Scientific structures perform the memorable actions. Source-management language remains outside student prose.','',
 '## Release boundary','', 'No Unit 5 Memory Objects, Review runtime, Challenge Lab runtime, or student-facing Unit 5 release is created in F4A. Journeys 2–8 remain at the F3 scene-brief stage.','',
 '## Next gate','', 'F4B may author Meiosis Transit Hall only after F4A narrative QA and human narrative review.','']
(ROOT/'docs'/'UNIT5_F4A_RELEASE.md').write_text('\n'.join(release),encoding='utf-8')
print(json.dumps({'journey':'U5-J1','scenes':5,'records':20,'checkpoints':2,'narrative_words':manifest['narrative_words'],'student_release':False,'preview_release':True},indent=2))
