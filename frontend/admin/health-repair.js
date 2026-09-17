const healthState = {
  report: null,
  csrfToken: "",
  loading: false,
};

function h(id) {
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

async function request(url, options = {}) {
  const headers = new Headers(options.headers || {});
  headers.set("Accept", "application/json");
  if (options.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  if (options.csrf) {
    if (!healthState.csrfToken) {
      const session = await request("/api/admin/session");
      healthState.csrfToken = session.csrf_token || "";
    }
    headers.set("X-CSRF-Token", healthState.csrfToken);
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

function ensureStyles() {
  if (document.querySelector('link[href="/admin/health-repair.css"]')) return;
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = "/admin/health-repair.css";
  document.head.appendChild(link);
}

function ensureView() {
  if (h("system-health-view")) return;
  const section = document.createElement("section");
  section.id = "system-health-view";
  section.className = "view-panel hidden";
  section.setAttribute("aria-live", "polite");
  section.innerHTML = `
    <div class="system-health-summary" id="system-health-summary"></div>

    <div class="health-repair-layout">
      <section class="panel">
        <div class="panel-heading">
          <div>
            <p class="eyebrow">Local operating environment</p>
            <h2>System Health Check</h2>
          </div>
          <div class="health-repair-actions">
            <button id="system-health-refresh" class="button secondary" type="button">Run health check</button>
            <button id="system-health-repair-all" class="button primary" type="button">Run safe repairs</button>
          </div>
        </div>
        <p class="panel-copy">Checks the private Content Studio databases, local storage, owner authentication configuration, publication locks, local backup, Python environment, Git checkout, updater readiness, and zero-cost boundary. The health check itself does not modify curriculum content.</p>
        <div id="system-health-message" class="system-health-message" role="status"></div>
        <div id="system-health-checks" class="system-health-checks"></div>
      </section>

      <aside class="panel health-repair-side">
        <div>
          <p class="eyebrow">Repair boundary</p>
          <h2>Safe maintenance only</h2>
        </div>
        <p>In-app repairs are limited to private directory creation, SQLite maintenance, stale temporary-file cleanup, and a local backup. Drafts, revisions, snapshots, staged media, credentials, AP Biology source content, and student content are never deleted by these actions.</p>
        <div class="health-boundary-card">
          <strong>Environment repair</strong>
          <p>If the private Python environment is missing or stale, close Content Studio and double-click <code>Repair Content Studio.cmd</code>. It creates a safety backup before touching the local environment and keeps the publication locks off.</p>
        </div>
        <div class="health-boundary-card">
          <strong>$0 operating rule</strong>
          <p>This local mode uses your own computer, local SQLite files, free Python packages, and GitHub repository files. Paid hosting, paid APIs, cloud databases, and billing accounts are outside this workflow.</p>
        </div>
      </aside>
    </div>
  `;
  const placeholder = h("placeholder-view");
  placeholder?.parentNode?.insertBefore(section, placeholder);

  h("system-health-refresh")?.addEventListener("click", () => loadReport(true));
  h("system-health-repair-all")?.addEventListener("click", () => runRepair("repair_all"));
}

function ensureSecurityShortcut() {
  const security = h("security-view");
  if (!security || h("security-system-health-shortcut")) return;
  const panel = document.createElement("section");
  panel.id = "security-system-health-shortcut";
  panel.className = "panel health-security-shortcut";
  panel.innerHTML = `
    <div>
      <p class="eyebrow">Local system protection</p>
      <h2>Content Studio health</h2>
      <p class="panel-copy">Check local databases, storage, backups, publication locks, Python environment, and updater readiness.</p>
    </div>
    <button class="button secondary" type="button">Open system health</button>
  `;
  panel.querySelector("button")?.addEventListener("click", () => {
    document.querySelector('.nav-item[data-view="settings"]')?.click();
  });
  security.insertBefore(panel, security.firstChild);
}

function summaryCard(label, value, note, className = "") {
  return `
    <article class="system-health-card ${esc(className)}">
      <span>${esc(label)}</span>
      <strong>${esc(value)}</strong>
      <small>${esc(note)}</small>
    </article>`;
}

function renderSummary(report) {
  const summary = report?.summary || {};
  const target = h("system-health-summary");
  if (!target) return;
  target.innerHTML = [
    summaryCard("Overall", humanize(report?.overall || "unknown"), `${summary.total || 0} checks`, report?.overall || ""),
    summaryCard("Healthy", summary.ok || 0, "checks passing", "healthy"),
    summaryCard("Warnings", summary.warning || 0, "need review", summary.warning ? "attention" : "healthy"),
    summaryCard("Errors", summary.error || 0, "blocking local safety issues", summary.error ? "blocked" : "healthy"),
    summaryCard("Zero-cost local mode", report?.zero_cost_local_mode ? "Locked" : "Needs attention", report?.zero_cost_local_mode ? "$0 boundary active" : "review required", report?.zero_cost_local_mode ? "healthy" : "blocked"),
  ].join("");
}

function renderChecks(report) {
  const target = h("system-health-checks");
  if (!target) return;
  const checks = Array.isArray(report?.checks) ? report.checks : [];
  if (!checks.length) {
    target.innerHTML = '<p class="empty-state">No system-health checks were returned.</p>';
    return;
  }
  target.innerHTML = checks
    .map((item) => {
      const repair = item.repairable && item.repair_action
        ? `<button class="button secondary compact-button" type="button" data-health-repair="${esc(item.repair_action)}">Repair safely</button>`
        : item.external_repair
          ? `<span class="health-external-repair">Close Content Studio and use ${esc(item.external_repair)}</span>`
          : "";
      return `
        <article class="system-health-row ${esc(item.status)}">
          <div class="system-health-icon" aria-hidden="true">${item.status === "ok" ? "✓" : item.status === "error" ? "!" : "•"}</div>
          <div class="system-health-copy">
            <div class="system-health-row-heading">
              <span>${esc(humanize(item.category))}</span>
              <strong>${esc(item.title)}</strong>
            </div>
            <p>${esc(item.message)}</p>
          </div>
          <div class="system-health-row-action">${repair}</div>
        </article>`;
    })
    .join("");
  target.querySelectorAll("[data-health-repair]").forEach((button) => {
    button.addEventListener("click", () => runRepair(button.dataset.healthRepair));
  });
}

async function loadReport(force = false) {
  if (healthState.loading) return;
  if (healthState.report && !force) {
    renderSummary(healthState.report);
    renderChecks(healthState.report);
    return;
  }
  healthState.loading = true;
  const message = h("system-health-message");
  if (message) message.textContent = "Running local Content Studio health checks…";
  try {
    const report = await request("/api/admin/system-health");
    healthState.report = report;
    renderSummary(report);
    renderChecks(report);
    if (message) {
      message.textContent = report.overall === "healthy"
        ? "All local system-health checks passed."
        : report.overall === "blocked"
          ? "One or more local safety checks need attention before administrative work continues."
          : "The local environment is usable, with warnings that should be reviewed.";
      message.className = `system-health-message ${report.overall}`;
    }
  } catch (error) {
    if (message) {
      message.textContent = error.status === 401 ? "Your admin session expired. Sign in again." : error.message;
      message.className = "system-health-message blocked";
    }
  } finally {
    healthState.loading = false;
  }
}

async function runRepair(action) {
  if (!action) return;
  const message = h("system-health-message");
  if (message) {
    message.textContent = `Running ${humanize(action)}…`;
    message.className = "system-health-message attention";
  }
  try {
    const result = await request("/api/admin/system-health/repair", {
      method: "POST",
      csrf: true,
      body: JSON.stringify({ action }),
    });
    healthState.report = result.report;
    renderSummary(result.report);
    renderChecks(result.report);
    if (message) {
      message.textContent = `${humanize(action)} completed. Health checks were refreshed.`;
      message.className = "system-health-message healthy";
    }
  } catch (error) {
    if (message) {
      message.textContent = error.message;
      message.className = "system-health-message blocked";
    }
  }
}

function showSettingsHealth() {
  ensureView();
  document.querySelectorAll(".view-panel").forEach((panel) => panel.classList.add("hidden"));
  h("system-health-view")?.classList.remove("hidden");
  const title = h("view-title");
  const eyebrow = h("view-eyebrow");
  const description = h("view-description");
  if (title) title.textContent = "Settings";
  if (eyebrow) eyebrow.textContent = "Local administration";
  if (description) description.textContent = "Verify the zero-cost local Content Studio environment and run only bounded, recoverable maintenance actions.";
  loadReport();
}

function wireNavigation() {
  document.querySelectorAll(".nav-item").forEach((button) => {
    button.addEventListener("click", () => {
      if (button.dataset.view === "settings") {
        showSettingsHealth();
      } else {
        h("system-health-view")?.classList.add("hidden");
      }
    });
  });
}

ensureStyles();
ensureView();
ensureSecurityShortcut();
wireNavigation();

const brandStatus = document.querySelector(".brand-block .status-pill");
if (brandStatus) brandStatus.textContent = "Integrated local admin workspace";
