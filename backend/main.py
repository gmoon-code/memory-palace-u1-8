from pathlib import Path
import hmac

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import admin_auth, admin_catalog, admin_draft_routes, content, course_packages
from .settings import ADMIN_ENABLED, FRONTEND_DIR, HOST, PORT

RUNTIME_VERSION = "v2-apbio-0.30.0-u8-f6"
FRONTEND_ROOT = Path(FRONTEND_DIR).resolve()
ADMIN_ROOT = (FRONTEND_ROOT / "admin").resolve()

app = FastAPI(
    title="The Story Method · Science Courses",
    version="0.30.0-u8-f6",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
app.add_middleware(GZipMiddleware, minimum_size=500)
app.mount("/static", StaticFiles(directory=FRONTEND_ROOT), name="static")
app.include_router(admin_draft_routes.router)


class AdminLoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=128)
    password: str = Field(min_length=1, max_length=1024)


@app.middleware("http")
async def security_and_cache_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; "
        "base-uri 'self'; frame-ancestors 'none'; form-action 'self'"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    if request.url.path.startswith("/api/admin") or request.url.path.startswith("/admin"):
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Robots-Tag"] = "noindex, nofollow"
        response.headers["Vary"] = "Cookie"
    elif request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    elif request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "no-cache"
    else:
        response.headers["Cache-Control"] = "no-cache"
    return response


def _require_admin_enabled() -> None:
    if not ADMIN_ENABLED:
        raise HTTPException(404, "Not found")


def _configured_admin() -> admin_auth.AdminConfig:
    config = admin_auth.AdminConfig.from_env()
    try:
        config.validate()
    except admin_auth.AdminConfigurationError as exc:
        raise HTTPException(503, "Admin authentication is not configured") from exc
    return config


def _owner_session(request: Request, *, require_csrf: bool = False) -> admin_auth.AdminSession:
    _require_admin_enabled()
    session = admin_auth.get_session(request, require_csrf=require_csrf)
    if session.role != "owner":
        raise HTTPException(403, "Admin owner access required")
    return session


@app.get("/api/health")
def health():
    return {"ok": True, "version": RUNTIME_VERSION}


def _require_course_id(course_id: str) -> dict:
    try:
        return course_packages.course(course_id)
    except course_packages.CoursePackageError as exc:
        raise HTTPException(404, str(exc)) from exc


@app.get("/api/courses")
def list_courses():
    return content.course_registry()


@app.get("/api/courses/{course_id}")
def get_course_by_id(course_id: str):
    return _require_course_id(course_id)


@app.get("/api/course")
def get_course():
    return content.course()


@app.get("/api/units")
def list_units():
    return {"units": content.course()["units"]}


@app.get("/api/units/{unit_id}")
def get_unit(unit_id: str):
    item = content.unit_summary(unit_id)
    if not item:
        raise HTTPException(404, "Unit not found")
    return item


@app.get("/api/units/{unit_id}/architecture")
def get_architecture(unit_id: str):
    unit = content.unit_by_id(unit_id)
    if not unit:
        raise HTTPException(404, "Unit not found")
    if unit_id == "unit-2":
        return content.unit2_architecture()
    if unit_id == "unit-3":
        return content.unit3_architecture()
    if unit_id == "unit-4":
        return content.unit4_architecture()
    if unit_id == "unit-5":
        return content.unit5_architecture()
    if unit_id == "unit-6":
        return content.unit6_architecture()
    if unit_id == "unit-7":
        return content.unit7_architecture()
    if unit_id == "unit-8":
        return content.unit8_architecture()
    raise HTTPException(404, "Architecture artifact not exposed for this unit")


@app.get("/api/units/{unit_id}/scene-briefs")
def get_scene_briefs(unit_id: str):
    unit = content.unit_by_id(unit_id)
    if not unit:
        raise HTTPException(404, "Unit not found")
    if unit_id == "unit-2":
        return content.unit2_scene_briefs()
    if unit_id == "unit-3":
        return content.unit3_scene_briefs()
    if unit_id == "unit-4":
        return content.unit4_scene_briefs()
    if unit_id == "unit-5":
        return content.unit5_scene_briefs()
    if unit_id == "unit-6":
        return content.unit6_scene_briefs()
    if unit_id == "unit-7":
        return content.unit7_scene_briefs()
    if unit_id == "unit-8":
        return content.unit8_scene_briefs()
    raise HTTPException(404, "Scene briefs not exposed for this unit")


