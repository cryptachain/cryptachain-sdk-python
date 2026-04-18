"""Tests for the CryptaChain client — initialization, context manager, error handling."""

from __future__ import annotations

import httpx
import pytest

from cryptachain import (
    AsyncCryptaChain,
    AuthenticationError,
    CryptaChain,
    CryptaChainError,
    QuotaExceededError,
    RateLimitError,
)
from cryptachain.errors import NotFoundError, ServerError, ValidationError
from tests.conftest import create_test_client, make_mock_transport


class TestCryptaChainClient:
    """Test suite for the sync client."""

    def test_client_init(self) -> None:
        """Client initializes with api_key and has all resources."""
        client = create_test_client({})
        assert client._config.api_key == "test-key"
        assert client.wallets is not None
        assert client.prices is not None
        assert client.fx is not None
        assert client.screening is not None
        assert client.tokens is not None
        assert client.blockchain is not None
        assert client.health is not None

    def test_context_manager(self) -> None:
        """Client works as a context manager."""
        with CryptaChain(api_key="test-key") as client:
            assert client._config.api_key == "test-key"

    def test_401_raises_authentication_error(self) -> None:
        """401 responses raise AuthenticationError."""
        client = create_test_client({
            "/v1/status/services": (401, {"message": "Invalid API key"}),
        })
        with pytest.raises(AuthenticationError, match="Invalid API key"):
            client.health.get_system_status()

    def test_402_raises_quota_exceeded_error(self) -> None:
        """402 responses raise QuotaExceededError."""
        client = create_test_client({
            "/v1/prices/by-symbol": (402, {"message": "Quota exceeded"}),
        })
        with pytest.raises(QuotaExceededError, match="Quota exceeded"):
            client.prices.by_symbol("BTC")

    def test_404_raises_not_found_error(self) -> None:
        """404 responses raise NotFoundError."""
        client = create_test_client({
            "/v1/tokens/DOESNOTEXIST": (404, {"message": "Token not found"}),
        })
        with pytest.raises(NotFoundError, match="Token not found"):
            client.tokens.get_metadata("DOESNOTEXIST")

    def test_429_raises_rate_limit_error(self) -> None:
        """429 responses raise RateLimitError after retries exhausted."""
        from cryptachain.client import HttpClient
        from cryptachain.config import Config

        call_count = 0

        def handler(request: httpx.Request) -> httpx.Response:
            nonlocal call_count
            call_count += 1
            return httpx.Response(
                429,
                json={"message": "Too many requests"},
                headers={"Retry-After": "0.01", "Content-Type": "application/json"},
            )

        transport = httpx.MockTransport(handler)
        config = Config(
            api_key="test-key",
            base_url="https://api.cryptachain.com",
            max_retries=1,
            retry_base_delay=0.01,
        )
        http_client = HttpClient.__new__(HttpClient)
        http_client._config = config
        http_client._client = httpx.Client(
            base_url="https://api.cryptachain.com",
            headers=config.get_headers(),
            transport=transport,
        )

        with pytest.raises(RateLimitError):
            http_client.get("/v1/prices/by-symbol", params={"symbol": "BTC"})

        # Should have retried once (2 total attempts)
        assert call_count == 2

    def test_500_raises_server_error(self) -> None:
        """500 responses raise ServerError after retries."""
        from cryptachain.client import HttpClient
        from cryptachain.config import Config

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                500,
                json={"message": "Internal error"},
                headers={"Content-Type": "application/json"},
            )

        transport = httpx.MockTransport(handler)
        config = Config(
            api_key="test-key",
            base_url="https://api.cryptachain.com",
            max_retries=0,
        )
        http_client = HttpClient.__new__(HttpClient)
        http_client._config = config
        http_client._client = httpx.Client(
            base_url="https://api.cryptachain.com",
            headers=config.get_headers(),
            transport=transport,
        )

        with pytest.raises(ServerError):
            http_client.get("/v1/status/services")

    def test_headers_include_api_key(self) -> None:
        """Verify that X-API-Key header is set."""
        from cryptachain.config import Config
        config = Config(api_key="my-secret-key")
        headers = config.get_headers()
        assert headers["X-API-Key"] == "my-secret-key"
        assert "User-Agent" in headers
