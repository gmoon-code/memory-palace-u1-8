import {chromium} from "playwright";
import assert from "node:assert/strict";
import {mkdir,readFile} from "node:fs/promises";
const origin=process.env.STORY_EDITOR_TEST_URL||"http://127.0.0.1:8765";
const browser=await chromium.launch({headless:true});
const ctx=await browser.newContext({acceptDownloads:true,viewport:{width:1400,height:950}});
const page=await ctx.newPage(),errors=[];
page.on("pageerror",e=>errors.push(e.message));
await mkdir("/tmp/story-editor-artifacts",{recursive:true});

async function downloadJourney(expected){
 const pending=page.waitForEvent("download");
 await page.locator("#export").click();
 const file=await pending;
 assert.equal(file.suggestedFilename(),expected+".json");
 const data=JSON.parse(await readFile(await file.path(),"utf8"));
 return data;
}
try{
 await page.goto(origin+"/editor.html",{waitUntil:"domcontentloaded"});
 await page.waitForURL("**/authoring/visual-editor.html");
 await page.locator('#scenePreview [data-edit-key="0:title"]').waitFor();
 const otherEditors=await page.locator('.other-editors nav a').evaluateAll(
   links=>links.map(link=>({
     pathname:new URL(link.href).pathname,
     target:link.target,
     noopener:link.rel.split(/\s+/).includes('noopener')
   }))
 );
 assert.deepEqual(otherEditors,[
   {pathname:'/editor.html',target:'_blank',noopener:true},
   {pathname:'/research-methods/editor.html',target:'_blank',noopener:true}
 ]);
 const hubLink=page.locator('.other-editors a[href="../../editors.html"]');
 assert.equal(await hubLink.count(),1);
 assert.equal(await hubLink.getAttribute('target'),'_blank');
 assert.match(await hubLink.getAttribute('rel'),/noopener/);
 assert.equal(await hubLink.evaluate(link=>new URL(link.href).pathname),'/editors.html');
 assert.equal(await page.locator('.other-editors').isVisible(),true);
 assert.equal(await page.locator("#unit").inputValue(),"unit-1");
 assert.equal(await page.locator("#journey").inputValue(),"Z1");
 assert.equal(await page.locator("#sceneList button").count(),9);
 const original=await (await page.request.get(origin+"/content/ap-biology/unit-1/journeys/Z1.json")).json();
 assert.equal(await page.locator("#export").isDisabled(),true);
 // Search inspects editable narrative fields across scenes without changing
 // the protected curriculum or creating an unpublished draft.
 await page.locator("#narrativeSearch").fill("observation");
 assert(await page.locator("#searchResults button").count()>0,
   "Search should find narrative text beyond the current selection");
 assert.match(await page.locator("#searchStatus").textContent(),/matching narrative field/);
 await page.locator("#searchResults button").first().click();
 assert.equal(await page.locator("#editingControls").isVisible(),true);
 assert.match(await page.locator("#editText").inputValue(),/observation/i);
 assert.equal(await page.locator("#export").isDisabled(),true,
   "Selecting a search result should not edit the curriculum");
 await page.locator("#narrativeSearch").fill("phrase-never-present-90210");
 assert.equal(await page.locator("#searchResults button").count(),0);
 assert.match(await page.locator("#searchStatus").textContent(),/No matching narrative fields/);
 await page.locator("#narrativeSearch").fill("");
 // Review-before-replace updates only editable narrative content and
 // must preserve the protected journey and offer a single-step undo.
 await page.locator(".narrative-replace summary").click();
 await page.locator("#narrativeSearch").fill(original.scenes[0].title.toUpperCase());
 await page.locator("#narrativeReplaceWith").fill("Temporary heading for search replace");
 await page.locator("#reviewReplace").click();
 await page.locator("#replaceDialog").waitFor({state:"visible"});
 assert.match(await page.locator("#replaceSummary").textContent(),/1 replacement across 1 editable narrative field/);
 assert.match(await page.locator("#replaceChanges .replace-before").textContent(),/Before/);
 assert.match(await page.locator("#replaceChanges .replace-after").textContent(),/Temporary heading for search replace/);
 assert.equal(await page.locator("#export").isDisabled(),true);
 await page.locator('#replaceDialog button:has-text("Cancel")').click();
 assert.equal(await page.locator("#export").isDisabled(),true,
   "Cancelling bulk replacement must preserve the original draft");
 await page.locator("#reviewReplace").click();
 await page.locator("#replaceDialog").waitFor({state:"visible"});
 await page.locator("#applyReplace").click();
 assert.equal(await page.locator('[data-edit-key="0:title"]').textContent(),
   "Temporary heading for search replace");
 assert.equal(await page.locator("#export").isEnabled(),true);
 await page.locator("#undo").click();
 assert.equal(await page.locator('[data-edit-key="0:title"]').textContent(),
   original.scenes[0].title);
 await page.locator("#redo").click();
 assert.equal(await page.locator('[data-edit-key="0:title"]').textContent(),
   "Temporary heading for search replace");
 await page.locator("#undo").click();
 assert.equal(await page.locator("#export").isDisabled(),true,
   "Undo must restore the entire unchanged journey");
 await page.locator("#narrativeReplaceWith").fill("");
 await page.locator("#reviewReplace").click();
 assert.match(await page.locator("#replaceStatus").textContent(),/Replacement blocked/,
   "Replacing the complete title with empty text must fail schema validation");
 assert.equal(await page.locator("#replaceDialog").isVisible(),false);
 await page.locator("#narrativeSearch").fill("");
 const emphasized=page.locator('[data-edit-key="0:paragraphs:1"]');
 assert(await emphasized.locator("strong.story-term").count()>0,
   "Narrative Markdown should render as accessible emphasis in reading preview");
 assert(!(await emphasized.textContent()).includes("**observation**"),
   "Reading preview should hide Markdown source markers");
 await emphasized.click();
 assert((await page.locator("#editText").inputValue()).includes("**observation**"),
   "The inspector must keep the exact editable Markdown source");
 assert.match(await page.locator("#fieldPosition").textContent(),/Editable field 5 of /);
 await page.locator("#previousField").click();
 assert.equal(await page.locator('[data-edit-key="0:paragraphs:0"][data-selected]').count(),1);
 await page.locator("#nextField").click();
 assert.equal(await page.locator('[data-edit-key="0:paragraphs:1"][data-selected]').count(),1);
 await page.locator('[data-edit-key="0:scene_kicker"]').click();
 assert.equal(await page.locator("#previousField").isDisabled(),true,
   "Previous must stop at the first editable narrative field");
 const lastParagraph=original.scenes[0].story_paragraphs.length-1;
 await page.locator('[data-edit-key="0:paragraphs:'+lastParagraph+'"]').click();
 await page.locator("#nextField").click();
 assert.equal(await page.locator('[data-edit-key="1:scene_kicker"][data-selected]').count(),1,
   "Next must continue into the next scene");
 assert.match(await page.locator("#journeyLabel").textContent(),/Scene 2 of /);
 await page.locator("#previousField").click();
 assert.equal(await page.locator(
   '[data-edit-key="0:paragraphs:'+lastParagraph+'"][data-selected]').count(),1,
   "Previous must return to the previous scene's final paragraph");
 assert.equal(await page.locator("#export").isDisabled(),true,
   "Field navigation must never edit student narrative");
 const title=page.locator('[data-edit-key="0:title"]');
 await title.click();
 assert.equal(await page.locator("#originalFieldText").textContent(),original.scenes[0].title,
   "The inspector must expose the exact original narrative when comparison is requested");
 await page.locator(".original-field-compare summary").click();
 assert.equal(await page.locator("#originalFieldText").isVisible(),true);
 await page.locator("#editText").fill("The Observation That Begins the Investigation");
 assert.equal((await title.textContent()).trim(),"The Observation That Begins the Investigation");
 assert.equal(await page.locator("#originalFieldText").textContent(),original.scenes[0].title,
   "Editing a draft must never overwrite its comparison baseline");
 assert.match(await page.locator("#selectionLength").textContent(),/of 4999 permitted characters/);
 assert.equal(await page.locator("#export").isEnabled(),true);
 assert.equal(await page.locator("#redo").isDisabled(),true);
 await page.locator("#undo").click();
 assert.equal((await page.locator('[data-edit-key="0:title"]').textContent()).trim(),
   original.scenes[0].title,"Undo must restore the original narrative");
 assert.equal(await page.locator("#redo").isEnabled(),true);
 await page.locator("#redo").click();
 assert.equal((await page.locator('[data-edit-key="0:title"]').textContent()).trim(),
   "The Observation That Begins the Investigation","Redo must restore the edited narrative");
 assert.equal(await page.locator("#redo").isDisabled(),true);
 await page.locator("#undo").click();
 await page.locator('[data-edit-key="0:title"]').click();
 await page.locator("#editText").fill("A different draft after undo");
 assert.equal(await page.locator("#redo").isDisabled(),true,
   "A new narrative edit must invalidate old redo history");
 await page.locator("#editText").fill("The Observation That Begins the Investigation");
 await page.locator("#review").click();
 assert.match(await page.locator("#reviewValidation").textContent(),/Protected curriculum fields match/);
 await page.locator("#reviewDialog button").click();
 const edited=await downloadJourney("Z1");
 assert.equal(edited.scenes[0].title,"The Observation That Begins the Investigation");
 assert.deepEqual(edited.scenes[0].object_ids,original.scenes[0].object_ids);
 assert.deepEqual(edited.scenes[0].story_beats,original.scenes[0].story_beats);
 assert.deepEqual(edited.scenes[0].memory_snapshot,original.scenes[0].memory_snapshot);
 assert.deepEqual(edited.scenes[0].checkpoint,original.scenes[0].checkpoint);
 assert.deepEqual(edited.route,original.route);

 await page.waitForTimeout(700);
 await page.reload();
 await page.locator('[data-edit-key="0:title"]').waitFor();
 assert.equal((await page.locator('[data-edit-key="0:title"]').textContent()).trim(),
   "The Observation That Begins the Investigation");

 page.once("dialog",dialog=>dialog.accept());
 await page.locator("#reset").click();
 assert.equal((await page.locator('[data-edit-key="0:title"]').textContent()).trim(),
   original.scenes[0].title);

 // The downloaded narrative can restore the selected journey's local draft.
 // Previewing and cancelling the import may not change any content.
 const upload={name:"Z1.json",mimeType:"application/json",
   buffer:Buffer.from(JSON.stringify(edited))};
 await page.locator("#importNarrativeFile").setInputFiles(upload);
 await page.locator("#importDialog").waitFor({state:"visible"});
 assert.match(await page.locator("#importSummary").textContent(),
   /unit-1 · Z1 · 1 changed narrative field/);
 assert.equal(await page.locator("#export").isDisabled(),true);
 await page.locator('#importDialog button:has-text("Cancel")').click();
 assert.equal(await page.locator("#export").isDisabled(),true);
 await page.locator("#importNarrativeFile").setInputFiles(upload);
 await page.locator("#applyImport").click();
 assert.equal((await page.locator('[data-edit-key="0:title"]').textContent()).trim(),
   edited.scenes[0].title);
 assert.equal(await page.locator("#export").isEnabled(),true);
 assert.equal(await page.locator("#undo").isEnabled(),true);
 await page.locator("#undo").click();
 assert.equal((await page.locator('[data-edit-key="0:title"]').textContent()).trim(),
   original.scenes[0].title);
 await page.locator("#redo").click();
 assert.equal((await page.locator('[data-edit-key="0:title"]').textContent()).trim(),
   edited.scenes[0].title);
 // Reject JSON that attempts to mutate any protected scientific field.
 const tampered=structuredClone(edited);
 tampered.scenes[0].object_ids=["intruder-object"];
 await page.locator("#importNarrativeFile").setInputFiles({
   name:"tampered.json",mimeType:"application/json",
   buffer:Buffer.from(JSON.stringify(tampered))
 });
 await page.locator("#errorDialog").waitFor({state:"visible"});
 assert.match(await page.locator("#errorMessage").textContent(),/Import blocked/);
 assert.equal(await page.locator("#importDialog").isVisible(),false);
 await page.locator("#errorDialog button").click();
 assert.equal((await page.locator('[data-edit-key="0:title"]').textContent()).trim(),
   edited.scenes[0].title);
 page.once("dialog",dialog=>dialog.accept());
 await page.locator("#reset").click();

 // Switching a picker must never file the outgoing journey's draft under
 // the newly selected journey's storage key.
 const specificZ1="Unsaved Z1 title remains attached to Z1";
 await page.locator('[data-edit-key="0:title"]').click();
 await page.locator("#editText").fill(specificZ1);
 await page.locator("#journey").selectOption("Z2");
 await page.waitForFunction(()=>document.querySelector("#journey")?.value==="Z2"&&
   document.querySelector('#scenePreview [data-edit-key="0:title"]')?.textContent.trim()!=="Unsaved Z1 title remains attached to Z1");
 const specificZ2="Another separate Z2 draft";
 await page.locator('[data-edit-key="0:title"]').click();
 await page.locator("#editText").fill(specificZ2);
 await page.locator("#journey").selectOption("Z1");
 await page.waitForFunction(expected=>
   document.querySelector('#scenePreview [data-edit-key="0:title"]')?.textContent.trim()===expected,
   specificZ1);
 assert.equal(await page.locator("#editText").isVisible(),false);
 await page.reload();
 await page.locator('[data-edit-key="0:title"]').waitFor();
 assert.equal((await page.locator('[data-edit-key="0:title"]').textContent()).trim(),specificZ1);
 await page.locator("#journey").selectOption("Z2");
 await page.waitForFunction(expected=>
   document.querySelector('#scenePreview [data-edit-key="0:title"]')?.textContent.trim()===expected,
   specificZ2);
 page.once("dialog",dialog=>dialog.accept());
 await page.locator("#reset").click();
 await page.locator("#journey").selectOption("Z1");
 await page.waitForFunction(expected=>
   document.querySelector('#scenePreview [data-edit-key="0:title"]')?.textContent.trim()===expected,
   specificZ1);
 page.once("dialog",dialog=>dialog.accept());
 await page.locator("#reset").click();

 await page.locator("#unit").selectOption("unit-2");
 await page.locator("#journey").waitFor();
 await page.waitForFunction(()=>document.querySelector("#journey")?.value==="U2-J1"&&
   document.querySelectorAll("#sceneList button").length===13);
 const unit2=await (await page.request.get(origin+"/content/ap-biology/unit-2/journeys/U2-J1.json")).json();
 const p=page.locator('[data-edit-key="0:paragraphs:0"]');
 await p.click();
 await page.locator("#editText").fill("A new opening narrative for visual editor testing.");
 const second=await downloadJourney("U2-J1");
 assert.equal(second.scenes[0].story_paragraphs[0],"A new opening narrative for visual editor testing.");
 if(unit2.scenes[0].story_open===unit2.scenes[0].story_paragraphs[0])
   assert.equal(second.scenes[0].story_open,second.scenes[0].story_paragraphs[0]);
 assert.deepEqual(second.scenes[0].object_ids,unit2.scenes[0].object_ids);
 assert.deepEqual(second.scenes[0].checkpoint,unit2.scenes[0].checkpoint);

 await page.locator("#viewport").selectOption("narrow");
 assert.match(await page.locator("#scenePreview").getAttribute("class"),/narrow/);
 // Viewport-size testing must check the actual mobile layout. The viewport
 // selector above simulates the student preview width only.
 await page.setViewportSize({width:390,height:844});
 const mobileLayout=await page.evaluate(()=>{
   const rect=id=>document.getElementById(id).getBoundingClientRect();
   return {
     viewport:window.innerWidth,
     documentWidth:document.documentElement.scrollWidth,
     jumpNavVisible:getComputedStyle(document.querySelector('.editor-jump-nav')).display!=="none",
     sceneTop:rect('storyWorkspace').top,
     inspectorTop:rect('storyInspector').top,
     curriculumTop:rect('storyCurriculum').top,
     previewMinHeight:getComputedStyle(document.getElementById('scenePreview')).minHeight
   };
 });
 assert.equal(mobileLayout.jumpNavVisible,true,
   "Mobile editors need direct navigation links to scenes, curricula and element settings");
 assert(mobileLayout.sceneTop<mobileLayout.inspectorTop,
   "The mobile narrative preview must appear before the inspector");
 assert(mobileLayout.inspectorTop<mobileLayout.curriculumTop,
   "The inspector must appear before the long curriculum picker on phones");
 assert(mobileLayout.documentWidth<=mobileLayout.viewport+1,
   "A 390px browser viewport must not have horizontal page overflow");
 assert.equal(mobileLayout.previewMinHeight,"0px");
 const jumpLinks=await page.locator('.editor-jump-nav a').evaluateAll(links=>
   links.map(a=>a.getAttribute('href')));
 assert.deepEqual(jumpLinks,['#storyWorkspace','#storyCurriculum','#storyInspector']);
 await page.locator('.editor-jump-nav a[href="#storyCurriculum"]').click();
 assert.equal(new URL(page.url()).hash,'#storyCurriculum');
 await page.locator('.editor-jump-nav a[href="#storyWorkspace"]').click();
 assert.equal(new URL(page.url()).hash,'#storyWorkspace');
 await page.screenshot({path:"/tmp/story-editor-artifacts/story-editor-mobile.png",fullPage:true});
 assert.deepEqual(errors,[]);
 console.log("PASS: journey navigation, scene editing, protected science, JSON export, drafts, mobile layout");
}finally{await browser.close()}
