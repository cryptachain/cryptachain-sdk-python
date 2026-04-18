"""FX resource — rates, history, monthly averages, currencies."""

from __future__ import annotations

from datetime import date as date_type
from typing import TYPE_CHECKING, Any

from cryptachain.types.fx import (
    CurrenciesResponse,
    FxHistoryResponse,
    FxMonthlyAverageResponse,
    FxRate,
)

if TYPE_CHECKING:
    from cryptachain.client import AsyncHttpClient, HttpClient


class FxResource:
    """Synchronous FX rate operations.

    Access via ``client.fx``.
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get_rate(
        self,
        from_currency: str,
        to_currency: str,
        date: date_type | str | None = None,
    ) -> FxRate:
        """Get a single FX rate between two currencies.

        Args:
            from_currency: Source currency code (e.g. "EUR").
            to_currency: Target currency code (e.g. "USD").
            date: Date for the rate. Accepts date object or "YYYY-MM-DD" string.

        Returns:
            FxRate with the exchange rate and source metadata.
        """
        params: dict[str, Any] = {"from": from_currency, "to": to_currency}
        if date is not None:
            params["date"] = str(date)
        data = self._http.get("/v1/fx/rate", params=params)
        return FxRate.model_validate(data)

    def get_history(
        self,
        currency: str,
        *,
        from_date: date_type | str,
        to_date: date_type | str,
    ) -> FxHistoryResponse:
        """Get daily FX rate history for a currency (vs USD).

        Args:
            currency: Currency code (e.g. "EUR").
            from_date: Start date.
            to_date: End date.

        Returns:
            FxHistoryResponse with a list of daily rates.
        """
        params: dict[str, Any] = {
            "currency": currency,
            "from": str(from_date),
            "to": str(to_date),
        }
        data = self._http.get("/v1/fx/history", params=params)
        return FxHistoryResponse.model_validate(data)

    def get_monthly_average(
        self,
        currency: str,
        year: int,
        month: int,
    ) -> FxMonthlyAverageResponse:
        """Get the IAS 21 monthly average FX rate.

        Args:
            currency: Currency code (e.g. "EUR").
            year: Year (e.g. 2026).
            month: Month (1-12).

        Returns:
            FxMonthlyAverageResponse with the average rate and metadata.
        """
        params: dict[str, Any] = {
            "currency": currency,
            "year": year,
            "month": month,
        }
        data = self._http.get("/v1/fx/monthly-average", params=params)
        return FxMonthlyAverageResponse.model_validate(data)

    def list_currencies(self) -> CurrenciesResponse:
        """List all supported currencies (36 total).

        Returns:
            CurrenciesResponse with currency details and count.
        """
        data = self._http.get("/v1/fx/currencies")
        return CurrenciesResponse.model_validate(data)


class AsyncFxResource:
    """Asynchronous FX rate operations.

    Access via ``client.fx`` on an ``AsyncCryptaChain`` instance.
    """

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get_rate(
        self,
        from_currency: str,
        to_currency: str,
        date: date_type | str | None = None,
    ) -> FxRate:
        """Get a single FX rate between two currencies."""
        params: dict[str, Any] = {"from": from_currency, "to": to_currency}
        if date is not None:
            params["date"] = str(date)
        data = await self._http.get("/v1/fx/rate", params=params)
        return FxRate.model_validate(data)

    async def get_history(
        self,
        currency: str,
        *,
        from_date: date_type | str,
        to_date: date_type | str,
    ) -> FxHistoryResponse:
        """Get daily FX rate history for a currency."""
        params: dict[str, Any] = {
            "currency": currency,
            "from": str(from_date),
            "to": str(to_date),
        }
        data = await self._http.get("/v1/fx/history", params=params)
        return FxHistoryResponse.model_validate(data)

    async def get_monthly_average(
        self,
        currency: str,
        year: int,
        month: int,
    ) -> FxMonthlyAverageResponse:
        """Get the IAS 21 monthly average FX rate."""
        params: dict[str, Any] = {
            "currency": currency,
            "year": year,
            "month": month,
        }
        data = await self._http.get("/v1/fx/monthly-average", params=params)
        return FxMonthlyAverageResponse.model_validate(data)

    async def list_currencies(self) -> CurrenciesResponse:
        """List all supported currencies."""
        data = await self._http.get("/v1/fx/currencies")
        return CurrenciesResponse.model_validate(data)
