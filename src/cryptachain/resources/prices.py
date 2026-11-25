"""Price resource: fair-value lookups on the routes the API serves."""

from __future__ import annotations

from datetime import date as date_type
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from cryptachain.types.price import BatchPriceResponse, PriceResponse
from cryptachain.utils.chain import resolve_chain_slug

if TYPE_CHECKING:
    from cryptachain.client import AsyncHttpClient, HttpClient


def _day_params(date: date_type | str | None, currency: str) -> dict[str, Any]:
    params: dict[str, Any] = {"currency": currency}
    if date is not None:
        params["date"] = str(date)
    return params


def _iso(timestamp: str | int | datetime) -> str:
    """ISO-8601 UTC text for epoch seconds, a datetime or text."""
    if isinstance(timestamp, int):
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if isinstance(timestamp, datetime):
        return timestamp.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return timestamp


def _batch(symbols: list[str], date: date_type | str, currency: str) -> tuple[str, dict[str, Any]]:
    if not 1 <= len(symbols) <= 500:
        raise ValueError("batch takes 1 to 500 symbols")
    return "/v1/prices/batch", {"symbols": ",".join(symbols), "date": str(date), "currency": currency}


def _batch_result(data: dict[str, Any]) -> BatchPriceResponse:
    return BatchPriceResponse(prices={k: PriceResponse.model_validate(v) for k, v in data.items()})


class PriceResource:
    """Synchronous price operations. Access via ``client.prices``."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def by_symbol(self, symbol: str, *, date: date_type | str | None = None, currency: str = "USD") -> PriceResponse:
        """``GET /v1/prices/{symbol}/fair-value`` (latest day when ``date`` is omitted)."""
        data = self._http.get(f"/v1/prices/{symbol}/fair-value", params=_day_params(date, currency))
        return PriceResponse.model_validate(data)

    def by_contract(
        self, chain: str | int, address: str, *, date: date_type | str | None = None, currency: str = "USD"
    ) -> PriceResponse:
        """``GET /v1/prices/by-contract/{chain}/{address}/fair-value``; ``chain`` is a slug or a known chain id."""
        slug = resolve_chain_slug(chain)
        data = self._http.get(f"/v1/prices/by-contract/{slug}/{address}/fair-value", params=_day_params(date, currency))
        return PriceResponse.model_validate(data)

    def batch(self, symbols: list[str], date: date_type | str, *, currency: str = "USD") -> BatchPriceResponse:
        """``GET /v1/prices/batch``: up to 500 symbols for one date. Symbols with no price are absent."""
        path, params = _batch(symbols, date, currency)
        return _batch_result(self._http.get(path, params=params))

    def at(self, symbol: str, timestamp: str | int | datetime, *, currency: str = "USD") -> PriceResponse:
        """``GET /v1/prices/{symbol}/at``: price at an ISO-8601 timestamp (daily fallback when no minute price)."""
        data = self._http.get(f"/v1/prices/{symbol}/at", params={"timestamp": _iso(timestamp), "currency": currency})
        return PriceResponse.model_validate(data)


class AsyncPriceResource:
    """Asynchronous price operations."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def by_symbol(self, symbol: str, *, date: date_type | str | None = None, currency: str = "USD") -> PriceResponse:
        data = await self._http.get(f"/v1/prices/{symbol}/fair-value", params=_day_params(date, currency))
        return PriceResponse.model_validate(data)

    async def by_contract(
        self, chain: str | int, address: str, *, date: date_type | str | None = None, currency: str = "USD"
    ) -> PriceResponse:
        slug = resolve_chain_slug(chain)
        data = await self._http.get(f"/v1/prices/by-contract/{slug}/{address}/fair-value", params=_day_params(date, currency))
        return PriceResponse.model_validate(data)

    async def batch(self, symbols: list[str], date: date_type | str, *, currency: str = "USD") -> BatchPriceResponse:
        path, params = _batch(symbols, date, currency)
        return _batch_result(await self._http.get(path, params=params))

    async def at(self, symbol: str, timestamp: str | int | datetime, *, currency: str = "USD") -> PriceResponse:
        data = await self._http.get(f"/v1/prices/{symbol}/at", params={"timestamp": _iso(timestamp), "currency": currency})
        return PriceResponse.model_validate(data)
