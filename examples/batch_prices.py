"""Batch price lookup example — up to 500 prices in a single request."""

from cryptachain import CryptaChain

client = CryptaChain(api_key="your-api-key")

# Build a batch of price requests
requests = [
    {"symbol": "BTC", "date": "2026-04-04", "currency": "EUR"},
    {"symbol": "ETH", "date": "2026-04-04", "currency": "EUR"},
    {"symbol": "SOL", "date": "2026-04-04", "currency": "EUR"},
    {"symbol": "USDC", "date": "2026-04-04", "currency": "EUR"},
    {"symbol": "MATIC", "date": "2026-04-04", "currency": "EUR"},
]

# Single API call for all prices
batch = client.prices.batch(requests)

print(f"Received {len(batch.results)} prices:\n")
for price in batch.results:
    level = price.fair_value_level.value if price.fair_value_level else "N/A"
    quality = price.quality_score or 0
    print(f"  {price.symbol:6s}  EUR {price.price:>12,.2f}  "
          f"(quality: {quality}/100, level: {level})")

if batch.errors:
    print(f"\n{len(batch.errors)} errors:")
    for err in batch.errors:
        print(f"  {err}")

# You can also mix symbol and contract-based lookups in a batch
mixed_batch = client.prices.batch([
    {"symbol": "BTC", "date": "2026-04-04", "currency": "USD"},
    {"chain_id": 1, "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
     "date": "2026-04-04", "currency": "USD"},  # USDC by contract
])

print(f"\nMixed batch: {len(mixed_batch.results)} results")
for price in mixed_batch.results:
    print(f"  {price.symbol}: ${price.price:,.2f}")

client.close()
