from __future__ import annotations

from pathlib import Path
from typing import Any

from .settings import ROOT

CAPABILITY_AUDIT_SCHEMA = "story-method-content-studio-capability-audit-1.0"

WORKSPACES = [
    {
        "id": "dashboard",
        "label": "Dashboard",
        "purpose": "Course totals, release alignment, normalized inventory, and administrator orientation.",
        "frontend": ["frontend/admin/admin.js"],
        "backend": ["backend/admin_catalog.py"],
        "capabilities": ["course totals", "release alignment", "catalog inventory", "global search"],
    },
    {
        "id": "course-map",
        "label": "Course Map",
        "purpose": "Browse Unit to Journey to Scene structure with dependency inspection.",
        "frontend": ["frontend/admin/admin.js"],
        "backend": ["backend/admin_catalog.py"],
        "capabilities": ["hierarchy browser", "dependency inspector", "source locations"],
    },
    {
        "id": "units",
        "label": "Units",
        "purpose": "Field-specific editing for normalized unit records through protected working copies.",
        "frontend": ["frontend/admin/editor.js"],
        "backend": ["backend/admin_editors.py", "backend/admin_drafts.py"],
        "capabilities": ["field editor", "autosave", "snapshots", "draft isolation"],
    },
    {
        "id": "journeys",
        "label": "Journeys",
        "purpose": "Edit journey identity, narrative framing, route guidance, and related metadata.",
        "frontend": ["frontend/admin/editor.js"],
        "backend": ["backend/admin_editors.py", "backend/admin_drafts.py"],
        "capabilities": ["field editor", "draft history", "dependency context"],
    },
    {
        "id": "scenes",
        "label": "Scenes",
        "purpose": "Edit scene place, cast, story, retrieval, and structural fields.",
        "frontend": ["frontend/admin/editor.js"],
        "backend": ["backend/admin_editors.py", "backend/admin_drafts.py"],
        "capabilities": ["scene editor", "story paragraphs", "cast", "retrieval fields"],
    },
    {
        "id": "stories",
        "label": "Stories",
        "purpose": "Narrative-focused scene editing with recoverable working-copy history.",
        "frontend": ["frontend/admin/editor.js"],
        "backend": ["backend/admin_editors.py", "backend/admin_drafts.py"],
        "capabilities": ["paragraph editing", "story focus", "autosave", "snapshots"],
    },
    {
        "id": "characters",
        "label": "Characters",
        "purpose": "Edit normalized character and scene-object roles used across narratives.",
        "frontend": ["frontend/admin/editor.js"],
        "backend": ["backend/admin_editors.py"],
        "capabilities": ["character browser", "role editing", "scene references"],
    },
    {
        "id": "locations",
        "label": "Locations",
        "purpose": "Edit spatial descriptions and scene-location records.",
        "frontend": ["frontend/admin/editor.js"],
        "backend": ["backend/admin_editors.py"],
        "capabilities": ["location browser", "spatial editing", "scene references"],
    },
    {
        "id": "replacement",
        "label": "Complete Story Replacement",
        "purpose": "Replace scene or journey narrative while preserving route identity and required scientific coverage.",
        "frontend": ["frontend/admin/replacement.js"],
        "backend": ["backend/admin_replacements.py", "backend/admin_replacement_routes.py"],
        "capabilities": ["replacement modes", "knowledge locks", "dependency analysis", "automatic snapshot"],
    },
    {
        "id": "concepts",
        "label": "Concept Library",
        "purpose": "Edit canonical scientific concepts and inspect downstream relationships.",
        "frontend": ["frontend/admin/editor.js"],
        "backend": ["backend/admin_editors.py", "backend/admin_catalog.py"],
        "capabilities": ["concept editor", "definitions", "relationships", "dependency graph"],
    },
    {
        "id": "memory-objects",
        "label": "Memory Objects",
        "purpose": "Edit structured memory representations, mnemonic fields, retrieval targets, and concept links.",
        "frontend": ["frontend/admin/editor.js"],
        "backend": ["backend/admin_editors.py"],
        "capabilities": ["memory-object editor", "mnemonic fields", "retrieval fields", "trace links"],
    },
    {
        "id": "questions",
        "label": "Question Bank",
        "purpose": "Manage existing questions, mixed-discrimination sets, and new draft-only proposals.",
        "frontend": ["frontend/admin/management.js"],
        "backend": ["backend/admin_management.py", "backend/admin_management_routes.py"],
        "capabilities": ["question editing", "new proposals", "question sets", "filters"],
    },
    {
        "id": "review",
        "label": "Review System",
        "purpose": "Inspect retrieval timing, review coverage, discrimination, and missing later retrieval.",
        "frontend": ["frontend/admin/management.js"],
        "backend": ["backend/admin_management.py", "backend/admin_management_routes.py"],
        "capabilities": ["retrieval timeline", "coverage inspection", "linked questions"],
    },
    {
        "id": "challenge",
        "label": "Challenge Lab",
        "purpose": "Edit application challenges, answer guides, prerequisites, and linked scientific references.",
        "frontend": ["frontend/admin/management.js"],
        "backend": ["backend/admin_management.py"],
        "capabilities": ["challenge editor", "new proposals", "prerequisites", "answer guides"],
    },
    {
        "id": "media",
        "label": "Media Library",
        "purpose": "Stage and manage private media metadata, accessibility information, associations, and archive state.",
        "frontend": ["frontend/admin/management.js"],
        "backend": ["backend/admin_management.py"],
        "capabilities": ["staging", "metadata", "alt text", "captions", "transcripts", "archive and restore"],
    },
    {
        "id": "preview",
        "label": "Student Preview",
        "purpose": "Render draft-aware student views in script-isolated responsive previews.",
        "frontend": ["frontend/admin/quality.js"],
        "backend": ["backend/admin_quality.py", "backend/admin_quality_routes.py"],
        "capabilities": ["working-copy preview", "published comparison", "device presets", "student renderers"],
    },
    {
        "id": "health",
        "label": "Content Health",
        "purpose": "Run pre-publication scientific, structural, narrative, retrieval, readability, and accessibility checks.",
        "frontend": ["frontend/admin/quality.js"],
        "backend": ["backend/admin_quality.py"],
        "capabilities": ["blocking errors", "warnings", "advisories", "draft-aware checks"],
    },
    {
        "id": "drafts",
        "label": "Draft Workspace",
        "purpose": "Manage protected working copies, autosave, snapshots, revisions, comparison, archive, and recovery.",
        "frontend": ["frontend/admin/drafts.js"],
        "backend": ["backend/admin_drafts.py", "backend/admin_draft_routes.py"],
        "capabilities": ["working copies", "revisions", "snapshots", "compare", "archive", "restore"],
    },
    {
        "id": "versions",
        "label": "Version History",
        "purpose": "Inspect publication candidates, validated releases, recovery history, and rollback candidates.",
        "frontend": ["frontend/admin/publication.js"],
        "backend": ["backend/admin_publication.py", "backend/admin_publication_routes.py"],
        "capabilities": ["candidate history", "release history", "rollback candidate"],
    },
    {
        "id": "import-export",
        "label": "Import and Export",
        "purpose": "Validate portable Content Studio bundles and apply imports to working copies only.",
        "frontend": ["frontend/admin/management.js"],
        "backend": ["backend/admin_management.py"],
        "capabilities": ["JSON export", "import validation", "draft-only import", "conflict handling"],
    },
    {
        "id": "publishing",
        "label": "Publishing",
        "purpose": "Create isolated release candidates, validate exact changes, submit controlled GitHub candidates, and verify releases.",
        "frontend": ["frontend/admin/publication.js"],
        "backend": ["backend/admin_publication.py", "backend/admin_publication_routes.py"],
        "capabilities": ["release candidates", "hash verification", "quality gates", "rollback", "GitHub delivery"],
    },
    {
        "id": "security",
        "label": "Security and Audit",
        "purpose": "Inspect owner authentication, session protection, CSRF enforcement, throttling, and audit events.",
        "frontend": ["frontend/admin/admin.js", "frontend/admin/health-repair.js"],
        "backend": ["backend/admin_auth.py"],
        "capabilities": ["owner session", "CSRF", "rate limiting", "audit history", "system health shortcut"],
    },
    {
        "id": "settings",
        "label": "Settings",
        "purpose": "Inspect zero-cost local system health and run bounded, recoverable maintenance actions.",
        "frontend": ["frontend/admin/health-repair.js"],
        "backend": ["backend/admin_health.py", "backend/admin_health_routes.py"],
        "capabilities": ["system health", "publication-lock checks", "safe repair", "backup", "local environment diagnostics"],
    },
]

