from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SETUP = ROOT / "scripts" / "setup_content_studio_local.py"
RUNNER = ROOT / "scripts" / "run_content_studio_local.py"
DOC = ROOT / "docs" / "admin" / "CONTENT_STUDIO_ZERO_COST_REHEARSAL.md"
GITIGNORE = ROOT / ".gitignore"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"ZERO-COST CONTENT STUDIO QA FAIL: {message}")


def main() -> None:
    for path in (SETUP, RUNNER, DOC, GITIGNORE):
        require(path.exists(), f"missing {path.relative_to(ROOT)}")

    setup = SETUP.read_text(encoding="utf-8")
    runner = RUNNER.read_text(encoding="utf-8")
    doc = DOC.read_text(encoding="utf-8")
    gitignore = GITIGNORE.read_text(encoding="utf-8")

    require('getpass("Content Studio owner password: ")' in setup, "credential setup must use hidden password input")
    require("hash_password(password)" in setup, "credential setup must store a password hash")
    require("secrets.token_urlsafe" in setup, "credential setup must generate a random session secret")
    require("os.chmod(target, 0o600)" in setup, "credential file should request owner-only permissions")
    require('"MEMORY_PALACE_HOST": "127.0.0.1"' in setup, "setup must default to loopback")
    require('"MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED": "false"' in setup, "setup must disable publication")
    require('"MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED": "false"' in setup, "setup must disable GitHub publication")
    require('"MEMORY_PALACE_GITHUB_ALLOW_MERGE": "false"' in setup, "setup must disable merge")

    require('os.environ["MEMORY_PALACE_HOST"] = "127.0.0.1"' in runner, "runner must force loopback")
    require('host="127.0.0.1"' in runner, "uvicorn must bind only to loopback")
    require('os.environ["MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED"] = "false"' in runner, "runner must force publication off")
    require('os.environ["MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED"] = "false"' in runner, "runner must force GitHub publication off")
    require('os.environ["MEMORY_PALACE_GITHUB_ALLOW_MERGE"] = "false"' in runner, "runner must force merge off")

    require(".env.*" in gitignore, "local credential files must be ignored")
    require("server_data/*" in gitignore, "local persistent state must be ignored")
    require("no paid hosting service" in doc.lower(), "documentation must state the zero-cost boundary")
    require("127.0.0.1" in doc, "documentation must describe local-only network binding")
    require("payment method" in doc.lower(), "documentation must exclude payment-method requirements")

    # The clean zero-cost rehearsal branch must not introduce provider blueprints.
    require(not (ROOT / "render.yaml").exists(), "paid-persistence Render blueprint must not be present")
    require(not (ROOT / "railway.toml").exists(), "cloud-provider blueprint must not be present")

    print("ZERO-COST CONTENT STUDIO QA PASS")
    print("- local owner credentials are generated without storing plaintext passwords")
    print("- server binds only to 127.0.0.1")
    print("- local state persists under ignored server_data")
    print("- publication, GitHub delivery, and merge are forced off")
    print("- no paid-hosting blueprint is present")


if __name__ == "__main__":
    main()
