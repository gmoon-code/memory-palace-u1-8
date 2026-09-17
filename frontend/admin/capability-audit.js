const capabilityState = {
  report: null,
  loading: false,
};

function c(id) {
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

async function capabilityApi(url) {
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

function ensureStyles() {
  if (document.querySelector('link[href="/admin/capability-audit.css"]')) return;
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = "/admin/capability-audit.css";
  document.head.appendChild(link);
}

function ensureNavigation() {
  const nav = document.querySelector(".admin-nav");
  if (!nav) return;

  const stories = nav.querySelector('[data-view="stories"]');
  if (stories && !nav.querySelector('[data-view="characters"]')) {
    const characters = document.createElement("button");
    characters.className = "nav-item";
    characters.dataset.view = "characters";
    characters.type = "button";
    characters.textContent = "Characters";
    stories.insertAdjacentElement("afterend", characters);
  }
  const characters = nav.querySelector('[data-view="characters"]');
  if (characters && !nav.querySelector('[data-view="locations"]')) {
    const locations = document.createElement("button");
    locations.className = "nav-item";
    locations.dataset.view = "locations";
    locations.type = "button";
    locations.textContent = "Locations";
    characters.insertAdjacentElement("afterend", locations);
  }

  if (!nav.querySelector('[data-view="capability-audit"]')) {
    const audit = document.createElement("button");
    audit.className = "nav-item";
    audit.dataset.view = "capability-audit";
    audit.type = "button";
    audit.textContent = "Admin Capability Audit";
    const settings = nav.querySelector('[data-view="settings"]');
    if (settings) settings.insertAdjacentElement("beforebegin", audit);
    else nav.appendChild(audit);
  }
}

function normalizeVisibleCopy() {
  const status = document.querySelector(".brand-block .status-pill");
  if (status) status.textContent = "Integrated administrator workspace";

  document.querySelectorAll(".capability-panel").forEach((panel) => {
    const heading = panel.querySelector("h2");
    const eyebrow = panel.querySelector(".eyebrow");
    if (heading?.textContent?.trim() === "Capability map") {
      heading.textContent = "Administrator capabilities";
      if (eyebrow) eyebrow.textContent = "Current workspace";
    }
  });

  const emptyDraft = c("draft-empty-state");
  if (emptyDraft) {
    const copy = emptyDraft.querySelector("p:last-child");
    if (copy) copy.textContent = "Select or create a protected working copy. Changes remain separate from published AP Biology content and retain revision and snapshot history.";
  }
  const help = document.querySelector("#draft-editor .field-help");
  if (help) help.textContent = "Title changes autosave to the protected working copy. Field-specific editors are available from the corresponding Content Studio workspaces.";
}

function ensureView() {
  if (c("capability-audit-view")) return;
  const section = document.createElement("section");
  section.id = "capability-audit-view";
  section.className = "view-panel hidden";
  section.setAttribute("aria-live", "polite");
  section.innerHTML = `
    <div id="capability-summary" class="capability-audit-summary"></div>
    <div class="capability-audit-layout">
      <section class="panel">
        <div class="panel-heading">
          <div>
            <p class="eyebrow">Whole administrator surface</p>
            <h2>Workspace capability audit</h2>
          </div>
          <button id="refresh-capability-audit" class="button secondary" type="button">Refresh audit</button>
        </div>
        <p class="panel-copy">This audit checks the administrator workspaces against the implementation files that provide their editing, draft, preview, quality, publication, security, and local-maintenance behavior.</p>
        <div id="capability-audit-message" class="capability-audit-message" role="status"></div>
        <div id="capability-workspaces" class="capability-workspaces"></div>
      </section>

      <aside class="panel capability-workflow-panel">
        <div>
          <p class="eyebrow">Integrated work route</p>
          <h2>Browse to recovery</h2>
        </div>
        <div id="capability-workflow" class="capability-workflow"></div>
        <div class="capability-boundary">
          <strong>Safety boundary</strong>
          <p>The audit is read-only. It never writes AP Biology source files or student-facing content.</p>
        </div>
      </aside>
    </div>
    <section class="panel capability-limits-panel">
      <div class="panel-heading">
        <div>
          <p class="eyebrow">Explicit boundaries</p>
          <h2>Intentional limits and deferred extensions</h2>
        </div>
      </div>
      <div id="capability-limits" class="capability-limits"></div>
    </section>
  `;
  const placeholder = c("placeholder-view");
  placeholder?.parentNode?.insertBefore(section, placeholder);
  c("refresh-capability-audit")?.addEventListener("click", () => loadAudit(true));
}

function summaryCard(label, value, note, className = "") {
  return `<article class="capability-summary-card ${esc(className)}"><span>${esc(label)}</span><strong>${esc(value)}</strong><small>${esc(note)}</small></article>`;
}

function renderAudit(report) {
  const summary = report?.summary || {};
  c("capability-summary").innerHTML = [
    summaryCard("Administrator workspaces", summary.workspace_count || 0, "audited navigation areas"),
    summaryCard("Implemented", summary.implemented || 0, "implementation evidence present", summary.incomplete ? "attention" : "ok"),
    summaryCard("Incomplete", summary.incomplete || 0, "missing implementation evidence", summary.incomplete ? "blocked" : "ok"),
    summaryCard("Workflow stages", summary.workflow_steps || 0, "browse through recovery"),
    summaryCard("Cost boundary", report?.zero_cost_boundary ? "$0" : "Review", report?.zero_cost_boundary ? "local operating model preserved" : "cost review required", report?.zero_cost_boundary ? "ok" : "blocked"),
  ].join("");

  const workspaces = Array.isArray(report?.workspaces) ? report.workspaces : [];
  c("capability-workspaces").innerHTML = workspaces.map((item) => `
    <article class="capability-workspace-row ${esc(item.status)}">
      <div class="capability-workspace-status">${item.status === "implemented" ? "✓" : "!"}</div>
      <div class="capability-workspace-copy">
        <div class="capability-workspace-heading">
          <strong>${esc(item.label)}</strong>
          <span>${esc(humanize(item.status))}</span>
        </div>
        <p>${esc(item.purpose)}</p>
        <small>${(item.capabilities || []).map(esc).join(" · ")}</small>
        ${(item.missing_evidence || []).length ? `<div class="capability-missing">Missing ${item.missing_evidence.map(esc).join(", ")}</div>` : ""}
      </div>
      <button class="text-button" type="button" data-capability-open="${esc(item.id)}">Open</button>
    </article>`).join("");

  c("capability-workspaces").querySelectorAll("[data-capability-open]").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelector(`.nav-item[data-view="${CSS.escape(button.dataset.capabilityOpen)}"]`)?.click();
    });
  });

  const workflow = Array.isArray(report?.workflow) ? report.workflow : [];
  c("capability-workflow").innerHTML = workflow.map((item) => `
    <button class="capability-workflow-step" type="button" data-workflow-open="${esc(item.view)}">
      <span>${esc(item.step)}</span>
      <div><strong>${esc(item.label)}</strong><small>${esc(item.detail)}</small></div>
    </button>`).join("");
  c("capability-workflow").querySelectorAll("[data-workflow-open]").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelector(`.nav-item[data-view="${CSS.escape(button.dataset.workflowOpen)}"]`)?.click();
    });
  });

  const limits = Array.isArray(report?.intentional_limits) ? report.intentional_limits : [];
  c("capability-limits").innerHTML = limits.map((item) => `
    <article class="capability-limit ${esc(item.status)}">
      <span>${esc(humanize(item.status))}</span>
      <div><strong>${esc(item.title)}</strong><p>${esc(item.detail)}</p></div>
    </article>`).join("");

  const message = c("capability-audit-message");
  if (message) {
    message.textContent = summary.incomplete
      ? `${summary.incomplete} administrator workspace${summary.incomplete === 1 ? "" : "s"} need implementation attention.`
      : "All audited administrator workspaces have their required implementation evidence present.";
    message.className = `capability-audit-message ${summary.incomplete ? "attention" : "ok"}`;
  }
}