@app.get("/api/units/{unit_id}/journey-briefs")
def get_journey_briefs(unit_id: str):
    unit = content.unit_by_id(unit_id)
    if not unit:
        raise HTTPException(404, "Unit not found")
    if unit_id == "unit-2":
        return content.unit2_journey_briefs()
    if unit_id == "unit-3":
        return content.unit3_journey_briefs()
    if unit_id == "unit-4":
        return content.unit4_journey_briefs()
    if unit_id == "unit-5":
        return content.unit5_journey_briefs()
    if unit_id == "unit-6":
        return content.unit6_journey_briefs()
    if unit_id == "unit-7":
        return content.unit7_journey_briefs()
    if unit_id == "unit-8":
        return content.unit8_journey_briefs()
    raise HTTPException(404, "Journey briefs not exposed for this unit")


@app.get("/api/units/{unit_id}/journeys")
def list_journeys(unit_id: str):
    unit = content.unit_by_id(unit_id)
    if not unit:
        raise HTTPException(404, "Unit not found")
    return {"unit_id": unit_id, "guided_journeys": content.journey_registry(unit_id)}


@app.get("/api/units/{unit_id}/journeys/{palace_id}")
def get_journey(unit_id: str, palace_id: str):
    item = content.journey_by_id(unit_id, palace_id)
    if not item:
        raise HTTPException(404, "Journey not found")
    return item


@app.get("/api/units/{unit_id}/application-lab")
def get_application_lab(unit_id: str):
    unit = content.unit_by_id(unit_id)
    if not unit:
        raise HTTPException(404, "Unit not found")
    if unit_id == "unit-1":
        return content.application_lab()
    if unit_id == "unit-2":
        return content.unit2_application_lab()
    if unit_id == "unit-3":
        return content.unit3_application_lab()
    if unit_id == "unit-4":
        return content.unit4_application_lab()
    if unit_id == "unit-5":
        return content.unit5_application_lab()
    if unit_id == "unit-6":
        return content.unit6_application_lab()
    if unit_id == "unit-7":
        return content.unit7_application_lab()
    if unit_id == "unit-8":
        return content.unit8_application_lab()
    return {"unit_id": unit_id, "title": "Application Lab", "challenge_count": 0, "items": []}


@app.get("/api/units/{unit_id}/review-manifest")
def get_review_manifest(unit_id: str):
    unit = content.unit_by_id(unit_id)
    if not unit:
        raise HTTPException(404, "Unit not found")
    if unit_id == "unit-2":
        return content.unit2_review_manifest()
    if unit_id == "unit-3":
        return content.unit3_review_manifest()
    if unit_id == "unit-4":
        return content.unit4_review_manifest()
    if unit_id == "unit-5":
        return content.unit5_review_manifest()
    if unit_id == "unit-6":
        return content.unit6_review_manifest()
    if unit_id == "unit-7":
        return content.unit7_review_manifest()
    if unit_id == "unit-8":
        return content.unit8_review_manifest()
    return {"unit_id": unit_id, "target_count": 0, "targets": []}


@app.get("/api/units/{unit_id}/mixed-discrimination")
def get_mixed_discrimination(unit_id: str):
    unit = content.unit_by_id(unit_id)
    if not unit:
        raise HTTPException(404, "Unit not found")
    if unit_id == "unit-2":
        return content.unit2_mixed_discrimination()
    if unit_id == "unit-3":
        return content.unit3_mixed_discrimination()
    if unit_id == "unit-4":
        return content.unit4_mixed_discrimination()
    if unit_id == "unit-5":
        return content.unit5_mixed_discrimination()
    if unit_id == "unit-6":
        return content.unit6_mixed_discrimination()
    if unit_id == "unit-7":
        return content.unit7_mixed_discrimination()
    if unit_id == "unit-8":
        return content.unit8_mixed_discrimination()
    return {"unit_id": unit_id, "set_count": 0, "question_count": 0, "sets": []}


