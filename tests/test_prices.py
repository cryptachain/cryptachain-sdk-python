"""Tests for the price resource."""

from __future__ import annotations

import pytest

from tests.conftest import create_test_client


MOCK_PRICE = {
    "symbol": "BTC",
    "date": "2026-04-04",
    "currency": "EUR",
    "price": 78500.50,
    "priceUsd": 85000.00,
    "fxRate": 0.9235,
    "fxSource": "FRANKFURTER_ECB",
    "fxDate": "2026-04-04",
    "source": "CRYPTAPRICE_VWAP",
    "qualityScore": 95,
    "fairValueLevel": "LEVEL_1",
    "sourceCount": 5,
    "methodologyVersion": "2.3",
    "stablecoinPegged": False,
    "manualOverride": False,
    "computedAt": "2026-04-04T12:00:00Z",
}

MOCK_BATCH = {
    "results": [
        {
            "symbol": "BTC",
            "date": "2026-04-04",
            "currency": "EUR",
            "price": 78500.50,
            "priceUsd": 85000.00,
            "source": "CRYPTAPRICE_VWAP",
            "qualityScore": 95,
        },
        {
            "symbol": "ETH",
            "date": "2026-04-04",
            "currency": "EUR",
            "price": 2800.25,
            "priceUsd": 3032.00,
            "source": "CRYPTAPRICE_VWAP",
            "qualityScore": 92,
        },
    ],
    "errors": None,
}


class TestPriceResource:
    """Test suite for price operations."""

    def test_by_symbol(self) -> None:
        """by_symbol returns a PriceResponse with v2.3 fields."""
        client = create_test_client({
            "/v1/prices/by-symbol": MOCK_PRICE,
        })
        result = client.prices.by_symbol("BTC", date="2026-04-04", currency="EUR")
        assert result.symbol == "BTC"
        assert result.price == 78500.50
        assert result.currency == "EUR"
        assert result.quality_score == 95
        assert result.fair_value_level is not None
        assert result.fair_value_level.value == "LEVEL_1"
        assert result.source is not None
        assert result.source.value == "CRYPTAPRICE_VWAP"
        assert result.stablecoin_pegged is False

    def test_by_contract(self) -> None:
        """by_contract returns a PriceResponse."""
        client = create_test_client({
            "/v1/prices/by-contract": MOCK_PRICE,
        })
        result = client.prices.by_contract(
            "ethereum",
            "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
            date="2026-04-04",
        )
        assert result.price == 78500.50

    def test_batch(self) -> None:
        """batch returns multiple price results."""
        client = create_test_client({
            ("POST", "/v1/prices/batch"): MOCK_BATCH,
        })
        result = client.prices.batch([
            {"symbol": "BTC", "date": "2026-04-04", "currency": "EUR"},
            {"symbol": "ETH", "date": "2026-04-04", "currency": "EUR"},
        ])
        assert len(result.results) == 2
        assert result.results[0].symbol == "BTC"
        assert result.results[1].symbol == "ETH"

    def test_at_timestamp(self) -> None:
        """at returns a PriceResponse for a specific timestamp."""
        client = create_test_client({
            "/v1/prices/at": MOCK_PRICE,
        })
        result = client.prices.at("BTC", timestamp=1712236800)
        assert result.symbol == "BTC"
        assert result.price == 78500.50
