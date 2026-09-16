import "./editor.js";

const draftState = {
  csrfToken: "",
  statusFilter: "draft",
  currentDraft: null,
  autosaveTimer: null,
  saving: false,
};

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

function humanize(value) {
  return String(value || "")
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function formatTime(value) {
  if (!value) return "Unknown";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? String(value) : date.toLocaleString();
}

async function draftApi(url, options = {}) {
  const headers = new Headers(options.headers || {});
  headers.set("Accept", "application/json");
  if (options.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  if (options.csrf) {
    await ensureCsrf();
    headers.set("X-CSRF-Token", draftState.csrfToken);
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

async function ensureCsrf() {
  if (draftState.csrfToken) return draftState.csrfToken;
  const session = await draftApi("/api/admin/session");
  draftState.csrfToken = session.csrf_token || "";
  return draftState.csrfToken;
}

function setSaveState(message, mode = "saved") {
  const node = el("draft-save-state");
  if (!node) return;
  node.textContent = message;
  node.classList.remove("pending", "error");
  if (mode === "pending") node.classList.add("pending");
  if (mode === "error") node.classList.add("error");
}

function showDraftMessage(message, error = false) {
  const node = el("draft-payload-message");
  if (!node) return;
  node.textContent = message;
  node.classList.toggle("draft-message", true);
  node.classList.toggle("error", error);
}

function activateDraftView(mode = "drafts") {
  document.querySelectorAll(".view-panel").forEach((panel) => panel.classList.add("hidden"));
  el("draft-view")?.classList.remove("hidden");
  document.querySelectorAll(".nav-item").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === mode);
  });
  if (mode === "versions") {
    el("view-eyebrow").textContent = "Recovery";
    el("view-title").textContent = "Version History";
    el("view-description").textContent = "Review autosaved revisions, named snapshots, comparisons, archived working copies, and non-destructive restoration points.";
  } else {
    el("view-eyebrow").textContent = "Protected working copies";
    el("view-title").textContent = "Draft Workspace";
    el("view-description").textContent = "Create and revise server-side working copies while the published student content remains locked.";
  }
  loadDraftWorkspace();
}

function renderDraftSummary(summary) {
  const cards = [
    ["Active drafts", summary.active_drafts, "working copies"],
    ["Changed", summary.changed_active_drafts, "different from catalog base"],
    ["Archived", summary.archived_drafts, "recoverable drafts"],
    ["Revisions", summary.revision_count, "stored history records"],
    ["Snapshots", summary.snapshot_count, "named recovery points"],
  ];
  el("draft-summary-grid").innerHTML = cards
    .map(
      ([label, value, note]) => `
        <article class="draft-summary-card">
          <span>${escapeHtml(label)}</span>
          <strong>${number(value)}</strong>
          <span>${escapeHtml(note)}</span>
        </article>`
    )
    .join("");
}

function renderDraftList(payload) {
  const items = Array.isArray(payload?.items) ? payload.items : [];
  const target = el("draft-list");
  if (!items.length) {
    target.innerHTML = '<p class="empty-state">No drafts match this filter.</p>';
    return;
  }
  target.innerHTML = items
    .map(
      (draft) => `
        <button class="draft-list-item ${draftState.currentDraft?.draft_id === draft.draft_id ? "active" : ""}" type="button" data-draft-id="${escapeHtml(draft.draft_id)}">
          <span class="draft-list-copy">
            <strong>${escapeHtml(draft.title || draft.entity_id)}</strong>
            <small>${escapeHtml(humanize(draft.entity_type))} · ${escapeHtml(draft.unit_id || "course-wide")} · ${escapeHtml(draft.status)} · ${escapeHtml(formatTime(draft.updated_at))}</small>
          </span>
          <span class="draft-version-pill">v${number(draft.version)}</span>
        </button>`
    )
    .join("");
  target.querySelectorAll("[data-draft-id]").forEach((button) => {
    button.addEventListener("click", () => openDraft(button.dataset.draftId));
  });
}

async function loadDraftWorkspace() {
  try {
    const params = new URLSearchParams({ limit: "500" });
    if (draftState.statusFilter) params.set("status", draftState.statusFilter);
    const [summary, drafts] = await Promise.all([
      draftApi("/api/admin/drafts/summary"),
      draftApi(`/api/admin/drafts?${params.toString()}`),
    ]);
    renderDraftSummary(summary);
    renderDraftList(drafts);
  } catch (error) {
    el("draft-list").innerHTML = `<p class="empty-state">${escapeHtml(error.message)}</p>`;
  }
}

function renderDraftEditor(draft) {
  draftState.currentDraft = draft;
  el("draft-empty-state").classList.add("hidden");
  el("draft-editor").classList.remove("hidden");
  el("draft-editor-type").textContent = `${humanize(draft.entity_type)} working copy`;
  el("draft-editor-title").textContent = draft.title || draft.entity_id;
  el("draft-editor-meta").textContent = `${draft.entity_id} · ${draft.unit_id || "course-wide"} · version ${draft.version} · updated ${formatTime(draft.updated_at)}`;
  el("draft-title-input").value = draft.payload?.title || draft.payload?.canonical_term || draft.title || "";
  el("draft-title-input").disabled = draft.status === "archived";
  el("draft-payload-editor").value = JSON.stringify(draft.payload || {}, null, 2);
  el("draft-payload-editor").disabled = draft.status === "archived";
  el("save-draft-payload").disabled = draft.status === "archived";
  el("create-snapshot-button").disabled = false;
  const archiveButton = el("draft-archive-button");
  archiveButton.textContent = draft.status === "archived" ? "Restore archived draft" : "Archive";
  setSaveState(draft.status === "archived" ? "Archived" : "Saved");
  showDraftMessage("");
}

async function openDraft(draftId) {
  clearTimeout(draftState.autosaveTimer);
  try {
    const draft = await draftApi(`/api/admin/drafts/${encodeURIComponent(draftId)}`);
    renderDraftEditor(draft);
    await loadDraftHistory();
    await loadDraftDiff();
    await loadDraftWorkspace();
  } catch (error) {
    showDraftMessage(error.message, true);
  }
}

async function savePayload(payload, options = {}) {
  const draft = draftState.currentDraft;
  if (!draft || draft.status !== "draft" || draftState.saving) return null;
  draftState.saving = true;
  setSaveState(options.autosave ? "Autosaving…" : "Saving…", "pending");
  try {
    const saved = await draftApi(`/api/admin/drafts/${encodeURIComponent(draft.draft_id)}`, {
      method: "PATCH",
      csrf: true,
      body: JSON.stringify({
        payload,
        expected_version: draft.version,
        note: options.note || null,
        autosave: Boolean(options.autosave),
      }),
    });
    renderDraftEditor(saved);
    setSaveState(saved.unchanged ? "No changes" : "Saved");
    await Promise.all([loadDraftHistory(), loadDraftDiff(), loadDraftWorkspace()]);
    return saved;
  } catch (error) {
    if (error.status === 409) {
      setSaveState("Newer version exists", "error");
      showDraftMessage("This draft changed after it was loaded. Reload it before saving so a newer revision is not overwritten.", true);
    } else {
      setSaveState("Save failed", "error");
      showDraftMessage(error.message, true);
    }
    return null;
  } finally {
    draftState.saving = false;
  }
}

function scheduleTitleAutosave() {
  clearTimeout(draftState.autosaveTimer);
  const draft = draftState.currentDraft;
  if (!draft || draft.status !== "draft") return;
  setSaveState("Unsaved change", "pending");
  draftState.autosaveTimer = setTimeout(async () => {
    const payload = structuredClone(draftState.currentDraft.payload || {});
    const title = el("draft-title-input").value.trim();
    if ("title" in payload || !("canonical_term" in payload)) payload.title = title;
    else payload.canonical_term = title;
    await savePayload(payload, { autosave: true, note: "Working title autosave" });
  }, 900);
}

async function saveAdvancedPayload() {
  const raw = el("draft-payload-editor").value;
  let payload;
  try {
    payload = JSON.parse(raw);
  } catch (error) {
    showDraftMessage(`Structured payload is not valid JSON. ${error.message}`, true);
    return;
  }
  if (!payload || Array.isArray(payload) || typeof payload !== "object") {
    showDraftMessage("Structured payload must be a JSON object.", true);
    return;
  }
  const saved = await savePayload(payload, { note: "Advanced structured payload save" });
  if (saved) showDraftMessage("Structured working copy saved as a new recoverable revision.");
}

function renderRevisions(payload) {
  const items = Array.isArray(payload?.items) ? payload.items : [];
  const target = el("draft-revisions");
  if (!items.length) {
    target.innerHTML = '<p class="empty-state compact">No revisions yet.</p>';
    return;
  }
  target.innerHTML = items
    .map(
      (item) => `
        <div class="history-row">
          <div>
            <strong>v${number(item.revision_number)} · ${escapeHtml(humanize(item.action))}</strong>
            <small>${escapeHtml(item.note || "No note")} · ${escapeHtml(formatTime(item.created_at))} · ${escapeHtml(item.created_by)}</small>
          </div>
          <button class="text-button restore-revision" type="button" data-revision-id="${item.revision_id}">Restore</button>
        </div>`
    )
    .join("");
  target.querySelectorAll(".restore-revision").forEach((button) => {
    button.addEventListener("click", () => restoreRevision(Number(button.dataset.revisionId)));
  });
}

function renderSnapshots(payload) {
  const items = Array.isArray(payload?.items) ? payload.items : [];
  const target = el("draft-snapshots");
  if (!items.length) {
    target.innerHTML = '<p class="empty-state compact">No named snapshots yet.</p>';
    return;
  }
  target.innerHTML = items
    .map(
      (item) => `
        <div class="history-row">
          <div>
            <strong>${escapeHtml(item.label)}</strong>
            <small>Draft v${number(item.draft_version)} · ${escapeHtml(formatTime(item.created_at))} · ${escapeHtml(item.created_by)}</small>
          </div>
          <button class="text-button restore-snapshot" type="button" data-snapshot-id="${item.snapshot_id}">Restore</button>
        </div>`
    )
    .join("");
  target.querySelectorAll(".restore-snapshot").forEach((button) => {
    button.addEventListener("click", () => restoreSnapshot(Number(button.dataset.snapshotId)));
  });
}

async function loadDraftHistory() {
  const draft = draftState.currentDraft;
  if (!draft) return;
  try {
    const [revisions, snapshots] = await Promise.all([
      draftApi(`/api/admin/drafts/${encodeURIComponent(draft.draft_id)}/revisions?limit=200`),
      draftApi(`/api/admin/drafts/${encodeURIComponent(draft.draft_id)}/snapshots?limit=200`),
    ]);
    renderRevisions(revisions);
    renderSnapshots(snapshots);
  } catch (error) {
    el("draft-revisions").innerHTML = `<p class="empty-state compact">${escapeHtml(error.message)}</p>`;
  }
}

function compactDiffValue(value) {
  const raw = typeof value === "string" ? value : JSON.stringify(value, null, 2);
  if (raw == null) return "∅";
  return raw.length > 900 ? `${raw.slice(0, 900)}…` : raw;
}

function renderDiff(payload) {
  const target = el("draft-diff");
  const changes = Array.isArray(payload?.changes) ? payload.changes : [];
  if (!changes.length) {
    target.innerHTML = '<p class="empty-state compact">The working copy currently matches its catalog base.</p>';
    return;
  }
  target.innerHTML = `
    <p class="muted">${number(payload.change_count)} changed fields${payload.truncated ? " · display truncated" : ""}</p>
    ${changes
      .slice(0, 120)
      .map(
        (change) => `
          <div class="diff-row">
            <code>${escapeHtml(change.path)} · ${escapeHtml(change.change)}</code>
            <div class="diff-values">
              <div class="diff-value"><strong>Before</strong>\n${escapeHtml(compactDiffValue(change.before))}</div>
              <div class="diff-value"><strong>Current</strong>\n${escapeHtml(compactDiffValue(change.after))}</div>
            </div>
          </div>`
      )
      .join("")}
  `;
}

async function loadDraftDiff() {
  const draft = draftState.currentDraft;
  if (!draft) return;
  try {
    const payload = await draftApi(`/api/admin/drafts/${encodeURIComponent(draft.draft_id)}/compare`);
    renderDiff(payload);
  } catch (error) {
    el("draft-diff").innerHTML = `<p class="empty-state compact">${escapeHtml(error.message)}</p>`;
  }
}

async function restoreRevision(revisionId) {
  const draft = draftState.currentDraft;
  if (!draft || draft.status !== "draft") return;
  if (!window.confirm("Restore this earlier revision as a new current revision? The existing history will remain intact.")) return;
  try {
    const restored = await draftApi(
      `/api/admin/drafts/${encodeURIComponent(draft.draft_id)}/revisions/${revisionId}/restore`,
      {
        method: "POST",
        csrf: true,
        body: JSON.stringify({ expected_version: draft.version }),
      }
    );
    renderDraftEditor(restored);
    await Promise.all([loadDraftHistory(), loadDraftDiff(), loadDraftWorkspace()]);
  } catch (error) {
    showDraftMessage(error.message, true);
  }
}

async function restoreSnapshot(snapshotId) {
  const draft = draftState.currentDraft;
  if (!draft || draft.status !== "draft") return;
  if (!window.confirm("Restore this snapshot as a new current revision? The existing history will remain intact.")) return;
  try {
    const restored = await draftApi(
      `/api/admin/drafts/${encodeURIComponent(draft.draft_id)}/snapshots/${snapshotId}/restore`,
      {
        method: "POST",
        csrf: true,
        body: JSON.stringify({ expected_version: draft.version }),
      }
    );
    renderDraftEditor(restored);
    await Promise.all([loadDraftHistory(), loadDraftDiff(), loadDraftWorkspace()]);
  } catch (error) {
    showDraftMessage(error.message, true);
  }
}

async function createSnapshot() {
  const draft = draftState.currentDraft;
  if (!draft) return;
  const suggested = `Snapshot before major edit · v${draft.version}`;
  const label = window.prompt("Name this recovery snapshot", suggested);
  if (!label?.trim()) return;
  try {
    await draftApi(`/api/admin/drafts/${encodeURIComponent(draft.draft_id)}/snapshots`, {
      method: "POST",
      csrf: true,
      body: JSON.stringify({ label: label.trim() }),
    });
    await Promise.all([loadDraftHistory(), loadDraftWorkspace()]);
  } catch (error) {
    showDraftMessage(error.message, true);
  }
}

async function toggleArchive() {
  const draft = draftState.currentDraft;
  if (!draft) return;
  const restoring = draft.status === "archived";
  if (!restoring && !window.confirm("Archive this working copy? Its full revision and snapshot history will remain recoverable.")) return;
  try {
    const endpoint = restoring ? "restore-archive" : "archive";
    const updated = await draftApi(`/api/admin/drafts/${encodeURIComponent(draft.draft_id)}/${endpoint}`, {
      method: "POST",
      csrf: true,
      body: JSON.stringify({ expected_version: draft.version }),
    });
    renderDraftEditor(updated);
    draftState.statusFilter = updated.status;
    document.querySelectorAll(".draft-filter").forEach((button) => {
      button.classList.toggle("active", button.dataset.draftStatus === draftState.statusFilter);
    });
    await Promise.all([loadDraftHistory(), loadDraftDiff(), loadDraftWorkspace()]);
  } catch (error) {
    showDraftMessage(error.message, true);
  }
}

el("create-draft-form")?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const entityId = el("draft-entity-id").value.trim();
  if (!entityId) return;
  try {
    const draft = await draftApi("/api/admin/drafts", {
      method: "POST",
      csrf: true,
      body: JSON.stringify({ entity_id: entityId }),
    });
    el("draft-entity-id").value = "";
    draftState.statusFilter = "draft";
    document.querySelectorAll(".draft-filter").forEach((button) => {
      button.classList.toggle("active", button.dataset.draftStatus === "draft");
    });
    renderDraftEditor(draft);
    await Promise.all([loadDraftHistory(), loadDraftDiff(), loadDraftWorkspace()]);
  } catch (error) {
    el("draft-list").insertAdjacentHTML("afterbegin", `<p class="draft-message error">${escapeHtml(error.message)}</p>`);
  }
});

el("draft-title-input")?.addEventListener("input", scheduleTitleAutosave);
el("save-draft-payload")?.addEventListener("click", saveAdvancedPayload);
el("refresh-drafts")?.addEventListener("click", loadDraftWorkspace);
el("refresh-revisions")?.addEventListener("click", loadDraftHistory);
el("refresh-diff")?.addEventListener("click", loadDraftDiff);
el("create-snapshot-button")?.addEventListener("click", createSnapshot);
el("draft-archive-button")?.addEventListener("click", toggleArchive);

document.querySelectorAll(".draft-filter").forEach((button) => {
  button.addEventListener("click", () => {
    draftState.statusFilter = button.dataset.draftStatus || "";
    document.querySelectorAll(".draft-filter").forEach((item) => item.classList.toggle("active", item === button));
    loadDraftWorkspace();
  });
});

document.querySelectorAll(".nav-item").forEach((button) => {
  button.addEventListener("click", () => {
    const name = button.dataset.view;
    if (name === "drafts" || name === "versions") {
      activateDraftView(name);
    } else {
      el("draft-view")?.classList.add("hidden");
    }
  });
});
