"""FX rate examples — spot rates, history, and IAS 21 monthly averages."""

from datetime import date

from cryptachain import CryptaChain

client = CryptaChain(api_key="your-api-key")

# Single FX rate
rate = client.fx.get_rate("EUR", "USD", date(2026, 4, 4))
print(f"EUR/USD on {rate.date}: {rate.rate}")
print(f"  Source: {rate.source}")
print(f"  Business day: {rate.is_business_day}")

# FX history over a range
print("\nEUR/USD daily rates (Apr 1-4, 2026):")
history = client.fx.get_history("EUR", from_date="2026-04-01", to_date="2026-04-04")
for fx_rate in history.rates:
    print(f"  {fx_rate.date}: {fx_rate.rate:.4f} ({fx_rate.source})")

# IAS 21 monthly average (for accounting)
avg = client.fx.get_monthly_average("EUR", 2026, 4)
print(f"\nIAS 21 Monthly Average for EUR ({avg.year}-{avg.month:02d}):")
print(f"  Average rate: {avg.average_rate:.4f}")
print(f"  Business days: {avg.business_days}/{avg.days_in_month}")
print(f"  Source: {avg.source}")

# List all supported currencies
currencies = client.fx.list_currencies()
print(f"\n{currencies.count} supported currencies:")
for c in currencies.currencies:
    peg = f" (pegged to USD @ {c.peg_ratio})" if c.pegged_to_usd else ""
    print(f"  {c.code} — {c.name}{peg}")

client.close()
