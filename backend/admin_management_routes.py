from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from . import admin_auth, admin_drafts, admin_management
from .settings import ADMIN_ENABLED

router = APIRouter(prefix="/api/admin/management", tags=["content-studio-management"])


class CreateManagedDraftRequest(BaseModel):
    entity_id: str = Field(min_length=1, max_length=512)
    course_id: str = Field(default="ap-biology", min_length=1, max_length=128)


class SaveManagedDraftRequest(BaseModel):
    course_id: str = Field(default="ap-biology", min_length=1, max_length=128)
    payload: dict[str, Any]
    expected_version: int = Field(ge=1)
    note: str | None = Field(default=None, max_length=500)
    autosave: bool = False


class CreateProposalRequest(BaseModel):
    course_id: str = Field(default="ap-biology", min_length=1, max_length=128)
    entity_type: str = Field(min_length=1, max_length=80)
    unit_id: str = Field(min_length=1, max_length=40)
    title: str = Field(min_length=1, max_length=500)
    seed: dict[str, Any] | None = None


class BulkPreviewRequest(BaseModel):
    course_id: str = Field(default="ap-biology", min_length=1, max_length=128)
    find: str = Field(min_length=2, max_length=500)
    replacement: str = Field(default="", max_length=5000)
    case_sensitive: bool = False
    unit_id: str | None = Field(default=None, max_length=40)
    entity_types: list[str] | None = None
    limit: int = Field(default=500, ge=1, le=500)


class BulkTarget(BaseModel):
    entity_id: str = Field(min_length=1, max_length=512)
    expected_version: int = Field(ge=0)


class BulkApplyRequest(BaseModel):
    course_id: str = Field(default="ap-biology", min_length=1, max_length=128)
    find: str = Field(min_length=2, max_length=500)
    replacement: str = Field(default="", max_length=5000)
    case_sensitive: bool = False
    targets: list[BulkTarget] = Field(min_length=1, max_length=75)


class ImportBundleRequest(BaseModel):
    course_id: str = Field(default="ap-biology", min_length=1, max_length=128)
    bundle: dict[str, Any]


class ApplyImportRequest(BaseModel):
    course_id: str = Field(default="ap-biology", min_length=1, max_length=128)
    bundle: dict[str, Any]
    conflict_policy: str = Field(default="skip", max_length=40)


class MediaMetadataRequest(BaseModel):
    course_id: str = Field(default="ap-biology", min_length=1, max_length=128)
    expected_version: int = Field(ge=1)
    alt_text: str | None = Field(default=None, max_length=4000)
    caption: str | None = Field(default=None, max_length=8000)
    transcript: str | None = Field(default=None, max_length=50000)
    unit_id: str | None = Field(default=None, max_length=40)
    entity_id: str | None = Field(default=None, max_length=512)


class MediaStatusRequest(BaseModel):
    course_id: str = Field(default="ap-biology", min_length=1, max_length=128)
    expected_version: int = Field(ge=1)


def _owner(request: Request, *, csrf: bool = False) -> admin_auth.AdminSession:
    if not ADMIN_ENABLED:
        raise HTTPException(404, "Not found")
    session = admin_auth.get_session(request, require_csrf=csrf)
    if session.role != "owner":
        raise HTTPException(403, "Admin owner access required")
    return session


def _raise_management_error(exc: Exception) -> None:
    if isinstance(exc, admin_drafts.DraftNotFound):
        raise HTTPException(404, str(exc)) from exc
    if isinstance(exc, admin_drafts.DraftConflict):
        raise HTTPException(409, str(exc)) from exc
    if isinstance(exc, admin_drafts.DraftError):
        raise HTTPException(400, str(exc)) from exc
    raise exc


@router.get("/question-bank")
def question_bank(
    request: Request,
    course_id: str = "ap-biology",
    unit_id: str | None = None,
    question_type: str | None = None,
    q: str | None = None,
    limit: int = 500,
):
    _owner(request)
    try:
        return admin_management.question_bank(
            course_id=course_id,
            unit_id=unit_id,
            question_type=question_type,
            query=q,
            limit=limit,
        )
    except Exception as exc:
        _raise_management_error(exc)


