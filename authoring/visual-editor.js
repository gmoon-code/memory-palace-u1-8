/* Narrative-only scene editor. Science and curriculum IDs stay unchanged. */
(function(){
"use strict";
const $=id=>document.getElementById(id);
const PREFIX="story-method-narrative-draft-v1:";
const s={unit:"",journey:"",loadedUnit:"",loadedJourney:"",
  original:null,draft:null,hash:"",scene:0,
  selected:null,dirty:new Set(),history:[],redo:[],stale:false,timer:null,
  ticket:0,unitTicket:0};
const clone=x=>JSON.parse(JSON.stringify(x));
const key=(i,f,p)=>String(i)+":"+f+(p===undefined?"":":"+p);
function fingerprint(str){let n=2166136261;for(let i=0;i<str.length;i++){
 n^=str.charCodeAt(i);n=Math.imul(n,16777619)}return(n>>>0).toString(16)}
function notice(message){$("errorMessage").textContent=message;$("errorDialog").showModal()}
function identify(k){const match=/^(\d+):(title|scene_kicker|location_description|paragraphs)(?::(\d+))?$/.exec(k);
 if(!match)return null;return {scene:Number(match[1]),field:match[2],part:Number(match[3])}}
function valueOf(data,k){const spec=identify(k),scene=data?.scenes?.[spec?.scene];
 if(!scene)return null;return spec.field==="paragraphs"?scene.story_paragraphs?.[spec.part]:scene[spec.field]}
function change(data,k,v){const z=identify(k),scene=data?.scenes?.[z?.scene],base=s.original?.scenes?.[z?.scene];
 if(!scene||!base)return false;
 if(z.field!=="paragraphs"){scene[z.field]=v;return true}
 if(z.part>=scene.story_paragraphs.length)return false;
 scene.story_paragraphs[z.part]=v;
 if(z.part===0&&base.story_open===base.story_paragraphs[0])scene.story_open=v;
 const last=scene.story_paragraphs.length-1;
 if(z.part===last&&base.story_close===base.story_paragraphs[last])scene.story_close=v;
 return true}
function protectedData(data){const c=clone(data);
 for(const x of c.scenes||[]){for(const field of
 ["title","scene_kicker","location_description","story_paragraphs","story_open","story_close"])
 delete x[field]}return JSON.stringify(c)}
function validate(){
 if(!s.original||!s.draft)return "No journey loaded";
 if(protectedData(s.original)!==protectedData(s.draft))
 return "A protected scientific, review, or identity field has changed.";
 for(let i=0;i<s.original.scenes.length;i++){
  const a=s.original.scenes[i],b=s.draft.scenes[i];
  if(!["title","scene_kicker","location_description"].every(f=>
   typeof b[f]==="string"&&b[f].trim().length>0&&b[f].length<5000))
   return "Scene "+(i+1)+" contains an empty or overlong field.";
  if(!Array.isArray(b.story_paragraphs)||b.story_paragraphs.length!==a.story_paragraphs.length||
   b.story_paragraphs.some(p=>typeof p!=="string"||!p.trim()||p.length>6000))
   return "Scene "+(i+1)+" has invalid narrative paragraphs.";
  if(a.story_open===a.story_paragraphs[0]){
   if(b.story_open!==b.story_paragraphs[0])return "Opening narrative is not synchronized.";
  }else if(b.story_open!==a.story_open)return "Protected opening changed.";
  const last=a.story_paragraphs.length-1;
  if(a.story_close===a.story_paragraphs[last]){
   if(b.story_close!==b.story_paragraphs[last])return "Closing narrative is not synchronized.";
  }else if(b.story_close!==a.story_close)return "Protected closing changed.";
 }
 return ""}
function allKeys(){if(!s.original)return [];const result=[];
 s.original.scenes.forEach((scene,i)=>{
  for(const f of ["title","scene_kicker","location_description"])result.push(key(i,f));
  scene.story_paragraphs.forEach((_,p)=>result.push(key(i,"paragraphs",p)));
 });return result}
function recalc(){
 s.dirty=new Set(allKeys().filter(k=>valueOf(s.original,k)!==valueOf(s.draft,k)));
 const count=s.dirty.size;
 $("saveStatus").textContent=count?count+" edited narrative fields · Local draft":
   s.stale?"Old draft exists; original shown":"No changes · Not published";
 $("reset").disabled=!count;$("review").disabled=!count;
 $("export").disabled=!count||!!validate();
 $("undo").disabled=!s.history.length;
 $("redo").disabled=!s.redo.length;
}
function checkpoint(){if(!s.draft)return;const json=JSON.stringify(s.draft);
 if(s.history.at(-1)?.json===json)return;s.history.push({json,scene:s.scene});
 if(s.history.length>25)s.history.shift();recalc()}
function save(){
 // The picker can already point to a different journey when the outgoing
 // draft is saved. Its file identity must come from the successfully loaded
 // data, never the current picker values.
 if(!s.loadedUnit||!s.loadedJourney||!s.draft)return;
 const name=PREFIX+s.loadedUnit+":"+s.loadedJourney;
 try{
  if(!s.dirty.size){if(!s.stale)localStorage.removeItem(name);return}
  localStorage.setItem(name,JSON.stringify({version:1,hash:s.hash,
   changes:[...s.dirty].map(k=>({key:k,text:valueOf(s.draft,k)}))}));
  $("saveStatus").textContent="Draft saved in this browser · Not published";
 }catch{$("saveStatus").textContent="Storage unavailable; export to retain changes"}}
function queue(){clearTimeout(s.timer);s.timer=setTimeout(save,600)}
function restore(){
 try{const raw=localStorage.getItem(PREFIX+s.loadedUnit+":"+s.loadedJourney);if(!raw)return;
  const d=JSON.parse(raw);if(!Array.isArray(d.changes)||d.version!==1)return;
  if(d.hash!==s.hash){s.stale=true;return}
  for(const c of d.changes)if(identify(c.key)&&typeof c.text==="string")
    change(s.draft,c.key,c.text);
  if(validate())s.draft=clone(s.original);
 }catch{s.draft=clone(s.original)}}
function searchLabel(k) {
 const entry=identify(k);
 if(!entry)return "Narrative";
 const field={
  title:"Scene title",scene_kicker:"Scene kicker",
  location_description:"Location description",paragraphs:"Paragraph"
 }[entry.field]||"Narrative";
 return field+(entry.field==="paragraphs"?" "+(entry.part+1):"");
}
function refreshNarrativeSearch(){
 const results=$("searchResults"),status=$("searchStatus");
 if(!results||!status)return;
 results.replaceChildren();
 const query=$("narrativeSearch").value.trim().toLocaleLowerCase();
 if(!query){
  status.textContent="Search scene titles, descriptions, and paragraphs.";
  return;
 }
 if(!s.draft){
  status.textContent="Choose a journey before searching.";
  return;
 }
 const matches=[];
 for(const k of allKeys()){
  const text=String(valueOf(s.draft,k)||"");
  const index=text.toLocaleLowerCase().indexOf(query);
  if(index>=0)matches.push({key:k,text,index,scene:identify(k).scene});
 }
 status.textContent=matches.length?
  matches.length+" matching narrative field"+(matches.length===1?"":"s")+
  " in this journey. Select a result to edit.":
  "No matching narrative fields in this journey.";
 for(const item of matches.slice(0,60)){
  const button=document.createElement("button");button.type="button";
  button.setAttribute("role","listitem");
  const heading=document.createElement("strong");
  heading.textContent="Scene "+(item.scene+1)+" · "+searchLabel(item.key);
  const snippet=document.createElement("span");
  const start=Math.max(0,item.index-42),end=Math.min(item.text.length,item.index+query.length+65);
  snippet.textContent=(start?"…":"")+
   item.text.slice(start,end).replace(/\s+/g," ")+(end<item.text.length?"…":"");
  button.append(heading,snippet);
  button.addEventListener("click",()=>{
   if(s.scene!==item.scene){s.scene=item.scene;render();}
   select(item.key);
  });
  results.appendChild(button);
 }
 if(matches.length>60)status.textContent+=" First 60 results shown.";
}
function sceneButtons(){
 const nav=$("sceneList");nav.replaceChildren();
 s.draft.scenes.forEach((scene,i)=>{
  const button=document.createElement("button");button.type="button";
  button.textContent=(i+1)+". "+scene.title;
  if(i===s.scene)button.setAttribute("aria-current","true");
  const changed=[...s.dirty].filter(k=>k.startsWith(i+":")).length;
  if(changed){const small=document.createElement("span");
   small.textContent=changed+" edited fields";button.appendChild(small)}
  button.addEventListener("click",()=>{s.scene=i;render()});
  nav.appendChild(button)});
}
/* Mirror the student reading view. Build emphasis with DOM nodes and
   textContent, so narrative text cannot inject HTML into the editor. */
function renderInline(node,source){
 node.replaceChildren();
 const tokens=String(source).split(/(\*\*[^*]+\*\*)/g);
 for(const token of tokens){
  if(token.startsWith("**")&&token.endsWith("**")&&token.length>4){
   const strong=document.createElement("strong");
   strong.className="story-term";
   strong.textContent=token.slice(2,-2);
   node.appendChild(strong);
  }else node.appendChild(document.createTextNode(token));
 }
}
function previewElement(tag,className,k,text){
 const el=document.createElement(tag);el.className=className;
 el.dataset.editKey=k;
 if(k.includes(":paragraphs:"))renderInline(el,text);
 else el.textContent=text;
 return el}
function render(){
 const box=$("scenePreview");box.replaceChildren();s.selected=null;$("editingControls").hidden=true;
 const scene=s.draft?.scenes?.[s.scene];if(!scene)return;
 $("journeyLabel").textContent="Scene "+(s.scene+1)+" of "+s.draft.scenes.length+
   " · "+scene.locus;
 $("journeyTitle").textContent=s.draft.story_title||s.draft.palace_name;
 box.append(
   previewElement("p","kicker",key(s.scene,"scene_kicker"),scene.scene_kicker),
   previewElement("h3","title",key(s.scene,"title"),scene.title),
   previewElement("p","location",key(s.scene,"location_description"),scene.location_description)
 );
 const prose=document.createElement("div");prose.className="narrative";
 scene.story_paragraphs.forEach((text,p)=>
   prose.appendChild(previewElement("p","",key(s.scene,"paragraphs",p),text)));
 box.appendChild(prose);sceneButtons();recalc();refreshNarrativeSearch()}
function select(k){
 const el=document.querySelector('[data-edit-key="'+k+'"]');if(!el)return;
 document.querySelectorAll("[data-selected]").forEach(n=>{
  n.removeAttribute("data-selected");n.removeAttribute("contenteditable");
  if(n.dataset.editKey?.includes(":paragraphs:"))
   renderInline(n,valueOf(s.draft,n.dataset.editKey));
 });
 s.selected=k;el.setAttribute("data-selected","");
 // The author edits original Markdown text. Read mode stays formatted.
 if(k.includes(":paragraphs:"))el.textContent=valueOf(s.draft,k);
 el.setAttribute("contenteditable","plaintext-only");
 $("editingControls").hidden=false;$("editText").value=valueOf(s.draft,k);
 $("selectionStatus").textContent="Scene "+(identify(k).scene+1)+" · "+searchLabel(k);
 updateFieldNavigation();
 el.focus({preventScroll:true})}
function updateFieldNavigation(){
 const fields=allKeys(),index=fields.indexOf(s.selected);
 $("previousField").disabled=index<=0;
 $("nextField").disabled=index<0||index===fields.length-1;
 $("fieldPosition").textContent=index>=0?
  "Editable field "+(index+1)+" of "+fields.length+" in this journey.":"";
}
function navigateField(direction){
 const fields=allKeys(),index=fields.indexOf(s.selected);
 if(index<0)return;
 const next=fields[index+direction];if(!next)return;
 const scene=identify(next).scene;
 if(scene!==s.scene){s.scene=scene;render()}
 select(next);
}
function sync(k,v){
 if(valueOf(s.draft,k)===v)return;
 if(!change(s.draft,k,v))return;
 s.redo.length=0;
 recalc();queue();sceneButtons();refreshNarrativeSearch()}
function pastePlain(event){
 const node=event.target.closest("[data-edit-key][contenteditable]");
 if(!node)return;event.preventDefault();
 const selection=window.getSelection();if(!selection?.rangeCount)return;
 const range=selection.getRangeAt(0);if(!node.contains(range.commonAncestorContainer))return;
 range.deleteContents();const text=document.createTextNode(event.clipboardData?.getData("text/plain")||"");
 range.insertNode(text);range.setStartAfter(text);range.collapse(true);
 selection.removeAllRanges();selection.addRange(range);
 node.dispatchEvent(new Event("input",{bubbles:true}))}
function revertField(){if(!s.selected)return;checkpoint();
 s.redo.length=0;
 change(s.draft,s.selected,valueOf(s.original,s.selected));recalc();queue();render()}
function undo(){const entry=s.history.pop();if(!entry)return;
 s.redo.push({json:JSON.stringify(s.draft),scene:s.scene});
 s.draft=JSON.parse(entry.json);s.scene=entry.scene;recalc();render();queue()}
function redo(){const entry=s.redo.pop();if(!entry)return;
 s.history.push({json:JSON.stringify(s.draft),scene:s.scene});
 if(s.history.length>25)s.history.shift();
 s.draft=JSON.parse(entry.json);s.scene=entry.scene;recalc();render();queue()}
function reset(){if(!s.dirty.size||!confirm("Discard this journey's narrative draft?"))return;
 s.draft=clone(s.original);s.history=[];s.redo=[];s.stale=false;recalc();render();save()}
function review(){
 const list=$("reviewList");list.replaceChildren();
 $("reviewSummary").textContent=s.dirty.size+" edited narrative fields in "+s.journey+".";
 for(const k of s.dirty){
  const div=document.createElement("section");div.className="review-change";
  const title=document.createElement("strong");title.textContent="Scene "+
    (identify(k).scene+1)+" · "+k.split(":").slice(1).join(" ");
  const old=document.createElement("p");old.className="old";
  old.textContent="Before: "+valueOf(s.original,k);
  const next=document.createElement("p");next.textContent="After: "+valueOf(s.draft,k);
  div.append(title,old,next);list.appendChild(div)}
 const problem=validate();$("reviewValidation").textContent=problem?
  "Export blocked. "+problem:"Protected curriculum fields match the source.";
 $("reviewDialog").showModal()}
function exportFile(){
 const problem=validate();if(problem){notice(problem);return}
 const contents=JSON.stringify(s.draft,null,2)+"\n";
 const url=URL.createObjectURL(new Blob([contents],{type:"application/json"}));
 const link=document.createElement("a");link.href=url;link.download=s.journey+".json";
 document.body.appendChild(link);link.click();link.remove();
 setTimeout(()=>URL.revokeObjectURL(url),10000);
 $("saveStatus").textContent="JSON exported · Not published"}
async function fetchData(relative){
 const url=new URL("../content/ap-biology/"+relative,location.href);
 const result=await fetch(url,{cache:"no-store",credentials:"same-origin"});
 if(!result.ok)throw Error("HTTP "+result.status+" for "+relative);
 const text=await result.text();return {raw:text,data:JSON.parse(text)}}
async function loadJourney(){
 if(s.draft)save();
 const unit=s.unit,j=s.journey;
 if(!/^unit-[1-8]$/.test(unit)||!/^[A-Za-z0-9-]+$/.test(j))return;
 const ticket=++s.ticket;$("saveStatus").textContent="Loading…";
 $("narrativeSearch").value="";
 $("searchResults").replaceChildren();
 $("searchStatus").textContent="Loading journey narrative…";
 try{
  const data=await fetchData(unit+"/journeys/"+j+".json");
  if(ticket!==s.ticket)return;
  if(data.data.palace_id!==j||!Array.isArray(data.data.scenes))
   throw Error("Journey identity was not recognized.");
  s.original=data.data;s.draft=clone(data.data);
  s.loadedUnit=unit;s.loadedJourney=j;s.hash=fingerprint(data.raw);
   s.scene=0;s.history=[];s.redo=[];s.stale=false;restore();recalc();render();
 }catch(e){notice(e.message);$("saveStatus").textContent="Load failed"}}
async function loadUnit(unit){
 if(s.draft)save();
 if(!/^unit-[1-8]$/.test(unit))return;
 const unitTicket=++s.unitTicket;
 const file=unit==="unit-1"?"journeys.json":"journeys-f5.json";
 const registry=(await fetchData(unit+"/"+file)).data;
 if(unitTicket!==s.unitTicket)return;
 const select=$("journey");select.replaceChildren();
 for(const item of registry.guided_journeys||[]){
  if(!/^[A-Za-z0-9-]+$/.test(item.palace_id||""))continue;
  const opt=document.createElement("option");opt.value=item.palace_id;
  opt.textContent=item.palace_id+" · "+(item.story_title||item.palace_name);
  select.appendChild(opt)}
 s.unit=unit;s.journey=select.value;await loadJourney()}
async function init(){
 try{
  const course=(await fetchData("course.json")).data;
  const picker=$("unit");for(const item of course.units||[]){
   if(!/^unit-[1-8]$/.test(item.unit_id))continue;
   const option=document.createElement("option");option.value=item.unit_id;
   option.textContent="Unit "+item.number+" · "+item.title;picker.appendChild(option)}
  await loadUnit(picker.value);
 }catch(e){notice(e.message);$("saveStatus").textContent="Course failed to load"}
 $("unit").addEventListener("change",event=>loadUnit(event.target.value).catch(e=>notice(e.message)));
 $("journey").addEventListener("change",event=>{
  s.journey=event.target.value;loadJourney()});
 $("narrativeSearch").addEventListener("input",refreshNarrativeSearch);
 $("viewport").addEventListener("change",event=>{
  $("scenePreview").className="scene-preview "+event.target.value});
 $("scenePreview").addEventListener("click",event=>{
  const el=event.target.closest("[data-edit-key]");if(el)select(el.dataset.editKey)});
 $("scenePreview").addEventListener("focusin",event=>{
  if(event.target.closest("[data-edit-key]"))checkpoint()});
 $("scenePreview").addEventListener("keydown",event=>{
  if(event.key==="Enter"&&event.target.closest('[data-edit-key][contenteditable]'))
   event.preventDefault()});
 $("scenePreview").addEventListener("paste",pastePlain);
 $("scenePreview").addEventListener("focusout",event=>{
  const el=event.target.closest("[data-edit-key]");
  if(!el||!el.dataset.editKey?.includes(":paragraphs:"))return;
  // Keep the original Markdown in the model; restore formatted reading
  // whenever editing focus moves away from the paragraph.
  el.removeAttribute("contenteditable");
  renderInline(el,valueOf(s.draft,el.dataset.editKey));
 });
 $("scenePreview").addEventListener("input",event=>{
  const el=event.target.closest("[data-edit-key]");if(!el)return;
  const v=el.textContent;sync(el.dataset.editKey,v);
  if(s.selected===el.dataset.editKey)$("editText").value=v});
 $("editText").addEventListener("focus",checkpoint);
 $("editText").addEventListener("input",event=>{
  if(!s.selected)return;const v=event.target.value;
  const el=document.querySelector('[data-edit-key="'+s.selected+'"]');
  if(el){
   if(s.selected.includes(":paragraphs:")&&document.activeElement!==el){
    el.removeAttribute("contenteditable");
    renderInline(el,v);
   }else el.textContent=v;
  }
  sync(s.selected,v)});
 $("revertField").addEventListener("click",revertField);
 $("previousField").addEventListener("click",()=>navigateField(-1));
 $("nextField").addEventListener("click",()=>navigateField(1));
 $("undo").addEventListener("click",undo);
 $("redo").addEventListener("click",redo);
 $("reset").addEventListener("click",reset);
 $("review").addEventListener("click",review);
 $("export").addEventListener("click",exportFile);
 window.addEventListener("beforeunload",()=>{if(s.draft)save()});
}
document.addEventListener("DOMContentLoaded",init);
})();