@app.get("/api/units/{unit_id}/finalization")
def get_finalization(unit_id: str):
    unit = content.unit_by_id(unit_id)
    if not unit:
        raise HTTPException(404, "Unit not found")
    if unit_id == "unit-2":
        return content.unit2_finalization()
    if unit_id == "unit-3":
        return content.unit3_finalization()
    if unit_id == "unit-4":
        return content.unit4_finalization()
    if unit_id == "unit-5":
        return content.unit5_finalization()
    if unit_id == "unit-6":
        return content.unit6_finalization()
    if unit_id == "unit-7":
        return content.unit7_finalization()
    if unit_id == "unit-8":
        return content.unit8_finalization()
    raise HTTPException(404, "Finalization artifact not exposed for this unit")


@app.get("/api/units/{unit_id}/scope-guards")
def get_scope_guards(unit_id: str):
    unit = content.unit_by_id(unit_id)
    if not unit:
        raise HTTPException(404, "Unit not found")
    if unit_id == "unit-3":
        return content.unit3_scope_guards()
    if unit_id == "unit-4":
        return content.unit4_scope_guards()
    if unit_id == "unit-5":
        return content.unit5_scope_guards()
    if unit_id == "unit-6":
        return content.unit6_scope_guards()
    if unit_id == "unit-7":
        return content.unit7_scope_guards()
    if unit_id == "unit-8":
        return content.unit8_scope_guards()
    return {"unit_id": unit_id, "guard_count": 0, "guards": []}


@app.get("/api/units/{unit_id}/objects/{object_id}")
def get_object(unit_id: str, object_id: str):
    item = content.object_index(unit_id).get(object_id)
    if not item:
        raise HTTPException(404, "Memory Object not found")
    return item


# Course-aware student routes. AP Biology remains available through the
# original routes during migration so existing links and tests keep working.
@app.get("/api/courses/{course_id}/units")
def list_course_units(course_id: str):
    course_item = _require_course_id(course_id)
    return {"course_id": course_id, "units": course_item.get("units", [])}


@app.get("/api/courses/{course_id}/units/{unit_id}")
def get_course_unit(course_id: str, unit_id: str):
    _require_course_id(course_id)
    item = course_packages.unit(course_id, unit_id)
    if not item:
        raise HTTPException(404, "Unit not found")
    return item


@app.get("/api/courses/{course_id}/units/{unit_id}/journeys")
def list_course_journeys(course_id: str, unit_id: str):
    _require_course_id(course_id)
    try:
        return course_packages.journeys(course_id, unit_id)
    except course_packages.CoursePackageError as exc:
        raise HTTPException(404, str(exc)) from exc


@app.get("/api/courses/{course_id}/units/{unit_id}/journeys/{palace_id}")
def get_course_journey(course_id: str, unit_id: str, palace_id: str):
    _require_course_id(course_id)
    try:
        item = course_packages.journey(course_id, unit_id, palace_id)
    except course_packages.CoursePackageError as exc:
        raise HTTPException(404, str(exc)) from exc
    if not item:
        raise HTTPException(404, "Journey not found")
    return item


@app.get("/api/courses/{course_id}/units/{unit_id}/application-lab")
def get_course_application_lab(course_id: str, unit_id: str):
    _require_course_id(course_id)
    try:
        return course_packages.application_lab(course_id, unit_id)
    except course_packages.CoursePackageError as exc:
        raise HTTPException(404, str(exc)) from exc


@app.get("/api/courses/{course_id}/units/{unit_id}/review-manifest")
def get_course_review_manifest(course_id: str, unit_id: str):
    _require_course_id(course_id)
    try:
        return course_packages.review_manifest(course_id, unit_id)
    except course_packages.CoursePackageError as exc:
        raise HTTPException(404, str(exc)) from exc


@app.get("/api/courses/{course_id}/units/{unit_id}/mixed-discrimination")
def get_course_mixed_discrimination(course_id: str, unit_id: str):
    _require_course_id(course_id)
    try:
        return course_packages.mixed_discrimination(course_id, unit_id)
    except course_packages.CoursePackageError as exc:
        raise HTTPException(404, str(exc)) from exc


@app.get("/api/courses/{course_id}/units/{unit_id}/objects/{object_id}")
def get_course_object(course_id: str, unit_id: str, object_id: str):
    _require_course_id(course_id)
    try:
        item = course_packages.memory_object(course_id, unit_id, object_id)
    except course_packages.CoursePackageError as exc:
        raise HTTPException(404, str(exc)) from exc
    if not item:
        raise HTTPException(404, "Memory Object not found")
    return item


