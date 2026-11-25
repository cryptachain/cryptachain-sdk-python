"""FX resource: routes and bodies recorded from the live API."""

from __future__ import annotations

from tests.recorded import fixture, recording_client


def test_get_rate() -> None:
    client, seen = recording_client({"/v1/fx/rate": fixture("fx_rate")})
    r = client.fx.get_rate("EUR", "USD", "2026-11-10")
    assert seen == [("GET", "/v1/fx/rate", {"from": "EUR", "to": "USD", "date": "2026-11-10"})]
    assert r.from_currency == "EUR" and r.rate == 1.1


def test_get_history() -> None:
    client, _ = recording_client({"/v1/fx/history": fixture("fx_history")})
    h = client.fx.get_history("EUR", from_date="2026-11-01", to_date="2026-11-10")
    assert h.base_currency == "USD" and h.from_date == "2026-11-01"
    assert h.rates[0].value == 1.01 and h.rates[0].carried_forward is False


def test_get_monthly_average_sends_month_as_yyyy_mm() -> None:
    client, seen = recording_client({"/v1/fx/monthly-average": fixture("fx_monthly_average")})
    a = client.fx.get_monthly_average("EUR", 2026, 11)
    assert seen[0][2] == {"currency": "EUR", "month": "2026-11"}
    assert a.avg_rate == 1.055 and a.days_in_average == 10 and a.is_live


def test_list_currencies() -> None:
    client, _ = recording_client({"/v1/fx/currencies": fixture("fx_currencies")})
    r = client.fx.list_currencies()
    assert r.total == 35 and "EUR" in r.currencies and "AED" in r.pegged
