"""Common types shared across the SDK."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class CamelModel(BaseModel):
    """Base model with camelCase alias generation from snake_case fields."""

    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=lambda s: "".join(
            word.capitalize() if i > 0 else word
            for i, word in enumerate(s.split("_"))
        ),
    )


class Pagination(CamelModel):
    """Pagination metadata."""

    cursor: str | None = None
    has_more: bool = False
    total: int | None = None
    limit: int | None = None


class Chain(CamelModel):
    """Blockchain chain information."""

    chain_id: int
    name: str
    symbol: str
    is_evm: bool = True
    is_testnet: bool = False
    explorer_url: str | None = None
    icon_url: str | None = None


class Address(CamelModel):
    """A blockchain address."""

    address: str
    chain_id: int | None = None
    chain_name: str | None = None
    is_contract: bool | None = None
    label: str | None = None
