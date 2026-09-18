const state = {
  csrfToken: "",
  session: null,
  courses: [],
  selectedCourseId: "ap-biology",
  selectedCourse: null,
  catalogSummary: null,
  courseMap: null,
  currentCatalogType: null,
};

const views = {
  dashboard: {
    title: "Dashboard",
    eyebrow: "Content overview",
    description: "A protected normalized inventory of the currently selected Story Method course.",
  },
  "course-map": {
    title: "Course Map",
    eyebrow: "Structure",
    description: "Browse the current Unit → Journey → Scene hierarchy and inspect linked scientific and retrieval dependencies.",
  },
  units: {
    title: "Units",
    eyebrow: "Course structure",
    description: "Browse normalized Unit records before editing capabilities are introduced.",
  },
  journeys: {
    title: "Journeys",
    eyebrow: "Narrative structure",
    description: "Browse all guided journeys in the selected course through one consistent normalized catalog.",
  },
  scenes: {
    title: "Scenes",
    eyebrow: "Scene workspace",
    description: "Browse permanent scenes, loci, story load, characters, Memory Objects, and dependency links.",
  },
  stories: {
    title: "Stories",
    eyebrow: "Narrative editor",
    description: "The story editor will use the normalized scene and dependency records created in this stage.",
  },
  replacement: {
    title: "Complete Story Replacement",
    eyebrow: "Major revision workflow",
    description: "The replacement workflow will use this dependency graph to preserve required knowledge and detect downstream effects.",
  },
  concepts: {
    title: "Concept Library",
    eyebrow: "Scientific backbone",
    description: "Browse canonical scientific records and their current scene, Memory Object, question, and Challenge Lab coverage.",
  },
  "memory-objects": {
    title: "Memory Objects",
    eyebrow: "Memory architecture",
    description: "Browse normalized Memory Objects and their links to canonical concepts, scenes, questions, and review records.",
  },
  questions: {
    title: "Question Bank",
    eyebrow: "Assessment",
    description: "Browse normalized Quick Recall, delayed review, and mixed-discrimination questions through one catalog.",
  },
  review: {
    title: "Review System",
    eyebrow: "Retrieval planning",
    description: "Review scheduling and retrieval timelines will build on the normalized question and concept graph.",
  },
  challenge: {
    title: "Challenge Lab",
    eyebrow: "Application",
    description: "Browse Challenge Lab records, prerequisite scenes, and linked scientific concepts within the selected course.",
  },
  media: {
    title: "Media Library",
    eyebrow: "Assets",
    description: "Media dependency indexing will be added after the draft store is established.",
  },
  preview: {
    title: "Student Preview",
    eyebrow: "Experience check",
    description: "Draft-aware student preview arrives after the revision layer is established.",
  },
  health: {
    title: "Content Health",
    eyebrow: "Validation",
    description: "Compare normalized totals with the frozen release and surface unresolved references or incomplete records.",
  },
  versions: {
    title: "Version History",
    eyebrow: "Recovery",
    description: "Revision history will be implemented with the draft store in the next stage.",
  },
  "import-export": {
    title: "Import and Export",
    eyebrow: "Portability",
    description: "Validated import and export will use the normalized catalog as its stable content model.",
  },
  publishing: {
    title: "Publishing",
    eyebrow: "Release control",
    description: "Publishing remains disabled until drafts, revisions, validation, and recoverable snapshots exist.",
  },
  security: {
    title: "Security and Audit",
    eyebrow: "Administration security",
    description: "Authentication, session protections, CSRF enforcement, sign-in throttling, and recent administrative security events are visible here.",
  },
  settings: {
    title: "Settings",
    eyebrow: "Administration",
    description: "Permissions, editor preferences, validation policy, source settings, and publication configuration will be controlled here.",
  },
};

const catalogViews = {
  units: { entityType: "unit", label: "Units" },
  journeys: { entityType: "journey", label: "Journeys" },
  scenes: { entityType: "scene", label: "Scenes" },
  concepts: { entityType: "concept", label: "Canonical concepts" },
  "memory-objects": { entityType: "memory_object", label: "Memory Objects" },
  questions: { entityType: "question", label: "Questions" },
  challenge: { entityType: "challenge", label: "Challenge Lab items" },
};

