const PROGRESS_KEY='memory-palace-v2:progress';
const BRAND_NAME='The Story Method';

function homeUrl(){
  const url=new URL(window.location.href);
  url.search='';
  url.hash='';
  return url.toString();
}

function goHome(){
  window.location.assign(homeUrl());
}

function clearProgress(){
  const ok=window.confirm('Clear all saved progress? This removes journey progress, Review items, visited locations, and your current position for every unit. This cannot be undone.');
  if(!ok)return;
  try{window.localStorage.removeItem(PROGRESS_KEY)}catch{}
  window.location.assign(homeUrl());
}

function applyBranding(){
  const brand=document.querySelector('.brand');
  if(brand){
    const first=brand.firstChild;
    if(first&&first.nodeType===Node.TEXT_NODE&&first.textContent!==`${BRAND_NAME} `){
      first.textContent=`${BRAND_NAME} `;
    }
    brand.setAttribute('aria-label',`Return to ${BRAND_NAME} home`);
  }

  document.querySelectorAll('.eyebrow').forEach(el=>{
    if(el.textContent.trim()==='Memory Palace')el.textContent=BRAND_NAME;
  });

  const home=document.querySelector('main[aria-label="AP Biology Memory Palace home"]');
  if(home)home.setAttribute('aria-label',`AP Biology ${BRAND_NAME} home`);
}

function enhanceShell(){
  applyBranding();
  const brand=document.querySelector('.brand');
  if(brand&&!brand.dataset.homeControl){
    brand.dataset.homeControl='true';
    brand.setAttribute('role','button');
    brand.setAttribute('tabindex','0');
    brand.setAttribute('aria-label',`Return to ${BRAND_NAME} home`);
    brand.setAttribute('title','Return to Home');
  }
  const nav=document.querySelector('.nav');
  if(nav&&!nav.querySelector('[data-clear-progress]')){
    const button=document.createElement('button');
    button.type='button';
    button.className='clear-progress-control';
    button.dataset.clearProgress='true';
    button.textContent='Clear progress';
    button.setAttribute('aria-label','Clear all saved progress');
    nav.appendChild(button);
  }
}

document.addEventListener('click',event=>{
  const brand=event.target.closest('.brand[data-home-control]');
  if(brand){event.preventDefault();goHome();return}
  const clear=event.target.closest('[data-clear-progress]');
  if(clear){event.preventDefault();clearProgress()}
});

document.addEventListener('keydown',event=>{
  const brand=event.target.closest?.('.brand[data-home-control]');
  if(!brand)return;
  if(event.key==='Enter'||event.key===' '){
    event.preventDefault();
    goHome();
  }
});

const observer=new MutationObserver(enhanceShell);
observer.observe(document.documentElement,{childList:true,subtree:true});
enhanceShell();

const style=document.createElement('style');
style.textContent=`
.brand[data-home-control]{
  display:inline-flex;
  align-items:baseline;
  gap:0;
  width:max-content;
  max-width:100%;
  padding:4px 6px 4px 2px;
  border:1px solid transparent;
  border-radius:2px;
  cursor:pointer;
  user-select:none;
}
.brand[data-home-control]:hover{
  background:#f5f5f5;
  border-color:var(--moon-rule);
}
.brand[data-home-control]:focus-visible{
  outline:2px solid #111;
  outline-offset:3px;
}
.nav .clear-progress-control{
  margin-left:4px;
  padding:8px 10px;
  color:#333;
  background:#fff;
  border:1px solid var(--moon-rule-dark);
  border-bottom:1px solid var(--moon-rule-dark);
  border-radius:3px;
  font-size:13px;
}
.nav .clear-progress-control:hover{
  color:#111;
  background:var(--moon-soft-pink);
  border-color:#b56c91;
}
@media(max-width:700px){
  .topbar{align-items:flex-start}
  .nav{gap:10px;flex-wrap:wrap}
  .nav .clear-progress-control{margin-left:0}
}
`;
document.head.appendChild(style);