async function loadAudit(force = false) {
  if (capabilityState.loading) return;
  if (capabilityState.report && !force) {
    renderAudit(capabilityState.report);
    return;
  }
  capabilityState.loading = true;
  const message = c("capability-audit-message");
  if (message) message.textContent = "Auditing administrator workspaces…";
  try {
    capabilityState.report = await capabilityApi("/api/admin/capabilities");
    renderAudit(capabilityState.report);
  } catch (error) {
    if (message) {
      message.textContent = error.status === 401 ? "Your administrator session expired. Sign in again." : error.message;
      message.className = "capability-audit-message blocked";
    }
  } finally {
    capabilityState.loading = false;
  }
}

function activateAudit() {
  document.querySelectorAll(".view-panel").forEach((panel) => panel.classList.add("hidden"));
  c("capability-audit-view")?.classList.remove("hidden");
  document.querySelectorAll(".nav-item").forEach((button) => button.classList.toggle("active", button.dataset.view === "capability-audit"));
  if (c("view-title")) c("view-title").textContent = "Admin Capability Audit";
  if (c("view-eyebrow")) c("view-eyebrow").textContent = "Whole-system administration";
  if (c("view-description")) c("view-description").textContent = "Verify that every Content Studio administrator workspace has a real implementation path and review the complete browse-to-recovery workflow.";
  loadAudit();
}

function wireNavigation() {
  document.querySelectorAll(".nav-item").forEach((button) => {
    if (button.dataset.capabilityBound === "true") return;
    button.dataset.capabilityBound = "true";
    button.addEventListener("click", (event) => {
      if (button.dataset.view === "capability-audit") {
        event.preventDefault();
        event.stopImmediatePropagation();
        activateAudit();
      } else {
        c("capability-audit-view")?.classList.add("hidden");
      }
    }, true);
  });
}

ensureStyles();
ensureNavigation();
ensureView();
normalizeVisibleCopy();
wireNavigation();
