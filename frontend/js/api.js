const DEFAULT_TIMEOUT_MS=12000;
const MODULE_URL=new URL(import.meta.url);
const STATIC_MODE=MODULE_URL.pathname.includes('/frontend/js/');
const STATIC_ROOT=new URL('../../',MODULE_URL);
const STATIC_CACHE=new Map();
const DEFAULT_COURSE_ID='ap-biology';

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
function courseDir(courseId=DEFAULT_COURSE_ID){return `content/${courseId}`}
function unitDir(courseId,unitId){return `${courseDir(courseId)}/${unitId}`}
async function staticCourses(){return staticJSON('content/courses.json')}
async function staticCourse(courseId=DEFAULT_COURSE_ID){return staticJSON(`${courseDir(courseId)}/course.json`)}
async function staticUnits(courseId=DEFAULT_COURSE_ID){return{course_id:courseId,units:(await staticCourse(courseId)).units||[]}}
async function staticUnit(courseId,unitId){return((await staticCourse(courseId)).units||[]).find(u=>u.unit_id===unitId)||null}
async function staticJourneys(courseId,unitId='unit-1'){
  const base=unitDir(courseId,unitId);
  const rel=courseId===DEFAULT_COURSE_ID
    ?(unitId==='unit-1'?`${base}/journeys.json`:`${base}/journeys-f5.json`)
    :`${base}/journeys.json`;
  const data=await staticJSON(rel);return{course_id:courseId,unit_id:unitId,guided_journeys:data.guided_journeys||[]};
}
async function staticJourney(courseId,unitId,id){return staticJSON(`${unitDir(courseId,unitId)}/journeys/${encodeURIComponent(id)}.json`)}
function canonicalObject(record){
  return{memory_object_id:record.knowledge_id,canonical_term:record.canonical_label,canonical_definition:record.canonical_verified_statement,exact_name_recall:record.exact_name_recall||false,source_reference:record.source_reference||'',canonical_lock:record.canonical_lock||''};
}
async function staticObject(courseId,unitId,id){
  const base=unitDir(courseId,unitId);
  if(courseId!==DEFAULT_COURSE_ID){
    const data=await staticJSON(`${base}/memory-objects.json`);return(data.memory_objects||[]).find(o=>o.memory_object_id===id)||null;
  }
  if(unitId==='unit-1'){
    const data=await staticJSON(`${base}/memory-objects.json`);return(data.memory_objects||[]).find(o=>o.memory_object_id===id)||null;
  }
  if(unitId==='unit-2'||unitId==='unit-3'){
    const data=await staticJSON(`${base}/source/canonical-${unitId.replace('unit-','unit')}-f1.json`);
    const record=(data.canonical_catalog||[]).find(r=>r.knowledge_id===id);return record?canonicalObject(record):null;
  }
  const data=await staticJSON(`${base}/memory-objects-f5.json`);return(data.memory_objects||[]).find(o=>o.memory_object_id===id)||null;
}
async function staticApplicationLab(courseId,unitId='unit-1'){return staticJSON(`${unitDir(courseId,unitId)}/application-lab.json`)}
async function staticReviewManifest(courseId,unitId){
  if(courseId===DEFAULT_COURSE_ID&&unitId==='unit-1')return{course_id:courseId,unit_id:unitId,target_count:0,targets:[]};
  const name=courseId===DEFAULT_COURSE_ID?'review-manifest-f5.json':'review-manifest.json';
  return staticJSON(`${unitDir(courseId,unitId)}/${name}`);
}
async function staticMixedDiscrimination(courseId,unitId){
  if(courseId===DEFAULT_COURSE_ID&&unitId==='unit-1')return{course_id:courseId,unit_id:unitId,set_count:0,question_count:0,sets:[]};
  const name=courseId===DEFAULT_COURSE_ID?'mixed-discrimination-f5.json':'mixed-discrimination.json';
  return staticJSON(`${unitDir(courseId,unitId)}/${name}`);
}

const dynamicApi={
  courses:()=>getJSON('/api/courses'),
  course:(courseId=DEFAULT_COURSE_ID)=>getJSON(`/api/courses/${encodeURIComponent(courseId)}`),
  units:(courseId=DEFAULT_COURSE_ID)=>getJSON(`/api/courses/${encodeURIComponent(courseId)}/units`),
  unit:(courseId,unitId)=>getJSON(`/api/courses/${encodeURIComponent(courseId)}/units/${encodeURIComponent(unitId)}`),
  journeys:(courseId,unitId='unit-1')=>getJSON(`/api/courses/${encodeURIComponent(courseId)}/units/${encodeURIComponent(unitId)}/journeys`),
  journey:(courseId,unitId,id)=>getJSON(`/api/courses/${encodeURIComponent(courseId)}/units/${encodeURIComponent(unitId)}/journeys/${encodeURIComponent(id)}`),
  object:(courseId,unitId,id)=>getJSON(`/api/courses/${encodeURIComponent(courseId)}/units/${encodeURIComponent(unitId)}/objects/${encodeURIComponent(id)}`),
  applicationLab:(courseId,unitId='unit-1')=>getJSON(`/api/courses/${encodeURIComponent(courseId)}/units/${encodeURIComponent(unitId)}/application-lab`),
  reviewManifest:(courseId,unitId)=>getJSON(`/api/courses/${encodeURIComponent(courseId)}/units/${encodeURIComponent(unitId)}/review-manifest`),
  mixedDiscrimination:(courseId,unitId)=>getJSON(`/api/courses/${encodeURIComponent(courseId)}/units/${encodeURIComponent(unitId)}/mixed-discrimination`),
};
const staticApi={
  courses:staticCourses,
  course:staticCourse,
  units:staticUnits,
  unit:staticUnit,
  journeys:staticJourneys,
  journey:staticJourney,
  object:staticObject,
  applicationLab:staticApplicationLab,
  reviewManifest:staticReviewManifest,
  mixedDiscrimination:staticMixedDiscrimination,
};
export const api=STATIC_MODE?staticApi:dynamicApi;
export const hostingMode=STATIC_MODE?'static':'server';
export const defaultCourseId=DEFAULT_COURSE_ID;
