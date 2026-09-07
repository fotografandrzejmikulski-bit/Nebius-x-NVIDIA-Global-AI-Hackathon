from __future__ import annotations

from app.schemas import InvestigationResult


def render_result(result: InvestigationResult) -> str:
    lines = [
        "INFRA SENTINEL — INCIDENT REPORT",
        "=" * 44,
        f"Incident:   {result.incident.title}",
        f"Service:    {result.incident.service}",
        f"Mode:       {result.mode}",
        f"Confidence: {result.confidence:.0%}",
        "",
        "DIAGNOSIS",
        result.diagnosis,
        "",
        f"EVIDENCE: {len(result.evidence)} source(s)",
    ]
    for evidence in result.evidence[:5]:
        lines.append(f"  - {evidence.title or evidence.url} :: {evidence.url}")
    lines += ["", f"ALLOWED ACTIONS: {len(result.actions)}"]
    for action in result.actions:
        lines.append(
            f"  - [{action.risk_tier.value}] {action.name} -> {action.target} | {action.command}"
        )
    lines += ["", f"BLOCKED ACTIONS: {len(result.blocked_actions)}"]
    for blocked in result.blocked_actions:
        lines.append(f"  - {blocked}")
    return "\n".join(lines)
