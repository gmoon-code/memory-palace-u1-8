from __future__ import annotations
import importlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.unit1_story_common import build_journey,UNIT

OUT=UNIT/'journeys';OUT.mkdir(parents=True,exist_ok=True)
water=json.loads((UNIT/'reference-journey-water.json').read_text(encoding='utf-8'))
water['narrative_design']='V2-NARRATIVE-2.0'
journeys=[]
for pid in ['Z1','Z2']:
 m=importlib.import_module(f'scripts.stories.{pid.lower()}')
 journeys.append(build_journey(m.META,m.SCENES))
journeys.append(water)
for pid in ['Z4','Z5','Z6','Z7','Z8','Z9']:
 m=importlib.import_module(f'scripts.stories.{pid.lower()}')
 journeys.append(build_journey(m.META,m.SCENES))
journeys.sort(key=lambda j:int(j['palace_id'][1:]))
for j in journeys:
 (OUT/f"{j['palace_id']}.json").write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
summary={'schema_version':'memory-palace-v2-unit1-1.0','course_id':'ap-biology','unit_id':'unit-1','unit_title':'Chemistry of Life','narrative_standard':'V2-NARRATIVE-2.0','journey_count':len(journeys),'scene_count':sum(j['scene_count'] for j in journeys),'checkpoint_count':sum(j['checkpoint_count'] for j in journeys),'guided_journeys':[{k:j[k] for k in ['palace_id','palace_name','story_title','tagline','guide','premise','mission','finale','estimated_minutes','scene_count','checkpoint_count','narrative_design']} for j in journeys]}
(UNIT/'journeys.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


# Build a compact Unit 1 application lab from the audited transfer bench.
# These tasks remain outside the permanent palace so students can apply the science without
# pretending every AP skill belongs in a mnemonic scene.
mos=json.loads((UNIT/'memory-objects.json').read_text(encoding='utf-8'))['memory_objects']
by_knowledge={o.get('source_knowledge_id'):o for o in mos}
transfer=json.loads((UNIT/'transfer-bench.json').read_text(encoding='utf-8'))['transfer_bench']
PROMPT_OVERRIDES={
 'PK-STAT-011':"Two treatments have means of 15.0 ± 0.4 and 14.8 ± 0.4, where the bars are ±2 SEM. A student says, 'Because the bars overlap, the treatments are definitely not significantly different.' Evaluate the statement.",
 'PK-MET-021':"A plant treatment group increases mean oxygen production from 12.0 to 15.0 µmol O₂/m²/s, while a water-control group changes from 12.1 to 12.3. Write one evidence statement supporting the claim that the treatment increased photosynthetic activity, then write a separate reasoning statement connecting the evidence to the biological process.",
 'PK-MET-022':"A treatment group shows a clear increase in oxygen production after treatment while the control remains nearly unchanged. Go beyond restating the numbers. Explain how the result connects to the larger biological process of photosynthesis.",
}
ANSWER_OVERRIDES={
 'PK-STAT-011':"The statement is too strong. First identify what the error bars represent. Overlap or non-overlap of ±2 SEM bars alone is not a universal formal significance test; a suitable statistical procedure and its assumptions are needed for a formal significance conclusion.",
 'PK-MET-021':"Evidence example: the treatment group's mean oxygen production increased by 3.0 µmol O₂/m²/s, while the control changed by only 0.2. Reasoning example: oxygen is produced during photosynthesis, so the larger increase in oxygen production is consistent with greater photosynthetic activity under the treatment; the control comparison makes time alone a weaker explanation for the change.",
 'PK-MET-022':"Because oxygen is produced during photosynthesis, an increase in oxygen-production rate is consistent with increased photosynthetic activity under the experimental conditions. The result should be interpreted as evidence about the rate of that biological process, not only as a numerical change.",
 'PK-CHO-020':"The cow would obtain less energy from the cellulose because fewer cellulose-digesting rumen microorganisms would reduce microbial digestion of cellulose. The scenario supports that specific causal conclusion; it does not by itself support broader claims about all agricultural antibiotic use.",
}
practice_only_ids=[]
story_ids={oid for j in journeys for sc in j['scenes'] for oid in sc['object_ids']}
items=[]
for i,t in enumerate(transfer,1):
    o=by_knowledge.get(t['knowledge_id'])
    if not o: raise RuntimeError(f"No Memory Object for transfer item {t['knowledge_id']}")
    if o['memory_object_id'] not in story_ids: practice_only_ids.append(o['memory_object_id'])
    q=PROMPT_OVERRIDES.get(t['knowledge_id']) or o.get('application_question') or t['required_practice']
    a=ANSWER_OVERRIDES.get(t['knowledge_id']) or o.get('application_answer_key') or t['canonical_verified_statement']
    items.append({
      'challenge_id':f"U1-APP-{i:02d}",
      'knowledge_id':t['knowledge_id'],
      'memory_object_id':o['memory_object_id'],
      'domain':t['domain'],
      'title':t['canonical_label'],
      'prompt':q,
      'answer_guide':a,
      'story_hint':t['supporting_mnemonic_cue'] if t['supporting_mnemonic_cue']!='No permanent mnemonic cue required.' else 'Return to the scientific relationship you learned in the story.',
      'success_criterion':'Solve the fresh problem and explain the reasoning. Recognition of a palace image alone is not enough.',
      'practice_only_runtime':o['memory_object_id'] not in story_ids,
    })
application_lab={
 'unit_id':'unit-1','title':'Unit 1 Challenge Lab',
 'student_intro':'Use these only after you have learned the relevant story. One challenge appears at a time so application practice stays manageable.',
 'challenge_count':len(items),'practice_only_runtime_count':len(set(practice_only_ids)),
 'practice_only_runtime_object_ids':sorted(set(practice_only_ids)),
 'items':items
}
(UNIT/'application-lab.json').write_text(json.dumps(application_lab,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

course_path=UNIT.parent/'course.json'
default_later_units=[
  {'unit_id':'unit-2','number':2,'title':'Cells','status':'SOURCE_AVAILABLE_NOT_MIGRATED','journey_count':0,'scene_count':0,'canonical_lock':'NOT_YET_BUILT','source_status':'SOURCE_AVAILABLE'},
  {'unit_id':'unit-3','number':3,'title':'Cellular Energetics','status':'SOURCE_AVAILABLE_NOT_MIGRATED','journey_count':0,'scene_count':0,'canonical_lock':'NOT_YET_BUILT','source_status':'SOURCE_AVAILABLE'},
  {'unit_id':'unit-4','number':4,'title':'Cell Communication and Cell Cycle','status':'SOURCE_AVAILABLE_NOT_MIGRATED','journey_count':0,'scene_count':0,'canonical_lock':'NOT_YET_BUILT','source_status':'SOURCE_AVAILABLE'},
  {'unit_id':'unit-5','number':5,'title':'Heredity','status':'SOURCE_AVAILABLE_NOT_MIGRATED','journey_count':0,'scene_count':0,'canonical_lock':'NOT_YET_BUILT','source_status':'SOURCE_AVAILABLE'},
  {'unit_id':'unit-6','number':6,'title':'Gene Expression and Regulation','status':'SOURCE_AVAILABLE_NOT_MIGRATED','journey_count':0,'scene_count':0,'canonical_lock':'NOT_YET_BUILT','source_status':'SOURCE_AVAILABLE'},
  {'unit_id':'unit-7','number':7,'title':'Natural Selection','status':'SOURCE_AVAILABLE_NOT_MIGRATED','journey_count':0,'scene_count':0,'canonical_lock':'NOT_YET_BUILT','source_status':'SOURCE_AVAILABLE'},
  {'unit_id':'unit-8','number':8,'title':'Ecology','status':'SOURCE_AVAILABLE_NOT_MIGRATED','journey_count':0,'scene_count':0,'canonical_lock':'NOT_YET_BUILT','source_status':'SOURCE_AVAILABLE'}
]
if course_path.exists():
    prior_course=json.loads(course_path.read_text(encoding='utf-8'))
    prior_by_id={u['unit_id']:u for u in prior_course.get('units',[]) if u.get('unit_id')!='unit-1'}
    later_units=[prior_by_id.get(u['unit_id'],u) for u in default_later_units]
else:
    later_units=default_later_units
course={
 'course_id':'ap-biology','course_title':'AP Biology','content_model_version':'v2-course-1.0',
 'student_experience':'Learn through vivid guided journeys, then use short adaptive review.',
 'units':[{'unit_id':'unit-1','number':1,'title':'Chemistry of Life','status':'STUDENT_READY','journey_count':9,'scene_count':78,'application_challenges':16,'canonical_lock':'LOCKED','source_status':'AUDITED_AND_LOCKED'}]+later_units
}
course_path.write_text(json.dumps(course,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

source_index={'policy':'Source PDFs are kept outside the GitHub repository. This manifest records local source identity for reproducibility; no copyrighted textbook or classroom PDF is redistributed with V2.','sources':[
 {'unit_id':'unit-1','role':'classroom_presentation','filename':'APBIO-U1-PPT.pdf','bytes':2667019,'sha256':'da1f0810173ddb75bb2e73fca696e1cddfbd76cbbac00ce56d1921b09c7b4662'},
 {'unit_id':'unit-1','role':'classroom_packet','filename':'APBIO-U1-Packet.pdf','bytes':2157184,'sha256':'15e516592fc84f79e2584da69f3dbae5343dd386667709f3f166e48e8d1e5127'},
 {'unit_id':'unit-2','role':'classroom_presentation','filename':'APBIO-U2-PPT(1).pdf','bytes':2805892,'sha256':'ca1042ce1a8b8998672b7e260bc056b6e3cc548be939421ef7d5246ff646327c'},
 {'unit_id':'unit-3','role':'classroom_presentation','filename':'APBIO-U3-PPT.pdf','bytes':3671885,'sha256':'00e231d3d2426182660df0c137ea39d47f8b4937a5b025f776a6b0c21966672c'},
 {'unit_id':'unit-4','role':'classroom_presentation','filename':'APBIO-U4-PPT.pdf','bytes':2506345,'sha256':'5c0216515be45277e21d703f77869126c120e1b057ce6d86579e0fc9bd5894c5'},
 {'unit_id':'unit-5','role':'classroom_presentation','filename':'APBIO-U5-PPT.pdf','bytes':2178455,'sha256':'3b5297a4e79266c32f1f3d792c5c59b58b9c3e99fdcdb7562413664863373522'},
 {'unit_id':'unit-6','role':'classroom_presentation','filename':'APBIO-U6-PPT.pdf','bytes':6179065,'sha256':'d6ae98c3f6a505baebca53c1af5b48b78bfe78f79360797da659b62fd5f4da3e'},
 {'unit_id':'unit-7','role':'classroom_presentation','filename':'APBIO-U7-PPT.pdf','bytes':4390563,'sha256':'a796624b377ff24ea22f983c9769221b6aeaf57ac39d4e7afa0939813bd5fa6a'},
 {'unit_id':'unit-8','role':'classroom_presentation','filename':'APBIO-U8-PPT.pdf','bytes':5044342,'sha256':'2696e2e6daecb01a64f3072f344266b809a1e96d7245495c6837741f1b064818'},
 {'unit_id':'all','role':'course_framework','filename':'ap-biology-course-and-exam-description.pdf','bytes':5140208,'sha256':'30db56cdd81a231b17d48aeda420364794b285beedfd1f1a1c256de0939b793c'},
 {'unit_id':'all','role':'scientific_reference','filename':'Campbell Biology (13th Ed.) by Urry, Minorsky, Hull & Orr.pdf','bytes':183657532,'sha256':'f918b65468142a17826c360a303497a1fe00a9f5e14f14c7c5a139402a1cc0cc'}
]}
(UNIT.parent/'source-index.json').write_text(json.dumps(source_index,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Built',len(journeys),'journeys',sum(j['scene_count'] for j in journeys),'scenes',sum(j['checkpoint_count'] for j in journeys),'checkpoints')
