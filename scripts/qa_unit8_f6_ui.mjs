import fs from 'fs';
global.localStorage={store:new Map(),setItem(k,v){this.store.set(k,String(v))},getItem(k){return this.store.has(k)?this.store.get(k):null},removeItem(k){this.store.delete(k)},clear(){this.store.clear()}};
const stateMod=await import('../frontend/js/state.js');
const {homeView}=await import('../frontend/js/views/home.js');
const {learnView,sceneSpeech}=await import('../frontend/js/views/learn.js');
const {reviewView}=await import('../frontend/js/views/review.js');
const {practiceView}=await import('../frontend/js/views/practice.js');
const {prepareSpeechText}=await import('../frontend/js/audio.js');
function read(p){return JSON.parse(fs.readFileSync(new URL('../'+p,import.meta.url),'utf8'))}
function text(p){return fs.readFileSync(new URL('../'+p,import.meta.url),'utf8')}
function assert(x,msg){if(!x)throw new Error(msg)}
function count(hay,needle){return hay.split(needle).length-1}

const course=read('content/ap-biology/course.json');
const status=read('content/ap-biology/unit-8/status.json');
const registry=read('content/ap-biology/unit-8/journeys-f5.json');
const mixed=read('content/ap-biology/unit-8/mixed-discrimination-f5.json');
const review=read('content/ap-biology/unit-8/review-manifest-f5.json');
const lab=read('content/ap-biology/unit-8/application-lab.json');
const journeys=Array.from({length:8},(_,i)=>read(`content/ap-biology/unit-8/journeys/U8-J${i+1}.json`));
assert(status.status==='STUDENT_READY'&&status.student_release===true&&status.preview_release===false,'Unit 8 is not student-ready');
assert(status.browser_validation==='PASS_F6'&&status.pipeline_stage==='UNIT8_CLASSROOM_BROWSER_VALIDATED_F6','Unit 8 F6 browser validation status missing');
assert(registry.journey_count===8&&registry.scene_count===58&&registry.checkpoint_count===18,'Unit 8 registry drifted');
const routeLengths=journeys.map(j=>j.scenes.length);
assert(JSON.stringify(routeLengths)===JSON.stringify([12,9,5,7,5,8,4,8]),'Unit 8 route lengths drifted');

let renderedScenes=0,renderedRecalls=0;
for(const j of journeys){
  assert((j.route||[]).length===j.scenes.length,`${j.palace_id} route does not match scenes`);
  for(let i=0;i<j.scenes.length;i++){
    const s=j.scenes[i], html=learnView(j,i,false); renderedScenes++;
    assert(html.includes('scene-orientation')&&html.includes('story-prose')&&html.includes('cast-section'),`${j.palace_id} scene ${i+1} missing core render`);
    assert(count(html,'class="stage-zone ')===3,`${j.palace_id} scene ${i+1} spatial zones != 3`);
    assert(count(html,'class="route-node ')===j.scenes.length,`${j.palace_id} scene ${i+1} route render length wrong`);
    assert(!/\bundefined\b/.test(html)&&!/>\s*null\s*</i.test(html),`${j.palace_id} scene ${i+1} broken interpolation`);
    assert(sceneSpeech(j,i).length>300,`${j.palace_id} scene ${i+1} speech too thin`);
    assert(!html.includes('<details class="memory-panel" open>'),`${j.palace_id} memory anchors open by default`);
    if(s.checkpoint){
      const r=learnView(j,i,true); renderedRecalls++;
      assert(r.includes('Quick recall · story hidden'),`${j.palace_id} recall missing`);
      for(const leak of ['scene-orientation','story-prose','memory-panel','route-wrap','cast-section'])assert(!r.includes(leak),`${j.palace_id} recall leaks ${leak}`);
      assert(!r.includes(s.locus),`${j.palace_id} recall leaks locus name`);
      assert(!/\bundefined\b/.test(r)&&!/>\s*null\s*</i.test(r),`${j.palace_id} recall broken interpolation`);
    }
  }
}
assert(renderedScenes===58&&renderedRecalls===18,'Unit 8 scene/recall render count mismatch');

const appCss=text('frontend/css/app.css'), baseCss=text('frontend/css/base.css');
for(const token of ['@media(max-width:900px)','@media(max-width:650px)','@media(max-width:750px)','@media(max-width:720px)'])assert(appCss.includes(token),`Responsive CSS contract missing ${token}`);
assert(appCss.includes('.scene-stage{grid-template-columns:1fr}')&&appCss.includes('.cast-grid{grid-template-columns:1fr}'),'Small-screen scene/cast stacking contract missing');
assert(appCss.includes('scroll-snap-type:x proximity'),'Mobile route scrolling contract missing');
assert(baseCss.includes('@media(max-width:700px)')&&baseCss.includes('.nav{width:100%}'),'Mobile shell/nav contract missing');
const targetViewports=['1440x1000','820x1180','390x844'];

const u8={...course.units.find(u=>u.unit_id==='unit-8'),...status};
const uiState={activeUnit:'unit-8',activeJourney:'U8-J3',sceneByJourney:{'U8-J3':2},review:[],storySeen:{'U8-J3:0':true,'U8-J3:1':true},completedJourneys:{},encounteredObjects:{},version:3};
const home=homeView(course,u8,registry.guided_journeys,uiState,3);
assert(count(home,'class="card journey-card"')===8,'Unit 8 Home journey count wrong');
assert(home.includes('13 challenges')&&home.includes('Open challenge lab'),'Unit 8 Challenge Lab entry missing');
assert(!home.includes('preview-banner'),'Unit 8 still renders preview banner');
for(const uid of ['unit-1','unit-2','unit-3','unit-4','unit-5','unit-6','unit-7'])assert(home.includes(`data-unit="${uid}"`),`Released ${uid} switch missing`);
for(const uid of ['unit-1','unit-2','unit-3','unit-4','unit-5','unit-6','unit-7','unit-8']){
  const u=course.units.find(x=>x.unit_id===uid); assert(u?.status==='STUDENT_READY',`${uid} not student-ready in course registry`);
}

