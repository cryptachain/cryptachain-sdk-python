"""Exponential backoff retry logic."""

from __future__ import annotations

import asyncio
import random
import time
from typing import TypeVar

import httpx

from cryptachain.config import Config
from cryptachain.errors import (
    AuthenticationError,
    CryptaChainError,
    NotFoundError,
    QuotaExceededError,
    RateLimitError,
    ServerError,
    ValidationError,
)

T = TypeVar("T")

_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
_NON_RETRYABLE_STATUS_CODES = {401, 402}


def _calculate_delay(attempt: int, config: Config, retry_after: float | None = None) -> float:
    """Calculate the delay before the next retry attempt."""
    if retry_after is not None:
        return retry_after
    delay = config.retry_base_delay * (2 ** attempt)
    delay = min(delay, config.retry_max_delay)
    # Add jitter: +/- 25%
    jitter = delay * 0.25
    return delay + random.uniform(-jitter, jitter)


def raise_for_status(response: httpx.Response) -> None:
    """Map HTTP error responses to typed exceptions."""
    if response.is_success:
        return

    try:
        body = response.json()
    except Exception:
        body = None

    message = ""
    if isinstance(body, dict):
        message = body.get("message", "") or body.get("error", "")

    status = response.status_code

    if status == 401:
        raise AuthenticationError(message or "Invalid or missing API key", response_body=body)
    elif status == 402:
        raise QuotaExceededError(message or "API quota exceeded", response_body=body)
    elif status == 404:
        raise NotFoundError(message or "Resource not found", response_body=body)
    elif status == 429:
        retry_after_header = response.headers.get("Retry-After")
        retry_after = float(retry_after_header) if retry_after_header else None
        raise RateLimitError(
            message or "Rate limit exceeded",
            retry_after=retry_after,
            response_body=body,
        )
    elif status in (400, 422):
        raise ValidationError(message or "Validation error", response_body=body)
    elif status >= 500:
        raise ServerError(message or f"Server error ({status})", response_body=body)
    else:
        raise CryptaChainError(
            message or f"HTTP {status}",
            status_code=status,
            response_body=body,
        )


def execute_with_retry(
    config: Config,
    request_fn: "callable",  # type: ignore[valid-type]
) -> httpx.Response:
    """Execute a sync request with retry logic.

    Args:
        config: SDK configuration with retry settings.
        request_fn: Callable that returns an httpx.Response.

    Returns:
        The successful response.

    Raises:
        CryptaChainError: If all retries are exhausted or a non-retryable error occurs.
    """
    last_exception: Exception | None = None

    for attempt in range(config.max_retries + 1):
        try:
            response = request_fn()
            if response.status_code in _RETRYABLE_STATUS_CODES and attempt < config.max_retries:
                retry_after = None
                if response.status_code == 429:
                    ra = response.headers.get("Retry-After")
                    retry_after = float(ra) if ra else None
                delay = _calculate_delay(attempt, config, retry_after)
                time.sleep(delay)
                continue
            raise_for_status(response)
            return response
        except (httpx.TimeoutException, httpx.ConnectError) as exc:
            last_exception = exc
            if attempt < config.max_retries:
                delay = _calculate_delay(attempt, config)
                time.sleep(delay)
                continue
            raise CryptaChainError(f"Request failed after {config.max_retries + 1} attempts: {exc}") from exc
        except CryptaChainError as exc:
            if exc.status_code in _NON_RETRYABLE_STATUS_CODES:
                raise
            if exc.status_code in _RETRYABLE_STATUS_CODES and attempt < config.max_retries:
                retry_after = getattr(exc, "retry_after", None)
                delay = _calculate_delay(attempt, config, retry_after)
                time.sleep(delay)
                last_exception = exc
                continue
            raise

    raise CryptaChainError(f"Request failed after {config.max_retries + 1} attempts") from last_exception


async def async_execute_with_retry(
    config: Config,
    request_fn: "callable",  # type: ignore[valid-type]
) -> httpx.Response:
    """Execute an async request with retry logic.

    Args:
        config: SDK configuration with retry settings.
        request_fn: Async callable that returns an httpx.Response.

    Returns:
        The successful response.

    Raises:
        CryptaChainError: If all retries are exhausted or a non-retryable error occurs.
    """
    last_exception: Exception | None = None

    for attempt in range(config.max_retries + 1):
        try:
            response = await request_fn()
            if response.status_code in _RETRYABLE_STATUS_CODES and attempt < config.max_retries:
                retry_after = None
                if response.status_code == 429:
                    ra = response.headers.get("Retry-After")
                    retry_after = float(ra) if ra else None
                delay = _calculate_delay(attempt, config, retry_after)
                await asyncio.sleep(delay)
                continue
            raise_for_status(response)
            return response
        except (httpx.TimeoutException, httpx.ConnectError) as exc:
            last_exception = exc
            if attempt < config.max_retries:
                delay = _calculate_delay(attempt, config)
                await asyncio.sleep(delay)
                continue
            raise CryptaChainError(f"Request failed after {config.max_retries + 1} attempts: {exc}") from exc
        except CryptaChainError as exc:
            if exc.status_code in _NON_RETRYABLE_STATUS_CODES:
                raise
            if exc.status_code in _RETRYABLE_STATUS_CODES and attempt < config.max_retries:
                retry_after = getattr(exc, "retry_after", None)
                delay = _calculate_delay(attempt, config, retry_after)
                await asyncio.sleep(delay)
                last_exception = exc
                continue
            raise

    raise CryptaChainError(f"Request failed after {config.max_retries + 1} attempts") from last_exception
