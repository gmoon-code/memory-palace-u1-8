from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import content
from .settings import ADMIN_ENABLED, FRONTEND_DIR, HOST, PORT

RUNTIME_VERSION = "v2-apbio-0.30.0-u8-f6"
FRONTEND_ROOT = Path(FRONTEND_DIR).resolve()
ADMIN_ROOT = (FRONTEND_ROOT / "admin").resolve()

app = FastAPI(
    title="Memory Palace V2 · AP Biology",
    version="0.30.0-u8-f6",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
app.add_middleware(GZipMiddleware, minimum_size=500)
app.mount("/static", StaticFiles(directory=FRONTEND_ROOT), name="static")


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
    if request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store"
    elif request.url.path.startswith("/static/") or request.url.path.startswith("/admin"):
        response.headers["Cache-Control"] = "no-cache"
    else:
        response.headers["Cache-Control"] = "no-cache"
    return response


@app.get("/api/health")
def health():
    return {"ok": True, "version": RUNTIME_VERSION}


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
    if not ADMIN_ENABLED:
        raise HTTPException(404, "Not found")
    return FileResponse(ADMIN_ROOT / "index.html")


@app.get("/admin/{path:path}")
def admin_assets(path: str):
    if not ADMIN_ENABLED:
        raise HTTPException(404, "Not found")
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
