import fs from 'fs';

global.localStorage={store:new Map(),setItem(k,v){this.store.set(k,String(v))},getItem(k){return this.store.has(k)?this.store.get(k):null},removeItem(k){this.store.delete(k)},clear(){this.store.clear()}};
const stateMod=await import('../frontend/js/state.js');
const {homeView}=await import('../frontend/js/views/home.js');
const {learnView,sceneSpeech}=await import('../frontend/js/views/learn.js');
const {reviewView}=await import('../frontend/js/views/review.js');
const {practiceView}=await import('../frontend/js/views/practice.js');
function read(p){return JSON.parse(fs.readFileSync(new URL('../'+p,import.meta.url),'utf8'))}
function text(p){return fs.readFileSync(new URL('../'+p,import.meta.url),'utf8')}
function assert(x,msg){if(!x)throw new Error(msg)}
function count(hay,needle){return hay.split(needle).length-1}
function ids(html){return [...html.matchAll(/(?:^|\s)id="([^"]+)"/g)].map(m=>m[1])}
function assertUniqueIds(html,label){const list=ids(html),set=new Set(list);assert(list.length===set.size,`${label} contains duplicate ids`)}
function assertNamedButtons(html,label){for(const m of html.matchAll(/<button\b[^>]*>([\s\S]*?)<\/button>/g)){const visible=m[1].replace(/<[^>]+>/g,'').replace(/\s+/g,' ').trim();const tag=m[0];assert(visible||/aria-label=/.test(tag),`${label} contains an unnamed button`)}}
function registryPath(n){return `content/ap-biology/unit-${n}/${n===1?'journeys.json':'journeys-f5.json'}`}
function journeyPath(n,id){return `content/ap-biology/unit-${n}/journeys/${id}.json`}
function reviewPath(n){return `content/ap-biology/unit-${n}/review-manifest-f5.json`}
function mixedPath(n){return `content/ap-biology/unit-${n}/mixed-discrimination-f5.json`}

const course=read('content/ap-biology/course.json');
assert(course.units.length===8,'Course registry does not expose exactly 8 units');
assert(course.units.every(u=>u.status==='STUDENT_READY'),'Every released unit must be student-ready');

let journeyTotal=0,sceneTotal=0,recallTotal=0,challengeTotal=0,exactTotal=0,mixedSetTotal=0,mixedQuestionTotal=0;
for(let n=1;n<=8;n++){
  const reg=read(registryPath(n)),unit={...course.units.find(u=>u.unit_id===`unit-${n}`)};
  assert(reg.guided_journeys.length===reg.journey_count,`Unit ${n} journey registry count mismatch`);
  journeyTotal+=reg.journey_count;sceneTotal+=reg.scene_count;recallTotal+=reg.checkpoint_count;
  const lab=read(`content/ap-biology/unit-${n}/application-lab.json`);challengeTotal+=lab.challenge_count;
  const review=n===1?{target_count:0,targets:[]}:read(reviewPath(n));exactTotal+=review.target_count||0;
  const mixed=n===1?{set_count:0,question_count:0,sets:[]}:read(mixedPath(n));mixedSetTotal+=mixed.set_count||0;mixedQuestionTotal+=mixed.question_count||0;

  const homeState={activeUnit:`unit-${n}`,activeJourney:null,sceneByJourney:{},review:[],storySeen:{},completedJourneys:{},encounteredObjects:{},assistedRecalls:{},assistedReviews:{},version:5};
  const home=homeView(course,unit,reg.guided_journeys,homeState,0,reg.guided_journeys[0]?.palace_id);
  assert(home.includes('id="main-content"')&&home.includes('Course map'),`Unit ${n} Home lacks main/course-map semantics`);
  assert(count(home,'class="card journey-card"')===reg.journey_count,`Unit ${n} Home journey-card count wrong`);
  assertUniqueIds(home,`Unit ${n} Home`);assertNamedButtons(home,`Unit ${n} Home`);

  for(const meta of reg.guided_journeys){
    const j=read(journeyPath(n,meta.palace_id));
    assert(j.scenes.length===meta.scene_count,`${meta.palace_id} scene count mismatch`);
    assert((j.route||[]).length===j.scenes.length,`${meta.palace_id} route length mismatch`);
    const visited=j.scenes.map((_,i)=>i);
    for(let i=0;i<j.scenes.length;i++){
      const s=j.scenes[i],html=learnView(j,i,false,visited);
      assert(html.includes('id="main-content"')&&html.includes('role="progressbar"'),`${meta.palace_id} scene ${i+1} accessibility shell missing`);
      assert(html.includes('scene-orientation')&&html.includes('story-prose'),`${meta.palace_id} scene ${i+1} core content missing`);
      assert(count(html,'class="route-node ')===j.scenes.length,`${meta.palace_id} scene ${i+1} route count wrong`);
      assert(!/\bundefined\b/.test(html)&&!/>\s*null\s*</i.test(html),`${meta.palace_id} scene ${i+1} broken interpolation`);
      assert(sceneSpeech(j,i).length>100,`${meta.palace_id} scene ${i+1} speech text unexpectedly thin`);
      assertUniqueIds(html,`${meta.palace_id} scene ${i+1}`);assertNamedButtons(html,`${meta.palace_id} scene ${i+1}`);
      if(i>0)assert(html.includes('Previous scene'),`${meta.palace_id} scene ${i+1} lacks Previous scene`);
      if(s.checkpoint){
        const recall=learnView(j,i,true,visited);
        assert(recall.includes('Quick recall · story hidden'),`${meta.palace_id} checkpoint ${i+1} missing hidden recall`);
        for(const leak of ['scene-orientation','story-prose','memory-panel','route-wrap','cast-section'])assert(!recall.includes(leak),`${meta.palace_id} recall leaks ${leak}`);
        assert(!recall.includes(s.locus),`${meta.palace_id} recall leaks locus name`);
        assert(recall.includes('aria-live="polite"'),`${meta.palace_id} recall lacks live feedback semantics`);
        assertUniqueIds(recall,`${meta.palace_id} recall ${i+1}`);assertNamedButtons(recall,`${meta.palace_id} recall ${i+1}`);
      }
    }
  }
  for(let i=0;i<lab.items.length;i++){
    const practice=practiceView(lab,i,false),revealed=practiceView(lab,i,true);
    assert(practice.includes(`${i+1} of ${lab.items.length}`),`Unit ${n} challenge ${i+1} progress missing`);
    assert(practice.includes('Story hint')&&revealed.includes('Answer guide'),`Unit ${n} challenge ${i+1} support controls missing`);
    if(i>0)assert(practice.includes('Previous challenge'),`Unit ${n} challenge ${i+1} previous control missing`);
    if(i===lab.items.length-1)assert(practice.includes('Finish challenge lab')&&!practice.includes('Start again'),`Unit ${n} final challenge completion behavior wrong`);
    assertUniqueIds(practice,`Unit ${n} challenge ${i+1}`);assertNamedButtons(practice,`Unit ${n} challenge ${i+1}`);
  }
  for(const t of review.targets||[]){
    const item={type:'exact',unitId:`unit-${n}`,objectId:t.knowledge_id,dueAt:0,prompt:t.prompt,hint:t.hint,answer:t.target_answer};
    const html=reviewView([item],review.target_count,mixed.sets||[]);
    assert(html.includes('Optional retrieval note')&&html.includes('does not automatically grade'),`Unit ${n} exact Review guidance missing`);
    assertUniqueIds(html,`Unit ${n} exact Review`);assertNamedButtons(html,`Unit ${n} exact Review`);
  }
  for(const set of mixed.sets||[]){
    for(let qi=0;qi<(set.questions||[]).length;qi++){
      const item={type:'mixed',unitId:`unit-${n}`,objectId:`MIXED:${set.set_id}`,setId:set.set_id,questionIndex:qi,dueAt:0};
      const html=reviewView([item],1,mixed.sets);
      assert(html.includes('Mixed discrimination'),`${set.set_id} question ${qi+1} mixed Review render missing`);
      assertUniqueIds(html,`${set.set_id} question ${qi+1}`);assertNamedButtons(html,`${set.set_id} question ${qi+1}`);
    }
  }
}
assert(JSON.stringify({journeyTotal,sceneTotal,recallTotal,challengeTotal,exactTotal,mixedSetTotal,mixedQuestionTotal})===JSON.stringify({journeyTotal:58,sceneTotal:448,recallTotal:152,challengeTotal:112,exactTotal:887,mixedSetTotal:220,mixedQuestionTotal:600}),'Whole-course accounting drifted');

// First-run and corrupted-state recovery.
localStorage.clear();let st=stateMod.loadState();assert(st.activeUnit==='unit-1'&&st.activeJourney===null&&st.version===5&&st.courseId==='ap-biology','First-run state does not begin cleanly in AP Biology Unit 1');
localStorage.setItem('memory-palace-v2:progress','{broken json');st=stateMod.loadState();assert(st.activeUnit==='unit-1'&&st.version===5,'Malformed JSON did not recover safely');
localStorage.setItem('memory-palace-v2:progress',JSON.stringify({activeUnit:7,activeJourney:42,sceneByJourney:{X:-9,Y:'oops',Z:3.9},review:'bad',storySeen:['bad'],version:1}));st=stateMod.loadState();assert(st.activeUnit==='unit-1'&&st.activeJourney===null&&st.sceneByJourney.Z===3&&!('X' in st.sceneByJourney)&&Array.isArray(st.review),'Malformed saved-state fields were not normalized');
const throwing={getItem(){throw new Error('blocked')},setItem(){throw new Error('blocked')}};global.localStorage=throwing;st=stateMod.loadState();assert(st.activeUnit==='unit-1','Unavailable localStorage did not recover in memory');assert(stateMod.saveState(st).version===5,'Unavailable localStorage prevented in-memory state use');
global.localStorage={store:new Map(),setItem(k,v){this.store.set(k,String(v))},getItem(k){return this.store.has(k)?this.store.get(k):null},removeItem(k){this.store.delete(k)},clear(){this.store.clear()}};

// Assisted Quick Recall persists across a reload and expires after the two-hour protection window.
st=stateMod.loadState();stateMod.markRecallAssisted(st,'U8-J1','K001');const reloaded=stateMod.loadState();assert(stateMod.wasRecallAssisted(reloaded,'U8-J1','K001'),'Assisted recall marker did not survive reload');reloaded.assistedRecalls['U8-J1:K001']=Date.now()-3*60*60*1000;stateMod.saveState(reloaded);assert(!stateMod.wasRecallAssisted(stateMod.loadState(),'U8-J1','K001'),'Expired assisted recall marker did not clear');

// Review and mixed scheduling remain bounded and unit-isolated.
const u8review=read(reviewPath(8)),u8mixed=read(mixedPath(8));let scheduler={activeUnit:'unit-8',review:[],encounteredObjects:{},assistedRecalls:{},assistedReviews:{}};
for(const t of u8review.targets)stateMod.scheduleEncounteredReview(scheduler,{unitId:'unit-8',objectId:t.knowledge_id,prompt:t.prompt,hint:t.hint,answer:t.target_answer});
for(const set of u8mixed.sets)for(const id of set.knowledge_ids)stateMod.markEncountered(scheduler,id);stateMod.scheduleEligibleMixedReviews(scheduler,u8mixed.sets,'unit-8');
assert(scheduler.review.filter(x=>x.type==='exact').length===135&&scheduler.review.filter(x=>x.type==='mixed').length===40,'Unit 8 scheduling counts drifted');
assert(scheduler.review.filter(x=>x.type==='mixed').every(x=>x.dueAt-Date.now()>=47.9*60*60*1000),'Mixed Review initial delay is below 48 hours');
scheduler.review=scheduler.review.map(x=>({...x,dueAt:0}));scheduler.review.push({type:'exact',unitId:'unit-7',objectId:'isolation',dueAt:0});assert(stateMod.dueReviews(scheduler,5,'unit-8').length===5&&!stateMod.dueReviews(scheduler,5,'unit-8').some(x=>x.unitId==='unit-7'),'Review cap or unit isolation failed');

// Synthetic hostile strings must remain escaped in student-facing renderers.
const hostile='<script>alert("x")</script>&';
const synthetic={palace_id:'X',story_title:hostile,mission:hostile,route_orientation:hostile,route:[{floor:'1',short:hostile,symbol:'<'}],scenes:[{title:hostile,locus:hostile,location_description:hostile,scene_layout:{orientation:hostile,zones:[{position:'left',label:hostile,description:hostile},{position:'center',label:hostile,description:hostile},{position:'right',label:hostile,description:hostile}]},cast:[{kind:hostile,name:hostile,visual:hostile,job:hostile}],story_paragraphs:[hostile],story_beats:[],checkpoint:false}]};
const hostileHtml=learnView(synthetic,0,false,[0]);assert(!hostileHtml.includes('<script>')&&hostileHtml.includes('&lt;script&gt;'),'Dynamic scene content is not safely escaped');
const hostileMixed={set_id:'X',title:hostile,questions:[{prompt:hostile,choices:[hostile,'B'],answer:'B',explanation:hostile}]};const hostileReview=reviewView([{type:'mixed',setId:'X',questionIndex:0}],1,[hostileMixed]);assert(!hostileReview.includes('<script>'),'Dynamic Review content is not safely escaped');

const index=text('frontend/index.html'),base=text('frontend/css/base.css'),css=text('frontend/css/app.css'),app=text('frontend/js/app.js'),api=text('frontend/js/api.js'),learnSrc=text('frontend/js/views/learn.js'),practiceSrc=text('frontend/js/views/practice.js');
for(const token of ['class="skip-link"','href="#main-content"','role="status"','aria-live="polite"'])assert(index.includes(token),`Initial HTML accessibility contract missing ${token}`);
for(const token of [':focus-visible','min-height:44px','prefers-reduced-motion','--muted','--line','--surface-2'])assert(base.includes(token),`Base accessibility/CSS contract missing ${token}`);
for(const token of ['nextUsefulJourney','markRecallAssisted','wasRecallAssisted','review-show-answer','focusMain','centerCurrentRoute','Promise.all','previous-scene','practice-previous','route-scene'])assert(app.includes(token),`Interaction contract missing ${token}`);
assert(learnSrc.includes('Previous scene'),'Learn view lacks Previous scene control');
assert(practiceSrc.includes('Previous challenge')&&practiceSrc.includes('Finish challenge lab'),'Challenge Lab navigation labels missing');
for(const token of ['AbortController','12000','application/json','credentials:\'same-origin\''])assert(api.includes(token),`API hardening contract missing ${token}`);
assert(css.includes('roadmap[open]')&&css.includes('.route-node:not(:disabled)'),'Route/course-map visual state contract missing');

console.log('SITE UX1 GLOBAL UI QA PASS');
console.log(JSON.stringify({units:8,journeys_rendered:journeyTotal,permanent_scenes_rendered:sceneTotal,intentional_quick_recalls:recallTotal,challenge_lab_items:challengeTotal,exact_review_targets:exactTotal,mixed_discrimination_sets:mixedSetTotal,mixed_questions:mixedQuestionTotal,first_run_recovery:true,malformed_state_recovery:true,assisted_recall_persistence:true,dynamic_content_escaping:true},null,2));
