function escapeHtml(value=''){return String(value).replace(/[&<>'"]/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[ch]))}
function rich(value=''){return escapeHtml(value).replace(/\*\*(.+?)\*\*/g,'<strong class="story-term">$1</strong>')}
function routeStrip(journey,index,visited=[]){
  const route=journey.route||journey.scenes.map((s,i)=>({scene_index:i,locus:s.locus,short:s.locus,floor:`Scene ${i+1}`,symbol:'•'}));
  const seen=new Set((visited||[]).map(Number));
  return `<div class="route-wrap" aria-label="Journey route"><div class="route-label"><span>Journey route</span><strong>${escapeHtml(journey.route_orientation||'Follow the route in order.')}</strong></div><div class="route-strip" style="--route-count:${Math.max(3,route.length)}">${route.map((r,i)=>{const isCurrent=i===index,isVisited=seen.has(i)||i<index,canOpen=isCurrent||isVisited;return `<button type="button" class="route-node ${isCurrent?'current':isVisited?'visited':''}" ${isCurrent?'aria-current="step"':''} ${canOpen?`data-action="route-scene" data-index="${i}"`:'disabled'} aria-label="${isCurrent?'Current location':isVisited?'Visited location':'Upcoming location'} ${i+1}, ${escapeHtml(r.short||r.locus)}"><span class="route-symbol">${escapeHtml(r.symbol||'•')}</span><span class="route-floor">${escapeHtml(r.floor||'')}</span><strong>${escapeHtml(r.short||r.locus)}</strong></button>`}).join('')}</div></div>`;
}
function layoutStage(scene){
  const layout=scene.scene_layout||{};
  return `<section class="scene-orientation"><div class="orientation-copy"><span class="eyebrow">Where you are</span><h2>${escapeHtml(scene.locus)}</h2><p>${escapeHtml(scene.location_description||'')}</p><p class="orientation-line">${escapeHtml(layout.orientation||'')}</p></div><div class="scene-stage">${(layout.zones||[]).map(z=>`<div class="stage-zone ${escapeHtml(z.position||'center')}"><span class="stage-symbol" aria-hidden="true">${escapeHtml(z.symbol||'•')}</span><span class="stage-position">${escapeHtml(z.position||'')}</span><strong>${escapeHtml(z.label||'')}</strong><p>${escapeHtml(z.description||'')}</p></div>`).join('')}</div></section>`;
}
function castPanel(scene){
  const cast=scene.cast||[];if(!cast.length)return'';
  return `<section class="cast-section"><div class="section-heading"><span class="eyebrow">Who and what are here</span><h3>Meet the scene</h3></div><div class="cast-grid">${cast.map(c=>`<article class="cast-card"><span class="cast-kind">${escapeHtml(c.kind||'')}</span><h4>${escapeHtml(c.name||'')}</h4><p><strong>Picture it</strong> · ${escapeHtml(c.visual||'')}</p><p><strong>Job</strong> · ${escapeHtml(c.job||'')}</p></article>`).join('')}</div></section>`;
}
function storyPanel(scene){
  const paragraphs=(scene.story_paragraphs&&scene.story_paragraphs.length)?scene.story_paragraphs:[scene.story_open,...(scene.story_beats||[]).map(b=>b.story),scene.story_close].filter(Boolean);
  return `<section class="narrative-section"><div class="section-heading"><span class="eyebrow">Follow what happens</span><h3>${escapeHtml(scene.scene_kicker||'The story continues.')}</h3></div><div class="story-prose">${paragraphs.map((p,i)=>`<p class="story-paragraph ${i===0?'lead':''}">${rich(p)}</p>`).join('')}</div></section>`;
}
function memoryPanel(scene){
  const items=scene.memory_snapshot||scene.story_beats||[];
  return `<details class="memory-panel"><summary><span><span class="eyebrow">Optional memory anchors</span><strong>${items.length} anchor${items.length===1?'':'s'} to revisit after the story</strong></span><span class="summary-chevron" aria-hidden="true">⌄</span></summary><div class="memory-grid">${items.map(x=>`<article class="memory-anchor"><h4>${escapeHtml(x.term||'')}</h4><p>${escapeHtml(x.meaning||x.science||'')}</p><div class="memory-image"><span>Picture</span>${escapeHtml(x.image||x.hint||'')}</div></article>`).join('')}</div></details>`;
}
function progressBar(value,label){return `<div class="progress" role="progressbar" aria-label="${escapeHtml(label)}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${value}"><span style="width:${value}%"></span></div>`}
function recallView(journey,index,scene){
  const pct=Math.round(((index+1)/journey.scenes.length)*100);
  return `<main id="main-content" tabindex="-1" class="story-shell recall-shell"><div class="recall-progress"><span>${index+1} of ${journey.scenes.length}</span>${progressBar(pct,'Journey progress')}</div><article class="card recall-card"><span class="eyebrow">Quick recall · story hidden</span><h1>Picture the scene before you answer.</h1><p class="recall-prompt">${escapeHtml(scene.checkpoint_prompt)}</p><p class="muted">The story, location name, and memory anchors are hidden for a real retrieval attempt. A hint can help, and the app will remember that the attempt was assisted.</p><div class="recall-actions"><button class="primary" data-action="remembered" data-object="${escapeHtml(scene.checkpoint_object_id)}">I remembered it</button><button class="secondary" data-action="hint" data-object="${escapeHtml(scene.checkpoint_object_id)}">Give me one hint</button></div><div id="recallHint" class="feedback-region" aria-live="polite"></div><div class="story-actions"><button class="ghost" data-action="cancel-recall">← Back to story</button><button class="ghost" data-action="next-scene">Skip this recall and continue →</button></div></article></main>`;
}
export function learnView(journey,index,recallOpen=false,visited=[]){
 const safeIndex=Math.max(0,Math.min(Number(index)||0,journey.scenes.length-1)),scene=journey.scenes[safeIndex];
 if(recallOpen)return recallView(journey,safeIndex,scene);
 const pct=Math.round(((safeIndex+1)/journey.scenes.length)*100),checkpoint=scene.checkpoint?`<button class="secondary" data-action="open-recall">Quick recall <span class="optional-label">optional · ~20 sec</span></button>`:'';
 const guide=journey.guide&&typeof journey.guide==='object'?journey.guide:{name:journey.guide||'Your guide',role:'story guide',visual:'',story_job:''};
 return `<main id="main-content" tabindex="-1" class="story-shell">
   <section class="journey-banner card"><div><span class="eyebrow">${escapeHtml(journey.story_title)}</span><h1>${escapeHtml(scene.title)}</h1><p>${escapeHtml(journey.mission||'')}</p></div><div class="guide-chip"><span class="guide-dot" aria-hidden="true">${escapeHtml((guide.name||'G').charAt(0).toUpperCase())}</span><div><span>Your guide</span><strong>${escapeHtml(guide.name)}</strong><small>${escapeHtml(guide.role||'')}</small></div></div></section>
   <div class="story-top"><div><span class="eyebrow">Scene ${safeIndex+1}</span><strong>${escapeHtml(scene.locus)}</strong></div><span class="muted">${safeIndex+1} / ${journey.scenes.length}</span></div>
   ${progressBar(pct,'Journey progress')}
   ${routeStrip(journey,safeIndex,visited)}
   <article class="card story-card">
     ${layoutStage(scene)}
     ${castPanel(scene)}
     ${storyPanel(scene)}
     <div class="listen-row"><button class="secondary" data-action="listen">▶ Listen to the story</button><button class="ghost" data-action="stop-audio">Stop</button><span class="muted" id="audioStatus" aria-live="polite">Close your eyes if that makes the scene easier to picture.</span></div>
     ${memoryPanel(scene)}
     <div class="story-actions"><button class="ghost" data-action="home">Leave journey</button><div class="row">${safeIndex>0?`<button class="secondary" data-action="previous-scene">← Previous scene</button>`:''}${checkpoint}<button class="primary" data-action="next-scene">${safeIndex===journey.scenes.length-1?'Finish journey':'Continue story →'}</button></div></div>
   </article>
 </main>`;
}
export function sceneSpeech(journey,index){const s=journey.scenes[index];const paragraphs=(s.story_paragraphs&&s.story_paragraphs.length)?s.story_paragraphs:[s.story_open,...(s.story_beats||[]).map(b=>b.story),s.story_close].filter(Boolean);return paragraphs.join(' ').replace(/\*\*/g,'')}
