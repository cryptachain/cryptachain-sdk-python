"""Basic usage example for the CryptaChain Python SDK."""

from cryptachain import CryptaChain

# Initialize the client
client = CryptaChain(api_key="your-api-key")

# Get wallet balances
balances = client.wallets.get_balances(
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    chain="ethereum",
)
print(f"Total portfolio value: ${balances.total_value_usd:,.2f}")
for token in balances.items:
    print(f"  {token.asset.symbol}: {token.balance_formatted} (${token.value_usd:,.2f})")

# Using context manager for automatic cleanup
with CryptaChain(api_key="your-api-key") as client:
    # Get system health
    status = client.health.get_system_status()
    print(f"\nAPI status: {status.status}")


    # Get token metadata
    btc = client.tokens.get_metadata("BTC")
    print(f"\nBTC: {btc.name} ({btc.category})")
