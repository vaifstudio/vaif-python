"""Official Python SDK for VAIF Studio.

Example::

    import asyncio
    import os

    from vaifstudio import create_client

    async def main() -> None:
        async with create_client(
            os.environ["VAIF_PROJECT_ID"], os.environ["VAIF_API_KEY"]
        ) as vaif:
            await vaif.auth.sign_in("ada@example.com", os.environ["VAIF_USER_PASSWORD"])
            todos = await vaif.from_("todos").eq("done", False).limit(20).list()
            print(todos.count, todos.data)

    asyncio.run(main())
"""

from vaifstudio._version import __version__
from vaifstudio.auth import AuthClient
from vaifstudio.client import DEFAULT_BASE_URL, VaifClient, create_client
from vaifstudio.copilot import CopilotClient
from vaifstudio.database import QueryBuilder
from vaifstudio.exceptions import (
    VaifAuthError,
    VaifConflictError,
    VaifConsoleOnlyError,
    VaifError,
    VaifNetworkError,
    VaifNotFoundError,
    VaifRateLimitError,
    VaifServerError,
    VaifTimeoutError,
    VaifValidationError,
)
from vaifstudio.functions import FunctionsClient
from vaifstudio.realtime import RealtimeClient, RealtimeSubscription
from vaifstudio.retry import NO_RETRY, RetryPolicy
from vaifstudio.storage import StorageClient
from vaifstudio.types import (
    FunctionResponse,
    ListResult,
    Page,
    Row,
    Session,
    SignInResult,
    SignUpResult,
    UploadResult,
    User,
)

__all__ = [
    "__version__",
    "create_client",
    "VaifClient",
    "DEFAULT_BASE_URL",
    "AuthClient",
    "QueryBuilder",
    "StorageClient",
    "FunctionsClient",
    "CopilotClient",
    "RealtimeClient",
    "RealtimeSubscription",
    "RetryPolicy",
    "NO_RETRY",
    "Session",
    "User",
    "SignInResult",
    "SignUpResult",
    "ListResult",
    "Page",
    "Row",
    "UploadResult",
    "FunctionResponse",
    "VaifError",
    "VaifConsoleOnlyError",
    "VaifValidationError",
    "VaifAuthError",
    "VaifNotFoundError",
    "VaifConflictError",
    "VaifRateLimitError",
    "VaifServerError",
    "VaifNetworkError",
    "VaifTimeoutError",
]
