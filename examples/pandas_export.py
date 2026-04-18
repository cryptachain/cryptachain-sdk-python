"""Export wallet transfers to a pandas DataFrame for analysis."""

from cryptachain import CryptaChain

# Requires: pip install cryptachain[pandas]
client = CryptaChain(api_key="your-api-key")

address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

# Export all transfers to a DataFrame
df = client.wallets.to_dataframe(address, chain="ethereum")

# Display summary
print(f"Total transfers: {len(df)}")
print(f"\nColumns: {list(df.columns)}\n")

# Show recent transfers
print(df[["timestamp", "direction", "value_formatted", "value_usd_at_time", "asset_symbol"]].head(20))

# Analyze by direction
print("\n--- Summary by direction ---")
print(df.groupby("direction")["value_usd_at_time"].agg(["count", "sum", "mean"]))

# Filter to only incoming ETH
eth_incoming = df[(df["asset_symbol"] == "ETH") & (df["direction"] == "IN")]
print(f"\nIncoming ETH transfers: {len(eth_incoming)}")
if not eth_incoming.empty:
    print(f"Total ETH received: {eth_incoming['value_formatted'].sum():.4f}")

# Export to CSV
df.to_csv("transfers.csv", index=False)
print("\nExported to transfers.csv")

client.close()
