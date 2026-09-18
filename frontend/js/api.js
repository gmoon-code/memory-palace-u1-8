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
async function staticCourses(){return staticJSON('platform/courses.json')}
async function staticPackage(courseId=DEFAULT_COURSE_ID){return staticJSON(`platform/course-packages/${courseId}.json`)}
async function staticCourse(courseId=DEFAULT_COURSE_ID){
  const pkg=await staticPackage(courseId);
  return staticJSON(pkg.course_file);
}
async function staticUnits(courseId=DEFAULT_COURSE_ID){return{course_id:courseId,units:(await staticCourse(courseId)).units||[]}}
async function staticUnit(courseId,unitId){return((await staticCourse(courseId)).units||[]).find(u=>u.unit_id===unitId)||null}
async function staticUnitPackage(courseId,unitId){
  const pkg=await staticPackage(courseId);
  return(pkg.units||[]).find(u=>u.unit_id===unitId)||null;
}
async function staticArtifact(spec){
  if(spec?.mode==='empty')return spec.empty_payload||{};
  if(spec?.mode!=='file'||!spec.path)throw new Error('Course package artifact is not available.');
  return staticJSON(spec.path);
}
function records(payload,keys=[]){
  if(Array.isArray(payload))return payload.filter(x=>x&&typeof x==='object');
  if(payload&&typeof payload==='object'){
    for(const key of keys){
      if(Array.isArray(payload[key]))return payload[key].filter(x=>x&&typeof x==='object');
    }
  }
  return[];
}
function first(record,keys,fallback=''){
  for(const key of keys){if(record?.[key]!==undefined&&record[key]!==null&&record[key]!=='')return record[key]}
  return fallback;
}
function canonicalObject(record){
  const id=String(first(record,['knowledge_id','Knowledge ID','id'],''));
  const exact=first(record,['exact_name_recall','Exact Name Recall','exact_name_required'],false);
  return{
    memory_object_id:id,
    source_knowledge_id:id,
    canonical_term:first(record,['canonical_label','Canonical Label','canonical_term','term'],id),
    canonical_definition:first(record,['canonical_verified_statement','Canonical Verified Statement','canonical_definition','definition'],''),
    exact_name_recall:typeof exact==='string'?['YES','TRUE','REQUIRED'].includes(exact.trim().toUpperCase()):!!exact,
    source_reference:first(record,['source_reference','Source Reference'],''),
    canonical_lock:first(record,['canonical_lock','Canonical Lock'],'')
  };
}
async function staticJourneys(courseId,unitId='unit-1'){
  const unit=await staticUnitPackage(courseId,unitId);
  if(!unit)throw new Error('Unit package is not available.');
  const spec=unit.journeys;
  const data=await staticJSON(spec.registry_path);
  return{course_id:courseId,unit_id:unitId,guided_journeys:Array.isArray(data?.[spec.collection_key])?data[spec.collection_key]:[]};
}
async function staticJourney(courseId,unitId,id){
  const unit=await staticUnitPackage(courseId,unitId);
  if(!unit)throw new Error('Unit package is not available.');
  const spec=unit.journeys;
  const filename=String(spec.filename_template).replace('{journey_id}',encodeURIComponent(id));
  return staticJSON(`${String(spec.directory).replace(/\/$/,'')}/${filename}`);
}
async function staticObject(courseId,unitId,id){
  const unit=await staticUnitPackage(courseId,unitId);
  if(!unit)throw new Error('Unit package is not available.');
  const spec=unit.memory_objects;
  const data=await staticArtifact(spec);
  const list=records(data,spec.collection_keys||['memory_objects','records','items']);
  if(spec.format==='canonical_catalog_as_memory_objects'){
    const record=list.find(item=>String(first(item,['knowledge_id','Knowledge ID','id'],''))===id);
    return record?canonicalObject(record):null;
  }
  return list.find(item=>String(first(item,['memory_object_id','object_id','knowledge_id','Knowledge ID'],''))===id)||null;
}
async function staticApplicationLab(courseId,unitId='unit-1'){
  const unit=await staticUnitPackage(courseId,unitId);if(!unit)throw new Error('Unit package is not available.');
  return staticArtifact(unit.challenge_lab);
}
async function staticReviewManifest(courseId,unitId){
  const unit=await staticUnitPackage(courseId,unitId);if(!unit)throw new Error('Unit package is not available.');
  return staticArtifact(unit.review);
}
async function staticMixedDiscrimination(courseId,unitId){
  const unit=await staticUnitPackage(courseId,unitId);if(!unit)throw new Error('Unit package is not available.');
  return staticArtifact(unit.mixed_discrimination);
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
