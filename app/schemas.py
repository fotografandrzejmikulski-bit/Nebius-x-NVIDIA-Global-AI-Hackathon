from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class RiskTier(str, Enum):
    READ_ONLY = "read_only"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Evidence(BaseModel):
    evidence_id: str = Field(default_factory=lambda: f"ev-{uuid4().hex[:10]}")
    source: str
    title: str = ""
    url: str
    excerpt: str
    relevance: float = Field(ge=0.0, le=1.0, default=0.0)
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    trust_tier: str = "external"

    @field_validator("url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        if not value.startswith(("https://", "http://")):
            raise ValueError("Evidence URL must be absolute HTTP(S)")
        return value


class RemediationAction(BaseModel):
    action_id: str = Field(default_factory=lambda: f"act-{uuid4().hex[:10]}")
    name: str
    description: str
    command: str
    target: str
    risk_tier: RiskTier
    requires_confirmation: bool = False
    dry_run: bool = True
    evidence_ids: list[str] = Field(default_factory=list)
    expected_effect: str = ""
    rollback: str = ""
    preconditions: list[str] = Field(default_factory=list)
    postconditions: list[str] = Field(default_factory=list)
    idempotency_key: str = Field(default_factory=lambda: uuid4().hex)
    policy_labels: list[str] = Field(default_factory=list)


class Incident(BaseModel):
    incident_id: str = Field(default_factory=lambda: f"inc-{uuid4().hex[:10]}")
    title: str
    description: str
    environment: str = "production"
    service: str = "unknown"
    severity: str = "unknown"
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    context: dict[str, Any] = Field(default_factory=dict)


class VerificationResult(BaseModel):
    status: str
    observed: list[str] = Field(default_factory=list)
    unmet: list[str] = Field(default_factory=list)


class InvestigationResult(BaseModel):
    incident: Incident
    diagnosis: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: list[Evidence] = Field(default_factory=list)
    actions: list[RemediationAction] = Field(default_factory=list)
    blocked_actions: list[str] = Field(default_factory=list)
    governance: dict[str, str] = Field(default_factory=dict)
    verification: VerificationResult | None = None
    mode: str = "simulated"
    audit_event_ids: list[str] = Field(default_factory=list)
