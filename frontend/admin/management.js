const managementState = {
  mode: null,
  unitId: "unit-1",
  questionType: "",
  query: "",
  records: [],
  selectedEntityId: null,
  currentEntity: null,
  currentDraft: null,
  workingPayload: null,
  csrfToken: "",
  saveTimer: null,
  saving: false,
  mediaItems: [],
  selectedMedia: null,
  importBundle: null,
  importPreview: null,
  bulkPreview: null,
};

const managementModes = new Set(["questions", "review", "challenge", "media", "import-export"]);

function m(id) {
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

function number(value) {
  return new Intl.NumberFormat().format(Number(value) || 0);
}

function humanize(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function unitOptions(includeAll = false) {
  const options = [];
  if (includeAll) options.push('<option value="">All units</option>');
  for (let value = 1; value <= 8; value += 1) {
    options.push(`<option value="unit-${value}" ${managementState.unitId === `unit-${value}` ? "selected" : ""}>Unit ${value}</option>`);
  }
  return options.join("");
}

function lines(value) {
  return String(value || "")
    .split(/\r?\n/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function listToLines(value) {
  if (!Array.isArray(value)) return "";
  return value
    .map((item) => {
      if (typeof item === "string") return item;
      if (item && typeof item === "object") return item.text || item.label || item.value || JSON.stringify(item);
      return String(item ?? "");
    })
    .filter(Boolean)
    .join("\n");
}

async function managementApi(url, options = {}) {
  const headers = new Headers(options.headers || {});
  headers.set("Accept", "application/json");
  if (options.body && !headers.has("Content-Type") && !(options.body instanceof Blob) && !(options.body instanceof ArrayBuffer)) {
    headers.set("Content-Type", "application/json");
  }
  if (options.csrf) {
    if (!managementState.csrfToken) {
      const session = await managementApi("/api/admin/session");
      managementState.csrfToken = session.csrf_token || "";
    }
    headers.set("X-CSRF-Token", managementState.csrfToken);
  }
  const response = await fetch(url, {
    credentials: "same-origin",
    cache: "no-store",
    ...options,
    headers,
  });
  const contentType = response.headers.get("content-type") || "";
  let payload = null;
  if (contentType.includes("application/json")) {
    try {
      payload = await response.json();
    } catch {
      payload = null;
    }
  }
  if (!response.ok) {
    const error = new Error(payload?.detail || `${url} returned ${response.status}`);
    error.status = response.status;
    throw error;
  }
  return payload;
}

function setManagementHeader(title, eyebrow, description) {
  m("view-title").textContent = title;
  m("view-eyebrow").textContent = eyebrow;
  m("view-description").textContent = description;
}

function managementMessage(message, error = false) {
  const node = m("management-message");
  if (!node) return;
  node.textContent = message || "";
  node.classList.toggle("error", Boolean(error));
}

function ensureManagementUi() {
  if (!document.querySelector('link[href="/admin/management.css"]')) {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "/admin/management.css";
    document.head.appendChild(link);
  }
  const status = document.querySelector(".brand-block .status-pill");
  if (status) status.textContent = "Step 7 content management";
  if (!m("management-view")) {
    const section = document.createElement("section");
    section.id = "management-view";
    section.className = "view-panel hidden";
    section.setAttribute("aria-live", "polite");
    section.innerHTML = '<div id="management-content"></div><p id="management-message" class="management-message" role="status" aria-live="polite"></p>';
    const placeholder = m("placeholder-view");
    if (placeholder) placeholder.insertAdjacentElement("beforebegin", section);
    else m("admin-main")?.appendChild(section);
  }

  document.querySelectorAll(".nav-item").forEach((button) => {
    if (button.dataset.managementBound === "true") return;
    button.dataset.managementBound = "true";
    button.addEventListener(
      "click",
      (event) => {
        const mode = button.dataset.view;
        if (managementModes.has(mode)) {
          event.preventDefault();
          event.stopImmediatePropagation();
          activateManagement(mode);
        } else {
          m("management-view")?.classList.add("hidden");
        }
      },
      true
    );
  });
}

async function activateManagement(mode) {
  managementState.mode = mode;
  document.querySelectorAll(".view-panel").forEach((panel) => panel.classList.add("hidden"));
  m("management-view")?.classList.remove("hidden");
  document.querySelectorAll(".nav-item").forEach((button) => button.classList.toggle("active", button.dataset.view === mode));
  managementMessage("");
  if (mode === "questions") await renderQuestionBank();
  if (mode === "review") await renderReviewSystem();
  if (mode === "challenge") await renderChallengeLab();
  if (mode === "media") await renderMediaLibrary();
  if (mode === "import-export") await renderImportExport();
}

function recordButton(item) {
  const state = item.source_state === "new_proposal" ? "New proposal" : item.source_state === "draft" ? `Draft v${item.draft?.version || ""}` : "Published";
  const type = item.question_type || item.challenge_type || item.type;
  return `
    <button class="management-record ${managementState.selectedEntityId === item.id ? "active" : ""}" type="button" data-managed-id="${esc(item.id)}">
      <span><strong>${esc(item.title || item.id)}</strong><small>${esc(item.unit_id || "course-wide")} · ${esc(humanize(type || "record"))}</small></span>
      <span class="management-state">${esc(state)}</span>
    </button>`;
}

async function renderQuestionBank() {
  setManagementHeader(
    "Question Bank",
    "Assessment management",
    "Edit current assessment records, create new question proposals, manage mixed-discrimination sets, and keep every change inside recoverable working copies."
  );
  m("management-content").innerHTML = `
    <div class="management-grid">
      <aside class="panel management-browser">
        <div class="panel-heading"><div><p class="eyebrow">Assessment inventory</p><h2>Questions and sets</h2></div><button id="new-question" class="button primary" type="button">New question</button></div>
        <div class="management-toolbar">
          <select id="question-unit" aria-label="Unit">${unitOptions(true)}</select>
          <select id="question-type" aria-label="Question type">
            <option value="">All types</option>
            <option value="quick_recall">Quick Recall</option>
            <option value="review">Delayed review</option>
            <option value="mixed_discrimination">Mixed discrimination</option>
            <option value="teacher_created">Teacher-created proposals</option>
          </select>
          <input id="question-search" type="search" maxlength="160" placeholder="Filter prompt, title, or ID…" value="${esc(managementState.query)}"/>
          <button id="new-question-set" class="button secondary" type="button">New question set</button>
        </div>
        <div id="question-list" class="management-record-list"></div>
      </aside>
      <section class="panel management-editor"><div id="management-editor-body" class="management-empty"><p class="eyebrow">Protected editor</p><h2>Select a question</h2><p>Published assessment files remain locked. Open a working copy to edit an existing record.</p></div></section>
    </div>`;
  m("question-unit").value = managementState.unitId === "" ? "" : managementState.unitId;
  m("question-type").value = managementState.questionType;
  m("question-unit").addEventListener("change", async (event) => {
    managementState.unitId = event.target.value;
    await loadQuestionRecords();
  });
  m("question-type").addEventListener("change", async (event) => {
    managementState.questionType = event.target.value;
    await loadQuestionRecords();
  });
  m("question-search").addEventListener("input", async (event) => {
    managementState.query = event.target.value;
    await loadQuestionRecords();
  });
  m("new-question").addEventListener("click", () => createProposal("question"));
  m("new-question-set").addEventListener("click", () => createProposal("question_set"));
  await loadQuestionRecords();
}

async function loadQuestionRecords() {
  const params = new URLSearchParams({ limit: "1000" });
  if (managementState.unitId) params.set("unit_id", managementState.unitId);
  if (managementState.questionType) params.set("question_type", managementState.questionType);
  if (managementState.query.trim()) params.set("q", managementState.query.trim());
  try {
    const payload = await managementApi(`/api/admin/management/question-bank?${params.toString()}`);
    managementState.records = payload.items || [];
    const target = m("question-list");
    target.innerHTML = managementState.records.length
      ? managementState.records.map(recordButton).join("")
      : '<p class="empty-state">No questions match these filters.</p>';
    target.querySelectorAll("[data-managed-id]").forEach((button) => button.addEventListener("click", () => openManagedEntity(button.dataset.managedId)));
  } catch (error) {
    managementMessage(error.message, true);
  }
}

async function createProposal(entityType) {
  const unitId = managementState.unitId || "unit-1";
  const title = window.prompt(entityType === "question_set" ? "Name the new question set" : "Name the new question", entityType === "question_set" ? "New discrimination set" : "New question");
  if (!title?.trim()) return;
  try {
    const draft = await managementApi("/api/admin/management/proposals", {
      method: "POST",
      csrf: true,
      body: JSON.stringify({ entity_type: entityType, unit_id: unitId, title: title.trim() }),
    });
    managementState.selectedEntityId = draft.entity_id;
    managementState.currentDraft = draft;
    managementState.workingPayload = structuredClone(draft.payload || {});
    await loadQuestionRecords();
    renderQuestionEditor(managementState.workingPayload, draft, true);
  } catch (error) {
    managementMessage(error.message, true);
  }
}

async function openManagedEntity(entityId) {
  clearTimeout(managementState.saveTimer);
  managementState.selectedEntityId = entityId;
  try {
    const payload = await managementApi(`/api/admin/management/entity?entity_id=${encodeURIComponent(entityId)}`);
    managementState.currentEntity = payload.entity;
    managementState.currentDraft = payload.draft || null;
    managementState.workingPayload = structuredClone(payload.draft?.payload || payload.entity || {});
    if (managementState.mode === "questions") renderQuestionEditor(managementState.workingPayload, managementState.currentDraft, Boolean(payload.proposal));
    if (managementState.mode === "challenge") renderChallengeEditor(managementState.workingPayload, managementState.currentDraft, Boolean(payload.proposal));
  } catch (error) {
    managementMessage(error.message, true);
  }
}

function editorActionHeader(payload, draft, proposal) {
  const state = draft ? `Working copy v${draft.version}` : "Published base";
  return `
    <header class="management-editor-header">
      <div><p class="eyebrow">${esc(proposal ? "New proposal" : humanize(payload.type || "record"))}</p><h2>${esc(payload.title || payload.id)}</h2><p class="muted">${esc(payload.id || "")} · ${esc(payload.unit_id || "")}</p></div>
      <div class="management-editor-actions"><span id="managed-save-state" class="management-state">${esc(state)}</span>${draft ? '<button id="managed-snapshot" class="button secondary" type="button">Snapshot</button><button id="managed-save" class="button primary" type="button">Save now</button>' : '<button id="managed-open-draft" class="button primary" type="button">Open working copy</button>'}</div>
    </header>`;
}

function renderQuestionEditor(payload, draft, proposal = false) {
  const target = m("management-editor-body");
  if (!target) return;
  const questionSet = payload.type === "question_set";
  if (questionSet) {
    target.innerHTML = `${editorActionHeader(payload, draft, proposal)}
      <form id="managed-form" class="managed-form">
        <label>Title<input data-managed-field="title" type="text" maxlength="500" value="${esc(payload.title || "")}" ${draft ? "" : "disabled"}/></label>
        <label>Purpose<textarea data-managed-field="purpose" rows="5" ${draft ? "" : "disabled"}>${esc(payload.purpose || "")}</textarea></label>
        <label>Knowledge IDs<textarea data-managed-list="knowledge_ids" rows="5" ${draft ? "" : "disabled"}>${esc(listToLines(payload.knowledge_ids))}</textarea><small>One ID per line.</small></label>
        <label>Terms students must discriminate<textarea data-managed-list="terms" rows="5" ${draft ? "" : "disabled"}>${esc(listToLines(payload.terms))}</textarea></label>
        <label>Initial delay in hours<input data-managed-number="initial_delay_hours" type="number" min="0" max="8760" value="${esc(payload.initial_delay_hours ?? "")}" ${draft ? "" : "disabled"}/></label>
        <section class="management-info-box"><strong>${number(Array.isArray(payload.questions) ? payload.questions.length : 0)} source questions in this set</strong><p>Individual question records remain editable from the Question Bank. This set editor controls grouping, timing, and discrimination targets.</p></section>
      </form>`;
  } else {
    target.innerHTML = `${editorActionHeader(payload, draft, proposal)}
      <form id="managed-form" class="managed-form">
        <div class="managed-two-col">
          <label>Title<input data-managed-field="title" type="text" maxlength="500" value="${esc(payload.title || "")}" ${draft ? "" : "disabled"}/></label>
          <label>Question type<input data-managed-field="question_type" type="text" maxlength="120" value="${esc(payload.question_type || "")}" ${draft && proposal ? "" : "disabled"}/></label>
        </div>
        <label>Prompt<textarea data-managed-field="prompt" rows="7" ${draft ? "" : "disabled"}>${esc(payload.prompt || "")}</textarea></label>
        <label>Choices<textarea data-managed-list="choices" rows="6" ${draft ? "" : "disabled"}>${esc(listToLines(payload.choices))}</textarea><small>One choice per line. Structured choice metadata already present in the source payload is preserved until this field is edited.</small></label>
        <label>Answer<textarea data-managed-field="answer" rows="4" ${draft ? "" : "disabled"}>${esc(payload.answer || payload.target_answer || "")}</textarea></label>
        <label>Explanation or canonical science<textarea data-managed-field="explanation" rows="6" ${draft ? "" : "disabled"}>${esc(payload.explanation || payload.canonical_science || "")}</textarea></label>
        <label>Knowledge IDs<textarea data-managed-list="knowledge_ids" rows="5" ${draft ? "" : "disabled"}>${esc(listToLines(payload.knowledge_ids))}</textarea><small>One Memory Object or canonical knowledge ID per line.</small></label>
        <div class="managed-two-col">
          <label>Initial review window in hours<input data-managed-number="initial_review_window_hours" type="number" min="0" max="8760" value="${esc(payload.initial_review_window_hours ?? "")}" ${draft ? "" : "disabled"}/></label>
          <label>AP skill<input data-managed-field="ap_skill" type="text" maxlength="300" value="${esc(payload.ap_skill || "")}" ${draft ? "" : "disabled"}/></label>
          <label>Difficulty<input data-managed-field="difficulty" type="text" maxlength="120" value="${esc(payload.difficulty || "")}" ${draft ? "" : "disabled"}/></label>
          <label>Distractor notes<textarea data-managed-field="distractor_notes" rows="3" ${draft ? "" : "disabled"}>${esc(payload.distractor_notes || "")}</textarea></label>
        </div>
      </form>`;
  }
  bindManagedEditor(draft);
}

function bindManagedEditor(draft) {
  m("managed-open-draft")?.addEventListener("click", openWorkingCopyForManaged);
  m("managed-save")?.addEventListener("click", () => saveManagedDraft(false));
  m("managed-snapshot")?.addEventListener("click", snapshotManagedDraft);
  if (!draft) return;
  m("managed-form")?.querySelectorAll("input, textarea, select").forEach((field) => {
    field.addEventListener("input", () => {
      collectManagedPayload();
      scheduleManagedAutosave();
    });
  });
}

function collectManagedPayload() {
  const payload = structuredClone(managementState.workingPayload || {});
  m("managed-form")?.querySelectorAll("[data-managed-field]").forEach((field) => {
    payload[field.dataset.managedField] = field.value;
  });
  m("managed-form")?.querySelectorAll("[data-managed-list]").forEach((field) => {
    payload[field.dataset.managedList] = lines(field.value);
  });
  m("managed-form")?.querySelectorAll("[data-managed-number]").forEach((field) => {
    payload[field.dataset.managedNumber] = field.value === "" ? null : Number(field.value);
  });
  managementState.workingPayload = payload;
  return payload;
}

function scheduleManagedAutosave() {
  if (!managementState.currentDraft) return;
  clearTimeout(managementState.saveTimer);
  const state = m("managed-save-state");
  if (state) state.textContent = "Unsaved change";
  managementState.saveTimer = setTimeout(() => saveManagedDraft(true), 1000);
}

async function openWorkingCopyForManaged() {
  if (!managementState.selectedEntityId) return;
  try {
    const draft = await managementApi("/api/admin/management/drafts", {
      method: "POST",
      csrf: true,
      body: JSON.stringify({ entity_id: managementState.selectedEntityId }),
    });
    managementState.currentDraft = draft;
    managementState.workingPayload = structuredClone(draft.payload || {});
    if (managementState.mode === "questions") renderQuestionEditor(managementState.workingPayload, draft, false);
    if (managementState.mode === "challenge") renderChallengeEditor(managementState.workingPayload, draft, false);
  } catch (error) {
    managementMessage(error.message, true);
  }
}

async function saveManagedDraft(autosave) {
  if (!managementState.currentDraft || managementState.saving) return null;
  clearTimeout(managementState.saveTimer);
  managementState.saving = true;
  const state = m("managed-save-state");
  if (state) state.textContent = autosave ? "Autosaving…" : "Saving…";
  try {
    const payload = collectManagedPayload();
    const saved = await managementApi(`/api/admin/management/drafts/${encodeURIComponent(managementState.currentDraft.draft_id)}`, {
      method: "PATCH",
      csrf: true,
      body: JSON.stringify({ payload, expected_version: managementState.currentDraft.version, note: autosave ? "Step 7 editor autosave" : "Step 7 editor save", autosave }),
    });
    managementState.currentDraft = saved;
    managementState.workingPayload = structuredClone(saved.payload || payload);
    if (state) state.textContent = saved.unchanged ? "No changes" : `Saved v${saved.version}`;
    const warnings = saved.management_validation?.warnings || [];
    managementMessage(warnings.length ? warnings.join(" · ") : "Saved to the protected working copy.", false);
    return saved;
  } catch (error) {
    if (state) state.textContent = error.status === 409 ? "Newer version exists" : "Save failed";
    managementMessage(error.message, true);
    return null;
  } finally {
    managementState.saving = false;
  }
}

async function snapshotManagedDraft() {
  if (!managementState.currentDraft) return;
  const saved = await saveManagedDraft(false);
  if (!saved) return;
  const label = window.prompt("Name this recovery snapshot", `Before assessment edit · v${saved.version}`);
  if (!label?.trim()) return;
  try {
    await managementApi(`/api/admin/drafts/${encodeURIComponent(saved.draft_id)}/snapshots`, {
      method: "POST",
      csrf: true,
      body: JSON.stringify({ label: label.trim() }),
    });
    managementMessage(`Snapshot “${label.trim()}” created.`);
  } catch (error) {
    managementMessage(error.message, true);
  }
}

async function renderReviewSystem() {
  setManagementHeader(
    "Review System",
    "Retrieval planning",
    "See immediate Quick Recall, delayed review, mixed discrimination, and application events together, with knowledge targets that currently lack a later retrieval event."
  );
  m("management-content").innerHTML = `
    <section class="panel review-controls"><div><p class="eyebrow">Retrieval timeline</p><h2>Review coverage by unit</h2></div><div class="management-toolbar horizontal"><select id="review-unit">${unitOptions(false)}</select><button id="refresh-review" class="button secondary" type="button">Refresh</button></div></section>
    <div id="review-phase-grid" class="review-phase-grid"></div>
    <div class="management-grid review-grid"><section class="panel"><div class="panel-heading"><div><p class="eyebrow">Scheduled retrieval</p><h2>Timeline</h2></div></div><div id="review-timeline" class="review-timeline"></div></section><section class="panel"><div class="panel-heading"><div><p class="eyebrow">Coverage check</p><h2>Knowledge without later retrieval</h2></div></div><div id="review-gaps" class="review-gaps"></div></section></div>`;
  m("review-unit").value = managementState.unitId || "unit-1";
  m("review-unit").addEventListener("change", async (event) => {
    managementState.unitId = event.target.value;
    await loadReviewTimeline();
  });
  m("refresh-review").addEventListener("click", loadReviewTimeline);
  await loadReviewTimeline();
}

async function loadReviewTimeline() {
  try {
    const data = await managementApi(`/api/admin/management/review-timeline?unit_id=${encodeURIComponent(managementState.unitId || "unit-1")}`);
    const phases = [
      ["Immediate", data.phase_counts?.immediate, "Quick Recall"],
      ["Delayed", data.phase_counts?.delayed, "review prompts"],
      ["Discrimination", data.phase_counts?.discrimination, "mixed sets"],
      ["Application", data.phase_counts?.application, "Challenge Lab"],
      ["Coverage gaps", data.coverage_gap_count, "targets to inspect"],
    ];
    m("review-phase-grid").innerHTML = phases.map(([label, value, note]) => `<article><span>${esc(label)}</span><strong>${number(value)}</strong><small>${esc(note)}</small></article>`).join("");
    m("review-timeline").innerHTML = data.events?.length
      ? data.events.map((event) => `<button class="timeline-event" type="button" data-review-entity="${esc(event.entity_id)}"><span class="timeline-phase">${esc(humanize(event.phase))}${event.delay_hours != null ? ` · ${number(event.delay_hours)} h` : ""}</span><strong>${esc(event.title || event.entity_id)}</strong><small>${esc(listToLines(event.knowledge_ids).replaceAll("\n", ", ") || "No explicit knowledge ID")}</small></button>`).join("")
      : '<p class="empty-state">No review events are indexed for this unit.</p>';
    m("review-timeline").querySelectorAll("[data-review-entity]").forEach((button) => button.addEventListener("click", async () => {
      const id = button.dataset.reviewEntity;
      if (id.startsWith("question:") || id.startsWith("question_set:")) {
        managementState.selectedEntityId = id;
        await activateManagement("questions");
        await openManagedEntity(id);
      } else if (id.startsWith("challenge:")) {
        managementState.selectedEntityId = id;
        await activateManagement("challenge");
        await openManagedEntity(id);
      }
    }));
    m("review-gaps").innerHTML = data.coverage_gaps?.length
      ? data.coverage_gaps.slice(0, 200).map((gap) => `<div class="review-gap"><strong>${esc(gap.knowledge_id)}</strong><small>${esc((gap.scene_titles || []).filter(Boolean).join(" · "))}</small></div>`).join("")
      : '<p class="empty-state compact">Every explicitly taught object ID has a later indexed retrieval or application event.</p>';
  } catch (error) {
    managementMessage(error.message, true);
  }
}

async function renderChallengeLab() {
  setManagementHeader(
    "Challenge Lab",
    "Application management",
    "Edit Challenge Lab prompts and answer guides, inspect prerequisite scene links, and create new draft-only application challenges."
  );
  m("management-content").innerHTML = `
    <div class="management-grid">
      <aside class="panel management-browser"><div class="panel-heading"><div><p class="eyebrow">Application inventory</p><h2>Challenge Lab</h2></div><button id="new-challenge" class="button primary" type="button">New challenge</button></div><div class="management-toolbar"><select id="challenge-unit">${unitOptions(true)}</select><input id="challenge-search" type="search" maxlength="160" placeholder="Filter title, prompt, or domain…"/></div><div id="challenge-list" class="management-record-list"></div></aside>
      <section class="panel management-editor"><div id="management-editor-body" class="management-empty"><p class="eyebrow">Protected editor</p><h2>Select a challenge</h2><p>Changes remain draft-only until the later validation and publication stages.</p></div></section>
    </div>`;
  m("challenge-unit").value = managementState.unitId;
  m("challenge-unit").addEventListener("change", async (event) => {
    managementState.unitId = event.target.value;
    await loadChallengeRecords();
  });
  m("challenge-search").addEventListener("input", async (event) => {
    managementState.query = event.target.value;
    await loadChallengeRecords();
  });
  m("new-challenge").addEventListener("click", () => createChallengeProposal());
  await loadChallengeRecords();
}

async function loadChallengeRecords() {
  const params = new URLSearchParams({ limit: "1000" });
  if (managementState.unitId) params.set("unit_id", managementState.unitId);
  if (managementState.query.trim()) params.set("q", managementState.query.trim());
  try {
    const data = await managementApi(`/api/admin/management/challenge-bank?${params.toString()}`);
    managementState.records = data.items || [];
    m("challenge-list").innerHTML = managementState.records.length ? managementState.records.map(recordButton).join("") : '<p class="empty-state">No Challenge Lab items match.</p>';
    m("challenge-list").querySelectorAll("[data-managed-id]").forEach((button) => button.addEventListener("click", () => openManagedEntity(button.dataset.managedId)));
  } catch (error) {
    managementMessage(error.message, true);
  }
}

async function createChallengeProposal() {
  const unitId = managementState.unitId || "unit-1";
  const title = window.prompt("Name the new Challenge Lab item", "New application challenge");
  if (!title?.trim()) return;
  try {
    const draft = await managementApi("/api/admin/management/proposals", {
      method: "POST",
      csrf: true,
      body: JSON.stringify({ entity_type: "challenge", unit_id: unitId, title: title.trim() }),
    });
    managementState.selectedEntityId = draft.entity_id;
    managementState.currentDraft = draft;
    managementState.workingPayload = structuredClone(draft.payload || {});
    await loadChallengeRecords();
    renderChallengeEditor(managementState.workingPayload, draft, true);
  } catch (error) {
    managementMessage(error.message, true);
  }
}

function renderChallengeEditor(payload, draft, proposal = false) {
  const target = m("management-editor-body");
  if (!target) return;
  target.innerHTML = `${editorActionHeader(payload, draft, proposal)}
    <form id="managed-form" class="managed-form">
      <div class="managed-two-col"><label>Title<input data-managed-field="title" type="text" maxlength="500" value="${esc(payload.title || "")}" ${draft ? "" : "disabled"}/></label><label>Domain<input data-managed-field="domain" type="text" maxlength="300" value="${esc(payload.domain || "")}" ${draft ? "" : "disabled"}/></label><label>Challenge type<input data-managed-field="challenge_type" type="text" maxlength="200" value="${esc(payload.challenge_type || payload.type_detail || "")}" ${draft ? "" : "disabled"}/></label><label>Source assessment<input data-managed-field="source_assessment" type="text" maxlength="500" value="${esc(payload.source_assessment || "")}" ${draft ? "" : "disabled"}/></label></div>
      <label>Prompt<textarea data-managed-field="prompt" rows="8" ${draft ? "" : "disabled"}>${esc(payload.prompt || "")}</textarea></label>
      <label>Answer guide<textarea data-managed-field="answer" rows="7" ${draft ? "" : "disabled"}>${esc(payload.answer || payload.answer_guide || "")}</textarea></label>
      <label>Knowledge IDs<textarea data-managed-list="knowledge_ids" rows="5" ${draft ? "" : "disabled"}>${esc(listToLines(payload.knowledge_ids))}</textarea></label>
      <div class="managed-two-col"><label>Prerequisite loci<textarea data-managed-list="prerequisite_loci" rows="6" ${draft ? "" : "disabled"}>${esc(listToLines(payload.prerequisite_loci))}</textarea></label><label>Prerequisite scene titles<textarea data-managed-list="prerequisite_scene_titles" rows="6" ${draft ? "" : "disabled"}>${esc(listToLines(payload.prerequisite_scene_titles))}</textarea></label></div>
    </form>`;
  bindManagedEditor(draft);
}

async function renderMediaLibrary() {
  setManagementHeader(
    "Media Library",
    "Protected asset staging",
    "Inventory existing published media and stage new images, audio, video, or PDFs with accessibility metadata before any later publication step."
  );
  m("management-content").innerHTML = `
    <section class="panel media-upload-panel"><div><p class="eyebrow">Staged assets</p><h2>Add media</h2><p class="muted">Uploads are stored in protected server_data and never appear on the student site automatically.</p></div><form id="media-upload-form" class="media-upload-form"><input id="media-file" type="file" accept="image/png,image/jpeg,image/webp,image/gif,audio/mpeg,audio/wav,audio/ogg,audio/mp4,video/mp4,video/webm,application/pdf" required/><select id="media-unit"><option value="">No unit</option>${unitOptions(false)}</select><input id="media-entity" type="text" maxlength="512" placeholder="Optional associated entity ID"/><input id="media-alt" type="text" maxlength="4000" placeholder="Alt text or accessibility description"/><input id="media-caption" type="text" maxlength="8000" placeholder="Caption or teacher note"/><button class="button primary" type="submit">Stage asset</button></form></section>
    <div class="management-grid media-grid"><section class="panel"><div class="panel-heading"><div><p class="eyebrow">Protected staging</p><h2>Staged assets</h2></div><button id="refresh-media" class="button secondary" type="button">Refresh</button></div><div id="staged-media-list" class="media-list"></div></section><section class="panel"><div id="media-editor" class="management-empty"><p class="eyebrow">Metadata</p><h2>Select a staged asset</h2><p>Edit alt text, captions, transcripts, and content associations without touching the published site.</p></div></section></div>
    <section class="panel published-media-panel"><div class="panel-heading"><div><p class="eyebrow">Current repository</p><h2>Published media inventory</h2></div></div><div id="existing-media-list" class="published-media-list"></div></section>`;
  m("media-unit").value = "";
  m("media-upload-form").addEventListener("submit", uploadMedia);
  m("refresh-media").addEventListener("click", loadMediaLibrary);
  await loadMediaLibrary();
}

async function uploadMedia(event) {
  event.preventDefault();
  const file = m("media-file").files?.[0];
  if (!file) return;
  const params = new URLSearchParams({ filename: file.name });
  if (m("media-unit").value) params.set("unit_id", m("media-unit").value);
  if (m("media-entity").value.trim()) params.set("entity_id", m("media-entity").value.trim());
  if (m("media-alt").value.trim()) params.set("alt_text", m("media-alt").value.trim());
  if (m("media-caption").value.trim()) params.set("caption", m("media-caption").value.trim());
  try {
    if (!managementState.csrfToken) {
      const session = await managementApi("/api/admin/session");
      managementState.csrfToken = session.csrf_token || "";
    }
    const response = await fetch(`/api/admin/management/media/upload?${params.toString()}`, {
      method: "POST",
      body: file,
      credentials: "same-origin",
      cache: "no-store",
      headers: { "X-CSRF-Token": managementState.csrfToken, "Content-Type": file.type || "application/octet-stream", Accept: "application/json" },
    });
    const payload = await response.json().catch(() => null);
    if (!response.ok) throw new Error(payload?.detail || `Media upload returned ${response.status}`);
    managementMessage(`${file.name} staged safely. It is not published.`);
    m("media-upload-form").reset();
    managementState.selectedMedia = payload;
    await loadMediaLibrary();
    renderMediaEditor(payload);
  } catch (error) {
    managementMessage(error.message, true);
  }
}

async function loadMediaLibrary() {
  try {
    const [staged, existing] = await Promise.all([
      managementApi("/api/admin/management/media/staged?status=staged&limit=500"),
      managementApi("/api/admin/management/media/existing?limit=1000"),
    ]);
    managementState.mediaItems = staged.items || [];
    m("staged-media-list").innerHTML = managementState.mediaItems.length
      ? managementState.mediaItems.map((item) => `<button class="media-row" type="button" data-media-id="${esc(item.asset_id)}"><span><strong>${esc(item.original_filename)}</strong><small>${esc(humanize(item.kind))} · ${number(Math.ceil(item.size_bytes / 1024))} KB · v${number(item.version)}</small></span><span>${esc(item.unit_id || "Unassigned")}</span></button>`).join("")
      : '<p class="empty-state">No staged assets.</p>';
    m("staged-media-list").querySelectorAll("[data-media-id]").forEach((button) => button.addEventListener("click", () => {
      const item = managementState.mediaItems.find((candidate) => candidate.asset_id === button.dataset.mediaId);
      if (item) renderMediaEditor(item);
    }));
    m("existing-media-list").innerHTML = existing.items?.length
      ? existing.items.slice(0, 300).map((item) => `<div class="published-media-row"><span><strong>${esc(item.filename)}</strong><small>${esc(item.path)}</small></span><span>${esc(humanize(item.kind))} · ${number(Math.ceil(item.size_bytes / 1024))} KB</span></div>`).join("")
      : '<p class="empty-state compact">No published media files were discovered.</p>';
  } catch (error) {
    managementMessage(error.message, true);
  }
}

function renderMediaEditor(item) {
  managementState.selectedMedia = item;
  m("media-editor").className = "media-metadata-editor";
  m("media-editor").innerHTML = `
    <div class="panel-heading"><div><p class="eyebrow">Staged ${esc(item.kind)}</p><h2>${esc(item.original_filename)}</h2></div><a class="button secondary" href="/api/admin/management/media/${encodeURIComponent(item.asset_id)}/file" target="_blank" rel="noopener">Preview</a></div>
    <p class="muted">SHA-256 ${esc(item.sha256)} · ${number(item.size_bytes)} bytes</p>
    <label>Alt text or accessibility description<textarea id="media-edit-alt" rows="4">${esc(item.alt_text || "")}</textarea></label>
    <label>Caption<textarea id="media-edit-caption" rows="4">${esc(item.caption || "")}</textarea></label>
    <label>Transcript or narration text<textarea id="media-edit-transcript" rows="8">${esc(item.transcript || "")}</textarea></label>
    <div class="managed-two-col"><label>Unit<select id="media-edit-unit"><option value="">No unit</option>${unitOptions(false)}</select></label><label>Associated entity ID<input id="media-edit-entity" type="text" maxlength="512" value="${esc(item.entity_id || "")}"/></label></div>
    <div class="management-editor-actions"><button id="media-save" class="button primary" type="button">Save metadata</button><button id="media-archive" class="button secondary" type="button">Archive staged asset</button></div>`;
  m("media-edit-unit").value = item.unit_id || "";
  m("media-save").addEventListener("click", saveMediaMetadata);
  m("media-archive").addEventListener("click", archiveMedia);
}

async function saveMediaMetadata() {
  const item = managementState.selectedMedia;
  if (!item) return;
  try {
    const updated = await managementApi(`/api/admin/management/media/${encodeURIComponent(item.asset_id)}`, {
      method: "PATCH",
      csrf: true,
      body: JSON.stringify({ expected_version: item.version, alt_text: m("media-edit-alt").value, caption: m("media-edit-caption").value, transcript: m("media-edit-transcript").value, unit_id: m("media-edit-unit").value || null, entity_id: m("media-edit-entity").value.trim() || null }),
    });
    managementState.selectedMedia = updated;
    managementMessage(`Media metadata saved as v${updated.version}.`);
    await loadMediaLibrary();
    renderMediaEditor(updated);
  } catch (error) {
    managementMessage(error.message, true);
  }
}

async function archiveMedia() {
  const item = managementState.selectedMedia;
  if (!item || !window.confirm("Archive this staged asset? The file and metadata remain recoverable on the server.")) return;
  try {
    await managementApi(`/api/admin/management/media/${encodeURIComponent(item.asset_id)}/archive`, {
      method: "POST",
      csrf: true,
      body: JSON.stringify({ expected_version: item.version }),
    });
    managementState.selectedMedia = null;
    m("media-editor").className = "management-empty";
    m("media-editor").innerHTML = '<p class="eyebrow">Metadata</p><h2>Select a staged asset</h2><p>Archived assets remain recoverable through the API and are never deleted by Step 7.</p>';
    await loadMediaLibrary();
  } catch (error) {
    managementMessage(error.message, true);
  }
}

async function renderImportExport() {
  setManagementHeader(
    "Import and Export",
    "Portability and bulk tools",
    "Move validated working content through portable JSON bundles and preview controlled text replacements before any draft is changed."
  );
  m("management-content").innerHTML = `
    <div class="management-grid import-grid">
      <section class="panel"><div class="panel-heading"><div><p class="eyebrow">Portable JSON</p><h2>Export</h2></div></div><p class="muted">Exports contain curriculum records and working-copy content only. Sessions, passwords, CSRF tokens, and security logs are excluded.</p><label>Unit<select id="export-unit"><option value="">All units</option>${unitOptions(false)}</select></label><label>Entity types<input id="export-types" type="text" value="question,question_set,challenge,scene,journey,concept,memory_object"/></label><button id="export-button" class="button primary" type="button">Download JSON bundle</button></section>
      <section class="panel"><div class="panel-heading"><div><p class="eyebrow">Draft-only import</p><h2>Import</h2></div></div><p class="muted">Imported content becomes a protected working copy or new proposal. It never writes published AP Biology files.</p><input id="import-file" type="file" accept="application/json,.json"/><select id="import-conflict"><option value="skip">Skip active draft conflicts</option><option value="replace_draft">Replace active drafts after snapshot</option></select><div class="management-editor-actions"><button id="import-preview" class="button secondary" type="button">Preview import</button><button id="import-apply" class="button primary" type="button" disabled>Apply to drafts</button></div><div id="import-results" class="import-results"></div></section>
    </div>
    <section class="panel bulk-panel"><div class="panel-heading"><div><p class="eyebrow">Controlled replacement</p><h2>Global draft-safe find and replace</h2></div></div><p class="muted">Only approved human-readable text fields are searched. Stable IDs, source paths, unit IDs, palace IDs, loci IDs, and other identity fields are never rewritten.</p><div class="bulk-controls"><input id="bulk-find" type="text" minlength="2" maxlength="500" placeholder="Find text"/><input id="bulk-replace" type="text" maxlength="5000" placeholder="Replacement text"/><select id="bulk-unit"><option value="">All units</option>${unitOptions(false)}</select><input id="bulk-types" type="text" value="scene,journey,concept,memory_object,question,question_set,challenge"/><label class="checkbox-label"><input id="bulk-case" type="checkbox"/> Case-sensitive</label><button id="bulk-preview" class="button secondary" type="button">Preview</button><button id="bulk-apply" class="button primary" type="button" disabled>Apply selected</button></div><div id="bulk-results" class="bulk-results"></div></section>
    <section class="panel"><div class="panel-heading"><div><p class="eyebrow">Workspace search</p><h2>Search published records, active drafts, proposals, and staged media</h2></div></div><div class="bulk-controls"><input id="workspace-search" type="search" minlength="2" maxlength="160" placeholder="Search all Content Studio work…"/><button id="workspace-search-button" class="button secondary" type="button">Search</button></div><div id="workspace-search-results" class="workspace-search-results"></div></section>`;
  m("export-button").addEventListener("click", exportContentBundle);
  m("import-file").addEventListener("change", loadImportFile);
  m("import-preview").addEventListener("click", previewImport);
  m("import-apply").addEventListener("click", applyImport);
  m("bulk-preview").addEventListener("click", previewBulkReplace);
  m("bulk-apply").addEventListener("click", applyBulkReplace);
  m("workspace-search-button").addEventListener("click", workspaceSearch);
}

async function exportContentBundle() {
  const params = new URLSearchParams({ include_drafts: "true", include_catalog: "true" });
  if (m("export-unit").value) params.set("unit_id", m("export-unit").value);
  const types = m("export-types").value.split(",").map((item) => item.trim()).filter(Boolean);
  if (types.length) params.set("entity_types", types.join(","));
  try {
    const bundle = await managementApi(`/api/admin/management/export?${params.toString()}`);
    const blob = new Blob([JSON.stringify(bundle, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `story-method-content-${m("export-unit").value || "all-units"}.json`;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    URL.revokeObjectURL(url);
    managementMessage(`Exported ${number(bundle.record_count)} records.`);
  } catch (error) {
    managementMessage(error.message, true);
  }
}

async function loadImportFile() {
  const file = m("import-file").files?.[0];
  managementState.importBundle = null;
  managementState.importPreview = null;
  m("import-apply").disabled = true;
  if (!file) return;
  try {
    const text = await file.text();
    const parsed = JSON.parse(text);
    if (!parsed || Array.isArray(parsed) || typeof parsed !== "object") throw new Error("Import file must contain a JSON object.");
    managementState.importBundle = parsed;
    m("import-results").innerHTML = `<p class="muted">Loaded ${esc(file.name)}. Preview it before applying.</p>`;
  } catch (error) {
    managementMessage(error.message, true);
  }
}

async function previewImport() {
  if (!managementState.importBundle) {
    managementMessage("Choose a Content Studio JSON bundle first.", true);
    return;
  }
  try {
    const preview = await managementApi("/api/admin/management/import/preview", { method: "POST", csrf: true, body: JSON.stringify({ bundle: managementState.importBundle }) });
    managementState.importPreview = preview;
    m("import-results").innerHTML = `<div class="import-summary"><strong>${number(preview.record_count)} records</strong><span>${number(preview.ready_count)} ready</span><span>${number(preview.conflict_count)} conflicts</span><span>${number(preview.error_count)} invalid</span></div>${(preview.records || []).slice(0, 100).map((item) => `<div class="import-row ${esc(item.status || "")}"><span><strong>${esc(item.title || item.entity_id || `Record ${item.index + 1}`)}</strong><small>${esc(item.entity_type || "")} · ${esc(item.unit_id || "")}</small></span><span>${esc(item.status || "")}${item.errors?.length ? ` · ${esc(item.errors.join("; "))}` : ""}</span></div>`).join("")}`;
    m("import-apply").disabled = !preview.can_apply;
  } catch (error) {
    managementMessage(error.message, true);
  }
}

async function applyImport() {
  if (!managementState.importBundle || !managementState.importPreview?.can_apply) return;
  if (!window.confirm("Apply this import to protected working copies? Published student content will remain unchanged.")) return;
  try {
    const result = await managementApi("/api/admin/management/import/apply", { method: "POST", csrf: true, body: JSON.stringify({ bundle: managementState.importBundle, conflict_policy: m("import-conflict").value }) });
    managementMessage(`Imported ${number(result.imported_count)} records into drafts. ${number(result.skipped_count)} conflicts skipped.`);
    m("import-apply").disabled = true;
  } catch (error) {
    managementMessage(error.message, true);
  }
}

async function previewBulkReplace() {
  const find = m("bulk-find").value;
  if (find.trim().length < 2) {
    managementMessage("Enter at least two characters to find.", true);
    return;
  }
  const entityTypes = m("bulk-types").value.split(",").map((item) => item.trim()).filter(Boolean);
  try {
    const preview = await managementApi("/api/admin/management/bulk/preview", { method: "POST", csrf: true, body: JSON.stringify({ find, replacement: m("bulk-replace").value, case_sensitive: m("bulk-case").checked, unit_id: m("bulk-unit").value || null, entity_types: entityTypes, limit: 500 }) });
    managementState.bulkPreview = preview;
    m("bulk-results").innerHTML = `<p class="muted">${number(preview.candidate_count)} records · ${number(preview.occurrence_count)} occurrences. Select the records to change.</p>${(preview.candidates || []).map((item, index) => `<label class="bulk-result"><input type="checkbox" data-bulk-index="${index}" checked/><span><strong>${esc(item.title || item.entity_id)}</strong><small>${esc(item.entity_type)} · ${esc(item.unit_id || "")} · ${number(item.occurrence_count)} matches · ${esc(item.source_state)}</small></span><span class="bulk-paths">${esc((item.changes || []).slice(0, 4).map((change) => change.path).join(" · "))}</span></label>`).join("")}`;
    m("bulk-apply").disabled = !preview.candidate_count;
  } catch (error) {
    managementMessage(error.message, true);
  }
}

async function applyBulkReplace() {
  const preview = managementState.bulkPreview;
  if (!preview) return;
  const targets = [];
  m("bulk-results").querySelectorAll("[data-bulk-index]:checked").forEach((box) => {
    const item = preview.candidates[Number(box.dataset.bulkIndex)];
    if (item) targets.push({ entity_id: item.entity_id, expected_version: item.expected_version });
  });
  if (!targets.length) {
    managementMessage("Select at least one record.", true);
    return;
  }
  if (!window.confirm(`Apply this replacement to ${targets.length} protected working copies? A recovery snapshot will be created for each record.`)) return;
  try {
    const result = await managementApi("/api/admin/management/bulk/apply", { method: "POST", csrf: true, body: JSON.stringify({ find: preview.find, replacement: preview.replacement, case_sensitive: preview.case_sensitive, targets }) });
    managementMessage(`Updated ${number(result.updated_count)} working copies across ${number(result.occurrence_count)} text occurrences.`);
    m("bulk-apply").disabled = true;
    await previewBulkReplace();
  } catch (error) {
    managementMessage(error.message, true);
  }
}

async function workspaceSearch() {
  const query = m("workspace-search").value.trim();
  if (query.length < 2) return;
  try {
    const data = await managementApi(`/api/admin/management/search?q=${encodeURIComponent(query)}&limit=150`);
    m("workspace-search-results").innerHTML = data.items?.length
      ? data.items.map((item) => `<div class="workspace-search-row"><span><strong>${esc(item.title || item.entity_id || item.asset_id)}</strong><small>${esc(item.entity_type || "record")} · ${esc(item.unit_id || "course-wide")}</small></span><span>${esc(item.source)}</span></div>`).join("")
      : '<p class="empty-state compact">No matches across catalog, drafts, proposals, or staged media.</p>';
  } catch (error) {
    managementMessage(error.message, true);
  }
}

ensureManagementUi();
