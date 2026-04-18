"""Health resource — system status, chain status, methodology."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cryptachain.types.common import CamelModel, Chain

if TYPE_CHECKING:
    from cryptachain.client import AsyncHttpClient, HttpClient


class ServiceStatus(CamelModel):
    """Overall service health status."""

    status: str  # "healthy", "degraded", "down"
    version: str | None = None
    uptime: str | None = None
    services: dict[str, Any] | None = None


class ChainStatus(CamelModel):
    """Sync status for a single chain."""

    chain_id: int
    name: str | None = None
    status: str | None = None  # "synced", "syncing", "error"
    latest_block: int | None = None
    synced_block: int | None = None
    lag_seconds: int | None = None


class Methodology(CamelModel):
    """Pricing methodology documentation."""

    version: str | None = None
    description: str | None = None
    sources: list[str] | None = None
    fair_value_hierarchy: dict[str, Any] | None = None


class HealthResource:
    """Synchronous health and status operations.

    Access via ``client.health``.
    """

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get_system_status(self) -> ServiceStatus:
        """Get overall system health status.

        Returns:
            ServiceStatus with health indicators for all services.
        """
        data = self._http.get("/v1/status/services")
        return ServiceStatus.model_validate(data)

    def get_chain_status(self) -> list[ChainStatus]:
        """Get sync status for all supported chains.

        Returns:
            List of ChainStatus objects with sync progress.
        """
        data = self._http.get("/v1/status/chains")
        items = data.get("chains", data) if isinstance(data, dict) else data
        return [ChainStatus.model_validate(c) for c in items]

    def get_chains(self) -> list[Chain]:
        """List all supported blockchain chains.

        Returns:
            List of Chain objects with chain IDs and metadata.
        """
        data = self._http.get("/v1/chains")
        items = data.get("chains", data) if isinstance(data, dict) else data
        return [Chain.model_validate(c) for c in items]

    def get_methodology(self) -> Methodology:
        """Get the pricing methodology documentation.

        Returns:
            Methodology with version, description, and source details.
        """
        data = self._http.get("/v1/methodology")
        return Methodology.model_validate(data)


class AsyncHealthResource:
    """Asynchronous health and status operations.

    Access via ``client.health`` on an ``AsyncCryptaChain`` instance.
    """

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get_system_status(self) -> ServiceStatus:
        """Get overall system health status."""
        data = await self._http.get("/v1/status/services")
        return ServiceStatus.model_validate(data)

    async def get_chain_status(self) -> list[ChainStatus]:
        """Get sync status for all supported chains."""
        data = await self._http.get("/v1/status/chains")
        items = data.get("chains", data) if isinstance(data, dict) else data
        return [ChainStatus.model_validate(c) for c in items]

    async def get_chains(self) -> list[Chain]:
        """List all supported blockchain chains."""
        data = await self._http.get("/v1/chains")
        items = data.get("chains", data) if isinstance(data, dict) else data
        return [Chain.model_validate(c) for c in items]

    async def get_methodology(self) -> Methodology:
        """Get the pricing methodology documentation."""
        data = await self._http.get("/v1/methodology")
        return Methodology.model_validate(data)
