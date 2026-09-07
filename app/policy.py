from __future__ import annotations

import re
from dataclasses import dataclass

from app.schemas import RemediationAction, RiskTier


DESTRUCTIVE_PATTERNS = [
    r"\brm\s+-rf\b",
    r"\bkubectl\s+delete\b",
    r"\bkubectl\s+delete\s+namespace\s+kube-system\b",
    r"\bDROP\s+(DATABASE|TABLE)\b",
    r"\bterraform\s+destroy\b",
    r"\bshutdown\s+.*production\b",
    r"\bdelete\s+.*production\b",
]


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str
    normalized_command: str


class PolicyEngine:
    """Deterministic action policy. AI proposes; policy decides."""

    def __init__(self, max_allowed_risk: RiskTier = RiskTier.MEDIUM) -> None:
        self.max_allowed_risk = max_allowed_risk
        self._risk_order = {
            RiskTier.READ_ONLY: 0,
            RiskTier.LOW: 1,
            RiskTier.MEDIUM: 2,
            RiskTier.HIGH: 3,
            RiskTier.CRITICAL: 4,
        }

    def evaluate(self, action: RemediationAction) -> PolicyDecision:
        command = " ".join(action.command.strip().split())
        lowered = command.lower()
        for pattern in DESTRUCTIVE_PATTERNS:
            if re.search(pattern, lowered, flags=re.IGNORECASE):
                return PolicyDecision(False, f"destructive pattern matched: {pattern}", command)

        if action.risk_tier in {RiskTier.HIGH, RiskTier.CRITICAL}:
            return PolicyDecision(False, "high-impact actions are not autonomous in this prototype", command)

        if self._risk_order[action.risk_tier] > self._risk_order[self.max_allowed_risk]:
            return PolicyDecision(False, "risk tier exceeds autonomous policy boundary", command)

        if not action.evidence_ids and action.risk_tier != RiskTier.READ_ONLY:
            return PolicyDecision(False, "non-read action requires linked evidence", command)

        if action.target in {"cluster", "database", "production"} and action.risk_tier != RiskTier.READ_ONLY:
            return PolicyDecision(False, "broad production scope requires human-controlled change management", command)

        return PolicyDecision(True, "action is inside autonomous policy envelope", command)

    def evaluate_many(self, actions: list[RemediationAction]) -> tuple[list[RemediationAction], list[str]]:
        allowed: list[RemediationAction] = []
        blocked: list[str] = []
        for action in actions:
            decision = self.evaluate(action)
            if decision.allowed:
                action.command = decision.normalized_command
                allowed.append(action)
            else:
                blocked.append(f"{action.name}: {decision.reason}")
        return allowed, blocked
