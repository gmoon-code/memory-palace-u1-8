from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import base64
import hashlib
import hmac
import os
from pathlib import Path
import secrets
import sqlite3
import time
from typing import Any

from fastapi import HTTPException, Request

from .settings import ENV, ROOT

SESSION_COOKIE = "mp_admin_session"
CSRF_HEADER = "x-csrf-token"
DEFAULT_SESSION_TTL_SECONDS = 8 * 60 * 60
DEFAULT_LOGIN_WINDOW_SECONDS = 10 * 60
DEFAULT_LOGIN_FAILURE_LIMIT = 5
SCRYPT_N = 16384
SCRYPT_R = 8
SCRYPT_P = 1
SCRYPT_DKLEN = 32


@dataclass(frozen=True)
class AdminConfig:
    username: str
    password_hash: str
    session_secret: str
    database_path: Path
    session_ttl_seconds: int
    login_window_seconds: int
    login_failure_limit: int
    secure_cookie: bool

    @classmethod
    def from_env(cls) -> "AdminConfig":
        username = os.getenv("MEMORY_PALACE_ADMIN_USERNAME", "").strip()
        password_hash = os.getenv("MEMORY_PALACE_ADMIN_PASSWORD_HASH", "").strip()
        session_secret = os.getenv("MEMORY_PALACE_ADMIN_SESSION_SECRET", "").strip()
        database_path = Path(
            os.getenv(
                "MEMORY_PALACE_ADMIN_DB",
                str(ROOT / "server_data" / "admin-security.sqlite3"),
            )
        ).expanduser()
        session_ttl_seconds = _bounded_int(
            os.getenv("MEMORY_PALACE_ADMIN_SESSION_TTL_SECONDS"),
            DEFAULT_SESSION_TTL_SECONDS,
            minimum=900,
            maximum=24 * 60 * 60,
        )
        login_window_seconds = _bounded_int(
            os.getenv("MEMORY_PALACE_ADMIN_LOGIN_WINDOW_SECONDS"),
            DEFAULT_LOGIN_WINDOW_SECONDS,
            minimum=60,
            maximum=60 * 60,
        )
        login_failure_limit = _bounded_int(
            os.getenv("MEMORY_PALACE_ADMIN_LOGIN_FAILURE_LIMIT"),
            DEFAULT_LOGIN_FAILURE_LIMIT,
            minimum=3,
            maximum=20,
        )
        secure_cookie = ENV != "development"
        return cls(
            username=username,
            password_hash=password_hash,
            session_secret=session_secret,
            database_path=database_path,
            session_ttl_seconds=session_ttl_seconds,
            login_window_seconds=login_window_seconds,
            login_failure_limit=login_failure_limit,
            secure_cookie=secure_cookie,
        )

    def validate(self) -> None:
        problems: list[str] = []
        if not self.username:
            problems.append("MEMORY_PALACE_ADMIN_USERNAME")
        if not self.password_hash:
            problems.append("MEMORY_PALACE_ADMIN_PASSWORD_HASH")
        elif not self.password_hash.startswith("scrypt$"):
            problems.append("MEMORY_PALACE_ADMIN_PASSWORD_HASH format")
        if len(self.session_secret) < 32:
            problems.append("MEMORY_PALACE_ADMIN_SESSION_SECRET")
        if problems:
            raise AdminConfigurationError(
                "Admin authentication is not fully configured. Missing or invalid: "
                + ", ".join(problems)
            )


@dataclass(frozen=True)
class AdminSession:
    username: str
    role: str
    csrf_token: str
    expires_at: int
    session_token: str


class AdminConfigurationError(RuntimeError):
    pass


def _bounded_int(raw: str | None, default: int, *, minimum: int, maximum: int) -> int:
    if raw is None or raw.strip() == "":
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return max(minimum, min(maximum, value))


def _b64_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _b64_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def hash_password(password: str, *, salt: bytes | None = None) -> str:
    if salt is None:
        salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        dklen=SCRYPT_DKLEN,
    )
    return f"scrypt${SCRYPT_N}${SCRYPT_R}${SCRYPT_P}${_b64_encode(salt)}${_b64_encode(digest)}"


