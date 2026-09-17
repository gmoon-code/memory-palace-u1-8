const publicationState = {
  mode: null,
  csrfToken: "",
  status: null,
  eligible: [],
  candidates: [],
  releases: [],
  selectedCandidateId: null,
  busy: false,
};

const publicationModes = new Set(["publishing", "versions"]);

function p(id) {
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

function number(value) {
  return new Intl.NumberFormat().format(Number(value) || 0);
}

function time(value) {
  if (!value) return "Unknown";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? String(value) : date.toLocaleString();
}

function setHeader(title, eyebrow, description) {
  p("view-title").textContent = title;
  p("view-eyebrow").textContent = eyebrow;
  p("view-description").textContent = description;
}

async function ensureCsrf() {
  if (publicationState.csrfToken) return publicationState.csrfToken;
  const response = await fetch("/api/admin/session", {
    credentials: "same-origin",
    cache: "no-store",
    headers: { Accept: "application/json" },
  });
  if (!response.ok) throw new Error("Admin session is unavailable");
  const session = await response.json();
  publicationState.csrfToken = session.csrf_token || "";
  return publicationState.csrfToken;
}

async function publicationApi(url, options = {}) {
  const headers = new Headers(options.headers || {});
  headers.set("Accept", "application/json");
  if (options.body && !headers.has("Content-Type")) headers.set("Content-Type", "application/json");
  if (options.csrf) headers.set("X-CSRF-Token", await ensureCsrf());
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

function ensurePublicationUi() {
  if (!document.querySelector('link[href="/admin/publication.css"]')) {
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "/admin/publication.css";
    document.head.appendChild(link);
  }
  const status = document.querySelector(".brand-block .status-pill");
  if (status) status.textContent = "Step 9 controlled publishing";

  if (!p("publication-view")) {
    const section = document.createElement("section");
    section.id = "publication-view";
    section.className = "view-panel hidden";
    section.setAttribute("aria-live", "polite");
    section.innerHTML = '<div id="publication-content"></div>';
    const placeholder = p("placeholder-view");
    if (placeholder) placeholder.insertAdjacentElement("beforebegin", section);
    else p("admin-main")?.appendChild(section);
  }

  document.querySelectorAll(".nav-item").forEach((button) => {
    if (button.dataset.publicationBound === "true") return;
    button.dataset.publicationBound = "true";
    button.addEventListener(
      "click",
      (event) => {
        const mode = button.dataset.view;
        if (publicationModes.has(mode)) {
          event.preventDefault();
          event.stopImmediatePropagation();
          activatePublication(mode);
        } else {
          p("publication-view")?.classList.add("hidden");
        }
      },
      true
    );
  });
}

function message(text, mode = "") {
  const node = p("publication-message");
  if (!node) return;
  node.textContent = text || "";
  node.className = `publication-message${mode ? ` ${mode}` : ""}${text ? "" : " hidden"}`;
}

function gateCard(label, value, enabled) {
  return `<article class="publication-gate ${enabled ? "ok" : "off"}"><span>${esc(label)}</span><strong>${esc(value)}</strong></article>`;
}

function renderStatus(status) {
  p("publication-gates").innerHTML = [
    gateCard("Candidate creation", status.publication_enabled ? "Enabled" : "Disabled", status.publication_enabled),
    gateCard("GitHub submission", status.github_enabled ? "Enabled" : "Disabled", status.github_enabled),
    gateCard("GitHub repository", status.github_repository || "Not active", Boolean(status.github_repository)),
    gateCard("Server-side merge", status.github_merge_enabled ? "Enabled" : "Manual PR merge", status.github_merge_enabled),
  ].join("");
  p("publication-safety-note").textContent = status.publication_enabled
    ? "Candidate creation writes only to isolated server-side release packages. Student content changes only after a validated GitHub candidate is merged and then verified."
    : "Controlled publication is disabled on this server. Drafting, preview, and quality checks remain available. Enable the Step 9 server gate only on a trusted deployment.";
}

function renderEligible(items) {
  const target = p("publication-eligible");
  if (!items.length) {
    target.innerHTML = '<p class="empty-state">No changed active working copies are currently eligible for a release candidate.</p>';
    return;
  }
  target.innerHTML = items
    .map((item) => {
      const quality = item.quality || {};
      const blocked = !item.publication_supported || Number(quality.errors || 0) > 0;
      return `
        <label class="eligible-row ${blocked ? "blocked" : ""}">
          <input class="candidate-draft-check" type="checkbox" value="${esc(item.draft_id)}" ${blocked ? "disabled" : ""}/>
          <span class="eligible-copy">
            <strong>${esc(item.title || item.entity_id)}</strong>
            <small>${esc(item.unit_id || "course-wide")} · ${esc(humanize(item.entity_type))} · draft v${number(item.version)}</small>
            <small>${esc(item.entity_id)}</small>
            <span class="eligible-quality">
              <span class="quality-chip ${quality.errors ? "error" : "ok"}">${number(quality.errors)} errors</span>
              <span class="quality-chip ${quality.warnings ? "warning" : "ok"}">${number(quality.warnings)} warnings</span>
              ${!item.publication_supported ? `<span class="quality-chip error">${esc(item.publication_note)}</span>` : ""}
            </span>
          </span>
        </label>`;
    })
    .join("");
}

function statusChip(status) {
  return `<span class="publication-status-chip ${esc(status)}">${esc(humanize(status))}</span>`;
}

function renderCandidates(items) {
  const target = p("publication-candidates");
  if (!items.length) {
    target.innerHTML = '<p class="empty-state">No release candidates have been created.</p>';
    return;
  }
  target.innerHTML = items
    .map(
      (item) => `
        <button class="candidate-row ${publicationState.selectedCandidateId === item.candidate_id ? "active" : ""}" type="button" data-candidate-id="${esc(item.candidate_id)}">
          <span class="candidate-row-top"><strong>${esc(item.title)}</strong>${statusChip(item.status)}</span>
          <small class="publication-meta">${esc(item.kind)} · ${number(item.manifest?.files?.length)} files · ${esc(time(item.updated_at))}</small>
        </button>`
    )
    .join("");
  target.querySelectorAll("[data-candidate-id]").forEach((button) => {
    button.addEventListener("click", () => selectCandidate(button.dataset.candidateId));
  });
}

function renderReleases(items) {
  const target = p("publication-releases");
  if (!items.length) {
    target.innerHTML = '<p class="empty-state">No verified Content Studio releases are recorded yet.</p>';
    return;
  }
  target.innerHTML = items
    .map(
      (item) => `
        <article class="release-row">
          <span class="release-row-top"><strong>${esc(item.title)}</strong><span class="publication-status-chip released">Released</span></span>
          <small class="publication-meta">${esc(item.release_id)} · ${esc(time(item.created_at))}</small>
          <small class="publication-meta">${number(item.summary?.files?.length)} changed files · candidate ${esc(item.candidate_id)}</small>
          <div class="publication-actions"><button class="button secondary rollback-release" type="button" data-release-id="${esc(item.release_id)}">Prepare rollback candidate</button></div>
        </article>`
    )
    .join("");
  target.querySelectorAll(".rollback-release").forEach((button) => {
    button.addEventListener("click", () => rollbackRelease(button.dataset.releaseId));
  });
}

function actionButtons(candidate) {
  const status = candidate.status;
  const github = publicationState.status || {};
  const buttons = [];
  if (["created", "failed", "validated"].includes(status)) {
    buttons.push('<button class="button primary" id="candidate-validate" type="button">Run release validation</button>');
  }
  if (status === "validated") {
    buttons.push(`<button class="button primary" id="candidate-submit" type="button" ${github.github_enabled ? "" : "disabled"}>Submit GitHub candidate</button>`);
  }
  if (["submitted", "merge_ready"].includes(status)) {
    buttons.push('<button class="button secondary" id="candidate-checks" type="button">Refresh GitHub Actions</button>');
    if (github.github_merge_enabled) {
      buttons.push(`<button class="button primary" id="candidate-merge" type="button" ${status === "merge_ready" ? "" : "disabled"}>Merge validated candidate</button>`);
    }
    buttons.push('<button class="button secondary" id="candidate-verify" type="button">Verify release on main</button>');
  }
  if (status === "merged_pending_verify") {
    buttons.push('<button class="button primary" id="candidate-verify" type="button">Verify merged release</button>');
  }
  return buttons.join("");
}

async function renderCandidateDetail(candidate) {
  const target = p("publication-detail");
  const manifest = candidate.manifest || {};
  let summaryText = "";
  try {
    const response = await fetch(`/api/admin/publication/candidates/${encodeURIComponent(candidate.candidate_id)}/summary`, {
      credentials: "same-origin",
      cache: "no-store",
    });
    if (response.ok) summaryText = await response.text();
  } catch {
    summaryText = "";
  }
  target.innerHTML = `
    <div class="publication-detail">
      <div class="publication-detail-heading">
        <div><p class="eyebrow">Release candidate</p><h2>${esc(candidate.title)}</h2><p class="publication-meta">${esc(candidate.candidate_id)} · ${esc(time(candidate.created_at))}</p></div>
        ${statusChip(candidate.status)}
      </div>
      <div class="publication-summary-grid">
        <article class="publication-stat"><span>Working copies</span><strong>${number(manifest.drafts?.length)}</strong></article>
        <article class="publication-stat"><span>Changed files</span><strong>${number(manifest.files?.length)}</strong></article>
        <article class="publication-stat"><span>Warnings</span><strong>${number(manifest.warning_count)}</strong></article>
        <article class="publication-stat"><span>Local QA</span><strong>${candidate.validation?.passed ? "Passed" : candidate.validation ? "Failed" : "Not run"}</strong></article>
      </div>
      <div class="publication-actions">${actionButtons(candidate)}</div>
      <section class="publication-detail-section"><h3>Working copies and dependency impact</h3><div class="publication-draft-list">${(manifest.drafts || []).map((item) => `<div class="publication-draft-row"><strong>${esc(item.title || item.entity_id)}</strong><code>${esc(item.entity_id)}</code><small class="publication-meta">draft v${number(item.version)} · ${number(item.quality?.warning_count)} warnings · dependencies ${esc(JSON.stringify(item.dependency_counts || {}))}</small></div>`).join("") || '<p class="empty-state compact">Rollback candidates use immutable release files and contain no active working copies.</p>'}</div></section>
      <section class="publication-detail-section"><h3>Exact file changes</h3><div class="publication-file-list">${(manifest.files || []).map((item) => `<div class="publication-file-row"><strong>${esc(item.path)}</strong><span class="publication-hash">${esc(item.before_sha256?.slice(0, 16))} → ${esc(item.after_sha256?.slice(0, 16))}</span></div>`).join("")}</div></section>
      ${candidate.validation ? `<section class="publication-detail-section"><h3>Local release gate</h3><div class="publication-check-list">${(candidate.validation.commands || []).map((item) => `<div class="publication-check-row"><strong>${esc(item.command)}</strong><small class="publication-meta">exit ${number(item.returncode)}</small></div>`).join("")}</div></section>` : ""}
      ${candidate.github?.pr_number ? `<section class="publication-detail-section"><h3>GitHub publication</h3><p class="publication-meta">Branch ${esc(candidate.github.branch)} · PR #${number(candidate.github.pr_number)} · commit ${esc(candidate.github.commit_sha || "")}</p></section>` : ""}
      ${summaryText ? `<details class="publication-detail-section"><summary>Release summary</summary><pre class="publication-release-summary">${esc(summaryText)}</pre></details>` : ""}
    </div>`;
  p("candidate-validate")?.addEventListener("click", () => candidateAction(candidate.candidate_id, "validate", "Running isolated release validation. This may take a few minutes…"));
  p("candidate-submit")?.addEventListener("click", () => candidateAction(candidate.candidate_id, "submit", "Creating a GitHub candidate branch and pull request…"));
  p("candidate-checks")?.addEventListener("click", () => candidateAction(candidate.candidate_id, "checks", "Refreshing GitHub Actions status…"));
  p("candidate-merge")?.addEventListener("click", () => {
    if (window.confirm("Merge this validated GitHub candidate into the configured publication branch?")) candidateAction(candidate.candidate_id, "merge", "Merging validated GitHub candidate…");
  });
  p("candidate-verify")?.addEventListener("click", () => candidateAction(candidate.candidate_id, "verify", "Verifying the exact candidate hashes on the publication branch…"));
}

async function selectCandidate(candidateId) {
  publicationState.selectedCandidateId = candidateId;
  renderCandidates(publicationState.candidates);
  p("publication-detail").innerHTML = '<p class="empty-state">Loading candidate…</p>';
  try {
    const candidate = await publicationApi(`/api/admin/publication/candidates/${encodeURIComponent(candidateId)}`);
    await renderCandidateDetail(candidate);
  } catch (error) {
    p("publication-detail").innerHTML = `<p class="publication-message error">${esc(error.message)}</p>`;
  }
}

async function candidateAction(candidateId, action, pendingMessage) {
  if (publicationState.busy) return;
  publicationState.busy = true;
  message(pendingMessage, "pending");
  try {
    const result = await publicationApi(`/api/admin/publication/candidates/${encodeURIComponent(candidateId)}/${action}`, {
      method: "POST",
      csrf: true,
    });
    message(`${humanize(action)} completed. Candidate status is ${humanize(result.status || "released")}.`, "success");
    await loadPublicationData();
    if (publicationState.candidates.some((item) => item.candidate_id === candidateId)) await selectCandidate(candidateId);
  } catch (error) {
    message(error.message, "error");
  } finally {
    publicationState.busy = false;
  }
}

async function rollbackRelease(releaseId) {
  if (publicationState.busy) return;
  if (!window.confirm("Prepare a rollback candidate from this verified release? No published file changes occur until the rollback candidate passes the same validation and GitHub process.")) return;
  publicationState.busy = true;
  message("Preparing a non-destructive rollback candidate…", "pending");
  try {
    const candidate = await publicationApi(`/api/admin/publication/releases/${encodeURIComponent(releaseId)}/rollback`, {
      method: "POST",
      csrf: true,
      body: JSON.stringify({ title: null }),
    });
    message("Rollback candidate created. Validate it before any GitHub submission.", "success");
    await loadPublicationData();
    await selectCandidate(candidate.candidate_id);
  } catch (error) {
    message(error.message, "error");
  } finally {
    publicationState.busy = false;
  }
}

async function createCandidate(event) {
  event.preventDefault();
  if (publicationState.busy) return;
  const draftIds = [...document.querySelectorAll(".candidate-draft-check:checked")].map((input) => input.value);
  if (!draftIds.length) {
    message("Select at least one supported changed working copy.", "error");
    return;
  }
  const title = p("candidate-title").value.trim();
  const notes = p("candidate-notes").value.trim();
  const warningsAcknowledged = p("candidate-warning-ack").checked;
  publicationState.busy = true;
  message("Creating an isolated candidate package and pre-publication recovery snapshots…", "pending");
  try {
    const candidate = await publicationApi("/api/admin/publication/candidates", {
      method: "POST",
      csrf: true,
      body: JSON.stringify({ draft_ids: draftIds, title, notes, warnings_acknowledged: warningsAcknowledged }),
    });
    message("Candidate created. Published course files are still unchanged.", "success");
    p("candidate-title").value = "";
    p("candidate-notes").value = "";
    p("candidate-warning-ack").checked = false;
    await loadPublicationData();
    await selectCandidate(candidate.candidate_id);
  } catch (error) {
    message(error.message, "error");
  } finally {
    publicationState.busy = false;
  }
}

function workspaceMarkup(mode) {
  const releaseOnly = mode === "versions";
  return `
    <div class="publication-shell">
      <section class="panel">
        <div class="panel-heading"><div><p class="eyebrow">Publication boundary</p><h2>Release controls</h2></div><button id="publication-refresh" class="button secondary" type="button">Refresh</button></div>
        <div id="publication-gates" class="publication-gate-grid"></div>
        <p id="publication-safety-note" class="publication-note"></p>
        <div id="publication-message" class="publication-message hidden" role="status" aria-live="polite"></div>
      </section>
      ${releaseOnly ? "" : `
      <div class="publication-grid">
        <section class="panel">
          <div class="panel-heading"><div><p class="eyebrow">Changed working copies</p><h2>Build a candidate</h2></div></div>
          <form id="candidate-form" class="publication-form">
            <div id="publication-eligible" class="eligible-list"><p class="empty-state">Loading changed drafts…</p></div>
            <label for="candidate-title">Release title</label>
            <input id="candidate-title" type="text" maxlength="300" required placeholder="Example  Unit 8 narrative revisions"/>
            <label for="candidate-notes">Release notes</label>
            <textarea id="candidate-notes" rows="5" maxlength="12000" placeholder="Describe the teacher-approved changes in this candidate."></textarea>
            <label class="publication-warning-ack"><input id="candidate-warning-ack" type="checkbox"/><span>I reviewed any teacher-review warnings for the selected working copies and accept them for this candidate. Blocking errors can never be acknowledged away.</span></label>
            <button class="button primary" type="submit">Create isolated candidate</button>
          </form>
        </section>
        <section class="panel">
          <div class="panel-heading"><div><p class="eyebrow">Validation and GitHub delivery</p><h2>Candidate inspector</h2></div></div>
          <div id="publication-detail"><p class="empty-state">Select a release candidate to inspect exact files, dependencies, validation, and GitHub status.</p></div>
        </section>
      </div>`}
      <div class="publication-grid">
        <section class="panel">
          <div class="panel-heading"><div><p class="eyebrow">Immutable packages</p><h2>Release candidates</h2></div></div>
          <div id="publication-candidates" class="candidate-list"></div>
        </section>
        <section class="panel">
          <div class="panel-heading"><div><p class="eyebrow">Verified publication history</p><h2>Releases and rollback</h2></div></div>
          <div id="publication-releases" class="release-list"></div>
          ${releaseOnly ? '<div id="publication-detail" class="top-gap"><p class="empty-state">Select a candidate from Publishing to inspect its full release package.</p></div>' : ""}
        </section>
      </div>
    </div>`;
}

async function loadPublicationData() {
  try {
    const status = await publicationApi("/api/admin/publication/status");
    publicationState.status = status;
    renderStatus(status);
    const eligiblePromise = publicationState.mode === "publishing" ? publicationApi("/api/admin/publication/eligible") : Promise.resolve({ items: [] });
    if (!status.publication_enabled) {
      publicationState.eligible = (await eligiblePromise).items || [];
      publicationState.candidates = [];
      publicationState.releases = [];
      if (p("publication-eligible")) renderEligible(publicationState.eligible);
      if (p("publication-candidates")) p("publication-candidates").innerHTML = '<p class="empty-state">Enable the trusted-server publication gate to create and retain release candidates.</p>';
      if (p("publication-releases")) p("publication-releases").innerHTML = '<p class="empty-state">Publication history is unavailable while the server gate is disabled.</p>';
      return;
    }
    const [eligible, candidates, releases] = await Promise.all([
      eligiblePromise,
      publicationApi("/api/admin/publication/candidates?limit=200"),
      publicationApi("/api/admin/publication/releases?limit=200"),
    ]);
    publicationState.eligible = eligible.items || [];
    publicationState.candidates = candidates.items || [];
    publicationState.releases = releases.items || [];
    if (p("publication-eligible")) renderEligible(publicationState.eligible);
    renderCandidates(publicationState.candidates);
    renderReleases(publicationState.releases);
  } catch (error) {
    message(error.message, "error");
  }
}

async function activatePublication(mode) {
  publicationState.mode = mode;
  document.querySelectorAll(".view-panel").forEach((panel) => panel.classList.add("hidden"));
  p("publication-view")?.classList.remove("hidden");
  document.querySelector(".global-search")?.classList.add("hidden");
  document.querySelectorAll(".nav-item").forEach((button) => button.classList.toggle("active", button.dataset.view === mode));
  if (mode === "versions") {
    setHeader(
      "Version History",
      "Verified releases and recovery",
      "Review immutable Content Studio release records and prepare rollback candidates that pass through the same validation and GitHub controls as forward releases."
    );
  } else {
    setHeader(
      "Publishing",
      "Controlled release workflow",
      "Turn approved working copies into isolated candidates, validate them, review exact file and dependency changes, deliver them through GitHub, and verify the published hashes before a release is recorded."
    );
  }
  p("publication-content").innerHTML = workspaceMarkup(mode);
  p("publication-refresh")?.addEventListener("click", loadPublicationData);
  p("candidate-form")?.addEventListener("submit", createCandidate);
  await loadPublicationData();
}

ensurePublicationUi();
