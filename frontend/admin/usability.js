const USABILITY_GUIDE_KEY = "story-method-content-studio-usability-guide-v1";

const staleCopy = new Map([
  ["Browse normalized Unit records before editing capabilities are introduced.", "Browse and edit normalized Unit records through protected working copies."],
  ["The story editor will use the normalized scene and dependency records created in this stage.", "Edit complete scene narratives while retaining spatial, scientific, retrieval, and dependency context."],
  ["The replacement workflow will use this dependency graph to preserve required knowledge and detect downstream effects.", "Replace complete scene or journey stories with required-knowledge, dependency, recovery, and comparison safeguards."],
  ["Review scheduling and retrieval timelines will build on the normalized question and concept graph.", "Inspect immediate, delayed, discrimination, and application retrieval across the normalized question and concept graph."],
  ["Media dependency indexing will be added after the draft store is established.", "Stage private media, manage accessibility metadata, inspect associations, and keep files outside the public student site."],
  ["Draft-aware student preview arrives after the revision layer is established.", "Preview published or working-copy content through the student renderers before publication."],
  ["Revision history will be implemented with the draft store in the next stage.", "Inspect working-copy revisions, snapshots, publication candidates, verified releases, and recovery paths."],
  ["Validated import and export will use the normalized catalog as its stable content model.", "Export portable Content Studio bundles and validate imports before they can create or update working copies."],
  ["Publishing remains disabled until drafts, revisions, validation, and recoverable snapshots exist.", "Build isolated release candidates from validated working copies when the trusted publication gate is deliberately enabled."],
  ["Permissions, editor preferences, validation policy, source settings, and publication configuration will be controlled here.", "Inspect local system health, publication locks, storage, backups, updater readiness, and bounded repair controls."],
  ["Step 4 stores every change in a separate server-side working copy with revision history. Published AP Biology files remain untouched.", "Working copies keep every change separate from published AP Biology content and retain revision and snapshot history."],
  ["Domain-specific story, question, concept, and Memory Object editors arrive in Step 5.", "Use the field-specific workspaces for ordinary editing. Advanced structured payload editing remains available for recovery and expert inspection."],
  ["This temporary Step 4 editor exposes the normalized working object for regression and recovery testing. Friendly field-specific forms replace this in the next stage.", "This advanced editor exposes the normalized working object for recovery and expert inspection. Ordinary work should use the field-specific Content Studio forms."],
]);

let replacementDirty = false;
let guardBypassUntil = 0;

function u(id) {
  return document.getElementById(id);
}

function normalizeVisibleCopy(root = document) {
  root.querySelectorAll("p, small, span").forEach((node) => {
    const text = node.textContent?.trim();
    if (text && staleCopy.has(text)) node.textContent = staleCopy.get(text);
  });
  document.querySelectorAll(".capability-panel").forEach((panel) => {
    const heading = panel.querySelector("h2");
    const eyebrow = panel.querySelector(".eyebrow");
    if (heading?.textContent?.trim() === "Capability map") {
      heading.textContent = "Administrator capabilities";
      if (eyebrow) eyebrow.textContent = "Integrated workspace";
    }
  });
}

function ensureStyles() {
  if (document.querySelector('link[href="/admin/usability.css"]')) return;
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = "/admin/usability.css";
  document.head.appendChild(link);
}

function guideWasSeen() {
  try {
    return window.sessionStorage.getItem(USABILITY_GUIDE_KEY) === "seen";
  } catch {
    return false;
  }
}

function markGuideSeen() {
  try {
    window.sessionStorage.setItem(USABILITY_GUIDE_KEY, "seen");
  } catch {
    // The guide remains usable when session storage is unavailable.
  }
}

