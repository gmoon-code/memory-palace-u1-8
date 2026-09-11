function esc(v=''){return String(v).replace(/[&<>'"]/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[ch]))}
function guideName(j){return typeof j?.guide==='object'?j.guide.name:j?.guide||'Your guide'}
function journeyStats(state,j){
 const total=Number(j?.scene_count||0);
 const seen=Array.from({length:total},(_,i)=>state?.storySeen?.[`${j.palace_id}:${i}`]).filter(Boolean).length;
 return{seen,total,done:!!state?.completedJourneys?.[j?.palace_id],pct:total?Math.min(100,Math.round((seen/total)*100)):0};
}
function nextUsefulJourney(journeys,state,recommendedId){
 const explicit=journeys.find(j=>j.palace_id===recommendedId);if(explicit)return explicit;
 const active=journeys.find(j=>j.palace_id===state?.activeJourney);if(active&&!state?.completedJourneys?.[active.palace_id])return active;
 return journeys.find(j=>!state?.completedJourneys?.[j.palace_id])||active||journeys[0]||null;
}
export function homeView(course,unit,journeys,state,dueCount=0,recommendedId=null){
 const list=Array.isArray(journeys)?journeys:[];
 const active=nextUsefulJourney(list,state,recommendedId);
 const activeStats=active?journeyStats(state,active):{seen:0,total:0,done:false,pct:0};
 const currentIndex=active?Math.min(Number(state?.sceneByJourney?.[active.palace_id]||0)+1,active.scene_count||1):0;
 const completeCount=list.filter(j=>state?.completedJourneys?.[j.palace_id]).length;
 const visitedCount=list.reduce((sum,j)=>sum+journeyStats(state,j).seen,0);
 const cards=list.map(j=>{
   const s=journeyStats(state,j),label=s.done?'Walk it again':s.seen?'Continue journey':'Begin journey';
   return `<article class="card journey-card"><div class="journey-card-top"><span class="eyebrow">${esc(j.palace_name)}</span><span class="pill">${s.done?'Complete':s.seen?`${s.pct}%`:`${esc(j.estimated_minutes)} min`}</span></div><h3>${esc(j.story_title)}</h3><p>${esc(j.tagline)}</p><div class="journey-meta"><span>${s.total} locations</span><span>${esc(j.checkpoint_count)} optional recalls</span><span>Guide · ${esc(guideName(j))}</span></div><button class="${s.seen?'primary':'secondary'}" data-action="learn" data-id="${esc(j.palace_id)}">${label}</button></article>`;
 }).join('');
 const courseMap=(course?.units||[]).map(u=>{
   const current=u.unit_id===unit?.unit_id;
   return `<div class="roadmap-row ${current?'current-unit':''}"><span>Unit ${esc(u.number)}</span><strong>${esc(u.title)}</strong><em>${current?'Current unit':'Available'}</em>${current?`<span class="pill" aria-label="Current unit">Current</span>`:`<button class="ghost unit-open" data-action="switch-unit" data-unit="${esc(u.unit_id)}">Open</button>`}</div>`;
 }).join('');
 const challenge=(unit?.application_challenges||0)>0?`<section class="card challenge-strip"><div><span class="eyebrow">Apply the science</span><h2>Unit ${esc(unit.number)} Challenge Lab</h2><p>Work through one short application at a time after the palace stories. Hints and answer guides stay separate so you can choose how much support you need.</p></div><div class="challenge-side"><strong>${esc(unit.application_challenges)} challenges</strong><span>Your progress stays in this session</span><button class="secondary" data-action="practice">Open challenge lab</button></div></section>`:'';
 const recommendation=active?`${activeStats.seen?`Continue at location ${currentIndex} of ${activeStats.total}`:'Start with the first location'}`:'';
 return `<main id="main-content" tabindex="-1" class="stack" aria-label="Unit ${esc(unit?.number||'')} home">
  <section class="card hero"><div><span class="eyebrow">AP Biology · Unit ${esc(unit?.number||'')} · ${esc(unit?.title||'')}</span><h1>Keep the whole route in view.</h1><p>Follow one journey at a time while Home keeps your unit progress, current route, Review queue, and the rest of the course easy to find.</p><div class="row">${active?`<button class="primary" data-action="learn" data-id="${esc(active.palace_id)}">${activeStats.done?'Revisit':activeStats.seen?'Continue':'Begin'} ${esc(active.story_title)}</button>`:''}<button class="secondary" data-action="review">${dueCount?`Review ${dueCount} due ${dueCount===1?'memory':'memories'}`:'Open Review'}</button></div></div><aside class="hero-side"><span class="eyebrow">Current progress</span><strong>${completeCount} of ${list.length} journeys complete</strong><p class="muted">${visitedCount} locations visited · ${dueCount} Review item${dueCount===1?'':'s'} due${active?` · ${esc(recommendation)}`:''}</p><div class="metric-grid"><div class="metric"><strong>${completeCount}/${list.length}</strong><span>journeys</span></div><div class="metric"><strong>${visitedCount}</strong><span>locations visited</span></div><div class="metric"><strong>${dueCount}</strong><span>Review due</span></div></div></aside></section>
  <section class="library-section" aria-labelledby="journey-library-title"><div class="library-heading"><div><span class="eyebrow">Unit ${esc(unit?.number||'')} journey library</span><h2 id="journey-library-title">Your routes through ${esc(unit?.title||'this unit')}</h2></div><p>Choose any released journey. Previously completed routes stay available for another walk.</p></div><div class="journey-list">${cards}</div></section>
  ${challenge}
  <details class="card roadmap"><summary><span><span class="eyebrow">Course map</span><strong>All eight AP Biology units</strong></span><span class="summary-chevron" aria-hidden="true">⌄</span></summary><div class="roadmap-list">${courseMap}</div></details>
 </main>`;
}
