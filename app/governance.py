from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.schemas import RemediationAction, RiskTier


class ApprovalState(str, Enum):
    AUTO_APPROVED = "auto_approved"
    HUMAN_REQUIRED = "human_required"
    DENIED = "denied"


@dataclass(frozen=True)
class GovernanceDecision:
    state: ApprovalState
    reasons: tuple[str, ...]


class GovernanceEngine:
    """Policy-adjacent governance: decides whether an allowed action needs a human."""

    def decide(self, action: RemediationAction) -> GovernanceDecision:
        reasons: list[str] = []
        if action.requires_confirmation:
            reasons.append("action explicitly requires human confirmation")
        if action.risk_tier in {RiskTier.MEDIUM, RiskTier.HIGH, RiskTier.CRITICAL}:
            reasons.append(f"risk tier {action.risk_tier.value} exceeds unattended comfort level")
        if not action.dry_run:
            reasons.append("non-dry-run execution requires human approval in the public prototype")
        if reasons:
            return GovernanceDecision(ApprovalState.HUMAN_REQUIRED, tuple(reasons))
        return GovernanceDecision(ApprovalState.AUTO_APPROVED, ())
