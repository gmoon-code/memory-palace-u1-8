from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from . import admin_auth, admin_drafts, admin_quality
from .settings import ADMIN_ENABLED

router = APIRouter(prefix="/api/admin/quality", tags=["content-studio-quality"])


def _owner(request: Request) -> admin_auth.AdminSession:
    if not ADMIN_ENABLED:
        raise HTTPException(404, "Not found")
    session = admin_auth.get_session(request)
    if session.role != "owner":
        raise HTTPException(403, "Admin owner access required")
    return session


def _raise_quality_error(exc: Exception) -> None:
    if isinstance(exc, admin_drafts.DraftNotFound):
        raise HTTPException(404, str(exc)) from exc
    if isinstance(exc, admin_drafts.DraftConflict):
        raise HTTPException(409, str(exc)) from exc
    if isinstance(exc, admin_drafts.DraftError):
        raise HTTPException(400, str(exc)) from exc
    raise exc


@router.get("/devices")
def quality_devices(request: Request):
    _owner(request)
    return {"schema": admin_quality.QUALITY_SCHEMA, "devices": admin_quality.DEVICE_PRESETS}


@router.get("/preview")
def quality_preview(
    request: Request,
    entity_id: str,
    draft_id: str | None = None,
    source: str = "auto",
    scene_index: int = 0,
):
    _owner(request)
    try:
        return admin_quality.build_preview(
            entity_id,
            draft_id=draft_id,
            source=source,
            scene_index=scene_index,
        )
    except Exception as exc:
        _raise_quality_error(exc)


@router.get("/entity")
def quality_entity(
    request: Request,
    entity_id: str,
    draft_id: str | None = None,
    source: str = "auto",
):
    _owner(request)
    try:
        return admin_quality.entity_quality(entity_id, draft_id=draft_id, source=source)
    except Exception as exc:
        _raise_quality_error(exc)


@router.get("/report")
def quality_report(request: Request, unit_id: str | None = None):
    _owner(request)
    try:
        return admin_quality.quality_report(unit_id=unit_id)
    except Exception as exc:
        _raise_quality_error(exc)
