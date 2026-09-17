from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / "Start Content Studio.cmd"
BOOTSTRAP = ROOT / "scripts" / "bootstrap_content_studio_windows.py"
RUNNER = ROOT / "scripts" / "run_content_studio_local.py"
DOC = ROOT / "docs" / "admin" / "CONTENT_STUDIO_ZERO_COST_REHEARSAL.md"
GITIGNORE = ROOT / ".gitignore"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ZERO-COST WINDOWS LAUNCHER QA FAIL: {message}")


def main() -> None:
    for path in (LAUNCHER, BOOTSTRAP, RUNNER, DOC, GITIGNORE):
        require(path.exists(), f"missing {path.relative_to(ROOT)}")

    launcher = LAUNCHER.read_text(encoding="utf-8")
    bootstrap = BOOTSTRAP.read_text(encoding="utf-8")
    runner = RUNNER.read_text(encoding="utf-8")
    doc = DOC.read_text(encoding="utf-8")
    gitignore = GITIGNORE.read_text(encoding="utf-8")

    require("py -3" in launcher, "Windows launcher does not prefer the Python launcher")
    require("where python" in launcher, "Windows launcher lacks python fallback detection")
    require(
        "bootstrap_content_studio_windows.py" in launcher,
        "Windows launcher does not invoke the bootstrapper",
    )
    require("pause" in launcher.lower(), "Windows launcher does not preserve failure messages")

    require('VENV_DIR = ROOT / ".venv"' in bootstrap, "bootstrapper does not isolate dependencies")
    require('ENV_FILE = ROOT / ".env.content-studio-local"' in bootstrap, "bootstrapper does not use ignored local credentials")
    require("hashlib.sha256" in bootstrap, "requirements fingerprinting is missing")
    require('"-m",\n        "pip"' in bootstrap, "bootstrapper does not install Python requirements")
    require("setup_content_studio_local.py" in bootstrap, "first-run credential setup is missing")
    require("run_content_studio_local.py" in bootstrap, "local runner handoff is missing")
    require('"--open-browser"' in bootstrap, "one-click browser opening is not requested")

    require('os.environ["MEMORY_PALACE_HOST"] = "127.0.0.1"' in runner, "runner is not locked to loopback")
    require('os.environ["MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED"] = "false"' in runner, "publication safety lock is missing")
    require('os.environ["MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED"] = "false"' in runner, "GitHub publication safety lock is missing")
    require('os.environ["MEMORY_PALACE_GITHUB_ALLOW_MERGE"] = "false"' in runner, "merge safety lock is missing")
    require("ensure_loopback_port_available" in runner, "local port safety check is missing")
    require("open_browser_when_ready" in runner, "browser readiness wait is missing")

    require(".venv/" in gitignore, "virtual environment is not ignored")
    require(".env.*" in gitignore, "local environment secrets are not ignored")
    require("server_data/*" in gitignore, "local Content Studio state is not ignored")

    require("Start Content Studio.cmd" in doc, "documentation does not describe one-click Windows start")
    require("double-click" in doc.lower(), "documentation does not explain the one-click workflow")

    forbidden_paid_markers = (
        "render.com",
        "railway.app",
        "fly.io",
        "heroku.com",
        "stripe",
        "credit card",
    )
    combined_runtime = (launcher + "\n" + bootstrap + "\n" + runner).lower()
    for marker in forbidden_paid_markers:
        require(marker not in combined_runtime, f"paid-service marker present in local runtime: {marker}")

    print("ZERO-COST WINDOWS LAUNCHER QA PASS")
    print("- double-click Windows launcher present")
    print("- private virtual environment is created locally")
    print("- dependencies install only when requirements change")
    print("- first-run owner credentials remain local and ignored")
    print("- browser opens only after loopback Content Studio responds")
    print("- publication and merge remain forced off")
    print("- no paid hosting or billing integration is present")


if __name__ == "__main__":
    main()
