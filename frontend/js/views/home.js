function esc(v=''){return String(v).replace(/[&<>'"]/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[ch]))}
function guideName(j){return typeof j?.guide==='object'?j.guide.name:j?.guide||'Your guide'}
function unitTheme(n){return ['yellow','green','turquoise','pink'][(Math.max(1,Number(n)||1)-1)%4]}
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
 const units=Array.isArray(course?.units)?course.units:[];
 const active=nextUsefulJourney(list,state,recommendedId);
 const activeStats=active?journeyStats(state,active):{seen:0,total:0,done:false,pct:0};
 const currentIndex=active?Math.min(Number(state?.sceneByJourney?.[active.palace_id]||0)+1,active.scene_count||1):0;
 const completeCount=list.filter(j=>state?.completedJourneys?.[j.palace_id]).length;
 const visitedCount=list.reduce((sum,j)=>sum+journeyStats(state,j).seen,0);
 const totalJourneys=units.reduce((sum,u)=>sum+Number(u.journey_count||0),0);
 const totalScenes=units.reduce((sum,u)=>sum+Number(u.scene_count||0),0);
 const totalChallenges=units.reduce((sum,u)=>sum+Number(u.application_challenges||0),0);
 const cards=list.map(j=>{
   const s=journeyStats(state,j),label=s.done?'Walk it again':s.seen?'Continue journey':'Begin journey';
   return `<article class="card journey-card"><div class="journey-card-top"><span class="eyebrow">${esc(j.palace_name)}</span><span class="pill">${s.done?'Complete':s.seen?`${s.pct}%`:`${esc(j.estimated_minutes)} min`}</span></div><h3>${esc(j.story_title)}</h3><p>${esc(j.tagline)}</p><div class="journey-meta"><span>${s.total} locations</span><span>${esc(j.checkpoint_count)} optional recalls</span><span>Guide · ${esc(guideName(j))}</span></div><button class="${s.seen?'primary':'secondary'}" data-action="learn" data-id="${esc(j.palace_id)}">${label}</button></article>`;
 }).join('');
 const unitCards=units.map(u=>{
   const current=u.unit_id===unit?.unit_id;
   const theme=unitTheme(u.number);
   const challenges=Number(u.application_challenges||0);
   return `<article class="card course-unit-card ${current?'current-unit-card':''}" data-unit-card-theme="${theme}">
    <div class="course-unit-card-head"><span class="unit-number-highlight">Unit ${esc(u.number)}</span>${current?`<span class="current-unit-mark">Current</span>`:''}</div>
    <h2>${esc(u.title)}</h2>
    <div class="course-unit-stats"><span><strong>${esc(u.journey_count||0)}</strong> journeys</span><span><strong>${esc(u.scene_count||0)}</strong> locations</span><span><strong>${esc(challenges)}</strong> challenges</span></div>
    <button class="${current?'primary':'secondary'}" data-action="switch-unit" data-unit="${esc(u.unit_id)}">${current?'Selected unit':'Select Unit '+esc(u.number)}</button>
   </article>`;
 }).join('');
 const challenge=(unit?.application_challenges||0)>0?`<section class="card challenge-strip"><div><span class="eyebrow">Unit ${esc(unit.number)}</span><h2>Challenge Lab</h2><p>${esc(unit.title)} application questions.</p></div><div class="challenge-side"><strong>${esc(unit.application_challenges)} challenges</strong><button class="secondary" data-action="practice">Open challenge lab</button></div></section>`:'';
 const recommendation=active?`${activeStats.seen?`Continue at location ${currentIndex} of ${activeStats.total}`:'Start with the first location'}`:'';
 return `<main id="main-content" tabindex="-1" class="stack course-home" aria-label="AP Biology Memory Palace home">
  <section class="card course-home-hero">
   <div class="course-home-copy"><span class="course-kicker">AP Biology</span><h1>Units 1–8</h1><p>Select a unit to open its memory journeys.</p></div>
   <div class="course-home-summary" aria-label="Course totals"><div><strong>8</strong><span>units</span></div><div><strong>${totalJourneys}</strong><span>journeys</span></div><div><strong>${totalScenes}</strong><span>locations</span></div><div><strong>${totalChallenges}</strong><span>challenges</span></div></div>
  </section>

  <section class="course-units-section" aria-labelledby="course-units-title">
   <div class="course-section-heading"><div><h2 id="course-units-title">AP Biology Units</h2></div></div>
   <div class="course-unit-grid">${unitCards}</div>
  </section>

  <section class="card current-unit-panel">
   <div class="current-unit-main"><span class="current-unit-label">Current unit · Unit ${esc(unit?.number||'')}</span><h2>${esc(unit?.title||'')}</h2><p>${completeCount} of ${list.length} journeys complete · ${visitedCount} locations visited · ${dueCount} Review item${dueCount===1?'':'s'} due.</p><div class="row">${active?`<button class="primary" data-action="learn" data-id="${esc(active.palace_id)}">${activeStats.done?'Revisit':activeStats.seen?'Continue':'Begin'} ${esc(active.story_title)}</button>`:''}<button class="secondary" data-action="review">${dueCount?`Review ${dueCount} due ${dueCount===1?'memory':'memories'}`:'Open Review'}</button></div></div>
   <aside class="current-unit-progress"><span class="eyebrow">Continue</span><strong>${active?esc(active.story_title):'Choose a journey'}</strong><p>${active?esc(recommendation):'Select a journey below.'}</p><div class="metric-grid"><div class="metric"><strong>${completeCount}/${list.length}</strong><span>journeys</span></div><div class="metric"><strong>${visitedCount}</strong><span>locations</span></div><div class="metric"><strong>${dueCount}</strong><span>Review due</span></div></div></aside>
  </section>

  <section class="library-section" aria-labelledby="journey-library-title"><div class="library-heading"><div><span class="eyebrow">Unit ${esc(unit?.number||'')} journeys</span><h2 id="journey-library-title">${esc(unit?.title||'')}</h2></div></div><div class="journey-list">${cards}</div></section>
  ${challenge}
  <!-- Course map removed because the eight-unit selector above already provides course navigation. -->
 </main>`;
}
