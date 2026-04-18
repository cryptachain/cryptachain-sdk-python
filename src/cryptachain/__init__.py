"""CryptaChain Python SDK — official client for the CryptaChain API.

Usage::

    from cryptachain import CryptaChain

    client = CryptaChain(api_key="your-api-key")
    balances = client.wallets.get_balances("0xABC...", chain="ethereum")

For async usage::

    from cryptachain import AsyncCryptaChain

    async with AsyncCryptaChain(api_key="your-api-key") as client:
        balances = await client.wallets.get_balances("0xABC...", chain="ethereum")
"""

from cryptachain.client import AsyncCryptaChain, CryptaChain
from cryptachain.errors import (
    AuthenticationError,
    ChainNotFoundError,
    CryptaChainError,
    QuotaExceededError,
    RateLimitError,
)

__version__ = "0.1.0"

__all__ = [
    "AsyncCryptaChain",
    "AuthenticationError",
    "ChainNotFoundError",
    "CryptaChain",
    "CryptaChainError",
    "QuotaExceededError",
    "RateLimitError",
]
