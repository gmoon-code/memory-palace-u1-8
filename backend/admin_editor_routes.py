from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from . import admin_auth, admin_drafts, admin_editors
from .settings import ADMIN_ENABLED

router = APIRouter(prefix="/api/admin/editors", tags=["content-studio-editors"])


class CreateEditorDraftRequest(BaseModel):
    entity_id: str = Field(min_length=1, max_length=512)


class SaveEditorDraftRequest(BaseModel):
    payload: dict[str, Any]
    expected_version: int = Field(ge=1)
    note: str | None = Field(default=None, max_length=500)
    autosave: bool = False


class ValidateEditorPayloadRequest(BaseModel):
    entity_type: str = Field(min_length=1, max_length=80)
    payload: dict[str, Any]


def _owner(request: Request, *, csrf: bool = False) -> admin_auth.AdminSession:
    if not ADMIN_ENABLED:
        raise HTTPException(404, "Not found")
    session = admin_auth.get_session(request, require_csrf=csrf)
    if session.role != "owner":
        raise HTTPException(403, "Admin owner access required")
    return session


def _raise_editor_error(exc: Exception) -> None:
    if isinstance(exc, admin_drafts.DraftNotFound):
        raise HTTPException(404, str(exc)) from exc
    if isinstance(exc, admin_drafts.DraftConflict):
        raise HTTPException(409, str(exc)) from exc
    if isinstance(exc, admin_drafts.DraftError):
        raise HTTPException(400, str(exc)) from exc
    raise exc


@router.get("/types")
def editor_types(request: Request):
    _owner(request)
    return {
        "schema": admin_editors.EDITOR_SCHEMA,
        "entity_types": admin_editors.editor_types(),
    }


@router.get("/schema")
def editor_schema(request: Request, entity_type: str):
    _owner(request)
    try:
        return admin_editors.schema_for(entity_type)
    except Exception as exc:
        _raise_editor_error(exc)


@router.get("/entity")
def editor_entity(request: Request, entity_id: str):
    _owner(request)
    try:
        entity = admin_editors.editable_entity(entity_id)
        return {
            "entity": entity,
            "editor_schema": admin_editors.schema_for(entity["type"]),
        }
    except Exception as exc:
        _raise_editor_error(exc)


@router.post("/validate")
def editor_validate(payload: ValidateEditorPayloadRequest, request: Request):
    _owner(request, csrf=True)
    try:
        return admin_editors.validate_payload(payload.entity_type, payload.payload)
    except Exception as exc:
        _raise_editor_error(exc)


@router.post("/drafts")
def editor_draft_create(payload: CreateEditorDraftRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        return admin_editors.create_editor_draft(payload.entity_id, session.username)
    except Exception as exc:
        _raise_editor_error(exc)


@router.patch("/drafts/{draft_id}")
def editor_draft_save(
    draft_id: str,
    payload: SaveEditorDraftRequest,
    request: Request,
):
    session = _owner(request, csrf=True)
    try:
        return admin_editors.save_editor_draft(
            draft_id,
            payload=payload.payload,
            expected_version=payload.expected_version,
            username=session.username,
            note=payload.note,
            autosave=payload.autosave,
        )
    except Exception as exc:
        _raise_editor_error(exc)
