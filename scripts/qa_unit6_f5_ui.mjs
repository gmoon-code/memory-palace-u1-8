import fs from 'fs';
global.localStorage={store:new Map(),setItem(k,v){this.store.set(k,String(v))},getItem(k){return this.store.has(k)?this.store.get(k):null},removeItem(k){this.store.delete(k)},clear(){this.store.clear()}};
const stateMod=await import('../frontend/js/state.js');
const {homeView}=await import('../frontend/js/views/home.js');
const {learnView,sceneSpeech}=await import('../frontend/js/views/learn.js');
const {reviewView}=await import('../frontend/js/views/review.js');
const {practiceView}=await import('../frontend/js/views/practice.js');
function read(p){return JSON.parse(fs.readFileSync(new URL('../'+p,import.meta.url),'utf8'))}
function assert(x,msg){if(!x)throw new Error(msg)}
function count(hay,needle){return hay.split(needle).length-1}
const course=read('content/ap-biology/course.json');
const status=read('content/ap-biology/unit-6/status.json');
const registry=read('content/ap-biology/unit-6/journeys-f5.json');
const mixed=read('content/ap-biology/unit-6/mixed-discrimination-f5.json');
const review=read('content/ap-biology/unit-6/review-manifest-f5.json');
const lab=read('content/ap-biology/unit-6/application-lab.json');
const journeys=Array.from({length:6},(_,i)=>read(`content/ap-biology/unit-6/journeys/U6-J${i+1}.json`));
assert(status.status==='STUDENT_READY'&&status.student_release===true&&status.preview_release===false,'Unit 6 is not student-ready');
assert(registry.journey_count===6&&registry.scene_count===53&&registry.checkpoint_count===18,'Unit 6 registry drifted');
let rendered=0, recalls=0;
for(const j of journeys){
  for(let i=0;i<j.scenes.length;i++){
    const s=j.scenes[i], html=learnView(j,i,false); rendered++;
    assert(html.includes('scene-orientation')&&html.includes('story-prose')&&html.includes('cast-section'),`${j.palace_id} scene ${i+1} missing core render`);
    assert(count(html,'class="stage-zone ')===3,`${j.palace_id} scene ${i+1} spatial zones != 3`);
    assert(sceneSpeech(j,i).length>100,`${j.palace_id} scene ${i+1} speech too thin`);
    if(s.checkpoint){const r=learnView(j,i,true);recalls++;assert(r.includes('Quick recall · story hidden'),`${j.palace_id} recall missing`);for(const leak of ['scene-orientation','story-prose','memory-panel','route-wrap','cast-section'])assert(!r.includes(leak),`${j.palace_id} recall leaks ${leak}`)}
  }
}
assert(rendered===53&&recalls===18,'Unit 6 scene/recall render count mismatch');
const u6={...course.units.find(u=>u.unit_id==='unit-6'),...status};
const uiState={activeUnit:'unit-6',activeJourney:'U6-J3',sceneByJourney:{'U6-J3':2},review:[],storySeen:{'U6-J3:0':true,'U6-J3:1':true},completedJourneys:{},encounteredObjects:{},version:3};
const home=homeView(course,u6,registry.guided_journeys,uiState,3);
assert(count(home,'class="card journey-card"')===6,'Unit 6 Home journey count wrong');
assert(home.includes('16 challenges')&&home.includes('Open challenge lab'),'Unit 6 Challenge Lab entry missing');
assert(!home.includes('preview-banner'),'Unit 6 still renders preview banner');
for(const uid of ['unit-1','unit-2','unit-3','unit-4','unit-5'])assert(home.includes(`data-unit="${uid}"`),`Released ${uid} switch missing`);
let scheduler={activeUnit:'unit-6',review:[],encounteredObjects:{}};
for(const t of review.targets)stateMod.scheduleEncounteredReview(scheduler,{unitId:'unit-6',objectId:t.knowledge_id,prompt:t.prompt,hint:t.hint,answer:t.target_answer});
assert(scheduler.review.filter(x=>x.type==='exact'&&x.unitId==='unit-6').length===134,'Unit 6 exact target scheduling wrong');
for(const set of mixed.sets)for(const id of set.knowledge_ids)stateMod.markEncountered(scheduler,id);
stateMod.scheduleEligibleMixedReviews(scheduler,mixed.sets,'unit-6');
assert(scheduler.review.filter(x=>x.type==='mixed'&&x.unitId==='unit-6').length===37,'Unit 6 mixed scheduling wrong');
scheduler.review=scheduler.review.map(x=>({...x,dueAt:0}));
assert(stateMod.dueReviews(scheduler,5,'unit-6').length===5,'Unit 6 visible review limit != 5');
assert(stateMod.totalDue(scheduler,'unit-6')===171,'Unit 6 due total should be 134 exact + 37 mixed');
const set=mixed.sets[0], m={type:'mixed',unitId:'unit-6',objectId:`MIXED:${set.set_id}`,setId:set.set_id,questionIndex:0,dueAt:0};
assert(reviewView([m],1,mixed.sets).includes('Mixed discrimination'),'Unit 6 mixed review render failed');
assert(lab.challenge_count===16&&practiceView(lab,0,false).includes('1 of 16')&&practiceView(lab,15,false).includes('16 of 16'),'Unit 6 challenge progression failed');
for(let i=0;i<lab.items.length;i++){assert(practiceView(lab,i,true).includes('Answer guide'),`Unit 6 challenge ${i+1} answer render failed`)}
console.log('UNIT6 F5 UI LOGIC QA PASS');
console.log(JSON.stringify({scenes_rendered:rendered,recalls_rendered:recalls,exact_targets_queued:134,mixed_sets_queued:37,mixed_questions:94,visible_due_limit:5,challenge_lab_items:16},null,2));