@router.get("/challenge-bank")
def challenge_bank(
    request: Request,
    course_id: str = "ap-biology",
    unit_id: str | None = None,
    q: str | None = None,
    limit: int = 500,
):
    _owner(request)
    try:
        return admin_management.challenge_bank(course_id=course_id, unit_id=unit_id, query=q, limit=limit)
    except Exception as exc:
        _raise_management_error(exc)


@router.get("/entity")
def managed_entity(request: Request, entity_id: str, course_id: str = "ap-biology"):
    _owner(request)
    if entity_id.startswith("new:"):
        try:
            draft = admin_management._active_draft_for_entity(entity_id, course_id)
            if draft is None:
                raise admin_drafts.DraftNotFound("Proposed record not found")
            return {"entity": draft["payload"], "draft": draft, "proposal": True}
        except Exception as exc:
            _raise_management_error(exc)
    try:
        return {
            "entity": admin_management.managed_entity(entity_id, course_id),
            "draft": admin_management._active_draft_for_entity(entity_id, course_id),
            "proposal": False,
        }
    except Exception as exc:
        _raise_management_error(exc)


@router.post("/drafts")
def create_managed_draft(payload: CreateManagedDraftRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        if payload.entity_id.startswith("new:"):
            draft = admin_management._active_draft_for_entity(payload.entity_id, payload.course_id)
            if draft is None:
                raise admin_drafts.DraftNotFound("Proposed record not found")
            return draft
        return admin_management.create_managed_draft(
            payload.entity_id,
            session.username,
            payload.course_id,
        )
    except Exception as exc:
        _raise_management_error(exc)


@router.patch("/drafts/{draft_id}")
def save_managed_draft(draft_id: str, payload: SaveManagedDraftRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        return admin_management.save_managed_draft(
            draft_id,
            payload=payload.payload,
            expected_version=payload.expected_version,
            username=session.username,
            note=payload.note,
            autosave=payload.autosave,
            course_id=payload.course_id,
        )
    except Exception as exc:
        _raise_management_error(exc)


@router.post("/proposals")
def create_proposal(payload: CreateProposalRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        return admin_management.create_proposed_draft(
            payload.entity_type,
            payload.unit_id,
            payload.title,
            session.username,
            seed=payload.seed,
            course_id=payload.course_id,
        )
    except Exception as exc:
        _raise_management_error(exc)


@router.get("/review-timeline")
def review_timeline(request: Request, unit_id: str, course_id: str = "ap-biology"):
    _owner(request)
    try:
        return admin_management.review_timeline(unit_id, course_id)
    except Exception as exc:
        _raise_management_error(exc)


@router.get("/search")
def workspace_search(
    request: Request,
    q: str,
    course_id: str = "ap-biology",
    unit_id: str | None = None,
    limit: int = 100,
):
    _owner(request)
    try:
        return admin_management.workspace_search(
            q,
            course_id=course_id,
            unit_id=unit_id,
            limit=limit,
        )
    except Exception as exc:
        _raise_management_error(exc)


@router.post("/bulk/preview")
def bulk_preview(payload: BulkPreviewRequest, request: Request):
    _owner(request, csrf=True)
    try:
        return admin_management.bulk_replace_preview(
            find=payload.find,
            replacement=payload.replacement,
            case_sensitive=payload.case_sensitive,
            course_id=payload.course_id,
            unit_id=payload.unit_id,
            entity_types=payload.entity_types,
            limit=payload.limit,
        )
    except Exception as exc:
        _raise_management_error(exc)


@router.post("/bulk/apply")
def bulk_apply(payload: BulkApplyRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        return admin_management.bulk_replace_apply(
            find=payload.find,
            replacement=payload.replacement,
            case_sensitive=payload.case_sensitive,
            targets=[target.model_dump() for target in payload.targets],
            username=session.username,
            course_id=payload.course_id,
        )
    except Exception as exc:
        _raise_management_error(exc)


@router.get("/export")
def export_bundle(
    request: Request,
    course_id: str = "ap-biology",
    unit_id: str | None = None,
    entity_types: str | None = None,
    include_drafts: bool = True,
    include_catalog: bool = True,
):
    _owner(request)
    types = [item.strip() for item in (entity_types or "").split(",") if item.strip()] or None
    try:
        return admin_management.export_bundle(
            course_id=course_id,
            unit_id=unit_id,
            entity_types=types,
            include_drafts=include_drafts,
            include_catalog=include_catalog,
        )
    except Exception as exc:
        _raise_management_error(exc)


@router.post("/import/preview")
def import_preview(payload: ImportBundleRequest, request: Request):
    _owner(request, csrf=True)
    try:
        return admin_management.validate_import_bundle(payload.bundle, payload.course_id)
    except Exception as exc:
        _raise_management_error(exc)


@router.post("/import/apply")
def import_apply(payload: ApplyImportRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        return admin_management.apply_import_bundle(
            payload.bundle,
            username=session.username,
            conflict_policy=payload.conflict_policy,
            course_id=payload.course_id,
        )
    except Exception as exc:
        _raise_management_error(exc)


@router.get("/media/existing")
def media_existing(request: Request, course_id: str = "ap-biology", limit: int = 1000):
    _owner(request)
    try:
        return admin_management.existing_media_inventory(course_id=course_id, limit=limit)
    except Exception as exc:
        _raise_management_error(exc)


@router.get("/media/staged")
def media_staged(
    request: Request,
    course_id: str = "ap-biology",
    status: str | None = "staged",
    unit_id: str | None = None,
    limit: int = 200,
):
    _owner(request)
    try:
        return admin_management.list_staged_media(course_id=course_id, status=status, unit_id=unit_id, limit=limit)
    except Exception as exc:
        _raise_management_error(exc)


@router.post("/media/upload")
async def media_upload(
    request: Request,
    filename: str = Query(min_length=1, max_length=240),
    course_id: str = Query(default="ap-biology", min_length=1, max_length=128),
    kind: str | None = Query(default=None, max_length=40),
    unit_id: str | None = Query(default=None, max_length=40),
    entity_id: str | None = Query(default=None, max_length=512),
    alt_text: str | None = Query(default=None, max_length=4000),
    caption: str | None = Query(default=None, max_length=8000),
):
    session = _owner(request, csrf=True)
    length_header = request.headers.get("content-length")
    if length_header:
        try:
            if int(length_header) > admin_management.MAX_MEDIA_BYTES:
                raise HTTPException(413, "Media file exceeds the 25 MB staging limit")
        except ValueError:
            pass
    content = await request.body()
    if len(content) > admin_management.MAX_MEDIA_BYTES:
        raise HTTPException(413, "Media file exceeds the 25 MB staging limit")
    try:
        return admin_management.stage_media(
            course_id=course_id,
            filename=filename,
            content=content,
            supplied_mime=request.headers.get("content-type"),
            kind=kind,
            unit_id=unit_id,
            entity_id=entity_id,
            alt_text=alt_text,
            caption=caption,
            transcript=None,
            username=session.username,
        )
    except Exception as exc:
        _raise_management_error(exc)


@router.patch("/media/{asset_id}")
def media_update(asset_id: str, payload: MediaMetadataRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        return admin_management.update_media_metadata(
            asset_id,
            expected_version=payload.expected_version,
            alt_text=payload.alt_text,
            caption=payload.caption,
            transcript=payload.transcript,
            unit_id=payload.unit_id,
            entity_id=payload.entity_id,
            username=session.username,
            course_id=payload.course_id,
        )
    except Exception as exc:
        _raise_management_error(exc)


@router.post("/media/{asset_id}/archive")
def media_archive(asset_id: str, payload: MediaStatusRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        return admin_management.set_media_status(
            asset_id,
            expected_version=payload.expected_version,
            status="archived",
            username=session.username,
            course_id=payload.course_id,
        )
    except Exception as exc:
        _raise_management_error(exc)


@router.post("/media/{asset_id}/restore")
def media_restore(asset_id: str, payload: MediaStatusRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        return admin_management.set_media_status(
            asset_id,
            expected_version=payload.expected_version,
            status="staged",
            username=session.username,
            course_id=payload.course_id,
        )
    except Exception as exc:
        _raise_management_error(exc)


@router.get("/media/{asset_id}/file")
def media_file(asset_id: str, request: Request, course_id: str = "ap-biology"):
    _owner(request)
    try:
        path, metadata = admin_management.media_file(asset_id, course_id)
    except Exception as exc:
        _raise_management_error(exc)
    return FileResponse(
        path,
        media_type=metadata["mime_type"],
        filename=metadata["original_filename"],
        content_disposition_type="inline",
        headers={"Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow"},
    )
