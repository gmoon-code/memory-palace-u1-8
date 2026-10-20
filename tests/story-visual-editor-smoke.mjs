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
 await page.goto(origin+"/authoring/visual-editor.html",{waitUntil:"domcontentloaded"});
 await page.locator('#scenePreview [data-edit-key="0:title"]').waitFor();
 assert.equal(await page.locator("#unit").inputValue(),"unit-1");
 assert.equal(await page.locator("#journey").inputValue(),"Z1");
 assert.equal(await page.locator("#sceneList button").count(),9);
 const original=await (await page.request.get(origin+"/content/ap-biology/unit-1/journeys/Z1.json")).json();
 assert.equal(await page.locator("#export").isDisabled(),true);
 const emphasized=page.locator('[data-edit-key="0:paragraphs:1"]');
 assert(await emphasized.locator("strong.story-term").count()>0,
   "Narrative Markdown should render as accessible emphasis in reading preview");
 assert(!(await emphasized.textContent()).includes("**observation**"),
   "Reading preview should hide Markdown source markers");
 await emphasized.click();
 assert((await page.locator("#editText").inputValue()).includes("**observation**"),
   "The inspector must keep the exact editable Markdown source");
 const title=page.locator('[data-edit-key="0:title"]');
 await title.click();
 await page.locator("#editText").fill("The Observation That Begins the Investigation");
 assert.equal((await title.textContent()).trim(),"The Observation That Begins the Investigation");
 assert.equal(await page.locator("#export").isEnabled(),true);
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
 await page.screenshot({path:"/tmp/story-editor-artifacts/story-editor-mobile.png",fullPage:true});
 assert.deepEqual(errors,[]);
 console.log("PASS: journey navigation, scene editing, protected science, JSON export, drafts, mobile layout");
}finally{await browser.close()}