def verify_password(password: str, encoded_hash: str) -> bool:
    try:
        algorithm, n_raw, r_raw, p_raw, salt_raw, digest_raw = encoded_hash.split("$", 5)
        if algorithm != "scrypt":
            return False
        n = int(n_raw)
        r = int(r_raw)
        p = int(p_raw)
        if n < 2**12 or n > 2**18 or r < 1 or r > 32 or p < 1 or p > 8:
            return False
        salt = _b64_decode(salt_raw)
        expected = _b64_decode(digest_raw)
        candidate = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=n,
            r=r,
            p=p,
            dklen=len(expected),
        )
        return hmac.compare_digest(candidate, expected)
    except (ValueError, TypeError, base64.binascii.Error):
        return False


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _client_key(request: Request, config: AdminConfig) -> str:
    host = request.client.host if request.client else "unknown"
    digest = hmac.new(
        config.session_secret.encode("utf-8"),
        host.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return digest[:24]


def _connect(config: AdminConfig) -> sqlite3.Connection:
    config.database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(config.database_path, timeout=5.0)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA foreign_keys=ON")
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS admin_sessions (
            session_hash TEXT PRIMARY KEY,
            username TEXT NOT NULL,
            role TEXT NOT NULL,
            csrf_hash TEXT NOT NULL,
            created_at INTEGER NOT NULL,
            expires_at INTEGER NOT NULL,
            last_seen_at INTEGER NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS admin_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            event TEXT NOT NULL,
            username TEXT,
            outcome TEXT NOT NULL,
            detail TEXT,
            client_key TEXT
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS admin_login_failures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_key TEXT NOT NULL,
            username_key TEXT NOT NULL,
            created_at INTEGER NOT NULL
        )
        """
    )
    connection.execute(
        "CREATE INDEX IF NOT EXISTS idx_admin_sessions_expiry ON admin_sessions(expires_at)"
    )
    connection.execute(
        "CREATE INDEX IF NOT EXISTS idx_admin_login_failures_lookup "
        "ON admin_login_failures(client_key, username_key, created_at)"
    )
    connection.commit()
    return connection


def _audit(
    config: AdminConfig,
    *,
    event: str,
    outcome: str,
    username: str | None = None,
    detail: str | None = None,
    client_key: str | None = None,
) -> None:
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with _connect(config) as connection:
        connection.execute(
            """
            INSERT INTO admin_audit(created_at, event, username, outcome, detail, client_key)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (created_at, event, username, outcome, detail, client_key),
        )
        connection.commit()


def _cleanup(config: AdminConfig, connection: sqlite3.Connection, now: int) -> None:
    connection.execute("DELETE FROM admin_sessions WHERE expires_at <= ?", (now,))
    connection.execute(
        "DELETE FROM admin_login_failures WHERE created_at < ?",
        (now - config.login_window_seconds,),
    )


def login_allowed(request: Request, username: str, config: AdminConfig) -> bool:
    now = int(time.time())
    client_key = _client_key(request, config)
    username_key = _sha256(username.strip().casefold())
    with _connect(config) as connection:
        _cleanup(config, connection, now)
        count = connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM admin_login_failures
            WHERE client_key = ? AND username_key = ? AND created_at >= ?
            """,
            (client_key, username_key, now - config.login_window_seconds),
        ).fetchone()["count"]
        connection.commit()
    return int(count) < config.login_failure_limit


def record_login_failure(request: Request, username: str, config: AdminConfig) -> None:
    now = int(time.time())
    client_key = _client_key(request, config)
    username_key = _sha256(username.strip().casefold())
    with _connect(config) as connection:
        _cleanup(config, connection, now)
        connection.execute(
            "INSERT INTO admin_login_failures(client_key, username_key, created_at) VALUES (?, ?, ?)",
            (client_key, username_key, now),
        )
        connection.commit()
    _audit(
        config,
        event="login",
        outcome="failure",
        username=username[:128],
        detail="invalid credentials",
        client_key=client_key,
    )


def clear_login_failures(request: Request, username: str, config: AdminConfig) -> None:
    client_key = _client_key(request, config)
    username_key = _sha256(username.strip().casefold())
    with _connect(config) as connection:
        connection.execute(
            "DELETE FROM admin_login_failures WHERE client_key = ? AND username_key = ?",
            (client_key, username_key),
        )
        connection.commit()


def create_session(request: Request, username: str, config: AdminConfig) -> AdminSession:
    now = int(time.time())
    expires_at = now + config.session_ttl_seconds
    session_token = secrets.token_urlsafe(32)
    csrf_token = secrets.token_urlsafe(32)
    with _connect(config) as connection:
        _cleanup(config, connection, now)
        connection.execute(
            """
            INSERT INTO admin_sessions(
                session_hash, username, role, csrf_hash, created_at, expires_at, last_seen_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                _sha256(session_token),
                username,
                "owner",
                _sha256(csrf_token),
                now,
                expires_at,
                now,
            ),
        )
        connection.commit()
    clear_login_failures(request, username, config)
    _audit(
        config,
        event="login",
        outcome="success",
        username=username,
        detail="owner session created",
        client_key=_client_key(request, config),
    )
    return AdminSession(
        username=username,
        role="owner",
        csrf_token=csrf_token,
        expires_at=expires_at,
        session_token=session_token,
    )


