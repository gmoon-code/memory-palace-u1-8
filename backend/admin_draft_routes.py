from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from . import admin_auth, admin_drafts, admin_editor_routes, admin_replacement_routes
from .settings import ADMIN_ENABLED

draft_router = APIRouter(prefix="/api/admin/drafts", tags=["content-studio-drafts"])


class CreateDraftRequest(BaseModel):
    entity_id: str = Field(min_length=1, max_length=512)


class SaveDraftRequest(BaseModel):
    payload: dict[str, Any]
    expected_version: int = Field(ge=1)
    note: str | None = Field(default=None, max_length=500)
    autosave: bool = False


class VersionRequest(BaseModel):
    expected_version: int = Field(ge=1)


class RevisionRestoreRequest(BaseModel):
    expected_version: int = Field(ge=1)


class SnapshotRequest(BaseModel):
    label: str = Field(min_length=1, max_length=160)


def _owner(request: Request, *, csrf: bool = False) -> admin_auth.AdminSession:
    if not ADMIN_ENABLED:
        raise HTTPException(404, "Not found")
    session = admin_auth.get_session(request, require_csrf=csrf)
    if session.role != "owner":
        raise HTTPException(403, "Admin owner access required")
    return session


def _raise_draft_error(exc: Exception) -> None:
    if isinstance(exc, admin_drafts.DraftNotFound):
        raise HTTPException(404, str(exc)) from exc
    if isinstance(exc, admin_drafts.DraftConflict):
        raise HTTPException(409, str(exc)) from exc
    if isinstance(exc, admin_drafts.DraftError):
        raise HTTPException(400, str(exc)) from exc
    raise exc


@draft_router.get("/summary")
def draft_summary(request: Request):
    _owner(request)
    return admin_drafts.draft_summary()


@draft_router.get("")
def drafts_list(
    request: Request,
    status: str | None = None,
    unit_id: str | None = None,
    entity_type: str | None = None,
    limit: int = 100,
):
    _owner(request)
    try:
        return admin_drafts.list_drafts(
            status=status,
            unit_id=unit_id,
            entity_type=entity_type,
            limit=limit,
        )
    except Exception as exc:
        _raise_draft_error(exc)


@draft_router.post("")
def drafts_create(payload: CreateDraftRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        return admin_drafts.create_draft(payload.entity_id, session.username)
    except Exception as exc:
        _raise_draft_error(exc)


@draft_router.get("/{draft_id}")
def draft_get(draft_id: str, request: Request):
    _owner(request)
    try:
        return admin_drafts.get_draft(draft_id)
    except Exception as exc:
        _raise_draft_error(exc)


@draft_router.patch("/{draft_id}")
def draft_save(draft_id: str, payload: SaveDraftRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        return admin_drafts.update_draft(
            draft_id,
            payload=payload.payload,
            expected_version=payload.expected_version,
            username=session.username,
            note=payload.note,
            autosave=payload.autosave,
        )
    except Exception as exc:
        _raise_draft_error(exc)


@draft_router.post("/{draft_id}/archive")
def draft_archive(draft_id: str, payload: VersionRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        return admin_drafts.archive_draft(
            draft_id,
            expected_version=payload.expected_version,
            username=session.username,
        )
    except Exception as exc:
        _raise_draft_error(exc)


@draft_router.post("/{draft_id}/restore-archive")
def draft_restore_archive(draft_id: str, payload: VersionRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        return admin_drafts.unarchive_draft(
            draft_id,
            expected_version=payload.expected_version,
            username=session.username,
        )
    except Exception as exc:
        _raise_draft_error(exc)


@draft_router.get("/{draft_id}/revisions")
def draft_revisions(draft_id: str, request: Request, limit: int = 100):
    _owner(request)
    try:
        return admin_drafts.list_revisions(draft_id, limit=limit)
    except Exception as exc:
        _raise_draft_error(exc)


@draft_router.get("/{draft_id}/revisions/{revision_id}")
def draft_revision(draft_id: str, revision_id: int, request: Request):
    _owner(request)
    try:
        return admin_drafts.get_revision(draft_id, revision_id)
    except Exception as exc:
        _raise_draft_error(exc)


@draft_router.post("/{draft_id}/revisions/{revision_id}/restore")
def draft_restore_revision(
    draft_id: str,
    revision_id: int,
    payload: RevisionRestoreRequest,
    request: Request,
):
    session = _owner(request, csrf=True)
    try:
        return admin_drafts.restore_revision(
            draft_id,
            revision_id,
            expected_version=payload.expected_version,
            username=session.username,
        )
    except Exception as exc:
        _raise_draft_error(exc)


@draft_router.get("/{draft_id}/snapshots")
def draft_snapshots(draft_id: str, request: Request, limit: int = 100):
    _owner(request)
    try:
        return admin_drafts.list_snapshots(draft_id, limit=limit)
    except Exception as exc:
        _raise_draft_error(exc)


@draft_router.post("/{draft_id}/snapshots")
def draft_snapshot_create(draft_id: str, payload: SnapshotRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        return admin_drafts.create_snapshot(
            draft_id,
            label=payload.label,
            username=session.username,
        )
    except Exception as exc:
        _raise_draft_error(exc)


@draft_router.post("/{draft_id}/snapshots/{snapshot_id}/restore")
def draft_snapshot_restore(
    draft_id: str,
    snapshot_id: int,
    payload: RevisionRestoreRequest,
    request: Request,
):
    session = _owner(request, csrf=True)
    try:
        return admin_drafts.restore_snapshot(
            draft_id,
            snapshot_id,
            expected_version=payload.expected_version,
            username=session.username,
        )
    except Exception as exc:
        _raise_draft_error(exc)


@draft_router.get("/{draft_id}/compare")
def draft_compare(
    draft_id: str,
    request: Request,
    revision_id: int | None = None,
    snapshot_id: int | None = None,
):
    _owner(request)
    if revision_id is not None and snapshot_id is not None:
        raise HTTPException(400, "Choose either revision_id or snapshot_id")
    try:
        return admin_drafts.compare_draft(
            draft_id,
            revision_id=revision_id,
            snapshot_id=snapshot_id,
        )
    except Exception as exc:
        _raise_draft_error(exc)


# Main imports one router. Keep draft, field-editor, and replacement APIs behind
# the same authenticated Content Studio registration point.
router = APIRouter()
router.include_router(admin_replacement_routes.assets)
router.include_router(draft_router)
router.include_router(admin_editor_routes.router)
router.include_router(admin_replacement_routes.router)