function ensureGuide() {
  const bar = u("workflow-context-bar");
  if (!bar || u("admin-usability-guide")) return;
  const guide = document.createElement("details");
  guide.id = "admin-usability-guide";
  guide.className = "admin-usability-guide";
  guide.open = !guideWasSeen();
  guide.innerHTML = `
    <summary>How Content Studio work moves from editing to release</summary>
    <div class="admin-usability-guide-body">
      <p><strong>Choose one record.</strong> The Current record bar keeps that Unit, Journey, Scene, story, concept, Memory Object, question, or challenge in context while you move between workspaces.</p>
      <p><strong>Edit safely.</strong> Published student content stays locked while you work. Open or create a working copy before making changes.</p>
      <p><strong>Inspect before release.</strong> Use Preview and Validate for the same current record, then review revisions or snapshots whenever you need recovery.</p>
      <p><strong>Publication stays deliberate.</strong> The workflow can take you to Publishing, but it never creates a release candidate, submits to GitHub, merges, or rolls back automatically.</p>
      <p><strong>Local edition remains $0.</strong> Content Studio operates on the local computer with publication gates off unless they are deliberately configured later.</p>
    </div>`;
  bar.insertAdjacentElement("afterend", guide);
  guide.addEventListener("toggle", () => {
    if (!guide.open) markGuideSeen();
  });
}

function visible(node) {
  if (!node) return false;
  if (node.classList.contains("hidden") || node.classList.contains("replacement-hidden")) return false;
  return node.getClientRects().length > 0 || !document.body.contains(node) ? false : window.getComputedStyle(node).display !== "none";
}

function textSuggestsUnsaved(node) {
  const value = node?.textContent?.trim().toLowerCase() || "";
  return value.includes("unsaved") || value.includes("saving") || value.includes("autosaving") || value.includes("pending");
}

function hasUnsavedLocalWork() {
  const editor = u("editor-view");
  if (visible(editor) && textSuggestsUnsaved(u("editor-save-state"))) return true;
  const management = u("management-view");
  if (visible(management) && textSuggestsUnsaved(u("managed-save-state"))) return true;
  const draft = u("draft-view");
  if (visible(draft) && textSuggestsUnsaved(u("draft-save-state"))) return true;
  const replacement = u("replacement-view");
  if (visible(replacement) && replacementDirty) return true;
  return false;
}

function guardNavigation(event) {
  if (Date.now() < guardBypassUntil || !hasUnsavedLocalWork()) return;
  const target = event.target instanceof Element ? event.target : null;
  if (!target) return;
  const navigation = target.closest(".nav-item, [data-workflow-stage]");
  if (!navigation) return;
  const accepted = window.confirm("There are unsaved local changes in the current Content Studio workspace. Leave this workspace and discard any changes that have not finished saving?");
  if (accepted) {
    guardBypassUntil = Date.now() + 800;
    return;
  }
  event.preventDefault();
  event.stopImmediatePropagation();
}

function wireReplacementDirtyState() {
  document.addEventListener("input", (event) => {
    const target = event.target instanceof Element ? event.target : null;
    if (target?.closest("#replacement-form")) replacementDirty = true;
  }, true);
  document.addEventListener("change", (event) => {
    const target = event.target instanceof Element ? event.target : null;
    if (target?.closest("#replacement-form, #replacement-policies, #replacement-mode")) replacementDirty = true;
  }, true);
  document.addEventListener("click", (event) => {
    const target = event.target instanceof Element ? event.target : null;
    if (!target) return;
    if (target.closest("[data-replacement-id]")) replacementDirty = false;
    if (target.closest("#replacement-open-draft")) replacementDirty = false;
    if (target.closest("#replacement-apply")) {
      window.setTimeout(() => {
        const applied = u("replacement-applied");
        if (applied && !applied.classList.contains("replacement-hidden") && applied.textContent.trim()) replacementDirty = false;
      }, 700);
    }
  }, true);
}

function wireUnloadGuard() {
  window.addEventListener("beforeunload", (event) => {
    if (!hasUnsavedLocalWork()) return;
    event.preventDefault();
    event.returnValue = "";
  });
  document.addEventListener("click", guardNavigation, true);
}

function observeCopy() {
  const shell = u("studio-shell");
  if (!shell) return;
  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      mutation.addedNodes.forEach((node) => {
        if (node instanceof Element) normalizeVisibleCopy(node);
      });
    }
  });
  observer.observe(shell, { childList: true, subtree: true });
}

function initializeUsabilityPass() {
  ensureStyles();
  normalizeVisibleCopy();
  ensureGuide();
  wireReplacementDirtyState();
  wireUnloadGuard();
  observeCopy();
  const status = document.querySelector(".brand-block .status-pill");
  if (status) status.textContent = "Integrated administrator workspace";
}

initializeUsabilityPass();