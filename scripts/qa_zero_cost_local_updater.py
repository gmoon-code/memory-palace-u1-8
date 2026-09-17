from __future__ import annotations

from contextlib import contextmanager
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
UPDATER_PATH = ROOT / "scripts" / "update_content_studio_local.py"
CMD_PATH = ROOT / "Update Content Studio.cmd"


def fail(message: str) -> None:
    raise SystemExit(f"ZERO-COST LOCAL UPDATER QA FAIL: {message}")


def load_updater():
    spec = importlib.util.spec_from_file_location("content_studio_local_updater", UPDATER_PATH)
    if spec is None or spec.loader is None:
        fail("could not load updater module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(cwd: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        fail(f"git {' '.join(args)} failed: {completed.stderr.strip()}")
    return completed.stdout.strip()


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False


@contextmanager
def patched_urlopen(module, payload: dict):
    original = module.urllib.request.urlopen

    def fake_urlopen(request, timeout=0):
        del request, timeout
        return FakeResponse(json.dumps(payload).encode("utf-8"))

    module.urllib.request.urlopen = fake_urlopen
    try:
        yield
    finally:
        module.urllib.request.urlopen = original


def main() -> None:
    if not UPDATER_PATH.exists() or not CMD_PATH.exists():
        fail("updater script or Windows launcher is missing")

    source = UPDATER_PATH.read_text(encoding="utf-8")
    cmd = CMD_PATH.read_text(encoding="utf-8")
    required_source_markers = [
        'EXPECTED_REPOSITORY = "gmoon-code/memory-palace-u1-8"',
        'EXPECTED_WORKFLOW = "Memory Palace QA"',
        "require_clean_worktree",
        "require_content_studio_stopped",
        "merge-base",
        "--is-ancestor",
        "github_actions_approved",
        "create_state_backup",
        "write_recovery_record",
        "--ff-only",
        "rollback_code",
        '"reset", "--hard"',
        "qa_zero_cost_runtime.py",
        "qa_zero_cost_backup_restore.py",
    ]
    for marker in required_source_markers:
        if marker not in source:
            fail(f"updater safety marker is missing: {marker}")

    if '"pull"' in source or "git pull" in source.lower():
        fail("updater must not use an unconstrained git pull")
    if "render" in cmd.lower() or "railway" in cmd.lower():
        fail("Windows updater references a hosted deployment provider")
    if "paid service" not in cmd.lower() or "billing" not in cmd.lower():
        fail("Windows updater does not state the zero-cost boundary")

    updater = load_updater()
    if updater.ALLOWED_BRANCHES != {"admin/content-studio-local-updater", "main"}:
        fail("approved updater branches are broader than the locked release channels")
    for origin in updater.APPROVED_ORIGINS:
        if "github.com/gmoon-code/memory-palace-u1-8" not in origin:
            fail(f"unexpected approved origin: {origin}")

    updater.require_approved_branch("admin/content-studio-local-updater")
    updater.require_approved_branch("main")
    try:
        updater.require_approved_branch("feature/untrusted")
    except updater.UpdateError:
        pass
    else:
        fail("unapproved branch was accepted")

    with tempfile.TemporaryDirectory(prefix="content-studio-port-qa-") as temp_raw:
        env_file = Path(temp_raw) / "local.env"
        env_file.write_text("MEMORY_PALACE_PORT=8123\n", encoding="utf-8")
        if updater.local_port(env_file) != 8123:
            fail("local port parser did not honor the local Content Studio port")

    approved_payload = {
        "workflow_runs": [
            {
                "name": "Memory Palace QA",
                "head_sha": "a" * 40,
                "status": "completed",
                "conclusion": "success",
            }
        ]
    }
    with patched_urlopen(updater, approved_payload):
        if not updater.github_actions_approved("a" * 40):
            fail("successful exact-commit workflow was not accepted")
        if updater.github_actions_approved("b" * 40):
            fail("workflow for a different commit was accepted")

    rejected_payload = {
        "workflow_runs": [
            {
                "name": "Memory Palace QA",
                "head_sha": "c" * 40,
                "status": "completed",
                "conclusion": "failure",
            }
        ]
    }
    with patched_urlopen(updater, rejected_payload):
        if updater.github_actions_approved("c" * 40):
            fail("failed workflow was accepted")

    with tempfile.TemporaryDirectory(prefix="content-studio-updater-git-qa-") as temp_raw:
        repo = Path(temp_raw)
        git(repo, "init")
        git(repo, "config", "user.email", "qa@example.invalid")
        git(repo, "config", "user.name", "Content Studio QA")
        tracked = repo / "tracked.txt"
        tracked.write_text("version one\n", encoding="utf-8")
        git(repo, "add", "tracked.txt")
        git(repo, "commit", "-m", "version one")
        first_sha = git(repo, "rev-parse", "HEAD")
        tracked.write_text("version two\n", encoding="utf-8")
        git(repo, "add", "tracked.txt")
        git(repo, "commit", "-m", "version two")
        second_sha = git(repo, "rev-parse", "HEAD")
        git(repo, "reset", "--hard", first_sha)

        if not updater.is_ancestor(first_sha, second_sha, cwd=repo):
            fail("valid fast-forward relationship was rejected")
        updater.fast_forward_to(second_sha, cwd=repo)
        if git(repo, "rev-parse", "HEAD") != second_sha:
            fail("fast-forward helper did not move to the validated target")
        updater.rollback_code(first_sha, cwd=repo)
        if git(repo, "rev-parse", "HEAD") != first_sha:
            fail("automatic rollback helper did not restore the previous commit")
        if tracked.read_text(encoding="utf-8") != "version one\n":
            fail("automatic rollback did not restore the previous tracked files")

    print("ZERO-COST LOCAL UPDATER QA PASS")
    print("- updater is locked to the official repository and approved branches")
    print("- exact target commit requires successful Memory Palace QA")
    print("- only clean fast-forward updates are allowed")
    print("- Content Studio must be stopped before code changes")
    print("- safety backup and code recovery record are required")
    print("- real git fast-forward and automatic rollback behavior passed")
    print("- no paid hosting provider or billing workflow is introduced")


if __name__ == "__main__":
    main()
