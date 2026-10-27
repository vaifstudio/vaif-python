# VAIF Studio Python SDK

<!-- BEGIN GENERATED SDK STATUS: notice:python -->
> `vaifstudio` 1.0.0 is the version in this repository. The hosted API (`https://api.vaif.studio`) and console are not available yet.
<!-- END GENERATED SDK STATUS: notice:python -->

`vaifstudio` is the official async Python client for the [VAIF Studio](https://vaif.studio)
API: end-user authentication, table queries, file storage, functions and realtime
table changes.

## Requirements

- Python 3.10 through 3.14.
- A VAIF Studio project: its project ID and a project API key, both shown in the
  VAIF Studio console.

The package depends on `httpx` (0.26 or later, below 1.0) for HTTP and `websockets`
(15 through 17) for realtime. It also declares minimum versions of `certifi`, `idna`,
`anyio` and `h11`, which `httpx` uses, so that installing the package upgrades any
release of them with a vulnerability known at the time of this release. CI fails on
any known vulnerability in the dependencies, at their newest and at their lowest
allowed versions. The package is fully typed (`py.typed`).

## Installation

Install the package from this repository:

```sh
python -m pip install "git+https://github.com/vaifstudio/vaif-python.git"
```

To make builds reproducible, pin a commit in your requirements file:

```text
vaifstudio @ git+https://github.com/vaifstudio/vaif-python.git@<commit-sha>
```

The distribution and the import package are both named `vaifstudio`.

### Upgrading from `vaif-client`

This package replaces `vaif-client` (import name `vaif`). Uninstall `vaif-client`,
install `vaifstudio`, and change `import vaif` and `from vaif import ...` to
`import vaifstudio` and `from vaifstudio import ...`. The interface changed in
1.0.0; the
[changelog](https://github.com/vaifstudio/vaif-python/blob/main/CHANGELOG.md)
lists what replaces each earlier interface. The `vaif` distribution on PyPI is
an older generated client and is not this package.

## Quick start

```python
import asyncio
import os

from vaifstudio import create_client


async def main() -> None:
    project_id = os.environ["VAIF_PROJECT_ID"]
    api_key = os.environ["VAIF_API_KEY"]

    async with create_client(project_id, api_key) as vaif:
        await vaif.auth.sign_in("ada@example.com", os.environ["VAIF_USER_PASSWORD"])

        created = await vaif.from_("todos").insert({"title": "Buy milk", "done": False})
        print("created", created["id"])

        open_todos = await (
            vaif.from_("todos")
            .eq("done", False)
            .order("created_at", desc=True)
            .limit(20)
            .list()
        )
        print(open_todos.count, [row["title"] for row in open_todos.data])


asyncio.run(main())
```

Every network call is a coroutine. Use the client as an async context manager, or
call `await vaif.close()` when you are done with it, to release its connections and
close its realtime subscriptions.

## Configuration

### API keys

The client sends the project API key in the `x-vaif-key` header on every request.

| Key prefix | Use |
| --- | --- |
| `vk_pub_` | Applications. Row-level security applies. |
| `vk_srv_` | Trusted servers only. It bypasses row-level security; never ship it in a browser, mobile or desktop application. |

Keep keys out of source control. Read them from the environment or a secret
manager, as the quick start does.

### Client options

```python
from vaifstudio import RetryPolicy, VaifClient

vaif = VaifClient(
    "YOUR_PROJECT_ID",
    "vk_pub_...",
    base_url="https://api.vaif.studio",
    timeout=30.0,
    retry=RetryPolicy(max_retries=3, base_delay=1.0, max_delay=30.0),
    headers={"X-App-Version": "1.4.2"},
)
```

`create_client(project_id, api_key, **options)` is equivalent to
`VaifClient(project_id, api_key, **options)`.

| Option | Default | Description |
| --- | --- | --- |
| `base_url` | `https://api.vaif.studio` | API origin. Must use `https`; `http` is accepted only for `localhost`, `127.0.0.1` and `::1`. |
| `timeout` | `30.0` | Timeout for each request, in seconds. |
| `retry` | `RetryPolicy()` | Retry policy for transient failures. `NO_RETRY` turns retries off. |
| `headers` | none | Headers sent with every request. |
| `http_client` | none | An `httpx.AsyncClient` to send requests with. The SDK does not close a client you pass in. After each API response it removes the API's `project_refresh_token` cookie from that client's cookie jar, so one end user's refresh token is never sent on another's requests; other cookies are kept. |
| `session` | none | A saved end-user `Session` to restore. |

The SDK does not follow redirects from the API, including on an `http_client`
created with `follow_redirects=True`, so the project key and the session token
are never sent to another origin. A redirect raises `VaifError` with code
`REDIRECT_NOT_FOLLOWED`. `error.headers["location"]` keeps where it pointed,
without the user information, query string or fragment: the query string of a
signed URL grants access to the object, so no error carries it. A binary
operation that the API redirects to a signed link, such as
`get_storage_download()`, reads that link without the key or the session; see
"Other API operations" below.

### Retries

`RetryPolicy` retries with exponential backoff (`base_delay * multiplier ** attempt`,
capped at `max_delay`, plus up to 25% jitter) and honors a `Retry-After` header,
also capped at `max_delay`.

- `GET`, `HEAD` and `OPTIONS` requests are retried on HTTP 429, 500, 502, 503 and
  504, on timeouts and on network errors.
- A request of any method is retried when the connection could not be opened
  (connection refused, DNS failure, connect timeout), because nothing reached the
  server.
- Other requests are not replayed once they may have reached the server, with two
  exceptions that repeat no work: the request behind `storage.create_signed_url()`
  and the object-store `PUT` inside `storage.upload()` are also retried on HTTP
  429, 500, 502, 503 and 504, on timeouts and on network errors.
  `functions.invoke()` accepts `idempotent=True` to opt in.

## End-user authentication

`vaif.auth` signs in the end users of your application, against
`/projects/{projectId}/auth`.

```python
result = await vaif.auth.sign_up("ada@example.com", password, metadata={"plan": "free"})
if result.pending_verification:
    print(result.message)

result = await vaif.auth.sign_in("ada@example.com", password)
if result.mfa_required and result.challenge_token:
    session = await vaif.auth.verify_mfa(result.challenge_token, totp_code)

user = await vaif.auth.get_user()
await vaif.auth.request_password_reset("ada@example.com")
await vaif.auth.reset_password(token_from_email, new_password)
await vaif.auth.sign_out()
```

While a user is signed in, database, storage, function, realtime and
`vaif.operations` calls carry the user's access token. Before each of those calls
the SDK refreshes the token if it expires within 30 seconds. If the user signs
out, or another session is installed, while that refresh runs, nothing is sent
and the call raises `VaifAuthError` with code `NOT_SIGNED_IN`. If the API refuses
the token with HTTP 401, the SDK refreshes the session and sends the call once
more, but only if the same user is still signed in: a call is never sent again
with another user's token. A function's own HTTP 401 is not treated this way; see
"Functions" below. Concurrent refreshes of one session share one request.

`sign_out()` clears the session locally, then asks the server to revoke every
session of that user. It sends the refresh token with the request, so the server
can identify the user after the access token has expired. A refresh that finishes
while no user is signed in raises `VaifAuthError` with code `NOT_SIGNED_IN`, does
not restore the session, and asks the server to revoke the refresh token it
received. A refresh that finishes after another session was installed returns that
session and leaves it unchanged.

### Persisting a session

Sessions are kept in memory. To keep a user signed in across restarts, save the
session when it changes and restore it on start-up:

```python
import json

from vaifstudio import Session, VaifClient


def session_key(vaif: VaifClient) -> str:
    # The API origin and the project ID together, so that clients for one
    # project at different base URLs never restore each other's session.
    return f"vaif-session:{vaif.base_url}|{vaif.project_id}"


def restore_session(vaif: VaifClient) -> None:
    saved = secure_store.get(session_key(vaif))
    if saved is None:
        return
    try:
        data = json.loads(saved)
        vaif.auth.set_session(
            data["access_token"], data["refresh_token"], expires_at=data["expires_at"]
        )
    except (ValueError, KeyError, TypeError):
        secure_store.delete(session_key(vaif))  # unreadable: sign in again


def persist_sessions(vaif: VaifClient) -> None:
    key = session_key(vaif)

    def on_change(event: str, session: Session | None) -> None:
        # event is "SIGNED_IN", "TOKEN_REFRESHED" or "SIGNED_OUT".
        if session is None:
            secure_store.delete(key)
            return
        value = json.dumps(
            {
                "access_token": session.access_token,
                "refresh_token": session.refresh_token,
                "expires_at": session.expires_at,
            }
        )
        try:
            secure_store.save(key, value)
        except Exception:
            # Never leave the previous session restorable.
            secure_store.delete(key)
            raise

    vaif.auth.on_session_change(on_change)
```

Call `restore_session(vaif)` and then `persist_sessions(vaif)` after creating the
client. `secure_store` stands for your application's secret storage, such as the
operating system's keychain: `get` returns `None` when nothing is saved under the
key, and `save` and `delete` raise when they fail. The session holds a refresh
token, which is a credential; do not keep it in a plain file or write it to a log.

- When a new session cannot be saved, the example deletes the saved one, so the
  next start signs in again instead of restoring a session that was replaced.
- When a listener raises on `SIGNED_IN`, `sign_in()`, `sign_up()` (when it returns
  a session), `verify_mfa()` and `handle_oauth_callback()` leave the user signed in
  and raise `VaifError` with code `SESSION_STORAGE_FAILED`, with the listener's
  exception as `__cause__`. If the store refused both to save the new session and
  to delete the saved one, the earlier session is restored on the next start, and
  this error is the only sign of it.
- When a listener raises on `SIGNED_OUT`, `sign_out()` still asks the server to
  revoke the session and then raises `VaifError` with code
  `SESSION_STORAGE_FAILED`, because the saved session could otherwise be restored
  on the next start.
- An exception from a listener on `TOKEN_REFRESHED`, from `set_session()`, or
  from the sign-out that follows a refresh the server refused, is logged to the
  `vaifstudio` logger and does not change the session.
- Listeners are plain functions, called synchronously when the session changes.

### Multi-factor authentication

TOTP enrollment and management require a signed-in user. Treat the enrollment
secret and the backup codes as credentials, and do not log them.

```python
enrollment = await vaif.auth.mfa.enroll_start()
await vaif.auth.mfa.enroll_confirm(enrollment["enrollToken"], totp_code)
await vaif.auth.mfa.regenerate_codes(totp_code)
await vaif.auth.mfa.disable(totp_code)
```

### OAuth with PKCE

Configure the provider and the redirect URL for your project in the console. The
SDK generates an S256 PKCE verifier and a state value and returns the consent URL.
Store the state and the verifier for this sign-in attempt, open the URL in a
browser, then exchange the code from the callback:

```python
pending = await vaif.auth.get_oauth_sign_in_url(
    "google", redirect_url="https://app.example.com/callback"
)
# Open pending["url"]. Keep pending["state"] and pending["code_verifier"]
# for this attempt only, and do not log the verifier.

result = await vaif.auth.handle_oauth_callback(
    code_from_callback,
    state=state_from_callback,
    expected_state=pending["state"],
    code_verifier=pending["code_verifier"],
)

providers = await vaif.auth.list_oauth_providers()
```

A state that does not match raises `VaifError` with code `OAUTH_STATE_MISMATCH`
before any request. If the user has MFA enrolled, `result.mfa_required` is `True`;
finish with `vaif.auth.verify_mfa()`.

### VAIF Studio accounts

`vaif.auth` is for the users of your own application. VAIF Studio accounts are
created, and their passwords reset, in the console. On a client created without a
project ID (`VaifClient(None, api_key)`), `auth.sign_up()` and
`auth.request_password_reset()` raise `VaifConsoleOnlyError` (code `CONSOLE_ONLY`,
with the console page in `console_url`) before any request. Every other `auth`
method that calls the API, such as `sign_in()`, `get_user()`, the `mfa` methods
and the OAuth methods, raises `VaifError` with code `PROJECT_ID_REQUIRED` before
any request; `sign_out()` does so after clearing the local session.
`set_session()` and `on_session_change()` do not call the API and work without a
project ID.

## Database queries

`vaif.from_(table)` (or `vaif.table(table)`) starts a query. Builders are
immutable: each method returns a new builder, so a base query can be reused.

```python
todos = vaif.from_("todos")

rows = await (
    todos.select("id", "title", "priority")
    .eq("owner", user.id)
    .gte("priority", 2)
    .in_("status", ["open", "blocked"])
    .order("priority", desc=True)
    .limit(50)
    .list()
)
rows.data   # the rows, as dicts
rows.count  # the total number of matching rows

page = await todos.eq("done", False).paginate(page=2, page_size=20)
page.data, page.total, page.has_next

row = await todos.get("row-id")  # raises VaifNotFoundError if there is no such row
first = await todos.ilike("title", "%milk%").first()  # None if nothing matches
total = await todos.eq("done", False).count()

created = await todos.insert({"title": "Buy milk"})
many = await todos.insert_many([{"title": "a"}, {"title": "b"}])
saved = await todos.upsert({"email": "ada@example.com", "name": "Ada"}, on_conflict=["email"])
updated = await todos.update("row-id", {"done": True})
await todos.delete("row-id")
```

- Filters: `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `like`, `ilike` and `in_`. Filters
  are combined with AND. For OR, pass a clause to `where()`:
  `todos.where({"OR": [{"field": "a", "value": 1}, {"field": "b", "value": 2}]})`.
- Table and column names must be SQL identifiers (letters, digits and
  underscores); anything else raises `ValueError` before any request.
- A row ID, like a function name, a bucket ID or a `path=` value of
  `vaif.operations`, is sent as one URL path segment. `.` and `..` raise
  `ValueError` before any request, because the HTTP stack would remove them from
  the path and the request would reach another route.
- `limit()` accepts 1 to 1000. `range(0, 19)` selects an inclusive, zero-based
  range of rows.

## Storage

```python
await vaif.storage.upload("avatars/u1.png", png_bytes, content_type="image/png")
data = await vaif.storage.download("avatars/u1.png")

download_url = await vaif.storage.create_signed_url("avatars/u1.png", expires_in=600)
upload_url = await vaif.storage.create_signed_upload_url(
    "exports/report.csv", size_bytes=len(csv_bytes), content_type="text/csv"
)
```

- `upload()` accepts bytes or a binary file object, up to 5 GB, read into memory.
  The API issues a presigned URL and the SDK sends the bytes to the object store
  with an HTTP `PUT`. The API key and the session token are not sent to that URL.
- `download()` asks the API for a signed link, then reads it from the file host
  without the API key or the session token. It follows at most 5 redirects, each
  to an `https` URL.
- Every signed URL, whether returned to you or used by `upload()` and
  `download()`, must use `https`; `http` is accepted only for `localhost`,
  `127.0.0.1` and `::1`. Any other URL raises `VaifError` with code
  `INSECURE_STORAGE_URL`, and nothing is sent to it.
- `bucket=` is optional on `upload()`, `download()` and both URL methods; without
  it the project's default bucket is used.
- A signed download URL lives `expires_in` seconds (1 to 604800, capped by the
  project's maximum), or the project's default lifetime when omitted.
- A signed upload URL is signed for exactly `size_bytes` and, when given,
  `content_type`. The `PUT` must send that size and that `Content-Type`. Buckets
  that restrict MIME types require `content_type`.

`storage.list(bucket_id, prefix=..., limit=..., cursor=...)` and
`storage.delete(key, bucket_id=...)` take the bucket's ID and require a VAIF Studio
console access token with access to the bucket, sent in the client's
`Authorization` header. A project key or an end-user session cannot authorize these
two calls.

## Functions

```python
response = await vaif.functions.invoke("send-email", {"to": "ada@example.com"})
response.status, response.data

report = await vaif.functions.invoke("report", method="GET", path="/daily", query={"day": "mon"})
```

`method`, `path`, `query` and `headers` are what the function receives. A JSON
response is decoded, a `text/*` response is returned as `str`, and anything else
as `bytes`. A non-2xx response from the function raises the matching `VaifError`
subclass, with the function's response body in `error.body` and its headers in
`error.headers`. `error.headers["X-Vaif-Run-Id"]` identifies the run.

An invocation that may have reached the function is not sent again unless you pass
`idempotent=True`. A 401 from the function itself is raised as it is: the SDK does
not refresh the session or run the function a second time. When the API refuses
the session token with HTTP 401, which it does before the function runs, the SDK
refreshes the session and sends the invocation once more.

## Realtime

```python
async with vaif.realtime.subscribe("todos", event="INSERT") as subscription:
    async for change in subscription:
        print(change["op"], change.get("record"))
```

- `event` is `"*"` (the default), `"INSERT"`, `"UPDATE"` or `"DELETE"`.
- Entering the context opens a WebSocket at `/realtime/ws` on the API origin,
  authenticates in the first message and waits until the API acknowledges the
  subscription. An `https` base URL opens `wss`; `ws` is used only for an `http`
  base URL on `localhost`, `127.0.0.1` or `::1`, and any other base URL raises
  `VaifError` with code `INVALID_REALTIME_URL` before the session is read.
  Credentials are never put in the URL, and a redirected handshake is refused.
- If the connection cannot be opened, entering the context raises
  `VaifNetworkError` with code `REALTIME_CLOSED`; when the handshake was refused,
  `status` is its HTTP status. If opening the connection, or waiting for the
  server's welcome or its acknowledgment of the subscription, takes longer than
  `timeout` seconds (`subscribe(table, timeout=15.0)` by default), it raises
  `VaifTimeoutError` with the same code.
- A heartbeat keeps the connection open and sends a refreshed access token to the
  server. A subscription belongs to the session it was opened with. If the user
  signs out, or another session is installed, before the socket is authenticated
  (while the access token is refreshed or the connection is made), entering the
  context raises `VaifAuthError` with code `NOT_SIGNED_IN` and sends no
  credentials. If it happens later, including a sign-in after a subscription that
  was opened without a session, the next heartbeat closes the socket and iteration
  raises the same error, without authenticating the socket as the other session.
  Open a new subscription.
- Leaving the context, canceling the task or `await vaif.close()` closes the
  socket.
- If the connection is lost, iteration raises `VaifNetworkError` with code
  `REALTIME_CLOSED` and the close code in `status`. A refused connection or
  subscription raises with the API's code, for example `UNAUTHORIZED`,
  `TOKEN_EXPIRED` or `FORBIDDEN`. The SDK does not reconnect or replay missed
  events: open a new subscription and reconcile rows that changed in between.

## Other API operations

`vaif.operations` has one coroutine for every API operation with a typed success
response, except the staff-only operations: 775 in this version.
The coroutines are generated from the API's OpenAPI description and named after
their method and path:

```python
keys = await vaif.operations.get_projects_by_project_id_api_keys(path={"projectId": project_id})
logs = await vaif.operations.get_logs_project_by_project_id(
    path={"projectId": project_id}, query={"limit": 50, "level": "error"}
)
```

Each method takes keyword arguments for what its route accepts: `path=` for path
parameters, `query=` and `body=` where the route has them, and always `headers=`.
JSON responses are decoded and binary responses are returned as `bytes`. When the
API answers a binary read with a redirect to a signed link, as
`get_storage_download()` does, the SDK reads the link the way `storage.download()`
does: without the API key or the session token, and only over `https` (`http`
only for `localhost`, `127.0.0.1` and `::1`). The server-sent event route returns
its `httpx.Response` after the stream has ended, with the whole body read. Calls
use the client's transport, so they carry the API key and the session, follow the
retry policy and raise the same errors.

`vaifstudio._generated.UNGENERATED_OPERATIONS` lists the other 168 operations
as `(method, path, reason)`: those without a typed success response, and the 134
staff-only operations, listed with the reason `platform staff only`. The API
answers the staff-only operations only for VAIF platform staff: every operation
under `/admin/*` and `/auth/impersonate/*`, and those outside them: feature flags
(`/flags`), enterprise contract and invoice writes, Verament usage statistics
(`GET /ai/copilot/stats`) and documentation edits under `/docs`.

Console routes, such as API keys, logs and project creation, need a VAIF Studio
access token. Pass it in the client's `headers` as `Authorization: Bearer <token>`.
An `Authorization` header you set is sent as given and is never replaced by an
end-user session.

## Verament

Verament is the VAIF Studio AI engine that builds backends from a prompt. It acts
for your VAIF Studio account, so `vaif.copilot()` takes an account access token in
addition to the project key.

A build request is answered with a plan card. Planning is charged; nothing is
built, and the build is not charged, until you confirm the plan.

```python
copilot = vaif.copilot(account_token)

planned = await copilot.chat(project_id, "tables for a todo list", generation_types=["schema"])
card = planned["preflightRequired"]["plan"]

built = await copilot.confirm_plan(
    project_id, planned["sessionId"], card["planId"], "tables for a todo list"
)
files = built["response"]["artifacts"]["files"]
```

- A plan is confirmed once, within 30 minutes, in its session, with the message it
  was made for. A refused confirm raises: 404 when the plan does not exist; 409
  when it was already confirmed, canceled or replaced, when the message differs
  from the one the plan was made for, or when the plan is stale (`PLAN_STALE`);
  and 410 when it has expired.
- `queue_confirm_plan()` runs the build in the background; poll `get_job(job_id)`
  for the result. `cancel_plan()` drops a plan.
- When the balance is below the run's maximum, `confirm_plan()` returns
  `preflightRequired` with a credit choice. Confirm again with
  `credit_choice="smaller"` or `credit_choice="until_zero"`.
- `chat(..., auto_confirm_max_credits=200)` builds in the same call when the whole
  run costs at most 200 credits.
- `chat(..., tier="standard", effort="deep")` selects the engine: Verament Lite 1.0,
  Standard 1.0 or Max 1.0 (`"lite"`, `"standard"`, `"max"`), at Quick, Balanced,
  Deep or Extended effort. When omitted, your plan's defaults apply. An engine your
  plan does not include is refused with HTTP 403 before any model call;
  `vaifstudio.copilot.blueprint_engine_offer(error)` returns what the plan allows.
- Every build writes a README at no charge. A card's `docs` row offers more
  documents, priced into the maximum; pass `docs={"kinds": ["api"]}` to
  `confirm_plan()` to add them.

## Error handling

Every failure from the API or the network raises a `VaifError` subclass:

```python
from vaifstudio import VaifError, VaifRateLimitError

try:
    rows = await vaif.from_("todos").eq("done", False).list()
except VaifRateLimitError as error:
    print("rate limited; retry after", error.retry_after, "seconds")
except VaifError as error:
    print(error.status, error.code, error.message, error.request_id)
```

| Exception | Raised for |
| --- | --- |
| `VaifError` | Base class. Also raised for responses that no subclass below covers. |
| `VaifConsoleOnlyError` | Platform sign-up or password reset (code `CONSOLE_ONLY`), before any request. |
| `VaifValidationError` | HTTP 400 and 422. |
| `VaifAuthError` | HTTP 401 and 403, and calls that need a signed-in user. |
| `VaifNotFoundError` | HTTP 404. |
| `VaifConflictError` | HTTP 409. |
| `VaifRateLimitError` | HTTP 429. `retry_after` is in seconds when the API sends it. |
| `VaifServerError` | HTTP 5xx. |
| `VaifNetworkError` | A request that could not be completed or whose response could not be read, or a realtime connection that could not be opened, failed or was lost. |
| `VaifTimeoutError` | A timeout. Subclass of `VaifNetworkError`. |

Each error has `message`, `status` (the HTTP status, or the WebSocket close code,
when there is one), `code` (the API's machine-readable code, such as
`INVALID_COLUMN`, when it sends one), `details`, `request_id`, `body` and `headers`
(the response headers, matched case-insensitively; empty when there was no HTTP
response). Include `request_id` when you contact support.

Codes set by the SDK itself:

| Code | Exception | Meaning |
| --- | --- | --- |
| `CONSOLE_ONLY` | `VaifConsoleOnlyError` | VAIF Studio accounts are created and reset in the console. |
| `PROJECT_ID_REQUIRED` | `VaifError` | An `auth` call that needs the API, on a client created without a project ID. |
| `NOT_SIGNED_IN` | `VaifAuthError` | The call needs a signed-in user, or the user signed out, or another session was installed, during a token refresh or while a realtime subscription was open. |
| `SESSION_STORAGE_FAILED` | `VaifError` | `sign_out()` signed out, or a call that signs a user in installed the session, but a session listener raised while the session was being cleared or saved. The listener's exception is `__cause__`. |
| `NO_REFRESH_TOKEN` | `VaifAuthError` | A refresh was requested for a session without a refresh token. |
| `OAUTH_STATE_MISMATCH` | `VaifError` | The OAuth callback's state does not match the saved state. |
| `OAUTH_MISSING_CODE` | `VaifError` | The OAuth callback carried no code. |
| `INVALID_REALTIME_URL` | `VaifError` | Realtime was opened on a base URL that is neither `https` nor `http` on `localhost`, `127.0.0.1` or `::1`. |
| `REDIRECT_NOT_FOLLOWED` | `VaifError` | The API answered with a redirect, which the SDK does not follow (a binary operation's redirect to a signed link is read instead; see "Other API operations"). `status` is the redirect's status; `headers["location"]` is its target without user information, query string or fragment. |
| `REALTIME_CLOSED` | `VaifNetworkError` or `VaifTimeoutError` | A realtime connection could not be opened, timed out while opening, or closed. |
| `INSECURE_STORAGE_URL` | `VaifError` | A signed storage URL, or a redirect while downloading, is not `https` (`http` is accepted only for `localhost`, `127.0.0.1` and `::1`). |
| `STORAGE_UPLOAD_FAILED` | a `VaifError` subclass, by HTTP status | The object store refused an upload and sent no error code of its own. |
| `STORAGE_DOWNLOAD_FAILED` | a `VaifError` subclass, by HTTP status | The file host refused a download and sent no error code of its own, or redirected it more than 5 times. |

Invalid arguments, such as an empty table name or a `limit` above 1000, raise
`ValueError` (or `TypeError` for a value of the wrong type) before any request is
sent.

## Versioning

This package follows [Semantic Versioning](https://semver.org). The public
interface is every name exported from `vaifstudio` (listed in `vaifstudio.__all__`),
the public attributes and methods of those objects, the `vaifstudio.copilot`
module, and the exception types and SDK error codes documented above. Names that
begin with an underscore, such as `vaifstudio._http`, are internal.

A new major version is required to:

- remove or rename a public name, method or argument;
- change an argument or a return type incompatibly;
- raise a different exception type, or a different SDK error code, for the same
  condition;
- raise the minimum supported Python version.

Minor versions add functionality without breaking existing code. Patch versions
contain fixes only.

`vaif.operations` follows the API's route table. When the API retires a route, its
method is removed in a minor release, because the call can no longer succeed. The
[changelog](https://github.com/vaifstudio/vaif-python/blob/main/CHANGELOG.md)
records every such removal.

## Support

- Bug reports and feature requests: [GitHub issues](https://github.com/vaifstudio/vaif-python/issues).
- Account, billing and product questions: support@vaif.studio.
- Security vulnerabilities: email security@vaif.studio and do not open a public
  issue. See [SECURITY.md](https://github.com/vaifstudio/vaif-python/blob/main/SECURITY.md).

## Contributing

See
[CONTRIBUTING.md](https://github.com/vaifstudio/vaif-python/blob/main/CONTRIBUTING.md)
for local development and how pull requests are handled. Participation in this
project is governed by the
[Code of Conduct](https://github.com/vaifstudio/vaif-python/blob/main/CODE_OF_CONDUCT.md).

## License

MIT. See [LICENSE](https://github.com/vaifstudio/vaif-python/blob/main/LICENSE).
