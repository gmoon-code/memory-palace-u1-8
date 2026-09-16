from __future__ import annotations

import argparse
import http.cookiejar
import json
import os
import ssl
import sys
import urllib.error
import urllib.request


def request_json(opener: urllib.request.OpenerDirector, url: str, *, method: str = "GET", payload: dict | None = None, headers: dict[str, str] | None = None) -> tuple[int, dict]:
    data = None
    merged = {"Accept": "application/json"}
    if headers:
        merged.update(headers)
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        merged["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, method=method, headers=merged)
    try:
        with opener.open(request, timeout=15) as response:
            raw = response.read().decode("utf-8")
            return response.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            body = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            body = {"raw": raw}
        return exc.code, body


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only deployment smoke test for The Story Method Content Studio")
    parser.add_argument("--url", default=os.getenv("CONTENT_STUDIO_URL", ""), help="HTTPS Content Studio base URL")
    parser.add_argument("--username", default=os.getenv("CONTENT_STUDIO_USERNAME", ""))
    parser.add_argument("--password", default=os.getenv("CONTENT_STUDIO_PASSWORD", ""))
    parser.add_argument("--allow-http-localhost", action="store_true", help="Allow HTTP only for localhost development smoke tests")
    args = parser.parse_args()

    base = args.url.strip().rstrip("/")
    if not base:
        raise SystemExit("Provide --url or CONTENT_STUDIO_URL")
    if not base.startswith("https://"):
        localhost = base.startswith("http://127.0.0.1") or base.startswith("http://localhost")
        if not (localhost and args.allow_http_localhost):
            raise SystemExit("Refusing non-HTTPS Content Studio URL")

    context = ssl.create_default_context()
    cookies = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookies),
        urllib.request.HTTPSHandler(context=context),
    )

    health_status, health = request_json(opener, f"{base}/api/health")
    if health_status != 200 or health.get("ok") is not True:
        raise SystemExit(f"Health check failed: HTTP {health_status} {health}")
    print(f"PASS health {health.get('version', 'unknown-version')}")

    if not args.username or not args.password:
        print("PASS public health only. Supply username and password for authenticated read-only checks.")
        return

    login_status, login = request_json(
        opener,
        f"{base}/api/admin/login",
        method="POST",
        payload={"username": args.username, "password": args.password},
    )
    if login_status != 200 or login.get("authenticated") is not True:
        raise SystemExit(f"Admin login failed: HTTP {login_status} {login}")
    csrf = login.get("csrf_token")
    if not csrf:
        raise SystemExit("Admin login did not return a CSRF token")
    print("PASS authenticated owner session")

    session_status, session = request_json(opener, f"{base}/api/admin/session")
    if session_status != 200 or session.get("authenticated") is not True or session.get("role") != "owner":
        raise SystemExit(f"Session check failed: HTTP {session_status} {session}")
    print("PASS session read")

    catalog_status, catalog = request_json(opener, f"{base}/api/admin/catalog/summary")
    if catalog_status != 200:
        raise SystemExit(f"Catalog summary failed: HTTP {catalog_status} {catalog}")
    print("PASS catalog read")

    publication_status_code, publication = request_json(opener, f"{base}/api/admin/publication/status")
    if publication_status_code not in {200, 503}:
        raise SystemExit(f"Publication status check failed: HTTP {publication_status_code} {publication}")
    print(f"PASS publication gate observable as HTTP {publication_status_code}")

    logout_status, logout = request_json(
        opener,
        f"{base}/api/admin/logout",
        method="POST",
        payload={},
        headers={"X-CSRF-Token": csrf},
    )
    if logout_status != 200 or logout.get("authenticated") is not False:
        raise SystemExit(f"Logout failed: HTTP {logout_status} {logout}")
    print("PASS CSRF-protected logout")

    post_logout_status, _ = request_json(opener, f"{base}/api/admin/session")
    if post_logout_status != 401:
        raise SystemExit(f"Revoked session remained usable: HTTP {post_logout_status}")
    print("PASS session revocation")
    print("CONTENT STUDIO DEPLOYMENT SMOKE PASS")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
