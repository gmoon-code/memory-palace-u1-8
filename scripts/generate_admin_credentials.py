from __future__ import annotations

from getpass import getpass
import secrets

from backend.admin_auth import hash_password


def main() -> None:
    username = input("Admin username [admin]: ").strip() or "admin"
    password = getpass("Admin password: ")
    confirm = getpass("Confirm password: ")
    if not password:
        raise SystemExit("Password cannot be empty.")
    if password != confirm:
        raise SystemExit("Passwords do not match.")
    if len(password) < 12:
        raise SystemExit("Use an admin password with at least 12 characters.")

    password_hash = hash_password(password)
    session_secret = secrets.token_urlsafe(48)

    print("\nStore these as deployment environment variables. Do not commit real values.\n")
    print("MEMORY_PALACE_ADMIN_ENABLED=true")
    print(f"MEMORY_PALACE_ADMIN_USERNAME={username}")
    print(f"MEMORY_PALACE_ADMIN_PASSWORD_HASH={password_hash}")
    print(f"MEMORY_PALACE_ADMIN_SESSION_SECRET={session_secret}")


if __name__ == "__main__":
    main()
