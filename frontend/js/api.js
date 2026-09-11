const DEFAULT_TIMEOUT_MS=12000;
const MODULE_URL=new URL(import.meta.url);
const STATIC_MODE=MODULE_URL.pathname.includes('/frontend/js/');
const STATIC_ROOT=new URL('../../',MODULE_URL);
const STATIC_CACHE=new Map();

export async function getJSON(path,{timeoutMs=DEFAULT_TIMEOUT_MS}={}){
  const controller=new AbortController();const timer=setTimeout(()=>controller.abort(),timeoutMs);
  try{
    const res=await fetch(path,{method:'GET',headers:{Accept:'application/json'},credentials:'same-origin',signal:controller.signal});
    if(!res.ok)throw new Error(`Request failed with ${res.status}${res.statusText?` ${res.statusText}`:''}.`);
    const type=(res.headers.get('content-type')||'').toLowerCase();
    if(!type.includes('application/json'))throw new Error('The server returned an unexpected response.');
    try{return await res.json()}catch{throw new Error('The server returned unreadable data.')}
  }catch(err){
    if(err?.name==='AbortError')throw new Error('The server took too long to respond. Please try again.');
    if(err instanceof TypeError)throw new Error('The site could not reach the server. Check your connection and try again.');
    throw err;
  }finally{clearTimeout(timer)}
}

function staticJSON(relativePath){
  const url=new URL(relativePath,STATIC_ROOT).href;
  if(!STATIC_CACHE.has(url))STATIC_CACHE.set(url,getJSON(url).catch(err=>{STATIC_CACHE.delete(url);throw err}));
  return STATIC_CACHE.get(url);
}
function unitDir(unitId){return `content/ap-biology/${unitId}`}
async function staticCourse(){return staticJSON('content/ap-biology/course.json')}
async function staticUnits(){return{units:(await staticCourse()).units||[]}}
async function staticUnit(unitId){return((await staticCourse()).units||[]).find(u=>u.unit_id===unitId)||null}
async function staticJourneys(unitId='unit-1'){
  const rel=unitId==='unit-1'?`${unitDir(unitId)}/journeys.json`:`${unitDir(unitId)}/journeys-f5.json`;
  const data=await staticJSON(rel);return{unit_id:unitId,guided_journeys:data.guided_journeys||[]};
}
async function staticJourney(unitId,id){return staticJSON(`${unitDir(unitId)}/journeys/${encodeURIComponent(id)}.json`)}
function canonicalObject(record){
  return{memory_object_id:record.knowledge_id,canonical_term:record.canonical_label,canonical_definition:record.canonical_verified_statement,exact_name_recall:record.exact_name_recall||false,source_reference:record.source_reference||'',canonical_lock:record.canonical_lock||''};
}
async function staticObject(unitId,id){
  if(unitId==='unit-1'){
    const data=await staticJSON(`${unitDir(unitId)}/memory-objects.json`);return(data.memory_objects||[]).find(o=>o.memory_object_id===id)||null;
  }
  if(unitId==='unit-2'||unitId==='unit-3'){
    const data=await staticJSON(`${unitDir(unitId)}/source/canonical-${unitId.replace('unit-','unit')}-f1.json`);
    const record=(data.canonical_catalog||[]).find(r=>r.knowledge_id===id);return record?canonicalObject(record):null;
  }
  const data=await staticJSON(`${unitDir(unitId)}/memory-objects-f5.json`);return(data.memory_objects||[]).find(o=>o.memory_object_id===id)||null;
}
async function staticApplicationLab(unitId='unit-1'){return staticJSON(`${unitDir(unitId)}/application-lab.json`)}
async function staticReviewManifest(unitId){
  if(unitId==='unit-1')return{unit_id:unitId,target_count:0,targets:[]};
  return staticJSON(`${unitDir(unitId)}/review-manifest-f5.json`);
}
async function staticMixedDiscrimination(unitId){
  if(unitId==='unit-1')return{unit_id:unitId,set_count:0,question_count:0,sets:[]};
  return staticJSON(`${unitDir(unitId)}/mixed-discrimination-f5.json`);
}

const dynamicApi={
  course:()=>getJSON('/api/course'),
  units:()=>getJSON('/api/units'),
  unit:(unitId)=>getJSON(`/api/units/${encodeURIComponent(unitId)}`),
  journeys:(unitId='unit-1')=>getJSON(`/api/units/${encodeURIComponent(unitId)}/journeys`),
  journey:(unitId,id)=>getJSON(`/api/units/${encodeURIComponent(unitId)}/journeys/${encodeURIComponent(id)}`),
  object:(unitId,id)=>getJSON(`/api/units/${encodeURIComponent(unitId)}/objects/${encodeURIComponent(id)}`),
  applicationLab:(unitId='unit-1')=>getJSON(`/api/units/${encodeURIComponent(unitId)}/application-lab`),
  reviewManifest:(unitId)=>getJSON(`/api/units/${encodeURIComponent(unitId)}/review-manifest`),
  mixedDiscrimination:(unitId)=>getJSON(`/api/units/${encodeURIComponent(unitId)}/mixed-discrimination`),
};
const staticApi={course:staticCourse,units:staticUnits,unit:staticUnit,journeys:staticJourneys,journey:staticJourney,object:staticObject,applicationLab:staticApplicationLab,reviewManifest:staticReviewManifest,mixedDiscrimination:staticMixedDiscrimination};
export const api=STATIC_MODE?staticApi:dynamicApi;
export const hostingMode=STATIC_MODE?'static':'server';