# Temporary Unit 1 compatibility routes for the original V2 starter.
@app.get("/api/unit-1/summary")
def unit1_summary():
    return content.unit_summary("unit-1")


@app.get("/api/unit-1/journeys")
def unit1_journeys():
    return {"guided_journeys": content.journey_registry("unit-1")}


@app.get("/api/unit-1/journeys/{palace_id}")
def unit1_journey(palace_id: str):
    item = content.journey_by_id("unit-1", palace_id)
    if not item:
        raise HTTPException(404, "Journey not found")
    return item


@app.get("/api/unit-1/objects/{object_id}")
def unit1_object(object_id: str):
    item = content.object_index().get(object_id)
    if not item:
        raise HTTPException(404, "Memory Object not found")
    return item


# Content Studio security boundary. These APIs are separate from student read APIs.
@app.post("/api/admin/login")
def admin_login(payload: AdminLoginRequest, request: Request):
    _require_admin_enabled()
    config = _configured_admin()
    username = payload.username.strip()

    if not admin_auth.login_allowed(request, username, config):
        admin_auth.record_rate_limit(request, username, config)
        raise HTTPException(429, "Too many login attempts. Try again later.")

    username_ok = hmac.compare_digest(username, config.username)
    password_ok = admin_auth.verify_password(payload.password, config.password_hash)
    if not (username_ok and password_ok):
        admin_auth.record_login_failure(request, username, config)
        raise HTTPException(401, "Invalid username or password")

    session = admin_auth.create_session(request, config.username, config)
    response = JSONResponse(
        {
            "authenticated": True,
            "username": session.username,
            "role": session.role,
            "expires_at": session.expires_at,
            "csrf_token": session.csrf_token,
        }
    )
    response.set_cookie(
        key=admin_auth.SESSION_COOKIE,
        value=session.session_token,
        max_age=config.session_ttl_seconds,
        httponly=True,
        secure=config.secure_cookie,
        samesite="strict",
        path="/",
    )
    return response


@app.get("/api/admin/session")
def admin_session(request: Request):
    session = _owner_session(request)
    return {
        "authenticated": True,
        "username": session.username,
        "role": session.role,
        "expires_at": session.expires_at,
        "csrf_token": session.csrf_token,
    }


@app.post("/api/admin/logout")
def admin_logout(request: Request):
    session = _owner_session(request, require_csrf=True)
    config = _configured_admin()
    admin_auth.revoke_session(request, session)
    response = JSONResponse({"authenticated": False})
    response.delete_cookie(
        key=admin_auth.SESSION_COOKIE,
        path="/",
        secure=config.secure_cookie,
        httponly=True,
        samesite="strict",
    )
    return response


@app.get("/api/admin/courses")
def admin_courses(request: Request):
    _owner_session(request)
    return admin_catalog.catalog_courses()


@app.get("/api/admin/course")
def admin_course(request: Request, course_id: str = "ap-biology"):
    _owner_session(request)
    item = content.course_by_id(course_id)
    if not item:
        raise HTTPException(404, "Course not found")
    return item


@app.get("/api/admin/units/{unit_id}")
def admin_unit(unit_id: str, request: Request, course_id: str = "ap-biology"):
    _owner_session(request)
    try:
        admin_catalog.course_access(course_id)
        item = course_packages.unit(course_id, unit_id)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
    if not item:
        raise HTTPException(404, "Unit not found")
    return item


def _admin_catalog_call(function, *args, **kwargs):
    try:
        return function(*args, **kwargs)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc


@app.get("/api/admin/catalog/summary")
def admin_catalog_summary(request: Request, course_id: str = "ap-biology"):
    _owner_session(request)
    return _admin_catalog_call(admin_catalog.catalog_summary, course_id)


@app.get("/api/admin/catalog/course-map")
def admin_catalog_course_map(request: Request, course_id: str = "ap-biology"):
    _owner_session(request)
    return _admin_catalog_call(admin_catalog.course_map, course_id)


