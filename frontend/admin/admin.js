const state = {
  csrfToken: "",
  session: null,
  courseLoaded: false,
};

const views = {
  dashboard: {
    title: "Dashboard",
    eyebrow: "Content overview",
    description: "A protected read-only inventory of the current eight-unit AP Biology release.",
  },
  "course-map": {
    title: "Course Map",
    eyebrow: "Structure",
    description: "A visual Unit → Journey → Scene map will live here, with ordering, status, coverage, and dependency indicators.",
  },
  units: {
    title: "Units",
    eyebrow: "Course structure",
    description: "Unit-level metadata, coverage, introductions, images, ordering, prerequisites, and release status will be managed here.",
  },
  journeys: {
    title: "Journeys",
    eyebrow: "Narrative structure",
    description: "Journey routes, scene order, locations, coverage, retrieval points, and journey-level replacement tools will be managed here.",
  },
  scenes: {
    title: "Scenes",
    eyebrow: "Scene workspace",
    description: "Scene text, spatial layout, characters, loci, scientific meaning, interactions, and scene-level replacement will be managed here.",
  },
  stories: {
    title: "Stories",
    eyebrow: "Narrative editor",
    description: "The story editor will support paragraph editing, reordering, focused writing, linked concepts, continuity checks, and student preview.",
  },
  replacement: {
    title: "Complete Story Replacement",
    eyebrow: "Major revision workflow",
    description: "A dedicated replacement flow will preserve required knowledge, compare old and new versions, detect lost dependencies, validate coverage, and keep the prior story recoverable.",
  },
  concepts: {
    title: "Concept Library",
    eyebrow: "Scientific backbone",
    description: "Canonical concepts, definitions, mechanisms, prerequisites, relationships, misconceptions, source notes, and teaching locations will be managed here.",
  },
  "memory-objects": {
    title: "Memory Objects",
    eyebrow: "Memory architecture",
    description: "Canonical terms, definitions, pronunciation, mnemonic actors, loci, confusables, productive retrieval, spelling retrieval, and application targets will be managed here.",
  },
  questions: {
    title: "Question Bank",
    eyebrow: "Assessment",
    description: "Question creation, variants, distractors, explanations, difficulty, concept links, AP skills, media, duplication, and bulk editing will be managed here.",
  },
  review: {
    title: "Review System",
    eyebrow: "Retrieval planning",
    description: "Immediate, journey, unit, delayed, mixed, and exact-name review opportunities will be visible on a concept timeline and editable as validated drafts.",
  },
  challenge: {
    title: "Challenge Lab",
    eyebrow: "Application",
    description: "Challenge scenarios, data, graphs, variables, questions, expected reasoning, scoring guidance, and prerequisite links will be managed here.",
  },
  media: {
    title: "Media Library",
    eyebrow: "Assets",
    description: "Images, diagrams, audio, alt text, source notes, usage locations, replacements, and orphan detection will be managed here.",
  },
  preview: {
    title: "Student Preview",
    eyebrow: "Experience check",
    description: "Draft content will be previewed through the real student interface across desktop, tablet, and phone views before publication.",
  },
  health: {
    title: "Content Health",
    eyebrow: "Validation",
    description: "Concrete checks will surface broken references, missing fields, orphaned content, duplicate candidates, overloaded scenes, and incomplete retrieval coverage.",
  },
  versions: {
    title: "Version History",
    eyebrow: "Recovery",
    description: "Every major content item will keep revision history, side-by-side comparisons, release notes, and recoverable prior versions.",
  },
  "import-export": {
    title: "Import and Export",
    eyebrow: "Portability",
    description: "Validated imports and exports will support structured content, question banks, units, journeys, backups, and future migrations.",
  },
  publishing: {
    title: "Publishing",
    eyebrow: "Release control",
    description: "The publish flow will move from draft through preview, validation, dependency review, version creation, release summary, and controlled publication.",
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
  return new Intl.NumberFormat().format(value || 0);
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

function renderMetrics(units) {
  const totals = units.reduce(
    (acc, unit) => {
      acc.units += 1;
      acc.journeys += Number(unit.journey_count || unit.journeys || 0);
      acc.scenes += Number(unit.scene_count || unit.permanent_loci || 0);
      acc.challenges += Number(unit.application_challenges || unit.challenge_lab_records || 0);
      acc.canonical += Number(unit.canonical_records || 0);
      return acc;
    },
    { units: 0, journeys: 0, scenes: 0, challenges: 0, canonical: 0 }
  );

  const metrics = [
    ["Units", totals.units, "released course units"],
    ["Journeys", totals.journeys, "guided narrative routes"],
    ["Scenes", totals.scenes, "permanent scene locations"],
    ["Canonical records", totals.canonical, "reported locked records"],
    ["Application challenges", totals.challenges, "reported unit challenges"],
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

function renderUnits(units) {
  el("unit-list").innerHTML = units
    .map(
      (unit) => `
        <article class="unit-row">
          <div>
            <h3>Unit ${number(unit.number)} · ${escapeHtml(unit.title)}</h3>
            <p>${escapeHtml(unit.source_status || "No source status recorded")}</p>
          </div>
          <div class="unit-meta" aria-label="Unit ${number(unit.number)} summary">
            <span>${number(unit.journey_count || unit.journeys)} journeys</span>
            <span>${number(unit.scene_count || unit.permanent_loci)} scenes</span>
            <span>${escapeHtml(unit.status || "Unknown")}</span>
          </div>
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
    if (error.status === 401) return showLogin("Your admin session has expired. Sign in again.");
    el("audit-list").innerHTML = `<p class="audit-empty">${escapeHtml(error.message)}</p>`;
  }
}

function activateView(name) {
  const view = views[name] || views.dashboard;
  document.querySelectorAll(".nav-item").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === name);
  });

  el("view-title").textContent = view.title;
  el("view-eyebrow").textContent = view.eyebrow;
  el("view-description").textContent = view.description;

  const isDashboard = name === "dashboard";
  const isSecurity = name === "security";
  el("dashboard-view").classList.toggle("hidden", !isDashboard);
  el("security-view").classList.toggle("hidden", !isSecurity);
  el("placeholder-view").classList.toggle("hidden", isDashboard || isSecurity);

  if (isSecurity) loadSecurity();
  if (!isDashboard && !isSecurity) {
    el("placeholder-title").textContent = view.title;
    el("placeholder-copy").textContent = `${view.description} The protected content catalog and draft layer are built in the next implementation stage.`;
  }
}

async function loadCourse() {
  const banner = el("status-banner");
  banner.classList.remove("ok", "error");
  try {
    const course = await apiRequest("/api/admin/course");
    const registryUnits = Array.isArray(course.units) ? course.units : [];
    const summaries = await Promise.all(
      registryUnits.map(async (unit) => {
        try {
          return await apiRequest(`/api/admin/units/${encodeURIComponent(unit.unit_id)}`);
        } catch {
          return {};
        }
      })
    );
    const units = registryUnits.map((unit, index) => ({ ...unit, ...summaries[index] }));
    renderMetrics(units);
    renderUnits(units);
    state.courseLoaded = true;
    banner.textContent = `Loaded ${units.length} released units through the protected admin API. Content editing remains disabled in Step 2.`;
    banner.classList.add("ok");
  } catch (error) {
    if (error.status === 401) return showLogin("Your admin session has expired. Sign in again.");
    banner.textContent = `The protected course inventory could not be read. ${error.message}`;
    banner.classList.add("error");
    el("metric-grid").innerHTML = "";
    el("unit-list").innerHTML = "";
  }
}

function showStudio(session) {
  state.session = session;
  state.csrfToken = session.csrf_token || "";
  el("session-user").textContent = `${session.username} · ${session.role}`;
  el("login-view").classList.add("hidden");
  el("studio-shell").classList.remove("hidden");
  el("login-message").textContent = "";
  el("admin-password").value = "";
  renderCapabilities();
  activateView("dashboard");
  loadCourse();
}

function showLogin(message = "") {
  state.session = null;
  state.csrfToken = "";
  state.courseLoaded = false;
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
    showStudio(session);
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
    showStudio(session);
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

el("refresh-audit").addEventListener("click", loadSecurity);

document.querySelectorAll(".nav-item").forEach((button) => {
  button.addEventListener("click", () => activateView(button.dataset.view));
});

restoreSession();
