# Changelog

## 0.1.2

0.1.1 called routes the API does not serve. Every request is now checked against the API's own route list
(`tests/test_route_conformance.py`) and the price, FX and token calls against bodies recorded from the live routes (`tests/fixtures`).

Fixed (breaking where noted, because the old calls never worked):
- `prices.by_symbol` -> `GET /v1/prices/{symbol}/fair-value`; `PriceResponse` is the real body (`fair_value_level` is 1/2/3, `close_final`, ...).
- `prices.by_contract(chain, address)` -> `GET /v1/prices/by-contract/{chain}/{address}/fair-value`; `chain` is a slug or a known chain id.
- `prices.batch(symbols, date, currency=)` is `GET /v1/prices/batch` (1-500 symbols, one date); returns `BatchPriceResponse.prices`, a map symbol -> price. (breaking)
- `prices.at` -> `GET /v1/prices/{symbol}/at`; the timestamp may be ISO text, epoch seconds or a datetime.
- `tokens.get_metadata` -> `GET /v1/prices/tokens/{symbol}`; `TokenMetadata` is the real record. (breaking)
- `fx.get_monthly_average` sends `month=YYYY-MM`; the FX types are the real bodies. (breaking: `CurrencyInfo` removed)
- `health.get_system_status` -> `GET /v1/status`.
- `blockchain.*` -> `/v1/chains/{chain}/...`; `get_logs` takes a block range, like the route. Wallets and screening send `chain` (slug), not `chain_id`.
- `screening.screen_address` / `screen_bulk` use `POST`; `screen_bulk` returns a list.

Removed (no such API route): `wallets.get_summary`, `health.get_chains`, the price/source enums.

Not verified: response shapes of wallets, blockchain, screening, status and methodology (no recorded fixtures); their routes are verified.
