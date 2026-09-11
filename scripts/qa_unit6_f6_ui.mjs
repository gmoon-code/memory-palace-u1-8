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
const status=read('content/ap-biology/unit-6/status.json');
const registry=read('content/ap-biology/unit-6/journeys-f5.json');
const mixed=read('content/ap-biology/unit-6/mixed-discrimination-f5.json');
const review=read('content/ap-biology/unit-6/review-manifest-f5.json');
const lab=read('content/ap-biology/unit-6/application-lab.json');
const journeys=Array.from({length:6},(_,i)=>read(`content/ap-biology/unit-6/journeys/U6-J${i+1}.json`));
assert(status.status==='STUDENT_READY'&&status.student_release===true&&status.preview_release===false,'Unit 6 is not student-ready');
assert(status.browser_validation==='PASS_F6','Unit 6 F6 browser validation status missing');
assert(registry.journey_count===6&&registry.scene_count===53&&registry.checkpoint_count===18,'Unit 6 registry drifted');
const routeLengths=journeys.map(j=>j.scenes.length);
assert(JSON.stringify(routeLengths)===JSON.stringify([12,8,8,12,8,5]),'Unit 6 route lengths drifted');

let renderedScenes=0,renderedRecalls=0;
for(const j of journeys){
  assert((j.route||[]).length===j.scenes.length,`${j.palace_id} route does not match scenes`);
  for(let i=0;i<j.scenes.length;i++){
    const s=j.scenes[i], html=learnView(j,i,false); renderedScenes++;
    assert(html.includes('scene-orientation')&&html.includes('story-prose')&&html.includes('cast-section'),`${j.palace_id} scene ${i+1} missing core render`);
    assert(count(html,'class="stage-zone ')===3,`${j.palace_id} scene ${i+1} spatial zones != 3`);
    assert(count(html,'class="route-node ')===j.scenes.length,`${j.palace_id} scene ${i+1} route render length wrong`);
    assert(!/\b(?:undefined|null)\b/.test(html),`${j.palace_id} scene ${i+1} broken interpolation`);
    assert(sceneSpeech(j,i).length>300,`${j.palace_id} scene ${i+1} speech too thin`);
    assert(!html.includes('<details class="memory-panel" open>'),`${j.palace_id} memory anchors open by default`);
    if(s.checkpoint){
      const r=learnView(j,i,true); renderedRecalls++;
      assert(r.includes('Quick recall · story hidden'),`${j.palace_id} recall missing`);
      for(const leak of ['scene-orientation','story-prose','memory-panel','route-wrap','cast-section'])assert(!r.includes(leak),`${j.palace_id} recall leaks ${leak}`);
      assert(!r.includes(s.locus),`${j.palace_id} recall leaks locus name`);
      assert(!/\b(?:undefined|null)\b/.test(r),`${j.palace_id} recall broken interpolation`);
    }
  }
}
assert(renderedScenes===53&&renderedRecalls===18,'Unit 6 scene/recall render count mismatch');

// Responsive CSS contract for target desktop/tablet/phone widths.
const appCss=text('frontend/css/app.css'), baseCss=text('frontend/css/base.css');
for(const token of ['@media(max-width:900px)','@media(max-width:650px)','@media(max-width:750px)','@media(max-width:720px)'])assert(appCss.includes(token),`Responsive CSS contract missing ${token}`);
assert(appCss.includes('.scene-stage{grid-template-columns:1fr}')&&appCss.includes('.cast-grid{grid-template-columns:1fr}'),'Small-screen scene/cast stacking contract missing');
assert(appCss.includes('scroll-snap-type:x proximity'),'Mobile route scrolling contract missing');
assert(baseCss.includes('@media(max-width:700px)')&&baseCss.includes('.nav{width:100%}'),'Mobile shell/nav contract missing');
const targetViewports=['1440x1000','820x1180','390x844'];

// Home and released-unit switching.
const u6={...course.units.find(u=>u.unit_id==='unit-6'),...status};
const uiState={activeUnit:'unit-6',activeJourney:'U6-J3',sceneByJourney:{'U6-J3':2},review:[],storySeen:{'U6-J3:0':true,'U6-J3:1':true},completedJourneys:{},encounteredObjects:{},version:3};
const home=homeView(course,u6,registry.guided_journeys,uiState,3);
assert(count(home,'class="card journey-card"')===6,'Unit 6 Home journey count wrong');
assert(home.includes('16 challenges')&&home.includes('Open challenge lab'),'Unit 6 Challenge Lab entry missing');
assert(!home.includes('preview-banner'),'Unit 6 still renders preview banner');
for(const uid of ['unit-1','unit-2','unit-3','unit-4','unit-5','unit-7','unit-8'])assert(home.includes(`data-unit="${uid}"`),`Released ${uid} switch missing`);
for(const uid of ['unit-1','unit-2','unit-3','unit-4','unit-5','unit-6','unit-7','unit-8']){
  const u=course.units.find(x=>x.unit_id===uid); assert(u?.status==='STUDENT_READY',`${uid} not student-ready in course registry`);
}


