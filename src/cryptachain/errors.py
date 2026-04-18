"""Typed exceptions for the CryptaChain SDK."""

from __future__ import annotations


class CryptaChainError(Exception):
    """Base exception for all CryptaChain SDK errors.

    Attributes:
        status_code: HTTP status code, if applicable.
        message: Human-readable error message.
        response_body: Raw response body from the API, if available.
    """

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: dict | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_body = response_body


class AuthenticationError(CryptaChainError):
    """Raised on 401 Unauthorized — invalid or missing API key."""

    def __init__(self, message: str = "Invalid or missing API key", **kwargs: object) -> None:
        super().__init__(message, status_code=401, **kwargs)  # type: ignore[arg-type]


class QuotaExceededError(CryptaChainError):
    """Raised on 402 Payment Required — API quota exhausted."""

    def __init__(
        self, message: str = "API quota exceeded", **kwargs: object
    ) -> None:
        super().__init__(message, status_code=402, **kwargs)  # type: ignore[arg-type]


class NotFoundError(CryptaChainError):
    """Raised on 404 Not Found."""

    def __init__(self, message: str = "Resource not found", **kwargs: object) -> None:
        super().__init__(message, status_code=404, **kwargs)  # type: ignore[arg-type]


class ChainNotFoundError(NotFoundError):
    """Raised when a requested chain is not supported."""

    def __init__(self, chain: str) -> None:
        super().__init__(message=f"Chain not found: {chain}")
        self.chain = chain


class RateLimitError(CryptaChainError):
    """Raised on 429 Too Many Requests.

    Attributes:
        retry_after: Seconds to wait before retrying, from the Retry-After header.
    """

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: float | None = None,
        **kwargs: object,
    ) -> None:
        super().__init__(message, status_code=429, **kwargs)  # type: ignore[arg-type]
        self.retry_after = retry_after


class ValidationError(CryptaChainError):
    """Raised on 400/422 — request validation failed."""

    def __init__(self, message: str = "Validation error", **kwargs: object) -> None:
        super().__init__(message, status_code=422, **kwargs)  # type: ignore[arg-type]


class ServerError(CryptaChainError):
    """Raised on 5xx — server-side error."""

    def __init__(self, message: str = "Server error", **kwargs: object) -> None:
        super().__init__(message, status_code=500, **kwargs)  # type: ignore[arg-type]
