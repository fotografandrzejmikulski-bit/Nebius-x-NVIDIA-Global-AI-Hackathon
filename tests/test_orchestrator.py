from pathlib import Path

from app.config import Settings
from app.orchestrator import AgentOrchestrator
from app.schemas import Incident


def test_demo_orchestrator_runs_without_external_keys(tmp_path: Path):
    settings = Settings(
        nebius_api_key=None,
        nebius_base_url="https://api.tokenfactory.nebius.com/v1/",
        nebius_model="nvidia/nemotron-3-super-120b-a12b",
        tavily_api_key=None,
        infra_mode="simulated",
        audit_log_path=tmp_path / "audit.jsonl",
    )
    result = AgentOrchestrator(settings).investigate(
        Incident(title="demo", description="CrashLoopBackOff caused by RBAC regression")
    )
    assert result.mode == "simulated"
    assert result.confidence > 0.8
    assert result.actions
    assert all(a.dry_run for a in result.actions)
    assert (tmp_path / "audit.jsonl").exists()


def test_audit_contains_action_event(tmp_path: Path):
    settings = Settings(
        nebius_api_key=None,
        nebius_base_url="https://api.tokenfactory.nebius.com/v1/",
        nebius_model="nvidia/nemotron-3-super-120b-a12b",
        tavily_api_key=None,
        infra_mode="simulated",
        audit_log_path=tmp_path / "audit.jsonl",
    )
    AgentOrchestrator(settings).investigate(
        Incident(title="demo", description="RBAC incident")
    )
    data = (tmp_path / "audit.jsonl").read_text(encoding="utf-8")
    assert "action.executed" in data
