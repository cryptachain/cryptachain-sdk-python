"""Screening resource: address risk screening (``POST /v1/screen/address``, ``POST /v1/screen/bulk``)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cryptachain.types.screening import ScreeningResult
from cryptachain.utils.chain import resolve_chain_slug

if TYPE_CHECKING:
    from cryptachain.client import AsyncHttpClient, HttpClient


def _bulk_body(addresses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Each item: ``{"address": ..., "chain": "ethereum"}`` (``"chain_id"`` is also accepted and converted)."""
    body = []
    for item in addresses:
        chain = item.get("chain", item.get("chain_id", 1))
        body.append({"address": item["address"], "chain": resolve_chain_slug(chain)})
    return body


class ScreeningResource:
    """Synchronous address screening operations. Access via ``client.screening``."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def screen_address(self, address: str, *, chain: str | int = 1) -> ScreeningResult:
        """Screen a single address. ``chain`` is a slug (``"ethereum"``) or a known chain id."""
        data = self._http.post("/v1/screen/address", json={"address": address, "chain": resolve_chain_slug(chain)})
        return ScreeningResult.model_validate(data)

    def screen_bulk(self, addresses: list[dict[str, Any]]) -> list[ScreeningResult]:
        """Screen several addresses; the API answers with one result per address."""
        data = self._http.post("/v1/screen/bulk", json=_bulk_body(addresses))
        return [ScreeningResult.model_validate(r) for r in data]


class AsyncScreeningResource:
    """Asynchronous address screening operations."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def screen_address(self, address: str, *, chain: str | int = 1) -> ScreeningResult:
        data = await self._http.post("/v1/screen/address", json={"address": address, "chain": resolve_chain_slug(chain)})
        return ScreeningResult.model_validate(data)

    async def screen_bulk(self, addresses: list[dict[str, Any]]) -> list[ScreeningResult]:
        data = await self._http.post("/v1/screen/bulk", json=_bulk_body(addresses))
        return [ScreeningResult.model_validate(r) for r in data]
