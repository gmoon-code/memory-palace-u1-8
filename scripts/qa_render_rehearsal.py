from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"CONTENT STUDIO RENDER REHEARSAL QA FAIL - {message}")


def main() -> None:
    blueprint_path = ROOT / "render.yaml"
    dockerfile_path = ROOT / "deploy" / "content-studio" / "Dockerfile"
    guide_path = ROOT / "docs" / "admin" / "CONTENT_STUDIO_RENDER_REHEARSAL.md"

    require(blueprint_path.is_file(), "render.yaml is missing")
    require(dockerfile_path.is_file(), "Content Studio Dockerfile is missing")
    require(guide_path.is_file(), "Render rehearsal guide is missing")

    blueprint = blueprint_path.read_text(encoding="utf-8")
    dockerfile = dockerfile_path.read_text(encoding="utf-8")
    guide = guide_path.read_text(encoding="utf-8")

    required_blueprint_fragments = [
        "name: story-method-content-studio-rehearsal",
        "runtime: docker",
        "branch: admin/content-studio-render-rehearsal",
        "region: singapore",
        "autoDeployTrigger: off",
        "dockerfilePath: ./deploy/content-studio/Dockerfile",
        "dockerContext: .",
        "healthCheckPath: /api/health",
        "numInstances: 1",
        "mountPath: /app/server_data",
        "sizeGB: 1",
        "MEMORY_PALACE_ADMIN_ENABLED",
        'value: "true"',
        "MEMORY_PALACE_ADMIN_PASSWORD_HASH",
        "sync: false",
        "MEMORY_PALACE_ADMIN_SESSION_SECRET",
        "generateValue: true",
        "MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED",
        "MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED",
        "MEMORY_PALACE_GITHUB_ALLOW_MERGE",
    ]
    for fragment in required_blueprint_fragments:
        require(fragment in blueprint, f"Blueprint missing {fragment!r}")

    require("MEMORY_PALACE_GITHUB_TOKEN" not in blueprint, "GitHub token must not be requested during rehearsal")
    require("PASSWORD=" not in blueprint, "Plaintext password-like value found in Blueprint")
    require("PASSWORD_HASH=\n" not in blueprint, "Password hash must be supplied as a Render secret prompt")

    false_gate_blocks = [
        "MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED",
        "MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED",
        "MEMORY_PALACE_GITHUB_ALLOW_MERGE",
    ]
    for key in false_gate_blocks:
        marker = f"- key: {key}\n        value: \"false\""
        require(marker in blueprint, f"{key} must remain false in rehearsal")

    require("${PORT:-8000}" in dockerfile, "Container command must honor platform PORT")
    require("os.getenv('PORT', '8000')" in dockerfile, "Container health check must honor platform PORT")
    require("USER app" in dockerfile, "Container must run as non-root app user")

    require("publication remains disabled" in guide.lower(), "Guide must state publication stays disabled")
    require("persistent" in guide.lower() and "/app/server_data" in guide, "Guide must cover persistent disk storage")
    require("smoke_content_studio.py" in guide, "Guide must document authenticated smoke test")

    print("CONTENT STUDIO RENDER REHEARSAL QA PASS")
    print("- Render Blueprint is pinned to the isolated rehearsal branch")
    print("- Singapore Docker web service uses one persistent /app/server_data disk")
    print("- Admin authentication is enabled while all publication gates stay closed")
    print("- Secrets remain outside Git and the session secret is platform-generated")
    print("- Container startup and health checks honor the hosting platform PORT")


if __name__ == "__main__":
    main()