const capabilityCards = [
  ["Narrative editing", "Paragraph, scene, journey, and full-story editing with focused writing and structural context."],
  ["Complete replacement", "Replace narrative only, narrative plus scene design, a full scene, or an entire journey while preserving required knowledge."],
  ["Questions", "Create, duplicate, vary, classify, explain, import, export, and bulk-edit questions and distractors."],
  ["Concept graph", "Track prerequisites, related concepts, misconceptions, teaching locations, later dependencies, and AP mapping."],
  ["Memory Objects", "Edit the structured memory model without exposing raw JSON during ordinary work."],
  ["Review planning", "See when each concept is learned, retrieved, delayed, discriminated, and reactivated."],
  ["Content dependencies", "Show every scene, question, review item, character, location, and lab affected by a proposed change."],
  ["Version safety", "Autosave drafts, compare revisions, restore earlier versions, archive safely, and create release snapshots."],
  ["Validation", "Block broken references and required-field failures while presenting actionable warnings for teacher review."],
  ["Student preview", "Preview the exact learner experience and return to the same editing context."],
  ["Search and bulk tools", "Global search, controlled replacement, filters, batch tagging, movement, status changes, and archive actions."],
  ["Media and audio", "Track usage, alt text, replacement, narration freshness, orphaned assets, and file metadata."],
  ["Teacher workflow", "Private notes, comments, to-do markers, recently edited content, drafts, and items ready for review."],
  ["Publishing", "Review a release summary, validate content, create a version, and publish through a controlled GitHub-backed workflow."],
  ["Access control", "Teacher-only authentication, roles, session protection, audit logs, and protected write actions."],
  ["Future analytics", "Optional student-performance signals can later connect errors and distractor patterns back to concepts and questions."],
];

function el(id) {
  return document.getElementById(id);
}

