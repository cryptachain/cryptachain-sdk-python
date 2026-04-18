"""Screening resource — address risk screening."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cryptachain.types.screening import BulkScreeningResult, ScreeningResult
from cryptachain.utils.chain import resolve_chain

if TYPE_CHECKING:
    from cryptachain.client import AsyncHttpClient, HttpClient


class ScreeningResource:
    """Synchronous address screening operations.

    Access via ``client.screening``.
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def screen_address(
        self,
        address: str,
        *,
        chain: str | int | None = None,
    ) -> ScreeningResult:
        """Screen a single address for sanctions and risk flags.

        Args:
            address: Blockchain address to screen.
            chain: Chain name or chain ID.

        Returns:
            ScreeningResult with risk level, score, and any flags.
        """
        params: dict[str, Any] = {"address": address}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)
        data = self._http.get("/api/v1/screen/address", params=params)
        return ScreeningResult.model_validate(data)

    def screen_bulk(
        self,
        addresses: list[dict[str, Any]],
    ) -> BulkScreeningResult:
        """Screen multiple addresses in a single request.

        Args:
            addresses: List of dicts, each with "address" and optional "chain_id".

        Returns:
            BulkScreeningResult with individual results and summary counts.
        """
        data = self._http.post("/api/v1/screen/bulk", json={"addresses": addresses})
        return BulkScreeningResult.model_validate(data)


class AsyncScreeningResource:
    """Asynchronous address screening operations.

    Access via ``client.screening`` on an ``AsyncCryptaChain`` instance.
    """

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def screen_address(
        self,
        address: str,
        *,
        chain: str | int | None = None,
    ) -> ScreeningResult:
        """Screen a single address for sanctions and risk flags."""
        params: dict[str, Any] = {"address": address}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)
        data = await self._http.get("/api/v1/screen/address", params=params)
        return ScreeningResult.model_validate(data)

    async def screen_bulk(
        self,
        addresses: list[dict[str, Any]],
    ) -> BulkScreeningResult:
        """Screen multiple addresses in a single request."""
        data = await self._http.post("/api/v1/screen/bulk", json={"addresses": addresses})
        return BulkScreeningResult.model_validate(data)
