const replacementState = {
  targetType: "scene",
  unitId: "unit-1",
  records: [],
  plan: null,
  draft: null,
  analysis: null,
  csrfToken: "",
};

function currentAdminCourseId() {
  return document.getElementById("admin-course-select")?.value || "ap-biology";
}

function currentAdminCourseEditable() {
  return document.getElementById("admin-course-select")?.selectedOptions?.[0]?.dataset?.editable === "true";
}

function r(id) {
  return document.getElementById(id);
}

function esc(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function humanize(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function splitParagraphs(value) {
  return String(value || "")
    .split(/\n\s*\n/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function joinParagraphs(value) {
  return Array.isArray(value) ? value.join("\n\n") : "";
}

function lines(value) {
  return String(value || "")
    .split(/\r?\n/)
    .map((item) => item.trim())
    .filter(Boolean);
}

async function replacementApi(url, options = {}) {
  const headers = new Headers(options.headers || {});
  headers.set("Accept", "application/json");
  if (options.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  if (options.csrf) {
    if (!replacementState.csrfToken) {
      const session = await replacementApi("/api/admin/session");
      replacementState.csrfToken = session.csrf_token || "";
    }
    headers.set("X-CSRF-Token", replacementState.csrfToken);
  }
  const response = await fetch(url, {
    cache: "no-store",
    credentials: "same-origin",
    ...options,
    headers,
  });
  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }
  if (!response.ok) {
    const error = new Error(payload?.detail || `${url} returned ${response.status}`);
    error.status = response.status;
    throw error;
  }
  return payload;
}

function ensureReplacementUi() {
  if (!document.querySelector('link[href="/admin/replacement.css"]')) {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "/admin/replacement.css";
    document.head.appendChild(link);
  }
  const status = document.querySelector(".brand-block .status-pill");
  if (status) status.textContent = "Step 6 complete replacement";

  if (!r("replacement-view")) {
    const section = document.createElement("section");
    section.id = "replacement-view";
    section.className = "view-panel hidden";
    section.setAttribute("aria-live", "polite");
    section.innerHTML = `
      <div class="replacement-workspace">
        <aside class="panel replacement-browser">
          <div class="panel-heading">
            <div><p class="eyebrow">Replacement target</p><h2>Choose a story</h2></div>
            <span id="replacement-record-count" class="read-only-badge"></span>
          </div>
          <div class="replacement-browser-controls">
            <div class="replacement-segmented" role="group" aria-label="Replacement target type">
              <button type="button" class="active" data-replacement-type="scene">Scene</button>
              <button type="button" data-replacement-type="journey">Journey</button>
            </div>
            <select id="replacement-unit-filter" aria-label="Unit">
              <option value="unit-1">Unit 1</option><option value="unit-2">Unit 2</option>
              <option value="unit-3">Unit 3</option><option value="unit-4">Unit 4</option>
              <option value="unit-5">Unit 5</option><option value="unit-6">Unit 6</option>
              <option value="unit-7">Unit 7</option><option value="unit-8">Unit 8</option>
            </select>
            <input id="replacement-filter" type="search" placeholder="Filter titles or IDs…" maxlength="160"/>
          </div>
          <div id="replacement-target-list" class="replacement-target-list"></div>
        </aside>

        <main class="panel replacement-main">
          <div id="replacement-empty" class="replacement-empty">
            <p class="eyebrow">Complete Story Replacement</p>
            <h2>Select a scene or journey</h2>
            <p>The workflow inventories required knowledge and downstream dependencies before a replacement draft can be applied. Stable IDs and the permanent route remain locked.</p>
          </div>
          <div id="replacement-active" class="replacement-hidden">
            <header class="replacement-header">
              <div>
                <p id="replacement-type-label" class="eyebrow">Story target</p>
                <h2 id="replacement-title">Replacement</h2>
                <p id="replacement-meta" class="replacement-muted"></p>
              </div>
              <div class="replacement-header-actions">
                <span id="replacement-draft-state" class="read-only-badge">Published base</span>
                <button id="replacement-open-draft" class="button primary" type="button">Open replacement draft</button>
              </div>
            </header>

            <div class="replacement-step-grid">
              <section class="replacement-card">
                <p class="eyebrow">1 · Knowledge lock</p>
                <h3>Required knowledge before replacement</h3>
                <p class="replacement-muted">These scientific records and Memory Objects are derived from the published story references and dependency graph. The replacement cannot remove required knowledge references.</p>
                <div id="replacement-knowledge" class="knowledge-grid"></div>
              </section>

              <section class="replacement-card">
                <p class="eyebrow">2 · Dependency review</p>
                <h3>Connected content</h3>
                <p class="replacement-muted">Questions, review records, Challenge Lab items, later scenes, concepts, and Memory Objects connected to this target remain visible during the replacement decision.</p>
                <div id="replacement-dependencies" class="dependency-counts"></div>
              </section>

              <section class="replacement-card">
                <p class="eyebrow">3 · Replacement policy</p>
                <div class="replacement-mode-row">
                  <div class="replacement-field">
                    <label for="replacement-mode">Replacement mode</label>
                    <select id="replacement-mode"></select>
                  </div>
                  <p id="replacement-mode-help" class="replacement-muted"></p>
                </div>
                <h4>Preserve from the current draft</h4>
                <div id="replacement-policies" class="replacement-policy-grid"></div>
                <p class="replacement-muted">Stable IDs, the permanent scene route, external questions, and review records are always preserved in Step 6.</p>
              </section>

              <section id="replacement-editor-card" class="replacement-card replacement-hidden">
                <p class="eyebrow">4 · Replacement draft</p>
                <h3>Write the replacement</h3>
                <p class="replacement-muted">Changes below stay inside the protected working copy. The published student site remains unchanged.</p>
                <form id="replacement-form" class="replacement-form"></form>
                <div class="replacement-toolbar">
                  <button id="replacement-analyze" class="button primary" type="button">Analyze replacement</button>
                  <span id="replacement-form-message" class="replacement-muted"></span>
                </div>
              </section>

              <section id="replacement-analysis-card" class="replacement-card replacement-analysis replacement-hidden">
                <p class="eyebrow">5 · Pre-acceptance validation</p>
                <h3>Old versus new</h3>
                <div id="replacement-result-banner" class="replacement-result-banner"></div>
                <div class="replacement-findings">
                  <div><strong>Blocking findings</strong><ul id="replacement-blockers"></ul></div>
                  <div><strong>Warnings to review</strong><ul id="replacement-warnings"></ul></div>
                </div>
                <div class="replacement-comparison">
                  <article><h4>Published story</h4><pre id="replacement-old-story"></pre></article>
                  <article><h4>Replacement candidate</h4><pre id="replacement-new-story"></pre></article>
                </div>
                <h4>Required knowledge check</h4>
                <div id="replacement-knowledge-status" class="replacement-knowledge-table"></div>
                <div class="replacement-apply-bar">
                  <span id="replacement-apply-note" class="replacement-muted">Analyze the current replacement before applying it.</span>
                  <button id="replacement-apply" class="button primary" type="button" disabled>Apply to draft</button>
                </div>
                <div id="replacement-applied" class="replacement-applied replacement-hidden"></div>
              </section>
            </div>
          </div>
        </main>
      </div>`;
    const placeholder = r("placeholder-view");
    if (placeholder) placeholder.insertAdjacentElement("beforebegin", section);
    else document.querySelector("#admin-main")?.appendChild(section);
  }

  bindReplacementUi();
}

function bindReplacementUi() {
  document.querySelectorAll("[data-replacement-type]").forEach((button) => {
    button.addEventListener("click", () => {
      replacementState.targetType = button.dataset.replacementType;
      replacementState.plan = null;
      replacementState.draft = null;
      document.querySelectorAll("[data-replacement-type]").forEach((item) => item.classList.toggle("active", item === button));
      loadReplacementTargets();
      resetReplacementDetail();
    });
  });
  r("replacement-unit-filter")?.addEventListener("change", () => {
    replacementState.unitId = r("replacement-unit-filter").value;
    loadReplacementTargets();
    resetReplacementDetail();
  });
  r("replacement-filter")?.addEventListener("input", renderReplacementTargets);
  r("replacement-open-draft")?.addEventListener("click", openReplacementDraft);
  r("replacement-mode")?.addEventListener("change", () => {
    renderModeHelp();
    markAnalysisStale();
  });
  r("replacement-policies")?.addEventListener("change", markAnalysisStale);
  r("replacement-analyze")?.addEventListener("click", analyzeReplacement);
  r("replacement-apply")?.addEventListener("click", applyReplacement);
  r("replacement-form")?.addEventListener("input", markAnalysisStale);

  document.querySelectorAll(".nav-item").forEach((button) => {
    if (button.dataset.replacementBound === "true") return;
    button.dataset.replacementBound = "true";
    button.addEventListener(
      "click",
      (event) => {
        if (button.dataset.view === "replacement") {
          event.preventDefault();
          event.stopImmediatePropagation();
          activateReplacement();
        } else {
          r("replacement-view")?.classList.add("hidden");
        }
      },
      true
    );
  });
}

function activateReplacement() {
  document.querySelectorAll(".view-panel").forEach((panel) => panel.classList.add("hidden"));
  r("replacement-view")?.classList.remove("hidden");
  document.querySelectorAll(".nav-item").forEach((button) => button.classList.toggle("active", button.dataset.view === "replacement"));
  r("view-eyebrow").textContent = "Major revision workflow";
  r("view-title").textContent = "Complete Story Replacement";
  r("view-description").textContent = "Replace an entire scene narrative or a complete journey through a required-knowledge checklist, dependency review, automatic recovery snapshot, and old-versus-new validation.";
  loadReplacementTargets();
}

function resetReplacementDetail() {
  r("replacement-empty")?.classList.remove("replacement-hidden");
  r("replacement-active")?.classList.add("replacement-hidden");
  r("replacement-analysis-card")?.classList.add("replacement-hidden");
}

async function loadReplacementTargets() {
  const target = r("replacement-target-list");
  if (!target) return;
  target.innerHTML = '<p class="empty-state">Loading replacement targets…</p>';
  const params = new URLSearchParams({ course_id: currentAdminCourseId(), entity_type: replacementState.targetType, unit_id: replacementState.unitId, limit: "500" });
  try {
    const payload = await replacementApi(`/api/admin/catalog/entities?${params.toString()}`);
    replacementState.records = Array.isArray(payload.items) ? payload.items : [];
    r("replacement-record-count").textContent = `${payload.total || replacementState.records.length} records`;
    renderReplacementTargets();
  } catch (error) {
    target.innerHTML = `<p class="empty-state">${esc(error.message)}</p>`;
  }
}

function renderReplacementTargets() {
  const target = r("replacement-target-list");
  if (!target) return;
  const query = (r("replacement-filter")?.value || "").trim().toLowerCase();
  const items = replacementState.records.filter((item) => {
    if (!query) return true;
    return `${item.title || ""} ${item.id || ""} ${item.palace_id || ""} ${item.locus || ""}`.toLowerCase().includes(query);
  });
  if (!items.length) {
    target.innerHTML = '<p class="empty-state">No targets match this filter.</p>';
    return;
  }
  target.innerHTML = items.map((item) => `
    <button class="replacement-target ${replacementState.plan?.entity_id === item.id ? "active" : ""}" type="button" data-replacement-id="${esc(item.id)}">
      <strong>${esc(item.title || item.id)}</strong>
      <small>${esc(item.palace_id || item.locus_id || item.id)}</small>
    </button>`).join("");
  target.querySelectorAll("[data-replacement-id]").forEach((button) => {
    button.addEventListener("click", () => selectReplacementTarget(button.dataset.replacementId));
  });
}

async function selectReplacementTarget(entityId) {
  replacementState.draft = null;
  replacementState.analysis = null;
  r("replacement-analysis-card")?.classList.add("replacement-hidden");
  r("replacement-editor-card")?.classList.add("replacement-hidden");
  try {
    const plan = await replacementApi(`/api/admin/replacements/plan?entity_id=${encodeURIComponent(entityId)}&course_id=${encodeURIComponent(currentAdminCourseId())}`);
    replacementState.plan = plan;
    renderReplacementTargets();
    renderReplacementPlan(plan);
  } catch (error) {
    r("replacement-target-list")?.insertAdjacentHTML("afterbegin", `<p class="draft-message error">${esc(error.message)}</p>`);
  }
}

function renderReplacementPlan(plan) {
  r("replacement-empty")?.classList.add("replacement-hidden");
  r("replacement-active")?.classList.remove("replacement-hidden");
  r("replacement-type-label").textContent = `${humanize(plan.entity_type)} replacement`;
  r("replacement-title").textContent = plan.title || plan.entity_id;
  r("replacement-meta").textContent = `${plan.entity_id} · ${plan.unit_id} · ${plan.required_knowledge_count} required knowledge records`;
  const courseEditable = currentAdminCourseEditable();
  r("replacement-draft-state").textContent = courseEditable ? "Published base" : "Read-only catalog";
  r("replacement-open-draft").classList.toggle("replacement-hidden", !courseEditable);
  r("replacement-open-draft").disabled = !courseEditable;

  const knowledge = Array.isArray(plan.required_knowledge) ? plan.required_knowledge : [];
  r("replacement-knowledge").innerHTML = knowledge.length ? knowledge.map((item) => `
    <article class="knowledge-item">
      <span class="knowledge-status ok">Required</span>
      <strong>${esc(item.canonical_term || item.title || item.raw_reference)}</strong>
      <small>${esc(item.type || "record")} · ${esc(item.raw_reference || item.knowledge_id || item.memory_object_id || "dependency graph")}</small>
      ${item.canonical_definition ? `<small>${esc(item.canonical_definition)}</small>` : ""}
    </article>`).join("") : '<p class="empty-state">No required knowledge records were resolved for this target.</p>';

  const counts = plan.dependency_impact?.related_counts_by_type || {};
  r("replacement-dependencies").innerHTML = Object.entries(counts).length ? Object.entries(counts).map(([key, value]) => `<span class="dependency-count">${esc(humanize(key))} · ${Number(value) || 0}</span>`).join("") : '<span class="replacement-muted">No linked records reported.</span>';

  r("replacement-mode").innerHTML = (plan.modes || []).map((mode) => `<option value="${esc(mode)}">${esc(humanize(mode))}</option>`).join("");
  renderModeHelp();
  renderPolicies(plan.default_preservation || {});
}

function renderModeHelp() {
  const mode = r("replacement-mode")?.value;
  const copy = {
    narrative_only: "Replace the narrative paragraphs while keeping the scene title, location, cast, knowledge links, and Quick Recall unless you explicitly change preservation settings.",
    narrative_plus_scene_design: "Replace the narrative and selected spatial or cast design fields while stable IDs, required knowledge, and the route remain protected.",
    complete_scene: "Replace the complete editable scene payload while stable identity and required-knowledge coverage remain enforced.",
    complete_journey: "Replace the journey frame and all scene narratives in one workflow while preserving scene count, scene order, stable loci, and required knowledge.",
  };
  r("replacement-mode-help").textContent = copy[mode] || "Choose a replacement mode.";
}

function renderPolicies(defaults) {
  const labels = {
    title: ["Title and naming", "Keep the current story, scene, and palace titles."],
    location: ["Location and layout", "Keep current loci, spatial descriptions, and scene layouts."],
    characters: ["Characters and scene objects", "Keep current cast, visuals, jobs, and continuity objects."],
    memory_objects: ["Memory Object links", "Keep the current object and concept references attached to each scene."],
    quick_recall: ["Quick Recall", "Keep checkpoint prompts and knowledge targets."],
    concept_associations: ["Concept associations", "Keep the required scientific coverage represented by the current story."],
    route: ["Permanent route", "Always locked in Step 6."],
    external_questions: ["Question Bank links", "Always preserved in Step 6."],
    review: ["Review links", "Always preserved in Step 6."],
  };
  r("replacement-policies").innerHTML = Object.entries(labels).map(([key, [title, note]]) => {
    const locked = ["route", "external_questions", "review"].includes(key);
    const checked = defaults[key] !== false;
    return `<label class="replacement-policy ${locked ? "locked" : ""}">
      <input type="checkbox" data-preserve-key="${esc(key)}" ${checked ? "checked" : ""} ${locked ? "disabled" : ""}/>
      <span><strong>${esc(title)}</strong><small>${esc(note)}</small></span>
    </label>`;
  }).join("");
}

function preservationPayload() {
  const result = {};
  r("replacement-policies")?.querySelectorAll("[data-preserve-key]").forEach((input) => {
    result[input.dataset.preserveKey] = input.checked;
  });
  result.route = true;
  result.external_questions = true;
  result.review = true;
  return result;
}

async function openReplacementDraft() {
  if (!replacementState.plan) return;
  const button = r("replacement-open-draft");
  button.disabled = true;
  button.textContent = "Preparing…";
  try {
    const draft = await replacementApi("/api/admin/replacements/drafts", {
      method: "POST",
      csrf: true,
      body: JSON.stringify({ entity_id: replacementState.plan.entity_id, course_id: currentAdminCourseId() }),
    });
    replacementState.draft = draft;
    r("replacement-draft-state").textContent = `Draft v${draft.version}`;
    r("replacement-open-draft").classList.add("replacement-hidden");
    r("replacement-editor-card").classList.remove("replacement-hidden");
    renderReplacementEditor(draft);
  } catch (error) {
    r("replacement-form-message").textContent = error.message;
  } finally {
    button.disabled = false;
    button.textContent = "Open replacement draft";
  }
}

function renderReplacementEditor(draft) {
  const payload = draft.payload || {};
  if (draft.entity_type === "scene") renderSceneReplacement(payload);
  else renderJourneyReplacement(payload);
  markAnalysisStale();
}

function sceneFields(scene, prefix = "replacement") {
  return `
    <div class="replacement-fields">
      <div class="replacement-field"><label>Scene title</label><input data-r-field="title" value="${esc(scene.title || "")}"/></div>
      <div class="replacement-field"><label>Locus</label><input data-r-field="locus" value="${esc(scene.locus || "")}"/></div>
      <div class="replacement-field full"><label>Location description</label><textarea data-r-field="location_description" rows="3">${esc(scene.location_description || "")}</textarea></div>
      <div class="replacement-field full"><label>Spatial orientation</label><textarea data-r-field="orientation" rows="4">${esc(scene.scene_layout?.orientation || "")}</textarea></div>
      <div class="replacement-field full"><label>Continuity object</label><textarea data-r-field="continuity_object" rows="3">${esc(scene.continuity_object || "")}</textarea></div>
      <div class="replacement-field"><label>Next locus</label><input data-r-field="next_locus" value="${esc(scene.next_locus || "")}"/></div>
      <div class="replacement-field"><label>Quick Recall target</label><input data-r-field="checkpoint_object_id" value="${esc(scene.checkpoint_object_id || "")}"/></div>
      <div class="replacement-field full"><label>Memory Object or concept IDs, one per line</label><textarea data-r-field="object_ids" rows="4">${esc((scene.object_ids || []).join("\n"))}</textarea></div>
      <div class="replacement-field full"><label>Quick Recall prompt</label><textarea data-r-field="checkpoint_prompt" rows="3">${esc(scene.checkpoint_prompt || "")}</textarea></div>
      <label class="replacement-policy"><input type="checkbox" data-r-field="checkpoint" ${scene.checkpoint ? "checked" : ""}/><span><strong>Quick Recall enabled</strong><small>Preservation policy can still lock the published setting.</small></span></label>
    </div>
    <details><summary>Characters and scene objects</summary><div class="replacement-cast" data-r-cast>${renderCast(scene.cast || [])}</div></details>
    <div class="replacement-field full"><label for="${prefix}-story">Replacement story paragraphs</label><textarea id="${prefix}-story" class="replacement-story-textarea" data-r-field="story_paragraphs">${esc(joinParagraphs(scene.story_paragraphs || []))}</textarea><small>Separate paragraphs with a blank line.</small></div>`;
}

function renderCast(cast) {
  return (Array.isArray(cast) ? cast : []).map((item, index) => `
    <div class="replacement-cast-row" data-cast-index="${index}">
      <div class="replacement-field"><label>Name</label><input data-cast-field="name" value="${esc(item.name || "")}"/></div>
      <div class="replacement-field"><label>Kind</label><input data-cast-field="kind" value="${esc(item.kind || "")}"/></div>
      <div class="replacement-field full"><label>Visual</label><textarea data-cast-field="visual" rows="2">${esc(item.visual || "")}</textarea></div>
      <div class="replacement-field full"><label>What it does</label><textarea data-cast-field="job" rows="2">${esc(item.job || item.story_job || "")}</textarea></div>
    </div>`).join("") || '<p class="replacement-muted">No cast records are attached to this scene.</p>';
}

function renderSceneReplacement(scene) {
  r("replacement-form").innerHTML = sceneFields(scene, "replacement-scene");
}

function renderJourneyReplacement(journey) {
  const scenes = Array.isArray(journey.scenes) ? journey.scenes : [];
  r("replacement-form").innerHTML = `
    <div class="replacement-fields">
      <div class="replacement-field"><label>Story title</label><input data-j-field="story_title" value="${esc(journey.story_title || journey.title || "")}"/></div>
      <div class="replacement-field"><label>Palace or route name</label><input data-j-field="palace_name" value="${esc(journey.palace_name || "")}"/></div>
      <div class="replacement-field full"><label>Tagline</label><textarea data-j-field="tagline" rows="3">${esc(journey.tagline || "")}</textarea></div>
      <div class="replacement-field full"><label>Premise</label><textarea data-j-field="premise" rows="4">${esc(journey.premise || "")}</textarea></div>
      <div class="replacement-field full"><label>Mission</label><textarea data-j-field="mission" rows="4">${esc(journey.mission || "")}</textarea></div>
      <div class="replacement-field full"><label>Finale</label><textarea data-j-field="finale" rows="4">${esc(journey.finale || "")}</textarea></div>
      <div class="replacement-field full"><label>Route orientation</label><textarea data-j-field="route_orientation" rows="4">${esc(journey.route_orientation || "")}</textarea></div>
    </div>
    <div class="replacement-scene-stack">
      ${scenes.map((scene, index) => `
        <details class="replacement-scene-card" data-journey-scene="${index}" ${index === 0 ? "open" : ""}>
          <summary>Scene ${Number(scene.scene_index) + 1} · ${esc(scene.title || scene.locus || "Untitled")}</summary>
          <div class="replacement-scene-body">
            <div class="replacement-field"><label>Scene title</label><input data-js-field="title" value="${esc(scene.title || "")}"/></div>
            <div class="replacement-field"><label>Location description</label><textarea data-js-field="location_description" rows="3">${esc(scene.location_description || "")}</textarea></div>
            <div class="replacement-field"><label>Spatial orientation</label><textarea data-js-field="orientation" rows="3">${esc(scene.scene_layout?.orientation || "")}</textarea></div>
            <div class="replacement-field"><label>Replacement narrative</label><textarea class="replacement-story-textarea" data-js-field="story_paragraphs">${esc(joinParagraphs(scene.story_paragraphs || []))}</textarea></div>
          </div>
        </details>`).join("")}
    </div>`;
}

function collectSceneReplacement(container, baseScene) {
  const replacement = structuredClone(baseScene || {});
  container.querySelectorAll("[data-r-field]").forEach((field) => {
    const key = field.dataset.rField;
    if (key === "story_paragraphs") replacement[key] = splitParagraphs(field.value);
    else if (key === "object_ids") replacement[key] = lines(field.value);
    else if (key === "checkpoint") replacement[key] = field.checked;
    else if (key === "orientation") {
      replacement.scene_layout = structuredClone(replacement.scene_layout || {});
      replacement.scene_layout.orientation = field.value;
    } else replacement[key] = field.value;
  });
  const cast = [];
  container.querySelectorAll("[data-cast-index]").forEach((row) => {
    const item = {};
    row.querySelectorAll("[data-cast-field]").forEach((field) => item[field.dataset.castField] = field.value);
    cast.push(item);
  });
  if (cast.length) replacement.cast = cast;
  return replacement;
}

function collectReplacementPayload() {
  const draft = replacementState.draft;
  if (!draft) return {};
  if (draft.entity_type === "scene") {
    return collectSceneReplacement(r("replacement-form"), draft.payload || {});
  }
  const replacement = structuredClone(draft.payload || {});
  r("replacement-form").querySelectorAll("[data-j-field]").forEach((field) => replacement[field.dataset.jField] = field.value);
  if (replacement.story_title) replacement.title = replacement.story_title;
  const scenes = Array.isArray(replacement.scenes) ? replacement.scenes.map((item) => structuredClone(item)) : [];
  r("replacement-form").querySelectorAll("[data-journey-scene]").forEach((card) => {
    const index = Number(card.dataset.journeyScene);
    const scene = scenes[index] || {};
    card.querySelectorAll("[data-js-field]").forEach((field) => {
      const key = field.dataset.jsField;
      if (key === "story_paragraphs") scene[key] = splitParagraphs(field.value);
      else if (key === "orientation") {
        scene.scene_layout = structuredClone(scene.scene_layout || {});
        scene.scene_layout.orientation = field.value;
      } else scene[key] = field.value;
    });
    scenes[index] = scene;
  });
  replacement.scenes = scenes;
  return replacement;
}

function requestPayload() {
  return {
    draft_id: replacementState.draft.draft_id,
    expected_version: replacementState.draft.version,
    mode: r("replacement-mode").value,
    replacement: collectReplacementPayload(),
    preservation: preservationPayload(),
  };
}

function markAnalysisStale() {
  replacementState.analysis = null;
  const apply = r("replacement-apply");
  if (apply) apply.disabled = true;
  const note = r("replacement-apply-note");
  if (note) note.textContent = "Analyze the current replacement before applying it.";
  r("replacement-applied")?.classList.add("replacement-hidden");
}

async function analyzeReplacement() {
  if (!replacementState.draft) return;
  const button = r("replacement-analyze");
  button.disabled = true;
  r("replacement-form-message").textContent = "Checking required knowledge and dependencies…";
  try {
    const analysis = await replacementApi("/api/admin/replacements/analyze", {
      method: "POST",
      csrf: true,
      body: JSON.stringify(requestPayload()),
    });
    replacementState.analysis = analysis;
    renderAnalysis(analysis);
    r("replacement-form-message").textContent = analysis.can_apply ? "Analysis complete. No blocking structural findings." : "Analysis complete. Resolve the blocking findings before applying.";
  } catch (error) {
    r("replacement-form-message").textContent = error.message;
  } finally {
    button.disabled = false;
  }
}

function renderAnalysis(analysis) {
  r("replacement-analysis-card").classList.remove("replacement-hidden");
  const banner = r("replacement-result-banner");
  banner.className = `replacement-result-banner ${analysis.can_apply ? "ok" : "blocked"}`;
  banner.textContent = analysis.can_apply ? "Replacement can be applied to the protected draft." : "Replacement is blocked until required knowledge and route checks pass.";
  r("replacement-blockers").innerHTML = (analysis.blockers || []).length ? analysis.blockers.map((item) => `<li>${esc(item)}</li>`).join("") : "<li>None</li>";
  r("replacement-warnings").innerHTML = (analysis.warnings || []).length ? analysis.warnings.map((item) => `<li>${esc(item)}</li>`).join("") : "<li>None</li>";
  r("replacement-old-story").textContent = analysis.published_story_text || "";
  r("replacement-new-story").textContent = analysis.candidate_story_text || "";
  r("replacement-knowledge-status").innerHTML = (analysis.required_knowledge || []).map((item) => `
    <div class="replacement-knowledge-row">
      <strong>${esc(item.canonical_term || item.title || item.raw_reference)}</strong>
      <span class="${item.reference_present ? "good" : "warning"}">${item.reference_present ? "Reference kept" : "Reference missing"}</span>
      <span class="${item.term_explicitly_named ? "good" : "warning"}">${item.term_explicitly_named ? "Term named" : "Term not explicit"}</span>
    </div>`).join("") || '<p class="replacement-muted">No required knowledge rows.</p>';
  r("replacement-apply").disabled = !analysis.can_apply;
  r("replacement-apply-note").textContent = analysis.can_apply ? "Applying creates an automatic snapshot first, then saves the candidate as a new draft revision." : "The apply action stays disabled while blocking findings remain.";
}

async function applyReplacement() {
  if (!replacementState.draft || !replacementState.analysis?.can_apply) return;
  if (!window.confirm("Apply this complete story replacement to the protected draft? A recovery snapshot will be created automatically before the replacement is saved.")) return;
  const button = r("replacement-apply");
  button.disabled = true;
  button.textContent = "Applying…";
  try {
    const result = await replacementApi("/api/admin/replacements/apply", {
      method: "POST",
      csrf: true,
      body: JSON.stringify(requestPayload()),
    });
    replacementState.draft = result.draft;
    replacementState.analysis = null;
    r("replacement-draft-state").textContent = `Draft v${result.draft.version}`;
    r("replacement-applied").classList.remove("replacement-hidden");
    r("replacement-applied").textContent = `Replacement saved to the protected draft. Recovery snapshot “${result.snapshot.label}” was created before the change. Published student content was not modified.`;
    r("replacement-apply-note").textContent = "Replacement applied to the draft. Re-analyze after any further edits.";
    renderReplacementEditor(result.draft);
  } catch (error) {
    r("replacement-applied").classList.remove("replacement-hidden");
    r("replacement-applied").textContent = error.message;
  } finally {
    button.textContent = "Apply to draft";
  }
}

ensureReplacementUi();

window.addEventListener("story-method-course-changed", (event) => {
  replacementState.records = [];
  replacementState.plan = null;
  replacementState.draft = null;
  replacementState.analysis = null;
  const units = Array.isArray(event.detail?.units) ? event.detail.units : [];
  const select = r("replacement-unit-filter");
  if (select && units.length) {
    select.innerHTML = units
      .map((unit) => `<option value="${esc(unit.unit_id)}">Unit ${Number(unit.number) || ""} · ${esc(unit.title || unit.unit_id)}</option>`)
      .join("");
    replacementState.unitId = select.value || units[0].unit_id;
  }
  resetReplacementDetail();
  if (!r("replacement-view")?.classList.contains("hidden")) loadReplacementTargets();
});