function escapeHtml(value) {
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

function formatTimestamp(epochSeconds) {
  if (!epochSeconds) return "Unknown";
  return new Date(epochSeconds * 1000).toLocaleString();
}

function humanizeKey(value) {
  return String(value)
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function unitLabel(unitId) {
  if (!unitId) return "Course-wide";
  return unitId.replace("unit-", "Unit ");
}

function courseApiUrl(path) {
  const url = new URL(path, window.location.origin);
  url.searchParams.set("course_id", state.selectedCourseId || "ap-biology");
  return `${url.pathname}${url.search}`;
}

function selectedCourseTitle() {
  return state.selectedCourse?.title || state.selectedCourse?.short_title || state.catalogSummary?.course_title || state.selectedCourseId || "Course";
}

function updateCourseChrome() {
  const course = state.courses.find((item) => item.course_id === state.selectedCourseId) || null;
  state.selectedCourse = course;
  const note = el("admin-course-note");
  if (note) {
    note.textContent = course?.catalog_ready
      ? `${course.unit_count || 0} units · catalog ready`
      : "Course content is registered but the teacher catalog is not ready yet.";
  }
  const studentLink = el("student-site-link");
  if (studentLink) {
    studentLink.href = `/?course=${encodeURIComponent(state.selectedCourseId)}`;
    studentLink.setAttribute("aria-label", `Open ${selectedCourseTitle()} student site`);
  }
}

function populateUnitFilter(courseMap) {
  const select = el("catalog-unit-filter");
  if (!select) return;
  const units = Array.isArray(courseMap?.units) ? courseMap.units : [];
  const previous = select.value;
  select.innerHTML = '<option value="">All units</option>' + units
    .map((unit) => `<option value="${escapeHtml(unit.unit_id)}">Unit ${number(unit.number)} · ${escapeHtml(unit.title)}</option>`)
    .join("");
  if ([...select.options].some((option) => option.value === previous)) select.value = previous;
}

function announceCourseContext() {
  window.dispatchEvent(new CustomEvent("story-method-course-changed", {
    detail: {
      courseId: state.selectedCourseId,
      course: state.selectedCourse,
      units: Array.isArray(state.courseMap?.units) ? state.courseMap.units : [],
    },
  }));
}

async function apiRequest(url, options = {}) {
  const headers = new Headers(options.headers || {});
  headers.set("Accept", "application/json");
  if (options.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  if (options.csrf) headers.set("X-CSRF-Token", state.csrfToken);
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
    const message = payload?.detail || `${url} returned ${response.status}`;
    const error = new Error(message);
    error.status = response.status;
    throw error;
  }
  return payload;
}

function handleApiError(error, target = null) {
  if (error.status === 401) {
    showLogin("Your admin session has expired. Sign in again.");
    return true;
  }
  if (target) target.innerHTML = `<p class="empty-state">${escapeHtml(error.message)}</p>`;
  return false;
}

function renderMetrics(summary) {
  const counts = summary?.counts || {};
  const metrics = [
    ["Units", counts.unit, "normalized unit records"],
    ["Journeys", counts.journey, "guided narrative routes"],
    ["Scenes", counts.scene, "permanent scenes"],
    ["Canonical records", counts.concept, "scientific concept records"],
    ["Challenge items", counts.challenge, "application challenges"],
  ];
  el("metric-grid").innerHTML = metrics
    .map(
      ([label, value, note]) => `
        <article class="metric-card">
          <span>${escapeHtml(label)}</span>
          <strong>${number(value)}</strong>
          <span>${escapeHtml(note)}</span>
        </article>`
    )
    .join("");
}

function renderUnits(courseMap) {
  const units = Array.isArray(courseMap?.units) ? courseMap.units : [];
  el("unit-list").innerHTML = units
    .map(
      (unit) => `
        <article class="unit-row">
          <div>
            <h3>Unit ${number(unit.number)} · ${escapeHtml(unit.title)}</h3>
            <p>${escapeHtml(unit.unit_id)}</p>
          </div>
          <div class="unit-meta" aria-label="Unit ${number(unit.number)} normalized summary">
            <span>${number(unit.journey_count)} journeys</span>
            <span>${number(unit.scene_count)} scenes</span>
          </div>
        </article>`
    )
    .join("");
}

function renderAlignment(targetId, alignment) {
  const target = el(targetId);
  const entries = Object.entries(alignment || {});
  if (!entries.length) {
    target.innerHTML = '<p class="empty-state">No frozen release comparison is available.</p>';
    return;
  }
  target.innerHTML = entries
    .map(([key, item]) => {
      const status = item.matches ? "match" : "mismatch";
      return `
        <div class="alignment-row ${status}">
          <div>
            <strong>${escapeHtml(humanizeKey(key))}</strong>
            <span>${number(item.actual)} normalized · ${number(item.expected)} frozen release</span>
          </div>
          <span class="alignment-status">${item.matches ? "Match" : "Mismatch"}</span>
        </div>`;
    })
    .join("");
}

function renderCatalogTypes(summary) {
  const labels = {
    unit: "Units",
    journey: "Journeys",
    scene: "Scenes",
    location: "Locations",
    character: "Characters and objects",
    concept: "Canonical concepts",
    memory_object: "Memory Objects",
    question: "Questions",
    question_set: "Mixed question sets",
    challenge: "Challenge Lab items",
  };
  const entries = Object.entries(summary?.counts || {}).filter(([key]) => key !== "course");
  el("catalog-type-grid").innerHTML = entries
    .map(
      ([key, value]) => `
        <article class="capability-card">
          <strong>${number(value)} ${escapeHtml(labels[key] || humanizeKey(key))}</strong>
          <span>Indexed with stable IDs and dependency links.</span>
        </article>`
    )
    .join("");
}

function renderCapabilities() {
  el("capability-grid").innerHTML = capabilityCards
    .map(
      ([title, copy]) => `
        <article class="capability-card">
          <strong>${escapeHtml(title)}</strong>
          <span>${escapeHtml(copy)}</span>
        </article>`
    )
    .join("");
}

function renderCourseMap(data) {
  const target = el("course-map-tree");
  const units = Array.isArray(data?.units) ? data.units : [];
  if (!units.length) {
    target.innerHTML = '<p class="empty-state">No normalized course structure is available.</p>';
    return;
  }
  target.innerHTML = units
    .map(
      (unit, unitIndex) => `
        <details class="map-unit" ${unitIndex === 0 ? "open" : ""}>
          <summary>
            <span>Unit ${number(unit.number)} · ${escapeHtml(unit.title)}</span>
            <small>${number(unit.journey_count)} journeys · ${number(unit.scene_count)} scenes</small>
          </summary>
          <div class="map-journeys">
            ${unit.journeys
              .map(
                (journey) => `
                  <details class="map-journey">
                    <summary>
                      <span>${escapeHtml(journey.palace_id)} · ${escapeHtml(journey.title)}</span>
                      <small>${number(journey.scene_count)} scenes · ${number(journey.checkpoint_count)} recalls</small>
                    </summary>
                    <div class="map-scenes">
                      ${journey.scenes
                        .map(
                          (scene) => `
                            <button class="map-scene" type="button" data-entity-id="${escapeHtml(scene.id)}">
                              <span class="scene-index">${number(Number(scene.scene_index) + 1)}</span>
                              <span class="scene-name">
                                <strong>${escapeHtml(scene.title)}</strong>
                                <small>${escapeHtml(scene.locus || "")}</small>
                              </span>
                              <span class="scene-stats">${number(scene.object_count)} objects · ${number(scene.character_count)} cast · ${number(scene.story_word_count)} words${scene.checkpoint ? " · recall" : ""}</span>
                            </button>`
                        )
                        .join("")}
                    </div>
                  </details>`
              )
              .join("")}
          </div>
        </details>`
    )
    .join("");
  target.querySelectorAll("[data-entity-id]").forEach((button) => {
    button.addEventListener("click", () => inspectEntity(button.dataset.entityId, "map"));
  });
}

function compactEntity(entity) {
  const title = entity?.title || entity?.id || "Untitled";
  const details = [entity?.type, entity?.unit_id, entity?.palace_id, entity?.locus_id]
    .filter(Boolean)
    .map(humanizeKey)
    .join(" · ");
  return { title, details };
}

function dependencyRows(items, direction) {
  if (!items?.length) return '<p class="empty-state compact">None</p>';
  return items
    .slice(0, 30)
    .map((item) => {
      const compact = compactEntity(item.entity);
      return `
        <button class="dependency-row" type="button" data-related-id="${escapeHtml(item.entity.id)}">
          <span>${escapeHtml(item.edge.kind)}</span>
          <strong>${escapeHtml(compact.title)}</strong>
          <small>${escapeHtml(compact.details || direction)}</small>
        </button>`;
    })
    .join("");
}

function renderDependencyReport(report, targetId, titleId) {
  const target = el(targetId);
  const titleNode = el(titleId);
  const entity = report?.entity || {};
  titleNode.textContent = entity.title || entity.id || "Linked record";
  const counts = Object.entries(report?.related_counts_by_type || {});
  target.innerHTML = `
    <div class="entity-meta">
      <span>${escapeHtml(humanizeKey(entity.type || "record"))}</span>
      <span>${escapeHtml(unitLabel(entity.unit_id))}</span>
      <code>${escapeHtml(entity.id || "")}</code>
    </div>
    ${entity.story_preview ? `<p class="inspector-preview">${escapeHtml(entity.story_preview)}</p>` : ""}
    <div class="dependency-counts">
      ${counts.map(([key, value]) => `<span><strong>${number(value)}</strong> ${escapeHtml(humanizeKey(key))}</span>`).join("") || "<span>No linked records within selected depth</span>"}
    </div>
    <section class="dependency-section">
      <h3>Directly uses or contains</h3>
      ${dependencyRows(report.direct_outbound, "outbound")}
    </section>
    <section class="dependency-section">
      <h3>Directly used by</h3>
      ${dependencyRows(report.direct_inbound, "inbound")}
    </section>
    ${entity.source_path ? `<p class="source-path"><strong>Source</strong><br/><code>${escapeHtml(entity.source_path)}</code></p>` : ""}
  `;
  target.querySelectorAll("[data-related-id]").forEach((button) => {
    button.addEventListener("click", () => inspectEntity(button.dataset.relatedId, targetId === "dependency-inspector" ? "map" : "catalog"));
  });
}

async function inspectEntity(entityId, destination = "map") {
  const targetId = destination === "catalog" ? "catalog-inspector" : "dependency-inspector";
  const titleId = destination === "catalog" ? "catalog-inspector-title" : "inspector-title";
  const target = el(targetId);
  target.innerHTML = '<p class="empty-state">Loading dependencies…</p>';
  try {
    const report = await apiRequest(courseApiUrl(`/api/admin/catalog/dependencies?entity_id=${encodeURIComponent(entityId)}&depth=2&limit=500`));
    renderDependencyReport(report, targetId, titleId);
  } catch (error) {
    handleApiError(error, target);
  }
}

async function loadCourseMap(force = false) {
  const target = el("course-map-tree");
  if (state.courseMap && !force) {
    renderCourseMap(state.courseMap);
    return;
  }
  target.innerHTML = '<p class="empty-state">Building normalized course map…</p>';
  try {
    state.courseMap = await apiRequest(courseApiUrl("/api/admin/catalog/course-map"));
    populateUnitFilter(state.courseMap);
    renderCourseMap(state.courseMap);
  } catch (error) {
    handleApiError(error, target);
  }
}

function entitySubtitle(item) {
  if (item.type === "scene") return `${item.palace_id || ""} · ${item.locus || ""}`;
  if (item.type === "journey") return item.palace_name || item.palace_id || "";
  if (item.type === "concept") return item.knowledge_id || "";
  if (item.type === "memory_object") return item.memory_object_id || "";
  if (item.type === "question") return item.question_type || "";
  if (item.type === "challenge") return item.domain || item.challenge_type || "";
  return item.id || "";
}

function renderCatalogRecords(payload) {
  const list = el("catalog-record-list");
  const items = Array.isArray(payload?.items) ? payload.items : [];
  el("catalog-result-count").textContent = `${number(payload?.total)} records`;
  if (!items.length) {
    list.innerHTML = '<p class="empty-state">No records match the selected filter.</p>';
    return;
  }
  list.innerHTML = items
    .map(
      (item) => `
        <button class="catalog-record" type="button" data-entity-id="${escapeHtml(item.id)}">
          <span class="record-type">${escapeHtml(humanizeKey(item.type))}</span>
          <span class="record-copy">
            <strong>${escapeHtml(item.title || item.id)}</strong>
            <small>${escapeHtml(unitLabel(item.unit_id))} · ${escapeHtml(entitySubtitle(item))}</small>
          </span>
          <span class="record-links">${number(item.dependency_counts?.inbound)} in · ${number(item.dependency_counts?.outbound)} out</span>
        </button>`
    )
    .join("");
  list.querySelectorAll("[data-entity-id]").forEach((button) => {
    button.addEventListener("click", () => inspectEntity(button.dataset.entityId, "catalog"));
  });
}

async function loadCatalogView(entityType = state.currentCatalogType) {
  if (!entityType) return;
  state.currentCatalogType = entityType;
  const unitId = el("catalog-unit-filter").value;
  const config = Object.values(catalogViews).find((item) => item.entityType === entityType);
  el("catalog-view-title").textContent = config?.label || humanizeKey(entityType);
  const list = el("catalog-record-list");
  list.innerHTML = '<p class="empty-state">Loading normalized records…</p>';
  const params = new URLSearchParams({ course_id: state.selectedCourseId, entity_type: entityType, limit: "500" });
  if (unitId) params.set("unit_id", unitId);
  try {
    const payload = await apiRequest(`/api/admin/catalog/entities?${params.toString()}`);
    renderCatalogRecords(payload);
  } catch (error) {
    handleApiError(error, list);
  }
}

function renderHealth(summary) {
  renderAlignment("health-alignment", summary?.release_alignment || {});
  const health = summary?.health || {};
  el("health-summary").innerHTML = `
    <div class="health-number"><strong>${number(health.error_count)}</strong><span>blocking catalog errors</span></div>
    <div class="health-number"><strong>${number(health.warning_count)}</strong><span>catalog warnings</span></div>
    <div class="health-number"><strong>${number(summary?.unresolved_reference_count)}</strong><span>unresolved source references</span></div>
  `;
  const problems = Array.isArray(health.problems) ? health.problems : [];
  el("health-problems").innerHTML = problems.length
    ? problems
        .map(
          (problem) => `
            <article class="health-problem ${escapeHtml(problem.severity)}">
              <span>${escapeHtml(problem.severity)}</span>
              <div><strong>${escapeHtml(humanizeKey(problem.code))}</strong><p>${escapeHtml(problem.message)}</p></div>
              ${problem.count != null ? `<b>${number(problem.count)}</b>` : ""}
            </article>`
        )
        .join("")
    : '<p class="empty-state">No normalized catalog warnings or errors are currently reported.</p>';
}

async function loadHealth(force = false) {
  if (state.catalogSummary && !force) {
    renderHealth(state.catalogSummary);
    return;
  }
  try {
    state.catalogSummary = await apiRequest(courseApiUrl("/api/admin/catalog/summary"));
    renderHealth(state.catalogSummary);
  } catch (error) {
    handleApiError(error, el("health-problems"));
  }
}

function renderSecurity(data) {
  const protections = data?.protections || {};
  el("security-grid").innerHTML = Object.entries(protections)
    .map(
      ([key, value]) => `
        <div class="security-item">
          <span>${escapeHtml(humanizeKey(key))}</span>
          <strong>${escapeHtml(String(value))}</strong>
        </div>`
    )
    .join("");
  const session = data?.session || {};
  el("session-details").innerHTML = `
    <div class="session-line"><span>User</span><strong>${escapeHtml(session.username || "Unknown")}</strong></div>
    <div class="session-line"><span>Role</span><strong>${escapeHtml(session.role || "Unknown")}</strong></div>
    <div class="session-line"><span>Expires</span><strong>${escapeHtml(formatTimestamp(session.expires_at))}</strong></div>
  `;
}

function renderAudit(events) {
  const list = el("audit-list");
  if (!events.length) {
    list.innerHTML = '<p class="audit-empty">No audit events are recorded yet.</p>';
    return;
  }
  list.innerHTML = events
    .map(
      (event) => `
        <article class="audit-row">
          <span class="muted">${escapeHtml(event.created_at)}</span>
          <strong>${escapeHtml(event.event)}</strong>
          <span>${escapeHtml(event.outcome)}</span>
          <span>${escapeHtml(event.detail || "")}${event.username ? ` · ${escapeHtml(event.username)}` : ""}</span>
        </article>`
    )
    .join("");
}

async function loadSecurity() {
  try {
    const [security, audit] = await Promise.all([
      apiRequest("/api/admin/security"),
      apiRequest("/api/admin/audit?limit=50"),
    ]);
    renderSecurity(security);
    renderAudit(Array.isArray(audit?.events) ? audit.events : []);
  } catch (error) {
    if (handleApiError(error)) return;
    el("audit-list").innerHTML = `<p class="audit-empty">${escapeHtml(error.message)}</p>`;
  }
}

function hideAllViews() {
  ["dashboard-view", "course-map-view", "catalog-view", "health-view", "security-view", "placeholder-view"].forEach((id) => {
    el(id).classList.add("hidden");
  });
}

function activateView(name) {
  const view = views[name] || views.dashboard;
  document.querySelectorAll(".nav-item").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === name);
  });
  el("view-title").textContent = view.title;
  el("view-eyebrow").textContent = view.eyebrow;
  el("view-description").textContent = view.description;
  hideAllViews();

  if (name === "dashboard") {
    el("dashboard-view").classList.remove("hidden");
    return;
  }
  if (name === "course-map") {
    el("course-map-view").classList.remove("hidden");
    loadCourseMap();
    return;
  }
  if (name === "health") {
    el("health-view").classList.remove("hidden");
    loadHealth();
    return;
  }
  if (name === "security") {
    el("security-view").classList.remove("hidden");
    loadSecurity();
    return;
  }
  if (catalogViews[name]) {
    el("catalog-view").classList.remove("hidden");
    el("catalog-unit-filter").value = "";
    loadCatalogView(catalogViews[name].entityType);
    return;
  }
  el("placeholder-view").classList.remove("hidden");
  el("placeholder-title").textContent = view.title;
  el("placeholder-copy").textContent = `${view.description} Step 3 has established the normalized catalog and dependency layer this workspace will use.`;
}

