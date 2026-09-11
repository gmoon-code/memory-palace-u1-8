from __future__ import annotations

import gzip
import http.client
import json
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = 'v2-apbio-0.30.0-u8-f6'


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def request(port: int, path: str, *, gzip_ok: bool = False):
    conn = http.client.HTTPConnection('127.0.0.1', port, timeout=8)
    headers = {'Accept': '*/*'}
    if gzip_ok:
        headers['Accept-Encoding'] = 'gzip'
    conn.request('GET', path, headers=headers)
    res = conn.getresponse()
    body = res.read()
    hdrs = {k.lower(): v for k, v in res.getheaders()}
    status = res.status
    conn.close()
    if hdrs.get('content-encoding') == 'gzip':
        body = gzip.decompress(body)
    return status, hdrs, body


def get_json(port: int, path: str):
    status, headers, body = request(port, path)
    if 'application/json' not in headers.get('content-type', ''):
        raise AssertionError(f'{path} did not return JSON: {headers.get("content-type")}')
    return status, headers, json.loads(body.decode('utf-8'))


port = free_port()
proc = subprocess.Popen(
    [sys.executable, '-m', 'uvicorn', 'backend.main:app', '--host', '127.0.0.1', '--port', str(port)],
    cwd=ROOT,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)
try:
    deadline = time.time() + 20
    last_error = None
    while time.time() < deadline:
        try:
            status, _, data = get_json(port, '/api/health')
            if status == 200 and data.get('ok'):
                break
        except Exception as exc:  # pragma: no cover - diagnostic wait loop
            last_error = exc
            time.sleep(0.2)
    else:
        output = proc.stdout.read() if proc.stdout else ''
        raise AssertionError(f'Uvicorn did not become ready: {last_error}\n{output}')

    status, api_headers, health = get_json(port, '/api/health')
    assert status == 200 and health['version'] == EXPECTED_VERSION
    assert api_headers.get('cache-control') == 'no-store'

    status, root_headers, root_body = request(port, '/', gzip_ok=True)
    root_text = root_body.decode('utf-8')
    assert status == 200 and 'text/html' in root_headers.get('content-type', '')
    assert 'class="skip-link"' in root_text and 'id="main-content"' in root_text
    assert root_headers.get('content-encoding') == 'gzip'

    security = {
        'content-security-policy': "default-src 'self'",
        'x-content-type-options': 'nosniff',
        'x-frame-options': 'DENY',
        'referrer-policy': 'no-referrer',
        'permissions-policy': 'camera=(), microphone=(), geolocation=()',
        'cross-origin-opener-policy': 'same-origin',
        'cross-origin-resource-policy': 'same-origin',
    }
    for header, required in security.items():
        actual = root_headers.get(header, '')
        assert required in actual, f'{header} missing or wrong: {actual}'
    assert root_headers.get('cache-control') == 'no-cache'

    status, static_headers, static_body = request(port, '/static/js/app.js', gzip_ok=True)
    assert status == 200 and b'nextUsefulJourney' in static_body
    assert static_headers.get('cache-control') == 'no-cache'
    assert 'javascript' in static_headers.get('content-type', '')

    # Developer schemas are intentionally unavailable on a student-facing deployment.
    for path in ['/docs', '/redoc', '/openapi.json']:
        status, _, _ = request(port, path)
        assert status == 404, f'{path} should be disabled'

    status, headers, data = get_json(port, '/api/definitely-not-a-route')
    assert status == 404 and data.get('detail') == 'API route not found'

    status, headers, body = request(port, '/student/deep/link')
    assert status == 200 and 'text/html' in headers.get('content-type', '') and b'Memory Palace' in body

    # A traversal request may resolve to the SPA shell or 404, but it must never disclose repository files.
    for path in ['/%2e%2e/requirements.txt', '/static/%2e%2e/requirements.txt', '/static/..%2Frequirements.txt']:
        status, headers, body = request(port, path)
        assert status in {200, 404}
        assert b'fastapi==0.116.1' not in body, f'Path traversal leaked requirements.txt through {path}'

    unit_count = journey_count = scene_count = challenge_count = 0
    for n in range(1, 9):
        unit_id = f'unit-{n}'
        status, _, u = get_json(port, f'/api/units/{unit_id}')
        assert status == 200 and u.get('status') == 'STUDENT_READY'
        unit_count += 1
        status, _, reg = get_json(port, f'/api/units/{unit_id}/journeys')
        assert status == 200
        for meta in reg['guided_journeys']:
            status, _, journey = get_json(port, f'/api/units/{unit_id}/journeys/{meta["palace_id"]}')
            assert status == 200
            assert len(journey['scenes']) == meta['scene_count']
            journey_count += 1
            scene_count += len(journey['scenes'])
        status, _, lab = get_json(port, f'/api/units/{unit_id}/application-lab')
        assert status == 200
        challenge_count += lab.get('challenge_count', 0)

    assert (unit_count, journey_count, scene_count, challenge_count) == (8, 58, 448, 112)

    print('SITE UX1 LIVE HTTP QA PASS')
    print(json.dumps({
        'runtime': EXPECTED_VERSION,
        'student_units': unit_count,
        'journeys_reached': journey_count,
        'scenes_reached': scene_count,
        'challenge_lab_items_reached': challenge_count,
        'gzip': True,
        'security_headers': True,
        'same_origin_isolation': True,
        'cache_policy': True,
        'developer_api_docs_disabled': True,
        'api_404_semantics': True,
        'spa_fallback': True,
        'path_traversal_protection': True,
    }, indent=2))
finally:
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=5)
