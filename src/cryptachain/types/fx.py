"""FX rate types, as recorded from the live /v1/fx routes."""

from __future__ import annotations

from pydantic import ConfigDict, Field

from cryptachain.types.common import CamelModel


class FxRate(CamelModel):
    """``GET /v1/fx/rate``: one rate, ``from_currency`` -> ``to_currency`` on ``date``."""

    from_currency: str
    to_currency: str
    date: str
    rate: float
    source: str | None = None  # FRANKFURTER_ECB, HARDCODED_PEG, ...


class FxHistoryPoint(CamelModel):
    """One day of an FX history: USD per 1 unit of the currency."""

    date: str
    value: float
    carried_forward: bool = False  # True when the previous day's rate was carried forward
    source: str | None = None


class FxHistoryResponse(CamelModel):
    """``GET /v1/fx/history``."""

    model_config = ConfigDict(populate_by_name=True)

    currency: str
    base_currency: str
    from_date: str = Field(alias="from")
    to_date: str = Field(alias="to")
    rates: list[FxHistoryPoint] = Field(default_factory=list)


class FxMonthlyAverageResponse(CamelModel):
    """``GET /v1/fx/monthly-average``: IAS 21 monthly average. ``is_live`` is True for an unfinished month."""

    currency: str
    base_currency: str
    year: int
    month: int
    avg_rate: float
    days_in_average: int
    is_live: bool = False


class CurrenciesResponse(CamelModel):
    """``GET /v1/fx/currencies``."""

    currencies: list[str] = Field(default_factory=list)
    ecb_count: int = 0
    pegged: list[str] = Field(default_factory=list)
    pegged_count: int = 0
    total: int = 0
