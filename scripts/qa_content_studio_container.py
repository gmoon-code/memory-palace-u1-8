from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

BASE = os.getenv("CONTENT_STUDIO_CONTAINER_URL", "http://127.0.0.1:8765").rstrip("/")


def get(path: str) -> tuple[int, str]:
    request = urllib.request.Request(f"{BASE}{path}", headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            return response.status, response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace")


def main() -> None:
    last: tuple[int, str] | None = None
    for _ in range(30):
        try:
            last = get("/api/health")
            if last[0] == 200:
                break
        except OSError:
            pass
        time.sleep(1)
    if last is None or last[0] != 200:
        raise SystemExit(f"CONTENT STUDIO CONTAINER QA FAIL: health endpoint did not become ready: {last}")

    health = json.loads(last[1])
    if health.get("ok") is not True:
        raise SystemExit(f"CONTENT STUDIO CONTAINER QA FAIL: invalid health payload: {health}")

    admin_status, _ = get("/admin")
    if admin_status != 404:
        raise SystemExit(f"CONTENT STUDIO CONTAINER QA FAIL: default container exposed /admin with HTTP {admin_status}")

    session_status, _ = get("/api/admin/session")
    if session_status != 404:
        raise SystemExit(
            "CONTENT STUDIO CONTAINER QA FAIL: default container exposed the admin API "
            f"with HTTP {session_status}"
        )

    print("CONTENT STUDIO CONTAINER QA PASS")
    print(f"- health endpoint ready at {BASE}")
    print("- /admin is disabled by default")
    print("- /api/admin is disabled by default")


if __name__ == "__main__":
    main()
