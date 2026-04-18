"""Cursor-based pagination helpers with sync and async generators."""

from __future__ import annotations

from typing import Any, AsyncIterator, Iterator, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class PaginatedResponse(BaseModel):
    """Generic paginated API response wrapper."""

    items: list[Any]
    cursor: str | None = None
    has_more: bool = False
    total: int | None = None


def iter_pages(
    fetch_fn: "callable",  # type: ignore[valid-type]
    params: dict[str, Any],
    item_key: str = "items",
    cursor_key: str = "cursor",
    limit: int = 100,
) -> Iterator[dict[str, Any]]:
    """Iterate over all pages of a paginated API endpoint (sync).

    Args:
        fetch_fn: Function that takes params dict and returns parsed JSON dict.
        params: Base query parameters.
        item_key: Key in the response containing the list of items.
        cursor_key: Key in the response containing the next cursor.
        limit: Page size.

    Yields:
        Individual items from across all pages.
    """
    params = {**params, "limit": limit}
    while True:
        data = fetch_fn(params)
        items = data.get(item_key, [])
        yield from items
        cursor = data.get(cursor_key)
        if not cursor or not items:
            break
        params["cursor"] = cursor


async def async_iter_pages(
    fetch_fn: "callable",  # type: ignore[valid-type]
    params: dict[str, Any],
    item_key: str = "items",
    cursor_key: str = "cursor",
    limit: int = 100,
) -> AsyncIterator[dict[str, Any]]:
    """Iterate over all pages of a paginated API endpoint (async).

    Args:
        fetch_fn: Async function that takes params dict and returns parsed JSON dict.
        params: Base query parameters.
        item_key: Key in the response containing the list of items.
        cursor_key: Key in the response containing the next cursor.
        limit: Page size.

    Yields:
        Individual items from across all pages.
    """
    params = {**params, "limit": limit}
    while True:
        data = await fetch_fn(params)
        items = data.get(item_key, [])
        for item in items:
            yield item
        cursor = data.get(cursor_key)
        if not cursor or not items:
            break
        params["cursor"] = cursor
