"""Price resource: routes and bodies recorded from the live API."""

from __future__ import annotations

import pytest

from tests.recorded import fixture, recording_client


def test_by_symbol_calls_fair_value_route() -> None:
    client, seen = recording_client({"/v1/prices/BTC/fair-value": fixture("price_usd")})
    p = client.prices.by_symbol("BTC", date="2026-11-10")
    assert seen == [("GET", "/v1/prices/BTC/fair-value", {"currency": "USD", "date": "2026-11-10"})]
    assert p.currency == "USD" and p.fair_value_level == 1 and p.close_final == "UNKNOWN" and p.fx_rate is None


def test_currency_returns_fx_fields() -> None:
    client, seen = recording_client({"/v1/prices/ETH/fair-value": fixture("price_eur")})
    p = client.prices.by_symbol("ETH", date="2026-11-10", currency="EUR")
    assert seen[0][2]["currency"] == "EUR"
    assert p.fx_source == "ECB" and p.fx_rate == 1.1


def test_by_contract_uses_chain_slug() -> None:
    a = "0xdac17f958d2ee523a2206206994597c13d831ec7"
    body = fixture("price_usd")
    client, seen = recording_client(
        {f"/v1/prices/by-contract/{c}/{a}/fair-value": body for c in ("ethereum", "bsc")}
    )
    client.prices.by_contract("ethereum", a, date="2026-11-10")
    client.prices.by_contract(56, a, date="2026-11-10")
    assert seen[0][1] == f"/v1/prices/by-contract/ethereum/{a}/fair-value"
    assert seen[1][1] == f"/v1/prices/by-contract/bsc/{a}/fair-value"
    with pytest.raises(ValueError):
        client.prices.by_contract(999999, a)


def test_batch_is_a_get_with_symbols_and_returns_a_map() -> None:
    client, seen = recording_client({"/v1/prices/batch": fixture("price_batch")})
    r = client.prices.batch(["BTC", "NOPE"], "2026-11-10", currency="EUR")
    assert seen == [("GET", "/v1/prices/batch", {"symbols": "BTC,NOPE", "date": "2026-11-10", "currency": "EUR"})]
    assert list(r.prices) == ["BTC"] and r.prices["BTC"].currency == "EUR"
    with pytest.raises(ValueError):
        client.prices.batch([], "2026-11-10")


def test_at_calls_at_route() -> None:
    client, seen = recording_client({"/v1/prices/BTC/at": fixture("price_at")})
    p = client.prices.at("BTC", "2026-11-10T12:00:00Z")
    assert seen[0][1] == "/v1/prices/BTC/at" and seen[0][2]["timestamp"] == "2026-11-10T12:00:00Z"
    assert p.precision == "DAILY_FALLBACK"