async function loadDashboard() {
  const banner = el("status-banner");
  banner.classList.remove("ok", "error");
  try {
    const [summary, map] = await Promise.all([
      apiRequest(courseApiUrl("/api/admin/catalog/summary")),
      apiRequest(courseApiUrl("/api/admin/catalog/course-map")),
    ]);
    state.catalogSummary = summary;
    state.courseMap = map;
    populateUnitFilter(map);
    renderMetrics(summary);
    renderUnits(map);
    renderAlignment("release-alignment", summary.release_alignment);
    renderCatalogTypes(summary);
    renderCapabilities();
    const health = summary.health || {};
    banner.textContent = `${selectedCourseTitle()} · normalized ${number(summary.counts?.concept)} scientific records, ${number(summary.counts?.journey)} journeys, and ${number(summary.counts?.scene)} scenes. ${number(health.error_count)} release-alignment errors and ${number(summary.unresolved_reference_count)} unresolved source references are currently reported.`;
    banner.classList.add(health.error_count ? "error" : "ok");
  } catch (error) {
    if (handleApiError(error)) return;
    banner.textContent = `The protected content catalog could not be built. ${error.message}`;
    banner.classList.add("error");
  }
}

function renderSearchResults(items, query) {
  const target = el("catalog-search-results");
  target.classList.remove("hidden");
  if (!items.length) {
    target.innerHTML = `<p class="empty-state">No normalized records match “${escapeHtml(query)}”.</p>`;
    return;
  }
  target.innerHTML = `
    <div class="search-results-heading"><strong>${number(items.length)} results</strong><button id="close-search-results" class="text-button" type="button">Close</button></div>
    ${items
      .map(
        (item) => `
          <button class="search-result" type="button" data-entity-id="${escapeHtml(item.id)}">
            <span>${escapeHtml(humanizeKey(item.type))}</span>
            <strong>${escapeHtml(item.title || item.id)}</strong>
            <small>${escapeHtml(unitLabel(item.unit_id))} · ${escapeHtml(entitySubtitle(item))}</small>
          </button>`
      )
      .join("")}
  `;
  target.querySelectorAll("[data-entity-id]").forEach((button) => {
    button.addEventListener("click", () => {
      activateView("course-map");
      inspectEntity(button.dataset.entityId, "map");
    });
  });
  el("close-search-results")?.addEventListener("click", () => target.classList.add("hidden"));
}

