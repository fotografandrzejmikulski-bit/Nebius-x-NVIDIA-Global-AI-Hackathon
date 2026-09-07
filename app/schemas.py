from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class RiskTier(str, Enum):
    READ_ONLY = "read_only"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Evidence(BaseModel):
    source: str
    title: str = ""
    url: str
    excerpt: str
    relevance: float = Field(ge=0.0, le=1.0, default=0.0)


class RemediationAction(BaseModel):
    action_id: str = Field(default_factory=lambda: str(uuid4()))
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


class Incident(BaseModel):
    incident_id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: str
    environment: str = "production"
    service: str = "unknown"
    severity: str = "unknown"
    observed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    context: dict[str, Any] = Field(default_factory=dict)


class InvestigationResult(BaseModel):
    incident: Incident
    diagnosis: str
    confidence: float = Field(ge=0.0, le=1.0)
    evidence: list[Evidence] = Field(default_factory=list)
    actions: list[RemediationAction] = Field(default_factory=list)
    blocked_actions: list[str] = Field(default_factory=list)
    mode: str = "simulated"
    audit_event_ids: list[str] = Field(default_factory=list)
