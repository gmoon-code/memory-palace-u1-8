const WORKFLOW_STORAGE_KEY = "story-method-content-studio-workflow-context-v1";
const WORKFLOW_SUPPORTED_PREVIEW_TYPES = new Set(["scene", "journey", "question", "challenge", "memory_object", "concept", "unit"]);
const WORKFLOW_EDIT_VIEW = {
  unit: "units",
  journey: "journeys",
  scene: "scenes",
  character: "characters",
  location: "locations",
  concept: "concepts",
  memory_object: "memory-objects",
  question: "questions",
  question_set: "questions",
  challenge: "challenge",
};
const WORKFLOW_EDITOR_VIEWS = new Set(["units", "journeys", "scenes", "stories", "characters", "locations", "concepts", "memory-objects"]);
const WORKFLOW_MANAGEMENT_VIEWS = new Set(["questions", "challenge"]);
const WORKFLOW_CONTEXT_SELECTORS = [
  ["[data-editor-entity]", "editorEntity"],
  ["[data-managed-id]", "managedId"],
  ["[data-preview-id]", "previewId"],
  ["[data-replacement-id]", "replacementId"],
  ["[data-health-preview]", "healthPreview"],
  ["[data-entity-id]", "entityId"],
  ["[data-related-id]", "relatedId"],
];

const workflowState = {
  context: null,
  busy: false,
  messageTimer: null,
};

