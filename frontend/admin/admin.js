const views = {
  dashboard: {
    title: "Dashboard",
    eyebrow: "Content overview",
    description: "A read-only foundation that inventories the current eight-unit AP Biology release without changing student content.",
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
  settings: {
    title: "Settings",
    eyebrow: "Administration",
    description: "Authentication, permissions, editor preferences, validation policy, source settings, and publication configuration will be controlled here.",
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

function number(value) {
  return new Intl.NumberFormat().format(value || 0);
}

function renderMetrics(units) {
  const totals = units.reduce(
    (acc, unit) => {
      acc.units += 1;
      acc.journeys += Number(unit.journey_count || 0);
      acc.scenes += Number(unit.scene_count || 0);
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
          <span>${label}</span>
          <strong>${number(value)}</strong>
          <span>${note}</span>
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
            <h3>Unit ${unit.number} · ${unit.title}</h3>
            <p>${unit.source_status || "No source status recorded"}</p>
          </div>
          <div class="unit-meta" aria-label="Unit ${unit.number} summary">
            <span>${number(unit.journey_count)} journeys</span>
            <span>${number(unit.scene_count)} scenes</span>
            <span>${unit.status || "Unknown"}</span>
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
          <strong>${title}</strong>
          <span>${copy}</span>
        </article>`
    )
    .join("");
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
  el("dashboard-view").classList.toggle("hidden", !isDashboard);
  el("placeholder-view").classList.toggle("hidden", isDashboard);

  if (!isDashboard) {
    el("placeholder-title").textContent = view.title;
    el("placeholder-copy").textContent = `${view.description} Step 1 reserves the module and its navigation while write operations remain intentionally unavailable.`;
  }
}

async function loadCourse() {
  const banner = el("status-banner");
  try {
    const response = await fetch("/api/course", { headers: { Accept: "application/json" }, cache: "no-store" });
    if (!response.ok) throw new Error(`Course API returned ${response.status}`);
    const course = await response.json();
    const units = Array.isArray(course.units) ? course.units : [];
    renderMetrics(units);
    renderUnits(units);
    banner.textContent = `Loaded ${units.length} released units from the current course registry. This foundation does not write to content.`;
    banner.classList.add("ok");
  } catch (error) {
    banner.textContent = `The Content Studio shell loaded, but the course registry could not be read. ${error.message}`;
    banner.classList.add("error");
    el("metric-grid").innerHTML = "";
    el("unit-list").innerHTML = "";
  }
}

document.querySelectorAll(".nav-item").forEach((button) => {
  button.addEventListener("click", () => activateView(button.dataset.view));
});

renderCapabilities();
activateView("dashboard");
loadCourse();