@app.get("/api/admin/catalog/entities")
def admin_catalog_entities(
    request: Request,
    course_id: str = "ap-biology",
    entity_type: str | None = None,
    unit_id: str | None = None,
    offset: int = 0,
    limit: int = 100,
):
    _owner_session(request)
    return _admin_catalog_call(
        admin_catalog.list_entities,
        course_id=course_id,
        entity_type=entity_type,
        unit_id=unit_id,
        offset=offset,
        limit=limit,
    )


@app.get("/api/admin/catalog/search")
def admin_catalog_search(
    request: Request,
    q: str,
    course_id: str = "ap-biology",
    unit_id: str | None = None,
    entity_type: str | None = None,
    limit: int = 50,
):
    _owner_session(request)
    if len(q.strip()) < 2:
        raise HTTPException(400, "Search query must contain at least 2 characters")
    return _admin_catalog_call(
        admin_catalog.search_entities,
        q,
        course_id=course_id,
        unit_id=unit_id,
        entity_type=entity_type,
        limit=limit,
    )


@app.get("/api/admin/catalog/resolve")
def admin_catalog_resolve(request: Request, unit_id: str, ref: str, course_id: str = "ap-biology"):
    _owner_session(request)
    return _admin_catalog_call(admin_catalog.resolve_reference, unit_id, ref, course_id)


@app.get("/api/admin/catalog/entity")
def admin_catalog_entity(request: Request, entity_id: str, course_id: str = "ap-biology"):
    _owner_session(request)
    item = _admin_catalog_call(admin_catalog.get_entity, entity_id, course_id)
    if item is None:
        raise HTTPException(404, "Catalog entity not found")
    return item


@app.get("/api/admin/catalog/dependencies")
def admin_catalog_dependencies(
    request: Request,
    entity_id: str,
    course_id: str = "ap-biology",
    depth: int = 2,
    limit: int = 500,
):
    _owner_session(request)
    item = _admin_catalog_call(admin_catalog.dependency_report, entity_id, course_id=course_id, depth=depth, limit=limit)
    if item is None:
        raise HTTPException(404, "Catalog entity not found")
    return item


@app.get("/api/admin/catalog/health")
def admin_catalog_health(request: Request, course_id: str = "ap-biology"):
    _owner_session(request)
    return _admin_catalog_call(admin_catalog.content_health, course_id)


@app.get("/api/admin/security")
def admin_security(request: Request):
    session = _owner_session(request)
    return {
        "session": {
            "username": session.username,
            "role": session.role,
            "expires_at": session.expires_at,
        },
        "protections": admin_auth.security_summary(),
    }


@app.get("/api/admin/audit")
def admin_audit(request: Request, limit: int = 50):
    _owner_session(request)
    return {"events": admin_auth.read_audit(limit)}


def _admin_file(path: str) -> Path | None:
    try:
        candidate = (ADMIN_ROOT / path).resolve()
        candidate.relative_to(ADMIN_ROOT)
    except (ValueError, OSError):
        return None
    return candidate if candidate.exists() and candidate.is_file() else None


@app.get("/admin")
@app.get("/admin/")
def admin_root():
    _require_admin_enabled()
    return FileResponse(ADMIN_ROOT / "index.html")


@app.get("/admin/{path:path}")
def admin_assets(path: str):
    _require_admin_enabled()
    candidate = _admin_file(path)
    if candidate is None:
        raise HTTPException(404, "Admin asset not found")
    return FileResponse(candidate)


@app.get("/")
def root():
    return FileResponse(FRONTEND_ROOT / "index.html")


def _safe_frontend_file(path: str) -> Path | None:
    try:
        candidate = (FRONTEND_ROOT / path).resolve()
        candidate.relative_to(FRONTEND_ROOT)
    except (ValueError, OSError):
        return None
    return candidate if candidate.exists() and candidate.is_file() else None


@app.get("/{path:path}")
def spa_fallback(path: str):
    if path == "api" or path.startswith("api/"):
        raise HTTPException(404, "API route not found")
    if path == "admin" or path.startswith("admin/"):
        raise HTTPException(404, "Not found")
    if path in {"docs", "redoc", "openapi.json"}:
        raise HTTPException(404, "Developer API documentation is disabled")
    candidate = _safe_frontend_file(path)
    if candidate is not None:
        return FileResponse(candidate)
    return FileResponse(FRONTEND_ROOT / "index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=True)
