# Content Studio Step 2 Security Release

Step 2 adds the security boundary required before any content editing capability is allowed.

The Content Studio remains disabled by default. When it is enabled, the teacher workspace now requires a configured username, scrypt password hash, and session secret. Successful login creates an opaque server-side session backed by SQLite in the ignored `server_data` directory. The browser receives only an HttpOnly session cookie and a session-specific CSRF token.

## Implemented protections

- Disabled-by-default admin switch
- Teacher login with scrypt password verification
- Server-side session storage
- Opaque random session tokens stored only as hashes in the database
- Eight-hour default session lifetime with configurable limits
- HttpOnly session cookie
- SameSite Strict session cookie
- Secure cookie outside development mode
- Session-specific CSRF token for protected actions
- Same-origin and Sec-Fetch-Site checks for protected actions
- Login throttling after repeated failures
- Client rate-limit keys derived through HMAC so raw client addresses are not persisted
- Server-side audit records for successful login, failed login, blocked login, CSRF failure, and logout
- Explicit owner role in the session model
- Protected `/api/admin/*` namespace separate from student read APIs
- Protected admin course and unit summary reads
- Security status and recent audit-event views inside Content Studio
- No content mutation endpoint
- No admin asset in the GitHub Pages student artifact

## Admin API surface in Step 2

Read operations

- `GET /api/admin/session`
- `GET /api/admin/course`
- `GET /api/admin/units/{unit_id}`
- `GET /api/admin/security`
- `GET /api/admin/audit`

Authentication operations

- `POST /api/admin/login`
- `POST /api/admin/logout`

The two POST routes manage authentication only. They do not modify AP Biology content.

## Configuration

The following environment variables are required before the admin workspace can authenticate.

```text
MEMORY_PALACE_ADMIN_ENABLED=true
MEMORY_PALACE_ADMIN_USERNAME=<teacher username>
MEMORY_PALACE_ADMIN_PASSWORD_HASH=<generated scrypt hash>
MEMORY_PALACE_ADMIN_SESSION_SECRET=<random secret of at least 32 characters>
```

The repository contains `scripts/generate_admin_credentials.py` to generate the password hash and session secret without storing the plaintext password.

Optional settings control session lifetime, login throttling, and the SQLite security database location. Real secrets must remain outside Git and are intentionally absent from `.env.example`.

## Security database

The default database is

`server_data/admin-security.sqlite3`

`server_data/*` is ignored by Git. The database contains server-side sessions, audit events, and login-failure counters. Raw passwords, raw session tokens, and raw client addresses are never stored.

## Content safety state

Step 2 deliberately does not create story, question, Memory Object, review, Challenge Lab, or publication write endpoints. The current student release remains authoritative.

The next implementation stage can therefore build the normalized eight-unit content catalog and dependency index behind an authenticated boundary without giving the browser direct access to production content files.