function w(id) {
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

function sleep(milliseconds) {
  return new Promise((resolve) => window.setTimeout(resolve, milliseconds));
}

async function waitFor(getter, timeout = 5000, interval = 70) {
  const started = Date.now();
  while (Date.now() - started < timeout) {
    const result = getter();
    if (result) return result;
    await sleep(interval);
  }
  return null;
}

async function workflowApi(url) {
  const response = await fetch(url, {
    credentials: "same-origin",
    cache: "no-store",
    headers: { Accept: "application/json" },
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

function loadStoredContext() {
  try {
    const raw = window.sessionStorage.getItem(WORKFLOW_STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object" || !parsed.entity_id) return null;
    return { ...parsed, course_id: parsed.course_id || "ap-biology" };
  } catch {
    return null;
  }
}

function storeContext(context) {
  try {
    if (context?.entity_id) window.sessionStorage.setItem(WORKFLOW_STORAGE_KEY, JSON.stringify(context));
    else window.sessionStorage.removeItem(WORKFLOW_STORAGE_KEY);
  } catch {
    // Workflow context is a convenience layer. Storage failure must never block editing.
  }
}

function currentView() {
  return document.querySelector(".nav-item.active")?.dataset.view || "";
}

function currentWorkflowCourseId() {
  return document.getElementById("admin-course-select")?.value || "ap-biology";
}

function preferredViewForType(entityType) {
  return WORKFLOW_EDIT_VIEW[entityType] || "course-map";
}

function normalizeContext(record, extras = {}) {
  const entityId = record?.id || record?.entity_id || extras.entity_id || "";
  const entityType = record?.type || record?.entity_type || extras.entity_type || "";
  const unitId = record?.unit_id || extras.unit_id || "";
  const courseId = record?.course_id || extras.course_id || currentWorkflowCourseId();
  const title = record?.title || record?.canonical_term || record?.name || extras.title || entityId;
  const active = extras.preferred_view || currentView();
  const typeDefault = preferredViewForType(entityType);
  const preferred = [
    ...WORKFLOW_EDITOR_VIEWS,
    ...WORKFLOW_MANAGEMENT_VIEWS,
    "replacement",
  ].includes(active)
    ? active
    : typeDefault;
  return {
    course_id: courseId,
    entity_id: entityId,
    entity_type: entityType,
    unit_id: unitId,
    title,
    preferred_view: preferred,
    draft_id: extras.draft_id || null,
    draft_version: extras.draft_version || null,
    source: extras.source || "selection",
    updated_at: new Date().toISOString(),
  };
}

function setContext(next, { quiet = false } = {}) {
  if (!next?.entity_id) return;
  const sameRecord =
    workflowState.context?.entity_id === next.entity_id &&
    workflowState.context?.course_id === next.course_id;
  workflowState.context = {
    ...(sameRecord ? workflowState.context : {}),
    ...next,
    updated_at: new Date().toISOString(),
  };
  storeContext(workflowState.context);
  renderWorkflowBar();
  if (!quiet) {
    window.dispatchEvent(new CustomEvent("contentstudio:workflow-context", { detail: structuredClone(workflowState.context) }));
  }
}

function clearContext() {
  workflowState.context = null;
  storeContext(null);
  renderWorkflowBar();
}

function setWorkflowMessage(text, mode = "") {
  const node = w("workflow-context-message");
  if (!node) return;
  window.clearTimeout(workflowState.messageTimer);
  node.textContent = text || "";
  node.className = `workflow-context-message${mode ? ` ${mode}` : ""}${text ? "" : " hidden"}`;
  if (text && mode !== "error") {
    workflowState.messageTimer = window.setTimeout(() => {
      if (node.textContent === text) {
        node.textContent = "";
        node.className = "workflow-context-message hidden";
      }
    }, 6500);
  }
}

function stageForView(view) {
  if (["dashboard", "course-map"].includes(view)) return "browse";
  if (WORKFLOW_EDITOR_VIEWS.has(view) || WORKFLOW_MANAGEMENT_VIEWS.has(view) || view === "replacement") return "edit";
  if (view === "drafts") return "draft";
  if (view === "preview") return "preview";
  if (view === "health") return "validate";
  if (view === "publishing") return "publish";
  if (view === "versions") return "recover";
  return "";
}

function updateWorkflowStageHighlight() {
  const active = stageForView(currentView());
  document.querySelectorAll("[data-workflow-stage]").forEach((button) => {
    const selected = button.dataset.workflowStage === active;
    button.classList.toggle("active", selected);
    if (selected) button.setAttribute("aria-current", "step");
    else button.removeAttribute("aria-current");
  });
}

function renderWorkflowBar() {
  const bar = w("workflow-context-bar");
  if (!bar) return;
  const context = workflowState.context;
  bar.classList.toggle("hidden", !context);
  if (!context) return;
  w("workflow-context-title").textContent = context.title || context.entity_id;
  w("workflow-context-id").textContent = context.entity_id;
  w("workflow-context-meta").textContent = [
    humanize(context.entity_type || "record"),
    context.unit_id ? context.unit_id.replace("unit-", "Unit ") : "Course-wide",
    context.draft_id ? `Working copy v${context.draft_version || "?"}` : "Published base",
  ].join(" · ");
  const history = w("workflow-version-history");
  if (history) history.disabled = !context.draft_id;
  updateWorkflowStageHighlight();
}

function ensureWorkflowUi() {
  if (!document.querySelector('link[href="/admin/workflow.css"]')) {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "/admin/workflow.css";
    document.head.appendChild(link);
  }

  const status = document.querySelector(".brand-block .status-pill");
  if (status) status.textContent = "Integrated editing workflow";

  if (!w("workflow-context-bar")) {
    const section = document.createElement("section");
    section.id = "workflow-context-bar";
    section.className = "workflow-context-bar hidden";
    section.setAttribute("aria-label", "Current Content Studio workflow context");
    section.innerHTML = `
      <div class="workflow-context-main">
        <div class="workflow-context-copy">
          <span class="workflow-context-label">Current record</span>
          <strong id="workflow-context-title"></strong>
          <span id="workflow-context-meta" class="workflow-context-meta"></span>
          <code id="workflow-context-id" class="workflow-context-id"></code>
        </div>
        <div class="workflow-context-actions">
          <button id="workflow-version-history" class="text-button" type="button">Version history</button>
          <button id="workflow-clear-context" class="text-button" type="button">Clear</button>
        </div>
      </div>
      <div class="workflow-stage-row" role="group" aria-label="Continue with the current record">
        <button class="workflow-stage" data-workflow-stage="browse" type="button"><span>1</span><strong>Browse</strong></button>
        <button class="workflow-stage" data-workflow-stage="edit" type="button"><span>2</span><strong>Edit</strong></button>
        <button class="workflow-stage" data-workflow-stage="draft" type="button"><span>3</span><strong>Draft</strong></button>
        <button class="workflow-stage" data-workflow-stage="preview" type="button"><span>4</span><strong>Preview</strong></button>
        <button class="workflow-stage" data-workflow-stage="validate" type="button"><span>5</span><strong>Validate</strong></button>
        <button class="workflow-stage" data-workflow-stage="publish" type="button"><span>6</span><strong>Publish</strong></button>
        <button class="workflow-stage" data-workflow-stage="recover" type="button"><span>7</span><strong>Recover</strong></button>
      </div>
      <p id="workflow-context-message" class="workflow-context-message hidden" role="status" aria-live="polite"></p>`;
    const statusBanner = w("status-banner");
    if (statusBanner) statusBanner.insertAdjacentElement("afterend", section);
    else document.querySelector("#admin-main")?.prepend(section);
  }

  w("workflow-clear-context")?.addEventListener("click", clearContext);
  w("workflow-version-history")?.addEventListener("click", () => openVersionHistory());
  document.querySelectorAll("[data-workflow-stage]").forEach((button) => {
    button.addEventListener("click", () => runStage(button.dataset.workflowStage));
  });
}

async function refreshDraftContext({ quiet = true } = {}) {
  const context = workflowState.context;
  if (!context?.entity_id || !context.entity_type) return null;
  const params = new URLSearchParams({ course_id: context.course_id || currentWorkflowCourseId(), status: "draft", entity_type: context.entity_type, limit: "500" });
  if (context.unit_id) params.set("unit_id", context.unit_id);
  try {
    const payload = await workflowApi(`/api/admin/drafts?${params.toString()}`);
    const draft = (payload.items || []).find((item) => item.entity_id === context.entity_id) || null;
    if (draft) {
      setContext({
        ...context,
        draft_id: draft.draft_id,
        draft_version: draft.version,
        title: draft.title || context.title,
        source: "draft-link",
      }, { quiet });
    } else if (context.draft_id) {
      setContext({ ...context, draft_id: null, draft_version: null }, { quiet });
    }
    return draft;
  } catch {
    return null;
  }
}

async function resolveEntityContext(entityId, preferredView = "") {
  if (!entityId) return;
  let record = null;
  let draft = null;
  try {
    const payload = await workflowApi(`/api/admin/catalog/entity?entity_id=${encodeURIComponent(entityId)}&course_id=${encodeURIComponent(currentWorkflowCourseId())}`);
    record = payload?.entity || payload;
  } catch {
    try {
      const payload = await workflowApi(`/api/admin/management/entity?entity_id=${encodeURIComponent(entityId)}`);
      record = payload?.entity || payload?.draft?.payload || null;
      draft = payload?.draft || null;
    } catch {
      record = null;
    }
  }
  if (!record) return;
  setContext(normalizeContext(record, {
    entity_id: entityId,
    preferred_view: preferredView || currentView(),
    draft_id: draft?.draft_id || null,
    draft_version: draft?.version || null,
  }));
  if (!draft) await refreshDraftContext();
}

async function resolveDraftContext(draftId) {
  if (!draftId) return;
  try {
    const draft = await workflowApi(`/api/admin/drafts/${encodeURIComponent(draftId)}?course_id=${encodeURIComponent(currentWorkflowCourseId())}`);
    setContext(normalizeContext(draft.payload || {}, {
      course_id: draft.course_id,
      entity_id: draft.entity_id,
      entity_type: draft.entity_type,
      unit_id: draft.unit_id,
      title: draft.title,
      preferred_view: preferredViewForType(draft.entity_type),
      draft_id: draft.draft_id,
      draft_version: draft.version,
      source: "draft",
    }));
  } catch {
    // A missing draft should not break the underlying workspace action.
  }
}

function findDataElement(selector, dataKey, value) {
  return [...document.querySelectorAll(selector)].find((node) => node.dataset?.[dataKey] === value) || null;
}

function clickNav(view) {
  const button = [...document.querySelectorAll(".nav-item")].find((item) => item.dataset.view === view);
  if (!button) return false;
  button.click();
  window.setTimeout(updateWorkflowStageHighlight, 100);
  return true;
}

async function openBrowse() {
  if (!clickNav("dashboard")) return;
  const input = await waitFor(() => w("catalog-search-input"));
  const form = w("catalog-search-form");
  if (!input || !form || !workflowState.context) return;
  input.value = workflowState.context.entity_id;
  form.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));
  setWorkflowMessage("Opened global browse with the current record ID preselected.", "success");
}

async function prepareManagementFilters(view, context) {
  const unitId = view === "questions" ? "question-unit" : "challenge-unit";
  const select = await waitFor(() => w(unitId), 4000);
  if (select && context.unit_id && [...select.options].some((option) => option.value === context.unit_id) && select.value !== context.unit_id) {
    select.value = context.unit_id;
    select.dispatchEvent(new Event("change", { bubbles: true }));
    await sleep(300);
  }
}

async function prepareReplacementFilters(context) {
  const typeButton = await waitFor(() => findDataElement("[data-replacement-type]", "replacementType", context.entity_type), 4000);
  if (typeButton && !typeButton.classList.contains("active")) {
    typeButton.click();
    await sleep(250);
  }
  const unit = w("replacement-unit-filter");
  if (unit && context.unit_id && unit.value !== context.unit_id) {
    unit.value = context.unit_id;
    unit.dispatchEvent(new Event("change", { bubbles: true }));
    await sleep(300);
  }
}

async function openEdit() {
  const context = workflowState.context;
  if (!context) return;
  let view = context.preferred_view || preferredViewForType(context.entity_type);
  if (view === "replacement" && !["scene", "journey"].includes(context.entity_type)) view = preferredViewForType(context.entity_type);
  if (!clickNav(view)) {
    setWorkflowMessage("This record does not currently have a field-specific editing workspace.", "error");
    return;
  }
  if (WORKFLOW_EDITOR_VIEWS.has(view)) {
    const target = await waitFor(() => findDataElement("[data-editor-entity]", "editorEntity", context.entity_id));
    if (target) target.click();
    else setWorkflowMessage("The editor opened, but the current record was not present in this editor filter.", "error");
    return;
  }
  if (WORKFLOW_MANAGEMENT_VIEWS.has(view)) {
    await prepareManagementFilters(view, context);
    const target = await waitFor(() => findDataElement("[data-managed-id]", "managedId", context.entity_id));
    if (target) target.click();
    else setWorkflowMessage("The management workspace opened, but the current record was not found in its active filter.", "error");
    return;
  }
  if (view === "replacement") {
    await prepareReplacementFilters(context);
    const target = await waitFor(() => findDataElement("[data-replacement-id]", "replacementId", context.entity_id));
    if (target) target.click();
    else setWorkflowMessage("Complete Story Replacement opened, but the current target was not found.", "error");
  }
}

async function openDraft({ history = false, snapshots = false } = {}) {
  const context = workflowState.context;
  if (!context) return;
  const draft = await refreshDraftContext();
  clickNav("drafts");
  if (!draft) {
    const input = await waitFor(() => w("draft-entity-id"));
    if (input) {
      input.value = context.entity_id;
      input.focus();
      setWorkflowMessage("No active working copy exists yet. The current record ID is ready in Draft Workspace for deliberate creation.", "attention");
    }
    return;
  }
  const target = await waitFor(() => findDataElement("[data-draft-id]", "draftId", draft.draft_id));
  if (target) target.click();
  await waitFor(() => w("draft-editor") && !w("draft-editor").classList.contains("hidden") ? w("draft-editor") : null);
  if (history) {
    w("draft-revisions")?.scrollIntoView({ behavior: "smooth", block: "start" });
    setWorkflowMessage("Showing revision history for the current working copy.", "success");
  } else if (snapshots) {
    w("draft-snapshots")?.scrollIntoView({ behavior: "smooth", block: "start" });
    setWorkflowMessage("Showing recovery snapshots for the current working copy.", "success");
  }
}

async function preparePreviewFilters(context) {
  const unit = await waitFor(() => w("preview-unit"));
  if (unit && context.unit_id && unit.value !== context.unit_id) {
    unit.value = context.unit_id;
    unit.dispatchEvent(new Event("change", { bubbles: true }));
    await sleep(350);
  }
  const type = w("preview-type");
  if (type && type.value !== context.entity_type && [...type.options].some((option) => option.value === context.entity_type)) {
    type.value = context.entity_type;
    type.dispatchEvent(new Event("change", { bubbles: true }));
    await sleep(350);
  }
}

async function openPreview() {
  const context = workflowState.context;
  if (!context) return;
  if (!WORKFLOW_SUPPORTED_PREVIEW_TYPES.has(context.entity_type)) {
    setWorkflowMessage(`${humanize(context.entity_type)} records do not have a direct student renderer.`, "attention");
    return;
  }
  clickNav("preview");
  await preparePreviewFilters(context);
  const target = await waitFor(() => findDataElement("[data-preview-id]", "previewId", context.entity_id), 6500);
  if (target) target.click();
  else setWorkflowMessage("Student Preview opened, but the current record was not found in the selected unit and type.", "error");
}

async function contextualQualitySummary(context) {
  if (WORKFLOW_SUPPORTED_PREVIEW_TYPES.has(context.entity_type)) {
    try {
      const params = new URLSearchParams({ entity_id: context.entity_id, source: "auto", scene_index: "0" });
      const preview = await workflowApi(`/api/admin/quality/preview?${params.toString()}`);
      return {
        errors: Number(preview.quality?.error_count || 0),
        warnings: Number(preview.quality?.warning_count || 0),
        advisories: Number(preview.quality?.advisory_count || 0),
      };
    } catch {
      // Fall through to the unit health report.
    }
  }
  try {
    const suffix = context.unit_id ? `?unit_id=${encodeURIComponent(context.unit_id)}` : "";
    const report = await workflowApi(`/api/admin/quality/report${suffix}`);
    const findings = (report.findings || []).filter((item) => item.entity_id === context.entity_id);
    return {
      errors: findings.filter((item) => item.severity === "error").length,
      warnings: findings.filter((item) => item.severity === "warning").length,
      advisories: findings.filter((item) => item.severity === "advisory").length,
    };
  } catch {
    return null;
  }
}

async function openValidate() {
  const context = workflowState.context;
  if (!context) return;
  clickNav("health");
  const unit = await waitFor(() => w("health-unit"));
  if (unit && context.unit_id && [...unit.options].some((option) => option.value === context.unit_id) && unit.value !== context.unit_id) {
    unit.value = context.unit_id;
    unit.dispatchEvent(new Event("change", { bubbles: true }));
  }
  const summary = await contextualQualitySummary(context);
  const finding = await waitFor(() => findDataElement("[data-health-preview]", "healthPreview", context.entity_id), 3500);
  finding?.closest(".quality-finding")?.scrollIntoView({ behavior: "smooth", block: "center" });
  if (summary) {
    setWorkflowMessage(`Current record quality check · ${summary.errors} errors · ${summary.warnings} warnings · ${summary.advisories} advisories.`, summary.errors ? "error" : summary.warnings ? "attention" : "success");
  } else {
    setWorkflowMessage("Content Health opened for the current unit. Context-specific findings remain visible in the workflow bar.", "success");
  }
}

async function openPublishing() {
  const context = workflowState.context;
  if (!context) return;
  const draft = await refreshDraftContext();
  clickNav("publishing");
  if (!draft) {
    setWorkflowMessage("Publishing requires a changed active working copy. Open or create the draft first.", "attention");
    return;
  }
  const checkbox = await waitFor(() => [...document.querySelectorAll(".candidate-draft-check")].find((item) => item.value === draft.draft_id), 6500);
  let status = null;
  try {
    status = await workflowApi("/api/admin/publication/status");
  } catch {
    status = null;
  }
  if (checkbox) {
    checkbox.checked = true;
    checkbox.closest(".eligible-row")?.scrollIntoView({ behavior: "smooth", block: "center" });
    setWorkflowMessage(status?.publication_enabled ? "The current working copy is selected for candidate preparation." : "The current working copy is selected. Candidate creation remains disabled by the server publication safety gate.", status?.publication_enabled ? "success" : "attention");
  } else {
    setWorkflowMessage("The current working copy is not eligible for a release candidate yet. Resolve blocking quality findings or make a saved change first.", "attention");
  }
}

async function openRecover() {
  const draft = await refreshDraftContext();
  if (draft) {
    await openDraft({ snapshots: true });
    return;
  }
  clickNav("versions");
  setWorkflowMessage("No active working copy exists for this record. Showing verified release history and rollback controls.", "attention");
}

async function openVersionHistory() {
  if (!workflowState.context) return;
  const draft = await refreshDraftContext();
  if (!draft) {
    setWorkflowMessage("This record has no active working-copy revision history yet.", "attention");
    await openEdit();
    return;
  }
  await openDraft({ history: true });
}

async function runStage(stage) {
  if (!workflowState.context || workflowState.busy) return;
  workflowState.busy = true;
  document.querySelectorAll("[data-workflow-stage]").forEach((button) => { button.disabled = true; });
  try {
    if (stage === "browse") await openBrowse();
    if (stage === "edit") await openEdit();
    if (stage === "draft") await openDraft();
    if (stage === "preview") await openPreview();
    if (stage === "validate") await openValidate();
    if (stage === "publish") await openPublishing();
    if (stage === "recover") await openRecover();
  } catch (error) {
    setWorkflowMessage(error.message || "The workflow action could not be completed.", "error");
  } finally {
    workflowState.busy = false;
    document.querySelectorAll("[data-workflow-stage]").forEach((button) => { button.disabled = false; });
    window.setTimeout(updateWorkflowStageHighlight, 120);
  }
}

function captureSelection(event) {
  const target = event.target instanceof Element ? event.target : null;
  if (!target) return;

  const draftButton = target.closest("[data-draft-id]");
  if (draftButton?.dataset.draftId) {
    resolveDraftContext(draftButton.dataset.draftId);
    return;
  }

  for (const [selector, key] of WORKFLOW_CONTEXT_SELECTORS) {
    const button = target.closest(selector);
    const entityId = button?.dataset?.[key];
    if (entityId) {
      resolveEntityContext(entityId, currentView());
      return;
    }
  }

  if (["editor-start-draft", "managed-open-draft", "replacement-open-draft", "managed-save", "editor-save-now", "replacement-apply"].includes(target.id)) {
    window.setTimeout(() => refreshDraftContext(), 450);
    window.setTimeout(() => refreshDraftContext(), 1200);
  }

  if (target.closest(".nav-item")) window.setTimeout(updateWorkflowStageHighlight, 130);
  if (target.id === "logout-button") clearContext();
}

function restoreWorkflowContext() {
  const stored = loadStoredContext();
  if (!stored) return;
  workflowState.context = stored;
  renderWorkflowBar();
  refreshDraftContext();
}

window.addEventListener("story-method-course-changed", (event) => {
  const nextCourseId = event.detail?.courseId || currentWorkflowCourseId();
  if (workflowState.context && workflowState.context.course_id !== nextCourseId) {
    clearContext();
  }
});

ensureWorkflowUi();
document.addEventListener("click", captureSelection, true);
restoreWorkflowContext();
window.setTimeout(updateWorkflowStageHighlight, 150);
