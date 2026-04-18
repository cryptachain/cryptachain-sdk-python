"""Token resource — token metadata lookups."""

from __future__ import annotations

from typing import TYPE_CHECKING

from cryptachain.types.token import TokenMetadata

if TYPE_CHECKING:
    from cryptachain.client import AsyncHttpClient, HttpClient


class TokenResource:
    """Synchronous token operations.

    Access via ``client.tokens``.
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get_metadata(self, symbol: str) -> TokenMetadata:
        """Get metadata for a token by symbol.

        Args:
            symbol: Token symbol, e.g. "BTC", "ETH", "USDC".

        Returns:
            TokenMetadata with name, decimals, contract info, and more.
        """
        data = self._http.get(f"/v1/tokens/{symbol}")
        return TokenMetadata.model_validate(data)


class AsyncTokenResource:
    """Asynchronous token operations.

    Access via ``client.tokens`` on an ``AsyncCryptaChain`` instance.
    """

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get_metadata(self, symbol: str) -> TokenMetadata:
        """Get metadata for a token by symbol."""
        data = await self._http.get(f"/v1/tokens/{symbol}")
        return TokenMetadata.model_validate(data)
