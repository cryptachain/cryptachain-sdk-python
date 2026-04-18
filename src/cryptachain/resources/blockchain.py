"""Blockchain resource — blocks, transactions, receipts, traces, logs."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cryptachain.types.blockchain import Block, LogEntry, Receipt, Trace, Transaction
from cryptachain.utils.chain import resolve_chain

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
        params: dict[str, Any] = {
            "chain_id": resolve_chain(chain),
            "block_number": block_number,
        }
        data = self._http.get("/v1/blocks", params=params)
        return Block.model_validate(data)

    def get_transaction(self, tx_hash: str, *, chain: str | int = 1) -> Transaction:
        """Get transaction data by hash.

        Args:
            tx_hash: Transaction hash.
            chain: Chain name or chain ID.

        Returns:
            Transaction with sender, receiver, value, and gas data.
        """
        params: dict[str, Any] = {"chain_id": resolve_chain(chain)}
        data = self._http.get(f"/v1/transactions/{tx_hash}", params=params)
        return Transaction.model_validate(data)

    def get_receipt(self, tx_hash: str, *, chain: str | int = 1) -> Receipt:
        """Get transaction receipt with logs.

        Args:
            tx_hash: Transaction hash.
            chain: Chain name or chain ID.

        Returns:
            Receipt with status, gas used, and log entries.
        """
        params: dict[str, Any] = {"chain_id": resolve_chain(chain)}
        data = self._http.get(f"/v1/transactions/{tx_hash}/receipt", params=params)
        return Receipt.model_validate(data)

    def get_traces(self, tx_hash: str, *, chain: str | int = 1) -> list[Trace]:
        """Get internal transaction traces.

        Args:
            tx_hash: Transaction hash.
            chain: Chain name or chain ID.

        Returns:
            List of Trace objects representing internal calls.
        """
        params: dict[str, Any] = {"chain_id": resolve_chain(chain)}
        data = self._http.get(f"/v1/transactions/{tx_hash}/traces", params=params)
        items = data.get("traces", data) if isinstance(data, dict) else data
        return [Trace.model_validate(t) for t in items]

    def get_logs(
        self,
        tx_hash: str,
        *,
        chain: str | int = 1,
    ) -> list[LogEntry]:
        """Get event logs for a transaction.

        Args:
            tx_hash: Transaction hash.
            chain: Chain name or chain ID.

        Returns:
            List of LogEntry objects.
        """
        params: dict[str, Any] = {"chain_id": resolve_chain(chain)}
        data = self._http.get(f"/v1/transactions/{tx_hash}/logs", params=params)
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
        params: dict[str, Any] = {
            "chain_id": resolve_chain(chain),
            "block_number": block_number,
        }
        data = await self._http.get("/v1/blocks", params=params)
        return Block.model_validate(data)

    async def get_transaction(self, tx_hash: str, *, chain: str | int = 1) -> Transaction:
        """Get transaction data by hash."""
        params: dict[str, Any] = {"chain_id": resolve_chain(chain)}
        data = await self._http.get(f"/v1/transactions/{tx_hash}", params=params)
        return Transaction.model_validate(data)

    async def get_receipt(self, tx_hash: str, *, chain: str | int = 1) -> Receipt:
        """Get transaction receipt with logs."""
        params: dict[str, Any] = {"chain_id": resolve_chain(chain)}
        data = await self._http.get(f"/v1/transactions/{tx_hash}/receipt", params=params)
        return Receipt.model_validate(data)

    async def get_traces(self, tx_hash: str, *, chain: str | int = 1) -> list[Trace]:
        """Get internal transaction traces."""
        params: dict[str, Any] = {"chain_id": resolve_chain(chain)}
        data = await self._http.get(f"/v1/transactions/{tx_hash}/traces", params=params)
        items = data.get("traces", data) if isinstance(data, dict) else data
        return [Trace.model_validate(t) for t in items]

    async def get_logs(self, tx_hash: str, *, chain: str | int = 1) -> list[LogEntry]:
        """Get event logs for a transaction."""
        params: dict[str, Any] = {"chain_id": resolve_chain(chain)}
        data = await self._http.get(f"/v1/transactions/{tx_hash}/logs", params=params)
        items = data.get("logs", data) if isinstance(data, dict) else data
        return [LogEntry.model_validate(log) for log in items]
