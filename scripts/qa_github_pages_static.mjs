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

// The public Pages artifact contains the local-first authoring UI, but it
// must never contain the backend's privileged admin editor, dev distribution,
// or server-side files. GitHub Pages only serves static assets.
const editorHtml=await readFile(path.join(ROOT,'authoring/visual-editor.html'),'utf8');
const editorJs=await readFile(path.join(ROOT,'authoring/visual-editor.js'),'utf8');
await readFile(path.join(ROOT,'authoring/visual-editor.css'));
assert(editorHtml.includes('visual-editor.js')&&editorHtml.includes('visual-editor.css'),
  'standalone visual editor must use repository-relative assets');
assert(editorJs.includes('../content/ap-biology/'),
  'editor must load the released journey content through relative paths');
assert(editorJs.includes('localStorage')&&editorJs.includes('Export'),
  'editor must retain browser-local drafts and controlled JSON export');
assert(!editorJs.includes('/api/admin/')&&!editorHtml.includes('/api/admin/'),
  'Pages narrative editor may not embed protected admin service routes');
for(const forbidden of [
  'frontend/admin/editor.js','backend/cloudflare-workers-ai',
  'distribution/content-studio-teacher','authoring/README.md'
]){
  try{await readFile(path.join(ROOT,forbidden));assert(false,
    'Pages artifact leaked non-public server or distribution file '+forbidden);}
  catch(e){if(e.code!=='ENOENT')throw e;}
}

const course=await api.course();
assert(Array.isArray(course?.units)&&course.units.length===8,'course registry does not expose 8 units');
assert(course.units.every(u=>u.status==='STUDENT_READY'),'a released unit is not STUDENT_READY');
const units=(await api.units()).units;
assert(units.length===8,'units adapter count mismatch');

let journeys=0,scenes=0,recalls=0,challenges=0,reviewTargets=0,mixedSets=0,mixedQuestions=0;
const objectRequests=new Map();
for(const entry of course.units){
  const unitId=entry.unit_id;
  const summary=await api.unit(unitId);
  assert(summary?.unit_id===unitId,`${unitId} summary unavailable`);
  const registry=await api.journeys(unitId);
  assert(Array.isArray(registry.guided_journeys),`${unitId} journey registry malformed`);
  assert(registry.guided_journeys.length===Number(entry.journey_count),`${unitId} journey count mismatch`);
  journeys+=registry.guided_journeys.length;
  for(const meta of registry.guided_journeys){
    const journey=await api.journey(unitId,meta.palace_id);
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
  const lab=await api.applicationLab(unitId);challenges+=(lab?.items||[]).length;
  const review=await api.reviewManifest(unitId);reviewTargets+=(review?.targets||[]).length;
  const mixed=await api.mixedDiscrimination(unitId);mixedSets+=(mixed?.sets||[]).length;
  mixedQuestions+=(mixed?.sets||[]).reduce((n,set)=>n+(set?.questions||[]).length,0);
}

for(const [key,[unitId,objectId]] of objectRequests){
  const object=await api.object(unitId,objectId);
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
