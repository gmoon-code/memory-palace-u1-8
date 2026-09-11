import fs from 'fs';
global.localStorage={store:new Map(),setItem(k,v){this.store.set(k,String(v))},getItem(k){return this.store.has(k)?this.store.get(k):null},removeItem(k){this.store.delete(k)}};
const stateMod=await import('../frontend/js/state.js');
const {learnView,sceneSpeech}=await import('../frontend/js/views/learn.js');
const {reviewView}=await import('../frontend/js/views/review.js');
const {practiceView}=await import('../frontend/js/views/practice.js');
const {prepareSpeechText}=await import('../frontend/js/audio.js');
function read(p){return JSON.parse(fs.readFileSync(new URL('../'+p,import.meta.url),'utf8'))}
function assert(x,msg){if(!x)throw new Error(msg)}
const mixed=read('content/ap-biology/unit-3/mixed-discrimination-f5.json');
const review=read('content/ap-biology/unit-3/review-manifest-f5.json');
const lab=read('content/ap-biology/unit-3/application-lab.json');
const j4=read('content/ap-biology/unit-3/journeys/U3-J4.json');
let state={activeUnit:'unit-3',review:[],encounteredObjects:{}};
// Every Unit 3 mixed set becomes eligible after all of its members have been encountered.
for(const set of mixed.sets)for(const id of set.knowledge_ids)stateMod.markEncountered(state,id);
stateMod.scheduleEligibleMixedReviews(state,mixed.sets,'unit-3');
assert(state.review.filter(x=>x.type==='mixed'&&x.unitId==='unit-3').length===28,'Unit 3 mixed scheduler did not create all 28 sets');
assert(state.review.filter(x=>x.type==='mixed').every(x=>x.dueAt-Date.now()>=47.9*60*60*1000),'Mixed review was scheduled earlier than 48 hours');
// All exact-name targets can be queued while visible review remains bounded.
for(const t of review.targets)stateMod.scheduleEncounteredReview(state,{unitId:'unit-3',objectId:t.knowledge_id,prompt:t.prompt,hint:t.hint,answer:t.target_answer});
assert(state.review.filter(x=>x.type==='exact'&&x.unitId==='unit-3').length===126,'Exact-name scheduler did not preserve 126 targets');
state.review=state.review.map(x=>({...x,dueAt:0}));
assert(stateMod.dueReviews(state,5,'unit-3').length===5,'Visible review limit is not five');
assert(stateMod.totalDue(state,'unit-3')===154,'Due total should include 126 exact + 28 mixed items');
// Long route remains a single full-length route declaration, and anchors begin collapsed.
const first=learnView(j4,0,false);const late=learnView(j4,11,false);
assert(first.includes('--route-count:12'),'12-scene route does not declare all 12 nodes');
assert(!first.includes('<details class="memory-panel" open>'),'Memory anchors are expanded by default');
assert(first.includes('Optional memory anchors'),'Collapsed memory-anchor affordance missing');
assert(late.includes('12 / 12'),'Late-scene progress rendering failed');
const cpIndex=j4.scenes.findIndex(s=>s.checkpoint);const recall=learnView(j4,cpIndex,true);
for(const leak of ['scene-orientation','story-prose','memory-panel','route-wrap','cast-section'])assert(!recall.includes(leak),`Recall leaks ${leak}`);
assert(recall.includes('Quick recall · story hidden'),'Recall hidden-state label missing');
// Review and Challenge Lab render their released Unit 3 data.
const mixedItem={type:'mixed',unitId:'unit-3',objectId:`MIXED:${mixed.sets[0].set_id}`,setId:mixed.sets[0].set_id,questionIndex:0,dueAt:0};
assert(reviewView([mixedItem],1,mixed.sets).includes('Mixed discrimination'),'Mixed review UI failed');
assert(practiceView(lab,0,false).includes('1 of 11'),'Challenge Lab UI does not expose 11-task progression');
// Speech-only normalization keeps the visual/scientific text unchanged while making browser narration clearer.
const speech=prepareSpeechText('CO₂ + H₂O → O₂; NAD⁺ becomes NADH; ATP and ADP; H⁺ flows through ATP synthase.');
for(const phrase of ['carbon dioxide','water','oxygen','N A D plus','N A D H','A T P','A D P','hydrogen ions'])assert(speech.includes(phrase),`Speech normalization missing ${phrase}`);
assert(!sceneSpeech(j4,0).includes('**'),'Scene speech still contains Markdown emphasis markers');
console.log('UNIT3 F6 UI LOGIC QA PASS');
console.log(JSON.stringify({mixed_sets_scheduled:28,exact_targets_queued:126,visible_due_limit:5,route_nodes_j4:12,challenge_lab_items:11},null,2));
