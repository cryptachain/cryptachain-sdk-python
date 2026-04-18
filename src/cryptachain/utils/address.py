"""Address utility functions."""

from __future__ import annotations

import re

_EVM_ADDRESS_PATTERN = re.compile(r"^0x[0-9a-fA-F]{40}$")


def is_evm_address(address: str) -> bool:
    """Check if the given string is a valid EVM address (0x + 40 hex chars).

    Args:
        address: The address string to validate.

    Returns:
        True if the address matches the EVM format.
    """
    return bool(_EVM_ADDRESS_PATTERN.match(address))


def normalize_address(address: str, chain: str | None = None) -> str:
    """Normalize a blockchain address.

    EVM addresses are lowercased. Non-EVM addresses (TRON, Solana, BTC, Cosmos)
    are returned as-is because they are case-sensitive.

    Args:
        address: The raw address string.
        chain: Optional chain name to determine normalization rules.

    Returns:
        The normalized address.
    """
    # Non-EVM chains are case-sensitive — never lowercase
    non_evm_chains = {"tron", "solana", "bitcoin", "btc", "cosmos", "litecoin", "dogecoin", "ripple"}
    if chain and chain.lower() in non_evm_chains:
        return address

    # EVM addresses: lowercase
    if is_evm_address(address):
        return address.lower()

    return address
