"""Wallet-related data types."""

from __future__ import annotations

from datetime import datetime

from cryptachain.types.common import CamelModel


class Asset(CamelModel):
    """Token asset within a transfer or balance."""

    symbol: str | None = None
    name: str | None = None
    contract_address: str | None = None
    decimals: int | None = None
    logo_url: str | None = None
    token_type: str | None = None  # ERC20, ERC721, NATIVE, etc.


class Transfer(CamelModel):
    """A single wallet transfer (in or out)."""

    tx_hash: str
    block_number: int
    timestamp: datetime
    direction: str  # IN, OUT
    from_address: str
    to_address: str
    value: str
    value_formatted: float | None = None
    value_usd_at_time: float | None = None
    asset: Asset | None = None
    gas_used: int | None = None
    gas_price: str | None = None
    status: str | None = None  # SUCCESS, FAILED


class WalletHistory(CamelModel):
    """Paginated list of wallet transfers."""

    items: list[Transfer] = []
    cursor: str | None = None
    has_more: bool = False
    total: int | None = None


class TokenBalance(CamelModel):
    """A single token balance for a wallet."""

    asset: Asset
    balance: str
    balance_formatted: float | None = None
    value_usd: float | None = None
    price_usd: float | None = None
    percentage: float | None = None


class WalletBalances(CamelModel):
    """All token balances for a wallet."""

    items: list[TokenBalance] = []
    total_value_usd: float | None = None


class NativeBalance(CamelModel):
    """Native coin balance for a wallet."""

    balance: str
    balance_formatted: float | None = None
    symbol: str | None = None
    value_usd: float | None = None
    price_usd: float | None = None


class WalletSummary(CamelModel):
    """Summary information for a wallet address."""

    address: str
    chain_id: int | None = None
    total_transactions: int | None = None
    first_seen: datetime | None = None
    last_seen: datetime | None = None
    total_value_usd: float | None = None
    is_contract: bool | None = None
    label: str | None = None
