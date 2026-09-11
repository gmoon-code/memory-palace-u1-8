const KEY='memory-palace-v2:progress';
const HOUR=60*60*1000, DAY=24*HOUR, ASSIST_TTL=2*HOUR;

function plainObject(value){return value&&typeof value==='object'&&!Array.isArray(value)?value:{}}
function finiteNonNegative(value,fallback=0){const n=Number(value);return Number.isFinite(n)&&n>=0?Math.floor(n):fallback}
function fresh(){return{activeUnit:'unit-1',activeJourney:null,sceneByJourney:{},review:[],storySeen:{},completedJourneys:{},encounteredObjects:{},assistedRecalls:{},assistedReviews:{},version:4}}
function cleanBooleanMap(value){const src=plainObject(value),out={};for(const [k,v] of Object.entries(src))if(typeof k==='string'&&v===true)out[k]=true;return out}
function cleanSceneMap(value){const src=plainObject(value),out={};for(const [k,v] of Object.entries(src)){if(typeof k!=='string')continue;const n=finiteNonNegative(v,-1);if(n>=0)out[k]=n}return out}
function cleanTimedMap(value,now=Date.now()){
 const src=plainObject(value),out={};
 for(const [k,v] of Object.entries(src)){
   const t=Number(v);if(typeof k==='string'&&Number.isFinite(t)&&t>0&&now-t<=ASSIST_TTL)out[k]=t;
 }
 return out;
}
function cleanReview(value){
 if(!Array.isArray(value))return[];
 return value.filter(x=>x&&typeof x==='object'&&typeof x.objectId==='string'&&Number.isFinite(Number(x.dueAt))).map(x=>({...x,dueAt:Number(x.dueAt),strength:finiteNonNegative(x.strength,0),questionIndex:finiteNonNegative(x.questionIndex,0)}));
}
function normalize(raw){
 const base=fresh(),src=plainObject(raw),unit=typeof src.activeUnit==='string'&&/^unit-\d+$/.test(src.activeUnit)?src.activeUnit:base.activeUnit;
 return{
   activeUnit:unit,
   activeJourney:typeof src.activeJourney==='string'&&src.activeJourney.trim()?src.activeJourney:null,
   sceneByJourney:cleanSceneMap(src.sceneByJourney),
   review:cleanReview(src.review),
   storySeen:cleanBooleanMap(src.storySeen),
   completedJourneys:cleanBooleanMap(src.completedJourneys),
   encounteredObjects:cleanBooleanMap(src.encounteredObjects),
   assistedRecalls:cleanTimedMap(src.assistedRecalls),
   assistedReviews:cleanTimedMap(src.assistedReviews),
   version:4,
 };
}
function storage(){try{return globalThis.localStorage||null}catch{return null}}
export function loadState(){
 try{const s=storage();if(!s)return fresh();const raw=s.getItem(KEY);return normalize(raw?JSON.parse(raw):{})}catch{return fresh()}
}
export function saveState(state){
 const normalized=normalize(state);Object.assign(state,normalized);
 try{const s=storage();if(s)s.setItem(KEY,JSON.stringify(normalized))}catch{/* Progress remains usable in memory when storage is unavailable. */}
 return state;
}
export function sceneIndex(state,id){return finiteNonNegative(state?.sceneByJourney?.[id],0)}
export function setSceneIndex(state,id,index){if(typeof id!=='string'||!id)return;state.sceneByJourney={...plainObject(state.sceneByJourney),[id]:finiteNonNegative(index,0)};saveState(state)}
export function markSeen(state,journeyId,index){if(typeof journeyId!=='string'||!journeyId)return;state.storySeen={...plainObject(state.storySeen),[`${journeyId}:${finiteNonNegative(index,0)}`]:true};saveState(state)}
export function markJourneyComplete(state,journeyId){if(typeof journeyId!=='string'||!journeyId)return;state.completedJourneys={...plainObject(state.completedJourneys),[journeyId]:true};saveState(state)}
export function journeyProgress(state,journey){
 const total=finiteNonNegative(journey?.scene_count,0);
 const seen=journey?Array.from({length:total},(_,i)=>state?.storySeen?.[`${journey.palace_id}:${i}`]).filter(Boolean).length:0;
 return {seen,total,complete:!!state?.completedJourneys?.[journey?.palace_id]};
}
export function markEncountered(state,objectId){if(typeof objectId!=='string'||!objectId)return;state.encounteredObjects={...plainObject(state.encounteredObjects),[objectId]:true}}
export function scheduleReview(state,item,remembered){
  if(!item||typeof item.objectId!=='string'||!item.objectId)return;
  const now=Date.now(); const next={...item,type:item.type||'exact',dueAt:now+(remembered?DAY:5*60*1000),strength:remembered?finiteNonNegative(item.strength,0)+1:finiteNonNegative(item.strength,0)};
  const rest=(Array.isArray(state.review)?state.review:[]).filter(x=>x?.objectId!==item.objectId); state.review=[...rest,next]; saveState(state);
}
export function scheduleEncounteredReview(state,item){
  if(!item||typeof item.objectId!=='string'||!item.objectId)return;
  markEncountered(state,item.objectId);
  const review=Array.isArray(state.review)?state.review:[];
  if(review.some(x=>x?.objectId===item.objectId)){saveState(state);return}
  const unitId=item.unitId||'unit-1';
  const pending=review.filter(x=>(x.unitId||'unit-1')===unitId && x.type!=='mixed').length;
  const dayBand=Math.floor(pending/5),withinDay=(pending%5)*90*60*1000;
  state.review=[...review,{...item,type:'exact',unitId,dueAt:Date.now()+18*HOUR+dayBand*DAY+withinDay,strength:0,source:'story'}];saveState(state);
}
export function scheduleEligibleMixedReviews(state,sets=[],unitId='unit-1'){
  if(!Array.isArray(sets)||!sets.length)return;
  const encountered=plainObject(state.encounteredObjects);let changed=false;const review=Array.isArray(state.review)?state.review:[];
  for(const set of sets){
    if(!set||!Array.isArray(set.knowledge_ids)||!set.knowledge_ids.every(id=>encountered[id]))continue;
    const objectId=`MIXED:${set.set_id}`;
    if((state.review||[]).some(x=>x?.objectId===objectId))continue;
    state.review=[...(state.review||[]),{type:'mixed',unitId,objectId,setId:set.set_id,questionIndex:0,dueAt:Date.now()+Math.max(48,Number(set.initial_delay_hours||48))*HOUR,strength:0,source:'mixed-discrimination'}];changed=true;
  }
  if(changed)saveState(state);
}
function belongsToUnit(x,unitId){return (x?.unitId||'unit-1')===unitId}
export function dueReviews(state,limit=5,unitId='unit-1'){return(Array.isArray(state.review)?state.review:[]).filter(x=>belongsToUnit(x,unitId)&&Number(x.dueAt)<=Date.now()).sort((a,b)=>Number(a.dueAt)-Number(b.dueAt)).slice(0,Math.max(0,finiteNonNegative(limit,5)))}
export function totalDue(state,unitId='unit-1'){return(Array.isArray(state.review)?state.review:[]).filter(x=>belongsToUnit(x,unitId)&&Number(x.dueAt)<=Date.now()).length}
export function completeReview(state,objectId,remembered){const existing=(Array.isArray(state.review)?state.review:[]).find(x=>x?.objectId===objectId);if(existing)scheduleReview(state,existing,remembered)}
export function completeMixedReview(state,set,remembered){
  if(!set)return;const objectId=`MIXED:${set.set_id}`;const existing=(Array.isArray(state.review)?state.review:[]).find(x=>x?.objectId===objectId);if(!existing)return;
  const questions=Array.isArray(set.questions)?set.questions:[];let next={...existing};
  if(!remembered){next.dueAt=Date.now()+5*60*1000;next.strength=Math.max(0,finiteNonNegative(existing.strength,0)-1)}
  else if(finiteNonNegative(existing.questionIndex,0)+1<questions.length){next.questionIndex=finiteNonNegative(existing.questionIndex,0)+1;next.dueAt=Date.now()+DAY;next.strength=finiteNonNegative(existing.strength,0)+1}
  else{next.questionIndex=0;next.dueAt=Date.now()+7*DAY;next.strength=finiteNonNegative(existing.strength,0)+1}
  state.review=(state.review||[]).map(x=>x?.objectId===objectId?next:x);saveState(state);
}
function assistedKey(journeyId,objectId){return `${journeyId||''}:${objectId||''}`}
export function markRecallAssisted(state,journeyId,objectId){const k=assistedKey(journeyId,objectId);if(k===':')return;state.assistedRecalls={...plainObject(state.assistedRecalls),[k]:Date.now()};saveState(state)}
export function wasRecallAssisted(state,journeyId,objectId){const k=assistedKey(journeyId,objectId),t=Number(state?.assistedRecalls?.[k]);return Number.isFinite(t)&&Date.now()-t<=ASSIST_TTL}
export function clearRecallAssisted(state,journeyId,objectId){const k=assistedKey(journeyId,objectId),next={...plainObject(state.assistedRecalls)};delete next[k];state.assistedRecalls=next;saveState(state)}
export function markReviewAssisted(state,objectId){if(typeof objectId!=='string'||!objectId)return;state.assistedReviews={...plainObject(state.assistedReviews),[objectId]:Date.now()};saveState(state)}
export function wasReviewAssisted(state,objectId){const t=Number(state?.assistedReviews?.[objectId]);return Number.isFinite(t)&&Date.now()-t<=ASSIST_TTL}
export function clearReviewAssisted(state,objectId){const next={...plainObject(state.assistedReviews)};delete next[objectId];state.assistedReviews=next;saveState(state)}
