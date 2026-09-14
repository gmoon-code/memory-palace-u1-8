function fitLevel(text,medium=13,long=20,xlong=29){
  const n=String(text||'').replace(/\s+/g,'').length;
  if(n>=xlong)return'xlong';
  if(n>=long)return'long';
  if(n>=medium)return'medium';
  return'short';
}

function addBreakOpportunities(el){
  if(!el||el.dataset.breaksAdded==='true')return;
  const text=el.textContent||'';
  const frag=document.createDocumentFragment();
  const parts=text.split(/([→↔⇄⇌—–\/|])/g);
  for(const part of parts){
    if(!part)continue;
    frag.append(document.createTextNode(part));
    if(/^[→↔⇄⇌—–\/|]$/.test(part))frag.append(document.createElement('wbr'));
  }
  el.replaceChildren(frag);
  el.dataset.breaksAdded='true';
}

function polishRoute(root=document){
  root.querySelectorAll('.route-node').forEach(node=>{
    const symbol=node.querySelector('.route-symbol');
    const name=node.querySelector(':scope > strong');
    if(symbol){
      const raw=symbol.textContent.trim();
      symbol.dataset.fit=fitLevel(raw,12,19,28);
      addBreakOpportunities(symbol);
    }
    if(name){
      const raw=name.textContent.trim();
      name.dataset.fit=fitLevel(raw,22,31,43);
    }
  });
}

let queued=false;
function queuePolish(){
  if(queued)return;
  queued=true;
  requestAnimationFrame(()=>{
    queued=false;
    polishRoute(document);
  });
}

/*
  Scene-to-scene reading position
  -------------------------------
  The Learn view re-renders the whole page whenever Previous scene or
  Continue story is used. app.js deliberately focuses the new main element,
  which resets the document to the top. Capture the intent before that render,
  then restore the learner to the newly rendered Follow what happens heading.
  Keeping this in an already-loaded runtime file also makes the behavior work
  in both the GitHub Pages build and the server shell.
*/
let storyNavigationPending=false;
let storyScrollQueued=false;

function queueStoryScroll(){
  if(!storyNavigationPending||storyScrollQueued)return;
  storyScrollQueued=true;
  requestAnimationFrame(()=>requestAnimationFrame(()=>{
    storyScrollQueued=false;
    if(!storyNavigationPending)return;
    storyNavigationPending=false;

    const heading=document.querySelector('.narrative-section .section-heading');
    if(!heading)return;

    const top=heading.getBoundingClientRect().top+window.scrollY-16;
    try{window.scrollTo({top:Math.max(0,top),left:0,behavior:'auto'})}
    catch{window.scrollTo?.(0,Math.max(0,top))}

    const focusTarget=heading.querySelector('h3')||heading;
    focusTarget.setAttribute('tabindex','-1');
    try{focusTarget.focus({preventScroll:true})}catch{/* focus is optional */}
  }));
}

document.addEventListener('click',event=>{
  const button=event.target.closest?.('[data-action="previous-scene"],[data-action="next-scene"]');
  if(!button)return;

  /* Only the controls under the visible story should preserve the story
     reading position. Quick Recall uses its own compact screen. */
  if(!button.closest('.story-card'))return;

  storyNavigationPending=true;
},true);

const app=document.querySelector('#app');
if(app){
  new MutationObserver(()=>{
    queuePolish();
    queueStoryScroll();
  }).observe(app,{childList:true,subtree:true});
}
polishRoute(document);
