from app.policy import PolicyEngine
from app.schemas import RemediationAction, RiskTier


def action(command: str, *, target: str = "namespace/monitoring", risk: RiskTier = RiskTier.LOW, evidence=None):
    return RemediationAction(
        name="candidate",
        description="test",
        command=command,
        target=target,
        risk_tier=risk,
        evidence_ids=evidence or ["e1"],
        rollback="revert",
        dry_run=True,
    )


def test_blocks_destructive_commands():
    policy = PolicyEngine()
    for command in [
        "rm -rf /",
        "kubectl delete namespace kube-system",
        "terraform destroy",
        "DROP TABLE incidents",
    ]:
        decision = policy.evaluate(action(command))
        assert not decision.allowed


def test_requires_evidence_for_mutation():
    policy = PolicyEngine()
    decision = policy.evaluate(action("kubectl apply --dry-run=server -f fix.yaml", evidence=[]))
    assert not decision.allowed
    assert "evidence" in decision.reason.lower()


def test_blocks_high_risk_autonomy():
    policy = PolicyEngine()
    decision = policy.evaluate(action("kubectl rollout restart deployment/app", risk=RiskTier.HIGH))
    assert not decision.allowed


def test_allows_scoped_read_only():
    policy = PolicyEngine()
    decision = policy.evaluate(action(
        "kubectl auth can-i --list --as=system:serviceaccount:monitoring:incident-agent",
        risk=RiskTier.READ_ONLY,
        evidence=[],
    ))
    assert decision.allowed
