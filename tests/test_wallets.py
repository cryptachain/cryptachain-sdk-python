"""Tests for the wallet resource."""

from __future__ import annotations

import pytest

from tests.conftest import create_test_client


MOCK_BALANCES = {
    "items": [
        {
            "asset": {"symbol": "ETH", "name": "Ether", "decimals": 18, "tokenType": "NATIVE"},
            "balance": "1500000000000000000",
            "balanceFormatted": 1.5,
            "valueUsd": 4500.00,
            "priceUsd": 3000.00,
            "percentage": 75.0,
        },
        {
            "asset": {"symbol": "USDC", "name": "USD Coin", "decimals": 6, "tokenType": "ERC20"},
            "balance": "1500000000",
            "balanceFormatted": 1500.0,
            "valueUsd": 1500.00,
            "priceUsd": 1.00,
            "percentage": 25.0,
        },
    ],
    "totalValueUsd": 6000.00,
}

MOCK_TRANSFERS = {
    "items": [
        {
            "txHash": "0xabc123",
            "blockNumber": 12345678,
            "timestamp": "2026-04-04T12:00:00Z",
            "direction": "IN",
            "fromAddress": "0xSender",
            "toAddress": "0xReceiver",
            "value": "1000000000000000000",
            "valueFormatted": 1.0,
            "valueUsdAtTime": 3000.00,
            "asset": {"symbol": "ETH", "name": "Ether"},
        }
    ],
    "cursor": None,
    "hasMore": False,
    "total": 1,
}

MOCK_NATIVE_BALANCE = {
    "balance": "2000000000000000000",
    "balanceFormatted": 2.0,
    "symbol": "ETH",
    "valueUsd": 6000.0,
    "priceUsd": 3000.0,
}

MOCK_SUMMARY = {
    "address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
    "chainId": 1,
    "totalTransactions": 5000,
    "firstSeen": "2020-01-01T00:00:00Z",
    "lastSeen": "2026-04-04T12:00:00Z",
    "totalValueUsd": 100000.0,
    "isContract": False,
}


class TestWalletResource:
    """Test suite for wallet operations."""

    def test_get_balances(self) -> None:
        """get_balances returns parsed WalletBalances."""
        client = create_test_client({
            "/v1/wallets/0xABC/balances": MOCK_BALANCES,
        })
        result = client.wallets.get_balances("0xABC", chain="ethereum")
        assert result.total_value_usd == 6000.00
        assert len(result.items) == 2
        assert result.items[0].asset.symbol == "ETH"
        assert result.items[1].asset.symbol == "USDC"

    def test_get_history(self) -> None:
        """get_history returns parsed WalletHistory."""
        client = create_test_client({
            "/v1/wallets/0xABC/transfers": MOCK_TRANSFERS,
        })
        result = client.wallets.get_history("0xABC", chain="ethereum")
        assert result.total == 1
        assert result.has_more is False
        assert result.items[0].tx_hash == "0xabc123"
        assert result.items[0].direction == "IN"

    def test_iter_all_transfers(self) -> None:
        """iter_all_transfers yields Transfer objects from paginated results."""
        client = create_test_client({
            "/v1/wallets/0xABC/transfers": MOCK_TRANSFERS,
        })
        transfers = list(client.wallets.iter_all_transfers("0xABC", chain="ethereum"))
        assert len(transfers) == 1
        assert transfers[0].tx_hash == "0xabc123"

    def test_get_native_balance(self) -> None:
        """get_native_balance returns NativeBalance."""
        client = create_test_client({
            "/v1/wallets/0xABC/native-balance": MOCK_NATIVE_BALANCE,
        })
        result = client.wallets.get_native_balance("0xABC", chain="ethereum")
        assert result.balance_formatted == 2.0
        assert result.symbol == "ETH"

    def test_get_erc20_transfers(self) -> None:
        """get_erc20_transfers returns WalletHistory."""
        client = create_test_client({
            "/v1/wallets/0xABC/erc20-transfers": MOCK_TRANSFERS,
        })
        result = client.wallets.get_erc20_transfers("0xABC", chain="ethereum")
        assert len(result.items) == 1

    def test_get_nft_transfers(self) -> None:
        """get_nft_transfers returns WalletHistory."""
        client = create_test_client({
            "/v1/wallets/0xABC/nft-transfers": MOCK_TRANSFERS,
        })
        result = client.wallets.get_nft_transfers("0xABC", chain="ethereum")
        assert len(result.items) == 1

    def test_get_native_transfers(self) -> None:
        """get_native_transfers returns WalletHistory."""
        client = create_test_client({
            "/v1/wallets/0xABC/native-transfers": MOCK_TRANSFERS,
        })
        result = client.wallets.get_native_transfers("0xABC", chain="ethereum")
        assert len(result.items) == 1

    def test_get_summary(self) -> None:
        """get_summary returns WalletSummary."""
        client = create_test_client({
            "/v1/wallets/0xABC/summary": MOCK_SUMMARY,
        })
        result = client.wallets.get_summary("0xABC", chain="ethereum")
        assert result.total_transactions == 5000
        assert result.is_contract is False

    def test_iter_pagination(self) -> None:
        """iter_all_transfers handles multi-page pagination."""
        call_count = 0

        import httpx

        def handler(request: httpx.Request) -> httpx.Response:
            nonlocal call_count
            call_count += 1
            cursor = request.url.params.get("cursor")
            if cursor is None:
                body = {
                    "items": [
                        {
                            "txHash": "0x1",
                            "blockNumber": 1,
                            "timestamp": "2026-01-01T00:00:00Z",
                            "direction": "IN",
                            "fromAddress": "0xA",
                            "toAddress": "0xB",
                            "value": "100",
                        }
                    ],
                    "cursor": "page2",
                    "hasMore": True,
                }
            else:
                body = {
                    "items": [
                        {
                            "txHash": "0x2",
                            "blockNumber": 2,
                            "timestamp": "2026-01-02T00:00:00Z",
                            "direction": "OUT",
                            "fromAddress": "0xB",
                            "toAddress": "0xA",
                            "value": "200",
                        }
                    ],
                    "cursor": None,
                    "hasMore": False,
                }
            return httpx.Response(200, json=body, headers={"Content-Type": "application/json"})

        transport = httpx.MockTransport(handler)
        from cryptachain.client import HttpClient
        from cryptachain.config import Config
        from cryptachain.resources.wallets import WalletResource

        config = Config(api_key="test", base_url="https://api.cryptachain.com")
        http_client = HttpClient.__new__(HttpClient)
        http_client._config = config
        http_client._client = httpx.Client(
            base_url="https://api.cryptachain.com",
            headers=config.get_headers(),
            transport=transport,
        )
        wallet_resource = WalletResource(http_client)

        transfers = list(wallet_resource.iter_all_transfers("0xABC"))
        assert len(transfers) == 2
        assert transfers[0].tx_hash == "0x1"
        assert transfers[1].tx_hash == "0x2"
        assert call_count == 2
