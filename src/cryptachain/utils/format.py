"""Formatting utility functions."""

from __future__ import annotations

from decimal import Decimal


def format_wei(value: str | int, decimals: int = 18) -> str:
    """Convert a raw wei/token value to a human-readable decimal string.

    Args:
        value: Raw integer value as string or int.
        decimals: Number of decimal places for the token (default 18 for ETH).

    Returns:
        Formatted decimal string, e.g. "1.234567890000000000".
    """
    d = Decimal(str(value))
    factor = Decimal(10) ** decimals
    result = d / factor
    return str(result)


def truncate_address(address: str, prefix: int = 6, suffix: int = 4) -> str:
    """Truncate a blockchain address for display.

    Args:
        address: Full address string.
        prefix: Number of characters to keep at the start.
        suffix: Number of characters to keep at the end.

    Returns:
        Truncated address, e.g. "0xd8dA...6045".
    """
    if len(address) <= prefix + suffix + 3:
        return address
    return f"{address[:prefix]}...{address[-suffix:]}"
