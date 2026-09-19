from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_JS = ROOT / "frontend" / "admin" / "workflow.js"
WORKFLOW_CSS = ROOT / "frontend" / "admin" / "workflow.css"
LOADER = ROOT / "backend" / "admin_replacement_routes.py"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ADMIN WORKFLOW QA FAIL\n- {message}")


def main() -> None:
    require(WORKFLOW_JS.exists(), "workflow.js is missing")
    require(WORKFLOW_CSS.exists(), "workflow.css is missing")
    js = WORKFLOW_JS.read_text(encoding="utf-8")
    css = WORKFLOW_CSS.read_text(encoding="utf-8")
    loader = LOADER.read_text(encoding="utf-8")

    required_stages = ["browse", "edit", "draft", "preview", "validate", "publish", "recover"]
    for stage in required_stages:
        require(f'data-workflow-stage="{stage}"' in js, f"workflow stage {stage!r} is missing")

    require("story-method-content-studio-workflow-context-v1" in js, "session-scoped workflow context storage is missing")
    require("sessionStorage" in js, "workflow context does not persist across same-tab navigation")
    require("workflow-version-history" in js and "openVersionHistory" in js, "record-level version history shortcut is missing")
    require("refreshDraftContext" in js, "active working-copy linking is missing")
    require("contextualQualitySummary" in js, "record-level quality summary is missing")
    require("candidate-draft-check" in js, "publication candidate handoff is missing")
    require("new URLSearchParams({ course_id: context.course_id || currentWorkflowCourseId() })" in js, "publication workflow status lookup is not course-scoped")
    require("data-editor-entity" in js, "field editor selections do not feed workflow context")
    require("data-managed-id" in js, "Question Bank and Challenge Lab selections do not feed workflow context")
    require("data-preview-id" in js, "Student Preview selections do not feed workflow context")
    require("data-replacement-id" in js, "Complete Story Replacement selections do not feed workflow context")
    require("data-draft-id" in js, "Draft Workspace selections do not feed workflow context")
    require('method: "POST"' not in js and "method: 'POST'" not in js, "workflow integration must not create or publish content automatically")
    require("content/ap-biology" not in js, "workflow integration must not target published course files directly")

    import_line = 'import "/admin/workflow.js";'
    require(import_line in loader, "canonical admin loader does not boot workflow.js")
    require(loader.rfind(import_line) > loader.rfind('import "/admin/capability-audit.js";'), "workflow integration must load after the other administrator modules")

    require("workflow-context-bar" in css, "workflow bar styles are missing")
    require("@media(max-width:720px)" in css, "mobile workflow layout is missing")

    print("CONTENT STUDIO WORKFLOW INTEGRATION QA PASS")
    print("- one persistent record context follows administrator navigation")
    print("- Browse, Edit, Draft, Preview, Validate, Publish, and Recover handoffs are present")
    print("- record-level Version History remains available from the context bar")
    print("- Question Bank, Challenge Lab, Story Replacement, editors, preview, and drafts feed the same context")
    print("- workflow integration performs navigation and read-only lookups only")
    print("- no published course source path is written by the workflow layer")


if __name__ == "__main__":
    main()
