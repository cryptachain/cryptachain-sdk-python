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

    # List supported chains
    chains = client.health.get_chains()
    print(f"\nSupported chains ({len(chains)}):")
    for chain in chains[:5]:
        print(f"  {chain.name} (ID: {chain.chain_id})")

    # Get token metadata
    btc = client.tokens.get_metadata("BTC")
    print(f"\nBTC market cap: ${btc.market_cap_usd:,.0f}")
