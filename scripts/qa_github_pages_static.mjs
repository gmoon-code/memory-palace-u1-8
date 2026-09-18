import {readFile} from 'node:fs/promises';
import {fileURLToPath,pathToFileURL} from 'node:url';
import path from 'node:path';

const SOURCE_ROOT=path.resolve(fileURLToPath(new URL('..',import.meta.url)));
const ROOT=process.env.PAGES_SITE_ROOT?path.resolve(process.env.PAGES_SITE_ROOT):SOURCE_ROOT;
const originalFetch=globalThis.fetch;
globalThis.fetch=async(input)=>{
  const url=input instanceof URL?input:new URL(String(input));
  if(url.protocol!=='file:')return originalFetch(input);
  try{
    const body=await readFile(fileURLToPath(url));
    return new Response(body,{status:200,headers:{'content-type':url.pathname.endsWith('.json')?'application/json; charset=utf-8':'application/octet-stream'}});
  }catch{
    return new Response('Not found',{status:404,headers:{'content-type':'text/plain'}});
  }
};

const {api,hostingMode}=await import(pathToFileURL(path.join(ROOT,'frontend/js/api.js')).href+`?qa=${Date.now()}`);
function assert(ok,message){if(!ok)throw new Error(`GITHUB PAGES QA FAIL · ${message}`)}

assert(hostingMode==='static','frontend API adapter did not select static mode');
const index=await readFile(path.join(ROOT,'index.html'),'utf8');
assert(index.includes('./frontend/css/base.css'),'root entrypoint does not use repository-relative CSS');
assert(index.includes('./frontend/css/unit-theme.css'),'root entrypoint does not load the unit color system');
assert(index.includes('./frontend/js/unit-theme.js'),'root entrypoint does not load unit color switching');
assert(index.includes('./frontend/js/app.js'),'root entrypoint does not use repository-relative JavaScript');
assert(!index.includes('src="/static/'),'root entrypoint contains server-only absolute script path');
assert(!index.includes('href="/static/'),'root entrypoint contains server-only absolute stylesheet path');
await readFile(path.join(ROOT,'frontend/css/unit-theme.css'));
await readFile(path.join(ROOT,'frontend/js/unit-theme.js'));
await readFile(path.join(ROOT,'.nojekyll'));

const courseId='ap-biology';
const registry=await api.courses();
assert(registry.courses?.some(c=>c.course_id===courseId&&c.status==='available'),'platform course registry does not expose AP Biology');
const course=await api.course(courseId);
assert(Array.isArray(course?.units)&&course.units.length===8,'course registry does not expose 8 units');
assert(course.units.every(u=>u.status==='STUDENT_READY'),'a released unit is not STUDENT_READY');
const units=(await api.units(courseId)).units;
assert(units.length===8,'units adapter count mismatch');

let journeys=0,scenes=0,recalls=0,challenges=0,reviewTargets=0,mixedSets=0,mixedQuestions=0;
const objectRequests=new Map();
for(const entry of course.units){
  const unitId=entry.unit_id;
  const summary=await api.unit(courseId,unitId);
  assert(summary?.unit_id===unitId,`${unitId} summary unavailable`);
  const registry=await api.journeys(courseId,unitId);
  assert(Array.isArray(registry.guided_journeys),`${unitId} journey registry malformed`);
  assert(registry.guided_journeys.length===Number(entry.journey_count),`${unitId} journey count mismatch`);
  journeys+=registry.guided_journeys.length;
  for(const meta of registry.guided_journeys){
    const journey=await api.journey(courseId,unitId,meta.palace_id);
    assert(journey?.palace_id===meta.palace_id,`${unitId}/${meta.palace_id} journey unavailable`);
    assert(Array.isArray(journey.scenes),`${unitId}/${meta.palace_id} scenes missing`);
    assert(journey.scenes.length===Number(meta.scene_count),`${unitId}/${meta.palace_id} scene count mismatch`);
    scenes+=journey.scenes.length;
    for(const scene of journey.scenes){
      if(scene?.checkpoint)recalls++;
      for(const beat of scene?.story_beats||[]){
        if(beat?.object_id)objectRequests.set(`${unitId}:${beat.object_id}`,[unitId,beat.object_id]);
      }
      if(scene?.checkpoint&&scene?.checkpoint_object_id)objectRequests.set(`${unitId}:${scene.checkpoint_object_id}`,[unitId,scene.checkpoint_object_id]);
    }
  }
  const lab=await api.applicationLab(courseId,unitId);challenges+=(lab?.items||[]).length;
  const review=await api.reviewManifest(courseId,unitId);reviewTargets+=(review?.targets||[]).length;
  const mixed=await api.mixedDiscrimination(courseId,unitId);mixedSets+=(mixed?.sets||[]).length;
  mixedQuestions+=(mixed?.sets||[]).reduce((n,set)=>n+(set?.questions||[]).length,0);
}

for(const [key,[unitId,objectId]] of objectRequests){
  const object=await api.object(courseId,unitId,objectId);
  assert(object?.memory_object_id===objectId,`${key} Memory Object unavailable in static mode`);
}

assert(journeys===58,`expected 58 journeys, got ${journeys}`);
assert(scenes===448,`expected 448 scenes, got ${scenes}`);
assert(recalls===152,`expected 152 Quick Recalls, got ${recalls}`);
assert(challenges===112,`expected 112 Challenge Lab items, got ${challenges}`);
assert(reviewTargets===887,`expected 887 Review targets, got ${reviewTargets}`);
assert(mixedSets===220,`expected 220 mixed-discrimination sets, got ${mixedSets}`);
assert(mixedQuestions===600,`expected 600 mixed questions, got ${mixedQuestions}`);

console.log('GITHUB PAGES STATIC QA PASS');
console.log(JSON.stringify({site_root:ROOT,units:8,journeys,scenes,quick_recalls:recalls,challenge_lab_items:challenges,review_targets:reviewTargets,mixed_sets:mixedSets,mixed_questions:mixedQuestions,objects_resolved:objectRequests.size,unit_theme_assets:true},null,2));
