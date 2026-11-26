from __future__ import annotations

import json
from pathlib import Path

import httpx

from cryptachain import CryptaChain
from cryptachain.client import HttpClient
from cryptachain.config import Config

FIXTURES = Path(__file__).parent / "fixtures"


def fixture(name: str):
    """A body recorded from the live route."""
    return json.loads((FIXTURES / f"{name}.json").read_text(encoding="utf-8"))


def recording_client(routes: dict[str, object]):
    """A client whose transport answers ``routes`` (path -> body) and records every (method, path, query)."""
    seen: list[tuple[str, str, dict[str, str]]] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append((request.method, request.url.path, dict(request.url.params)))
        body = routes.get(request.url.path, {})
        return httpx.Response(200, json=body)

    config = Config(api_key="test-key", base_url="https://api.cryptachain.com")
    http = HttpClient.__new__(HttpClient)
    http._config = config
    http._client = httpx.Client(
        base_url=config.base_url,
        headers=config.get_headers(),
        transport=httpx.MockTransport(handler),
    )
    client = CryptaChain.__new__(CryptaChain)
    client._config = config
    client._http = http
    from cryptachain.resources.blockchain import BlockchainResource
    from cryptachain.resources.fx import FxResource
    from cryptachain.resources.health import HealthResource
    from cryptachain.resources.prices import PriceResource
    from cryptachain.resources.screening import ScreeningResource
    from cryptachain.resources.tokens import TokenResource
    from cryptachain.resources.wallets import WalletResource

    client.prices = PriceResource(http)
    client.fx = FxResource(http)
    client.tokens = TokenResource(http)
    client.health = HealthResource(http)
    client.blockchain = BlockchainResource(http)
    client.wallets = WalletResource(http)
    client.screening = ScreeningResource(http)
    return client, seen
