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
    """Human-governance boundary after deterministic authorization.

    Authorization answers: "is this action technically inside the allowed policy envelope?"
    Governance answers: "may this otherwise-allowed action proceed unattended?"
    Execution is intentionally a separate responsibility.
    """

    def decide(self, action: RemediationAction) -> GovernanceDecision:
        reasons: list[str] = []

        if action.requires_confirmation:
            reasons.append("action explicitly requires human confirmation")

        if action.risk_tier in {RiskTier.MEDIUM, RiskTier.HIGH, RiskTier.CRITICAL}:
            reasons.append(f"risk tier {action.risk_tier.value} requires human-governed promotion")

        if not action.dry_run:
            reasons.append("live execution requires human approval in the public prototype")

        if not action.rollback:
            reasons.append("mutation without rollback guidance cannot proceed unattended")

        if reasons:
            return GovernanceDecision(ApprovalState.HUMAN_REQUIRED, tuple(reasons))

        return GovernanceDecision(ApprovalState.AUTO_APPROVED, ())
