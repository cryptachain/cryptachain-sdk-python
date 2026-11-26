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


# Slugs the API accepts (the API's own chain registry), keyed by numeric chain id.
_ID_TO_SLUG: dict[int, str] = {
    1: "ethereum",
    61: "ethereum-classic",
    56: "bsc",
    137: "polygon",
    42161: "arbitrum",
    10: "optimism",
    8453: "base",
    43114: "avalanche",
    250: "fantom",
    100: "gnosis",
    42220: "celo",
    59144: "linea",
    534352: "scroll",
    324: "zksync",
    1101: "polygon-zkevm",
    5000: "mantle",
    81457: "blast",
    34443: "mode",
    169: "manta",
    1284: "moonbeam",
    1285: "moonriver",
    25: "cronos",
    1313161554: "aurora",
    1666600000: "harmony",
    1088: "metis",
    288: "boba",
    2222: "kava",
    7700: "canto",
    7777777: "zora",
    185: "mint",
    2818: "morph",
    1135: "lisk",
    1868: "soneium",
    480: "world-chain",
    13371: "immutable-zkevm",
    57073: "ink",
    60808: "bob",
    0: "bitcoin",
}
_SLUGS = set(_ID_TO_SLUG.values())


def resolve_chain_slug(chain: str | int) -> str:
    """Return the chain slug the API expects (``ethereum``, ``bsc``, ...).

    A slug is used as given (lower-cased). A numeric chain id, or a known alias such as ``eth``
    or ``matic``, is converted. Raises ``ValueError`` instead of sending a request the API would refuse.
    """
    if isinstance(chain, int) or (isinstance(chain, str) and chain.strip().isdigit()):
        chain_id = int(chain)
        slug = _ID_TO_SLUG.get(chain_id)
        if slug is None:
            raise ValueError(
                f"Unknown chain id {chain_id}: pass the chain slug (for example 'ethereum')"
            )
        return slug
    name = str(chain).strip().lower()
    if name in _SLUGS:
        return name
    alias_id = _CHAIN_MAP.get(name)
    if alias_id is not None and alias_id in _ID_TO_SLUG:
        return _ID_TO_SLUG[alias_id]
    raise ValueError(f"Unknown chain {chain!r}: pass the chain slug (for example 'ethereum')")
