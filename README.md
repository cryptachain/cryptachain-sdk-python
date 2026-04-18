# CryptaChain Python SDK

Official Python SDK for the [CryptaChain API](https://docs.cryptachain.com) — blockchain data, pricing, FX rates, and address screening.

[![PyPI version](https://img.shields.io/pypi/v/cryptachain.svg)](https://pypi.org/project/cryptachain/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Installation

```bash
pip install cryptachain
```

With optional extras:

```bash
pip install cryptachain[pandas]   # DataFrame export support
pip install cryptachain[async]    # HTTP/2 support for async client
pip install cryptachain[dev]      # Development tools (pytest, mypy, ruff)
```

## Quick Start

```python
from cryptachain import CryptaChain

client = CryptaChain(api_key="your-api-key")

# Get wallet balances
balances = client.wallets.get_balances("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", chain="ethereum")
print(f"Portfolio: ${balances.total_value_usd:,.2f}")

# Get a price
price = client.prices.by_symbol("BTC", date="2026-04-04", currency="EUR")
print(f"BTC: EUR {price.price:,.2f} (quality: {price.quality_score}/100)")

# Close when done
client.close()
```

### Context Manager

```python
with CryptaChain(api_key="your-api-key") as client:
    balances = client.wallets.get_balances("0xABC...", chain="ethereum")
```

### Async Client

```python
from cryptachain import AsyncCryptaChain

async with AsyncCryptaChain(api_key="your-api-key") as client:
    balances = await client.wallets.get_balances("0xABC...", chain="ethereum")
    
    async for transfer in client.wallets.iter_all_transfers("0xABC...", chain="ethereum"):
        print(transfer.tx_hash)
```

## API Reference

### Wallets

```python
# Transfer history (paginated)
history = client.wallets.get_history("0xABC...", chain="ethereum", limit=50)

# Stream all transfers (auto-pagination)
for transfer in client.wallets.iter_all_transfers("0xABC...", chain="polygon"):
    print(f"{transfer.timestamp} {transfer.direction} {transfer.value_formatted}")

# Token balances
balances = client.wallets.get_balances("0xABC...", chain="ethereum")

# Native balance only
native = client.wallets.get_native_balance("0xABC...", chain="ethereum")

# Filtered transfers
erc20 = client.wallets.get_erc20_transfers("0xABC...", chain="ethereum")
nft = client.wallets.get_nft_transfers("0xABC...", chain="ethereum")
native_txs = client.wallets.get_native_transfers("0xABC...", chain="ethereum")

# Wallet summary
summary = client.wallets.get_summary("0xABC...", chain="ethereum")

# Export to pandas DataFrame (requires cryptachain[pandas])
df = client.wallets.to_dataframe("0xABC...", chain="ethereum")
```

### Prices

```python
# By symbol
price = client.prices.by_symbol("BTC", date="2026-04-04", currency="EUR")

# By contract address
price = client.prices.by_contract("ethereum", "0xA0b86991c...", date="2026-04-04")

# Batch (up to 500)
batch = client.prices.batch([
    {"symbol": "BTC", "date": "2026-04-04", "currency": "EUR"},
    {"symbol": "ETH", "date": "2026-04-04", "currency": "EUR"},
])

# At exact timestamp (1-minute precision)
price = client.prices.at("ETH", timestamp=1712236800)
```

### FX Rates

```python
from datetime import date

# Single rate
rate = client.fx.get_rate("EUR", "USD", date(2026, 4, 4))

# Daily history
history = client.fx.get_history("EUR", from_date="2026-04-01", to_date="2026-04-30")

# IAS 21 monthly average
avg = client.fx.get_monthly_average("EUR", 2026, 4)

# List all 36 supported currencies
currencies = client.fx.list_currencies()
```

### Address Screening

```python
# Single address
result = client.screening.screen_address("0xSuspicious...", chain="ethereum")
if result.sanctions_match:
    print(f"SANCTIONS MATCH: {result.flags[0].description}")

# Bulk screening
bulk = client.screening.screen_bulk([
    {"address": "0xABC...", "chain_id": 1},
    {"address": "0xDEF...", "chain_id": 137},
])
```

### Tokens

```python
token = client.tokens.get_metadata("BTC")
print(f"{token.name}: ${token.market_cap_usd:,.0f}")
```

### Health & Status

```python
status = client.health.get_system_status()
chains = client.health.get_chain_status()
methodology = client.health.get_methodology()
```

## Error Handling

```python
from cryptachain import CryptaChain, CryptaChainError, RateLimitError, AuthenticationError

try:
    price = client.prices.by_symbol("BTC")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
except CryptaChainError as e:
    print(f"API error ({e.status_code}): {e.message}")
```

Exception hierarchy:
- `CryptaChainError` (base)
  - `AuthenticationError` (401)
  - `QuotaExceededError` (402)
  - `NotFoundError` (404)
    - `ChainNotFoundError`
  - `RateLimitError` (429, includes `retry_after`)
  - `ValidationError` (400/422)
  - `ServerError` (5xx)

## Retry Logic

The SDK automatically retries on transient failures (429, 5xx, timeouts) with exponential backoff:

- Default: 3 retries
- Backoff: 0.5s, 1s, 2s (with jitter)
- 429 responses respect the `Retry-After` header
- 401/402 are never retried

Configure via constructor:

```python
client = CryptaChain(
    api_key="your-key",
    max_retries=5,
    timeout=60.0,
)
```

## Utilities

```python
from cryptachain.utils import (
    is_evm_address,
    normalize_address,
    chain_name_to_id,
    format_wei,
    truncate_address,
)

is_evm_address("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")  # True
normalize_address("0xD8DA6BF26964AF9D7EED9E03E53415D37AA96045")  # lowercase
chain_name_to_id("polygon")  # 137
format_wei("1500000000000000000", decimals=18)  # "1.5"
truncate_address("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")  # "0xd8dA...6045"
```

## Development

```bash
git clone https://github.com/cryptachain/cryptachain-sdk-python.git
cd cryptachain-sdk-python
pip install -e ".[dev]"
pytest -v
ruff check src/ tests/
mypy src/cryptachain/ --ignore-missing-imports
```

## License

MIT License. See [LICENSE](LICENSE) for details.
