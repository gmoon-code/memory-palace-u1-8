from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "release" / "content-studio" / "v1.0.0.json"
RC1_LOCK = ROOT / "release" / "content-studio" / "v1.0.0-rc1.json"
VERSION = ROOT / "release" / "content-studio" / "VERSION"

EXPECTED_VERSION = "1.0.0"
EXPECTED_STABLE_BASELINE = "562f09e1d72f3bceaa3f97cf3b19d7683c864877"
EXPECTED_STABLE_TREE = "53e7182c271f0a82a473e527b0f2c77c16a4ae85"
EXPECTED_STABLE_PROMOTION = "4727a86b3670f0375b66191849e76c2912a40e46"
EXPECTED_STABLE_PROMOTION_TREE = "429332c7c465e98f46975499584e8be8b0045348"
EXPECTED_RC1_HEAD = "0fef459bde6fb913f186c91df8f5492f58f2fa9b"
EXPECTED_IMPLEMENTATION = "cdf4bb2a1ea91415dd1634323ac5ab40ccba863f"
EXPECTED_IMPLEMENTATION_TREE = "133a3bc9b00c2149662d4e6dba8517f0706b585c"
EXPECTED_PRE_INTEGRATION_MAIN = "6d561f19a19b07b9a386442d327db3ca12299bef"

ALLOWED_STABLE_EVIDENCE = {
    ".github/workflows/qa.yml",
    "docs/admin/CONTENT_STUDIO_V1_RELEASE.md",
    "release/content-studio/VERSION",
    "release/content-studio/v1.0.0.json",
    "scripts/qa_content_studio_release_candidate.py",
    "scripts/qa_content_studio_stable_release.py",
}

ALLOWED_POST_STABLE_MAINTENANCE = {
    "Backup Content Studio.cmd",
    "Restore Content Studio.cmd",
    "scripts/backup_content_studio_local.py",
    "scripts/qa_zero_cost_backup_restore.py",
    "scripts/qa_content_studio_release_candidate.py",
    "scripts/qa_content_studio_stable_release.py",
}

RUNTIME_PATHS = (
    "backend",
    "frontend/admin",
    "deploy/content-studio",
    "Start Content Studio.cmd",
    "Backup Content Studio.cmd",
    "Restore Content Studio.cmd",
    "Repair Content Studio.cmd",
    "Update Content Studio.cmd",
    ".env.example",
    "requirements.txt",
)

STUDENT_PATHS = (
    "content",
    "frontend/index.html",
    "frontend/css",
    "frontend/js",
)

KEY_OBJECTS = {
    "backend": "e50cc927229aaa04da05e9011242add339537993",
    "frontend/admin": "5ca9e35331d68bd156c4b596911c430ba9ec17c3",
    "frontend/js": "5df314588165696062ed431cba266154d8351ca5",
    ".env.example": "e9d3e685a128d5d827c2e576e947c10149f46c45",
    "Start Content Studio.cmd": "b097e7babef109ed20a6b927b47ded3d58e3731b",
    "Backup Content Studio.cmd": "5bcc9c28a78095057878bc2031cefe88dffd6bea",
    "Restore Content Studio.cmd": "da85a766c0d5abeeeb6ce8a7665bcad076da9233",
    "Repair Content Studio.cmd": "dbf331f485506da7f5fb4b8f43901f116b3fdd87",
    "Update Content Studio.cmd": "6801056db3ba6ff80b0a11efe0bd90965db05974",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"CONTENT STUDIO STABLE RELEASE QA FAIL\n- {message}")


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
    )


def git_text(*args: str) -> str:
    return git(*args).stdout.strip()


