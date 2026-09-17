from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, Field

from . import admin_auth, admin_drafts, admin_replacements
from .settings import ADMIN_ENABLED, FRONTEND_DIR

router = APIRouter(prefix="/api/admin/replacements", tags=["content-studio-replacements"])
assets = APIRouter(tags=["content-studio-replacement-assets"])
ADMIN_FRONTEND = (Path(FRONTEND_DIR).resolve() / "admin").resolve()


class CreateReplacementDraftRequest(BaseModel):
    entity_id: str = Field(min_length=1, max_length=512)


class ReplacementRequest(BaseModel):
    draft_id: str = Field(min_length=1, max_length=512)
    expected_version: int = Field(ge=1)
    mode: str = Field(min_length=1, max_length=80)
    replacement: dict[str, Any]
    preservation: dict[str, Any] | None = None


def _owner(request: Request, *, csrf: bool = False) -> admin_auth.AdminSession:
    if not ADMIN_ENABLED:
        raise HTTPException(404, "Not found")
    session = admin_auth.get_session(request, require_csrf=csrf)
    if session.role != "owner":
        raise HTTPException(403, "Admin owner access required")
    return session


def _admin_enabled() -> None:
    if not ADMIN_ENABLED:
        raise HTTPException(404, "Not found")


def _raise_replacement_error(exc: Exception) -> None:
    if isinstance(exc, admin_drafts.DraftNotFound):
        raise HTTPException(404, str(exc)) from exc
    if isinstance(exc, admin_drafts.DraftConflict):
        raise HTTPException(409, str(exc)) from exc
    if isinstance(exc, admin_replacements.ReplacementBlocked):
        raise HTTPException(422, str(exc)) from exc
    if isinstance(exc, admin_drafts.DraftError):
        raise HTTPException(400, str(exc)) from exc
    raise exc


@assets.get("/admin/drafts.js")
def replacement_admin_loader():
    _admin_enabled()
    # This is the canonical Content Studio boot chain. The first registered exact
    # /admin/drafts.js route wins, so every administrator module that must be live
    # is imported here explicitly.
    return Response(
        'import "/admin/drafts-core.js";\n'
        'import "/admin/replacement.js";\n'
        'import "/admin/publication.js";\n'
        'import "/admin/health-repair.js";\n'
        'import "/admin/capability-audit.js";\n',
        media_type="text/javascript",
        headers={"Cache-Control": "no-store"},
    )


@assets.get("/admin/drafts-core.js")
def replacement_admin_core():
    _admin_enabled()
    return FileResponse(
        ADMIN_FRONTEND / "drafts.js",
        media_type="text/javascript",
        headers={"Cache-Control": "no-store"},
    )


@router.get("/plan")
def replacement_plan(request: Request, entity_id: str):
    _owner(request)
    try:
        return admin_replacements.target_plan(entity_id)
    except Exception as exc:
        _raise_replacement_error(exc)


@router.post("/drafts")
def replacement_draft_create(payload: CreateReplacementDraftRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        return admin_replacements.create_replacement_draft(payload.entity_id, session.username)
    except Exception as exc:
        _raise_replacement_error(exc)


@router.post("/analyze")
def replacement_analyze(payload: ReplacementRequest, request: Request):
    _owner(request, csrf=True)
    try:
        return admin_replacements.analyze_replacement(
            payload.draft_id,
            expected_version=payload.expected_version,
            mode=payload.mode,
            replacement=payload.replacement,
            preservation=payload.preservation,
        )
    except Exception as exc:
        _raise_replacement_error(exc)


@router.post("/apply")
def replacement_apply(payload: ReplacementRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        return admin_replacements.apply_replacement(
            payload.draft_id,
            expected_version=payload.expected_version,
            mode=payload.mode,
            replacement=payload.replacement,
            preservation=payload.preservation,
            username=session.username,
        )
    except Exception as exc:
        _raise_replacement_error(exc)
