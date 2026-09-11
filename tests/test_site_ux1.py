import hashlib
from pathlib import Path

from fastapi.testclient import TestClient

from backend.main import app
from scripts.site_release_guard import (
    CURRICULUM_RUNTIME,
    FROZEN_CONTENT_FILE_COUNT,
    FROZEN_CONTENT_TREE_SHA256,
    content_tree,
    load_site_lock,
    site_lock_is_valid,
)

ROOT = Path(__file__).resolve().parents[1]
client = TestClient(app)


def test_site_ux1_lock_preserves_frozen_curriculum_tree():
    count, digest = content_tree(ROOT)
    assert count == FROZEN_CONTENT_FILE_COUNT == 527
    assert digest == FROZEN_CONTENT_TREE_SHA256
    assert site_lock_is_valid(ROOT)
    lock = load_site_lock(ROOT)
    assert lock['curriculum_runtime_version'] == CURRICULUM_RUNTIME
    assert lock['curriculum_content_changed'] is False


def test_site_ux1_server_security_and_cache_contract():
    root = client.get('/')
    assert root.status_code == 200
    assert 'class="skip-link"' in root.text
    assert root.headers['x-content-type-options'] == 'nosniff'
    assert root.headers['x-frame-options'] == 'DENY'
    assert root.headers['referrer-policy'] == 'no-referrer'
    assert root.headers['cross-origin-opener-policy'] == 'same-origin'
    assert root.headers['cross-origin-resource-policy'] == 'same-origin'
    assert "default-src 'self'" in root.headers['content-security-policy']
    assert client.get('/api/health').headers['cache-control'] == 'no-store'
    assert client.get('/static/js/app.js').headers['cache-control'] == 'no-cache'


def test_site_ux1_disables_docs_and_protects_fallback_paths():
    assert client.get('/docs').status_code == 404
    assert client.get('/redoc').status_code == 404
    assert client.get('/openapi.json').status_code == 404
    bad = client.get('/api/definitely-not-real')
    assert bad.status_code == 404 and bad.json()['detail'] == 'API route not found'
    deep = client.get('/student/deep/link')
    assert deep.status_code == 200 and 'Memory Palace' in deep.text
    traversal = client.get('/%2e%2e/requirements.txt')
    assert 'fastapi==0.116.1' not in traversal.text


def test_site_ux1_frontend_accessibility_and_navigation_contracts():
    index = (ROOT / 'frontend/index.html').read_text(encoding='utf-8')
    base = (ROOT / 'frontend/css/base.css').read_text(encoding='utf-8')
    learn = (ROOT / 'frontend/js/views/learn.js').read_text(encoding='utf-8')
    practice = (ROOT / 'frontend/js/views/practice.js').read_text(encoding='utf-8')
    assert 'class="skip-link"' in index and 'href="#main-content"' in index
    assert ':focus-visible' in base and 'min-height:44px' in base and 'prefers-reduced-motion' in base
    assert 'Previous scene' in learn and 'aria-current="step"' in learn and 'role="progressbar"' in learn
    assert 'Previous challenge' in practice and 'Finish challenge lab' in practice


def test_site_ux1_state_and_retrieval_integrity_contracts():
    state = (ROOT / 'frontend/js/state.js').read_text(encoding='utf-8')
    appjs = (ROOT / 'frontend/js/app.js').read_text(encoding='utf-8')
    assert "activeJourney:null" in state and 'version:4' in state
    assert 'assistedRecalls' in state and 'ASSIST_TTL=2*HOUR' in state
    assert 'markRecallAssisted' in appjs and 'wasRecallAssisted' in appjs
    assert 'review-show-answer' in appjs and "recallOpen?skipRecallAndContinue():nextScene()" in appjs
    assert 'nextUsefulJourney' in appjs and 'previous-scene' in appjs and 'practice-previous' in appjs


def test_site_ux1_ci_uses_qa_gates_without_rebuilding_frozen_f6():
    workflow = (ROOT / '.github/workflows/qa.yml').read_text(encoding='utf-8')
    assert 'build_unit6_f6.py' not in workflow
    assert 'build_unit8_f6.py' not in workflow
    for token in ['build_site_ux1.py', 'qa_site_ux.mjs', 'qa_site_contrast.py', 'qa_site_http_live.py', 'build_site_ux1_release.py', 'git diff --exit-code']:
        assert token in workflow
