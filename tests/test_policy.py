from app.policy import PolicyEngine
from app.schemas import RemediationAction, RiskTier


def action(**kwargs):
    base = dict(
        name="test",
        description="test",
        command="kubectl auth can-i --list",
        target="namespace/monitoring",
        risk_tier=RiskTier.LOW,
        dry_run=True,
        evidence_ids=["e1"],
    )
    base.update(kwargs)
    return RemediationAction(**base)


def test_allows_scoped_dry_run_with_evidence():
    decision = PolicyEngine().evaluate(action())
    assert decision.allowed


def test_blocks_destructive_shell():
    decision = PolicyEngine().evaluate(action(command="rm -rf /"))
    assert not decision.allowed


def test_blocks_cluster_delete():
    decision = PolicyEngine().evaluate(
        action(command="kubectl delete namespace kube-system", target="cluster")
    )
    assert not decision.allowed


def test_blocks_non_read_action_without_evidence():
    decision = PolicyEngine().evaluate(action(evidence_ids=[]))
    assert not decision.allowed


def test_blocks_high_risk():
    decision = PolicyEngine().evaluate(action(risk_tier=RiskTier.HIGH))
    assert not decision.allowed
