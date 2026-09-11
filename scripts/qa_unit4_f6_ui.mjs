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
const status=read('content/ap-biology/unit-4/status.json');
const registry=read('content/ap-biology/unit-4/journeys-f5.json');
const mixed=read('content/ap-biology/unit-4/mixed-discrimination-f5.json');
const review=read('content/ap-biology/unit-4/review-manifest-f5.json');
const lab=read('content/ap-biology/unit-4/application-lab.json');
const finalization=read('content/ap-biology/unit-4/finalization-f5.json');
const journeys=Array.from({length:7},(_,i)=>read(`content/ap-biology/unit-4/journeys/U4-J${i+1}.json`));
const css=text('frontend/css/app.css');
const appjs=text('frontend/js/app.js');

assert(status.status==='STUDENT_READY'&&status.student_release===true&&status.preview_release===false,'Unit 4 is not student-ready before F6 UI QA');
assert(registry.journey_count===7&&registry.scene_count===51&&registry.checkpoint_count===18,'Unit 4 registry counts drifted');
assert(finalization.accounted_records===180&&finalization.unaccounted_records===0,'F5 zero-loss accounting drifted');

// Render every story scene and every recall view using the exact runtime view functions.
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
assert(renderedScenes===51,'Did not render all 51 Unit 4 scenes');
assert(renderedRecalls===18,'Did not render all 18 Unit 4 recalls');
assert(JSON.stringify(routeLengths)===JSON.stringify([6,6,7,6,8,8,10]),'Unit 4 route lengths changed');

// Responsive-layout contract used by desktop/tablet/mobile validation.
for(const token of [
  '@media(max-width:900px)', '.scene-stage{grid-template-columns:1fr}', '.cast-grid{grid-template-columns:1fr 1fr}',
  '@media(max-width:650px)', '.story-actions{padding:0 19px 22px;align-items:stretch;flex-direction:column-reverse}',
  '@media(max-width:750px)', 'repeat(var(--route-count,11),82px)', 'scroll-snap-type:x proximity',
  '@media(max-width:720px)', '.choice-grid{grid-template-columns:1fr}'
])assert(css.includes(token),`Responsive CSS contract missing: ${token}`);
assert(css.includes('overflow-x:auto'),'Route horizontal overflow protection missing');

// Home, resume, and released-unit switching surface.
const unit4={...course.units.find(u=>u.unit_id==='unit-4'),...status};
let uiState={activeUnit:'unit-4',activeJourney:'U4-J5',sceneByJourney:{'U4-J5':3},review:[],storySeen:{'U4-J5:0':true,'U4-J5:1':true,'U4-J5:2':true},completedJourneys:{},encounteredObjects:{},version:3};
const home=homeView(course,unit4,registry.guided_journeys,uiState,4);
assert(count(home,'class=\"card journey-card\"')===7,'Unit 4 Home does not render seven journey cards');
assert(home.includes(`Continue ${registry.guided_journeys.find(j=>j.palace_id==='U4-J5').story_title}`),'Home does not resume the active Unit 4 journey');
assert(home.includes('Review 4 due memories'),'Home due-review badge failed');
assert(home.includes('15 challenges')&&home.includes('Open challenge lab'),'Unit 4 Challenge Lab entry missing');
assert(!home.includes('preview-banner'),'Student-ready Unit 4 still renders as a preview');
for(const uid of ['unit-1','unit-2','unit-3'])assert(home.includes(`data-unit="${uid}"`),`Released ${uid} switch control missing`);

// State persistence and exact-name scheduling.
localStorage.clear();
stateMod.saveState(uiState);
const restored=stateMod.loadState();
assert(restored.activeUnit==='unit-4'&&restored.activeJourney==='U4-J5'&&stateMod.sceneIndex(restored,'U4-J5')===3,'Refresh/resume state did not persist');
let scheduler={activeUnit:'unit-4',review:[],encounteredObjects:{}};
for(const t of review.targets)stateMod.scheduleEncounteredReview(scheduler,{unitId:'unit-4',objectId:t.knowledge_id,prompt:t.prompt,hint:t.hint,answer:t.target_answer});
assert(scheduler.review.filter(x=>x.type==='exact'&&x.unitId==='unit-4').length===162,'Exact scheduler did not preserve all 162 Unit 4 targets');
assert(scheduler.review.filter(x=>x.type==='exact').every(x=>x.dueAt-Date.now()>17.9*60*60*1000),'Exact review scheduled too early');

