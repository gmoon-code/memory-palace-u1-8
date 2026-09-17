from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from . import admin_auth, admin_capabilities
from .settings import ADMIN_ENABLED

router = APIRouter(prefix="/api/admin/capabilities", tags=["content-studio-capabilities"])


def _owner(request: Request) -> admin_auth.AdminSession:
    if not ADMIN_ENABLED:
        raise HTTPException(404, "Not found")
    session = admin_auth.get_session(request)
    if session.role != "owner":
        raise HTTPException(403, "Admin owner access required")
    return session


@router.get("")
def capability_audit(request: Request):
    _owner(request)
    return admin_capabilities.capability_audit()
