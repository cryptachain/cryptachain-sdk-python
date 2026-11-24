"""Address screening types."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import Field

from cryptachain.types.common import CamelModel


class RiskLevel(str, Enum):
    """Risk level classification."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


class ScreeningFlag(CamelModel):
    """A single screening flag/alert."""

    flag_type: str
    description: str | None = None
    source: str | None = None
    severity: RiskLevel = RiskLevel.UNKNOWN


class ScreeningResult(CamelModel):
    """Result of screening a single address."""

    address: str
    chain: str | None = None
    risk_level: RiskLevel = RiskLevel.UNKNOWN
    risk_score: float | None = None
    sanctions_match: bool = False
    flags: list[ScreeningFlag] = Field(default_factory=list)
    screened_at: datetime | None = None


class BulkScreeningResult(CamelModel):
    """Results from bulk address screening."""

    results: list[ScreeningResult] = Field(default_factory=list)
    total: int = 0
    flagged: int = 0
