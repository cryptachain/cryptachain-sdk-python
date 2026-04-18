"""SDK configuration."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Config:
    """Configuration for the CryptaChain SDK client.

    Attributes:
        api_key: Your CryptaChain API key.
        base_url: Base URL for the CryptaChain API.
        timeout: Request timeout in seconds.
        max_retries: Maximum number of retry attempts for retryable errors.
        retry_base_delay: Base delay in seconds for exponential backoff.
        retry_max_delay: Maximum delay in seconds between retries.
    """

    api_key: str
    base_url: str = "https://api.cryptachain.com"
    timeout: float = 30.0
    max_retries: int = 3
    retry_base_delay: float = 0.5
    retry_max_delay: float = 30.0
    headers: dict[str, str] = field(default_factory=dict)

    def get_headers(self) -> dict[str, str]:
        """Return the full set of headers for API requests."""
        base = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "cryptachain-python/0.1.0",
        }
        base.update(self.headers)
        return base