async function loadCourseContext() {
  const payload = await apiRequest("/api/admin/courses");
  state.courses = Array.isArray(payload?.courses) ? payload.courses : [];
  const editable = state.courses.filter((item) => item.catalog_ready && item.editable !== false);
  if (!editable.length) throw new Error("No Content Studio course catalog is available.");
  if (!editable.some((item) => item.course_id === state.selectedCourseId)) {
    state.selectedCourseId = editable[0].course_id;
  }
  const select = el("admin-course-select");
  select.innerHTML = state.courses
    .map((course) => `<option value="${escapeHtml(course.course_id)}" ${course.catalog_ready ? "" : "disabled"}>${escapeHtml(course.title || course.course_id)}${course.catalog_ready ? "" : " · preparing"}</option>`)
    .join("");
  select.value = state.selectedCourseId;
  updateCourseChrome();
}

async function showStudio(session) {
  state.session = session;
  state.csrfToken = session.csrf_token || "";
  el("session-user").textContent = `${session.username} · ${session.role}`;
  el("login-view").classList.add("hidden");
  el("studio-shell").classList.remove("hidden");
  el("login-message").textContent = "";
  el("admin-password").value = "";
  try {
    await loadCourseContext();
    activateView("dashboard");
    await loadDashboard();
    announceCourseContext();
  } catch (error) {
    const banner = el("status-banner");
    banner.textContent = `Content Studio could not load the course registry. ${error.message}`;
    banner.classList.add("error");
  }
}