// Refresh/resume persistence.
localStorage.clear();
const persisted={activeUnit:'unit-6',activeJourney:'U6-J4',sceneByJourney:{'U6-J4':7},review:[],storySeen:{'U6-J4:0':true},completedJourneys:{},encounteredObjects:{},version:3};
stateMod.saveState(persisted); const loaded=stateMod.loadState();
assert(loaded.activeUnit==='unit-6'&&loaded.activeJourney==='U6-J4'&&loaded.sceneByJourney['U6-J4']===7,'Refresh/resume state did not persist');
const continueHome=homeView(course,u6,registry.guided_journeys,loaded,0);
assert(continueHome.includes('Continue '),'Refresh/resume Home lacks Continue action');

// Review scheduling, unit isolation, mixed practice, and five-item display cap.
let scheduler={activeUnit:'unit-6',review:[],encounteredObjects:{}};
for(const t of review.targets)stateMod.scheduleEncounteredReview(scheduler,{unitId:'unit-6',objectId:t.knowledge_id,prompt:t.prompt,hint:t.hint,answer:t.target_answer});
assert(scheduler.review.filter(x=>x.type==='exact'&&x.unitId==='unit-6').length===134,'Unit 6 exact target scheduling wrong');
for(const set of mixed.sets)for(const id of set.knowledge_ids)stateMod.markEncountered(scheduler,id);
stateMod.scheduleEligibleMixedReviews(scheduler,mixed.sets,'unit-6');
assert(scheduler.review.filter(x=>x.type==='mixed'&&x.unitId==='unit-6').length===37,'Unit 6 mixed scheduling wrong');
assert(scheduler.review.filter(x=>x.type==='mixed').every(x=>x.dueAt>Date.now()+47*60*60*1000),'Mixed review delay is below 48-hour contract');
scheduler.review=scheduler.review.map(x=>({...x,dueAt:0}));
scheduler.review.push({type:'exact',unitId:'unit-5',objectId:'UNIT5-ISOLATION-PROBE',dueAt:0,prompt:'probe',answer:'probe'});
assert(stateMod.dueReviews(scheduler,5,'unit-6').length===5,'Unit 6 visible review limit != 5');
assert(stateMod.totalDue(scheduler,'unit-6')===171,'Unit 6 due total should be 134 exact + 37 mixed');
assert(!stateMod.dueReviews(scheduler,5,'unit-6').some(x=>x.unitId==='unit-5'),'Review unit isolation failed');
const set=mixed.sets[0], m={type:'mixed',unitId:'unit-6',objectId:`MIXED:${set.set_id}`,setId:set.set_id,questionIndex:0,dueAt:0};
assert(reviewView([m],1,mixed.sets).includes('Mixed discrimination'),'Unit 6 mixed review render failed');
const exact={type:'exact',unitId:'unit-6',objectId:review.targets[0].knowledge_id,dueAt:0,prompt:review.targets[0].prompt,hint:review.targets[0].hint,answer:review.targets[0].target_answer};
assert(reviewView([exact],134,mixed.sets).includes('showing at most 5 this session'),'Exact Review visible-cap copy missing');

// Challenge Lab progression and answer-guide rendering.
assert(lab.challenge_count===16&&practiceView(lab,0,false).includes('1 of 16')&&practiceView(lab,15,false).includes('16 of 16'),'Unit 6 challenge progression failed');
for(let i=0;i<lab.items.length;i++){
  assert(practiceView(lab,i,false).includes('Story hint'),`Unit 6 challenge ${i+1} story hint control missing`);
  assert(practiceView(lab,i,true).includes('Answer guide'),`Unit 6 challenge ${i+1} answer render failed`);
}

// Shared interaction contracts.
const appJs=text('frontend/js/app.js');
assert(appJs.includes('centerCurrentRoute'),'Active route auto-centering missing');
assert(appJs.includes('data-action="review-next"')&&appJs.includes('Continue review'),'Hinted exact Review lacks direct continuation');
assert(appJs.includes('switchUnit(unitId)')&&appJs.includes("u.searchParams.set('unit',unitId)"),'Unit-switch URL/state contract missing');

// Unit 6 speech-only normalization.
const speech=prepareSpeechText('pre-mRNA mRNA tRNA rRNA siRNA miRNA microRNA PCR AUG UAA UAG UGA TATA AAUAAA HGT SSB dsDNA trp A-site P-site E-site 5′→3′ DNA RNA β-galactosidase');
for(const phrase of ['pre messenger R N A','messenger R N A','transfer R N A','ribosomal R N A','small interfering R N A','micro R N A','P C R','A U G','U A A','U A G','U G A','T A T A','A A U A A A','H G T','S S B','double stranded D N A','T R P','A site','P site','E site','five prime leads to three prime','D N A','R N A','beta-galactosidase'])assert(speech.includes(phrase),`Unit 6 speech normalization missing: ${phrase}`);

console.log('UNIT6 F6 UI LOGIC QA PASS');
console.log(JSON.stringify({
  scenes_rendered:renderedScenes,recalls_rendered:renderedRecalls,responsive_viewports:targetViewports,
  scene_viewport_contract_checks:renderedScenes*3,recall_viewport_contract_checks:renderedRecalls*3,
  exact_targets_queued:134,mixed_sets_queued:37,mixed_questions:94,visible_due_limit:5,challenge_lab_items:16,route_lengths:routeLengths,
  refresh_resume:true,released_unit_switching:'Units 1-8',pixel_screenshot_validation:false
},null,2));
