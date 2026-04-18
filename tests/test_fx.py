"""Tests for the FX resource."""

from __future__ import annotations

from datetime import date

import pytest

from tests.conftest import create_test_client


MOCK_FX_RATE = {
    "currency": "EUR",
    "date": "2026-04-04",
    "rate": 1.0832,
    "source": "FRANKFURTER_ECB",
    "isBusinessDay": True,
    "ratedate": "2026-04-04",
}

MOCK_FX_HISTORY = {
    "currency": "EUR",
    "fromDate": "2026-04-01",
    "toDate": "2026-04-04",
    "rates": [
        {"currency": "EUR", "date": "2026-04-01", "rate": 1.0810, "source": "FRANKFURTER_ECB", "isBusinessDay": True},
        {"currency": "EUR", "date": "2026-04-02", "rate": 1.0825, "source": "FRANKFURTER_ECB", "isBusinessDay": True},
        {"currency": "EUR", "date": "2026-04-03", "rate": 1.0830, "source": "FRANKFURTER_ECB", "isBusinessDay": True},
        {"currency": "EUR", "date": "2026-04-04", "rate": 1.0832, "source": "FRANKFURTER_ECB", "isBusinessDay": True},
    ],
}

MOCK_MONTHLY_AVG = {
    "currency": "EUR",
    "year": 2026,
    "month": 4,
    "averageRate": 1.0824,
    "daysInMonth": 30,
    "businessDays": 22,
    "source": "FRANKFURTER_ECB",
    "computedAt": "2026-04-30T23:59:59Z",
}

MOCK_CURRENCIES = {
    "currencies": [
        {"code": "EUR", "name": "Euro", "source": "FRANKFURTER_ECB", "peggedToUsd": False},
        {"code": "GBP", "name": "British Pound", "source": "FRANKFURTER_ECB", "peggedToUsd": False},
        {"code": "USDT", "name": "Tether", "source": "HARDCODED_PEG", "peggedToUsd": True, "pegRatio": 1.0},
    ],
    "count": 3,
}


class TestFxResource:
    """Test suite for FX operations."""

    def test_get_rate(self) -> None:
        """get_rate returns an FxRate."""
        client = create_test_client({
            "/v1/fx/rate": MOCK_FX_RATE,
        })
        result = client.fx.get_rate("EUR", "USD", date(2026, 4, 4))
        assert result.rate == 1.0832
        assert result.source == "FRANKFURTER_ECB"
        assert result.is_business_day is True

    def test_get_history(self) -> None:
        """get_history returns FxHistoryResponse with daily rates."""
        client = create_test_client({
            "/v1/fx/history": MOCK_FX_HISTORY,
        })
        result = client.fx.get_history("EUR", from_date="2026-04-01", to_date="2026-04-04")
        assert result.currency == "EUR"
        assert len(result.rates) == 4
        assert result.rates[0].rate == 1.0810

    def test_get_monthly_average(self) -> None:
        """get_monthly_average returns IAS 21 monthly average."""
        client = create_test_client({
            "/v1/fx/monthly-average": MOCK_MONTHLY_AVG,
        })
        result = client.fx.get_monthly_average("EUR", 2026, 4)
        assert result.average_rate == 1.0824
        assert result.business_days == 22
        assert result.year == 2026
        assert result.month == 4

    def test_list_currencies(self) -> None:
        """list_currencies returns all supported currencies."""
        client = create_test_client({
            "/v1/fx/currencies": MOCK_CURRENCIES,
        })
        result = client.fx.list_currencies()
        assert result.count == 3
        assert len(result.currencies) == 3
        assert result.currencies[0].code == "EUR"
        assert result.currencies[2].pegged_to_usd is True
        assert result.currencies[2].peg_ratio == 1.0