def get_session(request: Request, *, require_csrf: bool = False) -> AdminSession:
    config = AdminConfig.from_env()
    try:
        config.validate()
    except AdminConfigurationError as exc:
        raise HTTPException(503, "Admin authentication is not configured") from exc

    session_token = request.cookies.get(SESSION_COOKIE, "")
    if not session_token:
        raise HTTPException(401, "Admin authentication required")

    now = int(time.time())
    with _connect(config) as connection:
        _cleanup(config, connection, now)
        row = connection.execute(
            """
            SELECT username, role, csrf_hash, expires_at
            FROM admin_sessions
            WHERE session_hash = ? AND expires_at > ?
            """,
            (_sha256(session_token), now),
        ).fetchone()
        if row is None:
            connection.commit()
            raise HTTPException(401, "Admin session is invalid or expired")
        connection.execute(
            "UPDATE admin_sessions SET last_seen_at = ? WHERE session_hash = ?",
            (now, _sha256(session_token)),
        )
        connection.commit()

    csrf_token = request.headers.get(CSRF_HEADER, "") if require_csrf else ""
    if require_csrf:
        if not csrf_token or not hmac.compare_digest(_sha256(csrf_token), row["csrf_hash"]):
            _audit(
                config,
                event="csrf",
                outcome="failure",
                username=row["username"],
                detail="missing or invalid CSRF token",
                client_key=_client_key(request, config),
            )
            raise HTTPException(403, "CSRF validation failed")
        _validate_request_origin(request)

    return AdminSession(
        username=row["username"],
        role=row["role"],
        csrf_token=csrf_token,
        expires_at=int(row["expires_at"]),
        session_token=session_token,
    )


def _validate_request_origin(request: Request) -> None:
    sec_fetch_site = request.headers.get("sec-fetch-site", "")
    if sec_fetch_site and sec_fetch_site not in {"same-origin", "none"}:
        raise HTTPException(403, "Cross-site admin request rejected")
    origin = request.headers.get("origin")
    if origin:
        expected = f"{request.url.scheme}://{request.url.netloc}"
        if not hmac.compare_digest(origin.rstrip("/"), expected.rstrip("/")):
            raise HTTPException(403, "Admin request origin rejected")


def revoke_session(request: Request, session: AdminSession) -> None:
    config = AdminConfig.from_env()
    config.validate()
    with _connect(config) as connection:
        connection.execute(
            "DELETE FROM admin_sessions WHERE session_hash = ?",
            (_sha256(session.session_token),),
        )
        connection.commit()
    _audit(
        config,
        event="logout",
        outcome="success",
        username=session.username,
        detail="session revoked",
        client_key=_client_key(request, config),
    )


def read_audit(limit: int = 50) -> list[dict[str, Any]]:
    config = AdminConfig.from_env()
    config.validate()
    safe_limit = max(1, min(int(limit), 200))
    with _connect(config) as connection:
        rows = connection.execute(
            """
            SELECT id, created_at, event, username, outcome, detail
            FROM admin_audit
            ORDER BY id DESC
            LIMIT ?
            """,
            (safe_limit,),
        ).fetchall()
    return [dict(row) for row in rows]


def security_summary() -> dict[str, Any]:
    config = AdminConfig.from_env()
    config.validate()
    return {
        "authentication": "password+scrypt",
        "session_store": "server-side sqlite",
        "session_ttl_seconds": config.session_ttl_seconds,
        "csrf_protection": True,
        "same_site_cookie": "strict",
        "secure_cookie": config.secure_cookie,
        "role": "owner",
        "login_failure_limit": config.login_failure_limit,
        "login_window_seconds": config.login_window_seconds,
        "audit_log": True,
        "content_write_api": False,
    }
