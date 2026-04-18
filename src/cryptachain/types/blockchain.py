"""Blockchain data types — blocks, transactions, receipts, traces."""

from __future__ import annotations

from datetime import datetime

from cryptachain.types.common import CamelModel


class Block(CamelModel):
    """A blockchain block."""

    block_number: int
    block_hash: str
    parent_hash: str | None = None
    timestamp: datetime | None = None
    miner: str | None = None
    gas_used: int | None = None
    gas_limit: int | None = None
    transaction_count: int | None = None
    base_fee_per_gas: str | None = None


class Transaction(CamelModel):
    """A blockchain transaction."""

    tx_hash: str
    block_number: int
    timestamp: datetime | None = None
    from_address: str
    to_address: str | None = None
    value: str
    gas: int | None = None
    gas_price: str | None = None
    nonce: int | None = None
    input_data: str | None = None
    status: str | None = None


class LogEntry(CamelModel):
    """A single log entry from a transaction receipt."""

    log_index: int
    address: str
    topics: list[str] = []
    data: str | None = None


class Receipt(CamelModel):
    """A transaction receipt."""

    tx_hash: str
    block_number: int
    status: int | None = None  # 1 = success, 0 = reverted
    gas_used: int | None = None
    effective_gas_price: str | None = None
    contract_address: str | None = None
    logs: list[LogEntry] = []


class Trace(CamelModel):
    """An internal transaction trace."""

    tx_hash: str
    trace_type: str | None = None  # CALL, CREATE, DELEGATECALL, etc.
    from_address: str | None = None
    to_address: str | None = None
    value: str | None = None
    gas: int | None = None
    gas_used: int | None = None
    input_data: str | None = None
    output: str | None = None
    error: str | None = None
    subtraces: int | None = None
