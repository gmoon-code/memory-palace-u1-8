from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field

from . import admin_auth, admin_health
from .settings import ADMIN_ENABLED

router = APIRouter(prefix="/api/admin/system-health", tags=["content-studio-system-health"])


class RepairRequest(BaseModel):
    action: str = Field(min_length=1, max_length=80)


def _owner(request: Request, *, csrf: bool = False) -> admin_auth.AdminSession:
    if not ADMIN_ENABLED:
        raise HTTPException(404, "Not found")
    session = admin_auth.get_session(request, require_csrf=csrf)
    if session.role != "owner":
        raise HTTPException(403, "Admin owner access required")
    return session


@router.get("")
def system_health(request: Request):
    _owner(request)
    return admin_health.health_report()


@router.post("/repair")
def system_health_repair(payload: RepairRequest, request: Request):
    session = _owner(request, csrf=True)
    try:
        result = admin_health.run_repair(payload.action)
    except admin_health.HealthRepairError as exc:
        try:
            config = admin_auth.AdminConfig.from_env()
            config.validate()
            admin_auth._audit(
                config,
                event="system_health_repair",
                outcome="failure",
                username=session.username,
                detail=f"{payload.action}: {exc}",
            )
        except Exception:
            pass
        raise HTTPException(400, str(exc)) from exc

    try:
        config = admin_auth.AdminConfig.from_env()
        config.validate()
        admin_auth._audit(
            config,
            event="system_health_repair",
            outcome="success",
            username=session.username,
            detail=payload.action,
        )
    except Exception:
        pass
    return result
