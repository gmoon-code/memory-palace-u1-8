import {api,defaultCourseId} from './api.js';
import {loadState,saveState,sceneIndex,setSceneIndex,markSeen,markJourneyComplete,markEncountered,scheduleReview,scheduleEncounteredReview,scheduleEligibleMixedReviews,dueReviews,totalDue,completeReview,completeMixedReview,markRecallAssisted,wasRecallAssisted,clearRecallAssisted,markReviewAssisted,wasReviewAssisted,clearReviewAssisted} from './state.js';
import {speak,stopSpeech} from './audio.js';
import {coursesView} from './views/courses.js';
import {homeView} from './views/home.js';
import {learnView,sceneSpeech} from './views/learn.js';
import {reviewView} from './views/review.js';
import {practiceView} from './views/practice.js';

const root=document.querySelector('#app');
const state=loadState();
let registry={courses:[]},selectedCourseId=null,course=null,unit=null,journeys=[],activeJourney=null,applicationLab={items:[]},reviewManifest={targets:[]},mixedData={sets:[]};
let practiceIndex=0,practiceRevealed=false,view='courses',recallOpen=false;

function esc(v=''){return String(v).replace(/[&<>'\"]/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','\"':'&quot;'}[ch]))}
function shell(content){
 const courseTitle=course?.course_title||course?.title||'';
 if(view==='courses'){
   return `<div class="shell"><header class="topbar"><div class="brand">The Story Method</div><nav class="nav" aria-label="Primary"><button data-nav="courses" class="active" aria-current="page">Courses</button></nav></header>${content}</div>`;
 }
 return `<div class="shell"><header class="topbar"><div class="brand">The Story Method <span>${esc(courseTitle)}</span></div><nav class="nav" aria-label="Primary"><button data-nav="courses">Courses</button><button data-nav="home" ${view==='home'?'class="active" aria-current="page"':''}>Home</button><button data-nav="learn" ${view==='learn'?'class="active" aria-current="page"':''}>Learn</button><button data-nav="review" ${view==='review'?'class="active" aria-current="page"':''}>Review</button></nav></header>${content}</div>`;
}
function currentCourseId(){return selectedCourseId||defaultCourseId}
function currentUnitId(){return state.activeUnit||'unit-1'}
function targetMap(){return new Map((reviewManifest?.targets||[]).map(x=>[x.knowledge_id,x]))}
function seenCount(j){return Array.from({length:Number(j?.scene_count||0)},(_,i)=>state.storySeen?.[`${j.palace_id}:${i}`]).filter(Boolean).length}
function journeyInProgress(j){return !state.completedJourneys?.[j.palace_id]&&(sceneIndex(state,j.palace_id)>0||seenCount(j)>0)}
function nextUsefulJourney(){
 const active=journeys.find(j=>j.palace_id===state.activeJourney);
 if(active&&!state.completedJourneys?.[active.palace_id])return active;
 return journeys.find(j=>journeyInProgress(j))||journeys.find(j=>!state.completedJourneys?.[j.palace_id])||active||journeys[0]||null;
}
function nextIncompleteAfter(id){
 const start=Math.max(0,journeys.findIndex(j=>j.palace_id===id));
 for(let offset=1;offset<=journeys.length;offset++){
   const j=journeys[(start+offset)%journeys.length];
   if(j&&!state.completedJourneys?.[j.palace_id])return j;
 }
 return journeys.find(j=>j.palace_id===id)||journeys[0]||null;
}
function visitedIndexes(journey){
 const out=[];for(let i=0;i<(journey?.scenes?.length||0);i++)if(state.storySeen?.[`${journey.palace_id}:${i}`]||i===sceneIndex(state,journey.palace_id))out.push(i);return out;
}
function focusMain(){
 const main=document.getElementById('main-content');if(!main)return;
 try{window.scrollTo({top:0,left:0,behavior:'auto'})}catch{window.scrollTo?.(0,0)}
 requestAnimationFrame(()=>main.focus({preventScroll:true}));
}
function focusStory(){
 requestAnimationFrame(()=>requestAnimationFrame(()=>{
   const story=document.querySelector('.narrative-section');if(!story)return;
   const heading=story.querySelector('.section-heading h3');
   const top=story.getBoundingClientRect().top+window.scrollY-12;
   try{window.scrollTo({top:Math.max(0,top),left:0,behavior:'auto'})}catch{window.scrollTo?.(0,Math.max(0,top))}
   if(heading){heading.setAttribute('tabindex','-1');heading.focus({preventScroll:true})}
 }));
}
function centerCurrentRoute(){
 const strip=document.querySelector('.route-strip'),current=strip?.querySelector('.route-node.current');if(!strip||!current)return;
 const target=current.offsetLeft-(strip.clientWidth-current.clientWidth)/2;strip.scrollLeft=Math.max(0,target);
}
function render({focus=false}={}){
 if(view==='courses'){
   document.title='The Story Method · Science Courses';
   root.innerHTML=shell(coursesView(registry,state));
 }else{
   document.title=`The Story Method · ${course?.course_title||course?.title||'Science'}`;
   const recommended=nextUsefulJourney();
   if(view==='home')root.innerHTML=shell(homeView(course,unit,journeys,state,totalDue(state,currentUnitId()),recommended?.palace_id));
   else if(view==='learn'&&activeJourney)root.innerHTML=shell(learnView(activeJourney,sceneIndex(state,activeJourney.palace_id),recallOpen,visitedIndexes(activeJourney)));
   else if(view==='review')root.innerHTML=shell(reviewView(dueReviews(state,5,currentUnitId()),totalDue(state,currentUnitId()),mixedData?.sets||[]));
   else if(view==='practice')root.innerHTML=shell(practiceView(applicationLab,practiceIndex,practiceRevealed));
   else{view='home';root.innerHTML=shell(homeView(course,unit,journeys,state,totalDue(state,currentUnitId()),recommended?.palace_id));}
 }
 bind();centerCurrentRoute();if(focus)focusMain();
}
async function loadUnit(unitId){
 const courseId=currentCourseId();
 const [unitData,journeyData,labData,reviewData,mixedReviewData]=await Promise.all([api.unit(courseId,unitId),api.journeys(courseId,unitId),api.applicationLab(courseId,unitId),api.reviewManifest(courseId,unitId),api.mixedDiscrimination(courseId,unitId)]);
 unit=unitData;journeys=Array.isArray(journeyData?.guided_journeys)?journeyData.guided_journeys:[];applicationLab=labData||{items:[]};reviewManifest=reviewData||{targets:[]};mixedData=mixedReviewData||{sets:[]};state.activeUnit=unitId;
 const useful=nextUsefulJourney();state.activeJourney=useful?.palace_id||null;activeJourney=null;saveState(state);
}
function releasedUnitIds(){return new Set((course?.units||[]).filter(u=>u.status==='STUDENT_READY').map(u=>u.unit_id))}
function safeRequestedUnit(requested){const valid=releasedUnitIds();if(requested&&valid.has(requested))return requested;if(valid.has(state.activeUnit))return state.activeUnit;if(valid.has('unit-1'))return'unit-1';return [...valid][0]||'unit-1'}
function syncCourseUnitUrl(courseId,unitId){
 const u=new URL(location.href);u.searchParams.set('course',courseId);
 if(unitId==='unit-1')u.searchParams.delete('unit');else u.searchParams.set('unit',unitId);
 history.replaceState({},'',u);
}
function syncCoursesUrl(){const u=new URL(location.href);u.search='';u.hash='';history.replaceState({},'',u)}
async function openCourse(courseId,requestedUnit=null){
 const available=(registry?.courses||[]).find(c=>c.course_id===courseId&&c.student_visible!==false&&c.status==='available');
 if(!available)return;
 stopSpeech();recallOpen=false;practiceRevealed=false;activeJourney=null;
 selectedCourseId=courseId;
 try{
   course=await api.course(courseId);
   const unitId=safeRequestedUnit(requestedUnit);
   await loadUnit(unitId);
   view='home';syncCourseUnitUrl(courseId,unitId);render({focus:true});
 }catch(err){showError(err,()=>openCourse(courseId,requestedUnit))}
}
function goCourses(){
 stopSpeech();recallOpen=false;practiceRevealed=false;activeJourney=null;view='courses';
 selectedCourseId=null;course=null;unit=null;journeys=[];syncCoursesUrl();render({focus:true});
}
async function switchUnit(unitId){
 if(!releasedUnitIds().has(unitId))return;
 stopSpeech();recallOpen=false;view='home';practiceRevealed=false;
 try{await loadUnit(unitId);syncCourseUnitUrl(currentCourseId(),unitId);render({focus:true})}catch(err){showError(err,()=>switchUnit(unitId))}
}
async function openJourney(id=null){
 const selected=journeys.find(j=>j.palace_id===(id||nextUsefulJourney()?.palace_id));if(!selected)return;
 try{activeJourney=await api.journey(currentCourseId(),currentUnitId(),selected.palace_id);state.activeJourney=selected.palace_id;saveState(state);view='learn';recallOpen=false;stopSpeech();render({focus:true})}catch(err){showError(err,()=>openJourney(selected.palace_id))}
}
function currentScene(){if(!activeJourney)return null;return activeJourney.scenes[sceneIndex(state,activeJourney.palace_id)]||activeJourney.scenes[0]}
async function recallData(objectId){
 const scene=currentScene(),beat=(scene?.story_beats||[]).find(x=>x.object_id===objectId),obj=await api.object(currentCourseId(),currentUnitId(),objectId);
 return{obj,hint:scene?.checkpoint_hint||beat?.hint||obj.mnemonic_actor_or_object||obj.phonological_keyword||'Return to the defining action in the scene.',answer:scene?.checkpoint_answer||beat?.term||obj.canonical_term,prompt:scene?.checkpoint_prompt||`What term or idea matches this scientific meaning?`};
}
async function showRecallHint(objectId){
 const data=await recallData(objectId);markRecallAssisted(state,activeJourney?.palace_id,objectId);
 const host=document.getElementById('recallHint');if(host)host.innerHTML=`<div class="hint"><span class="eyebrow">One story hint</span><p>${esc(data.hint)}</p><button class="secondary" data-action="recall-answer" data-object="${esc(objectId)}">Show answer</button></div>`;
 document.querySelector('[data-action="recall-answer"]')?.addEventListener('click',()=>showRecallAnswer(objectId,data));
}
function showRecallAnswer(objectId,data){const host=document.getElementById('recallHint');if(host)host.innerHTML=`<div class="hint"><span class="eyebrow">Answer</span><p><strong>${esc(data.answer)}</strong></p><p class="muted">This attempt stays marked as assisted.</p></div>`}
function scheduleSceneMemories(scene){
 const unitId=currentUnitId(),map=targetMap();for(const beat of(scene?.story_beats||[]))markEncountered(state,beat.object_id);
 const beats=(scene?.story_beats||[]).filter(b=>b.exact_name),targets=beats.length?beats:(scene?.story_beats||[]).slice(0,1);
 targets.forEach(beat=>{const locked=map.get(beat.object_id);scheduleEncounteredReview(state,{unitId,objectId:beat.object_id,journeyId:activeJourney.palace_id,prompt:locked?.prompt||`What term or idea matches this scientific meaning? ${beat.science}`,hint:locked?.hint||beat.hint||'Picture the defining action from the story.',answer:locked?.target_answer||beat.term})});
 scheduleEligibleMixedReviews(state,mixedData?.sets||[],unitId);saveState(state);
}
function goHome(){view='home';recallOpen=false;stopSpeech();render({focus:true})}
function goToScene(index){
 if(!activeJourney)return;const current=sceneIndex(state,activeJourney.palace_id),next=Math.max(0,Math.min(Number(index)||0,activeJourney.scenes.length-1));
 if(next!==current){markSeen(state,activeJourney.palace_id,current);setSceneIndex(state,activeJourney.palace_id,next)}recallOpen=false;stopSpeech();render({focus:false});focusStory();
}
async function skipRecallAndContinue(){
 const scene=currentScene(),objectId=scene?.checkpoint_object_id;if(objectId){try{const data=await recallData(objectId);scheduleReview(state,{unitId:currentUnitId(),objectId:data.obj.memory_object_id,journeyId:activeJourney.palace_id,prompt:data.prompt,hint:data.hint,answer:data.answer},false)}catch{/* The normal story scheduler will still queue the memory. */}clearRecallAssisted(state,activeJourney.palace_id,objectId)}nextScene();
}
function previousScene(){if(!activeJourney)return;const i=sceneIndex(state,activeJourney.palace_id);if(i<=0)return;markSeen(state,activeJourney.palace_id,i);setSceneIndex(state,activeJourney.palace_id,i-1);recallOpen=false;stopSpeech();render({focus:false});focusStory()}
function nextScene(){
 if(!activeJourney)return;const id=activeJourney.palace_id,i=sceneIndex(state,id),scene=activeJourney.scenes[i];markSeen(state,id,i);scheduleSceneMemories(scene);
 if(scene?.checkpoint_object_id)clearRecallAssisted(state,id,scene.checkpoint_object_id);
 if(i>=activeJourney.scenes.length-1){markJourneyComplete(state,id);setSceneIndex(state,id,0);const next=nextIncompleteAfter(id);state.activeJourney=next?.palace_id||id;saveState(state);view='home';recallOpen=false;stopSpeech();render({focus:true});return}
 setSceneIndex(state,id,i+1);recallOpen=false;stopSpeech();render({focus:false});focusStory();
}
function exactDue(objectId){return dueReviews(state,5,currentUnitId()).find(i=>i.objectId===objectId)}
function showReviewHint(objectId){
 const x=exactDue(objectId);if(!x)return;markReviewAssisted(state,objectId);const host=document.getElementById('reviewFeedback');if(host)host.innerHTML=`<div class="hint"><span class="eyebrow">Hint</span><p>${esc(x.hint||'Return to the defining action in the story.')}</p><div class="row"><button class="secondary" data-action="review-after-hint" data-object="${esc(objectId)}">I got it from the hint</button><button class="ghost" data-action="review-show-answer" data-object="${esc(objectId)}">Show answer</button></div></div>`;
 document.querySelector('[data-action="review-after-hint"]')?.addEventListener('click',()=>finishExactReview(objectId,false));document.querySelector('[data-action="review-show-answer"]')?.addEventListener('click',()=>showReviewAnswer(objectId));
}
function showReviewAnswer(objectId){const x=exactDue(objectId);if(!x)return;markReviewAssisted(state,objectId);const host=document.getElementById('reviewFeedback');if(host)host.innerHTML=`<div class="hint"><span class="eyebrow">Answer</span><p><strong>${esc(x.answer||'')}</strong></p><button class="primary" data-action="review-next" data-object="${esc(objectId)}">Continue review</button></div>`;document.querySelector('[data-action="review-next"]')?.addEventListener('click',()=>finishExactReview(objectId,false))}
function finishExactReview(objectId,remembered){const assisted=wasReviewAssisted(state,objectId);completeReview(state,objectId,remembered&&!assisted);clearReviewAssisted(state,objectId);render({focus:true})}
function bind(){
 document.querySelectorAll('[data-nav]').forEach(b=>b.onclick=()=>{const v=b.dataset.nav;if(v==='courses')goCourses();else if(v==='learn')openJourney(nextUsefulJourney()?.palace_id);else if(v==='home')goHome();else{view='review';recallOpen=false;stopSpeech();render({focus:true})}});
 document.querySelectorAll('[data-action="open-course"]').forEach(b=>b.onclick=()=>openCourse(b.dataset.course));
 document.querySelectorAll('[data-action="home"]').forEach(b=>b.onclick=goHome);
 document.querySelectorAll('[data-action="learn"]').forEach(b=>b.onclick=()=>openJourney(b.dataset.id));
 document.querySelectorAll('[data-action="switch-unit"]').forEach(b=>b.onclick=()=>switchUnit(b.dataset.unit));
 document.querySelectorAll('[data-action="route-scene"]').forEach(b=>b.onclick=()=>goToScene(Number(b.dataset.index)));
 document.querySelector('[data-action="previous-scene"]')?.addEventListener('click',previousScene);
 document.querySelectorAll('[data-action="review"]').forEach(b=>b.onclick=()=>{view='review';recallOpen=false;stopSpeech();render({focus:true})});
 document.querySelectorAll('[data-action="practice"]').forEach(b=>b.onclick=()=>{practiceIndex=0;practiceRevealed=false;view='practice';stopSpeech();render({focus:true})});
 document.querySelector('[data-action="practice-reveal"]')?.addEventListener('click',()=>{practiceRevealed=true;render()});
 document.querySelector('[data-action="practice-hint"]')?.addEventListener('click',()=>{const x=applicationLab?.items?.[practiceIndex],host=document.getElementById('practiceHint');if(host)host.innerHTML=`<div class="hint"><span class="eyebrow">Story hint</span><p>${esc(x?.story_hint||'Return to the relevant story scene.')}</p></div>`});
 document.querySelector('[data-action="practice-previous"]')?.addEventListener('click',()=>{practiceIndex=Math.max(0,practiceIndex-1);practiceRevealed=false;render({focus:true})});
 document.querySelector('[data-action="practice-next"]')?.addEventListener('click',()=>{const total=applicationLab?.items?.length||0;if(practiceIndex>=total-1){view='home';practiceIndex=0;practiceRevealed=false;render({focus:true});return}practiceIndex++;practiceRevealed=false;render({focus:true})});
 document.querySelector('[data-action="listen"]')?.addEventListener('click',()=>{const ok=speak(sceneSpeech(activeJourney,sceneIndex(state,activeJourney.palace_id))),status=document.getElementById('audioStatus');if(status)status.textContent=ok?'Reading this scene aloud.':'Text-to-speech is unavailable in this browser.'});
 document.querySelector('[data-action="stop-audio"]')?.addEventListener('click',()=>{stopSpeech();const status=document.getElementById('audioStatus');if(status)status.textContent='Audio stopped.'});
 document.querySelector('[data-action="open-recall"]')?.addEventListener('click',()=>{recallOpen=true;stopSpeech();render({focus:true})});
 document.querySelector('[data-action="cancel-recall"]')?.addEventListener('click',()=>{recallOpen=false;render({focus:true})});
 document.querySelector('[data-action="hint"]')?.addEventListener('click',e=>showRecallHint(e.currentTarget.dataset.object).catch(err=>showInlineError('recallHint',err)));
 document.querySelector('[data-action="remembered"]')?.addEventListener('click',async e=>{const objectId=e.currentTarget.dataset.object;try{const data=await recallData(objectId),assisted=wasRecallAssisted(state,activeJourney.palace_id,objectId);scheduleReview(state,{unitId:currentUnitId(),objectId:data.obj.memory_object_id,journeyId:activeJourney.palace_id,prompt:data.prompt,hint:data.hint,answer:data.answer},!assisted);clearRecallAssisted(state,activeJourney.palace_id,objectId);nextScene()}catch(err){showInlineError('recallHint',err)}});
 document.querySelector('[data-action="next-scene"]')?.addEventListener('click',()=>recallOpen?skipRecallAndContinue():nextScene());
 document.querySelector('[data-action="review-hint"]')?.addEventListener('click',e=>showReviewHint(e.currentTarget.dataset.object));
 document.querySelector('[data-action="review-remembered"]')?.addEventListener('click',e=>finishExactReview(e.currentTarget.dataset.object,true));
 document.querySelectorAll('[data-action="mixed-choice"]').forEach(b=>b.onclick=()=>{const set=(mixedData?.sets||[]).find(s=>s.set_id===b.dataset.set),due=dueReviews(state,5,currentUnitId())[0],q=set?.questions?.[Number(due?.questionIndex||0)];if(!set||!q)return;const correct=b.dataset.choice===q.answer;document.querySelectorAll('[data-action="mixed-choice"]').forEach(x=>x.disabled=true);const host=document.getElementById('reviewFeedback');if(host)host.innerHTML=`<div class="review-feedback"><strong>${correct?'Correct':'Not yet'}</strong><p>${esc(q.explanation)}</p>${!correct?`<p><strong>Answer · ${esc(q.answer)}</strong></p>`:''}<button class="primary" data-action="mixed-next">Continue review</button></div>`;document.querySelector('[data-action="mixed-next"]')?.addEventListener('click',()=>{completeMixedReview(state,set,correct);render({focus:true})})});
}
function showInlineError(id,err){const host=document.getElementById(id);if(host)host.innerHTML=`<div class="error-note" role="alert">${esc(err?.message||'Something went wrong. Please try again.')}</div>`}
function showError(err,retry){
 stopSpeech();const message=err?.message||'The site could not load this part of the course.';
 root.innerHTML=`<div class="shell"><main id="main-content" tabindex="-1" class="error-shell"><section class="card error-card" role="alert"><span class="eyebrow">Memory Palace</span><h1>We could not load this page.</h1><p>${esc(message)}</p><p class="muted">Your saved progress is still on this device. Try the request again or return to Home.</p><div class="row"><button class="primary" id="retryApp">Try again</button><button class="secondary" id="errorHome">Back to Home</button></div></section></main></div>`;
 document.getElementById('retryApp')?.addEventListener('click',retry);document.getElementById('errorHome')?.addEventListener('click',()=>boot());focusMain();
}
async function boot(){
 try{
   registry=await api.courses();
   const params=new URLSearchParams(location.search),requestedCourse=params.get('course'),requestedUnit=params.get('unit');
   if(requestedCourse){await openCourse(requestedCourse,requestedUnit);return}
   if(requestedUnit){await openCourse(defaultCourseId,requestedUnit);return}
   view='courses';render({focus:false});
 }catch(err){showError(err,boot)}
}
boot();