WORKFLOW = [
    {"step": 1, "label": "Browse", "view": "course-map", "detail": "Locate the Unit, Journey, Scene, concept, Memory Object, or assessment record."},
    {"step": 2, "label": "Edit", "view": "stories", "detail": "Open a field-specific editor or Complete Story Replacement workflow."},
    {"step": 3, "label": "Draft", "view": "drafts", "detail": "Changes stay in protected working copies with revisions and snapshots."},
    {"step": 4, "label": "Preview", "view": "preview", "detail": "Inspect the working copy through the student-facing renderer."},
    {"step": 5, "label": "Validate", "view": "health", "detail": "Resolve blocking findings and review warnings before release."},
    {"step": 6, "label": "Publish", "view": "publishing", "detail": "Create and validate an isolated release candidate through explicit gates."},
    {"step": 7, "label": "Recover", "view": "versions", "detail": "Inspect release history or create a rollback candidate when needed."},
]

INTENTIONAL_LIMITS = [
    {
        "id": "local-owner-only",
        "status": "intentional",
        "title": "Single local owner account",
        "detail": "The zero-cost local deployment currently exposes the owner role only. Multi-user role administration is outside the current local operating model.",
    },
    {
        "id": "publication-off-by-default",
        "status": "safety_lock",
        "title": "Publication gates remain off by default",
        "detail": "Drafting, preview, validation, backup, and recovery work locally. Publication must be deliberately configured and is never enabled by the zero-cost launcher.",
    },
    {
        "id": "media-staging-only",
        "status": "intentional",
        "title": "Staged media is private until a runtime asset mapping exists",
        "detail": "Media metadata and files can be staged and audited, while student-runtime asset publication remains explicitly blocked until a validated mapping is added.",
    },
    {
        "id": "analytics-deferred",
        "status": "deferred",
        "title": "Student performance analytics are not part of the administrator release",
        "detail": "The current system manages curriculum content. Future student-performance signals remain a separate extension and are not represented as implemented functionality.",
    },
]


def _exists(path: str) -> bool:
    return (ROOT / path).exists()


def _workspace_status(spec: dict[str, Any]) -> dict[str, Any]:
    evidence = [*spec.get("frontend", []), *spec.get("backend", [])]
    missing = [path for path in evidence if not _exists(path)]
    result = dict(spec)
    result["evidence"] = evidence
    result["missing_evidence"] = missing
    result["status"] = "implemented" if not missing else "incomplete"
    return result


def capability_audit() -> dict[str, Any]:
    workspaces = [_workspace_status(spec) for spec in WORKSPACES]
    implemented = sum(1 for item in workspaces if item["status"] == "implemented")
    incomplete = len(workspaces) - implemented
    return {
        "schema": CAPABILITY_AUDIT_SCHEMA,
        "summary": {
            "workspace_count": len(workspaces),
            "implemented": implemented,
            "incomplete": incomplete,
            "workflow_steps": len(WORKFLOW),
            "intentional_limits": len(INTENTIONAL_LIMITS),
        },
        "workspaces": workspaces,
        "workflow": WORKFLOW,
        "intentional_limits": INTENTIONAL_LIMITS,
        "student_content_write_from_audit": False,
        "zero_cost_boundary": True,
    }
