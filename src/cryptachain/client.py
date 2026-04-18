"""Main CryptaChain SDK client — sync and async."""

from __future__ import annotations

from types import TracebackType
from typing import Any, Type

import httpx

from cryptachain.config import Config
from cryptachain.resources.blockchain import AsyncBlockchainResource, BlockchainResource
from cryptachain.resources.fx import AsyncFxResource, FxResource
from cryptachain.resources.health import AsyncHealthResource, HealthResource
from cryptachain.resources.prices import AsyncPriceResource, PriceResource
from cryptachain.resources.screening import AsyncScreeningResource, ScreeningResource
from cryptachain.resources.tokens import AsyncTokenResource, TokenResource
from cryptachain.resources.wallets import AsyncWalletResource, WalletResource
from cryptachain.retry import async_execute_with_retry, execute_with_retry, raise_for_status


class HttpClient:
    """Synchronous HTTP client wrapper for the CryptaChain API.

    Handles URL construction, authentication headers, JSON parsing,
    error mapping, timeout configuration, and retry logic.
    """

    def __init__(self, config: Config) -> None:
        self._config = config
        self._client = httpx.Client(
            base_url=config.base_url,
            headers=config.get_headers(),
            timeout=config.timeout,
        )

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send a GET request and return parsed JSON.

        Args:
            path: API path (e.g. "/v1/wallets/0x.../balances").
            params: Optional query parameters.

        Returns:
            Parsed JSON response as a dictionary.
        """
        def _request() -> httpx.Response:
            return self._client.get(path, params=params)

        response = execute_with_retry(self._config, _request)
        return response.json()  # type: ignore[no-any-return]

    def post(self, path: str, json: Any = None, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send a POST request and return parsed JSON.

        Args:
            path: API path.
            json: JSON body.
            params: Optional query parameters.

        Returns:
            Parsed JSON response as a dictionary.
        """
        def _request() -> httpx.Response:
            return self._client.post(path, json=json, params=params)

        response = execute_with_retry(self._config, _request)
        return response.json()  # type: ignore[no-any-return]

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()


class AsyncHttpClient:
    """Asynchronous HTTP client wrapper for the CryptaChain API."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._client = httpx.AsyncClient(
            base_url=config.base_url,
            headers=config.get_headers(),
            timeout=config.timeout,
        )

    async def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send an async GET request and return parsed JSON.

        Args:
            path: API path.
            params: Optional query parameters.

        Returns:
            Parsed JSON response as a dictionary.
        """
        async def _request() -> httpx.Response:
            return await self._client.get(path, params=params)

        response = await async_execute_with_retry(self._config, _request)
        return response.json()  # type: ignore[no-any-return]

    async def post(self, path: str, json: Any = None, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send an async POST request and return parsed JSON.

        Args:
            path: API path.
            json: JSON body.
            params: Optional query parameters.

        Returns:
            Parsed JSON response as a dictionary.
        """
        async def _request() -> httpx.Response:
            return await self._client.post(path, json=json, params=params)

        response = await async_execute_with_retry(self._config, _request)
        return response.json()  # type: ignore[no-any-return]

    async def close(self) -> None:
        """Close the underlying async HTTP client."""
        await self._client.aclose()


class CryptaChain:
    """Synchronous CryptaChain API client.

    Usage::

        from cryptachain import CryptaChain

        client = CryptaChain(api_key="your-api-key")
        balances = client.wallets.get_balances("0xABC...", chain="ethereum")

        # Or as a context manager:
        with CryptaChain(api_key="your-api-key") as client:
            balances = client.wallets.get_balances("0xABC...", chain="ethereum")

    Args:
        api_key: Your CryptaChain API key.
        base_url: Base URL override (default: https://api.cryptachain.com).
        timeout: Request timeout in seconds (default: 30).
        max_retries: Maximum retry attempts for retryable errors (default: 3).
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.cryptachain.com",
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        self._config = Config(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self._http = HttpClient(self._config)

        self.wallets = WalletResource(self._http)
        self.prices = PriceResource(self._http)
        self.fx = FxResource(self._http)
        self.screening = ScreeningResource(self._http)
        self.tokens = TokenResource(self._http)
        self.blockchain = BlockchainResource(self._http)
        self.health = HealthResource(self._http)

    def close(self) -> None:
        """Close the underlying HTTP client and release resources."""
        self._http.close()

    def __enter__(self) -> CryptaChain:
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()


class AsyncCryptaChain:
    """Asynchronous CryptaChain API client.

    Usage::

        from cryptachain import AsyncCryptaChain

        async with AsyncCryptaChain(api_key="your-api-key") as client:
            balances = await client.wallets.get_balances("0xABC...", chain="ethereum")

    Args:
        api_key: Your CryptaChain API key.
        base_url: Base URL override (default: https://api.cryptachain.com).
        timeout: Request timeout in seconds (default: 30).
        max_retries: Maximum retry attempts for retryable errors (default: 3).
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://api.cryptachain.com",
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        self._config = Config(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )
        self._http = AsyncHttpClient(self._config)

        self.wallets = AsyncWalletResource(self._http)
        self.prices = AsyncPriceResource(self._http)
        self.fx = AsyncFxResource(self._http)
        self.screening = AsyncScreeningResource(self._http)
        self.tokens = AsyncTokenResource(self._http)
        self.blockchain = AsyncBlockchainResource(self._http)
        self.health = AsyncHealthResource(self._http)

    async def close(self) -> None:
        """Close the underlying async HTTP client and release resources."""
        await self._http.close()

    async def __aenter__(self) -> AsyncCryptaChain:
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()
