"""Price response types, as recorded from the live price routes."""

from __future__ import annotations

from pydantic import Field

from cryptachain.types.common import CamelModel


class PriceResponse(CamelModel):
    """Body of ``GET /v1/prices/{symbol}/fair-value`` (and ``/at``, by-contract, one entry of batch).

    Decimals arrive as JSON numbers; ``fair_value_level`` is 1, 2 or 3 (None when unset).
    ``close_final`` is FINAL, PROVISIONAL or UNKNOWN; UNKNOWN is never FINAL.
    """

    price: float
    price_usd: float
    currency: str
    fx_rate: float | None = None  # USD per 1 unit of ``currency``; None for USD
    fx_source: str | None = None  # "ECB" or "PEG"; None for USD
    fx_date: str | None = None
    date: str
    source_count: int | None = None
    quality_score: int | None = None
    fair_value_level: int | None = None
    total_volume_usd: float | None = None
    spread_pct: float | None = None
    methodology_version: int | None = None
    revision: int | None = None
    price_close_zone: str | None = None
    precision: str | None = None  # DAILY, or DAILY_FALLBACK when no minute price was available
    close_grade: str | None = None
    close_final: str | None = None


class BatchPriceResponse(CamelModel):
    """``GET /v1/prices/batch``: prices by requested symbol. A symbol with no price on that date is absent."""

    prices: dict[str, PriceResponse] = Field(default_factory=dict)
