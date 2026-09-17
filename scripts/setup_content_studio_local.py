from __future__ import annotations

import argparse
from getpass import getpass
import os
from pathlib import Path
import secrets

from backend.admin_auth import hash_password


DEFAULT_ENV_FILE = Path(".env.content-studio-local")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a local-only, zero-cost Content Studio environment file."
    )
    parser.add_argument(
        "--env-file",
        default=str(DEFAULT_ENV_FILE),
        help="Ignored local environment file to create",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing local environment file",
    )
    args = parser.parse_args()

    target = Path(args.env_file).expanduser().resolve()
    if target.exists() and not args.force:
        raise SystemExit(
            f"Refusing to replace existing credentials at {target}. Use --force only if you intend to rotate them."
        )

    username = input("Content Studio owner username [admin]: ").strip() or "admin"
    password = getpass("Content Studio owner password: ")
    confirm = getpass("Confirm password: ")
    if not password:
        raise SystemExit("Password cannot be empty.")
    if password != confirm:
        raise SystemExit("Passwords do not match.")
    if len(password) < 12:
        raise SystemExit("Use an owner password with at least 12 characters.")

    password_hash = hash_password(password)
    session_secret = secrets.token_urlsafe(48)

    server_data = Path("server_data").resolve()
    server_data.mkdir(parents=True, exist_ok=True)

    values = {
        "MEMORY_PALACE_ENV": "development",
        "MEMORY_PALACE_HOST": "127.0.0.1",
        "MEMORY_PALACE_PORT": "8000",
        "MEMORY_PALACE_ADMIN_ENABLED": "true",
        "MEMORY_PALACE_ADMIN_USERNAME": username,
        "MEMORY_PALACE_ADMIN_PASSWORD_HASH": password_hash,
        "MEMORY_PALACE_ADMIN_SESSION_SECRET": session_secret,
        "MEMORY_PALACE_ADMIN_DB": "server_data/admin-security.sqlite3",
        "MEMORY_PALACE_ADMIN_DRAFT_DB": "server_data/content-studio-drafts.sqlite3",
        "MEMORY_PALACE_ADMIN_MEDIA_DB": "server_data/content-studio-media.sqlite3",
        "MEMORY_PALACE_ADMIN_MEDIA_DIR": "server_data/content-studio-media",
        "MEMORY_PALACE_ADMIN_PUBLICATION_ENABLED": "false",
        "MEMORY_PALACE_ADMIN_PUBLICATION_DB": "server_data/content-studio-publication.sqlite3",
        "MEMORY_PALACE_ADMIN_PUBLICATION_DIR": "server_data/content-studio-publications",
        "MEMORY_PALACE_GITHUB_PUBLICATION_ENABLED": "false",
        "MEMORY_PALACE_GITHUB_ALLOW_MERGE": "false",
    }
    target.write_text(
        "# Local-only Content Studio configuration. Never commit this file.\n"
        + "\n".join(f"{key}={value}" for key, value in values.items())
        + "\n",
        encoding="utf-8",
    )
    try:
        os.chmod(target, 0o600)
    except OSError:
        pass

    print(f"Created local-only credentials at {target}")
    print(f"Persistent local state directory: {server_data}")
    print("Publication and GitHub publication remain disabled.")
    print("No hosting account, paid plan, billing method, or cloud service is required.")
    print("Start Content Studio with:")
    print(f"  python scripts/run_content_studio_local.py --env-file \"{target}\"")


if __name__ == "__main__":
    main()
