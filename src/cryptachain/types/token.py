"""Token record type, as recorded from ``GET /v1/prices/tokens/{symbol}``."""

from __future__ import annotations

from cryptachain.types.common import CamelModel


class TokenMetadata(CamelModel):
    """A token of the price registry."""

    token_id: int
    symbol: str
    name: str | None = None
    category: str | None = None  # e.g. LAYER1, STABLECOIN, DEFI
    previous_symbols: list[str] | None = None
    is_active: bool = True
    is_delisted: bool = False
    coingecko_id: str | None = None