def main() -> None:
    require(LOCK.exists(), "stable release lock is missing")
    require(RC1_LOCK.exists(), "historical RC1 release lock is missing")
    require(VERSION.exists(), "release VERSION file is missing")
    require(VERSION.read_text(encoding="utf-8").strip() == EXPECTED_VERSION, "VERSION does not identify v1.0.0")

    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    rc1 = json.loads(RC1_LOCK.read_text(encoding="utf-8"))

    require(lock.get("version") == EXPECTED_VERSION, "stable lock version mismatch")
    require(lock.get("status") == "stable", "stable lock status is not stable")
    require(lock.get("release_scope") == "metadata-promotion-only", "stable release scope is not metadata-only")
    require(lock.get("stable_baseline_commit") == EXPECTED_STABLE_BASELINE, "stable baseline commit mismatch")
    require(lock.get("stable_baseline_tree") == EXPECTED_STABLE_TREE, "stable baseline tree mismatch")
    require(lock.get("source_rc1_head") == EXPECTED_RC1_HEAD, "RC1 source head mismatch")
    require(lock.get("frozen_implementation_commit") == EXPECTED_IMPLEMENTATION, "frozen implementation mismatch")
    require(lock.get("frozen_implementation_tree") == EXPECTED_IMPLEMENTATION_TREE, "frozen implementation tree mismatch")
    require(lock.get("pre_integration_main_commit") == EXPECTED_PRE_INTEGRATION_MAIN, "pre-integration main mismatch")
    require(lock.get("zero_cost_required") is True, "$0 requirement is not locked")

    require(rc1.get("version") == "1.0.0-rc1", "historical RC1 lock was altered")
    require(rc1.get("implementation_commit") == EXPECTED_IMPLEMENTATION, "historical RC1 implementation changed")
    require(rc1.get("implementation_tree") == EXPECTED_IMPLEMENTATION_TREE, "historical RC1 tree changed")

    stable_commit = git_text("rev-parse", f"{EXPECTED_STABLE_BASELINE}^{{commit}}")
    stable_tree = git_text("rev-parse", f"{EXPECTED_STABLE_BASELINE}^{{tree}}")
    require(stable_commit == EXPECTED_STABLE_BASELINE, "stable baseline commit cannot be resolved exactly")
    require(stable_tree == EXPECTED_STABLE_TREE, "stable baseline tree changed")
    require(git_text("rev-parse", f"{EXPECTED_RC1_HEAD}^{{tree}}") == EXPECTED_STABLE_TREE, "RC1 evidence tree differs from merged stable tree")
    require(git_text("rev-parse", f"{EXPECTED_IMPLEMENTATION}^{{tree}}") == EXPECTED_IMPLEMENTATION_TREE, "implementation tree changed")
    require(git_text("rev-parse", f"{EXPECTED_STABLE_PROMOTION}^{{tree}}") == EXPECTED_STABLE_PROMOTION_TREE, "stable promotion tree changed")

    parent_line = git_text("rev-list", "--parents", "-n", "1", EXPECTED_STABLE_BASELINE).split()
    require(len(parent_line) == 3, "stable integration commit is not a two-parent merge")
    require(parent_line[1] == EXPECTED_PRE_INTEGRATION_MAIN, "stable merge first parent is not the locked production baseline")
    require(parent_line[2] == EXPECTED_RC1_HEAD, "stable merge second parent is not the approved RC1 head")

    ancestor = git("merge-base", "--is-ancestor", EXPECTED_STABLE_PROMOTION, "HEAD", check=False)
    require(ancestor.returncode == 0, "stable promotion is not an ancestor of the current maintenance head")

    promotion_changes = {
        line.strip()
        for line in git_text("diff", "--name-only", f"{EXPECTED_STABLE_BASELINE}..{EXPECTED_STABLE_PROMOTION}").splitlines()
        if line.strip()
    }
    require(not sorted(promotion_changes - ALLOWED_STABLE_EVIDENCE), "v1.0.0 promotion contains non-evidence files")

    promotion_runtime_diff = git(
        "diff", "--quiet", EXPECTED_STABLE_BASELINE, EXPECTED_STABLE_PROMOTION, "--", *RUNTIME_PATHS, check=False
    )
    require(promotion_runtime_diff.returncode == 0, "administrator runtime changed during v1.0.0 promotion")

    maintenance_changes = {
        line.strip()
        for line in git_text("diff", "--name-only", f"{EXPECTED_STABLE_PROMOTION}..HEAD").splitlines()
        if line.strip()
    }
    unexpected_maintenance = sorted(maintenance_changes - ALLOWED_POST_STABLE_MAINTENANCE)
    require(not unexpected_maintenance, f"unexpected post-stable maintenance files: {unexpected_maintenance}")

    student_after_stable = git(
        "diff", "--quiet", EXPECTED_STABLE_PROMOTION, "HEAD", "--", *STUDENT_PATHS, check=False
    )
    require(student_after_stable.returncode == 0, "post-stable maintenance changed published curriculum or student frontend")

    student_diff = git(
        "diff", "--quiet", EXPECTED_PRE_INTEGRATION_MAIN, EXPECTED_STABLE_BASELINE, "--", *STUDENT_PATHS, check=False
    )
    require(student_diff.returncode == 0, "integration changed published curriculum or student frontend")

    for path, expected_object in KEY_OBJECTS.items():
        actual = git_text("rev-parse", f"{EXPECTED_STABLE_BASELINE}:{path}")
        require(actual == expected_object, f"stable runtime object mismatch for {path}: {actual}")

    env_text = git_text("show", "HEAD:.env.example")
    for gate in (
        "MEMORY_PALACE_ADMIN_ENABLED=false",
        "MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED=false",
        "MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED=false",
        "MEMORY_PALACE_GITHUB_ALLOW_MERGE=false",
    ):
        require(gate in env_text, f"default safety gate is not locked off: {gate}")

    validation = lock.get("post_merge_validation", {})
    require(validation.get("memory_palace_qa_run") == 354, "post-merge QA run identity changed")
    require(validation.get("memory_palace_qa_conclusion") == "success", "post-merge QA is not recorded as successful")
    require(validation.get("pages_run") == 98, "Pages validation run identity changed")
    require(validation.get("pages_conclusion") == "success", "Pages validation is not recorded as successful")
    require(validation.get("validated_commit") == EXPECTED_STABLE_BASELINE, "post-merge validation commit mismatch")

    print("CONTENT STUDIO STABLE RELEASE QA PASS")
    print(f"- version: {EXPECTED_VERSION}")
    print(f"- stable runtime baseline: {EXPECTED_STABLE_BASELINE}")
    print(f"- stable promotion commit: {EXPECTED_STABLE_PROMOTION}")
    print("- original v1.0.0 promotion remains metadata-only")
    print("- post-stable maintenance is restricted to the Windows backup/restore hotfix allowlist")
    print("- published AP Biology content and student frontend remain unchanged")
    print("- local $0 operation and publication-off defaults remain locked")


if __name__ == "__main__":
    main()
