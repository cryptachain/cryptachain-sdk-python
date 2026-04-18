"""Shared test fixtures for the CryptaChain SDK test suite."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest

from cryptachain import AsyncCryptaChain, CryptaChain


def make_mock_transport(routes: dict[str, Any]) -> httpx.MockTransport:
    """Create an httpx MockTransport that returns predefined responses.

    Args:
        routes: Dict mapping (method, path) tuples or path strings to response data.
            Values can be:
            - dict/list: returned as JSON with 200 status
            - tuple of (status_code, body_dict): returned with that status
    """

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        method = request.method.upper()

        # Try (method, path) first, then just path
        for key in [(method, path), path]:
            if key in routes:
                value = routes[key]
                if isinstance(value, tuple):
                    status_code, body = value
                    return httpx.Response(
                        status_code,
                        json=body,
                        headers={"Content-Type": "application/json"},
                    )
                return httpx.Response(
                    200,
                    json=value,
                    headers={"Content-Type": "application/json"},
                )

        return httpx.Response(404, json={"message": f"Not found: {method} {path}"})

    return httpx.MockTransport(handler)


@pytest.fixture
def mock_client(request: pytest.FixtureRequest) -> CryptaChain:
    """Create a CryptaChain client backed by a MockTransport.

    Use via indirect parametrize or by setting `routes` on the test.
    """
    routes = getattr(request, "param", {})
    transport = make_mock_transport(routes)
    client = CryptaChain.__new__(CryptaChain)
    from cryptachain.client import HttpClient
    from cryptachain.config import Config

    config = Config(api_key="test-key", base_url="https://api.cryptachain.com")
    http_client = HttpClient.__new__(HttpClient)
    http_client._config = config
    http_client._client = httpx.Client(
        base_url="https://api.cryptachain.com",
        headers=config.get_headers(),
        transport=transport,
    )
    client._config = config
    client._http = http_client

    from cryptachain.resources.wallets import WalletResource
    from cryptachain.resources.prices import PriceResource
    from cryptachain.resources.fx import FxResource
    from cryptachain.resources.screening import ScreeningResource
    from cryptachain.resources.tokens import TokenResource
    from cryptachain.resources.blockchain import BlockchainResource
    from cryptachain.resources.health import HealthResource

    client.wallets = WalletResource(http_client)
    client.prices = PriceResource(http_client)
    client.fx = FxResource(http_client)
    client.screening = ScreeningResource(http_client)
    client.tokens = TokenResource(http_client)
    client.blockchain = BlockchainResource(http_client)
    client.health = HealthResource(http_client)

    return client


def create_test_client(routes: dict[str, Any]) -> CryptaChain:
    """Helper to create a test client with mock routes inline."""
    transport = make_mock_transport(routes)
    client = CryptaChain.__new__(CryptaChain)
    from cryptachain.client import HttpClient
    from cryptachain.config import Config

    config = Config(api_key="test-key", base_url="https://api.cryptachain.com")
    http_client = HttpClient.__new__(HttpClient)
    http_client._config = config
    http_client._client = httpx.Client(
        base_url="https://api.cryptachain.com",
        headers=config.get_headers(),
        transport=transport,
    )
    client._config = config
    client._http = http_client

    from cryptachain.resources.wallets import WalletResource
    from cryptachain.resources.prices import PriceResource
    from cryptachain.resources.fx import FxResource
    from cryptachain.resources.screening import ScreeningResource
    from cryptachain.resources.tokens import TokenResource
    from cryptachain.resources.blockchain import BlockchainResource
    from cryptachain.resources.health import HealthResource

    client.wallets = WalletResource(http_client)
    client.prices = PriceResource(http_client)
    client.fx = FxResource(http_client)
    client.screening = ScreeningResource(http_client)
    client.tokens = TokenResource(http_client)
    client.blockchain = BlockchainResource(http_client)
    client.health = HealthResource(http_client)

    return client
