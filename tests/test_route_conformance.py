"""Every request the SDK can make must be a route the API serves (routes exported from the API's own OpenAPI document)."""

from __future__ import annotations

import re
from pathlib import Path

from tests.recorded import recording_client

A = "0xdac17f958d2ee523a2206206994597c13d831ec7"
H = "0x" + "ab" * 32


def _routes() -> list[tuple[str, re.Pattern[str]]]:
    out = []
    for line in (
        (Path(__file__).parent / "fixtures" / "server-routes.txt")
        .read_text(encoding="utf-8")
        .split("\n")
    ):
        if line.strip():
            method, path = line.split(" ")
            out.append((method, re.compile("^" + re.sub(r"\{[^/}]+\}", "[^/]+", path) + "$")))
    return out


def test_every_sdk_request_is_a_served_route() -> None:
    client, seen = recording_client({})
    calls = [
        lambda: client.prices.by_symbol("BTC", date="2026-11-10"),
        lambda: client.prices.by_contract("ethereum", A, date="2026-11-10"),
        lambda: client.prices.batch(["BTC"], "2026-11-10"),
        lambda: client.prices.at("BTC", "2026-11-10T12:00:00Z"),
        lambda: client.fx.get_rate("EUR", "USD", "2026-11-10"),
        lambda: client.fx.get_history("EUR", from_date="2026-11-01", to_date="2026-11-10"),
        lambda: client.fx.get_monthly_average("EUR", 2026, 11),
        lambda: client.fx.list_currencies(),
        lambda: client.tokens.get_metadata("BTC"),
        lambda: client.health.get_system_status(),
        lambda: client.health.get_chain_status(),
        lambda: client.health.get_methodology(),
        lambda: client.blockchain.get_block(1, chain="ethereum"),
        lambda: client.blockchain.get_transaction(H, chain="ethereum"),
        lambda: client.blockchain.get_receipt(H, chain="ethereum"),
        lambda: client.blockchain.get_traces(H, chain="ethereum"),
        lambda: client.blockchain.get_logs(from_block=1, to_block=2, chain="ethereum"),
        lambda: client.wallets.get_history(A, chain="ethereum"),
        lambda: client.wallets.get_balances(A, chain="ethereum"),
        lambda: client.wallets.get_native_balance(A, chain="ethereum"),
        lambda: client.wallets.get_erc20_transfers(A, chain="ethereum"),
        lambda: client.wallets.get_nft_transfers(A, chain="ethereum"),
        lambda: client.wallets.get_native_transfers(A, chain="ethereum"),
        lambda: client.screening.screen_address(A, chain="ethereum"),
        lambda: client.screening.screen_bulk([{"address": A, "chain": "ethereum"}]),
    ]
    for call in calls:
        try:
            call()
        except Exception:  # noqa: BLE001, S110  # bodies are empty here; only the request is under test
            pass
    assert len(seen) == len(calls)
    routes = _routes()
    unknown = [
        f"{m} {p}" for m, p, _ in seen if not any(m == rm and rx.match(p) for rm, rx in routes)
    ]
    assert unknown == [], f"SDK calls routes the API does not serve: {unknown}"