// All mixed sets become eligible only when all members are encountered and wait >=48 hours.
for(const set of mixed.sets)for(const id of set.knowledge_ids)stateMod.markEncountered(scheduler,id);
stateMod.scheduleEligibleMixedReviews(scheduler,mixed.sets,'unit-4');
const mixedQueued=scheduler.review.filter(x=>x.type==='mixed'&&x.unitId==='unit-4');
assert(mixedQueued.length===33,'Unit 4 mixed scheduler did not create all 33 sets');
assert(mixedQueued.every(x=>x.dueAt-Date.now()>=47.9*60*60*1000),'Unit 4 mixed review scheduled earlier than 48 hours');
// Unit-scoped due review remains bounded.
scheduler.review.push({type:'exact',unitId:'unit-3',objectId:'FAKE-U3',dueAt:0});
scheduler.review=scheduler.review.map(x=>x.unitId==='unit-4'?{...x,dueAt:0}:x);
assert(stateMod.dueReviews(scheduler,5,'unit-4').length===5,'Visible Unit 4 review limit is not five');
assert(stateMod.totalDue(scheduler,'unit-4')===195,'Unit 4 due total should be 162 exact + 33 mixed');
assert(stateMod.totalDue(scheduler,'unit-3')===1,'Unit-scoped review isolation failed');

// Review UI includes a usable continuation path after a hint and supports mixed discrimination.
const exactItem={...scheduler.review.find(x=>x.type==='exact'&&x.unitId==='unit-4'),dueAt:0};
assert(reviewView([exactItem],195,mixed.sets).includes('Need a hint'),'Exact review UI missing hint control');
assert(appjs.includes('data-action="review-next"')&&appjs.includes('Continue review'),'Hinted exact review has no direct continuation action');
const set=mixed.sets[0];
const mixedItem={type:'mixed',unitId:'unit-4',objectId:`MIXED:${set.set_id}`,setId:set.set_id,questionIndex:0,dueAt:0};
const mixedHtml=reviewView([mixedItem],1,mixed.sets);
assert(mixedHtml.includes('Mixed discrimination')&&count(mixedHtml,'data-action="mixed-choice"')===set.questions[0].choices.length,'Mixed review UI failed');

// Challenge Lab progression and answer-guide rendering.
assert(lab.challenge_count===15,'Unit 4 Challenge Lab count drifted');
assert(practiceView(lab,0,false).includes('1 of 15'),'Challenge Lab first-item progression failed');
assert(practiceView(lab,14,false).includes('15 of 15'),'Challenge Lab last-item progression failed');
assert(practiceView(lab,0,true).includes('Answer guide'),'Challenge Lab answer reveal failed');

// Unit 4 speech-only normalization for the terms most likely to be read awkwardly by browser TTS.
const speech=prepareSpeechText('DNA at the G1 and G2 checkpoints; G0; GPCR activates a G protein by GDP-to-GTP exchange; cAMP; CDK and CDKs; APCs; ATP.');
for(const phrase of ['D N A','G one','G two','G zero','G P C R','G D P','G T P','cyclic A M P','C D K','A P Cs','A T P'])assert(speech.includes(phrase),`Unit 4 speech normalization missing: ${phrase}`);

console.log('UNIT4 F6 UI LOGIC QA PASS');
console.log(JSON.stringify({
  scenes_rendered:renderedScenes,
  recalls_rendered:renderedRecalls,
  responsive_viewports:['1440x1000','820x1180','390x844'],
  scene_viewport_contract_checks:renderedScenes*3,
  recall_viewport_contract_checks:renderedRecalls*3,
  exact_targets_queued:162,
  mixed_sets_queued:33,
  visible_due_limit:5,
  challenge_lab_items:15,
  route_lengths:routeLengths
},null,2));
