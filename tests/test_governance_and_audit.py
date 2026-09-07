from pathlib import Path

from app.audit import AuditTrail
from app.governance import ApprovalState, GovernanceEngine
from app.schemas import RemediationAction, RiskTier


def test_audit_hash_chain_verifies(tmp_path: Path):
    audit = AuditTrail(tmp_path / "audit.jsonl")
    audit.record("one", {"x": 1})
    audit.record("two", {"x": 2})
    assert audit.verify() == (True, "verified")


def test_audit_hash_chain_detects_tampering(tmp_path: Path):
    path = tmp_path / "audit.jsonl"
    audit = AuditTrail(path)
    audit.record("one", {"x": 1})
    raw = path.read_text(encoding="utf-8").replace('"x": 1', '"x": 9')
    path.write_text(raw, encoding="utf-8")
    assert audit.verify()[0] is False


def test_governance_gates_medium_risk():
    action = RemediationAction(
        name="change", description="change", command="kubectl apply -f fix.yaml",
        target="namespace/monitoring", risk_tier=RiskTier.MEDIUM, dry_run=True,
        evidence_ids=["ev1"], expected_effect="fix", rollback="revert",
    )
    decision = GovernanceEngine().decide(action)
    assert decision.state == ApprovalState.HUMAN_REQUIRED
