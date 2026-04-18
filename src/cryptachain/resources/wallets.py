"""Wallet resource — transfer history, balances, and pandas export."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncIterator, Iterator

from cryptachain.pagination import async_iter_pages, iter_pages
from cryptachain.types.wallet import (
    NativeBalance,
    Transfer,
    WalletBalances,
    WalletHistory,
    WalletSummary,
)
from cryptachain.utils.chain import resolve_chain

if TYPE_CHECKING:
    from cryptachain.client import AsyncHttpClient, HttpClient


class WalletResource:
    """Synchronous wallet operations.

    Access via ``client.wallets``.
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get_history(
        self,
        address: str,
        *,
        chain: str | int | None = None,
        cursor: str | None = None,
        limit: int = 100,
    ) -> WalletHistory:
        """Get paginated transfer history for a wallet address.

        Args:
            address: Wallet address.
            chain: Chain name (e.g. "ethereum") or chain ID.
            cursor: Pagination cursor from a previous response.
            limit: Number of results per page (max 100).

        Returns:
            WalletHistory with transfers and pagination info.
        """
        params: dict[str, Any] = {"limit": limit}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)
        if cursor is not None:
            params["cursor"] = cursor
        data = self._http.get(f"/v1/wallets/{address}/transfers", params=params)
        return WalletHistory.model_validate(data)

    def iter_all_transfers(
        self,
        address: str,
        *,
        chain: str | int | None = None,
        limit: int = 100,
    ) -> Iterator[Transfer]:
        """Iterate over all transfers for a wallet, auto-paginating.

        Args:
            address: Wallet address.
            chain: Chain name or chain ID.
            limit: Page size for each request.

        Yields:
            Transfer objects across all pages.
        """
        params: dict[str, Any] = {}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)

        def fetch(p: dict[str, Any]) -> dict[str, Any]:
            return self._http.get(f"/v1/wallets/{address}/transfers", params=p)

        for item in iter_pages(fetch, params, limit=limit):
            yield Transfer.model_validate(item)

    def get_balances(
        self,
        address: str,
        *,
        chain: str | int | None = None,
    ) -> WalletBalances:
        """Get all token balances for a wallet address.

        Args:
            address: Wallet address.
            chain: Chain name or chain ID.

        Returns:
            WalletBalances with individual token balances and total USD value.
        """
        params: dict[str, Any] = {}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)
        data = self._http.get(f"/v1/wallets/{address}/balances", params=params)
        return WalletBalances.model_validate(data)

    def get_native_balance(
        self,
        address: str,
        *,
        chain: str | int | None = None,
    ) -> NativeBalance:
        """Get the native coin balance for a wallet address.

        Args:
            address: Wallet address.
            chain: Chain name or chain ID.

        Returns:
            NativeBalance with the raw and formatted balance.
        """
        params: dict[str, Any] = {}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)
        data = self._http.get(f"/v1/wallets/{address}/native-balance", params=params)
        return NativeBalance.model_validate(data)

    def get_erc20_transfers(
        self,
        address: str,
        *,
        chain: str | int | None = None,
        cursor: str | None = None,
        limit: int = 100,
    ) -> WalletHistory:
        """Get ERC-20 token transfers only.

        Args:
            address: Wallet address.
            chain: Chain name or chain ID.
            cursor: Pagination cursor.
            limit: Results per page.

        Returns:
            WalletHistory with ERC-20 transfers.
        """
        params: dict[str, Any] = {"limit": limit}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)
        if cursor is not None:
            params["cursor"] = cursor
        data = self._http.get(f"/v1/wallets/{address}/erc20-transfers", params=params)
        return WalletHistory.model_validate(data)

    def get_nft_transfers(
        self,
        address: str,
        *,
        chain: str | int | None = None,
        cursor: str | None = None,
        limit: int = 100,
    ) -> WalletHistory:
        """Get NFT transfers only.

        Args:
            address: Wallet address.
            chain: Chain name or chain ID.
            cursor: Pagination cursor.
            limit: Results per page.

        Returns:
            WalletHistory with NFT transfers.
        """
        params: dict[str, Any] = {"limit": limit}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)
        if cursor is not None:
            params["cursor"] = cursor
        data = self._http.get(f"/v1/wallets/{address}/nft-transfers", params=params)
        return WalletHistory.model_validate(data)

    def get_native_transfers(
        self,
        address: str,
        *,
        chain: str | int | None = None,
        cursor: str | None = None,
        limit: int = 100,
    ) -> WalletHistory:
        """Get native coin transfers only.

        Args:
            address: Wallet address.
            chain: Chain name or chain ID.
            cursor: Pagination cursor.
            limit: Results per page.

        Returns:
            WalletHistory with native transfers.
        """
        params: dict[str, Any] = {"limit": limit}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)
        if cursor is not None:
            params["cursor"] = cursor
        data = self._http.get(f"/v1/wallets/{address}/native-transfers", params=params)
        return WalletHistory.model_validate(data)

    def get_summary(
        self,
        address: str,
        *,
        chain: str | int | None = None,
    ) -> WalletSummary:
        """Get a summary for a wallet address.

        Args:
            address: Wallet address.
            chain: Chain name or chain ID.

        Returns:
            WalletSummary with aggregate information.
        """
        params: dict[str, Any] = {}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)
        data = self._http.get(f"/v1/wallets/{address}/summary", params=params)
        return WalletSummary.model_validate(data)

    def to_dataframe(
        self,
        address: str,
        *,
        chain: str | int | None = None,
        limit: int = 100,
    ) -> Any:
        """Export all transfers to a pandas DataFrame.

        Requires the ``pandas`` extra: ``pip install cryptachain[pandas]``.

        Args:
            address: Wallet address.
            chain: Chain name or chain ID.
            limit: Page size for pagination.

        Returns:
            A pandas DataFrame with transfer data.

        Raises:
            ImportError: If pandas is not installed.
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas is required for to_dataframe(). "
                "Install it with: pip install cryptachain[pandas]"
            ) from None

        records = []
        for transfer in self.iter_all_transfers(address, chain=chain, limit=limit):
            row = transfer.model_dump()
            # Flatten asset fields
            asset = row.pop("asset", None) or {}
            row["asset_symbol"] = asset.get("symbol")
            row["asset_name"] = asset.get("name")
            row["asset_contract"] = asset.get("contract_address")
            records.append(row)

        return pd.DataFrame(records)


class AsyncWalletResource:
    """Asynchronous wallet operations.

    Access via ``client.wallets`` on an ``AsyncCryptaChain`` instance.
    """

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get_history(
        self,
        address: str,
        *,
        chain: str | int | None = None,
        cursor: str | None = None,
        limit: int = 100,
    ) -> WalletHistory:
        """Get paginated transfer history for a wallet address.

        Args:
            address: Wallet address.
            chain: Chain name or chain ID.
            cursor: Pagination cursor.
            limit: Results per page.

        Returns:
            WalletHistory with transfers and pagination info.
        """
        params: dict[str, Any] = {"limit": limit}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)
        if cursor is not None:
            params["cursor"] = cursor
        data = await self._http.get(f"/v1/wallets/{address}/transfers", params=params)
        return WalletHistory.model_validate(data)

    async def iter_all_transfers(
        self,
        address: str,
        *,
        chain: str | int | None = None,
        limit: int = 100,
    ) -> AsyncIterator[Transfer]:
        """Iterate over all transfers for a wallet, auto-paginating.

        Args:
            address: Wallet address.
            chain: Chain name or chain ID.
            limit: Page size.

        Yields:
            Transfer objects across all pages.
        """
        params: dict[str, Any] = {}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)

        async def fetch(p: dict[str, Any]) -> dict[str, Any]:
            return await self._http.get(f"/v1/wallets/{address}/transfers", params=p)

        async for item in async_iter_pages(fetch, params, limit=limit):
            yield Transfer.model_validate(item)

    async def get_balances(
        self,
        address: str,
        *,
        chain: str | int | None = None,
    ) -> WalletBalances:
        """Get all token balances for a wallet address.

        Args:
            address: Wallet address.
            chain: Chain name or chain ID.

        Returns:
            WalletBalances with individual token balances and total USD value.
        """
        params: dict[str, Any] = {}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)
        data = await self._http.get(f"/v1/wallets/{address}/balances", params=params)
        return WalletBalances.model_validate(data)

    async def get_native_balance(
        self,
        address: str,
        *,
        chain: str | int | None = None,
    ) -> NativeBalance:
        """Get the native coin balance for a wallet address.

        Args:
            address: Wallet address.
            chain: Chain name or chain ID.

        Returns:
            NativeBalance with the raw and formatted balance.
        """
        params: dict[str, Any] = {}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)
        data = await self._http.get(f"/v1/wallets/{address}/native-balance", params=params)
        return NativeBalance.model_validate(data)

    async def get_erc20_transfers(
        self,
        address: str,
        *,
        chain: str | int | None = None,
        cursor: str | None = None,
        limit: int = 100,
    ) -> WalletHistory:
        """Get ERC-20 token transfers only."""
        params: dict[str, Any] = {"limit": limit}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)
        if cursor is not None:
            params["cursor"] = cursor
        data = await self._http.get(f"/v1/wallets/{address}/erc20-transfers", params=params)
        return WalletHistory.model_validate(data)

    async def get_nft_transfers(
        self,
        address: str,
        *,
        chain: str | int | None = None,
        cursor: str | None = None,
        limit: int = 100,
    ) -> WalletHistory:
        """Get NFT transfers only."""
        params: dict[str, Any] = {"limit": limit}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)
        if cursor is not None:
            params["cursor"] = cursor
        data = await self._http.get(f"/v1/wallets/{address}/nft-transfers", params=params)
        return WalletHistory.model_validate(data)

    async def get_native_transfers(
        self,
        address: str,
        *,
        chain: str | int | None = None,
        cursor: str | None = None,
        limit: int = 100,
    ) -> WalletHistory:
        """Get native coin transfers only."""
        params: dict[str, Any] = {"limit": limit}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)
        if cursor is not None:
            params["cursor"] = cursor
        data = await self._http.get(f"/v1/wallets/{address}/native-transfers", params=params)
        return WalletHistory.model_validate(data)

    async def get_summary(
        self,
        address: str,
        *,
        chain: str | int | None = None,
    ) -> WalletSummary:
        """Get a summary for a wallet address."""
        params: dict[str, Any] = {}
        if chain is not None:
            params["chain_id"] = resolve_chain(chain)
        data = await self._http.get(f"/v1/wallets/{address}/summary", params=params)
        return WalletSummary.model_validate(data)

    async def to_dataframe(
        self,
        address: str,
        *,
        chain: str | int | None = None,
        limit: int = 100,
    ) -> Any:
        """Export all transfers to a pandas DataFrame.

        Requires the ``pandas`` extra: ``pip install cryptachain[pandas]``.
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas is required for to_dataframe(). "
                "Install it with: pip install cryptachain[pandas]"
            ) from None

        records = []
        async for transfer in self.iter_all_transfers(address, chain=chain, limit=limit):
            row = transfer.model_dump()
            asset = row.pop("asset", None) or {}
            row["asset_symbol"] = asset.get("symbol")
            row["asset_name"] = asset.get("name")
            row["asset_contract"] = asset.get("contract_address")
            records.append(row)

        return pd.DataFrame(records)
