"""Price resource — symbol, contract, batch, and at-timestamp lookups."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cryptachain.types.price import BatchPriceResponse, PriceResponse
from cryptachain.utils.chain import resolve_chain

if TYPE_CHECKING:
    from cryptachain.client import AsyncHttpClient, HttpClient


class PriceResource:
    """Synchronous price operations.

    Access via ``client.prices``.
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def by_symbol(
        self,
        symbol: str,
        *,
        date: str | None = None,
        currency: str = "USD",
    ) -> PriceResponse:
        """Get the price for a token by its symbol.

        Args:
            symbol: Token symbol, e.g. "BTC", "ETH".
            date: Date string (YYYY-MM-DD). Defaults to latest.
            currency: Target currency code (default "USD").

        Returns:
            PriceResponse with v2.3 P11 shape including quality_score and fair_value_level.
        """
        params: dict[str, Any] = {"symbol": symbol, "currency": currency}
        if date is not None:
            params["date"] = date
        data = self._http.get("/v1/prices/by-symbol", params=params)
        return PriceResponse.model_validate(data)

    def by_contract(
        self,
        chain: str | int,
        address: str,
        *,
        date: str | None = None,
        currency: str = "USD",
    ) -> PriceResponse:
        """Get the price for a token by its contract address.

        Args:
            chain: Chain name or chain ID.
            address: Token contract address.
            date: Date string (YYYY-MM-DD). Defaults to latest.
            currency: Target currency code (default "USD").

        Returns:
            PriceResponse with pricing and quality metadata.
        """
        params: dict[str, Any] = {
            "chain_id": resolve_chain(chain),
            "address": address,
            "currency": currency,
        }
        if date is not None:
            params["date"] = date
        data = self._http.get("/v1/prices/by-contract", params=params)
        return PriceResponse.model_validate(data)

    def batch(
        self,
        requests: list[dict[str, Any]],
    ) -> BatchPriceResponse:
        """Get prices for multiple tokens in a single request.

        Args:
            requests: List of price request dicts. Each may contain:
                symbol, chain_id, address, date, timestamp, currency.
                Maximum 500 items per request.

        Returns:
            BatchPriceResponse with results and any errors.
        """
        data = self._http.post("/v1/prices/batch", json={"requests": requests})
        return BatchPriceResponse.model_validate(data)

    def at(
        self,
        symbol: str,
        *,
        timestamp: int,
        currency: str = "USD",
    ) -> PriceResponse:
        """Get the price at a specific Unix timestamp (1-minute precision via ClickHouse).

        Args:
            symbol: Token symbol, e.g. "BTC".
            timestamp: Unix timestamp in seconds.
            currency: Target currency code (default "USD").

        Returns:
            PriceResponse for the closest available minute.
        """
        params: dict[str, Any] = {
            "symbol": symbol,
            "timestamp": timestamp,
            "currency": currency,
        }
        data = self._http.get("/v1/prices/at", params=params)
        return PriceResponse.model_validate(data)


class AsyncPriceResource:
    """Asynchronous price operations.

    Access via ``client.prices`` on an ``AsyncCryptaChain`` instance.
    """

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def by_symbol(
        self,
        symbol: str,
        *,
        date: str | None = None,
        currency: str = "USD",
    ) -> PriceResponse:
        """Get the price for a token by its symbol.

        Args:
            symbol: Token symbol, e.g. "BTC", "ETH".
            date: Date string (YYYY-MM-DD). Defaults to latest.
            currency: Target currency code (default "USD").

        Returns:
            PriceResponse with v2.3 P11 shape.
        """
        params: dict[str, Any] = {"symbol": symbol, "currency": currency}
        if date is not None:
            params["date"] = date
        data = await self._http.get("/v1/prices/by-symbol", params=params)
        return PriceResponse.model_validate(data)

    async def by_contract(
        self,
        chain: str | int,
        address: str,
        *,
        date: str | None = None,
        currency: str = "USD",
    ) -> PriceResponse:
        """Get the price for a token by its contract address."""
        params: dict[str, Any] = {
            "chain_id": resolve_chain(chain),
            "address": address,
            "currency": currency,
        }
        if date is not None:
            params["date"] = date
        data = await self._http.get("/v1/prices/by-contract", params=params)
        return PriceResponse.model_validate(data)

    async def batch(
        self,
        requests: list[dict[str, Any]],
    ) -> BatchPriceResponse:
        """Get prices for multiple tokens in a single request.

        Args:
            requests: List of price request dicts (max 500).

        Returns:
            BatchPriceResponse with results and any errors.
        """
        data = await self._http.post("/v1/prices/batch", json={"requests": requests})
        return BatchPriceResponse.model_validate(data)

    async def at(
        self,
        symbol: str,
        *,
        timestamp: int,
        currency: str = "USD",
    ) -> PriceResponse:
        """Get the price at a specific Unix timestamp (1-minute precision)."""
        params: dict[str, Any] = {
            "symbol": symbol,
            "timestamp": timestamp,
            "currency": currency,
        }
        data = await self._http.get("/v1/prices/at", params=params)
        return PriceResponse.model_validate(data)
