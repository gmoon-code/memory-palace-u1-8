const editorModes = {
  units: { entityType: "unit", title: "Units", eyebrow: "Course structure", focusGroup: null },
  journeys: { entityType: "journey", title: "Journeys", eyebrow: "Narrative structure", focusGroup: null },
  scenes: { entityType: "scene", title: "Scenes", eyebrow: "Scene workspace", focusGroup: null },
  stories: { entityType: "scene", title: "Stories", eyebrow: "Narrative editor", focusGroup: "story" },
  characters: { entityType: "character", title: "Characters", eyebrow: "Narrative cast", focusGroup: null },
  locations: { entityType: "location", title: "Locations", eyebrow: "Spatial architecture", focusGroup: null },
  concepts: { entityType: "concept", title: "Concept Library", eyebrow: "Scientific backbone", focusGroup: null },
  "memory-objects": { entityType: "memory_object", title: "Memory Objects", eyebrow: "Memory architecture", focusGroup: null },
};

const editorState = {
  mode: null,
  entityType: null,
  focusGroup: null,
  schema: null,
  records: [],
  selectedEntity: null,
  currentDraft: null,
  workingPayload: null,
  csrfToken: "",
  saveTimer: null,
  saving: false,
  dirty: false,
  changeSerial: 0,
};

function currentAdminCourseId() {
  return document.getElementById("admin-course-select")?.value || "ap-biology";
}

function currentAdminCourseEditable() {
  return document.getElementById("admin-course-select")?.selectedOptions?.[0]?.dataset?.editable === "true";
}

