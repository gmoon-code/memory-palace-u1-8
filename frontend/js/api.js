const DEFAULT_TIMEOUT_MS=12000;
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
export const api={
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
