"""Price lookup examples — symbol, contract, and timestamp-based."""

from cryptachain import CryptaChain

client = CryptaChain(api_key="your-api-key")

# Price by symbol
price = client.prices.by_symbol("BTC", date="2026-04-04", currency="EUR")
print(f"BTC on 2026-04-04:")
print(f"  Price (EUR): {price.price:,.2f}")
print(f"  Price (USD): {price.price_usd:,.2f}")
print(f"  FX Rate: {price.fx_rate}")
print(f"  Source: {price.source}")
print(f"  Quality Score: {price.quality_score}/100")
print(f"  Fair Value Level: {price.fair_value_level}")
print(f"  Stablecoin: {price.stablecoin_pegged}")

# Price by contract address (e.g., USDC on Ethereum)
print("\nUSDC by contract:")
usdc_price = client.prices.by_contract(
    "ethereum",
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    date="2026-04-04",
    currency="USD",
)
print(f"  Price: ${usdc_price.price}")
print(f"  Stablecoin pegged: {usdc_price.stablecoin_pegged}")

# Price at exact timestamp (1-minute precision via ClickHouse)
import time
timestamp = int(time.time()) - 3600  # 1 hour ago
eth_price = client.prices.at("ETH", timestamp=timestamp)
print(f"\nETH 1 hour ago: ${eth_price.price:,.2f}")
print(f"  Computed at: {eth_price.computed_at}")

client.close()