function e(id) {
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

function unitLabel(unitId) {
  return unitId ? unitId.replace("unit-", "Unit ") : "Course-wide";
}

async function editorApi(url, options = {}) {
  const headers = new Headers(options.headers || {});
  headers.set("Accept", "application/json");
  if (options.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  if (options.csrf) {
    if (!editorState.csrfToken) {
      const session = await editorApi("/api/admin/session");
      editorState.csrfToken = session.csrf_token || "";
    }
    headers.set("X-CSRF-Token", editorState.csrfToken);
  }
  const response = await fetch(url, {
    credentials: "same-origin",
    cache: "no-store",
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

function ensureEditorUi() {
  if (!document.querySelector('link[href="/admin/editor.css"]')) {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "/admin/editor.css";
    document.head.appendChild(link);
  }

  const status = document.querySelector(".brand-block .status-pill");
  if (status) status.textContent = "Step 5 field editors";

  const nav = document.querySelector(".admin-nav");
  const storiesButton = nav?.querySelector('[data-view="stories"]');
  if (nav && storiesButton && !nav.querySelector('[data-view="characters"]')) {
    const characters = document.createElement("button");
    characters.className = "nav-item";
    characters.dataset.view = "characters";
    characters.type = "button";
    characters.textContent = "Characters";
    storiesButton.insertAdjacentElement("afterend", characters);

    const locations = document.createElement("button");
    locations.className = "nav-item";
    locations.dataset.view = "locations";
    locations.type = "button";
    locations.textContent = "Locations";
    characters.insertAdjacentElement("afterend", locations);
  }

  if (!e("editor-view")) {
    const section = document.createElement("section");
    section.id = "editor-view";
    section.className = "view-panel hidden";
    section.setAttribute("aria-live", "polite");
    section.innerHTML = `
      <div class="editor-workspace">
        <section class="panel editor-browser">
          <div class="panel-heading">
            <div>
              <p class="eyebrow">Published catalog</p>
              <h2 id="editor-browser-title">Records</h2>
            </div>
            <span id="editor-record-count" class="read-only-badge"></span>
          </div>
          <div class="editor-toolbar">
            <div class="editor-toolbar-row">
              <input id="editor-search" type="search" placeholder="Filter records…" maxlength="160"/>
              <select id="editor-unit-filter" aria-label="Filter by unit">
                <option value="">All units</option>
                <option value="unit-1">Unit 1</option>
                <option value="unit-2">Unit 2</option>
                <option value="unit-3">Unit 3</option>
                <option value="unit-4">Unit 4</option>
                <option value="unit-5">Unit 5</option>
                <option value="unit-6">Unit 6</option>
                <option value="unit-7">Unit 7</option>
                <option value="unit-8">Unit 8</option>
              </select>
            </div>
            <p class="muted">Select a published record, then open a protected working copy to edit it.</p>
          </div>
          <div id="editor-record-list" class="editor-record-list"></div>
        </section>

        <section class="panel editor-main">
          <div id="editor-empty" class="editor-empty">
            <p class="eyebrow">Field-specific editor</p>
            <h2>Select a record</h2>
            <p>The editor keeps the published student site locked. Changes are stored in the protected draft and revision system until a later publication step.</p>
          </div>
          <div id="editor-active" class="hidden">
            <header class="editor-header">
              <div>
                <p id="editor-record-type" class="eyebrow">Record</p>
                <h2 id="editor-record-title">Editor</h2>
                <p id="editor-record-meta" class="muted"></p>
              </div>
              <div class="editor-header-actions">
                <span id="editor-save-state" class="editor-state">Published base</span>
                <button id="editor-start-draft" class="button primary" type="button">Open working copy</button>
                <button id="editor-snapshot" class="button secondary hidden" type="button">Create snapshot</button>
              </div>
            </header>
            <div id="editor-published-summary" class="editor-published-summary"></div>
            <div id="editor-dependencies" class="editor-dependency-strip"></div>
            <div id="editor-readonly-note" class="editor-readonly-note">You are viewing the published base. Open a working copy to make changes.</div>
            <form id="field-editor-form" class="editor-form"></form>
            <footer id="editor-footer" class="editor-footer hidden">
              <span id="editor-message" class="editor-message">Draft changes stay separate from student content.</span>
              <div class="editor-footer-actions">
                <button id="editor-discard-local" class="button secondary" type="button">Reload saved draft</button>
                <button id="editor-save-now" class="button primary" type="button">Save now</button>
              </div>
            </footer>
          </div>
        </section>
      </div>`;
    const placeholder = e("placeholder-view");
    if (placeholder) placeholder.insertAdjacentElement("beforebegin", section);
    else document.querySelector("#admin-main")?.appendChild(section);
  }

  bindEditorUi();
}

function bindEditorUi() {
  e("editor-search")?.addEventListener("input", renderRecordList);
  e("editor-unit-filter")?.addEventListener("change", loadRecords);
  e("editor-start-draft")?.addEventListener("click", openWorkingCopy);
  e("editor-save-now")?.addEventListener("click", () => saveDraft(false));
  e("editor-discard-local")?.addEventListener("click", reloadSavedDraft);
  e("editor-snapshot")?.addEventListener("click", createEditorSnapshot);

  document.querySelectorAll(".nav-item").forEach((button) => {
    if (button.dataset.editorBound === "true") return;
    button.dataset.editorBound = "true";
    button.addEventListener(
      "click",
      (event) => {
        const mode = editorModes[button.dataset.view];
        if (mode) {
          event.preventDefault();
          event.stopImmediatePropagation();
          activateEditor(button.dataset.view);
        } else {
          e("editor-view")?.classList.add("hidden");
        }
      },
      true
    );
  });
}

function setHeader(mode) {
  e("view-eyebrow").textContent = mode.eyebrow;
  e("view-title").textContent = mode.title;
  e("view-description").textContent =
    mode.entityType === "scene" && mode.focusGroup === "story"
      ? "Edit complete scene narratives paragraph by paragraph while preserving scene identity, spatial context, retrieval links, and recoverable draft history."
      : `Edit ${mode.title.toLowerCase()} through structured fields backed by protected working copies and revision history.`;
  document.querySelectorAll(".nav-item").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === editorState.mode);
  });
}

async function activateEditor(modeName) {
  const mode = editorModes[modeName];
  if (!mode) return;
  clearTimeout(editorState.saveTimer);
  editorState.mode = modeName;
  editorState.entityType = mode.entityType;
  editorState.focusGroup = mode.focusGroup;
  editorState.schema = null;
  editorState.records = [];
  editorState.selectedEntity = null;
  editorState.currentDraft = null;
  editorState.workingPayload = null;
  editorState.dirty = false;

  document.querySelectorAll(".view-panel").forEach((panel) => panel.classList.add("hidden"));
  e("editor-view").classList.remove("hidden");
  setHeader(mode);
  e("editor-browser-title").textContent = mode.title;
  e("editor-search").value = "";
  e("editor-unit-filter").value = "";
  resetEditorMain();
  await loadSchema();
  await loadRecords();
}

function resetEditorMain() {
  e("editor-empty").classList.remove("hidden");
  e("editor-active").classList.add("hidden");
  e("field-editor-form").innerHTML = "";
}

async function loadSchema() {
  try {
    editorState.schema = await editorApi(`/api/admin/editors/schema?entity_type=${encodeURIComponent(editorState.entityType)}`);
  } catch (error) {
    e("editor-record-list").innerHTML = `<p class="empty-state">${esc(error.message)}</p>`;
  }
}

async function loadRecords() {
  const params = new URLSearchParams({ course_id: currentAdminCourseId(), entity_type: editorState.entityType, limit: "500" });
  const unit = e("editor-unit-filter")?.value;
  if (unit) params.set("unit_id", unit);
  e("editor-record-list").innerHTML = '<p class="empty-state">Loading records…</p>';
  try {
    const payload = await editorApi(`/api/admin/catalog/entities?${params.toString()}`);
    editorState.records = Array.isArray(payload.items) ? payload.items : [];
    renderRecordList();
  } catch (error) {
    e("editor-record-list").innerHTML = `<p class="empty-state">${esc(error.message)}</p>`;
  }
}

function recordSubtitle(item) {
  if (item.type === "scene") return `${item.palace_id || ""} · ${item.locus || ""}`;
  if (item.type === "journey") return item.palace_name || item.palace_id || "";
  if (item.type === "concept") return item.knowledge_id || "";
  if (item.type === "memory_object") return item.memory_object_id || "";
  if (item.type === "character") return item.kind || item.role || "";
  if (item.type === "location") return item.locus_id || item.locus || "";
  return item.id || "";
}

function renderRecordList() {
  const query = (e("editor-search")?.value || "").trim().toLowerCase();
  const items = editorState.records.filter((item) => {
    if (!query) return true;
    const text = [item.title, item.id, item.unit_id, recordSubtitle(item)].filter(Boolean).join(" ").toLowerCase();
    return text.includes(query);
  });
  e("editor-record-count").textContent = `${items.length} records`;
  e("editor-record-list").innerHTML = items.length
    ? items
        .map(
          (item) => `
            <button class="editor-record ${editorState.selectedEntity?.id === item.id ? "active" : ""}" type="button" data-editor-entity="${esc(item.id)}">
              <strong>${esc(item.title || item.id)}</strong>
              <small>${esc(unitLabel(item.unit_id))} · ${esc(recordSubtitle(item))}</small>
            </button>`
        )
        .join("")
    : '<p class="empty-state">No records match this filter.</p>';
  e("editor-record-list").querySelectorAll("[data-editor-entity]").forEach((button) => {
    button.addEventListener("click", () => selectEntity(button.dataset.editorEntity));
  });
}

async function selectEntity(entityId) {
  clearTimeout(editorState.saveTimer);
  if (editorState.dirty && !window.confirm("This editor has unsaved local changes. Leave this record and discard those unsaved changes?")) return;
  try {
    const [payload, dependencies] = await Promise.all([
      editorApi(`/api/admin/editors/entity?entity_id=${encodeURIComponent(entityId)}&course_id=${encodeURIComponent(currentAdminCourseId())}`),
      editorApi(`/api/admin/catalog/dependencies?entity_id=${encodeURIComponent(entityId)}&course_id=${encodeURIComponent(currentAdminCourseId())}&depth=2&limit=500`),
    ]);
    editorState.selectedEntity = payload.entity;
    editorState.schema = payload.editor_schema || editorState.schema;
    editorState.currentDraft = null;
    editorState.workingPayload = structuredClone(payload.entity);
    editorState.dirty = false;
    renderRecordList();
    renderEditor(payload.entity, dependencies, false);
  } catch (error) {
    showMessage(error.message, true);
  }
}

function renderDependencyStrip(report) {
  const counts = report?.related_counts_by_type || {};
  const selected = ["concept", "memory_object", "question", "scene", "challenge"];
  e("editor-dependencies").innerHTML = selected
    .map((type) => `<div><strong>${Number(counts[type] || 0).toLocaleString()}</strong><span>${esc(humanize(type))}</span></div>`)
    .join("");
}

function renderEditor(payload, dependencies, editable) {
  const courseEditable = currentAdminCourseEditable();
  e("editor-empty").classList.add("hidden");
  e("editor-active").classList.remove("hidden");
  e("editor-record-type").textContent = `${humanize(payload.type)} · ${editable ? "working copy" : courseEditable ? "published base" : "read-only catalog"}`;
  e("editor-record-title").textContent = payload.title || payload.canonical_term || payload.id;
  e("editor-record-meta").textContent = `${payload.id} · ${unitLabel(payload.unit_id)}${editorState.currentDraft ? ` · draft v${editorState.currentDraft.version}` : ""}`;
  e("editor-published-summary").textContent = editable
    ? "You are editing a protected working copy. Student-facing files remain unchanged until the later validation and publication workflow is completed."
    : courseEditable
      ? "This is the current normalized published record. Opening a working copy creates an isolated, revisioned draft without changing what students see."
      : "This development course is available for catalog and dependency inspection only. Editing remains locked until the course-specific authoring workflows pass isolation QA.";
  renderDependencyStrip(dependencies);
  e("editor-readonly-note").classList.toggle("hidden", editable);
  e("editor-readonly-note").textContent = courseEditable
    ? "You are viewing the published base. Open a working copy to make changes."
    : "Read-only architecture preview. Working copies are disabled for this course.";
  e("editor-start-draft").classList.toggle("hidden", editable || !courseEditable);
  e("editor-snapshot").classList.toggle("hidden", !editable);
  e("editor-footer").classList.toggle("hidden", !editable);
  setEditorState(editable ? "Saved" : courseEditable ? "Published base" : "Read only");
  renderForm(payload, editable);
}

function getPath(payload, path) {
  return path.split(".").reduce((current, key) => (current && typeof current === "object" ? current[key] : undefined), payload);
}

function setPath(payload, path, value) {
  const parts = path.split(".");
  let current = payload;
  parts.slice(0, -1).forEach((part) => {
    if (!current[part] || typeof current[part] !== "object" || Array.isArray(current[part])) current[part] = {};
    current = current[part];
  });
  current[parts.at(-1)] = value;
}

function orderedGroups() {
  const groups = [...(editorState.schema?.groups || [])];
  if (!editorState.focusGroup) return groups;
  return groups.sort((a, b) => (a.id === editorState.focusGroup ? -1 : b.id === editorState.focusGroup ? 1 : 0));
}

function renderForm(payload, editable) {
  const form = e("field-editor-form");
  form.innerHTML = orderedGroups()
    .map(
      (group) => `
        <section class="editor-group" data-editor-group="${esc(group.id)}">
          <div class="editor-group-heading">
            <h3>${esc(group.title)}</h3>
            ${group.description ? `<p>${esc(group.description)}</p>` : ""}
          </div>
          <div class="editor-group-body">
            ${(group.fields || []).map((field) => renderField(field, payload, editable)).join("")}
          </div>
        </section>`
    )
    .join("");
  bindFormControls(editable);
  updateStoryStats();
  if (editorState.focusGroup) {
    form.querySelector(`[data-editor-group="${CSS.escape(editorState.focusGroup)}"]`)?.scrollIntoView({ block: "nearest" });
  }
}

function renderField(field, payload, editable) {
  const value = getPath(payload, field.path);
  const disabled = editable ? "" : " disabled";
  if (field.type === "checkbox") {
    return `<div class="editor-field"><label class="editor-checkbox"><input data-field-path="${esc(field.path)}" data-field-type="checkbox" type="checkbox" ${value ? "checked" : ""}${disabled}/> ${esc(field.label)}</label></div>`;
  }
  if (field.type === "textarea") {
    return `<div class="editor-field"><label>${esc(field.label)}</label><textarea data-field-path="${esc(field.path)}" data-field-type="textarea" rows="${Number(field.rows || 5)}"${disabled}>${esc(value ?? "")}</textarea></div>`;
  }
  if (field.type === "number") {
    return `<div class="editor-field"><label>${esc(field.label)}</label><input data-field-path="${esc(field.path)}" data-field-type="number" type="number" value="${esc(value ?? "")}" ${field.minimum != null ? `min="${field.minimum}"` : ""} ${field.maximum != null ? `max="${field.maximum}"` : ""}${disabled}/></div>`;
  }
  if (field.type === "list") {
    const text = Array.isArray(value) ? value.join("\n") : value ?? "";
    return `<div class="editor-field"><label>${esc(field.label)}</label><textarea data-field-path="${esc(field.path)}" data-field-type="list" rows="4"${disabled}>${esc(text)}</textarea><span class="editor-field-help">One item per line.</span></div>`;
  }
  if (field.type === "paragraphs") return renderParagraphEditor(field, value, editable);
  if (field.type === "object_list") return renderObjectList(field, value, editable);
  return `<div class="editor-field"><label>${esc(field.label)}</label><input data-field-path="${esc(field.path)}" data-field-type="text" type="text" value="${esc(value ?? "")}" maxlength="${Number(field.max_length || 50000)}"${disabled}/></div>`;
}

function renderParagraphEditor(field, value, editable) {
  const paragraphs = Array.isArray(value) ? value : value ? [String(value)] : [];
  const controls = editable
    ? '<button class="add-row-button" type="button" data-paragraph-action="add">Add paragraph</button>'
    : "";
  return `
    <div class="editor-field" data-paragraph-field="${esc(field.path)}">
      <div class="paragraph-toolbar"><strong>${esc(field.label)}</strong>${controls}</div>
      <div class="story-stats" id="story-editor-stats"></div>
      <div class="paragraph-editor">
        ${paragraphs
          .map(
            (paragraph, index) => `
              <article class="paragraph-card" data-paragraph-index="${index}">
                <div class="paragraph-toolbar">
                  <strong>Paragraph ${index + 1}</strong>
                  ${
                    editable
                      ? `<div class="paragraph-actions">
                          <button type="button" data-paragraph-action="up" data-index="${index}">Up</button>
                          <button type="button" data-paragraph-action="down" data-index="${index}">Down</button>
                          <button type="button" data-paragraph-action="duplicate" data-index="${index}">Duplicate</button>
                          <button type="button" data-paragraph-action="delete" data-index="${index}">Delete</button>
                        </div>`
                      : ""
                  }
                </div>
                <textarea data-paragraph-text="${index}" ${editable ? "" : "disabled"}>${esc(paragraph)}</textarea>
              </article>`
          )
          .join("") || '<p class="empty-state compact">No story paragraphs are currently recorded.</p>'}
      </div>
    </div>`;
}

function renderObjectList(field, value, editable) {
  const items = Array.isArray(value) ? value : [];
  return `
    <div class="editor-field" data-object-list-field="${esc(field.path)}">
      <div class="object-list-toolbar">
        <strong>${esc(field.label)}</strong>
        ${editable ? '<button class="add-row-button" type="button" data-object-action="add">Add item</button>' : ""}
      </div>
      <div class="object-list">
        ${items
          .map(
            (item, index) => `
              <article class="object-list-item" data-object-index="${index}">
                <div class="object-list-toolbar">
                  <strong>Item ${index + 1}</strong>
                  ${
                    editable
                      ? `<div class="object-actions">
                          <button type="button" data-object-action="up" data-index="${index}">Up</button>
                          <button type="button" data-object-action="down" data-index="${index}">Down</button>
                          <button type="button" data-object-action="delete" data-index="${index}">Delete</button>
                        </div>`
                      : ""
                  }
                </div>
                <div class="object-list-fields">
                  ${(field.item_fields || [])
                    .map((subfield) => {
                      const subvalue = item?.[subfield.path] ?? "";
                      const full = subfield.type === "textarea" ? " full" : "";
                      return `<div class="object-field${full}"><label>${esc(subfield.label)}</label>${
                        subfield.type === "textarea"
                          ? `<textarea rows="${Number(subfield.rows || 3)}" data-object-value="${index}" data-object-key="${esc(subfield.path)}" ${editable ? "" : "disabled"}>${esc(subvalue)}</textarea>`
                          : `<input type="text" value="${esc(subvalue)}" data-object-value="${index}" data-object-key="${esc(subfield.path)}" ${editable ? "" : "disabled"}/>`
                      }</div>`;
                    })
                    .join("")}
                </div>
              </article>`
          )
          .join("") || '<p class="empty-state compact">No items are currently recorded.</p>'}
      </div>
    </div>`;
}

function bindFormControls(editable) {
  if (!editable) return;
  const form = e("field-editor-form");
  form.querySelectorAll("[data-field-path]").forEach((control) => {
    control.addEventListener("input", () => {
      const type = control.dataset.fieldType;
      let value = control.value;
      if (type === "checkbox") value = control.checked;
      if (type === "number") value = control.value === "" ? null : Number(control.value);
      if (type === "list") value = control.value.split(/\r?\n/).map((item) => item.trim()).filter(Boolean);
      setPath(editorState.workingPayload, control.dataset.fieldPath, value);
      markDirty();
    });
  });

  form.querySelectorAll("[data-paragraph-text]").forEach((textarea) => {
    textarea.addEventListener("input", () => {
      const field = textarea.closest("[data-paragraph-field]")?.dataset.paragraphField;
      const index = Number(textarea.dataset.paragraphText);
      const paragraphs = getPath(editorState.workingPayload, field) || [];
      paragraphs[index] = textarea.value;
      setPath(editorState.workingPayload, field, paragraphs);
      updateStoryStats();
      markDirty();
    });
  });

  form.querySelectorAll("[data-paragraph-action]").forEach((button) => {
    button.addEventListener("click", () => handleParagraphAction(button));
  });

  form.querySelectorAll("[data-object-value]").forEach((control) => {
    control.addEventListener("input", () => {
      const container = control.closest("[data-object-list-field]");
      const path = container.dataset.objectListField;
      const items = getPath(editorState.workingPayload, path) || [];
      const index = Number(control.dataset.objectValue);
      items[index] ||= {};
      items[index][control.dataset.objectKey] = control.value;
      setPath(editorState.workingPayload, path, items);
      markDirty();
    });
  });

  form.querySelectorAll("[data-object-action]").forEach((button) => {
    button.addEventListener("click", () => handleObjectAction(button));
  });
}

function handleParagraphAction(button) {
  const container = button.closest("[data-paragraph-field]");
  const path = container.dataset.paragraphField;
  const paragraphs = [...(getPath(editorState.workingPayload, path) || [])];
  const index = Number(button.dataset.index);
  const action = button.dataset.paragraphAction;
  if (action === "add") paragraphs.push("");
  if (action === "up" && index > 0) [paragraphs[index - 1], paragraphs[index]] = [paragraphs[index], paragraphs[index - 1]];
  if (action === "down" && index < paragraphs.length - 1) [paragraphs[index + 1], paragraphs[index]] = [paragraphs[index], paragraphs[index + 1]];
  if (action === "duplicate" && Number.isInteger(index)) paragraphs.splice(index + 1, 0, paragraphs[index]);
  if (action === "delete" && Number.isInteger(index)) paragraphs.splice(index, 1);
  setPath(editorState.workingPayload, path, paragraphs);
  markDirty();
  renderForm(editorState.workingPayload, true);
}

function handleObjectAction(button) {
  const container = button.closest("[data-object-list-field]");
  const path = container.dataset.objectListField;
  const items = [...(getPath(editorState.workingPayload, path) || [])].map((item) => ({ ...item }));
  const index = Number(button.dataset.index);
  const action = button.dataset.objectAction;
  const field = [...(editorState.schema.groups || [])].flatMap((group) => group.fields || []).find((candidate) => candidate.path === path);
  if (action === "add") {
    const empty = {};
    (field?.item_fields || []).forEach((itemField) => (empty[itemField.path] = ""));
    items.push(empty);
  }
  if (action === "up" && index > 0) [items[index - 1], items[index]] = [items[index], items[index - 1]];
  if (action === "down" && index < items.length - 1) [items[index + 1], items[index]] = [items[index], items[index + 1]];
  if (action === "delete" && Number.isInteger(index)) items.splice(index, 1);
  setPath(editorState.workingPayload, path, items);
  markDirty();
  renderForm(editorState.workingPayload, true);
}

function updateStoryStats() {
  const node = e("story-editor-stats");
  if (!node) return;
  const paragraphs = Array.isArray(editorState.workingPayload?.story_paragraphs) ? editorState.workingPayload.story_paragraphs : [];
  const words = paragraphs.join(" ").trim().split(/\s+/).filter(Boolean).length;
  const chars = paragraphs.join("\n\n").length;
  node.innerHTML = `<span>${paragraphs.length} paragraphs</span><span>${words.toLocaleString()} words</span><span>${chars.toLocaleString()} characters</span>`;
}

function markDirty() {
  editorState.dirty = true;
  editorState.changeSerial += 1;
  setEditorState("Unsaved changes", "pending");
  clearTimeout(editorState.saveTimer);
  editorState.saveTimer = setTimeout(() => saveDraft(true), 1200);
}

function setEditorState(message, mode = "saved") {
  const node = e("editor-save-state");
  if (!node) return;
  node.textContent = message;
  node.classList.remove("pending", "error");
  if (mode === "pending") node.classList.add("pending");
  if (mode === "error") node.classList.add("error");
}

function showMessage(message, error = false) {
  const node = e("editor-message");
  if (!node) return;
  node.textContent = message;
  node.classList.toggle("error", error);
}

async function openWorkingCopy() {
  if (!editorState.selectedEntity) return;
  try {
    setEditorState("Opening draft…", "pending");
    const draft = await editorApi("/api/admin/editors/drafts", {
      method: "POST",
      csrf: true,
      body: JSON.stringify({ entity_id: editorState.selectedEntity.id, course_id: currentAdminCourseId() }),
    });
    editorState.currentDraft = draft;
    editorState.workingPayload = structuredClone(draft.payload || {});
    editorState.dirty = false;
    editorState.changeSerial = 0;
    const dependencies = await editorApi(`/api/admin/catalog/dependencies?entity_id=${encodeURIComponent(draft.entity_id)}&course_id=${encodeURIComponent(draft.course_id || currentAdminCourseId())}&depth=2&limit=500`);
    renderEditor(editorState.workingPayload, dependencies, draft.status === "draft");
    if (draft.status === "archived") {
      e("editor-readonly-note").classList.remove("hidden");
      e("editor-readonly-note").textContent = "This working copy is archived. Restore it from Draft Workspace before editing.";
      e("editor-footer").classList.add("hidden");
    }
  } catch (error) {
    setEditorState("Could not open draft", "error");
    showMessage(error.message, true);
  }
}

async function saveDraft(autosave) {
  clearTimeout(editorState.saveTimer);
  if (!editorState.currentDraft || !editorState.dirty || editorState.currentDraft.status !== "draft") return editorState.currentDraft;
  if (editorState.saving) {
    editorState.saveTimer = setTimeout(() => saveDraft(true), 500);
    return null;
  }
  editorState.saving = true;
  const serial = editorState.changeSerial;
  const payload = structuredClone(editorState.workingPayload);
  setEditorState(autosave ? "Autosaving…" : "Saving…", "pending");
  try {
    const saved = await editorApi(`/api/admin/editors/drafts/${encodeURIComponent(editorState.currentDraft.draft_id)}`, {
      method: "PATCH",
      csrf: true,
      body: JSON.stringify({
        payload,
        expected_version: editorState.currentDraft.version,
        note: autosave ? "Field editor autosave" : "Field editor save",
        autosave: Boolean(autosave),
      }),
    });
    editorState.currentDraft = { ...saved, payload: editorState.workingPayload };
    if (editorState.changeSerial === serial) {
      editorState.dirty = false;
      setEditorState(saved.unchanged ? "No changes" : "Saved");
      showMessage(`Draft v${saved.version} saved. Published student content is unchanged.`);
    } else {
      editorState.dirty = true;
      setEditorState("More changes pending", "pending");
      editorState.saveTimer = setTimeout(() => saveDraft(true), 600);
    }
    e("editor-record-meta").textContent = `${saved.entity_id} · ${unitLabel(saved.unit_id)} · draft v${saved.version}`;
    return saved;
  } catch (error) {
    if (error.status === 409) {
      setEditorState("Newer version exists", "error");
      showMessage("This draft was changed elsewhere. Reload the saved draft before continuing so a newer revision is not overwritten.", true);
    } else {
      setEditorState("Save failed", "error");
      showMessage(error.message, true);
    }
    return null;
  } finally {
    editorState.saving = false;
  }
}

async function reloadSavedDraft() {
  if (!editorState.currentDraft) return;
  if (editorState.dirty && !window.confirm("Discard local unsaved changes and reload the last saved draft revision?")) return;
  try {
    const draft = await editorApi(`/api/admin/drafts/${encodeURIComponent(editorState.currentDraft.draft_id)}`);
    editorState.currentDraft = draft;
    editorState.workingPayload = structuredClone(draft.payload || {});
    editorState.dirty = false;
    renderForm(editorState.workingPayload, draft.status === "draft");
    setEditorState("Saved");
    showMessage(`Reloaded draft v${draft.version}.`);
  } catch (error) {
    showMessage(error.message, true);
  }
}

async function createEditorSnapshot() {
  if (!editorState.currentDraft) return;
  if (editorState.dirty) {
    const saved = await saveDraft(false);
    if (!saved || editorState.dirty) return;
  }
  const label = window.prompt("Name this recovery snapshot", `Before major edit · v${editorState.currentDraft.version}`);
  if (!label?.trim()) return;
  try {
    await editorApi(`/api/admin/drafts/${encodeURIComponent(editorState.currentDraft.draft_id)}/snapshots`, {
      method: "POST",
      csrf: true,
      body: JSON.stringify({ label: label.trim() }),
    });
    showMessage(`Snapshot “${label.trim()}” created.`);
  } catch (error) {
    showMessage(error.message, true);
  }
}

ensureEditorUi();

window.addEventListener("story-method-course-changed", (event) => {
  clearTimeout(editorState.saveTimer);
  editorState.records = [];
  editorState.selectedEntity = null;
  editorState.currentDraft = null;
  editorState.workingPayload = null;
  editorState.dirty = false;
  const select = e("editor-unit-filter");
  if (select) {
    const units = Array.isArray(event.detail?.units) ? event.detail.units : [];
    select.innerHTML = '<option value="">All units</option>' + units
      .map((unit) => `<option value="${esc(unit.unit_id)}">Unit ${Number(unit.number) || ""} · ${esc(unit.title || unit.unit_id)}</option>`)
      .join("");
  }
  resetEditorMain();
  if (!e("editor-view")?.classList.contains("hidden") && editorState.mode) {
    loadRecords();
  }
});