function showLogin(message = "") {
  state.session = null;
  state.csrfToken = "";
  state.catalogSummary = null;
  state.courseMap = null;
  state.courses = [];
  state.selectedCourse = null;
  el("studio-shell").classList.add("hidden");
  el("login-view").classList.remove("hidden");
  const messageNode = el("login-message");
  messageNode.textContent = message;
  messageNode.classList.toggle("error", Boolean(message));
  el("admin-password").value = "";
  el("admin-username").focus();
}

async function restoreSession() {
  try {
    const session = await apiRequest("/api/admin/session");
    await showStudio(session);
  } catch (error) {
    if (error.status === 401) return showLogin();
    if (error.status === 503) return showLogin("Admin authentication is enabled but has not been fully configured on the server.");
    showLogin(error.message);
  }
}

el("login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const button = el("login-button");
  const messageNode = el("login-message");
  const username = el("admin-username").value.trim();
  const password = el("admin-password").value;
  button.disabled = true;
  messageNode.classList.remove("error");
  messageNode.textContent = "Signing in…";
  try {
    const session = await apiRequest("/api/admin/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    });
    await showStudio(session);
  } catch (error) {
    messageNode.textContent = error.message;
    messageNode.classList.add("error");
    el("admin-password").value = "";
    el("admin-password").focus();
  } finally {
    button.disabled = false;
  }
});

