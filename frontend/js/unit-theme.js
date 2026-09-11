const UNIT_THEMES=['yellow','green','turquoise','pink'];
const STORAGE_KEY='memory-palace-v2:progress';

function unitIdFrom(value='unit-1'){
  const match=String(value||'unit-1').match(/unit-(\d+)/i);
  return match?`unit-${Number(match[1])}`:'unit-1';
}
function themeFor(unitId){
  const number=Math.max(1,Number(unitIdFrom(unitId).split('-')[1]||1));
  return UNIT_THEMES[(number-1)%UNIT_THEMES.length];
}
function savedUnit(){
  try{
    const raw=localStorage.getItem(STORAGE_KEY);
    const parsed=raw?JSON.parse(raw):null;
    return unitIdFrom(parsed?.activeUnit||'unit-1');
  }catch{return 'unit-1'}
}
function unitFromLocation(url=location.href){
  try{
    const parsed=new URL(url,location.href);
    return unitIdFrom(parsed.searchParams.get('unit')||savedUnit());
  }catch{return savedUnit()}
}
function applyTheme(unitId=unitFromLocation()){
  document.body.dataset.unitTheme=themeFor(unitId);
  document.body.dataset.unitId=unitIdFrom(unitId);
}

const nativeReplaceState=history.replaceState.bind(history);
history.replaceState=(state,title,url)=>{
  nativeReplaceState(state,title,url);
  applyTheme(unitFromLocation(url?new URL(url,location.href).href:location.href));
};
window.addEventListener('popstate',()=>applyTheme(unitFromLocation()));
window.addEventListener('storage',event=>{if(event.key===STORAGE_KEY)applyTheme(unitFromLocation())});
applyTheme();
