"""Blockchain resource — blocks, transactions, receipts, traces, logs."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cryptachain.types.blockchain import Block, LogEntry, Receipt, Trace, Transaction
from cryptachain.utils.chain import resolve_chain_slug

if TYPE_CHECKING:
    from cryptachain.client import AsyncHttpClient, HttpClient


class BlockchainResource:
    """Synchronous blockchain data operations.

    Access via ``client.blockchain``.
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get_block(self, block_number: int, *, chain: str | int = 1) -> Block:
        """Get block data by block number.

        Args:
            block_number: The block number.
            chain: Chain name or chain ID (default: Ethereum mainnet).

        Returns:
            Block with header data and transaction count.
        """
        slug = resolve_chain_slug(chain)
        data = self._http.get(f"/v1/chains/{slug}/blocks/{block_number}")
        return Block.model_validate(data)

    def get_transaction(self, tx_hash: str, *, chain: str | int = 1) -> Transaction:
        """Get transaction data by hash.

        Args:
            tx_hash: Transaction hash.
            chain: Chain name or chain ID.

        Returns:
            Transaction with sender, receiver, value, and gas data.
        """
        slug = resolve_chain_slug(chain)
        data = self._http.get(f"/v1/chains/{slug}/transactions/{tx_hash}")
        return Transaction.model_validate(data)

    def get_receipt(self, tx_hash: str, *, chain: str | int = 1) -> Receipt:
        """Get transaction receipt with logs.

        Args:
            tx_hash: Transaction hash.
            chain: Chain name or chain ID.

        Returns:
            Receipt with status, gas used, and log entries.
        """
        slug = resolve_chain_slug(chain)
        data = self._http.get(f"/v1/chains/{slug}/transactions/{tx_hash}/receipt")
        return Receipt.model_validate(data)

    def get_traces(self, tx_hash: str, *, chain: str | int = 1) -> list[Trace]:
        """Get internal transaction traces.

        Args:
            tx_hash: Transaction hash.
            chain: Chain name or chain ID.

        Returns:
            List of Trace objects representing internal calls.
        """
        slug = resolve_chain_slug(chain)
        data = self._http.get(f"/v1/chains/{slug}/transactions/{tx_hash}/traces")
        items = data.get("traces", data) if isinstance(data, dict) else data
        return [Trace.model_validate(t) for t in items]

    def get_logs(
        self,
        *,
        from_block: int,
        to_block: int,
        chain: str | int = 1,
        address: str | None = None,
        topics: list[str] | None = None,
    ) -> list[LogEntry]:
        """Get event logs for a block range (``GET /v1/chains/{chain}/logs``)."""
        params: dict[str, Any] = {"from_block": from_block, "to_block": to_block}
        if address:
            params["address"] = address
        if topics:
            params["topics"] = ",".join(topics)
        data = self._http.get(f"/v1/chains/{resolve_chain_slug(chain)}/logs", params=params)
        items = data.get("logs", data) if isinstance(data, dict) else data
        return [LogEntry.model_validate(log) for log in items]


class AsyncBlockchainResource:
    """Asynchronous blockchain data operations.

    Access via ``client.blockchain`` on an ``AsyncCryptaChain`` instance.
    """

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get_block(self, block_number: int, *, chain: str | int = 1) -> Block:
        """Get block data by block number."""
        slug = resolve_chain_slug(chain)
        data = await self._http.get(f"/v1/chains/{slug}/blocks/{block_number}")
        return Block.model_validate(data)

    async def get_transaction(self, tx_hash: str, *, chain: str | int = 1) -> Transaction:
        """Get transaction data by hash."""
        slug = resolve_chain_slug(chain)
        data = await self._http.get(f"/v1/chains/{slug}/transactions/{tx_hash}")
        return Transaction.model_validate(data)

    async def get_receipt(self, tx_hash: str, *, chain: str | int = 1) -> Receipt:
        """Get transaction receipt with logs."""
        slug = resolve_chain_slug(chain)
        data = await self._http.get(f"/v1/chains/{slug}/transactions/{tx_hash}/receipt")
        return Receipt.model_validate(data)

    async def get_traces(self, tx_hash: str, *, chain: str | int = 1) -> list[Trace]:
        """Get internal transaction traces."""
        slug = resolve_chain_slug(chain)
        data = await self._http.get(f"/v1/chains/{slug}/transactions/{tx_hash}/traces")
        items = data.get("traces", data) if isinstance(data, dict) else data
        return [Trace.model_validate(t) for t in items]

    async def get_logs(
        self,
        *,
        from_block: int,
        to_block: int,
        chain: str | int = 1,
        address: str | None = None,
        topics: list[str] | None = None,
    ) -> list[LogEntry]:
        """Get event logs for a block range (``GET /v1/chains/{chain}/logs``)."""
        params: dict[str, Any] = {"from_block": from_block, "to_block": to_block}
        if address:
            params["address"] = address
        if topics:
            params["topics"] = ",".join(topics)
        data = await self._http.get(f"/v1/chains/{resolve_chain_slug(chain)}/logs", params=params)
        items = data.get("logs", data) if isinstance(data, dict) else data
        return [LogEntry.model_validate(log) for log in items]
