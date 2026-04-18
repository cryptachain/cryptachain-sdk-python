"""Chain name/ID resolution utilities."""

from __future__ import annotations

# Common chain name -> chain ID mapping
_CHAIN_MAP: dict[str, int] = {
    "ethereum": 1,
    "eth": 1,
    "polygon": 137,
    "matic": 137,
    "bsc": 56,
    "binance": 56,
    "arbitrum": 42161,
    "arb": 42161,
    "optimism": 10,
    "op": 10,
    "avalanche": 43114,
    "avax": 43114,
    "fantom": 250,
    "ftm": 250,
    "base": 8453,
    "zksync": 324,
    "linea": 59144,
    "scroll": 534352,
    "blast": 81457,
    "mantle": 5000,
    "celo": 42220,
    "gnosis": 100,
    "moonbeam": 1284,
    "moonriver": 1285,
    "cronos": 25,
    "aurora": 1313161554,
    "harmony": 1666600000,
}

_ID_TO_NAME: dict[int, str] = {v: k for k, v in _CHAIN_MAP.items()}


def chain_name_to_id(name: str) -> int | None:
    """Convert a chain name to its chain ID.

    Args:
        name: Chain name (case-insensitive), e.g. "ethereum", "polygon".

    Returns:
        The chain ID, or None if not found.
    """
    return _CHAIN_MAP.get(name.lower())


def resolve_chain(chain: str | int) -> str:
    """Resolve a chain identifier to a query parameter value.

    Accepts either a chain name (str) or chain ID (int) and returns
    a string suitable for API query parameters.

    Args:
        chain: Chain name or chain ID.

    Returns:
        String representation for the API.
    """
    if isinstance(chain, int):
        return str(chain)
    # If it looks like a number, return as-is
    try:
        int(chain)
        return chain
    except ValueError:
        pass
    # Try to resolve name to ID
    chain_id = chain_name_to_id(chain)
    if chain_id is not None:
        return str(chain_id)
    # Return as-is (let the API decide)
    return chain
