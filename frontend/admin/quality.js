import { learnView } from "/static/js/views/learn.js";
import { reviewView } from "/static/js/views/review.js";
import { practiceView } from "/static/js/views/practice.js";

const qualityState = {
  mode: null,
  units: [],
  unitId: "unit-1",
  entityType: "scene",
  query: "",
  records: [],
  selectedEntityId: null,
  preview: null,
  previewSource: "auto",
  device: "laptop",
  sceneIndex: 0,
  recallOpen: false,
  answerRevealed: false,
  health: null,
  healthSeverity: "",
  healthCategory: "",
};

const qualityModes = new Set(["preview", "health"]);
const STUDENT_STYLES = [
  "/static/css/app.css",
  "/static/css/base.css",
  "/static/css/unit-theme.css",
  "/static/css/home-cleanup.css",
  "/static/css/practice-polish.css",
  "/static/css/learn-polish.css",
];

function q(id) {
  return document.getElementById(id);
}

function currentAdminCourseId() {
  return document.getElementById("admin-course-select")?.value || "ap-biology";
}

function currentAdminCourseCatalogReady() {
  return document.getElementById("admin-course-select")?.selectedOptions?.[0]?.dataset?.catalogReady === "true";
}

function currentAdminCourseEditable() {
  return document.getElementById("admin-course-select")?.selectedOptions?.[0]?.dataset?.editable === "true";
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

function number(value) {
  return new Intl.NumberFormat().format(Number(value) || 0);
}

function jsonSummary(value) {
  const raw = JSON.stringify(value || {}, null, 2);
  return raw.length > 1600 ? `${raw.slice(0, 1600)}\n…` : raw;
}

async function qualityApi(url) {
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

function setHeader(title, eyebrow, description) {
  q("view-title").textContent = title;
  q("view-eyebrow").textContent = eyebrow;
  q("view-description").textContent = description;
}

function ensureQualityUi() {
  if (!document.querySelector('link[href="/admin/quality.css"]')) {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "/admin/quality.css";
    document.head.appendChild(link);
  }
  const status = document.querySelector(".brand-block .status-pill");
  if (status) status.textContent = "Step 8 preview and quality";

  if (!q("quality-view")) {
    const section = document.createElement("section");
    section.id = "quality-view";
    section.className = "view-panel hidden";
    section.setAttribute("aria-live", "polite");
    section.innerHTML = '<div id="quality-content"></div>';
    const placeholder = q("placeholder-view");
    if (placeholder) placeholder.insertAdjacentElement("beforebegin", section);
    else q("admin-main")?.appendChild(section);
  }

  document.querySelectorAll(".nav-item").forEach((button) => {
    if (button.dataset.qualityBound === "true") return;
    button.dataset.qualityBound = "true";
    button.addEventListener(
      "click",
      (event) => {
        const mode = button.dataset.view;
        if (qualityModes.has(mode) && currentAdminCourseCatalogReady()) {
          event.preventDefault();
          event.stopImmediatePropagation();
          activateQuality(mode);
        } else {
          q("quality-view")?.classList.add("hidden");
          document.querySelector(".global-search")?.classList.remove("hidden");
        }
      },
      true
    );
  });
}

async function activateQuality(mode) {
  qualityState.mode = mode;
  document.querySelectorAll(".view-panel").forEach((panel) => panel.classList.add("hidden"));
  q("quality-view")?.classList.remove("hidden");
  document.querySelector(".global-search")?.classList.add("hidden");
  document.querySelectorAll(".nav-item").forEach((button) => button.classList.toggle("active", button.dataset.view === mode));
  if (mode === "preview") await renderPreviewWorkspace();
  if (mode === "health") await renderHealthWorkspace();
}

function unitOptions(includeAll = false) {
  const items = [];
  if (includeAll) items.push('<option value="">All units</option>');
  for (const unit of qualityState.units) {
    const label = unit.number
      ? `Unit ${unit.number} · ${unit.title || unit.unit_id}`
      : unit.title || unit.unit_id;
    items.push(
      `<option value="${esc(unit.unit_id)}" ${qualityState.unitId === unit.unit_id ? "selected" : ""}>${esc(label)}</option>`
    );
  }
  return items.join("");
}

function previewTypeOptions() {
  const options = [
    ["scene", "Scenes"],
    ["journey", "Journeys"],
    ["question", "Questions"],
    ["challenge", "Challenge Lab"],
    ["memory_object", "Memory Objects"],
    ["concept", "Concepts"],
    ["unit", "Units"],
  ];
  return options.map(([value, label]) => `<option value="${value}" ${qualityState.entityType === value ? "selected" : ""}>${label}</option>`).join("");
}

async function renderPreviewWorkspace() {
  setHeader(
    "Student Preview",
    "Draft-aware learner experience",
    "View published or working-copy content through the same student renderers used by The Story Method, then inspect responsive layouts and quality findings before publication."
  );
  q("quality-content").innerHTML = `
    <div class="quality-workspace">
      <aside class="panel quality-browser">
        <div class="panel-heading"><div><p class="eyebrow">Preview target</p><h2>Choose content</h2></div><span id="preview-record-count" class="read-only-badge"></span></div>
        <div class="quality-toolbar">
          <select id="preview-unit" aria-label="Preview unit">${unitOptions(false)}</select>
          <select id="preview-type" aria-label="Preview content type">${previewTypeOptions()}</select>
          <input id="preview-filter" type="search" maxlength="160" placeholder="Filter titles or IDs…" value="${esc(qualityState.query)}"/>
        </div>
        <div id="preview-target-list" class="preview-target-list"><p class="quality-loading">Loading preview targets…</p></div>
      </aside>
      <section class="panel quality-main">
        <div id="preview-empty" class="quality-empty"><p class="eyebrow">Student Preview</p><h2>Select content to inspect</h2><p>Working copies are previewed without changing the published student site.</p></div>
        <div id="preview-detail" class="hidden"></div>
      </section>
    </div>`;

  q("preview-unit").value = qualityState.unitId;
  q("preview-type").value = qualityState.entityType;
  q("preview-unit").addEventListener("change", async (event) => {
    qualityState.unitId = event.target.value;
    qualityState.selectedEntityId = null;
    qualityState.preview = null;
    await loadPreviewTargets();
    resetPreviewDetail();
  });
  q("preview-type").addEventListener("change", async (event) => {
    qualityState.entityType = event.target.value;
    qualityState.selectedEntityId = null;
    qualityState.preview = null;
    await loadPreviewTargets();
    resetPreviewDetail();
  });
  q("preview-filter").addEventListener("input", (event) => {
    qualityState.query = event.target.value;
    renderPreviewTargets();
  });
  await loadPreviewTargets();
  if (qualityState.selectedEntityId && qualityState.records.some((item) => item.id === qualityState.selectedEntityId)) {
    await loadPreview(qualityState.selectedEntityId);
  }
}

function resetPreviewDetail() {
  q("preview-empty")?.classList.remove("hidden");
  q("preview-detail")?.classList.add("hidden");
}

async function loadPreviewTargets() {
  const unit = encodeURIComponent(qualityState.unitId);
  const type = encodeURIComponent(qualityState.entityType);
  try {
    const course = encodeURIComponent(currentAdminCourseId());
    const [catalog, drafts] = await Promise.all([
      qualityApi(`/api/admin/catalog/entities?course_id=${course}&entity_type=${type}&unit_id=${unit}&limit=500`),
      qualityApi(`/api/admin/drafts?course_id=${course}&status=draft&entity_type=${type}&unit_id=${unit}&limit=500`),
    ]);
    const draftMap = new Map((drafts.items || []).map((item) => [item.entity_id, item]));
    const merged = (catalog.items || []).map((item) => ({
      id: item.id,
      title: item.title || item.canonical_term || item.id,
      type: item.type,
      unit_id: item.unit_id,
      palace_id: item.palace_id,
      locus: item.locus,
      draft: draftMap.get(item.id) || null,
      proposal: false,
    }));
    for (const draft of drafts.items || []) {
      if (!String(draft.entity_id || "").startsWith("new:")) continue;
      if (merged.some((item) => item.id === draft.entity_id)) continue;
      merged.push({
        id: draft.entity_id,
        title: draft.title || draft.entity_id,
        type: draft.entity_type,
        unit_id: draft.unit_id,
        draft,
        proposal: true,
      });
    }
    qualityState.records = merged.sort((a, b) => String(a.title).localeCompare(String(b.title)));
    renderPreviewTargets();
  } catch (error) {
    q("preview-target-list").innerHTML = `<p class="empty-state">${esc(error.message)}</p>`;
  }
}

function renderPreviewTargets() {
  const target = q("preview-target-list");
  if (!target) return;
  const needle = qualityState.query.trim().toLowerCase();
  const items = qualityState.records.filter((item) => {
    if (!needle) return true;
    return `${item.title} ${item.id} ${item.locus || ""} ${item.palace_id || ""}`.toLowerCase().includes(needle);
  });
  q("preview-record-count").textContent = `${number(items.length)} shown`;
  if (!items.length) {
    target.innerHTML = '<p class="empty-state">No preview targets match this filter.</p>';
    return;
  }
  target.innerHTML = items
    .map((item) => {
      const state = item.proposal ? "New proposal" : item.draft ? `Draft v${item.draft.version}` : "Published";
      const stateClass = item.draft ? "draft" : "";
      return `
        <button class="preview-target ${qualityState.selectedEntityId === item.id ? "active" : ""}" type="button" data-preview-id="${esc(item.id)}">
          <span><strong>${esc(item.title)}</strong><small>${esc(item.id)}${item.locus ? ` · ${esc(item.locus)}` : ""}</small></span>
          <span class="preview-state-pill ${stateClass}">${esc(state)}</span>
        </button>`;
    })
    .join("");
  target.querySelectorAll("[data-preview-id]").forEach((button) => {
    button.addEventListener("click", () => loadPreview(button.dataset.previewId));
  });
}

async function loadPreview(entityId, options = {}) {
  qualityState.selectedEntityId = entityId;
  if (options.source) qualityState.previewSource = options.source;
  if (Number.isInteger(options.sceneIndex)) qualityState.sceneIndex = options.sceneIndex;
  qualityState.recallOpen = Boolean(options.keepRecall ? qualityState.recallOpen : false);
  qualityState.answerRevealed = Boolean(options.keepAnswer ? qualityState.answerRevealed : false);
  renderPreviewTargets();
  q("preview-empty")?.classList.add("hidden");
  q("preview-detail")?.classList.remove("hidden");
  q("preview-detail").innerHTML = '<p class="quality-loading">Building protected student preview…</p>';
  try {
    const params = new URLSearchParams({
      course_id: currentAdminCourseId(),
      entity_id: entityId,
      source: qualityState.previewSource,
      scene_index: String(qualityState.sceneIndex),
    });
    const preview = await qualityApi(`/api/admin/quality/preview?${params.toString()}`);
    qualityState.preview = preview;
    if (preview.model?.scene_index != null) qualityState.sceneIndex = Number(preview.model.scene_index) || 0;
    renderPreviewDetail();
  } catch (error) {
    q("preview-detail").innerHTML = `<p class="empty-state">${esc(error.message)}</p>`;
  }
}

function previewHtml(preview) {
  const model = preview?.model || {};
  if (model.renderer === "learn" || model.renderer === "learn_recall") {
    const recall = model.renderer === "learn_recall" ? true : qualityState.recallOpen;
    const count = model.journey?.scenes?.length || 1;
    const visited = Array.from({ length: Math.max(0, qualityState.sceneIndex + 1) }, (_, index) => index);
    return learnView(model.journey, Math.min(qualityState.sceneIndex, count - 1), recall, visited);
  }
  if (model.renderer === "practice") {
    return practiceView(model.application_lab, 0, qualityState.answerRevealed);
  }
  if (model.renderer === "review_mixed" || model.renderer === "review_exact") {
    return reviewView(model.review_items || [], 1, model.mixed_sets || []);
  }
  const record = model.record || {};
  if (model.renderer === "knowledge") {
    const definition = record.canonical_definition || record.definition || "";
    const retrieval = record.productive_retrieval_target || record.application_question || "";
    return `<main id="main-content" tabindex="-1" class="review-wrap"><section class="card review-card"><span class="eyebrow">${esc(preview.entity_type === "memory_object" ? "Memory Object" : "Concept")}</span><h1>${esc(record.canonical_term || record.title || preview.title)}</h1><p>${esc(definition)}</p>${retrieval ? `<div class="hint"><span class="eyebrow">Retrieval target</span><p>${esc(retrieval)}</p></div>` : ""}<button class="ghost" type="button">Back to learning</button></section></main>`;
  }
  if (model.renderer === "unit") {
    return `<main id="main-content" tabindex="-1" class="review-wrap"><section class="card review-card"><span class="eyebrow">${esc(preview.course_title || "Course")} unit</span><h1>${esc(record.title || preview.title)}</h1><p>${esc(record.description || record.introduction || "")}</p></section></main>`;
  }
  return `<main id="main-content" tabindex="-1" class="review-wrap"><section class="card review-card"><span class="eyebrow">Student-facing record preview</span><h1>${esc(preview.title)}</h1><p>${esc(record.prompt || record.description || record.canonical_definition || "")}</p></section></main>`;
}

function studentDocument(html) {
  const links = STUDENT_STYLES.map((href) => `<link rel="stylesheet" href="${href}">`).join("");
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'"><title>Content Studio Student Preview</title>${links}</head><body><a class="skip-link" href="#main-content">Skip to main content</a><div id="app"><div class="shell">${html}</div></div></body></html>`;
}

function findingRows(findings, limit = 20) {
  if (!findings?.length) return '<p class="empty-state compact">No findings for this record.</p>';
  return findings.slice(0, limit).map((item) => `
    <article class="quality-finding ${esc(item.severity)}">
      <span class="quality-severity ${esc(item.severity)}">${esc(humanize(item.severity))}</span>
      <div><h3>${esc(humanize(item.code))}</h3><p>${esc(item.message)}</p><small>${esc(item.category)}${item.entity_id ? ` · ${esc(item.entity_id)}` : ""}</small>${Object.keys(item.details || {}).length ? `<details><summary>Details</summary><div class="quality-details">${esc(jsonSummary(item.details))}</div></details>` : ""}</div>
    </article>`).join("");
}

function renderPreviewDetail() {
  const preview = qualityState.preview;
  if (!preview) return;
  const model = preview.model || {};
  const devices = preview.device_presets || {};
  const device = devices[qualityState.device] || devices.laptop || { width: 1024, height: 768, label: "Preview" };
  const quality = preview.quality || {};
  const sourceLabel = preview.source_state === "published" ? "Published baseline" : preview.source_state === "new_proposal" ? "New proposal" : `Working copy${preview.draft_version ? ` v${preview.draft_version}` : ""}`;
  const canPublished = Boolean(preview.published_available);
  const hasScenes = ["learn", "learn_recall"].includes(model.renderer) && Number(model.scene_count || 0) > 0;

  q("preview-detail").innerHTML = `
    <div class="preview-header">
      <div class="preview-header-top">
        <div><p class="eyebrow">${esc(sourceLabel)}</p><h2>${esc(preview.title || preview.entity_id)}</h2><p class="preview-meta">${esc(preview.entity_id)} · ${esc(preview.unit_id || "course-wide")} · ${esc(humanize(preview.entity_type))}</p></div>
        <div class="preview-source-toggle" role="group" aria-label="Preview source">
          <button class="preview-source-button ${qualityState.previewSource !== "published" ? "active" : ""}" data-preview-source="auto" type="button">Working copy</button>
          <button class="preview-source-button ${qualityState.previewSource === "published" ? "active" : ""}" data-preview-source="published" type="button" ${canPublished ? "" : "disabled"}>Published</button>
        </div>
      </div>
      <div class="preview-toolbar">
        <div class="preview-device-toggle" role="group" aria-label="Responsive preview size">
          ${Object.entries(devices).map(([key, value]) => `<button class="preview-device-button ${qualityState.device === key ? "active" : ""}" type="button" data-device="${esc(key)}">${esc(value.label)}</button>`).join("")}
        </div>
        <span class="read-only-badge">${number(device.width)} × ${number(device.height)} reference viewport</span>
      </div>
    </div>
    <div class="preview-stage">
      <div class="preview-frame-shell" style="width:min(100%, ${Number(device.width) || 1024}px)">
        <div class="preview-frame-label"><span>${esc(device.label || qualityState.device)} preview</span><span>Draft data stays inside Content Studio</span></div>
        <iframe id="student-preview-frame" class="student-preview-frame" title="Student experience preview" sandbox=""></iframe>
      </div>
    </div>
    <div class="preview-controls">
      <div class="row">
        ${hasScenes && qualityState.sceneIndex > 0 ? '<button id="preview-previous-scene" class="button secondary" type="button">← Previous scene</button>' : ""}
        ${hasScenes && model.renderer !== "learn_recall" ? `<button id="preview-recall-toggle" class="button secondary" type="button">${qualityState.recallOpen ? "Back to story" : "Preview Quick Recall"}</button>` : ""}
        ${hasScenes && qualityState.sceneIndex < Number(model.scene_count || 1) - 1 ? '<button id="preview-next-scene" class="button primary" type="button">Next scene →</button>' : ""}
        ${model.renderer === "practice" ? `<button id="preview-answer-toggle" class="button secondary" type="button">${qualityState.answerRevealed ? "Hide answer guide" : "Show answer guide"}</button>` : ""}
      </div>
      <span class="muted">The iframe is script-disabled. Use these controls to inspect alternate student states safely.</span>
    </div>
    <div class="preview-quality-grid">
      <article class="preview-quality-card"><span>Errors</span><strong>${number(quality.error_count)}</strong></article>
      <article class="preview-quality-card"><span>Warnings</span><strong>${number(quality.warning_count)}</strong></article>
      <article class="preview-quality-card"><span>Advisories</span><strong>${number(quality.advisory_count)}</strong></article>
      <article class="preview-quality-card"><span>Linked record types</span><strong>${number(Object.keys(quality.dependency_counts || {}).length)}</strong></article>
    </div>
    <div class="quality-findings">${findingRows(quality.findings || [])}</div>`;

  const frame = q("student-preview-frame");
  if (frame) frame.srcdoc = studentDocument(previewHtml(preview));

  q("preview-detail").querySelectorAll("[data-device]").forEach((button) => {
    button.addEventListener("click", () => {
      qualityState.device = button.dataset.device;
      renderPreviewDetail();
    });
  });
  q("preview-detail").querySelectorAll("[data-preview-source]").forEach((button) => {
    button.addEventListener("click", async () => {
      qualityState.previewSource = button.dataset.previewSource;
      qualityState.recallOpen = false;
      qualityState.answerRevealed = false;
      await loadPreview(qualityState.selectedEntityId, { source: qualityState.previewSource });
    });
  });
  q("preview-previous-scene")?.addEventListener("click", async () => {
    qualityState.sceneIndex = Math.max(0, qualityState.sceneIndex - 1);
    qualityState.recallOpen = false;
    await loadPreview(qualityState.selectedEntityId, { sceneIndex: qualityState.sceneIndex });
  });
  q("preview-next-scene")?.addEventListener("click", async () => {
    qualityState.sceneIndex += 1;
    qualityState.recallOpen = false;
    await loadPreview(qualityState.selectedEntityId, { sceneIndex: qualityState.sceneIndex });
  });
  q("preview-recall-toggle")?.addEventListener("click", () => {
    qualityState.recallOpen = !qualityState.recallOpen;
    renderPreviewDetail();
  });
  q("preview-answer-toggle")?.addEventListener("click", () => {
    qualityState.answerRevealed = !qualityState.answerRevealed;
    renderPreviewDetail();
  });
}

async function renderHealthWorkspace() {
  setHeader(
    "Content Health",
    "Pre-publication quality control",
    "Inspect structural errors, teacher-review warnings, and non-blocking quality advisories across scientific coverage, retrieval, narrative continuity, readability, spatial clarity, accessibility, and active drafts."
  );
  q("quality-content").innerHTML = `
    <div class="health-header">
      <div class="health-toolbar">
        <label for="health-unit">Scope</label><select id="health-unit">${unitOptions(true)}</select>
        <label for="health-severity">Severity</label><select id="health-severity"><option value="">All severities</option><option value="error">Errors</option><option value="warning">Warnings</option><option value="advisory">Advisories</option></select>
        <label for="health-category">Category</label><select id="health-category"><option value="">All categories</option></select>
        <button id="health-refresh-step8" class="button secondary" type="button">Refresh checks</button>
      </div>
    </div>
    <div id="health-step8-body"><p class="quality-loading">Running Content Studio quality checks…</p></div>`;
  q("health-unit").value = qualityState.unitId || "";
  q("health-severity").value = qualityState.healthSeverity;
  q("health-unit").addEventListener("change", async (event) => {
    qualityState.unitId = event.target.value;
    await loadHealthReport();
  });
  q("health-severity").addEventListener("change", (event) => {
    qualityState.healthSeverity = event.target.value;
    renderHealthReport();
  });
  q("health-refresh-step8").addEventListener("click", loadHealthReport);
  await loadHealthReport();
}

async function loadHealthReport() {
  const params = new URLSearchParams({ course_id: currentAdminCourseId() });
  if (qualityState.unitId) params.set("unit_id", qualityState.unitId);
  const suffix = params.toString() ? `?${params.toString()}` : "";
  q("health-step8-body").innerHTML = '<p class="quality-loading">Running Content Studio quality checks…</p>';
  try {
    qualityState.health = await qualityApi(`/api/admin/quality/report${suffix}`);
    const categorySelect = q("health-category");
    if (categorySelect) {
      categorySelect.innerHTML = '<option value="">All categories</option>' + Object.keys(qualityState.health.category_counts || {}).map((key) => `<option value="${esc(key)}">${esc(humanize(key))}</option>`).join("");
      categorySelect.value = qualityState.healthCategory;
      categorySelect.onchange = (event) => {
        qualityState.healthCategory = event.target.value;
        renderHealthReport();
      };
    }
    renderHealthReport();
  } catch (error) {
    q("health-step8-body").innerHTML = `<p class="empty-state">${esc(error.message)}</p>`;
  }
}

function renderHealthReport() {
  const report = qualityState.health;
  const body = q("health-step8-body");
  if (!report || !body) return;
  let findings = Array.isArray(report.findings) ? report.findings : [];
  if (qualityState.healthSeverity) findings = findings.filter((item) => item.severity === qualityState.healthSeverity);
  if (qualityState.healthCategory) findings = findings.filter((item) => item.category === qualityState.healthCategory);
  const policy = report.policy || {};
  body.innerHTML = `
    <div class="health-summary-grid">
      <article class="health-summary-card"><span>Blocking errors</span><strong>${number(report.publication_blocking_count)}</strong></article>
      <article class="health-summary-card"><span>Warnings</span><strong>${number(report.warning_count)}</strong></article>
      <article class="health-summary-card"><span>Advisories</span><strong>${number(report.advisory_count)}</strong></article>
      <article class="health-summary-card"><span>Findings shown</span><strong>${number(findings.length)}</strong></article>
    </div>
    <div class="health-policy">
      <article><strong>Errors</strong><p>${esc(policy.errors || "Must be resolved before publication.")}</p></article>
      <article><strong>Warnings</strong><p>${esc(policy.warnings || "Require teacher review before publication.")}</p></article>
      <article><strong>Advisories</strong><p>${esc(policy.advisories || "Quality heuristics that remain subject to teacher judgment.")}</p></article>
    </div>
    <div class="quality-findings">
      ${findings.length ? findings.map((item) => `
        <article class="quality-finding ${esc(item.severity)}">
          <span class="quality-severity ${esc(item.severity)}">${esc(humanize(item.severity))}</span>
          <div><h3>${esc(humanize(item.code))}</h3><p>${esc(item.message)}</p><small>${esc(humanize(item.category))}${item.unit_id ? ` · ${esc(item.unit_id)}` : ""}${item.entity_id ? ` · ${esc(item.entity_id)}` : ""}</small>${Object.keys(item.details || {}).length ? `<details><summary>Evidence</summary><div class="quality-details">${esc(jsonSummary(item.details))}</div></details>` : ""}</div>
          ${item.entity_id && !String(item.entity_id).startsWith("asset-") && !String(item.entity_id).startsWith("new:media") ? `<button class="text-button health-preview-link" type="button" data-health-preview="${esc(item.entity_id)}">Preview</button>` : ""}
        </article>`).join("") : '<p class="empty-state">No findings match the current filters.</p>'}
    </div>`;
  body.querySelectorAll("[data-health-preview]").forEach((button) => {
    button.addEventListener("click", async () => {
      const entityId = button.dataset.healthPreview;
      const entity = await qualityApi(`/api/admin/catalog/entity?course_id=${encodeURIComponent(currentAdminCourseId())}&entity_id=${encodeURIComponent(entityId)}`).catch(() => null);
      qualityState.unitId = entity?.unit_id || qualityState.unitId || "unit-1";
      qualityState.entityType = entity?.type || "scene";
      qualityState.selectedEntityId = entityId;
      qualityState.previewSource = "auto";
      await activateQuality("preview");
      if (qualityState.records.some((item) => item.id === entityId)) await loadPreview(entityId);
    });
  });
}

window.addEventListener("story-method-course-changed", (event) => {
  qualityState.units = Array.isArray(event.detail?.units) ? event.detail.units : [];
  qualityState.unitId = qualityState.units[0]?.unit_id || "";
  qualityState.entityType = "scene";
  qualityState.query = "";
  qualityState.records = [];
  qualityState.selectedEntityId = null;
  qualityState.preview = null;
  qualityState.previewSource = "auto";
  qualityState.sceneIndex = 0;
  qualityState.recallOpen = false;
  qualityState.answerRevealed = false;
  qualityState.health = null;
  qualityState.healthSeverity = "";
  qualityState.healthCategory = "";
  q("quality-view")?.classList.add("hidden");
});

ensureQualityUi();
