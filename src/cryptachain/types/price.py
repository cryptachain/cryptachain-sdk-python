"""Price response types — v2.3 P11 shape."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from cryptachain.types.common import CamelModel


class FxSource(str, Enum):
    """FX rate source."""

    FRANKFURTER_ECB = "FRANKFURTER_ECB"
    HARDCODED_PEG = "HARDCODED_PEG"
    USD_BASE = "USD_BASE"


class PriceSource(str, Enum):
    """Price data source."""

    CRYPTAPRICE_VWAP = "CRYPTAPRICE_VWAP"
    MANUAL_OVERRIDE = "MANUAL_OVERRIDE"
    STABLECOIN_PEGGED = "STABLECOIN_PEGGED"
    ZERO_VALUE_IFRS_13_B37 = "ZERO_VALUE_IFRS_13_B37"


class FairValueLevel(str, Enum):
    """IFRS 13 fair value hierarchy level."""

    LEVEL_1 = "LEVEL_1"
    LEVEL_2 = "LEVEL_2"
    LEVEL_3 = "LEVEL_3"


class PriceResponse(CamelModel):
    """Price response following v2.3 P11 shape.

    Contains the price, FX conversion details, quality metadata,
    and IFRS fair value level classification.
    """

    symbol: str
    date: str
    currency: str
    price: float
    price_usd: float | None = None
    fx_rate: float | None = None
    fx_source: FxSource | None = None
    fx_date: str | None = None
    source: PriceSource | None = None
    quality_score: int | None = None  # 0-100
    fair_value_level: FairValueLevel | None = None
    source_count: int | None = None
    methodology_version: str | None = None
    stablecoin_pegged: bool | None = None
    manual_override: bool | None = None
    computed_at: datetime | None = None


class BatchPriceRequest(CamelModel):
    """A single item in a batch price request."""

    symbol: str | None = None
    chain_id: int | None = None
    address: str | None = None
    date: str | None = None
    timestamp: int | None = None
    currency: str = "USD"


class BatchPriceResponse(CamelModel):
    """Response from the batch price endpoint."""

    results: list[PriceResponse] = []
    errors: list[dict] | None = None  # type: ignore[type-arg]
