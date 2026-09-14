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

const app=document.querySelector('#app');
if(app){
  new MutationObserver(queuePolish).observe(app,{childList:true,subtree:true});
}
polishRoute(document);
