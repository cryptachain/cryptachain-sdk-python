"""Token metadata types."""

from __future__ import annotations

from cryptachain.types.common import CamelModel


class TokenMetadata(CamelModel):
    """Token metadata information."""

    symbol: str
    name: str | None = None
    decimals: int | None = None
    contract_address: str | None = None
    chain_id: int | None = None
    logo_url: str | None = None
    coingecko_id: str | None = None
    token_type: str | None = None  # ERC20, ERC721, NATIVE
    total_supply: str | None = None
    market_cap_usd: float | None = None
    website: str | None = None
