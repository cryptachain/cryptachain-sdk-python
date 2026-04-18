"""Wallet transfer history example — streaming all transfers with auto-pagination."""

from cryptachain import CryptaChain
from cryptachain.utils import truncate_address

client = CryptaChain(api_key="your-api-key")
address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"

# Get a single page of history
history = client.wallets.get_history(address, chain="ethereum", limit=10)
print(f"Total transfers: {history.total}")
print(f"Showing first {len(history.items)} results:\n")

for tx in history.items:
    symbol = tx.asset.symbol if tx.asset else "?"
    print(f"  {tx.timestamp} | {tx.direction:3s} | {tx.value_formatted} {symbol}")

# Stream ALL transfers using auto-pagination
print("\n--- Streaming all transfers ---\n")
count = 0
for transfer in client.wallets.iter_all_transfers(address, chain="polygon"):
    from_addr = truncate_address(transfer.from_address)
    to_addr = truncate_address(transfer.to_address)
    print(f"  {transfer.timestamp} {from_addr} -> {to_addr}: {transfer.value_formatted}")
    count += 1
    if count >= 50:
        print(f"  ... (stopping after 50 for demo)")
        break

print(f"\nProcessed {count} transfers.")
client.close()
