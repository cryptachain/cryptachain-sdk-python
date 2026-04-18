"""FX rate types — v2.3 P10 shape."""

from __future__ import annotations

from datetime import datetime

from cryptachain.types.common import CamelModel


class FxRate(CamelModel):
    """A single FX rate entry."""

    currency: str
    date: str
    rate: float
    source: str | None = None  # FRANKFURTER_ECB | HARDCODED_PEG | GAP_FILL_CARRY_FORWARD
    is_business_day: bool | None = None
    ratedate: str | None = None


class FxHistoryResponse(CamelModel):
    """FX rate history over a date range."""

    currency: str
    from_date: str
    to_date: str
    rates: list[FxRate] = []


class FxMonthlyAverageResponse(CamelModel):
    """IAS 21 monthly average FX rate."""

    currency: str
    year: int
    month: int
    average_rate: float
    days_in_month: int | None = None
    business_days: int | None = None
    source: str | None = None
    computed_at: datetime | None = None


class CurrencyInfo(CamelModel):
    """Information about a supported currency."""

    code: str
    name: str | None = None
    source: str | None = None
    pegged_to_usd: bool | None = None
    peg_ratio: float | None = None


class CurrenciesResponse(CamelModel):
    """List of all supported currencies."""

    currencies: list[CurrencyInfo] = []
    count: int = 0
