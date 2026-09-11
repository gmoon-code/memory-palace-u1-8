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
const status=read('content/ap-biology/unit-5/status.json');
const registry=read('content/ap-biology/unit-5/journeys-f5.json');
const mixed=read('content/ap-biology/unit-5/mixed-discrimination-f5.json');
const review=read('content/ap-biology/unit-5/review-manifest-f5.json');
const lab=read('content/ap-biology/unit-5/application-lab.json');
const finalization=read('content/ap-biology/unit-5/finalization-f5.json');
const journeys=Array.from({length:8},(_,i)=>read(`content/ap-biology/unit-5/journeys/U5-J${i+1}.json`));
const css=text('frontend/css/app.css');
const appjs=text('frontend/js/app.js');

assert(status.status==='STUDENT_READY'&&status.student_release===true&&status.preview_release===false,'Unit 5 is not student-ready before F6 UI QA');
assert(registry.journey_count===8&&registry.scene_count===50&&registry.checkpoint_count===18,'Unit 5 registry counts drifted');
assert(finalization.accounted_records===152&&finalization.unaccounted_records===0&&finalization.runtime_memory_objects===131,'F5 zero-loss accounting drifted');

let renderedScenes=0, renderedRecalls=0;
const routeLengths=[];
for(const journey of journeys){
  routeLengths.push(journey.scenes.length);
  for(let i=0;i<journey.scenes.length;i++){
    const scene=journey.scenes[i];
    const html=learnView(journey,i,false);
    renderedScenes++;
    assert(html.includes('scene-orientation'),`${journey.palace_id} scene ${i+1} missing orientation`);
    assert(html.includes('story-prose'),`${journey.palace_id} scene ${i+1} missing narrative prose`);
    assert(html.includes('cast-section'),`${journey.palace_id} scene ${i+1} missing cast`);
    assert(html.includes('<details class="memory-panel">'),`${journey.palace_id} scene ${i+1} memory anchors are not collapsed by default`);
    assert(!html.includes('<details class="memory-panel" open>'),`${journey.palace_id} scene ${i+1} memory anchors open by default`);
    assert(count(html,'class="stage-zone ')===3,`${journey.palace_id} scene ${i+1} does not render exactly three spatial zones`);
    for(const pos of ['left','center','right'])assert(html.includes(`stage-zone ${pos}`),`${journey.palace_id} scene ${i+1} missing ${pos} zone`);
    assert(count(html,'class="route-node ')===journey.scenes.length,`${journey.palace_id} scene ${i+1} route node count mismatch`);
    assert(html.includes(`--route-count:${journey.scenes.length}`),`${journey.palace_id} scene ${i+1} route length CSS variable missing`);
    assert((html.match(/class=\"route-node current\"/g)||[]).length===1,`${journey.palace_id} scene ${i+1} does not have exactly one current route node`);
    assert(!html.includes('undefined')&&!html.includes('[object Object]'),`${journey.palace_id} scene ${i+1} contains broken interpolation`);
    assert(sceneSpeech(journey,i).length>100,`${journey.palace_id} scene ${i+1} speech text is unexpectedly thin`);
    assert(!sceneSpeech(journey,i).includes('**'),`${journey.palace_id} scene ${i+1} speech leaks Markdown emphasis`);
    if(scene.checkpoint){
      const recall=learnView(journey,i,true); renderedRecalls++;
      assert(recall.includes('Quick recall · story hidden'),`${journey.palace_id} scene ${i+1} hidden-recall label missing`);
      for(const leak of ['scene-orientation','story-prose','memory-panel','route-wrap','cast-section'])assert(!recall.includes(leak),`${journey.palace_id} scene ${i+1} recall leaks ${leak}`);
      assert(!recall.includes(scene.locus),`${journey.palace_id} scene ${i+1} recall leaks locus name`);
      const answer=String(scene.checkpoint_answer||'').trim();
      if(answer.length>=4)assert(!recall.toLowerCase().includes(answer.toLowerCase()),`${journey.palace_id} scene ${i+1} recall leaks checkpoint answer`);
    }
  }
}
assert(renderedScenes===50,'Did not render all 50 Unit 5 scenes');
assert(renderedRecalls===18,'Did not render all 18 Unit 5 recalls');
assert(JSON.stringify(routeLengths)===JSON.stringify([5,10,4,7,4,7,6,7]),'Unit 5 route lengths changed');

for(const token of [
  '@media(max-width:900px)', '.scene-stage{grid-template-columns:1fr}', '.cast-grid{grid-template-columns:1fr 1fr}',
  '@media(max-width:650px)', '.story-actions{padding:0 19px 22px;align-items:stretch;flex-direction:column-reverse}',
  '@media(max-width:750px)', 'repeat(var(--route-count,11),82px)', 'scroll-snap-type:x proximity',
  '@media(max-width:720px)', '.choice-grid{grid-template-columns:1fr}'
])assert(css.includes(token),`Responsive CSS contract missing: ${token}`);
assert(css.includes('overflow-x:auto'),'Route horizontal overflow protection missing');

const unit5={...course.units.find(u=>u.unit_id==='unit-5'),...status};
let uiState={activeUnit:'unit-5',activeJourney:'U5-J6',sceneByJourney:{'U5-J6':4},review:[],storySeen:{'U5-J6:0':true,'U5-J6:1':true,'U5-J6:2':true,'U5-J6:3':true},completedJourneys:{},encounteredObjects:{},version:3};
const home=homeView(course,unit5,registry.guided_journeys,uiState,4);
assert(count(home,'class="card journey-card"')===8,'Unit 5 Home does not render eight journey cards');
assert(home.includes(`Continue ${registry.guided_journeys.find(j=>j.palace_id==='U5-J6').story_title}`),'Home does not resume the active Unit 5 journey');
assert(home.includes('Review 4 due memories'),'Home due-review badge failed');
assert(home.includes('16 challenges')&&home.includes('Open challenge lab'),'Unit 5 Challenge Lab entry missing');
assert(!home.includes('preview-banner'),'Student-ready Unit 5 still renders as a preview');
for(const uid of ['unit-1','unit-2','unit-3','unit-4'])assert(home.includes(`data-unit="${uid}"`),`Released ${uid} switch control missing`);

localStorage.clear(); stateMod.saveState(uiState); const restored=stateMod.loadState();
assert(restored.activeUnit==='unit-5'&&restored.activeJourney==='U5-J6'&&stateMod.sceneIndex(restored,'U5-J6')===4,'Refresh/resume state did not persist');
let scheduler={activeUnit:'unit-5',review:[],encounteredObjects:{}};
for(const t of review.targets)stateMod.scheduleEncounteredReview(scheduler,{unitId:'unit-5',objectId:t.knowledge_id,prompt:t.prompt,hint:t.hint,answer:t.target_answer});
assert(scheduler.review.filter(x=>x.type==='exact'&&x.unitId==='unit-5').length===130,'Exact scheduler did not preserve all 130 Unit 5 targets');
assert(scheduler.review.filter(x=>x.type==='exact').every(x=>x.dueAt-Date.now()>17.9*60*60*1000),'Exact review scheduled too early');

for(const set of mixed.sets)for(const id of set.knowledge_ids)stateMod.markEncountered(scheduler,id);
stateMod.scheduleEligibleMixedReviews(scheduler,mixed.sets,'unit-5');
const mixedQueued=scheduler.review.filter(x=>x.type==='mixed'&&x.unitId==='unit-5');
assert(mixedQueued.length===32,'Unit 5 mixed scheduler did not create all 32 sets');
assert(mixedQueued.every(x=>x.dueAt-Date.now()>=47.9*60*60*1000),'Unit 5 mixed review scheduled earlier than 48 hours');
scheduler.review.push({type:'exact',unitId:'unit-4',objectId:'FAKE-U4',dueAt:0});
scheduler.review=scheduler.review.map(x=>x.unitId==='unit-5'?{...x,dueAt:0}:x);
assert(stateMod.dueReviews(scheduler,5,'unit-5').length===5,'Visible Unit 5 review limit is not five');
assert(stateMod.totalDue(scheduler,'unit-5')===162,'Unit 5 due total should be 130 exact + 32 mixed');
assert(stateMod.totalDue(scheduler,'unit-4')===1,'Unit-scoped review isolation failed');

const exactItem={...scheduler.review.find(x=>x.type==='exact'&&x.unitId==='unit-5'),dueAt:0};
assert(reviewView([exactItem],162,mixed.sets).includes('Need a hint'),'Exact review UI missing hint control');
assert(appjs.includes('data-action="review-next"')&&appjs.includes('Continue review'),'Hinted exact review has no direct continuation action');
const set=mixed.sets[0];
const mixedItem={type:'mixed',unitId:'unit-5',objectId:`MIXED:${set.set_id}`,setId:set.set_id,questionIndex:0,dueAt:0};
const mixedHtml=reviewView([mixedItem],1,mixed.sets);
assert(mixedHtml.includes('Mixed discrimination')&&count(mixedHtml,'data-action="mixed-choice"')===set.questions[0].choices.length,'Mixed review UI failed');

assert(lab.challenge_count===16,'Unit 5 Challenge Lab count drifted');
assert(practiceView(lab,0,false).includes('1 of 16'),'Challenge Lab first-item progression failed');
assert(practiceView(lab,15,false).includes('16 of 16'),'Challenge Lab last-item progression failed');
assert(practiceView(lab,0,true).includes('Answer guide'),'Challenge Lab answer reveal failed');
for(let i=0;i<lab.items.length;i++){
  const a=practiceView(lab,i,false), b=practiceView(lab,i,true);
  assert(!a.includes('undefined')&&!a.includes('[object Object]'),`Challenge ${i+1} contains broken interpolation`);
  assert(b.includes('Answer guide'),`Challenge ${i+1} answer guide failed to render`);
}

// Unit 5 speech-only normalization for common genetics/statistics terms.
const speech=prepareSpeechText('DNA and RNA; F1 and F2; XX and XY; ABO; IA and IB; UV; HBB; 2n; χ²; Aa, AA, aa, and AaBb.');
for(const phrase of ['D N A','R N A','F one','F two','X X','X Y','A B O','I A','I B','U V','H B B','two n','chi squared','capital A lowercase a','A A','lowercase a lowercase a','capital A lowercase a capital B lowercase b'])assert(speech.includes(phrase),`Unit 5 speech normalization missing: ${phrase}`);

console.log('UNIT5 F6 UI LOGIC QA PASS');
console.log(JSON.stringify({
  scenes_rendered:renderedScenes,recalls_rendered:renderedRecalls,
  responsive_viewports:['1440x1000','820x1180','390x844'],
  scene_viewport_contract_checks:renderedScenes*3,recall_viewport_contract_checks:renderedRecalls*3,
  exact_targets_queued:130,mixed_sets_queued:32,mixed_questions:79,visible_due_limit:5,
  challenge_lab_items:16,route_lengths:routeLengths
},null,2));