el("logout-button").addEventListener("click", async () => {
  try {
    await apiRequest("/api/admin/logout", { method: "POST", csrf: true });
  } catch (error) {
    if (error.status !== 401) {
      el("status-banner").textContent = `Sign out could not be confirmed. ${error.message}`;
      el("status-banner").classList.add("error");
      return;
    }
  }
  showLogin("You have signed out.");
});

el("catalog-search-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const query = el("catalog-search-input").value.trim();
  if (query.length < 2) return;
  const target = el("catalog-search-results");
  target.classList.remove("hidden");
  target.innerHTML = '<p class="empty-state">Searching normalized content…</p>';
  try {
    const result = await apiRequest(courseApiUrl(`/api/admin/catalog/search?q=${encodeURIComponent(query)}&limit=50`));
    renderSearchResults(Array.isArray(result.items) ? result.items : [], query);
  } catch (error) {
    handleApiError(error, target);
  }
});

el("refresh-course-map").addEventListener("click", () => loadCourseMap(true));
el("refresh-health").addEventListener("click", () => loadHealth(true));
el("refresh-audit").addEventListener("click", loadSecurity);
el("catalog-filter-apply").addEventListener("click", () => loadCatalogView());

el("admin-course-select").addEventListener("change", async (event) => {
  const next = event.target.value;
  const record = state.courses.find((item) => item.course_id === next);
  if (!record?.catalog_ready) {
    event.target.value = state.selectedCourseId;
    return;
  }
  state.selectedCourseId = next;
  state.catalogSummary = null;
  state.courseMap = null;
  state.currentCatalogType = null;
  updateCourseChrome();
  el("catalog-search-results").classList.add("hidden");
  el("catalog-search-input").value = "";
  activateView("dashboard");
  await loadDashboard();
  announceCourseContext();
});

document.querySelectorAll(".nav-item").forEach((button) => {
  button.addEventListener("click", () => activateView(button.dataset.view));
});

restoreSession();
