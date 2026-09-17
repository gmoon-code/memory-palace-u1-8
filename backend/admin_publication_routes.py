from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from pydantic import BaseModel, Field

from . import admin_auth, admin_drafts, admin_publication
from .settings import ADMIN_ENABLED, FRONTEND_DIR

router = APIRouter(prefix="/api/admin/publication", tags=["content-studio-publication"])
assets = APIRouter(tags=["content-studio-publication-assets"])
ADMIN_INDEX = Path(FRONTEND_DIR) / "admin" / "index.html"


class CandidateRequest(BaseModel):
    draft_ids: list[str] = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=300)
    notes: str | None = Field(default=None, max_length=12000)
    warnings_acknowledged: bool = False


class RollbackRequest(BaseModel):
    title: str | None = Field(default=None, max_length=300)


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


def _audit(request: Request, session: admin_auth.AdminSession, event: str, outcome: str, detail: str) -> None:
    try:
        config = admin_auth.AdminConfig.from_env()
        config.validate()
        admin_auth._audit(
            config,
            event=event,
            outcome=outcome,
            username=session.username,
            detail=detail[:500],
            client_key=admin_auth._client_key(request, config),
        )
    except Exception:
        # Publication integrity must not depend on the presentation of audit history.
        pass


def _raise(exc: Exception) -> None:
    if isinstance(exc, admin_drafts.DraftNotFound):
        raise HTTPException(404, str(exc)) from exc
    if isinstance(exc, admin_publication.PublicationDisabled):
        raise HTTPException(503, str(exc)) from exc
    if isinstance(exc, (admin_publication.PublicationConflict, admin_drafts.DraftConflict)):
        raise HTTPException(409, str(exc)) from exc
    if isinstance(exc, (admin_publication.PublicationError, admin_drafts.DraftError)):
        raise HTTPException(400, str(exc)) from exc
    raise exc


@assets.get("/admin/drafts.js")
def step9_admin_loader():
    _admin_enabled()
    return Response(
        'import "/admin/drafts-core.js";\nimport "/admin/replacement.js";\nimport "/admin/publication.js";\n',
        media_type="text/javascript",
        headers={"Cache-Control": "no-store"},
    )


@assets.get("/admin", response_class=HTMLResponse)
@assets.get("/admin/", response_class=HTMLResponse)
def step9_admin_shell():
    _admin_enabled()
    html = ADMIN_INDEX.read_text(encoding="utf-8")
    loader = '<script type="module" src="/admin/publication.js"></script>'
    if loader not in html:
        html = html.replace("</body>", f"  {loader}\n</body>")
    return HTMLResponse(html)


@router.get("/status")
def status(request: Request):
    _owner(request)
    return admin_publication.publication_status()


@router.get("/eligible")
def eligible(request: Request):
    _owner(request)
    try:
        return admin_publication.eligible_drafts()
    except Exception as exc:
        _raise(exc)


@router.get("/candidates")
def candidates(request: Request, limit: int = 100):
    _owner(request)
    try:
        return admin_publication.list_candidates(limit=limit)
    except Exception as exc:
        _raise(exc)


@router.get("/candidates/{candidate_id}")
def candidate(candidate_id: str, request: Request):
    _owner(request)
    try:
        return admin_publication.get_candidate(candidate_id)
    except Exception as exc:
        _raise(exc)


@router.get("/candidates/{candidate_id}/summary", response_class=PlainTextResponse)
def candidate_summary(candidate_id: str, request: Request):
    _owner(request)
    try:
        return PlainTextResponse(admin_publication.release_summary(candidate_id))
    except Exception as exc:
        _raise(exc)


@router.post("/candidates")
def create_candidate(payload: CandidateRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        result = admin_publication.create_candidate(
            payload.draft_ids,
            title=payload.title,
            notes=payload.notes,
            warnings_acknowledged=payload.warnings_acknowledged,
            username=session.username,
        )
        _audit(request, session, "publication_candidate", "success", f"created {result['candidate_id']}")
        return result
    except Exception as exc:
        _audit(request, session, "publication_candidate", "failure", str(exc))
        _raise(exc)


@router.post("/candidates/{candidate_id}/validate")
def validate_candidate(candidate_id: str, request: Request):
    session = _owner(request, csrf=True)
    try:
        result = admin_publication.validate_candidate(candidate_id)
        outcome = "success" if result.get("status") == "validated" else "failure"
        _audit(request, session, "publication_validation", outcome, f"{candidate_id} → {result.get('status')}")
        return result
    except Exception as exc:
        _audit(request, session, "publication_validation", "failure", str(exc))
        _raise(exc)


@router.post("/candidates/{candidate_id}/submit")
def submit_candidate(candidate_id: str, request: Request):
    session = _owner(request, csrf=True)
    try:
        result = admin_publication.submit_candidate(candidate_id)
        _audit(request, session, "publication_submit", "success", f"submitted {candidate_id} as PR {result['github'].get('pr_number')}")
        return result
    except Exception as exc:
        _audit(request, session, "publication_submit", "failure", str(exc))
        _raise(exc)


@router.post("/candidates/{candidate_id}/checks")
def refresh_checks(candidate_id: str, request: Request):
    session = _owner(request, csrf=True)
    try:
        result = admin_publication.refresh_github_checks(candidate_id)
        _audit(request, session, "publication_checks", "success", f"refreshed checks for {candidate_id}")
        return result
    except Exception as exc:
        _audit(request, session, "publication_checks", "failure", str(exc))
        _raise(exc)


@router.post("/candidates/{candidate_id}/merge")
def merge_candidate(candidate_id: str, request: Request):
    session = _owner(request, csrf=True)
    try:
        result = admin_publication.merge_candidate(candidate_id)
        _audit(request, session, "publication_merge", "success", f"merged {candidate_id}")
        return result
    except Exception as exc:
        _audit(request, session, "publication_merge", "failure", str(exc))
        _raise(exc)


@router.post("/candidates/{candidate_id}/verify")
def verify_candidate(candidate_id: str, request: Request):
    session = _owner(request, csrf=True)
    try:
        result = admin_publication.verify_release(candidate_id, username=session.username)
        _audit(request, session, "publication_verify", "success", f"verified {candidate_id} as {result['release_id']}")
        return result
    except Exception as exc:
        _audit(request, session, "publication_verify", "failure", str(exc))
        _raise(exc)


@router.get("/releases")
def releases(request: Request, limit: int = 100):
    _owner(request)
    try:
        return admin_publication.list_releases(limit=limit)
    except Exception as exc:
        _raise(exc)


@router.get("/releases/{release_id}")
def release(release_id: str, request: Request):
    _owner(request)
    try:
        return admin_publication.get_release(release_id)
    except Exception as exc:
        _raise(exc)


@router.post("/releases/{release_id}/rollback")
def rollback(release_id: str, payload: RollbackRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        result = admin_publication.create_rollback_candidate(
            release_id,
            title=payload.title,
            username=session.username,
        )
        _audit(request, session, "publication_rollback", "success", f"created rollback candidate {result['candidate_id']} from {release_id}")
        return result
    except Exception as exc:
        _audit(request, session, "publication_rollback", "failure", str(exc))
        _raise(exc)
