"""Batch price lookup example: up to 500 symbols for one date in a single request (GET /v1/prices/batch)."""

from cryptachain import CryptaChain

client = CryptaChain(api_key="your-api-key")

batch = client.prices.batch(["BTC", "ETH", "SOL", "USDC", "MATIC"], "2026-04-04", currency="EUR")

print(f"Received {len(batch.prices)} prices:\n")
for symbol, price in batch.prices.items():
    quality = price.quality_score or 0
    print(f"  {symbol:6s}  EUR {price.price:>12,.2f}  (quality: {quality}/100, level: {price.fair_value_level})")

# A symbol with no price on that date is simply absent from the result.
missing = {"BTC", "ETH", "SOL", "USDC", "MATIC"} - set(batch.prices)
if missing:
    print(f"\nNo price on that date: {', '.join(sorted(missing))}")

client.close()
