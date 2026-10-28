# Changelog

All notable changes to this package are recorded in this file. The package
follows [Semantic Versioning](https://semver.org); see "Versioning" in the
[README](README.md) for what counts as a breaking change.

## 1.0.0 (unreleased)

The first release under the `vaifstudio` name. It replaces `vaif-client`
(import name `vaif`), whose releases 0.1.0, 0.2.0 and 0.2.1 call routes the VAIF
Studio API does not serve and should not be used.

### Upgrading from `vaif-client`

- The distribution is `vaifstudio` and the import package is `vaifstudio`.
  Uninstall `vaif-client`, install `vaifstudio`, and replace `import vaif` and
  `from vaif import ...` with `import vaifstudio` and `from vaifstudio import ...`.
- The interface is new. Queries on `vaif.db.from_(...)` that end in `execute()`
  become queries on `vaif.from_(...)` that end in `list()`, `first()`, `get()`,
  `insert()`, `update()`, `delete()` or another method listed below.
  `vaif.storage.from_(bucket)` calls become `vaif.storage` calls with
  `bucket=`. The earlier realtime client is replaced by
  `vaif.realtime.subscribe()`, and `vaif.ai` by `vaif.copilot(account_token)`.
  The `typegen` module and the synchronous client have no replacement.

### Added

- `VaifClient` and `create_client()`: an async client for one project. The
  project API key is sent as `x-vaif-key`. Options: `base_url` (HTTPS required;
  HTTP is accepted only for `localhost`, `127.0.0.1` and `::1`, and any other
  HTTP base URL raises `ValueError`), `timeout`, `retry`, `headers`,
  `http_client` and `session`. No cookie jar keeps an end user's refresh token, including that of
  an `http_client` you pass in.
- Redirects from the API are not followed, even on an `http_client` created
  with `follow_redirects=True`; they raise `VaifError` with code
  `REDIRECT_NOT_FOLLOWED`. The project key and the session token never reach
  another origin. A binary operation that the API redirects to a signed link,
  such as `get_storage_download()`, reads that link without the key or the
  session. An error keeps a `Location` header without its user information,
  query string or fragment, so it never carries a signed URL's signature.
- `RetryPolicy` and `NO_RETRY`: bounded exponential backoff with jitter that
  honors `Retry-After`. `GET`, `HEAD` and `OPTIONS` are retried on 429, 500, 502,
  503, 504 and network errors; any request is retried when the connection could
  not be opened.
- Typed exceptions for every failure: `VaifError` and its subclasses
  `VaifConsoleOnlyError`, `VaifValidationError`, `VaifAuthError`,
  `VaifNotFoundError`, `VaifConflictError`, `VaifRateLimitError`,
  `VaifServerError`, `VaifNetworkError` and `VaifTimeoutError`, with `status`,
  `code`, `details`, `request_id`, `body` and `headers`.
- `vaif.auth` for the end users of a project: `sign_up`, `sign_in`, `verify_mfa`,
  `refresh_session`, `sign_out`, `get_user`, `request_password_reset`,
  `reset_password`, `set_session` and `on_session_change`. Access tokens are
  refreshed before they expire and once after an HTTP 401. A request is not
  sent if the user signs out, or another session is installed, while its token
  is being refreshed (`VaifAuthError`, code `NOT_SIGNED_IN`), and after an
  HTTP 401 it is sent again only for the user who sent it; concurrent
  refreshes of one session share one request. `sign_out()` asks the server to
  revoke every session of the user and sends the refresh token, so it works
  after the access token has expired. A refresh that finishes while no user is
  signed in raises `VaifAuthError` with code `NOT_SIGNED_IN`, does not restore
  the session, and asks the server to revoke the refresh token it received.
- Session listeners: if a listener raises on `SIGNED_OUT`, for example because it
  could not delete a saved session, `sign_out()` still revokes the session on
  the server and then raises `VaifError` with code `SESSION_STORAGE_FAILED`. If
  a listener raises on `SIGNED_IN`, `sign_in()`, `sign_up()` (when it returns a
  session), `verify_mfa()` and `handle_oauth_callback()` leave the user signed
  in and raise the same code, so a store that could neither save the new
  session nor delete an earlier one is reported. The README's persistence
  example keys the saved session by API origin and project ID, and deletes it
  when a new session cannot be saved.
- `Session` leaves the access token and the refresh token out of `repr()`, and
  `SignInResult` leaves out the MFA challenge token, so logging either object
  does not log a credential.
- `vaif.auth.mfa`: TOTP `enroll_start`, `enroll_confirm`, `verify`, `disable` and
  `regenerate_codes`.
- OAuth sign-in with S256 PKCE: `get_oauth_sign_in_url`, `handle_oauth_callback`
  (checks the state before any request) and `list_oauth_providers`.
- `VaifConsoleOnlyError` (code `CONSOLE_ONLY`): platform sign-up and password
  reset, including the generated `post_auth_signup` and
  `post_auth_forgot_password`, are refused before any request, because VAIF
  Studio accounts are created and reset in the console. On a client without a
  project ID, every other `auth` method that calls the API raises code
  `PROJECT_ID_REQUIRED` before any request.
- Table queries (`vaif.from_()` and `vaif.table()`): the filters `eq`, `neq`,
  `gt`, `gte`, `lt`, `lte`, `like`, `ilike`, `in_` and `where`; `select`, `order`,
  `limit`, `offset` and `range`; and `list`, `first`, `paginate`, `count`, `get`,
  `insert`, `insert_many`, `upsert`, `update` and `delete`. Builders are
  immutable. A value that becomes a URL path segment (a row ID, a function
  name, a bucket ID, an OAuth provider, a project ID or a `path=` value of
  `vaif.operations`) is percent-encoded as one segment, and `.` and `..` raise
  `ValueError` before any request, because the HTTP stack would remove them
  from the path.
- `vaif.storage`: `upload` (through a presigned URL; the API key and session token
  are not sent to the object store), `download` (through a signed link, read
  without the API key or the session token), `create_signed_url`,
  `create_signed_upload_url` (requires `size_bytes`), and `list` and `delete` for
  a bucket by ID. Signed URLs must use `https` (`http` only for `localhost`,
  `127.0.0.1` and `::1`); any other raises code `INSECURE_STORAGE_URL`.
- `vaif.functions.invoke()` with method, path, query and headers, and decoded
  responses. An invocation that may have reached the function is sent again
  only with `idempotent=True`, and a function's own HTTP 401 never refreshes
  the session.
- `vaif.realtime.subscribe()`: table changes over an authenticated WebSocket, with
  subscription acknowledgment, heartbeat, access-token refresh, async iteration
  and cleanup on exit. Credentials are sent in the first message, never in the
  URL, and a redirected handshake is refused. The socket uses `wss` for an
  `https` base URL in any letter case, and `ws` only for `localhost`,
  `127.0.0.1` and `::1`; any other base URL raises code
  `INVALID_REALTIME_URL`. A connection that cannot be
  opened or is lost raises `VaifNetworkError` with code `REALTIME_CLOSED`, and
  one that times out while opening raises `VaifTimeoutError` with the same
  code. A subscription belongs to the session it was opened with: if the user
  signs out or another session is installed, it raises `VaifAuthError` with
  code `NOT_SIGNED_IN` instead of opening or authenticating the socket as the
  other session.
- `vaif.operations`: one coroutine for every API operation with a typed success
  response, except the staff-only operations (775 coroutines), generated from
  the API's OpenAPI description. `UNGENERATED_OPERATIONS` lists the other 168
  with the reason; the 134 staff-only operations are listed as
  `platform staff only`. A binary read that the API redirects to a signed link,
  such as `get_storage_download()`, returns the link's bytes, read without the
  API key or the session token and only over `https`.
- Staff-only operations are not generated, including the ones outside
  `/admin`: every operation under `/admin/*` and `/auth/impersonate/*`, plus
  feature flags (`/flags`), enterprise contract and invoice writes,
  `GET /ai/copilot/stats` and documentation edits under `/docs`. The API
  answers them only for VAIF platform staff.
- `vaif.copilot(account_token)` for Verament: `chat` (with `tier`, `effort` and
  `auto_confirm_max_credits`), `confirm_plan` (with `credit_choice` and `docs`),
  `queue_confirm_plan`, `get_job`, `cancel_plan`, `replan`, `plan_with_defaults`
  and `get_session`, plus `vaifstudio.copilot.blueprint_engine_offer()`.
- Type information for every public module (`py.typed`).

### Requirements

- Python 3.10 through 3.14.
- `httpx` 0.26 or later (below 1.0) and `websockets` 15 through 17 (`websockets`
  17 requires Python 3.11). Minimum versions of `certifi` (2026.10.19), `idna`
  (3.15), `anyio` (4.14.2) and `h11` (0.16) are declared so that installing the
  package upgrades releases with known vulnerabilities (GHSA-6q48-6c7w-9gw2,
  CVE-2026-45409, CVE-2026-63374, CVE-2026-64847 and CVE-2025-43859).

### Removed

- The pre-1.0 `db`, `ai` and `typegen` modules and the synchronous client. They
  targeted API routes that do not exist.
- The earlier realtime implementation, replaced by `vaif.realtime`.