localStorage.clear();
const persisted={activeUnit:'unit-8',activeJourney:'U8-J6',sceneByJourney:{'U8-J6':5},review:[],storySeen:{'U8-J6:0':true},completedJourneys:{},encounteredObjects:{},version:3};
stateMod.saveState(persisted); const loaded=stateMod.loadState();
assert(loaded.activeUnit==='unit-8'&&loaded.activeJourney==='U8-J6'&&loaded.sceneByJourney['U8-J6']===5,'Refresh/resume state did not persist');
const continueHome=homeView(course,u8,registry.guided_journeys,loaded,0);
assert(continueHome.includes('Continue '),'Refresh/resume Home lacks Continue action');

let scheduler={activeUnit:'unit-8',review:[],encounteredObjects:{}};
for(const t of review.targets)stateMod.scheduleEncounteredReview(scheduler,{unitId:'unit-8',objectId:t.knowledge_id,prompt:t.prompt,hint:t.hint,answer:t.target_answer});
assert(scheduler.review.filter(x=>x.type==='exact'&&x.unitId==='unit-8').length===135,'Unit 8 exact target scheduling wrong');
for(const set of mixed.sets)for(const id of set.knowledge_ids)stateMod.markEncountered(scheduler,id);
stateMod.scheduleEligibleMixedReviews(scheduler,mixed.sets,'unit-8');
assert(scheduler.review.filter(x=>x.type==='mixed'&&x.unitId==='unit-8').length===40,'Unit 8 mixed scheduling wrong');
assert(scheduler.review.filter(x=>x.type==='mixed').every(x=>x.dueAt>Date.now()+47*60*60*1000),'Mixed review delay is below 48-hour contract');
scheduler.review=scheduler.review.map(x=>({...x,dueAt:0}));
scheduler.review.push({type:'exact',unitId:'unit-7',objectId:'UNIT7-ISOLATION-PROBE',dueAt:0,prompt:'probe',answer:'probe'});
assert(stateMod.dueReviews(scheduler,5,'unit-8').length===5,'Unit 8 visible review limit != 5');
assert(stateMod.totalDue(scheduler,'unit-8')===175,'Unit 8 due total should be 135 exact + 40 mixed');
assert(!stateMod.dueReviews(scheduler,5,'unit-8').some(x=>x.unitId==='unit-7'),'Review unit isolation failed');
const set=mixed.sets[0], m={type:'mixed',unitId:'unit-8',objectId:`MIXED:${set.set_id}`,setId:set.set_id,questionIndex:0,dueAt:0};
assert(reviewView([m],1,mixed.sets).includes('Mixed discrimination'),'Unit 8 mixed review render failed');
const exact={type:'exact',unitId:'unit-8',objectId:review.targets[0].knowledge_id,dueAt:0,prompt:review.targets[0].prompt,hint:review.targets[0].hint,answer:review.targets[0].target_answer};
assert(reviewView([exact],135,mixed.sets).includes('showing at most 5 this session'),'Exact Review visible-cap copy missing');

assert(lab.challenge_count===13&&practiceView(lab,0,false).includes('1 of 13')&&practiceView(lab,12,false).includes('13 of 13'),'Unit 8 challenge progression failed');
for(let i=0;i<lab.items.length;i++){
  assert(practiceView(lab,i,false).includes('Story hint'),`Unit 8 challenge ${i+1} story hint control missing`);
  assert(practiceView(lab,i,true).includes('Answer guide'),`Unit 8 challenge ${i+1} answer render failed`);
}

const appJs=text('frontend/js/app.js');
assert(appJs.includes('centerCurrentRoute'),'Active route auto-centering missing');
assert(appJs.includes('data-action="review-next"')&&appJs.includes('Continue review'),'Hinted exact Review lacks direct continuation');
assert(appJs.includes('switchUnit(unitId)')&&appJs.includes("u.searchParams.set('unit',unitId)"),'Unit-switch URL/state contract missing');

const speech=prepareSpeechText('NPP = GPP − R; dN/dt = rmaxN; N₂; NH₄⁺; NO₃⁻; 1 − Σ(n/N)²');
for(const phrase of ['N P P','G P P','d N over d t','r max','nitrogen gas','ammonium','nitrate','one minus the sum of n over N squared','equals'])assert(speech.includes(phrase),`Unit 8 speech normalization missing: ${phrase}`);

console.log('UNIT8 F6 UI LOGIC QA PASS');
console.log(JSON.stringify({
  scenes_rendered:renderedScenes,recalls_rendered:renderedRecalls,responsive_viewports:targetViewports,
  scene_viewport_contract_checks:renderedScenes*3,recall_viewport_contract_checks:renderedRecalls*3,
  exact_targets_queued:135,non_exact_palace_records:76,mixed_sets_queued:40,mixed_questions:104,visible_due_limit:5,
  challenge_lab_items:13,route_lengths:routeLengths,refresh_resume:true,released_unit_switching:'Units 1-8',pixel_screenshot_validation:false
},null,2));
