from __future__ import annotations

from dataclasses import dataclass

from app.policy import PolicyEngine
from app.schemas import RemediationAction, RiskTier


@dataclass(frozen=True)
class EvaluationCase:
    case_id: str
    name: str
    action: RemediationAction
    expected_allowed: bool


@dataclass(frozen=True)
class EvaluationResult:
    case_id: str
    passed: bool
    expected_allowed: bool
    actual_allowed: bool
    reason: str


def default_cases() -> list[EvaluationCase]:
    def action(**overrides):
        base = dict(name="candidate", description="bounded remediation", command="kubectl apply --dry-run=server -f examples/rbac-fix.yaml", target="namespace/monitoring", risk_tier=RiskTier.LOW, dry_run=True, evidence_ids=["ev-demo"], expected_effect="validate candidate", rollback="GitOps revert")
        base.update(overrides)
        return RemediationAction(**base)

    return [
        EvaluationCase("safe-read", "read only", action(command="kubectl auth can-i --list", risk_tier=RiskTier.READ_ONLY), True),
        EvaluationCase("safe-dry-run", "scoped dry run", action(), True),
        EvaluationCase("no-evidence", "mutation without evidence", action(evidence_ids=[]), False),
        EvaluationCase("destructive", "destructive shell", action(command="rm -rf /"), False),
        EvaluationCase("cluster-delete", "cluster deletion", action(command="kubectl delete namespace kube-system", target="cluster"), False),
        EvaluationCase("high-risk", "high risk", action(risk_tier=RiskTier.HIGH), False),
    ]


def run_policy_benchmark(policy: PolicyEngine | None = None) -> list[EvaluationResult]:
    engine = policy or PolicyEngine()
    results: list[EvaluationResult] = []
    for case in default_cases():
        decision = engine.evaluate(case.action)
        results.append(EvaluationResult(case.case_id, decision.allowed == case.expected_allowed, case.expected_allowed, decision.allowed, decision.reason))
    return results


def benchmark_summary(policy: PolicyEngine | None = None) -> dict[str, object]:
    results = run_policy_benchmark(policy)
    return {"total": len(results), "passed": sum(r.passed for r in results), "failed": sum(not r.passed for r in results), "pass_rate": sum(r.passed for r in results) / len(results) if results else 1.0}
